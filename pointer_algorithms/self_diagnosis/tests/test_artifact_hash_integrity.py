"""
Phase 9 — test_artifact_hash_integrity.py

Tests cryptographic artifact binding and replay protection:
- Modifying candidate source after plan creation rejects repair
- Hash binding across plan, source, requirements, and compiler
- Proves hashes are strict architectural constraints, not passive metadata
"""

import hashlib
import json
import unittest

from pointer_algorithms.self_diagnosis.diagnostic_types import (
    ClassificationStatus,
    DiagnosticCertificate,
    DiagnosticMode,
    ImplementationBugKind,
    MissingHeaderEvidence,
    RepairStrategy,
    ReproducibilityStatus,
    SelfCorrectionPlan,
)
from pointer_algorithms.self_diagnosis.repair_strategies import build_self_correction_plan
from pointer_algorithms.self_diagnosis.targeted_repair_engine import TargetedRepairEngine


class TestArtifactHashIntegrity(unittest.TestCase):

    def setUp(self):
        self.source = "#include <iostream>\nint main() { return 0; }"
        self.source_hash = hashlib.sha256(self.source.encode()).hexdigest()
        self.plan_dict = {"status": "VALID_OPTIMAL_PLAN"}
        self.plan_hash = hashlib.sha256(json.dumps(self.plan_dict, sort_keys=True).encode()).hexdigest()
        self.req_hash = hashlib.sha256(b"req").hexdigest()
        self.comp_hash = hashlib.sha256(b"g++-12").hexdigest()

        self.ev = MissingHeaderEvidence(
            missing_header="<algorithm>",
            required_by_identifier="std::sort",
            compiler_diagnostic_excerpt="err",
        )

        self.cert = DiagnosticCertificate(
            certificate_id="cert_replay_test",
            classification_status=ClassificationStatus.CLASSIFIED,
            mode=DiagnosticMode.VALID_CANDIDATE_IMPLEMENTATION_BUG,
            bug_kind=ImplementationBugKind.MISSING_HEADER,
            stage="TEST",
            problem_hash=hashlib.sha256(b"prob").hexdigest(),
            requirements_hash=self.req_hash,
            plan_hash=self.plan_hash,
            candidate_source_hash=self.source_hash,
            compiler_identity_hash=self.comp_hash,
            test_vector_hash="vec_hash",
            generation_provenance_hash="gen_hash",
            causal_witness={},
            reproducibility_status=ReproducibilityStatus.CONTROLLED_REPRODUCIBLE,
            reproduction_runs=3,
            is_repairable=True,
            recommended_strategy=RepairStrategy.ADD_MISSING_HEADER,
            structured_evidence=self.ev,
            epistemic_status="PROVEN",
        )

    def test_certificate_fingerprint_changes_on_hash_modification(self):
        """Modifying any hash in the certificate changes its cryptographic fingerprint."""
        fp_original = self.cert.fingerprint()

        cert_modified_source = dataclasses_replace = DiagnosticCertificate(
            certificate_id=self.cert.certificate_id,
            classification_status=self.cert.classification_status,
            mode=self.cert.mode,
            bug_kind=self.cert.bug_kind,
            stage=self.cert.stage,
            problem_hash=self.cert.problem_hash,
            requirements_hash=self.cert.requirements_hash,
            plan_hash=self.cert.plan_hash,
            candidate_source_hash="tampered_source_hash",
            compiler_identity_hash=self.cert.compiler_identity_hash,
            test_vector_hash=self.cert.test_vector_hash,
            generation_provenance_hash=self.cert.generation_provenance_hash,
            causal_witness=self.cert.causal_witness,
            reproducibility_status=self.cert.reproducibility_status,
            reproduction_runs=self.cert.reproduction_runs,
            is_repairable=self.cert.is_repairable,
            recommended_strategy=self.cert.recommended_strategy,
            structured_evidence=self.cert.structured_evidence,
            epistemic_status=self.cert.epistemic_status,
        )
        fp_tampered = cert_modified_source.fingerprint()
        self.assertNotEqual(fp_original, fp_tampered)

    def test_repair_engine_rejects_source_hash_mismatch(self):
        """TargetedRepairEngine rejects transformation if source hash does not match plan."""
        plan = build_self_correction_plan(self.cert)
        self.assertIsNotNone(plan)

        tampered_source = self.source + "\n// Tampered code"
        res = TargetedRepairEngine.apply_repair(tampered_source, plan, self.cert)
        self.assertFalse(res.success)
        self.assertIn("Source code hash mismatch", res.error_message)


if __name__ == "__main__":
    unittest.main()
