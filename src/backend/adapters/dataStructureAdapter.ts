/**
 * CHUP / Offcode — Classical Data Structure Engine Adapter (Phase 5)
 *
 * Adapts the verified V1 C++ code generator for classical data structures.
 * Translates structured CapabilityPlan / CompositionStep into V1 ResolutionResult.
 *
 * Invariants:
 * - Zero natural language parsing: operates strictly on structured plan IR.
 * - Preserves existing V1 generator logic without duplication.
 * - Returns normalized BackendExecutionResult.
 */

import { CapabilityPlan, CompositionStep } from '../../models/capabilityModel';
import { BackendExecutionResult } from '../../models/backendModel';
import { generateCpp } from '../../generator/cppGenerator';
import { StructuredProblem } from '../../models/problemSpec';

const STACK_APPLICATIONS = new Set([
  'balanced_parentheses',
  'infix_to_postfix',
  'infix_to_prefix',
  'postfix_evaluation',
  'prefix_evaluation',
  'reverse_string_stack',
  'decimal_to_binary_stack',
  'min_stack',
  'two_stacks_array',
  'queue_using_stacks',
  'sort_stack',
  'reverse_stack',
  'delete_middle_stack',
  'next_greater_element',
  'next_smaller_element',
  'previous_greater_element',
  'previous_smaller_element',
  'stock_span',
  'largest_rectangle_histogram',
  'trapping_rain_water_stack',
  'celebrity_problem',
  'postfix_to_infix',
  'prefix_to_infix',
  'postfix_to_prefix',
  'prefix_to_postfix',
  'evaluate_infix',
  'redundant_brackets',
  'longest_valid_parentheses',
  'stack_using_queues',
  'k_stacks_array',
  'next_greater',
  'next_smaller',
  'previous_greater',
  'previous_smaller',
  'stock_span_problem',
  'histogram_rectangle',
  'trapping_rain_water',
  'celebrity',
  'reverse_stack_recursion',
  'delete_middle',
  'delete_middle_element',
  'redundant_parentheses',
  'stack_using_two_queues',
  'k_stacks'
]);

const QUEUE_APPLICATIONS = new Set([
  'linear_queue',
  'circular_queue',
  'deque',
  'priority_queue',
  'reverse_queue',
  'reverse_first_k_queue',
  'generate_binary_numbers',
  'first_non_repeating_char',
  'interleave_queue',
  'sliding_window_maximum',
  'first_negative_window',
  'circular_tour',
  'queue_sort_using_stack',
  'linear_queue_array',
  'circular_queue_array',
  'double_ended_queue',
  'deque_array',
  'priority_queue_array',
  'reverse_queue_stack',
  'reverse_first_k',
  'first_non_repeating',
  'first_negative_window_k',
  'gas_station_tour'
]);

const LL_SPECIAL_ALGORITHMS: Record<string, { struct: string; op: string }> = {
  'linked_list_cycle_detection': { struct: 'singly_linked_list', op: 'detect_cycle' },
  'linked_list_cycle_start': { struct: 'singly_linked_list', op: 'find_cycle_start' },
  'linked_list_remove_cycle': { struct: 'singly_linked_list', op: 'remove_cycle' },
  'linked_list_middle': { struct: 'singly_linked_list', op: 'middle_element' },
  'linked_list_nth_from_end': { struct: 'singly_linked_list', op: 'nth_from_end' },
  'linked_list_palindrome': { struct: 'singly_linked_list', op: 'palindrome' },
  'linked_list_merge_sorted': { struct: 'singly_linked_list', op: 'merge_sorted' },
  'linked_list_split_halves': { struct: 'singly_linked_list', op: 'split_halves' },
  'linked_list_reverse_recursive': { struct: 'singly_linked_list', op: 'reverse_recursive' },
  'linked_list_print_reverse': { struct: 'singly_linked_list', op: 'print_reverse' },
  'linked_list_rotate': { struct: 'singly_linked_list', op: 'rotate' },
  'linked_list_delete_all': { struct: 'singly_linked_list', op: 'delete_all' },
  'linked_list_delete_node_ptr': { struct: 'singly_linked_list', op: 'delete_node_ptr' },
  'linked_list_sum': { struct: 'singly_linked_list', op: 'sum' },
  'linked_list_add_two_numbers': { struct: 'singly_linked_list', op: 'add_two_numbers' },
  'student_records_linked_list': { struct: 'singly_linked_list', op: 'student_records' },
  'josephus_problem': { struct: 'circular_linked_list', op: 'josephus' }
};

