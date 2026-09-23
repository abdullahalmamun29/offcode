"""
CHUP Phase 3O — String Algorithms & Automata Benchmark Suite.

Evaluates recognition, structural derivation, invariant construction,
code generation, and C++17 execution across all 10 Phase 3O patterns (60 problems total):

3O-A: Knuth-Morris-Pratt (KMP) Search (STR-01..STR-06)
3O-B: Z-Algorithm LCP Boxes (STR-07..STR-12)
3O-C: Rabin-Karp Rolling Hash (STR-13..STR-18)
3O-D: Manacher Longest Palindrome (STR-19..STR-24)
3O-E: Aho-Corasick Multi-Pattern Search (STR-25..STR-30)
3O-F: Suffix Array & Kasai LCP (STR-31..STR-36)
3O-G: Suffix Automaton Distinct Substrings (STR-37..STR-42)
3O-H: Duval Lyndon Minimal Rotation (STR-43..STR-48)
3O-I: Subsequence Automaton (STR-49..STR-54)
3O-J: SAM Longest Common Substring (STR-55..STR-60)
"""

import sys
import os
import subprocess
import tempfile
import hashlib
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.strings.verification.string_oracles import (
    string_kmp_oracle,
    string_z_algorithm_oracle,
    string_rabin_karp_oracle,
    string_manacher_oracle,
    string_aho_corasick_oracle,
    string_suffix_array_lcp_oracle,
    string_sam_distinct_substrings_oracle,
    string_lyndon_duval_oracle,
    string_subsequence_automaton_oracle,
    string_lcs_sam_oracle
)

COMPILED_BINARIES: Dict[str, str] = {}


def compile_and_run_cpp(code: str, stdin_data: str, timeout: int = 10) -> str:
    code_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()
    exe = COMPILED_BINARIES.get(code_hash)
    if not exe or not os.path.exists(exe):
        tmp_cpp = tempfile.NamedTemporaryFile(suffix=".cpp", delete=False)
        tmp_cpp.write(code.encode("utf-8"))
        tmp_cpp.close()
        exe = tmp_cpp.name[:-4]
        compile_res = subprocess.run(
            ["g++", "-std=c++17", "-O2", tmp_cpp.name, "-o", exe],
            capture_output=True, text=True
        )
        if compile_res.returncode != 0:
            return f"COMPILE_ERROR: {compile_res.stderr[:200]}"
        COMPILED_BINARIES[code_hash] = exe
    try:
        run_res = subprocess.run(
            [exe], input=stdin_data, capture_output=True, text=True, timeout=timeout
        )
        if run_res.returncode != 0:
            return f"RUNTIME_ERROR: {run_res.stderr[:200]}"
        return run_res.stdout.strip()
    except subprocess.TimeoutExpired:
        return "RUNTIME_ERROR: TimeoutExpired"


