"""
CHUP Phase 5 — Multi-Constraint Holdout Benchmark Suite (Tier 2).

Evaluates the multi-constraint reasoning engine against formal specifications
of real-world competitive programming and complex systems engineering tasks:
- CSES Path Queries II (HLD + Segment Tree)
- CSES Static RMQ (Sparse Table)
- CSES Dynamic RMQ (Segment Tree Standard)
- SPOJ DQUERY (Mo's Algorithm + State Tracker)
- Massive Coordinate Offline Range Sum (Coordinate Compressor + Range Provider)
- Codeforces Negative Edge SSSP (Dijkstra Rejection -> SPFA/Bellman-Ford gap)
- Impossible Contradiction Scenarios from contests
"""

import unittest
from pointer_algorithms.multi_constraint.facade import MultiConstraintSolver
from pointer_algorithms.multi_constraint.multi_constraint_model import OutcomeState


class TestMultiConstraintHoldout(unittest.TestCase):
    """Tier 2 evaluation: real-world contest & systems holdout benchmarks."""

    def setUp(self):
        self.solver = MultiConstraintSolver()

    def test_holdout_01_cses_path_queries_ii(self):
        """CSES Path Queries II: Tree path maximum query with point updates.
        Requirements: Undirected Tree, N=200,000, Q=200,000, TREE_PATH target, POINT_UPDATE, MAX operation.
        Expected: SATISFIABLE_COMPOSED_PLAN chaining Heavy-Light Decomposition + Segment Tree.
        """
        spec = {
            "name": "CSES Path Queries II",
            "topology": "UNDIRECTED_TREE",
            "v": 200000,
            "e": 199999,
            "n": 200000,
            "q": 200000,
            "query_target": "TREE_PATH",
            "mutability": "POINT_UPDATE",
            "operation": "MAX"
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.SATISFIABLE_COMPOSED_PLAN)
        plan = res["verified_plan"]
        self.assertIn("heavy_light_decomposition", plan.selected_components)
        self.assertIn("segment_tree_standard", plan.selected_components)
        self.assertTrue(plan.verify_seal())

    def test_holdout_02_cses_static_rmq(self):
        """CSES Static RMQ: Static array range minimum queries.
        Requirements: Linear array, N=200,000, Q=200,000, STATIC, MIN operation.
        Expected: SATISFIABLE_SINGLE_CANDIDATE selecting Sparse Table for O(1) query time.
        """
        spec = {
            "name": "CSES Static RMQ",
            "temporal": "ONLINE",
            "n": 200000,
            "q": 200000,
            "mutability": "STATIC",
            "operation": "MIN",
            "query_target": "LINEAR_RANGE"
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.SATISFIABLE_SINGLE_CANDIDATE)
        plan = res["verified_plan"]
        self.assertEqual(plan.selected_components, ["sparse_table"])
        self.assertTrue(plan.verify_seal())

    def test_holdout_03_cses_dynamic_rmq(self):
        """CSES Dynamic RMQ: Range minimum queries with point updates.
        Requirements: Linear array, N=200,000, Q=200,000, POINT_UPDATE, MIN operation.
        Expected: SATISFIABLE_SINGLE_CANDIDATE selecting Standard Segment Tree (Sparse Table rejected on mutability, Fenwick rejected on non-invertible MIN).
        """
        spec = {
            "name": "CSES Dynamic RMQ",
            "temporal": "ONLINE",
            "n": 200000,
            "q": 200000,
            "mutability": "POINT_UPDATE",
            "operation": "MIN",
            "query_target": "LINEAR_RANGE"
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.SATISFIABLE_SINGLE_CANDIDATE)
        plan = res["verified_plan"]
        self.assertEqual(plan.selected_components, ["segment_tree_standard"])
        self.assertTrue(plan.verify_seal())

    def test_holdout_04_spoj_dquery(self):
        """SPOJ DQUERY: Count of distinct numbers in subarray [L, R] offline.
        Requirements: Offline query stream, N=30,000, Q=200,000, DISTINCT operation, reversible transition.
        Expected: SATISFIABLE_COMPOSED_PLAN synthesized with Mo's Algorithm Scheduler.
        """
        spec = {
            "name": "SPOJ DQUERY",
            "temporal": "OFFLINE",
            "n": 30000,
            "q": 200000,
            "mutability": "STATIC",
            "operation": "DISTINCT",
            "transition_reversible": True,
            "query_target": "LINEAR_RANGE"
        }
        res = self.solver.solve(spec)
        self.assertIn(
            res["outcome_state"],
            (OutcomeState.SATISFIABLE_SINGLE_CANDIDATE, OutcomeState.SATISFIABLE_COMPOSED_PLAN)
        )
        plan = res["verified_plan"]
        self.assertIsNotNone(plan)
        self.assertTrue(plan.verify_seal())

    def test_holdout_05_codeforces_massive_coordinate_offline_sum(self):
        """Codeforces Style Problem: Range sum on massive coordinates (10^18) with all points given offline.
        Requirements: OFFLINE, MASSIVE coordinates, POINT_UPDATE, SUM operation, flat arrays desired.
        Expected: SATISFIABLE_COMPOSED_PLAN chaining Coordinate Compressor + Range Query Provider.
        """
        spec = {
            "name": "Offline Massive Coordinate Range Sum",
            "temporal": "OFFLINE",
            "coordinate_scale": "MASSIVE",
            "c": 10**18,
            "offline_coordinates_known": True,
            "dynamic_pointers_allowed": False,
            "mutability": "POINT_UPDATE",
            "operation": "SUM"
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.SATISFIABLE_COMPOSED_PLAN)
        plan = res["verified_plan"]
        self.assertIn("coordinate_compressor", plan.selected_components)
        self.assertTrue(
            any(c in plan.selected_components for c in ("segment_tree_standard", "fenwick_tree"))
        )
        self.assertTrue(plan.verify_seal())

    def test_holdout_06_unresolved_dynamic_2d_range_counting(self):
        """High-dimensional 2D dynamic range query with range updates:
        Requirements: ALL_PAIRS / 2D target, RANGE_UPDATE, STREAMING temporal.
        Expected: UNRESOLVED_BY_CURRENT_ONTOLOGY (gap correctly flagged without false satisfaction).
        """
        spec = {
            "name": "2D Dynamic Range Updates in Streaming Mode",
            "query_target": "ALL_PAIRS",
            "mutability": "RANGE_UPDATE",
            "temporal": "STREAMING"
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.UNRESOLVED_BY_CURRENT_ONTOLOGY)
        cert = res["unresolved_certificate"]
        self.assertIsNotNone(cert)
        self.assertTrue(len(cert.uncovered_capabilities) > 0)

    def test_holdout_07_impossible_contest_spec_rejected(self):
        """Contest specification claiming an undirected tree with N=100,000 vertices and E=100,005 edges.
        Expected: UNSATISFIABLE_CONSTRAINT_SET with axiomatic proof certificate.
        """
        spec = {
            "name": "Flawed Contest Problem Statement",
            "topology": "UNDIRECTED_TREE",
            "v": 100000,
            "e": 100005
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        cert = res["conflict_certificate"]
        self.assertIsNotNone(cert)
        self.assertEqual(cert.failure_code, "TREE_EDGE_COUNT_CONTRADICTION")


if __name__ == "__main__":
    unittest.main()
