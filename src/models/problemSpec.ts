export type VerificationStatus =
  | "success"
  | "unsupported"
  | "ambiguous";

export type ConfidenceBasis =
  | "exact_rule_match"
  | "synonym_match"
  | "fuzzy_match"
  | "ambiguous"
  | "unsupported";

export interface ProblemSpec {
  status: VerificationStatus;
  language: string;
  domain?: string;
  structure?: string;
  operation?: string;
  confidence: number;
  confidence_basis: ConfidenceBasis;
  error_code?: string | null;
  message?: string;
  raw_query?: string;
  normalized_query?: string;
}

export type ResolutionCode =
  | "SUCCESS"
  | "IDENTIFIED_UNSUPPORTED"
  | "CANNOT_IDENTIFY"
  | "COMPOUND_UNSUPPORTED";

export interface ResolutionResult {
  code: ResolutionCode;
  moduleId?: string;
  moduleName?: string;
  message: string;
  spec: ProblemSpec;
}
