"""
Test Suite: Pillar IV — Parameterized Complexity & Hardness Boundary
Verifies Law 6 (certified reverse reduction H <=_p P for NP-hardness),
exact exponential feasibility envelopes, and Law 7 (budget exceeded != unsatisfiable).
"""

import unittest
from pointer_algorithms.research_level.hardness_boundary import HardnessBoundaryEngine
from pointer_algorithms.research_level.reduction_engine import ReductionEngine
from pointer_algorithms.research_level.research_types import (
    EpistemicStatus,
)


class TestHardnessAndFptBoundary(unittest.TestCase):

    def test_certify_hardness_via_valid_reduction(self):
        """Verify NP-hardness certified via valid reduction from known hard core (VERTEX_COVER)."""
        valid_red = ReductionEngine.reduce_vertex_cover_to_independent_set(
            problem_id="VERTEX_COVER_INSTANCE",
            requirements_hash="req_h_vc",
            num_vertices=10,
        )

        hard_cert, status, msg = HardnessBoundaryEngine.certify_hardness_via_reduction(
            user_problem_id="PROB_INDEPENDENT_SET",
            known_hard_core_id="VERTEX_COVER",
            reduction_cert=valid_red,
        )

        self.assertEqual(status, EpistemicStatus.PROVEN)
        self.assertIsNotNone(hard_cert)
        self.assertTrue(hard_cert.is_np_hard)
        self.assertEqual(hard_cert.known_hard_core_id, "VERTEX_COVER")
        self.assertIn("mathematically proven", msg)

    def test_certify_hardness_rejects_unknown_core(self):
        """Verify hardness certification rejected if hard core is not in certified registry."""
        valid_red = ReductionEngine.reduce_vertex_cover_to_independent_set(
            problem_id="ANY",
            requirements_hash="req_h",
            num_vertices=5,
        )

        hard_cert, status, msg = HardnessBoundaryEngine.certify_hardness_via_reduction(
            user_problem_id="PROB_CUSTOM",
            known_hard_core_id="UNREGISTERED_HARD_CORE_X",
            reduction_cert=valid_red,
        )

        self.assertEqual(status, EpistemicStatus.UNRESOLVED)
        self.assertIsNone(hard_cert)
        self.assertIn("not in certified known NP-hard core registry", msg)

    def test_certify_hardness_rejects_invalid_reduction(self):
        """Verify hardness certification rejected if reduction certificate fails validity."""
        invalid_red = ReductionEngine.reduce_bipartite_matching_to_vertex_cover(
            problem_id="PROB_FAIL",
            requirements_hash="req_fail",
            is_bipartite=False,
            left_nodes=0,
            right_nodes=0,
            num_edges=1,
        )

        hard_cert, status, msg = HardnessBoundaryEngine.certify_hardness_via_reduction(
            user_problem_id="PROB_USER",
            known_hard_core_id="3SAT",
            reduction_cert=invalid_red,
        )

        self.assertEqual(status, EpistemicStatus.UNRESOLVED)
        self.assertIsNone(hard_cert)
        self.assertIn("failed mathematical validity gates", msg)

    def test_bitmask_dp_tsp_feasibility_boundary(self):
        """Verify Bitmask DP feasibility boundary O(2^N * N^2) under contest budget 10^8."""
        # N = 15: 2^15 * 225 = 7,372,800 operations <= 10^8 -> FEASIBLE
        cert_feasible = HardnessBoundaryEngine.evaluate_exact_exponential_feasibility(
            algorithm_name="bitmask_dp_tsp",
            parameter_name="N",
            n_val=15,
        )
        self.assertTrue(cert_feasible.is_feasible)
        self.assertEqual(cert_feasible.status_label, "FEASIBLE")

        # N = 25: 2^25 * 625 = 2.09 * 10^10 operations > 10^8 -> EXCEEDED
        cert_exceeded = HardnessBoundaryEngine.evaluate_exact_exponential_feasibility(
            algorithm_name="bitmask_dp_tsp",
            parameter_name="N",
            n_val=25,
        )
        self.assertFalse(cert_exceeded.is_feasible)
        # Law 7: Must NOT be UNSATISFIABLE
        self.assertEqual(cert_exceeded.status_label, "PARAMETER_EXCEEDS_CERTIFIED_FEASIBILITY")
        self.assertNotEqual(cert_exceeded.status_label, "UNSATISFIABLE")

    def test_meet_in_the_middle_feasibility_boundary(self):
        """Verify Meet-in-the-Middle feasibility boundary O(2^(N/2) * (N/2))."""
        # N = 36: half_n = 18, 2^18 * 18 = 4,718,592 <= 10^8 -> FEASIBLE
        cert_feasible = HardnessBoundaryEngine.evaluate_exact_exponential_feasibility(
            algorithm_name="meet_in_the_middle",
            parameter_name="N",
            n_val=36,
        )
        self.assertTrue(cert_feasible.is_feasible)
        self.assertEqual(cert_feasible.status_label, "FEASIBLE")

        # N = 60: half_n = 30, 2^30 * 30 > 3 * 10^10 > 10^8 -> EXCEEDED
        cert_exceeded = HardnessBoundaryEngine.evaluate_exact_exponential_feasibility(
            algorithm_name="meet_in_the_middle",
            parameter_name="N",
            n_val=60,
        )
        self.assertFalse(cert_exceeded.is_feasible)
        self.assertEqual(cert_exceeded.status_label, "PARAMETER_EXCEEDS_CERTIFIED_FEASIBILITY")


if __name__ == "__main__":
    unittest.main()
