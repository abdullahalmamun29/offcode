/**
 * CHUP / Offcode — Capability Solver Registry (Phase 5)
 *
 * Dispatches and executes a CapabilityPlan by delegating through the formal
 * BackendRegistry and specialized engine adapters.
 *
 * Invariants:
 * - Unifies the interface, not the implementations.
 * - Zero reliance on domain classification.
 * - Fully deterministic and reproducible.
 */

import {
  CapabilityPlan,
  CapabilitySolverResult
} from '../models/capabilityModel';
import { StructuredProblem } from '../models/problemSpec';
import { BACKEND_REGISTRY } from '../backend/backendRegistry';

export class CapabilitySolverRegistry {
  /**
   * Execute a CapabilityPlan to produce compilable, verified C++ code
   * through the formal backend boundary.
   */
  public async executePlan(
    plan: CapabilityPlan,
    problem?: StructuredProblem
  ): Promise<CapabilitySolverResult> {
    return BACKEND_REGISTRY.resolveAndExecute(plan, problem);
  }
}

export const CAPABILITY_SOLVER_REGISTRY = new CapabilitySolverRegistry();
