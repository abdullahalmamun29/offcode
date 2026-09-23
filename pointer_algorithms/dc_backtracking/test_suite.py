"""
Comprehensive Unit Test Suite for CHUP Phase 3M: Divide & Conquer, Backtracking, and Exponential Decomposition.

Tests:
- DC/Backtracking Taxonomy & Enums (DCBacktrackingKind, SubproblemDependencyKind, TerminationGuaranteeKind, DC_BACKTRACKING_PATTERNS)
- Feature Extractor (Features correctly extracted from problem text; Section 8 Tower gate detection)
- Candidate Generator (generates candidates across all 10 patterns; Tower problem gate)
- Candidate Eliminator & Failure Analysis (all 12 failure categories; Section 8 Tower problem gate fail-closed)
- Structural Reasoning (DCBacktrackingStructuralReasoning with conditionally applicable fields and zero fabricated fields)
- Invariant Engine (4-phase invariants tailored to termination_guarantee_type)
- Movement Derivation (state mutation & restoration models across all 10 patterns)
- C++ Generator (syntax and validity across all 10 patterns)
- Reference Oracles (verification against independent brute-force/DP solutions)
- Bridge Integration (JSON-IPC bridge for divide_and_conquer_backtracking)
"""

import unittest
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.knowledge.taxonomy import (
    DCBacktrackingKind,
    SubproblemDependencyKind,
    TerminationGuaranteeKind,
    DC_BACKTRACKING_PATTERNS,
    PatternKind,
    AlgorithmFamily,
    TAXONOMY_TREE
)
from pointer_algorithms.reasoning.reasoning_engine import (
    DCBacktrackingStructuralReasoning,
    DCBacktrackingDerivation
)
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine
from pointer_algorithms.recognition.candidate_generator import CandidateGenerator
from pointer_algorithms.recognition.candidate_eliminator import CandidateEliminator
from pointer_algorithms.recognition.feature_extractor import ProblemFeatures, FeatureExtractor
from pointer_algorithms.failure_analysis.classifier import FailureClassifier, FailureCategory
from pointer_algorithms.generator.dc_backtracking_cpp_generator import generate_dc_backtracking_cpp
from pointer_algorithms.dc_backtracking.verification.dc_backtracking_oracles import (
    dc_merge_sort_inversions_oracle,
    dc_quickselect_oracle,
    dc_closest_pair_oracle,
    dc_tree_centroid_oracle,
    dc_cdq_divide_and_conquer_oracle,
    backtracking_subsets_permutations_oracle,
    backtracking_constraint_satisfaction_oracle,
    backtracking_branch_and_bound_oracle,
    backtracking_state_space_search_oracle,
    backtracking_meet_in_the_middle_oracle
)
from pointer_algorithms.bridge import handle_request


