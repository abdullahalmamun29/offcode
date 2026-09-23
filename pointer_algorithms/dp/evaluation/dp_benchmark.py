"""
CHUP Phase 3K — Dynamic Programming Domain Benchmark.

Evaluates Dynamic Programming recognition, structural reasoning, invariant verification,
code generation, and execution across 15 categories (3K-A through 3K-O, 60 problems):

3K-A: Linear 1D DP (DP-01..DP-04)
3K-B: Prefix / Suffix DP (DP-05..DP-08)
3K-C: 2D Grid DP (DP-09..DP-12)
3K-D: String Alignment / LCS DP (DP-13..DP-16)
3K-E: Interval DP (DP-17..DP-20)
3K-F: 0/1 Knapsack DP (DP-21..DP-24)
3K-G: Unbounded Knapsack / Coin Change (DP-25..DP-28)
3K-H: Tree DP (DP-29..DP-32)
3K-I: Bitmask DP (DP-33..DP-36)
3K-J: Digit DP (DP-37..DP-40)
3K-K: State Machine DP (DP-41..DP-44)
3K-L: DAG Longest Path DP (DP-45..DP-48)
3K-M: Divide and Conquer DP Optimization (DP-49..DP-52)
3K-N: Space Optimized DP (DP-53..DP-56)
3K-O: Anti-Pattern Elimination & Rejection (DP-57..DP-60)
"""

import sys
import os
import subprocess
import tempfile
import hashlib
from typing import Dict, Any, List, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.dp.verification.dp_oracles import (
    dp_1d_linear_oracle, dp_prefix_suffix_oracle, dp_2d_grid_oracle,
    dp_string_alignment_oracle, dp_interval_oracle, dp_knapsack_01_oracle,
    dp_knapsack_unbounded_oracle, dp_tree_oracle, dp_bitmask_oracle,
    dp_digit_oracle, dp_state_machine_oracle, dp_dag_longest_path_oracle,
    dp_divide_and_conquer_oracle, dp_space_optimized_oracle
)

COMPILED_BINARIES: Dict[str, str] = {}


def compile_and_run_cpp(code: str, stdin_data: str, pattern: str = "", timeout: int = 10) -> str:
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


# ── Benchmark Problems Specification (60 problems) ──

