"""
CHUP Phase 3I — Fenwick Tree Blind Holdout Evaluation Suite
12 unseen, realistic competitive programming problem descriptions across Fenwick patterns.
"""

import sys
import os
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.fenwick.evaluation.fenwick_benchmark import (
    compile_and_run_cpp,
    run_oracle_point_update_prefix,
    run_oracle_point_update_range,
    run_oracle_range_update_point,
    run_oracle_range_update_range,
    run_oracle_frequency,
    run_oracle_prefix_extremum,
    run_oracle_2d,
    run_oracle_kth,
    run_oracle_multiset,
    run_oracle_coord_compression,
)
from pointer_algorithms.fenwick.verification.fenwick_oracles import FenwickInversionOracle

BLIND_HOLDOUT_PROBLEMS = [
    {
        "id": "FH-01",
        "title": "Celestial Starlight Influx",
        "text": "Maintain cumulative brightness over telescopic sectors with dynamic stellar bursts adding flux at single positions and prefix total flux queries.",
        "expected_pattern": "fenwick_point_update_prefix_query",
        "input": "5 2\n1 2 3 4 5\n1 2 10\n2 1 3\n",
        "oracle_fn": lambda: run_oracle_point_update_range(5, [0, 1, 2, 3, 4, 5], [(1, 2, 10), (2, 1, 3)])
    },
    {
        "id": "FH-02",
        "title": "Submarine Hydrophone Range Acoustic Survey",
        "text": "Track acoustic sensor energy with single-point decibel increases and arbitrary range sum queries between depth levels.",
        "expected_pattern": "fenwick_point_update_prefix_query",
        "input": "6 2\n10 20 30 40 50 60\n1 3 15\n2 2 5\n",
        "oracle_fn": lambda: run_oracle_point_update_range(6, [0, 10, 20, 30, 40, 50, 60], [(1, 3, 15), (2, 2, 5)])
    },
    {
        "id": "FH-03",
        "title": "Atmospheric Radar Altitude Shield Calibration",
        "text": "Difference array Fenwick tree for radar attenuation adjustments over altitude spans [l, r] with point inquiries of local shield power.",
        "expected_pattern": "fenwick_range_update_point_query",
        "input": "5 2\n0 0 0 0 0\n1 2 4 12\n2 3\n",
        "oracle_fn": lambda: run_oracle_range_update_point(5, [0, 0, 0, 0, 0, 0], [(1, 2, 4, 12), (2, 3)])
    },
    {
        "id": "FH-04",
        "title": "District Water Grid Multi-Zone Allocation",
        "text": "Two-Fenwick tree formulation for interval additions of water pressure and range sum auditing of aggregate liters consumed across pipeline segments.",
        "expected_pattern": "fenwick_range_update_range_query",
        "input": "5 2\n1 1 1 1 1\n1 2 4 5\n2 1 5\n",
        "oracle_fn": lambda: run_oracle_range_update_range(5, [0, 1, 1, 1, 1, 1], [(1, 2, 4, 5), (2, 1, 5)])
    },
    {
        "id": "FH-05",
        "title": "MMORPG Player Level Dynamic Census",
        "text": "Dynamic frequency table tracking player counts per level: insert active player, remove inactive player, and count elements in range [low, high].",
        "expected_pattern": "fenwick_frequency",
        "input": "20 4\n1 15\n1 15\n1 7\n3 10 20\n",
        "oracle_fn": lambda: run_oracle_frequency(20, [(1, 15), (1, 15), (1, 7), (3, 10, 20)])
    },
    {
        "id": "FH-06",
        "title": "Thermal Core Minimum Temperature Monitor",
        "text": "Prefix minimum query across sensor nodes with monotonic decreasing temperature updates.",
        "expected_pattern": "fenwick_prefix_extremum",
        "input": "6 3\n1 2 100\n1 4 45\n2 5\n",
        "oracle_fn": lambda: run_oracle_prefix_extremum(6, True, [(1, 2, 100), (1, 4, 45), (2, 5)])
    },
    {
        "id": "FH-07",
        "title": "Planetary Satellite Grid Heatmap",
        "text": "2D matrix point update and subgrid range sum evaluation over orbital coordinates using 2D binary indexed tree.",
        "expected_pattern": "fenwick_2d_point_update_range_query",
        "input": "4 4 3\n1 2 2 30\n1 3 3 70\n2 1 1 4 4\n",
        "oracle_fn": lambda: run_oracle_2d(4, 4, [(1, 2, 2, 30), (1, 3, 3, 70), (2, 1, 1, 4, 4)])
    },
    {
        "id": "FH-08",
        "title": "Urgent Dispatch Priority Order Statistic",
        "text": "Locate the k-th smallest element dynamically in order-statistic waitlist using binary lifting over active frequencies in O(log M) time.",
        "expected_pattern": "fenwick_kth_element",
        "input": "16 4\n1 5\n1 11\n1 2\n3 2\n",
        "oracle_fn": lambda: run_oracle_kth(16, [(1, 5), (1, 11), (1, 2), (3, 2)])
    },
    {
        "id": "FH-09",
        "title": "Assembly Line Sequence Entropy Verification",
        "text": "Count inversions: number of pairs (i, j) with i < j and a[i] > a[j] using Fenwick tree to compute permutation disorder.",
        "expected_pattern": "fenwick_inversion_counting",
        "input": "5\n5 3 2 4 1\n",
        "oracle_fn": lambda: str(FenwickInversionOracle.count_inversions([5, 3, 2, 4, 1]))
    },
    {
        "id": "FH-10",
        "title": "Auction Bidding Multi-Item Depth Book",
        "text": "Dynamic multiset maintaining integer bids with multiplicity, point insertion, deletion, element rank, and k-th order statistic retrieval.",
        "expected_pattern": "fenwick_multiset",
        "input": "20 5\n1 12\n1 12\n1 5\n4 12\n5 1\n",
        "oracle_fn": lambda: run_oracle_multiset(20, [(1, 12), (1, 12), (1, 5), (4, 12), (5, 1)])
    },
    {
        "id": "FH-11",
        "title": "Astronomical Long-Baseline Interferometry",
        "text": "Fenwick tree with coordinate compression for vast coordinates up to 10^9 and dynamic point add and range queries.",
        "expected_pattern": "fenwick_coordinate_compression",
        "input": "3\n1 1000000000 8\n1 500000000 12\n2 1 1000000000\n",
        "oracle_fn": lambda: run_oracle_coord_compression([(1, 1000000000, 8), (1, 500000000, 12), (2, 1, 1000000000)])
    },
    {
        "id": "FH-12",
        "title": "Railway Toll Gate Linear Census Baseline",
        "text": "Linear build of Fenwick tree in O(N) time from baseline station counts and process subsequent point modifications and range sum.",
        "expected_pattern": "fenwick_point_update_prefix_query",
        "input": "4 2\n5 10 15 20\n1 2 5\n2 1 4\n",
        "oracle_fn": lambda: run_oracle_point_update_range(4, [0, 5, 10, 15, 20], [(1, 2, 5), (2, 1, 4)])
    }
]


