"""
CHUP Phase 3Q — Negative Closed-World Gate Test Suite (6 Cases).

Validates fail-closed proof gates A through I:
1. Gate A: Non-NTT modulus fails closed with NTT_UNSUPPORTED_MODULUS
2. Gate B: Inconsistent system (SYSTEM_INCONSISTENT) & Singular matrix (MATRIX_SINGULAR_NON_INVERTIBLE)
3. Gate C: Constant term non-unit fails closed with POLYNOMIAL_CONSTANT_TERM_NOT_A_UNIT
4. Gate D: Non-power-of-two transform length fails closed with TRANSFORM_LENGTH_NOT_POWER_OF_TWO
5. Gate E & F: Basis bitwidth overflow (BASIS_BITWIDTH_OVERFLOW) & BM field failure (BERLEKAMP_MASSEY_REQUIRES_FIELD)
6. Gate G, H, I: Duplicate interpolation nodes, missing multiplier, and singular pivot below tolerance
"""

import sys
import os
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.algebra.derivation_engine import AlgebraDerivationEngine, CandidateStatus


class TestAlgebraNegativeComposition(unittest.TestCase):

    def setUp(self):
        self.engine = AlgebraDerivationEngine()

    def test_neg_01_gate_a_ntt_modulus_rejection(self):
        text = "Compute NTT polynomial multiplication modulo 1000000007 non-ntt modulus"
        model = self.engine.extract_semantic_model(text)
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].rejection_code, "NTT_UNSUPPORTED_MODULUS")
        self.assertEqual(evals[0].status, CandidateStatus.INVALID_PRECONDITION)

    def test_neg_02_gate_b_system_inconsistent_and_singular(self):
        # Inconsistent
        text1 = "Solve linear equations A*x = b with system_inconsistent"
        model1 = self.engine.extract_semantic_model(text1)
        evals1, sel1 = self.engine.evaluate_candidates(model1)
        self.assertIsNone(sel1)
        self.assertEqual(evals1[0].rejection_code, "SYSTEM_INCONSISTENT")

        # Singular
        text2 = "Compute inverse of matrix with matrix_singular_non_invertible"
        model2 = self.engine.extract_semantic_model(text2)
        evals2, sel2 = self.engine.evaluate_candidates(model2)
        self.assertIsNone(sel2)
        self.assertEqual(evals2[0].rejection_code, "MATRIX_SINGULAR_NON_INVERTIBLE")

    def test_neg_03_gate_c_polynomial_constant_term_not_unit(self):
        text = "Find power series inverse with polynomial_constant_term_not_a_unit A(0) == 0"
        model = self.engine.extract_semantic_model(text)
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].rejection_code, "POLYNOMIAL_CONSTANT_TERM_NOT_A_UNIT")

    def test_neg_04_gate_d_transform_length_power_of_two(self):
        text = "Execute FFT transform_length_not_power_of_two length is not power"
        model = self.engine.extract_semantic_model(text)
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].rejection_code, "TRANSFORM_LENGTH_NOT_POWER_OF_TWO")

    def test_neg_05_gate_e_basis_overflow_and_gate_f_bm_field(self):
        # Gate E
        text1 = "Insert into linear basis with basis_bitwidth_overflow value >= 2^B"
        m1 = self.engine.extract_semantic_model(text1)
        ev1, s1 = self.engine.evaluate_candidates(m1)
        self.assertIsNone(s1)
        self.assertEqual(ev1[0].rejection_code, "BASIS_BITWIDTH_OVERFLOW")

        # Gate F
        text2 = "Berlekamp-Massey on composite modulus with berlekamp_massey_requires_field"
        m2 = self.engine.extract_semantic_model(text2)
        ev2, s2 = self.engine.evaluate_candidates(m2)
        self.assertIsNone(s2)
        self.assertEqual(ev2[0].rejection_code, "BERLEKAMP_MASSEY_REQUIRES_FIELD")

    def test_neg_06_gate_g_interpolation_and_gate_h_i(self):
        # Gate G
        text1 = "Lagrange interpolation with duplicate nodes interpolation_nodes_not_distinct"
        m1 = self.engine.extract_semantic_model(text1)
        ev1, s1 = self.engine.evaluate_candidates(m1)
        self.assertIsNone(s1)
        self.assertEqual(ev1[0].rejection_code, "INTERPOLATION_NODES_NOT_DISTINCT")

        # Gate H
        text2 = "Polynomial inverse with no_multiplication_provider"
        m2 = self.engine.extract_semantic_model(text2)
        ev2, s2 = self.engine.evaluate_candidates(m2)
        self.assertIsNone(s2)
        self.assertEqual(ev2[0].rejection_code, "NO_MULTIPLICATION_PROVIDER")

        # Gate I
        text3 = "Real Gaussian elimination with numeric_singular_pivot pivot < eps"
        m3 = self.engine.extract_semantic_model(text3)
        ev3, s3 = self.engine.evaluate_candidates(m3)
        self.assertIsNone(s3)
        self.assertEqual(ev3[0].rejection_code, "NUMERIC_SINGULAR_PIVOT")


if __name__ == "__main__":
    unittest.main()
