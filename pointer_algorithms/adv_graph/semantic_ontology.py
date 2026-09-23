"""
Phase 3N: Semantic Graph Ontology & Derivation Provenance.

Core Principle:
Primitive structural facts are strictly orthogonal and decoupled from algorithm names.
Derived properties are computed via deterministic mathematical deduction.
Every derived property retains complete provenance (source facts, deduction rule, proof obligations).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Set


# ── 1. Primitive Domain Enums ──

class Directedness(str, Enum):
    DIRECTED = "DIRECTED"
    UNDIRECTED = "UNDIRECTED"


class WeightDomain(str, Enum):
    UNWEIGHTED = "UNWEIGHTED"
    BINARY_01 = "BINARY_01"
    NON_NEGATIVE_REAL = "NON_NEGATIVE_REAL"
    GENERAL_REAL_WITH_NEGATIVES = "GENERAL_REAL_WITH_NEGATIVES"


class CapacityDomain(str, Enum):
    UNCONSTRAINED = "UNCONSTRAINED"
    INTEGER_CAPACITY = "INTEGER_CAPACITY"
    REAL_CAPACITY = "REAL_CAPACITY"


class CostDomain(str, Enum):
    ZERO_COST = "ZERO_COST"
    UNIT_COST = "UNIT_COST"
    GENERAL_COST = "GENERAL_COST"


class BipartiteStatus(str, Enum):
    BIPARTITE_CERTIFIED = "BIPARTITE_CERTIFIED"
    BIPARTITE_DERIVED = "BIPARTITE_DERIVED"
    NOT_BIPARTITE = "NOT_BIPARTITE"
    UNKNOWN = "UNKNOWN"


# ── 2. Atomic Objective Enums ──

class PathObjective(str, Enum):
    SHORTEST = "SHORTEST"
    LONGEST = "LONGEST"
    NONE = "NONE"


class PathScope(str, Enum):
    SINGLE_SOURCE = "SINGLE_SOURCE"
    SINGLE_PAIR = "SINGLE_PAIR"
    ALL_PAIRS = "ALL_PAIRS"
    NONE = "NONE"


class TraversalObjective(str, Enum):
    USE_EVERY_EDGE_ONCE = "USE_EVERY_EDGE_ONCE"  # Eulerian
    VISIT_ALL_VERTICES = "VISIT_ALL_VERTICES"
    NONE = "NONE"


class CycleQuery(str, Enum):
    DETECT_EXISTENCE = "DETECT_EXISTENCE"
    RECONSTRUCT_NEGATIVE_CYCLE = "RECONSTRUCT_NEGATIVE_CYCLE"
    NONE = "NONE"


class ConnectivityObjective(str, Enum):
    REACHABILITY = "REACHABILITY"
    STRONGLY_CONNECTED = "STRONGLY_CONNECTED"
    VERTEX_BICONNECTED = "VERTEX_BICONNECTED"
    EDGE_BICONNECTED = "EDGE_BICONNECTED"
    SPANNING_FOREST = "SPANNING_FOREST"
    NONE = "NONE"


class MatchingObjective(str, Enum):
    MAX_CARDINALITY = "MAX_CARDINALITY"
    MIN_WEIGHT_PERFECT = "MIN_WEIGHT_PERFECT"
    NONE = "NONE"


class FlowObjective(str, Enum):
    MAX_VALUE = "MAX_VALUE"
    MIN_CUT = "MIN_CUT"
    MIN_COST_MAX_FLOW = "MIN_COST_MAX_FLOW"
    NONE = "NONE"


class LogicModel(str, Enum):
    TWO_LITERAL_CLAUSES = "TWO_LITERAL_CLAUSES"  # 2-CNF
    NONE = "NONE"


# ── 3. Provenance Dataclass ──

class ProvenanceStatus(str, Enum):
    PROVEN = "PROVEN"
    UNPROVEN = "UNPROVEN"
    CONTRADICTED = "CONTRADICTED"


@dataclass
class DerivedFact:
    """
    Formal record tracking how a structural fact was deduced.
    """
    fact_id: str
    value: Any
    source_facts: List[str] = field(default_factory=list)
    derivation_rule: str = ""
    proof_obligations: List[str] = field(default_factory=list)
    status: ProvenanceStatus = ProvenanceStatus.PROVEN


# ── 4. Matching Relation Model ──

@dataclass
class MatchingRelation:
    """
    Structural specification for bipartite matching problems.
    Separates graph bipartiteness from matching constraints.
    """
    left_partition: str = "U"
    right_partition: str = "V"
    one_to_one: bool = True
    is_maximum_cardinality: bool = True


# ── 5. Semantic Graph Model ──

@dataclass
class SemanticGraphModel:
    """
    Complete semantic representation of a graph problem.
    Contains primitive facts and derived structural properties with full provenance.
    Zero algorithm names allowed in this representation.
    """
    # Primitive facts
    directedness: Directedness = Directedness.UNDIRECTED
    weight_domain: WeightDomain = WeightDomain.UNWEIGHTED
    capacity_domain: CapacityDomain = CapacityDomain.UNCONSTRAINED
    cost_domain: CostDomain = CostDomain.ZERO_COST
    bipartite_status: BipartiteStatus = BipartiteStatus.UNKNOWN
    negative_edges_present: bool = False
    source_vertex: Optional[str] = None
    target_vertex: Optional[str] = None

    # Atomic objectives
    path_objective: PathObjective = PathObjective.NONE
    path_scope: PathScope = PathScope.NONE
    traversal_objective: TraversalObjective = TraversalObjective.NONE
    cycle_query: CycleQuery = CycleQuery.NONE
    connectivity_objective: ConnectivityObjective = ConnectivityObjective.NONE
    matching_objective: MatchingObjective = MatchingObjective.NONE
    flow_objective: FlowObjective = FlowObjective.NONE
    logic_model: LogicModel = LogicModel.NONE

    # Structural matching relation
    matching_relation: Optional[MatchingRelation] = None

    # Problem constraints
    vertex_count_bound: Optional[int] = None
    edge_count_bound: Optional[int] = None
    time_limit_ms: int = 1000

    # Derived properties & provenance
    derived_properties: Dict[str, Any] = field(default_factory=dict)
    provenance_records: List[DerivedFact] = field(default_factory=list)

    def add_derived_property(self, fact_id: str, value: Any, source_facts: List[str], rule: str, obligations: Optional[List[str]] = None) -> None:
        self.derived_properties[fact_id] = value
        self.provenance_records.append(DerivedFact(
            fact_id=fact_id,
            value=value,
            source_facts=source_facts,
            derivation_rule=rule,
            proof_obligations=obligations or [],
            status=ProvenanceStatus.PROVEN
        ))

    def is_dag(self) -> bool:
        """
        DAG is a DERIVED property: directed == True AND cycle_exists == False.
        """
        return bool(self.derived_properties.get("is_dag", False))

    def is_bipartite(self) -> bool:
        """
        Bipartite is True if certified or derived from independent partitions.
        """
        return self.bipartite_status in (BipartiteStatus.BIPARTITE_CERTIFIED, BipartiteStatus.BIPARTITE_DERIVED) or bool(self.derived_properties.get("is_bipartite", False))
