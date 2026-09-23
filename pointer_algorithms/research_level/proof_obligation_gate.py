"""
Phase 10 — proof_obligation_gate.py

Dedicated Phase 10 Proof Obligation Gate.
Enforces Gates A–E before any research-level artifact is admitted
into Phase 5 authoritative multi-constraint planning.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Tuple

from .research_types import (
    ApplicabilityProof,
    ComplexityProof,
    CorroborationCertificate,
    EpistemicStatus,
    ReductionCertificate,
    RefutationCertificate,
    SemanticPreservationProof,
)


@dataclass(frozen=True)
class ResearchCandidateArtifact:
    artifact_id: str
    problem_id: str
    target_solver_id: str
    reduction_certificate: Optional[ReductionCertificate]
    corroboration_certificate: Optional[CorroborationCertificate]
    refutation_certificate: Optional[RefutationCertificate]
    provenance_hash: str
    is_sealed: bool


class ProofObligationGate:
    """
    Validates research candidates against the 5 proof gates.
    """

    @classmethod
    def evaluate_reduction_candidate(
        cls,
        reduction_cert: ReductionCertificate,
    ) -> Tuple[bool, Optional[str], Optional[ResearchCandidateArtifact]]:
        """
        Evaluates a candidate reduction against Gates A, B, and C.
        """
        # Gate A: ApplicabilityProof
        if not reduction_cert.applicability_proof.validate():
            return False, "Gate A Failed: Applicability proof not discharged or predicates unsatisfied", None

        # Gate B: SemanticPreservationProof
        if not reduction_cert.semantic_proof.validate():
            return False, "Gate B Failed: Semantic preservation obligations not discharged", None

        # Gate C: ComplexityProof
        if not reduction_cert.complexity_proof.validate():
            return False, "Gate C Failed: Complexity bounds exceed computational budget", None

        # Cryptographic Sealing
        fingerprint = reduction_cert.fingerprint()
        artifact = ResearchCandidateArtifact(
            artifact_id=f"art_{reduction_cert.certificate_id}",
            problem_id=reduction_cert.source_problem_id,
            target_solver_id=reduction_cert.target_family_id,
            reduction_certificate=reduction_cert,
            corroboration_certificate=None,
            refutation_certificate=None,
            provenance_hash=fingerprint,
            is_sealed=True,
        )

        return True, "All Research Proof Gates A-C Discharged and Sealed", artifact

    @classmethod
    def evaluate_hypothesis_candidate(
        cls,
        ref_cert: Optional[RefutationCertificate],
        corrob_cert: Optional[CorroborationCertificate],
    ) -> Tuple[bool, Optional[str]]:
        """
        Evaluates an algorithmic hypothesis candidate:
        - If RefutationCertificate exists: FAIL CLOSED (Law 2).
        - If CorroborationCertificate exists: SUPPORTED within envelope (Law 3).
        - Law 4: Cannot become PROVEN.
        """
        if ref_cert is not None:
            return False, f"Hypothesis definitively REFUTED by witness counterexample {ref_cert.counterexample_witness}."

        if corrob_cert is not None and corrob_cert.exhaustive_within_envelope:
            return True, f"Hypothesis corroborated within envelope across {corrob_cert.states_evaluated} states (SUPPORTED)."

        return False, "Hypothesis has incomplete evidence (UNRESOLVED)."
