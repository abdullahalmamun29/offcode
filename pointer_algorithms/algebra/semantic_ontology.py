"""
CHUP Phase 3Q — Semantic Algebra / Transforms Ontology & Provenance Model.

Defines orthogonal primitive algebraic dimensions, numerical floating-point policies,
and derived structural properties with complete provenance. Zero algorithm names allowed.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional


# ── 1. Primitive Algebraic Dimensions ──

class TransformDomainType(str, Enum):
    COMPLEX_FIELD = "COMPLEX_FIELD"             # Continuous complex field C with roots of unity e^(2pi*i/N)
    FINITE_FIELD_ROOTS = "FINITE_FIELD_ROOTS"   # Finite field F_p with primitive root g and order-N element omega
    WALSH_HYPERCUBE = "WALSH_HYPERCUBE"         # Discrete hypercube group (Z/2Z)^B under bitwise XOR


class AlgebraicFieldType(str, Enum):
    REAL_FIELD = "REAL_FIELD"                   # Continuous real field R (approximate floating point)
    COMPLEX_FIELD = "COMPLEX_FIELD"             # Continuous complex field C
    PRIME_FIELD = "PRIME_FIELD"                 # Exact finite field F_p
    BINARY_FIELD_F2 = "BINARY_FIELD_F2"         # Exact Galois field GF(2)
    GENERAL_RING = "GENERAL_RING"               # Modular ring Z/mZ (may contain zero-divisors)


class MatrixScalarDomain(str, Enum):
    REAL_SCALAR = "REAL_SCALAR"                 # Matrices over R requiring FloatingPointPolicy
    MODULAR_SCALAR = "MODULAR_SCALAR"           # Matrices over F_p requiring certified prime modulus
    BINARY_BITSET = "BINARY_BITSET"             # Packed word bitset matrices over F_2


class BasisBitwidth(str, Enum):
    BITS_32 = "BITS_32"                         # 32-bit unsigned integer vectors in F_2^32
    BITS_64 = "BITS_64"                         # 64-bit unsigned integer vectors in F_2^64


class SystemConsistency(str, Enum):
    UNIQUE_SOLUTION = "UNIQUE_SOLUTION"         # rank(A) == rank([A|b]) == n
    INFINITE_SOLUTIONS = "INFINITE_SOLUTIONS"   # rank(A) == rank([A|b]) < n
    INCONSISTENT = "INCONSISTENT"               # rank(A) < rank([A|b]) (pivot in constant column)


class PolynomialOperation(str, Enum):
    CONVOLUTION = "CONVOLUTION"                 # Multiplication A(x) * B(x)
    INVERSION = "INVERSION"                     # Formal power series inverse A(x)^(-1) mod x^N
    INTERPOLATION = "INTERPOLATION"             # Evaluating or reconstructing polynomial from points
    RECURRENCE = "RECURRENCE"                   # Finding minimal recurrence and N-th term evaluation


class CorrectnessGuarantee(str, Enum):
    DETERMINISTIC_EXACT = "DETERMINISTIC_EXACT"                                 # Mathematically exact result
    CORRECTNESS_NUMERIC_APPROXIMATE = "CORRECTNESS_NUMERIC_APPROXIMATE"         # Approximate subject to floating-point tolerance


# ── 2. Numerical Floating-Point Policy ──

@dataclass
class FloatingPointPolicy:
    """
    Explicit contract governing numerical rank, singularity, and pivot acceptance.
    Singularity decisions must originate from this policy, never from |det(A)| <= eps.
    """
    absolute_tolerance: float = 1e-9
    relative_tolerance: float = 1e-9
    pivot_strategy: str = "PARTIAL_PIVOTING_COLUMN_MAX"
    scale_metric: str = "ROW_NORM_MAX"

    def is_pivot_acceptable(self, pivot_abs: float, row_scale: float = 1.0) -> bool:
        threshold = max(self.absolute_tolerance, self.relative_tolerance * row_scale)
        return pivot_abs > threshold


# ── 3. Atomic Algebra Objectives ──

class AlgebraObjective(str, Enum):
    FAST_FOURIER_TRANSFORM = "FAST_FOURIER_TRANSFORM"                   # Complex continuous FFT
    NUMBER_THEORETIC_TRANSFORM = "NUMBER_THEORETIC_TRANSFORM"           # Exact modular NTT
    FAST_WALSH_HADAMARD_TRANSFORM = "FAST_WALSH_HADAMARD_TRANSFORM"     # Strictly XOR convolution over (Z/2Z)^B
    POLYNOMIAL_INVERSION = "POLYNOMIAL_INVERSION"                       # Newton's method on formal power series
    GAUSSIAN_ELIMINATION_REAL = "GAUSSIAN_ELIMINATION_REAL"             # Linear systems over R with FloatingPointPolicy
    GAUSSIAN_ELIMINATION_MODULAR = "GAUSSIAN_ELIMINATION_MODULAR"       # Exact linear systems over F_p
    GAUSSIAN_ELIMINATION_XOR = "GAUSSIAN_ELIMINATION_XOR"               # Bitset linear systems over F_2
    LINEAR_BASIS_XOR = "LINEAR_BASIS_XOR"                               # Subspace basis in F_2^B
    BERLEKAMP_MASSEY_RECURRENCE = "BERLEKAMP_MASSEY_RECURRENCE"         # Minimal recurrence & N-th term query
    LAGRANGE_INTERPOLATION = "LAGRANGE_INTERPOLATION"                   # Degree-d polynomial evaluation from points
    OUT_OF_SCOPE_NONLINEAR_SYSTEM = "OUT_OF_SCOPE_NONLINEAR_SYSTEM"     # Nonlinear algebraic equations / Newton-Raphson
    OUT_OF_SCOPE_SIMULATION = "OUT_OF_SCOPE_SIMULATION"                 # Generic ad-hoc simulation
    NONE = "NONE"


# ── 4. Provenance Dataclass ──

class ProvenanceStatus(str, Enum):
    PROVEN = "PROVEN"
    UNPROVEN = "UNPROVEN"
    CONTRADICTED = "CONTRADICTED"


@dataclass
class DerivedFact:
    """
    Formal record tracking how an algebraic, structural, or numerical property was deduced.
    """
    fact_id: str
    value: Any
    source_facts: List[str] = field(default_factory=list)
    derivation_rule: str = ""
    proof_obligations: List[str] = field(default_factory=list)
    status: ProvenanceStatus = ProvenanceStatus.PROVEN


# ── 5. Semantic Algebra Model ──

@dataclass
class SemanticAlgebraModel:
    """
    Complete semantic representation of an algebraic or transformation problem.
    Zero algorithm names allowed.
    """
    transform_domain: TransformDomainType = TransformDomainType.FINITE_FIELD_ROOTS
    algebraic_field: AlgebraicFieldType = AlgebraicFieldType.PRIME_FIELD
    matrix_scalar_domain: MatrixScalarDomain = MatrixScalarDomain.MODULAR_SCALAR
    basis_bitwidth: BasisBitwidth = BasisBitwidth.BITS_64
    correctness_guarantee: CorrectnessGuarantee = CorrectnessGuarantee.DETERMINISTIC_EXACT
    objective: AlgebraObjective = AlgebraObjective.NONE
    floating_point_policy: FloatingPointPolicy = field(default_factory=FloatingPointPolicy)

    # Concrete parameters
    modulus_value: Optional[int] = None
    primitive_root_value: Optional[int] = None
    transform_length: Optional[int] = None
    matrix_rows: Optional[int] = None
    matrix_cols: Optional[int] = None
    interpolation_degree: Optional[int] = None
    is_contiguous_interpolation: bool = False
    sequence_terms_count: Optional[int] = None
    target_query_n: Optional[int] = None

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
