/**
 * CHUP Phase 10 — Research-Level Algorithmic Reasoning Model (TypeScript Mirror).
 *
 * Strongly-typed mirror of the Python Research IR.
 * Enforces zero 'any' across IPC boundaries and provides fail-closed schema validation.
 */

export type EpistemicStatus =
  | 'PROVEN'
  | 'REFUTED'
  | 'SUPPORTED'
  | 'HYPOTHETICAL'
  | 'UNRESOLVED';

export type ReductionType =
  | 'PROJECT_SELECTION_TO_MIN_CUT'
  | 'BIPARTITE_MATCHING_TO_VERTEX_COVER'
  | 'VERTEX_COVER_TO_INDEPENDENT_SET'
  | 'DIFFERENCE_CONSTRAINTS_TO_SHORTEST_PATH'
  | 'PLANAR_DUAL_ROUTING'
  | 'COMPLEMENT_INCLUSION_EXCLUSION'
  | 'COMPOSED_REDUCTION'
  | 'HARDNESS_REDUCTION_REVERSE';

export type HypothesisSchema =
  | 'GREEDY_BY_KEY'
  | 'MONOTONICITY'
  | 'EXCHANGE_ARGUMENT'
  | 'STATE_DIMENSION_REMOVAL'
  | 'LOCAL_OPTIMALITY'
  | 'PARITY_STRUCTURE'
  | 'POTENTIAL_DECREASE';

export type InvariantClass =
  | 'LINEAR_COMBINATION'
  | 'MODULAR_CONSERVATION'
  | 'PARITY_INVARIANT'
  | 'BOUNDED_POTENTIAL'
  | 'XOR_SUM_GRUNDY';

export interface PredicateEvidenceModel {
  predicate_name: string;
  satisfied: boolean;
  witness_data?: Record<string, unknown>;
}

export interface ApplicabilityProofModel {
  predicates: PredicateEvidenceModel[];
  discharged: boolean;
}

export interface ProofObligationItemModel {
  obligation_id: string;
  property_name: string;
  discharged: boolean;
  evidence_details?: string;
}

export interface SemanticPreservationProofModel {
  obligations: ProofObligationItemModel[];
  discharged: boolean;
}

export interface ComplexityBoundModel {
  asymptotic_formula: string;
  parameter_dependencies: string[];
  is_polynomial: boolean;
  budget_satisfied: boolean;
}

export interface ComplexityProofModel {
  forward_bound: ComplexityBoundModel;
  solver_bound: ComplexityBoundModel;
  backward_bound: ComplexityBoundModel;
  total_bound: ComplexityBoundModel;
  discharged: boolean;
}

export interface ReductionCertificateModel {
  certificate_id: string;
  source_problem_id: string;
  target_family_id: string;
  reduction_type: ReductionType;
  applicability_proof: ApplicabilityProofModel;
  semantic_proof: SemanticPreservationProofModel;
  complexity_proof: ComplexityProofModel;
  forward_transform_name: string;
  backward_solution_map_name: string;
  domain_assumptions: string[];
  theorem_id: string;
  theorem_version: string;
  problem_hash: string;
  requirements_hash: string;
  status: EpistemicStatus;
}

export interface FiniteSearchEnvelopeModel {
  domain_type: string;
  size_bound: number;
  value_bound: number;
  structural_constraints: string[];
  max_states_budget: number;
  timeout_ms_budget: number;
  symmetry_reduction?: boolean;
}

export interface RefutationCertificateModel {
  certificate_id: string;
  hypothesis_id: string;
  schema: HypothesisSchema;
  counterexample_witness: Record<string, unknown>;
  hypothesis_output: string;
  oracle_output: string;
  envelope_fingerprint: string;
  status: EpistemicStatus;
}

export interface CorroborationCertificateModel {
  certificate_id: string;
  hypothesis_id: string;
  schema: HypothesisSchema;
  envelope_fingerprint: string;
  states_evaluated: number;
  exhaustive_within_envelope: boolean;
  status: EpistemicStatus;
}

export interface InvariantCertificateModel {
  certificate_id: string;
  invariant_class: InvariantClass;
  expression_representation: string;
  codomain: string;
  well_founded_proven: boolean;
  strict_decrease_proven: boolean;
  modular_conservation_proven: boolean;
  termination_bound_steps: number | null;
  status: EpistemicStatus;
}

export interface HardnessCertificateModel {
  certificate_id: string;
  user_problem_id: string;
  known_hard_core_id: string;
  reduction_proof: ReductionCertificateModel;
  is_np_hard: boolean;
  status: EpistemicStatus;
}

export interface ResourceFeasibilityCertificateModel {
  certificate_id: string;
  algorithm_name: string;
  parameter_name: string;
  parameter_value: number;
  complexity_formula: string;
  estimated_operations: number;
  max_operations_budget: number;
  is_feasible: boolean;
  status_label: string;
}

export interface ResearchCandidateArtifactModel {
  artifact_id: string;
  problem_id: string;
  target_solver_id: string;
  reduction_certificate: ReductionCertificateModel | null;
  corroboration_certificate: CorroborationCertificateModel | null;
  refutation_certificate: RefutationCertificateModel | null;
  provenance_hash: string;
  is_sealed: boolean;
}

export interface ResearchPipelineResultModel {
  problem_id: string;
  admitted_to_planning: boolean;
  status: EpistemicStatus;
  reason: string;
}

// ---------------------------------------------------------------------------
// Schema Validators (Fail-Closed)
// ---------------------------------------------------------------------------

