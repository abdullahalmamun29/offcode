/**
 * CHUP / Hidden Link — Structured C++ STL Knowledge Layer.
 *
 * Formalizes the C++ Standard Template Library (STL) as structured knowledge:
 * - Concept identity, C++ representation, category
 * - Semantic properties and capabilities
 * - Requirements it can satisfy
 * - Preconditions (required semantic states)
 * - Effects (produced semantic states)
 * - Supported operations and asymptotic complexity (average vs worst-case)
 * - Necessary headers
 *
 * This knowledge integrates into candidate evaluation, constraint reasoning,
 * and state-transition composition without phrase-to-template hardcoding.
 */

import { KnowledgeConcept, RequiredOperation } from '../models/problemSpec';

export const STL_CONCEPTS: KnowledgeConcept[] = [
  // ─── Sequence Containers ───────────────────────────────────────────────────

  {
    id: 'vector',
    name: 'std::vector',
    category: 'container',
    cppType: 'std::vector',
    properties: ['dynamic_sequence', 'random_access', 'contiguous_storage', 'indexable'],
    satisfies: ['sequence_io', 'random_access', 'dynamic_array_operations'],
    requires: [],
    produces: ['sequence'],
    dataStructures: ['sequence_static', 'sequence_dynamic'],
    supportedOperations: [
      'push_back', 'pop_back', 'front', 'back', 'size', 'empty',
      'operator[]', 'at', 'insert', 'erase'
    ],
    complexity: {
      time: 'O(1)',
      space: 'O(N)',
      operations: {
        random_access: 'O(1)',
        push_back: 'amortized O(1)',
        pop_back: 'O(1)',
        insert_middle: 'O(N)',
        erase_middle: 'O(N)'
      }
    },
    headers: ['<vector>'],
    isSTL: true
  },

  {
    id: 'array',
    name: 'std::array',
    category: 'container',
    cppType: 'std::array',
    properties: ['fixed_size_sequence', 'random_access', 'contiguous_storage'],
    satisfies: ['random_access'],
    requires: [],
    produces: ['sequence'],
    dataStructures: ['sequence_static'],
    supportedOperations: ['size', 'front', 'back', 'operator[]', 'at'],
    complexity: {
      time: 'O(1)',
      space: 'O(N)',
      operations: {
        random_access: 'O(1)'
      }
    },
    headers: ['<array>'],
    isSTL: true
  },

  {
    id: 'deque',
    name: 'std::deque',
    category: 'container',
    cppType: 'std::deque',
    properties: ['double_ended_sequence', 'random_access'],
    satisfies: ['double_ended_access', 'random_access', 'deque_operations', 'reversible_deque'],
    requires: [],
    produces: ['sequence'],
    dataStructures: ['sequence_dynamic'],
    supportedOperations: [
      'push_front', 'push_back', 'pop_front', 'pop_back',
      'front', 'back', 'operator[]', 'size', 'empty'
    ],
    complexity: {
      time: 'O(1)',
      space: 'O(N)',
      operations: {
        push_front: 'O(1)',
        push_back: 'O(1)',
        pop_front: 'O(1)',
        pop_back: 'O(1)',
        random_access: 'O(1)'
      }
    },
    headers: ['<deque>'],
    isSTL: true
  },

  {
    id: 'list',
    name: 'std::list',
    category: 'container',
    cppType: 'std::list',
    properties: [
      'linked_sequence',
      'constant_time_insert_erase_with_iterator',
      'bidirectional_iteration'
    ],
    satisfies: ['dynamic_insertion', 'dynamic_deletion'],
    requires: [],
    produces: ['sequence'],
    dataStructures: ['sequence_dynamic'],
    supportedOperations: [
      'push_front', 'push_back', 'pop_front', 'pop_back',
      'insert', 'erase', 'front', 'back', 'size', 'empty'
    ],
    complexity: {
      time: 'O(1)',
      space: 'O(N)',
      operations: {
        insert: 'O(1)',
        erase: 'O(1)',
        push_front: 'O(1)',
        push_back: 'O(1)',
        random_access: 'unsupported'
      }
    },
    headers: ['<list>'],
    isSTL: true
  },

  // ─── Container Adapters ────────────────────────────────────────────────────

  {
    id: 'stack',
    name: 'std::stack',
    category: 'adapter',
    cppType: 'std::stack',
    properties: ['lifo', 'top_access'],
    satisfies: [
      'lifo',
      'nearest_smaller_values',
      'monotonic_stack',
      'balanced_brackets',
      'bracket_sequence_min_cost'
    ],
    requires: ['sequence'],
    produces: ['lifo_state'],
    dataStructures: ['sequence_dynamic'],
    supportedOperations: ['push', 'pop', 'top', 'empty', 'size'],
    complexity: {
      time: 'O(1)',
      space: 'O(N)',
      operations: {
        push: 'O(1)',
        pop: 'O(1)',
        top: 'O(1)'
      }
    },
    headers: ['<stack>'],
    isSTL: true
  },

  {
    id: 'queue',
    name: 'std::queue',
    category: 'adapter',
    cppType: 'std::queue',
    properties: ['fifo', 'front_access', 'back_access'],
    satisfies: [
      'fifo',
      'notification_queue',
      'queue_simulation',
      'team_queue',
      'card_war_simulation'
    ],
    requires: ['sequence'],
    produces: ['fifo_state'],
    dataStructures: ['sequence_dynamic'],
    supportedOperations: ['push', 'pop', 'front', 'back', 'empty', 'size'],
    complexity: {
      time: 'O(1)',
      space: 'O(N)',
      operations: {
        push: 'O(1)',
        pop: 'O(1)',
        front: 'O(1)',
        back: 'O(1)'
      }
    },
    headers: ['<queue>'],
    isSTL: true
  },

  {
    id: 'priority_queue_max',
    name: 'std::priority_queue (max_heap)',
    category: 'adapter',
    cppType: 'std::priority_queue',
    variant: 'max_heap',
    properties: [
      'priority_order',
      'top_extreme_access',
      'dynamic_insertion',
      'dynamic_removal',
      'max_heap'
    ],
    satisfies: [
      'maximum_retrieval',
      'priority_queue_operations',
      'multi_priority_queue',
      'priority_queue_halving'
    ],
    requires: ['sequence'],
    produces: ['max_heap_state'],
    dataStructures: ['sequence_dynamic'],
    supportedOperations: ['push', 'pop', 'top', 'empty', 'size'],
    complexity: {
      time: 'O(log N)',
      space: 'O(N)',
      operations: {
        push: 'O(log N)',
        pop: 'O(log N)',
        top: 'O(1)'
      }
    },
    headers: ['<queue>'],
    isSTL: true
  },

  {
    id: 'priority_queue_min',
    name: 'std::priority_queue (min_heap)',
    category: 'adapter',
    cppType: 'std::priority_queue',
    variant: 'min_heap',
    properties: [
      'priority_order',
      'top_extreme_access',
      'dynamic_insertion',
      'dynamic_removal',
      'min_heap'
    ],
    satisfies: ['minimum_retrieval', 'interval_partitioning'],
    requires: ['sequence'],
    produces: ['min_heap_state'],
    dataStructures: ['sequence_dynamic', 'intervals'],
    supportedOperations: ['push', 'pop', 'top', 'empty', 'size'],
    complexity: {
      time: 'O(log N)',
      space: 'O(N)',
      operations: {
        push: 'O(log N)',
        pop: 'O(log N)',
        top: 'O(1)'
      }
    },
    headers: ['<queue>', '<vector>'],
    isSTL: true
  },

  // ─── Ordered Associative Containers ────────────────────────────────────────

  {
    id: 'set',
    name: 'std::set',
    category: 'container',
    cppType: 'std::set',
    properties: [
      'ordered',
      'unique_keys',
      'dynamic_insertion',
      'dynamic_deletion',
      'ordered_lookup'
    ],
    satisfies: ['uniqueness', 'sorted_order', 'ordered_lookup', 'duplicate_detection', 'distinct_count'],
    requires: ['sequence'],
    produces: ['unique_sorted_sequence'],
    dataStructures: ['sequence_static', 'sequence_dynamic'],
    supportedOperations: [
      'insert', 'erase', 'find', 'lower_bound', 'upper_bound',
      'begin', 'end', 'size', 'empty'
    ],
    complexity: {
      time: 'O(log N)',
      space: 'O(N)',
      operations: {
        insert: 'O(log N)',
        erase: 'O(log N)',
        find: 'O(log N)',
        lower_bound: 'O(log N)',
        upper_bound: 'O(log N)'
      }
    },
    headers: ['<set>'],
    isSTL: true
  },

  {
    id: 'multiset',
    name: 'std::multiset',
    category: 'container',
    cppType: 'std::multiset',
    properties: [
      'ordered',
      'duplicate_keys',
      'dynamic_insertion',
      'dynamic_deletion',
      'ordered_lookup'
    ],
    satisfies: ['duplicate_preservation', 'sorted_order', 'ordered_lookup', 'multiset_operations'],
    requires: ['sequence'],
    produces: ['sorted_sequence'],
    dataStructures: ['sequence_static', 'sequence_dynamic'],
    supportedOperations: [
      'insert', 'erase', 'find', 'lower_bound', 'upper_bound',
      'count', 'begin', 'end', 'size', 'empty'
    ],
    complexity: {
      time: 'O(log N)',
      space: 'O(N)',
      operations: {
        insert: 'O(log N)',
        erase: 'O(log N)',
        find: 'O(log N)',
        lower_bound: 'O(log N)',
        upper_bound: 'O(log N)',
        count: 'O(log N + count)'
      }
    },
    headers: ['<set>'],
    isSTL: true
  },

  {
    id: 'map',
    name: 'std::map',
    category: 'container',
    cppType: 'std::map',
    properties: [
      'ordered_keys',
      'key_value_mapping',
      'unique_keys',
      'dynamic_insertion',
      'dynamic_deletion',
      'ordered_lookup'
    ],
    satisfies: [
      'frequency_count',
      'ordered_frequency_output',
      'key_value_mapping',
      'ordered_lookup',
      'sorted_order',
      'uniqueness',
      'registration_system'
    ],
    requires: ['sequence'],
    produces: ['ordered_frequency_state'],
    dataStructures: ['sequence_static', 'sequence_dynamic'],
    supportedOperations: [
      'insert', 'erase', 'find', 'lower_bound', 'upper_bound',
      'operator[]', 'begin', 'end', 'size', 'empty'
    ],
    complexity: {
      time: 'O(log N)',
      space: 'O(N)',
      operations: {
        insert: 'O(log N)',
        erase: 'O(log N)',
        find: 'O(log N)',
        'operator[]': 'O(log N)',
        lower_bound: 'O(log N)',
        upper_bound: 'O(log N)'
      }
    },
    headers: ['<map>'],
    isSTL: true
  },

  {
    id: 'multimap',
    name: 'std::multimap',
    category: 'container',
    cppType: 'std::multimap',
    properties: ['ordered_keys', 'key_value_mapping', 'duplicate_keys'],
    satisfies: ['key_value_mapping', 'duplicate_preservation'],
    requires: ['sequence'],
    produces: ['frequency_state'],
    dataStructures: ['sequence_static', 'sequence_dynamic'],
    supportedOperations: ['insert', 'erase', 'find', 'count', 'equal_range'],
    complexity: {
      time: 'O(log N)',
      space: 'O(N)'
    },
    headers: ['<map>'],
    isSTL: true
  },

  // ─── Unordered Associative Containers ──────────────────────────────────────

  {
    id: 'unordered_set',
    name: 'std::unordered_set',
    category: 'container',
    cppType: 'std::unordered_set',
    properties: ['unique_keys', 'hash_based', 'average_constant_lookup', 'unordered'],
    satisfies: ['uniqueness', 'duplicate_detection', 'fast_membership', 'distinct_count'],
    requires: ['sequence'],
    produces: ['unique_sequence'],
    dataStructures: ['sequence_static', 'sequence_dynamic'],
    supportedOperations: ['insert', 'erase', 'find', 'count', 'size', 'empty'],
    complexity: {
      time: 'O(1)',
      space: 'O(N)',
      averageTime: 'average O(1)',
      worstTime: 'worst O(N)',
      operations: {
        insert: 'average O(1), worst O(N)',
        find: 'average O(1), worst O(N)',
        count: 'average O(1), worst O(N)',
        erase: 'average O(1), worst O(N)'
      }
    },
    headers: ['<unordered_set>'],
    isSTL: true
  },

  {
    id: 'unordered_map',
    name: 'std::unordered_map',
    category: 'container',
    cppType: 'std::unordered_map',
    properties: [
      'key_value_mapping',
      'unique_keys',
      'hash_based',
      'average_constant_lookup',
      'unordered'
    ],
    satisfies: [
      'frequency_count',
      'duplicate_detection',
      'fast_membership',
      'key_value_mapping',
      'uniqueness',
      'registration_system'
    ],
    requires: ['sequence'],
    produces: ['frequency_map'],
    dataStructures: ['sequence_static', 'sequence_dynamic'],
    supportedOperations: ['insert', 'erase', 'find', 'count', 'operator[]', 'size', 'empty'],
    complexity: {
      time: 'O(1)',
      space: 'O(N)',
      averageTime: 'average O(1)',
      worstTime: 'worst O(N)',
      operations: {
        insert: 'average O(1), worst O(N)',
        find: 'average O(1), worst O(N)',
        'operator[]': 'average O(1), worst O(N)',
        erase: 'average O(1), worst O(N)'
      }
    },
    headers: ['<unordered_map>'],
    isSTL: true
  },

  // ─── Utility Type ──────────────────────────────────────────────────────────

  {
    id: 'pair',
    name: 'std::pair',
    category: 'utility',
    cppType: 'std::pair',
    properties: [
      'pair',
      'key_value_pair',
      'two_value_record',
      'coordinate_pair',
      'interval',
      'edge_representation'
    ],
    satisfies: ['key_value_mapping'],
    requires: [],
    produces: ['intervals'],
    dataStructures: ['intervals', 'sequence_static'],
    supportedOperations: ['first', 'second'],
    complexity: {
      time: 'O(1)',
      space: 'O(1)'
    },
    headers: ['<utility>'],
    isSTL: true
  },

  // ─── <algorithm> Concepts ─────────────────────────────────────────────────

  {
    id: 'sort',
    name: 'std::sort',
    category: 'algorithm',
    cppType: 'std::sort',
    properties: ['comparison_sort', 'introsort', 'non_stable'],
    satisfies: ['sorting', 'sorted_order'],
    requires: ['sequence'],
    produces: ['sorted_sequence'],
    dataStructures: ['sequence_static', 'sequence_dynamic', 'intervals'],
    supportedOperations: ['sort'],
    complexity: {
      time: 'O(N log N)',
      space: 'O(log N)'
    },
    headers: ['<algorithm>'],
    isSTL: true
  },

  {
    id: 'stable_sort',
    name: 'std::stable_sort',
    category: 'algorithm',
    cppType: 'std::stable_sort',
    properties: ['comparison_sort', 'mergesort', 'stable_order'],
    satisfies: ['sorting', 'sorted_order'],
    requires: ['sequence'],
    produces: ['sorted_sequence'],
    dataStructures: ['sequence_static', 'sequence_dynamic'],
    supportedOperations: ['stable_sort'],
    complexity: {
      time: 'O(N log N)',
      space: 'O(N)'
    },
    headers: ['<algorithm>'],
    isSTL: true
  },

  {
    id: 'reverse',
    name: 'std::reverse',
    category: 'algorithm',
    cppType: 'std::reverse',
    properties: ['in_place_reversal'],
    satisfies: ['reversal'],
    requires: ['sequence'],
    produces: ['sequence'],
    dataStructures: ['sequence_static', 'sequence_dynamic'],
    supportedOperations: ['reverse'],
    complexity: {
      time: 'O(N)',
      space: 'O(1)'
    },
    headers: ['<algorithm>'],
    isSTL: true
  },

  {
    id: 'lower_bound',
    name: 'std::lower_bound',
    category: 'algorithm',
    cppType: 'std::lower_bound',
    properties: ['binary_search', 'threshold_search', 'ordered_lookup'],
    satisfies: ['threshold_search', 'ordered_lookup'],
    requires: ['sorted_sequence'],
    produces: ['position_result'],
    dataStructures: ['sequence_static'],
    supportedOperations: ['lower_bound'],
    complexity: {
      time: 'O(log N)',
      space: 'O(1)'
    },
    headers: ['<algorithm>'],
    isSTL: true
  },

  {
    id: 'upper_bound',
    name: 'std::upper_bound',
    category: 'algorithm',
    cppType: 'std::upper_bound',
    properties: ['binary_search', 'threshold_search', 'ordered_lookup'],
    satisfies: ['threshold_search', 'ordered_lookup'],
    requires: ['sorted_sequence'],
    produces: ['position_result'],
    dataStructures: ['sequence_static'],
    supportedOperations: ['upper_bound'],
    complexity: {
      time: 'O(log N)',
      space: 'O(1)'
    },
    headers: ['<algorithm>'],
    isSTL: true
  },

  {
    id: 'binary_search_algo',
    name: 'std::binary_search',
    category: 'algorithm',
    cppType: 'std::binary_search',
    properties: ['binary_search', 'membership_search'],
    satisfies: ['element_lookup'],
    requires: ['sorted_sequence'],
    produces: ['query_results'],
    dataStructures: ['sequence_static'],
    supportedOperations: ['binary_search'],
    complexity: {
      time: 'O(log N)',
      space: 'O(1)'
    },
    headers: ['<algorithm>'],
    isSTL: true
  },

  {
    id: 'min_element',
    name: 'std::min_element',
    category: 'algorithm',
    cppType: 'std::min_element',
    properties: ['linear_scan', 'extreme_element'],
    satisfies: ['minimum_retrieval'],
    requires: ['sequence'],
    produces: ['query_results'],
    dataStructures: ['sequence_static', 'sequence_dynamic'],
    supportedOperations: ['min_element'],
    complexity: {
      time: 'O(N)',
      space: 'O(1)'
    },
    headers: ['<algorithm>'],
    isSTL: true
  },

  {
    id: 'max_element',
    name: 'std::max_element',
    category: 'algorithm',
    cppType: 'std::max_element',
    properties: ['linear_scan', 'extreme_element'],
    satisfies: ['maximum_retrieval'],
    requires: ['sequence'],
    produces: ['query_results'],
    dataStructures: ['sequence_static', 'sequence_dynamic'],
    supportedOperations: ['max_element'],
    complexity: {
      time: 'O(N)',
      space: 'O(1)'
    },
    headers: ['<algorithm>'],
    isSTL: true
  },

  {
    id: 'arithmetic_gap',
    name: 'Arithmetic Gap',
    category: 'manual',
    properties: ['linear_scan', 'math_trick'],
    satisfies: ['arithmetic_gap'],
    requires: ['sequence'],
    produces: ['query_results'],
    dataStructures: ['sequence_static'],
    complexity: {
      time: 'O(N)',
      space: 'O(1)'
    },
    templateId: 'arithmeticGap',
    isSTL: false
  },

  {
    id: 'lis',
    name: 'Longest Increasing Subsequence',
    category: 'algorithm',
    properties: ['dp', 'binary_search'],
    satisfies: ['lis_dp', 'recurrence_1d'],
    requires: ['sequence'],
    produces: ['query_results'],
    dataStructures: ['sequence_static'],
    complexity: {
      time: 'O(N log N)',
      space: 'O(N)'
    },
    templateId: 'lis',
    isSTL: false
  }
];

export function getSTLConcept(id: string): KnowledgeConcept | null {
  return STL_CONCEPTS.find(c => c.id === id) || null;
}

export function getSTLConceptsSatisfying(op: RequiredOperation): KnowledgeConcept[] {
  return STL_CONCEPTS.filter(c => c.satisfies.includes(op));
}
