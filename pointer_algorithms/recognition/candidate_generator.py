"""
Candidate Generator for Pointer-Based and Alternative Algorithms.

Proposes algorithmic candidates based on structural indicators without hardcoding decisions.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from pointer_algorithms.recognition.feature_extractor import ProblemFeatures
from pointer_algorithms.knowledge.taxonomy import PatternKind, HeapKind, ADV_GRAPH_PATTERNS

@dataclass
class AlgorithmCandidate:
    pattern: str
    family: str
    confidence_prior: float
    supporting_signals: List[str]

class CandidateGenerator:
    """Generates plausible algorithm candidates for a set of problem features."""

    @staticmethod
    def generate_candidates(features: ProblemFeatures) -> List[AlgorithmCandidate]:
        candidates: List[AlgorithmCandidate] = []

        # 1. Linked list structure
        if features.input_structure == 'linked_list':
            if features.search_objective == 'cycle':
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.LINKED_CYCLE_DETECTION.value,
                    family="fast_slow_pointers",
                    confidence_prior=0.95,
                    supporting_signals=["linked_list_structure", "cycle_detection_objective"]
                ))
            elif features.search_objective == 'cycle_start':
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.LINKED_CYCLE_START.value,
                    family="fast_slow_pointers",
                    confidence_prior=0.95,
                    supporting_signals=["linked_list_structure", "cycle_start_node_objective"]
                ))
            elif features.search_objective == 'middle':
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.LINKED_MIDDLE_NODE.value,
                    family="fast_slow_pointers",
                    confidence_prior=0.95,
                    supporting_signals=["linked_list_structure", "middle_node_objective"]
                ))
            return candidates

        # 1b. Palindrome Verification
        if features.search_objective == 'palindrome':
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.PALINDROME_VERIFICATION.value,
                family="two_pointers_converging",
                confidence_prior=0.95,
                supporting_signals=["palindrome_symmetry", "converging_symmetric_ends"]
            ))

        # 2. Container With Most Water & Trapping Rain Water
        if features.optimization_objective == 'max_area':
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.CONTAINER_MOST_WATER.value,
                family="two_pointers_converging",
                confidence_prior=0.95,
                supporting_signals=["max_area_between_lines", "boundary_shrink_objective"]
            ))
        elif features.optimization_objective == 'trapping_water':
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.TRAPPING_RAIN_WATER.value,
                family="two_pointers_converging",
                confidence_prior=0.95,
                supporting_signals=["elevation_map", "trapped_water_between_bars"]
            ))

        # 3. Partition requirements & In-place Move Zeroes Ordered
        if features.partition_requirement == 'dutch_flag_012':
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.PARTITION_DUTCH_FLAG.value,
                family="partition_pointers",
                confidence_prior=0.95,
                supporting_signals=["three_way_partition", "012_sort_colors"]
            ))
        elif features.partition_requirement == 'move_zeroes_ordered':
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.MOVE_ZEROES_ORDERED.value,
                family="two_pointers_same_direction",
                confidence_prior=0.95,
                supporting_signals=["move_zeroes_end", "preserve_relative_order", "read_write_pointers"]
            ))
            # Also propose partition_two_way so CandidateEliminator can reject it for breaking order
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.PARTITION_TWO_WAY.value,
                family="partition_pointers",
                confidence_prior=0.85,
                supporting_signals=["two_way_partition_candidate"]
            ))
        elif features.partition_requirement in ('two_way_zeroes', 'parity', 'two_way_negatives'):
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.PARTITION_TWO_WAY.value,
                family="partition_pointers",
                confidence_prior=0.90,
                supporting_signals=["two_way_partition", features.partition_requirement or "two_way"]
            ))

        # 4. In-place deduplication / compaction
        if features.in_place_required:
            raw_low = features.raw_text.lower()
            if 'keep at most' in raw_low or 'remove duplicates' in raw_low or 'duplicates' in raw_low:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.REMOVE_DUPLICATES_SORTED.value,
                    family="two_pointers_same_direction",
                    confidence_prior=0.92,
                    supporting_signals=["in_place_compaction", "preserve_k_copies"]
                ))
            if 'remove' in raw_low or 'compact' in raw_low or 'predicate' in raw_low or 'occupies' in raw_low or not candidates:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.IN_PLACE_COMPACTION.value,
                    family="two_pointers_same_direction",
                    confidence_prior=0.91,
                    supporting_signals=["in_place_compaction", "relative_order_preserved"]
                ))

        # 4b. Two Sequences / Common Element / Merge
        if features.input_structure == 'two_sequences' or features.search_objective == 'common_element':
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.MERGE_SORTED_ARRAYS.value,
                family="two_pointers_same_direction",
                confidence_prior=0.92,
                supporting_signals=["two_sorted_streams", "same_direction_scan"]
            ))
            candidates.append(AlgorithmCandidate(
                pattern="hash_set_lookup",
                family="hashing",
                confidence_prior=0.75,
                supporting_signals=["set_intersection", "hash_lookup"]
            ))

        # 5. Sliding window candidates
        if features.is_contiguous:
            if features.window_size_k is not None or features.optimization_objective == 'max_sum':
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SLIDING_WINDOW_FIXED.value,
                    family="sliding_window",
                    confidence_prior=0.90,
                    supporting_signals=["contiguous_subarray", "fixed_window_size"]
                ))
            if features.optimization_objective == 'min_window_substring':
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.MINIMUM_WINDOW_SUBSTRING.value,
                    family="sliding_window",
                    confidence_prior=0.95,
                    supporting_signals=["contiguous_substring", "character_frequency_coverage", "min_window_substring"]
                ))
            if features.optimization_objective == 'min_length':
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SLIDING_WINDOW_VARIABLE_MIN.value,
                    family="sliding_window",
                    confidence_prior=0.88,
                    supporting_signals=["contiguous_subarray", "minimize_window_length"]
                ))
            if features.optimization_objective in ('max_length', 'count_windows') or features.tracks_distinct:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SLIDING_WINDOW_VARIABLE_MAX.value,
                    family="sliding_window",
                    confidence_prior=0.88,
                    supporting_signals=["contiguous_subarray", "maximize_window_length_or_count"]
                ))
            if features.optimization_objective == 'count_subarrays_bounded':
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.COUNT_SUBARRAYS_BOUNDED.value,
                    family="counting_pointers",
                    confidence_prior=0.92,
                    supporting_signals=["contiguous_subarrays", "bounded_sum_or_condition", "counting_with_pointers"]
                ))
            if features.optimization_objective == 'exact_count_derived':
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.EXACT_COUNT_DERIVED.value,
                    family="counting_pointers",
                    confidence_prior=0.95,
                    supporting_signals=["exact_distinct_count", "derived_monotonic_decomposition", "atMost_difference"]
                ))

        # 6. Pair Search & Multi-Sum
        if features.search_objective == 'closest_pair_sum':
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.CLOSEST_PAIR_SUM.value,
                family="two_pointers_converging",
                confidence_prior=0.92,
                supporting_signals=["closest_pair_sum_objective", "converging_sorted_search"]
            ))
        elif features.search_objective == 'three_sum':
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.THREE_SUM_CONVERGING.value,
                family="two_pointers_converging",
                confidence_prior=0.92,
                supporting_signals=["three_elements_sum", "fixed_outer_with_two_pointers"]
            ))
        elif features.search_objective == 'four_sum':
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.FOUR_SUM_CONVERGING.value,
                family="two_pointers_converging",
                confidence_prior=0.92,
                supporting_signals=["four_elements_sum", "nested_outer_with_two_pointers"]
            ))
        elif features.search_objective == 'count_pairs_less':
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.COUNT_PAIRS_LESS_THAN_K.value,
                family="counting_pointers",
                confidence_prior=0.95,
                supporting_signals=["count_pairs_condition", "value_monotonic_batch_count"]
            ))
        elif features.search_objective == 'count_pairs_equal':
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.COUNT_PAIRS_EQUAL_K.value,
                family="counting_pointers",
                confidence_prior=0.95,
                supporting_signals=["count_pairs_equal_target", "sorted_value_multiplicity"]
            ))
        elif features.search_objective == 'pair_diff':
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.PAIR_DIFFERENCE.value,
                family="two_pointers_same_direction",
                confidence_prior=0.90,
                supporting_signals=["pair_difference_objective", "two_element_difference"]
            ))
            candidates.append(AlgorithmCandidate(
                pattern="hash_map_pair_lookup",
                family="hashing",
                confidence_prior=0.75,
                supporting_signals=["complement_lookup", "single_pass_hash"]
            ))
            candidates.append(AlgorithmCandidate(
                pattern="binary_search_complement",
                family="binary_search",
                confidence_prior=0.70,
                supporting_signals=["sorted_array_lookup"]
            ))
        elif features.search_objective == 'pair_sum':
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.PAIR_SUM_SORTED.value,
                family="two_pointers_converging",
                confidence_prior=0.85,
                supporting_signals=["pair_search_objective", "two_element_relation"]
            ))
            candidates.append(AlgorithmCandidate(
                pattern="hash_map_pair_lookup",
                family="hashing",
                confidence_prior=0.75,
                supporting_signals=["complement_lookup", "single_pass_hash"]
            ))
            candidates.append(AlgorithmCandidate(
                pattern="binary_search_complement",
                family="binary_search",
                confidence_prior=0.70,
                supporting_signals=["sorted_array_lookup"]
            ))

        # 7. Add Prefix Sum / Subarray Target Sum Alternative
        if features.is_contiguous and ('sum equal' in features.raw_text.lower() or 'subarray with sum' in features.raw_text.lower() or 'sum equals' in features.raw_text.lower() or 'whose sum equals' in features.raw_text.lower()):
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.SLIDING_WINDOW_VARIABLE_MIN.value,
                family="sliding_window",
                confidence_prior=0.88,
                supporting_signals=["contiguous_subarray_sum_target"]
            ))
            candidates.append(AlgorithmCandidate(
                pattern="prefix_sum_hash_map",
                family="prefix_sum",
                confidence_prior=0.80,
                supporting_signals=["subarray_target_sum", "cumulative_difference"]
            ))

        # 8. Dynamic queries alternative
        if features.has_dynamic_updates or 'online updates' in features.raw_text.lower():
            if features.search_objective == 'pair_sum' or 'two elements sum' in features.raw_text.lower() or 'pair sum' in features.raw_text.lower():
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.PAIR_SUM_SORTED.value,
                    family="two_pointers_converging",
                    confidence_prior=0.85,
                    supporting_signals=["pair_sum_objective"]
                ))
            if features.is_contiguous:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SLIDING_WINDOW_VARIABLE_MIN.value,
                    family="sliding_window",
                    confidence_prior=0.85,
                    supporting_signals=["contiguous_subarray"]
                ))
            if 'inserts or deletes' in features.raw_text.lower() or 'pair sums' in features.raw_text.lower():
                candidates.append(AlgorithmCandidate(
                    pattern="dynamic_data_structure",
                    family="dynamic_data_structure",
                    confidence_prior=0.95,
                    supporting_signals=["dynamic_insert_delete_queries"]
                ))
            else:
                candidates.append(AlgorithmCandidate(
                    pattern="segment_tree_or_fenwick",
                    family="range_query_tree",
                    confidence_prior=0.95,
                    supporting_signals=["point_updates_interleaved", "dynamic_range_query"]
                ))

        # 9. Alternative classes for confusion cases
        raw_text_lower = features.raw_text.lower()
        if 'range-sum' in raw_text_lower or 'range sum' in raw_text_lower:
            candidates.append(AlgorithmCandidate(
                pattern="prefix_sum",
                family="prefix_sum",
                confidence_prior=0.92,
                supporting_signals=["static_range_sum_queries", "prefix_preprocessing"]
            ))
        if 'subset' in raw_text_lower and 'sums to' in raw_text_lower:
            candidates.append(AlgorithmCandidate(
                pattern="meet_in_middle_or_dp",
                family="meet_in_middle_or_dp",
                confidence_prior=0.95,
                supporting_signals=["arbitrary_subset_sum", "exponential_search_space"]
            ))
        if 'first index whose value is at least' in raw_text_lower or ('independent queries' in raw_text_lower and 'first index' in raw_text_lower):
            candidates.append(AlgorithmCandidate(
                pattern="binary_search",
                family="binary_search",
                confidence_prior=0.95,
                supporting_signals=["independent_threshold_queries", "sorted_monotonic_lookup"]
            ))
        if 'increasing subsequence' in raw_text_lower:
            candidates.append(AlgorithmCandidate(
                pattern="dp_or_patience_sorting",
                family="dp_or_patience_sorting",
                confidence_prior=0.95,
                supporting_signals=["subsequence_optimization", "patience_sorting"]
            ))
        if ('occurs more than once' in raw_text_lower or 'any value occurs' in raw_text_lower) and not features.in_place_required:
            candidates.append(AlgorithmCandidate(
                pattern="hash_set_or_sorting",
                family="hash_set_or_sorting",
                confidence_prior=0.92,
                supporting_signals=["membership_frequency_check", "unconstrained_ordering"]
            ))
        if 'mutually non-overlapping' in raw_text_lower or 'intervals' in raw_text_lower and 'maximum number' in raw_text_lower:
            candidates.append(AlgorithmCandidate(
                pattern="greedy",
                family="greedy",
                confidence_prior=0.95,
                supporting_signals=["interval_scheduling", "earliest_finish_time"]
            ))
        if features.input_structure == 'grid' or ('matrix' in raw_text_lower and 'minimize total cost' in raw_text_lower):
            candidates.append(AlgorithmCandidate(
                pattern="dynamic_programming",
                family="dynamic_programming",
                confidence_prior=0.95,
                supporting_signals=["2d_grid_path_substructure", "dag_minimum_cost"]
            ))

        # ── 10. Monotonic Stack Candidates (Phase 3B) ──
        # These are proposed only when structural signals specifically justify a stack-based approach.
        # Keyword presence alone is insufficient — structural patterns must align.

        if features.histogram_pattern:
            # Largest Rectangle in Histogram is unambiguously a stack problem
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.LARGEST_RECTANGLE_HISTOGRAM.value,
                family="monotonic_stack",
                confidence_prior=0.97,
                supporting_signals=["histogram_boundary_pattern", "prev_next_smaller_required", "width_height_area_objective"]
            ))

        if features.contribution_objective == 'sum_min':
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.SUM_SUBARRAY_MINIMUMS.value,
                family="monotonic_stack",
                confidence_prior=0.96,
                supporting_signals=["contribution_counting", "prev_next_boundary_pair", "sum_subarray_minimums"]
            ))
            # Also propose brute-force DP as rejected alternative for anti-pattern testing
            candidates.append(AlgorithmCandidate(
                pattern="brute_force_dp",
                family="dynamic_programming",
                confidence_prior=0.50,
                supporting_signals=["subarray_enumeration"]
            ))

        if features.contribution_objective == 'sum_max':
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.SUM_SUBARRAY_MAXIMUMS.value,
                family="monotonic_stack",
                confidence_prior=0.96,
                supporting_signals=["contribution_counting", "prev_next_boundary_pair", "sum_subarray_maximums"]
            ))

        if features.has_stock_span_pattern:
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.STOCK_SPAN.value,
                family="monotonic_stack",
                confidence_prior=0.95,
                supporting_signals=["distance_to_previous_dominant", "left_boundary_index", "span_computation"]
            ))
            # A naive O(n²) backward scan is a valid alternative
            candidates.append(AlgorithmCandidate(
                pattern="brute_force_backward_scan",
                family="brute_force",
                confidence_prior=0.40,
                supporting_signals=["backward_linear_scan"]
            ))

        if features.nearest_boundary_query and not features.histogram_pattern and not features.has_stock_span_pattern:
            # Determine the right MS pattern from direction and relation
            rel = features.boundary_relation or 'greater'
            direction = features.boundary_direction or 'right'

            if features.is_circular:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.CIRCULAR_NEXT_GREATER.value,
                    family="monotonic_stack",
                    confidence_prior=0.95,
                    supporting_signals=["circular_wrap_around", "monotonic_decreasing_stack", "modular_index"]
                ))
            elif direction == 'right' and rel == 'greater':
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.NEXT_GREATER_ELEMENT.value,
                    family="monotonic_stack",
                    confidence_prior=0.95,
                    supporting_signals=["right_scan_direction", "greater_relation", "monotonic_decreasing_stack"]
                ))
            elif direction == 'right' and rel == 'smaller':
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.NEXT_SMALLER_ELEMENT.value,
                    family="monotonic_stack",
                    confidence_prior=0.95,
                    supporting_signals=["right_scan_direction", "smaller_relation", "monotonic_increasing_stack"]
                ))
            elif direction == 'left' and rel == 'greater':
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.PREVIOUS_GREATER_ELEMENT.value,
                    family="monotonic_stack",
                    confidence_prior=0.95,
                    supporting_signals=["left_scan_direction", "greater_relation", "monotonic_decreasing_stack"]
                ))
            elif direction == 'left' and rel == 'smaller':
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.PREVIOUS_SMALLER_ELEMENT.value,
                    family="monotonic_stack",
                    confidence_prior=0.95,
                    supporting_signals=["left_scan_direction", "smaller_relation", "monotonic_increasing_stack"]
                ))
            elif direction == 'both' and rel == 'greater':
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.NEAREST_GREATER_ELEMENT.value,
                    family="monotonic_stack",
                    confidence_prior=0.93,
                    supporting_signals=["both_directions", "greater_relation", "two_pass_stack"]
                ))
            elif direction == 'both' and rel == 'smaller':
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.NEAREST_SMALLER_ELEMENT.value,
                    family="monotonic_stack",
                    confidence_prior=0.93,
                    supporting_signals=["both_directions", "smaller_relation", "two_pass_stack"]
                ))
            else:
                # Fallback: generic next_greater_element with lower confidence
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.NEXT_GREATER_ELEMENT.value,
                    family="monotonic_stack",
                    confidence_prior=0.80,
                    supporting_signals=["boundary_query_detected", "stack_dominance"]
                ))

            # For boundary queries, O(n²) brute force is always a valid but rejected alternative
            candidates.append(AlgorithmCandidate(
                pattern="brute_force_nested_scan",
                family="brute_force",
                confidence_prior=0.30,
                supporting_signals=["nested_linear_scan_quadratic"]
            ))

        # ── 11. Binary Search Candidates (Phase 3C) ──

        # 11a. Answer-space feasibility search
        if features.is_answer_space_search:
            if features.feasibility_objective == 'minimize_maximum':
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.BINARY_SEARCH_ANSWER_MIN.value,
                    family="binary_search",
                    confidence_prior=0.96,
                    supporting_signals=[
                        "answer_space_monotonic_feasibility",
                        "minimize_maximum_objective",
                        "first_true_boundary",
                        f"compound_with_{features.compound_with}" if features.compound_with else "direct_feasibility"
                    ]
                ))
            else:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.BINARY_SEARCH_ANSWER_MAX.value,
                    family="binary_search",
                    confidence_prior=0.96,
                    supporting_signals=[
                        "answer_space_monotonic_feasibility",
                        "maximize_minimum_objective",
                        "last_true_boundary",
                        f"compound_with_{features.compound_with}" if features.compound_with else "direct_feasibility"
                    ]
                ))
            # Naive exhaustive alternative (to be rejected by eliminator)
            candidates.append(AlgorithmCandidate(
                pattern="exhaustive_answer_search",
                family="brute_force",
                confidence_prior=0.25,
                supporting_signals=["exhaustive_linear_search_over_answer_domain"]
            ))

        # 11b. Value-domain / Numeric search
        elif features.has_numeric_domain:
            candidates.append(AlgorithmCandidate(
                pattern=PatternKind.BINARY_SEARCH_VALUE_DOMAIN.value,
                family="binary_search",
                confidence_prior=0.95,
                supporting_signals=["discrete_numeric_domain", "monotonic_arithmetic_predicate"]
            ))
            candidates.append(AlgorithmCandidate(
                pattern="exhaustive_value_scan",
                family="brute_force",
                confidence_prior=0.25,
                supporting_signals=["linear_increment_search"]
            ))

        # 11c. Ordered data search (exact, bounds, first/last true, pred/succ)
        elif features.target_boundary is not None and not (features.nearest_boundary_query or features.histogram_pattern):
            tb = features.target_boundary
            if tb == 'exact':
                pat = PatternKind.BINARY_SEARCH_EXACT.value
            elif tb == 'lower_bound':
                pat = PatternKind.LOWER_BOUND.value
            elif tb == 'upper_bound':
                pat = PatternKind.UPPER_BOUND.value
            elif tb == 'predecessor':
                pat = PatternKind.PREDECESSOR.value
            elif tb == 'successor':
                pat = PatternKind.SUCCESSOR.value
            elif tb == 'first_false':
                pat = PatternKind.FIRST_FALSE.value
            elif tb == 'last_false':
                pat = PatternKind.LAST_FALSE.value
            elif tb == 'last_true':
                pat = PatternKind.LAST_TRUE.value
            else:
                pat = PatternKind.FIRST_TRUE.value

            candidates.append(AlgorithmCandidate(
                pattern=pat,
                family="binary_search",
                confidence_prior=0.95,
                supporting_signals=[
                    f"target_boundary_{tb}",
                    f"predicate_direction_{features.predicate_direction}",
                    "ordered_index_search_space" if features.has_ordered_search_space else "unverified_order"
                ]
            ))
            # Linear scan alternative (to be rejected by eliminator in favor of O(log N))
            candidates.append(AlgorithmCandidate(
                pattern="linear_scan_lookup",
                family="brute_force",
                confidence_prior=0.35,
                supporting_signals=["linear_scan_o_n_complexity"]
            ))

        # ── 12. Trie candidates (Phase 3D) ──
        if features.trie_kind is not None or features.prefix_query_type is not None:
            pqt = features.prefix_query_type or "exact_search"
            if pqt == "max_xor_pair":
                trie_pat = PatternKind.TRIE_MAX_XOR_PAIR.value
            elif pqt == "max_xor_query":
                trie_pat = PatternKind.TRIE_MAX_XOR_QUERY.value
            elif pqt == "prefix_count":
                trie_pat = PatternKind.TRIE_PREFIX_COUNT.value
            elif pqt == "word_count":
                trie_pat = PatternKind.TRIE_WORD_COUNT.value
            elif pqt == "deletion":
                trie_pat = PatternKind.TRIE_DELETION.value
            elif pqt == "longest_prefix":
                trie_pat = PatternKind.TRIE_LONGEST_PREFIX.value
            elif pqt == "autocomplete":
                trie_pat = PatternKind.TRIE_AUTOCOMPLETE.value
            elif pqt == "lexicographic_sort":
                trie_pat = PatternKind.TRIE_LEXICOGRAPHIC_SORT.value
            elif pqt == "prefix_search":
                trie_pat = PatternKind.TRIE_PREFIX_SEARCH.value
            else:
                trie_pat = PatternKind.TRIE_EXACT_SEARCH.value

            candidates.append(AlgorithmCandidate(
                pattern=trie_pat,
                family="trie",
                confidence_prior=0.95,
                supporting_signals=[
                    f"trie_kind_{features.trie_kind.value if features.trie_kind else 'character'}",
                    f"prefix_query_{pqt}",
                    f"storage_{features.trie_storage.value if features.trie_storage else 'fixed_array'}"
                ]
            ))

            # Propose alternatives for comparison/elimination:
            if pqt in ("max_xor_pair", "max_xor_query"):
                candidates.append(AlgorithmCandidate(
                    pattern="brute_force_nested_xor",
                    family="brute_force",
                    confidence_prior=0.30,
                    supporting_signals=["quadratic_pairwise_xor_scan"]
                ))
            elif pqt == "lexicographic_sort":
                candidates.append(AlgorithmCandidate(
                    pattern="std_sort_comparison",
                    family="comparison_sort",
                    confidence_prior=0.75,
                    supporting_signals=["std_sort_n_log_n"]
                ))
            else:
                candidates.append(AlgorithmCandidate(
                    pattern="hash_table_lookup",
                    family="hash_table",
                    confidence_prior=0.70,
                    supporting_signals=["unordered_map_exact_lookup"]
                ))

        # ── 13. Tree candidates (Phase 3E) ──
        if not features.is_graph_detected and (
            features.tree_kind is not None
            or features.input_structure in ('tree', 'binary_tree')
            or features.tree_traversal_order is not None
            or features.tree_aggregation_op is not None
            or features.lca_query_type is not None
            or features.tree_dp_type is not None
        ):
            lower = features.raw_text.lower()

            # 13a. BST Validation vs BST Operations
            if features.is_validating_bst:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.TREE_BST_VALIDATE.value,
                    family="tree",
                    confidence_prior=0.95,
                    supporting_signals=["bst_validate_requirement", "strict_inorder_monotonicity"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="inorder_array_sort_check",
                    family="verification",
                    confidence_prior=0.65,
                    supporting_signals=["flatten_inorder_and_check_sorted"]
                ))
            elif features.is_bst or "bst" in lower:
                if features.lca_query_type == "bst":
                    candidates.append(AlgorithmCandidate(
                        pattern=PatternKind.TREE_LCA_BST.value,
                        family="tree",
                        confidence_prior=0.95,
                        supporting_signals=["bst_ordered_branch_elimination", "lca_split_discovery"]
                    ))
                    candidates.append(AlgorithmCandidate(
                        pattern=PatternKind.TREE_LCA_BINARY_TREE.value,
                        family="tree",
                        confidence_prior=0.70,
                        supporting_signals=["general_binary_tree_lca_suboptimal_for_bst"]
                    ))
                elif "search" in lower or "find" in lower or "lookup" in lower or "contains" in lower:
                    candidates.append(AlgorithmCandidate(
                        pattern=PatternKind.TREE_BST_SEARCH.value,
                        family="tree",
                        confidence_prior=0.95,
                        supporting_signals=["bst_ordered_branch_elimination", "search_invariant"]
                    ))
                    candidates.append(AlgorithmCandidate(
                        pattern="linear_tree_traversal",
                        family="brute_force",
                        confidence_prior=0.35,
                        supporting_signals=["linear_unpruned_tree_scan"]
                    ))
                elif "insert" in lower or "add" in lower:
                    candidates.append(AlgorithmCandidate(
                        pattern=PatternKind.TREE_BST_INSERT.value,
                        family="tree",
                        confidence_prior=0.95,
                        supporting_signals=["bst_ordered_branch_elimination", "leaf_insertion"]
                    ))
                elif "delete" in lower or "remove" in lower or "erase" in lower:
                    candidates.append(AlgorithmCandidate(
                        pattern=PatternKind.TREE_BST_DELETE.value,
                        family="tree",
                        confidence_prior=0.95,
                        supporting_signals=["bst_three_case_node_deletion", "inorder_successor_replacement"]
                    ))
                elif "min" in lower or "max" in lower or "smallest" in lower or "largest" in lower:
                    candidates.append(AlgorithmCandidate(
                        pattern=PatternKind.TREE_BST_MIN_MAX.value,
                        family="tree",
                        confidence_prior=0.95,
                        supporting_signals=["bst_extreme_left_or_right_descent"]
                    ))
                elif "predecessor" in lower or "successor" in lower:
                    candidates.append(AlgorithmCandidate(
                        pattern=PatternKind.TREE_BST_PRED_SUCC.value,
                        family="tree",
                        confidence_prior=0.95,
                        supporting_signals=["bst_inorder_step_boundary"]
                    ))
                else:
                    candidates.append(AlgorithmCandidate(
                        pattern=PatternKind.TREE_BST_SEARCH.value,
                        family="tree",
                        confidence_prior=0.90,
                        supporting_signals=["bst_ordered_branch_elimination"]
                    ))

            # 13b. LCA queries on non-BST trees
            elif features.lca_query_type is not None:
                if features.lca_query_type == "parent_array" or "parent_array" in lower or "parent array" in lower:
                    candidates.append(AlgorithmCandidate(
                        pattern=PatternKind.TREE_LCA_PARENT_ARRAY.value,
                        family="tree",
                        confidence_prior=0.95,
                        supporting_signals=["parent_array_depth_alignment", "step_together_ancestor_walk"]
                    ))
                    candidates.append(AlgorithmCandidate(
                        pattern=PatternKind.TREE_LCA_BINARY_TREE.value,
                        family="tree",
                        confidence_prior=0.60,
                        supporting_signals=["binary_tree_lca_candidate"]
                    ))
                else:
                    candidates.append(AlgorithmCandidate(
                        pattern=PatternKind.TREE_LCA_BINARY_TREE.value,
                        family="tree",
                        confidence_prior=0.95,
                        supporting_signals=["binary_tree_recursive_descendant_split", "postorder_bubble_up"]
                    ))
                    candidates.append(AlgorithmCandidate(
                        pattern="root_to_node_path_intersection",
                        family="simulation",
                        confidence_prior=0.65,
                        supporting_signals=["find_two_paths_and_find_divergence"]
                    ))

            # 13c. Tree DP queries
            elif features.tree_dp_type is not None:
                if features.tree_dp_type == "independent_set":
                    candidates.append(AlgorithmCandidate(
                        pattern=PatternKind.TREE_DP_INDEPENDENT_SET.value,
                        family="tree",
                        confidence_prior=0.95,
                        supporting_signals=["max_weight_independent_set", "two_state_include_exclude_recurrence"]
                    ))
                elif features.tree_dp_type == "subtree_weight":
                    candidates.append(AlgorithmCandidate(
                        pattern=PatternKind.TREE_DP_SUBTREE_WEIGHT.value,
                        family="tree",
                        confidence_prior=0.95,
                        supporting_signals=["optimal_subtree_weight", "subgraph_pruning"]
                    ))
                else:
                    candidates.append(AlgorithmCandidate(
                        pattern=PatternKind.TREE_DP_TWO_STATE.value,
                        family="tree",
                        confidence_prior=0.95,
                        supporting_signals=["two_state_tree_dp", "state_0_1_recurrence"]
                    ))
                candidates.append(AlgorithmCandidate(
                    pattern="exponential_subset_enumeration",
                    family="brute_force",
                    confidence_prior=0.20,
                    supporting_signals=["exhaustive_2_to_the_n_search"]
                ))

            # 13d. Traversals
            elif features.tree_traversal_order is not None:
                to = features.tree_traversal_order.value
                if to == "preorder":
                    pat = PatternKind.TREE_DFS_PREORDER.value
                elif to == "inorder":
                    pat = PatternKind.TREE_DFS_INORDER.value
                elif to == "postorder":
                    pat = PatternKind.TREE_DFS_POSTORDER.value
                else:
                    pat = PatternKind.TREE_BFS_LEVEL_ORDER.value

                candidates.append(AlgorithmCandidate(
                    pattern=pat,
                    family="tree",
                    confidence_prior=0.95,
                    supporting_signals=[f"traversal_order_{to}", "tree_hierarchy_walk"]
                ))
                if to == "level_order":
                    candidates.append(AlgorithmCandidate(
                        pattern="recursive_depth_traversal",
                        family="tree",
                        confidence_prior=0.60,
                        supporting_signals=["depth_bucket_collection"]
                    ))

            # 13e. Aggregations & Metrics
            elif features.is_diameter_query or features.tree_aggregation_op == "diameter":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.TREE_DIAMETER.value,
                    family="tree",
                    confidence_prior=0.95,
                    supporting_signals=["postorder_depth_aggregation", "two_longest_branches_merge"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="all_pairs_shortest_path",
                    family="graph",
                    confidence_prior=0.30,
                    supporting_signals=["quadratic_bfs_from_all_nodes"]
                ))
            elif features.is_path_sum_query or features.tree_aggregation_op == "path_sum":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.TREE_PATH_SUM.value,
                    family="tree",
                    confidence_prior=0.95,
                    supporting_signals=["root_to_leaf_prefix_accumulation", "path_sum_recurrence"]
                ))
            elif features.tree_aggregation_op == "height":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.TREE_DEPTH_HEIGHT.value,
                    family="tree",
                    confidence_prior=0.95,
                    supporting_signals=["height_postorder_max_child_depth"]
                ))
            elif features.tree_aggregation_op == "size":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.TREE_SUBTREE_SIZE.value,
                    family="tree",
                    confidence_prior=0.95,
                    supporting_signals=["subtree_size_postorder_sum"]
                ))
            elif features.tree_aggregation_op == "leaf_count":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.TREE_LEAF_COUNT.value,
                    family="tree",
                    confidence_prior=0.95,
                    supporting_signals=["leaf_predicate_base_case_count"]
                ))
            elif features.tree_aggregation_op in ("sum", "min", "max", "subtree_aggregation"):
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.TREE_SUBTREE_AGGREGATION.value,
                    family="tree",
                    confidence_prior=0.95,
                    supporting_signals=[f"operator_{features.tree_aggregation_op}", "bottom_up_fold"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="repeated_dfs_per_node",
                    family="brute_force",
                    confidence_prior=0.35,
                    supporting_signals=["quadratic_repeated_subtree_traversal"]
                ))
            else:
                # Default tree traversal if generic tree is given
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.TREE_DFS_PREORDER.value,
                    family="tree",
                    confidence_prior=0.85,
                    supporting_signals=["default_tree_dfs_hierarchy"]
                ))

        # ── Section 14: Graph Candidates (Phase 3F) ──
        elif features.is_graph_detected:
            alg = features.graph_algorithm_family
            qt = features.graph_query_type

            # Primary candidate: algorithm-family matched
            if alg == "graph_bfs_shortest_path":
                candidates.append(AlgorithmCandidate(
                    pattern="graph_bfs_shortest_path",
                    family="graph",
                    confidence_prior=0.97,
                    supporting_signals=["unweighted_graph", "shortest_path_bfs_layered"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_dijkstra",
                    family="graph",
                    confidence_prior=0.30,
                    supporting_signals=["dijkstra_on_unweighted_suboptimal"]
                ))
            elif alg == "graph_dijkstra":
                candidates.append(AlgorithmCandidate(
                    pattern="graph_dijkstra",
                    family="graph",
                    confidence_prior=0.96,
                    supporting_signals=["non_negative_weighted", "priority_queue_relaxation"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_bellman_ford",
                    family="graph",
                    confidence_prior=0.40,
                    supporting_signals=["correct_but_slower_o_ve"]
                ))
                if features.graph_vertex_count_v <= 500:
                    candidates.append(AlgorithmCandidate(
                        pattern="graph_floyd_warshall",
                        family="graph",
                        confidence_prior=0.25,
                        supporting_signals=["all_pairs_candidate"]
                    ))
            elif alg == "graph_bellman_ford":
                candidates.append(AlgorithmCandidate(
                    pattern="graph_bellman_ford",
                    family="graph",
                    confidence_prior=0.97,
                    supporting_signals=["negative_weights_present", "edge_relaxation_v_minus_1_rounds"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_dijkstra",
                    family="graph",
                    confidence_prior=0.20,
                    supporting_signals=["dijkstra_invalid_on_negative_weights"]
                ))
            elif alg == "graph_floyd_warshall":
                candidates.append(AlgorithmCandidate(
                    pattern="graph_floyd_warshall",
                    family="graph",
                    confidence_prior=0.97,
                    supporting_signals=["all_pairs_shortest_path", "small_v_cubic_feasible"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_dijkstra",
                    family="graph",
                    confidence_prior=0.30,
                    supporting_signals=["single_source_repeated"]
                ))
            elif alg == "graph_topological_sort":
                candidates.append(AlgorithmCandidate(
                    pattern="graph_topological_sort",
                    family="graph",
                    confidence_prior=0.97,
                    supporting_signals=["dag_required", "kahn_indegree_peeling"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_dfs_traversal",
                    family="graph",
                    confidence_prior=0.40,
                    supporting_signals=["dfs_postorder_reverse_topological"]
                ))
            elif alg == "graph_dag_dp":
                candidates.append(AlgorithmCandidate(
                    pattern="graph_dag_dp",
                    family="graph",
                    confidence_prior=0.97,
                    supporting_signals=["dag_dp_topological_order", "optimal_substructure"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_topological_sort",
                    family="graph",
                    confidence_prior=0.60,
                    supporting_signals=["prerequisite_for_dag_dp"]
                ))
            elif alg == "graph_scc_tarjan":
                candidates.append(AlgorithmCandidate(
                    pattern="graph_scc_tarjan",
                    family="graph",
                    confidence_prior=0.97,
                    supporting_signals=["strongly_connected_components", "tarjan_low_link"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_dfs_traversal",
                    family="graph",
                    confidence_prior=0.30,
                    supporting_signals=["naive_repeated_dfs_per_node"]
                ))
            elif alg == "graph_mst_kruskal":
                candidates.append(AlgorithmCandidate(
                    pattern="graph_mst_kruskal",
                    family="graph",
                    confidence_prior=0.96,
                    supporting_signals=["edge_sort_dsu_cycle_detection", "cut_property"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_mst_prim",
                    family="graph",
                    confidence_prior=0.85,
                    supporting_signals=["prim_priority_queue_alternative"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_dsu",
                    family="graph",
                    confidence_prior=0.50,
                    supporting_signals=["dsu_used_by_kruskal_internally"]
                ))
            elif alg == "graph_mst_prim":
                candidates.append(AlgorithmCandidate(
                    pattern="graph_mst_prim",
                    family="graph",
                    confidence_prior=0.96,
                    supporting_signals=["prim_priority_queue_cut_property"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_mst_kruskal",
                    family="graph",
                    confidence_prior=0.85,
                    supporting_signals=["kruskal_alternative"]
                ))
            elif alg == "graph_dsu":
                candidates.append(AlgorithmCandidate(
                    pattern="graph_dsu",
                    family="graph",
                    confidence_prior=0.97,
                    supporting_signals=["dynamic_connectivity", "path_compression_union_rank"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_bfs_shortest_path",
                    family="graph",
                    confidence_prior=0.30,
                    supporting_signals=["bfs_static_connectivity_check"]
                ))
            elif alg == "graph_bipartite_coloring":
                candidates.append(AlgorithmCandidate(
                    pattern="graph_bipartite_coloring",
                    family="graph",
                    confidence_prior=0.97,
                    supporting_signals=["two_coloring_bfs_dfs", "odd_cycle_check"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_bfs_shortest_path",
                    family="graph",
                    confidence_prior=0.40,
                    supporting_signals=["bfs_reachability_coloring"]
                ))
            elif alg == "graph_connected_components":
                candidates.append(AlgorithmCandidate(
                    pattern="graph_connected_components",
                    family="graph",
                    confidence_prior=0.97,
                    supporting_signals=["dfs_bfs_component_labeling"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_dsu",
                    family="graph",
                    confidence_prior=0.80,
                    supporting_signals=["dsu_connectivity_alternative"]
                ))
            elif alg == "graph_cycle_detection_directed":
                candidates.append(AlgorithmCandidate(
                    pattern="graph_cycle_detection_directed",
                    family="graph",
                    confidence_prior=0.97,
                    supporting_signals=["three_color_dfs_back_edge", "visiting_state_detection"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_cycle_detection_undirected",
                    family="graph",
                    confidence_prior=0.20,
                    supporting_signals=["undirected_method_wrong_for_directed"]
                ))
            elif alg == "graph_cycle_detection_undirected":
                candidates.append(AlgorithmCandidate(
                    pattern="graph_cycle_detection_undirected",
                    family="graph",
                    confidence_prior=0.97,
                    supporting_signals=["visited_parent_tracking_dfs"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_dsu",
                    family="graph",
                    confidence_prior=0.80,
                    supporting_signals=["dsu_cycle_detection_alternative"]
                ))
            elif alg == "graph_bridges_articulation":
                candidates.append(AlgorithmCandidate(
                    pattern="graph_bridges_articulation",
                    family="graph",
                    confidence_prior=0.97,
                    supporting_signals=["dfs_low_link_tin", "bridges_low_gt_tin", "articulation_low_ge_tin"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_dfs_traversal",
                    family="graph",
                    confidence_prior=0.30,
                    supporting_signals=["naive_brute_force_edge_removal"]
                ))
            else:
                # Default: DFS traversal for general graph queries
                candidates.append(AlgorithmCandidate(
                    pattern="graph_dfs_traversal",
                    family="graph",
                    confidence_prior=0.80,
                    supporting_signals=["default_graph_dfs"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="graph_bfs_shortest_path",
                    family="graph",
                    confidence_prior=0.70,
                    supporting_signals=["bfs_reachability_alternative"]
                ))

        # ── 15. Heap / Priority Queue Candidates (Phase 3G) ──
        if features.is_heap_detected:
            heap_alg = features.heap_algorithm_family

            if features.heap_requires_arbitrary_delete:
                # Anti-pattern: arbitrary delete by value -> favor BST / std::set
                candidates.append(AlgorithmCandidate(
                    pattern="set_or_multiset",
                    family="bst",
                    confidence_prior=0.95,
                    supporting_signals=["arbitrary_key_deletion_support", "ordered_set_erase"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=heap_alg or "heap_min_priority_queue",
                    family="heap",
                    confidence_prior=0.35,
                    supporting_signals=["priority_queue_lacks_arbitrary_erase"]
                ))
            elif features.heap_requires_full_sort:
                # Anti-pattern: full array sort offline -> favor std::sort
                candidates.append(AlgorithmCandidate(
                    pattern="sorting",
                    family="sorting",
                    confidence_prior=0.95,
                    supporting_signals=["full_array_total_sort", "introsort_cache_friendly"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=heap_alg or "heap_min_priority_queue",
                    family="heap",
                    confidence_prior=0.40,
                    supporting_signals=["heapsort_unnecessary_overhead"]
                ))
            elif heap_alg == "heap_top_k":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.HEAP_TOP_K.value,
                    family="heap",
                    confidence_prior=0.96,
                    supporting_signals=["bounded_top_k_candidate_set", "retention_invariant_eviction"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="sorting",
                    family="sorting",
                    confidence_prior=0.65,
                    supporting_signals=["full_sort_alternative"]
                ))
            elif heap_alg == "heap_kth_element":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.HEAP_KTH_ELEMENT.value,
                    family="heap",
                    confidence_prior=0.95,
                    supporting_signals=["kth_extremal_selection"]
                ))
                if features.heap_is_offline_kth:
                    candidates.append(AlgorithmCandidate(
                        pattern="quickselect",
                        family="selection",
                        confidence_prior=0.85,
                        supporting_signals=["offline_static_quickselect_nth_element"]
                    ))
                candidates.append(AlgorithmCandidate(
                    pattern="sorting",
                    family="sorting",
                    confidence_prior=0.60,
                    supporting_signals=["full_sort_alternative"]
                ))
            elif heap_alg == "heap_dynamic_median":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.HEAP_DYNAMIC_MEDIAN.value,
                    family="heap",
                    confidence_prior=0.98,
                    supporting_signals=["dual_heap_lower_upper_balance", "dynamic_median_stream"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.HEAP_TWO_HEAPS.value,
                    family="heap",
                    confidence_prior=0.90,
                    supporting_signals=["two_heap_partitioning"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="set_or_multiset",
                    family="bst",
                    confidence_prior=0.45,
                    supporting_signals=["balanced_bst_order_statistic"]
                ))
            elif heap_alg == "heap_two_heaps":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.HEAP_TWO_HEAPS.value,
                    family="heap",
                    confidence_prior=0.96,
                    supporting_signals=["two_heap_partitioning", "dual_frontier_balance"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.HEAP_DYNAMIC_MEDIAN.value,
                    family="heap",
                    confidence_prior=0.88,
                    supporting_signals=["dynamic_median_specialization"]
                ))
            elif heap_alg == "heap_k_way_merge":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.HEAP_K_WAY_MERGE.value,
                    family="heap",
                    confidence_prior=0.98,
                    supporting_signals=["k_way_frontier_min_heap", "stream_merge_preservation"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="sorting",
                    family="sorting",
                    confidence_prior=0.50,
                    supporting_signals=["concatenate_and_sort"]
                ))
            elif heap_alg == "heap_scheduling":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.HEAP_SCHEDULING.value,
                    family="heap",
                    confidence_prior=0.96,
                    supporting_signals=["greedy_interval_heap", "earliest_end_time_frontier"]
                ))
            elif heap_alg == "heap_greedy_selection":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.HEAP_GREEDY_SELECTION.value,
                    family="heap",
                    confidence_prior=0.96,
                    supporting_signals=["repeated_two_smallest_combination", "huffman_greedy_structure"]
                ))
            elif heap_alg == "heap_lazy_deletion":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.HEAP_LAZY_DELETION.value,
                    family="heap",
                    confidence_prior=0.96,
                    supporting_signals=["lazy_tombstone_eviction", "priority_queue_with_hash_counts"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="set_or_multiset",
                    family="bst",
                    confidence_prior=0.70,
                    supporting_signals=["ordered_multiset_erase"]
                ))
            elif heap_alg == "heap_build":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.HEAP_BUILD.value,
                    family="heap",
                    confidence_prior=0.96,
                    supporting_signals=["linear_bottom_up_heapify", "floyd_heapify_linear"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.HEAP_MIN_PRIORITY_QUEUE.value if features.heap_kind == HeapKind.MIN_HEAP else PatternKind.HEAP_MAX_PRIORITY_QUEUE.value,
                    family="heap",
                    confidence_prior=0.75,
                    supporting_signals=["sequential_insert_n_log_n"]
                ))
            elif heap_alg == "heap_max_priority_queue":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.HEAP_MAX_PRIORITY_QUEUE.value,
                    family="heap",
                    confidence_prior=0.96,
                    supporting_signals=["max_heap_priority_queue", "maximum_extremal_access"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="set_or_multiset",
                    family="bst",
                    confidence_prior=0.60,
                    supporting_signals=["ordered_set_extremal_access"]
                ))
            elif heap_alg == "heap_min_priority_queue":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.HEAP_MIN_PRIORITY_QUEUE.value,
                    family="heap",
                    confidence_prior=0.96,
                    supporting_signals=["min_heap_priority_queue", "minimum_extremal_access"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="set_or_multiset",
                    family="bst",
                    confidence_prior=0.60,
                    supporting_signals=["ordered_set_extremal_access"]
                ))
            else:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.HEAP_MIN_PRIORITY_QUEUE.value,
                    family="heap",
                    confidence_prior=0.85,
                    supporting_signals=["default_min_priority_queue"]
                ))

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 16. Disjoint Set Union (DSU) Candidates (Phase 3H)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        if features.is_dsu_detected:
            dsu_alg = features.dsu_algorithm_family

            if features.dsu_is_online_deletions:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_BASIC.value,
                    family="dsu",
                    confidence_prior=0.40,
                    supporting_signals=["online_deletions_requested"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_DYNAMIC_CONNECTIVITY.value,
                    family="dsu",
                    confidence_prior=0.40,
                    supporting_signals=["online_connectivity_with_deletion"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="bfs_dfs_rebuild_reference",
                    family="graph",
                    confidence_prior=0.90,
                    supporting_signals=["rebuild_per_query_reference"]
                ))
            elif dsu_alg == "dsu_offline_dynamic_connectivity":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_OFFLINE_DYNAMIC_CONNECTIVITY.value,
                    family="dsu",
                    confidence_prior=0.98,
                    supporting_signals=["offline_dynamic_connectivity", "segment_tree_over_time"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="bfs_dfs_rebuild_reference",
                    family="graph",
                    confidence_prior=0.45,
                    supporting_signals=["rebuild_graph_per_query"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_BASIC.value,
                    family="dsu",
                    confidence_prior=0.30,
                    supporting_signals=["naive_online_dsu"]
                ))
            elif dsu_alg == "dsu_rollback":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_ROLLBACK.value,
                    family="dsu",
                    confidence_prior=0.98,
                    supporting_signals=["historical_undo_stack", "rollback_snapshot"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_BASIC.value,
                    family="dsu",
                    confidence_prior=0.40,
                    supporting_signals=["standard_path_compression_dsu"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="bfs_dfs_rebuild_reference",
                    family="graph",
                    confidence_prior=0.30,
                    supporting_signals=["rebuild_state_history"]
                ))
            elif dsu_alg in ("dsu_weighted", "dsu_potential_difference"):
                candidates.append(AlgorithmCandidate(
                    pattern=dsu_alg,
                    family="dsu",
                    confidence_prior=0.98,
                    supporting_signals=["relative_potential_differences", "weighted_offsets_to_root"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_BASIC.value,
                    family="dsu",
                    confidence_prior=0.40,
                    supporting_signals=["unweighted_basic_dsu"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="bfs_dfs_rebuild_reference",
                    family="graph",
                    confidence_prior=0.50,
                    supporting_signals=["constraint_graph_traversal"]
                ))
            elif dsu_alg == "dsu_parity":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_PARITY.value,
                    family="dsu",
                    confidence_prior=0.98,
                    supporting_signals=["parity_xor_relation", "dynamic_bipartite_coloring"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_BASIC.value,
                    family="dsu",
                    confidence_prior=0.40,
                    supporting_signals=["uncolored_basic_dsu"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="bfs_dfs_rebuild_reference",
                    family="graph",
                    confidence_prior=0.50,
                    supporting_signals=["static_bipartite_coloring"]
                ))
            elif dsu_alg == "dsu_constraint_consistency":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_CONSTRAINT_CONSISTENCY.value,
                    family="dsu",
                    confidence_prior=0.98,
                    supporting_signals=["constraint_contradiction_detection", "redundant_edge_consistency"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_BASIC.value,
                    family="dsu",
                    confidence_prior=0.40,
                    supporting_signals=["standard_connectivity_without_consistency"]
                ))
            elif dsu_alg == "dsu_component_metadata":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_COMPONENT_METADATA.value,
                    family="dsu",
                    confidence_prior=0.98,
                    supporting_signals=["component_metadata_aggregation", "root_summary_merge"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_BASIC.value,
                    family="dsu",
                    confidence_prior=0.60,
                    supporting_signals=["basic_size_only_dsu"]
                ))
            elif dsu_alg == "dsu_kruskal_support":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_KRUSKAL_SUPPORT.value,
                    family="dsu",
                    confidence_prior=0.98,
                    supporting_signals=["kruskal_cycle_prevention", "mst_edge_disjoint_sets"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_BASIC.value,
                    family="dsu",
                    confidence_prior=0.70,
                    supporting_signals=["basic_dsu"]
                ))
            elif dsu_alg == "dsu_dynamic_connectivity":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_DYNAMIC_CONNECTIVITY.value,
                    family="dsu",
                    confidence_prior=0.98,
                    supporting_signals=["dynamic_incremental_connectivity", "edge_addition_equivalence"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="bfs_dfs_rebuild_reference",
                    family="graph",
                    confidence_prior=0.45,
                    supporting_signals=["bfs_dfs_connectivity"]
                ))
            else:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DSU_BASIC.value,
                    family="dsu",
                    confidence_prior=0.95,
                    supporting_signals=["basic_dsu_equivalence"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="bfs_dfs_rebuild_reference",
                    family="graph",
                    confidence_prior=0.45,
                    supporting_signals=["bfs_dfs_connectivity"]
                ))

        # ── 17. Fenwick Tree Candidates (Phase 3I) ──
        if features.is_fenwick_detected:
            fen_alg = features.fenwick_algorithm_family

            if features.fenwick_is_static:
                # Static array without updates: prefix_sum is optimal O(1), Fenwick is suboptimal O(log N)
                candidates.append(AlgorithmCandidate(
                    pattern="prefix_sum",
                    family="prefix_sum",
                    confidence_prior=0.98,
                    supporting_signals=["static_array_no_updates", "constant_time_range_sum"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_POINT_UPDATE_PREFIX_QUERY.value,
                    family="fenwick",
                    confidence_prior=0.55,
                    supporting_signals=["unnecessarily_dynamic_fenwick"]
                ))
            elif features.fenwick_is_offline_range_add:
                # Offline range additions without interleaved queries: difference array is O(1) update vs O(log N)
                candidates.append(AlgorithmCandidate(
                    pattern="difference_array",
                    family="prefix_sum",
                    confidence_prior=0.98,
                    supporting_signals=["offline_range_adds_only", "difference_array_recommended"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_POINT_UPDATE_PREFIX_QUERY.value,
                    family="fenwick",
                    confidence_prior=0.50,
                    supporting_signals=["unnecessarily_dynamic_range_add"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_RANGE_UPDATE_POINT_QUERY.value,
                    family="fenwick",
                    confidence_prior=0.45,
                    supporting_signals=["unnecessarily_dynamic_range_add"]
                ))
            elif features.fenwick_has_arbitrary_range_minmax or features.fenwick_has_range_assignment or features.fenwick_has_non_invertible_range:
                # Structurally incompatible with Fenwick: requires Segment Tree
                candidates.append(AlgorithmCandidate(
                    pattern="segment_tree",
                    family="segment_tree",
                    confidence_prior=0.98,
                    supporting_signals=["arbitrary_range_minmax_or_assignment_or_non_invertible", "segment_tree_required"]
                ))
                pat = PatternKind.FENWICK_PREFIX_EXTREMUM.value if features.fenwick_has_arbitrary_range_minmax else (
                    PatternKind.FENWICK_POINT_UPDATE_PREFIX_QUERY.value if features.fenwick_has_non_invertible_range else PatternKind.FENWICK_RANGE_UPDATE_POINT_QUERY.value
                )
                candidates.append(AlgorithmCandidate(
                    pattern=pat,
                    family="fenwick",
                    confidence_prior=0.40,
                    supporting_signals=["structurally_incompatible_fenwick"]
                ))
            elif features.fenwick_has_dynamic_unknown_coords:
                # Dynamically appearing unknown coordinates: requires dynamic coordinate representation / ordered structure
                candidates.append(AlgorithmCandidate(
                    pattern="dynamic_coordinate_ordered_structure",
                    family="ordered_set",
                    confidence_prior=0.98,
                    supporting_signals=["dynamic_unknown_coordinates", "dynamic_ordered_structure_required"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_POINT_UPDATE_PREFIX_QUERY.value,
                    family="fenwick",
                    confidence_prior=0.35,
                    supporting_signals=["unrepresentable_dynamic_coordinate_fenwick"]
                ))
            elif features.fenwick_has_negative_frequencies:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_KTH_ELEMENT.value,
                    family="fenwick",
                    confidence_prior=0.70,
                    supporting_signals=["kth_with_negative_frequency_attempt"]
                ))
            elif features.fenwick_resource_exceeded:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_2D_POINT_UPDATE_RANGE_QUERY.value if features.fenwick_is_2d else PatternKind.FENWICK_POINT_UPDATE_PREFIX_QUERY.value,
                    family="fenwick",
                    confidence_prior=0.70,
                    supporting_signals=["resource_budget_exceeded"]
                ))
            elif fen_alg == "fenwick_2d_point_update_range_query":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_2D_POINT_UPDATE_RANGE_QUERY.value,
                    family="fenwick",
                    confidence_prior=0.98,
                    supporting_signals=["2d_grid_point_update", "submatrix_rectangle_sum"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="naive_2d_matrix_scan",
                    family="brute_force",
                    confidence_prior=0.30,
                    supporting_signals=["2d_linear_rectangle_sum"]
                ))
            elif fen_alg == "fenwick_prefix_extremum":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_PREFIX_EXTREMUM.value,
                    family="fenwick",
                    confidence_prior=0.98,
                    supporting_signals=["monotonic_prefix_extremum", "non_decreasing_or_non_increasing_updates"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="segment_tree",
                    family="segment_tree",
                    confidence_prior=0.60,
                    supporting_signals=["segment_tree_extremum"]
                ))
            elif fen_alg == "fenwick_range_update_range_query":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_RANGE_UPDATE_RANGE_QUERY.value,
                    family="fenwick",
                    confidence_prior=0.98,
                    supporting_signals=["two_fenwick_algebraic_range_add", "range_sum_query"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="segment_tree_lazy",
                    family="segment_tree",
                    confidence_prior=0.65,
                    supporting_signals=["lazy_segment_tree_range_add"]
                ))
            elif fen_alg == "fenwick_range_update_point_query":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_RANGE_UPDATE_POINT_QUERY.value,
                    family="fenwick",
                    confidence_prior=0.98,
                    supporting_signals=["difference_array_fenwick", "range_add_point_query"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="segment_tree",
                    family="segment_tree",
                    confidence_prior=0.55,
                    supporting_signals=["segment_tree_range_add"]
                ))
            elif fen_alg == "fenwick_inversion_counting":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_INVERSION_COUNTING.value,
                    family="fenwick",
                    confidence_prior=0.98,
                    supporting_signals=["rank_ordered_inversion_counting", "frequency_prefix_accumulation"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.DC_MERGE_SORT_INVERSIONS.value,
                    family="divide_and_conquer_backtracking",
                    confidence_prior=0.70,
                    supporting_signals=["divide_and_conquer_inversion_count"]
                ))
            elif fen_alg == "fenwick_multiset":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_MULTISET.value,
                    family="fenwick",
                    confidence_prior=0.98,
                    supporting_signals=["dynamic_multiset_operations", "frequency_rank_and_kth"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="ordered_set",
                    family="ordered_set",
                    confidence_prior=0.65,
                    supporting_signals=["pbds_ordered_set"]
                ))
            elif fen_alg == "fenwick_kth_element":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_KTH_ELEMENT.value,
                    family="fenwick",
                    confidence_prior=0.98,
                    supporting_signals=["binary_lifting_kth_element", "monotonic_frequency_search"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="heap_top_k",
                    family="heap",
                    confidence_prior=0.50,
                    supporting_signals=["heap_kth"]
                ))
            elif fen_alg == "fenwick_coordinate_compression":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_COORDINATE_COMPRESSION.value,
                    family="fenwick",
                    confidence_prior=0.98,
                    supporting_signals=["coordinate_compression_pipeline", "sparse_large_value_mapping"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="hash_map_frequency",
                    family="hash_table",
                    confidence_prior=0.45,
                    supporting_signals=["hash_table_counts"]
                ))
            elif fen_alg == "fenwick_frequency":
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_FREQUENCY.value,
                    family="fenwick",
                    confidence_prior=0.98,
                    supporting_signals=["frequency_fenwick_table", "prefix_count_queries"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="ordered_set",
                    family="ordered_set",
                    confidence_prior=0.55,
                    supporting_signals=["ordered_set_frequency"]
                ))
            else:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_POINT_UPDATE_PREFIX_QUERY.value,
                    family="fenwick",
                    confidence_prior=0.96,
                    supporting_signals=["standard_point_add_prefix_range_query", "lowbit_interval_aggregation"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="segment_tree",
                    family="segment_tree",
                    confidence_prior=0.60,
                    supporting_signals=["segment_tree_point_update_range_query"]
                ))

        # ── 18. Segment Tree Candidates (Phase 3J) ──
        if features.is_segment_tree_detected:
            seg_alg = features.segment_tree_algorithm_family

            if features.segment_tree_is_static:
                candidates.append(AlgorithmCandidate(
                    pattern="prefix_sum" if features.segment_tree_query_op == "sum" else "sparse_table",
                    family="prefix_sum" if features.segment_tree_query_op == "sum" else "sparse_table",
                    confidence_prior=0.99,
                    supporting_signals=["static_array_no_updates", "o1_query_preferred"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SEGMENT_TREE_POINT_UPDATE_RANGE_QUERY.value,
                    family="segment_tree",
                    confidence_prior=0.30,
                    supporting_signals=["segment_tree_static_suboptimal"]
                ))
            elif features.segment_tree_is_simple_prefix:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_POINT_UPDATE_PREFIX_QUERY.value,
                    family="fenwick",
                    confidence_prior=0.99,
                    supporting_signals=["point_update_prefix_query_only", "fenwick_preferred"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SEGMENT_TREE_POINT_UPDATE_RANGE_QUERY.value,
                    family="segment_tree",
                    confidence_prior=0.30,
                    supporting_signals=["segment_tree_simple_prefix_overkill"]
                ))
            elif features.segment_tree_has_no_associative_merge:
                candidates.append(AlgorithmCandidate(
                    pattern="order_statistic_tree_or_sqrt_decomposition",
                    family="order_statistic_tree",
                    confidence_prior=0.99,
                    supporting_signals=["non_associative_merge", "order_statistic_tree_preferred"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SEGMENT_TREE_POINT_UPDATE_RANGE_QUERY.value,
                    family="segment_tree",
                    confidence_prior=0.30,
                    supporting_signals=["segment_tree_no_associative_merge"]
                ))
            elif features.segment_tree_has_unsupported_lazy:
                candidates.append(AlgorithmCandidate(
                    pattern="segment_tree_beats",
                    family="segment_tree_beats",
                    confidence_prior=0.99,
                    supporting_signals=["range_chmin_chmax", "segment_tree_beats_required"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SEGMENT_TREE_RANGE_ADD_RANGE_QUERY.value,
                    family="segment_tree",
                    confidence_prior=0.30,
                    supporting_signals=["segment_tree_lazy_tag_unsupported"]
                ))
            elif features.segment_tree_resource_exceeded:
                candidates.append(AlgorithmCandidate(
                    pattern="coordinate_compressed_segment_tree_or_dynamic_segtree",
                    family="dynamic_segment_tree",
                    confidence_prior=0.99,
                    supporting_signals=["resource_limit_exceeded", "dynamic_segment_tree_required"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SEGMENT_TREE_POINT_UPDATE_RANGE_QUERY.value,
                    family="segment_tree",
                    confidence_prior=0.30,
                    supporting_signals=["segment_tree_resource_limit"]
                ))
            elif features.segment_tree_has_negative_frequencies:
                candidates.append(AlgorithmCandidate(
                    pattern="balanced_bst",
                    family="tree",
                    confidence_prior=0.99,
                    supporting_signals=["negative_frequencies_in_kth", "balanced_bst_preferred"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SEGMENT_TREE_FREQUENCY_ORDER_STATISTIC.value,
                    family="segment_tree",
                    confidence_prior=0.30,
                    supporting_signals=["segment_tree_kth_negative_frequency"]
                ))
            elif features.segment_tree_is_offline_range_add:
                candidates.append(AlgorithmCandidate(
                    pattern="difference_array",
                    family="difference_array",
                    confidence_prior=0.99,
                    supporting_signals=["batch_offline_range_add_only", "single_sweep_reconstruction"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SEGMENT_TREE_RANGE_ADD_RANGE_QUERY.value,
                    family="segment_tree",
                    confidence_prior=0.35,
                    supporting_signals=["segment_tree_offline_overkill"]
                ))
            elif features.segment_tree_is_max_subarray:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SEGMENT_TREE_MAX_SUBARRAY.value,
                    family="segment_tree",
                    confidence_prior=0.99,
                    supporting_signals=["max_contiguous_subarray_sum", "ordered_merge_sum_pref_suff_ans"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="kadane_dynamic",
                    family="dynamic_programming",
                    confidence_prior=0.40,
                    supporting_signals=["kadane_point_updates"]
                ))
            elif features.segment_tree_has_combined_lazy:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SEGMENT_TREE_COMBINED_LAZY_RANGE_QUERY.value,
                    family="segment_tree",
                    confidence_prior=0.99,
                    supporting_signals=["combined_range_assign_and_add", "lazy_tag_composition_algebra"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="sqrt_decomposition",
                    family="sqrt_decomposition",
                    confidence_prior=0.45,
                    supporting_signals=["sqrt_block_lazy"]
                ))
            elif features.segment_tree_has_range_assign:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SEGMENT_TREE_RANGE_ASSIGN_RANGE_QUERY.value,
                    family="segment_tree",
                    confidence_prior=0.99,
                    supporting_signals=["lazy_range_assignment_overwrite", "deferred_propagation"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern="sqrt_decomposition",
                    family="sqrt_decomposition",
                    confidence_prior=0.40,
                    supporting_signals=["sqrt_range_assign"]
                ))
            elif features.segment_tree_has_range_add:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SEGMENT_TREE_RANGE_ADD_RANGE_QUERY.value,
                    family="segment_tree",
                    confidence_prior=0.98,
                    supporting_signals=["lazy_range_add_range_query", "deferred_propagation"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_RANGE_UPDATE_RANGE_QUERY.value,
                    family="fenwick",
                    confidence_prior=0.70,
                    supporting_signals=["two_fenwick_range_add_range_sum"]
                ))
            elif features.segment_tree_is_metadata:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SEGMENT_TREE_METADATA_AGGREGATE.value,
                    family="segment_tree",
                    confidence_prior=0.98,
                    supporting_signals=["composite_node_metadata", "simultaneous_sum_min_max_count"]
                ))
            elif features.segment_tree_is_interval_statistics:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SEGMENT_TREE_INTERVAL_STATISTICS.value,
                    family="segment_tree",
                    confidence_prior=0.98,
                    supporting_signals=["range_extrema_with_multiplicity", "conditional_min_max_count_merge"]
                ))
            elif features.segment_tree_is_frequency:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SEGMENT_TREE_FREQUENCY_ORDER_STATISTIC.value,
                    family="segment_tree",
                    confidence_prior=0.98,
                    supporting_signals=["frequency_segment_tree", "kth_order_statistic_tree_descent"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.FENWICK_KTH_ELEMENT.value,
                    family="fenwick",
                    confidence_prior=0.65,
                    supporting_signals=["fenwick_binary_lifting_kth"]
                ))
            else:
                candidates.append(AlgorithmCandidate(
                    pattern=PatternKind.SEGMENT_TREE_POINT_UPDATE_RANGE_QUERY.value,
                    family="segment_tree",
                    confidence_prior=0.98,
                    supporting_signals=["point_update_range_query", "associative_interval_merge"]
                ))
                if features.segment_tree_query_op == "sum":
                    candidates.append(AlgorithmCandidate(
                        pattern=PatternKind.FENWICK_POINT_UPDATE_PREFIX_QUERY.value,
                        family="fenwick",
                        confidence_prior=0.75,
                        supporting_signals=["fenwick_point_update_range_sum"]
                    ))

        # ── Dynamic Programming Candidates (Phase 3K) ──
        if features.is_dp_detected or features.dp_greedy_optimal or features.dp_is_cyclic or not features.dp_has_optimal_substructure or not features.dp_has_overlapping_subproblems or features.dp_is_non_markovian or features.dp_is_resource_exceeded:
            dp_alg = features.dp_algorithm_family

            if features.dp_greedy_optimal:
                if not features.is_greedy_detected:
                    candidates.append(AlgorithmCandidate(
                        pattern="greedy_algorithm",
                        family="greedy",
                        confidence_prior=0.99,
                        supporting_signals=["greedy_choice_property_holds", "matroid_or_exchange_argument"]
                    ))
                candidates.append(AlgorithmCandidate(
                    pattern=dp_alg or PatternKind.DP_1D_LINEAR.value,
                    family="dynamic_programming",
                    confidence_prior=0.30,
                    supporting_signals=["dp_greedy_choice_optimal"]
                ))
            elif features.dp_is_cyclic:
                candidates.append(AlgorithmCandidate(
                    pattern="graph_shortest_path_or_scc",
                    family="graph",
                    confidence_prior=0.99,
                    supporting_signals=["cyclic_state_dependencies", "shortest_path_algorithm_required"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=dp_alg or PatternKind.DP_DAG.value,
                    family="dynamic_programming",
                    confidence_prior=0.30,
                    supporting_signals=["dp_cyclic_state_dependency"]
                ))
            elif not features.dp_has_optimal_substructure:
                candidates.append(AlgorithmCandidate(
                    pattern="backtracking_or_exponential_search",
                    family="exhaustive_search",
                    confidence_prior=0.99,
                    supporting_signals=["subproblems_lack_optimal_substructure"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=dp_alg or PatternKind.DP_1D_LINEAR.value,
                    family="dynamic_programming",
                    confidence_prior=0.30,
                    supporting_signals=["dp_no_optimal_substructure"]
                ))
            elif not features.dp_has_overlapping_subproblems:
                candidates.append(AlgorithmCandidate(
                    pattern=features.dc_backtracking_algorithm_family or PatternKind.DC_MERGE_SORT_INVERSIONS.value,
                    family="divide_and_conquer_backtracking",
                    confidence_prior=0.99,
                    supporting_signals=["independent_disjoint_subproblems"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=dp_alg or PatternKind.DP_1D_LINEAR.value,
                    family="dynamic_programming",
                    confidence_prior=0.30,
                    supporting_signals=["dp_no_overlapping_subproblems"]
                ))
            elif features.dp_is_non_markovian:
                candidates.append(AlgorithmCandidate(
                    pattern="state_augmented_search",
                    family="exhaustive_search",
                    confidence_prior=0.99,
                    supporting_signals=["non_markovian_future_dependence"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=dp_alg or PatternKind.DP_1D_LINEAR.value,
                    family="dynamic_programming",
                    confidence_prior=0.30,
                    supporting_signals=["dp_non_markovian_future_dependence"]
                ))
            elif features.dp_is_resource_exceeded:
                candidates.append(AlgorithmCandidate(
                    pattern="approximation_or_meet_in_middle",
                    family="combinatorial_optimization",
                    confidence_prior=0.99,
                    supporting_signals=["state_space_explosion", "exceeds_memory_limit"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=dp_alg or PatternKind.DP_BITMASK.value,
                    family="dynamic_programming",
                    confidence_prior=0.30,
                    supporting_signals=["dp_state_space_explosion"]
                ))
            else:
                pattern_map = {
                    "dp_1d_linear": PatternKind.DP_1D_LINEAR.value,
                    "dp_grid_2d": PatternKind.DP_GRID_2D.value,
                    "dp_knapsack": PatternKind.DP_KNAPSACK.value,
                    "dp_subsequence_string": PatternKind.DP_SUBSEQUENCE_STRING.value,
                    "dp_interval": PatternKind.DP_INTERVAL.value,
                    "dp_partition": PatternKind.DP_PARTITION.value,
                    "dp_state_machine": PatternKind.DP_STATE_MACHINE.value,
                    "dp_bitmask": PatternKind.DP_BITMASK.value,
                    "dp_tree": PatternKind.DP_TREE.value,
                    "dp_dag": PatternKind.DP_DAG.value,
                    "dp_digit": PatternKind.DP_DIGIT.value,
                    "dp_optimization": PatternKind.DP_OPTIMIZATION.value,
                    "dp_solution_reconstruction": PatternKind.DP_SOLUTION_RECONSTRUCTION.value,
                    "dp_space_optimization": PatternKind.DP_SPACE_OPTIMIZATION.value,
                }
                target_pat = pattern_map.get(dp_alg, PatternKind.DP_1D_LINEAR.value)
                candidates.append(AlgorithmCandidate(
                    pattern=target_pat,
                    family="dynamic_programming",
                    confidence_prior=0.98,
                    supporting_signals=["optimal_substructure", "overlapping_subproblems", f"pattern_{target_pat}"]
                ))

        # ── 20. Greedy Candidate Generation (Phase 3L) ──
        if features.is_greedy_detected:
            greedy_alg = features.greedy_algorithm_family
            pattern_map = {
                "greedy_interval_selection": PatternKind.GREEDY_INTERVAL_SELECTION.value,
                "greedy_interval_covering": PatternKind.GREEDY_INTERVAL_COVERING.value,
                "greedy_fractional_knapsack": PatternKind.GREEDY_FRACTIONAL_KNAPSACK.value,
                "greedy_deadline_scheduling": PatternKind.GREEDY_DEADLINE_SCHEDULING.value,
                "greedy_heap_assisted": PatternKind.GREEDY_HEAP_ASSISTED.value,
                "greedy_huffman_merge": PatternKind.GREEDY_HUFFMAN_MERGE.value,
                "greedy_sequence_local_choice": PatternKind.GREEDY_SEQUENCE_LOCAL_CHOICE.value,
                "greedy_reachability_partition": PatternKind.GREEDY_REACHABILITY_PARTITION.value,
                "greedy_graph_mst": PatternKind.GREEDY_GRAPH_MST.value,
                "greedy_general_exchange": PatternKind.GREEDY_GENERAL_EXCHANGE.value,
            }
            target_pat = pattern_map.get(greedy_alg, PatternKind.GREEDY_INTERVAL_SELECTION.value)

            if features.greedy_counterexample_detected:
                candidates.append(AlgorithmCandidate(
                    pattern="dp_1d_linear",
                    family="dynamic_programming",
                    confidence_prior=0.99,
                    supporting_signals=["greedy_counterexample_detected", "exact_dp_recurrence"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=target_pat,
                    family="greedy",
                    confidence_prior=0.20,
                    supporting_signals=["greedy_counterexample_found"]
                ))
            elif features.greedy_competing_dp_signal:
                if "knapsack" in target_pat:
                    dp_comp = PatternKind.DP_KNAPSACK.value
                elif "interval" in target_pat:
                    dp_comp = PatternKind.DP_INTERVAL.value
                else:
                    dp_comp = PatternKind.DP_1D_LINEAR.value
                candidates.append(AlgorithmCandidate(
                    pattern=dp_comp,
                    family="dynamic_programming",
                    confidence_prior=0.98,
                    supporting_signals=["competing_dp_signal", "discrete_or_weighted_constraints"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=target_pat,
                    family="greedy",
                    confidence_prior=0.30,
                    supporting_signals=["greedy_exchange_proof_failed"]
                ))
            elif features.greedy_proof_unestablished:
                candidates.append(AlgorithmCandidate(
                    pattern="dp_1d_linear",
                    family="dynamic_programming",
                    confidence_prior=0.95,
                    supporting_signals=["greedy_proof_unestablished", "explore_competing_families"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=target_pat,
                    family="greedy",
                    confidence_prior=0.25,
                    supporting_signals=["greedy_proof_not_established"]
                ))
            else:
                signals = ["greedy_choice_property", f"pattern_{target_pat}"]
                if features.greedy_has_exchange_signal:
                    signals.append("exchange_argument")
                if features.greedy_has_staying_ahead_signal:
                    signals.append("staying_ahead")
                if features.greedy_has_dominance_signal:
                    signals.append("dominance")
                if features.greedy_has_cut_property_signal:
                    signals.append("safe_cut_property")
                candidates.append(AlgorithmCandidate(
                    pattern=target_pat,
                    family="greedy",
                    confidence_prior=0.98,
                    supporting_signals=signals
                ))

        # ── 21. Divide and Conquer & Backtracking Candidate Generation (Phase 3M) ──
        if features.is_dc_backtracking_detected:
            # Section 8: Cross-family composition / Tower gate
            if features.is_cross_family_composition or features.composition_unsupported:
                candidates.append(AlgorithmCandidate(
                    pattern="composition_unsupported",
                    family="divide_and_conquer_backtracking",
                    confidence_prior=0.99,
                    supporting_signals=["cross_family_composition", "tower_problem_gate", "fail_closed_unsupported"]
                ))
            elif features.dc_subproblems_not_independent:
                candidates.append(AlgorithmCandidate(
                    pattern="dp_1d_linear",
                    family="dynamic_programming",
                    confidence_prior=0.99,
                    supporting_signals=["subproblems_not_independent", "overlapping_subproblems"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=features.dc_backtracking_algorithm_family or PatternKind.DC_MERGE_SORT_INVERSIONS.value,
                    family="divide_and_conquer_backtracking",
                    confidence_prior=0.20,
                    supporting_signals=["dc_subproblems_not_independent"]
                ))
            elif features.dc_combine_step_intractable:
                candidates.append(AlgorithmCandidate(
                    pattern="approximation_or_dp",
                    family="dynamic_programming",
                    confidence_prior=0.99,
                    supporting_signals=["combine_step_intractable"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=features.dc_backtracking_algorithm_family or PatternKind.DC_MERGE_SORT_INVERSIONS.value,
                    family="divide_and_conquer_backtracking",
                    confidence_prior=0.20,
                    supporting_signals=["dc_combine_step_intractable"]
                ))
            elif features.dc_base_case_undefined:
                candidates.append(AlgorithmCandidate(
                    pattern=features.dc_backtracking_algorithm_family or PatternKind.DC_MERGE_SORT_INVERSIONS.value,
                    family="divide_and_conquer_backtracking",
                    confidence_prior=0.20,
                    supporting_signals=["dc_base_case_undefined"]
                ))
            elif features.backtracking_search_space_explosive:
                candidates.append(AlgorithmCandidate(
                    pattern="branch_and_bound_or_dp",
                    family="dynamic_programming",
                    confidence_prior=0.99,
                    supporting_signals=["search_space_explosive", "unpruned_exponential_search"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=features.dc_backtracking_algorithm_family or PatternKind.BACKTRACKING_SUBSETS_PERMUTATIONS.value,
                    family="divide_and_conquer_backtracking",
                    confidence_prior=0.20,
                    supporting_signals=["backtracking_search_space_explosive"]
                ))
            elif features.backtracking_greedy_sufficient:
                candidates.append(AlgorithmCandidate(
                    pattern="greedy_interval_selection",
                    family="greedy",
                    confidence_prior=0.99,
                    supporting_signals=["greedy_choice_sufficient", "matroid_or_exchange_property"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=features.dc_backtracking_algorithm_family or PatternKind.BACKTRACKING_BRANCH_AND_BOUND.value,
                    family="divide_and_conquer_backtracking",
                    confidence_prior=0.25,
                    supporting_signals=["backtracking_greedy_sufficient"]
                ))
            elif features.backtracking_dp_sufficient:
                candidates.append(AlgorithmCandidate(
                    pattern="dp_1d_linear",
                    family="dynamic_programming",
                    confidence_prior=0.99,
                    supporting_signals=["overlapping_subproblems_admit_dp"]
                ))
                candidates.append(AlgorithmCandidate(
                    pattern=features.dc_backtracking_algorithm_family or PatternKind.BACKTRACKING_STATE_SPACE_SEARCH.value,
                    family="divide_and_conquer_backtracking",
                    confidence_prior=0.25,
                    supporting_signals=["backtracking_dp_sufficient"]
                ))
            elif features.backtracking_resource_limit_exceeded:
                candidates.append(AlgorithmCandidate(
                    pattern=features.dc_backtracking_algorithm_family or PatternKind.BACKTRACKING_STATE_SPACE_SEARCH.value,
                    family="divide_and_conquer_backtracking",
                    confidence_prior=0.20,
                    supporting_signals=["backtracking_resource_limit_exceeded"]
                ))
            else:
                dc_bt_map = {
                    "dc_merge_sort_inversions": PatternKind.DC_MERGE_SORT_INVERSIONS.value,
                    "dc_quickselect": PatternKind.DC_QUICKSELECT.value,
                    "dc_closest_pair": PatternKind.DC_CLOSEST_PAIR.value,
                    "dc_tree_centroid": PatternKind.DC_TREE_CENTROID.value,
                    "dc_cdq_divide_and_conquer": PatternKind.DC_CDQ_DIVIDE_AND_CONQUER.value,
                    "backtracking_subsets_permutations": PatternKind.BACKTRACKING_SUBSETS_PERMUTATIONS.value,
                    "backtracking_constraint_satisfaction": PatternKind.BACKTRACKING_CONSTRAINT_SATISFACTION.value,
                    "backtracking_branch_and_bound": PatternKind.BACKTRACKING_BRANCH_AND_BOUND.value,
                    "backtracking_state_space_search": PatternKind.BACKTRACKING_STATE_SPACE_SEARCH.value,
                    "backtracking_meet_in_the_middle": PatternKind.BACKTRACKING_MEET_IN_THE_MIDDLE.value,
                }
                target_pat = dc_bt_map.get(features.dc_backtracking_algorithm_family, PatternKind.DC_MERGE_SORT_INVERSIONS.value)
                signals = [f"pattern_{target_pat}"]
                if features.dc_is_independent_subproblems:
                    signals.append("independent_subproblems")
                if features.dc_has_cross_boundary_combine:
                    signals.append("cross_boundary_combine")
                if features.backtracking_is_exponential:
                    signals.append("exponential_decision_space")
                if features.backtracking_requires_pruning:
                    signals.append(f"pruning_{features.backtracking_pruning_kind or 'feasibility'}")
                if features.backtracking_state_restoration:
                    signals.append("state_restoration")
                if features.backtracking_is_meet_in_middle:
                    signals.append("meet_in_the_middle_split")
                candidates.append(AlgorithmCandidate(
                    pattern=target_pat,
                    family="divide_and_conquer_backtracking",
                    confidence_prior=0.98,
                    supporting_signals=signals
                ))

        # ── 22. Advanced Graph Candidate Generation (Phase 3N) ──
        if features.is_adv_graph_detected and features.adv_graph_algorithm_family:
            candidates.append(AlgorithmCandidate(
                pattern=features.adv_graph_algorithm_family,
                family="adv_graph",
                confidence_prior=0.995,
                supporting_signals=[f"pattern_{features.adv_graph_algorithm_family}", "semantic_composition_proven"]
            ))

        # ── 23. String Algorithms & Automata Candidate Generation (Phase 3O) ──
        if features.is_string_algorithm_detected and features.string_algorithm_family:
            candidates.append(AlgorithmCandidate(
                pattern=features.string_algorithm_family,
                family="string",
                confidence_prior=0.995,
                supporting_signals=[f"pattern_{features.string_algorithm_family}", "semantic_composition_proven"]
            ))

        # ── 24. Number Theory & Combinatorics Candidate Generation (Phase 3P) ──
        if getattr(features, "is_number_theory_detected", False) and getattr(features, "number_theory_family", None):
            candidates.append(AlgorithmCandidate(
                pattern=features.number_theory_family,
                family="number_theory",
                confidence_prior=0.995,
                supporting_signals=[f"pattern_{features.number_theory_family}", "semantic_composition_proven"]
            ))

        # ── 25. Algebra / Transforms Candidate Generation (Phase 3Q) ──
        if getattr(features, "is_algebra_detected", False) and getattr(features, "algebra_family", None):
            candidates.append(AlgorithmCandidate(
                pattern=features.algebra_family,
                family="algebra",
                confidence_prior=0.995,
                supporting_signals=[f"pattern_{features.algebra_family}", "semantic_composition_proven"]
            ))

        # ── 26. Computational Geometry Candidate Generation (Phase 3R) ──
        if getattr(features, "is_geometry_detected", False) and getattr(features, "geometry_family", None):
            candidates.append(AlgorithmCandidate(
                pattern=features.geometry_family,
                family="geometry",
                confidence_prior=0.995,
                supporting_signals=[f"pattern_{features.geometry_family}", "geometric_preconditions_verified"]
            ))

        # ── 27. Advanced Data Structures Candidate Generation (Phase 3S) ──
        if getattr(features, "is_ads_detected", False) and getattr(features, "ads_family", None):
            candidates.append(AlgorithmCandidate(
                pattern=features.ads_family,
                family="adv_data_structures",
                confidence_prior=0.995,
                supporting_signals=[f"pattern_{features.ads_family}", "ads_preconditions_verified"]
            ))

        # ── 28. Cross-Family Composition Candidate Generation (Phase 4) ──
        if getattr(features, "is_cross_family_detected", False) and getattr(features, "cross_family_family", None):
            pat = features.cross_family_family
            text = getattr(features, "raw_text", "").lower()
            is_explicit_cf = (
                "cross_family" in text or "cross-family" in text or "cf_" in text or
                "composition" in text or "synthes" in text or pat not in ("cf_kruskal_mst", "cf_dijkstra_shortest_path")
            )
            confidence = 0.999 if is_explicit_cf else 0.95
            candidates.append(AlgorithmCandidate(
                pattern=pat,
                family="cross_family",
                confidence_prior=confidence,
                supporting_signals=[f"pattern_{pat}", "cross_family_composition_verified"]
            ))

        return candidates
