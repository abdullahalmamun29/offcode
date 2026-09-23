"""
Sector H — Relational Knowledge Graph for Algorithmic Concepts.

Defines formal relationships:
- PARENT_CONCEPT
- SPECIALIZATION_OF
- COMPOSES_WITH
- ALTERNATIVE_TO
- REQUIRES
- CONFLICTS_WITH
- GENERALIZES
- SPECIAL_CASE_OF
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set

class RelationType(str, Enum):
    PARENT_CONCEPT = "PARENT_CONCEPT"
    SPECIALIZATION_OF = "SPECIALIZATION_OF"
    COMPOSES_WITH = "COMPOSES_WITH"
    ALTERNATIVE_TO = "ALTERNATIVE_TO"
    REQUIRES = "REQUIRES"
    CONFLICTS_WITH = "CONFLICTS_WITH"
    GENERALIZES = "GENERALIZES"
    SPECIAL_CASE_OF = "SPECIAL_CASE_OF"

@dataclass
class KnowledgeEdge:
    source: str
    relation: RelationType
    target: str
    rationale: str
    metadata: Dict[str, Any] = field(default_factory=dict)

class KnowledgeGraph:
    """Directed graph of algorithmic concepts and structural relations."""

    def __init__(self):
        self.edges: List[KnowledgeEdge] = []
        self._concept_edges: Dict[str, List[KnowledgeEdge]] = {}
        self._build_core_relations()

    def add_edge(self, source: str, relation: RelationType, target: str, rationale: str, **metadata):
        edge = KnowledgeEdge(source=source, relation=relation, target=target, rationale=rationale, metadata=metadata)
        self.edges.append(edge)
        if source not in self._concept_edges:
            self._concept_edges[source] = []
        self._concept_edges[source].append(edge)

    def get_relations(self, concept: str, rel_type: Optional[RelationType] = None) -> List[KnowledgeEdge]:
        out = self._concept_edges.get(concept, [])
        if rel_type:
            return [e for e in out if e.relation == rel_type]
        return out

    def get_conflicts(self, concept: str) -> List[KnowledgeEdge]:
        return self.get_relations(concept, RelationType.CONFLICTS_WITH)

    def get_compositions(self, concept: str) -> List[KnowledgeEdge]:
        return self.get_relations(concept, RelationType.COMPOSES_WITH)

    def get_alternatives(self, concept: str) -> List[KnowledgeEdge]:
        return self.get_relations(concept, RelationType.ALTERNATIVE_TO)

    def _build_core_relations(self):
        # ── Two Pointers Core Relationships ──
        self.add_edge(
            "two_pointers", RelationType.PARENT_CONCEPT, "pointer_algorithms",
            "Two pointers is the foundational technique of bounded sequence index manipulation."
        )
        self.add_edge(
            "two_pointers_converging", RelationType.SPECIALIZATION_OF, "two_pointers",
            "Opposite-direction converging inward elimination."
        )
        self.add_edge(
            "two_pointers_same_direction", RelationType.SPECIALIZATION_OF, "two_pointers",
            "Same-direction fast-slow runner or chasing pointers."
        )
        self.add_edge(
            "sliding_window", RelationType.SPECIALIZATION_OF, "two_pointers",
            "Contiguous window state expansion and contraction."
        )
        self.add_edge(
            "counting_pointers", RelationType.SPECIALIZATION_OF, "two_pointers",
            "Combinatorial pair and subarray counting using monotonic boundary advances."
        )

        # ── Requirements & Invariants ──
        self.add_edge(
            "pair_sum_sorted", RelationType.REQUIRES, "sorted_order",
            "Pair sum elimination requires value-order monotonicity to safely discard candidate endpoints."
        )
        self.add_edge(
            "sliding_window_variable_min", RelationType.REQUIRES, "monotonic_window_state",
            "Shrinking left pointer must monotonically reverse validity condition."
        )
        self.add_edge(
            "sliding_window_sum", RelationType.CONFLICTS_WITH, "arbitrary_negative_values",
            "Negative numbers break window sum monotonicity, causing greedy shrinking to be invalid."
        )
        self.add_edge(
            "two_pointers", RelationType.CONFLICTS_WITH, "dynamic_point_updates",
            "Pointer traversal assumes static sequence state during walk."
        )
        self.add_edge(
            "sliding_window", RelationType.CONFLICTS_WITH, "non_contiguous_subsequence",
            "Sliding window operates strictly over contiguous subarrays."
        )

        # ── Compositions ──
        self.add_edge(
            "three_sum_converging", RelationType.COMPOSES_WITH, "sorting",
            "Sorts array first, then fixes outer element and runs converging two pointers."
        )
        self.add_edge(
            "minimum_window_substring", RelationType.COMPOSES_WITH, "frequency_hash_map",
            "Tracks target character counts and window match scalar."
        )
        self.add_edge(
            "exact_count_derived", RelationType.COMPOSES_WITH, "at_most_k_sliding_window",
            "Transforms exact K constraint into atMost(K) - atMost(K-1) monotonic windows."
        )

        # ── Alternatives ──
        self.add_edge(
            "pair_sum_sorted", RelationType.ALTERNATIVE_TO, "hash_map_pair_lookup",
            "When array is already sorted, two pointers achieves O(1) space vs O(N) space for hash set."
        )
        self.add_edge(
            "sliding_window_sum", RelationType.ALTERNATIVE_TO, "prefix_sum_hash_map",
            "Prefix sum + hash map handles arbitrary negative numbers when sliding window fails."
        )
        self.add_edge(
            "sliding_window_extremum", RelationType.COMPOSES_WITH, "monotonic_deque",
            "Monotonic deque maintains running maximum/minimum in O(N) total time."
        )

RELATIONAL_GRAPH = KnowledgeGraph()
