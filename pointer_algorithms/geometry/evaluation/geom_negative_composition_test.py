"""
CHUP Phase 3R — Negative Closed-World Composition Test Suite (6 Cases).

Verifies strict closed-world rejection and exact gate diagnostics:
1. Gate A: Orientation Turn with N < 3 points -> DEGENERATE_POINT_SET
2. Gate B: Collinear Polygon Vertices for Area -> COLLINEAR_DEGENERATE_POLYGON
3. Gate D: Parallel Disjoint Lines for Unique Point -> PARALLEL_LINES_NO_UNIQUE_INTERSECTION
4. Gate D: Coincident Lines for Unique Point -> COINCIDENT_LINES_INFINITE_INTERSECTIONS
5. Gate F: Infeasible Halfplane System -> HALFPLANE_INTERSECTION_EMPTY
6. Gate G: Unbounded Halfplane Feasible Region -> HALFPLANE_INTERSECTION_UNBOUNDED
"""

import sys
import os
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.geometry.semantic_ontology import (
    Point2D,
    Line2D,
    GeometryObjective,
)
from pointer_algorithms.geometry.derivation_engine import GeometryDerivationEngine
from pointer_algorithms.geometry.derivation.candidate_evaluator import CandidateStatus, SelectionStatus


class TestGeomNegativeComposition(unittest.TestCase):

    def setUp(self):
        self.engine = GeometryDerivationEngine()

    def test_neg_01_cardinality_shortfall(self):
        model = self.engine.extract_semantic_model("Compute orientation turn of 2 points")
        evals, sel = self.engine.evaluate_candidates(model, points=[Point2D(0, 0), Point2D(1, 1)])
        self.assertIsNone(sel)
        self.assertEqual(evals[0].status, CandidateStatus.INVALID_PRECONDITION)
        self.assertEqual(evals[0].rejection_code, "DEGENERATE_POINT_SET")

    def test_neg_02_collinear_polygon_degeneracy(self):
        model = self.engine.extract_semantic_model("Compute polygon area via shoelace formula")
        collinear_pts = [Point2D(0, 0), Point2D(2, 2), Point2D(4, 4), Point2D(6, 6)]
        evals, sel = self.engine.evaluate_candidates(model, points=collinear_pts)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].status, CandidateStatus.INVALID_PRECONDITION)
        self.assertEqual(evals[0].rejection_code, "COLLINEAR_DEGENERATE_POLYGON")

    def test_neg_03_parallel_lines_singularity(self):
        model = self.engine.extract_semantic_model("Find intersection point of two parallel lines")
        l1 = Line2D(1, 2, 5)
        l2 = Line2D(1, 2, 9)
        evals, sel = self.engine.evaluate_candidates(model, lines=[l1, l2])
        self.assertIsNone(sel)
        self.assertEqual(evals[0].status, CandidateStatus.INVALID_PRECONDITION)
        self.assertEqual(evals[0].rejection_code, "PARALLEL_LINES_NO_UNIQUE_INTERSECTION")

    def test_neg_04_coincident_lines_singularity(self):
        model = self.engine.extract_semantic_model("Find intersection point of two coincident lines")
        l1 = Line2D(1, 2, 5)
        l2 = Line2D(2, 4, 10)  # Identical line
        evals, sel = self.engine.evaluate_candidates(model, lines=[l1, l2])
        self.assertIsNone(sel)
        self.assertEqual(evals[0].status, CandidateStatus.INVALID_PRECONDITION)
        self.assertEqual(evals[0].rejection_code, "COINCIDENT_LINES_INFINITE_INTERSECTIONS")

    def test_neg_05_halfplane_empty_system(self):
        model = self.engine.extract_semantic_model("Construct convex kernel from halfplanes")
        model.add_derived_property("HALFPLANE_INTERSECTION_EMPTY", True, [], "TEST")
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].status, CandidateStatus.INVALID_PRECONDITION)
        self.assertEqual(evals[0].rejection_code, "HALFPLANE_INTERSECTION_EMPTY")

    def test_neg_06_halfplane_unbounded_system(self):
        model = self.engine.extract_semantic_model("Construct convex kernel from halfplanes")
        model.add_derived_property("HALFPLANE_INTERSECTION_UNBOUNDED", True, [], "TEST")
        evals, sel = self.engine.evaluate_candidates(model, require_bounded_polygon=True)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].status, CandidateStatus.INVALID_PRECONDITION)
        self.assertEqual(evals[0].rejection_code, "HALFPLANE_INTERSECTION_UNBOUNDED")


if __name__ == "__main__":
    unittest.main()
