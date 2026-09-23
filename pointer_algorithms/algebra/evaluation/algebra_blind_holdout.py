"""
CHUP Phase 3Q — Algebra / Transforms Blind Holdout Evaluation (12 Cases).

Evaluates capability synthesis on domain-masked, real-world narrative problems
(radio astronomy, cryptography, quantum spin, optics, civil engineering, robotics, finance).
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

BLIND_HOLDOUT_PROBLEMS = [
    {
        "id": "ALG-BH-01",
        "title": "Radio Astronomy Interferometry Aperture Synthesis",
        "text": "An array of radio telescopes records Fourier visibilities of a celestial radio source. Synthesize the celestial image by computing polynomial convolution using fast fourier transform FFT.",
        "expected_pattern": "algebra_fft",
        "input": "3 3\n1 4 2\n3 2 5",
        "expected_output": lambda: " ".join(map(str, fft_oracle([1, 4, 2], [3, 2, 5])))
    },
    {
        "id": "ALG-BH-02",
        "title": "Cryptographic Ring Lattice Ring-LWE Key Exchange",
        "text": "A post-quantum cryptographic protocol performs polynomial multiplication in quotient ring Z_q[x]/(x^n + 1) modulo 998244353 using number theoretic transform NTT.",
        "expected_pattern": "algebra_ntt",
        "input": "3 3\n12 34 56\n78 90 12",
        "expected_output": lambda: " ".join(map(str, ntt_oracle([12, 34, 56], [78, 90, 12])))
    },
    {
        "id": "ALG-BH-03",
        "title": "Quantum Spin State Superposition XOR Decoherence",
        "text": "A multi-qubit register undergoes Pauli-X bit flips. Compute the state vector probability distribution after bitwise XOR convolution using fast walsh-hadamard transform FWHT.",
        "expected_pattern": "algebra_fwht",
        "input": "2\n1 3 2 4\n5 1 2 3",
        "expected_output": lambda: " ".join(map(str, fwht_xor_oracle([1, 3, 2, 4], [5, 1, 2, 3])))
    },
    {
        "id": "ALG-BH-04",
        "title": "Optical Fiber Chromatic Dispersion Transfer Function Inversion",
        "text": "A high-speed optical transponder must equalize signal distortion by computing formal power series inverse A(x)^(-1) mod x^n modulo 998244353 with polynomial inverse.",
        "expected_pattern": "algebra_poly_inverse",
        "input": "4\n1 3 5 7",
        "expected_output": lambda: " ".join(map(str, poly_inverse_oracle([1, 3, 5, 7], 4)))
    },
    {
        "id": "ALG-BH-05",
        "title": "Civil Engineering Truss Bridge Static Equilibrium Nodal Forces",
        "text": "Analyze nodal equilibrium forces of a steel bridge truss by solving real system of linear equations A*x = b using Gaussian elimination with partial pivoting.",
        "expected_pattern": "algebra_gauss_real",
        "input": "2\n3 2 13\n1 -2 3",
        "expected_output": lambda: "UNIQUE_SOLUTION\n4.000000 0.500000"
    },
    {
        "id": "ALG-BH-06",
        "title": "Distributed Secret Sharing Finite Field Quorum System",
        "text": "Reconstruct distributed master secret keys across validator nodes by solving modular system of equations A*x = b modulo 998244353 with modular gaussian elimination.",
        "expected_pattern": "algebra_gauss_modular",
        "input": "2\n2 3 8\n1 2 5",
        "expected_output": lambda: "UNIQUE_SOLUTION\n1 2"
    },
    {
        "id": "ALG-BH-07",
        "title": "Telecommunication Error Correction Syndrome Decoding over F_2",
        "text": "Decode error syndrome bits of a low-density parity check code by solving XOR linear system over binary field F_2 using bitset gaussian elimination.",
        "expected_pattern": "algebra_gauss_xor",
        "input": "2 2\n1 0 1\n1 1 0",
        "expected_output": lambda: "UNIQUE_SOLUTION\n1 1"
    },
    {
        "id": "ALG-BH-08",
        "title": "Autonomous Drone Fleet Navigation Waypoint Basis",
        "text": "A fleet of autonomous drones transmits bitmask trajectory vectors. Find the maximum XOR subset of waypoint masks using linear basis in F_2.",
        "expected_pattern": "algebra_linear_basis",
        "input": "4\n5 9 14 2",
        "expected_output": lambda: str(linear_basis_xor_oracle([5, 9, 14, 2])[1])
    },
    {
        "id": "ALG-BH-09",
        "title": "Financial Market Order Book Recurrence Extrapolation",
        "text": "Detect the underlying generation rule of order flow tick intervals using Berlekamp-Massey algorithm modulo 998244353 and compute future nth term.",
        "expected_pattern": "algebra_berlekamp_massey",
        "input": "6 8\n1 3 9 27 81 243",
        "expected_output": lambda: str(linear_recurrence_eval_oracle([1, 3, 9, 27, 81, 243], 8))
    },
    {
        "id": "ALG-BH-10",
        "title": "Spacecraft Orbital Trajectory Polynomial Ephemeris",
        "text": "A deep space probe samples gravitational potentials at discrete telemetry points. Evaluate the potential at target coordinate x using Lagrange interpolation modulo 998244353.",
        "expected_pattern": "algebra_lagrange_interpolation",
        "input": "3 7\n1 3\n2 8\n3 15",
        "expected_output": lambda: str(lagrange_eval_oracle([1, 2, 3], [3, 8, 15], 7))
    },
    {
        "id": "ALG-BH-11",
        "title": "Radar Sonar Chirp Matched Filtering",
        "text": "Filter acoustic radar return echoes against transmitted chirp waveforms using fast fourier transform FFT floating-point convolution.",
        "expected_pattern": "algebra_fft",
        "input": "2 2\n4 1\n2 3",
        "expected_output": lambda: " ".join(map(str, fft_oracle([4, 1], [2, 3])))
    },
    {
        "id": "ALG-BH-12",
        "title": "High-Energy Particle Collision Momenta Convolution in F_p",
        "text": "Calculate quantum state particle momentum density distributions using number theoretic transform NTT modulo 998244353.",
        "expected_pattern": "algebra_ntt",
        "input": "3 3\n2 5 7\n1 3 4",
        "expected_output": lambda: " ".join(map(str, ntt_oracle([2, 5, 7], [1, 3, 4])))
    },
]


def run_blind_holdout():
    print("=" * 80)
    print("CHUP Phase 3Q — Algebra / Transforms Blind Holdout Evaluation (12 Cases)")
    print("=" * 80)
    passed_count = 0

    for prob in BLIND_HOLDOUT_PROBLEMS:
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
    print(f"Blind Holdout Results: {passed_count}/{len(BLIND_HOLDOUT_PROBLEMS)} Passed ({passed_count / len(BLIND_HOLDOUT_PROBLEMS) * 100:.1f}%)")
    print("=" * 80)
    return passed_count == len(BLIND_HOLDOUT_PROBLEMS)


if __name__ == "__main__":
    success = run_blind_holdout()
    sys.exit(0 if success else 1)
