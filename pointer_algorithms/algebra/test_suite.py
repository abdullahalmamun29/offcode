"""
CHUP Phase 3Q — Comprehensive Unit Test Suite (26 Tests).

Verifies the 9 hardened contract areas, state contracts, component registry,
closed-world proof gates (Gates A–I), derivation engine, and C++ code generator.
"""

import unittest
import math
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.algebra.semantic_ontology import (
    SemanticAlgebraModel,
    TransformDomainType,
    AlgebraicFieldType,
    MatrixScalarDomain,
    BasisBitwidth,
    CorrectnessGuarantee,
    AlgebraObjective,
    FloatingPointPolicy,
    DerivedFact,
    ProvenanceStatus,
)
from pointer_algorithms.algebra.algebra_state_contracts import (
    StateContract,
    make_complex_transform_domain_state,
    make_finite_field_transform_domain_state,
    make_walsh_hypercube_domain_state,
    make_polynomial_ring_state,
    make_real_matrix_state,
    make_modular_matrix_state,
    make_bitset_matrix_state,
    make_linear_basis_state,
    make_linear_recurrence_state,
    make_interpolation_points_state,
)
from pointer_algorithms.algebra.component_model import AlgebraComponentRegistry, AlgorithmComponent
from pointer_algorithms.algebra.derivation_engine import (
    AlgebraDerivationEngine,
    CandidateStatus,
    SelectionStatus,
)


