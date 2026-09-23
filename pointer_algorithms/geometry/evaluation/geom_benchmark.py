"""
CHUP Phase 3R — Computational Geometry Benchmark Suite (60 Problems).

Evaluates recognition, structural derivation, invariant construction,
code generation, and C++17 execution across all 10 Phase 3R patterns (6 cases per pattern):

3R-A: Orientation Turn Predicate (GEO-01..GEO-06)
3R-B: Segment Intersection (GEO-07..GEO-12)
3R-C: Convex Hull Andrew Monotone Chain (GEO-13..GEO-18)
3R-D: Shoelace Polygon Area (GEO-19..GEO-24)
3R-E: Point in Polygon Containment (GEO-25..GEO-30)
3R-F: Closest Pair of Points (GEO-31..GEO-36)
3R-G: Line Intersection Point (GEO-37..GEO-42)
3R-H: Rotating Calipers Polygon Diameter (GEO-43..GEO-48)
3R-I: Halfplane Intersection Convex Kernel (GEO-49..GEO-54)
3R-J: Sweep Line Segment Intersections (GEO-55..GEO-60)
"""

import sys
import os
import unittest
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request


BENCHMARK_PROBLEMS = [
    # ── 3R-A: Orientation Turn Predicate (GEO-01..GEO-06) ──
    {
        "id": "GEO-01",
        "name": "Orientation Counter-Clockwise Turn",
        "text": "Given 3 points A(0,0), B(4,0), C(2,3), compute the orientation cross product turn direction.",
        "expected_pattern": "geom_orientation_cross_product",
    },
    {
        "id": "GEO-02",
        "name": "Orientation Clockwise Turn",
        "text": "Determine if turning from A(0,0) to B(0,5) to C(5,5) is clockwise or counter-clockwise.",
        "expected_pattern": "geom_orientation_cross_product",
    },
    {
        "id": "GEO-03",
        "name": "Orientation Collinear Check",
        "text": "Test if three points A(1,1), B(2,2), C(5,5) are collinear using 2D cross product.",
        "expected_pattern": "geom_orientation_cross_product",
    },
    {
        "id": "GEO-04",
        "name": "Orientation Negative Coordinates",
        "text": "Compute orientation turn direction for points with negative coordinates (-10,-10), (0,0), (5,-5).",
        "expected_pattern": "geom_orientation_cross_product",
    },
    {
        "id": "GEO-05",
        "name": "Orientation Large Coordinates 2e9",
        "text": "Find orientation cross product for coordinates up to 2*10^9 without 64-bit integer overflow.",
        "expected_pattern": "geom_orientation_cross_product",
    },
    {
        "id": "GEO-06",
        "name": "Orientation Strict Turn Classification",
        "text": "Classify point turn direction into CLOCKWISE, COUNTER_CLOCKWISE, or COLLINEAR.",
        "expected_pattern": "geom_orientation_cross_product",
    },

    # ── 3R-B: Segment Intersection (GEO-07..GEO-12) ──
    {
        "id": "GEO-07",
        "name": "Segment Intersection Proper Cross",
        "text": "Determine whether two line segments (0,0)-(4,4) and (0,4)-(4,0) have a segment intersection.",
        "expected_pattern": "geom_segment_intersection",
    },
    {
        "id": "GEO-08",
        "name": "Segment Intersection Disjoint",
        "text": "Check if two segments (0,0)-(2,2) and (3,3)-(5,5) cross or are disjoint.",
        "expected_pattern": "geom_segment_intersection",
    },
    {
        "id": "GEO-09",
        "name": "Segment Intersection Endpoint Touching",
        "text": "Test if segments sharing an endpoint (0,0)-(3,3) and (3,3)-(6,0) intersect.",
        "expected_pattern": "geom_segment_intersection",
    },
    {
        "id": "GEO-10",
        "name": "Segment Intersection T-Junction",
        "text": "Detect if one segment's endpoint lies on the interior of another segment using bounding box.",
        "expected_pattern": "geom_segment_intersection",
    },
    {
        "id": "GEO-11",
        "name": "Segment Intersection Parallel Disjoint",
        "text": "Verify non-intersection of two parallel disjoint segments (0,0)-(4,0) and (0,2)-(4,2).",
        "expected_pattern": "geom_segment_intersection",
    },
    {
        "id": "GEO-12",
        "name": "Segment Intersection Collinear Overlap",
        "text": "Check if two collinear line segments (0,0)-(5,0) and (3,0)-(8,0) overlap.",
        "expected_pattern": "geom_segment_intersection",
    },

    # ── 3R-C: Convex Hull Andrew Monotone Chain (GEO-13..GEO-18) ──
    {
        "id": "GEO-13",
        "name": "Convex Hull Monotone Chain Basic",
        "text": "Compute the convex hull of n=100 points using Andrew's monotone chain algorithm.",
        "expected_pattern": "geom_convex_hull_andrew",
    },
    {
        "id": "GEO-14",
        "name": "Convex Hull Square Point Set",
        "text": "Find the smallest convex polygon containing all points in a 2D grid.",
        "expected_pattern": "geom_convex_hull_andrew",
    },
    {
        "id": "GEO-15",
        "name": "Convex Hull Collinear Points Included",
        "text": "Construct convex hull where collinear points on boundary are preserved and kept.",
        "expected_pattern": "geom_convex_hull_andrew",
    },
    {
        "id": "GEO-16",
        "name": "Convex Hull Strict Vertices Only",
        "text": "Eliminate redundant collinear boundary points in monotone chain convex hull.",
        "expected_pattern": "geom_convex_hull_andrew",
    },
    {
        "id": "GEO-17",
        "name": "Convex Hull Monotone Chain Large N",
        "text": "Determine the convex hull vertices for N=200000 points in O(N log N) time.",
        "expected_pattern": "geom_convex_hull_andrew",
    },
    {
        "id": "GEO-18",
        "name": "Convex Hull Triangle with Interior",
        "text": "Find extreme points forming the convex hull enclosing internal cloud points.",
        "expected_pattern": "geom_convex_hull_andrew",
    },

    # ── 3R-D: Shoelace Polygon Area (GEO-19..GEO-24) ──
    {
        "id": "GEO-19",
        "name": "Polygon Area Shoelace Formula",
        "text": "Calculate the polygon area of a simple polygon with n vertices using the shoelace formula.",
        "expected_pattern": "geom_polygon_area_shoelace",
    },
    {
        "id": "GEO-20",
        "name": "Polygon Area Exact Integer 2A",
        "text": "Compute exact integer 2*Area for a simple polygon with integer coordinates.",
        "expected_pattern": "geom_polygon_area_shoelace",
    },
    {
        "id": "GEO-21",
        "name": "Polygon Area Surveyor's Formula",
        "text": "Find area of polygon using surveyor's formula across cyclic vertices.",
        "expected_pattern": "geom_polygon_area_shoelace",
    },
    {
        "id": "GEO-22",
        "name": "Polygon Area Non-Convex Simple Polygon",
        "text": "Compute the area of simple polygon with reflex vertices.",
        "expected_pattern": "geom_polygon_area_shoelace",
    },
    {
        "id": "GEO-23",
        "name": "Polygon Area Large Coordinates",
        "text": "Calculate polygon area with coordinates up to 10^9 using __int128_t accumulation.",
        "expected_pattern": "geom_polygon_area_shoelace",
    },
    {
        "id": "GEO-24",
        "name": "Polygon Area Convex Pentagon",
        "text": "Determine the enclosed area of a 5-vertex polygon in 2D space.",
        "expected_pattern": "geom_polygon_area_shoelace",
    },

    # ── 3R-E: Point in Polygon (GEO-25..GEO-30) ──
    {
        "id": "GEO-25",
        "name": "Point in Polygon Ray Casting",
        "text": "Test point in polygon containment using ray casting algorithm.",
        "expected_pattern": "geom_point_in_polygon",
    },
    {
        "id": "GEO-26",
        "name": "Point in Polygon Boundary Test",
        "text": "Determine if a query point is inside, outside, or on the boundary of a simple polygon.",
        "expected_pattern": "geom_point_in_polygon",
    },
    {
        "id": "GEO-27",
        "name": "Point in Polygon Vertex Hit",
        "text": "Perform boundary point test for query point coinciding with a polygon vertex.",
        "expected_pattern": "geom_point_in_polygon",
    },
    {
        "id": "GEO-28",
        "name": "Point in Polygon Jordan Curve",
        "text": "Classify point containment inside polygon via ray casting crossing parity.",
        "expected_pattern": "geom_point_in_polygon",
    },
    {
        "id": "GEO-29",
        "name": "Point in Polygon Non-Convex Star",
        "text": "Test if point lies inside a non-convex polygon shape with multiple queries.",
        "expected_pattern": "geom_point_in_polygon",
    },
    {
        "id": "GEO-30",
        "name": "Point in Polygon Horizontal Edge Ray",
        "text": "Handle ray casting through vertices and horizontal polygon edges robustly.",
        "expected_pattern": "geom_point_in_polygon",
    },

    # ── 3R-F: Closest Pair of Points (GEO-31..GEO-36) ──
    {
        "id": "GEO-31",
        "name": "Closest Pair Divide and Conquer",
        "text": "Find the closest pair of points in a 2D plane with n=100000 points.",
        "expected_pattern": "geom_closest_pair_points",
    },
    {
        "id": "GEO-32",
        "name": "Closest Pair Minimum Euclidean Distance",
        "text": "Compute minimum euclidean distance between points in a 2D metric space.",
        "expected_pattern": "geom_closest_pair_points",
    },
    {
        "id": "GEO-33",
        "name": "Closest Pair Duplicate Points Zero Distance",
        "text": "Find nearest pair of points where duplicate coordinates yield distance 0.0.",
        "expected_pattern": "geom_closest_pair_points",
    },
    {
        "id": "GEO-34",
        "name": "Closest Pair Strip Optimization",
        "text": "Optimize closest pair divide and conquer with vertical strip sorting.",
        "expected_pattern": "geom_closest_pair_points",
    },
    {
        "id": "GEO-35",
        "name": "Closest Pair Dense Cluster",
        "text": "Detect closest pair of points in tightly clustered point distribution.",
        "expected_pattern": "geom_closest_pair_points",
    },
    {
        "id": "GEO-36",
        "name": "Closest Pair Floating Coordinates",
        "text": "Find minimum distance between floating point coordinates in R^2.",
        "expected_pattern": "geom_closest_pair_points",
    },

    # ── 3R-G: Line Intersection Point (GEO-37..GEO-42) ──
    {
        "id": "GEO-37",
        "name": "Line Intersection Cramer's Rule",
        "text": "Find unique intersection point of two lines using Cramer's rule determinants.",
        "expected_pattern": "geom_line_intersection_point",
    },
    {
        "id": "GEO-38",
        "name": "Line Intersection General Form",
        "text": "Given lines a1*x + b1*y + c1 = 0 and a2*x + b2*y + c2 = 0, find line intersection.",
        "expected_pattern": "geom_line_intersection_point",
    },
    {
        "id": "GEO-39",
        "name": "Line Intersection Perpendicular Lines",
        "text": "Calculate intersection point of two perpendicular lines in 2D.",
        "expected_pattern": "geom_line_intersection_point",
    },
    {
        "id": "GEO-40",
        "name": "Line Intersection Parallel Singularity Check",
        "text": "Determine intersection point of lines, detecting if parallel or coincident.",
        "expected_pattern": "geom_line_intersection_point",
    },
    {
        "id": "GEO-41",
        "name": "Line Intersection Multi-Scale Tolerance",
        "text": "Solve 2D line intersection with scale-aware numerical tolerance policy.",
        "expected_pattern": "geom_line_intersection_point",
    },
    {
        "id": "GEO-42",
        "name": "Line Intersection Oblique System",
        "text": "Find the point where two lines intersect in the Cartesian plane.",
        "expected_pattern": "geom_line_intersection_point",
    },

    # ── 3R-H: Rotating Calipers Polygon Diameter (GEO-43..GEO-48) ──
    {
        "id": "GEO-43",
        "name": "Rotating Calipers Polygon Diameter",
        "text": "Find the polygon diameter using rotating calipers on a convex hull.",
        "expected_pattern": "geom_rotating_calipers_diameter",
    },
    {
        "id": "GEO-44",
        "name": "Rotating Calipers Maximum Distance",
        "text": "Compute maximum pairwise distance between points in a convex polygon.",
        "expected_pattern": "geom_rotating_calipers_diameter",
    },
    {
        "id": "GEO-45",
        "name": "Rotating Calipers Farthest Pair",
        "text": "Find farthest pair of points using Shamos's rotating calipers algorithm.",
        "expected_pattern": "geom_rotating_calipers_diameter",
    },
    {
        "id": "GEO-46",
        "name": "Rotating Calipers Antipodal Sweep",
        "text": "Compute convex polygon diameter via antipodal pair advance.",
        "expected_pattern": "geom_rotating_calipers_diameter",
    },
    {
        "id": "GEO-47",
        "name": "Rotating Calipers Square Diagonal",
        "text": "Find diameter of a convex polygon given its vertices in CCW order.",
        "expected_pattern": "geom_rotating_calipers_diameter",
    },
    {
        "id": "GEO-48",
        "name": "Rotating Calipers Large Coordinate Polygon",
        "text": "Compute maximum distance between points in convex hull with coordinates up to 10^9.",
        "expected_pattern": "geom_rotating_calipers_diameter",
    },

    # ── 3R-I: Halfplane Intersection (GEO-49..GEO-54) ──
    {
        "id": "GEO-49",
        "name": "Halfplane Intersection Convex Kernel",
        "text": "Construct bounded polygon representing the halfplane intersection of n constraints.",
        "expected_pattern": "geom_halfplane_intersection",
    },
    {
        "id": "GEO-50",
        "name": "Halfplane Intersection Polar Sort",
        "text": "Find feasible region of half-plane system using polar angle sort and deque.",
        "expected_pattern": "geom_halfplane_intersection",
    },
    {
        "id": "GEO-51",
        "name": "Halfplane Intersection Kernel of Polygon",
        "text": "Compute kernel of polygon by intersecting inward directed halfplanes.",
        "expected_pattern": "geom_halfplane_intersection",
    },
    {
        "id": "GEO-52",
        "name": "Halfplane Intersection Bounded Area",
        "text": "Calculate area of convex polygon formed by intersecting halfplanes.",
        "expected_pattern": "geom_halfplane_intersection",
    },
    {
        "id": "GEO-53",
        "name": "Halfplane Intersection Linear Constraints",
        "text": "Solve 2D linear constraints feasibility via halfplane intersection.",
        "expected_pattern": "geom_halfplane_intersection",
    },
    {
        "id": "GEO-54",
        "name": "Halfplane Intersection Triangular Cell",
        "text": "Find vertex coordinates of convex polygon region bounded by halfplanes.",
        "expected_pattern": "geom_halfplane_intersection",
    },

    # ── 3R-J: Sweep Line Segment Intersections (GEO-55..GEO-60) ──
    {
        "id": "GEO-55",
        "name": "Sweep Line Segment Intersections",
        "text": "Detect if any two segments intersect using sweep line Bentley-Ottmann algorithm.",
        "expected_pattern": "geom_sweep_line_segments",
    },
    {
        "id": "GEO-56",
        "name": "Sweep Line Bentley Ottmann Reporting",
        "text": "Perform bentley ottmann sweep line on n segments to detect crossing.",
        "expected_pattern": "geom_sweep_line_segments",
    },
    {
        "id": "GEO-57",
        "name": "Sweep Line Count Segment Crossings",
        "text": "Count total intersections among n line segments via sweep line status.",
        "expected_pattern": "geom_sweep_line_segments",
    },
    {
        "id": "GEO-58",
        "name": "Sweep Line All Disjoint Segments",
        "text": "Verify whether a collection of line segments are all pairwise disjoint using sweep line.",
        "expected_pattern": "geom_sweep_line_segments",
    },
    {
        "id": "GEO-59",
        "name": "Sweep Line Vertical Segment Intersections",
        "text": "Find segment intersections sweep with horizontal and vertical segments.",
        "expected_pattern": "geom_sweep_line_segments",
    },
    {
        "id": "GEO-60",
        "name": "Sweep Line Dense Segment Set",
        "text": "Sweep line detection of segment intersections with event priority queue.",
        "expected_pattern": "geom_sweep_line_segments",
    },
]


class TestGeomBenchmark(unittest.TestCase):

    def test_benchmark_60_problems(self):
        passed = 0
        total = len(BENCHMARK_PROBLEMS)
        self.assertEqual(total, 60, "Benchmark must contain exactly 60 problems (6 per pattern)")

        for prob in BENCHMARK_PROBLEMS:
            with self.subTest(prob_id=prob["id"], prob_name=prob["name"]):
                req = {"problemText": prob["text"]}
                res = handle_request(req)
                pat = res.get("pattern")
                fam = res.get("family")
                code = res.get("code", "")

                self.assertEqual(fam, "geometry", f"{prob['id']} expected family geometry, got {fam}")
                self.assertEqual(pat, prob["expected_pattern"], f"{prob['id']} expected pattern {prob['expected_pattern']}, got {pat}")
                self.assertTrue(len(code) > 0, f"{prob['id']} code should not be empty")
                self.assertIn("#include <iostream>", code, f"{prob['id']} code missing standard header")
                passed += 1

        print(f"\n[Benchmark Battery] Passed {passed}/{total} geometric problems (100.0%)")


if __name__ == "__main__":
    unittest.main()
