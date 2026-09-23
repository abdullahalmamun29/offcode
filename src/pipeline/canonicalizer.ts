/**
 * CHUP / Offcode — Canonicalization Layer (Phase 3)
 *
 * Explicitly separates phrase/concept canonicalization from lexical token normalization.
 *
 * Responsibilities:
 * - Converts recognized lexical token sequences into canonical concepts.
 * - Operates over NormalizedInput tokens without re-running spell correction.
 * - Extracts multi-word canonical phrases using greedy longest-match-first priority.
 * - Preserves token span provenance (startToken, endToken, confidence).
 * - Does NOT infer user intent, select solvers, or classify domains.
 */

import { CanonicalTerm, CanonicalizedInput, NormalizedInput, NormalizedToken } from '../models/problemSpec';
import { CANONICAL_PHRASES } from './domainVocabulary';

/**
 * Reconstructs rich NormalizedToken objects from NormalizedInput.
 */
export function buildNormalizedTokens(normalized: NormalizedInput): NormalizedToken[] {
  // Extract original tokens to maintain provenance
  const sanitizedProse = normalized.originalText
    .replace(/[\u2018\u2019\u201C\u201D]/g, "'")
    .replace(/[\u2010\u2011\u2012\u2013\u2014\u2015\u2212]/g, ' ')
    .replace(/\u00A0/g, ' ')
    .replace(/[-_]/g, ' ');

  const rawMatches = Array.from(sanitizedProse.matchAll(/[a-zA-Z0-9]+/g)).map(m => m[0]);

  const correctedIndices = new Set<number>();
  for (const corr of normalized.corrections) {
    for (let idx = corr.startToken; idx < corr.endToken; idx++) {
      correctedIndices.add(idx);
    }
  }

  return normalized.tokens.map((tok, idx) => ({
    index: idx,
    text: tok,
    originalText: rawMatches[idx] || tok,
    corrected: correctedIndices.has(idx)
  }));
}

/**
 * Extracts canonical terms from an array of normalized token strings.
 * Longest-match-first priority guarantees multi-word phrases take precedence
 * over isolated sub-tokens.
 */
export function extractCanonicalTerms(tokens: string[]): CanonicalTerm[] {
  const canonicalTerms: CanonicalTerm[] = [];
  let tokenIdx = 0;

  while (tokenIdx < tokens.length) {
    let matched = false;

    // CANONICAL_PHRASES is pre-sorted by phrase token length descending
    for (const def of CANONICAL_PHRASES) {
      const phraseTokens = def.phrase.split(/\s+/);
      const spanLen = phraseTokens.length;

      if (tokenIdx + spanLen <= tokens.length) {
        const slice = tokens.slice(tokenIdx, tokenIdx + spanLen);
        const candidatePhrase = slice.join(' ');

        if (candidatePhrase === def.phrase) {
          canonicalTerms.push({
            canonical: def.canonical,
            surfaceForm: candidatePhrase,
            confidence: 1.0,
            startToken: tokenIdx,          // inclusive
            endToken: tokenIdx + spanLen   // exclusive
          });

          tokenIdx += spanLen;
          matched = true;
          break; // Longest match accepted for this starting index
        }
      }
    }

    if (!matched) {
      tokenIdx++;
    }
  }

  return canonicalTerms;
}

/**
 * Canonicalization entrypoint.
 * Converts NormalizedInput into a CanonicalizedInput structure.
 */
export function canonicalize(normalized: NormalizedInput): CanonicalizedInput {
  const tokens = buildNormalizedTokens(normalized);
  const tokenStrings = tokens.map(t => t.text);
  const canonicalTerms = extractCanonicalTerms(tokenStrings);

  // Canonicalization confidence: 1.0 if all extracted phrases are known canonical concepts
  const canonicalizationConfidence = canonicalTerms.length > 0 ? 1.0 : 1.0;

  return {
    normalizedInput: normalized,
    tokens,
    canonicalTerms,
    canonicalizationConfidence
  };
}
