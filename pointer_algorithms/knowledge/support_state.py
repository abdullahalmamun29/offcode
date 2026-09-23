"""
Sector D — Explicit Support State Machine.

Classifies problem support into 5 explicit states:
1. SUPPORTED: Canonical and directly solvable by validated rules.
2. SUPPORTED_WITH_COMPOSITION: Solved by composing 2 or more known concepts.
3. PARTIALLY_SUPPORTED: Core concept understood, but missing domain-specific sub-routine.
4. INSUFFICIENT_KNOWLEDGE: Valid problem recognized, but required paradigm is outside validated knowledge.
5. UNSUPPORTED: Mathematically impossible, contradictory constraints, or unmodellable.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

class SupportState(str, Enum):
    SUPPORTED = "SUPPORTED"
    SUPPORTED_WITH_COMPOSITION = "SUPPORTED_WITH_COMPOSITION"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    INSUFFICIENT_KNOWLEDGE = "INSUFFICIENT_KNOWLEDGE"
    UNSUPPORTED = "UNSUPPORTED"

@dataclass
class SupportAssessment:
    state: SupportState
    concept: Optional[str]
    is_solvable: bool
    explanation: str
    missing_capabilities: List[str]
    suggested_alternatives: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "state": self.state.value,
            "concept": self.concept,
            "is_solvable": self.is_solvable,
            "explanation": self.explanation,
            "missing_capabilities": self.missing_capabilities,
            "suggested_alternatives": self.suggested_alternatives,
        }

class SupportDetector:
    """Detects the support boundaries of CHUP without fabricating code for unsupported problems."""

    @staticmethod
    def assess(
        selected_pattern: Optional[str],
        is_composed: bool,
        eliminated_reasons: List[str],
        is_known_gap: bool = False,
        gap_name: Optional[str] = None
    ) -> SupportAssessment:
        if is_known_gap:
            return SupportAssessment(
                state=SupportState.INSUFFICIENT_KNOWLEDGE,
                concept=gap_name,
                is_solvable=False,
                explanation=f"The required concept '{gap_name}' is outside CHUP's current validated knowledge base.",
                missing_capabilities=[gap_name or "unknown_domain"],
                suggested_alternatives=[]
            )

        if not selected_pattern:
            # Check if elimination indicated impossible/unsupported
            if "DYNAMIC_UPDATES_PRESENT" in eliminated_reasons:
                return SupportAssessment(
                    state=SupportState.INSUFFICIENT_KNOWLEDGE,
                    concept="dynamic_segment_tree",
                    is_solvable=False,
                    explanation="Problem requires dynamic point updates with range queries; static two pointers is invalid.",
                    missing_capabilities=["segment_tree_with_lazy_propagation"],
                    suggested_alternatives=["prefix_sum_hash_map"]
                )
            if "WINDOW_NOT_MONOTONIC" in eliminated_reasons:
                return SupportAssessment(
                    state=SupportState.SUPPORTED_WITH_COMPOSITION,
                    concept="prefix_sum_hash_map",
                    is_solvable=True,
                    explanation="Negative values break window sum monotonicity; fallback to prefix sums + hash table composition.",
                    missing_capabilities=[],
                    suggested_alternatives=["prefix_sum_hash_map"]
                )
            return SupportAssessment(
                state=SupportState.UNSUPPORTED,
                concept=None,
                is_solvable=False,
                explanation="Problem constraints violate fundamental algorithmic invariants with no viable alternative.",
                missing_capabilities=["unconstrained_arbitrary_search"],
                suggested_alternatives=[]
            )

        if is_composed:
            return SupportAssessment(
                state=SupportState.SUPPORTED_WITH_COMPOSITION,
                concept=selected_pattern,
                is_solvable=True,
                explanation=f"Solved via multi-concept composition using {selected_pattern}.",
                missing_capabilities=[],
                suggested_alternatives=[]
            )

        return SupportAssessment(
            state=SupportState.SUPPORTED,
            concept=selected_pattern,
            is_solvable=True,
            explanation=f"Canonical solution available for {selected_pattern}.",
            missing_capabilities=[],
            suggested_alternatives=[]
        )
