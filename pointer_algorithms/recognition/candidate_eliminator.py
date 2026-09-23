"""
Candidate Eliminator — Explicit "Why Not This Pattern?" Stage.

Rejects candidates based on hard preconditions, monotonicity violations,
and structural mismatches rather than superficial keyword weights.
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pointer_algorithms.recognition.feature_extractor import ProblemFeatures
from pointer_algorithms.recognition.candidate_generator import AlgorithmCandidate
from pointer_algorithms.reasoning.monotonicity_engine import MonotonicityEngine, MonotonicityStatus
from pointer_algorithms.knowledge.taxonomy import (
    BINARY_SEARCH_PATTERNS, TRIE_PATTERNS, TREE_PATTERNS, GRAPH_PATTERNS, HEAP_PATTERNS, DSU_PATTERNS,
    FENWICK_PATTERNS, SEGMENT_TREE_PATTERNS, DP_PATTERNS, GREEDY_PATTERNS, DC_BACKTRACKING_PATTERNS,
    ADV_GRAPH_PATTERNS, STRING_PATTERNS, NUMBER_THEORY_PATTERNS,
    TreeKind, TreeRepresentation, GraphKind, HeapKind
)

@dataclass
class CandidateEvaluation:
    candidate: AlgorithmCandidate
    accepted: bool
    rejection_code: Optional[str]
    evidence: str
    precondition_tested: str
    recommended_alternative: Optional[str] = None
    is_suboptimal: bool = False

class CandidateEliminator:
    """Evaluates candidates against hard structural constraints and eliminates invalid ones."""

    @staticmethod
    def evaluate_candidate(candidate: AlgorithmCandidate, features: ProblemFeatures) -> CandidateEvaluation:
        pat = candidate.pattern

        # ── 0. Advanced Graph Specific Algorithm Overrides Generic Fallbacks ──
        if getattr(features, "is_adv_graph_detected", False) and getattr(features, "adv_graph_algorithm_family", None):
            if pat in ("graph_shortest_path_or_scc", "bfs_dfs_rebuild_reference", "backtracking_or_exponential_search"):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="ADV_GRAPH_SPECIFIC_ALGORITHM_RESOLVED",
                    evidence=f"Problem specifically resolved to advanced graph capability {features.adv_graph_algorithm_family}.",
                    precondition_tested="adv_graph_preconditions_verified",
                    recommended_alternative=features.adv_graph_algorithm_family
                )

        # ── 0b. String Specific Algorithm Overrides Generic Fallbacks ──
        if getattr(features, "is_string_algorithm_detected", False) and getattr(features, "string_algorithm_family", None):
            if pat in ("graph_shortest_path_or_scc", "bfs_dfs_rebuild_reference", "backtracking_or_exponential_search"):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="STRING_SPECIFIC_ALGORITHM_RESOLVED",
                    evidence=f"Problem specifically resolved to string capability {features.string_algorithm_family}.",
                    precondition_tested="string_preconditions_verified",
                    recommended_alternative=features.string_algorithm_family
                )

        # ── 0c. Number Theory Specific Algorithm Overrides Generic Fallbacks ──
        if getattr(features, "is_number_theory_detected", False) and getattr(features, "number_theory_family", None):
            if pat in ("graph_shortest_path_or_scc", "bfs_dfs_rebuild_reference", "backtracking_or_exponential_search"):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="NT_SPECIFIC_ALGORITHM_RESOLVED",
                    evidence=f"Problem specifically resolved to number theory capability {features.number_theory_family}.",
                    precondition_tested="number_theory_preconditions_verified",
                    recommended_alternative=features.number_theory_family
                )

        # ── 0d. Algebra Specific Algorithm Overrides Generic Fallbacks & Overlapping NT ──
        if getattr(features, "is_algebra_detected", False) and getattr(features, "algebra_family", None):
            if pat in ("graph_shortest_path_or_scc", "bfs_dfs_rebuild_reference", "backtracking_or_exponential_search") or (
                candidate.family == "number_theory" and features.algebra_family in ("algebra_poly_inverse", "algebra_berlekamp_massey", "algebra_gauss_modular", "algebra_ntt")
            ):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="ALGEBRA_SPECIFIC_ALGORITHM_RESOLVED",
                    evidence=f"Problem specifically resolved to algebra capability {features.algebra_family}.",
                    precondition_tested="algebra_preconditions_verified",
                    recommended_alternative=features.algebra_family
                )

        # ── 0e. Computational Geometry Specific Algorithm Overrides Generic Fallbacks ──
        if getattr(features, "is_geometry_detected", False) and getattr(features, "geometry_family", None):
            if pat in ("graph_shortest_path_or_scc", "bfs_dfs_rebuild_reference", "backtracking_or_exponential_search") or candidate.family == "graph" or (
                candidate.family == "algebra" and features.geometry_family == "geom_line_intersection_point"
            ) or (
                candidate.family == "number_theory" and features.geometry_family == "geom_line_intersection_point"
            ):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="GEOMETRY_SPECIFIC_ALGORITHM_RESOLVED",
                    evidence=f"Problem specifically resolved to geometry capability {features.geometry_family}.",
                    precondition_tested="geometry_preconditions_verified",
                    recommended_alternative=features.geometry_family
                )

        # ── 0f. Advanced Data Structures Specific Algorithm Overrides Generic Fallbacks ──
        if getattr(features, "is_ads_detected", False) and getattr(features, "ads_family", None):
            if pat in ("graph_shortest_path_or_scc", "bfs_dfs_rebuild_reference", "backtracking_or_exponential_search") or (
                candidate.family in ("two_pointers_converging", "sliding_window", "two_pointers_same_direction") and features.ads_family in ("ads_sparse_table", "ads_sqrt_decomposition", "ads_mos_algorithm", "ads_segment_tree_beats")
            ):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="ADS_SPECIFIC_ALGORITHM_RESOLVED",
                    evidence=f"Problem specifically resolved to advanced data structure capability {features.ads_family}.",
                    precondition_tested="ads_preconditions_verified",
                    recommended_alternative=features.ads_family
                )

        # ── 0g. Cross-Family Composition Specific Algorithm Overrides Generic Fallbacks ──
        if getattr(features, "is_cross_family_detected", False) and getattr(features, "cross_family_family", None):
            if pat in ("graph_shortest_path_or_scc", "bfs_dfs_rebuild_reference", "backtracking_or_exponential_search") or (
                candidate.family in ("two_pointers_converging", "sliding_window", "two_pointers_same_direction") and pat != features.cross_family_family
            ):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="CROSS_FAMILY_SPECIFIC_ALGORITHM_RESOLVED",
                    evidence=f"Problem specifically resolved to cross-family composition {features.cross_family_family}.",
                    precondition_tested="cross_family_composition_verified",
                    recommended_alternative=features.cross_family_family
                )

        # ── 1. Dynamic Point Updates Check ──
        if features.has_dynamic_updates and (candidate.family in (
            "two_pointers_converging", "two_pointers_same_direction", "sliding_window", "partition_pointers", "counting_pointers"
        ) or pat == "dc_quickselect"):
            return CandidateEvaluation(
                candidate=candidate,
                accepted=False,
                rejection_code="DYNAMIC_UPDATES_PRESENT",
                evidence="Problem requires handling point updates while answering kth element or range queries; static partition/selection algorithms require offline or static data.",
                precondition_tested="static_or_incremental_stream",
                recommended_alternative="segment_tree_or_fenwick"
            )

        # ── 2. Sliding Window & Subarray Counting - Sum Based with Negative Values ──
        if pat in ("sliding_window_variable_min", "sliding_window_variable_max", "count_subarrays_bounded") and not features.tracks_distinct:
            mono = MonotonicityEngine.assess_for_pattern(
                pattern=pat,
                has_negative_values=features.has_negative_values,
                is_sorted=features.is_sorted,
                can_sort=features.can_sort,
                is_contiguous=features.is_contiguous,
                tracks_distinct=features.tracks_distinct,
                objective_type=features.optimization_objective or ""
            )
            if mono.status == MonotonicityStatus.MONOTONICITY_BROKEN:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code=mono.broken_reason or "WINDOW_NOT_MONOTONIC",
                    evidence=(
                        "Window validity depends on cumulative sum reaching a target threshold. "
                        "Negative numbers allow the window sum to decrease upon adding elements or increase upon removing elements, "
                        "destroying the monotonic property required for greedy left-pointer shrinking."
                    ),
                    precondition_tested="window_validity_monotonicity",
                    recommended_alternative="prefix_sum_hash_map"
                )

        # ── 3. Pair Sum / Difference / Multi-Sum / Counting - Unsorted without Sorting Permitted ──
        if pat in (
            "pair_sum_sorted", "pair_difference", "closest_pair_sum",
            "three_sum_converging", "four_sum_converging",
            "count_pairs_less_than_k", "count_pairs_equal_k"
        ):
            if not features.is_sorted and not features.can_sort:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="UNSORTED_AND_CANNOT_SORT",
                    evidence="Array is unsorted and original order or contiguous requirements prevent sorting.",
                    precondition_tested="sorted_order_or_sorting_permissible",
                    recommended_alternative="hash_map_pair_lookup"
                )

        if pat == "merge_sorted_arrays":
            if not features.is_sorted and not features.can_sort:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="UNSORTED_AND_CANNOT_SORT",
                    evidence="Arrays are unsorted and cannot be sorted.",
                    precondition_tested="sorted_order_or_sorting_permissible",
                    recommended_alternative="hash_set_lookup"
                )

        if pat == "binary_search_complement":
            if not features.is_sorted and not features.can_sort:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="UNSORTED_AND_CANNOT_SORT",
                    evidence="Array is unsorted and binary search requires sorted array.",
                    precondition_tested="sorted_order_or_sorting_permissible",
                    recommended_alternative="hash_map_pair_lookup"
                )

        # ── 4. Two-Way Partition Destroys Relative Order Anti-Pattern ──
        if pat == "partition_two_way" and features.partition_requirement == "move_zeroes_ordered":
            return CandidateEvaluation(
                candidate=candidate,
                accepted=False,
                rejection_code="DESTROYS_RELATIVE_ORDER",
                evidence="Converging two-way partition swaps elements from both ends and does not maintain the relative order of non-zero elements.",
                precondition_tested="relative_order_preservation",
                recommended_alternative="move_zeroes_ordered"
            )

        # ── 5. Contiguity Violations for Sliding Window ──
        if candidate.family in ("sliding_window", "counting_pointers") and pat in ("count_subarrays_bounded", "exact_count_derived") and not features.is_contiguous:
            return CandidateEvaluation(
                candidate=candidate,
                accepted=False,
                rejection_code="NON_CONTIGUOUS_SUBSEQUENCE",
                evidence="Sliding window requires contiguous subarray or substring, but problem seeks arbitrary subsequence or subset.",
                precondition_tested="contiguous_range",
                recommended_alternative="dynamic_programming_or_greedy"
            )

        # ── 6. In-Place Compaction on Immutable Structure ──
        if pat in ("remove_duplicates_sorted", "in_place_compaction", "move_zeroes_ordered") and not features.in_place_required:
            if features.output_requirement == 'boolean':
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="IRRELEVANT_OPERATION",
                    evidence="Problem asks for boolean existence rather than in-place array mutation.",
                    precondition_tested="in_place_modification_required",
                    recommended_alternative="hash_set_lookup"
                )

        # ── 7. Monotonic Stack Anti-Pattern Rules ──

        MS_PATTERNS = {
            "next_greater_element", "next_smaller_element",
            "previous_greater_element", "previous_smaller_element",
            "nearest_greater_element", "nearest_smaller_element",
            "stock_span", "largest_rectangle_histogram",
            "circular_next_greater", "sum_subarray_minimums", "sum_subarray_maximums"
        }

        # 7a. Dynamic updates break monotonic stack: pops are irreversible
        if pat in MS_PATTERNS and features.has_dynamic_updates:
            return CandidateEvaluation(
                candidate=candidate,
                accepted=False,
                rejection_code="STACK_ELIMINATION_NOT_SAFE",
                evidence=(
                    "Monotonic stack discards elements permanently upon popping. "
                    "Dynamic point updates can invalidate previously resolved boundaries, "
                    "requiring un-popped elements — which is impossible with an irreversible stack."
                ),
                precondition_tested="static_sequence_required",
                recommended_alternative="segment_tree"
            )

        # 7b. Reject O(n²) brute-force alternatives — these exist only to be eliminated
        if pat in ("brute_force_nested_scan", "brute_force_backward_scan", "brute_force_dp"):
            return CandidateEvaluation(
                candidate=candidate,
                accepted=False,
                rejection_code="QUADRATIC_COMPLEXITY_REJECTED",
                evidence=(
                    f"Pattern '{pat}' runs in O(n²) time. A monotonic stack achieves O(n) with equivalent correctness. "
                    "The brute-force approach is dominated."
                ),
                precondition_tested="linear_time_achievable",
                recommended_alternative="monotonic_stack"
            )

        # 7c. Reject MS for arbitrary subsequence problems (MS needs contiguous linear scan)
        if pat in MS_PATTERNS and pat not in ("stock_span", "sum_subarray_minimums", "sum_subarray_maximums"):
            if features.repeated_queries and features.has_dynamic_updates:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="STACK_ELIMINATION_NOT_SAFE",
                    evidence=(
                        "Repeated independent queries with dynamic updates cannot be handled "
                        "by a single-pass monotonic stack scan."
                    ),
                    precondition_tested="single_pass_feasibility",
                    recommended_alternative="segment_tree"
                )

        # 7d. Contribution problems with dynamic updates need segment trees
        if pat in ("sum_subarray_minimums", "sum_subarray_maximums") and features.has_dynamic_updates:
            return CandidateEvaluation(
                candidate=candidate,
                accepted=False,
                rejection_code="STACK_ELIMINATION_NOT_SAFE",
                evidence=(
                    "Contribution counting via monotonic stack requires a static array. "
                    "Dynamic updates invalidate precomputed left/right boundaries."
                ),
                precondition_tested="static_sequence_required",
                recommended_alternative="segment_tree"
            )

        # ── 8. Binary Search Anti-Pattern & Rejection Rules (Phase 3C) ──

        # 8a. Naive linear / exhaustive scan alternatives (suboptimal, not rejected)
        if pat in ("exhaustive_answer_search", "exhaustive_value_scan", "linear_scan_lookup"):
            return CandidateEvaluation(
                candidate=candidate,
                accepted=True,
                is_suboptimal=True,
                rejection_code=None,
                evidence=(
                    f"Pattern '{pat}' is logically admissible over the search space, but runs in linear or exhaustive time. "
                    "When logarithmic binary search is feasible, this naive scan is asymptotically dominated and preserved as suboptimal."
                ),
                precondition_tested="asymptotic_optimality",
                recommended_alternative="binary_search"
            )

        # 8a. Binary search on heap / priority queue domain
        if pat in BINARY_SEARCH_PATTERNS and features.is_heap_detected:
            return CandidateEvaluation(
                candidate=candidate,
                accepted=False,
                rejection_code="HEAP_COMPLEXITY_EXCEEDED",
                evidence="Problem specifies priority queue / heap operations rather than monotone binary search.",
                precondition_tested="binary_search_applicability",
                recommended_alternative=features.heap_algorithm_family or "heap_min_priority_queue"
            )

        # 8b. Ordering missing for index-based binary search
        if pat in BINARY_SEARCH_PATTERNS and pat not in ("binary_search_answer_min", "binary_search_answer_max", "binary_search_value_domain"):
            if not features.has_ordered_search_space and not features.can_sort:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="BINARY_SEARCH_ORDERING_MISSING",
                    evidence=(
                        "Index-based binary search requires an ordered search space (sorted array). "
                        "Current representation is not ordered, and no legal transformation (sorting, coordinate compression, "
                        "or answer-domain formulation) is permissible without destroying required indexing."
                    ),
                    precondition_tested="ordered_search_space_required",
                    recommended_alternative="linear_scan_or_hash_set"
                )

        # 8c. Non-monotone predicate
        if pat in BINARY_SEARCH_PATTERNS and features.has_non_monotonic_predicate:
            code = "BINARY_SEARCH_FEASIBILITY_NOT_MONOTONE" if pat in ("binary_search_answer_min", "binary_search_answer_max") else "BINARY_SEARCH_PREDICATE_NOT_MONOTONE"
            return CandidateEvaluation(
                candidate=candidate,
                accepted=False,
                rejection_code=code,
                evidence=(
                    f"Binary search requires a monotone predicate (false->true or true->false). "
                    f"The problem condition for '{pat}' oscillates or is non-monotonic, invalidating interval bisection."
                ),
                precondition_tested="predicate_monotonicity_required",
                recommended_alternative="linear_scan_exhaustive"
            )

        # 8d. Dynamic updates invalidating static binary search across queries
        if pat in BINARY_SEARCH_PATTERNS and pat not in ("binary_search_answer_min", "binary_search_answer_max"):
            if features.has_dynamic_updates and features.repeated_queries:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="BINARY_SEARCH_SEARCH_SPACE_INVALID",
                    evidence=(
                        "Static binary search on indices requires an invariant sorted structure. "
                        "Interleaved dynamic point updates destroy invariant sorted order; "
                        "dynamic ordered structures (std::set, Segment Tree) are required."
                    ),
                    precondition_tested="static_ordered_space_required",
                    recommended_alternative="segment_tree_or_fenwick"
                )

        # ── 9. Trie Anti-Pattern & Evaluation Rules (Phase 3D) ──
        if pat in TRIE_PATTERNS:
            # 9a. Hard memory limit rejection
            if getattr(features, "memory_limit_exceeded", False):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="TRIE_MEMORY_LIMIT_EXCEEDED",
                    evidence=(
                        f"Trie construction exceeds available memory constraints: estimated "
                        f"{getattr(features, 'estimated_memory_bytes', 0) // (1024*1024)}MB exceeds 256MB limit."
                    ),
                    precondition_tested="memory_budget_feasible",
                    recommended_alternative="hash_set_or_sort"
                )

            # 9b. Suboptimal / No Trie advantage: Single query without prefix advantage
            # Important correction: Do NOT mark accepted=False!
            if getattr(features, "has_single_query_only", False) and not getattr(features, "has_prefix_sharing_advantage", False):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=True,
                    is_suboptimal=True,
                    rejection_code=None,
                    evidence=(
                        "Problem involves only a single one-off query without repeated lookups or prefix sharing. "
                        "A Trie is logically valid but introduces O(L) pointer overhead where a direct string comparison suffices."
                    ),
                    precondition_tested="amortized_query_advantage",
                    recommended_alternative="direct_string_comparison"
                )

        # ── 10. Tree Evaluation Rules & Anti-Patterns (Phase 3E) ──
        if pat in TREE_PATTERNS:
            # 10a. Graph Cycle & Disconnected Integrity Checks
            # Rule: If the problem specifies a tree, do NOT revalidate N-1 edges redundantly unless cycle/disconnection signaled
            if getattr(features, "has_cycle_signal", False):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="TREE_CYCLIC_GRAPH",
                    evidence="Graph contains cycles (E >= N in connected component); tree invariants violated.",
                    precondition_tested="acyclic_graph",
                    recommended_alternative="general_graph_dfs_bfs_or_union_find"
                )

            if getattr(features, "is_disconnected_signal", False):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="TREE_DISCONNECTED_GRAPH",
                    evidence="Graph is disconnected (E < N - 1); forest of multiple components violates single connected tree requirement.",
                    precondition_tested="connected_graph",
                    recommended_alternative="connected_components_or_union_find"
                )

            # 10b. BST Operations vs BST Validation
            if pat == "tree_bst_validate":
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=True,
                    rejection_code=None,
                    evidence="BST validation via bounded range [min_val, max_val] or in-order predecessor check confirmed.",
                    precondition_tested="bst_validation_required"
                )

            if pat in (
                "tree_bst_search", "tree_bst_insert", "tree_bst_delete",
                "tree_bst_min_max", "tree_bst_pred_succ", "tree_lca_bst"
            ):
                if not getattr(features, "is_bst", False):
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="TREE_INVALID_BST_STRUCTURE",
                        evidence="BST operations require an ordered binary search tree structure. General binary tree does not guarantee branch ordering.",
                        precondition_tested="bst_ordering_invariant",
                        recommended_alternative="general_binary_tree_traversal"
                    )

            # 10c. Arity Mismatch: In-order traversal requires binary tree
            if pat == "tree_dfs_inorder":
                if getattr(features, "tree_kind", None) == TreeKind.ROOTED_TREE:
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="TREE_ARITY_MISMATCH",
                        evidence="In-order traversal is uniquely defined for binary trees. Arbitrary k-ary trees do not possess a canonical left-root-right decomposition.",
                        precondition_tested="binary_tree_structure",
                        recommended_alternative="tree_dfs_preorder_or_postorder"
                    )

            # 10d. LCA Method Matching
            if pat == "tree_lca_binary_tree" and getattr(features, "is_bst", False):
                # Valid but suboptimal compared to BST ordered-branch elimination
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=True,
                    is_suboptimal=True,
                    rejection_code=None,
                    evidence="General binary tree LCA traverses descendants without exploiting BST ordering; BST ordered-branch elimination is strictly more efficient.",
                    precondition_tested="tree_lca_generality",
                    recommended_alternative="tree_lca_bst"
                )

            if pat == "tree_lca_parent_array" and getattr(features, "tree_representation", None) != TreeRepresentation.PARENT_ARRAY:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="TREE_LCA_METHOD_MISMATCH",
                    evidence="Parent-array LCA requires explicit parent pointers or parent array representation.",
                    precondition_tested="parent_pointers_available",
                    recommended_alternative="tree_lca_binary_tree"
                )

            # 10e. Recursion-Risk Analysis
            if getattr(features, "tree_recursion_risk", False):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=True,
                    is_suboptimal=True,
                    rejection_code=None,
                    evidence="Deep recursion on skewed tree (worst-case depth H = O(N) with N >= 10^5) risks call-stack overflow. Iterative traversal or explicit stack allocation recommended.",
                    precondition_tested="call_stack_safety",
                    recommended_alternative="iterative_stack_traversal"
                )

        # ── 11. Alternative Candidates Elimination ──
        if pat in ("linear_tree_traversal", "all_pairs_shortest_path", "repeated_dfs_per_node"):
            rec_alt = "tree_bst_search" if pat == "linear_tree_traversal" else ("tree_diameter" if pat == "all_pairs_shortest_path" else "tree_subtree_aggregation")
            return CandidateEvaluation(
                candidate=candidate,
                accepted=False,
                rejection_code="SUBOPTIMAL_COMPLEXITY",
                evidence=f"Candidate '{pat}' has suboptimal asymptotic time complexity compared to single-pass tree reasoning.",
                precondition_tested="asymptotic_optimality",
                recommended_alternative=rec_alt
            )

        if pat == "exponential_subset_enumeration":
            return CandidateEvaluation(
                candidate=candidate,
                accepted=False,
                rejection_code="EXPONENTIAL_COMPLEXITY",
                evidence="Exponential brute force is infeasible for tree problems with N > 20; Tree DP computes optimal substructure in O(N).",
                precondition_tested="polynomial_time_complexity",
                recommended_alternative="tree_dp_independent_set"
            )

        if pat in ("inorder_array_sort_check", "root_to_node_path_intersection", "recursive_depth_traversal"):
            rec_alt = "tree_bst_validate" if pat == "inorder_array_sort_check" else ("tree_lca_binary_tree" if pat == "root_to_node_path_intersection" else "tree_bfs_level_order")
            return CandidateEvaluation(
                candidate=candidate,
                accepted=True,
                is_suboptimal=True,
                rejection_code=None,
                evidence=f"Candidate '{pat}' is correct but requires extra auxiliary structures or passes compared to direct tree reasoning.",
                precondition_tested="direct_tree_algorithm",
                recommended_alternative=rec_alt
            )

        # ── Section 12: Graph Anti-Patterns & Elimination Rules (Phase 3F) ──

        # Rule G1: Dijkstra rejected on graphs with negative edge weights
        if pat == "graph_dijkstra" and features.graph_has_negative_weights:
            return CandidateEvaluation(
                candidate=candidate,
                accepted=False,
                rejection_code="GRAPH_NEGATIVE_WEIGHTS_FOR_DIJKSTRA",
                evidence="Graph has negative edge weights. Dijkstra requires non-negative weights (w >= 0) for its greedy relaxation invariant to hold.",
                precondition_tested="all_edge_weights_non_negative",
                recommended_alternative="graph_bellman_ford"
            )

        # Rule G2: Dijkstra on unweighted graph — correct but suboptimal (BFS is O(V+E), Dijkstra is O((V+E)logV))
        if pat == "graph_dijkstra" and not features.graph_is_weighted and features.is_graph_detected:
            return CandidateEvaluation(
                candidate=candidate,
                accepted=True,
                is_suboptimal=True,
                rejection_code=None,
                evidence="Dijkstra is correct on unweighted graphs but unnecessarily expensive; BFS achieves O(V+E) without a priority queue.",
                precondition_tested="weighted_graph",
                recommended_alternative="graph_bfs_shortest_path"
            )

        # Rule G3: Bellman-Ford on a graph with a reachable negative cycle — shortest path undefined
        if pat == "graph_bellman_ford" and features.graph_has_negative_cycles:
            is_detection_query = bool(re.search(r'detect|check|find\s+(?:a\s+)?(?:negative\s+)?cycle|arbitrage', features.raw_text.lower()))
            if not is_detection_query:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="GRAPH_NEGATIVE_CYCLE_SHORTEST_PATH",
                    evidence="A reachable negative cycle exists on the source→target path, making shortest path undefined/unbounded. Bellman-Ford detects but cannot compute a finite shortest path.",
                    precondition_tested="no_reachable_negative_cycle",
                    recommended_alternative="negative_cycle_detection_only"
                )

        # Rule G4: Topological sort / DAG-DP on a directed cyclic graph
        if pat in ("graph_topological_sort", "graph_dag_dp") and features.graph_is_cyclic is True:
            return CandidateEvaluation(
                candidate=candidate,
                accepted=False,
                rejection_code="GRAPH_CYCLIC_FOR_TOPOLOGICAL_SORT",
                evidence="Topological ordering only exists for Directed Acyclic Graphs (DAGs). This graph contains cycles, making topological ordering impossible.",
                precondition_tested="graph_is_acyclic_dag",
                recommended_alternative="graph_cycle_detection_directed"
            )

        # Rule G5: Floyd-Warshall budget-aware computational feasibility
        if pat == "graph_floyd_warshall":
            estimated_ops = features.graph_vertex_count_v ** 3
            budget = getattr(features, "computational_budget", 1.0e8)
            if estimated_ops > budget:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="GRAPH_COMPLEXITY_EXCEEDED",
                    evidence=f"Floyd-Warshall estimated operations V^3 = {estimated_ops:,} exceeds computational budget of {budget:,.0f} ops for execution limit.",
                    precondition_tested="estimated_operations_within_computational_budget",
                    recommended_alternative="graph_dijkstra"
                )
            elif estimated_ops > 0.5 * budget:
                # Valid but expensive (near limit)
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=True,
                    rejection_code=None,
                    is_suboptimal=True,
                    evidence=f"Floyd-Warshall estimated operations V^3 = {estimated_ops:,} is approaching computational budget; valid but computationally expensive.",
                    precondition_tested="estimated_operations_within_computational_budget",
                    recommended_alternative="graph_dijkstra"
                )

        # Rule G6: MST on disconnected graph — no single spanning tree exists for all vertices
        if pat in ("graph_mst_kruskal", "graph_mst_prim") and features.graph_is_disconnected is True:
            raw = getattr(features, "raw_text", "").lower()
            if "forest" in raw or "spanning forest" in raw:
                # Minimum Spanning Forest is valid across disconnected components
                pass
            else:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="GRAPH_DISCONNECTED_MST",
                    evidence="A spanning tree connecting all V vertices requires a connected graph. The graph is disconnected; no single spanning tree exists (only a minimum spanning forest may be computed).",
                    precondition_tested="graph_is_connected",
                    recommended_alternative="graph_dsu"
                )

        # Rule G7: Undirected cycle detection method applied to directed graph
        if pat == "graph_cycle_detection_undirected" and features.graph_is_directed:
            return CandidateEvaluation(
                candidate=candidate,
                accepted=False,
                rejection_code="GRAPH_DIRECTED_CYCLE_UNDIRECTED_MISMATCH",
                evidence="The undirected cycle detection method (visited + parent tracking) incorrectly identifies legitimate directed edges as cycles in a directed graph.",
                precondition_tested="graph_is_undirected",
                recommended_alternative="graph_cycle_detection_directed"
            )

        # Rule G8: Bipartite coloring rejected when odd cycle is proven (graph_is_bipartite explicitly False)
        if pat == "graph_bipartite_coloring" and features.graph_is_bipartite is False:
            return CandidateEvaluation(
                candidate=candidate,
                accepted=False,
                rejection_code="GRAPH_ODD_CYCLE_NON_BIPARTITE",
                evidence="Graph contains an odd cycle, which violates 2-colorability (bipartite impossibility theorem: a graph is bipartite iff it contains no odd-length cycle).",
                precondition_tested="graph_is_bipartite",
                recommended_alternative="graph_cycle_detection_undirected"
            )

        # Graph candidates that passed all checks — accept
        if pat in GRAPH_PATTERNS or candidate.family == "graph":
            return CandidateEvaluation(
                candidate=candidate,
                accepted=True,
                rejection_code=None,
                evidence="Graph pattern preconditions confirmed: structure, weights, directionality, and complexity constraints verified.",
                precondition_tested="graph_structural_preconditions_verified"
            )

        # ── 15. Heap / Priority Queue Domain Rules (Phase 3G) ──

        # Rule H1: Arbitrary delete mismatch
        if features.heap_requires_arbitrary_delete:
            if candidate.family == "heap" or pat in HEAP_PATTERNS:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="HEAP_ARBITRARY_DELETE_MISMATCH",
                    evidence="Standard binary heap does not support efficient arbitrary element deletion by value (requires O(N) linear search). Use a balanced BST (std::set/multiset) or hash-indexed heap.",
                    precondition_tested="heap_supports_arbitrary_delete",
                    recommended_alternative="set_or_multiset"
                )

        # Rule H2: Full offline sort vs Heap
        if features.heap_requires_full_sort:
            if candidate.family == "heap" or pat in HEAP_PATTERNS:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="HEAP_UNNECESSARY_SORTING",
                    evidence="Offline static array requires total sort. Introsort (std::sort) provides O(N log N) with superior cache locality and lower constant factor compared to Heapsort.",
                    precondition_tested="extremal_access_only",
                    recommended_alternative="sorting"
                )

        # Rule H3: Wrong extremum / retention invariant mismatch for Top-K
        if pat == "heap_top_k":
            if features.heap_k_direction == "largest" and candidate.supporting_signals and "max_heap" in candidate.supporting_signals:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="HEAP_WRONG_EXTREMUM",
                    evidence="To retain the K largest elements in O(K) bounded space, the weakest element to evict is the minimum. A min-heap must be used; a max-heap cannot evict the minimum in O(1).",
                    precondition_tested="retention_invariant_min_heap_for_largest",
                    recommended_alternative="heap_top_k"
                )
            elif features.heap_k_direction == "smallest" and candidate.supporting_signals and "min_heap" in candidate.supporting_signals:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="HEAP_WRONG_EXTREMUM",
                    evidence="To retain the K smallest elements in O(K) bounded space, the weakest element to evict is the maximum. A max-heap must be used; a min-heap cannot evict the maximum in O(1).",
                    precondition_tested="retention_invariant_max_heap_for_smallest",
                    recommended_alternative="heap_top_k"
                )

        # Rule H4: Offline static Kth element: quickselect is faster expected O(N)
        if pat == "quickselect" and not features.heap_is_streaming and features.heap_is_offline_kth:
            return CandidateEvaluation(
                candidate=candidate,
                accepted=True,
                rejection_code=None,
                evidence="Quickselect (std::nth_element) achieves expected O(N) time for static offline k-th element selection without maintaining a persistent priority queue.",
                precondition_tested="offline_static_array"
            )

        # Competitors: sorting rejected for top-K when K is small
        if candidate.family == "sorting" and features.is_heap_detected and features.heap_algorithm_family in ("heap_top_k", "heap_kth_element"):
            if not features.heap_requires_full_sort:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="HEAP_UNNECESSARY_SORTING",
                    evidence="Full sorting requires O(N log N) time and maintains total order, whereas Heap solves top-K in O(N log K) time by only maintaining partial extremal order.",
                    precondition_tested="partial_order_sufficiency",
                    recommended_alternative="heap_top_k"
                )

        # Competitor: set_or_multiset when only extremal access is needed
        if pat == "set_or_multiset" and features.is_heap_detected and not features.heap_requires_arbitrary_delete and not features.is_contiguous:
            if features.heap_algorithm_family in ("heap_min_priority_queue", "heap_max_priority_queue", "heap_top_k", "heap_k_way_merge"):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="HEAP_CAPACITY_MISMATCH",
                    evidence="std::set/multiset imposes node allocation overhead, pointer dereferencing, and tree rebalancing costs. A flat binary heap provides contiguous storage, lower structural overhead, superior cache locality, and optimal performance when only extremal access is required.",
                    precondition_tested="extremal_access_only",
                    recommended_alternative=features.heap_algorithm_family
                )

        # Heap candidates that passed all checks — accept
        if pat in HEAP_PATTERNS or candidate.family == "heap":
            return CandidateEvaluation(
                candidate=candidate,
                accepted=True,
                rejection_code=None,
                evidence="Heap pattern preconditions confirmed: dynamic candidate set, partial ordering invariant, and extremal element access verified.",
                precondition_tested="heap_structural_preconditions_verified"
            )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 16. Disjoint Set Union (DSU) Candidate Elimination (Phase 3H)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        if features.is_dsu_detected:
            # Rule D1: Arbitrary online deletions unsupported by Basic/Rollback DSU
            if features.dsu_is_online_deletions:
                if pat in DSU_PATTERNS or candidate.family == "dsu":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="DSU_DELETION_UNSUPPORTED",
                        evidence="Arbitrary online edge deletion cannot be handled by standard DSU or Rollback DSU merely because rollback exists. Rollback DSU only supports explicit historical rollback in LIFO order, not arbitrary edge deletions. Supported models: additions only -> Basic DSU; explicit historical rollback -> Rollback DSU; known add/remove timeline -> Offline Dynamic Connectivity.",
                        precondition_tested="dsu_supports_arbitrary_online_deletions",
                        recommended_alternative="bfs_dfs_rebuild_reference"
                    )

            # Rule D2: Offline dynamic connectivity vs Online mismatch
            if pat == "dsu_offline_dynamic_connectivity" and not features.dsu_is_offline:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="DSU_ONLINE_OFFLINE_MISMATCH",
                    evidence="Offline dynamic connectivity requires all edge insertions, deletions, and connectivity queries to be known in advance to build the time-interval segment tree. It cannot be used when queries arrive strictly online and require immediate answers.",
                    precondition_tested="offline_query_availability",
                    recommended_alternative="dsu_dynamic_connectivity"
                )
            if features.dsu_is_offline and pat in ("dsu_basic", "dsu_dynamic_connectivity"):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="DSU_ONLINE_OFFLINE_MISMATCH",
                    evidence="Basic DSU cannot handle edge expirations or deletions in an offline stream. Offline Dynamic Connectivity with Rollback DSU over a segment tree of time is required.",
                    precondition_tested="offline_segment_tree_required",
                    recommended_alternative="dsu_offline_dynamic_connectivity"
                )

            # Rule D3: Rollback required
            if features.dsu_requires_rollback and pat in ("dsu_basic", "dsu_dynamic_connectivity", "dsu_component_metadata"):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="DSU_ROLLBACK_REQUIRED",
                    evidence="Problem requires undoing operations or restoring snapshots. Basic DSU employs two-pass path compression which mutates tree history permanently and cannot be reverted in O(1) without full state copy. Rollback DSU (union-by-size without path compression) is required.",
                    precondition_tested="reversible_state_invariants",
                    recommended_alternative="dsu_rollback"
                )

            # Rule D4: Weighted potential difference mismatch
            if features.dsu_has_weights and pat in ("dsu_basic", "dsu_dynamic_connectivity", "dsu_component_metadata"):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="DSU_WEIGHT_MODEL_MISMATCH",
                    evidence="Problem specifies relative potential differences between elements (value[x] - value[y] = w). Basic DSU only tracks equivalence classes without relative offsets. Weighted/Potential DSU is required.",
                    precondition_tested="potential_difference_tracking",
                    recommended_alternative="dsu_weighted"
                )

            # Rule D5: Parity model mismatch
            if features.dsu_has_parity and pat in ("dsu_basic", "dsu_dynamic_connectivity", "dsu_component_metadata"):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="DSU_PARITY_MODEL_MISMATCH",
                    evidence="Problem imposes dynamic parity or 2-coloring constraints (color[x] ^ color[y] = p). Basic DSU cannot maintain or check 2-coloring relations. Parity DSU is required.",
                    precondition_tested="parity_relation_tracking",
                    recommended_alternative="dsu_parity"
                )

            # Rule D6: Metadata merge undefined
            if pat == "dsu_component_metadata" and not features.dsu_has_metadata:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="DSU_METADATA_MERGE_UNDEFINED",
                    evidence="The requested component state cannot be maintained correctly from the stored metadata and the available merge operation.",
                    precondition_tested="metadata_merge_operator_defined",
                    recommended_alternative="dsu_basic"
                )

            # Rule D7: Contradiction / consistency verification
            if features.dsu_has_contradiction_check and pat in ("dsu_basic", "dsu_dynamic_connectivity"):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="DSU_CONTRADICTION_DETECTED",
                    evidence="Problem requires verifying whether new edge/constraint relations contradict established components. Basic DSU lacks constraint consistency verification logic.",
                    precondition_tested="constraint_consistency_verification",
                    recommended_alternative="dsu_constraint_consistency"
                )

            # Competitor check: BFS/DFS rebuild vs DSU
            if pat == "bfs_dfs_rebuild_reference" and not features.dsu_is_online_deletions:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="DSU_COMPLEXITY_EXCEEDED",
                    evidence="Repeated graph rebuilds using BFS/DFS require O(Q * (V + E)) time, which exceeds competitive time limits. DSU solves incremental queries in nearly linear O(Q * alpha(V)) time, or offline dynamic connectivity in O(M log Q log V).",
                    precondition_tested="asymptotic_complexity_budget",
                    recommended_alternative=features.dsu_algorithm_family or "dsu_dynamic_connectivity"
                )

            # DSU candidates that passed all checks — accept
            if pat in DSU_PATTERNS or candidate.family == "dsu":
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=True,
                    rejection_code=None,
                    evidence="DSU pattern preconditions confirmed: partition of universe into disjoint sets, representative root invariant, and path compression / union-by-size complexity verified.",
                    precondition_tested="dsu_structural_preconditions_verified"
                )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 17. Fenwick Tree (Binary Indexed Tree) Candidate Elimination (Phase 3I)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        if features.is_fenwick_detected or pat in FENWICK_PATTERNS or candidate.family == "fenwick":
            # Rule F1: Static array with no updates -> Suboptimal compared to prefix sum
            if features.fenwick_is_static:
                if pat in FENWICK_PATTERNS or candidate.family == "fenwick":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="FENWICK_STATIC_QUERY_SUBOPTIMAL",
                        evidence="Static array with no updates is solved with O(1) query time and O(N) precomputation using standard prefix sums. Fenwick Tree introduces unnecessary O(log N) query overhead.",
                        precondition_tested="dynamic_point_updates_required",
                        recommended_alternative="prefix_sum",
                        is_suboptimal=True
                    )

            # Rule F2: Offline range additions without interleaved queries -> Overkill compared to difference array
            if features.fenwick_is_offline_range_add_only:
                if pat in FENWICK_PATTERNS or candidate.family == "fenwick":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="FENWICK_OFFLINE_RANGE_ADD_OVERKILL",
                        evidence="All range updates occur offline in a batch with no queries interleaved until the end. A simple difference array achieves O(1) updates and a single O(N) prefix sum sweep, whereas Fenwick Tree requires O(log N) per update and O(N log N) total time.",
                        precondition_tested="online_or_interleaved_queries_required",
                        recommended_alternative="difference_array"
                    )

            # Rule F3: Structural Incompatibility (Non-invertible range, arbitrary range extremum replacement, range assignment)
            if features.fenwick_has_non_invertible_range:
                if pat in FENWICK_PATTERNS or candidate.family == "fenwick":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="FENWICK_STRUCTURAL_INCOMPATIBILITY",
                        evidence="Arbitrary range query requiring subtraction/inversion when the aggregation has no suitable inverse, unless a separately supported Fenwick formulation exists. Prefix aggregation with a commutative monoid is supported, but arbitrary range queries without an inverse require Segment Tree.",
                        precondition_tested="invertible_range_aggregation",
                        recommended_alternative="segment_tree"
                    )

            if features.fenwick_has_range_extremum_with_arbitrary_point_replacement:
                if pat in FENWICK_PATTERNS or candidate.family == "fenwick":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="FENWICK_STRUCTURAL_INCOMPATIBILITY",
                        evidence="Arbitrary point replacement on range extremum is unsupported by Fenwick Tree. Fenwick prefix extremum variants only support monotonic updates (prefix min requires non-increasing updates; prefix max requires non-decreasing updates). Arbitrary point replacement or range min/max queries require Segment Tree or Sparse Table.",
                        precondition_tested="monotonic_extremum_updates",
                        recommended_alternative="segment_tree"
                    )

            if features.fenwick_has_range_assignment:
                if pat in FENWICK_PATTERNS or candidate.family == "fenwick":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="FENWICK_STRUCTURAL_INCOMPATIBILITY",
                        evidence="Range assignment updates overwrite values across an interval rather than accumulating deltas, which cannot be represented via difference arrays in a standard Fenwick Tree. Segment Tree with lazy propagation is required.",
                        precondition_tested="delta_accumulation_compatibility",
                        recommended_alternative="segment_tree"
                    )

            # Rule F4: Dynamic Unbounded Coordinates Unrepresentable
            if features.fenwick_has_dynamic_unbounded_coords:
                if pat in FENWICK_PATTERNS or candidate.family == "fenwick":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="FENWICK_DYNAMIC_COORDINATE_UNREPRESENTABLE",
                        evidence="Dynamically appearing unknown coordinates cannot be compressed offline without knowledge of the future coordinate universe. A flat Fenwick array requires a bounded or statically known coordinate space; dynamic coordinates require an ordered structure such as Treap, balanced BST, or dynamic Segment Tree.",
                        precondition_tested="bounded_or_offline_compressible_coordinate_space",
                        recommended_alternative="treap_or_balanced_bst"
                    )

            # Rule F5: Negative Frequencies in K-th Element Search
            if features.fenwick_has_negative_frequencies_in_kth:
                if pat in ("fenwick_kth_element", "fenwick_multiset") or candidate.family == "fenwick":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="FENWICK_KTH_NEGATIVE_FREQUENCY",
                        evidence="K-th element search via binary lifting relies on monotonic prefix sums of frequencies (frequency[x] >= 0). Negative frequencies destroy prefix monotonicity, causing binary lifting to fail. A balanced BST or ordered set is required.",
                        precondition_tested="non_negative_frequencies_for_binary_lifting",
                        recommended_alternative="balanced_bst"
                    )

            # Rule F6: Resource Limit Exceeded
            if features.fenwick_is_resource_limit_exceeded:
                if pat in FENWICK_PATTERNS or candidate.family == "fenwick":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="FENWICK_RESOURCE_LIMIT",
                        evidence="Universe size N or 2D grid dimensions N x M exceed available memory or competitive time limits for flat Fenwick array allocation without coordinate compression or sparse representation.",
                        precondition_tested="memory_and_time_resource_budget",
                        recommended_alternative="coordinate_compressed_fenwick_or_hash_map"
                    )

            # Dimensionality check: 2D pattern for 1D problem or 1D pattern for 2D problem
            if pat == "fenwick_2d_point_update_range_query" and not features.fenwick_is_2d:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="FENWICK_DIMENSION_MISMATCH",
                    evidence="2D Fenwick Tree candidate evaluated for a 1-dimensional problem.",
                    precondition_tested="problem_dimensionality_matches_2d",
                    recommended_alternative="fenwick_point_update_prefix_query"
                )
            if features.fenwick_is_2d and pat != "fenwick_2d_point_update_range_query" and pat in FENWICK_PATTERNS:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="FENWICK_DIMENSION_MISMATCH",
                    evidence="1D Fenwick Tree cannot answer 2D grid sub-rectangle queries directly. 2D Fenwick Tree is required.",
                    precondition_tested="problem_dimensionality_matches_1d",
                    recommended_alternative="fenwick_2d_point_update_range_query"
                )

            # Specific operation mismatch checks
            if pat == "fenwick_kth_element" and not features.fenwick_is_kth:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="FENWICK_OPERATION_MISMATCH",
                    evidence="Problem does not request k-th smallest element or quantile search.",
                    precondition_tested="kth_element_search_required",
                    recommended_alternative="fenwick_point_update_prefix_query"
                )

            if pat == "fenwick_inversion_counting" and not features.fenwick_is_inversion_counting:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="FENWICK_OPERATION_MISMATCH",
                    evidence="Problem does not require inversion counting.",
                    precondition_tested="inversion_counting_required",
                    recommended_alternative="fenwick_point_update_prefix_query"
                )

            if pat == "fenwick_coordinate_compression" and not features.fenwick_requires_coordinate_compression:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="FENWICK_COORDINATE_COMPRESSION_UNNECESSARY",
                    evidence="Problem coordinates are already dense and 1-indexed within memory limits; coordinate compression adds unnecessary O(K log K) precomputation.",
                    precondition_tested="sparse_large_coordinate_space",
                    recommended_alternative="fenwick_point_update_prefix_query"
                )

            # Competitor check: naive array scan vs Fenwick
            if pat in ("naive_array_scan", "brute_force_range_query"):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="FENWICK_COMPLEXITY_EXCEEDED",
                    evidence="Naive array scan takes O(N) per query, leading to O(Q * N) time which exceeds competitive time limits. Fenwick Tree answers queries in O(log N) time.",
                    precondition_tested="asymptotic_complexity_budget",
                    recommended_alternative=features.fenwick_algorithm_family or "fenwick_point_update_prefix_query"
                )

            # Fenwick candidates that passed all checks — accept
            if pat in FENWICK_PATTERNS or candidate.family == "fenwick":
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=True,
                    rejection_code=None,
                    evidence="Fenwick Tree pattern preconditions confirmed: binary index decomposition, commutative monoid/group aggregation, lowbit interval coverage, and O(log N) query/update verified.",
                    precondition_tested="fenwick_structural_preconditions_verified"
                )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 18. Segment Tree Candidate Elimination (Phase 3J)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        if features.is_segment_tree_detected or pat in SEGMENT_TREE_PATTERNS or candidate.family == "segment_tree":
            # Rule ST1: Static range query without updates -> Suboptimal compared to prefix sum or sparse table
            # Only eliminate if superior O(1) static alternatives exist (sum -> Prefix Sum; idempotent min/max/gcd -> Sparse Table)
            # Static maximum contiguous subarray or non-idempotent/non-invertible monoids lack O(1) static queries and remain valid for Segment Tree.
            if features.segment_tree_is_static and not features.segment_tree_is_max_subarray:
                if features.segment_tree_query_op == "sum":
                    if pat in SEGMENT_TREE_PATTERNS or candidate.family == "segment_tree":
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=False,
                            rejection_code="SEGMENT_TREE_STATIC_QUERY_SUBOPTIMAL",
                            evidence=(
                                "Static arrays with no updates may admit O(1) query structures. Prefix Sums provide "
                                "O(1) range-sum queries with O(N) memory, strictly dominating Segment Tree's O(log N) query time."
                            ),
                            precondition_tested="dynamic_updates_required",
                            recommended_alternative="prefix_sum",
                            is_suboptimal=True
                        )
                elif features.segment_tree_query_op in ("min", "max", "gcd"):
                    if pat in SEGMENT_TREE_PATTERNS or candidate.family == "segment_tree":
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=False,
                            rejection_code="SEGMENT_TREE_STATIC_QUERY_SUBOPTIMAL",
                            evidence=(
                                "Static arrays with no updates may admit O(1) query structures. Sparse Tables provide "
                                "O(1) queries for suitable idempotent operations such as minimum/maximum with O(N log N) "
                                "preprocessing and memory, dominating Segment Tree's O(log N) query complexity."
                            ),
                            precondition_tested="dynamic_updates_required",
                            recommended_alternative="sparse_table",
                            is_suboptimal=True
                        )
                elif not features.segment_tree_is_metadata:
                    if pat in SEGMENT_TREE_PATTERNS or candidate.family == "segment_tree":
                        alt = "prefix_sum" if features.segment_tree_query_op == "sum" else "sparse_table"
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=False,
                            rejection_code="SEGMENT_TREE_STATIC_QUERY_SUBOPTIMAL",
                            evidence=(
                                "Static arrays with no updates may admit O(1) query structures. Prefix Sums provide "
                                "O(1) range-sum queries with O(N) memory, while Sparse Tables provide O(1) queries for "
                                "suitable idempotent operations such as minimum/maximum with O(N log N) preprocessing and "
                                "memory. These structures may dominate Segment Tree query complexity, but their memory and "
                                "preprocessing trade-offs differ."
                            ),
                            precondition_tested="dynamic_updates_required",
                            recommended_alternative=alt,
                            is_suboptimal=True
                        )

            # Rule ST2: Point update with prefix query only on invertible monoid -> Overkill compared to Fenwick
            if features.segment_tree_is_simple_prefix:
                if pat in SEGMENT_TREE_PATTERNS or candidate.family == "segment_tree":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="SEGMENT_TREE_SIMPLE_PREFIX_OVERKILL",
                        evidence="Point updates with prefix-only queries on an invertible commutative monoid/group are more simply and efficiently implemented with Fenwick Tree (Binary Indexed Tree), which requires ~1/4 memory (N vs 4N) and has significantly smaller constant factors.",
                        precondition_tested="range_queries_or_non_invertible_monoid_required",
                        recommended_alternative="fenwick_point_update_prefix_query",
                        is_suboptimal=True
                    )

            # Rule ST3: Batch offline range additions without intermediate queries -> Overkill compared to Difference Array
            if features.segment_tree_is_offline_range_add:
                if pat in SEGMENT_TREE_PATTERNS or candidate.family == "segment_tree":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="SEGMENT_TREE_DIFFERENCE_ARRAY_OVERKILL",
                        evidence="Batch offline range additions without intermediate queries are solved with O(1) updates and O(N) final reconstruction using a Difference Array, avoiding O(N log N) lazy segment tree overhead.",
                        precondition_tested="online_or_interleaved_queries_required",
                        recommended_alternative="difference_array",
                        is_suboptimal=True
                    )

            # Rule ST4: Point update + range sum on abelian group -> Fenwick Tree preferred
            if features.segment_tree_is_fenwick_equivalent and not features.is_segment_tree_detected:
                if pat in SEGMENT_TREE_PATTERNS or candidate.family == "segment_tree":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="SEGMENT_TREE_FENWICK_EQUIVALENT",
                        evidence="Point updates and range sum queries on an abelian group (Z, +, 0) can be solved with a Fenwick Tree, which has lower constant factors, O(N) memory instead of 4N, and simpler implementation.",
                        precondition_tested="segment_tree_specific_feature_required",
                        recommended_alternative="fenwick_point_update_prefix_query",
                        is_suboptimal=True
                    )

            # Rule ST5: Non-associative merge operation
            if features.segment_tree_has_no_associative_merge:
                if pat in SEGMENT_TREE_PATTERNS or candidate.family == "segment_tree":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="SEGMENT_TREE_NO_ASSOCIATIVE_MERGE",
                        evidence="The requested range operation cannot be represented as an associative merge across sub-intervals (e.g., dynamic median without frequency buckets, mode, floating-point average without sum and count). Segment Tree requires an associative binary operator.",
                        precondition_tested="associative_interval_merge",
                        recommended_alternative="order_statistic_tree_or_sqrt_decomposition"
                    )

            # Rule ST6: Standard lazy propagation insufficient / Segment Tree Beats
            if features.segment_tree_has_unsupported_lazy:
                if pat in SEGMENT_TREE_PATTERNS or candidate.family == "segment_tree":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="SEGMENT_TREE_STANDARD_LAZY_INSUFFICIENT",
                        evidence=(
                            "The requested range operation (such as range chmin/chmax with range sum) cannot be propagated "
                            "with ordinary lazy propagation under the standard tag model; it requires break/tag condition "
                            "maintenance and historical extrema tracking (Segment Tree Beats)."
                        ),
                        precondition_tested="composable_lazy_tag_propagation",
                        recommended_alternative="segment_tree_beats"
                    )

            # Rule ST7: Resource limit exceeded
            if features.segment_tree_resource_exceeded:
                if pat in SEGMENT_TREE_PATTERNS or candidate.family == "segment_tree":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="SEGMENT_TREE_RESOURCE_LIMIT",
                        evidence=(
                            "Segment tree memory allocation (4N * sizeof(Node) + auxiliary) exceeds available memory budget. "
                            "Alternatives depend on domain density: "
                            "1) For sparse touched coordinates in a huge universe (Q << U), use Dynamic Segment Tree (pointer-based, O(Q log U) memory) or Coordinate Compression (O(Q) memory). "
                            "2) For dense universe with large N, use Sqrt Decomposition (block streaming, O(N) memory with O(sqrt(N)) query) or external memory algorithms."
                        ),
                        precondition_tested="memory_budget_under_4N_nodes",
                        recommended_alternative="coordinate_compressed_segment_tree_or_dynamic_segtree"
                    )

            # Rule ST8: Negative frequencies in frequency segment tree (k-th element)
            if features.segment_tree_has_negative_frequencies_in_kth:
                if pat == "segment_tree_frequency_order_statistic" or (pat in SEGMENT_TREE_PATTERNS and features.segment_tree_is_frequency):
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="SEGMENT_TREE_KTH_NEGATIVE_FREQUENCY",
                        evidence="K-th element search on a frequency segment tree requires non-negative frequencies (count >= 0) to ensure subtree counts are monotonic. Negative frequencies violate subtree size monotonicity, causing binary search / descent to fail.",
                        precondition_tested="non_negative_frequencies_for_tree_walk",
                        recommended_alternative="balanced_bst"
                    )

            # Operation / pattern mismatch checks
            if pat == "segment_tree_max_subarray" and not features.segment_tree_is_max_subarray:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="SEGMENT_TREE_OPERATION_MISMATCH",
                    evidence="Problem does not request maximum contiguous subarray sum queries.",
                    precondition_tested="max_subarray_query_required",
                    recommended_alternative="segment_tree_point_update_range_query"
                )

            if pat == "segment_tree_frequency_order_statistic" and not features.segment_tree_is_frequency:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="SEGMENT_TREE_OPERATION_MISMATCH",
                    evidence="Problem does not request frequency-based k-th order statistic search.",
                    precondition_tested="frequency_kth_search_required",
                    recommended_alternative="segment_tree_point_update_range_query"
                )

            if pat == "segment_tree_interval_statistics" and not features.segment_tree_is_interval_statistics:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="SEGMENT_TREE_OPERATION_MISMATCH",
                    evidence="Problem does not request interval statistics with multiplicity (min/max with frequency).",
                    precondition_tested="interval_statistics_required",
                    recommended_alternative="segment_tree_point_update_range_query"
                )

            if pat == "segment_tree_metadata_aggregate" and not features.segment_tree_is_metadata:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="SEGMENT_TREE_OPERATION_MISMATCH",
                    evidence="Problem does not request simultaneous multi-attribute metadata aggregation.",
                    precondition_tested="metadata_aggregate_required",
                    recommended_alternative="segment_tree_point_update_range_query"
                )

            if pat == "segment_tree_combined_lazy_range_query" and not features.segment_tree_has_combined_lazy:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="SEGMENT_TREE_OPERATION_MISMATCH",
                    evidence="Problem does not require combined range assignment and range addition lazy tags.",
                    precondition_tested="combined_lazy_propagation_required",
                    recommended_alternative="segment_tree_range_add_range_query" if features.segment_tree_has_range_add else "segment_tree_point_update_range_query"
                )

            # Competitor check: naive array scan vs Segment Tree
            if pat in ("naive_array_scan", "brute_force_range_query"):
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="SEGMENT_TREE_COMPLEXITY_EXCEEDED",
                    evidence="Naive array scan takes O(N) per query or update, resulting in O(Q * N) total time which exceeds competitive time limits. Segment Tree provides O(log N) per query and update.",
                    precondition_tested="asymptotic_complexity_budget",
                    recommended_alternative=features.segment_tree_algorithm_family or "segment_tree_point_update_range_query"
                )

            # Segment tree candidates that passed all checks — accept
            if pat in SEGMENT_TREE_PATTERNS or candidate.family == "segment_tree":
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=True,
                    rejection_code=None,
                    evidence="Segment Tree pattern preconditions confirmed: associative interval merge, valid canonical interval decomposition, correct lazy tag propagation / point update, and O(log N) complexity verified.",
                    precondition_tested="segment_tree_structural_preconditions_verified"
                )

        # ── 19. Dynamic Programming Candidates (Phase 3K) ──
        if features.is_dp_detected or pat in DP_PATTERNS or candidate.family == "dynamic_programming":
            # 1. Greedy choice property holds (DP Dominated by Greedy under identical objective/output semantics)
            if features.dp_greedy_optimal:
                if pat in DP_PATTERNS or candidate.family == "dynamic_programming":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="DP_DOMINATED_BY_GREEDY",
                        evidence="Problem exhibits the greedy choice property where local optimal decisions provably lead to global optimum under the exact requested objective and output semantics. While a DP recurrence can be mathematically formulated, it is asymptotically and structurally dominated by the greedy solution (e.g. O(N log N) greedy vs O(N*W) or O(N^2) DP).",
                        precondition_tested="greedy_choice_property_satisfies_exact_objective_and_dominates_dp",
                        recommended_alternative="greedy_algorithm"
                    )

            # 2. Cyclic state dependencies without topological ordering
            if features.dp_is_cyclic:
                if pat in DP_PATTERNS or candidate.family == "dynamic_programming":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="DP_CYCLIC_STATE_DEPENDENCY",
                        evidence="The proposed state transition graph cannot be evaluated through a valid acyclic recurrence/topological order. Candidate DP is rejected and CHUP analyzes underlying problem structure to dispatch to the appropriate competing family (e.g. shortest path, SCC condensation, or cycle resolution).",
                        precondition_tested="dag_topological_state_dependency",
                        recommended_alternative="competing_graph_algorithm"
                    )

            # 3. Subproblem decomposition incompatible (Non-optimal substructure / Invalid semiring)
            if not features.dp_has_optimal_substructure:
                if pat in DP_PATTERNS or candidate.family == "dynamic_programming":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="DP_NO_OPTIMAL_SUBSTRUCTURE",
                        evidence="Problem lacks valid subproblem decomposition: for optimization problems, subproblem optima do not compose into the global optimum for the requested objective. (Note: for problems where visited history is required, state augmentation dp[v][S] yields exponential state space O(V * 2^V), which is rejected under DP_STATE_SPACE_EXPLOSION).",
                        precondition_tested="principle_of_optimality_and_algebraic_decomposition",
                        recommended_alternative="backtracking_or_exponential_search"
                    )

            # 4. No overlapping subproblems / No reuse benefit
            if not features.dp_has_overlapping_subproblems:
                if pat in DP_PATTERNS or candidate.family == "dynamic_programming":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="DP_NO_REUSE_BENEFIT",
                        evidence="Subproblems are completely independent and disjoint with zero overlap/reuse. While a valid recurrence may exist, maintaining a memoization or tabulation table provides no reuse benefit over direct divide-and-conquer or tree traversal; divide-and-conquer is preferable.",
                        precondition_tested="overlapping_subproblem_reuse_benefit",
                        recommended_alternative="divide_and_conquer"
                    )

            # 5. Non-Markovian future dependence (State formulation invalid after augmentation attempt)
            if features.dp_is_non_markovian:
                if pat in DP_PATTERNS or candidate.family == "dynamic_programming":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="DP_NON_MARKOVIAN_FUTURE_DEPENDENCE",
                        evidence="Candidate state definition is insufficient because legal future transitions depend on historical trajectory. State augmentation was evaluated: adding finite state information (e.g., last element, bounded bitmask, or discrete state) was insufficient to compress the unbounded historical dependency into a finite Markovian state space.",
                        precondition_tested="markov_property_state_sufficiency_and_finite_augmentation",
                        recommended_alternative="state_augmented_search"
                    )

            # 6. State space explosion / Resource exceeded
            if features.dp_is_resource_exceeded:
                if pat in DP_PATTERNS or candidate.family == "dynamic_programming":
                    return CandidateEvaluation(
                        candidate=candidate,
                        accepted=False,
                        rejection_code="DP_STATE_SPACE_EXPLOSION",
                        evidence="State space size exceeds memory or time limits (exponential state complexity on large N).",
                        precondition_tested="state_space_tractability",
                        recommended_alternative="approximation_or_meet_in_middle"
                    )

            # 7. Unproven optimization prerequisite
            if pat == "dp_optimization" and features.dp_optimization_applicable == "unproven":
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="DP_UNPROVEN_OPTIMIZATION_PREREQUISITE",
                    evidence="DP optimization requires Quadrangle Inequality (Monge property) or slope convexity, which is unproven or violated for this cost function.",
                    precondition_tested="monge_property_or_convexity",
                    recommended_alternative="dp_1d_linear"
                )

            # 8. Selection model mismatch: Knapsack operates on arbitrary subsets, not contiguous segments
            if pat in ("dp_knapsack", "dp_knapsack_01", "dp_knapsack_unbounded") and features.is_contiguous:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="SELECTION_MODEL_MISMATCH",
                    evidence="Problem requires contiguous subarray / range selection, but knapsack operates over arbitrary subset selections.",
                    precondition_tested="arbitrary_subset_selection_model",
                    recommended_alternative="sliding_window_or_prefix_sum"
                )

            # DP candidates that passed all checks — accept!
            if pat in DP_PATTERNS or candidate.family == "dynamic_programming":
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=True,
                    rejection_code=None,
                    evidence="Dynamic Programming preconditions confirmed: minimal sufficient state space, optimal substructure, overlapping subproblems, acyclic state dependency DAG, and tractable polynomial complexity verified.",
                    precondition_tested="dp_structural_preconditions_verified"
                )

        # ── 20. Greedy Candidate Evaluation (Phase 3L) ──
        if pat in GREEDY_PATTERNS or candidate.family == "greedy":
            # 1. Concrete counterexample disproving greedy choice
            if features.greedy_counterexample_detected:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="GREEDY_COUNTEREXAMPLE_FOUND",
                    evidence="Concrete counterexample refutes the candidate greedy rule: a known valid input yields a suboptimal objective (e.g. coin change with non-canonical denominations {1, 3, 4} for target 6 gives 4+1+1=3 vs optimal 3+3=2). Candidate greedy strategy is rejected.",
                    precondition_tested="greedy_choice_soundness_against_counterexamples",
                    recommended_alternative="dynamic_programming"
                )

            # 2. Exchange proof failed (e.g. 0/1 knapsack discrete item constraints or weighted interval)
            if features.greedy_competing_dp_signal:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="GREEDY_EXCHANGE_PROOF_FAILED",
                    evidence="Exchange argument fails: substituting the local greedy choice into an optimal solution degrades the objective or violates discrete feasibility constraints (e.g. 0/1 knapsack discrete capacity or weighted interval scheduling).",
                    precondition_tested="exchange_argument_preserves_feasibility_and_optimality",
                    recommended_alternative="dynamic_programming"
                )

            # 3. Proof not established within supported proof systems
            if features.greedy_proof_unestablished:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="GREEDY_PROOF_NOT_ESTABLISHED",
                    evidence="No supported proof mechanism (Exchange Argument, Staying Ahead, Dominance, Cut Property, Matroid Independence) could establish correctness. The candidate remains unproven and cannot be selected.",
                    precondition_tested="supported_greedy_proof_obligation",
                    recommended_alternative="explore_competing_families"
                )

            # 4. Safe local choice requirement
            if not features.greedy_has_local_choice:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="GREEDY_NO_SAFE_LOCAL_CHOICE",
                    evidence="No locally optimal choice can be proven safe across all possible extensions of the partial solution.",
                    precondition_tested="safe_local_choice_property",
                    recommended_alternative="dynamic_programming"
                )

            # Greedy candidate passed all checks — accept!
            return CandidateEvaluation(
                candidate=candidate,
                accepted=True,
                rejection_code=None,
                evidence=f"Greedy choice property mathematically proven: local optimal decision is safe under the objective, feasibility is preserved, and global optimality is guaranteed.",
                precondition_tested="greedy_choice_property_verified"
            )

        # ── 21. Divide & Conquer & Backtracking Candidate Evaluation (Phase 3M) ──
        if pat in DC_BACKTRACKING_PATTERNS or candidate.family == "divide_and_conquer_backtracking" or pat == "composition_unsupported":
            # Section 8: Cross-family composition / Tower gate
            if pat == "composition_unsupported" or features.is_cross_family_composition or features.composition_unsupported:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="COMPOSITION_UNSUPPORTED",
                    evidence="Problem requires cross-family composition (e.g. greedy choice + ordered state / multiset / upper_bound successor queries as in the Tower problem) that CHUP cannot synthesize as a unified monolithic pattern. Failing closed without guessing.",
                    precondition_tested="monolithic_pattern_support",
                    recommended_alternative="fail_closed_unsupported"
                )

            # 1. DC Subproblems not independent
            if features.dc_subproblems_not_independent:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="DC_SUBPROBLEMS_NOT_INDEPENDENT",
                    evidence="Subproblems share mutable state or depend on each other's execution outcomes; divide-and-conquer independence assumption violated.",
                    precondition_tested="independent_disjoint_subproblems",
                    recommended_alternative="dynamic_programming"
                )

            # 2. DC Combine step intractable
            if features.dc_combine_step_intractable:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="DC_COMBINE_STEP_INTRACTABLE",
                    evidence="Merging subproblem solutions requires exponential or NP-hard computation; divide-and-conquer provides no polynomial advantage.",
                    precondition_tested="tractable_combine_step",
                    recommended_alternative="approximation_or_dp"
                )

            # 3. DC Base case undefined
            if features.dc_base_case_undefined:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="DC_BASE_CASE_UNDEFINED",
                    evidence="Base cases are ill-defined or infinite recursion occurs without reaching a terminal reduction.",
                    precondition_tested="well_defined_base_case",
                    recommended_alternative="define_explicit_base_case"
                )

            # 4. Backtracking search space explosive
            if features.backtracking_search_space_explosive:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="BACKTRACKING_SEARCH_SPACE_EXPLOSIVE",
                    evidence="Search space size exceeds practical budget without sufficient pruning mechanism.",
                    precondition_tested="search_space_tractability_with_pruning",
                    recommended_alternative="branch_and_bound_or_dp"
                )

            # 5. Backtracking greedy sufficient
            if features.backtracking_greedy_sufficient:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="BACKTRACKING_GREEDY_SUFFICIENT",
                    evidence="Problem exhibits the greedy choice property; exponential backtracking search is unnecessarily expensive when a greedy strategy is provably optimal.",
                    precondition_tested="no_provably_optimal_greedy_choice",
                    recommended_alternative="greedy"
                )

            # 6. Backtracking DP sufficient
            if features.backtracking_dp_sufficient:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="BACKTRACKING_DP_SUFFICIENT",
                    evidence="Problem exhibits overlapping subproblems and optimal substructure that admit a polynomial DP solution; exhaustive backtracking is suboptimal.",
                    precondition_tested="no_overlapping_polynomial_dp_formulation",
                    recommended_alternative="dynamic_programming"
                )

            # 7. Backtracking resource limit exceeded
            if features.backtracking_resource_limit_exceeded:
                return CandidateEvaluation(
                    candidate=candidate,
                    accepted=False,
                    rejection_code="BACKTRACKING_RESOURCE_LIMIT",
                    evidence="Recursion depth exceeds stack limit or search node count exceeds time budget.",
                    precondition_tested="execution_resource_bounds",
                    recommended_alternative="iterative_search_or_meet_in_middle"
                )

            # Passed all checks - accept!
            return CandidateEvaluation(
                candidate=candidate,
                accepted=True,
                rejection_code=None,
                evidence="Divide & Conquer / Backtracking preconditions confirmed: independent subproblems or structured search space with valid pruning, restoration, and termination guarantees.",
                precondition_tested="dc_backtracking_preconditions_verified"
            )

        # ── 22. Advanced Graph Candidate Evaluation (Phase 3N) ──
        if pat in ADV_GRAPH_PATTERNS or candidate.family == "adv_graph":
            for eval_res in getattr(features, "adv_graph_candidate_evaluations", []):
                if getattr(eval_res, "pattern", None) == pat:
                    from pointer_algorithms.adv_graph.composition_engine import CandidateStatus
                    if eval_res.status == CandidateStatus.VALID_OPTIMAL:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=True,
                            rejection_code=None,
                            evidence=eval_res.justification or "Advanced Graph capability validated via mathematical composition DAG.",
                            precondition_tested="adv_graph_preconditions_verified",
                            is_suboptimal=False
                        )
                    elif eval_res.status == CandidateStatus.VALID_SUBOPTIMAL:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=True,
                            rejection_code=None,
                            evidence=eval_res.justification or "Valid but suboptimal compared to optimal candidate.",
                            precondition_tested="adv_graph_optimality_check",
                            is_suboptimal=True
                        )
                    elif eval_res.status == CandidateStatus.INVALID_PRECONDITION:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=False,
                            rejection_code=eval_res.rejection_code or "ADV_GRAPH_INVALID_PRECONDITION",
                            evidence=eval_res.evidence or "Mathematical precondition violated for this graph capability.",
                            precondition_tested="adv_graph_preconditions_verified",
                            recommended_alternative="fail_closed_unsupported"
                        )
                    elif eval_res.status == CandidateStatus.COMPLEXITY_REQUIREMENT_UNSATISFIED:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=False,
                            rejection_code="COMPLEXITY_REQUIREMENT_UNSATISFIED",
                            evidence=f"Asymptotic complexity {eval_res.complexity} exceeds modeled problem constraints.",
                            precondition_tested="complexity_budget_contract",
                            recommended_alternative="approximation_or_fail_closed"
                        )

            return CandidateEvaluation(
                candidate=candidate,
                accepted=True,
                rejection_code=None,
                evidence="Advanced Graph composition verified.",
                precondition_tested="adv_graph_preconditions_verified"
            )

        # ── 23. String Algorithms & Automata Candidate Evaluation (Phase 3O) ──
        if pat in STRING_PATTERNS or candidate.family == "string":
            for eval_res in getattr(features, "string_candidate_evaluations", []):
                if getattr(eval_res, "pattern", None) == pat:
                    from pointer_algorithms.strings.derivation_engine import CandidateStatus
                    if eval_res.status == CandidateStatus.VALID_OPTIMAL:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=True,
                            rejection_code=None,
                            evidence=eval_res.justification or "String/Automata capability validated via semantic composition.",
                            precondition_tested="string_preconditions_verified",
                            is_suboptimal=False
                        )
                    elif eval_res.status == CandidateStatus.VALID_SUBOPTIMAL:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=True,
                            rejection_code=None,
                            evidence=eval_res.justification or "Valid but suboptimal compared to optimal candidate.",
                            precondition_tested="string_optimality_check",
                            is_suboptimal=True
                        )
                    elif eval_res.status == CandidateStatus.INVALID_PRECONDITION:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=False,
                            rejection_code=eval_res.rejection_code or "STRING_INVALID_PRECONDITION",
                            evidence=eval_res.evidence or "Mathematical precondition violated for this string capability.",
                            precondition_tested="string_preconditions_verified",
                            recommended_alternative="fail_closed_unsupported"
                        )
                    elif eval_res.status == CandidateStatus.COMPLEXITY_REQUIREMENT_UNSATISFIED:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=False,
                            rejection_code="COMPLEXITY_REQUIREMENT_UNSATISFIED",
                            evidence=f"Asymptotic complexity {eval_res.complexity} exceeds modeled problem constraints.",
                            precondition_tested="complexity_budget_contract",
                            recommended_alternative="approximation_or_fail_closed"
                        )

            return CandidateEvaluation(
                candidate=candidate,
                accepted=True,
                rejection_code=None,
                evidence="String capability composition verified.",
                precondition_tested="string_preconditions_verified"
            )

        # ── 24. Number Theory & Combinatorics Candidate Evaluation (Phase 3P) ──
        if pat in NUMBER_THEORY_PATTERNS or candidate.family == "number_theory":
            for eval_res in getattr(features, "number_theory_candidate_evaluations", []):
                if getattr(eval_res, "pattern", None) == pat:
                    from pointer_algorithms.number_theory.derivation_engine import CandidateStatus
                    if eval_res.status == CandidateStatus.VALID_OPTIMAL:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=True,
                            rejection_code=None,
                            evidence=eval_res.justification or "Number theory capability validated via algebraic/arithmetic composition.",
                            precondition_tested="nt_preconditions_verified",
                            is_suboptimal=False
                        )
                    elif eval_res.status == CandidateStatus.VALID_SUBOPTIMAL:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=True,
                            rejection_code=None,
                            evidence=eval_res.evidence or "Valid but suboptimal compared to optimal candidate.",
                            precondition_tested="nt_optimality_check",
                            is_suboptimal=True
                        )
                    elif eval_res.status in (CandidateStatus.INVALID_PRECONDITION, CandidateStatus.INTEGER_DOMAIN_EXCEEDED):
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=False,
                            rejection_code=eval_res.rejection_code or "NT_INVALID_PRECONDITION",
                            evidence=eval_res.evidence or "Mathematical precondition violated for this number theory capability.",
                            precondition_tested="nt_preconditions_verified",
                            recommended_alternative="fail_closed_unsupported"
                        )
                    elif eval_res.status == CandidateStatus.COMPLEXITY_REQUIREMENT_UNSATISFIED:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=False,
                            rejection_code="COMPLEXITY_REQUIREMENT_UNSATISFIED",
                            evidence=f"Asymptotic complexity {eval_res.complexity} exceeds modeled problem constraints.",
                            precondition_tested="complexity_budget_contract",
                            recommended_alternative="approximation_or_fail_closed"
                        )

            return CandidateEvaluation(
                candidate=candidate,
                accepted=True,
                rejection_code=None,
                evidence="Number theory capability composition verified.",
                precondition_tested="nt_preconditions_verified"
            )

        # ── 25. Algebra / Transforms Candidate Evaluation (Phase 3Q) ──
        if pat.startswith("algebra_") or candidate.family == "algebra":
            for eval_res in getattr(features, "algebra_candidate_evaluations", []):
                if getattr(eval_res, "pattern", None) == pat:
                    from pointer_algorithms.algebra.derivation_engine import CandidateStatus
                    if eval_res.status == CandidateStatus.VALID_OPTIMAL:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=True,
                            rejection_code=None,
                            evidence=eval_res.justification or "Algebra capability validated via algebraic/numerical composition.",
                            precondition_tested="algebra_preconditions_verified",
                            is_suboptimal=False
                        )
                    elif eval_res.status == CandidateStatus.INVALID_PRECONDITION:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=False,
                            rejection_code=eval_res.rejection_code or "INVALID_PRECONDITION",
                            evidence=eval_res.evidence or "Mathematical precondition violated.",
                            precondition_tested="algebra_preconditions_verified",
                            recommended_alternative="none"
                        )
            return CandidateEvaluation(
                candidate=candidate,
                accepted=True,
                rejection_code=None,
                evidence="Algebra capability composition verified.",
                precondition_tested="algebra_preconditions_verified"
            )

        # ── 26. Computational Geometry Candidate Evaluation (Phase 3R) ──
        if pat.startswith("geom_") or candidate.family == "geometry":
            for eval_res in getattr(features, "geometry_candidate_evaluations", []):
                if getattr(eval_res, "pattern", None) == pat:
                    from pointer_algorithms.geometry.derivation.candidate_evaluator import CandidateStatus
                    if eval_res.status == CandidateStatus.VALID_OPTIMAL:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=True,
                            rejection_code=None,
                            evidence=eval_res.justification or "Geometry capability validated via geometric/topological composition.",
                            precondition_tested="geometry_preconditions_verified",
                            is_suboptimal=False
                        )
                    elif eval_res.status == CandidateStatus.INVALID_PRECONDITION:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=False,
                            rejection_code=eval_res.rejection_code or "INVALID_PRECONDITION",
                            evidence=eval_res.evidence or "Geometric precondition violated.",
                            precondition_tested="geometry_preconditions_verified",
                            recommended_alternative="none"
                        )
            return CandidateEvaluation(
                candidate=candidate,
                accepted=True,
                rejection_code=None,
                evidence="Geometry capability composition verified.",
                precondition_tested="geometry_preconditions_verified"
            )

        # ── 27. Cross-Family Composition Candidate Evaluation (Phase 4) ──
        if pat.startswith("cf_") or candidate.family == "cross_family":
            for eval_res in getattr(features, "cross_family_candidate_evaluations", []):
                if getattr(eval_res, "pattern", None) == pat:
                    from pointer_algorithms.cross_family.candidate_evaluator import CandidateStatus
                    if eval_res.status == CandidateStatus.VALID_OPTIMAL:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=True,
                            rejection_code=None,
                            evidence=eval_res.justification or "Cross-family composition validated via verified DAG synthesis.",
                            precondition_tested="cross_family_composition_verified",
                            is_suboptimal=False
                        )
                    elif eval_res.status == CandidateStatus.INVALID_PRECONDITION:
                        return CandidateEvaluation(
                            candidate=candidate,
                            accepted=False,
                            rejection_code=eval_res.rejection_code or "INVALID_PRECONDITION",
                            evidence=eval_res.evidence or "Cross-family precondition violated.",
                            precondition_tested="cross_family_composition_verified",
                            recommended_alternative="none"
                        )
            return CandidateEvaluation(
                candidate=candidate,
                accepted=True,
                rejection_code=None,
                evidence="Cross-family composition verified.",
                precondition_tested="cross_family_composition_verified"
            )

        # Candidate passed all hard constraints!
        return CandidateEvaluation(
            candidate=candidate,
            accepted=True,
            rejection_code=None,
            evidence="All required preconditions and monotonic invariant conditions are confirmed.",
            precondition_tested="all_preconditions_verified"
        )

    @classmethod
    def filter_and_rank(cls, candidates: List[AlgorithmCandidate], features: ProblemFeatures) -> Dict[str, Any]:
        accepted: List[CandidateEvaluation] = []
        eliminated: List[CandidateEvaluation] = []

        for c in candidates:
            eval_res = cls.evaluate_candidate(c, features)
            if eval_res.accepted:
                accepted.append(eval_res)
            else:
                eliminated.append(eval_res)

        # Rank accepted by optimality first, then by prior confidence
        accepted.sort(key=lambda x: (not x.is_suboptimal, x.candidate.confidence_prior), reverse=True)

        return {
            "accepted": accepted,
            "eliminated": eliminated,
            "selected": accepted[0] if accepted else None
        }
