"""
Test Suite: Generic Fixed-Cardinality Additive Decomposition
Tests architectural invariants for:
  FIXED_CARDINALITY(k) + ADDITIVE_TARGET_RELATION + DISTINCT_SELECTION
emerging from generic multi-fact derivation, anchor + residual decomposition,
proof obligations, and verified C++17 execution.
"""

import unittest
import subprocess
import tempfile
import os
from architecture_v2.semantic_adapter import SemanticAdapter
from architecture_v2.semantic_model import (
    SelectionKind, RelationKind, RequiredOperation, StructuralProperty,
    FactStatus, SemanticScope
)
from architecture_v2.capability_registry import CapabilityRegistry
from architecture_v2.candidate_eliminator import CandidateEliminatorV2, CandidateStatus
from architecture_v2.planner import AlgorithmPlannerV2, PlanStatus
from architecture_v2.bridge_v2 import BridgeV2


class TestFixedCardinalityAdditiveComposition(unittest.TestCase):

    def setUp(self):
        self.registry = CapabilityRegistry()
        self.bridge = BridgeV2(self.registry)

    def test_a_pair_sum_existing_behavior(self):
        """
        Test A — Existing 2-value problem:
        'Find two distinct values whose sum is x.'
        Must establish FIXED_CARDINALITY(2), SUM, PAIR_SUM_SEARCH, and select two_pointer_pair_sum.
        """
        text = "Find two distinct values whose sum is x."
        model = SemanticAdapter.parse(text)

        self.assertEqual(model.selection.kind, SelectionKind.FIXED_CARDINALITY)
        self.assertEqual(model.selection.cardinality, 2)
        self.assertIn(RequiredOperation.PAIR_SUM_SEARCH, model.operations)
        self.assertIn(RequiredOperation.ADDITIVE_TARGET_SEARCH, model.operations)
        self.assertIn(StructuralProperty.FIXED_CARDINALITY, model.structural_properties)

        plan = AlgorithmPlannerV2.create_plan(model, self.registry)
        self.assertEqual(plan.status, PlanStatus.PROVEN)
        self.assertEqual(plan.primary_capability, "two_pointer_pair_sum")

    def test_b_three_values_generic_decomposition(self):
        """
        Test B — Three-value problem:
        'Find three values at distinct positions whose sum is x.'
        Must establish FIXED_CARDINALITY(3), SUM, DISTINCT_SELECTION,
        ADDITIVE_TARGET_SEARCH, DECOMPOSABLE_ADDITIVE_SEARCH, and consider anchor + pair-sum residual.
        """
        text = "Find three values at distinct positions whose sum is x."
        model = SemanticAdapter.parse(text)

        self.assertEqual(model.selection.kind, SelectionKind.FIXED_CARDINALITY)
        self.assertEqual(model.selection.cardinality, 3)
        self.assertTrue(model.selection.distinct_positions)
        self.assertIn(RequiredOperation.ADDITIVE_TARGET_SEARCH, model.operations)
        self.assertIn(StructuralProperty.DECOMPOSABLE_ADDITIVE_SEARCH, model.structural_properties)
        self.assertIn(StructuralProperty.PAIRWISE_DISTINCT_SELECTION, model.structural_properties)

        # Plan must instantiate anchor + residual pair-sum composition
        # When constraints are provided (N <= 5000)
        model.constraints.n = 5000
        plan = AlgorithmPlannerV2.create_plan(model, self.registry)
        self.assertEqual(plan.status, PlanStatus.PROVEN)
        self.assertEqual(plan.strategy_name, "anchor_residual_pair_sum")
        self.assertEqual(plan.composed_capabilities, ["anchor_selection", "two_pointer_pair_sum"])

    def test_c_input_schema_adversary(self):
        """
        Test C — Input-schema adversarial wording:
        'The first line contains two integers n and x. Find three values at distinct positions whose sum is x.'
        Must establish selection.cardinality = 3, NEVER 2.
        """
        text = (
            "The first line contains two integers n and x.\n"
            "Find three values at distinct positions whose sum is x."
        )
        model = SemanticAdapter.parse(text)

        self.assertEqual(model.selection.cardinality, 3)
        self.assertEqual(model.selection.kind, SelectionKind.FIXED_CARDINALITY)

        # input.parameter_count must be recorded in INPUT_SCHEMA scope
        param_fact = model.get_fact("input.parameter_count")
        self.assertIsNotNone(param_fact)
        self.assertEqual(param_fact.value, 2)
        self.assertEqual(param_fact.scope, SemanticScope.INPUT_SCHEMA)

    def test_d_output_positions(self):
        """
        Test D — Output positions:
        'Find three values whose sum is x. Print their positions.'
        Must establish selection.cardinality = 3, output = ORIGINAL_INDICES.
        """
        text = "Find three values whose sum is x. Print their positions."
        model = SemanticAdapter.parse(text)

        self.assertEqual(model.selection.cardinality, 3)
        self.assertEqual(model.output_spec.get("type"), "ORIGINAL_INDICES")
        out_fact = model.get_fact("output.type")
        self.assertIsNotNone(out_fact)
        self.assertEqual(out_fact.value, "ORIGINAL_INDICES")

    def test_e_explicit_distinctness(self):
        """
        Test E — Explicit distinctness:
        Compare 'Find three values whose sum is x.'
        with 'Find three values at distinct positions whose sum is x.'
        The latter must establish explicit distinct_positions = True.
        """
        text_without_distinct = "Find three values whose sum is x."
        text_with_distinct = "Find three values at distinct positions whose sum is x."

        model_without = SemanticAdapter.parse(text_without_distinct)
        model_with = SemanticAdapter.parse(text_with_distinct)

        self.assertFalse(model_without.selection.distinct_positions)
        self.assertNotIn(StructuralProperty.PAIRWISE_DISTINCT_SELECTION, model_without.structural_properties)

        self.assertTrue(model_with.selection.distinct_positions)
        self.assertIn(StructuralProperty.PAIRWISE_DISTINCT_SELECTION, model_with.structural_properties)

    def test_f_different_relation_xor(self):
        """
        Test F — Different relation:
        'Find three values whose XOR is x.'
        Must NOT derive ADDITIVE_TARGET_SEARCH or PAIR_SUM_SEARCH.
        """
        text = "Find three values whose XOR is x."
        model = SemanticAdapter.parse(text)

        self.assertNotIn(RequiredOperation.ADDITIVE_TARGET_SEARCH, model.operations)
        self.assertNotIn(RequiredOperation.PAIR_SUM_SEARCH, model.operations)
        self.assertNotIn(StructuralProperty.DECOMPOSABLE_ADDITIVE_SEARCH, model.structural_properties)

    def test_g_four_values_fails_closed(self):
        """
        Test G — Four values:
        'Find four values at distinct positions whose sum is x.'
        Must establish FIXED_CARDINALITY(4), SUM, ADDITIVE_TARGET_SEARCH, DECOMPOSABLE_ADDITIVE_SEARCH,
        but returns UNSUPPORTED because verified backend supports only residual_k == 2.
        Must NOT silently become 3-sum.
        """
        text = "Find four values at distinct positions whose sum is x."
        model = SemanticAdapter.parse(text)

        self.assertEqual(model.selection.cardinality, 4)
        self.assertIn(RequiredOperation.ADDITIVE_TARGET_SEARCH, model.operations)
        self.assertIn(StructuralProperty.DECOMPOSABLE_ADDITIVE_SEARCH, model.structural_properties)

        plan = AlgorithmPlannerV2.create_plan(model, self.registry)
        self.assertEqual(plan.status, PlanStatus.UNSUPPORTED)
        self.assertEqual(plan.strategy_name, "recursive_additive_decomposition")
        self.assertTrue(any("residual cardinality k=3" in r for r in plan.rejection_reasons))

    def test_h_complete_vs_residual_capability(self):
        """
        Test H — Complete vs Residual Capability:
        For a three-value problem:
        two_pointer_pair_sum as complete solution is REJECTED with CARDINALITY_MISMATCH.
        why_not() explains: rejected as complete solution, but valid as composed residual component.
        """
        text = "Find three values at distinct positions whose sum is x."
        model = SemanticAdapter.parse(text)

        cap = self.registry.get("two_pointer_pair_sum")
        decision = CandidateEliminatorV2.evaluate(cap, model)
        self.assertEqual(decision.status, CandidateStatus.REJECTED)
        self.assertIn("CARDINALITY_MISMATCH", decision.reasons)

        explanation = self.bridge.why_not(text, "two_pointer_pair_sum")
        self.assertIn("CARDINALITY_MISMATCH", explanation)
        self.assertIn("residual component after one anchor is selected", explanation)

    def test_i_end_to_end_cpp_execution(self):
        """
        Test I — End-to-End Generated Code Verification:
        Compiles generated C++17 and tests:
          1. CSES example: 4 8 / 2 7 5 1 -> valid distinct 1-based indices summing to 8.
          2. 5 10 / 1 2 3 4 5 -> valid indices summing to 10.
          3. 3 6 / 1 2 3 -> 1 2 3.
          4. 3 100 / 1 2 3 -> IMPOSSIBLE.
          5. Duplicates: 5 6 / 2 2 2 1 5 -> distinct positions summing to 6.
          6. Negative numbers (out-of-domain robustness test): 6 0 / -1 0 1 2 -2 4 -> valid distinct indices summing to 0.
        """
        problem_text = """
        You are given an array of n integers, and your task is to find three values (at distinct positions) whose sum is x.
        Input
        The first input line has two integers n and x: the array size and the target sum.
        The second line has n integers a1,a2,...,an: the array values.
        Output
        Print three integers: the positions of the values. If there are several solutions, you may print any of them. If there are no solutions, print IMPOSSIBLE.
        Constraints
        1 <= n <= 5000
        1 <= x, ai <= 10^9
        """
        res = self.bridge.solve(problem_text)
        self.assertEqual(res["status"], "success")
        code = res["code"]
        self.assertIsNotNone(code)

        with tempfile.TemporaryDirectory() as tmpdir:
            cpp_file = os.path.join(tmpdir, "solution.cpp")
            bin_file = os.path.join(tmpdir, "solution")
            with open(cpp_file, "w") as f:
                f.write(code)

            comp = subprocess.run(["g++", "-O3", "-std=c++17", cpp_file, "-o", bin_file], capture_output=True, text=True)
            self.assertEqual(comp.returncode, 0, f"Compilation failed: {comp.stderr}")

            def verify_run(inp, expected_sum, is_impossible=False):
                p = subprocess.run([bin_file], input=inp, capture_output=True, text=True)
                out = p.stdout.strip()
                if is_impossible:
                    self.assertEqual(out, "IMPOSSIBLE")
                    return
                parts = [int(x) for x in out.split()]
                self.assertEqual(len(parts), 3)
                self.assertEqual(len(set(parts)), 3, f"Indices not distinct: {parts}")
                lines = inp.strip().split("\n")
                vals = [int(x) for x in lines[1].split()]
                actual_sum = sum(vals[idx - 1] for idx in parts)
                self.assertEqual(actual_sum, expected_sum)

            # 1. CSES example
            verify_run("4 8\n2 7 5 1\n", 8)
            # 2. 5 10
            verify_run("5 10\n1 2 3 4 5\n", 10)
            # 3. 3 6
            verify_run("3 6\n1 2 3\n", 6)
            # 4. 3 100 -> IMPOSSIBLE
            verify_run("3 100\n1 2 3\n", 100, is_impossible=True)
            # 5. Duplicates: 5 6 / 2 2 2 1 5
            verify_run("5 6\n2 2 2 1 5\n", 6)
            # 6. Negative values (explicitly out-of-domain robustness test)
            verify_run("6 0\n-1 0 1 2 -2 4\n", 0)

    def test_j_semantic_paraphrases(self):
        """
        Test J — Semantic Paraphrases:
        Verify that generic multi-fact derivation and decomposition trigger across
        diverse semantic expressions:
          1. 'Choose three distinct elements whose total is x.'
          2. 'Find 3 array entries at different indices adding up to x.'
          3. 'Output positions of three elements with combined value x.'
          4. 'Select exactly three entries, no two from the same position, whose values sum to x.'
        """
        paraphrases = [
            "Choose three distinct elements whose total is x.",
            "Find 3 array entries at different indices adding up to x.",
            "Output positions of three elements with combined value x.",
            "Select exactly three entries, no two from the same position, whose values sum to x."
        ]

        for text in paraphrases:
            with self.subTest(text=text):
                model = SemanticAdapter.parse(text)
                self.assertEqual(model.selection.cardinality, 3)
                self.assertIn(RequiredOperation.ADDITIVE_TARGET_SEARCH, model.operations)
                self.assertIn(StructuralProperty.DECOMPOSABLE_ADDITIVE_SEARCH, model.structural_properties)
                self.assertTrue(model.selection.distinct_positions)
                self.assertIn(StructuralProperty.PAIRWISE_DISTINCT_SELECTION, model.structural_properties)

                model.constraints.n = 5000
                plan = AlgorithmPlannerV2.create_plan(model, self.registry)
                self.assertEqual(plan.status, PlanStatus.PROVEN)
                self.assertEqual(plan.strategy_name, "anchor_residual_pair_sum")
                self.assertEqual(plan.composed_capabilities, ["anchor_selection", "two_pointer_pair_sum"])


if __name__ == "__main__":
    unittest.main()

