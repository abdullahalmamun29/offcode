"""
Phase 9 — test_anti_guessing_and_fail_closed.py

Tests the anti-guessing and fail-closed guarantees across all failure scenarios:
- Unknown family: zero retries, zero code generation, zero mutation
- Precondition violation: zero algorithm swapping, fails closed
- Ambiguous specification: zero arbitrary candidate selection, fails closed
- Insufficient evidence: mode is None, status is UNRESOLVED, zero guessing
"""

import hashlib
import json
import unittest

from pointer_algorithms.self_diagnosis.diagnostic_types import (
    ClassificationStatus,
    DiagnosticMode,
    RepairStrategy,
)
from pointer_algorithms.self_diagnosis.failure_classifier import DeterministicFailureClassifier
from pointer_algorithms.self_diagnosis.failure_evidence import FailureEvidence
from pointer_algorithms.self_diagnosis.generation_provenance import GenerationProvenance
from pointer_algorithms.self_diagnosis.oracle_integrity import OracleExecutionEvidence
from pointer_algorithms.self_diagnosis.repair_strategies import build_self_correction_plan
from pointer_algorithms.self_diagnosis.targeted_repair_engine import TargetedRepairEngine


class TestAntiGuessingAndFailClosed(unittest.TestCase):

    def setUp(self):
        self.problem_id = "fail_closed_prob_01"
        self.source = "int main() { return 0; }"
        self.source_hash = hashlib.sha256(self.source.encode()).hexdigest()
        self.req_hash = hashlib.sha256(b"req").hexdigest()
        self.comp_hash = hashlib.sha256(b"g++-12").hexdigest()
        self.healthy_oracle = [
            OracleExecutionEvidence(exit_code=0, stdout="OK", stderr="", crashed=False)
        ]

    def test_unknown_family_fails_closed_with_no_repair_plan(self):
        """Unknown family produces no repair plan and rejects code transformation."""
        plan = {"status": "UNRESOLVED_BY_CURRENT_ONTOLOGY"}
        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=plan,
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=None,
            evidence_runs=(),
            oracle_runs=self.healthy_oracle,
            controlled_envelope={},
        )
        self.assertEqual(cert.mode, DiagnosticMode.UNKNOWN_FAMILY)
        self.assertFalse(cert.is_repairable)
        self.assertEqual(cert.recommended_strategy, RepairStrategy.NONE)

        # Ensure build_self_correction_plan returns None
        repair_plan = build_self_correction_plan(cert)
        self.assertIsNone(repair_plan)

        # Ensure TargetedRepairEngine rejects repair
        self.assertFalse(TargetedRepairEngine.authorize(cert))

    def test_precondition_violation_fails_closed_without_algorithm_swapping(self):
        """Precondition violation fails closed; cannot swap algorithms."""
        plan = {"status": "UNSATISFIABLE_CONSTRAINT_SET", "conflict_details": "Negative cycle detected"}
        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=plan,
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=None,
            evidence_runs=(),
            oracle_runs=self.healthy_oracle,
            controlled_envelope={},
        )
        self.assertEqual(cert.mode, DiagnosticMode.KNOWN_FAMILY_INVALID_ASSUMPTIONS)
        self.assertFalse(cert.is_repairable)
        self.assertIsNone(build_self_correction_plan(cert))
        self.assertFalse(TargetedRepairEngine.authorize(cert))

    def test_ambiguous_specification_fails_closed_without_arbitrary_choice(self):
        """Ambiguous specification fails closed; does not guess among candidates."""
        plan = {"status": "AMBIGUOUS_SPECIFICATION"}
        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=plan,
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=None,
            evidence_runs=(),
            oracle_runs=self.healthy_oracle,
            controlled_envelope={},
        )
        self.assertEqual(cert.mode, DiagnosticMode.AMBIGUOUS_CANDIDATE_SET)
        self.assertFalse(cert.is_repairable)
        self.assertIsNone(build_self_correction_plan(cert))

    def test_unclassified_defect_fails_closed_without_repair(self):
        """Unclassified runtime defect produces no repair plan."""
        plan_dict = {"status": "VALID_OPTIMAL_PLAN"}
        plan_hash = hashlib.sha256(json.dumps(plan_dict, sort_keys=True).encode()).hexdigest()
        prov = GenerationProvenance(
            plan_hash=plan_hash,
            candidate_source_hash=self.source_hash,
            generator_version="test-gen-1.0",
            generation_timestamp_utc="2026-09-23T10:00:00Z",
            generation_contract_hash="hash",
        )
        ev = [
            FailureEvidence(
                candidate_source_hash=self.source_hash,
                test_vector_hash="vec_01",
                compiler_identity_hash=self.comp_hash,
                compiler_flags=("-O3",),
                exit_code=1,
                signal_received=None,
                stdout_hash="out",
                stderr_hash="err",
                stderr_excerpt="Unknown failure mode",
                wall_time_ms=10.0,
                peak_rss_kb=1024,
                compiler_diagnostic_lines=(),
                execution_timestamp_utc="2026-09-23T10:00:00Z",
            )
            for _ in range(3)
        ]
        envelope = {
            "source_hash": self.source_hash,
            "compiler_hash": self.comp_hash,
            "flags": ["-O3"],
            "input_hash": "vec_01",
        }
        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=plan_dict,
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=prov,
            evidence_runs=ev,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=envelope,
        )
        self.assertFalse(cert.is_repairable)
        self.assertIsNone(build_self_correction_plan(cert))
        self.assertFalse(TargetedRepairEngine.authorize(cert))


if __name__ == "__main__":
    unittest.main()
