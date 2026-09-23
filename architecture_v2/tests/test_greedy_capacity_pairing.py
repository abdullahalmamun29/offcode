"""
Comprehensive test suite for Greedy Capacity Pairing in Architecture V2.

Verifies:
1. CSES Ferris Wheel canonical problem derivation, planning, and execution.
2. Vocabulary independence (boats, packages, vehicles, formal grouping).
3. Constraint and edge-case execution (single element, all pair, none pair, exact capacity, duplicates).
4. Full C++ compilation and I/O execution with g++.
5. Negative discrimination and contrast against Activity Selection, Two-Sum, Knapsack.
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
    OperatorKind,
    SelectionKind,
)
from architecture_v2.capability_registry import CapabilityRegistry
from architecture_v2.planner import AlgorithmPlannerV2, PlanStatus
from pointer_algorithms.bridge import handle_request


FERRIS_WHEEL_CANONICAL = """
There are n children who want to go to a Ferris wheel, and your task is to find a gondola for each child.

Each gondola may have one or two children in it, and in addition, the total weight in a gondola may not exceed x. You know the weight of every child.

What is the minimum number of gondolas needed for the children?
Input

The first input line contains two integers n and x: the number of children and the maximum allowed weight.

The next line contains n integers p1, p2, ..., pn: the weight of each child.
Output

Print one integer: the minimum number of gondolas.
Constraints

1 <= n <= 2 * 10^5
1 <= x <= 10^9
1 <= pi <= x

Example
Input
4 10
7 2 3 9

Output
3
"""

BOAT_RESCUE_VARIANT = """
You have n people waiting for rescue boats. Each boat can carry at most two people, provided their combined weight does not exceed x. Find the minimum number of boats needed to rescue all people.

