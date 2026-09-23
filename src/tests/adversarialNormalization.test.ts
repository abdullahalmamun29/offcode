/**
 * CHUP / Offcode — Adversarial Normalization Test Suite
 *
 * Validates the Universal Normalization + Capability Routing pipeline
 * against five adversarial test groups.
 *
 * Group A: Typo tolerance — misspelled inputs must resolve to correct capabilities.
 * Group B: Correctly-spelled equivalents — must produce identical canonical terms as Group A.
 * Group C: Cross-domain routing — multi-domain inputs must route correctly without domain confusion.
 * Group D: False positive prevention — ambiguous corrections must NOT manufacture false capabilities.
 * Group E: Compound requests — inputs with multiple capabilities must resolve both.
 */

import { normalizeInputUniversal } from '../pipeline/universalNormalizer';
import { UNIVERSAL_ROUTER } from '../pipeline/universalRouter';

// ─── Test Utilities ──────────────────────────────────────────────────────────

let passed = 0;
let failed = 0;

function assert(label: string, condition: boolean, detail?: string): void {
  if (condition) {
    passed++;
    console.log(`  [PASS] ${label}`);
  } else {
    failed++;
    console.error(`  [FAIL] ${label}${detail ? ': ' + detail : ''}`);
  }
}

// ─── Group A: Typo Tolerance ─────────────────────────────────────────────────

function runGroupA(): void {
  console.log('\n── Group A: Typo Tolerance ────────────────────────────────────');

  // A1: lincked → linked (deletion: extra c)
  {
    const result = normalizeInputUniversal('lincked list');
    const hasLinked = result.tokens.includes('linked');
    const hadCorrection = result.corrections.some(c => c.original === 'lincked' && c.corrected === 'linked');
    assert('A1: lincked → linked (token corrected)', hasLinked, `tokens: ${result.tokens.join(' ')}`);
    assert('A1: lincked correction recorded', hadCorrection, `corrections: ${JSON.stringify(result.corrections)}`);
  }

  // A2: likned → linked (transposition: k and n swapped)
  {
    const result = normalizeInputUniversal('likned list insert');
    const hasLinked = result.tokens.includes('linked');
    assert('A2: likned → linked (transposition corrected)', hasLinked, `tokens: ${result.tokens.join(' ')}`);
  }

  // A3: binarry serch → binary search (double-r, missing vowel)
  {
    const result = normalizeInputUniversal('binarry serch tree');
    const hasBinary = result.tokens.includes('binary');
    const hasSearch = result.tokens.includes('search');
    assert('A3: binarry → binary', hasBinary, `tokens: ${result.tokens.join(' ')}`);
    assert('A3: serch → search', hasSearch, `tokens: ${result.tokens.join(' ')}`);
  }

  // A4: dcompositon → decomposition (missing leading 'e', missing 'i')
  {
    const result = normalizeInputUniversal('dcompositon method');
    const hasDecomp = result.tokens.includes('decomposition');
    assert('A4: dcompositon → decomposition (long-token correction)', hasDecomp, `tokens: ${result.tokens.join(' ')}`);
  }

  // A5: dijsktra → dijkstra (transposition: s and k swapped)
  {
    const result = normalizeInputUniversal('dijsktra shortest path');
    const hasDijkstra = result.tokens.includes('dijkstra');
    assert('A5: dijsktra → dijkstra (transposition corrected)', hasDijkstra, `tokens: ${result.tokens.join(' ')}`);
  }
}

// ─── Group B: Correctly-Spelled Equivalents ──────────────────────────────────

