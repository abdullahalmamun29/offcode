"""
CHUP Phase 3O — String Algorithms & Automata Randomized Stress Test Suite.

Differential randomized stress testing comparing compiled C++ implementations
against independent reference oracles across 220 randomized test instances:
1. string_kmp_search vs KMP Oracle (22 runs)
2. string_z_algorithm vs Z-Array Oracle (22 runs)
3. string_rabin_karp vs Rabin-Karp Oracle (22 runs)
4. string_manacher vs Manacher Palindrome Oracle (22 runs)
5. string_aho_corasick vs Aho-Corasick Multi-Pattern Oracle (22 runs)
6. string_suffix_array vs Suffix Array & Kasai LCP Oracle (22 runs)
7. string_suffix_automaton vs SAM Distinct Substrings Oracle (22 runs)
8. string_lyndon_duval vs Duval Minimal Rotation Oracle (22 runs)
9. string_subsequence_automaton vs Subsequence Automaton Oracle (22 runs)
10. string_longest_common_substring_sam vs SAM LCS Oracle (22 runs)

Total: 220 test cases.
"""

import sys
import os
import random
import string
import subprocess
import tempfile
import hashlib
from typing import Dict, Any, List, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.generator.string_cpp_generator import generate_string_cpp
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


def compile_and_run(pattern: str, stdin_data: str, timeout: int = 10) -> str:
    code = generate_string_cpp(pattern, {})
    code_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()
    exe = COMPILED_BINARIES.get(code_hash)
    if not exe or not os.path.exists(exe):
        tmp_cpp = tempfile.NamedTemporaryFile(suffix=".cpp", delete=False)
        tmp_cpp.write(code.encode("utf-8"))
        tmp_cpp.close()
        exe = tmp_cpp.name[:-4]
        res = subprocess.run(["g++", "-std=c++17", "-O2", tmp_cpp.name, "-o", exe], capture_output=True, text=True)
        if res.returncode != 0:
            return f"COMPILE_ERROR: {res.stderr[:200]}"
        COMPILED_BINARIES[code_hash] = exe
    try:
        run_res = subprocess.run([exe], input=stdin_data, capture_output=True, text=True, timeout=timeout)
        if run_res.returncode != 0:
            return f"RUNTIME_ERROR: {run_res.stderr[:200]}"
        return run_res.stdout.strip()
    except subprocess.TimeoutExpired:
        return "RUNTIME_ERROR: TimeoutExpired"


def random_string(length: int, alphabet: str = "abcde") -> str:
    return "".join(random.choice(alphabet) for _ in range(length))


