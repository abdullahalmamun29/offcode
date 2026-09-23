"""
CHUP Phase 3K — Dynamic Programming Stress Test Suite.
Executes 150+ randomized differential tests comparing DP implementations
against brute-force and reference oracles across diverse inputs.
"""

import sys
import os
import random
from typing import Dict, Any, List, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.dp.verification.dp_oracles import (
    dp_1d_linear_oracle, brute_force_1d_linear,
    dp_prefix_suffix_oracle, brute_force_prefix_suffix,
    dp_2d_grid_oracle, brute_force_2d_grid,
    dp_string_alignment_oracle, brute_force_string_alignment,
    dp_interval_oracle, brute_force_interval,
    dp_knapsack_01_oracle, brute_force_knapsack_01,
    dp_knapsack_unbounded_oracle, brute_force_knapsack_unbounded,
    dp_tree_oracle, brute_force_tree,
    dp_bitmask_oracle, brute_force_bitmask,
    dp_digit_oracle, brute_force_digit,
    dp_state_machine_oracle, brute_force_state_machine,
    dp_space_optimized_oracle
)


def run_dp_stress_tests() -> Dict[str, Any]:
    random.seed(42)
    total_tests = 0
    passed_tests = 0
    failures = []

    print(f"\n========================================================")
    print(f"  CHUP Phase 3K — Dynamic Programming Stress Test Suite")
    print(f"  Target: 150+ Randomized Differential Runs")
    print(f"========================================================\n")

    # 1. Linear 1D DP Differential Tests (20 runs)
    print("  [Suite 1/11] 1D Linear DP Stress (20 runs)...")
    for i in range(20):
        total_tests += 1
        n = random.randint(1, 15)
        nums = [random.randint(0, 100) for _ in range(n)]
        dp_res = dp_1d_linear_oracle(nums)
        bf_res = brute_force_1d_linear(nums)
        if dp_res == bf_res:
            passed_tests += 1
        else:
            failures.append((f"1D Linear Run {i}", f"DP={dp_res} != BF={bf_res} on {nums}"))

    # 2. Prefix / Suffix DP Differential Tests (20 runs)
    print("  [Suite 2/11] Prefix / Suffix DP Stress (20 runs)...")
    for i in range(20):
        total_tests += 1
        n = random.randint(2, 12)
        prices = [random.randint(1, 50) for _ in range(n)]
        dp_res = dp_prefix_suffix_oracle(prices)
        bf_res = brute_force_prefix_suffix(prices)
        if dp_res == bf_res:
            passed_tests += 1
        else:
            failures.append((f"Prefix/Suffix Run {i}", f"DP={dp_res} != BF={bf_res} on {prices}"))

    # 3. 2D Grid DP Differential Tests (20 runs)
    print("  [Suite 3/11] 2D Grid DP Stress (20 runs)...")
    for i in range(20):
        total_tests += 1
        r = random.randint(1, 5)
        c = random.randint(1, 5)
        grid = [[random.randint(1, 20) for _ in range(c)] for _ in range(r)]
        dp_res = dp_2d_grid_oracle(grid)
        bf_res = brute_force_2d_grid(grid)
        if dp_res == bf_res:
            passed_tests += 1
        else:
            failures.append((f"2D Grid Run {i}", f"DP={dp_res} != BF={bf_res} on {grid}"))

    # 4. String Alignment / LCS DP Differential Tests (20 runs)
    print("  [Suite 4/11] String Alignment LCS Stress (20 runs)...")
    chars = "ABCD"
    for i in range(20):
        total_tests += 1
        len1 = random.randint(1, 8)
        len2 = random.randint(1, 8)
        s1 = "".join(random.choice(chars) for _ in range(len1))
        s2 = "".join(random.choice(chars) for _ in range(len2))
        dp_res = dp_string_alignment_oracle(s1, s2)
        bf_res = brute_force_string_alignment(s1, s2)
        if dp_res == bf_res:
            passed_tests += 1
        else:
            failures.append((f"LCS Run {i}", f"DP={dp_res} != BF={bf_res} on {s1}, {s2}"))

    # 5. Interval DP Differential Tests (15 runs)
    print("  [Suite 5/11] Interval DP Stress (15 runs)...")
    for i in range(15):
        total_tests += 1
        n = random.randint(1, 8)
        nums = [random.randint(1, 20) for _ in range(n)]
        dp_res = dp_interval_oracle(nums)
        bf_res = brute_force_interval(nums)
        if dp_res == bf_res:
            passed_tests += 1
        else:
            failures.append((f"Interval Run {i}", f"DP={dp_res} != BF={bf_res} on {nums}"))

    # 6. 0/1 Knapsack Differential Tests (20 runs)
    print("  [Suite 6/11] 0/1 Knapsack DP Stress (20 runs)...")
    for i in range(20):
        total_tests += 1
        n = random.randint(1, 10)
        W = random.randint(5, 30)
        weights = [random.randint(1, 15) for _ in range(n)]
        values = [random.randint(1, 50) for _ in range(n)]
        dp_res = dp_knapsack_01_oracle(weights, values, W)
        bf_res = brute_force_knapsack_01(weights, values, W)
        space_res = dp_space_optimized_oracle(weights, values, W)
        if dp_res == bf_res and dp_res == space_res:
            passed_tests += 1
        else:
            failures.append((f"0/1 Knapsack Run {i}", f"DP={dp_res}, BF={bf_res}, Space={space_res}"))

    # 7. Unbounded Knapsack Differential Tests (20 runs)
    print("  [Suite 7/11] Unbounded Knapsack DP Stress (20 runs)...")
    for i in range(20):
        total_tests += 1
        n = random.randint(1, 4)
        W = random.randint(5, 25)
        weights = [random.randint(1, 8) for _ in range(n)]
        values = [random.randint(1, 20) for _ in range(n)]
        dp_res = dp_knapsack_unbounded_oracle(weights, values, W)
        bf_res = brute_force_knapsack_unbounded(weights, values, W)
        if dp_res == bf_res:
            passed_tests += 1
        else:
            failures.append((f"Unbounded Knapsack Run {i}", f"DP={dp_res} != BF={bf_res}"))

    # 8. Tree DP Differential Tests (15 runs)
    print("  [Suite 8/11] Tree DP Stress (15 runs)...")
    for i in range(15):
        total_tests += 1
        n = random.randint(2, 9)
        values = [random.randint(1, 50) for _ in range(n)]
        # Generate random tree
        edges = []
        for v in range(2, n + 1):
            u = random.randint(1, v - 1)
            edges.append((u, v))
        dp_res = dp_tree_oracle(n, edges, values)
        bf_res = brute_force_tree(n, edges, values)
        if dp_res == bf_res:
            passed_tests += 1
        else:
            failures.append((f"Tree DP Run {i}", f"DP={dp_res} != BF={bf_res}"))

    # 9. Bitmask DP (TSP) Differential Tests (10 runs)
    print("  [Suite 9/11] Bitmask TSP Stress (10 runs)...")
    for i in range(10):
        total_tests += 1
        n = random.randint(2, 6)
        dist = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in range(n):
                if u != v:
                    dist[u][v] = random.randint(1, 20)
        dp_res = dp_bitmask_oracle(n, dist)
        bf_res = brute_force_bitmask(n, dist)
        if dp_res == bf_res:
            passed_tests += 1
        else:
            failures.append((f"Bitmask TSP Run {i}", f"DP={dp_res} != BF={bf_res}"))

    # 10. Digit DP Differential Tests (15 runs)
    print("  [Suite 10/11] Digit DP Stress (15 runs)...")
    for i in range(15):
        total_tests += 1
        low = random.randint(1, 50)
        high = low + random.randint(1, 100)
        dp_res = dp_digit_oracle(low, high)
        bf_res = brute_force_digit(low, high)
        if dp_res == bf_res:
            passed_tests += 1
        else:
            failures.append((f"Digit DP Run {i}", f"DP={dp_res} != BF={bf_res} on [{low}, {high}]"))

    # 11. State Machine DP Differential Tests (20 runs)
    print("  [Suite 11/11] State Machine DP Stress (20 runs)...")
    for i in range(20):
        total_tests += 1
        n = random.randint(1, 10)
        prices = [random.randint(1, 30) for _ in range(n)]
        dp_res = dp_state_machine_oracle(prices)
        bf_res = brute_force_state_machine(prices)
        if dp_res == bf_res:
            passed_tests += 1
        else:
            failures.append((f"State Machine Run {i}", f"DP={dp_res} != BF={bf_res} on {prices}"))

    summary = {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failures": failures
    }

    print("\n--------------------------------------------------------")
    print(f"  Stress Test Results: {passed_tests}/{total_tests} passed ({passed_tests/total_tests*100:.1f}%)")
    print("--------------------------------------------------------\n")

    return summary


if __name__ == "__main__":
    summary = run_dp_stress_tests()
    if summary["failures"]:
        sys.exit(1)
