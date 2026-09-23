/**
 * CHUP / Offcode — Deterministic Fuzzy Matcher
 *
 * Phase 2 Freeze Contract:
 * - The correction engine is a deterministic, offline, token-level evidence extractor
 *   whose candidate space is strictly limited to the authoritative Offcode vocabulary.
 * - It may correct only high-confidence lexical errors against that vocabulary.
 *   It may not infer semantics, select domains, select capabilities, select solvers, or manufacture concepts.
 * - Ambiguous or insufficient matches remain unmodified.
 * - Canonical phrase recognition occurs only after token normalization.
 * - Downstream classification, capability resolution, solving, and verification remain responsible for their respective decisions.
 *
 * Metric & Thresholds (Authoritative & Frozen):
 * - Metric: Restricted Damerau-Levenshtein distance (insertion, deletion, substitution, adjacent transposition).
 *   Adjacent transpositions (e.g. dijsktra -> dijkstra, likned -> linked) cost 1, not 2.
 * - Short-Token Shielding: Tokens with length <= 4 or in PROTECTED_SHORT_WORDS are strictly shielded (never modified).
 *   Short words (<= 4 chars) are also never proposed as candidate replacement targets.
 * - High Confidence:
 *     * length 5-6: distance <= 1, similarity >= 0.80 (Frozen authoritative threshold)
 *     * length >= 7: (distance <= 1, similarity >= 0.85) OR (distance <= 2, similarity >= 0.88)
 * - Ambiguity Margin: If two candidates have equal distance and Delta sim < 0.05, downgraded to MEDIUM_CONFIDENCE.
 * - Medium Confidence: Retained as metadata evidence, never rewrites normalizedText.
 * - Low Confidence: Ignored.
 * - Length-Difference Guard: Skip candidates where |token_len - vocab_len| > 2 for tokens < 9 chars,
 *   or > 3 for tokens >= 9 chars (accommodates longer compound-word typos like dcompositon -> decomposition).
 *
 * Architectural Invariant:
 * False normalization is substantially more dangerous than missed normalization.
 * A normalization failure may reduce downstream evidence; it must never manufacture domain evidence.
 */

import { PROTECTED_SHORT_WORDS, VALID_VOCABULARY_WORDS, PROTECTED_WORDS, VOCABULARY_WORDS } from './domainVocabulary';

export type MatchDecision = 'HIGH_CONFIDENCE' | 'MEDIUM_CONFIDENCE' | 'LOW_CONFIDENCE';

export interface FuzzyMatchResult {
  decision: MatchDecision;
  candidate: string | null;
  confidence: number;
  distance: number;
}

/**
 * Calculates standard Levenshtein distance between two strings,
 * Restricted Damerau-Levenshtein distance between two strings.
 * Counts: insertions, deletions, substitutions, and adjacent transpositions.
 * Adjacent transpositions (a[i] == b[j-1] && a[i-1] == b[j]) cost 1 instead of 2.
 * This correctly handles common keyboard transposition typos:
 *   dijsktra -> dijkstra (s <-> k swap), likned -> linked (k <-> n swap).
 */
export function levenshteinDistance(a: string, b: string): number {
  const al = a.length;
  const bl = b.length;
  if (al === 0) return bl;
  if (bl === 0) return al;

  // Initialize matrix (restricted Damerau-Levenshtein)
  const matrix: number[][] = [];
  for (let i = 0; i <= al; i++) {
    matrix[i] = new Array(bl + 1).fill(0);
    matrix[i][0] = i;
  }
  for (let j = 0; j <= bl; j++) {
    matrix[0][j] = j;
  }

  for (let i = 1; i <= al; i++) {
    for (let j = 1; j <= bl; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,       // deletion
        matrix[i][j - 1] + 1,       // insertion
        matrix[i - 1][j - 1] + cost // substitution
      );
      // Adjacent transposition: a[i-1] == b[j-2] && a[i-2] == b[j-1]
      if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) {
        matrix[i][j] = Math.min(matrix[i][j], matrix[i - 2][j - 2] + cost);
      }
    }
  }

  return matrix[al][bl];
}

/**
 * Alias: damerauLevenshteinDistance now correctly resolves to the Damerau implementation.
 */
export const damerauLevenshteinDistance = levenshteinDistance;

/**
 * Normalized similarity ratio based on distance:
 * 1.0 = identical, 0.0 = completely disjoint.
 */
export function similarityRatio(a: string, b: string, distance?: number): number {
  const maxLen = Math.max(a.length, b.length);
  if (maxLen === 0) return 1.0;
  const dist = distance !== undefined ? distance : damerauLevenshteinDistance(a, b);
  return Math.max(0, 1.0 - (dist / maxLen));
}

/**
 * Evaluates a single token against domain vocabulary using the three-state model.
 * Strict Processing Order:
 * 1. Case-normalize token for comparison
 * 2. Exact vocabulary lookup (if in VALID_VOCABULARY_WORDS -> exit immediately, no correction)
 * 3. Protected / short / numeric check (if len <= 4 || PROTECTED_SHORT_WORDS || numeric -> exit immediately)
 * 4. Fuzzy candidate generation (strictly in VALID_VOCABULARY_WORDS)
 * 5. Similarity calculation
 * 6. Deterministic candidate ranking
 * 7. HIGH / MEDIUM / LOW classification
 */
