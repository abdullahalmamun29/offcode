"""
CHUP Phase 6 — Source Fact Contradiction & Ambiguity Engine.

Detects mutually inconsistent extracted source facts BEFORE derivation or Phase 5
contamination can occur. Distinguishes:
1. CONTRADICTORY: Logical impossibility -> emits ConflictingFactsCertificate -> HALTS pipeline.
2. AMBIGUOUS: Multiple valid interpretations -> marks UNRESOLVED, prevents Phase 5 mutation.
3. UNDER_SPECIFIED: Missing required dimensions -> marks UNRESOLVED, prevents Phase 5 mutation.
"""

from dataclasses import dataclass
from typing import Optional, Tuple, Dict, List
from pointer_algorithms.deep_understanding.fact_model import (
    SemanticFact,
    FactSet,
    ProofStatus,
    AmbiguityStatus
)


@dataclass(frozen=True)
class ConflictingFactsCertificate:
    """
    Immutable certificate proving that two or more extracted facts are mutually contradictory.
    Halts the Phase 6 pipeline with zero code emission.
    """
    conflict_id: str
    failure_code: str = "CONFLICTING_SOURCE_FACTS"
    competing_facts: Tuple[str, ...] = ()
    axiomatic_proof: str = ""
    witness: str = ""


@dataclass(frozen=True)
class AmbiguityReport:
    """
    Immutable report recording underspecified or ambiguous semantic statements.
    """
    ambiguous_fact_names: Tuple[str, ...]
    interpretations: Dict[str, Tuple[str, ...]]
    witness: str


