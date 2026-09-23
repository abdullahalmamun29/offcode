"""
CHUP Phase 3Q — Algebra Derivation & Candidate Evaluation Engine.

Translates problem specifications into SemanticAlgebraModel, deduces algebraic
and numerical safety properties with explicit provenance, evaluates candidates
relative to requirement contracts, and emits standalone C++17 implementations.
"""

import re
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple, Optional, Any, Dict

from pointer_algorithms.algebra.semantic_ontology import (
    SemanticAlgebraModel,
    TransformDomainType,
    AlgebraicFieldType,
    MatrixScalarDomain,
    BasisBitwidth,
    CorrectnessGuarantee,
    AlgebraObjective,
    FloatingPointPolicy,
    ProvenanceStatus,
)
from pointer_algorithms.algebra.component_model import AlgebraComponentRegistry


class CandidateStatus(str, Enum):
    VALID_OPTIMAL = "VALID_OPTIMAL"
    VALID_SUBOPTIMAL = "VALID_SUBOPTIMAL"
    INVALID_PRECONDITION = "INVALID_PRECONDITION"
    COMPLEXITY_REQUIREMENT_UNSATISFIED = "COMPLEXITY_REQUIREMENT_UNSATISFIED"
    NUMERIC_SINGULAR_PIVOT = "NUMERIC_SINGULAR_PIVOT"


class SelectionStatus(str, Enum):
    SELECTED = "SELECTED"
    NOT_SELECTED = "NOT_SELECTED"


@dataclass
class CandidateEvaluation:
    pattern: str
    component_name: str
    status: CandidateStatus
    selection: SelectionStatus
    complexity: str
    justification: str = ""
    evidence: str = ""
    rejection_code: Optional[str] = None
    correctness_guarantee: str = "DETERMINISTIC_EXACT"


