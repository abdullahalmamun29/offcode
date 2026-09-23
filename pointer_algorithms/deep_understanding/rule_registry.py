"""
CHUP Phase 6 — Derivation Rule Registry.

Defines the formal contracts and axiomatic basis for every inference rule
in Phase 6. Invariant rules require explicit preconditions, produce proven facts,
and document mathematical/graph-theoretic proof theorems.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Callable, Any
from pointer_algorithms.deep_understanding.fact_model import (
    SemanticFact,
    FactSet,
    FactTier,
    ProofStatus,
    AmbiguityStatus
)


@dataclass(frozen=True)
class DerivationRule:
    """
    Formal specification of an axiomatic inference rule.
    """
    rule_id: str
    name: str
    description: str
    required_fact_names: Tuple[str, ...]
    produced_fact_name: str
    proof_basis: str
    evaluator: Callable[[FactSet], Optional[Tuple[Any, str]]]

    def is_applicable(self, facts: FactSet) -> bool:
        return all(facts.has_proven(req) for req in self.required_fact_names)

    def evaluate(self, facts: FactSet) -> Optional[Tuple[Any, str]]:
        if not self.is_applicable(facts):
            return None
        return self.evaluator(facts)


class DerivationRuleRegistry:
    """
    Authoritative registry of all formal derivation rules.
    """

    def __init__(self):
        self._rules: Dict[str, DerivationRule] = {}
        self._register_canonical_rules()

    def register(self, rule: DerivationRule) -> None:
        self._rules[rule.rule_id] = rule

    def get(self, rule_id: str) -> Optional[DerivationRule]:
        return self._rules.get(rule_id)

    def all_rules(self) -> Tuple[DerivationRule, ...]:
        return tuple(self._rules.values())

    def find_applicable_rules(self, facts: FactSet) -> List[DerivationRule]:
        return [rule for rule in self._rules.values() if rule.is_applicable(facts)]

    def _register_canonical_rules(self) -> None:
        # 1. Tree Equivalence: E = V - 1 conjoined with Connected, Undirected, Simple
        def eval_tree(facts: FactSet) -> Optional[Tuple[Any, str]]:
            v_fact = facts.get("VERTEX_COUNT")
            e_fact = facts.get("EDGE_COUNT")
            if not v_fact or not e_fact:
                return None
            v = v_fact.value
            e = e_fact.value
            if isinstance(v, int) and isinstance(e, int) and v >= 1 and e == v - 1:
                return (
                    "TREE",
                    f"Graph has V={v} vertices, E={e} edges (E=V-1) and is connected, undirected, and simple."
                )
            return None

        self.register(DerivationRule(
            rule_id="RULE_TREE_EQUIVALENCE_E_EQ_V_MINUS_ONE",
            name="Tree Equivalence (E = V - 1)",
            description="Proves TREE topology when E = V - 1, connected, undirected, and simple.",
            required_fact_names=("IS_CONNECTED", "IS_UNDIRECTED", "IS_SIMPLE", "VERTEX_COUNT", "EDGE_COUNT"),
            produced_fact_name="TOPOLOGY_TREE",
            proof_basis="Cayley's Tree Characterization Theorem: A connected simple undirected graph with V vertices and V-1 edges is an acyclic tree.",
            evaluator=eval_tree
        ))

        # 1b. Tree from Connectedness + Acyclicity
        def eval_tree_conn_acyclic(facts: FactSet) -> Optional[Tuple[Any, str]]:
            return (
                "TREE",
                "Graph is connected, acyclic, undirected, and simple, which uniquely characterizes a tree."
            )

        self.register(DerivationRule(
            rule_id="RULE_TREE_EQUIVALENCE_CONNECTED_ACYCLIC",
            name="Tree from Connected and Acyclic",
            description="Proves TREE topology when a simple undirected graph is connected and acyclic.",
            required_fact_names=("IS_CONNECTED", "IS_ACYCLIC", "IS_UNDIRECTED", "IS_SIMPLE"),
            produced_fact_name="TOPOLOGY_TREE",
            proof_basis="Graph Theory Theorem: A connected, acyclic, simple undirected graph is a tree.",
            evaluator=eval_tree_conn_acyclic
        ))

        # 2. DAG from Coordinate Progression
        def eval_dag_coords(facts: FactSet) -> Optional[Tuple[Any, str]]:
            return (
                "DAG",
                "Transitions strictly advance non-decreasing grid coordinates, forbidding backward cycles."
            )

        self.register(DerivationRule(
            rule_id="RULE_DAG_COORDINATE_PROGRESSION",
            name="DAG State Progression via Monotonic Coordinates",
            description="Proves state space is a Directed Acyclic Graph from monotonic coordinate progression.",
            required_fact_names=("TRANSITIONS_NON_DECREASING_COORDINATES",),
            produced_fact_name="STATE_TOPOLOGY_DAG",
            proof_basis="Strict coordinate progression forms a strict partial order on states, proving acyclicity.",
            evaluator=eval_dag_coords
        ))

        # 3. DAG from Index-Ordered Edges (u < v)
        def eval_dag_index(facts: FactSet) -> Optional[Tuple[Any, str]]:
            return (
                "DAG",
                "All directed edges (u, v) satisfy u < v, guaranteeing strict topological ordering."
            )

        self.register(DerivationRule(
            rule_id="RULE_DAG_INDEX_ORDER_EDGES",
            name="DAG from Index-Ordered Edges",
            description="Proves DAG from strictly increasing vertex indices on edges.",
            required_fact_names=("EDGES_RESPECT_INDEX_ORDER",),
            produced_fact_name="STATE_TOPOLOGY_DAG",
            proof_basis="Strict order relation on integer indices is well-founded and cycle-free.",
            evaluator=eval_dag_index
        ))

        # 4. Bipartite Graph from 2-Colorability / No Odd Cycles
        def eval_bipartite(facts: FactSet) -> Optional[Tuple[Any, str]]:
            return (
                "BIPARTITE",
                "Graph is explicitly 2-colorable with no odd-length cycles."
            )

        self.register(DerivationRule(
            rule_id="RULE_BIPARTITE_2_COLORABLE",
            name="Bipartite from 2-Colorability",
            description="Proves bipartite topology from absence of odd cycles.",
            required_fact_names=("NO_ODD_CYCLES",),
            produced_fact_name="GRAPH_BIPARTITE",
            proof_basis="Kőnig's Theorem: A graph is bipartite if and only if it contains no odd-length cycles.",
            evaluator=eval_bipartite
        ))

        # 5. Non-Negative Edge Weight Monotonicity
        def eval_nonneg_weights(facts: FactSet) -> Optional[Tuple[Any, str]]:
            return (
                True,
                "All edge weights / transition costs are strictly non-negative."
            )

        self.register(DerivationRule(
            rule_id="RULE_NON_NEGATIVE_DISTANCE_MONOTONICITY",
            name="Distance Monotonicity from Non-Negative Weights",
            description="Proves shortest-path distance monotonicity under non-negative edge weights.",
            required_fact_names=("ALL_EDGE_WEIGHTS_NON_NEGATIVE",),
            produced_fact_name="DISTANCE_MONOTONIC_PROGRESSION",
            proof_basis="Non-negative edge weights guarantee path lengths are non-decreasing along shortest path trees.",
            evaluator=eval_nonneg_weights
        ))

        # 5b. Non-Negative Edge Weight Dijkstra Compatibility (Compatibility only, not selection)
        def eval_dijkstra_compatible(facts: FactSet) -> Optional[Tuple[Any, str]]:
            return (
                True,
                "Non-negative weights satisfy the optimal substructure and greedy choice preconditions for Dijkstra's algorithm (compatibility only, not necessity)."
            )

        self.register(DerivationRule(
            rule_id="RULE_NON_NEGATIVE_WEIGHTS_DIJKSTRA_COMPATIBILITY",
            name="Dijkstra Compatibility from Non-Negative Weights",
            description="Proves Dijkstra algorithm compatibility (not necessity) when edge weights are non-negative.",
            required_fact_names=("ALL_EDGE_WEIGHTS_NON_NEGATIVE",),
            produced_fact_name="DIJKSTRA_COMPATIBLE",
            proof_basis="Non-negative edge weights ensure optimal substructure without negative cycles, guaranteeing Dijkstra compatibility. This is compatibility only, not selection or requirement.",
            evaluator=eval_dijkstra_compatible
        ))

        # 6. Massive Coordinate Dense Incompatibility
        def eval_dense_infeasible(facts: FactSet) -> Optional[Tuple[Any, str]]:
            return (
                True,
                "Coordinate domain exceeds dense addressable memory, requiring sparse or compressed indexing."
            )

        self.register(DerivationRule(
            rule_id="RULE_MASSIVE_COORDINATE_DENSE_INCOMPATIBILITY",
            name="Dense Infeasibility on Massive Coordinates",
            description="Deduces dense array indexing is unavailable when coordinates exceed memory budget.",
            required_fact_names=("COORDINATES_EXCEED_DENSE_MEMORY_BOUND", "COORDINATE_QUERY_OR_INDEX_REQUIRED"),
            produced_fact_name="DENSE_INDEX_SPACE_UNAVAILABLE",
            proof_basis="Physical memory limit exceeded by dense materialization of max coordinate range.",
            evaluator=eval_dense_infeasible
        ))

        # 7. Algebraic Invertibility Prefix Derivability
        def eval_invertible_prefix(facts: FactSet) -> Optional[Tuple[Any, str]]:
            return (
                True,
                "Invertible operation allows range aggregate derivation via prefix difference."
            )

        self.register(DerivationRule(
            rule_id="RULE_ALGEBRAIC_INVERTIBILITY_PREFIX_REDUCTION",
            name="Range from Prefix via Group Invertibility",
            description="Deduces range derivation from prefix difference under group invertibility.",
            required_fact_names=("OPERATION_INVERTIBLE", "RANGE_QUERY_REQUIRED"),
            produced_fact_name="RANGE_DERIVABLE_FROM_PREFIXES",
            proof_basis="Group theory: for any associative group (G, +), sum(L..R) = prefix(R) - prefix(L-1).",
            evaluator=eval_invertible_prefix
        ))

        # 8. Algebraic Idempotence Overlap Reduction
        def eval_idempotent_overlap(facts: FactSet) -> Optional[Tuple[Any, str]]:
            return (
                True,
                "Idempotent operation allows range queries via power-of-two overlapping intervals."
            )

        self.register(DerivationRule(
            rule_id="RULE_ALGEBRAIC_IDEMPOTENCE_OVERLAP_REDUCTION",
            name="Overlapping Interval Query Support via Idempotence",
            description="Deduces power-of-two interval overlap suitability under idempotence and static data.",
            required_fact_names=("OPERATION_IDEMPOTENT", "OPERATION_ASSOCIATIVE", "STATIC_DATA_WITHOUT_UPDATES"),
            produced_fact_name="OVERLAPPING_INTERVAL_QUERY_SUPPORTED",
            proof_basis="Semilattice idempotence: x * x = x ensures union of overlapping intervals computes exact range aggregate.",
            evaluator=eval_idempotent_overlap
        ))

        # 9. Predicate Monotonicity Bisection Feasibility
        def eval_bisection(facts: FactSet) -> Optional[Tuple[Any, str]]:
            return (
                True,
                "Monotone feasibility predicate guarantees logarithmic boundary convergence."
            )

        self.register(DerivationRule(
            rule_id="RULE_PREDICATE_MONOTONICITY_BISECTION",
            name="Answer Bisection via Predicate Monotonicity",
            description="Deduces binary search on answer feasibility from predicate monotonicity.",
            required_fact_names=("PREDICATE_MONOTONE",),
            produced_fact_name="ANSWER_BISECTION_SUPPORTED",
            proof_basis="Discrete Intermediate Value Theorem for monotone boolean predicates guarantees a unique boundary.",
            evaluator=eval_bisection
        ))

        # 10. Sliding Window Boundary Monotonicity
        def eval_sliding_window(facts: FactSet) -> Optional[Tuple[Any, str]]:
            return (
                True,
                "Right expansion monotonicity ensures left pointer never retreats."
            )

        self.register(DerivationRule(
            rule_id="RULE_SLIDING_WINDOW_MONOTONIC_PROGRESSION",
            name="Sliding Window Progression",
            description="Deduces two-pointer sliding window validity from boundary monotonicity.",
            required_fact_names=("WINDOW_VALIDITY_MONOTONE_IN_RIGHT_EXPANSION", "ELEMENTS_NON_NEGATIVE"),
            produced_fact_name="SLIDING_WINDOW_TWO_POINTER_SUPPORTED",
            proof_basis="Two-pointer monotonicity: when predicate is monotone under non-negative elements, advancing left pointer never causes right pointer to retreat.",
            evaluator=eval_sliding_window
        ))
