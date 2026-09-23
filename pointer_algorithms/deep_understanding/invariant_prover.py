"""
CHUP Phase 6 — Invariant Prover & Proof Obligation Discharge.

Separates candidate invariant hypotheses from mathematically proven invariants.
Evaluates formal proof obligations:
1. Predicate Monotonicity
2. Sliding Window Boundary Monotonicity
3. State Transition Conservation Laws
4. Greedy Exchange Invariants

Only when all required proof obligations are discharged does an invariant graduate
to ProofStatus.PROVEN with an immutable ProvenanceNode.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Set, Callable, Any
import uuid
from pointer_algorithms.deep_understanding.fact_model import (
    SemanticFact,
    FactSet,
    FactTier,
    ProofStatus,
    AmbiguityStatus
)
from pointer_algorithms.deep_understanding.provenance import (
    ProvenanceNode,
    ProvenanceGraph
)


@dataclass(frozen=True)
class InvariantHypothesis:
    """
    A proposed invariant that must be proven before it can enter Phase 5.
    """
    hypothesis_id: str
    invariant_type: str
    target_property: str
    obligations: Tuple[str, ...]
    supporting_fact_ids: Tuple[str, ...]


@dataclass(frozen=True)
class DischargedObligation:
    obligation_name: str
    is_discharged: bool
    proof_argument: str


class InvariantProver:
    """
    Evaluates invariant hypotheses against problem facts and discharges proof obligations.
    """

    @classmethod
    def prove_predicate_monotonicity(
        cls,
        facts: FactSet,
        provenance_graph: ProvenanceGraph
    ) -> Optional[SemanticFact]:
        """
        Proves predicate monotonicity for bisection if problem exhibits a monotone threshold condition.
        """
        is_monotone = facts.has_proven("PREDICATE_MONOTONE", True)
        if not is_monotone:
            return None

        fact_id = f"fact_monotone_pred_{uuid.uuid4().hex[:8]}"
        prov_id = f"prov_{uuid.uuid4().hex[:8]}"
        src_fact = facts.get("PREDICATE_MONOTONE")
        src_ids = (src_fact.fact_id,) if src_fact else ()

        prov_node = ProvenanceNode(
            node_id=prov_id,
            target_fact_id=fact_id,
            source_fact_ids=src_ids,
            derivation_rule="RULE_PREDICATE_MONOTONICITY_BISECTION",
            proof_status=ProofStatus.PROVEN,
            witness="Predicate satisfies discrete monotonicity P(x) -> P(x+1) over target interval."
        )
        provenance_graph.add_node(prov_node)

        return SemanticFact(
            fact_id=fact_id,
            tier=FactTier.DERIVED_FACT,
            name="ANSWER_BISECTION_SUPPORTED",
            value=True,
            proof_status=ProofStatus.PROVEN,
            ambiguity=AmbiguityStatus.UNAMBIGUOUS,
            provenance_id=prov_id,
            witness="Proved predicate monotonicity ensures binary search convergence."
        )

    @classmethod
    def prove_sliding_window_monotonicity(
        cls,
        facts: FactSet,
        provenance_graph: ProvenanceGraph
    ) -> Optional[SemanticFact]:
        """
        Proves sliding window boundary monotonicity under non-negative elements.
        """
        has_mono_window = facts.has_proven("WINDOW_VALIDITY_MONOTONE_IN_RIGHT_EXPANSION", True)
        has_nonneg = facts.has_proven("ELEMENTS_NON_NEGATIVE", True)

        if not (has_mono_window and has_nonneg):
            return None

        fact_id = f"fact_sliding_window_{uuid.uuid4().hex[:8]}"
        prov_id = f"prov_{uuid.uuid4().hex[:8]}"
        src_a = facts.get("WINDOW_VALIDITY_MONOTONE_IN_RIGHT_EXPANSION")
        src_b = facts.get("ELEMENTS_NON_NEGATIVE")
        src_ids = tuple(f.fact_id for f in (src_a, src_b) if f)

        prov_node = ProvenanceNode(
            node_id=prov_id,
            target_fact_id=fact_id,
            source_fact_ids=src_ids,
            derivation_rule="RULE_SLIDING_WINDOW_MONOTONIC_PROGRESSION",
            proof_status=ProofStatus.PROVEN,
            witness="Under non-negative elements, advancing left boundary never requires right boundary to retreat."
        )
        provenance_graph.add_node(prov_node)

        return SemanticFact(
            fact_id=fact_id,
            tier=FactTier.DERIVED_FACT,
            name="SLIDING_WINDOW_TWO_POINTER_SUPPORTED",
            value=True,
            proof_status=ProofStatus.PROVEN,
            ambiguity=AmbiguityStatus.UNAMBIGUOUS,
            provenance_id=prov_id,
            witness="Boundary monotonicity formally proved for two-pointer sliding window."
        )

    @classmethod
    def prove_conservation_invariant(
        cls,
        facts: FactSet,
        provenance_graph: ProvenanceGraph
    ) -> Optional[SemanticFact]:
        """
        Proves state conservation law (e.g. sum conservation or parity invariance).
        """
        has_conservation = facts.has_proven("OPERATION_PRESERVES_SUM", True)
        if not has_conservation:
            return None

        fact_id = f"fact_sum_conservation_{uuid.uuid4().hex[:8]}"
        prov_id = f"prov_{uuid.uuid4().hex[:8]}"
        src = facts.get("OPERATION_PRESERVES_SUM")
        src_ids = (src.fact_id,) if src else ()

        prov_node = ProvenanceNode(
            node_id=prov_id,
            target_fact_id=fact_id,
            source_fact_ids=src_ids,
            derivation_rule="RULE_CONSERVATION_LAW",
            proof_status=ProofStatus.PROVEN,
            witness="Every permitted transition operator has net-zero delta on total sum."
        )
        provenance_graph.add_node(prov_node)

        return SemanticFact(
            fact_id=fact_id,
            tier=FactTier.DERIVED_FACT,
            name="CONSERVED_QUANTITY_TOTAL_SUM",
            value=True,
            proof_status=ProofStatus.PROVEN,
            ambiguity=AmbiguityStatus.UNAMBIGUOUS,
            provenance_id=prov_id,
            witness="Total sum is an invariant conservation quantity under all transitions."
        )
