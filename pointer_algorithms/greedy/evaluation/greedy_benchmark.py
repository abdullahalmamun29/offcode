"""
CHUP Phase 3L — Greedy Algorithms Domain Benchmark.

Evaluates Greedy recognition, structural reasoning, invariant verification,
code generation, and execution across 10 core families (3L-A through 3L-J, 60 problems):

3L-A: Interval Selection / Activity Scheduling (GR-01..GR-06)
3L-B: Interval Covering / Minimum Points (GR-07..GR-12)
3L-C: Fractional Knapsack / Divisible Resources (GR-13..GR-18)
3L-D: Deadline / Scheduling Greedy (GR-19..GR-24)
3L-E: Heap-Assisted Greedy (GR-25..GR-30)
3L-F: Huffman / Optimal Merge (GR-31..GR-36)
3L-G: Sequence / String Local-Choice (GR-37..GR-42)
3L-H: Reachability / Partition Greedy (GR-43..GR-48)
3L-I: Graph-Greedy MST Integration (GR-49..GR-54)
3L-J: General Exchange / Dominance Greedy (GR-55..GR-60)
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
from pointer_algorithms.greedy.verification.greedy_oracles import (
    greedy_interval_selection_oracle,
    greedy_interval_covering_oracle,
    greedy_fractional_knapsack_oracle,
    greedy_deadline_scheduling_oracle,
    greedy_heap_assisted_oracle,
    greedy_huffman_merge_oracle,
    greedy_sequence_local_choice_oracle,
    greedy_reachability_partition_oracle,
    greedy_graph_mst_oracle,
    greedy_general_exchange_oracle
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
    # ── 3L-A: Interval Selection / Activity Scheduling ──
    {
        "id": "GR-01",
        "category": "3L-A",
        "title": "Classic Activity Selection Earliest Finish",
        "text": "Select maximum number of compatible non-overlapping intervals using earliest finish time greedy activity selection.",
        "expected_pattern": "greedy_interval_selection",
        "input": "4\n1 4\n3 5\n0 6\n5 7",
        "oracle_fn": lambda: str(greedy_interval_selection_oracle([(1, 4), (3, 5), (0, 6), (5, 7)]))
    },
    {
        "id": "GR-02",
        "category": "3L-A",
        "title": "All Overlapping Intervals",
        "text": "Activity selection on completely overlapping intervals where finish times determine singular choice.",
        "expected_pattern": "greedy_interval_selection",
        "input": "3\n1 10\n2 9\n3 8",
        "oracle_fn": lambda: str(greedy_interval_selection_oracle([(1, 10), (2, 9), (3, 8)]))
    },
    {
        "id": "GR-03",
        "category": "3L-A",
        "title": "Disjoint Adjacent Intervals",
        "text": "Interval scheduling with adjacent touching intervals that are mutually compatible.",
        "expected_pattern": "greedy_interval_selection",
        "input": "4\n0 2\n2 4\n4 6\n6 8",
        "oracle_fn": lambda: str(greedy_interval_selection_oracle([(0, 2), (2, 4), (4, 6), (6, 8)]))
    },
    {
        "id": "GR-04",
        "category": "3L-A",
        "title": "Identical Intervals Tie Handling",
        "text": "Interval scheduling with multiple identical intervals to test tie-breaking stability.",
        "expected_pattern": "greedy_interval_selection",
        "input": "3\n1 5\n1 5\n1 5",
        "oracle_fn": lambda: str(greedy_interval_selection_oracle([(1, 5), (1, 5), (1, 5)]))
    },
    {
        "id": "GR-05",
        "category": "3L-A",
        "title": "Single Interval Base Case",
        "text": "Activity selection with a single isolated interval.",
        "expected_pattern": "greedy_interval_selection",
        "input": "1\n5 10",
        "oracle_fn": lambda: str(greedy_interval_selection_oracle([(5, 10)]))
    },
    {
        "id": "GR-06",
        "category": "3L-A",
        "title": "Anti-Pattern: Weighted Interval Scheduling",
        "text": "Weighted interval scheduling: find maximum total weight of compatible non-overlapping intervals.",
        "expected_rejection": "GREEDY_EXCHANGE_PROOF_FAILED",
        "is_anti_pattern": True
    },

    # ── 3L-B: Interval Covering / Minimum Points ──
    {
        "id": "GR-07",
        "category": "3L-B",
        "title": "Burst Balloons Minimum Arrows",
        "text": "Find minimum number of arrows or points to burst and cover all intervals.",
        "expected_pattern": "greedy_interval_covering",
        "input": "4\n10 16\n2 8\n1 6\n7 12",
        "oracle_fn": lambda: str(greedy_interval_covering_oracle([(10, 16), (2, 8), (1, 6), (7, 12)]))
    },
    {
        "id": "GR-08",
        "category": "3L-B",
        "title": "Completely Disjoint Intervals",
        "text": "Interval covering on disjoint separated intervals requiring distinct points.",
        "expected_pattern": "greedy_interval_covering",
        "input": "3\n1 2\n3 4\n5 6",
        "oracle_fn": lambda: str(greedy_interval_covering_oracle([(1, 2), (3, 4), (5, 6)]))
    },
    {
        "id": "GR-09",
        "category": "3L-B",
        "title": "Nested Intervals Shared Stabbing Point",
        "text": "Interval stabbing where nested intervals share a single rightmost stabbing point.",
        "expected_pattern": "greedy_interval_covering",
        "input": "3\n1 10\n2 5\n3 5",
        "oracle_fn": lambda: str(greedy_interval_covering_oracle([(1, 10), (2, 5), (3, 5)]))
    },
    {
        "id": "GR-10",
        "category": "3L-B",
        "title": "Single Point Interval Covering",
        "text": "Interval covering with a single interval.",
        "expected_pattern": "greedy_interval_covering",
        "input": "1\n4 9",
        "oracle_fn": lambda: str(greedy_interval_covering_oracle([(4, 9)]))
    },
    {
        "id": "GR-11",
        "category": "3L-B",
        "title": "Touching Intervals Endpoint Tie",
        "text": "Interval covering with touching endpoints [1, 2] and [2, 3].",
        "expected_pattern": "greedy_interval_covering",
        "input": "2\n1 2\n2 3",
        "oracle_fn": lambda: str(greedy_interval_covering_oracle([(1, 2), (2, 3)]))
    },
    {
        "id": "GR-12",
        "category": "3L-B",
        "title": "Anti-Pattern: General Set Cover",
        "text": "General set cover on arbitrary subsets where interval stabbing structure is absent and proof cannot be established.",
        "expected_rejection": "GREEDY_PROOF_NOT_ESTABLISHED",
        "is_anti_pattern": True
    },

    # ── 3L-C: Fractional Knapsack / Divisible Resources ──
    {
        "id": "GR-13",
        "category": "3L-C",
        "title": "Classic Fractional Knapsack",
        "text": "Fractional knapsack with divisible items to maximize total value within capacity.",
        "expected_pattern": "greedy_fractional_knapsack",
        "input": "3 50\n60 10\n100 20\n120 30",
        "oracle_fn": lambda: f"{greedy_fractional_knapsack_oracle([(60, 10), (100, 20), (120, 30)], 50):.2f}"
    },
    {
        "id": "GR-14",
        "category": "3L-C",
        "title": "All Items Fit Inside Knapsack",
        "text": "Fractional knapsack where total weight of all divisible items is less than capacity.",
        "expected_pattern": "greedy_fractional_knapsack",
        "input": "2 100\n40 20\n50 30",
        "oracle_fn": lambda: f"{greedy_fractional_knapsack_oracle([(40, 20), (50, 30)], 100):.2f}"
    },
    {
        "id": "GR-15",
        "category": "3L-C",
        "title": "Capacity Fraction of Single Item",
        "text": "Fractional knapsack where capacity only allows taking a partial fraction of the highest density item.",
        "expected_pattern": "greedy_fractional_knapsack",
        "input": "1 15\n100 30",
        "oracle_fn": lambda: f"{greedy_fractional_knapsack_oracle([(100, 30)], 15):.2f}"
    },
    {
        "id": "GR-16",
        "category": "3L-C",
        "title": "Zero Capacity Boundary",
        "text": "Fractional knapsack with zero capacity boundary condition.",
        "expected_pattern": "greedy_fractional_knapsack",
        "input": "2 0\n10 5\n20 10",
        "oracle_fn": lambda: "0.00"
    },
    {
        "id": "GR-17",
        "category": "3L-C",
        "title": "Identical Densities Items",
        "text": "Fractional knapsack where all divisible items have identical value density.",
        "expected_pattern": "greedy_fractional_knapsack",
        "input": "2 30\n50 25\n40 20",
        "oracle_fn": lambda: f"{greedy_fractional_knapsack_oracle([(50, 25), (40, 20)], 30):.2f}"
    },
    {
        "id": "GR-18",
        "category": "3L-C",
        "title": "Anti-Pattern: 0/1 Discrete Knapsack",
        "text": "Discrete 0/1 knapsack where items are indivisible and cannot be broken into fractions.",
        "expected_rejection": "GREEDY_EXCHANGE_PROOF_FAILED",
        "is_anti_pattern": True
    },

    # ── 3L-D: Deadline / Scheduling Greedy ──
    {
        "id": "GR-19",
        "category": "3L-D",
        "title": "Minimize Maximum Lateness EDD",
        "text": "Minimize maximum lateness scheduling jobs with deadlines using earliest due date rule.",
        "expected_pattern": "greedy_deadline_scheduling",
        "input": "4\n1 2\n2 4\n1 4\n3 6",
        "oracle_fn": lambda: str(greedy_deadline_scheduling_oracle([(1, 2), (2, 4), (1, 4), (3, 6)]))
    },
    {
        "id": "GR-20",
        "category": "3L-D",
        "title": "All Deadlines Met Zero Lateness",
        "text": "Deadline scheduling where all jobs complete before their deadlines.",
        "expected_pattern": "greedy_deadline_scheduling",
        "input": "3\n2 5\n1 8\n2 12",
        "oracle_fn": lambda: str(greedy_deadline_scheduling_oracle([(2, 5), (1, 8), (2, 12)]))
    },
    {
        "id": "GR-21",
        "category": "3L-D",
        "title": "Equal Deadlines Different Durations",
        "text": "Deadline scheduling with equal deadlines to test tie handling.",
        "expected_pattern": "greedy_deadline_scheduling",
        "input": "3\n5 6\n2 6\n1 6",
        "oracle_fn": lambda: str(greedy_deadline_scheduling_oracle([(5, 6), (2, 6), (1, 6)]))
    },
    {
        "id": "GR-22",
        "category": "3L-D",
        "title": "Single Job Base Case",
        "text": "Deadline scheduling with a single job.",
        "expected_pattern": "greedy_deadline_scheduling",
        "input": "1\n5 3",
        "oracle_fn": lambda: str(greedy_deadline_scheduling_oracle([(5, 3)]))
    },
    {
        "id": "GR-23",
        "category": "3L-D",
        "title": "Strictly Increasing Lateness",
        "text": "Deadline scheduling where tight deadlines produce non-zero lateness on all jobs.",
        "expected_pattern": "greedy_deadline_scheduling",
        "input": "3\n4 2\n3 4\n2 5",
        "oracle_fn": lambda: str(greedy_deadline_scheduling_oracle([(4, 2), (3, 4), (2, 5)]))
    },
    {
        "id": "GR-24",
        "category": "3L-D",
        "title": "Anti-Pattern: Non-Canonical Coin Change",
        "text": "Greedy fails on coins: non-canonical coin system with denominations 1, 3, 4 for target 6 produces counterexample.",
        "expected_rejection": "GREEDY_COUNTEREXAMPLE_FOUND",
        "is_anti_pattern": True
    },

    # ── 3L-E: Heap-Assisted Greedy ──
    {
        "id": "GR-25",
        "category": "3L-E",
        "title": "Minimum Refueling Stops Classic",
        "text": "Heap-assisted greedy to find minimum refueling stops to reach target distance.",
        "expected_pattern": "greedy_heap_assisted",
        "input": "100 10 4\n10 60\n20 30\n30 30\n60 40",
        "oracle_fn": lambda: str(greedy_heap_assisted_oracle(100, 10, [(10, 60), (20, 30), (30, 30), (60, 40)]))
    },
    {
        "id": "GR-26",
        "category": "3L-E",
        "title": "Destination Reached Without Refueling",
        "text": "Minimum refueling stops where start fuel is already sufficient to reach target.",
        "expected_pattern": "greedy_heap_assisted",
        "input": "50 60 2\n10 20\n30 20",
        "oracle_fn": lambda: str(greedy_heap_assisted_oracle(50, 60, [(10, 20), (30, 20)]))
    },
    {
        "id": "GR-27",
        "category": "3L-E",
        "title": "Unreachable Destination Gap",
        "text": "Refueling greedy where a gap between stations causes destination to be unreachable.",
        "expected_pattern": "greedy_heap_assisted",
        "input": "100 10 1\n20 50",
        "oracle_fn": lambda: str(greedy_heap_assisted_oracle(100, 10, [(20, 50)]))
    },
    {
        "id": "GR-28",
        "category": "3L-E",
        "title": "Exact Fuel Match At Each Stop",
        "text": "Refueling greedy where fuel exactly reaches the next station.",
        "expected_pattern": "greedy_heap_assisted",
        "input": "50 10 3\n10 10\n20 10\n30 20",
        "oracle_fn": lambda: str(greedy_heap_assisted_oracle(50, 10, [(10, 10), (20, 10), (30, 20)]))
    },
    {
        "id": "GR-29",
        "category": "3L-E",
        "title": "All Stations Required",
        "text": "Refueling greedy where every available station must be used.",
        "expected_pattern": "greedy_heap_assisted",
        "input": "40 10 3\n10 10\n20 10\n30 10",
        "oracle_fn": lambda: str(greedy_heap_assisted_oracle(40, 10, [(10, 10), (20, 10), (30, 10)]))
    },
    {
        "id": "GR-30",
        "category": "3L-E",
        "title": "Single Station Sufficient",
        "text": "Refueling greedy with a single large station.",
        "expected_pattern": "greedy_heap_assisted",
        "input": "100 50 1\n50 50",
        "oracle_fn": lambda: str(greedy_heap_assisted_oracle(100, 50, [(50, 50)]))
    },

    # ── 3L-F: Huffman / Optimal Merge ──
    {
        "id": "GR-31",
        "category": "3L-F",
        "title": "Huffman Coding Optimal Merge Cost",
        "text": "Compute total cost for optimal merge pattern / Huffman coding by repeatedly merging two minimum components.",
        "expected_pattern": "greedy_huffman_merge",
        "input": "4\n4 3 2 6",
        "oracle_fn": lambda: str(greedy_huffman_merge_oracle([4, 3, 2, 6]))
    },
    {
        "id": "GR-32",
        "category": "3L-F",
        "title": "Two Elements Base Case",
        "text": "Optimal merge pattern with exactly two components.",
        "expected_pattern": "greedy_huffman_merge",
        "input": "2\n10 20",
        "oracle_fn": lambda: str(greedy_huffman_merge_oracle([10, 20]))
    },
    {
        "id": "GR-33",
        "category": "3L-F",
        "title": "All Equal Frequencies",
        "text": "Huffman coding with power-of-two equal frequencies.",
        "expected_pattern": "greedy_huffman_merge",
        "input": "4\n5 5 5 5",
        "oracle_fn": lambda: str(greedy_huffman_merge_oracle([5, 5, 5, 5]))
    },
    {
        "id": "GR-34",
        "category": "3L-F",
        "title": "Fibonacci Frequencies Merge",
        "text": "Huffman coding with Fibonacci-distributed frequencies.",
        "expected_pattern": "greedy_huffman_merge",
        "input": "5\n1 2 3 5 8",
        "oracle_fn": lambda: str(greedy_huffman_merge_oracle([1, 2, 3, 5, 8]))
    },
    {
        "id": "GR-35",
        "category": "3L-F",
        "title": "Large Single Frequency Skew",
        "text": "Optimal merge pattern with one dominant frequency.",
        "expected_pattern": "greedy_huffman_merge",
        "input": "3\n1 1 100",
        "oracle_fn": lambda: str(greedy_huffman_merge_oracle([1, 1, 100]))
    },
    {
        "id": "GR-36",
        "category": "3L-F",
        "title": "Single Element Trivial Case",
        "text": "Huffman coding with a single element requiring zero merges.",
        "expected_pattern": "greedy_huffman_merge",
        "input": "1\n42",
        "oracle_fn": lambda: "0"
    },

    # ── 3L-G: Sequence / String Local-Choice ──
    {
        "id": "GR-37",
        "category": "3L-G",
        "title": "Remove K Digits Standard",
        "text": "Remove k digits to minimize number using local choice monotonic stack greedy.",
        "expected_pattern": "greedy_sequence_local_choice",
        "input": "1432219 3",
        "oracle_fn": lambda: greedy_sequence_local_choice_oracle("1432219", 3)
    },
    {
        "id": "GR-38",
        "category": "3L-G",
        "title": "Leading Zeroes After Removal",
        "text": "Remove k digits resulting in leading zeroes that must be stripped.",
        "expected_pattern": "greedy_sequence_local_choice",
        "input": "10200 1",
        "oracle_fn": lambda: greedy_sequence_local_choice_oracle("10200", 1)
    },
    {
        "id": "GR-39",
        "category": "3L-G",
        "title": "All Digits Removed Zero",
        "text": "Remove k digits where k equals the length of the string.",
        "expected_pattern": "greedy_sequence_local_choice",
        "input": "10 2",
        "oracle_fn": lambda: "0"
    },
    {
        "id": "GR-40",
        "category": "3L-G",
        "title": "Monotonically Increasing Digits",
        "text": "Remove k digits from already ascending digits where trailing digits are dropped.",
        "expected_pattern": "greedy_sequence_local_choice",
        "input": "12345 2",
        "oracle_fn": lambda: greedy_sequence_local_choice_oracle("12345", 2)
    },
    {
        "id": "GR-41",
        "category": "3L-G",
        "title": "Monotonically Decreasing Digits",
        "text": "Remove k digits from descending digits where leading digits are dropped.",
        "expected_pattern": "greedy_sequence_local_choice",
        "input": "98765 2",
        "oracle_fn": lambda: greedy_sequence_local_choice_oracle("98765", 2)
    },
    {
        "id": "GR-42",
        "category": "3L-G",
        "title": "Zero Removals Identity",
        "text": "Remove k digits with k = 0.",
        "expected_pattern": "greedy_sequence_local_choice",
        "input": "4321 0",
        "oracle_fn": lambda: "4321"
    },

    # ── 3L-H: Reachability / Partition Greedy ──
    {
        "id": "GR-43",
        "category": "3L-H",
        "title": "Jump Game Minimum Jumps Standard",
        "text": "Find minimum jumps to reach the end of array using reachability frontier greedy.",
        "expected_pattern": "greedy_reachability_partition",
        "input": "5\n2 3 1 1 4",
        "oracle_fn": lambda: str(greedy_reachability_partition_oracle([2, 3, 1, 1, 4]))
    },
    {
        "id": "GR-44",
        "category": "3L-H",
        "title": "Single Jump to End",
        "text": "Jump game where the first element can reach the destination directly in 1 jump.",
        "expected_pattern": "greedy_reachability_partition",
        "input": "4\n5 1 1 1",
        "oracle_fn": lambda: str(greedy_reachability_partition_oracle([5, 1, 1, 1]))
    },
    {
        "id": "GR-45",
        "category": "3L-H",
        "title": "Single Element Zero Jumps",
        "text": "Jump game with a single element requiring 0 jumps.",
        "expected_pattern": "greedy_reachability_partition",
        "input": "1\n0",
        "oracle_fn": lambda: "0"
    },
    {
        "id": "GR-46",
        "category": "3L-H",
        "title": "Step By Step Unit Jumps",
        "text": "Jump game with all ones requiring step-by-step jumps.",
        "expected_pattern": "greedy_reachability_partition",
        "input": "5\n1 1 1 1 1",
        "oracle_fn": lambda: str(greedy_reachability_partition_oracle([1, 1, 1, 1, 1]))
    },
    {
        "id": "GR-47",
        "category": "3L-H",
        "title": "Exponential Jump Growth",
        "text": "Jump game with expanding jump capacities.",
        "expected_pattern": "greedy_reachability_partition",
        "input": "6\n1 2 4 1 1 1",
        "oracle_fn": lambda: str(greedy_reachability_partition_oracle([1, 2, 4, 1, 1, 1]))
    },
    {
        "id": "GR-48",
        "category": "3L-H",
        "title": "Gas Station Feasible Circuit",
        "text": "Gas station circuit reachability frontier greedy.",
        "expected_pattern": "greedy_reachability_partition",
        "input": "5\n2 3 0 1 4",
        "oracle_fn": lambda: str(greedy_reachability_partition_oracle([2, 3, 0, 1, 4]))
    },

    # ── 3L-I: Graph-Greedy MST Integration ──
    {
        "id": "GR-49",
        "category": "3L-I",
        "title": "Kruskal Minimum Spanning Tree Classic",
        "text": "Find minimum spanning tree weight using Kruskal algorithm with cut property and DSU.",
        "expected_pattern": "greedy_graph_mst",
        "input": "4 5\n1 2 1\n2 3 4\n3 4 2\n1 4 5\n2 4 3",
        "oracle_fn": lambda: str(greedy_graph_mst_oracle(4, [(1, 2, 1), (2, 3, 4), (3, 4, 2), (1, 4, 5), (2, 4, 3)]))
    },
    {
        "id": "GR-50",
        "category": "3L-I",
        "title": "Complete Graph Triangle MST",
        "text": "MST on a 3-vertex complete triangle graph.",
        "expected_pattern": "greedy_graph_mst",
        "input": "3 3\n1 2 10\n2 3 20\n1 3 30",
        "oracle_fn": lambda: str(greedy_graph_mst_oracle(3, [(1, 2, 10), (2, 3, 20), (1, 3, 30)]))
    },
    {
        "id": "GR-51",
        "category": "3L-I",
        "title": "Linear Chain Tree MST",
        "text": "MST on a graph that is already a simple tree chain.",
        "expected_pattern": "greedy_graph_mst",
        "input": "4 3\n1 2 5\n2 3 7\n3 4 9",
        "oracle_fn": lambda: str(greedy_graph_mst_oracle(4, [(1, 2, 5), (2, 3, 7), (3, 4, 9)]))
    },
    {
        "id": "GR-52",
        "category": "3L-I",
        "title": "Star Graph Center Hub MST",
        "text": "MST on a star graph with equal radial edge weights.",
        "expected_pattern": "greedy_graph_mst",
        "input": "5 4\n1 2 3\n1 3 3\n1 4 3\n1 5 3",
        "oracle_fn": lambda: str(greedy_graph_mst_oracle(5, [(1, 2, 3), (1, 3, 3), (1, 4, 3), (1, 5, 3)]))
    },
    {
        "id": "GR-53",
        "category": "3L-I",
        "title": "Duplicate Edge Weights Tie MST",
        "text": "MST on a graph with redundant duplicate weights.",
        "expected_pattern": "greedy_graph_mst",
        "input": "4 4\n1 2 2\n2 3 2\n3 4 2\n4 1 2",
        "oracle_fn": lambda: str(greedy_graph_mst_oracle(4, [(1, 2, 2), (2, 3, 2), (3, 4, 2), (4, 1, 2)]))
    },
    {
        "id": "GR-54",
        "category": "3L-I",
        "title": "Single Edge Base Case MST",
        "text": "MST on a 2-vertex single edge graph.",
        "expected_pattern": "greedy_graph_mst",
        "input": "2 1\n1 2 100",
        "oracle_fn": lambda: str(greedy_graph_mst_oracle(2, [(1, 2, 100)]))
    },

    # ── 3L-J: General Exchange / Dominance Greedy ──
    {
        "id": "GR-55",
        "category": "3L-J",
        "title": "Largest Number Composition Standard",
        "text": "Compose the largest number from array of integers using pairwise exchange comparator greedy.",
        "expected_pattern": "greedy_general_exchange",
        "input": "5\n3 30 34 5 9",
        "oracle_fn": lambda: greedy_general_exchange_oracle(["3", "30", "34", "5", "9"])
    },
    {
        "id": "GR-56",
        "category": "3L-J",
        "title": "All Zeroes Leading Digit Suppression",
        "text": "Largest number composition with all zeroes resulting in single '0'.",
        "expected_pattern": "greedy_general_exchange",
        "input": "3\n0 0 0",
        "oracle_fn": lambda: "0"
    },
    {
        "id": "GR-57",
        "category": "3L-J",
        "title": "Prefix Overlap Exchange",
        "text": "Largest number composition with prefix overlaps like '10' and '1'.",
        "expected_pattern": "greedy_general_exchange",
        "input": "2\n10 1",
        "oracle_fn": lambda: greedy_general_exchange_oracle(["10", "1"])
    },
    {
        "id": "GR-58",
        "category": "3L-J",
        "title": "Single Element Base Case",
        "text": "Largest number composition with a single string.",
        "expected_pattern": "greedy_general_exchange",
        "input": "1\n42",
        "oracle_fn": lambda: "42"
    },
    {
        "id": "GR-59",
        "category": "3L-J",
        "title": "Equal String Elements Tie",
        "text": "Largest number composition with identical string elements.",
        "expected_pattern": "greedy_general_exchange",
        "input": "3\n88 88 88",
        "oracle_fn": lambda: "888888"
    },
    {
        "id": "GR-60",
        "category": "3L-J",
        "title": "Reverse Sorted Input",
        "text": "Largest number composition with elements presented in reverse optimal order.",
        "expected_pattern": "greedy_general_exchange",
        "input": "3\n1 20 9",
        "oracle_fn": lambda: greedy_general_exchange_oracle(["1", "20", "9"])
    }
]


def run_benchmark():
    print("========================================================")
    print("  CHUP Phase 3L — Greedy Algorithms Domain Benchmark")
    print("  Total Problems: 60 (GR-01 through GR-60)")
    print("  Categories: 10 (3L-A through 3L-J)")
    print("========================================================\n")

    passed_recognition = 0
    passed_execution = 0
    total = len(BENCHMARK_PROBLEMS)

    for prob in BENCHMARK_PROBLEMS:
        prob_id = prob["id"]
        cat = prob["category"]
        title = prob["title"]
        text = prob["text"]

        res = handle_request({"action": "solve", "problemText": text})

        if prob.get("is_anti_pattern"):
            expected_rej = prob["expected_rejection"]
            eliminated = res.get("eliminatedCandidates", [])
            matched = any(e.get("rejectionCode") == expected_rej for e in eliminated)
            if matched or res.get("status") == "rejected":
                print(f"  [PASS] {prob_id} ({cat}) - {title} (Anti-pattern correctly rejected: {expected_rej})")
                passed_recognition += 1
                passed_execution += 1
            else:
                print(f"  [FAIL] {prob_id} ({cat}) - {title} (Expected rejection {expected_rej}, got: {res.get('selectedPattern')})")
            continue

        expected_pat = prob["expected_pattern"]
        selected_pat = res.get("selectedPattern")

        if selected_pat == expected_pat:
            passed_recognition += 1
            code = res.get("code", "")
            stdin_data = prob["input"]
            actual_out = compile_and_run_cpp(code, stdin_data)
            expected_out = prob["oracle_fn"]()

            if actual_out == expected_out:
                passed_execution += 1
                print(f"  [PASS] {prob_id} ({cat}) - {title} (Output: {actual_out})")
            else:
                print(f"  [FAIL-EXEC] {prob_id} ({cat}) - {title}")
                print(f"         Expected: {expected_out}")
                print(f"         Actual:   {actual_out}")
        else:
            print(f"  [FAIL-REC] {prob_id} ({cat}) - {title}")
            print(f"         Expected: {expected_pat}")
            print(f"         Actual:   {selected_pat}")

    print("\n--------------------------------------------------------")
    print(f"  Recognition: {passed_recognition}/{total} ({passed_recognition/total*100:.1f}%)")
    print(f"  Execution:   {passed_execution}/{total} ({passed_execution/total*100:.1f}%)")
    print("--------------------------------------------------------\n")

    if passed_recognition == total and passed_execution == total:
        print("ALL 60 GREEDY BENCHMARK PROBLEMS PASSED (100%)\n")
        return 0
    else:
        print("SOME BENCHMARK PROBLEMS FAILED\n")
        return 1

if __name__ == "__main__":
    sys.exit(run_benchmark())