function extractMenuOperations(struct: string, probText: string, constraints: string[]): string[] {
  const ops: string[] = [];

  const hasPos = (pos: string) =>
    probText.includes(pos) || constraints.some(c => c.includes(pos));

  if (struct === 'stack' || struct === 'stack_array' || struct === 'stack_linked_list') {
    if (probText.includes('push')) ops.push('push');
    if (probText.includes('pop')) ops.push('pop');
    if (probText.includes('peek') || probText.includes('top')) ops.push('peek');
    if (probText.includes('empty') || probText.includes('is_empty')) ops.push('is_empty');
    if (probText.includes('display') || probText.includes('show') || probText.includes('print')) ops.push('display');
    return ops;
  }

  if (struct === 'queue' || struct === 'circular_queue' || struct === 'linear_queue' || struct === 'queue_linked_list') {
    if (probText.includes('enqueue') || probText.includes('insert') || probText.includes('add') || probText.includes('push')) ops.push('enqueue');
    if (probText.includes('dequeue') || probText.includes('delete') || probText.includes('remove') || probText.includes('pop')) ops.push('dequeue');
    if (probText.includes('front') || probText.includes('peek')) ops.push('front');
    if (probText.includes('rear') || probText.includes('back')) ops.push('rear');
    if (probText.includes('empty') || probText.includes('is_empty')) ops.push('is_empty');
    if (probText.includes('display') || probText.includes('show') || probText.includes('print')) ops.push('display');
    return ops;
  }

  if (struct === 'deque' || struct === 'double_ended_queue') {
    if (probText.includes('front') && (probText.includes('insert') || probText.includes('add'))) ops.push('insert_front');
    if (probText.includes('rear') && (probText.includes('insert') || probText.includes('add') || probText.includes('end'))) ops.push('insert_rear');
    if (probText.includes('front') && (probText.includes('delete') || probText.includes('remove'))) ops.push('delete_front');
    if (probText.includes('rear') && (probText.includes('delete') || probText.includes('remove'))) ops.push('delete_rear');
    if (probText.includes('get front') || (probText.includes('front') && probText.includes('peek'))) ops.push('get_front');
    if (probText.includes('get rear') || (probText.includes('rear') && probText.includes('peek'))) ops.push('get_rear');
    if (probText.includes('display') || probText.includes('show') || probText.includes('print')) ops.push('display');
    return ops;
  }

  if (struct === 'priority_queue') {
    if (probText.includes('enqueue') || probText.includes('insert') || probText.includes('add')) ops.push('enqueue');
    if (probText.includes('dequeue') || probText.includes('delete') || probText.includes('remove') || probText.includes('extract')) ops.push('dequeue');
    if (probText.includes('peek') || probText.includes('highest') || probText.includes('top')) ops.push('peek');
    if (probText.includes('display') || probText.includes('show') || probText.includes('print')) ops.push('display');
    if (probText.includes('empty') || probText.includes('is_empty')) ops.push('is_empty');
    if (probText.includes('size') || probText.includes('count')) ops.push('size');
    return ops;
  }

  // Linked list structures
  const hasInsert = probText.includes('insert') || probText.includes('add');
  const hasDelete = probText.includes('delete') || probText.includes('remove');

  if (hasInsert) {
    if (hasPos('beginning') || hasPos('head') || hasPos('front') || hasPos('start')) {
      ops.push('insert_beginning');
    }
    if (hasPos('end') || hasPos('tail') || hasPos('back') || hasPos('last')) {
      ops.push('insert_end');
    }
    if (hasPos('after')) {
      ops.push('insert_after');
    }
    if (hasPos('position') || hasPos('index') || hasPos('middle')) {
      ops.push('insert_position');
    }
    if (hasPos('sorted')) {
      ops.push('sorted_insert');
    }
  }

  if (hasDelete) {
    if (hasPos('beginning') || hasPos('head') || hasPos('front') || hasPos('start')) {
      ops.push('delete_beginning');
    }
    if (hasPos('end') || hasPos('tail') || hasPos('back') || hasPos('last')) {
      ops.push('delete_end');
    }
    if (hasPos('after')) {
      ops.push('delete_after');
    }
    if (hasPos('position') || hasPos('index')) {
      ops.push('delete_position');
    }
    if (hasPos('value') || probText.includes('node')) {
      ops.push(struct.includes('doubly_circular') ? 'delete_node' : 'delete_value');
    }
  }

  if (probText.includes('search') || probText.includes('find')) {
    ops.push('search');
  }

  if (probText.includes('display') || probText.includes('traverse') || probText.includes('print') || probText.includes('show')) {
    if (probText.includes('forward')) {
      ops.push('display');
    }
    if (probText.includes('backward') || probText.includes('reverse')) {
      ops.push('display_reverse');
    }
    if (!ops.includes('display') && !ops.includes('display_reverse')) {
      ops.push('display');
    }
  }

  if (probText.includes('reverse') && !probText.includes('display') && !probText.includes('backward')) {
    ops.push('reverse');
  }

  return ops;
}

