"""
Phase 9 — repair_strategies.py

Structured repair strategies and SelfCorrectionPlan builder.
Ensures that a repair plan is strictly constructed from verified structured
evidence in the DiagnosticCertificate, with zero opportunity for the repair
engine to invent or guess an arbitrary strategy.
"""

from __future__ import annotations

import uuid
from typing import Optional

from .diagnostic_types import (
    BoundaryGuardEvidence,
    DiagnosticCertificate,
    ImplementationBugKind,
    IndexMappingEvidence,
    MissingHeaderEvidence,
    OverflowEvidence,
    RepairStrategy,
    SelfCorrectionPlan,
)


def build_self_correction_plan(certificate: DiagnosticCertificate) -> Optional[SelfCorrectionPlan]:
    """
    Builds a SelfCorrectionPlan from a DiagnosticCertificate.
    Returns None if certificate is not repairable or fails authorization.
    """
    if not certificate.is_repairable:
        return None

    if certificate.structured_evidence is None:
        return None

    if not certificate.structured_evidence.validate():
        return None

    strategy = certificate.recommended_strategy
    bug_kind = certificate.bug_kind

    # Validate 1-to-1 correspondence between bug_kind and strategy
    expected_mapping = {
        ImplementationBugKind.MISSING_HEADER: RepairStrategy.ADD_MISSING_HEADER,
        ImplementationBugKind.TYPE_WIDTH_MISMATCH: RepairStrategy.WIDEN_TO_64BIT,
        ImplementationBugKind.CERTIFIED_INDEX_BASE_TRANSLATION: RepairStrategy.ADJUST_INDEX_BASE,
        ImplementationBugKind.CERTIFIED_BOUNDARY_GUARD: RepairStrategy.INSERT_BOUNDARY_GUARD,
    }

    if expected_mapping.get(bug_kind) != strategy:
        # Unauthorized strategy combination
        return None

    target_symbol = ""
    target_scope = ""

    ev = certificate.structured_evidence
    if isinstance(ev, OverflowEvidence):
        target_symbol = ev.original_identifier
        target_scope = ev.target_scope
    elif isinstance(ev, IndexMappingEvidence):
        target_symbol = ev.offending_expression
        target_scope = ev.target_scope
    elif isinstance(ev, BoundaryGuardEvidence):
        target_symbol = ev.boundary_condition
        target_scope = "entry"
    elif isinstance(ev, MissingHeaderEvidence):
        target_symbol = ev.missing_header
        target_scope = "global_includes"

    plan_id = f"plan_{uuid.uuid4().hex[:12]}"
    return SelfCorrectionPlan(
        plan_id=plan_id,
        diagnostic_certificate_id=certificate.certificate_id,
        strategy=strategy,
        structured_evidence=ev,
        target_symbol=target_symbol,
        target_scope=target_scope,
        candidate_source_hash=certificate.candidate_source_hash,
        plan_hash=certificate.plan_hash,
    )
