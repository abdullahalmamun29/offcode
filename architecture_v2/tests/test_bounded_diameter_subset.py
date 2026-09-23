"""
CHUP Architecture V2 — Bounded Diameter Subset Family Test Suite (CF 1133C Balanced Team).

Verifies:
1. Meta-constraint isolation: Multi-test-case input-size bounds do not contaminate problem data.
2. Objective disambiguation: Relational bounds ("at most k") do not leak into MAXIMIZE.
3. Derivation provenance: Pairwise difference -> Bounded diameter -> Sorted contiguous block -> Monotone window.
4. Negative controls: Non-cardinality objectives, two collections, contiguous selections, sum constraints.
5. Strict non-regression: Subarray Distinct Values and Challenging Valleys remain UNSUPPORTED.
6. End-to-end C++ compilation and execution on 11 test cases.
"""

import unittest
import subprocess
import tempfile
import os
import shutil
from architecture_v2.semantic_adapter import SemanticAdapter
from architecture_v2.semantic_model import (
    SelectionKind, ObjectiveKind, RelationKind,
    RequiredOperation, StructuralProperty, ConstraintDomain
)
from architecture_v2.capability_registry import CapabilityRegistry
from architecture_v2.candidate_eliminator import CandidateEliminatorV2, CandidateStatus
from architecture_v2.planner import AlgorithmPlannerV2, PlanStatus
from architecture_v2.bridge_v2 import BridgeV2


CF_1133C_CANONICAL = """
You are a coach at your local university. There are n students under your supervision, the programming skill of the i-th student is a_i.
You have to form a team for a competition. You want to select a team with the maximum number of students such that the programming skill of each student differs from the skill of any other student in the team by at most 5.
In other words, if you select a team of size k with skills s_1, s_2, ..., s_k, then for each pair (i, j) the condition |s_i - s_j| <= 5 should be satisfied.
Input:
The first line contains one integer n (1 <= n <= 2 * 10^5) — the number of students.
The second line contains n integers a_1, a_2, ..., a_n (1 <= a_i <= 10^9) — the programming skill of the students.
Output:
Print one integer — the maximum possible number of students in the team.
"""

CF_1133C_MULTI_TEST_CASE_ADVERSARIAL = """
There are multiple test cases. The first line contains t (1 <= t <= 1000).
For each test case:
The first line contains one integer n (1 <= n <= 2 * 10^5).
The second line contains n integers a_1, a_2, ..., a_n (1 <= a_i <= 10^9).
It is guaranteed that the sum of n over all test cases does not exceed 2 * 10^5.
Find the maximum number of students you can choose such that the difference between any two students does not exceed 5.
Print one integer for each test case.
"""

SUBARRAY_DISTINCT_VALUES_ADVERSARIAL = """
Given an array of n integers, count the number of subarrays having at most k distinct values.
Input:
The first line has two integers n and k: the array size and the maximum number of distinct values.
The next line has n integers x_1, x_2, ..., x_n: the array contents.
Output:
Print one integer: the number of subarrays.
"""

CHALLENGING_VALLEYS_ADVERSARIAL = """
You are given an array a of n integers. Determine if there exists exactly one valley in the array.
It is guaranteed that the sum of n over all test cases does not exceed 2 * 10^5.
"""


