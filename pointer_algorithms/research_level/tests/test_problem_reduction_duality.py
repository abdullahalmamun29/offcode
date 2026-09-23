"""
Test Suite: Pillar I — Problem Reduction & Duality
Verifies certified polynomial reductions, structured proof objects,
and fail-closed behavior on unmet preconditions.
"""

import unittest
from pointer_algorithms.research_level.reduction_engine import ReductionEngine
from pointer_algorithms.research_level.research_types import (
    EpistemicStatus,
    ReductionType,
)


class TestProblemReductionDuality(unittest.TestCase):

    def test_project_selection_finite_inf_and_closure(self):
        """Verify project selection reduction computes finite INF and valid certificate."""
        projects = [
            {"id": "P1", "profit": 10},
            {"id": "P2", "profit": 20},
            {"id": "P3", "profit": -15},
            {"id": "P4", "profit": -5},
        ]
        deps = [("P1", "P3"), ("P2", "P3"), ("P2", "P4")]

        cert = ReductionEngine.reduce_project_selection_to_min_cut(
            problem_id="PROB_PROJECT_SELECTION_01",
            requirements_hash="req_hash_123",
            projects=projects,
            dependencies=deps,
        )

        self.assertEqual(cert.status, EpistemicStatus.PROVEN)
        self.assertTrue(cert.is_valid())
        self.assertEqual(cert.reduction_type, ReductionType.PROJECT_SELECTION_TO_MIN_CUT)

        # Verify finite INF strictly dominates sum of finite capacities: 10 + 20 + 15 + 5 + 1 = 51
        inf_pred = next(p for p in cert.applicability_proof.predicates if p.predicate_name == "FINITE_INF_STRICTLY_DOMINATES_CAPACITIES")
        self.assertTrue(inf_pred.satisfied)
        self.assertEqual(inf_pred.witness_data["finite_inf"], 51)
        self.assertEqual(inf_pred.witness_data["sum_finite"], 50)

        # Verify Picard theorem obligations
        self.assertTrue(all(o.discharged for o in cert.semantic_proof.obligations))
        self.assertTrue(cert.complexity_proof.validate())

    def test_konig_bipartite_matching_to_vertex_cover_proven(self):
        """Verify König's reduction discharges when graph is verified bipartite."""
        cert = ReductionEngine.reduce_bipartite_matching_to_vertex_cover(
            problem_id="PROB_BIPARTITE_01",
            requirements_hash="req_hash_konig",
            is_bipartite=True,
            left_nodes=5,
            right_nodes=5,
            num_edges=8,
        )

        self.assertEqual(cert.status, EpistemicStatus.PROVEN)
        self.assertTrue(cert.is_valid())
        self.assertTrue(cert.applicability_proof.validate())
        self.assertTrue(cert.semantic_proof.validate())
        self.assertTrue(cert.complexity_proof.validate())

    def test_konig_bipartite_matching_fails_closed_when_not_bipartite(self):
        """Verify König's reduction fails closed to UNRESOLVED when bipartiteness is unproven."""
        cert = ReductionEngine.reduce_bipartite_matching_to_vertex_cover(
            problem_id="PROB_GENERAL_GRAPH_01",
            requirements_hash="req_hash_konig_fail",
            is_bipartite=False,
            left_nodes=0,
            right_nodes=0,
            num_edges=10,
        )

        self.assertEqual(cert.status, EpistemicStatus.UNRESOLVED)
        self.assertFalse(cert.is_valid())
        self.assertFalse(cert.applicability_proof.validate())
        self.assertFalse(cert.semantic_proof.validate())
        self.assertFalse(cert.complexity_proof.validate())

    def test_vertex_cover_to_independent_set_gallai(self):
        """Verify Gallai complement reduction from vertex cover to independent set."""
        cert = ReductionEngine.reduce_vertex_cover_to_independent_set(
            problem_id="PROB_VC_01",
            requirements_hash="req_hash_gallai",
            num_vertices=10,
        )

        self.assertEqual(cert.status, EpistemicStatus.PROVEN)
        self.assertTrue(cert.is_valid())
        self.assertEqual(cert.reduction_type, ReductionType.VERTEX_COVER_TO_INDEPENDENT_SET)
        self.assertTrue(cert.semantic_proof.validate())

    def test_vertex_cover_to_independent_set_empty_graph_fails(self):
        """Verify Gallai reduction fails when vertex universe is empty."""
        cert = ReductionEngine.reduce_vertex_cover_to_independent_set(
            problem_id="PROB_VC_EMPTY",
            requirements_hash="req_hash_gallai_empty",
            num_vertices=0,
        )

        self.assertFalse(cert.applicability_proof.validate())
        self.assertFalse(cert.is_valid())

    def test_difference_constraints_to_shortest_path(self):
        """Verify system of difference constraints reduces to shortest paths on constraint graph."""
        constraints = [
            (1, 2, 3),   # x_2 - x_1 <= 3
            (2, 3, -2),  # x_3 - x_2 <= -2
            (1, 3, 5),   # x_3 - x_1 <= 5
        ]
        cert = ReductionEngine.reduce_difference_constraints_to_shortest_path(
            problem_id="PROB_DIFF_01",
            requirements_hash="req_hash_diff",
            num_variables=3,
            constraints=constraints,
        )

        self.assertEqual(cert.status, EpistemicStatus.PROVEN)
        self.assertTrue(cert.is_valid())
        self.assertEqual(cert.backward_solution_map_name, "extract_normalized_distance_assignment")
        self.assertTrue(cert.semantic_proof.validate())

    def test_planar_dual_routing_verified_success(self):
        """Verify planar dual routing reduction when all geometric/topological prerequisites hold."""
        cert = ReductionEngine.reduce_planar_dual_routing(
            problem_id="PROB_PLANAR_01",
            requirements_hash="req_hash_planar",
            verified_planar_embedding=True,
            valid_terminal_configuration=True,
            compatible_edge_model=True,
        )

        self.assertEqual(cert.status, EpistemicStatus.PROVEN)
        self.assertTrue(cert.is_valid())
        self.assertTrue(cert.applicability_proof.validate())

    def test_planar_dual_routing_fails_closed_on_unverified_embedding(self):
        """Verify planar dual routing fails closed when embedding is not verified planar."""
        cert = ReductionEngine.reduce_planar_dual_routing(
            problem_id="PROB_NON_PLANAR",
            requirements_hash="req_hash_planar_fail",
            verified_planar_embedding=False,
            valid_terminal_configuration=True,
            compatible_edge_model=True,
        )

        self.assertEqual(cert.status, EpistemicStatus.UNRESOLVED)
        self.assertFalse(cert.is_valid())

    def test_planar_dual_routing_fails_closed_on_invalid_terminals(self):
        """Verify planar dual routing fails closed when terminals are not boundary-configured."""
        cert = ReductionEngine.reduce_planar_dual_routing(
            problem_id="PROB_INTERIOR_TERMINALS",
            requirements_hash="req_hash_planar_term_fail",
            verified_planar_embedding=True,
            valid_terminal_configuration=False,
            compatible_edge_model=True,
        )

        self.assertEqual(cert.status, EpistemicStatus.UNRESOLVED)
        self.assertFalse(cert.is_valid())

    def test_inclusion_exclusion_within_parameter_budget(self):
        """Verify PIE reduction succeeds when 2^k <= operational budget."""
        cert = ReductionEngine.reduce_complement_inclusion_exclusion(
            problem_id="PROB_PIE_10",
            requirements_hash="req_hash_pie_10",
            num_conditions=16,
            max_time_budget_operations=100_000_000,
        )

        self.assertEqual(cert.status, EpistemicStatus.PROVEN)
        self.assertTrue(cert.is_valid())
        self.assertTrue(cert.complexity_proof.validate())

    def test_inclusion_exclusion_exceeds_budget_fails_closed(self):
        """Verify PIE reduction fails closed to UNRESOLVED when 2^k exceeds operational budget."""
        cert = ReductionEngine.reduce_complement_inclusion_exclusion(
            problem_id="PROB_PIE_40",
            requirements_hash="req_hash_pie_40",
            num_conditions=40,
            max_time_budget_operations=100_000_000,
        )

        self.assertEqual(cert.status, EpistemicStatus.UNRESOLVED)
        self.assertFalse(cert.is_valid())
        self.assertFalse(cert.complexity_proof.validate())


if __name__ == "__main__":
    unittest.main()
