"""
CHUP Phase 3I — "No Fenwick" Discrimination Holdout Suite
12 problems that superficially resemble prefix/range queries, frequency counts, or updates
but must NOT select Fenwick (or must reject Fenwick with explicit anti-pattern codes).
"""

import sys
import os
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.knowledge.taxonomy import FENWICK_PATTERNS

NO_FENWICK_PROBLEMS = [
    {
        "id": "NF-01",
        "title": "Static Array Range Sums",
        "text": "Static array with no updates: compute static range sums repeatedly on immutable sequence.",
        "must_not_select_fenwick": True,
        "anti_pattern_test": True,
        "rejected_pattern": "fenwick_point_update_prefix_query",
        "expected_rejection_code": "FENWICK_STATIC_QUERY_SUBOPTIMAL"
    },
    {
        "id": "NF-02",
        "title": "Offline Batch Interval Additions",
        "text": "Batch range adds offline where all queries are only after all updates finish.",
        "must_not_select_fenwick": True,
        "anti_pattern_test": True,
        "rejected_pattern": "fenwick_point_update_prefix_query",
        "expected_rejection_code": "FENWICK_OFFLINE_RANGE_ADD_OVERKILL"
    },
    {
        "id": "NF-03",
        "title": "Non-Invertible Range GCD Queries",
        "text": "Arbitrary range query requiring subtraction and inversion for non-invertible range gcd without inverse.",
        "must_not_select_fenwick": True,
        "anti_pattern_test": True,
        "rejected_pattern": "fenwick_point_update_prefix_query",
        "expected_rejection_code": "FENWICK_STRUCTURAL_INCOMPATIBILITY"
    },
    {
        "id": "NF-04",
        "title": "Range Minimum with Arbitrary Point Replacement",
        "text": "Arbitrary range min query with arbitrary point replacement modifying values both up and down.",
        "must_not_select_fenwick": True,
        "anti_pattern_test": True,
        "rejected_pattern": "fenwick_prefix_extremum",
        "expected_rejection_code": "FENWICK_STRUCTURAL_INCOMPATIBILITY"
    },
    {
        "id": "NF-05",
        "title": "Interval Assignment Overwrite",
        "text": "Support range assignment to set entire range to constant value and overwrite interval.",
        "must_not_select_fenwick": True,
        "anti_pattern_test": True,
        "rejected_pattern": "fenwick_range_update_point_query",
        "expected_rejection_code": "FENWICK_STRUCTURAL_INCOMPATIBILITY"
    },
    {
        "id": "NF-06",
        "title": "K-th Element with Negative Frequency Decrements",
        "text": "Allow negative counts for k-th element search with negative frequency updates.",
        "must_not_select_fenwick": True,
        "anti_pattern_test": True,
        "rejected_pattern": "fenwick_kth_element",
        "expected_rejection_code": "FENWICK_KTH_NEGATIVE_FREQUENCY"
    },
    {
        "id": "NF-07",
        "title": "Dynamic Unknown Streaming Keys",
        "text": "Unknown dynamic streaming keys appearing online without prior bound or coordinate compression feasibility.",
        "must_not_select_fenwick": True,
        "anti_pattern_test": True,
        "rejected_pattern": "fenwick_point_update_prefix_query",
        "expected_rejection_code": "FENWICK_DYNAMIC_COORDINATE_UNREPRESENTABLE"
    },
    {
        "id": "NF-08",
        "title": "Incremental Graph Dynamic Connectivity",
        "text": "Maintain connected components as edges are added dynamically and query if two vertices are in the same set.",
        "expected_family": "dsu",
        "must_not_select_fenwick": True
    },
    {
        "id": "NF-09",
        "title": "Shortest Path in Weighted Graph",
        "text": "Find shortest path distance from source to destination in graph with non-negative edge weights using Dijkstra.",
        "expected_family": "graph",
        "must_not_select_fenwick": True
    },
    {
        "id": "NF-10",
        "title": "Binary Search Tree Lowest Common Ancestor",
        "text": "Find lowest common ancestor of two nodes in binary search tree with ordered branches.",
        "expected_family": "tree",
        "must_not_select_fenwick": True
    },
    {
        "id": "NF-11",
        "title": "Topological Sort of Prerequisites",
        "text": "Compute valid topological order of tasks given directed dependency edges in DAG.",
        "expected_family": "graph",
        "must_not_select_fenwick": True
    },
    {
        "id": "NF-12",
        "title": "String Prefix Autocomplete Search",
        "text": "Dictionary of words supporting autocomplete suggestions and prefix matching of strings.",
        "expected_family": "trie",
        "must_not_select_fenwick": True
    }
]


def run_no_fenwick_holdout() -> bool:
    print("=" * 70)
    print("CHUP Phase 3I — 'No Fenwick' Discrimination Holdout Suite (NF-01..NF-12)")
    print("=" * 70)

    passed = 0
    total = len(NO_FENWICK_PROBLEMS)

    for prob in NO_FENWICK_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]

        resp = handle_request({"problemText": text})
        selected_pat = resp.get("selectedPattern")
        selected_fam = resp.get("family")

        if prob.get("anti_pattern_test"):
            elim = resp.get("eliminatedCandidates", [])
            rej_pat = prob["rejected_pattern"]
            exp_code = prob["expected_rejection_code"]

            found_elim = any(
                e.get("candidate") == rej_pat and e.get("rejectionCode") == exp_code
                for e in elim
            )

            # Must also NOT have selected Fenwick as the final pattern
            not_fenwick = (selected_pat not in FENWICK_PATTERNS) and (selected_fam != "fenwick")

            if found_elim and not_fenwick:
                print(f"  [PASS] {pid} ({title}): Correctly eliminated {rej_pat} with {exp_code} (selected: {selected_pat})")
                passed += 1
            else:
                print(f"  [FAIL] {pid} ({title}): Failed elimination check. Found elim: {found_elim}, Selected: {selected_pat}. Elim: {elim}")
            continue

        # Standard discrimination test: must route to expected domain / family
        exp_fam = prob.get("expected_family")
        is_not_fenwick = (selected_pat not in FENWICK_PATTERNS) and (selected_fam != "fenwick")
        fam_matches = (selected_fam == exp_fam) if exp_fam else True

        if is_not_fenwick and fam_matches:
            print(f"  [PASS] {pid} ({title}): Correctly routed to {selected_fam} / {selected_pat} (not Fenwick)")
            passed += 1
        else:
            print(f"  [FAIL] {pid} ({title}): Incorrectly selected {selected_pat} (family: {selected_fam}, expected: {exp_fam})")

    print("=" * 70)
    print(f"'No Fenwick' Discrimination Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 70)
    return passed == total


if __name__ == "__main__":
    success = run_no_fenwick_holdout()
    sys.exit(0 if success else 1)
