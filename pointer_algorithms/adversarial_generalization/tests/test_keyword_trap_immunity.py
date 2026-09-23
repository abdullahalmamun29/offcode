"""
Test Keyword Trap Immunity & Non-Prescription.

Verifies:
1. 100% of certified keyword traps trigger proper candidate elimination.
2. Candidate elimination is driven by mathematical precondition failure.
3. No replacement algorithm is prescribed by the evaluator.
"""

import unittest

from pointer_algorithms.adversarial_generalization.keyword_trap_registry import (
    KeywordTrapRegistry,
    KeywordTrap
)
from pointer_algorithms.adversarial_generalization.adversarial_comparator import AdversarialComparator
from pointer_algorithms.deep_understanding.deep_understanding_facade import DeepProblemUnderstandingFacade


class TestKeywordTrapImmunity(unittest.TestCase):

    def setUp(self):
        self.facade = DeepProblemUnderstandingFacade()

    def test_all_ten_traps_registered_and_evaluated(self):
        traps = KeywordTrapRegistry.get_all_traps()
        self.assertEqual(len(traps), 10, "Must contain exactly 10 canonical keyword traps")

        for trap in traps:
            with self.subTest(trap_id=trap.trap_id, name=trap.name):
                res = AdversarialComparator.compare_elimination(trap, self.facade)
                self.assertTrue(res.is_eliminated, f"Trap {trap.trap_id} failed elimination: {res.details}")
                self.assertFalse(res.prescribes_winner, f"Trap {trap.trap_id} unlawfully prescribed a winner")

    def test_trap_1_negative_weights_eliminates_dijkstra_without_prescription(self):
        trap = KeywordTrapRegistry.get_trap("TRAP-01-NEG-WEIGHTS")
        self.assertIsNotNone(trap)
        res = self.facade.process(trap.adversarial_spec)
        p5_res = res.get("phase5_result", {})
        analysis = p5_res.get("candidate_analysis")
        self.assertIsNotNone(analysis)
        self.assertIn("dijkstra_priority_queue", analysis.eliminated_candidates)
        cert = analysis.eliminated_candidates["dijkstra_priority_queue"]
        self.assertEqual(cert.failure_code, "NEGATIVE_WEIGHTS_REJECT_DIJKSTRA")
        # Ensure Phase 8 did not dictate replacement algorithm
        comp_res = AdversarialComparator.compare_elimination(trap, self.facade)
        self.assertFalse(comp_res.prescribes_winner)
        self.assertIn("bellman_ford_only", trap.forbidden_prescriptions)

    def test_trap_5_unsorted_negative_eliminates_two_pointers(self):
        trap = KeywordTrapRegistry.get_trap("TRAP-05-UNSORTED-TWO-POINTERS")
        self.assertIsNotNone(trap)
        res = self.facade.process(trap.adversarial_spec)
        p5_res = res.get("phase5_result", {})
        analysis = p5_res.get("candidate_analysis")
        self.assertIsNotNone(analysis)
        self.assertIn("two_pointers_monotone_window", analysis.eliminated_candidates)
        cert = analysis.eliminated_candidates["two_pointers_monotone_window"]
        self.assertEqual(cert.failure_code, "NON_MONOTONE_WINDOW_REJECTS_TWO_POINTERS")

    def test_trap_6_dynamic_updates_eliminates_static_structure(self):
        trap = KeywordTrapRegistry.get_trap("TRAP-06-DYNAMIC-RANGE-SUM")
        self.assertIsNotNone(trap)
        res = self.facade.process(trap.adversarial_spec)
        p5_res = res.get("phase5_result", {})
        analysis = p5_res.get("candidate_analysis")
        self.assertIsNotNone(analysis)
        self.assertIn("sparse_table", analysis.eliminated_candidates)
        cert = analysis.eliminated_candidates["sparse_table"]
        self.assertEqual(cert.failure_code, "MUTATION_DISALLOWED_ON_STATIC_STRUCTURE")


if __name__ == "__main__":
    unittest.main()
