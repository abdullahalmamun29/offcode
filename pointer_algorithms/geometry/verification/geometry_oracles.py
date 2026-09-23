"""
CHUP Phase 3R — Pure Python Reference Geometry Oracles.

Exact and robust reference implementations for all 10 canonical geometry patterns.
Used for differential testing, property validation, and stress benchmarks.
"""

from typing import List, Tuple, Optional, Union
import math

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
    SweepLineObjective,
    FloatingPointPolicy,
)


# ── 1. Orientation Turn Predicate (3R-A) ──

def oracle_orientation(
    p1: Point2D,
    p2: Point2D,
    p3: Point2D,
    policy: Optional[FloatingPointPolicy] = None
) -> OrientationResult:
    """
    Computes (p2 - p1) x (p3 - p1).
    Positive -> COUNTER_CLOCKWISE (left turn)
    Negative -> CLOCKWISE (right turn)
    Zero     -> COLLINEAR
    """
    cp = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
    if policy is not None:
        scale = max(abs(p2.x - p1.x), abs(p2.y - p1.y)) * max(abs(p3.x - p1.x), abs(p3.y - p1.y))
        if policy.approximately_zero(cp, scale):
            return OrientationResult.COLLINEAR
    else:
        if cp == 0:
            return OrientationResult.COLLINEAR

    return OrientationResult.COUNTER_CLOCKWISE if cp > 0 else OrientationResult.CLOCKWISE


# ── 2. Segment Intersection (3R-B) ──

def _on_segment_1d(a: float, b: float, c: float, eps: float = 1e-9) -> bool:
    return min(a, b) - eps <= c <= max(a, b) + eps


def oracle_segment_intersection(
    s1: Segment2D,
    s2: Segment2D,
    policy: Optional[FloatingPointPolicy] = None
) -> Tuple[bool, SegmentRelationshipType]:
    """
    Returns (intersects: bool, relationship_type).
    """
    p1, p2 = s1.p1, s1.p2
    p3, p4 = s2.p1, s2.p2

    o1 = oracle_orientation(p1, p2, p3, policy)
    o2 = oracle_orientation(p1, p2, p4, policy)
    o3 = oracle_orientation(p3, p4, p1, policy)
    o4 = oracle_orientation(p3, p4, p2, policy)

    # General proper crossing: endpoints strictly straddle each other
    if (o1 != o2 and o1 != OrientationResult.COLLINEAR and o2 != OrientationResult.COLLINEAR and
        o3 != o4 and o3 != OrientationResult.COLLINEAR and o4 != OrientationResult.COLLINEAR):
        return True, SegmentRelationshipType.PROPER_CROSSING

    # Both segments collinear (lie on same infinite line)
    all_collinear = (o1 == OrientationResult.COLLINEAR and o2 == OrientationResult.COLLINEAR)
    eps = policy.abs_epsilon if policy else 1e-9

    if all_collinear:
        # Check 1D interval overlap
        # Use X projection unless vertical
        if abs(p1.x - p2.x) > eps or abs(p3.x - p4.x) > eps:
            min1, max1 = min(p1.x, p2.x), max(p1.x, p2.x)
            min2, max2 = min(p3.x, p4.x), max(p3.x, p4.x)
        else:
            min1, max1 = min(p1.y, p2.y), max(p1.y, p2.y)
            min2, max2 = min(p3.y, p4.y), max(p3.y, p4.y)

        overlap_lo = max(min1, min2)
        overlap_hi = min(max1, max2)

        if overlap_lo < overlap_hi - eps:
            return True, SegmentRelationshipType.COLLINEAR_OVERLAP
        elif abs(overlap_lo - overlap_hi) <= eps:
            return True, SegmentRelationshipType.TOUCHING_ENDPOINT
        else:
            return False, SegmentRelationshipType.DISJOINT

    # Non-collinear touching cases (endpoint on segment or T-junction)
    if o1 == OrientationResult.COLLINEAR and _on_segment_1d(p1.x, p2.x, p3.x, eps) and _on_segment_1d(p1.y, p2.y, p3.y, eps):
        return True, SegmentRelationshipType.TOUCHING_ENDPOINT
    if o2 == OrientationResult.COLLINEAR and _on_segment_1d(p1.x, p2.x, p4.x, eps) and _on_segment_1d(p1.y, p2.y, p4.y, eps):
        return True, SegmentRelationshipType.TOUCHING_ENDPOINT
    if o3 == OrientationResult.COLLINEAR and _on_segment_1d(p3.x, p4.x, p1.x, eps) and _on_segment_1d(p3.y, p4.y, p1.y, eps):
        return True, SegmentRelationshipType.TOUCHING_ENDPOINT
    if o4 == OrientationResult.COLLINEAR and _on_segment_1d(p3.x, p4.x, p2.x, eps) and _on_segment_1d(p3.y, p4.y, p2.y, eps):
        return True, SegmentRelationshipType.TOUCHING_ENDPOINT

    return False, SegmentRelationshipType.DISJOINT


# ── 3. Convex Hull Monotone Chain (3R-C) ──

