"""
CHUP Phase 3S — Closed-World Validation Gate Evaluator.

Implements all 9 Closed-World Validation Gates (Gates A–I), partitioned into
Semantic/Correctness Proof Gates (A–E, G, H, I) and Resource Feasibility Gates (F).
Fails closed with deterministic, typed error codes.
"""

from typing import Tuple, Optional, Dict, Any
from pointer_algorithms.adv_data_structures.semantic_ontology import (
    SemanticAdvancedDataStructureModel,
    AdvancedDataStructureObjective,
    GraphTopologyState,
    QueryMode,
    StructureMutability,
    ProviderCapability,
)


class GateEvaluator:
    """
    Evaluates Closed-World Validation Gates A–I.
    Returns (passed: bool, failure_code: Optional[str], failure_message: Optional[str]).
    """

    def evaluate(
        self,
        model: SemanticAdvancedDataStructureModel,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        ctx = context or {}
        obj = model.objective

        # ── Gate A: Structural Topology Gate ──
        tree_objs = {
            AdvancedDataStructureObjective.LCA_BINARY_LIFTING,
            AdvancedDataStructureObjective.HEAVY_LIGHT_DECOMPOSITION,
            AdvancedDataStructureObjective.CENTROID_DECOMPOSITION,
        }
        if obj in tree_objs:
            if model.topology_state == GraphTopologyState.EMPTY:
                return False, "TOPOLOGY_EMPTY", "Input graph has zero vertices; cannot construct tree decomposition."
            if model.topology_state == GraphTopologyState.CYCLIC or model.has_derived_fact("TOPOLOGY_CYCLIC") or model.has_derived_fact("GRAPH_HAS_CYCLES"):
                return False, "TOPOLOGY_CYCLIC", "Input graph contains cycles; tree decomposition requires an acyclic graph."
            if model.topology_state == GraphTopologyState.DISCONNECTED or model.has_derived_fact("TOPOLOGY_DISCONNECTED") or model.has_derived_fact("GRAPH_DISCONNECTED"):
                return False, "TOPOLOGY_DISCONNECTED", "Input graph is disconnected; tree decomposition requires a connected component."

            root = ctx.get("root", 0)
            v_count = ctx.get("vertex_count", 1)
            if root < 0 or (v_count > 0 and root >= v_count):
                return False, "TREE_ROOT_INVALID", f"Root vertex index {root} is out of bounds for tree of size {v_count}."

        # ── Gate B: Offline Query Requirement Gate ──
        if obj == AdvancedDataStructureObjective.MOS_ALGORITHM:
            if model.query_mode == QueryMode.ONLINE or model.has_derived_fact("ALGORITHM_REQUIRES_OFFLINE_QUERIES"):
                return False, "ALGORITHM_REQUIRES_OFFLINE_QUERIES", "Mo's algorithm requires all queries upfront for offline block sorting; cannot handle interactive streams."

        # ── Gate C: Operation Idempotency & Associativity Gate ──
        if obj == AdvancedDataStructureObjective.SPARSE_TABLE_RMQ:
            if not model.algebraic_properties.associative or model.has_derived_fact("OPERATION_NOT_ASSOCIATIVE"):
                return False, "OPERATION_NOT_ASSOCIATIVE", "Sparse Table requires an associative operation: f(f(a,b),c) = f(a,f(b,c))."
            if not model.algebraic_properties.idempotent or model.has_derived_fact("NON_IDEMPOTENT_OPERATION_REJECTS_O1_SPARSE_TABLE") or model.has_derived_fact("OPERATION_NOT_IDEMPOTENT"):
                return False, "NON_IDEMPOTENT_OPERATION_REJECTS_O1_SPARSE_TABLE", "Sparse Table O(1) query requires an idempotent operation (f(x, x) = x). Non-idempotent operations require O(log N) disjoint blocks."

        # ── Gate D: Structure Mutability Gate ──
        if obj == AdvancedDataStructureObjective.MERGE_SORT_TREE:
            if model.mutability != StructureMutability.STATIC or ctx.get("has_updates", False) or model.has_derived_fact("MUTATION_NOT_SUPPORTED_ON_STATIC_STRUCTURE"):
                return False, "MUTATION_NOT_SUPPORTED_ON_STATIC_STRUCTURE", "Merge Sort Tree is strictly immutable; point and range updates are unsupported."

        # ── Gate E: Version Boundary Gate ──
        if obj == AdvancedDataStructureObjective.PERSISTENT_SEGMENT_TREE:
            version = ctx.get("query_version", 0)
            num_versions = ctx.get("num_versions", 1)
            if version < 0 or version >= num_versions or model.has_derived_fact("VERSION_ROOT_OUT_OF_BOUNDS") or model.has_derived_fact("INVALID_PERSISTENT_VERSION_INDEX"):
                return False, "VERSION_ROOT_OUT_OF_BOUNDS", f"Historical root version {version} is out of bounds [0, {num_versions - 1}]."

        # ── Gate F: Resource Feasibility / Node Allocation Gate ──
        if obj == AdvancedDataStructureObjective.DYNAMIC_SEGMENT_TREE:
            allocated = ctx.get("allocated_nodes", 0)
            capacity = ctx.get("max_capacity", 10**6)
            if allocated > capacity or model.has_derived_fact("NODE_ALLOCATION_LIMIT_EXCEEDED") or model.has_derived_fact("DYNAMIC_NODE_CAPACITY_EXCEEDED"):
                return False, "NODE_ALLOCATION_LIMIT_EXCEEDED", f"Dynamic segment tree allocated {allocated} nodes, exceeding capacity limit {capacity}."

        # ── Gate G: Reversible Transitions Gate ──
        if obj == AdvancedDataStructureObjective.MOS_ALGORITHM:
            if not model.transition_cost.is_reversible or model.has_derived_fact("IRREVERSIBLE_INTERVAL_TRANSITION") or model.has_derived_fact("STATE_TRANSITION_NOT_REVERSIBLE"):
                return False, "IRREVERSIBLE_INTERVAL_TRANSITION", "State transitions fail semantic reversibility: remove(add(S, x), x) != S."

        # ── Gate H: Underlying Range Structure Provider Gate ──
        if obj == AdvancedDataStructureObjective.HEAVY_LIGHT_DECOMPOSITION:
            if ProviderCapability.RANGE_QUERY not in model.provider_capabilities or model.has_derived_fact("NO_RANGE_STRUCTURE_PROVIDER") or model.has_derived_fact("RANGE_PROVIDER_MISSING"):
                return False, "NO_RANGE_STRUCTURE_PROVIDER", "Heavy-Light Decomposition requires a registered linear range structure provider."

        # ── Gate I: Beats Tag Monotonicity Gate ──
        if obj == AdvancedDataStructureObjective.SEGMENT_TREE_BEATS:
            if model.has_derived_fact("SEGMENT_BEATS_TAG_VIOLATION") or model.has_derived_fact("UNSUPPORTED_BEATS_OPERATION"):
                return False, "SEGMENT_BEATS_TAG_VIOLATION", "Requested operation outside canonical set or broken second-maximum tag invariant."

            max1 = ctx.get("max1")
            max2 = ctx.get("max2")
            has_sec = ctx.get("has_second_max", False)
            if max1 is not None and max2 is not None and has_sec:
                if max2 >= max1:
                    return False, "SEGMENT_BEATS_TAG_VIOLATION", f"Second maximum ({max2}) must be strictly less than maximum ({max1}) on multi-valued ranges."

        return True, None, None
