"""
CHUP Phase 6 — Semantic Fact Model & Epistemic Contracts.

Defines the authoritative 4-tier fact model, discrete proof statuses,
ambiguity classifications, and immutable SemanticFact records.

Core Invariant:
Only facts with tier in (OBSERVED_FACT, DERIVED_FACT, CAPABILITY_CONSEQUENCE),
proof_status == PROVEN, and ambiguity == UNAMBIGUOUS are eligible to modify
the frozen Phase 5 constraint vector. ALGORITHM_HYPOTHESIS is strictly
quarantined and may never become a Phase 5 constraint.
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any, Optional, Tuple, FrozenSet


class FactTier(Enum):
    """
    Authoritative 4-tier classification of semantic entities.
    """
    # Directly and unambiguously stated or represented in the accepted input specification
    OBSERVED_FACT = "OBSERVED_FACT"

    # Mathematically entailed by already proven facts via formal derivation rules
    DERIVED_FACT = "DERIVED_FACT"

    # Mechanically entailed by proven facts conjoined with registered capability contracts
    CAPABILITY_CONSEQUENCE = "CAPABILITY_CONSEQUENCE"

    # Speculative candidate; quarantined, cannot justify elimination or enter Phase 5 constraints
    ALGORITHM_HYPOTHESIS = "ALGORITHM_HYPOTHESIS"


class ProofStatus(Enum):
    """
    Discrete epistemic confidence-free proof status.
    """
    # Formally proved or accepted relative to the specification with valid provenance witness
    PROVEN = "PROVEN"

    # Plausible or partially supported, but formal deduction/witness is incomplete
    SUPPORTED = "SUPPORTED"

    # Conjectured or hypothesized interpretation
    HYPOTHETICAL = "HYPOTHETICAL"

    # Insufficient evidence or conflicting hypotheses leave the fact undetermined
    UNRESOLVED = "UNRESOLVED"


class AmbiguityStatus(Enum):
    """
    Distinguishes unambiguous facts from multi-interpretation or underspecified inputs.
    """
    UNAMBIGUOUS = "UNAMBIGUOUS"
    AMBIGUOUS = "AMBIGUOUS"          # Multiple valid readings exist
    UNDER_SPECIFIED = "UNDER_SPECIFIED"  # Missing essential parameters


@dataclass(frozen=True)
class SemanticFact:
    """
    Immutable semantic fact record.
    Once established and proved, neither the fact value nor its provenance may be mutated.
    """
    fact_id: str
    tier: FactTier
    name: str
    value: Any
    proof_status: ProofStatus = ProofStatus.PROVEN
    ambiguity: AmbiguityStatus = AmbiguityStatus.UNAMBIGUOUS
    provenance_id: Optional[str] = None
    witness: str = ""

    def is_eligible_for_phase5(self) -> bool:
        """
        Determines whether this fact is mathematically qualified to enter
        or modify the frozen Phase 5 MultiConstraintVector.
        """
        return (
            self.tier in (
                FactTier.OBSERVED_FACT,
                FactTier.DERIVED_FACT,
                FactTier.CAPABILITY_CONSEQUENCE
            )
            and self.proof_status == ProofStatus.PROVEN
            and self.ambiguity == AmbiguityStatus.UNAMBIGUOUS
        )

    def is_quarantined_hypothesis(self) -> bool:
        return self.tier == FactTier.ALGORITHM_HYPOTHESIS


@dataclass(frozen=True)
class FactSet:
    """
    Immutable set of semantic facts indexed by name and fact_id.
    """
    facts: Tuple[SemanticFact, ...] = ()

    @classmethod
    def from_iterable(cls, items) -> "FactSet":
        return cls(tuple(items))

    def get(self, name: str) -> Optional[SemanticFact]:
        for f in self.facts:
            if f.name == name:
                return f
        return None

    def get_all(self, name: str) -> Tuple[SemanticFact, ...]:
        return tuple(f for f in self.facts if f.name == name)

    def has_proven(self, name: str, expected_value: Any = None) -> bool:
        for f in self.facts:
            if f.name == name and f.proof_status == ProofStatus.PROVEN and f.ambiguity == AmbiguityStatus.UNAMBIGUOUS:
                if expected_value is None or f.value == expected_value:
                    return True
        return False

    def eligible_facts(self) -> Tuple[SemanticFact, ...]:
        return tuple(f for f in self.facts if f.is_eligible_for_phase5())

    def __iter__(self):
        return iter(self.facts)

    def __len__(self):
        return len(self.facts)
