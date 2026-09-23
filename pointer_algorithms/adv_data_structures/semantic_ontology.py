"""
CHUP Phase 3S — Semantic Advanced Data Structures Ontology & Provenance Model.

Defines composable algebraic properties, structural graph topology states,
path value domains, persistence and mutability models, order-statistic query objectives,
Mo's ordering strategies, segment tree beats tags, coordinate intervals, provider capabilities,
and derived facts with complete provenance tracking.
Zero monolithic algorithm names or rigid category heuristics in the ontology.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Set
import math


# ── 1. Composable Algebraic Properties ──

@dataclass
class AlgebraicProperties:
    """
    Models algebraic properties of associative operations composably.
    Sparse Table O(1) query strictly requires associative=True and idempotent=True.
    Invertible operations enable prefix/difference mechanisms.
    """
    associative: bool = True
    commutative: bool = True
    idempotent: bool = False
    invertible: bool = False
    has_identity: bool = False
    identity_element: Optional[Any] = None

    @classmethod
    def min_operation(cls) -> "AlgebraicProperties":
        return cls(associative=True, commutative=True, idempotent=True, invertible=False, has_identity=True, identity_element=float('inf'))

    @classmethod
    def max_operation(cls) -> "AlgebraicProperties":
        return cls(associative=True, commutative=True, idempotent=True, invertible=False, has_identity=True, identity_element=float('-inf'))

    @classmethod
    def gcd_operation(cls) -> "AlgebraicProperties":
        return cls(associative=True, commutative=True, idempotent=True, invertible=False, has_identity=True, identity_element=0)

    @classmethod
    def bitwise_and_operation(cls) -> "AlgebraicProperties":
        return cls(associative=True, commutative=True, idempotent=True, invertible=False, has_identity=True, identity_element=-1)

    @classmethod
    def bitwise_or_operation(cls) -> "AlgebraicProperties":
        return cls(associative=True, commutative=True, idempotent=True, invertible=False, has_identity=True, identity_element=0)

    @classmethod
    def sum_operation(cls) -> "AlgebraicProperties":
        return cls(associative=True, commutative=True, idempotent=False, invertible=True, has_identity=True, identity_element=0)

    @classmethod
    def xor_operation(cls) -> "AlgebraicProperties":
        return cls(associative=True, commutative=True, idempotent=False, invertible=True, has_identity=True, identity_element=0)


# ── 2. Graph Topology Derived State ──

class GraphTopologyState(str, Enum):
    VALID_TREE = "VALID_TREE"
    CYCLIC = "CYCLIC"
    DISCONNECTED = "DISCONNECTED"
    EMPTY = "EMPTY"


# ── 3. Path Value Domain (HLD) ──

class PathValueDomain(str, Enum):
    VERTEX_VALUES = "VERTEX_VALUES"   # Values on vertices; path u<->v includes LCA(u,v)
    EDGE_VALUES = "EDGE_VALUES"       # Values on edges; edge(p,c) mapped to child c; LCA(u,v) excluded


# ── 4. Temporal & Persistence Models ──

class QueryMode(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class PersistenceMode(str, Enum):
    NONE = "NONE"
    PARTIALLY_PERSISTENT = "PARTIALLY_PERSISTENT"
    FULLY_PERSISTENT = "FULLY_PERSISTENT"


class StructureMutability(str, Enum):
    STATIC = "STATIC"                             # Immutable once constructed (e.g. MergeSortTree, static SparseTable)
    EPHEMERAL_MUTABLE = "EPHEMERAL_MUTABLE"       # Mutable in-place, past versions lost
    PERSISTENT = "PERSISTENT"                     # Past versions preserved in a rooted version tree


# ── 5. Order Statistics & Range Query Objectives ──

class RangeOrderStatisticObjective(str, Enum):
    COUNT_LEQ = "COUNT_LEQ"                       # Count elements in [L, R] <= X
    COUNT_LT = "COUNT_LT"                         # Count elements in [L, R] < X
    COUNT_GE = "COUNT_GE"                         # Count elements in [L, R] >= X
    COUNT_RANGE = "COUNT_RANGE"                   # Count elements in [L, R] in [X, Y]


# ── 6. Mo's Scheduling & Transition Models ──

class MoOrderingStrategy(str, Enum):
    STANDARD_BLOCK_SNAKE = "STANDARD_BLOCK_SNAKE"
    HILBERT_CURVE = "HILBERT_CURVE"


@dataclass
class TransitionCost:
    add_cost: str = "O(1)"
    remove_cost: str = "O(1)"
    is_reversible: bool = True                    # Verified mathematically: remove(add(S, x), x) == S


# ── 7. Segment Tree Beats Tag State & Current Max Hierarchy ──

@dataclass
class BeatsTagState:
    max1: float = float('-inf')                   # Current strictly largest value
    max2: float = float('-inf')                   # Current strictly second largest value (-inf if leaf/single-valued)
    cnt_max: int = 1                              # Multiplicity of max1
    has_second_max: bool = False                  # True iff at least 2 distinct values exist in subtree range


# ── 8. Coordinate Domains & Scale ──

@dataclass
class CoordinateDomain:
    lower: int = 1
    upper: int = 10**18

    def midpoint(self, l: int, r: int) -> int:
        """Overflow-safe midpoint calculation."""
        return l + (r - l) // 2

    @property
    def max_depth(self) -> int:
        length = max(1, self.upper - self.lower + 1)
        return math.ceil(math.log2(length))


# ── 9. Provider Capabilities & Complexity ──

class ProviderCapability(str, Enum):
    RANGE_QUERY = "RANGE_QUERY"
    RANGE_UPDATE = "RANGE_UPDATE"
    POINT_UPDATE = "POINT_UPDATE"


@dataclass
class ProviderComplexity:
    build_complexity: str = "O(N)"
    query_complexity: str = "O(log N)"
    update_complexity: str = "O(log N)"


# ── 10. Phase 3S Canonical Objectives ──

class AdvancedDataStructureObjective(str, Enum):
    SPARSE_TABLE_RMQ = "SPARSE_TABLE_RMQ"                         # 3S-A
    LCA_BINARY_LIFTING = "LCA_BINARY_LIFTING"                     # 3S-B
    HEAVY_LIGHT_DECOMPOSITION = "HEAVY_LIGHT_DECOMPOSITION"       # 3S-C
    CENTROID_DECOMPOSITION = "CENTROID_DECOMPOSITION"             # 3S-D
    PERSISTENT_SEGMENT_TREE = "PERSISTENT_SEGMENT_TREE"           # 3S-E
    DYNAMIC_SEGMENT_TREE = "DYNAMIC_SEGMENT_TREE"                 # 3S-F
    MERGE_SORT_TREE = "MERGE_SORT_TREE"                           # 3S-G
    SQRT_DECOMPOSITION = "SQRT_DECOMPOSITION"                     # 3S-H
    MOS_ALGORITHM = "MOS_ALGORITHM"                               # 3S-I
    SEGMENT_TREE_BEATS = "SEGMENT_TREE_BEATS"                     # 3S-J


# ── 11. Provenance Records & Semantic Model ──

@dataclass
class DerivedFact:
    fact_type: str
    evidence: str
    confidence: float = 1.0
    source_component: str = "semantic_extractor"


@dataclass
class SemanticAdvancedDataStructureModel:
    """
    Structured problem model capturing orthogonal algebraic, topological,
    temporal, and query dimensions for advanced data structures.
    """
    objective: Optional[AdvancedDataStructureObjective] = None
    algebraic_properties: AlgebraicProperties = field(default_factory=AlgebraicProperties.min_operation)
    topology_state: GraphTopologyState = GraphTopologyState.VALID_TREE
    path_value_domain: PathValueDomain = PathValueDomain.VERTEX_VALUES
    persistence_mode: PersistenceMode = PersistenceMode.NONE
    mutability: StructureMutability = StructureMutability.STATIC
    order_statistic_objective: RangeOrderStatisticObjective = RangeOrderStatisticObjective.COUNT_LEQ
    mo_ordering_strategy: MoOrderingStrategy = MoOrderingStrategy.STANDARD_BLOCK_SNAKE
    transition_cost: TransitionCost = field(default_factory=TransitionCost)
    coordinate_domain: CoordinateDomain = field(default_factory=CoordinateDomain)
    query_mode: QueryMode = QueryMode.ONLINE
    beats_supported_ops: Set[str] = field(default_factory=lambda: {"RANGE_CHMIN", "RANGE_SUM_QUERY", "RANGE_MAX_QUERY"})
    provider_capabilities: Set[ProviderCapability] = field(default_factory=lambda: {ProviderCapability.RANGE_QUERY})
    provider_complexity: ProviderComplexity = field(default_factory=ProviderComplexity)
    derived_facts: List[DerivedFact] = field(default_factory=list)

    def add_fact(self, fact_type: str, evidence: str, confidence: float = 1.0, source: str = "semantic_extractor"):
        self.derived_facts.append(DerivedFact(fact_type, evidence, confidence, source))

    def has_derived_fact(self, fact_type: str) -> bool:
        return any(f.fact_type == fact_type for f in self.derived_facts)

    def get_fact(self, fact_type: str) -> Optional[DerivedFact]:
        for f in self.derived_facts:
            if f.fact_type == fact_type:
                return f
        return None
