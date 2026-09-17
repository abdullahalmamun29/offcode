/**
 * Unit tests for C++ Code Generator V1.
 */

import { generateCpp } from "../generator/cppGenerator";
import { ProblemSpecV1, ResolutionResult } from "../models/problemSpec";

function makeResolution(moduleId: string): ResolutionResult {
  return {
    code: "SUCCESS",
    moduleId: moduleId,
    moduleName: "Test Module",
    message: "Resolved",
    spec: {
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
      raw_query: "Insert a node at the end of a singly linked list.",
      normalized_query: "insert a node at the end of a singly linked list"
    }
  };
}

export function runGeneratorTests(): { passed: number; failed: number } {
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

  console.log("\n[TypeScript Tests: C++ Generator V1]");

  // Test 1: Generate SLL insert_end
  const code = generateCpp(makeResolution("singly_linked_list.insert_end.cpp"));
  assert(code.includes("#include"), "Generated code has includes");
  assert(code.includes("int main()"), "Generated code has main()");
  assert(code.includes("cin") || code.includes("std::cin"), "Generated code uses cin input (not hardcoded)");
  assert(!code.includes("CodeForge"), "Generated code has no CodeForge branding");

  // Test 2: Non-success resolution
  const failRes: ResolutionResult = {
    code: "UNSUPPORTED_OPERATION",
    message: "Not supported",
    spec: makeResolution("x").spec
  };
  const failCode = generateCpp(failRes);
  assert(failCode.includes("//") || failCode.includes("Failed"), "Non-success returns comment/error");

  return { passed, failed };
}
