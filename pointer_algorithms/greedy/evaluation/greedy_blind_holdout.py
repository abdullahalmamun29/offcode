"""
CHUP Phase 3L — Greedy Algorithms Blind Holdout Evaluation.

Evaluates Greedy algorithms on 12 unseen, non-templated real-world problem formulations
with diverse vocabulary and structural framing.
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


BLIND_HOLDOUT_PROBLEMS = [
    {
        "id": "GBH-01",
        "title": "Air Traffic Runway Landing Slot Allocation",
        "text": "A congested international airport must schedule incoming aircraft on a single runway. Each flight requests an arrival window [start, finish]. Apply earliest finish time greedy activity selection to accept the maximum number of compatible non-overlapping flights.",
        "expected_pattern": "greedy_interval_selection",
        "input": "5\n9 11\n10 13\n11 12\n12 15\n14 16",
        "oracle_fn": lambda: str(greedy_interval_selection_oracle([(9, 11), (10, 13), (11, 12), (12, 15), (14, 16)]))
    },
    {
        "id": "GBH-02",
        "title": "Astronomical Telescope Sensor Stabbing",
        "text": "Deep-sky telescope captures transient astronomical events across interval timeframes. Determine minimum points to cover and observe all event intervals with sensor bursts.",
        "expected_pattern": "greedy_interval_covering",
        "input": "4\n1 4\n2 5\n6 9\n7 10",
        "oracle_fn": lambda: str(greedy_interval_covering_oracle([(1, 4), (2, 5), (6, 9), (7, 10)]))
    },
    {
        "id": "GBH-03",
        "title": "Spacecraft Divisible Mineral Cargo Extraction",
        "text": "An asteroid mining rover collects divisible mineral ores with given total values and weights. Fill the return capsule using fractional knapsack value-density greedy allocation.",
        "expected_pattern": "greedy_fractional_knapsack",
        "input": "3 40\n120 30\n100 20\n60 10",
        "oracle_fn": lambda: f"{greedy_fractional_knapsack_oracle([(120, 30), (100, 20), (60, 10)], 40):.2f}"
    },
    {
        "id": "GBH-04",
        "title": "Factory Production Line Lateness Minimization",
        "text": "Industrial robotic workstation must order client orders to minimize maximum lateness scheduling jobs with deadlines using earliest due date rule.",
        "expected_pattern": "greedy_deadline_scheduling",
        "input": "3\n3 5\n2 4\n1 2",
        "oracle_fn": lambda: str(greedy_deadline_scheduling_oracle([(3, 5), (2, 4), (1, 2)]))
    },
    {
        "id": "GBH-05",
        "title": "Desert Expedition Water Canteen Refueling",
        "text": "An exploration vehicle traverses an arid desert toward an oasis. When water runs out, choose passed oases via heap-assisted greedy to find minimum refueling stops.",
        "expected_pattern": "greedy_heap_assisted",
        "input": "100 25 3\n20 30\n40 20\n70 30",
        "oracle_fn": lambda: str(greedy_heap_assisted_oracle(100, 25, [(20, 30), (40, 20), (70, 30)]))
    },
    {
        "id": "GBH-06",
        "title": "Satellite Telemetry Stream Huffman Compression",
        "text": "A deep-space probe compresses transmission packets by constructing an optimal merge pattern / Huffman coding tree, repeatedly combining the two minimum component costs.",
        "expected_pattern": "greedy_huffman_merge",
        "input": "5\n8 5 3 2 1",
        "oracle_fn": lambda: str(greedy_huffman_merge_oracle([8, 5, 3, 2, 1]))
    },
    {
        "id": "GBH-07",
        "title": "Cryptographic Nonce Digits Reduction",
        "text": "A security module must remove k digits to minimize number representation using monotonic stack greedy local choices.",
        "expected_pattern": "greedy_sequence_local_choice",
        "input": "54321 2",
        "oracle_fn": lambda: greedy_sequence_local_choice_oracle("54321", 2)
    },
    {
        "id": "GBH-08",
        "title": "Autonomous Drone Hop Minimization",
        "text": "A drone navigates recharging pylons along a straight line. Compute minimum jumps to reach the destination via reachability frontier greedy.",
        "expected_pattern": "greedy_reachability_partition",
        "input": "5\n1 3 1 1 1",
        "oracle_fn": lambda: str(greedy_reachability_partition_oracle([1, 3, 1, 1, 1]))
    },
    {
        "id": "GBH-09",
        "title": "Subsea Optical Cable Minimum Spanning Network",
        "text": "Intercontinental telecom grid links island nodes with minimum total fiber cost using Kruskal algorithm with cut property and DSU for minimum spanning tree.",
        "expected_pattern": "greedy_graph_mst",
        "input": "4 4\n1 2 10\n2 3 15\n3 4 20\n4 1 25",
        "oracle_fn": lambda: str(greedy_graph_mst_oracle(4, [(1, 2, 10), (2, 3, 15), (3, 4, 20), (4, 1, 25)]))
    },
    {
        "id": "GBH-10",
        "title": "Transaction Identifier Lexicographical Composition",
        "text": "Compose the largest number from array of integers / transaction tokens using pairwise exchange comparator greedy.",
        "expected_pattern": "greedy_general_exchange",
        "input": "4\n4 40 45 42",
        "oracle_fn": lambda: greedy_general_exchange_oracle(["4", "40", "45", "42"])
    },
    {
        "id": "GBH-11",
        "title": "Biochemical Incubation Chamber Scheduling",
        "text": "Laboratory incubator allocates thermal slots for reaction assays. Find maximum number of compatible non-overlapping intervals via earliest finish greedy activity selection.",
        "expected_pattern": "greedy_interval_selection",
        "input": "3\n1 3\n2 4\n3 5",
        "oracle_fn": lambda: str(greedy_interval_selection_oracle([(1, 3), (2, 4), (3, 5)]))
    },
    {
        "id": "GBH-12",
        "title": "Autonomous Rail Corridor Sensor Deployment",
        "text": "Deploy optical wayside sensors along railway maintenance zones. Find minimum points to cover all intervals using interval stabbing greedy.",
        "expected_pattern": "greedy_interval_covering",
        "input": "3\n10 20\n15 25\n30 40",
        "oracle_fn": lambda: str(greedy_interval_covering_oracle([(10, 20), (15, 25), (30, 40)]))
    }
]


def run_blind_holdout():
    print("========================================================")
    print("  CHUP Phase 3L — Greedy Algorithms Blind Holdout")
    print("  Total Problems: 12 (GBH-01 through GBH-12)")
    print("========================================================\n")

    passed_recognition = 0
    passed_execution = 0
    total = len(BLIND_HOLDOUT_PROBLEMS)

    for prob in BLIND_HOLDOUT_PROBLEMS:
        prob_id = prob["id"]
        title = prob["title"]
        text = prob["text"]
        expected_pat = prob["expected_pattern"]

        res = handle_request({"action": "solve", "problemText": text})
        selected_pat = res.get("selectedPattern")

        if selected_pat == expected_pat:
            passed_recognition += 1
            code = res.get("code", "")
            stdin_data = prob["input"]
            actual_out = compile_and_run_cpp(code, stdin_data)
            expected_out = prob["oracle_fn"]()

            if actual_out == expected_out:
                passed_execution += 1
                print(f"  [PASS] {prob_id} - {title} (Output: {actual_out})")
            else:
                print(f"  [FAIL-EXEC] {prob_id} - {title}")
                print(f"         Expected: {expected_out}")
                print(f"         Actual:   {actual_out}")
        else:
            print(f"  [FAIL-REC] {prob_id} - {title}")
            print(f"         Expected: {expected_pat}")
            print(f"         Actual:   {selected_pat}")

    print("\n--------------------------------------------------------")
    print(f"  Blind Recognition: {passed_recognition}/{total} ({passed_recognition/total*100:.1f}%)")
    print(f"  Blind Execution:   {passed_execution}/{total} ({passed_execution/total*100:.1f}%)")
    print("--------------------------------------------------------\n")

    return 0 if (passed_recognition == total and passed_execution == total) else 1

if __name__ == "__main__":
    sys.exit(run_blind_holdout())
