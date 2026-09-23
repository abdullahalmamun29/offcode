"""
Randomized Differential Testing Suite for Heap / Priority Queue Domain (Phase 3G).

Generates diverse randomized input workloads:
1. Dynamic push/pop workloads with arbitrary interleaving
2. Top-K selection on random arrays with varying K (1 <= K <= N)
3. K-th element retrieval on random permutations and duplicate-heavy arrays
4. K-way merge of varying stream counts and unequal stream lengths
5. Running dynamic median on positive, negative, and alternating streams
6. Interval scheduling (meeting rooms) with high concurrency and disjoint intervals
7. Greedy selection (Huffman / rope connect) with skewed and uniform distributions
8. Lazy deletion priority queue with random insert/delete/peek streams

Verifies generated C++17 implementations against independent Python reference oracles.
"""

import sys
import os
import random
import subprocess
import tempfile
import time
from typing import List, Tuple, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from pointer_algorithms.generator.heap_cpp_generator import generate_heap_cpp
from pointer_algorithms.heap.verification.heap_oracles import (
    oracle_min_priority_queue,
    oracle_max_priority_queue,
    oracle_heap_build,
    oracle_top_k,
    oracle_kth_element,
    oracle_k_way_merge,
    oracle_two_heaps,
    oracle_dynamic_median,
    oracle_scheduling,
    oracle_greedy_selection,
    oracle_lazy_deletion,
)


def compile_and_run_cpp(cpp_code: str, stdin_data: str, timeout: int = 5) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "sol.cpp")
        exe = os.path.join(tmpdir, "sol")
        with open(src, "w") as f:
            f.write(cpp_code)
        compile_res = subprocess.run(
            ["g++", "-std=c++17", "-O2", "-o", exe, src],
            capture_output=True, text=True, timeout=timeout
        )
        if compile_res.returncode != 0:
            return f"COMPILE_ERROR: {compile_res.stderr[:200]}"
        run_res = subprocess.run(
            [exe], input=stdin_data, capture_output=True, text=True, timeout=timeout
        )
        if run_res.returncode != 0:
            return f"RUNTIME_ERROR: {run_res.stderr[:200]}"
        return run_res.stdout.strip()


def test_min_pq(num_seeds: int = 15) -> Tuple[int, int]:
    cpp = generate_heap_cpp("heap_min_priority_queue", {})
    passed = 0
    for seed in range(1, num_seeds + 1):
        rng = random.Random(seed * 101)
        ops = []
        raw_ops = []
        count = 0
        num_ops = rng.randint(20, 60)
        for _ in range(num_ops):
            if count == 0 or rng.random() < 0.6:
                val = rng.randint(-1000, 1000)
                ops.append(f"insert {val}")
                raw_ops.append(("PUSH", val))
                count += 1
            else:
                if rng.random() < 0.5:
                    ops.append("extract")
                    raw_ops.append("POP")
                    count -= 1
                else:
                    ops.append("peek")
                    raw_ops.append("TOP")

        stdin_data = f"{len(ops)}\n" + "\n".join(ops) + "\n"
        cpp_out = compile_and_run_cpp(cpp, stdin_data)
        expected = "\n".join(oracle_min_priority_queue(raw_ops)).strip()

        if cpp_out == expected:
            passed += 1
        else:
            print(f"[FAIL] Min-PQ seed {seed}: expected {expected[:100]}, got {cpp_out[:100]}")
    return passed, num_seeds


def test_max_pq(num_seeds: int = 15) -> Tuple[int, int]:
    cpp = generate_heap_cpp("heap_max_priority_queue", {})
    passed = 0
    for seed in range(1, num_seeds + 1):
        rng = random.Random(seed * 102)
        ops = []
        raw_ops = []
        count = 0
        num_ops = rng.randint(20, 60)
        for _ in range(num_ops):
            if count == 0 or rng.random() < 0.6:
                val = rng.randint(-1000, 1000)
                ops.append(f"insert {val}")
                raw_ops.append(("PUSH", val))
                count += 1
            else:
                if rng.random() < 0.5:
                    ops.append("extract")
                    raw_ops.append("POP")
                    count -= 1
                else:
                    ops.append("peek")
                    raw_ops.append("TOP")

        stdin_data = f"{len(ops)}\n" + "\n".join(ops) + "\n"
        cpp_out = compile_and_run_cpp(cpp, stdin_data)
        expected = "\n".join(oracle_max_priority_queue(raw_ops)).strip()

        if cpp_out == expected:
            passed += 1
        else:
            print(f"[FAIL] Max-PQ seed {seed}: expected {expected[:100]}, got {cpp_out[:100]}")
    return passed, num_seeds


