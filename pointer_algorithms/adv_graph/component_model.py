"""
Phase 3N: Component Model & State Contract Unification.

Core Principle:
Algorithms and data structures declare formal inputs (consumes_state) and outputs (produces_state).
State contracts feature explicit type compatibility (IS-A supertypes) and strict attribute unification.
Distinguishes algorithmic components from mathematical reductions/transformations via CompositionNodeType.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Set


# ── 1. Composition Node Type ──

class CompositionNodeType(str, Enum):
    COMPONENT = "COMPONENT"              # Executable algorithmic primitive / data structure (e.g. SCC, DSU, Dinic)
    TRANSFORMATION = "TRANSFORMATION"    # Pure mathematical reduction / derivation (e.g. 2-CNF -> ImplicationGraph)


# ── 2. Formal State Contract & Unification ──

@dataclass
class StateContract:
    """
    Formal mathematical state representation with type hierarchy and attribute unification.
    """
    name: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    supertypes: List[str] = field(default_factory=list)

    def satisfies(self, requirement: "StateContract") -> bool:
        """
        Determines whether this state satisfies the required contract.
        Requires type/supertype compatibility and strict attribute matching.
        No silent omission when explicitly constrained.
        """
        # Type hierarchy match: exact name match or self declares requirement.name as a supertype
        if self.name != requirement.name and requirement.name not in self.supertypes:
            return False

        # Strict attribute unification
        for req_key, req_val in requirement.attributes.items():
            if req_key not in self.attributes:
                # Required attribute is missing from this state
                return False
            if self.attributes[req_key] != req_val:
                # Bound attribute value conflict (e.g. source vertex mismatch)
                return False

        return True


# ── 3. Algorithm Component Dataclass ──

@dataclass
class AlgorithmComponent:
    """
    Declarative capability model for an algorithm, primitive data structure, or transformation.
    """
    name: str
    category: str  # "data_structure", "primitive", "decomposition", "optimization", "transformation"
    node_type: CompositionNodeType = CompositionNodeType.COMPONENT
    consumes_state: List[StateContract] = field(default_factory=list)
    produces_state: List[StateContract] = field(default_factory=list)
    required_operations: List[str] = field(default_factory=list)
    proof_obligations: List[str] = field(default_factory=list)
    complexity_time: str = ""
    complexity_space: str = ""
    implementation_backend: str = ""


# ── 4. Component Registry ──

class ComponentRegistry:
    """
    Centralized registry of all available algorithmic components and transformations.
    Supports provider search via StateContract.satisfies().
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

    def find_providers(self, required_state: StateContract) -> List[AlgorithmComponent]:
        """
        Returns all components that produce a state satisfying required_state.
        """
        providers = []
        for comp in self.components.values():
            for prod_state in comp.produces_state:
                if prod_state.satisfies(required_state):
                    providers.append(comp)
                    break
        return providers

    def _register_default_components(self) -> None:
        # ─────────────────────────────────────────────────────────────
        # A. Classical Data Structures & Primitives
        # ─────────────────────────────────────────────────────────────

        # 1. Disjoint Set Union (DSU)
        self.register(AlgorithmComponent(
            name="disjoint_set_union",
            category="data_structure",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[
                StateContract(name="VertexUniverse")
            ],
            produces_state=[
                StateContract(name="EquivalencePartition"),
                StateContract(name="ForestConnectivity")
            ],
            required_operations=["find_leader", "unite_sets", "connected_check"],
            proof_obligations=["almost_linear_amortized_time", "acyclic_partition_guarantee"],
            complexity_time="O(alpha(V)) per operation",
            complexity_space="O(V)",
            implementation_backend="dsu_backend"
        ))

        # 2. Priority Queue / Min-Heap
        self.register(AlgorithmComponent(
            name="ordered_min_priority_queue",
            category="data_structure",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[],
            produces_state=[
                StateContract(name="OrderedMinExtractionCapability")
            ],
            required_operations=["push", "pop_min", "peek_min"],
            proof_obligations=["heap_order_invariant", "logarithmic_extraction"],
            complexity_time="O(log N)",
            complexity_space="O(N)",
            implementation_backend="heap_backend"
        ))

        # ─────────────────────────────────────────────────────────────
        # B. Graph Decompositions & Algorithms
        # ─────────────────────────────────────────────────────────────

        # 3. Strongly Connected Components (Tarjan / Kosaraju)
        self.register(AlgorithmComponent(
            name="scc_condensation_engine",
            category="decomposition",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[
                StateContract(name="DirectedGraph", attributes={"directed": True})
            ],
            produces_state=[
                StateContract(name="SCCPartition"),
                StateContract(name="CondensationDAG", attributes={"acyclic": True})
            ],
            required_operations=["dfs_low_link_traversal", "component_stack_contraction"],
            proof_obligations=["mutual_reachability_equivalence", "condensation_dag_acyclicity"],
            complexity_time="O(V + E)",
            complexity_space="O(V + E)",
            implementation_backend="tarjan_scc_backend"
        ))

        # 4. Dinic Maximum Flow
        self.register(AlgorithmComponent(
            name="max_flow_dinic",
            category="optimization",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[
                StateContract(name="CapacitatedNetwork", attributes={"directed": True})
            ],
            produces_state=[
                StateContract(name="MaxFlowResult"),
                StateContract(
                    name="SaturatedResidualNetwork",
                    supertypes=["ResidualNetwork"]
                )
            ],
            required_operations=["level_graph_bfs", "blocking_flow_dfs", "current_arc_advance"],
            proof_obligations=["flow_conservation_at_vertices", "capacity_constraints_respected", "max_flow_min_cut_theorem"],
            complexity_time="O(V^2 * E)",
            complexity_space="O(V + E)",
            implementation_backend="dinic_max_flow_backend"
        ))

        # 5. 0-1 BFS (Double-Ended Queue Relaxation)
        self.register(AlgorithmComponent(
            name="deque_01_relaxation",
            category="optimization",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[
                StateContract(name="Binary01Graph", attributes={"weights_binary": True})
            ],
            produces_state=[
                StateContract(name="MonotoneDistanceVector")
            ],
            required_operations=["deque_push_front_zero", "deque_push_back_one", "monotone_distance_update"],
            proof_obligations=["deque_distance_monotonicity_01", "exact_shortest_path_guarantee"],
            complexity_time="O(V + E)",
            complexity_space="O(V)",
            implementation_backend="deque_01_bfs_backend"
        ))

        # 6. SPFA / Negative Cycle Tracer
        self.register(AlgorithmComponent(
            name="spfa_negative_cycle_tracer",
            category="optimization",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[
                StateContract(name="DirectedGraphWithNegativeEdges")
            ],
            produces_state=[
                StateContract(name="ShortestDistanceVectorOrNegativeCycle")
            ],
            required_operations=["queue_relaxation", "relaxation_count_tracking", "parent_pointer_cycle_trace"],
            proof_obligations=["negative_cycle_detection_via_pigeonhole", "valid_parent_chain_traceback"],
            complexity_time="O(V * E) worst-case",
            complexity_space="O(V)",
            implementation_backend="spfa_negative_cycle_backend"
        ))

        # 7. Hierholzer Eulerian Trail Assembler
        self.register(AlgorithmComponent(
            name="hierholzer_trail_assembler",
            category="decomposition",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[
                StateContract(name="EulerianGraph", attributes={"degree_parity_valid": True, "connected": True})
            ],
            produces_state=[
                StateContract(name="EulerianTrail")
            ],
            required_operations=["current_edge_iteration", "trail_backtracking_stitch"],
            proof_obligations=["euler_tour_theorem", "single_edge_traversal_invariant"],
            complexity_time="O(V + E)",
            complexity_space="O(V + E)",
            implementation_backend="hierholzer_eulerian_backend"
        ))

        # 8. Biconnected Block-Cut Decomposer
        self.register(AlgorithmComponent(
            name="block_cut_decomposer",
            category="decomposition",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[
                StateContract(name="UndirectedGraph", attributes={"directed": False})
            ],
            produces_state=[
                StateContract(name="BlockCutTree", attributes={"bipartite_block_tree": True})
            ],
            required_operations=["dfs_articulation_stack", "block_node_extraction"],
            proof_obligations=["biconnectivity_2_vertex_equivalence", "block_cut_tree_structure"],
            complexity_time="O(V + E)",
            complexity_space="O(V + E)",
            implementation_backend="block_cut_tree_backend"
        ))

        # 9. Bridge-Block Decomposer (2-Edge-Connected Components)
        self.register(AlgorithmComponent(
            name="bridge_block_decomposer",
            category="decomposition",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[
                StateContract(name="UndirectedGraph", attributes={"directed": False})
            ],
            produces_state=[
                StateContract(name="BridgeBlockTree", attributes={"2_edge_connected_condensation": True})
            ],
            required_operations=["bridge_identification", "bridge_free_component_contraction"],
            proof_obligations=["bridge_edge_disconnectivity_theorem", "2_edge_connected_partition"],
            complexity_time="O(V + E)",
            complexity_space="O(V + E)",
            implementation_backend="bridge_block_tree_backend"
        ))

        # 10. Kuhn Maximum Bipartite Matching
        self.register(AlgorithmComponent(
            name="bipartite_matching_kuhn",
            category="optimization",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[
                StateContract(name="BipartiteGraphModel", attributes={"bipartite": True})
            ],
            produces_state=[
                StateContract(name="MaximumMatchingAssignment")
            ],
            required_operations=["alternating_path_dfs", "matching_partner_flip"],
            proof_obligations=["berges_lemma_augmenting_paths", "hall_marriage_condition_soundness"],
            complexity_time="O(V * E)",
            complexity_space="O(V)",
            implementation_backend="kuhn_matching_backend"
        ))

        # 11. MCMF Successive Shortest Path
        self.register(AlgorithmComponent(
            name="mcmf_successive_shortest_path",
            category="optimization",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[
                StateContract(name="CapacitatedCostNetwork", attributes={"capacitated": True, "has_cost": True})
            ],
            produces_state=[
                StateContract(name="MinCostMaxFlowResult")
            ],
            required_operations=["residual_cost_relaxation", "augmenting_path_capacity_flow", "potential_update"],
            proof_obligations=["reduced_cost_optimality_invariant", "successive_shortest_path_optimality"],
            complexity_time="O(F * E log V) or O(F * V * E)",
            complexity_space="O(V + E)",
            implementation_backend="mcmf_backend"
        ))

        # ─────────────────────────────────────────────────────────────
        # C. Pure Mathematical Reductions / Transformations
        # ─────────────────────────────────────────────────────────────

        # Transformation 1: 2-CNF to Implication Directed Graph
        self.register(AlgorithmComponent(
            name="two_cnf_to_implication_graph",
            category="transformation",
            node_type=CompositionNodeType.TRANSFORMATION,
            consumes_state=[
                StateContract(name="TwoCnfFormula", attributes={"clause_cardinality": 2})
            ],
            produces_state=[
                StateContract(
                    name="DirectedGraph",
                    attributes={"directed": True, "implication_model": True}
                )
            ],
            required_operations=["clause_to_contrapositive_implications"],
            proof_obligations=["implication_logic_equivalence"],
            complexity_time="O(Variables + Clauses)",
            complexity_space="O(Variables + Clauses)",
            implementation_backend="two_cnf_implication_reduction"
        ))

        # Transformation 2: SCC Partition to 2-SAT Truth Assignment
        self.register(AlgorithmComponent(
            name="scc_to_twosat_assignment",
            category="transformation",
            node_type=CompositionNodeType.TRANSFORMATION,
            consumes_state=[
                StateContract(name="SCCPartition")
            ],
            produces_state=[
                StateContract(name="TwoSatAssignmentResult")
            ],
            required_operations=["contradiction_check_variable_vs_negation", "topological_component_assignment"],
            proof_obligations=["twosat_satisfiability_theorem", "consistent_truth_assignment_guarantee"],
            complexity_time="O(Variables)",
            complexity_space="O(Variables)",
            implementation_backend="twosat_assignment_reduction"
        ))

        # Transformation 3: Saturated Residual Network to Min-Cut Partition
        self.register(AlgorithmComponent(
            name="saturated_residual_to_min_cut",
            category="transformation",
            node_type=CompositionNodeType.TRANSFORMATION,
            consumes_state=[
                StateContract(name="SaturatedResidualNetwork")
            ],
            produces_state=[
                StateContract(name="MinCutPartition")
            ],
            required_operations=["residual_bfs_source_reachability", "cut_edge_collection"],
            proof_obligations=["max_flow_min_cut_duality", "cut_capacity_equals_max_flow"],
            complexity_time="O(V + E)",
            complexity_space="O(V)",
            implementation_backend="min_cut_residual_reduction"
        ))

        # Transformation 4: Weighted Undirected Graph to Sorted Edge List
        self.register(AlgorithmComponent(
            name="graph_edge_sorting",
            category="transformation",
            node_type=CompositionNodeType.TRANSFORMATION,
            consumes_state=[
                StateContract(name="WeightedUndirectedGraph", attributes={"directed": False, "weighted": True})
            ],
            produces_state=[
                StateContract(name="SortedEdgeList", attributes={"sorted_by_weight": True})
            ],
            required_operations=["edge_extraction", "weight_comparison_sort"],
            proof_obligations=["total_ordering_preservation"],
            complexity_time="O(E log E)",
            complexity_space="O(E)",
            implementation_backend="edge_sorting_reduction"
        ))

        # Transformation 5: Sorted Edges + DSU to Spanning Forest (Kruskal Composition)
        self.register(AlgorithmComponent(
            name="cycle_free_edge_selection",
            category="transformation",
            node_type=CompositionNodeType.TRANSFORMATION,
            consumes_state=[
                StateContract(name="SortedEdgeList", attributes={"sorted_by_weight": True}),
                StateContract(name="EquivalencePartition")
            ],
            produces_state=[
                StateContract(name="SpanningForestResult")
            ],
            required_operations=["scan_edges_in_order", "dsu_unite_if_disconnected"],
            proof_obligations=["cut_property_greedy_choice", "cycle_avoidance_invariant"],
            complexity_time="O(E * alpha(V))",
            complexity_space="O(V)",
            implementation_backend="kruskal_cycle_free_selection"
        ))
