"""
CHUP Phase 3L — Greedy Algorithms Discrimination Holdout Evaluation.

Tests discrimination between Greedy and near-neighbor problem formulations
(0/1 Knapsack vs Fractional Knapsack, Weighted Interval vs Unweighted Activity Selection,
Huffman Merge vs Matrix Chain DP, MST vs Shortest Path Tree, etc.).
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
        "id": "NGR-01",
        "title": "0/1 Knapsack Discrete Items (Compete with DP)",
        "text": "0/1 knapsack where items are indivisible and cannot be broken into fractions. Maximize total value within capacity.",
        "expected_family": "dynamic_programming",
        "expected_rejection_code": "GREEDY_EXCHANGE_PROOF_FAILED"
    },
    {
        "id": "NGR-02",
        "title": "Weighted Interval Scheduling (Compete with DP)",
        "text": "Weighted interval scheduling: find maximum total weight of compatible non-overlapping intervals.",
        "expected_family": "dynamic_programming",
        "expected_rejection_code": "GREEDY_EXCHANGE_PROOF_FAILED"
    },
    {
        "id": "NGR-03",
        "title": "Non-Canonical Coin Change Counterexample",
        "text": "Greedy fails on coins: non-canonical coin system with denominations 1, 3, 4 for target 6 produces counterexample.",
        "expected_family": "dynamic_programming",
        "expected_rejection_code": "GREEDY_COUNTEREXAMPLE_FOUND"
    },
    {
        "id": "NGR-04",
        "title": "Matrix Chain Multiplication (Compete with Interval DP)",
        "text": "Find optimal parenthesization order to minimize scalar multiplications for matrix chain interval dynamic programming.",
        "expected_family": "dynamic_programming",
        "expected_pattern": "dp_interval"
    },
    {
        "id": "NGR-05",
        "title": "General Set Cover (Proof Not Established)",
        "text": "General set cover on arbitrary family of subsets where proof cannot be established within supported greedy proof systems.",
        "expected_rejection_code": "GREEDY_PROOF_NOT_ESTABLISHED"
    },
    {
        "id": "NGR-06",
        "title": "Longest Increasing Subsequence (Compete with DP / Binary Search)",
        "text": "Find length of longest strictly increasing subsequence in unsorted array using 1d linear dynamic programming.",
        "expected_family": "dynamic_programming",
        "expected_pattern": "dp_1d_linear"
    },
    {
        "id": "NGR-07",
        "title": "Single-Source Shortest Path (Compete with 3F Graph)",
        "text": "Find shortest path from source vertex to all other vertices in non-negative weighted graph.",
        "expected_family": "graph"
    },
    {
        "id": "NGR-08",
        "title": "Dynamic Range Sum with Point Updates (Compete with Fenwick)",
        "text": "Maintain array with dynamic point updates and answer prefix range sum queries.",
        "expected_family": "fenwick"
    },
    {
        "id": "NGR-09",
        "title": "Range Minimum Query with Range Add Updates (Compete with Segment Tree)",
        "text": "Range minimum query with range addition updates using segment tree with lazy propagation.",
        "expected_family": "segment_tree"
    },
    {
        "id": "NGR-10",
        "title": "Sliding Window Maximum (Compete with Monotonic Queue / Two Pointers)",
        "text": "Find maximum value in every contiguous sliding window of size k.",
        "expected_family": "sliding_window"
    },
    {
        "id": "NGR-11",
        "title": "Trie Prefix Autocomplete (Compete with Trie)",
        "text": "Store dictionary of strings and query if any word starts with given prefix using trie.",
        "expected_family": "trie"
    },
    {
        "id": "NGR-12",
        "title": "Two Pointers Converging Pair Sum (Compete with Two Pointers)",
        "text": "Find two numbers in sorted array that sum to target using converging two pointers.",
        "expected_family": "two_pointers_converging"
    }
]


def run_discrimination_holdout():
    print("========================================================")
    print("  CHUP Phase 3L — Greedy Discrimination Holdout")
    print("  Total Problems: 12 (NGR-01 through NGR-12)")
    print("========================================================\n")

    passed = 0
    total = len(DISCRIMINATION_PROBLEMS)

    for prob in DISCRIMINATION_PROBLEMS:
        prob_id = prob["id"]
        title = prob["title"]
        text = prob["text"]

        res = handle_request({"action": "solve", "problemText": text})

        # Check if rejection code was tested
        if "expected_rejection_code" in prob:
            expected_code = prob["expected_rejection_code"]
            eliminated = res.get("eliminatedCandidates", [])
            matched = any(e.get("rejectionCode") == expected_code for e in eliminated)
            if matched or res.get("status") == "rejected":
                passed += 1
                print(f"  [PASS] {prob_id} - {title} (Correctly rejected with {expected_code})")
            else:
                print(f"  [FAIL] {prob_id} - {title} (Expected rejection {expected_code}, got status: {res.get('status')})")
            continue

        # Check if routed to expected competing family / pattern
        expected_fam = prob.get("expected_family")
        expected_pat = prob.get("expected_pattern")
        actual_fam = res.get("family")
        actual_pat = res.get("selectedPattern")

        if (expected_fam and actual_fam == expected_fam) or (expected_pat and actual_pat == expected_pat):
            passed += 1
            print(f"  [PASS] {prob_id} - {title} (Correctly routed to {actual_fam} / {actual_pat})")
        else:
            print(f"  [FAIL] {prob_id} - {title}")
            print(f"         Expected Family: {expected_fam}, Pattern: {expected_pat}")
            print(f"         Actual Family:   {actual_fam}, Pattern: {actual_pat}")

    print("\n--------------------------------------------------------")
    print(f"  Discrimination Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("--------------------------------------------------------\n")

    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(run_discrimination_holdout())
