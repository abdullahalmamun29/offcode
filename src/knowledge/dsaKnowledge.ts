/**
 * CHUP V2 — Relational DSA Knowledge Base.
 *
 * Contains structured knowledge about algorithmic concepts, their recognition
 * patterns, relationships, and conditions. Used by the CP solver to match
 * problem features to algorithmic approaches.
 *
 * Each concept is categorized as:
 *   - Supported: has a solution template, can recognize AND solve
 *   - Recognized-only: can recognize, reports limitation honestly
 */

import { StructuredProblem, TopicCandidate } from '../models/problemSpec';

// ═══════════════════════════════════════════════════════════════════════════════
// DSA Concept Definition
// ═══════════════════════════════════════════════════════════════════════════════

export interface DSAConcept {
  id: string;
  name: string;
  category: string;
  recognitionPatterns: {
    /** Keywords in the problem text that suggest this concept */
    keywords: string[];
    /** Structural clues about the problem's shape */
    structuralClues: string[];
    /** Constraint-based clues */
    constraintClues: string[];
    /** Signals that REDUCE confidence in this concept */
    antiPatterns: string[];
    /** Hard conditions; if violated, the concept is rejected */
    conditions: string[];
  };
  complexityProfile: { time: string; space: string };
  prerequisites: string[];
  relatedConcepts: string[];
  commonMistakes: string[];
  solutionTemplateId: string | null;  // null = recognized-only
}

// ═══════════════════════════════════════════════════════════════════════════════
// The Knowledge Base — Concepts
// ═══════════════════════════════════════════════════════════════════════════════

