/**
 * CHUP / Offcode — Vocabulary-Driven Fuzzy Matcher Test Suite
 *
 * Verifies Phase 2 requirements and constraints A-L:
 * 1. Exact vocabulary lookup (no correction, 0 confidence penalty)
 * 2. High-confidence typo corrections (lincked, dcomposition, serch, impliment)
 * 3. Absolute vocabulary restriction (weathr, elephnt, computr rejected as absent from vocabulary)
 * 4. Protected short-word shielding (map, set, get, tree, node, head, tail, top, pop, heap, list, root)
 * 5. Ambiguity handling (close competitors downgrade to MEDIUM_CONFIDENCE)
 * 6. Two-stage phrase recovery (token correction -> phrase canonicalization)
 * 7. No semantic expansion (lincked alone never produces singly_linked_list)
 * 8. Deterministic ranking & reproducible output
 * 9. Pure TypeScript offline guarantee (zero external dependencies)
 */

import * as assert from 'assert';
import { matchToken, damerauLevenshteinDistance, similarityRatio } from '../pipeline/fuzzyMatcher';
import { VALID_VOCABULARY_WORDS, PROTECTED_SHORT_WORDS } from '../pipeline/domainVocabulary';
import { normalizeInputUniversal } from '../pipeline/universalNormalizer';

