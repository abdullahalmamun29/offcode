"""
Semantic Generalization Tests for Architecture V2.

Verifies that the semantic reasoning layer generalizes across varied phrasing,
lexical variations, and problem contexts without relying on keyword-to-algorithm mappings.
"""

import unittest
from architecture_v2.semantic_model import (
    SelectionKind, RelationKind, OperatorKind,
    RequiredOperation, StructuralProperty
)
from architecture_v2.semantic_adapter import SemanticAdapter
from architecture_v2.bridge_v2 import BridgeV2
from architecture_v2.planner import PlanStatus


class TestSemanticGeneralization(unittest.TestCase):

    def setUp(self):
        self.bridge = BridgeV2()

    def test_2sum_varied_phrasing_generalization(self):
        phrasings = [
            "Given an array of integers and a value X, find two numbers that sum to X.",
            "Find a pair of cards whose values add up to total T. Return their positions.",
            "Locate two distinct elements adding up to S. Output their 1-based indices.",
            "Given a sequence of numbers, determine if there exist two elements with sum equal to target."
        ]

        for text in phrasings:
            with self.subTest(text=text):
                model = SemanticAdapter.parse(text)
                self.assertEqual(model.selection.kind, SelectionKind.FIXED_CARDINALITY)
                self.assertEqual(model.selection.cardinality, 2)
                self.assertTrue(any(r.kind == RelationKind.SUM for r in model.relations))
                self.assertIn(RequiredOperation.PAIR_SUM_SEARCH, model.operations)

                res = self.bridge.solve(text)
                self.assertEqual(res["status"], "success")
                self.assertIsNotNone(res["code"])
                self.assertIn(res["capability"], ["two_pointer_pair_sum", "hash_pair_sum"])

    def test_dynamic_predecessor_paraphrases(self):
        phrasings = [
            "Customers want tickets with price at most X. When bought, tickets are removed.",
            "Repeatedly find the maximum available number not exceeding bound, then delete it.",
            "For each query x, find largest element <= x and erase it from the collection."
        ]

        for text in phrasings:
            with self.subTest(text=text):
                model = SemanticAdapter.parse(text)
                self.assertIn(RequiredOperation.PREDECESSOR, model.operations)
                self.assertIn(RequiredOperation.DELETE, model.operations)
                self.assertIn(StructuralProperty.DYNAMIC_STATE, model.structural_properties)

                res = self.bridge.solve(text)
                self.assertEqual(res["status"], "unsupported")
                self.assertIn("COMPOSITION_UNSUPPORTED", res["limitationMessage"])

    def test_static_bounded_selection_not_dynamic_predecessor(self):
        phrasings = [
            "Find the largest element in array A that is at most X.",
            "Find the maximum number in a static list not exceeding upper bound B."
        ]

        for text in phrasings:
            with self.subTest(text=text):
                model = SemanticAdapter.parse(text)
                self.assertIn(RequiredOperation.STATIC_BOUNDED_SELECTION, model.operations)
                self.assertNotIn(StructuralProperty.PREDECESSOR_QUERY, model.structural_properties)
                self.assertIn(StructuralProperty.STATIC_BOUNDED_SELECTION, model.structural_properties)

    def test_sliding_window_xor_generalization_no_trie(self):
        phrasings = [
            "Compute XOR sum of elements in each window of size k.",
            "For every contiguous segment of length w, calculate bitwise XOR."
        ]

        for text in phrasings:
            with self.subTest(text=text):
                model = SemanticAdapter.parse(text)
                self.assertEqual(model.selection.kind, SelectionKind.CONTIGUOUS_SEGMENT)
                self.assertTrue(any(r.operator == OperatorKind.XOR for r in model.relations))
                self.assertIn(StructuralProperty.CONTIGUOUS_SELECTION, model.structural_properties)

                res = self.bridge.solve(text)
                self.assertEqual(res["status"], "unsupported")
                self.assertNotEqual(res["capability"], "trie_max_xor")
                self.assertIn("COMPOSITION_UNSUPPORTED", res["limitationMessage"])


if __name__ == "__main__":
    unittest.main()
