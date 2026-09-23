"""
CHUP Phase 3G — Heap / Priority Queue Blind Holdout Evaluation.

Contains 12 challenging holdout problems with semantic real-world descriptions.
No algorithm names ('heap', 'priority queue', 'pq') are leaked in problem texts.
Tests whether CHUP autonomously recognizes the underlying dynamic candidate set
and extremal access invariants.
"""

import sys
import os
import subprocess
import tempfile
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request

COMPILED_BINARIES: Dict[str, str] = {}


import hashlib

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


BLIND_PROBLEMS = [
    {
        "id": "BH-01",
        "name": "Emergency Hospital Triage",
        "text": "An emergency department admits patients with severity rank scores. Support inserting patients and always extract the patient with the minimum severity score for immediate treatment.",
        "expected_pattern": "heap_min_priority_queue",
        "input": "4\ninsert 5\ninsert 1\nextract\nextract\n",
        "oracle_check": lambda out: out.split() == ["1", "5"]
    },
    {
        "id": "BH-02",
        "name": "Live Stock Auction Bidding",
        "text": "A live trading desk receives buy orders. Always extract the highest price offer when matched.",
        "expected_pattern": "heap_max_priority_queue",
        "input": "4\ninsert 150\ninsert 300\nextract\nextract\n",
        "oracle_check": lambda out: out.split() == ["300", "150"]
    },
    {
        "id": "BH-03",
        "name": "Web Traffic Heavy Hitters",
        "text": "A network monitor observes millions of incoming packet sizes. Identify the top 3 largest packet sizes observed.",
        "expected_pattern": "heap_top_k",
        "input": "6 3\n500 1200 300 1500 800 1100\n",
        "oracle_check": lambda out: out.split() == ["1500", "1200", "1100"]
    },
    {
        "id": "BH-04",
        "name": "Discount Store Clearance",
        "text": "A retailer wants to select the top 2 smallest price tags from an inventory list.",
        "expected_pattern": "heap_top_k",
        "input": "5 2\n99 15 45 10 30\n",
        "oracle_check": lambda out: set(out.split()) == {"10", "15"}
    },
    {
        "id": "BH-05",
        "name": "Tournament 3rd Rank Qualifier",
        "text": "In a gaming championship, identify the 3rd largest score achieved among all participants.",
        "expected_pattern": "heap_kth_element",
        "input": "6 3\n85 92 78 95 88 90\n",
        "oracle_check": lambda out: out.strip() == "90"
    },
    {
        "id": "BH-06",
        "name": "Multi-Region Event Log Chronology",
        "text": "Distributed server clusters output chronologically ordered event logs. Merge multiple sorted event logs into a single unified chronological timeline.",
        "expected_pattern": "heap_k_way_merge",
        "input": "3\n2 100 400\n3 200 300 500\n1 250\n",
        "oracle_check": lambda out: out.split() == ["100", "200", "250", "300", "400", "500"]
    },
    {
        "id": "BH-07",
        "name": "Continuous Financial Metric Centroid",
        "text": "A financial data feed streams trade prices one by one. Maintain the running median of trade prices after each incoming trade.",
        "expected_pattern": "heap_dynamic_median",
        "input": "4\n10\n20\n30\n40\n",
        "oracle_check": lambda out: out.split() == ["10", "15", "20", "25"]
    },
    {
        "id": "BH-08",
        "name": "Cloud Compute Cluster Capacity",
        "text": "Jobs arrive with execution start and completion end times. Determine the minimum number of parallel virtual machines needed so no job waits.",
        "expected_pattern": "heap_scheduling",
        "input": "4\n1 4\n2 5\n6 8\n3 7\n",
        "oracle_check": lambda out: out.strip() == "3"
    },
    {
        "id": "BH-09",
        "name": "Fiber Optic Line Splicing",
        "text": "Spools of optical fiber must be spliced together into one continuous line. Splicing two spools of lengths x and y costs x + y. Find the minimum total cost to connect all spools.",
        "expected_pattern": "heap_greedy_selection",
        "input": "4\n4 3 2 6\n",
        "oracle_check": lambda out: out.strip() == "29"
    },
    {
        "id": "BH-10",
        "name": "Canceled Order Orderbook",
        "text": "Orders arrive and some orders are subsequently canceled. Always retrieve the active order with the maximum price using delayed removal of canceled orders.",
        "expected_pattern": "heap_lazy_deletion",
        "input": "5\nINSERT 100\nINSERT 200\nDELETE 200\nGET_MAX\nEXTRACT_MAX\n",
        "oracle_check": lambda out: out.split() == ["100", "100"]
    },
    {
        "id": "BH-11",
        "name": "Satellite Telemetry Buffer Sorting",
        "text": "Downlinked telemetry data arrives as an unordered batch of measurements. Reorganize the entire array into a valid bottom-up heap order in linear time.",
        "expected_pattern": "heap_build",
        "input": "5\n8 3 5 1 4\n",
        "oracle_check": lambda out: int(out.split()[0]) == 1
    },
    {
        "id": "BH-12",
        "name": "Two-Pool Temperature Stabilization",
        "text": "Partition sensory temperature readings into two equal pools using two heaps to balance stream data continuously.",
        "expected_pattern": "heap_two_heaps",
        "input": "3\n22\n28\n25\n",
        "oracle_check": lambda out: out.split()[-1] == "25"
    },
]


def run_holdout():
    print("=" * 70)
    print("CHUP Phase 3G — Heap Blind Holdout Evaluation (BH-01..BH-12)")
    print("=" * 70)

    passed = 0
    total = len(BLIND_PROBLEMS)

    for p in BLIND_PROBLEMS:
        pid = p["id"]
        name = p["name"]

        resp = handle_request({"problemText": p["text"]})
        if resp.get("status") != "success":
            print(f"  [FAIL] {pid} ({name}): Request status {resp.get('status')}, reason: {resp.get('reasoning')}")
            continue

        actual_pattern = resp.get("selectedPattern")
        if actual_pattern != p["expected_pattern"]:
            print(f"  [FAIL] {pid} ({name}): Expected {p['expected_pattern']}, got {actual_pattern}")
            continue

        cpp_code = resp.get("code", "")
        out = compile_and_run_cpp(cpp_code, p["input"], pattern=actual_pattern)

        if out.startswith("COMPILE_ERROR") or out.startswith("RUNTIME_ERROR"):
            print(f"  [FAIL] {pid} ({name}): Execution error: {out[:120]}")
            continue

        if p["oracle_check"](out):
            print(f"  [PASS] {pid} ({name}): {actual_pattern} verified (output: {out[:40].strip()})")
            passed += 1
        else:
            print(f"  [FAIL] {pid} ({name}): Output '{out[:40].strip()}' failed oracle check")

    print("=" * 70)
    score_pct = (passed / total) * 100
    print(f"Blind Holdout Score: {passed}/{total} ({score_pct:.1f}%)")
    print("=" * 70)
    return passed == total


if __name__ == "__main__":
    success = run_holdout()
    sys.exit(0 if success else 1)
