/**
 * CHUP / Offcode — Competitive Programming & Algorithmic Backend (Phase 5)
 *
 * Provides execution infrastructure for sequence algorithms, graph algorithms,
 * and string algorithms. Delegates to modular sub-adapters:
 * - SequenceAlgorithmAdapter
 * - GraphAlgorithmAdapter
 * - StringAlgorithmAdapter
 *
 * Invariants:
 * - Zero monolithic switch statements.
 * - Validates implementation-specific mechanism requirements.
 * - Reuses existing verified templates and graph builders.
 */

import { Backend, BackendDescriptor, BackendCompatibility, BackendExecutionResult } from '../../models/backendModel';
import { CapabilityPlan, CompositionStep } from '../../models/capabilityModel';
import { StructuredProblem } from '../../models/problemSpec';
import { SEQUENCE_ADAPTER } from '../adapters/cp/sequenceAdapter';
import { GRAPH_ADAPTER } from '../adapters/cp/graphAdapter';
import { STRING_ADAPTER } from '../adapters/cp/stringAdapter';

export class CPAlgorithmBackend implements Backend {
  public readonly descriptor: BackendDescriptor = {
    id: 'cp_algorithm_backend',
    name: 'Competitive Programming & Algorithmic Backend',
    description: 'Verified CP algorithms, parameterized templates, and graph solvers',
    supportedCapabilities: [
      'prefix_sum',
      'two_pointers',
      'binary_search',
      'monotonic_stack',
      'sort',
      'trie',
      'single_source_shortest_path',
      'graph_traversal',
      'topological_sort',
      'minimum_spanning_tree',
      'connected_components'
    ],
    supportedAlgorithms: [
      'prefix_sum_standard',
      'two_pointers_standard',
      'binary_search_standard',
      'monotonic_stack_standard',
      'standard_sort',
      'trie_standard',
      'dijkstra',
      'bfs_shortest_path',
      'graph_bfs',
      'graph_dfs',
      'kahn_algorithm',
      'kruskal',
      'prim',
      'bfs_connected_components',
      'dsu_connected_components'
    ],
    supportedComponents: [
      'priority_queue',
      'disjoint_set_union',
      'edge_relaxation',
      'prefix_array',
      'left_right_pointers',
      'search_interval',
      'lifo_stack',
      'trie_node'
    ],
    supportedMechanisms: [
      'stl_std_vector',
      'two_pointers_opposite',
      'two_pointers_same_direction',
      'monotonic_stack_vector',
      'binary_heap_std',
      'adj_list_vector',
      'dsu_array',
      'trie_node_array',
      'array_based',
      'stl'
    ],
    supportedRepresentations: [
      'stl',
      'array_based'
    ],
    supportedOperations: [
      'query',
      'update',
      'search',
      'sort',
      'traverse',
      'shortest_path',
      'mst',
      'components'
    ],
    availability: 'AVAILABLE',
    priority: 90,
    version: '2.0.0'
  };

  public checkCompatibility(plan: CapabilityPlan, step?: CompositionStep): BackendCompatibility {
    const currentStep = step || plan.compositionSteps[0];
    if (!currentStep) {
      return {
        compatible: false,
        unsupportedRequirements: ['No composition steps provided in plan'],
        violatedConstraints: [],
        missingComponents: [],
        missingMechanisms: [],
        explanation: 'Plan contains no composition steps'
      };
    }

    const unsupportedReqs: string[] = [];
    const violatedConstraints: string[] = [];

    // Check capability support
    if (!this.descriptor.supportedCapabilities.includes(currentStep.capabilityId)) {
      unsupportedReqs.push(`Capability '${currentStep.capabilityId}' not supported by CP backend`);
    }

    // Check implementation mechanism: if plan strictly requires manual pointer-based memory
    const rep = currentStep.representationRequirements?.['representation'];
    if (rep && (rep === 'pointer_based' || rep === 'manual')) {
      violatedConstraints.push(`Representation '${rep}' requires manual pointer management not provided by standard CP template backend`);
    }

    const mech = currentStep.implementationMechanism;
    if (mech && (mech.includes('pointer_sll') || mech.includes('pointer_dll'))) {
      violatedConstraints.push(`Mechanism '${mech}' requires explicit manual linked list node management`);
    }

    const compatible = unsupportedReqs.length === 0 && violatedConstraints.length === 0;

    return {
      compatible,
      unsupportedRequirements: unsupportedReqs,
      violatedConstraints,
      missingComponents: [],
      missingMechanisms: [],
      explanation: compatible
        ? 'CP Algorithm backend is fully compatible with requested algorithmic capability'
        : `Incompatibility: ${[...unsupportedReqs, ...violatedConstraints].join('; ')}`
    };
  }

  public async execute(plan: CapabilityPlan, problem?: StructuredProblem): Promise<BackendExecutionResult> {
    const step = plan.compositionSteps[0];
    const capId = step.capabilityId;

    // Delegate to modular sub-adapters
    if (['single_source_shortest_path', 'graph_traversal', 'topological_sort', 'minimum_spanning_tree', 'connected_components'].includes(capId)) {
      return GRAPH_ADAPTER.execute(plan, step, problem);
    }

    if (capId === 'trie') {
      return STRING_ADAPTER.execute(plan, step, problem);
    }

    // Sequence & Array capabilities
    return SEQUENCE_ADAPTER.execute(plan, step, problem);
  }
}

export const CP_ALGORITHM_BACKEND = new CPAlgorithmBackend();
