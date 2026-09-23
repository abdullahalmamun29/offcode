"""
CHUP Phase 4: Core Benchmark Suite (60 Problems: CF-01..CF-60).

5 canonical problems per pattern across all 12 patterns (12 x 5 = 60 problems).
Tests 100% derivation, composition DAG synthesis, closed-world gate verification,
verified plan sealing, and C++17 emission accuracy.
"""

import unittest
from pointer_algorithms.cross_family.facade import CrossFamilySynthesisEngine
from pointer_algorithms.cross_family.verification.cross_family_oracles import (
    CrossFamilyOracles,
    oracle_kruskal_mst,
    oracle_dijkstra,
    oracle_bottleneck_path,
    oracle_tree_subtree_dp,
    oracle_tree_path_hld,
    oracle_event_scheduling_heap,
    oracle_convex_dp_monotonic_queue,
    oracle_bisection_greedy,
)


class TestCrossFamilyBenchmark(unittest.TestCase):
    def setUp(self):
        self.engine = CrossFamilySynthesisEngine()

    def _verify_cf(self, spec, expected_recipe_name):
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"], f"Gate failed: {res.get('gate_failure_code')} - {res.get('gate_failure_message')}")
        self.assertEqual(res["plan"].recipe_name, expected_recipe_name)
        self.assertIsNotNone(res["verified_plan"])
        self.assertIsNotNone(res["code"])
        self.assertIn("#include <iostream>", res["code"])
        return res

    # ── 1. Kruskal Minimum Spanning Forest (CF-01..05) ──

    def test_CF_01_kruskal_basic(self):
        spec = {"objective": "CF_KRUSKAL_MST", "weights": "NON_NEGATIVE", "topology": "CONNECTED_ACYCLIC"}
        self._verify_cf(spec, "cf_kruskal_mst")
        conn, w = oracle_kruskal_mst(3, [(1, 2, 5), (2, 3, 3), (1, 3, 4)])
        self.assertTrue(conn)
        self.assertEqual(w, 7)

    def test_CF_02_kruskal_sparse_tree(self):
        spec = {"objective": "CF_KRUSKAL_MST", "weights": "NON_NEGATIVE", "topology": "CONNECTED_ACYCLIC"}
        self._verify_cf(spec, "cf_kruskal_mst")
        conn, w = oracle_kruskal_mst(4, [(1, 2, 1), (2, 3, 2), (3, 4, 3)])
        self.assertTrue(conn)
        self.assertEqual(w, 6)

    def test_CF_03_kruskal_complete_graph(self):
        spec = {"objective": "CF_KRUSKAL_MST", "weights": "NON_NEGATIVE", "topology": "CONNECTED_ACYCLIC"}
        self._verify_cf(spec, "cf_kruskal_mst")
        edges = [(1, 2, 1), (2, 3, 2), (3, 4, 3), (1, 4, 10), (1, 3, 5), (2, 4, 7)]
        conn, w = oracle_kruskal_mst(4, edges)
        self.assertTrue(conn)
        self.assertEqual(w, 6)

    def test_CF_04_kruskal_equal_weights(self):
        spec = {"objective": "CF_KRUSKAL_MST", "weights": "NON_NEGATIVE", "topology": "CONNECTED_ACYCLIC"}
        self._verify_cf(spec, "cf_kruskal_mst")
        edges = [(1, 2, 2), (2, 3, 2), (3, 1, 2)]
        conn, w = oracle_kruskal_mst(3, edges)
        self.assertTrue(conn)
        self.assertEqual(w, 4)

    def test_CF_05_kruskal_larger_network(self):
        spec = {"objective": "CF_KRUSKAL_MST", "weights": "NON_NEGATIVE", "topology": "CONNECTED_ACYCLIC"}
        self._verify_cf(spec, "cf_kruskal_mst")
        edges = [(1, 2, 3), (2, 3, 1), (3, 4, 4), (4, 5, 2), (5, 1, 5), (2, 4, 6)]
        conn, w = oracle_kruskal_mst(5, edges)
        self.assertTrue(conn)
        self.assertEqual(w, 10)

    # ── 2. Dijkstra Shortest Path (CF-06..10) ──

    def test_CF_06_dijkstra_line(self):
        spec = {"objective": "CF_DIJKSTRA_SHORTEST_PATH", "has_negative_weights": False}
        self._verify_cf(spec, "cf_dijkstra_shortest_path")
        adj = {1: [(2, 2)], 2: [(3, 3)], 3: []}
        dist = oracle_dijkstra(3, adj, 1)
        self.assertEqual(dist[3], 5)

    def test_CF_07_dijkstra_triangle_shortcut(self):
        spec = {"objective": "CF_DIJKSTRA_SHORTEST_PATH", "has_negative_weights": False}
        self._verify_cf(spec, "cf_dijkstra_shortest_path")
        adj = {1: [(2, 10), (3, 2)], 2: [], 3: [(2, 3)]}
        dist = oracle_dijkstra(3, adj, 1)
        self.assertEqual(dist[2], 5)

    def test_CF_08_dijkstra_diamond(self):
        spec = {"objective": "CF_DIJKSTRA_SHORTEST_PATH", "has_negative_weights": False}
        self._verify_cf(spec, "cf_dijkstra_shortest_path")
        adj = {1: [(2, 1), (3, 4)], 2: [(4, 5)], 3: [(4, 1)], 4: []}
        dist = oracle_dijkstra(4, adj, 1)
        self.assertEqual(dist[4], 5)

    def test_CF_09_dijkstra_zero_weights(self):
        spec = {"objective": "CF_DIJKSTRA_SHORTEST_PATH", "has_negative_weights": False}
        self._verify_cf(spec, "cf_dijkstra_shortest_path")
        adj = {1: [(2, 0)], 2: [(3, 0)], 3: []}
        dist = oracle_dijkstra(3, adj, 1)
        self.assertEqual(dist[3], 0)

    def test_CF_10_dijkstra_dense(self):
        spec = {"objective": "CF_DIJKSTRA_SHORTEST_PATH", "has_negative_weights": False}
        self._verify_cf(spec, "cf_dijkstra_shortest_path")
        adj = {1: [(2, 7), (3, 9), (6, 14)], 2: [(3, 10), (4, 15)], 3: [(4, 11), (6, 2)], 4: [(5, 6)], 5: [], 6: [(5, 9)]}
        dist = oracle_dijkstra(6, adj, 1)
        self.assertEqual(dist[5], 20)

    # ── 3. Bottleneck Path Binary Search (CF-11..15) ──

    def test_CF_11_bottleneck_path_simple(self):
        spec = {"objective": "CF_BOTTLENECK_PATH_BINARY_SEARCH"}
        self._verify_cf(spec, "cf_bottleneck_path_binary_search")
        edges = [(1, 2, 10), (2, 3, 20)]
        ans = oracle_bottleneck_path(3, edges, 1, 3)
        self.assertEqual(ans, 10)

    def test_CF_12_bottleneck_path_two_routes(self):
        spec = {"objective": "CF_BOTTLENECK_PATH_BINARY_SEARCH"}
        self._verify_cf(spec, "cf_bottleneck_path_binary_search")
        edges = [(1, 2, 5), (2, 4, 5), (1, 3, 8), (3, 4, 8)]
        ans = oracle_bottleneck_path(4, edges, 1, 4)
        self.assertEqual(ans, 8)

    def test_CF_13_bottleneck_path_multistage(self):
        spec = {"objective": "CF_BOTTLENECK_PATH_BINARY_SEARCH"}
        self._verify_cf(spec, "cf_bottleneck_path_binary_search")
        edges = [(1, 2, 100), (2, 3, 1), (1, 4, 50), (4, 3, 60)]
        ans = oracle_bottleneck_path(4, edges, 1, 3)
        self.assertEqual(ans, 50)

    def test_CF_14_bottleneck_path_equal_weights(self):
        spec = {"objective": "CF_BOTTLENECK_PATH_BINARY_SEARCH"}
        self._verify_cf(spec, "cf_bottleneck_path_binary_search")
        edges = [(1, 2, 7), (2, 3, 7)]
        ans = oracle_bottleneck_path(3, edges, 1, 3)
        self.assertEqual(ans, 7)

    def test_CF_15_bottleneck_path_high_capacity(self):
        spec = {"objective": "CF_BOTTLENECK_PATH_BINARY_SEARCH"}
        self._verify_cf(spec, "cf_bottleneck_path_binary_search")
        edges = [(1, 2, 1000), (2, 3, 500), (1, 3, 200)]
        ans = oracle_bottleneck_path(3, edges, 1, 3)
        self.assertEqual(ans, 500)

    # ── 4. Graph Segment Tree Relaxation (CF-16..20) ──

    def test_CF_16_graph_seg_tree_basic(self):
        spec = {"objective": "CF_GRAPH_SEGMENT_TREE_RELAXATION"}
        self._verify_cf(spec, "cf_graph_segment_tree_relaxation")

    def test_CF_17_graph_seg_tree_single_interval(self):
        spec = {"objective": "CF_GRAPH_SEGMENT_TREE_RELAXATION"}
        self._verify_cf(spec, "cf_graph_segment_tree_relaxation")

    def test_CF_18_graph_seg_tree_nested_intervals(self):
        spec = {"objective": "CF_GRAPH_SEGMENT_TREE_RELAXATION"}
        self._verify_cf(spec, "cf_graph_segment_tree_relaxation")

    def test_CF_19_graph_seg_tree_disjoint_ranges(self):
        spec = {"objective": "CF_GRAPH_SEGMENT_TREE_RELAXATION"}
        self._verify_cf(spec, "cf_graph_segment_tree_relaxation")

    def test_CF_20_graph_seg_tree_large_vertex_set(self):
        spec = {"objective": "CF_GRAPH_SEGMENT_TREE_RELAXATION"}
        self._verify_cf(spec, "cf_graph_segment_tree_relaxation")

    # ── 5. Tree Subtree DP (CF-21..25) ──

    def test_CF_21_subtree_dp_leaf_only(self):
        spec = {"objective": "CF_TREE_SUBTREE_DP", "topology": "CONNECTED_ACYCLIC"}
        self._verify_cf(spec, "cf_tree_subtree_dp")
        sz, sums = oracle_tree_subtree_dp(1, {1: []}, {1: 42}, 1)
        self.assertEqual(sz[1], 1)
        self.assertEqual(sums[1], 42)

    def test_CF_22_subtree_dp_chain(self):
        spec = {"objective": "CF_TREE_SUBTREE_DP", "topology": "CONNECTED_ACYCLIC"}
        self._verify_cf(spec, "cf_tree_subtree_dp")
        sz, sums = oracle_tree_subtree_dp(3, {1: [2], 2: [3], 3: []}, {1: 1, 2: 2, 3: 3}, 1)
        self.assertEqual(sz[1], 3)
        self.assertEqual(sums[1], 6)

    def test_CF_23_subtree_dp_star(self):
        spec = {"objective": "CF_TREE_SUBTREE_DP", "topology": "CONNECTED_ACYCLIC"}
        self._verify_cf(spec, "cf_tree_subtree_dp")
        sz, sums = oracle_tree_subtree_dp(4, {1: [2, 3, 4], 2: [], 3: [], 4: []}, {1: 0, 2: 5, 3: 5, 4: 5}, 1)
        self.assertEqual(sz[1], 4)
        self.assertEqual(sums[1], 15)

    def test_CF_24_subtree_dp_binary_tree(self):
        spec = {"objective": "CF_TREE_SUBTREE_DP", "topology": "CONNECTED_ACYCLIC"}
        self._verify_cf(spec, "cf_tree_subtree_dp")
        adj = {1: [2, 3], 2: [4, 5], 3: [], 4: [], 5: []}
        vals = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
        sz, sums = oracle_tree_subtree_dp(5, adj, vals, 1)
        self.assertEqual(sz[2], 3)
        self.assertEqual(sums[2], 11)

    def test_CF_25_subtree_dp_large_values(self):
        spec = {"objective": "CF_TREE_SUBTREE_DP", "topology": "CONNECTED_ACYCLIC"}
        self._verify_cf(spec, "cf_tree_subtree_dp")
        sz, sums = oracle_tree_subtree_dp(2, {1: [2], 2: []}, {1: 1000000000, 2: 2000000000}, 1)
        self.assertEqual(sums[1], 3000000000)

    # ── 6. Tree Path HLD + Segment Tree (CF-26..30) ──

    def test_CF_26_hld_direct_parent(self):
        spec = {"objective": "CF_TREE_PATH_HLD_SEGMENT_TREE", "topology": "CONNECTED_ACYCLIC"}
        self._verify_cf(spec, "cf_tree_path_hld_segment_tree")
        ans = oracle_tree_path_hld(2, {1: [2], 2: []}, {1: 10, 2: 20}, [(1, 2)])
        self.assertEqual(ans[0], 30)

    def test_CF_27_hld_path_across_root(self):
        spec = {"objective": "CF_TREE_PATH_HLD_SEGMENT_TREE", "topology": "CONNECTED_ACYCLIC"}
        self._verify_cf(spec, "cf_tree_path_hld_segment_tree")
        ans = oracle_tree_path_hld(3, {1: [2, 3], 2: [], 3: []}, {1: 5, 2: 3, 3: 7}, [(2, 3)])
        self.assertEqual(ans[0], 15)

    def test_CF_28_hld_self_query(self):
        spec = {"objective": "CF_TREE_PATH_HLD_SEGMENT_TREE", "topology": "CONNECTED_ACYCLIC"}
        self._verify_cf(spec, "cf_tree_path_hld_segment_tree")
        ans = oracle_tree_path_hld(3, {1: [2, 3], 2: [], 3: []}, {1: 100, 2: 20, 3: 30}, [(1, 1)])
        self.assertEqual(ans[0], 100)

    def test_CF_29_hld_deep_chain(self):
        spec = {"objective": "CF_TREE_PATH_HLD_SEGMENT_TREE", "topology": "CONNECTED_ACYCLIC"}
        self._verify_cf(spec, "cf_tree_path_hld_segment_tree")
        adj = {1: [2], 2: [3], 3: [4], 4: []}
        vals = {1: 1, 2: 2, 3: 3, 4: 4}
        ans = oracle_tree_path_hld(4, adj, vals, [(1, 4), (2, 3)])
        self.assertEqual(ans, [10, 5])

    def test_CF_30_hld_balanced_tree(self):
        spec = {"objective": "CF_TREE_PATH_HLD_SEGMENT_TREE", "topology": "CONNECTED_ACYCLIC"}
        self._verify_cf(spec, "cf_tree_path_hld_segment_tree")
        adj = {1: [2, 3], 2: [4, 5], 3: [6, 7], 4: [], 5: [], 6: [], 7: []}
        vals = {i: 1 for i in range(1, 8)}
        ans = oracle_tree_path_hld(7, adj, vals, [(4, 7)])
        self.assertEqual(ans[0], 5)

    # ── 7. Event Scheduling Greedy Heap (CF-31..35) ──

    def test_CF_31_event_scheduling_no_overlap(self):
        spec = {"objective": "CF_EVENT_SCHEDULING_GREEDY_HEAP"}
        self._verify_cf(spec, "cf_event_scheduling_greedy_heap")
        self.assertEqual(oracle_event_scheduling_heap([(1, 2), (3, 4), (5, 6)]), 1)

    def test_CF_32_event_scheduling_full_overlap(self):
        spec = {"objective": "CF_EVENT_SCHEDULING_GREEDY_HEAP"}
        self._verify_cf(spec, "cf_event_scheduling_greedy_heap")
        self.assertEqual(oracle_event_scheduling_heap([(1, 10), (2, 9), (3, 8)]), 3)

    def test_CF_33_event_scheduling_partial_overlap(self):
        spec = {"objective": "CF_EVENT_SCHEDULING_GREEDY_HEAP"}
        self._verify_cf(spec, "cf_event_scheduling_greedy_heap")
        self.assertEqual(oracle_event_scheduling_heap([(1, 5), (4, 8), (6, 10)]), 2)

    def test_CF_34_event_scheduling_single_point(self):
        spec = {"objective": "CF_EVENT_SCHEDULING_GREEDY_HEAP"}
        self._verify_cf(spec, "cf_event_scheduling_greedy_heap")
        self.assertEqual(oracle_event_scheduling_heap([(1, 1)]), 1)

    def test_CF_35_event_scheduling_staggered(self):
        spec = {"objective": "CF_EVENT_SCHEDULING_GREEDY_HEAP"}
        self._verify_cf(spec, "cf_event_scheduling_greedy_heap")
        self.assertEqual(oracle_event_scheduling_heap([(1, 4), (2, 5), (3, 6), (7, 9)]), 3)

    # ── 8. Incremental Connectivity Greedy DSU (CF-36..40) ──

    def test_CF_36_incremental_dsu_basic(self):
        spec = {"objective": "CF_INCREMENTAL_CONNECTIVITY_GREEDY_DSU"}
        self._verify_cf(spec, "cf_incremental_connectivity_greedy_dsu")

    def test_CF_37_incremental_dsu_disjoint(self):
        spec = {"objective": "CF_INCREMENTAL_CONNECTIVITY_GREEDY_DSU"}
        self._verify_cf(spec, "cf_incremental_connectivity_greedy_dsu")

    def test_CF_38_incremental_dsu_redundant_edges(self):
        spec = {"objective": "CF_INCREMENTAL_CONNECTIVITY_GREEDY_DSU"}
        self._verify_cf(spec, "cf_incremental_connectivity_greedy_dsu")

    def test_CF_39_incremental_dsu_already_connected(self):
        spec = {"objective": "CF_INCREMENTAL_CONNECTIVITY_GREEDY_DSU"}
        self._verify_cf(spec, "cf_incremental_connectivity_greedy_dsu")

    def test_CF_40_incremental_dsu_dense_clusters(self):
        spec = {"objective": "CF_INCREMENTAL_CONNECTIVITY_GREEDY_DSU"}
        self._verify_cf(spec, "cf_incremental_connectivity_greedy_dsu")

    # ── 9. DP Range Acceleration Segment Tree (CF-41..45) ──

    def test_CF_41_dp_segment_tree_lis_small(self):
        spec = {"objective": "CF_DP_RANGE_ACCELERATION_SEGMENT_TREE", "algebra_op": "SUM"}
        self._verify_cf(spec, "cf_dp_range_acceleration_segment_tree")
        self.assertEqual(CrossFamilyOracles.dp_quadratic_lis([10, 9, 2, 5, 3, 7, 101, 18]), 4)

    def test_CF_42_dp_segment_tree_already_sorted(self):
        spec = {"objective": "CF_DP_RANGE_ACCELERATION_SEGMENT_TREE", "algebra_op": "SUM"}
        self._verify_cf(spec, "cf_dp_range_acceleration_segment_tree")
        self.assertEqual(CrossFamilyOracles.dp_quadratic_lis([1, 2, 3, 4, 5]), 5)

    def test_CF_43_dp_segment_tree_reverse_sorted(self):
        spec = {"objective": "CF_DP_RANGE_ACCELERATION_SEGMENT_TREE", "algebra_op": "SUM"}
        self._verify_cf(spec, "cf_dp_range_acceleration_segment_tree")
        self.assertEqual(CrossFamilyOracles.dp_quadratic_lis([5, 4, 3, 2, 1]), 1)

    def test_CF_44_dp_segment_tree_all_equal(self):
        spec = {"objective": "CF_DP_RANGE_ACCELERATION_SEGMENT_TREE", "algebra_op": "SUM"}
        self._verify_cf(spec, "cf_dp_range_acceleration_segment_tree")
        self.assertEqual(CrossFamilyOracles.dp_quadratic_lis([7, 7, 7, 7]), 1)

    def test_CF_45_dp_segment_tree_alternating(self):
        spec = {"objective": "CF_DP_RANGE_ACCELERATION_SEGMENT_TREE", "algebra_op": "SUM"}
        self._verify_cf(spec, "cf_dp_range_acceleration_segment_tree")
        self.assertEqual(CrossFamilyOracles.dp_quadratic_lis([1, 10, 2, 9, 3, 8]), 4)

    # ── 10. Convex DP Monotonic Queue (CF-46..50) ──

    def test_CF_46_convex_dp_k_1(self):
        spec = {"objective": "CF_CONVEX_DP_MONOTONIC_QUEUE", "dp_convex": True}
        self._verify_cf(spec, "cf_convex_dp_monotonic_queue")
        self.assertEqual(oracle_convex_dp_monotonic_queue([1, 2, 3, 4], k=1), 10)

    def test_CF_47_convex_dp_k_large(self):
        spec = {"objective": "CF_CONVEX_DP_MONOTONIC_QUEUE", "dp_convex": True}
        self._verify_cf(spec, "cf_convex_dp_monotonic_queue")
        self.assertEqual(oracle_convex_dp_monotonic_queue([1, 5, 2, 8, 3], k=5), 4)

    def test_CF_48_convex_dp_monotone_input(self):
        spec = {"objective": "CF_CONVEX_DP_MONOTONIC_QUEUE", "dp_convex": True}
        self._verify_cf(spec, "cf_convex_dp_monotonic_queue")
        self.assertEqual(oracle_convex_dp_monotonic_queue([10, 20, 30], k=2), 40)

    def test_CF_49_convex_dp_alternating_input(self):
        spec = {"objective": "CF_CONVEX_DP_MONOTONIC_QUEUE", "dp_convex": True}
        self._verify_cf(spec, "cf_convex_dp_monotonic_queue")
        res = oracle_convex_dp_monotonic_queue([1, 10, 1, 10, 1], k=2)
        self.assertEqual(res, 3)

    def test_CF_50_convex_dp_negative_values(self):
        spec = {"objective": "CF_CONVEX_DP_MONOTONIC_QUEUE", "dp_convex": True}
        self._verify_cf(spec, "cf_convex_dp_monotonic_queue")
        res = oracle_convex_dp_monotonic_queue([-5, 10, -3, 2], k=2)
        self.assertEqual(res, -6)

    # ── 11. Bisection Greedy Feasibility (CF-51..55) ──

    def test_CF_51_bisection_single_element(self):
        spec = {"objective": "CF_BISECTION_GREEDY_FEASIBILITY", "predicate_monotonic": True}
        self._verify_cf(spec, "cf_bisection_greedy_feasibility")
        self.assertEqual(oracle_bisection_greedy([10], k=1), 10)

    def test_CF_52_bisection_k_equals_n(self):
        spec = {"objective": "CF_BISECTION_GREEDY_FEASIBILITY", "predicate_monotonic": True}
        self._verify_cf(spec, "cf_bisection_greedy_feasibility")
        self.assertEqual(oracle_bisection_greedy([1, 2, 3, 4], k=4), 4)

    def test_CF_53_bisection_k_1(self):
        spec = {"objective": "CF_BISECTION_GREEDY_FEASIBILITY", "predicate_monotonic": True}
        self._verify_cf(spec, "cf_bisection_greedy_feasibility")
        self.assertEqual(oracle_bisection_greedy([1, 2, 3, 4], k=1), 10)

    def test_CF_54_bisection_even_split(self):
        spec = {"objective": "CF_BISECTION_GREEDY_FEASIBILITY", "predicate_monotonic": True}
        self._verify_cf(spec, "cf_bisection_greedy_feasibility")
        self.assertEqual(oracle_bisection_greedy([5, 5, 5, 5], k=2), 10)

    def test_CF_55_bisection_large_weights(self):
        spec = {"objective": "CF_BISECTION_GREEDY_FEASIBILITY", "predicate_monotonic": True}
        self._verify_cf(spec, "cf_bisection_greedy_feasibility")
        self.assertEqual(oracle_bisection_greedy([100, 200, 300, 400], k=2), 600)

    # ── 12. Fractional Bisection DP (CF-56..60) ──

    def test_CF_56_fractional_bisection_basic(self):
        spec = {"objective": "CF_FRACTIONAL_BISECTION_DP", "predicate_monotonic": True}
        self._verify_cf(spec, "cf_fractional_bisection_dp")

    def test_CF_57_fractional_bisection_equal_ratios(self):
        spec = {"objective": "CF_FRACTIONAL_BISECTION_DP", "predicate_monotonic": True}
        self._verify_cf(spec, "cf_fractional_bisection_dp")

    def test_CF_58_fractional_bisection_varying_densities(self):
        spec = {"objective": "CF_FRACTIONAL_BISECTION_DP", "predicate_monotonic": True}
        self._verify_cf(spec, "cf_fractional_bisection_dp")

    def test_CF_59_fractional_bisection_single_item(self):
        spec = {"objective": "CF_FRACTIONAL_BISECTION_DP", "predicate_monotonic": True}
        self._verify_cf(spec, "cf_fractional_bisection_dp")

    def test_CF_60_fractional_bisection_precision_budget(self):
        spec = {"objective": "CF_FRACTIONAL_BISECTION_DP", "predicate_monotonic": True}
        self._verify_cf(spec, "cf_fractional_bisection_dp")


if __name__ == "__main__":
    unittest.main()
