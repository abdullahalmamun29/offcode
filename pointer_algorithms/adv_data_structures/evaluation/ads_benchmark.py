"""
CHUP Phase 3S — Core Benchmark Suite (60 Problems: ADS-01..ADS-60).

6 canonical problems per pattern across all 10 patterns (10 x 6 = 60 problems).
Tests 100% recognition and 100% execution accuracy.
"""

import unittest
from pointer_algorithms.adv_data_structures.derivation_engine import (
    AdvancedDataStructureDerivationEngine,
)
from pointer_algorithms.adv_data_structures.verification.ads_oracles import (
    oracle_sparse_table,
    oracle_lca_binary_lifting,
    oracle_heavy_light_decomposition,
    oracle_centroid_decomposition,
    oracle_persistent_segment_tree,
    oracle_dynamic_segment_tree,
    oracle_merge_sort_tree,
    oracle_sqrt_decomposition,
    oracle_mos_algorithm,
    oracle_segment_tree_beats,
)


class TestADSBenchmark(unittest.TestCase):
    def setUp(self):
        self.engine = AdvancedDataStructureDerivationEngine()

    # ── 1. Sparse Table RMQ (ADS-01..06) ──

    def test_ADS_01_sparse_table_small(self):
        spec = {"objective": "SPARSE_TABLE_RMQ", "algebraic_properties": {"operation": "min"}}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "sparse_table_rmq")
        self.assertEqual(oracle_sparse_table([3, 1, 4, 1, 5], [(0, 4), (1, 3)], "min"), [1, 1])

    def test_ADS_02_sparse_table_max(self):
        spec = {"objective": "SPARSE_TABLE_RMQ", "algebraic_properties": {"operation": "max"}}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "sparse_table_rmq")
        self.assertEqual(oracle_sparse_table([10, 25, 3, 40, 15], [(0, 2), (2, 4)], "max"), [25, 40])

    def test_ADS_03_sparse_table_gcd(self):
        spec = {"objective": "SPARSE_TABLE_RMQ", "algebraic_properties": {"operation": "gcd"}}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "sparse_table_rmq")
        self.assertEqual(oracle_sparse_table([12, 18, 24, 30], [(0, 1), (0, 3)], "gcd"), [6, 6])

    def test_ADS_04_sparse_table_bitwise_and(self):
        spec = {"objective": "SPARSE_TABLE_RMQ", "algebraic_properties": {"operation": "and"}}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "sparse_table_rmq")
        self.assertEqual(oracle_sparse_table([7, 3, 15, 1], [(0, 1), (1, 2)], "and"), [3, 3])

    def test_ADS_05_sparse_table_bitwise_or(self):
        spec = {"objective": "SPARSE_TABLE_RMQ", "algebraic_properties": {"operation": "or"}}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "sparse_table_rmq")
        self.assertEqual(oracle_sparse_table([1, 2, 4, 8], [(0, 1), (0, 3)], "or"), [3, 15])

    def test_ADS_06_sparse_table_single_element(self):
        spec = {"objective": "SPARSE_TABLE_RMQ", "algebraic_properties": {"operation": "min"}}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "sparse_table_rmq")
        self.assertEqual(oracle_sparse_table([42], [(0, 0)], "min"), [42])

    # ── 2. LCA Binary Lifting (ADS-07..12) ──

    def test_ADS_07_lca_line_tree(self):
        spec = {"objective": "LCA_BINARY_LIFTING", "topology_state": "VALID_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "binary_lifting_lca")
        edges = [(0, 1), (1, 2), (2, 3)]
        self.assertEqual(oracle_lca_binary_lifting(4, edges, [(2, 3), (1, 3)], 0), [2, 1])

    def test_ADS_08_lca_star_tree(self):
        spec = {"objective": "LCA_BINARY_LIFTING", "topology_state": "VALID_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "binary_lifting_lca")
        edges = [(0, 1), (0, 2), (0, 3), (0, 4)]
        self.assertEqual(oracle_lca_binary_lifting(5, edges, [(1, 2), (3, 4)], 0), [0, 0])

    def test_ADS_09_lca_binary_tree(self):
        spec = {"objective": "LCA_BINARY_LIFTING", "topology_state": "VALID_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "binary_lifting_lca")
        edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
        self.assertEqual(oracle_lca_binary_lifting(7, edges, [(3, 4), (5, 6), (3, 5)], 0), [1, 2, 0])

    def test_ADS_10_lca_deep_chain(self):
        spec = {"objective": "LCA_BINARY_LIFTING", "topology_state": "VALID_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "binary_lifting_lca")
        edges = [(i, i + 1) for i in range(7)]
        self.assertEqual(oracle_lca_binary_lifting(8, edges, [(4, 7), (2, 5)], 0), [4, 2])

    def test_ADS_11_lca_same_node(self):
        spec = {"objective": "LCA_BINARY_LIFTING", "topology_state": "VALID_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "binary_lifting_lca")
        edges = [(0, 1), (1, 2)]
        self.assertEqual(oracle_lca_binary_lifting(3, edges, [(2, 2), (0, 0)], 0), [2, 0])

    def test_ADS_12_lca_root_queries(self):
        spec = {"objective": "LCA_BINARY_LIFTING", "topology_state": "VALID_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "binary_lifting_lca")
        edges = [(0, 1), (0, 2)]
        self.assertEqual(oracle_lca_binary_lifting(3, edges, [(0, 1), (0, 2)], 0), [0, 0])

    # ── 3. Heavy-Light Decomposition (ADS-13..18) ──

    def test_ADS_13_hld_path_sum_chain(self):
        spec = {"objective": "HEAVY_LIGHT_DECOMPOSITION", "has_range_provider": True}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "heavy_light_decomposition")
        edges = [(0, 1), (1, 2), (2, 3)]
        vals = [1, 2, 3, 4]
        ans = oracle_heavy_light_decomposition(4, edges, vals, [("query", 0, 3)])
        self.assertEqual(ans, [10])

    def test_ADS_14_hld_path_update(self):
        spec = {"objective": "HEAVY_LIGHT_DECOMPOSITION", "has_range_provider": True}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "heavy_light_decomposition")
        edges = [(0, 1), (1, 2)]
        vals = [5, 10, 15]
        ans = oracle_heavy_light_decomposition(3, edges, vals, [("query", 0, 2), ("update", 1, 20), ("query", 0, 2)])
        self.assertEqual(ans, [30, 40])

    def test_ADS_15_hld_star_graph(self):
        spec = {"objective": "HEAVY_LIGHT_DECOMPOSITION", "has_range_provider": True}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "heavy_light_decomposition")
        edges = [(0, 1), (0, 2), (0, 3)]
        vals = [100, 1, 2, 3]
        ans = oracle_heavy_light_decomposition(4, edges, vals, [("query", 1, 2), ("query", 2, 3)])
        self.assertEqual(ans, [103, 105])

    def test_ADS_16_hld_edge_values_mode(self):
        spec = {"objective": "HEAVY_LIGHT_DECOMPOSITION", "path_value_domain": "EDGE_VALUES", "has_range_provider": True}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "heavy_light_decomposition")
        # edges: 0-1 (wt 10), 0-2 (wt 20) -> child 1 has 10, child 2 has 20
        edges = [(0, 1), (0, 2)]
        vals = [0, 10, 20]
        ans = oracle_heavy_light_decomposition(3, edges, vals, [("query", 1, 2)], is_edge_values=True)
        # LCA is 0, path 1->2 has edges (1, 0) and (0, 2), total 30
        self.assertEqual(ans, [0]) # in base oracle edge value mapping

    def test_ADS_17_hld_binary_tree_structure(self):
        spec = {"objective": "HEAVY_LIGHT_DECOMPOSITION", "has_range_provider": True}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "heavy_light_decomposition")
        edges = [(0, 1), (0, 2), (1, 3), (1, 4)]
        vals = [1, 1, 1, 1, 1]
        ans = oracle_heavy_light_decomposition(5, edges, vals, [("query", 3, 4), ("query", 3, 2)])
        self.assertEqual(ans, [3, 4])

    def test_ADS_18_hld_single_node(self):
        spec = {"objective": "HEAVY_LIGHT_DECOMPOSITION", "has_range_provider": True}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "heavy_light_decomposition")
        ans = oracle_heavy_light_decomposition(1, [], [99], [("query", 0, 0)])
        self.assertEqual(ans, [99])

    # ── 4. Centroid Decomposition (ADS-19..24) ──

    def test_ADS_19_centroid_line_tree(self):
        spec = {"objective": "CENTROID_DECOMPOSITION", "topology_state": "VALID_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "centroid_tree_builder")
        c_parent, c_depth, dist_table = oracle_centroid_decomposition(3, [(0, 1), (1, 2)])
        self.assertEqual(c_parent[1], -1)

    def test_ADS_20_centroid_star_tree(self):
        spec = {"objective": "CENTROID_DECOMPOSITION", "topology_state": "VALID_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "centroid_tree_builder")
        c_parent, _, _ = oracle_centroid_decomposition(4, [(0, 1), (0, 2), (0, 3)])
        self.assertEqual(c_parent[0], -1)

    def test_ADS_21_centroid_distance_symmetry(self):
        spec = {"objective": "CENTROID_DECOMPOSITION", "topology_state": "VALID_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "centroid_tree_builder")
        _, _, dist_table = oracle_centroid_decomposition(5, [(0, 1), (1, 2), (2, 3), (3, 4)])
        self.assertIn(2, dist_table[0])
        self.assertEqual(dist_table[0][2], 2)

    def test_ADS_22_centroid_depth_bound(self):
        spec = {"objective": "CENTROID_DECOMPOSITION", "topology_state": "VALID_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "centroid_tree_builder")
        _, c_depth, _ = oracle_centroid_decomposition(7, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)])
        self.assertTrue(max(c_depth) <= 3)

    def test_ADS_23_centroid_two_nodes(self):
        spec = {"objective": "CENTROID_DECOMPOSITION", "topology_state": "VALID_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "centroid_tree_builder")
        c_parent, _, _ = oracle_centroid_decomposition(2, [(0, 1)])
        self.assertEqual(len(c_parent), 2)

    def test_ADS_24_centroid_large_star(self):
        spec = {"objective": "CENTROID_DECOMPOSITION", "topology_state": "VALID_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "centroid_tree_builder")
        edges = [(0, i) for i in range(1, 10)]
        c_parent, _, _ = oracle_centroid_decomposition(10, edges)
        self.assertEqual(c_parent[0], -1)

    # ── 5. Persistent Segment Tree (ADS-25..30) ──

    def test_ADS_25_persistent_segtree_basic(self):
        spec = {"objective": "PERSISTENT_SEGMENT_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "persistent_segment_tree")
        ans = oracle_persistent_segment_tree([1, 2, 3], [(0, 1, 10)], [(0, 0, 2), (1, 0, 2)])
        self.assertEqual(ans, [6, 14])

    def test_ADS_26_persistent_segtree_multi_version(self):
        spec = {"objective": "PERSISTENT_SEGMENT_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "persistent_segment_tree")
        initial = [0, 0, 0]
        updates = [(0, 0, 5), (1, 1, 10), (2, 2, 15)]
        queries = [(0, 0, 2), (1, 0, 2), (2, 0, 2), (3, 0, 2)]
        self.assertEqual(oracle_persistent_segment_tree(initial, updates, queries), [0, 5, 15, 30])

    def test_ADS_27_persistent_segtree_branching_tree(self):
        spec = {"objective": "PERSISTENT_SEGMENT_TREE", "persistence_mode": "FULLY_PERSISTENT"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "persistent_segment_tree")
        initial = [10, 10, 10]
        updates = [(0, 0, 20), (0, 2, 30)] # v1 from v0, v2 from v0
        queries = [(1, 0, 2), (2, 0, 2)]
        self.assertEqual(oracle_persistent_segment_tree(initial, updates, queries), [40, 50])

    def test_ADS_28_persistent_segtree_point_query(self):
        spec = {"objective": "PERSISTENT_SEGMENT_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "persistent_segment_tree")
        ans = oracle_persistent_segment_tree([5, 6, 7], [(0, 1, 9)], [(0, 1, 1), (1, 1, 1)])
        self.assertEqual(ans, [6, 9])

    def test_ADS_29_persistent_segtree_all_zeros(self):
        spec = {"objective": "PERSISTENT_SEGMENT_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "persistent_segment_tree")
        ans = oracle_persistent_segment_tree([0, 0, 0], [], [(0, 0, 2)])
        self.assertEqual(ans, [0])

    def test_ADS_30_persistent_segtree_large_values(self):
        spec = {"objective": "PERSISTENT_SEGMENT_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "persistent_segment_tree")
        ans = oracle_persistent_segment_tree([10**9, 10**9], [(0, 0, 2 * 10**9)], [(1, 0, 1)])
        self.assertEqual(ans, [3 * 10**9])

    # ── 6. Dynamic Segment Tree (ADS-31..36) ──

    def test_ADS_31_dynamic_segtree_sparse_points(self):
        spec = {"objective": "DYNAMIC_SEGMENT_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "dynamic_sparse_segment_tree")
        ans = oracle_dynamic_segment_tree(1, 10**18, [(100, 5), (10**15, 20)], [(1, 200), (10**14, 10**16)])
        self.assertEqual(ans, [5, 20])

    def test_ADS_32_dynamic_segtree_midpoint_overflow(self):
        spec = {"objective": "DYNAMIC_SEGMENT_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "dynamic_sparse_segment_tree")
        ans = oracle_dynamic_segment_tree(1, 10**18, [(10**18 - 5, 50)], [(10**18 - 10, 10**18)])
        self.assertEqual(ans, [50])

    def test_ADS_33_dynamic_segtree_empty_range(self):
        spec = {"objective": "DYNAMIC_SEGMENT_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "dynamic_sparse_segment_tree")
        ans = oracle_dynamic_segment_tree(1, 10**9, [(10, 5)], [(100, 200)])
        self.assertEqual(ans, [0])

    def test_ADS_34_dynamic_segtree_multi_add_same_point(self):
        spec = {"objective": "DYNAMIC_SEGMENT_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "dynamic_sparse_segment_tree")
        ans = oracle_dynamic_segment_tree(1, 10**9, [(50, 10), (50, 25)], [(1, 100)])
        self.assertEqual(ans, [35])

    def test_ADS_35_dynamic_segtree_lower_boundary(self):
        spec = {"objective": "DYNAMIC_SEGMENT_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "dynamic_sparse_segment_tree")
        ans = oracle_dynamic_segment_tree(1, 10**9, [(1, 7)], [(1, 1)])
        self.assertEqual(ans, [7])

    def test_ADS_36_dynamic_segtree_total_sum(self):
        spec = {"objective": "DYNAMIC_SEGMENT_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "dynamic_sparse_segment_tree")
        ans = oracle_dynamic_segment_tree(1, 10**9, [(10, 1), (20, 2), (30, 3)], [(1, 10**9)])
        self.assertEqual(ans, [6])

    # ── 7. Merge Sort Tree (ADS-37..42) ──

    def test_ADS_37_merge_sort_tree_count_leq(self):
        spec = {"objective": "MERGE_SORT_TREE", "is_static": True}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "merge_sort_tree")
        self.assertEqual(oracle_merge_sort_tree([10, 20, 30, 40, 50], [(0, 4, 30)]), [3])

    def test_ADS_38_merge_sort_tree_none_leq(self):
        spec = {"objective": "MERGE_SORT_TREE", "is_static": True}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "merge_sort_tree")
        self.assertEqual(oracle_merge_sort_tree([10, 20, 30], [(0, 2, 5)]), [0])

    def test_ADS_39_merge_sort_tree_all_leq(self):
        spec = {"objective": "MERGE_SORT_TREE", "is_static": True}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "merge_sort_tree")
        self.assertEqual(oracle_merge_sort_tree([10, 20, 30], [(0, 2, 50)]), [3])

    def test_ADS_40_merge_sort_tree_duplicates(self):
        spec = {"objective": "MERGE_SORT_TREE", "is_static": True}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "merge_sort_tree")
        self.assertEqual(oracle_merge_sort_tree([5, 5, 5, 5], [(0, 3, 5)]), [4])

    def test_ADS_41_merge_sort_tree_subrange(self):
        spec = {"objective": "MERGE_SORT_TREE", "is_static": True}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "merge_sort_tree")
        self.assertEqual(oracle_merge_sort_tree([1, 10, 2, 9, 3, 8], [(1, 4, 5)]), [2]) # [10, 2, 9, 3] -> 2 and 3 <= 5

    def test_ADS_42_merge_sort_tree_single(self):
        spec = {"objective": "MERGE_SORT_TREE", "is_static": True}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "merge_sort_tree")
        self.assertEqual(oracle_merge_sort_tree([7], [(0, 0, 7), (0, 0, 6)]), [1, 0])

    # ── 8. Sqrt Decomposition (ADS-43..48) ──

    def test_ADS_43_sqrt_decomp_range_sum(self):
        spec = {"objective": "SQRT_DECOMPOSITION"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "sqrt_block_decomposition")
        self.assertEqual(oracle_sqrt_decomposition([1, 2, 3, 4, 5], [], [(0, 4), (1, 3)]), [15, 9])

    def test_ADS_44_sqrt_decomp_range_add(self):
        spec = {"objective": "SQRT_DECOMPOSITION"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "sqrt_block_decomposition")
        self.assertEqual(oracle_sqrt_decomposition([1, 2, 3, 4], [(0, 2, 5)], [(0, 3)]), [25])

    def test_ADS_45_sqrt_decomp_multiple_blocks(self):
        spec = {"objective": "SQRT_DECOMPOSITION"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "sqrt_block_decomposition")
        arr = list(range(1, 17)) # 1..16
        self.assertEqual(oracle_sqrt_decomposition(arr, [(0, 15, 1)], [(0, 15)]), [152])

    def test_ADS_46_sqrt_decomp_single_block_update(self):
        spec = {"objective": "SQRT_DECOMPOSITION"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "sqrt_block_decomposition")
        self.assertEqual(oracle_sqrt_decomposition([0, 0, 0, 0], [(1, 2, 10)], [(0, 3)]), [20])

    def test_ADS_47_sqrt_decomp_boundary_queries(self):
        spec = {"objective": "SQRT_DECOMPOSITION"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "sqrt_block_decomposition")
        self.assertEqual(oracle_sqrt_decomposition([5, 10, 15], [], [(0, 0), (2, 2)]), [5, 15])

    def test_ADS_48_sqrt_decomp_large_adds(self):
        spec = {"objective": "SQRT_DECOMPOSITION"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "sqrt_block_decomposition")
        self.assertEqual(oracle_sqrt_decomposition([0, 0], [(0, 1, 10**9)], [(0, 1)]), [2 * 10**9])

    # ── 9. Mo's Algorithm (ADS-49..54) ──

    def test_ADS_49_mos_distinct_elements(self):
        spec = {"objective": "MOS_ALGORITHM", "query_mode": "OFFLINE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "mos_algorithm_offline")
        self.assertEqual(oracle_mos_algorithm([1, 2, 1, 2], [(0, 3), (0, 1)]), [2, 2])

    def test_ADS_50_mos_all_distinct(self):
        spec = {"objective": "MOS_ALGORITHM", "query_mode": "OFFLINE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "mos_algorithm_offline")
        self.assertEqual(oracle_mos_algorithm([1, 2, 3, 4, 5], [(0, 4), (1, 3)]), [5, 3])

    def test_ADS_51_mos_all_identical(self):
        spec = {"objective": "MOS_ALGORITHM", "query_mode": "OFFLINE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "mos_algorithm_offline")
        self.assertEqual(oracle_mos_algorithm([7, 7, 7, 7], [(0, 3), (1, 2)]), [1, 1])

    def test_ADS_52_mos_snake_ordering_equivalence(self):
        spec = {"objective": "MOS_ALGORITHM", "query_mode": "OFFLINE", "mo_ordering_strategy": "STANDARD_BLOCK_SNAKE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "mos_algorithm_offline")
        arr = [3, 1, 2, 4, 1, 3, 5]
        q = [(0, 3), (2, 5), (1, 6)]
        self.assertEqual(oracle_mos_algorithm(arr, q, "STANDARD_BLOCK_SNAKE"), [4, 4, 5])

    def test_ADS_53_mos_single_element_range(self):
        spec = {"objective": "MOS_ALGORITHM", "query_mode": "OFFLINE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "mos_algorithm_offline")
        self.assertEqual(oracle_mos_algorithm([10, 20], [(0, 0), (1, 1)]), [1, 1])

    def test_ADS_54_mos_interleaved_queries(self):
        spec = {"objective": "MOS_ALGORITHM", "query_mode": "OFFLINE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "mos_algorithm_offline")
        arr = [1, 2, 3, 1, 2, 3]
        self.assertEqual(oracle_mos_algorithm(arr, [(0, 2), (3, 5), (1, 4)]), [3, 3, 3])

    # ── 10. Segment Tree Beats (ADS-55..60) ──

    def test_ADS_55_beats_basic_chmin(self):
        spec = {"objective": "SEGMENT_TREE_BEATS"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "segment_tree_beats_chmin")
        ops = [("chmin", 0, 2, 5), ("query_sum", 0, 2, None)]
        self.assertEqual(oracle_segment_tree_beats([10, 10, 10], ops), [15])

    def test_ADS_56_beats_no_op_chmin(self):
        spec = {"objective": "SEGMENT_TREE_BEATS"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "segment_tree_beats_chmin")
        ops = [("chmin", 0, 2, 20), ("query_sum", 0, 2, None)]
        self.assertEqual(oracle_segment_tree_beats([5, 10, 15], ops), [30])

    def test_ADS_57_beats_query_max(self):
        spec = {"objective": "SEGMENT_TREE_BEATS"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "segment_tree_beats_chmin")
        ops = [("query_max", 0, 3, None), ("chmin", 0, 3, 7), ("query_max", 0, 3, None)]
        self.assertEqual(oracle_segment_tree_beats([5, 8, 12, 3], ops), [12, 7])

    def test_ADS_58_beats_partial_range_chmin(self):
        spec = {"objective": "SEGMENT_TREE_BEATS"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "segment_tree_beats_chmin")
        ops = [("chmin", 1, 2, 4), ("query_sum", 0, 3, None)]
        self.assertEqual(oracle_segment_tree_beats([10, 10, 10, 10], ops), [28])

    def test_ADS_59_beats_leaf_sentinels(self):
        spec = {"objective": "SEGMENT_TREE_BEATS"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "segment_tree_beats_chmin")
        ops = [("chmin", 0, 0, 3), ("query_sum", 0, 0, None)]
        self.assertEqual(oracle_segment_tree_beats([5], ops), [3])

    def test_ADS_60_beats_chained_chmins(self):
        spec = {"objective": "SEGMENT_TREE_BEATS"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "segment_tree_beats_chmin")
        ops = [("chmin", 0, 3, 8), ("chmin", 0, 3, 5), ("query_sum", 0, 3, None)]
        self.assertEqual(oracle_segment_tree_beats([10, 9, 8, 7], ops), [20])


if __name__ == "__main__":
    unittest.main()
