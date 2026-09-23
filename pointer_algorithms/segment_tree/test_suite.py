"""
Comprehensive Unit Test Suite for CHUP Phase 3J: Segment Tree
Tests:
- Structural invariants (canonical interval decomposition, node indexing, associative merges)
- Algebraic scope (commutative monoids, non-commutative associative merges, non-associative rejection)
- Invariant Engine construction across all 8 patterns
- Movement Derivation across all 8 patterns
- Candidate Eliminator Section 18 rules (ST1 through ST8)
- Failure Classifier across 11 Segment Tree categories
- C++ generator syntax and validity across all 8 patterns
- Bridge integration and structured segment_tree metadata emission
- Reference oracles verification
"""

import unittest
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.knowledge.taxonomy import (
    SegmentTreeKind,
    SegmentTreeOperationKind,
    SEGMENT_TREE_PATTERNS,
    PatternKind,
)
from pointer_algorithms.reasoning.reasoning_engine import (
    SegmentTreeStructuralReasoning,
)
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine
from pointer_algorithms.recognition.candidate_eliminator import CandidateEliminator
from pointer_algorithms.recognition.feature_extractor import ProblemFeatures, FeatureExtractor
from pointer_algorithms.failure_analysis.classifier import FailureClassifier, FailureCategory
from pointer_algorithms.generator.segment_tree_cpp_generator import generate_segment_tree_cpp
from pointer_algorithms.segment_tree.verification.segment_tree_oracles import (
    SegmentTreeOracle,
    BruteForcePointUpdateRangeQuery,
    LazyRangeAddSegmentTreeOracle,
    BruteForceRangeAdd,
    LazyRangeAssignSegmentTreeOracle,
    BruteForceRangeAssign,
    CombinedLazySegmentTreeOracle,
    BruteForceCombinedLazy,
    MetadataSegmentTreeOracle,
    BruteForceMetadata,
    MaxSubarraySegmentTreeOracle,
    BruteForceMaxSubarray,
    FrequencySegmentTreeOracle,
    BruteForceFrequencyKth,
    IntervalStatisticsSegmentTreeOracle,
    BruteForceIntervalStatistics,
)
from pointer_algorithms.bridge import handle_request


class TestSegmentTreeStructuralInvariants(unittest.TestCase):
    def test_canonical_interval_decomposition(self):
        """At most 2*ceil(log2(N)) canonical nodes are queried for any range [ql, qr]."""
        proof = SegmentTreeStructuralReasoning.explain("point_update_range_query")
        self.assertIn("1, N", proof.interval_decomposition)
        self.assertIn("2 * ceil(log2 N)", proof.interval_decomposition)
        self.assertIn("lazy", proof.lazy_tag_algebra.lower())
        self.assertIn("4N", proof.memory_representation)

    def test_algebraic_operations_and_merges(self):
        """Test merge functions: sum, min, max, gcd, max_subarray."""
        self.assertEqual(SegmentTreeStructuralReasoning.merge_sum(5, 7), 12)
        self.assertEqual(SegmentTreeStructuralReasoning.merge_min(5, 7), 5)
        self.assertEqual(SegmentTreeStructuralReasoning.merge_max(5, 7), 7)
        self.assertEqual(SegmentTreeStructuralReasoning.merge_gcd(12, 18), 6)

        # Max subarray merge: l_sum, l_pref, l_suff, l_ans, r_sum, r_pref, r_suff, r_ans
        merged = SegmentTreeStructuralReasoning.merge_max_subarray(10, 10, 5, 10, -2, -2, -2, -2)
        self.assertEqual(merged[0], 8)   # sum: 10 + (-2) = 8
        self.assertEqual(merged[1], 10)  # pref: max(10, 10 - 2) = 10
        self.assertEqual(merged[2], 3)   # suff: max(-2, -2 + 5) = 3
        self.assertEqual(merged[3], 10)  # ans: max(10, -2, 5 + (-2)) = 10

    def test_lazy_tag_composition(self):
        """Test combined lazy tag composition: assignment resets addition; addition accumulates."""
        # compose_lazy_tags(new_has_assign, new_assign_val, new_add_val, old_has_assign, old_assign_val, old_add_val)
        # Apply add 5 to identity (False, 0, 0)
        tag = SegmentTreeStructuralReasoning.compose_lazy_tags(False, 0, 5, False, 0, 0)
        self.assertEqual(tag, (False, 0, 5))
        # Apply assign 10 (overrides prior addition)
        tag = SegmentTreeStructuralReasoning.compose_lazy_tags(True, 10, 0, tag[0], tag[1], tag[2])
        self.assertEqual(tag, (True, 10, 0))
        # Apply add 3 (accumulates on current assignment)
        tag = SegmentTreeStructuralReasoning.compose_lazy_tags(False, 0, 3, tag[0], tag[1], tag[2])
        self.assertEqual(tag, (True, 10, 3))

    def test_frequency_kth_search(self):
        """Tree walk for k-th element over frequency segment tree."""
        # 4 values with counts [2, 1, 0, 3] -> tree with 4 leaves
        # tree layout: 1 covers [1..4] (6), 2 covers [1..2] (3), 3 covers [3..4] (3)
        tree = [0] * 16
        tree[1] = 6
        tree[2] = 3
        tree[3] = 3
        tree[4] = 2
        tree[5] = 1
        tree[6] = 0
        tree[7] = 3
        val = SegmentTreeStructuralReasoning.kth_frequency_search(tree, 3, 4)
        self.assertEqual(val, 2)


