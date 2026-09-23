"""
CHUP Phase 5 — Constraint Lattice & Predicate Representation.

Encodes orthogonal problem dimensions as capability predicates,
decoupled from rigid enum orderings. Implements singleton range reduction
(RANGE_WRITE -> POINT_WRITE), axiomatic topology invariants,
and parameter-dependent coordinate scale feasibility.
"""

from enum import Enum, auto
from typing import Dict, Any, List, Optional, Set, FrozenSet, Tuple, Callable
from dataclasses import dataclass, field


class TemporalMode(Enum):
    """Execution/query stream temporal semantics."""
    ONLINE = "ONLINE"          # Queries/updates arrive interleaved; each must be answered immediately
    OFFLINE = "OFFLINE"        # All queries/updates known in advance; reordering/sorting permitted
    STREAMING = "STREAMING"    # Sequential online stream under sublinear memory constraint
    ANY = "ANY"

    def is_compatible_with(self, candidate_mode: "TemporalMode") -> bool:
        if self == TemporalMode.ANY or candidate_mode == TemporalMode.ANY:
            return True
        if self == TemporalMode.STREAMING:
            return candidate_mode in (TemporalMode.STREAMING, TemporalMode.ONLINE)
        return self == candidate_mode


class MutabilityCapability(Enum):
    """Atomic mutation capabilities supported by data structures."""
    READ = "READ"
    POINT_WRITE = "POINT_WRITE"
    RANGE_WRITE = "RANGE_WRITE"
    STRUCTURAL_INSERT = "STRUCTURAL_INSERT"
    STRUCTURAL_DELETE = "STRUCTURAL_DELETE"


@dataclass(frozen=True)
class MutabilitySet:
    """
    Set of mutability capabilities.
    Encodes capability relations: RANGE_WRITE satisfies POINT_WRITE via singleton ranges [i, i].
    """
    capabilities: FrozenSet[MutabilityCapability] = frozenset([MutabilityCapability.READ])

    @classmethod
    def read_only(cls) -> "MutabilitySet":
        return cls(frozenset([MutabilityCapability.READ]))

    @classmethod
    def point_update(cls) -> "MutabilitySet":
        return cls(frozenset([MutabilityCapability.READ, MutabilityCapability.POINT_WRITE]))

    @classmethod
    def range_update(cls) -> "MutabilitySet":
        # A structure with range write natively supports point write
        return cls(frozenset([
            MutabilityCapability.READ,
            MutabilityCapability.POINT_WRITE,
            MutabilityCapability.RANGE_WRITE
        ]))

    @classmethod
    def fully_dynamic(cls) -> "MutabilitySet":
        return cls(frozenset([
            MutabilityCapability.READ,
            MutabilityCapability.POINT_WRITE,
            MutabilityCapability.RANGE_WRITE,
            MutabilityCapability.STRUCTURAL_INSERT,
            MutabilityCapability.STRUCTURAL_DELETE
        ]))

    def satisfies(self, required: MutabilityCapability) -> bool:
        """
        Evaluates whether this mutability set satisfies a required mutability capability.
        Supports singleton range reduction: RANGE_WRITE satisfies POINT_WRITE.
        """
        if required in self.capabilities:
            return True
        if required == MutabilityCapability.POINT_WRITE and MutabilityCapability.RANGE_WRITE in self.capabilities:
            return True
        return False

    def is_static(self) -> bool:
        return self.capabilities == frozenset([MutabilityCapability.READ])


class Directedness(Enum):
    DIRECTED = "DIRECTED"
    UNDIRECTED = "UNDIRECTED"
    ANY = "ANY"


