"""
Comprehensive Unit Test Suite for CHUP Phase 3K: Dynamic Programming
Tests:
- DP Taxonomy & Enums (DPKind, DPOperationKind, DP_PATTERNS, TAXONOMY_TREE)
- Feature Extractor (DP features correctly extracted from problem text)
- Candidate Generator (generates candidates across all 14 DP patterns)
- Candidate Eliminator & Failure Analysis (all 10 DP rejection codes)
- Structural Reasoning (DPStructuralReasoning answers all 14 Core DP questions)
- Invariant Engine construction across all 14 DP patterns
- Movement Derivation across all 14 DP patterns
- C++ generator syntax and validity across all 14 patterns
- Reference oracles verification against brute force
- Bridge integration and structured dynamic_programming metadata emission
"""

import unittest
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.knowledge.taxonomy import (
    DPKind,
    DPOperationKind,
    DP_PATTERNS,
    PatternKind,
    AlgorithmFamily,
    TAXONOMY_TREE
)
from pointer_algorithms.reasoning.reasoning_engine import (
    DPStructuralReasoning,
)
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine
from pointer_algorithms.recognition.candidate_generator import CandidateGenerator
from pointer_algorithms.recognition.candidate_eliminator import CandidateEliminator
from pointer_algorithms.recognition.feature_extractor import ProblemFeatures, FeatureExtractor
from pointer_algorithms.failure_analysis.classifier import FailureClassifier, FailureCategory
from pointer_algorithms.generator.dp_cpp_generator import generate_dp_cpp
from pointer_algorithms.dp.verification.dp_oracles import (
    dp_1d_linear_oracle, brute_force_1d_linear,
    dp_prefix_suffix_oracle, brute_force_prefix_suffix,
    dp_2d_grid_oracle, brute_force_2d_grid,
    dp_string_alignment_oracle, brute_force_string_alignment,
    dp_interval_oracle, brute_force_interval,
    dp_knapsack_01_oracle, brute_force_knapsack_01,
    dp_knapsack_unbounded_oracle, brute_force_knapsack_unbounded,
    dp_tree_oracle, brute_force_tree,
    dp_bitmask_oracle, brute_force_bitmask,
    dp_digit_oracle, brute_force_digit,
    dp_state_machine_oracle, brute_force_state_machine,
    dp_dag_longest_path_oracle,
    dp_divide_and_conquer_oracle,
    dp_space_optimized_oracle
)
from pointer_algorithms.bridge import handle_request


class TestDPTaxonomyAndReasoning(unittest.TestCase):
    def test_taxonomy_definitions(self):
        """Verify 14 DP patterns and hierarchy."""
        self.assertEqual(len(DP_PATTERNS), 14)
        self.assertIn("Dynamic Programming", TAXONOMY_TREE["Pointer-Based Algorithms"])
        self.assertEqual(AlgorithmFamily.DYNAMIC_PROGRAMMING.value, "dynamic_programming")

    def test_structural_reasoning_14_questions(self):
        """Verify DPStructuralReasoning addresses all 14 Core DP Reasoning Questions."""
        for pattern in DP_PATTERNS:
            proof = DPStructuralReasoning.explain(pattern)
            self.assertTrue(len(proof.subproblem_definition) > 5, f"Failed subproblem definition for {pattern}")
            self.assertTrue(len(proof.minimal_state_representation) > 5, f"Failed state representation for {pattern}")
            self.assertTrue(len(proof.overlapping_subproblems) > 5, f"Failed overlapping subproblems for {pattern}")
            self.assertTrue(len(proof.optimal_substructure_and_transitions) > 5, f"Failed transitions for {pattern}")
            self.assertTrue(len(proof.base_cases_and_boundaries) > 5, f"Failed base cases for {pattern}")
            self.assertTrue(len(proof.dependency_dag_and_evaluation_order) > 5, f"Failed DAG order for {pattern}")
            self.assertTrue(len(proof.answer_extraction) > 5, f"Failed answer extraction for {pattern}")
            self.assertTrue(len(proof.memory_complexity_and_compression) > 5, f"Failed memory compression for {pattern}")
            self.assertTrue(len(proof.solution_reconstruction) > 5, f"Failed solution reconstruction for {pattern}")
            self.assertTrue(len(proof.applicability_vs_alternatives) > 5, f"Failed applicability for {pattern}")
            self.assertTrue(len(proof.competing_structures) > 5, f"Failed competing structures for {pattern}")
            self.assertTrue(len(proof.invalidation_invariants) > 5, f"Failed invalidation invariants for {pattern}")
            self.assertTrue(len(proof.time_complexity_derivation) > 5, f"Failed time complexity for {pattern}")
            self.assertTrue(len(proof.space_complexity_derivation) > 5, f"Failed space complexity for {pattern}")


