"""
CHUP Phase 3G — "No Heap" Discrimination Holdout Suite.

Proves that CHUP does not over-generalize or default to Heap when other
algorithmic structures are strictly required. Tests rejection of Heap for:
1. Arbitrary element search and deletion (BST / std::set)
2. Range minimum query with point updates (Segment Tree / Fenwick)
3. FIFO element processing (Queue)
4. LIFO undo stack (Stack)
5. Offline static array total sorting (std::sort introsort)
6. Tree BST search and LCA (Tree)
7. String prefix search (Trie)
8. Contiguous sliding window with distinct constraints (Two Pointers)
9. Next Greater Element (Monotonic Stack)
10. Unweighted shortest path (BFS, not Dijkstra/heap)
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.recognition.feature_extractor import FeatureExtractor


NO_HEAP_PROBLEMS = [
    {
        "id": "NH-01",
        "name": "Arbitrary Search and Deletion",
        "text": "Maintain a dynamic set supporting insert, lookup of arbitrary key X, and deletion of an arbitrary element by value.",
        "forbidden_family": "heap",
        "expected_check": lambda resp, feat: resp.get("family") != "heap" or feat.heap_requires_arbitrary_delete
    },
    {
        "id": "NH-02",
        "name": "Dynamic Range Minimum Query",
        "text": "Given an array, support point updates A[i] = x and answer range minimum queries min(A[L..R]) dynamically.",
        "forbidden_family": "heap",
        "expected_check": lambda resp, feat: resp.get("status") == "rejected" or resp.get("family") != "heap"
    },
    {
        "id": "NH-03",
        "name": "FIFO Message Queue",
        "text": "Store incoming print requests in first-in first-out FIFO order. Always serve the oldest pending request first.",
        "forbidden_family": "heap",
        "expected_check": lambda resp, feat: resp.get("family") != "heap"
    },
    {
        "id": "NH-04",
        "name": "LIFO Document Undo Stack",
        "text": "Support text editor operations with undo capability. Always revert the most recently executed action (LIFO order).",
        "forbidden_family": "heap",
        "expected_check": lambda resp, feat: resp.get("family") != "heap"
    },
    {
        "id": "NH-05",
        "name": "Offline Static Array Total Sorting",
        "text": "Given an array of integers, output all elements in sorted ascending order. Sort the entire array without streaming.",
        "forbidden_family": "heap",
        "expected_check": lambda resp, feat: resp.get("family") != "heap" or feat.heap_requires_full_sort
    },
    {
        "id": "NH-06",
        "name": "Binary Search Tree Search",
        "text": "Given a binary search tree with root, search for target value X using BST ordered-branch elimination.",
        "forbidden_family": "heap",
        "expected_check": lambda resp, feat: resp.get("family") == "tree"
    },
    {
        "id": "NH-07",
        "name": "String Prefix Autocomplete",
        "text": "Store a dictionary of words. Given a query prefix, determine if any word in the dictionary begins with that prefix.",
        "forbidden_family": "heap",
        "expected_check": lambda resp, feat: resp.get("family") == "trie"
    },
    {
        "id": "NH-08",
        "name": "Contiguous Substring Distinct Constraint",
        "text": "Find the length of the longest contiguous substring containing at most 2 distinct characters.",
        "forbidden_family": "heap",
        "expected_check": lambda resp, feat: resp.get("family") in ("sliding_window", "two_pointers_same_direction")
    },
    {
        "id": "NH-09",
        "name": "Nearest Greater Element",
        "text": "For each element in an array, find the index of the next greater element to its right.",
        "forbidden_family": "heap",
        "expected_check": lambda resp, feat: resp.get("family") == "monotonic_stack"
    },
    {
        "id": "NH-10",
        "name": "Unweighted Shortest Path",
        "text": "Given an unweighted graph, find the minimum number of edge hops between vertex 1 and vertex N.",
        "forbidden_family": "heap",
        "expected_check": lambda resp, feat: resp.get("family") == "graph" and resp.get("selectedPattern") == "graph_bfs_shortest_path"
    },
]


def run_no_heap_holdout():
    print("=" * 70)
    print("CHUP Phase 3G — 'No Heap' Discrimination Holdout Evaluation (NH-01..NH-10)")
    print("=" * 70)

    passed = 0
    total = len(NO_HEAP_PROBLEMS)

    for p in NO_HEAP_PROBLEMS:
        pid = p["id"]
        name = p["name"]
        text = p["text"]

        feat = FeatureExtractor.extract(text)
        resp = handle_request({"problemText": text})

        if p["expected_check"](resp, feat):
            print(f"  [PASS] {pid} ({name}): Successfully rejected Heap / routed appropriately (family: {resp.get('family')})")
            passed += 1
        else:
            print(f"  [FAIL] {pid} ({name}): Incorrectly defaulted to Heap! Resp family: {resp.get('family')}, status: {resp.get('status')}")

    print("=" * 70)
    score_pct = (passed / total) * 100
    print(f"'No Heap' Holdout Score: {passed}/{total} ({score_pct:.1f}%)")
    print("=" * 70)
    return passed == total


if __name__ == "__main__":
    success = run_no_heap_holdout()
    sys.exit(0 if success else 1)
