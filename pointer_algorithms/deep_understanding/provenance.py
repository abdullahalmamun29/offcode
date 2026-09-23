"""
CHUP Phase 6 — Formal Provenance Graph & Traceability.

Guarantees complete mathematical traceability for every fact derived in Phase 6.
Every fact that enters Phase 5 must be grounded in an immutable ProvenanceNode
referencing valid source facts, a formal derivation rule, and a non-empty witness.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from pointer_algorithms.deep_understanding.fact_model import ProofStatus


@dataclass(frozen=True)
class ProvenanceNode:
    """
    Immutable provenance record documenting the origin and derivation of a fact.
    """
    node_id: str
    target_fact_id: str
    source_fact_ids: Tuple[str, ...]
    derivation_rule: str
    proof_status: ProofStatus
    witness: str

    def is_valid(self) -> bool:
        return bool(self.node_id and self.target_fact_id and self.derivation_rule and self.witness)


class ProvenanceGraph:
    """
    Directed Acyclic Graph recording all derivation steps.
    Enforces auditability and cycle-free proof lineages.
    """

    def __init__(self):
        self._nodes: Dict[str, ProvenanceNode] = {}
        self._fact_to_node: Dict[str, str] = {}

    @property
    def nodes(self) -> Dict[str, ProvenanceNode]:
        return self._nodes

    def add_node(self, node: ProvenanceNode) -> None:
        if not node.is_valid():
            raise ValueError(f"Invalid ProvenanceNode: {node}")
        self._nodes[node.node_id] = node
        self._fact_to_node[node.target_fact_id] = node.node_id

    def get_node(self, node_id: str) -> Optional[ProvenanceNode]:
        return self._nodes.get(node_id)

    def get_node_for_fact(self, fact_id: str) -> Optional[ProvenanceNode]:
        node_id = self._fact_to_node.get(fact_id)
        if node_id:
            return self._nodes.get(node_id)
        return None

    def get_ancestors(self, fact_id: str) -> List[ProvenanceNode]:
        """
        Traverses provenance graph backwards to gather all contributing nodes.
        Detects cycles to guarantee DAG invariant.
        """
        ancestors: List[ProvenanceNode] = []
        visited: Set[str] = set()
        active_stack: Set[str] = set()

        def dfs(current_fact_id: str):
            node_id = self._fact_to_node.get(current_fact_id)
            if not node_id:
                return
            if node_id in active_stack:
                raise ValueError(f"Circular derivation detected in ProvenanceGraph involving node {node_id}")
            if node_id in visited:
                return

            visited.add(node_id)
            active_stack.add(node_id)

            node = self._nodes[node_id]
            for src_id in node.source_fact_ids:
                dfs(src_id)

            active_stack.remove(node_id)
            ancestors.append(node)

        dfs(fact_id)
        return ancestors

    def verify_trace(self, fact_id: str) -> bool:
        """
        Verifies that every step in the ancestry chain is PROVEN and valid.
        """
        try:
            ancestors = self.get_ancestors(fact_id)
        except ValueError:
            return False

        if not ancestors:
            # Source observation without derivation node
            return self._fact_to_node.get(fact_id) is not None

        return all(node.proof_status == ProofStatus.PROVEN and node.is_valid() for node in ancestors)

    def format_audit_trail(self, fact_id: str) -> str:
        """
        Produces human-readable markdown audit trail of the fact's derivation.
        """
        try:
            ancestors = self.get_ancestors(fact_id)
        except Exception as e:
            return f"Error retrieving audit trail: {e}"

        if not ancestors:
            return f"Fact {fact_id}: Direct observation with no derivation steps."

        lines = [f"### Provenance Audit Trail for Fact: {fact_id}"]
        for idx, node in enumerate(ancestors, start=1):
            src_str = ", ".join(node.source_fact_ids) if node.source_fact_ids else "None (Initial Observation)"
            lines.append(
                f"{idx}. **Node {node.node_id}** -> Target: `{node.target_fact_id}`\n"
                f"   - Rule: `{node.derivation_rule}`\n"
                f"   - Status: `{node.proof_status.value}`\n"
                f"   - Sources: [{src_str}]\n"
                f"   - Witness: *\"{node.witness}\"*"
            )
        return "\n".join(lines)
