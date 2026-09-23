"""
CHUP Phase 3R — Semantic Computational Geometry Ontology & Provenance Model.

Defines orthogonal primitive geometric dimensions, multi-scale numerical floating-point policies,
geometric primitives (Point2D, Segment2D, Line2D, Halfplane2D), and derived structural properties
with complete provenance. Zero algorithm names allowed in the ontology.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
import math


# ── 1. Coordinate Domains & Guarantees ──

class CoordinateDomain(str, Enum):
    INTEGER_EXACT = "INTEGER_EXACT"                 # Exact integer coordinates Z^2 (requires __int128_t for orientation)
    FLOATING_APPROXIMATE = "FLOATING_APPROXIMATE"   # Real coordinates R^2 (governed by FloatingPointPolicy)


class CorrectnessGuarantee(str, Enum):
    DETERMINISTIC_EXACT = "DETERMINISTIC_EXACT"
    CORRECTNESS_NUMERIC_APPROXIMATE = "CORRECTNESS_NUMERIC_APPROXIMATE"


# ── 2. Primitive Geometric Classifications ──

class OrientationResult(str, Enum):
    CLOCKWISE = "CLOCKWISE"                         # Right turn / negative cross product
    COUNTER_CLOCKWISE = "COUNTER_CLOCKWISE"         # Left turn / positive cross product
    COLLINEAR = "COLLINEAR"                         # Zero cross product within tolerance


class PointInPolygonResult(str, Enum):
    INSIDE = "INSIDE"
    OUTSIDE = "OUTSIDE"
    ON_BOUNDARY = "ON_BOUNDARY"


class LineRelationshipType(str, Enum):
    SECANT_UNIQUE_INTERSECTION = "SECANT_UNIQUE_INTERSECTION"
    PARALLEL_DISJOINT = "PARALLEL_DISJOINT"
    COINCIDENT_IDENTICAL = "COINCIDENT_IDENTICAL"


class SegmentRelationshipType(str, Enum):
    PROPER_CROSSING = "PROPER_CROSSING"             # Strict intersection in interiors
    TOUCHING_ENDPOINT = "TOUCHING_ENDPOINT"         # Intersection at an endpoint or T-junction
    COLLINEAR_OVERLAP = "COLLINEAR_OVERLAP"         # Collinear with positive overlap length
    DISJOINT = "DISJOINT"                           # No common points


class HalfplaneIntersectionState(str, Enum):
    EMPTY = "EMPTY"
    UNBOUNDED = "UNBOUNDED"
    BOUNDED = "BOUNDED"


class HalfplaneRegionType(str, Enum):
    BOUNDED_CONVEX_POLYGON = "BOUNDED_CONVEX_POLYGON"
    UNBOUNDED_FEASIBLE_REGION = "UNBOUNDED_FEASIBLE_REGION"
    EMPTY_INFEASIBLE = "EMPTY_INFEASIBLE"


class HullCollinearPolicy(str, Enum):
    STRICT_VERTICES = "STRICT_VERTICES"             # Eliminates collinear points along hull edges (cross <= 0)
    KEEP_BOUNDARY_POINTS = "KEEP_BOUNDARY_POINTS"   # Preserves all points on hull perimeter (cross < 0)


class SweepLineObjective(str, Enum):
    EXISTS_INTERSECTION = "EXISTS_INTERSECTION"     # Detect if any two segments intersect (early exit O(N log N))
    COUNT_INTERSECTIONS = "COUNT_INTERSECTIONS"     # Count total intersection points O((N + K) log N)
    ENUMERATE_INTERSECTIONS = "ENUMERATE_INTERSECTIONS" # List all intersection points O((N + K) log N)

    # Aliases for backward compatibility
    EXISTENCE = "EXISTS_INTERSECTION"
    COUNT = "COUNT_INTERSECTIONS"
    ENUMERATE = "ENUMERATE_INTERSECTIONS"


# ── 3. Atomic Geometry Objectives ──

class GeometryObjective(str, Enum):
    ORIENTATION_CROSS_PRODUCT = "ORIENTATION_CROSS_PRODUCT"         # 3R-A
    SEGMENT_INTERSECTION = "SEGMENT_INTERSECTION"                   # 3R-B
    CONVEX_HULL_ANDREW = "CONVEX_HULL_ANDREW"                       # 3R-C
    POLYGON_AREA_SHOELACE = "POLYGON_AREA_SHOELACE"                 # 3R-D
    POINT_IN_POLYGON = "POINT_IN_POLYGON"                           # 3R-E
    CLOSEST_PAIR_POINTS = "CLOSEST_PAIR_POINTS"                     # 3R-F
    LINE_INTERSECTION_POINT = "LINE_INTERSECTION_POINT"             # 3R-G
    ROTATING_CALIPERS_DIAMETER = "ROTATING_CALIPERS_DIAMETER"       # 3R-H
    HALFPLANE_INTERSECTION = "HALFPLANE_INTERSECTION"               # 3R-I
    SWEEP_LINE_SEGMENTS = "SWEEP_LINE_SEGMENTS"                     # 3R-J
    OUT_OF_SCOPE_3D_GEOMETRY = "OUT_OF_SCOPE_3D_GEOMETRY"
    OUT_OF_SCOPE_VORONOI_DELAUNAY = "OUT_OF_SCOPE_VORONOI_DELAUNAY"
    NONE = "NONE"


# ── 4. Multi-Scale Numerical Floating-Point Policy ──

@dataclass
class FloatingPointPolicy:
    """
    Scale-aware tolerance policy replacing raw epsilon scalars.
    Provides explicit scale-aware predicates for numerical robustness.
    """
    abs_epsilon: float = 1e-9
    rel_epsilon: float = 1e-9
    angular_epsilon: float = 1e-9
    determinant_epsilon: float = 1e-12

    def approximately_zero(self, val: float, scale: float = 1.0) -> bool:
        threshold = self.abs_epsilon + self.rel_epsilon * abs(scale)
        return abs(val) <= threshold

    def approximately_equal(self, a: float, b: float, scale: float = 1.0) -> bool:
        threshold = self.abs_epsilon + self.rel_epsilon * abs(scale)
        return abs(a - b) <= threshold

    def determinant_ambiguous(self, det: float, scale: float = 1.0) -> bool:
        threshold = self.determinant_epsilon + self.rel_epsilon * abs(scale)
        return abs(det) <= threshold

    def angularly_ambiguous(self, angle: float) -> bool:
        return abs(angle) <= self.angular_epsilon


# ── 5. Geometric Primitives ──

@dataclass(frozen=True)
class Point2D:
    x: float
    y: float
    id: Optional[int] = None

    def __add__(self, other: 'Point2D') -> 'Point2D':
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point2D') -> 'Point2D':
        return Point2D(self.x - other.x, self.y - other.y)

    def cross(self, other: 'Point2D') -> float:
        return self.x * other.y - self.y * other.x

    def dot(self, other: 'Point2D') -> float:
        return self.x * other.x + self.y * other.y

    def dist_sq(self, other: 'Point2D') -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return dx * dx + dy * dy

    def dist(self, other: 'Point2D') -> float:
        return math.sqrt(self.dist_sq(other))


@dataclass(frozen=True)
class Segment2D:
    p1: Point2D
    p2: Point2D
    id: Optional[int] = None

    def is_degenerate(self, policy: Optional[FloatingPointPolicy] = None) -> bool:
        if policy is None:
            return self.p1.x == self.p2.x and self.p1.y == self.p2.y
        return policy.approximately_equal(self.p1.x, self.p2.x) and policy.approximately_equal(self.p1.y, self.p2.y)


@dataclass(frozen=True)
class Line2D:
    """Line in general form: ax + by + c = 0."""
    a: float
    b: float
    c: float

    @classmethod
    def from_points(cls, p1: Point2D, p2: Point2D) -> 'Line2D':
        a = p2.y - p1.y
        b = p1.x - p2.x
        c = -(a * p1.x + b * p1.y)
        return cls(a, b, c)


@dataclass(frozen=True)
class Halfplane2D:
    """Halfplane defined by directed line p -> p + d, feasible region to the left."""
    p: Point2D
    d: Point2D  # direction vector
    angle: float = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, 'angle', math.atan2(self.d.y, self.d.x))

    def contains(self, pt: Point2D, policy: Optional[FloatingPointPolicy] = None) -> bool:
        """Returns true if pt is to the left of directed vector d (cross product >= 0)."""
        cp = self.d.cross(pt - self.p)
        if policy is not None and policy.approximately_zero(cp):
            return True
        return cp >= 0.0


# ── 6. Provenance Dataclass ──

class ProvenanceStatus(str, Enum):
    PROVEN = "PROVEN"
    UNPROVEN = "UNPROVEN"
    CONTRADICTED = "CONTRADICTED"


@dataclass
class DerivedFact:
    """
    Formal record tracking how a geometric, topological, or numerical property was deduced.
    """
    fact_id: str
    value: Any
    source_facts: List[str] = field(default_factory=list)
    derivation_rule: str = ""
    proof_obligations: List[str] = field(default_factory=list)
    status: ProvenanceStatus = ProvenanceStatus.PROVEN


# ── 7. Semantic Geometry Model ──

@dataclass
class SemanticGeometryModel:
    """
    Complete semantic representation of a geometric problem.
    Zero algorithm names allowed.
    """
    coordinate_domain: CoordinateDomain = CoordinateDomain.INTEGER_EXACT
    correctness_guarantee: CorrectnessGuarantee = CorrectnessGuarantee.DETERMINISTIC_EXACT
    objective: GeometryObjective = GeometryObjective.NONE
    hull_collinear_policy: HullCollinearPolicy = HullCollinearPolicy.STRICT_VERTICES
    sweep_line_objective: SweepLineObjective = SweepLineObjective.EXISTENCE
    floating_point_policy: FloatingPointPolicy = field(default_factory=FloatingPointPolicy)

    # Concrete dimensional & cardinality parameters
    points_count: Optional[int] = None
    segments_count: Optional[int] = None
    lines_count: Optional[int] = None
    halfplanes_count: Optional[int] = None
    max_coordinate_magnitude: Optional[int] = None
    is_simple_polygon: bool = False
    is_convex_polygon: bool = False

    # Derived properties & provenance
    derived_properties: Dict[str, Any] = field(default_factory=dict)
    provenance_records: List[DerivedFact] = field(default_factory=list)

    def add_derived_property(
        self,
        fact_id: str,
        value: Any,
        source_facts: List[str],
        rule: str,
        obligations: Optional[List[str]] = None
    ) -> None:
        self.derived_properties[fact_id] = value
        self.provenance_records.append(DerivedFact(
            fact_id=fact_id,
            value=value,
            source_facts=source_facts,
            derivation_rule=rule,
            proof_obligations=obligations or [],
            status=ProvenanceStatus.PROVEN
        ))

    def has_derived_fact(self, fact_id: str) -> bool:
        return self.derived_properties.get(fact_id, False) is True
