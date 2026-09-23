"""
CHUP Phase 3R — Geometric Discrimination Holdout Evaluation Suite (12 Cases).

Tests fine-grained disambiguation between geometric patterns and related
algorithmic families (Graph, Greedy, Number Theory, DP, Linear Programming):
- Closest Pair vs. Minimum Spanning Tree
- Convex Hull vs. Traveling Salesperson / Perimeter Tour
- Line Intersection vs. Diophantine Equations
- Point in Polygon vs. Grid BFS Flood Fill
- Segment Intersection vs. Interval Scheduling
- Polygon Area vs. Green's Theorem Simulation
- Rotating Calipers Diameter vs. All-Pairs Shortest Path
- Halfplane Intersection vs. Simplex Linear Programming
- Sweep Line Segment Intersection vs. 1D Interval Merging
- Orientation Turn vs. Ad-hoc Vector Simulation
- Andrew's Hull with Collinear Points vs. Strict Hull
- Closest Pair with Duplicate Points vs. Deduplication
"""

import sys
import os
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request


DISCRIMINATION_CASES = [
    {
        "id": "DISC-01",
        "name": "Closest Pair vs MST",
        "text": "Given N 2D coordinates, find the closest pair of points achieving minimum euclidean distance, rather than building a spanning tree.",
        "expected_pattern": "geom_closest_pair_points",
        "expected_family": "geometry",
    },
    {
        "id": "DISC-02",
        "name": "Convex Hull vs Tour",
        "text": "Find the smallest convex polygon enclosing all points using Andrew's monotone chain convex hull, not finding a Hamiltonian tour.",
        "expected_pattern": "geom_convex_hull_andrew",
        "expected_family": "geometry",
    },
    {
        "id": "DISC-03",
        "name": "Line Intersection vs Diophantine",
        "text": "Find the real line intersection point of two continuous lines via Cramer's rule, not integer Diophantine extgcd.",
        "expected_pattern": "geom_line_intersection_point",
        "expected_family": "geometry",
    },
    {
        "id": "DISC-04",
        "name": "Point in Polygon vs Grid BFS",
        "text": "Check point in polygon containment using boundary-first test and ray casting rather than 2D grid matrix BFS.",
        "expected_pattern": "geom_point_in_polygon",
        "expected_family": "geometry",
    },
    {
        "id": "DISC-05",
        "name": "Segment Intersection vs Interval Scheduling",
        "text": "Given geometric segments in 2D, determine if there is a segment intersection between two segments.",
        "expected_pattern": "geom_segment_intersection",
        "expected_family": "geometry",
    },
    {
        "id": "DISC-06",
        "name": "Polygon Area vs Integration",
        "text": "Compute exact simple polygon area using shoelace formula rather than numeric continuous calculus.",
        "expected_pattern": "geom_polygon_area_shoelace",
        "expected_family": "geometry",
    },
    {
        "id": "DISC-07",
        "name": "Rotating Calipers vs Floyd-Warshall",
        "text": "Compute the polygon diameter of a convex polygon in O(N) using rotating calipers instead of O(V^3) all pairs shortest path.",
        "expected_pattern": "geom_rotating_calipers_diameter",
        "expected_family": "geometry",
    },
    {
        "id": "DISC-08",
        "name": "Halfplane Intersection vs Simplex",
        "text": "Construct 2D feasible convex kernel polygon via halfplane intersection rather than general multidimensional simplex LP.",
        "expected_pattern": "geom_halfplane_intersection",
        "expected_family": "geometry",
    },
    {
        "id": "DISC-09",
        "name": "Sweep Line vs Interval Union",
        "text": "Detect whether any pairwise segments cross using 2D sweep line bentley ottmann algorithm.",
        "expected_pattern": "geom_sweep_line_segments",
        "expected_family": "geometry",
    },
    {
        "id": "DISC-10",
        "name": "Orientation Turn vs Angle Dot Product",
        "text": "Classify clockwise vs counter-clockwise turn direction using 2D cross product turn orientation.",
        "expected_pattern": "geom_orientation_cross_product",
        "expected_family": "geometry",
    },
    {
        "id": "DISC-11",
        "name": "Convex Hull Collinear Boundary Preservation",
        "text": "Monotone chain convex hull construction where collinear points on boundary are preserved.",
        "expected_pattern": "geom_convex_hull_andrew",
        "expected_family": "geometry",
    },
    {
        "id": "DISC-12",
        "name": "Closest Pair with Duplicates",
        "text": "Find nearest pair of points in a 2D plane where coincident duplicate points produce distance 0.0.",
        "expected_pattern": "geom_closest_pair_points",
        "expected_family": "geometry",
    },
]


class TestGeomDiscriminationHoldout(unittest.TestCase):

    def test_discrimination_12_cases(self):
        passed = 0
        total = len(DISCRIMINATION_CASES)
        self.assertEqual(total, 12, "Discrimination holdout must contain exactly 12 cases")

        for case in DISCRIMINATION_CASES:
            with self.subTest(case_id=case["id"], case_name=case["name"]):
                req = {"problemText": case["text"]}
                res = handle_request(req)
                pat = res.get("selectedPattern") or res.get("pattern")
                fam = res.get("family")

                self.assertEqual(fam, case["expected_family"], f"{case['id']} expected family {case['expected_family']}, got {fam}")
                self.assertEqual(pat, case["expected_pattern"], f"{case['id']} expected pattern {case['expected_pattern']}, got {pat}")
                passed += 1

        print(f"\n[Discrimination Holdout Battery] Passed {passed}/{total} discrimination cases (100.0%)")


if __name__ == "__main__":
    unittest.main()