BENCHMARK_PROBLEMS = [
    # ── 3O-A: KMP Single Pattern Matching (STR-01..STR-06) ──
    {
        "id": "STR-01",
        "category": "3O-A",
        "title": "Basic KMP Pattern Matching",
        "text": "Find all occurrences of a pattern in text using KMP prefix function pi table.",
        "expected_pattern": "string_kmp_search",
        "input": "ababcababa aba",
        "oracle_fn": lambda: "0 5 7"
    },
    {
        "id": "STR-02",
        "category": "3O-A",
        "title": "KMP Overlapping Pattern Occurrences",
        "text": "Find all overlapping matches of pattern in text using Knuth-Morris-Pratt failure function.",
        "expected_pattern": "string_kmp_search",
        "input": "aaaaa aa",
        "oracle_fn": lambda: "0 1 2 3"
    },
    {
        "id": "STR-03",
        "category": "3O-A",
        "title": "KMP Single Occurrence",
        "text": "Find single occurrence of pattern P in string T using KMP border array.",
        "expected_pattern": "string_kmp_search",
        "input": "abcdefg cde",
        "oracle_fn": lambda: "2"
    },
    {
        "id": "STR-04",
        "category": "3O-A",
        "title": "KMP No Match Found",
        "text": "Locate occurrences of pattern in text using KMP prefix table deterministically.",
        "expected_pattern": "string_kmp_search",
        "input": "abcdefg xyz",
        "oracle_fn": lambda: ""
    },
    {
        "id": "STR-05",
        "category": "3O-A",
        "title": "KMP Periodic Pattern Matches",
        "text": "Find all periodic pattern occurrences in text via KMP prefix table.",
        "expected_pattern": "string_kmp_search",
        "input": "abcabcabc abc",
        "oracle_fn": lambda: "0 3 6"
    },
    {
        "id": "STR-06",
        "category": "3O-A",
        "title": "KMP Self Match",
        "text": "Find pattern in text where pattern equals text using KMP prefix function.",
        "expected_pattern": "string_kmp_search",
        "input": "chup chup",
        "oracle_fn": lambda: "0"
    },

    # ── 3O-B: Z-Algorithm (STR-07..STR-12) ──
    {
        "id": "STR-07",
        "category": "3O-B",
        "title": "Basic Z-Algorithm LCP Array",
        "text": "Compute Z-algorithm array of longest common prefix between suffix and entire string.",
        "expected_pattern": "string_z_algorithm",
        "input": "abacaba",
        "oracle_fn": lambda: "7 0 1 0 3 0 1"
    },
    {
        "id": "STR-08",
        "category": "3O-B",
        "title": "Z-Algorithm All Identical Characters",
        "text": "Compute Z values for string with repeated characters using Z-box boundaries.",
        "expected_pattern": "string_z_algorithm",
        "input": "aaaa",
        "oracle_fn": lambda: "4 3 2 1"
    },
    {
        "id": "STR-09",
        "category": "3O-B",
        "title": "Z-Algorithm Alternating String",
        "text": "Calculate Z-array values for alternating string using linear-time Z-algorithm.",
        "expected_pattern": "string_z_algorithm",
        "input": "ababab",
        "oracle_fn": lambda: "6 0 4 0 2 0"
    },
    {
        "id": "STR-10",
        "category": "3O-B",
        "title": "Z-Algorithm Distinct Characters",
        "text": "Compute Z-box array on string of distinct characters.",
        "expected_pattern": "string_z_algorithm",
        "input": "abcdef",
        "oracle_fn": lambda: "6 0 0 0 0 0"
    },
    {
        "id": "STR-11",
        "category": "3O-B",
        "title": "Z-Algorithm Palindrome",
        "text": "Evaluate Z-array prefix matches for palindromic word using Z-box algorithm.",
        "expected_pattern": "string_z_algorithm",
        "input": "racecar",
        "oracle_fn": lambda: "7 0 0 0 0 0 1"
    },
    {
        "id": "STR-12",
        "category": "3O-B",
        "title": "Z-Algorithm Boundary Extension",
        "text": "Compute Z-algorithm values where Z-box extends past current right boundary.",
        "expected_pattern": "string_z_algorithm",
        "input": "aabxaabxcaabxaabxay",
        "oracle_fn": lambda: "19 1 0 0 4 1 0 0 0 8 1 0 0 5 1 0 0 1 0"
    },

    # ── 3O-C: Rabin-Karp Rolling Hash (STR-13..STR-18) ──
    {
        "id": "STR-13",
        "category": "3O-C",
        "title": "Basic Rabin-Karp Single Pattern",
        "text": "Search pattern in text using Rabin-Karp polynomial rolling hash probabilistic matching.",
        "expected_pattern": "string_rabin_karp",
        "input": "ababcababa aba",
        "oracle_fn": lambda: "0 5 7"
    },
    {
        "id": "STR-14",
        "category": "3O-C",
        "title": "Rabin-Karp Repeated Match",
        "text": "Find occurrences of repeated substring using Rabin-Karp rolling hash.",
        "expected_pattern": "string_rabin_karp",
        "input": "banana an",
        "oracle_fn": lambda: "1 3"
    },
    {
        "id": "STR-15",
        "category": "3O-C",
        "title": "Rabin-Karp End of Text Match",
        "text": "Locate pattern matching the suffix of text using rolling hash Rabin-Karp.",
        "expected_pattern": "string_rabin_karp",
        "input": "codeforge forge",
        "oracle_fn": lambda: "4"
    },
    {
        "id": "STR-16",
        "category": "3O-C",
        "title": "Rabin-Karp Disjoint Matches",
        "text": "Find disjoint pattern occurrences using polynomial rolling hash Rabin-Karp.",
        "expected_pattern": "string_rabin_karp",
        "input": "catdogcatdogcat cat",
        "oracle_fn": lambda: "0 6 12"
    },
    {
        "id": "STR-17",
        "category": "3O-C",
        "title": "Rabin-Karp Single Character Pattern",
        "text": "Search for single character pattern using Rabin-Karp rolling hash.",
        "expected_pattern": "string_rabin_karp",
        "input": "mississippi s",
        "oracle_fn": lambda: "2 3 5 6"
    },
    {
        "id": "STR-18",
        "category": "3O-C",
        "title": "Rabin-Karp No Occurrences",
        "text": "Detect absent pattern in text using Rabin-Karp double rolling hash.",
        "expected_pattern": "string_rabin_karp",
        "input": "abcdefg zzz",
        "oracle_fn": lambda: ""
    },

    # ── 3O-D: Manacher Palindrome (STR-19..STR-24) ──
    {
        "id": "STR-19",
        "category": "3O-D",
        "title": "Basic Manacher Odd Palindrome",
        "text": "Find longest palindromic substring in linear time using Manacher algorithm.",
        "expected_pattern": "string_manacher",
        "input": "babad",
        "oracle_fn": lambda: "3\nbab"  # or aba
    },
    {
        "id": "STR-20",
        "category": "3O-D",
        "title": "Manacher Even Length Palindrome",
        "text": "Find even-length longest palindromic substring using Manacher with delimiter transformation.",
        "expected_pattern": "string_manacher",
        "input": "cbbd",
        "oracle_fn": lambda: "2\nbb"
    },
    {
        "id": "STR-21",
        "category": "3O-D",
        "title": "Manacher Entire String Palindrome",
        "text": "Locate longest palindromic substring in a palindrome using Manacher algorithm.",
        "expected_pattern": "string_manacher",
        "input": "racecar",
        "oracle_fn": lambda: "7\nracecar"
    },
    {
        "id": "STR-22",
        "category": "3O-D",
        "title": "Manacher Multiple Non-Overlapping Palindromes",
        "text": "Find longest palindromic substring with multiple candidate centers using Manacher.",
        "expected_pattern": "string_manacher",
        "input": "abacdfgdcaba",
        "oracle_fn": lambda: "3\naba"
    },
    {
        "id": "STR-23",
        "category": "3O-D",
        "title": "Manacher All Same Characters",
        "text": "Find longest palindrome in string of repeated characters using Manacher.",
        "expected_pattern": "string_manacher",
        "input": "aaaaa",
        "oracle_fn": lambda: "5\naaaaa"
    },
    {
        "id": "STR-24",
        "category": "3O-D",
        "title": "Manacher No Palindrome Longer Than 1",
        "text": "Compute longest palindromic substring on strictly increasing string via Manacher.",
        "expected_pattern": "string_manacher",
        "input": "abcdef",
        "oracle_fn": lambda: "1\na"
    },

    # ── 3O-E: Aho-Corasick Multi-Pattern Matching (STR-25..STR-30) ──
    {
        "id": "STR-25",
        "category": "3O-E",
        "title": "Classic Aho-Corasick Dictionary",
        "text": "Count occurrences of multiple dictionary patterns in text using Aho-Corasick automaton with failure links.",
        "expected_pattern": "string_aho_corasick",
        "input": "4\nhe\nshe\nhis\nhers\nushers",
        "oracle_fn": lambda: "1\n1\n0\n1"
    },
    {
        "id": "STR-26",
        "category": "3O-E",
        "title": "Aho-Corasick Prefix Suffix Overlaps",
        "text": "Find all matches for set of patterns in text using Aho-Corasick trie dictionary jumps.",
        "expected_pattern": "string_aho_corasick",
        "input": "3\na\naa\naaa\naaaa",
        "oracle_fn": lambda: "4\n3\n2"
    },
    {
        "id": "STR-27",
        "category": "3O-E",
        "title": "Aho-Corasick Single Letter Dictionary",
        "text": "Search multiple keywords simultaneously in text using Aho-Corasick automaton.",
        "expected_pattern": "string_aho_corasick",
        "input": "3\na\nb\nc\nabcba",
        "oracle_fn": lambda: "2\n2\n1"
    },
    {
        "id": "STR-28",
        "category": "3O-E",
        "title": "Aho-Corasick Substring Hierarchy",
        "text": "Count occurrences of nested pattern dictionary in text using Aho-Corasick failure links.",
        "expected_pattern": "string_aho_corasick",
        "input": "3\nin\nout\ninside\ninsideout",
        "oracle_fn": lambda: "1\n1\n1"
    },
    {
        "id": "STR-29",
        "category": "3O-E",
        "title": "Aho-Corasick Disjoint Words",
        "text": "Query multiple string keywords in text using Aho-Corasick automaton.",
        "expected_pattern": "string_aho_corasick",
        "input": "2\napple\nbanana\napplepieandbananashake",
        "oracle_fn": lambda: "1\n1"
    },
    {
        "id": "STR-30",
        "category": "3O-E",
        "title": "Aho-Corasick Zero Matches",
        "text": "Match dictionary words against text with no occurrences using Aho-Corasick.",
        "expected_pattern": "string_aho_corasick",
        "input": "2\nxyz\nuvw\nabcdef",
        "oracle_fn": lambda: "0\n0"
    },

    # ── 3O-F: Suffix Array & Kasai LCP (STR-31..STR-36) ──
    {
        "id": "STR-31",
        "category": "3O-F",
        "title": "Classic Banana Suffix Array and Kasai LCP",
        "text": "Construct suffix array and LCP array using prefix doubling and Kasai algorithm.",
        "expected_pattern": "string_suffix_array",
        "input": "banana",
        "oracle_fn": lambda: "5 3 1 0 4 2\n1 3 0 0 2"
    },
    {
        "id": "STR-32",
        "category": "3O-F",
        "title": "Suffix Array Distinct Characters",
        "text": "Build suffix array and Kasai LCP for string of distinct characters.",
        "expected_pattern": "string_suffix_array",
        "input": "abcdef",
        "oracle_fn": lambda: "0 1 2 3 4 5\n0 0 0 0 0"
    },
    {
        "id": "STR-33",
        "category": "3O-F",
        "title": "Suffix Array All Identical Characters",
        "text": "Construct suffix array and Kasai LCP for repeated character string.",
        "expected_pattern": "string_suffix_array",
        "input": "aaaa",
        "oracle_fn": lambda: "3 2 1 0\n1 2 3"
    },
    {
        "id": "STR-34",
        "category": "3O-F",
        "title": "Suffix Array Reversed Alphabet",
        "text": "Compute suffix array and LCP values for reverse sorted string via Kasai.",
        "expected_pattern": "string_suffix_array",
        "input": "fedcba",
        "oracle_fn": lambda: "5 4 3 2 1 0\n0 0 0 0 0"
    },
    {
        "id": "STR-35",
        "category": "3O-F",
        "title": "Suffix Array Mississipi",
        "text": "Build suffix array and compute longest common prefix array using Kasai algorithm.",
        "expected_pattern": "string_suffix_array",
        "input": "mississippi",
        "oracle_fn": lambda: "10 7 4 1 0 9 8 6 3 5 2\n1 1 4 0 0 1 0 2 1 3"
    },
    {
        "id": "STR-36",
        "category": "3O-F",
        "title": "Suffix Array Two Alternating Characters",
        "text": "Construct suffix array and Kasai LCP for alternating string abab.",
        "expected_pattern": "string_suffix_array",
        "input": "abab",
        "oracle_fn": lambda: "2 0 3 1\n2 0 1"
    },

    # ── 3O-G: Suffix Automaton Distinct Substrings (STR-37..STR-42) ──
    {
        "id": "STR-37",
        "category": "3O-G",
        "title": "SAM Distinct Substrings for Banana",
        "text": "Count total number of distinct substrings in string using Suffix Automaton SAM.",
        "expected_pattern": "string_suffix_automaton",
        "input": "banana",
        "oracle_fn": lambda: "15"
    },
    {
        "id": "STR-38",
        "category": "3O-G",
        "title": "SAM Distinct Substrings Distinct Characters",
        "text": "Compute number of distinct substrings for string with unique characters via Suffix Automaton.",
        "expected_pattern": "string_suffix_automaton",
        "input": "abcde",
        "oracle_fn": lambda: "15"
    },
    {
        "id": "STR-39",
        "category": "3O-G",
        "title": "SAM Distinct Substrings All Identical",
        "text": "Count distinct substrings in repeated character string using Suffix Automaton.",
        "expected_pattern": "string_suffix_automaton",
        "input": "aaaa",
        "oracle_fn": lambda: "4"
    },
    {
        "id": "STR-40",
        "category": "3O-G",
        "title": "SAM Distinct Substrings Alternating",
        "text": "Count total distinct substrings in alternating string using Suffix Automaton linear construction.",
        "expected_pattern": "string_suffix_automaton",
        "input": "ababab",
        "oracle_fn": lambda: "11"
    },
    {
        "id": "STR-41",
        "category": "3O-G",
        "title": "SAM Distinct Substrings Palindrome",
        "text": "Calculate count of distinct substrings for palindromic string using SAM.",
        "expected_pattern": "string_suffix_automaton",
        "input": "racecar",
        "oracle_fn": lambda: "25"
    },
    {
        "id": "STR-42",
        "category": "3O-G",
        "title": "SAM Distinct Substrings Long String",
        "text": "Count unique substrings in string using Suffix Automaton online construction.",
        "expected_pattern": "string_suffix_automaton",
        "input": "abracadabra",
        "oracle_fn": lambda: "54"
    },

    # ── 3O-H: Duval Lyndon Factorization & Minimal Rotation (STR-43..STR-48) ──
    {
        "id": "STR-43",
        "category": "3O-H",
        "title": "Duval Minimal Rotation Abracadabra",
        "text": "Find lexicographically minimal string rotation using Duval Lyndon factorization in O(N) time and O(1) space.",
        "expected_pattern": "string_lyndon_duval",
        "input": "abracadabra",
        "oracle_fn": lambda: "aabracadabr"
    },
    {
        "id": "STR-44",
        "category": "3O-H",
        "title": "Duval Minimal Rotation Already Minimal",
        "text": "Find lexicographically smallest cyclic shift via Duval algorithm.",
        "expected_pattern": "string_lyndon_duval",
        "input": "abcde",
        "oracle_fn": lambda: "abcde"
    },
    {
        "id": "STR-45",
        "category": "3O-H",
        "title": "Duval Minimal Rotation Reversed",
        "text": "Compute minimal rotation for decreasing string using Duval's algorithm.",
        "expected_pattern": "string_lyndon_duval",
        "input": "edcba",
        "oracle_fn": lambda: "aedcb"
    },
    {
        "id": "STR-46",
        "category": "3O-H",
        "title": "Duval Minimal Rotation Identical Characters",
        "text": "Find lexicographically minimal cyclic shift for string of identical characters using Duval.",
        "expected_pattern": "string_lyndon_duval",
        "input": "aaaa",
        "oracle_fn": lambda: "aaaa"
    },
    {
        "id": "STR-47",
        "category": "3O-H",
        "title": "Duval Minimal Rotation Banana",
        "text": "Determine minimal cyclic rotation of word using Duval's algorithm.",
        "expected_pattern": "string_lyndon_duval",
        "input": "banana",
        "oracle_fn": lambda: "abanan"
    },
    {
        "id": "STR-48",
        "category": "3O-H",
        "title": "Duval Minimal Rotation Multiple Minimums",
        "text": "Compute minimal cyclic shift with repeated prefixes using Duval Lyndon factorizer.",
        "expected_pattern": "string_lyndon_duval",
        "input": "bbaabb",
        "oracle_fn": lambda: "aabbbb"
    },

    # ── 3O-I: Subsequence Automaton (STR-49..STR-54) ──
    {
        "id": "STR-49",
        "category": "3O-I",
        "title": "Basic Subsequence Automaton Queries",
        "text": "Process multiple subsequence existence queries on string using subsequence automaton transition table.",
        "expected_pattern": "string_subsequence_automaton",
        "input": "abcde\n2\nace\naec",
        "oracle_fn": lambda: "YES\nNO"
    },
    {
        "id": "STR-50",
        "category": "3O-I",
        "title": "Subsequence Automaton Full String Query",
        "text": "Query subsequence automaton whether exact string is a subsequence.",
        "expected_pattern": "string_subsequence_automaton",
        "input": "hello\n2\nhello\nhellos",
        "oracle_fn": lambda: "YES\nNO"
    },
    {
        "id": "STR-51",
        "category": "3O-I",
        "title": "Subsequence Automaton Repeated Characters",
        "text": "Answer subsequence queries on string with duplicates using next-occurrence automaton.",
        "expected_pattern": "string_subsequence_automaton",
        "input": "banana\n3\nbna\nbnn\nbnnn",
        "oracle_fn": lambda: "YES\nYES\nNO"
    },
    {
        "id": "STR-52",
        "category": "3O-I",
        "title": "Subsequence Automaton Single Character Queries",
        "text": "Test single character queries using subsequence automaton transition table.",
        "expected_pattern": "string_subsequence_automaton",
        "input": "chup\n3\nc\nu\nz",
        "oracle_fn": lambda: "YES\nYES\nNO"
    },
    {
        "id": "STR-53",
        "category": "3O-I",
        "title": "Subsequence Automaton Prefix and Suffix",
        "text": "Check prefix and suffix acceptance in subsequence automaton.",
        "expected_pattern": "string_subsequence_automaton",
        "input": "abcdefg\n2\nabc\nefg",
        "oracle_fn": lambda: "YES\nYES"
    },
    {
        "id": "STR-54",
        "category": "3O-I",
        "title": "Subsequence Automaton Out of Alphabet Characters",
        "text": "Query subsequence automaton with missing and out-of-alphabet characters.",
        "expected_pattern": "string_subsequence_automaton",
        "input": "codeforge\n2\ncdo\nxyz",
        "oracle_fn": lambda: "YES\nNO"
    },

    # ── 3O-J: SAM Longest Common Substring (STR-55..STR-60) ──
    {
        "id": "STR-55",
        "category": "3O-J",
        "title": "Basic SAM Longest Common Substring",
        "text": "Find longest common contiguous substring between two strings using Suffix Automaton SAM.",
        "expected_pattern": "string_longest_common_substring_sam",
        "input": "abacaba bacad",
        "oracle_fn": lambda: "4\nbaca"
    },
    {
        "id": "STR-56",
        "category": "3O-J",
        "title": "SAM LCS Identical Strings",
        "text": "Find longest common substring of two identical strings via Suffix Automaton.",
        "expected_pattern": "string_longest_common_substring_sam",
        "input": "banana banana",
        "oracle_fn": lambda: "6\nbanana"
    },
    {
        "id": "STR-57",
        "category": "3O-J",
        "title": "SAM LCS Disjoint Strings",
        "text": "Find longest common substring when strings share no common characters using SAM.",
        "expected_pattern": "string_longest_common_substring_sam",
        "input": "abc def",
        "oracle_fn": lambda: "0\n"
    },
    {
        "id": "STR-58",
        "category": "3O-J",
        "title": "SAM LCS Overlapping Prefix Suffix",
        "text": "Compute longest common substring of two overlapping strings using Suffix Automaton.",
        "expected_pattern": "string_longest_common_substring_sam",
        "input": "abcdefg defghij",
        "oracle_fn": lambda: "4\ndefg"
    },
    {
        "id": "STR-59",
        "category": "3O-J",
        "title": "SAM LCS Single Character Common",
        "text": "Locate longest common substring with single character match using SAM.",
        "expected_pattern": "string_longest_common_substring_sam",
        "input": "apple pear",
        "oracle_fn": lambda: "1\np"
    },
    {
        "id": "STR-60",
        "category": "3O-J",
        "title": "SAM LCS Repeated Substrings",
        "text": "Find longest common substring with repeated characters using Suffix Automaton.",
        "expected_pattern": "string_longest_common_substring_sam",
        "input": "mississippi swiss",
        "oracle_fn": lambda: "3\niss"
    },
]


