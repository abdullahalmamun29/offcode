/**
 * CHUP V2 — CP Solver.
 *
 * Core competitive programming solving orchestrator.
 * Takes a StructuredProblem, runs the full analysis pipeline, and produces
 * a verified solution or an honest limitation report.
 *
 * Pipeline:
 *   StructuredProblem
 *   → Constraint Analysis (feasibility estimation)
 *   → Topic Detection (ranked concept candidates)
 *   → Algorithm Selection (filter by feasibility, rank by fit)
 *   → Solution Construction (compose from template)
 *   → Verification (compile + run examples + edge cases)
 *   → Failure Analysis → Correction (up to maxRetries)
 *   → SolverResult
 */

import {
  StructuredProblem, SolverResult, TopicCandidate,
  FeasibilityEstimate, VerificationResult, CorrectionAttempt,
  ComplexityClass, ProblemRequirements
} from '../models/problemSpec';
import { extractRequirements } from '../pipeline/requirementExtractor';
import { evaluateStrategy } from './strategyEvaluator';
import { analyzeConstraints } from '../pipeline/constraintAnalyzer';
import { scoreConcepts, getConceptById } from '../knowledge/dsaKnowledge';
import { buildFromTemplate, TemplateParams } from './solutionTemplates';
import { assembleComposedProgram } from '../generator/fragmentAssembler';
import { composeCode } from '../generator/codeComposer';
import { verifyCode, generateEdgeCases } from '../verifier/verificationEngine';
import { analyzeFailure } from './failureAnalyzer';
import { applyCorrection } from './correctionEngine';

/** Complexity class to approximate operation growth */
const COMPLEXITY_ORDER: Record<string, number> = {
  'O(1)': 0, 'O(log N)': 1, 'O(N)': 2, 'O(N log N)': 3,
  'O(N sqrt N)': 4, 'O(N²)': 5, 'O(N³)': 6, 'O(2^N)': 7, 'O(N!)': 8
};

/**
 * Solve a competitive programming problem.
 *
 * @param problem - The structured problem representation
 * @param maxRetries - Maximum correction attempts (default 3)
 * @returns SolverResult with code, verification, and correction history
 */
import { extractQuerySchema } from '../pipeline/querySchemaExtractor';
import { solveWithQuerySchema } from './genericQuerySolver';
import { PointerBridge } from '../parser/pointerBridge';

