/**
 * CHUP Batch 3 — Expanded Knowledge & Reasoning Test Suite.
 *
 * Tests the 10 expanded algorithmic and numerical domains:
 * 1. Monotonic Stack (Dominance elimination over sequences)
 * 2. Trie / Prefix Tree (Shared prefix transition tree)
 * 3. LRU Cache (Hash map + DLL composition)
 * 4. LFU Cache (Hash map + Frequency DLLs + Recency tie-break)
 * 5. Tree DP (Acyclic hierarchical post-order recurrence)
 * 6. Secant Root Finding
 * 7. Fixed-Point Iteration
 * 8. Lagrange Interpolation
 * 9. Simpson's 1/3 Integration
 * 10. Matrix Condition Number Estimate
 */

import { parseProblem } from '../pipeline/problemParser';
import { normalizeInput } from '../pipeline/inputNormalizer';
import { extractRequirements } from '../pipeline/requirementExtractor';
import { solveCpProblem } from '../solver/cpSolver';
import { generateCpp } from '../generator/cppGenerator';
import { ProblemSpecV1, ResolutionResult } from '../models/problemSpec';
import { verifyCode } from '../verifier/verificationEngine';
import { loadRegistry, lookupNumericalMethod } from '../knowledge/registry';

function makeNumericalSpec(method: string, category: string, moduleId: string): ResolutionResult {
  const spec: ProblemSpecV1 = {
    status: 'success',
    language: 'cpp',
    domain: 'numerical',
    intent: 'code_generation',
    structure: { type: null, confidence_basis: 'exact_rule_match' },
    operation: { action: method, position: null, combined: method, negated: false },
    compound: { is_compound: false, detected_actions: [] },
    numerical: { method, category },
    confidence: 1.0,
    confidence_basis: 'exact_rule_match',
    error_code: null,
    message: '',
    raw_query: `Run ${method}`,
    normalized_query: `run ${method}`
  };
  return {
    code: 'SUCCESS',
    moduleId,
    moduleName: method,
    message: 'Resolved',
    spec
  };
}

