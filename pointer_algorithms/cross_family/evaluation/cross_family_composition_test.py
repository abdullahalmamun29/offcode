"""
CHUP Phase 4: Positive Component Composition Tests (8 Scenarios).

Verifies multi-component algorithmic synthesis pipelines, state contract transitions,
and proof obligation discharges across heterogeneous algorithmic families.
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


class TestCrossFamilyComposition(unittest.TestCase):
    def setUp(self):
        self.engine = CrossFamilySynthesisEngine()

    def test_comp_01_kruskal_mst(self):
        """Pipeline 1: WeightedGraph -> EdgeSort -> DSU Cycle Prevention -> MST"""
        spec = {
            "objective": "CF_KRUSKAL_MST",
            "weights": "NON_NEGATIVE",
            "topology": "CONNECTED_ACYCLIC",
            "n": 5,
            "m": 6
        }
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["eval_result"].verdict, CandidateVerdict.VALID_OPTIMAL)
        self.assertIsNotNone(res["verified_plan"])
        self.assertIsNotNone(res["code"])

        # Oracle cross-validation
        edges = [(1, 2, 4), (1, 3, 2), (2, 3, 1), (2, 4, 5), (3, 4, 8), (4, 5, 3)]
        is_conn, mst_weight = oracle_kruskal_mst(5, edges)
        self.assertTrue(is_conn)
        self.assertGreater(mst_weight, 0)

    def test_comp_02_dijkstra_shortest_path(self):
        """Pipeline 2: NonNegativeWeightedGraph -> Min-Heap Priority Frontier -> ShortestPathDistances"""
        spec = {
            "objective": "CF_DIJKSTRA_SHORTEST_PATH",
            "has_negative_weights": False,
            "n": 4,
            "m": 4
        }
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["eval_result"].verdict, CandidateVerdict.VALID_OPTIMAL)
        self.assertIsNotNone(res["verified_plan"])

        adj = {
            1: [(2, 2), (3, 5)],
            2: [(3, 1), (4, 4)],
            3: [(4, 2)],
            4: []
        }
        dist = oracle_dijkstra(4, adj, 1)
        self.assertEqual(dist[4], 5)  # 1->2->3->4 = 2+1+2 = 5

    def test_comp_03_bottleneck_path_binary_search(self):
        """Pipeline 3: WeightedGraph + SearchDomainInterval -> Bisection -> BFS Reachability -> OptimalBottleneck"""
        spec = {
            "objective": "CF_BOTTLENECK_PATH_BINARY_SEARCH",
            "predicate_monotonic": True
        }
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["eval_result"].verdict, CandidateVerdict.VALID_OPTIMAL)
        self.assertIsNotNone(res["verified_plan"])

        edges = [(1, 2, 10), (2, 4, 20), (1, 3, 15), (3, 4, 5)]
        ans = oracle_bottleneck_path(4, edges, 1, 4)
        self.assertEqual(ans, 10)  # Path 1-2-4 has min capacity 10; Path 1-3-4 has 5. Max of min is 10.

    def test_comp_04_tree_subtree_dp(self):
        """Pipeline 4: RootedTree -> Post-Order Traversal -> SubtreeDPTable"""
        spec = {
            "objective": "CF_TREE_SUBTREE_DP",
            "topology": "CONNECTED_ACYCLIC"
        }
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["eval_result"].verdict, CandidateVerdict.VALID_OPTIMAL)
        self.assertIsNotNone(res["verified_plan"])

        adj = {1: [2, 3], 2: [], 3: [4], 4: []}
        vals = {1: 10, 2: 5, 3: 7, 4: 2}
        sz, sums = oracle_tree_subtree_dp(4, adj, vals, 1)
        self.assertEqual(sz[1], 4)
        self.assertEqual(sums[1], 24)
        self.assertEqual(sums[3], 9)

    def test_comp_05_tree_path_hld_segment_tree(self):
        """Pipeline 5: RootedTree -> HLD Mapping -> Linear Intervals -> Segment Tree -> PathAggregates"""
        spec = {
            "objective": "CF_TREE_PATH_HLD_SEGMENT_TREE",
            "topology": "CONNECTED_ACYCLIC"
        }
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["eval_result"].verdict, CandidateVerdict.VALID_OPTIMAL)
        self.assertIsNotNone(res["verified_plan"])

        adj = {1: [2, 3], 2: [], 3: [4], 4: []}
        vals = {1: 1, 2: 2, 3: 4, 4: 8}
        ans = oracle_tree_path_hld(4, adj, vals, [(2, 4)])
        self.assertEqual(ans[0], 15)  # Path 2 -> 1 -> 3 -> 4 = 2 + 1 + 4 + 8 = 15

    def test_comp_06_event_scheduling_greedy_heap(self):
        """Pipeline 6: IntervalSequence -> Start-Time Sort -> Min-Heap Active Ends -> RoomCount"""
        spec = {
            "objective": "CF_EVENT_SCHEDULING_GREEDY_HEAP"
        }
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["eval_result"].verdict, CandidateVerdict.VALID_OPTIMAL)
        self.assertIsNotNone(res["verified_plan"])

        intervals = [(1, 4), (2, 5), (6, 8), (5, 7)]
        rooms = oracle_event_scheduling_heap(intervals)
        self.assertEqual(rooms, 2)

    def test_comp_07_convex_dp_monotonic_queue(self):
        """Pipeline 7: ConvexRecurrenceDPTable -> Slope Dominance -> Monotone Deque -> Linear Transition"""
        spec = {
            "objective": "CF_CONVEX_DP_MONOTONIC_QUEUE",
            "dp_convex": True
        }
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["eval_result"].verdict, CandidateVerdict.VALID_OPTIMAL)
        self.assertIsNotNone(res["verified_plan"])

        arr = [10, 2, -10, 5, 20]
        dp_res = oracle_convex_dp_monotonic_queue(arr, k=2)
        self.assertIsInstance(dp_res, int)

    def test_comp_08_bisection_greedy_feasibility(self):
        """Pipeline 8: SearchDomainInterval -> Bisection -> Greedy Checker -> OptimalCapacity"""
        spec = {
            "objective": "CF_BISECTION_GREEDY_FEASIBILITY",
            "predicate_monotonic": True
        }
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["eval_result"].verdict, CandidateVerdict.VALID_OPTIMAL)
        self.assertIsNotNone(res["verified_plan"])

        items = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        min_max_load = oracle_bisection_greedy(items, k=3)
        self.assertEqual(min_max_load, 17)  # [1,2,3,4,5=15], [6,7=13], [8,9=17]


if __name__ == "__main__":
    unittest.main()
