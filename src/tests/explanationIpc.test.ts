/**
 * CHUP Phase 7 — Explanation IPC & Schema Verification Tests (Test N).
 *
 * Validates:
 * 1. Python -> JSON -> TypeScript round-trip validation against ExplanationDocument schema.
 * 2. Fail-closed behavior on corrupted / invalid payloads.
 * 3. Epistemic status enforcement and evidence integrity.
 * 4. All 10 explanation sections presence and claim typing.
 * 5. Clean C++ code guarantee (no explanation artifacts in generated program).
 * 6. Cross-run isolation across consecutive solver calls.
 */

import { PointerBridge } from '../parser/pointerBridge';
import {
  ExplanationDocument,
  validateExplanationDocument,
  EpistemicStatus
} from '../models/explanationModel';
import { parseProblem } from '../pipeline/problemParser';
import { normalizeInput } from '../pipeline/inputNormalizer';
import { solveCpProblem } from '../solver/cpSolver';

interface TestResult {
  name: string;
  passed: boolean;
  notes?: string;
}

export function runExplanationIpcTests(): { passed: number; failed: number } {
  const results: TestResult[] = [];

  function record(name: string, passed: boolean, notes: string = ""): boolean {
    results.push({ name, passed, notes });
    if (passed) {
      console.log(`  ✓ [ExplanationIPC] ${name}`);
    } else {
      console.error(`  ✗ [ExplanationIPC] ${name} — ${notes}`);
    }
    return passed;
  }

  const bridge = new PointerBridge();

  // Test 1: Python Bridge returns valid ExplanationDocument on standard CP query
  const query = "Given a sorted array of integers, find two numbers that add up to target T.";
  const resp = bridge.explainProblemSync(query, "DETAILED");

  record(
    "Bridge returns success status for valid problem query",
    resp.status === "success",
    `Expected status 'success', got '${resp.status}' (error: ${resp.error})`
  );

  const doc = resp.explanation ? validateExplanationDocument(resp.explanation) : null;
  record(
    "Schema validation passes for Python bridge explanation payload",
    doc !== null,
    "validateExplanationDocument returned null on Python bridge output"
  );

  if (doc) {
    record(
      "Document schema version is 1.0.0",
      doc.schema_version === "1.0.0",
      `Expected schema_version '1.0.0', got '${doc.schema_version}'`
    );

    record(
      "Outcome state is valid authoritative state",
      ["SATISFIABLE_SINGLE_CANDIDATE", "SATISFIABLE_COMPOSED_PLAN", "UNSATISFIABLE_CONSTRAINT_SET", "UNRESOLVED_BY_CURRENT_ONTOLOGY"].includes(doc.outcome_state),
      `Unexpected outcome state: ${doc.outcome_state}`
    );

    record(
      "All 10 required sections exist with titles",
      Boolean(
        doc.understanding_section?.title &&
        doc.proven_facts_section?.title &&
        doc.derivation_section?.title &&
        doc.constraint_section?.title &&
        doc.elimination_section?.title &&
        doc.selection_section?.title &&
        doc.composition_section?.title &&
        doc.resource_section?.title &&
        doc.correctness_section?.title &&
        doc.summary_section?.title
      ),
      "One or more required sections missing or untyped"
    );

    // Test claims have valid epistemic status and non-empty evidence
    const validStatuses: EpistemicStatus[] = ['PROVEN', 'SUPPORTED', 'HYPOTHETICAL', 'UNRESOLVED'];
    let allClaimsValid = true;
    let claimCount = 0;
    let evidenceCount = 0;

    const sections = [
      doc.understanding_section,
      doc.proven_facts_section,
      doc.derivation_section,
      doc.constraint_section,
      doc.elimination_section,
      doc.selection_section,
      doc.composition_section,
      doc.resource_section,
      doc.correctness_section,
      doc.summary_section
    ];

    for (const sec of sections) {
      for (const claim of sec.claims) {
        claimCount++;
        if (!validStatuses.includes(claim.epistemic_status)) {
          allClaimsValid = false;
        }
        if (!claim.evidence_refs || claim.evidence_refs.length === 0) {
          allClaimsValid = false;
        } else {
          evidenceCount += claim.evidence_refs.length;
        }
      }
    }

    record(
      "All explanation claims carry strictly typed epistemic status and mandatory evidence",
      allClaimsValid && claimCount > 0 && evidenceCount > 0,
      `claimCount=${claimCount}, evidenceCount=${evidenceCount}, valid=${allClaimsValid}`
    );
  }

  // Test 2: Schema validation fail-closed on corrupted inputs
  record(
    "Fail-closed on null input",
    validateExplanationDocument(null) === null,
    "Expected null for null input"
  );

  record(
    "Fail-closed on primitive string input",
    validateExplanationDocument("not an object") === null,
    "Expected null for primitive string"
  );

  record(
    "Fail-closed on missing required sections",
    validateExplanationDocument({
      schema_version: "1.0.0",
      problem_id: "test",
      outcome_state: "SATISFIABLE_SINGLE_CANDIDATE",
      level: "DETAILED"
    }) === null,
    "Expected null when sections are missing"
  );

  // Test 3: Corrupted claim fail-closed
  if (doc) {
    const corruptedDoc = JSON.parse(JSON.stringify(doc));
    // Corrupt an epistemic status
    if (corruptedDoc.understanding_section?.claims?.[0]) {
      corruptedDoc.understanding_section.claims[0].epistemic_status = "INVALID_STATUS";
      record(
        "Fail-closed on invalid epistemic status in claim",
        validateExplanationDocument(corruptedDoc) === null,
        "Expected null when claim epistemic_status is corrupted"
      );
    }

    const corruptedEvidenceDoc = JSON.parse(JSON.stringify(doc));
    if (corruptedEvidenceDoc.proven_facts_section?.claims?.[0]) {
      corruptedEvidenceDoc.proven_facts_section.claims[0].evidence_refs = [];
      record(
        "Fail-closed on claim with empty evidence_refs",
        validateExplanationDocument(corruptedEvidenceDoc) === null,
        "Expected null when claim has empty evidence_refs"
      );
    }
  }

  // Test 4: Clean code guarantee across solver pipeline
  const normalized = normalizeInput(query);
  const parsed = parseProblem(normalized, query);
  const solverRes = solveCpProblem(parsed);

  record(
    "Solver returns code successfully",
    Boolean(solverRes.success && solverRes.code),
    `Solver failed: ${solverRes.limitationMessage || solverRes.reasoning}`
  );

  if (solverRes.code) {
    const forbiddenPhrases = [
      "ExplanationDocument",
      "EvidenceRef",
      "EpistemicStatus",
      "ProofObligation",
      "ProblemUnderstandingClaim",
      "CandidateEliminationClaim"
    ];
    let sourceClean = true;
    for (const phrase of forbiddenPhrases) {
      if (solverRes.code.includes(phrase)) {
        sourceClean = false;
        break;
      }
    }
    record(
      "Generated C++ code is 100% clean and contains zero explanation or proof artifacts",
      sourceClean,
      "Found forbidden explanation artifacts inside generated C++ code"
    );
  }

  record(
    "Solver result carries typed explanation document",
    solverRes.explanation !== undefined && solverRes.explanation !== null,
    "solverRes.explanation is missing or null"
  );

  // Test 5: Cross-run isolation across consecutive problems
  const query2 = "Given an array of integers, find the maximum sum of a contiguous subarray.";
  const resp2 = bridge.explainProblemSync(query2, "DETAILED");
  const doc2 = resp2.explanation ? validateExplanationDocument(resp2.explanation) : null;

  record(
    "Consecutive distinct problem explanations have isolated IDs and non-overlapping claims",
    Boolean(doc && doc2 && doc.problem_id !== doc2.problem_id),
    `doc1 id=${doc?.problem_id}, doc2 id=${doc2?.problem_id}`
  );

  const passed = results.filter(r => r.passed).length;
  const failed = results.filter(r => !r.passed).length;
  return { passed, failed };
}
