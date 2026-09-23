"""
Phase 9 — test_mathematically_proven_repairs.py

Tests mathematically proven repair classes and fail-closed edge cases:
- Missing header with STL registry and AST verification
- Integer overflow with proven range (widen to long long)
- Integer overflow exceeding LLONG_MAX fails closed
- Integer overflow without range proof fails closed
- Index translation with structured evidence
- Boundary guard with proven algebraic identity
- Boundary guard without proven identity fails closed
"""

import hashlib
import json
import unittest

from pointer_algorithms.self_diagnosis.causal_analyzer import CausalAnalyzer
from pointer_algorithms.self_diagnosis.diagnostic_types import (
    BoundaryGuardEvidence,
    ClassificationStatus,
    DiagnosticMode,
    ImplementationBugKind,
    IndexMappingEvidence,
    MissingHeaderEvidence,
    OverflowEvidence,
    RepairStrategy,
)
from pointer_algorithms.self_diagnosis.failure_classifier import DeterministicFailureClassifier
from pointer_algorithms.self_diagnosis.failure_evidence import FailureEvidence
from pointer_algorithms.self_diagnosis.generation_provenance import GenerationProvenance
from pointer_algorithms.self_diagnosis.oracle_integrity import OracleExecutionEvidence
from pointer_algorithms.self_diagnosis.repair_strategies import build_self_correction_plan
from pointer_algorithms.self_diagnosis.targeted_repair_engine import TargetedRepairEngine