export function runBatch3ExpansionTests(): { passed: number; failed: number } {
  let passed = 0;
  let failed = 0;

  function assert(condition: boolean, description: string): boolean {
    if (condition) {
      console.log(`  ✓ ${description}`);
      passed++;
      return true;
    } else {
      console.error(`  ✗ ${description}`);
      failed++;
      return false;
    }
  }

  loadRegistry();

  console.log('\n=================================================');
  console.log('   CHUP Batch 3: Expanded Knowledge Test Suite   ');
  console.log('=================================================');

  // ── 1. Monotonic Stack ──────────────────────────────────────────────────────
  console.log('\n[Phase 3B: Monotonic Stack]');
  const textMono = `Given an array of n integers, your task is to find for each array position the nearest smaller value to its left.
Input:
8
2 5 1 4 8 3 2 5
Output:
0 1 0 3 4 3 3 7`;

  const parsedMono = parseProblem(normalizeInput(textMono), textMono);
  const reqsMono = extractRequirements(parsedMono);
  assert(reqsMono.operations.includes('monotonic_stack'), 'Monotonic stack operation extracted');
  assert(reqsMono.operations.includes('nearest_smaller_values'), 'Nearest smaller values operation extracted');

  const resMono = solveCpProblem(parsedMono);
  assert(resMono.success === true, 'Monotonic stack problem solved and verified against sample');
  assert(resMono.code.includes('<stack>'), 'Monotonic stack includes <stack>');
  assert(resMono.selectedAlgorithm === 'monotonic_stack', 'Selected concept is monotonic_stack');

  // ── 2. Trie / Prefix Tree ──────────────────────────────────────────────────
  console.log('\n[Phase 3C: Trie / Prefix Tree]');
  const textTrie = `Build a prefix tree (trie) from a dictionary of words. Support queries to search words and check starts with prefix.
Input:
3 3
apple app banana
1 app
2 app
1 ban
Output:
YES
YES
NO`;

  const parsedTrie = parseProblem(normalizeInput(textTrie), textTrie);
  const reqsTrie = extractRequirements(parsedTrie);
  assert(reqsTrie.operations.includes('prefix_tree'), 'Prefix tree operation extracted');

  const resTrie = solveCpProblem(parsedTrie);
  assert(resTrie.success === true, 'Trie problem solved and verified against sample');
  assert(resTrie.code.includes('struct TrieNode') && resTrie.code.includes('class Trie'), 'Generated C++ has complete Trie implementation');
  assert(resTrie.selectedAlgorithm === 'trie', 'Selected concept is trie');

  // ── 3. LRU Cache ───────────────────────────────────────────────────────────
  console.log('\n[Phase 3D: LRU Cache]');
  const textLru = `Design an LRU cache with capacity limit and O(1) get and put operations with eviction of least recently used.
Input:
2 6
put 1 10
put 2 20
get 1
put 3 30
get 2
get 3
Output:
10
-1
30`;

  const parsedLru = parseProblem(normalizeInput(textLru), textLru);
  const reqsLru = extractRequirements(parsedLru);
  assert(reqsLru.operations.includes('lru_cache'), 'LRU cache operation extracted');

  const resLru = solveCpProblem(parsedLru);
  assert(resLru.success === true, 'LRU cache problem solved and verified against sample');
  assert(resLru.code.includes('class LRUCache'), 'Generated C++ contains LRUCache class');
  assert(resLru.code.includes('<list>') && resLru.code.includes('<unordered_map>'), 'LRU Cache composes list and unordered_map');
  assert(resLru.selectedAlgorithm === 'lru_cache', 'Selected concept is lru_cache');

  // ── 4. LFU Cache ───────────────────────────────────────────────────────────
  console.log('\n[Phase 3E: LFU Cache]');
  const textLfu = `Design a least frequently used LFU cache with capacity eviction and LRU tie breaking.
Input:
2 6
put 1 10
put 2 20
get 1
put 3 30
get 2
get 3
Output:
10
-1
30`;

  const parsedLfu = parseProblem(normalizeInput(textLfu), textLfu);
  const reqsLfu = extractRequirements(parsedLfu);
  assert(reqsLfu.operations.includes('lfu_cache'), 'LFU cache operation extracted');

  const resLfu = solveCpProblem(parsedLfu);
  assert(resLfu.success === true, 'LFU cache problem solved and verified against sample');
  assert(resLfu.code.includes('class LFUCache'), 'Generated C++ contains LFUCache class');
  assert(resLfu.selectedAlgorithm === 'lfu_cache', 'Selected concept is lfu_cache');

  // ── 5. Tree DP ─────────────────────────────────────────────────────────────
  console.log('\n[Phase 3F: Tree DP]');
  const textTree = `Calculate the tree diameter, defined as the longest path between any two vertices in an unweighted tree.
Input:
5
1 2
1 3
3 4
4 5
Output:
4`;

  const parsedTree = parseProblem(normalizeInput(textTree), textTree);
  const reqsTree = extractRequirements(parsedTree);
  assert(reqsTree.operations.includes('tree_dp'), 'Tree DP operation extracted');

  const resTree = solveCpProblem(parsedTree);
  assert(resTree.success === true, 'Tree DP problem solved and verified against sample');
  assert(resTree.code.includes('dfsDiameter'), 'Generated C++ has post-order tree DP recurrence');
  assert(resTree.selectedAlgorithm === 'tree_dp', 'Selected concept is tree_dp');

  // ── 6-10. Numerical Methods ────────────────────────────────────────────────
  console.log('\n[Phase 3G: Numerical Expansion]');

  // 6. Secant
  const secantEntry = lookupNumericalMethod('secant');
  assert(secantEntry !== null, 'Secant method registered in knowledge base');
  const secantCode = generateCpp(makeNumericalSpec('secant', 'root_finding', 'numerical.root_finding.secant.cpp'));
  assert(secantCode.includes('secant') || secantCode.includes('evaluate'), 'Secant code generated');
  const vSecant = verifyCode(secantCode, []);
  assert(vSecant.compiled, 'Secant generated C++ compiles successfully');

  // 7. Fixed-Point Iteration
  const fpEntry = lookupNumericalMethod('fixed_point_iteration');
  assert(fpEntry !== null, 'Fixed-point iteration registered in knowledge base');
  const fpCode = generateCpp(makeNumericalSpec('fixed_point_iteration', 'root_finding', 'numerical.root_finding.fixed_point_iteration.cpp'));
  assert(fpCode.includes('evaluate'), 'Fixed-point iteration code generated');
  const vFp = verifyCode(fpCode, []);
  assert(vFp.compiled, 'Fixed-point iteration generated C++ compiles successfully');

  // 8. Lagrange Interpolation
  const lagrangeEntry = lookupNumericalMethod('lagrange');
  assert(lagrangeEntry !== null, 'Lagrange interpolation registered in knowledge base');
  const lagrangeCode = generateCpp(makeNumericalSpec('lagrange', 'interpolation', 'numerical.interpolation.lagrange.cpp'));
  assert(lagrangeCode.includes('lagrange') || lagrangeCode.includes('term'), 'Lagrange code generated');
  const vLagrange = verifyCode(lagrangeCode, []);
  assert(vLagrange.compiled, 'Lagrange generated C++ compiles successfully');

  // 9. Simpson's 1/3
  const simpsonEntry = lookupNumericalMethod('simpson_1_3');
  assert(simpsonEntry !== null, 'Simpson 1/3 registered in knowledge base');
  const simpsonCode = generateCpp(makeNumericalSpec('simpson_1_3', 'integration', 'numerical.integration.simpson_1_3.cpp'));
  assert(simpsonCode.includes('simpson') || simpsonCode.includes('evaluate'), 'Simpson 1/3 code generated');
  const vSimpson = verifyCode(simpsonCode, []);
  assert(vSimpson.compiled, 'Simpson 1/3 generated C++ compiles successfully');

  // 10. Matrix Condition Number
  const condEntry = lookupNumericalMethod('condition_number');
  assert(condEntry !== null, 'Condition number registered in knowledge base');
  const condCode = generateCpp(makeNumericalSpec('condition_number', 'linear_systems', 'numerical.linear_systems.condition_number.cpp'));
  assert(condCode.includes('computeConditionNumber'), 'Condition number code generated');
  const vCond = verifyCode(condCode, []);
  assert(vCond.compiled, 'Condition number generated C++ compiles successfully');

  return { passed, failed };
}
