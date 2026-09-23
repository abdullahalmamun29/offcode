"""
Trie Blind Holdout Evaluation — Phase 3D (BH-01 through BH-10)

10 held-out, unseen problem formulations testing generalized Trie reasoning:
- No problem statements or IDs are hardcoded in the solver
- All problems invoke handle_request({'problemText': ...})
- C++ code compiled and executed against independent oracles
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
    oracle_longest_common_prefix,
    oracle_max_xor_pair,
    oracle_max_xor_query,
    oracle_lexicographic_sort,
    oracle_autocomplete,
)

def compile_and_run_cpp(cpp_code: str, stdin_data: str, timeout: int = 5) -> str:
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


class TrieBlindHoldout:

    def run_all(self):
        tests = [
            ("BH-01", "Domain Vocabulary Prefix Lookup", self.test_bh01_vocab_prefix_lookup),
            ("BH-02", "Telephone Number Prefix Directory", self.test_bh02_telephone_prefix_directory),
            ("BH-03", "Interleaved Insertions and Deletions", self.test_bh03_interleaved_insert_delete),
            ("BH-04", "Max Bitwise XOR in Network Subnet Masks", self.test_bh04_max_xor_subnet_masks),
            ("BH-05", "Lexical Ordering of Log Keys", self.test_bh05_lexical_ordering_log_keys),
            ("BH-06", "Service Route Prefix Aggregation", self.test_bh06_service_route_prefix_aggregation),
            ("BH-07", "Query Completion with Query Stream", self.test_bh07_query_completion_stream),
            ("BH-08", "Bitwise Complement XOR Query", self.test_bh08_bitwise_complement_query),
            ("BH-09", "Shared Root with Divergent Branch Counting", self.test_bh09_divergent_branch_counts),
            ("BH-10", "Dense Multi-Word Lexicographical Sort", self.test_bh10_dense_lexicographical_sort),
        ]

        passed = 0
        failed = 0
        total_time = 0.0

        print("CHUP Phase 3D — Trie Blind Holdout (10 Problems)")
        print("=" * 70)

        for test_id, name, test_fn in tests:
            start = time.time()
            try:
                test_fn()
                elapsed = time.time() - start
                total_time += elapsed
                print(f"  ✓ {test_id} {name} ({elapsed:.2f}s)")
                passed += 1
            except Exception as e:
                elapsed = time.time() - start
                total_time += elapsed
                print(f"  ✗ {test_id} {name} — FAILED: {e}")
                failed += 1

        print("=" * 70)
        print(f"  Blind Holdout Results: {passed}/{len(tests)} passed ({passed/len(tests)*100:.0f}%)")
        print(f"  Total time: {total_time:.2f}s")
        print("=" * 70)
        return failed == 0

    def test_bh01_vocab_prefix_lookup(self):
        """Domain Vocabulary Prefix Lookup"""
        prob = "Construct a prefix tree dictionary to check if vocabulary terms start with a given query prefix."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"
        assert resp["family"] == "trie"

        words = ["quantum", "quarantine", "quasar"]
        commands = "\n".join([f"insert {w}" for w in words]) + "\nstartsWith qua\nstartsWith que\n"
        out = compile_and_run_cpp(resp["code"], commands)
        assert out.split() == ["true", "false"]

    def test_bh02_telephone_prefix_directory(self):
        """Telephone Number Prefix Directory"""
        prob = "Implement a phone directory prefix tree Trie for routing phone number strings."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"
        assert resp["family"] == "trie"

    def test_bh03_interleaved_insert_delete(self):
        """Interleaved Insertions and Deletions"""
        prob = "Implement a Trie supporting insert, search, and erase methods."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        commands = "insert alpha\ninsert beta\nerase alpha\nsearch alpha\nsearch beta\n"
        out = compile_and_run_cpp(resp["code"], commands)
        assert out.split() == ["true", "false", "true"]

    def test_bh04_max_xor_subnet_masks(self):
        """Max Bitwise XOR in Network Subnet Masks"""
        prob = "Given an array of 32-bit unsigned network identifiers, find the maximum bitwise XOR of two identifiers using a binary trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"
        assert resp["trie"]["kind"] == "binary_trie"

        nums = [192, 168, 1, 254, 10, 0]
        stdin = f"{len(nums)}\n{' '.join(map(str, nums))}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        assert int(out.strip()) == oracle_max_xor_pair(nums)

    def test_bh05_lexical_ordering_log_keys(self):
        """Lexical Ordering of Log Keys"""
        prob = "Sort strings in lexicographical order using a Trie traversal."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["error", "warn", "info", "debug", "trace"]
        stdin = f"{len(words)}\n{' '.join(words)}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        assert out.split() == oracle_lexicographic_sort(words)

    def test_bh06_service_route_prefix_aggregation(self):
        """Service Route Prefix Aggregation (Audited from mislabeled distinct substrings)"""
        prob = "Count microservice routing keys starting with a given service prefix using a Trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["microservice", "microarchitecture", "microwave"]
        commands = "\n".join([f"insert {w}" for w in words]) + "\ncountWordsStartingWith micro\n"
        out = compile_and_run_cpp(resp["code"], commands)
        expected = oracle_count_words_starting_with(words, "micro")
        assert int(out.strip()) == expected
        assert int(out.strip()) == 3

    def test_bh07_query_completion_stream(self):
        """Query Completion with Query Stream"""
        prob = "Implement an autocomplete system using a Trie to return suggestions with prefix."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["hyperlink", "hypertext", "hybrid", "hyper"]
        stdin = f"{len(words)}\n{' '.join(words)}\nhyper 3\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        assert out.split() == oracle_autocomplete(words, "hyper", 3)

    def test_bh08_bitwise_complement_query(self):
        """Bitwise Complement XOR Query"""
        prob = "Given an array of integers, for each query number find the maximum XOR with any element in the array using a binary trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"
        assert resp["trie"]["kind"] == "binary_trie"

        nums = [15, 30, 45, 60]
        q = 63
        stdin = f"{len(nums)} 1\n{' '.join(map(str, nums))}\n{q}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        assert int(out.strip()) == oracle_max_xor_query(nums, q)

    def test_bh09_divergent_branch_counts(self):
        """Shared Root with Divergent Branch Counting"""
        prob = "Implement a Trie supporting countWordsStartingWith prefix queries."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["algorithm", "algebra", "alchemy", "alien"]
        commands = "\n".join([f"insert {w}" for w in words]) + "\ncountWordsStartingWith al\ncountWordsStartingWith alg\n"
        out = compile_and_run_cpp(resp["code"], commands)
        assert [int(x) for x in out.split()] == [4, 2]

    def test_bh10_dense_lexicographical_sort(self):
        """Dense Multi-Word Lexicographical Sort"""
        prob = "Sort strings in lexicographical order using a Trie."
        resp = handle_request({"problemText": prob})
        assert resp["status"] == "success"

        words = ["zoom", "zone", "zero", "zebra", "zen"]
        stdin = f"{len(words)}\n{' '.join(words)}\n"
        out = compile_and_run_cpp(resp["code"], stdin)
        assert out.split() == oracle_lexicographic_sort(words)


if __name__ == "__main__":
    holdout = TrieBlindHoldout()
    success = holdout.run_all()
    sys.exit(0 if success else 1)
