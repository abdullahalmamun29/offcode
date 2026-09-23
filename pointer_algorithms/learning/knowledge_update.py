"""
Knowledge Update & Hard-Gate Promotion Manager.

Promotes an induced rule only when cross-problem validation succeeds.
Levels: CANDIDATE -> VALIDATED -> REPEATEDLY_VALIDATED.
"""

from typing import Dict, Any, Tuple
from pointer_algorithms.knowledge.knowledge_store import KnowledgeStore, AlgorithmicRule, ConfidenceLevel
from pointer_algorithms.learning.validation import CrossProblemValidator

class KnowledgeUpdateManager:

    @staticmethod
    def attempt_promotion(store: KnowledgeStore, rule: AlgorithmicRule) -> Tuple[bool, str, AlgorithmicRule]:
        """
        Runs cross-problem validation gate.
        If passes, upgrades confidence level and saves to store.
        If fails, discards or marks rejected.
        """
        val_result = CrossProblemValidator.validate_rule(rule)

        if val_result["all_passed"]:
            # Upgrade confidence level
            if rule.confidence_level == ConfidenceLevel.CANDIDATE:
                rule.confidence_level = ConfidenceLevel.VALIDATED
                rule.validation_count = 2
            elif rule.confidence_level == ConfidenceLevel.VALIDATED:
                rule.confidence_level = ConfidenceLevel.REPEATEDLY_VALIDATED
                rule.validation_count += 1

            store.add_rule(rule)
            msg = f"Rule '{rule.rule_id}' passed cross-problem validation across {val_result['total_tests']} tests. Promoted to {rule.confidence_level.value}."
            return True, msg, rule
        else:
            msg = f"Rule '{rule.rule_id}' FAILED cross-problem validation ({val_result['passed_tests']}/{val_result['total_tests']}). Promotion rejected."
            return False, msg, rule
