"""
Failure Classifier for Pointer-Based Algorithms.

Categorizes algorithmic and reasoning failures into principled failure classes.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any

class FailureCategory(str, Enum):
    WRONG_RECOGNITION = "WRONG_RECOGNITION"
    WRONG_PRECONDITION = "WRONG_PRECONDITION"
    WRONG_MONOTONICITY = "WRONG_MONOTONICITY"
    BROKEN_INVARIANT = "BROKEN_INVARIANT"
    INVALID_MOVEMENT_DERIVATION = "INVALID_MOVEMENT_DERIVATION"
    WRONG_PATTERN_FAMILY = "WRONG_PATTERN_FAMILY"
    WRONG_ALTERNATIVE_SELECTION = "WRONG_ALTERNATIVE_SELECTION"
    INDEX_PRESERVATION_ERROR = "INDEX_PRESERVATION_ERROR"
    DUPLICATE_HANDLING_ERROR = "DUPLICATE_HANDLING_ERROR"
    BOUNDARY_ERROR = "BOUNDARY_ERROR"
    OVERFLOW_ERROR = "OVERFLOW_ERROR"
    IMPLEMENTATION_ERROR = "IMPLEMENTATION_ERROR"
    VERIFICATION_FALSE_POSITIVE = "VERIFICATION_FALSE_POSITIVE"
    KNOWLEDGE_TRANSFER_FAILURE = "KNOWLEDGE_TRANSFER_FAILURE"

    # Backward compatibility aliases
    WINDOW_NOT_MONOTONIC = "WRONG_MONOTONICITY"
    LOSS_OF_INFORMATION = "INDEX_PRESERVATION_ERROR"
    WRONG_ALGORITHM = "WRONG_ALTERNATIVE_SELECTION"
    TERMINATION_ERROR = "BOUNDARY_ERROR"

    # ── Monotonic Stack Failure Categories (Phase 3B) ──
    MS_UNKNOWN_STRUCTURAL_PATTERN = "MS_UNKNOWN_STRUCTURAL_PATTERN"      # Could not recognize as any MS family
    MS_WRONG_RELATION = "MS_WRONG_RELATION"                               # Used > when < was required, or vice versa
    MS_WRONG_DIRECTION = "MS_WRONG_DIRECTION"                             # Scanned right when left was required
    MS_WRONG_STRICTNESS = "MS_WRONG_STRICTNESS"                           # Used >= when > was needed (or vice versa)
    MS_INVALID_ELIMINATION = "MS_INVALID_ELIMINATION"                     # Popped elements that should have been retained
    MS_INCORRECT_INVARIANT = "MS_INCORRECT_INVARIANT"                     # Stack order invariant violated
    MS_BOUNDARY_ERROR = "MS_BOUNDARY_ERROR"                               # Off-by-one in width/span computation
    MS_DUPLICATE_HANDLING = "MS_DUPLICATE_HANDLING"                       # Double-counted subarrays due to equal elements
    MS_CIRCULAR_INDEX_ERROR = "MS_CIRCULAR_INDEX_ERROR"                   # index % n used incorrectly or traversal not doubled
    MS_CONTRIBUTION_COUNT_ERROR = "MS_CONTRIBUTION_COUNT_ERROR"           # left[i]*right[i] count wrong for sum problems
    MS_COMPLEXITY_FAILURE = "MS_COMPLEXITY_FAILURE"                       # O(n²) approach used where O(n) is required
    MS_IMPLEMENTATION_BUG = "MS_IMPLEMENTATION_BUG"                       # Correct approach, wrong implementation detail
    MS_OUTPUT_ERROR = "MS_OUTPUT_ERROR"                                    # Wrong output format (values vs indices, etc.)

    # ── Binary Search Failure Categories (Phase 3C) ──
    BS_UNKNOWN_STRUCTURAL_PATTERN = "BS_UNKNOWN_STRUCTURAL_PATTERN"
    BS_WRONG_SEARCH_SPACE = "BS_WRONG_SEARCH_SPACE"
    BS_ORDERING_MISSED = "BS_ORDERING_MISSED"
    BS_PREDICATE_NOT_MONOTONE = "BS_PREDICATE_NOT_MONOTONE"
    BS_WRONG_PREDICATE_DIRECTION = "BS_WRONG_PREDICATE_DIRECTION"
    BS_WRONG_BOUNDARY = "BS_WRONG_BOUNDARY"
    BS_FIRST_TRUE_ERROR = "BS_FIRST_TRUE_ERROR"
    BS_LAST_TRUE_ERROR = "BS_LAST_TRUE_ERROR"
    BS_LOWER_BOUND_ERROR = "BS_LOWER_BOUND_ERROR"
    BS_UPPER_BOUND_ERROR = "BS_UPPER_BOUND_ERROR"
    BS_OFF_BY_ONE = "BS_OFF_BY_ONE"
    BS_TERMINATION_ERROR = "BS_TERMINATION_ERROR"
    BS_MIDPOINT_OVERFLOW = "BS_MIDPOINT_OVERFLOW"
    BS_NUMERIC_OVERFLOW = "BS_NUMERIC_OVERFLOW"
    BS_FEASIBILITY_CONSTRUCTION_ERROR = "BS_FEASIBILITY_CONSTRUCTION_ERROR"
    BS_COMPOUND_REASONING_ERROR = "BS_COMPOUND_REASONING_ERROR"
    BS_IMPLEMENTATION_BUG = "BS_IMPLEMENTATION_BUG"
    BS_OUTPUT_ERROR = "BS_OUTPUT_ERROR"

    # ── Trie Failure Categories (Phase 3D) ──
    TR_UNKNOWN_STRUCTURAL_PATTERN = "TR_UNKNOWN_STRUCTURAL_PATTERN"
    TR_WRONG_ALPHABET = "TR_WRONG_ALPHABET"
    TR_WRONG_CHILD_STORAGE = "TR_WRONG_CHILD_STORAGE"
    TR_MISSING_TERMINAL_MARKER = "TR_MISSING_TERMINAL_MARKER"
    TR_PREFIX_VS_WORD_CONFUSION = "TR_PREFIX_VS_WORD_CONFUSION"
    TR_DELETION_PRUNING_ERROR = "TR_DELETION_PRUNING_ERROR"
    TR_DUAL_COUNTER_CORRUPTION = "TR_DUAL_COUNTER_CORRUPTION"
    TR_BINARY_TRIE_BIT_WIDTH_ERROR = "TR_BINARY_TRIE_BIT_WIDTH_ERROR"
    TR_GREEDY_XOR_WRONG_BRANCH = "TR_GREEDY_XOR_WRONG_BRANCH"
    TR_MEMORY_LIMIT_EXCEEDED = "TR_MEMORY_LIMIT_EXCEEDED"
    TR_LEXICOGRAPHIC_TRAVERSAL_ERROR = "TR_LEXICOGRAPHIC_TRAVERSAL_ERROR"
    TR_AUTOCOMPLETE_LIMIT_ERROR = "TR_AUTOCOMPLETE_LIMIT_ERROR"
    TR_IMPLEMENTATION_BUG = "TR_IMPLEMENTATION_BUG"
    TR_OUTPUT_ERROR = "TR_OUTPUT_ERROR"

    # ── Tree Failure Categories (Phase 3E) ──
    TREE_UNKNOWN_STRUCTURAL_PATTERN = "TREE_UNKNOWN_STRUCTURAL_PATTERN"
    TREE_WRONG_TRAVERSAL_ORDER = "TREE_WRONG_TRAVERSAL_ORDER"
    TREE_CYCLIC_GRAPH = "TREE_CYCLIC_GRAPH"
    TREE_DISCONNECTED_GRAPH = "TREE_DISCONNECTED_GRAPH"
    TREE_INVALID_BST_STRUCTURE = "TREE_INVALID_BST_STRUCTURE"
    TREE_BST_VIOLATION = "TREE_BST_VIOLATION"
    TREE_BST_DUPLICATE_ERROR = "TREE_BST_DUPLICATE_ERROR"
    TREE_LCA_METHOD_MISMATCH = "TREE_LCA_METHOD_MISMATCH"
    TREE_SUBTREE_AGGREGATION_ERROR = "TREE_SUBTREE_AGGREGATION_ERROR"
    TREE_DP_STATE_MISMATCH = "TREE_DP_STATE_MISMATCH"
    TREE_DP_TRANSITION_ERROR = "TREE_DP_TRANSITION_ERROR"
    TREE_RECURSION_LIMIT_EXCEEDED = "TREE_RECURSION_LIMIT_EXCEEDED"
    TREE_PARENT_VISIT_CYCLE = "TREE_PARENT_VISIT_CYCLE"
    TREE_DIAMETER_PATH_ERROR = "TREE_DIAMETER_PATH_ERROR"
    TREE_ARITY_MISMATCH = "TREE_ARITY_MISMATCH"
    TREE_NULL_POINTER_DEREFERENCE = "TREE_NULL_POINTER_DEREFERENCE"
    TREE_BASE_CASE_ERROR = "TREE_BASE_CASE_ERROR"
    TREE_IMPLEMENTATION_BUG = "TREE_IMPLEMENTATION_BUG"
    TREE_OUTPUT_ERROR = "TREE_OUTPUT_ERROR"

    # ── Graph Failure Categories (Phase 3F) ──
    GRAPH_REPRESENTATION_ERROR = "GRAPH_REPRESENTATION_ERROR"       # Could not parse graph structure (directed/undirected/weighted)
    STRUCTURE_CLASSIFICATION_ERROR = "STRUCTURE_CLASSIFICATION_ERROR"  # Wrong domain classification (tree vs graph)
    ALGORITHM_SELECTION_ERROR = "ALGORITHM_SELECTION_ERROR"         # Wrong algorithm selected (Dijkstra on neg weights, etc.)
    STATE_MODEL_ERROR = "STATE_MODEL_ERROR"                         # Wrong state (UNVISITED/VISITING/VISITED mismatch)
    TRANSITION_ERROR = "TRANSITION_ERROR"                           # Wrong relaxation/expansion step
    CONSTRAINT_ANALYSIS_ERROR = "CONSTRAINT_ANALYSIS_ERROR"         # Wrong constraint analysis (cycle exists misclassified)
    COMPLEXITY_ESTIMATION_ERROR = "COMPLEXITY_ESTIMATION_ERROR"     # Floyd-Warshall on V=100K, etc.
    CODE_GENERATION_ERROR = "CODE_GENERATION_ERROR"                 # Generated code is syntactically/semantically wrong
    NUMERIC_ERROR = "NUMERIC_ERROR"                                 # Integer overflow, wrong INF, 32-bit distance overflow
    UNSUPPORTED_COMPOUND_GRAPH = "UNSUPPORTED_COMPOUND_GRAPH"       # Graph + another domain (e.g. Graph + Segment Tree)

    # ── Heap Failure Categories (Phase 3G) ──
    HEAP_UNKNOWN_STRUCTURAL_PATTERN = "HEAP_UNKNOWN_STRUCTURAL_PATTERN"
    HEAP_WRONG_EXTREMUM = "HEAP_WRONG_EXTREMUM"
    HEAP_CAPACITY_MISMATCH = "HEAP_CAPACITY_MISMATCH"
    HEAP_UNNECESSARY_SORTING = "HEAP_UNNECESSARY_SORTING"
    HEAP_ARBITRARY_DELETE_MISMATCH = "HEAP_ARBITRARY_DELETE_MISMATCH"
    HEAP_UPDATE_SEMANTICS_MISMATCH = "HEAP_UPDATE_SEMANTICS_MISMATCH"
    HEAP_COMPLEXITY_EXCEEDED = "HEAP_COMPLEXITY_EXCEEDED"
    HEAP_ORDER_VIOLATION = "HEAP_ORDER_VIOLATION"
    HEAP_EMPTY_ACCESS_ERROR = "HEAP_EMPTY_ACCESS_ERROR"
    HEAP_DUAL_PARTITION_UNBALANCED = "HEAP_DUAL_PARTITION_UNBALANCED"
    HEAP_IMPLEMENTATION_BUG = "HEAP_IMPLEMENTATION_BUG"
    HEAP_OUTPUT_ERROR = "HEAP_OUTPUT_ERROR"

    # ── DSU Failure Categories (Phase 3H) ──
    DSU_UNKNOWN_STRUCTURAL_PATTERN = "DSU_UNKNOWN_STRUCTURAL_PATTERN"
    DSU_DELETION_UNSUPPORTED = "DSU_DELETION_UNSUPPORTED"
    DSU_ONLINE_OFFLINE_MISMATCH = "DSU_ONLINE_OFFLINE_MISMATCH"
    DSU_WEIGHT_MODEL_MISMATCH = "DSU_WEIGHT_MODEL_MISMATCH"
    DSU_PARITY_MODEL_MISMATCH = "DSU_PARITY_MODEL_MISMATCH"
    DSU_ROLLBACK_REQUIRED = "DSU_ROLLBACK_REQUIRED"
    DSU_METADATA_MERGE_UNDEFINED = "DSU_METADATA_MERGE_UNDEFINED"
    DSU_CONTRADICTION_DETECTED = "DSU_CONTRADICTION_DETECTED"
    DSU_COMPLEXITY_EXCEEDED = "DSU_COMPLEXITY_EXCEEDED"
    DSU_PATH_COMPRESSION_ROLLBACK_CONFLICT = "DSU_PATH_COMPRESSION_ROLLBACK_CONFLICT"
    DSU_POTENTIAL_ACCUMULATION_ERROR = "DSU_POTENTIAL_ACCUMULATION_ERROR"
    DSU_PARITY_XOR_ERROR = "DSU_PARITY_XOR_ERROR"
    DSU_IMPLEMENTATION_BUG = "DSU_IMPLEMENTATION_BUG"
    DSU_OUTPUT_ERROR = "DSU_OUTPUT_ERROR"

    # ── Fenwick Tree Failure Categories (Phase 3I) ──
    FENWICK_UNKNOWN_STRUCTURAL_PATTERN = "FENWICK_UNKNOWN_STRUCTURAL_PATTERN"
    FENWICK_STATIC_QUERY_SUBOPTIMAL = "FENWICK_STATIC_QUERY_SUBOPTIMAL"
    FENWICK_OFFLINE_RANGE_ADD_OVERKILL = "FENWICK_OFFLINE_RANGE_ADD_OVERKILL"
    FENWICK_STRUCTURAL_INCOMPATIBILITY = "FENWICK_STRUCTURAL_INCOMPATIBILITY"
    FENWICK_DYNAMIC_COORDINATE_UNREPRESENTABLE = "FENWICK_DYNAMIC_COORDINATE_UNREPRESENTABLE"
    FENWICK_KTH_NEGATIVE_FREQUENCY = "FENWICK_KTH_NEGATIVE_FREQUENCY"
    FENWICK_RESOURCE_LIMIT = "FENWICK_RESOURCE_LIMIT"
    FENWICK_DIMENSION_MISMATCH = "FENWICK_DIMENSION_MISMATCH"
    FENWICK_OPERATION_MISMATCH = "FENWICK_OPERATION_MISMATCH"
    FENWICK_COORDINATE_COMPRESSION_UNNECESSARY = "FENWICK_COORDINATE_COMPRESSION_UNNECESSARY"
    FENWICK_COMPLEXITY_EXCEEDED = "FENWICK_COMPLEXITY_EXCEEDED"
    FENWICK_INDEX_OUT_OF_BOUNDS = "FENWICK_INDEX_OUT_OF_BOUNDS"
    FENWICK_IMPLEMENTATION_BUG = "FENWICK_IMPLEMENTATION_BUG"
    FENWICK_OUTPUT_ERROR = "FENWICK_OUTPUT_ERROR"

    # ── Segment Tree Failure Categories (Phase 3J) ──
    SEGMENT_TREE_STATIC_QUERY_SUBOPTIMAL = "SEGMENT_TREE_STATIC_QUERY_SUBOPTIMAL"
    SEGMENT_TREE_SIMPLE_PREFIX_OVERKILL = "SEGMENT_TREE_SIMPLE_PREFIX_OVERKILL"
    SEGMENT_TREE_DIFFERENCE_ARRAY_OVERKILL = "SEGMENT_TREE_DIFFERENCE_ARRAY_OVERKILL"
    SEGMENT_TREE_FENWICK_EQUIVALENT = "SEGMENT_TREE_FENWICK_EQUIVALENT"
    SEGMENT_TREE_NO_ASSOCIATIVE_MERGE = "SEGMENT_TREE_NO_ASSOCIATIVE_MERGE"
    SEGMENT_TREE_STANDARD_LAZY_INSUFFICIENT = "SEGMENT_TREE_STANDARD_LAZY_INSUFFICIENT"
    SEGMENT_TREE_LAZY_TAG_UNSUPPORTED = "SEGMENT_TREE_STANDARD_LAZY_INSUFFICIENT"  # Deprecated alias
    SEGMENT_TREE_RESOURCE_LIMIT = "SEGMENT_TREE_RESOURCE_LIMIT"
    SEGMENT_TREE_KTH_NEGATIVE_FREQUENCY = "SEGMENT_TREE_KTH_NEGATIVE_FREQUENCY"
    SEGMENT_TREE_OPERATION_MISMATCH = "SEGMENT_TREE_OPERATION_MISMATCH"
    SEGMENT_TREE_COMPLEXITY_EXCEEDED = "SEGMENT_TREE_COMPLEXITY_EXCEEDED"
    SEGMENT_TREE_IMPLEMENTATION_BUG = "SEGMENT_TREE_IMPLEMENTATION_BUG"

    # ── Dynamic Programming Failure Categories (Phase 3K) ──
    DP_DOMINATED_BY_GREEDY = "DP_DOMINATED_BY_GREEDY"
    DP_GREEDY_CHOICE_OPTIMAL = "DP_DOMINATED_BY_GREEDY"  # Backward-compatible alias
    DP_CYCLIC_STATE_DEPENDENCY = "DP_CYCLIC_STATE_DEPENDENCY"
    DP_NO_OPTIMAL_SUBSTRUCTURE = "DP_NO_OPTIMAL_SUBSTRUCTURE"
    DP_NO_REUSE_BENEFIT = "DP_NO_REUSE_BENEFIT"
    DP_NO_OVERLAPPING_SUBPROBLEMS = "DP_NO_REUSE_BENEFIT"  # Backward-compatible alias
    DP_NON_MARKOVIAN_FUTURE_DEPENDENCE = "DP_NON_MARKOVIAN_FUTURE_DEPENDENCE"
    DP_STATE_SPACE_EXPLOSION = "DP_STATE_SPACE_EXPLOSION"
    DP_UNPROVEN_OPTIMIZATION_PREREQUISITE = "DP_UNPROVEN_OPTIMIZATION_PREREQUISITE"
    DP_OPERATION_MISMATCH = "DP_OPERATION_MISMATCH"
    DP_RESOURCE_LIMIT = "DP_RESOURCE_LIMIT"
    DP_IMPLEMENTATION_BUG = "DP_IMPLEMENTATION_BUG"

    # ── Greedy Failure Categories (Phase 3L) ──
    GREEDY_NO_SAFE_LOCAL_CHOICE = "GREEDY_NO_SAFE_LOCAL_CHOICE"
    GREEDY_EXCHANGE_PROOF_FAILED = "GREEDY_EXCHANGE_PROOF_FAILED"
    GREEDY_STAYING_AHEAD_FAILED = "GREEDY_STAYING_AHEAD_FAILED"
    GREEDY_DOMINANCE_FAILED = "GREEDY_DOMINANCE_FAILED"
    GREEDY_LOOKAHEAD_REQUIRED = "GREEDY_LOOKAHEAD_REQUIRED"
    GREEDY_OBJECTIVE_MISMATCH = "GREEDY_OBJECTIVE_MISMATCH"
    GREEDY_COUNTEREXAMPLE_FOUND = "GREEDY_COUNTEREXAMPLE_FOUND"
    GREEDY_PROOF_NOT_ESTABLISHED = "GREEDY_PROOF_NOT_ESTABLISHED"
    GREEDY_MATROID_PREREQUISITE_UNPROVEN = "GREEDY_MATROID_PREREQUISITE_UNPROVEN"
    GREEDY_RESOURCE_LIMIT = "GREEDY_RESOURCE_LIMIT"
    GREEDY_IMPLEMENTATION_BUG = "GREEDY_IMPLEMENTATION_BUG"

    # ── Divide & Conquer and Backtracking Failure Categories (Phase 3M) ──
    DC_SUBPROBLEMS_NOT_INDEPENDENT = "DC_SUBPROBLEMS_NOT_INDEPENDENT"
    DC_COMBINE_STEP_INTRACTABLE = "DC_COMBINE_STEP_INTRACTABLE"
    DC_BASE_CASE_UNDEFINED = "DC_BASE_CASE_UNDEFINED"
    BACKTRACKING_SEARCH_SPACE_EXPLOSIVE = "BACKTRACKING_SEARCH_SPACE_EXPLOSIVE"
    BACKTRACKING_INSUFFICIENT_PRUNING = "BACKTRACKING_INSUFFICIENT_PRUNING"
    BACKTRACKING_STATE_RESTORATION_DEFECT = "BACKTRACKING_STATE_RESTORATION_DEFECT"
    BACKTRACKING_SYMMETRY_NOT_BROKEN = "BACKTRACKING_SYMMETRY_NOT_BROKEN"
    BACKTRACKING_LOOKAHEAD_MISMATCH = "BACKTRACKING_LOOKAHEAD_MISMATCH"
    BACKTRACKING_GREEDY_SUFFICIENT = "BACKTRACKING_GREEDY_SUFFICIENT"
    BACKTRACKING_DP_SUFFICIENT = "BACKTRACKING_DP_SUFFICIENT"
    BACKTRACKING_RESOURCE_LIMIT = "BACKTRACKING_RESOURCE_LIMIT"
    COMPOSITION_UNSUPPORTED = "COMPOSITION_UNSUPPORTED"

@dataclass
class FailureClassification:
    category: FailureCategory
    description: str
    suggested_alternative: Optional[str]
    root_cause_analysis: str

class FailureClassifier:

    @staticmethod
    def classify(error_signal: str, context: Dict[str, Any]) -> FailureClassification:
        sig = error_signal.upper()

        if "NEGATIVE_SUM" in sig or "WINDOW_NOT_MONOTONIC" in sig:
            return FailureClassification(
                category=FailureCategory.WINDOW_NOT_MONOTONIC,
                description="Greedy window shrinking was applied to a sequence whose cumulative property is not monotonic.",
                suggested_alternative="prefix_sum_hash_map",
                root_cause_analysis="Cumulative sum fluctuates in both directions due to negative values, so shrinking left does not guarantee monotonic reduction toward valid bound."
            )

        if "UNSORTED" in sig and context.get("requires_original_indices"):
            return FailureClassification(
                category=FailureCategory.LOSS_OF_INFORMATION,
                description="Sorting an unsorted array destroyed required original index positions.",
                suggested_alternative="hash_map_pair_lookup_or_pair_with_index",
                root_cause_analysis="In-place sort permuted elements without preserving (value, original_index) tracking pairs."
            )

        if "DYNAMIC_UPDATES" in sig or "POINT_UPDATE" in sig:
            return FailureClassification(
                category=FailureCategory.WRONG_ALGORITHM,
                description="Two pointers cannot maintain range queries when arbitrary dynamic point updates interleave queries.",
                suggested_alternative="segment_tree_or_fenwick",
                root_cause_analysis="Static/stream two-pointer scan assumes state is invariant to future point updates."
            )

        if "INFINITE_LOOP" in sig or "NO_ADVANCE" in sig:
            return FailureClassification(
                category=FailureCategory.TERMINATION_ERROR,
                description="Neither pointer advanced in an iteration, leading to non-termination.",
                suggested_alternative=None,
                root_cause_analysis="Branch conditions failed to cover all equality or threshold cases, stalling progress."
            )

        # ── Trie Classification (Phase 3D) ──
        if "TRIE_MEMORY" in sig or "MEMORY_LIMIT" in sig:
            return FailureClassification(
                category=FailureCategory.TR_MEMORY_LIMIT_EXCEEDED,
                description="Trie pointer allocation exceeded memory budget.",
                suggested_alternative="hash_set_or_sort",
                root_cause_analysis="Full node branching factor consumed more memory than available heap constraints."
            )

        if "DUAL_COUNTER" in sig or "PASS_COUNT" in sig:
            return FailureClassification(
                category=FailureCategory.TR_DUAL_COUNTER_CORRUPTION,
                description="Dual counter pass_count or word_count inconsistent with dictionary state.",
                suggested_alternative="trie_with_dual_counters",
                root_cause_analysis="pass_count was not decremented on deletion or word_count was checked instead of pass_count for prefix."
            )

        if "XOR_BRANCH" in sig or "GREEDY_XOR" in sig:
            return FailureClassification(
                category=FailureCategory.TR_GREEDY_XOR_WRONG_BRANCH,
                description="Binary Trie took non-optimal bit branch during XOR query.",
                suggested_alternative="binary_trie_max_xor",
                root_cause_analysis="Branching did not prioritize 1 - bit over bit, violating power-of-two strict dominance."
            )

        if "DELETION_PRUNING" in sig or "UNLINK" in sig:
            return FailureClassification(
                category=FailureCategory.TR_DELETION_PRUNING_ERROR,
                description="Node unlinked while other active words share its prefix.",
                suggested_alternative="safe_trie_pruning",
                root_cause_analysis="Node was pruned with pass_count > 0, severing descendants of other dictionary words."
            )

        # ── Tree Failure Classification (Phase 3E) ──
        if "TREE_CYCLIC" in sig or "CYCLE_IN_GRAPH" in sig:
            return FailureClassification(
                category=FailureCategory.TREE_CYCLIC_GRAPH,
                description="Graph contains cycles (E >= N in connected component), violating acyclic tree structure.",
                suggested_alternative="general_graph_dfs_bfs_or_union_find",
                root_cause_analysis="Attempted tree-specific algorithm on graph with back-edges or redundant connections."
            )

        if "TREE_DISCONNECTED" in sig or "FOREST" in sig:
            return FailureClassification(
                category=FailureCategory.TREE_DISCONNECTED_GRAPH,
                description="Graph is disconnected (E < N - 1), forming a forest rather than a single tree.",
                suggested_alternative="connected_components_or_union_find",
                root_cause_analysis="Tree traversal halted early because graph had multiple disconnected components."
            )

        if "BST_VIOLATION" in sig or "INVALID_BST" in sig:
            return FailureClassification(
                category=FailureCategory.TREE_INVALID_BST_STRUCTURE,
                description="BST ordered-branch elimination applied to non-BST tree.",
                suggested_alternative="general_binary_tree_traversal",
                root_cause_analysis="Node ordering invariant (left < node < right) violated; branch elimination caused false negative."
            )

        if "ARITY_MISMATCH" in sig or "INORDER_K_ARY" in sig:
            return FailureClassification(
                category=FailureCategory.TREE_ARITY_MISMATCH,
                description="In-order traversal attempted on k-ary tree with arity > 2.",
                suggested_alternative="tree_dfs_preorder_or_postorder",
                root_cause_analysis="In-order traversal requires binary left-root-right symmetric decomposition."
            )

        if "RECURSION_LIMIT" in sig or "STACK_OVERFLOW" in sig:
            return FailureClassification(
                category=FailureCategory.TREE_RECURSION_LIMIT_EXCEEDED,
                description="Call stack overflow on skewed tree with N >= 10^5.",
                suggested_alternative="iterative_stack_traversal",
                root_cause_analysis="Recursive DFS depth reached O(N) in worst-case skewed tree, exceeding runtime stack limit."
            )

        if "PARENT_CYCLE" in sig or "VISIT_PARENT" in sig:
            return FailureClassification(
                category=FailureCategory.TREE_PARENT_VISIT_CYCLE,
                description="Undirected tree traversal revisited parent node.",
                suggested_alternative="parent_tracking_dfs",
                root_cause_analysis="Neighbor loop lacked `if (v != p)` condition, creating infinite cycle with parent."
            )

        if "LCA_METHOD" in sig or "LCA_MISMATCH" in sig:
            return FailureClassification(
                category=FailureCategory.TREE_LCA_METHOD_MISMATCH,
                description="Mismatched LCA method applied to incompatible tree structure.",
                suggested_alternative="tree_lca_binary_tree",
                root_cause_analysis="Used BST LCA on non-BST or parent-array LCA without parent pointers."
            )

        if "TREE_DP_STATE" in sig or "TREE_DP" in sig:
            return FailureClassification(
                category=FailureCategory.TREE_DP_STATE_MISMATCH,
                description="Tree DP state definition or transition formula incorrect.",
                suggested_alternative="two_state_tree_dp",
                root_cause_analysis="Subtree state did not capture all mutually exclusive choices needed by parent."
            )

        if "DIAMETER" in sig:
            return FailureClassification(
                category=FailureCategory.TREE_DIAMETER_PATH_ERROR,
                description="Diameter calculation failed to track two longest child branches.",
                suggested_alternative="tree_diameter_depth_merge",
                root_cause_analysis="Only tracked single deepest path or failed to update global maximum through LCA."
            )

        # ── Graph Failure Classification (Phase 3F) ──
        if "GRAPH_NEGATIVE_WEIGHTS" in sig or "DIJKSTRA_NEG" in sig:
            return FailureClassification(
                category=FailureCategory.ALGORITHM_SELECTION_ERROR,
                description="Dijkstra applied to graph with negative edge weights.",
                suggested_alternative="graph_bellman_ford",
                root_cause_analysis="Dijkstra's greedy relaxation invariant requires all edge weights w >= 0. Negative weights can cause the settled-node distance to be updated later, breaking optimality."
            )

        if "NEGATIVE_CYCLE" in sig or "NEG_CYCLE_PATH" in sig:
            return FailureClassification(
                category=FailureCategory.CONSTRAINT_ANALYSIS_ERROR,
                description="Shortest path is undefined due to a reachable negative cycle on the source→target path.",
                suggested_alternative="negative_cycle_detection_only",
                root_cause_analysis="A reachable negative cycle allows unbounded relaxation. Bellman-Ford detects (V-th round relaxation) but cannot produce finite distances."
            )

        if "GRAPH_CYCLIC_TOPO" in sig or "CYCLIC_DAG" in sig:
            return FailureClassification(
                category=FailureCategory.CONSTRAINT_ANALYSIS_ERROR,
                description="Topological sort attempted on a cyclic directed graph.",
                suggested_alternative="graph_cycle_detection_directed",
                root_cause_analysis="Topological ordering exists if and only if the directed graph is acyclic. Kahn's algorithm detects cycles via leftover nodes with non-zero in-degree."
            )

        if "FLOYD_COMPLEXITY" in sig or "GRAPH_COMPLEXITY" in sig:
            return FailureClassification(
                category=FailureCategory.COMPLEXITY_ESTIMATION_ERROR,
                description="Floyd-Warshall O(V^3) applied to graph with V too large.",
                suggested_alternative="graph_dijkstra",
                root_cause_analysis="Floyd-Warshall runs in O(V^3) time, which is feasible only for V <= ~400-500. For larger V, repeated Dijkstra or Bellman-Ford must be used."
            )

        if "GRAPH_DISCONNECTED_MST" in sig or "SPANNING_FOREST" in sig:
            return FailureClassification(
                category=FailureCategory.CONSTRAINT_ANALYSIS_ERROR,
                description="MST algorithm applied to disconnected graph.",
                suggested_alternative="minimum_spanning_forest",
                root_cause_analysis="MST requires all V vertices to be reachable. Disconnected graph produces a spanning forest, not a spanning tree."
            )

        if "DIRECTED_UNDIRECTED_MISMATCH" in sig or "WRONG_CYCLE_METHOD" in sig:
            return FailureClassification(
                category=FailureCategory.STATE_MODEL_ERROR,
                description="Undirected cycle detection method applied to directed graph.",
                suggested_alternative="graph_cycle_detection_directed",
                root_cause_analysis="In directed graphs, both forward and backward traversals are distinct. The visited+parent method does not distinguish back-edges from forward-edges."
            )

        if "BIPARTITE_ODD_CYCLE" in sig or "NON_BIPARTITE" in sig:
            return FailureClassification(
                category=FailureCategory.CONSTRAINT_ANALYSIS_ERROR,
                description="Bipartite coloring applied to graph with odd cycle (non-bipartite).",
                suggested_alternative="graph_cycle_detection_undirected",
                root_cause_analysis="A graph is bipartite iff it contains no odd-length cycle. 2-coloring will fail at the odd-cycle vertex, producing a contradiction."
            )

        if "GRAPH_NUMERIC" in sig or "INT_OVERFLOW" in sig or "WRONG_INF" in sig:
            return FailureClassification(
                category=FailureCategory.NUMERIC_ERROR,
                description="Numeric overflow or wrong INF sentinel in graph algorithm.",
                suggested_alternative="use_long_long_INF_1e18",
                root_cause_analysis="Graph distances may exceed 32-bit int range. Use long long with INF = 1e18 (or LLONG_MAX/2) to prevent overflow during relaxation."
            )

        if "GRAPH_STATE" in sig or "VISITING_STATE" in sig or "THREE_COLOR" in sig:
            return FailureClassification(
                category=FailureCategory.STATE_MODEL_ERROR,
                description="Incorrect 3-color DFS state tracking for directed cycle detection.",
                suggested_alternative="graph_cycle_detection_directed",
                root_cause_analysis="Directed cycle detection requires 3 states: UNVISITED=0, VISITING=1 (in current DFS stack), VISITED=2 (fully processed). Back-edge to VISITING=1 node indicates a cycle."
            )

        if "LOW_LINK" in sig or "BRIDGE_ERROR" in sig or "ARTICULATION_ERROR" in sig:
            return FailureClassification(
                category=FailureCategory.STATE_MODEL_ERROR,
                description="Incorrect low-link or discovery time computation for bridges/articulation points.",
                suggested_alternative="graph_bridges_articulation",
                root_cause_analysis="Bridges: low[v] > tin[u]. Articulation points: root with 2+ children, or non-root with low[v] >= tin[u]. Discovery time tin[] and low[] must be correctly maintained during DFS."
            )

        if "GRAPH_REPR" in sig or "WRONG_REPRESENTATION" in sig:
            return FailureClassification(
                category=FailureCategory.GRAPH_REPRESENTATION_ERROR,
                description="Graph representation mismatch (adjacency matrix vs list vs edge list).",
                suggested_alternative="adjacency_list",
                root_cause_analysis="Problem input format did not match expected graph representation. Adjacency list is default; matrix is used only for dense small-V graphs."
            )

        if "TREE_VS_GRAPH" in sig or "DOMAIN_MISMATCH" in sig:
            return FailureClassification(
                category=FailureCategory.STRUCTURE_CLASSIFICATION_ERROR,
                description="Problem routed to wrong domain (Tree vs Graph).",
                suggested_alternative="tree_or_graph_domain_routing",
                root_cause_analysis="Trees are connected acyclic undirected graphs with N-1 edges. Graph-specific operations (shortest path, MST, SCC) should route to Graph; tree-specific operations (LCA, BST, tree DP) to Tree."
            )

        # ── Heap Failure Classifications (Phase 3G) ──

        if "HEAP_WRONG_EXTREMUM" in sig or "WRONG_HEAP_KIND" in sig:
            return FailureClassification(
                category=FailureCategory.HEAP_WRONG_EXTREMUM,
                description="Inverted heap kind for bounded retention (e.g. max-heap used for top-K largest).",
                suggested_alternative="min_heap_for_top_k_largest",
                root_cause_analysis="Retention Invariant: To maintain the K largest elements in O(K) space, the weakest element to evict is the minimum. A min-heap must be used; a max-heap cannot expose the minimum in O(1)."
            )

        if "HEAP_ARBITRARY_DELETE" in sig or "ARBITRARY_DELETE_MISMATCH" in sig:
            return FailureClassification(
                category=FailureCategory.HEAP_ARBITRARY_DELETE_MISMATCH,
                description="Standard binary heap used for arbitrary key deletion by value.",
                suggested_alternative="std::set_or_multiset",
                root_cause_analysis="Standard binary heap requires O(N) linear scan to locate arbitrary elements by value. Balanced BST (std::set/multiset) or hash table is required for O(log N) or O(1) arbitrary key lookup and erase."
            )

        if "HEAP_UNNECESSARY_SORTING" in sig:
            return FailureClassification(
                category=FailureCategory.HEAP_UNNECESSARY_SORTING,
                description="Unnecessary total sort performed where partial order / heap suffices, or vice versa.",
                suggested_alternative="heap_top_k_or_std_sort",
                root_cause_analysis="Top-K requires only O(N log K) time with a bounded heap instead of O(N log N) total sorting. Conversely, full offline sorting of an array is faster with introsort (std::sort) than heapsort."
            )

        if "HEAP_CAPACITY_MISMATCH" in sig or "CAPACITY_MISMATCH" in sig:
            return FailureClassification(
                category=FailureCategory.HEAP_CAPACITY_MISMATCH,
                description="The heap exceeds the allowed retention capacity or fails to enforce the required bounded-state invariant.",
                suggested_alternative="bound_heap_size_to_k",
                root_cause_analysis="Bounded Top-K must enforce the bounded-state invariant heap_size <= K (and heap_size == K after at least K elements are processed) to achieve O(K) space and O(N log K) runtime."
            )

        if "HEAP_DUAL_PARTITION" in sig or "MEDIAN_UNBALANCED" in sig:
            return FailureClassification(
                category=FailureCategory.HEAP_DUAL_PARTITION_UNBALANCED,
                description="Dual-heap partition balance invariant violated.",
                suggested_alternative="rebalance_dual_heaps",
                root_cause_analysis="Dynamic median requires maintaining |low| - |high| in {0, 1} and low.top() <= high.top(). Failure to rebalance produces an incorrect median."
            )

        if "HEAP_EMPTY_ACCESS" in sig:
            return FailureClassification(
                category=FailureCategory.HEAP_EMPTY_ACCESS_ERROR,
                description="Attempted top() or pop() on empty priority queue.",
                suggested_alternative="check_empty_before_access",
                root_cause_analysis="Calling top() or pop() on empty std::priority_queue triggers undefined behavior."
            )

        # ── DSU Failure Classifications (Phase 3H) ──
        if "DSU_DELETION_UNSUPPORTED" in sig:
            return FailureClassification(
                category=FailureCategory.DSU_DELETION_UNSUPPORTED,
                description="Arbitrary online edge deletion cannot be handled by standard DSU or Rollback DSU merely because rollback exists.",
                suggested_alternative="dsu_offline_dynamic_connectivity_or_link_cut_tree",
                root_cause_analysis="Arbitrary online edge deletion cannot be handled by standard DSU or Rollback DSU merely because rollback exists. Supported: additions only -> Basic DSU; explicit historical rollback -> Rollback DSU; known add/remove timeline -> Offline Dynamic Connectivity."
            )

        if "DSU_ONLINE_OFFLINE_MISMATCH" in sig:
            return FailureClassification(
                category=FailureCategory.DSU_ONLINE_OFFLINE_MISMATCH,
                description="Mismatch between online stream requirements and offline segment tree over time.",
                suggested_alternative="dsu_dynamic_connectivity_or_offline",
                root_cause_analysis="Offline dynamic connectivity requires all query timelines and edge active intervals to be known in advance to build the segment tree over time. It cannot be used when queries arrive strictly online and require immediate answers."
            )

        if "DSU_WEIGHT_MODEL_MISMATCH" in sig:
            return FailureClassification(
                category=FailureCategory.DSU_WEIGHT_MODEL_MISMATCH,
                description="Problem requires tracking potential differences (value[x] - value[y] = w) but unweighted DSU was selected.",
                suggested_alternative="dsu_weighted",
                root_cause_analysis="Basic DSU only maintains boolean component equivalence classes. Maintaining relative potential differences requires potential vectors updated via path compression and offset addition during union."
            )

        if "DSU_PARITY_MODEL_MISMATCH" in sig:
            return FailureClassification(
                category=FailureCategory.DSU_PARITY_MODEL_MISMATCH,
                description="Problem requires dynamic 2-coloring / parity relations but basic DSU was selected.",
                suggested_alternative="dsu_parity",
                root_cause_analysis="Basic DSU cannot verify whether an added edge creates an odd-length cycle. Parity DSU tracks XOR color offsets to root (color[x] ^ color[root]) to detect bipartite violations dynamically in O(alpha(N))."
            )

        if "DSU_ROLLBACK_REQUIRED" in sig:
            return FailureClassification(
                category=FailureCategory.DSU_ROLLBACK_REQUIRED,
                description="Reversible operations or snapshot rollback required but path-compressed DSU was selected.",
                suggested_alternative="dsu_rollback",
                root_cause_analysis="Path compression flattens tree structures permanently, destroying the exact mutation history. Rollback DSU must disable path compression and use union-by-size with an undo history stack to support O(1) state restoration."
            )

        if "DSU_METADATA_MERGE_UNDEFINED" in sig:
            return FailureClassification(
                category=FailureCategory.DSU_METADATA_MERGE_UNDEFINED,
                description="The requested component state cannot be maintained correctly from the stored metadata and the available merge operation.",
                suggested_alternative="dsu_basic",
                root_cause_analysis="The requested component state cannot be maintained correctly from the stored metadata and the available merge operation."
            )

        if "DSU_CONTRADICTION_DETECTED" in sig:
            return FailureClassification(
                category=FailureCategory.DSU_CONTRADICTION_DETECTED,
                description="Contradictory constraint asserted between already connected vertices.",
                suggested_alternative="dsu_constraint_consistency",
                root_cause_analysis="In Weighted or Parity DSU, two elements in the same connected component have their relative potential or parity uniquely fixed. Asserting a new constraint that differs from the existing path difference creates an unsatisfiable system."
            )

        if "DSU_COMPLEXITY_EXCEEDED" in sig:
            return FailureClassification(
                category=FailureCategory.DSU_COMPLEXITY_EXCEEDED,
                description="Repeated BFS/DFS rebuilds used instead of nearly linear DSU.",
                suggested_alternative="dsu_dynamic_connectivity",
                root_cause_analysis="Rebuilding the graph via BFS/DFS on every query takes O(Q * (V + E)), leading to Time Limit Exceeded. DSU answers connectivity in O(Q * alpha(V))."
            )

        if "DSU_PATH_COMPRESSION_ROLLBACK_CONFLICT" in sig:
            return FailureClassification(
                category=FailureCategory.DSU_PATH_COMPRESSION_ROLLBACK_CONFLICT,
                description="Path compression was erroneously enabled in Rollback DSU.",
                suggested_alternative="disable_path_compression_for_rollback",
                root_cause_analysis="Path compression performs an arbitrary number of pointer rewrites per find, which cannot be undone without logging every traversal step. Rollback DSU must strictly avoid path compression."
            )

        if "DSU_UNKNOWN_STRUCTURAL_PATTERN" in sig:
            return FailureClassification(
                category=FailureCategory.DSU_UNKNOWN_STRUCTURAL_PATTERN,
                description="Unknown or unregistered DSU structural pattern requested.",
                suggested_alternative="dsu_basic",
                root_cause_analysis="The requested DSU capability does not match registered DSU pattern models."
            )

        if "DSU_POTENTIAL_ACCUMULATION_ERROR" in sig:
            return FailureClassification(
                category=FailureCategory.DSU_POTENTIAL_ACCUMULATION_ERROR,
                description="Potential offset desynchronization during path compression or union.",
                suggested_alternative="accumulate_potential_to_root",
                root_cause_analysis="Failure to add parent's potential during path compression causes offset desync."
            )

        if "DSU_PARITY_XOR_ERROR" in sig:
            return FailureClassification(
                category=FailureCategory.DSU_PARITY_XOR_ERROR,
                description="Parity bit XOR desynchronization in dynamic 2-coloring.",
                suggested_alternative="accumulate_parity_xor",
                root_cause_analysis="Incorrect XOR accumulation across parent links causes color inconsistency."
            )

        if "DSU_IMPLEMENTATION_BUG" in sig:
            return FailureClassification(
                category=FailureCategory.DSU_IMPLEMENTATION_BUG,
                description="Implementation bug in DSU union, find, or metadata update.",
                suggested_alternative="verify_dsu_invariants",
                root_cause_analysis="Bug in canonical root finding, union by rank, or metadata combine function."
            )

        if "DSU_OUTPUT_ERROR" in sig:
            return FailureClassification(
                category=FailureCategory.DSU_OUTPUT_ERROR,
                description="DSU query response formatting mismatch.",
                suggested_alternative="format_dsu_output",
                root_cause_analysis="Query output does not match expected YES/NO, value, or UNKNOWN format."
            )

        # ── Fenwick Tree Classifications (Phase 3I) ──
        if "FENWICK_STATIC_QUERY_SUBOPTIMAL" in sig:
            return FailureClassification(
                category=FailureCategory.FENWICK_STATIC_QUERY_SUBOPTIMAL,
                description="Fenwick Tree selected for static array queries with no updates.",
                suggested_alternative="prefix_sum",
                root_cause_analysis="Static array with no updates is solved with O(1) query time and O(N) precomputation using standard prefix sums. Fenwick Tree introduces unnecessary O(log N) query overhead."
            )

        if "FENWICK_OFFLINE_RANGE_ADD_OVERKILL" in sig:
            return FailureClassification(
                category=FailureCategory.FENWICK_OFFLINE_RANGE_ADD_OVERKILL,
                description="Fenwick Tree selected for offline batch range additions without interleaved queries.",
                suggested_alternative="difference_array",
                root_cause_analysis="All range updates occur offline in a batch with no queries interleaved until the end. A simple difference array achieves O(1) updates and a single O(N) prefix sum sweep, whereas Fenwick Tree requires O(log N) per update and O(N log N) total time."
            )

        if "FENWICK_STRUCTURAL_INCOMPATIBILITY" in sig:
            return FailureClassification(
                category=FailureCategory.FENWICK_STRUCTURAL_INCOMPATIBILITY,
                description="Aggregation lacks group inverse for arbitrary range queries, or non-monotonic extremum update attempted, or range assignment requested.",
                suggested_alternative="segment_tree",
                root_cause_analysis="Arbitrary range query requiring subtraction/inversion when the aggregation has no suitable inverse, unless a separately supported Fenwick formulation exists. Prefix aggregation with a commutative monoid is supported, but arbitrary range queries without an inverse require Segment Tree."
            )

        if "FENWICK_DYNAMIC_COORDINATE_UNREPRESENTABLE" in sig:
            return FailureClassification(
                category=FailureCategory.FENWICK_DYNAMIC_COORDINATE_UNREPRESENTABLE,
                description="Dynamically appearing unknown coordinates cannot be compressed offline.",
                suggested_alternative="treap_or_balanced_bst",
                root_cause_analysis="Dynamically appearing unknown coordinates cannot be compressed offline without knowledge of the future coordinate universe. A flat Fenwick array requires a bounded or statically known coordinate space; dynamic coordinates require an ordered structure such as Treap, balanced BST, or dynamic Segment Tree."
            )

        if "FENWICK_KTH_NEGATIVE_FREQUENCY" in sig:
            return FailureClassification(
                category=FailureCategory.FENWICK_KTH_NEGATIVE_FREQUENCY,
                description="Negative frequencies present in k-th element search violating prefix monotonicity.",
                suggested_alternative="balanced_bst",
                root_cause_analysis="K-th element search via binary lifting relies on monotonic prefix sums of frequencies (frequency[x] >= 0). Negative frequencies destroy prefix monotonicity, causing binary lifting to fail."
            )

        if "FENWICK_RESOURCE_LIMIT" in sig:
            return FailureClassification(
                category=FailureCategory.FENWICK_RESOURCE_LIMIT,
                description="Coordinate space or grid dimensions exceed flat memory allocation limits.",
                suggested_alternative="coordinate_compressed_fenwick_or_hash_map",
                root_cause_analysis="Universe size N or 2D grid dimensions N x M exceed available memory or competitive time limits for flat Fenwick array allocation without coordinate compression or sparse representation."
            )

        if "FENWICK_DIMENSION_MISMATCH" in sig:
            return FailureClassification(
                category=FailureCategory.FENWICK_DIMENSION_MISMATCH,
                description="Mismatch between problem dimensionality and selected Fenwick Tree variant.",
                suggested_alternative="fenwick_2d_point_update_range_query",
                root_cause_analysis="1D Fenwick Tree cannot evaluate 2D grid queries directly, or 2D Fenwick Tree selected for a 1D problem."
            )

        if "FENWICK_OPERATION_MISMATCH" in sig:
            return FailureClassification(
                category=FailureCategory.FENWICK_OPERATION_MISMATCH,
                description="Specialized Fenwick variant selected for unsupported operation.",
                suggested_alternative="fenwick_point_update_prefix_query",
                root_cause_analysis="Problem does not require k-th element search or inversion counting."
            )

        if "FENWICK_COORDINATE_COMPRESSION_UNNECESSARY" in sig:
            return FailureClassification(
                category=FailureCategory.FENWICK_COORDINATE_COMPRESSION_UNNECESSARY,
                description="Coordinate compression applied to dense 1-indexed coordinates.",
                suggested_alternative="fenwick_point_update_prefix_query",
                root_cause_analysis="Problem coordinates are already dense and 1-indexed within memory limits; coordinate compression adds unnecessary O(K log K) precomputation."
            )

        if "FENWICK_COMPLEXITY_EXCEEDED" in sig:
            return FailureClassification(
                category=FailureCategory.FENWICK_COMPLEXITY_EXCEEDED,
                description="Naive linear scan used instead of logarithmic Fenwick Tree.",
                suggested_alternative="fenwick_point_update_prefix_query",
                root_cause_analysis="Naive array scan takes O(N) per query, leading to O(Q * N) time which exceeds competitive time limits. Fenwick Tree answers queries in O(log N) time."
            )

        if "FENWICK_INDEX_OUT_OF_BOUNDS" in sig:
            return FailureClassification(
                category=FailureCategory.FENWICK_INDEX_OUT_OF_BOUNDS,
                description="Fenwick Tree index out of bounds or 0-index used in 1-based lowbit loop.",
                suggested_alternative="check_1_based_indexing",
                root_cause_analysis="Index 0 causes infinite loop in i += lowbit(i) or out of bounds access in tree[1..N]."
            )

        if "FENWICK_UNKNOWN_STRUCTURAL_PATTERN" in sig:
            return FailureClassification(
                category=FailureCategory.FENWICK_UNKNOWN_STRUCTURAL_PATTERN,
                description="Unknown or unregistered Fenwick structural pattern requested.",
                suggested_alternative="fenwick_point_update_prefix_query",
                root_cause_analysis="The requested Fenwick capability does not match registered Fenwick pattern models."
            )

        if "FENWICK_IMPLEMENTATION_BUG" in sig:
            return FailureClassification(
                category=FailureCategory.FENWICK_IMPLEMENTATION_BUG,
                description="Implementation bug in Fenwick update, query, or binary lifting.",
                suggested_alternative="verify_fenwick_invariants",
                root_cause_analysis="Bug in lowbit calculation, prefix subtraction, or binary lifting bitmasking."
            )

        if "FENWICK_OUTPUT_ERROR" in sig:
            return FailureClassification(
                category=FailureCategory.FENWICK_OUTPUT_ERROR,
                description="Fenwick query response formatting mismatch.",
                suggested_alternative="format_fenwick_output",
                root_cause_analysis="Query output format does not match expected integer or range sum format."
            )

        # ── Segment Tree Failure Classification (Phase 3J) ──
        if "SEGMENT_TREE_STATIC_QUERY_SUBOPTIMAL" in sig:
            return FailureClassification(
                category=FailureCategory.SEGMENT_TREE_STATIC_QUERY_SUBOPTIMAL,
                description="Static range queries without updates are suboptimal with Segment Tree when O(1) static alternatives exist.",
                suggested_alternative="prefix_sum_or_sparse_table",
                root_cause_analysis="Static arrays with no updates may admit O(1) query structures. Prefix Sums provide O(1) range-sum queries with O(N) memory, while Sparse Tables provide O(1) queries for suitable idempotent operations such as minimum/maximum with O(N log N) preprocessing and memory. These structures may dominate Segment Tree query complexity, but their memory and preprocessing trade-offs differ. (Note: Non-invertible, non-idempotent static queries like maximum subarray sum remain valid for Segment Tree)."
            )

        if "SEGMENT_TREE_SIMPLE_PREFIX_OVERKILL" in sig:
            return FailureClassification(
                category=FailureCategory.SEGMENT_TREE_SIMPLE_PREFIX_OVERKILL,
                description="Segment tree is overkill for point update with prefix-only queries on an invertible monoid.",
                suggested_alternative="fenwick_point_update_prefix_query",
                root_cause_analysis="Fenwick Tree solves point update with prefix query with ~1/4 memory and smaller constant factor."
            )

        if "SEGMENT_TREE_DIFFERENCE_ARRAY_OVERKILL" in sig:
            return FailureClassification(
                category=FailureCategory.SEGMENT_TREE_DIFFERENCE_ARRAY_OVERKILL,
                description="Lazy segment tree is overkill for offline batch range additions without intermediate queries.",
                suggested_alternative="difference_array",
                root_cause_analysis="Difference array solves batch offline range additions in O(1) per update and O(N) sweep, avoiding O(N log N) lazy segment tree overhead."
            )

        if "SEGMENT_TREE_FENWICK_EQUIVALENT" in sig:
            return FailureClassification(
                category=FailureCategory.SEGMENT_TREE_FENWICK_EQUIVALENT,
                description="Point update and range sum on abelian group is more simply solved with Fenwick Tree.",
                suggested_alternative="fenwick_point_update_prefix_query",
                root_cause_analysis="Fenwick Tree requires O(N) memory rather than 4N and has lower constant factors for invertible abelian range sum."
            )

        if "SEGMENT_TREE_NO_ASSOCIATIVE_MERGE" in sig:
            return FailureClassification(
                category=FailureCategory.SEGMENT_TREE_NO_ASSOCIATIVE_MERGE,
                description="Range operation cannot be formulated as an associative interval merge.",
                suggested_alternative="order_statistic_tree_or_sqrt_decomposition",
                root_cause_analysis="Segment Tree requires an associative binary operation over intervals; non-associative operations cannot be decomposed into canonical sub-intervals."
            )

        if "SEGMENT_TREE_STANDARD_LAZY_INSUFFICIENT" in sig or "SEGMENT_TREE_LAZY_TAG_UNSUPPORTED" in sig:
            return FailureClassification(
                category=FailureCategory.SEGMENT_TREE_STANDARD_LAZY_INSUFFICIENT,
                description="Range operation requires extensions beyond standard lazy propagation (e.g. Segment Tree Beats).",
                suggested_alternative="segment_tree_beats",
                root_cause_analysis="Range chmin/chmax with range sum cannot be propagated with ordinary lazy propagation without break/tag condition maintenance and historical extrema tracking (Segment Tree Beats)."
            )

        if "SEGMENT_TREE_RESOURCE_LIMIT" in sig:
            return FailureClassification(
                category=FailureCategory.SEGMENT_TREE_RESOURCE_LIMIT,
                description="Segment tree memory exceeds available budget (4N * sizeof(Node) + auxiliary).",
                suggested_alternative="coordinate_compressed_segment_tree_or_dynamic_segtree",
                root_cause_analysis="Flat 4N node array allocation exceeds competitive programming memory limits. For sparse touched coordinates in a huge universe (Q << U), use Dynamic Segment Tree or Coordinate Compression; for dense large N, use Sqrt Decomposition."
            )

        if "SEGMENT_TREE_KTH_NEGATIVE_FREQUENCY" in sig:
            return FailureClassification(
                category=FailureCategory.SEGMENT_TREE_KTH_NEGATIVE_FREQUENCY,
                description="Negative frequencies violate subtree monotonicity in frequency segment tree.",
                suggested_alternative="balanced_bst",
                root_cause_analysis="K-th element search via tree walk requires non-negative subtree counts for monotonic binary descent."
            )

        if "SEGMENT_TREE_OPERATION_MISMATCH" in sig:
            return FailureClassification(
                category=FailureCategory.SEGMENT_TREE_OPERATION_MISMATCH,
                description="Selected Segment Tree variant does not match requested problem operation.",
                suggested_alternative="re-run candidate generation / select operation-compatible family or pattern",
                root_cause_analysis="Selected pattern assumes specialized algebraic state (e.g. max subarray prefix/suffix or frequency counts) not required by or compatible with the problem."
            )

        if "SEGMENT_TREE_COMPLEXITY_EXCEEDED" in sig:
            return FailureClassification(
                category=FailureCategory.SEGMENT_TREE_COMPLEXITY_EXCEEDED,
                description="Estimated O(Q * N) work exceeds problem time budget.",
                suggested_alternative="select_operation_compatible_segment_tree_variant",
                root_cause_analysis="Naive linear scan takes O(N) per query, leading to estimated O(Q * N) work exceeding the problem's time budget (using ~10^8 operations as a general rule-of-thumb heuristic depending on language, constant factors, and platform constraints)."
            )

        if "SEGMENT_TREE_IMPLEMENTATION_BUG" in sig:
            return FailureClassification(
                category=FailureCategory.SEGMENT_TREE_IMPLEMENTATION_BUG,
                description="Implementation bug in Segment Tree push_down, merge, or query.",
                suggested_alternative="verification / invariant repair pipeline",
                root_cause_analysis="Bug in lazy tag composition algebraic precedence, canonical interval intersection logic, or node merge neutral identity handling."
            )

        # ── Dynamic Programming Failure Handlers (Phase 3K) ──
        if "DP_DOMINATED_BY_GREEDY" in sig or "DP_GREEDY_CHOICE_OPTIMAL" in sig:
            return FailureClassification(
                category=FailureCategory.DP_DOMINATED_BY_GREEDY,
                description="Greedy choice property holds; DP formulation is asymptotically and structurally dominated by greedy.",
                suggested_alternative="greedy_algorithm",
                root_cause_analysis="Problem possesses the greedy choice property where local optimal decisions provably lead to global optimum. While a DP recurrence can be mathematically formulated, greedy is asymptotically and structurally preferable."
            )

        if "DP_CYCLIC_STATE_DEPENDENCY" in sig:
            return FailureClassification(
                category=FailureCategory.DP_CYCLIC_STATE_DEPENDENCY,
                description="State dependency graph contains cycles without topological ordering.",
                suggested_alternative="competing_graph_algorithm",
                root_cause_analysis="The proposed state transition graph cannot be evaluated through a valid acyclic recurrence/topological order. The candidate is rejected and CHUP dispatches to the appropriate competing graph family."
            )

        if "DP_NO_OPTIMAL_SUBSTRUCTURE" in sig or "DP_SUBPROBLEM_INCOMPATIBLE" in sig:
            return FailureClassification(
                category=FailureCategory.DP_NO_OPTIMAL_SUBSTRUCTURE,
                description="Problem lacks valid subproblem decomposition: subproblem optima or algebraic transitions do not compose.",
                suggested_alternative="backtracking_or_exponential_search",
                root_cause_analysis="For optimization, the Principle of Optimality fails (e.g. longest simple path in general graphs). For counting/feasibility, subproblems do not partition into independent semiring transitions."
            )

        if "DP_NO_REUSE_BENEFIT" in sig or "DP_NO_OVERLAPPING_SUBPROBLEMS" in sig:
            return FailureClassification(
                category=FailureCategory.DP_NO_REUSE_BENEFIT,
                description="Subproblems are disjoint; memoization/tabulation provides no reuse benefit over direct divide-and-conquer or tree traversal.",
                suggested_alternative="divide_and_conquer",
                root_cause_analysis="A valid recurrence exists, but subproblems have zero overlap or reuse (e.g. merge sort). Maintaining a DP table introduces unnecessary allocation overhead; divide-and-conquer or tree traversal is preferable."
            )

        if "DP_NON_MARKOVIAN_FUTURE_DEPENDENCE" in sig:
            return FailureClassification(
                category=FailureCategory.DP_NON_MARKOVIAN_FUTURE_DEPENDENCE,
                description="State definition violates Markov property and cannot be resolved by finite state augmentation.",
                suggested_alternative="state_augmented_search",
                root_cause_analysis="Future transitions depend on historical decision sequence. Finite state augmentation was evaluated and proved insufficient to compress unbounded trajectory history into a finite state space."
            )

        if "DP_RESOURCE_LIMIT" in sig:
            return FailureClassification(
                category=FailureCategory.DP_RESOURCE_LIMIT,
                description="DP table allocation exceeds hardware or memory limit.",
                suggested_alternative="dp_space_optimization",
                root_cause_analysis="DP state table exceeds memory limit; compress space using rolling array."
            )

        if "DP_STATE_SPACE_EXPLOSION" in sig:
            return FailureClassification(
                category=FailureCategory.DP_STATE_SPACE_EXPLOSION,
                description="DP state space exceeds memory or time complexity limits (computationally infeasible despite mathematical recurrence validity).",
                suggested_alternative="approximation_or_meet_in_middle",
                root_cause_analysis="Number of reachable states grows exponentially with input size, exceeding available RAM or runtime limits."
            )

        if "DP_UNPROVEN_OPTIMIZATION_PREREQUISITE" in sig:
            return FailureClassification(
                category=FailureCategory.DP_UNPROVEN_OPTIMIZATION_PREREQUISITE,
                description="Quadrangle inequality or slope convexity unproven for DP optimization.",
                suggested_alternative="dp_1d_linear",
                root_cause_analysis="Attempted to apply CHT, Knuth, or D&C optimization without verifying Monge property or convexity."
            )

        if "DP_OPERATION_MISMATCH" in sig:
            return FailureClassification(
                category=FailureCategory.DP_OPERATION_MISMATCH,
                description="Selected DP pattern does not match the problem's structural recurrence.",
                suggested_alternative="re-run candidate generation / select operation-compatible DP pattern",
                root_cause_analysis="DP recurrence formula or state dimensionality does not match the problem requirements."
            )

        if "DP_IMPLEMENTATION_BUG" in sig:
            return FailureClassification(
                category=FailureCategory.DP_IMPLEMENTATION_BUG,
                description="Implementation bug in DP transition, base case, or topological order.",
                suggested_alternative="verification / invariant repair pipeline",
                root_cause_analysis="Off-by-one in state transition, incorrect base case initialization, or invalid evaluation order."
            )

        # ── Greedy Failure Categories (Phase 3L) ──
        if "GREEDY_NO_SAFE_LOCAL_CHOICE" in sig:
            return FailureClassification(
                category=FailureCategory.GREEDY_NO_SAFE_LOCAL_CHOICE,
                description="Local greedy decision cannot be proven safe; local optimum does not imply global optimum.",
                suggested_alternative="dynamic_programming",
                root_cause_analysis="Problem lacks the greedy choice property; committing to a local choice irrevocably cuts off optimal solutions."
            )

        if "GREEDY_EXCHANGE_PROOF_FAILED" in sig:
            return FailureClassification(
                category=FailureCategory.GREEDY_EXCHANGE_PROOF_FAILED,
                description="Exchange argument failed: substituting the greedy choice into an optimal solution degrades the objective.",
                suggested_alternative="dynamic_programming",
                root_cause_analysis="Exchanging an arbitrary optimal decision with the candidate greedy choice results in a strictly worse objective or violates feasibility constraints (e.g. 0/1 knapsack discrete capacity or weighted interval scheduling)."
            )

        if "GREEDY_STAYING_AHEAD_FAILED" in sig:
            return FailureClassification(
                category=FailureCategory.GREEDY_STAYING_AHEAD_FAILED,
                description="Staying-ahead induction failed: greedy partial solution falls behind competitor at intermediate stage.",
                suggested_alternative="dynamic_programming_or_graph",
                root_cause_analysis="The greedy frontier or partial progress is strictly surpassed by an alternative construction on some prefix/stage."
            )

        if "GREEDY_DOMINANCE_FAILED" in sig:
            return FailureClassification(
                category=FailureCategory.GREEDY_DOMINANCE_FAILED,
                description="Dominance proof failed: discarded choice is not provably dominated across all future contexts.",
                suggested_alternative="backtracking_or_dp",
                root_cause_analysis="The discarded alternative can yield a better overall outcome when combined with specific future elements."
            )

        if "GREEDY_LOOKAHEAD_REQUIRED" in sig:
            return FailureClassification(
                category=FailureCategory.GREEDY_LOOKAHEAD_REQUIRED,
                description="Greedy strategy requires unbounded lookahead; myopic choice is insufficient.",
                suggested_alternative="dynamic_programming",
                root_cause_analysis="Evaluation of current decision requires inspecting unbounded downstream decisions, violating local choice independence."
            )

        if "GREEDY_OBJECTIVE_MISMATCH" in sig:
            return FailureClassification(
                category=FailureCategory.GREEDY_OBJECTIVE_MISMATCH,
                description="Greedy ordering heuristic targets a different objective than requested.",
                suggested_alternative="dynamic_programming_or_branch_and_bound",
                root_cause_analysis="Sorting or prioritizing by the chosen metric optimizes an intermediate surrogate rather than the global problem objective."
            )

        if "GREEDY_COUNTEREXAMPLE_FOUND" in sig:
            return FailureClassification(
                category=FailureCategory.GREEDY_COUNTEREXAMPLE_FOUND,
                description="Concrete counterexample disproves candidate greedy strategy.",
                suggested_alternative="dynamic_programming",
                root_cause_analysis="Candidate greedy strategy was explicitly disproven by generating an instance where greedy yields a suboptimal result (e.g. coin change {1, 3, 4} for target 6 gives 4+1+1=3 vs optimal 3+3=2)."
            )

        if "GREEDY_PROOF_NOT_ESTABLISHED" in sig:
            return FailureClassification(
                category=FailureCategory.GREEDY_PROOF_NOT_ESTABLISHED,
                description="No supported proof mechanism (Exchange, Staying Ahead, Dominance, Cut Property, Matroid) could establish correctness.",
                suggested_alternative="explore_competing_families",
                root_cause_analysis="CHUP could not derive a formal safety proof within the supported proof systems; candidate remains unproven."
            )

        if "GREEDY_MATROID_PREREQUISITE_UNPROVEN" in sig:
            return FailureClassification(
                category=FailureCategory.GREEDY_MATROID_PREREQUISITE_UNPROVEN,
                description="Matroid independence or exchange axiom does not hold on the candidate ground set.",
                suggested_alternative="dynamic_programming",
                root_cause_analysis="The candidate subset system violates either the hereditary property or the independent set exchange property."
            )

        if "GREEDY_RESOURCE_LIMIT" in sig:
            return FailureClassification(
                category=FailureCategory.GREEDY_RESOURCE_LIMIT,
                description="Greedy execution exceeded time/memory budget (e.g. sorting large N or heap memory).",
                suggested_alternative="bucket_or_radix_sort_or_linear_scan",
                root_cause_analysis="Resource limits exceeded during priority queue maintenance or full array sorting."
            )

        if "GREEDY_IMPLEMENTATION_BUG" in sig:
            return FailureClassification(
                category=FailureCategory.GREEDY_IMPLEMENTATION_BUG,
                description="Implementation bug in greedy choice comparison, heap maintenance, or state update.",
                suggested_alternative="verification_and_repair",
                root_cause_analysis="Comparator inverted, tie-breaking undefined, or loop bounds corrupted in greedy scan."
            )

        # ── Divide & Conquer & Backtracking Classification (Phase 3M) ──
        if "COMPOSITION_UNSUPPORTED" in sig or "TOWER" in sig or "CROSS_FAMILY" in sig:
            return FailureClassification(
                category=FailureCategory.COMPOSITION_UNSUPPORTED,
                description="Problem requires composition across distinct algorithmic families that CHUP cannot currently synthesize as a unified pattern.",
                suggested_alternative="fail_closed_unsupported",
                root_cause_analysis="Problem requires composing greedy choice with ordered state/successor queries (e.g. Tower problem requiring multiset/upper_bound with greedy placement) without an established monolithic pattern."
            )

        if "DC_SUBPROBLEMS_NOT_INDEPENDENT" in sig or "SUBPROBLEMS_NOT_INDEPENDENT" in sig:
            return FailureClassification(
                category=FailureCategory.DC_SUBPROBLEMS_NOT_INDEPENDENT,
                description="Subproblems share mutable state or depend on each other's execution outcomes; divide-and-conquer independence assumption violated.",
                suggested_alternative="dynamic_programming",
                root_cause_analysis="Divide and conquer requires mutually disjoint, independent subproblems; overlapping state requires memoization or topological evaluation."
            )

        if "DC_COMBINE_STEP_INTRACTABLE" in sig or "COMBINE_STEP_INTRACTABLE" in sig:
            return FailureClassification(
                category=FailureCategory.DC_COMBINE_STEP_INTRACTABLE,
                description="Merging subproblem solutions requires exponential or NP-hard computation; divide-and-conquer provides no polynomial advantage.",
                suggested_alternative="approximation_or_dp",
                root_cause_analysis="Combine step complexity dominates or matches full search complexity, negating the divide-and-conquer reduction."
            )

        if "DC_BASE_CASE_UNDEFINED" in sig or "BASE_CASE_UNDEFINED" in sig:
            return FailureClassification(
                category=FailureCategory.DC_BASE_CASE_UNDEFINED,
                description="Base cases are ill-defined or infinite recursion occurs without reaching a terminal reduction.",
                suggested_alternative="define_explicit_base_case",
                root_cause_analysis="Recursion step fails to strictly decrease subproblem size or base-case condition is omitted/unreachable."
            )

        if "BACKTRACKING_SEARCH_SPACE_EXPLOSIVE" in sig or "SEARCH_SPACE_EXPLOSIVE" in sig:
            return FailureClassification(
                category=FailureCategory.BACKTRACKING_SEARCH_SPACE_EXPLOSIVE,
                description="Search space size exceeds practical budget without sufficient pruning mechanism.",
                suggested_alternative="branch_and_bound_or_dp",
                root_cause_analysis="Combinatorial explosion without strong pruning rules or domain reduction makes full backtracking intractable."
            )

        if "BACKTRACKING_INSUFFICIENT_PRUNING" in sig or "INSUFFICIENT_PRUNING" in sig:
            return FailureClassification(
                category=FailureCategory.BACKTRACKING_INSUFFICIENT_PRUNING,
                description="Pruning rules fail to prune a significant fraction of the search tree; effectively exhaustive search.",
                suggested_alternative="strengthen_pruning_or_branch_and_bound",
                root_cause_analysis="Pruning bounds are too loose to eliminate subtrees before exponential growth."
            )

        if "BACKTRACKING_STATE_RESTORATION_DEFECT" in sig or "STATE_RESTORATION_DEFECT" in sig:
            return FailureClassification(
                category=FailureCategory.BACKTRACKING_STATE_RESTORATION_DEFECT,
                description="State mutations made during branch exploration are not correctly restored upon backtracking, corrupting subsequent branches.",
                suggested_alternative="explicit_undo_or_immutable_state",
                root_cause_analysis="Mutable state (arrays, masks, visited sets) modified during forward exploration was not reverted on return."
            )

        if "BACKTRACKING_SYMMETRY_NOT_BROKEN" in sig or "SYMMETRY_NOT_BROKEN" in sig:
            return FailureClassification(
                category=FailureCategory.BACKTRACKING_SYMMETRY_NOT_BROKEN,
                description="Search tree contains isomorphic or symmetric branches that are explored redundantly; symmetry-breaking constraints missing.",
                suggested_alternative="impose_canonical_ordering_or_symmetry_breaking",
                root_cause_analysis="Permutation/combination symmetry generates equivalent states that could be avoided by enforcing ordering (e.g. i >= start)."
            )

        if "BACKTRACKING_LOOKAHEAD_MISMATCH" in sig or "LOOKAHEAD_MISMATCH" in sig:
            return FailureClassification(
                category=FailureCategory.BACKTRACKING_LOOKAHEAD_MISMATCH,
                description="Lookahead / constraint propagation mechanism produces false pruning or misses domain wipeouts.",
                suggested_alternative="forward_checking_or_ac3",
                root_cause_analysis="Forward constraint propagation incorrectly eliminated valid assignments or failed to detect empty variable domains."
            )

        if "BACKTRACKING_GREEDY_SUFFICIENT" in sig or "GREEDY_SUFFICIENT" in sig:
            return FailureClassification(
                category=FailureCategory.BACKTRACKING_GREEDY_SUFFICIENT,
                description="Problem exhibits the greedy choice property; exponential backtracking search is unnecessarily expensive when a greedy strategy is provably optimal.",
                suggested_alternative="greedy",
                root_cause_analysis="Local greedy choice provably leads to a globally optimal solution; backtracking search is redundant."
            )

        if "BACKTRACKING_DP_SUFFICIENT" in sig or "DP_SUFFICIENT" in sig:
            return FailureClassification(
                category=FailureCategory.BACKTRACKING_DP_SUFFICIENT,
                description="Problem exhibits overlapping subproblems and optimal substructure that admit a polynomial DP solution; exhaustive backtracking is suboptimal.",
                suggested_alternative="dynamic_programming",
                root_cause_analysis="Subproblem results can be cached or tabulated, transforming exponential search into polynomial time."
            )

        if "BACKTRACKING_RESOURCE_LIMIT" in sig:
            return FailureClassification(
                category=FailureCategory.BACKTRACKING_RESOURCE_LIMIT,
                description="Recursion depth exceeds stack limit or search node count exceeds time budget.",
                suggested_alternative="iterative_search_or_meet_in_middle",
                root_cause_analysis="Call stack overflow or execution exceeded maximum allowable node expansions."
            )

        return FailureClassification(
            category=FailureCategory.IMPLEMENTATION_ERROR,
            description="Algorithmic execution did not match expected specification.",
            suggested_alternative=None,
            root_cause_analysis="Syntax or edge-case boundary handling error."
        )
