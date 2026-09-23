"""
CHUP Phase 3K — Dynamic Programming Discrimination Holdout Suite.
12 problems that superficially resemble DP, subproblems, or optimization
but must NOT select Dynamic Programming (or must reject DP with explicit rejection codes):
NDP-01 through NDP-12.
"""

import sys
import os
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.knowledge.taxonomy import DP_PATTERNS

DISCRIMINATION_PROBLEMS = [
    {
        "id": "NDP-01",
        "title": "Continuous Fractional Knapsack",
        "text": "Fractional knapsack allows continuous fractions of items to maximize value by density.",
        "anti_pattern_test": True,
        "must_not_select_dp": True,
        "rejected_pattern": "dp_knapsack_01",
        "expected_rejection_code": "DP_GREEDY_CHOICE_OPTIMAL"
    },
    {
        "id": "NDP-02",
        "title": "Shortest Path in Graph with Cycles",
        "text": "Find shortest path in general directed graph with negative cycles.",
        "anti_pattern_test": True,
        "must_not_select_dp": True,
        "rejected_pattern": "dp_dag_longest_path",
        "expected_rejection_code": "DP_CYCLIC_STATE_DEPENDENCY"
    },
    {
        "id": "NDP-03",
        "title": "Longest Simple Path in General Graph",
        "text": "Find longest simple path in general undirected graph without optimal substructure.",
        "anti_pattern_test": True,
        "must_not_select_dp": True,
        "rejected_pattern": "dp_1d_linear",
        "expected_rejection_code": "DP_NO_OPTIMAL_SUBSTRUCTURE"
    },
    {
        "id": "NDP-04",
        "title": "Merge Sort Divide and Conquer",
        "text": "Merge sort divides into completely disjoint halves without overlapping subproblems.",
        "anti_pattern_test": True,
        "must_not_select_dp": True,
        "rejected_pattern": "dp_1d_linear",
        "expected_rejection_code": "DP_NO_OVERLAPPING_SUBPROBLEMS"
    },
    {
        "id": "NDP-05",
        "title": "Non-Markovian History Dependent Routing",
        "text": "Path selection requires full historical visitation sequence violating Markov property.",
        "anti_pattern_test": True,
        "must_not_select_dp": True,
        "rejected_pattern": "dp_1d_linear",
        "expected_rejection_code": "DP_NON_MARKOVIAN_FUTURE_DEPENDENCE"
    },
    {
        "id": "NDP-06",
        "title": "State Space Explosion in Multi-Dimensional Knapsack",
        "text": "Subset selection over 100 dimensions causes state explosion beyond memory budget.",
        "anti_pattern_test": True,
        "must_not_select_dp": True,
        "rejected_pattern": "dp_knapsack_01",
        "expected_rejection_code": "DP_STATE_SPACE_EXPLOSION"
    },
    {
        "id": "NDP-07",
        "title": "Minimum Spanning Tree",
        "text": "Find minimum spanning tree in connected weighted undirected graph using Kruskal or Prim.",
        "expected_family": "graph",
        "must_not_select_dp": True
    },
    {
        "id": "NDP-08",
        "title": "Range Sum with Dynamic Point Updates",
        "text": "Maintain prefix sums on array with point updates at index using fenwick tree.",
        "expected_family": "fenwick",
        "must_not_select_dp": True
    },
    {
        "id": "NDP-09",
        "title": "Sliding Window Maximum",
        "text": "Find maximum element in every sliding window of size k moving across array.",
        "must_not_select_dp": True
    },
    {
        "id": "NDP-10",
        "title": "Binary Search on Monotonic Answer",
        "text": "Find minimum capacity such that all packages can be shipped within D days.",
        "expected_family": "binary_search",
        "must_not_select_dp": True
    },
    {
        "id": "NDP-11",
        "title": "Trie Prefix Matching",
        "text": "Insert words into dictionary and check if any word starts with given prefix.",
        "expected_family": "trie",
        "must_not_select_dp": True
    },
    {
        "id": "NDP-12",
        "title": "Two Pointers Converging Pair Sum",
        "text": "Given a sorted array of integers, find two numbers that add up to target T.",
        "expected_family": "two_pointers_converging",
        "must_not_select_dp": True
    },
]


def run_all_dp_discrimination_holdouts() -> Dict[str, Any]:
    total = len(DISCRIMINATION_PROBLEMS)
    passed = 0
    failures = []

    print(f"\n========================================================")
    print(f"  CHUP Phase 3K — Dynamic Programming Discrimination Holdout")
    print(f"  Total Problems: {total} (NDP-01 through NDP-12)")
    print(f"========================================================\n")

    for prob in DISCRIMINATION_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]

        res = handle_request({"action": "solve", "problemText": text})
        selected_pattern = res.get("selectedPattern")
        family = res.get("family")

        # 1. Must NOT select any DP pattern if flagged
        if prob.get("must_not_select_dp") and selected_pattern in DP_PATTERNS:
            failures.append((pid, f"Violated must_not_select_dp: selected {selected_pattern}"))
            print(f"  [FAIL] {pid} - {title}: Incorrectly selected DP pattern {selected_pattern}")
            continue

        # 2. Anti-pattern elimination test
        if prob.get("anti_pattern_test"):
            expected_code = prob.get("expected_rejection_code")
            found_rejection = False
            for e in res.get("eliminatedCandidates", []):
                code = e.get("rejectionCode")
                if code == expected_code or (expected_code in ("DP_GREEDY_CHOICE_OPTIMAL", "DP_DOMINATED_BY_GREEDY") and code in ("DP_GREEDY_CHOICE_OPTIMAL", "DP_DOMINATED_BY_GREEDY")) or (expected_code in ("DP_NO_OVERLAPPING_SUBPROBLEMS", "DP_NO_REUSE_BENEFIT") and code in ("DP_NO_OVERLAPPING_SUBPROBLEMS", "DP_NO_REUSE_BENEFIT")):
                    found_rejection = True
                    break
            if found_rejection or res.get("status") == "rejected":
                passed += 1
                print(f"  [PASS] {pid} - {title} (Correctly rejected with {expected_code})")
            else:
                failures.append((pid, f"Expected rejection code {expected_code} not found"))
                print(f"  [FAIL] {pid} - {title}: Expected rejection {expected_code}")
            continue

        # 3. Family check
        if "expected_family" in prob:
            expected_fam = prob["expected_family"]
            if family == expected_fam:
                passed += 1
                print(f"  [PASS] {pid} - {title} (Correctly routed to {family})")
            else:
                failures.append((pid, f"Expected family {expected_fam}, got {family}"))
                print(f"  [FAIL] {pid} - {title}: Expected family {expected_fam}, got {family}")
            continue

        # Passed must_not_select_dp
        passed += 1
        print(f"  [PASS] {pid} - {title} (Correctly avoided DP, routed to {family})")

    summary = {
        "total": total,
        "passed": passed,
        "failures": failures
    }

    print("\n--------------------------------------------------------")
    print(f"  Discrimination Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("--------------------------------------------------------\n")

    return summary


if __name__ == "__main__":
    summary = run_all_dp_discrimination_holdouts()
    if summary["failures"]:
        sys.exit(1)
