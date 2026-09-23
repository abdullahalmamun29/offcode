"""
Structural Feature Extractor for Pointer-Based Algorithms.

Extracts deep structural properties rather than merely searching keywords:
- Input structure: sequence, pairs of sequences, linked structure, grid
- Output requirement: boolean check, indices, values, length, count, in-place modified array
- Ordering properties: sorted, strictly sorted, unsorted, can sort without losing identity
- Index preservation: does the output require original 1-based or 0-based indices?
- Duplicates: presence, handling requirements (deduplicate, count, preserve)
- Contiguity: contiguous subarray/substring vs general subsequence vs subset
- Optimization objective: maximize area, maximize length, minimize length, minimize cost
- Search objective: find pair, find threshold, count pairs
- Value range: non-negative only, mixed positive/negative, zeroes only, small alphabet
- Mutability: in-place modification permitted vs immutable array
- Allowed preprocessing: sorting permitted vs order must remain intact
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pointer_algorithms.knowledge.taxonomy import (
    SearchSpaceKind, ExactMatchSemantics,
    TrieKind, TrieAlphabetKind, TrieStorageKind,
    TreeKind, TreeRepresentation, TreeTraversalOrder,
    GraphKind, GraphWeightKind, GraphRepresentation as GraphRepr,
    GraphComponentKind, GraphAcyclicityKind, GraphBipartiteKind,
    HeapKind, HeapOperationKind,
    DSUKind, DSUOperationKind,
    FenwickKind, FenwickOperationKind,
    SegmentTreeKind, SegmentTreeOperationKind,
    DPKind, DPOperationKind,
    GreedyKind, GreedyProofKind,
    DCBacktrackingKind, SubproblemDependencyKind, TerminationGuaranteeKind
)

@dataclass
class ProblemFeatures:
    raw_text: str
    input_structure: str  # 'single_sequence', 'two_sequences', 'linked_list', 'grid', 'other', 'tree', 'binary_tree'
    output_requirement: str  # 'pair_values', 'pair_indices', 'max_length', 'min_length', 'boolean', 'modified_array', 'count', 'traversal_list', 'node_value'
    is_sorted: bool
    can_sort: bool
    requires_original_indices: bool
    has_negative_values: bool
    is_contiguous: bool
    tracks_distinct: bool
    optimization_objective: Optional[str]  # 'max_area', 'max_length', 'min_length', 'max_sum', None
    search_objective: Optional[str]  # 'pair_sum', 'pair_diff', 'cycle', 'middle', None
    partition_requirement: Optional[str]  # 'dutch_flag_012', 'two_way_zeroes', 'parity', None
    in_place_required: bool
    has_dynamic_updates: bool
    repeated_queries: bool
    target_value: Optional[str] = None
    window_size_k: Optional[int] = None
    extra_signals: List[str] = field(default_factory=list)

    # ── Monotonic Stack features (Phase 3B) ──
    # True when problem seeks first element satisfying a directional comparison
    nearest_boundary_query: bool = False
    # 'greater' | 'smaller' | None
    boundary_relation: Optional[str] = None
    # 'right' | 'left' | 'both' | None
    boundary_direction: Optional[str] = None
    # 'strict' | 'non_strict' (e.g., > vs >=)
    comparison_strictness: Optional[str] = None
    # True when the sequence wraps around (circular array)
    is_circular: bool = False
    # 'sum_min' | 'sum_max' | 'range_count' | None
    contribution_objective: Optional[str] = None
    # True for "largest rectangle" or "maximal area in histogram" problems
    histogram_pattern: bool = False
    # True for stock-span-style "distance to previous dominant element" queries
    has_stock_span_pattern: bool = False
    # True when input likely has duplicate-heavy data requiring explicit strictness
    has_duplicate_dominance: bool = False

    # ── Binary Search features (Phase 3C) ──
    has_ordered_search_space: bool = False
    is_answer_space_search: bool = False
    search_space_type: Optional[str] = None  # 'indices', 'answer_values', 'numeric_domain'
    target_boundary: Optional[str] = None    # 'exact', 'lower_bound', 'upper_bound', 'first_true', 'last_true', 'first_false', 'last_false', 'predecessor', 'successor'
    predicate_direction: Optional[str] = None  # 'false_to_true', 'true_to_false', 'equality'
    feasibility_objective: Optional[str] = None  # 'minimize_maximum', 'maximize_minimum', 'minimum_feasible', 'maximum_feasible'
    requires_exact_lookup: bool = False
    has_monotonic_predicate: bool = False
    has_non_monotonic_predicate: bool = False
    has_numeric_domain: bool = False
    compound_with: Optional[str] = None  # 'greedy', 'sorting', 'prefix_sum', 'two_pointers'
    search_space_kind: Optional[SearchSpaceKind] = None
    exact_match_semantics: Optional[ExactMatchSemantics] = None
    answer_space_low_expression: Optional[str] = None
    answer_space_high_expression: Optional[str] = None

    # ── Trie features (Phase 3D) ──
    trie_kind: Optional[TrieKind] = None
    prefix_query_type: Optional[str] = None
    trie_alphabet: Optional[TrieAlphabetKind] = None
    trie_storage: Optional[TrieStorageKind] = None
    estimated_node_count: int = 0
    estimated_memory_bytes: int = 0
    memory_limit_bytes: int = 256 * 1024 * 1024
    memory_limit_exceeded: bool = False
    has_single_query_only: bool = False
    has_prefix_sharing_advantage: bool = False

    # ── Tree features (Phase 3E) ──
    tree_kind: Optional[TreeKind] = None
    tree_representation: Optional[TreeRepresentation] = None
    tree_traversal_order: Optional[TreeTraversalOrder] = None
    tree_aggregation_op: Optional[str] = None
    is_bst: bool = False
    is_validating_bst: bool = False
    bst_duplicate_policy: Optional[str] = None  # 'strictly_less', 'allow_duplicates_left', 'allow_duplicates_right', 'count_in_node'
    lca_query_type: Optional[str] = None        # 'binary_tree', 'bst', 'parent_array'
    tree_dp_type: Optional[str] = None          # 'independent_set', 'subtree_weight', 'two_state'
    is_diameter_query: bool = False
    is_path_sum_query: bool = False
    tree_node_count_n: int = 1000
    tree_max_depth_estimate: Optional[str] = None  # 'balanced_log_n', 'skewed_n'
    tree_recursion_risk: bool = False
    is_guaranteed_tree: bool = False
    graph_edge_count_e: Optional[int] = None
    has_cycle_signal: bool = False
    is_disconnected_signal: bool = False

    # ── Graph features (Phase 3F) ──
    # None means UNKNOWN (not assumed false)
    graph_kind: Optional[GraphKind] = None               # DIRECTED | UNDIRECTED | None=UNKNOWN
    graph_weight_kind: Optional[GraphWeightKind] = None  # UNWEIGHTED | NON_NEGATIVE_WEIGHTED | NEGATIVE_WEIGHTED
    graph_representation: Optional[GraphRepr] = None     # ADJACENCY_LIST | ADJACENCY_MATRIX | EDGE_LIST
    graph_has_negative_weights: bool = False
    graph_has_negative_cycles: bool = False              # UNKNOWN unless explicitly stated
    graph_is_directed: bool = False
    graph_is_weighted: bool = False
    graph_is_cyclic: Optional[bool] = None               # None = UNKNOWN
    graph_is_dag: Optional[bool] = None                  # None = UNKNOWN
    graph_is_bipartite: Optional[bool] = None            # None = UNKNOWN
    graph_is_disconnected: Optional[bool] = None         # None = UNKNOWN
    graph_vertex_count_v: int = 1000
    graph_index_base: Optional[int] = None               # 0 or 1 if explicitly established, else UNKNOWN (None)
    computational_budget: float = 1.0e8                  # standard 1s CPU operations budget (~10^8)
    graph_query_type: Optional[str] = None               # 'shortest_path'|'reachability'|'components'|'cycle'|'bipartite'|'topological'|'dag_dp'|'mst'|'dsu'|'scc'|'bridges_articulation'
    graph_algorithm_family: Optional[str] = None         # inferred family
    is_graph_detected: bool = False
    # Heap attributes (Phase 3G)
    is_heap_detected: bool = False
    heap_kind: Optional[HeapKind] = None
    heap_operation_kind: Optional[HeapOperationKind] = None
    heap_k_direction: Optional[str] = None              # 'largest' | 'smallest' | None
    heap_k_value: Optional[int] = None                  # K value if bounded top-k / k-th
    heap_is_streaming: bool = False                     # dynamic stream / online queries
    heap_is_dynamic_median: bool = False                # dual-frontier / dynamic median
    heap_is_k_way_merge: bool = False                   # k-way merge of sorted streams
    heap_is_scheduling: bool = False                    # interval / task / cpu scheduling
    heap_is_greedy_selection: bool = False              # Huffman / connect ropes / greedy minimum sum
    heap_is_lazy_deletion: bool = False                 # lazy deletion with frequency / tombstone
    heap_requires_arbitrary_delete: bool = False        # arbitrary deletion by value (anti-pattern for standard heap)
    heap_requires_full_sort: bool = False               # entire array needs total sort
    heap_is_offline_kth: bool = False                   # static offline array K-th element (quickselect competitor)
    heap_algorithm_family: Optional[str] = None         # inferred pattern name
    # DSU attributes (Phase 3H)
    is_dsu_detected: bool = False
    dsu_kind: Optional[DSUKind] = None
    dsu_operation_kind: Optional[DSUOperationKind] = None
    dsu_algorithm_family: Optional[str] = None          # inferred pattern name
    dsu_has_metadata: bool = False
    dsu_metadata_type: Optional[str] = None             # 'size' | 'sum' | 'min' | 'max' | 'count' | 'xor'
    dsu_has_weights: bool = False                       # potential differences: value[x] - value[y] = w
    dsu_has_parity: bool = False                        # XOR parity / 2-coloring: color[x] ^ color[y] = p
    dsu_requires_rollback: bool = False                 # undo / snapshot / rollback
    dsu_is_offline: bool = False                        # offline dynamic connectivity
    dsu_has_deletions: bool = False                     # edge deletions present in problem
    dsu_is_online_deletions: bool = False               # interactive/online edge deletions (anti-pattern)
    dsu_has_difference_query: bool = False              # query difference between elements
    dsu_has_contradiction_check: bool = False           # verify consistency / detect contradiction
    dsu_historical_queries: bool = False                # query state at historical snapshot
    # Fenwick Tree attributes (Phase 3I)
    is_fenwick_detected: bool = False
    fenwick_kind: Optional[FenwickKind] = None
    fenwick_operation_kind: Optional[FenwickOperationKind] = None
    fenwick_algorithm_family: Optional[str] = None      # inferred pattern name
    fenwick_has_point_update: bool = False
    fenwick_has_range_update: bool = False
    fenwick_has_point_query: bool = False
    fenwick_has_prefix_query: bool = False
    fenwick_has_range_query: bool = False
    fenwick_is_frequency: bool = False
    fenwick_has_kth_query: bool = False
    fenwick_requires_coordinate_compression: bool = False
    fenwick_is_inversion_counting: bool = False
    fenwick_is_multiset: bool = False
    fenwick_is_2d: bool = False
    fenwick_is_extremum: bool = False
    fenwick_extremum_direction: Optional[str] = None    # 'min' | 'max'
    fenwick_is_static: bool = False                     # static array, no updates (suboptimal)
    fenwick_is_offline_range_add: bool = False          # offline batch range adds with only final queries
    fenwick_has_range_assignment: bool = False          # interval assignment (unsupported)
    fenwick_has_arbitrary_range_minmax: bool = False    # arbitrary range min/max with replacement (unsupported)
    fenwick_has_dynamic_unknown_coords: bool = False    # unbounded dynamic streaming unknown coordinates
    fenwick_has_negative_frequencies: bool = False      # negative frequencies for kth element
    fenwick_resource_exceeded: bool = False             # time or memory budget exceeded
    fenwick_has_non_invertible_range: bool = False      # non-invertible range query

    @property
    def fenwick_has_updates(self) -> bool:
        return self.fenwick_has_point_update or self.fenwick_has_range_update

    @property
    def fenwick_is_offline_range_add_only(self) -> bool:
        return self.fenwick_is_offline_range_add

    @property
    def fenwick_has_range_extremum_with_arbitrary_point_replacement(self) -> bool:
        return self.fenwick_has_arbitrary_range_minmax

    @property
    def fenwick_has_dynamic_unbounded_coords(self) -> bool:
        return self.fenwick_has_dynamic_unknown_coords

    @property
    def fenwick_has_negative_frequencies_in_kth(self) -> bool:
        return self.fenwick_has_negative_frequencies

    @property
    def fenwick_is_resource_limit_exceeded(self) -> bool:
        return self.fenwick_resource_exceeded

    @property
    def fenwick_is_kth(self) -> bool:
        return self.fenwick_has_kth_query

    @property
    def fenwick_monotonic_extremum(self) -> Optional[str]:
        return self.fenwick_extremum_direction

    # ── 18. Segment Tree Signals (Phase 3J) ──
    is_segment_tree_detected: bool = False
    segment_tree_kind: Optional[SegmentTreeKind] = None
    segment_tree_operation_kind: Optional[SegmentTreeOperationKind] = None
    segment_tree_algorithm_family: Optional[str] = None
    segment_tree_has_point_update: bool = False
    segment_tree_has_range_update: bool = False
    segment_tree_has_range_add: bool = False
    segment_tree_has_range_assign: bool = False
    segment_tree_has_combined_lazy: bool = False
    segment_tree_has_range_query: bool = False
    segment_tree_query_op: str = "sum"  # 'sum' | 'min' | 'max' | 'gcd' | 'metadata' | 'max_subarray' | 'frequency' | 'interval_statistics'
    segment_tree_is_metadata: bool = False
    segment_tree_is_max_subarray: bool = False
    segment_tree_is_frequency: bool = False
    segment_tree_is_interval_statistics: bool = False
    segment_tree_is_static: bool = False
    segment_tree_is_simple_prefix: bool = False
    segment_tree_is_offline_range_add: bool = False
    segment_tree_is_fenwick_equivalent: bool = False
    segment_tree_has_no_associative_merge: bool = False
    segment_tree_has_unsupported_lazy: bool = False
    segment_tree_resource_exceeded: bool = False
    segment_tree_has_negative_frequencies: bool = False

    @property
    def segment_tree_has_negative_frequencies_in_kth(self) -> bool:
        return self.segment_tree_has_negative_frequencies

    @property
    def segment_tree_has_updates(self) -> bool:
        return self.segment_tree_has_point_update or self.segment_tree_has_range_update

    # ── 19. Dynamic Programming Signals (Phase 3K) ──
    is_dp_detected: bool = False
    dp_kind: Optional[DPKind] = None
    dp_operation_kind: Optional[DPOperationKind] = None
    dp_algorithm_family: Optional[str] = None
    dp_state_dimension: int = 1
    dp_has_optimal_substructure: bool = False
    dp_has_overlapping_subproblems: bool = False
    dp_is_dag: bool = True
    dp_is_cyclic: bool = False
    dp_greedy_optimal: bool = False
    dp_is_non_markovian: bool = False
    dp_state_space_size: int = 100000
    dp_is_resource_exceeded: bool = False
    dp_requires_reconstruction: bool = False
    dp_space_compressible: bool = False
    dp_is_unbounded: bool = False
    dp_optimization_applicable: Optional[str] = None

    # ── 20. Greedy Signals (Phase 3L) ──
    is_greedy_detected: bool = False
    greedy_kind: Optional[GreedyKind] = None
    greedy_proof_kind: Optional[GreedyProofKind] = None
    greedy_algorithm_family: Optional[str] = None
    greedy_ordering_candidate: Optional[str] = None
    greedy_has_local_choice: bool = False
    greedy_has_exchange_signal: bool = False
    greedy_has_dominance_signal: bool = False
    greedy_has_staying_ahead_signal: bool = False
    greedy_has_cut_property_signal: bool = False
    greedy_has_matroid_signal: bool = False
    greedy_requires_sorting: bool = False
    greedy_requires_heap: bool = False
    greedy_requires_graph_structure: bool = False
    greedy_objective_kind: Optional[str] = None
    greedy_feasibility_preserved: bool = True
    greedy_counterexample_detected: bool = False
    greedy_proof_unestablished: bool = False
    greedy_competing_dp_signal: bool = False
    greedy_has_greedy_choice: bool = True
    greedy_has_optimal_substructure: bool = True

    # ── 21. Divide & Conquer and Backtracking Signals (Phase 3M) ──
    is_dc_backtracking_detected: bool = False
    dc_backtracking_kind: Optional[DCBacktrackingKind] = None
    subproblem_dependency_kind: Optional[SubproblemDependencyKind] = None
    termination_guarantee_kind: Optional[TerminationGuaranteeKind] = None
    dc_backtracking_algorithm_family: Optional[str] = None

    # Structural signals
    dc_is_independent_subproblems: bool = False
    dc_has_cross_boundary_combine: bool = False
    dc_combine_complexity: Optional[str] = None  # 'O(N)', 'O(N log N)', 'O(1)', etc.
    dc_base_case_size: int = 1
    dc_recursion_depth_limit: int = 1000

    # Backtracking / Search signals
    backtracking_decision_space_size: int = 0
    backtracking_is_exponential: bool = False
    backtracking_requires_pruning: bool = False
    backtracking_pruning_kind: Optional[str] = None  # 'feasibility', 'optimality', 'symmetry', 'equivalence'
    backtracking_state_restoration: bool = False
    backtracking_symmetry_breaking: bool = False
    backtracking_is_exact_cover: bool = False
    backtracking_is_csp: bool = False
    backtracking_is_branch_and_bound: bool = False
    backtracking_objective_direction: Optional[str] = None  # 'MINIMIZE', 'MAXIMIZE'
    backtracking_bound_type: Optional[str] = None  # 'UPPER_BOUND', 'LOWER_BOUND'
    backtracking_is_meet_in_middle: bool = False
    backtracking_split_strategy: Optional[str] = None

    # ── 22. Advanced Graph Signals & Semantic Model (Phase 3N) ──
    is_adv_graph_detected: bool = False
    adv_graph_algorithm_family: Optional[str] = None
    adv_graph_semantic_model: Optional[Any] = None
    adv_graph_candidate_evaluations: List[Any] = field(default_factory=list)

    # ── 23. String Algorithms & Automata Signals & Semantic Model (Phase 3O) ──
    is_string_algorithm_detected: bool = False
    string_algorithm_family: Optional[str] = None
    string_semantic_model: Optional[Any] = None
    string_candidate_evaluations: List[Any] = field(default_factory=list)

    # ── 24. Number Theory & Combinatorics Signals & Semantic Model (Phase 3P) ──
    is_number_theory_detected: bool = False
    number_theory_family: Optional[str] = None
    number_theory_semantic_model: Optional[Any] = None
    number_theory_candidate_evaluations: List[Any] = field(default_factory=list)

    # ── 25. Algebra / Transforms Signals & Semantic Model (Phase 3Q) ──
    is_algebra_detected: bool = False
    algebra_family: Optional[str] = None
    algebra_semantic_model: Optional[Any] = None
    algebra_candidate_evaluations: List[Any] = field(default_factory=list)

    # ── 26. Computational Geometry Signals & Semantic Model (Phase 3R) ──
    is_geometry_detected: bool = False
    geometry_family: Optional[str] = None
    geometry_semantic_model: Optional[Any] = None
    geometry_candidate_evaluations: List[Any] = field(default_factory=list)

    # ── 27. Advanced Data Structures Signals & Semantic Model (Phase 3S) ──
    is_ads_detected: bool = False
    ads_family: Optional[str] = None
    ads_semantic_model: Optional[Any] = None
    ads_candidate_evaluations: List[Any] = field(default_factory=list)

    # ── 28. Cross-Family Composition Signals & Semantic Model (Phase 4) ──
    is_cross_family_detected: bool = False
    cross_family_family: Optional[str] = None
    cross_family_semantic_model: Optional[Any] = None
    cross_family_candidate_evaluations: List[Any] = field(default_factory=list)

    # Anti-patterns & Resource gates
    backtracking_search_space_explosive: bool = False
    backtracking_greedy_sufficient: bool = False
    backtracking_dp_sufficient: bool = False
    dc_subproblems_not_independent: bool = False
    dc_combine_step_intractable: bool = False
    dc_base_case_undefined: bool = False
    backtracking_resource_limit_exceeded: bool = False

    # Section 8: Cross-family composition / Tower gate
    is_cross_family_composition: bool = False
    composition_unsupported: bool = False

class FeatureExtractor:
    """Extracts semantic and structural features from problem text."""

    @staticmethod
    def extract(text: str) -> ProblemFeatures:
        lower = text.lower()

        # 1. Input Structure
        input_structure = 'single_sequence'
        if re.search(r'linked\s*list|node\s*\*\s*|head\s*->\s*next|list\s*node', lower):
            input_structure = 'linked_list'
        elif re.search(r'two\s+(?:already\s+)?(?:sorted\s+|unsorted\s+)?arrays|merge\s+two', lower):
            input_structure = 'two_sequences'
        elif re.search(r'grid|matrix|2d\s+array', lower):
            input_structure = 'grid'

        # 2. Ordering & Sorting
        is_sorted = bool(re.search(r'(?<!un)sorted\s+(?:[a-z]+\s+)?(?:array|sequence|order|list|stream|integers?|numbers?|collection)|already\s+sorted|ascending|non-?decreasing|ordered\s+(?:collection|sequence|array|vector|list)', lower))
        # Check if unsorted explicitly mentioned
        is_unsorted = bool(re.search(r'unsorted|arbitrary\s+order', lower))
        if is_unsorted:
            is_sorted = False

        # Can we sort? If indices must be reported, sorting might still be permitted IF we track original indices (e.g. vector<pair<int,int>>)
        # BUT if order of array cannot be modified and it asks for subarray, sorting is FORBIDDEN!
        is_contiguous = bool(re.search(r'contiguous|subarray|substring|window|consecutive|segment|block', lower))
        
        can_sort = True
        if is_contiguous and not re.search(r'sort\s+the\s+array', lower):
            # Subarray contiguity is destroyed by sorting!
            can_sort = False
        if re.search(r'cannot\s+be\s+sorted|do\s+not\s+sort|maintain\s+original\s+order|do\s+not\s+reorder|sorting\s+(?:the\s+input\s+)?is\s+forbidden|not\s+allowed|cannot\s+sort|without\s+sorting', lower):
            can_sort = False
        if re.search(r'sorting\s+is\s+allowed|sort\s+the\s+array|allowed\s+if|sorting\s+is\s+permitted', lower):
            can_sort = True

        requires_original_indices = bool(re.search(r'distinct\s+positions|original\s+indices|1-based\s+index|positions?\s+of\s+the\s+values|indices\s+of\s+the\s+two', lower))

        # 3. Value characteristics (negatives, non-negative)
        has_negative_values = False
        if re.search(r'negative|positive\s+and\s+negative|any\s+integer|-10\^|<=?\s*-', lower):
            has_negative_values = True
        if re.search(r'non-?negative|positive\s+integers|strictly\s+positive|1\s*<=\s*a\[i\]|0\s*<=\s*a\[i\]', lower):
            has_negative_values = False

        # 4. Contiguity & Tracks
        tracks_distinct = bool(re.search(r'distinct\s+(?:elements?|values?|characters?|event\s+types?)|unique\s+characters?|no\s+more\s+than\s+k\s+different|at\s+most\s+k\s+distinct|without\s+repeating|k\s+zeros?|k\s+different', lower))

        # 5. Objectives
        optimization_objective = None
        if re.search(r'trapping\s+rain\s+water|trap(?:ped)?\s+(?:rain\s+)?water|elevation\s+map', lower):
            optimization_objective = 'trapping_water'
        elif re.search(r'most\s+water|maximum\s+area|max\s+area|container', lower):
            optimization_objective = 'max_area'
        elif re.search(r'minimum\s+window\s+substring|smallest\s+substring\s+containing', lower):
            optimization_objective = 'min_window_substring'
        elif re.search(r'longest\s+(?:contiguous\s+)?(?:subarray|substring|window|segment|block)|maximum\s+length', lower):
            optimization_objective = 'max_length'
        elif re.search(r'shortest\s+(?:contiguous\s+)?(?:subarray|substring|window|segment)|(?:smallest|mini(?:mal|mum))\s+(?:size|length)', lower):
            optimization_objective = 'min_length'
        elif re.search(r'maximum\s+sum\s+(?:of\s+(?:a|any)?\s*)?(?:contiguous\s+)?subarray|max\s+sum\s+window', lower):
            optimization_objective = 'max_sum'
        elif re.search(r'exactly\s+[k\d]+\s+(?:distinct|different)', lower):
            optimization_objective = 'exact_count_derived'
        elif re.search(r'count\s+(?:the\s+number\s+of\s+)?contiguous\s+subarrays|number\s+of\s+subarrays', lower):
            optimization_objective = 'count_subarrays_bounded'

        # 6. Search objective
        search_objective = None
        if re.search(r'cycle\s+(?:begins?|starts?)|start\s+of\s+(?:the\s+)?cycle|beginning\s+of\s+(?:the\s+)?cycle', lower):
            search_objective = 'cycle_start'
        elif re.search(r'cycle|loop\s+in\s+linked|tortoise', lower):
            search_objective = 'cycle'
        elif re.search(r'closest\s+to\s+target|sum\s+closest|minimum\s+absolute\s+difference\s+between\s+the\s+sum\s+of\s+two', lower):
            search_objective = 'closest_pair_sum'
        elif re.search(r'count\s+(?:the\s+number\s+of\s+)?pairs\s+(?:whose\s+sum\s+is\s+|<|less\s+than)|number\s+of\s+pairs.*(?:less\s+than|<)', lower):
            search_objective = 'count_pairs_less'
        elif re.search(r'count\s+(?:the\s+number\s+of\s+)?pairs\s+(?:whose\s+sum\s+is\s+|==?|equals?)|number\s+of\s+pairs.*(?:equals?|==)', lower):
            search_objective = 'count_pairs_equal'
        elif re.search(r'three\s+(?:distinct\s+)?[a-z]+\s+(?:that\s+add|whose\s+sum|with\s+sum|sum\s+to)|triplet', lower):
            search_objective = 'three_sum'
        elif re.search(r'four\s+(?:distinct\s+)?[a-z]+\s+(?:that\s+add|whose\s+sum|with\s+sum|sum\s+to)|quadruplet', lower):
            search_objective = 'four_sum'
        elif re.search(r'difference.*(?:equal|equals?|==?|is|\bk\b)|pair\s+with\s+difference|a\[j\]\s*-\s*a\[i\]', lower) and not bool(re.search(r'difference\s+constraints?|system\s+of|\bconsistent\b|\bcontradiction\b|\bdsu\b|potential', lower)):
            search_objective = 'pair_diff'
        elif re.search(r'two\s+.*(?:whose\s+sum|whose\s+combined\s+value|combined\s+value|sum\s+(?:is|equals?|up\s+to)|that\s+add)|pair\s+.*(?:sum|combined)|sum\s+of\s+two|positions\s+with\s+sum|two\s+(?:elements?|values?|numbers?)\s+.*(?:sum|combined)', lower):
            search_objective = 'pair_sum'
        elif re.search(r'reads?\s+the\s+same\s+(?:from\s+)?left\s+to\s+right|palindrome', lower):
            search_objective = 'palindrome'
        elif re.search(r'middle\s+(?:node|of)|second\s+middle', lower):
            search_objective = 'middle'
        elif re.search(r'share\s+a\s+common\s+value|common\s+element|intersection\s+of\s+two', lower):
            search_objective = 'common_element'

        # 7. Partition requirement
        partition_requirement = None
        if re.search(r'dutch\s+national\s+flag|sort\s+0s?,\s*1s?,\s*and\s*2s?|containing\s+only\s+0,\s*1,\s*and\s*2|sort\s+colors|three-?way\s+partition', lower):
            partition_requirement = 'dutch_flag_012'
        elif re.search(r'(?:move|push)\s+(?:all\s+)?zero(?:es|s)?.*(?:relative\s+order|maintaining|preserving)', lower) or re.search(r'(?:maintaining|preserving)\s+the\s+relative\s+order.*zero(?:es|s)?', lower):
            partition_requirement = 'move_zeroes_ordered'
        elif re.search(r'negative\s+(?:values?\s+)?come\s+before\s+(?:all\s+)?non-?negative|negatives?\s+before\s+positives?', lower):
            partition_requirement = 'two_way_negatives'
        elif re.search(r'move\s+(?:all\s+)?zero(?:es|s)?|zero(?:es|s)?\s+to\s+(?:the\s+)?end|push\s+zero(?:es|s)?', lower):
            partition_requirement = 'two_way_zeroes'
        elif re.search(r'partition\s+(?:the\s+|an?\s+|array\s+)*by\s+parity|even\s+(?:integers?\s+)?(?:appear\s+)?before\s+odd|odd\s+(?:integers?\s+)?(?:appear\s+)?before\s+even', lower):
            partition_requirement = 'parity'

        # 8. Mutability & In-Place
        in_place_required = bool(re.search(r'in-?place|o\(1\)\s+(?:extra\s+)?memory|modify\s+(?:the\s+array\s+in-place|input\s+directly)|without\s+allocating\s+extra\s+space|remove\s+(?:all\s+occurrences|duplicates|element)|keep\s+at\s+most\s+\w+\s+copies|compacted?\s+in\s+place', lower))
        if re.search(r'remove\s+duplicates\s+from\s+sorted|compaction|remove\s+element|remove\s+all\s+occurrences|keep\s+at\s+most\s+\w+\s+copies|compacted?\s+in\s+place|move_zeroes_ordered', lower) or partition_requirement == 'move_zeroes_ordered':
            in_place_required = True

        # 9. Dynamic updates & repeated queries (Negative signals for Two Pointers)
        has_dynamic_updates = bool(re.search(
            r'online\s+updates?|point\s+updates?|updates?\s+(?:to\s+)?(?:the\s+value|elements?|positions?)|'
            r'modify\s+elements?\s+at\s+index|update\s+(?:arr\[\w+\]|\w+\[\w+\]|elements?|the\s+value)|'
            r'set\s+\w+\[\w+\]|queries\s+and\s+updates|updates?\s+and\s+queries|'
            r'operations\s+online|interleaved', lower))
        repeated_queries = bool(re.search(r'for\s+each\s+query|answer\s+q\s+queries|q\s+questions|repeated\s+(?:\w+\s+)*queries', lower))

        # 10. Output requirement
        output_requirement = 'values'
        if requires_original_indices or re.search(r'print\s+(?:the\s+)?(?:1-based\s+)?indices|positions', lower):
            output_requirement = 'pair_indices'
        elif optimization_objective in ('max_length', 'min_length', 'min_window_substring'):
            output_requirement = 'length'
        elif optimization_objective in ('max_area', 'trapping_water'):
            output_requirement = optimization_objective
        elif optimization_objective in ('count_subarrays_bounded', 'exact_count_derived') or search_objective in ('count_pairs_less', 'count_pairs_equal'):
            output_requirement = 'count'
        elif search_objective == 'cycle':
            output_requirement = 'boolean'
        elif search_objective in ('middle', 'cycle_start'):
            output_requirement = 'node'
        elif in_place_required:
            output_requirement = 'modified_array'
        elif search_objective in ('pair_sum', 'closest_pair_sum', 'three_sum', 'four_sum'):
            output_requirement = 'pair_values'

        # Extract target value if present
        target_val_match = re.search(r'(?:target|sum|x|s|k)\s*=\s*(\d+)|(?:sum|target)\s+(?:is\s+|equal\s+to\s+)(\d+)', lower)
        target_value = None
        if target_val_match:
            target_value = target_val_match.group(1) or target_val_match.group(2)

        # Extract fixed window size if present
        window_k_match = re.search(r'window\s+(?:of\s+)?size\s+(\d+|k)|subarray\s+of\s+size\s+(\d+|k)|k\s*=\s*(\d+)', lower)
        window_size_k = None
        if window_k_match:
            val = window_k_match.group(1) or window_k_match.group(2) or window_k_match.group(3)
            window_size_k = int(val) if val.isdigit() else 1

        # ── Monotonic Stack Feature Extraction (Phase 3B) ──

        # Detect nearest boundary query (structural: first element satisfying a directional comparison)
        _next_greater = bool(re.search(
            r'next\s+(?:greater|larger|bigger|higher)\s+(?:element|number|value|temperature|bar)|'
            r'next\s+(?:element|bar|number|value|temperature)\s+(?:that\s+is\s+)?(?:strictly\s+)?(?:greater|larger|bigger|higher|warmer|taller)|'
            r'first\s+(?:element|number|value|bar|temperature)\s+(?:to\s+the\s+right|on\s+the\s+right)?\s*(?:that\s+is\s+)?(?:strictly\s+)?(?:greater|larger|bigger|higher|warmer|taller)|'
            r'first\s+\w+\s+(?:you\s+reach\s+)?(?:\([^)]*\)\s+)?that\s+(?:is|has)\s+(?:a\s+)?(?:higher|greater|larger|warmer|taller)|'
            r'daily\s+temperatures?|warmer\s+temperature|days?\s+until\s+(?:a\s+)?warmer|'
            r'first\s+future\s+day\s+(?:that\s+is\s+)?warmer|'
            r'next\s+(?:element|bar|number)\s+(?:greater|larger|bigger)', lower))

        _next_smaller = bool(re.search(
            r'next\s+(?:smaller|lesser|lower)\s+(?:element|number|value|bar)|'
            r'next\s+(?:element|bar|number|value)\s+(?:that\s+is\s+)?(?:strictly\s+)?(?:smaller|lesser|lower)|'
            r'first\s+(?:element|number|value|bar|trench)\s+(?:to\s+the\s+right|on\s+the\s+right)?\s*(?:that\s+is\s+)?(?:strictly\s+)?(?:smaller|lesser|lower|shallower)|'
            r'next\s+(?:element|bar|number)\s+(?:smaller|lesser|lower)', lower))

        _prev_greater = bool(re.search(
            r'previous\s+(?:greater|larger|bigger|higher)\s+(?:element|number|value)|'
            r'previous\s+(?:element|bar|number|value)\s+(?:that\s+is\s+)?(?:strictly\s+)?(?:greater|larger|bigger|higher)|'
            r'first\s+(?:element|number|value)\s+(?:to\s+the\s+left|on\s+the\s+left)\s+(?:that\s+is\s+)?(?:strictly\s+)?(?:greater|larger|bigger|higher)|'
            r'nearest\s+(?:greater|larger|bigger|higher|taller)\s+(?:element|value|building|bar|number)|'
            r'nearest\s+(?:element|value|building|position)\s+(?:that\s+is\s+)?(?:strictly\s+)?(?:greater|larger|bigger|higher|taller)\s*(?:to\s+its\s+left|on\s+the\s+left|to\s+the\s+left)?|'
            r'taller\s+building\s+immediately\s+to\s+its\s+left', lower))

        _prev_smaller = bool(re.search(
            r'previous\s+(?:smaller|lesser|lower)\s+(?:element|number|value)|'
            r'previous\s+(?:element|bar|number|value)\s+(?:that\s+is\s+)?(?:strictly\s+)?(?:smaller|lesser|lower)|'
            r'first\s+(?:element|number|value)\s+(?:to\s+the\s+left|on\s+the\s+left)\s+(?:that\s+is\s+)?(?:strictly\s+)?(?:smaller|lesser|lower)|'
            r'nearest\s+(?:smaller|lesser|lower|shorter|shallower)\s+(?:element|value|building|bar|number)|'
            r'nearest\s+(?:element|value|position)\s+(?:j\s*<\s*i\s+)?(?:such\s+that.*)?(?:strictly\s+)?(?:smaller|lesser|lower)|'
            r'most\s+recent\s+previous\s+day.*strictly\s+lower', lower))

        _nearest_greater = bool(re.search(
            r'nearest\s+(?:greater|larger|higher)\s+(?:element|value|number)|'
            r'closest\s+(?:greater|larger)\s+(?:element|value)|'
            r'nearest\s+(?:element|value|number)\s+(?:that\s+is\s+)?(?:strictly\s+)?(?:greater|larger|higher)', lower))

        _nearest_smaller = bool(re.search(
            r'nearest\s+(?:smaller|lesser|lower)\s+(?:element|value|number)|'
            r'closest\s+(?:smaller|lesser)\s+(?:element|value)|'
            r'nearest\s+(?:element|value|number)\s+(?:that\s+is\s+)?(?:strictly\s+)?(?:smaller|lesser|lower)', lower))

        nearest_boundary_query = any([
            _next_greater, _next_smaller, _prev_greater, _prev_smaller,
            _nearest_greater, _nearest_smaller
        ])

        # Determine boundary_relation: 'greater' or 'smaller'
        boundary_relation: Optional[str] = None
        if _next_greater or _prev_greater or _nearest_greater:
            boundary_relation = 'greater'
        elif _next_smaller or _prev_smaller or _nearest_smaller:
            boundary_relation = 'smaller'
        # If both detected (e.g. "nearest greater or nearest smaller"), leave as 'greater' (first found wins)
        if _next_greater and _next_smaller:
            boundary_relation = 'greater'  # prefer first signal

        # Determine boundary_direction: 'right', 'left', or 'both'
        boundary_direction: Optional[str] = None
        if nearest_boundary_query:
            _either_direction = bool(re.search(r'either\s+direction|left\s+or\s+right|both\s+directions|either\s+to\s+the\s+left\s+or\s+right', lower))
            _left_explicit = bool(re.search(r'to\s+(?:its\s+|the\s+)?left|on\s+(?:its\s+|the\s+)?left|j\s*<\s*i|previous|before', lower))
            _right_explicit = bool(re.search(r'to\s+(?:its\s+|the\s+)?right|on\s+(?:its\s+|the\s+)?right|j\s*>\s*i|next|after|future\s+day', lower))

            if _either_direction or (_nearest_greater and not _left_explicit and not _right_explicit) or (_nearest_smaller and not _left_explicit and not _right_explicit):
                boundary_direction = 'both'
            elif _left_explicit and not _right_explicit:
                boundary_direction = 'left'
            elif _right_explicit and not _left_explicit:
                boundary_direction = 'right'
            elif _prev_greater or _prev_smaller:
                boundary_direction = 'left'
            elif _next_greater or _next_smaller:
                boundary_direction = 'right'
            else:
                boundary_direction = 'right'  # default scan direction

        # Comparison strictness: detect >= or <=
        comparison_strictness: Optional[str] = None
        if nearest_boundary_query:
            if re.search(r'greater\s+than\s+or\s+equal|>=|at\s+least|not\s+less\s+than', lower):
                comparison_strictness = 'non_strict'
            elif re.search(r'smaller\s+than\s+or\s+equal|<=|at\s+most|not\s+greater\s+than', lower):
                comparison_strictness = 'non_strict'
            else:
                comparison_strictness = 'strict'

        # Circular array detection
        is_circular = bool(re.search(
            r'circular\s+array|circular\s+queue|wrap\s+around|wraps?\s+around|'
            r'circularly|next\s+greater\s+.*circular|circular.*next\s+greater|'
            r'arranged\s+in\s+a\s+circle|clockwise', lower))

        # Contribution / range-ownership problems
        contribution_objective: Optional[str] = None
        if re.search(
            r'sum\s+of\s+(?:all\s+)?subarray\s+min(?:imum)?s?|'
            r'sum\s+of\s+minimum\s+(?:of\s+all\s+)?subarrays?|'
            r'sum\s+of\s+minimums?\s+of\s+(?:all\s+)?subarrays?|'
            r'total\s+minimum\s+(?:contribution|sum)|'
            r'subarray\s+min(?:imum)?\s+sum|'
            r'(?:total\s+)?sum\s+of\s+all\s+(?:those\s+)?minimum\s+values|'
            r'minimum\s+(?:daily\s+)?expense.*(?:total|sum)|'
            r'minimum\s+value\s+in\s+that\s+subarray.*(?:total|sum)|'
            r'minimum.*(?:during|for\s+every|in)\s+(?:that|each|every)\s+period.*(?:total|sum)|'
            r'(?:total|sum).*(?:across|over)\s+all\s+periods.*minimum', lower):
            contribution_objective = 'sum_min'
        elif re.search(
            r'sum\s+of\s+(?:all\s+)?subarray\s+max(?:imum)?s?|'
            r'sum\s+of\s+maximum\s+(?:of\s+all\s+)?subarrays?|'
            r'sum\s+of\s+maximums?\s+of\s+(?:all\s+)?subarrays?|'
            r'total\s+maximum\s+(?:contribution|sum)|'
            r'subarray\s+max(?:imum)?\s+sum|'
            r'(?:total\s+)?sum\s+of\s+all\s+(?:those\s+)?maximum\s+values|'
            r'maximum\s+(?:daily\s+)?revenue.*(?:total|sum)|'
            r'sum\s+of\s+peak\s+revenues|'
            r'maximum.*(?:during|for\s+every|in)\s+(?:that|each|every)\s+period.*(?:total|sum)|'
            r'(?:total|sum).*(?:across|over)\s+all\s+periods.*maximum', lower):
            contribution_objective = 'sum_max'

        # Histogram pattern detection
        histogram_pattern = bool(re.search(
            r'largest\s+rectangle\s+(?:in|of)\s+(?:a\s+)?histogram|'
            r'maximal\s+rectangle\s+.*histogram|'
            r'histogram\s+.*(?:largest|maximal|maximum)\s+rectangle|'
            r'bars?\s+.*(?:largest|maximum)\s+rectangle|'
            r'area\s+of\s+(?:the\s+)?largest\s+(?:axis-aligned\s+)?rectangle\s+(?:in|under|formed)|'
            r'maximum\s+area\s+of\s+a\s+rectangular\s+section|'
            r'rectangular\s+section.*planks?|planks?.*rectangular\s+section', lower))

        # Stock span detection: distance to previous dominant element
        has_stock_span_pattern = bool(re.search(
            r'stock\s+span|span\s+of\s+(?:a\s+)?stock|'
            r'(?:number\s+of\s+)?consecutive\s+(?:recent\s+)?days?\s+(?:the\s+)?(?:closing\s+)?(?:stock\s+)?price\s+(?:was|has\s+been|is|did\s+not).*?(?:less|lower|smaller|not\s+greater|not\s+higher|exceed)|'
            r'days?\s+(?:for\s+which\s+|where\s+)?(?:the\s+)?price\s+(?:was|is)\s+(?:less|lower|smaller)\s+(?:than\s+or\s+equal\s+to\s+)?(?:today|current)|'
            r'streak.*consecutive.*days.*price|price.*streak', lower))

        # Also detect stock span as: "for each day find number of consecutive days ... price <= today"
        if not has_stock_span_pattern and re.search(
            r'for\s+each\s+(?:day|element|index)\s+.*(?:how\s+many|number\s+of)\s+(?:consecutive|previous)\s+(?:days?|elements?)', lower):
            has_stock_span_pattern = True

        # Duplicate dominance: explicit mention of duplicates or equal elements in boundary context
        has_duplicate_dominance = bool(
            nearest_boundary_query and
            re.search(r'duplicate|equal\s+elements?|same\s+value|ties?|repeated\s+values?|'
                      r'not\s+strictly|greater\s+or\s+equal|smaller\s+or\s+equal', lower)
        )

        # If stock span or histogram also implies nearest_boundary_query
        if has_stock_span_pattern and not nearest_boundary_query:
            nearest_boundary_query = True
            boundary_relation = 'greater'
            boundary_direction = 'left'
            if comparison_strictness is None:
                comparison_strictness = 'non_strict'

        # ── Binary Search Feature Extraction (Phase 3C) ──
        has_ordered_search_space = (is_sorted or bool(re.search(
            r'(?<!un)sorted\s+(?:array|sequence|vector|list|collection)|ordered\s+(?:collection|sequence|array|vector|list|elements?|search\s+space)|'
            r'ascending\s+order|increasing\s+order|non-decreasing\s+order|already\s+sorted|elements\s+are\s+sorted', lower))) and not is_unsorted

        # Check for non-monotonicity anti-patterns
        has_non_monotonic_predicate = bool(re.search(
            r'predicate\s+(?:alternates|oscillates)|non-monoton(?:e|ic)|'
            r'true.*then\s+false.*then\s+true|false.*true.*false|'
            r'odd\s+index.*even\s+index', lower))

        # 1. Answer-space feasibility binary search
        is_ans_min = bool(re.search(
            r'minimum\s+(?:possible\s+)?(?:maximum\s+|largest\s+|max\s+)?(?:\w+\s+)?(?:capacity|speed|time|days|weight|operations|load|sum|value)|'
            r'minimize\s+(?:the\s+)?(?:maximum|largest)|least\s+(?:weight\s+)?capacity|'
            r'smallest\s+maximum\s+(?:load|sum)|koko\s+eating\s+bananas|painter\'?s?\s+partition|'
            r'book\s+allocation|split\s+array\s+largest\s+sum|minimum\s+feasible\s+value|'
            r'minimum\s+threshold\s+such\s+that', lower)) and not bool(re.search(r'sum\s+of\s+(?:all\s+)?subarray\s+min|\bheap(?:ify)?\b|\bpriority\s*queue\b', lower))

        is_ans_max = bool(re.search(
            r'maximum\s+(?:possible\s+)?(?:minimum\s+distance|distance|threshold|length|allocation|value)|'
            r'maximize\s+(?:the\s+)?(?:minimum|smallest)|minimum\s+distance.*is\s+maximized|'
            r'aggressive\s+cows|wood\s+cut|rope\s+cut|cut\s+.*at\s+least\s+k\s+pieces|'
            r'maximum\s+feasible\s+value|maximum\s+achievable\s+threshold', lower)) and not bool(re.search(r'sum\s+of\s+(?:all\s+)?subarray\s+max|\bheap(?:ify)?\b|\bpriority\s*queue\b|\bdsu\b|disjoint\s+set|union[\s-]find|component\s+metadata|sliding\s+window', lower))

        # 2. Value-domain / Numeric search
        has_numeric_domain = bool(re.search(
            r'integer\s+square\s+root|square\s+root\s+of\s+(?:an?\s+integer|n|x)|'
            r'monotone\s+function|root\s+of\s+(?:a\s+)?monotone|numeric\s+interval|'
            r'find\s+integer\s+x\s+such\s+that\s+x\s*\*\s*x', lower))

        # 3. Ordered Data Search (Lower / Upper / Exact / First / Last / Pred / Succ)
        is_lb = bool(re.search(
            r'lower\s*bound|first\s+(?:element|index|position)\s+.*?(?:>=|greater\s+than\s+or\s+equal)|'
            r'smallest\s+index\s+.*?(?:>=|greater\s+than\s+or\s+equal)|first\s+greater\s+than\s+or\s+equal', lower))

        is_ub = bool(re.search(
            r'upper\s*bound|first\s+(?:element|index|position)\s+.*?(?:>(?!=)|strictly\s+greater)|'
            r'smallest\s+index\s+.*?(?:>(?!=)|strictly\s+greater)|first\s+(?:element\s+)?strictly\s+greater', lower)) and not is_lb

        is_pred = bool(re.search(
            r'predecessor|largest\s+element.*strictly\s+less|largest\s+(?:element|value)\s+.*<(?!=)|'
            r'greatest\s+element\s+strictly\s+less', lower))

        is_succ = bool(re.search(
            r'successor|smallest\s+element.*strictly\s+greater|smallest\s+(?:element|value)\s+.*>(?!=)|'
            r'least\s+element\s+strictly\s+greater', lower))

        is_first_true = bool(re.search(
            r'first\s+true|first\s+bad\s+version|first\s+occurrence|first\s+(?:valid|feasible)\s+(?:element|position|index)|'
            r'first\s+index\s+where', lower))

        is_last_true = bool(re.search(
            r'last\s+true|last\s+occurrence|last\s+(?:valid|feasible)\s+(?:element|position|index)|'
            r'last\s+index\s+where', lower))

        is_first_false = bool(re.search(r'first\s+false', lower))
        is_last_false = bool(re.search(r'last\s+false', lower))

        is_exact = bool(re.search(
            r'search\s+for\s+(?:the\s+)?target|find\s+(?:the\s+)?index\s+of\s+(?:the\s+)?target|'
            r'exact\s+(?:binary\s+)?search|binary\s+search\s+for|search\s+in\s+sorted\s+array', lower)) and not (is_lb or is_ub or is_pred or is_succ or is_first_true or is_last_true)

        # Compound with other patterns
        compound_with = None
        if re.search(r'greedy|greedily|painter|ship|cows', lower):
            compound_with = 'greedy'
        elif re.search(r'prefix\s+sum', lower):
            compound_with = 'prefix_sum'
        elif re.search(r'sort.*then\s+binary\s+search|unsorted.*sort', lower):
            compound_with = 'sorting'
        elif re.search(r'two\s+pointers', lower):
            compound_with = 'two_pointers'

        is_answer_space_search = is_ans_min or is_ans_max
        search_space_type = None
        target_boundary = None
        predicate_direction = None
        feasibility_objective = None
        has_monotonic_predicate = False

        if is_answer_space_search:
            search_space_type = 'answer_values'
            has_monotonic_predicate = not has_non_monotonic_predicate
            if is_ans_min:
                feasibility_objective = 'minimize_maximum'
                target_boundary = 'first_true'
                predicate_direction = 'false_to_true'
            else:
                feasibility_objective = 'maximize_minimum'
                target_boundary = 'last_true'
                predicate_direction = 'true_to_false'
        elif has_numeric_domain:
            search_space_type = 'numeric_domain'
            target_boundary = 'last_true' if ('square root' in lower or 'sqrt' in lower) else 'first_true'
            predicate_direction = 'true_to_false' if target_boundary == 'last_true' else 'false_to_true'
            has_monotonic_predicate = not has_non_monotonic_predicate
        elif (has_ordered_search_space or has_non_monotonic_predicate or re.search(r'binary\s+search(?!\s+tree)', lower)) and not re.search(r'\b(?:tree|trees|bst|root|leaf|leaves|subtree|subtrees)\b', lower):
            # Check we don't accidentally intercept Two Pointers converging pair problems
            if not (search_objective in ('pair_sum', 'closest_pair_sum', 'three_sum', 'four_sum', 'trapping_water') or
                    optimization_objective in ('max_area', 'trapping_water')):
                search_space_type = 'indices'
                has_monotonic_predicate = not has_non_monotonic_predicate
                if is_exact:
                    target_boundary = 'exact'
                    predicate_direction = 'equality'
                elif is_lb:
                    target_boundary = 'lower_bound'
                    predicate_direction = 'false_to_true'
                elif is_ub:
                    target_boundary = 'upper_bound'
                    predicate_direction = 'false_to_true'
                elif is_pred:
                    target_boundary = 'predecessor'
                    predicate_direction = 'true_to_false'
                elif is_succ:
                    target_boundary = 'successor'
                    predicate_direction = 'false_to_true'
                elif is_first_false:
                    target_boundary = 'first_false'
                    predicate_direction = 'true_to_false'
                elif is_last_false:
                    target_boundary = 'last_false'
                    predicate_direction = 'false_to_true'
                elif is_first_true:
                    target_boundary = 'first_true'
                    predicate_direction = 'false_to_true'
                elif is_last_true:
                    target_boundary = 'last_true'
                    predicate_direction = 'true_to_false'
                elif re.search(r'binary\s+search|search\s+for|find\s+element', lower):
                    target_boundary = 'exact'
                    predicate_direction = 'equality'
                elif has_non_monotonic_predicate:
                    target_boundary = 'first_true'
                    predicate_direction = 'false_to_true'

        requires_exact_lookup = (target_boundary == 'exact')

        # ── Binary Search additions (Phase 3C hardening) ──
        if is_answer_space_search:
            search_space_kind = SearchSpaceKind.FEASIBILITY_DOMAIN
            if feasibility_objective in ("minimize_maximum", "minimum_feasible") or re.search(r'ship|capacity|load|painter|split\s+array', lower):
                answer_space_low_expression = "*std::max_element(weights.begin(), weights.end())"
                answer_space_high_expression = "std::accumulate(weights.begin(), weights.end(), 0LL)"
            elif re.search(r'speed|rate|banana|koko|hour', lower):
                answer_space_low_expression = "1LL"
                answer_space_high_expression = "*std::max_element(piles.begin(), piles.end())"
            elif re.search(r'aggressive\s+cows|distance|stall|coordinate', lower):
                answer_space_low_expression = "1LL"
                answer_space_high_expression = "stalls.back() - stalls.front()"
            else:
                answer_space_low_expression = "1LL"
                answer_space_high_expression = "1000000000LL"
        elif has_numeric_domain:
            search_space_kind = SearchSpaceKind.INTEGER_VALUE
            answer_space_low_expression = "0LL"
            answer_space_high_expression = "x"
        elif has_ordered_search_space:
            search_space_kind = SearchSpaceKind.INDEX
            answer_space_low_expression = "0"
            answer_space_high_expression = "n - 1"
        else:
            search_space_kind = None
            answer_space_low_expression = None
            answer_space_high_expression = None

        if target_boundary in ("lower_bound", "first_true", "first_occurrence"):
            exact_match_semantics = ExactMatchSemantics.FIRST_MATCH
        elif target_boundary in ("upper_bound", "last_true", "last_occurrence"):
            exact_match_semantics = ExactMatchSemantics.LAST_MATCH
        elif target_boundary == "exact":
            exact_match_semantics = ExactMatchSemantics.ANY_MATCH
        else:
            exact_match_semantics = None

        # ── 12. Trie Features (Phase 3D) ──
        trie_kind = None
        prefix_query_type = None
        trie_alphabet = None
        trie_storage = None
        estimated_node_count = 0
        estimated_memory_bytes = 0
        memory_limit_bytes = 256 * 1024 * 1024
        memory_limit_exceeded = False
        has_single_query_only = False
        has_prefix_sharing_advantage = False

        is_xor_problem = bool(re.search(r'\bxor\b|bitwise\s+xor|maximum\s+xor|max\s+xor', lower))
        is_trie_explicit = bool(re.search(r'\btrie\b', lower))
        is_prefix_dict = bool(re.search(r'prefix(?:es)?|starts?\s+with|autocomplete|lexicographical|dictionary|words?\s+list', lower)) and not bool(re.search(r'prefix\s+(?:\w+\s+){0,3}(?:sum|min|max|minimum|maximum|query|queries|aggregation|extremum|count|frequenc|total|flux)', lower))

        if is_xor_problem:
            trie_kind = TrieKind.BINARY_TRIE
            trie_alphabet = TrieAlphabetKind.BINARY_2
            trie_storage = TrieStorageKind.FIXED_ARRAY
            has_prefix_sharing_advantage = True
            if re.search(r'query|queries|given\s+(?:number|integer|x|val)|for\s+each', lower) and not re.search(r'maximum\s+xor\s+(?:of\s+)?two\s+(?:numbers|elements)|pair', lower):
                prefix_query_type = "max_xor_query"
            else:
                prefix_query_type = "max_xor_pair"
            estimated_node_count = 100000 * 32
            estimated_memory_bytes = estimated_node_count * 24

        elif is_trie_explicit or (is_prefix_dict and not re.search(r'binary\s+search|monotone', lower)):
            trie_kind = TrieKind.CHARACTER_TRIE
            has_prefix_sharing_advantage = True

            # Query type
            if re.search(r'longest\s+(?:common\s+)?prefix', lower):
                prefix_query_type = "longest_prefix"
            elif re.search(r'autocomplete|suggest(?:ions)?|typeahead', lower):
                prefix_query_type = "autocomplete"
            elif re.search(r'lexicographical(?:ly)?|alphabetical|lexical\s+order|sort\s+strings', lower):
                prefix_query_type = "lexicographic_sort"
            elif re.search(r'delete|deletion|remove|erasing|erasure', lower):
                prefix_query_type = "deletion"
            elif re.search(r'count\s+words?\s+equal|word\s+count|frequency\s+of\s+word', lower):
                prefix_query_type = "word_count"
            elif re.search(r'count\s+(?:words?\s+)?(?:starting|with\s+prefix)|prefix\s+count', lower):
                prefix_query_type = "prefix_count"
            elif re.search(r'starts?\s+with|prefix\s+search|has\s+prefix', lower):
                prefix_query_type = "prefix_search"
            else:
                prefix_query_type = "exact_search"

            # Alphabet
            if re.search(r'0-9|digits?|numeric\s+strings?', lower):
                trie_alphabet = TrieAlphabetKind.DIGITS_10
                slot_count = 10
            elif re.search(r'binary|bits?|0\s+and\s+1', lower):
                trie_alphabet = TrieAlphabetKind.BINARY_2
                slot_count = 2
            elif re.search(r'ascii|arbitrary\s+char|all\s+128', lower):
                trie_alphabet = TrieAlphabetKind.ASCII_128
                slot_count = 128
            elif re.search(r'unicode|arbitrary\s+unicode|map\s+backed', lower):
                trie_alphabet = TrieAlphabetKind.ARBITRARY_MAP
                slot_count = 0
            else:
                trie_alphabet = TrieAlphabetKind.LOWERCASE_26
                slot_count = 26

            # Child storage
            if prefix_query_type == "lexicographic_sort" and trie_alphabet in (TrieAlphabetKind.ASCII_128, TrieAlphabetKind.ARBITRARY_MAP):
                trie_storage = TrieStorageKind.ORDERED_MAP
            elif trie_alphabet in (TrieAlphabetKind.LOWERCASE_26, TrieAlphabetKind.DIGITS_10, TrieAlphabetKind.BINARY_2):
                trie_storage = TrieStorageKind.FIXED_ARRAY
            else:
                trie_storage = TrieStorageKind.HASH_MAP

            # Memory estimation
            if re.search(r'exceeds\s+memory|memory\s+limit\s+exceeded|out\s+of\s+memory|10\^7\s+strings|10\^8\s+characters|too\s+large\s+for\s+heap', lower):
                estimated_memory_bytes = 512 * 1024 * 1024
                memory_limit_exceeded = True
            else:
                estimated_node_count = 100000
                bytes_per_node = (slot_count * 8 + 16) if slot_count > 0 else 48
                estimated_memory_bytes = estimated_node_count * bytes_per_node
                if estimated_memory_bytes > memory_limit_bytes:
                    memory_limit_exceeded = True

            # Single query check
            if re.search(r'single\s+query|one\s+query|only\s+one\s+search|single\s+comparison|once\s+only', lower) and not re.search(r'dictionary|stream|repeated|insert.*and.*search', lower):
                has_single_query_only = True
                has_prefix_sharing_advantage = False

        # ── 13. Tree Features Extraction (Phase 3E) ──
        tree_kind: Optional[TreeKind] = None
        tree_representation: Optional[TreeRepresentation] = None
        tree_traversal_order: Optional[TreeTraversalOrder] = None
        tree_aggregation_op: Optional[str] = None
        is_bst: bool = False
        is_validating_bst: bool = False
        bst_duplicate_policy: Optional[str] = "strictly_less"
        lca_query_type: Optional[str] = None
        tree_dp_type: Optional[str] = None
        is_diameter_query: bool = False
        is_path_sum_query: bool = False
        tree_node_count_n: int = 1000
        tree_max_depth_estimate: Optional[str] = None
        tree_recursion_risk: bool = False
        is_guaranteed_tree: bool = False
        graph_edge_count_e: Optional[int] = None
        has_cycle_signal: bool = False
        is_disconnected_signal: bool = False

        tree_text = re.sub(r'\b(?:fenwick\s+tree|binary\s+indexed\s+tree|segment\s+tree)\b', '', lower)
        is_tree_detected = bool(re.search(
            r'\b(?:tree|trees|binary\s+tree|bst|binary\s+search\s+tree|subtree|subtrees|leaf|leaves|root|ancestor|ancestors|descendant|descendants|lca|lowest\s+common\s+ancestor|preorder|inorder|postorder|level\s+order|tree\s+dp|k-ary\s+tree|n-ary\s+tree)\b',
            tree_text
        ))

        if is_tree_detected:
            # Guaranteed tree signal
            if re.search(r'given\s+a\s+tree|given\s+(?:the\s+)?root|tree\s+of\s+n\s+nodes|binary\s+tree\s+root|valid\s+tree\s+with\s+n', lower):
                is_guaranteed_tree = True

            # Graph cycle / disconnected signals
            if re.search(r'contain(?:s|ing)?\s+(?:a\s+)?cycle|cyclic|redundant\s+(?:connection|edge)|cycle\s+in\s+graph|e\s*>=\s*n|e\s*>=\s*v', lower):
                has_cycle_signal = True
            if re.search(r'disconnected|forest|multiple\s+components|unconnected|e\s*<\s*n\s*-\s*1', lower):
                is_disconnected_signal = True

            # Tree kind
            if re.search(r'without\s+bst|not\s+(?:a\s+)?bst|arbitrary\s+(?:unordered\s+)?binary\s+tree|unordered\s+binary\s+tree|non-bst', lower):
                tree_kind = TreeKind.BINARY_TREE
                is_bst = False
            elif re.search(r'bst|binary\s+search\s+tree|ordered-branch\s+elimination', lower):
                tree_kind = TreeKind.BST
                is_bst = True
            elif re.search(r'binary\s+tree|left\s+and\s+right|treenode|left\s+child|right\s+child|inorder', lower):
                tree_kind = TreeKind.BINARY_TREE
            else:
                tree_kind = TreeKind.ROOTED_TREE

            # BST validation vs BST operations
            if re.search(r'validate\s+bst|valid\s+(?:binary\s+search\s+tree|bst)|is_valid_bst|check\s+if.*(?:valid\s+)?bst|verify.*bst', lower):
                is_validating_bst = True
                is_bst = True
                tree_kind = TreeKind.BST

            # BST duplicate policy
            if re.search(r'allow\s+duplicates?\s+(?:in\s+|on\s+)?left|left.*duplicate', lower):
                bst_duplicate_policy = "allow_duplicates_left"
            elif re.search(r'allow\s+duplicates?\s+(?:in\s+|on\s+)?right|right.*duplicate', lower):
                bst_duplicate_policy = "allow_duplicates_right"
            elif re.search(r'count\s+(?:in|field)|node\s+frequency|multiplicity\s+in\s+node', lower):
                bst_duplicate_policy = "count_in_node"
            else:
                bst_duplicate_policy = "strictly_less"

            # Tree representation
            has_no_parent_pointers = bool(re.search(r'without\s+parent\s+pointers?|no\s+parent\s+pointers?|lack(?:ing)?\s+parent\s+pointers?', lower))
            if not has_no_parent_pointers and re.search(r'parent\s+array|parent\[i\]|parent\s+pointer', lower):
                tree_representation = TreeRepresentation.PARENT_ARRAY
            elif re.search(r'edges?\s+list|undirected\s+edges?|given\s+n\s+nodes?\s+and\s+edges?', lower):
                tree_representation = TreeRepresentation.EDGE_LIST
            elif re.search(r'adjacency\s+list|neighbors|adj\[u\]', lower):
                tree_representation = TreeRepresentation.ADJACENCY_LIST
            elif tree_kind in (TreeKind.BINARY_TREE, TreeKind.BST) or re.search(r'treenode|root|left|right', lower):
                tree_representation = TreeRepresentation.BINARY_POINTERS
            else:
                tree_representation = TreeRepresentation.ADJACENCY_LIST

            # Traversal order
            if re.search(r'pre-?order|root\s+left\s+right|root.*before.*children', lower):
                tree_traversal_order = TreeTraversalOrder.PREORDER
            elif re.search(r'in-?order|left\s+root\s+right', lower):
                tree_traversal_order = TreeTraversalOrder.INORDER
            elif re.search(r'post-?order|left\s+right\s+root|child(?:ren|\s+subtrees?)?.*before.*(?:parent\s+)?root|bottom-?up\s+(?:traversal|order|evaluation)|teardown\s+order', lower):
                tree_traversal_order = TreeTraversalOrder.POSTORDER
            elif re.search(r'level-?order|bfs\s+traversal|breadth\s+first|by\s+levels?', lower):
                tree_traversal_order = TreeTraversalOrder.LEVEL_ORDER

            # Aggregations & Metrics
            if re.search(r'diameter|longest\s+path\s+between\s+(?:any\s+)?two\s+nodes', lower):
                is_diameter_query = True
                tree_aggregation_op = "diameter"
            elif re.search(r'max\s+path\s+sum|maximum\s+path\s+sum|root\s+to\s+leaf\s+path\s+sum|path\s+sum', lower):
                is_path_sum_query = True
                tree_aggregation_op = "path_sum"
            elif re.search(r'max\s+depth|maximum\s+depth|height\s+of\s+(?:the\s+)?tree|tree\s+height', lower):
                tree_aggregation_op = "height"
            elif re.search(r'subtree\s+size|size\s+of\s+(?:each\s+)?subtree|count\s+(?:nodes\s+in\s+)?subtrees?', lower):
                tree_aggregation_op = "size"
            elif re.search(r'leaf\s+count|count\s+(?:the\s+)?leaves|number\s+of\s+leaves|number\s+of\s+leaf\s+nodes', lower):
                tree_aggregation_op = "leaf_count"
            elif re.search(r'subtree\s+sum|sum\s+of\s+(?:all\s+)?nodes?\s+in\s+subtree', lower):
                tree_aggregation_op = "sum"
            elif re.search(r'subtree\s+min|minimum\s+in\s+subtree', lower):
                tree_aggregation_op = "min"
            elif re.search(r'subtree\s+max|maximum\s+in\s+subtree', lower):
                tree_aggregation_op = "max"
            elif re.search(r'subtree\s+aggregation|aggregate\s+subtree|state\s+recurrence', lower):
                tree_aggregation_op = "subtree_aggregation"

            # LCA queries
            if re.search(r'lowest\s+common\s+ancestor|lca', lower):
                if is_bst or tree_kind == TreeKind.BST:
                    lca_query_type = "bst"
                elif not has_no_parent_pointers and (tree_representation == TreeRepresentation.PARENT_ARRAY or re.search(r'parent\s+array', lower)):
                    lca_query_type = "parent_array"
                else:
                    lca_query_type = "binary_tree"

            # Tree DP queries
            if re.search(r'independent\s+set|house\s+robber\s+(?:iii|in\s+tree)|adjacent\s+nodes?\s+cannot\s+both\s+be\s+chosen', lower):
                tree_dp_type = "independent_set"
            elif re.search(r'subtree\s+weight|optimal\s+subtree\s+selection|maximum\s+weight\s+(?:contiguous\s+)?subtree', lower):
                tree_dp_type = "subtree_weight"
            elif re.search(r'two\s+state\s+tree\s+dp|vertex\s+cover\s+on\s+tree|include\s+or\s+exclude\s+each\s+node', lower):
                tree_dp_type = "two_state"

            # Recursion risk & depth analysis
            if re.search(r'10\^5|100000|100,000|skewed|chain\s+tree|worst-case\s+depth|deep\s+tree', lower):
                tree_node_count_n = 100000
                if re.search(r'balanced|avl|red-black|complete\s+binary\s+tree', lower):
                    tree_max_depth_estimate = "balanced_log_n"
                    tree_recursion_risk = False
                else:
                    tree_max_depth_estimate = "skewed_n"
                    tree_recursion_risk = True
            elif re.search(r'balanced|avl|red-black|complete\s+binary\s+tree', lower):
                tree_max_depth_estimate = "balanced_log_n"
                tree_recursion_risk = False
            else:
                tree_max_depth_estimate = "balanced_log_n"
                tree_recursion_risk = False


            if input_structure == 'other':
                input_structure = 'binary_tree' if tree_kind == TreeKind.BINARY_TREE else 'tree'

        # ── 14. Graph Features Extraction (Phase 3F) ──
        # Graph detection — must NOT trigger on purely tree-specific problems
        # Tree problems route to Tree domain; Graph domain handles general graphs
        is_graph_detected: bool = False
        graph_kind: Optional[GraphKind] = None
        graph_weight_kind: Optional[GraphWeightKind] = None
        graph_representation_gf: Optional[GraphRepr] = None
        graph_has_negative_weights: bool = False
        graph_has_negative_cycles: bool = False
        graph_is_directed: bool = False
        graph_is_weighted: bool = False
        graph_is_cyclic: Optional[bool] = None
        graph_is_dag: Optional[bool] = None
        graph_is_bipartite: Optional[bool] = None
        graph_is_disconnected: Optional[bool] = None
        graph_vertex_count_v: int = 100
        graph_query_type: Optional[str] = None
        graph_algorithm_family: Optional[str] = None
        graph_index_base: Optional[int] = None
        computational_budget: float = 1.0e8

        # Primary graph detection: explicit graph keywords, but only route to Graph
        # (not Tree) if graph-specific operations are requested.
        # Tree is preserved when tree invariants and tree-specific ops are described.
        _is_graph_keyword = bool(re.search(
            r'\bgraph\b|\bdigraph\b|\bdag\b|(?:unweighted|undirected|weighted|directed|computer|social|road|route|circuit|task|telecommunication|optical|transport(?:ation)?)\s+network|\bnetwork\s+(?:connections?|flow|topology|nodes?|vertices|edges?|graph)\b|vertices?\s+and\s+edges?|\bvertices\b|\bvertex\b|'
            r'adjacency\s+(?:list|matrix)|directed\s+(?:graph|acyclic)|'
            r'shortest\s+path|minimum\s+(?:number\s+of\s+)?edges|topological\s+(?:sort|order)|strongly\s+connected|minimum\s+spanning\s+tree|'
            r'union[\s-]find|disjoint\s+set|\bdsu\b|bipartite|2[\s-]color|bridges?|articulation\s+point|cut\s+vert(?:ex|ices)|'
            r'\bscc\b|\bmst\b|bellman[- ]ford|dijkstra|floyd[\s-]warshall|all[\s-]pairs|pairwise|'
            r'connected\s+components?|cycle\s+detection|detect.*cycle|contains?.*cycle|has.*cycle|\bcyclic\b|\bcycles?\b|'
            r'kahn\'?s|kruskal|prim\'?s|condensation\s+dag|\bdfs\b|\bbfs\b|depth[\s-]first|breadth[\s-]first|'
            r'telecommunication|substations?|power\s+grid|deadlock|precedence|prerequisites?|dependencies|'
            r'server\s+enclaves|mutual\s+reachability|antennas?|two\s+frequencies|depot|hubs?|fewest\s+route|'
            r'communication|\bphone\s+lines\b|isolated\s+(?:regional\s+)?(?:clusters?|groups?|islands?|components?)|friend\s+clusters?',
            lower
        ))

        # Tree-specific signals that should override graph routing (excluding MST / spanning tree)
        _tree_specific_ops = bool(is_tree_detected and not re.search(r'spanning\s+tree|\bmst\b|kruskal|prim', lower) and re.search(
            r'lca|lowest\s+common\s+ancestor|bst|binary\s+search\s+tree|inorder|postorder|preorder|'
            r'level\s+order|leaves|leaf|root|subtree|tree\s+traversal|traversal\s+on\s+tree|'
            r'tree\s+dp|tree\s+diameter|path\s+sum|tree\s+height|tree\s+depth|height\s+of\s+(?:the\s+)?tree|depth\s+of\s+(?:the\s+)?tree|'
            r'k-ary\s+tree|binary\s+tree|parent\s+array',
            lower
        ))

        if _is_graph_keyword and not _tree_specific_ops:
            is_graph_detected = True

            # Directed vs undirected
            if re.search(r'\bdirected\b|digraph|\bu\s*->\s*v\b|one[\s-]way|directed\s+edge|\bdag\b|\bdeadlock\b|\bprecedence\b|\bprerequisite\b|\bdependencies\b', lower):
                graph_is_directed = True
                graph_kind = GraphKind.DIRECTED
            elif re.search(r'\bundirected\b|bidirectional|two[\s-]way|u[\s-]+v\s+is\s+an\s+edge|optical|substations?|power\s+grid|antennas?', lower):
                graph_is_directed = False
                graph_kind = GraphKind.UNDIRECTED
            # else: UNKNOWN — do not assume

            # Weighted vs unweighted
            is_explicitly_unweighted = bool(re.search(r'\bunweighted\b|without\s+weights?|unit\s+weights?|no\s+weights?', lower))
            has_weight_keywords = bool(re.search(r'(?<!un)\bweight(?:ed|s)?\b|(?<!un)weighted\s+graph|edge\s+weight|edge\s+cost|\bcosts?\b|\bdistances?\b|\blength\b|\blatenc(?:y|ies)\b|\bdelays?\b|\bdurations?\b|\bfees?\b|\bexpenditure\b|\btransit\b', lower))
            if has_weight_keywords and not is_explicitly_unweighted:
                graph_is_weighted = True
                # Negative weight detection (ensure non-negative is not matched as negative)
                has_neg_mention = bool(re.search(r'(?<!non[- ])(?<!not\s)(?<!no\s)\bnegative\s+(?:weight|edge|cost|cycle|value|number|fee)|weight\s+can\s+be\s+negative|allow(?:s|ing)?\s+negative', lower))
                is_explicitly_non_neg = bool(re.search(r'non[- ]negative|all\s+(?:edge\s+)?weights?\s+(?:are\s+)?positive|positive\s+(?:edge\s+)?weights?|w\s*>=\s*0|weight\s*>=\s*0', lower))
                if has_neg_mention and not is_explicitly_non_neg:
                    graph_has_negative_weights = True
                    # Negative cycle: only if explicitly stated
                    if re.search(r'(?<!no\s)negative\s+cycle|negative[\s-]weight\s+cycle|cycle\s+with\s+negative|infinite\s+value\s+accumulation|arbitrage', lower):
                        graph_has_negative_cycles = True
                    graph_weight_kind = GraphWeightKind.NEGATIVE_WEIGHTED
                else:
                    graph_weight_kind = GraphWeightKind.NON_NEGATIVE_WEIGHTED
            else:
                graph_is_weighted = False
                graph_weight_kind = GraphWeightKind.UNWEIGHTED

            # Graph representation
            if re.search(r'adjacency\s+matrix|\bmatrix\[u\]\[v\]|w\[u\]\[v\]', lower):
                graph_representation_gf = GraphRepr.ADJACENCY_MATRIX
            elif re.search(r'edge\s+list|list\s+of\s+edges?|edges?\s+given\s+as\s+pairs?', lower):
                graph_representation_gf = GraphRepr.EDGE_LIST
            else:
                graph_representation_gf = GraphRepr.ADJACENCY_LIST  # default

            # DAG detection
            if re.search(r'\bdag\b|directed\s+acyclic\s+graph|acyclic\s+directed|\bacyclic\s+(?:task\s+)?network\b|\bacyclic\b', lower):
                graph_is_dag = True
                graph_is_directed = True
                graph_kind = GraphKind.DIRECTED
                graph_is_cyclic = False
            elif re.search(r'topological\s+(?:sort|order|ordering)', lower):
                # Topological sort implies DAG assumption
                graph_is_dag = True
                graph_is_directed = True

            # Cyclic detection
            if re.search(r'(?<!a)\bcyclic\b|contains?\s+(?:a\s+)?cycle|has\s+(?:a\s+)?cycle|\bcycle\s+exists\b|\bdeadlock\b', lower) and not re.search(r'\bacyclic\b', lower):
                graph_is_cyclic = True
                graph_is_dag = False

            # Connectivity / bipartite / disconnected
            if re.search(r'\bbipartite\b|2[\s-]colorable|two[\s-]colorable|can\s+be\s+colored\s+with\s+2|two\s+frequencies', lower):
                graph_is_bipartite = True  # to be confirmed by algorithm
            if re.search(r'\bdisconnected\b|multiple\s+connected\s+components?|not\s+necessarily\s+connected', lower):
                graph_is_disconnected = True
            elif re.search(r'connected\s+graph|connected\s+undirected|guaranteed\s+connected', lower):
                graph_is_disconnected = False

            # Vertex count estimation
            v_match = re.search(r'(?:v|n)\s*(?:<=|=|≤)\s*([\d,]+)', lower)
            if v_match:
                try:
                    graph_vertex_count_v = int(v_match.group(1).replace(',', ''))
                except ValueError:
                    pass
            elif re.search(r'10\^5|100000|100,000', lower):
                graph_vertex_count_v = 100000
            elif re.search(r'10\^4|10000', lower):
                graph_vertex_count_v = 10000
            elif re.search(r'10\^3|1000', lower):
                graph_vertex_count_v = 1000
            elif re.search(r'\b(?:400|500)\b', lower):
                graph_vertex_count_v = 500
            elif re.search(r'\bsmall\b', lower):
                graph_vertex_count_v = 50

            # Indexing interpretation: ONLY if explicitly established by problem specification.
            # ZERO inference from observed vertex values (e.g. absence of vertex 0 must not infer 1-indexed).
            if re.search(r'\b0[\s-]based\b|\b0[\s-]indexed\b|vertices\s+(?:numbered\s+)?0\s+to\s+n\s*-\s*1|from\s+0\s+to\s+n\s*-\s*1|indexed\s+from\s+0', lower):
                graph_index_base = 0
            elif re.search(r'\b1[\s-]based\b|\b1[\s-]indexed\b|vertices\s+(?:numbered\s+)?1\s+to\s+n\b|from\s+1\s+to\s+n\b|indexed\s+from\s+1', lower):
                graph_index_base = 1
            else:
                graph_index_base = None

            # Computational budget derived from time limit when specified (default 1.0e8 ops ~ 1s)
            time_match = re.search(r'time\s+limit[:\s]+([\d\.]+)\s*(?:s|sec|seconds?)', lower)
            if time_match:
                try:
                    computational_budget = float(time_match.group(1)) * 1.0e8
                except ValueError:
                    pass

            # Query type classification (ordered by specificity)
            if re.search(r'dag\s+dp|longest\s+(?:completion\s+time\s+)?path|critical\s+path|dp\s+on\s+dag|dynamic\s+programming\s+on\s+(?:a\s+)?dag', lower):
                graph_query_type = "dag_dp"
                graph_algorithm_family = "graph_dag_dp"
            elif re.search(r'floyd[\s-]warshall|all[\s-]pairs|between\s+all\s+pairs|every\s+pair|pairwise.*(?:distance|travel|transit)|distance\s+matrix', lower):
                graph_query_type = "shortest_path"
                graph_algorithm_family = "graph_floyd_warshall"
            elif re.search(r'dijkstra', lower):
                graph_query_type = "shortest_path"
                graph_algorithm_family = "graph_dijkstra"
            elif re.search(r'bellman[\s-]ford|negative\s+cycle|negative[\s-]weight\s+cycle|cycle\s+with\s+negative|infinite\s+value\s+accumulation|arbitrage|devaluation\s+loop', lower):
                graph_query_type = "shortest_path"
                graph_algorithm_family = "graph_bellman_ford"
            elif re.search(r'minimum\s+spanning\s+tree|\bmst\b|kruskal|prim|link\s+all\s+.*together.*(?:minimizing|minimum)|connect\s+all\s+.*(?:minimizing|minimum)|minimum\s+(?:total\s+)?(?:cost|expenditure|trenching|wiring)\s+to\s+connect|minimum\s+spanning\s+forest|\bmsf\b', lower):
                graph_query_type = "mst"
                if re.search(r'prim', lower):
                    graph_algorithm_family = "graph_mst_prim"
                else:
                    graph_algorithm_family = "graph_mst_kruskal"
            elif re.search(r'union[\s-]find|disjoint[\s-]set|\bdsu\b|dynamic\s+connectivity|are\s+(?:u\s+and\s+v|two\s+nodes?)\s+connected', lower):
                graph_query_type = "dsu"
                graph_algorithm_family = "graph_dsu"
            elif re.search(r'\bscc\b|strongly\s+connected|tarjan\s+(?:scc|algorithm)?|mutual\s+reachability|consensus\s+server\s+enclaves|server\s+enclaves', lower):
                graph_query_type = "scc"
                graph_algorithm_family = "graph_scc_tarjan"
            elif re.search(r'bridges?|articulation\s+point|cut\s+vert(?:ex|ices)|critical\s+(?:node|edge|connection|link|backbone)|vulnerable\s+(?:link|backbone)|severance.*partition|severance.*disconnect', lower):
                graph_query_type = "bridges_articulation"
                graph_algorithm_family = "graph_bridges_articulation"
            elif re.search(r'topological\s+(?:sort|order)|dependency\s+order|build\s+order|prerequisite\s+(?:sequence|order)|execution\s+order|assembly\s+steps?|precedence', lower):
                graph_query_type = "topological"
                graph_algorithm_family = "graph_topological_sort"
            elif re.search(r'shortest\s+path|shortest\s+route|nearest\s+node|fewest\s+(?:\w+\s+)?(?:edges?|stops?|hops?|steps?|transfers?)|minimum\s+(?:number\s+of\s+)?(?:\w+\s+)?(?:edges?|stops?|hops?|steps?|transfers?)|minimum\s+(?:distance|cost|latency|time|delay|weight)|cheapest\s+(?:path|route|way)|fastest\s+(?:route|path|way)|min\s+(?:distance|cost|latency|time|delay)', lower):
                graph_query_type = "shortest_path"
                if not graph_is_weighted:
                    graph_algorithm_family = "graph_bfs_shortest_path"
                elif graph_has_negative_weights:
                    graph_algorithm_family = "graph_bellman_ford"
                elif graph_is_dag:
                    graph_algorithm_family = "graph_dag_dp"
                else:
                    graph_algorithm_family = "graph_dijkstra"
            elif re.search(r'cycle\s+detection|detect.*cycle|contains?.*cycle|has.*cycle|whether.*cycles?|(?<!a)\bcyclic\b|\bcycles?\b|\bloop\b|\bdeadlock\b|circular\s+(?:dependency|wait)', lower) and not re.search(r'\bno\s+(?:negative\s+)?cycles?\b|\bwithout\s+cycles?\b|\bcontains\s+no\s+cycles?\b', lower):
                graph_query_type = "cycle"
                if graph_is_directed or graph_kind == GraphKind.DIRECTED:
                    graph_algorithm_family = "graph_cycle_detection_directed"
                else:
                    graph_algorithm_family = "graph_cycle_detection_undirected"
            elif re.search(r'\bbipartite\b|2[\s-]color|two[\s-]color|opposing\s+teams?|team\s+partition|two\s+frequencies|no\s+two\s+adjacent.*share\s+the\s+same', lower):
                graph_query_type = "bipartite"
                graph_algorithm_family = "graph_bipartite_coloring"
            elif re.search(r'connected\s+components?|count\s+components?|number\s+of\s+(?:connected\s+)?components|friend\s+clusters?|isolated\s+(?:\w+\s+)*(?:clusters?|groups?|circles?|islands?|components?)|count\s+(?:the\s+)?number\s+of\s+(?:\w+\s+)*(?:clusters?|groups?|islands?|components?)', lower):
                graph_query_type = "components"
                graph_algorithm_family = "graph_connected_components"
            elif re.search(r'reachab(?:le|ility)|can\s+reach|is\s+there\s+(?:a\s+)?path', lower):
                graph_query_type = "reachability"
                graph_algorithm_family = "graph_dfs_traversal"
            else:
                graph_query_type = "traversal"
                graph_algorithm_family = "graph_dfs_traversal"

            if input_structure == 'other':
                input_structure = 'graph'

        # ── 15. Heap / Priority Queue Domain Recognition (Phase 3G) ──
        is_heap_detected: bool = False
        heap_kind: Optional[HeapKind] = None
        heap_operation_kind: Optional[HeapOperationKind] = None
        heap_k_direction: Optional[str] = None
        heap_k_value: Optional[int] = None
        heap_is_streaming: bool = False
        heap_is_dynamic_median: bool = False
        heap_is_k_way_merge: bool = False
        heap_is_scheduling: bool = False
        heap_is_greedy_selection: bool = False
        heap_is_lazy_deletion: bool = False
        heap_requires_arbitrary_delete: bool = False
        heap_requires_full_sort: bool = False
        heap_is_offline_kth: bool = False
        heap_algorithm_family: Optional[str] = None

        # Check for arbitrary deletion / search (heap anti-pattern)
        if re.search(r'delete\s+(?:an?\s+)?arbitrary|arbitrary\s+(?:element\s+)?deletion|remove\s+by\s+value|search\s+for\s+(?:arbitrary\s+)?key|lookup\s+arbitrary', lower):
            heap_requires_arbitrary_delete = True

        # Check for full offline sort requirement
        if re.search(r'sort\s+the\s+entire\s+array|complete\s+(?:array\s+)?sort|full\s+lexicographical\s+sort|output\s+all\s+elements\s+in\s+sorted\s+order', lower) and not re.search(r'stream|dynamic|online|top[\s-]k|heap', lower):
            heap_requires_full_sort = True

        # Primary heap signals: dynamic candidate set, priority queue, extremal selection
        _is_heap_keyword = bool(re.search(
            r'\bheap(?:ify)?\b|\bpriority\s*queue\b|\bmin[\s-]heap\b|\bmax[\s-]heap\b|'
            r'\btop[\s-]?(?:k|\d+)\b|(?:\b\d+\b|\bk\b)\s+(?:largest|smallest|most\s+frequent|least\s+frequent|cheapest)|'
            r'\b(?:k-?th|kth|\d+-?(?:st|nd|rd|th))\b[\s-]*(?:largest|smallest|minimum|maximum|element)\b|'
            r'k[\s-]way\s+merge|merge\s+(?:multiple|k|\d+)?\s*(?:sorted\s+)?(?:\w+\s+)?(?:arrays?|lists?|streams?|sequences?|logs?|files?|lines?)|'
            r'median\s+from\s+(?:a\s+)?(?:data\s+)?stream|(?:dynamic|running|continuous|stream)\s+(?:\w+\s+)?median|two\s+heaps|dual\s+heaps?|'
            r'meeting\s+rooms?(?:\s+ii)?|minimum\s+(?:number\s+of\s+)?conference\s+rooms|cpu\s+task\s+scheduling|'
            r'schedule\s+tasks?|task\s+schedul(?:ing|er)|concurrent\s+servers?|parallel\s+(?:virtual\s+)?machines?|interval\s+scheduling|'
            r'start\s+and\s+(?:completion\s+)?end\s+times?|'
            r'connect\s+(?:all\s+)?(?:ropes?|sticks?|spools?|cables?)|merge\s+(?:ropes?|sticks?|spools?)|(?:greedy\s+)?merge\s+cost|splicing|huffman|greedy\s+(?:selection|choice).*extrem(?:um|al)|'
            r'lazy\s+deletion|stale\s+elements?|delayed\s+removal|canceled\s+orders?|tombstone|soft\s+delete|dijkstra\s+priority|pq\b|'
            r'always\s+extract|(?:insert|support\s+inserting).*extract|extract\s+(?:the\s+)?(?:highest|maximum|lowest|minimum)',
            lower
        ))

        # Do NOT route to Heap if Graph or Tree domain is clearly indicated, or if Fenwick cues present without explicit heap keyword
        _is_fenwick_cues = bool(re.search(r'\b(?:fenwick|binary\s+indexed|bit\b|binary\s+lifting|multiset|order\s+statistic)\b', lower))
        _is_explicit_heap = bool(re.search(r'\bheap(?:ify)?\b|\bpriority\s*queue\b', lower))
        _is_pure_heap = _is_heap_keyword and not is_graph_detected and not (is_tree_detected and not _is_explicit_heap) and not (_is_fenwick_cues and not _is_explicit_heap)

        if (_is_pure_heap or (_is_heap_keyword and not is_graph_detected)) and not (_is_fenwick_cues and not _is_explicit_heap):
            is_heap_detected = True

            # Streaming vs offline
            if re.search(r'stream|running|dynamic|online|elements\s+arrive|incoming', lower):
                heap_is_streaming = True

            # Extract K value if present
            k_match = re.search(r'\b(?:top|first|find)\s+(\d+)\b|\b(\d+)(?:-?(?:st|nd|rd|th))?\b', lower)
            if k_match:
                for grp in k_match.groups():
                    if grp:
                        try:
                            heap_k_value = int(grp)
                            break
                        except ValueError:
                            pass

            # Detect K direction (based on query target, not the heap type)
            if re.search(r'top[\s-]?(?:k|\d+)?\s*(?:smallest|minimum|min|least|lowest|cheapest)|(?:\bk\b|\b\d+\b)?\s*(?:smallest|minimum|min|least|lowest|cheapest)\s*(?:elements?|integers?|values?|numbers?|threshold)|\b(?:k|\d+)(?:-?(?:st|nd|rd|th))\b[\s-]*(?:smallest|minimum|min|least|lowest)', lower):
                heap_k_direction = "smallest"
            elif re.search(r'top[\s-]?(?:k|\d+)?\s*(?:largest|maximum|max|greatest|highest|most)|(?:\bk\b|\b\d+\b)?\s*(?:largest|maximum|max|greatest|highest|most)\s*(?:elements?|integers?|values?|numbers?|threshold)|\b(?:k|\d+)(?:-?(?:st|nd|rd|th))\b[\s-]*(?:largest|maximum|max|greatest|highest)', lower):
                heap_k_direction = "largest"
            elif re.search(r'smallest|minimum|least|lowest|cheapest', lower):
                heap_k_direction = "smallest"
            elif re.search(r'largest|maximum|greatest|highest|most\s+frequent', lower):
                heap_k_direction = "largest"

            # Classify Heap Pattern
            if re.search(r'median\s+from\s+(?:a\s+)?(?:data\s+)?stream|(?:dynamic|running|continuous|stream)\s+(?:\w+\s+)?median|find\s+median', lower):
                heap_is_dynamic_median = True
                heap_algorithm_family = "heap_dynamic_median"
            elif re.search(r'two\s+heaps|dual\s+heaps?', lower):
                heap_algorithm_family = "heap_two_heaps"
            elif re.search(r'k[\s-]way\s+merge|merge\s+(?:multiple|k|\d+)?\s*(?:sorted\s+)?(?:\w+\s+)?(?:arrays?|lists?|streams?|sequences?|logs?|files?|lines?)|merge\s+multiple\s+sorted', lower):
                heap_is_k_way_merge = True
                heap_kind = HeapKind.MIN_HEAP
                heap_algorithm_family = "heap_k_way_merge"
            elif re.search(r'lazy\s+deletion|stale\s+elements?|tombstone|soft\s+delete|delayed\s+removal|canceled\s+orders?', lower):
                heap_is_lazy_deletion = True
                heap_algorithm_family = "heap_lazy_deletion"
            elif re.search(r'meeting\s+rooms|conference\s+rooms|cpu\s+task\s+scheduling|task\s+schedul(?:ing|er)|schedule\s+tasks|concurrent\s+servers?|parallel\s+(?:virtual\s+)?machines?|interval\s+scheduling|start\s+and\s+(?:completion\s+)?end\s+times?', lower):
                heap_is_scheduling = True
                heap_kind = HeapKind.MIN_HEAP
                heap_algorithm_family = "heap_scheduling"
            elif re.search(r'connect\s+(?:all\s+)?(?:ropes?|sticks?|spools?|cables?)|merge\s+(?:ropes?|sticks?|spools?)|(?:greedy\s+)?merge\s+cost|splicing|huffman|stone\s+weight|greedy\s+(?:selection|choice)|repeatedly\s+(?:combine|merge)\s+(?:two\s+)?smallest', lower):
                heap_is_greedy_selection = True
                heap_kind = HeapKind.MIN_HEAP
                heap_algorithm_family = "heap_greedy_selection"
            elif re.search(r'\b(?:k|\d+)-?(?:st|nd|rd|th)\b|\b(?:k|\d+)-?(?:st|nd|rd|th)\s+(?:largest|smallest|minimum|maximum|element)', lower):
                heap_algorithm_family = "heap_kth_element"
                if not heap_is_streaming and re.search(r'static\s+array|given\s+an\s+array|in\s+the\s+array', lower):
                    heap_is_offline_kth = True
                if heap_k_direction == "smallest":
                    heap_kind = HeapKind.MAX_HEAP
                else:
                    heap_kind = HeapKind.MIN_HEAP
            elif re.search(r'top[\s-]?(?:k|\d+)|\b(?:k|\d+)\s+(?:largest|smallest|most\s+frequent|least\s+frequent)', lower):
                heap_algorithm_family = "heap_top_k"
                if heap_k_direction == "smallest":
                    heap_kind = HeapKind.MAX_HEAP
                else:
                    heap_kind = HeapKind.MIN_HEAP
            elif re.search(r'build\s+heap|floyd\s+heapify|bottom[\s-]up\s+heapify|convert\s+array\s+to\s+heap|bottom[\s-]up\s+heap', lower):
                heap_algorithm_family = "heap_build"
                if re.search(r'max', lower):
                    heap_kind = HeapKind.MAX_HEAP
                else:
                    heap_kind = HeapKind.MIN_HEAP
            elif re.search(r'max[\s-]?(?:priority\s*queue|heap)|maximum\s+priority|extract[\s-]max|priority_queue_max|pop\s+maximum|\bmax\b.*\b(?:priority\s*queue|heap)\b|extract.*maximum|extract.*highest', lower):
                heap_kind = HeapKind.MAX_HEAP
                heap_algorithm_family = "heap_max_priority_queue"
            elif re.search(r'min[\s-]?(?:priority\s*queue|heap)|minimum\s+priority|extract[\s-]min|priority_queue_min|pop\s+minimum|\bmin\b.*\b(?:priority\s*queue|heap)\b|extract.*minimum|extract.*lowest', lower):
                heap_kind = HeapKind.MIN_HEAP
                heap_algorithm_family = "heap_min_priority_queue"
            else:
                if re.search(r'\bmax\b|maximum|highest|greatest', lower):
                    heap_kind = HeapKind.MAX_HEAP
                    heap_algorithm_family = "heap_max_priority_queue"
                else:
                    heap_kind = HeapKind.MIN_HEAP
                    heap_algorithm_family = "heap_min_priority_queue"

            if input_structure == 'single_sequence':
                input_structure = 'heap'

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 16. Disjoint Set Union (DSU) Semantic Feature Extraction (Phase 3H)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        is_dsu_detected: bool = False
        dsu_kind: Optional[DSUKind] = None
        dsu_operation_kind: Optional[DSUOperationKind] = None
        dsu_algorithm_family: Optional[str] = None
        dsu_has_metadata: bool = False
        dsu_metadata_type: Optional[str] = None
        dsu_has_weights: bool = False
        dsu_has_parity: bool = False
        dsu_requires_rollback: bool = False
        dsu_is_offline: bool = False
        dsu_has_deletions: bool = False
        dsu_is_online_deletions: bool = False
        dsu_has_difference_query: bool = False
        dsu_has_contradiction_check: bool = False
        dsu_historical_queries: bool = False

        # Deletions / Removal detection
        if re.search(r'delete\s+(?:an?\s+)?edge|remove\s+(?:an?\s+)?edge|edge\s+deletion|disconnect\s+edge|cut\s+edge|delet(?:e|ing)\s+connections?', lower):
            dsu_has_deletions = True

        # Offline vs online detection
        if re.search(r'without\s+offline|arbitrary\s+online', lower):
            dsu_is_online_deletions = True
        elif re.search(r'offline\s+(?:dynamic\s+)?connectivity|segment\s+tree\s+over\s+time|all\s+queries\s+known\s+in\s+advance|time\s+intervals?\s+for\s+edges?|active\s+(?:interval|time|duration)|offline\s+queries', lower):
            dsu_is_offline = True
        elif dsu_has_deletions and not re.search(r'\boffline\b|\bbatch\b|time\s+interval', lower):
            # Arbitrary online edge deletions -> anti-pattern for basic/rollback DSU
            dsu_is_online_deletions = True
        elif re.search(r'online\s+(?:cut|disconnect|delet)', lower):
            dsu_is_online_deletions = True

        # Rollback / Undo detection
        if re.search(r'rollback|undo\s+(?:the\s+)?(?:last\s+)?(?:operation|union|merge|action|edge)|snapshot|checkpoint|revert\s+to\s+(?:previous\s+)?state|historical\s+(?:state|version|query)', lower):
            dsu_requires_rollback = True
            if re.search(r'query\s+(?:at|in|after)\s+(?:snapshot|version|checkpoint|time\s+t)', lower):
                dsu_historical_queries = True

        # Weighted / Potential difference detection
        if re.search(r'potential\s+difference|relative\s+potential|potential\s+dsu|offset\s+to\s+root|relative\s+weight|weight\s+differences?|value\[?\w+\]?\s*-\s*value\[?\w+\]?|difference\s+between\s+(?:\w+\s+)?elements?|is\s+\d+\s+(?:heavier|taller|larger|more)\s+than|weighs\s+\d+\s+more\s+than|x\s*-\s*y\s*=|weighted\s+(?:dsu|union[\s-]find)', lower):
            dsu_has_weights = True
            if re.search(r'difference\s+quer(?:y|ies)|query\s+(?:potential\s+)?difference|potential\s+difference\s+quer(?:y|ies)|evaluat(?:e|ing)\s+difference\s+quer(?:y|ies)|find\s+difference', lower):
                dsu_has_difference_query = True

        # Parity / 2-coloring detection
        if re.search(r'parity\s+constraint|parity\s+dsu|color\[?\w+\]?\s*(?:xor|\^)\s*color|different\s+colors?|same\s+or\s+opposite|friends\s+or\s+enemies|opposite\s+parity|bipartite\s+(?:consistency|check|relation)|two[\s-]coloring\s+(?:consistency|constraint)|dynamic\s+bipartite', lower):
            dsu_has_parity = True

        # Contradiction / Consistency check detection
        if re.search(r'contradiction|consistent|inconsistent|conflicting\s+(?:constraints?|statements?|equations?)|detect\s+contradiction|check\s+consistency|verify\s+consistency', lower):
            dsu_has_contradiction_check = True

        # Difference constraints system detection
        if re.search(r'(?:system\s+of\s+)?difference\s+constraints?.*(?:consisten|inconsisten|contradict|conflict)|(?:detect|check|verify)\s+.*(?:difference\s+constraints?|conflicting\s+equations?|equations?.*consistency)|contradictory\s+difference\s+constraints?|difference\s+constraints?.*contradiction', lower):
            dsu_has_weights = True
            dsu_has_contradiction_check = True

        # Metadata detection
        if re.search(r'component\s+(?:metadata|size|sum|min|max|count|weight|value|maximum|minimum)|size\s+of\s+(?:the\s+|each\s+)?component|total\s+(?:weight|sum)\s+of\s+(?:the\s+|each\s+)?component|total\s+sum\s+and\s+size|largest\s+component|maximum\s+component\s+size|running\s+sum\s+and\s+extremum|extremum\s+of\s+merged', lower):
            dsu_has_metadata = True
            if re.search(r'sum|total\s+weight', lower):
                dsu_metadata_type = "sum"
            elif re.search(r'min|minimum', lower):
                dsu_metadata_type = "min"
            elif re.search(r'max|maximum|largest|extremum', lower):
                dsu_metadata_type = "max"
            elif re.search(r'size|count', lower):
                dsu_metadata_type = "size"
            elif re.search(r'xor', lower):
                dsu_metadata_type = "xor"

        # DSU keyword / pattern signals
        _is_dsu_keyword = bool(re.search(
            r'\bdisjoint\s+set\b|\bunion[\s-]find\b|\bdsu\b|'
            r'equivalence\s+(?:classes?|relations?)|'
            r'dynamic\s+connectivity|incremental\s+connectivity|'
            r'unite\s+(?:sets?|elements?|nodes?|vertices?)|'
            r'same\s+(?:set|component|group)|'
            r'are\s+(?:\w+\s+)?connected|'
            r'merge\s+(?:groups?|sets?|components?|clusters?|accounts?|subsets?)|'
            r'set\s+merg(?:e|ers?|ing)|'
            r'kruskal\s+support|dsu\s+support',
            lower
        ))

        # Explicit Phase 3H pattern signal (takes precedence over generic graph routing)
        _is_phase_3h_explicit = bool(
            (dsu_has_weights or dsu_has_parity or dsu_requires_rollback or dsu_is_offline or
             dsu_is_online_deletions or (dsu_has_metadata and dsu_metadata_type != "size") or
             re.search(r'equivalence\s+(?:classes?|relations?)|make_set|union\s+by\s+size|disjoint\s+subsets?|basic\s+dsu|set\s+merg(?:e|ers?|ing)|partition\s+elements|component\s+metadata|kruskal\s+support|dsu\s+support|online\s+dynamic\s+connectivity|incremental\s+dynamic\s+connectivity|incremental\s+connectivity\s+stream', lower))
            and not re.search(r'contiguous\s+subarray|subarray\s+min|subarray\s+max', lower)
        )

        if _is_phase_3h_explicit:
            is_graph_detected = False
            graph_algorithm_family = None
            graph_query_type = None

        _is_pure_graph_mst = bool(is_graph_detected and graph_query_type == "mst" and not re.search(r'kruskal\s+support|dsu\s+support', lower))
        _is_pure_graph_dsu = bool(is_graph_detected and graph_algorithm_family == "graph_dsu" and not _is_phase_3h_explicit)

        if (_is_dsu_keyword or _is_phase_3h_explicit or dsu_has_weights or dsu_has_parity or dsu_requires_rollback or dsu_is_offline or dsu_is_online_deletions) \
           and not (is_graph_detected and re.search(r'shortest\s+path|dijkstra|bellman|floyd|topological|scc|articulation|bipartite|matching|kuhn|flow|dinic|mcmf', lower)) \
           and not _is_pure_graph_mst \
           and not _is_pure_graph_dsu \
           and not bool(re.search(r'contiguous\s+subarray|subarray\s+min|subarray\s+max', lower)):
            is_dsu_detected = True

            if dsu_is_offline:
                dsu_kind = DSUKind.ROLLBACK
                dsu_algorithm_family = "dsu_offline_dynamic_connectivity"
            elif dsu_requires_rollback:
                dsu_kind = DSUKind.ROLLBACK
                dsu_algorithm_family = "dsu_rollback"
            elif dsu_has_parity:
                dsu_kind = DSUKind.PARITY
                if dsu_has_contradiction_check and not re.search(r'bipartite|coloring|odd[\s-]cycle|parity', lower):
                    dsu_algorithm_family = "dsu_constraint_consistency"
                else:
                    dsu_algorithm_family = "dsu_parity"
            elif dsu_has_contradiction_check and re.search(r'check\s+consistency|detect\s+contradict|verify\s+(?:whether\s+)?(?:system\s+of\s+)?(?:difference\s+)?constraints?\s+is\s+consistent|detect\s+conflicting\s+equations', lower):
                dsu_kind = DSUKind.WEIGHTED
                dsu_algorithm_family = "dsu_constraint_consistency"
            elif dsu_has_weights:
                dsu_kind = DSUKind.WEIGHTED
                if re.search(r'maintain\s+relative\s+potentials', lower):
                    dsu_algorithm_family = "dsu_weighted"
                elif dsu_has_difference_query:
                    dsu_algorithm_family = "dsu_potential_difference"
                else:
                    dsu_algorithm_family = "dsu_weighted"
            elif dsu_has_metadata and (dsu_metadata_type in ("sum", "min", "max", "xor") or re.search(r'component\s+metadata|metadata', lower)) and not re.search(r'\bbasic\s+dsu\b', lower):
                dsu_kind = DSUKind.BASIC
                dsu_algorithm_family = "dsu_component_metadata"
            elif re.search(r'kruskal\s+support|dsu\s+support', lower):
                dsu_kind = DSUKind.BASIC
                dsu_algorithm_family = "dsu_kruskal_support"
            elif re.search(r'incremental|connectivity|connected|query|add\s+connection|add\s+edge|stream', lower) and not re.search(r'\bbasic\s+dsu\b|make_set|equivalence\s+classes|disjoint\s+subsets', lower):
                dsu_kind = DSUKind.BASIC
                dsu_algorithm_family = "dsu_dynamic_connectivity"
            else:
                dsu_kind = DSUKind.BASIC
                dsu_algorithm_family = "dsu_basic"

            if input_structure == 'single_sequence':
                input_structure = 'dsu'

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 17. Fenwick Tree / Binary Indexed Tree Feature Extraction (Phase 3I)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        is_fenwick_detected: bool = False
        fenwick_kind: Optional[FenwickKind] = None
        fenwick_operation_kind: Optional[FenwickOperationKind] = None
        fenwick_algorithm_family: Optional[str] = None
        fenwick_has_point_update: bool = False
        fenwick_has_range_update: bool = False
        fenwick_has_point_query: bool = False
        fenwick_has_prefix_query: bool = False
        fenwick_has_range_query: bool = False
        fenwick_has_non_invertible_range: bool = False
        fenwick_is_frequency: bool = False
        fenwick_has_kth_query: bool = False
        fenwick_requires_coordinate_compression: bool = False
        fenwick_is_inversion_counting: bool = False
        fenwick_is_multiset: bool = False
        fenwick_is_2d: bool = False
        fenwick_is_extremum: bool = False
        fenwick_extremum_direction: Optional[str] = None
        fenwick_is_static: bool = False
        fenwick_is_offline_range_add: bool = False
        fenwick_has_range_assignment: bool = False
        fenwick_has_arbitrary_range_minmax: bool = False
        fenwick_has_dynamic_unknown_coords: bool = False
        fenwick_has_negative_frequencies: bool = False
        fenwick_resource_exceeded: bool = False

        # Explicit Fenwick keyword / structural trigger
        _is_fenwick_keyword = bool(re.search(
            r'\bfenwick\b|\bbinary\s+indexed\s+tree\b|\bbit\b|'
            r'prefix\s+aggregation\s+over\s+indexed\s+ranges|'
            r'lowbit|range\s+update\s+(?:and|&)\s+range\s+query|'
            r'point\s+update\s+(?:and|&)\s+range\s+query',
            lower
        ))

        # Detection of Fenwick operations and requirements
        _has_point_upd = bool(re.search(
            r'point\s+(?:update|add|increment|increase)|add\s+(?:val|value|\w+|\d+)\s+to\s+(?:index|element|position)|'
            r'update\s+(?:at|element|index|position|single|value)|increment\s+(?:element|at|index)|'
            r'modify\s+(?:element\s+at|single)|dynamic\s+point\s+modification|add\s+\w+\s+at\s+index|'
            r'cell\s+(?:update|addition|add|increment|point\s+modification|modification)|single\s+position\s+increment|point\s+modification|'
            r'single[\s-]point|single\s+positions?',
            lower
        ))
        _has_range_upd = bool(re.search(
            r'range\s+(?:update|add|increment)|add\s+(?:val|value|\w+|\d+)\s+to\s+(?:range|interval|elements?\s+from)|'
            r'increment\s+(?:range|interval|all\s+elements\s+in)|add\s+delta\s+to\s+\[|'
            r'interval\s+(?:addition|update|add|increment)s?|two-fenwick|range\s+addition|'
            r'altitude\s+spans|range\s+span|spans?\s+\[',
            lower
        ))
        _has_pref_query = bool(re.search(
            r'prefix\s+sum|cumulative\s+(?:sum|frequency|count)|sum\s+of\s+prefix|sum\s+from\s+(?:index\s+)?1\s+to\s+i|'
            r'prefix\s+query|sum\s+in\s+prefix|prefix\s+(?:\w+\s+){0,2}queries',
            lower
        ))
        _has_rng_query = bool(re.search(
            r'range\s+sum|sum\s+in\s+range|sum\s+of\s+elements?\s+(?:between|from|in\s+\[)|'
            r'query\s+(?:range|sum\s+in)|range\s+query',
            lower
        ))
        _has_point_qry = bool(re.search(
            r'point\s+(?:\w+\s+)?(?:query|queries|inquir)|point\s+value|value\s+at\s+index|inspect\s+element\s+at|query\s+element\s+at|find\s+element\s+at\s+index',
            lower
        ))

        if _has_point_upd:
            fenwick_has_point_update = True
        if _has_range_upd:
            fenwick_has_range_update = True
        if _has_point_qry:
            fenwick_has_point_query = True
        if _has_pref_query:
            fenwick_has_prefix_query = True
        if _has_rng_query:
            fenwick_has_range_query = True

        if re.search(r'non-invertible|without\s+inverse|range\s+gcd|range\s+matrix\s+mult|range\s+bitwise\s+(?:and|or)|range\s+product\s+without\s+inverse|arbitrary\s+range\s+query\s+requiring\s+subtraction.*no\s+suitable\s+inverse', lower):
            fenwick_has_non_invertible_range = True
            fenwick_has_prefix_query = True
        if _has_rng_query:
            fenwick_has_range_query = True

        # 2D detection
        if re.search(r'2d\s+(?:fenwick|bit|binary\s+indexed)|matrix\s+(?:point\s+update|submatrix|sum)|submatrix\s+(?:sum|query)|rectangle\s+sum|grid\s+(?:point\s+update|sum|queries)|2d\s+range\s+sum', lower):
            fenwick_is_2d = True

        # Frequency & rank detection
        if re.search(r'frequency\s+table|frequency\s+fenwick|count\s+elements?\s+(?:less\s+than|<=|<|greater)|number\s+of\s+elements?\s+<=|dynamic\s+frequency|rank\s+of\s+element|cumulative\s+frequency|frequency\s+count', lower):
            fenwick_is_frequency = True

        # K-th element detection (Fenwick binary lifting / quantile / order statistic / frequency BIT)
        if (re.search(r'binary\s+lifting|quantile\s+query|k-th\s+smallest\s+element\s+in\s+multiset', lower) or
            (re.search(r'order\s+statistic', lower) and (fenwick_is_frequency or _is_fenwick_keyword or fenwick_has_point_update)) or
            (re.search(r'k[\s-]*th\s+(?:\w+\s+)*(?:element|smallest|largest)|kth\s+smallest', lower) and (
                _is_fenwick_keyword or fenwick_is_frequency or re.search(r'binary\s+lifting|frequencies|frequency\s+array', lower)
            ))) and not _is_explicit_heap and not bool(re.search(r'quickselect', lower)):
            fenwick_has_kth_query = True
            fenwick_is_frequency = True
        elif re.search(r'allow\s+negative\s+counts?\s+for\s+k[\s-]th|negative\s+frequenc.*k[\s-]th|k[\s-]th.*negative\s+frequenc', lower):
            fenwick_has_kth_query = True
            fenwick_has_negative_frequencies = True

        # Coordinate compression detection
        if re.search(r'coordinate\s+compression|coordinates?\s+up\s+to\s+10\^|sparse\s+coordinates?|large\s+coordinates?|values\s+up\s+to\s+10\^9|relative\s+ranking\s+of\s+values|rank\s+compression|compress\s+coordinates', lower):
            fenwick_requires_coordinate_compression = True

        # Inversion counting detection
        if re.search(r'inversion\s+count|count\s+inversions?|number\s+of\s+inversions?|count\s+pairs\s+(?:with\s+)?i\s*<\s*j\s+and\s+a\[i\]\s*>\s*a\[j\]|count\s+elements?\s+greater\s+than\s+a\[i\]\s+to\s+the\s+left|greater\s+elements?\s+before', lower):
            fenwick_is_inversion_counting = True
            fenwick_is_frequency = True

        # Dynamic multiset detection
        if re.search(r'order[\s-]statistic.*multiset|\bmultiset\b|dynamic\s+multiset|multiset\s+operations?|insert,\s+delete,\s+rank|multiset\s+with\s+k[\s-]th|order\s+statistics?\s+in\s+multiset|multiplicity.*rank|quantile\s+select', lower):
            fenwick_is_multiset = True
            fenwick_is_frequency = True

        # Monotonic prefix extremum detection
        if re.search(r'prefix\s+min|prefix\s+max|prefix\s+minimum|prefix\s+maximum', lower) and not re.search(r'arbitrary\s+range\s+min|range\s+minimum\s+query', lower):
            fenwick_is_extremum = True
            if re.search(r'min|minimum', lower):
                fenwick_extremum_direction = "min"
            else:
                fenwick_extremum_direction = "max"

        # Anti-pattern & Boundary conditions
        if re.search(r'static\s+array|no\s+updates|immutable\s+sequence|fixed\s+array\s+without\s+updates|static\s+range\s+sums?|static\s+prefix\s+sums?', lower) and not (_has_point_upd or _has_range_upd or fenwick_is_frequency or fenwick_is_inversion_counting):
            fenwick_is_static = True

        if re.search(r'batch\s+(?:range\s+)?(?:updates?|adds?).*query\s+only\s+at\s+(?:the\s+)?end|offline\s+range\s+adds?\s+with\s+final\s+reconstruction|all\s+updates?\s+before\s+any\s+queries?|queries?\s+(?:are\s+)?only\s+after\s+all\s+updates?|batch\s+(?:range\s+)?adds?', lower):
            fenwick_is_offline_range_add = True

        if re.search(r'arbitrary\s+range\s+min|arbitrary\s+point\s+replacement.*(?:min|max)|range\s+minimum\s+with\s+replacement|range\s+min/max\s+with\s+arbitrary\s+updates?', lower):
            fenwick_has_arbitrary_range_minmax = True

        if re.search(r'range\s+assignment|assign\s+val\s+to\s+range|set\s+range\s+to\s+constant|overwrite\s+interval', lower):
            fenwick_has_range_assignment = True

        if re.search(r'unknown\s+(?:dynamic\s+)?streaming\s+keys|unbounded\s+streaming\s+coordinates|unbounded\s+online\s+keys|dynamically\s+appearing\s+unknown\s+coordinates', lower):
            fenwick_has_dynamic_unknown_coords = True

        if re.search(r'negative\s+frequenc|frequencies\s+can\s+be\s+negative|allow\s+negative\s+counts?\s+for\s+k[\s-]th', lower):
            fenwick_has_negative_frequencies = True

        if re.search(r'exceeds\s+memory|10000\s*x\s*10000.*memory|memory\s+limit\s+exceeded.*fenwick', lower):
            fenwick_resource_exceeded = True

        # Structural trigger
        _is_fenwick_structural = bool(
            (fenwick_has_point_update and (fenwick_has_prefix_query or fenwick_has_range_query)) or
            (fenwick_has_range_update and (fenwick_has_point_query or fenwick_has_range_query)) or
            fenwick_is_2d or fenwick_is_inversion_counting or fenwick_is_multiset or fenwick_is_frequency or
            fenwick_is_extremum or fenwick_requires_coordinate_compression or
            fenwick_is_static or fenwick_is_offline_range_add or
            fenwick_has_arbitrary_range_minmax or fenwick_has_range_assignment or
            fenwick_has_dynamic_unknown_coords or fenwick_has_negative_frequencies or
            fenwick_has_non_invertible_range or
            _is_fenwick_keyword
        )

        # Do not steal genuine Graph, Heap, DSU, or Monotonic Stack problems
        if _is_fenwick_keyword:
            is_fenwick_detected = True
            is_heap_detected = False
        elif _is_fenwick_structural and not (is_dsu_detected or (is_heap_detected and not (fenwick_has_kth_query or fenwick_is_multiset or fenwick_is_frequency or fenwick_has_negative_frequencies)) or is_graph_detected or is_bst or bool(re.search(r'quickselect|closest\s+pair|centroid|cdq|branch\s+and\s+bound', lower))):
            is_fenwick_detected = True

        if is_fenwick_detected:
            # Determine Fenwick algorithm family & kind
            if fenwick_is_2d:
                fenwick_kind = FenwickKind.TWO_DIMENSIONAL
                fenwick_algorithm_family = "fenwick_2d_point_update_range_query"
                fenwick_operation_kind = FenwickOperationKind.RECTANGLE_QUERY
            elif fenwick_is_extremum and not fenwick_has_arbitrary_range_minmax:
                fenwick_kind = FenwickKind.PREFIX_EXTREMUM
                fenwick_algorithm_family = "fenwick_prefix_extremum"
                fenwick_operation_kind = FenwickOperationKind.PREFIX_QUERY
            elif fenwick_has_range_update and (fenwick_has_range_query or re.search(r'range\s+sum|sum\s+in\s+range', lower)):
                fenwick_kind = FenwickKind.RANGE_UPDATE_RANGE_QUERY
                fenwick_algorithm_family = "fenwick_range_update_range_query"
                fenwick_operation_kind = FenwickOperationKind.RANGE_QUERY
            elif fenwick_has_range_update and (fenwick_has_point_query or re.search(r'point\s+query|value\s+at\s+index', lower)):
                fenwick_kind = FenwickKind.RANGE_UPDATE_POINT_QUERY
                fenwick_algorithm_family = "fenwick_range_update_point_query"
                fenwick_operation_kind = FenwickOperationKind.POINT_QUERY
            elif fenwick_is_inversion_counting:
                fenwick_kind = FenwickKind.INVERSION_COUNTING
                fenwick_algorithm_family = "fenwick_inversion_counting"
                fenwick_operation_kind = FenwickOperationKind.PREFIX_QUERY
            elif fenwick_is_multiset:
                fenwick_kind = FenwickKind.MULTISET
                fenwick_algorithm_family = "fenwick_multiset"
                fenwick_operation_kind = FenwickOperationKind.KTH_ELEMENT if fenwick_has_kth_query else FenwickOperationKind.POINT_ADD
            elif fenwick_has_kth_query and not fenwick_has_negative_frequencies:
                fenwick_kind = FenwickKind.KTH_ELEMENT
                fenwick_algorithm_family = "fenwick_kth_element"
                fenwick_operation_kind = FenwickOperationKind.KTH_ELEMENT
            elif fenwick_requires_coordinate_compression and not fenwick_is_inversion_counting:
                fenwick_kind = FenwickKind.COORDINATE_COMPRESSION
                fenwick_algorithm_family = "fenwick_coordinate_compression"
                fenwick_operation_kind = FenwickOperationKind.COMPRESS
            elif fenwick_is_frequency:
                fenwick_kind = FenwickKind.FREQUENCY
                fenwick_algorithm_family = "fenwick_frequency"
                fenwick_operation_kind = FenwickOperationKind.COUNT_LESS_EQUAL
            else:
                fenwick_kind = FenwickKind.POINT_UPDATE_PREFIX_QUERY
                fenwick_algorithm_family = "fenwick_point_update_prefix_query"
                fenwick_operation_kind = FenwickOperationKind.RANGE_QUERY if fenwick_has_range_query else FenwickOperationKind.PREFIX_QUERY

            if input_structure == 'single_sequence':
                input_structure = 'fenwick'

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 18. Segment Tree Feature Extraction (Phase 3J)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        is_segment_tree_detected: bool = False
        segment_tree_kind: Optional[SegmentTreeKind] = None
        segment_tree_operation_kind: Optional[SegmentTreeOperationKind] = None
        segment_tree_algorithm_family: Optional[str] = None
        segment_tree_has_point_update: bool = False
        segment_tree_has_range_update: bool = False
        segment_tree_has_range_add: bool = False
        segment_tree_has_range_assign: bool = False
        segment_tree_has_combined_lazy: bool = False
        segment_tree_has_range_query: bool = False
        segment_tree_query_op: str = "sum"
        segment_tree_is_metadata: bool = False
        segment_tree_is_max_subarray: bool = False
        segment_tree_is_frequency: bool = False
        segment_tree_is_interval_statistics: bool = False
        segment_tree_is_static: bool = False
        segment_tree_is_simple_prefix: bool = False
        segment_tree_is_offline_range_add: bool = False
        segment_tree_is_fenwick_equivalent: bool = False
        segment_tree_has_no_associative_merge: bool = False
        segment_tree_has_unsupported_lazy: bool = False
        segment_tree_resource_exceeded: bool = False

        _is_segtree_keyword = bool(re.search(
            r'\bsegment\s+tree\b|\bsegtree\b',
            lower
        )) and not bool(re.search(r'rather\s+than.*(?:segment\s+tree|segtree)|instead\s+of.*(?:segment\s+tree|segtree)', lower))

        # Check updates
        if re.search(r'point\s+(?:update|modification)|update\s+(?:element\s+at|single\s+element|at\s+index|value\s+at)|modify\s+element\s+at\s+index', lower):
            segment_tree_has_point_update = True

        if re.search(r'range\s+(?:addition|add)|add\s+(?:delta|val|value|\w+|\d+)\s+to\s+(?:range|interval|all\s+elements\s+in)|increment\s+range', lower):
            segment_tree_has_range_update = True
            segment_tree_has_range_add = True

        if re.search(r'range\s+assignment|assign\s+(?:val|value|\w+|\d+)\s+to\s+(?:all\s+elements\s+in\s+)?(?:range|interval)|overwrite\s+(?:range|interval)|set\s+(?:all\s+elements\s+in\s+)?(?:range|interval)\s+to', lower):
            segment_tree_has_range_update = True
            segment_tree_has_range_assign = True

        if (segment_tree_has_range_add and segment_tree_has_range_assign) or re.search(r'both\s+range\s+assignment\s+and\s+range\s+add|range\s+assign.*range\s+add|range\s+add.*range\s+assign|assignment\s+and\s+addition|combined\s+lazy|additions?\s+and\s+assignments?', lower):
            segment_tree_has_combined_lazy = True
            segment_tree_has_range_update = True
            segment_tree_has_range_add = True
            segment_tree_has_range_assign = True

        # Check queries
        if re.search(r'range\s+(?:query|queries)|query\s+(?:in\s+)?range|interval\s+query|subsegment\s+query', lower) or _has_rng_query:
            segment_tree_has_range_query = True

        # Operation type
        if re.search(r'maximum\s+contiguous\s+subarray|maximum\s+subarray\s+sum|max\s+contiguous\s+subarray|max\s+subarray', lower):
            segment_tree_is_max_subarray = True
            segment_tree_query_op = "max_subarray"
        elif re.search(r'composite\s+node\s+metadata|sum,\s*min,\s*and\s*max\s+simultaneously|simultaneous\s+aggregate\s+statistics', lower):
            segment_tree_is_metadata = True
            segment_tree_query_op = "metadata"
        elif re.search(r'frequency\s+of\s+min(?:imum)?|min\s+and\s+max\s+with\s+multiplicity|range\s+extrema\s+frequency|interval\s+statistics', lower):
            segment_tree_is_interval_statistics = True
            segment_tree_query_op = "interval_statistics"
        elif re.search(r'frequency\s+segment\s+tree|order\s+statistic.*segment\s+tree|k-th\s+element\s+in\s+frequency\s+segment|kth\s+smallest\s+with\s+arbitrary\s+decrements', lower):
            segment_tree_is_frequency = True
            segment_tree_query_op = "frequency"
        elif re.search(r'range\s+gcd|greatest\s+common\s+divisor\s+in\s+range', lower):
            segment_tree_query_op = "gcd"
        elif re.search(r'range\s+min(?:imum)?|minimum\s+in\s+range', lower):
            segment_tree_query_op = "min"
        elif re.search(r'range\s+max(?:imum)?|maximum\s+in\s+range', lower):
            segment_tree_query_op = "max"
        else:
            segment_tree_query_op = "sum"

        # Anti-pattern signals
        if re.search(r'static\s+array|no\s+updates|immutable\s+sequence|fixed\s+array\s+without\s+updates', lower) and not (segment_tree_has_point_update or segment_tree_has_range_update):
            segment_tree_is_static = True

        if re.search(r'prefix\s+sum\s+only|prefix\s+queries\s+only|only\s+prefix\s+sums', lower) and segment_tree_has_point_update and not segment_tree_has_range_update:
            segment_tree_is_simple_prefix = True

        if re.search(r'batch\s+(?:range\s+)?adds?.*quer(?:y|ies)\s+(?:are\s+)?only\s+at\s+(?:the\s+)?end|offline\s+range\s+adds?|all\s+updates?\s+before\s+any\s+queries?|queries?\s+(?:are\s+)?only\s+after\s+all\s+updates?|batch\s+(?:range\s+)?adds?', lower):
            segment_tree_is_offline_range_add = True

        if segment_tree_has_point_update and segment_tree_has_range_query and segment_tree_query_op == "sum" and not (segment_tree_has_range_update or segment_tree_is_max_subarray or segment_tree_is_metadata):
            segment_tree_is_fenwick_equivalent = True

        if re.search(r'dynamic\s+median\s+without\s+rank\s+tree|non-associative|floating\s+point\s+average\s+without\s+sum', lower):
            segment_tree_has_no_associative_merge = True

        if re.search(r'range\s+chmin|range\s+chmax|segment\s+tree\s+beats\s+required', lower):
            segment_tree_has_unsupported_lazy = True

        if re.search(r'exceeds\s+memory.*segment\s+tree|segment\s+tree.*memory\s+limit\s+exceeded|4\s*\*\s*n\s*\*\s*sizeof.*budget\s+exceeded', lower):
            segment_tree_resource_exceeded = True

        segment_tree_has_negative_frequencies = fenwick_has_negative_frequencies or bool(re.search(r'negative\s+frequenc|frequencies\s+can\s+be\s+negative|allow\s+negative\s+counts?\s+for\s+k[\s-]th', lower))

        # Segment Tree detection
        _is_segtree_structural = bool(
            _is_segtree_keyword or
            segment_tree_is_max_subarray or
            segment_tree_has_combined_lazy or
            (segment_tree_has_range_assign and segment_tree_has_range_query) or
            (segment_tree_has_range_add and segment_tree_has_range_query and not _is_fenwick_keyword) or
            (segment_tree_has_point_update and segment_tree_query_op in ("min", "max", "gcd", "metadata", "interval_statistics")) or
            segment_tree_is_metadata or
            segment_tree_is_interval_statistics or
            (segment_tree_is_frequency and not _is_fenwick_keyword) or
            segment_tree_is_static or
            segment_tree_is_simple_prefix or
            segment_tree_is_offline_range_add or
            segment_tree_has_no_associative_merge or
            segment_tree_has_unsupported_lazy or
            segment_tree_resource_exceeded or
            segment_tree_has_negative_frequencies
        )

        if _is_segtree_keyword:
            is_segment_tree_detected = True
            is_fenwick_detected = False
            is_heap_detected = False
        elif _is_segtree_structural and not (is_dsu_detected or is_graph_detected or is_bst or (_is_fenwick_keyword and not segment_tree_has_range_assign)):
            is_segment_tree_detected = True

        if is_segment_tree_detected:
            if segment_tree_is_max_subarray:
                segment_tree_kind = SegmentTreeKind.MAX_SUBARRAY
                segment_tree_algorithm_family = "segment_tree_max_subarray"
                segment_tree_operation_kind = SegmentTreeOperationKind.RANGE_QUERY
            elif segment_tree_has_combined_lazy:
                segment_tree_kind = SegmentTreeKind.COMBINED_LAZY_RANGE_QUERY
                segment_tree_algorithm_family = "segment_tree_combined_lazy_range_query"
                segment_tree_operation_kind = SegmentTreeOperationKind.RANGE_QUERY
            elif segment_tree_has_range_assign:
                segment_tree_kind = SegmentTreeKind.RANGE_ASSIGN_RANGE_QUERY
                segment_tree_algorithm_family = "segment_tree_range_assign_range_query"
                segment_tree_operation_kind = SegmentTreeOperationKind.RANGE_ASSIGN
            elif segment_tree_has_range_add:
                segment_tree_kind = SegmentTreeKind.RANGE_ADD_RANGE_QUERY
                segment_tree_algorithm_family = "segment_tree_range_add_range_query"
                segment_tree_operation_kind = SegmentTreeOperationKind.RANGE_ADD
            elif segment_tree_is_metadata:
                segment_tree_kind = SegmentTreeKind.METADATA_AGGREGATE
                segment_tree_algorithm_family = "segment_tree_metadata_aggregate"
                segment_tree_operation_kind = SegmentTreeOperationKind.RANGE_QUERY
            elif segment_tree_is_interval_statistics:
                segment_tree_kind = SegmentTreeKind.INTERVAL_STATISTICS
                segment_tree_algorithm_family = "segment_tree_interval_statistics"
                segment_tree_operation_kind = SegmentTreeOperationKind.RANGE_QUERY
            elif segment_tree_is_frequency:
                segment_tree_kind = SegmentTreeKind.FREQUENCY_ORDER_STATISTIC
                segment_tree_algorithm_family = "segment_tree_frequency_order_statistic"
                segment_tree_operation_kind = SegmentTreeOperationKind.POINT_UPDATE
            else:
                segment_tree_kind = SegmentTreeKind.POINT_UPDATE_RANGE_QUERY
                segment_tree_algorithm_family = "segment_tree_point_update_range_query"
                segment_tree_operation_kind = SegmentTreeOperationKind.RANGE_QUERY

            if input_structure == 'single_sequence':
                input_structure = 'segment_tree'

        # ── 19. Dynamic Programming Signals (Phase 3K) ──
        is_dp_detected: bool = False
        dp_kind: Optional[DPKind] = None
        dp_operation_kind: Optional[DPOperationKind] = None
        dp_algorithm_family: Optional[str] = None
        dp_state_dimension: int = 1
        dp_has_optimal_substructure: bool = False
        dp_has_overlapping_subproblems: bool = False
        dp_is_dag: bool = True
        dp_is_cyclic: bool = False
        dp_greedy_optimal: bool = False
        dp_is_non_markovian: bool = False
        dp_state_space_size: int = 100000
        dp_is_resource_exceeded: bool = False
        dp_requires_reconstruction: bool = False
        dp_space_compressible: bool = False
        dp_optimization_applicable: Optional[str] = None

        _is_dp_keyword = bool(re.search(
            r'\bdynamic\s+programming\b|\bdp\b|overlapping\s+subproblems|optimal\s+substructure|memoiz(?:ation|ed)|tabulat(?:ion|ed)|bellman(?:\'s)?\s+equation',
            lower
        ))

        # Check for specific DP patterns
        dp_is_1d_linear = bool(re.search(
            r'longest\s+increasing\s+subsequence|\blis\b|kadane|climbing\s+stairs|house\s+robber|maximum\s+subarray\s+sum\s+via\s+dp|1d\s+(?:linear\s+)?dp|linear\s+dynamic\s+programming|fibonacci\s+dp|decode\s+ways|\bdp_1d_linear\b',
            lower
        ))
        dp_is_grid_2d = bool(re.search(
            r'grid\s+paths?|unique\s+paths|minimum\s+path\s+sum|matrix\s+traversal\s+dp|2d\s+grid\s+(?:dp|dynamic\s+programming)|grid\s+dynamic\s+programming|dungeon\s+game|cherry\s+pickup|triangle\s+min\s+path|\bdp_grid_2d\b|\bdp_2d_grid\b',
            lower
        ))
        dp_is_knapsack = bool(re.search(
            r'0/1\s+knapsack|unbounded\s+knapsack|bounded\s+knapsack|\bknapsack\b|subset\s+sum\s+problem|coin\s+change|partition\s+equal\s+subset\s+sum|\bdp_knapsack\b|\bdp_knapsack_01\b|\bdp_knapsack_unbounded\b',
            lower
        )) or (bool(re.search(r'\btarget\s+sum\b', lower)) and not is_contiguous)
        dp_is_subsequence = bool(re.search(
            r'longest\s+common\s+subsequence|\blcs\b|edit\s+distance|levenshtein|wildcard\s+matching|regular\s+expression\s+matching|distinct\s+subsequences|interleaving\s+string|shortest\s+common\s+supersequence|\bdp_subsequence_string\b|\bdp_string_alignment\b',
            lower
        ))
        dp_is_interval = bool(re.search(
            r'interval\s+(?:dp|dynamic\s+programming)|range\s+(?:dp|dynamic\s+programming)|matrix\s+chain\s+multiplication|\bmcm\b|burst\s+balloons|minimum\s+cost\s+to\s+merge\s+stones|palindrome\s+partitioning\s+(?:min|cuts?)|strange\s+printer|\bdp_interval\b',
            lower
        ))
        dp_is_partition = bool(re.search(
            r'partition\s+dp|partition\s+array\s+into\s+k|split\s+array\s+largest\s+sum|book\s+allocation|painter(?:s)?\s+partition|allocate\s+books|prefix\s+suffix|best\s+time\s+to\s+buy\s+and\s+sell\s+stock\s+with\s+two\s+transactions|\bdp_partition\b|\bdp_prefix_suffix\b',
            lower
        ))
        dp_is_state_machine = bool(re.search(
            r'state\s+machine\s+(?:dp|dynamic\s+programming)|finite\s+state\s+dynamic\s+programming|stock\s+(?:buy|sell)|best\s+time\s+to\s+buy\s+and\s+sell\s+stock|cooldown|transaction\s+fee|\bdp_state_machine\b',
            lower
        ))
        dp_is_bitmask = bool(re.search(
            r'bitmask\s+(?:dp|dynamic\s+programming)|travelling\s+sales(?:person|man)|\btsp\b|hamiltonian\s+path|assignment\s+problem\s+dp|subset\s+mask|sos\s+dp|sum\s+over\s+subsets|\bdp_bitmask\b',
            lower
        ))
        dp_is_tree = bool(re.search(
            r'tree\s+(?:dp|dynamic\s+programming)|tree\s+independent\s+set|max\s+independent\s+set\s+on\s+tree|rerooting\s+dp|tree\s+diameter\s+dp|subtree\s+dynamic\s+programming|\bdp_tree\b',
            lower
        ))
        dp_is_dag = bool(re.search(
            r'dag\s+(?:dp|dynamic\s+programming|longest\s+path)|longest\s+path\s+in\s+(?:a\s+)?(?:dag|directed\s+acyclic\s+graph)|topological\s+(?:dp|dynamic\s+programming)|game\s+theory\s+on\s+graph|\bdp_dag\b|\bdp_dag_longest_path\b',
            lower
        ))
        dp_is_digit = bool(re.search(
            r'digit\s+(?:dp|dynamic\s+programming)|counting\s+numbers\s+with\s+digit|numbers\s+with\s+repeated\s+digits|non-negative\s+integers\s+without\s+consecutive\s+ones|\bdp_digit\b',
            lower
        ))
        dp_is_optimization = bool(re.search(
            r'convex\s+hull\s+trick|\bcht\b|knuth(?:\'s)?\s+optimization|divide\s+and\s+conquer\s+(?:dp|optimization)|\bd&c\s+opt\b|monotonic\s+queue\s+dp|aliens\s+trick|slope\s+trick|quadrangle\s+inequality|opt(?:imal)?\s+monotonicity|\bdp_optimization\b|\bdp_divide_and_conquer\b',
            lower
        ))
        dp_is_reconstruction = bool(re.search(
            r'reconstruct\s+(?:the\s+)?(?:optimal\s+)?solution|print\s+(?:the\s+)?(?:actual\s+)?(?:path|sequence|items)|backtrack\s+solution|lexicographically\s+smallest\s+(?:path|sequence)|\bdp_solution_reconstruction\b',
            lower
        ))
        dp_is_space_opt = bool(re.search(
            r'rolling\s+array|in-place\s+(?:1d\s+)?knapsack|single\s+array\s+.*knapsack|space\s+optimi[zs](?:ed|ation)|reduce\s+space\s+to\s+o\(|\bdp_space_optimization\b',
            lower
        ))
        dp_is_unbounded = bool(re.search(
            r'unbounded\s+knapsack|coin\s+change|complete\s+knapsack|unlimited\s+copies|infinite\s+supply|\bdp_knapsack_unbounded\b',
            lower
        ))

        # Anti-pattern / Discrimination signals
        dp_greedy_optimal = bool(re.search(
            r'fractional\s+knapsack|interval\s+scheduling|earliest\s+deadline|activity\s+selection|huffman|dijkstra\s+sufficient|greedy\s+choice\s+property\s+holds|can\s+be\s+solved\s+greedily',
            lower
        ))
        dp_is_cyclic = bool(re.search(
            r'negative\s+cycles?|cyclic\s+dependenc(?:y|ies)|graph\s+(?:contains|with)\s+cycles|infinite\s+loop\s+in\s+transitions|arbitrary\s+cycles?|cycles?\s+and\s+arbitrary',
            lower
        ))
        dp_no_optimal_substructure = bool(re.search(
            r'longest\s+simple\s+path\s+in\s+general\s+(?:undirected\s+)?graph|subproblem\s+optima\s+do\s+not\s+compose|non-optimal\s+substructure|subproblems\s+lack\s+optimal\s+substructure|without\s+(?:subproblem\s+)?optimal(?:ity|\s+substructure)',
            lower
        ))
        dp_no_overlapping_subproblems = bool(re.search(
            r'disjoint\s+(?:halves|subproblems)|independent\s+subproblems|merge\s*sort|pure\s+divide\s+and\s+conquer|without\s+overlapping\s+subproblems|no\s+overlapping\s+subproblems',
            lower
        ))
        dp_is_non_markovian = bool(re.search(
            r'history\s+dependent\s+without\s+state\s+bound|path\s+depends\s+on\s+full\s+unbounded\s+history|non-markovian|future\s+transitions\s+depend\s+on\s+entire\s+past',
            lower
        ))
        dp_is_resource_exceeded = bool(re.search(
            r'state\s+space\s+explosion|exponential\s+states\s+exceeding\s+memory|n\s*=\s*(?:[3-9]\d|\d{3,})\s+with\s+subset\s+states|unbounded\s+state\s+space',
            lower
        ))

        dp_has_optimal_substructure = not dp_no_optimal_substructure
        dp_has_overlapping_subproblems = not dp_no_overlapping_subproblems

        _is_dp_structural = bool(
            _is_dp_keyword or
            dp_is_1d_linear or
            dp_is_grid_2d or
            dp_is_knapsack or
            dp_is_subsequence or
            dp_is_interval or
            dp_is_partition or
            dp_is_state_machine or
            dp_is_bitmask or
            dp_is_tree or
            dp_is_dag or
            dp_is_digit or
            dp_is_optimization or
            dp_is_reconstruction or
            dp_is_space_opt or
            dp_greedy_optimal or
            dp_is_cyclic or
            dp_no_optimal_substructure or
            dp_no_overlapping_subproblems or
            dp_is_non_markovian or
            dp_is_resource_exceeded
        )

        if (_is_dp_keyword or _is_dp_structural) and not bool(re.search(r'branch\s+(?:and|&)\s+bound|bnb|upper\s+bound\s+pruning|relaxation\s+bound', lower)):
            is_dp_detected = True

        if is_dp_detected:
            if dp_is_space_opt:
                dp_kind = DPKind.SPACE_OPTIMIZATION
                dp_algorithm_family = "dp_space_optimization"
                dp_operation_kind = DPOperationKind.COMPRESS_SPACE
                dp_state_dimension = 1
                dp_space_compressible = True
            elif dp_is_optimization:
                dp_kind = DPKind.OPTIMIZATION
                dp_algorithm_family = "dp_optimization"
                dp_operation_kind = DPOperationKind.OPTIMIZE_TRANSITION
                dp_state_dimension = 2
            elif dp_is_grid_2d:
                dp_kind = DPKind.GRID_2D
                dp_algorithm_family = "dp_grid_2d"
                dp_operation_kind = DPOperationKind.TABULATE
                dp_state_dimension = 2
            elif dp_is_knapsack:
                dp_kind = DPKind.KNAPSACK
                dp_algorithm_family = "dp_knapsack"
                dp_operation_kind = DPOperationKind.TABULATE
                dp_state_dimension = 2
            elif dp_is_subsequence:
                dp_kind = DPKind.SUBSEQUENCE_STRING
                dp_algorithm_family = "dp_subsequence_string"
                dp_operation_kind = DPOperationKind.TABULATE
                dp_state_dimension = 2
            elif dp_is_interval:
                dp_kind = DPKind.INTERVAL
                dp_algorithm_family = "dp_interval"
                dp_operation_kind = DPOperationKind.TABULATE
                dp_state_dimension = 2
            elif dp_is_partition:
                dp_kind = DPKind.PARTITION
                dp_algorithm_family = "dp_partition"
                dp_operation_kind = DPOperationKind.TABULATE
                dp_state_dimension = 2
            elif dp_is_state_machine:
                dp_kind = DPKind.STATE_MACHINE
                dp_algorithm_family = "dp_state_machine"
                dp_operation_kind = DPOperationKind.TRANSITION
                dp_state_dimension = 2
            elif dp_is_bitmask:
                dp_kind = DPKind.BITMASK
                dp_algorithm_family = "dp_bitmask"
                dp_operation_kind = DPOperationKind.TABULATE
                dp_state_dimension = 2
            elif dp_is_tree:
                dp_kind = DPKind.TREE
                dp_algorithm_family = "dp_tree"
                dp_operation_kind = DPOperationKind.MEMOIZE
                dp_state_dimension = 2
            elif dp_is_dag:
                dp_kind = DPKind.DAG
                dp_algorithm_family = "dp_dag"
                dp_operation_kind = DPOperationKind.MEMOIZE
                dp_state_dimension = 1
            elif dp_is_digit:
                dp_kind = DPKind.DIGIT
                dp_algorithm_family = "dp_digit"
                dp_operation_kind = DPOperationKind.MEMOIZE
                dp_state_dimension = 4
            elif dp_is_reconstruction:
                dp_kind = DPKind.RECONSTRUCTION
                dp_algorithm_family = "dp_solution_reconstruction"
                dp_operation_kind = DPOperationKind.RECONSTRUCT
                dp_state_dimension = 2
                dp_requires_reconstruction = True
            elif dp_is_1d_linear:
                dp_kind = DPKind.LINEAR_1D
                dp_algorithm_family = "dp_1d_linear"
                dp_operation_kind = DPOperationKind.TABULATE
                dp_state_dimension = 1
            else:
                dp_kind = DPKind.LINEAR_1D
                dp_algorithm_family = "dp_1d_linear"
                dp_operation_kind = DPOperationKind.TABULATE
                dp_state_dimension = 1

            dp_requires_reconstruction = dp_is_reconstruction or dp_requires_reconstruction
            dp_space_compressible = dp_is_space_opt or dp_space_compressible

        # ── 20. Greedy Feature Extraction (Phase 3L) ──
        is_greedy_detected: bool = False
        greedy_kind: Optional[GreedyKind] = None
        greedy_proof_kind: Optional[GreedyProofKind] = None
        greedy_algorithm_family: Optional[str] = None
        greedy_ordering_candidate: Optional[str] = None
        greedy_has_local_choice: bool = False
        greedy_has_exchange_signal: bool = False
        greedy_has_dominance_signal: bool = False
        greedy_has_staying_ahead_signal: bool = False
        greedy_has_cut_property_signal: bool = False
        greedy_has_matroid_signal: bool = False
        greedy_requires_sorting: bool = False
        greedy_requires_heap: bool = False
        greedy_requires_graph_structure: bool = False
        greedy_objective_kind: Optional[str] = None
        greedy_feasibility_preserved: bool = True
        greedy_counterexample_detected: bool = False
        greedy_proof_unestablished: bool = False
        greedy_competing_dp_signal: bool = False

        # Pattern detection:
        # 3L-A: Interval Selection / Activity Scheduling
        greedy_is_interval_selection = bool(re.search(r'activity\s+selection|non-?overlapping\s+intervals|earliest\s+finish(?:ing)?(?:\s+time)?|maximum\s+(?:number\s+of\s+)?compatible\s+intervals|interval\s+scheduling|select\s+maximum\s+intervals|greedy_interval_selection', lower))

        # 3L-B: Interval Covering / Minimum Point Selection / Stabbing
        greedy_is_interval_covering = bool(re.search(r'interval\s+covering|minimum\s+(?:number\s+of\s+)?arrows|burst\s+(?:some\s+)?balloons|minimum\s+points?\s+(?:to\s+)?cover|interval\s+stabbing|cover\s+all\s+intervals|greedy_interval_covering', lower))

        # 3L-C: Fractional Knapsack / Divisible Resource Allocation
        greedy_is_fractional_knapsack = bool(re.search(r'fractional\s+knapsack|divisible\s+(?:items?|resources?|weights?)|continuous\s+knapsack|value\s*[-/]?\s*density|take\s+fractions?|greedy_fractional_knapsack', lower))

        # 3L-D: Deadline / Scheduling Greedy (EDD / Smith's rule)
        greedy_is_deadline_scheduling = bool(re.search(r'minimize\s+maximum\s+lateness|earliest\s+due\s+date|smith\'?s\s+rule|weighted\s+completion\s+time|job\s+sequencing\s+with\s+deadlines|schedule\s+jobs?\s+(?:with\s+)?deadlines?|deadline\s+scheduling|scheduling\s+with\s+deadlines|greedy_deadline_scheduling', lower))

        # 3L-E: Heap-Assisted Greedy
        greedy_is_heap_assisted = bool(re.search(r'heap[- ]assisted\s+greedy|minimum\s+refueling\s+stops|refueling|resource\s+allocation\s+with\s+release|event\s+frontier\s+heap|maximum\s+tasks\s+with\s+resources?|greedy_heap_assisted', lower))

        # 3L-F: Huffman / Optimal Merge
        greedy_is_huffman_merge = bool(re.search(r'huffman(?:\s+coding)?|optimal\s+merge(?:\s+pattern)?|merge\s+two\s+smallest|combine\s+minimum\s+costs?|repeatedly\s+merge\s+(?:minimum|smallest)|greedy_huffman_merge', lower))

        # 3L-G: Sequence / String Local-Choice Greedy
        greedy_is_sequence_local_choice = bool(re.search(r'remove\s+(?:k\s+)?digits|lexicographically\s+smallest\s+(?:string|subsequence|number)\s+under\s+(?:removal|deletion)|local\s+choice\s+sequence|minimize\s+number\s+by\s+removing|greedy_sequence_local_choice', lower))

        # 3L-H: Reachability / Coverage / Partition Greedy
        greedy_is_reachability_partition = bool(re.search(r'jump\s+game|farthest\s+reach|minimum\s+jumps|gas\s+station(?:\s+circuit)?|greedy\s+coverage|reachability\s+frontier|greedy_reachability_partition', lower))

        # 3L-I: Graph-Greedy Integration (MST)
        greedy_is_graph_mst = bool(re.search(r'safe[- ]edge\s+cut|cut\s+property|greedy_graph_mst', lower)) or (
            bool(re.search(r'minimum\s+spanning\s+tree|mst\b', lower)) and not bool(re.search(r'\b(?:kruskal|prim)(?:\'s)?\b', lower))
        )

        # 3L-J: General Exchange / Dominance Greedy
        greedy_is_general_exchange = bool(re.search(r'general\s+exchange|custom\s+comparator|largest\s+number(?:\s+composition)?|compose\s+(?:the\s+)?largest\s+number|pairwise\s+exchange|exchange\s+argument\s+ordering|greedy_general_exchange', lower))

        # Anti-patterns & Counterexamples:
        if re.search(r'0/1\s+knapsack|discrete\s+knapsack|cannot\s+break\s+items|items?\s+(?:are\s+)?indivisible', lower):
            greedy_competing_dp_signal = True

        if re.search(r'non[- ]canonical\s+coin|counterexample|greedy\s+fails\s+on\s+coins?|canonical\s+coin\s+system\s+violated|greedy\s+counterexample', lower):
            greedy_counterexample_detected = True

        if re.search(r'weighted\s+interval\s+scheduling|intervals?\s+with\s+weights?|maximize\s+total\s+weight\s+of\s+non[- ]overlapping', lower):
            greedy_competing_dp_signal = True

        if re.search(r'proof\s+(?:cannot\s+be\s+established|unproven|not\s+established)|unsupported\s+greedy\s+proof|general\s+set\s+cover', lower):
            greedy_proof_unestablished = True

        if (greedy_is_interval_selection or greedy_is_interval_covering or
            greedy_is_fractional_knapsack or greedy_is_deadline_scheduling or
            greedy_is_heap_assisted or greedy_is_huffman_merge or
            greedy_is_sequence_local_choice or greedy_is_reachability_partition or
            greedy_is_graph_mst or greedy_is_general_exchange or
            greedy_counterexample_detected or greedy_competing_dp_signal or
            greedy_proof_unestablished or
            re.search(r'\bgreedy\b', lower)):
            is_greedy_detected = True

        greedy_has_greedy_choice = not (greedy_counterexample_detected or greedy_proof_unestablished or greedy_competing_dp_signal)
        greedy_has_optimal_substructure = True

        if is_greedy_detected:
            if greedy_is_interval_selection:
                greedy_kind = GreedyKind.INTERVAL_SELECTION
                greedy_algorithm_family = "greedy_interval_selection"
                greedy_proof_kind = GreedyProofKind.EXCHANGE
                greedy_ordering_candidate = "earliest_finish_time"
                greedy_has_local_choice = True
                greedy_has_exchange_signal = True
                greedy_requires_sorting = True
            elif greedy_is_interval_covering:
                greedy_kind = GreedyKind.INTERVAL_COVERING
                greedy_algorithm_family = "greedy_interval_covering"
                greedy_proof_kind = GreedyProofKind.STAYING_AHEAD
                greedy_ordering_candidate = "sorted_endpoints"
                greedy_has_local_choice = True
                greedy_has_staying_ahead_signal = True
                greedy_requires_sorting = True
            elif greedy_is_fractional_knapsack:
                greedy_kind = GreedyKind.FRACTIONAL_KNAPSACK
                greedy_algorithm_family = "greedy_fractional_knapsack"
                greedy_proof_kind = GreedyProofKind.EXCHANGE
                greedy_ordering_candidate = "value_density_descending"
                greedy_has_local_choice = True
                greedy_has_exchange_signal = True
                greedy_requires_sorting = True
            elif greedy_is_deadline_scheduling:
                greedy_kind = GreedyKind.DEADLINE_SCHEDULING
                greedy_algorithm_family = "greedy_deadline_scheduling"
                greedy_proof_kind = GreedyProofKind.EXCHANGE
                greedy_ordering_candidate = "earliest_due_date_or_smiths_ratio"
                greedy_has_local_choice = True
                greedy_has_exchange_signal = True
                greedy_requires_sorting = True
            elif greedy_is_heap_assisted:
                greedy_kind = GreedyKind.HEAP_ASSISTED
                greedy_algorithm_family = "greedy_heap_assisted"
                greedy_proof_kind = GreedyProofKind.STAYING_AHEAD
                greedy_ordering_candidate = "event_order_with_heap_priority"
                greedy_has_local_choice = True
                greedy_requires_heap = True
            elif greedy_is_huffman_merge:
                greedy_kind = GreedyKind.HUFFMAN_MERGE
                greedy_algorithm_family = "greedy_huffman_merge"
                greedy_proof_kind = GreedyProofKind.EXCHANGE
                greedy_ordering_candidate = "min_frequency_heap_merge"
                greedy_has_local_choice = True
                greedy_has_exchange_signal = True
                greedy_requires_heap = True
            elif greedy_is_sequence_local_choice:
                greedy_kind = GreedyKind.SEQUENCE_LOCAL_CHOICE
                greedy_algorithm_family = "greedy_sequence_local_choice"
                greedy_proof_kind = GreedyProofKind.DOMINANCE
                greedy_ordering_candidate = "monotonic_stack_irreversible_choice"
                greedy_has_local_choice = True
                greedy_has_dominance_signal = True
            elif greedy_is_reachability_partition:
                greedy_kind = GreedyKind.REACHABILITY_PARTITION
                greedy_algorithm_family = "greedy_reachability_partition"
                greedy_proof_kind = GreedyProofKind.STAYING_AHEAD
                greedy_ordering_candidate = "farthest_reach_scan"
                greedy_has_local_choice = True
                greedy_has_staying_ahead_signal = True
            elif greedy_is_graph_mst:
                greedy_kind = GreedyKind.GRAPH_MST
                greedy_algorithm_family = "greedy_graph_mst"
                greedy_proof_kind = GreedyProofKind.SAFE_CUT
                greedy_ordering_candidate = "lightest_cut_edge_sort"
                greedy_has_local_choice = True
                greedy_has_cut_property_signal = True
                greedy_requires_graph_structure = True
            elif greedy_is_general_exchange:
                greedy_kind = GreedyKind.GENERAL_EXCHANGE
                greedy_algorithm_family = "greedy_general_exchange"
                greedy_proof_kind = GreedyProofKind.EXCHANGE
                greedy_ordering_candidate = "custom_comparator_sort"
                greedy_has_local_choice = True
                greedy_has_exchange_signal = True
                greedy_requires_sorting = True
            else:
                greedy_kind = GreedyKind.INTERVAL_SELECTION
                greedy_algorithm_family = "greedy_interval_selection"
                greedy_proof_kind = GreedyProofKind.EXCHANGE
                greedy_ordering_candidate = "earliest_finish_time"
                greedy_has_local_choice = True
                greedy_has_exchange_signal = True
                greedy_requires_sorting = True

        # ── 21. Divide and Conquer & Backtracking Signals (Phase 3M) ──
        is_dc_backtracking_detected = False
        dc_backtracking_kind = None
        subproblem_dependency_kind = None
        termination_guarantee_kind = None
        dc_backtracking_algorithm_family = None

        dc_is_independent_subproblems = False
        dc_has_cross_boundary_combine = False
        dc_combine_complexity = None
        dc_base_case_size = 1
        dc_recursion_depth_limit = 1000

        backtracking_decision_space_size = 0
        backtracking_is_exponential = False
        backtracking_requires_pruning = False
        backtracking_pruning_kind = None
        backtracking_state_restoration = False
        backtracking_symmetry_breaking = False
        backtracking_is_exact_cover = False
        backtracking_is_csp = False
        backtracking_is_branch_and_bound = False
        backtracking_objective_direction = None
        backtracking_bound_type = None
        backtracking_is_meet_in_middle = False
        backtracking_split_strategy = None

        backtracking_search_space_explosive = False
        backtracking_greedy_sufficient = False
        backtracking_dp_sufficient = False
        dc_subproblems_not_independent = False
        dc_combine_step_intractable = False
        dc_base_case_undefined = False
        backtracking_resource_limit_exceeded = False

        is_cross_family_composition = False
        composition_unsupported = False

        # Section 8: Cross-family composition / Tower problem gate
        is_tower_problem = bool(re.search(
            r'towers?\s+problem|build\s+towers|minimum\s+(?:number\s+of\s+)?towers|'
            r'place\s+(?:each\s+)?cube\s+(?:on\s+top\s+of|on)\s+(?:an?\s+)?existing\s+tower|'
            r'tower\s+of\s+cubes|cubes?\s+into\s+towers', lower
        ))
        is_cross_family = bool(re.search(
            r'cross[- ]family\s+composition|composition_unsupported|'
            r'greedy\s+\+\s+(?:ordered\s+state|binary\s+search\s+tree|multiset|upper_bound)', lower
        )) or is_tower_problem

        if is_cross_family:
            is_cross_family_composition = True
            composition_unsupported = True

        # 3M Patterns
        dc_is_inversions = bool(re.search(
            r'merge\s+sort\s+inversions?|count\s+(?:the\s+number\s+of\s+)?inversions?|'
            r'inversion\s+count(?:ing)?|reverse\s+pairs?|cross[- ]boundary\s+pair\s+counting|'
            r'significant\s+inversions?|count\s+pairs.*a\[i\]\s*>\s*2\s*\*?\s*a\[j\]|'
            r'dc_merge_sort_inversions', lower
        )) and not bool(re.search(r'fenwick|binary\s+indexed\s+tree|segment\s+tree', lower))

        dc_is_quickselect = bool(re.search(
            r'quickselect|kth\s+largest\s+element\s+in\s+an?\s+unsorted|'
            r'kth\s+smallest\s+element\s+in\s+an?\s+unsorted|'
            r'selection\s+by\s+partition|linear\s+time\s+selection|'
            r'find\s+kth\s+(?:largest|smallest).*without\s+sorting|'
            r'dc_quickselect', lower
        )) and not bool(re.search(r'heap|priority\s+queue', lower))

        dc_is_closest_pair = bool(re.search(
            r'closest\s+pair\s+of\s+points?|closest\s+points?|'
            r'minimum\s+euclidean\s+distance|geometric\s+divide\s+and\s+conquer|'
            r'pair\s+of\s+points\s+with\s+(?:the\s+)?smallest\s+distance|'
            r'dc_closest_pair', lower
        ))

        dc_is_tree_centroid = bool(re.search(
            r'centroid\s+decomposition|tree\s+centroid|'
            r'paths\s+in\s+(?:a\s+)?tree\s+with\s+length|paths\s+of\s+length.*in\s+tree|'
            r'divide\s+tree\s+at\s+centroid|dc_tree_centroid', lower
        ))

        dc_is_cdq = bool(re.search(
            r'cdq(?:\s+divide\s+and\s+conquer)?|offline\s+divide\s+and\s+conquer|'
            r'partial\s+order(?:\s+counting)?|multi-?dimensional\s+queries|'
            r'dynamic\s+to\s+offline|3d\s+partial\s+order|'
            r'left\s+to\s+right\s+subproblem\s+contribution|dc_cdq_divide_and_conquer', lower
        ))

        bt_is_subsets_permutations = bool(re.search(
            r'generate\s+all\s+(?:subsets|permutations|combinations)|'
            r'all\s+subsets|all\s+permutations|power\s+set|'
            r'combinatorial\s+backtracking|subsets\s+with\s+duplicates|'
            r'permutations\s+with\s+duplicates|backtracking_subsets_permutations', lower
        ))

        bt_is_csp = bool(re.search(
            r'n[- ]queens|solve\s+sudoku|sudoku\s+solver|'
            r'constraint\s+satisfaction|exact\s+cover|dancing\s+links|'
            r'algorithm\s+x|backtracking_constraint_satisfaction', lower
        ))

        bt_is_branch_and_bound = bool(re.search(
            r'branch\s+(?:and|&)\s+bound|bound\s+pruning|'
            r'optimal\s+subset\s+with\s+bounding|traveling\s+sales(?:man|person)\s+branch\s+and\s+bound|'
            r'backtracking_branch_and_bound', lower
        ))

        bt_is_state_space_search = bool(re.search(
            r'state[- ]space\s+search|word\s+search(?:\s+ii)?|'
            r'rat\s+in\s+a\s+maze|maze\s+search|puzzle\s+search|'
            r'grid\s+word\s+search|backtracking_state_space_search', lower
        ))

        bt_is_meet_in_middle = bool(re.search(
            r'meet\s+in\s+the\s+middle|split\s+search\s+space|'
            r'subset\s+sum\s+with\s+n\s*<=\s*40|n\s*=\s*40|'
            r'two\s+halves\s+search|backtracking_meet_in_the_middle', lower
        ))

        # Anti-patterns
        if re.search(r'subproblems?\s+(?:are\s+)?not\s+independent|cross[- ]subproblem\s+dependency|dependent\s+subproblems|dc_subproblems_not_independent', lower):
            dc_subproblems_not_independent = True

        if re.search(r'combine\s+step\s+intractable|combine\s+(?:step\s+)?requires\s+o\(2\^n\)|combine\s+step\s+is\s+np[- ]hard|dc_combine_step_intractable', lower):
            dc_combine_step_intractable = True

        if re.search(r'base\s+case\s+undefined|missing\s+base\s+case|infinite\s+recursion|dc_base_case_undefined', lower):
            dc_base_case_undefined = True

        if re.search(r'search\s+space\s+explosive|exponential\s+without\s+pruning|backtracking_search_space_explosive|decision\s+tree\s+too\s+large', lower):
            backtracking_search_space_explosive = True

        if re.search(r'insufficient\s+pruning|weak\s+pruning|backtracking_insufficient_pruning', lower):
            backtracking_search_space_explosive = True

        if re.search(r'greedy\s+sufficient|greedy\s+choice\s+property\s+holds|backtracking_greedy_sufficient', lower):
            backtracking_greedy_sufficient = True

        if re.search(r'dp\s+sufficient|overlapping\s+subproblems\s+admit\s+dp|polynomial\s+dp\s+exists|backtracking_dp_sufficient', lower):
            backtracking_dp_sufficient = True

        if re.search(r'recursion\s+depth\s+limit\s+exceeded|resource\s+limit\s+exceeded|backtracking_resource_limit', lower):
            backtracking_resource_limit_exceeded = True

        if (dc_is_inversions or dc_is_quickselect or dc_is_closest_pair or
            dc_is_tree_centroid or dc_is_cdq or bt_is_subsets_permutations or
            bt_is_csp or bt_is_branch_and_bound or bt_is_state_space_search or
            bt_is_meet_in_middle or is_cross_family or
            dc_subproblems_not_independent or dc_combine_step_intractable or
            dc_base_case_undefined or backtracking_search_space_explosive or
            backtracking_greedy_sufficient or backtracking_dp_sufficient or
            backtracking_resource_limit_exceeded or
            re.search(r'divide\s+and\s+conquer|backtracking', lower)):
            is_dc_backtracking_detected = True

        if is_dc_backtracking_detected:
            if is_cross_family:
                dc_backtracking_algorithm_family = "composition_unsupported"
                subproblem_dependency_kind = SubproblemDependencyKind.CROSS_DEPENDENT
                termination_guarantee_kind = TerminationGuaranteeKind.DECISION_CORRECTNESS
            elif dc_is_inversions:
                dc_backtracking_kind = DCBacktrackingKind.MERGE_SORT_INVERSIONS
                dc_backtracking_algorithm_family = "dc_merge_sort_inversions"
                subproblem_dependency_kind = SubproblemDependencyKind.DISJOINT
                termination_guarantee_kind = TerminationGuaranteeKind.COUNTING_CORRECTNESS
                dc_is_independent_subproblems = True
                dc_has_cross_boundary_combine = True
                dc_combine_complexity = "O(N)"
            elif dc_is_quickselect:
                dc_backtracking_kind = DCBacktrackingKind.QUICKSELECT
                dc_backtracking_algorithm_family = "dc_quickselect"
                subproblem_dependency_kind = SubproblemDependencyKind.DISJOINT
                termination_guarantee_kind = TerminationGuaranteeKind.OPTIMALITY
                dc_is_independent_subproblems = True
                dc_combine_complexity = "O(1)"
            elif dc_is_closest_pair:
                dc_backtracking_kind = DCBacktrackingKind.CLOSEST_PAIR
                dc_backtracking_algorithm_family = "dc_closest_pair"
                subproblem_dependency_kind = SubproblemDependencyKind.DISJOINT
                termination_guarantee_kind = TerminationGuaranteeKind.OPTIMALITY
                dc_is_independent_subproblems = True
                dc_has_cross_boundary_combine = True
                dc_combine_complexity = "O(N)"
            elif dc_is_tree_centroid:
                dc_backtracking_kind = DCBacktrackingKind.TREE_CENTROID
                dc_backtracking_algorithm_family = "dc_tree_centroid"
                subproblem_dependency_kind = SubproblemDependencyKind.DISJOINT
                termination_guarantee_kind = TerminationGuaranteeKind.COUNTING_CORRECTNESS
                dc_is_independent_subproblems = True
                dc_has_cross_boundary_combine = True
                dc_combine_complexity = "O(N)"
            elif dc_is_cdq:
                dc_backtracking_kind = DCBacktrackingKind.CDQ_DIVIDE_AND_CONQUER
                dc_backtracking_algorithm_family = "dc_cdq_divide_and_conquer"
                subproblem_dependency_kind = SubproblemDependencyKind.DISJOINT
                termination_guarantee_kind = TerminationGuaranteeKind.COUNTING_CORRECTNESS
                dc_is_independent_subproblems = True
                dc_has_cross_boundary_combine = True
                dc_combine_complexity = "O(N log N)"
            elif bt_is_subsets_permutations:
                dc_backtracking_kind = DCBacktrackingKind.SUBSETS_PERMUTATIONS
                dc_backtracking_algorithm_family = "backtracking_subsets_permutations"
                subproblem_dependency_kind = SubproblemDependencyKind.DISJOINT
                termination_guarantee_kind = TerminationGuaranteeKind.ENUMERATION_COMPLETENESS
                backtracking_is_exponential = True
                backtracking_state_restoration = True
                backtracking_decision_space_size = 20
            elif bt_is_csp:
                dc_backtracking_kind = DCBacktrackingKind.CONSTRAINT_SATISFACTION
                dc_backtracking_algorithm_family = "backtracking_constraint_satisfaction"
                subproblem_dependency_kind = SubproblemDependencyKind.DISJOINT
                termination_guarantee_kind = TerminationGuaranteeKind.FEASIBILITY
                backtracking_is_exponential = True
                backtracking_requires_pruning = True
                backtracking_pruning_kind = "feasibility"
                backtracking_state_restoration = True
                if re.search(r'exact\s+cover|dancing\s+links|algorithm\s+x', lower):
                    backtracking_is_exact_cover = True
                else:
                    backtracking_is_csp = True
            elif bt_is_branch_and_bound:
                dc_backtracking_kind = DCBacktrackingKind.BRANCH_AND_BOUND
                dc_backtracking_algorithm_family = "backtracking_branch_and_bound"
                subproblem_dependency_kind = SubproblemDependencyKind.DISJOINT
                termination_guarantee_kind = TerminationGuaranteeKind.OPTIMALITY
                backtracking_is_branch_and_bound = True
                backtracking_requires_pruning = True
                backtracking_pruning_kind = "optimality"
                backtracking_objective_direction = "MINIMIZE" if "min" in lower else "MAXIMIZE"
                backtracking_bound_type = "LOWER_BOUND" if backtracking_objective_direction == "MINIMIZE" else "UPPER_BOUND"
            elif bt_is_state_space_search:
                dc_backtracking_kind = DCBacktrackingKind.STATE_SPACE_SEARCH
                dc_backtracking_algorithm_family = "backtracking_state_space_search"
                subproblem_dependency_kind = SubproblemDependencyKind.DISJOINT
                termination_guarantee_kind = TerminationGuaranteeKind.FEASIBILITY
                backtracking_state_restoration = True
                backtracking_requires_pruning = True
                backtracking_pruning_kind = "feasibility"
            elif bt_is_meet_in_middle:
                dc_backtracking_kind = DCBacktrackingKind.MEET_IN_THE_MIDDLE
                dc_backtracking_algorithm_family = "backtracking_meet_in_the_middle"
                subproblem_dependency_kind = SubproblemDependencyKind.DISJOINT
                termination_guarantee_kind = TerminationGuaranteeKind.OPTIMALITY
                backtracking_is_meet_in_middle = True
                backtracking_split_strategy = "half_split"
            else:
                dc_backtracking_kind = DCBacktrackingKind.MERGE_SORT_INVERSIONS
                dc_backtracking_algorithm_family = "dc_merge_sort_inversions"
                subproblem_dependency_kind = SubproblemDependencyKind.DISJOINT
                termination_guarantee_kind = TerminationGuaranteeKind.COUNTING_CORRECTNESS
                dc_is_independent_subproblems = True
                dc_has_cross_boundary_combine = True
                dc_combine_complexity = "O(N)"

        # Phase 3N: Advanced Graph Algorithms via Semantic Derivation Engine
        is_adv_graph_detected = False
        adv_graph_algorithm_family = None
        adv_graph_semantic_model = None
        adv_graph_candidate_evaluations = []

        try:
            from pointer_algorithms.adv_graph.derivation_engine import AdvancedGraphDerivationEngine
            ag_engine = AdvancedGraphDerivationEngine()
            adv_graph_semantic_model = ag_engine.extract_semantic_model(text)
            ag_candidates, ag_selected = ag_engine.evaluate_candidates(adv_graph_semantic_model)
            adv_graph_candidate_evaluations = ag_candidates
            if ag_selected and not is_cross_family_composition:
                is_adv_graph_detected = True
                adv_graph_algorithm_family = ag_selected
        except Exception:
            pass

        # Phase 3O: String Algorithms & Automata via Semantic Derivation Engine
        is_string_algorithm_detected = False
        string_algorithm_family = None
        string_semantic_model = None
        string_candidate_evaluations = []

        try:
            from pointer_algorithms.strings.derivation_engine import StringDerivationEngine
            str_engine = StringDerivationEngine()
            string_semantic_model = str_engine.extract_semantic_model(text)
            str_candidates, str_selected = str_engine.evaluate_candidates(string_semantic_model)
            string_candidate_evaluations = str_candidates
            if str_selected and not is_cross_family_composition:
                is_string_algorithm_detected = True
                string_algorithm_family = str_selected
        except Exception:
            pass

        # Phase 3P: Number Theory & Combinatorics via Semantic Derivation Engine
        is_number_theory_detected = False
        number_theory_family = None
        number_theory_semantic_model = None
        number_theory_candidate_evaluations = []

        try:
            from pointer_algorithms.number_theory.derivation_engine import NumberTheoryDerivationEngine
            nt_engine = NumberTheoryDerivationEngine()
            number_theory_semantic_model = nt_engine.extract_semantic_model(text)
            nt_candidates, nt_selected = nt_engine.evaluate_candidates(number_theory_semantic_model)
            number_theory_candidate_evaluations = nt_candidates
            if nt_selected and not is_cross_family_composition:
                is_number_theory_detected = True
                number_theory_family = nt_selected
        except Exception:
            pass

        # Phase 3Q: Algebra & Transforms via Semantic Derivation Engine
        is_algebra_detected = False
        algebra_family = None
        algebra_semantic_model = None
        algebra_candidate_evaluations = []

        try:
            from pointer_algorithms.algebra.derivation_engine import AlgebraDerivationEngine
            alg_engine = AlgebraDerivationEngine()
            algebra_semantic_model = alg_engine.extract_semantic_model(text)
            alg_candidates, alg_selected = alg_engine.evaluate_candidates(algebra_semantic_model)
            algebra_candidate_evaluations = alg_candidates
            if alg_selected and not is_cross_family_composition:
                is_algebra_detected = True
                algebra_family = alg_selected
        except Exception:
            pass

        # Phase 3R: Computational Geometry via Semantic Derivation Engine
        is_geometry_detected = False
        geometry_family = None
        geometry_semantic_model = None
        geometry_candidate_evaluations = []

        try:
            from pointer_algorithms.geometry.derivation_engine import GeometryDerivationEngine
            geom_engine = GeometryDerivationEngine()
            geometry_semantic_model = geom_engine.extract_semantic_model(text)
            geom_candidates, geom_selected = geom_engine.evaluate_candidates(geometry_semantic_model)
            geometry_candidate_evaluations = geom_candidates
            if geom_selected and not is_cross_family_composition:
                is_geometry_detected = True
                geometry_family = geom_selected
        except Exception:
            pass

        # Phase 3S: Advanced Data Structures via Semantic Derivation Engine
        is_ads_detected = False
        ads_family = None
        ads_semantic_model = None
        ads_candidate_evaluations = []

        try:
            from pointer_algorithms.adv_data_structures.derivation_engine import AdvancedDataStructureDerivationEngine
            ads_engine = AdvancedDataStructureDerivationEngine()
            ads_semantic_model = ads_engine.extract_semantic_model(text)
            ads_candidates, ads_selected = ads_engine.evaluate_candidates(ads_semantic_model)
            ads_candidate_evaluations = ads_candidates
            if ads_selected and not is_cross_family_composition:
                is_ads_detected = True
                ads_family = ads_selected
        except Exception:
            pass

        # Phase 4: Cross-Family Composition via CrossFamilySynthesisEngine
        is_cross_family_detected = False
        cross_family_family = None
        cross_family_semantic_model = None
        cross_family_candidate_evaluations = []

        try:
            from pointer_algorithms.cross_family.facade import CrossFamilySynthesisEngine
            cf_engine = CrossFamilySynthesisEngine()
            cf_res = cf_engine.process(text)
            if cf_res.get("gate_passed") and cf_res.get("verified_plan"):
                is_cross_family_detected = True
                cross_family_family = cf_res["plan"].recipe_name
                cross_family_semantic_model = cf_res.get("model")
                if cf_res.get("eval_result"):
                    cross_family_candidate_evaluations = [cf_res["eval_result"]]
        except Exception:
            pass

        return ProblemFeatures(
            raw_text=text,
            input_structure=input_structure,
            output_requirement=output_requirement,
            is_sorted=is_sorted,
            can_sort=can_sort,
            requires_original_indices=requires_original_indices,
            has_negative_values=has_negative_values,
            is_contiguous=is_contiguous,
            tracks_distinct=tracks_distinct,
            optimization_objective=optimization_objective,
            search_objective=search_objective,
            partition_requirement=partition_requirement,
            in_place_required=in_place_required,
            has_dynamic_updates=has_dynamic_updates,
            repeated_queries=repeated_queries,
            target_value=target_value,
            window_size_k=window_size_k,
            # Monotonic Stack features
            nearest_boundary_query=nearest_boundary_query,
            boundary_relation=boundary_relation,
            boundary_direction=boundary_direction,
            comparison_strictness=comparison_strictness,
            is_circular=is_circular,
            contribution_objective=contribution_objective,
            histogram_pattern=histogram_pattern,
            has_stock_span_pattern=has_stock_span_pattern,
            has_duplicate_dominance=has_duplicate_dominance,
            # Binary Search features
            has_ordered_search_space=has_ordered_search_space,
            is_answer_space_search=is_answer_space_search,
            search_space_type=search_space_type,
            target_boundary=target_boundary,
            predicate_direction=predicate_direction,
            feasibility_objective=feasibility_objective,
            requires_exact_lookup=requires_exact_lookup,
            has_monotonic_predicate=has_monotonic_predicate,
            has_non_monotonic_predicate=has_non_monotonic_predicate,
            has_numeric_domain=has_numeric_domain,
            compound_with=compound_with,
            search_space_kind=search_space_kind,
            exact_match_semantics=exact_match_semantics,
            answer_space_low_expression=answer_space_low_expression,
            answer_space_high_expression=answer_space_high_expression,
            # Trie features
            trie_kind=trie_kind,
            prefix_query_type=prefix_query_type,
            trie_alphabet=trie_alphabet,
            trie_storage=trie_storage,
            estimated_node_count=estimated_node_count,
            estimated_memory_bytes=estimated_memory_bytes,
            memory_limit_bytes=memory_limit_bytes,
            memory_limit_exceeded=memory_limit_exceeded,
            has_single_query_only=has_single_query_only,
            has_prefix_sharing_advantage=has_prefix_sharing_advantage,
            # Tree features
            tree_kind=tree_kind,
            tree_representation=tree_representation,
            tree_traversal_order=tree_traversal_order,
            tree_aggregation_op=tree_aggregation_op,
            is_bst=is_bst,
            is_validating_bst=is_validating_bst,
            bst_duplicate_policy=bst_duplicate_policy,
            lca_query_type=lca_query_type,
            tree_dp_type=tree_dp_type,
            is_diameter_query=is_diameter_query,
            is_path_sum_query=is_path_sum_query,
            tree_node_count_n=tree_node_count_n,
            tree_max_depth_estimate=tree_max_depth_estimate,
            tree_recursion_risk=tree_recursion_risk,
            is_guaranteed_tree=is_guaranteed_tree,
            graph_edge_count_e=graph_edge_count_e,
            has_cycle_signal=has_cycle_signal,
            is_disconnected_signal=is_disconnected_signal,
            # Graph features
            graph_kind=graph_kind,
            graph_weight_kind=graph_weight_kind,
            graph_representation=graph_representation_gf,
            graph_has_negative_weights=graph_has_negative_weights,
            graph_has_negative_cycles=graph_has_negative_cycles,
            graph_is_directed=graph_is_directed,
            graph_is_weighted=graph_is_weighted,
            graph_is_cyclic=graph_is_cyclic,
            graph_is_dag=graph_is_dag,
            graph_is_bipartite=graph_is_bipartite,
            graph_is_disconnected=graph_is_disconnected,
            graph_vertex_count_v=graph_vertex_count_v,
            graph_index_base=graph_index_base,
            computational_budget=computational_budget,
            graph_query_type=graph_query_type,
            graph_algorithm_family=graph_algorithm_family,
            is_graph_detected=is_graph_detected,
            # Heap features (Phase 3G)
            is_heap_detected=is_heap_detected,
            heap_kind=heap_kind,
            heap_operation_kind=heap_operation_kind,
            heap_k_direction=heap_k_direction,
            heap_k_value=heap_k_value,
            heap_is_streaming=heap_is_streaming,
            heap_is_dynamic_median=heap_is_dynamic_median,
            heap_is_k_way_merge=heap_is_k_way_merge,
            heap_is_scheduling=heap_is_scheduling,
            heap_is_greedy_selection=heap_is_greedy_selection,
            heap_is_lazy_deletion=heap_is_lazy_deletion,
            heap_requires_arbitrary_delete=heap_requires_arbitrary_delete,
            heap_requires_full_sort=heap_requires_full_sort,
            heap_is_offline_kth=heap_is_offline_kth,
            heap_algorithm_family=heap_algorithm_family,
            # DSU features (Phase 3H)
            is_dsu_detected=is_dsu_detected,
            dsu_kind=dsu_kind,
            dsu_operation_kind=dsu_operation_kind,
            dsu_algorithm_family=dsu_algorithm_family,
            dsu_has_metadata=dsu_has_metadata,
            dsu_metadata_type=dsu_metadata_type,
            dsu_has_weights=dsu_has_weights,
            dsu_has_parity=dsu_has_parity,
            dsu_requires_rollback=dsu_requires_rollback,
            dsu_is_offline=dsu_is_offline,
            dsu_has_deletions=dsu_has_deletions,
            dsu_is_online_deletions=dsu_is_online_deletions,
            dsu_has_difference_query=dsu_has_difference_query,
            dsu_has_contradiction_check=dsu_has_contradiction_check,
            dsu_historical_queries=dsu_historical_queries,
            # Fenwick features (Phase 3I)
            is_fenwick_detected=is_fenwick_detected,
            fenwick_kind=fenwick_kind,
            fenwick_operation_kind=fenwick_operation_kind,
            fenwick_algorithm_family=fenwick_algorithm_family,
            fenwick_has_point_update=fenwick_has_point_update,
            fenwick_has_range_update=fenwick_has_range_update,
            fenwick_has_point_query=fenwick_has_point_query,
            fenwick_has_prefix_query=fenwick_has_prefix_query,
            fenwick_has_range_query=fenwick_has_range_query,
            fenwick_has_non_invertible_range=fenwick_has_non_invertible_range,
            fenwick_is_frequency=fenwick_is_frequency,
            fenwick_has_kth_query=fenwick_has_kth_query,
            fenwick_requires_coordinate_compression=fenwick_requires_coordinate_compression,
            fenwick_is_inversion_counting=fenwick_is_inversion_counting,
            fenwick_is_multiset=fenwick_is_multiset,
            fenwick_is_2d=fenwick_is_2d,
            fenwick_is_extremum=fenwick_is_extremum,
            fenwick_extremum_direction=fenwick_extremum_direction,
            fenwick_is_static=fenwick_is_static,
            fenwick_is_offline_range_add=fenwick_is_offline_range_add,
            fenwick_has_range_assignment=fenwick_has_range_assignment,
            fenwick_has_arbitrary_range_minmax=fenwick_has_arbitrary_range_minmax,
            fenwick_has_dynamic_unknown_coords=fenwick_has_dynamic_unknown_coords,
            fenwick_has_negative_frequencies=fenwick_has_negative_frequencies,
            fenwick_resource_exceeded=fenwick_resource_exceeded,
            # Segment Tree features (Phase 3J)
            is_segment_tree_detected=is_segment_tree_detected,
            segment_tree_kind=segment_tree_kind,
            segment_tree_operation_kind=segment_tree_operation_kind,
            segment_tree_algorithm_family=segment_tree_algorithm_family,
            segment_tree_has_point_update=segment_tree_has_point_update,
            segment_tree_has_range_update=segment_tree_has_range_update,
            segment_tree_has_range_add=segment_tree_has_range_add,
            segment_tree_has_range_assign=segment_tree_has_range_assign,
            segment_tree_has_combined_lazy=segment_tree_has_combined_lazy,
            segment_tree_has_range_query=segment_tree_has_range_query,
            segment_tree_query_op=segment_tree_query_op,
            segment_tree_is_metadata=segment_tree_is_metadata,
            segment_tree_is_max_subarray=segment_tree_is_max_subarray,
            segment_tree_is_frequency=segment_tree_is_frequency,
            segment_tree_is_interval_statistics=segment_tree_is_interval_statistics,
            segment_tree_is_static=segment_tree_is_static,
            segment_tree_is_simple_prefix=segment_tree_is_simple_prefix,
            segment_tree_is_offline_range_add=segment_tree_is_offline_range_add,
            segment_tree_is_fenwick_equivalent=segment_tree_is_fenwick_equivalent,
            segment_tree_has_no_associative_merge=segment_tree_has_no_associative_merge,
            segment_tree_has_unsupported_lazy=segment_tree_has_unsupported_lazy,
            segment_tree_resource_exceeded=segment_tree_resource_exceeded,
            segment_tree_has_negative_frequencies=segment_tree_has_negative_frequencies,
            # Dynamic Programming features (Phase 3K)
            is_dp_detected=is_dp_detected,
            dp_kind=dp_kind,
            dp_operation_kind=dp_operation_kind,
            dp_algorithm_family=dp_algorithm_family,
            dp_state_dimension=dp_state_dimension,
            dp_has_optimal_substructure=dp_has_optimal_substructure,
            dp_has_overlapping_subproblems=dp_has_overlapping_subproblems,
            dp_is_dag=dp_is_dag,
            dp_is_cyclic=dp_is_cyclic,
            dp_greedy_optimal=dp_greedy_optimal,
            dp_is_non_markovian=dp_is_non_markovian,
            dp_state_space_size=dp_state_space_size,
            dp_is_resource_exceeded=dp_is_resource_exceeded,
            dp_requires_reconstruction=dp_requires_reconstruction,
            dp_space_compressible=dp_space_compressible,
            dp_is_unbounded=dp_is_unbounded,
            dp_optimization_applicable=dp_optimization_applicable,
            # Greedy features (Phase 3L)
            is_greedy_detected=is_greedy_detected,
            greedy_kind=greedy_kind,
            greedy_proof_kind=greedy_proof_kind,
            greedy_algorithm_family=greedy_algorithm_family,
            greedy_ordering_candidate=greedy_ordering_candidate,
            greedy_has_local_choice=greedy_has_local_choice,
            greedy_has_exchange_signal=greedy_has_exchange_signal,
            greedy_has_dominance_signal=greedy_has_dominance_signal,
            greedy_has_staying_ahead_signal=greedy_has_staying_ahead_signal,
            greedy_has_cut_property_signal=greedy_has_cut_property_signal,
            greedy_has_matroid_signal=greedy_has_matroid_signal,
            greedy_requires_sorting=greedy_requires_sorting,
            greedy_requires_heap=greedy_requires_heap,
            greedy_requires_graph_structure=greedy_requires_graph_structure,
            greedy_objective_kind=greedy_objective_kind,
            greedy_feasibility_preserved=greedy_feasibility_preserved,
            greedy_counterexample_detected=greedy_counterexample_detected,
            greedy_proof_unestablished=greedy_proof_unestablished,
            greedy_competing_dp_signal=greedy_competing_dp_signal,
            greedy_has_greedy_choice=greedy_has_greedy_choice,
            greedy_has_optimal_substructure=greedy_has_optimal_substructure,
            # Divide & Conquer / Backtracking features (Phase 3M)
            is_dc_backtracking_detected=is_dc_backtracking_detected,
            dc_backtracking_kind=dc_backtracking_kind,
            subproblem_dependency_kind=subproblem_dependency_kind,
            termination_guarantee_kind=termination_guarantee_kind,
            dc_backtracking_algorithm_family=dc_backtracking_algorithm_family,
            dc_is_independent_subproblems=dc_is_independent_subproblems,
            dc_has_cross_boundary_combine=dc_has_cross_boundary_combine,
            dc_combine_complexity=dc_combine_complexity,
            dc_base_case_size=dc_base_case_size,
            dc_recursion_depth_limit=dc_recursion_depth_limit,
            backtracking_decision_space_size=backtracking_decision_space_size,
            backtracking_is_exponential=backtracking_is_exponential,
            backtracking_requires_pruning=backtracking_requires_pruning,
            backtracking_pruning_kind=backtracking_pruning_kind,
            backtracking_state_restoration=backtracking_state_restoration,
            backtracking_symmetry_breaking=backtracking_symmetry_breaking,
            backtracking_is_exact_cover=backtracking_is_exact_cover,
            backtracking_is_csp=backtracking_is_csp,
            backtracking_is_branch_and_bound=backtracking_is_branch_and_bound,
            backtracking_objective_direction=backtracking_objective_direction,
            backtracking_bound_type=backtracking_bound_type,
            backtracking_is_meet_in_middle=backtracking_is_meet_in_middle,
            backtracking_split_strategy=backtracking_split_strategy,
            backtracking_search_space_explosive=backtracking_search_space_explosive,
            backtracking_greedy_sufficient=backtracking_greedy_sufficient,
            backtracking_dp_sufficient=backtracking_dp_sufficient,
            dc_subproblems_not_independent=dc_subproblems_not_independent,
            dc_combine_step_intractable=dc_combine_step_intractable,
            dc_base_case_undefined=dc_base_case_undefined,
            backtracking_resource_limit_exceeded=backtracking_resource_limit_exceeded,
            is_cross_family_composition=is_cross_family_composition,
            composition_unsupported=composition_unsupported,
            is_adv_graph_detected=is_adv_graph_detected,
            adv_graph_algorithm_family=adv_graph_algorithm_family,
            adv_graph_semantic_model=adv_graph_semantic_model,
            adv_graph_candidate_evaluations=adv_graph_candidate_evaluations,
            is_string_algorithm_detected=is_string_algorithm_detected,
            string_algorithm_family=string_algorithm_family,
            string_semantic_model=string_semantic_model,
            string_candidate_evaluations=string_candidate_evaluations,
            is_number_theory_detected=is_number_theory_detected,
            number_theory_family=number_theory_family,
            number_theory_semantic_model=number_theory_semantic_model,
            number_theory_candidate_evaluations=number_theory_candidate_evaluations,
            is_algebra_detected=is_algebra_detected,
            algebra_family=algebra_family,
            algebra_semantic_model=algebra_semantic_model,
            algebra_candidate_evaluations=algebra_candidate_evaluations,
            is_geometry_detected=is_geometry_detected,
            geometry_family=geometry_family,
            geometry_semantic_model=geometry_semantic_model,
            geometry_candidate_evaluations=geometry_candidate_evaluations,
            is_ads_detected=is_ads_detected,
            ads_family=ads_family,
            ads_semantic_model=ads_semantic_model,
            ads_candidate_evaluations=ads_candidate_evaluations,
            is_cross_family_detected=is_cross_family_detected,
            cross_family_family=cross_family_family,
            cross_family_semantic_model=cross_family_semantic_model,
            cross_family_candidate_evaluations=cross_family_candidate_evaluations,
        )
