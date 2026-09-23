/**
 * CHUP / Offcode — String Algorithm Adapter (Phase 5)
 *
 * Adapts existing verified Trie template and string capabilities:
 * - trie (insert, search, prefix)
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

export class StringAlgorithmAdapter {
  public execute(
    plan: CapabilityPlan,
    step: CompositionStep,
    problem?: StructuredProblem
  ): BackendExecutionResult {
    const fragment = buildFromTemplate('trie', {
      intType: 'int',
      hasQueries: true
    });

    if (!fragment) {
      return {
        status: 'EXECUTION_FAILED',
        backendId: 'cp_algorithm_backend',
        capabilityId: step.capabilityId,
        algorithmId: step.algorithmId,
        implementationMechanism: step.implementationMechanism,
        generatedCode: '',
        diagnostics: ['Trie template not found'],
        failure: {
          code: 'GENERATOR_VARIANT_UNSUPPORTED',
          layer: 'IMPLEMENTATION',
          message: 'String template not found for trie'
        },
        metadata: { capabilityId: step.capabilityId }
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
      diagnostics: [`Assembled string solution for Trie`],
      metadata: {
        componentsUsed: step.requiredComponents,
        mechanism: step.implementationMechanism
      }
    };
  }
}

export const STRING_ADAPTER = new StringAlgorithmAdapter();
