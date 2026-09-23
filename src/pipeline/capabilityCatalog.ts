/**
 * CHUP / Offcode — Authoritative Unified Capability Registry (Phase 4)
 *
 * Exhaustively catalogs capabilities, algorithms, components, mechanisms, and hierarchy
 * derived from the entire frozen CHUP repository.
 *
 * Invariants:
 * - Domain is metadata only.
 * - 100% deterministic, offline, and self-contained.
 * - Enforces 4-tier model: Capability -> Algorithm -> Component -> ImplementationMechanism.
 */

import {
  Capability,
  AlgorithmDefinition,
  AlgorithmComponent,
  ImplementationMechanism,
  CapabilityHierarchyNode
} from '../models/capabilityModel';

export class AuthoritativeCapabilityRegistry {
  private capabilities = new Map<string, Capability>();
  private algorithms = new Map<string, AlgorithmDefinition>();
  private components = new Map<string, AlgorithmComponent>();
  private mechanisms = new Map<string, ImplementationMechanism>();
  private hierarchy = new Map<string, CapabilityHierarchyNode>();
  private aliasMap = new Map<string, { capabilityId?: string; algorithmId?: string }>();

  constructor() {
    this.initializeRegistry();
  }

  // ── Registration Methods ────────────────────────────────────────────────────

  public registerComponent(comp: AlgorithmComponent): void {
    if (this.components.has(comp.id)) {
      throw new Error(`Duplicate AlgorithmComponent ID: ${comp.id}`);
    }
    this.components.set(comp.id, comp);
  }

  public registerMechanism(mech: ImplementationMechanism): void {
    if (this.mechanisms.has(mech.id)) {
      throw new Error(`Duplicate ImplementationMechanism ID: ${mech.id}`);
    }
    this.mechanisms.set(mech.id, mech);
  }

  public registerAlgorithm(algo: AlgorithmDefinition): void {
    if (this.algorithms.has(algo.id)) {
      throw new Error(`Duplicate AlgorithmDefinition ID: ${algo.id}`);
    }
    this.algorithms.set(algo.id, algo);

    for (const alias of algo.aliases) {
      const clean = alias.toLowerCase().trim();
      this.aliasMap.set(clean, { algorithmId: algo.id, capabilityId: algo.capabilityId });
    }
    this.aliasMap.set(algo.id.toLowerCase().trim(), { algorithmId: algo.id, capabilityId: algo.capabilityId });
    this.aliasMap.set(algo.name.toLowerCase().trim(), { algorithmId: algo.id, capabilityId: algo.capabilityId });
  }

  public registerCapability(cap: Capability): void {
    if (this.capabilities.has(cap.id)) {
      throw new Error(`Duplicate Capability ID: ${cap.id}`);
    }
    this.capabilities.set(cap.id, cap);

    for (const alias of cap.aliases) {
      const clean = alias.toLowerCase().trim();
      if (!this.aliasMap.has(clean)) {
        this.aliasMap.set(clean, { capabilityId: cap.id });
      }
    }
    this.aliasMap.set(cap.id.toLowerCase().trim(), { capabilityId: cap.id });
    this.aliasMap.set(cap.canonicalName.toLowerCase().trim(), { capabilityId: cap.id });
  }

  public registerHierarchyNode(node: CapabilityHierarchyNode): void {
    this.hierarchy.set(node.id, node);
  }

  // ── Lookup Methods ──────────────────────────────────────────────────────────

  public getCapability(id: string): Capability | undefined {
    return this.capabilities.get(id);
  }

  public getAlgorithm(id: string): AlgorithmDefinition | undefined {
    return this.algorithms.get(id);
  }

  public getComponent(id: string): AlgorithmComponent | undefined {
    return this.components.get(id);
  }

  public getMechanism(id: string): ImplementationMechanism | undefined {
    return this.mechanisms.get(id);
  }

  public getHierarchyNode(id: string): CapabilityHierarchyNode | undefined {
    return this.hierarchy.get(id);
  }

  public resolveAlias(alias: string): { capability?: Capability; algorithm?: AlgorithmDefinition } | undefined {
    const clean = alias.toLowerCase().trim().replace(/[-_]/g, ' ');
    const direct = this.aliasMap.get(clean) || this.aliasMap.get(alias.toLowerCase().trim());
    if (!direct) return undefined;

    return {
      capability: direct.capabilityId ? this.capabilities.get(direct.capabilityId) : undefined,
      algorithm: direct.algorithmId ? this.algorithms.get(direct.algorithmId) : undefined
    };
  }

  public getAllCapabilities(): Capability[] {
    return Array.from(this.capabilities.values());
  }

  public getAllAlgorithms(): AlgorithmDefinition[] {
    return Array.from(this.algorithms.values());
  }

  public getAllComponents(): AlgorithmComponent[] {
    return Array.from(this.components.values());
  }

  public getAllMechanisms(): ImplementationMechanism[] {
    return Array.from(this.mechanisms.values());
  }

  public validate(): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    // Verify algorithms reference valid capabilities and components
    for (const algo of this.algorithms.values()) {
      if (!this.capabilities.has(algo.capabilityId)) {
        errors.push(`Algorithm ${algo.id} references non-existent capability: ${algo.capabilityId}`);
      }
      for (const compId of algo.requiredComponents) {
        if (!this.components.has(compId)) {
          errors.push(`Algorithm ${algo.id} references non-existent component: ${compId}`);
        }
      }
      for (const mechId of algo.supportedMechanisms) {
        if (!this.mechanisms.has(mechId)) {
          errors.push(`Algorithm ${algo.id} references non-existent mechanism: ${mechId}`);
        }
      }
    }

