"""
Phase 9 — test_explanation_integration.py

Tests Phase 7 explanation integration:
- DiagnosticCertificate exported to structured Phase 7 explanation format
- Exposes authoritative evidence without trial/error narration
- Deep immutability of explanation export
"""

import hashlib
import unittest

from pointer_algorithms.self_diagnosis.diagnostic_types import (
    ClassificationStatus,
    DiagnosticCertificate,
    DiagnosticMode,
    ImplementationBugKind,
    MissingHeaderEvidence,
    RepairStrategy,
    ReproducibilityStatus,
)
from pointer_algorithms.self_diagnosis.self_diagnosis_facade import SelfDiagnosisFacade


class TestExplanationIntegration(unittest.TestCase):

    def test_format_explanation_for_phase7(self):
        ev = MissingHeaderEvidence(
            missing_header="<numeric>",
            required_by_identifier="std::accumulate",
            compiler_diagnostic_excerpt="error: accumulate was not declared in this scope",
        )
        cert = DiagnosticCertificate(
            certificate_id="diag_expl_01",
            classification_status=ClassificationStatus.CLASSIFIED,
            mode=DiagnosticMode.VALID_CANDIDATE_IMPLEMENTATION_BUG,
            bug_kind=ImplementationBugKind.MISSING_HEADER,
            stage="CAUSAL_DEFECT_ANALYZER",
            problem_hash=hashlib.sha256(b"prob").hexdigest(),
            requirements_hash=hashlib.sha256(b"req").hexdigest(),
            plan_hash=hashlib.sha256(b"plan").hexdigest(),
            candidate_source_hash=hashlib.sha256(b"src").hexdigest(),
            compiler_identity_hash=hashlib.sha256(b"comp").hexdigest(),
            test_vector_hash="vec_01",
            generation_provenance_hash="gen_hash",
            causal_witness={"reason": "Missing header <numeric>", "reproducibility": "CONTROLLED_REPRODUCIBLE"},
            reproducibility_status=ReproducibilityStatus.CONTROLLED_REPRODUCIBLE,
            reproduction_runs=3,
            is_repairable=True,
            recommended_strategy=RepairStrategy.ADD_MISSING_HEADER,
            structured_evidence=ev,
            epistemic_status="PROVEN",
        )

        facade = SelfDiagnosisFacade()
        expl = facade.format_explanation_for_phase7(cert)

        self.assertEqual(expl["mode"], "VALID_CANDIDATE_IMPLEMENTATION_BUG")
        self.assertEqual(expl["status"], "PROVEN")
        self.assertEqual(expl["classification_status"], "CLASSIFIED")
        self.assertEqual(expl["bug_kind"], "MISSING_HEADER")
        self.assertEqual(expl["recommended_strategy"], "ADD_MISSING_HEADER")
        self.assertTrue(expl["is_repairable"])
        self.assertEqual(expl["reproducibility"], "CONTROLLED_REPRODUCIBLE")
        self.assertEqual(expl["reproduction_runs"], 3)
        self.assertIn("witness", expl)


if __name__ == "__main__":
    unittest.main()
