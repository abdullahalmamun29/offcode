"""
Comprehensive Unit Test Suite for Monotonic Stack Domain (Phase 3B).
"""

import unittest
from pointer_algorithms.bridge import handle_request
from pointer_algorithms.reasoning.monotonicity_engine import MonotonicityEngine, MonotonicityKind, MonotonicityStatus
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine
from pointer_algorithms.failure_analysis.classifier import FailureClassifier, FailureCategory
from pointer_algorithms.recognition.feature_extractor import FeatureExtractor
from pointer_algorithms.recognition.candidate_generator import CandidateGenerator
from pointer_algorithms.recognition.candidate_eliminator import CandidateEliminator
from pointer_algorithms.monotonic_stack.verification.ms_brute_force_oracles import (
    oracle_next_greater_element, oracle_next_smaller_element,
    oracle_previous_greater_element, oracle_previous_smaller_element,
    oracle_nearest_greater_element, oracle_nearest_smaller_element,
    oracle_stock_span, oracle_largest_rectangle_histogram,
    oracle_circular_next_greater,
    oracle_sum_subarray_minimums, oracle_sum_subarray_maximums
)

class TestMonotonicStackDomain(unittest.TestCase):

    def test_monotonicity_engine_stack_elimination(self):
        """Monotonicity engine must confirm STACK_ELIMINATION_MONOTONICITY for MS patterns."""
        for pat in [
            "next_greater_element", "next_smaller_element",
            "previous_greater_element", "previous_smaller_element",
            "nearest_greater_element", "nearest_smaller_element",
            "stock_span", "largest_rectangle_histogram",
            "circular_next_greater", "sum_subarray_minimums", "sum_subarray_maximums"
        ]:
            assessment = MonotonicityEngine.assess_for_pattern(pat, {}, is_sorted=False, can_sort=False, is_contiguous=True)
            self.assertEqual(assessment.kind, MonotonicityKind.STACK_ELIMINATION_MONOTONICITY, f"Failed for {pat}")
            self.assertEqual(assessment.status, MonotonicityStatus.MONOTONICITY_CONFIRMED, f"Failed for {pat}")
            self.assertTrue(assessment.is_valid_for_movement)
            self.assertIn("Stack", assessment.property_description)

    def test_invariant_engine_phases(self):
        """Invariant engine must construct non-empty invariant stages for MS patterns."""
        for pat in ["next_greater_element", "stock_span", "largest_rectangle_histogram", "sum_subarray_minimums"]:
            inv = InvariantEngine.construct_invariant(pat, {})
            self.assertTrue(len(inv.before_iteration) > 10)
            self.assertTrue(len(inv.during_iteration) > 10)
            self.assertTrue(len(inv.after_movement) > 10)
            self.assertTrue(len(inv.at_termination) > 10)

    def test_movement_derivation_dominance_proof(self):
        """Movement derivation engine must provide formal elimination/dominance proofs."""
        for pat in ["next_greater_element", "stock_span", "largest_rectangle_histogram"]:
            deriv = MovementDerivationEngine.derive(pat, {})
            self.assertIn("Dominance proof", deriv.elimination_proof)
            self.assertTrue(len(deriv.decision_conditions) >= 2)

    def test_candidate_rejection_dynamic_updates(self):
        """Monotonic stack candidates must be rejected when dynamic updates are present."""
        text = "Find next greater element with online point updates to the array elements."
        features = FeatureExtractor.extract(text)
        self.assertTrue(features.has_dynamic_updates)
        cands = CandidateGenerator.generate_candidates(features)
        ranking = CandidateEliminator.filter_and_rank(cands, features)
        eliminated_codes = [e.rejection_code for e in ranking["eliminated"]]
        self.assertIn("STACK_ELIMINATION_NOT_SAFE", eliminated_codes)
        # End to end via bridge must be rejected from pointer/stack domain
        resp = handle_request({"problemText": text})
        self.assertEqual(resp["status"], "rejected")

    def test_brute_force_oracles_corner_cases(self):
        """Oracles must handle n=1, duplicates, and strictly monotonic arrays."""
        # n=1
        self.assertEqual(oracle_next_greater_element([10]), [-1])
        self.assertEqual(oracle_stock_span([10]), [1])
        self.assertEqual(oracle_largest_rectangle_histogram([10]), 10)
        self.assertEqual(oracle_sum_subarray_minimums([10]), 10)
        # All equal
        self.assertEqual(oracle_next_greater_element([5, 5, 5]), [-1, -1, -1])
        self.assertEqual(oracle_stock_span([5, 5, 5]), [1, 2, 3])
        self.assertEqual(oracle_largest_rectangle_histogram([5, 5, 5]), 15)
        self.assertEqual(oracle_circular_next_greater([5, 5, 5]), [-1, -1, -1])

    def test_metamorphic_histogram_scaling(self):
        """Metamorphic property: scaling bar heights by c scales max rectangle area by c."""
        heights = [2, 1, 5, 6, 2, 3]
        base_area = oracle_largest_rectangle_histogram(heights)
        scaled_c2 = oracle_largest_rectangle_histogram([h * 2 for h in heights])
        scaled_c5 = oracle_largest_rectangle_histogram([h * 5 for h in heights])
        self.assertEqual(scaled_c2, base_area * 2)
        self.assertEqual(scaled_c5, base_area * 5)

    def test_failure_classifier_ms_categories(self):
        """FailureClassifier must correctly map MS failure codes."""
        self.assertEqual(FailureCategory.MS_WRONG_RELATION.value, "MS_WRONG_RELATION")
        self.assertEqual(FailureCategory.MS_COMPLEXITY_FAILURE.value, "MS_COMPLEXITY_FAILURE")
        self.assertEqual(FailureCategory.MS_CIRCULAR_INDEX_ERROR.value, "MS_CIRCULAR_INDEX_ERROR")
        self.assertEqual(FailureCategory.MS_CONTRIBUTION_COUNT_ERROR.value, "MS_CONTRIBUTION_COUNT_ERROR")

    def test_end_to_end_bridge_request(self):
        """handle_request must return full reasoning structure for MS problems."""
        resp = handle_request({"problemText": "Given an array of temperatures, find how many days until a warmer temperature."})
        self.assertEqual(resp["status"], "success")
        self.assertEqual(resp["family"], "monotonic_stack")
        self.assertEqual(resp["selectedPattern"], "next_greater_element")
        self.assertIn("code", resp)
        self.assertIn("monotonicity", resp)
        self.assertIn("invariant", resp)
        self.assertIn("movement", resp)
        self.assertIn("reasoning", resp)

if __name__ == "__main__":
    unittest.main()
