/**
 * CHUP V2 — Generic Problem Parser with Source-Specific Heuristics.
 *
 * Parses normalized problem text into a StructuredProblem representation.
 * Currently supports Codeforces-format detection with generic fallback.
 * Architecture supports adding more source adapters later.
 */

import { StructuredProblem, ParsedConstraint, TestCase, NormalizedInput } from '../models/problemSpec';
import { normalizeInputUniversal } from './universalNormalizer';
import { canonicalize } from './canonicalizer';
import { extractSemanticInput } from './semanticExtractor';

/**
 * Parse normalized text into a structured problem representation.
 *
 * @param normalizedText - The cleaned/normalized text
 * @param rawText - The original raw text (preserved in output)
 * @param normalizedInput - Optional pre-computed NormalizedInput
 * @returns A StructuredProblem with all extractable fields populated
 */
export function parseProblem(normalizedText: string, rawTextOrNormalizedInput: string | NormalizedInput, normalizedInput?: NormalizedInput): StructuredProblem {
  let rawText: string;
  let normInput: NormalizedInput;
  if (typeof rawTextOrNormalizedInput === 'object' && rawTextOrNormalizedInput !== null) {
    normInput = rawTextOrNormalizedInput;
    rawText = normInput.originalText;
  } else {
    rawText = rawTextOrNormalizedInput || normalizedText;
    normInput = normalizedInput || normalizeInputUniversal(rawText);
  }
  const isCodeforces = /time\s*limit/i.test(normalizedText) ||
                       /memory\s*limit/i.test(normalizedText) ||
                       /examples?[\s:]*\n\s*input/i.test(normalizedText) ||
                       /^[A-Z]\.\s+/m.test(normalizedText);

  const constraints = extractConstraints(normalizedText);
  const timeLimit = extractTimeLimit(normalizedText);
  const memoryLimit = extractMemoryLimit(normalizedText);

  if (isCodeforces) {
    return parseCodeforces(normalizedText, rawText, constraints, timeLimit, memoryLimit, normInput);
  }

  return parseGeneric(normalizedText, rawText, constraints, timeLimit, memoryLimit, normInput);
}

// ═══════════════════════════════════════════════════════════════════════════════
// Codeforces Format Parser
// ═══════════════════════════════════════════════════════════════════════════════