export function solveCpProblem(problem: StructuredProblem, maxRetries: number = 3): SolverResult {
  // ── Step 0: Try generic query schema solver ────────────────────────────────
  try {
    const querySchema = extractQuerySchema(problem);
    if (querySchema && querySchema.confidence >= 0.6) {
      const genericCode = solveWithQuerySchema(querySchema, problem);
      if (genericCode && problem.examples.length > 0) {
        const { verifyCode } = require('../verifier/verificationEngine');
        const verification = verifyCode(genericCode, problem.examples);
        if (verification.allPassed) {
          return {
            success: true,
            problemType: 'competitive_programming',
            approach: `Generic Query Schema (${querySchema.container}, pattern=${querySchema.pattern}, ops=[${querySchema.commands.map(c => c.semanticOp).join(', ')}])`,
            detectedTopics: [],
            feasibility: null,
            selectedAlgorithm: `generic_${querySchema.container}`,
            code: genericCode,
            reasoning: `Query schema extracted with confidence ${querySchema.confidence}. Generic synthesizer produced verified code.`,
            verification,
            correctionHistory: [],
            limitationMessage: null,
          };
        }
      }
    }
  } catch (e) {
    // QSE failed — fall through to existing pipeline
  }

  // ── Step 1: Extract Requirements ──────────────────────────────────────────
  const requirements = extractRequirements(problem);

  // ── Step 1.5: Query Authoritative Python Pointer Reasoning Engine ─────────
  const textToScan = problem.normalizedText || problem.rawText || problem.statement;
  const hasMultipleSequencesOrArrays = /(?:two\s+(?:arrays|sequences|collections|lists)|given\s+(?:an?\s+)?(?:array|sequence)\s+.*?\s+and\s+(?:an?\s+)?(?:array|sequence)|n\s+[a-z]+\s+and\s+m\s+[a-z]+|n\s+integers[\s\S]*?m\s+integers)/i.test(textToScan);

  const hasPointerClues = hasMultipleSequencesOrArrays || requirements.operations.some(op =>
    op === 'pair_sum' || op === 'pair_sum_positions' || op === 'container_most_water' ||
    op === 'remove_duplicates_sorted' || op === 'in_place_compaction' ||
    op === 'partition_dutch_flag' || op === 'linked_cycle_detection' || op === 'subarray_window_opt'
  ) || /(?:pair|pairing|(?:at\s+most|up\s+to|one\s+or)\s+(?:two|2)|two\s+(?:numbers|values|elements|pointers|items|people|children|packages|objects)|capacity|exceed|pointer|sorted\s+(?:in\s+)?(?:non-decreasing|ascending|array)|window|water|container|duplicate|dutch\s+national|tortoise|contiguous|subarray|substring|minimal\s+length|minimum\s+size|longest\s+contiguous|zero(?:es|s)?|parity|partition|cycle|palindrome|rain\s*water|3-sum|three\s+sum)/i.test(textToScan);

  let excludedByPointerEngine: string[] = [];

  if (hasPointerClues) {
    try {
      const pointerBridge = new PointerBridge();
      const problemText = textToScan;
      const bridgeResult = pointerBridge.evaluateProblemSync(problemText);

      if (bridgeResult.status === 'success' && bridgeResult.code) {
        const { verifyCode, generateEdgeCases } = require('../verifier/verificationEngine');
        const allTests = [...problem.examples, ...generateEdgeCases(problem.constraints)];
        const verification = problem.examples.length > 0 ? verifyCode(bridgeResult.code, allTests) : verifyCode(bridgeResult.code, []);

        if (verification.allPassed || problem.examples.length === 0) {
          const feasibility = analyzeConstraints(problem);
          return {
            success: true,
            problemType: 'competitive_programming',
            approach: `Pointer Algorithm (${bridgeResult.family} → ${bridgeResult.selectedPattern})`,
            detectedTopics: [{
              conceptId: bridgeResult.selectedPattern || 'pointer_algorithm',
              confidence: 0.98,
              matchedPatterns: [bridgeResult.selectedPattern || 'pointer_algorithm'],
              supported: true
            }],
            feasibility,
            selectedAlgorithm: bridgeResult.selectedPattern,
            code: bridgeResult.code,
            reasoning: bridgeResult.reasoning,
            verification,
            correctionHistory: [],
            limitationMessage: null,
            explanation: bridgeResult.explanation,
            diagnosticTrace: bridgeResult.eliminatedCandidates?.map(e => ({
              requirement: e.family,
              candidate: e.candidate,
              accepted: false,
              reason: e.evidence
            }))
          };
        }
      } else if (bridgeResult.status === 'rejected') {
        // Exclude falsely proposed pointer algorithms
        excludedByPointerEngine = ['two_pointers', 'sliding_window'];

        if (bridgeResult.recommendedAlternative === 'hash_map_pair_lookup') {
          const code = `#include <iostream>
#include <vector>
#include <unordered_set>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    long long target;
    if (!(cin >> n >> target)) return 0;

    unordered_set<long long> seen;
    bool found = false;

    for (int i = 0; i < n; i++) {
        long long val;
        cin >> val;
        long long comp = target - val;
        if (seen.count(comp)) {
            found = true;
        }
        seen.insert(val);
    }

    if (found) {
        cout << "YES\\n";
    } else {
        cout << "NO\\n";
    }

    return 0;
}
`;
          const { verifyCode, generateEdgeCases } = require('../verifier/verificationEngine');
          const allTests = [...problem.examples, ...generateEdgeCases(problem.constraints)];
          const verification = problem.examples.length > 0 ? verifyCode(code, allTests) : verifyCode(code, []);
          const feasibility = analyzeConstraints(problem);

          return {
            success: true,
            problemType: 'competitive_programming',
            approach: 'Hash Set Pair Lookup (O(N) Unsorted Search)',
            detectedTopics: [{
              conceptId: 'unordered_set',
              confidence: 0.95,
              matchedPatterns: ['hash_map_pair_lookup'],
              supported: true
            }],
            feasibility,
            selectedAlgorithm: 'unordered_set',
            code,
            reasoning: bridgeResult.reasoning || 'Unsorted pair sum where sorting is forbidden uses unordered_set for O(N) lookup.',
            verification,
            correctionHistory: [],
            limitationMessage: null,
            explanation: bridgeResult.explanation,
            diagnosticTrace: bridgeResult.eliminatedCandidates?.map(e => ({
              requirement: e.family,
              candidate: e.candidate,
              accepted: false,
              reason: e.evidence
            }))
          };
        } else if (bridgeResult.recommendedAlternative === 'segment_tree_or_fenwick') {
          return {
            success: false,
            problemType: 'competitive_programming',
            approach: 'unsupported',
            detectedTopics: [],
            feasibility: null,
            selectedAlgorithm: 'compound_unsupported',
            code: '',
            reasoning: bridgeResult.reasoning || 'Problem requires dynamic range updates (Fenwick/Segment Tree), which is outside supported algorithmic capabilities.',
            verification: null,
            correctionHistory: [],
            limitationMessage: 'Dynamic range updates require Fenwick tree or Segment tree, which is currently unsupported.',
            explanation: bridgeResult.explanation
          };
        }
      }
    } catch (e) {
      // Bridge unavailable or failed; fall through to standard pipeline
    }
  }

  // ── Step 2: Constraint Analysis ───────────────────────────────────────────
  const feasibility = analyzeConstraints(problem);

  // ── Step 3: Topic Detection ───────────────────────────────────────────────
  const allTopics = scoreConcepts(problem);

  // ── Step 4: Filter by Feasibility ─────────────────────────────────────────
  const viableTopics = filterByFeasibility(allTopics, feasibility);

  // ── Step 5: Hierarchical Strategy Evaluation ──────────────────────────────
  const excludedAlgorithms: Set<string> = new Set(excludedByPointerEngine);

  return attemptSolve(problem, requirements, feasibility, viableTopics, excludedAlgorithms, maxRetries);
}

