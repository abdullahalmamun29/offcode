"""
Comprehensive Unit Test Suite for Binary Search Domain (Phase 3C).
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
from pointer_algorithms.binary_search.verification.bs_brute_force_oracles import (
    oracle_binary_search_exact,
    oracle_lower_bound,
    oracle_upper_bound,
    oracle_predecessor,
    oracle_successor,
    oracle_min_ship_capacity,
    oracle_max_min_distance,
    oracle_integer_sqrt,
)

class TestBinarySearchDomain(unittest.TestCase):

    def test_monotonicity_engine_bs_patterns(self):
        """Monotonicity engine must confirm appropriate monotonicity for BS patterns."""
        # Ordered data search
        for pat in ["binary_search_exact", "lower_bound", "upper_bound", "predecessor", "successor"]:
            res = MonotonicityEngine.assess_for_pattern(pat, {}, is_sorted=True, can_sort=False, is_contiguous=True)
            self.assertEqual(res.kind, MonotonicityKind.VALUE_ORDER_MONOTONICITY)
            self.assertEqual(res.status, MonotonicityStatus.MONOTONICITY_CONFIRMED)
            self.assertTrue(res.is_valid_for_movement)

        # Predicate search
        for pat in ["first_true", "last_true", "first_false", "last_false"]:
            res = MonotonicityEngine.assess_for_pattern(pat, {}, is_sorted=True, can_sort=False, is_contiguous=True)
            self.assertEqual(res.kind, MonotonicityKind.PREDICATE_MONOTONICITY)
            self.assertEqual(res.status, MonotonicityStatus.MONOTONICITY_CONFIRMED)

        # Answer space search
        for pat in ["binary_search_answer_min", "binary_search_answer_max"]:
            res = MonotonicityEngine.assess_for_pattern(pat, {}, is_sorted=False, can_sort=False, is_contiguous=False)
            self.assertEqual(res.kind, MonotonicityKind.FEASIBILITY_MONOTONICITY)
            self.assertEqual(res.status, MonotonicityStatus.MONOTONICITY_CONFIRMED)

    def test_invariant_engine_bs_phases(self):
        """Invariant engine must construct all 4 formal stages for BS patterns."""
        for pat in ["binary_search_exact", "lower_bound", "upper_bound", "binary_search_answer_min", "binary_search_answer_max"]:
            inv = InvariantEngine.construct_invariant(pat, {})
            self.assertTrue(len(inv.before_iteration) > 10)
            self.assertTrue(len(inv.during_iteration) > 10)
            self.assertTrue(len(inv.after_movement) > 10)
            self.assertTrue(len(inv.at_termination) > 10)

    def test_movement_derivation_half_elimination_proof(self):
        """Movement derivation must provide formal elimination proofs and safe midpoint calculation."""
        for pat in ["binary_search_exact", "lower_bound", "binary_search_answer_min", "binary_search_answer_max"]:
            deriv = MovementDerivationEngine.derive(pat, {})
            self.assertIn("Proof", deriv.elimination_proof)
            self.assertIn("mid", deriv.elimination_proof)
            self.assertTrue(len(deriv.decision_conditions) >= 2)

    def test_candidate_rejection_unsorted(self):
        """Index binary search must be rejected when array is unsorted and cannot be sorted."""
        text = "Given an unsorted array of numbers, search for target using binary search without sorting the array."
        features = FeatureExtractor.extract(text)
        self.assertFalse(features.has_ordered_search_space)
        cands = CandidateGenerator.generate_candidates(features)
        ranking = CandidateEliminator.filter_and_rank(cands, features)
        eliminated_codes = [e.rejection_code for e in ranking["eliminated"]]
        self.assertIn("BINARY_SEARCH_ORDERING_MISSING", eliminated_codes)
        resp = handle_request({"problemText": text})
        self.assertEqual(resp["status"], "rejected")

    def test_candidate_rejection_non_monotone_predicate(self):
        """Binary search must be rejected when predicate oscillates or is non-monotonic."""
        text = "Search in an array where the test predicate alternates between true and false arbitrarily (non-monotonic)."
        features = FeatureExtractor.extract(text)
        self.assertTrue(features.has_non_monotonic_predicate)
        cands = CandidateGenerator.generate_candidates(features)
        ranking = CandidateEliminator.filter_and_rank(cands, features)
        eliminated_codes = [e.rejection_code for e in ranking["eliminated"]]
        self.assertIn("BINARY_SEARCH_PREDICATE_NOT_MONOTONE", eliminated_codes)
        resp = handle_request({"problemText": text})
        self.assertEqual(resp["status"], "rejected")

    def test_candidate_rejection_dynamic_updates(self):
        """Static binary search must be rejected when interleaved with dynamic point updates across queries."""
        text = "Support interleaved online point updates to elements and repeated binary search queries."
        features = FeatureExtractor.extract(text)
        self.assertTrue(features.has_dynamic_updates)
        self.assertTrue(features.repeated_queries)
        cands = CandidateGenerator.generate_candidates(features)
        ranking = CandidateEliminator.filter_and_rank(cands, features)
        eliminated_codes = [e.rejection_code for e in ranking["eliminated"]]
        self.assertIn("BINARY_SEARCH_SEARCH_SPACE_INVALID", eliminated_codes)
        resp = handle_request({"problemText": text})
        self.assertEqual(resp["status"], "rejected")

    def test_oracles_corner_cases(self):
        """Oracles must handle duplicates, boundary values, empty results, and extreme thresholds."""
        arr = [2, 4, 4, 4, 8]
        self.assertEqual(oracle_lower_bound(arr, 4), 1)
        self.assertEqual(oracle_upper_bound(arr, 4), 4)
        self.assertEqual(oracle_predecessor(arr, 4), 2)
        self.assertEqual(oracle_successor(arr, 4), 8)
        self.assertEqual(oracle_integer_sqrt(0), 0)
        self.assertEqual(oracle_integer_sqrt(1), 1)
        self.assertEqual(oracle_integer_sqrt(15), 3)
        self.assertEqual(oracle_integer_sqrt(16), 4)

    def test_failure_classifier_bs_categories(self):
        """FailureClassifier must correctly map BS failure codes."""
        self.assertEqual(FailureCategory.BS_PREDICATE_NOT_MONOTONE.value, "BS_PREDICATE_NOT_MONOTONE")
        self.assertEqual(FailureCategory.BS_ORDERING_MISSED.value, "BS_ORDERING_MISSED")
        self.assertEqual(FailureCategory.BS_FIRST_TRUE_ERROR.value, "BS_FIRST_TRUE_ERROR")
        self.assertEqual(FailureCategory.BS_LAST_TRUE_ERROR.value, "BS_LAST_TRUE_ERROR")
        self.assertEqual(FailureCategory.BS_FEASIBILITY_CONSTRUCTION_ERROR.value, "BS_FEASIBILITY_CONSTRUCTION_ERROR")

    def test_end_to_end_bridge_request(self):
        """handle_request must return full reasoning and binarySearch trace."""
        resp = handle_request({"problemText": "Given a sorted array of integers, find the lower bound of target x."})
        self.assertEqual(resp["status"], "success")
        self.assertEqual(resp["family"], "binary_search")
        self.assertEqual(resp["selectedPattern"], "lower_bound")
        self.assertIn("code", resp)
        self.assertIn("binarySearch", resp)
        self.assertIsNotNone(resp["binarySearch"])
        self.assertEqual(resp["binarySearch"]["boundary"], "lower_bound")
        self.assertTrue(resp["binarySearch"]["predicate"]["isMonotone"])

if __name__ == "__main__":
    unittest.main()