class TestDPFeatureExtractionAndCandidates(unittest.TestCase):
    def test_feature_extraction_1d(self):
        """Verify feature extraction for 1D linear DP."""
        text = "Find maximum sum non-adjacent loot along houses using 1d dynamic programming."
        features = FeatureExtractor.extract(text)
        self.assertEqual(features.dp_kind, DPKind.LINEAR_1D)
        self.assertTrue(features.dp_has_overlapping_subproblems)
        self.assertTrue(features.dp_has_optimal_substructure)

    def test_candidate_generation_all_14_patterns(self):
        """Verify candidate generation for each pattern."""
        for pattern in DP_PATTERNS:
            features = FeatureExtractor.extract(f"Solve using {pattern} dynamic programming.")
            candidates = CandidateGenerator.generate_candidates(features)
            patterns_found = [c.pattern for c in candidates]
            self.assertIn(pattern, patterns_found, f"Candidate generator failed to propose {pattern}")


class TestDPCandidateElimination(unittest.TestCase):
    def test_rejection_greedy_choice(self):
        """Fractional knapsack must be eliminated with DP_DOMINATED_BY_GREEDY."""
        features = FeatureExtractor.extract("fractional knapsack allows continuous fractions")
        candidates = CandidateGenerator.generate_candidates(features)
        filter_res = CandidateEliminator.filter_and_rank(candidates, features)
        rejected_codes = [e.rejection_code for e in filter_res["eliminated"]]
        self.assertTrue("DP_DOMINATED_BY_GREEDY" in rejected_codes or "DP_GREEDY_CHOICE_OPTIMAL" in rejected_codes)

    def test_rejection_cyclic_graph(self):
        """Cyclic graph must be eliminated with DP_CYCLIC_STATE_DEPENDENCY."""
        features = FeatureExtractor.extract("graph with cycles and arbitrary negative edges")
        candidates = CandidateGenerator.generate_candidates(features)
        filter_res = CandidateEliminator.filter_and_rank(candidates, features)
        rejected_codes = [e.rejection_code for e in filter_res["eliminated"]]
        self.assertIn("DP_CYCLIC_STATE_DEPENDENCY", rejected_codes)

    def test_rejection_no_optimal_substructure(self):
        """No optimal substructure must be eliminated with DP_NO_OPTIMAL_SUBSTRUCTURE."""
        features = FeatureExtractor.extract("longest simple path in general undirected graph")
        candidates = CandidateGenerator.generate_candidates(features)
        filter_res = CandidateEliminator.filter_and_rank(candidates, features)
        rejected_codes = [e.rejection_code for e in filter_res["eliminated"]]
        self.assertIn("DP_NO_OPTIMAL_SUBSTRUCTURE", rejected_codes)

    def test_failure_classifier_categories(self):
        """FailureClassifier handles all 10 DP rejection categories."""
        for cat in [
            FailureCategory.DP_GREEDY_CHOICE_OPTIMAL,
            FailureCategory.DP_CYCLIC_STATE_DEPENDENCY,
            FailureCategory.DP_NO_OPTIMAL_SUBSTRUCTURE,
            FailureCategory.DP_NO_OVERLAPPING_SUBPROBLEMS,
            FailureCategory.DP_NON_MARKOVIAN_FUTURE_DEPENDENCE,
            FailureCategory.DP_STATE_SPACE_EXPLOSION,
            FailureCategory.DP_UNPROVEN_OPTIMIZATION_PREREQUISITE,
            FailureCategory.DP_OPERATION_MISMATCH,
            FailureCategory.DP_RESOURCE_LIMIT,
            FailureCategory.DP_IMPLEMENTATION_BUG
        ]:
            report = FailureClassifier.classify(cat.value, {})
            self.assertEqual(report.category, cat)