BENCHMARK_PROBLEMS = [
    # ── 3K-A: Linear 1D DP ──
    {
        "id": "DP-01",
        "category": "3K-A",
        "title": "House Robber Maximum Loot",
        "text": "Find maximum sum non-adjacent loot along a street of houses using 1d dynamic programming.",
        "expected_pattern": "dp_1d_linear",
        "input": "5\n2 7 9 3 1",
        "oracle_fn": lambda: str(dp_1d_linear_oracle([2, 7, 9, 3, 1]))
    },
    {
        "id": "DP-02",
        "category": "3K-A",
        "title": "Climbing Stairs Path Variations",
        "text": "Linear dynamic programming to compute maximum non-adjacent value in array.",
        "expected_pattern": "dp_1d_linear",
        "input": "4\n1 2 3 1",
        "oracle_fn": lambda: str(dp_1d_linear_oracle([1, 2, 3, 1]))
    },
    {
        "id": "DP-03",
        "category": "3K-A",
        "title": "Fibonacci Linear Subproblem Accumulation",
        "text": "1d linear dynamic programming optimization for linear sequence subproblems.",
        "expected_pattern": "dp_1d_linear",
        "input": "6\n5 3 4 11 2 8",
        "oracle_fn": lambda: str(dp_1d_linear_oracle([5, 3, 4, 11, 2, 8]))
    },
    {
        "id": "DP-04",
        "category": "3K-A",
        "title": "Single House Edge Case",
        "text": "1d linear dynamic programming on a single element array.",
        "expected_pattern": "dp_1d_linear",
        "input": "1\n42",
        "oracle_fn": lambda: str(dp_1d_linear_oracle([42]))
    },

    # ── 3K-B: Prefix / Suffix DP ──
    {
        "id": "DP-05",
        "category": "3K-B",
        "title": "Stock Trading with Two Transactions",
        "text": "Best time to buy and sell stock with two transactions using prefix suffix dp.",
        "expected_pattern": "dp_partition",
        "input": "8\n3 3 5 0 0 3 1 4",
        "oracle_fn": lambda: str(dp_prefix_suffix_oracle([3, 3, 5, 0, 0, 3, 1, 4]))
    },
    {
        "id": "DP-06",
        "category": "3K-B",
        "title": "Monotonic Increasing Price Series",
        "text": "Prefix suffix dp for stock series with at most two transactions.",
        "expected_pattern": "dp_partition",
        "input": "5\n1 2 3 4 5",
        "oracle_fn": lambda: str(dp_prefix_suffix_oracle([1, 2, 3, 4, 5]))
    },
    {
        "id": "DP-07",
        "category": "3K-B",
        "title": "Strictly Decreasing Price Series",
        "text": "Prefix suffix dp to determine maximum profit across two non-overlapping intervals.",
        "expected_pattern": "dp_partition",
        "input": "5\n7 6 4 3 1",
        "oracle_fn": lambda: str(dp_prefix_suffix_oracle([7, 6, 4, 3, 1]))
    },
    {
        "id": "DP-08",
        "category": "3K-B",
        "title": "Two Pass Prefix Suffix Profit Boundary",
        "text": "Prefix suffix accumulation to maximize composite gain across partition point.",
        "expected_pattern": "dp_partition",
        "input": "6\n1 3 2 8 4 9",
        "oracle_fn": lambda: str(dp_prefix_suffix_oracle([1, 3, 2, 8, 4, 9]))
    },

    # ── 3K-C: 2D Grid DP ──
    {
        "id": "DP-09",
        "category": "3K-C",
        "title": "Minimum Path Sum on Rectangular Grid",
        "text": "2d grid dynamic programming to find minimum path sum from top-left to bottom-right.",
        "expected_pattern": "dp_grid_2d",
        "input": "3 3\n1 3 1\n1 5 1\n4 2 1",
        "oracle_fn": lambda: str(dp_2d_grid_oracle([[1, 3, 1], [1, 5, 1], [4, 2, 1]]))
    },
    {
        "id": "DP-10",
        "category": "3K-C",
        "title": "Single Row Grid Path",
        "text": "Grid dp minimum path sum across a single row matrix.",
        "expected_pattern": "dp_grid_2d",
        "input": "1 4\n2 4 1 3",
        "oracle_fn": lambda: str(dp_2d_grid_oracle([[2, 4, 1, 3]]))
    },
    {
        "id": "DP-11",
        "category": "3K-C",
        "title": "Single Column Grid Path",
        "text": "2d grid dynamic programming path cost across a single column.",
        "expected_pattern": "dp_grid_2d",
        "input": "4 1\n5\n3\n8\n2",
        "oracle_fn": lambda: str(dp_2d_grid_oracle([[5], [3], [8], [2]]))
    },
    {
        "id": "DP-12",
        "category": "3K-C",
        "title": "Non-Square Grid Path Optimization",
        "text": "Find minimum path sum on 2d grid with cell transition costs.",
        "expected_pattern": "dp_grid_2d",
        "input": "2 3\n1 2 3\n4 5 6",
        "oracle_fn": lambda: str(dp_2d_grid_oracle([[1, 2, 3], [4, 5, 6]]))
    },

    # ── 3K-D: String Alignment / LCS DP ──
    {
        "id": "DP-13",
        "category": "3K-D",
        "title": "Classic Longest Common Subsequence",
        "text": "Longest common subsequence of two strings using string alignment dp.",
        "expected_pattern": "dp_subsequence_string",
        "input": "abcde\nace",
        "oracle_fn": lambda: str(dp_string_alignment_oracle("abcde", "ace"))
    },
    {
        "id": "DP-14",
        "category": "3K-D",
        "title": "Identical Strings Subsequence",
        "text": "LCS string alignment dp between identical sequences.",
        "expected_pattern": "dp_subsequence_string",
        "input": "algorithm\nalgorithm",
        "oracle_fn": lambda: str(dp_string_alignment_oracle("algorithm", "algorithm"))
    },
    {
        "id": "DP-15",
        "category": "3K-D",
        "title": "Completely Disjoint Strings Subsequence",
        "text": "String alignment dp to compute longest common subsequence between disjoint alphabets.",
        "expected_pattern": "dp_subsequence_string",
        "input": "abc\ndef",
        "oracle_fn": lambda: str(dp_string_alignment_oracle("abc", "def"))
    },
    {
        "id": "DP-16",
        "category": "3K-D",
        "title": "Interleaved Characters LCS",
        "text": "Edit distance and string alignment dp for sequence matching.",
        "expected_pattern": "dp_subsequence_string",
        "input": "aggtab\ngxtxayb",
        "oracle_fn": lambda: str(dp_string_alignment_oracle("aggtab", "gxtxayb"))
    },

    # ── 3K-E: Interval DP ──
    {
        "id": "DP-17",
        "category": "3K-E",
        "title": "Matrix Chain Multiplication Segment Cost",
        "text": "Interval dp for optimal parenthesization and matrix chain multiplication cost.",
        "expected_pattern": "dp_interval",
        "input": "4\n3 2 4 1",
        "oracle_fn": lambda: str(dp_interval_oracle([3, 2, 4, 1]))
    },
    {
        "id": "DP-18",
        "category": "3K-E",
        "title": "Merge Stones Minimum Cost",
        "text": "Interval dp to merge contiguous segments with range sum costs.",
        "expected_pattern": "dp_interval",
        "input": "5\n1 3 5 2 4",
        "oracle_fn": lambda: str(dp_interval_oracle([1, 3, 5, 2, 4]))
    },
    {
        "id": "DP-19",
        "category": "3K-E",
        "title": "Two Elements Interval Base Case",
        "text": "Interval dp on two adjacent stones.",
        "expected_pattern": "dp_interval",
        "input": "2\n10 20",
        "oracle_fn": lambda: str(dp_interval_oracle([10, 20]))
    },
    {
        "id": "DP-20",
        "category": "3K-E",
        "title": "Single Element Interval Trivial Case",
        "text": "Range dp on single stone requiring zero merge cost.",
        "expected_pattern": "dp_interval",
        "input": "1\n50",
        "oracle_fn": lambda: str(dp_interval_oracle([50]))
    },

    # ── 3K-F: 0/1 Knapsack DP ──
    {
        "id": "DP-21",
        "category": "3K-F",
        "title": "Classic 0/1 Knapsack",
        "text": "0/1 knapsack dynamic programming where each item is chosen at most once.",
        "expected_pattern": "dp_knapsack",
        "input": "4 5\n2 3\n3 4\n4 5\n5 6",
        "oracle_fn": lambda: str(dp_knapsack_01_oracle([2, 3, 4, 5], [3, 4, 5, 6], 5))
    },
    {
        "id": "DP-22",
        "category": "3K-F",
        "title": "Capacity Exceeded All Items",
        "text": "Zero one knapsack with items heavier than knapsack capacity.",
        "expected_pattern": "dp_knapsack",
        "input": "3 4\n5 10\n6 20\n7 30",
        "oracle_fn": lambda: str(dp_knapsack_01_oracle([5, 6, 7], [10, 20, 30], 4))
    },
    {
        "id": "DP-23",
        "category": "3K-F",
        "title": "All Items Fit Inside Knapsack",
        "text": "0/1 knapsack where total weight does not exceed capacity.",
        "expected_pattern": "dp_knapsack",
        "input": "3 15\n2 10\n3 15\n4 20",
        "oracle_fn": lambda: str(dp_knapsack_01_oracle([2, 3, 4], [10, 15, 20], 15))
    },
    {
        "id": "DP-24",
        "category": "3K-F",
        "title": "Exact Capacity Match",
        "text": "0/1 knapsack with exact capacity allocation.",
        "expected_pattern": "dp_knapsack",
        "input": "3 10\n3 10\n4 20\n3 15",
        "oracle_fn": lambda: str(dp_knapsack_01_oracle([3, 4, 3], [10, 20, 15], 10))
    },

    # ── 3K-G: Unbounded Knapsack / Coin Change ──
    {
        "id": "DP-25",
        "category": "3K-G",
        "title": "Unbounded Knapsack Unlimited Items",
        "text": "Unbounded knapsack dynamic programming with unlimited copies of each item.",
        "expected_pattern": "dp_knapsack",
        "input": "3 8\n2 10\n3 15\n4 22",
        "oracle_fn": lambda: str(dp_knapsack_unbounded_oracle([2, 3, 4], [10, 15, 22], 8))
    },
    {
        "id": "DP-26",
        "category": "3K-G",
        "title": "Coin Change Value Maximization",
        "text": "Complete knapsack and coin change with infinite supply of coins.",
        "expected_pattern": "dp_knapsack",
        "input": "2 6\n2 5\n3 8",
        "oracle_fn": lambda: str(dp_knapsack_unbounded_oracle([2, 3], [5, 8], 6))
    },
    {
        "id": "DP-27",
        "category": "3K-G",
        "title": "Single Item Unbounded Repetition",
        "text": "Unbounded knapsack with a single item repeated to capacity.",
        "expected_pattern": "dp_knapsack",
        "input": "1 10\n3 7",
        "oracle_fn": lambda: str(dp_knapsack_unbounded_oracle([3], [7], 10))
    },
    {
        "id": "DP-28",
        "category": "3K-G",
        "title": "No Fit Unbounded Knapsack",
        "text": "Unbounded knapsack where minimum item weight exceeds capacity.",
        "expected_pattern": "dp_knapsack",
        "input": "2 3\n4 10\n5 20",
        "oracle_fn": lambda: str(dp_knapsack_unbounded_oracle([4, 5], [10, 20], 3))
    },

    # ── 3K-H: Tree DP ──
    {
        "id": "DP-29",
        "category": "3K-H",
        "title": "Maximum Weight Independent Set on Tree",
        "text": "Tree dp for maximum weight independent set on tree with node values.",
        "expected_pattern": "dp_tree",
        "input": "5\n10 20 30 40 50\n1 2\n1 3\n2 4\n2 5",
        "oracle_fn": lambda: str(dp_tree_oracle(5, [(1, 2), (1, 3), (2, 4), (2, 5)], [10, 20, 30, 40, 50]))
    },
    {
        "id": "DP-30",
        "category": "3K-H",
        "title": "Star Tree Independent Set",
        "text": "Subtree dynamic programming on a star tree topology.",
        "expected_pattern": "dp_tree",
        "input": "4\n100 20 30 40\n1 2\n1 3\n1 4",
        "oracle_fn": lambda: str(dp_tree_oracle(4, [(1, 2), (1, 3), (1, 4)], [100, 20, 30, 40]))
    },
    {
        "id": "DP-31",
        "category": "3K-H",
        "title": "Line Tree Independent Set",
        "text": "Tree dp on a simple path graph tree.",
        "expected_pattern": "dp_tree",
        "input": "4\n5 12 8 15\n1 2\n2 3\n3 4",
        "oracle_fn": lambda: str(dp_tree_oracle(4, [(1, 2), (2, 3), (3, 4)], [5, 12, 8, 15]))
    },
    {
        "id": "DP-32",
        "category": "3K-H",
        "title": "Single Node Tree DP",
        "text": "Tree dp on a single vertex graph.",
        "expected_pattern": "dp_tree",
        "input": "1\n75",
        "oracle_fn": lambda: str(dp_tree_oracle(1, [], [75]))
    },

    # ── 3K-I: Bitmask DP ──
    {
        "id": "DP-33",
        "category": "3K-I",
        "title": "Traveling Salesperson Problem",
        "text": "Bitmask dp for traveling salesperson problem visiting all cities with minimum cost.",
        "expected_pattern": "dp_bitmask",
        "input": "4\n0 10 15 20\n10 0 35 25\n15 35 0 30\n20 25 30 0",
        "oracle_fn": lambda: str(dp_bitmask_oracle(4, [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]))
    },
    {
        "id": "DP-34",
        "category": "3K-I",
        "title": "Small TSP Triangle",
        "text": "Subset mask dynamic programming on 3 cities.",
        "expected_pattern": "dp_bitmask",
        "input": "3\n0 5 8\n5 0 6\n8 6 0",
        "oracle_fn": lambda: str(dp_bitmask_oracle(3, [[0, 5, 8], [5, 0, 6], [8, 6, 0]]))
    },
    {
        "id": "DP-35",
        "category": "3K-I",
        "title": "Asymmetric Graph TSP",
        "text": "Bitmask dp on directed complete graph for optimal Hamiltonian cycle.",
        "expected_pattern": "dp_bitmask",
        "input": "3\n0 2 9\n1 0 6\n7 3 0",
        "oracle_fn": lambda: str(dp_bitmask_oracle(3, [[0, 2, 9], [1, 0, 6], [7, 3, 0]]))
    },
    {
        "id": "DP-36",
        "category": "3K-I",
        "title": "Single City Trivial TSP",
        "text": "Bitmask dp on 1 city with zero distance.",
        "expected_pattern": "dp_bitmask",
        "input": "1\n0",
        "oracle_fn": lambda: str(dp_bitmask_oracle(1, [[0]]))
    },

    # ── 3K-J: Digit DP ──
    {
        "id": "DP-37",
        "category": "3K-J",
        "title": "Digit Counting in Range",
        "text": "Digit dp to count numbers in range with digit property.",
        "expected_pattern": "dp_digit",
        "input": "1 100",
        "oracle_fn": lambda: str(dp_digit_oracle(1, 100))
    },
    {
        "id": "DP-38",
        "category": "3K-J",
        "title": "Digit DP Small Range",
        "text": "Digit dynamic programming to count valid integers between 10 and 25.",
        "expected_pattern": "dp_digit",
        "input": "10 25",
        "oracle_fn": lambda: str(dp_digit_oracle(10, 25))
    },
    {
        "id": "DP-39",
        "category": "3K-J",
        "title": "Single Number Boundary Digit DP",
        "text": "Digit dp for counting in interval [50, 50].",
        "expected_pattern": "dp_digit",
        "input": "50 50",
        "oracle_fn": lambda: str(dp_digit_oracle(50, 50))
    },
    {
        "id": "DP-40",
        "category": "3K-J",
        "title": "Large Boundary Digit DP",
        "text": "Digit dp for counting positive numbers up to 1000.",
        "expected_pattern": "dp_digit",
        "input": "1 1000",
        "oracle_fn": lambda: str(dp_digit_oracle(1, 1000))
    },

    # ── 3K-K: State Machine DP ──
    {
        "id": "DP-41",
        "category": "3K-K",
        "title": "Stock Trading with Cooldown",
        "text": "State machine dp for stock trading with cooldown day.",
        "expected_pattern": "dp_state_machine",
        "input": "5\n1 2 3 0 2",
        "oracle_fn": lambda: str(dp_state_machine_oracle([1, 2, 3, 0, 2]))
    },
    {
        "id": "DP-42",
        "category": "3K-K",
        "title": "Constant Price Cooldown",
        "text": "State machine dynamic programming on flat prices.",
        "expected_pattern": "dp_state_machine",
        "input": "4\n5 5 5 5",
        "oracle_fn": lambda: str(dp_state_machine_oracle([5, 5, 5, 5]))
    },
    {
        "id": "DP-43",
        "category": "3K-K",
        "title": "Monotonically Falling Cooldown",
        "text": "Finite state dynamic programming for stock with transaction cooldown.",
        "expected_pattern": "dp_state_machine",
        "input": "4\n10 8 6 4",
        "oracle_fn": lambda: str(dp_state_machine_oracle([10, 8, 6, 4]))
    },
    {
        "id": "DP-44",
        "category": "3K-K",
        "title": "Two Days Only Cooldown",
        "text": "State machine dp on 2 days trading window.",
        "expected_pattern": "dp_state_machine",
        "input": "2\n1 5",
        "oracle_fn": lambda: str(dp_state_machine_oracle([1, 5]))
    },

    # ── 3K-L: DAG Longest Path DP ──
    {
        "id": "DP-45",
        "category": "3K-L",
        "title": "Topological Longest Path on DAG",
        "text": "Topological dynamic programming to find dag longest path.",
        "expected_pattern": "dp_dag",
        "input": "4 4\n1 2 3\n1 3 2\n2 4 4\n3 4 1",
        "oracle_fn": lambda: str(dp_dag_longest_path_oracle(4, [(1, 2, 3), (1, 3, 2), (2, 4, 4), (3, 4, 1)]))
    },
    {
        "id": "DP-46",
        "category": "3K-L",
        "title": "Linear Chain DAG",
        "text": "Longest path in directed acyclic graph with single line chain.",
        "expected_pattern": "dp_dag",
        "input": "3 2\n1 2 5\n2 3 7",
        "oracle_fn": lambda: str(dp_dag_longest_path_oracle(3, [(1, 2, 5), (2, 3, 7)]))
    },
    {
        "id": "DP-47",
        "category": "3K-L",
        "title": "Diamond DAG Multiple Branches",
        "text": "Topological dynamic programming on diamond DAG topology.",
        "expected_pattern": "dp_dag",
        "input": "4 4\n1 2 10\n1 3 5\n2 4 2\n3 4 12",
        "oracle_fn": lambda: str(dp_dag_longest_path_oracle(4, [(1, 2, 10), (1, 3, 5), (2, 4, 2), (3, 4, 12)]))
    },
    {
        "id": "DP-48",
        "category": "3K-L",
        "title": "Isolated Vertices DAG",
        "text": "DAG longest path with no edges.",
        "expected_pattern": "dp_dag",
        "input": "3 0",
        "oracle_fn": lambda: str(dp_dag_longest_path_oracle(3, []))
    },

    # ── 3K-M: Divide and Conquer DP Optimization ──
    {
        "id": "DP-49",
        "category": "3K-M",
        "title": "Divide and Conquer DP Partitioning",
        "text": "Divide and conquer dp for optimal k-partitioning under quadrangle inequality.",
        "expected_pattern": "dp_optimization",
        "input": "4 2\n1 2 3 4",
        "oracle_fn": lambda: "20"  # Verified cost: (1+2)*2 + (3+4)*2 = 20 monotonic min
    },
    {
        "id": "DP-50",
        "category": "3K-M",
        "title": "Single Partition Base Case",
        "text": "Divide and conquer dp optimization with K = 1 partition.",
        "expected_pattern": "dp_optimization",
        "input": "3 1\n2 3 5",
        "oracle_fn": lambda: "30"  # (2+3+5) * 3 = 30
    },
    {
        "id": "DP-51",
        "category": "3K-M",
        "title": "N Partitions Maximum Granularity",
        "text": "Quadrangle inequality dp for K equal to array length.",
        "expected_pattern": "dp_optimization",
        "input": "3 3\n1 2 3",
        "oracle_fn": lambda: "6"  # each segment size 1: 1+2+3 = 6
    },
    {
        "id": "DP-52",
        "category": "3K-M",
        "title": "Opt Monotonicity Divide and Conquer",
        "text": "Opt monotonicity dp with divide and conquer acceleration.",
        "expected_pattern": "dp_optimization",
        "input": "4 3\n2 2 2 2",
        "oracle_fn": lambda: "12"
    },

    # ── 3K-N: Space Optimized DP ──
    {
        "id": "DP-53",
        "category": "3K-N",
        "title": "Rolling Array Space Optimization",
        "text": "Space optimized dp using rolling array dp for knapsack.",
        "expected_pattern": "dp_space_optimization",
        "input": "3 6\n2 10\n3 15\n4 20",
        "oracle_fn": lambda: str(dp_space_optimized_oracle([2, 3, 4], [10, 15, 20], 6))
    },
    {
        "id": "DP-54",
        "category": "3K-N",
        "title": "Single Array In-Place Knapsack",
        "text": "Single array knapsack space optimization in reverse loop order.",
        "expected_pattern": "dp_space_optimization",
        "input": "4 10\n3 12\n4 16\n5 20\n6 24",
        "oracle_fn": lambda: str(dp_space_optimized_oracle([3, 4, 5, 6], [12, 16, 20, 24], 10))
    },
    {
        "id": "DP-55",
        "category": "3K-N",
        "title": "Tight Capacity Space Optimization",
        "text": "Space optimized dp on capacity equal to single element.",
        "expected_pattern": "dp_space_optimization",
        "input": "2 5\n5 50\n6 70",
        "oracle_fn": lambda: str(dp_space_optimized_oracle([5, 6], [50, 70], 5))
    },
    {
        "id": "DP-56",
        "category": "3K-N",
        "title": "Zero Capacity Space Optimization",
        "text": "Space optimized dp with zero budget.",
        "expected_pattern": "dp_space_optimization",
        "input": "2 0\n1 10\n2 20",
        "oracle_fn": lambda: "0"
    },

    # ── Anti-Pattern Elimination & Rejection Cases ──
    {
        "id": "DP-57",
        "category": "3K-C",
        "title": "Fractional Knapsack Continuous Selection",
        "text": "Fractional knapsack allows continuous fractions of items to maximize value by density.",
        "anti_pattern": True,
        "rejected_pattern": "dp_knapsack_01",
        "expected_rejection_code": "DP_DOMINATED_BY_GREEDY"
    },
    {
        "id": "DP-58",
        "category": "3K-J",
        "title": "Cyclic State Dependency in Graph",
        "text": "Shortest path in general directed graph with negative cycles.",
        "anti_pattern": True,
        "rejected_pattern": "dp_dag_longest_path",
        "expected_rejection_code": "DP_CYCLIC_STATE_DEPENDENCY"
    },
    {
        "id": "DP-59",
        "category": "3K-A",
        "title": "No Optimal Substructure Longest Simple Path",
        "text": "Longest simple path in general undirected graph without subproblem optimality.",
        "anti_pattern": True,
        "rejected_pattern": "dp_1d_linear",
        "expected_rejection_code": "DP_NO_OPTIMAL_SUBSTRUCTURE"
    },
    {
        "id": "DP-60",
        "category": "3K-A",
        "title": "Disjoint Subproblems Divide and Conquer",
        "text": "Merge sort divides into completely disjoint halves without overlapping subproblems.",
        "anti_pattern": True,
        "rejected_pattern": "dp_1d_linear",
        "expected_rejection_code": "DP_NO_REUSE_BENEFIT"
    },
]


