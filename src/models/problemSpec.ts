import { ExplanationDocument } from './explanationModel';

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

// ═══════════════════════════════════════════════════════════════════════════════
// CHUP V2 Types — Universal Problem-Solving System
// All V1 types above remain untouched.
// ═══════════════════════════════════════════════════════════════════════════════

export type ProblemType = 'competitive_programming' | 'academic' | 'code_debug' | 'template_match';
export type DifficultyLevel = 'basic' | 'intermediate' | 'advanced' | 'expert';
export type ComplexityClass = 'O(1)' | 'O(log N)' | 'O(N)' | 'O(N log N)' | 'O(N sqrt N)' | 'O(N²)' | 'O(N³)' | 'O(2^N)' | 'O(N!)';
export type FailureType = 'compilation_error' | 'runtime_error' | 'wrong_answer' | 'tle' | 'mle';
export type CauseCategory = 'code_level' | 'template_parameter' | 'algorithm';
export type CorrectionLevel = 1 | 2 | 3;

export type ConceptCategory =
  | 'container'
  | 'adapter'
  | 'algorithm'
  | 'utility'
  | 'iterator'
  | 'manual'
  | 'technique';

export interface ConceptComplexity {
  time: string;
  space: string;
  averageTime?: string;
  worstTime?: string;
  operations?: Record<string, string>;
}

/** Semantic operations that can be required by a problem. */
export type RequiredOperation =
  | 'sorting'
  | 'range_sum'
  | 'subarray_target_sum'
  | 'subarray_window_opt'
  | 'pair_sum'
  | 'element_lookup'
  | 'threshold_search'
  | 'shortest_path'
  | 'connectivity'
  | 'interval_schedule'
  | 'frequency_count'
  | 'recurrence_1d'
  | 'filter_count'
  | 'dynamic_range_min_query'
  | 'uniqueness'
  | 'sorted_order'
  | 'duplicate_detection'
  | 'duplicate_preservation'
  | 'fast_membership'
  | 'ordered_frequency_output'
  | 'key_value_mapping'
  | 'fifo'
  | 'lifo'
  | 'maximum_retrieval'
  | 'minimum_retrieval'
  | 'ordered_lookup'
  | 'dynamic_insertion'
  | 'dynamic_deletion'
  | 'double_ended_access'
  | 'random_access'
  | 'sequence_io'
  | 'reversal'
  | 'registration_system'
  | 'dynamic_array_operations'
  | 'deque_operations'
  | 'notification_queue'
  | 'queue_simulation'
  | 'team_queue'
  | 'nearest_smaller_values'
  | 'monotonic_stack'
  | 'balanced_brackets'
  | 'bracket_sequence_min_cost'
  | 'priority_queue_operations'
  | 'multi_priority_queue'
  | 'priority_queue_halving'
  | 'interval_partitioning'
  | 'card_war_simulation'
  | 'distinct_count'
  | 'reversible_deque'
  | 'multiset_operations'
  | 'arithmetic_gap'
  | 'lis_dp'
  | 'pair_sum_positions'
  | 'container_most_water'
  | 'palindrome_check'
  | 'in_place_compaction'
  | 'remove_duplicates_sorted'
  | 'sliding_window_fixed'
  | 'sliding_window_variable_min'
  | 'sliding_window_variable_max'
  | 'partition_dutch_flag'
  | 'partition_two_way'
  | 'linked_cycle_detection'
  | 'linked_middle_node'
  | 'prefix_tree'
  | 'trie_prefix_search'
  | 'lru_cache'
  | 'lfu_cache'
  | 'tree_dp'
  | 'histogram'
  | 'next_greater'
  | 'daily_temperatures'
  | 'stock_span';

export interface PointerReasoningResult {
  status: 'success' | 'rejected' | 'error';
  domain: string;
  selectedPattern: string | null;
  family: string | null;
  preconditionEvidence?: string;
  monotonicity?: {
    kind: string;
    status: string;
    property: string;
    justification: string;
  };
  invariant?: {
    before: string;
    during: string;
    after: string;
    termination: string;
  };
  movement?: {
    objective: string;
    decisions: Record<string, string>;
    eliminationProof: string;
  };
  eliminatedCandidates?: Array<{
    candidate: string;
    family: string;
    rejectionCode: string;
    evidence: string;
    preconditionTested: string;
    recommendedAlternative?: string;
  }>;
  code?: string;
  reasoning: string;
  ruleInduced?: Record<string, unknown>;
  promotionMessage?: string;
  recommendedAlternative?: string;
  explanation?: ExplanationDocument;
}

