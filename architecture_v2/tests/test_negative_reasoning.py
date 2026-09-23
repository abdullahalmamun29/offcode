"""
Negative Reasoning and Candidate Elimination Tests for Architecture V2.

Verifies that incompatible algorithm candidates are rejected for explicit,
verifiable structural reasons and that soft evidence / priors never override hard contradictions.
"""

import unittest
from architecture_v2.semantic_adapter import SemanticAdapter
from architecture_v2.capability_registry import CapabilityRegistry
from architecture_v2.candidate_eliminator import CandidateEliminatorV2, CandidateStatus
from architecture_v2.bridge_v2 import BridgeV2


class TestNegativeReasoning(unittest.TestCase):

    def setUp(self):
        self.registry = CapabilityRegistry()
        self.bridge = BridgeV2(self.registry)

    def test_knapsack_rejected_on_2sum(self):
        text = "Find two distinct numbers in the array whose sum equals target x = 1000000000."
        model = SemanticAdapter.parse(text)

        knapsack_cap = self.registry.get("knapsack_01")
        self.assertIsNotNone(knapsack_cap)

        decision = CandidateEliminatorV2.evaluate(knapsack_cap, model)
        self.assertEqual(decision.status, CandidateStatus.REJECTED)

        # Must be rejected for structural mismatch
        self.assertIn("SELECTION_MODEL_MISMATCH", decision.reasons)
        self.assertIn("CARDINALITY_MISMATCH", decision.reasons)
        self.assertIn("MEMORY_INFEASIBLE", decision.reasons)

        # Check why_not output
        explanation = self.bridge.why_not(text, "knapsack_01")
        self.assertIn("SELECTION_MODEL_MISMATCH", explanation)
        self.assertIn("CARDINALITY_MISMATCH", explanation)
        self.assertIn("MEMORY_INFEASIBLE", explanation)

    def test_subset_sum_dp_rejected_on_2sum(self):
        text = "Find two numbers with sum equal to target x = 1000000000."
        model = SemanticAdapter.parse(text)

        subset_cap = self.registry.get("subset_sum_dp")
        self.assertIsNotNone(subset_cap)

        decision = CandidateEliminatorV2.evaluate(subset_cap, model)
        self.assertEqual(decision.status, CandidateStatus.REJECTED)
        self.assertIn("SELECTION_MODEL_MISMATCH", decision.reasons)
        self.assertIn("CARDINALITY_MISMATCH", decision.reasons)
        self.assertIn("MEMORY_INFEASIBLE", decision.reasons)

    def test_trie_rejected_on_sliding_xor(self):
        text = "Calculate bitwise XOR of numbers in a sliding window of size k."
        model = SemanticAdapter.parse(text)

        trie_cap = self.registry.get("trie_max_xor")
        self.assertIsNotNone(trie_cap)

        decision = CandidateEliminatorV2.evaluate(trie_cap, model)
        self.assertEqual(decision.status, CandidateStatus.REJECTED)

        # Missing pairwise relation and pair search operation
        self.assertIn("MISSING_STRUCTURAL_PROPERTY_PAIRWISE_RELATION", decision.reasons)
        self.assertIn("operation_PAIR_SEARCH", decision.missing_requirements)

        explanation = self.bridge.why_not(text, "trie_max_xor")
        self.assertIn("MISSING_STRUCTURAL_PROPERTY_PAIRWISE_RELATION", explanation)
        self.assertIn("operation_PAIR_SEARCH", explanation)

    def test_two_pointer_rejected_on_knapsack_problem(self):
        text = "Find a subset of items that maximizes total value without exceeding capacity."
        model = SemanticAdapter.parse(text)

        tp_cap = self.registry.get("two_pointer_pair_sum")
        self.assertIsNotNone(tp_cap)

        decision = CandidateEliminatorV2.evaluate(tp_cap, model)
        self.assertEqual(decision.status, CandidateStatus.REJECTED)
        self.assertIn("SELECTION_MODEL_MISMATCH", decision.reasons)

        explanation = self.bridge.why_not(text, "two_pointer_pair_sum")
        self.assertIn("SELECTION_MODEL_MISMATCH", explanation)

    def test_why_not_accepted_candidate(self):
        text = "Find two numbers that sum to target."
        explanation = self.bridge.why_not(text, "two_pointer_pair_sum")
        self.assertIn("Status: ACCEPTED", explanation)
        self.assertIn("Candidate satisfies all preconditions", explanation)

    def test_why_not_unknown_candidate(self):
        text = "Find two numbers that sum to target."
        explanation = self.bridge.why_not(text, "non_existent_algorithm")
        self.assertIn("not registered", explanation)


if __name__ == "__main__":
    unittest.main()
