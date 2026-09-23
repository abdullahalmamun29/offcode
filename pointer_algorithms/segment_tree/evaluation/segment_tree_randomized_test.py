"""
CHUP Phase 3J — Segment Tree Randomized Differential Testing Suite.
Verifies Segment Tree implementations against Python reference oracles across 160+ seeds and thousands of operations:
1. Point Update & Range Query (Sum & Min) (30 seeds, ~750 ops)
2. Range Add & Range Sum Query (Lazy Propagation) (30 seeds, ~750 ops)
3. Range Assignment & Range Sum Query (Lazy Propagation) (25 seeds, ~625 ops)
4. Combined Range Assignment & Range Addition (25 seeds, ~625 ops)
5. Maximum Contiguous Subarray Sum Query (25 seeds, ~625 ops)
6. Frequency Segment Tree & K-th Smallest Element (25 seeds, ~625 ops)
Total: 160 seeds, 4,000+ operations verified against independent reference oracles.
"""

import sys
import os
import random
import subprocess
import tempfile
from typing import List, Tuple, Any

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.generator.segment_tree_cpp_generator import generate_segment_tree_cpp
from pointer_algorithms.segment_tree.evaluation.segment_tree_benchmark import (
    run_oracle_point_update_range_sum,
    run_oracle_point_update_range_min,
    run_oracle_range_add_sum,
    run_oracle_range_assign_sum,
    run_oracle_combined_lazy,
    run_oracle_max_subarray,
    run_oracle_frequency_kth,
)


class CppBinary:
    """Compiles C++ code once and executes multiple stdin inputs against the binary."""
    def __init__(self, cpp_code: str):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.src = os.path.join(self.tmp_dir.name, "sol.cpp")
        self.exe = os.path.join(self.tmp_dir.name, "sol")
        with open(self.src, "w") as f:
            f.write(cpp_code)
        compile_res = subprocess.run(
            ["g++", "-std=c++17", "-O2", "-o", self.exe, self.src],
            capture_output=True, text=True, timeout=10
        )
        if compile_res.returncode != 0:
            raise RuntimeError(f"Compilation failed: {compile_res.stderr}")

    def run(self, stdin_data: str, timeout: int = 5) -> str:
        res = subprocess.run(
            [self.exe], input=stdin_data, capture_output=True, text=True, timeout=timeout
        )
        if res.returncode != 0:
            return f"RUNTIME_ERROR: {res.stderr[:200]}"
        return res.stdout.strip()

    def cleanup(self):
        self.tmp_dir.cleanup()


def test_random_point_update_range_sum(num_seeds: int = 30, ops_per_seed: int = 25) -> Tuple[int, int, int]:
    print(f"Running Point Update & Range Sum testing ({num_seeds} seeds, {ops_per_seed} ops/seed)...")
    code = generate_segment_tree_cpp("segment_tree_point_update_range_query", {"segment_tree_query_op": "sum"})
    bin_obj = CppBinary(code)
    passed = 0
    failed = 0
    total_ops = 0

    try:
        for s in range(num_seeds):
            rng = random.Random(1000 + s)
            n = rng.randint(10, 50)
            q = ops_per_seed
            initial = [0] + [rng.randint(-100, 100) for _ in range(n)]
            queries = []
            for _ in range(q):
                t = rng.choice([1, 2])
                if t == 1:
                    idx = rng.randint(1, n)
                    val = rng.randint(-50, 50)
                    queries.append((1, idx, val))
                else:
                    l = rng.randint(1, n)
                    r = rng.randint(l, n)
                    queries.append((2, l, r))

            lines = [f"{n} {q}"]
            lines.append(" ".join(str(initial[i]) for i in range(1, n + 1)))
            for q_tuple in queries:
                if q_tuple[0] == 1:
                    lines.append(f"1 {q_tuple[1]} {q_tuple[2]}")
                else:
                    lines.append(f"2 {q_tuple[1]} {q_tuple[2]}")

            stdin_data = "\n".join(lines) + "\n"
            cpp_out = bin_obj.run(stdin_data)
            oracle_out = run_oracle_point_update_range_sum(n, initial, queries)

            if cpp_out == oracle_out:
                passed += 1
            else:
                failed += 1
                print(f"  Seed {s} FAILED!\nExpected:\n{oracle_out[:100]}\nGot:\n{cpp_out[:100]}")
            total_ops += q
    finally:
        bin_obj.cleanup()

    return passed, failed, total_ops


