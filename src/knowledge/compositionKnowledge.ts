/**
 * CHUP V2 — Composition Knowledge Layer.
 *
 * Encodes formal algorithmic concepts with:
 * - What operations they satisfy (\`satisfies: RequiredOperation[]\`)
 * - What preconditions they require (\`requires: string[]\`)
 * - What state transformations they produce (\`produces: string[]\`)
 * - State hierarchy / satisfaction relations (\`sorted_sequence IS-A sequence\`)
 *
 * This enables the composition engine to reason via state transitions:
 * sequence → sorting → sorted_sequence → prefix_sum → prefix_sum_sequence → range_sum
 * rather than maintaining an ad-hoc list of hardcoded pairwise combinations.
 */

import { AlgorithmConcept, KnowledgeConcept, RequiredOperation } from '../models/problemSpec';
import { STL_CONCEPTS } from './stlKnowledge';

// ═══════════════════════════════════════════════════════════════════════════════
// State Hierarchy (IS-A Relations) — Semantic Program Data States
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * State taxonomy defining semantic IS-A relations.
 * Represents what is currently true about the program data, completely
 * decoupled from which C++ type or class produced it.
 *
 * e.g. 'unique_sorted_sequence' IS-A 'sorted_sequence' IS-A 'sequence'.
 * When a concept requires 'sequence', an available 'sorted_sequence' satisfies it.
 */
const STATE_IS_A: Record<string, string[]> = {
  'unique_sorted_sequence': ['sorted_sequence', 'unique_sequence', 'sequence'],
  'sorted_sequence': ['sequence'],
  'unique_sequence': ['sequence'],
  'sorted_intervals': ['intervals', 'sequence'],
  'intervals': ['sequence'],
  'ordered_frequency_state': ['frequency_map', 'sequence'],
  'frequency_map': ['sequence'],
  'priority_ordered_state': ['sequence'],
  'max_heap_state': ['priority_ordered_state', 'sequence'],
  'min_heap_state': ['priority_ordered_state', 'sequence'],
  'lifo_state': ['sequence'],
  'fifo_state': ['sequence'],
  'position_result': ['query_results'],
  'grid': ['graph_unweighted'],
  'tree_state': ['graph_unweighted'],
  'trie_state': ['string_collection', 'sequence'],
  'lru_cache_state': ['cache_state', 'sequence'],
  'lfu_cache_state': ['cache_state', 'sequence'],
  'monotonic_stack_state': ['lifo_state', 'sequence']
};

/**
 * Checks if an available state satisfies a required state according to the state taxonomy.
 */
export function stateSatisfies(availableState: string, requiredState: string, visited: Set<string> = new Set()): boolean {
  if (availableState === requiredState) {
    return true;
  }
  if (visited.has(availableState)) {
    return false;
  }
  visited.add(availableState);

  const parents = STATE_IS_A[availableState];
  if (!parents) {
    return false;
  }
  if (parents.includes(requiredState)) {
    return true;
  }
  // Check transitively
  return parents.some(p => stateSatisfies(p, requiredState, visited));
}

/**
 * Checks if a collection of available states satisfies all required states of a concept.
 */
