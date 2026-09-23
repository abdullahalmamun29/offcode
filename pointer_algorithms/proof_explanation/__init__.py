"""
CHUP Phase 7 — Proof / Explanation Engine Module.
"""

from pointer_algorithms.proof_explanation.evidence import (
    EvidenceKind,
    EvidenceRef,
    AuthoritativeEvidenceStore
)
from pointer_algorithms.proof_explanation.explanation_model import (
    ClaimType,
    ExplanationLevel,
    EpistemicStatus,
    ExplanationClaim,
    ExplanationClaimBase,
    ProblemUnderstandingClaim,
    ProvenFactClaim,
    DerivationClaim,
    ConstraintClaim,
    CandidateEliminationClaim,
    ComponentSelectionClaim,
    CompositionClaim,
    ResourceClaim,
    ProofObligationClaim,
    CorrectnessClaim,
    FinalStatusClaim,
    ProblemUnderstandingSection,
    ProvenFactsSection,
    DerivationSection,
    ConstraintSection,
    CandidateEliminationSection,
    SelectionSection,
    CompositionSection,
    ResourceSection,
    CorrectnessSection,
    VerificationSummarySection,
    ExplanationDocument
)
from pointer_algorithms.proof_explanation.explanation_builder import ExplanationBuilder
from pointer_algorithms.proof_explanation.explanation_validator import (
    ExplanationValidator,
    ValidationResult
)
from pointer_algorithms.proof_explanation.proof_trace import (
    ProofTraceNavigator,
    ProofTraceStep
)
from pointer_algorithms.proof_explanation.renderers.json_renderer import JsonExplanationRenderer
from pointer_algorithms.proof_explanation.renderers.markdown_renderer import MarkdownExplanationRenderer
from pointer_algorithms.proof_explanation.renderers.text_renderer import TextExplanationRenderer

__all__ = [
    "EvidenceKind",
    "EvidenceRef",
    "AuthoritativeEvidenceStore",
    "ClaimType",
    "ExplanationLevel",
    "EpistemicStatus",
    "ExplanationClaim",
    "ExplanationClaimBase",
    "ProblemUnderstandingClaim",
    "ProvenFactClaim",
    "DerivationClaim",
    "ConstraintClaim",
    "CandidateEliminationClaim",
    "ComponentSelectionClaim",
    "CompositionClaim",
    "ResourceClaim",
    "ProofObligationClaim",
    "CorrectnessClaim",
    "FinalStatusClaim",
    "ProblemUnderstandingSection",
    "ProvenFactsSection",
    "DerivationSection",
    "ConstraintSection",
    "CandidateEliminationSection",
    "SelectionSection",
    "CompositionSection",
    "ResourceSection",
    "CorrectnessSection",
    "VerificationSummarySection",
    "ExplanationDocument",
    "ExplanationBuilder",
    "ExplanationValidator",
    "ValidationResult",
    "ProofTraceNavigator",
    "ProofTraceStep",
    "JsonExplanationRenderer",
    "MarkdownExplanationRenderer",
    "TextExplanationRenderer"
]
