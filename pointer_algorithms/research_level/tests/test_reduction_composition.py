"""
Test Suite: Pillar I — Reduction Composition
Verifies transitive chaining P <= Q and Q <= R => P <= R,
composed complexity bounds, and fail-closed handling on invalid links.
"""

import unittest
from pointer_algorithms.research_level.reduction_engine import ReductionEngine
from pointer_algorithms.research_level.research_types import (
    EpistemicStatus,
    ReductionType,
)


class TestReductionComposition(unittest.TestCase):

    def test_valid_reduction_composition_konig_then_gallai(self):
        """Verify composing König (Matching -> VC) and Gallai (VC -> IS) yields Matching -> IS."""
        r1 = ReductionEngine.reduce_bipartite_matching_to_vertex_cover(
            problem_id="PROB_BIPARTITE_GRAPH",
            requirements_hash="req_h1",
            is_bipartite=True,
            left_nodes=4,
            right_nodes=4,
            num_edges=6,
        )

        r2 = ReductionEngine.reduce_vertex_cover_to_independent_set(
            problem_id="minimum_vertex_cover",
            requirements_hash="req_h2",
            num_vertices=8,
        )

        composed = ReductionEngine.compose_reductions(r1, r2)
        self.assertIsNotNone(composed)
        self.assertEqual(composed.reduction_type, ReductionType.COMPOSED_REDUCTION)
        self.assertEqual(composed.source_problem_id, "PROB_BIPARTITE_GRAPH")
        self.assertEqual(composed.target_family_id, "minimum_vertex_cover")
        self.assertEqual(composed.status, EpistemicStatus.PROVEN)
        self.assertTrue(composed.is_valid())

        # Check combined obligations & predicates
        self.assertGreaterEqual(len(composed.applicability_proof.predicates), 2)
        self.assertGreaterEqual(len(composed.semantic_proof.obligations), 2)
        self.assertTrue(composed.applicability_proof.validate())
        self.assertTrue(composed.semantic_proof.validate())
        self.assertTrue(composed.complexity_proof.validate())

        # Check composed transform naming
        self.assertIn("then", composed.forward_transform_name)
        self.assertIn("then", composed.backward_solution_map_name)

    def test_composition_fails_if_first_reduction_invalid(self):
        """Verify composition fails closed (returns None) if r1 is unproven/invalid."""
        r1_invalid = ReductionEngine.reduce_bipartite_matching_to_vertex_cover(
            problem_id="PROB_ODD_CYCLE",
            requirements_hash="req_h1",
            is_bipartite=False,  # Invalid
            left_nodes=0,
            right_nodes=0,
            num_edges=5,
        )

        r2_valid = ReductionEngine.reduce_vertex_cover_to_independent_set(
            problem_id="minimum_vertex_cover",
            requirements_hash="req_h2",
            num_vertices=5,
        )

        composed = ReductionEngine.compose_reductions(r1_invalid, r2_valid)
        self.assertIsNone(composed)

    def test_composition_fails_if_second_reduction_invalid(self):
        """Verify composition fails closed (returns None) if r2 is unproven/invalid."""
        r1_valid = ReductionEngine.reduce_bipartite_matching_to_vertex_cover(
            problem_id="PROB_BIPARTITE_GRAPH",
            requirements_hash="req_h1",
            is_bipartite=True,
            left_nodes=3,
            right_nodes=3,
            num_edges=4,
        )

        r2_invalid = ReductionEngine.reduce_vertex_cover_to_independent_set(
            problem_id="minimum_vertex_cover",
            requirements_hash="req_h2",
            num_vertices=0,  # Invalid empty universe
        )

        composed = ReductionEngine.compose_reductions(r1_valid, r2_invalid)
        self.assertIsNone(composed)


if __name__ == "__main__":
    unittest.main()
