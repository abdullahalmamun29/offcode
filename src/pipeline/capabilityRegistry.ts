/**
 * CHUP / Offcode — Capability Registry (Phase 3)
 *
 * Defines registered capabilities across Offcode domains using structured evidence predicates.
 *
 * Design Invariants:
 * - Requirements are structured predicates (kind, value, optional type/role).
 * - OR-alternatives supported via string arrays (e.g. ['end', 'tail']).
 * - Contradictions are role-based (primary entity conflict), preventing brittle global bans.
 * - Capabilities are declarative; scoring and execution logic remain strictly downstream.
 */

import { EvidencePredicate, ProblemType } from '../models/problemSpec';

export interface CapabilityDefinition {
  id: string;
  name: string;
  domain: ProblemType;
  requirements: EvidencePredicate[];
  optionalEvidence?: EvidencePredicate[];
  contradictions?: EvidencePredicate[];
}

export const REGISTERED_CAPABILITIES: CapabilityDefinition[] = [
  // ── Data Structures (Template Match) ──────────────────────────────────────────

  // Singly Linked List: insert_end
  {
    id: 'singly_linked_list.insert_end',
    name: 'Singly Linked List Insert End',
    domain: 'template_match',
    requirements: [
      { kind: 'entity', value: ['singly_linked_list', 'linked_list'], role: 'primary' },
      { kind: 'operation', value: 'insert' },
      { kind: 'constraint', type: 'position', value: ['end', 'tail', 'back', 'last'] }
    ],
    optionalEvidence: [
      { kind: 'entity', value: 'node' },
      { kind: 'intent', value: ['implement', 'create', 'write', 'program', 'code'] }
    ],
    contradictions: [
      { kind: 'entity', value: ['binary_tree', 'bst', 'binary_search_tree', 'stack', 'queue', 'heap', 'graph'], role: 'primary' },
      { kind: 'constraint', type: 'position', value: ['beginning', 'head', 'front', 'start'] },
      { kind: 'operation', value: ['delete', 'search'] }
    ]
  },

  // Singly Linked List: insert_beginning
  {
    id: 'singly_linked_list.insert_beginning',
    name: 'Singly Linked List Insert Beginning',
    domain: 'template_match',
    requirements: [
      { kind: 'entity', value: ['singly_linked_list', 'linked_list'], role: 'primary' },
      { kind: 'operation', value: 'insert' },
      { kind: 'constraint', type: 'position', value: ['beginning', 'head', 'front', 'start'] }
    ],
    optionalEvidence: [
      { kind: 'entity', value: 'node' },
      { kind: 'intent', value: ['implement', 'create', 'write', 'program', 'code'] }
    ],
    contradictions: [
      { kind: 'entity', value: ['binary_tree', 'bst', 'binary_search_tree', 'stack', 'queue', 'heap', 'graph'], role: 'primary' },
      { kind: 'constraint', type: 'position', value: ['end', 'tail', 'back', 'last'] },
      { kind: 'operation', value: ['delete', 'search'] }
    ]
  },

  // Singly Linked List: delete_beginning
  {
    id: 'singly_linked_list.delete_beginning',
    name: 'Singly Linked List Delete Beginning',
    domain: 'template_match',
    requirements: [
      { kind: 'entity', value: ['singly_linked_list', 'linked_list'], role: 'primary' },
      { kind: 'operation', value: 'delete' },
      { kind: 'constraint', type: 'position', value: ['beginning', 'head', 'front', 'start'] }
    ],
    contradictions: [
      { kind: 'entity', value: ['binary_tree', 'bst', 'binary_search_tree', 'stack', 'queue', 'heap', 'graph'], role: 'primary' },
      { kind: 'constraint', type: 'position', value: ['end', 'tail', 'back', 'last'] },
      { kind: 'operation', value: ['insert', 'search'] }
    ]
  },

  // Singly Linked List: delete_end
  {
    id: 'singly_linked_list.delete_end',
    name: 'Singly Linked List Delete End',
    domain: 'template_match',
    requirements: [
      { kind: 'entity', value: ['singly_linked_list', 'linked_list'], role: 'primary' },
      { kind: 'operation', value: 'delete' },
      { kind: 'constraint', type: 'position', value: ['end', 'tail', 'back', 'last'] }
    ],
    contradictions: [
      { kind: 'entity', value: ['binary_tree', 'bst', 'binary_search_tree', 'stack', 'queue', 'heap', 'graph'], role: 'primary' },
      { kind: 'constraint', type: 'position', value: ['beginning', 'head', 'front', 'start'] },
      { kind: 'operation', value: ['insert', 'search'] }
    ]
  },

  // Doubly Linked List: insert_end
  {
    id: 'doubly_linked_list.insert_end',
    name: 'Doubly Linked List Insert End',
    domain: 'template_match',
    requirements: [
      { kind: 'entity', value: 'doubly_linked_list', role: 'primary' },
      { kind: 'operation', value: 'insert' },
      { kind: 'constraint', type: 'position', value: ['end', 'tail', 'back', 'last'] }
    ],
    contradictions: [
      { kind: 'entity', value: ['binary_tree', 'bst', 'stack', 'queue'], role: 'primary' },
      { kind: 'constraint', type: 'position', value: ['beginning', 'head', 'front', 'start'] }
    ]
  },

  // Doubly Linked List: insert_beginning
  {
    id: 'doubly_linked_list.insert_beginning',
    name: 'Doubly Linked List Insert Beginning',
    domain: 'template_match',
    requirements: [
      { kind: 'entity', value: 'doubly_linked_list', role: 'primary' },
      { kind: 'operation', value: 'insert' },
      { kind: 'constraint', type: 'position', value: ['beginning', 'head', 'front', 'start'] }
    ],
    contradictions: [
      { kind: 'entity', value: ['binary_tree', 'bst', 'stack', 'queue'], role: 'primary' },
      { kind: 'constraint', type: 'position', value: ['end', 'tail', 'back', 'last'] }
    ]
  },

  // Stack: push
  {
    id: 'stack.push',
    name: 'Stack Push',
    domain: 'template_match',
    requirements: [
      { kind: 'entity', value: 'stack', role: 'primary' },
      { kind: 'operation', value: ['push', 'insert'] }
    ],
    contradictions: [
      { kind: 'entity', value: ['queue', 'linked_list', 'binary_tree'], role: 'primary' },
      { kind: 'operation', value: ['pop', 'peek'] }
    ]
  },

  // Stack: pop
  {
    id: 'stack.pop',
    name: 'Stack Pop',
    domain: 'template_match',
    requirements: [
      { kind: 'entity', value: 'stack', role: 'primary' },
      { kind: 'operation', value: ['pop', 'delete'] }
    ],
    contradictions: [
      { kind: 'entity', value: ['queue', 'linked_list', 'binary_tree'], role: 'primary' },
      { kind: 'operation', value: ['push', 'peek'] }
    ]
  },

  // Queue: enqueue
  {
    id: 'queue.enqueue',
    name: 'Queue Enqueue',
    domain: 'template_match',
    requirements: [
      { kind: 'entity', value: ['queue', 'linear_queue', 'circular_queue'], role: 'primary' },
      { kind: 'operation', value: ['enqueue', 'push', 'insert'] }
    ],
    contradictions: [
      { kind: 'entity', value: ['stack', 'binary_tree'], role: 'primary' },
      { kind: 'operation', value: ['dequeue', 'pop'] }
    ]
  },

  // Binary Search Tree: insert
  {
    id: 'binary_search_tree.insert',
    name: 'Binary Search Tree Insert',
    domain: 'template_match',
    requirements: [
      { kind: 'entity', value: ['binary_search_tree', 'bst', 'binary_tree'], role: 'primary' },
      { kind: 'operation', value: 'insert' }
    ],
    contradictions: [
      { kind: 'entity', value: ['singly_linked_list', 'doubly_linked_list', 'stack', 'queue'], role: 'primary' },
      { kind: 'operation', value: 'delete' }
    ]
  },

  // ── Standard Algorithms ───────────────────────────────────────────────────────

  // Binary Search
  {
    id: 'binary_search',
    name: 'Binary Search',
    domain: 'template_match',
    requirements: [
      { kind: 'entity', value: 'binary_search', role: 'primary' }
    ],
    optionalEvidence: [
      { kind: 'operation', value: ['search', 'find'] },
      { kind: 'constraint', type: 'ordering', value: ['sorted', 'ascending', 'descending'] }
    ],
    contradictions: [
      { kind: 'entity', value: ['linked_list', 'stack', 'queue'], role: 'primary' }
    ]
  },

  // Bubble Sort
  {
    id: 'bubble_sort',
    name: 'Bubble Sort',
    domain: 'template_match',
    requirements: [
      { kind: 'entity', value: 'bubble_sort', role: 'primary' }
    ],
    optionalEvidence: [
      { kind: 'operation', value: 'sort' }
    ]
  },

  // Quick Sort
  {
    id: 'quick_sort',
    name: 'Quick Sort',
    domain: 'template_match',
    requirements: [
      { kind: 'entity', value: 'quick_sort', role: 'primary' }
    ],
    optionalEvidence: [
      { kind: 'operation', value: 'sort' }
    ]
  },

  // Merge Sort
  {
    id: 'merge_sort',
    name: 'Merge Sort',
    domain: 'template_match',
    requirements: [
      { kind: 'entity', value: 'merge_sort', role: 'primary' }
    ],
    optionalEvidence: [
      { kind: 'operation', value: 'sort' }
    ]
  },

  // ── Numerical Methods (Academic Domain) ───────────────────────────────────────

  // LU Decomposition
  {
    id: 'lu_decomposition',
    name: 'LU Decomposition',
    domain: 'academic',
    requirements: [
      { kind: 'entity', value: 'lu_decomposition', role: 'primary' }
    ],
    optionalEvidence: [
      { kind: 'entity', value: 'matrix' },
      { kind: 'intent', value: ['implement', 'calculate', 'find', 'solve', 'compute'] }
    ],
    contradictions: [
      { kind: 'entity', value: ['binary_tree', 'bst', 'singly_linked_list', 'stack', 'queue'], role: 'primary' }
    ]
  },

  // Gauss Elimination
  {
    id: 'gauss_elimination',
    name: 'Gauss Elimination',
    domain: 'academic',
    requirements: [
      { kind: 'entity', value: ['gauss_elimination', 'gauss_jordan'], role: 'primary' }
    ],
    optionalEvidence: [
      { kind: 'entity', value: 'matrix' },
      { kind: 'intent', value: ['solve', 'compute', 'calculate', 'implement'] }
    ],
    contradictions: [
      { kind: 'entity', value: ['binary_tree', 'singly_linked_list'], role: 'primary' }
    ]
  },

  // Bisection Method
  {
    id: 'bisection',
    name: 'Bisection Method',
    domain: 'academic',
    requirements: [
      { kind: 'entity', value: 'bisection', role: 'primary' }
    ],
    optionalEvidence: [
      { kind: 'intent', value: ['find', 'solve', 'calculate', 'implement'] },
      { kind: 'entity', value: 'root' }
    ]
  },

  // Newton-Raphson Method
  {
    id: 'newton_raphson',
    name: 'Newton-Raphson Method',
    domain: 'academic',
    requirements: [
      { kind: 'entity', value: 'newton_raphson', role: 'primary' }
    ],
    optionalEvidence: [
      { kind: 'intent', value: ['find', 'solve', 'calculate', 'implement'] },
      { kind: 'entity', value: 'root' }
    ]
  },

  // Runge-Kutta Method
  {
    id: 'runge_kutta',
    name: 'Runge-Kutta Method',
    domain: 'academic',
    requirements: [
      { kind: 'entity', value: ['runge_kutta', 'runge_kutta_4'], role: 'primary' }
    ],
    optionalEvidence: [
      { kind: 'intent', value: ['solve', 'compute', 'calculate', 'derive', 'implement'] }
    ]
  },

  // Simpson's Rule
  {
    id: 'simpson',
    name: "Simpson's Rule",
    domain: 'academic',
    requirements: [
      { kind: 'entity', value: ['simpson', 'simpson_one_third', 'simpson_three_eighth'], role: 'primary' }
    ],
    optionalEvidence: [
      { kind: 'intent', value: ['calculate', 'integrate', 'compute', 'implement'] }
    ]
  },

  // ── Code Debug Domain ─────────────────────────────────────────────────────────

  {
    id: 'code_debug.general',
    name: 'General Code Debugging',
    domain: 'code_debug',
    requirements: [
      { kind: 'intent', value: ['debug', 'fix', 'troubleshoot'] }
    ],
    optionalEvidence: [
      { kind: 'entity', value: ['error', 'bug', 'crash', 'segfault'] }
    ]
  }
];
