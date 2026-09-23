"""
CHUP Phase 8 — Adversarial Generalization & Robustness Engine.

Audits CHUP's reasoning resilience against surface traps, distractor lore,
and syntactic rewordings without altering frozen Phase 1–7 reasoning laws.
"""

from pointer_algorithms.adversarial_generalization.certified_fixtures import (
    CanonicalFact,
    CanonicalSemanticModel,
    SemanticMutation,
    ExpectedElimination,
    SymbolicBudgetSpec,
    DistractorSpec,
    CertifiedFixture,
    FixtureValidator,
    CertifiedFixtureRegistry
)
from pointer_algorithms.adversarial_generalization.keyword_trap_registry import (
    KeywordTrap,
    KeywordTrapRegistry
)
from pointer_algorithms.adversarial_generalization.relevance_discriminator import (
    RelevanceDiscriminator,
    DistractorAuditResult
)
from pointer_algorithms.adversarial_generalization.symbolic_boundary_evaluator import (
    SymbolicBoundaryEvaluator,
    BoundaryAuditResult
)
from pointer_algorithms.adversarial_generalization.adversarial_comparator import (
    AdversarialComparator,
    InvarianceComparisonResult,
    SeparationComparisonResult,
    EliminationComparisonResult
)

__all__ = [
    "CanonicalFact",
    "CanonicalSemanticModel",
    "SemanticMutation",
    "ExpectedElimination",
    "SymbolicBudgetSpec",
    "DistractorSpec",
    "CertifiedFixture",
    "FixtureValidator",
    "CertifiedFixtureRegistry",
    "KeywordTrap",
    "KeywordTrapRegistry",
    "RelevanceDiscriminator",
    "DistractorAuditResult",
    "SymbolicBoundaryEvaluator",
    "BoundaryAuditResult",
    "AdversarialComparator",
    "InvarianceComparisonResult",
    "SeparationComparisonResult",
    "EliminationComparisonResult",
]
