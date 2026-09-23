/**
 * CHUP / Offcode — Classical Data Structure Backend (Phase 5)
 *
 * Provides execution infrastructure for foundational classical data structures
 * via the verified V1 generator.
 */

import { Backend, BackendDescriptor, BackendCompatibility, BackendExecutionResult } from '../../models/backendModel';
import { CapabilityPlan, CompositionStep } from '../../models/capabilityModel';
import { StructuredProblem } from '../../models/problemSpec';
import { CLASSICAL_DS_ADAPTER } from '../adapters/dataStructureAdapter';

export class ClassicalDataStructureBackend implements Backend {
  public readonly descriptor: BackendDescriptor = {
    id: 'classical_data_structure_backend',
    name: 'Classical Data Structure Backend',
    description: 'Verified pointer-based and array-based classical data structure implementations',
    supportedCapabilities: [
      'singly_linked_list',
      'doubly_linked_list',
      'circular_linked_list',
      'doubly_circular_linked_list',
      'polynomial',
      'stack',
      'stack_array',
      'stack_linked_list',
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
      'linked_list_cycle_detection',
      'linked_list_cycle_start',
      'linked_list_remove_cycle',
      'linked_list_middle',
      'linked_list_nth_from_end',
      'linked_list_palindrome',
      'linked_list_remove_duplicates',
      'linked_list_merge_sorted',
      'linked_list_split_halves',
      'linked_list_reverse_recursive',
      'linked_list_print_reverse',
      'linked_list_rotate',
      'linked_list_delete_all',
      'linked_list_delete_node_ptr',
      'linked_list_sum',
      'linked_list_add_two_numbers',
      'student_records_linked_list',
      'josephus_problem',
      'queue',
      'circular_queue',
      'linear_queue',
      'queue_linked_list',
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
      'binary_tree',
      'binary_search_tree',
      'heap',
      'hash_table',
      'sort'
    ],
    supportedAlgorithms: [
      'singly_linked_list_standard',
      'doubly_linked_list_standard',
      'circular_linked_list_standard',
      'doubly_circular_linked_list_standard',
      'polynomial_standard',
      'stack_standard',
      'stack_linked_list_standard',
      'balanced_parentheses_standard',
      'infix_to_postfix_standard',
      'infix_to_prefix_standard',
      'postfix_evaluation_standard',
      'prefix_evaluation_standard',
      'reverse_string_stack_standard',
      'decimal_to_binary_stack_standard',
      'min_stack_standard',
      'two_stacks_array_standard',
      'queue_using_stacks_standard',
      'sort_stack_standard',
      'reverse_stack_standard',
      'delete_middle_stack_standard',
      'next_greater_element_standard',
      'next_smaller_element_standard',
      'previous_greater_element_standard',
      'previous_smaller_element_standard',
      'stock_span_standard',
      'largest_rectangle_histogram_standard',
      'trapping_rain_water_stack_standard',
      'celebrity_problem_standard',
      'postfix_to_infix_standard',
      'prefix_to_infix_standard',
      'postfix_to_prefix_standard',
      'prefix_to_postfix_standard',
      'evaluate_infix_standard',
      'redundant_brackets_standard',
      'longest_valid_parentheses_standard',
      'stack_using_queues_standard',
      'k_stacks_array_standard',
      'linked_list_cycle_detection_standard',
      'linked_list_cycle_start_standard',
      'linked_list_remove_cycle_standard',
      'linked_list_middle_standard',
      'linked_list_nth_from_end_standard',
      'linked_list_palindrome_standard',
      'linked_list_remove_duplicates_standard',
      'linked_list_merge_sorted_standard',
      'linked_list_split_halves_standard',
      'linked_list_reverse_recursive_standard',
      'linked_list_print_reverse_standard',
      'linked_list_rotate_standard',
      'linked_list_delete_all_standard',
      'linked_list_delete_node_ptr_standard',
      'linked_list_sum_standard',
      'linked_list_add_two_numbers_standard',
      'student_records_linked_list_standard',
      'josephus_problem_standard',
      'queue_standard',
      'circular_queue_standard',
      'linear_queue_standard',
      'queue_linked_list_standard',
      'deque_standard',
      'priority_queue_standard',
      'reverse_queue_standard',
      'reverse_first_k_queue_standard',
      'generate_binary_numbers_standard',
      'first_non_repeating_char_standard',
      'interleave_queue_standard',
      'sliding_window_maximum_standard',
      'first_negative_window_standard',
      'circular_tour_standard',
      'queue_sort_using_stack_standard',
      'binary_tree_standard',
      'bst_standard',
      'bubble_sort',
      'quick_sort',
      'merge_sort'
    ],
    supportedComponents: [
      'sll_node',
      'dll_node',
      'cll_node',
      'binary_tree_node',
      'bst_node',
      'fixed_array_storage',
      'pointer_manipulation',
      'linked_node_chain',
      'cyclic_node_chain',
      'lifo_storage',
      'fifo_storage'
    ],
    supportedMechanisms: [
      'pointer_sll',
      'pointer_dll',
      'pointer_cll',
      'pointer_binary_tree',
      'pointer_bst',
      'cyclic_array_queue',
      'linear_array_stack',
      'pointer_based',
      'array_based',
      'pointer_based_sll',
      'pointer_based_dll',
      'pointer_based_cll',
      'array_based_static',
      'stl_std_vector'
    ],
    supportedRepresentations: [
      'pointer_based',
      'array_based',
      'custom_struct',
      'stl'
    ],
    supportedOperations: [
      'insert',
      'delete',
      'search',
      'display',
      'menu',
      'push',
      'pop',
      'peek',
      'enqueue',
      'dequeue',
      'traverse',
      'reverse',
      'sort',
      'evaluate',
      'convert',
      'simulate',
      'check',
      'merge',
      'split',
      'add',
      'multiply'
    ],
    availability: 'AVAILABLE',
    priority: 100, // High priority for explicit classical data structure problems
    version: '1.0.0'
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
    const missingMechs: string[] = [];

    // Check capability support
    if (!this.descriptor.supportedCapabilities.includes(currentStep.capabilityId)) {
      unsupportedReqs.push(`Capability '${currentStep.capabilityId}' not supported by classical DS backend`);
    }

    // Check implementation mechanism: if plan strictly requires STL and this is pointer_based
    const mech = currentStep.implementationMechanism;
    if (mech && mech.includes('stl') && !this.descriptor.supportedMechanisms.includes(mech)) {
      violatedConstraints.push(`Mechanism '${mech}' requires STL which is not supported by classical pointer-based backend`);
    }

    // Check representation
    const rep = currentStep.representationRequirements?.['representation'];
    if (rep && !this.descriptor.supportedRepresentations.includes(rep)) {
      violatedConstraints.push(`Representation requirement '${rep}' incompatible with classical DS backend`);
    }

    const compatible = unsupportedReqs.length === 0 && violatedConstraints.length === 0 && missingMechs.length === 0;

    return {
      compatible,
      unsupportedRequirements: unsupportedReqs,
      violatedConstraints,
      missingComponents: [],
      missingMechanisms: missingMechs,
      explanation: compatible
        ? 'Classical data structure backend is fully compatible with requested mechanism and representation'
        : `Incompatibility: ${[...unsupportedReqs, ...violatedConstraints].join('; ')}`
    };
  }

  public async execute(plan: CapabilityPlan, problem?: StructuredProblem): Promise<BackendExecutionResult> {
    const step = plan.compositionSteps[0];
    return CLASSICAL_DS_ADAPTER.execute(plan, step, problem);
  }
}

export const CLASSICAL_DS_BACKEND = new ClassicalDataStructureBackend();
