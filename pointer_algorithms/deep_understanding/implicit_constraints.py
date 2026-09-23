"""
CHUP Phase 6 — Implicit Constraints Inferrer.

Deduces implicit mathematical constraints from observed facts using the
authoritative DerivationRuleRegistry.

Core Soundness Guarantees:
1. TREE topology is derived ONLY from the full theorem: E = V - 1, connected, undirected, simple.
   (E = V - 1 alone never implies Tree).
2. Large coordinates (<= 10^18) derive DENSE_INDEX_SPACE_UNAVAILABLE ONLY when combined
   with coordinate querying/indexing and memory infeasibility. (Coordinates alone never dictate algorithms).
3. Non-negative edge weights establish compatibility, NEVER prescribing Dijkstra.
4. Negative weights establish absence of monotonicity, NEVER triggering false global UNSAT.
"""

from typing import List, Tuple, Optional
import uuid
from pointer_algorithms.deep_understanding.fact_model import (
    SemanticFact,
    FactSet,
    FactTier,
    ProofStatus,
    AmbiguityStatus
)
from pointer_algorithms.deep_understanding.rule_registry import (
    DerivationRuleRegistry,
    DerivationRule
)
from pointer_algorithms.deep_understanding.provenance import (
    ProvenanceNode,
    ProvenanceGraph
)


class ImplicitConstraintInferrer:
    """
    Applies registered axiomatic rules to infer implicit constraints with full provenance.
    """

    def __init__(self, registry: Optional[DerivationRuleRegistry] = None):
        self.registry = registry or DerivationRuleRegistry()

    def infer_constraints(
        self,
        facts: FactSet,
        provenance_graph: ProvenanceGraph
    ) -> List[SemanticFact]:
        """
        Executes applicable derivation rules and returns new PROVEN derived facts.
        """
        new_facts: List[SemanticFact] = []
        current_facts = list(facts.facts)

        applicable_rules = self.registry.find_applicable_rules(facts)
        for rule in applicable_rules:
            # If the fact is already proven, skip re-derivation
            if facts.has_proven(rule.produced_fact_name):
                continue

            eval_res = rule.evaluate(facts)
            if eval_res is not None:
                val, witness = eval_res
                fact_id = f"fact_derived_{uuid.uuid4().hex[:8]}"
                prov_id = f"prov_{uuid.uuid4().hex[:8]}"

                # Collect source fact IDs
                src_ids = tuple(
                    f.fact_id for f in facts
                    if f.name in rule.required_fact_names
                )

                prov_node = ProvenanceNode(
                    node_id=prov_id,
                    target_fact_id=fact_id,
                    source_fact_ids=src_ids,
                    derivation_rule=rule.rule_id,
                    proof_status=ProofStatus.PROVEN,
                    witness=f"[{rule.name}] {witness} Proof basis: {rule.proof_basis}"
                )
                provenance_graph.add_node(prov_node)

                derived_fact = SemanticFact(
                    fact_id=fact_id,
                    tier=FactTier.DERIVED_FACT,
                    name=rule.produced_fact_name,
                    value=val,
                    proof_status=ProofStatus.PROVEN,
                    ambiguity=AmbiguityStatus.UNAMBIGUOUS,
                    provenance_id=prov_id,
                    witness=witness
                )
                new_facts.append(derived_fact)

        return new_facts
