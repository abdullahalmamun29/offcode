"""
CHUP Phase 3Q — Cross-Family Discrimination Holdout Suite (12 Cases).

Verifies boundary discrimination between Algebra / Transforms and neighboring families:
- vs Two Pointers / Sliding Window (ALG-D-01)
- vs Number Theory Sieve (ALG-D-02)
- vs Bitmask Dynamic Programming (ALG-D-03)
- vs Scalar Modular Inverse (ALG-D-04)
- vs Graph Shortest Path (ALG-D-05)
- vs DSU Connectivity (ALG-D-06)
- vs Greedy Set Cover (ALG-D-07)
- vs Trie Bitwise Maximum XOR (ALG-D-08)
- vs Matrix Power Exponentiation (ALG-D-09)
- vs Fenwick / Segment Tree Point Query (ALG-D-10)
- vs Divide & Conquer Sorting (ALG-D-11)
- vs Spanning Tree Cycles (ALG-D-12)
"""

import sys
import os
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.algebra.evaluation.algebra_benchmark import compile_and_run_cpp
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
    lagrange_eval_oracle,
)

DISCRIMINATION_PROBLEMS = [
    {
        "id": "ALG-D-01",
        "title": "Sliding Window Narrative vs FFT Polynomial Convolution",
        "text": "An incoming continuous audio stream presents windowed samples. Rather than finding a subarray window sum, evaluate the complete signal convolution using Fast Fourier Transform FFT.",
        "expected_pattern": "algebra_fft",
        "input": "2 2\n3 1\n4 2",
        "expected_output": lambda: " ".join(map(str, fft_oracle([3, 1], [4, 2])))
    },
    {
        "id": "ALG-D-02",
        "title": "Prime Sieve Narrative vs NTT Exact Convolution",
        "text": "Although prime numbers up to N are discussed, the goal is to multiply two coefficient sequences modulo 998244353 using Number Theoretic Transform NTT.",
        "expected_pattern": "algebra_ntt",
        "input": "2 2\n5 6\n7 8",
        "expected_output": lambda: " ".join(map(str, ntt_oracle([5, 6], [7, 8])))
    },
    {
        "id": "ALG-D-03",
        "title": "Bitmask DP Narrative vs Fast Walsh-Hadamard Transform",
        "text": "Rather than calculating minimum cost subsets via bitmask dynamic programming, evaluate full bitwise XOR convolution of two mask frequency vectors using FWHT fast walsh-hadamard transform.",
        "expected_pattern": "algebra_fwht",
        "input": "2\n1 2 1 2\n3 1 3 1",
        "expected_output": lambda: " ".join(map(str, fwht_xor_oracle([1, 2, 1, 2], [3, 1, 3, 1])))
    },
    {
        "id": "ALG-D-04",
        "title": "Scalar Modular Inverse Narrative vs Formal Power Series Inversion",
        "text": "Rather than computing a single integer modular multiplicative inverse, invert the entire polynomial series A(x)^(-1) mod x^n modulo 998244353 using polynomial inverse.",
        "expected_pattern": "algebra_poly_inverse",
        "input": "3\n1 2 1",
        "expected_output": lambda: " ".join(map(str, poly_inverse_oracle([1, 2, 1], 3)))
    },
    {
        "id": "ALG-D-05",
        "title": "Graph Network Flows vs Real Gaussian Elimination",
        "text": "A network topology resembles an electrical mesh. Rather than finding shortest paths or min-cut, solve the system of linear equations A*x = b using Gaussian elimination with partial pivoting over real numbers.",
        "expected_pattern": "algebra_gauss_real",
        "input": "2\n2 3 7\n1 -1 1",
        "expected_output": lambda: "UNIQUE_SOLUTION\n2.000000 1.000000"
    },
    {
        "id": "ALG-D-06",
        "title": "DSU Disjoint Sets vs Modular Gaussian Elimination",
        "text": "Although equivalence sets are mentioned, the constraints represent linear equations over a prime field. Solve the modular system of equations A*x = b modulo 998244353 with modular gaussian elimination.",
        "expected_pattern": "algebra_gauss_modular",
        "input": "2\n3 1 5\n1 2 5",
        "expected_output": lambda: "UNIQUE_SOLUTION\n1 2"
    },
    {
        "id": "ALG-D-07",
        "title": "Greedy Set Cover Narrative vs F_2 Bitset Gaussian Elimination",
        "text": "Rather than selecting a greedy subset of toggles, determine the exact toggling state by solving XOR linear system over binary field F_2 using bitset gaussian elimination.",
        "expected_pattern": "algebra_gauss_xor",
        "input": "2 2\n1 0 1\n0 1 0",
        "expected_output": lambda: "UNIQUE_SOLUTION\n1 0"
    },
    {
        "id": "ALG-D-08",
        "title": "Trie Bitwise XOR Pair vs Linear Basis Subspace Span",
        "text": "Rather than finding a pair of elements with maximum XOR via a binary trie, find the maximum XOR subset over any number of elements using a linear basis in F_2.",
        "expected_pattern": "algebra_linear_basis",
        "input": "3\n1 2 4",
        "expected_output": lambda: str(linear_basis_xor_oracle([1, 2, 4])[1])
    },
    {
        "id": "ALG-D-09",
        "title": "Fixed Matrix Exponentiation vs Berlekamp-Massey Recurrence",
        "text": "The state transition matrix is not known beforehand. Given observed sequence terms, discover the minimal recurrence via Berlekamp-Massey algorithm modulo 998244353 and compute the nth term.",
        "expected_pattern": "algebra_berlekamp_massey",
        "input": "6 7\n1 2 4 8 16 32",
        "expected_output": lambda: str(linear_recurrence_eval_oracle([1, 2, 4, 8, 16, 32], 7))
    },
    {
        "id": "ALG-D-10",
        "title": "Segment Tree Range Point Update vs Lagrange Interpolation",
        "text": "The points are fixed evaluation nodes of a polynomial. Evaluate the polynomial at query point x using Lagrange interpolation modulo 998244353.",
        "expected_pattern": "algebra_lagrange_interpolation",
        "input": "3 5\n1 2\n2 5\n3 10",
        "expected_output": lambda: str(lagrange_eval_oracle([1, 2, 3], [2, 5, 10], 5))
    },
    {
        "id": "ALG-D-11",
        "title": "Divide and Conquer Sort vs NTT Convolution",
        "text": "Rather than sorting the arrays, multiply two polynomial coefficient vectors modulo 998244353 using Number Theoretic Transform NTT.",
        "expected_pattern": "algebra_ntt",
        "input": "2 2\n1 3\n2 4",
        "expected_output": lambda: " ".join(map(str, ntt_oracle([1, 3], [2, 4])))
    },
    {
        "id": "ALG-D-12",
        "title": "Spanning Tree Cycles vs XOR Linear Basis",
        "text": "Vector cycle space constraints are modeled as bitwise vectors. Compute the maximum XOR value over the subspace using linear basis in F_2.",
        "expected_pattern": "algebra_linear_basis",
        "input": "3\n3 5 6",
        "expected_output": lambda: str(linear_basis_xor_oracle([3, 5, 6])[1])
    },
]


