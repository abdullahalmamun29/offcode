/**
 * CHUP / Offcode — Semantic Extractor (Phase 3)
 *
 * Explicitly separates semantic extraction from lexical normalization and canonicalization.
 *
 * Responsibilities:
 * - Identifies computational entities (data structures, algorithms, numerical methods, mathematical objects).
 * - Identifies explicit operations (insert, delete, search, reverse, etc.).
 * - Identifies explicit user intent (implement, create, solve, calculate, etc.).
 * - Identifies explicit operational constraints (position, ordering, etc.).
 * - Strictly enforces: NO SEMANTIC INVENTION.
 *   - "insert" alone never invents a data structure or position.
 *   - "singly linked list" alone never invents an operation.
 *   - Missing evidence remains missing.
 * - Preserves provenance for every evidence item (sourceTokens, startToken, endToken).
 */

import {
  CanonicalTerm,
  CanonicalizedInput,
  ConstraintEvidence,
  EntityEvidence,
  EntityKind,
  IntentEvidence,
  NormalizedInput,
  NormalizedToken,
  OperationEvidence,
  SemanticInput
} from '../models/problemSpec';
import { canonicalize } from './canonicalizer';

// ── Vocabulary & Classification Maps ──────────────────────────────────────────

const DATA_STRUCTURE_SET = new Set([
  'singly_linked_list',
  'doubly_linked_list',
  'circular_linked_list',
  'doubly_circular_linked_list',
  'linked_list',
  'stack',
  'queue',
  'linear_queue',
  'circular_queue',
  'priority_queue',
  'deque',
  'queue_linked_list',
  'binary_search_tree',
  'binary_tree',
  'avl_tree',
  'red_black_tree',
  'b_tree',
  'heap',
  'min_heap',
  'max_heap',
  'hash_table',
  'hash_map',
  'hash_set',
  'trie',
  'prefix_tree',
  'graph',
  'tree',
  'forest',
  'array',
  'vector',
  'matrix',
  'polynomial',
  'stack_linked_list',
  'stack_array',
  'two_stacks_array',
  'min_stack',
  'student_records_linked_list',
  'queue_using_stacks',
  'stack_using_queues',
  'k_stacks_array',
  'disjoint_set',
  'dsu',
  'segment_tree',
  'fenwick_tree'
]);

const ALGORITHM_SET = new Set([
  'balanced_parentheses',
  'infix_to_postfix',
  'infix_to_prefix',
  'postfix_evaluation',
  'prefix_evaluation',
  'reverse_string_stack',
  'decimal_to_binary_stack',
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
  'reverse_queue',
  'reverse_first_k_queue',
  'generate_binary_numbers',
  'first_non_repeating_char',
  'interleave_queue',
  'sliding_window_maximum',
  'first_negative_window',
  'circular_tour',
  'queue_sort_using_stack',
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
  'josephus_problem',
  'binary_search',
  'linear_search',
  'bubble_sort',
  'insertion_sort',
  'selection_sort',
  'quick_sort',
  'merge_sort',
  'heap_sort',
  'radix_sort',
  'counting_sort',
  'two_pointers',
  'sliding_window',
  'prefix_sum',
  'dijkstra',
  'bellman_ford',
  'floyd_warshall',
  'kruskal',
  'prim',
  'bfs',
  'dfs',
  'topological_sort',
  'kadane',
  'knapsack',
  'lcs',
  'lis'
]);

const NUMERICAL_SET = new Set([
  'lu_decomposition',
  'gauss_elimination',
  'gauss_jordan',
  'bisection',
  'newton_raphson',
  'secant',
  'false_position',
  'jacobi',
  'gauss_seidel',
  'trapezoidal',
  'simpson',
  'simpson_one_third',
  'simpson_three_eighth',
  'euler',
  'runge_kutta',
  'runge_kutta_4',
  'lagrange',
  'power_method',
  'qr_decomposition',
  'cholesky',
  'regula_falsi'
]);

const MATHEMATICAL_OBJECT_SET = new Set([
  'node',
  'root',
  'leaf',
  'edge',
  'vertex',
  'vertices',
  'matrix',
  'matrices',
  'polynomial',
  'eigenvalue',
  'eigenvalues',
  'eigenvector',
  'eigenvectors',
  'determinant',
  'inverse',
  'system',
  'equation',
  'equations'
]);

