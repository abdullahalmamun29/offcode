"""
CHUP Phase 3R — Geometry State Contracts & Type System.

Enforces strict semantic substitutability, mathematical preconditions, and attribute unification.
Implementation ancestry does NOT imply IS-A. No caller-supplied certification booleans.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from pointer_algorithms.geometry.semantic_ontology import (
    CoordinateDomain,
    HullCollinearPolicy,
    LineRelationshipType,
    SegmentRelationshipType,
    HalfplaneRegionType,
    SweepLineObjective,
)


@dataclass
class StateContract:
    """
    Formal contract definition for a geometric state.
    Enforces explicit subtyping (supertypes) and attribute unification.
    """
    name: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    supertypes: List[str] = field(default_factory=list)

    def satisfies(self, requirement: 'StateContract') -> bool:
        type_compatible = (self.name == requirement.name or requirement.name in self.supertypes)
        if not type_compatible:
            return False

        for req_attr, req_val in requirement.attributes.items():
            if req_attr not in self.attributes:
                return False
            if req_val is not None and self.attributes[req_attr] != req_val:
                return False

        return True


# ── Canonical State Contract Constructors ──

def make_point_set_state(
    count: int = 3,
    coordinate_domain: str = "INTEGER_EXACT",
    max_coord: Optional[int] = None,
    distinct: bool = True
) -> StateContract:
    """
    State representing a finite point set in R^2 or Z^2.
    For signed coords > 1e9, requires_int128 is set to True.
    """
    requires_int128 = False
    if coordinate_domain == "INTEGER_EXACT":
        if max_coord is None or max_coord > 1_000_000_000:
            requires_int128 = True

    return StateContract(
        name="PointSetState",
        attributes={
            "count": count,
            "coordinate_domain": coordinate_domain,
            "max_coord": max_coord,
            "distinct": distinct,
            "requires_int128": requires_int128,
            "correctness_guarantee": "DETERMINISTIC_EXACT" if coordinate_domain == "INTEGER_EXACT" else "CORRECTNESS_NUMERIC_APPROXIMATE",
        },
        supertypes=["GeometricEntityState"]
    )


def make_convex_hull_state(
    vertex_count: int = 3,
    collinear_policy: str = "STRICT_VERTICES",
    is_convex: bool = True,
    cyclic_ordered: bool = True,
    coordinate_domain: str = "INTEGER_EXACT"
) -> StateContract:
    """
    ConvexHullState models a strictly or non-strictly convex cyclic polygon.
    Satisfies SimplePolygonState requirements.
    """
    return StateContract(
        name="ConvexHullState",
        attributes={
            "vertex_count": vertex_count,
            "is_simple": True,
            "collinear_policy": collinear_policy,
            "is_convex": is_convex,
            "cyclic_ordered": cyclic_ordered,
            "coordinate_domain": coordinate_domain,
            "correctness_guarantee": "DETERMINISTIC_EXACT" if coordinate_domain == "INTEGER_EXACT" else "CORRECTNESS_NUMERIC_APPROXIMATE",
        },
        supertypes=["SimplePolygonState", "GeometricEntityState"]
    )


def make_simple_polygon_state(
    vertex_count: int = 3,
    is_simple: bool = True,
    coordinate_domain: str = "INTEGER_EXACT"
) -> StateContract:
    """
    SimplePolygonState models a 2D simple polygon without self-intersections.
    """
    return StateContract(
        name="SimplePolygonState",
        attributes={
            "vertex_count": vertex_count,
            "is_simple": is_simple,
            "coordinate_domain": coordinate_domain,
            "correctness_guarantee": "DETERMINISTIC_EXACT" if coordinate_domain == "INTEGER_EXACT" else "CORRECTNESS_NUMERIC_APPROXIMATE",
        },
        supertypes=["GeometricEntityState"]
    )


def make_segment_set_state(
    count: int = 2,
    coordinate_domain: str = "INTEGER_EXACT",
    non_overlapping: bool = True,
    sweep_objective: str = "EXISTENCE"
) -> StateContract:
    """
    SegmentSetState models a set of 2D line segments.
    """
    return StateContract(
        name="SegmentSetState",
        attributes={
            "count": count,
            "coordinate_domain": coordinate_domain,
            "non_overlapping": non_overlapping,
            "sweep_objective": sweep_objective,
            "correctness_guarantee": "DETERMINISTIC_EXACT" if coordinate_domain == "INTEGER_EXACT" else "CORRECTNESS_NUMERIC_APPROXIMATE",
        },
        supertypes=["GeometricEntityState"]
    )


def make_line_pair_state(
    coordinate_domain: str = "FLOATING_APPROXIMATE",
    relationship: str = "SECANT_UNIQUE_INTERSECTION"
) -> StateContract:
    """
    LinePairState models two 2D lines and their relationship.
    """
    return StateContract(
        name="LinePairState",
        attributes={
            "coordinate_domain": coordinate_domain,
            "relationship": relationship,
            "correctness_guarantee": "CORRECTNESS_NUMERIC_APPROXIMATE",
        },
        supertypes=["GeometricEntityState"]
    )


def make_halfplane_set_state(
    count: int = 3,
    region_type: str = "BOUNDED_CONVEX_POLYGON",
    bounded: bool = True
) -> StateContract:
    """
    HalfplaneSetState models a system of 2D halfplanes.
    """
    return StateContract(
        name="HalfplaneSetState",
        attributes={
            "count": count,
            "region_type": region_type,
            "bounded": bounded,
            "correctness_guarantee": "CORRECTNESS_NUMERIC_APPROXIMATE",
        },
        supertypes=["GeometricEntityState"]
    )


def make_metric_space_2d_state(
    points_count: int = 2,
    coordinate_domain: str = "INTEGER_EXACT",
    has_duplicates: bool = False
) -> StateContract:
    """
    MetricSpace2DState models points in 2D Euclidean metric space.
    Duplicates yield distance 0.0, which is valid and not a failure.
    """
    return StateContract(
        name="MetricSpace2DState",
        attributes={
            "points_count": points_count,
            "coordinate_domain": coordinate_domain,
            "has_duplicates": has_duplicates,
            "correctness_guarantee": "DETERMINISTIC_EXACT" if coordinate_domain == "INTEGER_EXACT" else "CORRECTNESS_NUMERIC_APPROXIMATE",
        },
        supertypes=["GeometricEntityState"]
    )
