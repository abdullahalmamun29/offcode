"""
Dedicated regression test battery for Input-Size Aggregate Meta-Constraint Isolation.

Verifies:
1. Input-size aggregate constraints (e.g. "sum of n over all test cases <= 2e5")
   are partitioned strictly into ConstraintDomain.INPUT_SIZE.
2. They NEVER participate in:
   - MONOTONE_RANGE_SUM
   - RANGE_AGGREGATE
   - TARGET_SUM
   - relation.kind or operator.kind facts
3. Parameter variations: n, m, q, k, vertices, queries, strings, edges.
4. Codeforces 1760D "Challenging Valleys" is correctly rejected/unsupported
   without spurious MONOTONE_RANGE_SUM derivation.
5. Contrastive preservation: actual problem-data range sums (CSES Subarray Sums I)
   still derive MONOTONE_RANGE_SUM even when meta-constraints are present.
"""

import unittest

from architecture_v2.semantic_adapter import SemanticAdapter
from architecture_v2.semantic_model import (
    StructuralProperty,
    RequiredOperation,
    ConstraintDomain,
    RelationKind,
    OperatorKind,
)
from architecture_v2.planner import AlgorithmPlannerV2, PlanStatus
from architecture_v2.bridge_v2 import BridgeV2


CF_1760D_CHALLENGING_VALLEYS = """
You are given an array a[0...n-1] of n integers. This array is called a "valley" if there exists exactly one subarray a[l...r] such that:
0 <= l <= r <= n - 1,
al = al+1 = al+2 = ... = ar,
l = 0 or al-1 > al,
r = n - 1 or ar < ar+1.
Here are three examples:
The first image shows the array [3,2,2,1,2,2,3], it is a valley because only subarray with indices l=r=3 satisfies the condition.
The second image shows the array [1,1,1,2,3,3,4,5,6,6,6], it is a valley because only subarray with indices l=0,r=2 satisfies the condition.
The third image shows the array [1,2,3,4,3,2,1], it is not a valley because two subarrays l=r=0 and l=r=6 that satisfy the condition.
You are asked whether the given array is a valley or not.
Note that we consider the array to be indexed from 0.
Input
The first line contains a single integer t (1 <= t <= 10^4) - the number of test cases.
The first line of each test case contains a single integer n (1 <= n <= 2*10^5) - the length of the array.
The second line of each test case contains n integers a0, a1, ..., an-1 (1 <= ai <= 10^9) - the elements of the array.
It is guaranteed that the sum of n over all test cases does not exceed 2*10^5.
Output
For each test case, output "YES" (without quotes) if the given array is a valley, and "NO" (without quotes) otherwise.
"""


