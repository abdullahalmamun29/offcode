/**
 * CHUP / Offcode — Backend Abstraction & Integration Contracts (Phase 5)
 *
 * Defines the formal boundary between:
 * - What capability/algorithm is required (CapabilityPlan - semantic authority)
 * - How that capability is implemented by existing specialized engines (Backend - execution infrastructure)
 *
 * Core Principles:
 * 1. Capability != Algorithm != Component != ImplementationMechanism != Backend != Adapter.
 * 2. Backend candidate discovery uses supportedCapabilities / algorithms as index.
 * 3. Backend compatibility evaluation is the execution authority (mechanisms & representations).
 * 4. Zero semantic precondition duplication: semantic invariants are checked in Phase 4.
 * 5. Deterministic resolution trace recorded via BackendResolution.
 */

import {
  CapabilityPlan,
  CompositionStep,
  CapabilityFailureCode,
  CapabilityFailureLayer
} from './capabilityModel';
import { StructuredProblem } from './problemSpec';

export interface BackendDescriptor {
  /** Unique backend identifier (e.g. 'classical_data_structure_backend') */
  id: string;
  name: string;
  description: string;
  /** Indexed capabilities for initial candidate discovery */
  supportedCapabilities: string[];
  /** Indexed algorithms for candidate discovery */
  supportedAlgorithms: string[];
  /** Constituents supported by this backend */
  supportedComponents: string[];
  /** Concrete implementation mechanisms supported (e.g. 'pointer_sll', 'binary_heap_std') */
  supportedMechanisms: string[];
  /** Representations supported (e.g. 'pointer_based', 'array_based', 'stl') */
  supportedRepresentations: string[];
  /** Operations supported (e.g. 'insert', 'delete', 'search', 'solve') */
  supportedOperations: string[];
  /** Operational availability */
  availability: 'AVAILABLE' | 'DEGRADED' | 'UNAVAILABLE';
  /** Deterministic priority for tie-breaking when multiple backends are equally compatible */
  priority: number;
  version: string;
}

export interface BackendCompatibility {
  compatible: boolean;
  unsupportedRequirements: string[];
  violatedConstraints: string[];
  missingComponents: string[];
  missingMechanisms: string[];
  explanation: string;
}

export interface BackendResolution {
  candidates: string[];
  compatibilityResults: Record<string, BackendCompatibility>;
  selectedBackend: string | null;
  selectionReason: string;
  deterministicRanking: string[];
}

export interface BackendExecutionResult {
  status: 'SUCCESS' | 'UNSUPPORTED' | 'INCOMPATIBLE' | 'EXECUTION_FAILED';
  backendId: string;
  capabilityId: string;
  algorithmId: string;
  implementationMechanism: string;
  generatedCode: string;
  diagnostics: string[];
  failure?: {
    code: CapabilityFailureCode | string;
    layer: CapabilityFailureLayer | string;
    message: string;
  };
  metadata: Record<string, any>;
}

export interface Backend {
  readonly descriptor: BackendDescriptor;

  /**
   * Evaluates whether this backend can execute the given plan / composition step.
   * Checks implementation mechanisms, representations, and supported operations.
   */
  checkCompatibility(plan: CapabilityPlan, step?: CompositionStep): BackendCompatibility;

  /**
   * Executes the plan by delegating to its specialized engine adapter.
   */
  execute(plan: CapabilityPlan, problem?: StructuredProblem): Promise<BackendExecutionResult>;
}