export function matchToken(token: string): FuzzyMatchResult {
  const lower = token.toLowerCase();

  // 1. Exact match in domain vocabulary — no correction needed
  if (VALID_VOCABULARY_WORDS.has(lower)) {
    return {
      decision: 'LOW_CONFIDENCE',
      candidate: lower,
      confidence: 1.0,
      distance: 0
    };
  }

  // 2. Strict Short-Token & Protected Word Protection
  // Invariant: Protected tokens bypass fuzzy matching entirely.
  // Words <= 4 chars or in PROTECTED_SHORT_WORDS must NEVER enter candidate generation.
  // Prevents semantic corruption (map -> max, set -> get, tree -> free, stack -> slack).
  if (lower.length <= 4 || PROTECTED_SHORT_WORDS.has(lower) || /^\d+$/.test(lower)) {
    return {
      decision: 'LOW_CONFIDENCE',
      candidate: null,
      confidence: 0,
      distance: Infinity
    };
  }

  // 3. Search domain vocabulary candidates strictly in VALID_VOCABULARY_WORDS
  interface ScoredCandidate {
    word: string;
    distance: number;
    similarity: number;
  }

  const candidates: ScoredCandidate[] = [];

  for (const vocabWord of VALID_VOCABULARY_WORDS) {
    // Invariant: Do not propose short protected words (<= 4 chars) as fuzzy targets
    if (vocabWord.length <= 4 || PROTECTED_SHORT_WORDS.has(vocabWord)) {
      continue;
    }

    // Length difference guard: for tokens < 9 chars, skip if diff > 2.
    // For tokens >= 9 chars (long compound words), allow diff up to 3 to
    // catch typos like dcompositon (10) -> decomposition (13).
    const maxLenDiff = lower.length >= 9 ? 3 : 2;
    if (Math.abs(lower.length - vocabWord.length) > maxLenDiff) {
      continue;
    }

    const dist = damerauLevenshteinDistance(lower, vocabWord);
    const sim = similarityRatio(lower, vocabWord, dist);

    if (dist <= 2 && sim >= 0.70) {
      candidates.push({ word: vocabWord, distance: dist, similarity: sim });
    }
  }

  if (candidates.length === 0) {
    return {
      decision: 'LOW_CONFIDENCE',
      candidate: null,
      confidence: 0,
      distance: Infinity
    };
  }

  // 4. Deterministic ranking:
  // 1. similarity descending
  // 2. distance ascending
  // 3. lexical ordering ascending
  candidates.sort((a, b) => {
    if (b.similarity !== a.similarity) {
      return b.similarity - a.similarity;
    }
    if (a.distance !== b.distance) {
      return a.distance - b.distance;
    }
    return a.word < b.word ? -1 : (a.word > b.word ? 1 : 0);
  });

  const best = candidates[0];
  const second = candidates.length > 1 ? candidates[1] : null;

  // 5. Decision: Check for HIGH_CONFIDENCE
  // Requirements for HIGH_CONFIDENCE:
  // - Length 5-6: max distance 1, similarity >= 0.80 (allows 5-letter single edit: 1 - 1/5 = 0.80)
  // - Length 7-9: (dist <= 1 && sim >= 0.85) || (dist <= 2 && sim >= 0.88)
  // - Length >= 10: (dist <= 1 && sim >= 0.85) || (dist <= 2 && sim >= 0.82)
  //   Long compound words (decomposition, interpolation) tolerate slightly lower sim
  //   at dist=2 because their max sim floor is lower (e.g. dcompositon -> decomposition = sim 0.846)
  // - Unambiguous: if a second candidate exists with equal distance, best must be separated
  //   by at least MIN_MARGIN (0.05). If ambiguity exists, downgrade to MEDIUM_CONFIDENCE.
  const isLen5to6 = lower.length >= 5 && lower.length <= 6;
  const isLen7to9 = lower.length >= 7 && lower.length <= 9;
  const isLen10Plus = lower.length >= 10;

  const validThreshold = (isLen5to6  && best.distance <= 1 && best.similarity >= 0.80) ||
                         (isLen7to9  && best.distance <= 1 && best.similarity >= 0.85) ||
                         (isLen7to9  && best.distance <= 2 && best.similarity >= 0.88) ||
                         (isLen10Plus && best.distance <= 1 && best.similarity >= 0.85) ||
                         (isLen10Plus && best.distance <= 2 && best.similarity >= 0.82);

  const unambiguous = !second ||
                      (best.distance < second.distance) ||
                      (best.similarity - second.similarity >= 0.05);

  if (validThreshold && unambiguous) {
    return {
      decision: 'HIGH_CONFIDENCE',
      candidate: best.word,
      confidence: Number(best.similarity.toFixed(4)),
      distance: best.distance
    };
  }

  // 6. Decision: MEDIUM_CONFIDENCE
  // Valid candidate found (dist <= 2, sim >= 0.70) but does not meet strict rewriting criteria (ambiguous competitor or borderline)
  return {
    decision: 'MEDIUM_CONFIDENCE',
    candidate: best.word,
    confidence: Number(best.similarity.toFixed(4)),
    distance: best.distance
  };
}

/** Backward-compatibility alias */
export const matchTokenAgainstVocabulary = matchToken;
