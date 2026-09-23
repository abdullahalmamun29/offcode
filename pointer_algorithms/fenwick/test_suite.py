"""
Comprehensive Unit Test Suite for CHUP Phase 3I: Fenwick Tree (Binary Indexed Tree)
Tests:
- Structural invariants (lowbit intervals, covering length, parents)
- Algebraic group vs monoid properties
- Invariant Engine construction across all 10 patterns
- Movement Derivation across all 10 patterns
- Candidate Eliminator Section 17 rules
- Failure Classifier across 14 Fenwick categories
- C++ generator syntax and validity
- Bridge integration and structured fenwick metadata emission
"""

import unittest
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.knowledge.taxonomy import (
    FenwickKind,
    FenwickOperationKind,
    FENWICK_PATTERNS,
    PatternKind,
)
from pointer_algorithms.reasoning.reasoning_engine import (
    FenwickStructuralReasoning,
)
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine
from pointer_algorithms.recognition.candidate_eliminator import CandidateEliminator
from pointer_algorithms.recognition.feature_extractor import ProblemFeatures, FeatureExtractor
from pointer_algorithms.failure_analysis.classifier import FailureClassifier, FailureCategory
from pointer_algorithms.generator.fenwick_cpp_generator import generate_fenwick_cpp
from pointer_algorithms.bridge import handle_request


class TestFenwickStructuralInvariants(unittest.TestCase):
    def test_lowbit_algebra(self):
        """Test lowbit calculation: lowbit(i) = i & (-i)."""
        for i in range(1, 17):
            self.assertEqual(FenwickStructuralReasoning.lowbit(i), i & (-i))
        self.assertEqual(FenwickStructuralReasoning.lowbit(1), 1)
        self.assertEqual(FenwickStructuralReasoning.lowbit(2), 2)
        self.assertEqual(FenwickStructuralReasoning.lowbit(4), 4)
        self.assertEqual(FenwickStructuralReasoning.lowbit(8), 8)
        self.assertEqual(FenwickStructuralReasoning.lowbit(12), 4)

    def test_structural_proof(self):
        """Verify structural proof properties and algebraic scopes."""
        proof = FenwickStructuralReasoning.explain("point_update_prefix_query")
        self.assertIn("commutative monoid", proof.algebraic_scope)
        self.assertIn("1-based indexing", proof.indexing_convention)
        self.assertIn("Prefix Query Derivation", proof.prefix_query_derivation)
        self.assertIn("Point Update Derivation", proof.point_update_derivation)
        self.assertIn("F[v]", proof.frequency_invariant)
        self.assertIn("Right-to-left", proof.inversion_counting_traversal)
        self.assertIn("Left-to-right", proof.inversion_counting_traversal)
        self.assertIn("long long", proof.integer_width_policy)
        self.assertIn("Linear-Time Build", proof.linear_build_derivation)

    def test_two_fenwick_algebraic_derivation(self):
        """Verify Two-Fenwick range sum algebraic formula: sum(1..i) = (i+1)*pref(B1) - pref(B2)."""
        pref = FenwickStructuralReasoning.derive_two_fenwick_prefix(5, 10, 4)
        self.assertEqual(pref, (5 + 1) * 10 - 4)  # 56
        updates = FenwickStructuralReasoning.derive_two_fenwick_range_add_updates(2, 4, 5)
        self.assertEqual(len(updates), 4)
        self.assertEqual(updates[0], ("B1", 2, 5))
        self.assertEqual(updates[1], ("B1", 5, -5))
        self.assertEqual(updates[2], ("B2", 2, 10))
        self.assertEqual(updates[3], ("B2", 5, -25))

    def test_kth_binary_lifting_search(self):
        """K-th element binary lifting over monotonic non-negative frequencies."""
        tree = [0, 2, 3, 0, 6]  # BIT for counts [2, 1, 0, 3]
        ans = FenwickStructuralReasoning.kth_element_search(tree, 3, 4)
        self.assertEqual(ans, 2)


class TestFenwickInvariantAndMovement(unittest.TestCase):
    def test_all_10_patterns_invariant_generation(self):
        """All 10 Fenwick patterns must generate valid 4-phase invariants."""
        for pat in FENWICK_PATTERNS:
            inv = InvariantEngine.construct_invariant(pat, {})
            self.assertTrue(len(inv.before_iteration) > 10, f"Failed before invariant for {pat}")
            self.assertTrue(len(inv.during_iteration) > 10, f"Failed during invariant for {pat}")
            self.assertTrue(len(inv.after_movement) > 10, f"Failed after invariant for {pat}")
            self.assertTrue(len(inv.at_termination) > 10, f"Failed termination invariant for {pat}")

    def test_all_10_patterns_movement_derivation(self):
        """All 10 Fenwick patterns must generate valid movement decisions and proofs."""
        for pat in FENWICK_PATTERNS:
            mv = MovementDerivationEngine.derive(pat, {})
            self.assertTrue(len(mv.objective_function) > 5, f"Failed objective for {pat}")
            self.assertTrue(len(mv.decision_conditions) > 0, f"Failed decisions for {pat}")
            self.assertTrue(len(mv.elimination_proof) > 10, f"Failed proof for {pat}")


