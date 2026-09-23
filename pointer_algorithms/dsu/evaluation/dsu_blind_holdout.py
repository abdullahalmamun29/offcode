"""
CHUP Phase 3H — Advanced DSU Blind Holdout Evaluation Suite
12 unseen, realistic competitive programming problem descriptions across DSU patterns.
"""

import sys
import os
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.dsu.evaluation.dsu_benchmark import compile_and_run_cpp
from pointer_algorithms.dsu.verification.dsu_oracles import (
    oracle_basic_dsu, oracle_component_metadata, oracle_dynamic_connectivity,
    oracle_weighted_dsu, oracle_potential_difference, oracle_parity_dsu,
    oracle_rollback_dsu, oracle_offline_dynamic_connectivity,
    oracle_kruskal_support, oracle_constraint_consistency
)

BLIND_HOLDOUT_PROBLEMS = [
    {
        "id": "BH-01",
        "title": "Social Circles Equivalence Partitioning",
        "text": "Maintain equivalence classes of users as friendship links are forged, supporting make_set, find, and union on elements.",
        "expected_pattern": "dsu_basic",
        "input": "4 4\n1 1 2\n1 2 3\n2 1 3\n3 1 0\n",
        "oracle_fn": lambda: oracle_basic_dsu(4, [(1, 1, 2), (1, 2, 3), (2, 1, 3), (3, 1, 0)])
    },
    {
        "id": "BH-02",
        "title": "Data Center Live Route Testing",
        "text": "Maintain incremental dynamic connectivity between server nodes as communication cables are installed online.",
        "expected_pattern": "dsu_dynamic_connectivity",
        "input": "4 4\n1 1 2\n1 3 4\n2 1 2\n2 1 4\n",
        "oracle_fn": lambda: oracle_dynamic_connectivity(4, [(1, 1, 2), (1, 3, 4), (2, 1, 2), (2, 1, 4)])
    },
    {
        "id": "BH-03",
        "title": "Clan Power & Champion Tracking",
        "text": "Component metadata DSU tracking component sum and maximum element across merged allied clans.",
        "expected_pattern": "dsu_component_metadata",
        "input": "4 3\n10 20 5 40\n1 1 2\n1 3 4\n2 1\n",
        "oracle_fn": lambda: oracle_component_metadata(4, [0, 10, 20, 5, 40], [(1, 1, 2), (1, 3, 4), (2, 1)])
    },
    {
        "id": "BH-04",
        "title": "Ore Vein Aggregation",
        "text": "Maintain component metadata tracking component size and minimum value across set mergers.",
        "expected_pattern": "dsu_component_metadata",
        "input": "5 3\n1 2 3 4 5\n1 1 2\n1 2 3\n2 1\n",
        "oracle_fn": lambda: oracle_component_metadata(5, [0, 1, 2, 3, 4, 5], [(1, 1, 2), (1, 2, 3), (2, 1)])
    },
    {
        "id": "BH-05",
        "title": "Planetary Altitude Alignment",
        "text": "Maintain relative potentials with weighted DSU path compression and difference queries for elevation offsets.",
        "expected_pattern": "dsu_weighted",
        "input": "4 3\n1 1 3 12\n1 2 4 4\n2 1 3\n",
        "oracle_fn": lambda: oracle_weighted_dsu(4, [(1, 1, 3, 12), (1, 2, 4, 4), (2, 1, 3)])
    },
    {
        "id": "BH-06",
        "title": "Relative Financial Valuation",
        "text": "Query potential difference value[x] - value[y] between elements using weighted DSU else UNKNOWN.",
        "expected_pattern": "dsu_potential_difference",
        "input": "4 4\n1 1 2 8\n1 2 3 2\n2 1 3\n2 1 4\n",
        "oracle_fn": lambda: oracle_potential_difference(4, [(1, 1, 2, 8), (1, 2, 3, 2), (2, 1, 3), (2, 1, 4)])
    },
    {
        "id": "BH-07",
        "title": "Diplomatic Alliance vs Hostility",
        "text": "Maintain parity constraints color[x] xor color[y] with dynamic 2-coloring DSU for allies and foes.",
        "expected_pattern": "dsu_parity",
        "input": "4 4\n1 1 2 1\n1 2 3 1\n2 1 3\n2 1 4\n",
        "oracle_fn": lambda: oracle_parity_dsu(4, [(1, 1, 2, 1), (1, 2, 3, 1), (2, 1, 3), (2, 1, 4)])
    },
    {
        "id": "BH-08",
        "title": "Odd Cycle Detection in Conflict Graph",
        "text": "Detect odd-cycle contradiction in dynamic bipartite coloring using parity DSU.",
        "expected_pattern": "dsu_parity",
        "input": "3 3\n1 1 2 1\n1 2 3 1\n1 3 1 1\n",
        "oracle_fn": lambda: oracle_parity_dsu(3, [(1, 1, 2, 1), (1, 2, 3, 1), (1, 3, 1, 1)])
    },
    {
        "id": "BH-09",
        "title": "Chess Puzzle Exploration Backtracking",
        "text": "Rollback DSU with union-by-size and undo operation to revert previous merges during branch exploration.",
        "expected_pattern": "dsu_rollback",
        "input": "4 6\n1 1 2\n3\n1 2 3\n2 1 3\n4\n2 1 3\n",
        "oracle_fn": lambda: oracle_rollback_dsu(4, [(1, 1, 2), (3,), (1, 2, 3), (2, 1, 3), (4,), (2, 1, 3)])
    },
    {
        "id": "BH-10",
        "title": "Transaction Checkpoint Reversion",
        "text": "Checkpoint snapshot and rollback DSU without path compression to undo operations.",
        "expected_pattern": "dsu_rollback",
        "input": "5 4\n3\n1 1 5\n4\n2 1 5\n",
        "oracle_fn": lambda: oracle_rollback_dsu(5, [(3,), (1, 1, 5), (4,), (2, 1, 5)])
    },
    {
        "id": "BH-11",
        "title": "Temporal Bridge Network Connectivity",
        "text": "Offline dynamic connectivity using segment tree over time with rollback DSU where all queries known in advance.",
        "expected_pattern": "dsu_offline_dynamic_connectivity",
        "input": "4 5\n1 1 2\n3 1 2\n2 1 2\n3 1 2\n3 3 4\n",
        "oracle_fn": lambda: oracle_offline_dynamic_connectivity(4, [(1, 1, 2), (3, 1, 2), (2, 1, 2), (3, 1, 2), (3, 3, 4)])
    },
    {
        "id": "BH-12",
        "title": "Power Line Cycle Prevention",
        "text": "DSU Kruskal support for cycle prevention by checking if edge endpoints share the same root.",
        "expected_pattern": "dsu_kruskal_support",
        "input": "4 5\n1 2 1\n2 3 2\n3 4 3\n4 1 4\n1 3 5\n",
        "oracle_fn": lambda: str(oracle_kruskal_support(4, [(1, 2, 1), (2, 3, 2), (3, 4, 3), (4, 1, 4), (1, 3, 5)]))
    }
]


