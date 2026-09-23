"""
CHUP Phase 4: Formal Component Model, Typed State Contracts & Attribute Lattice.

Core Principles:
1. Universal StateContract: Formal state representation with asymmetric satisfaction.
2. 3-Valued Property Logic: PROVEN_PRESENT, PROVEN_ABSENT, UNKNOWN.
3. SemanticAttribute: Typed, domain-validated attributes preventing untyped escape hatches.
4. MutationCompatibilityMatrix: Explicit operational mutability and ownership contracts.
5. AttributeLattice: Formal relation lattice (IS-A, HAS, REQUIRES, EXCLUDES, IMPLIES, DERIVES).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Set, Tuple


# ── 1. 3-Valued Logic for Structural Properties ──

class PropertyProofStatus(str, Enum):
    PROVEN_PRESENT = "PROVEN_PRESENT"
    PROVEN_ABSENT = "PROVEN_ABSENT"
    UNKNOWN = "UNKNOWN"

    def is_proven_present(self) -> bool:
        return self == PropertyProofStatus.PROVEN_PRESENT

    def is_proven_absent(self) -> bool:
        return self == PropertyProofStatus.PROVEN_ABSENT

    def is_unknown(self) -> bool:
        return self == PropertyProofStatus.UNKNOWN


# ── 2. Typed Semantic Attributes ──

class AttributeDomainType(str, Enum):
    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"
    ORDERING = "ORDERING"
    TOPOLOGY = "TOPOLOGY"
    OBJECTIVE = "OBJECTIVE"
    WEIGHT_KIND = "WEIGHT_KIND"
    ALGEBRAIC_OP = "ALGEBRAIC_OP"
    PREDICATE_DIR = "PREDICATE_DIR"
    STRING = "STRING"
    DIRECTEDNESS = "DIRECTEDNESS"
    CONNECTEDNESS = "CONNECTEDNESS"
    CYCLICITY = "CYCLICITY"
    SIGN_CONSTRAINT = "SIGN_CONSTRAINT"
    STORAGE_SEMANTICS = "STORAGE_SEMANTICS"


# ── Orthogonal Topology Dimensions ──

class Directedness(str, Enum):
    DIRECTED = "DIRECTED"
    UNDIRECTED = "UNDIRECTED"
    ANY = "ANY"


class Connectedness(str, Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    ANY = "ANY"


class DirectedConnectivity(str, Enum):
    STRONGLY_CONNECTED = "STRONGLY_CONNECTED"
    NOT_STRONGLY_CONNECTED = "NOT_STRONGLY_CONNECTED"
    ANY = "ANY"


class VertexConnectivity(str, Enum):
    BICONNECTED = "BICONNECTED"
    NOT_BICONNECTED = "NOT_BICONNECTED"
    ANY = "ANY"


class Cyclicity(str, Enum):
    ACYCLIC = "ACYCLIC"
    CYCLIC = "CYCLIC"
    ANY = "ANY"


class Rootedness(str, Enum):
    ROOTED = "ROOTED"
    UNROOTED = "UNROOTED"
    ANY = "ANY"


# ── Orthogonal Weight Domain & Sign Constraints ──

class WeightDomain(str, Enum):
    UNIT = "UNIT"
    INTEGER = "INTEGER"
    RATIONAL = "RATIONAL"
    REAL = "REAL"


class SignConstraint(str, Enum):
    STRICTLY_POSITIVE = "STRICTLY_POSITIVE"  # w > 0
    NON_NEGATIVE = "NON_NEGATIVE"            # w >= 0
    ARBITRARY_SIGN = "ARBITRARY_SIGN"        # w in (-inf, +inf)


# ── Mathematical Domain vs Machine Representation ──

class MathematicalDomain(str, Enum):
    INTEGER = "INTEGER"
    RATIONAL = "RATIONAL"
    REAL_APPROX = "REAL_APPROX"
    MODULAR = "MODULAR"


class MachineRepresentation(str, Enum):
    INT32 = "INT32"
    INT64 = "INT64"
    INT128 = "INT128"
    DOUBLE = "DOUBLE"
    LONG_DOUBLE = "LONG_DOUBLE"

    def can_safely_cast_to(self, target: "MachineRepresentation") -> bool:
        """Asymmetric numeric promotion compatibility."""
        if self == target:
            return True
        if self == MachineRepresentation.INT32 and target in (MachineRepresentation.INT64, MachineRepresentation.INT128):
            return True
        if self == MachineRepresentation.INT64 and target == MachineRepresentation.INT128:
            return True
        if self == MachineRepresentation.DOUBLE and target == MachineRepresentation.LONG_DOUBLE:
            return True
        return False


# Backward-compatible alias
NumericDomain = MachineRepresentation


@dataclass
class SemanticAttribute:
    """
    Strongly typed, domain-validated attribute preventing untyped string escapes.
    """
    name: str
    domain_type: AttributeDomainType
    value: Any
    provenance: Optional[str] = None
    confidence_status: str = "PROVEN"

    def is_compatible_with(self, other: "SemanticAttribute") -> bool:
        if self.domain_type != other.domain_type:
            return False
        # Specific subtyping/domain compatibility rules
        if self.domain_type == AttributeDomainType.WEIGHT_KIND:
            # NON_NEGATIVE or STRICTLY_POSITIVE satisfies ARBITRARY_SIGN / WEIGHTED
            if self.value in ("NON_NEGATIVE", "STRICTLY_POSITIVE", "ARBITRARY_SIGN") and other.value in ("WEIGHTED", "ARBITRARY_SIGN"):
                return True
            if self.value in ("NON_NEGATIVE", "STRICTLY_POSITIVE") and other.value == "NON_NEGATIVE":
                return True
            if self.value == other.value:
                return True
        if self.domain_type == AttributeDomainType.SIGN_CONSTRAINT:
            if other.value in (SignConstraint.ARBITRARY_SIGN.value, "ARBITRARY_SIGN"):
                return True
            if self.value in (SignConstraint.NON_NEGATIVE.value, SignConstraint.STRICTLY_POSITIVE.value, "NON_NEGATIVE", "STRICTLY_POSITIVE") and other.value in (SignConstraint.NON_NEGATIVE.value, "NON_NEGATIVE"):
                return True
        if self.domain_type == AttributeDomainType.TOPOLOGY:
            if other.value in ("GENERAL_GRAPH", "GRAPH"):
                return True
            if other.value == "TREE" and self.value in ("TREE", "CONNECTED_ACYCLIC"):
                return True
            if other.value == "DAG" and self.value in ("DAG", "DIRECTED_ACYCLIC"):
                return True
        return self.value == other.value


# ── 3. Operational State Semantics & Domains ──

class StateKind(str, Enum):
    GRAPH = "GRAPH"
    TREE = "TREE"
    SEQUENCE = "SEQUENCE"
    PARTITION = "PARTITION"
    DISTANCES = "DISTANCES"
    NUMERIC_INTERVAL = "NUMERIC_INTERVAL"
    TOPOLOGICAL_ORDER = "TOPOLOGICAL_ORDER"
    OPTIMIZATION_FRONTIER = "OPTIMIZATION_FRONTIER"
    DP_TABLE = "DP_TABLE"


# Component behavior semantics
class MutationSemantics(str, Enum):
    READ_ONLY = "READ_ONLY"      # Inspects state without alteration
    MUTATING = "MUTATING"        # In-place state modification
    CONSUMING = "CONSUMING"      # Takes exclusive ownership; destroys state downstream
    DERIVING = "DERIVING"        # Pure functional transformation creating a distinct new state


# State storage & update semantics
class StorageSemantics(str, Enum):
    IMMUTABLE = "IMMUTABLE"          # Snapshot cannot be modified
    IN_PLACE = "IN_PLACE"            # Mutable memory buffer
    COPY_ON_WRITE = "COPY_ON_WRITE"  # Modified via copy-on-write
    APPEND_ONLY = "APPEND_ONLY"      # Only additions allowed


class IndexingSemantics(str, Enum):
    ZERO_BASED = "ZERO_BASED"
    ONE_BASED = "ONE_BASED"
    ARBITRARY_ID = "ARBITRARY_ID"


class MutationCompatibilityMatrix:
    """
    Formal operational compatibility matrix between provider state semantics
    (storage + mutation) and consumer requirements.
    """
    @staticmethod
    def is_compatible(
        provider: MutationSemantics,
        consumer: MutationSemantics,
        provider_storage: StorageSemantics = StorageSemantics.IMMUTABLE
    ) -> bool:
        if consumer == MutationSemantics.READ_ONLY:
            return provider in (MutationSemantics.READ_ONLY, MutationSemantics.DERIVING)
        if consumer == MutationSemantics.CONSUMING:
            return provider in (MutationSemantics.CONSUMING, MutationSemantics.DERIVING)
        if consumer == MutationSemantics.MUTATING:
            # Cannot mutate immutable storage without copy
            if provider_storage == StorageSemantics.IMMUTABLE:
                return False
            return provider in (MutationSemantics.MUTATING, MutationSemantics.DERIVING)
        if consumer == MutationSemantics.DERIVING:
            return True
        return False


# ── 4. Attribute Lattice & Relational Constraints ──

class AttributeRelationKind(str, Enum):
    IS_A = "IS_A"           # Subtyping
    HAS = "HAS"             # Compositional feature
    REQUIRES = "REQUIRES"   # Dependency obligation
    EXCLUDES = "EXCLUDES"   # Structural incompatibility
    IMPLIES = "IMPLIES"     # Formal deduction
    DERIVES = "DERIVES"     # Constructive transformation


@dataclass
class AttributeConstraint:
    attribute_name: str
    relation: AttributeRelationKind
    target_value: Any
    is_hard_barrier: bool = True


class AttributeLattice:
    """
    Formal constraint solver over semantic attributes.
    Enforces logical implications, exclusions, and consistency.
    """
    IMPLICATIONS: Dict[Tuple[str, Any], List[Tuple[str, Any]]] = {
        ("weights", "NON_NEGATIVE"): [("weights", "WEIGHTED"), ("graph_type", "WEIGHTED_GRAPH")],
        ("topology", "TREE"): [("connectivity", "CONNECTED"), ("cyclicity", "ACYCLIC")],
        ("topology", "DAG"): [("cyclicity", "ACYCLIC")],
        ("predicate", "MONOTONE_INCREASING"): [("predicate_searchable", True)],
        ("predicate", "MONOTONE_DECREASING"): [("predicate_searchable", True)],
    }

    EXCLUSIONS: Dict[Tuple[str, Any], List[Tuple[str, Any]]] = {
        ("cyclicity", "ACYCLIC"): [("cyclicity", "CYCLIC")],
        ("connectivity", "CONNECTED"): [("connectivity", "DISCONNECTED")],
        ("weights", "NON_NEGATIVE"): [("weights", "CONTAINS_NEGATIVE")],
    }

    @classmethod
    def expand_implications(cls, attributes: Dict[str, SemanticAttribute]) -> Dict[str, SemanticAttribute]:
        """Expands attributes with all derived implications."""
        expanded = dict(attributes)
        changed = True
        while changed:
            changed = False
            for (attr_name, attr_val), implied_list in cls.IMPLICATIONS.items():
                if attr_name in expanded and expanded[attr_name].value == attr_val:
                    for imp_name, imp_val in implied_list:
                        if imp_name not in expanded:
                            domain = expanded[attr_name].domain_type
                            expanded[imp_name] = SemanticAttribute(
                                name=imp_name,
                                domain_type=domain,
                                value=imp_val,
                                provenance=f"Implied by ({attr_name}={attr_val})"
                            )
                            changed = True
        return expanded

    @classmethod
    def check_contradictions(cls, attributes: Dict[str, SemanticAttribute]) -> Tuple[bool, Optional[str]]:
        """Checks for conflicting mutually exclusive attributes."""
        for (attr_name, attr_val), excl_list in cls.EXCLUSIONS.items():
            if attr_name in attributes and attributes[attr_name].value == attr_val:
                for excl_name, excl_val in excl_list:
                    if excl_name in attributes and attributes[excl_name].value == excl_val:
                        return False, f"Contradiction: ({attr_name}={attr_val}) excludes ({excl_name}={excl_val})"
        return True, None


# ── 5. Formal StateContract ──

@dataclass
class StateContract:
    """
    Formal mathematical state representation with asymmetric satisfaction.
    """
    state_kind: StateKind
    name: str
    attributes: Dict[str, SemanticAttribute] = field(default_factory=dict)
    invariants: List[str] = field(default_factory=list)
    required_relations: List[str] = field(default_factory=list)
    forbidden_properties: Set[str] = field(default_factory=set)
    proven_properties: Dict[str, PropertyProofStatus] = field(default_factory=dict)
    mutation_semantics: MutationSemantics = MutationSemantics.READ_ONLY
    storage_semantics: StorageSemantics = StorageSemantics.IMMUTABLE
    indexing_semantics: IndexingSemantics = IndexingSemantics.ZERO_BASED
    numeric_domain: NumericDomain = NumericDomain.INT64
    mathematical_domain: MathematicalDomain = MathematicalDomain.INTEGER
    representation: MachineRepresentation = MachineRepresentation.INT64
    directedness: Directedness = Directedness.ANY
    connectedness: Connectedness = Connectedness.ANY
    directed_connectivity: DirectedConnectivity = DirectedConnectivity.ANY
    vertex_connectivity: VertexConnectivity = VertexConnectivity.ANY
    cyclicity: Cyclicity = Cyclicity.ANY
    sign_constraint: SignConstraint = SignConstraint.ARBITRARY_SIGN
    weight_domain: WeightDomain = WeightDomain.REAL
    supertypes: List[str] = field(default_factory=list)
    supported_fact_ids: List[str] = field(default_factory=list)

    def get_property_status(self, prop: str) -> PropertyProofStatus:
        return self.proven_properties.get(prop, PropertyProofStatus.UNKNOWN)

    def set_property(self, prop: str, status: PropertyProofStatus) -> None:
        self.proven_properties[prop] = status

    def satisfies(self, requirement: "StateContract") -> bool:
        """
        Determines whether self (actual provider state) satisfies requirement (consumer state).
        This relation is STRICTLY ASYMMETRIC.
        """
        # 1. State Kind compatibility
        if self.state_kind != requirement.state_kind and requirement.state_kind.value not in self.supertypes:
            return False

        # 2. Type hierarchy match
        if self.name != requirement.name and requirement.name not in self.supertypes:
            return False

        # 3. Forbidden Properties Check (3-valued logic):
        # If required_state forbids property P, and self proves P present -> FAIL
        for forbidden in requirement.forbidden_properties:
            if self.get_property_status(forbidden) == PropertyProofStatus.PROVEN_PRESENT:
                return False

        # If self forbids property P, and requirement proves P present -> FAIL
        for forbidden in self.forbidden_properties:
            if requirement.get_property_status(forbidden) == PropertyProofStatus.PROVEN_PRESENT:
                return False

        # 4. Strict Attribute Unification:
        # Every required attribute must be satisfied by self's attributes
        for req_name, req_attr in requirement.attributes.items():
            if req_name not in self.attributes:
                # Missing required attribute -> fail closed
                return False
            actual_attr = self.attributes[req_name]
            if not actual_attr.is_compatible_with(req_attr):
                return False

        # 5. Mutation & Storage Semantics Compatibility
        if not MutationCompatibilityMatrix.is_compatible(
            self.mutation_semantics,
            requirement.mutation_semantics,
            provider_storage=self.storage_semantics
        ):
            return False

        # 6. Numeric Domain Compatibility (asymmetric castability)
        if not self.numeric_domain.can_safely_cast_to(requirement.numeric_domain):
            return False

        # 7. Orthogonal Topology Compatibility
        if requirement.directedness != Directedness.ANY and self.directedness != Directedness.ANY:
            if self.directedness != requirement.directedness:
                return False
        if requirement.connectedness != Connectedness.ANY and self.connectedness != Connectedness.ANY:
            if self.connectedness != requirement.connectedness:
                return False
        if requirement.directed_connectivity != DirectedConnectivity.ANY and self.directed_connectivity != DirectedConnectivity.ANY:
            if self.directed_connectivity != requirement.directed_connectivity:
                return False
        if requirement.vertex_connectivity != VertexConnectivity.ANY and self.vertex_connectivity != VertexConnectivity.ANY:
            if self.vertex_connectivity != requirement.vertex_connectivity:
                return False
        if requirement.cyclicity != Cyclicity.ANY and self.cyclicity != Cyclicity.ANY:
            if self.cyclicity != requirement.cyclicity:
                return False

        # 8. Orthogonal Sign Constraint Compatibility
        if requirement.sign_constraint in (SignConstraint.NON_NEGATIVE, SignConstraint.STRICTLY_POSITIVE):
            if self.sign_constraint == SignConstraint.ARBITRARY_SIGN and self.get_property_status("CONTAINS_NEGATIVE_WEIGHTS") == PropertyProofStatus.PROVEN_PRESENT:
                return False

        return True


# ── 6. Composition Node & Component Model ──

class CompositionNodeType(str, Enum):
    COMPONENT = "COMPONENT"              # Executable algorithmic primitive / data structure
    TRANSFORMATION = "TRANSFORMATION"    # Pure mathematical reduction / derivation


@dataclass
class AlgorithmComponent:
    """
    Declarative capability model for a cross-family algorithmic component.
    """
    name: str
    category: str
    node_type: CompositionNodeType = CompositionNodeType.COMPONENT
    consumes_state: List[StateContract] = field(default_factory=list)
    produces_state: List[StateContract] = field(default_factory=list)
    required_operations: List[str] = field(default_factory=list)
    forbidden_properties: Set[str] = field(default_factory=set)
    proof_obligations: List[str] = field(default_factory=list)
    complexity_time: str = "O(N)"
    complexity_space: str = "O(N)"
    mutation_semantics: MutationSemantics = MutationSemantics.READ_ONLY
    implementation_backend: str = ""

    def can_consume(self, available_states: List[StateContract]) -> bool:
        """Checks if all required input states are satisfied by available_states."""
        for req in self.consumes_state:
            if not any(avail.satisfies(req) for avail in available_states):
                return False
        return True