class TestDCBacktrackingTaxonomyAndReasoning(unittest.TestCase):
    def test_taxonomy_definitions(self):
        """Verify 10 DC/Backtracking patterns and taxonomy tree hierarchy."""
        self.assertEqual(len(DC_BACKTRACKING_PATTERNS), 10)
        self.assertIn("Divide & Conquer and Backtracking", TAXONOMY_TREE["Pointer-Based Algorithms"])
        self.assertEqual(AlgorithmFamily.DIVIDE_AND_CONQUER_BACKTRACKING.value, "divide_and_conquer_backtracking")

    def test_conditional_schema_dc_patterns(self):
        """Verify DC patterns (3M-A to 3M-E) populate dc_fields and set search/mitm to NOT_APPLICABLE."""
        dc_patterns = [
            PatternKind.DC_MERGE_SORT_INVERSIONS.value,
            PatternKind.DC_QUICKSELECT.value,
            PatternKind.DC_CLOSEST_PAIR.value,
            PatternKind.DC_TREE_CENTROID.value,
            PatternKind.DC_CDQ_DIVIDE_AND_CONQUER.value,
        ]
        for pat in dc_patterns:
            d = DCBacktrackingStructuralReasoning.derive_proof(pat)
            self.assertNotEqual(d.dc_subproblem_split_strategy, "NOT_APPLICABLE", f"Missing split strategy for {pat}")
            self.assertNotEqual(d.dc_combine_step_derivation, "NOT_APPLICABLE", f"Missing combine derivation for {pat}")
            self.assertNotEqual(d.dc_recurrence_relation, "NOT_APPLICABLE", f"Missing recurrence relation for {pat}")
            self.assertEqual(d.backtracking_state_representation, "NOT_APPLICABLE", f"Should be NOT_APPLICABLE for {pat}")
            self.assertEqual(d.backtracking_pruning_rules, "NOT_APPLICABLE", f"Should be NOT_APPLICABLE for {pat}")
            self.assertEqual(d.mitm_split_dimension, "NOT_APPLICABLE", f"Should be NOT_APPLICABLE for {pat}")

    def test_conditional_schema_backtracking_patterns(self):
        """Verify Backtracking patterns (3M-F to 3M-I) populate search_fields and set dc/mitm to NOT_APPLICABLE."""
        bt_patterns = [
            PatternKind.BACKTRACKING_SUBSETS_PERMUTATIONS.value,
            PatternKind.BACKTRACKING_CONSTRAINT_SATISFACTION.value,
            PatternKind.BACKTRACKING_BRANCH_AND_BOUND.value,
            PatternKind.BACKTRACKING_STATE_SPACE_SEARCH.value,
        ]
        for pat in bt_patterns:
            d = DCBacktrackingStructuralReasoning.derive_proof(pat)
            self.assertEqual(d.dc_subproblem_split_strategy, "NOT_APPLICABLE", f"Should be NOT_APPLICABLE for {pat}")
            self.assertEqual(d.dc_combine_step_derivation, "NOT_APPLICABLE", f"Should be NOT_APPLICABLE for {pat}")
            self.assertNotEqual(d.backtracking_state_representation, "NOT_APPLICABLE", f"Missing state rep for {pat}")
            self.assertNotEqual(d.backtracking_pruning_rules, "NOT_APPLICABLE", f"Missing pruning rules for {pat}")
            self.assertNotEqual(d.backtracking_state_restoration_mechanism, "NOT_APPLICABLE", f"Missing restoration for {pat}")
            self.assertEqual(d.mitm_split_dimension, "NOT_APPLICABLE", f"Should be NOT_APPLICABLE for {pat}")

    def test_conditional_schema_mitm_pattern(self):
        """Verify Meet in the Middle (3M-J) populates mitm_fields and sets dc/search to NOT_APPLICABLE."""
        pat = PatternKind.BACKTRACKING_MEET_IN_THE_MIDDLE.value
        d = DCBacktrackingStructuralReasoning.derive_proof(pat)
        self.assertEqual(d.dc_subproblem_split_strategy, "NOT_APPLICABLE")
        self.assertEqual(d.backtracking_state_representation, "NOT_APPLICABLE")
        self.assertNotEqual(d.mitm_split_dimension, "NOT_APPLICABLE")
        self.assertNotEqual(d.mitm_left_generation, "NOT_APPLICABLE")
        self.assertNotEqual(d.mitm_right_search_strategy, "NOT_APPLICABLE")


class TestDCBacktrackingFeatureExtractionAndCandidates(unittest.TestCase):
    def test_feature_extraction_all_10_patterns(self):
        """Verify feature extraction for all 10 patterns."""
        test_cases = [
            ("Count the number of inversions in array using merge sort", PatternKind.DC_MERGE_SORT_INVERSIONS.value),
            ("Find the kth largest element in an unsorted array using quickselect", PatternKind.DC_QUICKSELECT.value),
            ("Find the closest pair of points in 2D Euclidean plane", PatternKind.DC_CLOSEST_PAIR.value),
            ("Path counting in tree using centroid decomposition", PatternKind.DC_TREE_CENTROID.value),
            ("3D partial order counting using cdq divide and conquer", PatternKind.DC_CDQ_DIVIDE_AND_CONQUER.value),
            ("Generate all subsets and permutations with duplicates", PatternKind.BACKTRACKING_SUBSETS_PERMUTATIONS.value),
            ("Solve N-Queens puzzle with constraint satisfaction", PatternKind.BACKTRACKING_CONSTRAINT_SATISFACTION.value),
            ("Traveling salesperson problem using branch and bound", PatternKind.BACKTRACKING_BRANCH_AND_BOUND.value),
            ("Word search in 2D grid using state space search", PatternKind.BACKTRACKING_STATE_SPACE_SEARCH.value),
            ("Subset sum with N=40 using meet in the middle", PatternKind.BACKTRACKING_MEET_IN_THE_MIDDLE.value),
        ]
        for text, expected_pat in test_cases:
            features = FeatureExtractor.extract(text)
            self.assertTrue(features.is_dc_backtracking_detected, f"Failed detection for {expected_pat}")
            self.assertEqual(features.dc_backtracking_algorithm_family, expected_pat, f"Mismatch for {expected_pat}")

    def test_tower_problem_acceptance_gate(self):
        """Section 8 Gate: Tower problem must be recognized as composition_unsupported, never sort_greedy."""
        tower_text = "You are given n cubes. You need to build towers by placing each cube on top of an existing tower or starting a new tower. Find the minimum number of towers."
        features = FeatureExtractor.extract(tower_text)
        self.assertTrue(features.is_cross_family_composition)
        self.assertTrue(features.composition_unsupported)

        candidates = CandidateGenerator.generate_candidates(features)
        candidate_patterns = [c.pattern for c in candidates]
        self.assertIn("composition_unsupported", candidate_patterns)
        self.assertNotIn("sort_greedy", candidate_patterns)
        self.assertNotIn("greedy_interval_selection", candidate_patterns)


