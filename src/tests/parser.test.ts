/**
 * Integration tests for PythonBridge from TypeScript.
 */

import { PythonBridge } from "../parser/pythonBridge";

export async function runPythonBridgeTests(): Promise<{ passed: number; failed: number }> {
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

  console.log("\n[TypeScript Tests: PythonBridge]");

  const bridge = new PythonBridge();

  // Test 1: Supported query
  const res1 = await bridge.parseQuery("Add a node to the tail of the linked list.");
  assert(res1.status === "success", "Bridge returns success for valid linked list query");
  assert(res1.structure === "singly_linked_list", "Bridge correctly identifies structure singly_linked_list");
  assert(res1.operation === "insert_end", "Bridge correctly identifies operation insert_end");

  // Test 2: Conservative structure check
  const res2 = await bridge.parseQuery("Append a new node.");
  assert(res2.status === "ambiguous", "Bridge marks ambiguous when structure is omitted");
  assert(res2.error_code === "AMBIGUOUS_STRUCTURE", "Bridge sets AMBIGUOUS_STRUCTURE error code");

  // Test 3: Compound query prevention
  const res3 = await bridge.parseQuery("Reverse a singly linked list and then insert a node at the end.");
  assert(res3.status === "unsupported", "Bridge rejects compound query");
  assert(res3.error_code === "UNSUPPORTED_COMPOUND_PROBLEM", "Bridge sets UNSUPPORTED_COMPOUND_PROBLEM");

  return { passed, failed };
}
