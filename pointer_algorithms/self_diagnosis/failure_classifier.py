"""
Phase 9 — failure_classifier.py

Deterministic 7-tier failure classification engine.
Evaluates failure evidence strictly in priority order:
1. Harness Integrity -> TEST_HARNESS_DEFECT
2. Oracle Integrity -> ORACLE_DEFECT (only if DEFECT_CONFIRMED; INCONSISTENT -> UNRESOLVED)
3. Ontology Resolution -> UNKNOWN_FAMILY (planning outcome)
4. Precondition Satisfiability -> KNOWN_FAMILY_INVALID_ASSUMPTIONS (planning outcome)
5. Specification Determinacy -> AMBIGUOUS_CANDIDATE_SET (planning outcome)
6. Causal Implementation Defect -> VALID_CANDIDATE_IMPLEMENTATION_BUG (requires provenance, reproducibility, etc.)
7. Insufficient Evidence -> UNRESOLVED (mode = None)
"""

from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any, Mapping, Optional, Sequence, Tuple

from .causal_analyzer import CausalAnalyzer, ControlledReproductionReport
from .diagnostic_types import (
    ClassificationStatus,
    DiagnosticCertificate,
    DiagnosticMode,
    HarnessStatus,
    ImplementationBugKind,
    OracleStatus,
    RepairStrategy,
    ReproducibilityStatus,
    StructuredEvidence,
)
from .failure_evidence import FailureEvidence
from .generation_provenance import GenerationProvenance, verify_generation_provenance
from .harness_integrity import HarnessIntegrityGate, HarnessIntegrityResult
from .oracle_integrity import OracleExecutionEvidence, OracleIntegrityGate, OracleIntegrityResult


