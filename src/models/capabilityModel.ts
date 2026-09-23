/**
 * CHUP / Offcode — Canonical Capability & Composition Model (Phase 4)
 *
 * Implements the 4-tier abstraction architecture:
 * 1. Capability: High-level computational objective / interface contract.
 * 2. Algorithm: Specific mathematical or algorithmic method fulfilling a capability.
 * 3. AlgorithmComponent: Reusable constituent building block (e.g. priority queue, DSU, relaxation).
 * 4. ImplementationMechanism: Concrete data representation or code pattern (e.g. pointer_based, binary_heap).
 *
 * Enforces:
 * - Domain is metadata ONLY (never a routing stage).
 * - Multi-layer failure taxonomy.
 * - Composition with state transitions, preconditions, loop invariants, and proof obligations.
 * - Provenance tracking for every resolved evidence item.
 */

// ── 1. The 4-Tier Abstraction Model ──────────────────────────────────────────

export interface AlgorithmComponent {
  id: string; // e.g. 'priority_queue', 'disjoint_set_union', 'edge_relaxation', 'pivoting'
  name: string;
  description: string;
  role: 'data_organizer' | 'invariant_maintainer' | 'transition_step' | 'numerical_kernel';
  requiredInterfaces: string[];
  providedInterfaces: string[];
}

export interface ImplementationMechanism {
  id: string; // e.g. 'binary_heap_std', 'pointer_sll', 'cyclic_array_queue', 'flat_matrix_vector'
  name: string;
  representation: 'pointer_based' | 'array_based' | 'stl' | 'matrix_dense' | 'custom_struct';
  timeComplexity: string;
  spaceComplexity: string;
  supportedConstraints: Record<string, unknown>;
}

export interface AlgorithmDefinition {
  id: string; // e.g. 'dijkstra', 'kruskal', 'doolittle_lu', 'bisection', 'binary_search'
  name: string;
  aliases: string[];
  capabilityId: string; // High-level capability this algorithm satisfies
  requiredComponents: string[]; // AlgorithmComponent IDs (e.g. ['priority_queue', 'edge_relaxation'])
  supportedMechanisms: string[]; // ImplementationMechanism IDs
  preconditions: string[]; // e.g. ['non_negative_edge_weights', 'non_singular_pivot']
  invariants: string[]; // e.g. ['triangle_inequality_holds', 'pivot_row_maximized']
  postconditions: string[]; // e.g. ['distances_minimal', 'factors_lu_exact']
  complexity: {
    time: string;
    space: string;
  };
}

export interface Capability {
  id: string; // e.g. 'single_source_shortest_path', 'dynamic_sequence_storage', 'linear_system_solver'
  canonicalName: string;
  parentId?: string; // e.g. 'shortest_path' for hierarchy DAG
  aliases: string[];
  semanticDescription: string;
  domains: string[]; // METADATA ONLY! e.g. ['graph_algorithm', 'shortest_path', 'competitive_programming']
  supportedOperations: string[]; // e.g. ['solve', 'implement', 'insert', 'delete', 'search', 'compute']
  representations: string[]; // e.g. ['pointer_based', 'array_based', 'stl']
  algorithms: string[]; // AlgorithmDefinition IDs fulfilling this capability
  requiredStates: string[];
  producedStates: string[];
  constraints: Record<string, unknown>;
}

export interface CapabilityHierarchyNode {
  id: string;
  name: string;
  parentId?: string;
  children: string[];
  associatedCapabilities: string[];
}

// ── 2. Evidence & Provenance Tracking ─────────────────────────────────────────

export type EvidenceType =
  | 'explicit_identifier'
  | 'alias'
  | 'objective'
  | 'operation'
  | 'constraint'
  | 'structural_context';

export interface CapabilityEvidence {
  sourceText: string;
  normalizedText: string;
  evidenceType: EvidenceType;
  capabilityId: string;
  algorithmId?: string;
  strength: number; // 0.0 to 1.0
  tokenSpan: [number, number];
}

export interface CapabilityMatch {
  capabilityId: string;
  algorithmId?: string;
  evidence: CapabilityEvidence[];
  source: 'direct_mention' | 'synonym' | 'objective_inference' | 'structural_inference';
  resolutionPath: string[];
  confidence: number;
}

// ── 3. Multi-Layer Integrated Failure Taxonomy ───────────────────────────────

export type CapabilityFailureLayer =
  | 'CAPABILITY_RESOLUTION'
  | 'DERIVATION'
  | 'COMPONENT_SELECTION'
  | 'COMPOSITION'
  | 'BACKEND_SELECTION'
  | 'BACKEND_COMPATIBILITY'
  | 'IMPLEMENTATION'
  | 'VERIFICATION';

