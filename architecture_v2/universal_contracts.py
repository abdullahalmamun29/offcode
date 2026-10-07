"""
Architecture V2: Universal Capability Contracts & Typed State Graph Infrastructure.

Defines the mathematical contracts between semantic requirements, typed states,
capability providers, resource envelopes, and VerifiedPlanIR.
Decoupled entirely from specific algorithm families or template catalogs.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Set, Type, Tuple, Callable


# ── 1. Epistemic Proof Status & Evidence ─────────────────────────────────────

class ProofStatus(str, Enum):
    PROVEN = "PROVEN"             # Formally derived from mathematical axioms or explicit input guarantees
    SUPPORTED = "SUPPORTED"       # Stated textually in natural language, but unverified mathematically
    UNPROVEN = "UNPROVEN"         # Insufficient evidence to establish truth
    CONTRADICTED = "CONTRADICTED" # Inconsistent with established axioms or explicit bounds


@dataclass(frozen=True)
class EvidenceRef:
    evidence_id: str
    source_snippet: str
    confidence: float = 1.0
    is_structural: bool = False


# ── 2. Topology Claims ───────────────────────────────────────────────────────

class TopologyKind(str, Enum):
    TREE = "TREE"
    GRAPH = "GRAPH"
    FOREST = "FOREST"
    DAG = "DAG"
    BIPARTITE = "BIPARTITE"
    UNKNOWN = "UNKNOWN"


class ConnectivityStatus(str, Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    UNKNOWN = "UNKNOWN"


class CyclicityStatus(str, Enum):
    ACYCLIC = "ACYCLIC"
    CYCLIC = "CYCLIC"
    UNKNOWN = "UNKNOWN"


class DirectionKind(str, Enum):
    UNDIRECTED = "UNDIRECTED"
    DIRECTED = "DIRECTED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class TopologyClaim:
    """
    Epistemic claim regarding graph/tree topology.
    Does not assert 'TREE' unconditionally unless formal axioms are satisfied.
    """
    graph_id: str = "main_graph"
    vertices_bound: Optional[int] = None
    edges_bound: Optional[int] = None
    is_connected: ProofStatus = ProofStatus.UNPROVEN
    is_acyclic: ProofStatus = ProofStatus.UNPROVEN
    is_directed: bool = False
    max_degree: Optional[int] = None
    evidence: List[EvidenceRef] = field(default_factory=list)
    proof_status: ProofStatus = ProofStatus.UNPROVEN

    @property
    def is_proven_tree(self) -> bool:
        if self.proof_status == ProofStatus.PROVEN:
            return True
        # Fundamental Theorem of Trees: connected + acyclic + |E| == |V| - 1
        if (self.vertices_bound is not None and self.edges_bound is not None and
            self.vertices_bound >= 1 and self.edges_bound == self.vertices_bound - 1 and
            self.is_connected == ProofStatus.PROVEN and self.is_acyclic == ProofStatus.PROVEN):
            return True
        return False


# ── 3. Multi-Tier Rooting Semantics ──────────────────────────────────────────

class RootSemanticModel(str, Enum):
    INPUT_SPECIFIED = "INPUT_SPECIFIED"       # Root vertex r is explicitly provided in input
    STRUCTURALLY_DERIVED = "STRUCTURAL"       # Root is unique fixed point (e.g. parent[r] == r or parent[r] == 0)
    ARBITRARY_COMPUTATIONAL = "ARBITRARY"     # Unrooted tree; ANY valid v in V may serve as computational root
    ALL_ROOTS_EVALUATED = "ALL_ROOTS"         # Objective requires evaluating every candidate root
    INTRINSICALLY_UNROOTED = "UNROOTED"       # Metric is unrooted (e.g. diameter, MST)
    UNKNOWN = "UNKNOWN"                       # Root choice matters to output, but is unspecified


@dataclass(frozen=True)
class RootSpec:
    model: RootSemanticModel = RootSemanticModel.UNKNOWN
    vertex: Optional[int] = None


# ── 4. Algebraic Payload Specification ───────────────────────────────────────

class CppTypeDescriptor(str, Enum):
    NONE = "void"
    INT32 = "int"
    INT64 = "long long"
    DOUBLE = "double"
    STRING = "std::string"
    CHAR = "char"
    BOOL = "bool"
    CUSTOM_STRUCT = "CustomStruct"


class AlgebraicOp(str, Enum):
    SUM = "SUM"
    MIN = "MIN"
    MAX = "MAX"
    XOR = "XOR"
    GCD = "GCD"
    CONCAT = "CONCAT"
    NONE = "NONE"


@dataclass(frozen=True)
class AlgebraicStructure:
    carrier_type: CppTypeDescriptor = CppTypeDescriptor.INT64
    operator: AlgebraicOp = AlgebraicOp.NONE
    is_associative: bool = False
    is_commutative: bool = False
    is_invertible: bool = False
    is_idempotent: bool = False
    identity_element: Optional[Any] = None
    has_total_order: bool = True
    weights_non_negative: bool = True


# ── 5. Query & Operation Requirements ────────────────────────────────────────

class QueryScope(str, Enum):
    NODE = "NODE"
    EDGE = "EDGE"
    PATH = "PATH"                     # Simple path between u and v
    SUBTREE = "SUBTREE"               # Subtree rooted at v
    GLOBAL = "GLOBAL"                 # Entire graph / metric space


class QueryAction(str, Enum):
    AGGREGATE = "AGGREGATE"           # Apply algebraic operation over scope
    EXTREMUM = "EXTREMUM"             # Find min/max over scope
    COUNT = "COUNT"                   # Count elements meeting predicate
    DISTANCE = "DISTANCE"             # Metric distance between u and v
    ANCESTOR_CHECK = "ANCESTOR_CHECK" # Relative ancestor / descendant check
    MUTATION = "MUTATION"             # Dynamic state update
    TRAVERSAL = "TRAVERSAL"           # Visit all nodes in topological / walk order
    SEARCH = "SEARCH"                 # Membership / ordered key search


class TargetDomain(str, Enum):
    VERTEX_PAYLOAD = "VERTEX_PAYLOAD"
    EDGE_PAYLOAD = "EDGE_PAYLOAD"
    TOPOLOGY_ONLY = "TOPOLOGY_ONLY"


class UpdateModel(str, Enum):
    STATIC = "STATIC"
    POINT_UPDATE = "POINT_UPDATE"
    SCOPE_UPDATE = "SCOPE_UPDATE"


class InteractivityModel(str, Enum):
    SINGLE_SHOT = "SINGLE_SHOT"
    OFFLINE_BATCH = "OFFLINE_BATCH"
    ONLINE_REPEATED = "ONLINE_REPEATED"


@dataclass(frozen=True)
class QueryRequirement:
    scope: QueryScope
    action: QueryAction
    target_domain: TargetDomain = TargetDomain.TOPOLOGY_ONLY
    algebra: AlgebraicStructure = field(default_factory=AlgebraicStructure)
    update_model: UpdateModel = UpdateModel.STATIC
    interactivity: InteractivityModel = InteractivityModel.SINGLE_SHOT
    kth_distance: Optional[int] = None


# ── 6. Strongly-Typed States ─────────────────────────────────────────────────

@dataclass(frozen=True)
class TypedStateDescriptor:
    state_type: str
    schema: Dict[str, Any] = field(default_factory=dict)

    def matches(self, other: "TypedStateDescriptor") -> bool:
        return self.state_type == other.state_type


# Canonical State Descriptors
STATE_TOPOLOGY = TypedStateDescriptor("TopologyState")
STATE_ROOTED_HIERARCHY = TypedStateDescriptor("RootedHierarchyState")
STATE_SUBTREE_SIZES = TypedStateDescriptor("SubtreeSizeState")
STATE_DEPTH_HEIGHT = TypedStateDescriptor("DepthHeightState")
STATE_ANCESTOR_TABLE = TypedStateDescriptor("AncestorTableState")
STATE_LCA = TypedStateDescriptor("LowestCommonAncestorState")
STATE_EULER_TOUR_INTERVALS = TypedStateDescriptor("EulerTourIntervalState")
STATE_HEAVY_LIGHT_CHAINS = TypedStateDescriptor("HeavyPathDecompositionState")
STATE_PREFIX_PATH_AGGREGATE = TypedStateDescriptor("PrefixPathAggregateState")
STATE_PATH_AGGREGATE = TypedStateDescriptor("PathAggregateState")
STATE_SUBTREE_DP = TypedStateDescriptor("SubtreeDPState")
STATE_ALL_ROOTS = TypedStateDescriptor("AllRootsState")
STATE_TREE_DIAMETER = TypedStateDescriptor("TreeDiameterState")
STATE_DIFFERENCE_ACCUMULATOR = TypedStateDescriptor("DifferenceAccumulatorState")
STATE_TRAVERSAL_ORDER = TypedStateDescriptor("TraversalOrderState")
STATE_ORDERED_KEYS = TypedStateDescriptor("OrderedKeysState")
STATE_SEARCH_INSERT_VALIDATE = TypedStateDescriptor("SearchInsertValidateState")


# ── 7. Resource Envelope & Validation Constraints ────────────────────────────

@dataclass(frozen=True)
class ResourceEnvelope:
    time_preprocessing: str                   # e.g., "O(N log N)"
    time_per_query: str                       # e.g., "O(log N)"
    space_preprocessing: str                  # e.g., "O(N log N)"
    space_per_query: str                      # e.g., "O(1)"
    recursion_depth: str                      # e.g., "O(N)" (chain) or "O(log N)"
    requires_stack_expansion: bool = False

    def is_feasible(self, n: Optional[int], q: Optional[int], time_limit_ms: int = 1000) -> bool:
        if n is None:
            return True
        effective_q = q or 1
        # Asymptotic sanity checks
        if "O(Q * N)" in self.time_preprocessing or "O(N)" in self.time_per_query:
            ops = effective_q * n
            if ops > 2e8:  # exceeds standard 1-second limit
                return False
        return True


@dataclass(frozen=True)
class PreconditionPredicate:
    name: str
    evaluate_fn: Callable[[Any], bool]
    failure_message: str


@dataclass(frozen=True)
class ProofObligation:
    name: str
    statement: str
    discharge_status: ProofStatus = ProofStatus.UNPROVEN


# ── 8. Abstract Capabilities & Capability Providers ──────────────────────────

@dataclass(frozen=True)
class AbstractCapability:
    capability_id: str
    description: str
    semantic_service: str
    required_states: List[TypedStateDescriptor]
    provided_states: List[TypedStateDescriptor]


class CapabilityProvider(ABC):
    """
    An executable algorithmic component realizing an abstract capability.
    Operates strictly via state transformations.
    """
    provider_id: str
    implements_capability: str

    @abstractmethod
    def consumes(self) -> List[TypedStateDescriptor]:
        """Input states required to execute."""
        pass

    @abstractmethod
    def produces(self) -> List[TypedStateDescriptor]:
        """Output states synthesized by this provider."""
        pass

    @abstractmethod
    def preconditions(self) -> List[PreconditionPredicate]:
        """Mathematical preconditions on the ProblemModel/constraints."""
        pass

    @abstractmethod
    def semantic_proof_obligations(self) -> List[ProofObligation]:
        """Formal proof obligations to discharge."""
        pass

    @abstractmethod
    def complexity_bounds(self, n: int, q: int) -> ResourceEnvelope:
        """Asymptotic time/space envelope."""
        pass

    @abstractmethod
    def emit_cpp_fragment(self, bindings: Dict[str, Any], payload: AlgebraicStructure) -> Dict[str, str]:
        """Emits modular C++17 functions, declarations, and calls."""
        pass


# ── 9. VerifiedPlanIR Specification ──────────────────────────────────────────

class InputRepresentationKind(str, Enum):
    EDGE_LIST = "EDGE_LIST"
    PARENT_ARRAY = "PARENT_ARRAY"
    ADJACENCY_LIST = "ADJACENCY_LIST"
    BINARY_POINTERS = "BINARY_POINTERS"


@dataclass
class BoundPipelineStep:
    step_id: str
    provider_id: str
    input_state_bindings: Dict[str, str]  # Input state port -> output port of prior step
    output_state_id: str
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BoundQueryHandler:
    query_id: str
    handler_provider_id: str
    input_state_bindings: Dict[str, str]
    emit_action: str


@dataclass
class DischargedProofCertificate:
    obligation_name: str
    status: ProofStatus
    witness: str


@dataclass
class VerifiedPlanIR:
    """
    The closed-world intermediate representation passed to the C++ emitter.
    Contains strictly resolved components and dataflow bindings.
    Zero unparsed natural language tokens or problem classifications.
    """
    plan_id: str
    target_language: str = "cpp17"
    payload_spec: AlgebraicStructure = field(default_factory=AlgebraicStructure)
    input_representation: InputRepresentationKind = InputRepresentationKind.EDGE_LIST
    root_policy: RootSpec = field(default_factory=RootSpec)
    vertices_bound: Optional[int] = None
    queries_bound: Optional[int] = None
    recursion_guard: bool = False
    pipeline_steps: List[BoundPipelineStep] = field(default_factory=list)
    query_handlers: List[BoundQueryHandler] = field(default_factory=list)
    proof_certificates: List[DischargedProofCertificate] = field(default_factory=list)
    has_vertex_weights: bool = False