def run_discrimination_holdout():
    print("=" * 80)
    print("CHUP Phase 3Q — Cross-Family Discrimination Holdout Suite (12 Cases)")
    print("=" * 80)
    passed_count = 0

    for prob in DISCRIMINATION_PROBLEMS:
        prob_id = prob["id"]
        prob_text = prob["text"]
        expected_pat = prob["expected_pattern"]
        stdin_data = prob["input"]

        resp = handle_request({"problemText": prob_text})
        selected_pat = resp.get("selectedPattern")
        code = resp.get("code") or resp.get("generatedCode")

        if selected_pat != expected_pat:
            print(f"FAIL [{prob_id}]: Recognition mismatch. Expected {expected_pat}, got {selected_pat}")
            continue

        try:
            actual_output = compile_and_run_cpp(code, stdin_data)
            expected_output = prob["expected_output"]()
            if actual_output.strip() == expected_output.strip():
                print(f"{prob_id} PASS: {prob['title']} (Pattern={selected_pat})")
                passed_count += 1
            else:
                print(f"FAIL [{prob_id}]: Execution output mismatch.")
                print(f"  Expected: {expected_output}")
                print(f"  Actual:   {actual_output}")
        except Exception as e:
            print(f"FAIL [{prob_id}]: Execution error: {e}")

    print("=" * 80)
    print(f"Discrimination Results: {passed_count}/{len(DISCRIMINATION_PROBLEMS)} Passed ({passed_count / len(DISCRIMINATION_PROBLEMS) * 100:.1f}%)")
    print("=" * 80)
    return passed_count == len(DISCRIMINATION_PROBLEMS)


if __name__ == "__main__":
    success = run_discrimination_holdout()
    sys.exit(0 if success else 1)
