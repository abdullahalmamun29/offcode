/**
 * Unit tests for C++ Code Generator.
 */

import { generateSinglyLinkedListInsertEnd } from "../generator/cppGenerator";
import { ProblemSpec } from "../models/problemSpec";

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

  console.log("\n[TypeScript Tests: C++ Generator]");

  const spec: ProblemSpec = {
    status: "success",
    language: "cpp",
    domain: "data_structure",
    structure: "singly_linked_list",
    operation: "insert_end",
    confidence: 1.0,
    confidence_basis: "exact_rule_match",
    raw_query: "Insert a node at the end of a singly linked list."
  };

  const code = generateSinglyLinkedListInsertEnd(spec);

  assert(code.includes("#include <iostream>"), "Includes <iostream>");
  assert(code.includes("struct Node"), "Defines Node struct");
  assert(code.includes("Node* next;"), "Node contains next pointer");
  assert(code.includes("int data;"), "Node contains data member");
  assert(code.includes("createNode(int data)"), "Defines createNode helper");
  assert(code.includes("insertAtEnd(Node*& head, int data)"), "Defines insertAtEnd function");
  assert(code.includes("displayList(const Node* head)"), "Defines displayList traversal function");
  assert(code.includes("freeList(Node*& head)"), "Defines freeList memory management function");
  assert(code.includes("int main()"), "Contains runnable main() function");
  assert(code.includes("Time Complexity"), "Contains educational complexity metadata");

  return { passed, failed };
}
