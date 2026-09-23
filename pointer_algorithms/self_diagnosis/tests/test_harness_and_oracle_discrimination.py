"""
Phase 9 — test_harness_and_oracle_discrimination.py

Tests harness defect isolation, oracle defect isolation,
and crucial distinctions:
- Metamorphic inconsistency -> UNRESOLVED (not ORACLE_DEFECT)
- SIGSEGV alone without causal proof -> UNRESOLVED
- Secondary oracle disagreement -> UNRESOLVED
"""

import hashlib
import json
import unittest

from pointer_algorithms.self_diagnosis.diagnostic_types import (
    ClassificationStatus,
    DiagnosticMode,
    OracleStatus,
    ReproducibilityStatus,
)
from pointer_algorithms.self_diagnosis.failure_classifier import DeterministicFailureClassifier
from pointer_algorithms.self_diagnosis.failure_evidence import FailureEvidence
from pointer_algorithms.self_diagnosis.generation_provenance import GenerationProvenance
from pointer_algorithms.self_diagnosis.oracle_integrity import OracleExecutionEvidence


class TestHarnessAndOracleDiscrimination(unittest.TestCase):

    def setUp(self):
        self.problem_id = "infra_prob_01"
        self.source = "int main() { return 0; }"
        self.source_hash = hashlib.sha256(self.source.encode()).hexdigest()
        self.plan = {"status": "VALID_OPTIMAL_PLAN", "constraints": {"N_max": 1000}}
        self.plan_hash = hashlib.sha256(json.dumps(self.plan, sort_keys=True).encode()).hexdigest()
        self.req_hash = hashlib.sha256(b"req").hexdigest()
        self.comp_hash = hashlib.sha256(b"g++-12").hexdigest()

        self.provenance = GenerationProvenance(
            plan_hash=self.plan_hash,
            candidate_source_hash=self.source_hash,
            generator_version="test-gen-1.0",
            generation_timestamp_utc="2026-09-23T10:00:00Z",
            generation_contract_hash=hashlib.sha256(b"contract").hexdigest(),
        )

        self.envelope = {
            "source_hash": self.source_hash,
            "compiler_hash": self.comp_hash,
            "flags": ["-O3"],
            "input_hash": "vec_01",
        }

        self.healthy_oracle = [
            OracleExecutionEvidence(exit_code=0, stdout="42", stderr="", crashed=False),
            OracleExecutionEvidence(exit_code=0, stdout="42", stderr="", crashed=False),
            OracleExecutionEvidence(exit_code=0, stdout="42", stderr="", crashed=False),
        ]

    def _make_evidence(self, exit_code=1, stderr="error", signal=None):
        return FailureEvidence(
            candidate_source_hash=self.source_hash,
            test_vector_hash="vec_01",
            compiler_identity_hash=self.comp_hash,
            compiler_flags=("-O3",),
            exit_code=exit_code,
            signal_received=signal,
            stdout_hash="out",
            stderr_hash=hashlib.sha256(stderr.encode()).hexdigest(),
            stderr_excerpt=stderr,
            wall_time_ms=10.0,
            peak_rss_kb=1024,
            compiler_diagnostic_lines=(stderr,),
            execution_timestamp_utc="2026-09-23T10:00:00Z",
        )

    def test_compiler_ice_is_isolated_as_test_harness_defect(self):
        """Internal compiler error is classified as TEST_HARNESS_DEFECT."""
        ev = [self._make_evidence(exit_code=1, stderr="internal compiler error: in emit_move_insn") for _ in range(3)]
        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=self.plan,
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=self.provenance,
            evidence_runs=ev,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=self.envelope,
        )
        self.assertEqual(cert.mode, DiagnosticMode.TEST_HARNESS_DEFECT)
        self.assertEqual(cert.classification_status, ClassificationStatus.CLASSIFIED)
        self.assertFalse(cert.is_repairable)

    def test_oracle_crash_is_isolated_as_oracle_defect(self):
        """Oracle crash (exit code 139) is classified as ORACLE_DEFECT."""
        ev = [self._make_evidence(exit_code=0, stderr="") for _ in range(3)]
        oracle_crashed = [
            OracleExecutionEvidence(exit_code=139, stdout="", stderr="SIGSEGV", crashed=True),
            OracleExecutionEvidence(exit_code=139, stdout="", stderr="SIGSEGV", crashed=True),
            OracleExecutionEvidence(exit_code=139, stdout="", stderr="SIGSEGV", crashed=True),
        ]
        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=self.plan,
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=self.provenance,
            evidence_runs=ev,
            oracle_runs=oracle_crashed,
            controlled_envelope=self.envelope,
        )
        self.assertEqual(cert.mode, DiagnosticMode.ORACLE_DEFECT)
        self.assertEqual(cert.classification_status, ClassificationStatus.CLASSIFIED)
        self.assertFalse(cert.is_repairable)

    def test_oracle_metamorphic_inconsistency_maps_to_unresolved(self):
        """
        Metamorphic violation does NOT prove oracle is defective;
        it proves INCONSISTENCY, which maps to UNRESOLVED (anti-guessing principle).
        """
        ev = [self._make_evidence(exit_code=1, stderr="Wrong answer") for _ in range(3)]
        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=self.plan,
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=self.provenance,
            evidence_runs=ev,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=self.envelope,
            metamorphic_check_passed=False,  # Metamorphic relation failed
        )
        self.assertEqual(cert.classification_status, ClassificationStatus.UNRESOLVED)
        self.assertIsNone(cert.mode)
        self.assertIn("Metamorphic consistency property violated", cert.unresolved_reason)
        self.assertFalse(cert.is_repairable)

    def test_oracle_consensus_disagreement_maps_to_unresolved(self):
        """Secondary oracle disagreement maps to UNRESOLVED."""
        ev = [self._make_evidence(exit_code=1, stderr="Wrong answer") for _ in range(3)]
        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=self.plan,
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=self.provenance,
            evidence_runs=ev,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=self.envelope,
            secondary_oracle_agreement=False,
        )
        self.assertEqual(cert.classification_status, ClassificationStatus.UNRESOLVED)
        self.assertIsNone(cert.mode)
        self.assertIn("Disagreement between primary and secondary reference oracles", cert.unresolved_reason)
        self.assertFalse(cert.is_repairable)

    def test_sigsegv_without_causal_evidence_is_unresolved(self):
        """SIGSEGV alone is an execution signal, not an implementation diagnosis."""
        sigsegv_ev = [
            self._make_evidence(exit_code=139, stderr="Segmentation fault", signal=11)
            for _ in range(3)
        ]
        # No phase6 indexing/overflow/boundary facts provided
        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=self.plan,
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=self.provenance,
            evidence_runs=sigsegv_ev,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=self.envelope,
            phase6_facts=(),  # No causal facts
        )
        # It's an unclassified code defect -> not repairable, epistemic status SUPPORTED/UNRESOLVED
        self.assertEqual(cert.mode, DiagnosticMode.VALID_CANDIDATE_IMPLEMENTATION_BUG)
        self.assertFalse(cert.is_repairable)
        self.assertIn("does not match any certified deterministic repair pattern", cert.unresolved_reason)


if __name__ == "__main__":
    unittest.main()
