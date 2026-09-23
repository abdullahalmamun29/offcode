/**
 * CHUP / Offcode — Universal Capability-First Router (Phase 4)
 *
 * Unifies the entire front-to-back pipeline:
 * Raw Input
 *   ↓
 * Lexical Normalization (Universal Normalizer + Vocabulary-Driven Fuzzy Matcher)
 *   ↓
 * Canonicalization (Canonicalizer: Multi-Token Concepts)
 *   ↓
 * Semantic Extraction (SemanticExtractor: Entities, Operations, Constraints)
 *   ↓
 * Capability Retrieval & Resolution (CapabilityResolver)
 *   ↓
 * Capability Plan (CapabilityPlanner: Components, State Transitions, Proof Obligations)
 *   ↓
 * Execution / Solving (CapabilitySolverRegistry)
 *   ↓
 * Generation & Verification
 *
 * Core Invariant: Domain is strictly metadata; it is NEVER consulted during routing!
 */

import {
  CapabilityPlan,
  CapabilityRequest,
  CapabilitySolverResult
} from '../models/capabilityModel';
import { StructuredProblem } from '../models/problemSpec';
import { normalizeInputUniversal } from './universalNormalizer';
import { canonicalize } from './canonicalizer';
import { extractSemanticInput } from './semanticExtractor';
import { resolveCapabilityRequest } from './capabilityResolver';
import { buildCapabilityPlan } from './capabilityPlanner';
import { CAPABILITY_SOLVER_REGISTRY } from '../solver/capabilitySolverRegistry';

export class UniversalRouter {
  /**
   * Constructs a CapabilityRequest IR directly from raw query text.
   */
  public resolveRequest(text: string, problem?: StructuredProblem): CapabilityRequest {
    const normalized = normalizeInputUniversal(text);
    const canonicalized = canonicalize(normalized);
    const semantic = extractSemanticInput(canonicalized);
    return resolveCapabilityRequest(semantic, problem);
  }

  /**
   * Constructs a domain-independent CapabilityPlan from raw query text.
   */
  public createPlan(text: string, problem?: StructuredProblem): CapabilityPlan {
    const request = this.resolveRequest(text, problem);
    return buildCapabilityPlan(request, problem);
  }

  /**
   * Resolves, plans, and executes code generation in one unified pipeline.
   */
  public async routeAndSolve(
    text: string,
    problem?: StructuredProblem
  ): Promise<CapabilitySolverResult> {
    const norm = normalizeInputUniversal(text);
    const resolvedProblem: StructuredProblem = problem || {
      rawText: text,
      normalizedText: norm.normalizedText,
      statement: text,
      title: null,
      problemType: null,
      domain: null,
      inputSpecification: null,
      outputSpecification: null,
      constraints: [],
      examples: [],
      notes: null,
      timeLimit: null,
      memoryLimit: null,
      source: null,
      parserConfidence: 1.0
    };
    const plan = this.createPlan(text, resolvedProblem);
    return CAPABILITY_SOLVER_REGISTRY.executePlan(plan, resolvedProblem);
  }
}

export const UNIVERSAL_ROUTER = new UniversalRouter();
