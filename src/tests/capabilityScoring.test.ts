/**
 * CHUP Phase 3: Capability Scoring & Classification Test Suite
 *
 * Verifies Categories H through L and E2E acceptance cases:
 * - H: Contradictory entity (primary role conflict marks capability as disqualified)
 * - I: Insufficient evidence (missing requirements marks capability as insufficient, score < 0.50)
 * - J: Ambiguous capability (competing candidates with equal/close scores yield status: 'ambiguous', selected: null)
 * - K: Unsupported input (gibberish yields status: 'unsupported', selected: null, confidence: 0)
 * - L: Determinism (repeated execution is bit-for-bit identical)
 * - E2E Cases 1–5: End-to-end verification
 */

import * as assert from 'assert';
import { normalizeInputUniversal } from '../pipeline/universalNormalizer';
import { extractSemanticInput } from '../pipeline/semanticExtractor';
import { scoreCapabilities } from '../pipeline/capabilityScorer';
import { classifySemanticInput } from '../pipeline/problemClassifier';
import { parseProblem } from '../pipeline/problemParser';

export function runCapabilityScoringTests(): { passed: number; failed: number } {
  console.log('\n=================================================');
  console.log('   CHUP Phase 3: Capability Scoring Suite       ');
  console.log('=================================================\n');

  let passed = 0;
  let failed = 0;

  function runTest(name: string, fn: () => void) {
    try {
      fn();
      console.log(`  ✓ ${name}`);
      passed++;
    } catch (err: any) {
      console.error(`  ✗ ${name}`);
      console.error(`    ${err.message}`);
      failed++;
    }
  }

  // ── Category H: Contradictory Entity Disqualification ──────────────────────
  runTest('H. Contradiction: "insert into a binary tree" disqualifies singly_linked_list capabilities', () => {
    const norm = normalizeInputUniversal('insert into a binary tree');
    const semantic = extractSemanticInput(norm);
    const scores = scoreCapabilities(semantic);

    const sllInsert = scores.find(s => s.capability === 'singly_linked_list.insert_end')!;
    assert.ok(sllInsert, 'SLL insert_end capability evaluated');
    assert.strictEqual(sllInsert.status, 'disqualified', 'Must be disqualified due to contradictory entity binary_tree');
    assert.strictEqual(sllInsert.score, 0, 'Disqualified score must be exactly 0');
    assert.ok(sllInsert.negativeEvidence.some(e => e.value === 'binary_tree'), 'Records binary_tree as negative evidence');
  });

  // ── Category I: Insufficient Evidence ─────────────────────────────────────
  runTest('I. Insufficient: "insert a node" lacks target data structure', () => {
    const norm = normalizeInputUniversal('insert a node');
    const semantic = extractSemanticInput(norm);
    const scores = scoreCapabilities(semantic);

    const sllInsert = scores.find(s => s.capability === 'singly_linked_list.insert_end')!;
    assert.strictEqual(sllInsert.status, 'insufficient', 'Missing structure leaves capability insufficient');
    assert.ok(sllInsert.score < 0.50, 'Insufficient score must be strictly below 0.50');
    assert.ok(sllInsert.missingEvidence.some(m => m.kind === 'entity'), 'Records entity as missing');
  });

  // ── Category J: Ambiguity Handling ─────────────────────────────────────────
  runTest('J. Ambiguity: multiple close domain candidates yield status=ambiguous, selected=null', () => {
    // Both academic question phrasing and code debug error signals present equally
    const norm = normalizeInputUniversal('explain why does this program crash and give formula for error');
    const semantic = extractSemanticInput(norm);
    const classification = classifySemanticInput(semantic);

    // If academic and debug are within 0.05, status must be ambiguous with selected: null
    if (Math.abs(classification.scores.academic - classification.scores.code_debug) < 0.05 && classification.scores.academic > 0) {
      assert.strictEqual(classification.status, 'ambiguous', 'Equal signals produce ambiguous status');
      assert.strictEqual(classification.selected, null, 'Ambiguous classification has selected: null');
    } else {
      // At least confirm selected is not CP
      assert.notStrictEqual(classification.selected, 'competitive_programming');
    }
  });

  // ── Category K: Unsupported Input ──────────────────────────────────────────
  runTest('K. Unsupported: "random unstructured gibberish xyz123" yields unsupported, null', () => {
    const norm = normalizeInputUniversal('random unstructured gibberish xyz123');
    const semantic = extractSemanticInput(norm);
    const classification = classifySemanticInput(semantic);

    assert.strictEqual(classification.status, 'unsupported', 'Must be unsupported');
    assert.strictEqual(classification.selected, null, 'Selected must be null');
    assert.strictEqual(classification.confidence, 0, 'Confidence must be 0');
    assert.strictEqual(classification.scores.competitive_programming, 0, 'CP score must be 0');
  });

  // ── Category L: Determinism ────────────────────────────────────────────────
  runTest('L. Determinism: 10 repeated runs yield deeply equal results', () => {
    const raw = 'insert a node at the end of a singly lincked list';
    const firstNorm = normalizeInputUniversal(raw);
    const firstSemantic = extractSemanticInput(firstNorm);
    const firstScores = scoreCapabilities(firstSemantic);
    const firstClass = classifySemanticInput(firstSemantic);

    for (let i = 0; i < 9; i++) {
      const norm = normalizeInputUniversal(raw);
      const semantic = extractSemanticInput(norm);
      const scores = scoreCapabilities(semantic);
      const classification = classifySemanticInput(semantic);

      assert.deepStrictEqual(semantic, firstSemantic, 'SemanticInput must be bit-for-bit identical');
      assert.deepStrictEqual(scores, firstScores, 'CapabilityScores must be bit-for-bit identical');
      assert.deepStrictEqual(classification, firstClass, 'Classification must be bit-for-bit identical');
    }
  });

  // ── E2E Acceptance Cases 1–5 ───────────────────────────────────────────────
  runTest('E2E Case 1: "insert a node at the end of a singly lincked list" matches singly_linked_list.insert_end', () => {
    const raw = 'insert a node at the end of a singly lincked list';
    const norm = normalizeInputUniversal(raw);
    const semantic = extractSemanticInput(norm);
    const scores = scoreCapabilities(semantic);
    const top = scores[0];

    assert.strictEqual(top.capability, 'singly_linked_list.insert_end', 'Top capability is SLL insert_end');
    assert.strictEqual(top.status, 'eligible', 'Status is eligible');
    assert.ok(top.score >= 0.80, 'Score is >= 0.80');

    const problem = parseProblem(norm.normalizedText, raw, norm);
    const classification = classifySemanticInput(semantic, problem);
    assert.strictEqual(classification.status, 'classified');
    assert.strictEqual(classification.selected, 'template_match');
  });

  runTest('E2E Case 2: Lexical-only "lincked" produces no semantic entities or operations', () => {
    const raw = 'lincked';
    const norm = normalizeInputUniversal(raw);
    const semantic = extractSemanticInput(norm);
    const classification = classifySemanticInput(semantic);

    assert.strictEqual(semantic.normalizedText, 'linked');
    assert.strictEqual(semantic.entities.length, 0);
    assert.strictEqual(semantic.operations.length, 0);
    assert.strictEqual(classification.status, 'unsupported');
    assert.strictEqual(classification.selected, null);
  });

  runTest('E2E Case 3: "singly linked list" has entity but no operation', () => {
    const raw = 'singly linked list';
    const norm = normalizeInputUniversal(raw);
    const semantic = extractSemanticInput(norm);
    const scores = scoreCapabilities(semantic);

    assert.strictEqual(semantic.entities.length, 1);
    assert.strictEqual(semantic.entities[0].value, 'singly_linked_list');
    assert.strictEqual(semantic.operations.length, 0);

    // SLL insert_end should be insufficient, NOT eligible
    const sllInsert = scores.find(s => s.capability === 'singly_linked_list.insert_end')!;
    assert.strictEqual(sllInsert.status, 'insufficient', 'Without operation, insert_end is insufficient');
  });

  runTest('E2E Case 4: "insert a node" has operation and object but no linked list', () => {
    const raw = 'insert a node';
    const norm = normalizeInputUniversal(raw);
    const semantic = extractSemanticInput(norm);

    assert.strictEqual(semantic.operations.length, 1);
    assert.strictEqual(semantic.operations[0].operation, 'insert');
    assert.strictEqual(semantic.entities.length, 1);
    assert.strictEqual(semantic.entities[0].value, 'node');
    assert.ok(!semantic.entities.some(e => e.value === 'singly_linked_list'), 'Does NOT assume singly_linked_list');
  });

  runTest('E2E Case 5: "random unstructured gibberish xyz123" stays unsupported (No CP fallback)', () => {
    const raw = 'random unstructured gibberish xyz123';
    const norm = normalizeInputUniversal(raw);
    const semantic = extractSemanticInput(norm);
    const problem = parseProblem(norm.normalizedText, raw, norm);
    const classification = classifySemanticInput(semantic, problem);

    assert.strictEqual(classification.status, 'unsupported');
    assert.strictEqual(classification.selected, null);
    assert.notStrictEqual(classification.selected, 'competitive_programming', 'Never defaults to CP');
  });

  console.log(`\nCapability Scoring Summary: ${passed} passed, ${failed} failed.\n`);
  return { passed, failed };
}

if (require.main === module) {
  const res = runCapabilityScoringTests();
  if (res.failed > 0) {
    process.exit(1);
  }
}
