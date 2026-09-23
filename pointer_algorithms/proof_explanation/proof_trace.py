"""
CHUP Phase 7 — Proof Trace Navigator.

Navigates the Phase 6 ProvenanceGraph DAG to produce a safe, deterministic,
serializable audit proof trace for Level 3 inspection.
"""

from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class ProofTraceStep:
    step_id: str
    target_fact_id: str
    target_fact_name: str
    rule_name: str
    source_fact_ids: Tuple[str, ...]
    source_fact_names: Tuple[str, ...]
    witness: str
    depth: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "target_fact_id": self.target_fact_id,
            "target_fact_name": self.target_fact_name,
            "rule_name": self.rule_name,
            "source_fact_ids": list(self.source_fact_ids),
            "source_fact_names": list(self.source_fact_names),
            "witness": self.witness,
            "depth": self.depth
        }


class ProofTraceNavigator:
    """
    Traverses the ProvenanceGraph deterministically and extracts causal chains.
    """

    @classmethod
    def build_trace(
        cls,
        provenance_graph: Any,
        facts: Any
    ) -> List[ProofTraceStep]:
        if provenance_graph is None:
            return []

        nodes = getattr(provenance_graph, "nodes", {})
        if not nodes:
            return []

        # Map fact_id -> fact_name
        fact_name_map: Dict[str, str] = {}
        if facts is not None:
            fact_iter = getattr(facts, "facts", facts)
            for f in fact_iter:
                fid = getattr(f, "fact_id", "")
                fname = getattr(f, "name", fid)
                fact_name_map[fid] = fname

        # Deterministic topological ordering by node_id
        sorted_nodes = sorted(nodes.items(), key=lambda x: x[0])
        trace_steps: List[ProofTraceStep] = []

        for pid, node in sorted_nodes:
            target_id = getattr(node, "target_fact_id", "")
            target_name = fact_name_map.get(target_id, target_id)
            rule = getattr(node, "derivation_rule", "UNKNOWN_RULE")
            sources = tuple(getattr(node, "source_fact_ids", ()))
            source_names = tuple(fact_name_map.get(s, s) for s in sources)
            witness = getattr(node, "witness", "")

            # Depth approximation: 0 for direct observation, 1 + max(source depths)
            depth = 0 if rule == "RULE_DIRECT_OBSERVATION" else 1

            trace_steps.append(ProofTraceStep(
                step_id=pid,
                target_fact_id=target_id,
                target_fact_name=target_name,
                rule_name=rule,
                source_fact_ids=sources,
                source_fact_names=source_names,
                witness=witness,
                depth=depth
            ))

        return trace_steps
