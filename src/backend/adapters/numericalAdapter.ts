/**
 * CHUP / Offcode — Numerical Engine Adapter (Phase 5)
 *
 * Adapts the existing verified V1 C++ code generator for numerical methods.
 * Translates structured CapabilityPlan / CompositionStep into V1 numerical ResolutionResult.
 *
 * Invariants:
 * - Zero natural language parsing: operates strictly on structured plan IR.
 * - Preserves existing V1 numerical generator logic.
 * - Returns normalized BackendExecutionResult.
 */

import { CapabilityPlan, CompositionStep } from '../../models/capabilityModel';
import { BackendExecutionResult } from '../../models/backendModel';
import { generateCpp } from '../../generator/cppGenerator';
import { StructuredProblem, ResolutionResult } from '../../models/problemSpec';

export class NumericalBackendAdapter {
  public execute(
    plan: CapabilityPlan,
    step: CompositionStep,
    problem?: StructuredProblem
  ): BackendExecutionResult {
    let moduleId = 'numerical.linear_systems.lu_decomposition.cpp';
    let moduleName = 'LU Decomposition';
    const algoId = step.algorithmId;

    if (step.capabilityId === 'lu_decomposition' || algoId === 'doolittle_lu') {
      moduleId = 'numerical.linear_systems.lu_decomposition.cpp';
      moduleName = 'LU Decomposition (Doolittle)';
    } else if (step.capabilityId === 'gauss_elimination' || algoId === 'gauss_elimination_pivoting') {
      moduleId = 'numerical.linear_systems.gauss_elimination.cpp';
      moduleName = 'Gaussian Elimination';
    } else if (algoId === 'bisection') {
      moduleId = 'numerical.root_finding.bisection.cpp';
      moduleName = 'Bisection Method';
    } else if (algoId === 'newton_raphson') {
      moduleId = 'numerical.root_finding.newton_raphson.cpp';
      moduleName = 'Newton-Raphson Method';
    } else if (algoId === 'secant') {
      moduleId = 'numerical.root_finding.secant.cpp';
      moduleName = 'Secant Method';
    }

    const resolution: any = {
      code: 'SUCCESS',
      moduleId,
      moduleName,
      message: 'Resolved via CapabilityPlan and NumericalBackendAdapter',
      generationMode: 'single',
      spec: {
        domain: 'numerical',
        numerical: { method: algoId }
      }
    };

    const code = generateCpp(resolution);

    if (code.startsWith('// Code generation failed')) {
      return {
        status: 'EXECUTION_FAILED',
        backendId: 'numerical_backend',
        capabilityId: step.capabilityId,
        algorithmId: algoId,
        implementationMechanism: step.implementationMechanism,
        generatedCode: '',
        diagnostics: [`V1 numerical generator failed to emit code for ${algoId}`],
        failure: {
          code: 'GENERATOR_VARIANT_UNSUPPORTED',
          layer: 'IMPLEMENTATION',
          message: `Numerical generator failed for ${algoId}`
        },
        metadata: {
          moduleId,
          algorithmId: algoId
        }
      };
    }

    return {
      status: 'SUCCESS',
      backendId: 'numerical_backend',
      capabilityId: step.capabilityId,
      algorithmId: algoId,
      implementationMechanism: step.implementationMechanism,
      generatedCode: code,
      diagnostics: [`Emitted numerical C++ module ${moduleId} via NumericalBackendAdapter`],
      metadata: {
        moduleId,
        componentsUsed: step.requiredComponents,
        mechanism: step.implementationMechanism
      }
    };
  }
}

export const NUMERICAL_ADAPTER = new NumericalBackendAdapter();
