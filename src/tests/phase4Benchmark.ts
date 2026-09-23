/**
 * CHUP / Offcode — Phase 4 Capability Routing Held-Out Benchmark
 *
 * 105 Genuinely Held-Out Requests evaluating:
 *   - Category A: Data Structures (SLL, DLL, CLL, Stack, Queue, BST, Trees) [20 cases]
 *   - Category B: Graph Algorithms (Dijkstra, SSSP, BFS, DFS, Traversal) [18 cases]
 *   - Category C: Numerical Methods (LU, Gauss, Bisection, Newton-Raphson) [14 cases]
 *   - Category D: CP Core Techniques (Prefix Sum, Two Pointers, Binary Search, Monotonic, Trie) [20 cases]
 *   - Category E: Lexical Variations & Misspellings [10 cases]
 *   - Category F: Ambiguity Resolution [8 cases]
 *   - Category G: Conflict Detection & Invariant Guards [7 cases]
 *   - Category H: Unsupported & Domain Boundary Fail-Closed [8 cases]
 *
 * Total: 105 cases. All verified offline and deterministically.
 */

import * as assert from 'assert';
import { UNIVERSAL_ROUTER } from '../pipeline/universalRouter';
import { CapabilityPlan, CapabilityRequestStatus, CapabilityFailureCode } from '../models/capabilityModel';
import { CAPABILITY_SOLVER_REGISTRY } from '../solver/capabilitySolverRegistry';

export interface BenchmarkCase {
  id: string;
  category: string;
  prompt: string;
  expectedStatus: CapabilityRequestStatus;
  expectedCapability?: string;
  expectedAlgorithm?: string;
  expectedFailureCode?: CapabilityFailureCode;
  expectedComponents?: string[];
  expectedMechanism?: string;
  checkCodeGeneration?: boolean;
}