function isObject(val: unknown): val is Record<string, unknown> {
  return typeof val === 'object' && val !== null && !Array.isArray(val);
}

export function validateReductionCertificate(data: unknown): ReductionCertificateModel {
  if (!isObject(data)) {
    throw new Error('ReductionCertificate must be an object');
  }

  const validEpistemic: EpistemicStatus[] = ['PROVEN', 'REFUTED', 'SUPPORTED', 'HYPOTHETICAL', 'UNRESOLVED'];
  if (typeof data.certificate_id !== 'string' || !data.certificate_id) {
    throw new Error('Invalid or missing certificate_id');
  }
  if (typeof data.source_problem_id !== 'string' || !data.source_problem_id) {
    throw new Error('Invalid or missing source_problem_id');
  }
  if (typeof data.target_family_id !== 'string' || !data.target_family_id) {
    throw new Error('Invalid or missing target_family_id');
  }
  if (!validEpistemic.includes(data.status as EpistemicStatus)) {
    throw new Error(`Invalid epistemic status: ${String(data.status)}`);
  }
  if (!isObject(data.applicability_proof) || typeof data.applicability_proof.discharged !== 'boolean') {
    throw new Error('Invalid or missing applicability_proof');
  }
  if (!isObject(data.semantic_proof) || typeof data.semantic_proof.discharged !== 'boolean') {
    throw new Error('Invalid or missing semantic_proof');
  }
  if (!isObject(data.complexity_proof) || typeof data.complexity_proof.discharged !== 'boolean') {
    throw new Error('Invalid or missing complexity_proof');
  }

  return data as unknown as ReductionCertificateModel;
}

export function validateRefutationCertificate(data: unknown): RefutationCertificateModel {
  if (!isObject(data)) {
    throw new Error('RefutationCertificate must be an object');
  }
  if (typeof data.certificate_id !== 'string' || !data.certificate_id) {
    throw new Error('Invalid or missing certificate_id');
  }
  if (typeof data.hypothesis_id !== 'string' || !data.hypothesis_id) {
    throw new Error('Invalid or missing hypothesis_id');
  }
  if (!isObject(data.counterexample_witness)) {
    throw new Error('Invalid or missing counterexample_witness');
  }
  if (data.status !== 'REFUTED') {
    throw new Error(`RefutationCertificate status must be REFUTED, got ${String(data.status)}`);
  }

  return data as unknown as RefutationCertificateModel;
}

export function validateCorroborationCertificate(data: unknown): CorroborationCertificateModel {
  if (!isObject(data)) {
    throw new Error('CorroborationCertificate must be an object');
  }
  if (typeof data.certificate_id !== 'string' || !data.certificate_id) {
    throw new Error('Invalid or missing certificate_id');
  }
  if (typeof data.states_evaluated !== 'number' || data.states_evaluated < 0) {
    throw new Error('Invalid states_evaluated');
  }
  if (data.status !== 'SUPPORTED') {
    throw new Error(`CorroborationCertificate status must be SUPPORTED, got ${String(data.status)}`);
  }

  return data as unknown as CorroborationCertificateModel;
}

export function validateInvariantCertificate(data: unknown): InvariantCertificateModel {
  if (!isObject(data)) {
    throw new Error('InvariantCertificate must be an object');
  }
  if (typeof data.certificate_id !== 'string' || !data.certificate_id) {
    throw new Error('Invalid or missing certificate_id');
  }
  if (typeof data.expression_representation !== 'string') {
    throw new Error('Invalid expression_representation');
  }
  if (data.status !== 'PROVEN') {
    throw new Error(`InvariantCertificate status must be PROVEN, got ${String(data.status)}`);
  }

  return data as unknown as InvariantCertificateModel;
}

export function validateHardnessCertificate(data: unknown): HardnessCertificateModel {
  if (!isObject(data)) {
    throw new Error('HardnessCertificate must be an object');
  }
  if (typeof data.certificate_id !== 'string' || !data.certificate_id) {
    throw new Error('Invalid or missing certificate_id');
  }
  if (typeof data.known_hard_core_id !== 'string') {
    throw new Error('Invalid known_hard_core_id');
  }
  if (!isObject(data.reduction_proof)) {
    throw new Error('Missing reduction_proof in HardnessCertificate');
  }
  validateReductionCertificate(data.reduction_proof);

  return data as unknown as HardnessCertificateModel;
}

export function validateResourceFeasibilityCertificate(data: unknown): ResourceFeasibilityCertificateModel {
  if (!isObject(data)) {
    throw new Error('ResourceFeasibilityCertificate must be an object');
  }
  if (typeof data.certificate_id !== 'string' || !data.certificate_id) {
    throw new Error('Invalid or missing certificate_id');
  }
  if (typeof data.status_label !== 'string' || !data.status_label) {
    throw new Error('Invalid status_label');
  }
  if (typeof data.is_feasible !== 'boolean') {
    throw new Error('Invalid is_feasible');
  }

  return data as unknown as ResourceFeasibilityCertificateModel;
}

export function validateResearchCandidateArtifact(data: unknown): ResearchCandidateArtifactModel {
  if (!isObject(data)) {
    throw new Error('ResearchCandidateArtifact must be an object');
  }
  if (typeof data.artifact_id !== 'string' || !data.artifact_id) {
    throw new Error('Invalid artifact_id');
  }
  if (typeof data.provenance_hash !== 'string' || !data.provenance_hash) {
    throw new Error('Invalid provenance_hash');
  }
  if (typeof data.is_sealed !== 'boolean') {
    throw new Error('Invalid is_sealed');
  }

  return data as unknown as ResearchCandidateArtifactModel;
}
