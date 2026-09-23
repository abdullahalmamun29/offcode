"""
CHUP Phase 3L — Greedy Algorithms Adversarial Test Suite.

Contains 15+ stress and edge cases:
- Empty inputs and single elements
- Equal endpoints and identical densities
- Ties in deadlines, weights, and frequencies
- Minimal counterexamples breaking false greedy heuristics
- Worst-case input orderings
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


ADVERSARIAL_CASES = [
    {
        "id": "ADV-GR-01",
        "title": "Interval Selection with Zero Intervals",
        "pattern": "greedy_interval_selection",
        "input": "0",
        "expected": "0"
    },
    {
        "id": "ADV-GR-02",
        "title": "Interval Selection with 10 Identical Intervals",
        "pattern": "greedy_interval_selection",
        "input": "10\n1 5\n1 5\n1 5\n1 5\n1 5\n1 5\n1 5\n1 5\n1 5\n1 5",
        "expected": "1"
    },
    {
        "id": "ADV-GR-03",
        "title": "Interval Covering with Identical Endpoints",
        "pattern": "greedy_interval_covering",
        "input": "5\n1 10\n2 10\n3 10\n4 10\n5 10",
        "expected": "1"
    },
    {
        "id": "ADV-GR-04",
        "title": "Fractional Knapsack Zero Capacity",
        "pattern": "greedy_fractional_knapsack",
        "input": "3 0\n10 5\n20 10\n30 15",
        "expected": "0.00"
    },
    {
        "id": "ADV-GR-05",
        "title": "Fractional Knapsack Huge Capacity (All Items Taken)",
        "pattern": "greedy_fractional_knapsack",
        "input": "3 1000\n10 5\n20 10\n30 15",
        "expected": "60.00"
    },
    {
        "id": "ADV-GR-06",
        "title": "Deadline Scheduling All Deadlines Exceeded",
        "pattern": "greedy_deadline_scheduling",
        "input": "3\n10 1\n20 2\n30 3",
        "expected": str(greedy_deadline_scheduling_oracle([(10, 1), (20, 2), (30, 3)]))
    },
    {
        "id": "ADV-GR-07",
        "title": "Deadline Scheduling Single Job Zero Duration",
        "pattern": "greedy_deadline_scheduling",
        "input": "1\n0 5",
        "expected": "0"
    },
    {
        "id": "ADV-GR-08",
        "title": "Heap-Assisted Refueling Impossible Initial Gap",
        "pattern": "greedy_heap_assisted",
        "input": "100 5 2\n10 50\n20 50",
        "expected": "-1"
    },
    {
        "id": "ADV-GR-09",
        "title": "Huffman Coding with 2 Frequencies",
        "pattern": "greedy_huffman_merge",
        "input": "2\n1 1",
        "expected": "2"
    },
    {
        "id": "ADV-GR-10",
        "title": "Huffman Coding with Large Identical Frequencies",
        "pattern": "greedy_huffman_merge",
        "input": "4\n100 100 100 100",
        "expected": "800"
    },
    {
        "id": "ADV-GR-11",
        "title": "Remove K Digits All Identical Digits",
        "pattern": "greedy_sequence_local_choice",
        "input": "77777 2",
        "expected": "777"
    },
    {
        "id": "ADV-GR-12",
        "title": "Remove K Digits Resulting in Pure Zeroes",
        "pattern": "greedy_sequence_local_choice",
        "input": "10000 1",
        "expected": "0"
    },
    {
        "id": "ADV-GR-13",
        "title": "Jump Game 2-Element Single Step",
        "pattern": "greedy_reachability_partition",
        "input": "2\n1 0",
        "expected": "1"
    },
    {
        "id": "ADV-GR-14",
        "title": "Graph MST Complete Graph All Equal Weights",
        "pattern": "greedy_graph_mst",
        "input": "4 6\n1 2 1\n1 3 1\n1 4 1\n2 3 1\n2 4 1\n3 4 1",
        "expected": "3"
    },
    {
        "id": "ADV-GR-15",
        "title": "Largest Number Composition All Single Digit Zeroes",
        "pattern": "greedy_general_exchange",
        "input": "5\n0 0 0 0 0",
        "expected": "0"
    }
]


def run_adversarial_suite():
    print("========================================================")
    print("  CHUP Phase 3L — Greedy Algorithms Adversarial Suite")
    print("  Total Cases: 15 (ADV-GR-01 through ADV-GR-15)")
    print("========================================================\n")

    passed = 0
    total = len(ADVERSARIAL_CASES)

    for case in ADVERSARIAL_CASES:
        case_id = case["id"]
        title = case["title"]
        pattern = case["pattern"]
        stdin_data = case["input"]
        expected_out = case["expected"]

        res = handle_request({"action": "solve", "problemText": f"Execute {pattern} algorithm."})
        code = res.get("code", "")

        actual_out = compile_and_run_cpp(code, stdin_data)

        if actual_out == expected_out:
            passed += 1
            print(f"  [PASS] {case_id} - {title} (Output: {actual_out})")
        else:
            print(f"  [FAIL] {case_id} - {title}")
            print(f"         Expected: {expected_out}")
            print(f"         Actual:   {actual_out}")

    print("\n--------------------------------------------------------")
    print(f"  Adversarial Results: {passed}/{total} passed ({passed/total*100:.1f}%)")
    print("--------------------------------------------------------\n")

    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(run_adversarial_suite())