export type CapabilityFailureCode =
  // Capability Resolution Layer
  | 'CAPABILITY_AMBIGUOUS'
  | 'CAPABILITY_CONFLICT'
  | 'CAPABILITY_UNSUPPORTED'
  | 'CAPABILITY_PARTIALLY_RESOLVED'
  // Derivation Layer
  | 'DERIVATION_UNSUPPORTED'
  // Component Selection Layer
  | 'COMPONENT_UNSUPPORTED'
  | 'COMPONENT_INCOMPATIBLE'
  // Composition Layer
  | 'COMPOSITION_UNSUPPORTED'
  | 'PROOF_OBLIGATION_UNMET'
  | 'STATE_FLOW_BROKEN'
  // Backend Selection & Compatibility Layer (Phase 5)
  | 'BACKEND_UNAVAILABLE'
  | 'BACKEND_INCOMPATIBLE'
  | 'EXECUTION_FAILED'
  // Implementation Layer
  | 'IMPLEMENTATION_UNSUPPORTED'
  | 'GENERATOR_VARIANT_UNSUPPORTED'
  // Verification Layer
  | 'VERIFICATION_FAILED';

export type CapabilityRequestStatus =
  | 'CAPABILITY_RESOLVED'
  | 'CAPABILITY_AMBIGUOUS'
  | 'CAPABILITY_PARTIALLY_RESOLVED'
  | 'CAPABILITY_UNSUPPORTED'
  | 'CAPABILITY_CONFLICT';

// ── 4. Composition & Proof Obligations ────────────────────────────────────────

export interface ProofObligation {
  obligationId: string;
  description: string;
  dischargeType: 'certified' | 'precondition_check' | 'runtime_assertion';
  discharged: boolean;
  witness?: string;
}

export interface CompositionStep {
  stepIndex: number;
  capabilityId: string;
  algorithmId: string;
  requiredComponents: string[];
  implementationMechanism: string;
  requiredStates: string[];
  producedStates: string[];
  preconditions: string[];
  postconditions: string[];
  invariants: string[];
  proofObligations: ProofObligation[];
  representationRequirements: Record<string, string>;
  constraintRequirements: Record<string, unknown>;
  parameters?: Record<string, unknown>;
}

// ── 5. Capability Request IR ──────────────────────────────────────────────────

export interface CapabilityRequest {
  capabilities: string[]; // Primary resolved canonical capability IDs
  primaryAlgorithmId?: string; // Resolved specific algorithm (if explicit)
  operations: string[];
  attributes: {
    position?: 'beginning' | 'end' | 'middle' | 'index' | string;
    representation?: 'pointer_based' | 'array_based' | 'stl' | string;
    graphType?: 'directed' | 'undirected' | string;
    weight?: 'weighted' | 'unweighted' | 'nonnegative' | 'negative' | string;
    queryType?: 'point' | 'range' | string;
    updateType?: 'point' | 'range' | string;
    stlAllowed?: boolean;
    [key: string]: unknown;
  };
  representations: string[];
  parameters: Record<string, unknown>;
  constraints: string[];
  requiredStates: string[];
  producedStates: string[];
  domains: string[]; // Metadata ONLY
  evidence: CapabilityEvidence[];
  matches: CapabilityMatch[];
  unresolved: string[];
  status: CapabilityRequestStatus;
  failureCode?: CapabilityFailureCode;
  failureLayer?: CapabilityFailureLayer;
  failureMessage?: string;
  ambiguousCandidates?: string[];
  conflictReason?: string;
}

// ── 6. Capability Execution Plan ──────────────────────────────────────────────

export interface CapabilityPlan {
  status: CapabilityRequestStatus;
  failureCode?: CapabilityFailureCode;
  failureLayer?: CapabilityFailureLayer;
  failureMessage?: string;
  resolvedCapabilities: string[];
  primaryAlgorithm?: string;
  operationPlan: string[];
  requiredComponents: string[];
  selectedMechanism: string;
  stateRequirements: string[];
  stateProduction: string[];
  constraints: string[];
  solverCandidates: string[];
  selectedSolver: string | null;
  selectedBackend?: string | null;
  backendResolution?: any;
  compositionSteps: CompositionStep[];
  verificationObligations: ProofObligation[];
  domains: string[]; // Metadata
  explanation: string;
}

// ── 7. Standardized Solver Result ─────────────────────────────────────────────

export interface CapabilitySolverResult {
  success: boolean;
  status: CapabilityRequestStatus;
  capabilityId?: string;
  algorithmId?: string;
  approach: string;
  code: string;
  reasoning: string;
  plan?: CapabilityPlan;
  verification?: {
    compiled: boolean;
    allPassed: boolean;
    errors?: string[];
  } | null;
  failureCode?: CapabilityFailureCode;
  failureLayer?: CapabilityFailureLayer;
  limitationMessage?: string | null;
  backendResolution?: any;
  metadata: {
    domains: string[];
    componentsUsed: string[];
    mechanism: string;
    backendId?: string;
    backendResolution?: any;
    [key: string]: any;
  };
}