export function canSatisfyPreconditions(availableStates: Set<string>, requiredStates: string[]): boolean {
  return requiredStates.every(req => {
    for (const avail of availableStates) {
      if (stateSatisfies(avail, req)) {
        return true;
      }
    }
    return false;
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// Formal Algorithm Concepts
// ═══════════════════════════════════════════════════════════════════════════════

export const ALGORITHM_CONCEPTS: AlgorithmConcept[] = [
  {
    id: 'sorting',
    name: 'Array Sorting',
    category: 'algorithm',
    properties: ['comparison_sort', 'order_elements'],
    satisfies: ['sorting', 'sorted_order'],
    requires: ['sequence'],
    produces: ['sorted_sequence'],
    dataStructures: ['sequence_static', 'sequence_dynamic', 'intervals'],
    templateId: 'sorting'
  },
  {
    id: 'prefix_sum',
    name: 'Prefix Sum',
    category: 'technique',
    properties: ['cumulative_aggregation', 'range_query_o1'],
    satisfies: ['range_sum', 'subarray_target_sum'],
    requires: ['sequence'],  // Satisfied by sequence, sorted_sequence, etc. via IS-A
    produces: ['prefix_sum_sequence'],
    dataStructures: ['sequence_static'],
    templateId: 'prefixSum'
  },
  {
    id: 'two_pointers',
    name: 'Two Pointers',
    category: 'technique',
    properties: ['converging_indices', 'linear_scan_sorted'],
    satisfies: ['pair_sum', 'pair_sum_positions'],
    requires: ['sorted_sequence'],
    produces: ['pair_result'],
    dataStructures: ['sequence_static', 'sequence_dynamic'],
    templateId: 'twoPointers'
  },
  {
    id: 'binary_search',
    name: 'Binary Search',
    category: 'algorithm',
    properties: ['logarithmic_lookup', 'sorted_domain'],
    satisfies: ['element_lookup', 'threshold_search'],
    requires: ['sorted_sequence'],
    produces: ['query_results'],
    dataStructures: ['sequence_static'],
    templateId: 'binarySearch'
  },
  {
    id: 'sort_greedy',
    name: 'Sorting + Greedy Scheduling',
    category: 'technique',
    properties: ['interval_selection', 'earliest_end_time'],
    satisfies: ['interval_schedule'],
    requires: ['sorted_intervals'],
    produces: ['scheduled_tasks'],
    dataStructures: ['intervals'],
    templateId: 'sortGreedy'
  },
  {
    id: 'frequency_count',
    name: 'Frequency Counting / Hash Map',
    category: 'technique',
    properties: ['occurrence_tracking', 'element_multiplicity'],
    satisfies: ['frequency_count'],
    requires: ['sequence'],
    produces: ['frequency_state', 'frequency_map'],
    dataStructures: ['sequence_static', 'sequence_dynamic'],
    templateId: 'frequencyCount'
  },
  {
    id: 'filter_count',
    name: 'Frequency Filter',
    category: 'algorithm',
    properties: ['threshold_filtering', 'occurrence_filter'],
    satisfies: ['filter_count'],
    requires: ['frequency_map'],
    produces: ['filtered_results'],
    dataStructures: ['sequence_static', 'sequence_dynamic'],
    templateId: 'frequencyCount'
  },
  {
    id: 'bfs',
    name: 'Breadth-First Search',
    category: 'algorithm',
    properties: ['queue_traversal', 'level_order', 'unweighted_shortest_path'],
    satisfies: ['shortest_path', 'connectivity'],
    requires: ['graph_unweighted'],  // Satisfied by grid via grid IS-A graph_unweighted
    produces: ['shortest_distances', 'components'],
    dataStructures: ['graph_unweighted', 'grid'],
    templateId: 'bfs'
  },
  {
    id: 'dfs',
    name: 'Depth-First Search',
    category: 'algorithm',
    properties: ['recursive_traversal', 'component_exploration'],
    satisfies: ['connectivity'],
    requires: ['graph_unweighted'],
    produces: ['components'],
    dataStructures: ['graph_unweighted', 'grid'],
    templateId: 'dfs'
  },
  {
    id: 'dp_1d',
    name: '1D Dynamic Programming',
    category: 'technique',
    properties: ['optimal_substructure', 'memoization'],
    satisfies: ['recurrence_1d'],
    requires: ['sequence'],
    produces: ['dp_table'],
    dataStructures: ['sequence_static'],
    templateId: 'dp1d'
  },
  {
    id: 'monotonic_stack',
    name: 'Monotonic Stack (Dominance Elimination)',
    category: 'technique',
    properties: ['monotonic_stack', 'dominance_elimination', 'nearest_bound'],
    satisfies: ['nearest_smaller_values', 'monotonic_stack', 'histogram', 'next_greater', 'daily_temperatures', 'stock_span'],
    requires: ['sequence'],
    produces: ['monotonic_stack_state', 'query_results'],
    dataStructures: ['sequence_static', 'sequence_dynamic'],
    templateId: 'monotonicStack'
  },
  {
    id: 'trie',
    name: 'Trie / Prefix Tree',
    category: 'algorithm',
    properties: ['prefix_tree', 'shared_prefix_state', 'character_transitions'],
    satisfies: ['prefix_tree', 'trie_prefix_search'],
    requires: ['sequence'],
    produces: ['trie_state', 'query_results'],
    dataStructures: ['sequence_static', 'sequence_dynamic'],
    templateId: 'trie'
  },
  {
    id: 'lru_cache',
    name: 'LRU Cache (Least Recently Used)',
    category: 'algorithm',
    properties: ['lru_eviction', 'doubly_linked_list', 'hash_map_composition'],
    satisfies: ['lru_cache', 'key_value_mapping'],
    requires: ['sequence'],
    produces: ['lru_cache_state'],
    dataStructures: ['sequence_dynamic'],
    templateId: 'lruCache'
  },
  {
    id: 'lfu_cache',
    name: 'LFU Cache (Least Frequently Used)',
    category: 'algorithm',
    properties: ['lfu_eviction', 'frequency_lists', 'recency_tie_breaking'],
    satisfies: ['lfu_cache', 'key_value_mapping'],
    requires: ['sequence'],
    produces: ['lfu_cache_state'],
    dataStructures: ['sequence_dynamic'],
    templateId: 'lfuCache'
  },
  {
    id: 'tree_dp',
    name: 'Tree Dynamic Programming',
    category: 'technique',
    properties: ['tree_recurrence', 'post_order_dfs', 'hierarchical_substructure'],
    satisfies: ['tree_dp'],
    requires: ['tree_state'],
    produces: ['query_results'],
    dataStructures: ['graph_unweighted'],
    templateId: 'treeDp'
  }
];

// ═══════════════════════════════════════════════════════════════════════════════
// Unified Concept Lookups
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Returns all unified concepts across algorithms and STL knowledge.
 */
export function getAllUnifiedConcepts(): KnowledgeConcept[] {
  return [...ALGORITHM_CONCEPTS, ...STL_CONCEPTS];
}

export function getAlgorithmConcept(id: string): KnowledgeConcept | null {
  return getAllUnifiedConcepts().find(c => c.id === id) || null;
}

export function getConceptsSatisfying(operation: RequiredOperation): KnowledgeConcept[] {
  return getAllUnifiedConcepts().filter(c => c.satisfies.includes(operation));
}

