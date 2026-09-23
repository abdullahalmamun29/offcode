"""
Comprehensive test suite for Exact-Sum Contiguous Range Reasoning (Sliding Window) in Architecture V2.

Verifies:
1. CSES Subarray Sums I canonical problem derivation, planning, and execution.
2. Positivity extraction and proof obligation verification (strictly positive required).
3. Monotonicity derivation without dependence on COUNT objective.
4. Exclusion of spurious properties (LOCAL_CHOICE is NOT derived).
5. Fail-closed behavior on zero/negative elements, unstated bounds, and at-most sums.
6. Contrastive discrimination: subset sum vs contiguous subarray sum.
7. Candidate elimination: knapsack / subset_sum eliminated with SELECTION_MODEL_MISMATCH.
8. Full C++ compilation and I/O execution with g++.
"""

import os
import shutil
import subprocess
import tempfile
import unittest

from architecture_v2.bridge_v2 import BridgeV2
from architecture_v2.semantic_adapter import SemanticAdapter
from architecture_v2.semantic_model import (
    StructuralProperty,
    RequiredOperation,
    RelationKind,
    SelectionKind,
    ObjectiveKind,
    OperatorKind,
)
from architecture_v2.capability_registry import CapabilityRegistry
from architecture_v2.candidate_eliminator import CandidateEliminatorV2, CandidateStatus
from architecture_v2.planner import AlgorithmPlannerV2, PlanStatus
from pointer_algorithms.bridge import handle_request


CSES_SUBARRAY_SUMS_I_CANONICAL = """
Given an array of nn positive integers, your task is to count the number of subarrays having sum xx.
Input

The first input line has two integers nn and xx: the size of the array and the target sum xx.

The next line has nn integers a1,a2,...,an: the contents of the array.
Output

Print one integer: the required number of subarrays.
Constraints

1 <= n <= 2 * 10^5
1 <= x, ai <= 10^9

Example
InputCopy 	

5 7
2 4 1 2 7

OutputCopy	

3
"""

SINGULAR_WORDING_PROBLEM = """
Given an array of positive integers, find a subarray whose sum is equal to x.
Constraints: 1 <= ai <= 10^9
"""

PLURAL_WORDING_PROBLEM = """
Count subarrays whose sum is x in an array of positive integers.
Constraints: 1 <= ai <= 10^9
"""

CONTIGUOUS_RANGES_PROBLEM = """
Count contiguous ranges having sum x in an array of positive integers.
Constraints: 1 <= ai <= 10^9
"""

UNPROVEN_POSITIVITY_PROBLEM = """
Given an array of integers, count the number of subarrays having sum x.
Input: n x, array a.
Constraints: 1 <= n <= 2*10^5
"""

ZERO_VALUES_PROBLEM = """
Count the number of subarrays having sum x.
Constraints:
1 <= n <= 2*10^5
0 <= ai <= 10^9
"""

NEGATIVE_VALUES_PROBLEM = """
Count the number of subarrays having sum x.
The array may contain negative numbers.
Constraints:
-10^9 <= ai <= 10^9
"""

AT_MOST_SUM_PROBLEM = """
Count the number of subarrays having sum at most x.
Constraints:
1 <= ai <= 10^9
"""

SUBSET_SUM_PROBLEM = """
Given an array of positive integers, determine if there exists a subset of elements whose sum is x.
Constraints: 1 <= ai <= 10^9
"""


