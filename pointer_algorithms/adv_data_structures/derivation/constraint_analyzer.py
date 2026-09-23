"""
CHUP Phase 3S — Constraint Analyzer for Advanced Data Structures.

Performs constraint verification, algebraic compatibility checks, and
precondition validations across problem dimensions and components.
"""

from typing import Dict, Any, List, Tuple
from pointer_algorithms.adv_data_structures.semantic_ontology import (
    SemanticAdvancedDataStructureModel,
    AdvancedDataStructureObjective,
    GraphTopologyState,
    QueryMode,
    StructureMutability,
    ProviderCapability,
)


class ConstraintAnalyzer:
    """
    Analyzes mathematical, topological, and resource constraints against
    candidate data structure contracts.
    """

    def analyze(self, model: SemanticAdvancedDataStructureModel) -> List[Tuple[str, str, bool]]:
        """
        Runs constraint analysis, returning a list of (check_name, description, passed).
        """
        results = []

        # Check 1: Sparse Table Idempotency
        if model.objective == AdvancedDataStructureObjective.SPARSE_TABLE_RMQ:
            is_idem = model.algebraic_properties.idempotent
            results.append((
                "SPARSE_TABLE_IDEMPOTENCY",
                "Sparse Table O(1) query requires associative and idempotent operation",
                is_idem
            ))
            if not is_idem:
                model.add_fact("NON_IDEMPOTENT_OPERATION_REJECTS_O1_SPARSE_TABLE", "Operation is not idempotent; cannot use O(1) overlapping query")

        # Check 2: Tree Topology Acyclicity and Connectivity
        tree_objs = {
            AdvancedDataStructureObjective.LCA_BINARY_LIFTING,
            AdvancedDataStructureObjective.HEAVY_LIGHT_DECOMPOSITION,
            AdvancedDataStructureObjective.CENTROID_DECOMPOSITION,
        }
        if model.objective in tree_objs:
            is_valid_tree = (model.topology_state == GraphTopologyState.VALID_TREE)
            results.append((
                "TREE_TOPOLOGY_VALIDITY",
                "Tree structures strictly require an acyclic, connected graph with valid root",
                is_valid_tree
            ))
            if model.topology_state == GraphTopologyState.EMPTY:
                model.add_fact("TOPOLOGY_EMPTY", "Input graph has zero vertices")
            elif model.topology_state == GraphTopologyState.CYCLIC:
                model.add_fact("TOPOLOGY_CYCLIC", "Input graph contains cycles")
            elif model.topology_state == GraphTopologyState.DISCONNECTED:
                model.add_fact("TOPOLOGY_DISCONNECTED", "Input graph is disconnected / multi-component")

        # Check 3: Mo's Algorithm Offline Query Prerequisite
        if model.objective == AdvancedDataStructureObjective.MOS_ALGORITHM:
            is_offline = (model.query_mode == QueryMode.OFFLINE)
            results.append((
                "MOS_OFFLINE_QUERIES",
                "Mo's algorithm requires all queries known upfront for block-sorted scheduling",
                is_offline
            ))
            if not is_offline:
                model.add_fact("ALGORITHM_REQUIRES_OFFLINE_QUERIES", "Online interactive query stream cannot be reordered by Mo's scheduler")

            # Check 4: Mo's Algorithm Reversible State Transitions
            is_rev = model.transition_cost.is_reversible
            results.append((
                "MOS_REVERSIBLE_TRANSITIONS",
                "Mo's algorithm requires state transitions to satisfy remove(add(S, x), x) == S",
                is_rev
            ))
            if not is_rev:
                model.add_fact("IRREVERSIBLE_INTERVAL_TRANSITION", "State transitions have irreversible side effects")

        # Check 5: Static Structure Immutability (Merge Sort Tree)
        if model.objective == AdvancedDataStructureObjective.MERGE_SORT_TREE:
            is_static = (model.mutability == StructureMutability.STATIC)
            results.append((
                "MERGE_SORT_TREE_STATIC",
                "Merge Sort Tree is strictly immutable; point/range updates are disallowed",
                is_static
            ))
            if not is_static:
                model.add_fact("MUTATION_NOT_SUPPORTED_ON_STATIC_STRUCTURE", "Dynamic mutations attempted on static Merge Sort Tree")

        # Check 6: HLD Range Provider Requirement
        if model.objective == AdvancedDataStructureObjective.HEAVY_LIGHT_DECOMPOSITION:
            has_provider = (ProviderCapability.RANGE_QUERY in model.provider_capabilities)
            results.append((
                "HLD_RANGE_PROVIDER_ATTACHED",
                "Heavy-Light Decomposition requires a registered linear range structure provider",
                has_provider
            ))
            if not has_provider:
                model.add_fact("NO_RANGE_STRUCTURE_PROVIDER", "No underlying range structure provider registered for HLD")

        # Check 7: Segment Tree Beats Supported Operations
        if model.objective == AdvancedDataStructureObjective.SEGMENT_TREE_BEATS:
            unsupported = model.beats_supported_ops - {"RANGE_CHMIN", "RANGE_SUM_QUERY", "RANGE_MAX_QUERY"}
            is_valid_ops = (len(unsupported) == 0)
            results.append((
                "SEGMENT_BEATS_OPERATIONS_SUPPORTED",
                "Segment Tree Beats canonical component supports only {RANGE_CHMIN, RANGE_SUM_QUERY, RANGE_MAX_QUERY}",
                is_valid_ops
            ))
            if not is_valid_ops:
                model.add_fact("SEGMENT_BEATS_TAG_VIOLATION", f"Operations outside canonical beats set requested: {unsupported}")

        return results
