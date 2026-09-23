"""
CHUP Phase 3M — Divide & Conquer, Backtracking & Exponential Decomposition Discrimination Holdout Evaluation.

Tests discrimination between Divide & Conquer / Backtracking and near-neighbor problem formulations
(DP overlapping subproblems, Greedy MST, Fenwick point updates, Segment Tree lazy propagation,
Graph Dijkstra, Advanced DSU, Trie prefix search, Monotonic Stack, Binary Search, Two Pointers,
and Section 8 Gate: Tower Problem).
"""

import sys
import os
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request

DISCRIMINATION_PROBLEMS = [
    {
        "id": "DCD-01",
        "title": "Overlapping Subproblems Fibonacci (Compete with DP)",
        "text": "Compute nth Fibonacci number with overlapping subproblems using 1d linear dynamic programming.",
        "expected_family": "dynamic_programming",
        "expected_pattern": "dp_1d_linear"
    },
    {
        "id": "DCD-02",
        "title": "0/1 Knapsack Discrete Items (Compete with DP)",
        "text": "0/1 knapsack where items are indivisible and cannot be broken into fractions. Maximize total value within capacity using dynamic programming.",
        "expected_family": "dynamic_programming",
        "expected_pattern": "dp_knapsack"
    },
    {
        "id": "DCD-03",
        "title": "Minimum Spanning Tree (Compete with Greedy)",
        "text": "Find minimum weight edge set connecting all vertices in undirected weighted graph using greedy MST.",
        "expected_family": "greedy",
        "expected_pattern": "greedy_graph_mst"
    },
    {
        "id": "DCD-04",
        "title": "Dynamic Prefix Sums with Point Updates (Compete with Fenwick)",
        "text": "Maintain array with dynamic point updates and answer prefix range sum queries using Fenwick tree.",
        "expected_family": "fenwick",
        "expected_pattern": "fenwick_point_update_prefix_query"
    },
    {
        "id": "DCD-05",
        "title": "Range Minimum Query with Range Add Updates (Compete with Segment Tree)",
        "text": "Range minimum query with range addition updates using segment tree with lazy propagation.",
        "expected_family": "segment_tree",
        "expected_pattern": "segment_tree_range_add_range_query"
    },
    {
        "id": "DCD-06",
        "title": "Shortest Path in Directed Graph (Compete with Graph)",
        "text": "Find shortest path from source vertex to all other vertices in non-negative weighted graph using Dijkstra.",
        "expected_family": "graph",
        "expected_pattern": "graph_dijkstra"
    },
    {
        "id": "DCD-07",
        "title": "Disjoint Set Connected Components (Compete with DSU)",
        "text": "Maintain incremental dynamic connectivity under edge additions using basic dsu union by rank.",
        "expected_family": "dsu",
        "expected_pattern": "dsu_basic"
    },
    {
        "id": "DCD-08",
        "title": "Trie Prefix Autocomplete (Compete with Trie)",
        "text": "Store dictionary of strings and query if any word starts with given prefix using trie.",
        "expected_family": "trie",
        "expected_pattern": "trie_prefix_search"
    },
    {
        "id": "DCD-09",
        "title": "Next Greater Element (Compete with Monotonic Stack)",
        "text": "Find next greater element to the right for each element in array using monotonic stack.",
        "expected_family": "monotonic_stack",
        "expected_pattern": "next_greater_element"
    },
    {
        "id": "DCD-10",
        "title": "Target Search in Sorted Array (Compete with Binary Search)",
        "text": "Find first position of target in sorted array using binary search lower bound.",
        "expected_family": "binary_search",
        "expected_pattern": "lower_bound"
    },
    {
        "id": "DCD-11",
        "title": "Two Pointers Converging Pair Sum (Compete with Two Pointers)",
        "text": "Find two numbers in sorted array that sum to target using converging two pointers.",
        "expected_family": "two_pointers_converging",
        "expected_pattern": "pair_sum_sorted"
    },
    {
        "id": "DCD-12",
        "title": "Section 8 Gate: Tower Problem (Cross-Family Composition Gate)",
        "text": "You are given n cubes. Build towers by placing each cube on an existing tower. Find minimum number of towers.",
        "expected_rejection_code": "COMPOSITION_UNSUPPORTED"
    }
]


def run_discrimination_holdout() -> Dict[str, Any]:
    print("=" * 80)
    print("CHUP Phase 3M — Divide & Conquer & Backtracking Discrimination Holdout")
    print(f"Total problems: {len(DISCRIMINATION_PROBLEMS)}")
    print("=" * 80)

    passed = 0
    failed = 0

    for prob in DISCRIMINATION_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]

        res = handle_request({"action": "solve", "problemText": text})

        # Check rejection expectation
        if prob.get("expected_rejection_code"):
            expected_rej = prob["expected_rejection_code"]
            elim_codes = [e["rejectionCode"] for e in res.get("eliminatedCandidates", []) if e.get("rejectionCode")]
            if expected_rej in elim_codes or res.get("status") == "rejected":
                passed += 1
                print(f"[{pid}] PASS: Correctly rejected with {expected_rej} ({title})")
            else:
                failed += 1
                print(f"[{pid}] FAIL: Expected rejection {expected_rej}, got status={res['status']}, elim={elim_codes} ({title})")
            continue

        # Check family expectation
        expected_fam = prob.get("expected_family")
        actual_fam = res.get("family")

        if expected_fam and actual_fam != expected_fam:
            failed += 1
            print(f"[{pid}] FAIL: Expected family '{expected_fam}', got '{actual_fam}' ({title})")
            continue

        # Check pattern expectation if specified
        expected_pat = prob.get("expected_pattern")
        actual_pat = res.get("selectedPattern")

        if expected_pat and actual_pat != expected_pat:
            failed += 1
            print(f"[{pid}] FAIL: Expected pattern '{expected_pat}', got '{actual_pat}' ({title})")
            continue

        passed += 1
        print(f"[{pid}] PASS: {title} (Family={actual_fam}, Pattern={actual_pat})")

    total = len(DISCRIMINATION_PROBLEMS)
    print("=" * 80)
    print(f"Discrimination Holdout Results: {passed}/{total} Passed ({passed/total*100:.1f}%)")
    print("=" * 80)

    return {"total": total, "passed": passed, "failed": failed}


if __name__ == "__main__":
    res = run_discrimination_holdout()
    if res["failed"] > 0:
        sys.exit(1)
