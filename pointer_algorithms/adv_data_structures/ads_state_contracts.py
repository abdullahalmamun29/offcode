"""
CHUP Phase 3S — Advanced Data Structures State Contracts & Type System.

Enforces strict semantic substitutability, subtyping hierarchies, attribute unification,
and mathematical preconditions across advanced tree, range, version, and partition structures.
Implementation ancestry does NOT imply IS-A. No caller-supplied certification booleans.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from pointer_algorithms.adv_data_structures.semantic_ontology import (
    GraphTopologyState,
    PathValueDomain,
    PersistenceMode,
    StructureMutability,
    RangeOrderStatisticObjective,
    MoOrderingStrategy,
    ProviderCapability,
)


@dataclass
class StateContract:
    """
    Formal contract definition for an advanced data structure state.
    Enforces explicit subtyping (supertypes) and attribute unification.
    """
    name: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    supertypes: List[str] = field(default_factory=list)

    def satisfies(self, requirement: 'StateContract') -> bool:
        type_compatible = (self.name == requirement.name or requirement.name in self.supertypes)
        if not type_compatible:
            return False

        for req_attr, req_val in requirement.attributes.items():
            if req_attr not in self.attributes:
                return False
            if req_val is not None and self.attributes[req_attr] != req_val:
                return False

        return True


# ── Canonical State Contract Constructors ──

def make_sparse_table_state(
    size: int = 1,
    is_idempotent: bool = True,
    is_associative: bool = True
) -> StateContract:
    """SparseTableState models a static table for O(1) idempotent or O(log N) disjoint queries."""
    return StateContract(
        name="SparseTableState",
        attributes={
            "size": size,
            "is_idempotent": is_idempotent,
            "is_associative": is_associative,
            "mutability": StructureMutability.STATIC,
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=["RangeQueryStructureState"]
    )


def make_tree_topology_state(
    vertex_count: int = 1,
    topology_state: str = GraphTopologyState.VALID_TREE,
    root: int = 0
) -> StateContract:
    """TreeTopologyState models an unrooted/rooted tree graph."""
    return StateContract(
        name="TreeTopologyState",
        attributes={
            "vertex_count": vertex_count,
            "topology_state": topology_state,
            "root": root,
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=["GraphState"]
    )


def make_binary_lifting_lca_state(
    vertex_count: int = 1,
    max_depth: int = 1
) -> StateContract:
    """BinaryLiftingLCAState models tree jump tables for O(log N) LCA and k-th ancestor queries."""
    return StateContract(
        name="BinaryLiftingLCAState",
        attributes={
            "vertex_count": vertex_count,
            "max_depth": max_depth,
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=["TreeTopologyState", "AncestorQueryStructureState"]
    )


def make_heavy_light_decomposition_state(
    vertex_count: int = 1,
    path_value_domain: str = PathValueDomain.VERTEX_VALUES,
    has_range_provider: bool = True
) -> StateContract:
    """HeavyLightDecompositionState models tree path decomposition into heavy chains."""
    return StateContract(
        name="HeavyLightDecompositionState",
        attributes={
            "vertex_count": vertex_count,
            "path_value_domain": path_value_domain,
            "has_range_provider": has_range_provider,
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=["TreeTopologyState", "PathDecompositionState"]
    )


def make_centroid_tree_state(
    vertex_count: int = 1,
    max_depth: int = 1,
    query_objective: str = "NEAREST_MARKED_NODE"
) -> StateContract:
    """CentroidTreeState models balanced centroid divide-and-conquer tree decomposition."""
    return StateContract(
        name="CentroidTreeState",
        attributes={
            "vertex_count": vertex_count,
            "max_depth": max_depth,
            "query_objective": query_objective,
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=["TreeTopologyState", "BalancedDecompositionState"]
    )


def make_persistent_segment_tree_state(
    size: int = 1,
    persistence_mode: str = PersistenceMode.PARTIALLY_PERSISTENT,
    num_versions: int = 1
) -> StateContract:
    """PersistentSegmentTreeState models path-copying immutable version trees."""
    return StateContract(
        name="PersistentSegmentTreeState",
        attributes={
            "size": size,
            "persistence_mode": persistence_mode,
            "num_versions": num_versions,
            "mutability": StructureMutability.PERSISTENT,
            "is_rooted_tree": True,
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=["RangeQueryStructureState", "VersionedStructureState"]
    )


def make_dynamic_segment_tree_state(
    lower: int = 1,
    upper: int = 10**18,
    allocated_nodes: int = 1,
    max_capacity: int = 10**6
) -> StateContract:
    """DynamicSegmentTreeState models lazy pointer node allocation over large coordinate domains."""
    return StateContract(
        name="DynamicSegmentTreeState",
        attributes={
            "lower": lower,
            "upper": upper,
            "allocated_nodes": allocated_nodes,
            "max_capacity": max_capacity,
            "mutability": StructureMutability.EPHEMERAL_MUTABLE,
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=["RangeQueryStructureState", "SparseStructureState"]
    )


def make_merge_sort_tree_state(
    size: int = 1,
    objective: str = RangeOrderStatisticObjective.COUNT_LEQ
) -> StateContract:
    """MergeSortTreeState models static range rank/count structures without point updates."""
    return StateContract(
        name="MergeSortTreeState",
        attributes={
            "size": size,
            "objective": objective,
            "mutability": StructureMutability.STATIC,
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=["RangeQueryStructureState", "StaticOrderStatisticState"]
    )


def make_sqrt_decomposition_state(
    size: int = 1,
    block_size: int = 1
) -> StateContract:
    """SqrtDecompositionState models block partitioning of size B = ceil(sqrt(N))."""
    return StateContract(
        name="SqrtDecompositionState",
        attributes={
            "size": size,
            "block_size": block_size,
            "mutability": StructureMutability.EPHEMERAL_MUTABLE,
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=["RangeQueryStructureState", "BlockPartitionState"]
    )


def make_mos_query_schedule_state(
    query_count: int = 1,
    is_offline: bool = True,
    is_reversible: bool = True,
    ordering_strategy: str = MoOrderingStrategy.STANDARD_BLOCK_SNAKE
) -> StateContract:
    """MosQueryScheduleState models offline query scheduling with reversible state transitions."""
    return StateContract(
        name="MosQueryScheduleState",
        attributes={
            "query_count": query_count,
            "is_offline": is_offline,
            "is_reversible": is_reversible,
            "ordering_strategy": ordering_strategy,
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=["OfflineQueryScheduleState"]
    )


def make_segment_tree_beats_state(
    size: int = 1,
    supported_ops: Optional[List[str]] = None,
    has_second_max: bool = True
) -> StateContract:
    """SegmentTreeBeatsState models range chmin and current max hierarchy maintenance."""
    if supported_ops is None:
        supported_ops = ["RANGE_CHMIN", "RANGE_SUM_QUERY", "RANGE_MAX_QUERY"]
    return StateContract(
        name="SegmentTreeBeatsState",
        attributes={
            "size": size,
            "supported_ops": supported_ops,
            "has_second_max": has_second_max,
            "mutability": StructureMutability.EPHEMERAL_MUTABLE,
            "correctness_guarantee": "DETERMINISTIC_EXACT",
        },
        supertypes=["RangeQueryStructureState", "AdaptiveTagState"]
    )
