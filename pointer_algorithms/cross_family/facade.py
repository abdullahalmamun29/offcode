"""
CHUP Phase 4: Unified Cross-Family Synthesis Engine Facade.

Coordinates:
Problem -> Derivation -> Composition Synthesis -> Gate Evaluation -> VerifiedCompositionPlan Barrier -> C++ Generation.
"""

from typing import Dict, Any, Optional, Tuple, List
from pointer_algorithms.cross_family.semantic_ontology import CrossFamilyProblemModel, CrossFamilyObjective
from pointer_algorithms.cross_family.derivation_engine import CrossFamilyDerivationEngine
from pointer_algorithms.cross_family.composition_engine import (
    CrossFamilyCompositionEngine,
    CompositionPlan,
    VerifiedCompositionPlan,
)
from pointer_algorithms.cross_family.gate_evaluator import CrossFamilyGateEvaluator
from pointer_algorithms.cross_family.candidate_evaluator import (
    CrossFamilyCandidateEvaluator,
    CandidateEvaluationResult,
    CandidateVerdict,
)
from pointer_algorithms.cross_family.generator.cross_family_cpp_generator import CrossFamilyCppGenerator


class CrossFamilySynthesisEngine:
    """
    Unified entry point for Phase 4 Cross-Family Composition & Multi-Component Synthesis.
    """
    def __init__(self):
        self.derivation = CrossFamilyDerivationEngine()
        self.composition = CrossFamilyCompositionEngine()
        self.gate_evaluator = CrossFamilyGateEvaluator()
        self.candidate_evaluator = CrossFamilyCandidateEvaluator()
        self.generator = CrossFamilyCppGenerator()

    def process(self, text_or_spec: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        ctx = context or {}

        # 1. Semantic Derivation
        model = self.derivation.extract_semantic_model(text_or_spec)

        # 2. Composition DAG Synthesis
        plan = self.composition.synthesize_plan(model)

        # 3. Gate Evaluation
        gate_passed, gate_code, gate_msg = self.gate_evaluator.evaluate(model, plan, ctx)
        if not gate_passed:
            plan.is_valid = False
            plan.failure_code = gate_code
            plan.failure_reason = gate_msg

        # 4. Candidate Evaluation
        eval_result = self.candidate_evaluator.evaluate(plan, gate_passed, gate_code, gate_msg)

        # 5. Verified Plan Sealing (The Absolute Barrier)
        verified_plan: Optional[VerifiedCompositionPlan] = None
        code: Optional[str] = None

        if gate_passed and plan.is_valid:
            verified_plan = self.composition.verify_and_seal_plan(plan)
            if verified_plan:
                # 6. C++ Code Generation accepts ONLY VerifiedCompositionPlan
                code = self.generator.generate(verified_plan, model)

        return {
            "model": model,
            "plan": plan,
            "gate_passed": gate_passed,
            "gate_failure_code": gate_code,
            "gate_failure_message": gate_msg,
            "eval_result": eval_result,
            "verified_plan": verified_plan,
            "code": code,
        }

    def generate_cpp_solution(self, text_or_spec: Any) -> Optional[str]:
        res = self.process(text_or_spec)
        return res.get("code")
