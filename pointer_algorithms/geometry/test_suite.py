"""
CHUP Phase 3R — Computational Geometry Unit Test Suite.

Comprehensive 26-test suite verifying:
- All 10 canonical geometric patterns
- Exact __int128_t arithmetic bounds and overflow prevention
- Multi-scale FloatingPointPolicy and scale-aware predicates
- Objective-dependent Gates A through I
- Convex hull collinear policies (STRICT_VERTICES vs KEEP_BOUNDARY_POINTS)
- Deterministic boundary-first point-in-polygon containment
- Closest pair duplicate point semantics (d = 0.0 is valid optimal)
- State contracts, component registry, and provenance tracking
- C++17 generator compilation readiness
"""

import unittest
import math

from pointer_algorithms.geometry.semantic_ontology import (
    Point2D,
    Segment2D,
    Line2D,
    Halfplane2D,
    CoordinateDomain,
    GeometryObjective,
    HullCollinearPolicy,
    SweepLineObjective,
    FloatingPointPolicy,
    OrientationResult,
    PointInPolygonResult,
    LineRelationshipType,
    SegmentRelationshipType,
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
from pointer_algorithms.geometry.derivation.candidate_evaluator import CandidateStatus, SelectionStatus
from pointer_algorithms.geometry.verification.geometry_oracles import (
    oracle_orientation,
    oracle_segment_intersection,
    oracle_convex_hull,
    oracle_polygon_area,
    oracle_polygon_double_area_integer,
    oracle_point_in_polygon,
    oracle_closest_pair,
    oracle_line_intersection,
    oracle_rotating_calipers_diameter,
    oracle_halfplane_intersection,
    oracle_sweep_line_segments,
)
from pointer_algorithms.generator.geometry_cpp_generator import generate_geometry_cpp


class TestGeometryPhase3R(unittest.TestCase):

    def setUp(self):
        self.engine = GeometryDerivationEngine()
        self.registry = GeometryComponentRegistry()
        self.fp_policy = FloatingPointPolicy()

    # ── Test 1: Orientation Predicate Exact Integer (3R-A) ──
    def test_01_orientation_exact_integer(self):
        p1 = Point2D(0, 0)
        p2 = Point2D(4, 4)
        p3_left = Point2D(0, 4)
        p3_right = Point2D(4, 0)
        p3_collinear = Point2D(8, 8)

        self.assertEqual(oracle_orientation(p1, p2, p3_left), OrientationResult.COUNTER_CLOCKWISE)
        self.assertEqual(oracle_orientation(p1, p2, p3_right), OrientationResult.CLOCKWISE)
        self.assertEqual(oracle_orientation(p1, p2, p3_collinear), OrientationResult.COLLINEAR)

    # ── Test 2: Large Coordinate Overflow Safety (2e9) ──
    def test_02_large_coordinate_overflow_bounds(self):
        # Coordinates in [-2e9, 2e9]. Determinant can reach 3.2e19, exceeding signed 64-bit max (~9.22e18).
        # We test that our int128 promotion logic is certified.
        text = "Check orientation of 3 points with coordinates up to 2*10^9"
        model = self.engine.extract_semantic_model(text)
        self.assertTrue(model.has_derived_fact("INT128_PROMOTION_CERTIFIED"))
        self.assertEqual(model.coordinate_domain, CoordinateDomain.INTEGER_EXACT)

        # Direct arithmetic test in Python (which has arbitrary precision) simulating __int128_t
        p1 = Point2D(-2_000_000_000, -2_000_000_000)
        p2 = Point2D(2_000_000_000, 2_000_000_000)
        p3 = Point2D(-2_000_000_000, 2_000_000_000)
        res = oracle_orientation(p1, p2, p3)
        self.assertEqual(res, OrientationResult.COUNTER_CLOCKWISE)

    # ── Test 3: Segment Intersection Proper Crossing (3R-B) ──
    def test_03_segment_intersection_proper(self):
        s1 = Segment2D(Point2D(0, 0), Point2D(4, 4))
        s2 = Segment2D(Point2D(0, 4), Point2D(4, 0))
        intersects, rel = oracle_segment_intersection(s1, s2)
        self.assertTrue(intersects)
        self.assertEqual(rel, SegmentRelationshipType.PROPER_CROSSING)

    # ── Test 4: Segment Intersection Touching Endpoints & Disjoint ──
    def test_04_segment_intersection_touching_and_disjoint(self):
        s1 = Segment2D(Point2D(0, 0), Point2D(2, 2))
        s2 = Segment2D(Point2D(2, 2), Point2D(4, 0))  # Touches at (2, 2)
        intersects, rel = oracle_segment_intersection(s1, s2)
        self.assertTrue(intersects)
        self.assertEqual(rel, SegmentRelationshipType.TOUCHING_ENDPOINT)

        s3 = Segment2D(Point2D(5, 5), Point2D(6, 6))  # Disjoint
        intersects, rel = oracle_segment_intersection(s1, s3)
        self.assertFalse(intersects)
        self.assertEqual(rel, SegmentRelationshipType.DISJOINT)

    # ── Test 5: Andrew's Monotone Chain Convex Hull (3R-C) ──
    def test_05_convex_hull_strict(self):
        pts = [
            Point2D(0, 0), Point2D(2, 0), Point2D(4, 0),
            Point2D(4, 4), Point2D(2, 4), Point2D(0, 4),
            Point2D(2, 2)  # Interior point
        ]
        hull = oracle_convex_hull(pts, policy=HullCollinearPolicy.STRICT_VERTICES)
        # Strict hull should eliminate (2, 0) and (2, 4) and (2, 2), leaving 4 corners
        self.assertEqual(len(hull), 4)
        hull_coords = {(p.x, p.y) for p in hull}
        expected = {(0, 0), (4, 0), (4, 4), (0, 4)}
        self.assertEqual(hull_coords, expected)

    # ── Test 6: Convex Hull Keep Boundary Points Policy ──
    def test_06_convex_hull_keep_collinear(self):
        pts = [
            Point2D(0, 0), Point2D(2, 0), Point2D(4, 0),
            Point2D(4, 4), Point2D(2, 4), Point2D(0, 4),
            Point2D(2, 2)  # Interior
        ]
        hull = oracle_convex_hull(pts, policy=HullCollinearPolicy.KEEP_BOUNDARY_POINTS)
        # Non-strict hull should preserve collinear perimeter points (2, 0) and (2, 4)
        self.assertEqual(len(hull), 6)
        self.assertNotIn((2, 2), {(p.x, p.y) for p in hull})

    # ── Test 7: Shoelace Polygon Area Exact Integer & Float (3R-D) ──
    def test_07_shoelace_polygon_area(self):
        # Triangle (0,0), (5,0), (0,6) -> Area = 15.0, Double Area = 30
        pts = [Point2D(0, 0), Point2D(5, 0), Point2D(0, 6)]
        self.assertAlmostEqual(oracle_polygon_area(pts), 15.0)
        self.assertEqual(oracle_polygon_double_area_integer(pts), 30)

    # ── Test 8: Point in Polygon Deterministic Boundary-First (3R-E) ──
    def test_08_point_in_polygon_boundary_first(self):
        poly = [Point2D(0, 0), Point2D(10, 0), Point2D(10, 10), Point2D(0, 10)]
        pt_inside = Point2D(5, 5)
        pt_outside = Point2D(15, 5)
        pt_boundary = Point2D(10, 5)  # Exactly on right edge
        pt_vertex = Point2D(0, 0)     # Exactly on vertex

        self.assertEqual(oracle_point_in_polygon(poly, pt_inside), PointInPolygonResult.INSIDE)
        self.assertEqual(oracle_point_in_polygon(poly, pt_outside), PointInPolygonResult.OUTSIDE)
        self.assertEqual(oracle_point_in_polygon(poly, pt_boundary), PointInPolygonResult.ON_BOUNDARY)
        self.assertEqual(oracle_point_in_polygon(poly, pt_vertex), PointInPolygonResult.ON_BOUNDARY)

    # ── Test 9: Closest Pair of Points (3R-F) ──
    def test_09_closest_pair_distinct(self):
        pts = [Point2D(0, 0), Point2D(1, 1), Point2D(10, 10), Point2D(20, 20)]
        d = oracle_closest_pair(pts)
        self.assertAlmostEqual(d, math.sqrt(2.0))

    # ── Test 10: Closest Pair Duplicate Point Semantics (d = 0.0) ──
    def test_10_closest_pair_duplicate_semantics(self):
        # If duplicate points exist, d = 0.0 is valid optimal result, NOT a degeneracy failure
        pts = [Point2D(5, 5), Point2D(1, 2), Point2D(5, 5), Point2D(9, 9)]
        d = oracle_closest_pair(pts)
        self.assertEqual(d, 0.0)

    # ── Test 11: Line Intersection via Cramer's Rule (3R-G) ──
    def test_11_line_intersection_secant(self):
        # L1: x - y = 0 -> (1, -1, 0)
        # L2: x + y - 4 = 0 -> (1, 1, -4)
        l1 = Line2D(1, -1, 0)
        l2 = Line2D(1, 1, -4)
        rel, pt = oracle_line_intersection(l1, l2, self.fp_policy)
        self.assertEqual(rel, LineRelationshipType.SECANT_UNIQUE_INTERSECTION)
        self.assertIsNotNone(pt)
        self.assertAlmostEqual(pt.x, 2.0)
        self.assertAlmostEqual(pt.y, 2.0)

    # ── Test 12: Parallel and Coincident Line Singularity Gating ──
    def test_12_line_intersection_parallel_coincident(self):
        # Parallel: x + y = 0 vs x + y - 5 = 0
        l1 = Line2D(1, 1, 0)
        l2 = Line2D(1, 1, -5)
        rel_par, pt_par = oracle_line_intersection(l1, l2, self.fp_policy)
        self.assertEqual(rel_par, LineRelationshipType.PARALLEL_DISJOINT)
        self.assertIsNone(pt_par)

        # Coincident: 2x + 2y - 10 = 0 vs x + y - 5 = 0
        l3 = Line2D(2, 2, -10)
        rel_coin, pt_coin = oracle_line_intersection(l2, l3, self.fp_policy)
        self.assertEqual(rel_coin, LineRelationshipType.COINCIDENT_IDENTICAL)
        self.assertIsNone(pt_coin)

    # ── Test 13: Rotating Calipers Polygon Diameter (3R-H) ──
    def test_13_rotating_calipers_diameter(self):
        # Rectangle [0, 4] x [0, 3] -> Diameter is diagonal = sqrt(16 + 9) = 5.0
        hull = [Point2D(0, 0), Point2D(4, 0), Point2D(4, 3), Point2D(0, 3)]
        diam = oracle_rotating_calipers_diameter(hull)
        self.assertAlmostEqual(diam, 5.0)

    # ── Test 14: Halfplane Intersection Bounded Kernel (3R-I) ──
    def test_14_halfplane_intersection_box(self):
        # 4 bounding halfplanes forming [0, 2] x [0, 2]
        # x >= 0: p=(0,0), d=(0,1)
        # y >= 0: p=(0,0), d=(1,0) (wait, left of d: for y>=0, line x-axis from (0,0) with d=(1,0), left is +y)
        # x <= 2: line x=2 from (2,2) with d=(0,-1), left is x <= 2
        # y <= 2: line y=2 from (2,2) with d=(-1,0), left is y <= 2
        h1 = Halfplane2D(Point2D(0, 0), Point2D(1, 0))   # y >= 0
        h2 = Halfplane2D(Point2D(2, 0), Point2D(0, 1))   # x <= 2
        h3 = Halfplane2D(Point2D(2, 2), Point2D(-1, 0))  # y <= 2
        h4 = Halfplane2D(Point2D(0, 2), Point2D(0, -1))  # x >= 0

        poly = oracle_halfplane_intersection([h1, h2, h3, h4])
        self.assertGreaterEqual(len(poly), 4)
        area = oracle_polygon_area(poly)
        self.assertAlmostEqual(area, 4.0, places=4)

    # ── Test 15: Sweep Line Segment Intersections (3R-J) ──
    def test_15_sweep_line_segments(self):
        s1 = Segment2D(Point2D(0, 0), Point2D(2, 2))
        s2 = Segment2D(Point2D(0, 2), Point2D(2, 0))
        s3 = Segment2D(Point2D(10, 10), Point2D(12, 12))

        any_cross = oracle_sweep_line_segments([s1, s2, s3], SweepLineObjective.EXISTENCE)
        self.assertTrue(any_cross)

        count = oracle_sweep_line_segments([s1, s2, s3], SweepLineObjective.COUNT)
        self.assertEqual(count, 1)

    # ── Test 16: Gate A — Degenerate Point Set (Cardinality Shortfall) ──
    def test_16_gate_a_cardinality_shortfall(self):
        model = self.engine.extract_semantic_model("Compute orientation of 2 points")
        passed, rej, reason = self.engine.gate_evaluator.evaluate_gates(model, points=[Point2D(0, 0), Point2D(1, 1)])
        self.assertFalse(passed)
        self.assertEqual(rej, "DEGENERATE_POINT_SET")

    # ── Test 17: Gate B — Collinear Polygon Degeneracy ──
    def test_17_gate_b_collinear_polygon(self):
        model = self.engine.extract_semantic_model("Compute polygon area via shoelace formula")
        collinear_pts = [Point2D(0, 0), Point2D(1, 1), Point2D(2, 2), Point2D(3, 3)]
        passed, rej, reason = self.engine.gate_evaluator.evaluate_gates(model, points=collinear_pts)
        self.assertFalse(passed)
        self.assertEqual(rej, "COLLINEAR_DEGENERATE_POLYGON")

    # ── Test 18: Gate D — Parallel / Coincident Line Singularities ──
    def test_18_gate_d_parallel_line_singularity(self):
        model = self.engine.extract_semantic_model("Find unique intersection point of two parallel lines")
        l1 = Line2D(1, 2, 3)
        l2 = Line2D(1, 2, 7)  # Parallel
        passed, rej, reason = self.engine.gate_evaluator.evaluate_gates(model, lines=[l1, l2])
        self.assertFalse(passed)
        self.assertEqual(rej, "PARALLEL_LINES_NO_UNIQUE_INTERSECTION")

    # ── Test 19: Gate E — Collinear Segment Point Ambiguity ──
    def test_19_gate_e_collinear_segment_overlap(self):
        model = self.engine.extract_semantic_model("Find unique intersection point of two segments")
        model.add_derived_property("SEGMENTS_COLLINEAR_OVERLAPPING", True, [], "TEST")
        s1 = Segment2D(Point2D(0, 0), Point2D(4, 0))
        s2 = Segment2D(Point2D(2, 0), Point2D(6, 0))
        passed, rej, reason = self.engine.gate_evaluator.evaluate_gates(model, segments=[s1, s2], require_unique_point=True)
        self.assertFalse(passed)
        self.assertEqual(rej, "COLLINEAR_SEGMENT_AMBIGUOUS_POINT")

    # ── Test 20: Gate F & G — Halfplane Empty and Unbounded Gating ──
    def test_20_gate_f_and_g_halfplane_gating(self):
        model = self.engine.extract_semantic_model("Construct bounded polygon kernel from halfplanes")
        model.add_derived_property("HALFPLANE_INTERSECTION_EMPTY", True, [], "TEST")
        passed, rej, reason = self.engine.gate_evaluator.evaluate_gates(model)
        self.assertFalse(passed)
        self.assertEqual(rej, "HALFPLANE_INTERSECTION_EMPTY")

        model2 = self.engine.extract_semantic_model("Construct bounded polygon kernel from halfplanes")
        model2.add_derived_property("HALFPLANE_INTERSECTION_UNBOUNDED", True, [], "TEST")
        passed2, rej2, reason2 = self.engine.gate_evaluator.evaluate_gates(model2, require_bounded_polygon=True)
        self.assertFalse(passed2)
        self.assertEqual(rej2, "HALFPLANE_INTERSECTION_UNBOUNDED")

    # ── Test 21: Gate I — Scale-Aware Floating-Point Ambiguity ──
    def test_21_gate_i_scale_aware_tolerance(self):
        fp = FloatingPointPolicy(abs_epsilon=1e-9, rel_epsilon=1e-9)
        # On small scale 1.0, 1e-8 is not zero
        self.assertFalse(fp.approximately_zero(1e-8, scale=1.0))
        # On large scale 1e8, 1e-8 is within tolerance (1e-9 + 1e-9*1e8 = 0.100000001)
        self.assertTrue(fp.approximately_zero(1e-8, scale=1e8))

    # ── Test 22: State Contracts Subtyping & Satisfaction ──
    def test_22_state_contracts_subtyping(self):
        hull_state = make_convex_hull_state(vertex_count=5)
        simple_poly_req = make_simple_polygon_state(vertex_count=5)
        # ConvexHullState has supertype SimplePolygonState
        self.assertTrue(hull_state.satisfies(simple_poly_req))

    # ── Test 23: Component Registry & Provider Capabilities ──
    def test_23_component_registry_capabilities(self):
        comp = self.registry.get("convex_hull_monotone_chain")
        self.assertIsNotNone(comp)
        self.assertIn("CONVEX_HULL", comp.provided_capabilities)

        providers = self.registry.find_providers("CONVEX_HULL")
        self.assertEqual(len(providers), 1)
        self.assertEqual(providers[0].name, "convex_hull_monotone_chain")

    # ── Test 24: Candidate Evaluator Optimal Selection & Rejection ──
    def test_24_candidate_evaluator_selection(self):
        text = "Find minimum distance between any pair of points in a 2D plane with n=100000"
        model = self.engine.extract_semantic_model(text)
        evals, selected = self.engine.evaluate_candidates(model)
        self.assertEqual(selected, "geom_closest_pair_points")
        self.assertTrue(any(e.status == CandidateStatus.VALID_OPTIMAL and e.selection == SelectionStatus.SELECTED for e in evals))
        # Suboptimal brute force should be evaluated as COMPLEXITY_REQUIREMENT_UNSATISFIED
        self.assertTrue(any(e.status == CandidateStatus.COMPLEXITY_REQUIREMENT_UNSATISFIED for e in evals))

    # ── Test 25: Composition Convex Hull -> Rotating Calipers Diameter ──
    def test_25_convex_hull_to_calipers_composition(self):
        # Starting with un-ordered, non-convex point set containing interior points
        pts = [
            Point2D(0, 0), Point2D(4, 0), Point2D(4, 3), Point2D(0, 3),
            Point2D(2, 1), Point2D(1, 2)  # Interior points
        ]
        # Step 1: Andrew's monotone chain produces ConvexHullState
        hull = oracle_convex_hull(pts, HullCollinearPolicy.STRICT_VERTICES)
        self.assertEqual(len(hull), 4)
        # Step 2: Calipers takes ConvexHullState and computes diameter
        diam = oracle_rotating_calipers_diameter(hull)
        self.assertAlmostEqual(diam, 5.0)

    # ── Test 26: C++17 Generator Code Emission for All 10 Patterns ──
    def test_26_cpp_generator_all_patterns(self):
        patterns = [
            "geom_orientation_cross_product",
            "geom_segment_intersection",
            "geom_convex_hull_andrew",
            "geom_polygon_area_shoelace",
            "geom_point_in_polygon",
            "geom_closest_pair_points",
            "geom_line_intersection_point",
            "geom_rotating_calipers_diameter",
            "geom_halfplane_intersection",
            "geom_sweep_line_segments",
        ]
        for pat in patterns:
            code = generate_geometry_cpp(pat)
            self.assertIn("#include <iostream>", code, f"Pattern {pat} failed basic C++ header test")
            self.assertIn("int main()", code, f"Pattern {pat} missing main function")


if __name__ == "__main__":
    unittest.main()
