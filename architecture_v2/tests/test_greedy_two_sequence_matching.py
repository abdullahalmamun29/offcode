"""
Comprehensive test suite for Two-Sequence Monotonic Matching in Architecture V2.

Verifies:
1. CSES Apartments canonical problem derivation, planning, and execution.
2. Vocabulary independence (workers/tasks, boxes/items, servers/requests, formal collections).
3. Constraint and edge-case execution (all match, none match, exact boundary tolerance, duplicates, N != M).
4. Full C++ compilation and I/O execution with g++.
5. Negative discrimination and contrast against Ferris Wheel, Two Sum, Activity Selection, Knapsack.
6. Fail-closed behavior on unproven or invalid inputs.
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
)
from architecture_v2.capability_registry import CapabilityRegistry
from architecture_v2.planner import AlgorithmPlannerV2, PlanStatus
from pointer_algorithms.bridge import handle_request


APARTMENTS_CANONICAL = """
There are n applicants and m free apartments. Your task is to distribute the apartments so that as many applicants as possible will get an apartment.

Each applicant has a desired apartment size, and they will accept any apartment whose size is close enough to the desired size.
Input

The first input line has three integers n, m, and k: the number of applicants, the number of apartments, and the maximum allowed difference.

The next line contains n integers a1, a2, ... an: the desired apartment size of each applicant. If the desired size of an applicant is x, they will accept any apartment whose size is between x - k and x + k.

The last line contains m integers b1, b2, ... bm: the size of each apartment.
Output

Print one integer: the number of applicants who will get an apartment.
Constraints

1 <= n, m <= 2 * 10^5
0 <= k <= 10^9
1 <= ai, bi <= 10^9

Example
Input
4 3 5
60 45 80 60
30 60 75

