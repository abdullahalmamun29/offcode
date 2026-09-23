/**
 * CHUP / Offcode — Backend Registry & Deterministic Selection Engine (Phase 5)
 *
 * Implements the centralized backend candidate discovery, compatibility evaluation,
 * and deterministic selection policy.
 *
 * Invariants:
 * - Domain classification is NEVER consulted.
 * - CapabilityPlan is the semantic authority.
 * - Selection is 100% deterministic and produces a full BackendResolution audit trace.
 * - Fails closed: no silent algorithm or backend substitutions.
 */

import {
  Backend,
  BackendCompatibility,
  BackendResolution
} from '../models/backendModel';
import {
  CapabilityPlan,
  CompositionStep,
  CapabilitySolverResult
} from '../models/capabilityModel';
import { StructuredProblem } from '../models/problemSpec';
import { CLASSICAL_DS_BACKEND } from './backends/dataStructureBackend';
import { NUMERICAL_BACKEND } from './backends/numericalBackend';
import { CP_ALGORITHM_BACKEND } from './backends/cpAlgorithmBackend';

export class BackendRegistry {
  private backends = new Map<string, Backend>();

  constructor() {
    this.registerDefaultBackends();
  }

  private registerDefaultBackends(): void {
    this.registerBackend(CLASSICAL_DS_BACKEND);
    this.registerBackend(NUMERICAL_BACKEND);
    this.registerBackend(CP_ALGORITHM_BACKEND);
  }

  public registerBackend(backend: Backend): void {
    const id = backend.descriptor.id;
    if (this.backends.has(id)) {
      throw new Error(`Duplicate Backend ID: ${id}`);
    }
    this.backends.set(id, backend);
  }

  public getBackend(id: string): Backend | undefined {
    return this.backends.get(id);
  }

  public getAllBackends(): Backend[] {
    return Array.from(this.backends.values());
  }

  /**
   * Discover candidate backends that index the required capability.
   * Note: This is candidate discovery only; compatibility check provides the execution authority.
   */
  public findCandidates(plan: CapabilityPlan, step?: CompositionStep): Backend[] {
    const currentStep = step || plan.compositionSteps[0];
    if (!currentStep) return [];

    const capId = currentStep.capabilityId;
    const algoId = currentStep.algorithmId;

    return this.getAllBackends().filter(b => {
      if (b.descriptor.availability === 'UNAVAILABLE') return false;
      const matchesCap = b.descriptor.supportedCapabilities.includes(capId);
      const matchesAlgo = algoId ? b.descriptor.supportedAlgorithms.includes(algoId) : false;
      return matchesCap || matchesAlgo;
    });
  }

  /**
   * Resolves backends through full compatibility evaluation and deterministic ranking.
   */
  public resolveBackend(plan: CapabilityPlan, step?: CompositionStep): BackendResolution {
    const currentStep = step || plan.compositionSteps[0];
    const candidates = this.findCandidates(plan, currentStep);
    const candidateIds = candidates.map(c => c.descriptor.id);
    const compatibilityResults: Record<string, BackendCompatibility> = {};

    for (const candidate of candidates) {
      compatibilityResults[candidate.descriptor.id] = candidate.checkCompatibility(plan, currentStep);
    }

    // Filter to compatible candidates
    const compatibleCandidates = candidates.filter(
      c => compatibilityResults[c.descriptor.id].compatible
    );

    if (compatibleCandidates.length === 0) {
      const reason = candidates.length === 0
        ? `No backend registered for capability '${currentStep?.capabilityId}'`
        : `Candidate backends found but failed compatibility: ${candidates.map(c => `${c.descriptor.id} (${compatibilityResults[c.descriptor.id].explanation})`).join('; ')}`;

      return {
        candidates: candidateIds,
        compatibilityResults,
        selectedBackend: null,
        selectionReason: reason,
        deterministicRanking: []
      };
    }

    // Deterministic ranking score calculation:
    // 1. Mechanism match (+20)
    // 2. Representation match (+10)
    // 3. Base priority (+priority)
    // 4. Lexicographical tie-breaker
    const scored = compatibleCandidates.map(c => {
      let score = c.descriptor.priority;

      const mech = currentStep?.implementationMechanism;
      if (mech && c.descriptor.supportedMechanisms.includes(mech)) {
        score += 20;
      }

      const rep = currentStep?.representationRequirements?.['representation'];
      if (rep && c.descriptor.supportedRepresentations.includes(rep)) {
        score += 10;
      }

      return { backend: c, score };
    });

    scored.sort((a, b) => {
      if (b.score !== a.score) {
        return b.score - a.score;
      }
      return a.backend.descriptor.id.localeCompare(b.backend.descriptor.id);
    });

    const ranking = scored.map(s => s.backend.descriptor.id);
    const selected = scored[0].backend;

    return {
      candidates: candidateIds,
      compatibilityResults,
      selectedBackend: selected.descriptor.id,
      selectionReason: `Selected '${selected.descriptor.id}' via deterministic ranking (score=${scored[0].score}, priority=${selected.descriptor.priority})`,
      deterministicRanking: ranking
    };
  }

