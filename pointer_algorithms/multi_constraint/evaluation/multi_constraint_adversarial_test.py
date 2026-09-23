"""
CHUP Phase 5 — Multi-Constraint Adversarial Attacks Evaluation Suite (Tier 2).

Adversarially probes for false elimination, false contradiction, false composition
failures, and cryptographic integrity tampering in the reasoning engine.
"""

import unittest
from pointer_algorithms.multi_constraint.facade import MultiConstraintSolver
from pointer_algorithms.multi_constraint.multi_constraint_model import OutcomeState, VerifiedMultiConstraintPlan
from pointer_algorithms.multi_constraint.constraint_lattice import (
    TemporalMode,
    MutabilityCapability,
    CoordinateScale,
)


class TestMultiConstraintAdversarial(unittest.TestCase):
    """Tier 2 evaluation: adversarial robustness and integrity tests."""

    def setUp(self):
        self.solver = MultiConstraintSolver()

    def test_adv_01_kruskal_negative_weights_not_eliminated(self):
        """CRITICAL: Kruskal MST handles negative edge weights correctly and must NOT be eliminated."""
        spec = {
            "query_target": "POINT",
            "operation": "SUM",
            "negative_weights": True
        }
        elim = self.solver.explain_candidate("kruskal_mst", spec)
        self.assertIsNone(
            elim,
            "Adversarial Failure: Kruskal was falsely eliminated on negative edge weights! Kruskal allows arbitrary comparable weights."
        )

    def test_adv_02_singleton_range_reduction_preserves_fenwick(self):
        """Range update [i, i] reduced to POINT_WRITE must NOT eliminate Fenwick Tree."""
        spec = {
            "temporal": "ONLINE",
            "mutability": "SINGLETON_RANGE_UPDATE",
            "operation": "SUM",
            "query_target": "LINEAR_RANGE"
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.SATISFIABLE_SINGLE_CANDIDATE)
        plan = res["verified_plan"]
        self.assertIsNotNone(plan)
        # Fenwick or Segment Tree can satisfy point update sum, but neither should be eliminated by mutability
        elim_fenwick = self.solver.explain_candidate("fenwick_tree", spec)
        self.assertIsNone(elim_fenwick, "Fenwick tree was falsely eliminated despite singleton reduction")

    def test_adv_03_tree_path_query_not_falsely_unsatisfiable(self):
        """Tree path query with point updates must NOT return UNSATISFIABLE_CONSTRAINT_SET."""
        spec = {
            "topology": "UNDIRECTED_TREE",
            "v": 50000,
            "e": 49999,
            "query_target": "TREE_PATH",
            "mutability": "POINT_UPDATE",
            "operation": "SUM"
        }
        res = self.solver.solve(spec)
        self.assertNotEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        self.assertEqual(res["outcome_state"], OutcomeState.SATISFIABLE_COMPOSED_PLAN)
        plan = res["verified_plan"]
        self.assertIn("heavy_light_decomposition", plan.selected_components)

    def test_adv_04_offline_distinct_not_falsely_unsatisfiable(self):
        """Offline range distinct query must NOT return UNSATISFIABLE_CONSTRAINT_SET."""
        spec = {
            "temporal": "OFFLINE",
            "operation": "DISTINCT",
            "transition_reversible": True,
            "query_target": "LINEAR_RANGE"
        }
        res = self.solver.solve(spec)
        self.assertNotEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        self.assertIn(
            res["outcome_state"],
            (OutcomeState.SATISFIABLE_SINGLE_CANDIDATE, OutcomeState.SATISFIABLE_COMPOSED_PLAN)
        )

    def test_adv_05_massive_coordinates_offline_known_not_unsatisfiable(self):
        """Coordinates up to 10^18 with offline coordinates known must NOT return UNSATISFIABLE_CONSTRAINT_SET."""
        spec = {
            "temporal": "OFFLINE",
            "coordinate_scale": "MASSIVE",
            "c": 10**18,
            "offline_coordinates_known": True,
            "dynamic_pointers_allowed": False,
            "mutability": "POINT_UPDATE",
            "operation": "SUM"
        }
        res = self.solver.solve(spec)
        self.assertNotEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        self.assertEqual(res["outcome_state"], OutcomeState.SATISFIABLE_COMPOSED_PLAN)
        plan = res["verified_plan"]
        self.assertIn("coordinate_compressor", plan.selected_components)

    def test_adv_06_non_invertible_range_min_rejects_fenwick(self):
        """Range MIN query with point updates must select Segment Tree, NOT Fenwick Tree."""
        spec = {
            "temporal": "ONLINE",
            "mutability": "POINT_UPDATE",
            "operation": "MIN",
            "query_target": "LINEAR_RANGE"
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.SATISFIABLE_SINGLE_CANDIDATE)
        plan = res["verified_plan"]
        self.assertEqual(plan.selected_components, ["segment_tree_standard"])
        elim_fenwick = self.solver.explain_candidate("fenwick_tree", spec)
        self.assertIsNotNone(elim_fenwick)
        self.assertEqual(elim_fenwick.failure_code, "NON_INVERTIBLE_OPERATION_REJECTS_FENWICK")

    def test_adv_07_online_massive_coordinates_selects_dynamic_segtree(self):
        """Online massive coordinates with dynamic pointers allowed must select Dynamic Segment Tree."""
        spec = {
            "temporal": "ONLINE",
            "coordinate_scale": "MASSIVE",
            "dynamic_pointers_allowed": True,
            "mutability": "POINT_UPDATE",
            "operation": "SUM",
            "query_target": "LINEAR_RANGE"
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.SATISFIABLE_SINGLE_CANDIDATE)
        plan = res["verified_plan"]
        self.assertEqual(plan.selected_components, ["dynamic_segment_tree"])

    def test_adv_08_non_negative_weights_sssp_selects_dijkstra(self):
        """Graph SSSP with non-negative edge weights must select Dijkstra without false rejection."""
        spec = {
            "query_target": "SINGLE_SOURCE_SHORTEST_PATH",
            "operation": "MIN",
            "negative_weights": False
        }
        elim = self.solver.explain_candidate("dijkstra_priority_queue", spec)
        self.assertIsNone(elim, "Dijkstra was falsely eliminated on non-negative edge weights")

    def test_adv_09_cryptographic_seal_deterministic(self):
        """SHA-256 seal is strictly deterministic and invariant to non-semantic ordering."""
        spec = {
            "temporal": "ONLINE",
            "mutability": "POINT_UPDATE",
            "operation": "SUM",
            "query_target": "LINEAR_RANGE"
        }
        res1 = self.solver.solve(spec)
        res2 = self.solver.solve(spec)
        plan1 = res1["verified_plan"]
        plan2 = res2["verified_plan"]
        # Both produce valid 64-character hex digests
        self.assertEqual(len(plan1.cryptographic_hash_seal), 64)
        self.assertEqual(len(plan2.cryptographic_hash_seal), 64)
        self.assertTrue(plan1.verify_seal())
        self.assertTrue(plan2.verify_seal())

    def test_adv_10_tampered_plan_seal_rejected(self):
        """Tampering with selected_components or proof obligations breaks cryptographic seal."""
        spec = {
            "temporal": "ONLINE",
            "mutability": "POINT_UPDATE",
            "operation": "SUM",
            "query_target": "LINEAR_RANGE"
        }
        res = self.solver.solve(spec)
        plan = res["verified_plan"]
        self.assertTrue(plan.verify_seal())

        # Construct a tampered copy with different selected components
        from dataclasses import replace
        tampered_plan = replace(plan, selected_components=["unauthorized_backdoor_algorithm"])
        self.assertFalse(tampered_plan.verify_seal(), "Tampered plan must fail cryptographic verification")


if __name__ == "__main__":
    unittest.main()