class Connectedness(Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    ANY = "ANY"


class Cyclicity(Enum):
    ACYCLIC = "ACYCLIC"
    CYCLIC = "CYCLIC"
    ANY = "ANY"


class Simplicity(Enum):
    SIMPLE = "SIMPLE"
    MULTIGRAPH = "MULTIGRAPH"
    ANY = "ANY"


class Rootedness(Enum):
    ROOTED = "ROOTED"
    UNROOTED = "UNROOTED"
    ANY = "ANY"


@dataclass(frozen=True)
class TopologyDomain:
    """
    Axiomatic topology model. Invariants are derived from axioms rather than
    hardcoded as arbitrary labels.
    """
    directedness: Directedness = Directedness.ANY
    connectedness: Connectedness = Connectedness.ANY
    cyclicity: Cyclicity = Cyclicity.ANY
    simplicity: Simplicity = Simplicity.ANY
    rootedness: Rootedness = Rootedness.ANY
    vertex_count: Optional[int] = None
    edge_count: Optional[int] = None

    @classmethod
    def arbitrary(cls) -> "TopologyDomain":
        return cls()

    @classmethod
    def undirected_tree(cls, v: Optional[int] = None, e: Optional[int] = None) -> "TopologyDomain":
        return cls(
            directedness=Directedness.UNDIRECTED,
            connectedness=Connectedness.CONNECTED,
            cyclicity=Cyclicity.ACYCLIC,
            simplicity=Simplicity.SIMPLE,
            rootedness=Rootedness.ROOTED,
            vertex_count=v,
            edge_count=e
        )

    def is_undirected_tree(self) -> bool:
        return (
            self.directedness == Directedness.UNDIRECTED and
            self.connectedness == Connectedness.CONNECTED and
            self.cyclicity == Cyclicity.ACYCLIC and
            self.simplicity == Simplicity.SIMPLE
        )

    def derive_invariants(self) -> List[Tuple[str, str]]:
        """
        Derives mathematical invariants and flags contradictions.
        Returns list of (invariant_id, message).
        """
        invariants = []
        if self.is_undirected_tree() and self.vertex_count is not None:
            expected_edges = max(0, self.vertex_count - 1)
            invariants.append((
                "TREE_EDGE_COUNT_THEOREM",
                f"An undirected connected acyclic simple graph with V={self.vertex_count} vertices has exactly E={expected_edges} edges"
            ))
            if self.edge_count is not None and self.edge_count != expected_edges:
                invariants.append((
                    "AXIOMATIC_TREE_EDGE_COUNT_CONTRADICTION",
                    f"Axiomatic tree contradiction: expected E={expected_edges} but got E={self.edge_count}"
                ))
        return invariants


class CoordinateScale(Enum):
    """
    Coordinate domain scale.
    Dense feasibility is parameter-dependent, not hardcoded to N <= 10^6.
    """
    DENSE = "DENSE"        # Can be indexed directly given memory budget
    SPARSE = "SPARSE"      # Bounded range with sparse values; compression advantageous
    MASSIVE = "MASSIVE"    # Huge coordinate domain (up to 10^18) requiring dynamic or compressed representation

    @staticmethod
    def is_dense_feasible(domain_size: int, element_size_bytes: int, memory_budget_bytes: int) -> bool:
        """Computes whether direct dense indexing fits within the memory budget."""
        if domain_size <= 0 or memory_budget_bytes <= 0:
            return False
        return (domain_size * element_size_bytes) <= memory_budget_bytes


class ConstraintPolarity(Enum):
    REQUIRED = "REQUIRED"
    FORBIDDEN = "FORBIDDEN"


@dataclass(frozen=True)
class Constraint:
    """
    Formal predicate-based constraint.
    """
    dimension: str              # "TEMPORAL", "MUTABILITY", "COORDINATES", "TOPOLOGY", "RESOURCE", "ALGEBRA", "QUERY"
    name: str
    polarity: ConstraintPolarity
    description: str
    parameterized_bounds: Dict[str, Any] = field(default_factory=dict)
    relational_dependencies: List[str] = field(default_factory=list)
    witness: str = ""

    def is_required(self) -> bool:
        return self.polarity == ConstraintPolarity.REQUIRED

    def is_forbidden(self) -> bool:
        return self.polarity == ConstraintPolarity.FORBIDDEN


@dataclass
class MultiConstraintVector:
    """
    Multidimensional constraint state container representing the intersection
    of all active problem constraints.
    """
    temporal: TemporalMode = TemporalMode.ANY
    mutability: MutabilitySet = field(default_factory=MutabilitySet.read_only)
    topology: TopologyDomain = field(default_factory=TopologyDomain.arbitrary)
    coordinate_scale: CoordinateScale = CoordinateScale.DENSE
    coordinate_max: Optional[int] = None
    time_limit_ms: int = 1000
    memory_limit_mb: int = 256
    constraints: List[Constraint] = field(default_factory=list)

    def add_constraint(self, c: Constraint) -> None:
        self.constraints.append(c)

    def has_constraint(self, name: str) -> bool:
        return any(c.name == name for c in self.constraints)

    def get_constraints_by_dimension(self, dimension: str) -> List[Constraint]:
        return [c for c in self.constraints if c.dimension == dimension]
