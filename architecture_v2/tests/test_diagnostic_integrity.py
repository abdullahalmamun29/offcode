"""
Diagnostic Integrity Tests for Architecture V2.

Verifies that diagnostic output is truthful, complete, and contains only
verified structural facts, explicit rules, traceable dependencies, and evaluated proof obligations.
"""

import unittest
from architecture_v2.semantic_model import (
    ProblemModel, Fact, FactStatus, SelectionKind, SelectionModel,
    ObjectiveKind, ObjectiveModel, ConstraintModel
)
from architecture_v2.semantic_adapter import SemanticAdapter
from architecture_v2.planner import AlgorithmPlannerV2, PlanStatus
from architecture_v2.diagnostics import DiagnosticTracer
from architecture_v2.bridge_v2 import BridgeV2


class TestDiagnosticIntegrity(unittest.TestCase):

    def setUp(self):
        self.bridge = BridgeV2()

    def test_diagnostic_trace_completeness_and_truthfulness(self):
        text = "Find two distinct elements in the array whose sum equals target. Return their 1-based indices."
        res = self.bridge.solve(text)

        trace = res["reasoning"]

        # Check required sections in trace
        self.assertIn("PROBLEM UNDERSTANDING", trace)
        self.assertIn("CONSTRAINT MODEL", trace)
        self.assertIn("SEMANTIC EVIDENCE", trace)
        self.assertIn("DERIVED FACTS & TRACE", trace)
        self.assertIn("REQUIRED OPERATIONS", trace)
        self.assertIn("STRUCTURAL PROPERTIES", trace)
        self.assertIn("CANDIDATES", trace)
        self.assertIn("PROOF OBLIGATIONS", trace)
        self.assertIn("IMPLEMENTATION PLAN", trace)
        self.assertIn("FINAL DECISION", trace)

        # Verify derived fact provenance is reported with rules and dependencies
        self.assertIn("Rule: FixedCardinalityPairSum", trace)
        self.assertIn("Dependencies: (selection.cardinality, relation.kind)", trace)

        # Verify proof obligations are truthfully listed as PROVEN
        self.assertIn("✓ selection_cardinality_is_2: PROVEN", trace)
        self.assertIn("✓ relation_is_sum: PROVEN", trace)
        self.assertIn("✓ original_indices_preserved: PROVEN", trace)

        # Verify structured diagnosticTrace
        diag_items = res["diagnosticTrace"]
        self.assertIsInstance(diag_items, list)
        self.assertGreater(len(diag_items), 0)

        # Find knapsack decision in diagnostic items
        knapsack_entry = next((d for d in diag_items if d["candidate"] == "knapsack_01"), None)
        self.assertIsNotNone(knapsack_entry)
        self.assertEqual(knapsack_entry["status"], "REJECTED")
        self.assertIn("SELECTION_MODEL_MISMATCH", knapsack_entry["reasons"])

    def test_diagnostic_reports_unsupported_composition(self):
        text = "Customers arrive one after another. Find largest ticket price <= x and delete it."
        res = self.bridge.solve(text)

        self.assertEqual(res["status"], "unsupported")
        self.assertIn("COMPOSITION_UNSUPPORTED", res["limitationMessage"])

        trace = res["reasoning"]
        self.assertIn("COMPOSITION", trace)
        self.assertIn("COMPOSITION_UNSUPPORTED", trace)
        self.assertIn("dynamic_collection", trace)

    def test_semantic_model_validation_layer(self):
        # Test valid model
        text = "Find two elements with sum equal to target."
        model = SemanticAdapter.parse(text)
        val = model.validate()
        self.assertTrue(val.is_valid)
        self.assertEqual(len(val.errors), 0)

        # Test invalid model (negative constraint)
        invalid_model = ProblemModel(raw_text="invalid test")
        invalid_model.constraints.n = -5
        invalid_model.constraints.memory_limit_mb = -10
        val_inv = invalid_model.validate()
        self.assertFalse(val_inv.is_valid)
        self.assertIn("Constraint N cannot be negative", val_inv.errors)
        self.assertIn("Memory limit must be positive", val_inv.errors)

        # Test invalid model (contradictory selection: ARBITRARY_SUBSET with fixed cardinality 2)
        contradictory_model = ProblemModel(raw_text="contradictory test")
        contradictory_model.selection = SelectionModel(SelectionKind.ARBITRARY_SUBSET, cardinality=2)
        val_contra = contradictory_model.validate()
        self.assertFalse(val_contra.is_valid)
        self.assertIn("Selection cannot be both ARBITRARY_SUBSET and fixed cardinality 2", val_contra.errors)


if __name__ == "__main__":
    unittest.main()
