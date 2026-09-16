/**
 * Unit tests for Operation Resolver.
 */

import { resolveProblemSpec } from "../resolver/operationResolver";
import { ProblemSpec } from "../models/problemSpec";

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

  console.log("\n[TypeScript Tests: Operation Resolver]");

  // 1. Success case: singly_linked_list + insert_end + cpp
  const validSpec: ProblemSpec = {
    status: "success",
    language: "cpp",
    domain: "data_structure",
    structure: "singly_linked_list",
    operation: "insert_end",
    confidence: 1.0,
    confidence_basis: "exact_rule_match",
    raw_query: "Insert a node at the end of a singly linked list."
  };
  const resSuccess = resolveProblemSpec(validSpec);
  assert(resSuccess.code === "SUCCESS", "Resolves valid singly_linked_list insert_end to SUCCESS");
  assert(resSuccess.moduleId === "singly_linked_list_insert_end_cpp", "Resolves to correct moduleId");

  // 2. Identified but unsupported operation: singly_linked_list + reverse
  const unsupportedOpSpec: ProblemSpec = {
    status: "unsupported",
    language: "cpp",
    domain: "data_structure",
    structure: "singly_linked_list",
    operation: "reverse",
    confidence: 0.0,
    confidence_basis: "unsupported",
    error_code: "UNSUPPORTED_OPERATION",
    message: "Operation reverse not supported."
  };
  const resUnsupportedOp = resolveProblemSpec(unsupportedOpSpec);
  assert(
    resUnsupportedOp.code === "IDENTIFIED_UNSUPPORTED",
    "Resolves recognized but unsupported operation to IDENTIFIED_UNSUPPORTED"
  );

  // 3. Identified but unsupported structure: binary_tree
  const unsupportedStructSpec: ProblemSpec = {
    status: "unsupported",
    language: "cpp",
    domain: "data_structure",
    structure: "binary_tree",
    operation: "create",
    confidence: 0.0,
    confidence_basis: "unsupported",
    error_code: "UNSUPPORTED_STRUCTURE"
  };
  const resUnsupportedStruct = resolveProblemSpec(unsupportedStructSpec);
  assert(
    resUnsupportedStruct.code === "IDENTIFIED_UNSUPPORTED",
    "Resolves unsupported structure to IDENTIFIED_UNSUPPORTED"
  );

  // 4. Ambiguous / Missing structure
  const ambiguousSpec: ProblemSpec = {
    status: "ambiguous",
    language: "cpp",
    domain: "data_structure",
    structure: undefined,
    operation: "insert_end",
    confidence: 0.0,
    confidence_basis: "ambiguous",
    error_code: "AMBIGUOUS_STRUCTURE"
  };
  const resAmbiguous = resolveProblemSpec(ambiguousSpec);
  assert(resAmbiguous.code === "CANNOT_IDENTIFY", "Resolves ambiguous structure to CANNOT_IDENTIFY");

  // 5. Compound operation
  const compoundSpec: ProblemSpec = {
    status: "unsupported",
    language: "cpp",
    domain: "data_structure",
    structure: "singly_linked_list",
    operation: "compound_operation",
    confidence: 0.0,
    confidence_basis: "unsupported",
    error_code: "UNSUPPORTED_COMPOUND_PROBLEM"
  };
  const resCompound = resolveProblemSpec(compoundSpec);
  assert(resCompound.code === "COMPOUND_UNSUPPORTED", "Resolves compound query to COMPOUND_UNSUPPORTED");

  return { passed, failed };
}
