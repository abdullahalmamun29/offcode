"""
CHUP Phase 3P — Number Theory & Combinatorics Blind Holdout Evaluation.

Evaluates 12 unseen, real-world domain problem formulations with rich contextual vocabulary
across the number theory and combinatorics domain:

1. NT-BH-01: Ancient Astronomy Calendar Synchronization & Planetary Alignment (Extended GCD)
2. NT-BH-02: Cryptographic RSA Decryption Key Exponent Inversion (Modular Inverse)
3. NT-BH-03: Distributed Secret Sharing Residue Reconstruction (Chinese Remainder Theorem)
4. NT-BH-04: High-Throughput Genomic Prime Sequence Frequency Indexer (Linear Sieve)
5. NT-BH-05: Network Security Coprime Port Assignment (Euler Totient)
6. NT-BH-06: Quantum Lattice Point Coprimality & Ray Visibility (Möbius Inversion)
7. NT-BH-07: Population Growth Matrix Transformation System (Matrix Power)
8. NT-BH-08: Lottery Ticket Selection & Distribution Paths (Factorial Combinatorics)
9. NT-BH-09: Intergalactic Spacecraft Route Configurations (Lucas' Theorem)
10. NT-BH-10: Cryptographic Certificate Prime Authenticity Verification (Miller-Rabin)
11. NT-BH-11: Gear Ratio Synchronization & Mechanical Step Balancing (Extended GCD)
12. NT-BH-12: Distributed Blockchain Validator Quorum Residues (Chinese Remainder Theorem)
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


BLIND_HOLDOUT_PROBLEMS = [
    {
        "id": "NT-BH-01",
        "title": "Ancient Astronomy Calendar Synchronization & Planetary Alignment",
        "text": "Two celestial bodies orbit an ancient star with periods a and b days. Determine the integer step intervals x and y when their observation vectors align at offset c by solving the linear Diophantine equation a*x + b*y = c via extended Euclidean algorithm.",
        "expected_pattern": "nt_extended_gcd",
        "input": "21 14 7",
        "expected_output": lambda: "1 -1 7"
    },
    {
        "id": "NT-BH-02",
        "title": "Cryptographic RSA Decryption Key Exponent Inversion",
        "text": "In a secure cryptosystem, an encryption public exponent e and modulus m are provided. Compute the private decryption exponent d satisfying e * d = 1 (mod m) by evaluating the modular multiplicative inverse via extended GCD.",
        "expected_pattern": "nt_modular_inverse",
        "input": "65537 1000000007",
        "expected_output": lambda: str(modular_inverse(65537, 1000000007))
    },
    {
        "id": "NT-BH-03",
        "title": "Distributed Secret Sharing Residue Reconstruction",
        "text": "A vault's secret key is split among multiple cryptographic custodians, each holding a remainder r_i modulo a secure modulus m_i. Reconstruct the minimal positive secret value by solving this simultaneous system of modular congruences using the Chinese Remainder Theorem CRT.",
        "expected_pattern": "nt_chinese_remainder",
        "input": "3\n1 5\n4 7\n8 11",
        "expected_output": lambda: str(chinese_remainder([(1, 5), (4, 7), (8, 11)])[0])
    },
    {
        "id": "NT-BH-04",
        "title": "High-Throughput Genomic Prime Sequence Frequency Indexer",
        "text": "A bioinformatics pipeline requires fast precomputed prime counts and smallest prime factors up to N to analyze genomic hash seeds. Construct the list of primes and smallest prime factor spf table using Euler linear sieve.",
        "expected_pattern": "nt_linear_sieve",
        "input": "5000",
        "expected_output": lambda: "669"
    },
    {
        "id": "NT-BH-05",
        "title": "Network Security Coprime Port Assignment",
        "text": "A secure network router assigns communication ports that must share no common factors with a master encryption modulus N. Compute the number of coprime ports using Euler's totient phi function.",
        "expected_pattern": "nt_euler_totient",
        "input": "360",
        "expected_output": lambda: str(euler_totient_single(360))
    },
    {
        "id": "NT-BH-06",
        "title": "Quantum Lattice Point Coprimality & Ray Visibility",
        "text": "In a photonic laser simulation grid of dimensions N by M, calculate the number of unobstructed lattice points visible from the origin satisfying gcd(i, j) == 1 using Mobius inversion and square-free parity transforms.",
        "expected_pattern": "nt_mobius_inversion",
        "input": "50 50",
        "expected_output": lambda: str(coprime_pairs_grid(50, 50))
    },
    {
        "id": "NT-BH-07",
        "title": "Population Growth Matrix Transformation System",
        "text": "A biological organism ecosystem models population stage transitions via a linear recurrence. Predict the population vector at time step K by computing the transition matrix exponentiation to power k modulo 1000000007.",
        "expected_pattern": "nt_matrix_power",
        "input": "2 10 1000000007\n1 2\n1 0",
        "expected_output": lambda: "\n".join(" ".join(map(str, row)) for row in matrix_power([[1, 2], [1, 0]], 10, 1000000007))
    },
    {
        "id": "NT-BH-08",
        "title": "Lottery Ticket Selection & Distribution Paths",
        "text": "An entertainment system distributes prizes across lottery tickets. Compute the total combinations n choose k modulo 1000000007 of selecting k winning items from n options using precomputed factorials and inverse factorials.",
        "expected_pattern": "nt_combinatorics_factorials",
        "input": "100 25 1000000007",
        "expected_output": lambda: str(combinations_mod_p(100, 25, 1000000007))
    },
    {
        "id": "NT-BH-09",
        "title": "Intergalactic Spacecraft Route Configurations",
        "text": "An interstellar navigation computer must choose K navigation waypoints out of N cosmic beacons where N and K reach 10^18, evaluated modulo a small prime communication frequency p = 17. Compute combinations nCr mod p using Lucas theorem.",
        "expected_pattern": "nt_lucas_theorem",
        "input": "123456789012345 9876543210123 17",
        "expected_output": lambda: str(lucas_theorem(123456789012345, 9876543210123, 17))
    },
    {
        "id": "NT-BH-10",
        "title": "Cryptographic Certificate Prime Authenticity Verification",
        "text": "A public key infrastructure engine must verify whether an incoming 64-bit candidate integer is prime. Perform the primality test using deterministic Miller-Rabin test.",
        "expected_pattern": "nt_miller_rabin",
        "input": "18446744073709551557",
        "expected_output": lambda: "PRIME" if miller_rabin_deterministic(18446744073709551557) else "COMPOSITE"
    },
    {
        "id": "NT-BH-11",
        "title": "Gear Ratio Synchronization & Mechanical Step Balancing",
        "text": "A precision mechanical watch requires gear rotation matching. Given tooth counts a and b, compute the gear step teeth alignment solving linear Diophantine equation a*x + b*y = c via extended Euclidean algorithm.",
        "expected_pattern": "nt_extended_gcd",
        "input": "48 18 6",
        "expected_output": lambda: "-1 3 6"
    },
    {
        "id": "NT-BH-12",
        "title": "Distributed Blockchain Validator Quorum Residues",
        "text": "A decentralized network coordinates consensus slot timers across validators with asynchronous clock cycles. Determine the unified synchronization epoch by solving the system of modular congruences via Chinese Remainder Theorem CRT.",
        "expected_pattern": "nt_chinese_remainder",
        "input": "2\n17 19\n13 23",
        "expected_output": lambda: str(chinese_remainder([(17, 19), (13, 23)])[0])
    }
]


def run_blind_holdout() -> bool:
    print("=" * 80)
    print("CHUP Phase 3P — Number Theory & Combinatorics Blind Holdout Evaluation (12 Cases)")
    print("=" * 80)

    total = len(BLIND_HOLDOUT_PROBLEMS)
    passed = 0
    failed = 0

    for prob in BLIND_HOLDOUT_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]
        expected_pat = prob["expected_pattern"]
        stdin_data = prob["input"]
        expected_out = prob["expected_output"]()

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
        if cpp_output.strip() == expected_out.strip():
            passed += 1
            print(f"{pid} PASS: {title} (Pattern={expected_pat})")
        else:
            failed += 1
            print(f"{pid} FAIL: Output mismatch: expected '{expected_out}', got '{cpp_output}' ({title})")

    print("=" * 80)
    print(f"Blind Holdout Results: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("=" * 80)
    return passed == total


if __name__ == "__main__":
    success = run_blind_holdout()
    sys.exit(0 if success else 1)
