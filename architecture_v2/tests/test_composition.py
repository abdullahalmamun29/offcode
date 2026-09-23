"""
Unit tests for AlgorithmPlannerV2 and Composition.
"""

import unittest
from architecture_v2.semantic_model import (
    SelectionKind, SelectionModel, ObjectiveKind, ObjectiveModel,
    RelationKind, RelationModel, RequiredOperation, StructuralProperty,
    ConstraintModel, ProblemModel
)
from architecture_v2.planner import AlgorithmPlannerV2, PlanStatus


class TestPlannerAndComposition(unittest.TestCase):

    def test_2sum_plan_generation(self):
        pm = ProblemModel(raw_text="Find two numbers summing to target. Output 1-based indices.")
        pm.selection = SelectionModel(SelectionKind.FIXED_CARDINALITY, 2)
        pm.relations = [RelationModel(RelationKind.SUM)]
        pm.output_spec = {"type": "ORIGINAL_INDICES"}
        pm.operations = {RequiredOperation.PAIR_SUM_SEARCH, RequiredOperation.PAIR_SEARCH}

        plan = AlgorithmPlannerV2.create_plan(pm)
        self.assertEqual(plan.status, PlanStatus.PROVEN)
        self.assertEqual(plan.primary_capability, "two_pointer_pair_sum")
        self.assertIsNotNone(plan.code)
        self.assertIn("while (lo < hi)", plan.code)
        self.assertIn("vector<pair<long long, int>>", plan.code)
        self.assertIn("All pairs outside pointer interval", plan.invariant)

    def test_towers_fail_closed_composition_unsupported(self):
        pm = ProblemModel(raw_text="Towers problem: place cubes on towers, minimize towers.")
        pm.selection = SelectionModel(SelectionKind.ALL_ELEMENTS)
        pm.objective = ObjectiveModel(ObjectiveKind.MINIMIZE, target_property="towers")
        pm.operations = {RequiredOperation.SUCCESSOR}
        pm.structural_properties = {StructuralProperty.ORDERED_STATE, StructuralProperty.SUCCESSOR_QUERY}

        plan = AlgorithmPlannerV2.create_plan(pm)
        self.assertEqual(plan.status, PlanStatus.COMPOSITION_UNSUPPORTED)
        self.assertIsNone(plan.code)
        self.assertIn("COMPOSITION_UNSUPPORTED", plan.rejection_reasons[0])

    def test_concert_tickets_fail_closed_composition_unsupported(self):
        pm = ProblemModel(raw_text="Find largest ticket price <= x and delete it from available tickets.")
        pm.operations = {RequiredOperation.PREDECESSOR, RequiredOperation.DELETE}
        pm.structural_properties = {StructuralProperty.DYNAMIC_STATE, StructuralProperty.ORDERED_STATE}

        plan = AlgorithmPlannerV2.create_plan(pm)
        self.assertEqual(plan.status, PlanStatus.COMPOSITION_UNSUPPORTED)
        self.assertIsNone(plan.code)
        self.assertIn("COMPOSITION_UNSUPPORTED", plan.rejection_reasons[0])

    def test_sliding_xor_fail_closed_composition_unsupported(self):
        pm = ProblemModel(raw_text="Calculate sliding window XOR.")
        pm.selection = SelectionModel(SelectionKind.CONTIGUOUS_SEGMENT)
        pm.relations = [RelationModel(RelationKind.EQUALITY, operator=RelationKind.SUM)]  # operator XOR
        from architecture_v2.semantic_model import OperatorKind
        pm.relations[0].operator = OperatorKind.XOR
        pm.operations = {RequiredOperation.RANGE_AGGREGATE}

        plan = AlgorithmPlannerV2.create_plan(pm)
        self.assertEqual(plan.status, PlanStatus.COMPOSITION_UNSUPPORTED)
        self.assertIsNone(plan.code)
        self.assertIn("COMPOSITION_UNSUPPORTED", plan.rejection_reasons[0])


if __name__ == "__main__":
    unittest.main()
