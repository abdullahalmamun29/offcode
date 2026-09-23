"""
CHUP Phase 3O — String Algorithms & Automata Discrimination Holdout Evaluation.

Tests discrimination between Phase 3O string patterns and competing alternative families:
1. STR-D-01: Exact Single Pattern Matching (KMP Search vs Naive / Fallbacks) -> string / string_kmp_search
2. STR-D-02: Multi-Pattern Dictionary Matching (Aho-Corasick vs Individual KMP) -> string / string_aho_corasick
3. STR-D-03: Longest Palindromic Substring (Manacher O(N) vs Quadratic Expansion) -> string / string_manacher
4. STR-D-04: Full String Palindrome Verification (Two Pointers Converging vs Manacher) -> two_pointers_converging / palindrome_verification
5. STR-D-05: Suffix Sorting & LCP (Suffix Array vs Quadratic Trie) -> string / string_suffix_array
6. STR-D-06: Fast Subsequence Acceptance (Subsequence Automaton vs Two Pointers Scan) -> string / string_subsequence_automaton
7. STR-D-07: Edit Distance / Global Alignment (DP Levenshtein vs Contiguous Substring) -> dynamic_programming / dp_subsequence_string
8. STR-D-08: Minimum Window with Character Frequencies (Sliding Window vs Exact Pattern) -> sliding_window / minimum_window_substring
9. STR-D-09: Minimal Cyclic Rotation (Duval Lyndon vs Lexicographical Sort) -> string / string_lyndon_duval
10. STR-D-10: Distinct Substring Count (SAM O(N) vs Brute Force Set) -> string / string_suffix_automaton
11. STR-D-11: Exact Word Retrieval in Dictionary (Standard Trie vs Multi-Pattern Automaton) -> trie / trie_exact_search
12. STR-D-12: Longest Common Contiguous Substring (SAM LCS vs LCS Subsequence DP) -> string / string_longest_common_substring_sam
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
        "id": "STR-D-01",
        "title": "Exact Single Pattern Matching (KMP Search)",
        "text": "Find all occurrences of a pattern in text using KMP prefix function pi table.",
        "expected_family": "string",
        "expected_pattern": "string_kmp_search"
    },
    {
        "id": "STR-D-02",
        "title": "Multi-Pattern Dictionary Matching (Aho-Corasick)",
        "text": "Count occurrences of multiple dictionary patterns in text using Aho-Corasick automaton with failure links.",
        "expected_family": "string",
        "expected_pattern": "string_aho_corasick"
    },
    {
        "id": "STR-D-03",
        "title": "Longest Palindromic Substring (Manacher)",
        "text": "Find longest palindromic substring in linear time using Manacher algorithm.",
        "expected_family": "string",
        "expected_pattern": "string_manacher"
    },
    {
        "id": "STR-D-04",
        "title": "Full String Palindrome Verification (Two Pointers Converging)",
        "text": "Given a string S, determine if the entire string S is a palindrome by comparing characters from both ends converging inward.",
        "expected_family": "two_pointers_converging",
        "expected_pattern": "palindrome_verification"
    },
    {
        "id": "STR-D-05",
        "title": "Suffix Sorting & LCP (Suffix Array)",
        "text": "Construct suffix array and LCP array using prefix doubling and Kasai algorithm.",
        "expected_family": "string",
        "expected_pattern": "string_suffix_array"
    },
    {
        "id": "STR-D-06",
        "title": "Fast Subsequence Acceptance (Subsequence Automaton)",
        "text": "Process multiple subsequence existence queries on string using subsequence automaton transition table.",
        "expected_family": "string",
        "expected_pattern": "string_subsequence_automaton"
    },
    {
        "id": "STR-D-07",
        "title": "String Edit Distance / Alignment (Dynamic Programming)",
        "text": "Compute minimum edit distance between two strings with insertion deletion and substitution operations using dynamic programming table.",
        "expected_family": "dynamic_programming",
        "expected_pattern": "dp_subsequence_string"
    },
    {
        "id": "STR-D-08",
        "title": "Minimum Window Substring (Sliding Window)",
        "text": "Find the minimum window substring of text T containing all characters of target string using two pointers sliding window.",
        "expected_family": "sliding_window",
        "expected_pattern": "minimum_window_substring"
    },
    {
        "id": "STR-D-09",
        "title": "Minimal Cyclic Rotation (Duval Lyndon)",
        "text": "Find lexicographically minimal string rotation using Duval Lyndon factorization in O(N) time and O(1) space.",
        "expected_family": "string",
        "expected_pattern": "string_lyndon_duval"
    },
    {
        "id": "STR-D-10",
        "title": "Distinct Substring Count (Suffix Automaton)",
        "text": "Count total number of distinct substrings in string using Suffix Automaton SAM.",
        "expected_family": "string",
        "expected_pattern": "string_suffix_automaton"
    },
    {
        "id": "STR-D-11",
        "title": "Exact Word Retrieval in Dictionary (Standard Trie)",
        "text": "Given a dictionary of strings, insert all words and answer exact match query if a word exists in the dictionary using character prefix tree.",
        "expected_family": "trie",
        "expected_pattern": "trie_exact_search"
    },
    {
        "id": "STR-D-12",
        "title": "Longest Common Contiguous Substring (SAM LCS)",
        "text": "Find longest common contiguous substring between two strings using Suffix Automaton SAM.",
        "expected_family": "string",
        "expected_pattern": "string_longest_common_substring_sam"
    }
]


def run_discrimination_holdout():
    passed = 0
    failed = 0
    total = len(DISCRIMINATION_PROBLEMS)

    print("=" * 80)
    print("CHUP Phase 3O — String Discrimination Holdout Evaluation")
    print(f"Total problems: {total} (Competitor & boundary discrimination)")
    print("=" * 80)

    for prob in DISCRIMINATION_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]
        exp_family = prob["expected_family"]
        exp_pattern = prob["expected_pattern"]

        res = handle_request({"action": "solve", "problemText": text})

        act_family = res.get("family")
        act_pattern = res.get("selectedPattern")

        if act_family == exp_family and act_pattern == exp_pattern:
            passed += 1
            print(f"{pid} PASS: {title} -> {act_family} / {act_pattern}")
        else:
            failed += 1
            print(f"{pid} FAIL: {title}")
            print(f"   Expected: {exp_family} / {exp_pattern}")
            print(f"   Got:      {act_family} / {act_pattern}")

    print("=" * 80)
    print(f"Discrimination Holdout Results: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("=" * 80)
    return passed == total


if __name__ == "__main__":
    success = run_discrimination_holdout()
    sys.exit(0 if success else 1)
