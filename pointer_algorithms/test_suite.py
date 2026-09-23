"""
Comprehensive Python Test Suite for Pointer-Based Algorithms Domain.

Tests:
1. Convergence Simulation & Oracles (Pair sum, Container with most water)
2. Compaction Simulation & Property Tests (Remove duplicates)
3. Sliding Window Simulation & Oracles (Fixed, Variable min, Variable max)
4. Partition Pointers (Dutch national flag 3-way)
5. Fast/Slow Pointers (Cycle detection)
6. Metamorphic Testing (Scaling invariance for pair sum & container)
7. Monotonicity Engine (Value order, window validity, negative breaking)
8. Knowledge Induction & Cross-Problem Promotion
9. Rejection of Negative Problems
10. Failure Classifier & Hypothesis Generator
"""

import unittest
from pointer_algorithms.simulation.simulator import PointerSimulator
from pointer_algorithms.verification.brute_force_oracles import BruteForceOracles
from pointer_algorithms.verification.property_tests import PropertyVerifier
from pointer_algorithms.verification.metamorphic_tests import MetamorphicTester
from pointer_algorithms.reasoning.monotonicity_engine import MonotonicityEngine, MonotonicityStatus
from pointer_algorithms.knowledge.knowledge_store import KnowledgeStore, ConfidenceLevel
from pointer_algorithms.learning.induction import KnowledgeInductionEngine
from pointer_algorithms.learning.knowledge_update import KnowledgeUpdateManager
from pointer_algorithms.failure_analysis.classifier import FailureClassifier, FailureCategory
from pointer_algorithms.failure_analysis.repair_hypothesis import RepairHypothesisGenerator
from pointer_algorithms.bridge import handle_request
from pointer_algorithms.fast_slow.fast_slow import ListNode

