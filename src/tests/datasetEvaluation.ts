/**
 * Comprehensive Test Runner for chup_v2_test_dataset.jsonl
 */

import * as fs from 'fs';
import * as path from 'path';
import { normalizeInput } from '../pipeline/inputNormalizer';
import { parseProblem } from '../pipeline/problemParser';
import { classifyProblem } from '../pipeline/problemClassifier';
import { analyzeConstraints } from '../pipeline/constraintAnalyzer';
import { scoreConcepts, getConceptById } from '../knowledge/dsaKnowledge';
import { solveCpProblem } from '../solver/cpSolver';
import { buildFromTemplate } from '../solver/solutionTemplates';

interface DatasetItem {
  id: string;
  category: string;
  difficulty: string;
  input: string;
  expected: any;
  checks: string[];
}

export interface TestResult {
  id: string;
  category: string;
  status: 'PASS' | 'FAIL' | 'WARN';
  details: string;
}

export async function runDatasetEvaluation(): Promise<{ passed: number; failed: number; results: TestResult[] }> {
  // Check workspace first, then fallback to Downloads
  let datasetPath = path.resolve(__dirname, '../../chup_v2_test_dataset.jsonl');
  if (!fs.existsSync(datasetPath)) {
    datasetPath = '/home/jobayer/Downloads/chup_v2_test_dataset.jsonl';
  }

  if (!fs.existsSync(datasetPath)) {
    console.error('Dataset not found at:', datasetPath);
    return { passed: 0, failed: 1, results: [] };
  }

  const rawLines = fs.readFileSync(datasetPath, 'utf8').trim().split('\n');
  const items: DatasetItem[] = rawLines.map(l => JSON.parse(l));

  console.log(`\n======================================================`);
  console.log(`   Running CHUP v2 Test Dataset (${items.length} test cases)`);
  console.log(`======================================================\n`);

  const results: TestResult[] = [];

  for (const item of items) {
    try {
      const normalized = normalizeInput(item.input);
      const parsed = parseProblem(normalized, item.input);
      const classification = classifyProblem(parsed);
      const topics = scoreConcepts(parsed);
      const feasibility = analyzeConstraints(parsed);

      let passed = true;
      let reasons: string[] = [];

      // ── UI routing tests ───────────────────────────────────────────────
      if (item.id.startsWith('UI-')) {
        const expectedRoute = item.expected.route;
        if (expectedRoute) {
          const actualRoute = classification.selected;
          const match = (expectedRoute === 'debug' && actualRoute === 'code_debug') ||
                        (expectedRoute === 'academic' && actualRoute === 'academic') ||
                        (expectedRoute === 'template_match' && actualRoute === 'template_match') ||
                        (expectedRoute === 'competitive_programming' && actualRoute === 'competitive_programming');
          if (!match) {
            passed = false;
            reasons.push(`Route mismatch: expected ${expectedRoute}, got ${actualRoute}`);
          }
        }
        if (item.expected.likely_topic) {
          const expectedTopics = item.expected.likely_topic;
          const topCandidate = topics.find(t => !t.rejected);
          const topTopic = topCandidate?.conceptId || topics[0]?.conceptId;
          const inTop3 = topics.slice(0, 3).some(t => expectedTopics.includes(t.conceptId));
          if (!inTop3) {
            passed = false;
            reasons.push(`Top topic mismatch: expected one of ${expectedTopics}, top: ${topTopic}`);
          }
        }
        if (item.expected.examples_must_be_parsed) {
          if (parsed.examples.length === 0) {
            passed = false;
            reasons.push(`Expected examples to be parsed, got 0`);
          }
        }
      }

      // ── CP solving & topic matching tests ──────────────────────────────
      else if (item.id.startsWith('CP-')) {
        const expectedTopic = item.expected.topic;
        const topCandidate = topics.find(t => !t.rejected);
        const topId = topCandidate?.conceptId || topics[0]?.conceptId;

        if (expectedTopic && topId !== expectedTopic) {
          passed = false;
          reasons.push(`Topic mismatch: expected ${expectedTopic}, top detected: ${topId} (top: ${topics.slice(0, 3).map(t => `${t.conceptId}:${t.confidence}${t.rejected ? '(REJ)' : ''}`).join(', ')})`);
        }

        if (item.expected.must_reject) {
          const sw = topics.find(t => t.conceptId === 'sliding_window');
          if (sw && !sw.rejected && sw.confidence >= (topCandidate?.confidence || 0)) {
            passed = false;
            reasons.push(`Expected sliding_window to be rejected, but confidence was ${sw.confidence}`);
          }
        }

        if (item.expected.must_not_prefer) {
          const demoted = topics.find(t => t.conceptId === item.expected.must_not_prefer);
          if (demoted && !demoted.rejected && demoted.confidence >= (topCandidate?.confidence || 0)) {
            passed = false;
            reasons.push(`Expected not to prefer ${item.expected.must_not_prefer}`);
          }
        }

        // Test compilation of the template
        if (item.expected.template) {
          const frag = buildFromTemplate(item.expected.template, { intType: feasibility.overflowRisk ? 'long long' : 'int' });
          if (!frag) {
            passed = false;
            reasons.push(`Template ${item.expected.template} failed to build`);
          }
        }
      }

      // ── Recognized-only tests ──────────────────────────────────────────
      else if (item.id.startsWith('UN-') || item.id.startsWith('HL-')) {
        const expectedTopic = item.expected.recognized_topic || item.category;
        const topicAliasMap: Record<string, string> = {
          'dsu': 'union_find'
        };
        const mappedExpected = topicAliasMap[expectedTopic] || expectedTopic;
        const found = topics.find(t => t.conceptId === mappedExpected || t.conceptId === expectedTopic);
        if (!found) {
          passed = false;
          reasons.push(`Expected recognized-only topic ${mappedExpected} detected in: ${topics.map(t => t.conceptId).join(', ')}`);
        } else {
          const concept = getConceptById(found.conceptId);
          if (concept?.solutionTemplateId !== null) {
            passed = false;
            reasons.push(`Expected topic ${expectedTopic} to be recognized-only, but templateId is ${concept?.solutionTemplateId}`);
          }
        }
      }

      // ── Constraint analysis tests ──────────────────────────────────────
      else if (item.id.startsWith('FX-')) {
        const exp = item.expected.constraint_expectation;
        const normComp = (s: string) => s.replace(/²/g, '2').replace(/³/g, '3').replace(/\^/g, '').replace(/\s+/g, '');
        if (exp) {
          if (exp.feasible) {
            for (const f of exp.feasible) {
              const target = normComp(f);
              const isFeas = feasibility.feasible.some(c => normComp(c) === target);
              if (!isFeas) {
                passed = false;
                reasons.push(`Expected ${f} to be feasible. Feasible: [${feasibility.feasible.join(', ')}]`);
              }
            }
          }
          if (exp.likely_infeasible) {
            for (const inf of exp.likely_infeasible) {
              const target = normComp(inf);
              const isInfeas = feasibility.likelyInfeasible.some(c => normComp(c) === target);
              if (!isInfeas) {
                passed = false;
                reasons.push(`Expected ${inf} to be likely_infeasible. Infeasible: [${feasibility.likelyInfeasible.join(', ')}]`);
              }
            }
          }
          if (exp.overflow_risk !== undefined) {
            if (feasibility.overflowRisk !== exp.overflow_risk) {
              passed = false;
              reasons.push(`Expected overflowRisk=${exp.overflow_risk}, got ${feasibility.overflowRisk}`);
            }
          }
        }
      }

      // ── Verification tests ─────────────────────────────────────────────
      else if (item.id.startsWith('VR-')) {
        const exp = item.expected.verification;
        if (exp) {
          if (exp.verified === false && exp.message_contains) {
            const solverRes = solveCpProblem(parsed);
            if (!solverRes.verification?.summary.includes('No test cases available')) {
              passed = false;
              reasons.push(`Expected verification message to contain "${exp.message_contains}", got: ${solverRes.verification?.summary}`);
            }
          }
        }
      }

      // ── Menu driven tests ──────────────────────────────────────────────
      else if (item.id.startsWith('MENU-')) {
        const isMenu = classification.selected === 'template_match';
        if (!isMenu) {
          passed = false;
          reasons.push(`Expected classification template_match, got ${classification.selected}`);
        }
      }

      // ── Messy input tests ──────────────────────────────────────────────
      else if (item.id.startsWith('MS-')) {
        if (item.expected.expectation?.route) {
          if (classification.selected !== item.expected.expectation.route) {
            passed = false;
            reasons.push(`Route mismatch on messy input: expected ${item.expected.expectation.route}, got ${classification.selected}`);
          }
        }
        if (item.expected.expectation?.parse_examples) {
          if (parsed.examples.length === 0) {
            passed = false;
            reasons.push(`Expected messy examples to be parsed, got 0`);
          }
        }
      }

      // ── Novel wording tests ────────────────────────────────────────────
      else if (item.id.startsWith('NW-')) {
        const expectedTopic = item.expected.topic;
        const hasTopic = topics.some(t => t.conceptId === expectedTopic && t.confidence >= 0.1);
        if (!hasTopic) {
          passed = false;
          reasons.push(`Novel wording failed to detect ${expectedTopic}. Detected: ${topics.slice(0, 3).map(t => `${t.conceptId}(${t.confidence})`).join(', ')}`);
        }
      }

      // ── Anti pattern tests ─────────────────────────────────────────────
      else if (item.id.startsWith('AP-')) {
        const exp = item.expected.expectation;
        if (exp?.prefer) {
          const topCandidate = topics.find(t => !t.rejected);
          if (topCandidate?.conceptId !== exp.prefer) {
            passed = false;
            reasons.push(`Anti-pattern failed to prefer ${exp.prefer}, top was ${topCandidate?.conceptId} (${topics.slice(0, 3).map(t => `${t.conceptId}:${t.confidence}`).join(', ')})`);
          }
        }
        if (exp?.recognize) {
          const recognized = topics.some(t => t.conceptId === exp.recognize);
          if (!recognized) {
            passed = false;
            reasons.push(`Failed to recognize ${exp.recognize}`);
          }
        }
      }

      // ── Edge cases tests ───────────────────────────────────────────────
      else if (item.id.startsWith('ED-')) {
        if (!parsed || !classification || !topics) {
          passed = false;
          reasons.push('Pipeline crashed on edge case');
        }
      }

      // ── V1 regression tests ────────────────────────────────────────────
      else if (item.id.startsWith('REG-')) {
        const expRoute = item.expected.route;
        if (expRoute && classification.selected !== expRoute) {
          passed = false;
          reasons.push(`Regression route mismatch: expected ${expRoute}, got ${classification.selected}`);
        }
      }

      // ── Composition preview tests ──────────────────────────────────────
      else if (item.id.startsWith('CMP-')) {
        const expConcepts = item.expected.expectation?.concepts || [];
        for (const c of expConcepts) {
          const found = topics.some(t => t.conceptId === c);
          if (!found) {
            reasons.push(`Composition concept ${c} not detected among: ${topics.map(t => t.conceptId).join(', ')}`);
          }
        }
        if (reasons.length > 0) {
          passed = false;
        }
      }

      results.push({
        id: item.id,
        category: item.category,
        status: passed ? 'PASS' : 'FAIL',
        details: reasons.join('; ')
      });

    } catch (err: any) {
      results.push({
        id: item.id,
        category: item.category,
        status: 'FAIL',
        details: `Exception thrown: ${err.message}`
      });
    }
  }

  // Print results
  let passedCount = 0;
  let failedCount = 0;

  for (const r of results) {
    const symbol = r.status === 'PASS' ? '✓' : '✗';
    const detailStr = r.details ? ` (${r.details})` : '';
    console.log(`  ${symbol} [${r.id}] ${r.category}: ${r.status}${detailStr}`);
    if (r.status === 'PASS') passedCount++;
    else failedCount++;
  }

  console.log(`\n======================================================`);
  console.log(`Dataset Summary: ${passedCount} passed, ${failedCount} failed (${items.length} total)`);
  console.log(`Pass Rate: ${(passedCount / items.length * 100).toFixed(1)}%`);
  console.log(`======================================================\n`);

  return { passed: passedCount, failed: failedCount, results };
}

if (require.main === module) {
  runDatasetEvaluation().then(({ failed }) => {
    process.exit(failed > 0 ? 1 : 0);
  });
}