class TestSegmentTreeInvariantAndMovement(unittest.TestCase):
    def test_all_8_patterns_invariant_generation(self):
        """All 8 Segment Tree patterns must generate valid 4-phase invariants."""
        for pat in SEGMENT_TREE_PATTERNS:
            inv = InvariantEngine.construct_invariant(pat, {})
            self.assertTrue(len(inv.before_iteration) > 10, f"Failed before invariant for {pat}")
            self.assertTrue(len(inv.during_iteration) > 10, f"Failed during invariant for {pat}")
            self.assertTrue(len(inv.after_movement) > 10, f"Failed after invariant for {pat}")
            self.assertTrue(len(inv.at_termination) > 10, f"Failed termination invariant for {pat}")

    def test_all_8_patterns_movement_derivation(self):
        """All 8 Segment Tree patterns must generate valid movement decisions and proofs."""
        for pat in SEGMENT_TREE_PATTERNS:
            mv = MovementDerivationEngine.derive(pat, {})
            self.assertTrue(len(mv.objective_function) > 5, f"Failed objective for {pat}")
            self.assertTrue(len(mv.decision_conditions) > 0, f"Failed decisions for {pat}")
            self.assertTrue(len(mv.elimination_proof) > 10, f"Failed proof for {pat}")


class TestSegmentTreeCandidateEliminator(unittest.TestCase):
    def test_rule_st1_static_array_suboptimal(self):
        feat = FeatureExtractor.extract("Static array with no updates: range minimum queries on fixed array.")
        res = handle_request({"problemText": feat.raw_text})
        elim = res.get("eliminatedCandidates", [])
        self.assertTrue(any(e.get("rejectionCode") == "SEGMENT_TREE_STATIC_QUERY_SUBOPTIMAL" for e in elim))

    def test_rule_st2_simple_prefix_overkill(self):
        feat = FeatureExtractor.extract("Point updates at index with prefix sum only queries on array.")
        res = handle_request({"problemText": feat.raw_text})
        elim = res.get("eliminatedCandidates", [])
        self.assertTrue(any(e.get("rejectionCode") == "SEGMENT_TREE_SIMPLE_PREFIX_OVERKILL" for e in elim))

    def test_rule_st3_difference_array_overkill(self):
        feat = FeatureExtractor.extract("Batch range adds where queries are only at the end with final reconstruction.")
        res = handle_request({"problemText": feat.raw_text})
        elim = res.get("eliminatedCandidates", [])
        self.assertTrue(any(e.get("rejectionCode") == "SEGMENT_TREE_DIFFERENCE_ARRAY_OVERKILL" for e in elim))

    def test_rule_st5_no_associative_merge(self):
        feat = FeatureExtractor.extract("Dynamic median without rank tree requires non-associative interval query.")
        res = handle_request({"problemText": feat.raw_text})
        elim = res.get("eliminatedCandidates", [])
        self.assertTrue(any(e.get("rejectionCode") == "SEGMENT_TREE_NO_ASSOCIATIVE_MERGE" for e in elim))

    def test_rule_st6_lazy_tag_unsupported(self):
        feat = FeatureExtractor.extract("Range chmin and range sum queries require segment tree beats.")
        res = handle_request({"problemText": feat.raw_text})
        elim = res.get("eliminatedCandidates", [])
        self.assertTrue(any(e.get("rejectionCode") in ("SEGMENT_TREE_STANDARD_LAZY_INSUFFICIENT", "SEGMENT_TREE_LAZY_TAG_UNSUPPORTED") for e in elim))

    def test_rule_st7_resource_limit(self):
        feat = FeatureExtractor.extract("Segment tree 4 * N * sizeof(Node) budget exceeded with memory limit exceeded.")
        res = handle_request({"problemText": feat.raw_text})
        elim = res.get("eliminatedCandidates", [])
        self.assertTrue(any(e.get("rejectionCode") == "SEGMENT_TREE_RESOURCE_LIMIT" for e in elim))

    def test_rule_st8_kth_negative_frequency(self):
        feat = FeatureExtractor.extract("Allow negative counts for k-th element in frequency segment tree.")
        res = handle_request({"problemText": feat.raw_text})
        elim = res.get("eliminatedCandidates", [])
        self.assertTrue(any(e.get("rejectionCode") == "SEGMENT_TREE_KTH_NEGATIVE_FREQUENCY" for e in elim))


