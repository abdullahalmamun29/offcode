"""
CHUP Phase 4: Declarative Composition Recipe Registry.

The 12 canonical patterns serve as declarative conformance fixtures for the
generic synthesis engine rather than hardcoded dispatch paths.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from pointer_algorithms.cross_family.semantic_ontology import CrossFamilyObjective


@dataclass
class CompositionRecipe:
    """
    Declarative specification of a target multi-component synthesis goal.
    """
    objective: CrossFamilyObjective
    name: str
    target_state_name: str
    initial_state_names: List[str]
    allowed_component_names: List[str]
    derivation_rules: List[str]
    proof_obligations: List[str]
    complexity_bound: str
    description: str


class CompositionRecipeRegistry:
    """
    Registry of canonical cross-family composition recipes.
    """
    def __init__(self):
        self.recipes: Dict[CrossFamilyObjective, CompositionRecipe] = {}
        self._register_default_recipes()

    def register(self, recipe: CompositionRecipe) -> None:
        self.recipes[recipe.objective] = recipe

    def get(self, objective: CrossFamilyObjective) -> Optional[CompositionRecipe]:
        return self.recipes.get(objective)

    def get_by_name(self, name: str) -> Optional[CompositionRecipe]:
        for r in self.recipes.values():
            if r.name == name:
                return r
        return None

    def list_recipes(self) -> List[str]:
        return [r.name for r in self.recipes.values()]

    def all(self) -> List[CompositionRecipe]:
        return list(self.recipes.values())

    @classmethod
    def get_instance(cls) -> "CompositionRecipeRegistry":
        global _GLOBAL_RECIPE_REGISTRY
        if _GLOBAL_RECIPE_REGISTRY is None:
            _GLOBAL_RECIPE_REGISTRY = cls()
        return _GLOBAL_RECIPE_REGISTRY

    def _register_default_recipes(self) -> None:
        # 1. Kruskal Minimum Spanning Forest (Graph + Sorting + DSU)
        self.register(CompositionRecipe(
            objective=CrossFamilyObjective.CF_KRUSKAL_MST,
            name="cf_kruskal_mst",
            target_state_name="MinimumSpanningForest",
            initial_state_names=["WeightedGraph"],
            allowed_component_names=["graph_edge_sort_provider", "dsu_cycle_prevention_provider"],
            derivation_rules=["GREEDY_CUT_PROPERTY", "CYCLE_EQUIVALENCE_PARTITION"],
            proof_obligations=["WEIGHT_COMPARABILITY", "GREEDY_CHOICE_PROPERTY", "ACYCLIC_STRUCTURE"],
            complexity_bound="O(E log E)",
            description="Minimum Spanning Forest on arbitrary comparable edge weights via sorting and DSU acyclic union."
        ))

        # 2. Dijkstra Shortest Path (Graph + Min-Heap Priority Queue)
        self.register(CompositionRecipe(
            objective=CrossFamilyObjective.CF_DIJKSTRA_SHORTEST_PATH,
            name="cf_dijkstra_shortest_path",
            target_state_name="ShortestPathDistances",
            initial_state_names=["NonNegativeWeightedGraph"],
            allowed_component_names=["min_heap_priority_frontier_provider"],
            derivation_rules=["GREEDY_FRONTIER_OPTIMALITY"],
            proof_obligations=["NON_NEGATIVE_WEIGHTS"],
            complexity_bound="O(E log V)",
            description="Single-source shortest path via priority queue frontier expansion."
        ))

        # 3. Bottleneck Path via Binary Search (Graph + Bisection + Reachability)
        self.register(CompositionRecipe(
            objective=CrossFamilyObjective.CF_BOTTLENECK_PATH_BINARY_SEARCH,
            name="cf_bottleneck_path_binary_search",
            target_state_name="OptimalBoundaryValue",
            initial_state_names=["SearchDomainInterval", "WeightedGraph"],
            allowed_component_names=["binary_search_bisection_provider", "graph_reachability_checker_provider"],
            derivation_rules=["MONOTONE_THRESHOLD_FILTER"],
            proof_obligations=["MONOTONE_PREDICATE"],
            complexity_bound="O((V + E) log(MaxWeight))",
            description="Max-min bottleneck path via binary search answer bisection and BFS reachability."
        ))

        # 4. Graph Segment Tree Relaxation (Graph + Segment Tree Auxiliary Nodes)
        self.register(CompositionRecipe(
            objective=CrossFamilyObjective.CF_GRAPH_SEGMENT_TREE_RELAXATION,
            name="cf_graph_segment_tree_relaxation",
            target_state_name="ShortestPathDistances",
            initial_state_names=["IntervalRangeGraph"],
            allowed_component_names=["segment_tree_auxiliary_graph_provider", "min_heap_priority_frontier_provider"],
            derivation_rules=["SEGMENT_TREE_INTERVAL_GRAPH_REDUCTION"],
            proof_obligations=["NON_NEGATIVE_WEIGHTS"],
            complexity_bound="O((V + E) log V)",
            description="Shortest path on interval-range edges via auxiliary segment tree graph nodes."
        ))

        # 5. Tree Subtree DP (Tree + Post-Order Recurrence)
        self.register(CompositionRecipe(
            objective=CrossFamilyObjective.CF_TREE_SUBTREE_DP,
            name="cf_tree_subtree_dp",
            target_state_name="SubtreeDPTable",
            initial_state_names=["RootedTree"],
            allowed_component_names=["tree_subtree_dp_provider"],
            derivation_rules=["TOPOLOGICAL_POSTORDER_RECURRENCE"],
            proof_obligations=["CONNECTIVITY_ASSUMPTION", "ACYCLIC_STRUCTURE"],
            complexity_bound="O(N)",
            description="Subtree aggregation and dynamic programming over tree hierarchy."
        ))

        # 6. Tree Path HLD + Segment Tree (Tree + HLD + Range Provider)
        self.register(CompositionRecipe(
            objective=CrossFamilyObjective.CF_TREE_PATH_HLD_SEGMENT_TREE,
            name="cf_tree_path_hld_segment_tree",
            target_state_name="TreePathRangeOperation",
            initial_state_names=["RootedTree"],
            allowed_component_names=["hld_tree_path_provider", "segment_tree_range_acceleration_provider"],
            derivation_rules=["HEAVY_PATH_DECOMPOSITION_MAPPING"],
            proof_obligations=["CONNECTIVITY_ASSUMPTION", "ACYCLIC_STRUCTURE", "ASSOCIATIVE_OPERATION"],
            complexity_bound="O(log^2 N)",
            description="Path queries and path updates on trees via Heavy-Light Decomposition and Range Provider."
        ))

        # 7. Event Scheduling Greedy + Heap (Greedy Choice + Priority Queue)
        self.register(CompositionRecipe(
            objective=CrossFamilyObjective.CF_EVENT_SCHEDULING_GREEDY_HEAP,
            name="cf_event_scheduling_greedy_heap",
            target_state_name="OptimalIntervalPartition",
            initial_state_names=["IntervalSequence"],
            allowed_component_names=["greedy_interval_scheduling_heap_provider"],
            derivation_rules=["INTERVAL_PARTITIONING_EXCHANGE_ARGUMENT"],
            proof_obligations=["GREEDY_CHOICE_PROPERTY"],
            complexity_bound="O(N log N)",
            description="Interval partitioning and room allocation via start-time sorting and min-heap tracking."
        ))

        # 8. Incremental Connectivity Greedy + DSU
        self.register(CompositionRecipe(
            objective=CrossFamilyObjective.CF_INCREMENTAL_CONNECTIVITY_GREEDY_DSU,
            name="cf_incremental_connectivity_greedy_dsu",
            target_state_name="MinimumSpanningForest",
            initial_state_names=["WeightedGraph"],
            allowed_component_names=["graph_edge_sort_provider", "dsu_cycle_prevention_provider"],
            derivation_rules=["GREEDY_EDGE_WEIGHT_CLUSTERING"],
            proof_obligations=["ACYCLIC_STRUCTURE"],
            complexity_bound="O(E log E)",
            description="Incremental clustering and maximum weight forest via greedy edge ordering and DSU."
        ))

        # 9. DP Range Acceleration via Segment Tree
        self.register(CompositionRecipe(
            objective=CrossFamilyObjective.CF_DP_RANGE_ACCELERATION_SEGMENT_TREE,
            name="cf_dp_range_acceleration_segment_tree",
            target_state_name="RangeAggregatedSequence",
            initial_state_names=["LinearIntervalSequence"],
            allowed_component_names=["segment_tree_range_acceleration_provider"],
            derivation_rules=["DP_TRANSITION_RANGE_QUERY_REPRESENTATION"],
            proof_obligations=["ASSOCIATIVE_OPERATION"],
            complexity_bound="O(N log N)",
            description="Acceleration of 1D DP transition search from O(N^2) to O(N log N) via Segment Tree."
        ))

        # 10. Convex DP Optimization via Monotonic Deque
        self.register(CompositionRecipe(
            objective=CrossFamilyObjective.CF_CONVEX_DP_MONOTONIC_QUEUE,
            name="cf_convex_dp_monotonic_queue",
            target_state_name="OptimizedDPTable",
            initial_state_names=["ConvexRecurrenceDPTable"],
            allowed_component_names=["monotonic_deque_convex_optimizer"],
            derivation_rules=["SLOPE_MONOTONICITY_DOMINANCE", "DEQUE_MONOTONIC_VALUE_INVARIANT", "DOMINANCE_LEMMA", "MONOTONE_WINDOW_BOUNDS"],
            proof_obligations=["SLIDING_WINDOW_MONOTONICITY", "DOMINANCE_ORDER", "WINDOW_EXPIRATION"],
            complexity_bound="O(N)",
            description="Acceleration of 1D DP sliding-window transition from O(N*K) to O(N) via monotonic deque."
        ))

        # 11. Bisection + Greedy Feasibility
        self.register(CompositionRecipe(
            objective=CrossFamilyObjective.CF_BISECTION_GREEDY_FEASIBILITY,
            name="cf_bisection_greedy_feasibility",
            target_state_name="OptimalBoundaryValue",
            initial_state_names=["SearchDomainInterval"],
            allowed_component_names=["binary_search_bisection_provider"],
            derivation_rules=["GREEDY_CHOICE_MONOTONICITY"],
            proof_obligations=["MONOTONE_PREDICATE"],
            complexity_bound="O(N log(Domain))",
            description="Answer-space binary search with greedy feasibility checker."
        ))

        # 12. Fractional Bisection + DP Knapsack
        self.register(CompositionRecipe(
            objective=CrossFamilyObjective.CF_FRACTIONAL_BISECTION_DP,
            name="cf_fractional_bisection_dp",
            target_state_name="OptimalBoundaryValue",
            initial_state_names=["SearchDomainInterval"],
            allowed_component_names=["binary_search_bisection_provider"],
            derivation_rules=["PARAMETRIC_FRACTIONAL_DUAL_TRANSFORM"],
            proof_obligations=[
                "FRACTIONAL_OBJECTIVE_FORM",
                "DENOMINATOR_POSITIVITY",
                "PARAMETRIC_RATIO_TRANSFORMATION_VALID",
                "MONOTONE_PREDICATE",
                "NUMERICAL_PRECISION_BOUND",
            ],
            complexity_bound="O(N * W * log(Precision))",
            description="0-1 fractional programming via parametric bisection lambda and knapsack DP."
        ))


_GLOBAL_RECIPE_REGISTRY: Optional[CompositionRecipeRegistry] = None
