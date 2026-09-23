/**
 * CHUP V2 — Strategy Evaluator.
 *
 * Implements the core architectural decision rule:
 *
 * Problem
 *  ↓
 * Extract requirements
 *  ↓
 * Generate/rank concepts
 *  ↓
 * Can ONE supported concept satisfy all requirements?
 *  ├─ YES → use it (Single Strategy)
 *  └─ NO
 *       ↓
 *    Composition Engine (State-transition reasoning)
 *       ├─ YES → compose pipeline
 *       └─ NO → COMPOUND_UNSUPPORTED
 */

import {
  ProblemRequirements,
  TopicCandidate,
  RequiredOperation,
  StrategyPlan,
  DiagnosticTraceEntry,
  KnowledgeConcept
} from '../models/problemSpec';
import { getConceptById } from '../knowledge/dsaKnowledge';
import { getAllUnifiedConcepts, canSatisfyPreconditions } from '../knowledge/compositionKnowledge';
import { composePipeline } from './compositionEngine';
import { TemplateParams } from './solutionTemplates';

export interface StrategyDecision {
  type: 'single' | 'compose' | 'compound_unsupported' | 'unrecognized';
  selectedConcept: TopicCandidate | null;
  compositionConcepts: TopicCandidate[];
  templateId: string | null;
  templateParams: TemplateParams;
  plan?: StrategyPlan;
  reasoning: string;
  limitationMessage: string | null;
  diagnosticTrace?: DiagnosticTraceEntry[];
}

/** Operations fully covered by legacy DSA concepts */
const CONCEPT_OPERATION_COVERAGE: Record<string, RequiredOperation[]> = {
  prefix_sum: ['range_sum', 'subarray_target_sum'],
  sliding_window: ['subarray_window_opt'],
  two_pointers: ['pair_sum'],
  frequency_count: ['frequency_count', 'pair_sum'],
  binary_search: ['element_lookup', 'threshold_search'],
  sort_greedy: ['interval_schedule'],
  bfs: ['shortest_path', 'connectivity'],
  dfs: ['connectivity'],
  dp_1d: ['recurrence_1d', 'subarray_target_sum'],
  sorting: ['sorting', 'sorted_order'],
  monotonic_stack: ['nearest_smaller_values', 'monotonic_stack', 'histogram', 'next_greater', 'daily_temperatures', 'stock_span'],
  trie: ['prefix_tree', 'trie_prefix_search'],
  lru_cache: ['lru_cache', 'key_value_mapping'],
  lfu_cache: ['lfu_cache', 'key_value_mapping'],
  tree_dp: ['tree_dp']
};

/**
 * Evaluate requirements against topic candidates to produce a strategy decision.
 *
 * @param requirements - Semantic requirements extracted from problem statement
 * @param rankedCandidates - Ranked topic candidates from knowledge base scoring
 * @param overflowRisk - Whether integer overflow is anticipated
 * @returns StrategyDecision indicating whether single, composite, or unsupported
 */
