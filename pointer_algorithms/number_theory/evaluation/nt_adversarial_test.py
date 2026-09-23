"""
CHUP Phase 3P — Number Theory & Combinatorics Adversarial Test Suite.

Contains 16 adversarial entrapment and extreme boundary test cases:
1. ADV-NT-01: "graph" lattice path narrative entrapment in Extended GCD
2. ADV-NT-02: "dynamic programming" state table narrative in Modular Inverse
3. ADV-NT-03: "hash table" remainder buckets narrative in CRT
4. ADV-NT-04: "tree" prime factorization narrative in Linear Sieve
5. ADV-NT-05: "greedy" coprime selection narrative in Euler's Totient
6. ADV-NT-06: "matrix" 2D grid cell narrative in Möbius Inversion
7. ADV-NT-07: "two pointers" sliding window narrative in Matrix Power recurrence
8. ADV-NT-08: "prefix sum" cumulative distribution narrative in Factorial Combinatorics
9. ADV-NT-09: "binary search" monotonic search narrative in Lucas' Theorem
10. ADV-NT-10: "randomized monte carlo" narrative in Deterministic Miller-Rabin
11. ADV-NT-11: Boundary N = 1 for Euler's Totient
12. ADV-NT-12: Boundary N = 1 for Miller-Rabin primality (COMPOSITE)
13. ADV-NT-13: Boundary N = 2 for Miller-Rabin primality (PRIME)
14. ADV-NT-14: Boundary K = 0 for Combinatorics Factorials
15. ADV-NT-15: Boundary N = K for Lucas' Theorem
16. ADV-NT-16: 64-bit composite boundary for Miller-Rabin
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


ADVERSARIAL_PROBLEMS = [
    {
        "id": "ADV-NT-01",
        "title": "Graph Lattice Narrative Entrapment in Extended GCD",
        "text": "In a 2D integer coordinate graph lattice, we need to find if there is an edge-hop vector reaching offset c from linear steps a and b. Solve the linear Diophantine equation a*x + b*y = c using extended Euclidean algorithm and Bezout coefficients.",
        "expected_pattern": "nt_extended_gcd",
        "input": "12 8 4",
        "validator": lambda out: out.strip() == "1 -1 4"
    },
    {
        "id": "ADV-NT-02",
        "title": "DP State Table Narrative in Modular Inverse",
        "text": "Consider a dynamic programming transition ring where states wrap modulo m. We want the inverse state operation satisfying a * x = 1 (mod m). Compute the modular multiplicative inverse via extended GCD algorithm.",
        "expected_pattern": "nt_modular_inverse",
        "input": "5 13",
        "validator": lambda out: out.strip() == "8"
    },
    {
        "id": "ADV-NT-03",
        "title": "Hash Table Remainder Buckets Narrative in CRT",
        "text": "A distributed hash table maps key records across partitioned modulus buckets where each partition gives a remainder r_i mod m_i. Reconstruct the global key index by solving the system of modular congruences using Chinese Remainder Theorem CRT.",
        "expected_pattern": "nt_chinese_remainder",
        "input": "2\n3 5\n4 7",
        "validator": lambda out: out.strip() == "18"
    },
    {
        "id": "ADV-NT-04",
        "title": "Tree Prime Factorization Narrative in Linear Sieve",
        "text": "Decompose numbers along a prime factorization tree structure. Precompute all prime factors and smallest prime factor spf up to N in linear time using Euler linear sieve.",
        "expected_pattern": "nt_linear_sieve",
        "input": "30",
        "validator": lambda out: out.strip() == "10"
    },
    {
        "id": "ADV-NT-05",
        "title": "Greedy Coprime Selection Narrative in Euler's Totient",
        "text": "In a greedy resource allocation model, pick items that share no common factors with capacity N. Determine the total count of coprime elements using Euler's totient phi function.",
        "expected_pattern": "nt_euler_totient",
        "input": "100",
        "validator": lambda out: out.strip() == "40"
    },
    {
        "id": "ADV-NT-06",
        "title": "Matrix Grid Cell Narrative in Möbius Inversion",
        "text": "In an N by M matrix grid of integers, count all coordinate pairs (i, j) that are mutually coprime with gcd(i, j) == 1 using Mobius inversion sum.",
        "expected_pattern": "nt_mobius_inversion",
        "input": "6 6",
        "validator": lambda out: out.strip() == "23"
    },
    {
        "id": "ADV-NT-07",
        "title": "Two Pointers Window Narrative in Matrix Power",
        "text": "A recurrence sliding window sequence is driven by a constant linear recurrence. Evaluate the k-th state vector in log time using transition matrix exponentiation.",
        "expected_pattern": "nt_matrix_power",
        "input": "2 3 1000000007\n1 1\n1 0",
        "validator": lambda out: out.strip() == "3 2\n2 1"
    },
    {
        "id": "ADV-NT-08",
        "title": "Prefix Sum Narrative in Factorial Combinatorics",
        "text": "Calculate cumulative prefix combinations for selecting k subsets out of n elements. Compute combinations nCr modulo prime 10^9+7 using factorials and inverse factorials.",
        "expected_pattern": "nt_combinatorics_factorials",
        "input": "15 5 1000000007",
        "validator": lambda out: out.strip() == "3003"
    },
    {
        "id": "ADV-NT-09",
        "title": "Binary Search Monotonic Narrative in Lucas' Theorem",
        "text": "In a combinatorial threshold problem over a massive search space where N and K reach 10^18, compute nCr mod p for small prime p using Lucas theorem.",
        "expected_pattern": "nt_lucas_theorem",
        "input": "100 20 13",
        "validator": lambda out: out.strip() == str(lucas_theorem(100, 20, 13))
    },
    {
        "id": "ADV-NT-10",
        "title": "Randomized Monte Carlo Narrative in Deterministic Miller-Rabin",
        "text": "Rather than probabilistic randomized Miller-Rabin sampling, verify 64-bit prime testing deterministically using the 7-witness basis deterministic Miller-Rabin primality test.",
        "expected_pattern": "nt_miller_rabin",
        "input": "999999999999999989",
        "validator": lambda out: out.strip() == ("PRIME" if miller_rabin_deterministic(999999999999999989) else "COMPOSITE")
    },
    {
        "id": "ADV-NT-11",
        "title": "Boundary N = 1 for Euler's Totient",
        "text": "Compute Euler's totient phi function for boundary case N = 1.",
        "expected_pattern": "nt_euler_totient",
        "input": "1",
        "validator": lambda out: out.strip() == "1"
    },
    {
        "id": "ADV-NT-12",
        "title": "Boundary N = 1 for Miller-Rabin Primality",
        "text": "Check if number is prime for N = 1 using Miller-Rabin primality test.",
        "expected_pattern": "nt_miller_rabin",
        "input": "1",
        "validator": lambda out: out.strip() == "COMPOSITE"
    },
    {
        "id": "ADV-NT-13",
        "title": "Boundary N = 2 for Miller-Rabin Primality",
        "text": "Check if number is prime for even prime N = 2 using Miller-Rabin primality test.",
        "expected_pattern": "nt_miller_rabin",
        "input": "2",
        "validator": lambda out: out.strip() == "PRIME"
    },
    {
        "id": "ADV-NT-14",
        "title": "Boundary K = 0 for Combinatorics Factorials",
        "text": "Compute binomial coefficient n choose 0 modulo prime 10^9+7 using factorials and inverse factorials.",
        "expected_pattern": "nt_combinatorics_factorials",
        "input": "42 0 1000000007",
        "validator": lambda out: out.strip() == "1"
    },
    {
        "id": "ADV-NT-15",
        "title": "Boundary N = K for Lucas' Theorem",
        "text": "Compute nCr mod p when N = K using Lucas theorem.",
        "expected_pattern": "nt_lucas_theorem",
        "input": "777 777 19",
        "validator": lambda out: out.strip() == "1"
    },
    {
        "id": "ADV-NT-16",
        "title": "Boundary Unsigned 64-bit Composite Exceeding 2^63-1 for Miller-Rabin",
        "text": "Check if large integer N exceeding 2^63-1 is prime using deterministic 7-witness Miller-Rabin primality test over the unsigned 64-bit domain.",
        "expected_pattern": "nt_miller_rabin",
        "input": "18446744073709551555",
        "validator": lambda out: out.strip() == "COMPOSITE"
    }
]


def run_adversarial_test() -> bool:
    print("=" * 80)
    print("CHUP Phase 3P — Number Theory & Combinatorics Adversarial Test Suite (16 Cases)")
    print("=" * 80)

    total = len(ADVERSARIAL_PROBLEMS)
    passed = 0
    failed = 0

    for prob in ADVERSARIAL_PROBLEMS:
        pid = prob["id"]
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
            print(f"{pid} FAIL: Recognition mismatch: expected '{expected_pat}', got '{actual_pat}' ({title})")
            continue

        if family != "number_theory":
            failed += 1
            print(f"{pid} FAIL: Family mismatch: expected 'number_theory', got '{family}' ({title})")
            continue

        # 2. C++ Generation & Execution
        cpp_code = response.get("code", "")
        if not cpp_code:
            failed += 1
            print(f"{pid} FAIL: Missing C++ code in response ({title})")
            continue

        cpp_output = compile_and_run_cpp(cpp_code, stdin_data)
        if cpp_output.startswith("COMPILE_ERROR") or cpp_output.startswith("RUNTIME_ERROR"):
            failed += 1
            print(f"{pid} FAIL: Execution error: {cpp_output} ({title})")
            continue

        # 3. Output Validation
        validator = prob.get("validator")
        if validator and validator(cpp_output):
            passed += 1
            print(f"{pid} PASS: {title} (Pattern={expected_pat})")
        else:
            failed += 1
            print(f"{pid} FAIL: Output validation failed: got '{cpp_output}' ({title})")

    print("=" * 80)
    print(f"Adversarial Results: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("=" * 80)
    return passed == total


if __name__ == "__main__":
    success = run_adversarial_test()
    sys.exit(0 if success else 1)
