"""
CHUP Phase 3Q — Algebra / Transforms Randomized Differential Stress Test Suite.

Differential randomized stress testing comparing compiled C++ implementations
against independent reference oracles across 220 randomized test instances:
1. algebra_fft vs FFT Oracle (22 runs)
2. algebra_ntt vs NTT Oracle (22 runs)
3. algebra_fwht vs FWHT XOR Oracle (22 runs)
4. algebra_poly_inverse vs Polynomial Inverse Oracle (22 runs)
5. algebra_gauss_real vs Real Gaussian Elimination Oracle (22 runs)
6. algebra_gauss_modular vs Modular Gaussian Elimination Oracle (22 runs)
7. algebra_gauss_xor vs XOR Gaussian Elimination Oracle (22 runs)
8. algebra_linear_basis vs XOR Linear Basis Oracle (22 runs)
9. algebra_berlekamp_massey vs Berlekamp-Massey Recurrence Oracle (22 runs)
10. algebra_lagrange_interpolation vs Lagrange Interpolation Oracle (22 runs)

Total: 220 test cases.
"""

import sys
import os
import random
import subprocess
import tempfile
import hashlib
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.algebra.derivation_engine import AlgebraDerivationEngine
from pointer_algorithms.algebra.verification.algebra_oracles import (
    fft_oracle,
    ntt_oracle,
    fwht_xor_oracle,
    poly_inverse_oracle,
    gauss_real_oracle,
    gauss_modular_oracle,
    gauss_xor_oracle,
    linear_basis_xor_oracle,
    linear_recurrence_eval_oracle,
    lagrange_eval_oracle
)

COMPILED_BINARIES: Dict[str, str] = {}
ENGINE = AlgebraDerivationEngine()


def compile_and_run(pattern: str, stdin_data: str, timeout: int = 10) -> str:
    code = ENGINE.generate_cpp_solution(pattern)
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


