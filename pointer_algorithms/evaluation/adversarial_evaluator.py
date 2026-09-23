"""
Adversarial Evaluator for Pointer-Based Algorithms.

Executes a rigorous 3-pass adversarial evaluation across 40 unseen problems:
- Pass 1: Isolated evaluation recording all 11 required fields.
- Pass 2: Shuffled order evaluation (testing order independence / absence of cross-problem contamination).
- Pass 3: Paraphrased query evaluation (testing generalization over surface wording variations).
"""

import os
import sys
import json
import random
from typing import Dict, Any, List, Optional

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.failure_analysis.classifier import FailureClassifier, FailureCategory

class AdversarialEvaluator:

    @staticmethod
    def evaluate_problem(problem_id: str, problem_text: str, oracle: Dict[str, Any]) -> Dict[str, Any]:
        """Runs evaluation for a single problem and captures all 11 required fields."""
        res = handle_request({"problemText": problem_text})

        status = res.get("status")
        selected_pattern = res.get("selectedPattern")
        family = res.get("family")
        rec_alt = res.get("recommendedAlternative")
        eliminated = res.get("eliminatedCandidates", [])

        expected_decision = oracle["expected_decision"]
        expected_family = oracle["expected_family"]

        decision = "accept" if status == "success" else "reject"

        # Check correctness against oracle specification
        is_pass = False
        failure_category: Optional[str] = None

        if expected_decision == "accept":
            if decision == "accept":
                # Verify family compatibility
                family_matches = False
                if expected_family == "two_pointers.converging" and family == "two_pointers_converging":
                    family_matches = True
                elif expected_family == "two_pointers.sliding_window" and family == "sliding_window":
                    family_matches = True
                elif expected_family in ("two_pointers.same_direction", "two_pointer.same_direction") and family == "two_pointers_same_direction":
                    family_matches = True
                elif expected_family == "two_pointers.converging_or_same_direction" and family in ("two_pointers_converging", "two_pointers_same_direction"):
                    family_matches = True
                elif expected_family == "pointer_algorithms.partition" and family == "partition_pointers":
                    family_matches = True
                elif expected_family == "pointer_algorithms.fast_slow" and family == "fast_slow_pointers":
                    family_matches = True

                # Must also produce structurally valid reasoning trace and generated code
                has_trace = bool(
                    res.get("preconditionEvidence") and
                    res.get("monotonicity", {}).get("property") and
                    res.get("invariant", {}).get("before") and
                    res.get("movement", {}).get("eliminationProof") and
                    res.get("code")
                )

                if family_matches and has_trace:
                    is_pass = True
                elif not family_matches:
                    failure_category = FailureCategory.WRONG_PATTERN_FAMILY.value
                else:
                    failure_category = FailureCategory.BROKEN_INVARIANT.value
            else:
                failure_category = FailureCategory.WRONG_RECOGNITION.value

        elif expected_decision == "multiple_valid_strategies":
            # Both pointer strategy and valid non-pointer strategy are acceptable
            if decision == "accept":
                is_pass = True
            elif decision == "reject" and rec_alt in (
                "hash_map_pair_lookup", "hash_set_lookup", "hash_set_or_sorting", "sort_plus_two_pointers_or_hash_set"
            ):
                is_pass = True
            else:
                failure_category = FailureCategory.WRONG_ALTERNATIVE_SELECTION.value

        elif expected_decision.startswith("reject") or expected_decision == "do_not_force_pointer":
            if decision == "reject":
                is_pass = True
            else:
                failure_category = FailureCategory.VERIFICATION_FALSE_POSITIVE.value

        # Extract all 11 required fields
        preconditions = res.get("preconditionEvidence")
        if not preconditions:
            if eliminated:
                preconditions = f"Precondition failed: {eliminated[0].get('evidence', '')}"
            else:
                preconditions = "Preconditions not satisfied for pointer algorithms"

        mono = res.get("monotonicity", {})
        invariant = res.get("invariant", {})
        movement = res.get("movement", {})
        code = res.get("code", "")

        return {
            "problem_id": problem_id,
            "candidate_family": family or (eliminated[0]["family"] if eliminated else "none"),
            "decision": decision,
            "verified_preconditions": preconditions,
            "monotonicity_type": mono.get("kind", "none"),
            "monotonicity_proof": mono.get("justification", "none"),
            "invariant": invariant,
            "movement_justification": movement.get("eliminationProof", "none"),
            "alternative": rec_alt or (eliminated[0]["recommendedAlternative"] if eliminated else "none"),
            "code": code,
            "verification_result": "PASS" if is_pass else "FAIL",
            "failure_category": failure_category
        }

    @classmethod
    def run_pass_1_isolated(cls, blind_path: str, oracle_path: str) -> List[Dict[str, Any]]:
        with open(blind_path, "r", encoding="utf-8") as f:
            tests = [json.loads(line) for line in f if line.strip()]
        with open(oracle_path, "r", encoding="utf-8") as f:
            oracles = {json.loads(line)["id"]: json.loads(line) for line in f if line.strip()}

        results = []
        for t in tests:
            r = cls.evaluate_problem(t["id"], t["problem"], oracles[t["id"]])
            results.append(r)
        return results

    @classmethod
    def run_pass_2_shuffled(cls, blind_path: str, oracle_path: str, seed: int = 42) -> List[Dict[str, Any]]:
        with open(blind_path, "r", encoding="utf-8") as f:
            tests = [json.loads(line) for line in f if line.strip()]
        with open(oracle_path, "r", encoding="utf-8") as f:
            oracles = {json.loads(line)["id"]: json.loads(line) for line in f if line.strip()}

        shuffled_tests = list(tests)
        random.seed(seed)
        random.shuffle(shuffled_tests)

        results = []
        for t in shuffled_tests:
            r = cls.evaluate_problem(t["id"], t["problem"], oracles[t["id"]])
            results.append(r)
        return results

    @classmethod
    def run_pass_3_paraphrased(cls, oracle_path: str) -> List[Dict[str, Any]]:
        with open(oracle_path, "r", encoding="utf-8") as f:
            oracles = {json.loads(line)["id"]: json.loads(line) for line in f if line.strip()}

        paraphrased_suite = [
            {
                "id": "TP-B01",
                "problem": "We have a sorted array of numbers. Can we pick two distinct elements that sum up to target X? Output YES or NO."
            },
            {
                "id": "TP-B03",
                "problem": "Find two vertical lines from an input list of heights that form a container with maximum water area."
            },
            {
                "id": "TP-B04",
                "problem": "Check if a string reads the same from left to right and right to left after removing non-alphanumeric characters."
            },
            {
                "id": "TP-B06",
                "problem": "Modify the input array in-place by removing all occurrences of value X while preserving relative order."
            },
            {
                "id": "TP-B09",
                "problem": "Find the length of the longest contiguous substring containing at most K distinct characters."
            },
            {
                "id": "TP-B10",
                "problem": "In an array of positive integers, locate the minimum length of a contiguous subarray whose sum is at least S."
            },
            {
                "id": "TP-B13",
                "problem": "Rearrange an array in-place so that all negative values come before all nonnegative values."
            },
            {
                "id": "TP-B17",
                "problem": "With an integer array containing both negative and positive values, find the minimum length of a contiguous subarray whose sum is at least S."
            },
            {
                "id": "TP-B19",
                "problem": "Support point updates alongside online range minimum queries."
            },
            {
                "id": "TP-B25",
                "problem": "Given intervals, select the maximum number of mutually non-overlapping intervals."
            }
        ]

        results = []
        for t in paraphrased_suite:
            r = cls.evaluate_problem(t["id"], t["problem"], oracles[t["id"]])
            results.append(r)
        return results

