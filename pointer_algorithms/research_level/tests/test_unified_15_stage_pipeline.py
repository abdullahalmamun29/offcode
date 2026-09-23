"""
Test Suite: Pillar V — Unified Research-Level Cognitive Pipeline
Verifies orchestration across Pillars I-IV, Gate validation,
admittance to Phase 5 planning, and complete cryptographic provenance chain.
"""

import unittest
from pointer_algorithms.research_level.hardness_boundary import HardnessBoundaryEngine
from pointer_algorithms.research_level.reduction_engine import ReductionEngine
from pointer_algorithms.research_level.research_types import (
    EpistemicStatus,
    HypothesisSchema,
    InvariantCertificate,
    InvariantClass,
    RefutationCertificate,
)
from pointer_algorithms.research_level.unified_research_pipeline import (
    UnifiedResearchPipeline,
)


class TestUnified15StagePipeline(unittest.TestCase):

    def test_pipeline_admits_proven_reduction(self):
        """Verify pipeline successfully admits a proven problem reduction to Phase 5 planning."""
        valid_red = ReductionEngine.reduce_project_selection_to_min_cut(
            problem_id="PROB_CLOSURE_01",
            requirements_hash="req_h_closure",
            projects=[{"id": "A", "profit": 10}, {"id": "B", "profit": -5}],
            dependencies=[("A", "B")],
        )

        res = UnifiedResearchPipeline.execute(
            problem_id="PROB_CLOSURE_01",
            requirements_text="Solve maximum profit closure on directed graph",
            reduction_cert=valid_red,
        )

        self.assertTrue(res.admitted_to_planning)
        self.assertEqual(res.status, EpistemicStatus.PROVEN)
        self.assertIsNotNone(res.provenance_chain)
        self.assertGreater(len(res.provenance_chain.master_provenance_digest), 32)
        self.assertIn("admitted to Phase 5 planning", res.reason)

    def test_pipeline_fails_closed_on_refutation_certificate(self):
        """Verify pipeline immediately rejects candidate when refutation certificate is present (Law 2)."""
        ref_cert = RefutationCertificate(
            certificate_id="ref_witness_01",
            hypothesis_id="HYP_GREEDY_FAIL",
            schema=HypothesisSchema.GREEDY_BY_KEY,
            counterexample_witness={"input": 6},
            hypothesis_output="3",
            oracle_output="2",
            envelope_fingerprint="env_fp_abc",
            status=EpistemicStatus.REFUTED,
        )

        res = UnifiedResearchPipeline.execute(
            problem_id="PROB_COIN_01",
            requirements_text="Coin change problem",
            refutation_cert=ref_cert,
        )

        self.assertFalse(res.admitted_to_planning)
        self.assertEqual(res.status, EpistemicStatus.REFUTED)
        self.assertIn("refuted by counterexample", res.reason)

    def test_pipeline_fails_closed_on_infeasible_parameter(self):
        """Verify pipeline halts with PARAMETER_EXCEEDS_CERTIFIED_FEASIBILITY when budget exceeded (Law 7)."""
        feas_cert = HardnessBoundaryEngine.evaluate_exact_exponential_feasibility(
            algorithm_name="bitmask_dp_tsp",
            parameter_name="N",
            n_val=35,
        )

        res = UnifiedResearchPipeline.execute(
            problem_id="PROB_TSP_LARGE",
            requirements_text="Solve TSP with N=35",
            feasibility_cert=feas_cert,
        )

        self.assertFalse(res.admitted_to_planning)
        self.assertEqual(res.status, EpistemicStatus.UNRESOLVED)
        self.assertIn("PARAMETER_EXCEEDS_CERTIFIED_FEASIBILITY", res.reason)

    def test_pipeline_admits_proven_invariant(self):
        """Verify pipeline admits a formally proven discrete invariant."""
        inv_cert = InvariantCertificate(
            certificate_id="inv_cert_01",
            invariant_class=InvariantClass.BOUNDED_POTENTIAL,
            expression_representation="Phi(S) = sum(s_i)",
            codomain="NATURAL_NUMBERS",
            well_founded_proven=True,
            strict_decrease_proven=True,
            modular_conservation_proven=False,
            termination_bound_steps=50,
            status=EpistemicStatus.PROVEN,
        )

        res = UnifiedResearchPipeline.execute(
            problem_id="PROB_GAME_CONVERGENCE",
            requirements_text="Prove finite termination of state transitions",
            invariant_cert=inv_cert,
        )

        self.assertTrue(res.admitted_to_planning)
        self.assertEqual(res.status, EpistemicStatus.PROVEN)
        self.assertIn("Discrete invariant verified", res.reason)

    def test_pipeline_fallback_unresolved_zero_code_generation(self):
        """Verify pipeline fails closed with UNRESOLVED when no proof or evidence is provided."""
        res = UnifiedResearchPipeline.execute(
            problem_id="PROB_UNKNOWN",
            requirements_text="Arbitrary unanalyzed specification",
        )

        self.assertFalse(res.admitted_to_planning)
        self.assertEqual(res.status, EpistemicStatus.UNRESOLVED)
        self.assertIn("zero code generation", res.reason)


if __name__ == "__main__":
    unittest.main()
