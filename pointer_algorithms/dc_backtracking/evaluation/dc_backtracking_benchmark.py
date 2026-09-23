"""
CHUP Phase 3M — Divide & Conquer, Backtracking, and Exponential Decomposition Benchmark.

Evaluates recognition, structural reasoning, invariant verification,
code generation, and execution across 10 core families (3M-A through 3M-J, 60 problems):

3M-A: Merge Sort & Cross-Boundary Counting (DC-01..DC-06)
3M-B: Quickselect & Selection by Partition (DC-07..DC-12)
3M-C: Closest Pair / Geometric D&C (DC-13..DC-18)
3M-D: Centroid Decomposition (DC-19..DC-24)
3M-E: CDQ Offline Divide & Conquer (DC-25..DC-30)
3M-F: Combinatorial Backtracking (DC-31..DC-36)
3M-G: Constraint Satisfaction & Exact Cover (DC-37..DC-42)
3M-H: Branch & Bound (DC-43..DC-48)
3M-I: State-Space Search (DC-49..DC-54)
3M-J: Meet in the Middle (DC-55..DC-60)
"""

import sys
import os
import subprocess
import tempfile
import hashlib
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.dc_backtracking.verification.dc_backtracking_oracles import (
    dc_merge_sort_inversions_oracle,
    dc_quickselect_oracle,
    dc_closest_pair_oracle,
    dc_tree_centroid_oracle,
    dc_cdq_divide_and_conquer_oracle,
    backtracking_subsets_permutations_oracle,
    backtracking_constraint_satisfaction_oracle,
    backtracking_branch_and_bound_oracle,
    backtracking_state_space_search_oracle,
    backtracking_meet_in_the_middle_oracle
)

COMPILED_BINARIES: Dict[str, str] = {}

def compile_and_run_cpp(code: str, stdin_data: str, timeout: int = 10) -> str:
    code_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()
    exe = COMPILED_BINARIES.get(code_hash)
    if not exe or not os.path.exists(exe):
        tmp_cpp = tempfile.NamedTemporaryFile(suffix=".cpp", delete=False)
        tmp_cpp.write(code.encode("utf-8"))
        tmp_cpp.close()
        exe = tmp_cpp.name[:-4]
        compile_res = subprocess.run(
            ["g++", "-std=c++17", "-O2", tmp_cpp.name, "-o", exe],
            capture_output=True, text=True
        )
        if compile_res.returncode != 0:
            return f"COMPILE_ERROR: {compile_res.stderr[:200]}"
        COMPILED_BINARIES[code_hash] = exe
    try:
        run_res = subprocess.run(
            [exe], input=stdin_data, capture_output=True, text=True, timeout=timeout
        )
        if run_res.returncode != 0:
            return f"RUNTIME_ERROR: {run_res.stderr[:200]}"
        return run_res.stdout.strip()
    except subprocess.TimeoutExpired:
        return "RUNTIME_ERROR: TimeoutExpired"