def run_blind_holdout() -> bool:
    print("=" * 70)
    print("CHUP Phase 3H — Advanced DSU Blind Holdout (BH-01 through BH-12)")
    print("=" * 70)

    passed = 0
    total = len(BLIND_HOLDOUT_PROBLEMS)

    for prob in BLIND_HOLDOUT_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]
        expected_pat = prob["expected_pattern"]
        stdin_input = prob["input"]
        oracle_fn = prob["oracle_fn"]

        resp = handle_request({"problemText": text})
        actual_pat = resp.get("selectedPattern")

        if actual_pat != expected_pat:
            print(f"  [FAIL] {pid} ({title}): Expected {expected_pat}, got {actual_pat}")
            continue

        cpp_code = resp.get("code") or resp.get("generatedCode")
        if not cpp_code:
            print(f"  [FAIL] {pid} ({title}): No C++ code generated")
            continue

        expected_raw = oracle_fn()
        if isinstance(expected_raw, list):
            oracle_out = "\n".join(expected_raw).strip()
        else:
            oracle_out = str(expected_raw).strip()
        cpp_out = compile_and_run_cpp(cpp_code, stdin_input, pattern=expected_pat).strip()

        if cpp_out != oracle_out:
            print(f"  [FAIL] {pid} ({title}): Output mismatch! Oracle: '{oracle_out}' vs C++: '{cpp_out}'")
            continue

        print(f"  [PASS] {pid} ({title}): {actual_pat} verified against oracle (output: {cpp_out})")
        passed += 1

    print("=" * 70)
    print(f"DSU Blind Holdout Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 70)
    return passed == total


if __name__ == "__main__":
    success = run_blind_holdout()
    sys.exit(0 if success else 1)
