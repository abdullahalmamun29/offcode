/**
 * CHUP Phase 3: Semantic Extraction Test Suite
 *
 * Verifies Category A through G of Phase 3 specification:
 * - A: Lexical/semantic separation (typos produce lexical corrections, not false entities/operations)
 * - B: Entity extraction (data structures, algorithms, numerical methods, mathematical objects)
 * - C: Operation extraction (insert, delete, search, reverse, etc.)
 * - D: Intent extraction (implement, create, solve, calculate, etc.)
 * - E: Constraint extraction (position, ordering)
 * - F: Full Composition with token provenance
 * - G: No Semantic Invention (missing evidence remains missing)
 */

import * as assert from 'assert';
import { normalizeInputUniversal } from '../pipeline/universalNormalizer';
import { canonicalize } from '../pipeline/canonicalizer';
import {
  extractSemanticInput,
  extractEntities,
  extractOperations,
  extractIntents,
  extractConstraints
} from '../pipeline/semanticExtractor';

export function runSemanticExtractionTests(): { passed: number; failed: number } {
  console.log('\n=================================================');
  console.log('   CHUP Phase 3: Semantic Extraction Suite       ');
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

  // ── Category A: Lexical / Semantic Separation ──────────────────────────────
  runTest('A. Lexical/Semantic Separation: "lincked" produces lexical correction only', () => {
    const raw = 'lincked';
    const norm = normalizeInputUniversal(raw);
    const semantic = extractSemanticInput(norm);

    assert.strictEqual(semantic.normalizedText, 'linked', 'Lexical layer corrects lincked -> linked');
    assert.strictEqual(semantic.corrections.length, 1, 'Records 1 spelling correction');
    assert.strictEqual(semantic.entities.length, 0, 'Must NOT produce entities from "lincked" alone');
    assert.strictEqual(semantic.operations.length, 0, 'Must NOT produce operations from "lincked" alone');
    assert.strictEqual(semantic.intents.length, 0, 'Must NOT produce intents from "lincked" alone');
  });

  // ── Category B: Entity Extraction ──────────────────────────────────────────
  runTest('B. Entity Extraction: "singly linked list" extracts singly_linked_list', () => {
    const norm = normalizeInputUniversal('singly linked list');
    const semantic = extractSemanticInput(norm);

    assert.strictEqual(semantic.entities.length, 1);
    const ent = semantic.entities[0];
    assert.strictEqual(ent.kind, 'data_structure');
    assert.strictEqual(ent.value, 'singly_linked_list');
    assert.strictEqual(ent.startToken, 0);
    assert.strictEqual(ent.endToken, 3);
    assert.deepStrictEqual(ent.sourceTokens, [0, 1, 2]);
  });

  runTest('B2. Entity Extraction: numerical and math objects', () => {
    const norm = normalizeInputUniversal('compute eigenvalue of a matrix using lu decomposition');
    const semantic = extractSemanticInput(norm);

    const values = semantic.entities.map(e => e.value);
    assert.ok(values.includes('eigenvalue'), 'Detects eigenvalue as entity');
    assert.ok(values.includes('matrix'), 'Detects matrix as entity');
    assert.ok(values.includes('lu_decomposition'), 'Detects lu_decomposition as entity');
  });

  // ── Category C: Operation Extraction ───────────────────────────────────────
  runTest('C. Operation Extraction: "insert", "delete", "search"', () => {
    const norm = normalizeInputUniversal('insert delete search reverse');
    const semantic = extractSemanticInput(norm);

    const ops = semantic.operations.map(o => o.operation);
    assert.deepStrictEqual(ops, ['insert', 'delete', 'search', 'reverse']);
  });

  // ── Category D: Intent Extraction ──────────────────────────────────────────
  runTest('D. Intent Extraction: "implement a solution"', () => {
    const norm = normalizeInputUniversal('implement a solution');
    const semantic = extractSemanticInput(norm);

    const intents = semantic.intents.map(i => i.intent);
    assert.ok(intents.includes('implement'));
  });

  // ── Category E: Constraint Extraction ──────────────────────────────────────
  runTest('E. Constraint Extraction: "at the end", "in ascending sorted order"', () => {
    const norm = normalizeInputUniversal('insert at the end in ascending sorted order');
    const semantic = extractSemanticInput(norm);

    const positions = semantic.constraints.filter(c => c.type === 'position').map(c => c.value);
    const orderings = semantic.constraints.filter(c => c.type === 'ordering').map(c => c.value);

    assert.ok(positions.includes('end'), 'Extracts position=end');
    assert.ok(orderings.includes('ascending') || orderings.includes('sorted'), 'Extracts ordering constraint');
  });

  // ── Category F: Composition with Provenance ────────────────────────────────
  runTest('F. Composition: "insert a node at the end of a singly lincked list"', () => {
    const norm = normalizeInputUniversal('insert a node at the end of a singly lincked list');
    const semantic = extractSemanticInput(norm);

    // Entity checks
    const entityValues = semantic.entities.map(e => e.value);
    assert.ok(entityValues.includes('node'), 'Contains node entity');
    assert.ok(entityValues.includes('singly_linked_list'), 'Contains singly_linked_list entity');

    // Operation check
    const ops = semantic.operations.map(o => o.operation);
    assert.ok(ops.includes('insert'), 'Contains insert operation');

    // Constraint check
    const pos = semantic.constraints.filter(c => c.type === 'position').map(c => c.value);
    assert.ok(pos.includes('end'), 'Contains position=end constraint');

    // Provenance verification
    const sll = semantic.entities.find(e => e.value === 'singly_linked_list')!;
    assert.ok(sll.startToken < sll.endToken);
    assert.strictEqual(semantic.tokens[sll.startToken].text, 'singly');
    assert.strictEqual(semantic.tokens[sll.endToken - 1].text, 'list');
  });

  // ── Category G: No Semantic Invention Invariant ───────────────────────────
  runTest('G1. No Semantic Invention: "insert" alone never invents entity or position', () => {
    const norm = normalizeInputUniversal('insert');
    const semantic = extractSemanticInput(norm);

    assert.strictEqual(semantic.operations.length, 1);
    assert.strictEqual(semantic.operations[0].operation, 'insert');
    assert.strictEqual(semantic.entities.length, 0, 'Must NOT invent any data structure');
    assert.strictEqual(semantic.constraints.length, 0, 'Must NOT invent position=end or head');
  });

  runTest('G2. No Semantic Invention: "singly linked list" alone never invents operation', () => {
    const norm = normalizeInputUniversal('singly linked list');
    const semantic = extractSemanticInput(norm);

    assert.strictEqual(semantic.entities.length, 1);
    assert.strictEqual(semantic.entities[0].value, 'singly_linked_list');
    assert.strictEqual(semantic.operations.length, 0, 'Must NOT invent insert, delete, or display');
    assert.strictEqual(semantic.constraints.length, 0, 'Must NOT invent position');
  });

  runTest('G3. No Semantic Invention: "insert a node into a linked list" never invents position', () => {
    const norm = normalizeInputUniversal('insert a node into a linked list');
    const semantic = extractSemanticInput(norm);

    const positions = semantic.constraints.filter(c => c.type === 'position');
    assert.strictEqual(positions.length, 0, 'Missing position evidence remains missing');
  });

  console.log(`\nSemantic Extraction Summary: ${passed} passed, ${failed} failed.\n`);
  return { passed, failed };
}

if (require.main === module) {
  const res = runSemanticExtractionTests();
  if (res.failed > 0) {
    process.exit(1);
  }
}