export function evaluateStrategy(
  requirements: ProblemRequirements,
  rankedCandidates: TopicCandidate[],
  overflowRisk: boolean,
  excludedAlgorithms?: Set<string>
): StrategyDecision {
  const diagnosticTrace: DiagnosticTraceEntry[] = [];
  let operationSubtype: string = requirements.operations.includes('range_sum') ? 'range_sum' : 'target_sum';
  if (requirements.operations.includes('histogram')) {
    operationSubtype = 'histogram';
  } else if (requirements.operations.includes('next_greater')) {
    operationSubtype = 'next_greater';
  } else if (requirements.operations.includes('daily_temperatures')) {
    operationSubtype = 'daily_temperatures';
  } else if (requirements.operations.includes('stock_span')) {
    operationSubtype = 'stock_span';
  }

  const templateParams: TemplateParams = {
    intType: overflowRisk ? 'long long' : 'int',
    hasQueries: requirements.hasRepeatedQueries,
    operationSubtype
  };

  const initialStates = requirements.dataStructure === 'grid'
    ? ['grid', 'graph_unweighted']
    : (requirements.dataStructure === 'intervals' ? ['intervals', 'sequence'] : ['sequence']);
  if (requirements.requiresSorted && !requirements.operations.includes('sorting')) {
    initialStates.push('sorted_sequence');
  }

  // ── Step 0: Check Explicit Implementation Constraints ────────────────────
  if (requirements.implementationConstraint === 'manual_array' || requirements.implementationConstraint === 'manual') {
    if (requirements.operations.includes('lifo') || requirements.explanation.toLowerCase().includes('stack')) {
      diagnosticTrace.push({
        requirement: 'lifo',
        candidate: 'stack',
        accepted: false,
        reason: 'Explicit implementation constraint requires manual array implementation; STL stack rejected.',
        complexityAssessment: 'O(1)'
      });
      diagnosticTrace.push({
        requirement: 'lifo',
        candidate: 'manual_stack_array',
        accepted: true,
        reason: 'Manual array-backed stack satisfies explicit implementation constraint.',
        complexityAssessment: 'O(1)'
      });

      const singlePlan: StrategyPlan = {
        mode: 'single',
        steps: [{ conceptId: 'manual_stack_array', satisfies: ['lifo'], produces: ['lifo_state'] }],
        initialStates,
        finalStates: [...initialStates, 'lifo_state'],
        coveredOperations: ['lifo'],
        uncoveredOperations: [],
        reasoning: 'Explicit manual implementation requested: using manual array-backed stack.',
        diagnosticTrace
      };

      return {
        type: 'single',
        selectedConcept: {
          conceptId: 'manual_stack_array',
          confidence: 1.0,
          matchedPatterns: ['explicit manual array constraint'],
          supported: true
        },
        compositionConcepts: [],
        templateId: 'manual_stack_array',
        templateParams,
        plan: singlePlan,
        reasoning: singlePlan.reasoning,
        limitationMessage: null,
        diagnosticTrace
      };
    }
  }

  // ── Step 1: Evaluate Unified Concepts (Single Strategy) ───────────────────
  if (requirements.operations.length > 0) {
    const unified = getAllUnifiedConcepts();
    const availableSet = new Set<string>(initialStates);

    // Filter candidate pool based on manual implementation constraints & excluded algorithms
    const candidatePool = unified.filter(c => {
      if (excludedAlgorithms && excludedAlgorithms.has(c.id)) {
        return false;
      }
      if (requirements.implementationConstraint === 'manual_array' || requirements.implementationConstraint === 'manual') {
        return !c.isSTL;
      }
      return true;
    });

    // Score and evaluate each candidate concept against requirements
    interface EvaluatedCandidate {
      concept: KnowledgeConcept;
      coveredOps: RequiredOperation[];
      coversAll: boolean;
      preconditionsMet: boolean;
      asymptoticallyFeasible: boolean;
      score: number;
    }

    const evaluated: EvaluatedCandidate[] = [];

    for (const cand of candidatePool) {
      const coveredOps = cand.satisfies.filter(op => requirements.operations.includes(op));
      const coversAll = requirements.operations.length > 0 && requirements.operations.every(op => cand.satisfies.includes(op));
      const preconditionsMet = canSatisfyPreconditions(availableSet, cand.requires);
      const isFeasible = true; // By default feasible unless constraints rule it out

      let score = coveredOps.length;
      if (coversAll) score += 10;
      if (preconditionsMet) score += 5;

      // Semantic preferences based on properties:
      // If ordered_frequency_output is required, map is strictly preferred over unordered_map
      if (requirements.operations.includes('ordered_frequency_output') && cand.id === 'map') {
        score += 5;
      }
      // If frequency counting is required, map guarantees deterministic key-ordered output
      if (requirements.operations.includes('frequency_count') && cand.id === 'map') {
        score += 3;
      }
      // If fast_membership or pure duplicate_detection without ordering is required, unordered_set preferred
      if (
        (requirements.operations.includes('fast_membership') ||
         (requirements.operations.includes('duplicate_detection') && !requirements.operations.includes('sorted_order'))) &&
        cand.id === 'unordered_set'
      ) {
        score += 5;
      }
      // If uniqueness and sorted_order are required, set satisfies both
      if (requirements.operations.includes('uniqueness') && requirements.operations.includes('sorted_order') && cand.id === 'set') {
        score += 10;
      }
      // If registration_system is required, unordered_map provides O(1) average lookup/insert
      if (requirements.operations.includes('registration_system') && cand.id === 'unordered_map') {
        score += 10;
      }
      // If dynamic_array_operations is required, vector is strictly preferred
      if (requirements.operations.includes('dynamic_array_operations') && cand.id === 'vector') {
        score += 15;
      }
      // If deque_operations or reversible_deque is required, deque is strictly preferred
      if ((requirements.operations.includes('deque_operations') || requirements.operations.includes('reversible_deque')) && cand.id === 'deque') {
        score += 15;
      }
      // If notification_queue, queue_simulation, team_queue, or card_war_simulation is required, queue is strictly preferred
      if (
        (requirements.operations.includes('notification_queue') ||
         requirements.operations.includes('queue_simulation') ||
         requirements.operations.includes('team_queue') ||
         requirements.operations.includes('card_war_simulation')) &&
        cand.id === 'queue'
      ) {
        score += 15;
      }
      // If nearest_smaller_values or monotonic_stack is required, monotonic_stack is preferred
      if (
        (requirements.operations.includes('nearest_smaller_values') ||
         requirements.operations.includes('monotonic_stack')) &&
        cand.id === 'monotonic_stack'
      ) {
        score += 20;
      }
      // If nearest_smaller_values, monotonic_stack, balanced_brackets, or bracket_sequence_min_cost is required, stack is candidate
      if (
        (requirements.operations.includes('balanced_brackets') ||
         requirements.operations.includes('bracket_sequence_min_cost')) &&
        cand.id === 'stack'
      ) {
        score += 15;
      }
      // If priority_queue_operations, multi_priority_queue, or priority_queue_halving is required, priority_queue_max is preferred
      if (
        (requirements.operations.includes('priority_queue_operations') ||
         requirements.operations.includes('multi_priority_queue') ||
         requirements.operations.includes('priority_queue_halving')) &&
        cand.id === 'priority_queue_max'
      ) {
        score += 15;
      }
      // If interval_partitioning is required, priority_queue_min is preferred
      if (requirements.operations.includes('interval_partitioning') && cand.id === 'priority_queue_min') {
        score += 15;
      }
      // If distinct_count is required, set is preferred
      if (requirements.operations.includes('distinct_count') && (cand.id === 'set' || cand.id === 'unordered_set')) {
        score += 15;
      }
      // If multiset_operations is required, multiset is strictly preferred
      if (requirements.operations.includes('multiset_operations') && cand.id === 'multiset') {
        score += 15;
      }
      // If arithmetic_gap is required, arithmetic_gap concept is preferred
      if (requirements.operations.includes('arithmetic_gap') && cand.id === 'arithmetic_gap') {
        score += 15;
      }
      // If lis_dp is required, lis concept is preferred
      if (requirements.operations.includes('lis_dp') && cand.id === 'lis') {
        score += 15;
      }

      diagnosticTrace.push({
        requirement: requirements.operations.join(', '),
        candidate: cand.id,
        accepted: coversAll && preconditionsMet,
        reason: coversAll
          ? (preconditionsMet ? `Candidate satisfies all required operations [${requirements.operations.join(', ')}] and preconditions [${cand.requires.join(', ')}] are met` : `Candidate satisfies operations but preconditions [${cand.requires.join(', ')}] not met`)
          : `Candidate covers [${coveredOps.join(', ')}], missing [${requirements.operations.filter(op => !cand.satisfies.includes(op)).join(', ')}]`,
        requiredStates: cand.requires,
        availableStates: initialStates,
        producedStates: cand.produces,
        complexityAssessment: cand.complexity?.time
      });

      if (coveredOps.length > 0) {
        evaluated.push({
          concept: cand,
          coveredOps,
          coversAll,
          preconditionsMet,
          asymptoticallyFeasible: isFeasible,
          score
        });
      }
    }

    // Check if any unified candidate completely covers all operations with preconditions met
    const fullySatisfying = evaluated
      .filter(e => e.coversAll && e.preconditionsMet)
      .sort((a, b) => b.score - a.score);

    if (fullySatisfying.length > 0) {
      const best = fullySatisfying[0].concept;
      // Domain constraint check: sliding window cannot handle negative values for sum queries
      if (
        !(requirements.allowsNegativeValues &&
          best.id === 'sliding_window' &&
          requirements.operations.includes('subarray_window_opt'))
      ) {
        const singlePlan: StrategyPlan = {
          mode: 'single',
          steps: [{ conceptId: best.id, satisfies: requirements.operations, produces: best.produces }],
          initialStates,
          finalStates: [...initialStates, ...best.produces],
          coveredOperations: requirements.operations,
          uncoveredOperations: [],
          reasoning: `Single strategy evaluation: concept '${best.id}' completely satisfies all required operations [${requirements.operations.join(', ')}].`,
          diagnosticTrace
        };

        return {
          type: 'single',
          selectedConcept: {
            conceptId: best.id,
            confidence: 0.95,
            matchedPatterns: [`Satisfies operations: ${requirements.operations.join(', ')}`],
            supported: true
          },
          compositionConcepts: [],
          templateId: best.templateId || best.id,
          templateParams,
          plan: singlePlan,
          reasoning: singlePlan.reasoning,
          limitationMessage: null,
          diagnosticTrace
        };
      }
    }

    // Fallback: Also evaluate rankedCandidates from topic detection (DSA concepts)
    for (const cand of rankedCandidates) {
      if (!cand.supported || cand.rejected || (excludedAlgorithms && excludedAlgorithms.has(cand.conceptId))) continue;
      const coveredOps = CONCEPT_OPERATION_COVERAGE[cand.conceptId] || [];
      const coversAll = requirements.operations.length > 0 && requirements.operations.every(op => coveredOps.includes(op));
      if (coversAll) {
        // Domain constraint check: sliding window cannot handle negative values for sum queries
        if (
          requirements.allowsNegativeValues &&
          cand.conceptId === 'sliding_window' &&
          requirements.operations.includes('subarray_window_opt')
        ) {
          continue;
        }

        // sort_greedy strictly requires interval_schedule operation
        if (cand.conceptId === 'sort_greedy' && !requirements.operations.includes('interval_schedule')) {
          continue;
        }

        const dsaConcept = getConceptById(cand.conceptId);
        const singlePlan: StrategyPlan = {
          mode: 'single',
          steps: [{ conceptId: cand.conceptId, satisfies: requirements.operations, produces: [] }],
          initialStates,
          finalStates: initialStates,
          coveredOperations: requirements.operations,
          uncoveredOperations: [],
          reasoning: `Single strategy evaluation: concept '${cand.conceptId}' completely satisfies all required operations [${requirements.operations.join(', ')}].`,
          diagnosticTrace
        };

        return {
          type: 'single',
          selectedConcept: cand,
          compositionConcepts: [],
          templateId: dsaConcept?.solutionTemplateId || null,
          templateParams,
          plan: singlePlan,
          reasoning: singlePlan.reasoning,
          limitationMessage: null,
          diagnosticTrace
        };
      }
    }
  }

  // ── Step 2: Composition Engine (State-transition reasoning) ────────────────
  if (requirements.operations.length > 0) {
    const plan = composePipeline(requirements, excludedAlgorithms);
    if (plan.diagnosticTrace) {
      diagnosticTrace.push(...plan.diagnosticTrace);
    }
    plan.diagnosticTrace = diagnosticTrace;

    if (plan.mode === 'composed') {
      const topConcept = rankedCandidates.find(t => t.conceptId === plan.steps[0].conceptId) ||
                         rankedCandidates.find(t => t.supported) || {
                           conceptId: plan.steps[0].conceptId,
                           confidence: 0.8,
                           matchedPatterns: ['composed pipeline step'],
                           supported: true
                         };

      return {
        type: 'compose',
        selectedConcept: topConcept,
        compositionConcepts: rankedCandidates.filter(c => plan.steps.some(s => s.conceptId === c.conceptId)),
        templateId: 'composed',
        templateParams: {
          ...templateParams,
          hasInitialSort: plan.steps.some(s => s.conceptId === 'sorting' || s.conceptId === 'sort')
        },
        plan,
        reasoning: plan.reasoning,
        limitationMessage: null,
        diagnosticTrace
      };
    } else {
      return {
        type: 'compound_unsupported',
        selectedConcept: null,
        compositionConcepts: [],
        templateId: null,
        templateParams,
        plan,
        reasoning: plan.reasoning,
        limitationMessage: `Uncovered requirement: ${plan.uncoveredOperations.join(', ')}. No supported concept satisfies this operation.`,
        diagnosticTrace
      };
    }
  }

  // ── Step 3: Fail-closed if no formal operations were extracted ───────────
  // Architecture invariant: Broad keyword scoring without proven semantic operation
  // coverage must NEVER directly select an executable implementation template.
  // Any recognized candidate without verified operation coverage is treated as recognized-only (templateId: null).

  // ── Step 4: Check recognized-only patterns ────────────────────────────────
  const recognizedOnly = rankedCandidates.find(t => !t.supported && !t.rejected && t.confidence > 0.1);
  if (recognizedOnly) {
    const concept = getConceptById(recognizedOnly.conceptId);
    return {
      type: 'single',
      selectedConcept: recognizedOnly,
      compositionConcepts: [],
      templateId: null,
      templateParams,
      reasoning: `Recognized concept: ${concept?.name || recognizedOnly.conceptId}.`,
      limitationMessage: `Pattern recognized: ${concept?.name || recognizedOnly.conceptId}. No implementation template available for this pattern yet.`,
      diagnosticTrace
    };
  }

  // ── Step 5: Unrecognized ──────────────────────────────────────────────────
  return {
    type: 'unrecognized',
    selectedConcept: null,
    compositionConcepts: [],
    templateId: null,
    templateParams,
    reasoning: 'No algorithmic patterns detected that satisfy problem requirements.',
    limitationMessage: 'Unable to identify a solvable pattern in this problem.',
    diagnosticTrace
  };
}