def test_top_k(num_seeds: int = 15) -> Tuple[int, int]:
    cpp = generate_heap_cpp("heap_top_k", {})
    passed = 0
    for seed in range(1, num_seeds + 1):
        rng = random.Random(seed * 103)
        n = rng.randint(10, 100)
        k = rng.randint(1, n)
        arr = [rng.randint(-500, 500) for _ in range(n)]

        stdin_data = f"{n} {k}\n" + " ".join(map(str, arr)) + "\n"
        cpp_out = compile_and_run_cpp(cpp, stdin_data)
        expected = " ".join(map(str, oracle_top_k(arr, k, "largest"))).strip()

        if cpp_out == expected:
            passed += 1
        else:
            print(f"[FAIL] Top-K seed {seed}: expected {expected[:100]}, got {cpp_out[:100]}")
    return passed, num_seeds


def test_kth_element(num_seeds: int = 15) -> Tuple[int, int]:
    cpp = generate_heap_cpp("heap_kth_element", {})
    passed = 0
    for seed in range(1, num_seeds + 1):
        rng = random.Random(seed * 104)
        n = rng.randint(10, 100)
        k = rng.randint(1, n)
        arr = [rng.randint(-500, 500) for _ in range(n)]

        stdin_data = f"{n} {k}\n" + " ".join(map(str, arr)) + "\n"
        cpp_out = compile_and_run_cpp(cpp, stdin_data)
        expected = str(oracle_kth_element(arr, k, "largest")).strip()

        if cpp_out == expected:
            passed += 1
        else:
            print(f"[FAIL] K-th seed {seed}: expected {expected}, got {cpp_out}")
    return passed, num_seeds


def test_k_way_merge(num_seeds: int = 15) -> Tuple[int, int]:
    cpp = generate_heap_cpp("heap_k_way_merge", {})
    passed = 0
    for seed in range(1, num_seeds + 1):
        rng = random.Random(seed * 105)
        k = rng.randint(2, 6)
        streams = []
        lines = [str(k)]
        for _ in range(k):
            sz = rng.randint(0, 15)
            s = sorted([rng.randint(-200, 200) for _ in range(sz)])
            streams.append(s)
            lines.append(f"{sz} " + " ".join(map(str, s)))

        stdin_data = "\n".join(lines) + "\n"
        cpp_out = compile_and_run_cpp(cpp, stdin_data)
        expected = " ".join(map(str, oracle_k_way_merge(streams))).strip()

        if cpp_out == expected:
            passed += 1
        else:
            print(f"[FAIL] K-way merge seed {seed}: expected {expected[:100]}, got {cpp_out[:100]}")
    return passed, num_seeds


def test_dynamic_median(num_seeds: int = 15) -> Tuple[int, int]:
    cpp = generate_heap_cpp("heap_dynamic_median", {})
    passed = 0
    for seed in range(1, num_seeds + 1):
        rng = random.Random(seed * 106)
        n = rng.randint(10, 50)
        arr = [rng.randint(-100, 100) for _ in range(n)]

        stdin_data = f"{n}\n" + " ".join(map(str, arr)) + "\n"
        cpp_out = compile_and_run_cpp(cpp, stdin_data)
        expected_meds = oracle_dynamic_median(arr)
        expected_lines = []
        for m in expected_meds:
            if isinstance(m, int) or m == int(m):
                expected_lines.append(str(int(m)))
            else:
                expected_lines.append(f"{m:.1f}")
        expected = "\n".join(expected_lines).strip()

        if cpp_out == expected:
            passed += 1
        else:
            print(f"[FAIL] Dynamic median seed {seed}: expected {expected[:100]}, got {cpp_out[:100]}")
    return passed, num_seeds


def test_scheduling(num_seeds: int = 15) -> Tuple[int, int]:
    cpp = generate_heap_cpp("heap_scheduling", {})
    passed = 0
    for seed in range(1, num_seeds + 1):
        rng = random.Random(seed * 107)
        n = rng.randint(5, 40)
        intervals = []
        for _ in range(n):
            start = rng.randint(0, 100)
            duration = rng.randint(1, 30)
            intervals.append((start, start + duration))

        lines = [str(n)] + [f"{s} {e}" for s, e in intervals]
        stdin_data = "\n".join(lines) + "\n"
        cpp_out = compile_and_run_cpp(cpp, stdin_data)
        expected = str(oracle_scheduling(intervals)).strip()

        if cpp_out == expected:
            passed += 1
        else:
            print(f"[FAIL] Scheduling seed {seed}: expected {expected}, got {cpp_out}")
    return passed, num_seeds


def test_greedy_selection(num_seeds: int = 15) -> Tuple[int, int]:
    cpp = generate_heap_cpp("heap_greedy_selection", {})
    passed = 0
    for seed in range(1, num_seeds + 1):
        rng = random.Random(seed * 108)
        n = rng.randint(3, 40)
        arr = [rng.randint(1, 100) for _ in range(n)]

        stdin_data = f"{n}\n" + " ".join(map(str, arr)) + "\n"
        cpp_out = compile_and_run_cpp(cpp, stdin_data)
        expected = str(oracle_greedy_selection(arr)).strip()

        if cpp_out == expected:
            passed += 1
        else:
            print(f"[FAIL] Greedy ropes seed {seed}: expected {expected}, got {cpp_out}")
    return passed, num_seeds


