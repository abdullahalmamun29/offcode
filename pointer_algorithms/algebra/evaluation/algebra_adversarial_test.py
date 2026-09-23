"""
CHUP Phase 3Q — Algebra / Transforms Adversarial Test Suite.

Contains 16 adversarial entrapment and extreme boundary test cases:
1. ADV-ALG-01: Sliding window audio narrative entrapment in FFT
2. ADV-ALG-02: Segment tree frequency range narrative in NTT
3. ADV-ALG-03: Dynamic programming bitmask subset narrative in FWHT
4. ADV-ALG-04: Graph electrical mesh flow narrative in Real Gauss
5. ADV-ALG-05: CRT simultaneous congruence narrative in Modular Gauss
6. ADV-ALG-06: Switch toggle puzzle graph narrative in XOR Gauss
7. ADV-ALG-07: Binary trie maximum XOR narrative in XOR Linear Basis
8. ADV-ALG-08: Matrix exponentiation transition narrative in Berlekamp-Massey
9. ADV-ALG-09: Spline curve fitting narrative in Lagrange Interpolation
10. ADV-ALG-10: Taylor series quotient narrative in Polynomial Inversion
11. ADV-ALG-11: Boundary: Degree 0 polynomial multiplication in NTT (size 1 x size 1)
12. ADV-ALG-12: Boundary: 1-element hypercube (N = 1) in FWHT
13. ADV-ALG-13: Boundary: Single term A(0)=1, N=1 in Polynomial Inversion
14. ADV-ALG-14: Boundary: All-zero stream in XOR Linear Basis
15. ADV-ALG-15: Boundary: Single point degree-0 in Lagrange Interpolation
16. ADV-ALG-16: Boundary: 1x1 linear system over F_p in Modular Gauss
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
        "id": "ADV-ALG-01",
        "title": "Sliding Window Audio Narrative Entrapment in FFT",
        "text": "An incoming audio stream arrives in windowed frames. Rather than maintaining running window statistics or sliding sums, compute the complete discrete convolution of the signal vectors using Fast Fourier Transform FFT.",
        "expected_pattern": "algebra_fft",
        "input": "3 3\n1 2 3\n4 5 6",
        "validator": lambda out: out.strip() == "4 13 28 27 18"
    },
    {
        "id": "ADV-ALG-02",
        "title": "Segment Tree Frequency Range Narrative in NTT",
        "text": "Sequence frequencies form polynomial coefficients. Rather than querying interval sums with a segment tree, calculate the exact product polynomial modulo 998244353 using Number Theoretic Transform NTT.",
        "expected_pattern": "algebra_ntt",
        "input": "2 2\n3 4\n5 6",
        "validator": lambda out: out.strip() == "15 38 24"
    },
    {
        "id": "ADV-ALG-03",
        "title": "Dynamic Programming Bitmask Subset Narrative in FWHT",
        "text": "Subset states interact across bitwise configurations. Rather than computing subset convolutions with dynamic programming, evaluate the complete bitwise XOR convolution of the hypercube vectors using Fast Walsh-Hadamard Transform FWHT.",
        "expected_pattern": "algebra_fwht",
        "input": "2\n1 2 3 4\n5 6 7 8",
        "validator": lambda out: out.strip() == "70 68 62 60"
    },
    {
        "id": "ADV-ALG-04",
        "title": "Graph Electrical Mesh Flow Narrative in Real Gauss",
        "text": "An interconnected circuit topology models resistor branches. Rather than finding shortest paths or minimum cut flows, solve the linear system of mesh equations A*x = b using Gaussian elimination with partial pivoting over real numbers.",
        "expected_pattern": "algebra_gauss_real",
        "input": "2\n2 1 5\n1 -1 1",
        "validator": lambda out: "UNIQUE_SOLUTION" in out and "2.000000 1.000000" in out
    },
    {
        "id": "ADV-ALG-05",
        "title": "CRT Simultaneous Congruence Narrative in Modular Gauss",
        "text": "A cryptographic scheme imposes simultaneous constraints on variables. Rather than single variable modular reduction, solve the multivariable system of linear equations A*x = b modulo 998244353 using modular gaussian elimination over prime field.",
        "expected_pattern": "algebra_gauss_modular",
        "input": "2\n1 2 5\n3 4 11",
        "validator": lambda out: out.strip() == "UNIQUE_SOLUTION\n1 2"
    },
    {
        "id": "ADV-ALG-06",
        "title": "Switch Toggle Puzzle Graph Narrative in XOR Gauss",
        "text": "A network of light bulbs and toggle switches must reach an off state. Rather than searching states via breadth-first search, solve the system of linear equations over binary field F_2 using bitset gaussian elimination.",
        "expected_pattern": "algebra_gauss_xor",
        "input": "2 2\n1 1 0\n0 1 1",
        "validator": lambda out: out.strip() == "UNIQUE_SOLUTION\n1 1"
    },
    {
        "id": "ADV-ALG-07",
        "title": "Binary Trie Maximum XOR Narrative in XOR Linear Basis",
        "text": "A collection of 64-bit masks is given. Rather than querying pairwise maximum XOR using a binary prefix trie, find the maximum possible XOR sum over any subset of masks using a linear basis in F_2.",
        "expected_pattern": "algebra_linear_basis",
        "input": "3\n12 5 10",
        "validator": lambda out: out.strip() == "15"
    },
    {
        "id": "ADV-ALG-08",
        "title": "Matrix Exponentiation Transition Narrative in Berlekamp-Massey",
        "text": "The sequence transition rules are unknown beforehand. Rather than multiplying a fixed transition matrix, discover the minimal linear recurrence from observed sequence terms using Berlekamp-Massey algorithm modulo 998244353 and extrapolate the nth term.",
        "expected_pattern": "algebra_berlekamp_massey",
        "input": "6 7\n1 1 2 3 5 8",
        "validator": lambda out: out.strip() == "21"
    },
    {
        "id": "ADV-ALG-09",
        "title": "Spline Curve Fitting Narrative in Lagrange Interpolation",
        "text": "Sensor measurements record polynomial samples at fixed nodes. Rather than cubic spline interpolation, evaluate the exact polynomial at query point x using Lagrange interpolation modulo 998244353.",
        "expected_pattern": "algebra_lagrange_interpolation",
        "input": "3 4\n1 3\n2 7\n3 13",
        "validator": lambda out: out.strip() == "21"
    },
    {
        "id": "ADV-ALG-10",
        "title": "Taylor Series Quotient Narrative in Polynomial Inversion",
        "text": "A generating function requires formal power series division. Rather than long polynomial division, compute the formal power series inverse A(x)^(-1) mod x^n modulo 998244353 using polynomial inversion.",
        "expected_pattern": "algebra_poly_inverse",
        "input": "3\n1 1 1",
        "validator": lambda out: out.strip() == "1 998244352 0"
    },
    {
        "id": "ADV-ALG-11",
        "title": "Boundary: Degree 0 Polynomial Multiplication in NTT",
        "text": "Multiply two single-term constant polynomials modulo 998244353 using number theoretic transform NTT.",
        "expected_pattern": "algebra_ntt",
        "input": "1 1\n42\n10",
        "validator": lambda out: out.strip() == "420"
    },
    {
        "id": "ADV-ALG-12",
        "title": "Boundary: 1-Element Hypercube (N = 1) in FWHT",
        "text": "Compute the bitwise XOR convolution of 1-element hypercube vectors using Fast Walsh-Hadamard Transform FWHT.",
        "expected_pattern": "algebra_fwht",
        "input": "0\n7\n6",
        "validator": lambda out: out.strip() == "42"
    },
    {
        "id": "ADV-ALG-13",
        "title": "Boundary: Single Term Constant Series in Polynomial Inversion",
        "text": "Find the formal power series inverse modulo x^1 with constant term 1 modulo 998244353 using polynomial inversion.",
        "expected_pattern": "algebra_poly_inverse",
        "input": "1\n1",
        "validator": lambda out: out.strip() == "1"
    },
    {
        "id": "ADV-ALG-14",
        "title": "Boundary: All-Zero Vector Stream in XOR Linear Basis",
        "text": "Find the maximum XOR subset over an array of all zero elements using linear basis in F_2.",
        "expected_pattern": "algebra_linear_basis",
        "input": "3\n0 0 0",
        "validator": lambda out: out.strip() == "0"
    },
    {
        "id": "ADV-ALG-15",
        "title": "Boundary: Single Point Degree-0 in Lagrange Interpolation",
        "text": "Evaluate a constant degree-0 polynomial from 1 point at query coordinate x using Lagrange interpolation modulo 998244353.",
        "expected_pattern": "algebra_lagrange_interpolation",
        "input": "1 100\n5 99",
        "validator": lambda out: out.strip() == "99"
    },
    {
        "id": "ADV-ALG-16",
        "title": "Boundary: 1x1 Linear System over F_p in Modular Gauss",
        "text": "Solve a 1-variable linear equation A*x = b modulo 998244353 using modular gaussian elimination over prime field.",
        "expected_pattern": "algebra_gauss_modular",
        "input": "1\n3 6",
        "validator": lambda out: out.strip() == "UNIQUE_SOLUTION\n2"
    }
]


def run_adversarial_suite():
    print("=" * 80)
    print("CHUP Phase 3Q — Algebra / Transforms Adversarial Suite (16 Cases)")
    print("=" * 80)
    passed = 0
    for prob in ADVERSARIAL_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]
        expected_pat = prob["expected_pattern"]
        stdin_data = prob["input"]

        resp = handle_request({"action": "solve", "problemText": text})
        sel_pat = resp.get("selectedPattern")

        if sel_pat != expected_pat:
            print(f"FAIL [{pid}]: Pattern mismatch. Expected {expected_pat}, got {sel_pat}")
            continue

        code = resp.get("code", "")
        if not code:
            print(f"FAIL [{pid}]: No code generated.")
            continue

        output = compile_and_run_cpp(code, stdin_data)
        if not prob["validator"](output):
            print(f"FAIL [{pid}]: Output validation failed. Output: {output!r}")
            continue

        print(f"{pid} PASS: {title} (Pattern={sel_pat})")
        passed += 1

    print("=" * 80)
    print(f"Adversarial Results: {passed}/{len(ADVERSARIAL_PROBLEMS)} Passed ({passed/len(ADVERSARIAL_PROBLEMS)*100:.1f}%)")
    print("=" * 80)
    if passed < len(ADVERSARIAL_PROBLEMS):
        sys.exit(1)


if __name__ == "__main__":
    run_adversarial_suite()
