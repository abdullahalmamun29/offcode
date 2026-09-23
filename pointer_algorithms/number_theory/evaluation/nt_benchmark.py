"""
CHUP Phase 3P — Number Theory & Combinatorics Benchmark Suite.

Evaluates recognition, structural derivation, invariant construction,
code generation, and C++17 execution across all 10 Phase 3P patterns (60 problems total):

3P-A: Extended Euclidean & Linear Diophantine (NT-01..NT-06)
3P-B: Modular Multiplicative Inverse (NT-07..NT-12)
3P-C: Chinese Remainder Theorem (NT-13..NT-18)
3P-D: Euler Linear Sieve & SPF Factorization (NT-19..NT-24)
3P-E: Euler's Totient Function (NT-25..NT-30)
3P-F: Möbius Inversion & Multiplicative Transforms (NT-31..NT-36)
3P-G: Matrix Exponentiation & Linear Recurrences (NT-37..NT-42)
3P-H: Factorial Combinatorics (nCr mod p, N < p) (NT-43..NT-48)
3P-I: Lucas' Theorem (Large nCr mod p, prime p) (NT-49..NT-54)
3P-J: Deterministic Miller-Rabin Primality Test (NT-55..NT-60)
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
from pointer_algorithms.number_theory.verification.nt_oracles import (
    extended_gcd,
    solve_diophantine,
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


BENCHMARK_PROBLEMS = [
    # ── 3P-A: Extended GCD & Linear Diophantine (NT-01..NT-06) ──
    {
        "id": "NT-01",
        "category": "3P-A",
        "title": "Extended Euclidean Algorithm Standard",
        "text": "Find integer solution to a*x + b*y = c using extended Euclidean algorithm and Bezout coefficients.",
        "expected_pattern": "nt_extended_gcd",
        "input": "15 25 5",
        "validator": lambda out: out.strip() == "2 -1 5"
    },
    {
        "id": "NT-02",
        "category": "3P-A",
        "title": "Linear Diophantine Equation Impossible",
        "text": "Solve linear Diophantine equation a*x + b*y = c using extended GCD algorithm.",
        "expected_pattern": "nt_extended_gcd",
        "input": "6 9 7",
        "validator": lambda out: out.strip() == "IMPOSSIBLE"
    },
    {
        "id": "NT-03",
        "category": "3P-A",
        "title": "Extended GCD Coprime Coefficients",
        "text": "Compute Bezout identity coefficients x and y such that a*x + b*y = gcd(a, b) using extended GCD.",
        "expected_pattern": "nt_extended_gcd",
        "input": "101 103 1",
        "validator": lambda out: out.strip() == "51 -50 1"
    },
    {
        "id": "NT-04",
        "category": "3P-A",
        "title": "Linear Diophantine Multiple of GCD",
        "text": "Find particular solution to linear Diophantine equation a*x + b*y = c via extended Euclidean algorithm.",
        "expected_pattern": "nt_extended_gcd",
        "input": "35 15 10",
        "validator": lambda out: out.strip() == "2 -4 5"
    },
    {
        "id": "NT-05",
        "category": "3P-A",
        "title": "Extended GCD Zero First Coefficient",
        "text": "Solve a*x + b*y = c using extended GCD when one coefficient is zero.",
        "expected_pattern": "nt_extended_gcd",
        "input": "0 5 15",
        "validator": lambda out: out.strip() == "0 3 5"
    },
    {
        "id": "NT-06",
        "category": "3P-A",
        "title": "Extended GCD Homogeneous Equation",
        "text": "Find Bezout representation for linear Diophantine equation with c = 0 using extended Euclidean.",
        "expected_pattern": "nt_extended_gcd",
        "input": "14 21 0",
        "validator": lambda out: out.strip() == "0 0 7"
    },

    # ── 3P-B: Modular Multiplicative Inverse (NT-07..NT-12) ──
    {
        "id": "NT-07",
        "category": "3P-B",
        "title": "Modular Multiplicative Inverse Prime Modulus",
        "text": "Find modular multiplicative inverse of a modulo m using extended Euclidean algorithm.",
        "expected_pattern": "nt_modular_inverse",
        "input": "3 11",
        "validator": lambda out: out.strip() == "4"
    },
    {
        "id": "NT-08",
        "category": "3P-B",
        "title": "Modular Inverse Non-Coprime Failure",
        "text": "Compute modular inverse of a modulo m or detect that inverse modulo does not exist.",
        "expected_pattern": "nt_modular_inverse",
        "input": "6 9",
        "validator": lambda out: out.strip() == "-1"
    },
    {
        "id": "NT-09",
        "category": "3P-B",
        "title": "Modular Multiplicative Inverse Composite Modulus",
        "text": "Compute a^(-1) mod m where m is composite and coprime to a using extended GCD modular inverse.",
        "expected_pattern": "nt_modular_inverse",
        "input": "10 17",
        "validator": lambda out: out.strip() == "12"
    },
    {
        "id": "NT-10",
        "category": "3P-B",
        "title": "Modular Inverse Large Prime Modulus",
        "text": "Find modular inverse of a modulo large prime 10^9+7 using modular multiplicative inverse.",
        "expected_pattern": "nt_modular_inverse",
        "input": "7 1000000007",
        "validator": lambda out: out.strip() == str(modular_inverse(7, 1000000007))
    },
    {
        "id": "NT-11",
        "category": "3P-B",
        "title": "Modular Inverse Shared Factor",
        "text": "Determine modular multiplicative inverse of a mod m or return -1 when gcd(a, m) > 1.",
        "expected_pattern": "nt_modular_inverse",
        "input": "15 25",
        "validator": lambda out: out.strip() == "-1"
    },
    {
        "id": "NT-12",
        "category": "3P-B",
        "title": "Modular Inverse Modulus Equal to 2",
        "text": "Find modular inverse of odd number modulo 2 using extended GCD modular inverse.",
        "expected_pattern": "nt_modular_inverse",
        "input": "1 2",
        "validator": lambda out: out.strip() == "1"
    },

    # ── 3P-C: Chinese Remainder Theorem (NT-13..NT-18) ──
    {
        "id": "NT-13",
        "category": "3P-C",
        "title": "Chinese Remainder Theorem Coprime Pair",
        "text": "Solve system of modular congruences using Chinese Remainder Theorem CRT.",
        "expected_pattern": "nt_chinese_remainder",
        "input": "2\n2 3\n3 5",
        "validator": lambda out: out.strip() == "8"
    },
    {
        "id": "NT-14",
        "category": "3P-C",
        "title": "Chinese Remainder Theorem Three Congruences",
        "text": "Find simultaneous congruences solution using Chinese Remainder Theorem CRT with pairwise coprime moduli.",
        "expected_pattern": "nt_chinese_remainder",
        "input": "3\n2 3\n3 5\n2 7",
        "validator": lambda out: out.strip() == "23"
    },
    {
        "id": "NT-15",
        "category": "3P-C",
        "title": "Chinese Remainder Non-Coprime Solvable",
        "text": "Solve system of congruences with non-coprime moduli using extended CRT algorithm.",
        "expected_pattern": "nt_chinese_remainder",
        "input": "2\n2 4\n4 6",
        "validator": lambda out: out.strip() == "10"
    },
    {
        "id": "NT-16",
        "category": "3P-C",
        "title": "Chinese Remainder Non-Coprime Incompatible",
        "text": "Detect incompatible system of modular congruences where CRT has no solution.",
        "expected_pattern": "nt_chinese_remainder",
        "input": "2\n1 4\n2 6",
        "validator": lambda out: out.strip() == "-1"
    },
    {
        "id": "NT-17",
        "category": "3P-C",
        "title": "Chinese Remainder Large Moduli",
        "text": "Solve system of modular congruences with large 30-bit moduli using Chinese Remainder Theorem CRT.",
        "expected_pattern": "nt_chinese_remainder",
        "input": "2\n3 1000000007\n5 1000000009",
        "validator": lambda out: out.strip() == str(chinese_remainder([(3, 1000000007), (5, 1000000009)])[0])
    },
    {
        "id": "NT-18",
        "category": "3P-C",
        "title": "Chinese Remainder Single Congruence",
        "text": "Evaluate trivial system of one congruence using Chinese Remainder Theorem CRT.",
        "expected_pattern": "nt_chinese_remainder",
        "input": "1\n5 13",
        "validator": lambda out: out.strip() == "5"
    },

    # ── 3P-D: Euler Linear Sieve & SPF (NT-19..NT-24) ──
    {
        "id": "NT-19",
        "category": "3P-D",
        "title": "Linear Sieve Small Bound",
        "text": "Precompute all prime numbers up to N in linear time using Euler linear sieve.",
        "expected_pattern": "nt_linear_sieve",
        "input": "10",
        "validator": lambda out: out.strip() == "4"
    },
    {
        "id": "NT-20",
        "category": "3P-D",
        "title": "Linear Sieve Up To 20",
        "text": "Compute smallest prime factor and list of primes up to N using Euler linear sieve.",
        "expected_pattern": "nt_linear_sieve",
        "input": "20",
        "validator": lambda out: out.strip() == "8"
    },
    {
        "id": "NT-21",
        "category": "3P-D",
        "title": "Linear Sieve Up To 100",
        "text": "Find prime count up to 100 using linear sieve algorithm with smallest prime factor spf table.",
        "expected_pattern": "nt_linear_sieve",
        "input": "100",
        "validator": lambda out: out.strip() == "25"
    },
    {
        "id": "NT-22",
        "category": "3P-D",
        "title": "Linear Sieve Up To 1000",
        "text": "Run Euler linear sieve to find number of primes up to 1000.",
        "expected_pattern": "nt_linear_sieve",
        "input": "1000",
        "validator": lambda out: out.strip() == "168"
    },
    {
        "id": "NT-23",
        "category": "3P-D",
        "title": "Linear Sieve Minimum Prime Boundary",
        "text": "Count primes up to N = 2 using linear sieve algorithm.",
        "expected_pattern": "nt_linear_sieve",
        "input": "2",
        "validator": lambda out: out.strip() == "1"
    },
    {
        "id": "NT-24",
        "category": "3P-D",
        "title": "Linear Sieve Up To 100000",
        "text": "Compute primes and spf table up to 100000 using linear sieve.",
        "expected_pattern": "nt_linear_sieve",
        "input": "100000",
        "validator": lambda out: out.strip() == "9592"
    },

    # ── 3P-E: Euler's Totient Function (NT-25..NT-30) ──
    {
        "id": "NT-25",
        "category": "3P-E",
        "title": "Euler Totient Unit Value",
        "text": "Compute Euler's totient phi function for N = 1.",
        "expected_pattern": "nt_euler_totient",
        "input": "1",
        "validator": lambda out: out.strip() == "1"
    },
    {
        "id": "NT-26",
        "category": "3P-E",
        "title": "Euler Totient Prime Power",
        "text": "Calculate Euler totient phi(n) for prime square 9.",
        "expected_pattern": "nt_euler_totient",
        "input": "9",
        "validator": lambda out: out.strip() == "6"
    },
    {
        "id": "NT-27",
        "category": "3P-E",
        "title": "Euler Totient Composite Number",
        "text": "Evaluate Euler's totient function phi(n) for composite integer 12.",
        "expected_pattern": "nt_euler_totient",
        "input": "12",
        "validator": lambda out: out.strip() == "4"
    },
    {
        "id": "NT-28",
        "category": "3P-E",
        "title": "Euler Totient Highly Composite",
        "text": "Compute Euler totient phi(n) count of coprime residues up to 36.",
        "expected_pattern": "nt_euler_totient",
        "input": "36",
        "validator": lambda out: out.strip() == "12"
    },
    {
        "id": "NT-29",
        "category": "3P-E",
        "title": "Euler Totient Prime Value",
        "text": "Calculate Euler totient function phi(n) for prime number 97.",
        "expected_pattern": "nt_euler_totient",
        "input": "97",
        "validator": lambda out: out.strip() == "96"
    },
    {
        "id": "NT-30",
        "category": "3P-E",
        "title": "Euler Totient Large Prime",
        "text": "Compute Euler's totient phi function for 1000000007.",
        "expected_pattern": "nt_euler_totient",
        "input": "1000000007",
        "validator": lambda out: out.strip() == "1000000006"
    },

    # ── 3P-F: Möbius Inversion & Multiplicative Transforms (NT-31..NT-36) ──
    {
        "id": "NT-31",
        "category": "3P-F",
        "title": "Möbius Inversion Coprime Grid 3x3",
        "text": "Count coprime pairs in grid gcd(i, j) == 1 using Mobius inversion.",
        "expected_pattern": "nt_mobius_inversion",
        "input": "3 3",
        "validator": lambda out: out.strip() == "7"
    },
    {
        "id": "NT-32",
        "category": "3P-F",
        "title": "Möbius Inversion Coprime Grid 4x4",
        "text": "Calculate number of pairs with gcd(i, j) == 1 up to 4 using Mobius inversion and square-free parity.",
        "expected_pattern": "nt_mobius_inversion",
        "input": "4 4",
        "validator": lambda out: out.strip() == "11"
    },
    {
        "id": "NT-33",
        "category": "3P-F",
        "title": "Möbius Inversion Degenerate Grid",
        "text": "Find coprime pairs in grid 1 by 10 using Mobius inversion transform.",
        "expected_pattern": "nt_mobius_inversion",
        "input": "1 10",
        "validator": lambda out: out.strip() == "10"
    },
    {
        "id": "NT-34",
        "category": "3P-F",
        "title": "Möbius Inversion Grid 5x5",
        "text": "Count coprime pairs in grid 5 by 5 with gcd(i, j) == 1 via Mobius inversion sum.",
        "expected_pattern": "nt_mobius_inversion",
        "input": "5 5",
        "validator": lambda out: out.strip() == "19"
    },
    {
        "id": "NT-35",
        "category": "3P-F",
        "title": "Möbius Inversion Grid 10x10",
        "text": "Count coprime pairs in grid 10 by 10 using Mobius inversion mu function.",
        "expected_pattern": "nt_mobius_inversion",
        "input": "10 10",
        "validator": lambda out: out.strip() == "63"
    },
    {
        "id": "NT-36",
        "category": "3P-F",
        "title": "Möbius Inversion Grid 100x100",
        "text": "Compute total coprime pairs in grid up to 100 using Mobius inversion.",
        "expected_pattern": "nt_mobius_inversion",
        "input": "100 100",
        "validator": lambda out: out.strip() == "6087"
    },

    # ── 3P-G: Matrix Exponentiation & Linear Recurrences (NT-37..NT-42) ──
    {
        "id": "NT-37",
        "category": "3P-G",
        "title": "Matrix Exponentiation Fibonacci Recurrence",
        "text": "Compute n-th term of linear recurrence using transition matrix exponentiation.",
        "expected_pattern": "nt_matrix_power",
        "input": "2 5 1000000007\n1 1\n1 0",
        "validator": lambda out: out.strip() == "8 5\n5 3"
    },
    {
        "id": "NT-38",
        "category": "3P-G",
        "title": "Matrix Power Identity Matrix",
        "text": "Raise identity transition matrix to power k using matrix power algorithm.",
        "expected_pattern": "nt_matrix_power",
        "input": "2 10 1000000007\n1 0\n0 1",
        "validator": lambda out: out.strip() == "1 0\n0 1"
    },
    {
        "id": "NT-39",
        "category": "3P-G",
        "title": "Matrix Power Zero Exponent",
        "text": "Compute matrix exponentiation with power k = 0 modulo 1000000007.",
        "expected_pattern": "nt_matrix_power",
        "input": "2 0 1000000007\n2 3\n4 5",
        "validator": lambda out: out.strip() == "1 0\n0 1"
    },
    {
        "id": "NT-40",
        "category": "3P-G",
        "title": "Matrix Exponentiation 3x3 Nilpotent",
        "text": "Compute power of 3x3 transition matrix using matrix exponentiation.",
        "expected_pattern": "nt_matrix_power",
        "input": "3 3 1000000007\n1 1 0\n0 1 1\n0 0 1",
        "validator": lambda out: out.strip() == "1 3 3\n0 1 3\n0 0 1"
    },
    {
        "id": "NT-41",
        "category": "3P-G",
        "title": "Matrix Exponentiation Large Exponent",
        "text": "Compute fast Fibonacci in log time using 2x2 matrix exponentiation to 10^9 modulo 1000000007.",
        "expected_pattern": "nt_matrix_power",
        "input": "2 1000000000 1000000007\n1 1\n1 0",
        "validator": lambda out: out.strip() == "999999994 21\n21 999999973"
    },
    {
        "id": "NT-42",
        "category": "3P-G",
        "title": "Matrix Power Small Prime Modulus",
        "text": "Evaluate matrix power for linear recurrence with matrix modulo 7.",
        "expected_pattern": "nt_matrix_power",
        "input": "2 4 7\n1 2\n3 4",
        "validator": lambda out: out.strip() == "3 3\n1 4"
    },

    # ── 3P-H: Factorial Combinatorics (NT-43..NT-48) ──
    {
        "id": "NT-43",
        "category": "3P-H",
        "title": "Binomial Coefficient Standard 5 Choose 2",
        "text": "Calculate binomial coefficient n choose k modulo 1000000007 using factorials and inverse factorials.",
        "expected_pattern": "nt_combinatorics_factorials",
        "input": "5 2 1000000007",
        "validator": lambda out: out.strip() == "10"
    },
    {
        "id": "NT-44",
        "category": "3P-H",
        "title": "Binomial Coefficient 10 Choose 3",
        "text": "Compute combinations nCr modulo prime p using factorials and inverse factorials table.",
        "expected_pattern": "nt_combinatorics_factorials",
        "input": "10 3 1000000007",
        "validator": lambda out: out.strip() == "120"
    },
    {
        "id": "NT-45",
        "category": "3P-H",
        "title": "Binomial Coefficient Boundary K = 0",
        "text": "Evaluate binomial coefficient n choose 0 modulo prime p using factorials and inverse factorials.",
        "expected_pattern": "nt_combinatorics_factorials",
        "input": "100 0 1000000007",
        "validator": lambda out: out.strip() == "1"
    },
    {
        "id": "NT-46",
        "category": "3P-H",
        "title": "Binomial Coefficient Boundary K = N",
        "text": "Compute combinations nCr for N = K modulo prime p using factorials and inverse factorials.",
        "expected_pattern": "nt_combinatorics_factorials",
        "input": "50 50 1000000007",
        "validator": lambda out: out.strip() == "1"
    },
    {
        "id": "NT-47",
        "category": "3P-H",
        "title": "Binomial Coefficient Large N 1000 Choose 500",
        "text": "Compute binomial coefficient 1000 choose 500 modulo prime 10^9+7 using factorials and inverse factorials.",
        "expected_pattern": "nt_combinatorics_factorials",
        "input": "1000 500 1000000007",
        "validator": lambda out: out.strip() == str(combinations_mod_p(1000, 500, 1000000007))
    },
    {
        "id": "NT-48",
        "category": "3P-H",
        "title": "Binomial Coefficient Modulo NTT Prime",
        "text": "Calculate combinations nCr modulo 998244353 using factorials and inverse factorials.",
        "expected_pattern": "nt_combinatorics_factorials",
        "input": "20 10 998244353",
        "validator": lambda out: out.strip() == "184756"
    },

    # ── 3P-I: Lucas' Theorem (NT-49..NT-54) ──
    {
        "id": "NT-49",
        "category": "3P-I",
        "title": "Lucas Theorem Small Base Zero",
        "text": "Compute nCr mod p for large n and k with small prime p using Lucas theorem.",
        "expected_pattern": "nt_lucas_theorem",
        "input": "10 2 3",
        "validator": lambda out: out.strip() == "0"
    },
    {
        "id": "NT-50",
        "category": "3P-I",
        "title": "Lucas Theorem Modulo 13",
        "text": "Compute binomial coefficient n choose k modulo small prime p using Lucas theorem.",
        "expected_pattern": "nt_lucas_theorem",
        "input": "10 2 13",
        "validator": lambda out: out.strip() == "6"
    },
    {
        "id": "NT-51",
        "category": "3P-I",
        "title": "Lucas Theorem Huge N and K 10^18",
        "text": "Compute large combinations with n and k up to 10^18 modulo prime 7 using Lucas theorem.",
        "expected_pattern": "nt_lucas_theorem",
        "input": "1000000000000000000 500000000000000000 7",
        "validator": lambda out: out.strip() == str(lucas_theorem(1000000000000000000, 500000000000000000, 7))
    },
    {
        "id": "NT-52",
        "category": "3P-I",
        "title": "Lucas Theorem Parity Modulo 2",
        "text": "Compute nCr mod p modulo 2 for arbitrary n and k using Lucas theorem.",
        "expected_pattern": "nt_lucas_theorem",
        "input": "5 5 2",
        "validator": lambda out: out.strip() == "1"
    },
    {
        "id": "NT-53",
        "category": "3P-I",
        "title": "Lucas Theorem Digit Carry Zero",
        "text": "Evaluate binomial coefficient n choose k mod p using Lucas theorem where p = 5.",
        "expected_pattern": "nt_lucas_theorem",
        "input": "12 4 5",
        "validator": lambda out: out.strip() == "0"
    },
    {
        "id": "NT-54",
        "category": "3P-I",
        "title": "Lucas Theorem Modulo 11",
        "text": "Compute combinations nCr mod p with n > p using Lucas theorem.",
        "expected_pattern": "nt_lucas_theorem",
        "input": "27 9 11",
        "validator": lambda out: out.strip() == str(lucas_theorem(27, 9, 11))
    },

    # ── 3P-J: Miller-Rabin Primality Test (NT-55..NT-60) ──
    {
        "id": "NT-55",
        "category": "3P-J",
        "title": "Miller-Rabin Smallest Prime 2",
        "text": "Check if number is prime using deterministic Miller-Rabin primality test.",
        "expected_pattern": "nt_miller_rabin",
        "input": "2",
        "validator": lambda out: out.strip() == "PRIME"
    },
    {
        "id": "NT-56",
        "category": "3P-J",
        "title": "Miller-Rabin Non-Prime One",
        "text": "Check if number is prime for N = 1 using Miller-Rabin primality test.",
        "expected_pattern": "nt_miller_rabin",
        "input": "1",
        "validator": lambda out: out.strip() == "COMPOSITE"
    },
    {
        "id": "NT-57",
        "category": "3P-J",
        "title": "Miller-Rabin Standard Large Prime",
        "text": "Verify 64-bit prime testing for 1000000007 using deterministic Miller-Rabin.",
        "expected_pattern": "nt_miller_rabin",
        "input": "1000000007",
        "validator": lambda out: out.strip() == "PRIME"
    },
    {
        "id": "NT-58",
        "category": "3P-J",
        "title": "Miller-Rabin Twin Prime Companion",
        "text": "Check if prime number 1000000009 is prime using Miller-Rabin primality test.",
        "expected_pattern": "nt_miller_rabin",
        "input": "1000000009",
        "validator": lambda out: out.strip() == "PRIME"
    },
    {
        "id": "NT-59",
        "category": "3P-J",
        "title": "Miller-Rabin Semiprime Composite",
        "text": "Check if number is prime for composite 1000000011 using Miller-Rabin primality test.",
        "expected_pattern": "nt_miller_rabin",
        "input": "1000000011",
        "validator": lambda out: out.strip() == "COMPOSITE"
    },
    {
        "id": "NT-60",
        "category": "3P-J",
        "title": "Miller-Rabin Carmichael Number",
        "text": "Detect composite Carmichael pseudoprime 561 using deterministic 7-witness Miller-Rabin primality test.",
        "expected_pattern": "nt_miller_rabin",
        "input": "561",
        "validator": lambda out: out.strip() == "COMPOSITE"
    }
]


def run_benchmark() -> bool:
    print("=" * 80)
    print("CHUP Phase 3P — Number Theory & Combinatorics Benchmark Suite (60 Problems)")
    print("=" * 80)

    total = len(BENCHMARK_PROBLEMS)
    passed = 0
    failed = 0

    for prob in BENCHMARK_PROBLEMS:
        pid = prob["id"]
        cat = prob["category"]
        title = prob["title"]
        text = prob["text"]
        expected_pat = prob["expected_pattern"]
        stdin_data = prob["input"]

        # 1. Pipeline Recognition
        response = handle_request({"problemText": text})
        actual_pat = response.get("selectedPattern")
        family = response.get("family")

        if actual_pat != expected_pat:
            failed += 1
            print(f"[{cat}] {pid} FAIL: Recognition mismatch: expected '{expected_pat}', got '{actual_pat}' ({title})")
            continue

        if family != "number_theory":
            failed += 1
            print(f"[{cat}] {pid} FAIL: Family mismatch: expected 'number_theory', got '{family}' ({title})")
            continue

        # 2. C++ Generation & Execution
        cpp_code = response.get("code", "")
        if not cpp_code:
            failed += 1
            print(f"[{cat}] {pid} FAIL: Missing C++ code in response ({title})")
            continue

        cpp_output = compile_and_run_cpp(cpp_code, stdin_data)
        if cpp_output.startswith("COMPILE_ERROR") or cpp_output.startswith("RUNTIME_ERROR"):
            failed += 1
            print(f"[{cat}] {pid} FAIL: Execution error: {cpp_output} ({title})")
            continue

        # 3. Output Validation
        validator = prob.get("validator")
        if validator and validator(cpp_output):
            passed += 1
            print(f"[{cat}] {pid} PASS: {title} (Pattern={expected_pat})")
        else:
            failed += 1
            print(f"[{cat}] {pid} FAIL: Output validation failed: got '{cpp_output}' ({title})")

    print("=" * 80)
    print(f"Benchmark Results: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("=" * 80)
    return passed == total


if __name__ == "__main__":
    success = run_benchmark()
    sys.exit(0 if success else 1)
