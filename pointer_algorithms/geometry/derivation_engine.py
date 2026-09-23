"""
CHUP Phase 3R — Computational Geometry Derivation Engine Façade.

Coordinates semantic extraction, constraint analysis, closed-world gate evaluation,
candidate ranking, and delegates C++ solution generation.
"""

from typing import List, Tuple, Optional, Any, Dict

from pointer_algorithms.geometry.semantic_ontology import (
    SemanticGeometryModel,
    CoordinateDomain,
    CorrectnessGuarantee,
    GeometryObjective,
    HullCollinearPolicy,
    SweepLineObjective,
    FloatingPointPolicy,
    Point2D,
    Segment2D,
    Line2D,
    Halfplane2D,
)
from pointer_algorithms.geometry.component_model import GeometryComponentRegistry
from pointer_algorithms.geometry.derivation.semantic_extractor import SemanticExtractor
from pointer_algorithms.geometry.derivation.constraint_analyzer import ConstraintAnalyzer
from pointer_algorithms.geometry.derivation.gate_evaluator import GateEvaluator
from pointer_algorithms.geometry.derivation.candidate_evaluator import (
    CandidateEvaluator,
    CandidateEvaluation,
    CandidateStatus,
    SelectionStatus,
)


class GeometryDerivationEngine:
    """
    Unified derivation engine façade for Computational Geometry.
    """

    def __init__(self, registry: Optional[GeometryComponentRegistry] = None) -> None:
        self.registry = registry or GeometryComponentRegistry()
        self.extractor = SemanticExtractor()
        self.analyzer = ConstraintAnalyzer()
        self.gate_evaluator = GateEvaluator()
        self.candidate_evaluator = CandidateEvaluator(self.registry)

    def extract_semantic_model(self, text: str) -> SemanticGeometryModel:
        """
        Extracts semantic model from problem text and populates derived constraint properties.
        """
        model = self.extractor.extract(text)
        self.analyzer.analyze(model)
        return model

    def evaluate_candidates(
        self,
        model: SemanticGeometryModel,
        points: Optional[List[Point2D]] = None,
        segments: Optional[List[Segment2D]] = None,
        lines: Optional[List[Line2D]] = None,
        require_unique_point: bool = True,
        require_bounded_polygon: bool = True
    ) -> Tuple[List[CandidateEvaluation], Optional[str]]:
        """
        Evaluates closed-world gates and ranks candidates.
        Returns (candidate_evaluations, selected_pattern_name).
        """
        gate_passed, rejection_code, failure_reason = self.gate_evaluator.evaluate_gates(
            model=model,
            points=points,
            segments=segments,
            lines=lines,
            require_unique_point=require_unique_point,
            require_bounded_polygon=require_bounded_polygon
        )

        return self.candidate_evaluator.evaluate(
            model=model,
            gate_passed=gate_passed,
            gate_rejection_code=rejection_code,
            gate_failure_reason=failure_reason
        )

    def generate_cpp_solution(self, pattern: str, features: Optional[Dict[str, Any]] = None) -> str:
        """
        Emits verified C++17 implementation by delegating to geometry_cpp_generator.
        """
        from pointer_algorithms.generator.geometry_cpp_generator import generate_geometry_cpp
        return generate_geometry_cpp(pattern, features)
