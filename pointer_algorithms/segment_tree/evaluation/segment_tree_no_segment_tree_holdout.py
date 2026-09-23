"""
CHUP Phase 3J — "No Segment Tree" Discrimination Holdout Suite.
12 problems that superficially resemble range queries, updates, or tree operations
but must NOT select Segment Tree (or must reject Segment Tree with explicit anti-pattern codes):
NS-01 through NS-12.
"""

import sys
import os
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.knowledge.taxonomy import SEGMENT_TREE_PATTERNS

NO_SEGMENT_TREE_PROBLEMS = [
    {
        "id": "NS-01",
        "title": "Static Array Range Minimum Queries",
        "text": "Static array with no updates: range minimum queries on fixed array without updates.",
        "must_not_select_segtree": True,
        "anti_pattern_test": True,
        "rejected_pattern": "segment_tree_point_update_range_query",
        "expected_rejection_code": "SEGMENT_TREE_STATIC_QUERY_SUBOPTIMAL"
    },
    {
        "id": "NS-02",
        "title": "Point Updates with Prefix Sum Queries Only",
        "text": "Point updates at index with prefix sum only queries on array.",
        "must_not_select_segtree": True,
        "anti_pattern_test": True,
        "rejected_pattern": "segment_tree_point_update_range_query",
        "expected_rejection_code": "SEGMENT_TREE_SIMPLE_PREFIX_OVERKILL"
    },
    {
        "id": "NS-03",
        "title": "Batch Range Additions Offline",
        "text": "Batch range adds where queries are only at the end with final reconstruction.",
        "must_not_select_segtree": True,
        "anti_pattern_test": True,
        "rejected_pattern": "segment_tree_range_add_range_query",
        "expected_rejection_code": "SEGMENT_TREE_DIFFERENCE_ARRAY_OVERKILL"
    },
    {
        "id": "NS-04",
        "title": "Dynamic Median Without Rank Tree",
        "text": "Dynamic median without rank tree requires non-associative interval query.",
        "must_not_select_segtree": True,
        "anti_pattern_test": True,
        "rejected_pattern": "segment_tree_point_update_range_query",
        "expected_rejection_code": "SEGMENT_TREE_NO_ASSOCIATIVE_MERGE"
    },
    {
        "id": "NS-05",
        "title": "Range Chmin and Chmax Operations",
        "text": "Range chmin and range sum queries require segment tree beats.",
        "must_not_select_segtree": True,
        "anti_pattern_test": True,
        "rejected_pattern": "segment_tree_range_add_range_query",
        "expected_rejection_code": "SEGMENT_TREE_STANDARD_LAZY_INSUFFICIENT"
    },
    {
        "id": "NS-06",
        "title": "Memory Budget Exceeded Under 4N Allocation",
        "text": "Segment tree 4 * N * sizeof(Node) budget exceeded with memory limit exceeded.",
        "must_not_select_segtree": True,
        "anti_pattern_test": True,
        "rejected_pattern": "segment_tree_point_update_range_query",
        "expected_rejection_code": "SEGMENT_TREE_RESOURCE_LIMIT"
    },
    {
        "id": "NS-07",
        "title": "Negative Frequencies in K-th Element Search",
        "text": "Allow negative counts for k-th element in frequency segment tree.",
        "must_not_select_segtree": True,
        "anti_pattern_test": True,
        "rejected_pattern": "segment_tree_frequency_order_statistic",
        "expected_rejection_code": "SEGMENT_TREE_KTH_NEGATIVE_FREQUENCY"
    },
    {
        "id": "NS-08",
        "title": "Dynamic Connectivity in Undirected Graph",
        "text": "Maintain connected components as edges are added dynamically and query if two vertices are in the same set.",
        "expected_family": "dsu",
        "must_not_select_segtree": True
    },
    {
        "id": "NS-09",
        "title": "Single Source Shortest Path",
        "text": "Find shortest path distance from source to destination in graph with non-negative edge weights using Dijkstra.",
        "expected_family": "graph",
        "must_not_select_segtree": True
    },
    {
        "id": "NS-10",
        "title": "Binary Search Tree Lowest Common Ancestor",
        "text": "Find lowest common ancestor of two nodes in binary search tree with ordered branches.",
        "expected_family": "tree",
        "must_not_select_segtree": True
    },
    {
        "id": "NS-11",
        "title": "Dictionary Prefix Matching",
        "text": "Find longest common prefix matching across word dictionary using trie.",
        "expected_family": "trie",
        "must_not_select_segtree": True
    },
    {
        "id": "NS-12",
        "title": "Dynamic Median of Streaming Numbers",
        "text": "Maintain median of streaming numbers using two heaps min-heap and max-heap.",
        "expected_family": "heap",
        "must_not_select_segtree": True
    },
]


def run_no_segment_tree_holdout() -> Dict[str, Any]:
    print("=" * 70)
    print("CHUP Phase 3J — 'No Segment Tree' Discrimination Holdout (12 Problems)")
    print("=" * 70)

    total = len(NO_SEGMENT_TREE_PROBLEMS)
    passed = 0
    results = []

    for prob in NO_SEGMENT_TREE_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]

        res = handle_request({"problemText": text})
        sel_pat = res.get("selectedPattern")
        sel_fam = res.get("family")

        # Must not select Segment Tree
        if sel_pat in SEGMENT_TREE_PATTERNS or sel_fam == "segment_tree":
            print(f"[{pid}] {title}: FAIL (Erroneously selected Segment Tree: {sel_pat})")
            results.append((pid, title, False, f"Erroneously selected: {sel_pat}"))
            continue

        if prob.get("anti_pattern_test"):
            exp_code = prob["expected_rejection_code"]
            elim = res.get("eliminatedCandidates", [])
            has_rejection = any(e.get("rejectionCode") == exp_code for e in elim)
            if has_rejection:
                passed += 1
                print(f"[{pid}] {title}: PASS (Rejected Segment Tree with {exp_code})")
                results.append((pid, title, True, f"Rejected with {exp_code}"))
            else:
                print(f"[{pid}] {title}: FAIL (Missing expected rejection {exp_code}, elim={elim})")
                results.append((pid, title, False, f"Missing rejection: {exp_code}"))
            continue

        if "expected_family" in prob:
            exp_fam = prob["expected_family"]
            if sel_fam == exp_fam:
                passed += 1
                print(f"[{pid}] {title}: PASS (Correctly routed to {exp_fam})")
                results.append((pid, title, True, f"Routed to {exp_fam}"))
            else:
                print(f"[{pid}] {title}: FAIL (Expected family {exp_fam}, got {sel_fam})")
                results.append((pid, title, False, f"Family mismatch: {sel_fam}"))
            continue

        passed += 1
        print(f"[{pid}] {title}: PASS (Did not select Segment Tree)")
        results.append((pid, title, True, "Correctly avoided Segment Tree"))

    rate = (passed / total) * 100
    print("-" * 70)
    print(f"No-Segment-Tree Results: {passed}/{total} passed ({rate:.1f}%)")
    print("-" * 70)

    return {
        "total": total,
        "passed": passed,
        "rate": rate,
        "results": results
    }


if __name__ == "__main__":
    res = run_no_segment_tree_holdout()
    if res["passed"] < res["total"]:
        sys.exit(1)
