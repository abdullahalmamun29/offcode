"""
CHUP Phase 6 — Operation Semantics & Algebraic Properties.

Decouples:
1. Pure Algebraic Properties (Associativity, Commutativity, Invertibility, Idempotence)
2. Structural Consequences (Prefix Derivability, Overlapping Interval Immunity)
3. Data Structure Capabilities (Prefix Sum O(1), Fenwick O(log N), Sparse Table O(1))

Guarantees that algebraic properties entail mathematical consequences without
prescribing specific data structures or confusing algebraic capabilities with
complexity bounds.
"""

from dataclasses import dataclass
from typing import Optional, List, Tuple
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
from pointer_algorithms.multi_constraint.aggregate_ontology import AggregateSpec


@dataclass(frozen=True)
class AlgebraicSignature:
    """
    Formal algebraic signature of an operation.
    """
    operation_name: str
    is_associative: bool
    is_commutative: bool
    is_invertible: bool
    is_idempotent: bool
    is_reversible: bool
    identity_element: Optional[int] = None


class OperationSemanticsEngine:
    """
    Deduces structural query consequences from algebraic operation semantics.
    """

    KNOWN_SIGNATURES = {
        "SUM": AlgebraicSignature("SUM", True, True, True, False, True, 0),
        "XOR": AlgebraicSignature("XOR", True, True, True, True, True, 0),  # self-inverse and idempotent
        "MIN": AlgebraicSignature("MIN", True, True, False, True, False, None),
        "MAX": AlgebraicSignature("MAX", True, True, False, True, False, None),
        "GCD": AlgebraicSignature("GCD", True, True, False, True, False, 0),
    }

    @classmethod
    def deduce_algebraic_capabilities(
        cls,
        operation_name: str,
        facts: FactSet,
        provenance_graph: ProvenanceGraph
    ) -> Tuple[List[SemanticFact], AggregateSpec]:
        """
        Deduces structural consequences from the algebraic properties of the operation.
        Returns derived semantic facts and an authoritative AggregateSpec for Phase 5.
        """
        sig = cls.KNOWN_SIGNATURES.get(operation_name.upper())
        if sig is None:
            # Default uninterpreted operation
            sig = AlgebraicSignature(operation_name, True, False, False, False, False, None)

        derived_facts: List[SemanticFact] = []

        # 1. Invertibility -> Prefix derivability
        if sig.is_invertible:
            fact_id = f"fact_invertible_{uuid.uuid4().hex[:8]}"
            prov_id = f"prov_{uuid.uuid4().hex[:8]}"
            prov_node = ProvenanceNode(
                node_id=prov_id,
                target_fact_id=fact_id,
                source_fact_ids=(),
                derivation_rule="RULE_ALGEBRAIC_INVERTIBILITY_PREFIX_REDUCTION",
                proof_status=ProofStatus.PROVEN,
                witness=f"Operation {operation_name} possesses group invertibility: sum(L..R) = prefix(R) - prefix(L-1)."
            )
            provenance_graph.add_node(prov_node)

            derived_facts.append(SemanticFact(
                fact_id=fact_id,
                tier=FactTier.CAPABILITY_CONSEQUENCE,
                name="RANGE_DERIVABLE_FROM_PREFIXES",
                value=True,
                proof_status=ProofStatus.PROVEN,
                ambiguity=AmbiguityStatus.UNAMBIGUOUS,
                provenance_id=prov_id,
                witness=f"Invertible operation {operation_name} enables prefix difference extraction."
            ))

        # 2. Idempotence -> Overlapping interval immunity
        if sig.is_idempotent:
            is_static = facts.has_proven("STATIC_DATA_WITHOUT_UPDATES", True)
            fact_id = f"fact_idempotent_{uuid.uuid4().hex[:8]}"
            prov_id = f"prov_{uuid.uuid4().hex[:8]}"
            prov_node = ProvenanceNode(
                node_id=prov_id,
                target_fact_id=fact_id,
                source_fact_ids=(),
                derivation_rule="RULE_ALGEBRAIC_IDEMPOTENCE_OVERLAP_REDUCTION",
                proof_status=ProofStatus.PROVEN,
                witness=f"Operation {operation_name} is idempotent (x * x = x), permitting overlapping interval union."
            )
            provenance_graph.add_node(prov_node)

            derived_facts.append(SemanticFact(
                fact_id=fact_id,
                tier=FactTier.CAPABILITY_CONSEQUENCE,
                name="OVERLAPPING_INTERVAL_QUERY_SUPPORTED",
                value=True,
                proof_status=ProofStatus.PROVEN,
                ambiguity=AmbiguityStatus.UNAMBIGUOUS,
                provenance_id=prov_id,
                witness=f"Idempotent operation {operation_name} prevents double-counting over overlapping ranges."
            ))

        # 3. Build canonical Phase 5 AggregateSpec
        agg_spec = AggregateSpec(
            operation_name=operation_name.upper(),
            identity_element=sig.identity_element,
            is_associative=sig.is_associative,
            is_commutative=sig.is_commutative,
            is_idempotent=sig.is_idempotent,
            is_invertible=sig.is_invertible,
            supports_merge=sig.is_associative,
            supports_lazy_update=False,
            supports_order_statistics=(operation_name.upper() in ("KTH", "MEDIAN"))
        )

        return derived_facts, agg_spec