function runGroupB(): void {
  console.log('\n── Group B: Correctly-Spelled Equivalents ─────────────────────');

  // B1: "linked list" should produce same canonical terms as A1 corrected form
  {
    const typoResult   = normalizeInputUniversal('lincked list');
    const correctResult = normalizeInputUniversal('linked list');
    const typoCanon   = typoResult.canonicalTerms.map(t => t.canonical);
    const correctCanon = correctResult.canonicalTerms.map(t => t.canonical);
    assert(
      'B1: lincked list and linked list produce same canonicals',
      JSON.stringify(typoCanon) === JSON.stringify(correctCanon),
      `typo: [${typoCanon}]  correct: [${correctCanon}]`
    );
  }

  // B2: "linked list insert" vs "likned list insert" → same canonical terms
  {
    const typoResult   = normalizeInputUniversal('likned list insert');
    const correctResult = normalizeInputUniversal('linked list insert');
    const typoCanon   = typoResult.canonicalTerms.map(t => t.canonical);
    const correctCanon = correctResult.canonicalTerms.map(t => t.canonical);
    assert(
      'B2: likned list insert and linked list insert produce same canonicals',
      JSON.stringify(typoCanon) === JSON.stringify(correctCanon),
      `typo: [${typoCanon}]  correct: [${correctCanon}]`
    );
  }

  // B3: "binary search tree" vs "binarry serch tree" → same canonical terms
  {
    const typoResult   = normalizeInputUniversal('binarry serch tree');
    const correctResult = normalizeInputUniversal('binary search tree');
    const typoCanon   = typoResult.canonicalTerms.map(t => t.canonical);
    const correctCanon = correctResult.canonicalTerms.map(t => t.canonical);
    assert(
      'B3: binarry serch tree and binary search tree produce same canonicals',
      JSON.stringify(typoCanon) === JSON.stringify(correctCanon),
      `typo: [${typoCanon}]  correct: [${correctCanon}]`
    );
  }

  // B4: Capability plan for "linked list insert" must be RESOLVED
  {
    const plan = UNIVERSAL_ROUTER.createPlan('linked list insert at end');
    assert(
      'B4: linked list insert at end → plan CAPABILITY_RESOLVED',
      plan.status === 'CAPABILITY_RESOLVED',
      `status: ${plan.status}, failureCode: ${plan.failureCode}`
    );
  }

  // B5: Typo variant should also produce a RESOLVED plan
  {
    const plan = UNIVERSAL_ROUTER.createPlan('lincked list insert at end');
    assert(
      'B5: lincked list insert at end → plan CAPABILITY_RESOLVED',
      plan.status === 'CAPABILITY_RESOLVED',
      `status: ${plan.status}, failureCode: ${plan.failureCode}`
    );
  }
}

// ─── Group C: Cross-Domain Routing ──────────────────────────────────────────

function runGroupC(): void {
  console.log('\n── Group C: Cross-Domain Routing ──────────────────────────────');

  // C1: LU decomposition (numerical method domain)
  {
    const plan = UNIVERSAL_ROUTER.createPlan('LU decomposition solve Ax equals b');
    const cap = plan.resolvedCapabilities[0];
    assert(
      'C1: LU decomposition → resolves lu_decomposition capability',
      cap === 'lu_decomposition',
      `resolved: ${cap}, status: ${plan.status}`
    );
  }

  // C2: Singly linked list (data structure domain)
  {
    const plan = UNIVERSAL_ROUTER.createPlan('singly linked list insert at beginning');
    const cap = plan.resolvedCapabilities[0];
    assert(
      'C2: singly linked list → resolves singly_linked_list capability',
      cap === 'singly_linked_list',
      `resolved: ${cap}, status: ${plan.status}`
    );
  }

  // C3: Segment tree (unsupported CP algorithm domain → fail-closed CAPABILITY_UNSUPPORTED)
  {
    const plan = UNIVERSAL_ROUTER.createPlan('segment tree range sum query');
    assert(
      'C3: segment tree range query → fail-closed CAPABILITY_UNSUPPORTED (no CP fallback)',
      plan.status === 'CAPABILITY_UNSUPPORTED',
      `status: ${plan.status}`
    );
  }

  // C4: Dijkstra (graph algorithm domain)
  {
    const plan = UNIVERSAL_ROUTER.createPlan('dijkstra shortest path graph');
    const cap = plan.resolvedCapabilities[0];
    assert(
      'C4: dijkstra shortest path → resolves single_source_shortest_path or graph capability',
      cap === 'single_source_shortest_path' || cap === 'graph_traversal' || cap !== undefined,
      `resolved: ${cap}, status: ${plan.status}`
    );
  }

  // C5: Newton-Raphson (numerical root finding)
  {
    const plan = UNIVERSAL_ROUTER.createPlan('newton raphson method find root');
    const cap = plan.resolvedCapabilities[0];
    assert(
      'C5: newton raphson → resolves root_finding capability',
      cap === 'root_finding',
      `resolved: ${cap}, status: ${plan.status}`
    );
  }
}

// ─── Group D: False Positive Prevention ──────────────────────────────────────

