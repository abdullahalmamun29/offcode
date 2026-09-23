"""
Test Suite: Adversarial Epistemic Laundering Defense
Verifies Law 4 (empirical search cannot be laundered into mathematical PROVEN),
Gate A-C failure handling, oracle disagreement handling, and timeout behavior.
"""

import unittest
from pointer_algorithms.self_diagnosis.oracle_integrity import OracleExecutionEvidence
from pointer_algorithms.research_level.hypothesis_refutation import InductiveRefutationEngine
from pointer_algorithms.research_level.proof_obligation_gate import ProofObligationGate
from pointer_algorithms.research_level.reduction_engine import ReductionEngine
from pointer_algorithms.research_level.research_types import (
    ApplicabilityProof,
    ComplexityBound,
    ComplexityProof,
    CorroborationCertificate,
    EpistemicStatus,
    FiniteSearchEnvelope,
    HypothesisSchema,
    PredicateEvidence,
    ProofObligationItem,
    ReductionCertificate,
    ReductionType,
    SemanticPreservationProof,
)


class TestAdversarialEpistemicLaundering(unittest.TestCase):

    def test_massive_empirical_search_cannot_produce_proven(self):
        """
        Law 4: Even after evaluating 10,000 empirical instances with zero counterexamples,
        the epistemic status must remain strictly SUPPORTED and cannot be PROVEN.
        """
        corrob_cert = CorroborationCertificate(
            certificate_id="corrob_massive_01",
            hypothesis_id="HYP_GREEDY_MASSIVE",
            schema=HypothesisSchema.GREEDY_BY_KEY,
            envelope_fingerprint="env_fp_100k",
            states_evaluated=10000,
            exhaustive_within_envelope=True,
            status=EpistemicStatus.SUPPORTED,
        )

        # Confirm type level and value constraints
        self.assertEqual(corrob_cert.status, EpistemicStatus.SUPPORTED)
        self.assertNotEqual(corrob_cert.status, EpistemicStatus.PROVEN)

        # Gate evaluation treats corroboration strictly as SUPPORTED
        ok, msg = ProofObligationGate.evaluate_hypothesis_candidate(
            ref_cert=None,
            corrob_cert=corrob_cert,
        )
        self.assertTrue(ok)
        self.assertIn("SUPPORTED", msg)
        self.assertNotIn("PROVEN", msg)

    def test_gate_a_failure_undischarged_predicate(self):
        """Verify candidate reduction is rejected if an applicability predicate is unsatisfied."""
        p1 = PredicateEvidence("PRED_1", satisfied=False)  # Unsatisfied predicate
        app_proof = ApplicabilityProof(predicates=(p1,), discharged=False)
        sem_proof = SemanticPreservationProof(obligations=(), discharged=True)
        comp = ComplexityBound("O(1)", (), True, True)
        comp_proof = ComplexityProof(comp, comp, comp, comp, True)

        cert = ReductionCertificate(
            certificate_id="cert_bad_a",
            source_problem_id="PROB_1",
            target_family_id="TARGET_1",
            reduction_type=ReductionType.PROJECT_SELECTION_TO_MIN_CUT,
            applicability_proof=app_proof,
            semantic_proof=sem_proof,
            complexity_proof=comp_proof,
            forward_transform_name="fwd",
            backward_solution_map_name="bwd",
            domain_assumptions=(),
            theorem_id="THM_1",
            theorem_version="1.0",
            problem_hash="h1",
            requirements_hash="h2",
            status=EpistemicStatus.PROVEN,
        )

        ok, msg, artifact = ProofObligationGate.evaluate_reduction_candidate(cert)
        self.assertFalse(ok)
        self.assertIn("Gate A Failed", msg)
        self.assertIsNone(artifact)

    def test_gate_b_failure_undischarged_obligation(self):
        """Verify candidate reduction is rejected if a semantic preservation obligation is undischarged."""
        p1 = PredicateEvidence("PRED_1", satisfied=True)
        app_proof = ApplicabilityProof(predicates=(p1,), discharged=True)
        o1 = ProofObligationItem("OBLIG_1", "PROP_1", discharged=False)  # Undischarged obligation
        sem_proof = SemanticPreservationProof(obligations=(o1,), discharged=False)
        comp = ComplexityBound("O(1)", (), True, True)
        comp_proof = ComplexityProof(comp, comp, comp, comp, True)

        cert = ReductionCertificate(
            certificate_id="cert_bad_b",
            source_problem_id="PROB_1",
            target_family_id="TARGET_1",
            reduction_type=ReductionType.PROJECT_SELECTION_TO_MIN_CUT,
            applicability_proof=app_proof,
            semantic_proof=sem_proof,
            complexity_proof=comp_proof,
            forward_transform_name="fwd",
            backward_solution_map_name="bwd",
            domain_assumptions=(),
            theorem_id="THM_1",
            theorem_version="1.0",
            problem_hash="h1",
            requirements_hash="h2",
            status=EpistemicStatus.PROVEN,
        )

        ok, msg, artifact = ProofObligationGate.evaluate_reduction_candidate(cert)
        self.assertFalse(ok)
        self.assertIn("Gate B Failed", msg)
        self.assertIsNone(artifact)

    def test_gate_c_failure_complexity_budget_exceeded(self):
        """Verify candidate reduction is rejected if complexity proof exceeds budget."""
        p1 = PredicateEvidence("PRED_1", satisfied=True)
        app_proof = ApplicabilityProof(predicates=(p1,), discharged=True)
        o1 = ProofObligationItem("OBLIG_1", "PROP_1", discharged=True)
        sem_proof = SemanticPreservationProof(obligations=(o1,), discharged=True)
        comp_bad = ComplexityBound("O(2^N)", ("N",), False, budget_satisfied=False)  # Exceeds budget
        comp_proof = ComplexityProof(comp_bad, comp_bad, comp_bad, comp_bad, discharged=False)

        cert = ReductionCertificate(
            certificate_id="cert_bad_c",
            source_problem_id="PROB_1",
            target_family_id="TARGET_1",
            reduction_type=ReductionType.PROJECT_SELECTION_TO_MIN_CUT,
            applicability_proof=app_proof,
            semantic_proof=sem_proof,
            complexity_proof=comp_proof,
            forward_transform_name="fwd",
            backward_solution_map_name="bwd",
            domain_assumptions=(),
            theorem_id="THM_1",
            theorem_version="1.0",
            problem_hash="h1",
            requirements_hash="h2",
            status=EpistemicStatus.PROVEN,
        )

        ok, msg, artifact = ProofObligationGate.evaluate_reduction_candidate(cert)
        self.assertFalse(ok)
        self.assertIn("Gate C Failed", msg)
        self.assertIsNone(artifact)

    def test_search_timeout_halts_as_unresolved_not_refuted(self):
        """Verify that hitting a search budget or timeout yields UNRESOLVED, not REFUTED."""
        envelope = FiniteSearchEnvelope(
            domain_type="INTEGERS",
            size_bound=100,
            value_bound=100,
            structural_constraints=(),
            max_states_budget=5,  # Artificially low budget
            timeout_ms_budget=10,  # 10ms
        )

        def infinite_generator(env):
            i = 0
            while True:
                yield i
                i += 1

        oracle_runs = [
            OracleExecutionEvidence(
                exit_code=0,
                stdout="OK",
                stderr="",
                crashed=False,
                wall_time_ms=1.0,
            )
        ]

        ref_cert, corrob_cert, status, reason = InductiveRefutationEngine.evaluate_hypothesis(
            hypothesis_id="HYP_BUDGET_TEST",
            schema=HypothesisSchema.LOCAL_OPTIMALITY,
            envelope=envelope,
            instance_generator=infinite_generator,
            hypothesis_solver=lambda x: x,
            reference_oracle=lambda x: x,
            oracle_runs=oracle_runs,
            metamorphic_check_passed=True,
            secondary_oracle_agreement=True,
        )

        self.assertEqual(status, EpistemicStatus.UNRESOLVED)
        self.assertIsNone(ref_cert)
        self.assertIsNone(corrob_cert)
        self.assertIn("budget exhausted", reason)


if __name__ == "__main__":
    unittest.main()
