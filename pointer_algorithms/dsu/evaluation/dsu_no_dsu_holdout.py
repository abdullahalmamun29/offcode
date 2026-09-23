"""
CHUP Phase 3H — "No DSU" Discrimination Holdout Suite
12 problems that superficially resemble connectivity, components, or dynamic queries
but must NOT select DSU (or must reject DSU with explicit anti-pattern codes).
"""

import sys
import os
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.knowledge.taxonomy import DSU_PATTERNS

NO_DSU_PROBLEMS = [
    {
        "id": "ND-01",
        "title": "Online Edge Cut & Deletion",
        "text": "Arbitrary online edge deletion requested without offline knowledge: delete edge between u and v dynamically.",
        "must_not_select_dsu": True,
        "anti_pattern_test": True,
        "rejected_pattern": "dsu_basic",
        "expected_rejection_code": "DSU_DELETION_UNSUPPORTED"
    },
    {
        "id": "ND-02",
        "title": "Lowest Common Ancestor Queries",
        "text": "Find the lowest common ancestor of two nodes in a rooted binary tree.",
        "expected_family": "tree",
        "must_not_select_dsu": True
    },
    {
        "id": "ND-03",
        "title": "Shortest Path in Unweighted Graph",
        "text": "Find the shortest path distance in terms of number of edges between source s and destination t using BFS.",
        "expected_family": "graph",
        "must_not_select_dsu": True
    },
    {
        "id": "ND-04",
        "title": "Single-Source Shortest Paths with Weights",
        "text": "Find shortest path from starting vertex in weighted graph with non-negative edge weights using Dijkstra's algorithm.",
        "expected_family": "graph",
        "must_not_select_dsu": True
    },
    {
        "id": "ND-05",
        "title": "Topological Order of Task Prerequisites",
        "text": "Determine a valid topological ordering of tasks given prerequisite directed dependency edges.",
        "expected_family": "graph",
        "must_not_select_dsu": True
    },
    {
        "id": "ND-06",
        "title": "Minimum Spanning Tree with Prim",
        "text": "Find the minimum spanning tree weight of an undirected weighted graph using Prim's algorithm with a priority queue.",
        "expected_family": "graph",
        "must_not_select_dsu": True
    },
    {
        "id": "ND-07",
        "title": "Strongly Connected Components",
        "text": "Find strongly connected components in a directed graph using Tarjan's algorithm.",
        "expected_family": "graph",
        "must_not_select_dsu": True
    },
    {
        "id": "ND-08",
        "title": "Bridges in Communication Network",
        "text": "Find all critical bridges whose removal disconnects the communication network using DFS tin and low link.",
        "expected_family": "graph",
        "must_not_select_dsu": True
    },
    {
        "id": "ND-09",
        "title": "Dynamic Running Median",
        "text": "Maintain the dynamic median of a numerical stream using two balanced priority queues.",
        "expected_family": "heap",
        "must_not_select_dsu": True
    },
    {
        "id": "ND-10",
        "title": "Top-K Highest Values",
        "text": "Maintain top-k largest elements from a stream of numbers using a min-heap.",
        "expected_family": "heap",
        "must_not_select_dsu": True
    },
    {
        "id": "ND-11",
        "title": "Maximize Minimum Allocation",
        "text": "Find the maximum achievable threshold such that monotonic feasibility check is satisfied using binary search on answer.",
        "expected_family": "binary_search",
        "must_not_select_dsu": True
    },
    {
        "id": "ND-12",
        "title": "Online Interactive Disconnections",
        "text": "Online cut edge and disconnect edge operations arriving in real time.",
        "must_not_select_dsu": True,
        "anti_pattern_test": True,
        "rejected_pattern": "dsu_dynamic_connectivity",
        "expected_rejection_code": "DSU_DELETION_UNSUPPORTED"
    }
]


def run_no_dsu_holdout() -> bool:
    print("=" * 70)
    print("CHUP Phase 3H — 'No DSU' Discrimination Holdout (ND-01 through ND-12)")
    print("=" * 70)

    passed = 0
    total = len(NO_DSU_PROBLEMS)

    for prob in NO_DSU_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]

        resp = handle_request({"problemText": text})

        if prob.get("anti_pattern_test"):
            elim = resp.get("eliminatedCandidates", [])
            rej_pat = prob["rejected_pattern"]
            expected_code = prob["expected_rejection_code"]

            found_elim = any(
                e.get("candidate") == rej_pat and e.get("rejectionCode") == expected_code
                for e in elim
            )
            if found_elim:
                print(f"  [PASS] {pid} ({title}): Correctly eliminated {rej_pat} with {expected_code}")
                passed += 1
            else:
                print(f"  [FAIL] {pid} ({title}): Failed to eliminate {rej_pat} with {expected_code}. Elim: {elim}")
            continue

        selected_pat = resp.get("selectedPattern")
        selected_family = resp.get("family")
        expected_family = prob.get("expected_family")

        # Must NOT select any DSU pattern
        if selected_pat in DSU_PATTERNS or selected_family == "dsu":
            print(f"  [FAIL] {pid} ({title}): Erroneously selected DSU pattern '{selected_pat}' (family: {selected_family})")
            continue

        if expected_family and selected_family != expected_family:
            print(f"  [FAIL] {pid} ({title}): Expected family '{expected_family}', got '{selected_family}' (pattern: {selected_pat})")
            continue

        print(f"  [PASS] {pid} ({title}): Correctly routed away from DSU to {selected_family} ({selected_pat})")
        passed += 1

    print("=" * 70)
    print(f"'No DSU' Discrimination Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 70)
    return passed == total


if __name__ == "__main__":
    success = run_no_dsu_holdout()
    sys.exit(0 if success else 1)