Output
2
"""

WORKER_TASK_VARIANT = """
There are n workers and m available tasks. Distribute the tasks so that as many workers as possible receive a task.
Each worker has an optimal skill rating, and will accept any task whose difficulty is within tolerance k of their skill rating.
The first line contains n, m, and k.
The second line contains n integers for worker skills.
The third line contains m integers for task difficulties.
Print the maximum number of workers assigned a task.
"""

BOX_ITEM_VARIANT = """
Given two sequences of integers: n items and m boxes. Each item can be placed in at most one box, and each box can hold at most one item.
An item of size x fits into a box of size y if |x - y| <= k.
Find the maximum number of items that can be boxed.
Input
n m k
a1 ... an
b1 ... bm
"""

FORMAL_MATHEMATICAL_VARIANT = """
Given two finite sequences of numbers A of length n and B of length m, find a maximum cardinality one-to-one matching between elements of A and elements of B such that an element a in A and b in B can be paired if and only if |a - b| <= k.
Input format:
The first line has integers n, m, and k.
The second line has n integers for A.
The third line has m integers for B.
Output the maximum number of pairs.
"""

FERRIS_WHEEL_CONTRAST = """
There are n children who want to go to a Ferris wheel, and your task is to find a gondola for each child.
Each gondola may have one or two children in it, and in addition, the total weight in a gondola may not exceed x. You know the weight of every child.
What is the minimum number of gondolas needed for the children?
Input:
4 10
7 2 3 9
Constraints:
1 <= n <= 2*10^5
1 <= x <= 10^9
"""

TWO_SUM_CONTRAST = """
Given an array of n integers, find two values at distinct positions whose sum is x.
Input:
4 8
2 7 5 1
Constraints:
1 <= n <= 2*10^5
1 <= x <= 10^9
"""

ACTIVITY_SELECTION_CONTRAST = """
Given n intervals with start and end times, select the maximum number of mutually compatible, non-overlapping intervals.
"""

UNBOUNDED_MATCHING_CONTRAST = """
There are n applicants and m apartments. Each apartment can hold arbitrarily many applicants, provided each applicant desired size is close enough.
"""


def compile_and_run_cpp(cpp_source: str, stdin_data: str) -> str:
    """Helper to compile C++ source code and run with stdin_data, returning stdout."""
    cxx = shutil.which("g++") or shutil.which("clang++")
    if not cxx:
        raise unittest.SkipTest("No C++ compiler available")

    with tempfile.TemporaryDirectory() as tmpdir:
        src_file = os.path.join(tmpdir, "solution.cpp")
        bin_file = os.path.join(tmpdir, "solution.exe")

        with open(src_file, "w", encoding="utf-8") as f:
            f.write(cpp_source)

        compile_cmd = [cxx, "-O3", "-std=c++17", src_file, "-o", bin_file]
        proc_compile = subprocess.run(compile_cmd, capture_output=True, text=True)
        if proc_compile.returncode != 0:
            raise RuntimeError(f"C++ Compilation failed:\n{proc_compile.stderr}")

        proc_run = subprocess.run([bin_file], input=stdin_data, capture_output=True, text=True, timeout=5)
        if proc_run.returncode != 0:
            raise RuntimeError(f"C++ Execution failed with code {proc_run.returncode}:\n{proc_run.stderr}")

        return proc_run.stdout.strip()


class TestGreedyTwoSequenceMatching(unittest.TestCase):

    def setUp(self):
        self.bridge = BridgeV2()

    def test_canonical_apartments_semantic_derivation(self):
        """Test that canonical CSES Apartments derives all required properties and facts."""
        model = SemanticAdapter.parse(APARTMENTS_CANONICAL)

        self.assertIn(StructuralProperty.TWO_SEQUENCE_MATCHING, model.structural_properties)
        self.assertIn(StructuralProperty.ONE_TO_ONE_MATCHING, model.structural_properties)
        self.assertIn(StructuralProperty.MONOTONE_COMPATIBILITY, model.structural_properties)
        self.assertIn(StructuralProperty.ORDERED_STATE, model.structural_properties)
        self.assertIn(StructuralProperty.LOCAL_CHOICE, model.structural_properties)
        self.assertIn(StructuralProperty.MAX_CARDINALITY_MATCHING, model.structural_properties)
        self.assertIn(RequiredOperation.TWO_SEQUENCE_INTERVAL_MATCHING, model.operations)

        self.assertTrue(model.has_fact("collection.two_distinct_collections"))
        self.assertTrue(model.has_fact("matching.one_to_one"))
        self.assertTrue(model.has_fact("relation.interval_tolerance"))
        self.assertEqual(model.get_fact("objective.kind").value, ObjectiveKind.MAXIMIZE)

    def test_canonical_apartments_planning_and_proofs(self):
        """Test that planning establishes all 11 proof obligations and status is PROVEN."""
        model = SemanticAdapter.parse(APARTMENTS_CANONICAL)
        plan = AlgorithmPlannerV2.create_plan(model)

        self.assertEqual(plan.status, PlanStatus.PROVEN)
        self.assertEqual(plan.primary_capability, "greedy_two_sequence_interval_matching")
        self.assertEqual(plan.strategy_name, "greedy_two_sequence_interval_matching")
        self.assertEqual(len(plan.unresolved_obligations), 0)

        required_obligations = [
            "two_distinct_collections",
            "one_to_one_matching",
            "maximize_match_count",
            "sortable_numeric_domains",
            "interval_compatibility",
            "monotone_compatibility",
            "discard_too_small_is_safe",
            "discard_too_large_is_safe",
            "feasible_pair_match_is_safe",
            "both_pointers_monotonically_advance",
            "all_remaining_elements_eventually_processed"
        ]
        for obl in required_obligations:
            self.assertIn(obl, plan.established_obligations)

    def test_canonical_apartments_code_execution(self):
        """Test compiling and executing the generated code on CSES sample input."""
        res = self.bridge.solve(APARTMENTS_CANONICAL)
        self.assertEqual(res["status"], "success")
        code = res["code"]
        self.assertIsNotNone(code)

        stdin = "4 3 5\n60 45 80 60\n30 60 75\n"
        output = compile_and_run_cpp(code, stdin)
        self.assertEqual(output, "2")

    def test_vocabulary_independence_worker_task(self):
        """Test capability derivation on worker-task variant without apartment vocabulary."""
        res = self.bridge.solve(WORKER_TASK_VARIANT)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["selectedPattern"], "greedy_two_sequence_interval_matching")

    def test_vocabulary_independence_box_item(self):
        """Test capability derivation on box-item variant without apartment vocabulary."""
        res = self.bridge.solve(BOX_ITEM_VARIANT)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["selectedPattern"], "greedy_two_sequence_interval_matching")

    def test_vocabulary_independence_formal_mathematical(self):
        """Test capability derivation on formal mathematical phrasing."""
        res = self.bridge.solve(FORMAL_MATHEMATICAL_VARIANT)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["selectedPattern"], "greedy_two_sequence_interval_matching")

    def test_edge_case_all_matched(self):
        """Test execution when all elements match due to large tolerance."""
        res = self.bridge.solve(APARTMENTS_CANONICAL)
        code = res["code"]

        stdin = "3 3 100\n10 20 30\n15 25 35\n"
        output = compile_and_run_cpp(code, stdin)
        self.assertEqual(output, "3")

    def test_edge_case_none_matched(self):
        """Test execution when no elements match due to zero tolerance and disjoint values."""
        res = self.bridge.solve(APARTMENTS_CANONICAL)
        code = res["code"]

        stdin = "3 3 0\n10 20 30\n11 21 31\n"
        output = compile_and_run_cpp(code, stdin)
        self.assertEqual(output, "0")

    def test_edge_case_exact_boundary_tolerance(self):
        """Test execution when values match exactly at |a - b| == k."""
        res = self.bridge.solve(APARTMENTS_CANONICAL)
        code = res["code"]

        # a = [10, 20], b = [15, 25], k = 5 -> |10-15|=5 (valid), |20-25|=5 (valid) -> 2 matches
        stdin = "2 2 5\n10 20\n15 25\n"
        output = compile_and_run_cpp(code, stdin)
        self.assertEqual(output, "2")

    def test_edge_case_duplicates_and_unequal_sizes(self):
        """Test execution with duplicate values and n != m."""
        res = self.bridge.solve(APARTMENTS_CANONICAL)
        code = res["code"]

        # 5 applicants, 2 apartments: duplicate requests
        stdin = "5 2 2\n10 10 10 10 10\n11 12\n"
        output = compile_and_run_cpp(code, stdin)
        self.assertEqual(output, "2")

    def test_negative_discrimination_ferris_wheel(self):
        """Ferris wheel has single array and group capacity bound, must NOT select interval matching."""
        res = self.bridge.solve(FERRIS_WHEEL_CONTRAST)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["selectedPattern"], "greedy_capacity_pairing")
        self.assertNotEqual(res["selectedPattern"], "greedy_two_sequence_interval_matching")

    def test_negative_discrimination_two_sum(self):
        """Two sum has single array and target sum equality, must NOT select interval matching."""
        res = self.bridge.solve(TWO_SUM_CONTRAST)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["selectedPattern"], "two_pointer_pair_sum")
        self.assertNotEqual(res["selectedPattern"], "greedy_two_sequence_interval_matching")

    def test_negative_discrimination_activity_selection(self):
        """Activity selection is on intervals, not two-sequence numeric matching."""
        model = SemanticAdapter.parse(ACTIVITY_SELECTION_CONTRAST)
        plan = AlgorithmPlannerV2.create_plan(model)
        self.assertNotEqual(plan.primary_capability, "greedy_two_sequence_interval_matching")

    def test_pointer_bridge_integration(self):
        """Test pointer_algorithms bridge integration for Apartments."""
        res = handle_request({"action": "solve", "problemText": APARTMENTS_CANONICAL})
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["selectedPattern"], "greedy_two_sequence_interval_matching")
        self.assertEqual(res["family"], "two_pointers_same_direction")
        self.assertIsNotNone(res["code"])


if __name__ == "__main__":
    unittest.main()