export const HELD_OUT_BENCHMARK_CASES: BenchmarkCase[] = [
  // ── Category A: Data Structures (20 cases) ──────────────────────────────────
  {
    id: 'DS-01',
    category: 'Data Structures',
    prompt: 'insert a node at the end of a singly linked list',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'singly_linked_list',
    expectedAlgorithm: 'singly_linked_list_standard',
    expectedMechanism: 'pointer_based_sll',
    checkCodeGeneration: true
  },
  {
    id: 'DS-02',
    category: 'Data Structures',
    prompt: 'insert a node at the front of a singly linked list',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'singly_linked_list',
    expectedAlgorithm: 'singly_linked_list_standard',
    expectedMechanism: 'pointer_based_sll',
    checkCodeGeneration: true
  },
  {
    id: 'DS-03',
    category: 'Data Structures',
    prompt: 'delete the head node of a singly linked list',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'singly_linked_list',
    expectedMechanism: 'pointer_based_sll',
    checkCodeGeneration: true
  },
  {
    id: 'DS-04',
    category: 'Data Structures',
    prompt: 'delete a node at the end of a singly linked list',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'singly_linked_list',
    expectedMechanism: 'pointer_based_sll',
    checkCodeGeneration: true
  },
  {
    id: 'DS-05',
    category: 'Data Structures',
    prompt: 'reverse a singly linked list in place',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'singly_linked_list',
    expectedMechanism: 'pointer_based_sll',
    checkCodeGeneration: true
  },
  {
    id: 'DS-06',
    category: 'Data Structures',
    prompt: 'search for a key in a singly linked list',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'singly_linked_list',
    expectedMechanism: 'pointer_based_sll',
    checkCodeGeneration: true
  },
  {
    id: 'DS-07',
    category: 'Data Structures',
    prompt: 'insert node at beginning of doubly linked list',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'doubly_linked_list',
    expectedMechanism: 'pointer_based_dll',
    checkCodeGeneration: true
  },
  {
    id: 'DS-08',
    category: 'Data Structures',
    prompt: 'insert node at tail of doubly linked list',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'doubly_linked_list',
    expectedMechanism: 'pointer_based_dll',
    checkCodeGeneration: true
  },
  {
    id: 'DS-09',
    category: 'Data Structures',
    prompt: 'delete node from doubly linked list',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'doubly_linked_list',
    expectedMechanism: 'pointer_based_dll',
    checkCodeGeneration: true
  },
  {
    id: 'DS-10',
    category: 'Data Structures',
    prompt: 'insert node into circular linked list',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'circular_linked_list',
    expectedMechanism: 'pointer_based_cll',
    checkCodeGeneration: true
  },
  {
    id: 'DS-11',
    category: 'Data Structures',
    prompt: 'delete node from circular linked list',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'circular_linked_list',
    expectedMechanism: 'pointer_based_cll',
    checkCodeGeneration: true
  },
  {
    id: 'DS-12',
    category: 'Data Structures',
    prompt: 'implement stack push and pop operations',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'stack',
    checkCodeGeneration: true
  },
  {
    id: 'DS-13',
    category: 'Data Structures',
    prompt: 'check balanced parentheses using stack',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'stack',
    checkCodeGeneration: true
  },
  {
    id: 'DS-14',
    category: 'Data Structures',
    prompt: 'implement queue enqueue and dequeue operations',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'queue',
    checkCodeGeneration: true
  },
  {
    id: 'DS-15',
    category: 'Data Structures',
    prompt: 'insert value into binary search tree',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'binary_search_tree',
    checkCodeGeneration: true
  },
  {
    id: 'DS-16',
    category: 'Data Structures',
    prompt: 'search for value in binary search tree',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'binary_search_tree',
    checkCodeGeneration: true
  },
  {
    id: 'DS-17',
    category: 'Data Structures',
    prompt: 'inorder traversal of binary tree',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'binary_tree',
    checkCodeGeneration: true
  },
  {
    id: 'DS-18',
    category: 'Data Structures',
    prompt: 'preorder traversal of binary tree',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'binary_tree',
    checkCodeGeneration: true
  },
  {
    id: 'DS-19',
    category: 'Data Structures',
    prompt: 'postorder traversal of binary tree',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'binary_tree',
    checkCodeGeneration: true
  },
  {
    id: 'DS-20',
    category: 'Data Structures',
    prompt: 'find height of a binary tree',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'binary_tree',
    checkCodeGeneration: true
  },

  // ── Category B: Graph Algorithms (18 cases) ─────────────────────────────────
  {
    id: 'GR-01',
    category: 'Graph Algorithms',
    prompt: 'find shortest path using Dijkstra algorithm',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'single_source_shortest_path',
    expectedAlgorithm: 'dijkstra',
    expectedMechanism: 'binary_heap_std',
    expectedComponents: ['priority_queue', 'edge_relaxation'],
    checkCodeGeneration: true
  },
  {
    id: 'GR-02',
    category: 'Graph Algorithms',
    prompt: 'single source shortest path with non-negative edge weights using dijkstra',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'single_source_shortest_path',
    expectedAlgorithm: 'dijkstra',
    checkCodeGeneration: true
  },
  {
    id: 'GR-03',
    category: 'Graph Algorithms',
    prompt: 'compute shortest path from source vertex to all vertices using dijkstra',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'single_source_shortest_path',
    expectedAlgorithm: 'dijkstra',
    checkCodeGeneration: true
  },
  {
    id: 'GR-04',
    category: 'Graph Algorithms',
    prompt: 'shortest path in unweighted graph using breadth first search bfs',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'single_source_shortest_path',
    expectedAlgorithm: 'bfs_shortest_path',
    checkCodeGeneration: true
  },
  {
    id: 'GR-05',
    category: 'Graph Algorithms',
    prompt: 'breadth first search traversal on directed graph',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'graph_traversal',
    expectedAlgorithm: 'graph_bfs'
  },
  {
    id: 'GR-06',
    category: 'Graph Algorithms',
    prompt: 'depth first search traversal on undirected graph',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'graph_traversal',
    expectedAlgorithm: 'graph_dfs'
  },
  {
    id: 'GR-07',
    category: 'Graph Algorithms',
    prompt: 'topological sort of directed acyclic graph using kahn bfs',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'topological_sort',
    expectedAlgorithm: 'kahn_algorithm'
  },
  {
    id: 'GR-08',
    category: 'Graph Algorithms',
    prompt: 'topological sort using dfs postorder reverse',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'topological_sort',
    expectedAlgorithm: 'dfs_topological_sort'
  },
  {
    id: 'GR-09',
    category: 'Graph Algorithms',
    prompt: 'minimum spanning tree using kruskal algorithm with disjoint set union',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'minimum_spanning_tree',
    expectedAlgorithm: 'kruskal'
  },
  {
    id: 'GR-10',
    category: 'Graph Algorithms',
    prompt: 'minimum spanning tree using prim algorithm with priority queue',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'minimum_spanning_tree',
    expectedAlgorithm: 'prim'
  },
  {
    id: 'GR-11',
    category: 'Graph Algorithms',
    prompt: 'connected components in undirected graph using bfs',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'connected_components',
    expectedAlgorithm: 'bfs_connected_components'
  },
  {
    id: 'GR-12',
    category: 'Graph Algorithms',
    prompt: 'connected components using disjoint set union dsu',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'connected_components',
    expectedAlgorithm: 'dsu_connected_components'
  },
  {
    id: 'GR-13',
    category: 'Graph Algorithms',
    prompt: 'detect cycle in directed graph using dfs recursion stack',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'GR-14',
    category: 'Graph Algorithms',
    prompt: 'detect cycle in undirected graph using dsu union find',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'GR-15',
    category: 'Graph Algorithms',
    prompt: 'bipartite graph check using two coloring bfs',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'GR-16',
    category: 'Graph Algorithms',
    prompt: 'single source shortest path with negative edges using bellman ford',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'single_source_shortest_path',
    expectedAlgorithm: 'bellman_ford'
  },
  {
    id: 'GR-17',
    category: 'Graph Algorithms',
    prompt: 'all pairs shortest path using floyd warshall dynamic programming',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'GR-18',
    category: 'Graph Algorithms',
    prompt: 'bridges in graph using tarjan low link algorithm',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },

  // ── Category C: Numerical Methods (14 cases) ────────────────────────────────
  {
    id: 'NM-01',
    category: 'Numerical Methods',
    prompt: 'solve system of linear equations using LU decomposition',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'lu_decomposition',
    expectedAlgorithm: 'doolittle_lu',
    expectedMechanism: 'dense_matrix_vector',
    expectedComponents: ['forward_substitution', 'back_substitution'],
    checkCodeGeneration: true
  },
  {
    id: 'NM-02',
    category: 'Numerical Methods',
    prompt: 'LU decomposition of square matrix using Doolittle method',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'lu_decomposition',
    expectedAlgorithm: 'doolittle_lu',
    checkCodeGeneration: true
  },
  {
    id: 'NM-03',
    category: 'Numerical Methods',
    prompt: 'solve linear system using Gaussian elimination with back substitution',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'gauss_elimination',
    expectedAlgorithm: 'gauss_elimination_pivoting',
    checkCodeGeneration: true
  },
  {
    id: 'NM-04',
    category: 'Numerical Methods',
    prompt: 'Gaussian elimination with partial pivoting for system of equations',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'gauss_elimination',
    expectedAlgorithm: 'gauss_elimination_pivoting',
    checkCodeGeneration: true
  },
  {
    id: 'NM-05',
    category: 'Numerical Methods',
    prompt: 'find root of continuous function using bisection method',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'root_finding',
    expectedAlgorithm: 'bisection',
    checkCodeGeneration: true
  },
  {
    id: 'NM-06',
    category: 'Numerical Methods',
    prompt: 'root finding using Newton-Raphson method with derivative',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'root_finding',
    expectedAlgorithm: 'newton_raphson',
    checkCodeGeneration: true
  },
  {
    id: 'NM-07',
    category: 'Numerical Methods',
    prompt: 'solve nonlinear equation f(x) = 0 using secant method',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'root_finding',
    expectedAlgorithm: 'secant'
  },
  {
    id: 'NM-08',
    category: 'Numerical Methods',
    prompt: 'numerical integration using Simpson 1/3 rule',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'NM-09',
    category: 'Numerical Methods',
    prompt: 'numerical integration using composite trapezoidal rule',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'NM-10',
    category: 'Numerical Methods',
    prompt: 'polynomial interpolation using Lagrange interpolating polynomial',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'NM-11',
    category: 'Numerical Methods',
    prompt: 'Newton forward divided difference interpolation',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'NM-12',
    category: 'Numerical Methods',
    prompt: 'solve ordinary differential equation using 4th order Runge Kutta rk4',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'NM-13',
    category: 'Numerical Methods',
    prompt: 'matrix inversion using Gauss-Jordan elimination',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'NM-14',
    category: 'Numerical Methods',
    prompt: 'find eigenvalue of matrix using power iteration method',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },

  // ── Category D: CP Core Techniques (20 cases) ───────────────────────────────
  {
    id: 'CP-01',
    category: 'Competitive Programming',
    prompt: 'compute prefix sum array for 1D static range sum queries',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'prefix_sum',
    expectedAlgorithm: 'prefix_sum_standard',
    checkCodeGeneration: true
  },
  {
    id: 'CP-02',
    category: 'Competitive Programming',
    prompt: '2D prefix sum table for 2D submatrix sum queries',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'prefix_sum',
    expectedAlgorithm: 'prefix_sum_standard',
    checkCodeGeneration: true
  },
  {
    id: 'CP-03',
    category: 'Competitive Programming',
    prompt: 'two sum in sorted array using two pointers from opposite ends',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'two_pointers',
    expectedAlgorithm: 'two_pointers_standard',
    checkCodeGeneration: true
  },
  {
    id: 'CP-04',
    category: 'Competitive Programming',
    prompt: 'longest subarray with sum at most k using sliding window two pointers',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'two_pointers',
    expectedAlgorithm: 'two_pointers_standard',
    checkCodeGeneration: true
  },
  {
    id: 'CP-05',
    category: 'Competitive Programming',
    prompt: 'binary search for target element in sorted array',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'binary_search',
    expectedAlgorithm: 'binary_search_standard',
    checkCodeGeneration: true
  },
  {
    id: 'CP-06',
    category: 'Competitive Programming',
    prompt: 'find first index >= x using binary search lower bound',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'binary_search',
    expectedAlgorithm: 'binary_search_standard',
    checkCodeGeneration: true
  },
  {
    id: 'CP-07',
    category: 'Competitive Programming',
    prompt: 'find next greater element using monotonic stack',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'monotonic_stack',
    expectedAlgorithm: 'monotonic_stack_standard'
  },
  {
    id: 'CP-08',
    category: 'Competitive Programming',
    prompt: 'sliding window maximum using monotonic deque',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'CP-09',
    category: 'Competitive Programming',
    prompt: 'disjoint set union with path compression and union by rank',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'CP-10',
    category: 'Competitive Programming',
    prompt: 'prefix tree trie insert and search words',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'trie',
    expectedAlgorithm: 'trie_standard'
  },
  {
    id: 'CP-11',
    category: 'Competitive Programming',
    prompt: 'binary indexed tree fenwick tree for point update range sum',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'CP-12',
    category: 'Competitive Programming',
    prompt: 'segment tree for range minimum query with point updates',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'CP-13',
    category: 'Competitive Programming',
    prompt: 'segment tree with lazy propagation for range add and range sum',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'CP-14',
    category: 'Competitive Programming',
    prompt: 'sieve of eratosthenes to generate prime numbers up to n',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'CP-15',
    category: 'Competitive Programming',
    prompt: 'fast modular exponentiation binary exponentiation',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'CP-16',
    category: 'Competitive Programming',
    prompt: 'extended euclidean algorithm for modular inverse gcd',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'CP-17',
    category: 'Competitive Programming',
    prompt: 'maximum subarray sum using Kadane algorithm',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'CP-18',
    category: 'Competitive Programming',
    prompt: 'longest increasing subsequence in O(N log N) using binary search',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'CP-19',
    category: 'Competitive Programming',
    prompt: '0/1 knapsack problem with dynamic programming table',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'CP-20',
    category: 'Competitive Programming',
    prompt: 'matrix exponentiation to calculate nth Fibonacci number',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },

  // ── Category E: Lexical Variations & Misspellings (10 cases) ────────────────
  {
    id: 'LEX-01',
    category: 'Lexical Variations',
    prompt: 'lincked list insert at end',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'singly_linked_list'
  },
  {
    id: 'LEX-02',
    category: 'Lexical Variations',
    prompt: 'impliment singly linked list delete head',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'singly_linked_list'
  },
  {
    id: 'LEX-03',
    category: 'Lexical Variations',
    prompt: 'dijktra shortest path algorithm',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'single_source_shortest_path',
    expectedAlgorithm: 'dijkstra'
  },
  {
    id: 'LEX-04',
    category: 'Lexical Variations',
    prompt: 'lu dcomposition solver',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'lu_decomposition'
  },
  {
    id: 'LEX-05',
    category: 'Lexical Variations',
    prompt: 'gaus elimination linear equations',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'gauss_elimination'
  },
  {
    id: 'LEX-06',
    category: 'Lexical Variations',
    prompt: 'binnary serch for lower bound',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'binary_search'
  },
  {
    id: 'LEX-07',
    category: 'Lexical Variations',
    prompt: 'prifix sum array range query',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'prefix_sum'
  },
  {
    id: 'LEX-08',
    category: 'Lexical Variations',
    prompt: 'topollogical sort directed graph',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'topological_sort'
  },
  {
    id: 'LEX-09',
    category: 'Lexical Variations',
    prompt: 'krushkal minimum spanning tree',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'minimum_spanning_tree'
  },
  {
    id: 'LEX-10',
    category: 'Lexical Variations',
    prompt: 'bissection root finder',
    expectedStatus: 'CAPABILITY_RESOLVED',
    expectedCapability: 'root_finding'
  },

  // ── Category F: Ambiguity Resolution (8 cases) ──────────────────────────────
  {
    id: 'AMB-01',
    category: 'Ambiguity Handling',
    prompt: 'find shortest path',
    expectedStatus: 'CAPABILITY_AMBIGUOUS',
    expectedFailureCode: 'CAPABILITY_AMBIGUOUS'
  },
  {
    id: 'AMB-02',
    category: 'Ambiguity Handling',
    prompt: 'search for value',
    expectedStatus: 'CAPABILITY_AMBIGUOUS',
    expectedFailureCode: 'CAPABILITY_AMBIGUOUS'
  },
  {
    id: 'AMB-03',
    category: 'Ambiguity Handling',
    prompt: 'sort elements',
    expectedStatus: 'CAPABILITY_AMBIGUOUS',
    expectedFailureCode: 'CAPABILITY_AMBIGUOUS'
  },
  {
    id: 'AMB-04',
    category: 'Ambiguity Handling',
    prompt: 'traverse graph nodes',
    expectedStatus: 'CAPABILITY_AMBIGUOUS',
    expectedFailureCode: 'CAPABILITY_AMBIGUOUS'
  },
  {
    id: 'AMB-05',
    category: 'Ambiguity Handling',
    prompt: 'find optimal spanning tree',
    expectedStatus: 'CAPABILITY_AMBIGUOUS',
    expectedFailureCode: 'CAPABILITY_AMBIGUOUS'
  },
  {
    id: 'AMB-06',
    category: 'Ambiguity Handling',
    prompt: 'find cycle in graph',
    expectedStatus: 'CAPABILITY_AMBIGUOUS',
    expectedFailureCode: 'CAPABILITY_AMBIGUOUS'
  },
  {
    id: 'AMB-07',
    category: 'Ambiguity Handling',
    prompt: 'evaluate root of function',
    expectedStatus: 'CAPABILITY_AMBIGUOUS',
    expectedFailureCode: 'CAPABILITY_AMBIGUOUS'
  },
  {
    id: 'AMB-08',
    category: 'Ambiguity Handling',
    prompt: 'query range in array',
    expectedStatus: 'CAPABILITY_AMBIGUOUS',
    expectedFailureCode: 'CAPABILITY_AMBIGUOUS'
  },

  // ── Category G: Conflict Detection & Invariant Guards (7 cases) ─────────────
  {
    id: 'CONF-01',
    category: 'Conflict Detection',
    prompt: 'Dijkstra shortest path with negative edge weights',
    expectedStatus: 'CAPABILITY_CONFLICT',
    expectedFailureCode: 'CAPABILITY_CONFLICT'
  },
  {
    id: 'CONF-02',
    category: 'Conflict Detection',
    prompt: 'single source shortest path using dijkstra on graph with negative cycle',
    expectedStatus: 'CAPABILITY_CONFLICT',
    expectedFailureCode: 'CAPABILITY_CONFLICT'
  },
  {
    id: 'CONF-03',
    category: 'Conflict Detection',
    prompt: 'topological sort on cyclic directed graph',
    expectedStatus: 'CAPABILITY_CONFLICT',
    expectedFailureCode: 'CAPABILITY_CONFLICT'
  },
  {
    id: 'CONF-04',
    category: 'Conflict Detection',
    prompt: 'binary search on unsorted unordered arbitrary array',
    expectedStatus: 'CAPABILITY_CONFLICT',
    expectedFailureCode: 'CAPABILITY_CONFLICT'
  },
  {
    id: 'CONF-05',
    category: 'Conflict Detection',
    prompt: 'bisection method on function where f(a) and f(b) have the same sign',
    expectedStatus: 'CAPABILITY_CONFLICT',
    expectedFailureCode: 'CAPABILITY_CONFLICT'
  },
  {
    id: 'CONF-06',
    category: 'Conflict Detection',
    prompt: 'stack with first in first out fifo order',
    expectedStatus: 'CAPABILITY_CONFLICT',
    expectedFailureCode: 'CAPABILITY_CONFLICT'
  },
  {
    id: 'CONF-07',
    category: 'Conflict Detection',
    prompt: 'queue with last in first out lifo order',
    expectedStatus: 'CAPABILITY_CONFLICT',
    expectedFailureCode: 'CAPABILITY_CONFLICT'
  },

  // ── Category H: Unsupported & Domain Boundary Fail-Closed (8 cases) ────────
  {
    id: 'UNS-01',
    category: 'Unsupported / Fail-Closed',
    prompt: 'quantum fourier transform algorithm for quantum computing',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'UNS-02',
    category: 'Unsupported / Fail-Closed',
    prompt: 'traveling salesman problem using simulated annealing heuristic',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'UNS-03',
    category: 'Unsupported / Fail-Closed',
    prompt: 'train deep convolutional neural network for image recognition',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'UNS-04',
    category: 'Unsupported / Fail-Closed',
    prompt: 'solve mixed integer linear programming using branch and bound simplex',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'UNS-05',
    category: 'Unsupported / Fail-Closed',
    prompt: 'blockchain proof of work consensus mechanism with cryptographic hash',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'UNS-06',
    category: 'Unsupported / Fail-Closed',
    prompt: 'reinforcement learning proximal policy optimization ppo agent',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'UNS-07',
    category: 'Unsupported / Fail-Closed',
    prompt: 'genetic algorithm with crossover and mutation for scheduling',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  },
  {
    id: 'UNS-08',
    category: 'Unsupported / Fail-Closed',
    prompt: 'arbitrary unsupported magic spell request that does not exist',
    expectedStatus: 'CAPABILITY_UNSUPPORTED',
    expectedFailureCode: 'CAPABILITY_UNSUPPORTED'
  }
];

