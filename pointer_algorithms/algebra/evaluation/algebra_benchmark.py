"""
CHUP Phase 3Q — Algebra / Transforms Benchmark Suite (60 Problems).

Evaluates recognition, structural derivation, invariant construction,
code generation, and C++17 execution across all 10 Phase 3Q patterns (6 cases per pattern):

3Q-A: Fast Fourier Transform (ALG-01..ALG-06)
3Q-B: Number Theoretic Transform (ALG-07..ALG-12)
3Q-C: Fast Walsh-Hadamard Transform (ALG-13..ALG-18)
3Q-D: Polynomial Inversion via Newton's Method (ALG-19..ALG-24)
3Q-E: Gaussian Elimination over R (ALG-25..ALG-30)
3Q-F: Gaussian Elimination over F_p (ALG-31..ALG-36)
3Q-G: Gaussian Elimination over F_2 (ALG-37..ALG-42)
3Q-H: XOR Linear Basis (ALG-43..ALG-48)
3Q-I: Berlekamp-Massey & Recurrence (ALG-49..ALG-54)
3Q-J: Lagrange Interpolation (ALG-55..ALG-60)
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
    berlekamp_massey_oracle,
    linear_recurrence_eval_oracle,
    lagrange_eval_oracle,
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
            raise RuntimeError(f"C++ Compilation failed: {compile_res.stderr}")
        COMPILED_BINARIES[code_hash] = exe

    run_res = subprocess.run(
        [exe],
        input=stdin_data,
        capture_output=True,
        text=True,
        timeout=timeout
    )
    if run_res.returncode != 0:
        raise RuntimeError(f"C++ Execution failed: {run_res.stderr}")
    return run_res.stdout.strip()


BENCHMARK_PROBLEMS = [
    # ── 3Q-A: Fast Fourier Transform (ALG-01..06) ──
    {
        "id": "ALG-01",
        "title": "Continuous Signal Polynomial Convolution",
        "text": "Given two sequences representing continuous acoustic signal coefficients, compute their polynomial convolution using Fast Fourier Transform FFT.",
        "expected_pattern": "algebra_fft",
        "input": "3 3\n1 2 3\n4 5 6",
        "expected_output": lambda: " ".join(map(str, fft_oracle([1, 2, 3], [4, 5, 6])))
    },
    {
        "id": "ALG-02",
        "title": "Complex Polynomial Multiplication",
        "text": "Given degree n polynomials, evaluate their product using fast fourier transform with floating-point convolution.",
        "expected_pattern": "algebra_fft",
        "input": "4 3\n1 0 2 1\n3 1 2",
        "expected_output": lambda: " ".join(map(str, fft_oracle([1, 0, 2, 1], [3, 1, 2])))
    },
    {
        "id": "ALG-03",
        "title": "High Degree Signal Convolution",
        "text": "Compute complex polynomial multiplication for time-series filters using FFT.",
        "expected_pattern": "algebra_fft",
        "input": "4 4\n2 1 3 4\n1 5 2 1",
        "expected_output": lambda: " ".join(map(str, fft_oracle([2, 1, 3, 4], [1, 5, 2, 1])))
    },
    {
        "id": "ALG-04",
        "title": "Impulse Response Convolution",
        "text": "Perform convolution of two impulse response vectors using fast fourier transform with complex roots.",
        "expected_pattern": "algebra_fft",
        "input": "2 3\n5 7\n1 2 3",
        "expected_output": lambda: " ".join(map(str, fft_oracle([5, 7], [1, 2, 3])))
    },
    {
        "id": "ALG-05",
        "title": "Audio Waveform Echo Blending",
        "text": "Blend audio echo filters using FFT floating-point convolution over complex twiddle factors.",
        "expected_pattern": "algebra_fft",
        "input": "3 2\n3 4 5\n2 1",
        "expected_output": lambda: " ".join(map(str, fft_oracle([3, 4, 5], [2, 1])))
    },
    {
        "id": "ALG-06",
        "title": "Discrete Spectral Power Convolution",
        "text": "Convolve two discrete spectral frequency series using Fast Fourier Transform FFT algorithm.",
        "expected_pattern": "algebra_fft",
        "input": "2 2\n10 20\n30 40",
        "expected_output": lambda: " ".join(map(str, fft_oracle([10, 20], [30, 40])))
    },

    # ── 3Q-B: Number Theoretic Transform (ALG-07..12) ──
    {
        "id": "ALG-07",
        "title": "Exact Modular Polynomial Multiplication",
        "text": "Multiply two polynomials modulo 998244353 using Number Theoretic Transform NTT.",
        "expected_pattern": "algebra_ntt",
        "input": "3 3\n1 2 3\n4 5 6",
        "expected_output": lambda: " ".join(map(str, ntt_oracle([1, 2, 3], [4, 5, 6])))
    },
    {
        "id": "ALG-08",
        "title": "Large Degree Modular Convolution",
        "text": "Evaluate exact modular polynomial convolution modulo 998244353 via NTT.",
        "expected_pattern": "algebra_ntt",
        "input": "4 4\n100 200 300 400\n500 600 700 800",
        "expected_output": lambda: " ".join(map(str, ntt_oracle([100, 200, 300, 400], [500, 600, 700, 800])))
    },
    {
        "id": "ALG-09",
        "title": "Combinatorial Generating Function Product",
        "text": "Compute the product of generating function polynomials modulo 998244353 using number theoretic transform.",
        "expected_pattern": "algebra_ntt",
        "input": "3 2\n5 12 13\n7 24",
        "expected_output": lambda: " ".join(map(str, ntt_oracle([5, 12, 13], [7, 24])))
    },
    {
        "id": "ALG-10",
        "title": "Finite Field Convolution Pipeline",
        "text": "Given coefficient vectors in F_p, compute their exact convolution modulo 998244353 with NTT.",
        "expected_pattern": "algebra_ntt",
        "input": "4 2\n1 1 1 1\n1 1",
        "expected_output": lambda: " ".join(map(str, ntt_oracle([1, 1, 1, 1], [1, 1])))
    },
    {
        "id": "ALG-11",
        "title": "Cryptographic Sequence NTT Convolution",
        "text": "Evaluate exact polynomial product modulo 998244353 using NTT number theoretic transform.",
        "expected_pattern": "algebra_ntt",
        "input": "2 3\n1000 2000\n3 4 5",
        "expected_output": lambda: " ".join(map(str, ntt_oracle([1000, 2000], [3, 4, 5])))
    },
    {
        "id": "ALG-12",
        "title": "Permutation Inversion Sequence Convolution",
        "text": "Compute exact modular convolution modulo 998244353 with number theoretic transform NTT.",
        "expected_pattern": "algebra_ntt",
        "input": "3 3\n9 8 7\n6 5 4",
        "expected_output": lambda: " ".join(map(str, ntt_oracle([9, 8, 7], [6, 5, 4])))
    },

    # ── 3Q-C: Fast Walsh-Hadamard Transform (ALG-13..18) ──
    {
        "id": "ALG-13",
        "title": "Bitwise XOR Array Convolution",
        "text": "Given two arrays indexed by bitmasks of length 2^B, compute their XOR convolution using Fast Walsh-Hadamard Transform FWHT.",
        "expected_pattern": "algebra_fwht",
        "input": "2\n1 2 3 4\n5 6 7 8",
        "expected_output": lambda: " ".join(map(str, fwht_xor_oracle([1, 2, 3, 4], [5, 6, 7, 8])))
    },
    {
        "id": "ALG-14",
        "title": "Hypercube State XOR Transition",
        "text": "Evaluate bitwise XOR convolution on state vectors of length 2^B using fast walsh-hadamard transform.",
        "expected_pattern": "algebra_fwht",
        "input": "3\n1 0 1 0 1 0 1 0\n0 1 0 1 0 1 0 1",
        "expected_output": lambda: " ".join(map(str, fwht_xor_oracle([1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1])))
    },
    {
        "id": "ALG-15",
        "title": "Walsh Transform Mask Pairing",
        "text": "Compute exact bitwise XOR sum over indices using FWHT transform.",
        "expected_pattern": "algebra_fwht",
        "input": "2\n2 1 4 3\n1 2 3 4",
        "expected_output": lambda: " ".join(map(str, fwht_xor_oracle([2, 1, 4, 3], [1, 2, 3, 4])))
    },
    {
        "id": "ALG-16",
        "title": "Subspace Parity Convolution",
        "text": "Perform hypercube transform for bitwise XOR convolution with fast walsh-hadamard.",
        "expected_pattern": "algebra_fwht",
        "input": "1\n3 5\n2 4",
        "expected_output": lambda: " ".join(map(str, fwht_xor_oracle([3, 5], [2, 4])))
    },
    {
        "id": "ALG-17",
        "title": "Quantum Bitmask Amplitude Convolution",
        "text": "Compute the XOR convolution of two probability vectors using FWHT fast walsh-hadamard transform.",
        "expected_pattern": "algebra_fwht",
        "input": "2\n1 1 1 1\n2 2 2 2",
        "expected_output": lambda: " ".join(map(str, fwht_xor_oracle([1, 1, 1, 1], [2, 2, 2, 2])))
    },
    {
        "id": "ALG-18",
        "title": "Telecommunication Orthogonal Code XOR Sum",
        "text": "Convolve orthogonal Walsh codes under bitwise XOR using fast walsh-hadamard transform FWHT.",
        "expected_pattern": "algebra_fwht",
        "input": "3\n1 2 3 4 5 6 7 8\n8 7 6 5 4 3 2 1",
        "expected_output": lambda: " ".join(map(str, fwht_xor_oracle([1, 2, 3, 4, 5, 6, 7, 8], [8, 7, 6, 5, 4, 3, 2, 1])))
    },

    # ── 3Q-D: Polynomial Inversion (ALG-19..24) ──
    {
        "id": "ALG-19",
        "title": "Formal Power Series Truncated Inverse",
        "text": "Compute formal power series inverse A(x)^(-1) mod x^n modulo 998244353 using polynomial inverse.",
        "expected_pattern": "algebra_poly_inverse",
        "input": "4\n1 2 3 4",
        "expected_output": lambda: " ".join(map(str, poly_inverse_oracle([1, 2, 3, 4], 4)))
    },
    {
        "id": "ALG-20",
        "title": "Newton Iteration Reciprocal Series",
        "text": "Find polynomial inverse modulo 998244353 of degree n via Newton's method.",
        "expected_pattern": "algebra_poly_inverse",
        "input": "3\n1 1 1",
        "expected_output": lambda: " ".join(map(str, poly_inverse_oracle([1, 1, 1], 3)))
    },
    {
        "id": "ALG-21",
        "title": "Generating Function Inversion Pipeline",
        "text": "Invert polynomial series A(x)^(-1) mod x^n modulo 998244353 with non-zero constant term.",
        "expected_pattern": "algebra_poly_inverse",
        "input": "5\n2 1 0 1 1",
        "expected_output": lambda: " ".join(map(str, poly_inverse_oracle([2, 1, 0, 1, 1], 5)))
    },
    {
        "id": "ALG-22",
        "title": "Differential Equation Polynomial Inversion",
        "text": "Compute truncated reciprocal series using polynomial inverse modulo 998244353.",
        "expected_pattern": "algebra_poly_inverse",
        "input": "4\n5 4 3 2",
        "expected_output": lambda: " ".join(map(str, poly_inverse_oracle([5, 4, 3, 2], 4)))
    },
    {
        "id": "ALG-23",
        "title": "Eulerian Fraction Series Inverse",
        "text": "Evaluate power series inverse modulo 998244353 using polynomial inversion.",
        "expected_pattern": "algebra_poly_inverse",
        "input": "3\n3 2 1",
        "expected_output": lambda: " ".join(map(str, poly_inverse_oracle([3, 2, 1], 3)))
    },
    {
        "id": "ALG-24",
        "title": "Reciprocal Partition Generating Series",
        "text": "Find formal power series inverse modulo 998244353 with Newton iteration polynomial inverse.",
        "expected_pattern": "algebra_poly_inverse",
        "input": "4\n1 0 0 1",
        "expected_output": lambda: " ".join(map(str, poly_inverse_oracle([1, 0, 0, 1], 4)))
    },

    # ── 3Q-E: Gaussian Elimination over R (ALG-25..30) ──
    {
        "id": "ALG-25",
        "title": "Real Linear System Unique Solution",
        "text": "Solve system of linear equations A*x = b over real numbers using Gaussian elimination with partial pivoting.",
        "expected_pattern": "algebra_gauss_real",
        "input": "2\n2 1 5\n1 -1 1",
        "expected_output": lambda: "UNIQUE_SOLUTION\n2.000000 1.000000"
    },
    {
        "id": "ALG-26",
        "title": "Real Linear System 3x3",
        "text": "Solve real linear system A*x = b using gaussian elimination over R.",
        "expected_pattern": "algebra_gauss_real",
        "input": "3\n1 1 1 6\n0 2 5 -4\n2 5 -1 27",
        "expected_output": lambda: "UNIQUE_SOLUTION\n5.000000 3.000000 -2.000000"
    },
    {
        "id": "ALG-27",
        "title": "Real System Inconsistent Check",
        "text": "Solve system of linear equations with gaussian elimination over real numbers.",
        "expected_pattern": "algebra_gauss_real",
        "input": "2\n1 1 2\n1 1 3",
        "expected_output": lambda: "INCONSISTENT"
    },
    {
        "id": "ALG-28",
        "title": "Real System Infinite Solutions",
        "text": "Determine system consistency and solve real linear system with gaussian elimination.",
        "expected_pattern": "algebra_gauss_real",
        "input": "2\n1 1 2\n2 2 4",
        "expected_output": lambda: "INFINITE_SOLUTIONS"
    },
    {
        "id": "ALG-29",
        "title": "Numerical Circuit Mesh Voltage System",
        "text": "Solve linear system of mesh equations A*x = b using Gaussian elimination over real floating-point numbers.",
        "expected_pattern": "algebra_gauss_real",
        "input": "2\n4 -1 9\n-1 4 6",
        "expected_output": lambda: "UNIQUE_SOLUTION\n2.800000 2.200000"
    },
    {
        "id": "ALG-30",
        "title": "Robotic Kinematics Real Linear Equations",
        "text": "Solve 3-variable kinematic linear equations with gaussian elimination over R.",
        "expected_pattern": "algebra_gauss_real",
        "input": "3\n2 1 -1 8\n-3 -1 2 -11\n-2 1 2 -3",
        "expected_output": lambda: "UNIQUE_SOLUTION\n2.000000 3.000000 -1.000000"
    },

    # ── 3Q-F: Gaussian Elimination over F_p (ALG-31..36) ──
    {
        "id": "ALG-31",
        "title": "Modular Linear System Unique Solution",
        "text": "Solve modular system of equations A*x = b modulo 998244353 using gaussian elimination over prime field.",
        "expected_pattern": "algebra_gauss_modular",
        "input": "2\n1 2 5\n3 4 11",
        "expected_output": lambda: "UNIQUE_SOLUTION\n1 2"
    },
    {
        "id": "ALG-32",
        "title": "Modular System 3x3 Prime Field",
        "text": "Solve 3x3 modular system of linear equations modulo 998244353 using modular gaussian elimination.",
        "expected_pattern": "algebra_gauss_modular",
        "input": "3\n1 1 1 6\n2 1 1 7\n1 2 1 8",
        "expected_output": lambda: "UNIQUE_SOLUTION\n1 2 3"
    },
    {
        "id": "ALG-33",
        "title": "Modular System Inconsistency",
        "text": "Solve linear system modulo prime 998244353 with gaussian elimination over F_p.",
        "expected_pattern": "algebra_gauss_modular",
        "input": "2\n1 1 1\n1 1 2",
        "expected_output": lambda: "INCONSISTENT"
    },
    {
        "id": "ALG-34",
        "title": "Modular System Underdetermined",
        "text": "Evaluate consistency of modular linear system modulo 998244353 with gaussian elimination.",
        "expected_pattern": "algebra_gauss_modular",
        "input": "2\n1 2 3\n2 4 6",
        "expected_output": lambda: "INFINITE_SOLUTIONS"
    },
    {
        "id": "ALG-35",
        "title": "Cryptographic Lattice Congruences",
        "text": "Solve system of linear congruences modulo 998244353 using modular gaussian elimination.",
        "expected_pattern": "algebra_gauss_modular",
        "input": "2\n5 7 19\n2 3 8",
        "expected_output": lambda: "UNIQUE_SOLUTION\n1 2"
    },
    {
        "id": "ALG-36",
        "title": "Finite Field Channel Inversion",
        "text": "Solve linear matrix system over F_p modulo 998244353 with modular gaussian elimination.",
        "expected_pattern": "algebra_gauss_modular",
        "input": "3\n1 0 0 7\n0 1 0 8\n0 0 1 9",
        "expected_output": lambda: "UNIQUE_SOLUTION\n7 8 9"
    },

    # ── 3Q-G: Gaussian Elimination over F_2 (ALG-37..42) ──
    {
        "id": "ALG-37",
        "title": "Binary Linear System over F_2",
        "text": "Solve linear system of equations over binary field F_2 using bitset gaussian elimination.",
        "expected_pattern": "algebra_gauss_xor",
        "input": "2 2\n1 1 1\n0 1 1",
        "expected_output": lambda: "UNIQUE_SOLUTION\n0 1"
    },
    {
        "id": "ALG-38",
        "title": "Light Bulb Toggle Puzzle",
        "text": "Solve system of light bulb toggles under XOR linear system over F_2 with bitset gauss.",
        "expected_pattern": "algebra_gauss_xor",
        "input": "3 3\n1 0 1 1\n1 1 0 0\n0 0 1 1",
        "expected_output": lambda: "UNIQUE_SOLUTION\n0 0 1"
    },
    {
        "id": "ALG-39",
        "title": "Binary Matrix Inconsistency",
        "text": "Solve system of equations over F_2 using bitset gaussian elimination.",
        "expected_pattern": "algebra_gauss_xor",
        "input": "2 2\n1 1 0\n1 1 1",
        "expected_output": lambda: "INCONSISTENT"
    },
    {
        "id": "ALG-40",
        "title": "Underdetermined Binary System",
        "text": "Find solution to XOR linear system over binary field F_2 with bitset gaussian elimination.",
        "expected_pattern": "algebra_gauss_xor",
        "input": "2 2\n1 0 1\n0 0 0",
        "expected_output": lambda: "INFINITE_SOLUTIONS"
    },
    {
        "id": "ALG-41",
        "title": "Parity Check Matrix Solving",
        "text": "Solve error-correcting parity check matrix equations over F_2 using bitset gauss.",
        "expected_pattern": "algebra_gauss_xor",
        "input": "3 3\n1 1 1 1\n0 1 1 0\n0 0 1 1",
        "expected_output": lambda: "UNIQUE_SOLUTION\n1 1 1"
    },
    {
        "id": "ALG-42",
        "title": "Logic Gate Network System",
        "text": "Solve XOR circuit equations over binary field F_2 with bitset gaussian elimination.",
        "expected_pattern": "algebra_gauss_xor",
        "input": "2 2\n1 0 0\n0 1 1",
        "expected_output": lambda: "UNIQUE_SOLUTION\n0 1"
    },

    # ── 3Q-H: XOR Linear Basis (ALG-43..48) ──
    {
        "id": "ALG-43",
        "title": "Maximum XOR Subset Selection",
        "text": "Given an array of integers, compute the maximum XOR subset value using a linear basis in F_2.",
        "expected_pattern": "algebra_linear_basis",
        "input": "3\n1 2 4",
        "expected_output": lambda: str(linear_basis_xor_oracle([1, 2, 4])[1])
    },
    {
        "id": "ALG-44",
        "title": "Vector Subspace Maximum XOR",
        "text": "Maintain an online XOR linear basis and find the maximum XOR value.",
        "expected_pattern": "algebra_linear_basis",
        "input": "4\n3 7 12 15",
        "expected_output": lambda: str(linear_basis_xor_oracle([3, 7, 12, 15])[1])
    },
    {
        "id": "ALG-45",
        "title": "Network Packet Header XOR Maximization",
        "text": "Find the maximum XOR subset of packet header masks using linear basis.",
        "expected_pattern": "algebra_linear_basis",
        "input": "5\n10 20 30 40 50",
        "expected_output": lambda: str(linear_basis_xor_oracle([10, 20, 30, 40, 50])[1])
    },
    {
        "id": "ALG-46",
        "title": "Cryptographic Key Component Basis",
        "text": "Construct an echelonized linear basis in F_2^B and query maximum xor subset.",
        "expected_pattern": "algebra_linear_basis",
        "input": "3\n8 4 2",
        "expected_output": lambda: str(linear_basis_xor_oracle([8, 4, 2])[1])
    },
    {
        "id": "ALG-47",
        "title": "Bitwise Subspace Dimension Span",
        "text": "Query maximum XOR sum over vector space using xor linear basis.",
        "expected_pattern": "algebra_linear_basis",
        "input": "4\n1 3 5 7",
        "expected_output": lambda: str(linear_basis_xor_oracle([1, 3, 5, 7])[1])
    },
    {
        "id": "ALG-48",
        "title": "Large Mask Linear Basis",
        "text": "Determine maximum XOR value of 64-bit integers using online linear basis in F_2.",
        "expected_pattern": "algebra_linear_basis",
        "input": "4\n100 200 300 400",
        "expected_output": lambda: str(linear_basis_xor_oracle([100, 200, 300, 400])[1])
    },

    # ── 3Q-I: Berlekamp-Massey & Recurrence (ALG-49..54) ──
    {
        "id": "ALG-49",
        "title": "Fibonacci N-th Term via Recurrence",
        "text": "Find minimal linear recurrence using Berlekamp-Massey algorithm modulo 998244353 and compute nth term.",
        "expected_pattern": "algebra_berlekamp_massey",
        "input": "6 10\n0 1 1 2 3 5",
        "expected_output": lambda: str(linear_recurrence_eval_oracle([0, 1, 1, 2, 3, 5], 10))
    },
    {
        "id": "ALG-50",
        "title": "Tribonacci Sequence Large Query",
        "text": "Compute nth term of sequence generated by Berlekamp-Massey recurrence modulo 998244353.",
        "expected_pattern": "algebra_berlekamp_massey",
        "input": "6 7\n1 1 2 4 7 13",
        "expected_output": lambda: str(linear_recurrence_eval_oracle([1, 1, 2, 4, 7, 13], 7))
    },
    {
        "id": "ALG-51",
        "title": "Linear Recurrence Discovery",
        "text": "Given sequence prefix, find recurrence via Berlekamp-Massey and evaluate nth term modulo 998244353.",
        "expected_pattern": "algebra_berlekamp_massey",
        "input": "6 5\n1 2 4 8 16 32",
        "expected_output": lambda: str(linear_recurrence_eval_oracle([1, 2, 4, 8, 16, 32], 5))
    },
    {
        "id": "ALG-52",
        "title": "Polynomial Modulus Sequence Extrapolation",
        "text": "Find linear recurrence using BM algorithm modulo 998244353 and evaluate large query index.",
        "expected_pattern": "algebra_berlekamp_massey",
        "input": "6 8\n2 3 5 9 17 33",
        "expected_output": lambda: str(linear_recurrence_eval_oracle([2, 3, 5, 9, 17, 33], 8))
    },
    {
        "id": "ALG-53",
        "title": "Order-2 Alternating Sequence Recurrence",
        "text": "Reconstruct recurrence via Berlekamp-Massey and compute nth term modulo 998244353.",
        "expected_pattern": "algebra_berlekamp_massey",
        "input": "6 9\n1 -1 1 -1 1 -1",
        "expected_output": lambda: str(linear_recurrence_eval_oracle([1, -1, 1, -1, 1, -1], 9))
    },
    {
        "id": "ALG-54",
        "title": "High Order Recurrence Prediction",
        "text": "Find minimal linear recurrence of sequence modulo 998244353 using Berlekamp-Massey algorithm.",
        "expected_pattern": "algebra_berlekamp_massey",
        "input": "6 4\n3 5 9 17 33 65",
        "expected_output": lambda: str(linear_recurrence_eval_oracle([3, 5, 9, 17, 33, 65], 4))
    },

    # ── 3Q-J: Lagrange Interpolation (ALG-55..60) ──
    {
        "id": "ALG-55",
        "title": "Lagrange Point Evaluation",
        "text": "Given points on a polynomial, evaluate the polynomial at x using Lagrange interpolation modulo 998244353.",
        "expected_pattern": "algebra_lagrange_interpolation",
        "input": "3 5\n1 1\n2 4\n3 9",
        "expected_output": lambda: str(lagrange_eval_oracle([1, 2, 3], [1, 4, 9], 5))
    },
    {
        "id": "ALG-56",
        "title": "Cubic Polynomial Interpolation",
        "text": "Evaluate polynomial from sample points using Lagrange interpolation modulo 998244353.",
        "expected_pattern": "algebra_lagrange_interpolation",
        "input": "4 10\n1 1\n2 8\n3 27\n4 64",
        "expected_output": lambda: str(lagrange_eval_oracle([1, 2, 3, 4], [1, 8, 27, 64], 10))
    },
    {
        "id": "ALG-57",
        "title": "Linear Function Point Evaluation",
        "text": "Evaluate polynomial at target query using Lagrange interpolation modulo 998244353.",
        "expected_pattern": "algebra_lagrange_interpolation",
        "input": "2 100\n1 5\n2 7",
        "expected_output": lambda: str(lagrange_eval_oracle([1, 2], [5, 7], 100))
    },
    {
        "id": "ALG-58",
        "title": "Quadratic Sensor Calibration Curve",
        "text": "Calibrate sensor polynomial at target point via Lagrange interpolation modulo 998244353.",
        "expected_pattern": "algebra_lagrange_interpolation",
        "input": "3 6\n1 2\n2 5\n3 10",
        "expected_output": lambda: str(lagrange_eval_oracle([1, 2, 3], [2, 5, 10], 6))
    },
    {
        "id": "ALG-59",
        "title": "Power Sum Polynomial Evaluation",
        "text": "Evaluate degree d polynomial at query point using Lagrange interpolation modulo 998244353.",
        "expected_pattern": "algebra_lagrange_interpolation",
        "input": "3 4\n0 0\n1 1\n2 5",
        "expected_output": lambda: str(lagrange_eval_oracle([0, 1, 2], [0, 1, 5], 4))
    },
    {
        "id": "ALG-60",
        "title": "Contiguous Node Lagrange Interpolation",
        "text": "Evaluate polynomial from contiguous points 0 to d at query point using Lagrange interpolation modulo 998244353.",
        "expected_pattern": "algebra_lagrange_interpolation",
        "input": "3 10\n0 1\n1 3\n2 7",
        "expected_output": lambda: str(lagrange_eval_oracle([0, 1, 2], [1, 3, 7], 10))
    },
]


def run_all_benchmarks():
    print("=" * 80)
    print("CHUP Phase 3Q — Algebra / Transforms Benchmark Suite (60 Problems)")
    print("=" * 80)
    passed_count = 0

    for prob in BENCHMARK_PROBLEMS:
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

        if not code or "#include" not in code:
            print(f"FAIL [{prob_id}]: No C++ code generated.")
            continue

        # Execute C++ code
        try:
            actual_output = compile_and_run_cpp(code, stdin_data)
            expected_output = prob["expected_output"]()
            if actual_output.strip() == expected_output.strip():
                print(f"{prob_id} PASS: {prob['title']} (Pattern={selected_pat})")
                passed_count += 1
            else:
                print(f"FAIL [{prob_id}]: Execution output mismatch.")
                print(f"  Input:    {stdin_data}")
                print(f"  Expected: {expected_output}")
                print(f"  Actual:   {actual_output}")
        except Exception as e:
            print(f"FAIL [{prob_id}]: Error during C++ compilation/execution: {e}")

    print("=" * 80)
    print(f"Benchmark Results: {passed_count}/{len(BENCHMARK_PROBLEMS)} Passed ({passed_count / len(BENCHMARK_PROBLEMS) * 100:.1f}%)")
    print("=" * 80)
    return passed_count == len(BENCHMARK_PROBLEMS)


if __name__ == "__main__":
    success = run_all_benchmarks()
    sys.exit(0 if success else 1)