def oracle_convex_hull(
    points: List[Point2D],
    policy: HullCollinearPolicy = HullCollinearPolicy.STRICT_VERTICES
) -> List[Point2D]:
    """
    Andrew's Monotone Chain convex hull algorithm.
    Returns vertices in counter-clockwise cyclic order.
    """
    pts = sorted(list({(p.x, p.y): p for p in points}.values()), key=lambda p: (p.x, p.y))
    n = len(pts)
    if n <= 1:
        return pts

    def cross_prod(o: Point2D, a: Point2D, b: Point2D) -> float:
        return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

    # Lower hull
    lower: List[Point2D] = []
    for p in pts:
        if policy == HullCollinearPolicy.STRICT_VERTICES:
            while len(lower) >= 2 and cross_prod(lower[-2], lower[-1], p) <= 0:
                lower.pop()
        else:
            while len(lower) >= 2 and cross_prod(lower[-2], lower[-1], p) < 0:
                lower.pop()
        lower.append(p)

    # Upper hull
    upper: List[Point2D] = []
    for p in reversed(pts):
        if policy == HullCollinearPolicy.STRICT_VERTICES:
            while len(upper) >= 2 and cross_prod(upper[-2], upper[-1], p) <= 0:
                upper.pop()
        else:
            while len(upper) >= 2 and cross_prod(upper[-2], upper[-1], p) < 0:
                upper.pop()
        upper.append(p)

    # Concatenate hulls omitting redundant endpoints
    return lower[:-1] + upper[:-1]


# ── 4. Shoelace Polygon Area (3R-D) ──

def oracle_polygon_area(points: List[Point2D]) -> float:
    """
    Returns signed/absolute polygon area via Shoelace formula.
    """
    n = len(points)
    if n < 3:
        return 0.0
    area2 = 0.0
    for i in range(n):
        j = (i + 1) % n
        area2 += points[i].x * points[j].y - points[j].x * points[i].y
    return abs(area2) / 2.0


def oracle_polygon_double_area_integer(points: List[Point2D]) -> int:
    """
    Returns exact 2*Area in integer Z for integer coordinates.
    """
    n = len(points)
    if n < 3:
        return 0
    area2 = 0
    for i in range(n):
        j = (i + 1) % n
        area2 += int(points[i].x) * int(points[j].y) - int(points[j].x) * int(points[i].y)
    return abs(area2)


# ── 5. Point in Polygon (3R-E) ──

def oracle_point_in_polygon(
    poly: List[Point2D],
    pt: Point2D,
    policy: Optional[FloatingPointPolicy] = None
) -> PointInPolygonResult:
    """
    Deterministic boundary-first containment check, followed by ray casting parity.
    """
    n = len(poly)
    if n < 3:
        return PointInPolygonResult.OUTSIDE

    eps = policy.abs_epsilon if policy else 1e-9

    # 1. Deterministic boundary test on each edge
    for i in range(n):
        p1 = poly[i]
        p2 = poly[(i + 1) % n]
        cp = (p2.x - p1.x) * (pt.y - p1.y) - (p2.y - p1.y) * (pt.x - p1.x)
        if abs(cp) <= eps:
            if _on_segment_1d(p1.x, p2.x, pt.x, eps) and _on_segment_1d(p1.y, p2.y, pt.y, eps):
                return PointInPolygonResult.ON_BOUNDARY

    # 2. Ray casting crossing parity
    inside = False
    for i in range(n):
        p1 = poly[i]
        p2 = poly[(i + 1) % n]
        if ((p1.y > pt.y) != (p2.y > pt.y)):
            # X intersection of edge with horizontal line through pt.y
            x_cross = (p2.x - p1.x) * (pt.y - p1.y) / (p2.y - p1.y) + p1.x
            if pt.x < x_cross:
                inside = not inside

    return PointInPolygonResult.INSIDE if inside else PointInPolygonResult.OUTSIDE


# ── 6. Closest Pair of Points (3R-F) ──

def oracle_closest_pair(points: List[Point2D]) -> float:
    """
    Exact minimum Euclidean distance between any pair in points.
    If points has duplicate coordinates, minimum distance is 0.0 (valid optimal result).
    """
    n = len(points)
    if n < 2:
        return 0.0

    min_dist_sq = float('inf')
    for i in range(n):
        for j in range(i + 1, n):
            d2 = points[i].dist_sq(points[j])
            if d2 < min_dist_sq:
                min_dist_sq = d2
                if min_dist_sq == 0.0:
                    return 0.0

    return math.sqrt(min_dist_sq)


# ── 7. Line Intersection Point (3R-G) ──