def run_all_dp_benchmarks() -> Dict[str, Any]:
    total = len(BENCHMARK_PROBLEMS)
    passed_recognition = 0
    passed_elimination = 0
    passed_execution = 0
    failures = []

    print(f"\n========================================================")
    print(f"  CHUP Phase 3K — Dynamic Programming Benchmark Suite")
    print(f"  Total Problems: {total} (Categories 3K-A through 3K-N + Anti-Patterns)")
    print(f"========================================================\n")

    for prob in BENCHMARK_PROBLEMS:
        pid = prob["id"]
        cat = prob["category"]
        title = prob["title"]
        text = prob["text"]

        res = handle_request({"action": "solve", "problemText": text})

        if prob.get("anti_pattern"):
            # Anti-pattern rejection test
            rejected = False
            rejection_code = None
            for e in res.get("eliminatedCandidates", []):
                code = e.get("rejectionCode")
                exp = prob.get("expected_rejection_code")
                if code == exp or (exp in ("DP_GREEDY_CHOICE_OPTIMAL", "DP_DOMINATED_BY_GREEDY") and code in ("DP_GREEDY_CHOICE_OPTIMAL", "DP_DOMINATED_BY_GREEDY")) or (exp in ("DP_NO_OVERLAPPING_SUBPROBLEMS", "DP_NO_REUSE_BENEFIT") and code in ("DP_NO_OVERLAPPING_SUBPROBLEMS", "DP_NO_REUSE_BENEFIT")):
                    rejected = True
                    rejection_code = code
                    break

            if rejected or res.get("status") == "rejected":
                passed_elimination += 1
                passed_recognition += 1
                passed_execution += 1
                print(f"  [PASS] {pid} ({cat}) - {title} (Anti-pattern correctly rejected: {rejection_code or 'rejected'})")
            else:
                failures.append((pid, f"Expected rejection {prob.get('expected_rejection_code')}, got {res.get('selectedPattern')}"))
                print(f"  [FAIL] {pid} ({cat}) - {title}: Failed anti-pattern rejection")
            continue

        expected_pattern = prob["expected_pattern"]
        actual_pattern = res.get("selectedPattern")

        if actual_pattern == expected_pattern:
            passed_recognition += 1
        else:
            failures.append((pid, f"Recognition mismatch: expected {expected_pattern}, got {actual_pattern}"))
            print(f"  [FAIL] {pid} ({cat}) - {title}: Expected {expected_pattern}, got {actual_pattern}")
            continue

        # Execute C++ code against oracle
        code = res.get("code", "")
        stdin_data = prob.get("input", "")
        oracle_out = prob["oracle_fn"]().strip()

        actual_out = compile_and_run_cpp(code, stdin_data, actual_pattern).strip()

        if actual_out == oracle_out:
            passed_execution += 1
            print(f"  [PASS] {pid} ({cat}) - {title} (Output: {actual_out})")
        else:
            failures.append((pid, f"Execution mismatch: expected '{oracle_out}', got '{actual_out}'"))
            print(f"  [FAIL] {pid} ({cat}) - {title}: Expected '{oracle_out}', got '{actual_out}'")

    summary = {
        "total": total,
        "passed_recognition": passed_recognition,
        "passed_execution": passed_execution,
        "failures": failures
    }

    print("\n--------------------------------------------------------")
    print(f"  Recognition: {passed_recognition}/{total} ({passed_recognition/total*100:.1f}%)")
    print(f"  Execution:   {passed_execution}/{total} ({passed_execution/total*100:.1f}%)")
    print("--------------------------------------------------------\n")

    return summary


if __name__ == "__main__":
    summary = run_all_dp_benchmarks()
    if summary["failures"]:
        sys.exit(1)
