"""
CHUP Phase 3R — Geometry Component Model & Registry.

Defines declarative AlgorithmComponent nodes with state requirements, preconditions,
proof obligations, provider-relative complexity contracts, and explicit composition dependencies.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any

from pointer_algorithms.geometry.geometry_state_contracts import (
    StateContract,
    make_point_set_state,
    make_convex_hull_state,
    make_simple_polygon_state,
    make_segment_set_state,
    make_line_pair_state,
    make_halfplane_set_state,
    make_metric_space_2d_state,
)


class CompositionNodeType(str, Enum):
    COMPONENT = "COMPONENT"
    TRANSFORMATION = "TRANSFORMATION"


@dataclass
class AlgorithmComponent:
    """
    Formal specification of a reusable geometric algorithm component.
    """
    name: str
    node_type: CompositionNodeType = CompositionNodeType.COMPONENT
    consumes_state: List[StateContract] = field(default_factory=list)
    produces_state: List[StateContract] = field(default_factory=list)
    requires_capabilities: List[str] = field(default_factory=list)
    provided_capabilities: List[str] = field(default_factory=list)
    preconditions: List[str] = field(default_factory=list)
    proof_obligations: List[str] = field(default_factory=list)
    operation_complexity: str = ""
    space_complexity: str = ""
    correctness_guarantee: str = "DETERMINISTIC_EXACT"
    description: str = ""


class GeometryComponentRegistry:
    """
    Centralized registry for all Phase 3R Computational Geometry components.
    """
    _instance: Optional['GeometryComponentRegistry'] = None

    def __new__(cls) -> 'GeometryComponentRegistry':
        if cls._instance is None:
            cls._instance = super(GeometryComponentRegistry, cls).__new__(cls)
            cls._instance._components = {}
            cls._instance._register_default_components()
        return cls._instance

    def __init__(self) -> None:
        pass

    def register(self, component: AlgorithmComponent) -> None:
        self._components[component.name] = component

    def get(self, name: str) -> Optional[AlgorithmComponent]:
        return self._components.get(name)

    def remove(self, name: str) -> Optional[AlgorithmComponent]:
        return self._components.pop(name, None)

    def all_components(self) -> List[AlgorithmComponent]:
        return list(self._components.values())

    def reset_defaults(self) -> None:
        self._components.clear()
        self._register_default_components()

    def find_providers(self, capability: str) -> List[AlgorithmComponent]:
        return [c for c in self._components.values() if capability in c.provided_capabilities]

    def _register_default_components(self) -> None:
        # ── 1. Orientation / Cross Product Turn Predicate (3R-A) ──
        self.register(AlgorithmComponent(
            name="orientation_turn_predicate",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_point_set_state(count=3)],
            produces_state=[StateContract("OrientationState")],
            requires_capabilities=[],
            provided_capabilities=["ORIENTATION_PREDICATE", "CROSS_PRODUCT_TURN"],
            preconditions=["points_count_eq_3"],
            proof_obligations=["int128_overflow_safety_proven", "turn_sign_correctness_proven"],
            operation_complexity="O(1) exact arithmetic",
            space_complexity="O(1)",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="2D orientation predicate via cross product with __int128_t promotion for integer coordinates."
        ))

        # ── 2. Segment Intersection Detector (3R-B) ──
        self.register(AlgorithmComponent(
            name="segment_intersection_detector",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_segment_set_state(count=2)],
            produces_state=[StateContract("SegmentIntersectionState")],
            requires_capabilities=["ORIENTATION_PREDICATE"],
            provided_capabilities=["SEGMENT_INTERSECTION", "BOUNDING_BOX_REJECTION"],
            preconditions=["segment_endpoints_valid"],
            proof_obligations=["four_turn_cross_soundness_proven", "bounding_box_overlap_soundness_proven"],
            operation_complexity="O(1) checks",
            space_complexity="O(1)",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Robust 2D segment intersection using 4-turn orientation checks and 1D bounding-box projections."
        ))

        # ── 3. Convex Hull Monotone Chain (3R-C) ──
        self.register(AlgorithmComponent(
            name="convex_hull_monotone_chain",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_point_set_state(count=3)],
            produces_state=[make_convex_hull_state(vertex_count=3)],
            requires_capabilities=["ORIENTATION_PREDICATE"],
            provided_capabilities=["CONVEX_HULL", "EXTREME_POINTS_ENUMERATION"],
            preconditions=["points_count_ge_3", "non_collinear_point_set"],
            proof_obligations=["lexicographical_sort_soundness", "upper_lower_hull_cross_elimination_proven"],
            operation_complexity="O(N log N) sorting + O(N) sweep",
            space_complexity="O(N) output hull stack",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Andrew's Monotone Chain convex hull algorithm with configurable HullCollinearPolicy."
        ))

        # ── 4. Shoelace Polygon Area (3R-D) ──
        self.register(AlgorithmComponent(
            name="shoelace_polygon_area",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_simple_polygon_state(vertex_count=3)],
            produces_state=[StateContract("PolygonAreaState")],
            requires_capabilities=[],
            provided_capabilities=["POLYGON_AREA", "SHOELACE_FORMULA"],
            preconditions=["vertex_count_ge_3", "polygon_is_simple"],
            proof_obligations=["greens_theorem_discrete_exactness_proven", "int128_double_area_overflow_safe"],
            operation_complexity="O(N) cyclic summation",
            space_complexity="O(1)",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Computes signed/absolute polygon area via Shoelace formula, supporting exact integer 2A in __int128_t."
        ))

        # ── 5. Point in Polygon Ray Casting (3R-E) ──
        self.register(AlgorithmComponent(
            name="point_in_polygon_ray_casting",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_simple_polygon_state(vertex_count=3)],
            produces_state=[StateContract("PointInPolygonState")],
            requires_capabilities=[],
            provided_capabilities=["POINT_IN_POLYGON", "BOUNDARY_FIRST_TEST"],
            preconditions=["vertex_count_ge_3", "polygon_is_simple"],
            proof_obligations=["boundary_classification_prior_to_ray_casting", "jordan_curve_parity_soundness"],
            operation_complexity="O(N) boundary scan + ray intersection",
            space_complexity="O(1)",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Deterministic boundary-first point-in-polygon containment test followed by ray casting crossing parity."
        ))

        # ── 6. Closest Pair Divide and Conquer (3R-F) ──
        self.register(AlgorithmComponent(
            name="closest_pair_divide_conquer",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_metric_space_2d_state(points_count=2)],
            produces_state=[StateContract("ClosestPairState")],
            requires_capabilities=[],
            provided_capabilities=["CLOSEST_PAIR_OF_POINTS", "EUCLIDEAN_METRIC_MINIMUM"],
            preconditions=["points_count_ge_2"],
            proof_obligations=["divide_conquer_geometric_strip_bounded_comparisons_proven", "duplicate_point_zero_distance_valid"],
            operation_complexity="O(N log N) divide and conquer",
            space_complexity="O(N) merge buffer",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Shamos-Hoey style divide-and-conquer closest pair of 2D points with strip bounding optimization."
        ))

        # ── 7. Line Intersection Cramer (3R-G) ──
        self.register(AlgorithmComponent(
            name="line_intersection_cramer",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_line_pair_state()],
            produces_state=[StateContract("LineIntersectionPointState")],
            requires_capabilities=[],
            provided_capabilities=["LINE_INTERSECTION_POINT", "CRAMERS_RULE"],
            preconditions=["lines_non_parallel_proven", "determinant_exceeds_numerical_tolerance"],
            proof_obligations=["cramers_rule_determinant_soundness_proven", "scale_aware_tolerance_gate_proven"],
            operation_complexity="O(1) determinants",
            space_complexity="O(1)",
            correctness_guarantee="CORRECTNESS_NUMERIC_APPROXIMATE",
            description="2D line intersection point via Cramer's rule determinants with scale-aware singularity gating."
        ))

        # ── 8. Rotating Calipers Antipodal Diameter (3R-H) ──
        self.register(AlgorithmComponent(
            name="rotating_calipers_antipodal",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_convex_hull_state(vertex_count=3)],
            produces_state=[StateContract("PolygonDiameterState")],
            requires_capabilities=["CONVEX_HULL"],
            provided_capabilities=["CONVEX_POLYGON_DIAMETER", "ROTATING_CALIPERS", "MAXIMUM_DISTANCE_PAIR"],
            preconditions=["polygon_is_convex_certified", "vertices_cyclic_ordered_certified"],
            proof_obligations=["shamos_antipodal_pairs_exhaustion_proven", "monotonic_cross_advance_soundness"],
            operation_complexity="O(N) single-pass calipers advance",
            space_complexity="O(1) index pointers",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Shamos's rotating calipers algorithm for maximum pairwise distance / polygon diameter on convex polygons."
        ))

        # ── 9. Halfplane Intersection Deque (3R-I) ──
        self.register(AlgorithmComponent(
            name="halfplane_intersection_deque",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_halfplane_set_state(count=3)],
            produces_state=[make_convex_hull_state(vertex_count=3)],
            requires_capabilities=[],
            provided_capabilities=["HALFPLANE_INTERSECTION", "CONVEX_KERNEL_CONSTRUCTION"],
            preconditions=["halfplanes_count_ge_3", "feasible_region_bounded_certified", "feasible_region_non_empty_certified"],
            proof_obligations=["polar_angle_sort_deque_soundness_proven", "explicit_boundedness_verification_proven"],
            operation_complexity="O(N log N) polar angle sort + O(N) deque",
            space_complexity="O(N) double-ended queue",
            correctness_guarantee="CORRECTNESS_NUMERIC_APPROXIMATE",
            description="Dual deque incremental halfplane intersection constructing bounded convex polygon feasible regions."
        ))

        # ── 10. Sweep Line Bentley-Ottmann (3R-J) ──
        self.register(AlgorithmComponent(
            name="sweep_line_bentley_ottmann",
            node_type=CompositionNodeType.COMPONENT,
            consumes_state=[make_segment_set_state(count=2)],
            produces_state=[StateContract("SegmentIntersectionsEnsembleState")],
            requires_capabilities=["SEGMENT_INTERSECTION"],
            provided_capabilities=["SWEEP_LINE_SEGMENT_INTERSECTION", "BENTLEY_OTTMANN"],
            preconditions=["segments_non_overlapping_certified", "supported_sweep_objective_certified"],
            proof_obligations=["lexicographical_sweep_event_queue_soundness", "active_status_balanced_tree_soundness"],
            operation_complexity="O((N + K) log N) event queue sweep",
            space_complexity="O(N) status tree + event priority queue",
            correctness_guarantee="DETERMINISTIC_EXACT",
            description="Bentley-Ottmann sweep-line reporting pairwise segment intersections with explicit SweepLineObjective."
        ))
