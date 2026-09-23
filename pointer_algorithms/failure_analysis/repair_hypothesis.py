"""
Diagnostic Repair Hypothesis Generator.

Generates reasoned diagnostic hypotheses rather than applying unconstrained ad-hoc patches.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from pointer_algorithms.failure_analysis.classifier import FailureClassification, FailureCategory

@dataclass
class RepairHypothesis:
    hypothesis_id: str
    failure_category: FailureCategory
    hypothesis_statement: str
    missing_rule_description: str
    recommended_action: str
    verification_requirement: str

class RepairHypothesisGenerator:

    @staticmethod
    def generate(classification: FailureClassification, problem_features: Dict[str, Any]) -> RepairHypothesis:
        cat = classification.category

        if cat == FailureCategory.WINDOW_NOT_MONOTONIC:
            return RepairHypothesis(
                hypothesis_id="HYP_WINDOW_NOT_MONOTONIC",
                failure_category=cat,
                hypothesis_statement="Sliding window validity predicate cannot be monotonically restored by left-pointer shrinking because values include negative numbers.",
                missing_rule_description="Rule must state: when tracking sum over contiguous segments, negative values break monotonic window shrinking; Prefix Sum + Hash Map must be selected.",
                recommended_action="Reject sliding window candidate; select Prefix Sum + Hash Map approach.",
                verification_requirement="Re-evaluate candidate selection across positive, negative, and mixed test cases."
            )

        if cat == FailureCategory.LOSS_OF_INFORMATION:
            return RepairHypothesis(
                hypothesis_id="HYP_INDEX_LOSS",
                failure_category=cat,
                hypothesis_statement="Sorting destroyed original element positions required for problem output.",
                missing_rule_description="Rule must state: if output requires original indices, sorting must be performed on vector<pair<value, original_index>> or hash-based lookup must be chosen.",
                recommended_action="Wrap input elements in (value, original_index) pairs before sorting, or use Hash Map.",
                verification_requirement="Verify that 1-based original indices match on both sorted and unsorted test inputs."
            )

        if cat == FailureCategory.WRONG_ALGORITHM:
            return RepairHypothesis(
                hypothesis_id="HYP_WRONG_ALGORITHM",
                failure_category=cat,
                hypothesis_statement="The computational requirements of this problem (e.g. dynamic updates) cannot be satisfied in O(N) by static two-pointer scans.",
                missing_rule_description="Rule must reject Two Pointers when point updates are interleaved with range queries.",
                recommended_action="Classify as compound unsupported or delegate to tree-based range structure.",
                verification_requirement="Confirm negative rejection across query-update benchmark problems."
            )

        return RepairHypothesis(
            hypothesis_id="HYP_GENERIC_IMPLEMENTATION",
            failure_category=cat,
            hypothesis_statement="Pointer movement stalled or terminated at an off-by-one boundary.",
            missing_rule_description="Check boundary termination condition (e.g. <= vs <).",
            recommended_action="Inspect loop termination predicate.",
            verification_requirement="Re-run edge case generator on 0, 1, 2-element inputs."
        )
