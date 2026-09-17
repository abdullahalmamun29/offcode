/**
 * Unit tests for Operation Resolver V1.
 */

import { resolveProblemSpec } from "../resolver/operationResolver";
import { ProblemSpecV1 } from "../models/problemSpec";

function makeSpec(overrides: Partial<ProblemSpecV1>): ProblemSpecV1 {
  return {
    status: "success",
    language: "cpp",
    domain: "data_structure",
    intent: "code_generation",
    structure: { type: "singly_linked_list", confidence_basis: "exact_rule_match" },
    operation: { action: "insert", position: "tail", combined: "insert_end", negated: false },
    compound: { is_compound: false, detected_actions: [] },
    numerical: { method: null, category: null },
    confidence: 1.0,
    confidence_basis: "exact_rule_match",
    error_code: null,
    message: "",
    raw_query: "test",
    normalized_query: "test",
    ...overrides
  };
}

export function runResolverTests(): { passed: number; failed: number } {
  let passed = 0;
  let failed = 0;

  function assert(condition: boolean, testName: string) {
    if (condition) {
      console.log(`  ✓ ${testName}`);
      passed++;
    } else {
      console.error(`  ✗ ${testName}`);
      failed++;
    }
  }

  console.log("\n[TypeScript Tests: Operation Resolver V1]");

  // 1. Success: SLL + insert_end
  const res1 = resolveProblemSpec(makeSpec({}));
  assert(res1.code === "SUCCESS", "Resolves SLL insert_end to SUCCESS");
  assert(res1.moduleId === "singly_linked_list.insert_end.cpp", "Correct moduleId for SLL insert_end");

  // 2. Negated
  const res2 = resolveProblemSpec(makeSpec({ status: "negated" }));
  assert(res2.code === "NEGATED", "Resolves negated to NEGATED");

  // 3. Question
  const res3 = resolveProblemSpec(makeSpec({ status: "question", intent: "conceptual_question" }));
  assert(res3.code === "QUESTION", "Resolves question to QUESTION");

  // 4. Compound
  const res4 = resolveProblemSpec(makeSpec({
    status: "unsupported",
    compound: { is_compound: true, detected_actions: ["insert", "delete"] },
    error_code: "UNSUPPORTED_COMPOUND_PROBLEM"
  }));
  assert(res4.code === "COMPOUND_UNSUPPORTED", "Resolves compound to COMPOUND_UNSUPPORTED");

  // 5. Ambiguous
  const res5 = resolveProblemSpec(makeSpec({
    status: "ambiguous",
    structure: { type: null, confidence_basis: "ambiguous" },
    error_code: "AMBIGUOUS_STRUCTURE"
  }));
  assert(res5.code === "AMBIGUOUS", "Resolves ambiguous to AMBIGUOUS");

  // 6. Unsupported structure
  const res6 = resolveProblemSpec(makeSpec({
    status: "unsupported",
    structure: { type: "unknown_ds", confidence_basis: "exact_rule_match" },
    operation: { action: "insert", position: "tail", combined: "insert_end", negated: false }
  }));
  assert(res6.code === "UNSUPPORTED_STRUCTURE", "Resolves unknown structure to UNSUPPORTED_STRUCTURE");

  // 7. Unsupported operation on known structure
  const res7 = resolveProblemSpec(makeSpec({
    operation: { action: "frobnicate", position: null, combined: "frobnicate", negated: false }
  }));
  assert(res7.code === "UNSUPPORTED_OPERATION", "Resolves unknown operation to UNSUPPORTED_OPERATION");

  // 8. Numerical method resolution
  const res8 = resolveProblemSpec(makeSpec({
    domain: "numerical",
    structure: { type: null, confidence_basis: "exact_rule_match" },
    numerical: { method: "bisection", category: "root_finding" },
    operation: { action: null, position: null, combined: null, negated: false }
  }));
  assert(res8.code === "SUCCESS", "Resolves bisection to SUCCESS");
  assert(res8.moduleId === "numerical.root_finding.bisection.cpp", "Correct moduleId for bisection");

  return { passed, failed };
}
