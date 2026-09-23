"""
Randomized Differential Testing Suite for Advanced DSU Domain (Phase 3H).

Generates diverse randomized input workloads:
1. Basic DSU: 1,000+ operations (unions, finds, connectivity checks, component sizes)
2. Weighted DSU: 500+ operations (relative potential difference constraints and queries)
3. Parity DSU: 500+ operations (dynamic 2-coloring XOR parity, bipartiteness conflict checks)
4. Rollback DSU: 500+ operations (union by size, undo history stack, snapshot checkpoints)
5. Offline Dynamic Connectivity: 500+ operations (segment tree over time, edge lifespans, offline queries)

Total: 3,000+ operations verified against independent Python reference oracles.
"""

import sys
import os
import random
import subprocess
import tempfile
from typing import List, Tuple, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from pointer_algorithms.generator.dsu_cpp_generator import generate_dsu_cpp
from pointer_algorithms.dsu.verification.dsu_oracles import (
    oracle_basic_dsu,
    oracle_weighted_dsu,
    oracle_parity_dsu,
    oracle_rollback_dsu,
    oracle_offline_dynamic_connectivity,
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


def test_basic_dsu(num_seeds: int = 50, ops_per_seed: int = 25) -> Tuple[int, int, int]:
    """Test 50 seeds * 25 ops = 1,250 operations."""
    cpp = generate_dsu_cpp("dsu_basic", {})
    binary = CppBinary(cpp)
    passed = 0
    total_ops = 0

    try:
        for seed in range(1, num_seeds + 1):
            rng = random.Random(seed * 2026)
            n = rng.randint(5, 20)
            q = ops_per_seed
            total_ops += q

            ops = []
            raw_ops = []
            for _ in range(q):
                op_type = rng.choice([1, 2, 3])
                u = rng.randint(1, n)
                v = rng.randint(1, n)
                ops.append(f"{op_type} {u} {v}")
                raw_ops.append((op_type, u, v))

            stdin_data = f"{n} {q}\n" + "\n".join(ops) + "\n"
            cpp_out = binary.run(stdin_data)
            expected_list = oracle_basic_dsu(n, raw_ops)
            expected = "\n".join(expected_list).strip()

            if cpp_out == expected:
                passed += 1
            else:
                print(f"[FAIL] Basic DSU seed {seed}: expected {expected[:60]}, got {cpp_out[:60]}")
    finally:
        binary.cleanup()

    return passed, num_seeds, total_ops


def test_weighted_dsu(num_seeds: int = 30, ops_per_seed: int = 20) -> Tuple[int, int, int]:
    """Test 30 seeds * 20 ops = 600 operations."""
    cpp = generate_dsu_cpp("dsu_weighted", {})
    binary = CppBinary(cpp)
    passed = 0
    total_ops = 0

    try:
        for seed in range(1, num_seeds + 1):
            rng = random.Random(seed * 3037)
            n = rng.randint(5, 15)
            q = ops_per_seed
            total_ops += q

            ops = []
            raw_ops = []
            for _ in range(q):
                op_type = rng.choice([1, 2])
                u = rng.randint(1, n)
                v = rng.randint(1, n)
                if op_type == 1:
                    w = rng.randint(-50, 50)
                    ops.append(f"1 {u} {v} {w}")
                    raw_ops.append((1, u, v, w))
                else:
                    ops.append(f"2 {u} {v}")
                    raw_ops.append((2, u, v))

            stdin_data = f"{n} {q}\n" + "\n".join(ops) + "\n"
            cpp_out = binary.run(stdin_data)
            expected_list = oracle_weighted_dsu(n, raw_ops)
            expected = "\n".join(expected_list).strip()

            if cpp_out == expected:
                passed += 1
            else:
                print(f"[FAIL] Weighted DSU seed {seed}: expected {expected[:60]}, got {cpp_out[:60]}")
    finally:
        binary.cleanup()

    return passed, num_seeds, total_ops


def test_parity_dsu(num_seeds: int = 30, ops_per_seed: int = 20) -> Tuple[int, int, int]:
    """Test 30 seeds * 20 ops = 600 operations."""
    cpp = generate_dsu_cpp("dsu_parity", {})
    binary = CppBinary(cpp)
    passed = 0
    total_ops = 0

    try:
        for seed in range(1, num_seeds + 1):
            rng = random.Random(seed * 4049)
            n = rng.randint(5, 15)
            q = ops_per_seed
            total_ops += q

            ops = []
            raw_ops = []
            for _ in range(q):
                op_type = rng.choice([1, 2])
                u = rng.randint(1, n)
                v = rng.randint(1, n)
                if op_type == 1:
                    rel = rng.choice([0, 1])
                    ops.append(f"1 {u} {v} {rel}")
                    raw_ops.append((1, u, v, rel))
                else:
                    ops.append(f"2 {u} {v}")
                    raw_ops.append((2, u, v))

            stdin_data = f"{n} {q}\n" + "\n".join(ops) + "\n"
            cpp_out = binary.run(stdin_data)
            expected_list = oracle_parity_dsu(n, raw_ops)
            expected = "\n".join(expected_list).strip()

            if cpp_out == expected:
                passed += 1
            else:
                print(f"[FAIL] Parity DSU seed {seed}: expected {expected[:60]}, got {cpp_out[:60]}")
    finally:
        binary.cleanup()

    return passed, num_seeds, total_ops


def test_rollback_dsu(num_seeds: int = 30, ops_per_seed: int = 20) -> Tuple[int, int, int]:
    """Test 30 seeds * 20 ops = 600 operations."""
    cpp = generate_dsu_cpp("dsu_rollback", {})
    binary = CppBinary(cpp)
    passed = 0
    total_ops = 0

    try:
        for seed in range(1, num_seeds + 1):
            rng = random.Random(seed * 5051)
            n = rng.randint(5, 15)
            q = ops_per_seed
            total_ops += q

            ops = []
            raw_ops = []
            snapshots_active = 0

            for _ in range(q):
                # 1: union, 2: connected, 3: snapshot, 4: rollback
                r = rng.random()
                if r < 0.45:
                    u = rng.randint(1, n)
                    v = rng.randint(1, n)
                    ops.append(f"1 {u} {v}")
                    raw_ops.append((1, u, v))
                elif r < 0.75:
                    u = rng.randint(1, n)
                    v = rng.randint(1, n)
                    ops.append(f"2 {u} {v}")
                    raw_ops.append((2, u, v))
                elif r < 0.90:
                    ops.append("3")
                    raw_ops.append((3,))
                    snapshots_active += 1
                else:
                    ops.append("4")
                    raw_ops.append((4,))
                    snapshots_active = max(0, snapshots_active - 1)

            stdin_data = f"{n} {q}\n" + "\n".join(ops) + "\n"
            cpp_out = binary.run(stdin_data)
            expected_list = oracle_rollback_dsu(n, raw_ops)
            expected = "\n".join(expected_list).strip()

            if cpp_out == expected:
                passed += 1
            else:
                print(f"[FAIL] Rollback DSU seed {seed}: expected {expected[:60]}, got {cpp_out[:60]}")
    finally:
        binary.cleanup()

    return passed, num_seeds, total_ops


def test_offline_dynamic_connectivity(num_seeds: int = 25, ops_per_seed: int = 24) -> Tuple[int, int, int]:
    """Test 25 seeds * 24 ops = 600 operations."""
    cpp = generate_dsu_cpp("dsu_offline_dynamic_connectivity", {})
    binary = CppBinary(cpp)
    passed = 0
    total_ops = 0

    try:
        for seed in range(1, num_seeds + 1):
            rng = random.Random(seed * 6063)
            n = rng.randint(4, 10)
            q = ops_per_seed
            total_ops += q

            active_edges = set()
            ops = []
            raw_ops = []

            for _ in range(q):
                u = rng.randint(1, n)
                v = rng.randint(1, n)
                while v == u and n > 1:
                    v = rng.randint(1, n)
                edge = (min(u, v), max(u, v))

                r = rng.random()
                if r < 0.40:
                    # Query connectivity
                    ops.append(f"3 {u} {v}")
                    raw_ops.append((3, u, v))
                elif r < 0.70:
                    # Add edge
                    if edge not in active_edges:
                        ops.append(f"1 {edge[0]} {edge[1]}")
                        raw_ops.append((1, edge[0], edge[1]))
                        active_edges.add(edge)
                    else:
                        ops.append(f"3 {u} {v}")
                        raw_ops.append((3, u, v))
                else:
                    # Remove edge
                    if edge in active_edges:
                        ops.append(f"2 {edge[0]} {edge[1]}")
                        raw_ops.append((2, edge[0], edge[1]))
                        active_edges.remove(edge)
                    else:
                        ops.append(f"3 {u} {v}")
                        raw_ops.append((3, u, v))

            stdin_data = f"{n} {len(ops)}\n" + "\n".join(ops) + "\n"
            cpp_out = binary.run(stdin_data)
            expected_list = oracle_offline_dynamic_connectivity(n, raw_ops)
            expected = "\n".join(expected_list).strip()

            if cpp_out == expected:
                passed += 1
            else:
                print(f"[FAIL] Offline DSU seed {seed}: expected {expected[:60]}, got {cpp_out[:60]}")
    finally:
        binary.cleanup()

    return passed, num_seeds, total_ops


def run_all_randomized_tests() -> bool:
    print("=" * 70)
    print("CHUP Phase 3H — Advanced DSU Randomized Stress Testing")
    print("=" * 70)

    total_passed = 0
    total_runs = 0
    grand_ops = 0

    suites = [
        ("Basic DSU (1000+ ops)", test_basic_dsu, 50, 25),
        ("Weighted DSU (500+ ops)", test_weighted_dsu, 30, 20),
        ("Parity DSU (500+ ops)", test_parity_dsu, 30, 20),
        ("Rollback DSU (500+ ops)", test_rollback_dsu, 30, 20),
        ("Offline Dynamic Connectivity (500+ ops)", test_offline_dynamic_connectivity, 25, 24),
    ]

    for name, fn, seeds, ops in suites:
        passed, runs, ops_count = fn(seeds, ops)
        total_passed += passed
        total_runs += runs
        grand_ops += ops_count
        status = "PASS" if passed == runs else "FAIL"
        print(f"  [{status}] {name}: {passed}/{runs} test suites passed ({ops_count} operations)")

    print("=" * 70)
    print(f"Total Test Runs Passed: {total_passed}/{total_runs} ({total_passed/total_runs*100:.1f}%)")
    print(f"Total Operations Verified Against Oracles: {grand_ops}")
    print("=" * 70)

    return total_passed == total_runs


if __name__ == "__main__":
    success = run_all_randomized_tests()
    sys.exit(0 if success else 1)