class TestSlidingWindowExactSum(unittest.TestCase):
    def setUp(self):
        self.bridge = BridgeV2()
        self.registry = CapabilityRegistry()

    def test_canonical_cses_subarray_sums_i(self):
        """Test complete derivation and planning for CSES Subarray Sums I."""
        model = SemanticAdapter.parse(CSES_SUBARRAY_SUMS_I_CANONICAL)

        # 1. Semantic parsing checks
        self.assertEqual(model.selection.kind, SelectionKind.CONTIGUOUS_SEGMENT)
        self.assertTrue(model.constraints.strictly_positive)
        self.assertEqual(model.objective.kind, ObjectiveKind.COUNT)
        self.assertTrue(any(r.kind == RelationKind.EQUALITY and r.operator == OperatorKind.SUM for r in model.relations))

        # 2. Structural derivation checks
        self.assertIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)
        self.assertIn(StructuralProperty.MONOTONICITY, model.structural_properties)
        self.assertIn(StructuralProperty.CONTIGUOUS_SELECTION, model.structural_properties)
        self.assertIn(StructuralProperty.ORDERED_STATE, model.structural_properties)
        self.assertIn(RequiredOperation.RANGE_AGGREGATE, model.operations)
        self.assertIn(RequiredOperation.COUNT, model.operations)

        # 3. SPURIOUS PROPERTY CHECK: LOCAL_CHOICE must NOT be derived for monotone range sums
        self.assertNotIn(StructuralProperty.LOCAL_CHOICE, model.structural_properties)

        # 4. Plan creation and proof obligations
        plan = AlgorithmPlannerV2.create_plan(model, self.registry)
        self.assertEqual(plan.status, PlanStatus.PROVEN)
        self.assertEqual(plan.primary_capability, 'sliding_window_exact_range_sum_count')
        self.assertEqual(len(plan.unresolved_obligations), 0)
        self.assertIn('strictly_positive_elements', plan.established_obligations)
        self.assertIn('contiguous_range_selection', plan.established_obligations)
        self.assertIn('monotone_right_expansion', plan.established_obligations)
        self.assertIn('monotone_left_contraction', plan.established_obligations)
        self.assertIsNotNone(plan.code)
        self.assertIn('while (current_sum > target && left <= right)', plan.code)

    def test_cpp_compilation_and_execution(self):
        """Compile generated C++ with g++ and verify correctness against multiple test cases."""
        if not shutil.which('g++'):
            self.skipTest('g++ compiler not available')

        model = SemanticAdapter.parse(CSES_SUBARRAY_SUMS_I_CANONICAL)
        plan = AlgorithmPlannerV2.create_plan(model, self.registry)
        self.assertEqual(plan.status, PlanStatus.PROVEN)
        self.assertIsNotNone(plan.code)

        with tempfile.TemporaryDirectory() as tmpdir:
            cpp_path = os.path.join(tmpdir, 'solution.cpp')
            bin_path = os.path.join(tmpdir, 'solution')

            with open(cpp_path, 'w') as f:
                f.write(plan.code)

            # Compile
            comp_res = subprocess.run(
                ['g++', '-O3', cpp_path, '-o', bin_path],
                capture_output=True,
                text=True
            )
            self.assertEqual(comp_res.returncode, 0, f'Compilation failed: {comp_res.stderr}')

            # Test 1: Canonical CSES sample (5 elements, target 7) -> 3
            # Subarrays with sum 7: [2, 4, 1], [4, 1, 2], [7]
            input_data = "5 7\n2 4 1 2 7\n"
            run_res = subprocess.run([bin_path], input=input_data, capture_output=True, text=True)
            self.assertEqual(run_res.returncode, 0)
            self.assertEqual(run_res.stdout.strip(), "3")

            # Test 2: All ones (5 elements, target 3) -> 3 ([1,1,1] at [0..2], [1..3], [2..4])
            input_data = "5 3\n1 1 1 1 1\n"
            run_res = subprocess.run([bin_path], input=input_data, capture_output=True, text=True)
            self.assertEqual(run_res.returncode, 0)
            self.assertEqual(run_res.stdout.strip(), "3")

            # Test 3: No match
            input_data = "3 10\n1 2 3\n"
            run_res = subprocess.run([bin_path], input=input_data, capture_output=True, text=True)
            self.assertEqual(run_res.returncode, 0)
            self.assertEqual(run_res.stdout.strip(), "0")

            # Test 4: Single element match
            input_data = "1 42\n42\n"
            run_res = subprocess.run([bin_path], input=input_data, capture_output=True, text=True)
            self.assertEqual(run_res.returncode, 0)
            self.assertEqual(run_res.stdout.strip(), "1")

            # Test 5: Entire array match
            input_data = "4 10\n1 2 3 4\n"
            run_res = subprocess.run([bin_path], input=input_data, capture_output=True, text=True)
            self.assertEqual(run_res.returncode, 0)
            self.assertEqual(run_res.stdout.strip(), "1")

    def test_singular_wording_derives_monotonicity_without_count(self):
        """Singular 'find a subarray' must derive monotonicity without depending on COUNT objective."""
        model = SemanticAdapter.parse(SINGULAR_WORDING_PROBLEM)
        self.assertEqual(model.selection.kind, SelectionKind.CONTIGUOUS_SEGMENT)
        self.assertTrue(model.constraints.strictly_positive)
        self.assertIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)
        self.assertIn(StructuralProperty.MONOTONICITY, model.structural_properties)
        # Objective is FIND_ANY, not COUNT
        self.assertNotEqual(model.objective.kind, ObjectiveKind.COUNT)

    def test_plural_wording_parses_selection_and_count(self):
        """Plural 'count subarrays' correctly sets CONTIGUOUS_SEGMENT and COUNT."""
        model = SemanticAdapter.parse(PLURAL_WORDING_PROBLEM)
        self.assertEqual(model.selection.kind, SelectionKind.CONTIGUOUS_SEGMENT)
        self.assertTrue(model.constraints.strictly_positive)
        self.assertEqual(model.objective.kind, ObjectiveKind.COUNT)
        self.assertIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)

    def test_contiguous_ranges_wording(self):
        """'contiguous ranges' maps to CONTIGUOUS_SEGMENT."""
        model = SemanticAdapter.parse(CONTIGUOUS_RANGES_PROBLEM)
        self.assertEqual(model.selection.kind, SelectionKind.CONTIGUOUS_SEGMENT)
        self.assertTrue(model.constraints.strictly_positive)
        self.assertIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)

    def test_unproven_positivity_fails_closed(self):
        """When positivity is not stated or provable, strictly positive proof fails closed."""
        model = SemanticAdapter.parse(UNPROVEN_POSITIVITY_PROBLEM)
        self.assertFalse(model.constraints.strictly_positive)
        self.assertNotIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)

        decisions = CandidateEliminatorV2.filter_candidates(self.registry, model)
        sw_decision = next((d for d in decisions if d.candidate_name == 'sliding_window_exact_range_sum_count'), None)
        self.assertIsNotNone(sw_decision)
        self.assertNotEqual(sw_decision.status, CandidateStatus.ACCEPTED)

        plan = AlgorithmPlannerV2.create_plan(model, self.registry)
        self.assertNotEqual(plan.status, PlanStatus.PROVEN)

    def test_zero_values_fails_closed(self):
        """0 <= ai <= 10^9 allows zero, which destroys strict window contraction monotonicity."""
        model = SemanticAdapter.parse(ZERO_VALUES_PROBLEM)
        self.assertFalse(model.constraints.strictly_positive)
        self.assertNotIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)

        plan = AlgorithmPlannerV2.create_plan(model, self.registry)
        self.assertNotEqual(plan.status, PlanStatus.PROVEN)

    def test_negative_values_fails_closed(self):
        """Negative elements destroy window sum monotonicity."""
        model = SemanticAdapter.parse(NEGATIVE_VALUES_PROBLEM)
        self.assertFalse(model.constraints.strictly_positive)
        self.assertNotIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)

        plan = AlgorithmPlannerV2.create_plan(model, self.registry)
        self.assertNotEqual(plan.status, PlanStatus.PROVEN)

    def test_at_most_sum_relation_mismatch(self):
        """At-most sum requires RelationKind.LESS_EQUAL, rejecting exact sum capability."""
        model = SemanticAdapter.parse(AT_MOST_SUM_PROBLEM)
        self.assertTrue(any(r.kind == RelationKind.LESS_EQUAL for r in model.relations))
        self.assertFalse(any(r.kind == RelationKind.EQUALITY for r in model.relations))

        decisions = CandidateEliminatorV2.filter_candidates(self.registry, model)
        sw_decision = next((d for d in decisions if d.candidate_name == 'sliding_window_exact_range_sum_count'), None)
        self.assertIsNotNone(sw_decision)
        self.assertEqual(sw_decision.status, CandidateStatus.REJECTED)
        self.assertIn('RELATION_MISMATCH', sw_decision.reasons[0])

    def test_cross_family_contrast_subset_sum_vs_contiguous(self):
        """Subset sum (arbitrary subset) must be rejected by sliding window; contiguous subarray must accept."""
        # Subset sum
        subset_model = SemanticAdapter.parse(SUBSET_SUM_PROBLEM)
        self.assertEqual(subset_model.selection.kind, SelectionKind.ARBITRARY_SUBSET)
        subset_decisions = CandidateEliminatorV2.filter_candidates(self.registry, subset_model)
        sw_on_subset = next((d for d in subset_decisions if d.candidate_name == 'sliding_window_exact_range_sum_count'), None)
        self.assertIsNotNone(sw_on_subset)
        self.assertEqual(sw_on_subset.status, CandidateStatus.REJECTED)
        self.assertIn('SELECTION_MODEL_MISMATCH', sw_on_subset.reasons[0])

        # Contiguous subarray sum
        contiguous_model = SemanticAdapter.parse(PLURAL_WORDING_PROBLEM)
        self.assertEqual(contiguous_model.selection.kind, SelectionKind.CONTIGUOUS_SEGMENT)
        contiguous_decisions = CandidateEliminatorV2.filter_candidates(self.registry, contiguous_model)
        sw_on_contiguous = next((d for d in contiguous_decisions if d.candidate_name == 'sliding_window_exact_range_sum_count'), None)
        self.assertIsNotNone(sw_on_contiguous)
        self.assertEqual(sw_on_contiguous.status, CandidateStatus.ACCEPTED)

    def test_knapsack_elimination_on_contiguous_problem(self):
        """Candidates requiring ARBITRARY_SUBSET (e.g. knapsack) are eliminated with SELECTION_MODEL_MISMATCH."""
        model = SemanticAdapter.parse(CSES_SUBARRAY_SUMS_I_CANONICAL)
        decisions = CandidateEliminatorV2.filter_candidates(self.registry, model)
        knapsack_decision = next((d for d in decisions if d.candidate_name == 'knapsack_01'), None)
        self.assertIsNotNone(knapsack_decision)
        self.assertEqual(knapsack_decision.status, CandidateStatus.REJECTED)
        self.assertIn('SELECTION_MODEL_MISMATCH', knapsack_decision.reasons[0])

    def test_pointer_bridge_end_to_end_cses(self):
        """Handle request through pointer_algorithms bridge for CSES Subarray Sums I."""
        res = handle_request({
            'action': 'solve',
            'problemText': CSES_SUBARRAY_SUMS_I_CANONICAL
        })
        self.assertEqual(res['status'], 'success')
        self.assertEqual(res['selectedPattern'], 'sliding_window_exact_range_sum_count')
        self.assertEqual(res['family'], 'sliding_window')
        self.assertEqual(res['supportState']['state'], 'first_class_supported')
        self.assertIn('strictly positive', res['reasoning'].lower())
        self.assertIsNotNone(res['code'])
        self.assertIn('while (current_sum > target && left <= right)', res['code'])


if __name__ == '__main__':
    unittest.main()
