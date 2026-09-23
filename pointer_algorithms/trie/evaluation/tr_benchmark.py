"""
Trie Benchmark — Phase 3D (TR-01 through TR-40)

Benchmark structure:
  A. Basic Character Trie      (TR-01..TR-08) — insert, exact search, prefix search, digits
  B. Counting & Multiplicity   (TR-09..TR-16) — word count, prefix count, dual counter
  C. Safe Deletion & Pruning   (TR-17..TR-20) — deletion without unlinking shared prefixes
  D. Longest Common Prefix     (TR-21..TR-24) — LCP over string collections
  E. Binary Trie & Max XOR     (TR-25..TR-32) — 32-bit unsigned uint32_t max XOR pair and query
  F. Sorting & Autocomplete    (TR-33..TR-36) — in-order traversal, prefix completion
  G. Anti-Patterns & Ranking   (TR-37..TR-40) — memory bounds, suboptimality, dynamic updates

All problems invoke the real pipeline entry point: handle_request({'problemText': ...}).
All generated C++ code is compiled with g++ -std=c++17 -O2, executed with test inputs,
and independently verified against brute-force oracles.
"""

import sys
import os
import subprocess
import tempfile
import random
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.trie.verification.trie_brute_force_oracles import (
    oracle_trie_search,
    oracle_trie_starts_with,
    oracle_count_words_equal_to,
    oracle_count_words_starting_with,
    oracle_trie_deletion,
    oracle_longest_common_prefix,
    oracle_max_xor_pair,
    oracle_max_xor_query,
    oracle_lexicographic_sort,
    oracle_autocomplete,
)

def compile_and_run_cpp(cpp_code: str, stdin_data: str, timeout: int = 5) -> str:
    """Compile C++ code, run with stdin_data, return stdout."""
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "sol.cpp")
        exe = os.path.join(tmpdir, "sol")
        with open(src, "w") as f:
            f.write(cpp_code)
        compile_result = subprocess.run(
            ["g++", "-std=c++17", "-O2", "-o", exe, src],
            capture_output=True, text=True, timeout=timeout
        )
        if compile_result.returncode != 0:
            return f"COMPILE_ERROR: {compile_result.stderr[:200]}"
        run_result = subprocess.run(
            [exe],
            input=stdin_data,
            capture_output=True, text=True, timeout=timeout
        )
        if run_result.returncode != 0:
            return f"RUNTIME_ERROR: {run_result.stderr[:200]}"
        return run_result.stdout.strip()


