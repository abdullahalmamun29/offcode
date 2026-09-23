"""
CHUP Phase 3O — String Algorithms & Automata Adversarial Test Suite.

Contains 16 adversarial entrapment and extreme boundary test cases:
1. ADV-STR-01: "trie" narrative entrapment in KMP search
2. ADV-STR-02: "graph" state transition narrative in KMP search
3. ADV-STR-03: "tree" suffix narrative in Suffix Array
4. ADV-STR-04: "subsequence" narrative in SAM LCS
5. ADV-STR-05: "palindrome" mirror narrative in Duval minimal rotation
6. ADV-STR-06: "hash table" dictionary narrative in Aho-Corasick
7. ADV-STR-07: "dynamic programming" state transition narrative in Z-algorithm
8. ADV-STR-08: "bloom filter" probabilistic narrative in Rabin-Karp
9. ADV-STR-09: "two pointers" narrative in Manacher
10. ADV-STR-10: "dag" topological narrative in SAM distinct substrings
11. ADV-STR-11: Single character string boundary for KMP
12. ADV-STR-12: Single character string boundary for Z-algorithm
13. ADV-STR-13: Single character string boundary for Manacher
14. ADV-STR-14: Single character string boundary for Suffix Array
15. ADV-STR-15: Single character string boundary for Suffix Automaton
16. ADV-STR-16: Single character string boundary for Subsequence Automaton
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


ADVERSARIAL_CASES = [
    {
        "id": "ADV-STR-01",
        "title": "Trie narrative entrapment in KMP",
        "text": "A computer network routes packets through a trie-like prefix structure, but the core engine must find all occurrences of pattern in text using KMP prefix function pi table.",
        "expected_pattern": "string_kmp_search",
        "input": "abcdecdfabc abc",
        "expected_output": "0 8"
    },
    {
        "id": "ADV-STR-02",
        "title": "Graph state transition narrative in KMP",
        "text": "Model string matching as a state machine graph traversal to find pattern occurrences in text using Knuth-Morris-Pratt failure function.",
        "expected_pattern": "string_kmp_search",
        "input": "aaaaaa aaa",
        "expected_output": "0 1 2 3"
    },
    {
        "id": "ADV-STR-03",
        "title": "Tree suffix narrative in Suffix Array",
        "text": "Avoid heavy suffix tree memory overhead by building lexicographical suffix array and Kasai LCP array using prefix doubling.",
        "expected_pattern": "string_suffix_array",
        "input": "cba",
        "expected_output": "2 1 0\n0 0"
    },
    {
        "id": "ADV-STR-04",
        "title": "Subsequence narrative in SAM LCS",
        "text": "Even though biological sequences contain gap subsequences, we must find the longest common contiguous substring between two strings using Suffix Automaton SAM.",
        "expected_pattern": "string_longest_common_substring_sam",
        "input": "protein seq",
        "expected_output": "1\ne"
    },
    {
        "id": "ADV-STR-05",
        "title": "Palindrome mirror narrative in Duval rotation",
        "text": "Looking for symmetric palindrome-like shifts, find lexicographically minimal string rotation using Duval Lyndon factorization in O(N) time.",
        "expected_pattern": "string_lyndon_duval",
        "input": "cba",
        "expected_output": "acb"
    },
    {
        "id": "ADV-STR-06",
        "title": "Hash table narrative in Aho-Corasick",
        "text": "Rather than building isolated hash tables for each keyword, count occurrences of multiple dictionary patterns in text using Aho-Corasick automaton with failure links.",
        "expected_pattern": "string_aho_corasick",
        "input": "2\nin\nout\ninsideout",
        "expected_output": "1\n1"
    },
    {
        "id": "ADV-STR-07",
        "title": "DP state transition narrative in Z-algorithm",
        "text": "Replacing quadratic dynamic programming grid, compute Z-algorithm array of longest common prefix between suffix and entire string.",
        "expected_pattern": "string_z_algorithm",
        "input": "aba",
        "expected_output": "3 0 1"
    },
    {
        "id": "ADV-STR-08",
        "title": "Bloom filter narrative in Rabin-Karp",
        "text": "Using rolling hash instead of bloom filters, search pattern in text using Rabin-Karp polynomial rolling hash probabilistic matching.",
        "expected_pattern": "string_rabin_karp",
        "input": "bloomfilterfilter filter",
        "expected_output": "5 11"
    },
    {
        "id": "ADV-STR-09",
        "title": "Two pointers narrative in Manacher",
        "text": "Instead of naive two pointers center expansion, find longest palindromic substring in linear time using Manacher algorithm.",
        "expected_pattern": "string_manacher",
        "input": "racecar",
        "expected_output": "7\nracecar"
    },
    {
        "id": "ADV-STR-10",
        "title": "DAG topological narrative in SAM distinct substrings",
        "text": "Rather than traversing generic DAG states, count total number of distinct substrings in string using Suffix Automaton SAM.",
        "expected_pattern": "string_suffix_automaton",
        "input": "aba",
        "expected_output": "5"
    },
    {
        "id": "ADV-STR-11",
        "title": "Single character string boundary for KMP",
        "text": "Single character edge case: find all occurrences of a pattern in text using KMP prefix function pi table.",
        "expected_pattern": "string_kmp_search",
        "input": "a a",
        "expected_output": "0"
    },
    {
        "id": "ADV-STR-12",
        "title": "Single character string boundary for Z-algorithm",
        "text": "Single character edge case: compute Z-algorithm array of longest common prefix between suffix and entire string.",
        "expected_pattern": "string_z_algorithm",
        "input": "a",
        "expected_output": "1"
    },
    {
        "id": "ADV-STR-13",
        "title": "Single character string boundary for Manacher",
        "text": "Single character edge case: find longest palindromic substring in linear time using Manacher algorithm.",
        "expected_pattern": "string_manacher",
        "input": "a",
        "expected_output": "1\na"
    },
    {
        "id": "ADV-STR-14",
        "title": "Single character string boundary for Suffix Array",
        "text": "Single character edge case: construct suffix array and LCP array using prefix doubling and Kasai algorithm.",
        "expected_pattern": "string_suffix_array",
        "input": "a",
        "expected_output": "0\n"
    },
    {
        "id": "ADV-STR-15",
        "title": "Single character string boundary for Suffix Automaton",
        "text": "Single character edge case: count total number of distinct substrings in string using Suffix Automaton SAM.",
        "expected_pattern": "string_suffix_automaton",
        "input": "a",
        "expected_output": "1"
    },
    {
        "id": "ADV-STR-16",
        "title": "Single character string boundary for Subsequence Automaton",
        "text": "Single character edge case: process multiple subsequence existence queries on string using subsequence automaton transition table.",
        "expected_pattern": "string_subsequence_automaton",
        "input": "a\n2\na\nb",
        "expected_output": "YES\nNO"
    }
]


def run_adversarial_tests():
    total = len(ADVERSARIAL_CASES)
    passed = 0
    failed = 0

    print("=" * 80)
    print(f"CHUP Phase 3O — String Algorithms Adversarial Test Suite ({total} Cases)")
    print("=" * 80)

    for case in ADVERSARIAL_CASES:
        cid = case["id"]
        title = case["title"]
        text = case["text"]
        expected_pat = case["expected_pattern"]
        stdin_data = case["input"]
        expected_output = case["expected_output"]

        resp = handle_request({"problemText": text})
        selected_pat = resp.get("selectedPattern")
        family = resp.get("family")
        code = resp.get("code", "")

        if selected_pat != expected_pat:
            print(f"{cid} FAIL: Pattern mismatch: expected {expected_pat}, got {selected_pat} ({title})")
            failed += 1
            continue

        if family != "string":
            print(f"{cid} FAIL: Family mismatch: expected 'string', got {family} ({title})")
            failed += 1
            continue

        if not code:
            print(f"{cid} FAIL: No C++ code generated ({title})")
            failed += 1
            continue

        cpp_output = compile_and_run_cpp(code, stdin_data)

        if cpp_output.startswith("COMPILE_ERROR") or cpp_output.startswith("RUNTIME_ERROR"):
            print(f"{cid} FAIL: Execution error: {cpp_output} ({title})")
            failed += 1
            continue

        if expected_pat in ("string_manacher", "string_longest_common_substring_sam"):
            exp_lines = expected_output.strip().splitlines()
            act_lines = cpp_output.strip().splitlines()
            match = (exp_lines[0].strip() == act_lines[0].strip()) if exp_lines and act_lines else False
        else:
            match = (cpp_output.strip() == expected_output.strip())

        if match:
            passed += 1
            print(f"{cid} PASS: {title} (Pattern={expected_pat})")
        else:
            failed += 1
            print(f"{cid} FAIL: Output mismatch: expected '{expected_output}', got '{cpp_output}' ({title})")

    print("=" * 80)
    print(f"Adversarial Results: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("=" * 80)
    return passed == total


if __name__ == "__main__":
    success = run_adversarial_tests()
    sys.exit(0 if success else 1)