class TestPhase3QAlgebra(unittest.TestCase):

    def setUp(self):
        self.engine = AlgebraDerivationEngine()
        self.registry = AlgebraComponentRegistry()

    # ── Test 01: Ontology Primitive Dimensions ──
    def test_01_ontology_primitive_dimensions(self):
        self.assertEqual(TransformDomainType.COMPLEX_FIELD, "COMPLEX_FIELD")
        self.assertEqual(TransformDomainType.FINITE_FIELD_ROOTS, "FINITE_FIELD_ROOTS")
        self.assertEqual(TransformDomainType.WALSH_HYPERCUBE, "WALSH_HYPERCUBE")
        self.assertEqual(AlgebraicFieldType.PRIME_FIELD, "PRIME_FIELD")
        self.assertEqual(AlgebraicFieldType.BINARY_FIELD_F2, "BINARY_FIELD_F2")
        self.assertEqual(CorrectnessGuarantee.DETERMINISTIC_EXACT, "DETERMINISTIC_EXACT")
        self.assertEqual(CorrectnessGuarantee.CORRECTNESS_NUMERIC_APPROXIMATE, "CORRECTNESS_NUMERIC_APPROXIMATE")

    # ── Test 02: FloatingPointPolicy Semantics ──
    def test_02_floating_point_policy_semantics(self):
        policy = FloatingPointPolicy(absolute_tolerance=1e-9, relative_tolerance=1e-6)
        self.assertTrue(policy.is_pivot_acceptable(1e-5, row_scale=1.0))
        self.assertFalse(policy.is_pivot_acceptable(1e-10, row_scale=1.0))
        # Relative tolerance scaling
        self.assertFalse(policy.is_pivot_acceptable(1e-5, row_scale=1e3))  # 1e-6 * 1e3 = 1e-3 > 1e-5

    # ── Test 03: DerivedFact Provenance ──
    def test_03_derived_fact_provenance(self):
        fact = DerivedFact(
            fact_id="PRIME_MODULUS_CERTIFIED",
            value=True,
            source_facts=["modulus_998244353"],
            derivation_rule="MILLER_RABIN_7_WITNESS",
            proof_obligations=["witness_basis_soundness"],
            status=ProvenanceStatus.PROVEN
        )
        self.assertEqual(fact.status, ProvenanceStatus.PROVEN)
        self.assertTrue(fact.value)

    # ── Test 04: Complex Transform Domain Contract ──
    def test_04_complex_transform_domain_contract(self):
        state = make_complex_transform_domain_state(1024)
        self.assertTrue(state.attributes["is_power_of_two"])
        self.assertEqual(state.attributes["correctness_guarantee"], "CORRECTNESS_NUMERIC_APPROXIMATE")
        odd_state = make_complex_transform_domain_state(1000)
        self.assertFalse(odd_state.attributes["is_power_of_two"])

    # ── Test 05: NTT Domain 3-Tier Provenance Contract ──
    def test_05_ntt_domain_3tier_provenance(self):
        cert = StateContract(
            name="MillerRabinResultState",
            attributes={"result": True, "n": 998244353, "deterministic_64bit": True}
        )
        valid_ntt = make_finite_field_transform_domain_state(998244353, 3, 1024, prime_certificate=cert)
        self.assertTrue(valid_ntt.attributes["is_valid_ntt"])
        self.assertTrue(valid_ntt.attributes["root_order_certified"])
        self.assertEqual(valid_ntt.attributes["correctness_guarantee"], "DETERMINISTIC_EXACT")

        # Modulus not dividing target length
        invalid_ntt = make_finite_field_transform_domain_state(1000000007, 5, 1024, prime_certificate=cert)
        self.assertFalse(invalid_ntt.attributes["is_valid_ntt"])

    # ── Test 06: FWHT Domain Normalization Contract ──
    def test_06_fwht_domain_normalization_contract(self):
        fwht_state = make_walsh_hypercube_domain_state(10, modulus=998244353)
        self.assertTrue(fwht_state.attributes["normalization_invertible"])
        # Even modulus where 2^B has common factor
        fwht_even = make_walsh_hypercube_domain_state(10, modulus=1000)
        self.assertFalse(fwht_even.attributes["normalization_invertible"])

    # ── Test 07: PolynomialRingState NOT a Field ──
    def test_07_polynomial_ring_not_a_field(self):
        ring_state = make_polynomial_ring_state(coefficient_domain="PRIME_FIELD", constant_term=5)
        self.assertNotIn("FieldState", ring_state.supertypes)
        self.assertTrue(ring_state.attributes["constant_term_is_unit"])
        zero_ring = make_polynomial_ring_state(coefficient_domain="PRIME_FIELD", constant_term=0)
        self.assertFalse(zero_ring.attributes["constant_term_is_unit"])
        composite_ring = make_polynomial_ring_state(coefficient_domain="GENERAL_RING", constant_term=4, modulus=6)
        self.assertFalse(composite_ring.attributes["constant_term_is_unit"])

    # ── Test 08: Matrix States Mutually Non-Substitutable ──
    def test_08_matrix_states_substitutability(self):
        real_mat = make_real_matrix_state(3, 3)
        mod_mat = make_modular_matrix_state(3, 3, 998244353)
        bitset_mat = make_bitset_matrix_state(3, 3)
        self.assertFalse(real_mat.satisfies(mod_mat))
        self.assertFalse(mod_mat.satisfies(bitset_mat))
        self.assertFalse(bitset_mat.satisfies(real_mat))

    # ── Test 09: LinearBasisState NOT Substitutable for BitsetMatrixState ──
    def test_09_linear_basis_not_substitutable_for_bitset_matrix(self):
        basis = make_linear_basis_state(64)
        bitset_mat = make_bitset_matrix_state(64, 64)
        self.assertFalse(basis.satisfies(bitset_mat))
        self.assertFalse(bitset_mat.satisfies(basis))

    # ── Test 10: Linear Recurrence Field Requirement Contract ──
    def test_10_linear_recurrence_field_requirement(self):
        valid_bm = make_linear_recurrence_state(terms_count=10, modulus=998244353, is_field=True)
        self.assertTrue(valid_bm.attributes["is_field"])
        invalid_bm = make_linear_recurrence_state(terms_count=10, modulus=1000, is_field=False)
        self.assertFalse(invalid_bm.attributes["is_field"])

    # ── Test 11: Interpolation Points Distinctness & Domain ──
    def test_11_interpolation_points_distinctness_and_domain(self):
        pts = make_interpolation_points_state(points_count=100, is_contiguous=True, modulus=998244353)
        self.assertTrue(pts.attributes["contiguous_domain_valid"])
        pts_collapse = make_interpolation_points_state(points_count=100, is_contiguous=True, modulus=50)
        self.assertFalse(pts_collapse.attributes["contiguous_domain_valid"])

    # ── Test 12: Component Registry Registration & Provider Discovery ──
    def test_12_component_registry_registration(self):
        providers = self.registry.find_providers("POLYNOMIAL_MULTIPLICATION_CAPABILITY")
        names = [p.name for p in providers]
        self.assertIn("ntt_polynomial_multiply", names)
        self.assertIn("fft_polynomial_multiply", names)
        self.assertIn("naive_polynomial_multiply", names)

    # ── Test 13: Gate A (NTT Unsupported Modulus) ──
    def test_13_gate_a_ntt_unsupported_modulus(self):
        text = "Perform NTT polynomial multiplication modulo 1000000007 unsupported NTT modulus"
        model = self.engine.extract_semantic_model(text)
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].rejection_code, "NTT_UNSUPPORTED_MODULUS")

    # ── Test 14: Gate B (System Inconsistent) ──
    def test_14_gate_b_system_inconsistent(self):
        text = "Solve system of linear equations A*x = b system_inconsistent"
        model = self.engine.extract_semantic_model(text)
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].rejection_code, "SYSTEM_INCONSISTENT")

    # ── Test 15: Gate B (Matrix Singular) ──
    def test_15_gate_b_matrix_singular(self):
        text = "Compute matrix inverse of real matrix matrix_singular_non_invertible"
        model = self.engine.extract_semantic_model(text)
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].rejection_code, "MATRIX_SINGULAR_NON_INVERTIBLE")

    # ── Test 16: Gate C (Polynomial Constant Term Not a Unit) ──
    def test_16_gate_c_polynomial_constant_term_not_unit(self):
        text = "Compute formal power series inverse A(x)^(-1) mod x^n with polynomial_constant_term_not_a_unit A(0) == 0"
        model = self.engine.extract_semantic_model(text)
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].rejection_code, "POLYNOMIAL_CONSTANT_TERM_NOT_A_UNIT")

    # ── Test 17: Gate D (Transform Length Not Power of Two) ──
    def test_17_gate_d_transform_length_not_power_of_two(self):
        text = "Fast Fourier transform FFT with transform_length_not_power_of_two length is not power"
        model = self.engine.extract_semantic_model(text)
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].rejection_code, "TRANSFORM_LENGTH_NOT_POWER_OF_TWO")

    # ── Test 18: Gate E (Basis Bitwidth Overflow) ──
    def test_18_gate_e_basis_bitwidth_overflow(self):
        text = "Insert into linear basis with basis_bitwidth_overflow value >= 2^B"
        model = self.engine.extract_semantic_model(text)
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].rejection_code, "BASIS_BITWIDTH_OVERFLOW")

    # ── Test 19: Gate F (Berlekamp-Massey Requires Field) ──
    def test_19_gate_f_berlekamp_massey_requires_field(self):
        text = "Find recurrence via Berlekamp-Massey on composite modulus bm with berlekamp_massey_requires_field"
        model = self.engine.extract_semantic_model(text)
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].rejection_code, "BERLEKAMP_MASSEY_REQUIRES_FIELD")

    # ── Test 20: Gate G (Interpolation Nodes Not Distinct) ──
    def test_20_gate_g_interpolation_nodes_not_distinct(self):
        text = "Lagrange interpolation with duplicate nodes interpolation_nodes_not_distinct"
        model = self.engine.extract_semantic_model(text)
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].rejection_code, "INTERPOLATION_NODES_NOT_DISTINCT")

    # ── Test 21: Gate G (Contiguous Interpolation Domain Exceeded) ──
    def test_21_gate_g_contiguous_domain_exceeded(self):
        text = "Lagrange interpolation with contiguous nodes contiguous_interpolation_domain_exceeded d >= p"
        model = self.engine.extract_semantic_model(text)
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].rejection_code, "CONTIGUOUS_INTERPOLATION_DOMAIN_EXCEEDED")

    # ── Test 22: Gate H (No Multiplication Provider) ──
    def test_22_gate_h_no_multiplication_provider(self):
        text = "Formal power series inverse polynomial inverse with no_multiplication_provider"
        model = self.engine.extract_semantic_model(text)
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].rejection_code, "NO_MULTIPLICATION_PROVIDER")

    # ── Test 23: Gate I (Numeric Singular Pivot Under FloatingPointPolicy) ──
    def test_23_gate_i_numeric_singular_pivot(self):
        text = "Gaussian elimination real matrix with numeric_singular_pivot pivot < eps"
        model = self.engine.extract_semantic_model(text)
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].rejection_code, "NUMERIC_SINGULAR_PIVOT")

    # ── Test 24: Newton Inversion Provider-Relative Complexity & Guarantee ──
    def test_24_newton_inversion_complexity_and_guarantee_propagation(self):
        text = "Compute polynomial inverse A(x)^(-1) mod x^n modulo 998244353"
        model = self.engine.extract_semantic_model(text)
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertEqual(sel, "algebra_poly_inverse")
        self.assertIn("O(M(N))", evals[0].complexity)
        self.assertEqual(evals[0].correctness_guarantee, "DETERMINISTIC_EXACT")

    # ── Test 25: Out-of-Scope Rejections ──
    def test_25_out_of_scope_rejection(self):
        nonlinear_text = "Solve system of nonlinear algebraic equations via Newton-Raphson"
        m1 = self.engine.extract_semantic_model(nonlinear_text)
        ev1, s1 = self.engine.evaluate_candidates(m1)
        self.assertIsNone(s1)
        self.assertEqual(ev1[0].rejection_code, "NONLINEAR_SYSTEM_UNSUPPORTED")

        sim_text = "Run discrete event simulation on algebraic cellular automata"
        m2 = self.engine.extract_semantic_model(sim_text)
        ev2, s2 = self.engine.evaluate_candidates(m2)
        self.assertIsNone(s2)
        self.assertEqual(ev2[0].rejection_code, "SIMULATION_UNSUPPORTED")

    # ── Test 26: C++ Generator Emission for all 10 Patterns ──
    def test_26_cpp_generator_emission_all_10_patterns(self):
        patterns = [
            "algebra_fft",
            "algebra_ntt",
            "algebra_fwht",
            "algebra_poly_inverse",
            "algebra_gauss_real",
            "algebra_gauss_modular",
            "algebra_gauss_xor",
            "algebra_linear_basis",
            "algebra_berlekamp_massey",
            "algebra_lagrange_interpolation",
        ]
        for p in patterns:
            code = self.engine.generate_cpp_solution(p)
            self.assertIn("#include <iostream>", code)
            self.assertIn("int main()", code)


if __name__ == "__main__":
    unittest.main()