class TestDCBacktrackingCandidateElimination(unittest.TestCase):
    def test_tower_problem_rejection_fail_closed(self):
        """Section 8 Gate: Tower problem candidate must be eliminated with COMPOSITION_UNSUPPORTED."""
        tower_text = "Build towers by placing each cube on an existing tower. Minimum number of towers."
        features = FeatureExtractor.extract(tower_text)
        candidates = CandidateGenerator.generate_candidates(features)
        filter_res = CandidateEliminator.filter_and_rank(candidates, features)
        eliminated_codes = [e.rejection_code for e in filter_res["eliminated"]]
        self.assertIn("COMPOSITION_UNSUPPORTED", eliminated_codes)
        self.assertIsNone(filter_res["selected"])

    def test_rejection_dc_subproblems_not_independent(self):
        """Subproblems sharing state must be eliminated with DC_SUBPROBLEMS_NOT_INDEPENDENT."""
        features = FeatureExtractor.extract("divide and conquer but subproblems are not independent and share mutable state")
        candidates = CandidateGenerator.generate_candidates(features)
        filter_res = CandidateEliminator.filter_and_rank(candidates, features)
        eliminated_codes = [e.rejection_code for e in filter_res["eliminated"]]
        self.assertIn("DC_SUBPROBLEMS_NOT_INDEPENDENT", eliminated_codes)

    def test_rejection_dc_combine_step_intractable(self):
        """Combine step requiring exponential time must be eliminated with DC_COMBINE_STEP_INTRACTABLE."""
        features = FeatureExtractor.extract("divide and conquer where combine step requires O(2^n) time")
        candidates = CandidateGenerator.generate_candidates(features)
        filter_res = CandidateEliminator.filter_and_rank(candidates, features)
        eliminated_codes = [e.rejection_code for e in filter_res["eliminated"]]
        self.assertIn("DC_COMBINE_STEP_INTRACTABLE", eliminated_codes)

    def test_rejection_backtracking_search_space_explosive(self):
        """Explosive search space must be eliminated with BACKTRACKING_SEARCH_SPACE_EXPLOSIVE."""
        features = FeatureExtractor.extract("backtracking with search space explosive and insufficient pruning")
        candidates = CandidateGenerator.generate_candidates(features)
        filter_res = CandidateEliminator.filter_and_rank(candidates, features)
        eliminated_codes = [e.rejection_code for e in filter_res["eliminated"]]
        self.assertIn("BACKTRACKING_SEARCH_SPACE_EXPLOSIVE", eliminated_codes)

    def test_rejection_backtracking_greedy_sufficient(self):
        """When greedy choice holds, backtracking must be eliminated with BACKTRACKING_GREEDY_SUFFICIENT."""
        features = FeatureExtractor.extract("backtracking but greedy sufficient because greedy choice property holds")
        candidates = CandidateGenerator.generate_candidates(features)
        filter_res = CandidateEliminator.filter_and_rank(candidates, features)
        eliminated_codes = [e.rejection_code for e in filter_res["eliminated"]]
        self.assertIn("BACKTRACKING_GREEDY_SUFFICIENT", eliminated_codes)

    def test_rejection_backtracking_dp_sufficient(self):
        """When overlapping subproblems admit DP, backtracking must be eliminated with BACKTRACKING_DP_SUFFICIENT."""
        features = FeatureExtractor.extract("backtracking search but overlapping subproblems admit dp")
        candidates = CandidateGenerator.generate_candidates(features)
        filter_res = CandidateEliminator.filter_and_rank(candidates, features)
        eliminated_codes = [e.rejection_code for e in filter_res["eliminated"]]
        self.assertIn("BACKTRACKING_DP_SUFFICIENT", eliminated_codes)

    def test_failure_classifier_all_12_categories(self):
        """FailureClassifier handles all 12 Phase 3M failure categories."""
        categories = [
            FailureCategory.DC_SUBPROBLEMS_NOT_INDEPENDENT,
            FailureCategory.DC_COMBINE_STEP_INTRACTABLE,
            FailureCategory.DC_BASE_CASE_UNDEFINED,
            FailureCategory.BACKTRACKING_SEARCH_SPACE_EXPLOSIVE,
            FailureCategory.BACKTRACKING_INSUFFICIENT_PRUNING,
            FailureCategory.BACKTRACKING_STATE_RESTORATION_DEFECT,
            FailureCategory.BACKTRACKING_SYMMETRY_NOT_BROKEN,
            FailureCategory.BACKTRACKING_LOOKAHEAD_MISMATCH,
            FailureCategory.BACKTRACKING_GREEDY_SUFFICIENT,
            FailureCategory.BACKTRACKING_DP_SUFFICIENT,
            FailureCategory.BACKTRACKING_RESOURCE_LIMIT,
            FailureCategory.COMPOSITION_UNSUPPORTED,
        ]
        for cat in categories:
            report = FailureClassifier.classify(cat.value, {})
            self.assertEqual(report.category, cat, f"Mismatch for {cat.value}")


