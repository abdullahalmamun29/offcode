"""
CHUP Phase 3R — Closed-World Geometric Gate Evaluator.

Evaluates objective-dependent precondition gates (Gates A–I).
Core Architecture V2 Principle:
    Degeneracy != Failure
    Failure = Requested objective cannot be soundly satisfied by component contract.
"""

from typing import Tuple, Optional, List
import math

from pointer_algorithms.geometry.semantic_ontology import (
    SemanticGeometryModel,
    GeometryObjective,
    FloatingPointPolicy,
    Point2D,
    Segment2D,
    Line2D,
)


class GateEvaluator:
    """
    Evaluates closed-world gates with objective-dependent criteria.
    """

    def evaluate_gates(
        self,
        model: SemanticGeometryModel,
        points: Optional[List[Point2D]] = None,
        segments: Optional[List[Segment2D]] = None,
        lines: Optional[List[Line2D]] = None,
        require_unique_point: bool = True,
        require_bounded_polygon: bool = True
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Returns (passed, rejection_code, failure_reason).
        """
        obj = model.objective
        policy = model.floating_point_policy

        # ── Gate A: Degenerate Point Set (Objective-Dependent Cardinality & Dimension) ──
        if points is not None:
            n = len(points)
            # Orientation requires exactly 3 points
            if obj == GeometryObjective.ORIENTATION_CROSS_PRODUCT and n < 3:
                return False, "DEGENERATE_POINT_SET", f"Orientation turn predicate requires exactly 3 points, observed {n}."
            # Segment requires 2 points
            if obj == GeometryObjective.SEGMENT_INTERSECTION and n < 2:
                return False, "DEGENERATE_POINT_SET", f"Segment operations require at least 2 points, observed {n}."
            # Closest pair requires at least 2 points (duplicates yield d=0.0 which is valid optimal)
            if obj == GeometryObjective.CLOSEST_PAIR_POINTS and n < 2:
                return False, "DEGENERATE_POINT_SET", f"Closest pair requires at least 2 points, observed {n}."
            # Polygon / Convex Hull / Calipers requires at least 3 points
            if obj in (GeometryObjective.CONVEX_HULL_ANDREW, GeometryObjective.POLYGON_AREA_SHOELACE,
                       GeometryObjective.POINT_IN_POLYGON, GeometryObjective.ROTATING_CALIPERS_DIAMETER) and n < 3:
                return False, "DEGENERATE_POINT_SET", f"Polygon and hull operations require at least 3 points, observed {n}."

        if model.points_count is not None:
            if obj == GeometryObjective.ORIENTATION_CROSS_PRODUCT and model.points_count < 3:
                return False, "DEGENERATE_POINT_SET", f"Orientation turn predicate requires 3 points, observed {model.points_count}."
            if obj in (GeometryObjective.CONVEX_HULL_ANDREW, GeometryObjective.POLYGON_AREA_SHOELACE,
                       GeometryObjective.POINT_IN_POLYGON, GeometryObjective.ROTATING_CALIPERS_DIAMETER) and model.points_count < 3:
                return False, "DEGENERATE_POINT_SET", f"Polygon and hull operations require at least 3 points, observed {model.points_count}."
            if obj == GeometryObjective.CLOSEST_PAIR_POINTS and model.points_count < 2:
                return False, "DEGENERATE_POINT_SET", f"Closest pair requires at least 2 points, observed {model.points_count}."

        # ── Gate B: Collinear Polygon Degeneracy ──
        if points is not None and len(points) >= 3:
            if obj in (GeometryObjective.POLYGON_AREA_SHOELACE, GeometryObjective.POINT_IN_POLYGON):
                # Check if all points are collinear
                p0, p1 = points[0], points[1]
                all_collinear = True
                for p in points[2:]:
                    cp = (p1.x - p0.x) * (p.y - p0.y) - (p1.y - p0.y) * (p.x - p0.x)
                    if not policy.approximately_zero(cp):
                        all_collinear = False
                        break
                if all_collinear:
                    return False, "COLLINEAR_DEGENERATE_POLYGON", "All vertices are collinear; degenerate 1D polygon has zero area and no interior."

        # ── Gate C: Self-Intersecting Polygon ──
        if model.has_derived_fact("POLYGON_SELF_INTERSECTING"):
            return False, "POLYGON_SELF_INTERSECTING", "Polygon has self-intersecting non-consecutive edges; simple polygon contract violated."

        # ── Gate D: Parallel / Coincident Line Singularity ──
        if lines is not None and len(lines) >= 2 and obj == GeometryObjective.LINE_INTERSECTION_POINT:
            l1, l2 = lines[0], lines[1]
            det = l1.a * l2.b - l2.a * l1.b
            scale = max(abs(l1.a), abs(l1.b)) * max(abs(l2.a), abs(l2.b))
            if policy.determinant_ambiguous(det, scale):
                # Check if coincident: a1*c2 - a2*c1 == 0 and b1*c2 - b2*c1 == 0
                det_c1 = l1.a * l2.c - l2.a * l1.c
                det_c2 = l1.b * l2.c - l2.b * l1.c
                if policy.approximately_zero(det_c1, scale) and policy.approximately_zero(det_c2, scale):
                    return False, "COINCIDENT_LINES_INFINITE_INTERSECTIONS", "Lines are coincident; infinite intersection points exist."
                return False, "PARALLEL_LINES_NO_UNIQUE_INTERSECTION", "Lines are parallel and disjoint; no unique intersection point exists."

        # ── Gate E: Collinear Segment Point Ambiguity ──
        if segments is not None and len(segments) >= 2 and require_unique_point:
            s1, s2 = segments[0], segments[1]
            if model.has_derived_fact("SEGMENTS_COLLINEAR_OVERLAPPING"):
                return False, "COLLINEAR_SEGMENT_AMBIGUOUS_POINT", "Collinear segments overlap on an interval; no unique intersection point exists."

        # ── Gate F & G: Halfplane Feasibility and Boundedness ──
        if obj == GeometryObjective.HALFPLANE_INTERSECTION:
            if model.has_derived_fact("HALFPLANE_INTERSECTION_EMPTY"):
                return False, "HALFPLANE_INTERSECTION_EMPTY", "Halfplane system is infeasible; intersection region is empty."
            if model.has_derived_fact("HALFPLANE_INTERSECTION_UNBOUNDED") and require_bounded_polygon:
                return False, "HALFPLANE_INTERSECTION_UNBOUNDED", "Halfplane intersection region is unbounded; cannot emit finite convex polygon."

        # ── Gate H: Division by Zero in Geometric Inversion ──
        if model.has_derived_fact("GEOMETRIC_ZERO_VECTOR_NORMALIZATION"):
            return False, "GEOMETRIC_ZERO_DIVISION", "Attempted vector normalization or projection on zero-length direction vector."

        # ── Gate I: Floating-Point Tolerance Violation ──
        if model.has_derived_fact("NUMERICAL_TOLERANCE_VIOLATED"):
            return False, "FLOATING_POINT_TOLERANCE_EXCEEDED", "Numerical pivot or determinant falls within multi-scale ambiguity threshold."

        return True, None, None
