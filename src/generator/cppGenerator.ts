/**
 * CodeForge V1 C++ Code Generator.
 * Routes resolution results to the correct verified module template
 * and assembles complete C++ programs via the code composer.
 */

import { ResolutionResult } from '../models/problemSpec';
import { composeCode, CodeFragment } from './codeComposer';

// Data Structures
import { singlyLinkedList } from './modules/data_structures/singlyLinkedList';
import { doublyLinkedList } from './modules/data_structures/doublyLinkedList';
import { circularLinkedList } from './modules/data_structures/circularLinkedList';
import { stack } from './modules/data_structures/stack';
import { queue } from './modules/data_structures/queue';
import { deque } from './modules/data_structures/deque';
import { binaryTree } from './modules/data_structures/binaryTree';
import { bst } from './modules/data_structures/bst';
import { heap } from './modules/data_structures/heap';
import { hashTable } from './modules/data_structures/hashTable';
import { graph } from './modules/data_structures/graph';
import { arrays } from './modules/data_structures/arrays';

// Algorithms
import { searching } from './modules/algorithms/searching';
import { sorting } from './modules/algorithms/sorting';

// Numerical Methods
import { rootFinding } from './modules/numerical/rootFinding';
import { linearSystems } from './modules/numerical/linearSystems';
import { interpolation } from './modules/numerical/interpolation';
import { differentiationModules } from './modules/numerical/differentiation';
import { integrationModules } from './modules/numerical/integration';
import { regressionModules } from './modules/numerical/regression';
import { odeModules } from './modules/numerical/ode';
import { eigenvaluesModules } from './modules/numerical/eigenvalues';

import { doublyCircularLinkedList } from './modules/data_structures/doublyCircularLinkedList';
import { stackLinkedList } from './modules/data_structures/stackLinkedList';
import { linearQueue } from './modules/data_structures/linearQueue';
import { queueLinkedList } from './modules/data_structures/queueLinkedList';
import { polynomial } from './modules/data_structures/polynomial';
import { stackApplications } from './modules/data_structures/stackApplications';
import { queueApplications } from './modules/data_structures/queueApplications';

// Registry mapping structure/category names to their module records
const dataStructureModules: Record<string, Record<string, () => CodeFragment>> = {
  'singly_linked_list': singlyLinkedList,
  'doubly_linked_list': doublyLinkedList,
  'circular_linked_list': circularLinkedList,
  'doubly_circular_linked_list': doublyCircularLinkedList,
  'circular_doubly_linked_list': doublyCircularLinkedList,
  'stack': stack,
  'stack_array': stack,
  'stack_linked_list': stackLinkedList,
  'stack_applications': stackApplications,
  'queue': queue,
  'circular_queue': queue,
  'linear_queue': linearQueue,
  'queue_linked_list': queueLinkedList,
  'queue_applications': queueApplications,
  'deque': deque,
  'double_ended_queue': deque,
  'priority_queue': queueApplications,
  'binary_tree': binaryTree,
  'bst': bst,
  'heap': heap,
  'hash_table': hashTable,
  'graph': graph,
  'array': arrays,
  'polynomial': polynomial,
};

const algorithmModules: Record<string, Record<string, () => CodeFragment>> = {
  'sorting': sorting,
  'searching': searching,
};

const numericalModules: Record<string, Record<string, () => CodeFragment>> = {
  'root_finding': rootFinding,
  'linear_systems': linearSystems,
  'interpolation': interpolation,
  'differentiation': differentiationModules,
  'integration': integrationModules,
  'regression': regressionModules,
  'ode': odeModules,
  'eigenvalues': eigenvaluesModules,
};

/**
 * Generate complete compilable C++ code from a resolution result.
 *
 * ModuleId patterns:
 *   Data structures: "{structure}.{operation}.cpp"    e.g. "singly_linked_list.insert_end.cpp"
 *   Algorithms:      "algorithm.{category}.{method}.cpp"  e.g. "algorithm.sorting.bubble_sort.cpp"
 *   Numerical:       "numerical.{category}.{method}.cpp"  e.g. "numerical.root_finding.bisection.cpp"
 */
import { buildScopedMenu } from './menuGenerator';

export function generateCpp(resolution: ResolutionResult): string {
  if (resolution.code !== 'SUCCESS') {
    return `// Code generation failed: ${resolution.message}`;
  }

  // Handle menu-driven program composition mode
  if (resolution.generationMode === 'menu') {
    const requestedOps = resolution.operations || resolution.spec.menu_operations;
    const target = resolution.spec.domain === 'numerical' ? 'numerical' : (resolution.spec.structure?.type || '');
    const menuCode = buildScopedMenu(target, requestedOps);
    if (menuCode) return menuCode;
  }

  const moduleId = resolution.moduleId;
  if (!moduleId) {
    return `// No moduleId provided in resolution result.`;
  }

  const parts = moduleId.replace('.cpp', '').split('.');

  let fragment: CodeFragment | null = null;

  if (parts[0] === 'algorithm' && parts.length >= 3) {
    // algorithm.sorting.bubble_sort
    const category = parts[1];
    const method = parts[2];
    const registry = algorithmModules[category];
    if (registry && registry[method]) {
      fragment = registry[method]();
    }
  } else if (parts[0] === 'numerical' && parts.length >= 3) {
    // numerical.root_finding.bisection
    const category = parts[1];
    const method = parts[2];
    const registry = numericalModules[category];
    if (registry && registry[method]) {
      fragment = registry[method]();
    }
  } else if (parts.length >= 2) {
    // singly_linked_list.insert_end
    const structure = parts[0];
    const operation = parts[1];
    const registry = dataStructureModules[structure];
    if (registry && registry[operation]) {
      fragment = registry[operation]();
    }
  }

  if (!fragment) {
    return `// Code generation for module "${moduleId}" is not yet implemented.`;
  }

  return composeCode([fragment]);
}