    // Verify capabilities reference valid algorithms
    for (const cap of this.capabilities.values()) {
      for (const algoId of cap.algorithms) {
        if (!this.algorithms.has(algoId)) {
          errors.push(`Capability ${cap.id} references non-existent algorithm: ${algoId}`);
        }
      }
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  // ── Population from Repository Knowledge ────────────────────────────────────

  private initializeRegistry(): void {
    // 1. Register Core Algorithm Components
    this.registerComponent({
      id: 'priority_queue',
      name: 'Priority Queue / Heap Structure',
      description: 'Maintains optimal frontier elements with logarithmic extraction',
      role: 'data_organizer',
      requiredInterfaces: ['comparison'],
      providedInterfaces: ['push', 'pop_min', 'top', 'empty']
    });

    this.registerComponent({
      id: 'edge_relaxation',
      name: 'Edge Distance Relaxation',
      description: 'Updates distance bounds satisfying the triangle inequality: d[v] = min(d[v], d[u] + w)',
      role: 'invariant_maintainer',
      requiredInterfaces: ['distance_array', 'graph_adjacency'],
      providedInterfaces: ['relax_edge']
    });

    this.registerComponent({
      id: 'disjoint_set_union',
      name: 'Disjoint Set Union (DSU / Union-Find)',
      description: 'Tracks partition of elements into disjoint sets with near-O(1) find and union',
      role: 'invariant_maintainer',
      requiredInterfaces: ['parent_array', 'rank_array'],
      providedInterfaces: ['find', 'unite', 'same_set']
    });

    this.registerComponent({
      id: 'pivoting',
      name: 'Partial Matrix Pivoting',
      description: 'Swaps rows to place maximum magnitude element on diagonal, preventing division by zero',
      role: 'numerical_kernel',
      requiredInterfaces: ['matrix_rows'],
      providedInterfaces: ['pivot_row']
    });

    this.registerComponent({
      id: 'forward_substitution',
      name: 'Forward Substitution',
      description: 'Solves lower triangular system Ly = b',
      role: 'numerical_kernel',
      requiredInterfaces: ['lower_triangular_matrix', 'vector'],
      providedInterfaces: ['solve_forward']
    });

    this.registerComponent({
      id: 'back_substitution',
      name: 'Back Substitution',
      description: 'Solves upper triangular system Ux = y',
      role: 'numerical_kernel',
      requiredInterfaces: ['upper_triangular_matrix', 'vector'],
      providedInterfaces: ['solve_back']
    });

    this.registerComponent({
      id: 'interval_bisection',
      name: 'Interval Bisection',
      description: 'Halves search interval containing target root or bound',
      role: 'transition_step',
      requiredInterfaces: ['ordered_domain'],
      providedInterfaces: ['midpoint', 'shrink_interval']
    });

    this.registerComponent({
      id: 'prefix_sum_array',
      name: 'Prefix Sum Array',
      description: 'Cumulative sum array enabling O(1) range queries: sum(L, R) = pref[R] - pref[L-1]',
      role: 'data_organizer',
      requiredInterfaces: ['input_array'],
      providedInterfaces: ['range_query']
    });

    this.registerComponent({
      id: 'two_pointers_window',
      name: 'Two Pointers / Sliding Window',
      description: 'Maintains left and right pointer bounds with monotonic state expansion/contraction',
      role: 'invariant_maintainer',
      requiredInterfaces: ['indexed_sequence'],
      providedInterfaces: ['advance_left', 'advance_right']
    });

    this.registerComponent({
      id: 'monotonic_envelope',
      name: 'Monotonic Envelope / Stack',
      description: 'Maintains strictly increasing or decreasing sequence for nearest smaller/greater queries',
      role: 'invariant_maintainer',
      requiredInterfaces: ['sequence_elements'],
      providedInterfaces: ['push_monotonic', 'pop_invalidated']
    });

    this.registerComponent({
      id: 'binary_indexed_tree',
      name: 'Binary Indexed Tree (Fenwick)',
      description: 'Tree represented implicitly in an array with LSB indexing for O(log N) prefix updates and queries',
      role: 'data_organizer',
      requiredInterfaces: ['monoid_operation'],
      providedInterfaces: ['add', 'query_prefix']
    });

    this.registerComponent({
      id: 'segment_tree_node',
      name: 'Segment Tree Array',
      description: 'Complete binary tree over ranges for O(log N) associative aggregation and updates',
      role: 'data_organizer',
      requiredInterfaces: ['associative_combine'],
      providedInterfaces: ['update_point', 'query_range']
    });

    this.registerComponent({
      id: 'linked_node_chain',
      name: 'Linked Node Chain',
      description: 'Dynamically allocated nodes connected by pointers',
      role: 'data_organizer',
      requiredInterfaces: ['heap_memory'],
      providedInterfaces: ['insert_after', 'delete_after', 'traverse']
    });

    this.registerComponent({
      id: 'cyclic_node_chain',
      name: 'Cyclic Node Chain',
      description: 'Linked nodes where tail connects back to head',
      role: 'data_organizer',
      requiredInterfaces: ['heap_memory'],
      providedInterfaces: ['circular_traverse']
    });

    this.registerComponent({
      id: 'tree_node_links',
      name: 'Hierarchical Tree Node Links',
      description: 'Nodes with left and right children references',
      role: 'data_organizer',
      requiredInterfaces: ['heap_memory'],
      providedInterfaces: ['inorder', 'insert_bst', 'search_bst']
    });

    this.registerComponent({
      id: 'array_based_static',
      name: 'Fixed-Size / Dynamic Static Array',
      description: 'Contiguous memory buffer supporting direct index-based random access',
      role: 'data_organizer',
      requiredInterfaces: [],
      providedInterfaces: ['random_access', 'indexed_read', 'indexed_write']
    });

    this.registerComponent({
      id: 'fifo_storage',
      name: 'FIFO Queue Buffer',
      description: 'First-in first-out storage buffer for frontier expansion',
      role: 'data_organizer',
      requiredInterfaces: [],
      providedInterfaces: ['enqueue', 'dequeue', 'empty']
    });

    this.registerComponent({
      id: 'lifo_storage',
      name: 'LIFO Stack Buffer',
      description: 'Last-in first-out storage buffer for backtracking and depth-first searches',
      role: 'data_organizer',
      requiredInterfaces: [],
      providedInterfaces: ['push', 'pop', 'top', 'empty']
    });

    // 2. Register Core Implementation Mechanisms
    this.registerMechanism({
      id: 'pointer_based_sll',
      name: 'Pointer-based Singly Linked Chain',
      representation: 'pointer_based',
      timeComplexity: 'O(1) insert/delete at head, O(N) access',
      spaceComplexity: 'O(N) with sizeof(Node) overhead',
      supportedConstraints: { manual: true, stl: false }
    });

    this.registerMechanism({
      id: 'pointer_based_dll',
      name: 'Pointer-based Doubly Linked Chain',
      representation: 'pointer_based',
      timeComplexity: 'O(1) insert/delete at known node, O(N) access',
      spaceComplexity: 'O(N) with 2 pointers per node',
      supportedConstraints: { manual: true, stl: false }
    });

    this.registerMechanism({
      id: 'pointer_based_cll',
      name: 'Pointer-based Circular Linked Chain',
      representation: 'pointer_based',
      timeComplexity: 'O(1) insert/delete at head/tail, O(N) access',
      spaceComplexity: 'O(N)',
      supportedConstraints: { manual: true, stl: false }
    });

    this.registerMechanism({
      id: 'binary_heap_std',
      name: 'Standard Binary Min-Heap Priority Queue',
      representation: 'stl',
      timeComplexity: 'O(log N) push/pop, O(1) top',
      spaceComplexity: 'O(N)',
      supportedConstraints: { stl: true }
    });

    this.registerMechanism({
      id: 'dense_matrix_vector',
      name: '2D Dense Matrix (std::vector<std::vector<double>>)',
      representation: 'matrix_dense',
      timeComplexity: 'O(1) row/cell indexing',
      spaceComplexity: 'O(N^2)',
      supportedConstraints: { arbitrary_order: true }
    });

    this.registerMechanism({
      id: 'array_based_static',
      name: 'Flat Contiguous Array',
      representation: 'array_based',
      timeComplexity: 'O(1) access',
      spaceComplexity: 'O(N)',
      supportedConstraints: { stl: false }
    });

    this.registerMechanism({
      id: 'stl_std_vector',
      name: 'Dynamic STL Vector',
      representation: 'stl',
      timeComplexity: 'O(1) amortized append, O(1) access',
      spaceComplexity: 'O(N)',
      supportedConstraints: { stl: true }
    });

    // 3. Register Hierarchy Nodes
    this.registerHierarchyNode({
      id: 'shortest_path',
      name: 'Shortest Path Algorithms',
      children: ['single_source_shortest_path', 'all_pairs_shortest_path'],
      associatedCapabilities: ['single_source_shortest_path', 'all_pairs_shortest_path']
    });

    this.registerHierarchyNode({
      id: 'linear_sequence_structure',
      name: 'Linear Sequence Structures',
      children: ['linked_list', 'sequential_array'],
      associatedCapabilities: ['singly_linked_list', 'doubly_linked_list', 'circular_linked_list', 'doubly_circular_linked_list', 'polynomial']
    });

    this.registerHierarchyNode({
      id: 'linear_system_solver',
      name: 'Linear System Solvers',
      children: ['direct_elimination', 'matrix_factorization', 'iterative_relaxation'],
      associatedCapabilities: ['lu_decomposition', 'gauss_elimination', 'jacobi']
    });

    this.registerHierarchyNode({
      id: 'range_aggregation',
      name: 'Range Aggregation Structures',
      children: ['prefix_sum', 'fenwick_tree', 'segment_tree'],
      associatedCapabilities: ['prefix_sum', 'fenwick_tree', 'segment_tree']
    });

    // 4. Register Capabilities and Algorithms

    // ── DATA STRUCTURES ──
    this.registerCapability({
      id: 'singly_linked_list',
      canonicalName: 'Singly Linked List',
      parentId: 'linear_sequence_structure',
      aliases: ['singly linked list', 'singly linked', 'singly list', 'sll', 'single linked list', 'linked list', 'linked_list', 'linkedlist'],
      semanticDescription: 'Linear sequence of data nodes connected sequentially via next pointers',
      domains: ['data_structures', 'academic', 'linear_storage'],
      supportedOperations: ['insert', 'delete', 'search', 'display', 'reverse', 'create', 'menu'],
      representations: ['pointer_based', 'stl'],
      algorithms: ['singly_linked_list_standard'],
      requiredStates: [],
      producedStates: ['LINKED_LIST_STRUCTURE'],
      constraints: { ordering: 'sequential' }
    });

    this.registerAlgorithm({
      id: 'singly_linked_list_standard',
      name: 'Standard Pointer Singly Linked List',
      aliases: ['singly_linked_list', 'sll_pointer'],
      capabilityId: 'singly_linked_list',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['tail_points_to_null', 'nodes_singly_linked'],
      postconditions: ['operation_completed'],
      complexity: { time: 'O(1) head, O(N) tail/search', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'doubly_linked_list',
      canonicalName: 'Doubly Linked List',
      parentId: 'linear_sequence_structure',
      aliases: ['doubly linked list', 'doubly linked', 'dll', 'double linked list'],
      semanticDescription: 'Linear sequence of nodes connected via next and prev pointers',
      domains: ['data_structures', 'academic'],
      supportedOperations: ['insert', 'delete', 'search', 'display', 'reverse', 'menu'],
      representations: ['pointer_based'],
      algorithms: ['doubly_linked_list_standard'],
      requiredStates: [],
      producedStates: ['DOUBLY_LINKED_LIST_STRUCTURE'],
      constraints: { bidirectional: true }
    });

    this.registerAlgorithm({
      id: 'doubly_linked_list_standard',
      name: 'Standard Pointer Doubly Linked List',
      aliases: ['doubly_linked_list'],
      capabilityId: 'doubly_linked_list',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_dll'],
      preconditions: [],
      invariants: ['node_prev_next_reciprocal'],
      postconditions: ['operation_completed'],
      complexity: { time: 'O(1) head/tail, O(N) search', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'circular_linked_list',
      canonicalName: 'Circular Linked List',
      parentId: 'linear_sequence_structure',
      aliases: ['circular linked list', 'cll', 'circular list'],
      semanticDescription: 'Linked list whose tail node points back to the head',
      domains: ['data_structures', 'academic'],
      supportedOperations: ['insert', 'delete', 'search', 'display', 'menu'],
      representations: ['pointer_based'],
      algorithms: ['circular_linked_list_standard'],
      requiredStates: [],
      producedStates: ['CIRCULAR_LINKED_LIST_STRUCTURE'],
      constraints: { cyclic: true }
    });

    this.registerAlgorithm({
      id: 'circular_linked_list_standard',
      name: 'Standard Pointer Circular Linked List',
      aliases: ['circular_linked_list'],
      capabilityId: 'circular_linked_list',
      requiredComponents: ['cyclic_node_chain'],
      supportedMechanisms: ['pointer_based_cll'],
      preconditions: [],
      invariants: ['tail_next_equals_head'],
      postconditions: ['operation_completed'],
      complexity: { time: 'O(1) head/tail, O(N) search', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'doubly_circular_linked_list',
      canonicalName: 'Doubly Circular Linked List',
      parentId: 'linear_sequence_structure',
      aliases: [
        'doubly circular linked list',
        'circular doubly linked list',
        'doubly circular list',
        'circular doubly list',
        'dcll',
        'cdll'
      ],
      semanticDescription: 'Circular linked list with bidirectional prev and next pointers',
      domains: ['data_structures', 'academic'],
      supportedOperations: ['insert', 'delete', 'search', 'display', 'display_reverse', 'reverse', 'menu'],
      representations: ['pointer_based'],
      algorithms: ['doubly_circular_linked_list_standard'],
      requiredStates: [],
      producedStates: ['DOUBLY_CIRCULAR_LINKED_LIST_STRUCTURE'],
      constraints: { bidirectional: true, cyclic: true }
    });

    this.registerAlgorithm({
      id: 'doubly_circular_linked_list_standard',
      name: 'Standard Pointer Circular Doubly Linked List',
      aliases: ['doubly_circular_linked_list', 'circular_doubly_linked_list', 'dcll'],
      capabilityId: 'doubly_circular_linked_list',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_dll'],
      preconditions: [],
      invariants: ['bidirectional_cyclic_links_reciprocal'],
      postconditions: ['operation_completed'],
      complexity: { time: 'O(1) head/tail, O(N) search', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'polynomial',
      canonicalName: 'Polynomial Representation & Operations',
      parentId: 'linear_sequence_structure',
      aliases: [
        'polynomial',
        'polynomials',
        'polynomial addition',
        'polynomial multiplication',
        'polynomial linked list',
        'polynomial_linked_list'
      ],
      semanticDescription: 'Polynomial arithmetic represented as linked list of coefficient and exponent terms',
      domains: ['data_structures', 'academic', 'numerical'],
      supportedOperations: ['create', 'insert', 'add', 'multiply', 'evaluate', 'display', 'menu'],
      representations: ['pointer_based'],
      algorithms: ['polynomial_standard'],
      requiredStates: [],
      producedStates: ['POLYNOMIAL_STRUCTURE'],
      constraints: { ordered: true }
    });

    this.registerAlgorithm({
      id: 'polynomial_standard',
      name: 'Standard Linked List Polynomial Operations',
      aliases: ['polynomial', 'polynomial_standard', 'polynomial_linked_list'],
      capabilityId: 'polynomial',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['terms_ordered_by_exponent_descending'],
      postconditions: ['polynomial_evaluated_or_combined'],
      complexity: { time: 'O(M + N) addition, O(M * N) multiplication', space: 'O(M + N)' }
    });

    this.registerCapability({
      id: 'linked_list_cycle_detection',
      canonicalName: 'Linked List Cycle Detection',
      aliases: ['detect cycle', 'floyd cycle detection', 'detect cycle in', 'cycle detection', 'has cycle', 'detect loop'],
      semanticDescription: "Detects cycles in a singly linked list using Floyd's Tortoise and Hare algorithm",
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['detect', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['linked_list_cycle_detection_standard'],
      requiredStates: [],
      producedStates: ['CYCLE_STATUS'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'linked_list_cycle_detection_standard',
      name: 'Floyd Cycle Detection',
      aliases: ['detect cycle', 'floyd cycle detection', 'detect loop'],
      capabilityId: 'linked_list_cycle_detection',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['fast_moves_two_slow_moves_one'],
      postconditions: ['cycle_detected_or_null_reached'],
      complexity: { time: 'O(N)', space: 'O(1)' }
    });

    this.registerCapability({
      id: 'linked_list_cycle_start',
      canonicalName: 'Linked List Cycle Start Finding',
      aliases: ['find cycle start', 'detect loop starting point', 'find cycle beginning', 'cycle starting node'],
      semanticDescription: 'Finds the exact node where a cycle begins in a singly linked list',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['find', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['linked_list_cycle_start_standard'],
      requiredStates: [],
      producedStates: ['CYCLE_START_NODE'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'linked_list_cycle_start_standard',
      name: 'Floyd Cycle Start Finder',
      aliases: ['find cycle start', 'cycle starting node'],
      capabilityId: 'linked_list_cycle_start',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['slow_resets_to_head_and_both_advance_by_one'],
      postconditions: ['cycle_start_identified'],
      complexity: { time: 'O(N)', space: 'O(1)' }
    });

    this.registerCapability({
      id: 'linked_list_remove_cycle',
      canonicalName: 'Linked List Cycle Removal',
      aliases: ['remove cycle', 'remove cycle from', 'remove cycle linked', 'remove loop'],
      semanticDescription: 'Breaks the cycle in a singly linked list so it becomes a standard linear list',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['remove', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['linked_list_remove_cycle_standard'],
      requiredStates: [],
      producedStates: ['LINEAR_LIST'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'linked_list_remove_cycle_standard',
      name: 'Floyd Cycle Breaker',
      aliases: ['remove cycle', 'remove loop'],
      capabilityId: 'linked_list_remove_cycle',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['tail_pointer_reset_to_null'],
      postconditions: ['list_cycle_free'],
      complexity: { time: 'O(N)', space: 'O(1)' }
    });

    this.registerCapability({
      id: 'linked_list_middle',
      canonicalName: 'Linked List Middle Node Finding',
      aliases: ['find middle node', 'find middle element', 'middle node', 'middle of linked list'],
      semanticDescription: 'Finds the middle node of a singly linked list in a single pass using slow and fast pointers',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['find', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['linked_list_middle_standard'],
      requiredStates: [],
      producedStates: ['MIDDLE_NODE'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'linked_list_middle_standard',
      name: 'Two-Pointer Middle Node Finder',
      aliases: ['find middle node', 'middle node'],
      capabilityId: 'linked_list_middle',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['slow_advances_one_fast_advances_two'],
      postconditions: ['middle_node_found'],
      complexity: { time: 'O(N)', space: 'O(1)' }
    });

    this.registerCapability({
      id: 'linked_list_nth_from_end',
      canonicalName: 'Linked List Nth Node From End',
      aliases: ['nth node from', 'nth from end', 'kth node from end', 'kth from end'],
      semanticDescription: 'Finds or deletes the nth node from the end of a singly linked list in one pass',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['find', 'delete', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['linked_list_nth_from_end_standard'],
      requiredStates: [],
      producedStates: ['NTH_FROM_END_NODE'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'linked_list_nth_from_end_standard',
      name: 'Two-Pointer Nth Node From End Finder',
      aliases: ['nth from end', 'kth from end'],
      capabilityId: 'linked_list_nth_from_end',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['gap_between_pointers_is_n'],
      postconditions: ['nth_node_from_end_located'],
      complexity: { time: 'O(N)', space: 'O(1)' }
    });

    this.registerCapability({
      id: 'linked_list_palindrome',
      canonicalName: 'Linked List Palindrome Verification',
      aliases: ['check palindrome list', 'check if palindrome', 'palindrome linked list', 'linked list palindrome'],
      semanticDescription: 'Checks if values in a singly linked list read identically forward and backward',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['check', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['linked_list_palindrome_standard'],
      requiredStates: [],
      producedStates: ['PALINDROME_STATUS'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'linked_list_palindrome_standard',
      name: 'Half-Reversal Palindrome Checker',
      aliases: ['check palindrome list', 'palindrome linked list'],
      capabilityId: 'linked_list_palindrome',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['second_half_reversed_and_compared_with_first'],
      postconditions: ['palindrome_verified'],
      complexity: { time: 'O(N)', space: 'O(1)' }
    });

    this.registerCapability({
      id: 'linked_list_remove_duplicates',
      canonicalName: 'Linked List Duplicate Removal',
      aliases: ['remove duplicates from', 'remove duplicates linked list', 'delete duplicates'],
      semanticDescription: 'Eliminates duplicate values from a singly linked list',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['remove', 'delete', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['linked_list_remove_duplicates_standard'],
      requiredStates: [],
      producedStates: ['DEDUPLICATED_LIST'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'linked_list_remove_duplicates_standard',
      name: 'Linked List Duplicate Remover',
      aliases: ['remove duplicates from', 'delete duplicates'],
      capabilityId: 'linked_list_remove_duplicates',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['no_duplicate_adjacent_values'],
      postconditions: ['duplicates_removed'],
      complexity: { time: 'O(N) sorted, O(N) hash unsorted', space: 'O(1) sorted, O(N) unsorted' }
    });

    this.registerCapability({
      id: 'linked_list_merge_sorted',
      canonicalName: 'Merge Two Sorted Linked Lists',
      aliases: ['merge sorted lists', 'merge two sorted', 'merge sorted linked lists'],
      semanticDescription: 'Merges two individually sorted singly linked lists into a single sorted list',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['merge', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['linked_list_merge_sorted_standard'],
      requiredStates: [],
      producedStates: ['MERGED_SORTED_LIST'],
      constraints: { ordered: true }
    });

    this.registerAlgorithm({
      id: 'linked_list_merge_sorted_standard',
      name: 'Two-Way Sorted List Merger',
      aliases: ['merge sorted lists', 'merge two sorted'],
      capabilityId: 'linked_list_merge_sorted',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['merged_tail_always_takes_minimum_head'],
      postconditions: ['lists_merged_in_nondecreasing_order'],
      complexity: { time: 'O(M + N)', space: 'O(1)' }
    });

    this.registerCapability({
      id: 'linked_list_split_halves',
      canonicalName: 'Split Linked List into Two Halves',
      aliases: ['split into two', 'split linked list', 'split into two halves'],
      semanticDescription: 'Splits a singly linked list into two approximately equal sublists',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['split', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['linked_list_split_halves_standard'],
      requiredStates: [],
      producedStates: ['TWO_HALF_LISTS'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'linked_list_split_halves_standard',
      name: 'Slow-Fast Half Splitter',
      aliases: ['split into two', 'split linked list'],
      capabilityId: 'linked_list_split_halves',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['slow_terminates_first_half_tail'],
      postconditions: ['two_disjoint_halves_formed'],
      complexity: { time: 'O(N)', space: 'O(1)' }
    });

    this.registerCapability({
      id: 'linked_list_reverse_recursive',
      canonicalName: 'Recursive Linked List Reversal',
      aliases: ['reverse recursive', 'reverse linked list recursively', 'recursive reverse linked list'],
      semanticDescription: 'Reverses pointer links of a singly linked list using call-stack recursion',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['reverse', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['linked_list_reverse_recursive_standard'],
      requiredStates: [],
      producedStates: ['REVERSED_LIST'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'linked_list_reverse_recursive_standard',
      name: 'Recursive Pointer Inversion',
      aliases: ['reverse recursive', 'recursive reverse'],
      capabilityId: 'linked_list_reverse_recursive',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['sublist_reversed_and_tail_linked_to_head'],
      postconditions: ['entire_list_reversed'],
      complexity: { time: 'O(N)', space: 'O(N) call stack' }
    });

    this.registerCapability({
      id: 'linked_list_print_reverse',
      canonicalName: 'Print Linked List in Reverse Without Modifying',
      aliases: ['print in reverse', 'print reverse linked', 'print linked list in reverse without modifying'],
      semanticDescription: 'Prints nodes of a linked list in reverse order without modifying the list structure',
      domains: ['data_structures', 'academic', 'operations'],
      supportedOperations: ['display', 'print', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['linked_list_print_reverse_standard'],
      requiredStates: [],
      producedStates: ['OUTPUT_PRINTED'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'linked_list_print_reverse_standard',
      name: 'Recursive Non-destructive Reverse Printer',
      aliases: ['print in reverse', 'print reverse linked'],
      capabilityId: 'linked_list_print_reverse',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['tail_printed_before_head_returns'],
      postconditions: ['all_elements_displayed_reversed'],
      complexity: { time: 'O(N)', space: 'O(N) recursion' }
    });

    this.registerCapability({
      id: 'linked_list_rotate',
      canonicalName: 'Rotate Linked List by K Positions',
      aliases: ['rotate linked list', 'rotate by k', 'rotate list'],
      semanticDescription: 'Rotates elements of a linked list to the left or right by k positions',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['rotate', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['linked_list_rotate_standard'],
      requiredStates: [],
      producedStates: ['ROTATED_LIST'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'linked_list_rotate_standard',
      name: 'Circular Connect-Break List Rotator',
      aliases: ['rotate linked list', 'rotate by k'],
      capabilityId: 'linked_list_rotate',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['tail_connects_to_head_and_breaks_at_len_minus_k'],
      postconditions: ['list_rotated'],
      complexity: { time: 'O(N)', space: 'O(1)' }
    });

    this.registerCapability({
      id: 'linked_list_delete_all',
      canonicalName: 'Delete All Occurrences of Value in Linked List',
      aliases: ['delete all occurrences', 'delete all occurrences of value', 'delete all nodes with value'],
      semanticDescription: 'Deletes every node containing a target value from a singly linked list',
      domains: ['data_structures', 'academic', 'operations'],
      supportedOperations: ['delete', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['linked_list_delete_all_standard'],
      requiredStates: [],
      producedStates: ['PURGED_LIST'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'linked_list_delete_all_standard',
      name: 'Target Occurrence Purger',
      aliases: ['delete all occurrences'],
      capabilityId: 'linked_list_delete_all',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['all_matching_nodes_deallocated'],
      postconditions: ['zero_instances_of_val_remain'],
      complexity: { time: 'O(N)', space: 'O(1)' }
    });

    this.registerCapability({
      id: 'linked_list_delete_node_ptr',
      canonicalName: 'Delete Node Given Only a Pointer to It',
      aliases: ['delete without head', 'delete node without head', 'delete node given pointer'],
      semanticDescription: 'Deletes a node from a singly linked list given only a direct pointer to that node',
      domains: ['data_structures', 'academic', 'operations'],
      supportedOperations: ['delete', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['linked_list_delete_node_ptr_standard'],
      requiredStates: [],
      producedStates: ['NODE_REMOVED'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'linked_list_delete_node_ptr_standard',
      name: 'Next-Node Copy and Delete In-Place',
      aliases: ['delete without head', 'delete node given pointer'],
      capabilityId: 'linked_list_delete_node_ptr',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: ['target_node_is_not_tail'],
      invariants: ['data_copied_from_next_and_next_deleted'],
      postconditions: ['node_effectively_deleted'],
      complexity: { time: 'O(1)', space: 'O(1)' }
    });

    this.registerCapability({
      id: 'linked_list_sum',
      canonicalName: 'Sum and Aggregate Linked List Elements',
      aliases: ['sum of nodes', 'sum of list', 'sum linked list', 'sum and count linked list'],
      semanticDescription: 'Traverses a linked list and computes the arithmetic sum, count, and average of its values',
      domains: ['data_structures', 'academic', 'operations'],
      supportedOperations: ['sum', 'count', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['linked_list_sum_standard'],
      requiredStates: [],
      producedStates: ['AGGREGATION_RESULT'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'linked_list_sum_standard',
      name: 'Linear Node Accumulator',
      aliases: ['sum of nodes', 'sum linked list'],
      capabilityId: 'linked_list_sum',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['running_sum_accumulates_each_node_value'],
      postconditions: ['total_sum_computed'],
      complexity: { time: 'O(N)', space: 'O(1)' }
    });

    this.registerCapability({
      id: 'linked_list_add_two_numbers',
      canonicalName: 'Add Two Numbers Represented by Linked Lists',
      aliases: ['add two numbers', 'add two numbers linked list', 'add two numbers represented by linked lists'],
      semanticDescription: 'Sums two big numbers stored in reverse order in two linked lists with digit carry',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['add', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['linked_list_add_two_numbers_standard'],
      requiredStates: [],
      producedStates: ['SUM_LINKED_LIST'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'linked_list_add_two_numbers_standard',
      name: 'Digit-by-Digit Carry Adder',
      aliases: ['add two numbers', 'add two numbers linked list'],
      capabilityId: 'linked_list_add_two_numbers',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['carry_propagated_to_next_column'],
      postconditions: ['sum_list_constructed'],
      complexity: { time: 'O(max(N, M))', space: 'O(max(N, M))' }
    });

    this.registerCapability({
      id: 'student_records_linked_list',
      canonicalName: 'Student Records Management (Linked List)',
      aliases: ['student records', 'menu driven student records', 'student linked list', 'student record management'],
      semanticDescription: 'Maintains an interactive linked list database of student records (ID, name, GPA)',
      domains: ['data_structures', 'academic'],
      supportedOperations: ['insert', 'delete', 'search', 'display', 'menu', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['student_records_linked_list_standard'],
      requiredStates: [],
      producedStates: ['STUDENT_DATABASE'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'student_records_linked_list_standard',
      name: 'Student Record Node Chain',
      aliases: ['student records', 'student linked list'],
      capabilityId: 'student_records_linked_list',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['records_indexed_by_student_id'],
      postconditions: ['record_operation_completed'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'josephus_problem',
      canonicalName: 'Josephus Circle Elimination Problem',
      aliases: ['josephus problem', 'josephus circle', 'josephus problem circular', 'josephus problem using', 'circle elimination'],
      semanticDescription: 'Simulates the Josephus circle counting and elimination game using a circular linked list',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['simulate', 'solve'],
      representations: ['pointer_based'],
      algorithms: ['josephus_problem_standard'],
      requiredStates: [],
      producedStates: ['SURVIVOR_IDENTIFIED'],
      constraints: { cyclic: true }
    });

    this.registerAlgorithm({
      id: 'josephus_problem_standard',
      name: 'Circular List Josephus Simulator',
      aliases: ['josephus problem', 'josephus circle'],
      capabilityId: 'josephus_problem',
      requiredComponents: ['cyclic_node_chain'],
      supportedMechanisms: ['pointer_based_cll'],
      preconditions: ['n_positive', 'k_positive'],
      invariants: ['every_kth_node_deleted_until_one_remains'],
      postconditions: ['last_survivor_returned'],
      complexity: { time: 'O(N * K)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'stack',
      canonicalName: 'Stack (LIFO)',
      aliases: ['stack', 'stacks', 'lifo', 'stack_array', 'stack array', 'array stack'],
      semanticDescription: 'Last-in, first-out container supporting push, pop, and top',
      domains: ['data_structures', 'academic', 'linear_storage'],
      supportedOperations: ['push', 'pop', 'peek', 'top', 'display', 'menu'],
      representations: ['array_based', 'pointer_based', 'stl'],
      algorithms: ['stack_standard'],
      requiredStates: [],
      producedStates: ['STACK_STRUCTURE'],
      constraints: { discipline: 'lifo' }
    });

    this.registerAlgorithm({
      id: 'stack_standard',
      name: 'Standard LIFO Stack',
      aliases: ['stack'],
      capabilityId: 'stack',
      requiredComponents: ['array_based_static'],
      supportedMechanisms: ['array_based_static', 'pointer_based_sll', 'stl_std_vector'],
      preconditions: [],
      invariants: ['top_always_points_to_latest_element'],
      postconditions: ['lifo_satisfied'],
      complexity: { time: 'O(1) push/pop/top', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'stack_linked_list',
      canonicalName: 'Stack (Linked List Implementation)',
      aliases: ['stack linked list', 'stack using linked list', 'linked list stack', 'stack_linked_list'],
      semanticDescription: 'Last-in, first-out container implemented via dynamically allocated linked nodes',
      domains: ['data_structures', 'academic'],
      supportedOperations: ['push', 'pop', 'peek', 'top', 'display', 'is_empty', 'size', 'menu'],
      representations: ['pointer_based'],
      algorithms: ['stack_linked_list_standard'],
      requiredStates: [],
      producedStates: ['STACK_STRUCTURE'],
      constraints: { discipline: 'lifo' }
    });

    this.registerAlgorithm({
      id: 'stack_linked_list_standard',
      name: 'Pointer-based Linked List Stack',
      aliases: ['stack_linked_list', 'stack using linked list'],
      capabilityId: 'stack_linked_list',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['top_always_points_to_head_node'],
      postconditions: ['lifo_satisfied'],
      complexity: { time: 'O(1) push/pop/peek', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'balanced_parentheses',
      canonicalName: 'Balanced Parentheses Verification',
      aliases: ['balanced parentheses', 'check balanced parentheses', 'check balanced brackets', 'valid parentheses', 'parentheses matching'],
      semanticDescription: 'Verifies whether bracket pairs in an expression are properly nested and balanced using a LIFO stack',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['check', 'solve', 'validate'],
      representations: ['stl', 'array_based', 'pointer_based'],
      algorithms: ['balanced_parentheses_standard'],
      requiredStates: [],
      producedStates: ['PARENTHESES_VALIDATED'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'balanced_parentheses_standard',
      name: 'Stack-based Parentheses Balance Checker',
      aliases: ['balanced_parentheses', 'check balanced parentheses', 'valid parentheses'],
      capabilityId: 'balanced_parentheses',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector', 'pointer_based_sll', 'array_based_static'],
      preconditions: [],
      invariants: ['open_brackets_stored_in_lifo_order'],
      postconditions: ['balance_evaluated'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'infix_to_postfix',
      canonicalName: 'Infix to Postfix Conversion',
      aliases: ['infix to postfix', 'convert infix to postfix', 'infix to postfix conversion', 'shunting yard'],
      semanticDescription: 'Converts standard infix arithmetic expressions into postfix (Reverse Polish) notation using operator precedence and stack',
      domains: ['data_structures', 'academic'],
      supportedOperations: ['convert', 'solve'],
      representations: ['stl'],
      algorithms: ['infix_to_postfix_standard'],
      requiredStates: [],
      producedStates: ['POSTFIX_EXPRESSION'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'infix_to_postfix_standard',
      name: 'Shunting-Yard Infix to Postfix Algorithm',
      aliases: ['infix_to_postfix', 'infix to postfix'],
      capabilityId: 'infix_to_postfix',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['operator_precedence_maintained_on_stack'],
      postconditions: ['postfix_string_produced'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'infix_to_prefix',
      canonicalName: 'Infix to Prefix Conversion',
      aliases: ['infix to prefix', 'convert infix to prefix', 'infix to prefix conversion'],
      semanticDescription: 'Converts infix expression to prefix notation by reversing, adjusting parentheses, and transforming via stack',
      domains: ['data_structures', 'academic'],
      supportedOperations: ['convert', 'solve'],
      representations: ['stl'],
      algorithms: ['infix_to_prefix_standard'],
      requiredStates: [],
      producedStates: ['PREFIX_EXPRESSION'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'infix_to_prefix_standard',
      name: 'Stack-based Infix to Prefix Algorithm',
      aliases: ['infix_to_prefix', 'infix to prefix'],
      capabilityId: 'infix_to_prefix',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['operator_precedence_maintained_on_stack'],
      postconditions: ['prefix_string_produced'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'postfix_evaluation',
      canonicalName: 'Postfix Expression Evaluation',
      aliases: ['postfix evaluation', 'evaluate postfix', 'evaluate postfix expression', 'postfix expression evaluation', 'rpn evaluation'],
      semanticDescription: 'Evaluates the numerical result of a postfix expression using an operand stack',
      domains: ['data_structures', 'academic'],
      supportedOperations: ['evaluate', 'solve', 'compute'],
      representations: ['stl'],
      algorithms: ['postfix_evaluation_standard'],
      requiredStates: [],
      producedStates: ['EVALUATION_RESULT'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'postfix_evaluation_standard',
      name: 'Stack-based Postfix Evaluator',
      aliases: ['postfix_evaluation', 'evaluate postfix'],
      capabilityId: 'postfix_evaluation',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['operands_popped_in_order_for_each_operator'],
      postconditions: ['single_result_on_stack'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'prefix_evaluation',
      canonicalName: 'Prefix Expression Evaluation',
      aliases: ['prefix evaluation', 'evaluate prefix', 'evaluate prefix expression', 'prefix expression evaluation'],
      semanticDescription: 'Evaluates the numerical result of a prefix expression scanning right to left using an operand stack',
      domains: ['data_structures', 'academic'],
      supportedOperations: ['evaluate', 'solve', 'compute'],
      representations: ['stl'],
      algorithms: ['prefix_evaluation_standard'],
      requiredStates: [],
      producedStates: ['EVALUATION_RESULT'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'prefix_evaluation_standard',
      name: 'Stack-based Prefix Evaluator',
      aliases: ['prefix_evaluation', 'evaluate prefix'],
      capabilityId: 'prefix_evaluation',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['operands_popped_in_order_for_each_operator'],
      postconditions: ['single_result_on_stack'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'reverse_string_stack',
      canonicalName: 'Reverse String Using Stack',
      aliases: ['reverse string stack', 'reverse string using stack', 'reverse a string using stack'],
      semanticDescription: 'Reverses characters in a string by pushing them onto a stack and popping in reverse order',
      domains: ['data_structures', 'academic'],
      supportedOperations: ['reverse', 'solve'],
      representations: ['stl'],
      algorithms: ['reverse_string_stack_standard'],
      requiredStates: [],
      producedStates: ['REVERSED_STRING'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'reverse_string_stack_standard',
      name: 'Stack String Reversal',
      aliases: ['reverse_string_stack', 'reverse string stack'],
      capabilityId: 'reverse_string_stack',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['chars_popped_in_reverse_order'],
      postconditions: ['string_reversed'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'decimal_to_binary_stack',
      canonicalName: 'Decimal to Binary Conversion Using Stack',
      aliases: ['decimal to binary stack', 'decimal to binary', 'convert decimal to binary using stack', 'decimal to binary using stack'],
      semanticDescription: 'Converts base-10 integer to binary by pushing remainders onto stack and popping from MSB to LSB',
      domains: ['data_structures', 'academic'],
      supportedOperations: ['convert', 'solve'],
      representations: ['stl'],
      algorithms: ['decimal_to_binary_stack_standard'],
      requiredStates: [],
      producedStates: ['BINARY_RESULT'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'decimal_to_binary_stack_standard',
      name: 'Stack Decimal to Binary Conversion',
      aliases: ['decimal_to_binary_stack', 'decimal to binary stack'],
      capabilityId: 'decimal_to_binary_stack',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['remainders_pushed_in_increasing_significance'],
      postconditions: ['binary_representation_produced'],
      complexity: { time: 'O(log N)', space: 'O(log N)' }
    });

    this.registerCapability({
      id: 'min_stack',
      canonicalName: 'Min Stack (O(1) Minimum Retrieval)',
      aliases: ['min stack', 'minimum stack', 'implement min stack', 'getmin stack', 'min stack getmin', 'stack with getmin'],
      semanticDescription: 'Stack data structure that supports push, pop, top, and retrieving the minimum element in O(1) time',
      domains: ['data_structures', 'academic'],
      supportedOperations: ['push', 'pop', 'get_min', 'peek', 'solve'],
      representations: ['stl'],
      algorithms: ['min_stack_standard'],
      requiredStates: [],
      producedStates: ['MIN_STACK_STRUCTURE'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'min_stack_standard',
      name: 'Dual-Stack Min Element Maintainer',
      aliases: ['min_stack', 'min stack'],
      capabilityId: 'min_stack',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['auxiliary_stack_tracks_current_minimum'],
      postconditions: ['o1_minimum_retrieval'],
      complexity: { time: 'O(1) all operations', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'two_stacks_array',
      canonicalName: 'Two Stacks in One Array',
      aliases: ['two stacks array', 'two stacks in one array', 'two stacks in a single array', '2 stacks in one array'],
      semanticDescription: 'Implements two independent stacks within a single fixed array from opposite ends',
      domains: ['data_structures', 'academic'],
      supportedOperations: ['push1', 'push2', 'pop1', 'pop2', 'display1', 'display2', 'solve'],
      representations: ['array_based'],
      algorithms: ['two_stacks_array_standard'],
      requiredStates: [],
      producedStates: ['TWO_STACKS_STRUCTURE'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'two_stacks_array_standard',
      name: 'Boundary-Opposing Two Stacks in Single Array',
      aliases: ['two_stacks_array', 'two stacks array'],
      capabilityId: 'two_stacks_array',
      requiredComponents: ['array_based_static'],
      supportedMechanisms: ['array_based_static'],
      preconditions: [],
      invariants: ['top1_increases_from_zero_and_top2_decreases_from_capacity'],
      postconditions: ['space_shared_optimally'],
      complexity: { time: 'O(1) push/pop for both stacks', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'queue_using_stacks',
      canonicalName: 'Queue Using Two Stacks',
      aliases: ['queue using stacks', 'queue using stack', 'queue using two stacks', 'implement queue using stacks'],
      semanticDescription: 'Implements a FIFO queue using two LIFO stacks with amortized O(1) dequeue',
      domains: ['data_structures', 'academic'],
      supportedOperations: ['enqueue', 'dequeue', 'peek', 'solve'],
      representations: ['stl'],
      algorithms: ['queue_using_stacks_standard'],
      requiredStates: [],
      producedStates: ['QUEUE_STRUCTURE'],
      constraints: { discipline: 'fifo' }
    });

    this.registerAlgorithm({
      id: 'queue_using_stacks_standard',
      name: 'Dual-Stack FIFO Queue Simulation',
      aliases: ['queue_using_stacks', 'queue using two stacks'],
      capabilityId: 'queue_using_stacks',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['elements_transferred_to_output_stack_on_demand'],
      postconditions: ['fifo_behavior_verified'],
      complexity: { time: 'O(1) enqueue, O(1) amortized dequeue', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'sort_stack',
      canonicalName: 'Sort Stack Using Recursion',
      aliases: ['sort stack', 'sort stack recursion', 'sort stack using recursion', 'reverse stack using recursion', 'sort a stack'],
      semanticDescription: 'Sorts elements of a stack using recursive calls and sorted insert without explicit auxiliary data structures',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['sort', 'solve'],
      representations: ['stl'],
      algorithms: ['sort_stack_standard'],
      requiredStates: [],
      producedStates: ['SORTED_STACK'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'sort_stack_standard',
      name: 'Recursive Stack Sorter',
      aliases: ['sort_stack', 'sort stack'],
      capabilityId: 'sort_stack',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['call_stack_retains_elements_for_sorted_insertion'],
      postconditions: ['stack_sorted_monotonically'],
      complexity: { time: 'O(N^2)', space: 'O(N) recursion stack' }
    });

    this.registerCapability({
      id: 'reverse_stack',
      canonicalName: 'Reverse Stack Using Recursion',
      aliases: ['reverse_stack', 'reverse stack', 'reverse stack recursion'],
      semanticDescription: 'Reverses a stack recursively using bottom-insertion helper',
      domains: ['data_structures', 'academic', 'linear_storage'],
      supportedOperations: ['reverse'],
      representations: ['stl'],
      algorithms: ['reverse_stack_standard'],
      requiredStates: [],
      producedStates: ['REVERSED_STACK'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'reverse_stack_standard',
      name: 'Recursive Stack Reverser',
      aliases: ['reverse_stack', 'reverse stack'],
      capabilityId: 'reverse_stack',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['recursive_bottom_insertion'],
      postconditions: ['stack_reversed'],
      complexity: { time: 'O(N^2)', space: 'O(N) call stack' }
    });

    this.registerCapability({
      id: 'delete_middle_stack',
      canonicalName: 'Delete Middle Element of Stack',
      aliases: ['delete_middle_stack', 'delete middle element of stack', 'delete middle stack', 'delete_middle'],
      semanticDescription: 'Deletes the middle element of a stack recursively',
      domains: ['data_structures', 'academic', 'linear_storage'],
      supportedOperations: ['delete'],
      representations: ['stl'],
      algorithms: ['delete_middle_stack_standard'],
      requiredStates: [],
      producedStates: ['MODIFIED_STACK'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'delete_middle_stack_standard',
      name: 'Stack Middle Deleter',
      aliases: ['delete_middle_stack'],
      capabilityId: 'delete_middle_stack',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['call_stack_retains_outer_elements'],
      postconditions: ['middle_element_deleted'],
      complexity: { time: 'O(N)', space: 'O(N) call stack' }
    });

    this.registerCapability({
      id: 'next_greater_element',
      canonicalName: 'Next Greater Element (NGE)',
      aliases: ['next_greater_element', 'next greater element', 'next_greater'],
      semanticDescription: 'Finds next greater element for each array item using monotonic stack',
      domains: ['data_structures', 'algorithms', 'linear_storage'],
      supportedOperations: ['query'],
      representations: ['stl'],
      algorithms: ['next_greater_element_standard'],
      requiredStates: [],
      producedStates: ['NGE_ARRAY'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'next_greater_element_standard',
      name: 'Monotonic Stack NGE',
      aliases: ['next_greater_element', 'next_greater'],
      capabilityId: 'next_greater_element',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['monotonic_decreasing_stack'],
      postconditions: ['next_greater_computed'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'next_smaller_element',
      canonicalName: 'Next Smaller Element (NSE)',
      aliases: ['next_smaller_element', 'next smaller element', 'next_smaller'],
      semanticDescription: 'Finds next smaller element for each array item using monotonic stack',
      domains: ['data_structures', 'algorithms', 'linear_storage'],
      supportedOperations: ['query'],
      representations: ['stl'],
      algorithms: ['next_smaller_element_standard'],
      requiredStates: [],
      producedStates: ['NSE_ARRAY'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'next_smaller_element_standard',
      name: 'Monotonic Stack NSE',
      aliases: ['next_smaller_element', 'next_smaller'],
      capabilityId: 'next_smaller_element',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['monotonic_increasing_stack'],
      postconditions: ['next_smaller_computed'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'previous_greater_element',
      canonicalName: 'Previous Greater Element (PGE)',
      aliases: ['previous_greater_element', 'previous greater element', 'previous_greater'],
      semanticDescription: 'Finds previous greater element using monotonic stack',
      domains: ['data_structures', 'algorithms', 'linear_storage'],
      supportedOperations: ['query'],
      representations: ['stl'],
      algorithms: ['previous_greater_element_standard'],
      requiredStates: [],
      producedStates: ['PGE_ARRAY'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'previous_greater_element_standard',
      name: 'Monotonic Stack PGE',
      aliases: ['previous_greater_element'],
      capabilityId: 'previous_greater_element',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['monotonic_decreasing_stack'],
      postconditions: ['previous_greater_computed'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'previous_smaller_element',
      canonicalName: 'Previous Smaller Element (PSE)',
      aliases: ['previous_smaller_element', 'previous smaller element', 'previous_smaller'],
      semanticDescription: 'Finds previous smaller element using monotonic stack',
      domains: ['data_structures', 'algorithms', 'linear_storage'],
      supportedOperations: ['query'],
      representations: ['stl'],
      algorithms: ['previous_smaller_element_standard'],
      requiredStates: [],
      producedStates: ['PSE_ARRAY'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'previous_smaller_element_standard',
      name: 'Monotonic Stack PSE',
      aliases: ['previous_smaller_element'],
      capabilityId: 'previous_smaller_element',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['monotonic_increasing_stack'],
      postconditions: ['previous_smaller_computed'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'stock_span',
      canonicalName: 'Stock Span Problem',
      aliases: ['stock_span', 'stock span', 'stock span problem', 'stock_span_problem'],
      semanticDescription: 'Computes consecutive smaller/equal price span for each day',
      domains: ['data_structures', 'algorithms', 'linear_storage'],
      supportedOperations: ['query'],
      representations: ['stl'],
      algorithms: ['stock_span_standard'],
      requiredStates: [],
      producedStates: ['SPAN_ARRAY'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'stock_span_standard',
      name: 'Monotonic Stock Span',
      aliases: ['stock_span'],
      capabilityId: 'stock_span',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['monotonic_index_stack'],
      postconditions: ['span_computed'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'largest_rectangle_histogram',
      canonicalName: 'Largest Rectangle in Histogram',
      aliases: ['largest_rectangle_histogram', 'largest rectangle in histogram', 'histogram largest rectangle', 'histogram_rectangle'],
      semanticDescription: 'Finds the maximum area rectangle in a histogram using stack',
      domains: ['data_structures', 'algorithms', 'linear_storage'],
      supportedOperations: ['query'],
      representations: ['stl'],
      algorithms: ['largest_rectangle_histogram_standard'],
      requiredStates: [],
      producedStates: ['MAX_AREA_VALUE'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'largest_rectangle_histogram_standard',
      name: 'Histogram Max Area Sorter',
      aliases: ['largest_rectangle_histogram'],
      capabilityId: 'largest_rectangle_histogram',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['monotonic_increasing_height_indices'],
      postconditions: ['max_histogram_area_computed'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'trapping_rain_water_stack',
      canonicalName: 'Trapping Rain Water (Stack Approach)',
      aliases: ['trapping_rain_water_stack', 'trapping rain water using stack', 'trapping rain water', 'trapping_rain_water'],
      semanticDescription: 'Calculates trapped rain water between elevation bars using monotonic stack',
      domains: ['data_structures', 'algorithms', 'linear_storage'],
      supportedOperations: ['query'],
      representations: ['stl'],
      algorithms: ['trapping_rain_water_stack_standard'],
      requiredStates: [],
      producedStates: ['WATER_VOLUME'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'trapping_rain_water_stack_standard',
      name: 'Monotonic Rain Water Trapper',
      aliases: ['trapping_rain_water_stack'],
      capabilityId: 'trapping_rain_water_stack',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['monotonic_decreasing_bars'],
      postconditions: ['trapped_water_computed'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'celebrity_problem',
      canonicalName: 'Celebrity Problem (Stack Approach)',
      aliases: ['celebrity_problem', 'celebrity problem using stack', 'celebrity problem', 'celebrity'],
      semanticDescription: 'Finds party celebrity known by all and knowing nobody in O(N)',
      domains: ['data_structures', 'algorithms', 'linear_storage'],
      supportedOperations: ['query'],
      representations: ['stl'],
      algorithms: ['celebrity_problem_standard'],
      requiredStates: [],
      producedStates: ['CELEBRITY_INDEX'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'celebrity_problem_standard',
      name: 'Stack Celebrity Solver',
      aliases: ['celebrity_problem'],
      capabilityId: 'celebrity_problem',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['pairwise_elimination'],
      postconditions: ['celebrity_verified'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'postfix_to_infix',
      canonicalName: 'Postfix to Infix Conversion',
      aliases: ['postfix_to_infix', 'postfix to infix', 'convert postfix to infix'],
      semanticDescription: 'Converts postfix expression into fully parenthesized infix expression',
      domains: ['data_structures', 'academic', 'parsing'],
      supportedOperations: ['convert'],
      representations: ['stl'],
      algorithms: ['postfix_to_infix_standard'],
      requiredStates: [],
      producedStates: ['INFIX_EXPRESSION'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'postfix_to_infix_standard',
      name: 'Postfix to Infix Converter',
      aliases: ['postfix_to_infix'],
      capabilityId: 'postfix_to_infix',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['operands_combined_with_operator'],
      postconditions: ['infix_built'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'prefix_to_infix',
      canonicalName: 'Prefix to Infix Conversion',
      aliases: ['prefix_to_infix', 'prefix to infix', 'convert prefix to infix'],
      semanticDescription: 'Converts prefix expression into fully parenthesized infix expression',
      domains: ['data_structures', 'academic', 'parsing'],
      supportedOperations: ['convert'],
      representations: ['stl'],
      algorithms: ['prefix_to_infix_standard'],
      requiredStates: [],
      producedStates: ['INFIX_EXPRESSION'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'prefix_to_infix_standard',
      name: 'Prefix to Infix Converter',
      aliases: ['prefix_to_infix'],
      capabilityId: 'prefix_to_infix',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['reverse_prefix_processing'],
      postconditions: ['infix_built'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'postfix_to_prefix',
      canonicalName: 'Postfix to Prefix Conversion',
      aliases: ['postfix_to_prefix', 'postfix to prefix', 'convert postfix to prefix'],
      semanticDescription: 'Converts postfix expression into prefix notation',
      domains: ['data_structures', 'academic', 'parsing'],
      supportedOperations: ['convert'],
      representations: ['stl'],
      algorithms: ['postfix_to_prefix_standard'],
      requiredStates: [],
      producedStates: ['PREFIX_EXPRESSION'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'postfix_to_prefix_standard',
      name: 'Postfix to Prefix Converter',
      aliases: ['postfix_to_prefix'],
      capabilityId: 'postfix_to_prefix',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['operands_prefixed_with_operator'],
      postconditions: ['prefix_built'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'prefix_to_postfix',
      canonicalName: 'Prefix to Postfix Conversion',
      aliases: ['prefix_to_postfix', 'prefix to postfix', 'convert prefix to postfix'],
      semanticDescription: 'Converts prefix expression into postfix notation',
      domains: ['data_structures', 'academic', 'parsing'],
      supportedOperations: ['convert'],
      representations: ['stl'],
      algorithms: ['prefix_to_postfix_standard'],
      requiredStates: [],
      producedStates: ['POSTFIX_EXPRESSION'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'prefix_to_postfix_standard',
      name: 'Prefix to Postfix Converter',
      aliases: ['prefix_to_postfix'],
      capabilityId: 'prefix_to_postfix',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['reverse_prefix_postfixed_with_operator'],
      postconditions: ['postfix_built'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'evaluate_infix',
      canonicalName: 'Infix Expression Evaluation',
      aliases: ['evaluate_infix', 'evaluate infix expression', 'evaluate infix', 'infix evaluation'],
      semanticDescription: 'Evaluates infix arithmetic expression in a single pass using two stacks',
      domains: ['data_structures', 'academic', 'parsing'],
      supportedOperations: ['evaluate'],
      representations: ['stl'],
      algorithms: ['evaluate_infix_standard'],
      requiredStates: [],
      producedStates: ['EVALUATION_RESULT'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'evaluate_infix_standard',
      name: 'Two-Stack Infix Evaluator',
      aliases: ['evaluate_infix'],
      capabilityId: 'evaluate_infix',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['operator_precedence_in_stack'],
      postconditions: ['expression_evaluated'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'redundant_brackets',
      canonicalName: 'Redundant Brackets Checker',
      aliases: ['redundant_brackets', 'check redundant brackets', 'redundant parentheses', 'redundant_parentheses'],
      semanticDescription: 'Checks if an algebraic expression has redundant or useless brackets',
      domains: ['data_structures', 'academic', 'parsing'],
      supportedOperations: ['validate'],
      representations: ['stl'],
      algorithms: ['redundant_brackets_standard'],
      requiredStates: [],
      producedStates: ['VALIDATION_BOOLEAN'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'redundant_brackets_standard',
      name: 'Stack Redundancy Checker',
      aliases: ['redundant_brackets'],
      capabilityId: 'redundant_brackets',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['bracket_scope_contains_operator'],
      postconditions: ['redundancy_determined'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'longest_valid_parentheses',
      canonicalName: 'Longest Valid Parentheses',
      aliases: ['longest_valid_parentheses', 'longest valid parentheses using stack'],
      semanticDescription: 'Calculates the length of the longest valid parentheses substring',
      domains: ['data_structures', 'algorithms', 'linear_storage'],
      supportedOperations: ['query'],
      representations: ['stl'],
      algorithms: ['longest_valid_parentheses_standard'],
      requiredStates: [],
      producedStates: ['LENGTH_INTEGER'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'longest_valid_parentheses_standard',
      name: 'Stack Parentheses Span Finder',
      aliases: ['longest_valid_parentheses'],
      capabilityId: 'longest_valid_parentheses',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['index_stack_tracks_valid_boundaries'],
      postconditions: ['max_valid_length_computed'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'stack_using_queues',
      canonicalName: 'Stack Using Two Queues',
      aliases: ['stack_using_queues', 'stack using two queues', 'stack using queues', 'stack_using_two_queues'],
      semanticDescription: 'Simulates LIFO stack using two FIFO queues',
      domains: ['data_structures', 'academic', 'linear_storage'],
      supportedOperations: ['push', 'pop', 'top', 'menu'],
      representations: ['stl'],
      algorithms: ['stack_using_queues_standard'],
      requiredStates: [],
      producedStates: ['SIMULATED_STACK'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'stack_using_queues_standard',
      name: 'Queue-based Stack Simulation',
      aliases: ['stack_using_queues'],
      capabilityId: 'stack_using_queues',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['queue_transfer_reverses_fifo'],
      postconditions: ['lifo_preserved'],
      complexity: { time: 'O(N) push, O(1) pop', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'k_stacks_array',
      canonicalName: 'K Stacks in One Array',
      aliases: ['k_stacks_array', 'k stacks in an array', 'k stacks', 'k_stacks'],
      semanticDescription: 'Maintains K independent stacks in a single array using free list',
      domains: ['data_structures', 'academic', 'linear_storage'],
      supportedOperations: ['push', 'pop', 'menu'],
      representations: ['array_based'],
      algorithms: ['k_stacks_array_standard'],
      requiredStates: [],
      producedStates: ['K_STACKS_STRUCTURE'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'k_stacks_array_standard',
      name: 'Free-List K Stacks',
      aliases: ['k_stacks_array'],
      capabilityId: 'k_stacks_array',
      requiredComponents: ['fixed_array_storage'],
      supportedMechanisms: ['array_based'],
      preconditions: [],
      invariants: ['free_list_links_available_slots'],
      postconditions: ['k_independent_lifo_maintained'],
      complexity: { time: 'O(1) push, O(1) pop', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'queue',
      canonicalName: 'Queue (FIFO)',
      aliases: ['queue', 'queues', 'fifo', 'linear queue', 'circular queue'],
      semanticDescription: 'First-in, first-out container supporting enqueue and dequeue',
      domains: ['data_structures', 'academic', 'linear_storage'],
      supportedOperations: ['enqueue', 'dequeue', 'peek', 'front', 'display', 'menu'],
      representations: ['array_based', 'pointer_based', 'stl'],
      algorithms: ['queue_standard'],
      requiredStates: [],
      producedStates: ['QUEUE_STRUCTURE'],
      constraints: { discipline: 'fifo' }
    });

    this.registerAlgorithm({
      id: 'queue_standard',
      name: 'Standard FIFO Queue',
      aliases: ['queue'],
      capabilityId: 'queue',
      requiredComponents: ['array_based_static'],
      supportedMechanisms: ['array_based_static', 'pointer_based_sll'],
      preconditions: [],
      invariants: ['front_always_points_to_oldest_element'],
      postconditions: ['fifo_satisfied'],
      complexity: { time: 'O(1) enqueue/dequeue', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'circular_queue',
      canonicalName: 'Circular Queue (Ring Buffer)',
      aliases: ['circular queue', 'circular_queue', 'ring buffer', 'circular buffer'],
      semanticDescription: 'Queue where last position connects back to the first position to make a circle',
      domains: ['data_structures', 'academic', 'linear_storage'],
      supportedOperations: ['enqueue', 'dequeue', 'peek', 'front', 'display', 'menu'],
      representations: ['array_based'],
      algorithms: ['circular_queue_standard'],
      requiredStates: [],
      producedStates: ['QUEUE_STRUCTURE'],
      constraints: { discipline: 'fifo', circular: true }
    });

    this.registerAlgorithm({
      id: 'circular_queue_standard',
      name: 'Circular Queue Ring Buffer',
      aliases: ['circular_queue', 'circular queue'],
      capabilityId: 'circular_queue',
      requiredComponents: ['array_based_static'],
      supportedMechanisms: ['array_based_static'],
      preconditions: [],
      invariants: ['front_and_rear_wrap_around_modulo_capacity'],
      postconditions: ['fifo_satisfied'],
      complexity: { time: 'O(1) enqueue/dequeue', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'linear_queue',
      canonicalName: 'Linear Queue (Array-based)',
      aliases: ['linear queue', 'linear_queue', 'queue using array', 'queue_array'],
      semanticDescription: 'Linear FIFO queue with fixed-size array representation',
      domains: ['data_structures', 'academic', 'linear_storage'],
      supportedOperations: ['enqueue', 'dequeue', 'peek', 'front', 'display', 'menu'],
      representations: ['array_based'],
      algorithms: ['linear_queue_standard'],
      requiredStates: [],
      producedStates: ['QUEUE_STRUCTURE'],
      constraints: { discipline: 'fifo' }
    });

    this.registerAlgorithm({
      id: 'linear_queue_standard',
      name: 'Linear Array Queue',
      aliases: ['linear_queue', 'queue_array'],
      capabilityId: 'linear_queue',
      requiredComponents: ['array_based_static'],
      supportedMechanisms: ['array_based_static'],
      preconditions: [],
      invariants: ['front_and_rear_bounded_by_capacity'],
      postconditions: ['fifo_satisfied'],
      complexity: { time: 'O(1) enqueue/dequeue', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'queue_linked_list',
      canonicalName: 'Queue (Linked List Implementation)',
      aliases: ['queue linked list', 'queue using linked list', 'linked list queue', 'queue_linked_list'],
      semanticDescription: 'FIFO queue implemented using singly linked list with front and rear pointers',
      domains: ['data_structures', 'academic', 'linear_storage'],
      supportedOperations: ['enqueue', 'dequeue', 'peek', 'front', 'display', 'menu'],
      representations: ['pointer_based'],
      algorithms: ['queue_linked_list_standard'],
      requiredStates: [],
      producedStates: ['QUEUE_STRUCTURE'],
      constraints: { discipline: 'fifo' }
    });

    this.registerAlgorithm({
      id: 'queue_linked_list_standard',
      name: 'Linked List FIFO Queue',
      aliases: ['queue_linked_list', 'queue using linked list'],
      capabilityId: 'queue_linked_list',
      requiredComponents: ['linked_node_chain'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['rear_points_to_tail_front_points_to_head'],
      postconditions: ['fifo_satisfied'],
      complexity: { time: 'O(1) enqueue/dequeue', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'deque',
      canonicalName: 'Double-Ended Queue (Deque)',
      aliases: ['deque', 'double ended queue', 'deques'],
      semanticDescription: 'Double-ended queue allowing insertion and deletion at both ends',
      domains: ['data_structures', 'academic', 'linear_storage'],
      supportedOperations: ['insert_front', 'insert_rear', 'delete_front', 'delete_rear', 'get_front', 'get_rear', 'display', 'menu'],
      representations: ['array_based', 'stl'],
      algorithms: ['deque_standard'],
      requiredStates: [],
      producedStates: ['QUEUE_STRUCTURE'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'deque_standard',
      name: 'Circular Array Deque',
      aliases: ['deque', 'double_ended_queue'],
      capabilityId: 'deque',
      requiredComponents: ['array_based_static'],
      supportedMechanisms: ['array_based_static'],
      preconditions: [],
      invariants: ['front_and_rear_wrap_both_directions'],
      postconditions: ['deque_satisfied'],
      complexity: { time: 'O(1) insert/delete at both ends', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'priority_queue',
      canonicalName: 'Priority Queue (Heap-based)',
      aliases: ['priority queue', 'priority_queue', 'priority_queue_array', 'binary heap priority queue'],
      semanticDescription: 'Queue where each element has an associated priority and element with highest/lowest priority is served first',
      domains: ['data_structures', 'academic', 'linear_storage'],
      supportedOperations: ['insert', 'extract_min', 'extract_max', 'peek', 'display', 'menu'],
      representations: ['array_based', 'stl'],
      algorithms: ['priority_queue_standard'],
      requiredStates: [],
      producedStates: ['QUEUE_STRUCTURE'],
      constraints: { priority_discipline: true }
    });

    this.registerAlgorithm({
      id: 'priority_queue_standard',
      name: 'Array-based Priority Queue / Heap',
      aliases: ['priority_queue', 'priority_queue_standard'],
      capabilityId: 'priority_queue',
      requiredComponents: ['array_based_static'],
      supportedMechanisms: ['array_based_static'],
      preconditions: [],
      invariants: ['elements_ordered_by_priority'],
      postconditions: ['priority_satisfied'],
      complexity: { time: 'O(N) or O(log N) insert/delete', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'reverse_queue',
      canonicalName: 'Reverse Queue',
      aliases: ['reverse queue', 'reverse_queue', 'reverse a queue', 'reverse queue using recursion', 'reverse queue using stack'],
      semanticDescription: 'Reverses the sequence of elements in a FIFO queue using recursion or an auxiliary stack',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['reverse', 'solve'],
      representations: ['array_based', 'stl'],
      algorithms: ['reverse_queue_standard'],
      requiredStates: [],
      producedStates: ['QUEUE_REVERSED'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'reverse_queue_standard',
      name: 'Queue Reversal via Recursion / Stack',
      aliases: ['reverse_queue'],
      capabilityId: 'reverse_queue',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector', 'pointer_based_sll'],
      preconditions: [],
      invariants: ['all_elements_inverted_in_order'],
      postconditions: ['queue_reversed'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'reverse_first_k_queue',
      canonicalName: 'Reverse First K Elements of Queue',
      aliases: ['reverse first k elements of queue', 'reverse first k elements', 'reverse_first_k_queue'],
      semanticDescription: 'Reverses order of the first k elements of a queue while keeping remainder unchanged',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['reverse_k', 'solve'],
      representations: ['array_based', 'stl'],
      algorithms: ['reverse_first_k_queue_standard'],
      requiredStates: [],
      producedStates: ['QUEUE_K_REVERSED'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'reverse_first_k_queue_standard',
      name: 'Queue First K Reversal using Stack',
      aliases: ['reverse_first_k_queue'],
      capabilityId: 'reverse_first_k_queue',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['first_k_reversed_remainder_preserved'],
      postconditions: ['queue_k_reversed'],
      complexity: { time: 'O(N)', space: 'O(k)' }
    });

    this.registerCapability({
      id: 'generate_binary_numbers',
      canonicalName: 'Generate Binary Numbers from 1 to N using Queue',
      aliases: ['generate binary numbers using queue', 'generate binary numbers', 'generate_binary_numbers'],
      semanticDescription: 'Generates binary numbers from 1 to N using BFS queue progression',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['generate', 'solve'],
      representations: ['stl', 'array_based'],
      algorithms: ['generate_binary_numbers_standard'],
      requiredStates: [],
      producedStates: ['BINARY_NUMBERS_GENERATED'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'generate_binary_numbers_standard',
      name: 'Queue-based Binary Number Generation',
      aliases: ['generate_binary_numbers'],
      capabilityId: 'generate_binary_numbers',
      requiredComponents: ['array_based_static'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['bfs_string_append_order'],
      postconditions: ['binary_numbers_printed'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'first_non_repeating_char',
      canonicalName: 'First Non-Repeating Character in Stream',
      aliases: ['first non repeating character', 'first non repeating character stream', 'first_non_repeating_char'],
      semanticDescription: 'Finds first non-repeating character dynamically as characters arrive in a stream using a queue and frequency map',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['find', 'solve'],
      representations: ['stl', 'array_based'],
      algorithms: ['first_non_repeating_char_standard'],
      requiredStates: [],
      producedStates: ['NON_REPEATING_FOUND'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'first_non_repeating_char_standard',
      name: 'Queue Stream Non-repeating Character Tracking',
      aliases: ['first_non_repeating_char'],
      capabilityId: 'first_non_repeating_char',
      requiredComponents: ['array_based_static'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['front_of_queue_contains_current_first_unique_char'],
      postconditions: ['stream_processed'],
      complexity: { time: 'O(N)', space: 'O(1) 256 chars' }
    });

    this.registerCapability({
      id: 'interleave_queue',
      canonicalName: 'Interleave First Half of Queue with Second Half',
      aliases: ['interleave queue', 'interleave first half with second', 'interleave_queue'],
      semanticDescription: 'Rearranges queue elements by interleaving the first half with the second half',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['interleave', 'solve'],
      representations: ['stl', 'array_based'],
      algorithms: ['interleave_queue_standard'],
      requiredStates: [],
      producedStates: ['QUEUE_INTERLEAVED'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'interleave_queue_standard',
      name: 'Queue Interleaving using Auxiliary Stack',
      aliases: ['interleave_queue'],
      capabilityId: 'interleave_queue',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['even_length_queue_halves_interleaved'],
      postconditions: ['queue_interleaved'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'sliding_window_maximum',
      canonicalName: 'Sliding Window Maximum (Maximum of All Subarrays of Size K)',
      aliases: ['sliding window maximum', 'sliding window max', 'sliding_window_maximum'],
      semanticDescription: 'Finds maximum element in each sliding window of size k across an array using a monotonic deque',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['solve', 'compute'],
      representations: ['stl', 'array_based'],
      algorithms: ['sliding_window_maximum_standard'],
      requiredStates: [],
      producedStates: ['WINDOW_MAXIMA_COMPUTED'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'sliding_window_maximum_standard',
      name: 'Monotonic Deque Sliding Window Maximum',
      aliases: ['sliding_window_maximum'],
      capabilityId: 'sliding_window_maximum',
      requiredComponents: ['array_based_static'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['deque_stores_indices_in_decreasing_order_of_values'],
      postconditions: ['all_window_maxima_produced'],
      complexity: { time: 'O(N)', space: 'O(K)' }
    });

    this.registerCapability({
      id: 'first_negative_window',
      canonicalName: 'First Negative Integer in Every Window of Size K',
      aliases: ['first negative integer in window', 'first negative window', 'first_negative_window'],
      semanticDescription: 'Finds first negative integer in every sliding window of size k using a queue',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['solve', 'compute'],
      representations: ['stl', 'array_based'],
      algorithms: ['first_negative_window_standard'],
      requiredStates: [],
      producedStates: ['WINDOW_NEGATIVES_COMPUTED'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'first_negative_window_standard',
      name: 'Queue-based First Negative Integer in Window',
      aliases: ['first_negative_window'],
      capabilityId: 'first_negative_window',
      requiredComponents: ['array_based_static'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['queue_maintains_indices_of_negative_elements_in_window'],
      postconditions: ['all_window_first_negatives_produced'],
      complexity: { time: 'O(N)', space: 'O(K)' }
    });

    this.registerCapability({
      id: 'circular_tour',
      canonicalName: 'Circular Tour / Petrol Pump Problem',
      aliases: ['circular tour', 'petrol pump tour', 'circular_tour', 'gas station'],
      semanticDescription: 'Finds starting petrol pump from which a truck can complete the entire circular tour without running out of fuel',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['solve', 'find'],
      representations: ['stl', 'array_based'],
      algorithms: ['circular_tour_standard'],
      requiredStates: [],
      producedStates: ['TOUR_START_FOUND'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'circular_tour_standard',
      name: 'Queue / Two-pointer Circular Tour Solver',
      aliases: ['circular_tour'],
      capabilityId: 'circular_tour',
      requiredComponents: ['array_based_static'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['balance_sum_tracks_surplus'],
      postconditions: ['starting_pump_determined'],
      complexity: { time: 'O(N)', space: 'O(1)' }
    });

    this.registerCapability({
      id: 'queue_sort_using_stack',
      canonicalName: 'Sort Queue using Stack',
      aliases: ['sort queue using stack', 'sort queue', 'queue_sort_using_stack'],
      semanticDescription: 'Sorts elements of a queue in ascending or descending order using an auxiliary stack',
      domains: ['data_structures', 'academic', 'algorithms'],
      supportedOperations: ['sort', 'solve'],
      representations: ['stl', 'array_based'],
      algorithms: ['queue_sort_using_stack_standard'],
      requiredStates: [],
      producedStates: ['QUEUE_SORTED'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'queue_sort_using_stack_standard',
      name: 'Auxiliary Stack Queue Sorter',
      aliases: ['queue_sort_using_stack'],
      capabilityId: 'queue_sort_using_stack',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['min_elements_repeatedly_placed_in_queue'],
      postconditions: ['queue_sorted'],
      complexity: { time: 'O(N^2)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'binary_tree',
      canonicalName: 'Binary Tree',
      aliases: ['binary tree'],
      semanticDescription: 'Hierarchical tree structure where each node has at most two children',
      domains: ['data_structures', 'academic'],
      supportedOperations: ['insert', 'traverse', 'inorder', 'preorder', 'postorder', 'search'],
      representations: ['pointer_based'],
      algorithms: ['binary_tree_standard'],
      requiredStates: [],
      producedStates: ['BINARY_TREE_STRUCTURE'],
      constraints: { acyclic: true, max_degree: 2 }
    });

    this.registerAlgorithm({
      id: 'binary_tree_standard',
      name: 'Pointer-based Binary Tree',
      aliases: ['binary_tree'],
      capabilityId: 'binary_tree',
      requiredComponents: ['tree_node_links'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['node_children_count_at_most_2'],
      postconditions: ['traversed'],
      complexity: { time: 'O(N) traversal', space: 'O(H)' }
    });

    this.registerCapability({
      id: 'binary_search_tree',
      canonicalName: 'Binary Search Tree (BST)',
      aliases: ['binary search tree', 'bst'],
      semanticDescription: 'Binary tree where left subtree contains values smaller and right larger than parent',
      domains: ['data_structures', 'academic'],
      supportedOperations: ['insert', 'delete', 'search', 'inorder', 'traverse', 'menu'],
      representations: ['pointer_based'],
      algorithms: ['bst_standard'],
      requiredStates: [],
      producedStates: ['BST_STRUCTURE'],
      constraints: { ordered: true, binary_search_property: true }
    });

    this.registerAlgorithm({
      id: 'bst_standard',
      name: 'Standard Binary Search Tree',
      aliases: ['bst'],
      capabilityId: 'binary_search_tree',
      requiredComponents: ['tree_node_links'],
      supportedMechanisms: ['pointer_based_sll'],
      preconditions: [],
      invariants: ['left_val_lt_parent', 'right_val_gt_parent'],
      postconditions: ['inorder_sorted'],
      complexity: { time: 'O(H) search/insert, O(N) worst case', space: 'O(H)' }
    });

    // ── GRAPH ALGORITHMS ──
    this.registerCapability({
      id: 'single_source_shortest_path',
      canonicalName: 'Single Source Shortest Path',
      parentId: 'shortest_path',
      aliases: ['shortest path', 'minimum cost path', 'shortest path from source', 'find shortest path', 'cheapest path'],
      semanticDescription: 'Computes minimal distances from a single source vertex to all vertices in a graph',
      domains: ['graph_algorithms', 'shortest_path', 'competitive_programming'],
      supportedOperations: ['solve', 'compute', 'find', 'calculate'],
      representations: ['stl', 'array_based'],
      algorithms: ['dijkstra', 'bfs_shortest_path', 'bellman_ford'],
      requiredStates: ['GRAPH_ADJACENCY', 'SOURCE_VERTEX'],
      producedStates: ['SHORTEST_PATH_DISTANCES', 'PREDECESSOR_MAP'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'dijkstra',
      name: "Dijkstra's Shortest Path Algorithm",
      aliases: ['dijkstra', 'dijkstra algorithm', 'dijkstras algorithm', 'dijkstra shortest path', 'cf_dijkstra_shortest_path'],
      capabilityId: 'single_source_shortest_path',
      requiredComponents: ['priority_queue', 'edge_relaxation'],
      supportedMechanisms: ['binary_heap_std'],
      preconditions: ['non_negative_edge_weights', 'source_exists'],
      invariants: ['triangle_inequality_holds', 'visited_vertex_distance_is_optimal'],
      postconditions: ['all_reachable_distances_minimal'],
      complexity: { time: 'O((V + E) log V)', space: 'O(V + E)' }
    });

    this.registerAlgorithm({
      id: 'bfs_shortest_path',
      name: 'Breadth-First Search Unit-Weight Shortest Path',
      aliases: ['bfs shortest path', 'unweighted shortest path', 'graph bfs shortest path', 'breadth first search shortest path', 'shortest path in unweighted graph', 'shortest path using bfs', 'shortest path bfs'],
      capabilityId: 'single_source_shortest_path',
      requiredComponents: ['fifo_storage', 'edge_relaxation'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: ['unweighted_or_unit_weights', 'source_exists'],
      invariants: ['queue_distances_monotonic'],
      postconditions: ['all_reachable_distances_minimal'],
      complexity: { time: 'O(V + E)', space: 'O(V)' }
    });

    this.registerAlgorithm({
      id: 'bellman_ford',
      name: 'Bellman-Ford Shortest Path Algorithm',
      aliases: ['bellman ford', 'bellman-ford algorithm'],
      capabilityId: 'single_source_shortest_path',
      requiredComponents: ['edge_relaxation'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: ['no_negative_cycles_reachable_from_source'],
      invariants: ['k_th_iteration_distance_optimal_for_paths_len_le_k'],
      postconditions: ['all_distances_minimal_or_negative_cycle_flagged'],
      complexity: { time: 'O(V * E)', space: 'O(V)' }
    });

    this.registerCapability({
      id: 'graph_traversal',
      canonicalName: 'Graph Traversal',
      aliases: ['graph traversal', 'traverse graph', 'traversal', 'traverse'],
      semanticDescription: 'Visits all vertices in connected graph components',
      domains: ['graph_algorithms'],
      supportedOperations: ['traverse', 'visit', 'search'],
      representations: ['stl'],
      algorithms: ['graph_bfs', 'graph_dfs'],
      requiredStates: ['GRAPH_ADJACENCY', 'START_VERTEX'],
      producedStates: ['VISITED_SET'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'graph_bfs',
      name: 'Breadth-First Search Traversal',
      aliases: ['bfs', 'breadth first search', 'bfs traversal', 'breadth first search traversal'],
      capabilityId: 'graph_traversal',
      requiredComponents: ['fifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['level_by_level_exploration'],
      postconditions: ['all_connected_vertices_visited'],
      complexity: { time: 'O(V + E)', space: 'O(V)' }
    });

    this.registerAlgorithm({
      id: 'graph_dfs',
      name: 'Depth-First Search Traversal',
      aliases: ['dfs', 'depth first search', 'dfs traversal', 'depth first search traversal'],
      capabilityId: 'graph_traversal',
      requiredComponents: ['tree_node_links'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['depth_first_path_exploration'],
      postconditions: ['all_connected_vertices_visited'],
      complexity: { time: 'O(V + E)', space: 'O(V)' }
    });

    // ── NUMERICAL METHODS ──
    this.registerCapability({
      id: 'lu_decomposition',
      canonicalName: 'LU Matrix Decomposition',
      parentId: 'linear_system_solver',
      aliases: ['lu decomposition', 'lu factorization', 'lu dcomposition', 'doolittle', 'doolittle method', 'doolittle lu'],
      semanticDescription: 'Factorizes square matrix A into unit lower triangular matrix L and upper triangular matrix U',
      domains: ['numerical_methods', 'linear_algebra', 'academic'],
      supportedOperations: ['solve', 'compute', 'calculate', 'implement', 'decompose'],
      representations: ['matrix_dense'],
      algorithms: ['doolittle_lu'],
      requiredStates: ['COEFFICIENT_MATRIX_A', 'CONSTANT_VECTOR_B'],
      producedStates: ['LOWER_MATRIX_L', 'UPPER_MATRIX_U', 'SOLUTION_VECTOR_X'],
      constraints: { square_matrix: true, invertible: true }
    });

    this.registerAlgorithm({
      id: 'doolittle_lu',
      name: 'Doolittle Algorithm for LU Factorization',
      aliases: ['doolittle', 'lu_decomposition'],
      capabilityId: 'lu_decomposition',
      requiredComponents: ['pivoting', 'forward_substitution', 'back_substitution'],
      supportedMechanisms: ['dense_matrix_vector'],
      preconditions: ['square_matrix', 'non_singular_pivots'],
      invariants: ['A_equals_L_times_U', 'L_diagonal_is_one'],
      postconditions: ['system_solved_Ax_equals_b'],
      complexity: { time: 'O(N^3) factorization, O(N^2) substitutions', space: 'O(N^2)' }
    });

    this.registerCapability({
      id: 'gauss_elimination',
      canonicalName: 'Gaussian Elimination',
      parentId: 'linear_system_solver',
      aliases: ['gauss elimination', 'gaussian elimination', 'gauss elimination method', 'gaus elimination'],
      semanticDescription: 'Reduces augmented matrix to row echelon form with partial pivoting to solve linear systems',
      domains: ['numerical_methods', 'linear_algebra', 'academic'],
      supportedOperations: ['solve', 'compute', 'calculate', 'implement'],
      representations: ['matrix_dense'],
      algorithms: ['gauss_elimination_pivoting'],
      requiredStates: ['COEFFICIENT_MATRIX_A', 'CONSTANT_VECTOR_B'],
      producedStates: ['ROW_ECHELON_MATRIX', 'SOLUTION_VECTOR_X'],
      constraints: { square_matrix: true }
    });

    this.registerAlgorithm({
      id: 'gauss_elimination_pivoting',
      name: 'Gaussian Elimination with Partial Pivoting',
      aliases: ['gauss_elimination'],
      capabilityId: 'gauss_elimination',
      requiredComponents: ['pivoting', 'back_substitution'],
      supportedMechanisms: ['dense_matrix_vector'],
      preconditions: ['square_matrix', 'non_singular'],
      invariants: ['sub_diagonal_zeros_created'],
      postconditions: ['system_solved_Ax_equals_b'],
      complexity: { time: 'O(N^3)', space: 'O(N^2)' }
    });

    this.registerCapability({
      id: 'root_finding',
      canonicalName: 'Root Finding',
      aliases: ['root finding', 'find root', 'solve nonlinear equation', 'find zero of function'],
      semanticDescription: 'Finds x such that f(x) = 0 within prescribed tolerance',
      domains: ['numerical_methods', 'calculus', 'academic'],
      supportedOperations: ['solve', 'find', 'compute', 'calculate'],
      representations: ['custom_struct'],
      algorithms: ['bisection', 'newton_raphson', 'secant'],
      requiredStates: ['CONTINUOUS_FUNCTION_F'],
      producedStates: ['ROOT_APPROXIMATION'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'bisection',
      name: 'Bisection Method',
      aliases: ['bisection', 'bisection method', 'interval halving'],
      capabilityId: 'root_finding',
      requiredComponents: ['interval_bisection'],
      supportedMechanisms: ['array_based_static'],
      preconditions: ['continuous_function', 'opposite_signs_fA_fB_lt_0'],
      invariants: ['root_bracketed_in_interval'],
      postconditions: ['interval_width_le_tolerance'],
      complexity: { time: 'O(log((b-a)/tol)) iterations', space: 'O(1)' }
    });

    this.registerAlgorithm({
      id: 'newton_raphson',
      name: 'Newton-Raphson Method',
      aliases: ['newton raphson', 'newton-raphson method', 'newtons method'],
      capabilityId: 'root_finding',
      requiredComponents: ['interval_bisection'],
      supportedMechanisms: ['array_based_static'],
      preconditions: ['differentiable_function', 'derivative_nonzero_at_root'],
      invariants: ['quadratic_local_convergence'],
      postconditions: ['f_x_approx_zero'],
      complexity: { time: 'O(log(1/tol)) quadratic convergence', space: 'O(1)' }
    });

    this.registerAlgorithm({
      id: 'secant',
      name: 'Secant Method',
      aliases: ['secant', 'secant method'],
      capabilityId: 'root_finding',
      requiredComponents: ['interval_bisection'],
      supportedMechanisms: ['array_based_static'],
      preconditions: ['two_distinct_initial_guesses'],
      invariants: ['approximations_converge'],
      postconditions: ['root_computed'],
      complexity: { time: 'O(log N) iterations', space: 'O(1)' }
    });

    // ── COMPETITIVE PROGRAMMING / SEARCH & AGGREGATION ──
    this.registerCapability({
      id: 'prefix_sum',
      canonicalName: 'Prefix Sum Aggregation',
      parentId: 'range_aggregation',
      aliases: ['prefix sum', 'prefix sums', 'cumulative sum', 'range sum queries'],
      semanticDescription: 'Precomputes cumulative array to answer contiguous subsegment sum queries in O(1)',
      domains: ['algorithms', 'competitive_programming', 'data_structures'],
      supportedOperations: ['calculate', 'query', 'compute', 'solve'],
      representations: ['stl', 'array_based'],
      algorithms: ['prefix_sum_standard'],
      requiredStates: ['INPUT_SEQUENCE'],
      producedStates: ['PREFIX_SUM_ARRAY'],
      constraints: { static_array: true }
    });

    this.registerAlgorithm({
      id: 'prefix_sum_standard',
      name: 'Standard Prefix Sum Technique',
      aliases: ['prefix_sum'],
      capabilityId: 'prefix_sum',
      requiredComponents: ['prefix_sum_array'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: ['associative_invertible_operation'],
      invariants: ['prefix_i_equals_sum_0_to_i'],
      postconditions: ['subsegment_queries_o1'],
      complexity: { time: 'O(N) build, O(1) query', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'sort',
      canonicalName: 'Sequence Sorting',
      aliases: ['sort', 'sorting', 'order array', 'sorted order', 'sort an array'],
      semanticDescription: 'Arranges sequence elements in non-decreasing or non-increasing order',
      domains: ['algorithms', 'sorting', 'competitive_programming'],
      supportedOperations: ['sort', 'order', 'arrange'],
      representations: ['stl', 'array_based'],
      algorithms: ['standard_sort', 'bubble_sort', 'merge_sort', 'quick_sort'],
      requiredStates: ['INPUT_SEQUENCE'],
      producedStates: ['SORTED_SEQUENCE'],
      constraints: { comparison_defined: true }
    });

    this.registerAlgorithm({
      id: 'standard_sort',
      name: 'Standard Introsort / Quick-Sort',
      aliases: ['sort', 'std::sort', 'introsort'],
      capabilityId: 'sort',
      requiredComponents: ['interval_bisection'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: ['strict_weak_ordering'],
      invariants: ['elements_partitioned'],
      postconditions: ['all_elements_monotonic'],
      complexity: { time: 'O(N log N)', space: 'O(log N)' }
    });

    this.registerAlgorithm({
      id: 'bubble_sort',
      name: 'Bubble Sort',
      aliases: ['bubble sort'],
      capabilityId: 'sort',
      requiredComponents: ['array_based_static'],
      supportedMechanisms: ['array_based_static'],
      preconditions: [],
      invariants: ['suffix_is_sorted'],
      postconditions: ['array_fully_sorted'],
      complexity: { time: 'O(N^2)', space: 'O(1)' }
    });

    this.registerAlgorithm({
      id: 'merge_sort',
      name: 'Merge Sort',
      aliases: ['merge sort'],
      capabilityId: 'sort',
      requiredComponents: ['array_based_static'],
      supportedMechanisms: ['array_based_static', 'stl_std_vector'],
      preconditions: [],
      invariants: ['subarrays_sorted_before_merge'],
      postconditions: ['array_fully_sorted'],
      complexity: { time: 'O(N log N)', space: 'O(N)' }
    });

    this.registerAlgorithm({
      id: 'quick_sort',
      name: 'Quick Sort',
      aliases: ['quick sort'],
      capabilityId: 'sort',
      requiredComponents: ['array_based_static'],
      supportedMechanisms: ['array_based_static'],
      preconditions: [],
      invariants: ['elements_left_of_pivot_le', 'elements_right_of_pivot_ge'],
      postconditions: ['array_fully_sorted'],
      complexity: { time: 'O(N log N) expected', space: 'O(log N)' }
    });

    this.registerCapability({
      id: 'binary_search',
      canonicalName: 'Binary Search',
      aliases: ['binary search', 'bsearch', 'locate in sorted array', 'binary search on answer'],
      semanticDescription: 'Searches for target value or optimal monotonic threshold in O(log N)',
      domains: ['algorithms', 'searching', 'competitive_programming'],
      supportedOperations: ['search', 'find', 'locate', 'solve'],
      representations: ['stl', 'array_based'],
      algorithms: ['binary_search_standard'],
      requiredStates: ['SORTED_SEQUENCE'],
      producedStates: ['SEARCH_TARGET_INDEX'],
      constraints: { monotonic_predicate: true }
    });

    this.registerAlgorithm({
      id: 'binary_search_standard',
      name: 'Binary Search in Ordered Domain',
      aliases: ['binary_search'],
      capabilityId: 'binary_search',
      requiredComponents: ['interval_bisection'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: ['monotonic_sequence_or_predicate'],
      invariants: ['target_bracketed_in_low_high'],
      postconditions: ['exact_or_lower_bound_found'],
      complexity: { time: 'O(log N)', space: 'O(1)' }
    });

    this.registerCapability({
      id: 'two_pointers',
      canonicalName: 'Two Pointers Technique',
      aliases: ['two pointers', 'two-pointers', 'pair with sum', 'pair sum'],
      semanticDescription: 'Advances two pointer positions simultaneously over sorted or partitioned sequences',
      domains: ['algorithms', 'competitive_programming'],
      supportedOperations: ['find', 'solve', 'pair'],
      representations: ['stl'],
      algorithms: ['two_pointers_standard'],
      requiredStates: ['SORTED_SEQUENCE'],
      producedStates: ['SATISFYING_PAIR_OR_BOUND'],
      constraints: { monotonic_movement: true }
    });

    this.registerAlgorithm({
      id: 'two_pointers_standard',
      name: 'Monotonic Two Pointers Walk',
      aliases: ['two_pointers'],
      capabilityId: 'two_pointers',
      requiredComponents: ['two_pointers_window'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: ['sorted_array_or_monotonic_window'],
      invariants: ['left_le_right', 'eliminated_prefixes_suboptimal'],
      postconditions: ['target_found_or_nonexistent'],
      complexity: { time: 'O(N)', space: 'O(1)' }
    });

    this.registerCapability({
      id: 'monotonic_stack',
      canonicalName: 'Monotonic Stack',
      aliases: ['monotonic stack', 'nearest smaller value', 'next greater element'],
      semanticDescription: 'Maintains monotonic stack for nearest smaller or larger element queries',
      domains: ['algorithms', 'competitive_programming', 'data_structures'],
      supportedOperations: ['find', 'compute', 'solve'],
      representations: ['stl'],
      algorithms: ['monotonic_stack_standard'],
      requiredStates: ['INPUT_SEQUENCE'],
      producedStates: ['NEAREST_BOUNDS_ARRAY'],
      constraints: {}
    });

    this.registerAlgorithm({
      id: 'monotonic_stack_standard',
      name: 'Standard Monotonic Stack',
      aliases: ['monotonic_stack'],
      capabilityId: 'monotonic_stack',
      requiredComponents: ['monotonic_envelope'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: [],
      invariants: ['stack_elements_strictly_monotonic'],
      postconditions: ['all_nearest_bounds_computed'],
      complexity: { time: 'O(N)', space: 'O(N)' }
    });

    this.registerCapability({
      id: 'trie',
      canonicalName: 'Trie / Prefix Tree',
      aliases: ['trie', 'prefix tree', 'radix tree', 'dictionary tree'],
      semanticDescription: 'Tree structure for efficient retrieval of keys in a dataset of strings or bit prefixes',
      domains: ['data_structures', 'strings', 'competitive_programming'],
      supportedOperations: ['insert', 'search', 'starts_with', 'solve'],
      representations: ['pointer_based', 'array_based'],
      algorithms: ['trie_standard'],
      requiredStates: [],
      producedStates: ['TRIE_INDEX'],
      constraints: { finite_alphabet: true }
    });

    this.registerAlgorithm({
      id: 'trie_standard',
      name: 'Standard 26-way or Binary Trie',
      aliases: ['trie'],
      capabilityId: 'trie',
      requiredComponents: ['tree_node_links'],
      supportedMechanisms: ['pointer_based_sll', 'array_based_static'],
      preconditions: ['string_keys_in_valid_alphabet'],
      invariants: ['path_from_root_spells_prefix'],
      postconditions: ['keys_indexed_for_prefix_search'],
      complexity: { time: 'O(L) per operation', space: 'O(Sigma * total_chars)' }
    });

    // ── Additional Graph Capabilities to complete 21-capability inventory ──
    this.registerCapability({
      id: 'topological_sort',
      canonicalName: 'Topological Sort',
      aliases: ['topological sort', 'topological ordering', 'topo sort', 'topological'],
      semanticDescription: 'Linear ordering of vertices in a DAG such that for every directed edge uv, u comes before v',
      domains: ['graph_algorithms', 'competitive_programming'],
      supportedOperations: ['sort', 'order', 'solve'],
      representations: ['stl'],
      algorithms: ['kahn_algorithm', 'dfs_topological_sort'],
      requiredStates: ['DIRECTED_GRAPH'],
      producedStates: ['TOPOLOGICAL_ORDER'],
      constraints: { acyclic: true }
    });

    this.registerAlgorithm({
      id: 'kahn_algorithm',
      name: 'Kahn BFS Topological Sort',
      aliases: ['kahn', 'kahn algorithm', 'bfs topological sort', 'kahn bfs', 'topological sort using bfs'],
      capabilityId: 'topological_sort',
      requiredComponents: ['fifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: ['directed_acyclic_graph'],
      invariants: ['zero_indegree_vertices_processed_first'],
      postconditions: ['linear_ordering_valid'],
      complexity: { time: 'O(V + E)', space: 'O(V)' }
    });

    this.registerAlgorithm({
      id: 'dfs_topological_sort',
      name: 'DFS Postorder Topological Sort',
      aliases: ['dfs topo', 'dfs topological sort', 'topological sort using dfs', 'dfs postorder'],
      capabilityId: 'topological_sort',
      requiredComponents: ['lifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: ['directed_acyclic_graph'],
      invariants: ['finished_vertices_pushed_to_result'],
      postconditions: ['linear_ordering_valid'],
      complexity: { time: 'O(V + E)', space: 'O(V)' }
    });

    this.registerCapability({
      id: 'minimum_spanning_tree',
      canonicalName: 'Minimum Spanning Tree (MST)',
      aliases: ['minimum spanning tree', 'mst', 'kruskal', 'prim'],
      semanticDescription: 'Subset of edges that connects all vertices together without cycles and with the minimum total edge weight',
      domains: ['graph_algorithms', 'competitive_programming'],
      supportedOperations: ['find', 'compute', 'solve'],
      representations: ['stl'],
      algorithms: ['kruskal', 'prim'],
      requiredStates: ['WEIGHTED_CONNECTED_GRAPH'],
      producedStates: ['MST_EDGE_SET'],
      constraints: { connected: true, undirected: true }
    });

    this.registerAlgorithm({
      id: 'kruskal',
      name: 'Kruskal Algorithm with DSU',
      aliases: ['kruskal', 'kruskal algorithm'],
      capabilityId: 'minimum_spanning_tree',
      requiredComponents: ['disjoint_set_union'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: ['undirected_weighted_graph'],
      invariants: ['forest_of_minimum_weight_edges'],
      postconditions: ['spanning_tree_weight_minimal'],
      complexity: { time: 'O(E log E)', space: 'O(V)' }
    });

    this.registerAlgorithm({
      id: 'prim',
      name: 'Prim Algorithm with Priority Queue',
      aliases: ['prim', 'prim algorithm'],
      capabilityId: 'minimum_spanning_tree',
      requiredComponents: ['priority_queue'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: ['undirected_weighted_graph'],
      invariants: ['tree_grows_by_minimal_cut_edge'],
      postconditions: ['spanning_tree_weight_minimal'],
      complexity: { time: 'O((V + E) log V)', space: 'O(V)' }
    });

    this.registerCapability({
      id: 'connected_components',
      canonicalName: 'Connected Components',
      aliases: ['connected components', 'graph connectivity', 'find components'],
      semanticDescription: 'Partitions undirected graph vertices into maximal connected subgraphs',
      domains: ['graph_algorithms', 'competitive_programming'],
      supportedOperations: ['find', 'count', 'label', 'solve'],
      representations: ['stl'],
      algorithms: ['bfs_connected_components', 'dsu_connected_components'],
      requiredStates: ['UNDIRECTED_GRAPH'],
      producedStates: ['COMPONENT_LABELS'],
      constraints: { undirected: true }
    });

    this.registerAlgorithm({
      id: 'bfs_connected_components',
      name: 'BFS Connected Components',
      aliases: ['bfs connected components', 'connected components using bfs'],
      capabilityId: 'connected_components',
      requiredComponents: ['fifo_storage'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: ['undirected_graph'],
      invariants: ['unvisited_vertex_spawns_new_component'],
      postconditions: ['all_vertices_labeled_by_component'],
      complexity: { time: 'O(V + E)', space: 'O(V)' }
    });

    this.registerAlgorithm({
      id: 'dsu_connected_components',
      name: 'DSU Connected Components',
      aliases: ['dsu connected components', 'connected components using dsu', 'connected components using disjoint set union'],
      capabilityId: 'connected_components',
      requiredComponents: ['disjoint_set_union'],
      supportedMechanisms: ['stl_std_vector'],
      preconditions: ['undirected_graph'],
      invariants: ['edges_merge_component_sets'],
      postconditions: ['disjoint_sets_reflect_connectivity'],
      complexity: { time: 'O(E alpha(V))', space: 'O(V)' }
    });

    // ── Hierarchy Root Nodes ──
    this.registerHierarchyNode({
      id: 'data_structures',
      name: 'Data Structures',
      children: ['linear_data_structures', 'trees'],
      associatedCapabilities: ['singly_linked_list', 'doubly_linked_list', 'circular_linked_list', 'doubly_circular_linked_list', 'stack', 'stack_linked_list', 'queue', 'binary_tree', 'bst', 'trie', 'polynomial']
    });

    this.registerHierarchyNode({
      id: 'algorithms',
      name: 'Algorithms',
      children: ['graph_algorithms', 'sorting_searching'],
      associatedCapabilities: ['single_source_shortest_path', 'graph_traversal', 'binary_search', 'sort', 'topological_sort', 'minimum_spanning_tree', 'connected_components']
    });

    this.registerHierarchyNode({
      id: 'numerical_methods',
      name: 'Numerical Methods',
      children: ['linear_systems', 'root_finding'],
      associatedCapabilities: ['lu_decomposition', 'gauss_elimination', 'root_finding']
    });

    this.registerHierarchyNode({
      id: 'competitive_programming',
      name: 'Competitive Programming Patterns',
      children: ['range_queries', 'pointer_techniques'],
      associatedCapabilities: ['prefix_sum', 'two_pointers', 'binary_search', 'monotonic_stack', 'trie', 'topological_sort', 'minimum_spanning_tree']
    });
  }
}

/** Global singleton authoritative instance */
export const CAPABILITY_REGISTRY = new AuthoritativeCapabilityRegistry();