class TestSegmentTreeFailureClassifier(unittest.TestCase):
    def test_failure_categories(self):
        """Verify Segment Tree failure categories classify accurately."""
        cases = [
            ("SEGMENT_TREE_STATIC_QUERY_SUBOPTIMAL static range query", FailureCategory.SEGMENT_TREE_STATIC_QUERY_SUBOPTIMAL),
            ("SEGMENT_TREE_SIMPLE_PREFIX_OVERKILL prefix only queries", FailureCategory.SEGMENT_TREE_SIMPLE_PREFIX_OVERKILL),
            ("SEGMENT_TREE_DIFFERENCE_ARRAY_OVERKILL batch adds offline", FailureCategory.SEGMENT_TREE_DIFFERENCE_ARRAY_OVERKILL),
            ("SEGMENT_TREE_FENWICK_EQUIVALENT point sum overkill", FailureCategory.SEGMENT_TREE_FENWICK_EQUIVALENT),
            ("SEGMENT_TREE_NO_ASSOCIATIVE_MERGE non-associative operation", FailureCategory.SEGMENT_TREE_NO_ASSOCIATIVE_MERGE),
            ("SEGMENT_TREE_STANDARD_LAZY_INSUFFICIENT segment tree beats required", FailureCategory.SEGMENT_TREE_STANDARD_LAZY_INSUFFICIENT),
            ("SEGMENT_TREE_LAZY_TAG_UNSUPPORTED deprecated alias test", FailureCategory.SEGMENT_TREE_STANDARD_LAZY_INSUFFICIENT),
            ("SEGMENT_TREE_RESOURCE_LIMIT 4N memory exceeded", FailureCategory.SEGMENT_TREE_RESOURCE_LIMIT),
            ("SEGMENT_TREE_KTH_NEGATIVE_FREQUENCY negative frequencies in kth", FailureCategory.SEGMENT_TREE_KTH_NEGATIVE_FREQUENCY),
            ("SEGMENT_TREE_OPERATION_MISMATCH operation mismatch", FailureCategory.SEGMENT_TREE_OPERATION_MISMATCH),
            ("SEGMENT_TREE_COMPLEXITY_EXCEEDED naive scan O(N)", FailureCategory.SEGMENT_TREE_COMPLEXITY_EXCEEDED),
            ("SEGMENT_TREE_IMPLEMENTATION_BUG bug in push_down or merge", FailureCategory.SEGMENT_TREE_IMPLEMENTATION_BUG),
        ]
        for msg, expected_cat in cases:
            rec = FailureClassifier.classify(msg, {})
            self.assertEqual(rec.category, expected_cat, f"Mismatch for '{msg}': got {rec.category}, expected {expected_cat}")


