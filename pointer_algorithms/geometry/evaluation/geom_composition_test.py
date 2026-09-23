"""
CHUP Phase 3R — Positive Geometric Capability Composition Test Suite (8 Cases).

Validates end-to-end capability synthesis chains across geometric domains:
1. Exact Orientation Pipeline: PointSet -> __int128_t Promotion -> OrientationTurn
2. Monotone Chain Pipeline: PointSet -> Andrew's Algorithm -> ConvexHullState
3. Calipers Diameter Pipeline: PointSet -> HullCollinearPolicy -> ConvexHullState -> RotatingCalipers -> PolygonDiameter
4. Shoelace Area Pipeline: PointSet -> ConvexHull -> SimplePolygonState -> Shoelace Area
5. Boundary-First Containment: SimplePolygon -> PointQuery -> BoundaryTest -> RayCasting -> PointInPolygonResult
6. Closest Pair Metric Pipeline: MetricSpace2D -> DivideAndConquer -> StripMerge -> MinimumDistance
7. Scale-Aware Line Intersection: LinePair -> CramerDeterminants -> ScaleAwareTolerance -> UniquePoint
8. Halfplane Convex Kernel: Halfplanes -> PolarAngleSort -> DequeClipping -> BoundedConvexPolygon
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
    CoordinateDomain,
    GeometryObjective,
    HullCollinearPolicy,
    FloatingPointPolicy,
    OrientationResult,
    PointInPolygonResult,
    LineRelationshipType,
)
from pointer_algorithms.geometry.geometry_state_contracts import (
    make_point_set_state,
    make_convex_hull_state,
    make_simple_polygon_state,
    make_segment_set_state,
    make_line_pair_state,
    make_halfplane_set_state,
    make_metric_space_2d_state,
)
from pointer_algorithms.geometry.component_model import GeometryComponentRegistry
from pointer_algorithms.geometry.derivation_engine import GeometryDerivationEngine
from pointer_algorithms.geometry.verification.geometry_oracles import (
    oracle_orientation,
    oracle_convex_hull,
    oracle_polygon_area,
    oracle_point_in_polygon,
    oracle_closest_pair,
    oracle_line_intersection,
    oracle_rotating_calipers_diameter,
    oracle_halfplane_intersection,
)


class TestGeomComposition(unittest.TestCase):

    def setUp(self):
        self.engine = GeometryDerivationEngine()
        self.registry = GeometryComponentRegistry()

    def test_comp_01_orientation_pipeline(self):
        point_set = make_point_set_state(count=3, coordinate_domain="INTEGER_EXACT", max_coord=2_000_000_000)
        self.assertTrue(point_set.attributes["requires_int128"])
        model = self.engine.extract_semantic_model("Compute orientation turn of 3 points with coordinates up to 2*10^9")
        evals, sel = self.engine.evaluate_candidates(model)
        self.assertEqual(sel, "geom_orientation_cross_product")
        self.assertEqual(evals[0].correctness_guarantee, "DETERMINISTIC_EXACT")

    def test_comp_02_monotone_chain_pipeline(self):
        pts = [Point2D(0, 0), Point2D(5, 0), Point2D(5, 5), Point2D(0, 5), Point2D(2, 2)]
        hull = oracle_convex_hull(pts, HullCollinearPolicy.STRICT_VERTICES)
        self.assertEqual(len(hull), 4)
        hull_state = make_convex_hull_state(vertex_count=len(hull))
        self.assertTrue(hull_state.attributes["is_convex"])
        self.assertTrue(hull_state.attributes["cyclic_ordered"])

    def test_comp_03_calipers_diameter_pipeline(self):
        # PointSet -> HullCollinearPolicy -> ConvexHullState -> RotatingCalipers -> Diameter
        pts = [Point2D(0, 0), Point2D(6, 0), Point2D(6, 8), Point2D(0, 8), Point2D(3, 4)]
        hull = oracle_convex_hull(pts, HullCollinearPolicy.STRICT_VERTICES)
        diam = oracle_rotating_calipers_diameter(hull)
        self.assertAlmostEqual(diam, 10.0)  # Diagonal sqrt(36 + 64) = 10.0

    def test_comp_04_shoelace_area_pipeline(self):
        pts = [Point2D(0, 0), Point2D(4, 0), Point2D(4, 4), Point2D(0, 4)]
        hull = oracle_convex_hull(pts)
        hull_state = make_convex_hull_state(vertex_count=len(hull))
        poly_req = make_simple_polygon_state(vertex_count=len(hull))
        self.assertTrue(hull_state.satisfies(poly_req))
        area = oracle_polygon_area(hull)
        self.assertAlmostEqual(area, 16.0)

    def test_comp_05_boundary_first_containment_pipeline(self):
        poly = [Point2D(0, 0), Point2D(10, 0), Point2D(10, 10), Point2D(0, 10)]
        pt_b = Point2D(10, 3)
        res_b = oracle_point_in_polygon(poly, pt_b)
        self.assertEqual(res_b, PointInPolygonResult.ON_BOUNDARY)
        pt_in = Point2D(3, 3)
        res_in = oracle_point_in_polygon(poly, pt_in)
        self.assertEqual(res_in, PointInPolygonResult.INSIDE)

    def test_comp_06_closest_pair_pipeline(self):
        pts = [Point2D(0, 0), Point2D(3, 4), Point2D(10, 10), Point2D(100, 100)]
        metric_state = make_metric_space_2d_state(points_count=len(pts))
        self.assertEqual(metric_state.attributes["points_count"], 4)
        min_d = oracle_closest_pair(pts)
        self.assertAlmostEqual(min_d, 5.0)

    def test_comp_07_scale_aware_line_intersection_pipeline(self):
        # L1: 2x - y = 0, L2: x + y - 6 = 0 -> (2, 4)
        l1 = Line2D(2, -1, 0)
        l2 = Line2D(1, 1, -6)
        fp = FloatingPointPolicy()
        rel, pt = oracle_line_intersection(l1, l2, fp)
        self.assertEqual(rel, LineRelationshipType.SECANT_UNIQUE_INTERSECTION)
        self.assertIsNotNone(pt)
        self.assertAlmostEqual(pt.x, 2.0)
        self.assertAlmostEqual(pt.y, 4.0)

    def test_comp_08_halfplane_convex_kernel_pipeline(self):
        h1 = Halfplane2D(Point2D(0, 0), Point2D(1, 0))   # y >= 0
        h2 = Halfplane2D(Point2D(5, 0), Point2D(0, 1))   # x <= 5
        h3 = Halfplane2D(Point2D(5, 5), Point2D(-1, 0))  # y <= 5
        h4 = Halfplane2D(Point2D(0, 5), Point2D(0, -1))  # x >= 0
        kernel = oracle_halfplane_intersection([h1, h2, h3, h4])
        self.assertGreaterEqual(len(kernel), 4)
        area = oracle_polygon_area(kernel)
        self.assertAlmostEqual(area, 25.0, places=4)


if __name__ == "__main__":
    unittest.main()