class DeterministicFailureClassifier:
    """
    Implements the 7-tier deterministic decision table.
    Ensures zero guesswork and fail-closed operation.
    """

    @classmethod
    def classify(
        cls,
        *,
        problem_id: str,
        requirements_hash: str,
        phase5_plan: Mapping[str, Any],
        candidate_source: str,
        compiler_identity_hash: str,
        generation_provenance: Optional[GenerationProvenance],
        evidence_runs: Sequence[FailureEvidence],
        oracle_runs: Sequence[OracleExecutionEvidence],
        controlled_envelope: Mapping[str, Any],
        phase6_facts: Sequence[Mapping[str, Any]] = (),
        ast_context: Optional[Mapping[str, Any]] = None,
        metamorphic_check_passed: Optional[bool] = None,
        secondary_oracle_agreement: Optional[bool] = None,
    ) -> DiagnosticCertificate:
        cert_id = f"diag_{uuid.uuid4().hex[:12]}"
        ast_ctx = ast_context or {}

        # Basic hashes
        source_bytes = candidate_source.encode("utf-8")
        candidate_source_hash = hashlib.sha256(source_bytes).hexdigest()
        plan_canonical = json.dumps(phase5_plan, sort_keys=True)
        plan_hash = hashlib.sha256(plan_canonical.encode()).hexdigest()
        problem_hash = hashlib.sha256(problem_id.encode()).hexdigest()
        test_vector_hash = evidence_runs[0].test_vector_hash if evidence_runs else ""
        gen_provenance_hash = generation_provenance.fingerprint() if generation_provenance else ""

        # =========================================================================
        # Priority 1: Test Harness Integrity Gate
        # =========================================================================
        first_evidence = evidence_runs[0] if evidence_runs else None
        if first_evidence:
            harness_res = HarnessIntegrityGate.evaluate(first_evidence)
            if not harness_res.is_healthy():
                return DiagnosticCertificate(
                    certificate_id=cert_id,
                    classification_status=ClassificationStatus.CLASSIFIED,
                    mode=DiagnosticMode.TEST_HARNESS_DEFECT,
                    bug_kind=None,
                    stage="HARNESS_INTEGRITY_GATE",
                    problem_hash=problem_hash,
                    requirements_hash=requirements_hash,
                    plan_hash=plan_hash,
                    candidate_source_hash=candidate_source_hash,
                    compiler_identity_hash=compiler_identity_hash,
                    test_vector_hash=test_vector_hash,
                    generation_provenance_hash=gen_provenance_hash,
                    causal_witness={"reason": harness_res.reason, "details": harness_res.defect_details},
                    reproducibility_status=ReproducibilityStatus.UNVERIFIED,
                    reproduction_runs=len(evidence_runs),
                    is_repairable=False,
                    recommended_strategy=RepairStrategy.NONE,
                    structured_evidence=None,
                    epistemic_status="PROVEN",
                    unresolved_reason="",
                )

        # =========================================================================
        # Priority 2: Oracle Integrity Gate (Independent)
        # =========================================================================
        oracle_res = OracleIntegrityGate.evaluate(
            oracle_runs=oracle_runs,
            metamorphic_check_passed=metamorphic_check_passed,
            secondary_oracle_agreement=secondary_oracle_agreement,
        )
        if oracle_res.status == OracleStatus.DEFECT_CONFIRMED:
            return DiagnosticCertificate(
                certificate_id=cert_id,
                classification_status=ClassificationStatus.CLASSIFIED,
                mode=DiagnosticMode.ORACLE_DEFECT,
                bug_kind=None,
                stage="ORACLE_INTEGRITY_GATE",
                problem_hash=problem_hash,
                requirements_hash=requirements_hash,
                plan_hash=plan_hash,
                candidate_source_hash=candidate_source_hash,
                compiler_identity_hash=compiler_identity_hash,
                test_vector_hash=test_vector_hash,
                generation_provenance_hash=gen_provenance_hash,
                causal_witness={"reason": oracle_res.reason, "witness": oracle_res.witness},
                reproducibility_status=ReproducibilityStatus.UNVERIFIED,
                reproduction_runs=len(evidence_runs),
                is_repairable=False,
                recommended_strategy=RepairStrategy.NONE,
                structured_evidence=None,
                epistemic_status="PROVEN",
                unresolved_reason="",
            )
        elif oracle_res.status in (OracleStatus.INCONSISTENT, OracleStatus.UNRESOLVED):
            # Anti-guessing: Metamorphic or consensus inconsistency does NOT prove oracle defect!
            # It maps to UNRESOLVED (Priority 7 fail-closed)
            return DiagnosticCertificate(
                certificate_id=cert_id,
                classification_status=ClassificationStatus.UNRESOLVED,
                mode=None,
                bug_kind=None,
                stage="ORACLE_INTEGRITY_GATE",
                problem_hash=problem_hash,
                requirements_hash=requirements_hash,
                plan_hash=plan_hash,
                candidate_source_hash=candidate_source_hash,
                compiler_identity_hash=compiler_identity_hash,
                test_vector_hash=test_vector_hash,
                generation_provenance_hash=gen_provenance_hash,
                causal_witness={"oracle_status": oracle_res.status.value, "reason": oracle_res.reason},
                reproducibility_status=ReproducibilityStatus.UNVERIFIED,
                reproduction_runs=len(evidence_runs),
                is_repairable=False,
                recommended_strategy=RepairStrategy.NONE,
                structured_evidence=None,
                epistemic_status="UNRESOLVED",
                unresolved_reason=f"Oracle integrity cannot be certified: {oracle_res.reason}",
            )

        # =========================================================================
        # Priority 3: Ontology Resolution (Authoritative Planning Outcome)
        # =========================================================================
        plan_status = phase5_plan.get("status")
        if plan_status == "UNRESOLVED_BY_CURRENT_ONTOLOGY":
            return DiagnosticCertificate(
                certificate_id=cert_id,
                classification_status=ClassificationStatus.CLASSIFIED,
                mode=DiagnosticMode.UNKNOWN_FAMILY,
                bug_kind=None,
                stage="ONTOLOGY_RESOLUTION_GATE",
                problem_hash=problem_hash,
                requirements_hash=requirements_hash,
                plan_hash=plan_hash,
                candidate_source_hash=candidate_source_hash,
                compiler_identity_hash=compiler_identity_hash,
                test_vector_hash=test_vector_hash,
                generation_provenance_hash=gen_provenance_hash,
                causal_witness={"ontology_gap": phase5_plan.get("ontology_gap_reason", "Gap in ontology")},
                reproducibility_status=ReproducibilityStatus.UNVERIFIED,
                reproduction_runs=0,
                is_repairable=False,
                recommended_strategy=RepairStrategy.NONE,
                structured_evidence=None,
                epistemic_status="PROVEN",
                unresolved_reason="",
            )

        # =========================================================================
        # Priority 4: Precondition Satisfiability (Authoritative Planning Outcome)
        # =========================================================================
        if plan_status in ("UNSATISFIABLE_CONSTRAINT_SET", "ELIMINATION_CERTIFICATE"):
            return DiagnosticCertificate(
                certificate_id=cert_id,
                classification_status=ClassificationStatus.CLASSIFIED,
                mode=DiagnosticMode.KNOWN_FAMILY_INVALID_ASSUMPTIONS,
                bug_kind=None,
                stage="PRECONDITION_SATISFIABILITY_GATE",
                problem_hash=problem_hash,
                requirements_hash=requirements_hash,
                plan_hash=plan_hash,
                candidate_source_hash=candidate_source_hash,
                compiler_identity_hash=compiler_identity_hash,
                test_vector_hash=test_vector_hash,
                generation_provenance_hash=gen_provenance_hash,
                causal_witness={"conflict_details": phase5_plan.get("conflict_details", "Contradictory constraints")},
                reproducibility_status=ReproducibilityStatus.UNVERIFIED,
                reproduction_runs=0,
                is_repairable=False,
                recommended_strategy=RepairStrategy.NONE,
                structured_evidence=None,
                epistemic_status="PROVEN",
                unresolved_reason="",
            )

        # =========================================================================
        # Priority 5: Specification Determinacy (Authoritative Planning Outcome)
        # =========================================================================
        if plan_status == "AMBIGUOUS_SPECIFICATION":
            return DiagnosticCertificate(
                certificate_id=cert_id,
                classification_status=ClassificationStatus.CLASSIFIED,
                mode=DiagnosticMode.AMBIGUOUS_CANDIDATE_SET,
                bug_kind=None,
                stage="SPECIFICATION_DETERMINACY_GATE",
                problem_hash=problem_hash,
                requirements_hash=requirements_hash,
                plan_hash=plan_hash,
                candidate_source_hash=candidate_source_hash,
                compiler_identity_hash=compiler_identity_hash,
                test_vector_hash=test_vector_hash,
                generation_provenance_hash=gen_provenance_hash,
                causal_witness={"ambiguity_report": phase5_plan.get("ambiguity_report", "Multiple incompatible candidates")},
                reproducibility_status=ReproducibilityStatus.UNVERIFIED,
                reproduction_runs=0,
                is_repairable=False,
                recommended_strategy=RepairStrategy.NONE,
                structured_evidence=None,
                epistemic_status="PROVEN",
                unresolved_reason="",
            )

        # =========================================================================
        # Priority 6: Causal Implementation Defect Gate
        # =========================================================================
        # Requires:
        # a) plan_status == "VALID_OPTIMAL_PLAN"
        # b) generation provenance matches exactly
        # c) controlled reproducibility confirmed
        # d) causal analyzer matches certified defect pattern
        if plan_status == "VALID_OPTIMAL_PLAN":
            # 6.b Check generation provenance
            if generation_provenance is None:
                return DiagnosticCertificate(
                    certificate_id=cert_id,
                    classification_status=ClassificationStatus.UNRESOLVED,
                    mode=None,
                    bug_kind=None,
                    stage="PROVENANCE_CHECK_GATE",
                    problem_hash=problem_hash,
                    requirements_hash=requirements_hash,
                    plan_hash=plan_hash,
                    candidate_source_hash=candidate_source_hash,
                    compiler_identity_hash=compiler_identity_hash,
                    test_vector_hash=test_vector_hash,
                    generation_provenance_hash="",
                    causal_witness={"provenance_error": "No generation provenance provided"},
                    reproducibility_status=ReproducibilityStatus.UNVERIFIED,
                    reproduction_runs=len(evidence_runs),
                    is_repairable=False,
                    recommended_strategy=RepairStrategy.NONE,
                    structured_evidence=None,
                    epistemic_status="UNRESOLVED",
                    unresolved_reason="Missing generation provenance binding; repair cannot be authorized.",
                )

            prov_res = verify_generation_provenance(
                generation_provenance,
                plan_hash=plan_hash,
                candidate_source_hash=candidate_source_hash,
            )
            if not prov_res.verified:
                return DiagnosticCertificate(
                    certificate_id=cert_id,
                    classification_status=ClassificationStatus.UNRESOLVED,
                    mode=None,
                    bug_kind=None,
                    stage="PROVENANCE_CHECK_GATE",
                    problem_hash=problem_hash,
                    requirements_hash=requirements_hash,
                    plan_hash=plan_hash,
                    candidate_source_hash=candidate_source_hash,
                    compiler_identity_hash=compiler_identity_hash,
                    test_vector_hash=test_vector_hash,
                    generation_provenance_hash=gen_provenance_hash,
                    causal_witness={"provenance_mismatch": prov_res.reason},
                    reproducibility_status=ReproducibilityStatus.UNVERIFIED,
                    reproduction_runs=len(evidence_runs),
                    is_repairable=False,
                    recommended_strategy=RepairStrategy.NONE,
                    structured_evidence=None,
                    epistemic_status="UNRESOLVED",
                    unresolved_reason=f"Candidate source does not match generation provenance: {prov_res.reason}",
                )

            # 6.c Controlled reproducibility check
            repro_rep = CausalAnalyzer.evaluate_controlled_reproducibility(
                evidence_runs,
                controlled_envelope_info=controlled_envelope,
            )
            if not repro_rep.is_controlled_reproducible():
                return DiagnosticCertificate(
                    certificate_id=cert_id,
                    classification_status=ClassificationStatus.UNRESOLVED,
                    mode=None,
                    bug_kind=None,
                    stage="CONTROLLED_REPRODUCIBILITY_GATE",
                    problem_hash=problem_hash,
                    requirements_hash=requirements_hash,
                    plan_hash=plan_hash,
                    candidate_source_hash=candidate_source_hash,
                    compiler_identity_hash=compiler_identity_hash,
                    test_vector_hash=test_vector_hash,
                    generation_provenance_hash=gen_provenance_hash,
                    causal_witness={"reproducibility_report": repro_rep.details},
                    reproducibility_status=repro_rep.status,
                    reproduction_runs=repro_rep.reproduction_runs,
                    is_repairable=False,
                    recommended_strategy=RepairStrategy.NONE,
                    structured_evidence=None,
                    epistemic_status="UNRESOLVED",
                    unresolved_reason=f"Controlled reproducibility failed: {repro_rep.details}",
                )

            # 6.d Causal defect matching
            assert first_evidence is not None
            bug_kind, strategy, struct_ev, reason = CausalAnalyzer.match_certified_defect(
                first_evidence,
                ast_context=ast_ctx,
                phase5_plan=phase5_plan,
                phase6_facts=phase6_facts,
            )

            is_repairable = (
                bug_kind is not None
                and bug_kind != ImplementationBugKind.UNCLASSIFIED_CODE_DEFECT
                and strategy is not None
                and strategy != RepairStrategy.NONE
                and struct_ev is not None
                and struct_ev.validate()
            )

            return DiagnosticCertificate(
                certificate_id=cert_id,
                classification_status=ClassificationStatus.CLASSIFIED,
                mode=DiagnosticMode.VALID_CANDIDATE_IMPLEMENTATION_BUG,
                bug_kind=bug_kind,
                stage="CAUSAL_DEFECT_ANALYZER",
                problem_hash=problem_hash,
                requirements_hash=requirements_hash,
                plan_hash=plan_hash,
                candidate_source_hash=candidate_source_hash,
                compiler_identity_hash=compiler_identity_hash,
                test_vector_hash=test_vector_hash,
                generation_provenance_hash=gen_provenance_hash,
                causal_witness={
                    "reproducibility": repro_rep.status.value,
                    "reason": reason,
                    "bug_kind": bug_kind.value if bug_kind else None,
                },
                reproducibility_status=repro_rep.status,
                reproduction_runs=repro_rep.reproduction_runs,
                is_repairable=is_repairable,
                recommended_strategy=strategy if strategy else RepairStrategy.NONE,
                structured_evidence=struct_ev,
                epistemic_status="PROVEN" if is_repairable else "SUPPORTED",
                unresolved_reason="" if is_repairable else reason,
            )

        # =========================================================================
        # Priority 7: Insufficient Evidence -> UNRESOLVED
        # =========================================================================
        return DiagnosticCertificate(
            certificate_id=cert_id,
            classification_status=ClassificationStatus.UNRESOLVED,
            mode=None,
            bug_kind=None,
            stage="DEFAULT_INSUFFICIENT_EVIDENCE",
            problem_hash=problem_hash,
            requirements_hash=requirements_hash,
            plan_hash=plan_hash,
            candidate_source_hash=candidate_source_hash,
            compiler_identity_hash=compiler_identity_hash,
            test_vector_hash=test_vector_hash,
            generation_provenance_hash=gen_provenance_hash,
            causal_witness={"details": "Failure evidence could not satisfy Priorities 1-6 deterministically."},
            reproducibility_status=ReproducibilityStatus.UNVERIFIED,
            reproduction_runs=len(evidence_runs),
            is_repairable=False,
            recommended_strategy=RepairStrategy.NONE,
            structured_evidence=None,
            epistemic_status="UNRESOLVED",
            unresolved_reason="Insufficient evidence to attribute failure deterministically.",
        )
