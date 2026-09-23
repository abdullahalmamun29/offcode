"""
Phase 9 — test_decision_table_all_7_tiers.py

Tests the 7-tier deterministic decision table.
Guarantees strictly decreasing priority evaluation with no cross-tier misclassification.
"""

import hashlib
import json
import unittest

from pointer_algorithms.self_diagnosis.diagnostic_types import (
    ClassificationStatus,
    DiagnosticMode,
    ImplementationBugKind,
    OracleStatus,
    RepairStrategy,
    ReproducibilityStatus,
)
from pointer_algorithms.self_diagnosis.failure_classifier import DeterministicFailureClassifier
from pointer_algorithms.self_diagnosis.failure_evidence import FailureEvidence
from pointer_algorithms.self_diagnosis.generation_provenance import GenerationProvenance
from pointer_algorithms.self_diagnosis.oracle_integrity import OracleExecutionEvidence


class TestDecisionTableAll7Tiers(unittest.TestCase):

    def setUp(self):
        self.problem_id = "test_prob_01"
        self.source = "int main() { return 0; }"
        self.source_hash = hashlib.sha256(self.source.encode()).hexdigest()
        self.plan_dict = {"status": "VALID_OPTIMAL_PLAN", "constraints": {"N_max": 1000}}
        self.plan_hash = hashlib.sha256(json.dumps(self.plan_dict, sort_keys=True).encode()).hexdigest()
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

        # Healthy oracle run
        self.healthy_oracle = [
            OracleExecutionEvidence(exit_code=0, stdout="42", stderr="", crashed=False),
            OracleExecutionEvidence(exit_code=0, stdout="42", stderr="", crashed=False),
            OracleExecutionEvidence(exit_code=0, stdout="42", stderr="", crashed=False),
        ]

    def _make_evidence(self, exit_code=1, stderr="error: test", signal=None):
        return FailureEvidence(
            candidate_source_hash=self.source_hash,
            test_vector_hash="vec_01",
            compiler_identity_hash=self.comp_hash,
            compiler_flags=("-O3",),
            exit_code=exit_code,
            signal_received=signal,
            stdout_hash="stdout_hash",
            stderr_hash=hashlib.sha256(stderr.encode()).hexdigest(),
            stderr_excerpt=stderr,
            wall_time_ms=10.0,
            peak_rss_kb=1024,
            compiler_diagnostic_lines=(stderr,),
            execution_timestamp_utc="2026-09-23T10:00:00Z",
        )

    def test_priority_1_harness_integrity(self):
        """Priority 1: Harness failure beats all other potential diagnoses."""
        harness_evidence = [
            self._make_evidence(exit_code=1, stderr="internal compiler error: Segmentation fault")
            for _ in range(3)
        ]
        # Even if oracle also failed
        oracle_crashed = [OracleExecutionEvidence(exit_code=139, stdout="", stderr="crash", crashed=True)]

        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan={"status": "UNRESOLVED_BY_CURRENT_ONTOLOGY"},
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=self.provenance,
            evidence_runs=harness_evidence,
            oracle_runs=oracle_crashed,
            controlled_envelope=self.envelope,
        )
        self.assertEqual(cert.mode, DiagnosticMode.TEST_HARNESS_DEFECT)
        self.assertEqual(cert.classification_status, ClassificationStatus.CLASSIFIED)
        self.assertFalse(cert.is_repairable)

    def test_priority_2_oracle_integrity(self):
        """Priority 2: Oracle defect confirmed beats planning outcomes."""
        normal_evidence = [self._make_evidence(exit_code=1, stderr="Wrong answer") for _ in range(3)]
        oracle_crashed = [
            OracleExecutionEvidence(exit_code=139, stdout="", stderr="SIGSEGV in oracle", crashed=True),
            OracleExecutionEvidence(exit_code=139, stdout="", stderr="SIGSEGV in oracle", crashed=True),
            OracleExecutionEvidence(exit_code=139, stdout="", stderr="SIGSEGV in oracle", crashed=True),
        ]

        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan={"status": "UNRESOLVED_BY_CURRENT_ONTOLOGY"},
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=self.provenance,
            evidence_runs=normal_evidence,
            oracle_runs=oracle_crashed,
            controlled_envelope=self.envelope,
        )
        self.assertEqual(cert.mode, DiagnosticMode.ORACLE_DEFECT)
        self.assertEqual(cert.classification_status, ClassificationStatus.CLASSIFIED)
        self.assertFalse(cert.is_repairable)

    def test_priority_3_ontology_resolution(self):
        """Priority 3: Ontology gap in plan produces UNKNOWN_FAMILY."""
        normal_evidence = [self._make_evidence(exit_code=1, stderr="WA") for _ in range(3)]
        plan = {"status": "UNRESOLVED_BY_CURRENT_ONTOLOGY", "ontology_gap_reason": "No match"}

        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=plan,
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=self.provenance,
            evidence_runs=normal_evidence,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=self.envelope,
        )
        self.assertEqual(cert.mode, DiagnosticMode.UNKNOWN_FAMILY)
        self.assertEqual(cert.classification_status, ClassificationStatus.CLASSIFIED)
        self.assertFalse(cert.is_repairable)

    def test_priority_4_precondition_satisfiability(self):
        """Priority 4: Contradictory/eliminated constraints produce KNOWN_FAMILY_INVALID_ASSUMPTIONS."""
        normal_evidence = [self._make_evidence(exit_code=1, stderr="WA") for _ in range(3)]
        plan = {"status": "UNSATISFIABLE_CONSTRAINT_SET", "conflict_details": "Contradiction in bounds"}

        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=plan,
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=self.provenance,
            evidence_runs=normal_evidence,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=self.envelope,
        )
        self.assertEqual(cert.mode, DiagnosticMode.KNOWN_FAMILY_INVALID_ASSUMPTIONS)
        self.assertEqual(cert.classification_status, ClassificationStatus.CLASSIFIED)
        self.assertFalse(cert.is_repairable)

    def test_priority_5_specification_determinacy(self):
        """Priority 5: Ambiguous spec produces AMBIGUOUS_CANDIDATE_SET."""
        normal_evidence = [self._make_evidence(exit_code=1, stderr="WA") for _ in range(3)]
        plan = {"status": "AMBIGUOUS_SPECIFICATION", "ambiguity_report": "Two candidates tied"}

        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=plan,
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=self.provenance,
            evidence_runs=normal_evidence,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=self.envelope,
        )
        self.assertEqual(cert.mode, DiagnosticMode.AMBIGUOUS_CANDIDATE_SET)
        self.assertEqual(cert.classification_status, ClassificationStatus.CLASSIFIED)
        self.assertFalse(cert.is_repairable)

    def test_priority_6_causal_implementation_bug(self):
        """Priority 6: Valid plan + healthy infra + provenance + certified defect -> VALID_CANDIDATE_IMPLEMENTATION_BUG."""
        source = "#include <iostream>\nint main() { std::accumulate(nullptr, nullptr, 0); return 0; }"
        source_hash = hashlib.sha256(source.encode()).hexdigest()
        prov = GenerationProvenance(
            plan_hash=self.plan_hash,
            candidate_source_hash=source_hash,
            generator_version="test-gen-1.0",
            generation_timestamp_utc="2026-09-23T10:00:00Z",
            generation_contract_hash=hashlib.sha256(b"contract").hexdigest(),
        )
        err = "error: 'accumulate' is not a member of 'std'"
        ev_runs = [
            FailureEvidence(
                candidate_source_hash=source_hash,
                test_vector_hash="vec_01",
                compiler_identity_hash=self.comp_hash,
                compiler_flags=("-O3",),
                exit_code=1,
                signal_received=None,
                stdout_hash="out",
                stderr_hash=hashlib.sha256(err.encode()).hexdigest(),
                stderr_excerpt=err,
                wall_time_ms=10.0,
                peak_rss_kb=1024,
                compiler_diagnostic_lines=(err,),
                execution_timestamp_utc="2026-09-23T10:00:00Z",
            )
            for _ in range(3)
        ]
        envelope = dict(self.envelope)
        envelope["source_hash"] = source_hash

        ast_ctx = {
            "identifiers": ["accumulate", "std::accumulate"],
            "includes": ["<iostream>"],
        }

        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=self.plan_dict,
            candidate_source=source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=prov,
            evidence_runs=ev_runs,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=envelope,
            ast_context=ast_ctx,
        )
        self.assertEqual(cert.mode, DiagnosticMode.VALID_CANDIDATE_IMPLEMENTATION_BUG)
        self.assertEqual(cert.bug_kind, ImplementationBugKind.MISSING_HEADER)
        self.assertEqual(cert.recommended_strategy, RepairStrategy.ADD_MISSING_HEADER)
        self.assertTrue(cert.is_repairable)

    def test_priority_7_unresolved(self):
        """Priority 7: Insufficient evidence produces UNRESOLVED without guessing."""
        normal_evidence = [self._make_evidence(exit_code=1, stderr="Random failure") for _ in range(3)]
        # Unknown status
        plan = {"status": "SOME_UNKNOWN_PLAN_STATUS"}

        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=plan,
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=self.provenance,
            evidence_runs=normal_evidence,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=self.envelope,
        )
        self.assertEqual(cert.classification_status, ClassificationStatus.UNRESOLVED)
        self.assertIsNone(cert.mode)
        self.assertFalse(cert.is_repairable)


if __name__ == "__main__":
    unittest.main()