class TestBoundedDiameterSubset(unittest.TestCase):

    def setUp(self):
        self.bridge = BridgeV2()
        self.registry = CapabilityRegistry()

    # ── 1. Meta-Constraint & Semantic Boundary Isolation ──

    def test_multi_test_case_sum_of_n_isolated(self):
        """Verify that 'sum of n over all test cases' is isolated to INPUT_SIZE and not MONOTONE_RANGE_SUM."""
        model = SemanticAdapter.parse(CF_1133C_MULTI_TEST_CASE_ADVERSARIAL)
        self.assertIn(StructuralProperty.BOUNDED_DIAMETER, model.structural_properties)
        self.assertIn(StructuralProperty.SORTED_CONTIGUOUS_OPTIMAL_BLOCK, model.structural_properties)
        self.assertIn(StructuralProperty.MONOTONE_VALID_WINDOW, model.structural_properties)
        self.assertNotIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)
        self.assertNotIn(RequiredOperation.RANGE_AGGREGATE, model.operations)

        # Confirm input size constraint captured
        self.assertTrue(any(c.domain == ConstraintDomain.INPUT_SIZE for c in model.constraints.input_size_aggregates))

    def test_subarray_distinct_values_not_contaminated_by_at_most(self):
        """Verify that 'at most k distinct values' is COUNT / LESS_EQUAL and does not derive MAXIMIZE or PREDECESSOR."""
        model = SemanticAdapter.parse(SUBARRAY_DISTINCT_VALUES_ADVERSARIAL)
        self.assertEqual(model.objective.kind, ObjectiveKind.COUNT)
        self.assertNotIn(StructuralProperty.BOUNDED_DIAMETER, model.structural_properties)
        self.assertNotIn(RequiredOperation.PREDECESSOR, model.operations)
        self.assertNotIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)

        # Must fail-closed / unsupported in V2
        res = self.bridge.solve(SUBARRAY_DISTINCT_VALUES_ADVERSARIAL)
        self.assertEqual(res["status"], "unsupported")

    def test_challenging_valleys_unsupported(self):
        """Verify Challenging Valleys remains unsupported and sum of n does not trigger range sum."""
        model = SemanticAdapter.parse(CHALLENGING_VALLEYS_ADVERSARIAL)
        self.assertNotIn(StructuralProperty.MONOTONE_RANGE_SUM, model.structural_properties)
        res = self.bridge.solve(CHALLENGING_VALLEYS_ADVERSARIAL)
        self.assertEqual(res["status"], "unsupported")

    # ── 2. CF 1133C Canonical Semantic Parsing ──

    def test_canonical_cf1133c_semantic_model(self):
        """Verify semantic model extraction on canonical CF 1133C."""
        model = SemanticAdapter.parse(CF_1133C_CANONICAL)
        self.assertEqual(model.selection.kind, SelectionKind.ARBITRARY_SUBSET)
        self.assertEqual(model.objective.kind, ObjectiveKind.MAXIMIZE_CARDINALITY)
        self.assertTrue(any(r.kind == RelationKind.PAIRWISE_ABSOLUTE_DIFFERENCE for r in model.relations))
        self.assertIn(StructuralProperty.BOUNDED_DIAMETER, model.structural_properties)
        self.assertIn(StructuralProperty.SORTED_CONTIGUOUS_OPTIMAL_BLOCK, model.structural_properties)
        self.assertIn(StructuralProperty.MONOTONE_VALID_WINDOW, model.structural_properties)
        self.assertIn(StructuralProperty.ORDERED_STATE, model.structural_properties)
        self.assertIn(StructuralProperty.SINGLE_COLLECTION, model.structural_properties)
        self.assertIn(StructuralProperty.SORTABLE, model.structural_properties)
        self.assertIn(RequiredOperation.MAX_VALID_WINDOW, model.operations)

    def test_canonical_cf1133c_proof_obligations(self):
        """Verify that all 7 proof obligations are established for sort_and_maximum_bounded_diameter_subset."""
        model = SemanticAdapter.parse(CF_1133C_CANONICAL)
        cap = self.registry.get("sort_and_maximum_bounded_diameter_subset")
        self.assertIsNotNone(cap)

        decision = CandidateEliminatorV2.evaluate(cap, model)
        self.assertEqual(decision.status, CandidateStatus.ACCEPTED)
        for obl in cap.proof_obligations:
            self.assertEqual(decision.proof_status.get(obl), "PROVEN", f"Proof obligation {obl} not proven")

    def test_canonical_cf1133c_planning(self):
        """Verify planning creates a proven plan for CF 1133C."""
        model = SemanticAdapter.parse(CF_1133C_CANONICAL)
        plan = AlgorithmPlannerV2.create_plan(model, self.registry)
        self.assertEqual(plan.status, PlanStatus.PROVEN)
        self.assertEqual(plan.primary_capability, "sort_and_maximum_bounded_diameter_subset")
        self.assertTrue(plan.is_executable())
        self.assertIn("sort", plan.code)
        self.assertIn("while", plan.code)

    # ── 3. Phrasing Generalization ──

    def test_phrasing_variations(self):
        """Verify semantic model derives correctly across varied phrasings of bounded diameter subset."""
        phrasings = [
            "Given an array of integers, select the largest subset such that any two elements differ by at most 5.",
            "Find a subset of maximum size where for all pairs (x, y), |x - y| <= 5.",
            "Choose as many numbers as possible such that the difference between the maximum and minimum element is at most 5.",
            "Find the maximum number of items you can pick so that every pair has absolute difference <= 5.",
            "Select a subset of maximum cardinality with diameter at most 5."
        ]

        for text in phrasings:
            with self.subTest(text=text):
                model = SemanticAdapter.parse(text)
                self.assertEqual(model.selection.kind, SelectionKind.ARBITRARY_SUBSET)
                self.assertEqual(model.objective.kind, ObjectiveKind.MAXIMIZE_CARDINALITY)
                self.assertIn(StructuralProperty.BOUNDED_DIAMETER, model.structural_properties)
                self.assertIn(StructuralProperty.SORTED_CONTIGUOUS_OPTIMAL_BLOCK, model.structural_properties)
                self.assertIn(StructuralProperty.MONOTONE_VALID_WINDOW, model.structural_properties)

                plan = AlgorithmPlannerV2.create_plan(model, self.registry)
                self.assertEqual(plan.status, PlanStatus.PROVEN)
                self.assertEqual(plan.primary_capability, "sort_and_maximum_bounded_diameter_subset")

    # ── 4. Negative Controls ──

    def test_negative_control_maximize_sum_not_cardinality(self):
        """If objective is MAXIMIZE_SUM instead of MAXIMIZE_CARDINALITY, do NOT derive SORTED_CONTIGUOUS_OPTIMAL_BLOCK."""
        text = "Choose a subset of elements with diameter at most 5 that maximizes the total sum of chosen elements."
        model = SemanticAdapter.parse(text)
        self.assertEqual(model.objective.kind, ObjectiveKind.MAXIMIZE_SUM)
        self.assertIn(StructuralProperty.BOUNDED_DIAMETER, model.structural_properties)
        # Structural lemma requires MAXIMIZE_CARDINALITY!
        self.assertNotIn(StructuralProperty.SORTED_CONTIGUOUS_OPTIMAL_BLOCK, model.structural_properties)
        self.assertNotIn(StructuralProperty.MONOTONE_VALID_WINDOW, model.structural_properties)

        cap = self.registry.get("sort_and_maximum_bounded_diameter_subset")
        dec = CandidateEliminatorV2.evaluate(cap, model)
        self.assertNotEqual(dec.status, CandidateStatus.ACCEPTED)

    def test_negative_control_contiguous_segment_selection(self):
        """If selection is contiguous subarray (not arbitrary subset), do NOT accept sort_and_maximum_bounded_diameter_subset."""
        text = "Find the longest contiguous subarray whose elements differ by at most 5."
        model = SemanticAdapter.parse(text)
        self.assertEqual(model.selection.kind, SelectionKind.CONTIGUOUS_SEGMENT)
        cap = self.registry.get("sort_and_maximum_bounded_diameter_subset")
        dec = CandidateEliminatorV2.evaluate(cap, model)
        self.assertEqual(dec.status, CandidateStatus.REJECTED)
        self.assertIn("SELECTION_MODEL_MISMATCH", dec.reasons)

    def test_negative_control_two_distinct_collections(self):
        """If problem involves two arrays (e.g. students and apartments), do NOT accept single collection bounded diameter."""
        text = "Match students to apartments such that for each match the difference is at most 5. Maximize matches."
        model = SemanticAdapter.parse(text)
        cap = self.registry.get("sort_and_maximum_bounded_diameter_subset")
        dec = CandidateEliminatorV2.evaluate(cap, model)
        self.assertEqual(dec.status, CandidateStatus.REJECTED)

    # ── 5. End-to-End C++ Compilation & Test Battery ──

    def test_cpp_execution_battery(self):
        """Compiles C++ solution for CF 1133C and executes against 11 test cases."""
        if not shutil.which("g++"):
            self.skipTest("g++ compiler not available in environment")

        res = self.bridge.solve(CF_1133C_CANONICAL)
        self.assertEqual(res["status"], "success")
        code = res["code"]
        self.assertIsNotNone(code)

        with tempfile.TemporaryDirectory() as tmpdir:
            src_path = os.path.join(tmpdir, "solution.cpp")
            bin_path = os.path.join(tmpdir, "solution")

            with open(src_path, "w") as f:
                f.write(code)

            compile_proc = subprocess.run(
                ["g++", "-O3", "-std=c++17", src_path, "-o", bin_path],
                capture_output=True,
                text=True
            )
            self.assertEqual(compile_proc.returncode, 0, f"Compilation failed: {compile_proc.stderr}")

            # 11 Test cases: (input_string, expected_output)
            test_cases = [
                # 1. CF 1133C Canonical Example 1
                ("6\n1 10 17 12 15 2\n", "3"),
                # 2. CF 1133C Canonical Example 2
                ("3\n4 5 6\n", "3"),
                # 3. CF 1133C Canonical Example 3 (all identical)
                ("6\n2 2 2 2 2 2\n", "6"),
                # 4. Single element
                ("1\n42\n", "1"),
                # 5. Two elements exactly at boundary (diff == 5)
                ("2\n1 6\n", "2"),
                # 6. Two elements just over boundary (diff == 6)
                ("2\n1 7\n", "1"),
                # 7. All elements spaced > 5 apart
                ("5\n1 10 20 30 40\n", "1"),
                # 8. Duplicate clusters with large gap
                ("8\n3 3 3 10 10 10 10 25\n", "4"),
                # 9. Large numbers (10^9)
                ("5\n1000000000 1000000003 1000000005 1000000006 1000000012\n", "3"),
                # 10. Dense contiguous range 1..7 (diff <= 5 yields 6 elements: 1..6 or 2..7)
                ("7\n1 2 3 4 5 6 7\n", "6"),
                # 11. Reverse sorted input
                ("6\n100 95 90 85 80 75\n", "2")
            ]

            for idx, (tc_in, tc_expected) in enumerate(test_cases, 1):
                run_proc = subprocess.run(
                    [bin_path],
                    input=tc_in,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                self.assertEqual(run_proc.returncode, 0, f"Runtime error on test case {idx}: {run_proc.stderr}")
                actual = run_proc.stdout.strip()
                self.assertEqual(actual, tc_expected, f"Failed on test case {idx}: expected {tc_expected}, got {actual}")


if __name__ == "__main__":
    unittest.main()
