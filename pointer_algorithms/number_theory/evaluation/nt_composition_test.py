"""
CHUP Phase 3P — Number Theory Architecture Composition Tests.

Verifies the 5 Mandatory Core Composition Gates (Gates A–E) and algebraic pipelines:
1. Composition Gate A (Modular Inverse via ExtGCD): extended_gcd_builder -> modular_inverse_extgcd
2. Composition Gate A (Modular Inverse via Fermat): prime field -> fermat_inverse_builder
3. Composition Gate B (Non-coprime CRT System): crt_solver_builder with dynamic LCM tracking
4. Composition Gate C (Lucas Theorem Combinatorics): prime field + factorial table -> lucas_theorem_solver
5. Composition Gate D (Euler Totient Range Table): linear_sieve_builder -> euler_totient_sieve
6. Composition Gate D (Möbius Inversion Reducer): linear_sieve_builder -> mobius_sieve_builder -> mobius_inversion_reducer
7. Composition Gate E (Factorial Combinatorics): factorial_table_builder telescoping inverse factorials
8. Composition Algebraic (Matrix Exponentiation): matrix_exponentiation_builder recurrence evaluation

Total: 8 tests.
"""

import unittest
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.adv_graph.component_model import StateContract
from pointer_algorithms.number_theory.nt_state_contracts import (
    make_integer_state,
    make_diophantine_system_state,
    make_modular_ring_state,
    make_modular_inverse_state,
    make_crt_system_state,
    make_sieve_table_state,
    make_arithmetic_function_table_state,
    make_matrix_ring_state,
    make_factorial_table_state,
    make_lucas_decomposition_state,
    make_miller_rabin_result_state,
)
from pointer_algorithms.number_theory.component_model import (
    AlgorithmComponent,
    NumberTheoryComponentRegistry,
)


