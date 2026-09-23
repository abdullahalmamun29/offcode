"""
CHUP Phase 3K — Dynamic Programming Adversarial Edge Cases Suite.
Tests 15 adversarial, boundary, and degenerate inputs against DP implementations:
ADV-DP-01 through ADV-DP-15.
"""

import sys
import os
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.dp.verification.dp_oracles import (
    dp_1d_linear_oracle, dp_prefix_suffix_oracle, dp_2d_grid_oracle,
    dp_string_alignment_oracle, dp_interval_oracle, dp_knapsack_01_oracle,
    dp_knapsack_unbounded_oracle, dp_tree_oracle, dp_bitmask_oracle,
    dp_digit_oracle, dp_state_machine_oracle, dp_dag_longest_path_oracle
)

ADVERSARIAL_TESTS = [
    {
        "id": "ADV-DP-01",
        "title": "Single element linear DP",
        "test": lambda: dp_1d_linear_oracle([42]) == 42
    },
    {
        "id": "ADV-DP-02",
        "title": "All negative elements in linear DP (clipped to 0)",
        "test": lambda: dp_1d_linear_oracle([-5, -10, -3]) == 0
    },
    {
        "id": "ADV-DP-03",
        "title": "Empty array linear DP",
        "test": lambda: dp_1d_linear_oracle([]) == 0
    },
    {
        "id": "ADV-DP-04",
        "title": "Knapsack with capacity W = 0",
        "test": lambda: dp_knapsack_01_oracle([2, 3, 5], [10, 20, 30], 0) == 0
    },
    {
        "id": "ADV-DP-05",
        "title": "Knapsack with all items heavier than W",
        "test": lambda: dp_knapsack_01_oracle([10, 20, 30], [100, 200, 300], 5) == 0
    },
    {
        "id": "ADV-DP-06",
        "title": "2D Grid 1x1 base case",
        "test": lambda: dp_2d_grid_oracle([[99]]) == 99
    },
    {
        "id": "ADV-DP-07",
        "title": "2D Grid 1xN single row",
        "test": lambda: dp_2d_grid_oracle([[1, 2, 3, 4]]) == 10
    },
    {
        "id": "ADV-DP-08",
        "title": "2D Grid Nx1 single column",
        "test": lambda: dp_2d_grid_oracle([[1], [2], [3], [4]]) == 10
    },
    {
        "id": "ADV-DP-09",
        "title": "LCS with empty string",
        "test": lambda: dp_string_alignment_oracle("", "abcdef") == 0
    },
    {
        "id": "ADV-DP-10",
        "title": "LCS with identical strings",
        "test": lambda: dp_string_alignment_oracle("dynamic", "dynamic") == 7
    },
    {
        "id": "ADV-DP-11",
        "title": "Interval DP single element (no merge cost)",
        "test": lambda: dp_interval_oracle([100]) == 0
    },
    {
        "id": "ADV-DP-12",
        "title": "Tree DP single node",
        "test": lambda: dp_tree_oracle(1, [], [88]) == 88
    },
    {
        "id": "ADV-DP-13",
        "title": "Bitmask TSP single city",
        "test": lambda: dp_bitmask_oracle(1, [[0]]) == 0
    },
    {
        "id": "ADV-DP-14",
        "title": "Digit DP point interval [X, X]",
        "test": lambda: dp_digit_oracle(42, 42) == 1
    },
    {
        "id": "ADV-DP-15",
        "title": "State machine stock with strictly decreasing prices",
        "test": lambda: dp_state_machine_oracle([10, 9, 8, 7, 6]) == 0
    },
]


def run_all_dp_adversarial_tests() -> Dict[str, Any]:
    total = len(ADVERSARIAL_TESTS)
    passed = 0
    failures = []

    print(f"\n========================================================")
    print(f"  CHUP Phase 3K — Dynamic Programming Adversarial Suite")
    print(f"  Total Cases: {total} (ADV-DP-01 through ADV-DP-15)")
    print(f"========================================================\n")

    for tc in ADVERSARIAL_TESTS:
        tid = tc["id"]
        title = tc["title"]
        try:
            ok = tc["test"]()
            if ok:
                passed += 1
                print(f"  [PASS] {tid} - {title}")
            else:
                failures.append((tid, "Assertion returned False"))
                print(f"  [FAIL] {tid} - {title}: Test returned False")
        except Exception as e:
            failures.append((tid, str(e)))
            print(f"  [FAIL] {tid} - {title}: Exception {e}")

    summary = {
        "total": total,
        "passed": passed,
        "failures": failures
    }

    print("\n--------------------------------------------------------")
    print(f"  Adversarial Results: {passed}/{total} passed ({passed/total*100:.1f}%)")
    print("--------------------------------------------------------\n")

    return summary


if __name__ == "__main__":
    summary = run_all_dp_adversarial_tests()
    if summary["failures"]:
        sys.exit(1)
