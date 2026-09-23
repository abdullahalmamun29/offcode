/**
 * CHUP V2 — Verification Engine.
 *
 * Orchestrates the full verification pipeline: compile → run examples →
 * generate edge cases → classify failures.
 *
 * Reuses v1's compileCpp() and executeProgram() for the actual work.
 */

import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import { TestCase, TestCaseResult, VerificationResult, FailureType, ParsedConstraint } from '../models/problemSpec';
import { compileCpp } from './compiler';
import { executeProgram } from './runner';

/**
 * Verify generated C++ code by compiling and running against test cases.
 *
 * @param code - The C++ source code to verify
 * @param testCases - Test cases to run (parsed examples + generated edge cases)
 * @param timeoutMs - Execution timeout per test case (default 5000ms)
 * @returns VerificationResult with detailed test results
 */
export function verifyCode(code: string, testCases: TestCase[], timeoutMs?: number): VerificationResult {
  const tmpDir = os.tmpdir();
  const baseName = `chup_v2_${Date.now()}_${Math.floor(Math.random() * 1000000)}`;
  const sourcePath = path.join(tmpDir, `${baseName}.cpp`);
  const binaryPath = path.join(tmpDir, baseName);

  try {
    fs.writeFileSync(sourcePath, code, 'utf8');

    // ── Compile ───────────────────────────────────────────────────────────
    const compileResult = compileCpp(sourcePath, binaryPath);
    if (!compileResult.success) {
      return {
        compiled: false,
        compilationErrors: compileResult.errors,
        testResults: [],
        allPassed: false,
        failureType: 'compilation_error',
        summary: `Compilation failed: ${compileResult.errors.join('; ')}`
      };
    }

    // ── Run Tests ─────────────────────────────────────────────────────────
    const testResults: TestCaseResult[] = [];
    let hasTle = false;
    let hasRuntimeError = false;
    let hasWrongAnswer = false;

    for (const testCase of testCases) {
      const execResult = executeProgram(binaryPath, testCase.input, timeoutMs || 5000);

      const timedOut = execResult.timedOut;
      const exitCode = execResult.exitCode;
      const actualOutput = (execResult.stdout || '').trim();
      const runtimeError = !timedOut && exitCode !== 0;

      // Compare output (only if we have expected output and no runtime/timeout issues)
      let passed = false;
      if (!timedOut && !runtimeError && testCase.expectedOutput) {
        passed = compareTokens(testCase.expectedOutput, actualOutput);
      } else if (!timedOut && !runtimeError && !testCase.expectedOutput) {
        // Edge case: no expected output — pass means "didn't crash"
        passed = true;
      }

      if (timedOut) hasTle = true;
      if (runtimeError) hasRuntimeError = true;
      if (!timedOut && !runtimeError && !passed && testCase.expectedOutput) hasWrongAnswer = true;

      testResults.push({
        testCase,
        actualOutput,
        passed,
        timedOut,
        runtimeError,
        exitCode
      });
    }

    // ── Classify Failure ──────────────────────────────────────────────────
    let failureType: FailureType | null = null;
    if (hasTle) failureType = 'tle';
    else if (hasRuntimeError) failureType = 'runtime_error';
    else if (hasWrongAnswer) failureType = 'wrong_answer';

    const allPassed = failureType === null;
    const passCount = testResults.filter(r => r.passed).length;
    const totalCount = testResults.length;

    let summary: string;
    if (allPassed) {
      summary = totalCount > 0
        ? `All ${totalCount} test(s) passed.`
        : 'Compilation successful. No test cases available for verification.';
    } else {
      summary = `${passCount}/${totalCount} test(s) passed. Failure: ${failureType}.`;
    }

    return {
      compiled: true,
      compilationErrors: [],
      testResults,
      allPassed,
      failureType,
      summary
    };
  } finally {
    // Clean up temp files
    try {
      if (fs.existsSync(sourcePath)) fs.unlinkSync(sourcePath);
      if (fs.existsSync(binaryPath)) fs.unlinkSync(binaryPath);
    } catch {
      // Ignore cleanup errors
    }
  }
}

/**
 * Compare expected and actual output using exact token comparison with whitespace normalization.
 * Splits both strings into tokens by whitespace and compares token-by-token.
 */
function compareTokens(expected: string, actual: string): boolean {
  const expectedTokens = expected.trim().split(/\s+/).filter(t => t.length > 0);
  const actualTokens = actual.trim().split(/\s+/).filter(t => t.length > 0);

  if (expectedTokens.length !== actualTokens.length) return false;
  return expectedTokens.every((val, idx) => val === actualTokens[idx]);
}

/**
 * Generate edge case test inputs based on parsed constraints.
 * Edge cases have empty expectedOutput — they're primarily for crash/TLE detection.
 */
export function generateEdgeCases(constraints: ParsedConstraint[]): TestCase[] {
  const edgeCases: TestCase[] = [];
  const sizeVars = new Set(['n', 'm', 'size', 'length', 'len']);

  // Check if we have a size-like constraint
  const sizeConstraint = constraints.find(c =>
    sizeVars.has(c.variable.toLowerCase()) || /^[a-zA-Z]$/.test(c.variable)
  );

  if (!sizeConstraint) return edgeCases;

  // Minimum size
  edgeCases.push({
    input: '1\n1\n',
    expectedOutput: '',
    label: 'edge: minimum size (N=1)'
  });

  // Small size
  edgeCases.push({
    input: '2\n1 2\n',
    expectedOutput: '',
    label: 'edge: small case (N=2)'
  });

  // All equal
  edgeCases.push({
    input: '5\n7 7 7 7 7\n',
    expectedOutput: '',
    label: 'edge: all equal'
  });

  // Sorted ascending
  edgeCases.push({
    input: '5\n1 2 3 4 5\n',
    expectedOutput: '',
    label: 'edge: sorted ascending'
  });

  // Sorted descending
  edgeCases.push({
    input: '5\n5 4 3 2 1\n',
    expectedOutput: '',
    label: 'edge: sorted descending'
  });

  // All zeros
  edgeCases.push({
    input: '3\n0 0 0\n',
    expectedOutput: '',
    label: 'edge: all zeros'
  });

  // Boundary value
  if (sizeConstraint.upperBound <= 100) {
    edgeCases.push({
      input: `1\n${sizeConstraint.upperBound}\n`,
      expectedOutput: '',
      label: `edge: boundary value (${sizeConstraint.upperBound})`
    });
  }

  return edgeCases;
}
