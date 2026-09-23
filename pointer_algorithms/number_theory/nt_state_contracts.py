"""
CHUP Phase 3P — Number Theory State Contracts & Type System.

Enforces strict semantic substitutability and attribute unification for algebraic,
modular, sieve, and combinatorial structures. Implementation ancestry does NOT imply IS-A.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

from pointer_algorithms.number_theory.verification.nt_oracles import miller_rabin_deterministic


@dataclass
class StateContract:
    """
    Formal contract definition for a mathematical or data state.
    Enforces explicit subtyping (supertypes) and attribute unification.
    """
    name: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    supertypes: List[str] = field(default_factory=list)

    def satisfies(self, requirement: 'StateContract') -> bool:
        """
        Returns True iff this state contract satisfies the requirement contract:
        1. Type compatibility: exact name match or declared supertype ancestry.
        2. Attribute unification: all required attributes must exist and match values if specified.
        """
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

def make_integer_state(value: int = 0, bit_width: int = 64, signedness: str = "SIGNED") -> StateContract:
    return StateContract(
        name="IntegerState",
        attributes={
            "value": value,
            "bit_width": bit_width,
            "signedness": signedness,
        }
    )


def make_diophantine_system_state(a: int = 0, b: int = 0, c: int = 0, gcd_val: int = 1,
                                   x0: int = 0, y0: int = 0, step_x: int = 0, step_y: int = 0) -> StateContract:
    return StateContract(
        name="DiophantineSystemState",
        attributes={
            "a": a,
            "b": b,
            "c": c,
            "gcd_val": gcd_val,
            "x0": x0,
            "y0": y0,
            "step_x": step_x,
            "step_y": step_y,
        }
    )


def make_modular_ring_state(modulus: int = 1000000007, prime_certificate: Optional[StateContract] = None) -> StateContract:
    """
    Constructs a ModularRingState.
    CRITICAL PROVENANCE INVARIANT:
    is_prime and is_field CANNOT be asserted by a caller boolean.
    Field properties are derived ONLY if a valid deterministic MillerRabinResultState
    certifies the modulus as prime.
    """
    is_prime = False
    is_field = False
    if prime_certificate is not None:
        if (prime_certificate.name == "MillerRabinResultState" and
            prime_certificate.attributes.get("result") is True and
            prime_certificate.attributes.get("n") == modulus and
            prime_certificate.attributes.get("deterministic_64bit") is True):
            is_prime = True
            is_field = True

    return StateContract(
        name="ModularRingState",
        attributes={
            "modulus": modulus,
            "is_prime": is_prime,
            "is_field": is_field,
            "has_prime_certificate": is_prime,
        }
    )


def make_modular_inverse_state(element: int = 1, modulus: int = 1000000007, inv: int = 1, method: str = "extgcd") -> StateContract:
    return StateContract(
        name="ModularInverseState",
        attributes={
            "element": element,
            "modulus": modulus,
            "inv": inv,
            "method": method,
        },
        supertypes=["ModularRingState"]  # ModularInverseState IS-A ModularRingState
    )


def make_crt_system_state(congruence_count: int = 2, current_modulus: int = 1, current_residue: int = 0) -> StateContract:
    return StateContract(
        name="CRTSystemState",
        attributes={
            "congruence_count": congruence_count,
            "current_modulus": current_modulus,
            "current_residue": current_residue,
        }
    )


def make_sieve_table_state(limit_n: int = 1000000, has_spf: bool = True) -> StateContract:
    return StateContract(
        name="SieveTableState",
        attributes={
            "limit_n": limit_n,
            "has_spf": has_spf,
        }
    )


def make_arithmetic_function_table_state(function_name: str = "phi", limit_n: int = 1000000,
                                         source_sieve_capability: str = "linear_sieve_builder") -> StateContract:
    # CRITICAL ARCHITECTURAL PRINCIPLE: Does NOT inherit SieveTableState!
    # Implementation ancestry does NOT imply semantic subtyping.
    return StateContract(
        name="ArithmeticFunctionTableState",
        attributes={
            "function_name": function_name,
            "limit_n": limit_n,
            "source_sieve_capability": source_sieve_capability,
        },
        supertypes=[]  # Independent state contract!
    )


def make_matrix_ring_state(dimension: int = 2, exponent: int = 1, modulus: int = 1000000007, is_modular: bool = True) -> StateContract:
    return StateContract(
        name="MatrixRingState",
        attributes={
            "dimension": dimension,
            "exponent": exponent,
            "modulus": modulus,
            "is_modular": is_modular,
        }
    )


def make_divisor_lattice_state(n: int = 1) -> StateContract:
    # Invariant: Divisor lattice state does NOT inherit DirectedAcyclicGraph
    return StateContract(
        name="DivisorLatticeState",
        attributes={
            "n": n,
        },
        supertypes=[]
    )


def make_factorial_table_state(limit_n: int = 1000000, modulus: int = 1000000007) -> StateContract:
    return StateContract(
        name="FactorialTableState",
        attributes={
            "limit_n": limit_n,
            "modulus": modulus,
        }
    )


def make_lucas_decomposition_state(n: int = 0, k: int = 0, prime_p: int = 1000003) -> StateContract:
    return StateContract(
        name="LucasDecompositionState",
        attributes={
            "n": n,
            "k": k,
            "prime_p": prime_p,
        }
    )


def make_miller_rabin_result_state(n: int = 0, witness_basis: Optional[List[int]] = None) -> StateContract:
    # Locked 7-witness deterministic basis covering all N < 2^64
    basis = witness_basis or [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
    # Invariant: Certification must originate from capability execution, never caller assertion
    is_prime_result = miller_rabin_deterministic(n) if n > 0 else False
    return StateContract(
        name="MillerRabinResultState",
        attributes={
            "n": n,
            "witness_basis": basis,
            "result": is_prime_result,
            "deterministic_64bit": True,
            "certification_method": "DETERMINISTIC_7_WITNESS_BASIS",
        }
    )
