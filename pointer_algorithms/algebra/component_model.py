"""
CHUP Phase 3Q — Algebra Component Model & Registry.

Defines declarative AlgorithmComponent nodes with state requirements, preconditions,
proof obligations, provider-relative complexity contracts, and explicit composition dependencies.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any

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


class CompositionNodeType(str, Enum):
    COMPONENT = "COMPONENT"
    TRANSFORMATION = "TRANSFORMATION"


@dataclass
class AlgorithmComponent:
    """
    Formal specification of a reusable algebraic or transformation component.
    """
    name: str
    node_type: CompositionNodeType = CompositionNodeType.COMPONENT
    consumes_state: List[StateContract] = field(default_factory=list)
    produces_state: List[StateContract] = field(default_factory=list)
    requires_capabilities: List[str] = field(default_factory=list)
    provided_capabilities: List[str] = field(default_factory=list)
    preconditions: List[str] = field(default_factory=list)
    proof_obligations: List[str] = field(default_factory=list)
    operation_complexity: str = ""
    space_complexity: str = ""
    correctness_guarantee: str = "DETERMINISTIC_EXACT"
    description: str = ""


class AlgebraComponentRegistry:
    """
    Centralized registry for all Phase 3Q Algebra / Transforms components.
    """
    _instance: Optional['AlgebraComponentRegistry'] = None

    def __new__(cls) -> 'AlgebraComponentRegistry':
        if cls._instance is None:
            cls._instance = super(AlgebraComponentRegistry, cls).__new__(cls)
            cls._instance._components = {}
            cls._instance._register_default_components()
        return cls._instance

    def __init__(self) -> None:
        pass

    def register(self, component: AlgorithmComponent) -> None:
        self._components[component.name] = component

    def get(self, name: str) -> Optional[AlgorithmComponent]:
        return self._components.get(name)

    def remove(self, name: str) -> Optional[AlgorithmComponent]:
        return self._components.pop(name, None)

    def all_components(self) -> List[AlgorithmComponent]:
        return list(self._components.values())

    def reset_defaults(self) -> None:
        self._components.clear()
        self._register_default_components()

    def find_providers(self, capability: str) -> List[AlgorithmComponent]:
        return [c for c in self._components.values() if capability in c.provided_capabilities]

    def _register_default_components(self) -> None:
        # ── 1. Fast Fourier Transform (Complex Numerical) ──
        self.register(AlgorithmComponent(
            name="fast_fourier_transform_builder",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_complex_transform_domain_state()],
            produces_state=[StateContract("FFTTransformedState")],
            requires_capabilities=[],
            provided_capabilities=["FAST_FOURIER_TRANSFORM", "COMPLEX_CONVOLUTION"],
            preconditions=["transform_length_is_power_of_two", "length_gt_0"],
            proof_obligations=["cooley_tukey_bit_reversal_soundness", "twiddle_factor_periodicity_proven"],
            operation_complexity="O(N log N) floating-point operations",
            space_complexity="O(N) complex buffer",
            correctness_guarantee="CORRECTNESS_NUMERIC_APPROXIMATE",
            description="Cooley-Tukey Radix-2 DIT/DIF complex continuous FFT with bit-reversal."
        ))

        # ── 2. Number Theoretic Transform (Exact Modular F_p) ──
        self.register(AlgorithmComponent(
            name="number_theoretic_transform_builder",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_finite_field_transform_domain_state()],
            produces_state=[StateContract("NTTTransformedState")],
            requires_capabilities=[],
            provided_capabilities=["NUMBER_THEORETIC_TRANSFORM", "EXACT_MODULAR_CONVOLUTION"],
            preconditions=["prime_modulus_certified", "length_is_power_of_two", "modulus_minus_one_divisible_by_length", "root_order_certified"],
            proof_obligations=["finite_field_root_of_unity_order_proven", "butterfly_exact_invertibility_proven"],
            operation_complexity="O(N log N) modular operations in F_p",
            space_complexity="O(N) modular buffer",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Exact finite field Number Theoretic Transform over prime modulus p with primitive root g."
        ))

        # ── 3. Fast Walsh-Hadamard Transform (Strictly XOR Convolution) ──
        self.register(AlgorithmComponent(
            name="fast_walsh_hadamard_builder",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_walsh_hypercube_domain_state()],
            produces_state=[StateContract("FWHTTransformedState")],
            requires_capabilities=[],
            provided_capabilities=["FAST_WALSH_HADAMARD_TRANSFORM", "XOR_CONVOLUTION"],
            preconditions=["hypercube_length_is_power_of_two", "normalization_factor_invertible_or_exact_division"],
            proof_obligations=["hadamard_matrix_kronecker_product_proven", "xor_convolution_theorem_satisfied"],
            operation_complexity="O(N log N) where N = 2^B",
            space_complexity="O(N) buffer",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Fast Walsh-Hadamard Transform strictly for bitwise XOR convolution over hypercube (Z/2Z)^B."
        ))

        # ── 4. Polynomial Multiplication Providers ──
        self.register(AlgorithmComponent(
            name="ntt_polynomial_multiply",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_polynomial_ring_state(coefficient_domain="PRIME_FIELD")],
            produces_state=[make_polynomial_ring_state(coefficient_domain="PRIME_FIELD")],
            requires_capabilities=["NUMBER_THEORETIC_TRANSFORM"],
            provided_capabilities=["POLYNOMIAL_MULTIPLICATION_CAPABILITY"],
            preconditions=["coefficient_domain_is_prime_field", "length_fits_ntt_modulus"],
            proof_obligations=["convolution_theorem_over_finite_field"],
            operation_complexity="O(N log N) modular operations",
            space_complexity="O(N) auxiliary",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Exact polynomial multiplication via Number Theoretic Transform in F_p."
        ))

        self.register(AlgorithmComponent(
            name="fft_polynomial_multiply",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_polynomial_ring_state(coefficient_domain="REAL_FIELD")],
            produces_state=[make_polynomial_ring_state(coefficient_domain="REAL_FIELD")],
            requires_capabilities=["FAST_FOURIER_TRANSFORM"],
            provided_capabilities=["POLYNOMIAL_MULTIPLICATION_CAPABILITY"],
            preconditions=["coefficient_dynamic_range_within_53bit"],
            proof_obligations=["floating_point_rounding_error_bounded"],
            operation_complexity="O(N log N) floating-point operations",
            space_complexity="O(N) auxiliary",
            correctness_guarantee="CORRECTNESS_NUMERIC_APPROXIMATE",
            description="Polynomial multiplication via Complex FFT with bounded dynamic range."
        ))

        self.register(AlgorithmComponent(
            name="naive_polynomial_multiply",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_polynomial_ring_state()],
            produces_state=[make_polynomial_ring_state()],
            requires_capabilities=[],
            provided_capabilities=["POLYNOMIAL_MULTIPLICATION_CAPABILITY"],
            preconditions=["degree_le_1000"],
            proof_obligations=["direct_cauchy_product_formula_proven"],
            operation_complexity="O(N^2) ring operations",
            space_complexity="O(N) auxiliary",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Direct O(N^2) Cauchy product polynomial multiplication for small degrees."
        ))

        # ── 5. Formal Power Series Inverse (Newton's Method) ──
        self.register(AlgorithmComponent(
            name="polynomial_inverse_builder",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_polynomial_ring_state()],
            produces_state=[make_polynomial_ring_state()],
            requires_capabilities=["POLYNOMIAL_MULTIPLICATION_CAPABILITY"],
            provided_capabilities=["POLYNOMIAL_INVERSE_CAPABILITY"],
            preconditions=["constant_term_is_unit"],
            proof_obligations=["newton_iteration_quadratic_convergence_proven", "multiplication_provider_guarantee_propagated"],
            operation_complexity="O(M(N)) where M(N) is the resolved multiplication provider complexity",
            space_complexity="O(N) auxiliary",
            correctness_guarantee="PROPAGATED_FROM_PROVIDER",
            description="Formal power series inverse A(x)^(-1) mod x^N via Newton's method B_{2k} = B_k(2 - A B_k)."
        ))

        # ── 6. Gaussian Elimination over R (Floating-Point Policy) ──
        self.register(AlgorithmComponent(
            name="gaussian_elimination_real_builder",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_real_matrix_state()],
            produces_state=[StateContract("RealRowEchelonState")],
            requires_capabilities=[],
            provided_capabilities=["GAUSSIAN_ELIMINATION_REAL", "LINEAR_SYSTEM_SOLVER_REAL", "MATRIX_INVERSE_REAL"],
            preconditions=["floating_point_policy_configured"],
            proof_obligations=["partial_pivoting_maximizes_pivot_stability", "singularity_decided_by_pivot_policy"],
            operation_complexity="O(N^3) floating-point operations",
            space_complexity="O(N^2) matrix buffer",
            correctness_guarantee="CORRECTNESS_NUMERIC_APPROXIMATE",
            description="Gaussian elimination over R with partial pivoting, explicit tolerance policy, rank, and consistency."
        ))

        # ── 7. Gaussian Elimination over F_p (Exact Modular Field) ──
        self.register(AlgorithmComponent(
            name="gaussian_elimination_modular_builder",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_modular_matrix_state()],
            produces_state=[StateContract("ModularRowEchelonState")],
            requires_capabilities=[],
            provided_capabilities=["GAUSSIAN_ELIMINATION_MODULAR", "LINEAR_SYSTEM_SOLVER_MODULAR", "MATRIX_INVERSE_MODULAR"],
            preconditions=["modulus_prime_certified", "ground_field_has_no_zero_divisors"],
            proof_obligations=["modular_inverse_pivot_elimination_proven", "exact_field_rank_soundness"],
            operation_complexity="O(N^3) field operations in F_p",
            space_complexity="O(N^2) matrix buffer",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Exact Gaussian elimination over prime field F_p with modular inverse pivots, determinant, and rank."
        ))

        # ── 8. Gaussian Elimination over F_2 (Bitset Word Elimination) ──
        self.register(AlgorithmComponent(
            name="gaussian_elimination_xor_builder",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_bitset_matrix_state()],
            produces_state=[StateContract("BitsetRowEchelonState")],
            requires_capabilities=[],
            provided_capabilities=["GAUSSIAN_ELIMINATION_XOR", "LINEAR_SYSTEM_SOLVER_XOR"],
            preconditions=["ground_field_is_binary_f2"],
            proof_obligations=["bitset_word_parallel_elimination_soundness", "f2_linear_system_consistency_proven"],
            operation_complexity="O(N^2 * M / 64) 64-bit word operations",
            space_complexity="O(N * M / 64) bitset memory",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="High-throughput Gaussian elimination over F_2 using packed 64-bit word bitsets."
        ))

        # ── 9. Linear Basis (Online XOR Subspace Basis in F_2^B) ──
        self.register(AlgorithmComponent(
            name="linear_basis_xor_builder",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_linear_basis_state()],
            produces_state=[StateContract("EchelonizedLinearBasisState")],
            requires_capabilities=[],
            provided_capabilities=["LINEAR_BASIS_XOR_MAINTENANCE", "MAXIMUM_XOR_SUBSET_QUERY"],
            preconditions=["element_in_bitwidth_domain_0_to_2_B_minus_1"],
            proof_obligations=["echelon_canonical_basis_invariant_proven", "greedy_xor_maximization_optimality_proven"],
            operation_complexity="O(B) per insertion or query",
            space_complexity="O(B) integer memory",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Online linear basis in F_2^B supporting incremental vector insertion, span check, and greedy max XOR."
        ))

        # ── 10. Berlekamp-Massey Recurrence Solver ──
        self.register(AlgorithmComponent(
            name="berlekamp_massey_recurrence_builder",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_linear_recurrence_state()],
            produces_state=[StateContract("MinimalRecurrencePolynomialState")],
            requires_capabilities=[],
            provided_capabilities=["MINIMAL_LINEAR_RECURRENCE_POLYNOMIAL"],
            preconditions=["coefficient_domain_is_certified_field", "sequence_length_sufficient"],
            proof_obligations=["berlekamp_massey_minimal_degree_theorem_proven", "discrepancy_division_valid_in_field"],
            operation_complexity="O(K^2) field operations",
            space_complexity="O(K) polynomial memory",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Berlekamp-Massey algorithm finding the minimal linear recurrence polynomial C(x) in O(K^2) over field."
        ))

        # ── 11. Linear Recurrence Evaluator (Separate Composition Node) ──
        self.register(AlgorithmComponent(
            name="linear_recurrence_evaluator",
            node_type=CompositionNodeType.TRANSFORMATION,
            consumes_state=[StateContract("MinimalRecurrencePolynomialState")],
            produces_state=[StateContract("RecurrenceNthTermResultState")],
            requires_capabilities=["MINIMAL_LINEAR_RECURRENCE_POLYNOMIAL", "POLYNOMIAL_MULTIPLICATION_CAPABILITY"],
            provided_capabilities=["LINEAR_RECURRENCE_NTH_TERM_EVALUATION"],
            preconditions=["minimal_recurrence_polynomial_available"],
            proof_obligations=["characteristic_polynomial_modulus_exponentiation_soundness"],
            operation_complexity="O(K^2 log N) or O(K log K log N) with fast multiplier",
            space_complexity="O(K) buffer",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Evaluates the N-th term of a linear recurrence using polynomial modulus reduction x^N mod P(x)."
        ))

        # ── 12. Lagrange Point Evaluation (General Points) ──
        self.register(AlgorithmComponent(
            name="lagrange_point_evaluation_general",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_interpolation_points_state()],
            produces_state=[StateContract("LagrangePointEvaluationState")],
            requires_capabilities=[],
            provided_capabilities=["LAGRANGE_POINT_EVALUATION"],
            preconditions=["interpolation_nodes_distinct"],
            proof_obligations=["lagrange_basis_polynomial_orthogonality_proven"],
            operation_complexity="O(d^2) field operations",
            space_complexity="O(d) auxiliary",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Evaluates degree-d polynomial at query point X from d+1 arbitrary distinct points in O(d^2)."
        ))

        # ── 13. Lagrange Point Evaluation (Contiguous Integer Nodes O(d)) ──
        self.register(AlgorithmComponent(
            name="lagrange_point_evaluation_contiguous",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_interpolation_points_state(is_contiguous=True)],
            produces_state=[StateContract("LagrangePointEvaluationState")],
            requires_capabilities=[],
            provided_capabilities=["LAGRANGE_POINT_EVALUATION_O_D"],
            preconditions=["interpolation_nodes_distinct", "is_contiguous_nodes", "contiguous_domain_valid_d_lt_p"],
            proof_obligations=["prefix_suffix_product_telescoping_proven", "factorial_signs_alternation_soundness"],
            operation_complexity="O(d) linear point evaluation",
            space_complexity="O(d) prefix/suffix memory",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Evaluates degree-d polynomial at query point X from consecutive integer nodes x_i = i in strictly O(d)."
        ))

        # ── 14. Lagrange Polynomial Construction (All Coefficients O(d^2)) ──
        self.register(AlgorithmComponent(
            name="lagrange_polynomial_construction",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_interpolation_points_state()],
            produces_state=[make_polynomial_ring_state()],
            requires_capabilities=[],
            provided_capabilities=["LAGRANGE_POLYNOMIAL_COEFFICIENT_RECONSTRUCTION"],
            preconditions=["interpolation_nodes_distinct"],
            proof_obligations=["full_coefficient_vector_uniqueness_proven"],
            operation_complexity="O(d^2) polynomial reconstruction",
            space_complexity="O(d) coefficient buffer",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Reconstructs all d+1 coefficients of interpolating polynomial in O(d^2) time."
        ))
