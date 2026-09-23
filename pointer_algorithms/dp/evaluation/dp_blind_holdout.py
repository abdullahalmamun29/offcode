"""
CHUP Phase 3K — Dynamic Programming Blind Holdout Evaluation Suite.
12 unseen, realistic competitive programming problem descriptions across DP patterns:
DPH-01 through DPH-12.
"""

import sys
import os
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.dp.evaluation.dp_benchmark import compile_and_run_cpp
from pointer_algorithms.dp.verification.dp_oracles import (
    dp_1d_linear_oracle, dp_prefix_suffix_oracle, dp_2d_grid_oracle,
    dp_string_alignment_oracle, dp_interval_oracle, dp_knapsack_01_oracle,
    dp_knapsack_unbounded_oracle, dp_tree_oracle, dp_bitmask_oracle,
    dp_digit_oracle, dp_state_machine_oracle, dp_dag_longest_path_oracle
)

BLIND_HOLDOUT_PROBLEMS = [
    {
        "id": "DPH-01",
        "title": "Cyber Defense Firewall Packet Filter",
        "text": "Optimize inspection bandwidth by selecting non-adjacent packet streams using 1d dynamic programming.",
        "expected_pattern": "dp_1d_linear",
        "input": "5\n10 2 3 15 7",
        "oracle_fn": lambda: str(dp_1d_linear_oracle([10, 2, 3, 15, 7]))
    },
    {
        "id": "DPH-02",
        "title": "Satellite Orbital Window Solar Exposure",
        "text": "Prefix suffix dp to maximize telemetry collection across at most two solar exposure intervals.",
        "expected_pattern": "dp_partition",
        "input": "6\n2 6 1 8 4 10",
        "oracle_fn": lambda: str(dp_prefix_suffix_oracle([2, 6, 1, 8, 4, 10]))
    },
    {
        "id": "DPH-03",
        "title": "Mars Rover Hazardous Terrain Path",
        "text": "Navigate planetary surface grid from top-left to bottom-right minimizing hazard cost with 2d grid dynamic programming.",
        "expected_pattern": "dp_grid_2d",
        "input": "3 3\n5 1 2\n3 8 1\n4 2 1",
        "oracle_fn": lambda: str(dp_2d_grid_oracle([[5, 1, 2], [3, 8, 1], [4, 2, 1]]))
    },
    {
        "id": "DPH-04",
        "title": "Genomic Sequence Homology Alignment",
        "text": "Evaluate longest common subsequence between DNA strings using string alignment dp.",
        "expected_pattern": "dp_subsequence_string",
        "input": "GTCGAT\nCAGT",
        "oracle_fn": lambda: str(dp_string_alignment_oracle("GTCGAT", "CAGT"))
    },
    {
        "id": "DPH-05",
        "title": "Deep Space Transmission Burst Merging",
        "text": "Interval dp to coalesce consecutive message bursts minimizing merge latency.",
        "expected_pattern": "dp_interval",
        "input": "4\n4 3 6 2",
        "oracle_fn": lambda: str(dp_interval_oracle([4, 3, 6, 2]))
    },
    {
        "id": "DPH-06",
        "title": "Emergency Relief Cargo Optimization",
        "text": "Pack emergency medical supplies under total payload capacity where each item is chosen at most once using 0/1 knapsack.",
        "expected_pattern": "dp_knapsack",
        "input": "4 7\n3 12\n4 18\n2 8\n5 25",
        "oracle_fn": lambda: str(dp_knapsack_01_oracle([3, 4, 2, 5], [12, 18, 8, 25], 7))
    },
    {
        "id": "DPH-07",
        "title": "Quantum Energy Unit Resupply",
        "text": "Unbounded knapsack dynamic programming to maximize energy with unlimited copies of each canister.",
        "expected_pattern": "dp_knapsack",
        "input": "3 9\n2 7\n3 11\n4 16",
        "oracle_fn": lambda: str(dp_knapsack_unbounded_oracle([2, 3, 4], [7, 11, 16], 9))
    },
    {
        "id": "DPH-08",
        "title": "Fiber Network Core Router Placement",
        "text": "Tree dp for maximum independent set on tree to position backbone routers without adjacent interference.",
        "expected_pattern": "dp_tree",
        "input": "5\n50 30 20 40 10\n1 2\n1 3\n3 4\n3 5",
        "oracle_fn": lambda: str(dp_tree_oracle(5, [(1, 2), (1, 3), (3, 4), (3, 5)], [50, 30, 20, 40, 10]))
    },
    {
        "id": "DPH-09",
        "title": "Drone Fleet Package Delivery TSP",
        "text": "Bitmask dp for traveling salesperson problem across distribution hubs visiting all locations.",
        "expected_pattern": "dp_bitmask",
        "input": "4\n0 20 42 35\n20 0 30 34\n42 30 0 12\n35 34 12 0",
        "oracle_fn": lambda: str(dp_bitmask_oracle(4, [[0, 20, 42, 35], [20, 0, 30, 34], [42, 30, 0, 12], [35, 34, 12, 0]]))
    },
    {
        "id": "DPH-10",
        "title": "Cryptographic Key Nonce Validation",
        "text": "Digit dp to count numbers in range with digit property for security hashes.",
        "expected_pattern": "dp_digit",
        "input": "5 500",
        "oracle_fn": lambda: str(dp_digit_oracle(5, 500))
    },
    {
        "id": "DPH-11",
        "title": "High-Frequency Algorithmic Market Maker",
        "text": "State machine dp for stock trading with cooldown day between sell and next buy.",
        "expected_pattern": "dp_state_machine",
        "input": "6\n3 2 6 5 0 3",
        "oracle_fn": lambda: str(dp_state_machine_oracle([3, 2, 6, 5, 0, 3]))
    },
    {
        "id": "DPH-12",
        "title": "Distributed Workflow Task Dependency Delay",
        "text": "Find dag longest path in computation graph using topological dynamic programming.",
        "expected_pattern": "dp_dag",
        "input": "4 4\n1 2 4\n2 3 5\n1 3 8\n3 4 2",
        "oracle_fn": lambda: str(dp_dag_longest_path_oracle(4, [(1, 2, 4), (2, 3, 5), (1, 3, 8), (3, 4, 2)]))
    },
]