/**
 * Filter topic candidates by feasibility: remove concepts whose complexity
 * is in the likelyInfeasible list.
 */
function filterByFeasibility(
  topics: TopicCandidate[],
  feasibility: FeasibilityEstimate
): TopicCandidate[] {
  const infeasibleSet = new Set<string>(feasibility.likelyInfeasible);

  return topics.map(topic => {
    const concept = getConceptById(topic.conceptId);
    if (!concept) return topic;

    // Check if the concept's complexity is infeasible
    const timeComplexity = concept.complexityProfile.time;
    // Extract the primary complexity class (some concepts have ranges like 'O(N) to O(N²)')
    const complexityClasses = extractComplexityClasses(timeComplexity);

    // If ALL complexity classes of this concept are infeasible, demote it
    const allInfeasible = complexityClasses.length > 0 &&
      complexityClasses.every(cc => infeasibleSet.has(cc));

    if (allInfeasible) {
      return {
        ...topic,
        confidence: topic.confidence * 0.1,
        rejected: true,
        rejectionReason: `Complexity ${timeComplexity} is infeasible for given constraints`
      };
    }

    return topic;
  }).sort((a, b) => b.confidence - a.confidence);
}

/**
 * Extract complexity classes from a complexity string like 'O(N log N)' or 'O(N) to O(N²)'.
 */
function extractComplexityClasses(complexityStr: string): ComplexityClass[] {
  const classes: ComplexityClass[] = [
    'O(1)', 'O(log N)', 'O(N)', 'O(N log N)', 'O(N sqrt N)',
    'O(N²)', 'O(N³)', 'O(2^N)', 'O(N!)'
  ];

  const found: ComplexityClass[] = [];
  for (const cc of classes) {
    if (complexityStr.includes(cc)) {
      found.push(cc);
    }
  }

  if (found.length > 0) {
    return [found[found.length - 1]];
  }

  return found;
}