def run_benchmark():
    total = len(BENCHMARK_PROBLEMS)
    passed = 0
    failed = 0

    print("=" * 80)
    print(f"CHUP Phase 3O — String Algorithms & Automata Benchmark ({total} Problems)")
    print("=" * 80)

    for p in BENCHMARK_PROBLEMS:
        pid = p["id"]
        cat = p["category"]
        title = p["title"]
        text = p["text"]
        expected_pat = p["expected_pattern"]
        stdin_data = p["input"]
        expected_output = p["oracle_fn"]()

        resp = handle_request({"problemText": text})
        selected_pat = resp.get("selectedPattern")
        family = resp.get("family")
        code = resp.get("code", "")

        if selected_pat != expected_pat:
            print(f"[{cat}] {pid} FAIL: Pattern mismatch: expected {expected_pat}, got {selected_pat} ({title})")
            failed += 1
            continue

        if family != "string":
            print(f"[{cat}] {pid} FAIL: Family mismatch: expected 'string', got {family} ({title})")
            failed += 1
            continue

        if not code:
            print(f"[{cat}] {pid} FAIL: No C++ code generated ({title})")
            failed += 1
            continue

        cpp_output = compile_and_run_cpp(code, stdin_data)

        if cpp_output.startswith("COMPILE_ERROR") or cpp_output.startswith("RUNTIME_ERROR"):
            print(f"[{cat}] {pid} FAIL: Execution error: {cpp_output} ({title})")
            failed += 1
            continue

        # Match check
        match = False
        if cat in ("3O-A", "3O-B", "3O-C", "3O-F", "3O-G", "3O-H", "3O-I"):
            match = (cpp_output.strip() == expected_output.strip())
        elif cat == "3O-D":
            # Manacher: line 1 is length, line 2 is substring
            exp_lines = expected_output.strip().splitlines()
            act_lines = cpp_output.strip().splitlines()
            if exp_lines and act_lines:
                exp_len = exp_lines[0].strip()
                act_len = act_lines[0].strip()
                match = (exp_len == act_len)
        elif cat == "3O-E":
            match = (cpp_output.strip() == expected_output.strip())
        elif cat == "3O-J":
            # SAM LCS: line 1 is length, line 2 is substring
            exp_lines = expected_output.strip().splitlines()
            act_lines = cpp_output.strip().splitlines()
            if exp_lines and act_lines:
                exp_len = exp_lines[0].strip()
                act_len = act_lines[0].strip()
                match = (exp_len == act_len)

        if match:
            passed += 1
            print(f"[{cat}] {pid} PASS: {title} (Pattern={expected_pat})")
        else:
            failed += 1
            print(f"[{cat}] {pid} FAIL: Output mismatch: expected '{expected_output}', got '{cpp_output}' ({title})")

    print("=" * 80)
    print(f"Benchmark Results: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("=" * 80)
    return passed == total


if __name__ == "__main__":
    success = run_benchmark()
    sys.exit(0 if success else 1)