/** A formal concept definition in the unified program synthesis architecture. */
export interface KnowledgeConcept {
  id: string;
  name: string;
  category: ConceptCategory;
  cppType?: string;
  properties: string[];
  satisfies: RequiredOperation[];
  requires: string[];   // Preconditions (SemanticConceptState), e.g. ['sequence']
  produces: string[];   // Effects (SemanticConceptState), e.g. ['sorted_sequence']
  dataStructures: string[];
  supportedOperations?: string[];
  complexity?: ConceptComplexity;
  headers?: string[];
  isSTL?: boolean;
  variant?: string;
  templateId?: string;
}

/** Backward-compatible alias for AlgorithmConcept. */
export type AlgorithmConcept = KnowledgeConcept;

/** A single step in an assembled strategy pipeline. */
export interface StrategyStep {
  conceptId: string;
  satisfies: RequiredOperation[];
  produces: string[];
}

/** Structured diagnostic trace describing genuine decisions made during evaluation. */
export interface DiagnosticTraceEntry {
  requirement: string;
  candidate: string;
  accepted: boolean;
  reason: string;
  requiredStates?: string[];
  availableStates?: string[];
  producedStates?: string[];
  complexityAssessment?: string;
}

/** Complete strategy plan produced by single evaluation or composition engine. */
export interface StrategyPlan {
  mode: 'single' | 'composed' | 'compound_unsupported' | 'unrecognized';
  steps: StrategyStep[];
  initialStates: string[];
  finalStates: string[];
  coveredOperations: RequiredOperation[];
  uncoveredOperations: RequiredOperation[];
  reasoning: string;
  diagnosticTrace?: DiagnosticTraceEntry[];
}

/** Problem requirements extracted from natural language and structure. */
export interface ProblemRequirements {
  dataStructure: 'sequence_static' | 'sequence_dynamic' | 'graph_unweighted' | 'graph_weighted' | 'grid' | 'intervals' | 'general';
  operations: RequiredOperation[];
  allowsNegativeValues: boolean;
  hasRepeatedQueries: boolean;
  requiresSorted: boolean;
  isCompoundCandidate: boolean;
  explanation: string;
  implementationConstraint?: 'auto' | 'stl' | 'manual' | 'manual_array' | 'manual_linked_list';
}

/** A single test case parsed from the problem statement or generated. */
export interface TestCase {
  input: string;
  expectedOutput: string;
  label?: string;
}

/** A numeric constraint extracted from the problem text. */
export interface ParsedConstraint {
  variable: string;       // e.g. "N", "M", "a_i"
  upperBound: number;
  lowerBound?: number;
  raw: string;            // original text that was parsed
}

/** Feasibility estimation for each complexity class. */
export interface FeasibilityEstimate {
  constraints: ParsedConstraint[];
  timeLimit: number | null;           // seconds
  testCases: number | null;           // T
  memoryLimit: number | null;         // MB
  feasible: ComplexityClass[];
  marginal: ComplexityClass[];
  likelyInfeasible: ComplexityClass[];
  overflowRisk: boolean;
  reasoning: string;
}

/** A candidate DSA concept detected in the problem, with confidence. */
export interface TopicCandidate {
  conceptId: string;
  confidence: number;         // 0.0 to 1.0
  matchedPatterns: string[];
  supported: boolean;         // has solution template?
  rejected?: boolean;         // demoted by anti-pattern/condition?
  rejectionReason?: string;
}

/** Structured normalized token preserving index and original text provenance. */
export interface NormalizedToken {
  index: number;
  text: string;
  originalText: string;
  corrected: boolean;
}

/** Explicit linguistic correction applied during universal normalization. */
export interface InputCorrection {
  original: string;
  corrected: string;
  confidence: number;
  startToken: number; // inclusive
  endToken: number;   // exclusive
}

/** Structured canonical term representation preserving provenance and token spans. */
export interface CanonicalTerm {
  canonical: string;
  surfaceForm: string;
  confidence: number;
  startToken: number; // inclusive
  endToken: number;   // exclusive
}

/** Universal Input Normalization Contract across all Offcode domains. */
export interface NormalizedInput {
  originalText: string;
  normalizedText: string;
  corrections: InputCorrection[];
  tokens: string[];
  canonicalTerms: CanonicalTerm[];
  normalizationConfidence: number;
}

/** Canonicalized input stage separating phrase recognition from lexical normalization. */
export interface CanonicalizedInput {
  normalizedInput: NormalizedInput;
  tokens: NormalizedToken[];
  canonicalTerms: CanonicalTerm[];
  canonicalizationConfidence: number;
}

/** Entity classification categories. */
export type EntityKind =
  | 'data_structure'
  | 'algorithm'
  | 'numerical_method'
  | 'linear_algebra_concept'
  | 'mathematical_object'
  | 'unknown';

/** Entity evidence extracted from canonical terms and vocabulary. */
export interface EntityEvidence {
  kind: EntityKind;
  value: string;
  sourceTokens: number[];
  startToken: number; // inclusive
  endToken: number;   // exclusive
  confidence: number;
}