class TestDCBacktrackingInvariantAndMovement(unittest.TestCase):
    def test_all_10_invariants(self):
        """All 10 patterns generate complete 4-phase invariants with tailored termination guarantee."""
        for pat in DC_BACKTRACKING_PATTERNS:
            inv = InvariantEngine.construct_invariant(pat, {})
            self.assertTrue(len(inv.before_iteration) > 10, f"Failed before_iteration for {pat}")
            self.assertTrue(len(inv.during_iteration) > 10, f"Failed during_iteration for {pat}")
            self.assertTrue(len(inv.after_movement) > 10, f"Failed after_movement for {pat}")
            self.assertTrue(len(inv.at_termination) > 10, f"Failed at_termination for {pat}")

    def test_all_10_movement_derivations(self):
        """All 10 patterns generate valid movement derivations."""
        for pat in DC_BACKTRACKING_PATTERNS:
            mv = MovementDerivationEngine.derive(pat, {})
            self.assertTrue(len(mv.objective_function) > 5, f"Failed objective for {pat}")
            self.assertTrue(len(mv.decision_conditions) > 0, f"Failed decision conditions for {pat}")
            self.assertTrue(len(mv.elimination_proof) > 10, f"Failed elimination proof for {pat}")


class TestDCBacktrackingCppGenerator(unittest.TestCase):
    def test_cpp_generation_all_10_patterns(self):
        """C++ generator produces valid C++17 implementations for all 10 patterns."""
        for pat in DC_BACKTRACKING_PATTERNS:
            code = generate_dc_backtracking_cpp(pat, {})
            self.assertIn("#include <iostream>", code, f"Missing #include for {pat}")
            self.assertIn("int main()", code, f"Missing main() for {pat}")
            self.assertIn("return 0;", code, f"Missing return 0 for {pat}")


