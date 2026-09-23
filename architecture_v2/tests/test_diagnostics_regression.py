"""
CHUP Recognition Architecture V2 — Four Mandatory Regression Cases.

Case A: 2-Sum ("target sum") must never select Knapsack DP.
Case B: Towers must produce COMPOSITION_UNSUPPORTED (never an unrelated greedy template).
Case C: Concert Tickets must produce COMPOSITION_UNSUPPORTED (never Graph BFS).
Case D: LCG + Sliding XOR must produce COMPOSITION_UNSUPPORTED (never Binary Trie).
"""

import unittest
from architecture_v2.bridge_v2 import BridgeV2
from architecture_v2.semantic_adapter import SemanticAdapter
from architecture_v2.capability_registry import CapabilityRegistry
from architecture_v2.candidate_eliminator import CandidateEliminatorV2, CandidateStatus


class TestDiagnosticsRegression(unittest.TestCase):

    def setUp(self):
        self.bridge = BridgeV2()

    def test_case_a_2sum_never_selects_knapsack(self):
        text = "Find two elements in the array whose target sum equals x. Return their original indices."
        res = self.bridge.solve(text)

        # 2-Sum must succeed with two_pointer_pair_sum or hash_pair_sum
        self.assertEqual(res["status"], "success")
        self.assertIn(res["selectedPattern"], ("two_pointer_pair_sum", "hash_pair_sum"))

        # Verify that knapsack was explicitly evaluated and rejected in the diagnostic trace
        knapsack_trace = [item for item in res["diagnosticTrace"] if item["candidate"] == "knapsack_01"]
        self.assertTrue(len(knapsack_trace) > 0)
        self.assertEqual(knapsack_trace[0]["status"], "REJECTED")
        self.assertIn("CARDINALITY_MISMATCH", knapsack_trace[0]["reasons"])
        self.assertIn("SELECTION_MODEL_MISMATCH", knapsack_trace[0]["reasons"])

    def test_case_b_towers_fails_closed_never_unrelated_greedy(self):
        text = "You are given n cubes. Build towers by placing each cube on top of an existing tower or starting a new tower. Find the minimum number of towers."
        res = self.bridge.solve(text)

        # Must NOT select an unrelated greedy template (such as interval selection)
        self.assertEqual(res["status"], "unsupported")
        self.assertIsNone(res["code"])
        self.assertIn("COMPOSITION_UNSUPPORTED", res["limitationMessage"])
        self.assertIn("successor", res["reasoning"].lower())

    def test_case_c_concert_tickets_fails_closed_never_graph_bfs(self):
        text = "Customers want to buy concert tickets. For each customer, find the largest ticket price not exceeding customer budget x, and then delete that ticket from the available tickets."
        res = self.bridge.solve(text)

        # Must NOT select Graph BFS
        self.assertEqual(res["status"], "unsupported")
        self.assertIsNone(res["code"])
        self.assertIn("COMPOSITION_UNSUPPORTED", res["limitationMessage"])
        self.assertNotIn("bfs", res["reasoning"].lower())

    def test_case_d_lcg_sliding_xor_fails_closed_never_binary_trie(self):
        text = "Generate numbers using a linear congruential generator (LCG). Maintain a sliding window of size k and compute the bitwise XOR reduction of elements in the window."
        res = self.bridge.solve(text)

        # Must NOT select Binary Trie
        self.assertEqual(res["status"], "unsupported")
        self.assertIsNone(res["code"])
        self.assertIn("COMPOSITION_UNSUPPORTED", res["limitationMessage"])
        # Trie must not be selected
        self.assertNotEqual(res["selectedPattern"], "trie_max_xor")


if __name__ == "__main__":
    unittest.main()
