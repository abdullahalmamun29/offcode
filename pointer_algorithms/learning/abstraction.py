"""
Knowledge Abstraction Engine.

Transforms problem-specific solution traces into domain-level AlgorithmicRules.
Ensures CHUP does NOT store "Problem 17 -> L++, R--", but rather generalized
conditions, invariants, and elimination proofs.
"""

from typing import Dict, Any, List
from pointer_algorithms.knowledge.knowledge_store import AlgorithmicRule, ConfidenceLevel

class AbstractionEngine:

    @staticmethod
    def abstract_from_trace(
        problem_id: str,
        domain: str,
        pattern_kind: str,
        preconditions: List[str],
        pointer_roles: List[Dict[str, Any]],
        invariant: Dict[str, str],
        monotonic_relation: str,
        movement_rule: Dict[str, str],
        elimination_proof: str,
        complexity: Dict[str, str],
        failure_conditions: List[str]
    ) -> AlgorithmicRule:
        """Constructs a candidate generalized AlgorithmicRule from validated trace semantics."""
        rule_id = f"induced_{pattern_kind}_{problem_id}"

        return AlgorithmicRule(
            rule_id=rule_id,
            domain=domain,
            pattern=pattern_kind,
            preconditions=list(preconditions),
            state_variables=["L", "R", "window_state"],
            pointer_roles=pointer_roles,
            invariant=invariant,
            monotonic_relation=monotonic_relation,
            movement_rule=movement_rule,
            elimination_proof=elimination_proof,
            complexity=complexity,
            failure_conditions=failure_conditions,
            supporting_examples=[problem_id],
            confidence_level=ConfidenceLevel.CANDIDATE,
            validation_count=1
        )