BENCHMARK_PROBLEMS = [
    # ── 3M-A: Merge Sort & Cross-Boundary Counting ──
    {
        "id": "DC-01",
        "category": "3M-A",
        "title": "Classic Inversion Count",
        "text": "Count the number of inversions in array using merge sort divide and conquer.",
        "expected_pattern": "dc_merge_sort_inversions",
        "input": "4\n8 4 2 1",
        "oracle_fn": lambda: str(dc_merge_sort_inversions_oracle([8, 4, 2, 1]))
    },
    {
        "id": "DC-02",
        "category": "3M-A",
        "title": "Already Sorted Array",
        "text": "Inversion counting on already sorted array with merge sort.",
        "expected_pattern": "dc_merge_sort_inversions",
        "input": "5\n1 2 3 4 5",
        "oracle_fn": lambda: str(dc_merge_sort_inversions_oracle([1, 2, 3, 4, 5]))
    },
    {
        "id": "DC-03",
        "category": "3M-A",
        "title": "Strictly Decreasing Array",
        "text": "Merge sort inversion count on strictly decreasing sequence.",
        "expected_pattern": "dc_merge_sort_inversions",
        "input": "5\n5 4 3 2 1",
        "oracle_fn": lambda: str(dc_merge_sort_inversions_oracle([5, 4, 3, 2, 1]))
    },
    {
        "id": "DC-04",
        "category": "3M-A",
        "title": "Array with Duplicates",
        "text": "Inversion counting with identical elements using merge sort cross-boundary counting.",
        "expected_pattern": "dc_merge_sort_inversions",
        "input": "4\n2 4 1 2",
        "oracle_fn": lambda: str(dc_merge_sort_inversions_oracle([2, 4, 1, 2]))
    },
    {
        "id": "DC-05",
        "category": "3M-A",
        "title": "Single Element Base Case",
        "text": "Merge sort inversion count on a single element.",
        "expected_pattern": "dc_merge_sort_inversions",
        "input": "1\n42",
        "oracle_fn": lambda: str(dc_merge_sort_inversions_oracle([42]))
    },
    {
        "id": "DC-06",
        "category": "3M-A",
        "title": "Anti-Pattern: Subproblems Not Independent",
        "text": "Divide and conquer but subproblems are not independent and share mutable state.",
        "expected_rejection": "DC_SUBPROBLEMS_NOT_INDEPENDENT",
        "is_anti_pattern": True
    },

    # ── 3M-B: Quickselect & Selection by Partition ──
    {
        "id": "DC-07",
        "category": "3M-B",
        "title": "Kth Smallest Element",
        "text": "Find kth smallest element in an unsorted array using quickselect linear time selection.",
        "expected_pattern": "dc_quickselect",
        "input": "6 2\n7 10 4 3 20 15",
        "oracle_fn": lambda: str(dc_quickselect_oracle([7, 10, 4, 3, 20, 15], 2))
    },
    {
        "id": "DC-08",
        "category": "3M-B",
        "title": "Minimum Element via Quickselect",
        "text": "Quickselect order statistic finding index 0 smallest element in unsorted array.",
        "expected_pattern": "dc_quickselect",
        "input": "5 0\n5 2 8 1 9",
        "oracle_fn": lambda: str(dc_quickselect_oracle([5, 2, 8, 1, 9], 0))
    },
    {
        "id": "DC-09",
        "category": "3M-B",
        "title": "Maximum Element via Quickselect",
        "text": "Quickselect selection by partition finding maximum element without sorting.",
        "expected_pattern": "dc_quickselect",
        "input": "5 4\n5 2 8 1 9",
        "oracle_fn": lambda: str(dc_quickselect_oracle([5, 2, 8, 1, 9], 4))
    },
    {
        "id": "DC-10",
        "category": "3M-B",
        "title": "Quickselect with Many Duplicates",
        "text": "Quickselect 3-way partition on array with multiple duplicate values.",
        "expected_pattern": "dc_quickselect",
        "input": "6 3\n3 2 3 1 2 4",
        "oracle_fn": lambda: str(dc_quickselect_oracle([3, 2, 3, 1, 2, 4], 3))
    },
    {
        "id": "DC-11",
        "category": "3M-B",
        "title": "Quickselect Single Element",
        "text": "Quickselect on single element array base case.",
        "expected_pattern": "dc_quickselect",
        "input": "1 0\n100",
        "oracle_fn": lambda: str(dc_quickselect_oracle([100], 0))
    },
    {
        "id": "DC-12",
        "category": "3M-B",
        "title": "Anti-Pattern: Dynamic Online Kth Element",
        "text": "Quickselect on dynamic online updates with kth element queries in streaming data.",
        "expected_rejection": "DYNAMIC_UPDATES_PRESENT",
        "is_anti_pattern": True
    },

    # ── 3M-C: Closest Pair / Geometric D&C ──
    {
        "id": "DC-13",
        "category": "3M-C",
        "title": "Closest Pair 2D Points",
        "text": "Find closest pair of points in 2D Euclidean plane using geometric divide and conquer.",
        "expected_pattern": "dc_closest_pair",
        "input": "3\n0 0\n1 1\n5 5",
        "oracle_fn": lambda: f"{dc_closest_pair_oracle([(0, 0), (1, 1), (5, 5)]):.6f}"
    },
    {
        "id": "DC-14",
        "category": "3M-C",
        "title": "Points on a Line",
        "text": "Closest pair of points positioned horizontally along the x-axis.",
        "expected_pattern": "dc_closest_pair",
        "input": "4\n0 0\n3 0\n10 0\n1 0",
        "oracle_fn": lambda: f"{dc_closest_pair_oracle([(0, 0), (3, 0), (10, 0), (1, 0)]):.6f}"
    },
    {
        "id": "DC-15",
        "category": "3M-C",
        "title": "Closest Pair in Grid",
        "text": "Closest pair of points in small grid using geometric divide and conquer.",
        "expected_pattern": "dc_closest_pair",
        "input": "4\n0 0\n0 2\n2 0\n2 2",
        "oracle_fn": lambda: f"{dc_closest_pair_oracle([(0, 0), (0, 2), (2, 0), (2, 2)]):.6f}"
    },
    {
        "id": "DC-16",
        "category": "3M-C",
        "title": "Two Points Base Case",
        "text": "Closest pair of points with exactly two points.",
        "expected_pattern": "dc_closest_pair",
        "input": "2\n1 1\n4 5",
        "oracle_fn": lambda: f"{dc_closest_pair_oracle([(1, 1), (4, 5)]):.6f}"
    },
    {
        "id": "DC-17",
        "category": "3M-C",
        "title": "Three Points Base Case",
        "text": "Closest pair of points with exactly three points.",
        "expected_pattern": "dc_closest_pair",
        "input": "3\n0 0\n3 4\n1 1",
        "oracle_fn": lambda: f"{dc_closest_pair_oracle([(0, 0), (3, 4), (1, 1)]):.6f}"
    },
    {
        "id": "DC-18",
        "category": "3M-C",
        "title": "Anti-Pattern: Combine Step Intractable",
        "text": "Divide and conquer where combine step requires O(2^n) time.",
        "expected_rejection": "DC_COMBINE_STEP_INTRACTABLE",
        "is_anti_pattern": True
    },

    # ── 3M-D: Centroid Decomposition ──
    {
        "id": "DC-19",
        "category": "3M-D",
        "title": "Tree Paths of Length K",
        "text": "Count paths in a tree with length <= k using centroid decomposition.",
        "expected_pattern": "dc_tree_centroid",
        "input": "3 1\n1 2\n2 3",
        "oracle_fn": lambda: str(dc_tree_centroid_oracle(3, [(1, 2, 1), (2, 3, 1)], 1))
    },
    {
        "id": "DC-20",
        "category": "3M-D",
        "title": "Star Graph Centroid",
        "text": "Centroid decomposition on star tree graph to count paths.",
        "expected_pattern": "dc_tree_centroid",
        "input": "5 1\n1 2\n1 3\n1 4\n1 5",
        "oracle_fn": lambda: str(dc_tree_centroid_oracle(5, [(1, 2, 1), (1, 3, 1), (1, 4, 1), (1, 5, 1)], 1))
    },
    {
        "id": "DC-21",
        "category": "3M-D",
        "title": "Line Tree Centroid",
        "text": "Path counting in tree with centroid decomposition on line graph.",
        "expected_pattern": "dc_tree_centroid",
        "input": "4 2\n1 2\n2 3\n3 4",
        "oracle_fn": lambda: str(dc_tree_centroid_oracle(4, [(1, 2, 1), (2, 3, 1), (3, 4, 1)], 2))
    },
    {
        "id": "DC-22",
        "category": "3M-D",
        "title": "Binary Tree Centroid",
        "text": "Divide tree at centroid to compute paths of length <= k.",
        "expected_pattern": "dc_tree_centroid",
        "input": "7 2\n1 2\n1 3\n2 4\n2 5\n3 6\n3 7",
        "oracle_fn": lambda: str(dc_tree_centroid_oracle(7, [(1, 2, 1), (1, 3, 1), (2, 4, 1), (2, 5, 1), (3, 6, 1), (3, 7, 1)], 2))
    },
    {
        "id": "DC-23",
        "category": "3M-D",
        "title": "Single Edge Tree",
        "text": "Tree centroid decomposition on 2-node tree.",
        "expected_pattern": "dc_tree_centroid",
        "input": "2 1\n1 2",
        "oracle_fn": lambda: str(dc_tree_centroid_oracle(2, [(1, 2, 1)], 1))
    },
    {
        "id": "DC-24",
        "category": "3M-D",
        "title": "Anti-Pattern: Base Case Undefined",
        "text": "Divide and conquer where base case is undefined leading to infinite recursion.",
        "expected_rejection": "DC_BASE_CASE_UNDEFINED",
        "is_anti_pattern": True
    },

    # ── 3M-E: CDQ Offline Divide & Conquer ──
    {
        "id": "DC-25",
        "category": "3M-E",
        "title": "3D Partial Order Counting",
        "text": "Count elements dominated in 3 dimensions using cdq divide and conquer.",
        "expected_pattern": "dc_cdq_divide_and_conquer",
        "input": "3\n1 2 3\n2 3 4\n1 1 1",
        "oracle_fn": lambda: "\n".join(str(x) for x in dc_cdq_divide_and_conquer_oracle([(1, 2, 3), (2, 3, 4), (1, 1, 1)]))
    },
    {
        "id": "DC-26",
        "category": "3M-E",
        "title": "Identical Elements CDQ",
        "text": "CDQ divide and conquer 3D partial order on elements with identical coordinates.",
        "expected_pattern": "dc_cdq_divide_and_conquer",
        "input": "2\n2 2 2\n2 2 2",
        "oracle_fn": lambda: "\n".join(str(x) for x in dc_cdq_divide_and_conquer_oracle([(2, 2, 2), (2, 2, 2)]))
    },
    {
        "id": "DC-27",
        "category": "3M-E",
        "title": "Single Element CDQ",
        "text": "CDQ divide and conquer on single element base case.",
        "expected_pattern": "dc_cdq_divide_and_conquer",
        "input": "1\n5 5 5",
        "oracle_fn": lambda: "0"
    },
    {
        "id": "DC-28",
        "category": "3M-E",
        "title": "Strictly Increasing Chain",
        "text": "3d partial order cdq divide and conquer with chain of increasing tuples.",
        "expected_pattern": "dc_cdq_divide_and_conquer",
        "input": "3\n1 1 1\n2 2 2\n3 3 3",
        "oracle_fn": lambda: "\n".join(str(x) for x in dc_cdq_divide_and_conquer_oracle([(1, 1, 1), (2, 2, 2), (3, 3, 3)]))
    },
    {
        "id": "DC-29",
        "category": "3M-E",
        "title": "Inverted Dimensions CDQ",
        "text": "Offline divide and conquer for multi-dimensional queries using cdq.",
        "expected_pattern": "dc_cdq_divide_and_conquer",
        "input": "3\n3 1 2\n2 2 1\n1 3 3",
        "oracle_fn": lambda: "\n".join(str(x) for x in dc_cdq_divide_and_conquer_oracle([(3, 1, 2), (2, 2, 1), (1, 3, 3)]))
    },
    {
        "id": "DC-30",
        "category": "3M-E",
        "title": "Section 8 Gate: Tower Problem",
        "text": "You are given n cubes. Build towers by placing each cube on an existing tower. Find minimum number of towers.",
        "expected_rejection": "COMPOSITION_UNSUPPORTED",
        "is_anti_pattern": True
    },

    # ── 3M-F: Combinatorial Backtracking ──
    {
        "id": "DC-31",
        "category": "3M-F",
        "title": "Subsets with Duplicates",
        "text": "Generate all subsets with duplicates using combinatorial backtracking.",
        "expected_pattern": "backtracking_subsets_permutations",
        "input": "3\n1 2 2",
        "oracle_fn": lambda: "Total Subsets: 6"
    },
    {
        "id": "DC-32",
        "category": "3M-F",
        "title": "Distinct Elements Subsets",
        "text": "Generate all subsets from distinct numbers using combinatorial backtracking.",
        "expected_pattern": "backtracking_subsets_permutations",
        "input": "3\n1 2 3",
        "oracle_fn": lambda: "Total Subsets: 8"
    },
    {
        "id": "DC-33",
        "category": "3M-F",
        "title": "All Identical Elements Subsets",
        "text": "Backtracking subsets with duplicates where all elements are identical.",
        "expected_pattern": "backtracking_subsets_permutations",
        "input": "3\n2 2 2",
        "oracle_fn": lambda: "Total Subsets: 4"
    },
    {
        "id": "DC-34",
        "category": "3M-F",
        "title": "Single Element Subsets",
        "text": "Combinatorial backtracking subsets on single element.",
        "expected_pattern": "backtracking_subsets_permutations",
        "input": "1\n5",
        "oracle_fn": lambda: "Total Subsets: 2"
    },
    {
        "id": "DC-35",
        "category": "3M-F",
        "title": "Empty Set Subsets",
        "text": "Backtracking subsets with duplicates base case.",
        "expected_pattern": "backtracking_subsets_permutations",
        "input": "2\n1 2",
        "oracle_fn": lambda: "Total Subsets: 4"
    },
    {
        "id": "DC-36",
        "category": "3M-F",
        "title": "Anti-Pattern: Search Space Explosive",
        "text": "Backtracking with search space explosive and insufficient pruning.",
        "expected_rejection": "BACKTRACKING_SEARCH_SPACE_EXPLOSIVE",
        "is_anti_pattern": True
    },

    # ── 3M-G: Constraint Satisfaction & Exact Cover ──
    {
        "id": "DC-37",
        "category": "3M-G",
        "title": "4-Queens Puzzle",
        "text": "Solve N-Queens puzzle with constraint satisfaction for n=4.",
        "expected_pattern": "backtracking_constraint_satisfaction",
        "input": "4",
        "oracle_fn": lambda: str(backtracking_constraint_satisfaction_oracle(4))
    },
    {
        "id": "DC-38",
        "category": "3M-G",
        "title": "8-Queens Classic",
        "text": "Solve N-Queens puzzle with constraint satisfaction for standard 8x8 chessboard.",
        "expected_pattern": "backtracking_constraint_satisfaction",
        "input": "8",
        "oracle_fn": lambda: str(backtracking_constraint_satisfaction_oracle(8))
    },
    {
        "id": "DC-39",
        "category": "3M-G",
        "title": "1-Queen Base Case",
        "text": "N-Queens constraint satisfaction for n=1.",
        "expected_pattern": "backtracking_constraint_satisfaction",
        "input": "1",
        "oracle_fn": lambda: str(backtracking_constraint_satisfaction_oracle(1))
    },
    {
        "id": "DC-40",
        "category": "3M-G",
        "title": "2-Queens Infeasible",
        "text": "N-Queens constraint satisfaction for n=2 where no solution exists.",
        "expected_pattern": "backtracking_constraint_satisfaction",
        "input": "2",
        "oracle_fn": lambda: str(backtracking_constraint_satisfaction_oracle(2))
    },
    {
        "id": "DC-41",
        "category": "3M-G",
        "title": "6-Queens Constraint Propagation",
        "text": "Solve N-Queens puzzle with constraint satisfaction for n=6.",
        "expected_pattern": "backtracking_constraint_satisfaction",
        "input": "6",
        "oracle_fn": lambda: str(backtracking_constraint_satisfaction_oracle(6))
    },
    {
        "id": "DC-42",
        "category": "3M-G",
        "title": "Anti-Pattern: Greedy Choice Sufficient",
        "text": "Backtracking search but greedy sufficient because greedy choice property holds.",
        "expected_rejection": "BACKTRACKING_GREEDY_SUFFICIENT",
        "is_anti_pattern": True
    },

    # ── 3M-H: Branch & Bound ──
    {
        "id": "DC-43",
        "category": "3M-H",
        "title": "0/1 Knapsack Branch and Bound",
        "text": "Find optimal subset using branch and bound with upper bound pruning.",
        "expected_pattern": "backtracking_branch_and_bound",
        "input": "3 50\n10 60\n20 100\n30 120",
        "oracle_fn": lambda: str(backtracking_branch_and_bound_oracle([60, 100, 120], [10, 20, 30], 50))
    },
    {
        "id": "DC-44",
        "category": "3M-H",
        "title": "All Items Feasible",
        "text": "Branch and bound knapsack where capacity exceeds all items.",
        "expected_pattern": "backtracking_branch_and_bound",
        "input": "2 100\n10 50\n20 80",
        "oracle_fn": lambda: str(backtracking_branch_and_bound_oracle([50, 80], [10, 20], 100))
    },
    {
        "id": "DC-45",
        "category": "3M-H",
        "title": "No Items Feasible",
        "text": "Branch and bound knapsack where every item exceeds capacity.",
        "expected_pattern": "backtracking_branch_and_bound",
        "input": "2 5\n10 50\n20 80",
        "oracle_fn": lambda: str(backtracking_branch_and_bound_oracle([50, 80], [10, 20], 5))
    },
    {
        "id": "DC-46",
        "category": "3M-H",
        "title": "Single Item Exactly Fits",
        "text": "Branch and bound knapsack with single item matching capacity.",
        "expected_pattern": "backtracking_branch_and_bound",
        "input": "1 15\n15 100",
        "oracle_fn": lambda: str(backtracking_branch_and_bound_oracle([100], [15], 15))
    },
    {
        "id": "DC-47",
        "category": "3M-H",
        "title": "Tight Bound Pruning",
        "text": "Branch & bound optimization with upper bound pruning.",
        "expected_pattern": "backtracking_branch_and_bound",
        "input": "4 16\n2 40\n5 30\n10 50\n5 10",
        "oracle_fn": lambda: str(backtracking_branch_and_bound_oracle([40, 30, 50, 10], [2, 5, 10, 5], 16))
    },
    {
        "id": "DC-48",
        "category": "3M-H",
        "title": "Anti-Pattern: DP Sufficient",
        "text": "Backtracking search but overlapping subproblems admit dp.",
        "expected_rejection": "BACKTRACKING_DP_SUFFICIENT",
        "is_anti_pattern": True
    },

    # ── 3M-I: State-Space Search ──
    {
        "id": "DC-49",
        "category": "3M-I",
        "title": "Word Search in Grid Match",
        "text": "Word search in 2D grid using state space search with visited tracking.",
        "expected_pattern": "backtracking_state_space_search",
        "input": "3 4\nABCE\nSFCS\nADEE\nABCCED",
        "oracle_fn": lambda: "true"
    },
    {
        "id": "DC-50",
        "category": "3M-I",
        "title": "Word Search Mismatch",
        "text": "Grid word search state space search for absent word.",
        "expected_pattern": "backtracking_state_space_search",
        "input": "3 4\nABCE\nSFCS\nADEE\nABCB",
        "oracle_fn": lambda: "false"
    },
    {
        "id": "DC-51",
        "category": "3M-I",
        "title": "Single Cell Word Search",
        "text": "State-space search for 1-character word in single cell grid.",
        "expected_pattern": "backtracking_state_space_search",
        "input": "1 1\nA\nA",
        "oracle_fn": lambda: "true"
    },
    {
        "id": "DC-52",
        "category": "3M-I",
        "title": "Single Cell Word Mismatch",
        "text": "Word search state space search single cell mismatch.",
        "expected_pattern": "backtracking_state_space_search",
        "input": "1 1\nA\nB",
        "oracle_fn": lambda: "false"
    },
    {
        "id": "DC-53",
        "category": "3M-I",
        "title": "Snake Word Search",
        "text": "State space search following winding snake word in grid.",
        "expected_pattern": "backtracking_state_space_search",
        "input": "3 3\nABC\nFED\nGHI\nABCDEFGHI",
        "oracle_fn": lambda: "true"
    },
    {
        "id": "DC-54",
        "category": "3M-I",
        "title": "Anti-Pattern: Resource Limit Exceeded",
        "text": "Backtracking search with recursion depth limit exceeded and resource limit exceeded.",
        "expected_rejection": "BACKTRACKING_RESOURCE_LIMIT",
        "is_anti_pattern": True
    },

    # ── 3M-J: Meet in the Middle ──
    {
        "id": "DC-55",
        "category": "3M-J",
        "title": "Subset Sum N=40 Split",
        "text": "Subset sum with N<=40 using meet in the middle search space bisection.",
        "expected_pattern": "backtracking_meet_in_the_middle",
        "input": "6 15\n1 3 9 2 7 12",
        "oracle_fn": lambda: str(backtracking_meet_in_the_middle_oracle([1, 3, 9, 2, 7, 12], 15))
    },
    {
        "id": "DC-56",
        "category": "3M-J",
        "title": "Zero Target Subset Sum",
        "text": "Meet in the middle subset sum finding subsets summing to 0.",
        "expected_pattern": "backtracking_meet_in_the_middle",
        "input": "4 0\n1 2 -1 -2",
        "oracle_fn": lambda: str(backtracking_meet_in_the_middle_oracle([1, 2, -1, -2], 0))
    },
    {
        "id": "DC-57",
        "category": "3M-J",
        "title": "Unreachable Target Sum",
        "text": "Meet in the middle subset sum with target exceeding all elements.",
        "expected_pattern": "backtracking_meet_in_the_middle",
        "input": "3 100\n1 2 3",
        "oracle_fn": lambda: str(backtracking_meet_in_the_middle_oracle([1, 2, 3], 100))
    },
    {
        "id": "DC-58",
        "category": "3M-J",
        "title": "Exact Single Match",
        "text": "Meet in the middle split search space with single matching combination.",
        "expected_pattern": "backtracking_meet_in_the_middle",
        "input": "4 10\n1 2 3 4",
        "oracle_fn": lambda: str(backtracking_meet_in_the_middle_oracle([1, 2, 3, 4], 10))
    },
    {
        "id": "DC-59",
        "category": "3M-J",
        "title": "Single Element Meet in Middle",
        "text": "Meet in the middle bisection with single element.",
        "expected_pattern": "backtracking_meet_in_the_middle",
        "input": "1 5\n5",
        "oracle_fn": lambda: str(backtracking_meet_in_the_middle_oracle([5], 5))
    },
    {
        "id": "DC-60",
        "category": "3M-J",
        "title": "Section 8 Gate: Tower Composition Gate",
        "text": "Tower problem: place each cube on an existing tower. Minimum towers.",
        "expected_rejection": "COMPOSITION_UNSUPPORTED",
        "is_anti_pattern": True
    },
]