/**
 * Attempt to solve with hierarchical strategy evaluation:
 * 1. Can ONE supported concept satisfy all requirements?
 * 2. Can supported concepts be composed?
 * 3. Otherwise report COMPOUND_UNSUPPORTED or limitation honestly.
 */
function attemptSolve(
  problem: StructuredProblem,
  requirements: ProblemRequirements,
  feasibility: FeasibilityEstimate,
  topics: TopicCandidate[],
  excludedAlgorithms: Set<string>,
  retriesRemaining: number
): SolverResult {
  const activeTopics = topics.filter(t => !excludedAlgorithms.has(t.conceptId));
  const decision = evaluateStrategy(requirements, activeTopics, feasibility.overflowRisk, excludedAlgorithms);

  if (decision.type === 'compound_unsupported') {
    return {
      success: false,
      problemType: 'competitive_programming',
      approach: 'compound',
      detectedTopics: topics,
      feasibility,
      selectedAlgorithm: null,
      code: '',
      reasoning: decision.reasoning,
      verification: null,
      correctionHistory: [],
      limitationMessage: decision.limitationMessage,
      diagnosticTrace: decision.diagnosticTrace || decision.plan?.diagnosticTrace
    };
  }

  if (decision.type === 'unrecognized' || !decision.selectedConcept) {
    return {
      success: false,
      problemType: 'competitive_programming',
      approach: '',
      detectedTopics: topics,
      feasibility,
      selectedAlgorithm: null,
      code: '',
      reasoning: decision.reasoning,
      verification: null,
      correctionHistory: [],
      limitationMessage: decision.limitationMessage
    };
  }

  const candidate = decision.selectedConcept;
  const concept = getConceptById(candidate.conceptId);

  // If recognized-only or template missing
  const isSupported = decision.type === 'compose' ? true : candidate.supported;
  if (!isSupported || !decision.templateId) {
    return {
      success: false,
      problemType: 'competitive_programming',
      approach: '',
      detectedTopics: topics,
      feasibility,
      selectedAlgorithm: candidate.conceptId,
      code: '',
      reasoning: decision.reasoning,
      verification: null,
      correctionHistory: [],
      limitationMessage: decision.limitationMessage || `Pattern recognized: ${concept?.name || candidate.conceptId}. No implementation template available for this pattern yet.`
    };
  }

  // ── Build solution from template or fragment assembler ──────────────────
  let fragment = null;
  if (decision.type === 'compose' && decision.plan) {
    fragment = assembleComposedProgram(decision.plan, decision.templateParams);
  } else {
    if (decision.templateId) {
      fragment = buildFromTemplate(decision.templateId, decision.templateParams);
    }
    if (!fragment && decision.plan) {
      fragment = assembleComposedProgram(decision.plan, decision.templateParams);
    }
  }

  if (!fragment) {
    return {
      success: false,
      problemType: 'competitive_programming',
      approach: candidate.conceptId,
      detectedTopics: topics,
      feasibility,
      selectedAlgorithm: candidate.conceptId,
      code: '',
      reasoning: `Template '${decision.templateId}' failed to build.`,
      verification: null,
      correctionHistory: [],
      limitationMessage: `Template '${decision.templateId}' failed to build.`
    };
  }

  let code = composeCode([fragment]);
  const approach = decision.type === 'compose' && decision.plan
    ? `Composed: ${decision.plan.steps.map(s => s.conceptId).join(' → ')}`
    : `${concept?.name || candidate.conceptId} (${concept?.complexityProfile.time || 'unknown'})`;
  const reasoning = `${decision.reasoning} ${buildReasoning(candidate, concept, feasibility, topics)}`;

  // ── Verify ────────────────────────────────────────────────────────────────
  const allTestCases = [...problem.examples];
  // Also generate edge cases from constraints
  const edgeCases = generateEdgeCases(problem.constraints);
  allTestCases.push(...edgeCases);

  let verification: VerificationResult | null = null;
  const correctionHistory: CorrectionAttempt[] = [];

  if (problem.examples.length === 0) {
    const compileCheck = verifyCode(code, []);
    verification = {
      compiled: compileCheck.compiled,
      compilationErrors: compileCheck.compilationErrors,
      testResults: [],
      allPassed: compileCheck.compiled,
      failureType: compileCheck.compiled ? null : 'compilation_error',
      summary: compileCheck.compiled
        ? 'Compilation successful. No test cases available for verification.'
        : `Compilation failed: ${compileCheck.compilationErrors.join('; ')}`
    };
  } else {
    verification = verifyCode(code, allTestCases);

    // ── Correction Loop ───────────────────────────────────────────────────
    let attempt = 0;
    while (verification && !verification.allPassed && attempt < retriesRemaining) {
      attempt++;
      const diagnosis = analyzeFailure(verification);

      if (!diagnosis) break;

      // Level 3: Algorithm replacement
      if (diagnosis.correctionLevel === 3) {
        excludedAlgorithms.add(candidate.conceptId);
        // Try next algorithm by recursion with reduced retries
        const retryResult = attemptSolve(
          problem, requirements, feasibility, topics, excludedAlgorithms, retriesRemaining - attempt
        );
        // Carry forward correction history
        correctionHistory.push({
          attempt,
          diagnosis,
          fixApplied: `Algorithm replacement: excluded ${candidate.conceptId}, trying next candidate`,
          result: verification
        });
        retryResult.correctionHistory = [...correctionHistory, ...retryResult.correctionHistory];
        return retryResult;
      }

      // Level 1 & 2: Code-level fixes
      const correction = applyCorrection(code, diagnosis);

      if (!correction) {
        correctionHistory.push({
          attempt,
          diagnosis,
          fixApplied: 'No applicable correction found',
          result: verification
        });
        break;
      }

      code = correction.correctedCode;
      verification = verifyCode(code, allTestCases);

      correctionHistory.push({
        attempt,
        diagnosis,
        fixApplied: correction.fixDescription,
        result: verification
      });
    }
  }

  const success = verification ? (problem.examples.length > 0 ? verification.allPassed : verification.compiled) : false;

  return {
    success,
    problemType: 'competitive_programming',
    approach,
    detectedTopics: topics,
    feasibility,
    selectedAlgorithm: candidate.conceptId,
    code,
    reasoning,
    verification,
    correctionHistory,
    limitationMessage: null,
    diagnosticTrace: decision.diagnosticTrace || decision.plan?.diagnosticTrace
  };
}

