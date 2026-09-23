/**
 * End-to-End Pipeline Verification Test for CodeForge V1.
 *
 * Full pipeline:
 * Natural Language Query → Python NLP Parser → ProblemSpecV1 JSON
 * → TypeScript Resolver → Verified C++ Generator → C++ Source File
 * → g++ Compilation → Executable Binary → stdin-fed Execution → stdout Verification
 */

import * as fs from "fs";
import * as path from "path";
import * as os from "os";
import { PythonBridge } from "../parser/pythonBridge";
import { resolveProblemSpec } from "../resolver/operationResolver";
import { generateCpp } from "../generator/cppGenerator";
import { compileCpp } from "../verifier/compiler";
import { executeProgram } from "../verifier/runner";

export async function runE2EPipeline(): Promise<void> {
  console.log("=================================================");
  console.log("    CodeForge V1 Full End-to-End Pipeline Test    ");
  console.log("=================================================\n");

  const projectRoot = path.resolve(__dirname, "..", "..");
  let buildDir = path.join(projectRoot, "dist_test");
  try {
    if (!fs.existsSync(buildDir)) {
      fs.mkdirSync(buildDir, { recursive: true });
    }
    const probe = path.join(buildDir, ".write_probe");
    fs.writeFileSync(probe, "ok");
    fs.unlinkSync(probe);
  } catch (_) {
    buildDir = path.join(os.tmpdir(), "chup_dist_test");
    if (!fs.existsSync(buildDir)) {
      fs.mkdirSync(buildDir, { recursive: true });
    }
  }

  const pythonBridge = new PythonBridge();

  // ─── Test Case A: SLL Insert at End (stdin-fed) ───────────────────────────
  const validQuery = "Insert a node at the end of a singly linked list.";
  console.log(`[Step 1: Input Query]`);
  console.log(`  Natural Language: "${validQuery}"\n`);

  console.log(`[Step 2: Python NLP Parser]`);
  const spec = await pythonBridge.parseQuery(validQuery);
  console.log(`  Status           : ${spec.status}`);
  console.log(`  Structure        : ${spec.structure.type}`);
  console.log(`  Operation        : ${spec.operation.combined}`);
  console.log(`  Domain           : ${spec.domain}`);
  console.log(`  Intent           : ${spec.intent}`);
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
    throw new Error(`Expected resolution SUCCESS, got: ${resolution.code} — ${resolution.message}`);
  }

  console.log(`[Step 4: Verified C++ Generator]`);
  const cppCode = generateCpp(resolution);
  const cppFilePath = path.join(buildDir, "singly_linked_list_insert_end.cpp");
  fs.writeFileSync(cppFilePath, cppCode, "utf8");
  console.log(`  Generated C++ written to: ${cppFilePath}`);
  console.log(`  Code length: ${cppCode.length} characters\n`);

  // Verify code quality
  if (!cppCode.includes("#include")) {
    throw new Error("Generated code missing #include directives");
  }
  if (!cppCode.includes("int main()") && !cppCode.includes("int main(")) {
    throw new Error("Generated code missing main() function");
  }
  if (cppCode.includes("CodeForge")) {
    throw new Error("Generated code contains CodeForge branding (not allowed in V1)");
  }
  console.log(`  ✓ Code quality checks passed\n`);

  console.log(`[Step 5: Compilation with g++]`);
  const binFilePath = path.join(buildDir, "singly_linked_list_insert_end");
  const compileResult = compileCpp(cppFilePath, binFilePath);
  if (!compileResult.success) {
    console.error(`  Compilation errors:`);
    compileResult.errors.forEach(e => console.error(`    ${e}`));
    throw new Error("Compilation failed");
  }
  console.log(`  ✓ Compilation succeeded with 0 errors!\n`);

  console.log(`[Step 6: Executable Runtime Execution (stdin-fed)]`);
  const stdinInput = "3\n10\n20\n30\n";
  console.log(`  Feeding stdin: ${JSON.stringify(stdinInput)}`);
  const execResult = executeProgram(binFilePath, stdinInput);
  console.log(`  Exit code: ${execResult.exitCode}`);
  console.log(`  Program Output:\n----------------------------------------`);
  console.log(execResult.stdout.trim());
  console.log(`----------------------------------------\n`);

  if (!execResult.success) {
    throw new Error(`Runtime execution failed. stderr: ${execResult.stderr}`);
  }
  if (execResult.stdout.includes("10") && execResult.stdout.includes("20") && execResult.stdout.includes("30")) {
    console.log(`  ✓ Output contains expected values (10, 20, 30)\n`);
  } else {
    throw new Error(`Output missing expected values. Got: ${execResult.stdout}`);
  }

  // ─── Test Case B: Compound Query Rejection ────────────────────────────────
  const compoundQuery = "Reverse a singly linked list and then insert a node at the end.";
  console.log(`[Safety Test: Compound Query Rejection]`);
  console.log(`  Query: "${compoundQuery}"`);
  const compoundSpec = await pythonBridge.parseQuery(compoundQuery);
  const compoundResolution = resolveProblemSpec(compoundSpec);
  console.log(`  Parser Status   : ${compoundSpec.status}`);
  console.log(`  Resolution Code : ${compoundResolution.code}`);
  if (compoundResolution.code !== "COMPOUND_UNSUPPORTED") {
    throw new Error(`Expected COMPOUND_UNSUPPORTED, got ${compoundResolution.code}`);
  }
  console.log(`  ✓ Compound query safely rejected!\n`);

  // ─── Test Case C: Negation Safety ─────────────────────────────────────────
  const negatedQuery = "do not insert at the end of the linked list";
  console.log(`[Safety Test: Negation Rejection]`);
  console.log(`  Query: "${negatedQuery}"`);
  const negatedSpec = await pythonBridge.parseQuery(negatedQuery);
  const negatedResolution = resolveProblemSpec(negatedSpec);
  console.log(`  Parser Status   : ${negatedSpec.status}`);
  console.log(`  Resolution Code : ${negatedResolution.code}`);
  if (negatedResolution.code !== "NEGATED") {
    throw new Error(`Expected NEGATED, got ${negatedResolution.code}`);
  }
  console.log(`  ✓ Negated instruction safely rejected!\n`);

  // ─── Test Case D: Question Detection ──────────────────────────────────────
  const questionQuery = "whats the difference between insert at tail and insert at head in a linked list";
  console.log(`[Safety Test: Question Detection]`);
  console.log(`  Query: "${questionQuery}"`);
  const questionSpec = await pythonBridge.parseQuery(questionQuery);
  const questionResolution = resolveProblemSpec(questionSpec);
  console.log(`  Parser Status   : ${questionSpec.status}`);
  console.log(`  Resolution Code : ${questionResolution.code}`);
  if (questionResolution.code !== "QUESTION") {
    throw new Error(`Expected QUESTION, got ${questionResolution.code}`);
  }
  console.log(`  ✓ Question detected and handled!\n`);

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
