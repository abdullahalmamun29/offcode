/**
 * CHUP / Offcode — Capability Routing Unit Test Suite (Phase 4)
 *
 * Verifies all 12 Phase 4 architectural categories:
 *  1. Capability Registry Validation
 *  2. Lexical Normalization Separation
 *  3. Three Representative Capabilities (SLL, Dijkstra, LU)
 *  4. Algorithm Dominance
 *  5. Component Decomposition
 *  6. Mechanical Domain Independence
 *  7. Operation & Attribute Extraction
 *  8. Composition with Invariants & Proof Obligations
 *  9. Ambiguity Handling
 * 10. Conflict Handling
 * 11. Unsupported Fail-Closed
 * 12. Determinism
 */

import * as assert from 'assert';
import { CAPABILITY_REGISTRY } from '../pipeline/capabilityCatalog';
import { UNIVERSAL_ROUTER } from '../pipeline/universalRouter';
import { CAPABILITY_SOLVER_REGISTRY } from '../solver/capabilitySolverRegistry';
import { normalizeInput } from '../pipeline/inputNormalizer';
import { parseProblem } from '../pipeline/problemParser';

export function runCapabilityRoutingTests(): { passed: number; failed: number } {
  console.log('\n=================================================');
  console.log('   CHUP Phase 4: Capability Routing Test Suite  ');
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

  // ── Category 1: Registry Validation ──────────────────────────────────────
  runTest('1.1 Registry contains at least 20 capabilities with full specifications', () => {
    const allCaps = CAPABILITY_REGISTRY.getAllCapabilities();
    assert.ok(allCaps.length >= 20, `Expected >= 20 capabilities, got ${allCaps.length}`);
    for (const cap of allCaps) {
      assert.ok(cap.id, 'Capability must have id');
      assert.ok(cap.canonicalName, `Capability ${cap.id} must have canonicalName`);
      assert.ok(cap.domains.length > 0, `Capability ${cap.id} must have domains`);
      assert.ok(cap.algorithms.length > 0, `Capability ${cap.id} must have algorithms`);
    }
  });

  runTest('1.2 Registry components, mechanisms, and algorithms pass cross-validation', () => {
    const validation = CAPABILITY_REGISTRY.validate();
    assert.strictEqual(validation.valid, true, `Registry validation failed: ${validation.errors.join(', ')}`);
  });

  runTest('1.3 Capability hierarchy root categories exist', () => {
    const roots = ['data_structures', 'algorithms', 'numerical_methods', 'competitive_programming'];
    for (const rootId of roots) {
      const node = CAPABILITY_REGISTRY.getHierarchyNode(rootId);
      assert.ok(node, `Hierarchy root node ${rootId} must be registered`);
      assert.strictEqual(node.id, rootId);
    }
  });

  // ── Category 2: Lexical Normalization Separation ──────────────────────────
  runTest('2.1 Misspelled queries resolve to correct capabilities via lexical pipeline', () => {
    const q1 = 'lincked list insert at end';
    const req1 = UNIVERSAL_ROUTER.resolveRequest(q1);
    assert.strictEqual(req1.status, 'CAPABILITY_RESOLVED');
    assert.strictEqual(req1.capabilities[0], 'singly_linked_list');

    const q2 = 'shortest path using dijktra algorithm';
    const req2 = UNIVERSAL_ROUTER.resolveRequest(q2);
    assert.strictEqual(req2.status, 'CAPABILITY_RESOLVED');
    assert.strictEqual(req2.capabilities[0], 'single_source_shortest_path');
    assert.strictEqual(req2.primaryAlgorithmId, 'dijkstra');

    const q3 = 'solve with lu dcomposition';
    const req3 = UNIVERSAL_ROUTER.resolveRequest(q3);
    assert.strictEqual(req3.status, 'CAPABILITY_RESOLVED');
    assert.strictEqual(req3.capabilities[0], 'lu_decomposition');
  });

  // ── Category 3: Three Representative Capabilities ─────────────────────────
  runTest('3.1 Representative 1: Singly Linked List insertion', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('Insert a node at the end of a singly linked list');
    assert.strictEqual(plan.status, 'CAPABILITY_RESOLVED');
    assert.strictEqual(plan.resolvedCapabilities[0], 'singly_linked_list');
    assert.strictEqual(plan.primaryAlgorithm, 'singly_linked_list_standard');
    assert.strictEqual(plan.selectedMechanism, 'pointer_based_sll');
    assert.ok(plan.requiredComponents.includes('linked_node_chain'));
    assert.ok(plan.operationPlan.includes('insert'));
    assert.ok(plan.compositionSteps.length > 0);
  });

  runTest('3.2 Representative 2: Dijkstra Shortest Path', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('Find shortest path using Dijkstra algorithm');
    assert.strictEqual(plan.status, 'CAPABILITY_RESOLVED');
    assert.strictEqual(plan.resolvedCapabilities[0], 'single_source_shortest_path');
    assert.strictEqual(plan.primaryAlgorithm, 'dijkstra');
    assert.strictEqual(plan.selectedMechanism, 'binary_heap_std');
    assert.ok(plan.requiredComponents.includes('priority_queue'));
    assert.ok(plan.requiredComponents.includes('edge_relaxation'));
  });

  runTest('3.3 Representative 3: LU Decomposition', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('Solve system of equations using LU decomposition');
    assert.strictEqual(plan.status, 'CAPABILITY_RESOLVED');
    assert.strictEqual(plan.resolvedCapabilities[0], 'lu_decomposition');
    assert.strictEqual(plan.primaryAlgorithm, 'doolittle_lu');
    assert.strictEqual(plan.selectedMechanism, 'dense_matrix_vector');
    assert.ok(plan.requiredComponents.includes('forward_substitution'));
    assert.ok(plan.requiredComponents.includes('back_substitution'));
  });

  // ── Category 4: Algorithm Dominance ───────────────────────────────────────
  runTest('4.1 Specific algorithm dominates generic capability request', () => {
    const req = UNIVERSAL_ROUTER.resolveRequest('Find shortest path using Dijkstra');
    assert.strictEqual(req.capabilities[0], 'single_source_shortest_path');
    assert.strictEqual(req.primaryAlgorithmId, 'dijkstra');
    assert.notStrictEqual(req.primaryAlgorithmId, 'sssp_generic');
  });

  runTest('4.2 Root finding with bisection dominates to bisection', () => {
    const req = UNIVERSAL_ROUTER.resolveRequest('Find root of function using bisection method');
    assert.strictEqual(req.capabilities[0], 'root_finding');
    assert.strictEqual(req.primaryAlgorithmId, 'bisection');
  });

  // ── Category 5: Component Decomposition ───────────────────────────────────
  runTest('5.1 Dijkstra decomposes into required priority_queue and edge_relaxation', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('Dijkstra algorithm');
    assert.ok(plan.requiredComponents.includes('priority_queue'), 'Must require priority_queue component');
    assert.ok(plan.requiredComponents.includes('edge_relaxation'), 'Must require edge_relaxation component');
  });

  runTest('5.2 LU decomposition decomposes into forward and back substitution', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('LU decomposition');
    assert.ok(plan.requiredComponents.includes('forward_substitution'), 'Must require forward_substitution');
    assert.ok(plan.requiredComponents.includes('back_substitution'), 'Must require back_substitution');
  });

  // ── Category 6: Mechanical Domain Independence ────────────────────────────
  runTest('6.1 Plan is invariant under mutated problem domain metadata', () => {
    const query = 'Find shortest path using Dijkstra algorithm';
    const basePlan = UNIVERSAL_ROUTER.createPlan(query);

    const norm = normalizeInput(query);
    const parsedProblem = parseProblem(norm, query);

    const problemAcademic = { ...parsedProblem, domain: 'academic' };
    const problemCp = { ...parsedProblem, domain: 'competitive_programming' };
    const problemUnknown = { ...parsedProblem, domain: 'arbitrary_domain_xyz' };

    const planAcademic = UNIVERSAL_ROUTER.createPlan(query, problemAcademic);
    const planCp = UNIVERSAL_ROUTER.createPlan(query, problemCp);
    const planUnknown = UNIVERSAL_ROUTER.createPlan(query, problemUnknown);

    assert.strictEqual(planAcademic.primaryAlgorithm, basePlan.primaryAlgorithm, 'Domain=academic must not alter algorithm');
    assert.strictEqual(planCp.primaryAlgorithm, basePlan.primaryAlgorithm, 'Domain=cp must not alter algorithm');
    assert.strictEqual(planUnknown.primaryAlgorithm, basePlan.primaryAlgorithm, 'Domain=unknown must not alter algorithm');

    assert.deepStrictEqual(planAcademic.requiredComponents, basePlan.requiredComponents, 'Components must match');
    assert.deepStrictEqual(planCp.requiredComponents, basePlan.requiredComponents, 'Components must match');
    assert.deepStrictEqual(planUnknown.requiredComponents, basePlan.requiredComponents, 'Components must match');
  });

  // ── Category 7: Operation & Attribute Extraction ──────────────────────────
  runTest('7.1 Position attribute extraction: insert at end of singly linked list', () => {
    const req = UNIVERSAL_ROUTER.resolveRequest('insert a node at the end of singly linked list');
    assert.strictEqual(req.attributes.position, 'end');
    assert.ok(req.operations.includes('insert'));
  });

  runTest('7.2 Position attribute extraction: insert at front of singly linked list', () => {
    const req = UNIVERSAL_ROUTER.resolveRequest('insert a node at front of singly linked list');
    assert.strictEqual(req.attributes.position, 'beginning');
    assert.ok(req.operations.includes('insert'));
  });

  runTest('7.3 Negative edge weight attribute extraction', () => {
    const req = UNIVERSAL_ROUTER.resolveRequest('shortest path with negative edge weights');
    assert.strictEqual(req.attributes.negativeWeights, true);
    assert.strictEqual(req.attributes.weight, 'negative');
  });

  // ── Category 8: Composition with Invariants & Proof Obligations ───────────
  runTest('8.1 Composition step populates invariants and proof obligations for SLL', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('insert at end of singly linked list');
    assert.ok(plan.compositionSteps.length > 0);
    const step = plan.compositionSteps[0];
    assert.ok(step.invariants.length > 0, 'Must have invariants');
    assert.ok(step.proofObligations.length > 0, 'Must have proof obligations');
    const hasSllObligation = step.proofObligations.some(o =>
      o.obligationId.includes('tail_points_to_null') || o.obligationId.includes('nodes_singly_linked')
    );
    assert.ok(hasSllObligation, 'Must verify SLL invariants');
  });

  runTest('8.2 Composition step populates invariants and proof obligations for Dijkstra', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('Dijkstra algorithm');
    assert.ok(plan.compositionSteps.length > 0);
    const step = plan.compositionSteps[0];
    const hasDijkstraObligation = step.proofObligations.some(o =>
      o.obligationId.includes('triangle_inequality') || o.obligationId.includes('non_negative')
    );
    assert.ok(hasDijkstraObligation, 'Must verify Dijkstra invariants');
  });

  // ── Category 9: Ambiguity Handling ────────────────────────────────────────
  runTest('9.1 Generic ambiguous shortest path reports CAPABILITY_AMBIGUOUS', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('shortest path');
    assert.strictEqual(plan.status, 'CAPABILITY_AMBIGUOUS');
    assert.strictEqual(plan.failureCode, 'CAPABILITY_AMBIGUOUS');
    assert.strictEqual(plan.failureLayer, 'CAPABILITY_RESOLUTION');
    assert.ok(plan.solverCandidates.length > 1, `Must list candidates, got ${plan.solverCandidates.length}`);
  });

  // ── Category 10: Conflict Handling ────────────────────────────────────────
  runTest('10.1 Dijkstra with negative weights reports CAPABILITY_CONFLICT', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('Dijkstra shortest path with negative edge weights');
    assert.strictEqual(plan.status, 'CAPABILITY_CONFLICT');
    assert.strictEqual(plan.failureCode, 'CAPABILITY_CONFLICT');
    assert.strictEqual(plan.failureLayer, 'CAPABILITY_RESOLUTION');
    assert.ok(plan.failureMessage && plan.failureMessage.includes('negative'));
  });

  // ── Category 11: Unsupported Fail-Closed ───────────────────────────────────
  runTest('11.1 Quantum Fourier Transform fails closed with zero hallucinated code', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('implement quantum fourier transform');
    assert.strictEqual(plan.status, 'CAPABILITY_UNSUPPORTED');
    assert.strictEqual(plan.failureCode, 'CAPABILITY_UNSUPPORTED');
    assert.strictEqual(plan.failureLayer, 'CAPABILITY_RESOLUTION');
    assert.strictEqual(plan.selectedSolver, null);
  });

  runTest('11.2 Simulated Annealing TSP fails closed without false generation', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('traveling salesman problem with simulated annealing');
    assert.strictEqual(plan.status, 'CAPABILITY_UNSUPPORTED');
  });

  // ── Category 12: Determinism ───────────────────────────────────────
  runTest('12.1 Repeated plan generation produces bit-for-bit identical plans', () => {
    const query = 'Insert a node at the end of a singly linked list';
    const p1 = UNIVERSAL_ROUTER.createPlan(query);
    for (let i = 0; i < 5; i++) {
      const pi = UNIVERSAL_ROUTER.createPlan(query);
      assert.deepStrictEqual(pi.resolvedCapabilities, p1.resolvedCapabilities);
      assert.strictEqual(pi.primaryAlgorithm, p1.primaryAlgorithm);
      assert.deepStrictEqual(pi.requiredComponents, p1.requiredComponents);
      assert.strictEqual(pi.selectedMechanism, p1.selectedMechanism);
      assert.deepStrictEqual(pi.operationPlan, p1.operationPlan);
    }
  });

  console.log(`\nPhase 4 Capability Routing Summary: ${passed} passed, ${failed} failed.`);
  return { passed, failed };
}

// Standalone execution support
if (require.main === module) {
  const result = runCapabilityRoutingTests();
  if (result.failed > 0) {
    process.exit(1);
  }
}
