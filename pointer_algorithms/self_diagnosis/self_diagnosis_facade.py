"""
Phase 9 — self_diagnosis_facade.py

Master facade for Phase 9 Self-Diagnosis and Self-Correction.
Exposes the end-to-end workflow:
1. Classify failure via deterministic 7-tier decision table.
2. If repairable and authorized, generate SelfCorrectionPlan.
3. Apply structural, non-search repair via TargetedRepairEngine.
4. Verify repaired candidate via RepairVerifier (4-tier battery + -Werror).
5. Output immutable certificates and structured evidence for Phase 7 explanation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping, Optional, Sequence, Tuple

from .certificate_store import ProblemCertificateStore
from .diagnostic_types import (
    DiagnosticCertificate,
    RepairStrategy,
    SelfCorrectionCertificate,
    SelfCorrectionPlan,
)
from .failure_classifier import DeterministicFailureClassifier
from .failure_evidence import FailureEvidence
from .generation_provenance import GenerationProvenance
from .oracle_integrity import OracleExecutionEvidence
from .repair_strategies import build_self_correction_plan
from .repair_verifier import RepairVerifier, VerificationBatteryResult
from .targeted_repair_engine import RepairResult, TargetedRepairEngine


@dataclass(frozen=True)
class SelfDiagnosisRunResult:
    diagnostic_certificate: DiagnosticCertificate
    self_correction_plan: Optional[SelfCorrectionPlan] = None
    repair_result: Optional[RepairResult] = None
    verification_result: Optional[VerificationBatteryResult] = None
    self_correction_certificate: Optional[SelfCorrectionCertificate] = None
    final_source: str = ""
    repaired: bool = False


class SelfDiagnosisFacade:
    """
    Main orchestration entry point for Phase 9.
    Enforces the single-shot repair bound and restores original source on any failure.
    """

    def __init__(self, store: Optional[ProblemCertificateStore] = None) -> None:
        self.store = store or ProblemCertificateStore()

    def run(
        self,
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
        compiler_path: str = "g++",
        compiler_flags: Tuple[str, ...] = RepairVerifier.DEFAULT_COMPILER_FLAGS,
        witness_runner: Optional[Callable[[str], bool]] = None,
        candidate_suite_runner: Optional[Callable[[str], bool]] = None,
        phase8_suite_runner: Optional[Callable[[str], bool]] = None,
        historical_suite_runner: Optional[Callable[[], bool]] = None,
    ) -> SelfDiagnosisRunResult:
        # 1. Deterministic failure classification
        diag_cert = DeterministicFailureClassifier.classify(
            problem_id=problem_id,
            requirements_hash=requirements_hash,
            phase5_plan=phase5_plan,
            candidate_source=candidate_source,
            compiler_identity_hash=compiler_identity_hash,
            generation_provenance=generation_provenance,
            evidence_runs=evidence_runs,
            oracle_runs=oracle_runs,
            controlled_envelope=controlled_envelope,
            phase6_facts=phase6_facts,
            ast_context=ast_context,
            metamorphic_check_passed=metamorphic_check_passed,
            secondary_oracle_agreement=secondary_oracle_agreement,
        )

        self.store.store_diagnostic_certificate(diag_cert)

        # 2. Check if repairable
        if not diag_cert.is_repairable:
            return SelfDiagnosisRunResult(
                diagnostic_certificate=diag_cert,
                final_source=candidate_source,
                repaired=False,
            )

        # 3. Build SelfCorrectionPlan
        plan = build_self_correction_plan(diag_cert)
        if plan is None:
            return SelfDiagnosisRunResult(
                diagnostic_certificate=diag_cert,
                final_source=candidate_source,
                repaired=False,
            )

        # 4. Apply Single-Shot Targeted Repair
        repair_res = TargetedRepairEngine.apply_repair(
            source_code=candidate_source,
            plan=plan,
            certificate=diag_cert,
        )

        if not repair_res.success:
            return SelfDiagnosisRunResult(
                diagnostic_certificate=diag_cert,
                self_correction_plan=plan,
                repair_result=repair_res,
                final_source=candidate_source,  # Restore original
                repaired=False,
            )

        # 5. Full Verification Battery
        verif_res = RepairVerifier.verify_repaired_source(
            original_source=candidate_source,
            repaired_source=repair_res.repaired_source,
            plan=plan,
            certificate=diag_cert,
            compiler_path=compiler_path,
            compiler_flags=compiler_flags,
            witness_runner=witness_runner,
            candidate_suite_runner=candidate_suite_runner,
            phase8_suite_runner=phase8_suite_runner,
            historical_suite_runner=historical_suite_runner,
        )

        if not verif_res.passed:
            # Verification failed! Restore original source and fail closed
            return SelfDiagnosisRunResult(
                diagnostic_certificate=diag_cert,
                self_correction_plan=plan,
                repair_result=repair_res,
                verification_result=verif_res,
                final_source=candidate_source,  # Restore original
                repaired=False,
            )

        # Successful repair! Store certificate
        corr_cert = verif_res.certificate
        if corr_cert:
            self.store.store_correction_certificate(corr_cert)

        return SelfDiagnosisRunResult(
            diagnostic_certificate=diag_cert,
            self_correction_plan=plan,
            repair_result=repair_res,
            verification_result=verif_res,
            self_correction_certificate=corr_cert,
            final_source=repair_res.repaired_source,
            repaired=True,
        )

    def format_explanation_for_phase7(self, cert: DiagnosticCertificate) -> Mapping[str, Any]:
        """
        Formats diagnostic certificate into structured evidence format for Phase 7.
        Exposes authoritative evidence without revealing trial/error narration.
        """
        return {
            "mode": cert.mode.value if cert.mode else None,
            "status": cert.epistemic_status,
            "classification_status": cert.classification_status.value,
            "stage": cert.stage,
            "bug_kind": cert.bug_kind.value if cert.bug_kind else None,
            "recommended_strategy": cert.recommended_strategy.value,
            "is_repairable": cert.is_repairable,
            "reproducibility": cert.reproducibility_status.value,
            "reproduction_runs": cert.reproduction_runs,
            "witness": dict(cert.causal_witness),
            "unresolved_reason": cert.unresolved_reason,
        }
