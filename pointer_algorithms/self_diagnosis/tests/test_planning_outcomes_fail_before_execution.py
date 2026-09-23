"""
Phase 9 — test_planning_outcomes_fail_before_execution.py

Proves that Priorities 3–5 (planning failures: ontology gap, unsatisfied constraints,
ambiguous specification) are authoritative planning outcomes that terminate before
any code generation or candidate execution occurs.
"""

import hashlib
import unittest

from pointer_algorithms.self_diagnosis.diagnostic_types import (
    ClassificationStatus,
    DiagnosticMode,
)
from pointer_algorithms.self_diagnosis.failure_classifier import DeterministicFailureClassifier
from pointer_algorithms.self_diagnosis.oracle_integrity import OracleExecutionEvidence


class TestPlanningOutcomesFailBeforeExecution(unittest.TestCase):

    def setUp(self):
        self.problem_id = "planning_prob_01"
        self.dummy_source = ""  # No candidate generated
        self.req_hash = hashlib.sha256(b"req").hexdigest()
        self.comp_hash = hashlib.sha256(b"g++-12").hexdigest()
        self.healthy_oracle = [
            OracleExecutionEvidence(exit_code=0, stdout="OK", stderr="", crashed=False)
        ]

    def test_ontology_gap_terminates_with_zero_evidence_runs(self):
        """Ontology gap classifies directly without any candidate execution evidence."""
        plan = {
            "status": "UNRESOLVED_BY_CURRENT_ONTOLOGY",
            "ontology_gap_reason": "No supported graph algorithm for 3-SAT reduction",
        }
        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=plan,
            candidate_source=self.dummy_source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=None,  # No generation provenance because no code generated
            evidence_runs=(),            # ZERO execution evidence runs
            oracle_runs=self.healthy_oracle,
            controlled_envelope={},
        )
        self.assertEqual(cert.mode, DiagnosticMode.UNKNOWN_FAMILY)
        self.assertEqual(cert.classification_status, ClassificationStatus.CLASSIFIED)
        self.assertEqual(cert.reproduction_runs, 0)
        self.assertFalse(cert.is_repairable)
        self.assertEqual(cert.stage, "ONTOLOGY_RESOLUTION_GATE")

    def test_unsatisfiable_constraints_terminates_without_generation(self):
        """Unsatisfiable constraints classify directly without execution."""
        plan = {
            "status": "UNSATISFIABLE_CONSTRAINT_SET",
            "conflict_details": "N <= 10^5 but memory limit 1MB precludes table DP",
        }
        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=plan,
            candidate_source=self.dummy_source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=None,
            evidence_runs=(),
            oracle_runs=self.healthy_oracle,
            controlled_envelope={},
        )
        self.assertEqual(cert.mode, DiagnosticMode.KNOWN_FAMILY_INVALID_ASSUMPTIONS)
        self.assertEqual(cert.classification_status, ClassificationStatus.CLASSIFIED)
        self.assertEqual(cert.reproduction_runs, 0)
        self.assertFalse(cert.is_repairable)
        self.assertEqual(cert.stage, "PRECONDITION_SATISFIABILITY_GATE")

    def test_ambiguous_specification_terminates_without_arbitrary_choice(self):
        """Ambiguous specification classifies directly without choosing arbitrary candidate."""
        plan = {
            "status": "AMBIGUOUS_SPECIFICATION",
            "ambiguity_report": "Kruskal vs Prim tied on all metric dimensions",
        }
        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash=self.req_hash,
            phase5_plan=plan,
            candidate_source=self.dummy_source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=None,
            evidence_runs=(),
            oracle_runs=self.healthy_oracle,
            controlled_envelope={},
        )
        self.assertEqual(cert.mode, DiagnosticMode.AMBIGUOUS_CANDIDATE_SET)
        self.assertEqual(cert.classification_status, ClassificationStatus.CLASSIFIED)
        self.assertEqual(cert.reproduction_runs, 0)
        self.assertFalse(cert.is_repairable)
        self.assertEqual(cert.stage, "SPECIFICATION_DETERMINACY_GATE")


if __name__ == "__main__":
    unittest.main()