export interface BenchmarkScorecard {
  total: number;
  passed: number;
  failed: number;
  accuracyPercent: number;
  categoryBreakdown: Record<string, { total: number; passed: number; failed: number }>;
}

export async function runPhase4Benchmark(): Promise<BenchmarkScorecard> {
  console.log('\n===================================================================');
  console.log('       CHUP / Offcode Phase 4: Capability Routing Benchmark        ');
  console.log('       105 Genuinely Held-Out Capability Requests Evaluation       ');
  console.log('===================================================================\n');

  let passed = 0;
  let failed = 0;
  const breakdown: Record<string, { total: number; passed: number; failed: number }> = {};

  for (const bCase of HELD_OUT_BENCHMARK_CASES) {
    if (!breakdown[bCase.category]) {
      breakdown[bCase.category] = { total: 0, passed: 0, failed: 0 };
    }
    breakdown[bCase.category].total++;

    try {
      const plan = UNIVERSAL_ROUTER.createPlan(bCase.prompt);

      // 1. Status Match Check
      assert.strictEqual(
        plan.status,
        bCase.expectedStatus,
        `[${bCase.id}] Status mismatch: expected ${bCase.expectedStatus}, got ${plan.status}`
      );

      // 2. Resolved Capability Check
      if (bCase.expectedCapability) {
        assert.ok(
          plan.resolvedCapabilities.includes(bCase.expectedCapability),
          `[${bCase.id}] Capability mismatch: expected ${bCase.expectedCapability}, got ${plan.resolvedCapabilities.join(', ')}`
        );
      }

      // 3. Algorithm Dominance Check
      if (bCase.expectedAlgorithm) {
        assert.strictEqual(
          plan.primaryAlgorithm,
          bCase.expectedAlgorithm,
          `[${bCase.id}] Algorithm mismatch: expected ${bCase.expectedAlgorithm}, got ${plan.primaryAlgorithm}`
        );
      }

      // 4. Failure Code Check
      if (bCase.expectedFailureCode) {
        assert.strictEqual(
          plan.failureCode,
          bCase.expectedFailureCode,
          `[${bCase.id}] FailureCode mismatch: expected ${bCase.expectedFailureCode}, got ${plan.failureCode}`
        );
      }

      // 5. Component Check
      if (bCase.expectedComponents) {
        for (const reqComp of bCase.expectedComponents) {
          assert.ok(
            plan.requiredComponents.includes(reqComp),
            `[${bCase.id}] Missing required component: ${reqComp}`
          );
        }
      }

      // 6. Mechanism Check
      if (bCase.expectedMechanism) {
        assert.strictEqual(
          plan.selectedMechanism,
          bCase.expectedMechanism,
          `[${bCase.id}] Mechanism mismatch: expected ${bCase.expectedMechanism}, got ${plan.selectedMechanism}`
        );
      }

      // 7. Optional Code Generation Check
      if (bCase.checkCodeGeneration) {
        const solverResult = await CAPABILITY_SOLVER_REGISTRY.executePlan(plan);
        assert.ok(
          solverResult.success,
          `[${bCase.id}] Code generation failed: ${solverResult.limitationMessage || solverResult.reasoning}`
        );
        assert.ok(
          solverResult.code && solverResult.code.length > 50,
          `[${bCase.id}] Generated code is empty or insufficient`
        );
      }

      console.log(`  ✓ [${bCase.id}] ${bCase.category} — ${bCase.prompt.substring(0, 50)}...`);
      passed++;
      breakdown[bCase.category].passed++;
    } catch (err: any) {
      console.error(`  ✗ [${bCase.id}] ${bCase.category} — ${bCase.prompt}`);
      console.error(`    Error: ${err.message}`);
      failed++;
      breakdown[bCase.category].failed++;
    }
  }

  const total = HELD_OUT_BENCHMARK_CASES.length;
  const accuracyPercent = Math.round((passed / total) * 1000) / 10;

  console.log('\n===================================================================');
  console.log('                 PHASE 4 BENCHMARK SCORECARD                       ');
  console.log('===================================================================');
  console.log(
    `Overall: ${passed}/${total} passed (${accuracyPercent}% accuracy, ${failed} failed)`
  );
  console.log('-------------------------------------------------------------------');
  for (const [cat, score] of Object.entries(breakdown)) {
    const catPercent = Math.round((score.passed / score.total) * 1000) / 10;
    const padCat = (cat + ':').padEnd(30, ' ');
    console.log(`  ${padCat} ${score.passed}/${score.total} (${catPercent}%)`);
  }
  console.log('===================================================================\n');

  return {
    total,
    passed,
    failed,
    accuracyPercent,
    categoryBreakdown: breakdown
  };
}

// Standalone execution support
if (require.main === module) {
  runPhase4Benchmark().then(card => {
    if (card.failed > 0) {
      process.exit(1);
    }
  });
}