const OPERATION_MAP: Record<string, string> = {
  insert: 'insert',
  insertion: 'insert',
  add: 'insert',
  append: 'insert',
  push: 'push',
  push_back: 'insert',
  push_front: 'insert',
  enqueue: 'enqueue',
  delete: 'delete',
  deletion: 'delete',
  remove: 'delete',
  pop: 'pop',
  pop_back: 'delete',
  pop_front: 'delete',
  dequeue: 'dequeue',
  search: 'search',
  searching: 'search',
  find: 'find',
  lookup: 'lookup',
  traverse: 'traverse',
  traversal: 'traverse',
  display: 'display',
  print: 'display',
  show: 'display',
  peek: 'peek',
  top: 'peek',
  reverse: 'reverse',
  reversal: 'reverse',
  sort: 'sort',
  sorting: 'sort',
  count: 'count',
  counting: 'count',
  update: 'update',
  query: 'query',
  menu: 'menu',
  menu_driven: 'menu'
};

const INTENT_SET = new Set([
  'implement',
  'create',
  'construct',
  'write',
  'solve',
  'calculate',
  'find',
  'compute',
  'explain',
  'demonstrate',
  'convert',
  'evaluate',
  'derive',
  'prove',
  'program',
  'code',
  'debug',
  'fix',
  'troubleshoot'
]);

const POSITION_MAP: Record<string, string> = {
  end: 'end',
  tail: 'end',
  back: 'end',
  last: 'end',
  beginning: 'beginning',
  head: 'beginning',
  front: 'beginning',
  start: 'beginning',
  middle: 'middle',
  index: 'index',
  position: 'position',
  kth: 'kth',
  after: 'after',
  sorted: 'sorted'
};

// ── Sub-Extractors ────────────────────────────────────────────────────────────

export function extractEntities(
  tokens: NormalizedToken[],
  canonicalTerms: CanonicalTerm[]
): EntityEvidence[] {
  const entities: EntityEvidence[] = [];
  const coveredTokens = new Set<number>();

  // 1. Process canonical terms first (high precision multi-word / authoritative concepts)
  for (const term of canonicalTerms) {
    const canonical = term.canonical;
    let kind: EntityKind | null = null;

    if (DATA_STRUCTURE_SET.has(canonical)) {
      kind = 'data_structure';
    } else if (ALGORITHM_SET.has(canonical)) {
      kind = 'algorithm';
    } else if (NUMERICAL_SET.has(canonical)) {
      kind = 'numerical_method';
    } else if (MATHEMATICAL_OBJECT_SET.has(canonical)) {
      kind = 'mathematical_object';
    }

    if (kind) {
      const sourceTokens: number[] = [];
      for (let i = term.startToken; i < term.endToken; i++) {
        sourceTokens.push(i);
        coveredTokens.add(i);
      }
      entities.push({
        kind,
        value: canonical,
        sourceTokens,
        startToken: term.startToken,
        endToken: term.endToken,
        confidence: term.confidence
      });
    }
  }

  // 2. Check remaining individual tokens for computational objects
  for (let i = 0; i < tokens.length; i++) {
    if (coveredTokens.has(i)) continue;
    const word = tokens[i].text.toLowerCase();

    let kind: EntityKind | null = null;
    let canonicalVal = word;

    if (DATA_STRUCTURE_SET.has(word)) {
      kind = 'data_structure';
    } else if (ALGORITHM_SET.has(word)) {
      kind = 'algorithm';
    } else if (NUMERICAL_SET.has(word)) {
      kind = 'numerical_method';
    } else if (MATHEMATICAL_OBJECT_SET.has(word)) {
      kind = 'mathematical_object';
      if (word === 'matrices') canonicalVal = 'matrix';
      if (word === 'vertices') canonicalVal = 'vertex';
      if (word === 'eigenvalues') canonicalVal = 'eigenvalue';
      if (word === 'eigenvectors') canonicalVal = 'eigenvector';
      if (word === 'equations') canonicalVal = 'equation';
    }

    if (kind) {
      entities.push({
        kind,
        value: canonicalVal,
        sourceTokens: [i],
        startToken: i,
        endToken: i + 1,
        confidence: 1.0
      });
      coveredTokens.add(i);
    }
  }

  return entities;
}

