"""
CHUP Phase 3P — Number Theory & Combinatorics Discrimination Holdout Evaluation.

Tests discrimination between Phase 3P number theory patterns and competing alternative families:
1. NT-D-01: Linear Diophantine Equation (Extended GCD vs Two Pointers) -> number_theory / nt_extended_gcd
2. NT-D-02: Modular Multiplicative Inverse (ExtGCD Mod Inverse vs Brute Force) -> number_theory / nt_modular_inverse
3. NT-D-03: System of Simultaneous Congruences (CRT vs Simulation) -> number_theory / nt_chinese_remainder
4. NT-D-04: Sieve Prime Factorization (Linear Sieve vs DP) -> number_theory / nt_linear_sieve
5. NT-D-05: Coprime Totient Counting (Euler Totient vs Brute Force) -> number_theory / nt_euler_totient
6. NT-D-06: 2D Grid Coprime Pairs (Möbius Inversion vs Nested Loop) -> number_theory / nt_mobius_inversion
7. NT-D-07: Fast Fibonacci / Linear Recurrence (Matrix Exponentiation vs Linear DP) -> number_theory / nt_matrix_power
8. NT-D-08: Binomial Coefficient Modulo Prime (Factorials vs Pascal DP) -> number_theory / nt_combinatorics_factorials
9. NT-D-09: Large Combinations Modulo Prime (Lucas' Theorem vs Pascal DP) -> number_theory / nt_lucas_theorem
10. NT-D-10: 64-bit Primality Testing (Miller-Rabin vs Trial Division) -> number_theory / nt_miller_rabin
11. NT-D-11: Shortest Path in Weighted Graph (Dijkstra vs Number Theory) -> graph / dijkstra
12. NT-D-12: Substring Pattern Matching (KMP vs Number Theory) -> string / string_kmp_search
"""

import sys
import os
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request

DISCRIMINATION_PROBLEMS = [
    {
        "id": "NT-D-01",
        "title": "Linear Diophantine Equation (Extended GCD)",
        "text": "Solve linear Diophantine equation a*x + b*y = c using extended Euclidean algorithm and Bezout coefficients.",
        "expected_family": "number_theory",
        "expected_pattern": "nt_extended_gcd"
    },
    {
        "id": "NT-D-02",
        "title": "Modular Multiplicative Inverse (Extended GCD)",
        "text": "Find modular multiplicative inverse of a modulo m using extended Euclidean algorithm.",
        "expected_family": "number_theory",
        "expected_pattern": "nt_modular_inverse"
    },
    {
        "id": "NT-D-03",
        "title": "System of Simultaneous Congruences (CRT)",
        "text": "Solve system of modular congruences using Chinese Remainder Theorem CRT.",
        "expected_family": "number_theory",
        "expected_pattern": "nt_chinese_remainder"
    },
    {
        "id": "NT-D-04",
        "title": "Linear Sieve Prime Factorization (Linear Sieve)",
        "text": "Precompute smallest prime factor spf and list of primes up to N in linear time using Euler linear sieve.",
        "expected_family": "number_theory",
        "expected_pattern": "nt_linear_sieve"
    },
    {
        "id": "NT-D-05",
        "title": "Coprime Totient Counting (Euler Totient)",
        "text": "Compute count of coprime integers up to N using Euler's totient phi function.",
        "expected_family": "number_theory",
        "expected_pattern": "nt_euler_totient"
    },
    {
        "id": "NT-D-06",
        "title": "2D Grid Coprime Pairs (Möbius Inversion)",
        "text": "Count coprime pairs in grid gcd(i, j) == 1 using Mobius inversion and square-free parity.",
        "expected_family": "number_theory",
        "expected_pattern": "nt_mobius_inversion"
    },
    {
        "id": "NT-D-07",
        "title": "Fast Linear Recurrence (Matrix Exponentiation)",
        "text": "Compute n-th term of linear recurrence in log time using transition matrix exponentiation.",
        "expected_family": "number_theory",
        "expected_pattern": "nt_matrix_power"
    },
    {
        "id": "NT-D-08",
        "title": "Binomial Coefficient Modulo Prime (Factorials)",
        "text": "Calculate combinations nCr modulo prime 10^9+7 using factorials and inverse factorials.",
        "expected_family": "number_theory",
        "expected_pattern": "nt_combinatorics_factorials"
    },
    {
        "id": "NT-D-09",
        "title": "Large Combinations Modulo Prime (Lucas Theorem)",
        "text": "Compute nCr mod p for large n and k with small prime p using Lucas theorem.",
        "expected_family": "number_theory",
        "expected_pattern": "nt_lucas_theorem"
    },
    {
        "id": "NT-D-10",
        "title": "64-bit Primality Testing (Miller-Rabin)",
        "text": "Determine if large 64-bit integer is prime using deterministic Miller-Rabin primality test.",
        "expected_family": "number_theory",
        "expected_pattern": "nt_miller_rabin"
    },
    {
        "id": "NT-D-11",
        "title": "Shortest Path in Weighted Graph (Dijkstra)",
        "text": "Find shortest path from single source vertex to all other vertices in non-negative weighted graph using Dijkstra algorithm with priority queue.",
        "expected_family": "graph",
        "expected_pattern": "graph_dijkstra"
    },
    {
        "id": "NT-D-12",
        "title": "Substring Pattern Matching (KMP Search)",
        "text": "Find all occurrences of a pattern in text using KMP prefix function pi table.",
        "expected_family": "string",
        "expected_pattern": "string_kmp_search"
    }
]


def run_discrimination_holdout() -> bool:
    print("=" * 80)
    print("CHUP Phase 3P — Number Theory & Combinatorics Discrimination Holdout Evaluation (12 Cases)")
    print("=" * 80)

    total = len(DISCRIMINATION_PROBLEMS)
    passed = 0
    failed = 0

    for prob in DISCRIMINATION_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]
        expected_family = prob["expected_family"]
        expected_pattern = prob["expected_pattern"]

        resp = handle_request({"problemText": text})
        actual_pat = resp.get("selectedPattern")
        actual_family = resp.get("family")

        pat_match = (actual_pat == expected_pattern)
        fam_match = (actual_family == expected_family)

        if pat_match and fam_match:
            passed += 1
            print(f"{pid} PASS: {title} -> {actual_family} / {actual_pat}")
        else:
            failed += 1
            print(f"{pid} FAIL: {title}")
            if not fam_match:
                print(f"   Family mismatch: expected '{expected_family}', got '{actual_family}'")
            if not pat_match:
                print(f"   Pattern mismatch: expected '{expected_pattern}', got '{actual_pat}'")

    print("=" * 80)
    print(f"Discrimination Results: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("=" * 80)
    return passed == total


if __name__ == "__main__":
    success = run_discrimination_holdout()
    sys.exit(0 if success else 1)
