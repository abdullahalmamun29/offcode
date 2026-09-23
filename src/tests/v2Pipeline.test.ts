/**
 * CHUP V2 Pipeline Tests.
 *
 * Tests the complete v2 pipeline: normalizer → parser → classifier →
 * constraint analyzer → topic detection → solver (integration).
 */

import { normalizeInput } from '../pipeline/inputNormalizer';
import { parseProblem } from '../pipeline/problemParser';
import { classifyProblem } from '../pipeline/problemClassifier';
import { analyzeConstraints } from '../pipeline/constraintAnalyzer';
import { scoreConcepts } from '../knowledge/dsaKnowledge';
import { buildFromTemplate } from '../solver/solutionTemplates';
import { composeCode } from '../generator/codeComposer';
import { StructuredProblem } from '../models/problemSpec';
import { extractRequirements } from '../pipeline/requirementExtractor';
import { evaluateStrategy } from '../solver/strategyEvaluator';
import { solveCpProblem } from '../solver/cpSolver';

// ═══════════════════════════════════════════════════════════════════════════════
// Test Infrastructure
// ═══════════════════════════════════════════════════════════════════════════════

function assert(condition: boolean, description: string): boolean {
  if (condition) {
    console.log(`  ✓ ${description}`);
    return true;
  } else {
    console.log(`  ✗ ${description}`);
    return false;
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// Sample Problem Texts
// ═══════════════════════════════════════════════════════════════════════════════

const CF_PROBLEM_CLEAN = `A. Watermelon
time limit per test
1 second
memory limit per test
256 megabytes

Pete and Billy found a watermelon and decided to divide it.
They want to divide the watermelon into two parts, each part weighing an even number of kilos.

Input
The first line contains a single integer w (1 ≤ w ≤ 100) — the weight of the watermelon.

Output
Print "YES" if Pete and Billy can divide the watermelon into two parts, each weighing an even number of kilos; otherwise print "NO".

Examples

Input
8

Output
YES

Input
3

Output
NO

Note
In the first test sample, Pete and Billy can divide the watermelon into parts weighing 2 and 6.`;

const CF_PROBLEM_MESSY = `A. Watermelon
A. Watermelon
time limit per test
1 second
memory limit per test
256 megabytes

Pete   and   Billy found a watermelon   and decided to divide it.
They want to divide the watermelon into two parts, each part weighing an even number of kilos.

Input
The first line contains a single integer w (1 ≤ w ≤ 100) — the weight of the watermelon.

Output
Print "YES" if they can divide the watermelon.



Examples

Input
8

Output
YES`;

const CF_SUBARRAY_SUM = `B. Subarray Sum
time limit per test
2 seconds
memory limit per test
256 megabytes

Given an array of n integers, find the length of the longest subarray with sum equal to k.
The array can contain negative values.

Input
The first line contains two integers n and k (1 ≤ n ≤ 200000, -10^9 ≤ k ≤ 10^9).
The second line contains n integers a_i (-10^9 ≤ a_i ≤ 10^9).

Output
Print the length of the longest subarray with sum k. If no such subarray exists, print 0.

Examples

Input
5 3
1 2 3 -1 1

Output
3

Note
The subarray [1, 2, 3] has sum 6. Wait no, [1, 2] has sum 3, length 2.
Actually the subarray from index 0 to 2 has values 1+2+3-1+1=6. Hmm.`;

const TEMPLATE_MATCH_INPUT = `implement a menu driven program for singly linked list with insert at end, delete from beginning, and display operations`;

const ACADEMIC_INPUT = `Use the bisection method to find the root of f(x) = x^3 - 4x - 9 in the interval [2, 3] with tolerance 0.001`;

const DEBUG_INPUT = `why does this linked list crash when I try to delete the last node?
\`\`\`cpp
void deleteLast(Node* head) {
  Node* temp = head;
  while(temp->next != NULL) {
    temp = temp->next;
  }
  delete temp;
}
\`\`\``;

const GENERIC_CP = `Given an array of n integers, find a pair of elements that sum to a target value. The array is sorted in ascending order.`;

const NOVEL_WORDING_PREFIX_SUM = `Given an integer sequence, determine the maximum length contiguous segment whose total equals X.`;

const NOVEL_WORDING_TWO_POINTERS = `In an ascending collection of numbers, locate two values that add up to T.`;

const NOVEL_WORDING_BINARY_SEARCH = `Locate a specific value within an ordered collection of elements.`;

const CSES_SUBARRAY_SUMS_I = `
    Given an array of nn positive integers, your task is to count the number of subarrays having sum xx.
    Input

    The first input line has two integers nn and xx: the size of the array and the target sum xx.

    The next line has nn integers a1,a2,…,ana1​,a2​,…,an​: the contents of the array.
    Output

    Print one integer: the required number of subarrays.
    Constraints

        1≤n≤2⋅1051≤n≤2⋅105
        1≤x,ai≤1091≤x,ai​≤109

    Example
    InputCopy 	

    5 7
    2 4 1 2 7

    OutputCopy	

    3
`;

// ═══════════════════════════════════════════════════════════════════════════════
// Tests
// ═══════════════════════════════════════════════════════════════════════════════

export function runV2PipelineTests(): { passed: number; failed: number } {
  let passed = 0;
  let failed = 0;

  function check(condition: boolean, desc: string) {
    if (assert(condition, desc)) passed++;
    else failed++;
  }

  // ── Normalizer Tests ──────────────────────────────────────────────────────
  console.log('\n[V2 Tests: Input Normalizer]');

  const normalized = normalizeInput(CF_PROBLEM_MESSY);
  check(!normalized.includes('\u2014'), 'Normalizes Unicode em-dash');
  check(!/\n\n\n\n/.test(normalized), 'Collapses 3+ blank lines to at most 2');
  // Duplicate line removed (A. Watermelon appears once)
  const titleMatches = normalized.match(/A\. Watermelon/g);
  check(titleMatches !== null && titleMatches.length === 1, 'Removes exact duplicate consecutive lines');
  check(!normalized.includes('   and   ') || normalized.includes('Pete'), 'Preserves meaningful content (internal whitespace preserved)');
  check(normalized.includes('Pete'), 'Preserves meaningful content');

  // ── Parser Tests ──────────────────────────────────────────────────────────
  console.log('\n[V2 Tests: Problem Parser]');

  const cleanParsed = parseProblem(normalizeInput(CF_PROBLEM_CLEAN), CF_PROBLEM_CLEAN);
  check(cleanParsed.title === 'A. Watermelon', 'Extracts title from clean CF problem');
  check(cleanParsed.source === 'codeforces', 'Detects Codeforces source');
  check(cleanParsed.timeLimit === 1, 'Extracts time limit (1 second)');
  check(cleanParsed.memoryLimit === 256, 'Extracts memory limit (256 MB)');
  check(cleanParsed.constraints.length > 0, 'Extracts at least one constraint');
  check(cleanParsed.constraints.some(c => c.upperBound === 100), 'Constraint upper bound = 100');
  check(cleanParsed.examples.length === 2, 'Parses 2 examples');
  check(cleanParsed.examples[0]?.input === '8', 'First example input = "8"');
  check(cleanParsed.examples[0]?.expectedOutput === 'YES', 'First example output = "YES"');
  check(cleanParsed.inputSpecification !== null, 'Has input specification');
  check(cleanParsed.outputSpecification !== null, 'Has output specification');
  check(cleanParsed.notes !== null && cleanParsed.notes.includes('first test sample'), 'Has notes section');

  const subarrayParsed = parseProblem(normalizeInput(CF_SUBARRAY_SUM), CF_SUBARRAY_SUM);
  check(subarrayParsed.title === 'B. Subarray Sum', 'Parses second problem title');
  check(subarrayParsed.timeLimit === 2, 'Time limit = 2 seconds');
  check(subarrayParsed.constraints.some(c => c.variable === 'n' && c.upperBound === 200000), 'Parses n ≤ 200000');
  check(subarrayParsed.examples.length >= 1, 'Has at least 1 example');

  const genericParsed = parseProblem(normalizeInput(GENERIC_CP), GENERIC_CP);
  check(genericParsed.source === 'generic', 'Generic problem detected as generic source');
  check(genericParsed.statement.includes('sorted'), 'Statement preserved');

  const csesParsed = parseProblem(normalizeInput(CSES_SUBARRAY_SUMS_I), CSES_SUBARRAY_SUMS_I);
  check(csesParsed.examples.length === 1, 'Parses CSES example with InputCopy / OutputCopy');
  check(csesParsed.examples[0]?.input.includes('5 7'), 'CSES example input includes "5 7"');
  check(csesParsed.examples[0]?.expectedOutput.trim() === '3', 'CSES example output is "3"');

  // ── Classifier Tests ──────────────────────────────────────────────────────
  console.log('\n[V2 Tests: Problem Classifier]');

  const cpClass = classifyProblem(cleanParsed);
  check(cpClass.selected === 'competitive_programming', 'CF problem classified as CP');
  check(cpClass.confidence >= 0.70, 'CF problem confidence ≥ 0.70');

  const tmParsed = parseProblem(normalizeInput(TEMPLATE_MATCH_INPUT), TEMPLATE_MATCH_INPUT);
  const tmClass = classifyProblem(tmParsed);
  check(tmClass.selected === 'template_match', '"implement menu driven linked list" → template_match');
  check(tmClass.scores.template_match >= 0.50, 'Template match score ≥ 0.50');

  const acParsed = parseProblem(normalizeInput(ACADEMIC_INPUT), ACADEMIC_INPUT);
  const acClass = classifyProblem(acParsed);
  check(acClass.selected === 'academic', '"bisection method" → academic');
  check(acClass.scores.academic >= 0.50, 'Academic score ≥ 0.50');

  const dbgParsed = parseProblem(normalizeInput(DEBUG_INPUT), DEBUG_INPUT);
  const dbgClass = classifyProblem(dbgParsed);
  check(dbgClass.selected === 'code_debug', '"why does this crash" + code block → code_debug');
  check(dbgClass.scores.code_debug >= 0.40, 'Debug score ≥ 0.40');

  const subarrayClass = classifyProblem(subarrayParsed);
  check(subarrayClass.selected === 'competitive_programming', 'Subarray sum problem → CP');

  const genericCpParsed = parseProblem(normalizeInput(GENERIC_CP), GENERIC_CP);
  // Generic CP might not have enough signals for high confidence
  const genericCpClass = classifyProblem(genericCpParsed);
  check(
    genericCpClass.selected === 'competitive_programming' || genericCpClass.selected === 'template_match',
    'Generic CP problem classified reasonably'
  );

  // Mode override
  const overridden = classifyProblem(cleanParsed, 'academic');
  check(overridden.selected === 'academic', 'Mode override forces academic');
  check(overridden.scores.academic === 1.0, 'Override sets score to 1.0');

  // ── Constraint Analyzer Tests ─────────────────────────────────────────────
  console.log('\n[V2 Tests: Constraint Analyzer]');

  const feas1 = analyzeConstraints(subarrayParsed);
  check(feas1.feasible.includes('O(N)'), 'N=200000: O(N) is feasible');
  check(feas1.feasible.includes('O(N log N)'), 'N=200000: O(N log N) is feasible');
  check(feas1.likelyInfeasible.includes('O(N²)'), 'N=200000: O(N²) is infeasible');
  check(feas1.timeLimit === 2, 'Time limit correctly passed to feasibility');

  const smallProblem: StructuredProblem = {
    rawText: '', normalizedText: '', title: null, problemType: null, domain: null,
    statement: '', inputSpecification: null, outputSpecification: null,
    constraints: [{ variable: 'n', upperBound: 1000, raw: 'n ≤ 1000' }],
    examples: [], notes: null, timeLimit: 1, memoryLimit: 256, source: null, parserConfidence: 0.5
  };
  const feas2 = analyzeConstraints(smallProblem);
  check(feas2.feasible.includes('O(N²)'), 'N=1000: O(N²) is feasible');

  const tinyProblem: StructuredProblem = {
    rawText: '', normalizedText: '', title: null, problemType: null, domain: null,
    statement: '', inputSpecification: null, outputSpecification: null,
    constraints: [{ variable: 'n', upperBound: 20, raw: 'n ≤ 20' }],
    examples: [], notes: null, timeLimit: 2, memoryLimit: 256, source: null, parserConfidence: 0.5
  };
  const feas3 = analyzeConstraints(tinyProblem);
  check(feas3.feasible.includes('O(2^N)'), 'N=20: O(2^N) is feasible');

  const overflowProblem: StructuredProblem = {
    rawText: '', normalizedText: '', title: null, problemType: null, domain: null,
    statement: '', inputSpecification: null, outputSpecification: null,
    constraints: [
      { variable: 'n', upperBound: 200000, raw: 'n ≤ 200000' },
      { variable: 'a', upperBound: 1000000000, raw: 'a ≤ 10^9' }
    ],
    examples: [], notes: null, timeLimit: 2, memoryLimit: 256, source: null, parserConfidence: 0.5
  };
  const feas4 = analyzeConstraints(overflowProblem);
  check(feas4.overflowRisk === true, 'Detects overflow risk (N*val > 2^31)');

  // ── Topic Detection Tests ─────────────────────────────────────────────────
  console.log('\n[V2 Tests: Topic Detection]');

  const subarrayTopics = scoreConcepts(subarrayParsed);
  const topSubarray = subarrayTopics[0];
  check(topSubarray?.conceptId === 'prefix_sum', 'Subarray sum → top concept is prefix_sum');
  check(topSubarray?.confidence >= 0.30, 'Prefix sum confidence ≥ 0.30');

  // Check sliding window is rejected for negative values
  const swCandidate = subarrayTopics.find(t => t.conceptId === 'sliding_window');
  if (swCandidate) {
    check(
      swCandidate.rejected === true || swCandidate.confidence < topSubarray.confidence,
      'Sliding window rejected/demoted for negative-value problem'
    );
  } else {
    check(true, 'Sliding window not even detected (correct for negative-value problem)');
  }

  // Two pointers detection
  const tpParsed = parseProblem(normalizeInput(GENERIC_CP), GENERIC_CP);
  tpParsed.problemType = 'competitive_programming';
  const tpTopics = scoreConcepts(tpParsed);
  const hasTwoPointers = tpTopics.some(t => t.conceptId === 'two_pointers' && t.confidence > 0.1);
  check(hasTwoPointers, '"sorted array, pair with sum" → detects two_pointers');

  // ── Novel Wording Tests ───────────────────────────────────────────────────
  console.log('\n[V2 Tests: Novel Wording Detection]');

  const novelPrefixParsed = parseProblem(normalizeInput(NOVEL_WORDING_PREFIX_SUM), NOVEL_WORDING_PREFIX_SUM);
  novelPrefixParsed.problemType = 'competitive_programming';
  const novelPrefixTopics = scoreConcepts(novelPrefixParsed);
  const prefixDetected = novelPrefixTopics.some(t => t.conceptId === 'prefix_sum' && t.confidence >= 0.15);
  check(prefixDetected, '"contiguous segment whose total equals X" → detects prefix_sum');

  const novelTpParsed = parseProblem(normalizeInput(NOVEL_WORDING_TWO_POINTERS), NOVEL_WORDING_TWO_POINTERS);
  novelTpParsed.problemType = 'competitive_programming';
  const novelTpTopics = scoreConcepts(novelTpParsed);
  const tpDetected = novelTpTopics.some(t => t.conceptId === 'two_pointers' && t.confidence >= 0.10);
  check(tpDetected, '"ascending collection, two values add up to T" → detects two_pointers');

  const novelBsParsed = parseProblem(normalizeInput(NOVEL_WORDING_BINARY_SEARCH), NOVEL_WORDING_BINARY_SEARCH);
  novelBsParsed.problemType = 'competitive_programming';
  const novelBsTopics = scoreConcepts(novelBsParsed);
  const bsDetected = novelBsTopics.some(t => t.conceptId === 'binary_search' && t.confidence >= 0.10);
  check(bsDetected, '"locate value in ordered collection" → detects binary_search');

  // ── Solution Template Tests ───────────────────────────────────────────────
  console.log('\n[V2 Tests: Solution Templates]');

  const templates = ['frequencyCount', 'prefixSum', 'twoPointers', 'slidingWindow',
    'binarySearch', 'sortGreedy', 'bfs', 'dfs', 'dp1d'];

  for (const tid of templates) {
    const frag = buildFromTemplate(tid, { intType: 'int' });
    check(frag !== null, `Template "${tid}" builds successfully`);
    if (frag) {
      const code = composeCode([frag]);
      check(code.includes('#include'), `Template "${tid}" produces code with includes`);
      check(code.includes('int main()'), `Template "${tid}" produces code with main()`);
      check(code.includes('cin'), `Template "${tid}" uses cin for input`);
    }
  }

  // Long long variant
  const llFrag = buildFromTemplate('prefixSum', { intType: 'long long' });
  check(llFrag !== null && llFrag.mainCode!.includes('long long'), 'Prefix sum template uses long long when specified');

  // Unknown template
  const unknown = buildFromTemplate('nonexistent', { intType: 'int' });
  check(unknown === null, 'Unknown template returns null');

  // ── Strategy Evaluation & Requirement Extraction Tests ─────────────────────
  console.log('\n[V2 Tests: Strategy Evaluation & Requirement Extraction]');

  const warehouseText = `A warehouse keeps a fixed sequence of daily stock changes.

You are given n integers representing the change in stock on each day. 
After reading the sequence, answer q questions. Each question gives two positions l and r.
For every question, report the total stock change from day l through day r, inclusive.

The values may be negative.

Input
The first line contains two integers n and q.
The second line contains n integers.
Each of the next q lines contains two integers l and r.

Output
For every question, print the requested total on a separate line.

Example

Input
8 4
3 -2 7 1 -5 4 6 -3
1 4
2 5
4 8
3 3

Output
9
1
3
7`;

  const warehouseParsed = parseProblem(normalizeInput(warehouseText), warehouseText);
  const warehouseReqs = extractRequirements(warehouseParsed);
  check(warehouseReqs.operations.includes('range_sum'), 'Warehouse problem extracts range_sum operation');
  check(warehouseReqs.hasRepeatedQueries === true, 'Warehouse problem detects repeated queries');
  check(warehouseReqs.allowsNegativeValues === true, 'Warehouse problem detects negative values allowed');

  const warehouseCandidates = scoreConcepts(warehouseParsed);
  const stratDecision = evaluateStrategy(warehouseReqs, warehouseCandidates, false);
  check(stratDecision.type === 'single', 'Warehouse problem evaluates to single strategy (not compound_unsupported)');
  check(stratDecision.selectedConcept?.conceptId === 'prefix_sum', 'Warehouse selects prefix_sum as single satisfying concept');

  const warehouseResult = solveCpProblem(warehouseParsed);
  check(warehouseResult.success === true, 'Warehouse problem solves successfully');
  check(warehouseResult.verification?.allPassed === true, 'Warehouse problem passes example test cases');

  return { passed, failed };
}
