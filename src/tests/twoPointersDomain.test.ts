/**
 * CHUP — Pointer-Based Algorithms Domain Benchmark & Evaluation Suite.
 *
 * Evaluates:
 * 1. Known Problems (5 problems)
 * 2. Variant Problems (5 problems)
 * 3. Unseen Problems (4 problems)
 * 4. Negative Cases (4 problems with strict rejection)
 * 5. Algorithm-Confusion Battery (6 cross-domain problems)
 * 6. Knowledge Transfer Benchmark (transfer from Set A to Set B)
 *
 * Separately reports:
 * - Known Problem Accuracy
 * - Variant Problem Accuracy
 * - Unseen Problem Accuracy
 * - Negative-Case Accuracy
 * - Cross-Family Confusion Accuracy
 * - Knowledge Transfer Accuracy
 * - Failure Classification breakdown
 */

import { parseProblem } from '../pipeline/problemParser';
import { normalizeInput } from '../pipeline/inputNormalizer';
import { solveCpProblem } from '../solver/cpSolver';
import { verifyCode } from '../verifier/verificationEngine';
import { PointerBridge } from '../parser/pointerBridge';
import * as path from 'path';
import { PythonRuntimeManager } from '../runtime/pythonRuntimeManager';

interface TestResult {
  category: string;
  name: string;
  passed: boolean;
  notes: string;
}

const allResults: TestResult[] = [];

function record(category: string, name: string, passed: boolean, notes: string = ""): boolean {
  allResults.push({ category, name, passed, notes });
  if (passed) {
    console.log(`  ✓ [${category}] ${name}`);
  } else {
    console.error(`  ✗ [${category}] ${name} — ${notes}`);
  }
  return passed;
}

