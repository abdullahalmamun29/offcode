/**
 * CHUP Phase 8 — Adversarial Generalization & Robustness IPC Test Suite.
 *
 * Validates:
 * 1. Paraphrase & narrative invariance across certified perturbations.
 * 2. Keyword trap immunity: candidate rejection on precondition failure.
 * 3. Relevance discrimination: ignoring decoy lore while retaining core constraints.
 * 4. Preservation of 100% clean C++ code guarantee under adversarial surfaces.
 * 5. Order independence and cross-query state isolation.
 */

import { PointerBridge } from '../parser/pointerBridge';
import { normalizeInput } from '../pipeline/inputNormalizer';
import { parseProblem } from '../pipeline/problemParser';
import { solveCpProblem } from '../solver/cpSolver';
import { SolverResult } from '../models/problemSpec';
import { validateExplanationDocument } from '../models/explanationModel';

interface TestResult {
  name: string;
  passed: boolean;
  notes?: string;
}

function solveQuery(query: string): SolverResult {
  const normalized = normalizeInput(query);
  const parsed = parseProblem(normalized, query);
  return solveCpProblem(parsed);
}

export function runAdversarialGeneralizationTests(): { passed: number; failed: number } {
  const results: TestResult[] = [];

  function record(name: string, passed: boolean, notes: string = ""): boolean {
    results.push({ name, passed, notes });
    if (passed) {
      console.log(`  ✓ [AdversarialIPC] ${name}`);
    } else {
      console.error(`  ✗ [AdversarialIPC] ${name} — ${notes}`);
    }
    return passed;
  }

  const bridge = new PointerBridge();

  // ── 1. Paraphrase & Surface Invariance ──────────────────────────────
  const p1 = "Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number.";
  const p2 = "An ascending sorted sequence of values is provided. Identify indices of two elements whose summation exactly matches target T.";

  const sol1 = solveQuery(p1);
  const sol2 = solveQuery(p2);

  record(
    "Paraphrase Variant 1 solves successfully",
    sol1.success,
    `Success was false (reasoning: ${sol1.reasoning})`
  );

  record(
    "Paraphrase Variant 2 solves successfully",
    sol2.success,
    `Success was false (reasoning: ${sol2.reasoning})`
  );

  record(
    "Both paraphrase variants converge to equivalent solution concepts",
    sol1.selectedAlgorithm === sol2.selectedAlgorithm,
    `Variant 1 algorithm '${sol1.selectedAlgorithm}' != Variant 2 algorithm '${sol2.selectedAlgorithm}'`
  );

  // ── 2. Decoy Lore & Distractor Immunity ─────────────────────────────
  const distractorQuery =
    "Chef Luigi is in the kitchen preparing a feast for the festival of Numeralia with 5 mystical gates. " +
    "He has an inventory of N=100000 numbered spices stored in an ascending sorted sequence in non-decreasing order. " +
    "Help Luigi find two spices whose labels add up to the secret target sum before midnight.";

  const solDistractor = solveQuery(distractorQuery);

  record(
    "Distractor query with heavy lore solves successfully",
    solDistractor.success,
    `Success was false (reasoning: ${solDistractor.reasoning})`
  );

  record(
    "Distractor query does not leak narrative tokens into generated C++",
    Boolean(
      solDistractor.code &&
      !solDistractor.code.includes("Chef Luigi") &&
      !solDistractor.code.includes("Numeralia") &&
      !solDistractor.code.includes("mystical gates")
    ),
    "Generated C++ contained distractor lore tokens"
  );

  // ── 3. Keyword Trap Immunity (Candidate Elimination) ───────────────
  const trapNegativeQuery =
    "Find contiguous subarray sum in unsorted sequence with negative values where sum equals target.";

  const solTrap = solveQuery(trapNegativeQuery);

  // Two pointers must NOT be selected on unsorted negative array without verification
  record(
    "Keyword trap on unsorted negative sequence avoids naive Two Pointers",
    solTrap.selectedAlgorithm !== "twoPointers" || !solTrap.success,
    "Naive Two Pointers was mistakenly selected on unsorted sequence with negative values"
  );

  // Explanation verification on trap
  const trapResp = bridge.explainProblemSync(
    "Compute single-source shortest paths in a directed graph where some edges have negative weights.",
    "DETAILED"
  );

  record(
    "Bridge returns explanation for negative shortest path trap",
    trapResp.status === "success",
    `Bridge returned ${trapResp.status}`
  );

  if (trapResp.explanation) {
    const expDoc = validateExplanationDocument(trapResp.explanation);
    record(
      "Trap explanation document is structurally valid",
      expDoc !== null,
      "validateExplanationDocument failed on trap output"
    );

    if (expDoc) {
      const eliminatedCands = expDoc.elimination_section.claims.map(c => c.candidate_id);
      record(
        "Dijkstra is properly eliminated in negative weights trap explanation",
        eliminatedCands.includes("dijkstra_priority_queue"),
        `Eliminated candidates were: ${eliminatedCands.join(", ")}`
      );
    }
  }

  // ── 4. Clean C++ Source Code Guarantee Under Adversarial Surfaces ───
  const allGeneratedCodes = [sol1.code, sol2.code, solDistractor.code].filter(Boolean) as string[];

  let allClean = true;
  const forbiddenPhrases = [
    "ExplanationSector",
    "EpistemicStatus",
    "PROVEN",
    "HYPOTHETICAL",
    "UNRESOLVED",
    "Phase 7",
    "Phase 8"
  ];

  for (const code of allGeneratedCodes) {
    for (const phrase of forbiddenPhrases) {
      if (code.includes(phrase)) {
        allClean = false;
        break;
      }
    }
  }

  record(
    "Clean C++ code guarantee: zero explanation/metadata comments across all adversarial runs",
    allClean,
    "Generated C++ contained forbidden metadata or explanation phrases"
  );

  // ── 5. Evaluator Order Independence (A -> B == B -> A) ─────────────
  const order1A = solveQuery(p1);
  const order1B = solveQuery(distractorQuery);

  const order2B = solveQuery(distractorQuery);
  const order2A = solveQuery(p1);

  record(
    "Order independence: Result of P1 identical regardless of preceding query",
    order1A.success === order2A.success && order1A.selectedAlgorithm === order2A.selectedAlgorithm,
    "Order dependence detected for P1"
  );

  record(
    "Order independence: Result of Distractor query identical regardless of preceding query",
    order1B.success === order2B.success && order1B.selectedAlgorithm === order2B.selectedAlgorithm,
    "Order dependence detected for Distractor query"
  );

  const passed = results.filter(r => r.passed).length;
  const failed = results.filter(r => !r.passed).length;

  console.log(`\nAdversarial Generalization Summary: ${passed} passed, ${failed} failed.\n`);
  return { passed, failed };
}
