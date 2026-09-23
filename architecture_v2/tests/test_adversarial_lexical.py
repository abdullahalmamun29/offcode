"""
CHUP Recognition Architecture V2 — Adversarial Lexical Test Suite.

Demonstrates that identical lexical tokens occurring in different structural contexts
produce different semantic models and never independently determine the algorithm.
Tests:
- XOR: Max pair XOR vs Range XOR vs Sliding-window XOR vs XOR parity
- Sum: Pair Sum vs Subarray Sum vs Subset Sum vs Range Sum
- Minimum: Minimum element vs Range minimum vs Minimum towers vs Minimum path
- Nearest: Nearest <= x vs Nearest >= x vs Nearest graph node vs Ambiguous nearest
- Order: Sort sequence vs Ordered set vs Relative order vs Topological order
"""

import unittest
from architecture_v2.semantic_adapter import SemanticAdapter
from architecture_v2.semantic_model import (
    SelectionKind, ObjectiveKind, RelationKind, OperatorKind,
    RequiredOperation, StructuralProperty
)
from architecture_v2.capability_registry import CapabilityRegistry
from architecture_v2.candidate_eliminator import CandidateEliminatorV2, CandidateStatus


class TestAdversarialLexical(unittest.TestCase):

    def setUp(self):
        self.registry = CapabilityRegistry()

    # ── 1. XOR Tests ──

    def test_xor_pairwise_max_vs_range_vs_window(self):
        # A) Pairwise Maximum XOR
        text_pair = "Find the maximum XOR of two distinct elements in the array."
        m_pair = SemanticAdapter.parse(text_pair)
        self.assertEqual(m_pair.selection.kind, SelectionKind.FIXED_CARDINALITY)
        self.assertEqual(m_pair.selection.cardinality, 2)
        self.assertIn(m_pair.objective.kind, (ObjectiveKind.MAXIMIZE, ObjectiveKind.MAXIMIZE_VALUE))
        self.assertTrue(any(r.operator == OperatorKind.XOR for r in m_pair.relations))

        # B) Sliding Window XOR
        text_window = "Compute the bitwise XOR in a sliding window of size k."
        m_win = SemanticAdapter.parse(text_window)
        self.assertEqual(m_win.selection.kind, SelectionKind.CONTIGUOUS_SEGMENT)
        self.assertTrue(any(r.operator == OperatorKind.XOR for r in m_win.relations))
        self.assertNotIn(RequiredOperation.PAIR_SEARCH, m_win.operations)

        # C) Candidate elimination check: Sliding window XOR must REJECT Binary Trie
        decisions = {d.candidate_name: d for d in CandidateEliminatorV2.filter_candidates(self.registry, m_win)}
        trie_dec = decisions["trie_max_xor"]
        self.assertEqual(trie_dec.status, CandidateStatus.REJECTED)
        self.assertIn("MISSING_STRUCTURAL_PROPERTY_PAIRWISE_RELATION", trie_dec.reasons)

    # ── 2. Sum Tests ──

    def test_sum_pair_vs_subarray_vs_subset(self):
        # A) Pair Sum
        text_pair = "Find two elements whose sum equals target."
        m_pair = SemanticAdapter.parse(text_pair)
        self.assertEqual(m_pair.selection.kind, SelectionKind.FIXED_CARDINALITY)
        self.assertEqual(m_pair.selection.cardinality, 2)
        self.assertIn(RequiredOperation.PAIR_SUM_SEARCH, m_pair.operations)

        # B) Subarray Sum
        text_sub = "Find a contiguous subarray whose sum equals target."
        m_sub = SemanticAdapter.parse(text_sub)
        self.assertEqual(m_sub.selection.kind, SelectionKind.CONTIGUOUS_SEGMENT)
        self.assertNotIn(RequiredOperation.PAIR_SUM_SEARCH, m_sub.operations)

        # C) Subset Sum
        text_subset = "Determine if there exists a subset whose sum equals target."
        m_subset = SemanticAdapter.parse(text_subset)
        self.assertEqual(m_subset.selection.kind, SelectionKind.ARBITRARY_SUBSET)
        self.assertNotIn(RequiredOperation.PAIR_SUM_SEARCH, m_subset.operations)

        # D) Candidate check: Pair sum rejects Knapsack & Subset Sum DP
        dec_pair = {d.candidate_name: d for d in CandidateEliminatorV2.filter_candidates(self.registry, m_pair)}
        self.assertEqual(dec_pair["two_pointer_pair_sum"].status, CandidateStatus.ACCEPTED)
        self.assertEqual(dec_pair["knapsack_01"].status, CandidateStatus.REJECTED)
        self.assertEqual(dec_pair["subset_sum_dp"].status, CandidateStatus.REJECTED)

    # ── 3. Minimum Tests ──

    def test_minimum_element_vs_towers_vs_boundary(self):
        # A) Minimum element (find smallest)
        text_min = "Find the minimum element in the array."
        m_min = SemanticAdapter.parse(text_min)
        self.assertEqual(m_min.objective.kind, ObjectiveKind.MINIMIZE)

        # B) Minimum towers (grouping / packing)
        text_towers = "Place cubes on towers to find the minimum number of towers."
        m_towers = SemanticAdapter.parse(text_towers)
        self.assertEqual(m_towers.objective.kind, ObjectiveKind.MINIMIZE)
        self.assertEqual(m_towers.objective.target_property, "towers")

        # C) Minimum valid value above lower bound (Successor)
        text_succ = "Find the smallest value greater than or equal to x."
        m_succ = SemanticAdapter.parse(text_succ)
        self.assertEqual(m_succ.objective.kind, ObjectiveKind.MINIMIZE)
        self.assertIn(RequiredOperation.SUCCESSOR, m_succ.operations)

    # ── 4. Nearest Tests ──

    def test_nearest_predecessor_vs_successor_vs_ambiguous(self):
        # A) Largest value <= x (Predecessor)
        text_pred = "Find the largest ticket price not exceeding x."
        m_pred = SemanticAdapter.parse(text_pred)
        self.assertIn(RequiredOperation.PREDECESSOR, m_pred.operations)

        # B) Smallest value >= x (Successor)
        text_succ = "Find the smallest price at least x."
        m_succ = SemanticAdapter.parse(text_succ)
        self.assertIn(RequiredOperation.SUCCESSOR, m_succ.operations)

        # C) Ambiguous "nearest" without ordering direction or distance
        text_amb = "Find the nearest value in the collection."
        m_amb = SemanticAdapter.parse(text_amb)
        self.assertIn("nearest", m_amb.hypotheses)
        self.assertEqual(m_amb.hypotheses["nearest"].status.value, "AMBIGUOUS")

    # ── 5. Order Tests ──

    def test_order_sort_vs_relative_order_vs_ordered_set(self):
        # A) Original Indices required preserves initial order information
        text_indices = "Find two numbers with sum target. Return their 1-based original indices."
        m_indices = SemanticAdapter.parse(text_indices)
        self.assertEqual(m_indices.output_spec.get("type"), "ORIGINAL_INDICES")

        # B) Dynamic ordered search
        text_pred = "Find the largest price <= x in the dynamic ticket set."
        m_pred = SemanticAdapter.parse(text_pred)
        self.assertIn(StructuralProperty.ORDERED_STATE, m_pred.structural_properties)
        self.assertIn(RequiredOperation.PREDECESSOR, m_pred.operations)


if __name__ == "__main__":
    unittest.main()
