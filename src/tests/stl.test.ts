/**
 * CHUP / Hidden Link — Comprehensive STL Knowledge & Composition Test Suite.
 *
 * Tests T3.1 through T3.15:
 * - Requirements extraction
 * - Candidate evaluation & complexity feasibility
 * - Precondition satisfaction & state transitions
 * - Composition discovery without phrase-to-template hardcoding
 * - Explicit manual implementation priority
 * - Full compilation with g++ and execution verification
 * - Live structured diagnostic trace verification
 */

import { parseProblem } from '../pipeline/problemParser';
import { normalizeInput } from '../pipeline/inputNormalizer';
import { extractRequirements } from '../pipeline/requirementExtractor';
import { composePipeline } from '../solver/compositionEngine';
import { evaluateStrategy } from '../solver/strategyEvaluator';
import { solveCpProblem } from '../solver/cpSolver';
import { verifyCode } from '../verifier/verificationEngine';

function assert(condition: boolean, description: string): boolean {
  if (condition) {
    console.log(`  ✓ ${description}`);
    return true;
  } else {
    console.error(`  ✗ ${description}`);
    return false;
  }
}

export function runStlTests(): { passed: number; failed: number } {
  let passed = 0;
  let failed = 0;

  function check(condition: boolean, description: string) {
    if (assert(condition, description)) passed++;
    else failed++;
  }

  console.log('\n=================================================');
  console.log('   CHUP V2 STL Knowledge & Composition (T3.1 - T3.15) ');
  console.log('=================================================');

  // ── T3.1: vector basic generation ──────────────────────────────────────────
  console.log('\n[T3.1: vector basic generation]');
  const t3_1_text = `Read n integers and print them.
Input:
5
10 20 30 40 50
Output:
10 20 30 40 50`;

  const parsed3_1 = parseProblem(normalizeInput(t3_1_text), t3_1_text);
  const reqs3_1 = extractRequirements(parsed3_1);
  check(reqs3_1.operations.includes('sequence_io'), 'T3.1 extracts sequence_io requirement');
  const res3_1 = solveCpProblem(parsed3_1);
  check(res3_1.success === true, 'T3.1 compiles and executes successfully');
  check(res3_1.code.includes('<vector>'), 'T3.1 includes <vector>');
  check(res3_1.selectedAlgorithm === 'vector', 'T3.1 selects vector concept');

  // ── T3.2: sorting ──────────────────────────────────────────────────────────
  console.log('\n[T3.2: sorting]');
  const t3_2_text = `Sort an array and print it.
Input:
5
5 2 4 1 3
Output:
1 2 3 4 5`;

  const parsed3_2 = parseProblem(normalizeInput(t3_2_text), t3_2_text);
  const reqs3_2 = extractRequirements(parsed3_2);
  check(reqs3_2.operations.includes('sorting'), 'T3.2 extracts sorting requirement');
  const res3_2 = solveCpProblem(parsed3_2);
  check(res3_2.success === true, 'T3.2 compiles and executes successfully');
  check(res3_2.code.includes('sort('), 'T3.2 uses sort() function');
  check(res3_2.code.includes('<algorithm>'), 'T3.2 includes <algorithm>');

  // ── T3.3: unique + sorted ──────────────────────────────────────────────────
  console.log('\n[T3.3: unique + sorted]');
  const t3_3_text = `Remove duplicate values and print the remaining values in sorted order.
Input:
8
4 2 5 2 3 4 1 5
Output:
1 2 3 4 5`;

  const parsed3_3 = parseProblem(normalizeInput(t3_3_text), t3_3_text);
  const reqs3_3 = extractRequirements(parsed3_3);
  check(reqs3_3.operations.includes('uniqueness') && reqs3_3.operations.includes('sorted_order'), 'T3.3 extracts uniqueness and sorted_order');
  const res3_3 = solveCpProblem(parsed3_3);
  check(res3_3.selectedAlgorithm === 'set', 'T3.3 selects std::set for uniqueness + sorted_order');
  check(res3_3.success === true, 'T3.3 compiles and executes successfully');
  check(res3_3.code.includes('<set>'), 'T3.3 includes <set>');

  // ── T3.4: duplicate detection with fast membership ─────────────────────────
  console.log('\n[T3.4: duplicate detection with fast membership]');
  const t3_4_text = `Given n integers, output YES if any value occurs more than once, otherwise output NO.
Constraints:
1 <= n <= 1000000
Input:
4
1 2 3 2
Output:
YES`;

  const parsed3_4 = parseProblem(normalizeInput(t3_4_text), t3_4_text);
  const reqs3_4 = extractRequirements(parsed3_4);
  check(reqs3_4.operations.includes('duplicate_detection'), 'T3.4 extracts duplicate_detection');
  const res3_4 = solveCpProblem(parsed3_4);
  check(res3_4.success === true, 'T3.4 compiles and executes successfully on duplicate case');
  check(res3_4.selectedAlgorithm === 'unordered_set' || res3_4.selectedAlgorithm === 'set', 'T3.4 selects asymptotically feasible candidate');
  check(res3_4.code.includes('unordered_set') || res3_4.code.includes('set'), 'T3.4 uses set-based container');

  // Verify second test case for distinct values
  const distinctVerification = verifyCode(res3_4.code, [{ input: '3\n1 2 3', expectedOutput: 'NO' }]);
  check(distinctVerification.allPassed, 'T3.4 correctly outputs NO for distinct elements');

  // ── T3.5: frequency counting ───────────────────────────────────────────────
  console.log('\n[T3.5: frequency counting]');
  const t3_5_text = `Count the frequency of every distinct value.
Input:
5
1 2 2 3 3
Output:
1 1
2 2
3 2`;

  const parsed3_5 = parseProblem(normalizeInput(t3_5_text), t3_5_text);
  const reqs3_5 = extractRequirements(parsed3_5);
  check(reqs3_5.operations.includes('frequency_count'), 'T3.5 extracts frequency_count');
  const res3_5 = solveCpProblem(parsed3_5);
  check(res3_5.selectedAlgorithm === 'unordered_map' || res3_5.selectedAlgorithm === 'map', 'T3.5 selects valid frequency mapping candidate');
  check(res3_5.success === true, 'T3.5 compiles and executes successfully');

  // ── T3.6: ordered frequency output ─────────────────────────────────────────
  console.log('\n[T3.6: ordered frequency output]');
  const t3_6_text = `Count the frequency of every value and print the values in increasing order.
Input:
6
3 1 2 3 2 3
Output:
1 1
2 2
3 3`;

  const parsed3_6 = parseProblem(normalizeInput(t3_6_text), t3_6_text);
  const reqs3_6 = extractRequirements(parsed3_6);
  check(reqs3_6.operations.includes('ordered_frequency_output') || (reqs3_6.operations.includes('frequency_count') && reqs3_6.operations.includes('sorted_order')), 'T3.6 extracts ordered frequency requirement');
  const res3_6 = solveCpProblem(parsed3_6);
  check(res3_6.selectedAlgorithm === 'map', 'T3.6 naturally favors std::map over unordered_map due to ordered keys');
  check(res3_6.success === true, 'T3.6 compiles and executes successfully');
  check(res3_6.code.includes('<map>'), 'T3.6 includes <map>');

  // ── T3.7: stack ────────────────────────────────────────────────────────────
  console.log('\n[T3.7: stack]');
  const t3_7_text = `Use a stack to reverse a sequence.
Input:
4
1 2 3 4
Output:
4 3 2 1`;

  const parsed3_7 = parseProblem(normalizeInput(t3_7_text), t3_7_text);
  const reqs3_7 = extractRequirements(parsed3_7);
  check(reqs3_7.operations.includes('lifo'), 'T3.7 extracts lifo requirement');
  const res3_7 = solveCpProblem(parsed3_7);
  check(res3_7.selectedAlgorithm === 'stack', 'T3.7 selects std::stack');
  check(res3_7.success === true, 'T3.7 compiles and executes successfully');
  check(res3_7.code.includes('<stack>'), 'T3.7 includes <stack>');

  // ── T3.8: queue ────────────────────────────────────────────────────────────
  console.log('\n[T3.8: queue]');
  const t3_8_text = `Process people in first-come-first-served order.
Input:
3
10 20 30
Output:
10 20 30`;

  const parsed3_8 = parseProblem(normalizeInput(t3_8_text), t3_8_text);
  const reqs3_8 = extractRequirements(parsed3_8);
  check(reqs3_8.operations.includes('fifo'), 'T3.8 extracts fifo requirement');
  const res3_8 = solveCpProblem(parsed3_8);
  check(res3_8.selectedAlgorithm === 'queue', 'T3.8 selects std::queue');
  check(res3_8.success === true, 'T3.8 compiles and executes successfully');
  check(res3_8.code.includes('<queue>'), 'T3.8 includes <queue>');

  // ── T3.9: priority queue max heap ──────────────────────────────────────────
  console.log('\n[T3.9: priority queue max heap]');
  const t3_9_text = `Repeatedly output and remove the largest element.
Input:
4
3 1 4 2
Output:
4 3 2 1`;

  const parsed3_9 = parseProblem(normalizeInput(t3_9_text), t3_9_text);
  const reqs3_9 = extractRequirements(parsed3_9);
  check(reqs3_9.operations.includes('maximum_retrieval'), 'T3.9 extracts maximum_retrieval');
  const res3_9 = solveCpProblem(parsed3_9);
  check(res3_9.selectedAlgorithm === 'priority_queue_max', 'T3.9 selects priority_queue_max');
  check(res3_9.success === true, 'T3.9 compiles and executes successfully');
  check(res3_9.code.includes('priority_queue'), 'T3.9 uses priority_queue');

  // ── T3.10: priority queue min heap ─────────────────────────────────────────
  console.log('\n[T3.10: priority queue min heap]');
  const t3_10_text = `Repeatedly output and remove the smallest element.
Input:
4
3 1 4 2
Output:
1 2 3 4`;

  const parsed3_10 = parseProblem(normalizeInput(t3_10_text), t3_10_text);
  const reqs3_10 = extractRequirements(parsed3_10);
  check(reqs3_10.operations.includes('minimum_retrieval'), 'T3.10 extracts minimum_retrieval');
  const res3_10 = solveCpProblem(parsed3_10);
  check(res3_10.selectedAlgorithm === 'priority_queue_min', 'T3.10 selects priority_queue_min');
  check(res3_10.success === true, 'T3.10 compiles and executes successfully');
  check(res3_10.code.includes('greater<'), 'T3.10 uses greater comparator for min heap');

  // ── T3.11: lower_bound ─────────────────────────────────────────────────────
  console.log('\n[T3.11: lower_bound]');
  const t3_11_text = `Given a sorted array, for every query x print the first position whose value is at least x.
Input:
5 2
1 3 5 7 9
5
4
Output:
3
3`;

  const parsed3_11 = parseProblem(normalizeInput(t3_11_text), t3_11_text);
  const reqs3_11 = extractRequirements(parsed3_11);
  check(reqs3_11.requiresSorted === true, 'T3.11 detects pre-sorted array');
  check(reqs3_11.operations.includes('threshold_search'), 'T3.11 extracts threshold_search');
  const res3_11 = solveCpProblem(parsed3_11);
  check(res3_11.selectedAlgorithm === 'lower_bound', 'T3.11 selects lower_bound');
  check(res3_11.success === true, 'T3.11 compiles and executes successfully');

  // ── T3.12: sort + lower_bound composition (anti-hardcoding) ────────────────
  console.log('\n[T3.12: sort + lower_bound composition]');
  const t3_12_text = `Sort the array, then answer many queries asking for the first value >= x.
Input:
5 2
9 1 5 3 7
5
4
Output:
3
3`;

  const parsed3_12 = parseProblem(normalizeInput(t3_12_text), t3_12_text);
  const reqs3_12 = extractRequirements(parsed3_12);
  check(reqs3_12.operations.includes('sorting') && reqs3_12.operations.includes('threshold_search'), 'T3.12 extracts sorting and threshold_search');
  const plan3_12 = composePipeline(reqs3_12);
  check(plan3_12.mode === 'composed', 'T3.12 discovers composed pipeline');
  check(
    (plan3_12.steps[0].conceptId === 'sorting' || plan3_12.steps[0].conceptId === 'sort') &&
    plan3_12.steps[1].conceptId === 'lower_bound',
    'T3.12 orders pipeline: sort → lower_bound via state transitions'
  );
  const res3_12 = solveCpProblem(parsed3_12);
  check(res3_12.success === true, 'T3.12 compiles and executes successfully');

  // ── T3.13: frequency map + filtering ───────────────────────────────────────
  console.log('\n[T3.13: frequency map + filtering]');
  const t3_13_text = `Read numbers, count frequencies, then print values whose frequency is greater than k.
Input:
6 2
1 2 2 3 3 3
Output:
3`;

  const parsed3_13 = parseProblem(normalizeInput(t3_13_text), t3_13_text);
  const reqs3_13 = extractRequirements(parsed3_13);
  check(reqs3_13.operations.includes('frequency_count') && reqs3_13.operations.includes('filter_count'), 'T3.13 extracts frequency_count and filter_count');
  const res3_13 = solveCpProblem(parsed3_13);
  check(res3_13.success === true, 'T3.13 compiles and executes successfully');

  // ── T3.14: manual stack must remain manual ─────────────────────────────────
  console.log('\n[T3.14: manual stack must remain manual]');
  const t3_14_text = `Implement a stack using an array.
Input:
4
1 2 3 4
Output:
4 3 2 1`;

  const parsed3_14 = parseProblem(normalizeInput(t3_14_text), t3_14_text);
  const reqs3_14 = extractRequirements(parsed3_14);
  check(reqs3_14.implementationConstraint === 'manual_array', 'T3.14 extracts manual_array implementation constraint');
  const res3_14 = solveCpProblem(parsed3_14);
  check(res3_14.selectedAlgorithm === 'manual_stack_array', 'T3.14 selects manual_stack_array');
  check(!res3_14.code.includes('<stack>'), 'T3.14 FORBIDDEN: std::stack header must not be included');
  check(!res3_14.code.includes('std::stack'), 'T3.14 FORBIDDEN: std::stack type must not be used');
  check(res3_14.code.includes('arr') || res3_14.code.includes('top'), 'T3.14 uses manual array storage');
  check(res3_14.success === true, 'T3.14 manual stack compiles and executes successfully');

  // ── T3.15: genuine unsupported compound (Negative Control) ─────────────────
  console.log('\n[T3.15: genuine unsupported compound]');
  const t3_15_text = `Given an array that receives point updates, answer range minimum queries after each update.
Input:
5 2
1 5 2 4 3
1 10
1 3
Output:
1`;

  const parsed3_15 = parseProblem(normalizeInput(t3_15_text), t3_15_text);
  const reqs3_15 = extractRequirements(parsed3_15);
  check(reqs3_15.operations.includes('dynamic_range_min_query'), 'T3.15 extracts dynamic_range_min_query');
  const plan3_15 = composePipeline(reqs3_15);
  check(plan3_15.mode === 'compound_unsupported', 'T3.15 classifies as compound_unsupported');
  check(plan3_15.uncoveredOperations.includes('dynamic_range_min_query'), 'T3.15 identifies uncovered operation');
  const res3_15 = solveCpProblem(parsed3_15);
  check(res3_15.success === false, 'T3.15 does not fabricate code');
  check(res3_15.limitationMessage !== null && res3_15.limitationMessage.includes('No supported concept'), 'T3.15 provides honest limitation message');

  // ── Diagnostic Trace Verification ──────────────────────────────────────────
  console.log('\n[Diagnostic Trace Verification]');
  check(Array.isArray(res3_12.diagnosticTrace) && res3_12.diagnosticTrace.length > 0, 'Diagnostic trace is populated with real decisions');
  const traceItem = res3_12.diagnosticTrace![0];
  check(
    traceItem.candidate !== undefined &&
    traceItem.accepted !== undefined &&
    traceItem.reason !== undefined,
    'Trace items contain required structured fields (candidate, accepted, reason)'
  );

  return { passed, failed };
}

if (require.main === module) {
  const { failed } = runStlTests();
  process.exit(failed > 0 ? 1 : 0);
}
