"""
Knowledge Induction Engine.

Analyzes a verified solution trace and induces:
- Structural preconditions that made the solution correct
- The exact monotonic relationship that justified movement
- Invariant phases preserved across steps
- Generalized rule candidate
"""

from typing import Dict, Any, List
from pointer_algorithms.learning.abstraction import AbstractionEngine
from pointer_algorithms.knowledge.knowledge_store import AlgorithmicRule
from pointer_algorithms.reasoning.monotonicity_engine import MonotonicityEngine, MonotonicityKind
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine

class KnowledgeInductionEngine:

    @staticmethod
    def induce_rule_from_solution(
        problem_id: str,
        pattern_kind: str,
        sample_input: Any,
        features: Dict[str, Any],
        simulation_result: Dict[str, Any]
    ) -> AlgorithmicRule:
        """Induces an AlgorithmicRule from a successfully verified simulation and problem features."""
        # 1. Extract confirmed preconditions
        preconditions = []
        if features.get("is_sorted"):
            preconditions.append("sorted_order")
        if features.get("is_contiguous"):
            preconditions.append("contiguous_subarray")
        if features.get("in_place_required"):
            preconditions.append("in_place_modification_allowed")

        # 2. Extract monotonic relation
        mono_assessment = MonotonicityEngine.assess_for_pattern(
            pattern=pattern_kind,
            has_negative_values=features.get("has_negative_values", False),
            is_sorted=features.get("is_sorted", False),
            can_sort=features.get("can_sort", True),
            is_contiguous=features.get("is_contiguous", False),
            tracks_distinct=features.get("tracks_distinct", False),
            objective_type=features.get("optimization_objective", "")
        )
        monotonic_relation = f"{mono_assessment.kind.value}: {mono_assessment.property_description}"

        # 3. Extract formal invariant
        invariant_spec = InvariantEngine.construct_invariant(pattern_kind, features)
        invariant_dict = {
            "before": invariant_spec.before_iteration,
            "during": invariant_spec.during_iteration,
            "after": invariant_spec.after_movement,
            "termination": invariant_spec.at_termination
        }

        # 4. Extract derived movement & elimination proof
        derivation = MovementDerivationEngine.derive(pattern_kind, features)

        # 5. Determine pointer roles
        pointer_roles = [
            {"name": "L", "role": "left_bound", "direction": "increment"},
            {"name": "R", "role": "right_bound", "direction": "decrement"}
        ]

        # 6. Complexity
        complexity = {"time": "O(N)", "space": "O(1)", "preprocessing": "None"}
        if not features.get("is_sorted") and features.get("can_sort"):
            complexity["preprocessing"] = "O(N log N) sort"

        # 7. Failure conditions
        failure_conditions = []
        if mono_assessment.kind == MonotonicityKind.WINDOW_VALIDITY_MONOTONICITY:
            failure_conditions.append("WINDOW_NOT_MONOTONIC")
        if not features.get("is_sorted"):
            failure_conditions.append("UNSORTED_INPUT")

        return AbstractionEngine.abstract_from_trace(
            problem_id=problem_id,
            domain="pointer_algorithms",
            pattern_kind=pattern_kind,
            preconditions=preconditions,
            pointer_roles=pointer_roles,
            invariant=invariant_dict,
            monotonic_relation=monotonic_relation,
            movement_rule=derivation.decision_conditions,
            elimination_proof=derivation.elimination_proof,
            complexity=complexity,
            failure_conditions=failure_conditions
        )