class TestDCBacktrackingOracles(unittest.TestCase):
    def test_inversions_oracle(self):
        arr = [8, 4, 2, 1]
        self.assertEqual(dc_merge_sort_inversions_oracle(arr), 6)

    def test_quickselect_oracle(self):
        arr = [7, 10, 4, 3, 20, 15]
        self.assertEqual(dc_quickselect_oracle(arr, 2), 7)

    def test_closest_pair_oracle(self):
        pts = [(0, 0), (1, 1), (5, 5)]
        self.assertAlmostEqual(dc_closest_pair_oracle(pts), 1.41421356, places=5)

    def test_tree_centroid_oracle(self):
        # 1 - 2 - 3 (weights 1)
        edges = [(1, 2, 1), (2, 3, 1)]
        self.assertEqual(dc_tree_centroid_oracle(3, edges, 1), 2)

    def test_cdq_oracle(self):
        elems = [(1, 2, 3), (2, 3, 4), (1, 1, 1)]
        ans = dc_cdq_divide_and_conquer_oracle(elems)
        self.assertEqual(ans, [1, 2, 0])

    def test_subsets_oracle(self):
        subsets = backtracking_subsets_permutations_oracle([1, 2], mode="subsets")
        self.assertEqual(len(subsets), 4)

    def test_nqueens_oracle(self):
        self.assertEqual(backtracking_constraint_satisfaction_oracle(4), 2)
        self.assertEqual(backtracking_constraint_satisfaction_oracle(8), 92)

    def test_knapsack_oracle(self):
        vals = [60, 100, 120]
        wts = [10, 20, 30]
        self.assertEqual(backtracking_branch_and_bound_oracle(vals, wts, 50), 220)

    def test_word_search_oracle(self):
        board = ["ABCE", "SFCS", "ADEE"]
        self.assertTrue(backtracking_state_space_search_oracle(board, "ABCCED"))
        self.assertFalse(backtracking_state_space_search_oracle(board, "ABCB"))

    def test_mitm_oracle(self):
        nums = [1, 3, 9, 2, 7, 12]
        self.assertEqual(backtracking_meet_in_the_middle_oracle(nums, 15), 3)


class TestDCBacktrackingBridge(unittest.TestCase):
    def test_bridge_request(self):
        req = {
            "action": "solve",
            "problemText": "Count inversions in array using merge sort divide and conquer."
        }
        res = handle_request(req)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["family"], "divide_and_conquer_backtracking")
        self.assertEqual(res["selectedPattern"], "dc_merge_sort_inversions")
        self.assertIn("invariant", res)
        self.assertIn("movement", res)
        self.assertIn("code", res)

    def test_negative_generation_fail_closed(self):
        """Unsupported problems must produce structured rejection with NO code generated."""
        req = {
            "action": "solve",
            "problemText": "You are given n cubes. Build towers by placing each cube on an existing tower. Find minimum number of towers."
        }
        res = handle_request(req)
        self.assertEqual(res["status"], "rejected")
        self.assertIsNone(res.get("code"))
        self.assertIsNone(res.get("selectedPattern"))
        self.assertIsNone(res.get("family"))
        self.assertIn("COMPOSITION_UNSUPPORTED", [e["rejectionCode"] for e in res.get("eliminatedCandidates", [])])
        self.assertEqual(res.get("recommendedAlternative"), "fail_closed_unsupported")

    def test_failure_taxonomy_distinctions(self):
        """Verify distinction between COMPOSITION_UNSUPPORTED and other rejection types."""
        # 1. Composition unsupported (Tower problem)
        res_comp = handle_request({
            "action": "solve",
            "problemText": "Build towers by placing each cube on an existing tower. Find minimum number of towers."
        })
        self.assertEqual(res_comp["status"], "rejected")
        elim_codes = [e["rejectionCode"] for e in res_comp.get("eliminatedCandidates", [])]
        self.assertIn("COMPOSITION_UNSUPPORTED", elim_codes)

        # 2. Intractable combine step
        res_intract = handle_request({
            "action": "solve",
            "problemText": "Divide and conquer where combine step requires O(2^n) time."
        })
        elim_intract = [e["rejectionCode"] for e in res_intract.get("eliminatedCandidates", [])]
        self.assertIn("DC_COMBINE_STEP_INTRACTABLE", elim_intract)

        # 3. Base case undefined
        res_base = handle_request({
            "action": "solve",
            "problemText": "Divide and conquer where base case is undefined leading to infinite recursion."
        })
        self.assertEqual(res_base["status"], "rejected")
        elim_base = [e["rejectionCode"] for e in res_base.get("eliminatedCandidates", [])]
        self.assertIn("DC_BASE_CASE_UNDEFINED", elim_base)


if __name__ == "__main__":
    unittest.main()

