"""
CHUP Phase 3R — Geometric Adversarial Test Suite (16 Cases).

Stress tests edge cases, boundary perturbations, numerical precision limits,
coordinate overflows up to 2e9, and geometric degeneracies.
"""

import sys
import os
import unittest
import math

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.geometry.semantic_ontology import (
    Point2D,
    Segment2D,
    Line2D,
    Halfplane2D,
    OrientationResult,
    PointInPolygonResult,
    LineRelationshipType,
    SegmentRelationshipType,
    HullCollinearPolicy,
    FloatingPointPolicy,
)
from pointer_algorithms.geometry.derivation_engine import GeometryDerivationEngine
from pointer_algorithms.geometry.verification.geometry_oracles import (
    oracle_orientation,
    oracle_segment_intersection,
    oracle_convex_hull,
    oracle_polygon_area,
    oracle_point_in_polygon,
    oracle_closest_pair,
    oracle_line_intersection,
    oracle_rotating_calipers_diameter,
    oracle_halfplane_intersection,
    oracle_sweep_line_segments,
)


class TestGeomAdversarial(unittest.TestCase):

    def setUp(self):
        self.engine = GeometryDerivationEngine()
        self.fp = FloatingPointPolicy()

    def test_adv_01_negative_coordinate_turn(self):
        p1 = Point2D(-1_000_000, -1_000_000)
        p2 = Point2D(0, 0)
        p3 = Point2D(-1_000_000, 1_000_000)
        res = oracle_orientation(p1, p2, p3)
        self.assertEqual(res, OrientationResult.COUNTER_CLOCKWISE)

    def test_adv_02_max_coordinate_overflow_2e9(self):
        # Coordinates in [-2e9, 2e9]
        p1 = Point2D(-2_000_000_000, -2_000_000_000)
        p2 = Point2D(2_000_000_000, 2_000_000_000)
        p3 = Point2D(-2_000_000_000, 2_000_000_000)
        res = oracle_orientation(p1, p2, p3)
        self.assertEqual(res, OrientationResult.COUNTER_CLOCKWISE)

    def test_adv_03_collinear_segment_overlap(self):
        s1 = Segment2D(Point2D(0, 0), Point2D(10, 0))
        s2 = Segment2D(Point2D(5, 0), Point2D(15, 0))
        intersects, rel = oracle_segment_intersection(s1, s2)
        self.assertTrue(intersects)
        self.assertEqual(rel, SegmentRelationshipType.COLLINEAR_OVERLAP)

    def test_adv_04_segment_t_junction(self):
        s1 = Segment2D(Point2D(0, 0), Point2D(10, 0))
        s2 = Segment2D(Point2D(5, 0), Point2D(5, 5))
        intersects, rel = oracle_segment_intersection(s1, s2)
        self.assertTrue(intersects)
        self.assertEqual(rel, SegmentRelationshipType.TOUCHING_ENDPOINT)

    def test_adv_05_convex_hull_all_collinear(self):
        pts = [Point2D(i, i) for i in range(20)]
        hull = oracle_convex_hull(pts, HullCollinearPolicy.STRICT_VERTICES)
        # For collinear points, Monotone Chain collapses to the two endpoints
        self.assertLessEqual(len(hull), 2)

    def test_adv_06_convex_hull_100_duplicates(self):
        pts = [Point2D(1, 1)] * 50 + [Point2D(5, 5)] * 50
        hull = oracle_convex_hull(pts)
        self.assertEqual(len(hull), 2)

    def test_adv_07_polygon_self_intersecting_gate(self):
        model = self.engine.extract_semantic_model("Compute area of polygon with self-intersecting edges")
        model.add_derived_property("POLYGON_SELF_INTERSECTING", True, [], "TEST")
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].rejection_code, "POLYGON_SELF_INTERSECTING")

    def test_adv_08_polygon_zero_area_collinear_gate(self):
        pts = [Point2D(0, 0), Point2D(1, 1), Point2D(5, 5)]
        model = self.engine.extract_semantic_model("Calculate simple polygon area")
        evals, sel = self.engine.evaluate_candidates(model, points=pts)
        self.assertIsNone(sel)
        self.assertEqual(evals[0].rejection_code, "COLLINEAR_DEGENERATE_POLYGON")

    def test_adv_09_point_in_poly_horizontal_edge(self):
        poly = [Point2D(0, 0), Point2D(10, 0), Point2D(10, 10), Point2D(0, 10)]
        pt = Point2D(5, 0)  # Exactly on horizontal bottom edge
        self.assertEqual(oracle_point_in_polygon(poly, pt), PointInPolygonResult.ON_BOUNDARY)

    def test_adv_10_point_in_poly_vertex_hit(self):
        poly = [Point2D(0, 0), Point2D(10, 0), Point2D(10, 10), Point2D(0, 10)]
        pt = Point2D(10, 10)  # Exactly on top-right vertex
        self.assertEqual(oracle_point_in_polygon(poly, pt), PointInPolygonResult.ON_BOUNDARY)

    def test_adv_11_closest_pair_duplicate_zero_distance(self):
        # Duplicate coordinates produce d = 0.0, which is valid optimal
        pts = [Point2D(7, 3), Point2D(1, 1), Point2D(7, 3), Point2D(20, 30)]
        d = oracle_closest_pair(pts)
        self.assertEqual(d, 0.0)

    def test_adv_12_closest_pair_vertical_line(self):
        pts = [Point2D(5, 0), Point2D(5, 2), Point2D(5, 5), Point2D(5, 9)]
        d = oracle_closest_pair(pts)
        self.assertAlmostEqual(d, 2.0)

    def test_adv_13_parallel_lines_singularity_gate(self):
        l1 = Line2D(1.0, 2.0, 3.0)
        l2 = Line2D(1.0, 2.0, 7.0)
        rel, pt = oracle_line_intersection(l1, l2, self.fp)
        self.assertEqual(rel, LineRelationshipType.PARALLEL_DISJOINT)
        self.assertIsNone(pt)

    def test_adv_14_calipers_needle_rectangle(self):
        # 1000 x 0.01 rectangle
        hull = [Point2D(0, 0), Point2D(1000, 0), Point2D(1000, 0.01), Point2D(0, 0.01)]
        diam = oracle_rotating_calipers_diameter(hull)
        self.assertAlmostEqual(diam, math.sqrt(1000**2 + 0.01**2), places=3)

    def test_adv_15_halfplane_redundant_parallel(self):
        # Redundant halfplanes: x >= 0 and x >= -1
        h1 = Halfplane2D(Point2D(0, 0), Point2D(1, 0))   # y >= 0
        h2 = Halfplane2D(Point2D(4, 0), Point2D(0, 1))   # x <= 4
        h3 = Halfplane2D(Point2D(4, 4), Point2D(-1, 0))  # y <= 4
        h4 = Halfplane2D(Point2D(0, 4), Point2D(0, -1))  # x >= 0
        h_redundant = Halfplane2D(Point2D(-2, 4), Point2D(0, -1)) # x >= -2 (weaker)

        poly = oracle_halfplane_intersection([h1, h2, h3, h4, h_redundant])
        area = oracle_polygon_area(poly)
        self.assertAlmostEqual(area, 16.0, places=3)

    def test_adv_16_sweep_line_collinear_cluster(self):
        s1 = Segment2D(Point2D(0, 0), Point2D(10, 0))
        s2 = Segment2D(Point2D(2, 0), Point2D(8, 0))
        any_cross = oracle_sweep_line_segments([s1, s2])
        self.assertTrue(any_cross)


if __name__ == "__main__":
    unittest.main()
