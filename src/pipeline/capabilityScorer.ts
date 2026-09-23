/**
 * CHUP / Offcode — Capability Scorer (Phase 3)
 *
 * Evaluates structured SemanticInput against Registered Capabilities.
 *
 * Core Architectural Invariants:
 * - Tri-state matching: 'eligible' | 'disqualified' | 'insufficient'.
 * - Disqualification: Conflicting evidence in primary role actively disqualifies candidate (status: 'disqualified', score: 0).
 * - Insufficient evidence: Missing required evidence leaves capability unqualified (status: 'insufficient', score < 0.50).
 * - No semantic invention: Scorer never infers or fabricates missing evidence.
 * - Ambiguity handling: When top eligible candidates have comparable scores (|Δscore| < 0.05), flags ambiguity without guessing.
 */

import {
  CapabilityMatchStatus,
  CapabilityScore,
  EvidencePredicate,
  EvidenceRef,
  SemanticInput
} from '../models/problemSpec';
import { CapabilityDefinition, REGISTERED_CAPABILITIES } from './capabilityRegistry';

/**
 * Checks if a given predicate matches any item in the extracted semantic evidence.
 */
function matchesPredicate(
  pred: EvidencePredicate,
  semantic: SemanticInput
): { matched: boolean; matchedRef?: EvidenceRef } {
  const targetValues = Array.isArray(pred.value) ? pred.value : [pred.value];

  switch (pred.kind) {
    case 'entity': {
      for (const ent of semantic.entities) {
        if (targetValues.includes(ent.value)) {
          return {
            matched: true,
            matchedRef: { kind: 'entity', value: ent.value }
          };
        }
      }
      return { matched: false };
    }

    case 'operation': {
      for (const op of semantic.operations) {
        if (targetValues.includes(op.operation)) {
          return {
            matched: true,
            matchedRef: { kind: 'operation', value: op.operation }
          };
        }
      }
      return { matched: false };
    }

    case 'intent': {
      for (const it of semantic.intents) {
        if (targetValues.includes(it.intent)) {
          return {
            matched: true,
            matchedRef: { kind: 'intent', value: it.intent }
          };
        }
      }
      return { matched: false };
    }

    case 'constraint': {
      for (const c of semantic.constraints) {
        if (pred.type && c.type !== pred.type) continue;
        if (targetValues.includes(c.value)) {
          return {
            matched: true,
            matchedRef: { kind: 'constraint', type: c.type, value: c.value }
          };
        }
      }
      return { matched: false };
    }

    default:
      return { matched: false };
  }
}

/**
 * Evaluates semantic evidence against a single capability definition.
 */
export function scoreSingleCapability(
  cap: CapabilityDefinition,
  semantic: SemanticInput
): CapabilityScore {
  const positiveEvidence: EvidenceRef[] = [];
  const negativeEvidence: EvidenceRef[] = [];
  const missingEvidence: EvidenceRef[] = [];

  // 1. Check Contradictions (Semantic Role Based)
  if (cap.contradictions) {
    for (const contra of cap.contradictions) {
      const match = matchesPredicate(contra, semantic);
      if (match.matched && match.matchedRef) {
        negativeEvidence.push(match.matchedRef);
      }
    }
  }

  // If contradictory evidence was identified, disqualify immediately
  if (negativeEvidence.length > 0) {
    return {
      capability: cap.id,
      domain: cap.domain,
      status: 'disqualified',
      positiveEvidence: [],
      negativeEvidence,
      missingEvidence: [],
      score: 0.0
    };
  }

  // 2. Check Requirements
  let requiredMatchedCount = 0;
  for (const req of cap.requirements) {
    const match = matchesPredicate(req, semantic);
    if (match.matched && match.matchedRef) {
      positiveEvidence.push(match.matchedRef);
      requiredMatchedCount++;
    } else {
      const primaryVal = Array.isArray(req.value) ? req.value.join('|') : req.value;
      missingEvidence.push({
        kind: req.kind,
        type: req.type,
        value: primaryVal
      });
    }
  }

  // 3. Check Optional Evidence (only if not disqualified)
  if (cap.optionalEvidence) {
    for (const opt of cap.optionalEvidence) {
      const match = matchesPredicate(opt, semantic);
      if (match.matched && match.matchedRef) {
        positiveEvidence.push(match.matchedRef);
      }
    }
  }

  // 4. Determine Tri-State Status and Score
  let status: CapabilityMatchStatus;
  let score: number;

  if (missingEvidence.length > 0) {
    // Insufficient evidence to discharge all capability obligations
    status = 'insufficient';
    // Score reflects partial match but stays strictly below 0.50
    const ratio = cap.requirements.length > 0 ? requiredMatchedCount / cap.requirements.length : 0;
    score = Number((ratio * 0.35).toFixed(4));
  } else {
    // All requirements fully satisfied!
    status = 'eligible';
    // Base score 0.80 for complete requirement fulfillment
    let calculated = 0.80;
    // Add small bonus for each optional evidence piece matched (up to 1.0)
    const optionalMatches = positiveEvidence.length - requiredMatchedCount;
    calculated += Math.min(0.20, optionalMatches * 0.05);
    score = Number(calculated.toFixed(4));
  }

  return {
    capability: cap.id,
    domain: cap.domain,
    status,
    positiveEvidence,
    negativeEvidence,
    missingEvidence,
    score
  };
}

/**
 * Scores all registered capabilities against the semantic input.
 * Returns candidate scores sorted descending by score.
 */
export function scoreCapabilities(semantic: SemanticInput): CapabilityScore[] {
  const scores: CapabilityScore[] = [];

  for (const cap of REGISTERED_CAPABILITIES) {
    scores.push(scoreSingleCapability(cap, semantic));
  }

  // Sort descending by score, then alphabetically by capability ID for determinism
  return scores.sort((a, b) => {
    if (b.score !== a.score) {
      return b.score - a.score;
    }
    return a.capability.localeCompare(b.capability);
  });
}