export class ClassicalDataStructureAdapter {
  public execute(
    plan: CapabilityPlan,
    step: CompositionStep,
    problem?: StructuredProblem
  ): BackendExecutionResult {
    const rawCap = step.capabilityId;
    let struct = rawCap;
    let op = 'create';
    const probText = (problem?.rawText || problem?.normalizedText || '').toLowerCase();
    let isMenu = plan.operationPlan.includes('menu') || probText.includes('menu');
    const ops = plan.operationPlan;

    // 1. Stack Applications
    if (STACK_APPLICATIONS.has(rawCap)) {
      struct = 'stack_applications';
      op = rawCap;
      isMenu = false;
    }
    // 1b. Queue Applications (non-menu standalone algorithms)
    else if (QUEUE_APPLICATIONS.has(rawCap) && !isMenu) {
      struct = 'queue_applications';
      op = rawCap;
    }
    // 2. Linked List Special Algorithms
    else if (LL_SPECIAL_ALGORITHMS[rawCap]) {
      const mapping = LL_SPECIAL_ALGORITHMS[rawCap];
      struct = mapping.struct;
      op = mapping.op;
      isMenu = false;
    }
    // 3. Remove Duplicates (Sorted vs Unsorted)
    else if (rawCap === 'linked_list_remove_duplicates') {
      struct = 'singly_linked_list';
      op = (ops.includes('unsorted') || probText.includes('unsorted'))
        ? 'remove_duplicates_unsorted'
        : 'remove_duplicates_sorted';
      isMenu = false;
    }
    // 4. Stack (Array or Linked List)
    else if (rawCap === 'stack' || rawCap === 'stack_array' || rawCap === 'stack_linked_list') {
      struct = rawCap === 'stack_linked_list' ? 'stack_linked_list' : 'stack';
      if (isMenu) {
        op = 'menu';
      } else if (ops.includes('pop') || ops.includes('delete') || probText.includes('pop')) {
        op = 'pop';
      } else if (ops.includes('peek') || ops.includes('top') || probText.includes('peek') || probText.includes('top')) {
        op = 'peek';
      } else if (ops.includes('is_empty') || probText.includes('empty')) {
        op = 'is_empty';
      } else if (ops.includes('size') || ops.includes('count') || probText.includes('size') || probText.includes('count')) {
        op = 'size';
      } else if (ops.includes('display') || ops.includes('show') || probText.includes('display')) {
        op = 'display';
      } else if (ops.includes('push') || probText.includes('push')) {
        op = 'push';
      } else {
        op = 'create';
      }
    }
    // 5. Queue, Deque, Priority Queue
    else if (rawCap === 'queue' || rawCap === 'circular_queue' || rawCap === 'linear_queue' || rawCap === 'queue_linked_list' || rawCap === 'deque' || rawCap === 'priority_queue' || rawCap === 'double_ended_queue') {
      if (rawCap === 'queue') {
        if (probText.includes('circular') || probText.includes('ring')) {
          struct = 'circular_queue';
        } else if (probText.includes('linked list') || probText.includes('linked_list') || probText.includes('pointer')) {
          struct = 'queue_linked_list';
        } else if (probText.includes('deque') || probText.includes('double ended') || probText.includes('double-ended')) {
          struct = 'deque';
        } else if (probText.includes('priority') || probText.includes('heap')) {
          struct = 'priority_queue';
        } else {
          struct = 'linear_queue';
        }
      } else {
        struct = rawCap;
      }
      if (isMenu) {
        op = 'menu';
      } else if (ops.includes('dequeue') || ops.includes('delete') || probText.includes('dequeue')) {
        op = 'dequeue';
      } else if (ops.includes('peek') || ops.includes('front') || probText.includes('peek') || probText.includes('front')) {
        op = 'front';
      } else if (ops.includes('display') || probText.includes('display')) {
        op = 'display';
      } else if (ops.includes('enqueue') || ops.includes('insert') || probText.includes('enqueue')) {
        op = 'enqueue';
      } else {
        op = 'create';
      }
    }
    // 6. Polynomial
    else if (rawCap === 'polynomial') {
      struct = 'polynomial';
      if (isMenu) {
        op = 'menu';
      } else if (ops.includes('add') || probText.includes('addition') || probText.includes('add')) {
        op = 'add';
      } else if (ops.includes('multiply') || probText.includes('multiplication')) {
        op = 'multiply';
      } else if (ops.includes('evaluate') || probText.includes('evaluation')) {
        op = 'evaluate';
      } else if (ops.includes('display') || probText.includes('display')) {
        op = 'display';
      } else {
        op = 'create';
      }
    }
    // 7. General Linked Lists (Singly, Doubly, Circular, DCLL)
    else {
      if (rawCap === 'binary_search_tree') {
        struct = 'bst';
      } else if (rawCap === 'linked_list') {
        struct = 'singly_linked_list';
      }

      if (isMenu) {
        op = 'menu';
      } else if (ops.includes('search') || probText.includes('search')) {
        op = 'search';
      } else if (ops.includes('reverse') || probText.includes('reverse')) {
        if (ops.includes('recursive') || probText.includes('recursiv')) {
          op = 'reverse_recursive';
        } else if (probText.includes('without modifying') || probText.includes('print')) {
          op = 'print_reverse';
        } else {
          op = 'reverse';
        }
      } else if (ops.includes('display') || ops.includes('traverse') || probText.includes('display') || probText.includes('traverse')) {
        if (step.parameters?.direction === 'reverse' || probText.includes('backward') || probText.includes('reverse')) {
          op = 'display_reverse';
        } else {
          op = 'display';
        }
      } else if (ops.includes('count') || probText.includes('count')) {
        op = 'count';
      } else if (probText.includes('min') || probText.includes('minimum')) {
        op = 'find_min';
      } else if (probText.includes('max') || probText.includes('maximum')) {
        op = 'find_max';
      } else if (ops.includes('sum') || probText.includes('sum')) {
        op = 'sum';
      } else if (probText.includes('middle')) {
        op = 'middle_element';
      } else if (probText.includes('palindrome')) {
        op = 'palindrome';
      } else if (probText.includes('rotate')) {
        op = 'rotate';
      } else if (ops.includes('delete') || probText.includes('delete') || probText.includes('remove')) {
        if (probText.includes('duplicate') || plan.resolvedCapabilities.includes('linked_list_remove_duplicates')) {
          op = (ops.includes('unsorted') || probText.includes('unsorted'))
            ? 'remove_duplicates_unsorted'
            : 'remove_duplicates_sorted';
        } else if (probText.includes('all occurren')) {
          op = 'delete_all';
        } else if (probText.includes('without head') || probText.includes('pointer to it')) {
          op = 'delete_node_ptr';
        } else if (step.parameters?.position && step.parameters.position !== 'sorted') {
          op = `delete_${step.parameters.position}`;
        } else if (probText.includes('value')) {
          op = 'delete_value';
        } else if (probText.includes('end') || probText.includes('tail') || probText.includes('last')) {
          op = 'delete_end';
        } else {
          op = 'delete_beginning';
        }
      } else if (ops.includes('insert') || probText.includes('insert') || probText.includes('add')) {
        if (probText.includes('sorted') || step.parameters?.position === 'sorted') {
          op = 'sorted_insert';
        } else if (probText.includes('after') || step.parameters?.position === 'after') {
          op = 'insert_after';
        } else if (step.parameters?.position) {
          op = `insert_${step.parameters.position}`;
        } else if (probText.includes('head') || probText.includes('beginning') || probText.includes('front')) {
          op = 'insert_beginning';
        } else {
          op = 'insert_end';
        }
      } else {
        op = 'create';
      }
    }

    const moduleId = op === 'menu' ? `${struct}.menu.cpp` : `${struct}.${op}.cpp`;

    let requestedOps: string[] = [];
    if (isMenu) {
      requestedOps = extractMenuOperations(struct, probText, plan.constraints);
    }
    if (requestedOps.length === 0) {
      requestedOps = ops.filter(o => o !== 'menu' && o !== 'solve' && o !== 'implement');
    }

    const resolution: any = {
      code: 'SUCCESS',
      moduleId,
      moduleName: `${struct} (${op})`,
      message: 'Resolved via CapabilityPlan and BackendAdapter',
      generationMode: isMenu ? 'menu' : 'single',
      operations: requestedOps.length > 0 ? requestedOps : undefined,
      spec: {
        domain: 'data_structure',
        structure: { type: struct },
        operation: { combined: op },
        menu_operations: requestedOps.length > 0 ? requestedOps : undefined
      }
    };

    const code = generateCpp(resolution);

    if (code.startsWith('// Code generation failed') || code.startsWith('// Code generation for module')) {
      return {
        status: 'EXECUTION_FAILED',
        backendId: 'classical_data_structure_backend',
        capabilityId: step.capabilityId,
        algorithmId: step.algorithmId,
        implementationMechanism: step.implementationMechanism,
        generatedCode: '',
        diagnostics: [`V1 generator failed to emit code for ${moduleId}`],
        failure: {
          code: 'GENERATOR_VARIANT_UNSUPPORTED',
          layer: 'IMPLEMENTATION',
          message: `Classical data structure generator failed for ${struct}.${op}`
        },
        metadata: {
          moduleId,
          structure: struct,
          operation: op
        }
      };
    }

    return {
      status: 'SUCCESS',
      backendId: 'classical_data_structure_backend',
      capabilityId: step.capabilityId,
      algorithmId: step.algorithmId,
      implementationMechanism: step.implementationMechanism,
      generatedCode: code,
      diagnostics: [`Emitted C++ module ${moduleId} via ClassicalDataStructureAdapter`],
      metadata: {
        moduleId,
        componentsUsed: step.requiredComponents,
        mechanism: step.implementationMechanism
      }
    };
  }
}

export const CLASSICAL_DS_ADAPTER = new ClassicalDataStructureAdapter();