class TestDPInvariantAndMovement(unittest.TestCase):
    def test_all_14_patterns_invariants(self):
        """All 14 DP patterns must generate complete 4-phase invariants."""
        for pattern in DP_PATTERNS:
            inv = InvariantEngine.construct_invariant(pattern, {})
            self.assertTrue(len(inv.before_iteration) > 10, f"Failed before invariant for {pattern}")
            self.assertTrue(len(inv.during_iteration) > 10, f"Failed during invariant for {pattern}")
            self.assertTrue(len(inv.after_movement) > 10, f"Failed after invariant for {pattern}")
            self.assertTrue(len(inv.at_termination) > 10, f"Failed termination invariant for {pattern}")

    def test_all_14_patterns_movement(self):
        """All 14 DP patterns must generate valid movement and state transition models."""
        for pattern in DP_PATTERNS:
            model = MovementDerivationEngine.derive(pattern, {})
            self.assertTrue(len(model.objective_function) > 5, f"Failed objective for {pattern}")
            self.assertTrue(len(model.decision_conditions) > 0, f"Failed decisions for {pattern}")
            self.assertTrue(len(model.elimination_proof) > 10, f"Failed elimination proof for {pattern}")


class TestDPCppGenerator(unittest.TestCase):
    def test_cpp_code_generation_all_14_patterns(self):
        """Verify C++ code generation for all 14 DP patterns."""
        for pattern in DP_PATTERNS:
            code = generate_dp_cpp(pattern, {})
            self.assertIn("#include <iostream>", code)
            self.assertIn("int main()", code)
            self.assertIn("return 0;", code)


class TestDPOracles(unittest.TestCase):
    def test_1d_linear_oracle(self):
        nums = [2, 7, 9, 3, 1]
        self.assertEqual(dp_1d_linear_oracle(nums), brute_force_1d_linear(nums))

    def test_prefix_suffix_oracle(self):
        prices = [3, 3, 5, 0, 0, 3, 1, 4]
        self.assertEqual(dp_prefix_suffix_oracle(prices), brute_force_prefix_suffix(prices))

    def test_2d_grid_oracle(self):
        grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
        self.assertEqual(dp_2d_grid_oracle(grid), brute_force_2d_grid(grid))

    def test_string_alignment_oracle(self):
        self.assertEqual(dp_string_alignment_oracle("abcde", "ace"), brute_force_string_alignment("abcde", "ace"))

    def test_interval_oracle(self):
        nums = [3, 2, 4, 1]
        self.assertEqual(dp_interval_oracle(nums), brute_force_interval(nums))

    def test_knapsack_01_oracle(self):
        w, v, W = [2, 3, 4, 5], [3, 4, 5, 6], 5
        self.assertEqual(dp_knapsack_01_oracle(w, v, W), brute_force_knapsack_01(w, v, W))

    def test_knapsack_unbounded_oracle(self):
        w, v, W = [2, 3, 4], [10, 15, 22], 8
        self.assertEqual(dp_knapsack_unbounded_oracle(w, v, W), brute_force_knapsack_unbounded(w, v, W))

    def test_tree_oracle(self):
        n = 5
        edges = [(1, 2), (1, 3), (2, 4), (2, 5)]
        vals = [10, 20, 30, 40, 50]
        self.assertEqual(dp_tree_oracle(n, edges, vals), brute_force_tree(n, edges, vals))

    def test_bitmask_oracle(self):
        n = 4
        dist = [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0]
        ]
        self.assertEqual(dp_bitmask_oracle(n, dist), brute_force_bitmask(n, dist))

    def test_digit_oracle(self):
        self.assertEqual(dp_digit_oracle(10, 25), brute_force_digit(10, 25))

    def test_state_machine_oracle(self):
        prices = [1, 2, 3, 0, 2]
        self.assertEqual(dp_state_machine_oracle(prices), brute_force_state_machine(prices))


class TestDPBridgeIntegration(unittest.TestCase):
    def test_bridge_dynamic_programming_payload(self):
        """Verify handle_request produces complete dynamic_programming payload."""
        req = {
            "action": "solve",
            "problemText": "Find maximum sum non-adjacent loot along houses using 1d dynamic programming."
        }
        res = handle_request(req)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["family"], "dynamic_programming")
        self.assertEqual(res["selectedPattern"], "dp_1d_linear")
        self.assertIsNotNone(res.get("dynamic_programming"))
        dp_info = res["dynamic_programming"]
        self.assertTrue(dp_info["hasOverlappingSubproblems"])
        self.assertTrue(dp_info["hasOptimalSubstructure"])
        self.assertIn("code", res)
        self.assertIn("invariant", res)
        self.assertIn("movement", res)


if __name__ == "__main__":
    unittest.main()