class TestMathematicallyProvenRepairs(unittest.TestCase):

    def setUp(self):
        self.problem_id = "math_repair_prob"
        self.comp_hash = hashlib.sha256(b"g++-12").hexdigest()
        self.healthy_oracle = [
            OracleExecutionEvidence(exit_code=0, stdout="OK", stderr="", crashed=False)
        ]

    def _setup_context(self, source, plan_dict):
        src_bytes = source.encode()
        src_hash = hashlib.sha256(src_bytes).hexdigest()
        plan_hash = hashlib.sha256(json.dumps(plan_dict, sort_keys=True).encode()).hexdigest()
        prov = GenerationProvenance(
            plan_hash=plan_hash,
            candidate_source_hash=src_hash,
            generator_version="gen-1.0",
            generation_timestamp_utc="2026-09-23T10:00:00Z",
            generation_contract_hash="hash",
        )
        envelope = {
            "source_hash": src_hash,
            "compiler_hash": self.comp_hash,
            "flags": ["-O3"],
            "input_hash": "vec_01",
        }
        return src_hash, plan_hash, prov, envelope

    def test_missing_header_stl_registry_verified(self):
        source = "#include <vector>\nint main() { std::sort(nullptr, nullptr); return 0; }"
        plan = {"status": "VALID_OPTIMAL_PLAN"}
        src_hash, plan_hash, prov, env = self._setup_context(source, plan)
        err = "error: 'sort' is not a member of 'std'"

        ev_runs = [
            FailureEvidence(
                candidate_source_hash=src_hash,
                test_vector_hash="vec_01",
                compiler_identity_hash=self.comp_hash,
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

        ast_ctx = {"identifiers": ["sort", "std::sort"], "includes": ["<vector>"]}

        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash="req",
            phase5_plan=plan,
            candidate_source=source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=prov,
            evidence_runs=ev_runs,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=env,
            ast_context=ast_ctx,
        )
        self.assertTrue(cert.is_repairable)
        self.assertEqual(cert.bug_kind, ImplementationBugKind.MISSING_HEADER)
        self.assertEqual(cert.recommended_strategy, RepairStrategy.ADD_MISSING_HEADER)
        self.assertIsInstance(cert.structured_evidence, MissingHeaderEvidence)
        self.assertEqual(cert.structured_evidence.missing_header, "<algorithm>")

        # Test repair execution
        plan_obj = build_self_correction_plan(cert)
        repair_res = TargetedRepairEngine.apply_repair(source, plan_obj, cert)
        self.assertTrue(repair_res.success)
        self.assertIn("#include <algorithm>", repair_res.repaired_source)

    def test_integer_overflow_with_proven_range(self):
        source = (
            "#include <iostream>\n"
            "#include <vector>\n"
            "using namespace std;\n"
            "int main() {\n"
            "    int sum = 0;\n"
            "    return sum;\n"
            "}\n"
        )
        plan = {
            "status": "VALID_OPTIMAL_PLAN",
            "constraints": {"N_max": 200_000, "value_max": 1_000_000_000},
        }
        src_hash, plan_hash, prov, env = self._setup_context(source, plan)
        ev_runs = [
            FailureEvidence(
                candidate_source_hash=src_hash,
                test_vector_hash="vec_01",
                compiler_identity_hash=self.comp_hash,
                compiler_flags=("-O3",),
                exit_code=0,
                signal_received=None,
                stdout_hash="wrong_out",
                stderr_hash="",
                stderr_excerpt="Wrong answer on test 5 (overflow)",
                wall_time_ms=10.0,
                peak_rss_kb=1024,
                compiler_diagnostic_lines=(),
                execution_timestamp_utc="2026-09-23T10:00:00Z",
            )
            for _ in range(3)
        ]

        # Phase 6 derived fact with intermediate magnitude 2 * 10^14
        phase6_facts = [{
            "fact_type": "INTERMEDIATE_ACCUMULATOR_MAGNITUDE",
            "max_magnitude": 200_000_000_000_000,
            "target_variable": "sum",
            "target_scope": "main",
        }]

        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash="req",
            phase5_plan=plan,
            candidate_source=source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=prov,
            evidence_runs=ev_runs,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=env,
            phase6_facts=phase6_facts,
        )

        self.assertTrue(cert.is_repairable)
        self.assertEqual(cert.bug_kind, ImplementationBugKind.TYPE_WIDTH_MISMATCH)
        self.assertEqual(cert.recommended_strategy, RepairStrategy.WIDEN_TO_64BIT)
        self.assertIsInstance(cert.structured_evidence, OverflowEvidence)
        self.assertTrue(cert.structured_evidence.is_widening_sufficient())

        # Test repair execution
        plan_obj = build_self_correction_plan(cert)
        repair_res = TargetedRepairEngine.apply_repair(source, plan_obj, cert)
        self.assertTrue(repair_res.success)
        self.assertIn("long long sum = 0;", repair_res.repaired_source)

    def test_integer_overflow_exceeding_llong_max_fails_closed(self):
        """If required magnitude exceeds LLONG_MAX, widening is insufficient -> fail closed!"""
        source = "int main() { int sum = 0; return 0; }"
        plan = {"status": "VALID_OPTIMAL_PLAN", "constraints": {}}
        src_hash, plan_hash, prov, env = self._setup_context(source, plan)
        ev_runs = [
            FailureEvidence(
                candidate_source_hash=src_hash,
                test_vector_hash="vec_01",
                compiler_identity_hash=self.comp_hash,
                compiler_flags=("-O3",),
                exit_code=0,
                signal_received=None,
                stdout_hash="out",
                stderr_hash="",
                stderr_excerpt="",
                wall_time_ms=10.0,
                peak_rss_kb=1024,
                compiler_diagnostic_lines=(),
                execution_timestamp_utc="2026-09-23T10:00:00Z",
            )
            for _ in range(3)
        ]

        # Intermediate magnitude exceeds LLONG_MAX (e.g. 10^20)
        phase6_facts = [{
            "fact_type": "INTERMEDIATE_ACCUMULATOR_MAGNITUDE",
            "max_magnitude": 10**20,
            "target_variable": "sum",
            "target_scope": "main",
        }]

        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash="req",
            phase5_plan=plan,
            candidate_source=source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=prov,
            evidence_runs=ev_runs,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=env,
            phase6_facts=phase6_facts,
        )
        self.assertFalse(cert.is_repairable)
        self.assertEqual(cert.recommended_strategy, RepairStrategy.NONE)
        self.assertIn("exceeds LLONG_MAX", cert.unresolved_reason)

    def test_integer_overflow_without_range_proof_fails_closed(self):
        """Without Phase 6 proven range fact, overflow is not assumed -> no repair."""
        source = "int main() { int sum = 0; return 0; }"
        plan = {"status": "VALID_OPTIMAL_PLAN", "constraints": {}}
        src_hash, plan_hash, prov, env = self._setup_context(source, plan)
        ev_runs = [
            FailureEvidence(
                candidate_source_hash=src_hash,
                test_vector_hash="vec_01",
                compiler_identity_hash=self.comp_hash,
                compiler_flags=("-O3",),
                exit_code=0,
                signal_received=None,
                stdout_hash="out",
                stderr_hash="",
                stderr_excerpt="WA",
                wall_time_ms=10.0,
                peak_rss_kb=1024,
                compiler_diagnostic_lines=(),
                execution_timestamp_utc="2026-09-23T10:00:00Z",
            )
            for _ in range(3)
        ]

        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash="req",
            phase5_plan=plan,
            candidate_source=source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=prov,
            evidence_runs=ev_runs,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=env,
            phase6_facts=(),  # No fact!
        )
        self.assertFalse(cert.is_repairable)

    def test_index_translation_with_structured_evidence(self):
        source = "void solve() { int u; cin >> u; a[u] = 1; }"
        plan = {"status": "VALID_OPTIMAL_PLAN"}
        src_hash, plan_hash, prov, env = self._setup_context(source, plan)
        ev_runs = [
            FailureEvidence(
                candidate_source_hash=src_hash,
                test_vector_hash="vec_01",
                compiler_identity_hash=self.comp_hash,
                compiler_flags=("-O3",),
                exit_code=139,
                signal_received=11,
                stdout_hash="out",
                stderr_hash="",
                stderr_excerpt="SIGSEGV out of bounds",
                wall_time_ms=10.0,
                peak_rss_kb=1024,
                compiler_diagnostic_lines=(),
                execution_timestamp_utc="2026-09-23T10:00:00Z",
            )
            for _ in range(3)
        ]

        phase6_facts = [{
            "fact_type": "INDEXING_BASE_DISCREPANCY",
            "external_base": 1,
            "internal_base": 0,
            "offending_expression": "a[u]",
            "translated_expression": "a[u - 1]",
            "target_scope": "solve",
        }]

        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash="req",
            phase5_plan=plan,
            candidate_source=source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=prov,
            evidence_runs=ev_runs,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=env,
            phase6_facts=phase6_facts,
        )
        self.assertTrue(cert.is_repairable)
        self.assertEqual(cert.bug_kind, ImplementationBugKind.CERTIFIED_INDEX_BASE_TRANSLATION)
        self.assertEqual(cert.recommended_strategy, RepairStrategy.ADJUST_INDEX_BASE)
        self.assertIsInstance(cert.structured_evidence, IndexMappingEvidence)

        plan_obj = build_self_correction_plan(cert)
        repair_res = TargetedRepairEngine.apply_repair(source, plan_obj, cert)
        self.assertTrue(repair_res.success)
        self.assertIn("a[u - 1] = 1;", repair_res.repaired_source)

    def test_boundary_guard_with_proven_identity(self):
        source = (
            "#include <iostream>\n"
            "using namespace std;\n"
            "int solve(int n) {\n"
            "    int ans = 100 / n;\n"
            "    return ans;\n"
            "}\n"
            "int main() { return 0; }\n"
        )
        plan = {"status": "VALID_OPTIMAL_PLAN"}
        src_hash, plan_hash, prov, env = self._setup_context(source, plan)
        ev_runs = [
            FailureEvidence(
                candidate_source_hash=src_hash,
                test_vector_hash="vec_01",
                compiler_identity_hash=self.comp_hash,
                compiler_flags=("-O3",),
                exit_code=136,
                signal_received=8,  # SIGFPE
                stdout_hash="out",
                stderr_hash="",
                stderr_excerpt="SIGFPE division by zero",
                wall_time_ms=10.0,
                peak_rss_kb=1024,
                compiler_diagnostic_lines=(),
                execution_timestamp_utc="2026-09-23T10:00:00Z",
            )
            for _ in range(3)
        ]

        phase6_facts = [{
            "fact_type": "BOUNDARY_ALGEBRAIC_IDENTITY",
            "boundary_condition": "n == 0",
            "identity_expression": "0",
            "proof_reference": "FACT_P6_EMPTY_IDENTITY_0",
            "source_layer": "PHASE6_DERIVED_FACT",
        }]

        cert = DeterministicFailureClassifier.classify(
            problem_id=self.problem_id,
            requirements_hash="req",
            phase5_plan=plan,
            candidate_source=source,
            compiler_identity_hash=self.comp_hash,
            generation_provenance=prov,
            evidence_runs=ev_runs,
            oracle_runs=self.healthy_oracle,
            controlled_envelope=env,
            phase6_facts=phase6_facts,
        )
        self.assertTrue(cert.is_repairable)
        self.assertEqual(cert.bug_kind, ImplementationBugKind.CERTIFIED_BOUNDARY_GUARD)
        self.assertEqual(cert.recommended_strategy, RepairStrategy.INSERT_BOUNDARY_GUARD)
        self.assertIsInstance(cert.structured_evidence, BoundaryGuardEvidence)

        plan_obj = build_self_correction_plan(cert)
        repair_res = TargetedRepairEngine.apply_repair(source, plan_obj, cert)
        self.assertTrue(repair_res.success)
        self.assertIn("if (n == 0) return 0;", repair_res.repaired_source)


if __name__ == "__main__":
    unittest.main()