export function extractOperations(
  tokens: NormalizedToken[],
  canonicalTerms: CanonicalTerm[]
): OperationEvidence[] {
  const operations: OperationEvidence[] = [];
  const coveredTokens = new Set<number>();

  // Check canonical terms first
  for (const term of canonicalTerms) {
    const canonical = term.canonical;
    if (OPERATION_MAP[canonical]) {
      const sourceTokens: number[] = [];
      for (let i = term.startToken; i < term.endToken; i++) {
        sourceTokens.push(i);
        coveredTokens.add(i);
      }
      operations.push({
        operation: OPERATION_MAP[canonical],
        sourceTokens,
        startToken: term.startToken,
        endToken: term.endToken,
        confidence: term.confidence
      });
    }
  }

  // Check individual tokens
  for (let i = 0; i < tokens.length; i++) {
    if (coveredTokens.has(i)) continue;
    const word = tokens[i].text.toLowerCase();
    if (OPERATION_MAP[word]) {
      operations.push({
        operation: OPERATION_MAP[word],
        sourceTokens: [i],
        startToken: i,
        endToken: i + 1,
        confidence: 1.0
      });
      coveredTokens.add(i);
    }
  }

  return operations;
}

export function extractIntents(tokens: NormalizedToken[]): IntentEvidence[] {
  const intents: IntentEvidence[] = [];

  for (let i = 0; i < tokens.length; i++) {
    const word = tokens[i].text.toLowerCase();
    if (INTENT_SET.has(word)) {
      intents.push({
        intent: word,
        sourceTokens: [i],
        startToken: i,
        endToken: i + 1,
        confidence: 1.0
      });
    }
  }

  return intents;
}

export function extractConstraints(
  tokens: NormalizedToken[],
  canonicalTerms: CanonicalTerm[]
): ConstraintEvidence[] {
  const constraints: ConstraintEvidence[] = [];

  for (let i = 0; i < tokens.length; i++) {
    const word = tokens[i].text.toLowerCase();

    // Position constraints
    if (POSITION_MAP[word]) {
      // Look back for "at the", "from the", "to the", "at", "from"
      constraints.push({
        type: 'position',
        value: POSITION_MAP[word],
        sourceTokens: [i],
        startToken: i,
        endToken: i + 1,
        confidence: 1.0
      });
    }

    // Ordering constraints
    if (word === 'sorted' || word === 'ascending' || word === 'descending') {
      constraints.push({
        type: 'ordering',
        value: word,
        sourceTokens: [i],
        startToken: i,
        endToken: i + 1,
        confidence: 1.0
      });
    }
  }

  return constraints;
}

// ── Main Entrypoint ───────────────────────────────────────────────────────────

/**
 * Extracts structured semantic evidence from a normalized/canonicalized input.
 */
export function extractSemanticInput(
  input: CanonicalizedInput | NormalizedInput
): SemanticInput {
  // Ensure we have a CanonicalizedInput
  const canonicalized: CanonicalizedInput =
    'canonicalizationConfidence' in input
      ? (input as CanonicalizedInput)
      : canonicalize(input as NormalizedInput);

  const tokens = canonicalized.tokens;
  const canonicalTerms = canonicalized.canonicalTerms;

  const entities = extractEntities(tokens, canonicalTerms);
  const operations = extractOperations(tokens, canonicalTerms);
  const intents = extractIntents(tokens);
  const constraints = extractConstraints(tokens, canonicalTerms);

  // Confidence for extraction: 1.0 when deterministic rules execute
  const extractionConfidence = 1.0;

  return {
    originalText: canonicalized.normalizedInput.originalText,
    normalizedText: canonicalized.normalizedInput.normalizedText,
    tokens,
    corrections: canonicalized.normalizedInput.corrections,
    canonicalTerms,
    entities,
    operations,
    intents,
    constraints,
    normalizationConfidence: canonicalized.normalizedInput.normalizationConfidence,
    extractionConfidence
  };
}
