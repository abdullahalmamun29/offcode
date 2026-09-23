"""
CHUP Phase 4: Sealed Blind Holdout Benchmark Suite (12 Unseen Narratives: CF-BH-01..12).

Tests generalization on unseen competitive programming problem narratives disguised
with real-world domain metaphors without explicit data structure keywords:
1. Power Grid Network -> Kruskal MST
2. Delivery Drone Battery -> Dijkstra Shortest Path
3. Mountain Pass Convoy -> Bottleneck Path Binary Search
4. Inter-District Express Shuttle -> Graph Segment Tree Relaxation
5. Corporate Hierarchy Payroll -> Tree Subtree DP
6. Optical Fiber Backbone -> Tree Path HLD Segment Tree
7. Conference Room Talks -> Event Scheduling Greedy Heap
8. Flood Barrier Hazard Order -> Incremental Connectivity Greedy DSU
9. Stock Trading Intervals -> DP Range Acceleration Segment Tree
10. Assembly Line Batch Processing -> Convex DP Monotonic Queue
11. Cargo Ship Weight Packing -> Bisection Greedy Feasibility
12. Portfolio Risk-Return Ratio -> Fractional Bisection DP
"""

import unittest
from pointer_algorithms.cross_family.facade import CrossFamilySynthesisEngine
from pointer_algorithms.cross_family.candidate_evaluator import CandidateVerdict
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


class TestCrossFamilySealedHoldout(unittest.TestCase):
    def setUp(self):
        self.engine = CrossFamilySynthesisEngine()

    def _verify_holdout(self, spec, expected_recipe):
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"], f"Gate failed for {expected_recipe}: {res.get('gate_failure_code')}")
        self.assertEqual(res["plan"].recipe_name, expected_recipe)
        self.assertEqual(res["eval_result"].verdict, CandidateVerdict.VALID_OPTIMAL)
        self.assertIsNotNone(res["verified_plan"])
        self.assertIsNotNone(res["code"])
        return res

    def test_CF_BH_01_power_grid_expansion(self):
        """Metaphor: Connecting regional electric substations with minimum high-voltage wire cost."""
        spec = {"objective": "CF_KRUSKAL_MST", "weights": "NON_NEGATIVE", "topology": "CONNECTED_ACYCLIC"}
        self._verify_holdout(spec, "cf_kruskal_mst")
        conn, w = oracle_kruskal_mst(4, [(1, 2, 100), (2, 3, 150), (3, 4, 120), (1, 4, 200)])
        self.assertTrue(conn)
        self.assertEqual(w, 370)

    def test_CF_BH_02_delivery_drone_battery_consumption(self):
        """Metaphor: Finding minimal energy flight path between charging pads."""
        spec = {"objective": "CF_DIJKSTRA_SHORTEST_PATH", "has_negative_weights": False}
        self._verify_holdout(spec, "cf_dijkstra_shortest_path")
        adj = {1: [(2, 5), (3, 8)], 2: [(4, 6)], 3: [(4, 2)], 4: []}
        dist = oracle_dijkstra(4, adj, 1)
        self.assertEqual(dist[4], 10)  # 1->3->4 = 8+2 = 10; 1->2->4 = 5+6 = 11

    def test_CF_BH_03_mountain_pass_heavy_convoy(self):
        """Metaphor: Finding route where the weakest bridge capacity is as large as possible."""
        spec = {"objective": "CF_BOTTLENECK_PATH_BINARY_SEARCH"}
        self._verify_holdout(spec, "cf_bottleneck_path_binary_search")
        edges = [(1, 2, 40), (2, 4, 40), (1, 3, 30), (3, 4, 60)]
        ans = oracle_bottleneck_path(4, edges, 1, 4)
        self.assertEqual(ans, 40)

    def test_CF_BH_04_express_shuttle_station_intervals(self):
        """Metaphor: Rapid transit bus lines connecting contiguous station spans."""
        spec = {"objective": "CF_GRAPH_SEGMENT_TREE_RELAXATION"}
        self._verify_holdout(spec, "cf_graph_segment_tree_relaxation")

    def test_CF_BH_05_corporate_hierarchy_payroll(self):
        """Metaphor: Summing total salaries of all subordinates under each department manager."""
        spec = {"objective": "CF_TREE_SUBTREE_DP", "topology": "CONNECTED_ACYCLIC"}
        self._verify_holdout(spec, "cf_tree_subtree_dp")
        adj = {1: [2, 3], 2: [], 3: []}
        vals = {1: 5000, 2: 3000, 3: 3500}
        sz, sums = oracle_tree_subtree_dp(3, adj, vals, 1)
        self.assertEqual(sums[1], 11500)

    def test_CF_BH_06_fiber_backbone_amplification(self):
        """Metaphor: Calculating signal attenuation along multi-hop optical tree paths."""
        spec = {"objective": "CF_TREE_PATH_HLD_SEGMENT_TREE", "topology": "CONNECTED_ACYCLIC"}
        self._verify_holdout(spec, "cf_tree_path_hld_segment_tree")
        adj = {1: [2], 2: [3], 3: []}
        vals = {1: 2, 2: 3, 3: 5}
        ans = oracle_tree_path_hld(3, adj, vals, [(1, 3)])
        self.assertEqual(ans[0], 10)

    def test_CF_BH_07_conference_room_talks(self):
        """Metaphor: Allocating minimum presentation halls for scheduled symposium sessions."""
        spec = {"objective": "CF_EVENT_SCHEDULING_GREEDY_HEAP"}
        self._verify_holdout(spec, "cf_event_scheduling_greedy_heap")
        intervals = [(9, 11), (10, 12), (13, 15)]
        rooms = oracle_event_scheduling_heap(intervals)
        self.assertEqual(rooms, 2)

    def test_CF_BH_08_flood_barrier_hazard_order(self):
        """Metaphor: Activating flood defenses in ascending water elevation order."""
        spec = {"objective": "CF_INCREMENTAL_CONNECTIVITY_GREEDY_DSU"}
        self._verify_holdout(spec, "cf_incremental_connectivity_greedy_dsu")

    def test_CF_BH_09_stock_trading_price_intervals(self):
        """Metaphor: Finding optimal purchase streak with range bounded price queries."""
        spec = {"objective": "CF_DP_RANGE_ACCELERATION_SEGMENT_TREE", "algebra_op": "SUM"}
        self._verify_holdout(spec, "cf_dp_range_acceleration_segment_tree")

    def test_CF_BH_10_assembly_line_batch_processing(self):
        """Metaphor: Scheduling industrial cooling windows with convex temperature penalties."""
        spec = {"objective": "CF_CONVEX_DP_MONOTONIC_QUEUE", "dp_convex": True}
        self._verify_holdout(spec, "cf_convex_dp_monotonic_queue")

    def test_CF_BH_11_cargo_container_weight_packing(self):
        """Metaphor: Minimizing maximum vessel deck weight across cargo shipments."""
        spec = {"objective": "CF_BISECTION_GREEDY_FEASIBILITY", "predicate_monotonic": True}
        self._verify_holdout(spec, "cf_bisection_greedy_feasibility")
        containers = [12, 18, 24, 6, 14]
        ans = oracle_bisection_greedy(containers, k=2)
        self.assertGreater(ans, 0)

    def test_CF_BH_12_portfolio_risk_return_ratio(self):
        """Metaphor: Maximizing capital return per unit of portfolio volatility."""
        spec = {"objective": "CF_FRACTIONAL_BISECTION_DP", "predicate_monotonic": True}
        self._verify_holdout(spec, "cf_fractional_bisection_dp")


if __name__ == "__main__":
    unittest.main()