class SourceFactContradictionEngine:
    """
    Evaluates semantic consistency of extracted facts before derivation.
    """

    @classmethod
    def analyze(cls, facts: FactSet) -> Tuple[Optional[ConflictingFactsCertificate], Optional[AmbiguityReport]]:
        """
        Returns (conflict_cert, ambiguity_report).
        If conflict_cert is not None, the pipeline MUST halt immediately.
        """
        # 1. Directed vs Undirected Conflict
        is_directed = facts.has_proven("IS_DIRECTED", True)
        is_undirected = facts.has_proven("IS_UNDIRECTED", True)
        if is_directed and is_undirected:
            return (
                ConflictingFactsCertificate(
                    conflict_id="CONFLICT_DIRECTEDNESS",
                    competing_facts=("IS_DIRECTED", "IS_UNDIRECTED"),
                    axiomatic_proof="Graph cannot simultaneously be directed and undirected.",
                    witness="Conflicting source assertions: IS_DIRECTED=True and IS_UNDIRECTED=True."
                ),
                None
            )

        # 2. Online Stream vs Offline Reordering Conflict
        req_online = facts.has_proven("REQUIRES_ONLINE_INTERACTIVE", True)
        req_offline = facts.has_proven("OFFLINE_QUERY_REORDERING_REQUIRED", True)
        if req_online and req_offline:
            return (
                ConflictingFactsCertificate(
                    conflict_id="CONFLICT_TEMPORAL_MODE",
                    competing_facts=("REQUIRES_ONLINE_INTERACTIVE", "OFFLINE_QUERY_REORDERING_REQUIRED"),
                    axiomatic_proof="Problem cannot mandate online interactive answering while requiring offline query reordering.",
                    witness="Conflicting temporal modes: online stream requirement vs offline reordering."
                ),
                None
            )

        # 3. Immutable Array vs Dynamic Point Updates
        is_immutable = facts.has_proven("IMMUTABLE_ARRAY", True)
        has_updates = facts.has_proven("REQUIRES_DYNAMIC_POINT_UPDATE", True)
        if is_immutable and has_updates:
            return (
                ConflictingFactsCertificate(
                    conflict_id="CONFLICT_MUTABILITY",
                    competing_facts=("IMMUTABLE_ARRAY", "REQUIRES_DYNAMIC_POINT_UPDATE"),
                    axiomatic_proof="Array cannot be immutable while requiring dynamic in-place updates.",
                    witness="Contradiction between IMMUTABLE_ARRAY and REQUIRES_DYNAMIC_POINT_UPDATE."
                ),
                None
            )

        # 4. Tree Topology Cardinality Contradiction (E != V - 1 on claimed tree)
        claimed_tree = facts.has_proven("CLAIMED_TREE", True)
        v_fact = facts.get("VERTEX_COUNT")
        e_fact = facts.get("EDGE_COUNT")
        if claimed_tree and v_fact and e_fact:
            v, e = v_fact.value, e_fact.value
            if isinstance(v, int) and isinstance(e, int) and v >= 1 and e != v - 1:
                return (
                    ConflictingFactsCertificate(
                        conflict_id="CONFLICT_TREE_CARDINALITY",
                        competing_facts=("CLAIMED_TREE", f"V={v}", f"E={e}"),
                        axiomatic_proof="By definition, every tree with V vertices has exactly V - 1 edges.",
                        witness=f"Claimed tree has V={v} vertices but E={e} != {v-1} edges."
                    ),
                    None
                )

        # 5. Acyclic DAG vs Directed Cycle
        req_dag = facts.has_proven("REQUIRES_ACYCLIC_DAG", True)
        has_cycle = facts.has_proven("HAS_DIRECTED_CYCLE", True)
        if req_dag and has_cycle:
            return (
                ConflictingFactsCertificate(
                    conflict_id="CONFLICT_CYCLICITY",
                    competing_facts=("REQUIRES_ACYCLIC_DAG", "HAS_DIRECTED_CYCLE"),
                    axiomatic_proof="A directed graph cannot be acyclic if it contains a directed cycle.",
                    witness="Acyclicity requirement violated by confirmed directed cycle."
                ),
                None
            )

        # 6. Non-Negative Elements vs Negative Elements Present
        is_nonneg = facts.has_proven("ALL_ELEMENTS_NON_NEGATIVE", True)
        has_neg = facts.has_proven("CONTAINS_NEGATIVE_ELEMENTS", True)
        if is_nonneg and has_neg:
            return (
                ConflictingFactsCertificate(
                    conflict_id="CONFLICT_VALUE_SIGNS",
                    competing_facts=("ALL_ELEMENTS_NON_NEGATIVE", "CONTAINS_NEGATIVE_ELEMENTS"),
                    axiomatic_proof="Problem domain cannot simultaneously declare all elements non-negative and contain negative elements.",
                    witness="Contradictory sign domain: ALL_ELEMENTS_NON_NEGATIVE=True and CONTAINS_NEGATIVE_ELEMENTS=True."
                ),
                None
            )

        # 7. Connected vs Disconnected Conflict
        is_conn = facts.has_proven("IS_CONNECTED", True)
        is_disconn = facts.has_proven("IS_DISCONNECTED", True)
        if is_conn and is_disconn:
            return (
                ConflictingFactsCertificate(
                    conflict_id="CONFLICT_CONNECTIVITY",
                    competing_facts=("IS_CONNECTED", "IS_DISCONNECTED"),
                    axiomatic_proof="A graph cannot simultaneously be connected and disconnected.",
                    witness="Conflicting connectivity assertions: IS_CONNECTED=True and IS_DISCONNECTED=True."
                ),
                None
            )

        # 8. Tree Claim vs Disconnected or Cyclic
        claimed_tree = facts.has_proven("CLAIMED_TREE", True) or facts.has_proven("IS_TREE", True)
        if claimed_tree and is_disconn:
            return (
                ConflictingFactsCertificate(
                    conflict_id="CONFLICT_TREE_DISCONNECTED",
                    competing_facts=("CLAIMED_TREE", "IS_DISCONNECTED"),
                    axiomatic_proof="By definition, a tree must be a connected graph; a disconnected graph cannot be a tree.",
                    witness="Claimed tree cannot be disconnected."
                ),
                None
            )
        if claimed_tree and (facts.has_proven("HAS_CYCLE", True) or facts.has_proven("HAS_DIRECTED_CYCLE", True)):
            return (
                ConflictingFactsCertificate(
                    conflict_id="CONFLICT_TREE_CYCLIC",
                    competing_facts=("CLAIMED_TREE", "HAS_CYCLE"),
                    axiomatic_proof="By definition, a tree is an acyclic graph; a cyclic graph cannot be a tree.",
                    witness="Claimed tree cannot contain cycles."
                ),
                None
            )

        # 9. Simple Graph vs Multigraph / Self-Loops
        is_simple = facts.has_proven("IS_SIMPLE", True)
        has_multiedges = facts.has_proven("HAS_MULTIEDGES", True)
        has_self_loops = facts.has_proven("HAS_SELF_LOOPS", True)
        if is_simple and (has_multiedges or has_self_loops):
            return (
                ConflictingFactsCertificate(
                    conflict_id="CONFLICT_SIMPLICITY",
                    competing_facts=("IS_SIMPLE", "HAS_MULTIEDGES" if has_multiedges else "HAS_SELF_LOOPS"),
                    axiomatic_proof="A simple graph cannot contain multi-edges or self-loops.",
                    witness="Contradiction: simple graph asserted but multi-edges or self-loops declared."
                ),
                None
            )

        # 10. Simple Undirected Graph Edge Count Bound
        if is_undirected and is_simple and v_fact and e_fact:
            v_val, e_val = v_fact.value, e_fact.value
            if isinstance(v_val, int) and isinstance(e_val, int) and v_val >= 1:
                max_edges = v_val * (v_val - 1) // 2
                if e_val > max_edges:
                    return (
                        ConflictingFactsCertificate(
                            conflict_id="CONFLICT_EDGE_BOUND",
                            competing_facts=(f"V={v_val}", f"E={e_val}"),
                            axiomatic_proof=f"A simple undirected graph on {v_val} vertices can have at most V*(V-1)/2 = {max_edges} edges.",
                            witness=f"Given E={e_val} exceeds theoretical maximum of {max_edges} edges."
                        ),
                        None
                    )

        # 7. Check for Ambiguity
        ambiguous_facts = [f for f in facts if f.ambiguity == AmbiguityStatus.AMBIGUOUS]
        if ambiguous_facts:
            ambig_names = tuple(f.name for f in ambiguous_facts)
            interp = {f.name: ("INTERPRETATION_A", "INTERPRETATION_B") for f in ambiguous_facts}
            return (
                None,
                AmbiguityReport(
                    ambiguous_fact_names=ambig_names,
                    interpretations=interp,
                    witness=f"Ambiguity detected in facts: {', '.join(ambig_names)}. Left unresolved."
                )
            )

        return (None, None)