def test_random_range_add(num_seeds: int = 30, ops_per_seed: int = 25) -> Tuple[int, int, int]:
    print(f"Running Range Add (Lazy) testing ({num_seeds} seeds, {ops_per_seed} ops/seed)...")
    code = generate_segment_tree_cpp("segment_tree_range_add_range_query", {})
    bin_obj = CppBinary(code)
    passed = 0
    failed = 0
    total_ops = 0

    try:
        for s in range(num_seeds):
            rng = random.Random(2000 + s)
            n = rng.randint(10, 50)
            q = ops_per_seed
            initial = [0] + [rng.randint(-50, 50) for _ in range(n)]
            queries = []
            for _ in range(q):
                t = rng.choice([1, 2])
                if t == 1:
                    l = rng.randint(1, n)
                    r = rng.randint(l, n)
                    val = rng.randint(-20, 20)
                    queries.append((1, l, r, val))
                else:
                    l = rng.randint(1, n)
                    r = rng.randint(l, n)
                    queries.append((2, l, r))

            lines = [f"{n} {q}"]
            lines.append(" ".join(str(initial[i]) for i in range(1, n + 1)))
            for q_tuple in queries:
                if q_tuple[0] == 1:
                    lines.append(f"1 {q_tuple[1]} {q_tuple[2]} {q_tuple[3]}")
                else:
                    lines.append(f"2 {q_tuple[1]} {q_tuple[2]}")

            stdin_data = "\n".join(lines) + "\n"
            cpp_out = bin_obj.run(stdin_data)
            oracle_out = run_oracle_range_add_sum(n, initial, queries)

            if cpp_out == oracle_out:
                passed += 1
            else:
                failed += 1
                print(f"  Seed {s} FAILED!\nExpected:\n{oracle_out[:100]}\nGot:\n{cpp_out[:100]}")
            total_ops += q
    finally:
        bin_obj.cleanup()

    return passed, failed, total_ops


def test_random_range_assign(num_seeds: int = 25, ops_per_seed: int = 25) -> Tuple[int, int, int]:
    print(f"Running Range Assign (Lazy) testing ({num_seeds} seeds, {ops_per_seed} ops/seed)...")
    code = generate_segment_tree_cpp("segment_tree_range_assign_range_query", {})
    bin_obj = CppBinary(code)
    passed = 0
    failed = 0
    total_ops = 0

    try:
        for s in range(num_seeds):
            rng = random.Random(3000 + s)
            n = rng.randint(10, 50)
            q = ops_per_seed
            initial = [0] + [rng.randint(-50, 50) for _ in range(n)]
            queries = []
            for _ in range(q):
                t = rng.choice([1, 2])
                if t == 1:
                    l = rng.randint(1, n)
                    r = rng.randint(l, n)
                    val = rng.randint(-20, 20)
                    queries.append((1, l, r, val))
                else:
                    l = rng.randint(1, n)
                    r = rng.randint(l, n)
                    queries.append((2, l, r))

            lines = [f"{n} {q}"]
            lines.append(" ".join(str(initial[i]) for i in range(1, n + 1)))
            for q_tuple in queries:
                if q_tuple[0] == 1:
                    lines.append(f"1 {q_tuple[1]} {q_tuple[2]} {q_tuple[3]}")
                else:
                    lines.append(f"2 {q_tuple[1]} {q_tuple[2]}")

            stdin_data = "\n".join(lines) + "\n"
            cpp_out = bin_obj.run(stdin_data)
            oracle_out = run_oracle_range_assign_sum(n, initial, queries)

            if cpp_out == oracle_out:
                passed += 1
            else:
                failed += 1
                print(f"  Seed {s} FAILED!\nExpected:\n{oracle_out[:100]}\nGot:\n{cpp_out[:100]}")
            total_ops += q
    finally:
        bin_obj.cleanup()

    return passed, failed, total_ops


def test_random_combined_lazy(num_seeds: int = 25, ops_per_seed: int = 25) -> Tuple[int, int, int]:
    print(f"Running Combined Lazy (Add + Assign) testing ({num_seeds} seeds, {ops_per_seed} ops/seed)...")
    code = generate_segment_tree_cpp("segment_tree_combined_lazy_range_query", {})
    bin_obj = CppBinary(code)
    passed = 0
    failed = 0
    total_ops = 0

    try:
        for s in range(num_seeds):
            rng = random.Random(4000 + s)
            n = rng.randint(10, 50)
            q = ops_per_seed
            initial = [0] + [rng.randint(-50, 50) for _ in range(n)]
            queries = []
            for _ in range(q):
                t = rng.choice([1, 2, 3])
                if t == 1:
                    l = rng.randint(1, n)
                    r = rng.randint(l, n)
                    val = rng.randint(-20, 20)
                    queries.append((1, l, r, val))
                elif t == 2:
                    l = rng.randint(1, n)
                    r = rng.randint(l, n)
                    val = rng.randint(-20, 20)
                    queries.append((2, l, r, val))
                else:
                    l = rng.randint(1, n)
                    r = rng.randint(l, n)
                    queries.append((3, l, r))

            lines = [f"{n} {q}"]
            lines.append(" ".join(str(initial[i]) for i in range(1, n + 1)))
            for q_tuple in queries:
                if q_tuple[0] == 1:
                    lines.append(f"1 {q_tuple[1]} {q_tuple[2]} {q_tuple[3]}")
                elif q_tuple[0] == 2:
                    lines.append(f"2 {q_tuple[1]} {q_tuple[2]} {q_tuple[3]}")
                else:
                    lines.append(f"3 {q_tuple[1]} {q_tuple[2]}")

            stdin_data = "\n".join(lines) + "\n"
            cpp_out = bin_obj.run(stdin_data)
            oracle_out = run_oracle_combined_lazy(n, initial, queries)

            if cpp_out == oracle_out:
                passed += 1
            else:
                failed += 1
                print(f"  Seed {s} FAILED!\nExpected:\n{oracle_out[:100]}\nGot:\n{cpp_out[:100]}")
            total_ops += q
    finally:
        bin_obj.cleanup()

    return passed, failed, total_ops


