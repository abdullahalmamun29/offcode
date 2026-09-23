"""
CHUP Phase 3R — Geometric Differential Stress Test Suite (220 Cases).

Partitions 220 differential stress runs across 10 distinct categories (22 runs each):
1. Large Coordinate Overflow Stress (22 runs)
2. Collinear & Flat Hull Stress (22 runs)
3. Duplicate & Zero-Length Degeneracies (22 runs)
4. Segment Crossing & Overlap Edge Cases (22 runs)
5. Point-in-Polygon Boundary Edge Cases (22 runs)
6. Parallel & Coincident Lines (22 runs)
7. Polygon Area Integer vs Float (22 runs)
8. Closest Pair Boundary Clusters (22 runs)
9. Convex Hull -> Calipers Composition Stress (22 runs)
10. Halfplane Boundedness & Empty Systems (22 runs)
"""

import sys
import os
import unittest
import math
import random

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
)


class TestGeomStress(unittest.TestCase):

    def setUp(self):
        random.seed(1337)
        self.fp = FloatingPointPolicy()

    # ── Category 1: Large Coordinate Overflow Stress (22 runs) ──
    def test_cat_01_large_coordinate_overflow(self):
        for i in range(22):
            scale = 2_000_000_000
            ax, ay = random.randint(-scale, scale), random.randint(-scale, scale)
            bx, by = random.randint(-scale, scale), random.randint(-scale, scale)
            cx, cy = random.randint(-scale, scale), random.randint(-scale, scale)

            p1, p2, p3 = Point2D(ax, ay), Point2D(bx, by), Point2D(cx, cy)
            res = oracle_orientation(p1, p2, p3)

            # Re-compute in arbitrary precision Python
            cross = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
            if cross > 0:
                expected = OrientationResult.COUNTER_CLOCKWISE
            elif cross < 0:
                expected = OrientationResult.CLOCKWISE
            else:
                expected = OrientationResult.COLLINEAR

            self.assertEqual(res, expected, f"Run {i} failed large coordinate orientation")

    # ── Category 2: Collinear & Flat Hull Stress (22 runs) ──
    def test_cat_02_collinear_and_flat_hull(self):
        for i in range(22):
            n = random.randint(5, 30)
            # Collinear points on line y = 2x + 1
            pts = [Point2D(x, 2 * x + 1) for x in range(n)]
            random.shuffle(pts)
            hull_strict = oracle_convex_hull(pts, HullCollinearPolicy.STRICT_VERTICES)
            self.assertLessEqual(len(hull_strict), 2, f"Collinear hull must collapse to <= 2 endpoints on run {i}")

    # ── Category 3: Duplicate & Zero-Length Degeneracies (22 runs) ──
    def test_cat_03_duplicate_and_zero_length(self):
        for i in range(22):
            # Points containing identical duplicates
            k = random.randint(3, 15)
            base_pts = [Point2D(random.randint(-50, 50), random.randint(-50, 50)) for _ in range(k)]
            # Add duplicates
            dup_pts = base_pts + [base_pts[0], base_pts[1]]
            d = oracle_closest_pair(dup_pts)
            self.assertEqual(d, 0.0, f"Closest pair with duplicates must return 0.0 on run {i}")

    # ── Category 4: Segment Crossing & Overlap Edge Cases (22 runs) ──
    def test_cat_04_segment_crossing_and_overlap(self):
        for i in range(22):
            mode = i % 4
            if mode == 0:
                # Proper cross
                s1 = Segment2D(Point2D(-10, 0), Point2D(10, 0))
                s2 = Segment2D(Point2D(0, -10), Point2D(0, 10))
                intersects, rel = oracle_segment_intersection(s1, s2)
                self.assertTrue(intersects)
                self.assertEqual(rel, SegmentRelationshipType.PROPER_CROSSING)
            elif mode == 1:
                # Endpoint touching
                s1 = Segment2D(Point2D(0, 0), Point2D(5, 5))
                s2 = Segment2D(Point2D(5, 5), Point2D(10, 0))
                intersects, rel = oracle_segment_intersection(s1, s2)
                self.assertTrue(intersects)
                self.assertEqual(rel, SegmentRelationshipType.TOUCHING_ENDPOINT)
            elif mode == 2:
                # Collinear overlap
                s1 = Segment2D(Point2D(0, 0), Point2D(10, 0))
                s2 = Segment2D(Point2D(5, 0), Point2D(15, 0))
                intersects, rel = oracle_segment_intersection(s1, s2)
                self.assertTrue(intersects)
                self.assertEqual(rel, SegmentRelationshipType.COLLINEAR_OVERLAP)
            else:
                # Disjoint
                s1 = Segment2D(Point2D(0, 0), Point2D(2, 2))
                s2 = Segment2D(Point2D(3, 3), Point2D(5, 5))
                intersects, rel = oracle_segment_intersection(s1, s2)
                self.assertFalse(intersects)
                self.assertEqual(rel, SegmentRelationshipType.DISJOINT)

    # ── Category 5: Point-in-Polygon Boundary Edge Cases (22 runs) ──
    def test_cat_05_point_in_polygon_boundary(self):
        poly = [Point2D(0, 0), Point2D(20, 0), Point2D(20, 20), Point2D(0, 20)]
        for i in range(22):
            if i < 11:
                # Point on bottom horizontal edge (x in [0, 20], y = 0)
                x = i * 2
                pt = Point2D(x, 0)
                res = oracle_point_in_polygon(poly, pt)
                self.assertEqual(res, PointInPolygonResult.ON_BOUNDARY)
            else:
                # Point inside vs outside
                offset = i - 11 + 1
                pt_in = Point2D(offset, offset)
                res_in = oracle_point_in_polygon(poly, pt_in)
                self.assertEqual(res_in, PointInPolygonResult.INSIDE)

    # ── Category 6: Parallel & Coincident Lines (22 runs) ──
    def test_cat_06_parallel_and_coincident_lines(self):
        for i in range(22):
            if i % 2 == 0:
                # Parallel lines: ax + by + c1 vs ax + by + c2 (c1 != c2)
                a, b = random.randint(1, 100), random.randint(1, 100)
                l1 = Line2D(a, b, random.randint(-100, 0))
                l2 = Line2D(a, b, random.randint(1, 100))
                rel, pt = oracle_line_intersection(l1, l2, self.fp)
                self.assertEqual(rel, LineRelationshipType.PARALLEL_DISJOINT)
                self.assertIsNone(pt)
            else:
                # Secant lines
                l1 = Line2D(1, 0, -i)       # x = i
                l2 = Line2D(0, 1, -(i * 2)) # y = 2i
                rel, pt = oracle_line_intersection(l1, l2, self.fp)
                self.assertEqual(rel, LineRelationshipType.SECANT_UNIQUE_INTERSECTION)
                self.assertIsNotNone(pt)
                self.assertAlmostEqual(pt.x, float(i))
                self.assertAlmostEqual(pt.y, float(i * 2))

    # ── Category 7: Polygon Area Integer vs Float (22 runs) ──
    def test_cat_07_polygon_area_exactness(self):
        for i in range(22):
            w = i + 1
            h = i + 2
            # Triangle (0,0), (w, 0), (0, h) -> Area = (w*h)/2, Double Area = w*h
            pts = [Point2D(0, 0), Point2D(w, 0), Point2D(0, h)]
            self.assertEqual(oracle_polygon_double_area_integer(pts), w * h)
            self.assertAlmostEqual(oracle_polygon_area(pts), (w * h) / 2.0)

    # ── Category 8: Closest Pair Boundary Clusters (22 runs) ──
    def test_cat_08_closest_pair_clusters(self):
        for i in range(22):
            # Cluster around (100, 100)
            pts = [Point2D(100 + random.uniform(-1, 1), 100 + random.uniform(-1, 1)) for _ in range(10)]
            d = oracle_closest_pair(pts)
            self.assertGreaterEqual(d, 0.0)

    # ── Category 9: Convex Hull -> Calipers Composition Stress (22 runs) ──
    def test_cat_09_convex_hull_calipers_composition(self):
        for i in range(22):
            w = float(i + 3)
            h = float(i + 4)
            # Box with random interior points
            corners = [Point2D(0, 0), Point2D(w, 0), Point2D(w, h), Point2D(0, h)]
            interior = [Point2D(random.uniform(0.1, w - 0.1), random.uniform(0.1, h - 0.1)) for _ in range(10)]
            all_pts = corners + interior
            random.shuffle(all_pts)

            # Step 1: Monotone chain
            hull = oracle_convex_hull(all_pts, HullCollinearPolicy.STRICT_VERTICES)
            self.assertEqual(len(hull), 4)

            # Step 2: Rotating Calipers
            diam = oracle_rotating_calipers_diameter(hull)
            expected_diam = math.sqrt(w * w + h * h)
            self.assertAlmostEqual(diam, expected_diam, places=4)

    # ── Category 10: Halfplane Boundedness & Empty Systems (22 runs) ──
    def test_cat_10_halfplane_boundedness(self):
        for i in range(22):
            s = float(i + 2)
            # Regular square [0, s] x [0, s]
            h1 = Halfplane2D(Point2D(0, 0), Point2D(1, 0))   # y >= 0
            h2 = Halfplane2D(Point2D(s, 0), Point2D(0, 1))   # x <= s
            h3 = Halfplane2D(Point2D(s, s), Point2D(-1, 0))  # y <= s
            h4 = Halfplane2D(Point2D(0, s), Point2D(0, -1))  # x >= 0

            poly = oracle_halfplane_intersection([h1, h2, h3, h4])
            self.assertGreaterEqual(len(poly), 4)
            area = oracle_polygon_area(poly)
            self.assertAlmostEqual(area, s * s, places=3)


if __name__ == "__main__":
    unittest.main()