export function runTwoPointersDomainTests(): {
  knownAccuracy: number;
  variantAccuracy: number;
  unseenAccuracy: number;
  negativeAccuracy: number;
  confusionAccuracy: number;
  transferAccuracy: number;
  totalPassed: number;
  totalFailed: number;
} {
  const pointerBridge = new PointerBridge();

  console.log('\n=================================================================');
  console.log('      CHUP Pointer-Based Algorithms Domain Benchmark Suite       ');
  console.log('=================================================================');

  // ═════════════════════════════════════════════════════════════════════════════
  // Category 1: Known-Style Problems
  // ═════════════════════════════════════════════════════════════════════════════
  console.log('\n--- 1. Known-Style Problems ---');

  // KP1: Sorted pair sum
  const kp1_text = `Given a sorted array of n integers and a target sum, find two numbers that add up to target.
Input:
4 8
1 2 4 7
Output:
1 7`;
  const p_kp1 = parseProblem(normalizeInput(kp1_text), kp1_text);
  const res_kp1 = solveCpProblem(p_kp1);
  record("Known", "KP1: Pair sum in sorted array", res_kp1.success === true && res_kp1.code.includes("lo") && res_kp1.code.includes("hi"));

  // KP2: Fixed window max sum
  const kp2_text = `Find the maximum sum of a contiguous subarray of size k.
Input:
4 2
100 200 300 400
Output:
700`;
  const p_kp2 = parseProblem(normalizeInput(kp2_text), kp2_text);
  const res_kp2 = solveCpProblem(p_kp2);
  record("Known", "KP2: Fixed window maximum sum", res_kp2.success === true);

  // KP3: In-place remove duplicates from sorted array
  const kp3_text = `Remove duplicates from sorted array in-place and print unique elements.
Input:
5
1 1 2 2 3
Output:
1 2 3`;
  const p_kp3 = parseProblem(normalizeInput(kp3_text), kp3_text);
  const res_kp3 = solveCpProblem(p_kp3);
  record("Known", "KP3: In-place remove duplicates from sorted array", res_kp3.success === true);

  // KP4: Converging pair sum with negative values in sorted array
  const kp4_text = `Given a sorted nondecreasing sequence, find two numbers whose combined value is target T.
Input:
5 0
-10 -3 0 3 8
Output:
-3 3`;
  const p_kp4 = parseProblem(normalizeInput(kp4_text), kp4_text);
  const res_kp4 = solveCpProblem(p_kp4);
  record("Known", "KP4: Sorted pair sum with negative values", res_kp4.success === true);

  // KP5: Dutch National Flag (3-way partition)
  const kp5_text = `Sort an array of 0s, 1s, and 2s in-place using Dutch National Flag three-way partition.
Input:
6
2 0 2 1 1 0
Output:
0 0 1 1 2 2`;
  const p_kp5 = parseProblem(normalizeInput(kp5_text), kp5_text);
  const res_kp5 = solveCpProblem(p_kp5);
  record("Known", "KP5: Dutch National Flag 3-way partition", res_kp5.success === true);

  // ═════════════════════════════════════════════════════════════════════════════
  // Category 2: Variant Problems
  // ═════════════════════════════════════════════════════════════════════════════
  console.log('\n--- 2. Variant Problems ---');

  // VP1: Pair sum with 1-based original index tracking
  const vp1_text = `Given an array of n integers and target x, find two values at distinct positions whose sum is x. Print their 1-based original indices.
Input:
4 8
2 7 5 1
Output:
2 4`;
  const p_vp1 = parseProblem(normalizeInput(vp1_text), vp1_text);
  const res_vp1 = solveCpProblem(p_vp1);
  record("Variant", "VP1: Pair sum with original 1-based indices", res_vp1.success === true && res_vp1.code.includes("pair"));

  // VP2: Pair difference (a[j] - a[i] = k)
  const vp2_text = `Given a sorted array, find two numbers with difference equal to k.
Input:
5 3
1 2 4 7 11
Output:
1 4`;
  const p_vp2 = parseProblem(normalizeInput(vp2_text), vp2_text);
  const res_vp2 = solveCpProblem(p_vp2);
  record("Variant", "VP2: Pair difference in sorted array", res_vp2.success === true);

  // VP3: Longest contiguous segment with sum <= S on positive integers
  const vp3_text = `Find the length of the longest contiguous subarray whose sum is at most S. All numbers are positive integers.
Input:
5 7
2 1 3 4 1
Output:
3`;
  const p_vp3 = parseProblem(normalizeInput(vp3_text), vp3_text);
  const res_vp3 = solveCpProblem(p_vp3);
  record("Variant", "VP3: Longest subarray with sum <= S on positive integers", res_vp3.success === true);

  // VP4: In-place move zeroes to end
  const vp4_text = `Move all zeroes to the end of the array in-place while maintaining relative order of non-zero elements.
Input:
5
0 1 0 3 12
Output:
1 3 12 0 0`;
  const p_vp4 = parseProblem(normalizeInput(vp4_text), vp4_text);
  const res_vp4 = solveCpProblem(p_vp4);
  record("Variant", "VP4: In-place move zeroes to end", res_vp4.success === true);

  // VP5: Linked list cycle detection
  const vp5_text = `Detect cycle in a linked list using Floyd's tortoise and hare pointer algorithm.
Input:
3
1 2 3
Output:
NO`;
  const p_vp5 = parseProblem(normalizeInput(vp5_text), vp5_text);
  const res_vp5 = solveCpProblem(p_vp5);
  record("Variant", "VP5: Linked list cycle detection recognition", res_vp5.success === true || (res_vp5.selectedAlgorithm !== null));

  // ═════════════════════════════════════════════════════════════════════════════
  // Category 3: Unseen Problems (Novel Structure / Objective)
  // ═════════════════════════════════════════════════════════════════════════════
  console.log('\n--- 3. Unseen Problems ---');

  // UP1: Container With Most Water (Objective derived)
  const up1_text = `Given n non-negative integers representing vertical lines, find two lines that together with the x-axis form a container holding the maximum area of water.
Input:
9
1 8 6 2 5 4 8 3 7
Output:
49`;
  const p_up1 = parseProblem(normalizeInput(up1_text), up1_text);
  const res_up1 = solveCpProblem(p_up1);
  record("Unseen", "UP1: Container With Most Water (area maximization)", res_up1.success === true && res_up1.approach.includes("container_most_water"));

  // UP2: Minimum size subarray sum >= S
  const up2_text = `Find the minimal length of a contiguous subarray of which the sum is at least target S. All elements are positive.
Input:
6 7
2 3 1 2 4 3
Output:
2`;
  const p_up2 = parseProblem(normalizeInput(up2_text), up2_text);
  const res_up2 = solveCpProblem(p_up2);
  record("Unseen", "UP2: Minimum size subarray sum >= S (variable min window)", res_up2.success === true);

  // UP3: Longest substring with at most K distinct characters
  const up3_text = `Find the length of the longest contiguous substring containing at most k distinct characters.
Input:
eceba 2
Output:
3`;
  const p_up3 = parseProblem(normalizeInput(up3_text), up3_text);
  const res_up3 = solveCpProblem(p_up3);
  record("Unseen", "UP3: Longest substring with at most K distinct (frequency window)", res_up3.success === true);

  // UP4: Partition array by parity (even before odd)
  const up4_text = `Partition array by parity so that all even integers appear before all odd integers in-place.
Input:
4
3 1 2 4
Output:
4 2 1 3`;
  const p_up4 = parseProblem(normalizeInput(up4_text), up4_text);
  const res_up4 = solveCpProblem(p_up4);
  record("Unseen", "UP4: Partition array by parity in-place", res_up4.success === true);

  // UP5: Ferris Wheel (Capacity-constrained pairing: max 2 per group, sum <= x, minimize groups)
  const up5_text = `There are n children who want to go to a Ferris wheel, and your task is to find a gondola for each child.
Each gondola may have one or two children in it, and in addition, the total weight in a gondola may not exceed x. You know the weight of every child.
What is the minimum number of gondolas needed for the children?
Input:
4 10
7 2 3 9
Output:
3`;
  const p_up5 = parseProblem(normalizeInput(up5_text), up5_text);
  const res_up5 = solveCpProblem(p_up5);
  record("Unseen", "UP5: Capacity-constrained pairing (Ferris Wheel)", res_up5.success === true && res_up5.selectedAlgorithm === "greedy_capacity_pairing" && res_up5.verification?.allPassed === true);

  // UP6: Two-sequence monotonic matching (Apartments)
  const up6_text = `There are n applicants and m free apartments. Your task is to distribute the apartments so that as many applicants as possible will get an apartment.
Each applicant has a desired apartment size, and they will accept any apartment whose size is close enough to the desired size.
The first input line has three integers n, m, and k: the number of applicants, the number of apartments, and the maximum allowed difference.
The next line contains n integers a1, a2, ... an: the desired apartment size of each applicant. If the desired size of an applicant is x, they will accept any apartment whose size is between x - k and x + k.
The last line contains m integers b1, b2, ... bm: the size of each apartment.
Constraints:
1 <= n, m <= 2 * 10^5
0 <= k <= 10^9
1 <= ai, bi <= 10^9
Input:
4 3 5
60 45 80 60
30 60 75
Output:
2`;
  const p_up6 = parseProblem(normalizeInput(up6_text), up6_text);
  const res_up6 = solveCpProblem(p_up6);
  record("Unseen", "UP6: Two-sequence monotonic matching (Apartments)", res_up6.success === true && res_up6.selectedAlgorithm === "greedy_two_sequence_interval_matching" && res_up6.verification?.allPassed === true);

  // ═════════════════════════════════════════════════════════════════════════════
  // Category 4: Negative Cases (Strict Rejection of Two Pointers)
  // ═════════════════════════════════════════════════════════════════════════════
  console.log('\n--- 4. Negative Cases (Strict Rejection) ---');

  // NP1: Subarray sum equal to K with negative values -> MUST REJECT sliding window, MUST USE Prefix Sum + Hash Map
  const np1_text = `Find the length of the longest contiguous segment whose total equals exact sum K in an array containing negative and positive numbers.
Input:
5 3
1 -1 5 -2 3
Output:
4`;
  const p_np1 = parseProblem(normalizeInput(np1_text), np1_text);
  const res_np1 = solveCpProblem(p_np1);
  const np1_rejects_sliding = (res_np1.selectedAlgorithm === 'prefix_sum' || res_np1.selectedAlgorithm === 'prefixSum' || !res_np1.approach.includes('sliding_window'));
  record("Negative", "NP1: Subarray sum with negatives rejects sliding window", np1_rejects_sliding && res_np1.success === true, `selected=${res_np1.selectedAlgorithm}`);

  // NP2: Unsorted array pair sum where sorting is forbidden and indices cannot change
  const np2_text = `Given an unsorted array of numbers that cannot be sorted, find if there exists a pair with sum equal to target using O(N) time.
Input:
4 9
2 7 11 15
Output:
YES`;
  const p_np2 = parseProblem(normalizeInput(np2_text), np2_text);
  const res_np2 = solveCpProblem(p_np2);
  const np2_passed = res_np2.success === true && (res_np2.code.includes("unordered_set") || res_np2.code.includes("unordered_map") || res_np2.selectedAlgorithm === 'frequency_count');
  record("Negative", "NP2: Unsorted pair sum without sorting prefers hash set/map", np2_passed);

  // NP3: Dynamic range minimum query with point updates -> MUST REJECT Two Pointers
  const np3_text = `Given an array that receives point updates, answer range minimum queries after each update.
Input:
5 2
1 5 2 4 3
1 10
1 3
Output:
1`;
  const p_np3 = parseProblem(normalizeInput(np3_text), np3_text);
  const res_np3 = solveCpProblem(p_np3);
  const np3_rejected = (res_np3.success === false && res_np3.limitationMessage !== null && !res_np3.approach.includes("two_pointer"));
  record("Negative", "NP3: Dynamic updates with range queries rejects Two Pointers", np3_rejected);

  // NP4: Non-monotonic arbitrary subset sum -> MUST REJECT Two Pointers
  const np4_text = `Find a subset of numbers that adds up to target T where elements can be chosen non-contiguously from arbitrary positions.
Input:
4 9
3 34 4 12
Output:
NO`;
  const p_np4 = parseProblem(normalizeInput(np4_text), np4_text);
  const res_np4 = solveCpProblem(p_np4);
  const np4_rejected = !res_np4.approach.includes("two_pointers");
  record("Negative", "NP4: Arbitrary subset sum rejects Two Pointers", np4_rejected);

  // ═════════════════════════════════════════════════════════════════════════════
  // Category 5: Algorithm-Confusion Battery (Cross-Domain Separation)
  // ═════════════════════════════════════════════════════════════════════════════
  console.log('\n--- 5. Algorithm-Confusion Battery ---');

  // CF1: Two Pointer vs Hash Map (Fast membership duplicate check)
  const cf1_text = `Given n integers, output YES if any value occurs more than once, otherwise output NO.
Constraints:
1 <= n <= 1000000
Input:
4
1 2 3 2
Output:
YES`;
  const p_cf1 = parseProblem(normalizeInput(cf1_text), cf1_text);
  const res_cf1 = solveCpProblem(p_cf1);
  record("Confusion", "CF1: Fast membership duplicate check selects set/map over Two Pointers", res_cf1.code.includes("set") && res_cf1.success === true);

  // CF2: Two Pointer vs Binary Search (threshold search)
  const cf2_text = `Given a sorted array, for every query x print the first position whose value is at least x.
Input:
5 2
1 3 5 7 9
5
4
Output:
3
3`;
  const p_cf2 = parseProblem(normalizeInput(cf2_text), cf2_text);
  const res_cf2 = solveCpProblem(p_cf2);
  record("Confusion", "CF2: Threshold query in sorted array selects lower_bound binary search", res_cf2.selectedAlgorithm === 'lower_bound' && res_cf2.success === true);

  // CF3: Sliding Window vs Prefix Sum (Repeated static range queries)
  const cf3_text = `Given an immutable array, answer q queries asking for the sum of elements between indices l and r.
Input:
5 2
1 2 3 4 5
1 3
2 4
Output:
6
9`;
  const p_cf3 = parseProblem(normalizeInput(cf3_text), cf3_text);
  const res_cf3 = solveCpProblem(p_cf3);
  record("Confusion", "CF3: Static range sum queries selects Prefix Sum over Sliding Window", res_cf3.selectedAlgorithm === 'prefix_sum' || res_cf3.code.includes("pref"));

  // CF4: Two Pointer vs Greedy (Interval scheduling)
  const cf4_text = `Given a set of intervals, select the maximum number of mutually non-overlapping intervals.
Input:
3
1 3
2 4
3 5
Output:
2`;
  const p_cf4 = parseProblem(normalizeInput(cf4_text), cf4_text);
  const res_cf4 = solveCpProblem(p_cf4);
  record("Confusion", "CF4: Interval scheduling selects sort_greedy over Two Pointers", res_cf4.selectedAlgorithm === 'sort_greedy' || res_cf4.code.includes("sort"));

  // CF5: Partition vs General Sorting
  const cf5_text = `Sort an array and print it.
Input:
5
5 2 4 1 3
Output:
1 2 3 4 5`;
  const p_cf5 = parseProblem(normalizeInput(cf5_text), cf5_text);
  const res_cf5 = solveCpProblem(p_cf5);
  record("Confusion", "CF5: Arbitrary sequence sort selects general sort over partition", res_cf5.code.includes("sort(") && res_cf5.success === true);

  // CF6: Two Pointer vs 1D DP
  const cf6_text = `Find the length of the longest increasing subsequence.
Input:
6
10 9 2 5 3 7
Output:
3`;
  const p_cf6 = parseProblem(normalizeInput(cf6_text), cf6_text);
  const res_cf6 = solveCpProblem(p_cf6);
  record("Confusion", "CF6: LIS does not mistakenly choose sliding window", !res_cf6.approach.includes("sliding_window"));

  // ═════════════════════════════════════════════════════════════════════════════
  // Category 6: Knowledge Transfer Benchmark (Cross-Problem Transfer)
  // ═════════════════════════════════════════════════════════════════════════════
  console.log('\n--- 6. Knowledge Transfer Benchmark ---');
  let transferSuccess = false;
  try {
    const { execFileSync } = require('child_process');
    const runtime = PythonRuntimeManager.getInstance().resolveRuntimeSync();
    const projectRoot = path.resolve(__dirname, "..", "..");
    const delimiter = process.platform === "win32" ? ";" : ":";
    const existingPythonPath = process.env.PYTHONPATH;
    const combinedPythonPath =
      existingPythonPath && existingPythonPath.trim().length > 0
        ? `${projectRoot}${delimiter}${existingPythonPath.trim()}`
        : projectRoot;

    const execPath = runtime.concreteExecutable || runtime.executable;
    const execArgs = runtime.concreteExecutable
      ? [
          "-c",
          "from pointer_algorithms.learning.transfer_eval import TransferBenchmark; import json; print(json.dumps(TransferBenchmark.run_transfer_experiment()))"
        ]
      : [
          ...runtime.args,
          "-c",
          "from pointer_algorithms.learning.transfer_eval import TransferBenchmark; import json; print(json.dumps(TransferBenchmark.run_transfer_experiment()))"
        ];

    const stdout = execFileSync(
      execPath,
      execArgs,
      {
        cwd: projectRoot,
        env: {
          ...process.env,
          PYTHONPATH: combinedPythonPath,
          PYTHONDONTWRITEBYTECODE: "1"
        },
        encoding: "utf-8",
        shell: false
      }
    );
    const parsed = JSON.parse(stdout);
    transferSuccess = parsed.induced_rule_promoted && parsed.transfer_accuracy === 100;
  } catch (e) {
    transferSuccess = false;
  }
  record("Transfer", "KT1: Induced abstraction transfers to 100% of unseen variant targets", transferSuccess);

  // ═════════════════════════════════════════════════════════════════════════════
  // Aggregate Metrics Computation
  // ═════════════════════════════════════════════════════════════════════════════
  const getAcc = (cat: string) => {
    const items = allResults.filter(r => r.category === cat);
    if (items.length === 0) return 100;
    const passed = items.filter(r => r.passed).length;
    return (passed / items.length) * 100;
  };

  const knownAccuracy = getAcc("Known");
  const variantAccuracy = getAcc("Variant");
  const unseenAccuracy = getAcc("Unseen");
  const negativeAccuracy = getAcc("Negative");
  const confusionAccuracy = getAcc("Confusion");
  const transferAccuracy = getAcc("Transfer");

  const totalPassed = allResults.filter(r => r.passed).length;
  const totalFailed = allResults.filter(r => !r.passed).length;

  console.log('\n=================================================================');
  console.log('                 DOMAIN EVALUATION SCORECARD                     ');
  console.log('=================================================================');
  console.log(`  Known Problem Accuracy:          ${knownAccuracy.toFixed(1)}%`);
  console.log(`  Variant Problem Accuracy:        ${variantAccuracy.toFixed(1)}%`);
  console.log(`  Unseen Problem Accuracy:         ${unseenAccuracy.toFixed(1)}%`);
  console.log(`  Negative-Case Accuracy:          ${negativeAccuracy.toFixed(1)}%`);
  console.log(`  Algorithm-Confusion Accuracy:    ${confusionAccuracy.toFixed(1)}%`);
  console.log(`  Knowledge Transfer Accuracy:     ${transferAccuracy.toFixed(1)}%`);
  console.log('-----------------------------------------------------------------');
  console.log(`  Total: ${totalPassed} passed, ${totalFailed} failed.`);
  console.log('=================================================================\n');

  return {
    knownAccuracy,
    variantAccuracy,
    unseenAccuracy,
    negativeAccuracy,
    confusionAccuracy,
    transferAccuracy,
    totalPassed,
    totalFailed
  };
}

if (require.main === module) {
  const res = runTwoPointersDomainTests();
  process.exit(res.totalFailed > 0 ? 1 : 0);
}
