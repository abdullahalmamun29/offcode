"""
Phase 9 — test_repair_engine_cannot_select_strategy.py

Tests that TargetedRepairEngine cannot select or invent its own repair strategy:
- Unclassified defect with strategy NONE is rejected.
- Mismatched strategy (e.g. bug_kind is index translation, but strategy is widening) is rejected.
- The engine executes strictly the authorized transformation from the certificate.
"""

import hashlib
import unittest

from pointer_algorithms.self_diagnosis.diagnostic_types import (
    ClassificationStatus,
    DiagnosticCertificate,
    DiagnosticMode,
    ImplementationBugKind,
    IndexMappingEvidence,
    OverflowEvidence,
    RepairStrategy,
    ReproducibilityStatus,
)
from pointer_algorithms.self_diagnosis.repair_strategies import build_self_correction_plan
from pointer_algorithms.self_diagnosis.targeted_repair_engine import TargetedRepairEngine


class TestRepairEngineCannotSelectStrategy(unittest.TestCase):

    def _make_dummy_cert(self, bug_kind, strategy, evidence, is_repairable=True):
        return DiagnosticCertificate(
            certificate_id="diag_auth_test",
            classification_status=ClassificationStatus.CLASSIFIED,
            mode=DiagnosticMode.VALID_CANDIDATE_IMPLEMENTATION_BUG,
            bug_kind=bug_kind,
            stage="TEST",
            problem_hash="prob_hash",
            requirements_hash="req_hash",
            plan_hash="plan_hash",
            candidate_source_hash="src_hash",
            compiler_identity_hash="comp_hash",
            test_vector_hash="vec_hash",
            generation_provenance_hash="gen_hash",
            causal_witness={},
            reproducibility_status=ReproducibilityStatus.CONTROLLED_REPRODUCIBLE,
            reproduction_runs=3,
            is_repairable=is_repairable,
            recommended_strategy=strategy,
            structured_evidence=evidence,
            epistemic_status="PROVEN",
        )

    def test_unclassified_bug_produces_no_repair(self):
        """Unclassified defect with strategy NONE is rejected for repair."""
        cert = self._make_dummy_cert(
            bug_kind=ImplementationBugKind.UNCLASSIFIED_CODE_DEFECT,
            strategy=RepairStrategy.NONE,
            evidence=None,
            is_repairable=False,
        )
        self.assertFalse(TargetedRepairEngine.authorize(cert))
        self.assertIsNone(build_self_correction_plan(cert))

    def test_mismatched_strategy_is_rejected(self):
        """
        If bug_kind is CERTIFIED_INDEX_BASE_TRANSLATION but strategy is WIDEN_TO_64BIT,
        the engine detects authorization failure and strictly rejects repair.
        """
        ev = IndexMappingEvidence(
            external_base=1,
            internal_base=0,
            offending_expression="a[x]",
            translated_expression="a[x - 1]",
            target_scope="solve",
        )
        cert = self._make_dummy_cert(
            bug_kind=ImplementationBugKind.CERTIFIED_INDEX_BASE_TRANSLATION,
            strategy=RepairStrategy.WIDEN_TO_64BIT,  # MISMATCH!
            evidence=ev,
            is_repairable=True,
        )
        self.assertFalse(TargetedRepairEngine.authorize(cert))
        self.assertIsNone(build_self_correction_plan(cert))

    def test_engine_executes_only_authorized_strategy(self):
        """Engine authorizes and builds plan only when bug_kind and strategy match perfectly."""
        ev = OverflowEvidence(
            constraint_n_bound=1000,
            constraint_value_bound=1000,
            max_intermediate_magnitude=10**12,
            original_identifier="ans",
            target_scope="solve",
        )
        cert = self._make_dummy_cert(
            bug_kind=ImplementationBugKind.TYPE_WIDTH_MISMATCH,
            strategy=RepairStrategy.WIDEN_TO_64BIT,
            evidence=ev,
            is_repairable=True,
        )
        self.assertTrue(TargetedRepairEngine.authorize(cert))
        plan = build_self_correction_plan(cert)
        self.assertIsNotNone(plan)
        self.assertEqual(plan.strategy, RepairStrategy.WIDEN_TO_64BIT)


if __name__ == "__main__":
    unittest.main()