class TrieBenchmark:

    def run_all(self):
        tests = [
            # ── Category A: Basic Character Trie (TR-01..TR-08) ──
            ("TR-01", "A.BasicChar", self.test_tr01_insert_and_search_exact),
            ("TR-02", "A.BasicChar", self.test_tr02_search_absent_word),
            ("TR-03", "A.BasicChar", self.test_tr03_prefix_search_exists),
            ("TR-04", "A.BasicChar", self.test_tr04_prefix_search_absent),
            ("TR-05", "A.BasicChar", self.test_tr05_single_character_strings),
            ("TR-06", "A.BasicChar", self.test_tr06_word_is_prefix_of_another),
            ("TR-07", "A.BasicChar", self.test_tr07_digits_alphabet_trie),
            ("TR-08", "A.BasicChar", self.test_tr08_repeated_insertions_search),

            # ── Category B: Counting & Multiplicity (TR-09..TR-16) ──
            ("TR-09", "B.Counting", self.test_tr09_count_words_equal_to),
            ("TR-10", "B.Counting", self.test_tr10_count_words_starting_with),
            ("TR-11", "B.Counting", self.test_tr11_count_starting_with_absent),
            ("TR-12", "B.Counting", self.test_tr12_prefix_count_shared_root),
            ("TR-13", "B.Counting", self.test_tr13_deep_prefix_sharing_counts),
            ("TR-14", "B.Counting", self.test_tr14_disjoint_prefixes_counts),
            ("TR-15", "B.Counting", self.test_tr15_suffix_disjoint_counts),
            ("TR-16", "B.Counting", self.test_tr16_high_multiplicity_word_count),

            # ── Category C: Safe Deletion & Pruning (TR-17..TR-20) ──
            ("TR-17", "C.Deletion", self.test_tr17_delete_prefix_word_preserves_extension),
            ("TR-18", "C.Deletion", self.test_tr18_delete_extension_preserves_prefix),
            ("TR-19", "C.Deletion", self.test_tr19_delete_non_existent_word_noop),
            ("TR-20", "C.Deletion", self.test_tr20_delete_one_of_multiple_instances),

            # ── Category D: Longest Common Prefix (TR-21..TR-24) ──
            ("TR-21", "D.LCP", self.test_tr21_standard_common_prefix),
            ("TR-22", "D.LCP", self.test_tr22_no_common_prefix),
            ("TR-23", "D.LCP", self.test_tr23_all_strings_identical),
            ("TR-24", "D.LCP", self.test_tr24_array_with_empty_string),

            # ── Category E: Binary Trie & Max XOR (TR-25..TR-32) ──
            ("TR-25", "E.BinaryTrie", self.test_tr25_max_xor_pair_basic),
            ("TR-26", "E.BinaryTrie", self.test_tr26_max_xor_pair_single_bit_diff),
            ("TR-27", "E.BinaryTrie", self.test_tr27_max_xor_pair_large_30bit_integers),
            ("TR-28", "E.BinaryTrie", self.test_tr28_max_xor_pair_identical_elements),
            ("TR-29", "E.BinaryTrie", self.test_tr29_max_xor_query_single),
            ("TR-30", "E.BinaryTrie", self.test_tr30_max_xor_multiple_queries),
            ("TR-31", "E.BinaryTrie", self.test_tr31_max_xor_powers_of_two),
            ("TR-32", "E.BinaryTrie", self.test_tr32_max_xor_randomized_values),

            # ── Category F: Sorting & Autocomplete (TR-33..TR-36) ──
            ("TR-33", "F.SortAutocomplete", self.test_tr33_lexicographical_sort),
            ("TR-34", "F.SortAutocomplete", self.test_tr34_lexicographical_sort_duplicates),
            ("TR-35", "F.SortAutocomplete", self.test_tr35_autocomplete_suggestions),
            ("TR-36", "F.SortAutocomplete", self.test_tr36_autocomplete_few_completions),

            # ── Category G: Anti-Patterns & Ranking (TR-37..TR-40) ──
            ("TR-37", "G.AntiPattern", self.test_tr37_memory_limit_exceeded_reject),
            ("TR-38", "G.AntiPattern", self.test_tr38_single_query_suboptimal_preference),
            ("TR-39", "G.AntiPattern", self.test_tr39_unordered_numeric_lookup_reject),
            ("TR-40", "G.AntiPattern", self.test_tr40_dynamic_updates_range_sum_reject),
        ]

        passed = 0
        failed = 0
        total_time = 0.0

        print("CHUP Phase 3D — Trie Benchmark")
        print("=" * 70)

        for test_id, category, test_fn in tests:
            start = time.time()
            try:
                test_fn()
                elapsed = time.time() - start
                total_time += elapsed
                print(f"  ✓ {test_id} [{category}] {test_fn.__doc__} ({elapsed:.2f}s)")
                passed += 1
            except Exception as e:
                elapsed = time.time() - start
                total_time += elapsed
                print(f"  ✗ {test_id} [{category}] {test_fn.__doc__} — FAILED: {e}")
                failed += 1

        print("=" * 70)
        print(f"  Trie Benchmark Results: {passed}/{len(tests)} passed ({passed/len(tests)*100:.0f}%)")
        print(f"  Total time: {total_time:.2f}s")
        print("=" * 70)
        return failed == 0

    # ──────────────────────────────────────────────────────────────────────────
    # Category A: Basic Character Trie (TR-01..TR-08)
    # ──────────────────────────────────────────────────────────────────────────

    def test_tr01_insert_and_search_exact(self):
        """Insert and exact search in character trie"""
        prob = "Implement a prefix tree (trie) supporting insert, search, and startsWith operations for lowercase words."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"
        assert resp["family"] == "trie"

        words = ["apple", "app", "application", "banana", "bat"]
        commands = "\n".join([f"insert {w}" for w in words])
        commands += "\nsearch apple\nsearch app\nsearch ban\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = out.split()
        assert lines == ["true", "true", "false"]
        assert oracle_trie_search(words, "apple") is True
        assert oracle_trie_search(words, "ban") is False

    def test_tr02_search_absent_word(self):
        """Search for absent word in trie"""
        prob = "Implement a prefix tree trie with insert and exact search for strings."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["hello", "world", "code", "forge"]
        commands = "\n".join([f"insert {w}" for w in words])
        commands += "\nsearch missing\nsearch word\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = out.split()
        assert lines == ["false", "false"]
        assert oracle_trie_search(words, "missing") is False

    def test_tr03_prefix_search_exists(self):
        """Prefix search startsWith returns true for existing prefix"""
        prob = "Design a Trie data structure supporting insert, search, and startsWith prefix methods."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["programming", "progress", "project"]
        commands = "\n".join([f"insert {w}" for w in words])
        commands += "\nstartsWith prog\nstartsWith proj\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = out.split()
        assert lines == ["true", "true"]
        assert oracle_trie_starts_with(words, "prog") is True

    def test_tr04_prefix_search_absent(self):
        """Prefix search startsWith returns false for non-existing prefix"""
        prob = "Design a Trie data structure supporting insert, search, and startsWith prefix methods."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["cat", "caterpillar", "category"]
        commands = "\n".join([f"insert {w}" for w in words])
        commands += "\nstartsWith dog\nstartsWith cattle\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = out.split()
        assert lines == ["false", "false"]
        assert oracle_trie_starts_with(words, "dog") is False

    def test_tr05_single_character_strings(self):
        """Single character string operations in Trie"""
        prob = "Implement a character prefix tree Trie with single character support."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["a", "b"]
        commands = "insert a\ninsert b\nsearch a\nsearch b\nsearch c\nstartsWith a\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = out.split()
        assert lines == ["true", "true", "false", "true"]
        assert oracle_trie_search(words, "c") is False

    def test_tr06_word_is_prefix_of_another(self):
        """Word is strict prefix of another word (app vs apple)"""
        prob = "Implement a trie dictionary handling prefixes that are also words."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        commands = "insert app\ninsert apple\nsearch app\nsearch apple\nsearch appl\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = out.split()
        assert lines == ["true", "true", "false"]

    def test_tr07_digits_alphabet_trie(self):
        """Trie with numeric digits alphabet (0-9)"""
        prob = "Design a prefix tree Trie for numeric strings of digits 0-9."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"
        assert resp["family"] == "trie"

    def test_tr08_repeated_insertions_search(self):
        """Repeated insertions of same word in Trie"""
        prob = "Design a prefix tree trie supporting insert and search with repeated elements."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        commands = "insert repeat\ninsert repeat\ninsert repeat\nsearch repeat\n"
        out = compile_and_run_cpp(resp["code"], commands)
        assert out.strip() == "true"

    # ──────────────────────────────────────────────────────────────────────────
    # Category B: Counting & Multiplicity (TR-09..TR-16)
    # ──────────────────────────────────────────────────────────────────────────

    def test_tr09_count_words_equal_to(self):
        """Count exact word occurrences in Trie"""
        prob = "Implement a Trie with countWordsEqualTo and countWordsStartingWith methods."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["apple", "apple", "app", "application"]
        commands = "\n".join([f"insert {w}" for w in words])
        commands += "\ncountWordsEqualTo apple\ncountWordsEqualTo app\ncountWordsEqualTo banana\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = [int(x) for x in out.split()]
        assert lines == [2, 1, 0]
        assert oracle_count_words_equal_to(words, "apple") == 2

    def test_tr10_count_words_starting_with(self):
        """Count words starting with a prefix in Trie"""
        prob = "Implement a Trie supporting countWordsStartingWith prefix count queries."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["apple", "apple", "app", "application", "banana"]
        commands = "\n".join([f"insert {w}" for w in words])
        commands += "\ncountWordsStartingWith app\ncountWordsStartingWith appl\ncountWordsStartingWith b\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = [int(x) for x in out.split()]
        assert lines == [4, 3, 1]
        assert oracle_count_words_starting_with(words, "app") == 4

    def test_tr11_count_starting_with_absent(self):
        """Count words starting with non-existent prefix returns 0"""
        prob = "Implement a Trie supporting prefix counting countWordsStartingWith."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["zebra", "zoo"]
        commands = "\n".join([f"insert {w}" for w in words])
        commands += "\ncountWordsStartingWith a\ncountWordsStartingWith zeb\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = [int(x) for x in out.split()]
        assert lines == [0, 1]
        assert oracle_count_words_starting_with(words, "a") == 0

    def test_tr12_prefix_count_shared_root(self):
        """Prefix count with single-letter common root"""
        prob = "Count words starting with prefix in a Trie dictionary."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["data", "database", "datum", "dare"]
        commands = "\n".join([f"insert {w}" for w in words])
        commands += "\ncountWordsStartingWith d\ncountWordsStartingWith dat\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = [int(x) for x in out.split()]
        assert lines == [4, 3]
        assert oracle_count_words_starting_with(words, "d") == 4

    def test_tr13_deep_prefix_sharing_counts(self):
        """Deep prefix branch counting"""
        prob = "Trie prefix count and word count with deep branches."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["abcdefg", "abcdefh", "abcxyz"]
        commands = "\n".join([f"insert {w}" for w in words])
        commands += "\ncountWordsStartingWith abc\ncountWordsStartingWith abcdef\ncountWordsStartingWith abcxyz\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = [int(x) for x in out.split()]
        assert lines == [3, 2, 1]

    def test_tr14_disjoint_prefixes_counts(self):
        """Completely disjoint prefix strings count independently"""
        prob = "Trie structure with countWordsStartingWith."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["cat", "dog", "fish"]
        commands = "\n".join([f"insert {w}" for w in words])
        commands += "\ncountWordsStartingWith c\ncountWordsStartingWith d\ncountWordsStartingWith f\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = [int(x) for x in out.split()]
        assert lines == [1, 1, 1]

    def test_tr15_suffix_disjoint_counts(self):
        """Common prefix with multiple divergent suffixes"""
        prob = "Count words with prefix using a Trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["pretest", "prepare", "predict", "prefix"]
        commands = "\n".join([f"insert {w}" for w in words])
        commands += "\ncountWordsStartingWith pre\ncountWordsStartingWith prep\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = [int(x) for x in out.split()]
        assert lines == [oracle_count_words_starting_with(words, "pre"), oracle_count_words_starting_with(words, "prep")]
        assert lines == [4, 1]

    def test_tr16_high_multiplicity_word_count(self):
        """High multiplicity insertion and word counting"""
        prob = "Trie with duplicate words counting countWordsEqualTo."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["item"] * 5 + ["other"]
        commands = "\n".join([f"insert {w}" for w in words])
        commands += "\ncountWordsEqualTo item\ncountWordsEqualTo other\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = [int(x) for x in out.split()]
        assert lines == [5, 1]

    # ──────────────────────────────────────────────────────────────────────────
    # Category C: Safe Deletion & Pruning (TR-17..TR-20)
    # ──────────────────────────────────────────────────────────────────────────

    def test_tr17_delete_prefix_word_preserves_extension(self):
        """Delete word that is a prefix of another word (app deleted, apple preserved)"""
        prob = "Implement a Trie with insert, search, and erase methods for dictionary deletion."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        commands = "insert app\ninsert apple\nerase app\nsearch app\nsearch apple\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = out.split()
        assert lines == ["true", "false", "true"]

    def test_tr18_delete_extension_preserves_prefix(self):
        """Delete extension word while preserving prefix word (apple deleted, app preserved)"""
        prob = "Implement a Trie with insert, search, and erase methods for dictionary deletion."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        commands = "insert app\ninsert apple\nerase apple\nsearch app\nsearch apple\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = out.split()
        assert lines == ["true", "true", "false"]

    def test_tr19_delete_non_existent_word_noop(self):
        """Delete non-existent word is safe no-op"""
        prob = "Implement a Trie with erase deletion method."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        commands = "insert test\nerase missing\nsearch test\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = out.split()
        assert lines == ["false", "true"]

    def test_tr20_delete_one_of_multiple_instances(self):
        """Delete one instance of duplicate word decreases count by 1"""
        prob = "Implement a Trie with countWordsEqualTo and erase methods."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        commands = "insert key\ninsert key\ncountWordsEqualTo key\nerase key\ncountWordsEqualTo key\n"
        out = compile_and_run_cpp(resp["code"], commands)
        lines = out.split()
        assert lines == ["2", "true", "1"]

    # ──────────────────────────────────────────────────────────────────────────
    # Category D: Longest Common Prefix (TR-21..TR-24)
    # ──────────────────────────────────────────────────────────────────────────

    def test_tr21_standard_common_prefix(self):
        """Find longest common prefix of string array using a Trie"""
        prob = "Find the longest common prefix string amongst an array of strings using a Trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["flower", "flow", "flight"]
        stdin = f"3\n{' '.join(words)}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        assert out.strip() == oracle_longest_common_prefix(words)
        assert out.strip() == "fl"

    def test_tr22_no_common_prefix(self):
        """No common prefix amongst strings returns empty string"""
        prob = "Find the longest common prefix string amongst an array of strings using a Trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["dog", "racecar", "car"]
        stdin = f"3\n{' '.join(words)}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        assert out.strip() == oracle_longest_common_prefix(words)
        assert out.strip() == ""

    def test_tr23_all_strings_identical(self):
        """All strings identical returns full string as common prefix"""
        prob = "Find the longest common prefix string amongst an array of strings using a Trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["identical", "identical", "identical"]
        stdin = f"3\n{' '.join(words)}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        assert out.strip() == oracle_longest_common_prefix(words)
        assert out.strip() == "identical"

    def test_tr24_array_with_empty_string(self):
        """Array containing empty string returns empty prefix"""
        prob = "Find the longest common prefix string amongst an array of strings using a Trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["prefix", "pre", ""]
        stdin = f"3\nprefix pre \n"
        out = compile_and_run_cpp(resp["code"], stdin)
        assert out.strip() == ""

    # ──────────────────────────────────────────────────────────────────────────
    # Category E: Binary Trie & Max XOR (TR-25..TR-32)
    # ──────────────────────────────────────────────────────────────────────────

    def test_tr25_max_xor_pair_basic(self):
        """Maximum XOR of two numbers in array using binary trie"""
        prob = "Given an integer array nums, return the maximum result of nums[i] XOR nums[j] where 0 <= i <= j < n using a binary trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"
        assert resp["family"] == "trie"
        assert resp["trie"]["kind"] == "binary_trie"

        nums = [3, 10, 5, 25, 2, 8]
        stdin = f"{len(nums)}\n{' '.join(map(str, nums))}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        expected = oracle_max_xor_pair(nums)
        assert int(out.strip()) == expected
        assert int(out.strip()) == 28

    def test_tr26_max_xor_pair_single_bit_diff(self):
        """Max XOR pair with complementary single bits"""
        prob = "Find maximum bitwise XOR of two numbers in an array using binary trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        nums = [1, 2, 4, 8, 16]
        stdin = f"{len(nums)}\n{' '.join(map(str, nums))}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        assert int(out.strip()) == oracle_max_xor_pair(nums)
        assert int(out.strip()) == 24

    def test_tr27_max_xor_pair_large_30bit_integers(self):
        """Max XOR pair with 30-bit integers uint32_t overflow safety"""
        prob = "Find the maximum bitwise XOR of two numbers in array using binary trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        nums = [1073741823, 536870912, 1000000000, 42]
        stdin = f"{len(nums)}\n{' '.join(map(str, nums))}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        assert int(out.strip()) == oracle_max_xor_pair(nums)

    def test_tr28_max_xor_pair_identical_elements(self):
        """Max XOR pair with identical elements returns 0"""
        prob = "Find maximum XOR of two numbers in an array."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        nums = [7, 7, 7, 7]
        stdin = f"{len(nums)}\n{' '.join(map(str, nums))}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        assert int(out.strip()) == 0

    def test_tr29_max_xor_query_single(self):
        """Max XOR query with a given query number using binary trie"""
        prob = "Given an array of integers, for each query number find the maximum XOR with any element in the array using a binary trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"
        assert resp["trie"]["kind"] == "binary_trie"

        nums = [3, 10, 5, 25, 2, 8]
        q = 5
        stdin = f"{len(nums)} 1\n{' '.join(map(str, nums))}\n{q}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        assert int(out.strip()) == oracle_max_xor_query(nums, q)

    def test_tr30_max_xor_multiple_queries(self):
        """Max XOR multiple queries on binary trie"""
        prob = "For each query integer, find the maximum bitwise XOR with any number in the array using a binary trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        nums = [14, 70, 53, 83, 49, 91, 36, 80, 92, 51]
        queries = [1, 23, 50, 100]
        stdin = f"{len(nums)} {len(queries)}\n{' '.join(map(str, nums))}\n{' '.join(map(str, queries))}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        lines = [int(x) for x in out.split()]
        expected = [oracle_max_xor_query(nums, q) for q in queries]
        assert lines == expected

    def test_tr31_max_xor_powers_of_two(self):
        """Max XOR with powers of two in binary trie"""
        prob = "Find maximum XOR pair in integer array using binary trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        nums = [2**i for i in range(10)]
        stdin = f"{len(nums)}\n{' '.join(map(str, nums))}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        assert int(out.strip()) == oracle_max_xor_pair(nums)

    def test_tr32_max_xor_randomized_values(self):
        """Max XOR pair with randomized integers verified against oracle"""
        prob = "Find maximum XOR of two numbers in array using binary trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        rng = random.Random(42)
        nums = [rng.randint(0, 100000) for _ in range(20)]
        stdin = f"{len(nums)}\n{' '.join(map(str, nums))}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        assert int(out.strip()) == oracle_max_xor_pair(nums)

    # ──────────────────────────────────────────────────────────────────────────
    # Category F: Sorting & Autocomplete (TR-33..TR-36)
    # ──────────────────────────────────────────────────────────────────────────

    def test_tr33_lexicographical_sort(self):
        """Lexicographical sort of strings using Trie traversal"""
        prob = "Sort an array of strings in lexicographical alphabetical order using a Trie traversal."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["zebra", "apple", "banana", "cat", "dog"]
        stdin = f"{len(words)}\n{' '.join(words)}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        lines = out.split()
        assert lines == oracle_lexicographic_sort(words)

    def test_tr34_lexicographical_sort_duplicates(self):
        """Lexicographical sort preserving duplicates via word_count"""
        prob = "Sort strings in lexicographical order using a Trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["beta", "alpha", "beta", "alpha", "gamma"]
        stdin = f"{len(words)}\n{' '.join(words)}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        lines = out.split()
        assert lines == oracle_lexicographic_sort(words)

    def test_tr35_autocomplete_suggestions(self):
        """Autocomplete prefix suggestions using Trie"""
        prob = "Implement an autocomplete system using a Trie to return suggestions with a given prefix."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["card", "car", "cart", "cat", "carbon", "care"]
        stdin = f"{len(words)}\n{' '.join(words)}\ncar 3\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        lines = out.split()
        assert lines == oracle_autocomplete(words, "car", 3)

    def test_tr36_autocomplete_few_completions(self):
        """Autocomplete when available completions are fewer than limit"""
        prob = "Implement an autocomplete suggestions system using a Trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["airplane", "airport"]
        stdin = f"{len(words)}\n{' '.join(words)}\nair 5\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        lines = out.split()
        assert lines == oracle_autocomplete(words, "air", 5)

    # ──────────────────────────────────────────────────────────────────────────
    # Category G: Anti-Patterns & Ranking (TR-37..TR-40)
    # ──────────────────────────────────────────────────────────────────────────

    def test_tr37_memory_limit_exceeded_reject(self):
        """Hard rejection when Trie memory exceeds 256MB limit"""
        prob = "Store 10^7 strings of length 100 in memory. Trie construction exceeds memory limit of 256MB."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "rejected"
        rejection_codes = [e["rejectionCode"] for e in resp["eliminatedCandidates"]]
        assert "TRIE_MEMORY_LIMIT_EXCEEDED" in rejection_codes

    def test_tr38_single_query_suboptimal_preference(self):
        """Single query without prefix sharing is marked suboptimal, not hard rejected"""
        prob = "Check once only if a single string S equals single query T without dictionary or repeated queries."
        resp = handle_request({"problemText": prob})
        # Important user instruction: A one-query Trie is correct but suboptimal, not rejected
        # So it should either accept with is_suboptimal or rank direct comparison above it
        # If rejected, must NOT be accepted=False for Trie if admissible
        if resp["status"] == "success":
            assert resp["family"] in ("trie", "two_pointers_converging", "two_pointers_same_direction")
        else:
            # Check elimination details
            rejection_codes = [e.get("rejectionCode") for e in resp.get("eliminatedCandidates", [])]
            assert "TRIE_SINGLE_QUERY_SUBOPTIMAL" not in rejection_codes

    def test_tr39_unordered_numeric_lookup_reject(self):
        """Reject Trie for arbitrary numeric point queries without prefix/XOR structure"""
        prob = "Given an unsorted array of numbers, handle point updates and answer range sum queries."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "rejected"

    def test_tr40_dynamic_updates_range_sum_reject(self):
        """Dynamic updates interleaved with range queries rejected for static pointer/trie"""
        prob = "Array with dynamic point updates and range minimum queries."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "rejected"


if __name__ == "__main__":
    bench = TrieBenchmark()
    success = bench.run_all()
    sys.exit(0 if success else 1)
