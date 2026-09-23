/**
 * CHUP V2 — Composition Test Suite (T2.1 - T2.8).
 *
 * Verifies generic state-transition composition, fragment assembly,
 * ordering correctness, and strict negative controls.
 */

import { parseProblem } from '../pipeline/problemParser';
import { normalizeInput } from '../pipeline/inputNormalizer';
import { extractRequirements } from '../pipeline/requirementExtractor';
import { composePipeline } from '../solver/compositionEngine';
import { solveCpProblem } from '../solver/cpSolver';

function assert(condition: boolean, description: string): boolean {
  if (condition) {
    console.log(`  ✓ ${description}`);
    return true;
  } else {
    console.log(`  ✗ ${description}`);
    return false;
  }
}

export function runCompositionTests(): { passed: number; failed: number } {
  let passed = 0;
  let failed = 0;

  function check(condition: boolean, description: string) {
    if (assert(condition, description)) passed++;
    else failed++;
  }

  console.log('\n=================================================');
  console.log('   CHUP V2 Composition Test Suite (T2.1 - T2.8)   ');
  console.log('=================================================');

  // ── T2.1: sort + range_sum ────────────────────────────────────────────────
  console.log('\n[T2.1: sort + range_sum]');
  const t2_1_text = `You are given an array of n integers.
First, sort the array in non-decreasing order.
Then you are given q queries. Each query contains two positions l and r.
For every query, print the sum of the elements from position l through r,
inclusive, in the sorted array.
Input:
8 4
5 -2 7 1 3 -4 6 2
1 3
2 5
4 8
3 3
Constraints:
1 <= n <= 100000
1 <= q <= 100000
-10^9 <= a[i] <= 10^9
1 <= l <= r <= n
Output:
-5
4
23
1`;

  const parsed2_1 = parseProblem(normalizeInput(t2_1_text), t2_1_text);
  const reqs2_1 = extractRequirements(parsed2_1);
  check(reqs2_1.operations.includes('sorting') && reqs2_1.operations.includes('range_sum'), 'T2.1 extracts sorting and range_sum');
  const plan2_1 = composePipeline(reqs2_1);
  check(plan2_1.mode === 'composed', 'T2.1 discovers composed pipeline');
  check(plan2_1.steps[0].conceptId === 'sorting' && plan2_1.steps[1].conceptId === 'prefix_sum', 'T2.1 orders pipeline: sorting → prefix_sum');

  const result2_1 = solveCpProblem(parsed2_1);
  check(result2_1.success === true, 'T2.1 solves and compiles successfully');
  check(result2_1.code.includes('long long'), 'T2.1 uses long long for overflow risk');
  check(result2_1.verification?.allPassed === true, 'T2.1 passes all verification test cases');

  // ── T2.2: sort + binary_search ────────────────────────────────────────────
  console.log('\n[T2.2: sort + binary_search]');
  const t2_2_text = `You are given an unsorted array of n integers.
First, sort the array in ascending order.
Then answer q queries, each asking for the 1-based index of a value x in the sorted array.
Input:
5 2
9 1 5 3 7
5
8
Output:
3
-1`;

  const parsed2_2 = parseProblem(normalizeInput(t2_2_text), t2_2_text);
  const reqs2_2 = extractRequirements(parsed2_2);
  const plan2_2 = composePipeline(reqs2_2);
  check(plan2_2.mode === 'composed', 'T2.2 discovers composed pipeline');
  check(plan2_2.steps.some(s => s.conceptId === 'sorting') && plan2_2.steps.some(s => s.conceptId === 'binary_search'), 'T2.2 combines sorting and binary_search');

  // ── T2.3: frequency_map + filter_count ────────────────────────────────────
  console.log('\n[T2.3: frequency_map + filter_count]');
  const t2_3_text = `Given an array of n integers, find the count of distinct elements appearing at least k times.
Input:
6 2
1 2 2 3 3 3
Output:
2`;

  const parsed2_3 = parseProblem(normalizeInput(t2_3_text), t2_3_text);
  const reqs2_3 = extractRequirements(parsed2_3);
  check(reqs2_3.operations.includes('frequency_count') || reqs2_3.operations.includes('filter_count'), 'T2.3 extracts frequency count / filter');
  const plan2_3 = composePipeline(reqs2_3);
  check(plan2_3.steps.some(s => s.conceptId === 'frequency_count'), 'T2.3 pipeline includes frequency_count');

  // ── T2.4: BFS + shortest_path ─────────────────────────────────────────────
  console.log('\n[T2.4: BFS + shortest_path]');
  const t2_4_text = `Given an unweighted graph with n vertices and m edges, find the shortest path distance from vertex 1 to vertex n.
Input:
4 4
1 2
2 3
3 4
1 3
Output:
2`;

  const parsed2_4 = parseProblem(normalizeInput(t2_4_text), t2_4_text);
  const reqs2_4 = extractRequirements(parsed2_4);
  check(reqs2_4.operations.includes('shortest_path'), 'T2.4 extracts shortest_path');
  const plan2_4 = composePipeline(reqs2_4);
  check(plan2_4.steps.some(s => s.conceptId === 'bfs'), 'T2.4 uses bfs for unweighted shortest path');

  // ── T2.5: sorting + two_pointers ──────────────────────────────────────────
  console.log('\n[T2.5: sorting + two_pointers]');
  const t2_5_text = `Given an unsorted array of n integers, first sort the array.
Then find a pair with sum equal to target T using two pointers.
Input:
5 9
8 1 4 2 5
Output:
1 8`;

  const parsed2_5 = parseProblem(normalizeInput(t2_5_text), t2_5_text);
  const reqs2_5 = extractRequirements(parsed2_5);
  check(reqs2_5.operations.includes('sorting') && reqs2_5.operations.includes('pair_sum'), 'T2.5 extracts sorting and pair_sum');
  const plan2_5 = composePipeline(reqs2_5);
  check(plan2_5.mode === 'composed', 'T2.5 discovers composed pipeline');
  check(plan2_5.steps[0].conceptId === 'sorting' && plan2_5.steps[1].conceptId === 'two_pointers', 'T2.5 orders pipeline: sorting → two_pointers');

  // ── T2.6: sorting + greedy ────────────────────────────────────────────────
  console.log('\n[T2.6: sorting + greedy]');
  const t2_6_text = `You are given n intervals. Sort them to maximize the number of compatible tasks (interval scheduling).
Input:
3
1 3
2 5
4 6
Output:
2`;

  const parsed2_6 = parseProblem(normalizeInput(t2_6_text), t2_6_text);
  const reqs2_6 = extractRequirements(parsed2_6);
  check(reqs2_6.operations.includes('interval_schedule'), 'T2.6 extracts interval_schedule');

  // ── T2.7: prefix_sum + multiple range queries ─────────────────────────────
  console.log('\n[T2.7: prefix_sum + multiple range queries]');
  const t2_7_text = `A static array of n integers is given. Answer q range sum queries from index l to r.
Input:
4 2
1 2 3 4
1 2
2 4
Output:
3
9`;

  const parsed2_7 = parseProblem(normalizeInput(t2_7_text), t2_7_text);
  const reqs2_7 = extractRequirements(parsed2_7);
  check(reqs2_7.operations.includes('range_sum') && reqs2_7.hasRepeatedQueries, 'T2.7 extracts range_sum with repeated queries');
  const result2_7 = solveCpProblem(parsed2_7);
  check(result2_7.success === true, 'T2.7 solves static range sum queries');

  // ── T2.8: genuinely unsupported compound problem (Negative Control) ────────
  console.log('\n[T2.8: genuinely unsupported compound problem]');
  const t2_8_text = `You are given an array with point updates and range minimum queries.
After each update, output the minimum value in a range.
Input:
5 3
1 5 2 4 3
update 2 10
range min 1 3
Output:
1`;

  const parsed2_8 = parseProblem(normalizeInput(t2_8_text), t2_8_text);
  const reqs2_8 = extractRequirements(parsed2_8);
  check(reqs2_8.operations.includes('dynamic_range_min_query'), 'T2.8 extracts dynamic_range_min_query operation');
  const plan2_8 = composePipeline(reqs2_8);
  check(plan2_8.mode === 'compound_unsupported', 'T2.8 strictly classifies as compound_unsupported');
  check(plan2_8.uncoveredOperations.includes('dynamic_range_min_query'), 'T2.8 identifies uncovered dynamic_range_min_query requirement');

  const result2_8 = solveCpProblem(parsed2_8);
  check(result2_8.success === false, 'T2.8 does not attempt to fabricate code');
  check(result2_8.limitationMessage !== null && result2_8.limitationMessage.includes('No supported concept'), 'T2.8 provides honest limitation message');

  return { passed, failed };
}

if (require.main === module) {
  const { failed } = runCompositionTests();
  process.exit(failed > 0 ? 1 : 0);
}
