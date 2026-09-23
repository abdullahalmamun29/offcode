"""
CHUP Phase 3R — Geometric Candidate Evaluator.

Ranks and evaluates candidate algorithmic patterns relative to problem requirements,
structural properties, numerical contracts, and complexity bounds.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple, Optional

from pointer_algorithms.geometry.semantic_ontology import (
    SemanticGeometryModel,
    GeometryObjective,
    CoordinateDomain,
    HullCollinearPolicy,
    SweepLineObjective,
)
from pointer_algorithms.geometry.component_model import GeometryComponentRegistry


class CandidateStatus(str, Enum):
    VALID_OPTIMAL = "VALID_OPTIMAL"
    VALID_SUBOPTIMAL = "VALID_SUBOPTIMAL"
    INVALID_PRECONDITION = "INVALID_PRECONDITION"
    COMPLEXITY_REQUIREMENT_UNSATISFIED = "COMPLEXITY_REQUIREMENT_UNSATISFIED"
    NUMERIC_AMBIGUITY = "NUMERIC_AMBIGUITY"


class SelectionStatus(str, Enum):
    SELECTED = "SELECTED"
    NOT_SELECTED = "NOT_SELECTED"


@dataclass
class CandidateEvaluation:
    pattern: str
    component_name: str
    status: CandidateStatus
    selection: SelectionStatus
    complexity: str
    justification: str = ""
    evidence: str = ""
    rejection_code: Optional[str] = None
    correctness_guarantee: str = "DETERMINISTIC_EXACT"


class CandidateEvaluator:
    """
    Evaluates geometric algorithm candidates against the extracted SemanticGeometryModel.
    """

    def __init__(self, registry: Optional[GeometryComponentRegistry] = None) -> None:
        self.registry = registry or GeometryComponentRegistry()

    def evaluate(
        self,
        model: SemanticGeometryModel,
        gate_passed: bool = True,
        gate_rejection_code: Optional[str] = None,
        gate_failure_reason: Optional[str] = None
    ) -> Tuple[List[CandidateEvaluation], Optional[str]]:
        """
        Returns (candidate_evaluations, selected_pattern_name).
        """
        evaluations: List[CandidateEvaluation] = []
        selected_pattern: Optional[str] = None
        obj = model.objective

        # Mapping of canonical objective to (pattern_name, component_name, complexity, guarantee)
        objective_map = {
            GeometryObjective.ORIENTATION_CROSS_PRODUCT: (
                "geom_orientation_cross_product",
                "orientation_turn_predicate",
                "O(1)",
                "DETERMINISTIC_EXACT" if model.coordinate_domain == CoordinateDomain.INTEGER_EXACT else "CORRECTNESS_NUMERIC_APPROXIMATE"
            ),
            GeometryObjective.SEGMENT_INTERSECTION: (
                "geom_segment_intersection",
                "segment_intersection_detector",
                "O(1)",
                "DETERMINISTIC_EXACT" if model.coordinate_domain == CoordinateDomain.INTEGER_EXACT else "CORRECTNESS_NUMERIC_APPROXIMATE"
            ),
            GeometryObjective.CONVEX_HULL_ANDREW: (
                "geom_convex_hull_andrew",
                "convex_hull_monotone_chain",
                "O(N log N)",
                "DETERMINISTIC_EXACT"
            ),
            GeometryObjective.POLYGON_AREA_SHOELACE: (
                "geom_polygon_area_shoelace",
                "shoelace_polygon_area",
                "O(N)",
                "DETERMINISTIC_EXACT" if model.coordinate_domain == CoordinateDomain.INTEGER_EXACT else "CORRECTNESS_NUMERIC_APPROXIMATE"
            ),
            GeometryObjective.POINT_IN_POLYGON: (
                "geom_point_in_polygon",
                "point_in_polygon_ray_casting",
                "O(N)",
                "DETERMINISTIC_EXACT" if model.coordinate_domain == CoordinateDomain.INTEGER_EXACT else "CORRECTNESS_NUMERIC_APPROXIMATE"
            ),
            GeometryObjective.CLOSEST_PAIR_POINTS: (
                "geom_closest_pair_points",
                "closest_pair_divide_conquer",
                "O(N log N)",
                "DETERMINISTIC_EXACT" if model.coordinate_domain == CoordinateDomain.INTEGER_EXACT else "CORRECTNESS_NUMERIC_APPROXIMATE"
            ),
            GeometryObjective.LINE_INTERSECTION_POINT: (
                "geom_line_intersection_point",
                "line_intersection_cramer",
                "O(1)",
                "CORRECTNESS_NUMERIC_APPROXIMATE"
            ),
            GeometryObjective.ROTATING_CALIPERS_DIAMETER: (
                "geom_rotating_calipers_diameter",
                "rotating_calipers_antipodal",
                "O(N)",
                "DETERMINISTIC_EXACT" if model.coordinate_domain == CoordinateDomain.INTEGER_EXACT else "CORRECTNESS_NUMERIC_APPROXIMATE"
            ),
            GeometryObjective.HALFPLANE_INTERSECTION: (
                "geom_halfplane_intersection",
                "halfplane_intersection_deque",
                "O(N log N)",
                "CORRECTNESS_NUMERIC_APPROXIMATE"
            ),
            GeometryObjective.SWEEP_LINE_SEGMENTS: (
                "geom_sweep_line_segments",
                "sweep_line_bentley_ottmann",
                "O((N + K) log N)",
                "DETERMINISTIC_EXACT"
            ),
        }

        # Handle out of scope
        if obj in (GeometryObjective.OUT_OF_SCOPE_3D_GEOMETRY, GeometryObjective.OUT_OF_SCOPE_VORONOI_DELAUNAY):
            evaluations.append(CandidateEvaluation(
                pattern="out_of_scope_geometric_pattern",
                component_name="none",
                status=CandidateStatus.INVALID_PRECONDITION,
                selection=SelectionStatus.NOT_SELECTED,
                complexity="N/A",
                justification=f"Problem requests {obj.value}, outside supported 2D canonical geometric patterns.",
                evidence="Out of scope 3D / Voronoi / Delaunay pattern detected.",
                rejection_code="OUT_OF_SCOPE_GEOMETRY"
            ))
            return evaluations, None

        # If gate failed
        if not gate_passed:
            target_info = objective_map.get(obj)
            pat_name = target_info[0] if target_info else "geom_unknown"
            comp_name = target_info[1] if target_info else "none"
            cplx = target_info[2] if target_info else "O(1)"
            guar = target_info[3] if target_info else "DETERMINISTIC_EXACT"

            evaluations.append(CandidateEvaluation(
                pattern=pat_name,
                component_name=comp_name,
                status=CandidateStatus.INVALID_PRECONDITION,
                selection=SelectionStatus.NOT_SELECTED,
                complexity=cplx,
                justification=gate_failure_reason or "Closed-world geometric gate failed.",
                evidence=f"Rejection code {gate_rejection_code}: {gate_failure_reason}",
                rejection_code=gate_rejection_code,
                correctness_guarantee=guar
            ))
            return evaluations, None

        # Valid optimal candidate
        if obj in objective_map:
            pat_name, comp_name, cplx, guar = objective_map[obj]
            evaluations.append(CandidateEvaluation(
                pattern=pat_name,
                component_name=comp_name,
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity=cplx,
                justification=f"Optimal geometric component {comp_name} satisfies objective {obj.value}.",
                evidence=f"Preconditions satisfied, guarantee: {guar}, complexity: {cplx}.",
                correctness_guarantee=guar
            ))
            selected_pattern = pat_name

            # Add suboptimal alternatives for evaluation rigor
            if obj == GeometryObjective.ROTATING_CALIPERS_DIAMETER:
                evaluations.append(CandidateEvaluation(
                    pattern="geom_all_pairs_diameter_brute_force",
                    component_name="all_pairs_distance_check",
                    status=CandidateStatus.COMPLEXITY_REQUIREMENT_UNSATISFIED,
                    selection=SelectionStatus.NOT_SELECTED,
                    complexity="O(N^2)",
                    justification="All-pairs distance check O(N^2) is suboptimal compared to rotating calipers O(N).",
                    evidence="Quadratic complexity rejected for large point sets."
                ))
            elif obj == GeometryObjective.CLOSEST_PAIR_POINTS:
                evaluations.append(CandidateEvaluation(
                    pattern="geom_closest_pair_brute_force",
                    component_name="all_pairs_metric_check",
                    status=CandidateStatus.COMPLEXITY_REQUIREMENT_UNSATISFIED,
                    selection=SelectionStatus.NOT_SELECTED,
                    complexity="O(N^2)",
                    justification="All-pairs distance check O(N^2) is suboptimal compared to divide-and-conquer O(N log N).",
                    evidence="Quadratic metric search rejected."
                ))
            elif obj == GeometryObjective.SWEEP_LINE_SEGMENTS:
                evaluations.append(CandidateEvaluation(
                    pattern="geom_all_pairs_segment_intersection",
                    component_name="all_pairs_segment_checker",
                    status=CandidateStatus.COMPLEXITY_REQUIREMENT_UNSATISFIED,
                    selection=SelectionStatus.NOT_SELECTED,
                    complexity="O(N^2)",
                    justification="O(N^2) pairwise check is suboptimal compared to Bentley-Ottmann sweep-line O((N+K) log N).",
                    evidence="Quadratic segment checking rejected."
                ))

        return evaluations, selected_pattern
