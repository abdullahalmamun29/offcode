"""
CHUP Recognition Architecture V2 — Reference End-to-End Test: 2-Sum.

Verifies:
1. Problem text → Evidence with provenance (no algorithm keywords)
2. Semantic model derivation:
   - selection: FIXED_CARDINALITY(2)
   - relation: SUM
   - output: ORIGINAL_INDICES
   - operation: PAIR_SUM_SEARCH
3. Candidate competition & hard elimination:
   - two_pointer_pair_sum: ACCEPTED
   - hash_pair_sum: ACCEPTED
   - knapsack_01: REJECTED (CARDINALITY_MISMATCH, SELECTION_MODEL_MISMATCH)
   - subset_sum_dp: REJECTED (SELECTION_MODEL_MISMATCH)
4. Proof obligations established:
   - cardinality == 2
   - relation == SUM
   - index preservation
   - pointer elimination invariant
5. C++17 compilation and execution against test vectors:
   - unsorted input
   - duplicate values
   - negative values
   - no solution (-1)
"""

import unittest
import subprocess
import tempfile
import os
from architecture_v2.semantic_model import (
    SelectionKind, ObjectiveKind, RelationKind, RequiredOperation
)
from architecture_v2.semantic_adapter import SemanticAdapter
from architecture_v2.capability_registry import CapabilityRegistry
from architecture_v2.candidate_eliminator import CandidateEliminatorV2, CandidateStatus
from architecture_v2.planner import AlgorithmPlannerV2, PlanStatus
from architecture_v2.bridge_v2 import BridgeV2


class Test2SumV2EndToEnd(unittest.TestCase):

    def setUp(self):
        self.problem_text = "Find two distinct elements in the array whose sum equals target. Return their 1-based indices."
        self.bridge = BridgeV2()

    def test_2sum_semantic_model_and_evidence(self):
        model = SemanticAdapter.parse(self.problem_text)

        # 1. Selection Model
        self.assertEqual(model.selection.kind, SelectionKind.FIXED_CARDINALITY)
        self.assertEqual(model.selection.cardinality, 2)

        # 2. Relation
        self.assertTrue(any(r.kind == RelationKind.SUM for r in model.relations))

        # 3. Output requirement
        self.assertEqual(model.output_spec.get("type"), "ORIGINAL_INDICES")
        self.assertEqual(model.output_spec.get("base"), 1)

        # 4. Required operation
        self.assertIn(RequiredOperation.PAIR_SUM_SEARCH, model.operations)

        # 5. Check Evidence provenance
        cardinality_ev = [ev for ev in model.evidence if ev.fact == "selection_cardinality_2"]
        self.assertTrue(len(cardinality_ev) > 0)
        self.assertIn("two", cardinality_ev[0].source.lower())

        sum_ev = [ev for ev in model.evidence if ev.fact == "relation_sum"]
        self.assertTrue(len(sum_ev) > 0)
        self.assertIn("sum", sum_ev[0].source.lower())

    def test_2sum_candidate_competition_and_hard_elimination(self):
        model = SemanticAdapter.parse(self.problem_text, {"target_value": 10**9, "memory_limit_mb": 256})
        registry = CapabilityRegistry()
        decisions = {d.candidate_name: d for d in CandidateEliminatorV2.filter_candidates(registry, model)}

        # Two-pointer must be ACCEPTED
        self.assertEqual(decisions["two_pointer_pair_sum"].status, CandidateStatus.ACCEPTED)

        # Hash pair sum must be ACCEPTED
        self.assertEqual(decisions["hash_pair_sum"].status, CandidateStatus.ACCEPTED)

        # Knapsack must be REJECTED with semantic reasons
        knap = decisions["knapsack_01"]
        self.assertEqual(knap.status, CandidateStatus.REJECTED)
        self.assertIn("CARDINALITY_MISMATCH", knap.reasons)
        self.assertIn("SELECTION_MODEL_MISMATCH", knap.reasons)

        # Subset sum DP must be REJECTED with semantic reasons
        ss = decisions["subset_sum_dp"]
        self.assertEqual(ss.status, CandidateStatus.REJECTED)
        self.assertIn("SELECTION_MODEL_MISMATCH", ss.reasons)

    def test_2sum_plan_and_proof_obligations(self):
        res = self.bridge.solve(self.problem_text)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["selectedPattern"], "two_pointer_pair_sum")
        self.assertIsNotNone(res["code"])

        # Check proof obligations in reasoning
        self.assertIn("selection_cardinality_is_2", res["proofObligations"])
        self.assertIn("relation_is_sum", res["proofObligations"])
        self.assertIn("original_indices_preserved", res["proofObligations"])
        self.assertIn("pointer_elimination_sound", res["proofObligations"])
        self.assertIn("search_terminates", res["proofObligations"])

    def test_2sum_compilation_and_execution(self):
        res = self.bridge.solve(self.problem_text)
        code = res["code"]
        self.assertIsNotNone(code)

        # Compile C++ code
        with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False) as tmp_cpp:
            tmp_cpp.write(code.encode("utf-8"))
            tmp_cpp_path = tmp_cpp.name

        exe_path = tmp_cpp_path[:-4]
        try:
            compile_proc = subprocess.run(
                ["g++", "-std=c++17", "-O2", tmp_cpp_path, "-o", exe_path],
                capture_output=True, text=True
            )
            self.assertEqual(compile_proc.returncode, 0, f"Compilation failed: {compile_proc.stderr}")

            # Test 1: Unsorted array [3, 2, 4], target = 6 -> elements 2 and 4 at 1-based indices 2 and 3
            input_data = "3 6\n3 2 4\n"
            run_proc = subprocess.run([exe_path], input=input_data, capture_output=True, text=True, timeout=5)
            self.assertEqual(run_proc.returncode, 0)
            out_tokens = sorted(map(int, run_proc.stdout.strip().split()))
            self.assertEqual(out_tokens, [2, 3])

            # Test 2: Sorted array [2, 7, 11, 15], target = 9 -> indices 1 and 2
            input_data = "4 9\n2 7 11 15\n"
            run_proc = subprocess.run([exe_path], input=input_data, capture_output=True, text=True, timeout=5)
            out_tokens = sorted(map(int, run_proc.stdout.strip().split()))
            self.assertEqual(out_tokens, [1, 2])

            # Test 3: Duplicates [3, 3], target = 6 -> indices 1 and 2
            input_data = "2 6\n3 3\n"
            run_proc = subprocess.run([exe_path], input=input_data, capture_output=True, text=True, timeout=5)
            out_tokens = sorted(map(int, run_proc.stdout.strip().split()))
            self.assertEqual(out_tokens, [1, 2])

            # Test 4: Negative numbers [-1, -2, -3, -4, -5], target = -8 -> (-3, -5) at indices 3 and 5
            input_data = "5 -8\n-1 -2 -3 -4 -5\n"
            run_proc = subprocess.run([exe_path], input=input_data, capture_output=True, text=True, timeout=5)
            out_tokens = sorted(map(int, run_proc.stdout.strip().split()))
            self.assertEqual(out_tokens, [3, 5])

            # Test 5: No solution [1, 2, 3], target = 7 -> -1
            input_data = "3 7\n1 2 3\n"
            run_proc = subprocess.run([exe_path], input=input_data, capture_output=True, text=True, timeout=5)
            self.assertEqual(run_proc.stdout.strip(), "-1")

        finally:
            if os.path.exists(tmp_cpp_path):
                os.remove(tmp_cpp_path)
            if os.path.exists(exe_path):
                os.remove(exe_path)


if __name__ == "__main__":
    unittest.main()