def run_blind_holdout() -> bool:
    print("=" * 70)
    print("CHUP Phase 3I — Fenwick Tree Blind Holdout Suite (FH-01 through FH-12)")
    print("=" * 70)

    passed = 0
    total = len(BLIND_HOLDOUT_PROBLEMS)

    for prob in BLIND_HOLDOUT_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]
        expected_pat = prob["expected_pattern"]

        resp = handle_request({"problemText": text})
        actual_pat = resp.get("selectedPattern")
        code = resp.get("code") or resp.get("generatedCode")

        if actual_pat != expected_pat:
            print(f"  [FAIL] {pid} ({title}): Expected {expected_pat}, got {actual_pat}")
            continue

        if not code or len(code) < 50:
            print(f"  [FAIL] {pid} ({title}): No C++ code generated")
            continue

        stdin_data = prob.get("input", "")
        actual_out = compile_and_run_cpp(code, stdin_data, actual_pat)

        oracle_fn = prob.get("oracle_fn")
        if oracle_fn:
            expected_out = oracle_fn()
            if isinstance(expected_out, list):
                expected_str = "\n".join(expected_out).strip()
            else:
                expected_str = str(expected_out).strip()

            if actual_out != expected_str:
                print(f"  [FAIL] {pid} ({title}): Output mismatch. Expected:\n{expected_str}\nGot:\n{actual_out}")
                continue

        print(f"  [PASS] {pid} ({title}): {actual_pat} verified against oracle (output: {actual_out})")
        passed += 1

    print("=" * 70)
    print(f"Blind Holdout Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 70)
    return passed == total


if __name__ == "__main__":
    success = run_blind_holdout()
    sys.exit(0 if success else 1)
