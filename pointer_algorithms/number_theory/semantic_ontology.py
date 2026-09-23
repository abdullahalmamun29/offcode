"""
CHUP Phase 3P — Semantic Number Theory Ontology & Provenance Model.

Defines orthogonal, primitive mathematical dimensions, arithmetic safety facts,
and derived structural properties with complete provenance. Zero algorithm labels allowed.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional


# ── 1. Primitive Mathematical Dimensions ──

class IntegerMagnitude(str, Enum):
    MAGNITUDE_LE_1E6 = "MAGNITUDE_LE_1E6"       # N <= 10^6: Full precomputation table O(N) is feasible under standard 256MB limit
    MAGNITUDE_LE_1E9 = "MAGNITUDE_LE_1E9"       # N <= 10^9: Requires O(sqrt(N)) or O(log N); O(N) memory infeasible
    MAGNITUDE_LE_1E18 = "MAGNITUDE_LE_1E18"     # N <= 10^18: Signed 64-bit integer; modular products require 128-bit
    MAGNITUDE_HUGE = "MAGNITUDE_HUGE"           # N >= 2^64: Exceeds standard 64-bit register


class ModulusCharacteristic(str, Enum):
    PRIME_MODULUS = "PRIME_MODULUS"             # Field F_p; Fermat inverse valid; zero-divisors absent
    COMPOSITE_COPRIME = "COMPOSITE_COPRIME"     # Moduli pairwise coprime; classical CRT applies directly
    GENERAL_COMPOSITE = "GENERAL_COMPOSITE"     # Ring Z/mZ; ExtGCD required; non-coprime CRT requires solvability checks
    UNMODULARIZED_EXACT = "UNMODULARIZED_EXACT" # Exact arithmetic without modular reduction


class ArithmeticMode(str, Enum):
    MODULAR_FIXED_WIDTH = "MODULAR_FIXED_WIDTH"         # Modular computation within fixed integer registers
    EXACT_BOUNDED_INT64 = "EXACT_BOUNDED_INT64"         # Exact computation guaranteed to fit in signed 64-bit integer
    EXACT_BOUNDED_INT128 = "EXACT_BOUNDED_INT128"       # Exact computation guaranteed to fit in signed 128-bit integer
    EXACT_BIGINT_UNSUPPORTED = "EXACT_BIGINT_UNSUPPORTED" # Unbounded exact arithmetic exceeding 128 bits (fails closed)


class QueryMultiplicity(str, Enum):
    SINGLE_INSTANCE = "SINGLE_INSTANCE"         # One-off computation; no precomputed state needed
    MULTI_QUERY = "MULTI_QUERY"                 # Repeated queries; precomputed factorials/sieve beneficial
    RANGE_PREFIX = "RANGE_PREFIX"               # Entire table 1..N required


class AlgebraicStructure(str, Enum):
    DIOPHANTINE_LATTICE = "DIOPHANTINE_LATTICE"
    MODULAR_RING = "MODULAR_RING"
    PRIME_FIELD = "PRIME_FIELD"
    MULTIPLICATIVE_FUNCTION = "MULTIPLICATIVE_FUNCTION"
    MATRIX_RING = "MATRIX_RING"


class CorrectnessGuarantee(str, Enum):
    DETERMINISTIC_EXACT = "DETERMINISTIC_EXACT"                   # Provably correct without failure probability
    DETERMINISTIC_BOUNDED_BASIS = "DETERMINISTIC_BOUNDED_BASIS"   # Deterministic Miller-Rabin test over locked 7-witness basis for N < 2^64


class ResourceConstraint(str, Enum):
    STANDARD_COMPETITIVE = "STANDARD_COMPETITIVE"   # 1000ms / 256MB
    EXTENDED_TIME = "EXTENDED_TIME"                 # 2000ms+
    TIGHT_MEMORY = "TIGHT_MEMORY"                   # 64MB or less
    LARGE_MEMORY = "LARGE_MEMORY"                   # 512MB or more


# ── 2. Atomic Number Theory Objectives ──

class NumberTheoryObjective(str, Enum):
    GREATEST_COMMON_DIVISOR_BEZOUT = "GREATEST_COMMON_DIVISOR_BEZOUT" # Extended GCD & linear Diophantine family
    MODULAR_INVERSE = "MODULAR_INVERSE"                               # Inverse in ring Z/mZ or field F_p
    CHINESE_REMAINDER_SYSTEM = "CHINESE_REMAINDER_SYSTEM"             # System of modular congruences
    LINEAR_SIEVE_FACTORIZATION = "LINEAR_SIEVE_FACTORIZATION"         # O(N) linear sieve and SPF table
    EULER_TOTIENT_EVALUATION = "EULER_TOTIENT_EVALUATION"             # phi(n) single or range table
    MOBIUS_INVERSION_SUM = "MOBIUS_INVERSION_SUM"                     # mu(n) table and divisor-convolution sums
    MATRIX_POWER_RECURRENCE = "MATRIX_POWER_RECURRENCE"               # Binary matrix exponentiation for recurrences
    COMBINATORIAL_COEFFICIENTS_FACTORIAL = "COMBINATORIAL_COEFFICIENTS_FACTORIAL" # nCr mod p via precomputed factorials
    LUCAS_THEOREM_COMBINATORICS = "LUCAS_THEOREM_COMBINATORICS"       # nCr mod p for large N, K with small prime p
    MILLER_RABIN_PRIMALITY = "MILLER_RABIN_PRIMALITY"                 # Deterministic 64-bit primality certification
    OUT_OF_SCOPE_ELLIPTIC_CURVE = "OUT_OF_SCOPE_ELLIPTIC_CURVE"       # Elliptic curve point counting / Schoof's algorithm
    OUT_OF_SCOPE_GAME_THEORY = "OUT_OF_SCOPE_GAME_THEORY"             # Nim-sum / Sprague-Grundy game theory
    OUT_OF_SCOPE_SIMULATION = "OUT_OF_SCOPE_SIMULATION"               # Calendar date simulation
    NONE = "NONE"


# ── 3. Provenance Dataclass ──

class ProvenanceStatus(str, Enum):
    PROVEN = "PROVEN"
    UNPROVEN = "UNPROVEN"
    CONTRADICTED = "CONTRADICTED"


@dataclass
class DerivedFact:
    """
    Formal record tracking how an algebraic, structural, or arithmetic safety property was deduced.
    """
    fact_id: str
    value: Any
    source_facts: List[str] = field(default_factory=list)
    derivation_rule: str = ""
    proof_obligations: List[str] = field(default_factory=list)
    status: ProvenanceStatus = ProvenanceStatus.PROVEN


# ── 4. Semantic Number Theory Model ──

@dataclass
class SemanticNumberTheoryModel:
    """
    Complete semantic representation of a number-theoretic or combinatorial problem.
    Contains primitive facts and derived structural/safety properties with full provenance.
    Zero algorithm names allowed.
    """
    # Primitive mathematical facts
    integer_magnitude: IntegerMagnitude = IntegerMagnitude.MAGNITUDE_LE_1E9
    modulus_characteristic: ModulusCharacteristic = ModulusCharacteristic.GENERAL_COMPOSITE
    arithmetic_mode: ArithmeticMode = ArithmeticMode.MODULAR_FIXED_WIDTH
    query_multiplicity: QueryMultiplicity = QueryMultiplicity.SINGLE_INSTANCE
    algebraic_structure: AlgebraicStructure = AlgebraicStructure.MODULAR_RING
    correctness_guarantee: CorrectnessGuarantee = CorrectnessGuarantee.DETERMINISTIC_EXACT
    objective: NumberTheoryObjective = NumberTheoryObjective.NONE

    # Resource constraints
    resource_constraint: ResourceConstraint = ResourceConstraint.STANDARD_COMPETITIVE
    time_limit_ms: int = 1000
    memory_limit_mb: int = 256

    # Concrete parameters
    n_bound: Optional[int] = None
    k_bound: Optional[int] = None
    modulus_value: Optional[int] = None
    matrix_dimension: Optional[int] = None

    # Derived properties & provenance
    derived_properties: Dict[str, Any] = field(default_factory=dict)
    provenance_records: List[DerivedFact] = field(default_factory=list)

    def add_derived_property(
        self,
        fact_id: str,
        value: Any,
        source_facts: List[str],
        rule: str,
        obligations: Optional[List[str]] = None
    ) -> None:
        self.derived_properties[fact_id] = value
        self.provenance_records.append(DerivedFact(
            fact_id=fact_id,
            value=value,
            source_facts=source_facts,
            derivation_rule=rule,
            proof_obligations=obligations or [],
            status=ProvenanceStatus.PROVEN
        ))

    def has_derived_fact(self, fact_id: str) -> bool:
        return self.derived_properties.get(fact_id, False) is True
