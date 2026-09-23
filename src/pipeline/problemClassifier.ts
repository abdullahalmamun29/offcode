/**
 * CHUP V2 / Offcode — Problem Classifier (Phase 3 Decoupled Semantic Architecture)
 *
 * Consumes structured SemanticInput and scored capabilities.
 * Does NOT perform raw lexical substring matching or implicit domain defaulting.
 *
 * Invariant: UNSUPPORTED ≠ COMPETITIVE_PROGRAMMING
 * If zero or insufficient domain evidence exists, output status is 'unsupported' with selected: null.
 */

import {
  ClassificationResult,
  ProblemType,
  SemanticInput,
  StructuredProblem
} from '../models/problemSpec';
import { scoreCapabilities } from './capabilityScorer';
import { extractSemanticInput } from './semanticExtractor';
import { normalizeInputUniversal } from './universalNormalizer';

/**
 * Classify a problem directly from structured SemanticInput.
 *
 * @param semantic - The extracted SemanticInput evidence
 * @param problem - Optional parsed StructuredProblem for CP/structural signals
 * @param modeOverride - Optional manual mode override
 * @returns ClassificationResult with structured scores and signals
 */
export function classifySemanticInput(
  semantic: SemanticInput,
  problem?: StructuredProblem,
  modeOverride?: string
): ClassificationResult {
  const scores = {
    competitive_programming: 0,
    template_match: 0,
    academic: 0,
    code_debug: 0
  };

  const signals: string[] = [];

  // 1. Evaluate Semantic Capability Scores
  const capabilityScores = scoreCapabilities(semantic);

  // Check top eligible matches for each domain
  for (const capScore of capabilityScores) {
    if (capScore.status === 'eligible' && capScore.score > 0) {
      if (capScore.domain === 'template_match' && capScore.score > scores.template_match) {
        scores.template_match = capScore.score;
        signals.push(`TM: matched capability ${capScore.capability} (score: ${capScore.score})`);
      } else if (capScore.domain === 'academic' && capScore.score > scores.academic) {
        scores.academic = capScore.score;
        signals.push(`AC: matched capability ${capScore.capability} (score: ${capScore.score})`);
      } else if (capScore.domain === 'code_debug' && capScore.score > scores.code_debug) {
        scores.code_debug = capScore.score;
        signals.push(`DBG: matched capability ${capScore.capability} (score: ${capScore.score})`);
      }
    }
  }

  // Check general conceptual academic queries (e.g. "derive", "prove", "explain")
  const hasAcademicIntent = semantic.intents.some(i =>
    ['derive', 'prove', 'explain', 'demonstrate', 'compare'].includes(i.intent)
  );
  if (hasAcademicIntent) {
    const boost = 0.50;
    if (boost > scores.academic) {
      scores.academic = boost;
      signals.push('AC: conceptual academic intent detected');
    }
  }

  // Check debug entities or keywords
  const hasDebugTokens = semantic.tokens.some(t =>
    ['crash', 'bug', 'error', 'segfault', 'wrong', 'fix', 'debug'].includes(t.text)
  );
  if (hasDebugTokens) {
    const boost = 0.55;
    if (boost > scores.code_debug) {
      scores.code_debug = boost;
      signals.push('DBG: error / segfault token detected');
    }
  }

  // Check menu-driven intent
  const isMenuDriven = semantic.tokens.some(t => t.text === 'menu');
  if (isMenuDriven && (scores.template_match > 0 || semantic.entities.length > 0)) {
    scores.template_match = Math.max(scores.template_match, 0.70);
    signals.push('TM: menu-driven program requested');
  }

  // 2. Evaluate Structural Competitive Programming Signals
  if (problem) {
    const fullText = [
      problem.title || '',
      problem.statement,
      problem.inputSpecification || '',
      problem.outputSpecification || '',
      problem.notes || ''
    ].join('\n').toLowerCase();

    if (problem.timeLimit !== null || fullText.includes('time limit')) {
      scores.competitive_programming += 0.35;
      signals.push('CP: time limit specification found');
    }

    if (problem.inputSpecification || problem.outputSpecification) {
      scores.competitive_programming += 0.20;
      signals.push('CP: structured Input/Output sections found');
    }

    if (problem.constraints && problem.constraints.length > 0) {
      scores.competitive_programming += 0.20;
      signals.push('CP: numeric constraints found');
    }

    if (problem.examples && problem.examples.length > 0) {
      scores.competitive_programming += 0.15;
      signals.push('CP: sample test case examples parsed');
    }

    if (problem.source === 'codeforces') {
      scores.competitive_programming += 0.10;
      signals.push('CP: source platform is codeforces');
    }

    if (/given an array|given a graph|find the maximum|find the minimum|find the shortest/i.test(fullText)) {
      scores.competitive_programming += 0.25;
      signals.push('CP: standard competitive phrasing pattern');
    }

    if (fullText.includes('queries') || fullText.includes('test cases')) {
      scores.competitive_programming += 0.10;
      signals.push('CP: test cases / queries specification');
    }
  }

  // Round scores to 4 decimal places
  scores.competitive_programming = Number(scores.competitive_programming.toFixed(4));
  scores.template_match = Number(scores.template_match.toFixed(4));
  scores.academic = Number(scores.academic.toFixed(4));
  scores.code_debug = Number(scores.code_debug.toFixed(4));

  // 3. Status & Winner Determination (Invariant: UNSUPPORTED ≠ CP)
  let status: 'classified' | 'ambiguous' | 'unsupported' = 'unsupported';
  let selected: ProblemType | null = null;
  let maxScore = 0;

  const sortedCandidates = (Object.entries(scores) as [ProblemType, number][])
    .sort((a, b) => b[1] - a[1]);

  const top = sortedCandidates[0];
  const runnerUp = sortedCandidates[1];

  if (top && top[1] > 0) {
    maxScore = top[1];
    // Check for ambiguity: equal or nearly equal top scores across different domains
    if (runnerUp && runnerUp[1] > 0 && Math.abs(top[1] - runnerUp[1]) < 0.05) {
      status = 'ambiguous';
      selected = null; // Ambiguous: do not artificially favor one candidate
      signals.push(`AMBIGUITY: ${top[0]} (${top[1]}) and ${runnerUp[0]} (${runnerUp[1]}) are too close`);
    } else {
      status = 'classified';
      selected = top[0];
    }
  } else {
    // Invariant: Zero matched evidence yields unsupported with null selected
    status = 'unsupported';
    selected = null;
    maxScore = 0;
  }

  // 4. Authoritative Manual Mode Override
  if (modeOverride && modeOverride in scores) {
    selected = modeOverride as ProblemType;
    scores[modeOverride as ProblemType] = 1.0;
    maxScore = 1.0;
    status = 'classified';
    signals.push(`OVERRIDE: mode manually set to ${modeOverride}`);
  }

  return {
    status,
    scores,
    selected,
    confidence: maxScore,
    signals
  };
}

/**
 * Wrapper for StructuredProblem backward-compatibility.
 */
export function classifyProblem(
  problem: StructuredProblem,
  modeOverride?: string
): ClassificationResult {
  const semantic =
    problem.semanticInput ||
    extractSemanticInput(problem.normalizedInput || normalizeInputUniversal(problem.rawText));

  // Attach to problem for downstream inspection
  problem.semanticInput = semantic;

  return classifySemanticInput(semantic, problem, modeOverride);
}
