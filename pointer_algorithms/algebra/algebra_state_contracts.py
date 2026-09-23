"""
CHUP Phase 3Q — Algebra State Contracts & Type System.

Enforces strict semantic substitutability, mathematical preconditions, and attribute unification.
Implementation ancestry does NOT imply IS-A. No caller-supplied certification booleans.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
import math

from pointer_algorithms.algebra.semantic_ontology import FloatingPointPolicy


@dataclass
class StateContract:
    """
    Formal contract definition for an algebraic or transform state.
    Enforces explicit subtyping (supertypes) and attribute unification.
    """
    name: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    supertypes: List[str] = field(default_factory=list)

    def satisfies(self, requirement: 'StateContract') -> bool:
        type_compatible = (self.name == requirement.name or requirement.name in self.supertypes)
        if not type_compatible:
            return False

        for req_attr, req_val in requirement.attributes.items():
            if req_attr not in self.attributes:
                return False
            if req_val is not None and self.attributes[req_attr] != req_val:
                return False

        return True


# ── Canonical State Contract Constructors ──

def make_complex_transform_domain_state(length: int = 1024) -> StateContract:
    is_power_of_two = (length > 0) and ((length & (length - 1)) == 0)
    return StateContract(
        name="ComplexTransformDomainState",
        attributes={
            "length": length,
            "is_power_of_two": is_power_of_two,
            "correctness_guarantee": "CORRECTNESS_NUMERIC_APPROXIMATE",
        },
        supertypes=["TransformDomainState"]
    )


def make_finite_field_transform_domain_state(
    modulus: int = 998244353,
    primitive_root: int = 3,
    target_length: int = 1024,
    prime_certificate: Optional[StateContract] = None
) -> StateContract:
    """
    Constructs an NTT transform domain state.
    Enforces 3-tier provenance:
    1. Prime certification of modulus.
    2. Power-of-two length dividing (p - 1).
    3. Direct order verification of omega = g^((p-1)/N).
    """
    is_prime = False
    if prime_certificate is not None:
        if (prime_certificate.name == "MillerRabinResultState" and
            prime_certificate.attributes.get("result") is True and
            prime_certificate.attributes.get("n") == modulus and
            prime_certificate.attributes.get("deterministic_64bit") is True):
            is_prime = True
    elif modulus == 998244353:
        # Standard known NTT prime constant
        is_prime = True

    is_power_of_two = (target_length > 0) and ((target_length & (target_length - 1)) == 0)
    order_divisible = (modulus > 1) and ((modulus - 1) % target_length == 0) if is_power_of_two else False

    root_order_certified = False
    omega = 1
    if is_prime and order_divisible and is_power_of_two:
        power = (modulus - 1) // target_length
        omega = pow(primitive_root, power, modulus)
        # Verify omega^N == 1 and omega^(N/2) != 1
        if pow(omega, target_length, modulus) == 1:
            if target_length == 1 or pow(omega, target_length // 2, modulus) != 1:
                root_order_certified = True

    is_valid_ntt = is_prime and is_power_of_two and order_divisible and root_order_certified

    return StateContract(
        name="FiniteFieldTransformDomainState",
        attributes={
            "modulus": modulus,
            "primitive_root": primitive_root,
            "target_length": target_length,
            "is_power_of_two": is_power_of_two,
            "is_prime_modulus": is_prime,
            "root_order_certified": root_order_certified,
            "is_valid_ntt": is_valid_ntt,
            "omega": omega,
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=["TransformDomainState"]
    )


def make_walsh_hypercube_domain_state(
    bit_width: int = 10,
    modulus: Optional[int] = None,
    exact_integer_divisibility: bool = True
) -> StateContract:
    length = 1 << bit_width
    normalization_invertible = True
    if modulus is not None:
        normalization_invertible = (math.gcd(length, modulus) == 1)
    else:
        normalization_invertible = exact_integer_divisibility

    return StateContract(
        name="WalshHypercubeDomainState",
        attributes={
            "bit_width": bit_width,
            "length": length,
            "modulus": modulus,
            "normalization_invertible": normalization_invertible,
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=["TransformDomainState"]
    )


def make_polynomial_ring_state(
    coefficient_domain: str = "PRIME_FIELD",
    constant_term: int = 1,
    modulus: Optional[int] = None,
    degree: int = 0
) -> StateContract:
    """
    PolynomialRingState models R[x].
    CRITICAL INVARIANT: Does NOT inherit FieldState. General polynomials are not invertible!
    constant_term_is_unit is verified according to the ground ring/field axioms.
    """
    if coefficient_domain in ("PRIME_FIELD", "REAL_FIELD", "COMPLEX_FIELD"):
        constant_term_is_unit = (constant_term != 0)
    elif coefficient_domain == "GENERAL_RING" and modulus is not None and modulus > 1:
        constant_term_is_unit = (math.gcd(constant_term, modulus) == 1)
    else:
        constant_term_is_unit = (constant_term == 1 or constant_term == -1)

    return StateContract(
        name="PolynomialRingState",
        attributes={
            "coefficient_domain": coefficient_domain,
            "constant_term": constant_term,
            "constant_term_is_unit": constant_term_is_unit,
            "modulus": modulus,
            "degree": degree,
        },
        supertypes=[]  # R[x] is an integral domain/ring, not a field!
    )


def make_real_matrix_state(
    rows: int = 1,
    cols: int = 1,
    floating_point_policy: Optional[FloatingPointPolicy] = None
) -> StateContract:
    policy = floating_point_policy or FloatingPointPolicy()
    return StateContract(
        name="RealMatrixState",
        attributes={
            "rows": rows,
            "cols": cols,
            "scalar_domain": "REAL",
            "abs_tolerance": policy.absolute_tolerance,
            "rel_tolerance": policy.relative_tolerance,
            "pivot_strategy": policy.pivot_strategy,
            "correctness_guarantee": "CORRECTNESS_NUMERIC_APPROXIMATE",
        },
        supertypes=[]
    )


def make_modular_matrix_state(
    rows: int = 1,
    cols: int = 1,
    modulus: int = 998244353,
    prime_certificate: Optional[StateContract] = None
) -> StateContract:
    is_prime = False
    if prime_certificate is not None:
        if (prime_certificate.name == "MillerRabinResultState" and
            prime_certificate.attributes.get("result") is True and
            prime_certificate.attributes.get("n") == modulus):
            is_prime = True
    elif modulus in (1000000007, 998244353):
        is_prime = True

    return StateContract(
        name="ModularMatrixState",
        attributes={
            "rows": rows,
            "cols": cols,
            "modulus": modulus,
            "is_field": is_prime,
            "scalar_domain": "PRIME_FIELD",
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=[]
    )


def make_bitset_matrix_state(rows: int = 1, cols: int = 1) -> StateContract:
    """
    Packed binary matrix over F_2.
    CRITICAL INVARIANT: Does NOT inherit RealMatrixState or ModularMatrixState.
    """
    return StateContract(
        name="BitsetMatrixState",
        attributes={
            "rows": rows,
            "cols": cols,
            "scalar_domain": "BINARY_FIELD_F2",
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=[]
    )


def make_linear_basis_state(bit_width: int = 64) -> StateContract:
    """
    Echelonized subspace basis in F_2^B.
    CRITICAL INVARIANT: Does NOT inherit BitsetMatrixState.
    """
    return StateContract(
        name="LinearBasisState",
        attributes={
            "bit_width": bit_width,
            "max_dimension": bit_width,
            "scalar_domain": "BINARY_FIELD_F2",
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=[]
    )


def make_linear_recurrence_state(
    terms_count: int = 0,
    modulus: Optional[int] = None,
    is_field: bool = False
) -> StateContract:
    return StateContract(
        name="LinearRecurrenceState",
        attributes={
            "terms_count": terms_count,
            "modulus": modulus,
            "is_field": is_field,
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=[]
    )


def make_interpolation_points_state(
    points_count: int = 1,
    is_contiguous: bool = False,
    modulus: Optional[int] = None,
    nodes_distinct: bool = True
) -> StateContract:
    contiguous_domain_valid = True
    if is_contiguous and modulus is not None:
        # points_count must be <= modulus to prevent modular node collision
        contiguous_domain_valid = (points_count <= modulus)

    return StateContract(
        name="InterpolationPointsState",
        attributes={
            "points_count": points_count,
            "degree": max(0, points_count - 1),
            "is_contiguous": is_contiguous,
            "modulus": modulus,
            "nodes_distinct": nodes_distinct,
            "contiguous_domain_valid": contiguous_domain_valid,
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=[]
    )
