/**
 * CHUP V2 — Input Normalizer.
 *
 * Rule-based text cleaning for problem statements.
 * Normalizes Unicode, collapses blank lines, removes duplicate lines,
 * while preserving code blocks and I/O example blocks.
 */

import { normalizeInputUniversal } from './universalNormalizer';

/**
 * Normalize raw problem text into a clean, consistent format.
 * Delegates to normalizeInputUniversal for single-line queries and commands,
 * while preserving multi-line structural formatting (fenced code, I/O tables) for CP problems.
 *
 * @param rawText - The raw text pasted by the user
 * @returns Cleaned text ready for parsing
 */
export function normalizeInput(rawText: string): string {
  const norm = normalizeInputUniversal(rawText);

  // If query is a plain natural language instruction without newlines and without math constraints/formulas,
  // return universal normalizer's cleaned prose directly:
  if (!rawText.includes('\n') && !/[=<>[\]{}]/.test(rawText)) {
    return norm.normalizedText;
  }

  // Otherwise, apply high-confidence word replacements to rawText while preserving structural formatting:
  let text = rawText;
  if (norm.corrections.length > 0) {
    for (const corr of norm.corrections) {
      const regex = new RegExp(`\\b${corr.original}\\b`, 'g');
      text = text.replace(regex, corr.corrected);
    }
  }

  // ── Step 1: Unicode normalization ───────────────────────────────────────
  text = text
    .replace(/[\u2018\u2019\u201C\u201D]/g, "'")   // smart quotes → ASCII
    .replace(/\u2014/g, '--')                        // em-dash
    .replace(/\u2026/g, '...')                       // ellipsis
    .replace(/\u00A0/g, ' ')                         // non-breaking space
    .replace(/[\u2010\u2011\u2012\u2013\u2015\u2212]/g, '-') // various dashes & unicode minus
    .replace(/\u200B/gi, '')                         // zero-width space
    .replace(/≤/g, '<=')
    .replace(/≥/g, '>=')
    .replace(/\b([a-zA-Z])\1\b/g, '$1')              // KaTeX duplicated single-letter math variables (nn -> n, mm -> m, etc.)
    .replace(/([a-zA-Z0-9]+(?:\s*[-+*/]\s*[a-zA-Z0-9]+)+)\1/g, '$1') // KaTeX duplicated expressions (x-kx-k -> x-k)
    .replace(/(\d)\u2009(\d{3})/g, '$1$2')          // thin-space in thousands: 300 000 -> 300000
    .replace(/(\d),(\d{3})/g, '$1$2')                // commas in thousands: 200,000 -> 200000
    .replace(/\u2009/g, ' ')                         // remaining thin spaces -> space
    .replace(/(\d+)\s*[×⋅*]\s*10\^?(\d+)/g, (_m, a, b) => String(Number(a) * Math.pow(10, Number(b))))
    .replace(/(\d+)\s*[×⋅*]\s*10(\d)/g, (_m, a, b) => String(Number(a) * Math.pow(10, Number(b))));

  // ── Step 1.2: HackerRank two-column STDIN / Function tables ─────────────
  text = text.replace(/STDIN\s+Function\s*\n[- \t]+\n([\s\S]*?)(?=\n\s*(?:Sample\s+Output|Output|Explanation)|$)/gi, (_m, tableContent) => {
    const tLines = tableContent.split('\n');
    const dataLines: string[] = [];
    for (const tLine of tLines) {
      const trimmed = tLine.trim();
      if (!trimmed || /^(?:STDIN|-----)/i.test(trimmed)) continue;
      const firstToken = trimmed.split(/\s{2,}|\t/)[0].trim();
      if (firstToken) dataLines.push(firstToken);
    }
    return dataLines.join('\n') + '\n';
  });

  // ── Step 1.5: Browser table normalization (Codeforces, HackerRank, SPOJ) ─
  text = text.replace(/InputCopy[\s\t]+OutputCopy\s*\n+([\s\S]*?)\n+[\t ]+\n+([\s\S]*?)(?=\n*InputCopy|$|\n*(?:Note|Explanation|Warning))/gi, (_m, inp, out) => {
    let cleanInp = inp.trim();
    if (/STDIN\s+Function/i.test(cleanInp)) {
      const tLines = cleanInp.split('\n');
      const dataLines: string[] = [];
      for (const tLine of tLines) {
        const trimmed = tLine.trim();
        if (/^(?:STDIN|-----)/i.test(trimmed) || !trimmed) continue;
        const firstToken = trimmed.split(/\s{2,}|\t/)[0].trim();
        if (firstToken) dataLines.push(firstToken);
      }
      cleanInp = dataLines.join('\n');
    }
    return `\nInput:\n${cleanInp.trim()}\nOutput:\n${out.trim()}\n`;
  });

  // ── Step 2: Line-by-line processing ─────────────────────────────────────
  const lines = text.split('\n');
  const processedLines: string[] = [];

  let inFencedBlock = false;
  let inIOBlock = false;
  let previousLine: string | null = null;

  for (const rawLine of lines) {
    const trimmed = rawLine.trim();

    // Strip Plain text artifacts from HackerEarth/CodeChef
    if (/^\s*plain\s*text\s*$/i.test(trimmed)) {
      continue;
    }

    // Track fenced code blocks
    if (trimmed.startsWith('```')) {
      inFencedBlock = !inFencedBlock;
    }

    // Track I/O and example blocks to preserve all duplicate lines in test data
    if (/^(?:examples?|sample\s*input|sample\s*output|input\b|output\b|inputcopy)/i.test(trimmed)) {
      inIOBlock = true;
    }

    // Normalize tabs and trailing whitespace
    let line = rawLine.replace(/\t/g, '    ');
    line = line.replace(/\s+$/, '');

    // MathJax halved line deduplication (e.g. 1≤n≤2⋅1051≤n≤2⋅105 -> 1≤n≤2⋅105)
    const lineTrimmed = line.trim();
    if (lineTrimmed.length >= 6 && lineTrimmed.length % 2 === 0 && /[≤≥<>=^]|\b10\b/i.test(lineTrimmed) && !/[_()[\]{}]/.test(lineTrimmed)) {
      const mid = lineTrimmed.length / 2;
      if (lineTrimmed.substring(0, mid) === lineTrimmed.substring(mid)) {
        line = lineTrimmed.substring(0, mid);
      }
    }

    // Skip exact duplicate consecutive lines in prose (not inside code blocks, I/O blocks, or numeric data)
    const isNumericData = /^\s*[\d\s.-]+\s*$/.test(line);
    if (!inFencedBlock && !inIOBlock && !isNumericData && line === previousLine && line !== '') {
      continue;
    }

    processedLines.push(line);
    previousLine = line;
  }

  // ── Step 3: Post-process — collapse 3+ consecutive blank lines to 2 ────
  const finalLines: string[] = [];
  let consecutiveBlanks = 0;

  for (const line of processedLines) {
    if (line === '') {
      consecutiveBlanks++;
      if (consecutiveBlanks > 2) {
        continue; // Drop blanks beyond 2 in a row
      }
    } else {
      consecutiveBlanks = 0;
    }
    finalLines.push(line);
  }

  return finalLines.join('\n');
}

export { normalizeInputUniversal } from './universalNormalizer';
