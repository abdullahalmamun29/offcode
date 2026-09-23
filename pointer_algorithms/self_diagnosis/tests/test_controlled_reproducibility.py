"""
Phase 9 — test_controlled_reproducibility.py

Tests controlled reproducibility evaluation:
- reproduction_runs >= 3 required
- Identical failure signatures under controlled envelope required
- Non-reproducible / divergent runs map to UNRESOLVED (fail closed)
"""

import hashlib
import json
import unittest

from pointer_algorithms.self_diagnosis.causal_analyzer import CausalAnalyzer
from pointer_algorithms.self_diagnosis.diagnostic_types import (
    ClassificationStatus,
    ReproducibilityStatus,
)
from pointer_algorithms.self_diagnosis.failure_classifier import DeterministicFailureClassifier
from pointer_algorithms.self_diagnosis.failure_evidence import FailureEvidence
from pointer_algorithms.self_diagnosis.generation_provenance import GenerationProvenance
from pointer_algorithms.self_diagnosis.oracle_integrity import OracleExecutionEvidence


class TestControlledReproducibility(unittest.TestCase):

    def setUp(self):
        self.source = "int main() { return 1; }"
        self.source_hash = hashlib.sha256(self.source.encode()).hexdigest()
        self.comp_hash = hashlib.sha256(b"g++-12").hexdigest()
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
            "compiler_hash": self.comp_hash,
            "flags": ["-O3"],
            "input_hash": "vec_01",
        }
        self.healthy_oracle = [
            OracleExecutionEvidence(exit_code=0, stdout="OK", stderr="", crashed=False)
        ]

    def _make_evidence(self, exit_code=1, stderr="error", signal=None, stdout="out"):
        return FailureEvidence(
            candidate_source_hash=self.source_hash,
            test_vector_hash="vec_01",
            compiler_identity_hash=self.comp_hash,
            compiler_flags=("-O3",),
            exit_code=exit_code,
            signal_received=signal,
            stdout_hash=hashlib.sha256(stdout.encode()).hexdigest(),
            stderr_hash=hashlib.sha256(stderr.encode()).hexdigest(),
            stderr_excerpt=stderr,
            wall_time_ms=10.0,
            peak_rss_kb=1024,
            compiler_diagnostic_lines=(stderr,),
            execution_timestamp_utc="2026-09-23T10:00:00Z",
        )

    def test_reproducibility_requires_at_least_three_runs(self):
        """Fewer than 3 runs produces UNVERIFIED and maps to UNRESOLVED."""
        runs_two = [self._make_evidence() for _ in range(2)]
        rep = CausalAnalyzer.evaluate_controlled_reproducibility(runs_two, self.envelope)
        self.assertEqual(rep.status, ReproducibilityStatus.UNVERIFIED)
        self.assertFalse(rep.is_controlled_reproducible())

        cert = DeterministicFailureClassifier.classify(
            problem_id="prob_01",
            requirements_hash="req",
            phase5_plan=self.plan,
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=self.prov,
            evidence_runs=runs_two,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=self.envelope,
        )
        self.assertEqual(cert.classification_status, ClassificationStatus.UNRESOLVED)
        self.assertIsNone(cert.mode)
        self.assertIn("Insufficient runs", cert.unresolved_reason)

    def test_divergent_runs_produce_not_reproducible(self):
        """Runs with divergent exits/outputs produce NOT_REPRODUCIBLE and map to UNRESOLVED."""
        run1 = self._make_evidence(exit_code=1, stderr="Error A")
        run2 = self._make_evidence(exit_code=1, stderr="Error B")
        run3 = self._make_evidence(exit_code=1, stderr="Error A")
        runs = [run1, run2, run3]

        rep = CausalAnalyzer.evaluate_controlled_reproducibility(runs, self.envelope)
        self.assertEqual(rep.status, ReproducibilityStatus.NOT_REPRODUCIBLE)
        self.assertFalse(rep.is_controlled_reproducible())

        cert = DeterministicFailureClassifier.classify(
            problem_id="prob_01",
            requirements_hash="req",
            phase5_plan=self.plan,
            candidate_source=self.source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=self.prov,
            evidence_runs=runs,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=self.envelope,
        )
        self.assertEqual(cert.classification_status, ClassificationStatus.UNRESOLVED)
        self.assertIsNone(cert.mode)
        self.assertIn("Controlled reproducibility failed", cert.unresolved_reason)

    def test_identical_three_runs_confirm_controlled_reproducibility(self):
        """3 identical runs confirm CONTROLLED_REPRODUCIBLE."""
        runs = [self._make_evidence(exit_code=1, stderr="Identical error") for _ in range(3)]
        rep = CausalAnalyzer.evaluate_controlled_reproducibility(runs, self.envelope)
        self.assertEqual(rep.status, ReproducibilityStatus.CONTROLLED_REPRODUCIBLE)
        self.assertTrue(rep.is_controlled_reproducible())


if __name__ == "__main__":
    unittest.main()
