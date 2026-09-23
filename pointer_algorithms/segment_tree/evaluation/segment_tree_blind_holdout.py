"""
CHUP Phase 3J — Segment Tree Blind Holdout Evaluation Suite.
12 unseen, realistic competitive programming problem descriptions across Segment Tree patterns:
SH-01 through SH-12.
"""

import sys
import os
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.segment_tree.evaluation.segment_tree_benchmark import (
    compile_and_run_cpp,
    run_oracle_point_update_range_sum,
    run_oracle_point_update_range_min,
    run_oracle_point_update_range_max,
    run_oracle_point_update_range_gcd,
    run_oracle_range_add_sum,
    run_oracle_range_assign_sum,
    run_oracle_combined_lazy,
    run_oracle_metadata,
    run_oracle_max_subarray,
    run_oracle_frequency_kth,
    run_oracle_interval_statistics,
)

BLIND_HOLDOUT_PROBLEMS = [
    {
        "id": "SH-01",
        "title": "Cosmic Ray Sensor Calibration",
        "text": "Maintain cosmic particle counts across array of detector cells with point modifications at index and range sum queries using segment tree.",
        "expected_pattern": "segment_tree_point_update_range_query",
        "input": "5 3\n1 3 5 7 9\n2 1 4\n1 2 10\n2 1 4",
        "oracle_fn": lambda: run_oracle_point_update_range_sum(5, [0, 1, 3, 5, 7, 9], [(2, 1, 4), (1, 2, 10), (2, 1, 4)])
    },
    {
        "id": "SH-02",
        "title": "Submarine Trench Depth Sensor",
        "text": "Track underwater elevation with single-point depth alterations and range minimum queries via segment tree.",
        "expected_pattern": "segment_tree_point_update_range_query",
        "input": "6 3\n15 8 22 5 19 12\n2 1 6\n1 4 30\n2 1 6",
        "oracle_fn": lambda: run_oracle_point_update_range_min(6, [0, 15, 8, 22, 5, 19, 12], [(2, 1, 6), (1, 4, 30), (2, 1, 6)])
    },
    {
        "id": "SH-03",
        "title": "Power Grid Peak Voltage Monitor",
        "text": "Segment tree for range maximum queries across transmission substations with point updates.",
        "expected_pattern": "segment_tree_point_update_range_query",
        "input": "5 3\n120 240 110 230 180\n2 2 5\n1 3 300\n2 2 5",
        "oracle_fn": lambda: run_oracle_point_update_range_max(5, [0, 120, 240, 110, 230, 180], [(2, 2, 5), (1, 3, 300), (2, 2, 5)])
    },
    {
        "id": "SH-04",
        "title": "Cryptographic Mesh Key Synchronization",
        "text": "Evaluate greatest common divisor in range across shared security tokens with point updates using segment tree.",
        "expected_pattern": "segment_tree_point_update_range_query",
        "input": "5 3\n24 36 48 60 72\n2 1 5\n1 2 18\n2 1 5",
        "oracle_fn": lambda: run_oracle_point_update_range_gcd(5, [0, 24, 36, 48, 60, 72], [(2, 1, 5), (1, 2, 18), (2, 1, 5)])
    },
    {
        "id": "SH-05",
        "title": "Aqueduct Water Delivery Surge",
        "text": "Segment tree with lazy propagation for range addition and range sum queries across irrigation channels.",
        "expected_pattern": "segment_tree_range_add_range_query",
        "input": "6 3\n10 10 10 10 10 10\n1 2 5 15\n2 1 6\n2 3 4",
        "oracle_fn": lambda: run_oracle_range_add_sum(6, [0, 10, 10, 10, 10, 10, 10], [(1, 2, 5, 15), (2, 1, 6), (2, 3, 4)])
    },
    {
        "id": "SH-06",
        "title": "Warehouse Stock Re-leveling",
        "text": "Segment tree with lazy propagation for range assignment and range sum queries to overwrite bin capacities.",
        "expected_pattern": "segment_tree_range_assign_range_query",
        "input": "5 3\n5 8 12 4 9\n1 2 4 20\n2 1 5\n2 2 4",
        "oracle_fn": lambda: run_oracle_range_assign_sum(5, [0, 5, 8, 12, 4, 9], [(1, 2, 4, 20), (2, 1, 5), (2, 2, 4)])
    },
    {
        "id": "SH-07",
        "title": "Smart Highway Traffic Metering",
        "text": "Combined lazy segment tree supporting both range assignment and range add with interval sum queries.",
        "expected_pattern": "segment_tree_combined_lazy_range_query",
        "input": "5 4\n0 0 0 0 0\n2 1 5 10\n1 2 4 5\n3 1 5\n3 2 4",
        "oracle_fn": lambda: run_oracle_combined_lazy(5, [0, 0, 0, 0, 0, 0], [(2, 1, 5, 10), (1, 2, 4, 5), (3, 1, 5), (3, 2, 4)])
    },
    {
        "id": "SH-08",
        "title": "Telemetry Composite Packet Audit",
        "text": "Segment tree with composite node metadata: sum, min, and max simultaneously with point updates.",
        "expected_pattern": "segment_tree_metadata_aggregate",
        "input": "5 3\n7 2 9 4 1\n2 1 5\n1 3 0\n2 1 5",
        "oracle_fn": lambda: run_oracle_metadata(5, [0, 7, 2, 9, 4, 1], [(2, 1, 5), (1, 3, 0), (2, 1, 5)])
    },
    {
        "id": "SH-09",
        "title": "Financial Trade Sequence Optimum Profit Window",
        "text": "Segment tree for maximum contiguous subarray sum queries with dynamic point updates.",
        "expected_pattern": "segment_tree_max_subarray",
        "input": "5 3\n2 -5 3 4 -2\n2 1 5\n1 2 6\n2 1 5",
        "oracle_fn": lambda: run_oracle_max_subarray(5, [0, 2, -5, 3, 4, -2], [(2, 1, 5), (1, 2, 6), (2, 1, 5)])
    },
    {
        "id": "SH-10",
        "title": "Priority Queue Quantile Select",
        "text": "Frequency segment tree for order statistic and k-th smallest element search with insertions and deletions.",
        "expected_pattern": "segment_tree_frequency_order_statistic",
        "input": "15 5\n1 4\n1 9\n1 2\n3 2\n3 3",
        "oracle_fn": lambda: run_oracle_frequency_kth(15, [(1, 4), (1, 9), (1, 2), (3, 2), (3, 3)])
    },
    {
        "id": "SH-11",
        "title": "Seismic Sensor Extrema Frequency Tally",
        "text": "Segment tree for interval statistics: min and max with multiplicity and point updates.",
        "expected_pattern": "segment_tree_interval_statistics",
        "input": "5 3\n4 2 8 2 8\n2 1 5\n1 4 4\n2 1 5",
        "oracle_fn": lambda: run_oracle_interval_statistics(5, [0, 4, 2, 8, 2, 8], [(2, 1, 5), (1, 4, 4), (2, 1, 5)])
    },
    {
        "id": "SH-12",
        "title": "Rail Network Signal Calibration",
        "text": "Maintain array with point modification at index and range sum queries using segment tree for track sensors.",
        "expected_pattern": "segment_tree_point_update_range_query",
        "input": "4 3\n5 15 25 35\n2 1 4\n1 3 50\n2 1 4",
        "oracle_fn": lambda: run_oracle_point_update_range_sum(4, [0, 5, 15, 25, 35], [(2, 1, 4), (1, 3, 50), (2, 1, 4)])
    },
]


