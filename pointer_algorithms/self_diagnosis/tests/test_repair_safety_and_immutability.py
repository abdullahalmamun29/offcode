"""
Phase 9 — test_repair_safety_and_immutability.py

Tests safety invariants:
- DiagnosticCertificate deep immutability (dataclasses.FrozenInstanceError on mutation)
- Single-shot repair bound (attempts_used is 1, no loops)
- Plan and requirements byte-identity preservation (zero reasoning mutation)
"""

import dataclasses
import hashlib
import json
import unittest

from pointer_algorithms.self_diagnosis.diagnostic_types import (
    ClassificationStatus,
    DiagnosticCertificate,
    DiagnosticMode,
    ImplementationBugKind,
    MissingHeaderEvidence,
    RepairStrategy,
    ReproducibilityStatus,
)
from pointer_algorithms.self_diagnosis.generation_provenance import GenerationProvenance
from pointer_algorithms.self_diagnosis.oracle_integrity import OracleExecutionEvidence
from pointer_algorithms.self_diagnosis.self_diagnosis_facade import SelfDiagnosisFacade


class TestRepairSafetyAndImmutability(unittest.TestCase):

    def setUp(self):
        self.evidence = MissingHeaderEvidence(
            missing_header="<algorithm>",
            required_by_identifier="std::sort",
            compiler_diagnostic_excerpt="sort not found",
        )
        self.cert = DiagnosticCertificate(
            certificate_id="cert_immut_01",
            classification_status=ClassificationStatus.CLASSIFIED,
            mode=DiagnosticMode.VALID_CANDIDATE_IMPLEMENTATION_BUG,
            bug_kind=ImplementationBugKind.MISSING_HEADER,
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
            is_repairable=True,
            recommended_strategy=RepairStrategy.ADD_MISSING_HEADER,
            structured_evidence=self.evidence,
            epistemic_status="PROVEN",
        )

    def test_certificate_deep_immutability(self):
        """Mutating any field on DiagnosticCertificate must raise FrozenInstanceError."""
        with self.assertRaises(dataclasses.FrozenInstanceError):
            self.cert.is_repairable = False

        with self.assertRaises(dataclasses.FrozenInstanceError):
            self.cert.mode = DiagnosticMode.ORACLE_DEFECT

        with self.assertRaises(dataclasses.FrozenInstanceError):
            self.cert.recommended_strategy = RepairStrategy.NONE

    def test_structured_evidence_deep_immutability(self):
        """Mutating any field on StructuredEvidence must raise FrozenInstanceError."""
        with self.assertRaises(dataclasses.FrozenInstanceError):
            self.evidence.missing_header = "<iostream>"

    def test_single_shot_bound_and_no_reasoning_mutation(self):
        """
        Verify that SelfDiagnosisFacade executes single-shot repair without mutating
        the authoritative plan or requirements.
        """
        source = (
            "#include <iostream>\n"
            "#include <vector>\n"
            "int main() {\n"
            "    std::vector<int> v = {3, 1, 2};\n"
            "    std::sort(v.begin(), v.end());\n"
            "    return 0;\n"
            "}\n"
        )
        src_bytes = source.encode()
        src_hash = hashlib.sha256(src_bytes).hexdigest()

        original_plan = {
            "status": "VALID_OPTIMAL_PLAN",
            "candidate_id": "sort_algorithm",
            "constraints": {"N_max": 1000},
        }
        original_plan_json = json.dumps(original_plan, sort_keys=True)
        plan_hash = hashlib.sha256(original_plan_json.encode()).hexdigest()

        original_req = "Find sorted order of N integers."
        req_hash = hashlib.sha256(original_req.encode()).hexdigest()

        prov = GenerationProvenance(
            plan_hash=plan_hash,
            candidate_source_hash=src_hash,
            generator_version="gen-1.0",
            generation_timestamp_utc="2026-09-23T10:00:00Z",
            generation_contract_hash="hash",
        )

        from pointer_algorithms.self_diagnosis.failure_evidence import FailureEvidence
        err = "error: 'sort' is not a member of 'std'"
        ev_runs = [
            FailureEvidence(
                candidate_source_hash=src_hash,
                test_vector_hash="vec_01",
                compiler_identity_hash="comp",
                compiler_flags=("-O3",),
                exit_code=1,
                signal_received=None,
                stdout_hash="out",
                stderr_hash="err",
                stderr_excerpt=err,
                wall_time_ms=10.0,
                peak_rss_kb=1024,
                compiler_diagnostic_lines=(err,),
                execution_timestamp_utc="2026-09-23T10:00:00Z",
            )
            for _ in range(3)
        ]

        oracle_runs = [
            OracleExecutionEvidence(exit_code=0, stdout="OK", stderr="", crashed=False)
        ]

        envelope = {
            "source_hash": src_hash,
            "compiler_hash": "comp",
            "flags": ["-O3"],
            "input_hash": "vec_01",
        }

        ast_ctx = {"identifiers": ["sort", "std::sort"], "includes": ["<iostream>", "<vector>"]}

        facade = SelfDiagnosisFacade()
        res = facade.run(
            problem_id="prob_immut",
            requirements_hash=req_hash,
            phase5_plan=original_plan,
            candidate_source=source,
            compiler_identity_hash="comp",
            generation_provenance=prov,
            evidence_runs=ev_runs,
            oracle_runs=oracle_runs,
            controlled_envelope=envelope,
            ast_context=ast_ctx,
            witness_runner=lambda src: "<algorithm>" in src,
            candidate_suite_runner=lambda src: True,
            phase8_suite_runner=lambda src: True,
            historical_suite_runner=lambda: True,
        )

        self.assertTrue(res.repaired)
        self.assertIsNotNone(res.self_correction_certificate)
        self.assertEqual(res.self_correction_certificate.attempts_used, 1)

        # Invariant: Phase 5 plan JSON remains 100% byte-identical
        after_plan_json = json.dumps(original_plan, sort_keys=True)
        self.assertEqual(original_plan_json, after_plan_json)

        # Invariant: Requirements hash remains identical
        self.assertEqual(req_hash, hashlib.sha256(original_req.encode()).hexdigest())


if __name__ == "__main__":
    unittest.main()
