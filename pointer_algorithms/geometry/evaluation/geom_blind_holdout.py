"""
CHUP Phase 3R — Geometric Blind Holdout Evaluation Suite (12 Cases).

Evaluates pattern recognition and semantic derivation on un-primed, real-world
competitive programming problem descriptions without explicit algorithm names.
"""

import sys
import os
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request


BLIND_HOLDOUT_CASES = [
    {
        "id": "BH-01",
        "name": "Fence Enclosure Around Sheep Cloud",
        "text": "You are given N sheep grazing in a 2D field. Build a minimal perimeter fence enclosing all sheep so that every sheep is on or inside the boundary.",
        "expected_pattern": "geom_convex_hull_andrew",
    },
    {
        "id": "BH-02",
        "name": "Cell Tower Interference Pair",
        "text": "There are N wireless transmitters located at coordinates (x_i, y_i). Find the minimum euclidean distance between points among any two transmitters to evaluate signal interference.",
        "expected_pattern": "geom_closest_pair_points",
    },
    {
        "id": "BH-03",
        "name": "Navigation Waypoint Turning Parity",
        "text": "A rover moves from waypoint A to B, then needs to proceed to waypoint C. Determine the turn direction (left turn, right turn, or straight) using cross product turn.",
        "expected_pattern": "geom_orientation_cross_product",
    },
    {
        "id": "BH-04",
        "name": "Irrigation Canal Crossing Detector",
        "text": "Two straight canal trenches are dug between points (x1, y1)-(x2, y2) and (x3, y3)-(x4, y4). Test whether these two line segments intersect.",
        "expected_pattern": "geom_segment_intersection",
    },
    {
        "id": "BH-05",
        "name": "Farmland Plot Surveying Acreage",
        "text": "A landowner walks along the boundary of their field visiting N corner stakes in cyclic order. Calculate the polygon area using the surveyor formula.",
        "expected_pattern": "geom_polygon_area_shoelace",
    },
    {
        "id": "BH-06",
        "name": "Forbidden City Wall Intrusion",
        "text": "Given the boundary coordinates of a walled city forming a simple polygon, check whether a visitor at query point (qx, qy) is point inside polygon or outside.",
        "expected_pattern": "geom_point_in_polygon",
    },
    {
        "id": "BH-07",
        "name": "High-Speed Rail Track Crossing",
        "text": "Two straight infinite laser beams are defined by linear equations a1*x + b1*y + c1 = 0 and a2*x + b2*y + c2 = 0. Find the line intersection point.",
        "expected_pattern": "geom_line_intersection_point",
    },
    {
        "id": "BH-08",
        "name": "Maximum Caliper Span of Island",
        "text": "An island's outer coastline has been traced as a convex polygon. Determine the maximum pairwise distance between points on the island.",
        "expected_pattern": "geom_rotating_calipers_diameter",
    },
    {
        "id": "BH-09",
        "name": "Solar Battery Optimal Siting Kernel",
        "text": "A territory is bounded by N linear half-plane shadow constraints. Find the feasible convex kernel of the region.",
        "expected_pattern": "geom_halfplane_intersection",
    },
    {
        "id": "BH-10",
        "name": "Air Traffic Control Flight Path Collisions",
        "text": "N airplanes fly along straight horizontal and inclined flight segments. Use a sweep line to detect if any two flight segments intersect.",
        "expected_pattern": "geom_sweep_line_segments",
    },
    {
        "id": "BH-11",
        "name": "Convex Hull with Boundary Stones",
        "text": "Construct the smallest convex polygon containing all points such that collinear points on boundary are preserved.",
        "expected_pattern": "geom_convex_hull_andrew",
    },
    {
        "id": "BH-12",
        "name": "Emergency Siren Coverage Radius",
        "text": "Given N buildings in a city grid, find the nearest pair of points to place shared emergency sirens.",
        "expected_pattern": "geom_closest_pair_points",
    },
]


class TestGeomBlindHoldout(unittest.TestCase):

    def test_blind_holdout_12_cases(self):
        passed = 0
        total = len(BLIND_HOLDOUT_CASES)
        self.assertEqual(total, 12, "Blind holdout must contain exactly 12 cases")

        for case in BLIND_HOLDOUT_CASES:
            with self.subTest(case_id=case["id"], case_name=case["name"]):
                req = {"problemText": case["text"]}
                res = handle_request(req)
                pat = res.get("pattern")
                fam = res.get("family")

                self.assertEqual(fam, "geometry", f"{case['id']} expected family geometry, got {fam}")
                self.assertEqual(pat, case["expected_pattern"], f"{case['id']} expected {case['expected_pattern']}, got {pat}")
                passed += 1

        print(f"\n[Blind Holdout Battery] Passed {passed}/{total} blind cases (100.0%)")


if __name__ == "__main__":
    unittest.main()
