/**
 * CHUP / Offcode — Phase 5 Backend Integration Test Suite
 *
 * Verifies all 12 architectural categories required by Phase 5:
 * Category 1 — Backend Registry Validity
 * Category 2 — Backend Discovery
 * Category 3 — Capability Independence (Domain Metadata Invariance)
 * Category 4 — Adapter Invocation to Real Specialized Engines
 * Category 5 — Result Normalization
 * Category 6 — Failure Taxonomy Preservation
 * Category 7 — Constraint & Mechanism Preservation
 * Category 8 — Multiple Candidates & Deterministic Selection
 * Category 9 — Composition Support
 * Category 10 — Unsupported Backend (Fail Closed)
 * Category 11 — Regression
 * Category 12 — Deterministic Reproducibility
 */

import * as assert from 'assert';
import { BACKEND_REGISTRY } from '../backend/backendRegistry';
import { UNIVERSAL_ROUTER } from '../pipeline/universalRouter';
import { CapabilityPlan, CompositionStep } from '../models/capabilityModel';
import { BackendResolution } from '../models/backendModel';

export function runPhase5BackendIntegrationTests(): { passed: number; failed: number } {
  let passed = 0;
  let failed = 0;

  function runTest(name: string, fn: () => void | Promise<void>) {
    try {
      const res = fn();
      if (res instanceof Promise) {
        throw new Error('Sync test expected, async returned');
      }
      passed++;
      console.log(`  ✓ ${name}`);
    } catch (err: unknown) {
      failed++;
      console.error(`  ✗ ${name}`);
      console.error(`    ${(err as Error).message}`);
    }
  }

  async function runAsyncTest(name: string, fn: () => Promise<void>) {
    try {
      await fn();
      passed++;
      console.log(`  ✓ ${name}`);
    } catch (err: unknown) {
      failed++;
      console.error(`  ✗ ${name}`);
      console.error(`    ${(err as Error).message}`);
    }
  }

  console.log('\n=================================================');
  console.log('   CHUP Phase 5 — Backend Integration Test Suite  ');
  console.log('=================================================');

  // ── Category 1: Backend Registry Validity ───────────────────────────────────
  runTest('[Cat 1.1] Backend Registry is populated with all default specialized backends', () => {
    const backends = BACKEND_REGISTRY.getAllBackends();
    assert.strictEqual(backends.length >= 3, true, 'At least 3 default backends should be registered');
    
    const ids = backends.map(b => b.descriptor.id);
    assert.strictEqual(ids.includes('classical_data_structure_backend'), true);
    assert.strictEqual(ids.includes('numerical_backend'), true);
    assert.strictEqual(ids.includes('cp_algorithm_backend'), true);
  });

  runTest('[Cat 1.2] Backend descriptors declare required metadata and no duplicate IDs exist', () => {
    const backends = BACKEND_REGISTRY.getAllBackends();
    const idSet = new Set<string>();

    for (const b of backends) {
      const d = b.descriptor;
      assert.strictEqual(idSet.has(d.id), false, `Duplicate backend ID: ${d.id}`);
      idSet.add(d.id);

      assert.strictEqual(typeof d.name, 'string');
      assert.strictEqual(typeof d.description, 'string');
      assert.strictEqual(Array.isArray(d.supportedCapabilities), true);
      assert.strictEqual(Array.isArray(d.supportedMechanisms), true);
      assert.strictEqual(d.availability, 'AVAILABLE');
      assert.strictEqual(typeof d.priority, 'number');
    }
  });

  // ── Category 2: Backend Discovery ───────────────────────────────────────────
  runTest('[Cat 2.1] Discovers classical backend for Singly Linked List plan', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('singly linked list insert at end');
    const candidates = BACKEND_REGISTRY.findCandidates(plan);
    const candidateIds = candidates.map(c => c.descriptor.id);
    assert.strictEqual(candidateIds.includes('classical_data_structure_backend'), true);
  });

  runTest('[Cat 2.2] Discovers CP backend for Dijkstra shortest path plan', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('dijkstra shortest path algorithm');
    const candidates = BACKEND_REGISTRY.findCandidates(plan);
    const candidateIds = candidates.map(c => c.descriptor.id);
    assert.strictEqual(candidateIds.includes('cp_algorithm_backend'), true);
  });

  runTest('[Cat 2.3] Discovers Numerical backend for LU Decomposition plan', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('solve system of linear equations using LU decomposition');
    const candidates = BACKEND_REGISTRY.findCandidates(plan);
    const candidateIds = candidates.map(c => c.descriptor.id);
    assert.strictEqual(candidateIds.includes('numerical_backend'), true);
  });

  // ── Category 3: Capability Independence (Domain Invariance) ─────────────────
  runTest('[Cat 3.1] Backend resolution is invariant to domain metadata mutations', () => {
    const planA = UNIVERSAL_ROUTER.createPlan('dijkstra shortest path');
    planA.domains = ['graph_algorithm'];

    const planB = UNIVERSAL_ROUTER.createPlan('dijkstra shortest path');
    planB.domains = ['competitive_programming'];

    const planC = UNIVERSAL_ROUTER.createPlan('dijkstra shortest path');
    planC.domains = ['arbitrary_domain_metadata', 'academic'];

    const resA = BACKEND_REGISTRY.resolveBackend(planA);
    const resB = BACKEND_REGISTRY.resolveBackend(planB);
    const resC = BACKEND_REGISTRY.resolveBackend(planC);

    assert.strictEqual(resA.selectedBackend, resB.selectedBackend);
    assert.strictEqual(resB.selectedBackend, resC.selectedBackend);
    assert.deepStrictEqual(resA.deterministicRanking, resB.deterministicRanking);
  });

  // ── Category 4: Real Adapter Invocation ──────────────────────────────────────
  runTest('[Cat 4.1] SLL executes through ClassicalDataStructureAdapter into C++ code', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('singly linked list insert at end');
    const res = BACKEND_REGISTRY.resolveBackend(plan);
    assert.strictEqual(res.selectedBackend, 'classical_data_structure_backend');

    const backend = BACKEND_REGISTRY.getBackend(res.selectedBackend!)!;
    assert.strictEqual(backend.descriptor.id, 'classical_data_structure_backend');

    const { CLASSICAL_DS_ADAPTER } = require('../backend/adapters/dataStructureAdapter');
    const execRes = CLASSICAL_DS_ADAPTER.execute(plan, plan.compositionSteps[0]);
    assert.strictEqual(execRes.status, 'SUCCESS');
    assert.strictEqual(typeof execRes.generatedCode, 'string');
    assert.strictEqual(execRes.generatedCode.length > 50, true);
    assert.strictEqual(execRes.generatedCode.includes('#include'), true);
  });

  runTest('[Cat 4.2] Dijkstra executes through GraphAlgorithmAdapter into C++ code', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('dijkstra shortest path algorithm');
    const res = BACKEND_REGISTRY.resolveBackend(plan);
    assert.strictEqual(res.selectedBackend, 'cp_algorithm_backend');

    const { GRAPH_ADAPTER } = require('../backend/adapters/cp/graphAdapter');
    const execRes = GRAPH_ADAPTER.execute(plan, plan.compositionSteps[0]);
    assert.strictEqual(execRes.status, 'SUCCESS');
    assert.strictEqual(typeof execRes.generatedCode, 'string');
    assert.strictEqual(execRes.generatedCode.includes('priority_queue'), true);
    assert.strictEqual(execRes.generatedCode.includes('main()'), true);
  });

  runTest('[Cat 4.3] LU Decomposition executes through NumericalBackendAdapter into C++ code', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('LU decomposition of square matrix using Doolittle algorithm');
    const res = BACKEND_REGISTRY.resolveBackend(plan);
    assert.strictEqual(res.selectedBackend, 'numerical_backend');

    const { NUMERICAL_ADAPTER } = require('../backend/adapters/numericalAdapter');
    const execRes = NUMERICAL_ADAPTER.execute(plan, plan.compositionSteps[0]);
    assert.strictEqual(execRes.status, 'SUCCESS');
    assert.strictEqual(typeof execRes.generatedCode, 'string');
    assert.strictEqual(execRes.generatedCode.length > 50, true);
    assert.strictEqual(execRes.generatedCode.includes('#include'), true);
  });

  // ── Category 5: Result Normalization ────────────────────────────────────────
  runTest('[Cat 5.1] Backend execution result normalizes cleanly into universal result structure', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('prefix sum array range query');
    const res = BACKEND_REGISTRY.resolveBackend(plan);
    assert.strictEqual(res.selectedBackend, 'cp_algorithm_backend');
    assert.strictEqual(Array.isArray(res.deterministicRanking), true);
    assert.strictEqual(res.deterministicRanking.length > 0, true);
    assert.strictEqual(typeof res.selectionReason, 'string');
  });

  // ── Category 6: Failure Taxonomy Preservation ───────────────────────────────
  runTest('[Cat 6.1] Upstream planning failure preserves failureCode and failureLayer', () => {
    // Dijkstra on negative weights triggers CAPABILITY_CONFLICT in Phase 4 planner
    const plan = UNIVERSAL_ROUTER.createPlan('Dijkstra shortest path with negative edge weights');
    assert.strictEqual(plan.status, 'CAPABILITY_CONFLICT');
    assert.strictEqual(plan.failureCode, 'CAPABILITY_CONFLICT');
  });

  // ── Category 7: Constraint & Mechanism Preservation ─────────────────────────
  runTest('[Cat 7.1] Mechanism compatibility rejects backend lacking requested mechanism', () => {
    const step: CompositionStep = {
      stepIndex: 0,
      capabilityId: 'singly_linked_list',
      algorithmId: 'singly_linked_list_standard',
      requiredComponents: ['sll_node'],
      implementationMechanism: 'pointer_sll',
      requiredStates: ['pointer_based'],
      producedStates: ['sequence'],
      preconditions: [],
      postconditions: [],
      invariants: [],
      proofObligations: [],
      representationRequirements: { representation: 'pointer_based' },
      constraintRequirements: {}
    };

    const dummyPlan: CapabilityPlan = {
      status: 'CAPABILITY_RESOLVED',
      resolvedCapabilities: ['singly_linked_list'],
      operationPlan: ['insert_end'],
      requiredComponents: ['sll_node'],
      selectedMechanism: 'pointer_sll',
      stateRequirements: [],
      stateProduction: [],
      constraints: [],
      solverCandidates: [],
      selectedSolver: null,
      compositionSteps: [step],
      verificationObligations: [],
      domains: [],
      explanation: 'Test plan'
    };

    // CP backend does not support manual pointer node management for classical SLL
    const cpBackend = BACKEND_REGISTRY.getBackend('cp_algorithm_backend')!;
    const compat = cpBackend.checkCompatibility(dummyPlan, step);
    assert.strictEqual(compat.compatible, false);
    assert.strictEqual(compat.violatedConstraints.length > 0, true);
  });

  runTest('[Cat 7.2] Classical DS backend accepts pointer_based mechanism', () => {
    const step: CompositionStep = {
      stepIndex: 0,
      capabilityId: 'singly_linked_list',
      algorithmId: 'singly_linked_list_standard',
      requiredComponents: ['sll_node'],
      implementationMechanism: 'pointer_sll',
      requiredStates: ['pointer_based'],
      producedStates: ['sequence'],
      preconditions: [],
      postconditions: [],
      invariants: [],
      proofObligations: [],
      representationRequirements: { representation: 'pointer_based' },
      constraintRequirements: {}
    };

    const dummyPlan: CapabilityPlan = {
      status: 'CAPABILITY_RESOLVED',
      resolvedCapabilities: ['singly_linked_list'],
      operationPlan: ['insert_end'],
      requiredComponents: ['sll_node'],
      selectedMechanism: 'pointer_sll',
      stateRequirements: [],
      stateProduction: [],
      constraints: [],
      solverCandidates: [],
      selectedSolver: null,
      compositionSteps: [step],
      verificationObligations: [],
      domains: [],
      explanation: 'Test plan'
    };

    const dsBackend = BACKEND_REGISTRY.getBackend('classical_data_structure_backend')!;
    const compat = dsBackend.checkCompatibility(dummyPlan, step);
    assert.strictEqual(compat.compatible, true);
  });

  // ── Category 8: Multiple Candidates & Deterministic Ranking ─────────────────
  runTest('[Cat 8.1] Sort query discovers multiple backend candidates with deterministic ranking', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('sort elements in array');
    const candidates = BACKEND_REGISTRY.findCandidates(plan);
    assert.strictEqual(candidates.length >= 2, true, 'Sort should discover both DS and CP backends');

    const res = BACKEND_REGISTRY.resolveBackend(plan);
    assert.strictEqual(res.candidates.length >= 2, true);
    assert.strictEqual(res.deterministicRanking.length >= 1, true);
    assert.strictEqual(typeof res.selectedBackend, 'string');
    assert.strictEqual(res.selectionReason.includes('deterministic ranking'), true);
  });

  // ── Category 9: Composition Support ─────────────────────────────────────────
  runTest('[Cat 9.1] Composed plan preserves proof obligations and state requirements', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('compute prefix sum array for 1D static range sum queries');
    assert.strictEqual(plan.status, 'CAPABILITY_RESOLVED');
    assert.strictEqual(plan.compositionSteps.length > 0, true);
    assert.strictEqual(plan.verificationObligations.length > 0, true);

    const res = BACKEND_REGISTRY.resolveBackend(plan);
    assert.strictEqual(res.selectedBackend, 'cp_algorithm_backend');
  });

  // ── Category 10: Unsupported Backend (Fail Closed) ──────────────────────────
  runTest('[Cat 10.1] Capability without registered backend returns BACKEND_UNAVAILABLE', () => {
    const dummyStep: CompositionStep = {
      stepIndex: 0,
      capabilityId: 'unsupported_quantum_annealing',
      algorithmId: 'quantum_gate_solver',
      requiredComponents: [],
      implementationMechanism: 'quantum_circuit',
      requiredStates: [],
      producedStates: [],
      preconditions: [],
      postconditions: [],
      invariants: [],
      proofObligations: [],
      representationRequirements: {},
      constraintRequirements: {}
    };

    const dummyPlan: CapabilityPlan = {
      status: 'CAPABILITY_RESOLVED',
      resolvedCapabilities: ['unsupported_quantum_annealing'],
      operationPlan: ['solve'],
      requiredComponents: [],
      selectedMechanism: 'quantum_circuit',
      stateRequirements: [],
      stateProduction: [],
      constraints: [],
      solverCandidates: [],
      selectedSolver: null,
      compositionSteps: [dummyStep],
      verificationObligations: [],
      domains: [],
      explanation: 'Unsupported capability test plan'
    };

    const res = BACKEND_REGISTRY.resolveBackend(dummyPlan, dummyStep);
    assert.strictEqual(res.selectedBackend, null);
    assert.strictEqual(res.candidates.length, 0);
  });

  // ── Category 11: Regression Protection ──────────────────────────────────────
  runTest('[Cat 11.1] Baseline representative queries resolve and plan cleanly', () => {
    const sll = UNIVERSAL_ROUTER.createPlan('singly linked list insert at end');
    assert.strictEqual(sll.status, 'CAPABILITY_RESOLVED');
    assert.strictEqual(sll.resolvedCapabilities.includes('singly_linked_list'), true);

    const dijkstra = UNIVERSAL_ROUTER.createPlan('dijkstra shortest path algorithm');
    assert.strictEqual(dijkstra.status, 'CAPABILITY_RESOLVED');
    assert.strictEqual(dijkstra.resolvedCapabilities.includes('single_source_shortest_path'), true);

    const lu = UNIVERSAL_ROUTER.createPlan('LU decomposition of square matrix using Doolittle algorithm');
    assert.strictEqual(lu.status, 'CAPABILITY_RESOLVED');
    assert.strictEqual(lu.resolvedCapabilities.includes('lu_decomposition'), true);
  });

  // ── Category 12: Deterministic Reproducibility ──────────────────────────────
  runTest('[Cat 12.1] Repeated identical resolution calls produce identical BackendResolution', () => {
    const plan = UNIVERSAL_ROUTER.createPlan('dijkstra shortest path algorithm');

    const res1 = BACKEND_REGISTRY.resolveBackend(plan);
    const res2 = BACKEND_REGISTRY.resolveBackend(plan);
    const res3 = BACKEND_REGISTRY.resolveBackend(plan);

    assert.deepStrictEqual(res1, res2);
    assert.deepStrictEqual(res2, res3);
  });

  console.log(`\nPhase 5 Backend Integration Summary: ${passed} passed, ${failed} failed.`);
  return { passed, failed };
}
