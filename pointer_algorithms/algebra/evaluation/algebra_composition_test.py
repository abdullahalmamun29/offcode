"""
CHUP Phase 3Q — Positive Capability Composition Test Suite (8 Cases).

Validates end-to-end capability synthesis chains across algebraic and transform domains:
1. NTT Pipeline: Prime -> Primitive Root -> Order -> NTT -> Polynomial Multiplication
2. Newton Inversion Pipeline: Multiplier Provider + Unit Constant -> Inversion
3. Modular Linear Algebra: Prime Certificate -> Modular Matrix -> Gauss Elimination
4. Linear Recurrence Pipeline: Sequence -> Field -> Berlekamp-Massey -> Recurrence Evaluator
5. Lagrange Interpolation: Distinct Nodes + Domain Bounds -> O(d) Point Evaluator
6. XOR Linear Basis: Vectors in F_2^B -> Echelon Basis -> Maximum XOR
7. Real Linear Algebra: Real Matrix + FloatingPointPolicy -> Approximate Gauss
8. FWHT Pipeline: Hypercube Domain -> Fast Walsh-Hadamard -> Exact XOR Convolution
"""

import sys
import os
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.algebra.semantic_ontology import (
    SemanticAlgebraModel,
    TransformDomainType,
    AlgebraicFieldType,
    MatrixScalarDomain,
    AlgebraObjective,
    FloatingPointPolicy,
)
from pointer_algorithms.algebra.algebra_state_contracts import (
    StateContract,
    make_finite_field_transform_domain_state,
    make_polynomial_ring_state,
    make_modular_matrix_state,
    make_real_matrix_state,
    make_linear_basis_state,
    make_linear_recurrence_state,
    make_interpolation_points_state,
    make_walsh_hypercube_domain_state,
)
from pointer_algorithms.algebra.component_model import AlgebraComponentRegistry
from pointer_algorithms.algebra.derivation_engine import AlgebraDerivationEngine


class TestAlgebraComposition(unittest.TestCase):

    def setUp(self):
        self.engine = AlgebraDerivationEngine()
        self.registry = AlgebraComponentRegistry()

    def test_comp_01_ntt_pipeline(self):
        cert = StateContract("MillerRabinResultState", {"result": True, "n": 998244353, "deterministic_64bit": True})
        ntt_domain = make_finite_field_transform_domain_state(998244353, 3, 1024, prime_certificate=cert)
        self.assertTrue(ntt_domain.attributes["is_valid_ntt"])
        providers = self.registry.find_providers("POLYNOMIAL_MULTIPLICATION_CAPABILITY")
        ntt_provider = [p for p in providers if p.name == "ntt_polynomial_multiply"][0]
        self.assertEqual(ntt_provider.correctness_guarantee, "DETERMINISTIC_EXACT")

    def test_comp_02_newton_inversion_pipeline(self):
        poly_ring = make_polynomial_ring_state("PRIME_FIELD", constant_term=3, modulus=998244353)
        self.assertTrue(poly_ring.attributes["constant_term_is_unit"])
        inv_comp = self.registry.get("polynomial_inverse_builder")
        self.assertIn("POLYNOMIAL_MULTIPLICATION_CAPABILITY", inv_comp.requires_capabilities)
        model = self.engine.extract_semantic_model("Compute polynomial inverse modulo 998244353")
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertEqual(sel, "algebra_poly_inverse")
        self.assertEqual(evals[0].correctness_guarantee, "DETERMINISTIC_EXACT")

    def test_comp_03_modular_linear_algebra(self):
        cert = StateContract("MillerRabinResultState", {"result": True, "n": 998244353})
        mod_mat = make_modular_matrix_state(3, 3, 998244353, prime_certificate=cert)
        self.assertTrue(mod_mat.attributes["is_field"])
        model = self.engine.extract_semantic_model("Solve modular system of equations modulo 998244353")
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertEqual(sel, "algebra_gauss_modular")
        self.assertEqual(evals[0].correctness_guarantee, "DETERMINISTIC_EXACT")

    def test_comp_04_linear_recurrence_pipeline(self):
        rec_state = make_linear_recurrence_state(terms_count=10, modulus=998244353, is_field=True)
        self.assertTrue(rec_state.attributes["is_field"])
        evaluator = self.registry.get("linear_recurrence_evaluator")
        self.assertIn("MINIMAL_LINEAR_RECURRENCE_POLYNOMIAL", evaluator.requires_capabilities)
        self.assertIn("POLYNOMIAL_MULTIPLICATION_CAPABILITY", evaluator.requires_capabilities)
        model = self.engine.extract_semantic_model("Find linear recurrence via Berlekamp-Massey modulo 998244353 and evaluate nth term")
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertEqual(sel, "algebra_berlekamp_massey")

    def test_comp_05_lagrange_interpolation_pipeline(self):
        pts = make_interpolation_points_state(points_count=50, is_contiguous=True, modulus=998244353)
        self.assertTrue(pts.attributes["contiguous_domain_valid"])
        model = self.engine.extract_semantic_model("Lagrange interpolation from contiguous points 0 to d modulo 998244353")
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertEqual(sel, "algebra_lagrange_interpolation")
        self.assertEqual(evals[0].complexity, "O(d)")

    def test_comp_06_xor_linear_basis_pipeline(self):
        basis = make_linear_basis_state(64)
        self.assertEqual(basis.attributes["bit_width"], 64)
        model = self.engine.extract_semantic_model("Maintain online linear basis and query maximum xor subset in F_2")
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertEqual(sel, "algebra_linear_basis")
        self.assertEqual(evals[0].correctness_guarantee, "DETERMINISTIC_EXACT")

    def test_comp_07_real_linear_algebra_pipeline(self):
        policy = FloatingPointPolicy(absolute_tolerance=1e-8, relative_tolerance=1e-8)
        real_mat = make_real_matrix_state(4, 4, floating_point_policy=policy)
        self.assertEqual(real_mat.attributes["abs_tolerance"], 1e-8)
        model = self.engine.extract_semantic_model("Solve real floating-point system of linear equations A*x = b with determinant")
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertEqual(sel, "algebra_gauss_real")
        self.assertEqual(evals[0].correctness_guarantee, "CORRECTNESS_NUMERIC_APPROXIMATE")

    def test_comp_08_fwht_xor_pipeline(self):
        hypercube = make_walsh_hypercube_domain_state(10, modulus=998244353)
        self.assertTrue(hypercube.attributes["normalization_invertible"])
        model = self.engine.extract_semantic_model("Fast Walsh-Hadamard Transform FWHT bitwise xor convolution")
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertEqual(sel, "algebra_fwht")
        self.assertEqual(evals[0].correctness_guarantee, "DETERMINISTIC_EXACT")


if __name__ == "__main__":
    unittest.main()