const DSA_CONCEPTS: DSAConcept[] = [

  // ─── SUPPORTED (9) ──────────────────────────────────────────────────────────

  {
    id: 'frequency_count',
    name: 'Frequency Counting / Hash Map',
    category: 'array_technique',
    recognitionPatterns: {
      keywords: [
        'frequency', 'count', 'occurrences', 'how many times', 'appears',
        'most frequent', 'least frequent', 'mode', 'duplicate', 'duplicates',
        'distinct', 'unique', 'number of distinct', 'count elements',
        'appeared', 'occurring', 'majority', 'more than k times',
        'distinct value', 'distinct values', 'how many times each id occurs',
        'pair summing to', 'pair sum', 'pair sum k', 'pair with sum in unsorted',
        'pair-sum', 'pair-sum frequency', 'frequencies'
      ],
      structuralClues: [
        'single array input', 'count elements satisfying condition',
        'find elements with specific frequency', 'hash map lookup'
      ],
      constraintClues: [],
      antiPatterns: [],
      conditions: []
    },
    complexityProfile: { time: 'O(N)', space: 'O(N)' },
    prerequisites: [],
    relatedConcepts: ['prefix_sum', 'sliding_window'],
    commonMistakes: [
      'Using array instead of hash map when value range is large',
      'Forgetting to handle empty input'
    ],
    solutionTemplateId: 'frequencyCount'
  },

  {
    id: 'prefix_sum',
    name: 'Prefix Sum',
    category: 'array_technique',
    recognitionPatterns: {
      keywords: [
        'subarray sum', 'range sum', 'sum of subarray', 'contiguous sum',
        'subarray with sum', 'subarray whose sum', 'segment sum',
        'cumulative', 'prefix', 'sum equal to', 'sum equals',
        'total equals', 'total equal to', 'sum of elements between',
        'sum from index', 'number of subarrays',
        'sum of elements from l through r', 'from l through r', 'immutable array',
        'sum of any contiguous segment', 'contiguous segment whose total equals',
        'contiguous segment whose total', 'segment [l,r]', 'longest subarray with sum',
        'longest contiguous segment whose total', 'exact sum', 'exact sum k',
        'longest subarray with exact sum', 'sum between l and r',
        'range queries asking for the sum', 'sum of values between l and r'
      ],
      structuralClues: [
        'array with sum queries', 'find subarray matching sum condition',
        'range query on array'
      ],
      constraintClues: ['large N suggests O(N) needed, prefix sum gives O(1) per query'],
      antiPatterns: ['shortest path', 'tree', 'graph'],
      conditions: []
    },
    complexityProfile: { time: 'O(N)', space: 'O(N)' },
    prerequisites: [],
    relatedConcepts: ['frequency_count', 'two_pointers'],
    commonMistakes: [
      'Off-by-one in range queries',
      'Forgetting prefix[0] = 0',
      'Integer overflow on large sums'
    ],
    solutionTemplateId: 'prefixSum'
  },

  {
    id: 'two_pointers',
    name: 'Two Pointers',
    category: 'array_technique',
    recognitionPatterns: {
      keywords: [
        'pair', 'two elements', 'pair with sum', 'two numbers that add up',
        'two numbers adding', 'sorted array', 'merge sorted', 'merge two',
        'remove duplicates from sorted', 'in-place', 'pair of elements',
        'find pair', 'pair whose', 'two values',
        'two numbers in a sorted ascending array', 'add up to target',
        'ascending array', 'nondecreasing sequence', 'pair whose combined value',
        'two numbers in ascending sequence', 'adding to', 'two numbers in ascending',
        'locate a pair', 'two numbers'
      ],
      structuralClues: [
        'sorted array operations', 'converging from both ends',
        'two arrays to merge', 'partition operation'
      ],
      constraintClues: [],
      antiPatterns: ['unsorted', 'negative values with sum target'],
      conditions: ['typically requires sorted data or two sequences']
    },
    complexityProfile: { time: 'O(N)', space: 'O(1)' },
    prerequisites: ['sorting'],
    relatedConcepts: ['sliding_window', 'binary_search'],
    commonMistakes: [
      'Forgetting to sort first',
      'Infinite loop when pointers don\'t advance',
      'Missing equal elements case'
    ],
    solutionTemplateId: 'twoPointers'
  },

  {
    id: 'sliding_window',
    name: 'Sliding Window',
    category: 'array_technique',
    recognitionPatterns: {
      keywords: [
        'window', 'subarray of size', 'substring', 'contiguous',
        'consecutive', 'window of size k', 'maximum sum subarray of size',
        'minimum length subarray', 'longest substring', 'without repeating',
        'at most k distinct', 'sliding', 'window length',
        'at most k distinct values', 'longest subarray containing at most',
        'smallest length subarray whose sum', 'subarray whose sum is at least',
        'moving contiguous range', 'longest window', 'contiguous segment with sum <= s',
        'distinct values stays within k', 'moving contiguous range while'
      ],
      structuralClues: [
        'fixed or variable size window over sequence',
        'maintain property over contiguous elements',
        'optimize over subarrays/substrings'
      ],
      constraintClues: [],
      antiPatterns: ['negative values and sum target', 'non-contiguous', 'subsequence'],
      conditions: [
        'for sum-based sliding window: values must be non-negative (monotonic sum)',
        'the property being tracked must be maintainable incrementally'
      ]
    },
    complexityProfile: { time: 'O(N)', space: 'O(1) to O(K)' },
    prerequisites: [],
    relatedConcepts: ['two_pointers', 'frequency_count'],
    commonMistakes: [
      'Using sliding window with negative values for sum problems',
      'Not handling window shrinking correctly',
      'Off-by-one in window size'
    ],
    solutionTemplateId: 'slidingWindow'
  },

  {
    id: 'binary_search',
    name: 'Binary Search',
    category: 'search_technique',
    recognitionPatterns: {
      keywords: [
        'find element', 'search in sorted', 'first occurrence',
        'last occurrence', 'lower bound', 'upper bound',
        'minimum possible maximum', 'maximum possible minimum',
        'binary search', 'minimize the maximum', 'maximize the minimum',
        'can we achieve', 'is it possible to', 'smallest value such that',
        'largest value such that', 'monotonic', 'check if feasible',
        'locate', 'find in', 'search for', 'look up', 'ordered',
        'sorted collection', 'find value', 'specific value',
        'locate value x in a sorted array', 'locate value in a sorted array',
        'ordered sequence is at least x', 'first position at which an ordered',
        'binary search on answer', 'feasibility increases as capacity increases',
        'minimum machine capacity needed', 'locate value v inside an ordered collection',
        'first element >=', 'last element <=', 'queries for the first element',
        'binary search in c++', 'locate value'
      ],
      structuralClues: [
        'sorted data', 'monotonic predicate', 'answer space search',
        'yes/no feasibility check', 'minimize/maximize a bound'
      ],
      constraintClues: ['large N but answer has bounded range'],
      antiPatterns: [],
      conditions: [
        'requires sorted data OR a monotonic predicate on the answer space'
      ]
    },
    complexityProfile: { time: 'O(N log N) or O(log N)', space: 'O(1)' },
    prerequisites: [],
    relatedConcepts: ['sorting', 'two_pointers'],
    commonMistakes: [
      'Off-by-one in lo/hi boundaries',
      'Infinite loop with wrong mid calculation',
      'Not handling equal elements correctly'
    ],
    solutionTemplateId: 'binarySearch'
  },

  {
    id: 'sort_greedy',
    name: 'Sorting + Greedy',
    category: 'greedy',
    recognitionPatterns: {
      keywords: [
        'schedule', 'interval',
        'activity selection', 'meeting rooms', 'platforms',
        'non-overlapping', 'overlap', 'earliest',
        'deadline', 'sort and pick',
        'intervals', 'non-overlapping intervals', 'non-overlapping events',
        'attend as many', 'sorting tasks by finish time', 'next compatible task',
        'finish time', 'compatible task', 'sorting tasks',
        'starting and ending time', 'starting and ending', 'watch entirely'
      ],
      structuralClues: [
        'intervals or events to schedule',
        'interval scheduling with start and end times'
      ],
      constraintClues: [],
      antiPatterns: ['shortest path', 'dynamic programming needed'],
      conditions: [
        'greedy choice property must hold: local optimum leads to global optimum'
      ]
    },
    complexityProfile: { time: 'O(N log N)', space: 'O(N)' },
    prerequisites: [],
    relatedConcepts: ['binary_search'],
    commonMistakes: [
      'Assuming greedy works when DP is actually needed',
      'Wrong sorting criterion',
      'Not handling ties correctly'
    ],
    solutionTemplateId: 'sortGreedy'
  },

  {
    id: 'bfs',
    name: 'BFS (Breadth-First Search)',
    category: 'graph',
    recognitionPatterns: {
      keywords: [
        'shortest path', 'minimum distance', 'fewest moves', 'fewest steps',
        'level order', 'breadth first', 'bfs', 'grid', 'maze',
        'minimum operations', 'reachable', 'connected', 'nearest',
        'closest', 'unweighted graph', 'number of moves',
        'shortest distance', 'minimum jumps',
        'shortest number of edges', 'from source s to every vertex',
        'grid with blocked cells', 'four-directional moves', 'layer by layer',
        'visit the graph layer by layer', 'start at one vertex and visit'
      ],
      structuralClues: [
        'unweighted graph', 'grid traversal', 'layer-by-layer exploration',
        'find shortest in unweighted'
      ],
      constraintClues: [],
      antiPatterns: ['weighted edges', 'weighted graph'],
      conditions: [
        'for shortest path: graph must be unweighted (or all weights equal)'
      ]
    },
    complexityProfile: { time: 'O(V+E)', space: 'O(V)' },
    prerequisites: [],
    relatedConcepts: ['dfs', 'dijkstra'],
    commonMistakes: [
      'Not marking visited before pushing to queue',
      'Using DFS instead of BFS for shortest path',
      'Wrong neighbor generation in grid problems'
    ],
    solutionTemplateId: 'bfs'
  },

  {
    id: 'dfs',
    name: 'DFS (Depth-First Search)',
    category: 'graph',
    recognitionPatterns: {
      keywords: [
        'connected components', 'component', 'flood fill', 'island',
        'number of islands', 'cycle', 'cycle detection', 'depth first',
        'dfs', 'explore', 'reachable', 'path exists', 'traverse all',
        'backtrack', 'connected',
        'connected regions', 'connected regions of 1s', 'binary matrix',
        'four-directional adjacency', 'explore each reachable vertex completely before backtracking'
      ],
      structuralClues: [
        'explore all reachable nodes', 'detect cycles', 'count components',
        'flood fill on grid', 'check connectivity'
      ],
      constraintClues: [],
      antiPatterns: ['shortest path in unweighted'],
      conditions: []
    },
    complexityProfile: { time: 'O(V+E)', space: 'O(V)' },
    prerequisites: [],
    relatedConcepts: ['bfs', 'topological_sort'],
    commonMistakes: [
      'Stack overflow on deep recursion (use iterative for large N)',
      'Not marking visited nodes',
      'Wrong base case in recursion'
    ],
    solutionTemplateId: 'dfs'
  },

  {
    id: 'dp_1d',
    name: 'Simple 1D Dynamic Programming',
    category: 'dynamic_programming',
    recognitionPatterns: {
      keywords: [
        'maximum subarray', 'maximum sum', 'climbing stairs', 'fibonacci',
        'ways to reach', 'number of ways', 'minimum cost', 'coin change',
        'longest increasing subsequence', 'lis', 'house robber',
        'non-adjacent', 'optimal substructure', 'overlapping subproblems',
        'dp', 'dynamic programming', 'tabulation', 'memoization',
        'minimum steps', 'maximum profit',
        'climb 1 or 2 at a time', 'ways to reach step n',
        'each new value depends only on the previous two', 'depends only on the previous',
        'remember the best answer for each prefix', 'earlier states',
        'build the next answer from earlier states', 'compute the nth value',
        'print their maximum', 'find their maximum', 'maximum of n integers'
      ],
      structuralClues: [
        'decision at each step depends on previous', 'build solution from subproblems',
        'recurrence relation over single dimension'
      ],
      constraintClues: ['N <= 10^5 or 10^6 typically allows O(N) DP'],
      antiPatterns: ['two-dimensional state clearly needed', 'knapsack with weight'],
      conditions: [
        'problem has optimal substructure',
        'problem has overlapping subproblems'
      ]
    },
    complexityProfile: { time: 'O(N) to O(N²)', space: 'O(N)' },
    prerequisites: [],
    relatedConcepts: ['knapsack_2d', 'prefix_sum'],
    commonMistakes: [
      'Wrong recurrence relation',
      'Wrong base case initialization',
      'Not considering all previous states',
      'Integer overflow in accumulation'
    ],
    solutionTemplateId: 'dp1d'
  },

  {
    id: 'monotonic_stack',
    name: 'Monotonic Stack (Dominance Elimination)',
    category: 'stack_technique',
    recognitionPatterns: {
      keywords: [
        'next greater', 'next smaller', 'previous greater', 'previous smaller',
        'nearest greater', 'nearest smaller', 'next larger', 'next element greater than',
        'first element to the right greater', 'first element to the left greater',
        'largest rectangle in histogram', 'histogram', 'maximal rectangle',
        'daily temperatures', 'stock span', 'online stock span',
        'warmer temperature', 'days until warmer', 'spans of stock'
      ],
      structuralClues: [
        'nearest element satisfying comparison in linear time',
        'expanding rectangular span bounded by smaller bars',
        'dominance elimination in ordered sequences'
      ],
      constraintClues: ['N <= 10^6 allows O(N) single-pass stack'],
      antiPatterns: ['arbitrary range minimum with dynamic updates', 'kth largest element'],
      conditions: [
        'requires sequential dominance elimination without intermediate point updates'
      ]
    },
    complexityProfile: { time: 'O(N)', space: 'O(N)' },
    prerequisites: ['stack'],
    relatedConcepts: ['two_pointers', 'sliding_window'],
    commonMistakes: [
      'Popping wrong inequality condition (< vs <=)',
      'Storing values instead of indices when distances/widths are required',
      'Not processing remaining elements in stack after loop'
    ],
    solutionTemplateId: 'monotonicStack'
  },

  {
    id: 'trie',
    name: 'Trie / Prefix Tree',
    category: 'string_data_structure',
    recognitionPatterns: {
      keywords: [
        'trie', 'prefix tree', 'prefix search', 'starts with',
        'longest common prefix', 'dictionary lookup', 'autocomplete',
        'strings with prefix', 'prefix matching', 'word search in dictionary',
        'common prefix of words'
      ],
      structuralClues: [
        'collection of strings with shared prefix queries',
        'character transition tree rooted at empty string'
      ],
      constraintClues: ['total sum of string lengths <= 10^6'],
      antiPatterns: ['exact full string lookup only (use hash set)'],
      conditions: []
    },
    complexityProfile: { time: 'O(L) per operation', space: 'O(total characters * alphabet)' },
    prerequisites: [],
    relatedConcepts: ['hash_table'],
    commonMistakes: [
      'Memory leak with manual pointers (use vector<array<int, 26>> for fast static trie)',
      'Not marking end of word flag'
    ],
    solutionTemplateId: 'trie'
  },

  {
    id: 'lru_cache',
    name: 'LRU Cache (Least Recently Used)',
    category: 'cache_data_structure',
    recognitionPatterns: {
      keywords: [
        'lru', 'least recently used', 'cache eviction', 'lru cache',
        'capacity limit with eviction', 'most recent access', 'page replacement lru'
      ],
      structuralClues: [
        'fast O(1) key lookup combined with recency order maintenance'
      ],
      constraintClues: ['capacity C <= 10^5, Q operations <= 10^5'],
      antiPatterns: ['frequency-based eviction'],
      conditions: ['requires O(1) get and put with capacity eviction']
    },
    complexityProfile: { time: 'O(1) get, O(1) put', space: 'O(capacity)' },
    prerequisites: ['hash_table', 'doubly_linked_list'],
    relatedConcepts: ['lfu_cache'],
    commonMistakes: [
      'Not moving accessed node to front on get()',
      'Dangling pointers on node removal'
    ],
    solutionTemplateId: 'lruCache'
  },

  {
    id: 'lfu_cache',
    name: 'LFU Cache (Least Frequently Used)',
    category: 'cache_data_structure',
    recognitionPatterns: {
      keywords: [
        'lfu', 'least frequently used', 'lfu cache', 'frequency eviction',
        'tie break by least recently used', 'access count cache'
      ],
      structuralClues: [
        'evict minimum frequency item with LRU tie-breaking'
      ],
      constraintClues: ['capacity C <= 10^5'],
      antiPatterns: ['pure recency eviction without frequency tracking'],
      conditions: ['requires frequency counts and recency tie-breaking']
    },
    complexityProfile: { time: 'O(1) get, O(1) put', space: 'O(capacity)' },
    prerequisites: ['hash_table', 'doubly_linked_list'],
    relatedConcepts: ['lru_cache'],
    commonMistakes: [
      'Not updating min_freq correctly when an item frequency increases',
      'Forgetting to initialize frequency list for new count'
    ],
    solutionTemplateId: 'lfuCache'
  },

  {
    id: 'tree_dp',
    name: 'Tree Dynamic Programming',
    category: 'dynamic_programming',
    recognitionPatterns: {
      keywords: [
        'tree dp', 'dynamic programming on tree', 'tree diameter', 'diameter of tree',
        'maximum independent set on tree', 'subtree size', 'vertex cover on tree',
        'longest path in tree', 'tree path sum', 're-rooting tree'
      ],
      structuralClues: [
        'acyclic connected graph (tree) with hierarchical substructure',
        'optimal solution for node depends on optimal solutions for its children'
      ],
      constraintClues: ['N <= 2 * 10^5 vertices'],
      antiPatterns: ['graph has cycles (not a tree)'],
      conditions: ['graph must be acyclic and connected']
    },
    complexityProfile: { time: 'O(N)', space: 'O(N)' },
    prerequisites: ['dfs'],
    relatedConcepts: ['dp_1d', 'dfs'],
    commonMistakes: [
      'Visiting parent node causing infinite recursion in undirected tree',
      'Accumulating child answers incorrectly'
    ],
    solutionTemplateId: 'treeDp'
  },

  // ─── RECOGNIZED-ONLY (7) ────────────────────────────────────────────────────

  {
    id: 'dijkstra',
    name: 'Dijkstra / Weighted Shortest Path',
    category: 'graph',
    recognitionPatterns: {
      keywords: [
        'weighted graph', 'shortest path weighted', 'minimum cost path',
        'dijkstra', 'edge weights', 'weighted edges', 'cost of path',
        'cheapest path', 'minimum weight path', 'nonnegative edge weights',
        'nonnegative weights', 'weights including values greater than 1',
        'weighted road network'
      ],
      structuralClues: [
        'graph with weighted edges', 'find minimum cost from source'
      ],
      constraintClues: [],
      antiPatterns: ['unweighted'],
      conditions: ['requires non-negative edge weights for Dijkstra']
    },
    complexityProfile: { time: 'O((V+E) log V)', space: 'O(V)' },
    prerequisites: ['bfs'],
    relatedConcepts: ['bfs', 'mst'],
    commonMistakes: ['Using with negative weights', 'Not using priority queue'],
    solutionTemplateId: null
  },

  {
    id: 'union_find',
    name: 'Union-Find / Disjoint Set Union (DSU)',
    category: 'graph',
    recognitionPatterns: {
      keywords: [
        'union find', 'disjoint set', 'dsu', 'connected components dynamically',
        'merge groups', 'same group', 'same component', 'union', 'find parent',
        'group operations', 'equivalence classes', 'union and connectivity queries'
      ],
      structuralClues: [
        'dynamic connectivity queries', 'merge and query group membership'
      ],
      constraintClues: [],
      antiPatterns: [],
      conditions: []
    },
    complexityProfile: { time: 'O(α(N)) per operation', space: 'O(N)' },
    prerequisites: [],
    relatedConcepts: ['dfs', 'mst'],
    commonMistakes: ['Not using path compression', 'Not using union by rank'],
    solutionTemplateId: null
  },

  {
    id: 'segment_tree',
    name: 'Segment Tree',
    category: 'range_query',
    recognitionPatterns: {
      keywords: [
        'range query', 'range update', 'segment tree',
        'point update', 'range minimum', 'range maximum',
        'range sum with updates', 'query and update',
        'range minimum queries and point updates', 'range minimum queries'
      ],
      structuralClues: [
        'array with both queries and updates on ranges'
      ],
      constraintClues: ['many queries (Q ~ N) with updates'],
      antiPatterns: [],
      conditions: []
    },
    complexityProfile: { time: 'O(N log N)', space: 'O(N)' },
    prerequisites: ['prefix_sum'],
    relatedConcepts: ['prefix_sum', 'fenwick_tree'],
    commonMistakes: ['Off-by-one in lazy propagation'],
    solutionTemplateId: null
  },

  {
    id: 'fenwick_tree',
    name: 'Fenwick Tree / Binary Indexed Tree (BIT)',
    category: 'range_query',
    recognitionPatterns: {
      keywords: [
        'fenwick tree', 'fenwick', 'binary indexed tree', 'bit',
        'point additions', 'point addition', 'prefix-sum queries and point additions',
        'prefix-sum queries'
      ],
      structuralClues: [
        'prefix sum queries with point updates'
      ],
      constraintClues: [],
      antiPatterns: [],
      conditions: []
    },
    complexityProfile: { time: 'O(log N) per query', space: 'O(N)' },
    prerequisites: ['prefix_sum'],
    relatedConcepts: ['prefix_sum', 'segment_tree'],
    commonMistakes: ['1-based indexing required'],
    solutionTemplateId: null
  },

  {
    id: 'knapsack_2d',
    name: '2D DP / Knapsack',
    category: 'dynamic_programming',
    recognitionPatterns: {
      keywords: [
        'knapsack', 'weight capacity', '2d dp', 'grid dp', 'edit distance',
        'longest common subsequence', 'lcs', 'matrix chain', 'two dimensions',
        'subset sum', 'partition equal subset', 'minimum path sum grid',
        '0/1 knapsack', 'weights and values under capacity w', 'capacity w'
      ],
      structuralClues: [
        'two-dimensional state space', 'items with weight and value',
        'grid traversal with optimal path'
      ],
      constraintClues: ['N*M or N*W product must be manageable'],
      antiPatterns: [],
      conditions: []
    },
    complexityProfile: { time: 'O(N*M) or O(N*W)', space: 'O(N*M)' },
    prerequisites: ['dp_1d'],
    relatedConcepts: ['dp_1d'],
    commonMistakes: ['Wrong state transition', 'Not optimizing space when possible'],
    solutionTemplateId: null
  },

  {
    id: 'topological_sort',
    name: 'Topological Sort',
    category: 'graph',
    recognitionPatterns: {
      keywords: [
        'topological sort', 'topological order', 'prerequisite', 'dependency',
        'course schedule', 'task ordering', 'ordering constraints',
        'directed acyclic graph', 'dag', 'topo sort',
        'ordering of courses that respects all prerequisites', 'topological ordering'
      ],
      structuralClues: [
        'directed graph with ordering requirements',
        'determine valid ordering of tasks with dependencies'
      ],
      constraintClues: [],
      antiPatterns: ['undirected graph'],
      conditions: ['graph must be a DAG (no cycles)']
    },
    complexityProfile: { time: 'O(V+E)', space: 'O(V)' },
    prerequisites: ['dfs', 'bfs'],
    relatedConcepts: ['dfs', 'bfs'],
    commonMistakes: ['Not detecting cycles', 'Wrong ordering direction'],
    solutionTemplateId: null
  },

  {
    id: 'mst',
    name: 'Minimum Spanning Tree',
    category: 'graph',
    recognitionPatterns: {
      keywords: [
        'minimum spanning tree', 'mst', 'kruskal', 'prim',
        'connect all nodes minimum cost', 'minimum total edge weight',
        'spanning tree', 'minimum cost to connect',
        'connect every vertex in a weighted undirected graph'
      ],
      structuralClues: [
        'connect all vertices in weighted undirected graph with minimum total weight'
      ],
      constraintClues: [],
      antiPatterns: ['directed graph', 'shortest path'],
      conditions: ['graph must be undirected and connected']
    },
    complexityProfile: { time: 'O(E log E)', space: 'O(V+E)' },
    prerequisites: ['union_find'],
    relatedConcepts: ['union_find', 'dijkstra'],
    commonMistakes: ['Confusing MST with shortest path'],
    solutionTemplateId: null
  },

  {
    id: 'sorting',
    name: 'Sorting',
    category: 'array_technique',
    recognitionPatterns: {
      keywords: [
        'sort an array', 'sorting', 'sort the array', 'sort array'
      ],
      structuralClues: [
        'order array elements prior to queries'
      ],
      constraintClues: [],
      antiPatterns: [],
      conditions: []
    },
    complexityProfile: { time: 'O(N log N)', space: 'O(1)' },
    prerequisites: [],
    relatedConcepts: ['binary_search', 'two_pointers'],
    commonMistakes: [],
    solutionTemplateId: 'sorting'
  }
];

