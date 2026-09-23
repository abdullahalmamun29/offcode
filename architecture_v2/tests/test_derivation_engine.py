"""
Unit tests for DerivationEngine and SemanticAdapter.
"""

import unittest
from architecture_v2.semantic_model import (
    SelectionKind, ObjectiveKind, RelationKind, OperatorKind,
    RequiredOperation, StructuralProperty, FactStatus
)
from architecture_v2.semantic_adapter import SemanticAdapter
from architecture_v2.derivation_engine import DerivationEngine


class TestDerivationAndAdapter(unittest.TestCase):

    def test_2sum_semantic_adapter_and_derivation(self):
        text = "Find two distinct elements in the array whose sum equals target. Return their 1-based indices."
        model = SemanticAdapter.parse(text)

        # Assert selection model
        self.assertEqual(model.selection.kind, SelectionKind.FIXED_CARDINALITY)
        self.assertEqual(model.selection.cardinality, 2)

        # Assert relation
        self.assertTrue(any(r.kind == RelationKind.SUM for r in model.relations))

        # Assert output requirement
        self.assertEqual(model.output_spec.get("type"), "ORIGINAL_INDICES")

        # Assert derived operations
        self.assertIn(RequiredOperation.PAIR_SUM_SEARCH, model.operations)
        self.assertIn(RequiredOperation.PAIR_SEARCH, model.operations)

        # Assert provenance of PAIR_SUM_SEARCH
        fact = model.get_fact("operation.pair_sum_search")
        self.assertIsNotNone(fact)
        self.assertEqual(fact.derivation_rule, "FixedCardinalityPairSum")
        self.assertEqual(fact.dependencies, ["selection.cardinality", "relation.kind"])

    def test_predecessor_derivation(self):
        text = "Find the largest ticket price not exceeding customer budget x. Then remove the ticket."
        model = SemanticAdapter.parse(text)

        # Assert objective & relation
        self.assertEqual(model.objective.kind, ObjectiveKind.MAXIMIZE)
        self.assertTrue(any(r.kind == RelationKind.LESS_EQUAL for r in model.relations))

        # Assert operations: PREDECESSOR and DELETE
        self.assertIn(RequiredOperation.PREDECESSOR, model.operations)
        self.assertIn(RequiredOperation.DELETE, model.operations)

        # Assert derived structural properties
        self.assertIn(StructuralProperty.DYNAMIC_STATE, model.structural_properties)
        self.assertIn(StructuralProperty.ORDERED_STATE, model.structural_properties)

    def test_xor_does_not_trigger_trie_in_adapter(self):
        text = "Calculate bitwise XOR of numbers in sliding window of size k."
        model = SemanticAdapter.parse(text)

        # Operator XOR recognized as operator, NOT as an algorithm!
        self.assertTrue(any(r.operator == OperatorKind.XOR for r in model.relations))
        self.assertEqual(model.selection.kind, SelectionKind.CONTIGUOUS_SEGMENT)
        self.assertIn(StructuralProperty.CONTIGUOUS_SELECTION, model.structural_properties)

        # Must not contain any algorithm name
        for f in model.facts.values():
            self.assertNotIn("trie", f.name.lower())
            self.assertNotIn("trie", str(f.value).lower())

    def test_nearest_ambiguity_tracking(self):
        text = "Find the nearest value in the collection."
        model = SemanticAdapter.parse(text)

        # In absence of bounded relation (<= or >=) or graph context, "nearest" is ambiguous
        self.assertIn("nearest", model.hypotheses)
        self.assertEqual(model.hypotheses["nearest"].status.value, "AMBIGUOUS")
        self.assertIn("nearest_semantics", model.uncertainty)


if __name__ == "__main__":
    unittest.main()
