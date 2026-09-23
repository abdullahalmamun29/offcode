"""
Phase 9 — diagnostic_types.py

All enumerations, deeply frozen dataclasses, and certificate types
for the self-diagnosis subsystem. No mutable state. No Phase 5/6/7/8 mutation.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional, Tuple, Union


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class DiagnosticMode(str, Enum):
    """Authoritative classification of what went wrong."""
    UNKNOWN_FAMILY = "UNKNOWN_FAMILY"
    KNOWN_FAMILY_INVALID_ASSUMPTIONS = "KNOWN_FAMILY_INVALID_ASSUMPTIONS"
    VALID_CANDIDATE_IMPLEMENTATION_BUG = "VALID_CANDIDATE_IMPLEMENTATION_BUG"
    AMBIGUOUS_CANDIDATE_SET = "AMBIGUOUS_CANDIDATE_SET"
    ORACLE_DEFECT = "ORACLE_DEFECT"
    TEST_HARNESS_DEFECT = "TEST_HARNESS_DEFECT"


class ClassificationStatus(str, Enum):
    """Whether a definitive classification was reached."""
    CLASSIFIED = "CLASSIFIED"
    UNRESOLVED = "UNRESOLVED"  # Insufficient evidence — fail closed


class OracleStatus(str, Enum):
    """
    Oracle integrity evaluation result.

    Only DEFECT_CONFIRMED maps to ORACLE_DEFECT.
    INCONSISTENT / UNRESOLVED map to UNRESOLVED (Priority 7).
    A metamorphic inconsistency proves inconsistency, NOT oracle defect.
    """
    HEALTHY = "HEALTHY"
    DEFECT_CONFIRMED = "DEFECT_CONFIRMED"   # Crash / exception / cross-run divergence
    INCONSISTENT = "INCONSISTENT"           # Metamorphic property violated
    UNRESOLVED = "UNRESOLVED"               # No usable output, non-crash reason


class HarnessStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEFECT_CONFIRMED = "DEFECT_CONFIRMED"


class ImplementationBugKind(str, Enum):
    """Certified, pre-enumerated implementation defect classes."""
    MISSING_HEADER = "MISSING_HEADER"
    TYPE_WIDTH_MISMATCH = "TYPE_WIDTH_MISMATCH"
    CERTIFIED_INDEX_BASE_TRANSLATION = "CERTIFIED_INDEX_BASE_TRANSLATION"
    CERTIFIED_BOUNDARY_GUARD = "CERTIFIED_BOUNDARY_GUARD"
    UNCLASSIFIED_CODE_DEFECT = "UNCLASSIFIED_CODE_DEFECT"


class RepairStrategy(str, Enum):
    """One-to-one mapping to ImplementationBugKind (except UNCLASSIFIED → NONE)."""
    ADD_MISSING_HEADER = "ADD_MISSING_HEADER"
    WIDEN_TO_64BIT = "WIDEN_TO_64BIT"
    ADJUST_INDEX_BASE = "ADJUST_INDEX_BASE"
    INSERT_BOUNDARY_GUARD = "INSERT_BOUNDARY_GUARD"
    NONE = "NONE"


class ReproducibilityStatus(str, Enum):
    CONTROLLED_REPRODUCIBLE = "CONTROLLED_REPRODUCIBLE"
    NOT_REPRODUCIBLE = "NOT_REPRODUCIBLE"
    UNVERIFIED = "UNVERIFIED"


# ---------------------------------------------------------------------------
# Structured Mathematical Repair Evidence
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class OverflowEvidence:
    """
    Proven integer overflow requiring type widening.

    The repair engine must prove not only that the accumulator requires 64-bit
    width, but that the chosen replacement type is sufficient.
    If max_intermediate_magnitude > LLONG_MAX, repair FAILS CLOSED.
    """
    constraint_n_bound: int
    constraint_value_bound: int
    max_intermediate_magnitude: int
    original_type: str = "int"
    required_type: str = "long long"
    original_identifier: str = ""     # AST symbol being widened
    target_scope: str = ""            # AST scope identifier

    INT32_MAX: int = field(default=2_147_483_647, init=False, repr=False, compare=False)
    INT64_MAX: int = field(default=9_223_372_036_854_775_807, init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "INT32_MAX", 2_147_483_647)
        object.__setattr__(self, "INT64_MAX", 9_223_372_036_854_775_807)

    def is_widening_sufficient(self) -> bool:
        """Proves long long is sufficient for the required range. Must be True before repair."""
        return self.max_intermediate_magnitude <= self.INT64_MAX

    def validate(self) -> bool:
        """Full validation: overflow exists AND long long is sufficient."""
        return (self.max_intermediate_magnitude > self.INT32_MAX
                and self.is_widening_sufficient())


@dataclass(frozen=True)
class IndexMappingEvidence:
    """
    Proven external-1-based to internal-0-based index translation.
    All six structural fields are required. The transformation is deterministic.
    """
    external_base: int = 1
    external_lower_bound: int = 1
    external_upper_bound_var: str = "N"
    internal_base: int = 0
    internal_lower_bound: int = 0
    internal_upper_bound_expr: str = "N - 1"
    offending_expression: str = ""       # e.g. "a[x]"
    translated_expression: str = ""      # e.g. "a[x - 1]"
    target_scope: str = ""               # AST scope containing the expression

    def validate(self) -> bool:
        return (self.offending_expression != ""
                and self.translated_expression != ""
                and self.target_scope != "")


@dataclass(frozen=True)
class BoundaryGuardEvidence:
    """
    Proven algebraic identity for empty-input case.
    proof_reference must reference an existing Phase 5/6 authoritative fact.
    Without a proven identity, no repair is attempted.
    """
    boundary_condition: str       # e.g. "n == 0"
    identity_expression: str      # e.g. "0" (the proven identity value)
    proof_reference: str          # Phase 5/6 fact ID establishing F(∅) = identity
    authoritative_source_layer: str = "PHASE6_DERIVED_FACT"

    def validate(self) -> bool:
        return (self.boundary_condition != ""
                and self.identity_expression != ""
                and self.proof_reference != "")


@dataclass(frozen=True)
class MissingHeaderEvidence:
    """
    Syntactic missing #include requirement.
    Validated via STL_HEADER_REGISTRY + AST symbol presence + compiler diagnostic.
    """
    missing_header: str                      # e.g. "<numeric>"
    required_by_identifier: str              # e.g. "std::accumulate"
    compiler_diagnostic_excerpt: str
    stl_registry_entry_verified: bool = True
    ast_identifier_confirmed: bool = True    # Identifier confirmed present in AST

    def validate(self) -> bool:
        return (self.missing_header != ""
                and self.required_by_identifier != ""
                and self.stl_registry_entry_verified
                and self.ast_identifier_confirmed)


# Type alias for structured evidence union
StructuredEvidence = Union[
    OverflowEvidence,
    IndexMappingEvidence,
    BoundaryGuardEvidence,
    MissingHeaderEvidence,
]


# ---------------------------------------------------------------------------
# Diagnostic Certificate — Deeply Frozen with Full Artifact Binding
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DiagnosticCertificate:
    """
    Immutable diagnostic result with full artifact hash binding.
    All artifact hashes are architectural constraints, not metadata.
    """
    certificate_id: str
    classification_status: ClassificationStatus
    mode: Optional[DiagnosticMode]          # None when UNRESOLVED
    bug_kind: Optional[ImplementationBugKind]
    stage: str

    # Artifact binding hashes (SHA-256)
    problem_hash: str
    requirements_hash: str
    plan_hash: str
    candidate_source_hash: str
    compiler_identity_hash: str
    test_vector_hash: str
    generation_provenance_hash: str

    # Causal evidence (immutable)
    causal_witness: Mapping[str, Any]
    reproducibility_status: ReproducibilityStatus
    reproduction_runs: int

    # Repair authorization
    is_repairable: bool
    recommended_strategy: RepairStrategy
    structured_evidence: Optional[StructuredEvidence]

    # Epistemic provenance
    epistemic_status: str    # "PROVEN" | "SUPPORTED" | "UNRESOLVED"
    unresolved_reason: str = ""

    def fingerprint(self) -> str:
        """SHA-256 fingerprint of all binding fields for downstream verification."""
        fields = {
            "certificate_id": self.certificate_id,
            "problem_hash": self.problem_hash,
            "requirements_hash": self.requirements_hash,
            "plan_hash": self.plan_hash,
            "candidate_source_hash": self.candidate_source_hash,
            "compiler_identity_hash": self.compiler_identity_hash,
            "generation_provenance_hash": self.generation_provenance_hash,
            "mode": self.mode.value if self.mode else None,
            "bug_kind": self.bug_kind.value if self.bug_kind else None,
            "recommended_strategy": self.recommended_strategy.value,
        }
        canonical = json.dumps(fields, sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Self-Correction Plan
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SelfCorrectionPlan:
    """
    Fully structured repair plan emitted by DiagnosticCertificate.
    The repair engine executes this plan deterministically — it cannot
    search for an alternative strategy.
    """
    plan_id: str
    diagnostic_certificate_id: str
    strategy: RepairStrategy
    structured_evidence: StructuredEvidence

    # Repair target (structurally identified, not ad hoc)
    target_symbol: str          # e.g. "sum"
    target_scope: str           # e.g. "solve" function body
    target_line_hint: int = -1  # Optional compiler-reported line, for hint only

    # Artifact binding (must match DiagnosticCertificate)
    candidate_source_hash: str = ""
    plan_hash: str = ""


# ---------------------------------------------------------------------------
# Self-Correction Certificate — Full Provenance Chain
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SelfCorrectionCertificate:
    """
    Immutable result of a successful repair + full verification cycle.
    Exposes the complete evidence chain for Phase 7 explanation.
    """
    certificate_id: str
    diagnostic_certificate_id: str
    repair_plan_id: str

    # Source provenance
    original_source_hash: str
    repaired_source_hash: str

    # Artifact hashes (architectural constraints)
    plan_hash: str
    requirements_hash: str
    compiler_fingerprint: str
    compiler_flags_hash: str
    verification_suite_hash: str
    phase8_suite_hash: str
    historical_suite_hash: str

    # Repair metadata
    attempts_used: int          # Always 1
    applied_strategy: RepairStrategy
    target_symbol: str
    target_scope: str

    # Verification outcome
    verification_passed: bool


# ---------------------------------------------------------------------------
# Unresolved Certificate — fail-closed result
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class UnresolvedCertificate:
    """Emitted when Phase 9 cannot form a confident causal diagnosis."""
    certificate_id: str
    stage: str
    reason: str
    problem_hash: str
    candidate_source_hash: str
    reproducibility_status: ReproducibilityStatus
    harness_status: HarnessStatus
    oracle_status: OracleStatus