Input
The first line contains n and x.
The next line contains n weights.
"""

PACKAGE_CONTAINER_VARIANT = """
Given n packages with varying weights, package them into bins. Each bin can hold at most 2 packages and the total weight must not exceed x. Minimize the total number of bins required to pack all packages.
"""

VEHICLE_CARGO_VARIANT = """
There are n cargo items. Each vehicle can take at most two items, with sum of item weights at most x. What is the minimum number of vehicles needed to transport all items?
"""

FORMAL_PARTITION_VARIANT = """
Given an array of n integers and a threshold x, partition all elements into groups such that each group contains at most two elements and the sum of elements in each group is less than or equal to x. Minimize the number of groups.
"""

ACTIVITY_SELECTION_CONTRAST = """
Given n intervals with start and end times, select the maximum number of mutually compatible, non-overlapping intervals.
"""

TWO_SUM_CONTRAST = """
Given an array of n integers, find two values whose sum is x.
"""

GENERAL_BIN_PACKING_CONTRAST = """
Given n items each with weight w_i, pack them into knapsacks of capacity x. Each knapsack can hold any number of items as long as their total weight does not exceed x. Find the minimum number of knapsacks.
"""


def compile_and_run_cpp(cpp_source: str, stdin_data: str) -> str:
    """Helper to compile C++ source code and run with stdin_data, returning stdout."""
    cxx = shutil.which("g++") or shutil.which("clang++")
    if not cxx:
        raise unittest.SkipTest("No C++ compiler available")

    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, "solution.cpp")
        bin_path = os.path.join(tmpdir, "solution")

        with open(src_path, "w", encoding="utf-8") as f:
            f.write(cpp_source)

        compile_proc = subprocess.run(
            [cxx, "-O3", "-std=c++17", src_path, "-o", bin_path],
            capture_output=True,
            text=True
        )
        if compile_proc.returncode != 0:
            raise RuntimeError(f"C++ Compilation failed:\n{compile_proc.stderr}")

        run_proc = subprocess.run(
            [bin_path],
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=5
        )
        if run_proc.returncode != 0:
            raise RuntimeError(f"Execution failed:\n{run_proc.stderr}")

        return run_proc.stdout.strip()


class TestGreedyCapacityPairing(unittest.TestCase):

    def setUp(self):
        self.bridge = BridgeV2()

    def test_semantic_derivation_ferris_wheel(self):
        """Verify semantic adapter and derivation engine extract capacity pairing properties."""
        model = SemanticAdapter.parse(FERRIS_WHEEL_CANONICAL)

        # 1. Structural constraints
        self.assertEqual(model.constraints.max_group_cardinality, 2)
        self.assertEqual(model.constraints.group_capacity, 10)
        self.assertEqual(model.selection.kind, SelectionKind.ALL_ELEMENTS)
        self.assertEqual(model.objective.target_property, "groups")

        # 2. Relations
        has_sum_relation = any(
            (r.kind == RelationKind.LESS_EQUAL and r.operator == OperatorKind.SUM)
            or (r.kind == RelationKind.SUM)
            for r in model.relations
        )
        self.assertTrue(has_sum_relation, "Should extract sum relation with capacity bound")

        # 3. Derived properties
        self.assertIn(StructuralProperty.CAPACITY_CONSTRAINED_GROUPING, model.structural_properties)
        self.assertIn(StructuralProperty.EXTREMAL_PAIRING, model.structural_properties)
        self.assertIn(RequiredOperation.CAPACITY_PAIRING, model.operations)

    def test_solve_ferris_wheel_canonical(self):
        """Verify BridgeV2 creates a proven plan and correct C++ code for CSES Ferris Wheel."""
        res = self.bridge.solve(FERRIS_WHEEL_CANONICAL)

        self.assertEqual(res["status"], "success")
        self.assertEqual(res["selectedPattern"], "greedy_capacity_pairing")
        self.assertIsNotNone(res["code"])
        self.assertIn("while (left <= right)", res["code"])
        self.assertIn("sort(a.begin(), a.end())", res["code"])
        self.assertIn("invariant", res)
        self.assertTrue(len(res["invariant"]) > 0)

        # Check proof obligations
        expected_obs = [
            "extremal_pairing_optimal",
            "sorting_permitted",
            "opposite_pointers_exhaust_search",
            "capacity_feasibility_checked",
            "all_items_covered"
        ]
        for ob in expected_obs:
            self.assertIn(ob, res["proofObligations"])

        # Compile and verify canonical example: 4 10 / 7 2 3 9 -> 3
        output = compile_and_run_cpp(res["code"], "4 10\n7 2 3 9\n")
        self.assertEqual(output, "3")

    def test_cpp_execution_edge_cases(self):
        """Verify compiled solution executes correctly across edge cases."""
        res = self.bridge.solve(FERRIS_WHEEL_CANONICAL)
        self.assertEqual(res["status"], "success")
        code = res["code"]

        # Case 1: Single element
        out = compile_and_run_cpp(code, "1 10\n7\n")
        self.assertEqual(out, "1")

        # Case 2: Everyone pairs: 1+4<=10, 2+3<=10 -> 2 groups
        out = compile_and_run_cpp(code, "4 10\n1 2 3 4\n")
        self.assertEqual(out, "2")

        # Case 3: Nobody pairs: 6, 7, 8, 9 with capacity 10 -> 4 groups
        out = compile_and_run_cpp(code, "4 10\n6 7 8 9\n")
        self.assertEqual(out, "4")

        # Case 4: Exact capacity: 1+9=10, 2+8=10 -> 2 groups
        out = compile_and_run_cpp(code, "4 10\n1 9 2 8\n")
        self.assertEqual(out, "2")

        # Case 5: Duplicate weights: all 5s with capacity 10 -> 3 groups of 2
        out = compile_and_run_cpp(code, "6 10\n5 5 5 5 5 5\n")
        self.assertEqual(out, "3")

        # Case 6: Mixed odd count: 2, 3, 5, 7, 8 -> pairs (2,8), (3,7), alone (5) -> 3 groups
        out = compile_and_run_cpp(code, "5 10\n2 3 5 7 8\n")
        self.assertEqual(out, "3")

    def test_vocabulary_generalization(self):
        """Verify solver derives capacity pairing across diverse domain vocabularies."""
        for name, text in [
            ("boat rescue", BOAT_RESCUE_VARIANT),
            ("package container", PACKAGE_CONTAINER_VARIANT),
            ("vehicle cargo", VEHICLE_CARGO_VARIANT),
            ("formal partition", FORMAL_PARTITION_VARIANT),
        ]:
            with self.subTest(variant=name):
                res = self.bridge.solve(text)
                self.assertEqual(
                    res["status"], "success",
                    f"Failed on vocabulary variant '{name}': {res.get('limitationMessage')}"
                )
                self.assertEqual(res["selectedPattern"], "greedy_capacity_pairing")

    def test_negative_discrimination_activity_selection(self):
        """Activity selection must NOT resolve to capacity pairing."""
        res = self.bridge.solve(ACTIVITY_SELECTION_CONTRAST)
        self.assertNotEqual(res.get("selectedPattern"), "greedy_capacity_pairing")

    def test_negative_discrimination_two_sum(self):
        """Two sum equality search must resolve to two_pointer_pair_sum, not capacity pairing."""
        res = self.bridge.solve(TWO_SUM_CONTRAST)
        self.assertNotEqual(res.get("selectedPattern"), "greedy_capacity_pairing")

    def test_negative_discrimination_general_knapsack_bin_packing(self):
        """General bin packing (cardinality unbounded) must fail closed, not use pair greedy."""
        res = self.bridge.solve(GENERAL_BIN_PACKING_CONTRAST)
        self.assertNotEqual(res.get("selectedPattern"), "greedy_capacity_pairing")

    def test_ipc_bridge_integration(self):
        """Verify pointer_algorithms/bridge.py handle_request routes to capacity pairing."""
        req = {
            "action": "solve",
            "problemText": FERRIS_WHEEL_CANONICAL
        }
        res = handle_request(req)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["selectedPattern"], "greedy_capacity_pairing")
        self.assertIn("while (left <= right)", res["code"])


if __name__ == '__main__':
    unittest.main()
