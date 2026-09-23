/**
 * CHUP Phase 7 — Explanation Model (TypeScript Mirror).
 *
 * Strongly-typed mirror of the Python Explanation IR.
 * Enforces zero 'any' across IPC boundaries and provides fail-closed schema validation.
 */

export type EvidenceKind =
  | 'OBSERVED_FACT'
  | 'DERIVED_FACT'
  | 'PROVENANCE_NODE'
  | 'CONSTRAINT'
  | 'ELIMINATION_CERTIFICATE'
  | 'CAPABILITY_CONTRACT'
  | 'RESOURCE_VERIFICATION'
  | 'PROOF_OBLIGATION'
  | 'VERIFIED_PLAN'
  | 'CONFLICT_CERTIFICATE'
  | 'AMBIGUITY_REPORT';

export interface EvidenceRef {
  evidence_id: string;
  kind: EvidenceKind;
  source_layer: string;
  summary: string;
  fingerprint?: string | null;
}

export type ClaimType =
  | 'PROBLEM_UNDERSTANDING'
  | 'PROVEN_FACT'
  | 'DERIVATION'
  | 'CONSTRAINT'
  | 'CANDIDATE_ELIMINATION'
  | 'COMPONENT_SELECTION'
  | 'COMPOSITION'
  | 'RESOURCE'
  | 'PROOF_OBLIGATION'
  | 'CORRECTNESS'
  | 'FINAL_STATUS';

export type ExplanationLevel = 'CONCISE' | 'DETAILED' | 'AUDIT_PROOF_TRACE';

export type EpistemicStatus = 'PROVEN' | 'SUPPORTED' | 'HYPOTHETICAL' | 'UNRESOLVED';

export interface ExplanationClaimBase {
  claim_id: string;
  claim_type: ClaimType;
  text: string;
  evidence_refs: EvidenceRef[];
  source_layer: string;
  epistemic_status: EpistemicStatus;
}

export interface ProblemUnderstandingClaim extends ExplanationClaimBase {
  claim_type: 'PROBLEM_UNDERSTANDING';
  dimension: string;
  key: string;
  canonical_value: string;
}

export interface ProvenFactClaim extends ExplanationClaimBase {
  claim_type: 'PROVEN_FACT';
  fact_name: string;
  tier: string;
  witness: string;
}

export interface DerivationClaim extends ExplanationClaimBase {
  claim_type: 'DERIVATION';
  derived_fact: string;
  rule_name: string;
  source_fact_ids: string[];
  witness: string;
}

export interface ConstraintClaim extends ExplanationClaimBase {
  claim_type: 'CONSTRAINT';
  constraint_name: string;
  polarity: string;
  lattice_dimension: string;
}

export interface CandidateEliminationClaim extends ExplanationClaimBase {
  claim_type: 'CANDIDATE_ELIMINATION';
  candidate_id: string;
  family: string;
  rejection_code: string;
  certificate_id: string;
  violated_constraint: string;
}

export interface ComponentSelectionClaim extends ExplanationClaimBase {
  claim_type: 'COMPONENT_SELECTION';
  component_id: string;
  role: string;
  supported_capabilities: string[];
}

export interface CompositionClaim extends ExplanationClaimBase {
  claim_type: 'COMPOSITION';
  step_index: number;
  producer_id: string;
  consumer_id: string;
  capability_name: string;
  contract_status: string;
}

export interface ResourceClaim extends ExplanationClaimBase {
  claim_type: 'RESOURCE';
  metric: string;
  bound_value: string;
  verdict: string;
}

export interface ProofObligationClaim extends ExplanationClaimBase {
  claim_type: 'PROOF_OBLIGATION';
  obligation_id: string;
  description: string;
  discharge_status: string;
  witness: string;
}

export interface CorrectnessClaim extends ExplanationClaimBase {
  claim_type: 'CORRECTNESS';
  invariant_name: string;
  argument: string;
}

export interface FinalStatusClaim extends ExplanationClaimBase {
  claim_type: 'FINAL_STATUS';
  outcome_state: string;
  plan_id: string;
  verification_artifact_id: string;
  integrity_seal?: string | null;
}

export type ExplanationClaim =
  | ProblemUnderstandingClaim
  | ProvenFactClaim
  | DerivationClaim
  | ConstraintClaim
  | CandidateEliminationClaim
  | ComponentSelectionClaim
  | CompositionClaim
  | ResourceClaim
  | ProofObligationClaim
  | CorrectnessClaim
  | FinalStatusClaim;

export interface Section<T extends ExplanationClaimBase> {
  title: string;
  claims: T[];
}

export interface ExplanationDocument {
  schema_version: string;
  problem_id: string;
  outcome_state: string;
  level: ExplanationLevel;
  understanding_section: Section<ProblemUnderstandingClaim>;
  proven_facts_section: Section<ProvenFactClaim>;
  derivation_section: Section<DerivationClaim>;
  constraint_section: Section<ConstraintClaim>;
  elimination_section: Section<CandidateEliminationClaim>;
  selection_section: Section<ComponentSelectionClaim>;
  composition_section: Section<CompositionClaim>;
  resource_section: Section<ResourceClaim>;
  correctness_section: Section<ProofObligationClaim | CorrectnessClaim>;
  summary_section: Section<FinalStatusClaim>;
}

/**
 * Validates untyped JSON payload against the ExplanationDocument schema.
 * Fails closed by returning null if required fields or structures are invalid.
 */
export function validateExplanationDocument(data: unknown): ExplanationDocument | null {
  if (!data || typeof data !== 'object') {
    return null;
  }
  const obj = data as Record<string, unknown>;

  if (typeof obj.schema_version !== 'string' || typeof obj.problem_id !== 'string') {
    return null;
  }
  if (typeof obj.outcome_state !== 'string' || typeof obj.level !== 'string') {
    return null;
  }

  // Validate sections exist
  const sections = [
    'understanding_section',
    'proven_facts_section',
    'derivation_section',
    'constraint_section',
    'elimination_section',
    'selection_section',
    'composition_section',
    'resource_section',
    'correctness_section',
    'summary_section'
  ];

  for (const secKey of sections) {
    const sec = obj[secKey];
    if (!sec || typeof sec !== 'object') {
      return null;
    }
    const secObj = sec as Record<string, unknown>;
    if (typeof secObj.title !== 'string' || !Array.isArray(secObj.claims)) {
      return null;
    }

    // Validate claims
    for (const claim of secObj.claims) {
      if (!claim || typeof claim !== 'object') {
        return null;
      }
      const c = claim as Record<string, unknown>;
      if (typeof c.claim_id !== 'string' || typeof c.claim_type !== 'string' || typeof c.text !== 'string') {
        return null;
      }
      const validStatuses = ['PROVEN', 'SUPPORTED', 'HYPOTHETICAL', 'UNRESOLVED'];
      if (typeof c.epistemic_status !== 'string' || !validStatuses.includes(c.epistemic_status)) {
        return null;
      }
      if (!Array.isArray(c.evidence_refs)) {
        return null;
      }
      // Mandatory evidence rule
      if (c.evidence_refs.length === 0) {
        return null;
      }
      for (const ref of c.evidence_refs) {
        if (!ref || typeof ref !== 'object') {
          return null;
        }
        const r = ref as Record<string, unknown>;
        if (typeof r.evidence_id !== 'string' || typeof r.kind !== 'string') {
          return null;
        }
      }
    }
  }

  return data as ExplanationDocument;
}
