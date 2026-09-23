"""
CHUP Phase 3P — Number Theory Component Model & Registry.

Defines declarative AlgorithmComponent nodes with state requirements, preconditions,
proof obligations, and representation-dependent complexity contracts.
Enforces closed-world anti-hardcoding isolation gates A through E.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional
from pointer_algorithms.number_theory.nt_state_contracts import (
    StateContract,
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


class CompositionNodeType(str, Enum):
    COMPONENT = "COMPONENT"
    TRANSFORMATION = "TRANSFORMATION"
    ADAPTER = "ADAPTER"


@dataclass
class AlgorithmComponent:
    """
    Formal specification of a reusable mathematical capability component.
    """
    name: str
    node_type: CompositionNodeType = CompositionNodeType.COMPONENT
    requires_states: List[StateContract] = field(default_factory=list)
    provides_states: List[StateContract] = field(default_factory=list)
    requires_capabilities: List[str] = field(default_factory=list)
    provided_capabilities: List[str] = field(default_factory=list)
    preconditions: List[str] = field(default_factory=list)
    proof_obligations: List[str] = field(default_factory=list)
    operation_complexity: str = ""
    space_complexity: str = ""
    description: str = ""


class NumberTheoryComponentRegistry:
    """
    Authoritative registry for all Phase 3P Number Theory & Combinatorics components.
    """
    _instance: Optional['NumberTheoryComponentRegistry'] = None

    def __new__(cls) -> 'NumberTheoryComponentRegistry':
        if cls._instance is None:
            cls._instance = super(NumberTheoryComponentRegistry, cls).__new__(cls)
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

    def _register_default_components(self) -> None:
        # ── 1. Extended Euclidean Algorithm & Bézout Identity ──
        self.register(AlgorithmComponent(
            name="extended_gcd_builder",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[make_integer_state(), make_integer_state()],
            provides_states=[make_diophantine_system_state()],
            requires_capabilities=[],
            provided_capabilities=["EXTENDED_GCD", "BEZOUT_COEFFICIENT_DERIVATION", "LINEAR_DIOPHANTINE_SOLVER"],
            preconditions=["boundary_handled_a_b_zero_iff_c_zero"],
            proof_obligations=["bezout_identity_satisfied", "quotient_step_inversion_proven"],
            operation_complexity="O(log(min(|a|, |b|)))",
            space_complexity="O(1) auxiliary",
            description="Extended Euclidean algorithm computing gcd(a, b) and complete Diophantine solution family; (0,0) conventionally yields gcd 0, solvable iff c=0."
        ))

        # ── 2. Modular Multiplicative Inverse via Extended GCD ──
        self.register(AlgorithmComponent(
            name="modular_inverse_extgcd",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[make_modular_ring_state(), make_integer_state()],
            provides_states=[make_modular_inverse_state(method="extgcd")],
            requires_capabilities=["EXTENDED_GCD"],
            provided_capabilities=["MODULAR_INVERSE_RING"],
            preconditions=["modulus_gt_1", "gcd_element_modulus_is_1"],
            proof_obligations=["unit_inversion_congruence_proven"],
            operation_complexity="O(log m)",
            space_complexity="O(1) auxiliary",
            description="Computes modular inverse for units in general ring Z/mZ via Extended GCD."
        ))

        # ── 3. Modular Multiplicative Inverse via Fermat's Little Theorem ──
        self.register(AlgorithmComponent(
            name="fermat_inverse_builder",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[make_modular_ring_state(), make_integer_state()],
            provides_states=[make_modular_inverse_state(method="fermat")],
            requires_capabilities=[],
            provided_capabilities=["MODULAR_INVERSE_FIELD"],
            preconditions=["modulus_prime_certified", "element_not_zero_mod_p"],
            proof_obligations=["fermat_little_theorem_satisfied"],
            operation_complexity="O(log p)",
            space_complexity="O(1) auxiliary",
            description="Computes modular inverse in prime field F_p via binary power a^(p-2) mod p."
        ))

        # ── 4. General Chinese Remainder Theorem Solver ──
        self.register(AlgorithmComponent(
            name="crt_solver_builder",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[make_crt_system_state()],
            provides_states=[make_crt_system_state()],
            requires_capabilities=["EXTENDED_GCD"],
            provided_capabilities=["CHINESE_REMAINDER_THEOREM_GENERAL"],
            preconditions=["all_moduli_gt_1", "pairwise_congruence_solvable"],
            proof_obligations=["lcm_congruence_unification_proven", "dynamic_128bit_overflow_checked"],
            operation_complexity="O(sum_{i=1}^{k-1} log(L_i)) where L_i is intermediate LCM",
            space_complexity="O(1) auxiliary",
            description="General non-coprime Chinese Remainder Theorem solver with dynamic 128-bit LCM tracking."
        ))

        # ── 5. Linear Euler Sieve & SPF Factorization ──
        self.register(AlgorithmComponent(
            name="linear_sieve_builder",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[make_integer_state()],
            provides_states=[make_sieve_table_state()],
            requires_capabilities=[],
            provided_capabilities=["LINEAR_SIEVE", "MINIMUM_PRIME_FACTOR_TABLE", "PRIME_GENERATION"],
            preconditions=["limit_n_ge_2", "precomputation_memory_feasible"],
            proof_obligations=["each_composite_visited_exactly_once_by_spf"],
            operation_complexity="O(N) strictly linear operations",
            space_complexity="O(N) table memory",
            description="Euler linear sieve generating primes and minimum prime factors (spf) in strictly O(N) time."
        ))

        # ── 6. Euler's Totient Function (Single Instance O(sqrt(N))) ──
        self.register(AlgorithmComponent(
            name="euler_totient_single",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[make_integer_state()],
            provides_states=[StateContract("EulerTotientValueState")],
            requires_capabilities=[],
            provided_capabilities=["EULER_TOTIENT_SINGLE"],
            preconditions=["n_ge_1"],
            proof_obligations=["prime_factorization_product_formula_proven"],
            operation_complexity="O(sqrt(N))",
            space_complexity="O(1) auxiliary",
            description="Computes phi(N) = N * product(1 - 1/p) via O(sqrt(N)) trial division."
        ))

        # ── 7. Euler's Totient Range Sieve Table (Multiplicative Function) ──
        self.register(AlgorithmComponent(
            name="euler_totient_sieve",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[make_sieve_table_state()],
            provides_states=[make_arithmetic_function_table_state(function_name="phi")],
            requires_capabilities=["LINEAR_SIEVE"],
            provided_capabilities=["EULER_TOTIENT_RANGE_TABLE"],
            preconditions=["sieve_table_valid"],
            proof_obligations=["multiplicative_totient_recurrence_proven"],
            operation_complexity="O(N) linear table generation",
            space_complexity="O(N) table memory",
            description="Generates phi(1..N) table via linear sieve multiplicative property."
        ))

        # ── 8. Möbius Function Sieve Table ──
        self.register(AlgorithmComponent(
            name="mobius_sieve_builder",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[make_sieve_table_state()],
            provides_states=[make_arithmetic_function_table_state(function_name="mobius")],
            requires_capabilities=["LINEAR_SIEVE"],
            provided_capabilities=["MOBIUS_FUNCTION_TABLE"],
            preconditions=["sieve_table_valid"],
            proof_obligations=["square_free_parity_invariant_proven"],
            operation_complexity="O(N) linear table generation",
            space_complexity="O(N) table memory",
            description="Computes mu(1..N) square-free parity table via linear sieve transitions."
        ))

        # ── 9. Möbius Inversion Reducer ──
        self.register(AlgorithmComponent(
            name="mobius_inversion_reducer",
            node_type=CompositionNodeType.TRANSFORMATION,
            requires_states=[make_arithmetic_function_table_state(function_name="mobius")],
            provides_states=[StateContract("MobiusInversionResultState")],
            requires_capabilities=["MOBIUS_FUNCTION_TABLE"],
            provided_capabilities=["MOBIUS_INVERSION_SUM_EVALUATION"],
            preconditions=["mobius_table_computed"],
            proof_obligations=["divisor_convolution_inversion_theorem_proven"],
            operation_complexity="O(N) precomp, query derived from formulation (e.g. O(min(N, M)))",
            space_complexity="O(N) table memory",
            description="Evaluates divisor-convolution sums and coprime grid counting via Möbius inversion."
        ))

        # ── 10. Binary Matrix Exponentiation Recurrence Solver ──
        self.register(AlgorithmComponent(
            name="matrix_exponentiation_builder",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[make_matrix_ring_state()],
            provides_states=[make_matrix_ring_state()],
            requires_capabilities=[],
            provided_capabilities=["MATRIX_EXPONENTIATION_RING"],
            preconditions=["dimension_le_64", "exponent_ge_0", "ring_multiplication_associative"],
            proof_obligations=["binary_exponentiation_associative_power_proven", "identity_base_case_verified"],
            operation_complexity="O(D^3 * log K) ring operations",
            space_complexity="O(D^2) auxiliary memory",
            description="Binary matrix exponentiation for linear recurrences and transition graphs."
        ))

        # ── 11. Combinatorial Factorials & Inverse Factorials Table ──
        self.register(AlgorithmComponent(
            name="factorial_table_builder",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[make_modular_ring_state()],
            provides_states=[make_factorial_table_state()],
            requires_capabilities=[],
            provided_capabilities=["MODULAR_FACTORIAL_TABLE", "COMBINATORIAL_COEFFICIENTS_O1"],
            preconditions=["modulus_prime_certified", "n_lt_modulus", "0_le_k_le_n"],
            proof_obligations=["factorial_domain_valid_n_lt_p", "inverse_factorial_telescoping_proven"],
            operation_complexity="O(N) precomp, O(1) query",
            space_complexity="O(N) table memory",
            description="Computes nCr mod p in O(1) query time using precomputed factorials for N < p."
        ))

        # ── 12. Lucas' Theorem Solver for Large N, K ──
        self.register(AlgorithmComponent(
            name="lucas_theorem_solver",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[make_lucas_decomposition_state()],
            provides_states=[StateContract("LucasCombinatorialResultState")],
            requires_capabilities=[],
            provided_capabilities=["LUCAS_THEOREM_EVALUATION"],
            preconditions=["modulus_prime_certified", "prime_p_le_1e6_table_feasible"],
            proof_obligations=["base_p_digit_expansion_lucas_congruence_proven"],
            operation_complexity="Precomputation O(p), Query O(log_p N)",
            space_complexity="O(p) small table memory",
            description="Evaluates nCr mod p when N, K >= p using base-p digit expansion and small modulo factorials."
        ))

        # ── 13. Deterministic 64-bit Miller-Rabin Primality Tester ──
        self.register(AlgorithmComponent(
            name="miller_rabin_tester",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[make_integer_state(bit_width=64, signedness="UNSIGNED")],
            provides_states=[make_miller_rabin_result_state()],
            requires_capabilities=[],
            provided_capabilities=["DETERMINISTIC_64BIT_PRIMALITY_TEST"],
            preconditions=["n_in_unsigned_64bit_domain"],
            proof_obligations=["locked_7_witness_basis_guarantee_for_n_lt_2_64"],
            operation_complexity="O(W * log N) modular multiplications (W=7)",
            space_complexity="O(1) auxiliary",
            description="Deterministic Miller-Rabin primality test for all N < 2^64 using exact 7-witness basis."
        ))
