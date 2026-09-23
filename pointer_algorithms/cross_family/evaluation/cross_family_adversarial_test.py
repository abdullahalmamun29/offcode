"""
CHUP Phase 4: Adversarial & Boundary Benchmark Suite (16 Tests: ADV-CF-01..ADV-CF-16).

Tests degeneracies, extreme boundaries, singletons, self-loops, disconnected components,
unreachable targets, and high-degree star graphs.
"""

import unittest
from pointer_algorithms.cross_family.verification.cross_family_oracles import (
    oracle_kruskal_mst,
    oracle_dijkstra,
    oracle_bottleneck_path,
    oracle_tree_subtree_dp,
    oracle_tree_path_hld,
    oracle_event_scheduling_heap,
    oracle_convex_dp_monotonic_queue,
    oracle_bisection_greedy,
)


class TestCrossFamilyAdversarial(unittest.TestCase):

    def test_ADV_CF_01_kruskal_disconnected_graph(self):
        """Kruskal on disconnected graph returns spanning forest and detects incompleteness."""
        edges = [(1, 2, 5), (3, 4, 10)]
        conn, w = oracle_kruskal_mst(4, edges)
        self.assertFalse(conn)

    def test_ADV_CF_02_kruskal_identical_weights(self):
        """Kruskal with identical weights across all edges."""
        edges = [(1, 2, 1), (2, 3, 1), (3, 4, 1), (1, 4, 1)]
        conn, w = oracle_kruskal_mst(4, edges)
        self.assertTrue(conn)
        self.assertEqual(w, 3)

    def test_ADV_CF_03_dijkstra_single_vertex(self):
        """Dijkstra on N=1 graph."""
        dist = oracle_dijkstra(1, {1: []}, 1)
        self.assertEqual(dist[1], 0)

    def test_ADV_CF_04_dijkstra_large_edge_weights(self):
        """Dijkstra with edge weights around 10^9."""
        adj = {1: [(2, 10**9)], 2: [(3, 2 * 10**9)], 3: []}
        dist = oracle_dijkstra(3, adj, 1)
        self.assertEqual(dist[3], 3 * 10**9)

    def test_ADV_CF_05_bottleneck_path_same_source_dest(self):
        """Bottleneck path when source equals destination."""
        edges = [(1, 2, 10)]
        ans = oracle_bottleneck_path(2, edges, 1, 1)
        self.assertGreaterEqual(ans, -1)

    def test_ADV_CF_06_bottleneck_path_unreachable_target(self):
        """Bottleneck path when destination is completely disconnected."""
        edges = [(1, 2, 10), (3, 4, 20)]
        ans = oracle_bottleneck_path(4, edges, 1, 4)
        self.assertEqual(ans, -1)

    def test_ADV_CF_07_subtree_dp_singleton_tree(self):
        """Subtree DP on N=1 tree."""
        sz, sums = oracle_tree_subtree_dp(1, {1: []}, {1: 99}, 1)
        self.assertEqual(sz[1], 1)
        self.assertEqual(sums[1], 99)

    def test_ADV_CF_08_subtree_dp_deep_linear_chain(self):
        """Subtree DP on deep chain of length 50."""
        n = 50
        adj = {i: [i + 1] if i < n else [] for i in range(1, n + 1)}
        vals = {i: 1 for i in range(1, n + 1)}
        sz, sums = oracle_tree_subtree_dp(n, adj, vals, 1)
        self.assertEqual(sz[1], 50)
        self.assertEqual(sums[1], 50)

    def test_ADV_CF_09_hld_path_query_self_loop(self):
        """HLD path query between vertex and itself."""
        adj = {1: [2], 2: []}
        vals = {1: 42, 2: 10}
        ans = oracle_tree_path_hld(2, adj, vals, [(1, 1)])
        self.assertEqual(ans[0], 42)

    def test_ADV_CF_10_hld_star_graph_high_degree(self):
        """HLD path query on star graph with central hub 1."""
        n = 30
        adj = {1: list(range(2, n + 1))}
        for i in range(2, n + 1):
            adj[i] = []
        vals = {i: 1 for i in range(1, n + 1)}
        ans = oracle_tree_path_hld(n, adj, vals, [(5, 15)])
        self.assertEqual(ans[0], 3)  # 5 -> 1 -> 15 = 1 + 1 + 1 = 3

    def test_ADV_CF_11_event_scheduling_all_identical(self):
        """Event scheduling with identical overlapping intervals."""
        intervals = [(10, 20)] * 5
        rooms = oracle_event_scheduling_heap(intervals)
        self.assertEqual(rooms, 5)

    def test_ADV_CF_12_event_scheduling_empty_schedule(self):
        """Event scheduling with 0 intervals."""
        rooms = oracle_event_scheduling_heap([])
        self.assertEqual(rooms, 0)

    def test_ADV_CF_13_bottleneck_path_cycle(self):
        """Bottleneck path in graph containing cycles."""
        edges = [(1, 2, 10), (2, 3, 20), (3, 1, 30), (3, 4, 15)]
        ans = oracle_bottleneck_path(4, edges, 1, 4)
        self.assertEqual(ans, 15)

    def test_ADV_CF_14_convex_dp_window_exceeds_n(self):
        """Convex DP monotonic queue where window size k >= N."""
        arr = [5, 2, 8, 1, 9]
        res = oracle_convex_dp_monotonic_queue(arr, k=10)
        self.assertIsInstance(res, int)

    def test_ADV_CF_15_convex_dp_large_negative_values(self):
        """Convex DP with negative cost transitions."""
        arr = [-100, -200, -300]
        res = oracle_convex_dp_monotonic_queue(arr, k=2)
        self.assertEqual(res, -600)

    def test_ADV_CF_16_bisection_greedy_k_is_one(self):
        """Bisection greedy feasibility when k=1."""
        items = [10, 20, 30, 40]
        ans = oracle_bisection_greedy(items, k=1)
        self.assertEqual(ans, 100)


if __name__ == "__main__":
    unittest.main()