def run_all_dp_blind_holdouts() -> Dict[str, Any]:
    total = len(BLIND_HOLDOUT_PROBLEMS)
    passed_recognition = 0
    passed_execution = 0
    failures = []

    print(f"\n========================================================")
    print(f"  CHUP Phase 3K — Dynamic Programming Blind Holdout")
    print(f"  Total Problems: {total} (DPH-01 through DPH-12)")
    print(f"========================================================\n")

    for prob in BLIND_HOLDOUT_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]

        res = handle_request({"action": "solve", "problemText": text})

        expected_pattern = prob["expected_pattern"]
        actual_pattern = res.get("selectedPattern")

        if actual_pattern == expected_pattern:
            passed_recognition += 1
        else:
            failures.append((pid, f"Recognition mismatch: expected {expected_pattern}, got {actual_pattern}"))
            print(f"  [FAIL] {pid} - {title}: Expected {expected_pattern}, got {actual_pattern}")
            continue

        code = res.get("code", "")
        stdin_data = prob.get("input", "")
        oracle_out = prob["oracle_fn"]().strip()

        actual_out = compile_and_run_cpp(code, stdin_data, actual_pattern).strip()

        if actual_out == oracle_out:
            passed_execution += 1
            print(f"  [PASS] {pid} - {title} (Output: {actual_out})")
        else:
            failures.append((pid, f"Execution mismatch: expected '{oracle_out}', got '{actual_out}'"))
            print(f"  [FAIL] {pid} - {title}: Expected '{oracle_out}', got '{actual_out}'")

    summary = {
        "total": total,
        "passed_recognition": passed_recognition,
        "passed_execution": passed_execution,
        "failures": failures
    }

    print("\n--------------------------------------------------------")
    print(f"  Blind Recognition: {passed_recognition}/{total} ({passed_recognition/total*100:.1f}%)")
    print(f"  Blind Execution:   {passed_execution}/{total} ({passed_execution/total*100:.1f}%)")
    print("--------------------------------------------------------\n")

    return summary


if __name__ == "__main__":
    summary = run_all_dp_blind_holdouts()
    if summary["failures"]:
        sys.exit(1)
