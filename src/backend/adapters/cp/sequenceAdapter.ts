/**
 * CHUP / Offcode — Sequence & Array Algorithm Adapter (Phase 5)
 *
 * Adapts existing V2 parameterized templates (buildFromTemplate / composeCode)
 * for sequence-based algorithmic capabilities:
 * - prefix_sum
 * - two_pointers
 * - binary_search
 * - monotonic_stack
 * - sort
 *
 * Invariants:
 * - Operates strictly on structured plan and composition steps.
 * - Reuses existing verified template implementations.
 */

import { CapabilityPlan, CompositionStep } from '../../../models/capabilityModel';
import { BackendExecutionResult } from '../../../models/backendModel';
import { buildFromTemplate } from '../../../solver/solutionTemplates';
import { composeCode } from '../../../generator/codeComposer';
import { StructuredProblem } from '../../../models/problemSpec';

export class SequenceAlgorithmAdapter {
  public execute(
    plan: CapabilityPlan,
    step: CompositionStep,
    problem?: StructuredProblem
  ): BackendExecutionResult {
    let templateName: string = 'prefixSum';

    if (step.capabilityId === 'prefix_sum') {
      templateName = 'prefixSum';
    } else if (step.capabilityId === 'two_pointers') {
      templateName = 'twoPointers';
    } else if (step.capabilityId === 'binary_search') {
      templateName = 'binarySearch';
    } else if (step.capabilityId === 'monotonic_stack') {
      templateName = 'monotonicStack';
    } else if (step.capabilityId === 'sort') {
      templateName = 'sortGreedy';
    }

    const fragment = buildFromTemplate(templateName, {
      intType: 'long long',
      hasQueries: true,
      hasInitialSort: plan.resolvedCapabilities.includes('sort')
    });

    if (!fragment) {
      return {
        status: 'EXECUTION_FAILED',
        backendId: 'cp_algorithm_backend',
        capabilityId: step.capabilityId,
        algorithmId: step.algorithmId,
        implementationMechanism: step.implementationMechanism,
        generatedCode: '',
        diagnostics: [`Template ${templateName} not found in template registry`],
        failure: {
          code: 'GENERATOR_VARIANT_UNSUPPORTED',
          layer: 'IMPLEMENTATION',
          message: `CP sequence template not found for ${templateName}`
        },
        metadata: { templateName }
      };
    }

    const code = composeCode([fragment]);

    return {
      status: 'SUCCESS',
      backendId: 'cp_algorithm_backend',
      capabilityId: step.capabilityId,
      algorithmId: step.algorithmId,
      implementationMechanism: step.implementationMechanism,
      generatedCode: code,
      diagnostics: [`Assembled sequence solution using template '${templateName}'`],
      metadata: {
        templateName,
        componentsUsed: step.requiredComponents,
        mechanism: step.implementationMechanism
      }
    };
  }
}

export const SEQUENCE_ADAPTER = new SequenceAlgorithmAdapter();