class TestPointerAlgorithms(unittest.TestCase):

    def test_pair_sum_simulation_vs_oracle(self):
        arr = [1, 3, 5, 8, 12, 19]
        target = 13
        sim_res = PointerSimulator.simulate("pair_sum_sorted", arr, {"target": target})
        oracle_res = BruteForceOracles.pair_sum_sorted(arr, target)
        self.assertTrue(sim_res["success"])
        self.assertEqual(sim_res["result"], oracle_res)
        self.assertTrue(PropertyVerifier.verify_valid_pair_sum(arr, sim_res["result"], target))

    def test_container_most_water_simulation_vs_oracle(self):
        heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
        sim_res = PointerSimulator.simulate("container_most_water", heights, {})
        oracle_res = BruteForceOracles.container_most_water(heights)
        self.assertEqual(sim_res["max_area"], oracle_res)
        self.assertEqual(sim_res["max_area"], 49)

    def test_in_place_compaction_multiset(self):
        arr = [1, 1, 2, 2, 3, 4, 4, 5]
        sim_res = PointerSimulator.simulate("remove_duplicates_sorted", arr, {})
        oracle_res = BruteForceOracles.remove_duplicates(arr)
        self.assertEqual(sim_res["compacted_array"], oracle_res)
        self.assertTrue(PropertyVerifier.verify_in_place_compaction(arr, sim_res["compacted_array"]))

    def test_sliding_window_fixed_vs_oracle(self):
        arr = [2, 1, 5, 1, 3, 2]
        k = 3
        sim_res = PointerSimulator.simulate("sliding_window_fixed", arr, {"k": k})
        oracle_res = BruteForceOracles.sliding_window_fixed_max(arr, k)
        self.assertEqual(sim_res["max_sum"], oracle_res)
        self.assertEqual(sim_res["max_sum"], 9)

    def test_sliding_window_variable_min_vs_oracle(self):
        arr = [2, 3, 1, 2, 4, 3]
        target = 7
        sim_res = PointerSimulator.simulate("sliding_window_variable_min", arr, {"target": target})
        oracle_res = BruteForceOracles.min_size_subarray_sum(arr, target)
        self.assertEqual(sim_res["min_len"], oracle_res)
        self.assertEqual(sim_res["min_len"], 2)

    def test_sliding_window_variable_max_distinct(self):
        s = "eceba"
        k = 2
        sim_res = PointerSimulator.simulate("sliding_window_variable_max", list(s), {"k_distinct": k})
        oracle_res = BruteForceOracles.longest_substring_k_distinct(s, k)
        self.assertEqual(sim_res["max_len"], oracle_res)
        self.assertEqual(sim_res["max_len"], 3)

    def test_dutch_national_flag_partition(self):
        arr = [2, 0, 2, 1, 1, 0]
        sim_res = PointerSimulator.simulate("partition_dutch_flag", arr, {})
        oracle_res = BruteForceOracles.dutch_national_flag(arr)
        self.assertEqual(sim_res["partitioned_array"], oracle_res)
        self.assertTrue(PropertyVerifier.verify_multiset_conservation(arr, sim_res["partitioned_array"]))
        self.assertTrue(PropertyVerifier.verify_dutch_flag_partition(sim_res["partitioned_array"]))

    def test_fast_slow_cycle_detection(self):
        # Acyclic list
        n1 = ListNode(1)
        n2 = ListNode(2)
        n3 = ListNode(3)
        n1.next = n2
        n2.next = n3
        acyclic_res = PointerSimulator.simulate("linked_cycle_detection", n1, {})
        self.assertFalse(acyclic_res["has_cycle"])

        # Cyclic list
        n3.next = n2
        cyclic_res = PointerSimulator.simulate("linked_cycle_detection", n1, {})
        self.assertTrue(cyclic_res["has_cycle"])

    def test_metamorphic_scaling(self):
        arr = [1, 2, 4, 7, 11, 15]
        target = 15
        self.assertTrue(MetamorphicTester.test_pair_sum_scaling(arr, target, c=5))

        heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
        self.assertTrue(MetamorphicTester.test_container_scaling(heights, c=3))

    def test_monotonicity_engine(self):
        # Non-negative window sum is confirmed
        res_pos = MonotonicityEngine.assess_for_pattern(
            pattern="sliding_window_variable_min",
            has_negative_values=False,
            is_sorted=False,
            can_sort=False,
            is_contiguous=True,
            tracks_distinct=False,
            objective_type="min_length"
        )
        self.assertEqual(res_pos.status, MonotonicityStatus.MONOTONICITY_CONFIRMED)

        # Negative values break sum-based window monotonicity
        res_neg = MonotonicityEngine.assess_for_pattern(
            pattern="sliding_window_variable_min",
            has_negative_values=True,
            is_sorted=False,
            can_sort=False,
            is_contiguous=True,
            tracks_distinct=False,
            objective_type="min_length"
        )
        self.assertEqual(res_neg.status, MonotonicityStatus.MONOTONICITY_BROKEN)
        self.assertEqual(res_neg.broken_reason, "WINDOW_NOT_MONOTONIC_NEGATIVE_SUM")

    def test_induction_and_promotion_gate(self):
        store = KnowledgeStore()
        features = {
            "is_sorted": True,
            "is_contiguous": True,
            "has_negative_values": False,
            "target": 10
        }
        rule = KnowledgeInductionEngine.induce_rule_from_solution(
            problem_id="unit_test_prob",
            pattern_kind="pair_sum_sorted",
            sample_input=[1, 2, 3, 4],
            features=features,
            simulation_result={}
        )
        self.assertEqual(rule.confidence_level, ConfidenceLevel.CANDIDATE)

        promoted, msg, promoted_rule = KnowledgeUpdateManager.attempt_promotion(store, rule)
        self.assertTrue(promoted)
        self.assertEqual(promoted_rule.confidence_level, ConfidenceLevel.VALIDATED)
        self.assertIn("unit_test_prob", promoted_rule.rule_id)

    def test_negative_problem_rejection(self):
        # Subarray sum with negative values must be rejected
        req = {"problemText": "Find shortest contiguous subarray with sum equal to 5 in an array with negative numbers"}
        resp = handle_request(req)
        self.assertEqual(resp["status"], "rejected")
        self.assertEqual(resp["recommendedAlternative"], "prefix_sum_hash_map")

    def test_failure_classification_and_hypothesis(self):
        classification = FailureClassifier.classify("WINDOW_NOT_MONOTONIC_NEGATIVE_SUM", {})
        self.assertEqual(classification.category, FailureCategory.WINDOW_NOT_MONOTONIC)

        hypothesis = RepairHypothesisGenerator.generate(classification, {})
        self.assertEqual(hypothesis.failure_category, FailureCategory.WINDOW_NOT_MONOTONIC)
        self.assertIn("Prefix Sum + Hash Map", hypothesis.recommended_action)

if __name__ == '__main__':
    unittest.main()