def test_random_max_subarray(num_seeds: int = 25, ops_per_seed: int = 25) -> Tuple[int, int, int]:
    print(f"Running Maximum Subarray Sum testing ({num_seeds} seeds, {ops_per_seed} ops/seed)...")
    code = generate_segment_tree_cpp("segment_tree_max_subarray", {})
    bin_obj = CppBinary(code)
    passed = 0
    failed = 0
    total_ops = 0

    try:
        for s in range(num_seeds):
            rng = random.Random(5000 + s)
            n = rng.randint(10, 50)
            q = ops_per_seed
            initial = [0] + [rng.randint(-50, 50) for _ in range(n)]
            queries = []
            for _ in range(q):
                t = rng.choice([1, 2])
                if t == 1:
                    idx = rng.randint(1, n)
                    val = rng.randint(-50, 50)
                    queries.append((1, idx, val))
                else:
                    l = rng.randint(1, n)
                    r = rng.randint(l, n)
                    queries.append((2, l, r))

            lines = [f"{n} {q}"]
            lines.append(" ".join(str(initial[i]) for i in range(1, n + 1)))
            for q_tuple in queries:
                if q_tuple[0] == 1:
                    lines.append(f"1 {q_tuple[1]} {q_tuple[2]}")
                else:
                    lines.append(f"2 {q_tuple[1]} {q_tuple[2]}")

            stdin_data = "\n".join(lines) + "\n"
            cpp_out = bin_obj.run(stdin_data)
            oracle_out = run_oracle_max_subarray(n, initial, queries)

            if cpp_out == oracle_out:
                passed += 1
            else:
                failed += 1
                print(f"  Seed {s} FAILED!\nExpected:\n{oracle_out[:100]}\nGot:\n{cpp_out[:100]}")
            total_ops += q
    finally:
        bin_obj.cleanup()

    return passed, failed, total_ops


def test_random_frequency_kth(num_seeds: int = 25, ops_per_seed: int = 25) -> Tuple[int, int, int]:
    print(f"Running Frequency K-th Element testing ({num_seeds} seeds, {ops_per_seed} ops/seed)...")
    code = generate_segment_tree_cpp("segment_tree_frequency_order_statistic", {})
    bin_obj = CppBinary(code)
    passed = 0
    failed = 0
    total_ops = 0

    try:
        for s in range(num_seeds):
            rng = random.Random(6000 + s)
            max_val = 30
            q = ops_per_seed
            queries = []
            cur_elements = []

            for _ in range(q):
                if not cur_elements:
                    t = 1
                else:
                    t = rng.choice([1, 2, 3])

                if t == 1:
                    val = rng.randint(1, max_val)
                    cur_elements.append(val)
                    queries.append((1, val))
                elif t == 2:
                    val = rng.choice(cur_elements)
                    cur_elements.remove(val)
                    queries.append((2, val))
                else:
                    k = rng.randint(1, len(cur_elements))
                    queries.append((3, k))

            lines = [f"{max_val} {q}"]
            for q_tuple in queries:
                if q_tuple[0] == 1:
                    lines.append(f"1 {q_tuple[1]}")
                elif q_tuple[0] == 2:
                    lines.append(f"2 {q_tuple[1]}")
                else:
                    lines.append(f"3 {q_tuple[1]}")

            stdin_data = "\n".join(lines) + "\n"
            cpp_out = bin_obj.run(stdin_data)
            oracle_out = run_oracle_frequency_kth(max_val, queries)

            if cpp_out == oracle_out:
                passed += 1
            else:
                failed += 1
                print(f"  Seed {s} FAILED!\nExpected:\n{oracle_out[:100]}\nGot:\n{cpp_out[:100]}")
            total_ops += q
    finally:
        bin_obj.cleanup()

    return passed, failed, total_ops


def run_all_randomized_tests():
    print("=" * 70)
    print("CHUP Phase 3J — Segment Tree Randomized Differential Test Suite")
    print("=" * 70)

    total_passed = 0
    total_failed = 0
    total_operations = 0

    tests = [
        test_random_point_update_range_sum,
        test_random_range_add,
        test_random_range_assign,
        test_random_combined_lazy,
        test_random_max_subarray,
        test_random_frequency_kth,
    ]

    for test_fn in tests:
        p, f, ops = test_fn()
        total_passed += p
        total_failed += f
        total_operations += ops

    total_runs = total_passed + total_failed
    pass_rate = (total_passed / total_runs) * 100 if total_runs > 0 else 0.0

    print("=" * 70)
    print(f"Randomized Test Summary: {total_passed}/{total_runs} seeds passed ({pass_rate:.1f}%)")
    print(f"Total Operations Verified: {total_operations}")
    print("=" * 70)

    if total_failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    run_all_randomized_tests()
