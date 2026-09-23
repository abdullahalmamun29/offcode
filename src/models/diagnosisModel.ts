/**
 * CHUP Phase 9 — Self-Diagnosis and Self-Correction Model (TypeScript Mirror).
 *
 * Strongly-typed mirror of the Python Self-Diagnosis IR.
 * Enforces zero 'any' across IPC boundaries and provides fail-closed schema validation.
 */

export type DiagnosticMode =
  | 'UNKNOWN_FAMILY'
  | 'KNOWN_FAMILY_INVALID_ASSUMPTIONS'
  | 'VALID_CANDIDATE_IMPLEMENTATION_BUG'
  | 'AMBIGUOUS_CANDIDATE_SET'
  | 'ORACLE_DEFECT'
  | 'TEST_HARNESS_DEFECT';

export type ClassificationStatus = 'CLASSIFIED' | 'UNRESOLVED';

export type OracleStatus = 'HEALTHY' | 'DEFECT_CONFIRMED' | 'INCONSISTENT' | 'UNRESOLVED';

export type ImplementationBugKind =
  | 'MISSING_HEADER'
  | 'TYPE_WIDTH_MISMATCH'
  | 'CERTIFIED_INDEX_BASE_TRANSLATION'
  | 'CERTIFIED_BOUNDARY_GUARD'
  | 'UNCLASSIFIED_CODE_DEFECT';

export type RepairStrategy =
  | 'ADD_MISSING_HEADER'
  | 'WIDEN_TO_64BIT'
  | 'ADJUST_INDEX_BASE'
  | 'INSERT_BOUNDARY_GUARD'
  | 'NONE';

export type ReproducibilityStatus =
  | 'CONTROLLED_REPRODUCIBLE'
  | 'NOT_REPRODUCIBLE'
  | 'UNVERIFIED';

export interface StructuredEvidenceBase {
  evidence_type: string;
}

export interface OverflowEvidenceModel extends StructuredEvidenceBase {
  evidence_type: 'OVERFLOW';
  constraint_n_bound: number;
  constraint_value_bound: number;
  max_intermediate_magnitude: number;
  original_type: string;
  required_type: string;
  original_identifier: string;
  target_scope: string;
}

export interface IndexMappingEvidenceModel extends StructuredEvidenceBase {
  evidence_type: 'INDEX_MAPPING';
  external_base: number;
  internal_base: number;
  offending_expression: string;
  translated_expression: string;
  target_scope: string;
}

export interface BoundaryGuardEvidenceModel extends StructuredEvidenceBase {
  evidence_type: 'BOUNDARY_GUARD';
  boundary_condition: string;
  identity_expression: string;
  proof_reference: string;
  authoritative_source_layer: string;
}

export interface MissingHeaderEvidenceModel extends StructuredEvidenceBase {
  evidence_type: 'MISSING_HEADER';
  missing_header: string;
  required_by_identifier: string;
  compiler_diagnostic_excerpt: string;
}

export type StructuredEvidenceModel =
  | OverflowEvidenceModel
  | IndexMappingEvidenceModel
  | BoundaryGuardEvidenceModel
  | MissingHeaderEvidenceModel;

export interface DiagnosticCertificate {
  certificate_id: string;
  classification_status: ClassificationStatus;
  mode: DiagnosticMode | null;
  bug_kind: ImplementationBugKind | null;
  stage: string;

  problem_hash: string;
  requirements_hash: string;
  plan_hash: string;
  candidate_source_hash: string;
  compiler_identity_hash: string;
  test_vector_hash: string;
  generation_provenance_hash: string;

  causal_witness: Record<string, unknown>;
  reproducibility_status: ReproducibilityStatus;
  reproduction_runs: number;

  is_repairable: bool_type;
  recommended_strategy: RepairStrategy;
  structured_evidence: StructuredEvidenceModel | null;

  epistemic_status: string;
  unresolved_reason: string;
}

type bool_type = boolean;

export interface SelfCorrectionCertificate {
  certificate_id: string;
  diagnostic_certificate_id: string;
  repair_plan_id: string;

  original_source_hash: string;
  repaired_source_hash: string;

  plan_hash: string;
  requirements_hash: string;
  compiler_fingerprint: string;
  compiler_flags_hash: string;
  verification_suite_hash: string;
  phase8_suite_hash: string;
  historical_suite_hash: string;

  attempts_used: number;
  applied_strategy: RepairStrategy;
  target_symbol: string;
  target_scope: string;
  verification_passed: boolean;
}

// ---------------------------------------------------------------------------
// Fail-Closed Runtime Validators (Zero 'any')
// ---------------------------------------------------------------------------

function isRecord(val: unknown): val is Record<string, unknown> {
  return typeof val === 'object' && val !== null && !Array.isArray(val);
}

export function validateDiagnosticCertificate(data: unknown): DiagnosticCertificate {
  if (!isRecord(data)) {
    throw new Error('Invalid DiagnosticCertificate: expected object');
  }

  if (typeof data.certificate_id !== 'string' || !data.certificate_id) {
    throw new Error('Invalid DiagnosticCertificate: missing certificate_id');
  }

  const status = data.classification_status;
  if (status !== 'CLASSIFIED' && status !== 'UNRESOLVED') {
    throw new Error(`Invalid classification_status: ${String(status)}`);
  }

  const validModes: (DiagnosticMode | null)[] = [
    'UNKNOWN_FAMILY',
    'KNOWN_FAMILY_INVALID_ASSUMPTIONS',
    'VALID_CANDIDATE_IMPLEMENTATION_BUG',
    'AMBIGUOUS_CANDIDATE_SET',
    'ORACLE_DEFECT',
    'TEST_HARNESS_DEFECT',
    null,
  ];

  if (data.mode !== null && !validModes.includes(data.mode as DiagnosticMode)) {
    throw new Error(`Invalid DiagnosticMode: ${String(data.mode)}`);
  }

  if (typeof data.problem_hash !== 'string' || typeof data.plan_hash !== 'string') {
    throw new Error('Invalid DiagnosticCertificate: missing required hash bindings');
  }

  if (typeof data.is_repairable !== 'boolean') {
    throw new Error('Invalid DiagnosticCertificate: is_repairable must be boolean');
  }

  return data as unknown as DiagnosticCertificate;
}

export function validateSelfCorrectionCertificate(data: unknown): SelfCorrectionCertificate {
  if (!isRecord(data)) {
    throw new Error('Invalid SelfCorrectionCertificate: expected object');
  }

  if (typeof data.certificate_id !== 'string' || !data.certificate_id) {
    throw new Error('Invalid SelfCorrectionCertificate: missing certificate_id');
  }

  if (typeof data.attempts_used !== 'number' || data.attempts_used !== 1) {
    throw new Error('Invalid SelfCorrectionCertificate: single-shot bound violated (attempts_used must be 1)');
  }

  if (typeof data.verification_passed !== 'boolean' || !data.verification_passed) {
    throw new Error('Invalid SelfCorrectionCertificate: verification_passed must be true');
  }

  return data as unknown as SelfCorrectionCertificate;
}