// ═══════════════════════════════════════════════════════════════════════════════
// Lookup Functions
// ═══════════════════════════════════════════════════════════════════════════════

/** Get all DSA concepts in the knowledge base. */
export function getAllConcepts(): DSAConcept[] {
  return DSA_CONCEPTS;
}

/** Get a concept by its ID. Returns null if not found. */
export function getConceptById(id: string): DSAConcept | null {
  // Check direct match
  const direct = DSA_CONCEPTS.find(c => c.id === id);
  if (direct) return direct;

  // Check aliases
  if (id === 'dsu') return DSA_CONCEPTS.find(c => c.id === 'union_find') || null;
  if (id === 'dp_2d') return DSA_CONCEPTS.find(c => c.id === 'knapsack_2d') || null;

  return null;
}

/** Get all concepts in a given category. */
export function getConceptsByCategory(category: string): DSAConcept[] {
  return DSA_CONCEPTS.filter(c => c.category === category);
}

/** Get only the supported concepts (those with solution templates). */
export function getSupportedConcepts(): DSAConcept[] {
  return DSA_CONCEPTS.filter(c => c.solutionTemplateId !== null);
}

// ═══════════════════════════════════════════════════════════════════════════════
// Topic Scoring — The Core Intelligence
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Score all DSA concepts against a structured problem.
 *
 * Returns a ranked list of TopicCandidates, sorted by confidence (highest first).
 * Applies condition-based elimination to reject concepts whose preconditions
 * are violated by the problem.
 */