def oracle_line_intersection(
    l1: Line2D,
    l2: Line2D,
    policy: Optional[FloatingPointPolicy] = None
) -> Tuple[LineRelationshipType, Optional[Point2D]]:
    """
    Computes unique intersection point of two lines via Cramer's rule.
    """
    fp = policy or FloatingPointPolicy()
    det = l1.a * l2.b - l2.a * l1.b
    scale = max(abs(l1.a), abs(l1.b)) * max(abs(l2.a), abs(l2.b))

    if fp.determinant_ambiguous(det, scale):
        det_c1 = l1.a * l2.c - l2.a * l1.c
        det_c2 = l1.b * l2.c - l2.b * l1.c
        if fp.approximately_zero(det_c1, scale) and fp.approximately_zero(det_c2, scale):
            return LineRelationshipType.COINCIDENT_IDENTICAL, None
        return LineRelationshipType.PARALLEL_DISJOINT, None

    x = (l1.b * l2.c - l2.b * l1.c) / det
    y = (l2.a * l1.c - l1.a * l2.c) / det
    return LineRelationshipType.SECANT_UNIQUE_INTERSECTION, Point2D(x, y)


# ── 8. Rotating Calipers Diameter (3R-H) ──

def oracle_rotating_calipers_diameter(hull_points: List[Point2D]) -> float:
    """
    Computes maximum pairwise Euclidean distance on a convex polygon.
    """
    n = len(hull_points)
    if n < 2:
        return 0.0
    if n == 2:
        return hull_points[0].dist(hull_points[1])

    def cross_2d(p1: Point2D, p2: Point2D, p3: Point2D) -> float:
        return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)

    max_dist_sq = 0.0
    k = 1
    # Advance k to the point furthest from edge 0 -> 1
    while cross_2d(hull_points[0], hull_points[1], hull_points[(k + 1) % n]) > cross_2d(hull_points[0], hull_points[1], hull_points[k]):
        k = (k + 1) % n

    for i in range(n):
        i_next = (i + 1) % n
        while cross_2d(hull_points[i], hull_points[i_next], hull_points[(k + 1) % n]) > cross_2d(hull_points[i], hull_points[i_next], hull_points[k]):
            k = (k + 1) % n
        max_dist_sq = max(max_dist_sq, hull_points[i].dist_sq(hull_points[k]))
        max_dist_sq = max(max_dist_sq, hull_points[i_next].dist_sq(hull_points[k]))

    return math.sqrt(max_dist_sq)


# ── 9. Halfplane Intersection (3R-I) ──

def _line_intersect_halfplanes(h1: Halfplane2D, h2: Halfplane2D) -> Optional[Point2D]:
    # h1: p1 + t*d1, h2: p2 + u*d2
    cp = h1.d.cross(h2.d)
    if abs(cp) < 1e-11:
        return None
    v = h2.p - h1.p
    t = v.cross(h2.d) / cp
    return Point2D(h1.p.x + t * h1.d.x, h1.p.y + t * h1.d.y)


def oracle_halfplane_intersection(halfplanes: List[Halfplane2D]) -> List[Point2D]:
    """
    Computes convex polygon representing feasible intersection of halfplanes.
    Returns ordered vertices, or empty list if infeasible or unbounded.
    """
    if len(halfplanes) < 3:
        return []

    # Sort by polar angle
    hps = sorted(halfplanes, key=lambda h: h.angle)

    # Remove parallel halfplanes with smaller feasible regions
    unique_hps: List[Halfplane2D] = []
    for h in hps:
        if unique_hps and abs(h.angle - unique_hps[-1].angle) < 1e-9:
            if unique_hps[-1].contains(h.p):
                unique_hps[-1] = h
        else:
            unique_hps.append(h)

    n = len(unique_hps)
    if n < 3:
        return []

    # Deque maintenance
    dq: List[Halfplane2D] = [unique_hps[0], unique_hps[1]]
    pts: List[Point2D] = []
    p01 = _line_intersect_halfplanes(unique_hps[0], unique_hps[1])
    if p01 is None:
        return []
    pts.append(p01)

    for i in range(2, n):
        cur = unique_hps[i]
        while pts and not cur.contains(pts[-1]):
            pts.pop()
            dq.pop()
        while pts and not cur.contains(pts[0]):
            pts.pop(0)
            dq.pop(0)
        p_new = _line_intersect_halfplanes(dq[-1], cur)
        if p_new is None:
            return []
        pts.append(p_new)
        dq.append(cur)

    while pts and not dq[0].contains(pts[-1]):
        pts.pop()
        dq.pop()

    if len(dq) < 3:
        return []

    p_close = _line_intersect_halfplanes(dq[-1], dq[0])
    if p_close is None:
        return []
    pts.append(p_close)

    return pts


# ── 10. Sweep Line Segment Intersections (3R-J) ──

def oracle_sweep_line_segments(
    segments: List[Segment2D],
    objective: SweepLineObjective = SweepLineObjective.EXISTENCE
) -> Union[bool, int, List[Tuple[int, int]]]:
    """
    Reference oracle for pairwise segment intersections.
    """
    n = len(segments)
    pairs: List[Tuple[int, int]] = []

    for i in range(n):
        for j in range(i + 1, n):
            intersects, _ = oracle_segment_intersection(segments[i], segments[j])
            if intersects:
                if objective == SweepLineObjective.EXISTENCE:
                    return True
                pairs.append((i, j))

    if objective == SweepLineObjective.EXISTENCE:
        return False
    elif objective == SweepLineObjective.COUNT:
        return len(pairs)
    else:
        return pairs