def main():
    blind_path = os.path.join(PROJECT_ROOT, "pointer_algorithms/data/adversarial/chup_pointer_blind_tests.jsonl")
    oracle_path = os.path.join(PROJECT_ROOT, "pointer_algorithms/data/adversarial/chup_pointer_oracle.jsonl")

    print("=" * 80)
    print("      CHUP POINTER ALGORITHMS — 40-PROBLEM ADVERSARIAL BENCHMARK")
    print("=" * 80)

    # Pass 1: Isolated
    print("\n[Pass 1] Running Isolated Evaluation across all 40 blind tests...")
    pass_1_res = AdversarialEvaluator.run_pass_1_isolated(blind_path, oracle_path)
    pass_1_correct = sum(1 for r in pass_1_res if r["verification_result"] == "PASS")
    pass_1_acc = (pass_1_correct / len(pass_1_res)) * 100.0
    print(f"Pass 1 Result: {pass_1_correct}/{len(pass_1_res)} passed ({pass_1_acc:.1f}%)")

    # Pass 2: Shuffled
    print("\n[Pass 2] Running Shuffled Order Evaluation (Testing Order Independence)...")
    pass_2_res = AdversarialEvaluator.run_pass_2_shuffled(blind_path, oracle_path, seed=1337)
    pass_2_correct = sum(1 for r in pass_2_res if r["verification_result"] == "PASS")
    pass_2_acc = (pass_2_correct / len(pass_2_res)) * 100.0
    print(f"Pass 2 Result: {pass_2_correct}/{len(pass_2_res)} passed ({pass_2_acc:.1f}%)")

    # Pass 3: Paraphrased
    print("\n[Pass 3] Running Paraphrased Query Evaluation (Testing Generalization)...")
    pass_3_res = AdversarialEvaluator.run_pass_3_paraphrased(oracle_path)
    pass_3_correct = sum(1 for r in pass_3_res if r["verification_result"] == "PASS")
    pass_3_acc = (pass_3_correct / len(pass_3_res)) * 100.0
    print(f"Pass 3 Result: {pass_3_correct}/{len(pass_3_res)} passed ({pass_3_acc:.1f}%)")

    print("\n" + "=" * 80)
    print("                           SCORECARD SUMMARY")
    print("=" * 80)
    print(f"  Pass 1 (Isolated 40/40):         {pass_1_acc:.1f}% ({pass_1_correct}/40)")
    print(f"  Pass 2 (Shuffled 40/40):         {pass_2_acc:.1f}% ({pass_2_correct}/40)")
    print(f"  Pass 3 (Paraphrased 10/10):      {pass_3_acc:.1f}% ({pass_3_correct}/10)")
    print("=" * 80)

    # Save detailed JSON evaluation report
    report_path = os.path.join(PROJECT_ROOT, "pointer_algorithms/data/adversarial/adversarial_evaluation_report.json")
    report_data = {
        "pass_1_isolated": pass_1_res,
        "pass_2_shuffled_order": pass_2_res,
        "pass_3_paraphrased": pass_3_res,
        "summary": {
            "pass_1_accuracy": pass_1_acc,
            "pass_2_accuracy": pass_2_acc,
            "pass_3_accuracy": pass_3_acc
        }
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)
    print(f"Detailed 11-field report saved to: {report_path}")

if __name__ == "__main__":
    main()
