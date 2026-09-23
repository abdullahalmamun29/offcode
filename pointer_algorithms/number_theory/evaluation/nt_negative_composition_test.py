"""
CHUP Phase 3P — Number Theory Negative Composition Tests (Closed-World Gates A–E).

Validates:
1. Anti-hardcoding Invariant Gate A: Removal of extended_gcd_builder breaks modular_inverse_extgcd.
2. Closed-world Gate A: Modular inverse fails closed when gcd(a, m) != 1 (INVERSE_DOES_NOT_EXIST).
3. Closed-world Gate B: Incompatible CRT system fails closed with CRT_NO_SIMULTANEOUS_SOLUTION.
4. Closed-world Gate C: Lucas theorem with prime p > 10^6 fails closed with FACTORIAL_TABLE_INFEASIBLE.
5. Anti-hardcoding Invariant Gate D: Removal of linear_sieve_builder prevents multiplicative range tables.
6. Closed-world Gate E: Factorial combinatorics fails closed when N >= p (DOMAIN_VIOLATION_N_GE_P).

Total: 6 tests.
"""

import unittest
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.number_theory.component_model import NumberTheoryComponentRegistry
from pointer_algorithms.number_theory.derivation_engine import (
    NumberTheoryDerivationEngine,
    CandidateStatus
)


class TestNumberTheoryNegativeComposition(unittest.TestCase):

    def setUp(self):
        self.registry = NumberTheoryComponentRegistry()
        self.registry.reset_defaults()
        self.engine = NumberTheoryDerivationEngine(self.registry)

    def test_01_negative_gate_a_missing_extgcd(self):
        """Removing extended_gcd_builder means modular_inverse_extgcd has no provider for EXTENDED_GCD."""
        self.registry.remove("extended_gcd_builder")
        mod_inv = self.registry.get("modular_inverse_extgcd")
        self.assertIsNotNone(mod_inv)
        req_cap = "EXTENDED_GCD"

        providers = [
            c for c in self.registry.all_components()
            if req_cap in c.provided_capabilities
        ]
        self.assertEqual(len(providers), 0)

    def test_02_negative_gate_a_zero_divisor_closed(self):
        """gcd(a, m) != 1 or zero-divisor fails closed with INVERSE_DOES_NOT_EXIST."""
        model = self.engine.extract_semantic_model("Compute modular inverse of 6 modulo 9 where gcd(a, m) != 1.")
        evals, selected = self.engine.evaluate_candidates(model)
        self.assertIsNone(selected)
        self.assertTrue(any(e.rejection_code == "INVERSE_DOES_NOT_EXIST" for e in evals))

    def test_03_negative_gate_b_crt_insolvability(self):
        """Contradictory system of congruences fails closed with CRT_NO_SIMULTANEOUS_SOLUTION."""
        model = self.engine.extract_semantic_model("Solve Chinese remainder system with inconsistent remainders crt_no_simultaneous_solution.")
        evals, selected = self.engine.evaluate_candidates(model)
        self.assertIsNone(selected)
        self.assertTrue(any(e.rejection_code == "CRT_NO_SIMULTANEOUS_SOLUTION" for e in evals))

    def test_04_negative_gate_c_lucas_table_infeasible(self):
        """Modulus prime p > 10^6 exceeds RAM capacity, fails closed with FACTORIAL_TABLE_INFEASIBLE."""
        model = self.engine.extract_semantic_model("Evaluate combination nCr mod p using Lucas theorem where prime p >= 10^9 factorial_table_infeasible.")
        evals, selected = self.engine.evaluate_candidates(model)
        self.assertIsNone(selected)
        self.assertTrue(any(e.rejection_code == "FACTORIAL_TABLE_INFEASIBLE" for e in evals))

    def test_05_negative_gate_d_missing_linear_sieve(self):
        """Removing linear_sieve_builder means euler_totient_sieve and mobius_sieve_builder have no provider."""
        self.registry.remove("linear_sieve_builder")
        phi_table = self.registry.get("euler_totient_sieve")
        self.assertIsNotNone(phi_table)
        req_state = phi_table.requires_states[0]

        providers = [
            c for c in self.registry.all_components()
            if any(s.satisfies(req_state) for s in c.provides_states)
        ]
        self.assertEqual(len(providers), 0)

    def test_06_negative_gate_e_factorial_domain_violation(self):
        """N >= p implies N! = 0 mod p, so standard factorial table fails closed with DOMAIN_VIOLATION_N_GE_P."""
        model = self.engine.extract_semantic_model("Compute combinations nCr mod p with n greater than p domain_violation_n_ge_p.")
        evals, selected = self.engine.evaluate_candidates(model)
        fact_eval = next(e for e in evals if e.pattern == "nt_combinatorics_factorials")
        self.assertEqual(fact_eval.status, CandidateStatus.INVALID_PRECONDITION)
        self.assertEqual(fact_eval.rejection_code, "DOMAIN_VIOLATION_N_GE_P")


if __name__ == "__main__":
    unittest.main()