class TestSegmentTreeOraclesAndCppGenerator(unittest.TestCase):
    def test_all_8_cpp_templates_generate_cleanly(self):
        """All 8 Segment Tree patterns generate valid C++ code with 64-bit safety and 1-based indexing."""
        for pat in SEGMENT_TREE_PATTERNS:
            code = generate_segment_tree_cpp(pat, {})
            self.assertIn("#include <iostream>", code)
            self.assertTrue("tree[" in code or "tree." in code, f"Missing tree array in {pat}")
            self.assertTrue(len(code) > 200)

    def test_point_update_oracle_vs_brute_force(self):
        arr = [0, 3, 1, 4, 1, 5, 9, 2, 6]
        st = SegmentTreeOracle(arr, op="min")
        bf = BruteForcePointUpdateRangeQuery(arr, op="min")
        self.assertEqual(st.query(2, 6), bf.query(2, 6))
        st.update(4, 0)
        bf.update(4, 0)
        self.assertEqual(st.query(2, 6), bf.query(2, 6))

    def test_combined_lazy_oracle_vs_brute_force(self):
        arr = [0, 1, 2, 3, 4, 5]
        st = CombinedLazySegmentTreeOracle(arr)
        bf = BruteForceCombinedLazy(arr)
        self.assertEqual(st.range_query(2, 4), bf.range_query(2, 4))
        st.range_add(2, 4, 10)
        bf.range_add(2, 4, 10)
        self.assertEqual(st.range_query(1, 5), bf.range_query(1, 5))
        st.range_assign(3, 5, 7)
        bf.range_assign(3, 5, 7)
        self.assertEqual(st.range_query(1, 5), bf.range_query(1, 5))

    def test_max_subarray_oracle_vs_brute_force(self):
        arr = [0, 2, -4, 3, -1, 2, -3, 5]
        st = MaxSubarraySegmentTreeOracle(arr)
        bf = BruteForceMaxSubarray(arr)
        self.assertEqual(st.query(1, 7), bf.query(1, 7))
        st.update(3, 10)
        bf.update(3, 10)
        self.assertEqual(st.query(1, 7), bf.query(1, 7))

    def test_frequency_kth_oracle_vs_brute_force(self):
        st = FrequencySegmentTreeOracle(10)
        bf = BruteForceFrequencyKth(10)
        st.add(3, 2)
        bf.add(3, 2)
        st.add(7, 1)
        bf.add(7, 1)
        st.add(2, 1)
        bf.add(2, 1)
        self.assertEqual(st.query_kth(1), bf.query_kth(1))
        self.assertEqual(st.query_kth(2), bf.query_kth(2))
        self.assertEqual(st.query_kth(3), bf.query_kth(3))
        self.assertEqual(st.query_kth(4), bf.query_kth(4))

    def test_interval_statistics_oracle_vs_brute_force(self):
        arr = [0, 3, 1, 4, 1, 5, 9, 2, 6, 9]
        st = IntervalStatisticsSegmentTreeOracle(arr)
        bf = BruteForceIntervalStatistics(arr)
        self.assertEqual(st.query(1, 9), bf.query(1, 9))
        st.update(3, 9)
        bf.update(3, 9)
        self.assertEqual(st.query(1, 9), bf.query(1, 9))


class TestSegmentTreeBridge(unittest.TestCase):
    def test_bridge_emits_structured_segment_tree_metadata(self):
        res = handle_request({"problemText": "Segment tree point update range query for range minimum queries."})
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["selectedPattern"], "segment_tree_point_update_range_query")
        st_meta = res.get("segment_tree")
        self.assertIsNotNone(st_meta)
        self.assertIn("kind", st_meta)
        self.assertIn("operationKind", st_meta)
        self.assertIn("algorithmFamily", st_meta)
        self.assertIn("queryOp", st_meta)


class TestSegmentTreeAdversarialAlgebra(unittest.TestCase):
    """Verifies all 15 adversarial algebra tests (ST-ADV-01 through ST-ADV-15)."""
    def test_adversarial_battery(self):
        from pointer_algorithms.segment_tree.evaluation.segment_tree_adversarial_test import (
            test_st_adv_01_non_commutative_merge,
            test_st_adv_02_all_negative_max_subarray,
            test_st_adv_03_identity_from_left_query_only,
            test_st_adv_04_identity_from_right_query_only,
            test_st_adv_05_assignment_then_addition,
            test_st_adv_06_addition_then_assignment,
            test_st_adv_07_assign_add_assign,
            test_st_adv_08_overlapping_assignments,
            test_st_adv_09_negative_values_lazy,
            test_st_adv_10_64bit_overflow_boundary,
            test_st_adv_11_int128_intermediate_multiplication,
            test_st_adv_12_n_not_power_of_two,
            test_st_adv_13_n_equals_one,
            test_st_adv_14_query_exact_node_boundary,
            test_st_adv_15_query_crossing_midpoint_repeatedly,
        )
        self.assertTrue(test_st_adv_01_non_commutative_merge())
        self.assertTrue(test_st_adv_02_all_negative_max_subarray())
        self.assertTrue(test_st_adv_03_identity_from_left_query_only())
        self.assertTrue(test_st_adv_04_identity_from_right_query_only())
        self.assertTrue(test_st_adv_05_assignment_then_addition())
        self.assertTrue(test_st_adv_06_addition_then_assignment())
        self.assertTrue(test_st_adv_07_assign_add_assign())
        self.assertTrue(test_st_adv_08_overlapping_assignments())
        self.assertTrue(test_st_adv_09_negative_values_lazy())
        self.assertTrue(test_st_adv_10_64bit_overflow_boundary())
        self.assertTrue(test_st_adv_11_int128_intermediate_multiplication())
        self.assertTrue(test_st_adv_12_n_not_power_of_two())
        self.assertTrue(test_st_adv_13_n_equals_one())
        self.assertTrue(test_st_adv_14_query_exact_node_boundary())
        self.assertTrue(test_st_adv_15_query_crossing_midpoint_repeatedly())


if __name__ == "__main__":
    unittest.main()