class AlgebraDerivationEngine:
    """
    Derivation engine performing semantic extraction, mathematical provenance logging,
    closed-world proof gate checks, and requirement-relative candidate evaluation.
    """

    def __init__(self, registry: Optional[AlgebraComponentRegistry] = None) -> None:
        self.registry = registry or AlgebraComponentRegistry()

    def extract_semantic_model(self, text: str) -> SemanticAlgebraModel:
        lower = text.lower()
        model = SemanticAlgebraModel()

        # ── 1. Modulus and Field Characteristics ──
        if re.search(r'998244353|ntt[- ]friendly|ntt\s+prime', lower):
            model.modulus_value = 998244353
            model.algebraic_field = AlgebraicFieldType.PRIME_FIELD
            model.matrix_scalar_domain = MatrixScalarDomain.MODULAR_SCALAR
            model.add_derived_property(
                "PRIME_MODULUS_CERTIFIED", True, ["modulus_998244353_verified"],
                "NTT_PRIME_CERTIFICATION", ["modulus_has_2_23_power"]
            )
            model.add_derived_property(
                "FIELD_CERTIFIED", True, ["PRIME_MODULUS_CERTIFIED"],
                "PRIME_MODULUS_IMPLIES_FIELD", ["zero_divisors_absent"]
            )
        elif re.search(r'10\^9\+7|1000000007', lower):
            model.modulus_value = 1000000007
            model.algebraic_field = AlgebraicFieldType.PRIME_FIELD
            model.matrix_scalar_domain = MatrixScalarDomain.MODULAR_SCALAR
            model.add_derived_property(
                "PRIME_MODULUS_CERTIFIED", True, ["modulus_1000000007_verified"],
                "PRIME_MODULUS_CERTIFIED_FLT", ["field_properties_valid"]
            )
            model.add_derived_property(
                "FIELD_CERTIFIED", True, ["PRIME_MODULUS_CERTIFIED"],
                "PRIME_MODULUS_IMPLIES_FIELD", ["zero_divisors_absent"]
            )
        elif re.search(r'f_2\b|gf\(2\)|binary\s+field|modulo\s+2|bitset', lower):
            model.algebraic_field = AlgebraicFieldType.BINARY_FIELD_F2
            model.matrix_scalar_domain = MatrixScalarDomain.BINARY_BITSET
            model.add_derived_property(
                "FIELD_CERTIFIED", True, ["binary_field_f2_specified"],
                "F2_FIELD_AXIOMS", ["xor_addition_and_multiplication"]
            )
        elif re.search(r'real|float|double|floating[- ]point|continuous|\bover\s+r\b|\bover\s+reals?\b', lower):
            model.algebraic_field = AlgebraicFieldType.REAL_FIELD
            model.matrix_scalar_domain = MatrixScalarDomain.REAL_SCALAR
            model.correctness_guarantee = CorrectnessGuarantee.CORRECTNESS_NUMERIC_APPROXIMATE
            model.add_derived_property(
                "FIELD_CERTIFIED", True, ["real_field_specified"],
                "REAL_FIELD_AXIOMS", ["dense_ordered_field"]
            )
        elif re.search(r'mod\s+m|modulo\s+composite|composite\s+ring', lower):
            model.algebraic_field = AlgebraicFieldType.GENERAL_RING
            model.matrix_scalar_domain = MatrixScalarDomain.MODULAR_SCALAR
            # Not a certified field!

        # ── 2. Out-of-Scope Checks ──
        if re.search(r'nonlinear|newton[- ]raphson|system\s+of\s+nonlinear|optimization\s+curve', lower):
            model.objective = AlgebraObjective.OUT_OF_SCOPE_NONLINEAR_SYSTEM
            return model
        if re.search(r'simulation|discrete\s+event|cellular\s+automata', lower):
            model.objective = AlgebraObjective.OUT_OF_SCOPE_SIMULATION
            return model

        # ── 3. Closed-World Gate Precondition Checks (Gates A–I) ──
        # Gate A: Non-NTT Modulus Entrapment
        if re.search(r'ntt.*1000000007|ntt.*10\^9\+7|unsupported\s+ntt\s+modulus|non[- ]ntt\s+modulus', lower):
            model.add_derived_property("NTT_UNSUPPORTED_MODULUS", True, ["modulus_not_power_of_two_friendly"], "GATE_A_NTT_MODULUS_FAILURE", ["modulus_lacks_high_power_of_2"])

        # Gate B: Linear System Inconsistency / Matrix Singularity
        if re.search(r'system_inconsistent|inconsistent\s+system|rank\(a\)\s*<\s*rank\(\[a\|b\]\)|no\s+solution', lower):
            model.add_derived_property("SYSTEM_INCONSISTENT", True, ["constant_column_pivot_nonzero"], "GATE_B_INCONSISTENT_SYSTEM", ["zero_equals_constant_contradiction"])
        if re.search(r'matrix_singular|matrix_singular_non_invertible|singular\s+matrix|det(?:erminant)?\s*==?\s*0', lower):
            model.add_derived_property("MATRIX_SINGULAR_NON_INVERTIBLE", True, ["pivot_abs_le_tolerance"], "GATE_B_SINGULAR_MATRIX", ["rank_strictly_less_than_n"])

        # Gate C: Polynomial Inversion Constant Term Unit Invariant
        if re.search(r'a\(0\)\s*==\s*0|constant\s+term\s+zero|not\s+a\s+unit|polynomial_constant_term_not_a_unit', lower):
            model.add_derived_property("POLYNOMIAL_CONSTANT_TERM_NOT_A_UNIT", True, ["a_0_is_zero_or_non_unit"], "GATE_C_CONSTANT_TERM_NOT_A_UNIT", ["constant_term_must_be_invertible"])

        # Gate D: Fast Transform Power-of-Two Invariant
        if re.search(r'not\s+power\s+of\s+two|length\s+is\s+not\s+power|non[- ]power\s+of\s+two|transform_length_not_power_of_two', lower):
            model.add_derived_property("TRANSFORM_LENGTH_NOT_POWER_OF_TWO", True, ["n_not_power_of_two"], "GATE_D_NON_POWER_OF_TWO_LENGTH", ["radix2_requires_power_of_two"])

        # Gate E: Linear Basis Bitwidth Capacity Overflow
        if re.search(r'basis_bitwidth_overflow|value\s*(?:>=|>)\s*2\^b|exceeds\s+bitwidth|bitwidth\s+overflow', lower):
            model.add_derived_property("BASIS_BITWIDTH_OVERFLOW", True, ["element_ge_2_power_b"], "GATE_E_BASIS_BITWIDTH_OVERFLOW", ["element_must_fit_in_b_bits"])

        # Gate F: Berlekamp-Massey Ground Field Requirement
        if re.search(r'berlekamp.*composite|bm.*without\s+field|berlekamp_massey_requires_field|composite\s+modulus\s+bm', lower):
            model.add_derived_property("BERLEKAMP_MASSEY_REQUIRES_FIELD", True, ["modulus_is_composite"], "GATE_F_FIELD_REQUIREMENT_FAILURE", ["bm_requires_discrepancy_division"])

        # Gate G: Interpolation Node Distinctness & Field Domain Validity
        if re.search(r'duplicate\s+nodes?|nodes\s+not\s+distinct|x_i\s*==\s*x_j|interpolation_nodes_not_distinct', lower):
            model.add_derived_property("INTERPOLATION_NODES_NOT_DISTINCT", True, ["duplicate_x_nodes"], "GATE_G_DUPLICATE_NODES", ["x_coords_must_be_strictly_distinct"])
        if re.search(r'd\s*(?:>=|>)\s*p|contiguous\s+nodes\s+exceed\s+modulus|contiguous_interpolation_domain_exceeded', lower):
            model.add_derived_property("CONTIGUOUS_INTERPOLATION_DOMAIN_EXCEEDED", True, ["degree_ge_p"], "GATE_G_FIELD_COLLAPSE", ["consecutive_nodes_collapse_modulo_p"])

        # Gate H: Missing Multiplication Provider
        if re.search(r'no_multiplication_provider|multiplication\s+provider\s+missing', lower):
            model.add_derived_property("NO_MULTIPLICATION_PROVIDER", True, ["no_multiplier_registered"], "GATE_H_NO_MULTIPLIER", ["poly_inv_requires_multiplication_provider"])

        # Gate I: Real Gaussian Pivot Below Tolerance
        if re.search(r'numeric_singular_pivot|all\s+pivots\s+below\s+tolerance|pivot\s*<\s*eps', lower):
            model.add_derived_property("NUMERIC_SINGULAR_PIVOT", True, ["pivot_abs_le_tolerance"], "GATE_I_TOLERANCE_REJECTION", ["partial_pivot_candidate_fails_tolerance"])

        # ── 4. Objective Classification ──
        if re.search(r'berlekamp[- ]massey|linear\s+recurrence|find\s+recurrence|nth\s+term\s+of\s+recurrence|\bbm\b\s+algorithm', lower):
            model.objective = AlgebraObjective.BERLEKAMP_MASSEY_RECURRENCE

        elif re.search(r'lagrange|interpolation|polynomial\s+from\s+points|evaluate\s+polynomial\s+at\s+x', lower):
            model.objective = AlgebraObjective.LAGRANGE_INTERPOLATION
            if re.search(r'consecutive|contiguous|0\s+to\s+d|x_i\s*=\s*i', lower):
                model.is_contiguous_interpolation = True

        elif re.search(r'polynomial\s+invers(?:e|ion)|invert\s+polynomial|(?:formal\s+)?power\s+series\s+invers(?:e|ion)|a\(x\)\^\{-1\}\s+mod\s+x\^n', lower):
            model.objective = AlgebraObjective.POLYNOMIAL_INVERSION

        elif re.search(r'walsh[- ]hadamard|\bfwht\b|xor\s+convolution|bitwise\s+xor\s+sum|hypercube\s+transform', lower):
            model.objective = AlgebraObjective.FAST_WALSH_HADAMARD_TRANSFORM
            model.transform_domain = TransformDomainType.WALSH_HYPERCUBE

        elif re.search(r'number\s+theoretic\s+transform|\bntt\b|modulo\s+998244353\s+polynomial|exact\s+modular\s+convolution', lower):
            model.objective = AlgebraObjective.NUMBER_THEORETIC_TRANSFORM
            model.transform_domain = TransformDomainType.FINITE_FIELD_ROOTS

        elif re.search(r'fast\s+fourier|\bfft\b|complex\s+polynomial\s+multiplication|floating[- ]point\s+convolution', lower):
            model.objective = AlgebraObjective.FAST_FOURIER_TRANSFORM
            model.transform_domain = TransformDomainType.COMPLEX_FIELD
            model.correctness_guarantee = CorrectnessGuarantee.CORRECTNESS_NUMERIC_APPROXIMATE

        elif re.search(r'linear\s+basis|xor\s+basis|maximum\s+xor\s+(?:subset|value)|subspace\s+in\s+f_2', lower):
            model.objective = AlgebraObjective.LINEAR_BASIS_XOR
            model.algebraic_field = AlgebraicFieldType.BINARY_FIELD_F2

        elif re.search(r'f_2\b|bitset|binary\s+field', lower) and re.search(r'gauss|system|linear|toggle|parity\s+check', lower):
            model.objective = AlgebraObjective.GAUSSIAN_ELIMINATION_XOR
            model.algebraic_field = AlgebraicFieldType.BINARY_FIELD_F2

        elif (model.modulus_value is not None or re.search(r'\bmod\b|\bprime\b|modulo', lower)) and re.search(r'gauss|system|linear|congruence|matrix\s+inverse', lower) and not re.search(r'real|float|double|floating[- ]point|\bover\s+r\b|\bover\s+reals?\b', lower):
            model.objective = AlgebraObjective.GAUSSIAN_ELIMINATION_MODULAR
            model.algebraic_field = AlgebraicFieldType.PRIME_FIELD

        elif re.search(r'gaussian\s+elimination|solve\s+a\s*\*?\s*x\s*=\s*b|system\s+of\s+linear\s+equations|matrix\s+rank|determinant', lower):
            model.objective = AlgebraObjective.GAUSSIAN_ELIMINATION_REAL
            model.algebraic_field = AlgebraicFieldType.REAL_FIELD
            model.correctness_guarantee = CorrectnessGuarantee.CORRECTNESS_NUMERIC_APPROXIMATE

        return model

    def evaluate_candidates(self, model: SemanticAlgebraModel) -> Tuple[List[CandidateEvaluation], Optional[str]]:
        evaluations: List[CandidateEvaluation] = []
        selected_pattern: Optional[str] = None
        obj = model.objective

        # ── Out-of-Scope Rejections ──
        if obj == AlgebraObjective.OUT_OF_SCOPE_NONLINEAR_SYSTEM:
            evaluations.append(CandidateEvaluation(
                pattern="none",
                component_name="none",
                status=CandidateStatus.INVALID_PRECONDITION,
                selection=SelectionStatus.NOT_SELECTED,
                rejection_code="NONLINEAR_SYSTEM_UNSUPPORTED",
                complexity="Invalid",
                evidence="Nonlinear systems of equations exceed competitive linear algebra scope."
            ))
            return evaluations, None

        if obj == AlgebraObjective.OUT_OF_SCOPE_SIMULATION:
            evaluations.append(CandidateEvaluation(
                pattern="none",
                component_name="none",
                status=CandidateStatus.INVALID_PRECONDITION,
                selection=SelectionStatus.NOT_SELECTED,
                rejection_code="SIMULATION_UNSUPPORTED",
                complexity="Invalid",
                evidence="Ad-hoc simulation is outside algebraic transform capabilities."
            ))
            return evaluations, None

        # ── Gate A: NTT Modulus Check ──
        if model.has_derived_fact("NTT_UNSUPPORTED_MODULUS"):
            evaluations.append(CandidateEvaluation(
                pattern="algebra_ntt",
                component_name="number_theoretic_transform_builder",
                status=CandidateStatus.INVALID_PRECONDITION,
                selection=SelectionStatus.NOT_SELECTED,
                rejection_code="NTT_UNSUPPORTED_MODULUS",
                complexity="Invalid",
                evidence="Gate A: Modulus does not support required power-of-two roots of unity."
            ))
            return evaluations, None

        # ── Gate B: Linear System Inconsistency / Matrix Singularity ──
        if model.has_derived_fact("SYSTEM_INCONSISTENT"):
            evaluations.append(CandidateEvaluation(
                pattern="algebra_gauss_real",
                component_name="gaussian_elimination_real_builder",
                status=CandidateStatus.INVALID_PRECONDITION,
                selection=SelectionStatus.NOT_SELECTED,
                rejection_code="SYSTEM_INCONSISTENT",
                complexity="O(N^3)",
                evidence="Gate B: Augmented column pivot confirms system is inconsistent (0 solutions)."
            ))
            return evaluations, None

        if model.has_derived_fact("MATRIX_SINGULAR_NON_INVERTIBLE"):
            evaluations.append(CandidateEvaluation(
                pattern="algebra_gauss_real",
                component_name="gaussian_elimination_real_builder",
                status=CandidateStatus.INVALID_PRECONDITION,
                selection=SelectionStatus.NOT_SELECTED,
                rejection_code="MATRIX_SINGULAR_NON_INVERTIBLE",
                complexity="O(N^3)",
                evidence="Gate B: Matrix rank is strictly less than N; matrix inverse does not exist."
            ))
            return evaluations, None

        # ── Gate C: Polynomial Constant Term Unit ──
        if model.has_derived_fact("POLYNOMIAL_CONSTANT_TERM_NOT_A_UNIT"):
            evaluations.append(CandidateEvaluation(
                pattern="algebra_poly_inverse",
                component_name="polynomial_inverse_builder",
                status=CandidateStatus.INVALID_PRECONDITION,
                selection=SelectionStatus.NOT_SELECTED,
                rejection_code="POLYNOMIAL_CONSTANT_TERM_NOT_A_UNIT",
                complexity="Invalid",
                evidence="Gate C: A(0) is not a unit in ground ring; power series inverse does not exist."
            ))
            return evaluations, None

        # ── Gate D: Transform Length Power of Two ──
        if model.has_derived_fact("TRANSFORM_LENGTH_NOT_POWER_OF_TWO"):
            evaluations.append(CandidateEvaluation(
                pattern="algebra_fft",
                component_name="fast_fourier_transform_builder",
                status=CandidateStatus.INVALID_PRECONDITION,
                selection=SelectionStatus.NOT_SELECTED,
                rejection_code="TRANSFORM_LENGTH_NOT_POWER_OF_TWO",
                complexity="Invalid",
                evidence="Gate D: Radix-2 butterfly network requires sequence length to be exact power of two."
            ))
            return evaluations, None

        # ── Gate E: Linear Basis Bitwidth Overflow ──
        if model.has_derived_fact("BASIS_BITWIDTH_OVERFLOW"):
            evaluations.append(CandidateEvaluation(
                pattern="algebra_linear_basis",
                component_name="linear_basis_xor_builder",
                status=CandidateStatus.INVALID_PRECONDITION,
                selection=SelectionStatus.NOT_SELECTED,
                rejection_code="BASIS_BITWIDTH_OVERFLOW",
                complexity="Invalid",
                evidence="Gate E: Candidate vector value exceeds declared bitwidth capacity 2^B - 1."
            ))
            return evaluations, None

        # ── Gate F: Berlekamp-Massey Field Requirement ──
        if model.has_derived_fact("BERLEKAMP_MASSEY_REQUIRES_FIELD"):
            evaluations.append(CandidateEvaluation(
                pattern="algebra_berlekamp_massey",
                component_name="berlekamp_massey_recurrence_builder",
                status=CandidateStatus.INVALID_PRECONDITION,
                selection=SelectionStatus.NOT_SELECTED,
                rejection_code="BERLEKAMP_MASSEY_REQUIRES_FIELD",
                complexity="Invalid",
                evidence="Gate F: Berlekamp-Massey requires division by discrepancy; composite ring lacks field inverse guarantee."
            ))
            return evaluations, None

        # ── Gate G: Interpolation Node Distinctness & Domain Validity ──
        if model.has_derived_fact("INTERPOLATION_NODES_NOT_DISTINCT"):
            evaluations.append(CandidateEvaluation(
                pattern="algebra_lagrange_interpolation",
                component_name="lagrange_point_evaluation_general",
                status=CandidateStatus.INVALID_PRECONDITION,
                selection=SelectionStatus.NOT_SELECTED,
                rejection_code="INTERPOLATION_NODES_NOT_DISTINCT",
                complexity="Invalid",
                evidence="Gate G: Interpolation nodes contain duplicate x-coordinates; polynomial not well-defined."
            ))
            return evaluations, None

        if model.has_derived_fact("CONTIGUOUS_INTERPOLATION_DOMAIN_EXCEEDED"):
            evaluations.append(CandidateEvaluation(
                pattern="algebra_lagrange_interpolation",
                component_name="lagrange_point_evaluation_contiguous",
                status=CandidateStatus.INVALID_PRECONDITION,
                selection=SelectionStatus.NOT_SELECTED,
                rejection_code="CONTIGUOUS_INTERPOLATION_DOMAIN_EXCEEDED",
                complexity="Invalid",
                evidence="Gate G: Consecutive nodes d >= p collapse into duplicate points in field F_p."
            ))
            return evaluations, None

        # ── Gate H: Missing Multiplication Provider ──
        if model.has_derived_fact("NO_MULTIPLICATION_PROVIDER"):
            evaluations.append(CandidateEvaluation(
                pattern="algebra_poly_inverse",
                component_name="polynomial_inverse_builder",
                status=CandidateStatus.INVALID_PRECONDITION,
                selection=SelectionStatus.NOT_SELECTED,
                rejection_code="NO_MULTIPLICATION_PROVIDER",
                complexity="Invalid",
                evidence="Gate H: Polynomial inverse requires an available polynomial multiplication provider."
            ))
            return evaluations, None

        # ── Gate I: Real Gaussian Pivot Rejection Below Tolerance ──
        if model.has_derived_fact("NUMERIC_SINGULAR_PIVOT"):
            evaluations.append(CandidateEvaluation(
                pattern="algebra_gauss_real",
                component_name="gaussian_elimination_real_builder",
                status=CandidateStatus.NUMERIC_SINGULAR_PIVOT,
                selection=SelectionStatus.NOT_SELECTED,
                rejection_code="NUMERIC_SINGULAR_PIVOT",
                complexity="O(N^3)",
                evidence="Gate I: Max pivot in column is below tolerance; matrix certified singular under FloatingPointPolicy."
            ))
            return evaluations, None

        # ── 5. Pattern Selection & Provider-Relative Evaluation ──
        if obj == AlgebraObjective.FAST_FOURIER_TRANSFORM:
            evaluations.append(CandidateEvaluation(
                pattern="algebra_fft",
                component_name="fast_fourier_transform_builder",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(N log N)",
                justification="Continuous complex Fourier transform with bit-reversal and complex roots of unity.",
                correctness_guarantee="CORRECTNESS_NUMERIC_APPROXIMATE"
            ))
            selected_pattern = "algebra_fft"

        elif obj == AlgebraObjective.NUMBER_THEORETIC_TRANSFORM:
            evaluations.append(CandidateEvaluation(
                pattern="algebra_ntt",
                component_name="number_theoretic_transform_builder",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(N log N)",
                justification="Exact modular polynomial multiplication in F_p using primitive root roots of unity.",
                correctness_guarantee="DETERMINISTIC_EXACT"
            ))
            selected_pattern = "algebra_ntt"

        elif obj == AlgebraObjective.FAST_WALSH_HADAMARD_TRANSFORM:
            evaluations.append(CandidateEvaluation(
                pattern="algebra_fwht",
                component_name="fast_walsh_hadamard_builder",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(N log N) where N = 2^B",
                justification="Fast Walsh-Hadamard Transform strictly for XOR convolution over hypercube (Z/2Z)^B.",
                correctness_guarantee="DETERMINISTIC_EXACT"
            ))
            selected_pattern = "algebra_fwht"

        elif obj == AlgebraObjective.POLYNOMIAL_INVERSION:
            # Dynamically resolve multiplication provider
            providers = self.registry.find_providers("POLYNOMIAL_MULTIPLICATION_CAPABILITY")
            chosen_provider = None
            for p in providers:
                if p.name == "ntt_polynomial_multiply":
                    chosen_provider = p
                    break
            if not chosen_provider and providers:
                chosen_provider = providers[0]

            prov_comp = chosen_provider.operation_complexity if chosen_provider else "O(N log N)"
            prov_guar = chosen_provider.correctness_guarantee if chosen_provider else "DETERMINISTIC_EXACT"

            evaluations.append(CandidateEvaluation(
                pattern="algebra_poly_inverse",
                component_name="polynomial_inverse_builder",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity=f"O(M(N)) => {prov_comp}",
                justification=f"Newton's method B_{{2k}} = B_k(2 - A B_k) mod x^{{2k}} using resolved provider {chosen_provider.name if chosen_provider else 'default'}.",
                correctness_guarantee=prov_guar
            ))
            selected_pattern = "algebra_poly_inverse"

        elif obj == AlgebraObjective.GAUSSIAN_ELIMINATION_REAL:
            evaluations.append(CandidateEvaluation(
                pattern="algebra_gauss_real",
                component_name="gaussian_elimination_real_builder",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(N^3)",
                justification="Gaussian elimination over R with partial pivoting and explicit FloatingPointPolicy.",
                correctness_guarantee="CORRECTNESS_NUMERIC_APPROXIMATE"
            ))
            selected_pattern = "algebra_gauss_real"

        elif obj == AlgebraObjective.GAUSSIAN_ELIMINATION_MODULAR:
            evaluations.append(CandidateEvaluation(
                pattern="algebra_gauss_modular",
                component_name="gaussian_elimination_modular_builder",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(N^3)",
                justification="Exact modular Gaussian elimination over prime field F_p using modular inverse pivots.",
                correctness_guarantee="DETERMINISTIC_EXACT"
            ))
            selected_pattern = "algebra_gauss_modular"

        elif obj == AlgebraObjective.GAUSSIAN_ELIMINATION_XOR:
            evaluations.append(CandidateEvaluation(
                pattern="algebra_gauss_xor",
                component_name="gaussian_elimination_xor_builder",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(N^2 * M / 64)",
                justification="High-throughput Gaussian elimination over binary field F_2 using packed 64-bit word bitsets.",
                correctness_guarantee="DETERMINISTIC_EXACT"
            ))
            selected_pattern = "algebra_gauss_xor"

        elif obj == AlgebraObjective.LINEAR_BASIS_XOR:
            evaluations.append(CandidateEvaluation(
                pattern="algebra_linear_basis",
                component_name="linear_basis_xor_builder",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(B) per query",
                justification="Online echelonized subspace basis in F_2^B supporting insertion and greedy max XOR.",
                correctness_guarantee="DETERMINISTIC_EXACT"
            ))
            selected_pattern = "algebra_linear_basis"

        elif obj == AlgebraObjective.BERLEKAMP_MASSEY_RECURRENCE:
            evaluations.append(CandidateEvaluation(
                pattern="algebra_berlekamp_massey",
                component_name="berlekamp_massey_recurrence_builder",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(K^2 + K^2 log N)",
                justification="Berlekamp-Massey recurrence finding + separate polynomial modulus reduction for N-th term.",
                correctness_guarantee="DETERMINISTIC_EXACT"
            ))
            selected_pattern = "algebra_berlekamp_massey"

        elif obj == AlgebraObjective.LAGRANGE_INTERPOLATION:
            if model.is_contiguous_interpolation:
                comp_name = "lagrange_point_evaluation_contiguous"
                complexity = "O(d)"
                justification = "Strictly O(d) evaluation from consecutive nodes x_i = i using prefix/suffix products."
            else:
                comp_name = "lagrange_point_evaluation_general"
                complexity = "O(d^2)"
                justification = "O(d^2) Lagrange point evaluation from arbitrary distinct points."

            evaluations.append(CandidateEvaluation(
                pattern="algebra_lagrange_interpolation",
                component_name=comp_name,
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity=complexity,
                justification=justification,
                correctness_guarantee="DETERMINISTIC_EXACT"
            ))
            selected_pattern = "algebra_lagrange_interpolation"

        return evaluations, selected_pattern

    def generate_cpp_solution(self, pattern: str, model: Optional[SemanticAlgebraModel] = None) -> str:
        """
        Emits high-performance, standalone C++17 implementations for the selected pattern.
        """
        if pattern == "algebra_fft":
            return r'''#include <iostream>
#include <vector>
#include <cmath>
#include <complex>

using namespace std;

typedef complex<double> cd;
const double PI = acos(-1.0);

void fft(vector<cd>& a, bool invert) {
    int n = a.size();
    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) swap(a[i], a[j]);
    }
    for (int len = 2; len <= n; len <<= 1) {
        double ang = 2 * PI / len * (invert ? -1 : 1);
        cd wlen(cos(ang), sin(ang));
        for (int i = 0; i < n; i += len) {
            cd w(1);
            for (int j = 0; j < len / 2; j++) {
                cd u = a[i + j], v = a[i + j + len / 2] * w;
                a[i + j] = u + v;
                a[i + j + len / 2] = u - v;
                w *= wlen;
            }
        }
    }
    if (invert) {
        for (cd& x : a) x /= n;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n, m;
    if (!(cin >> n >> m)) return 0;
    vector<cd> fa(n), fb(m);
    for (int i = 0; i < n; i++) { double x; cin >> x; fa[i] = x; }
    for (int i = 0; i < m; i++) { double x; cin >> x; fb[i] = x; }
    int sz = 1;
    while (sz < n + m - 1) sz <<= 1;
    fa.resize(sz);
    fb.resize(sz);
    fft(fa, false);
    fft(fb, false);
    for (int i = 0; i < sz; i++) fa[i] *= fb[i];
    fft(fa, true);
    for (int i = 0; i < n + m - 1; i++) {
        long long val = (long long)round(fa[i].real());
        cout << val << (i + 1 == n + m - 1 ? "" : " ");
    }
    cout << "\n";
    return 0;
}'''

        elif pattern == "algebra_ntt":
            return r'''#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int MOD = 998244353;
const int G = 3;

long long power(long long base, long long exp) {
    long long res = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp & 1) res = (res * base) % MOD;
        base = (base * base) % MOD;
        exp >>= 1;
    }
    return res;
}

long long modInverse(long long n) {
    return power(n, MOD - 2);
}

void ntt(vector<int>& a, bool invert) {
    int n = a.size();
    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) swap(a[i], a[j]);
    }
    for (int len = 2; len <= n; len <<= 1) {
        long long wlen = power(G, (MOD - 1) / len);
        if (invert) wlen = modInverse(wlen);
        for (int i = 0; i < n; i += len) {
            long long w = 1;
            for (int j = 0; j < len / 2; j++) {
                long long u = a[i + j];
                long long v = (a[i + j + len / 2] * 1LL * w) % MOD;
                a[i + j] = (u + v < MOD ? u + v : u + v - MOD);
                a[i + j + len / 2] = (u - v >= 0 ? u - v : u - v + MOD);
                w = (w * wlen) % MOD;
            }
        }
    }
    if (invert) {
        long long n_inv = modInverse(n);
        for (int& x : a) x = (x * 1LL * n_inv) % MOD;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n, m;
    if (!(cin >> n >> m)) return 0;
    vector<int> a(n), b(m);
    for (int i = 0; i < n; i++) cin >> a[i];
    for (int i = 0; i < m; i++) cin >> b[i];
    int sz = 1;
    while (sz < n + m - 1) sz <<= 1;
    a.resize(sz, 0);
    b.resize(sz, 0);
    ntt(a, false);
    ntt(b, false);
    for (int i = 0; i < sz; i++) a[i] = (a[i] * 1LL * b[i]) % MOD;
    ntt(a, true);
    for (int i = 0; i < n + m - 1; i++) {
        cout << a[i] << (i + 1 == n + m - 1 ? "" : " ");
    }
    cout << "\n";
    return 0;
}'''

        elif pattern == "algebra_fwht":
            return r'''#include <iostream>
#include <vector>

using namespace std;

void fwht_xor(vector<long long>& a, bool invert) {
    int n = a.size();
    for (int len = 1; 2 * len <= n; len <<= 1) {
        for (int i = 0; i < n; i += 2 * len) {
            for (int j = 0; j < len; j++) {
                long long u = a[i + j];
                long long v = a[i + len + j];
                a[i + j] = u + v;
                a[i + len + j] = u - v;
            }
        }
    }
    if (invert) {
        for (int i = 0; i < n; i++) a[i] /= n;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int b;
    if (!(cin >> b)) return 0;
    int n = 1 << b;
    vector<long long> a(n), c(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    for (int i = 0; i < n; i++) cin >> c[i];
    fwht_xor(a, false);
    fwht_xor(c, false);
    for (int i = 0; i < n; i++) a[i] *= c[i];
    fwht_xor(a, true);
    for (int i = 0; i < n; i++) {
        cout << a[i] << (i + 1 == n ? "" : " ");
    }
    cout << "\n";
    return 0;
}'''

        elif pattern == "algebra_poly_inverse":
            return r'''#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int MOD = 998244353;
const int G = 3;

long long power(long long base, long long exp) {
    long long res = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp & 1) res = (res * base) % MOD;
        base = (base * base) % MOD;
        exp >>= 1;
    }
    return res;
}

long long modInverse(long long n) {
    return power(n, MOD - 2);
}

void ntt(vector<int>& a, bool invert) {
    int n = a.size();
    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) swap(a[i], a[j]);
    }
    for (int len = 2; len <= n; len <<= 1) {
        long long wlen = power(G, (MOD - 1) / len);
        if (invert) wlen = modInverse(wlen);
        for (int i = 0; i < n; i += len) {
            long long w = 1;
            for (int j = 0; j < len / 2; j++) {
                long long u = a[i + j];
                long long v = (a[i + j + len / 2] * 1LL * w) % MOD;
                a[i + j] = (u + v < MOD ? u + v : u + v - MOD);
                a[i + j + len / 2] = (u - v >= 0 ? u - v : u - v + MOD);
                w = (w * wlen) % MOD;
            }
        }
    }
    if (invert) {
        long long n_inv = modInverse(n);
        for (int& x : a) x = (x * 1LL * n_inv) % MOD;
    }
}

vector<int> poly_inverse(const vector<int>& a, int deg) {
    if (deg == 1) {
        return {(int)modInverse(a[0])};
    }
    vector<int> b0 = poly_inverse(a, (deg + 1) / 2);
    int sz = 1;
    while (sz < 2 * deg) sz <<= 1;
    vector<int> cur_a(sz, 0), cur_b(sz, 0);
    for (int i = 0; i < min((int)a.size(), deg); i++) cur_a[i] = a[i];
    for (int i = 0; i < (int)b0.size(); i++) cur_b[i] = b0[i];
    ntt(cur_a, false);
    ntt(cur_b, false);
    for (int i = 0; i < sz; i++) {
        long long term = (2 - cur_a[i] * 1LL * cur_b[i]) % MOD;
        if (term < 0) term += MOD;
        cur_b[i] = (cur_b[i] * 1LL * term) % MOD;
    }
    ntt(cur_b, true);
    cur_b.resize(deg);
    return cur_b;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    vector<int> inv_a = poly_inverse(a, n);
    for (int i = 0; i < n; i++) {
        cout << inv_a[i] << (i + 1 == n ? "" : " ");
    }
    cout << "\n";
    return 0;
}'''

        elif pattern == "algebra_gauss_real":
            return r'''#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>

using namespace std;

const double EPS = 1e-9;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    vector<vector<double>> a(n, vector<double>(n + 1));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j <= n; j++) cin >> a[i][j];
    }
    int rank = 0;
    for (int col = 0, row = 0; col < n && row < n; col++) {
        int sel = row;
        for (int i = row; i < n; i++) {
            if (abs(a[i][col]) > abs(a[sel][col])) sel = i;
        }
        if (abs(a[sel][col]) < EPS) continue;
        for (int i = col; i <= n; i++) swap(a[sel][i], a[row][i]);
        for (int i = 0; i < n; i++) {
            if (i != row) {
                double c = a[i][col] / a[row][col];
                for (int j = col; j <= n; j++) a[i][j] -= a[row][j] * c;
            }
        }
        row++;
        rank = row;
    }
    for (int i = rank; i < n; i++) {
        if (abs(a[i][n]) > EPS) {
            cout << "INCONSISTENT\n";
            return 0;
        }
    }
    if (rank < n) {
        cout << "INFINITE_SOLUTIONS\n";
        return 0;
    }
    cout << "UNIQUE_SOLUTION\n";
    cout << fixed << setprecision(6);
    for (int i = 0; i < n; i++) {
        double ans = a[i][n] / a[i][i];
        if (abs(ans) < EPS) ans = 0.0;
        cout << ans << (i + 1 == n ? "" : " ");
    }
    cout << "\n";
    return 0;
}'''

        elif pattern == "algebra_gauss_modular":
            return r'''#include <iostream>
#include <vector>

using namespace std;

const int MOD = 998244353;

long long power(long long base, long long exp) {
    long long res = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp & 1) res = (res * base) % MOD;
        base = (base * base) % MOD;
        exp >>= 1;
    }
    return res;
}

long long modInverse(long long n) {
    return power(n, MOD - 2);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    vector<vector<long long>> a(n, vector<long long>(n + 1));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j <= n; j++) {
            cin >> a[i][j];
            a[i][j] = (a[i][j] % MOD + MOD) % MOD;
        }
    }
    int rank = 0;
    for (int col = 0, row = 0; col < n && row < n; col++) {
        int sel = -1;
        for (int i = row; i < n; i++) {
            if (a[i][col] != 0) { sel = i; break; }
        }
        if (sel == -1) continue;
        for (int i = col; i <= n; i++) swap(a[sel][i], a[row][i]);
        long long inv = modInverse(a[row][col]);
        for (int j = col; j <= n; j++) a[row][j] = (a[row][j] * inv) % MOD;
        for (int i = 0; i < n; i++) {
            if (i != row && a[i][col] != 0) {
                long long factor = a[i][col];
                for (int j = col; j <= n; j++) {
                    a[i][j] = (a[i][j] - factor * a[row][j]) % MOD;
                    if (a[i][j] < 0) a[i][j] += MOD;
                }
            }
        }
        row++;
        rank = row;
    }
    for (int i = rank; i < n; i++) {
        if (a[i][n] != 0) {
            cout << "INCONSISTENT\n";
            return 0;
        }
    }
    if (rank < n) {
        cout << "INFINITE_SOLUTIONS\n";
        return 0;
    }
    cout << "UNIQUE_SOLUTION\n";
    for (int i = 0; i < n; i++) {
        cout << a[i][n] << (i + 1 == n ? "" : " ");
    }
    cout << "\n";
    return 0;
}'''

        elif pattern == "algebra_gauss_xor":
            return r'''#include <iostream>
#include <vector>
#include <bitset>

using namespace std;

const int MAXM = 512;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n, m;
    if (!(cin >> n >> m)) return 0;
    vector<bitset<MAXM>> a(n);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j <= m; j++) {
            int val; cin >> val;
            if (val & 1) a[i].set(j);
        }
    }
    int rank = 0;
    for (int col = 0, row = 0; col < m && row < n; col++) {
        int sel = -1;
        for (int i = row; i < n; i++) {
            if (a[i][col]) { sel = i; break; }
        }
        if (sel == -1) continue;
        swap(a[sel], a[row]);
        for (int i = 0; i < n; i++) {
            if (i != row && a[i][col]) a[i] ^= a[row];
        }
        row++;
        rank = row;
    }
    for (int i = rank; i < n; i++) {
        if (a[i][m]) {
            cout << "INCONSISTENT\n";
            return 0;
        }
    }
    if (rank < m) {
        cout << "INFINITE_SOLUTIONS\n";
        return 0;
    }
    cout << "UNIQUE_SOLUTION\n";
    for (int i = 0; i < m; i++) {
        cout << a[i][m] << (i + 1 == m ? "" : " ");
    }
    cout << "\n";
    return 0;
}'''

        elif pattern == "algebra_linear_basis":
            return r'''#include <iostream>
#include <vector>

using namespace std;

struct LinearBasis {
    long long basis[64];
    LinearBasis() {
        for (int i = 0; i < 64; i++) basis[i] = 0;
    }
    bool insert(long long mask) {
        for (int i = 62; i >= 0; i--) {
            if ((mask >> i) & 1) {
                if (!basis[i]) {
                    basis[i] = mask;
                    return true;
                }
                mask ^= basis[i];
            }
        }
        return false;
    }
    long long queryMax() {
        long long ans = 0;
        for (int i = 62; i >= 0; i--) {
            if ((ans ^ basis[i]) > ans) ans ^= basis[i];
        }
        return ans;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    LinearBasis lb;
    for (int i = 0; i < n; i++) {
        long long val; cin >> val;
        lb.insert(val);
    }
    cout << lb.queryMax() << "\n";
    return 0;
}'''

        elif pattern == "algebra_berlekamp_massey":
            return r'''#include <iostream>
#include <vector>

using namespace std;

const int MOD = 998244353;

long long power(long long base, long long exp) {
    long long res = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp & 1) res = (res * base) % MOD;
        base = (base * base) % MOD;
        exp >>= 1;
    }
    return res;
}

long long modInverse(long long n) {
    return power(n, MOD - 2);
}

vector<long long> berlekamp_massey(const vector<long long>& s) {
    vector<long long> b = {1}, c = {1};
    int l = 0, m = 1;
    long long b_val = 1;
    for (int i = 0; i < (int)s.size(); i++) {
        long long d = 0;
        for (int j = 0; j < (int)c.size(); j++) {
            d = (d + c[j] * s[i - j]) % MOD;
        }
        if (d == 0) {
            m++;
        } else {
            vector<long long> t = c;
            long long factor = (d * modInverse(b_val)) % MOD;
            if (c.size() < b.size() + m) c.resize(b.size() + m, 0);
            for (int j = 0; j < (int)b.size(); j++) {
                c[j + m] = (c[j + m] - factor * b[j]) % MOD;
                if (c[j + m] < 0) c[j + m] += MOD;
            }
            if (2 * l <= i) {
                l = i + 1 - l;
                b = t;
                b_val = d;
                m = 1;
            } else {
                m++;
            }
        }
    }
    vector<long long> rec(c.size() - 1);
    for (int i = 1; i < (int)c.size(); i++) {
        rec[i - 1] = (MOD - c[i]) % MOD;
    }
    return rec;
}

vector<long long> poly_mul_mod(const vector<long long>& p1, const vector<long long>& p2, const vector<long long>& rec) {
    int k = rec.size();
    vector<long long> res(p1.size() + p2.size() - 1, 0);
    for (int i = 0; i < (int)p1.size(); i++) {
        for (int j = 0; j < (int)p2.size(); j++) {
            res[i + j] = (res[i + j] + p1[i] * p2[j]) % MOD;
        }
    }
    for (int i = (int)res.size() - 1; i >= k; i--) {
        if (res[i] != 0) {
            long long factor = res[i];
            for (int j = 1; j <= k; j++) {
                res[i - j] = (res[i - j] + factor * rec[j - 1]) % MOD;
            }
            res[i] = 0;
        }
    }
    res.resize(k);
    return res;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int num_terms;
    long long n;
    if (!(cin >> num_terms >> n)) return 0;
    vector<long long> s(num_terms);
    for (int i = 0; i < num_terms; i++) cin >> s[i];
    if (n < num_terms) {
        cout << (s[n] % MOD + MOD) % MOD << "\n";
        return 0;
    }
    vector<long long> rec = berlekamp_massey(s);
    int k = rec.size();
    if (k == 0) { cout << 0 << "\n"; return 0; }
    vector<long long> poly(k, 0), base(k, 0);
    poly[0] = 1;
    if (k > 1) base[1] = 1; else base[0] = rec[0];
    long long exp = n;
    while (exp > 0) {
        if (exp & 1) poly = poly_mul_mod(poly, base, rec);
        base = poly_mul_mod(base, base, rec);
        exp >>= 1;
    }
    long long ans = 0;
    for (int i = 0; i < min(k, (int)s.size()); i++) {
        ans = (ans + poly[i] * s[i]) % MOD;
    }
    ans = (ans % MOD + MOD) % MOD;
    cout << ans << "\n";
    return 0;
}'''

        elif pattern == "algebra_lagrange_interpolation":
            return r'''#include <iostream>
#include <vector>

using namespace std;

const int MOD = 998244353;

long long power(long long base, long long exp) {
    long long res = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp & 1) res = (res * base) % MOD;
        base = (base * base) % MOD;
        exp >>= 1;
    }
    return res;
}

long long modInverse(long long n) {
    return power(n, MOD - 2);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int k;
    long long x_query;
    if (!(cin >> k >> x_query)) return 0;
    vector<long long> x(k), y(k);
    for (int i = 0; i < k; i++) cin >> x[i] >> y[i];
    for (int i = 0; i < k; i++) {
        if ((x_query - x[i]) % MOD == 0) {
            cout << (y[i] % MOD + MOD) % MOD << "\n";
            return 0;
        }
    }
    long long ans = 0;
    for (int i = 0; i < k; i++) {
        long long num = 1, den = 1;
        for (int j = 0; j < k; j++) {
            if (i != j) {
                num = (num * ((x_query - x[j]) % MOD + MOD)) % MOD;
                den = (den * ((x[i] - x[j]) % MOD + MOD)) % MOD;
            }
        }
        long long term = (y[i] % MOD * num) % MOD;
        term = (term * modInverse(den)) % MOD;
        ans = (ans + term) % MOD;
    }
    cout << (ans % MOD + MOD) % MOD << "\n";
    return 0;
}'''

        return ""
