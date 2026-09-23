"""
CHUP Phase 4: Discrimination Holdout Benchmark Suite (12 Tests: CFD-01..CFD-12).

Verifies strict mathematical and structural boundary discrimination:
ensures cross-family multi-component pipelines are selected when preconditions hold,
and strictly fail closed with precise diagnostic failure codes when violated.
"""

import unittest
from pointer_algorithms.cross_family.facade import CrossFamilySynthesisEngine
from pointer_algorithms.cross_family.candidate_evaluator import CandidateVerdict


class TestCrossFamilyDiscriminationHoldout(unittest.TestCase):
    def setUp(self):
        self.engine = CrossFamilySynthesisEngine()

    def test_CFD_01_kruskal_selects_mst_pipeline(self):
        """Valid undirected weighted graph selects Kruskal MST composition."""
        spec = {"objective": "CF_KRUSKAL_MST", "weights": "NON_NEGATIVE", "topology": "CONNECTED_ACYCLIC"}
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["plan"].recipe_name, "cf_kruskal_mst")
        self.assertEqual(res["eval_result"].verdict, CandidateVerdict.VALID_OPTIMAL)

    def test_CFD_02_negative_weights_rejects_dijkstra(self):
        """Graph with negative edges strictly rejects Dijkstra greedy frontier."""
        spec = {"objective": "CF_DIJKSTRA_SHORTEST_PATH", "has_negative_weights": True}
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "NEGATIVE_EDGE_WEIGHTS_REJECT_GREEDY_HEAP")
        self.assertEqual(res["eval_result"].verdict, CandidateVerdict.INVALID_PRECONDITION)

    def test_CFD_03_cyclic_graph_rejects_tree_dp(self):
        """Cyclic topology strictly rejects Tree Subtree DP (Gate A)."""
        spec = {"objective": "CF_TREE_SUBTREE_DP", "is_cyclic": True, "topology": "CYCLIC"}
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "REQUIRED_ACYCLICITY_VIOLATED")
        self.assertEqual(res["eval_result"].verdict, CandidateVerdict.INVALID_PRECONDITION)

    def test_CFD_04_disconnected_graph_rejects_tree_dp(self):
        """Disconnected topology strictly rejects single-tree Subtree DP."""
        spec = {"objective": "CF_TREE_SUBTREE_DP", "is_disconnected": True, "topology": "DISCONNECTED"}
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "REQUIRED_CONNECTIVITY_VIOLATED")

    def test_CFD_05_non_monotonic_predicate_rejects_bisection(self):
        """Oscillating decision predicate strictly rejects answer bisection."""
        spec = {"objective": "CF_BISECTION_GREEDY_FEASIBILITY", "predicate_monotonic": False}
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "PREDICATE_NOT_MONOTONIC")

    def test_CFD_06_non_convex_dp_rejects_monotone_queue(self):
        """Arbitrary non-convex DP cost strictly rejects monotonic deque optimization."""
        spec = {"objective": "CF_CONVEX_DP_MONOTONIC_QUEUE", "dp_convex": False}
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "NON_CONVEX_COST_REJECTS_MONOTONIC_QUEUE")

    def test_CFD_07_bottleneck_path_selects_bisection_reachability(self):
        """Bottleneck minimax query selects bisection + reachability BFS."""
        spec = {"objective": "CF_BOTTLENECK_PATH_BINARY_SEARCH"}
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["plan"].recipe_name, "cf_bottleneck_path_binary_search")

    def test_CFD_08_interval_edges_selects_segment_tree_graph(self):
        """Range-to-range edge relaxation selects auxiliary segment tree graph nodes."""
        spec = {"objective": "CF_GRAPH_SEGMENT_TREE_RELAXATION"}
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["plan"].recipe_name, "cf_graph_segment_tree_relaxation")

    def test_CFD_09_dynamic_tree_path_selects_hld_segtree(self):
        """Tree path updates select HLD + Segment Tree range provider."""
        spec = {"objective": "CF_TREE_PATH_HLD_SEGMENT_TREE", "topology": "CONNECTED_ACYCLIC"}
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["plan"].recipe_name, "cf_tree_path_hld_segment_tree")

    def test_CFD_10_dp_range_acceleration_selects_segtree(self):
        """Associative contiguous DP transition selects Segment Tree acceleration."""
        spec = {"objective": "CF_DP_RANGE_ACCELERATION_SEGMENT_TREE", "algebra_op": "SUM"}
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["plan"].recipe_name, "cf_dp_range_acceleration_segment_tree")

    def test_CFD_11_fractional_ratio_selects_fractional_bisection(self):
        """Fractional ratio optimization selects parametric bisection lambda."""
        spec = {"objective": "CF_FRACTIONAL_BISECTION_DP", "predicate_monotonic": True}
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["plan"].recipe_name, "cf_fractional_bisection_dp")

    def test_CFD_12_event_scheduling_selects_greedy_heap(self):
        """Interval scheduling with start-time sorting selects Min-Heap priority queue."""
        spec = {"objective": "CF_EVENT_SCHEDULING_GREEDY_HEAP"}
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["plan"].recipe_name, "cf_event_scheduling_greedy_heap")


if __name__ == "__main__":
    unittest.main()
