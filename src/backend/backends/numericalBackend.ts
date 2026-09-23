/**
 * CHUP / Offcode — Numerical Backend (Phase 5)
 *
 * Provides execution infrastructure for numerical linear systems, matrix decompositions,
 * and root-finding methods via the verified V1 generator.
 */

import { Backend, BackendDescriptor, BackendCompatibility, BackendExecutionResult } from '../../models/backendModel';
import { CapabilityPlan, CompositionStep } from '../../models/capabilityModel';
import { StructuredProblem } from '../../models/problemSpec';
import { NUMERICAL_ADAPTER } from '../adapters/numericalAdapter';

export class NumericalBackend implements Backend {
  public readonly descriptor: BackendDescriptor = {
    id: 'numerical_backend',
    name: 'Numerical Methods Backend',
    description: 'Verified mathematical algorithms for linear systems, decompositions, and root finding',
    supportedCapabilities: [
      'lu_decomposition',
      'gauss_elimination',
      'root_finding'
    ],
    supportedAlgorithms: [
      'doolittle_lu',
      'gauss_elimination_pivoting',
      'bisection',
      'newton_raphson',
      'secant'
    ],
    supportedComponents: [
      'forward_substitution',
      'back_substitution',
      'partial_pivoting',
      'bracket_evaluation',
      'derivative_evaluation'
    ],
    supportedMechanisms: [
      'dense_matrix_vector',
      'flat_matrix_vector',
      'bracket_interval',
      'derivative_step',
      'secant_step',
      'matrix_dense',
      'array_based'
    ],
    supportedRepresentations: [
      'matrix_dense',
      'array_based',
      'custom_struct'
    ],
    supportedOperations: [
      'solve',
      'decompose',
      'find_root',
      'evaluate'
    ],
    availability: 'AVAILABLE',
    priority: 100,
    version: '1.0.0'
  };

  public checkCompatibility(plan: CapabilityPlan, step?: CompositionStep): BackendCompatibility {
    const currentStep = step || plan.compositionSteps[0];
    if (!currentStep) {
      return {
        compatible: false,
        unsupportedRequirements: ['No composition steps provided in plan'],
        violatedConstraints: [],
        missingComponents: [],
        missingMechanisms: [],
        explanation: 'Plan contains no composition steps'
      };
    }

    const unsupportedReqs: string[] = [];
    const violatedConstraints: string[] = [];

    // Check capability support
    if (!this.descriptor.supportedCapabilities.includes(currentStep.capabilityId)) {
      unsupportedReqs.push(`Capability '${currentStep.capabilityId}' not supported by numerical backend`);
    }

    // Check algorithm support if explicitly set
    if (currentStep.algorithmId && !this.descriptor.supportedAlgorithms.includes(currentStep.algorithmId)) {
      unsupportedReqs.push(`Algorithm '${currentStep.algorithmId}' not supported by numerical backend`);
    }

    const compatible = unsupportedReqs.length === 0 && violatedConstraints.length === 0;

    return {
      compatible,
      unsupportedRequirements: unsupportedReqs,
      violatedConstraints,
      missingComponents: [],
      missingMechanisms: [],
      explanation: compatible
        ? 'Numerical backend is fully compatible with requested mathematical method'
        : `Incompatibility: ${[...unsupportedReqs, ...violatedConstraints].join('; ')}`
    };
  }

  public async execute(plan: CapabilityPlan, problem?: StructuredProblem): Promise<BackendExecutionResult> {
    const step = plan.compositionSteps[0];
    return NUMERICAL_ADAPTER.execute(plan, step, problem);
  }
}

export const NUMERICAL_BACKEND = new NumericalBackend();