class TestNumberTheoryComposition(unittest.TestCase):

    def setUp(self):
        self.registry = NumberTheoryComponentRegistry()

    # ── 1. Composition Gate A: ExtGCD Modular Inverse Pipeline ──
    def test_01_gate_a_modular_inverse_extgcd_pipeline(self):
        extgcd = self.registry.get("extended_gcd_builder")
        mod_inv = self.registry.get("modular_inverse_extgcd")
        self.assertIsNotNone(extgcd)
        self.assertIsNotNone(mod_inv)

        # modular_inverse_extgcd requires capability EXTENDED_GCD
        self.assertIn("EXTENDED_GCD", mod_inv.requires_capabilities)
        # extended_gcd_builder provides EXTENDED_GCD
        self.assertIn("EXTENDED_GCD", extgcd.provided_capabilities)
        # modular_inverse_extgcd provides ModularInverseState
        prov_state = mod_inv.provides_states[0]
        self.assertEqual(prov_state.name, "ModularInverseState")
        self.assertEqual(prov_state.attributes.get("method"), "extgcd")

    # ── 2. Composition Gate A: Fermat Modular Inverse Pipeline ──
    def test_02_gate_a_fermat_modular_inverse_prime_field_pipeline(self):
        fermat_inv = self.registry.get("fermat_inverse_builder")
        self.assertIsNotNone(fermat_inv)

        # Requires ModularRingState with is_prime=True
        req_state = fermat_inv.requires_states[0]
        self.assertEqual(req_state.name, "ModularRingState")

        # Produces ModularInverseState with method=fermat
        prov_state = fermat_inv.provides_states[0]
        self.assertEqual(prov_state.name, "ModularInverseState")
        self.assertEqual(prov_state.attributes.get("method"), "fermat")

    # ── 3. Composition Gate B: Non-Coprime CRT Solver Pipeline ──
    def test_03_gate_b_non_coprime_crt_pipeline(self):
        crt_solver = self.registry.get("crt_solver_builder")
        extgcd = self.registry.get("extended_gcd_builder")
        self.assertIsNotNone(crt_solver)
        self.assertIsNotNone(extgcd)

        # CRT requires EXTENDED_GCD capability for pairwise congruence solving
        self.assertIn("EXTENDED_GCD", crt_solver.requires_capabilities)
        self.assertIn("EXTENDED_GCD", extgcd.provided_capabilities)

        # Operates on CRTSystemState
        prov = crt_solver.provides_states[0]
        self.assertEqual(prov.name, "CRTSystemState")

    # ── 4. Composition Gate C: Lucas Theorem Pipeline ──
    def test_04_gate_c_lucas_theorem_pipeline(self):
        lucas_solver = self.registry.get("lucas_theorem_solver")
        self.assertIsNotNone(lucas_solver)

        # Lucas requires LucasDecompositionState
        req_names = [s.name for s in lucas_solver.requires_states]
        self.assertIn("LucasDecompositionState", req_names)

        # Lucas provides LucasCombinatorialResultState
        self.assertTrue(any(s.name == "LucasCombinatorialResultState" for s in lucas_solver.provides_states))
        self.assertIn("LUCAS_THEOREM_EVALUATION", lucas_solver.provided_capabilities)

    # ── 5. Composition Gate D: Linear Sieve -> Euler Totient Table ──
    def test_05_gate_d_linear_sieve_euler_totient_pipeline(self):
        sieve = self.registry.get("linear_sieve_builder")
        phi_table = self.registry.get("euler_totient_sieve")
        self.assertIsNotNone(sieve)
        self.assertIsNotNone(phi_table)

        # euler_totient_sieve requires SieveTableState
        req_state = phi_table.requires_states[0]
        self.assertEqual(req_state.name, "SieveTableState")

        # linear_sieve_builder provides SieveTableState
        self.assertTrue(any(s.satisfies(req_state) for s in sieve.provides_states))

        # euler_totient_sieve provides ArithmeticFunctionTableState
        self.assertTrue(any(s.name == "ArithmeticFunctionTableState" for s in phi_table.provides_states))

    # ── 6. Composition Gate D: Linear Sieve -> Möbius Sieve -> Inversion Reducer ──
    def test_06_gate_d_linear_sieve_mobius_inversion_pipeline(self):
        sieve = self.registry.get("linear_sieve_builder")
        mu_table = self.registry.get("mobius_sieve_builder")
        reducer = self.registry.get("mobius_inversion_reducer")
        self.assertIsNotNone(sieve)
        self.assertIsNotNone(mu_table)
        self.assertIsNotNone(reducer)

        # mobius_sieve_builder requires SieveTableState
        req_sieve = mu_table.requires_states[0]
        self.assertTrue(any(s.satisfies(req_sieve) for s in sieve.provides_states))

        # mobius_inversion_reducer requires ArithmeticFunctionTableState
        req_arith = reducer.requires_states[0]
        self.assertTrue(any(s.satisfies(req_arith) for s in mu_table.provides_states))

    # ── 7. Composition Gate E: Factorial Combinatorics Telescoping Pipeline ──
    def test_07_gate_e_factorial_combinatorics_telescoping_pipeline(self):
        fact_builder = self.registry.get("factorial_table_builder")
        self.assertIsNotNone(fact_builder)

        # Requires ModularRingState
        req_names = [s.name for s in fact_builder.requires_states]
        self.assertIn("ModularRingState", req_names)

        # Provides FactorialTableState
        self.assertTrue(any(s.name == "FactorialTableState" for s in fact_builder.provides_states))
        self.assertIn("COMBINATORIAL_COEFFICIENTS_O1", fact_builder.provided_capabilities)

    # ── 8. Composition Algebraic: Matrix Exponentiation Pipeline ──
    def test_08_algebraic_matrix_exponentiation_pipeline(self):
        mat_exp = self.registry.get("matrix_exponentiation_builder")
        self.assertIsNotNone(mat_exp)

        # Requires MatrixRingState
        req_names = [s.name for s in mat_exp.requires_states]
        self.assertIn("MatrixRingState", req_names)

        # Provides MatrixRingState with power computed
        self.assertTrue(any(s.name == "MatrixRingState" for s in mat_exp.provides_states))
        self.assertIn("MATRIX_EXPONENTIATION_RING", mat_exp.provided_capabilities)


if __name__ == "__main__":
    unittest.main()