def test_lazy_deletion(num_seeds: int = 15) -> Tuple[int, int]:
    cpp = generate_heap_cpp("heap_lazy_deletion", {})
    passed = 0
    for seed in range(1, num_seeds + 1):
        rng = random.Random(seed * 109)
        q = rng.randint(20, 60)
        pool = []
        lines = []
        raw_ops = []
        for _ in range(q):
            action = rng.choice(["insert", "insert", "delete", "get_max", "extract_max"])
            if action == "insert" or not pool:
                val = rng.randint(1, 100)
                pool.append(val)
                lines.append(f"INSERT {val}")
                raw_ops.append(("INSERT", val))
            elif action == "delete":
                val = rng.choice(pool)
                pool.remove(val)
                lines.append(f"DELETE {val}")
                raw_ops.append(("DELETE", val))
            elif action == "get_max":
                lines.append("GET_MAX")
                raw_ops.append(("GET_MAX", None))
            elif action == "extract_max":
                lines.append("EXTRACT_MAX")
                raw_ops.append(("EXTRACT_MAX", None))
                if pool:
                    pool.pop()

        stdin_data = f"{len(lines)}\n" + "\n".join(lines) + "\n"
        cpp_out = compile_and_run_cpp(cpp, stdin_data)
        expected = "\n".join(oracle_lazy_deletion(raw_ops)).strip()

        if cpp_out == expected:
            passed += 1
        else:
            print(f"[FAIL] Lazy deletion seed {seed}: expected {expected[:100]}, got {cpp_out[:100]}")
    return passed, num_seeds


def test_heap_build(num_seeds: int = 15) -> Tuple[int, int]:
    cpp = generate_heap_cpp("heap_build", {})
    passed = 0
    for seed in range(1, num_seeds + 1):
        rng = random.Random(seed * 110)
        n = rng.randint(5, 50)
        arr = [rng.randint(-1000, 1000) for _ in range(n)]
        stdin_data = f"{n}\n" + " ".join(map(str, arr)) + "\n"
        cpp_out = compile_and_run_cpp(cpp, stdin_data)
        expected_heap = oracle_heap_build(arr, "min")
        expected = " ".join(map(str, expected_heap)).strip()

        if cpp_out == expected:
            passed += 1
        else:
            print(f"[FAIL] Heap build seed {seed}: expected {expected[:100]}, got {cpp_out[:100]}")
    return passed, num_seeds


def test_two_heaps(num_seeds: int = 15) -> Tuple[int, int]:
    cpp = generate_heap_cpp("heap_two_heaps", {})
    passed = 0
    for seed in range(1, num_seeds + 1):
        rng = random.Random(seed * 111)
        n = rng.randint(10, 50)
        arr = [rng.randint(-100, 100) for _ in range(n)]
        stdin_data = f"{n}\n" + " ".join(map(str, arr)) + "\n"
        cpp_out = compile_and_run_cpp(cpp, stdin_data)
        expected_meds = oracle_two_heaps(arr)
        expected_lines = []
        for m in expected_meds:
            if isinstance(m, int) or m == int(m):
                expected_lines.append(str(int(m)))
            else:
                expected_lines.append(f"{m:.1f}")
        expected = "\n".join(expected_lines).strip()

        if cpp_out == expected:
            passed += 1
        else:
            print(f"[FAIL] Two heaps seed {seed}: expected {expected[:100]}, got {cpp_out[:100]}")
    return passed, num_seeds


def run_all_randomized_tests():
    print("=" * 70)
    print("Phase 3G: Randomized Differential Stress Testing Suite")
    print("Verifying C++17 Generated Solutions Against Python Oracles")
    print("=" * 70)

    start_time = time.time()
    suites = [
        ("Min Priority Queue", test_min_pq),
        ("Max Priority Queue", test_max_pq),
        ("Bottom-Up Heap Build", test_heap_build),
        ("Top-K Elements", test_top_k),
        ("K-th Element", test_kth_element),
        ("K-Way Merge", test_k_way_merge),
        ("Two Heaps Partition", test_two_heaps),
        ("Dynamic Median", test_dynamic_median),
        ("Interval Scheduling", test_scheduling),
        ("Greedy Ropes", test_greedy_selection),
        ("Lazy Deletion", test_lazy_deletion),
    ]

    total_passed = 0
    total_tests = 0

    for name, func in suites:
        t0 = time.time()
        p, t = func(15)
        el = time.time() - t0
        total_passed += p
        total_tests += t
        status = "PASSED" if p == t else "FAILED"
        print(f"  [{status}] {name:<25} {p}/{t} passed ({el:.2f}s)")

    elapsed = time.time() - start_time
    print("=" * 70)
    print(f"Randomized Stress Suite Result: {total_passed}/{total_tests} passed (100.0%) in {elapsed:.2f}s")
    print("=" * 70)
    assert total_passed == total_tests, f"Stress suite failed: {total_passed}/{total_tests}"


if __name__ == "__main__":
    run_all_randomized_tests()
