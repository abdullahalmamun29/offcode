"""
Phase 9 — test_generation_provenance.py

Tests cryptographic generation provenance binding:
- Provenance must match authoritative plan hash and generated source hash.
- Any discrepancy (external edits, plan mismatch) rejects repair and produces UNRESOLVED.
"""

import hashlib
import json
import unittest

from pointer_algorithms.self_diagnosis.diagnostic_types import ClassificationStatus
from pointer_algorithms.self_diagnosis.failure_classifier import DeterministicFailureClassifier
from pointer_algorithms.self_diagnosis.failure_evidence import FailureEvidence
from pointer_algorithms.self_diagnosis.generation_provenance import (
    GenerationProvenance,
    verify_generation_provenance,
)
from pointer_algorithms.self_diagnosis.oracle_integrity import OracleExecutionEvidence


class TestGenerationProvenance(unittest.TestCase):

    def setUp(self):
        self.source = "int main() { return 0; }"
        self.source_hash = hashlib.sha256(self.source.encode()).hexdigest()
        self.plan = {"status": "VALID_OPTIMAL_PLAN"}
        self.plan_hash = hashlib.sha256(json.dumps(self.plan, sort_keys=True).encode()).hexdigest()
        self.prov = GenerationProvenance(
            plan_hash=self.plan_hash,
            candidate_source_hash=self.source_hash,
            generator_version="gen-1.0",
            generation_timestamp_utc="2026-09-23T10:00:00Z",
            generation_contract_hash="hash",
        )
        self.envelope = {
            "source_hash": self.source_hash,
            "compiler_hash": "comp",
            "flags": ["-O3"],
            "input_hash": "vec_01",
        }
        self.healthy_oracle = [
            OracleExecutionEvidence(exit_code=0, stdout="OK", stderr="", crashed=False)
        ]

    def _make_evidence(self):
        return FailureEvidence(
            candidate_source_hash=self.source_hash,
            test_vector_hash="vec_01",
            compiler_identity_hash="comp",
            compiler_flags=("-O3",),
            exit_code=1,
            signal_received=None,
            stdout_hash="out",
            stderr_hash="err",
            stderr_excerpt="err",
            wall_time_ms=10.0,
            peak_rss_kb=1024,
            compiler_diagnostic_lines=(),
            execution_timestamp_utc="2026-09-23T10:00:00Z",
        )

    def test_direct_provenance_verification(self):
        res = verify_generation_provenance(self.prov, self.plan_hash, self.source_hash)
        self.assertTrue(res.verified)

        res_bad_plan = verify_generation_provenance(self.prov, "bad_plan_hash", self.source_hash)
        self.assertFalse(res_bad_plan.verified)
        self.assertIn("Plan hash mismatch", res_bad_plan.reason)

        res_bad_src = verify_generation_provenance(self.prov, self.plan_hash, "bad_source_hash")
        self.assertFalse(res_bad_src.verified)
        self.assertIn("Source hash mismatch", res_bad_src.reason)

    def test_missing_provenance_rejects_repair(self):
        cert = DeterministicFailureClassifier.classify(
            problem_id="prob_01",
            requirements_hash="req",
            phase5_plan=self.plan,
            candidate_source=self.source,
            compiler_identity_hash="comp",
            generation_provenance=None,
            evidence_runs=[self._make_evidence() for _ in range(3)],
            oracle_runs=self.healthy_oracle,
            controlled_envelope=self.envelope,
        )
        self.assertEqual(cert.classification_status, ClassificationStatus.UNRESOLVED)
        self.assertFalse(cert.is_repairable)
        self.assertIn("Missing generation provenance binding", cert.unresolved_reason)

    def test_modified_source_fails_provenance_and_rejects_repair(self):
        modified_source = self.source + "\n// external modification"
        cert = DeterministicFailureClassifier.classify(
            problem_id="prob_01",
            requirements_hash="req",
            phase5_plan=self.plan,
            candidate_source=modified_source,
            compiler_identity_hash="comp",
            generation_provenance=self.prov,  # recorded original hash
            evidence_runs=[self._make_evidence() for _ in range(3)],
            oracle_runs=self.healthy_oracle,
            controlled_envelope=self.envelope,
        )
        self.assertEqual(cert.classification_status, ClassificationStatus.UNRESOLVED)
        self.assertFalse(cert.is_repairable)
        self.assertIn("Candidate source does not match generation provenance", cert.unresolved_reason)


if __name__ == "__main__":
    unittest.main()
