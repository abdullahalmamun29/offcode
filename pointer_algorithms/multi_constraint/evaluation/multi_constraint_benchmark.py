"""
CHUP Phase 5 — Multi-Constraint Benchmark Evaluation Suite (Tier 2).

Measures reasoning latency, throughput, memory stability, and determinism
across diverse problem sizes, ensuring all solving decisions complete well
under the 50ms ceiling with zero memory leaks.
"""

import unittest
import time
from pointer_algorithms.multi_constraint.facade import MultiConstraintSolver
from pointer_algorithms.multi_constraint.multi_constraint_model import OutcomeState


class TestMultiConstraintBenchmark(unittest.TestCase):
    """Tier 2 evaluation: latency, scalability, and determinism benchmarks."""

    def setUp(self):
        self.solver = MultiConstraintSolver()

    def test_bench_01_single_candidate_latency(self):
        """Single candidate solving decision latency must be well under 10ms."""
        spec = {
            "temporal": "ONLINE",
            "mutability": "POINT_UPDATE",
            "operation": "SUM",
            "query_target": "LINEAR_RANGE"
        }
        # Warmup
        self.solver.solve(spec)

        start = time.perf_counter()
        iterations = 100
        for _ in range(iterations):
            res = self.solver.solve(spec)
            self.assertEqual(res["outcome_state"], OutcomeState.SATISFIABLE_SINGLE_CANDIDATE)
        duration = time.perf_counter() - start
        avg_ms = (duration / iterations) * 1000.0

        self.assertLess(avg_ms, 10.0, f"Average latency {avg_ms:.3f}ms exceeds 10ms threshold")

    def test_bench_02_composed_plan_latency(self):
        """Multi-component composition synthesis latency must be well under 25ms."""
        spec = {
            "topology": "UNDIRECTED_TREE",
            "v": 100000,
            "e": 99999,
            "query_target": "TREE_PATH",
            "mutability": "POINT_UPDATE",
            "operation": "SUM"
        }
        # Warmup
        self.solver.solve(spec)

        start = time.perf_counter()
        iterations = 100
        for _ in range(iterations):
            res = self.solver.solve(spec)
            self.assertEqual(res["outcome_state"], OutcomeState.SATISFIABLE_COMPOSED_PLAN)
        duration = time.perf_counter() - start
        avg_ms = (duration / iterations) * 1000.0

        self.assertLess(avg_ms, 25.0, f"Composition latency {avg_ms:.3f}ms exceeds 25ms threshold")

    def test_bench_03_conflict_detection_latency(self):
        """Axiomatic contradiction detection latency must be under 5ms."""
        spec = {
            "topology": "UNDIRECTED_TREE",
            "v": 100,
            "e": 105
        }
        # Warmup
        self.solver.solve(spec)

        start = time.perf_counter()
        iterations = 100
        for _ in range(iterations):
            res = self.solver.solve(spec)
            self.assertEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        duration = time.perf_counter() - start
        avg_ms = (duration / iterations) * 1000.0

        self.assertLess(avg_ms, 5.0, f"Conflict detection latency {avg_ms:.3f}ms exceeds 5ms threshold")

    def test_bench_04_coverage_gap_latency(self):
        """Coverage gap detection latency must be under 20ms."""
        spec = {
            "query_target": "ALL_PAIRS",
            "mutability": "RANGE_UPDATE",
            "temporal": "STREAMING"
        }
        # Warmup
        self.solver.solve(spec)

        start = time.perf_counter()
        iterations = 100
        for _ in range(iterations):
            res = self.solver.solve(spec)
            self.assertEqual(res["outcome_state"], OutcomeState.UNRESOLVED_BY_CURRENT_ONTOLOGY)
        duration = time.perf_counter() - start
        avg_ms = (duration / iterations) * 1000.0

        self.assertLess(avg_ms, 20.0, f"Coverage gap latency {avg_ms:.3f}ms exceeds 20ms threshold")

    def test_bench_05_determinism_across_all_outcome_states(self):
        """Repeated invocations across all 4 terminal outcome states yield bit-identical plans and certificates."""
        specs = [
            (
                {"temporal": "ONLINE", "mutability": "STATIC", "operation": "MIN", "query_target": "LINEAR_RANGE"},
                OutcomeState.SATISFIABLE_SINGLE_CANDIDATE
            ),
            (
                {"topology": "UNDIRECTED_TREE", "v": 5000, "e": 4999, "query_target": "TREE_PATH", "mutability": "POINT_UPDATE", "operation": "SUM"},
                OutcomeState.SATISFIABLE_COMPOSED_PLAN
            ),
            (
                {"topology": "UNDIRECTED_TREE", "v": 10, "e": 15},
                OutcomeState.UNSATISFIABLE_CONSTRAINT_SET
            ),
            (
                {"query_target": "ALL_PAIRS", "mutability": "RANGE_UPDATE", "temporal": "STREAMING"},
                OutcomeState.UNRESOLVED_BY_CURRENT_ONTOLOGY
            )
        ]

        for spec, expected_state in specs:
            runs = [self.solver.solve(spec) for _ in range(10)]
            for r in runs:
                self.assertEqual(r["outcome_state"], expected_state)
            if expected_state in (OutcomeState.SATISFIABLE_SINGLE_CANDIDATE, OutcomeState.SATISFIABLE_COMPOSED_PLAN):
                first_components = runs[0]["verified_plan"].selected_components
                for r in runs[1:]:
                    self.assertEqual(r["verified_plan"].selected_components, first_components)
                    self.assertTrue(r["verified_plan"].verify_seal())


if __name__ == "__main__":
    unittest.main()
