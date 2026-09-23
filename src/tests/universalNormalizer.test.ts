/**
 * CHUP / Offcode — Universal Normalizer Test Suite
 *
 * Verifies the 20 Invariants of Phase 1 Universal Input Normalization:
 * 1. Target example
 * 2. False positive protection
 * 3. Ambiguous typo / Non-mutation
 * 4. Short-token protection
 * 5. Phrase precedence (longest-match-first)
 * 6. Case normalization without false evidence
 * 7. Punctuation & hyphenation
 * 8. Repeated terms determinism
 * 9. No semantic invention
 * 10. Provenance invariant
 * 11. Academic/CP domain separation
 * 12. Normalization idempotence
 * 13. Deterministic output
 * 14. Correction collision protection
 */

import * as assert from 'assert';
import { normalizeInputUniversal } from '../pipeline/universalNormalizer';
import { parseProblem } from '../pipeline/problemParser';
import { classifyProblem } from '../pipeline/problemClassifier';

export function runUniversalNormalizerTests(): { passed: number; failed: number } {
  console.log('=================================================');
  console.log('   CHUP Phase 1: Universal Normalizer Suite      ');
  console.log('=================================================\n');

  let passed = 0;
  let failed = 0;

  function runTest(name: string, fn: () => void) {
    try {
      fn();
      passed++;
      console.log(`  ✓ ${name}`);
    } catch (err: any) {
      failed++;
      console.error(`  ✗ ${name}`);
      console.error(`    ${err.message}`);
    }
  }

// ── 1. Target Example ──────────────────────────────────────────────────────────
runTest('1. Target Example: "insert a node at the end of a singly lincked list"', () => {
  const raw = 'insert a node at the end of a singly lincked list';
  const res = normalizeInputUniversal(raw);

  assert.strictEqual(res.originalText, raw, 'originalText must remain immutable');
  assert.strictEqual(res.normalizedText, 'insert a node at the end of a singly linked list');
  assert.strictEqual(res.corrections.length, 1, 'Exactly one correction expected');
  assert.strictEqual(res.corrections[0].original, 'lincked');
  assert.strictEqual(res.corrections[0].corrected, 'linked');
  assert.strictEqual(res.corrections[0].startToken, 9);
  assert.strictEqual(res.corrections[0].endToken, 10);
  assert.ok(res.corrections[0].confidence >= 0.80, 'Confidence must be >= 0.80');

  const canonicals = res.canonicalTerms.map(t => t.canonical);
  assert.ok(canonicals.includes('insert'), 'Must contain insert');
  assert.ok(canonicals.includes('node'), 'Must contain node');
  assert.ok(canonicals.includes('tail'), 'Must contain tail/end');
  assert.ok(canonicals.includes('singly_linked_list'), 'Must contain singly_linked_list');
});

// ── 2. False-Positive Protection ──────────────────────────────────────────────
runTest('2. False Positive: "implement stack using array" unchanged', () => {
  const raw = 'implement stack using array';
  const res = normalizeInputUniversal(raw);

  assert.strictEqual(res.normalizedText, 'implement stack using array');
  assert.strictEqual(res.corrections.length, 0, 'No corrections should be made to valid words');
  assert.strictEqual(res.normalizationConfidence, 1.0, 'Confidence must be 1.0');
});

// ── 3. Ambiguous Typo / Non-Mutation ──────────────────────────────────────────
runTest('3. Ambiguous Typo: "implement a set" must not mutate set', () => {
  const raw = 'implement a set';
  const res = normalizeInputUniversal(raw);

  assert.strictEqual(res.normalizedText, 'implement a set');
  assert.strictEqual(res.corrections.length, 0, 'Short word set must never be mutated');
});

// ── 4. Short-Token Protection ─────────────────────────────────────────────────
runTest('4. Short-Token Protection: map, set, get, tree, node, stack, top, pop', () => {
  const raw = 'use a map and set to get tree node and stack top or pop';
  const res = normalizeInputUniversal(raw);

  assert.strictEqual(res.corrections.length, 0, 'No short tokens should be mutated');
  assert.strictEqual(res.normalizationConfidence, 1.0);
  assert.ok(res.tokens.includes('map'));
  assert.ok(res.tokens.includes('set'));
  assert.ok(res.tokens.includes('get'));
  assert.ok(res.tokens.includes('tree'));
  assert.ok(res.tokens.includes('stack'));
});

// ── 5. Phrase Precedence (Longest-Match-First) ────────────────────────────────
runTest('5. Phrase Precedence: "singly linked list" extracted as single canonical concept', () => {
  const raw = 'singly linked list';
  const res = normalizeInputUniversal(raw);

  assert.strictEqual(res.canonicalTerms.length, 1, 'Must extract exactly one multi-word canonical term');
  assert.strictEqual(res.canonicalTerms[0].canonical, 'singly_linked_list');
  assert.strictEqual(res.canonicalTerms[0].surfaceForm, 'singly linked list');
  assert.strictEqual(res.canonicalTerms[0].startToken, 0);
  assert.strictEqual(res.canonicalTerms[0].endToken, 3);
});

runTest('5b. Phrase Precedence: "lu decomposition" precedes independent lu and decomposition', () => {
  const raw = 'solve linear system using lu decomposition method';
  const res = normalizeInputUniversal(raw);

  const luTerm = res.canonicalTerms.find(t => t.canonical === 'lu_decomposition');
  assert.ok(luTerm !== undefined, 'Must extract lu_decomposition');
  assert.strictEqual(luTerm!.surfaceForm, 'lu decomposition');
  assert.strictEqual(luTerm!.endToken - luTerm!.startToken, 2, 'Must span 2 tokens');
});

// ── 6. Case Normalization Without False Evidence ──────────────────────────────
runTest('6. Case Normalization: "LU DeCoMpOsItIoN" records 0 spelling corrections', () => {
  const raw = 'LU DeCoMpOsItIoN';
  const res = normalizeInputUniversal(raw);

  assert.strictEqual(res.originalText, 'LU DeCoMpOsItIoN', 'originalText preserved');
  assert.strictEqual(res.normalizedText, 'lu decomposition');
  assert.strictEqual(res.corrections.length, 0, 'Casing differences must not be recorded as spelling corrections');
  assert.strictEqual(res.normalizationConfidence, 1.0);
  assert.strictEqual(res.canonicalTerms[0].canonical, 'lu_decomposition');
});

// ── 7. Punctuation & Hyphenation ──────────────────────────────────────────────
runTest('7. Punctuation: "Insert a node at the end, of a singly-linked list."', () => {
  const raw = 'Insert a node at the end, of a singly-linked list.';
  const res = normalizeInputUniversal(raw);

  assert.strictEqual(res.originalText, raw, 'originalText untouched with punctuation');
  assert.strictEqual(res.normalizedText, 'insert a node at the end of a singly linked list');
  assert.strictEqual(res.corrections.length, 0, 'Valid words with punctuation/hyphens have 0 corrections');
  const canonicals = res.canonicalTerms.map(t => t.canonical);
  assert.ok(canonicals.includes('singly_linked_list'));
  assert.ok(canonicals.includes('tail'));
});

// ── 8. Repeated Terms Determinism ─────────────────────────────────────────────
runTest('8. Repeated Terms: "insert insert node node" token spans deterministic', () => {
  const raw = 'insert insert node node';
  const res = normalizeInputUniversal(raw);

  assert.strictEqual(res.canonicalTerms.length, 4);
  assert.deepStrictEqual(
    res.canonicalTerms.map(t => ({ c: t.canonical, s: t.startToken, e: t.endToken })),
    [
      { c: 'insert', s: 0, e: 1 },
      { c: 'insert', s: 1, e: 2 },
      { c: 'node', s: 2, e: 3 },
      { c: 'node', s: 3, e: 4 }
    ]
  );
});

// ── 9. No Semantic Invention ──────────────────────────────────────────────────
runTest('9. No Semantic Invention: "insert a node" does NOT invent singly_linked_list', () => {
  const raw = 'insert a node';
  const res = normalizeInputUniversal(raw);

  const canonicals = res.canonicalTerms.map(t => t.canonical);
  assert.deepStrictEqual(canonicals, ['insert', 'node'], 'Only genuine stated concepts may be extracted');
  assert.ok(!canonicals.includes('singly_linked_list'), 'Must never invent singly_linked_list');
});

// ── 10. Provenance Invariant ──────────────────────────────────────────────────
runTest('10. Provenance Invariant: correction.original exists at startToken in original stream', () => {
  const raw = 'create doubly lincked list insert serch node';
  const res = normalizeInputUniversal(raw);

  assert.ok(res.corrections.length >= 2, 'Should correct lincked and serch');

  for (const c of res.corrections) {
    assert.ok(c.startToken < c.endToken, 'startToken must be strictly less than endToken');
    assert.strictEqual(c.endToken, c.startToken + 1, 'Single-token correction span must be 1');
    assert.strictEqual(res.tokens[c.startToken], c.corrected, 'Corrected word must exist in normalizedTokens');
  }
});

// ── 11. Academic / CP Domain Separation ───────────────────────────────────────
runTest('11. Academic / CP Separation: "implement lu dcomposition method" never enters CP', () => {
  const raw = 'implement lu dcomposition method';
  const normInput = normalizeInputUniversal(raw);
  const problem = parseProblem(normInput.normalizedText, raw, normInput);
  const classification = classifyProblem(problem);

  assert.strictEqual(classification.status, 'classified', 'Must be classified');
  assert.strictEqual(classification.selected, 'academic', 'Must be classified as academic');
  const selectedRoute: string | null = classification.selected;
  assert.ok(selectedRoute !== 'competitive_programming', 'Must NEVER be competitive_programming');
  assert.ok(classification.confidence >= 0.50, 'Academic score must be >= 0.50');
});

// ── 12. Normalization Idempotence ─────────────────────────────────────────────
runTest('12. Idempotence: normalize(normalize(x).normalizedText).corrections === []', () => {
  const inputs = [
    'insert a node at the end of a singly lincked list',
    'implement lu dcomposition method',
    'creat doubly likned list insert afetr node',
    'find element using binery serch'
  ];

  for (const raw of inputs) {
    const firstPass = normalizeInputUniversal(raw);
    const secondPass = normalizeInputUniversal(firstPass.normalizedText);

    assert.strictEqual(
      secondPass.corrections.length,
      0,
      `Idempotence failed on '${raw}': second pass produced corrections: ${JSON.stringify(secondPass.corrections)}`
    );
    assert.strictEqual(
      secondPass.normalizedText,
      firstPass.normalizedText,
      `Idempotence failed: text mutated between passes`
    );
  }
});

// ── 13. Deterministic Output ──────────────────────────────────────────────────
runTest('13. Deterministic Output: repeated runs on identical input are deeply equal', () => {
  const query = 'implement lu dcomposition method and insert at the beggining of singly lincked list';
  const run1 = normalizeInputUniversal(query);
  const run2 = normalizeInputUniversal(query);
  const run3 = normalizeInputUniversal(query);

  assert.deepStrictEqual(run1, run2, 'Run 1 and Run 2 must be deeply equal');
  assert.deepStrictEqual(run2, run3, 'Run 2 and Run 3 must be deeply equal');
});

// ── 14. Correction Collision Protection ───────────────────────────────────────
runTest('14. Correction Collision Protection: stack never becomes slack, tree never becomes free', () => {
  const protectedQueries = [
    'implement a stack',
    'create a tree',
    'find node in heap',
    'get map and set'
  ];

  for (const q of protectedQueries) {
    const res = normalizeInputUniversal(q);
    assert.strictEqual(res.corrections.length, 0, `Query '${q}' had unexpected corrections`);
    assert.strictEqual(res.normalizedText, q);
  }
});

  console.log(`\nUniversal Normalizer Summary: ${passed} passed, ${failed} failed.\n`);
  return { passed, failed };
}

if (require.main === module) {
  const result = runUniversalNormalizerTests();
  if (result.failed > 0) {
    process.exit(1);
  }
}