def run_benchmark():
    passed = 0
    failed = 0
    total = len(BENCHMARK_PROBLEMS)

    print("=" * 80)
    print("CHUP Phase 3M — Divide & Conquer, Backtracking & Exponential Decomposition Benchmark")
    print(f"Total problems: {total} (10 families, 6 problems each)")
    print("=" * 80)

    for prob in BENCHMARK_PROBLEMS:
        pid = prob["id"]
        cat = prob["category"]
        title = prob["title"]
        text = prob["text"]
        is_anti = prob.get("is_anti_pattern", False)

        res = handle_request({"action": "solve", "problemText": text})

        if is_anti:
            expected_rej = prob["expected_rejection"]
            elim_codes = [e["rejectionCode"] for e in res.get("eliminatedCandidates", []) if e.get("rejectionCode")]
            if expected_rej in elim_codes or res.get("status") == "rejected":
                passed += 1
                print(f"[{cat}] {pid} PASS: Correctly rejected with {expected_rej} ({title})")
            else:
                failed += 1
                print(f"[{cat}] {pid} FAIL: Expected rejection {expected_rej}, got status={res['status']}, elim={elim_codes} ({title})")
        else:
            expected_pat = prob["expected_pattern"]
            if res["status"] != "success":
                failed += 1
                print(f"[{cat}] {pid} FAIL: Bridge returned status={res['status']}, reasoning={res.get('reasoning')} ({title})")
                continue

            if res["selectedPattern"] != expected_pat:
                failed += 1
                print(f"[{cat}] {pid} FAIL: Expected pattern {expected_pat}, got {res['selectedPattern']} ({title})")
                continue

            code = res.get("code", "")
            stdin_data = prob.get("input", "")
            cpp_output = compile_and_run_cpp(code, stdin_data)
            expected_output = prob["oracle_fn"]()

            if "COMPILE_ERROR" in cpp_output or "RUNTIME_ERROR" in cpp_output:
                failed += 1
                print(f"[{cat}] {pid} FAIL: C++ execution error: {cpp_output} ({title})")
                continue

            # Compare output
            if cpp_output == expected_output or (cat == "3M-F" and expected_output in cpp_output):
                passed += 1
                print(f"[{cat}] {pid} PASS: {title} (Pattern={expected_pat}, Output={cpp_output})")
            else:
                failed += 1
                print(f"[{cat}] {pid} FAIL: Output mismatch: expected {expected_output}, got {cpp_output} ({title})")

    print("=" * 80)
    print(f"Benchmark Results: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("=" * 80)
    return passed == total


if __name__ == "__main__":
    success = run_benchmark()
    sys.exit(0 if success else 1)