def run_stress_tests():
    random.seed(1337)
    total_passed = 0
    total_tests = 220
    test_idx = 0

    print("=" * 80)
    print("CHUP Phase 3Q — Algebra / Transforms Randomized Stress Tests (220 Cases)")
    print("=" * 80)

    # ── 1. Fast Fourier Transform (22 runs) ──
    for i in range(22):
        test_idx += 1
        n1 = random.randint(1, 16)
        n2 = random.randint(1, 16)
        a = [random.randint(-10, 10) for _ in range(n1)]
        b = [random.randint(-10, 10) for _ in range(n2)]
        expected = fft_oracle(a, b)
        expected_str = " ".join(map(str, expected))

        stdin_data = f"{n1} {n2}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b))
        out = compile_and_run("algebra_fft", stdin_data)
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: FFT run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 2. Number Theoretic Transform (22 runs) ──
    for i in range(22):
        test_idx += 1
        n1 = random.randint(1, 32)
        n2 = random.randint(1, 32)
        a = [random.randint(0, 1000) for _ in range(n1)]
        b = [random.randint(0, 1000) for _ in range(n2)]
        expected = ntt_oracle(a, b)
        expected_str = " ".join(map(str, expected))

        stdin_data = f"{n1} {n2}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b))
        out = compile_and_run("algebra_ntt", stdin_data)
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: NTT run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 3. Fast Walsh-Hadamard Transform (22 runs) ──
    for i in range(22):
        test_idx += 1
        dim = random.randint(0, 4)
        n = 1 << dim
        a = [random.randint(0, 50) for _ in range(n)]
        b = [random.randint(0, 50) for _ in range(n)]
        expected = fwht_xor_oracle(a, b)
        expected_str = " ".join(map(str, expected))

        stdin_data = f"{dim}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b))
        out = compile_and_run("algebra_fwht", stdin_data)
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: FWHT run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 4. Polynomial Inversion (22 runs) ──
    for i in range(22):
        test_idx += 1
        n = random.randint(1, 25)
        # a[0] must be non-zero (invertible unit)
        a = [random.randint(1, 100)] + [random.randint(0, 100) for _ in range(n - 1)]
        expected = poly_inverse_oracle(a, n)
        expected_str = " ".join(map(str, expected))

        stdin_data = f"{n}\n" + " ".join(map(str, a))
        out = compile_and_run("algebra_poly_inverse", stdin_data)
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: PolyInv run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 5. Real Gaussian Elimination (22 runs) ──
    for i in range(22):
        test_idx += 1
        n = random.randint(2, 4)
        if i % 4 == 0:
            # Inconsistent system: duplicate row with different constant
            row = [random.randint(1, 5) for _ in range(n)]
            A = [row[:] for _ in range(n)]
            b = [1] + [2] * (n - 1)
        elif i % 4 == 1:
            # Infinite solutions: all zero row
            A = [[random.randint(-5, 5) for _ in range(n)] for _ in range(n - 1)] + [[0] * n]
            b = [random.randint(-5, 5) for _ in range(n - 1)] + [0]
        else:
            # Unique solution
            A = [[random.randint(-5, 5) for _ in range(n)] for _ in range(n)]
            for r in range(n):
                A[r][r] += 15  # diagonally dominant ensures invertible
            sol_true = [random.randint(-5, 5) for _ in range(n)]
            b = [sum(A[r][c] * sol_true[c] for c in range(n)) for r in range(n)]

        status, sol, rank, _ = gauss_real_oracle(A, b)
        if status == "UNIQUE_SOLUTION":
            clean_sol = [0.0 if abs(x) < 1e-9 else x for x in sol]
            expected_str = "UNIQUE_SOLUTION\n" + " ".join(f"{x:.6f}" for x in clean_sol)
        elif status == "INCONSISTENT":
            expected_str = "INCONSISTENT"
        else:
            expected_str = "INFINITE_SOLUTIONS"

        stdin_data = f"{n}\n" + "\n".join(" ".join(map(str, A[r] + [b[r]])) for r in range(n))
        out = compile_and_run("algebra_gauss_real", stdin_data)
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: GaussReal run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 6. Modular Gaussian Elimination (22 runs) ──
    for i in range(22):
        test_idx += 1
        n = random.randint(2, 4)
        mod = 998244353
        if i % 4 == 0:
            # Inconsistent
            row = [random.randint(1, 5) for _ in range(n)]
            A = [row[:] for _ in range(n)]
            b = [1] + [2] * (n - 1)
        elif i % 4 == 1:
            # Infinite
            A = [[random.randint(0, 5) for _ in range(n)] for _ in range(n - 1)] + [[0] * n]
            b = [random.randint(0, 5) for _ in range(n - 1)] + [0]
        else:
            # Unique
            A = [[random.randint(0, 10) for _ in range(n)] for _ in range(n)]
            for r in range(n):
                A[r][r] += 20
            sol_true = [random.randint(0, 10) for _ in range(n)]
            b = [sum(A[r][c] * sol_true[c] for c in range(n)) % mod for r in range(n)]

        status, sol, rank, _ = gauss_modular_oracle(A, b, mod)
        if status == "UNIQUE_SOLUTION":
            expected_str = "UNIQUE_SOLUTION\n" + " ".join(map(str, sol))
        elif status == "INCONSISTENT":
            expected_str = "INCONSISTENT"
        else:
            expected_str = "INFINITE_SOLUTIONS"

        stdin_data = f"{n}\n" + "\n".join(" ".join(map(str, A[r] + [b[r]])) for r in range(n))
        out = compile_and_run("algebra_gauss_modular", stdin_data)
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: GaussModular run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 7. XOR Gaussian Elimination (22 runs) ──
    for i in range(22):
        test_idx += 1
        n = random.randint(2, 4)
        m = n
        if i % 4 == 0:
            # Inconsistent
            row = [1] * m
            A = [row[:] for _ in range(n)]
            b = [0] + [1] * (n - 1)
        elif i % 4 == 1:
            # Infinite
            A = [[random.randint(0, 1) for _ in range(m)] for _ in range(n - 1)] + [[0] * m]
            b = [random.randint(0, 1) for _ in range(n - 1)] + [0]
        else:
            # Random
            A = [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]
            for r in range(n):
                A[r][r] = 1
            b = [random.randint(0, 1) for _ in range(n)]

        status, sol, rank = gauss_xor_oracle(A, b)
        if status == "UNIQUE_SOLUTION":
            expected_str = "UNIQUE_SOLUTION\n" + " ".join(map(str, sol))
        elif status == "INCONSISTENT":
            expected_str = "INCONSISTENT"
        else:
            expected_str = "INFINITE_SOLUTIONS"

        stdin_data = f"{n} {m}\n" + "\n".join(" ".join(map(str, A[r] + [b[r]])) for r in range(n))
        out = compile_and_run("algebra_gauss_xor", stdin_data)
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: GaussXOR run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 8. XOR Linear Basis (22 runs) ──
    for i in range(22):
        test_idx += 1
        n = random.randint(1, 20)
        vals = [random.randint(0, (1 << 30) - 1) for _ in range(n)]
        _, max_xor = linear_basis_xor_oracle(vals)
        expected_str = str(max_xor)

        stdin_data = f"{n}\n" + " ".join(map(str, vals))
        out = compile_and_run("algebra_linear_basis", stdin_data)
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: LinearBasis run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 9. Berlekamp-Massey & Linear Recurrence (22 runs) ──
    for i in range(22):
        test_idx += 1
        # Generate known recurrence: s_{n} = c1 s_{n-1} + c2 s_{n-2}
        k = random.randint(1, 3)
        c = [random.randint(1, 5) for _ in range(k)]
        s = [random.randint(1, 10) for _ in range(k)]
        for _ in range(2 * k + 4):
            nxt = sum(c[j] * s[-1 - j] for j in range(k)) % 998244353
            s.append(nxt)

        n_query = random.randint(0, 100)
        expected = linear_recurrence_eval_oracle(s, n_query)
        expected_str = str(expected)

        stdin_data = f"{len(s)} {n_query}\n" + " ".join(map(str, s))
        out = compile_and_run("algebra_berlekamp_massey", stdin_data)
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: BerlekampMassey run {i+1}: expected '{expected_str}', got '{out}'")

    # ── 10. Lagrange Interpolation (22 runs) ──
    for i in range(22):
        test_idx += 1
        d = random.randint(1, 5)
        k = d + 1
        x_pts = random.sample(range(1, 50), k)
        y_pts = [random.randint(0, 1000) for _ in range(k)]
        x_query = random.randint(51, 100)

        expected = lagrange_eval_oracle(x_pts, y_pts, x_query)
        expected_str = str(expected)

        stdin_data = f"{k} {x_query}\n" + "\n".join(f"{x_pts[j]} {y_pts[j]}" for j in range(k))
        out = compile_and_run("algebra_lagrange_interpolation", stdin_data)
        if out == expected_str:
            total_passed += 1
        else:
            print(f"[{test_idx}] FAIL: Lagrange run {i+1}: expected '{expected_str}', got '{out}'")

    print("=" * 80)
    print(f"Stress Test Results: {total_passed}/{total_tests} Passed ({total_passed/total_tests*100:.1f}%)")
    print("=" * 80)
    if total_passed < total_tests:
        sys.exit(1)


if __name__ == "__main__":
    run_stress_tests()