class TestMetaConstraintIsolation(unittest.TestCase):
    """Verifies that input-size aggregate meta-constraints are strictly isolated."""

    def test_meta_constraint_n_isolation(self):
        """subarray + 1 <= ai <= 10^9 + sum of n over all test cases is smaller than 2*10^5."""
        text = """
        Given an array of integers, check whether a valid subarray exists.
        Input:
        The first line has n integers (1 <= ai <= 10^9).
        It is guaranteed that the sum of n over all test cases is smaller than 2*10^5.
        """
        model = SemanticAdapter.parse(text)

        # 1. Structural properties must NOT contain MONOTONE_RANGE_SUM
        self.assertNotIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)
        self.assertNotIn(RequiredOperation.RANGE_AGGREGATE, model.operations)

        # 2. Input-size aggregate constraint must be present in ConstraintDomain.INPUT_SIZE
        self.assertEqual(len(model.constraints.input_size_aggregates), 1)
        agg = model.constraints.input_size_aggregates[0]
        self.assertEqual(agg.domain, ConstraintDomain.INPUT_SIZE)
        self.assertEqual(agg.aggregate, "SUM")
        self.assertEqual(agg.variable, "n")
        self.assertEqual(agg.scope, "ALL_TEST_CASES")
        self.assertEqual(agg.bound, 200000)

        # 3. Facts must reflect the input size aggregate
        self.assertTrue(model.has_fact("constraint.input_size.sum_n_all_test_cases"))
        self.assertEqual(model.get_fact("constraint.input_size.sum_n_all_test_cases").value, 200000)

        # 4. No problem data relations should be created from the meta-constraint
        for r in model.relations:
            self.assertEqual(r.domain, ConstraintDomain.PROBLEM_DATA)
            self.assertNotEqual(r.operator, OperatorKind.SUM)

    def test_meta_constraint_m_variant(self):
        """Variant with m: 'Across all test cases, the sum of m does not exceed 200,000.'"""
        text = """
        Process multiple queries on an array with subarrays.
        Constraints: 1 <= ai <= 10^9.
        Across all test cases, the sum of m does not exceed 200,000.
        """
        model = SemanticAdapter.parse(text)
        self.assertNotIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)
        self.assertNotIn(RequiredOperation.RANGE_AGGREGATE, model.operations)

        aggs = [a for a in model.constraints.input_size_aggregates if a.variable == "m"]
        self.assertEqual(len(aggs), 1)
        self.assertEqual(aggs[0].bound, 200000)
        self.assertEqual(aggs[0].domain, ConstraintDomain.INPUT_SIZE)

    def test_meta_constraint_q_variant(self):
        """Variant with q: 'The sum of q over all test cases <= 2*10^5.'"""
        text = """
        Answer queries on subarrays. Elements are positive: 1 <= ai <= 10^9.
        The sum of q over all test cases <= 2*10^5.
        """
        model = SemanticAdapter.parse(text)
        self.assertNotIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)
        self.assertNotIn(RequiredOperation.RANGE_AGGREGATE, model.operations)

        aggs = [a for a in model.constraints.input_size_aggregates if a.variable == "q"]
        self.assertEqual(len(aggs), 1)
        self.assertEqual(aggs[0].bound, 200000)
        self.assertEqual(aggs[0].domain, ConstraintDomain.INPUT_SIZE)

    def test_meta_constraint_k_variant(self):
        """Variant with k: 'the sum of k over all test cases is at most 2*10^5'"""
        text = """
        Select contiguous elements. 1 <= ai <= 10^9.
        It is guaranteed that the sum of k over all test cases is at most 2*10^5.
        """
        model = SemanticAdapter.parse(text)
        self.assertNotIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)
        self.assertNotIn(RequiredOperation.RANGE_AGGREGATE, model.operations)

        aggs = [a for a in model.constraints.input_size_aggregates if a.variable == "k"]
        self.assertEqual(len(aggs), 1)
        self.assertEqual(aggs[0].bound, 200000)
        self.assertEqual(aggs[0].domain, ConstraintDomain.INPUT_SIZE)

    def test_meta_constraint_vertices_variant(self):
        """Variant with vertices: 'The sum of vertices over all test cases <= 2e5.'"""
        text = """
        Subarray segmentation of tree vertices. 1 <= ai <= 10^9.
        The sum of vertices over all test cases <= 2e5.
        """
        model = SemanticAdapter.parse(text)
        self.assertNotIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)
        self.assertNotIn(RequiredOperation.RANGE_AGGREGATE, model.operations)

        aggs = [a for a in model.constraints.input_size_aggregates if a.variable == "vertices"]
        self.assertEqual(len(aggs), 1)
        self.assertEqual(aggs[0].bound, 200000)
        self.assertEqual(aggs[0].domain, ConstraintDomain.INPUT_SIZE)

    def test_meta_constraint_queries_variant(self):
        """Variant with queries: 'The sum of queries over all test cases does not exceed 200000.'"""
        text = """
        Inspect subarrays of positive numbers (1 <= ai <= 10^9).
        The sum of queries over all test cases does not exceed 200000.
        """
        model = SemanticAdapter.parse(text)
        self.assertNotIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)
        self.assertNotIn(RequiredOperation.RANGE_AGGREGATE, model.operations)

        aggs = [a for a in model.constraints.input_size_aggregates if a.variable == "queries"]
        self.assertEqual(len(aggs), 1)
        self.assertEqual(aggs[0].bound, 200000)
        self.assertEqual(aggs[0].domain, ConstraintDomain.INPUT_SIZE)

    def test_meta_constraint_strings_variant(self):
        """Variant with strings: 'The sum of strings over all test cases <= 2*10^5.'"""
        text = """
        Check subarrays of character codes. 1 <= ai <= 10^9.
        The sum of strings over all test cases <= 2*10^5.
        """
        model = SemanticAdapter.parse(text)
        self.assertNotIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)
        self.assertNotIn(RequiredOperation.RANGE_AGGREGATE, model.operations)

        aggs = [a for a in model.constraints.input_size_aggregates if a.variable == "strings"]
        self.assertEqual(len(aggs), 1)
        self.assertEqual(aggs[0].bound, 200000)
        self.assertEqual(aggs[0].domain, ConstraintDomain.INPUT_SIZE)

    def test_meta_constraint_edges_variant(self):
        """Variant with edges: 'The sum of edges over all test cases <= 2e5.'"""
        text = """
        Linear graph path subarrays. 1 <= ai <= 10^9.
        The sum of edges over all test cases <= 2e5.
        """
        model = SemanticAdapter.parse(text)
        self.assertNotIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)
        self.assertNotIn(RequiredOperation.RANGE_AGGREGATE, model.operations)

        aggs = [a for a in model.constraints.input_size_aggregates if a.variable == "edges"]
        self.assertEqual(len(aggs), 1)
        self.assertEqual(aggs[0].bound, 200000)
        self.assertEqual(aggs[0].domain, ConstraintDomain.INPUT_SIZE)

    def test_codeforces_1760d_challenging_valleys_audit(self):
        """
        Codeforces 1760D "Challenging Valleys":
        Must NOT derive MONOTONE_RANGE_SUM or RANGE_AGGREGATE.
        Must remain strictly UNSUPPORTED until the general adjacent-comparison/extremum family is implemented.
        """
        model = SemanticAdapter.parse(CF_1760D_CHALLENGING_VALLEYS)

        # Meta-constraint correctly identified as INPUT_SIZE aggregate:
        aggs = [a for a in model.constraints.input_size_aggregates if a.variable == "n"]
        self.assertEqual(len(aggs), 1)
        self.assertEqual(aggs[0].bound, 200000)
        self.assertEqual(aggs[0].domain, ConstraintDomain.INPUT_SIZE)

        # Structural properties must NOT contain MONOTONE_RANGE_SUM:
        self.assertNotIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)
        self.assertNotIn(RequiredOperation.RANGE_AGGREGATE, model.operations)

        # Planner must classify as UNSUPPORTED (no valid algorithm in registry):
        plan = AlgorithmPlannerV2.create_plan(model)
        self.assertEqual(plan.status, PlanStatus.UNSUPPORTED)

        # Bridge must fail closed:
        res = BridgeV2().solve(CF_1760D_CHALLENGING_VALLEYS)
        self.assertEqual(res.get("status"), "unsupported")

    def test_multi_meta_constraints(self):
        """Multiple meta-constraints across test cases (e.g. both n and m)."""
        text = """
        Process bipartite relations.
        It is guaranteed that the sum of n over all test cases does not exceed 2*10^5.
        The sum of m over all test cases does not exceed 2*10^5.
        """
        model = SemanticAdapter.parse(text)
        vars_found = {a.variable: a.bound for a in model.constraints.input_size_aggregates}
        self.assertIn("n", vars_found)
        self.assertIn("m", vars_found)
        self.assertEqual(vars_found["n"], 200000)
        self.assertEqual(vars_found["m"], 200000)

    def test_contrastive_preservation_cses_subarray_sums_i(self):
        """
        CSES Subarray Sums I problem text with an additional meta-constraint.
        The genuine range sum condition ('having sum x') MUST still derive MONOTONE_RANGE_SUM,
        while the meta-constraint is properly recorded in input_size_aggregates.
        """
        text = """
        Given an array of n positive integers, your task is to count the number of subarrays having sum x.
        Input
        The first input line has two integers n and x: the size of the array and the target sum x.
        The next line has n integers a1, a2, ..., an: the contents of the array.
        Output
        Print one integer: the required number of subarrays.
        Constraints
        1 <= n <= 2 * 10^5
        1 <= x, ai <= 10^9
        It is guaranteed that the sum of n over all test cases does not exceed 2*10^5.
        """
        model = SemanticAdapter.parse(text)

        # Genuine range sum property IS derived from 'having sum x':
        self.assertIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)
        self.assertIn(RequiredOperation.RANGE_AGGREGATE, model.operations)

        # Meta-constraint is cleanly isolated:
        self.assertTrue(any(a.variable == "n" and a.bound == 200000 for a in model.constraints.input_size_aggregates))

        # Successfully plans sliding window:
        plan = AlgorithmPlannerV2.create_plan(model)
        self.assertEqual(plan.status, PlanStatus.PROVEN)
        self.assertEqual(plan.primary_capability, "sliding_window_exact_range_sum_count")


if __name__ == "__main__":
    unittest.main()
