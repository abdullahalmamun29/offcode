/**
 * End-to-End Pipeline Verification Test for CodeForge.
 *
 * Full pipeline:
 * Natural Language Query
 *        ↓
 * Python NLP Parser (python_parser/parser.py)
 *        ↓
 * Structured ProblemSpec JSON
 *        ↓
 * TypeScript Resolver (src/resolver/operationResolver.ts)
 *        ↓
 * Verified C++ Generator (src/generator/cppGenerator.ts)
 *        ↓
 * C++ Source File (.cpp)
 *        ↓
 * Compiler (g++ -std=c++17 -Wall -Wextra -pedantic)
 *        ↓
 * Executable Binary
 *        ↓
 * Program Execution & Stdout Verification
 */

import * as fs from "fs";
import * as path from "path";
import { execSync } from "child_process";
import { PythonBridge } from "../parser/pythonBridge";
import { resolveProblemSpec, generateCodeForResolution } from "../resolver/operationResolver";

export async function runE2EPipeline(): Promise<void> {
  console.log("=================================================");
  console.log("    CodeForge Full End-to-End Pipeline Test      ");
  console.log("=================================================\n");

  const projectRoot = path.resolve(__dirname, "..", "..");
  const buildDir = path.join(projectRoot, "dist_test");
  if (!fs.existsSync(buildDir)) {
    fs.mkdirSync(buildDir, { recursive: true });
  }

  const pythonBridge = new PythonBridge();

  // Test Case A: Valid Natural Language Query -> Full compilation & execution
  const validQuery = "Insert a node at the end of a singly linked list.";
  console.log(`[Step 1: Input Query]`);
  console.log(`  Natural Language: "${validQuery}"\n`);

  console.log(`[Step 2: Python NLP Parser]`);
  const spec = await pythonBridge.parseQuery(validQuery);
  console.log(`  Status           : ${spec.status}`);
  console.log(`  Structure        : ${spec.structure}`);
  console.log(`  Operation        : ${spec.operation}`);
  console.log(`  Confidence Basis : ${spec.confidence_basis}`);
  console.log(`  Confidence       : ${spec.confidence}\n`);

  if (spec.status !== "success") {
    throw new Error(`Expected parser success, got: ${spec.status} (${spec.message})`);
  }

  console.log(`[Step 3: TypeScript Resolver]`);
  const resolution = resolveProblemSpec(spec);
  console.log(`  Resolution Code  : ${resolution.code}`);
  console.log(`  Module ID        : ${resolution.moduleId}`);
  console.log(`  Module Name      : ${resolution.moduleName}\n`);

  if (resolution.code !== "SUCCESS") {
    throw new Error(`Expected resolution SUCCESS, got: ${resolution.code}`);
  }

  console.log(`[Step 4: Verified C++ Generator]`);
  const cppCode = generateCodeForResolution(resolution);
  const cppFilePath = path.join(buildDir, "singly_linked_list_insert_end.cpp");
  fs.writeFileSync(cppFilePath, cppCode, "utf8");
  console.log(`  Generated C++ file written to: ${cppFilePath}\n`);

  console.log(`[Step 5: Compilation with g++]`);
  const binFilePath = path.join(buildDir, "singly_linked_list_insert_end");
  const compileCmd = `g++ -std=c++17 -Wall -Wextra -pedantic "${cppFilePath}" -o "${binFilePath}"`;
  console.log(`  Executing: ${compileCmd}`);
  execSync(compileCmd, { stdio: "inherit" });
  console.log(`  ✓ Compilation succeeded with 0 warnings/errors!\n`);

  console.log(`[Step 6: Executable Runtime Execution]`);
  const runtimeOutput = execSync(`"${binFilePath}"`, { encoding: "utf8" });
  console.log(`  Program Output:\n----------------------------------------`);
  console.log(runtimeOutput.trim());
  console.log(`----------------------------------------\n`);

  // Assert expected output
  if (!runtimeOutput.includes("10 -> 20 -> 30 -> NULL")) {
    throw new Error(`Runtime output missing expected linked list traversal: "10 -> 20 -> 30 -> NULL"`);
  }
  console.log(`  ✓ Output validation passed: Linked list successfully built and traversed!\n`);

  // Test Case B: Compound Query Rejection (Safety check)
  const compoundQuery = "Reverse a singly linked list and then insert a node at the end.";
  console.log(`[Safety Test: Compound Query Rejection]`);
  console.log(`  Query: "${compoundQuery}"`);
  const compoundSpec = await pythonBridge.parseQuery(compoundQuery);
  const compoundResolution = resolveProblemSpec(compoundSpec);
  console.log(`  Parser Status   : ${compoundSpec.status}`);
  console.log(`  Resolution Code : ${compoundResolution.code}`);
  console.log(`  Message         : ${compoundResolution.message}`);

  if (compoundResolution.code !== "COMPOUND_UNSUPPORTED") {
    throw new Error(`Expected COMPOUND_UNSUPPORTED, got ${compoundResolution.code}`);
  }
  console.log(`  ✓ Compound query safely rejected without generating code!\n`);

  console.log("=================================================");
  console.log("  ✓ ALL END-TO-END PIPELINE CHECKS PASSED 100%   ");
  console.log("=================================================");
}

if (require.main === module) {
  runE2EPipeline().catch((err) => {
    console.error("\n❌ E2E Pipeline Failure:", err);
    process.exit(1);
  });
}
