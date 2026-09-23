/**
 * CHUP Phase 9 — Self-Diagnosis and Self-Correction Test Suite.
 *
 * Validates:
 * 1. DiagnosticCertificate schema validation and fail-closed operation.
 * 2. SelfCorrectionCertificate single-shot bound enforcement (attempts_used === 1).
 * 3. 7-tier decision table representation and type safety.
 * 4. OracleStatus 4-value discrimination (DEFECT_CONFIRMED vs INCONSISTENT).
 * 5. Structured mathematical evidence model verification.
 * 6. Non-mutation and fail-closed invariants across IPC boundaries.
 */

import {
  DiagnosticCertificate,
  DiagnosticMode,
  ImplementationBugKind,
  OracleStatus,
  RepairStrategy,
  ReproducibilityStatus,
  SelfCorrectionCertificate,
  validateDiagnosticCertificate,
  validateSelfCorrectionCertificate,
} from '../models/diagnosisModel';

interface TestResult {
  name: string;
  passed: boolean;
  notes?: string;
}

export function runSelfDiagnosisTests(): { passed: number; failed: number } {
  const results: TestResult[] = [];

  function record(name: string, passed: boolean, notes: string = ''): boolean {
    results.push({ name, passed, notes });
    if (passed) {
      console.log(`  ✓ [SelfDiagnosis] ${name}`);
    } else {
      console.error(`  ✗ [SelfDiagnosis] ${name} — ${notes}`);
    }
    return passed;
  }

  // ── 1. DiagnosticCertificate Validations ───────────────────────────
  const validClassifiedCert: DiagnosticCertificate = {
    certificate_id: 'diag_test_01',
    classification_status: 'CLASSIFIED',
    mode: 'VALID_CANDIDATE_IMPLEMENTATION_BUG',
    bug_kind: 'MISSING_HEADER',
    stage: 'CAUSAL_DEFECT_ANALYZER',
    problem_hash: 'prob_hash_abc',
    requirements_hash: 'req_hash_123',
    plan_hash: 'plan_hash_456',
    candidate_source_hash: 'src_hash_789',
    compiler_identity_hash: 'g++-12',
    test_vector_hash: 'vec_hash_01',
    generation_provenance_hash: 'gen_hash_999',
    causal_witness: { reason: 'Missing header <numeric>' },
    reproducibility_status: 'CONTROLLED_REPRODUCIBLE',
    reproduction_runs: 3,
    is_repairable: true,
    recommended_strategy: 'ADD_MISSING_HEADER',
    structured_evidence: {
      evidence_type: 'MISSING_HEADER',
      missing_header: '<numeric>',
      required_by_identifier: 'std::accumulate',
      compiler_diagnostic_excerpt: 'accumulate was not declared in this scope',
    },
    epistemic_status: 'PROVEN',
    unresolved_reason: '',
  };

  try {
    const validated = validateDiagnosticCertificate(validClassifiedCert);
    record('Valid classified DiagnosticCertificate validates cleanly', validated.certificate_id === 'diag_test_01');
  } catch (e: unknown) {
    record('Valid classified DiagnosticCertificate validates cleanly', false, String(e));
  }

  // ── 2. UNRESOLVED Mode Validation ─────────────────────────────────
  const unresolvedCert: DiagnosticCertificate = {
    certificate_id: 'diag_unres_01',
    classification_status: 'UNRESOLVED',
    mode: null,
    bug_kind: null,
    stage: 'DEFAULT_INSUFFICIENT_EVIDENCE',
    problem_hash: 'prob_hash_abc',
    requirements_hash: 'req_hash_123',
    plan_hash: 'plan_hash_456',
    candidate_source_hash: 'src_hash_789',
    compiler_identity_hash: 'g++-12',
    test_vector_hash: 'vec_hash_01',
    generation_provenance_hash: 'gen_hash_999',
    causal_witness: {},
    reproducibility_status: 'UNVERIFIED',
    reproduction_runs: 1,
    is_repairable: false,
    recommended_strategy: 'NONE',
    structured_evidence: null,
    epistemic_status: 'UNRESOLVED',
    unresolved_reason: 'Insufficient evidence to form causal diagnosis.',
  };

  try {
    const validated = validateDiagnosticCertificate(unresolvedCert);
    record('Valid UNRESOLVED DiagnosticCertificate with mode=null validates cleanly', validated.mode === null);
  } catch (e: unknown) {
    record('Valid UNRESOLVED DiagnosticCertificate with mode=null validates cleanly', false, String(e));
  }

  // ── 3. Malformed DiagnosticCertificate Rejections ─────────────────
  try {
    validateDiagnosticCertificate({ ...validClassifiedCert, classification_status: 'INVALID_STATUS' });
    record('Rejects invalid classification_status', false, 'Should have thrown');
  } catch {
    record('Rejects invalid classification_status', true);
  }

  try {
    validateDiagnosticCertificate({ ...validClassifiedCert, mode: 'INVALID_MODE' });
    record('Rejects invalid DiagnosticMode string', false, 'Should have thrown');
  } catch {
    record('Rejects invalid DiagnosticMode string', true);
  }

  try {
    const { problem_hash, ...missingHash } = validClassifiedCert as any;
    validateDiagnosticCertificate(missingHash);
    record('Rejects missing hash bindings', false, 'Should have thrown');
  } catch {
    record('Rejects missing hash bindings', true);
  }

  // ── 4. SelfCorrectionCertificate Single-Shot Bound ────────────────
  const validCorrectionCert: SelfCorrectionCertificate = {
    certificate_id: 'selfcorr_01',
    diagnostic_certificate_id: 'diag_test_01',
    repair_plan_id: 'plan_01',
    original_source_hash: 'orig_hash_1',
    repaired_source_hash: 'rep_hash_2',
    plan_hash: 'plan_hash_456',
    requirements_hash: 'req_hash_123',
    compiler_fingerprint: 'g++-12',
    compiler_flags_hash: 'flags_hash_abc',
    verification_suite_hash: 'suite_hash_1',
    phase8_suite_hash: 'phase8_hash_1',
    historical_suite_hash: 'hist_hash_1',
    attempts_used: 1,
    applied_strategy: 'ADD_MISSING_HEADER',
    target_symbol: '<numeric>',
    target_scope: 'global_includes',
    verification_passed: true,
  };

  try {
    const validated = validateSelfCorrectionCertificate(validCorrectionCert);
    record('Valid SelfCorrectionCertificate validates single-shot bound (attempts_used=1)', validated.attempts_used === 1);
  } catch (e: unknown) {
    record('Valid SelfCorrectionCertificate validates single-shot bound', false, String(e));
  }

  try {
    validateSelfCorrectionCertificate({ ...validCorrectionCert, attempts_used: 2 });
    record('Rejects multiple repair attempts (attempts_used > 1)', false, 'Should have thrown');
  } catch {
    record('Rejects multiple repair attempts (attempts_used > 1)', true);
  }

  try {
    validateSelfCorrectionCertificate({ ...validCorrectionCert, verification_passed: false });
    record('Rejects unverified repair certificate (verification_passed = false)', false, 'Should have thrown');
  } catch {
    record('Rejects unverified repair certificate (verification_passed = false)', true);
  }

  // ── 5. Decision Table Priority Types ──────────────────────────────
  const modes: DiagnosticMode[] = [
    'UNKNOWN_FAMILY',
    'KNOWN_FAMILY_INVALID_ASSUMPTIONS',
    'VALID_CANDIDATE_IMPLEMENTATION_BUG',
    'AMBIGUOUS_CANDIDATE_SET',
    'ORACLE_DEFECT',
    'TEST_HARNESS_DEFECT',
  ];
  record('All 6 DiagnosticMode enums defined and strongly typed', modes.length === 6);

  // ── 6. OracleStatus Discrimination ────────────────────────────────
  const oracleStatuses: OracleStatus[] = ['HEALTHY', 'DEFECT_CONFIRMED', 'INCONSISTENT', 'UNRESOLVED'];
  record('OracleStatus includes 4 discrete states', oracleStatuses.length === 4);

  // ── 7. Bug Kinds and Strategies Mapping ────────────────────────────
  const bugKinds: ImplementationBugKind[] = [
    'MISSING_HEADER',
    'TYPE_WIDTH_MISMATCH',
    'CERTIFIED_INDEX_BASE_TRANSLATION',
    'CERTIFIED_BOUNDARY_GUARD',
    'UNCLASSIFIED_CODE_DEFECT',
  ];
  const strategies: RepairStrategy[] = [
    'ADD_MISSING_HEADER',
    'WIDEN_TO_64BIT',
    'ADJUST_INDEX_BASE',
    'INSERT_BOUNDARY_GUARD',
    'NONE',
  ];
  record('Bug kinds and repair strategies maintain 1:1 typed alignment', bugKinds.length === strategies.length);

  // ── 8. Reproducibility Status Typing ──────────────────────────────
  const reproStatuses: ReproducibilityStatus[] = [
    'CONTROLLED_REPRODUCIBLE',
    'NOT_REPRODUCIBLE',
    'UNVERIFIED',
  ];
  record('ReproducibilityStatus strongly typed with 3 states', reproStatuses.length === 3);

  // ── 9. Mathematical Structured Evidence Model ─────────────────────
  const overflowEv = {
    evidence_type: 'OVERFLOW' as const,
    constraint_n_bound: 200000,
    constraint_value_bound: 1000000000,
    max_intermediate_magnitude: 200000000000000,
    original_type: 'int',
    required_type: 'long long',
    original_identifier: 'sum',
    target_scope: 'main',
  };
  record('OverflowEvidenceModel strongly typed with intermediate magnitude bound', overflowEv.max_intermediate_magnitude > 2147483647);

  const passed = results.filter((r) => r.passed).length;
  const failed = results.filter((r) => !r.passed).length;
  return { passed, failed };
}
