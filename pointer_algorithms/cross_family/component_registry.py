"""
CHUP Phase 4: Universal Component Registry for Cross-Family Synthesis.

Registers decoupled algorithmic components and data structures across
all 19 frozen domains (Graph, Tree, DSU, Heap, Binary Search, Segment Tree,
Fenwick, Monotonic Queue, Greedy, DP, etc.).
"""

from typing import Dict, List, Optional
from pointer_algorithms.cross_family.component_model import (
    AlgorithmComponent,
    CompositionNodeType,
    StateContract,
    StateKind,
    SemanticAttribute,
    AttributeDomainType,
    MutationSemantics,
    NumericDomain,
    IndexingSemantics,
)


class CrossFamilyComponentRegistry:
    """
    Centralized registry of modular cross-family capability providers.
    """
    def __init__(self):
        self.components: Dict[str, AlgorithmComponent] = {}
        self._register_default_components()

    def register(self, component: AlgorithmComponent) -> None:
        self.components[component.name] = component

    def get(self, name: str) -> Optional[AlgorithmComponent]:
        return self.components.get(name)

    def all(self) -> List[AlgorithmComponent]:
        return list(self.components.values())

    def find_providers_for(self, target_state: StateContract) -> List[AlgorithmComponent]:
        """Finds all components that produce a state satisfying target_state."""
        providers = []
        for comp in self.components.values():
            for prod in comp.produces_state:
                if prod.satisfies(target_state):
                    providers.append(comp)
                    break
        return providers

    def _register_default_components(self) -> None:
        # 1. Edge Sorting Provider (Kruskal preparation)
        self.register(AlgorithmComponent(
            name="graph_edge_sort_provider",
            category="transformation",
            node_type=CompositionNodeType.TRANSFORMATION,
            consumes_state=[StateContract(
                state_kind=StateKind.GRAPH,
                name="WeightedGraph",
                attributes={"weights": SemanticAttribute("weights", AttributeDomainType.WEIGHT_KIND, "WEIGHTED")}
            )],
            produces_state=[StateContract(
                state_kind=StateKind.SEQUENCE,
                name="OrderedEdgeSequence",
                attributes={"ordering": SemanticAttribute("ordering", AttributeDomainType.ORDERING, "ASCENDING_WEIGHT")},
                mutation_semantics=MutationSemantics.DERIVING
            )],
            required_operations=["SORT_EDGES_BY_WEIGHT"],
            proof_obligations=["WEIGHT_COMPARABILITY"],
            complexity_time="O(E log E)",
            complexity_space="O(E)",
            implementation_backend="cpp_generator:edge_sort"
        ))

        # 2. DSU Cycle Prevention & Spanning Forest Provider
        self.register(AlgorithmComponent(
            name="dsu_cycle_prevention_provider",
            category="data_structure",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[StateContract(
                state_kind=StateKind.SEQUENCE,
                name="OrderedEdgeSequence"
            )],
            produces_state=[StateContract(
                state_kind=StateKind.GRAPH,
                name="MinimumSpanningForest",
                attributes={"cyclicity": SemanticAttribute("cyclicity", AttributeDomainType.TOPOLOGY, "ACYCLIC")},
                supertypes=["SpanningForest", "GraphState"],
                mutation_semantics=MutationSemantics.DERIVING
            )],
            required_operations=["FIND", "UNION", "CYCLE_PREVENTION"],
            proof_obligations=["ACYCLIC_STRUCTURE"],
            complexity_time="O(E alpha(V))",
            complexity_space="O(V)",
            implementation_backend="cpp_generator:kruskal_dsu"
        ))

        # 3. Min-Heap Priority Frontier Provider (Dijkstra)
        self.register(AlgorithmComponent(
            name="min_heap_priority_frontier_provider",
            category="primitive",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[StateContract(
                state_kind=StateKind.GRAPH,
                name="NonNegativeWeightedGraph",
                supertypes=["WeightedGraph"],
                attributes={"weights": SemanticAttribute("weights", AttributeDomainType.WEIGHT_KIND, "NON_NEGATIVE")}
            )],
            produces_state=[StateContract(
                state_kind=StateKind.DISTANCES,
                name="ShortestPathDistances",
                attributes={"optimality": SemanticAttribute("optimality", AttributeDomainType.OBJECTIVE, "SHORTEST_PATH")},
                mutation_semantics=MutationSemantics.DERIVING
            )],
            required_operations=["INSERT_FRONTIER", "EXTRACT_MIN", "RELAX_EDGE"],
            proof_obligations=["NON_NEGATIVE_WEIGHTS"],
            forbidden_properties={"CONTAINS_NEGATIVE_WEIGHTS"},
            complexity_time="O(E log V)",
            complexity_space="O(V)",
            implementation_backend="cpp_generator:dijkstra_heap"
        ))

        # 4. Answer-Space Binary Search Bisection Provider
        self.register(AlgorithmComponent(
            name="binary_search_bisection_provider",
            category="optimization",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[StateContract(
                state_kind=StateKind.NUMERIC_INTERVAL,
                name="SearchDomainInterval"
            )],
            produces_state=[StateContract(
                state_kind=StateKind.OPTIMIZATION_FRONTIER,
                name="OptimalBoundaryValue",
                mutation_semantics=MutationSemantics.DERIVING
            )],
            required_operations=["BISECTION_STEP", "CHECK_FEASIBILITY"],
            proof_obligations=["MONOTONE_PREDICATE"],
            complexity_time="O(log(Domain))",
            complexity_space="O(1)",
            implementation_backend="cpp_generator:answer_bisection"
        ))

        # 5. Graph BFS/DFS Reachability Feasibility Checker Provider
        self.register(AlgorithmComponent(
            name="graph_reachability_checker_provider",
            category="primitive",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[StateContract(
                state_kind=StateKind.GRAPH,
                name="WeightedGraph",
                supertypes=["GraphState"]
            )],
            produces_state=[StateContract(
                state_kind=StateKind.OPTIMIZATION_FRONTIER,
                name="ReachabilityWitness",
                attributes={"feasible": SemanticAttribute("feasible", AttributeDomainType.BOOLEAN, True)},
                mutation_semantics=MutationSemantics.DERIVING
            )],
            required_operations=["TRAVERSE_THRESHOLD"],
            complexity_time="O(V + E)",
            complexity_space="O(V)",
            implementation_backend="cpp_generator:reachability_bfs"
        ))

        # 6. Tree Heavy-Light Decomposition Range Provider
        self.register(AlgorithmComponent(
            name="hld_tree_path_provider",
            category="decomposition",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[StateContract(
                state_kind=StateKind.TREE,
                name="RootedTree",
                supertypes=["TreeState", "GraphState"]
            )],
            produces_state=[StateContract(
                state_kind=StateKind.SEQUENCE,
                name="HeavyLightPathSegments",
                supertypes=["LinearIntervalSequence", "SequenceState"],
                attributes={"structure": SemanticAttribute("structure", AttributeDomainType.TOPOLOGY, "DISJOINT_INTERVALS")},
                mutation_semantics=MutationSemantics.DERIVING
            )],
            required_operations=["HEAVY_PATH_DECOMPOSE", "MAP_PATH_TO_SEGMENTS"],
            proof_obligations=["CONNECTIVITY_ASSUMPTION", "ACYCLIC_STRUCTURE"],
            complexity_time="O(N)",
            complexity_space="O(N)",
            implementation_backend="cpp_generator:hld_decomposition"
        ))

        # 7. Segment Tree Range Acceleration Provider
        self.register(AlgorithmComponent(
            name="segment_tree_range_acceleration_provider",
            category="data_structure",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[StateContract(
                state_kind=StateKind.SEQUENCE,
                name="LinearIntervalSequence"
            )],
            produces_state=[StateContract(
                state_kind=StateKind.SEQUENCE,
                name="RangeAggregatedSequence",
                supertypes=["TreePathRangeOperation"],
                attributes={"range_queryable": SemanticAttribute("range_queryable", AttributeDomainType.BOOLEAN, True)},
                mutation_semantics=MutationSemantics.DERIVING
            )],
            required_operations=["POINT_UPDATE", "RANGE_QUERY"],
            proof_obligations=["ASSOCIATIVE_OPERATION"],
            complexity_time="O(log N)",
            complexity_space="O(N)",
            implementation_backend="cpp_generator:segment_tree_acceleration"
        ))

        # 8. Fenwick Invertible Prefix Difference Provider
        self.register(AlgorithmComponent(
            name="fenwick_tree_range_acceleration_provider",
            category="data_structure",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[StateContract(
                state_kind=StateKind.SEQUENCE,
                name="LinearIntervalSequence"
            )],
            produces_state=[StateContract(
                state_kind=StateKind.SEQUENCE,
                name="RangeAggregatedSequence",
                supertypes=["TreePathRangeOperation"],
                attributes={"range_queryable": SemanticAttribute("range_queryable", AttributeDomainType.BOOLEAN, True)},
                mutation_semantics=MutationSemantics.DERIVING
            )],
            required_operations=["POINT_UPDATE", "PREFIX_QUERY"],
            proof_obligations=["INVERTIBLE_OPERATION", "ASSOCIATIVE_OPERATION"],
            complexity_time="O(log N)",
            complexity_space="O(N)",
            implementation_backend="cpp_generator:fenwick_acceleration"
        ))

        # 9. Monotonic Deque Convex 1D-1D DP Optimizer
        self.register(AlgorithmComponent(
            name="monotonic_deque_convex_optimizer",
            category="optimization",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[StateContract(
                state_kind=StateKind.DP_TABLE,
                name="ConvexRecurrenceDPTable"
            )],
            produces_state=[StateContract(
                state_kind=StateKind.DP_TABLE,
                name="OptimizedDPTable",
                attributes={"acceleration": SemanticAttribute("acceleration", AttributeDomainType.OBJECTIVE, "LINEAR_TIME")},
                mutation_semantics=MutationSemantics.DERIVING
            )],
            required_operations=["MAINTAIN_SLOPE_ENVELOPE", "QUERY_MIN"],
            proof_obligations=["SLIDING_WINDOW_MONOTONICITY", "DOMINANCE_ORDER", "WINDOW_EXPIRATION"],
            complexity_time="O(N)",
            complexity_space="O(N)",
            implementation_backend="cpp_generator:monotonic_queue_dp"
        ))

        # 10. Greedy Interval Scheduling & Heap Resource Allocator
        self.register(AlgorithmComponent(
            name="greedy_interval_scheduling_heap_provider",
            category="optimization",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[StateContract(
                state_kind=StateKind.SEQUENCE,
                name="IntervalSequence",
                attributes={"ordering": SemanticAttribute("ordering", AttributeDomainType.ORDERING, "START_TIME")}
            )],
            produces_state=[StateContract(
                state_kind=StateKind.PARTITION,
                name="OptimalIntervalPartition",
                mutation_semantics=MutationSemantics.DERIVING
            )],
            required_operations=["EXTRACT_EARLIEST_FINISH", "ALLOCATE_RESOURCE"],
            complexity_time="O(N log N)",
            complexity_space="O(N)",
            implementation_backend="cpp_generator:greedy_heap_intervals"
        ))

        # 11. Tree Subtree Dynamic Programming Provider
        self.register(AlgorithmComponent(
            name="tree_subtree_dp_provider",
            category="optimization",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[StateContract(
                state_kind=StateKind.TREE,
                name="RootedTree",
                supertypes=["TreeState"]
            )],
            produces_state=[StateContract(
                state_kind=StateKind.DP_TABLE,
                name="SubtreeDPTable",
                mutation_semantics=MutationSemantics.DERIVING
            )],
            required_operations=["POSTORDER_DFS", "SUBTREE_RECURRENCE"],
            proof_obligations=["CONNECTIVITY_ASSUMPTION", "ACYCLIC_STRUCTURE"],
            complexity_time="O(N)",
            complexity_space="O(N)",
            implementation_backend="cpp_generator:tree_subtree_dp"
        ))

        # 12. Segment Tree Auxiliary Graph Nodes Provider
        self.register(AlgorithmComponent(
            name="segment_tree_auxiliary_graph_provider",
            category="decomposition",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[StateContract(
                state_kind=StateKind.GRAPH,
                name="IntervalRangeGraph",
                supertypes=["GraphState"]
            )],
            produces_state=[StateContract(
                state_kind=StateKind.GRAPH,
                name="AuxiliarySegmentGraph",
                supertypes=["NonNegativeWeightedGraph", "WeightedGraph", "GraphState"],
                attributes={"weights": SemanticAttribute("weights", AttributeDomainType.WEIGHT_KIND, "NON_NEGATIVE")},
                mutation_semantics=MutationSemantics.DERIVING
            )],
            required_operations=["BUILD_AUXILIARY_TREE_NODES", "ADD_INTERVAL_EDGES"],
            complexity_time="O((V + E) log V)",
            complexity_space="O((V + E) log V)",
            implementation_backend="cpp_generator:segment_tree_graph"
        ))


_GLOBAL_COMPONENT_REGISTRY: Optional[CrossFamilyComponentRegistry] = None

def get_component_registry() -> CrossFamilyComponentRegistry:
    global _GLOBAL_COMPONENT_REGISTRY
    if _GLOBAL_COMPONENT_REGISTRY is None:
        _GLOBAL_COMPONENT_REGISTRY = CrossFamilyComponentRegistry()
    return _GLOBAL_COMPONENT_REGISTRY


def register_standard_components(registry: CrossFamilyComponentRegistry) -> None:
    registry._register_default_components()
