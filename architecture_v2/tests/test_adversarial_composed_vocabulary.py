"""
Adversarial Composed Vocabulary and Cross-Context Ambiguity Tests for Architecture V2.

Verifies that problems sharing overlapping lexical tokens:
    ["minimum", "sum", "order", "nearest", "query"]
resolve to fundamentally distinct semantic problem models, that ungrounded ambiguity
is preserved rather than collapsed, and that composition requires strict structural combinations.
"""

import unittest
from architecture_v2.semantic_model import (
    SelectionKind, RelationKind, OperatorKind,
    RequiredOperation, StructuralProperty, HypothesisStatus
)
from architecture_v2.semantic_adapter import SemanticAdapter
from architecture_v2.bridge_v2 import BridgeV2
from architecture_v2.planner import AlgorithmPlannerV2, PlanStatus
from architecture_v2.capability_registry import CapabilityRegistry
from architecture_v2.candidate_eliminator import CandidateEliminatorV2, CandidateStatus


class TestAdversarialComposedVocabulary(unittest.TestCase):

    def setUp(self):
        self.bridge = BridgeV2()
        self.registry = CapabilityRegistry()

    # ── 1. Adversarial Composed Vocabulary Battery ──

    def test_case_1_pair_sum_with_adversarial_vocabulary(self):
        # Contains: minimum, sum, order, nearest, query
        text = (
            "Given an array, process the query: find a pair of two numbers with sum equal to target. "
            "If multiple pairs exist, select the one with minimum 1-based order of indices. "
            "Do not find the nearest element to target or sum arbitrary subsets."
        )
        model = SemanticAdapter.parse(text)

        # Must derive FIXED_CARDINALITY(2) and RelationKind.SUM
        self.assertEqual(model.selection.kind, SelectionKind.FIXED_CARDINALITY)
        self.assertEqual(model.selection.cardinality, 2)
        self.assertTrue(any(r.kind == RelationKind.SUM for r in model.relations))

        # Must derive PAIR_SUM_SEARCH and PAIR_SEARCH
        self.assertIn(RequiredOperation.PAIR_SUM_SEARCH, model.operations)
        self.assertIn(RequiredOperation.PAIR_SEARCH, model.operations)

        # Plan must be PROVEN with two_pointer_pair_sum
        plan = AlgorithmPlannerV2.create_plan(model, self.registry)
        self.assertEqual(plan.status, PlanStatus.PROVEN)
        self.assertEqual(plan.primary_capability, "two_pointer_pair_sum")

    def test_case_2_contiguous_sum_with_adversarial_vocabulary(self):
        # Contains: minimum, sum, order, nearest, query
        text = (
            "Given an array in sorted order, answer each query: find the minimum sum of a "
            "contiguous subarray of size k. Do not find nearest element or pair sum."
        )
        model = SemanticAdapter.parse(text)

        # Must be CONTIGUOUS_SEGMENT, NOT FIXED_CARDINALITY(2)
        self.assertEqual(model.selection.kind, SelectionKind.CONTIGUOUS_SEGMENT)
        self.assertNotEqual(model.selection.kind, SelectionKind.FIXED_CARDINALITY)
        self.assertIn(StructuralProperty.CONTIGUOUS_SELECTION, model.structural_properties)

        # Must NOT derive PAIR_SUM_SEARCH
        self.assertNotIn(RequiredOperation.PAIR_SUM_SEARCH, model.operations)

        # Two-pointer pair sum must be hard-rejected for SELECTION_MODEL_MISMATCH
        tp_decision = CandidateEliminatorV2.evaluate(self.registry.get("two_pointer_pair_sum"), model)
        self.assertEqual(tp_decision.status, CandidateStatus.REJECTED)
        self.assertIn("SELECTION_MODEL_MISMATCH", tp_decision.reasons)

    def test_case_3_arbitrary_subset_sum_with_adversarial_vocabulary(self):
        # Contains: minimum, sum, order, nearest, query
        text = (
            "Given items in given order, for each query find a subset of numbers whose sum "
            "equals target x = 1000000000, minimizing the number of items used. "
            "Do not find nearest value."
        )
        model = SemanticAdapter.parse(text)

        # Must be ARBITRARY_SUBSET, NOT FIXED_CARDINALITY
        self.assertEqual(model.selection.kind, SelectionKind.ARBITRARY_SUBSET)
        self.assertIn(StructuralProperty.ARBITRARY_SUBSET, model.structural_properties)
        self.assertNotIn(RequiredOperation.PAIR_SUM_SEARCH, model.operations)

        # Two-pointer pair sum must be hard-rejected for SELECTION_MODEL_MISMATCH
        tp_decision = CandidateEliminatorV2.evaluate(self.registry.get("two_pointer_pair_sum"), model)
        self.assertEqual(tp_decision.status, CandidateStatus.REJECTED)
        self.assertIn("SELECTION_MODEL_MISMATCH", tp_decision.reasons)

    def test_case_4_bounded_predecessor_with_adversarial_vocabulary(self):
        # Contains: minimum, sum, order, nearest, query
        text = (
            "Process queries in order. For each query, find the maximum ticket price not exceeding x "
            "(nearest valid price <= x), then remove the ticket. "
            "We do not compute minimum element or sum of elements."
        )
        model = SemanticAdapter.parse(text)

        # Must derive PREDECESSOR, DELETE, DYNAMIC_STATE, ORDERED_STATE
        self.assertIn(RequiredOperation.PREDECESSOR, model.operations)
        self.assertIn(RequiredOperation.DELETE, model.operations)
        self.assertIn(StructuralProperty.DYNAMIC_STATE, model.structural_properties)
        self.assertIn(StructuralProperty.ORDERED_STATE, model.structural_properties)

        # Must fail closed with COMPOSITION_UNSUPPORTED
        plan = AlgorithmPlannerV2.create_plan(model, self.registry)
        self.assertEqual(plan.status, PlanStatus.COMPOSITION_UNSUPPORTED)
        self.assertEqual(plan.strategy_name, "dynamic_ordered_multiset_predecessor")

    # ── 2. Cross-Context Ambiguity Tests ──

    def test_nearest_alone_remains_ambiguous(self):
        text = "Find the nearest value to x in the collection."
        model = SemanticAdapter.parse(text)

        # "nearest" without directional inequality or graph context must remain AMBIGUOUS
        self.assertIn("nearest", model.hypotheses)
        self.assertEqual(model.hypotheses["nearest"].status, HypothesisStatus.AMBIGUOUS)
        self.assertIn("nearest_semantics", model.uncertainty)

        # Must NOT derive PREDECESSOR or SUCCESSOR
        self.assertNotIn(RequiredOperation.PREDECESSOR, model.operations)
        self.assertNotIn(RequiredOperation.SUCCESSOR, model.operations)

    def test_nearest_graph_node_disambiguation(self):
        text = "Find the nearest node in the graph connected by edges."
        model = SemanticAdapter.parse(text)

        self.assertIn("nearest", model.hypotheses)
        self.assertEqual(model.hypotheses["nearest"].status, HypothesisStatus.CONFIRMED)
        self.assertEqual(model.hypotheses["nearest"].value, "graph_shortest_path")

    def test_largest_bounded_derives_predecessor(self):
        text = "Find the largest element not exceeding x."
        model = SemanticAdapter.parse(text)

        self.assertIn(RequiredOperation.PREDECESSOR, model.operations)
        self.assertNotIn(RequiredOperation.SUCCESSOR, model.operations)

    def test_smallest_bounded_derives_successor(self):
        text = "Find the smallest element greater than or equal to x."
        model = SemanticAdapter.parse(text)

        self.assertIn(RequiredOperation.SUCCESSOR, model.operations)
        self.assertNotIn(RequiredOperation.PREDECESSOR, model.operations)

    # ── 3. Composition Negative Tests ──

    def test_insufficient_structure_ordered_successor_without_all_elements(self):
        # ORDERED_STATE + SUCCESSOR on a single element search does NOT trigger greedy towers composition
        text = "In a sorted array, find the smallest element >= x."
        model = SemanticAdapter.parse(text)

        self.assertIn(RequiredOperation.SUCCESSOR, model.operations)
        self.assertIn(StructuralProperty.ORDERED_STATE, model.structural_properties)
        self.assertNotIn(StructuralProperty.ALL_ELEMENTS_REQUIRED, model.structural_properties)

        plan = AlgorithmPlannerV2.create_plan(model, self.registry)
        # Should NOT trigger greedy_ordered_successor_placement
        self.assertNotEqual(plan.strategy_name, "greedy_ordered_successor_placement")

    def test_branching_alone_does_not_trigger_backtracking(self):
        model = SemanticAdapter.parse("Explore branches in search space.")
        model.structural_properties.add(StructuralProperty.BRANCHING)

        plan = AlgorithmPlannerV2.create_plan(model, self.registry)
        self.assertNotEqual(plan.strategy_name, "backtracking_search")

    def test_pruning_alone_does_not_trigger_backtracking(self):
        model = SemanticAdapter.parse("Prune infeasible solutions.")
        model.structural_properties.add(StructuralProperty.PRUNING)

        plan = AlgorithmPlannerV2.create_plan(model, self.registry)
        self.assertNotEqual(plan.strategy_name, "backtracking_search")

    def test_complete_backtracking_composition_triggers_backtracking_plan(self):
        model = SemanticAdapter.parse("Search solution space with reversible decisions and pruning.")
        model.structural_properties.add(StructuralProperty.REVERSIBLE_DECISIONS)
        model.structural_properties.add(StructuralProperty.BRANCHING)
        model.structural_properties.add(StructuralProperty.PRUNING)

        plan = AlgorithmPlannerV2.create_plan(model, self.registry)
        self.assertEqual(plan.status, PlanStatus.COMPOSITION_UNSUPPORTED)
        self.assertEqual(plan.strategy_name, "backtracking_search")


if __name__ == "__main__":
    unittest.main()
