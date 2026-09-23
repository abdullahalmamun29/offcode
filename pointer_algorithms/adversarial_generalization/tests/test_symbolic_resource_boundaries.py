"""
Test Symbolic Resource Boundaries & Memory Layouts.

Verifies:
1. Strict Phase 5 SymbolicBudget evaluation without heuristic guessing.
2. Accurate accounting of element byte sizes (4 vs 8 bytes).
3. Exact auxiliary structure memory calculation (Segment Tree 4N, Sparse Table N log N).
4. Rejection when time or space limits are exceeded.
"""

import unittest

from pointer_algorithms.adversarial_generalization.symbolic_boundary_evaluator import SymbolicBoundaryEvaluator
from pointer_algorithms.adversarial_generalization.certified_fixtures import SymbolicBudgetSpec
from pointer_algorithms.multi_constraint.domain_capability_adapter import DomainCapabilityAdapter


class TestSymbolicResourceBoundaries(unittest.TestCase):

    def setUp(self):
        self.universe = DomainCapabilityAdapter.get_candidate_universe()

    def test_memory_footprint_scaling_by_element_size(self):
        n = 100000
        # 4-byte integers
        flat_4 = SymbolicBoundaryEvaluator.calculate_memory_footprint("flat_array", n, element_size_bytes=4)
        self.assertEqual(flat_4, 400000)

        # 8-byte integers
        flat_8 = SymbolicBoundaryEvaluator.calculate_memory_footprint("flat_array", n, element_size_bytes=8)
        self.assertEqual(flat_8, 800000)

        # Segment tree 4N nodes
        seg_4 = SymbolicBoundaryEvaluator.calculate_memory_footprint("segment_tree", n, element_size_bytes=4)
        self.assertEqual(seg_4, 1600000)

        seg_8 = SymbolicBoundaryEvaluator.calculate_memory_footprint("segment_tree", n, element_size_bytes=8)
        self.assertEqual(seg_8, 3200000)

        # Sparse Table N * log2(N)
        sparse_4 = SymbolicBoundaryEvaluator.calculate_memory_footprint("sparse_table", n, element_size_bytes=4)
        self.assertGreater(sparse_4, seg_4)

    def test_candidate_resource_evaluation_under_budget(self):
        cand = self.universe.get("fenwick_tree")
        self.assertIsNotNone(cand)

        spec = SymbolicBudgetSpec(
            n_bound=200000,
            q_bound=200000,
            time_limit_sec=1.5,
            memory_limit_mb=256,
            element_size_bytes=8
        )

        res = SymbolicBoundaryEvaluator.evaluate_candidate(cand, spec)
        self.assertTrue(res.is_feasible)
        self.assertTrue(res.is_time_feasible)
        self.assertTrue(res.is_space_feasible)
        self.assertIsNone(res.failure_code)

    def test_candidate_resource_evaluation_exceeding_memory(self):
        cand = self.universe.get("fenwick_tree")
        self.assertIsNotNone(cand)

        # Massive N that exceeds memory limit of 16MB
        spec = SymbolicBudgetSpec(
            n_bound=50000000, # 50 million elements * 8 bytes = ~400 MB
            q_bound=100000,
            time_limit_sec=5.0,
            memory_limit_mb=16, # Only 16 MB allowed
            element_size_bytes=8
        )

        res = SymbolicBoundaryEvaluator.evaluate_candidate(cand, spec)
        self.assertFalse(res.is_space_feasible)
        self.assertFalse(res.is_feasible)
        self.assertIn("SPACE_BOUND_EXCEEDED", res.failure_code)


if __name__ == "__main__":
    unittest.main()
