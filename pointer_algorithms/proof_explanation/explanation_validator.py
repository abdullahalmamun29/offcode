"""
CHUP Phase 7 — Explanation Validator.

Audits an ExplanationDocument against an AuthoritativeEvidenceStore to ensure:
1. Every claim is backed by valid, authoritative evidence references.
2. Epistemic barrier integrity: No hypothetical or unresolved facts are claimed as PROVEN.
3. No second-proof heuristics or subjective algorithm rankings ("best", "optimal algorithm").
4. Fail-closed on missing, broken, or fabricated evidence.
"""

from typing import Tuple, List, Optional
from dataclasses import dataclass
import re

from pointer_algorithms.proof_explanation.evidence import AuthoritativeEvidenceStore
from pointer_algorithms.proof_explanation.explanation_model import (
    ExplanationDocument,
    ExplanationClaim,
    EpistemicStatus,
    ClaimType
)


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: Tuple[str, ...]

    def __bool__(self) -> bool:
        return self.valid


class ExplanationValidator:
    """
    Authoritative auditor of ExplanationDocument instances.
    """

    FORBIDDEN_SUBJECTIVE_PATTERNS = [
        re.compile(r'\b(best\s+algorithm|better\s+than|superior\s+to|worse\s+than)\b', re.IGNORECASE),
        re.compile(r'\b(obviously|clearly|trivially\s+chosen)\b', re.IGNORECASE),
        re.compile(r'\bwe\s+selected\s+.*?because\s+it\s+is\s+the\s+best\b', re.IGNORECASE),
    ]

    @classmethod
    def validate(
        cls,
        doc: ExplanationDocument,
        store: AuthoritativeEvidenceStore
    ) -> ValidationResult:
        errors: List[str] = []

        claims = doc.all_claims()
        if not claims:
            # An empty document with unknown status is invalid unless terminal
            if doc.outcome_state == "UNKNOWN":
                errors.append("Document contains zero claims and has UNKNOWN outcome state.")

        for claim in claims:
            # 1. Mandatory Evidence Rule
            if not claim.evidence_refs:
                errors.append(f"Claim '{claim.claim_id}' ({claim.claim_type.value}) has NO evidence references.")
                continue

            for eref in claim.evidence_refs:
                # 2. Evidence must exist in authoritative store
                if not store.has_evidence(eref.evidence_id):
                    errors.append(
                        f"Claim '{claim.claim_id}' references unknown evidence ID '{eref.evidence_id}'."
                    )
                else:
                    stored_ref = store.get_evidence(eref.evidence_id)
                    # Check kind consistency
                    if stored_ref and stored_ref.kind != eref.kind:
                        errors.append(
                            f"Claim '{claim.claim_id}' evidence kind mismatch: claimed {eref.kind.value}, stored {stored_ref.kind.value}."
                        )

            # 3. Epistemic preservation
            if claim.claim_type == ClaimType.PROVEN_FACT:
                # If claim asserts PROVEN, verify evidence isn't UNRESOLVED/HYPOTHETICAL
                if claim.epistemic_status == EpistemicStatus.PROVEN:
                    for eref in claim.evidence_refs:
                        if "status=HYPOTHETICAL" in eref.summary or "status=UNRESOLVED" in eref.summary:
                            errors.append(
                                f"Epistemic violation: Claim '{claim.claim_id}' claims PROVEN, but evidence '{eref.evidence_id}' is not proven ({eref.summary})."
                            )

            # 4. Forbidden subjective language check
            for pattern in cls.FORBIDDEN_SUBJECTIVE_PATTERNS:
                if pattern.search(claim.text):
                    errors.append(
                        f"Claim '{claim.claim_id}' contains forbidden subjective phrasing: '{claim.text}'."
                    )

        return ValidationResult(
            valid=(len(errors) == 0),
            errors=tuple(errors)
        )
