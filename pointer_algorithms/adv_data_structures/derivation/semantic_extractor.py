"""
CHUP Phase 3S — Semantic Extractor for Advanced Data Structures.

Parses structural, algebraic, topological, and temporal problem specifications
into a rich SemanticAdvancedDataStructureModel without rigid monolithic keyword heuristics.
"""

import re
from typing import Dict, Any, Optional
from pointer_algorithms.adv_data_structures.semantic_ontology import (
    SemanticAdvancedDataStructureModel,
    AdvancedDataStructureObjective,
    AlgebraicProperties,
    GraphTopologyState,
    PathValueDomain,
    PersistenceMode,
    StructureMutability,
    RangeOrderStatisticObjective,
    MoOrderingStrategy,
    TransitionCost,
    CoordinateDomain,
    QueryMode,
    ProviderCapability,
)


class SemanticExtractor:
    """
    Extracts semantic features, algebraic properties, and structural topology
    into a SemanticAdvancedDataStructureModel with complete provenance.
    """

    def extract(self, problem_spec: Any) -> SemanticAdvancedDataStructureModel:
        if isinstance(problem_spec, str):
            problem_spec = self._parse_text_to_spec(problem_spec)
        elif not isinstance(problem_spec, dict):
            problem_spec = {}

        model = SemanticAdvancedDataStructureModel()

        # 1. Objective Extraction
        raw_obj = problem_spec.get("objective")
        if raw_obj:
            for obj in AdvancedDataStructureObjective:
                if obj.value == raw_obj or obj.name == raw_obj:
                    model.objective = obj
                    model.add_fact("OBJECTIVE_DECLARED", f"Objective declared as {obj.value}")
                    break

        # 2. Algebraic Properties
        alg = problem_spec.get("algebraic_properties")
        if alg:
            op_name = alg.get("operation", "min").lower()
            if op_name in ("min", "minimum"):
                model.algebraic_properties = AlgebraicProperties.min_operation()
            elif op_name in ("max", "maximum"):
                model.algebraic_properties = AlgebraicProperties.max_operation()
            elif op_name in ("gcd", "greatest_common_divisor"):
                model.algebraic_properties = AlgebraicProperties.gcd_operation()
            elif op_name in ("and", "bitwise_and"):
                model.algebraic_properties = AlgebraicProperties.bitwise_and_operation()
            elif op_name in ("or", "bitwise_or"):
                model.algebraic_properties = AlgebraicProperties.bitwise_or_operation()
            elif op_name in ("sum", "summation", "addition"):
                model.algebraic_properties = AlgebraicProperties.sum_operation()
            elif op_name in ("xor", "bitwise_xor"):
                model.algebraic_properties = AlgebraicProperties.xor_operation()
            else:
                model.algebraic_properties = AlgebraicProperties(
                    associative=alg.get("associative", True),
                    commutative=alg.get("commutative", True),
                    idempotent=alg.get("idempotent", False),
                    invertible=alg.get("invertible", False),
                    has_identity=alg.get("has_identity", False),
                    identity_element=alg.get("identity_element", None),
                )
            if model.algebraic_properties.idempotent:
                model.add_fact("OPERATION_IDEMPOTENT", "Operation satisfies f(x, x) = x enabling O(1) overlapping query")
            else:
                model.add_fact("OPERATION_NON_IDEMPOTENT", "Operation does not satisfy idempotence; requires disjoint intervals")

        # 3. Topology State
        raw_topo = problem_spec.get("topology_state")
        if raw_topo:
            for top in GraphTopologyState:
                if top.value == raw_topo:
                    model.topology_state = top
                    model.add_fact("TOPOLOGY_STATE_RECORDED", f"Graph topology identified as {top.value}")
                    break
        elif problem_spec.get("vertex_count", 1) == 0:
            model.topology_state = GraphTopologyState.EMPTY
            model.add_fact("TOPOLOGY_EMPTY", "Vertex set has size zero")

        # 4. Path Value Domain (HLD)
        raw_domain = problem_spec.get("path_value_domain")
        if raw_domain == "EDGE_VALUES":
            model.path_value_domain = PathValueDomain.EDGE_VALUES
            model.add_fact("EDGE_WEIGHTED_TREE", "Values reside on edges; LCA vertex excluded from interval queries")
        else:
            model.path_value_domain = PathValueDomain.VERTEX_VALUES
            model.add_fact("VERTEX_WEIGHTED_TREE", "Values reside on vertices; path includes LCA vertex")

        # 5. Temporal Semantics & Query Mode
        raw_qm = problem_spec.get("query_mode")
        if raw_qm == "OFFLINE":
            model.query_mode = QueryMode.OFFLINE
            model.add_fact("QUERY_MODE_OFFLINE", "Queries are provided upfront in batch")
        else:
            model.query_mode = QueryMode.ONLINE
            model.add_fact("QUERY_MODE_ONLINE", "Queries arrive interactively online")

        # 6. Persistence & Mutability
        raw_pm = problem_spec.get("persistence_mode")
        if raw_pm == "PARTIALLY_PERSISTENT":
            model.persistence_mode = PersistenceMode.PARTIALLY_PERSISTENT
            model.mutability = StructureMutability.PERSISTENT
            model.add_fact("PARTIALLY_PERSISTENT", "Linear historical versions; modifications to newest version only")
        elif raw_pm == "FULLY_PERSISTENT":
            model.persistence_mode = PersistenceMode.FULLY_PERSISTENT
            model.mutability = StructureMutability.PERSISTENT
            model.add_fact("FULLY_PERSISTENT", "Rooted version tree; branching from any historical version permitted")
        else:
            model.persistence_mode = PersistenceMode.NONE
            if problem_spec.get("is_static", False):
                model.mutability = StructureMutability.STATIC
                model.add_fact("STRUCTURE_STATIC", "Structure is immutable once built")
            else:
                model.mutability = StructureMutability.EPHEMERAL_MUTABLE
                model.add_fact("STRUCTURE_MUTABLE", "Structure supports in-place modifications")

        # 7. Order Statistic Objective (MergeSortTree)
        raw_ord = problem_spec.get("order_statistic_objective")
        if raw_ord:
            for ord_obj in RangeOrderStatisticObjective:
                if ord_obj.value == raw_ord:
                    model.order_statistic_objective = ord_obj
                    model.add_fact("ORDER_STATISTIC_OBJECTIVE", f"Range order statistic objective: {ord_obj.value}")
                    break

        # 8. Mo's Scheduling & Reversibility
        raw_strat = problem_spec.get("mo_ordering_strategy")
        if raw_strat == "HILBERT_CURVE":
            model.mo_ordering_strategy = MoOrderingStrategy.HILBERT_CURVE
        else:
            model.mo_ordering_strategy = MoOrderingStrategy.STANDARD_BLOCK_SNAKE

        trans = problem_spec.get("transition_cost")
        if trans:
            is_rev = trans.get("is_reversible", True)
            model.transition_cost = TransitionCost(
                add_cost=trans.get("add_cost", "O(1)"),
                remove_cost=trans.get("remove_cost", "O(1)"),
                is_reversible=is_rev
            )
            if not is_rev:
                model.add_fact("IRREVERSIBLE_TRANSITION", "State transitions cannot be inverted back to original state")
            else:
                model.add_fact("REVERSIBLE_TRANSITION", "State transitions satisfy remove(add(S, x), x) == S")

        # 9. Coordinate Domain Bounds
        coord = problem_spec.get("coordinate_domain")
        if coord:
            model.coordinate_domain = CoordinateDomain(
                lower=coord.get("lower", 1),
                upper=coord.get("upper", 10**18)
            )
            model.add_fact("COORDINATE_DOMAIN_BOUNDED", f"Domain bounded in [{model.coordinate_domain.lower}, {model.coordinate_domain.upper}]")

        # 10. Provider Binding for HLD
        if problem_spec.get("has_range_provider", True):
            model.provider_capabilities.add(ProviderCapability.RANGE_QUERY)
            if problem_spec.get("requires_updates", False):
                model.provider_capabilities.add(ProviderCapability.RANGE_UPDATE)
            model.add_fact("RANGE_PROVIDER_ATTACHED", "Valid range query/update provider attached to tree decomposition")
        else:
            model.provider_capabilities.clear()
            model.add_fact("NO_RANGE_PROVIDER", "No underlying range structure provider registered")

        # 11. Beats Operation Verification
        ops = problem_spec.get("supported_ops")
        if ops:
            model.beats_supported_ops = set(ops)
            unsupported = model.beats_supported_ops - {"RANGE_CHMIN", "RANGE_SUM_QUERY", "RANGE_MAX_QUERY"}
            if unsupported:
                model.add_fact("UNSUPPORTED_BEATS_OP", f"Operations not supported by canonical beats: {unsupported}")

        return model

    def _parse_text_to_spec(self, text: str) -> Dict[str, Any]:
        t = text.lower()
        spec: Dict[str, Any] = {}
        if "sparse table" in t or ("static" in t and ("rmq" in t or "range min" in t or "range max" in t or "range gcd" in t)):
            spec["objective"] = "SPARSE_TABLE_RMQ"
            if "gcd" in t:
                spec["algebraic_properties"] = {"operation": "gcd"}
            elif "max" in t:
                spec["algebraic_properties"] = {"operation": "max"}
            else:
                spec["algebraic_properties"] = {"operation": "min"}
            spec["is_static"] = True
        elif "beats" in t or "chmin" in t or "range minimize" in t:
            spec["objective"] = "SEGMENT_TREE_BEATS"
            spec["supported_ops"] = ["RANGE_CHMIN", "RANGE_SUM_QUERY", "RANGE_MAX_QUERY"]
        elif ("heavy" in t and "light" in t) or "hld" in t:
            spec["objective"] = "HEAVY_LIGHT_DECOMPOSITION"
            spec["topology_state"] = "VALID_TREE"
        elif "centroid" in t:
            spec["objective"] = "CENTROID_DECOMPOSITION"
            spec["topology_state"] = "VALID_TREE"
        elif "lowest common ancestor" in t or "lca" in t or "binary lifting" in t:
            spec["objective"] = "LCA_BINARY_LIFTING"
            spec["topology_state"] = "VALID_TREE"
        elif "persistent" in t or ("version" in t and "tree" in t):
            spec["objective"] = "PERSISTENT_SEGMENT_TREE"
            spec["persistence_mode"] = "PARTIALLY_PERSISTENT"
        elif "dynamic segment tree" in t or "implicit segment tree" in t or ("sparse" in t and "segment tree" in t) or ("10^18" in t and "segment tree" in t):
            spec["objective"] = "DYNAMIC_SEGMENT_TREE"
            spec["coordinate_domain"] = {"lower": 1, "upper": 10**18}
        elif "merge sort tree" in t or ("count" in t and "less than" in t and "range" in t):
            spec["objective"] = "MERGE_SORT_TREE"
            spec["is_static"] = True
            spec["order_statistic_objective"] = "COUNT_LEQ"
        elif "mo's algorithm" in t or "mos algorithm" in t or re.search(r"\bmo'?s\b", t) or ("offline" in t and "distinct" in t and "query" in t):
            spec["objective"] = "MOS_ALGORITHM"
            spec["query_mode"] = "OFFLINE"
            spec["transition_cost"] = {"is_reversible": True}
        elif "sqrt decomposition" in t or "square root decomposition" in t or "block decomposition" in t:
            spec["objective"] = "SQRT_DECOMPOSITION"
            spec["is_static"] = False
        return spec

