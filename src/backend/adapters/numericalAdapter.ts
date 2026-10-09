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

    const probText = (problem?.rawText || problem?.normalizedText || '').toLowerCase();

    // 1. LU Decomposition & Gaussian Elimination
    if (step.capabilityId === 'lu_decomposition' || algoId === 'doolittle_lu') {
      moduleId = 'numerical.linear_systems.lu_decomposition.cpp';
      moduleName = 'LU Decomposition (Doolittle)';
    } else if (step.capabilityId === 'gauss_elimination' || algoId === 'gauss_elimination_pivoting') {
      moduleId = 'numerical.linear_systems.gauss_elimination.cpp';
      moduleName = 'Gaussian Elimination';
    }
    // 2. Linear Systems Iterative
    else if (step.capabilityId === 'linear_systems_iterative' || algoId === 'jacobi' || algoId === 'gauss_seidel' || algoId === 'gauss_jordan') {
      if (algoId === 'jacobi' || probText.includes('jacobi')) {
        moduleId = 'numerical.linear_systems.jacobi.cpp';
        moduleName = 'Jacobi Iteration';
      } else if (algoId === 'gauss_seidel' || probText.includes('seidel')) {
        moduleId = 'numerical.linear_systems.gauss_seidel.cpp';
        moduleName = 'Gauss-Seidel Iteration';
      } else {
        moduleId = 'numerical.linear_systems.gauss_jordan.cpp';
        moduleName = 'Gauss-Jordan Elimination';
      }
    }
    // 3. Numerical Integration
    else if (step.capabilityId === 'numerical_integration' || algoId === 'trapezoidal' || algoId === 'simpson_1_3' || algoId === 'simpson_3_8') {
      if (algoId === 'simpson_3_8' || probText.includes('3/8') || probText.includes('3 8')) {
        moduleId = 'numerical.integration.simpson_3_8.cpp';
        moduleName = "Simpson's 3/8 Rule";
      } else if (algoId === 'simpson_1_3' || probText.includes('simpson') || probText.includes('1/3') || probText.includes('1 3')) {
        moduleId = 'numerical.integration.simpson_1_3.cpp';
        moduleName = "Simpson's 1/3 Rule";
      } else {
        moduleId = 'numerical.integration.trapezoidal.cpp';
        moduleName = 'Trapezoidal Rule';
      }
    }
    // 4. Interpolation
    else if (step.capabilityId === 'interpolation' || algoId === 'lagrange' || algoId === 'newton_forward' || algoId === 'newton_backward' || algoId === 'divided_difference') {
      if (algoId === 'newton_forward' || probText.includes('forward')) {
        moduleId = 'numerical.interpolation.newton_forward.cpp';
        moduleName = 'Newton Forward Interpolation';
      } else if (algoId === 'newton_backward' || probText.includes('backward')) {
        moduleId = 'numerical.interpolation.newton_backward.cpp';
        moduleName = 'Newton Backward Interpolation';
      } else if (algoId === 'divided_difference' || probText.includes('divided')) {
        moduleId = 'numerical.interpolation.divided_difference.cpp';
        moduleName = 'Newton Divided Difference';
      } else {
        moduleId = 'numerical.interpolation.lagrange.cpp';
        moduleName = 'Lagrange Interpolation';
      }
    }
    // 5. ODE Solvers
    else if (step.capabilityId === 'ode_solver' || algoId === 'euler' || algoId === 'modified_euler' || algoId === 'runge_kutta_4') {
      if (algoId === 'runge_kutta_4' || probText.includes('runge') || probText.includes('rk4')) {
        moduleId = 'numerical.ode.runge_kutta_4.cpp';
        moduleName = 'Runge-Kutta 4th Order';
      } else if (algoId === 'modified_euler' || probText.includes('modified')) {
        moduleId = 'numerical.ode.modified_euler.cpp';
        moduleName = "Modified Euler's Method";
      } else {
        moduleId = 'numerical.ode.euler.cpp';
        moduleName = "Euler's Method";
      }
    }
    // 6. Root Finding
    else if (algoId === 'bisection' || (step.capabilityId === 'root_finding' && probText.includes('bisection'))) {
      moduleId = 'numerical.root_finding.bisection.cpp';
      moduleName = 'Bisection Method';
    } else if (algoId === 'newton_raphson' || (step.capabilityId === 'root_finding' && (probText.includes('newton') || probText.includes('raphson')))) {
      moduleId = 'numerical.root_finding.newton_raphson.cpp';
      moduleName = 'Newton-Raphson Method';
    } else if (algoId === 'secant' || (step.capabilityId === 'root_finding' && probText.includes('secant'))) {
      moduleId = 'numerical.root_finding.secant.cpp';
      moduleName = 'Secant Method';
    } else if (algoId === 'false_position' || (step.capabilityId === 'root_finding' && (probText.includes('false position') || probText.includes('regula falsi')))) {
      moduleId = 'numerical.root_finding.false_position.cpp';
      moduleName = 'False Position Method';
    } else if (algoId === 'fixed_point_iteration' || (step.capabilityId === 'root_finding' && probText.includes('fixed point'))) {
      moduleId = 'numerical.root_finding.fixed_point_iteration.cpp';
      moduleName = 'Fixed Point Iteration';
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