def run_stress_tests():
    random.seed(42)
    total_passed = 0
    total_tests = 220
    test_idx = 0

    print("=" * 80)
    print("CHUP Phase 3O — String Algorithms Randomized Stress Tests (220 Cases)")
    print("=" * 80)

    # ── 1. KMP Search (22 runs) ──
    for i in range(22):
        test_idx += 1
        n = random.randint(10, 80)
        m = random.randint(1, min(10, n))
        alpha = random.choice(["ab", "abc", "abcd"])
        text = random_string(n, alpha)
        # 50% chance pattern is an actual substring of text
        if random.random() < 0.5:
            start = random.randint(0, n - m)
            pattern = text[start:start + m]
        else:
            pattern = random_string(m, alpha)

        expected_matches = string_kmp_oracle(text, pattern)
        expected_str = " ".join(map(str, expected_matches))

        out = compile_and_run("string_kmp_search", f"{text} {pattern}")
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: KMP run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 2. Z-Algorithm (22 runs) ──
    for i in range(22):
        test_idx += 1
        n = random.randint(5, 60)
        alpha = random.choice(["a", "ab", "abc", "abcdef"])
        s = random_string(n, alpha)

        expected_z = string_z_algorithm_oracle(s)
        expected_str = " ".join(map(str, expected_z))

        out = compile_and_run("string_z_algorithm", s)
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: Z-algorithm run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 3. Rabin-Karp (22 runs) ──
    for i in range(22):
        test_idx += 1
        n = random.randint(10, 80)
        m = random.randint(1, min(8, n))
        alpha = random.choice(["ab", "abc"])
        text = random_string(n, alpha)
        if random.random() < 0.5:
            start = random.randint(0, n - m)
            pattern = text[start:start + m]
        else:
            pattern = random_string(m, alpha)

        expected_matches = string_rabin_karp_oracle(text, pattern)
        expected_str = " ".join(map(str, expected_matches))

        out = compile_and_run("string_rabin_karp", f"{text} {pattern}")
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: Rabin-Karp run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 4. Manacher Longest Palindrome (22 runs) ──
    for i in range(22):
        test_idx += 1
        n = random.randint(5, 50)
        alpha = random.choice(["ab", "abc", "abcdef"])
        s = random_string(n, alpha)

        expected_len, expected_sub = string_manacher_oracle(s)

        out = compile_and_run("string_manacher", s)
        lines = out.splitlines()
        if len(lines) >= 2:
            act_len = int(lines[0].strip())
            act_sub = lines[1].strip()
            # Verified: length matches oracle, act_sub is a valid palindrome of that length in s
            if act_len == expected_len and act_sub == act_sub[::-1] and len(act_sub) == act_len and act_sub in s:
                total_passed += 1
            else:
                print(f"[{test_idx}] FAIL: Manacher run {i+1}: len={act_len} (exp {expected_len})")
        else:
            print(f"[{test_idx}] FAIL: Manacher output format: '{out}'")

    # ── 5. Aho-Corasick Multi-Pattern (22 runs) ──
    for i in range(22):
        test_idx += 1
        k = random.randint(2, 6)
        alpha = random.choice(["ab", "abc"])
        text = random_string(random.randint(15, 60), alpha)
        patterns = [random_string(random.randint(1, 5), alpha) for _ in range(k)]

        stdin_data = f"{k}\n" + "\n".join(patterns) + f"\n{text}"
        expected_counts = [len(string_kmp_oracle(text, p)) for p in patterns]
        expected_str = "\n".join(map(str, expected_counts))

        out = compile_and_run("string_aho_corasick", stdin_data)
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: Aho-Corasick run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 6. Suffix Array & Kasai LCP (22 runs) ──
    for i in range(22):
        test_idx += 1
        n = random.randint(2, 35)
        alpha = random.choice(["ab", "abc", "abcdef"])
        s = random_string(n, alpha)

        sa, lcp = string_suffix_array_lcp_oracle(s)
        expected_sa = " ".join(map(str, sa))
        expected_lcp = " ".join(map(str, lcp))

        out = compile_and_run("string_suffix_array", s)
        lines = out.splitlines()
        if len(lines) >= 2 and lines[0].strip() == expected_sa and lines[1].strip() == expected_lcp:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: Suffix Array run {i+1}: expected SA='{expected_sa}', got '{lines[0] if lines else ''}'")

    # ── 7. Suffix Automaton Distinct Substrings (22 runs) ──
    for i in range(22):
        test_idx += 1
        n = random.randint(3, 25)
        alpha = random.choice(["a", "ab", "abc"])
        s = random_string(n, alpha)

        expected_count = string_sam_distinct_substrings_oracle(s)

        out = compile_and_run("string_suffix_automaton", s)
        if out == str(expected_count):
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: SAM Distinct run {i+1}: expected {expected_count}, got {out} for '{s}'")

    # ── 8. Duval Minimal String Rotation (22 runs) ──
    for i in range(22):
        test_idx += 1
        n = random.randint(2, 40)
        alpha = random.choice(["ab", "abc", "abcdef"])
        s = random_string(n, alpha)

        min_rot = min(s[j:] + s[:j] for j in range(n))

        out = compile_and_run("string_lyndon_duval", s)
        if out == min_rot:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: Duval run {i+1}: expected '{min_rot}', got '{out}' for '{s}'")

    # ── 9. Subsequence Automaton (22 runs) ──
    for i in range(22):
        test_idx += 1
        n = random.randint(10, 40)
        q_count = random.randint(2, 5)
        alpha = random.choice(["ab", "abc"])
        s = random_string(n, alpha)
        queries = [random_string(random.randint(1, 8), alpha) for _ in range(q_count)]

        stdin_data = f"{s}\n{q_count}\n" + "\n".join(queries)
        answers = string_subsequence_automaton_oracle(s, queries)
        expected_str = "\n".join("YES" if ok else "NO" for ok in answers)

        out = compile_and_run("string_subsequence_automaton", stdin_data)
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: Subseq Automaton run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 10. SAM Longest Common Substring (22 runs) ──
    for i in range(22):
        test_idx += 1
        n1 = random.randint(5, 30)
        n2 = random.randint(5, 30)
        alpha = random.choice(["ab", "abc"])
        s1 = random_string(n1, alpha)
        s2 = random_string(n2, alpha)

        expected_lcs = string_lcs_sam_oracle(s1, s2)
        expected_len = len(expected_lcs)

        out = compile_and_run("string_longest_common_substring_sam", f"{s1} {s2}")
        lines = out.splitlines()
        if len(lines) >= 2:
            act_len = int(lines[0].strip())
            act_sub = lines[1].strip()
            if act_len == expected_len and (expected_len == 0 or (act_sub in s1 and act_sub in s2 and len(act_sub) == expected_len)):
                total_passed += 1
            else:
                print(f"[{test_idx}] FAIL: SAM LCS run {i+1}: expected len {expected_len}, got {act_len}")
        elif expected_len == 0 and len(lines) == 1 and int(lines[0].strip()) == 0:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: SAM LCS run {i+1}: format error '{out}'")

    print("=" * 80)
    print(f"Stress Test Results: {total_passed}/{total_tests} Passed ({(total_passed/total_tests)*100:.1f}%)")
    print("=" * 80)
    return total_passed == total_tests


if __name__ == "__main__":
    success = run_stress_tests()
    sys.exit(0 if success else 1)
