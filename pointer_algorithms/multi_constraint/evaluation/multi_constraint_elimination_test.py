"""
CHUP Phase 5 — Multi-Constraint Elimination Evaluation Suite (Tier 2).

Verifies closed-world elimination across 15 distinct negative witness scenarios,
ensuring machine-verifiable EliminationCertificates with authoritative failure codes.
"""

import unittest
from pointer_algorithms.multi_constraint.facade import MultiConstraintSolver
from pointer_algorithms.multi_constraint.multi_constraint_model import OutcomeState
from pointer_algorithms.multi_constraint.constraint_lattice import (
    TemporalMode,
    MutabilityCapability,
    CoordinateScale,
)


class TestMultiConstraintElimination(unittest.TestCase):
    """Tier 2 evaluation: comprehensive verification of candidate elimination certificates."""

    def setUp(self):
        self.solver = MultiConstraintSolver()

    def test_elim_01_mutability_sparse_table_point_update(self):
        """Sparse Table eliminated on POINT_UPDATE with MUTATION_DISALLOWED_ON_STATIC_STRUCTURE."""
        spec = {
            "temporal": "ONLINE",
            "mutability": "POINT_UPDATE",
            "operation": "MIN",
            "query_target": "LINEAR_RANGE"
        }
        elim = self.solver.explain_candidate("sparse_table", spec)
        self.assertIsNotNone(elim)
        self.assertEqual(elim.failure_code, "MUTATION_DISALLOWED_ON_STATIC_STRUCTURE")
        self.assertEqual(elim.candidate_id, "sparse_table")
        self.assertEqual(elim.severity, "HARD_PRECONDITION_VIOLATION")

    def test_elim_02_mutability_merge_sort_tree_range_write(self):
        """Merge Sort Tree eliminated on RANGE_UPDATE with MUTATION_DISALLOWED_ON_STATIC_STRUCTURE."""
        spec = {
            "temporal": "ONLINE",
            "mutability": "RANGE_UPDATE",
            "operation": "KTH",
            "query_target": "LINEAR_RANGE"
        }
        elim = self.solver.explain_candidate("merge_sort_tree", spec)
        self.assertIsNotNone(elim)
        self.assertEqual(elim.failure_code, "MUTATION_DISALLOWED_ON_STATIC_STRUCTURE")
        self.assertEqual(elim.candidate_id, "merge_sort_tree")

    def test_elim_03_temporal_mos_algorithm_online(self):
        """Mo's Algorithm eliminated on ONLINE mode with OFFLINE_MODE_REQUIRED_REJECTS_ONLINE_MOS."""
        spec = {
            "temporal": "ONLINE",
            "mutability": "STATIC",
            "operation": "DISTINCT",
            "query_target": "LINEAR_RANGE"
        }
        elim = self.solver.explain_candidate("mos_algorithm_scheduler", spec)
        self.assertIsNotNone(elim)
        self.assertEqual(elim.failure_code, "OFFLINE_MODE_REQUIRED_REJECTS_ONLINE_MOS")
        self.assertEqual(elim.severity, "TEMPORAL_INCOMPATIBILITY")

    def test_elim_04_algebraic_sparse_table_non_idempotent_sum(self):
        """Sparse Table eliminated on non-idempotent SUM with NON_IDEMPOTENT_OPERATION_REJECTS_SPARSE_TABLE."""
        spec = {
            "temporal": "ONLINE",
            "mutability": "STATIC",
            "operation": "SUM",
            "query_target": "LINEAR_RANGE"
        }
        elim = self.solver.explain_candidate("sparse_table", spec)
        self.assertIsNotNone(elim)
        self.assertEqual(elim.failure_code, "NON_IDEMPOTENT_OPERATION_REJECTS_SPARSE_TABLE")
        self.assertIn("Sparse Table", elim.asymptotic_argument)

    def test_elim_05_algebraic_fenwick_non_invertible_min(self):
        """Fenwick Tree eliminated on non-invertible MIN with NON_INVERTIBLE_OPERATION_REJECTS_FENWICK."""
        spec = {
            "temporal": "ONLINE",
            "mutability": "POINT_UPDATE",
            "operation": "MIN",
            "query_target": "LINEAR_RANGE"
        }
        elim = self.solver.explain_candidate("fenwick_tree", spec)
        self.assertIsNotNone(elim)
        self.assertEqual(elim.failure_code, "NON_INVERTIBLE_OPERATION_REJECTS_FENWICK")
        self.assertIn("Fenwick", elim.asymptotic_argument)

    def test_elim_06_dijkstra_negative_edge_weights(self):
        """Dijkstra eliminated on negative edge weights with NEGATIVE_WEIGHTS_REJECT_DIJKSTRA."""
        spec = {
            "query_target": "SINGLE_SOURCE_SHORTEST_PATH",
            "operation": "MIN",
            "negative_edge_weights": True
        }
        elim = self.solver.explain_candidate("dijkstra_priority_queue", spec)
        self.assertIsNotNone(elim)
        self.assertEqual(elim.failure_code, "NEGATIVE_WEIGHTS_REJECT_DIJKSTRA")
        self.assertEqual(elim.severity, "HARD_PRECONDITION_VIOLATION")

    def test_elim_07_two_pointers_negative_elements(self):
        """Two Pointers eliminated on negative sequence elements with NON_MONOTONE_WINDOW_REJECTS_TWO_POINTERS."""
        spec = {
            "query_target": "LINEAR_RANGE",
            "operation": "SUM",
            "negative_elements": True
        }
        elim = self.solver.explain_candidate("two_pointers_monotone_window", spec)
        self.assertIsNotNone(elim)
        self.assertEqual(elim.failure_code, "NON_MONOTONE_WINDOW_REJECTS_TWO_POINTERS")

    def test_elim_08_binary_search_oscillating_predicate(self):
        """Binary search eliminated on oscillating predicate with NON_MONOTONE_PREDICATE_REJECTS_BISECTION."""
        spec = {
            "query_target": "POINT_LOOKUP",
            "non_monotone_predicate": True
        }
        elim = self.solver.explain_candidate("binary_search_bisection", spec)
        self.assertIsNotNone(elim)
        self.assertEqual(elim.failure_code, "NON_MONOTONE_PREDICATE_REJECTS_BISECTION")

    def test_elim_09_monotonic_deque_non_convex_cost(self):
        """Monotonic deque eliminated on non-convex cost with NON_CONVEX_COST_REJECTS_MONOTONIC_DEQUE."""
        spec = {
            "query_target": "LINEAR_RANGE",
            "operation": "MIN",
            "non_convex_transition": True
        }
        elim = self.solver.explain_candidate("monotonic_deque_sliding_window", spec)
        self.assertIsNotNone(elim)
        self.assertEqual(elim.failure_code, "NON_CONVEX_COST_REJECTS_MONOTONIC_DEQUE")

    def test_elim_10_dynamic_segtree_dynamic_pointers_forbidden(self):
        """Dynamic Segment Tree eliminated when dynamic pointer allocation is forbidden."""
        spec = {
            "coordinate_scale": "MASSIVE",
            "dynamic_pointers_allowed": False,
            "operation": "SUM",
            "query_target": "LINEAR_RANGE"
        }
        elim = self.solver.explain_candidate("dynamic_segment_tree", spec)
        self.assertIsNotNone(elim)
        self.assertEqual(elim.failure_code, "DYNAMIC_POINTER_ALLOCATION_FORBIDDEN")

    def test_elim_11_massive_coordinates_flat_array_rejection(self):
        """Flat array structures rejected by massive coordinates (10^18) without compression."""
        spec = {
            "coordinate_scale": "MASSIVE",
            "operation": "SUM",
            "query_target": "LINEAR_RANGE"
        }
        elim = self.solver.explain_candidate("segment_tree_standard", spec)
        self.assertIsNotNone(elim)
        self.assertEqual(elim.failure_code, "MASSIVE_COORDINATES_REJECT_FLAT_ARRAY")

    def test_elim_12_space_bound_exceeded_massive_elements(self):
        """Space bound exceeded for N=20,000,000 with 64MB memory limit."""
        spec = {
            "n": 20000000,
            "q": 10,
            "memory_limit_mb": 64,
            "time_limit_ms": 100000,
            "operation": "SUM",
            "query_target": "LINEAR_RANGE",
            "mutability": "POINT_UPDATE"
        }
        elim = self.solver.explain_candidate("segment_tree_standard", spec)
        self.assertIsNotNone(elim)
        self.assertEqual(elim.failure_code, "SPACE_BOUND_EXCEEDED")
        self.assertEqual(elim.severity, "RESOURCE_BUDGET_EXCEEDED")

    def test_elim_13_time_budget_exceeded_quadratic_ops(self):
        """Time budget exceeded for Q=200,000 on O(N) linear query structure."""
        spec = {
            "n": 100000,
            "q": 200000,
            "time_limit_ms": 100,
            "operation": "SUM",
            "query_target": "LINEAR_RANGE"
        }
        # In a custom/generic linear scanner with O(N) per query, ops = 2e10 >> 1e7
        # We test time budget rejection through a candidate requiring O(N) per query
        from pointer_algorithms.multi_constraint.candidate_profile import CandidateProfile, SymbolicComplexity
        from pointer_algorithms.multi_constraint.resource_evaluator import SymbolicBudget
        from pointer_algorithms.multi_constraint.elimination_engine import EliminationEngine

        cand = CandidateProfile(
            candidate_id="brute_force_scanner",
            family="BruteForce",
            display_name="Brute Force Linear Scanner",
            supported_temporals=frozenset([TemporalMode.ONLINE, TemporalMode.OFFLINE]),
            supported_mutability=self.solver.universe["segment_tree_standard"].supported_mutability,
            supported_query_targets=self.solver.universe["segment_tree_standard"].supported_query_targets,
            supported_aggregate_names=frozenset(["SUM"]),
            produces_capabilities=frozenset(["RANGE_AGGREGATION"]),
            complexity=SymbolicComplexity(
                time_op_formula="N",
                total_time_formula="Q * N",
                space_bytes_formula="4 * N",
                space_complexity_class="O(N)",
                estimate_ops=lambda n, q, v, e, c: q * n,
                estimate_bytes=lambda n, q, v, e, c: 4 * n
            )
        )
        vec = self.solver.parse_spec(spec)
        budget = SymbolicBudget(N=100000, Q=200000, time_limit_ms=100)
        query = self.solver.parse_query(spec)
        cert = EliminationEngine.verify_and_eliminate(cand, vec, query, budget)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.failure_code, "TIME_BUDGET_EXCEEDED")

    def test_elim_14_query_target_topology_incompatible(self):
        """Segment tree directly querying TREE_PATH rejected with TARGET_TOPOLOGY_INCOMPATIBLE."""
        spec = {
            "topology": "UNDIRECTED_TREE",
            "query_target": "TREE_PATH",
            "operation": "SUM"
        }
        elim = self.solver.explain_candidate("segment_tree_standard", spec)
        self.assertIsNotNone(elim)
        self.assertEqual(elim.failure_code, "TARGET_TOPOLOGY_INCOMPATIBLE")

    def test_elim_15_order_statistics_sparse_table_rejection(self):
        """Sparse Table rejected for KTH element queries."""
        spec = {
            "operation": "KTH",
            "query_target": "LINEAR_RANGE"
        }
        elim = self.solver.explain_candidate("sparse_table", spec)
        self.assertIsNotNone(elim)
        self.assertIn(
            elim.failure_code,
            ("OPERATION_NOT_ORDER_STATISTIC", "UNSUPPORTED_AGGREGATE_OPERATION", "NON_IDEMPOTENT_OPERATION_REJECTS_SPARSE_TABLE")
        )


if __name__ == "__main__":
    unittest.main()