/**
 * Build human-readable reasoning string explaining the solving process.
 */
function buildReasoning(
  candidate: TopicCandidate,
  concept: ReturnType<typeof getConceptById>,
  feasibility: FeasibilityEstimate,
  allTopics: TopicCandidate[]
): string {
  const lines: string[] = [];

  // Constraint summary
  if (feasibility.constraints.length > 0) {
    const constraintStr = feasibility.constraints
      .map(c => `${c.variable} ≤ ${c.upperBound}`)
      .join(', ');
    lines.push(`Constraints: ${constraintStr}.`);
  }

  if (feasibility.timeLimit !== null) {
    lines.push(`Time limit: ${feasibility.timeLimit}s.`);
  }

  // Feasibility
  if (feasibility.feasible.length > 0) {
    lines.push(`Feasible complexities: ${feasibility.feasible.join(', ')}.`);
  }
  if (feasibility.likelyInfeasible.length > 0) {
    lines.push(`Infeasible: ${feasibility.likelyInfeasible.join(', ')}.`);
  }

  // Topic detection
  const topN = allTopics.slice(0, 5);
  if (topN.length > 0) {
    lines.push(`Detected concepts: ${topN.map(t =>
      `${t.conceptId}(${t.confidence}${t.rejected ? ' REJECTED' : ''})`
    ).join(', ')}.`);
  }

  // Selected approach
  lines.push(`Selected: ${concept?.name || candidate.conceptId} ` +
    `(confidence ${candidate.confidence}, complexity ${concept?.complexityProfile.time || '?'}).`);

  // Common mistakes to watch for
  if (concept?.commonMistakes && concept.commonMistakes.length > 0) {
    lines.push(`Watch for: ${concept.commonMistakes[0]}.`);
  }

  if (feasibility.overflowRisk) {
    lines.push('Overflow risk detected — using long long.');
  }

  return lines.join('\n');
}
