"""
Taxonomy of Pointer-Based Algorithms.

Hierarchy:
Pointer-Based Algorithms
├── Two Pointers
│   ├── Converging (Opposite Direction)
│   ├── Same Direction (Fast/Slow, Read/Write, Compaction)
│   └── Sliding Window (Fixed, Variable Min, Variable Max)
├── Partition Pointers (2-way, 3-way Dutch National Flag)
├── Fast/Slow Pointers (Linked Structures, Cycle, Middle)
└── Monotonic Stack (Phase 3B)
    ├── Directional Boundary (next/previous greater/smaller)
    ├── Distance and Span (stock span)
    ├── Structural Applications (histogram, circular)
    └── Contribution Counting (subarray min/max sums)
"""

from enum import Enum
from typing import Dict, List, Any

class SearchSpaceKind(str, Enum):
    INDEX = "index"
    INTEGER_VALUE = "integer_value"
    REAL_VALUE = "real_value"
    FEASIBILITY_DOMAIN = "feasibility_domain"

class ExactMatchSemantics(str, Enum):
    ANY_MATCH = "any_match"
    FIRST_MATCH = "first_match"
    LAST_MATCH = "last_match"

class TrieKind(str, Enum):
    CHARACTER_TRIE = "character_trie"
    BINARY_TRIE = "binary_trie"

class TrieAlphabetKind(str, Enum):
    LOWERCASE_26 = "lowercase_26"
    DIGITS_10 = "digits_10"
    ASCII_128 = "ascii_128"
    BINARY_2 = "binary_2"
    ARBITRARY_MAP = "arbitrary_map"

class TrieStorageKind(str, Enum):
    FIXED_ARRAY = "fixed_array"
    HASH_MAP = "hash_map"
    ORDERED_MAP = "ordered_map"

class TreeKind(str, Enum):
    ROOTED_TREE = "rooted_tree"
    BINARY_TREE = "binary_tree"
    BST = "bst"

class TreeRepresentation(str, Enum):
    EDGE_LIST = "edge_list"
    PARENT_ARRAY = "parent_array"
    ADJACENCY_LIST = "adjacency_list"
    BINARY_POINTERS = "binary_pointers"

class TreeTraversalOrder(str, Enum):
    PREORDER = "preorder"
    INORDER = "inorder"
    POSTORDER = "postorder"
    LEVEL_ORDER = "level_order"

# ── Graph enums (Phase 3F) ──

class GraphKind(str, Enum):
    UNDIRECTED = "undirected"
    DIRECTED = "directed"

class GraphWeightKind(str, Enum):
    UNWEIGHTED = "unweighted"
    NON_NEGATIVE_WEIGHTED = "non_negative_weighted"
    NEGATIVE_WEIGHTED = "negative_weighted"

class GraphRepresentation(str, Enum):
    ADJACENCY_LIST = "adjacency_list"
    ADJACENCY_MATRIX = "adjacency_matrix"
    EDGE_LIST = "edge_list"

