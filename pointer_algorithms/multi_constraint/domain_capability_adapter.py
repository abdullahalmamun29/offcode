"""
CHUP Phase 5 — Universal Domain Capability Adapter.

Consumes the frozen domain registry (Phase 3A through 3S, Phase 4) and adapts
each technique into a uniform CandidateProfile with formal requires/produces
contracts. Avoids maintaining any separate or competing shadow ontology.
"""

from typing import Dict, List, Optional, FrozenSet
import math
from pointer_algorithms.multi_constraint.constraint_lattice import (
    TemporalMode,
    MutabilityCapability,
    MutabilitySet,
)
from pointer_algorithms.multi_constraint.aggregate_ontology import QueryTarget
from pointer_algorithms.multi_constraint.candidate_profile import (
    CandidateProfile,
    SymbolicComplexity,
)


class DomainCapabilityAdapter:
    """
    Universal adapter bridging all 19 frozen domains and Phase 4 compositions
    into the Phase 5 multi-constraint reasoning engine.
    """

    _REGISTRY: Optional[Dict[str, CandidateProfile]] = None

    @classmethod
    def get_candidate_universe(cls) -> Dict[str, CandidateProfile]:
        """Returns the full candidate profile universe across all 19 frozen domains."""
        if cls._REGISTRY is None:
            cls._REGISTRY = cls._build_universe()
        return dict(cls._REGISTRY)

    @classmethod
    def get_candidate(cls, candidate_id: str) -> Optional[CandidateProfile]:
        return cls.get_candidate_universe().get(candidate_id)

    @classmethod
    def _build_universe(cls) -> Dict[str, CandidateProfile]:
        universe: Dict[str, CandidateProfile] = {}

        # ── 1. Phase 3S: Advanced Data Structures ──────────────────────
        universe["sparse_table"] = CandidateProfile(
            candidate_id="sparse_table",
            family="adv_data_structures",
            display_name="Sparse Table (Static RMQ)",
            supported_temporals=frozenset([TemporalMode.ONLINE, TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.read_only(),
            supported_query_targets=frozenset([QueryTarget.LINEAR_RANGE]),
            supported_aggregate_names=frozenset(["*"]),
            requires_idempotence=True,
            requires_capabilities=frozenset(["LINEAR_ARRAY"]),
            produces_capabilities=frozenset(["RANGE_AGGREGATION", "RANGE_RMQ_O1"]),
            preconditions=frozenset(["ASSOCIATIVE_AND_IDEMPOTENT_OPERATION"]),
            forbidden_properties=frozenset(["DYNAMIC_MUTATION", "NON_IDEMPOTENT_OPERATION"]),
            complexity=SymbolicComplexity(
                time_op_formula="1",
                total_time_formula="N * log(N) + Q",
                space_bytes_formula="4 * N * (log2(N) + 1) * 4",
                space_complexity_class="O(N log N)",
                estimate_ops=lambda n, q, v, e, c: n * (int(math.log2(max(1, n))) + 1) + q,
                estimate_bytes=lambda n, q, v, e, c: 4 * n * (int(math.log2(max(1, n))) + 1) * 4
            ),
            description="Static O(1) range minimum/maximum/gcd query over idempotent semigroup"
        )

        universe["dynamic_segment_tree"] = CandidateProfile(
            candidate_id="dynamic_segment_tree",
            family="adv_data_structures",
            display_name="Dynamic Segment Tree",
            supported_temporals=frozenset([TemporalMode.ONLINE, TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.range_update(),
            supported_query_targets=frozenset([QueryTarget.POINT, QueryTarget.LINEAR_RANGE]),
            supported_aggregate_names=frozenset(["*"]),
            requires_capabilities=frozenset(["MASSIVE_COORDINATES"]),
            produces_capabilities=frozenset(["RANGE_AGGREGATION", "POINT_UPDATE", "RANGE_UPDATE", "DYNAMIC_COORDINATE_INDEXING"]),
            complexity=SymbolicComplexity(
                time_op_formula="log(C)",
                total_time_formula="Q * log(C)",
                space_bytes_formula="32 * Q * log2(C)",
                space_complexity_class="O(Q log C)",
                estimate_ops=lambda n, q, v, e, c: q * (int(math.log2(max(1, c))) + 1),
                estimate_bytes=lambda n, q, v, e, c: 32 * q * (int(math.log2(max(1, c))) + 1)
            ),
            description="Dynamically allocated pointer segment tree for massive coordinate domains up to 10^18"
        )

        universe["persistent_segment_tree"] = CandidateProfile(
            candidate_id="persistent_segment_tree",
            family="adv_data_structures",
            display_name="Persistent Segment Tree",
            supported_temporals=frozenset([TemporalMode.ONLINE, TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.point_update(),
            supported_query_targets=frozenset([QueryTarget.LINEAR_RANGE]),
            supported_aggregate_names=frozenset(["*"]),
            requires_order_statistics=False,
            produces_capabilities=frozenset(["HISTORICAL_VERSION_QUERY", "PREFIX_VERSION_ROOTS", "RANGE_KTH_STATIC"]),
            complexity=SymbolicComplexity(
                time_op_formula="log(N)",
                total_time_formula="N * log(N) + Q * log(N)",
                space_bytes_formula="32 * (N + Q) * log2(N)",
                space_complexity_class="O((N + Q) log N)",
                estimate_ops=lambda n, q, v, e, c: (n + q) * (int(math.log2(max(1, n))) + 1),
                estimate_bytes=lambda n, q, v, e, c: 32 * (n + q) * (int(math.log2(max(1, n))) + 1)
            ),
            description="Path-copying persistent segment tree maintaining prefix historical versions"
        )

        universe["merge_sort_tree"] = CandidateProfile(
            candidate_id="merge_sort_tree",
            family="adv_data_structures",
            display_name="Merge Sort Tree",
            supported_temporals=frozenset([TemporalMode.ONLINE, TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.read_only(),
            supported_query_targets=frozenset([QueryTarget.LINEAR_RANGE]),
            supported_aggregate_names=frozenset(["KTH", "COUNT", "DISTINCT"]),
            requires_order_statistics=True,
            produces_capabilities=frozenset(["RANGE_KTH_STATIC", "RANGE_RANK_QUERY"]),
            forbidden_properties=frozenset(["DYNAMIC_MUTATION"]),
            complexity=SymbolicComplexity(
                time_op_formula="log^2(N)",
                total_time_formula="N * log(N) + Q * log^2(N)",
                space_bytes_formula="4 * N * (log2(N) + 1)",
                space_complexity_class="O(N log N)",
                estimate_ops=lambda n, q, v, e, c: n * (int(math.log2(max(1, n))) + 1) + q * (int(math.log2(max(1, n))) + 1)**2,
                estimate_bytes=lambda n, q, v, e, c: 4 * n * (int(math.log2(max(1, n))) + 1)
            ),
            description="Static segment tree storing sorted sub-vectors for range order statistic queries"
        )

        universe["mos_algorithm_scheduler"] = CandidateProfile(
            candidate_id="mos_algorithm_scheduler",
            family="adv_data_structures",
            display_name="Mo's Algorithm Query Scheduler",
            supported_temporals=frozenset([TemporalMode.OFFLINE]),  # STRICTLY OFFLINE ONLY
            supported_mutability=MutabilitySet.read_only(),
            supported_query_targets=frozenset([QueryTarget.LINEAR_RANGE]),
            supported_aggregate_names=frozenset(["*"]),
            preconditions=frozenset(["TRANSITION_REVERSIBLE", "OFFLINE_QUERIES_KNOWN"]),
            forbidden_properties=frozenset(["ONLINE_QUERY_STREAM"]),
            produces_capabilities=frozenset(["OFFLINE_QUERY_SCHEDULE"]),
            complexity=SymbolicComplexity(
                time_op_formula="sqrt(N)",
                total_time_formula="(N + Q) * sqrt(N)",
                space_bytes_formula="4 * N + 16 * Q",
                space_complexity_class="O(N + Q)",
                estimate_ops=lambda n, q, v, e, c: int((n + q) * math.sqrt(max(1, n))),
                estimate_bytes=lambda n, q, v, e, c: 4 * n + 16 * q
            ),
            description="Square root query scheduler for offline arbitrary reversible range queries"
        )

        universe["sqrt_decomposition"] = CandidateProfile(
            candidate_id="sqrt_decomposition",
            family="adv_data_structures",
            display_name="Square Root Block Decomposition",
            supported_temporals=frozenset([TemporalMode.ONLINE, TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.range_update(),
            supported_query_targets=frozenset([QueryTarget.POINT, QueryTarget.LINEAR_RANGE]),
            supported_aggregate_names=frozenset(["*"]),
            produces_capabilities=frozenset(["RANGE_AGGREGATION", "BLOCK_UPDATE"]),
            complexity=SymbolicComplexity(
                time_op_formula="sqrt(N)",
                total_time_formula="Q * sqrt(N)",
                space_bytes_formula="4 * N + 4 * sqrt(N)",
                space_complexity_class="O(N)",
                estimate_ops=lambda n, q, v, e, c: int(q * math.sqrt(max(1, n))),
                estimate_bytes=lambda n, q, v, e, c: int(4 * n + 4 * math.sqrt(max(1, n)))
            ),
            description="Block partitioning with lazy tags for polylog-infeasible interval updates"
        )

        universe["heavy_light_decomposition"] = CandidateProfile(
            candidate_id="heavy_light_decomposition",
            family="adv_data_structures",
            display_name="Heavy-Light Decomposition",
            supported_temporals=frozenset([TemporalMode.ONLINE, TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.range_update(),
            supported_query_targets=frozenset([QueryTarget.TREE_PATH, QueryTarget.TREE_SUBTREE]),
            supported_aggregate_names=frozenset(["*"]),
            requires_capabilities=frozenset(["TREE_TOPOLOGY"]),
            produces_capabilities=frozenset(["TREE_PATH_TO_LINEAR_RANGES", "SUBTREE_TO_LINEAR_RANGE"]),
            complexity=SymbolicComplexity(
                time_op_formula="log^2(N)",
                total_time_formula="Q * log^2(N)",
                space_bytes_formula="24 * N",
                space_complexity_class="O(N)",
                estimate_ops=lambda n, q, v, e, c: q * (int(math.log2(max(1, n))) + 1)**2,
                estimate_bytes=lambda n, q, v, e, c: 24 * n
            ),
            description="Heavy-Light chain tree partitioning decomposing paths into O(log N) contiguous intervals"
        )

        universe["centroid_decomposition"] = CandidateProfile(
            candidate_id="centroid_decomposition",
            family="adv_data_structures",
            display_name="Centroid Decomposition",
            supported_temporals=frozenset([TemporalMode.ONLINE, TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.read_only(),
            supported_query_targets=frozenset([QueryTarget.TREE_PATH]),
            supported_aggregate_names=frozenset(["*"]),
            requires_capabilities=frozenset(["TREE_TOPOLOGY"]),
            produces_capabilities=frozenset(["TREE_DISTANCE_QUERY", "CENTROID_TREE_ROOT"]),
            complexity=SymbolicComplexity(
                time_op_formula="log(N)",
                total_time_formula="Q * log(N)",
                space_bytes_formula="16 * N * log2(N)",
                space_complexity_class="O(N log N)",
                estimate_ops=lambda n, q, v, e, c: q * (int(math.log2(max(1, n))) + 1),
                estimate_bytes=lambda n, q, v, e, c: 16 * n * (int(math.log2(max(1, n))) + 1)
            ),
            description="Balanced divide-and-conquer centroid tree for path distance queries"
        )

        universe["segment_tree_beats"] = CandidateProfile(
            candidate_id="segment_tree_beats",
            family="adv_data_structures",
            display_name="Segment Tree Beats",
            supported_temporals=frozenset([TemporalMode.ONLINE, TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.range_update(),
            supported_query_targets=frozenset([QueryTarget.LINEAR_RANGE]),
            supported_aggregate_names=frozenset(["*"]),
            produces_capabilities=frozenset(["NONLINEAR_RANGE_CHMIN", "CURRENT_MAX_HIERARCHY"]),
            complexity=SymbolicComplexity(
                time_op_formula="log(N)",
                total_time_formula="Q * log(N)",
                space_bytes_formula="32 * N",
                space_complexity_class="O(N)",
                estimate_ops=lambda n, q, v, e, c: q * (int(math.log2(max(1, n))) + 1),
                estimate_bytes=lambda n, q, v, e, c: 32 * n
            ),
            description="Segment tree maintaining first and second max hierarchy for range chmin updates"
        )

        # ── 2. Phase 3J: Segment Tree ──────────────────────────────────
        universe["segment_tree_standard"] = CandidateProfile(
            candidate_id="segment_tree_standard",
            family="segment_tree",
            display_name="Standard Segment Tree (Point/Range with Lazy)",
            supported_temporals=frozenset([TemporalMode.ONLINE, TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.range_update(),
            supported_query_targets=frozenset([QueryTarget.POINT, QueryTarget.LINEAR_RANGE]),
            supported_aggregate_names=frozenset(["*"]),
            requires_capabilities=frozenset(["LINEAR_ARRAY"]),
            produces_capabilities=frozenset(["RANGE_AGGREGATION", "POINT_UPDATE", "RANGE_UPDATE"]),
            complexity=SymbolicComplexity(
                time_op_formula="log(N)",
                total_time_formula="Q * log(N)",
                space_bytes_formula="16 * N",
                space_complexity_class="O(N)",
                estimate_ops=lambda n, q, v, e, c: q * (int(math.log2(max(1, n))) + 1),
                estimate_bytes=lambda n, q, v, e, c: 16 * n
            ),
            description="Array-based 4N segment tree with lazy propagation for associative operations"
        )

        # ── 3. Phase 3I: Fenwick Tree (BIT) ───────────────────────────
        universe["fenwick_tree"] = CandidateProfile(
            candidate_id="fenwick_tree",
            family="fenwick",
            display_name="Fenwick Tree / Binary Indexed Tree",
            supported_temporals=frozenset([TemporalMode.ONLINE, TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.point_update(),
            supported_query_targets=frozenset([QueryTarget.POINT, QueryTarget.LINEAR_RANGE]),
            supported_aggregate_names=frozenset(["SUM", "XOR"]),
            requires_invertibility=True,
            requires_capabilities=frozenset(["LINEAR_ARRAY"]),
            produces_capabilities=frozenset(["RANGE_AGGREGATION", "PREFIX_AGGREGATION", "POINT_UPDATE"]),
            complexity=SymbolicComplexity(
                time_op_formula="log(N)",
                total_time_formula="Q * log(N)",
                space_bytes_formula="4 * N",
                space_complexity_class="O(N)",
                estimate_ops=lambda n, q, v, e, c: q * (int(math.log2(max(1, n))) + 1),
                estimate_bytes=lambda n, q, v, e, c: 4 * n
            ),
            description="Prefix sum tree using lowest set bit navigation over invertible groups"
        )

        # ── 4. Phase 3F: Graph Algorithms ──────────────────────────────
        universe["dijkstra_priority_queue"] = CandidateProfile(
            candidate_id="dijkstra_priority_queue",
            family="graph",
            display_name="Dijkstra Shortest Path (Min-Heap)",
            supported_temporals=frozenset([TemporalMode.ONLINE, TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.read_only(),
            supported_query_targets=frozenset([QueryTarget.POINT, QueryTarget.ALL_PAIRS]),
            supported_aggregate_names=frozenset(["MIN"]),
            preconditions=frozenset(["NON_NEGATIVE_EDGE_WEIGHTS"]),
            forbidden_properties=frozenset(["NEGATIVE_EDGE_WEIGHTS", "NEGATIVE_CYCLE"]),
            produces_capabilities=frozenset(["SHORTEST_PATH_DISTANCES"]),
            complexity=SymbolicComplexity(
                time_op_formula="(V + E) * log(V)",
                total_time_formula="(V + E) * log(V)",
                space_bytes_formula="8 * (V + E)",
                space_complexity_class="O(V + E)",
                estimate_ops=lambda n, q, v, e, c: (v + e) * (int(math.log2(max(1, v))) + 1),
                estimate_bytes=lambda n, q, v, e, c: 8 * (v + e)
            ),
            description="Single-source shortest paths on weighted graphs with strictly non-negative edge weights"
        )

        # ── 5. Phase 3F / Phase 4: Kruskal MST ─────────────────────────
        universe["kruskal_mst"] = CandidateProfile(
            candidate_id="kruskal_mst",
            family="graph",
            display_name="Kruskal MST (DSU)",
            supported_temporals=frozenset([TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.read_only(),
            supported_query_targets=frozenset([QueryTarget.POINT]),
            supported_aggregate_names=frozenset(["SUM"]),
            preconditions=frozenset(["WEIGHT_COMPARABILITY", "GREEDY_CHOICE_PROPERTY", "ACYCLIC_STRUCTURE"]),
            produces_capabilities=frozenset(["MINIMUM_SPANNING_FOREST"]),
            complexity=SymbolicComplexity(
                time_op_formula="E * log(E)",
                total_time_formula="E * log(E)",
                space_bytes_formula="8 * (V + E)",
                space_complexity_class="O(V + E)",
                estimate_ops=lambda n, q, v, e, c: e * (int(math.log2(max(1, e))) + 1),
                estimate_bytes=lambda n, q, v, e, c: 8 * (v + e)
            ),
            description="Greedy edge sorting with DSU cycle prevention on arbitrary comparable edge weights"
        )

        # ── 6. Phase 3A: Two Pointers ──────────────────────────────────
        universe["two_pointers_monotone_window"] = CandidateProfile(
            candidate_id="two_pointers_monotone_window",
            family="two_pointers",
            display_name="Two Pointers Monotone Window",
            supported_temporals=frozenset([TemporalMode.ONLINE, TemporalMode.STREAMING, TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.read_only(),
            supported_query_targets=frozenset([QueryTarget.LINEAR_RANGE]),
            supported_aggregate_names=frozenset(["SUM"]),
            preconditions=frozenset(["MONOTONE_WINDOW", "NON_NEGATIVE_ELEMENTS"]),
            forbidden_properties=frozenset(["NEGATIVE_ELEMENTS_FOR_RANGE_SUM"]),
            produces_capabilities=frozenset(["RANGE_AGGREGATION", "SUBARRAY_SUM_BOUND", "TWO_SUM_SORTED"]),
            complexity=SymbolicComplexity(
                time_op_formula="1",
                total_time_formula="N",
                space_bytes_formula="4",
                space_complexity_class="O(1)",
                estimate_ops=lambda n, q, v, e, c: 2 * n,
                estimate_bytes=lambda n, q, v, e, c: 16
            ),
            description="Linear O(N) sliding window or two-pointer traversal on monotone sequences"
        )

        # ── 7. Phase 3C / Phase 4: Monotonic Deque ─────────────────────
        universe["monotonic_deque_sliding_window"] = CandidateProfile(
            candidate_id="monotonic_deque_sliding_window",
            family="monotonic_stack",
            display_name="Monotonic Deque (Sliding Window Extremum)",
            supported_temporals=frozenset([TemporalMode.ONLINE, TemporalMode.STREAMING, TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.read_only(),
            supported_query_targets=frozenset([QueryTarget.LINEAR_RANGE]),
            supported_aggregate_names=frozenset(["MIN", "MAX"]),
            preconditions=frozenset(["SLIDING_WINDOW_MONOTONICITY", "DOMINANCE_ORDER", "WINDOW_EXPIRATION"]),
            forbidden_properties=frozenset(["NON_CONVEX_TRANSITION"]),
            produces_capabilities=frozenset(["RANGE_AGGREGATION", "SLIDING_WINDOW_EXTREMUM_O1", "OPTIMIZED_DP_TABLE"]),
            complexity=SymbolicComplexity(
                time_op_formula="1",
                total_time_formula="N",
                space_bytes_formula="4 * N",
                space_complexity_class="O(K)",
                estimate_ops=lambda n, q, v, e, c: 2 * n,
                estimate_bytes=lambda n, q, v, e, c: 4 * n
            ),
            description="Amortized O(1) sliding window extremum maintaining monotonic deque invariant"
        )

        # ── 8. Phase 3B: Binary Search ─────────────────────────────────
        universe["binary_search_bisection"] = CandidateProfile(
            candidate_id="binary_search_bisection",
            family="binary_search",
            display_name="Binary Search / Bisection",
            supported_temporals=frozenset([TemporalMode.ONLINE, TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.read_only(),
            supported_query_targets=frozenset([QueryTarget.POINT, QueryTarget.LINEAR_RANGE]),
            supported_aggregate_names=frozenset(["*"]),
            preconditions=frozenset(["MONOTONE_PREDICATE", "BOUNDED_DOMAIN"]),
            forbidden_properties=frozenset(["NON_MONOTONE_PREDICATE"]),
            produces_capabilities=frozenset(["OPTIMAL_BOUNDARY_VALUE"]),
            complexity=SymbolicComplexity(
                time_op_formula="log(Domain)",
                total_time_formula="log(Domain) * T_pred",
                space_bytes_formula="16",
                space_complexity_class="O(1)",
                estimate_ops=lambda n, q, v, e, c: 60,
                estimate_bytes=lambda n, q, v, e, c: 16
            ),
            description="Logarithmic interval bisection over monotone boolean decision predicate"
        )

        # ── 9. Phase 4 Bridge: Coordinate Compressor ──────────────────
        universe["coordinate_compressor"] = CandidateProfile(
            candidate_id="coordinate_compressor",
            family="cross_family",
            display_name="Coordinate Compressor (Sort + Unique + Bisection)",
            supported_temporals=frozenset([TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.read_only(),
            supported_query_targets=frozenset([QueryTarget.POINT, QueryTarget.LINEAR_RANGE]),
            supported_aggregate_names=frozenset(["*"]),
            requires_capabilities=frozenset(["MASSIVE_COORDINATES", "OFFLINE_COORDINATES_KNOWN"]),
            produces_capabilities=frozenset(["DENSE_INDEX_SPACE", "MAPPED_ARRAY"]),
            complexity=SymbolicComplexity(
                time_op_formula="log(N)",
                total_time_formula="N * log(N) + Q * log(N)",
                space_bytes_formula="8 * N",
                space_complexity_class="O(N)",
                estimate_ops=lambda n, q, v, e, c: n * (int(math.log2(max(1, n))) + 1) + q * (int(math.log2(max(1, n))) + 1),
                estimate_bytes=lambda n, q, v, e, c: 8 * n
            ),
            description="Transforms massive coordinate domain (up to 10^18) to compact 1..N index space"
        )

        # ── 10. Phase 3H: Disjoint Set Union ──────────────────────────
        universe["dsu_incremental"] = CandidateProfile(
            candidate_id="dsu_incremental",
            family="dsu",
            display_name="Disjoint Set Union (Path Compression + Rank)",
            supported_temporals=frozenset([TemporalMode.ONLINE, TemporalMode.OFFLINE]),
            supported_mutability=MutabilitySet.point_update(),
            supported_query_targets=frozenset([QueryTarget.POINT]),
            supported_aggregate_names=frozenset(["*"]),
            produces_capabilities=frozenset(["INCREMENTAL_CONNECTIVITY", "CYCLE_DETECTION"]),
            complexity=SymbolicComplexity(
                time_op_formula="alpha(V)",
                total_time_formula="Q * alpha(V)",
                space_bytes_formula="8 * V",
                space_complexity_class="O(V)",
                estimate_ops=lambda n, q, v, e, c: 4 * q,
                estimate_bytes=lambda n, q, v, e, c: 8 * v
            ),
            description="Near-constant time incremental dynamic connectivity and equivalence class merging"
        )

        return universe
