/**
 * CHUP / Offcode — Universal Input Normalizer
 *
 * Implements the Universal Input Normalization Contract.
 * Strict Architectural Separation:
 * - Normalization knows language.
 * - Normalization NEVER selects a domain.
 * - Normalization NEVER selects a solver.
 * - Normalization NEVER invokes a solver.
 * - Normalization NEVER applies concept-combination routing rules.
 * - Provenance Invariant: originalText is immutable; corrections capture forensic evidence.
 */

import { NormalizedInput, InputCorrection, CanonicalTerm } from '../models/problemSpec';
import { VALID_VOCABULARY_WORDS, PROTECTED_SHORT_WORDS } from './domainVocabulary';
import { matchToken } from './fuzzyMatcher';
import { extractCanonicalTerms } from './canonicalizer';

/**
 * Universal Input Normalization entrypoint.
 *
 * @param rawText - The un-mutated user query
 * @returns NormalizedInput contract carrying normalized text, forensic corrections,
 *          token sequence, and structured canonical terms.
 */
export function normalizeInputUniversal(rawText: string): NormalizedInput {
  const originalText = rawText;

  // 1. Initial sanitization for linguistic analysis
  // Standardize unicode quotes, dashes, non-breaking spaces, and normalize hyphens to spaces
  const sanitizedProse = rawText
    .replace(/[\u2018\u2019\u201C\u201D]/g, "'")
    .replace(/[\u2010\u2011\u2012\u2013\u2014\u2015\u2212]/g, ' ')
    .replace(/\u00A0/g, ' ')
    .replace(/[-_]/g, ' ');

  // 2. Tokenize words while stripping punctuation
  // Matches continuous alphanumeric tokens
  const rawTokenMatches = Array.from(sanitizedProse.matchAll(/[a-zA-Z0-9]+/g));
  const originalTokens = rawTokenMatches.map(m => m[0]);

  const normalizedTokens: string[] = [];
  const corrections: InputCorrection[] = [];

  // 3. Process each token for casing and high-confidence spelling correction
  for (let i = 0; i < originalTokens.length; i++) {
    const orig = originalTokens[i];
    const lower = orig.toLowerCase();

    // Check if token is already valid vocabulary or protected short word
    if (VALID_VOCABULARY_WORDS.has(lower) || PROTECTED_SHORT_WORDS.has(lower) || /^\d+$/.test(lower) || lower.length <= 4) {
      normalizedTokens.push(lower);
      continue;
    }

    // Evaluate fuzzy candidate
    const matchRes = matchToken(lower);

    if (matchRes.decision === 'HIGH_CONFIDENCE' && matchRes.candidate && matchRes.candidate !== lower) {
      // Invariant: High-confidence corrections rewrite normalizedText and record forensic evidence
      corrections.push({
        original: orig,
        corrected: matchRes.candidate,
        confidence: matchRes.confidence,
        startToken: i,     // inclusive
        endToken: i + 1    // exclusive
      });
      normalizedTokens.push(matchRes.candidate);
    } else {
      // Medium or low confidence: leave token untouched in normalizedText
      // Invariant: Medium-confidence candidates never rewrite normalizedText
      normalizedTokens.push(lower);
    }
  }

  // 4. Reconstruct normalizedText
  const normalizedText = normalizedTokens.join(' ');

  // 5. Compute normalizationConfidence
  // Deterministic multiplicative formula: product(correction_confidence_i)
  // Invariant: normalizationConfidence describes reliability of normalization only,
  // decoupled from classification or solver confidence.
  let normalizationConfidence = 1.0;
  if (corrections.length > 0) {
    normalizationConfidence = corrections.reduce((acc, c) => acc * c.confidence, 1.0);
    normalizationConfidence = Number(normalizationConfidence.toFixed(4));
  }

  // 6. Greedy Longest-Match-First Canonical Term Extraction
  // Invariant: Multi-word phrases take strict priority over fragmented single tokens.
  const canonicalTerms = extractCanonicalTerms(normalizedTokens);

  return {
    originalText,
    normalizedText,
    corrections,
    tokens: normalizedTokens,
    canonicalTerms,
    normalizationConfidence
  };
}