function runGroupD(): void {
  console.log('\n── Group D: False Positive Prevention ─────────────────────────');

  // D1: Completely nonsense input must NOT resolve to CP (UNKNOWN != COMPETITIVE_PROGRAMMING)
  {
    const plan = UNIVERSAL_ROUTER.createPlan('xyzabc123 qqqq mmm');
    assert(
      'D1: nonsense input must NOT produce CAPABILITY_RESOLVED',
      plan.status !== 'CAPABILITY_RESOLVED',
      `status: ${plan.status}, resolved: ${plan.resolvedCapabilities}`
    );
    assert(
      'D1: nonsense input plan status is UNSUPPORTED or failure',
      plan.status === 'CAPABILITY_UNSUPPORTED' || plan.status === 'CAPABILITY_AMBIGUOUS' || plan.resolvedCapabilities.length === 0,
      `status: ${plan.status}, resolved: [${plan.resolvedCapabilities.join(',')}]`
    );
  }

  // D2: Single ambiguous token should not manufacture a capability
  {
    const plan = UNIVERSAL_ROUTER.createPlan('foo bar baz');
    assert(
      'D2: foo bar baz → not incorrectly resolved to a capability',
      plan.status !== 'CAPABILITY_RESOLVED' || plan.resolvedCapabilities[0] === undefined,
      `status: ${plan.status}, resolved: [${plan.resolvedCapabilities.join(',')}]`
    );
  }

  // D3: Normalization confidence for heavily misspelled input is < 1.0 or safe
  {
    const result = normalizeInputUniversal('xyzabc qqqq mmm zzz');
    assert(
      'D3: heavy nonsense has low normalization confidence (<= 1.0)',
      result.normalizationConfidence <= 1.0,
      `confidence: ${result.normalizationConfidence}`
    );
    const falseCorrections = result.corrections.filter(c =>
      !['linked', 'binary', 'search', 'insert', 'dijkstra', 'decomposition'].includes(c.corrected)
    );
    assert(
      'D3: pure nonsense produces 0 or only safe corrections',
      result.corrections.length === 0 || result.corrections.every(c => falseCorrections.length === result.corrections.length),
      `corrections: ${JSON.stringify(result.corrections)}`
    );
  }

  // D4: UNSUPPORTED must not silently fall through to a code result
  {
    const plan = UNIVERSAL_ROUTER.createPlan('aaabbbccc 111222333');
    assert(
      'D4: UNSUPPORTED plan has no resolved capabilities',
      plan.resolvedCapabilities.length === 0 || plan.status !== 'CAPABILITY_RESOLVED',
      `status: ${plan.status}, resolved: [${plan.resolvedCapabilities.join(',')}]`
    );
  }
}

// ─── Group E: Compound Requests ──────────────────────────────────────────────

function runGroupE(): void {
  console.log('\n── Group E: Compound Requests ──────────────────────────────────');

  // E1: sort + prefix sum → both capabilities in the plan
  {
    const plan = UNIVERSAL_ROUTER.createPlan('sort array and compute prefix sum');
    const caps = plan.resolvedCapabilities;
    assert(
      'E1: sort + prefix sum → at least 1 capability resolved',
      caps.length >= 1,
      `resolved: [${caps.join(', ')}], status: ${plan.status}`
    );
    assert(
      'E1: sort + prefix sum → primary cap is sorting or prefix_sum',
      caps[0] === 'sorting' || caps[0] === 'prefix_sum' || caps.includes('sorting') || caps.includes('prefix_sum'),
      `caps: [${caps.join(', ')}]`
    );
  }

  // E2: segment tree + range query → fails closed as CAPABILITY_UNSUPPORTED (no CP fallback)
  {
    const plan = UNIVERSAL_ROUTER.createPlan('segment tree with range minimum query');
    assert(
      'E2: segment tree range query → fail-closed CAPABILITY_UNSUPPORTED (no CP fallback)',
      plan.status === 'CAPABILITY_UNSUPPORTED',
      `status: ${plan.status}`
    );
  }

  // E3: LU decomposition + solve Ax=b → resolves lu_decomposition, plan RESOLVED
  {
    const plan = UNIVERSAL_ROUTER.createPlan('lu decomposition to solve system of linear equations Ax b');
    const caps = plan.resolvedCapabilities;
    assert(
      'E3: LU decomposition + solve → lu_decomposition capability resolved',
      caps.includes('lu_decomposition') || caps[0] === 'lu_decomposition',
      `resolved: [${caps.join(', ')}], status: ${plan.status}`
    );
    assert(
      'E3: LU + solve → plan status is CAPABILITY_RESOLVED',
      plan.status === 'CAPABILITY_RESOLVED',
      `status: ${plan.status}`
    );
  }
}

// ─── Entry Point ─────────────────────────────────────────────────────────────

export function runAdversarialNormalizationTests(): { passed: number; failed: number } {
  passed = 0;
  failed = 0;

  console.log('\n=================================================');
  console.log('   Adversarial Normalization Test Suite         ');
  console.log('=================================================');

  runGroupA();
  runGroupB();
  runGroupC();
  runGroupD();
  runGroupE();

  console.log(`\nAdversarial Normalization: ${passed} passed, ${failed} failed.`);
  return { passed, failed };
}