/** Operation evidence representing explicit computational actions requested. */
export interface OperationEvidence {
  operation: string;
  sourceTokens: number[];
  startToken: number;
  endToken: number;
  confidence: number;
}

/** Intent evidence representing what the user asks to do. */
export interface IntentEvidence {
  intent: string;
  sourceTokens: number[];
  startToken: number;
  endToken: number;
  confidence: number;
}

/** Constraint evidence representing explicit operational conditions. */
export interface ConstraintEvidence {
  type: 'position' | 'ordering' | 'direction' | 'range' | 'value' | 'key' | 'size' | 'unknown';
  value: string;
  sourceTokens: number[];
  startToken: number;
  endToken: number;
  confidence: number;
}

/** Explicit intermediate semantic representation of user input. */
export interface SemanticInput {
  originalText: string;
  normalizedText: string;
  tokens: NormalizedToken[];
  corrections: InputCorrection[];
  canonicalTerms: CanonicalTerm[];
  entities: EntityEvidence[];
  operations: OperationEvidence[];
  intents: IntentEvidence[];
  constraints: ConstraintEvidence[];
  normalizationConfidence: number;
  extractionConfidence: number;
}

/** Reference to structured evidence piece for capability matching. */
export interface EvidenceRef {
  kind: 'entity' | 'operation' | 'intent' | 'constraint';
  type?: string;
  value: string;
}

/** Structured evidence predicate for capability definition requirements. */
export interface EvidencePredicate {
  kind: 'entity' | 'operation' | 'intent' | 'constraint';
  type?: string;
  value: string | string[];          // scalar or OR-alternatives (e.g. ['head', 'beginning'])
  role?: 'primary' | 'contextual';   // for role-based contradiction evaluation
  negated?: boolean;
}

/** Tri-state capability match evaluation status. */
export type CapabilityMatchStatus = 'eligible' | 'disqualified' | 'insufficient';

/** Scored capability candidate with explicit positive, negative, and missing evidence. */
export interface CapabilityScore {
  capability: string;
  domain: ProblemType;
  status: CapabilityMatchStatus;
  positiveEvidence: EvidenceRef[];
  negativeEvidence: EvidenceRef[];
  missingEvidence: EvidenceRef[];
  score: number;
}

/** Domain classification status preventing false CP conflation. */
export type ClassificationStatus = 'classified' | 'ambiguous' | 'unsupported';

/** Confidence-scored problem classification. */
export interface ClassificationResult {
  status: ClassificationStatus;
  scores: {
    competitive_programming: number;
    template_match: number;
    academic: number;
    code_debug: number;
  };
  selected: ProblemType | null;
  confidence: number;
  signals: string[];
}

/** The v2 structured problem representation. */
export interface StructuredProblem {
  rawText: string;
  normalizedText: string;
  normalizedInput?: NormalizedInput;
  canonicalizedInput?: CanonicalizedInput;
  semanticInput?: SemanticInput;
  capabilityScores?: CapabilityScore[];
  title: string | null;
  problemType: ProblemType | null;
  domain: string | null;
  statement: string;
  inputSpecification: string | null;
  outputSpecification: string | null;
  constraints: ParsedConstraint[];
  examples: TestCase[];
  notes: string | null;
  timeLimit: number | null;           // seconds
  memoryLimit: number | null;         // MB
  source: string | null;             // "codeforces", "generic", etc.
  parserConfidence: number;
}

/** Result of running a single test case. */
export interface TestCaseResult {
  testCase: TestCase;
  actualOutput: string;
  passed: boolean;
  timedOut: boolean;
  runtimeError: boolean;
  exitCode: number;
}

/** Full verification result. */
export interface VerificationResult {
  compiled: boolean;
  compilationErrors: string[];
  testResults: TestCaseResult[];
  allPassed: boolean;
  failureType: FailureType | null;
  summary: string;
}

/** Diagnosis of why a solution failed. */
export interface FailureDiagnosis {
  failureType: FailureType;
  causeCategory: CauseCategory;
  description: string;
  suggestedFix: string;
  correctionLevel: CorrectionLevel;
}

/** Record of a single correction attempt. */
export interface CorrectionAttempt {
  attempt: number;
  diagnosis: FailureDiagnosis;
  fixApplied: string;
  result: VerificationResult;
}

/** The output of any v2 solver. */
export interface SolverResult {
  success: boolean;
  problemType: ProblemType;
  approach: string;                     // human-readable approach description
  detectedTopics: TopicCandidate[];
  feasibility: FeasibilityEstimate | null;
  selectedAlgorithm: string | null;
  code: string;
  reasoning: string;
  verification: VerificationResult | null;
  correctionHistory: CorrectionAttempt[];
  limitationMessage: string | null;     // non-null when recognized-only
  diagnosticTrace?: DiagnosticTraceEntry[];
  explanation?: ExplanationDocument;
}