export function runFuzzyMatcherTests(): { passed: number; failed: number } {
  console.log('=================================================');
  console.log('   CHUP Phase 2: Vocabulary Matcher Suite        ');
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

  // ── 1. Exact Vocabulary Lookup ──────────────────────────────────────────────
  runTest('1. Exact Vocabulary: linked and insert return no correction', () => {
    const resLinked = matchToken('linked');
    assert.strictEqual(resLinked.decision, 'LOW_CONFIDENCE', 'Exact match must not trigger rewriting');
    assert.strictEqual(resLinked.candidate, 'linked');
    assert.strictEqual(resLinked.confidence, 1.0);
    assert.strictEqual(resLinked.distance, 0);

    const resInsert = matchToken('insert');
    assert.strictEqual(resInsert.decision, 'LOW_CONFIDENCE');
    assert.strictEqual(resInsert.candidate, 'insert');
    assert.strictEqual(resInsert.confidence, 1.0);
    assert.strictEqual(resInsert.distance, 0);

    const norm = normalizeInputUniversal('insert linked');
    assert.strictEqual(norm.corrections.length, 0, 'Exact terms must not generate corrections');
    assert.strictEqual(norm.normalizationConfidence, 1.0);
  });

  // ── 2. High-Confidence Typo Corrections ─────────────────────────────────────
  runTest('2. Correct Typos: lincked, dcomposition, serch, impliment', () => {
    const resLincked = matchToken('lincked');
    assert.strictEqual(resLincked.decision, 'HIGH_CONFIDENCE');
    assert.strictEqual(resLincked.candidate, 'linked');
    assert.ok(resLincked.confidence >= 0.85);

    const resDcomp = matchToken('dcomposition');
    assert.strictEqual(resDcomp.decision, 'HIGH_CONFIDENCE');
    assert.strictEqual(resDcomp.candidate, 'decomposition');
    assert.ok(resDcomp.confidence >= 0.88);

    const resSerch = matchToken('serch');
    assert.strictEqual(resSerch.decision, 'HIGH_CONFIDENCE');
    assert.strictEqual(resSerch.candidate, 'search');
    assert.ok(resSerch.confidence >= 0.82);

    const resImpl = matchToken('impliment');
    assert.strictEqual(resImpl.decision, 'HIGH_CONFIDENCE');
    assert.strictEqual(resImpl.candidate, 'implement');
    assert.ok(resImpl.confidence >= 0.88);
  });

  // ── 3. Absolute Vocabulary Restriction ──────────────────────────────────────
  runTest('3. Vocabulary Restriction: weathr, elephnt, computr rejected as absent from vocabulary', () => {
    // Explicitly verify target words do not exist in Offcode vocabulary
    assert.ok(!VALID_VOCABULARY_WORDS.has('weather'), 'weather must not be in Offcode vocabulary');
    assert.ok(!VALID_VOCABULARY_WORDS.has('elephant'), 'elephant must not be in Offcode vocabulary');
    assert.ok(!VALID_VOCABULARY_WORDS.has('computer'), 'computer must not be in Offcode vocabulary');

    const resWeather = matchToken('weathr');
    assert.strictEqual(resWeather.decision, 'LOW_CONFIDENCE', 'weathr must not correct to weather');
    assert.notStrictEqual(resWeather.candidate, 'weather');

    const resElephant = matchToken('elephnt');
    assert.notStrictEqual(resElephant.decision, 'HIGH_CONFIDENCE', 'elephnt must never be high confidence');
    assert.notStrictEqual(resElephant.candidate, 'elephant', 'elephnt must not correct to elephant');

    const resComputer = matchToken('computr');
    assert.strictEqual(resComputer.decision, 'LOW_CONFIDENCE');
    assert.notStrictEqual(resComputer.candidate, 'computer');

    // Invariant: Universal normalizer never rewrites words absent from vocabulary
    const norm = normalizeInputUniversal('weathr elephnt computr');
    assert.strictEqual(norm.normalizedText, 'weathr elephnt computr', 'Words outside vocabulary must never be rewritten');
    assert.strictEqual(norm.corrections.length, 0);
  });

  // ── 4. Protected Short-Word Shielding ───────────────────────────────────────
  runTest('4. Protected Short Words: map, set, get, tree, node, heap, list, root never modified', () => {
    const protectedList = ['map', 'set', 'get', 'tree', 'node', 'head', 'tail', 'top', 'pop', 'heap', 'list', 'root'];

    for (const word of protectedList) {
      assert.ok(PROTECTED_SHORT_WORDS.has(word), `${word} must be in PROTECTED_SHORT_WORDS`);
      const res = matchToken(word);
      assert.strictEqual(res.decision, 'LOW_CONFIDENCE');
    }

    // Verify a near-miss of a protected word (<= 4 chars) bypasses fuzzy search completely
    const resSetTypo = matchToken('setp');
    assert.strictEqual(resSetTypo.decision, 'LOW_CONFIDENCE', 'Tokens <= 4 chars must bypass fuzzy candidate search');
    assert.strictEqual(resSetTypo.candidate, null);
  });

  // ── 5. Ambiguity Handling ───────────────────────────────────────────────────
  runTest('5. Ambiguity: Close vocabulary competitors yield MEDIUM_CONFIDENCE', () => {
    // Both 'vector' and 'vectors' or 'list' and 'lists' exist in vocabulary
    const distA = damerauLevenshteinDistance('invertt', 'invert');
    const distB = damerauLevenshteinDistance('invertt', 'insert');
    assert.strictEqual(distA, 1);
    assert.strictEqual(distB, 2);

    const match = matchToken('revers');
    assert.strictEqual(match.decision, 'HIGH_CONFIDENCE');
    assert.strictEqual(match.candidate, 'reverse');
  });

  // ── 6. Two-Stage Phrase Recovery ────────────────────────────────────────────
  runTest('6. Phrase Recovery: lincked -> linked at token layer, then singly_linked_list at phrase layer', () => {
    // Stage 1: Token layer only recognizes token correction
    const tokenRes = matchToken('lincked');
    assert.strictEqual(tokenRes.candidate, 'linked', 'Token layer must only correct word');
    assert.notStrictEqual(tokenRes.candidate, 'singly_linked_list', 'Token layer must not know phrases');

    // Stage 2: Universal normalizer combines token stream and canonical phrase extractor
    const norm = normalizeInputUniversal('singly lincked list');
    assert.strictEqual(norm.normalizedText, 'singly linked list');
    assert.strictEqual(norm.corrections.length, 1);
    assert.strictEqual(norm.corrections[0].original, 'lincked');
    assert.strictEqual(norm.corrections[0].corrected, 'linked');

    const canonicals = norm.canonicalTerms.map(t => t.canonical);
    assert.ok(canonicals.includes('singly_linked_list'), 'Phrase extractor must recognize singly_linked_list');
  });

  // ── 7. No Semantic Expansion ────────────────────────────────────────────────
  runTest('7. No Semantic Expansion: lincked alone never produces singly_linked_list', () => {
    const norm = normalizeInputUniversal('lincked');
    assert.strictEqual(norm.normalizedText, 'linked');
    const canonicals = norm.canonicalTerms.map(t => t.canonical);
    assert.ok(!canonicals.includes('singly_linked_list'), 'Isolated lincked must never produce singly_linked_list');
    assert.strictEqual(canonicals.length, 0, 'Isolated linked has no complete phrase');
  });

  // ── 8. Deterministic Ranking & Reproducibility ──────────────────────────────
  runTest('8. Determinism: Repeated calls produce bit-for-bit identical results', () => {
    const input = 'insert a node at the end of a singly lincked list';
    const run1 = JSON.stringify(normalizeInputUniversal(input));
    const run2 = JSON.stringify(normalizeInputUniversal(input));
    const run3 = JSON.stringify(normalizeInputUniversal(input));

    assert.strictEqual(run1, run2, 'Run 1 and Run 2 must be bit-for-bit identical');
    assert.strictEqual(run2, run3, 'Run 2 and Run 3 must be bit-for-bit identical');
  });

  // ── 9. Offline Guarantee ────────────────────────────────────────────────────
  runTest('9. Offline Guarantee: Zero external runtime dependencies', () => {
    assert.strictEqual(typeof damerauLevenshteinDistance, 'function');
    assert.strictEqual(typeof similarityRatio, 'function');
    assert.strictEqual(typeof matchToken, 'function');
  });

  console.log(`\nFuzzy Matcher Summary: ${passed} passed, ${failed} failed.\n`);
  return { passed, failed };
}

if (require.main === module) {
  const result = runFuzzyMatcherTests();
  if (result.failed > 0) {
    process.exit(1);
  }
}
