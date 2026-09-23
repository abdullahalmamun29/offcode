"""
CHUP Phase 3P — Number Theory & Combinatorics Randomized Stress Test Suite.

Differential randomized stress testing comparing compiled C++ implementations
against independent reference oracles across 220 randomized test instances:
1. nt_extended_gcd vs Diophantine & ExtGCD Oracle (22 runs)
2. nt_modular_inverse vs Modular Inverse Oracle (22 runs)
3. nt_chinese_remainder vs CRT Oracle (22 runs)
4. nt_linear_sieve vs Linear Sieve Oracle (22 runs)
5. nt_euler_totient vs Euler Totient Oracle (22 runs)
6. nt_mobius_inversion vs Möbius Inversion Oracle (22 runs)
7. nt_matrix_power vs Matrix Power Oracle (22 runs)
8. nt_combinatorics_factorials vs Factorial Combinatorics Oracle (22 runs)
9. nt_lucas_theorem vs Lucas Theorem Oracle (22 runs)
10. nt_miller_rabin vs Deterministic Miller-Rabin Oracle (22 runs)

Total: 220 test cases.
"""

import sys
import os
import random
import subprocess
import tempfile
import hashlib
from typing import Dict, Any, List, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.generator.nt_cpp_generator import generate_nt_cpp
from pointer_algorithms.number_theory.verification.nt_oracles import (
    solve_diophantine,
    extended_gcd,
    modular_inverse,
    chinese_remainder,
    linear_sieve,
    euler_totient_single,
    coprime_pairs_grid,
    matrix_power,
    combinations_mod_p,
    lucas_theorem,
    miller_rabin_deterministic
)

COMPILED_BINARIES: Dict[str, str] = {}


def compile_and_run(pattern: str, stdin_data: str, timeout: int = 10) -> str:
    code = generate_nt_cpp(pattern, {})
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


SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def run_stress_tests():
    random.seed(1337)
    total_passed = 0
    total_tests = 220
    test_idx = 0

    print("=" * 80)
    print("CHUP Phase 3P — Number Theory Randomized Stress Tests (220 Cases)")
    print("=" * 80)

    # ── 1. Extended GCD & Linear Diophantine (22 runs) ──
    for i in range(22):
        test_idx += 1
        a = random.randint(1, 10000)
        b = random.randint(1, 10000)
        solvable = (random.random() < 0.7)
        g, _, _ = extended_gcd(a, b)
        if solvable:
            c = g * random.randint(0, 100)
        else:
            c = g * random.randint(1, 100) + random.randint(1, g - 1) if g > 1 else g + 1

        sol = solve_diophantine(a, b, c)
        if sol is None:
            expected_str = "IMPOSSIBLE"
        else:
            x0, y0, _, _, gcd_val = sol
            expected_str = f"{x0} {y0} {gcd_val}"

        out = compile_and_run("nt_extended_gcd", f"{a} {b} {c}")
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: ExtGCD run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 2. Modular Multiplicative Inverse (22 runs) ──
    for i in range(22):
        test_idx += 1
        m = random.randint(2, 100000)
        a = random.randint(1, m * 2)

        inv = modular_inverse(a, m)
        expected_str = "-1" if inv is None else str(inv)

        out = compile_and_run("nt_modular_inverse", f"{a} {m}")
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: ModInverse run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 3. Chinese Remainder Theorem (22 runs) ──
    for i in range(22):
        test_idx += 1
        k = random.randint(2, 4)
        congruences = []
        # pick coprime moduli mostly
        mods = random.sample(SMALL_PRIMES[1:15], k)
        for mod in mods:
            r = random.randint(0, mod - 1)
            congruences.append((r, mod))

        res = chinese_remainder(congruences)
        expected_str = "-1" if res is None else str(res[0])

        stdin_data = f"{k}\n" + "\n".join(f"{r} {m}" for r, m in congruences)
        out = compile_and_run("nt_chinese_remainder", stdin_data)
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: CRT run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 4. Euler Linear Sieve (22 runs) ──
    for i in range(22):
        test_idx += 1
        n = random.randint(2, 50000)
        primes, _ = linear_sieve(n)
        expected_str = str(len(primes))

        out = compile_and_run("nt_linear_sieve", str(n))
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: Linear Sieve run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 5. Euler's Totient Function (22 runs) ──
    for i in range(22):
        test_idx += 1
        n = random.randint(1, 10000000)
        expected_str = str(euler_totient_single(n))

        out = compile_and_run("nt_euler_totient", str(n))
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: Euler Totient run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 6. Möbius Inversion (22 runs) ──
    for i in range(22):
        test_idx += 1
        n = random.randint(1, 200)
        m = random.randint(1, 200)
        expected_str = str(coprime_pairs_grid(n, m))

        out = compile_and_run("nt_mobius_inversion", f"{n} {m}")
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: Mobius Inversion run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 7. Matrix Exponentiation (22 runs) ──
    for i in range(22):
        test_idx += 1
        d = random.choice([2, 3])
        k = random.randint(0, 1000)
        mod = random.choice([1000000007, 998244353, 10007, 7])
        A = [[random.randint(0, 10) for _ in range(d)] for _ in range(d)]

        res_matrix = matrix_power(A, k, mod)
        expected_str = "\n".join(" ".join(map(str, row)) for row in res_matrix)

        stdin_data = f"{d} {k} {mod}\n" + "\n".join(" ".join(map(str, row)) for row in A)
        out = compile_and_run("nt_matrix_power", stdin_data)
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: Matrix Power run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 8. Factorial Combinatorics (22 runs) ──
    for i in range(22):
        test_idx += 1
        p = 1000000007
        n = random.randint(0, 10000)
        k = random.randint(0, n)
        expected_str = str(combinations_mod_p(n, k, p))

        out = compile_and_run("nt_combinatorics_factorials", f"{n} {k} {p}")
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: Combinatorics run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 9. Lucas' Theorem (22 runs) ──
    for i in range(22):
        test_idx += 1
        p = random.choice(SMALL_PRIMES[1:10])  # small prime
        n = random.randint(0, 10**9)
        k = random.randint(0, n)
        expected_str = str(lucas_theorem(n, k, p))

        out = compile_and_run("nt_lucas_theorem", f"{n} {k} {p}")
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: Lucas run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 10. Deterministic Miller-Rabin Primality (22 runs) ──
    test_cases_mr = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79,
        561, 1105, 1729, 2465, 2821, 8911,  # Carmichael numbers
        1000000007, 1000000009, 1000000011, 1000000021, 1000000033,
        999999999999999989, 4611686014132420609, 18446744073709551557
    ]
    for i in range(22):
        test_idx += 1
        if i < len(test_cases_mr):
            n = test_cases_mr[i]
        else:
            n = random.randint(1, 2**60)

        is_pr = miller_rabin_deterministic(n)
        expected_str = "PRIME" if is_pr else "COMPOSITE"

        out = compile_and_run("nt_miller_rabin", str(n))
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: Miller-Rabin run {i+1} (n={n}): expected '{expected_str}', got '{out}'")

    print("=" * 80)
    print(f"Stress Test Results: {total_passed}/{total_tests} Passed ({(total_passed/total_tests)*100:.1f}%)")
    print("=" * 80)
    return total_passed == total_tests


if __name__ == "__main__":
    success = run_stress_tests()
    sys.exit(0 if success else 1)