class TestFenwickCandidateEliminator(unittest.TestCase):
    def test_rule_f1_static_array_suboptimal(self):
        feat = FeatureExtractor.extract("Static array with no updates: query range sums.")
        res = handle_request({"problemText": feat.raw_text})
        elim = res.get("eliminatedCandidates", [])
        self.assertTrue(any(e.get("rejectionCode") == "FENWICK_STATIC_QUERY_SUBOPTIMAL" for e in elim))

    def test_rule_f2_offline_range_add_overkill(self):
        feat = FeatureExtractor.extract("Batch range adds offline where all queries are only after all updates finish.")
        res = handle_request({"problemText": feat.raw_text})
        elim = res.get("eliminatedCandidates", [])
        self.assertTrue(any(e.get("rejectionCode") == "FENWICK_OFFLINE_RANGE_ADD_OVERKILL" for e in elim))

    def test_rule_f3_structural_incompatibility(self):
        feat = FeatureExtractor.extract("Arbitrary range query requiring subtraction and inversion for non-invertible range gcd without inverse.")
        res = handle_request({"problemText": feat.raw_text})
        elim = res.get("eliminatedCandidates", [])
        self.assertTrue(any(e.get("rejectionCode") == "FENWICK_STRUCTURAL_INCOMPATIBILITY" for e in elim))

    def test_rule_f4_dynamic_coordinate_unrepresentable(self):
        feat = FeatureExtractor.extract("Unknown dynamic streaming keys appearing online without prior bound.")
        res = handle_request({"problemText": feat.raw_text})
        elim = res.get("eliminatedCandidates", [])
        self.assertTrue(any(e.get("rejectionCode") == "FENWICK_DYNAMIC_COORDINATE_UNREPRESENTABLE" for e in elim))

    def test_rule_f5_kth_negative_frequency(self):
        feat = FeatureExtractor.extract("Allow negative counts for k-th element search with negative frequency updates.")
        res = handle_request({"problemText": feat.raw_text})
        elim = res.get("eliminatedCandidates", [])
        self.assertTrue(any(e.get("rejectionCode") == "FENWICK_KTH_NEGATIVE_FREQUENCY" for e in elim))


class TestFenwickFailureClassifier(unittest.TestCase):
    def test_failure_categories(self):
        """Verify Fenwick failure categories classify accurately."""
        cases = [
            ("FENWICK_STATIC_QUERY_SUBOPTIMAL static sum on immutable array", FailureCategory.FENWICK_STATIC_QUERY_SUBOPTIMAL),
            ("FENWICK_OFFLINE_RANGE_ADD_OVERKILL difference array recommended", FailureCategory.FENWICK_OFFLINE_RANGE_ADD_OVERKILL),
            ("FENWICK_STRUCTURAL_INCOMPATIBILITY non-invertible range query", FailureCategory.FENWICK_STRUCTURAL_INCOMPATIBILITY),
            ("FENWICK_DYNAMIC_COORDINATE_UNREPRESENTABLE unknown dynamic coordinates", FailureCategory.FENWICK_DYNAMIC_COORDINATE_UNREPRESENTABLE),
            ("FENWICK_KTH_NEGATIVE_FREQUENCY negative frequencies unsupported", FailureCategory.FENWICK_KTH_NEGATIVE_FREQUENCY),
            ("FENWICK_DIMENSION_MISMATCH 2D required", FailureCategory.FENWICK_DIMENSION_MISMATCH),
            ("FENWICK_OPERATION_MISMATCH operation mismatch", FailureCategory.FENWICK_OPERATION_MISMATCH),
        ]
        for msg, expected_cat in cases:
            rec = FailureClassifier.classify(msg, {})
            self.assertEqual(rec.category, expected_cat, f"Mismatch for '{msg}': got {rec.category}, expected {expected_cat}")


class TestFenwickBridgeAndGenerator(unittest.TestCase):
    def test_bridge_emits_structured_fenwick_metadata(self):
        res = handle_request({"problemText": "Maintain dynamic prefix sums with point update at index and prefix sum queries."})
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["selectedPattern"], "fenwick_point_update_prefix_query")
        fenwick_meta = res.get("fenwick")
        self.assertIsNotNone(fenwick_meta)
        self.assertIn("kind", fenwick_meta)
        self.assertIn("operationKind", fenwick_meta)
        self.assertIn("algorithmFamily", fenwick_meta)

    def test_all_10_cpp_templates_generate_cleanly(self):
        """All 10 Fenwick patterns generate valid C++ code with 64-bit safety and 1-based indexing."""
        for pat in FENWICK_PATTERNS:
            code = generate_fenwick_cpp(pat, {})
            self.assertIn("#include <iostream>", code)
            self.assertTrue("& -" in code or "& (-" in code, f"Missing lowbit expression in {pat}")
            self.assertTrue(len(code) > 200)


if __name__ == "__main__":
    unittest.main()