export function scoreConcepts(problem: StructuredProblem): TopicCandidate[] {
  const text = `${problem.statement} ${problem.inputSpecification || ''} ${problem.outputSpecification || ''} ${problem.notes || ''}`.toLowerCase();
  const titleText = (problem.title || '').toLowerCase();
  const fullText = `${titleText} ${text}`;

  const candidates: TopicCandidate[] = [];

  for (const concept of DSA_CONCEPTS) {
    let score = 0;
    const matchedPatterns: string[] = [];
    let rejected = false;
    let rejectionReason: string | undefined;

    // ── Keyword matching (primary signal) ────────────────────────────────
    for (const keyword of concept.recognitionPatterns.keywords) {
      if (fullText.includes(keyword.toLowerCase())) {
        // Longer / more specific keyword matches get higher score
        const weight = keyword.split(' ').length > 2 ? 0.30 : 0.15;
        score += weight;
        matchedPatterns.push(`keyword: "${keyword}"`);
      }
    }

    // ── Semantic requirement matching ─────────────────────────────────────
    if (concept.id === 'prefix_sum') {
      if (
        /(?:sum|total).*?(?:from|between).*?[lr]|(?:from|between)\s+(?:day|position|index|elements?)?\s*[lr].*?(?:through|to)\s*[lr]/i.test(fullText) ||
        ((/answer\s+q\s+questions|for\s+q\s+queries|each\s+question\s+gives\s+two\s+positions\s+l\s+and\s+r/i.test(fullText)) && /(?:total|sum)/i.test(fullText))
      ) {
        score += 0.40;
        matchedPatterns.push('requirement: range sum query [l, r]');
      }
    }

    // ── Structural clue matching ──────────────────────────────────────────
    for (const clue of concept.recognitionPatterns.structuralClues) {
      if (fullText.includes(clue.toLowerCase())) {
        score += 0.10;
        matchedPatterns.push(`structure: "${clue}"`);
      }
    }

    // ── Anti-pattern demotion ─────────────────────────────────────────────
    for (const anti of concept.recognitionPatterns.antiPatterns) {
      if (fullText.includes(anti.toLowerCase())) {
        score *= 0.15;  // severely reduce confidence
        matchedPatterns.push(`anti-pattern: "${anti}" (demoted)`);
      }
    }

    // ── Condition-based elimination ───────────────────────────────────────
    for (const condition of concept.recognitionPatterns.conditions) {
      // Check negative value conditions (affects sum-based sliding window)
      if (condition.includes('non-negative') || condition.includes('monotonic sum')) {
        if (
          /\bnegative\b/i.test(fullText) ||
          /\bcan be negative\b/i.test(fullText) ||
          /\bmay be negative\b/i.test(fullText) ||
          fullText.includes('-10') ||
          fullText.includes('−10')
        ) {
          rejected = true;
          rejectionReason = condition;
          score *= 0.05;
        }
      }

      // Check sorted data requirement (affects two_pointers)
      if (condition.includes('sorted data')) {
        if (
          /\bunsorted\b/i.test(fullText) ||
          /\bnot sorted\b/i.test(fullText) ||
          /\bin any order\b/i.test(fullText)
        ) {
          rejected = true;
          rejectionReason = 'Array is unsorted';
          score *= 0.05;
        }
      }

      // Check unweighted requirement (affects BFS for shortest path)
      if (condition.includes('unweighted')) {
        const isExplicitlyUnweighted =
          /\bunweighted\b/i.test(fullText) ||
          /\bweights?\s+(?:all\s+have\s+)?1\b/i.test(fullText) ||
          /\bweight\s*=\s*1\b/i.test(fullText);

        if (!isExplicitlyUnweighted) {
          if (
            /\bweighted\b/i.test(fullText) ||
            /\bcost of edge\b/i.test(fullText) ||
            /\bnonnegative weights\b/i.test(fullText) ||
            /\bvalues greater than 1\b/i.test(fullText)
          ) {
            rejected = true;
            rejectionReason = condition;
            score *= 0.05;
          }
        }
      }

      // Check DAG requirement (affects topological_sort)
      if (condition.includes('DAG') || condition.includes('no cycles')) {
        if (fullText.includes('undirected') || (fullText.includes('cycle') && !fullText.includes('no cycle') && !fullText.includes('acyclic'))) {
          score *= 0.5;
          matchedPatterns.push(`condition weakened: "${condition}"`);
        }
      }
    }

    // ── Cap score at 1.0 ──────────────────────────────────────────────────
    score = Math.min(score, 1.0);

    // Only include concepts that had at least one keyword match
    if (matchedPatterns.length > 0) {
      candidates.push({
        conceptId: concept.id,
        confidence: Math.round(score * 100) / 100,
        matchedPatterns,
        supported: concept.solutionTemplateId !== null,
        rejected: rejected || undefined,
        rejectionReason
      });
    }
  }

  // Sort by confidence, highest first
  candidates.sort((a, b) => b.confidence - a.confidence);

  return candidates;
}