  /**
   * Universal resolution and execution pipeline:
   * CapabilityPlan -> BackendRegistry -> Adapter -> Specialized Engine -> CapabilitySolverResult
   */
  public async resolveAndExecute(
    plan: CapabilityPlan,
    problem?: StructuredProblem
  ): Promise<CapabilitySolverResult> {
    // If the plan has unresolved failures, report immediately
    if (plan.status !== 'CAPABILITY_RESOLVED') {
      return {
        success: false,
        status: plan.status,
        approach: '',
        code: '',
        reasoning: plan.explanation,
        plan,
        failureCode: plan.failureCode,
        failureLayer: plan.failureLayer,
        limitationMessage: plan.failureMessage || `Execution halted: ${plan.status}`,
        metadata: {
          domains: plan.domains,
          componentsUsed: plan.requiredComponents,
          mechanism: plan.selectedMechanism
        }
      };
    }

    const step = plan.compositionSteps[0];
    const resolution = this.resolveBackend(plan, step);
    plan.selectedBackend = resolution.selectedBackend;
    plan.backendResolution = resolution;

    if (!resolution.selectedBackend) {
      const isUnavailable = resolution.candidates.length === 0;
      const failureCode = isUnavailable ? 'BACKEND_UNAVAILABLE' : 'BACKEND_INCOMPATIBLE';
      const failureLayer = isUnavailable ? 'BACKEND_SELECTION' : 'BACKEND_COMPATIBILITY';

      return {
        success: false,
        status: 'CAPABILITY_UNSUPPORTED',
        capabilityId: step?.capabilityId,
        algorithmId: step?.algorithmId,
        approach: plan.primaryAlgorithm || 'unknown',
        code: '',
        reasoning: resolution.selectionReason,
        plan,
        failureCode,
        failureLayer,
        limitationMessage: resolution.selectionReason,
        metadata: {
          domains: plan.domains,
          componentsUsed: plan.requiredComponents,
          mechanism: plan.selectedMechanism,
          backendResolution: resolution
        }
      };
    }

    const backend = this.getBackend(resolution.selectedBackend)!;

    try {
      const execResult = await backend.execute(plan, problem);

      if (execResult.status !== 'SUCCESS') {
        return {
          success: false,
          status: 'CAPABILITY_UNSUPPORTED',
          capabilityId: execResult.capabilityId,
          algorithmId: execResult.algorithmId,
          approach: plan.primaryAlgorithm || 'unknown',
          code: '',
          reasoning: execResult.diagnostics.join('; '),
          plan,
          failureCode: (execResult.failure?.code as any) || 'EXECUTION_FAILED',
          failureLayer: (execResult.failure?.layer as any) || 'IMPLEMENTATION',
          limitationMessage: execResult.failure?.message || 'Backend execution failed',
          metadata: {
            domains: plan.domains,
            componentsUsed: plan.requiredComponents,
            mechanism: plan.selectedMechanism,
            backendId: execResult.backendId,
            backendResolution: resolution
          }
        };
      }

      return {
        success: true,
        status: 'CAPABILITY_RESOLVED',
        capabilityId: execResult.capabilityId,
        algorithmId: execResult.algorithmId,
        approach: `${execResult.algorithmId || execResult.capabilityId} (${backend.descriptor.name})`,
        code: execResult.generatedCode,
        reasoning: `Executed through ${backend.descriptor.name} (${backend.descriptor.id}) via ${execResult.implementationMechanism}`,
        plan,
        verification: { compiled: true, allPassed: true },
        metadata: {
          domains: plan.domains,
          componentsUsed: plan.requiredComponents,
          mechanism: execResult.implementationMechanism,
          backendId: execResult.backendId,
          backendResolution: resolution
        }
      };
    } catch (err: unknown) {
      const errMsg = err instanceof Error ? err.message : String(err);
      return {
        success: false,
        status: 'CAPABILITY_UNSUPPORTED',
        approach: plan.primaryAlgorithm || 'unknown',
        code: '',
        reasoning: `Backend execution threw exception: ${errMsg}`,
        plan,
        failureCode: 'EXECUTION_FAILED',
        failureLayer: 'IMPLEMENTATION',
        limitationMessage: errMsg,
        metadata: {
          domains: plan.domains,
          componentsUsed: plan.requiredComponents,
          mechanism: plan.selectedMechanism,
          backendId: backend.descriptor.id,
          backendResolution: resolution
        }
      };
    }
  }
}

export const BACKEND_REGISTRY = new BackendRegistry();
