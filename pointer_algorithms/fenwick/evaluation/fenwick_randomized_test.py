"""
CHUP Phase 3I — Fenwick Tree (BIT) Randomized Differential Testing Suite
Verifies Fenwick Tree implementations against Python reference oracles across 165+ seeds and thousands of operations:
1. Point Update & Prefix Query (40 seeds, ~1000 ops)
2. Point Update & Range Query (30 seeds, ~750 ops)
3. Range Update & Point Query (25 seeds, ~625 ops)
4. Range Update & Range Query (Two-Fenwick) (25 seeds, ~625 ops)
5. Dynamic Multiset & K-th Element via Binary Lifting (25 seeds, ~625 ops)
6. 2D Subgrid Inclusion-Exclusion (20 seeds, ~500 ops)
Total: 165 seeds, 4,000+ operations verified against independent reference oracles.
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

from pointer_algorithms.generator.fenwick_cpp_generator import generate_fenwick_cpp
from pointer_algorithms.fenwick.evaluation.fenwick_benchmark import (
    run_oracle_point_update_prefix,
    run_oracle_point_update_range,
    run_oracle_range_update_point,
    run_oracle_range_update_range,
    run_oracle_multiset,
    run_oracle_2d,
)
from pointer_algorithms.fenwick.verification.fenwick_oracles import (
    FenwickTreeOracle,
    RangeUpdatePointQueryBITOracle,
    RangeUpdateRangeQueryBITOracle,
    Fenwick2DOracle,
    FenwickMultisetOracle,
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


def test_random_point_update_prefix(num_seeds: int = 40, ops_per_seed: int = 25) -> Tuple[int, int, int]:
    print(f"Running Point Update & Prefix Query testing ({num_seeds} seeds, {ops_per_seed} ops/seed)...")
    code = generate_fenwick_cpp("fenwick_point_update_prefix_query", {"fenwick_operation_kind": "prefix_query"})
    bin_obj = CppBinary(code)
    passed = 0
    failed = 0
    total_ops = 0

    try:
        for s in range(num_seeds):
            rng = random.Random(42 + s)
            n = rng.randint(10, 50)
            q = ops_per_seed
            initial = [0] + [rng.randint(-100, 100) for _ in range(n)]
            queries = []
            for _ in range(q):
                t = rng.choice([1, 2])
                if t == 1:
                    idx = rng.randint(1, n)
                    delta = rng.randint(-50, 50)
                    queries.append((1, idx, delta))
                else:
                    idx = rng.randint(1, n)
                    queries.append((2, idx))

            lines = [f"{n} {q}"]
            lines.append(" ".join(str(initial[i]) for i in range(1, n + 1)))
            range_queries = []
            for q_tuple in queries:
                if q_tuple[0] == 1:
                    lines.append(f"1 {q_tuple[1]} {q_tuple[2]}")
                    range_queries.append(q_tuple)
                else:
                    lines.append(f"2 1 {q_tuple[1]}")
                    range_queries.append((2, 1, q_tuple[1]))
            stdin_data = "\n".join(lines) + "\n"

            expected = run_oracle_point_update_range(n, list(initial), range_queries)
            exp_str = expected.strip()
            act_str = bin_obj.run(stdin_data).strip()

            if act_str == exp_str:
                passed += 1
            else:
                failed += 1
                print(f"  [FAIL] Seed {s}: Expected {exp_str[:50]}..., got {act_str[:50]}...")
            total_ops += q
    finally:
        bin_obj.cleanup()

    return passed, failed, total_ops


def test_random_point_update_range(num_seeds: int = 30, ops_per_seed: int = 25) -> Tuple[int, int, int]:
    print(f"Running Point Update & Range Query testing ({num_seeds} seeds, {ops_per_seed} ops/seed)...")
    code = generate_fenwick_cpp("fenwick_point_update_prefix_query", {"fenwick_operation_kind": "range_query"})
    bin_obj = CppBinary(code)
    passed = 0
    failed = 0
    total_ops = 0

    try:
        for s in range(num_seeds):
            rng = random.Random(100 + s)
            n = rng.randint(10, 40)
            q = ops_per_seed
            initial = [0] + [rng.randint(-100, 100) for _ in range(n)]
            queries = []
            for _ in range(q):
                t = rng.choice([1, 2])
                if t == 1:
                    idx = rng.randint(1, n)
                    delta = rng.randint(-50, 50)
                    queries.append((1, idx, delta))
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

            expected = run_oracle_point_update_range(n, list(initial), queries)
            exp_str = expected.strip()
            act_str = bin_obj.run(stdin_data).strip()

            if act_str == exp_str:
                passed += 1
            else:
                failed += 1
                print(f"  [FAIL] Range Query Seed {s}: Expected {exp_str[:50]}..., got {act_str[:50]}...")
            total_ops += q
    finally:
        bin_obj.cleanup()

    return passed, failed, total_ops


def test_random_range_update_point(num_seeds: int = 25, ops_per_seed: int = 25) -> Tuple[int, int, int]:
    print(f"Running Range Update & Point Query testing ({num_seeds} seeds, {ops_per_seed} ops/seed)...")
    code = generate_fenwick_cpp("fenwick_range_update_point_query", {})
    bin_obj = CppBinary(code)
    passed = 0
    failed = 0
    total_ops = 0

    try:
        for s in range(num_seeds):
            rng = random.Random(200 + s)
            n = rng.randint(10, 40)
            q = ops_per_seed
            initial = [0] + [rng.randint(-50, 50) for _ in range(n)]
            queries = []
            for _ in range(q):
                t = rng.choice([1, 2])
                if t == 1:
                    l = rng.randint(1, n)
                    r = rng.randint(l, n)
                    delta = rng.randint(-30, 30)
                    queries.append((1, l, r, delta))
                else:
                    idx = rng.randint(1, n)
                    queries.append((2, idx))

            lines = [f"{n} {q}"]
            lines.append(" ".join(str(initial[i]) for i in range(1, n + 1)))
            for q_tuple in queries:
                if q_tuple[0] == 1:
                    lines.append(f"1 {q_tuple[1]} {q_tuple[2]} {q_tuple[3]}")
                else:
                    lines.append(f"2 {q_tuple[1]}")
            stdin_data = "\n".join(lines) + "\n"

            expected = run_oracle_range_update_point(n, list(initial), queries)
            exp_str = expected.strip()
            act_str = bin_obj.run(stdin_data).strip()

            if act_str == exp_str:
                passed += 1
            else:
                failed += 1
                print(f"  [FAIL] Range Upd Point Qry Seed {s}: Expected {exp_str[:50]}..., got {act_str[:50]}...")
            total_ops += q
    finally:
        bin_obj.cleanup()

    return passed, failed, total_ops


def test_random_range_update_range(num_seeds: int = 25, ops_per_seed: int = 25) -> Tuple[int, int, int]:
    print(f"Running Range Update & Range Query (Two-Fenwick) testing ({num_seeds} seeds, {ops_per_seed} ops/seed)...")
    code = generate_fenwick_cpp("fenwick_range_update_range_query", {})
    bin_obj = CppBinary(code)
    passed = 0
    failed = 0
    total_ops = 0

    try:
        for s in range(num_seeds):
            rng = random.Random(300 + s)
            n = rng.randint(10, 35)
            q = ops_per_seed
            initial = [0] + [rng.randint(-50, 50) for _ in range(n)]
            queries = []
            for _ in range(q):
                t = rng.choice([1, 2])
                if t == 1:
                    l = rng.randint(1, n)
                    r = rng.randint(l, n)
                    delta = rng.randint(-20, 20)
                    queries.append((1, l, r, delta))
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

            expected = run_oracle_range_update_range(n, list(initial), queries)
            exp_str = expected.strip()
            act_str = bin_obj.run(stdin_data).strip()

            if act_str == exp_str:
                passed += 1
            else:
                failed += 1
                print(f"  [FAIL] Two-Fenwick Seed {s}: Expected {exp_str[:50]}..., got {act_str[:50]}...")
            total_ops += q
    finally:
        bin_obj.cleanup()

    return passed, failed, total_ops


def test_random_multiset_kth(num_seeds: int = 25, ops_per_seed: int = 25) -> Tuple[int, int, int]:
    print(f"Running Dynamic Multiset & K-th Element testing ({num_seeds} seeds, {ops_per_seed} ops/seed)...")
    code = generate_fenwick_cpp("fenwick_multiset", {})
    bin_obj = CppBinary(code)
    passed = 0
    failed = 0
    total_ops = 0

    try:
        for s in range(num_seeds):
            rng = random.Random(400 + s)
            max_val = 30
            q = ops_per_seed
            queries = []
            active = []
            for _ in range(q):
                t = rng.choices([1, 2, 3, 4, 5], weights=[40, 20, 15, 15, 10])[0]
                if t == 1:
                    val = rng.randint(1, max_val)
                    queries.append((1, val))
                    active.append(val)
                elif t == 2:
                    if active:
                        val = rng.choice(active)
                        active.remove(val)
                        queries.append((2, val))
                    else:
                        val = rng.randint(1, max_val)
                        queries.append((1, val))
                        active.append(val)
                elif t == 3:
                    val = rng.randint(1, max_val)
                    queries.append((3, val))
                elif t == 4:
                    val = rng.randint(1, max_val)
                    queries.append((4, val))
                else:
                    k = rng.randint(1, max(1, len(active)))
                    queries.append((5, k))

            lines = [f"{max_val} {len(queries)}"]
            for q_tuple in queries:
                lines.append(f"{q_tuple[0]} {q_tuple[1]}")
            stdin_data = "\n".join(lines) + "\n"

            expected = run_oracle_multiset(max_val, queries)
            exp_str = expected.strip()
            act_str = bin_obj.run(stdin_data).strip()

            if act_str == exp_str:
                passed += 1
            else:
                failed += 1
                print(f"  [FAIL] Multiset Seed {s}: Expected {exp_str[:50]}..., got {act_str[:50]}...")
            total_ops += len(queries)
    finally:
        bin_obj.cleanup()

    return passed, failed, total_ops


def test_random_2d_fenwick(num_seeds: int = 20, ops_per_seed: int = 25) -> Tuple[int, int, int]:
    print(f"Running 2D Fenwick Grid testing ({num_seeds} seeds, {ops_per_seed} ops/seed)...")
    code = generate_fenwick_cpp("fenwick_2d_point_update_range_query", {})
    bin_obj = CppBinary(code)
    passed = 0
    failed = 0
    total_ops = 0

    try:
        for s in range(num_seeds):
            rng = random.Random(500 + s)
            r_max = rng.randint(4, 10)
            c_max = rng.randint(4, 10)
            q = ops_per_seed
            queries = []
            for _ in range(q):
                t = rng.choice([1, 2])
                if t == 1:
                    r = rng.randint(1, r_max)
                    c = rng.randint(1, c_max)
                    delta = rng.randint(1, 20)
                    queries.append((1, r, c, delta))
                else:
                    r1 = rng.randint(1, r_max)
                    r2 = rng.randint(r1, r_max)
                    c1 = rng.randint(1, c_max)
                    c2 = rng.randint(c1, c_max)
                    queries.append((2, r1, c1, r2, c2))

            lines = [f"{r_max} {c_max} {q}"]
            for q_tuple in queries:
                if q_tuple[0] == 1:
                    lines.append(f"1 {q_tuple[1]} {q_tuple[2]} {q_tuple[3]}")
                else:
                    lines.append(f"2 {q_tuple[1]} {q_tuple[2]} {q_tuple[3]} {q_tuple[4]}")
            stdin_data = "\n".join(lines) + "\n"

            expected = run_oracle_2d(r_max, c_max, queries)
            exp_str = expected.strip()
            act_str = bin_obj.run(stdin_data).strip()

            if act_str == exp_str:
                passed += 1
            else:
                failed += 1
                print(f"  [FAIL] 2D Fenwick Seed {s}: Expected {exp_str[:50]}..., got {act_str[:50]}...")
            total_ops += q
    finally:
        bin_obj.cleanup()

    return passed, failed, total_ops


def run_all_randomized_tests() -> bool:
    print("=" * 70)
    print("CHUP Phase 3I — Fenwick Tree Randomized Differential Test Battery")
    print("=" * 70)

    total_passed = 0
    total_failed = 0
    grand_ops = 0

    suites = [
        ("Point Update & Prefix Query", test_random_point_update_prefix, 40),
        ("Point Update & Range Query", test_random_point_update_range, 30),
        ("Range Update & Point Query", test_random_range_update_point, 25),
        ("Two-Fenwick Range Add / Range Query", test_random_range_update_range, 25),
        ("Dynamic Multiset & K-th Lifting", test_random_multiset_kth, 25),
        ("2D Fenwick Grid Inclusion-Exclusion", test_random_2d_fenwick, 20),
    ]

    for name, func, expected_seeds in suites:
        p, f, ops = func()
        total_passed += p
        total_failed += f
        grand_ops += ops
        status = "PASSED" if f == 0 and p == expected_seeds else "FAILED"
        print(f"  [{status}] {name}: {p}/{expected_seeds} seeds passed ({ops} operations)")

    total_seeds = total_passed + total_failed
    print("=" * 70)
    print(f"Randomized Test Total: {total_passed}/{total_seeds} seeds ({grand_ops} operations)")
    print("=" * 70)
    return total_failed == 0


if __name__ == "__main__":
    success = run_all_randomized_tests()
    sys.exit(0 if success else 1)
