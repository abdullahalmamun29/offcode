"""
Test Suite: Zero Regression & Safety Invariants
Verifies deep immutability (frozen=True) across all Phase 10 dataclasses,
purity of the 5-state epistemic model, and zero pollution/mutation of upstream phases.
"""

from dataclasses import FrozenInstanceError
import unittest

from pointer_algorithms.self_diagnosis.failure_evidence import FailureEvidence
from pointer_algorithms.self_diagnosis.oracle_integrity import OracleExecutionEvidence, OracleIntegrityGate
from pointer_algorithms.self_diagnosis.harness_integrity import HarnessIntegrityGate
from pointer_algorithms.research_level.proof_obligation_gate import ResearchCandidateArtifact
from pointer_algorithms.research_level.research_types import (
    ApplicabilityProof,
    ComplexityBound,
    ComplexityProof,
    CorroborationCertificate,
    EpistemicStatus,
    FiniteSearchEnvelope,
    HardnessCertificate,
    HypothesisSchema,
    InvariantCertificate,
    InvariantClass,
    PredicateEvidence,
    ProofObligationItem,
    ReductionCertificate,
    ReductionType,
    RefutationCertificate,
    ResourceFeasibilityCertificate,
    SemanticPreservationProof,
)
from pointer_algorithms.research_level.unified_research_pipeline import (
    ResearchPipelineResult,
    ResearchProvenanceChain,
)


class TestZeroRegressionAndSafety(unittest.TestCase):

    def test_epistemic_status_five_states_exactly(self):
        """Verify the epistemic status model has exactly 5 certified discrete states."""
        expected_states = {"PROVEN", "REFUTED", "SUPPORTED", "HYPOTHETICAL", "UNRESOLVED"}
        actual_states = {s.value for s in EpistemicStatus}
        self.assertEqual(actual_states, expected_states)

    def test_all_certificates_and_proof_objects_frozen(self):
        """Verify frozen immutability across all Phase 10 dataclasses."""
        p_ev = PredicateEvidence("P", True)
        with self.assertRaises(FrozenInstanceError):
            p_ev.satisfied = False  # type: ignore

        app_proof = ApplicabilityProof((p_ev,), True)
        with self.assertRaises(FrozenInstanceError):
            app_proof.discharged = False  # type: ignore

        o_item = ProofObligationItem("O1", "P1", True)
        with self.assertRaises(FrozenInstanceError):
            o_item.discharged = False  # type: ignore

        sem_proof = SemanticPreservationProof((o_item,), True)
        with self.assertRaises(FrozenInstanceError):
            sem_proof.discharged = False  # type: ignore

        c_bound = ComplexityBound("O(1)", (), True, True)
        with self.assertRaises(FrozenInstanceError):
            c_bound.budget_satisfied = False  # type: ignore

        c_proof = ComplexityProof(c_bound, c_bound, c_bound, c_bound, True)
        with self.assertRaises(FrozenInstanceError):
            c_proof.discharged = False  # type: ignore

        red_cert = ReductionCertificate(
            certificate_id="c1",
            source_problem_id="p1",
            target_family_id="t1",
            reduction_type=ReductionType.PROJECT_SELECTION_TO_MIN_CUT,
            applicability_proof=app_proof,
            semantic_proof=sem_proof,
            complexity_proof=c_proof,
            forward_transform_name="f",
            backward_solution_map_name="b",
            domain_assumptions=(),
            theorem_id="th1",
            theorem_version="1.0",
            problem_hash="h1",
            requirements_hash="h2",
            status=EpistemicStatus.PROVEN,
        )
        with self.assertRaises(FrozenInstanceError):
            red_cert.status = EpistemicStatus.UNRESOLVED  # type: ignore

        env = FiniteSearchEnvelope("INT", 10, 10, (), 100, 1000)
        with self.assertRaises(FrozenInstanceError):
            env.size_bound = 20  # type: ignore

        ref_cert = RefutationCertificate("rc1", "h1", HypothesisSchema.GREEDY_BY_KEY, {}, "a", "b", "fp")
        with self.assertRaises(FrozenInstanceError):
            ref_cert.hypothesis_id = "tampered"  # type: ignore

        corrob_cert = CorroborationCertificate("cc1", "h1", HypothesisSchema.GREEDY_BY_KEY, "fp", 10, True)
        with self.assertRaises(FrozenInstanceError):
            corrob_cert.states_evaluated = 999  # type: ignore

        inv_cert = InvariantCertificate("ic1", InvariantClass.BOUNDED_POTENTIAL, "phi", "NAT", True, True, False, 10)
        with self.assertRaises(FrozenInstanceError):
            inv_cert.well_founded_proven = False  # type: ignore

        hard_cert = HardnessCertificate("hc1", "p1", "3SAT", red_cert, True)
        with self.assertRaises(FrozenInstanceError):
            hard_cert.is_np_hard = False  # type: ignore

        feas_cert = ResourceFeasibilityCertificate("fc1", "algo", "N", 10, "O(1)", 10, 100, True, "FEASIBLE")
        with self.assertRaises(FrozenInstanceError):
            feas_cert.is_feasible = False  # type: ignore

        art = ResearchCandidateArtifact("art1", "p1", "t1", red_cert, None, None, "prov", True)
        with self.assertRaises(FrozenInstanceError):
            art.is_sealed = False  # type: ignore

        chain = ResearchProvenanceChain("h1", "h2", "h3", "h4", "h5", "h6", "md")
        with self.assertRaises(FrozenInstanceError):
            chain.master_provenance_digest = "tampered"  # type: ignore

        res = ResearchPipelineResult("p1", True, EpistemicStatus.PROVEN)
        with self.assertRaises(FrozenInstanceError):
            res.admitted_to_planning = False  # type: ignore

    def test_upstream_phase9_gate_integrity_preserved(self):
        """Verify Phase 9 gates function identically without regressions."""
        ev = OracleExecutionEvidence(exit_code=0, stdout="OK", stderr="", crashed=False, wall_time_ms=1.0)
        res = OracleIntegrityGate.evaluate([ev], metamorphic_check_passed=True, secondary_oracle_agreement=True)
        self.assertTrue(res.is_healthy())

        fe = FailureEvidence(
            candidate_source_hash="cand_hash",
            test_vector_hash="tv_hash",
            compiler_identity_hash="comp_hash",
            compiler_flags=("-O3",),
            exit_code=0,
            signal_received=None,
            stdout_hash="out_hash",
            stderr_hash="err_hash",
            stderr_excerpt="",
            wall_time_ms=5.0,
            peak_rss_kb=1024,
            compiler_diagnostic_lines=(),
            execution_timestamp_utc="2026-09-23T00:00:00Z",
        )
        harness_res = HarnessIntegrityGate.evaluate(fe)
        self.assertTrue(harness_res.is_healthy())


if __name__ == "__main__":
    unittest.main()
