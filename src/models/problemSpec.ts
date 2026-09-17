export type VerificationStatus = 'success' | 'unsupported' | 'ambiguous' | 'negated' | 'question';
export type ConfidenceBasis = 'exact_rule_match' | 'synonym_match' | 'fuzzy_match' | 'ambiguous' | 'unsupported';
export type IntentType = 'code_generation' | 'conceptual_question' | 'ambiguous';
export type DomainType = 'data_structure' | 'algorithm' | 'numerical';

export interface ProblemSpecV1 {
  status: VerificationStatus;
  language: string;
  domain: DomainType;
  intent: IntentType;
  structure: {
    type: string | null;
    confidence_basis: ConfidenceBasis;
  };
  operation: {
    action: string | null;
    position: string | null;
    combined: string | null;
    target_value?: string | number | null;
    target_index?: number | null;
    negated: boolean;
    parameters?: Record<string, unknown>;
  };
  compound: {
    is_compound: boolean;
    detected_actions: string[];
    sequencing_marker?: string | null;
  };
  numerical: {
    method: string | null;
    category: string | null;
  };
  confidence: number;
  confidence_basis: ConfidenceBasis;
  error_code: string | null;
  message: string;
  raw_query: string;
  normalized_query: string;
  generation_mode?: 'single' | 'menu';
  menu_operations?: string[];
}

export type ResolutionCode =
  | 'SUCCESS'
  | 'NEGATED'
  | 'QUESTION'
  | 'COMPOUND_UNSUPPORTED'
  | 'AMBIGUOUS'
  | 'UNSUPPORTED_STRUCTURE'
  | 'UNSUPPORTED_OPERATION'
  | 'IDENTIFIED_UNSUPPORTED';

export interface ResolutionResult {
  code: ResolutionCode;
  moduleId?: string;
  moduleName?: string;
  message: string;
  spec: ProblemSpecV1;
  generationMode?: 'single' | 'menu';
  operations?: string[];
}

export interface ProblemUnderstanding {
  problemType: string;
  entities: Record<string, unknown>;
  constraints: Record<string, unknown>;
  objectives: Record<string, unknown>;
  inputModel: Record<string, unknown>;
  outputModel: Record<string, unknown>;
  candidatePatterns: string[];
  selectedStrategy?: string;
  complexityTarget?: string;
}
