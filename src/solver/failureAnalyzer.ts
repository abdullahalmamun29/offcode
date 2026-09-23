/**
 * CHUP V2 — Failure Analyzer.
 *
 * Rule-based failure diagnosis: examines compilation errors, runtime behavior,
 * and output comparison to determine what went wrong and suggest fixes.
 */

import { VerificationResult, FailureDiagnosis, FailureType, CauseCategory, CorrectionLevel } from '../models/problemSpec';

/**
 * Analyze a verification failure and produce a structured diagnosis.
 *
 * @param verification - The verification result to analyze
 * @returns FailureDiagnosis with cause category, description, and suggested fix. Null if all passed.
 */
export function analyzeFailure(verification: VerificationResult): FailureDiagnosis | null {
  if (verification.allPassed) return null;

  const { failureType, compilationErrors, testResults } = verification;

  // ── Compilation Errors ──────────────────────────────────────────────────
  if (failureType === 'compilation_error' && compilationErrors.length > 0) {
    const errorMsg = compilationErrors.join('\n').toLowerCase();

    if (errorMsg.includes('overflow') || errorMsg.includes('truncation') || errorMsg.includes('narrowing')) {
      return {
        failureType: 'compilation_error',
        causeCategory: 'code_level',
        description: 'Compiler detected integer overflow, truncation, or narrowing conversion.',
        suggestedFix: 'Widen integer type: int → long long',
        correctionLevel: 1
      };
    }
    if (errorMsg.includes('undeclared') || errorMsg.includes('not declared')) {
      return {
        failureType: 'compilation_error',
        causeCategory: 'code_level',
        description: 'Undeclared identifier or missing include.',
        suggestedFix: 'Missing variable declaration or include',
        correctionLevel: 1
      };
    }
    if (errorMsg.includes('expected')) {
      return {
        failureType: 'compilation_error',
        causeCategory: 'code_level',
        description: 'Syntax error detected by compiler.',
        suggestedFix: 'Syntax error — check braces, semicolons',
        correctionLevel: 1
      };
    }
    return {
      failureType: 'compilation_error',
      causeCategory: 'code_level',
      description: `Compilation failed: ${compilationErrors[0]}`,
      suggestedFix: 'Review compilation errors',
      correctionLevel: 1
    };
  }

  // ── Runtime Errors ──────────────────────────────────────────────────────
  if (failureType === 'runtime_error') {
    const failingResult = testResults.find(r => r.runtimeError);
    if (failingResult) {
      if (failingResult.exitCode === 139) {
        return {
          failureType: 'runtime_error',
          causeCategory: 'code_level',
          description: 'SIGSEGV (segmentation fault): accessing invalid memory.',
          suggestedFix: 'Segmentation fault — check array bounds and null pointers',
          correctionLevel: 1
        };
      }
      if (failingResult.exitCode === 134) {
        return {
          failureType: 'runtime_error',
          causeCategory: 'code_level',
          description: 'SIGABRT: likely assertion failure or out-of-range container access.',
          suggestedFix: 'Abort — likely assertion failure or out-of-range access',
          correctionLevel: 1
        };
      }
      return {
        failureType: 'runtime_error',
        causeCategory: 'code_level',
        description: `Process exited with code ${failingResult.exitCode}.`,
        suggestedFix: 'Runtime error — check edge cases and bounds',
        correctionLevel: 1
      };
    }
  }

  // ── TLE ─────────────────────────────────────────────────────────────────
  if (failureType === 'tle') {
    return {
      failureType: 'tle',
      causeCategory: 'algorithm',
      description: 'Execution timed out. The algorithm is too slow for the given constraints.',
      suggestedFix: 'Algorithm too slow for constraints. Try next viable approach.',
      correctionLevel: 3
    };
  }

  // ── Wrong Answer ────────────────────────────────────────────────────────
  if (failureType === 'wrong_answer') {
    const failingResult = testResults.find(r => !r.passed && !r.timedOut && !r.runtimeError);

    if (failingResult) {
      // No output produced
      if (!failingResult.actualOutput || failingResult.actualOutput.trim() === '') {
        return {
          failureType: 'wrong_answer',
          causeCategory: 'code_level',
          description: 'No output was produced. The program may have terminated before printing.',
          suggestedFix: 'No output produced. Check I/O logic.',
          correctionLevel: 1
        };
      }

      // Token comparison for off-by-one detection
      const expected = failingResult.testCase.expectedOutput.trim().split(/\s+/).filter(t => t.length > 0);
      const actual = failingResult.actualOutput.trim().split(/\s+/).filter(t => t.length > 0);

      if (Math.abs(expected.length - actual.length) <= 1 && expected.length > 0) {
        let diffCount = 0;
        const minLen = Math.min(expected.length, actual.length);
        for (let i = 0; i < minLen; i++) {
          if (expected[i] !== actual[i]) diffCount++;
        }
        if (diffCount === 1) {
          return {
            failureType: 'wrong_answer',
            causeCategory: 'template_parameter',
            description: `Single token differs: expected "${expected.find((v, i) => v !== actual[i])}", got "${actual.find((v, i) => v !== expected[i])}".`,
            suggestedFix: 'Possible off-by-one error. Check loop bounds and comparisons.',
            correctionLevel: 2
          };
        }
      }

      // Integer overflow detection
      const hasLargeNumber = actual.some(token => {
        const num = Number(token);
        return !isNaN(num) && Math.abs(num) > 2147483647;
      });
      if (hasLargeNumber) {
        return {
          failureType: 'wrong_answer',
          causeCategory: 'code_level',
          description: 'Output contains values exceeding INT_MAX, suggesting integer overflow.',
          suggestedFix: 'Integer overflow detected. Use long long.',
          correctionLevel: 1
        };
      }
    }

    // Default wrong answer
    return {
      failureType: 'wrong_answer',
      causeCategory: 'template_parameter',
      description: 'Output does not match expected. Algorithm logic may be incorrect.',
      suggestedFix: 'Wrong answer. Review algorithm logic.',
      correctionLevel: 2
    };
  }

  return null;
}
