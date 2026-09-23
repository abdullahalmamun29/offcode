"""
Canonical Semantic Problem Model for CHUP Recognition Architecture V2.

Decouples semantic problem requirements from algorithm capabilities and implementations:
WHAT the problem requires (ProblemModel)
    ↓
WHAT algorithms provide (AlgorithmCapability)
    ↓
HOW the plan is implemented (Existing Generator)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Set, Tuple


# ── 1. Evidence ───────────────────────────────────────────────────────────────

class EvidenceStatus(str, Enum):
    EXPLICIT = "EXPLICIT"
    INFERRED = "INFERRED"


class SemanticScope(str, Enum):
    TASK_REQUIREMENT = "TASK_REQUIREMENT"
    INPUT_SCHEMA = "INPUT_SCHEMA"
    OUTPUT_SPEC = "OUTPUT_SPEC"
    CONSTRAINT = "CONSTRAINT"


class ConstraintDomain(str, Enum):
    PROBLEM_DATA = "PROBLEM_DATA"
    INPUT_SIZE = "INPUT_SIZE"
    OUTPUT = "OUTPUT"
    STRUCTURAL = "STRUCTURAL"


@dataclass
class InputSizeAggregateConstraint:
    domain: ConstraintDomain = ConstraintDomain.INPUT_SIZE
    aggregate: str = "SUM"
    variable: str = "n"
    scope: str = "ALL_TEST_CASES"
    bound: Optional[int] = None
    raw: Optional[str] = None


@dataclass
class Evidence:
    """
    Extracted textual evidence with provenance.
    Never contains an algorithm selection or template name.
    """
    fact: str
    source: str
    confidence: float
    status: EvidenceStatus
    location: Optional[str] = None
    scope: str = "TASK_REQUIREMENT"

    def __repr__(self) -> str:
        return f"Evidence({self.fact!r}, source={self.source!r}, status={self.status.value}, conf={self.confidence:.2f})"


# ── 2. Facts ──────────────────────────────────────────────────────────────────

class FactStatus(str, Enum):
    KNOWN = "KNOWN"
    INFERRED = "INFERRED"
    AMBIGUOUS = "AMBIGUOUS"
    UNKNOWN = "UNKNOWN"
    CONTRADICTED = "CONTRADICTED"


@dataclass
class Fact:
    """
    A semantic fact about the problem, independent of algorithms.
    Tracks derivation rule, source, and dependencies for auditability.
    """
    name: str
    value: Any
    status: FactStatus
    source: str
    derivation_rule: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    confidence: float = 1.0
    scope: str = "TASK_REQUIREMENT"

    def __repr__(self) -> str:
        return f"Fact({self.name}={self.value!r}, status={self.status.value}, rule={self.derivation_rule})"


# ── 3. Hypotheses ─────────────────────────────────────────────────────────────

class HypothesisStatus(str, Enum):
    PROPOSED = "PROPOSED"
    CONFIRMED = "CONFIRMED"
    AMBIGUOUS = "AMBIGUOUS"
    REJECTED = "REJECTED"


@dataclass
class Hypothesis:
    """
    Hypothesis used when interpretation is not yet established.
    Never silently collapses ambiguity.
    """
    name: str
    value: Any
    status: HypothesisStatus
    evidence: List[Evidence] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Hypothesis({self.name}={self.value!r}, status={self.status.value})"


# ── 4. Selection Model ────────────────────────────────────────────────────────

class SelectionKind(str, Enum):
    FIXED_CARDINALITY = "FIXED_CARDINALITY"
    CONTIGUOUS_SEGMENT = "CONTIGUOUS_SEGMENT"
    ARBITRARY_SUBSET = "ARBITRARY_SUBSET"
    ALL_ELEMENTS = "ALL_ELEMENTS"
    UNKNOWN = "UNKNOWN"


@dataclass
class SelectionModel:
    kind: SelectionKind
    cardinality: Optional[int] = None
    distinct_positions: bool = False

    def __repr__(self) -> str:
        if self.kind == SelectionKind.FIXED_CARDINALITY:
            dist = ", distinct" if self.distinct_positions else ""
            return f"SelectionModel(FIXED_CARDINALITY({self.cardinality}{dist}))"
        return f"SelectionModel({self.kind.value})"


# ── 5. Objective Model ────────────────────────────────────────────────────────

class ObjectiveKind(str, Enum):
    MINIMIZE = "MINIMIZE"
    MAXIMIZE = "MAXIMIZE"
    MAXIMIZE_CARDINALITY = "MAXIMIZE_CARDINALITY"
    MAXIMIZE_SUM = "MAXIMIZE_SUM"
    MAXIMIZE_VALUE = "MAXIMIZE_VALUE"
    FIND_ANY = "FIND_ANY"
    COUNT = "COUNT"
    CONSTRUCT = "CONSTRUCT"
    DECIDE = "DECIDE"
    OPTIMIZE = "OPTIMIZE"
    UNKNOWN = "UNKNOWN"


@dataclass
class ObjectiveModel:
    kind: ObjectiveKind
    target_property: Optional[str] = None  # e.g., "cost", "length", "pairs", "towers"

    def __repr__(self) -> str:
        return f"ObjectiveModel({self.kind.value}, target={self.target_property})"


# ── 6. Constraint Model ───────────────────────────────────────────────────────

@dataclass
class ConstraintModel:
    n: Optional[int] = None
    m: Optional[int] = None
    k: Optional[int] = None
    target_value: Optional[int] = None
    value_bounds: Optional[Tuple[Optional[int], Optional[int]]] = None
    time_limit_ms: int = 1000
    memory_limit_mb: int = 256
    query_count: Optional[int] = None
    update_count: Optional[int] = None
    recursion_depth: Optional[int] = None
    is_cardinality_fixed: bool = False
    group_capacity: Optional[int] = None
    max_group_cardinality: Optional[int] = None
    match_tolerance: Optional[int] = None
    strictly_positive: bool = False
    input_size_aggregates: List[InputSizeAggregateConstraint] = field(default_factory=list)

    def is_memory_exceeded(self, required_mb: float) -> bool:
        return required_mb > self.memory_limit_mb


# ── 7. Required Operations ────────────────────────────────────────────────────

class RequiredOperation(str, Enum):
    SEARCH = "SEARCH"
    PAIR_SEARCH = "PAIR_SEARCH"
    PAIR_SUM_SEARCH = "PAIR_SUM_SEARCH"
    PREDECESSOR = "PREDECESSOR"
    SUCCESSOR = "SUCCESSOR"
    QUERY = "QUERY"
    UPDATE = "UPDATE"
    POINT_UPDATE = "POINT_UPDATE"
    RANGE_UPDATE = "RANGE_UPDATE"
    INSERT = "INSERT"
    DELETE = "DELETE"
    MERGE = "MERGE"
    TRAVERSAL = "TRAVERSAL"
    CONNECTIVITY = "CONNECTIVITY"
    PARTITION = "PARTITION"
    SORT = "SORT"
    SELECT = "SELECT"
    COUNT = "COUNT"
    CONSTRUCT = "CONSTRUCT"
    AGGREGATE = "AGGREGATE"
    RANGE_AGGREGATE = "RANGE_AGGREGATE"
    PREFIX_AGGREGATE = "PREFIX_AGGREGATE"
    MINIMUM_QUERY = "MINIMUM_QUERY"
    MAXIMUM_QUERY = "MAXIMUM_QUERY"
    STATIC_BOUNDED_SELECTION = "STATIC_BOUNDED_SELECTION"
    ADDITIVE_TARGET_SEARCH = "ADDITIVE_TARGET_SEARCH"
    CAPACITY_PAIRING = "CAPACITY_PAIRING"
    TWO_SEQUENCE_INTERVAL_MATCHING = "TWO_SEQUENCE_INTERVAL_MATCHING"
    MAX_VALID_WINDOW = "MAX_VALID_WINDOW"
    BOUNDED_DIAMETER_SUBSET = "BOUNDED_DIAMETER_SUBSET"


# ── 8. Relations and Operators ────────────────────────────────────────────────

class RelationKind(str, Enum):
    EQUALITY = "EQUALITY"
    INEQUALITY = "INEQUALITY"
    SUM = "SUM"
    DIFFERENCE = "DIFFERENCE"
    ORDERING = "ORDERING"
    ADJACENCY = "ADJACENCY"
    MEMBERSHIP = "MEMBERSHIP"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    INTERVAL_TOLERANCE = "INTERVAL_TOLERANCE"
    PAIRWISE_ABSOLUTE_DIFFERENCE = "PAIRWISE_ABSOLUTE_DIFFERENCE"


class OperatorKind(str, Enum):
    NONE = "NONE"
    SUM = "SUM"
    XOR = "XOR"
    AND = "AND"
    OR = "OR"
    MODULO = "MODULO"


@dataclass
class RelationModel:
    kind: RelationKind
    operator: OperatorKind = OperatorKind.NONE
    domain: ConstraintDomain = ConstraintDomain.PROBLEM_DATA
    quantifier: Optional[str] = None  # e.g., "FOR_ALL_PAIRS"
    left: Optional[str] = None
    right: Optional[str] = None
    target: Optional[str] = None
    tolerance: Optional[str] = None


# ── 9. Structural Properties ──────────────────────────────────────────────────

class StructuralProperty(str, Enum):
    FIXED_CARDINALITY = "FIXED_CARDINALITY"
    CONTIGUOUS_SELECTION = "CONTIGUOUS_SELECTION"
    ARBITRARY_SUBSET = "ARBITRARY_SUBSET"
    ALL_ELEMENTS_REQUIRED = "ALL_ELEMENTS_REQUIRED"
    ORDERED_STATE = "ORDERED_STATE"
    DYNAMIC_STATE = "DYNAMIC_STATE"
    STATIC_STATE = "STATIC_STATE"
    MONOTONICITY = "MONOTONICITY"
    LOCAL_CHOICE = "LOCAL_CHOICE"
    GLOBAL_OPTIMUM = "GLOBAL_OPTIMUM"
    OPTIMAL_SUBSTRUCTURE = "OPTIMAL_SUBSTRUCTURE"
    OVERLAPPING_SUBPROBLEMS = "OVERLAPPING_SUBPROBLEMS"
    INDEPENDENT_SUBPROBLEMS = "INDEPENDENT_SUBPROBLEMS"
    STATE_TRANSITION = "STATE_TRANSITION"
    RECURSIVE_DECOMPOSITION = "RECURSIVE_DECOMPOSITION"
    PARTITIONING = "PARTITIONING"
    BRANCHING = "BRANCHING"
    PRUNING = "PRUNING"
    REVERSIBLE_DECISIONS = "REVERSIBLE_DECISIONS"
    IRREVERSIBLE_DECISIONS = "IRREVERSIBLE_DECISIONS"
    SEARCH_SPACE = "SEARCH_SPACE"
    EXPONENTIAL_SEARCH_SPACE = "EXPONENTIAL_SEARCH_SPACE"
    PREFIX_RELATION = "PREFIX_RELATION"
    SUFFIX_RELATION = "SUFFIX_RELATION"
    RANGE_RELATION = "RANGE_RELATION"
    PAIRWISE_RELATION = "PAIRWISE_RELATION"
    CONNECTIVITY = "CONNECTIVITY"
    TREE_STRUCTURE = "TREE_STRUCTURE"
    GRAPH_STRUCTURE = "GRAPH_STRUCTURE"
    FREQUENCY_STATE = "FREQUENCY_STATE"
    PREDECESSOR_QUERY = "PREDECESSOR_QUERY"
    SUCCESSOR_QUERY = "SUCCESSOR_QUERY"
    MINIMUM_QUERY = "MINIMUM_QUERY"
    MAXIMUM_QUERY = "MAXIMUM_QUERY"
    POINT_UPDATE = "POINT_UPDATE"
    RANGE_UPDATE = "RANGE_UPDATE"
    SUBPROBLEM_INDEPENDENCE = "SUBPROBLEM_INDEPENDENCE"
    MERGE_REQUIREMENT = "MERGE_REQUIREMENT"
    TERMINAL_STATE = "TERMINAL_STATE"
    STATIC_BOUNDED_SELECTION = "STATIC_BOUNDED_SELECTION"
    STREAM_PROCESSING = "STREAM_PROCESSING"
    BITWISE_DECOMPOSITION = "BITWISE_DECOMPOSITION"
    PAIRWISE_DISTINCT_SELECTION = "PAIRWISE_DISTINCT_SELECTION"
    DECOMPOSABLE_ADDITIVE_SEARCH = "DECOMPOSABLE_ADDITIVE_SEARCH"
    CAPACITY_CONSTRAINED_GROUPING = "CAPACITY_CONSTRAINED_GROUPING"
    EXTREMAL_PAIRING = "EXTREMAL_PAIRING"
    TWO_SEQUENCE_MATCHING = "TWO_SEQUENCE_MATCHING"
    ONE_TO_ONE_MATCHING = "ONE_TO_ONE_MATCHING"
    MONOTONE_COMPATIBILITY = "MONOTONE_COMPATIBILITY"
    MAX_CARDINALITY_MATCHING = "MAX_CARDINALITY_MATCHING"
    MONOTONE_RANGE_SUM = "MONOTONE_RANGE_SUM"
    BOUNDED_DIAMETER = "BOUNDED_DIAMETER"
    SORTED_CONTIGUOUS_OPTIMAL_BLOCK = "SORTED_CONTIGUOUS_OPTIMAL_BLOCK"
    MONOTONE_VALID_WINDOW = "MONOTONE_VALID_WINDOW"
    SINGLE_COLLECTION = "SINGLE_COLLECTION"
    SORTABLE = "SORTABLE"


# ── 10. State Model ───────────────────────────────────────────────────────────

@dataclass
class StateModel:
    """
    Generic state representation for DP, Backtracking, DSU, Segment Tree, etc.
    """
    state_variables: Dict[str, str] = field(default_factory=dict)
    transitions: List[str] = field(default_factory=list)
    initial_state: Optional[str] = None
    terminal_conditions: List[str] = field(default_factory=list)
    choice_points: List[str] = field(default_factory=list)
    mutation_operations: List[str] = field(default_factory=list)
    reversible_operations: List[str] = field(default_factory=list)
    state_reversibility: bool = False
    state_domain: Optional[str] = None


# ── 11. Problem Structure Graph ───────────────────────────────────────────────

@dataclass
class GraphNode:
    node_id: str
    kind: str  # entity, constraint, objective, operation, relation, state, structural_property, proof_obligation
    data: Any


@dataclass
class GraphEdge:
    source: str
    target: str
    relation: str  # requires, produces, depends_on, contradicts, supports, derived_from, partitions_into, combines_with


class ProblemStructureGraph:
    """
    Graph of semantic problem entities, operations, constraints, and dependencies.
    """
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []

    def add_node(self, node_id: str, kind: str, data: Any = None) -> None:
        if node_id not in self.nodes:
            self.nodes[node_id] = GraphNode(node_id, kind, data)

    def add_edge(self, source: str, target: str, relation: str) -> None:
        self.edges.append(GraphEdge(source, target, relation))

    def get_dependencies(self, target_id: str) -> List[str]:
        return [e.source for e in self.edges if e.target == target_id and e.relation in ("depends_on", "derived_from", "requires")]


# ── 12. Canonical Problem Model ───────────────────────────────────────────────

@dataclass
class ProblemModel:
    """
    The central architectural contract of CHUP Recognition Architecture V2.
    Completely decoupled from algorithm templates.
    """
    raw_text: str
    entities: List[str] = field(default_factory=list)
    collections: List[str] = field(default_factory=list)
    input_spec: Dict[str, Any] = field(default_factory=dict)
    output_spec: Dict[str, Any] = field(default_factory=dict)  # e.g., {'type': 'ORIGINAL_INDICES', 'base': 1}
    objective: ObjectiveModel = field(default_factory=lambda: ObjectiveModel(ObjectiveKind.UNKNOWN))
    selection: SelectionModel = field(default_factory=lambda: SelectionModel(SelectionKind.UNKNOWN))
    constraints: ConstraintModel = field(default_factory=ConstraintModel)
    operations: Set[RequiredOperation] = field(default_factory=set)
    relations: List[RelationModel] = field(default_factory=list)
    structural_properties: Set[StructuralProperty] = field(default_factory=set)
    state_model: Optional[StateModel] = None
    graph: ProblemStructureGraph = field(default_factory=ProblemStructureGraph)
    evidence: List[Evidence] = field(default_factory=list)
    facts: Dict[str, Fact] = field(default_factory=dict)
    hypotheses: Dict[str, Hypothesis] = field(default_factory=dict)
    uncertainty: Dict[str, str] = field(default_factory=dict)

    def add_fact(self, fact: Fact) -> None:
        self.facts[fact.name] = fact
        self.graph.add_node(fact.name, "fact", fact.value)
        for dep in fact.dependencies:
            self.graph.add_edge(dep, fact.name, "derived_from")

    def get_fact(self, name: str) -> Optional[Fact]:
        return self.facts.get(name)

    def has_fact(self, name: str) -> bool:
        return name in self.facts and self.facts[name].status in (FactStatus.KNOWN, FactStatus.INFERRED)

    def validate(self) -> "ValidationResult":
        errors: List[str] = []
        warnings: List[str] = []

        # 1. Selection Model validation
        if self.selection.kind == SelectionKind.FIXED_CARDINALITY:
            if self.selection.cardinality is None or self.selection.cardinality <= 0:
                errors.append("Selection is FIXED_CARDINALITY but cardinality is not a positive integer")
        elif self.selection.kind == SelectionKind.ARBITRARY_SUBSET:
            if self.selection.cardinality is not None and self.selection.cardinality == 2:
                errors.append("Selection cannot be both ARBITRARY_SUBSET and fixed cardinality 2")

        # 2. Relation consistency validation
        has_sum = any(r.kind == RelationKind.SUM for r in self.relations)
        has_xor = any(r.operator == OperatorKind.XOR for r in self.relations)
        if has_sum and has_xor and len(self.relations) == 1:
            errors.append("Single relation cannot have conflicting operators SUM and XOR")

        # 3. Output consistency validation
        if self.output_spec.get("type") == "ORIGINAL_INDICES":
            if self.selection.kind == SelectionKind.UNKNOWN:
                warnings.append("Output requires ORIGINAL_INDICES but selection kind is UNKNOWN")

        # 4. Constraint contradiction validation
        if self.constraints.n is not None and self.constraints.n < 0:
            errors.append("Constraint N cannot be negative")
        if self.constraints.memory_limit_mb <= 0:
            errors.append("Memory limit must be positive")
        if self.constraints.time_limit_ms <= 0:
            errors.append("Time limit must be positive")

        # 5. Contradicted facts check
        for name, fact in self.facts.items():
            if fact.status == FactStatus.CONTRADICTED:
                errors.append(f"Fact '{name}' is marked CONTRADICTED")

        is_valid = (len(errors) == 0)
        return ValidationResult(is_valid=is_valid, errors=errors, warnings=warnings)


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.is_valid
