/**
 * Integration tests for PythonBridge V1.
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

  console.log("\n[TypeScript Tests: PythonBridge V1]");

  const bridge = new PythonBridge();

  // Test 1: Supported query
  const res1 = await bridge.parseQuery("Add a node to the tail of the linked list.");
  assert(res1.status === "success", "Bridge returns success for valid SLL query");
  assert(res1.structure.type === "singly_linked_list", "Bridge identifies structure");
  assert(res1.operation.combined === "insert_end", "Bridge identifies operation insert_end");

  // Test 2: Conservative structure check
  const res2 = await bridge.parseQuery("Append a new node.");
  assert(res2.status === "ambiguous", "Bridge marks ambiguous when structure omitted");
  assert(res2.error_code === "AMBIGUOUS_STRUCTURE", "Bridge sets AMBIGUOUS_STRUCTURE");

  // Test 3: Compound rejection
  const res3 = await bridge.parseQuery("Reverse a singly linked list and then insert a node at the end.");
  assert(res3.status === "unsupported", "Bridge rejects compound query");
  assert(res3.error_code === "UNSUPPORTED_COMPOUND_PROBLEM", "Bridge sets compound error");

  // Test 4: Negation safety
  const res4 = await bridge.parseQuery("do not insert at the end of the linked list");
  assert(res4.status === "negated", "Bridge detects negated instruction");
  assert(res4.error_code === "NEGATED_INSTRUCTION_REFUSAL", "Bridge sets negation error");

  // Test 5: Question detection
  const res5 = await bridge.parseQuery("whats the difference between insert at tail and insert at head");
  assert(res5.status === "question", "Bridge detects conceptual question");

  // Test 6: Programmer vocabulary
  const res6 = await bridge.parseQuery("push_back in singly linked list");
  assert(res6.status === "success", "Bridge handles push_back vocabulary");
  assert(res6.operation.combined === "insert_end", "push_back maps to insert_end");

  // Test 7: Scope notation
  const res7 = await bridge.parseQuery("singly_linked_list::insert_tail()");
  assert(res7.status === "success", "Bridge handles :: scope notation");
  assert(res7.structure.type === "singly_linked_list", "Scope notation resolves structure");

  // Test 8: Contrastive negation
  const res8 = await bridge.parseQuery("insert a node at the beginning not at the end of singly linked list");
  assert(res8.status === "unsupported", "Contrastive negation not treated as compound");
  assert(res8.operation.combined === "insert_beginning", "Contrastive negation resolves to beginning");

  // Test 9: Numerical method
  const res9 = await bridge.parseQuery("bisection method");
  assert(res9.domain === "numerical", "Bridge detects numerical domain");
  assert(res9.numerical.method === "bisection", "Bridge identifies bisection method");

  return { passed, failed };
}
