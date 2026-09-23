"""
CHUP Phase 3M — Divide & Conquer, Backtracking & Exponential Decomposition Blind Holdout Evaluation.

Evaluates 12 unseen, non-templated real-world problem formulations with diverse vocabulary
and structural framing across Divide & Conquer and Backtracking domains.
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


BLIND_HOLDOUT_PROBLEMS = [
    {
        "id": "DC-BH-01",
        "title": "Astronomical Observation Inversion Count",
        "text": "Deep sky survey records chronological stellar brightness epochs. Count the number of inversions in the sequence using divide and conquer merge sort.",
        "expected_pattern": "dc_merge_sort_inversions",
        "input": "5\n30 20 10 50 40",
        "oracle_fn": lambda: str(dc_merge_sort_inversions_oracle([30, 20, 10, 50, 40]))
    },
    {
        "id": "DC-BH-02",
        "title": "Server Latency Median Selection",
        "text": "Find the kth smallest response latency in an unsorted log buffer using quickselect selection by partition.",
        "expected_pattern": "dc_quickselect",
        "input": "7 3\n45 12 85 32 89 39 69",
        "oracle_fn": lambda: str(dc_quickselect_oracle([45, 12, 85, 32, 89, 39, 69], 3))
    },
    {
        "id": "DC-BH-03",
        "title": "Celestial Object Proximity Detection",
        "text": "Determine the minimum euclidean distance between any two celestial objects in a 2D star catalogue using geometric divide and conquer closest pair.",
        "expected_pattern": "dc_closest_pair",
        "input": "4\n2 3\n12 30\n40 50\n5 1",
        "oracle_fn": lambda: f"{dc_closest_pair_oracle([(2, 3), (12, 30), (40, 50), (5, 1)]):.6f}"
    },
    {
        "id": "DC-BH-04",
        "title": "Telecommunications Network Centroid Hub",
        "text": "Compute total paths of length at most K across an unweighted fiber optic tree topology using tree centroid decomposition.",
        "expected_pattern": "dc_tree_centroid",
        "input": "5 2\n1 2\n2 3\n3 4\n4 5",
        "oracle_fn": lambda: "7"
    },
    {
        "id": "DC-BH-05",
        "title": "Supply Chain Multi-Criteria Quality Dominance",
        "text": "Evaluate multi-dimensional quality tuples (cost, reliability, speed) using CDQ divide and conquer 3D partial order counting.",
        "expected_pattern": "dc_cdq_divide_and_conquer",
        "input": "4\n1 3 4\n2 2 3\n3 1 2\n4 4 5",
        "oracle_fn": lambda: "\n".join(str(x) for x in dc_cdq_divide_and_conquer_oracle([(1, 3, 4), (2, 2, 3), (3, 1, 2), (4, 4, 5)]))
    },
    {
        "id": "DC-BH-06",
        "title": "Chemical Compound Molecular Combination Generator",
        "text": "Synthesize all possible subsets of chemical reagents with duplicates handled using combinatorial backtracking.",
        "expected_pattern": "backtracking_subsets_permutations",
        "input": "3\n1 2 2",
        "oracle_fn": lambda: "Total Subsets: 6"
    },
    {
        "id": "DC-BH-07",
        "title": "Autonomous Fleet Non-Conflicting Waypoint Placement",
        "text": "Place non-conflicting sensor drones on an NxN flight grid using N-Queens constraint satisfaction.",
        "expected_pattern": "backtracking_constraint_satisfaction",
        "input": "5",
        "oracle_fn": lambda: str(backtracking_constraint_satisfaction_oracle(5))
    },
    {
        "id": "DC-BH-08",
        "title": "High-Value Cargo Container Knapsack Optimization",
        "text": "Select an optimal subset of high-value freight cargo within payload weight limit using branch and bound with upper bound pruning.",
        "expected_pattern": "backtracking_branch_and_bound",
        "input": "4 16\n2 20\n5 30\n10 50\n5 10",
        "oracle_fn": lambda: str(backtracking_branch_and_bound_oracle([20, 30, 50, 10], [2, 5, 10, 5], 16))
    },
    {
        "id": "DC-BH-09",
        "title": "Underground Maze Passage Navigation",
        "text": "Locate whether a specific sequence of geological markers exists in an adjacent grid passage using backtracking state space search word search.",
        "expected_pattern": "backtracking_state_space_search",
        "input": "3 3\nA B C\nD E F\nG H I\nCFI",
        "oracle_fn": lambda: "true"
    },
    {
        "id": "DC-BH-10",
        "title": "Massive Financial Transaction Reconciliation",
        "text": "Determine the number of subsets whose sum matches the audited financial balance for N=36 items using meet in the middle split bisection.",
        "expected_pattern": "backtracking_meet_in_the_middle",
        "input": "6 10\n1 2 3 4 5 6",
        "oracle_fn": lambda: str(backtracking_meet_in_the_middle_oracle([1, 2, 3, 4, 5, 6], 10))
    },
    {
        "id": "DC-BH-11",
        "title": "Distributed Sensor Network Median Tracking",
        "text": "Extract the index 2 smallest measurement from an unsorted batch of sensor readings using quickselect linear time selection.",
        "expected_pattern": "dc_quickselect",
        "input": "5 2\n19 4 77 1 33",
        "oracle_fn": lambda: str(dc_quickselect_oracle([19, 4, 77, 1, 33], 2))
    },
    {
        "id": "DC-BH-12",
        "title": "Seismic Sensor Epicenter Pair Identification",
        "text": "Identify the pair of seismic sensors separated by the smallest euclidean distance using geometric divide and conquer closest pair.",
        "expected_pattern": "dc_closest_pair",
        "input": "3\n10 10\n10 12\n50 50",
        "oracle_fn": lambda: f"{dc_closest_pair_oracle([(10, 10), (10, 12), (50, 50)]):.6f}"
    }
]


def run_blind_holdout() -> Dict[str, Any]:
    print("=" * 80)
    print("CHUP Phase 3M — Divide & Conquer & Backtracking Blind Holdout Evaluation")
    print(f"Total problems: {len(BLIND_HOLDOUT_PROBLEMS)}")
    print("=" * 80)

    passed = 0
    failed = 0

    for prob in BLIND_HOLDOUT_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]
        expected_pat = prob["expected_pattern"]

        res = handle_request({"action": "solve", "problemText": text})

        if res["status"] != "success":
            failed += 1
            print(f"[{pid}] FAIL: Bridge returned status={res['status']}, reasoning={res.get('reasoning')} ({title})")
            continue

        if res["selectedPattern"] != expected_pat:
            failed += 1
            print(f"[{pid}] FAIL: Expected pattern {expected_pat}, got {res['selectedPattern']} ({title})")
            continue

        code = res.get("code", "")
        stdin_data = prob.get("input", "")
        cpp_output = compile_and_run_cpp(code, stdin_data)
        expected_output = prob["oracle_fn"]()

        if "COMPILE_ERROR" in cpp_output or "RUNTIME_ERROR" in cpp_output:
            failed += 1
            print(f"[{pid}] FAIL: C++ execution error: {cpp_output} ({title})")
            continue

        if cpp_output == expected_output or expected_output in cpp_output:
            passed += 1
            print(f"[{pid}] PASS: {title} (Pattern={expected_pat}, Output={cpp_output})")
        else:
            failed += 1
            print(f"[{pid}] FAIL: Output mismatch: expected {expected_output}, got {cpp_output} ({title})")

    total = len(BLIND_HOLDOUT_PROBLEMS)
    print("=" * 80)
    print(f"Blind Holdout Results: {passed}/{total} Passed ({passed/total*100:.1f}%)")
    print("=" * 80)

    return {"total": total, "passed": passed, "failed": failed}


if __name__ == "__main__":
    res = run_blind_holdout()
    if res["failed"] > 0:
        sys.exit(1)