class GraphComponentKind(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    BICONNECTED = "biconnected"
    STRONGLY_CONNECTED = "strongly_connected"
    WEAKLY_CONNECTED = "weakly_connected"

class GraphAcyclicityKind(str, Enum):
    DAG = "dag"
    DIRECTED_CYCLIC = "directed_cyclic"
    UNDIRECTED_TREE = "undirected_tree"
    UNDIRECTED_CYCLIC = "undirected_cyclic"

class GraphBipartiteKind(str, Enum):
    BIPARTITE = "bipartite"
    NON_BIPARTITE = "non_bipartite"

# ── Heap enums (Phase 3G) ──

class HeapKind(str, Enum):
    MIN_HEAP = "min_heap"
    MAX_HEAP = "max_heap"

class HeapOperationKind(str, Enum):
    PEEK = "peek"
    INSERT = "insert"
    EXTRACT = "extract"
    UPDATE = "update"
    REMOVE = "remove"
    BUILD = "build"
    MERGE = "merge"

class DSUKind(str, Enum):
    BASIC = "basic"
    WEIGHTED = "weighted"
    PARITY = "parity"
    ROLLBACK = "rollback"

class DSUOperationKind(str, Enum):
    FIND = "find"
    UNION = "union"
    CONNECTED = "connected"
    COMPONENT_SIZE = "component_size"
    COMPONENT_METADATA = "component_metadata"
    DIFF = "diff"
    CONSISTENCY_CHECK = "consistency_check"
    SNAPSHOT = "snapshot"
    ROLLBACK = "rollback"

# ── Fenwick Tree (Phase 3I) ──
class FenwickKind(str, Enum):
    POINT_UPDATE_PREFIX_QUERY = "point_update_prefix_query"
    RANGE_UPDATE_POINT_QUERY = "range_update_point_query"
    RANGE_UPDATE_RANGE_QUERY = "range_update_range_query"
    FREQUENCY = "frequency"
    KTH_ELEMENT = "kth_element"
    COORDINATE_COMPRESSION = "coordinate_compression"
    INVERSION_COUNTING = "inversion_counting"
    MULTISET = "multiset"
    PREFIX_EXTREMUM = "prefix_extremum"
    TWO_DIMENSIONAL = "two_dimensional"

class FenwickOperationKind(str, Enum):
    POINT_ADD = "point_add"
    PREFIX_QUERY = "prefix_query"
    RANGE_QUERY = "range_query"
    RANGE_ADD = "range_add"
    POINT_QUERY = "point_query"
    KTH_ELEMENT = "kth_element"
    COUNT_LESS_EQUAL = "count_less_equal"
    COUNT_GREATER = "count_greater"
    COMPRESS = "compress"
    RECTANGLE_ADD = "rectangle_add"
    RECTANGLE_QUERY = "rectangle_query"

# ── Segment Tree (Phase 3J) ──
class SegmentTreeKind(str, Enum):
    POINT_UPDATE_RANGE_QUERY = "point_update_range_query"
    RANGE_ADD_RANGE_QUERY = "range_add_range_query"
    RANGE_ASSIGN_RANGE_QUERY = "range_assign_range_query"
    COMBINED_LAZY_RANGE_QUERY = "combined_lazy_range_query"
    METADATA_AGGREGATE = "metadata_aggregate"
    MAX_SUBARRAY = "max_subarray"
    FREQUENCY_ORDER_STATISTIC = "frequency_order_statistic"
    INTERVAL_STATISTICS = "interval_statistics"

class SegmentTreeOperationKind(str, Enum):
    BUILD = "build"
    MERGE = "merge"
    POINT_UPDATE = "point_update"
    RANGE_QUERY = "range_query"
    RANGE_ADD = "range_add"
    RANGE_ASSIGN = "range_assign"
    LAZY_APPLY = "lazy_apply"
    LAZY_PUSH = "lazy_push"

# ── Dynamic Programming (Phase 3K) ──
class DPKind(str, Enum):
    LINEAR_1D = "linear_1d"
    GRID_2D = "grid_2d"
    KNAPSACK = "knapsack"
    SUBSEQUENCE_STRING = "subsequence_string"
    INTERVAL = "interval"
    PARTITION = "partition"
    STATE_MACHINE = "state_machine"
    BITMASK = "bitmask"
    TREE = "tree_dp"
    DAG = "dag_dp"
    DIGIT = "digit"
    OPTIMIZATION = "optimization"
    RECONSTRUCTION = "reconstruction"
    SPACE_OPTIMIZATION = "space_optimization"

class DPOperationKind(str, Enum):
    MEMOIZE = "memoize"
    TABULATE = "tabulate"
    TRANSITION = "transition"
    RECONSTRUCT = "reconstruct"
    COMPRESS_SPACE = "compress_space"
    OPTIMIZE_TRANSITION = "optimize_transition"

# ── Greedy Algorithms (Phase 3L) ──
class GreedyKind(str, Enum):
    INTERVAL_SELECTION = "greedy_interval_selection"
    INTERVAL_COVERING = "greedy_interval_covering"
    FRACTIONAL_KNAPSACK = "greedy_fractional_knapsack"
    DEADLINE_SCHEDULING = "greedy_deadline_scheduling"
    HEAP_ASSISTED = "greedy_heap_assisted"
    HUFFMAN_MERGE = "greedy_huffman_merge"
    SEQUENCE_LOCAL_CHOICE = "greedy_sequence_local_choice"
    REACHABILITY_PARTITION = "greedy_reachability_partition"
    GRAPH_MST = "greedy_graph_mst"
    GENERAL_EXCHANGE = "greedy_general_exchange"

class GreedyProofKind(str, Enum):
    EXCHANGE = "greedy_exchange_proof"
    STAYING_AHEAD = "greedy_staying_ahead_proof"
    DOMINANCE = "greedy_dominance_proof"
    SAFE_CUT = "greedy_safe_cut_proof"
    MATROID = "greedy_matroid_proof"

# ── Divide and Conquer & Backtracking (Phase 3M) ──
class DCBacktrackingKind(str, Enum):
    # Divide and Conquer
    MERGE_SORT_INVERSIONS = "dc_merge_sort_inversions"
    QUICKSELECT = "dc_quickselect"
    CLOSEST_PAIR = "dc_closest_pair"
    TREE_CENTROID = "dc_tree_centroid"
    CDQ_DIVIDE_AND_CONQUER = "dc_cdq_divide_and_conquer"
    # Backtracking & Exponential Search
    SUBSETS_PERMUTATIONS = "backtracking_subsets_permutations"
    CONSTRAINT_SATISFACTION = "backtracking_constraint_satisfaction"
    BRANCH_AND_BOUND = "backtracking_branch_and_bound"
    STATE_SPACE_SEARCH = "backtracking_state_space_search"
    MEET_IN_THE_MIDDLE = "backtracking_meet_in_the_middle"

class SubproblemDependencyKind(str, Enum):
    DISJOINT = "disjoint"
    OVERLAPPING_REUSABLE = "overlapping_reusable"
    CROSS_DEPENDENT = "cross_dependent"

class TerminationGuaranteeKind(str, Enum):
    OPTIMALITY = "optimality"
    FEASIBILITY = "feasibility"
    ENUMERATION_COMPLETENESS = "enumeration_completeness"
    COUNTING_CORRECTNESS = "counting_correctness"
    DECISION_CORRECTNESS = "decision_correctness"

class AlgorithmFamily(str, Enum):
    TWO_POINTERS_CONVERGING = "two_pointers_converging"
    TWO_POINTERS_SAME_DIRECTION = "two_pointers_same_direction"
    SLIDING_WINDOW = "sliding_window"
    COUNTING_POINTERS = "counting_pointers"
    PARTITION_POINTERS = "partition_pointers"
    FAST_SLOW_POINTERS = "fast_slow_pointers"
    MONOTONIC_STACK = "monotonic_stack"
    BINARY_SEARCH = "binary_search"
    TRIE = "trie"
    TREE = "tree"
    GRAPH = "graph"          # Phase 3F
    HEAP = "heap"            # Phase 3G
    DSU = "dsu"              # Phase 3H
    FENWICK = "fenwick"      # Phase 3I
    SEGMENT_TREE = "segment_tree"  # Phase 3J
    DYNAMIC_PROGRAMMING = "dynamic_programming"  # Phase 3K
    GREEDY = "greedy"        # Phase 3L
    DIVIDE_AND_CONQUER_BACKTRACKING = "divide_and_conquer_backtracking"  # Phase 3M
    ADV_GRAPH = "adv_graph"  # Phase 3N

class PatternKind(str, Enum):
    # Converging (Opposite Direction)
    PAIR_SUM_SORTED = "pair_sum_sorted"
    CLOSEST_PAIR_SUM = "closest_pair_sum"
    THREE_SUM_CONVERGING = "three_sum_converging"
    FOUR_SUM_CONVERGING = "four_sum_converging"
    CONTAINER_MOST_WATER = "container_most_water"
    TRAPPING_RAIN_WATER = "trapping_rain_water"
    PALINDROME_VERIFICATION = "palindrome_verification"
    PAIR_DIFFERENCE = "pair_difference"

    # Same Direction
    IN_PLACE_COMPACTION = "in_place_compaction"
    REMOVE_DUPLICATES_SORTED = "remove_duplicates_sorted"
    MOVE_ZEROES_ORDERED = "move_zeroes_ordered"
    CHASE_POINTER_DIFFERENCE = "chase_pointer_difference"
    MERGE_SORTED_ARRAYS = "merge_sorted_arrays"

    # Sliding Window
    SLIDING_WINDOW_FIXED = "sliding_window_fixed"
    SLIDING_WINDOW_VARIABLE_MIN = "sliding_window_variable_min"
    SLIDING_WINDOW_VARIABLE_MAX = "sliding_window_variable_max"
    MINIMUM_WINDOW_SUBSTRING = "minimum_window_substring"

    # Counting with Pointers
    COUNT_PAIRS_LESS_THAN_K = "count_pairs_less_than_k"
    COUNT_PAIRS_EQUAL_K = "count_pairs_equal_k"
    COUNT_SUBARRAYS_BOUNDED = "count_subarrays_bounded"
    EXACT_COUNT_DERIVED = "exact_count_derived"

    # Partition
    PARTITION_TWO_WAY = "partition_two_way"
    PARTITION_DUTCH_FLAG = "partition_dutch_flag"

    # Fast/Slow Linked
    LINKED_CYCLE_DETECTION = "linked_cycle_detection"
    LINKED_CYCLE_START = "linked_cycle_start"
    LINKED_MIDDLE_NODE = "linked_middle_node"

    # ── Monotonic Stack (Phase 3B) ──
    NEXT_GREATER_ELEMENT = "next_greater_element"
    NEXT_SMALLER_ELEMENT = "next_smaller_element"
    PREVIOUS_GREATER_ELEMENT = "previous_greater_element"
    PREVIOUS_SMALLER_ELEMENT = "previous_smaller_element"
    NEAREST_GREATER_ELEMENT = "nearest_greater_element"
    NEAREST_SMALLER_ELEMENT = "nearest_smaller_element"
    STOCK_SPAN = "stock_span"
    LARGEST_RECTANGLE_HISTOGRAM = "largest_rectangle_histogram"
    CIRCULAR_NEXT_GREATER = "circular_next_greater"
    SUM_SUBARRAY_MINIMUMS = "sum_subarray_minimums"
    SUM_SUBARRAY_MAXIMUMS = "sum_subarray_maximums"

    # ── Binary Search (Phase 3C) ──
    BINARY_SEARCH_EXACT = "binary_search_exact"
    LOWER_BOUND = "lower_bound"
    UPPER_BOUND = "upper_bound"
    FIRST_TRUE = "first_true"
    LAST_TRUE = "last_true"
    FIRST_FALSE = "first_false"
    LAST_FALSE = "last_false"
    PREDECESSOR = "predecessor"
    SUCCESSOR = "successor"
    BINARY_SEARCH_ANSWER_MIN = "binary_search_answer_min"
    BINARY_SEARCH_ANSWER_MAX = "binary_search_answer_max"
    BINARY_SEARCH_VALUE_DOMAIN = "binary_search_value_domain"

    # ── Trie (Phase 3D) ──
    TRIE_INSERT = "trie_insert"
    TRIE_EXACT_SEARCH = "trie_exact_search"
    TRIE_PREFIX_SEARCH = "trie_prefix_search"
    TRIE_PREFIX_COUNT = "trie_prefix_count"
    TRIE_WORD_COUNT = "trie_word_count"
    TRIE_DELETION = "trie_deletion"
    TRIE_LONGEST_PREFIX = "trie_longest_prefix"
    TRIE_MAX_XOR_PAIR = "trie_max_xor_pair"
    TRIE_MAX_XOR_QUERY = "trie_max_xor_query"
    TRIE_LEXICOGRAPHIC_SORT = "trie_lexicographic_sort"
    TRIE_AUTOCOMPLETE = "trie_autocomplete"

    # ── Tree (Phase 3E) ──
    TREE_DFS_PREORDER = "tree_dfs_preorder"
    TREE_DFS_INORDER = "tree_dfs_inorder"
    TREE_DFS_POSTORDER = "tree_dfs_postorder"
    TREE_BFS_LEVEL_ORDER = "tree_bfs_level_order"
    TREE_DEPTH_HEIGHT = "tree_depth_height"
    TREE_SUBTREE_SIZE = "tree_subtree_size"
    TREE_LEAF_COUNT = "tree_leaf_count"
    TREE_SUBTREE_AGGREGATION = "tree_subtree_aggregation"
    TREE_PATH_SUM = "tree_path_sum"
    TREE_DIAMETER = "tree_diameter"
    TREE_BST_SEARCH = "tree_bst_search"
    TREE_BST_INSERT = "tree_bst_insert"
    TREE_BST_DELETE = "tree_bst_delete"
    TREE_BST_MIN_MAX = "tree_bst_min_max"
    TREE_BST_PRED_SUCC = "tree_bst_pred_succ"
    TREE_BST_VALIDATE = "tree_bst_validate"
    TREE_LCA_BINARY_TREE = "tree_lca_binary_tree"
    TREE_LCA_BST = "tree_lca_bst"
    TREE_LCA_PARENT_ARRAY = "tree_lca_parent_array"
    TREE_DP_INDEPENDENT_SET = "tree_dp_independent_set"
    TREE_DP_SUBTREE_WEIGHT = "tree_dp_subtree_weight"
    TREE_DP_TWO_STATE = "tree_dp_two_state"

    # ── Graph (Phase 3F) ──
    GRAPH_BFS_SHORTEST_PATH = "graph_bfs_shortest_path"
    GRAPH_DFS_TRAVERSAL = "graph_dfs_traversal"
    GRAPH_CONNECTED_COMPONENTS = "graph_connected_components"
    GRAPH_CYCLE_DETECTION_UNDIRECTED = "graph_cycle_detection_undirected"
    GRAPH_CYCLE_DETECTION_DIRECTED = "graph_cycle_detection_directed"
    GRAPH_BIPARTITE_COLORING = "graph_bipartite_coloring"
    GRAPH_DIJKSTRA = "graph_dijkstra"
    GRAPH_BELLMAN_FORD = "graph_bellman_ford"
    GRAPH_FLOYD_WARSHALL = "graph_floyd_warshall"
    GRAPH_TOPOLOGICAL_SORT = "graph_topological_sort"
    GRAPH_DAG_DP = "graph_dag_dp"
    GRAPH_DSU = "graph_dsu"
    GRAPH_MST_KRUSKAL = "graph_mst_kruskal"
    GRAPH_MST_PRIM = "graph_mst_prim"
    GRAPH_SCC_TARJAN = "graph_scc_tarjan"
    GRAPH_BRIDGES_ARTICULATION = "graph_bridges_articulation"

    # ── Heap / Priority Queue (Phase 3G) ──
    HEAP_MIN_PRIORITY_QUEUE = "heap_min_priority_queue"
    HEAP_MAX_PRIORITY_QUEUE = "heap_max_priority_queue"
    HEAP_BUILD = "heap_build"
    HEAP_TOP_K = "heap_top_k"
    HEAP_KTH_ELEMENT = "heap_kth_element"
    HEAP_K_WAY_MERGE = "heap_k_way_merge"
    HEAP_TWO_HEAPS = "heap_two_heaps"
    HEAP_DYNAMIC_MEDIAN = "heap_dynamic_median"
    HEAP_SCHEDULING = "heap_scheduling"
    HEAP_GREEDY_SELECTION = "heap_greedy_selection"
    HEAP_LAZY_DELETION = "heap_lazy_deletion"

    # ── Disjoint Set Union / Union-Find (Phase 3H) ──
    DSU_BASIC = "dsu_basic"
    DSU_COMPONENT_METADATA = "dsu_component_metadata"
    DSU_DYNAMIC_CONNECTIVITY = "dsu_dynamic_connectivity"
    DSU_WEIGHTED = "dsu_weighted"
    DSU_POTENTIAL_DIFFERENCE = "dsu_potential_difference"
    DSU_PARITY = "dsu_parity"
    DSU_ROLLBACK = "dsu_rollback"
    DSU_OFFLINE_DYNAMIC_CONNECTIVITY = "dsu_offline_dynamic_connectivity"
    DSU_KRUSKAL_SUPPORT = "dsu_kruskal_support"
    DSU_CONSTRAINT_CONSISTENCY = "dsu_constraint_consistency"

    # ── Fenwick Tree / Binary Indexed Tree (Phase 3I) ──
    # Tier A: Core Variants
    FENWICK_POINT_UPDATE_PREFIX_QUERY = "fenwick_point_update_prefix_query"
    FENWICK_RANGE_UPDATE_POINT_QUERY = "fenwick_range_update_point_query"
    FENWICK_RANGE_UPDATE_RANGE_QUERY = "fenwick_range_update_range_query"
    FENWICK_FREQUENCY = "fenwick_frequency"
    FENWICK_PREFIX_EXTREMUM = "fenwick_prefix_extremum"
    FENWICK_2D_POINT_UPDATE_RANGE_QUERY = "fenwick_2d_point_update_range_query"
    # Tier B: Applications
    FENWICK_KTH_ELEMENT = "fenwick_kth_element"
    FENWICK_INVERSION_COUNTING = "fenwick_inversion_counting"
    FENWICK_MULTISET = "fenwick_multiset"
    # Tier C: Transformations
    FENWICK_COORDINATE_COMPRESSION = "fenwick_coordinate_compression"

    # ── Segment Tree (Phase 3J) ──
    # Tier A: Core Variants
    SEGMENT_TREE_POINT_UPDATE_RANGE_QUERY = "segment_tree_point_update_range_query"
    SEGMENT_TREE_RANGE_ADD_RANGE_QUERY = "segment_tree_range_add_range_query"
    SEGMENT_TREE_RANGE_ASSIGN_RANGE_QUERY = "segment_tree_range_assign_range_query"
    SEGMENT_TREE_COMBINED_LAZY_RANGE_QUERY = "segment_tree_combined_lazy_range_query"
    SEGMENT_TREE_METADATA_AGGREGATE = "segment_tree_metadata_aggregate"
    # Tier B: Applications
    SEGMENT_TREE_MAX_SUBARRAY = "segment_tree_max_subarray"
    SEGMENT_TREE_FREQUENCY_ORDER_STATISTIC = "segment_tree_frequency_order_statistic"
    SEGMENT_TREE_INTERVAL_STATISTICS = "segment_tree_interval_statistics"

    # ── Dynamic Programming (Phase 3K) ──
    DP_1D_LINEAR = "dp_1d_linear"
    DP_GRID_2D = "dp_grid_2d"
    DP_KNAPSACK = "dp_knapsack"
    DP_SUBSEQUENCE_STRING = "dp_subsequence_string"
    DP_INTERVAL = "dp_interval"
    DP_PARTITION = "dp_partition"
    DP_STATE_MACHINE = "dp_state_machine"
    DP_BITMASK = "dp_bitmask"
    DP_TREE = "dp_tree"
    DP_DAG = "dp_dag"
    DP_DIGIT = "dp_digit"
    DP_OPTIMIZATION = "dp_optimization"
    DP_SOLUTION_RECONSTRUCTION = "dp_solution_reconstruction"
    DP_SPACE_OPTIMIZATION = "dp_space_optimization"

    # ── Greedy Algorithms (Phase 3L) ──
    # Core Families (3L-A through 3L-J)
    GREEDY_INTERVAL_SELECTION = "greedy_interval_selection"
    GREEDY_INTERVAL_COVERING = "greedy_interval_covering"
    GREEDY_FRACTIONAL_KNAPSACK = "greedy_fractional_knapsack"
    GREEDY_DEADLINE_SCHEDULING = "greedy_deadline_scheduling"
    GREEDY_HEAP_ASSISTED = "greedy_heap_assisted"
    GREEDY_HUFFMAN_MERGE = "greedy_huffman_merge"
    GREEDY_SEQUENCE_LOCAL_CHOICE = "greedy_sequence_local_choice"
    GREEDY_REACHABILITY_PARTITION = "greedy_reachability_partition"
    GREEDY_GRAPH_MST = "greedy_graph_mst"
    GREEDY_GENERAL_EXCHANGE = "greedy_general_exchange"
    # Proof Capabilities (3L-K through 3L-O)
    GREEDY_EXCHANGE_PROOF = "greedy_exchange_proof"
    GREEDY_STAYING_AHEAD_PROOF = "greedy_staying_ahead_proof"
    GREEDY_DOMINANCE_PROOF = "greedy_dominance_proof"
    GREEDY_SAFE_CUT_PROOF = "greedy_safe_cut_proof"
    GREEDY_MATROID_PROOF = "greedy_matroid_proof"

    # ── Divide and Conquer & Backtracking (Phase 3M) ──
    DC_MERGE_SORT_INVERSIONS = "dc_merge_sort_inversions"
    DC_QUICKSELECT = "dc_quickselect"
    DC_CLOSEST_PAIR = "dc_closest_pair"
    DC_TREE_CENTROID = "dc_tree_centroid"
    DC_CDQ_DIVIDE_AND_CONQUER = "dc_cdq_divide_and_conquer"
    BACKTRACKING_SUBSETS_PERMUTATIONS = "backtracking_subsets_permutations"
    BACKTRACKING_CONSTRAINT_SATISFACTION = "backtracking_constraint_satisfaction"
    BACKTRACKING_BRANCH_AND_BOUND = "backtracking_branch_and_bound"
    BACKTRACKING_STATE_SPACE_SEARCH = "backtracking_state_space_search"
    BACKTRACKING_MEET_IN_THE_MIDDLE = "backtracking_meet_in_the_middle"

    # ── Advanced Graph Algorithms (Phase 3N) ──
    ADV_GRAPH_01_BFS = "adv_graph_01_bfs"
    ADV_GRAPH_SPFA_NEGATIVE_CYCLE = "adv_graph_spfa_negative_cycle"
    ADV_GRAPH_EULERIAN_PATH = "adv_graph_eulerian_path"
    ADV_GRAPH_2SAT = "adv_graph_2sat"
    ADV_GRAPH_BLOCK_CUT_TREE = "adv_graph_block_cut_tree"
    ADV_GRAPH_BRIDGE_BLOCK_TREE = "adv_graph_bridge_block_tree"
    ADV_GRAPH_BIPARTITE_MATCHING = "adv_graph_bipartite_matching"
    ADV_GRAPH_MAX_FLOW_DINIC = "adv_graph_max_flow_dinic"
    ADV_GRAPH_MIN_CUT = "adv_graph_min_cut"
    ADV_GRAPH_MCMF = "adv_graph_mcmf"

    # Phase 3O: String Algorithms & Automata
    STRING_KMP_SEARCH = "string_kmp_search"
    STRING_Z_ALGORITHM = "string_z_algorithm"
    STRING_RABIN_KARP = "string_rabin_karp"
    STRING_MANACHER = "string_manacher"
    STRING_AHO_CORASICK = "string_aho_corasick"
    STRING_SUFFIX_ARRAY = "string_suffix_array"
    STRING_SUFFIX_AUTOMATON = "string_suffix_automaton"
    STRING_LYNDON_DUVAL = "string_lyndon_duval"
    STRING_SUBSEQUENCE_AUTOMATON = "string_subsequence_automaton"
    STRING_LONGEST_COMMON_SUBSTRING_SAM = "string_longest_common_substring_sam"

    # Phase 3P: Number Theory & Combinatorics
    NT_EXTENDED_GCD = "nt_extended_gcd"
    NT_MODULAR_INVERSE = "nt_modular_inverse"
    NT_CHINESE_REMAINDER = "nt_chinese_remainder"
    NT_LINEAR_SIEVE = "nt_linear_sieve"
    NT_EULER_TOTIENT = "nt_euler_totient"
    NT_MOBIUS_INVERSION = "nt_mobius_inversion"
    NT_MATRIX_POWER = "nt_matrix_power"
    NT_COMBINATORICS_FACTORIALS = "nt_combinatorics_factorials"
    NT_LUCAS_THEOREM = "nt_lucas_theorem"
    NT_MILLER_RABIN = "nt_miller_rabin"

    # Phase 3Q: Algebra & Transforms
    ALGEBRA_FFT = "algebra_fft"
    ALGEBRA_NTT = "algebra_ntt"
    ALGEBRA_FWHT = "algebra_fwht"
    ALGEBRA_POLY_INVERSE = "algebra_poly_inverse"
    ALGEBRA_GAUSS_REAL = "algebra_gauss_real"
    ALGEBRA_GAUSS_MODULAR = "algebra_gauss_modular"
    ALGEBRA_GAUSS_XOR = "algebra_gauss_xor"
    ALGEBRA_LINEAR_BASIS = "algebra_linear_basis"
    ALGEBRA_BERLEKAMP_MASSEY = "algebra_berlekamp_massey"
    ALGEBRA_LAGRANGE_INTERPOLATION = "algebra_lagrange_interpolation"

    # Phase 3R: Computational Geometry
    GEOM_ORIENTATION_CROSS_PRODUCT = "geom_orientation_cross_product"
    GEOM_SEGMENT_INTERSECTION = "geom_segment_intersection"
    GEOM_CONVEX_HULL_ANDREW = "geom_convex_hull_andrew"
    GEOM_POLYGON_AREA_SHOELACE = "geom_polygon_area_shoelace"
    GEOM_POINT_IN_POLYGON = "geom_point_in_polygon"
    GEOM_CLOSEST_PAIR_POINTS = "geom_closest_pair_points"
    GEOM_LINE_INTERSECTION_POINT = "geom_line_intersection_point"
    GEOM_ROTATING_CALIPERS_DIAMETER = "geom_rotating_calipers_diameter"
    GEOM_HALFPLANE_INTERSECTION = "geom_halfplane_intersection"
    GEOM_SWEEP_LINE_SEGMENTS = "geom_sweep_line_segments"

    # Phase 3S: Advanced Data Structures
    ADS_SPARSE_TABLE = "ads_sparse_table"
    ADS_LCA_BINARY_LIFTING = "ads_lca_binary_lifting"
    ADS_HEAVY_LIGHT_DECOMPOSITION = "ads_heavy_light_decomposition"
    ADS_CENTROID_DECOMPOSITION = "ads_centroid_decomposition"
    ADS_PERSISTENT_SEGMENT_TREE = "ads_persistent_segment_tree"
    ADS_DYNAMIC_SEGMENT_TREE = "ads_dynamic_segment_tree"
    ADS_MERGE_SORT_TREE = "ads_merge_sort_tree"
    ADS_SQRT_DECOMPOSITION = "ads_sqrt_decomposition"
    ADS_MOS_ALGORITHM = "ads_mos_algorithm"
    ADS_SEGMENT_TREE_BEATS = "ads_segment_tree_beats"

    # Phase 4: Cross-Family Composition & Multi-Component Synthesis
    CF_KRUSKAL_MST = "cf_kruskal_mst"
    CF_DIJKSTRA_SHORTEST_PATH = "cf_dijkstra_shortest_path"
    CF_BOTTLENECK_PATH_BINARY_SEARCH = "cf_bottleneck_path_binary_search"
    CF_GRAPH_SEGMENT_TREE_RELAXATION = "cf_graph_segment_tree_relaxation"
    CF_TREE_SUBTREE_DP = "cf_tree_subtree_dp"
    CF_TREE_PATH_HLD_SEGMENT_TREE = "cf_tree_path_hld_segment_tree"
    CF_EVENT_SCHEDULING_GREEDY_HEAP = "cf_event_scheduling_greedy_heap"
    CF_INCREMENTAL_CONNECTIVITY_GREEDY_DSU = "cf_incremental_connectivity_greedy_dsu"
    CF_DP_RANGE_ACCELERATION_SEGMENT_TREE = "cf_dp_range_acceleration_segment_tree"
    CF_CONVEX_DP_MONOTONIC_QUEUE = "cf_convex_dp_monotonic_queue"
    CF_BISECTION_GREEDY_FEASIBILITY = "cf_bisection_greedy_feasibility"
    CF_FRACTIONAL_BISECTION_DP = "cf_fractional_bisection_dp"

# All Monotonic Stack pattern names as a set (for fast lookup)
MONOTONIC_STACK_PATTERNS = {
    PatternKind.NEXT_GREATER_ELEMENT.value,
    PatternKind.NEXT_SMALLER_ELEMENT.value,
    PatternKind.PREVIOUS_GREATER_ELEMENT.value,
    PatternKind.PREVIOUS_SMALLER_ELEMENT.value,
    PatternKind.NEAREST_GREATER_ELEMENT.value,
    PatternKind.NEAREST_SMALLER_ELEMENT.value,
    PatternKind.STOCK_SPAN.value,
    PatternKind.LARGEST_RECTANGLE_HISTOGRAM.value,
    PatternKind.CIRCULAR_NEXT_GREATER.value,
    PatternKind.SUM_SUBARRAY_MINIMUMS.value,
    PatternKind.SUM_SUBARRAY_MAXIMUMS.value,
}

# All Binary Search pattern names as a set (for fast lookup)
BINARY_SEARCH_PATTERNS = {
    PatternKind.BINARY_SEARCH_EXACT.value,
    PatternKind.LOWER_BOUND.value,
    PatternKind.UPPER_BOUND.value,
    PatternKind.FIRST_TRUE.value,
    PatternKind.LAST_TRUE.value,
    PatternKind.FIRST_FALSE.value,
    PatternKind.LAST_FALSE.value,
    PatternKind.PREDECESSOR.value,
    PatternKind.SUCCESSOR.value,
    PatternKind.BINARY_SEARCH_ANSWER_MIN.value,
    PatternKind.BINARY_SEARCH_ANSWER_MAX.value,
    PatternKind.BINARY_SEARCH_VALUE_DOMAIN.value,
}

# All Trie pattern names as a set (for fast lookup)
TRIE_PATTERNS = {
    PatternKind.TRIE_INSERT.value,
    PatternKind.TRIE_EXACT_SEARCH.value,
    PatternKind.TRIE_PREFIX_SEARCH.value,
    PatternKind.TRIE_PREFIX_COUNT.value,
    PatternKind.TRIE_WORD_COUNT.value,
    PatternKind.TRIE_DELETION.value,
    PatternKind.TRIE_LONGEST_PREFIX.value,
    PatternKind.TRIE_MAX_XOR_PAIR.value,
    PatternKind.TRIE_MAX_XOR_QUERY.value,
    PatternKind.TRIE_LEXICOGRAPHIC_SORT.value,
    PatternKind.TRIE_AUTOCOMPLETE.value,
}

# All Tree pattern names as a set (for fast lookup)
TREE_PATTERNS = {
    PatternKind.TREE_DFS_PREORDER.value,
    PatternKind.TREE_DFS_INORDER.value,
    PatternKind.TREE_DFS_POSTORDER.value,
    PatternKind.TREE_BFS_LEVEL_ORDER.value,
    PatternKind.TREE_DEPTH_HEIGHT.value,
    PatternKind.TREE_SUBTREE_SIZE.value,
    PatternKind.TREE_LEAF_COUNT.value,
    PatternKind.TREE_SUBTREE_AGGREGATION.value,
    PatternKind.TREE_PATH_SUM.value,
    PatternKind.TREE_DIAMETER.value,
    PatternKind.TREE_BST_SEARCH.value,
    PatternKind.TREE_BST_INSERT.value,
    PatternKind.TREE_BST_DELETE.value,
    PatternKind.TREE_BST_MIN_MAX.value,
    PatternKind.TREE_BST_PRED_SUCC.value,
    PatternKind.TREE_BST_VALIDATE.value,
    PatternKind.TREE_LCA_BINARY_TREE.value,
    PatternKind.TREE_LCA_BST.value,
    PatternKind.TREE_LCA_PARENT_ARRAY.value,
    PatternKind.TREE_DP_INDEPENDENT_SET.value,
    PatternKind.TREE_DP_SUBTREE_WEIGHT.value,
    PatternKind.TREE_DP_TWO_STATE.value,
}

# All Graph pattern names as a set (for fast lookup) — Phase 3F
GRAPH_PATTERNS = {
    PatternKind.GRAPH_BFS_SHORTEST_PATH.value,
    PatternKind.GRAPH_DFS_TRAVERSAL.value,
    PatternKind.GRAPH_CONNECTED_COMPONENTS.value,
    PatternKind.GRAPH_CYCLE_DETECTION_UNDIRECTED.value,
    PatternKind.GRAPH_CYCLE_DETECTION_DIRECTED.value,
    PatternKind.GRAPH_BIPARTITE_COLORING.value,
    PatternKind.GRAPH_DIJKSTRA.value,
    PatternKind.GRAPH_BELLMAN_FORD.value,
    PatternKind.GRAPH_FLOYD_WARSHALL.value,
    PatternKind.GRAPH_TOPOLOGICAL_SORT.value,
    PatternKind.GRAPH_DAG_DP.value,
    PatternKind.GRAPH_DSU.value,
    PatternKind.GRAPH_MST_KRUSKAL.value,
    PatternKind.GRAPH_MST_PRIM.value,
    PatternKind.GRAPH_SCC_TARJAN.value,
    PatternKind.GRAPH_BRIDGES_ARTICULATION.value,
}

# All Heap pattern names as a set (for fast lookup) — Phase 3G
HEAP_PATTERNS = {
    PatternKind.HEAP_MIN_PRIORITY_QUEUE.value,
    PatternKind.HEAP_MAX_PRIORITY_QUEUE.value,
    PatternKind.HEAP_BUILD.value,
    PatternKind.HEAP_TOP_K.value,
    PatternKind.HEAP_KTH_ELEMENT.value,
    PatternKind.HEAP_K_WAY_MERGE.value,
    PatternKind.HEAP_TWO_HEAPS.value,
    PatternKind.HEAP_DYNAMIC_MEDIAN.value,
    PatternKind.HEAP_SCHEDULING.value,
    PatternKind.HEAP_GREEDY_SELECTION.value,
    PatternKind.HEAP_LAZY_DELETION.value,
}

# All Disjoint Set Union pattern names as a set (for fast lookup) — Phase 3H
DSU_PATTERNS = {
    PatternKind.DSU_BASIC.value,
    PatternKind.DSU_COMPONENT_METADATA.value,
    PatternKind.DSU_DYNAMIC_CONNECTIVITY.value,
    PatternKind.DSU_WEIGHTED.value,
    PatternKind.DSU_POTENTIAL_DIFFERENCE.value,
    PatternKind.DSU_PARITY.value,
    PatternKind.DSU_ROLLBACK.value,
    PatternKind.DSU_OFFLINE_DYNAMIC_CONNECTIVITY.value,
    PatternKind.DSU_KRUSKAL_SUPPORT.value,
    PatternKind.DSU_CONSTRAINT_CONSISTENCY.value,
}

# All Fenwick Tree pattern names as a set (for fast lookup) — Phase 3I
FENWICK_PATTERNS = {
    PatternKind.FENWICK_POINT_UPDATE_PREFIX_QUERY.value,
    PatternKind.FENWICK_RANGE_UPDATE_POINT_QUERY.value,
    PatternKind.FENWICK_RANGE_UPDATE_RANGE_QUERY.value,
    PatternKind.FENWICK_FREQUENCY.value,
    PatternKind.FENWICK_PREFIX_EXTREMUM.value,
    PatternKind.FENWICK_2D_POINT_UPDATE_RANGE_QUERY.value,
    PatternKind.FENWICK_KTH_ELEMENT.value,
    PatternKind.FENWICK_INVERSION_COUNTING.value,
    PatternKind.FENWICK_MULTISET.value,
    PatternKind.FENWICK_COORDINATE_COMPRESSION.value,
}

# All Segment Tree pattern names as a set (for fast lookup) — Phase 3J
SEGMENT_TREE_PATTERNS = {
    PatternKind.SEGMENT_TREE_POINT_UPDATE_RANGE_QUERY.value,
    PatternKind.SEGMENT_TREE_RANGE_ADD_RANGE_QUERY.value,
    PatternKind.SEGMENT_TREE_RANGE_ASSIGN_RANGE_QUERY.value,
    PatternKind.SEGMENT_TREE_COMBINED_LAZY_RANGE_QUERY.value,
    PatternKind.SEGMENT_TREE_METADATA_AGGREGATE.value,
    PatternKind.SEGMENT_TREE_MAX_SUBARRAY.value,
    PatternKind.SEGMENT_TREE_FREQUENCY_ORDER_STATISTIC.value,
    PatternKind.SEGMENT_TREE_INTERVAL_STATISTICS.value,
}

# All Dynamic Programming pattern names as a set (for fast lookup) — Phase 3K
DP_PATTERNS = {
    PatternKind.DP_1D_LINEAR.value,
    PatternKind.DP_GRID_2D.value,
    PatternKind.DP_KNAPSACK.value,
    PatternKind.DP_SUBSEQUENCE_STRING.value,
    PatternKind.DP_INTERVAL.value,
    PatternKind.DP_PARTITION.value,
    PatternKind.DP_STATE_MACHINE.value,
    PatternKind.DP_BITMASK.value,
    PatternKind.DP_TREE.value,
    PatternKind.DP_DAG.value,
    PatternKind.DP_DIGIT.value,
    PatternKind.DP_OPTIMIZATION.value,
    PatternKind.DP_SOLUTION_RECONSTRUCTION.value,
    PatternKind.DP_SPACE_OPTIMIZATION.value,
}

# All Greedy pattern names as a set (for fast lookup) — Phase 3L
GREEDY_PATTERNS = {
    PatternKind.GREEDY_INTERVAL_SELECTION.value,
    PatternKind.GREEDY_INTERVAL_COVERING.value,
    PatternKind.GREEDY_FRACTIONAL_KNAPSACK.value,
    PatternKind.GREEDY_DEADLINE_SCHEDULING.value,
    PatternKind.GREEDY_HEAP_ASSISTED.value,
    PatternKind.GREEDY_HUFFMAN_MERGE.value,
    PatternKind.GREEDY_SEQUENCE_LOCAL_CHOICE.value,
    PatternKind.GREEDY_REACHABILITY_PARTITION.value,
    PatternKind.GREEDY_GRAPH_MST.value,
    PatternKind.GREEDY_GENERAL_EXCHANGE.value,
}

GREEDY_PROOF_PATTERNS = {
    PatternKind.GREEDY_EXCHANGE_PROOF.value,
    PatternKind.GREEDY_STAYING_AHEAD_PROOF.value,
    PatternKind.GREEDY_DOMINANCE_PROOF.value,
    PatternKind.GREEDY_SAFE_CUT_PROOF.value,
    PatternKind.GREEDY_MATROID_PROOF.value,
}

# All Divide and Conquer & Backtracking pattern names as a set (for fast lookup) — Phase 3M
DC_BACKTRACKING_PATTERNS = {
    PatternKind.DC_MERGE_SORT_INVERSIONS.value,
    PatternKind.DC_QUICKSELECT.value,
    PatternKind.DC_CLOSEST_PAIR.value,
    PatternKind.DC_TREE_CENTROID.value,
    PatternKind.DC_CDQ_DIVIDE_AND_CONQUER.value,
    PatternKind.BACKTRACKING_SUBSETS_PERMUTATIONS.value,
    PatternKind.BACKTRACKING_CONSTRAINT_SATISFACTION.value,
    PatternKind.BACKTRACKING_BRANCH_AND_BOUND.value,
    PatternKind.BACKTRACKING_STATE_SPACE_SEARCH.value,
    PatternKind.BACKTRACKING_MEET_IN_THE_MIDDLE.value,
}

# All Advanced Graph pattern names as a set (for fast lookup) — Phase 3N
ADV_GRAPH_PATTERNS = {
    PatternKind.ADV_GRAPH_01_BFS.value,
    PatternKind.ADV_GRAPH_SPFA_NEGATIVE_CYCLE.value,
    PatternKind.ADV_GRAPH_EULERIAN_PATH.value,
    PatternKind.ADV_GRAPH_2SAT.value,
    PatternKind.ADV_GRAPH_BLOCK_CUT_TREE.value,
    PatternKind.ADV_GRAPH_BRIDGE_BLOCK_TREE.value,
    PatternKind.ADV_GRAPH_BIPARTITE_MATCHING.value,
    PatternKind.ADV_GRAPH_MAX_FLOW_DINIC.value,
    PatternKind.ADV_GRAPH_MIN_CUT.value,
    PatternKind.ADV_GRAPH_MCMF.value,
}

# All String Algorithms & Automata pattern names as a set (for fast lookup) — Phase 3O
STRING_PATTERNS = {
    PatternKind.STRING_KMP_SEARCH.value,
    PatternKind.STRING_Z_ALGORITHM.value,
    PatternKind.STRING_RABIN_KARP.value,
    PatternKind.STRING_MANACHER.value,
    PatternKind.STRING_AHO_CORASICK.value,
    PatternKind.STRING_SUFFIX_ARRAY.value,
    PatternKind.STRING_SUFFIX_AUTOMATON.value,
    PatternKind.STRING_LYNDON_DUVAL.value,
    PatternKind.STRING_SUBSEQUENCE_AUTOMATON.value,
    PatternKind.STRING_LONGEST_COMMON_SUBSTRING_SAM.value,
}

# All Number Theory & Combinatorics pattern names as a set (for fast lookup) — Phase 3P
NUMBER_THEORY_PATTERNS = {
    PatternKind.NT_EXTENDED_GCD.value,
    PatternKind.NT_MODULAR_INVERSE.value,
    PatternKind.NT_CHINESE_REMAINDER.value,
    PatternKind.NT_LINEAR_SIEVE.value,
    PatternKind.NT_EULER_TOTIENT.value,
    PatternKind.NT_MOBIUS_INVERSION.value,
    PatternKind.NT_MATRIX_POWER.value,
    PatternKind.NT_COMBINATORICS_FACTORIALS.value,
    PatternKind.NT_LUCAS_THEOREM.value,
    PatternKind.NT_MILLER_RABIN.value,
    # Common structural aliases
    "nt_modular_inverse_extgcd",
    "nt_modular_inverse_fermat",
    "nt_euler_totient_single",
    "nt_euler_totient_sieve",
    "nt_matrix_exponentiation",
    "nt_factorial_combinatorics",
    "nt_diophantine",
    "nt_crt",
    "nt_prime_factorization",
    "nt_phi",
    "nt_mobius_sieve",
    "nt_linear_recurrence",
    "nt_ncr_mod_p",
    "nt_lucas",
    "nt_primality_test",
}

# All Algebra & Transforms pattern names as a set (for fast lookup) — Phase 3Q
ALGEBRA_PATTERNS = {
    PatternKind.ALGEBRA_FFT.value,
    PatternKind.ALGEBRA_NTT.value,
    PatternKind.ALGEBRA_FWHT.value,
    PatternKind.ALGEBRA_POLY_INVERSE.value,
    PatternKind.ALGEBRA_GAUSS_REAL.value,
    PatternKind.ALGEBRA_GAUSS_MODULAR.value,
    PatternKind.ALGEBRA_GAUSS_XOR.value,
    PatternKind.ALGEBRA_LINEAR_BASIS.value,
    PatternKind.ALGEBRA_BERLEKAMP_MASSEY.value,
    PatternKind.ALGEBRA_LAGRANGE_INTERPOLATION.value,
}

# All Computational Geometry pattern names as a set (for fast lookup) — Phase 3R
GEOMETRY_PATTERNS = {
    PatternKind.GEOM_ORIENTATION_CROSS_PRODUCT.value,
    PatternKind.GEOM_SEGMENT_INTERSECTION.value,
    PatternKind.GEOM_CONVEX_HULL_ANDREW.value,
    PatternKind.GEOM_POLYGON_AREA_SHOELACE.value,
    PatternKind.GEOM_POINT_IN_POLYGON.value,
    PatternKind.GEOM_CLOSEST_PAIR_POINTS.value,
    PatternKind.GEOM_LINE_INTERSECTION_POINT.value,
    PatternKind.GEOM_ROTATING_CALIPERS_DIAMETER.value,
    PatternKind.GEOM_HALFPLANE_INTERSECTION.value,
    PatternKind.GEOM_SWEEP_LINE_SEGMENTS.value,
}

# All Advanced Data Structures pattern names as a set (for fast lookup) — Phase 3S
ADV_DATA_STRUCTURES_PATTERNS = {
    PatternKind.ADS_SPARSE_TABLE.value,
    PatternKind.ADS_LCA_BINARY_LIFTING.value,
    PatternKind.ADS_HEAVY_LIGHT_DECOMPOSITION.value,
    PatternKind.ADS_CENTROID_DECOMPOSITION.value,
    PatternKind.ADS_PERSISTENT_SEGMENT_TREE.value,
    PatternKind.ADS_DYNAMIC_SEGMENT_TREE.value,
    PatternKind.ADS_MERGE_SORT_TREE.value,
    PatternKind.ADS_SQRT_DECOMPOSITION.value,
    PatternKind.ADS_MOS_ALGORITHM.value,
    PatternKind.ADS_SEGMENT_TREE_BEATS.value,
}

# All Cross-Family Composition pattern names as a set (for fast lookup) — Phase 4
CROSS_FAMILY_PATTERNS = {
    PatternKind.CF_KRUSKAL_MST.value,
    PatternKind.CF_DIJKSTRA_SHORTEST_PATH.value,
    PatternKind.CF_BOTTLENECK_PATH_BINARY_SEARCH.value,
    PatternKind.CF_GRAPH_SEGMENT_TREE_RELAXATION.value,
    PatternKind.CF_TREE_SUBTREE_DP.value,
    PatternKind.CF_TREE_PATH_HLD_SEGMENT_TREE.value,
    PatternKind.CF_EVENT_SCHEDULING_GREEDY_HEAP.value,
    PatternKind.CF_INCREMENTAL_CONNECTIVITY_GREEDY_DSU.value,
    PatternKind.CF_DP_RANGE_ACCELERATION_SEGMENT_TREE.value,
    PatternKind.CF_CONVEX_DP_MONOTONIC_QUEUE.value,
    PatternKind.CF_BISECTION_GREEDY_FEASIBILITY.value,
    PatternKind.CF_FRACTIONAL_BISECTION_DP.value,
}

TAXONOMY_TREE: Dict[str, Any] = {
    "Pointer-Based Algorithms": {
        "Two Pointers": {
            "Converging": [
                PatternKind.PAIR_SUM_SORTED,
                PatternKind.CLOSEST_PAIR_SUM,
                PatternKind.THREE_SUM_CONVERGING,
                PatternKind.FOUR_SUM_CONVERGING,
                PatternKind.CONTAINER_MOST_WATER,
                PatternKind.TRAPPING_RAIN_WATER,
                PatternKind.PALINDROME_VERIFICATION,
                PatternKind.PAIR_DIFFERENCE
            ],
            "Same Direction": [
                PatternKind.IN_PLACE_COMPACTION,
                PatternKind.REMOVE_DUPLICATES_SORTED,
                PatternKind.MOVE_ZEROES_ORDERED,
                PatternKind.CHASE_POINTER_DIFFERENCE,
                PatternKind.MERGE_SORTED_ARRAYS
            ],
            "Sliding Window": [
                PatternKind.SLIDING_WINDOW_FIXED,
                PatternKind.SLIDING_WINDOW_VARIABLE_MIN,
                PatternKind.SLIDING_WINDOW_VARIABLE_MAX,
                PatternKind.MINIMUM_WINDOW_SUBSTRING
            ],
            "Counting Pointers": [
                PatternKind.COUNT_PAIRS_LESS_THAN_K,
                PatternKind.COUNT_PAIRS_EQUAL_K,
                PatternKind.COUNT_SUBARRAYS_BOUNDED,
                PatternKind.EXACT_COUNT_DERIVED
            ]
        },
        "Partition Pointers": [
            PatternKind.PARTITION_TWO_WAY,
            PatternKind.PARTITION_DUTCH_FLAG
        ],
        "Fast/Slow Pointers": {
            "Linked Structures": [
                PatternKind.LINKED_CYCLE_DETECTION,
                PatternKind.LINKED_CYCLE_START,
                PatternKind.LINKED_MIDDLE_NODE
            ]
        },
        "Monotonic Stack": {
            "Directional Boundary": [
                PatternKind.NEXT_GREATER_ELEMENT,
                PatternKind.NEXT_SMALLER_ELEMENT,
                PatternKind.PREVIOUS_GREATER_ELEMENT,
                PatternKind.PREVIOUS_SMALLER_ELEMENT,
                PatternKind.NEAREST_GREATER_ELEMENT,
                PatternKind.NEAREST_SMALLER_ELEMENT,
            ],
            "Distance and Span": [
                PatternKind.STOCK_SPAN,
            ],
            "Structural Applications": [
                PatternKind.LARGEST_RECTANGLE_HISTOGRAM,
                PatternKind.CIRCULAR_NEXT_GREATER,
            ],
            "Contribution Counting": [
                PatternKind.SUM_SUBARRAY_MINIMUMS,
                PatternKind.SUM_SUBARRAY_MAXIMUMS,
            ]
        },
        "Binary Search": {
            "Ordered Data Search": [
                PatternKind.BINARY_SEARCH_EXACT,
                PatternKind.LOWER_BOUND,
                PatternKind.UPPER_BOUND,
                PatternKind.FIRST_TRUE,
                PatternKind.LAST_TRUE,
                PatternKind.FIRST_FALSE,
                PatternKind.LAST_FALSE,
                PatternKind.PREDECESSOR,
                PatternKind.SUCCESSOR,
            ],
            "Binary Search on Answer": [
                PatternKind.BINARY_SEARCH_ANSWER_MIN,
                PatternKind.BINARY_SEARCH_ANSWER_MAX,
            ],
            "Value Domain Search": [
                PatternKind.BINARY_SEARCH_VALUE_DOMAIN,
            ]
        },
        "Trie": {
            "Character Trie": [
                PatternKind.TRIE_INSERT,
                PatternKind.TRIE_EXACT_SEARCH,
                PatternKind.TRIE_PREFIX_SEARCH,
                PatternKind.TRIE_PREFIX_COUNT,
                PatternKind.TRIE_WORD_COUNT,
                PatternKind.TRIE_DELETION,
                PatternKind.TRIE_LONGEST_PREFIX,
                PatternKind.TRIE_AUTOCOMPLETE,
                PatternKind.TRIE_LEXICOGRAPHIC_SORT,
            ],
            "Binary Trie": [
                PatternKind.TRIE_MAX_XOR_PAIR,
                PatternKind.TRIE_MAX_XOR_QUERY,
            ]
        },
        "Tree": {
            "Traversals": [
                PatternKind.TREE_DFS_PREORDER,
                PatternKind.TREE_DFS_INORDER,
                PatternKind.TREE_DFS_POSTORDER,
                PatternKind.TREE_BFS_LEVEL_ORDER,
            ],
            "Subtree Aggregations & Metrics": [
                PatternKind.TREE_DEPTH_HEIGHT,
                PatternKind.TREE_SUBTREE_SIZE,
                PatternKind.TREE_LEAF_COUNT,
                PatternKind.TREE_SUBTREE_AGGREGATION,
                PatternKind.TREE_PATH_SUM,
                PatternKind.TREE_DIAMETER,
            ],
            "Binary Search Tree": [
                PatternKind.TREE_BST_SEARCH,
                PatternKind.TREE_BST_INSERT,
                PatternKind.TREE_BST_DELETE,
                PatternKind.TREE_BST_MIN_MAX,
                PatternKind.TREE_BST_PRED_SUCC,
                PatternKind.TREE_BST_VALIDATE,
            ],
            "Lowest Common Ancestor": [
                PatternKind.TREE_LCA_BINARY_TREE,
                PatternKind.TREE_LCA_BST,
                PatternKind.TREE_LCA_PARENT_ARRAY,
            ],
            "Tree Dynamic Programming": [
                PatternKind.TREE_DP_INDEPENDENT_SET,
                PatternKind.TREE_DP_SUBTREE_WEIGHT,
                PatternKind.TREE_DP_TWO_STATE,
            ]
        },
        "Graph": {
            "Traversal & Reachability": [
                PatternKind.GRAPH_BFS_SHORTEST_PATH,
                PatternKind.GRAPH_DFS_TRAVERSAL,
                PatternKind.GRAPH_CONNECTED_COMPONENTS,
            ],
            "Cycle Detection": [
                PatternKind.GRAPH_CYCLE_DETECTION_UNDIRECTED,
                PatternKind.GRAPH_CYCLE_DETECTION_DIRECTED,
            ],
            "Coloring & Ordering": [
                PatternKind.GRAPH_BIPARTITE_COLORING,
                PatternKind.GRAPH_TOPOLOGICAL_SORT,
            ],
            "Shortest Path": [
                PatternKind.GRAPH_DIJKSTRA,
                PatternKind.GRAPH_BELLMAN_FORD,
                PatternKind.GRAPH_FLOYD_WARSHALL,
            ],
            "DAG Dynamic Programming": [
                PatternKind.GRAPH_DAG_DP,
            ],
            "Connectivity & MST": [
                PatternKind.GRAPH_DSU,
                PatternKind.GRAPH_MST_KRUSKAL,
                PatternKind.GRAPH_MST_PRIM,
            ],
            "Strongly Connected Components": [
                PatternKind.GRAPH_SCC_TARJAN,
            ],
            "Bridges & Articulation Points": [
                PatternKind.GRAPH_BRIDGES_ARTICULATION,
            ]
        },
        "Heap": {
            "Basic Priority Queue": [
                PatternKind.HEAP_MIN_PRIORITY_QUEUE,
                PatternKind.HEAP_MAX_PRIORITY_QUEUE,
                PatternKind.HEAP_BUILD,
            ],
            "Extremal Selection & Subsets": [
                PatternKind.HEAP_TOP_K,
                PatternKind.HEAP_KTH_ELEMENT,
            ],
            "Stream Merging & Frontiers": [
                PatternKind.HEAP_K_WAY_MERGE,
            ],
            "Dual Frontiers & Partitioning": [
                PatternKind.HEAP_TWO_HEAPS,
                PatternKind.HEAP_DYNAMIC_MEDIAN,
            ],
            "Greedy Choice & Simulation": [
                PatternKind.HEAP_SCHEDULING,
                PatternKind.HEAP_GREEDY_SELECTION,
                PatternKind.HEAP_LAZY_DELETION,
            ],
        },
        "Disjoint Set Union": {
            "Basic Equivalence Classes": [
                PatternKind.DSU_BASIC,
                PatternKind.DSU_DYNAMIC_CONNECTIVITY,
                PatternKind.DSU_KRUSKAL_SUPPORT,
            ],
            "Component Aggregates": [
                PatternKind.DSU_COMPONENT_METADATA,
            ],
            "Constraint & Potential DSU": [
                PatternKind.DSU_WEIGHTED,
                PatternKind.DSU_POTENTIAL_DIFFERENCE,
                PatternKind.DSU_PARITY,
                PatternKind.DSU_CONSTRAINT_CONSISTENCY,
            ],
            "Historical & Offline DSU": [
                PatternKind.DSU_ROLLBACK,
                PatternKind.DSU_OFFLINE_DYNAMIC_CONNECTIVITY,
            ],
        },
        "Fenwick Tree": {
            "Core Variants": [
                PatternKind.FENWICK_POINT_UPDATE_PREFIX_QUERY,
                PatternKind.FENWICK_RANGE_UPDATE_POINT_QUERY,
                PatternKind.FENWICK_RANGE_UPDATE_RANGE_QUERY,
                PatternKind.FENWICK_FREQUENCY,
                PatternKind.FENWICK_PREFIX_EXTREMUM,
                PatternKind.FENWICK_2D_POINT_UPDATE_RANGE_QUERY,
            ],
            "Applications": [
                PatternKind.FENWICK_KTH_ELEMENT,
                PatternKind.FENWICK_INVERSION_COUNTING,
                PatternKind.FENWICK_MULTISET,
            ],
            "Transformations": [
                PatternKind.FENWICK_COORDINATE_COMPRESSION,
            ]
        },
        "Segment Tree": {
            "Core Variants": [
                PatternKind.SEGMENT_TREE_POINT_UPDATE_RANGE_QUERY,
                PatternKind.SEGMENT_TREE_RANGE_ADD_RANGE_QUERY,
                PatternKind.SEGMENT_TREE_RANGE_ASSIGN_RANGE_QUERY,
                PatternKind.SEGMENT_TREE_COMBINED_LAZY_RANGE_QUERY,
                PatternKind.SEGMENT_TREE_METADATA_AGGREGATE,
            ],
            "Applications": [
                PatternKind.SEGMENT_TREE_MAX_SUBARRAY,
                PatternKind.SEGMENT_TREE_FREQUENCY_ORDER_STATISTIC,
                PatternKind.SEGMENT_TREE_INTERVAL_STATISTICS,
            ]
        },
        "Dynamic Programming": {
            "Linear & Sequence": [
                PatternKind.DP_1D_LINEAR,
                PatternKind.DP_SUBSEQUENCE_STRING,
                PatternKind.DP_PARTITION,
                PatternKind.DP_STATE_MACHINE,
            ],
            "Multi-Dimensional & Grid": [
                PatternKind.DP_GRID_2D,
                PatternKind.DP_KNAPSACK,
                PatternKind.DP_INTERVAL,
            ],
            "Combinatorial & Structural": [
                PatternKind.DP_BITMASK,
                PatternKind.DP_TREE,
                PatternKind.DP_DAG,
                PatternKind.DP_DIGIT,
            ],
            "Optimizations & Transformations": [
                PatternKind.DP_OPTIMIZATION,
                PatternKind.DP_SOLUTION_RECONSTRUCTION,
                PatternKind.DP_SPACE_OPTIMIZATION,
            ]
        },
        "Greedy Algorithms": {
            "Interval & Scheduling": [
                PatternKind.GREEDY_INTERVAL_SELECTION,
                PatternKind.GREEDY_INTERVAL_COVERING,
                PatternKind.GREEDY_DEADLINE_SCHEDULING,
            ],
            "Resource Allocation & Merging": [
                PatternKind.GREEDY_FRACTIONAL_KNAPSACK,
                PatternKind.GREEDY_HEAP_ASSISTED,
                PatternKind.GREEDY_HUFFMAN_MERGE,
            ],
            "Sequence & Reachability": [
                PatternKind.GREEDY_SEQUENCE_LOCAL_CHOICE,
                PatternKind.GREEDY_REACHABILITY_PARTITION,
            ],
            "Graph & General Exchange": [
                PatternKind.GREEDY_GRAPH_MST,
                PatternKind.GREEDY_GENERAL_EXCHANGE,
            ],
            "Proof Capabilities": [
                PatternKind.GREEDY_EXCHANGE_PROOF,
                PatternKind.GREEDY_STAYING_AHEAD_PROOF,
                PatternKind.GREEDY_DOMINANCE_PROOF,
                PatternKind.GREEDY_SAFE_CUT_PROOF,
                PatternKind.GREEDY_MATROID_PROOF,
            ]
        },
        "Divide & Conquer and Backtracking": {
            "Divide and Conquer": [
                PatternKind.DC_MERGE_SORT_INVERSIONS,
                PatternKind.DC_QUICKSELECT,
                PatternKind.DC_CLOSEST_PAIR,
                PatternKind.DC_TREE_CENTROID,
                PatternKind.DC_CDQ_DIVIDE_AND_CONQUER,
            ],
            "Backtracking & Exponential Search": [
                PatternKind.BACKTRACKING_SUBSETS_PERMUTATIONS,
                PatternKind.BACKTRACKING_CONSTRAINT_SATISFACTION,
                PatternKind.BACKTRACKING_BRANCH_AND_BOUND,
                PatternKind.BACKTRACKING_STATE_SPACE_SEARCH,
                PatternKind.BACKTRACKING_MEET_IN_THE_MIDDLE,
            ]
        },
        "Advanced Graph Algorithms": {
            "Shortest Paths & Walks": [
                PatternKind.ADV_GRAPH_01_BFS,
                PatternKind.ADV_GRAPH_SPFA_NEGATIVE_CYCLE,
                PatternKind.ADV_GRAPH_EULERIAN_PATH,
            ],
            "Logic & Decompositions": [
                PatternKind.ADV_GRAPH_2SAT,
                PatternKind.ADV_GRAPH_BLOCK_CUT_TREE,
                PatternKind.ADV_GRAPH_BRIDGE_BLOCK_TREE,
            ],
            "Matchings & Network Flows": [
                PatternKind.ADV_GRAPH_BIPARTITE_MATCHING,
                PatternKind.ADV_GRAPH_MAX_FLOW_DINIC,
                PatternKind.ADV_GRAPH_MIN_CUT,
                PatternKind.ADV_GRAPH_MCMF,
            ]
        },
        "String Algorithms & Automata": {
            "Pattern Matching": [
                PatternKind.STRING_KMP_SEARCH,
                PatternKind.STRING_Z_ALGORITHM,
                PatternKind.STRING_RABIN_KARP,
                PatternKind.STRING_AHO_CORASICK,
            ],
            "Palindromes & Suffixes": [
                PatternKind.STRING_MANACHER,
                PatternKind.STRING_SUFFIX_ARRAY,
                PatternKind.STRING_SUFFIX_AUTOMATON,
                PatternKind.STRING_LONGEST_COMMON_SUBSTRING_SAM,
            ],
            "Rotations & Subsequences": [
                PatternKind.STRING_LYNDON_DUVAL,
                PatternKind.STRING_SUBSEQUENCE_AUTOMATON,
            ]
        },
        "Number Theory & Combinatorics": {
            "Modular & Diophantine": [
                PatternKind.NT_EXTENDED_GCD,
                PatternKind.NT_MODULAR_INVERSE,
                PatternKind.NT_CHINESE_REMAINDER,
            ],
            "Multiplicative & Sieve": [
                PatternKind.NT_LINEAR_SIEVE,
                PatternKind.NT_EULER_TOTIENT,
                PatternKind.NT_MOBIUS_INVERSION,
            ],
            "Algebraic & Primality": [
                PatternKind.NT_MATRIX_POWER,
                PatternKind.NT_COMBINATORICS_FACTORIALS,
                PatternKind.NT_LUCAS_THEOREM,
                PatternKind.NT_MILLER_RABIN,
            ]
        },
        "Algebra & Transforms": {
            "Transforms": [
                PatternKind.ALGEBRA_FFT,
                PatternKind.ALGEBRA_NTT,
                PatternKind.ALGEBRA_FWHT,
            ],
            "Polynomials & Systems": [
                PatternKind.ALGEBRA_POLY_INVERSE,
                PatternKind.ALGEBRA_GAUSS_REAL,
                PatternKind.ALGEBRA_GAUSS_MODULAR,
                PatternKind.ALGEBRA_GAUSS_XOR,
                PatternKind.ALGEBRA_LINEAR_BASIS,
                PatternKind.ALGEBRA_BERLEKAMP_MASSEY,
                PatternKind.ALGEBRA_LAGRANGE_INTERPOLATION,
            ]
        },
        "Computational Geometry": {
            "Orientation & Predicates": [
                PatternKind.GEOM_ORIENTATION_CROSS_PRODUCT,
                PatternKind.GEOM_SEGMENT_INTERSECTION,
                PatternKind.GEOM_LINE_INTERSECTION_POINT,
            ],
            "Polygons & Containment": [
                PatternKind.GEOM_CONVEX_HULL_ANDREW,
                PatternKind.GEOM_POLYGON_AREA_SHOELACE,
                PatternKind.GEOM_POINT_IN_POLYGON,
            ],
            "Extremal & Sweep": [
                PatternKind.GEOM_CLOSEST_PAIR_POINTS,
                PatternKind.GEOM_ROTATING_CALIPERS_DIAMETER,
                PatternKind.GEOM_HALFPLANE_INTERSECTION,
                PatternKind.GEOM_SWEEP_LINE_SEGMENTS,
            ]
        },
        "Advanced Data Structures": {
            "Static & Path Decomposition": [
                PatternKind.ADS_SPARSE_TABLE,
                PatternKind.ADS_LCA_BINARY_LIFTING,
                PatternKind.ADS_HEAVY_LIGHT_DECOMPOSITION,
                PatternKind.ADS_CENTROID_DECOMPOSITION,
            ],
            "Persistent & Dynamic Trees": [
                PatternKind.ADS_PERSISTENT_SEGMENT_TREE,
                PatternKind.ADS_DYNAMIC_SEGMENT_TREE,
                PatternKind.ADS_MERGE_SORT_TREE,
                PatternKind.ADS_SEGMENT_TREE_BEATS,
            ],
            "Partition & Offline Batching": [
                PatternKind.ADS_SQRT_DECOMPOSITION,
                PatternKind.ADS_MOS_ALGORITHM,
            ]
        },
        "Cross-Family Composition": {
            "Graph Hybrids": [
                PatternKind.CF_KRUSKAL_MST,
                PatternKind.CF_DIJKSTRA_SHORTEST_PATH,
                PatternKind.CF_BOTTLENECK_PATH_BINARY_SEARCH,
                PatternKind.CF_GRAPH_SEGMENT_TREE_RELAXATION,
            ],
            "Tree Hybrids": [
                PatternKind.CF_TREE_SUBTREE_DP,
                PatternKind.CF_TREE_PATH_HLD_SEGMENT_TREE,
            ],
            "Greedy Hybrids": [
                PatternKind.CF_EVENT_SCHEDULING_GREEDY_HEAP,
                PatternKind.CF_INCREMENTAL_CONNECTIVITY_GREEDY_DSU,
            ],
            "DP Hybrids": [
                PatternKind.CF_DP_RANGE_ACCELERATION_SEGMENT_TREE,
                PatternKind.CF_CONVEX_DP_MONOTONIC_QUEUE,
            ],
            "Bisection Hybrids": [
                PatternKind.CF_BISECTION_GREEDY_FEASIBILITY,
                PatternKind.CF_FRACTIONAL_BISECTION_DP,
            ]
        }
    }
}