function parseCodeforces(
  text: string, rawText: string,
  constraints: ParsedConstraint[],
  timeLimit: number | null,
  memoryLimit: number | null,
  normInput?: NormalizedInput
): StructuredProblem {
  const lines = text.split('\n');

  // Title: first non-empty line
  let title: string | null = null;
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.length > 0) {
      title = trimmed;
      break;
    }
  }

  const sectionPattern = /^\s*(Sample\s+Input|Sample\s+Output|Sample\s+InputCopy|Sample\s+OutputCopy|InputCopy|OutputCopy|Input|Output|Examples?|Note|Warning|Constraints?)\s*[:?!]*\s*$/im;
  const sections: { heading: string; content: string }[] = [];
  let currentHeading = 'header';
  let currentContent: string[] = [];

  for (const line of lines) {
    const match = line.match(sectionPattern);
    if (match) {
      sections.push({
        heading: currentHeading.toLowerCase(),
        content: currentContent.join('\n').trim()
      });
      currentHeading = match[1].trim().toLowerCase();
      currentContent = [];
    } else {
      currentContent.push(line);
    }
  }
  // Push last section
  sections.push({
    heading: currentHeading.toLowerCase(),
    content: currentContent.join('\n').trim()
  });

  // Extract statement, input spec, output spec, examples, notes
  let statement = '';
  let inputSpec: string | null = null;
  let outputSpec: string | null = null;
  const examples: TestCase[] = [];
  let notes: string | null = null;

  let inExamples = false;
  let currentExampleInput = '';
  let exampleCount = 0;

  for (const section of sections) {
    const heading = section.heading;
    const content = section.content;

    if (heading === 'header') {
      statement += cleanStatement(content) + '\n';
      continue;
    }

    if (heading === 'examples' || heading === 'example') {
      inExamples = true;
      continue;
    }

    if (heading.startsWith('constraint')) {
      continue;
    }

    if (heading === 'note' || heading === 'warning') {
      notes = (notes ? notes + '\n' : '') + content;
      continue;
    }

    if (heading === 'inputcopy' || heading.includes('sample input')) {
      currentExampleInput = content;
      continue;
    } else if (heading === 'outputcopy' || heading.includes('sample output')) {
      exampleCount++;
      let cleanOutput = content;
      const noteIdx = cleanOutput.search(/\b(?:note|warning|explanation)\b[:!\s]/i);
      if (noteIdx !== -1) {
        notes = cleanOutput.substring(noteIdx).trim();
        cleanOutput = cleanOutput.substring(0, noteIdx).trim();
      }
      examples.push({
        input: currentExampleInput,
        expectedOutput: cleanOutput,
        label: `example ${exampleCount}`
      });
      continue;
    }

    if (inExamples) {
      // Inside examples section: Input/Output are example I/O pairs
      if (heading === 'input') {
        currentExampleInput = content;
      } else if (heading === 'output') {
        exampleCount++;
        // If content has "Note: ...", extract it
        let cleanOutput = content;
        const noteIdx = cleanOutput.search(/\b(?:note|warning|explanation)\b[:!\s]/i);
        if (noteIdx !== -1) {
          notes = cleanOutput.substring(noteIdx).trim();
          cleanOutput = cleanOutput.substring(0, noteIdx).trim();
        }
        examples.push({
          input: currentExampleInput,
          expectedOutput: cleanOutput,
          label: `example ${exampleCount}`
        });
      }
    } else {
      // Before examples: Input/Output are main specs
      if (heading === 'input') {
        inputSpec = content || null;
      } else if (heading === 'output') {
        outputSpec = content || null;
      }
    }
  }

  // Fallback: If no examples parsed via sections, try generic regex
  if (examples.length === 0) {
    const fallbackExamples = parseGenericExamples(text);
    examples.push(...fallbackExamples);
  }

  // Calculate parser confidence
  let confidence = 0.3;
  if (title) confidence += 0.10;
  if (timeLimit !== null) confidence += 0.10;
  if (inputSpec) confidence += 0.15;
  if (outputSpec) confidence += 0.10;
  if (examples.length > 0) confidence += 0.15;
  if (constraints.length > 0) confidence += 0.10;
  confidence = Math.min(confidence, 1.0);

  const canonicalized = normInput ? canonicalize(normInput) : undefined;
  const semantic = canonicalized ? extractSemanticInput(canonicalized) : undefined;

  return {
    rawText,
    normalizedText: text,
    title,
    problemType: null,  // Set by classifier
    domain: null,
    statement,
    inputSpecification: inputSpec,
    outputSpecification: outputSpec,
    constraints,
    examples,
    notes,
    timeLimit,
    memoryLimit,
    source: 'codeforces',
    parserConfidence: Math.round(confidence * 100) / 100,
    normalizedInput: normInput,
    canonicalizedInput: canonicalized,
    semanticInput: semantic
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Generic Format Parser (Fallback)
// ═══════════════════════════════════════════════════════════════════════════════

function parseGeneric(
  text: string, rawText: string,
  constraints: ParsedConstraint[],
  timeLimit: number | null,
  memoryLimit: number | null,
  normInput?: NormalizedInput
): StructuredProblem {
  const lines = text.split('\n');

  // Title: first non-empty line if it's short
  let title: string | null = null;
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.length > 0 && trimmed.length < 100) {
      title = trimmed;
      break;
    }
  }

  // Try to find Sample Input / Sample Output or Input: / Output:
  const examples = parseGenericExamples(text);

  let confidence = 0.15;
  if (title) confidence += 0.05;
  if (examples.length > 0) confidence += 0.15;
  if (constraints.length > 0) confidence += 0.10;
  confidence = Math.min(confidence, 1.0);

  const canonicalized = normInput ? canonicalize(normInput) : undefined;
  const semantic = canonicalized ? extractSemanticInput(canonicalized) : undefined;

  return {
    rawText,
    normalizedText: text,
    title,
    problemType: null,
    domain: null,
    statement: text,
    inputSpecification: null,
    outputSpecification: null,
    constraints,
    examples,
    notes: null,
    timeLimit,
    memoryLimit,
    source: 'generic',
    parserConfidence: Math.round(confidence * 100) / 100,
    normalizedInput: normInput,
    canonicalizedInput: canonicalized,
    semanticInput: semantic
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Helpers
// ═══════════════════════════════════════════════════════════════════════════════

/** Extract time limit in seconds from text. */
function extractTimeLimit(text: string): number | null {
  const match = text.match(/(?:time\s*limit|time)(?:\s*per\s*test)?[:\s=]*(\d+(?:\.\d+)?)\s*(?:s|sec|second[s]?)/i);
  if (match) return parseFloat(match[1]);
  return null;
}

/** Extract memory limit in MB from text. */
function extractMemoryLimit(text: string): number | null {
  const match = text.match(/(?:memory\s*limit|memory)(?:\s*per\s*test)?[:\s=]*(\d+)\s*(?:mb|megabyte[s]?)/i);
  if (match) return parseInt(match[1], 10);
  return null;
}

/** Extract numeric constraints from text. */
function extractConstraints(text: string): ParsedConstraint[] {
  const constraints: ParsedConstraint[] = [];
  const seen = new Set<string>();

  // Full range: 1 ≤ n, m ≤ 10^5 or 1 <= n <= 200000
  const fullRangeRegex = /(\d+)\s*(?:≤|<=)\s*([a-zA-Z_]\w*(?:\s*,\s*[a-zA-Z_]\w*)*)\s*(?:≤|<=)\s*(\d+\s*[*×·]\s*10\s*\^\s*\d+|\d+\s*\^\s*\d+|\d+(?:[eE][+-]?\d+)|\d+)/g;
  let match: RegExpExecArray | null;

  while ((match = fullRangeRegex.exec(text)) !== null) {
    const lower = parseInt(match[1], 10);
    const varsStr = match[2];
    const upperStr = match[3];
    const upper = parseNumericBound(upperStr);

    const vars = varsStr.split(/\s*,\s*/);
    for (const v of vars) {
      const variable = v.trim();
      const key = `${variable}:${upper}`;
      if (!seen.has(key) && variable.length > 0) {
        seen.add(key);
        constraints.push({
          variable,
          upperBound: upper,
          lowerBound: lower,
          raw: match[0]
        });
      }
    }
  }

  // Upper bound inequality: var <= bound (e.g., n <= 200000, a_i <= 10^9)
  const upperRegex = /\b([a-zA-Z_]\w*)\s*(?:≤|<=)\s*(\d+\s*[*×·]\s*10\s*\^\s*\d+|\d+\s*\^\s*\d+|\d+(?:[eE][+-]?\d+)|\d+)/g;
  while ((match = upperRegex.exec(text)) !== null) {
    const variable = match[1];
    const upperStr = match[2];
    const upper = parseNumericBound(upperStr);
    const key = `${variable}:${upper}`;

    const skipWords = new Set(['time', 'memory', 'limit', 'second', 'megabyte', 'test', 'the', 'and', 'for', 'with']);
    if (!seen.has(key) && !skipWords.has(variable.toLowerCase())) {
      seen.add(key);
      constraints.push({
        variable,
        upperBound: upper,
        raw: match[0]
      });
    }
  }

  // Explicit equality: N=200000, T=1, N = 1000
  const eqRegex = /\b([a-zA-Z_]\w*)\s*=\s*(\d+\s*[*×·]\s*10\s*\^\s*\d+|\d+\s*\^\s*\d+|\d+(?:[eE][+-]?\d+)|\d+)/g;
  while ((match = eqRegex.exec(text)) !== null) {
    const variable = match[1];
    const upperStr = match[2];
    const upper = parseNumericBound(upperStr);
    const key = `${variable}:${upper}`;

    const skipWords = new Set(['time', 'sec', 'second', 'seconds', 'memory', 'mb', 'megabyte', 'limit', 'test']);
    if (!seen.has(key) && !skipWords.has(variable.toLowerCase())) {
      seen.add(key);
      constraints.push({
        variable,
        upperBound: upper,
        raw: match[0]
      });
    }
  }

  // "n up to 2e5" or "n up to 200000"
  const upToRegex = /\b([a-zA-Z_]\w*)\s*up\s*to\s*(\d+\s*[*×·]\s*10\s*\^\s*\d+|\d+\s*\^\s*\d+|\d+(?:[eE][+-]?\d+)|\d+)/gi;
  while ((match = upToRegex.exec(text)) !== null) {
    const variable = match[1];
    const upperStr = match[2];
    const upper = parseNumericBound(upperStr);
    const key = `${variable}:${upper}`;

    if (!seen.has(key)) {
      seen.add(key);
      constraints.push({
        variable,
        upperBound: upper,
        raw: match[0]
      });
    }
  }

  return constraints;
}

/** Parse a numeric bound string like "200000", "2*10^5", "10^9", "2e5". */
function parseNumericBound(str: string): number {
  const cleaned = str.replace(/\s/g, '');

  // Pattern: coefficient * 10^exponent (e.g., "2*10^5", "2×10^5") or "10^9"
  const sciMatch = cleaned.match(/^(\d+)?[*×·]?10\^(\d+)$/);
  if (sciMatch) {
    const coeff = sciMatch[1] ? parseInt(sciMatch[1], 10) : 1;
    const exp = parseInt(sciMatch[2], 10);
    return coeff * Math.pow(10, exp);
  }

  // base^exp (e.g. 2^10)
  const caretMatch = cleaned.match(/^(\d+)\^(\d+)$/);
  if (caretMatch) {
    return Math.pow(parseInt(caretMatch[1], 10), parseInt(caretMatch[2], 10));
  }

  // Plain number or scientific notation (2e5)
  const num = Number(cleaned);
  return isNaN(num) ? 0 : num;
}

/**
 * Parse examples from generic format text.
 * Looks for "Sample Input" / "Sample Output" or "Input:" / "Output:" patterns.
 */
function parseGenericExamples(text: string): TestCase[] {
  const examples: TestCase[] = [];
  let match: RegExpExecArray | null;
  let count = 0;

  // Try Codeforces browser copy "InputCopy ... OutputCopy"
  const cfPattern = /InputCopy[\s\t]+OutputCopy\s*\n+([\s\S]*?)\n+[\t ]+\n+([\s\S]*?)(?=\n*InputCopy|$|\n*(?:Note|Warning|Explanation))/gi;
  while ((match = cfPattern.exec(text)) !== null) {
    count++;
    let expectedOutput = match[2].trim();
    const noteIdx = expectedOutput.search(/\b(?:note|warning|explanation)\b[:!\s]/i);
    if (noteIdx !== -1) {
      expectedOutput = expectedOutput.substring(0, noteIdx).trim();
    }
    examples.push({
      input: match[1].trim(),
      expectedOutput,
      label: `example ${count}`
    });
  }

  if (examples.length > 0) return examples;

  // Try sequential "InputCopy ... OutputCopy" (AOJ, AtCoder)
  const aojPattern = /InputCopy\s*\n+([\s\S]*?)\n+OutputCopy\s*\n+([\s\S]*?)(?=\n*InputCopy|$|\n*(?:Note|Explanation|Warning))/gi;
  while ((match = aojPattern.exec(text)) !== null) {
    count++;
    let expectedOutput = match[2].trim();
    const noteIdx = expectedOutput.search(/\b(?:note|warning|explanation)\b[:!\s]/i);
    if (noteIdx !== -1) {
      expectedOutput = expectedOutput.substring(0, noteIdx).trim();
    }
    examples.push({
      input: match[1].trim(),
      expectedOutput,
      label: `example ${count}`
    });
  }

  if (examples.length > 0) return examples;

  // Try "Sample Input" / "Sample Output"
  const samplePattern = /sample\s*input\s*[:\n]\s*([\s\S]*?)sample\s*output\s*[:\n]\s*([\s\S]*?)(?=sample\s*input|$)/gi;

  while ((match = samplePattern.exec(text)) !== null) {
    count++;
    examples.push({
      input: match[1].trim(),
      expectedOutput: match[2].trim(),
      label: `sample ${count}`
    });
  }

  if (examples.length > 0) return examples;

  // Try "Input:" / "Output:" (less reliable)
  const ioPattern = /\binput\s*:\s*([\s\S]*?)\boutput\s*:\s*([\s\S]*?)(?=\binput\s*:|\bconstraints?\s*:|$)/gi;
  while ((match = ioPattern.exec(text)) !== null) {
    count++;
    examples.push({
      input: match[1].trim(),
      expectedOutput: match[2].trim(),
      label: `example ${count}`
    });
  }

  return examples;
}

/** Remove time/memory limit lines and title from statement text. */
function cleanStatement(text: string): string {
  return text
    .replace(/(?:time\s*limit|time).*?(?:second[s]?|sec|s)\n?/gi, '')
    .replace(/(?:memory\s*limit|memory).*?(?:megabyte[s]?|mb)\n?/gi, '')
    .trim();
}