def run_blind_holdout() -> Dict[str, Any]:
    print("=" * 70)
    print("CHUP Phase 3J — Segment Tree Blind Holdout Evaluation (12 Problems)")
    print("=" * 70)

    total = len(BLIND_HOLDOUT_PROBLEMS)
    passed = 0
    results = []

    for prob in BLIND_HOLDOUT_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]
        exp_pat = prob["expected_pattern"]

        res = handle_request({"problemText": text})
        sel_pat = res.get("selectedPattern")

        if sel_pat != exp_pat:
            print(f"[{pid}] {title}: FAIL (Pattern mismatch: expected {exp_pat}, got {sel_pat})")
            results.append((pid, title, False, f"Pattern mismatch: {sel_pat}"))
            continue

        code = res.get("code", "")
        if not code or "COMPILE_ERROR" in code:
            print(f"[{pid}] {title}: FAIL (No code generated)")
            results.append((pid, title, False, "No code generated"))
            continue

        stdin_data = prob["input"]
        actual_out = compile_and_run_cpp(code, stdin_data, pattern=exp_pat)
        expected_out = prob["oracle_fn"]()

        if actual_out == expected_out:
            passed += 1
            print(f"[{pid}] {title}: PASS")
            results.append((pid, title, True, "Match"))
        else:
            print(f"[{pid}] {title}: FAIL (Execution mismatch)")
            print(f"  Expected:\n{expected_out[:100]}")
            print(f"  Actual:\n{actual_out[:100]}")
            results.append((pid, title, False, "Output mismatch"))

    rate = (passed / total) * 100
    print("-" * 70)
    print(f"Blind Holdout Results: {passed}/{total} passed ({rate:.1f}%)")
    print("-" * 70)

    return {
        "total": total,
        "passed": passed,
        "rate": rate,
        "results": results
    }


if __name__ == "__main__":
    res = run_blind_holdout()
    if res["passed"] < res["total"]:
        sys.exit(1)
