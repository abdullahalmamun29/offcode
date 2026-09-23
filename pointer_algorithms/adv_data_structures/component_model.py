"""
CHUP Phase 3S — Advanced Data Structures Component Registry & Composition Model.

Defines the formal AlgorithmComponent abstraction and the AdvancedDataStructureComponentRegistry,
registering all 10 canonical patterns with typed StateContracts, capability dependencies,
preconditions, proof obligations, and provider-derived complexities.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
from pointer_algorithms.adv_data_structures.ads_state_contracts import (
    StateContract,
    make_sparse_table_state,
    make_tree_topology_state,
    make_binary_lifting_lca_state,
    make_heavy_light_decomposition_state,
    make_centroid_tree_state,
    make_persistent_segment_tree_state,
    make_dynamic_segment_tree_state,
    make_merge_sort_tree_state,
    make_sqrt_decomposition_state,
    make_mos_query_schedule_state,
    make_segment_tree_beats_state,
)


class CompositionNodeType(str, Enum):
    PRIMITIVE = "PRIMITIVE"
    COMPOSITE = "COMPOSITE"
    ADAPTER = "ADAPTER"
    COMPONENT = "COMPONENT"


@dataclass
class AlgorithmComponent:
    """
    Formal Architecture V2 component definition.
    Components declare input/output state contracts, required and provided
    capabilities, preconditions, proof obligations, and complexity bounds.
    """
    name: str
    node_type: CompositionNodeType
    consumes_state: List[StateContract]
    produces_state: List[StateContract]
    requires_capabilities: List[str]
    provided_capabilities: List[str]
    preconditions: List[str]
    proof_obligations: List[str]
    operation_complexity: str
    space_complexity: str
    correctness_guarantee: str
    description: str


class AdvancedDataStructureComponentRegistry:
    """
    Registry of canonical Phase 3S advanced data structure components.
    """
    def __init__(self):
        self._components: Dict[str, AlgorithmComponent] = {}
        self._register_canonical_components()

    def register(self, component: AlgorithmComponent):
        self._components[component.name] = component

    def get(self, name: str) -> Optional[AlgorithmComponent]:
        return self._components.get(name)

    def list_components(self) -> List[AlgorithmComponent]:
        return list(self._components.values())

    def _register_canonical_components(self):
        # ── 1. Sparse Table RMQ (3S-A) ──
        self.register(AlgorithmComponent(
            name="sparse_table_rmq",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_sparse_table_state()],
            produces_state=[StateContract("RangeQueryResultState")],
            requires_capabilities=[],
            provided_capabilities=["STATIC_RMQ", "SPARSE_TABLE", "IDEMPOTENT_RANGE_QUERY"],
            preconditions=["operation_associative", "operation_idempotent"],
            proof_obligations=["overlapping_power_of_two_covering_proven", "table_power_of_two_transition_soundness"],
            operation_complexity="O(1) query, O(N log N) build",
            space_complexity="O(N log N)",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Static table supporting O(1) query for associative and idempotent semigroup operations via overlapping blocks."
        ))

        # ── 2. Binary Lifting LCA (3S-B) ──
        self.register(AlgorithmComponent(
            name="binary_lifting_lca",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_tree_topology_state()],
            produces_state=[make_binary_lifting_lca_state()],
            requires_capabilities=[],
            provided_capabilities=["LOWEST_COMMON_ANCESTOR", "KTH_ANCESTOR", "BINARY_LIFTING"],
            preconditions=["topology_is_valid_tree", "tree_root_valid"],
            proof_obligations=["binary_lifting_recurrence_soundness", "depth_monotonicity_proven"],
            operation_complexity="O(log N) query, O(N log N) build",
            space_complexity="O(N log N)",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Tree jump pointers up[u][k] for O(log N) Lowest Common Ancestor and k-th ancestor queries."
        ))

        # ── 3. Heavy-Light Decomposition (3S-C) ──
        self.register(AlgorithmComponent(
            name="heavy_light_decomposition",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_tree_topology_state()],
            produces_state=[make_heavy_light_decomposition_state()],
            requires_capabilities=["RANGE_QUERY"],
            provided_capabilities=["TREE_PATH_QUERY", "TREE_PATH_UPDATE", "HEAVY_LIGHT_DECOMPOSITION"],
            preconditions=["topology_is_valid_tree", "has_range_structure_provider"],
            proof_obligations=["log_n_heavy_chains_bound_proven", "dfs_interval_continuity_proven"],
            operation_complexity="O(log N * T_range) path op, O(N) build",
            space_complexity="O(N)",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Decomposes tree paths into at most O(log N) contiguous heavy chains mapped to an underlying range provider."
        ))

        # ── 4. Centroid Decomposition (3S-D) ──
        self.register(AlgorithmComponent(
            name="centroid_tree_builder",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_tree_topology_state()],
            produces_state=[make_centroid_tree_state()],
            requires_capabilities=[],
            provided_capabilities=["CENTROID_DECOMPOSITION", "BALANCED_TREE_DECOMPOSITION"],
            preconditions=["topology_is_valid_tree"],
            proof_obligations=["subtree_half_size_bound_proven", "centroid_depth_log_n_bound_proven"],
            operation_complexity="O(N log N) build, O(log N) ancestor path query",
            space_complexity="O(N)",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Balanced divide-and-conquer tree decomposition guaranteeing component size <= floor(size/2) and depth <= floor(log2 N) + 1."
        ))

        # ── 5. Persistent Segment Tree (3S-E) ──
        self.register(AlgorithmComponent(
            name="persistent_segment_tree",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_persistent_segment_tree_state()],
            produces_state=[StateContract("HistoricalRangeQueryResultState")],
            requires_capabilities=[],
            provided_capabilities=["PERSISTENT_RANGE_QUERY", "HISTORICAL_VERSION_QUERY", "RANGE_KTH_ORDER_STATISTIC"],
            preconditions=["version_root_valid", "path_copying_immutability_preserved"],
            proof_obligations=["path_copying_log_n_nodes_proven", "historical_root_immutability_soundness"],
            operation_complexity="O(log N) update, O(log N) query, O(N) build",
            space_complexity="O(N + Q log N)",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Path-copying immutable version tree enabling queries and updates across historical roots."
        ))

        # ── 6. Dynamic Segment Tree (3S-F) ──
        self.register(AlgorithmComponent(
            name="dynamic_sparse_segment_tree",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_dynamic_segment_tree_state()],
            produces_state=[StateContract("SparseRangeQueryResultState")],
            requires_capabilities=[],
            provided_capabilities=["DYNAMIC_SEGMENT_TREE", "SPARSE_COORDINATE_RANGE_QUERY"],
            preconditions=["domain_bounds_valid", "node_pool_capacity_sufficient"],
            proof_obligations=["overflow_safe_midpoint_soundness", "lazy_node_allocation_path_bound_proven"],
            operation_complexity="O(log C) update/query",
            space_complexity="O(Q log C)",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Pointer-based lazy node allocation over large coordinate domains with overflow-safe midpoint calculation."
        ))

        # ── 7. Merge Sort Tree (3S-G) ──
        self.register(AlgorithmComponent(
            name="merge_sort_tree",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_merge_sort_tree_state()],
            produces_state=[StateContract("RangeOrderStatisticResultState")],
            requires_capabilities=[],
            provided_capabilities=["RANGE_COUNT_LEQ", "MERGE_SORT_TREE", "STATIC_RANGE_RANK"],
            preconditions=["structure_is_static", "objective_supported"],
            proof_obligations=["sorted_vector_merge_soundness", "log2_n_binary_search_bound_proven"],
            operation_complexity="O(log^2 N) query, O(N log N) build",
            space_complexity="O(N log N)",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Static segment tree storing sorted vectors at nodes for O(log^2 N) range order-statistic queries; updates disallowed."
        ))

        # ── 8. Sqrt Decomposition (3S-H) ──
        self.register(AlgorithmComponent(
            name="sqrt_block_decomposition",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_sqrt_decomposition_state()],
            produces_state=[StateContract("BlockPartitionResultState")],
            requires_capabilities=[],
            provided_capabilities=["SQRT_DECOMPOSITION", "BLOCK_PARTITION_RANGE_QUERY"],
            preconditions=["block_size_optimal"],
            proof_obligations=["sqrt_n_balance_soundness", "partial_block_point_walk_soundness"],
            operation_complexity="O(sqrt(N)) update/query, O(N) build",
            space_complexity="O(N)",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Partitioning array into blocks of size B = ceil(sqrt(N)) balancing whole-block updates and partial point walks."
        ))

        # ── 9. Mo's Algorithm (3S-I) ──
        self.register(AlgorithmComponent(
            name="mos_algorithm_offline",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_mos_query_schedule_state()],
            produces_state=[StateContract("OfflineBatchQueryResultState")],
            requires_capabilities=[],
            provided_capabilities=["MOS_ALGORITHM", "OFFLINE_RANGE_QUERY_SCHEDULE"],
            preconditions=["queries_known_offline", "state_transitions_reversible"],
            proof_obligations=["pointer_movements_n2_b_plus_qb_proven", "semantic_reversibility_invariance_proven"],
            operation_complexity="O((N + Q) sqrt(N) * T_transition)",
            space_complexity="O(N + Q)",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Offline range query scheduler using block snake ordering with O(N^2/B + QB) pointer movements and reversible state transitions."
        ))

        # ── 10. Segment Tree Beats (3S-J) ──
        self.register(AlgorithmComponent(
            name="segment_tree_beats_chmin",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_segment_tree_beats_state()],
            produces_state=[StateContract("AdaptiveTagRangeResultState")],
            requires_capabilities=[],
            provided_capabilities=["RANGE_CHMIN", "SEGMENT_TREE_BEATS", "CURRENT_MAX_HIERARCHY"],
            preconditions=["operations_within_supported_set", "leaf_sentinel_initialized"],
            proof_obligations=["amortized_log_n_chmin_bound_proven", "max1_max2_hierarchy_monotonicity_proven"],
            operation_complexity="O((N + Q) log N) amortized",
            space_complexity="O(N)",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Range chmin and current max hierarchy maintenance (max1 > max2, cnt_max) with leaf sentinel -INF and tag break conditions."
        ))
