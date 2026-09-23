import { SolverResult, VerificationResult, FailureDiagnosis, CorrectionAttempt, CorrectionLevel, TopicCandidate } from '../models/problemSpec';
import { analyzeFailure } from './failureAnalyzer';

/**
 * Applies a correction to the code based on the failure diagnosis.
 * @param code The original code.
 * @param diagnosis The failure diagnosis.
 * @returns The corrected code and fix description, or null if no correction is applicable.
 */
export function applyCorrection(code: string, diagnosis: FailureDiagnosis): { correctedCode: string; fixDescription: string } | null {
  if (!diagnosis) return null;

  let newCode = code;
  let fixApplied = false;
  let fixDescription = '';

  if (diagnosis.correctionLevel === 1) {
    if (diagnosis.suggestedFix.includes('Widen integer type') || diagnosis.suggestedFix.includes('Integer overflow')) {
      const regex = /\b(int)\s+(sum|result|ans|answer|count|total|maxVal|minVal|res)\b/g;
      if (regex.test(newCode)) {
        newCode = newCode.replace(regex, 'long long $2');
        newCode = newCode.replace(/long long\s+main\s*\(/g, 'int main(');
        fixApplied = true;
        fixDescription = 'Widened commonly overflowed integer variables to long long.';
      }
    }

    if (diagnosis.suggestedFix.includes('No output produced') || diagnosis.suggestedFix.includes('Missing variable declaration')) {
      if (newCode.includes('cout <<') && !newCode.includes('endl') && !newCode.includes('\\n')) {
        const coutRegex = /(cout\s*<<.*?;)/g;
        newCode = newCode.replace(coutRegex, (match) => {
          if (match.includes('endl') || match.includes('\\n')) return match;
          return match.replace(/;$/, ' << endl;');
        });
        fixApplied = true;
        fixDescription = 'Added missing endl to cout statements.';
      }
    }

    if (diagnosis.suggestedFix.includes('Segmentation fault')) {
      if (newCode.includes('[') && newCode.includes(']')) {
        fixApplied = true;
        fixDescription = 'Noted segmentation fault. Auto-fix for array bounds is not safe, requires manual review.';
        newCode = '// FIXME: Check array bounds and null pointers here to avoid SIGSEGV\n' + newCode;
      }
    }
  }

  if (diagnosis.correctionLevel === 2) {
    if (diagnosis.suggestedFix.includes('off-by-one')) {
      // Count how many loop bounds would change — only apply if exactly one
      // Changing ALL < n to <= n in multi-loop code causes subtle bugs
      const ltCount = (newCode.match(/< n\b/g) || []).length;
      const leCount = (newCode.match(/<= n\b/g) || []).length;
      if (newCode.includes('< n') && ltCount === 1) {
        newCode = newCode.replace(/< n\b/, '<= n');
        fixApplied = true;
        fixDescription = 'Changed < n to <= n to attempt fixing off-by-one error.';
      } else if (newCode.includes('<= n') && leCount === 1) {
        newCode = newCode.replace(/<= n\b/, '< n');
        fixApplied = true;
        fixDescription = 'Changed <= n to < n to attempt fixing off-by-one error.';
      }
    }

    if (newCode.includes('int maxVal = 0') || newCode.includes('int minVal = 0')) {
      newCode = newCode.replace(/int\s+maxVal\s*=\s*0/g, 'int maxVal = INT_MIN');
      newCode = newCode.replace(/int\s+minVal\s*=\s*0/g, 'int minVal = INT_MAX');
      if (!newCode.includes('<climits>')) {
        newCode = '#include <climits>\n' + newCode;
      }
      fixApplied = true;
      fixDescription = 'Fixed initialization of min/max values to use INT_MAX/INT_MIN.';
    }

    const inputRegex = /cin\s*>>\s*n\s*;/;
    if (inputRegex.test(newCode) && !newCode.includes('if (n == 0)')) {
      newCode = newCode.replace(inputRegex, 'cin >> n;\n    if (n == 0) { cout << 0 << endl; return 0; }');
      fixApplied = true;
      fixDescription = 'Added empty input guard for n == 0.';
    }
  }

  if (diagnosis.correctionLevel === 3) {
    return null;
  }

  if (fixApplied && newCode !== code) {
    return {
      correctedCode: newCode,
      fixDescription
    };
  }

  return null;
}
