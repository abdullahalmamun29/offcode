"""
Comprehensive Unit Test Suite for CHUP Phase 3L: Greedy Algorithms
Tests:
- Greedy Taxonomy & Enums (GreedyKind, GreedyProofKind, GREEDY_PATTERNS, TAXONOMY_TREE)
- Feature Extractor (Greedy features correctly extracted from problem text)
- Candidate Generator (generates candidates across all 10 Greedy patterns)
- Candidate Eliminator & Failure Analysis (all 11 Greedy rejection codes)
- Structural Reasoning (GreedyStructuralReasoning derives complete 14-field proof)
- Invariant Engine construction across all 10 Greedy patterns
- Movement Derivation across all 10 Greedy patterns
- C++ generator syntax and validity across all 10 patterns
- Reference oracles verification against independent solutions
- Bridge integration and structured greedy metadata emission
"""

import unittest
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.knowledge.taxonomy import (
    GreedyKind,
    GreedyProofKind,
    GREEDY_PATTERNS,
    PatternKind,
    AlgorithmFamily,
    TAXONOMY_TREE
)
from pointer_algorithms.reasoning.reasoning_engine import (
    GreedyStructuralReasoning,
)
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine
from pointer_algorithms.recognition.candidate_generator import CandidateGenerator
from pointer_algorithms.recognition.candidate_eliminator import CandidateEliminator
from pointer_algorithms.recognition.feature_extractor import ProblemFeatures, FeatureExtractor
from pointer_algorithms.failure_analysis.classifier import FailureClassifier, FailureCategory
from pointer_algorithms.generator.greedy_cpp_generator import generate_greedy_cpp
from pointer_algorithms.greedy.verification.greedy_oracles import (
    greedy_interval_selection_oracle,
    greedy_interval_covering_oracle,
    greedy_fractional_knapsack_oracle,
    greedy_deadline_scheduling_oracle,
    greedy_heap_assisted_oracle,
    greedy_huffman_merge_oracle,
    greedy_sequence_local_choice_oracle,
    greedy_reachability_partition_oracle,
    greedy_graph_mst_oracle,
    greedy_general_exchange_oracle
)
from pointer_algorithms.bridge import handle_request


class TestGreedyTaxonomyAndReasoning(unittest.TestCase):
    def test_taxonomy_definitions(self):
        """Verify 10 Greedy patterns and hierarchy."""
        self.assertEqual(len(GREEDY_PATTERNS), 10)
        self.assertIn("Greedy Algorithms", TAXONOMY_TREE["Pointer-Based Algorithms"])
        self.assertEqual(AlgorithmFamily.GREEDY.value, "greedy")

    def test_structural_reasoning_16_fields(self):
        """Verify GreedyStructuralReasoning addresses all 16 Core Greedy Reasoning Fields."""
        for pattern in GREEDY_PATTERNS:
            derivation = GreedyStructuralReasoning.derive_greedy_proof(pattern)
            self.assertTrue(len(derivation.pattern) > 0, f"Failed pattern for {pattern}")
            self.assertTrue(len(derivation.problem_objective) > 5, f"Failed problem objective for {pattern}")
            self.assertTrue(len(derivation.feasibility_constraints) > 5, f"Failed feasibility constraints for {pattern}")
            self.assertTrue(len(derivation.candidate_local_choice) > 5, f"Failed local choice for {pattern}")
            self.assertTrue(len(derivation.ordering_priority_rule) > 5, f"Failed ordering rule for {pattern}")
            self.assertTrue(len(derivation.safe_choice_hypothesis) > 5, f"Failed safe choice hypothesis for {pattern}")
            self.assertTrue(len(derivation.proof_method) > 5, f"Failed proof method for {pattern}")
            self.assertTrue(len(derivation.proof_derivation) > 5, f"Failed proof derivation for {pattern}")
            self.assertTrue(len(derivation.feasibility_preservation) > 5, f"Failed feasibility preservation for {pattern}")
            self.assertTrue(len(derivation.greedy_invariant) > 5, f"Failed greedy invariant for {pattern}")
            self.assertTrue(len(derivation.termination_condition) > 5, f"Failed termination condition for {pattern}")
            self.assertTrue(len(derivation.global_correctness_argument) > 5, f"Failed correctness argument for {pattern}")
            self.assertTrue(len(derivation.time_complexity_derivation) > 5, f"Failed time complexity for {pattern}")
            self.assertTrue(len(derivation.space_complexity_derivation) > 5, f"Failed space complexity for {pattern}")
            self.assertTrue(len(derivation.competing_families) > 5, f"Failed competing families for {pattern}")
            self.assertTrue(len(derivation.why_competing_not_selected) > 5, f"Failed why competing not selected for {pattern}")


class TestGreedyFeatureExtractionAndCandidates(unittest.TestCase):
    def test_feature_extraction_interval(self):
        """Verify feature extraction for interval selection."""
        text = "Select maximum number of non-overlapping intervals using earliest finish time greedy."
        features = FeatureExtractor.extract(text)
        self.assertEqual(features.greedy_kind, GreedyKind.INTERVAL_SELECTION)
        self.assertTrue(features.greedy_has_optimal_substructure)
        self.assertTrue(features.greedy_has_greedy_choice)

    def test_candidate_generation_all_10_patterns(self):
        """Verify candidate generation for each greedy pattern."""
        for pattern in GREEDY_PATTERNS:
            features = FeatureExtractor.extract(f"Solve using {pattern} greedy algorithm.")
            candidates = CandidateGenerator.generate_candidates(features)
            patterns_found = [c.pattern for c in candidates]
            self.assertIn(pattern, patterns_found, f"Candidate generator failed to propose {pattern}")


class TestGreedyCandidateElimination(unittest.TestCase):
    def test_rejection_exchange_proof_failed(self):
        """0/1 Knapsack must be eliminated with GREEDY_EXCHANGE_PROOF_FAILED."""
        features = FeatureExtractor.extract("discrete 0/1 knapsack where items are indivisible")
        candidates = CandidateGenerator.generate_candidates(features)
        filter_res = CandidateEliminator.filter_and_rank(candidates, features)
        rejected_codes = [e.rejection_code for e in filter_res["eliminated"]]
        self.assertIn("GREEDY_EXCHANGE_PROOF_FAILED", rejected_codes)

    def test_rejection_counterexample_found(self):
        """Non-canonical coin system must be eliminated with GREEDY_COUNTEREXAMPLE_FOUND."""
        features = FeatureExtractor.extract("non-canonical coin system with denominations 1, 3, 4 for target 6")
        candidates = CandidateGenerator.generate_candidates(features)
        filter_res = CandidateEliminator.filter_and_rank(candidates, features)
        rejected_codes = [e.rejection_code for e in filter_res["eliminated"]]
        self.assertIn("GREEDY_COUNTEREXAMPLE_FOUND", rejected_codes)

    def test_rejection_proof_not_established(self):
        """General set cover must be eliminated with GREEDY_PROOF_NOT_ESTABLISHED."""
        features = FeatureExtractor.extract("general set cover on arbitrary subsets where interval stabbing structure is absent")
        candidates = CandidateGenerator.generate_candidates(features)
        filter_res = CandidateEliminator.filter_and_rank(candidates, features)
        rejected_codes = [e.rejection_code for e in filter_res["eliminated"]]
        self.assertIn("GREEDY_PROOF_NOT_ESTABLISHED", rejected_codes)

    def test_failure_classifier_categories(self):
        """FailureClassifier handles all 11 Greedy rejection categories."""
        for cat in [
            FailureCategory.GREEDY_NO_SAFE_LOCAL_CHOICE,
            FailureCategory.GREEDY_EXCHANGE_PROOF_FAILED,
            FailureCategory.GREEDY_STAYING_AHEAD_FAILED,
            FailureCategory.GREEDY_DOMINANCE_FAILED,
            FailureCategory.GREEDY_LOOKAHEAD_REQUIRED,
            FailureCategory.GREEDY_OBJECTIVE_MISMATCH,
            FailureCategory.GREEDY_COUNTEREXAMPLE_FOUND,
            FailureCategory.GREEDY_PROOF_NOT_ESTABLISHED,
            FailureCategory.GREEDY_MATROID_PREREQUISITE_UNPROVEN,
            FailureCategory.GREEDY_RESOURCE_LIMIT,
            FailureCategory.GREEDY_IMPLEMENTATION_BUG
        ]:
            report = FailureClassifier.classify(cat.value, {})
            self.assertEqual(report.category, cat)


class TestGreedyInvariantAndMovement(unittest.TestCase):
    def test_all_10_patterns_invariants(self):
        """All 10 Greedy patterns must generate complete 4-phase invariants."""
        for pattern in GREEDY_PATTERNS:
            inv = InvariantEngine.construct_invariant(pattern, {})
            self.assertTrue(len(inv.before_iteration) > 10, f"Failed before invariant for {pattern}")
            self.assertTrue(len(inv.during_iteration) > 10, f"Failed during invariant for {pattern}")
            self.assertTrue(len(inv.after_movement) > 10, f"Failed after invariant for {pattern}")
            self.assertTrue(len(inv.at_termination) > 10, f"Failed termination invariant for {pattern}")
            self.assertNotIn("maximal", inv.at_termination.lower(), f"Termination invariant for {pattern} should not use 'maximal'")
            self.assertIn("the construction is complete and the associated correctness proof establishes", inv.at_termination.lower())

        # Test Gas Station reachability partition variant
        inv_gas = InvariantEngine.construct_invariant("greedy_reachability_partition", {"reachability_kind": "gas_station"})
        self.assertIn("tank", inv_gas.during_iteration)
        self.assertIn("surplus", inv_gas.at_termination)
        self.assertNotIn("maximal", inv_gas.at_termination.lower())

    def test_all_10_patterns_movement(self):
        """All 10 Greedy patterns must generate valid movement and state transition models."""
        for pattern in GREEDY_PATTERNS:
            model = MovementDerivationEngine.derive(pattern, {})
            self.assertTrue(len(model.objective_function) > 5, f"Failed objective for {pattern}")
            self.assertTrue(len(model.decision_conditions) > 0, f"Failed decisions for {pattern}")
            self.assertTrue(len(model.elimination_proof) > 10, f"Failed elimination proof for {pattern}")


class TestGreedyCppGenerator(unittest.TestCase):
    def test_cpp_code_generation_all_10_patterns(self):
        """Verify C++ code generation for all 10 Greedy patterns."""
        for pattern in GREEDY_PATTERNS:
            code = generate_greedy_cpp(pattern, {})
            self.assertIn("#include <iostream>", code)
            self.assertIn("int main()", code)
            self.assertIn("return 0;", code)


class TestGreedyOracles(unittest.TestCase):
    def test_interval_selection_oracle(self):
        intervals = [(1, 4), (3, 5), (0, 6), (5, 7)]
        self.assertEqual(greedy_interval_selection_oracle(intervals), 2)

    def test_interval_covering_oracle(self):
        intervals = [(10, 16), (2, 8), (1, 6), (7, 12)]
        self.assertEqual(greedy_interval_covering_oracle(intervals), 2)

    def test_fractional_knapsack_oracle(self):
        items = [(60.0, 10.0), (100.0, 20.0), (120.0, 30.0)]
        self.assertEqual(greedy_fractional_knapsack_oracle(items, 50.0), 240.0)

    def test_deadline_scheduling_oracle(self):
        jobs = [(1, 2), (2, 4), (1, 4), (3, 6)]
        self.assertEqual(greedy_deadline_scheduling_oracle(jobs), 1)

    def test_heap_assisted_oracle(self):
        stations = [(10, 60), (20, 30), (30, 30), (60, 40)]
        self.assertEqual(greedy_heap_assisted_oracle(100, 10, stations), 2)

    def test_huffman_merge_oracle(self):
        freqs = [4, 3, 2, 6]
        self.assertEqual(greedy_huffman_merge_oracle(freqs), 29)

    def test_sequence_local_choice_oracle(self):
        self.assertEqual(greedy_sequence_local_choice_oracle("1432219", 3), "1219")

    def test_reachability_partition_oracle(self):
        self.assertEqual(greedy_reachability_partition_oracle([2, 3, 1, 1, 4]), 2)

    def test_graph_mst_oracle(self):
        edges = [(1, 2, 1), (2, 3, 4), (3, 4, 2), (1, 4, 5), (2, 4, 3)]
        self.assertEqual(greedy_graph_mst_oracle(4, edges), 6)

    def test_general_exchange_oracle(self):
        self.assertEqual(greedy_general_exchange_oracle(["3", "30", "34", "5", "9"]), "9534330")


class TestGreedyBridgeIntegration(unittest.TestCase):
    def test_bridge_greedy_payload(self):
        """Verify handle_request produces complete greedy payload."""
        req = {
            "action": "solve",
            "problemText": "Select maximum number of compatible non-overlapping intervals using earliest finish time greedy activity selection."
        }
        res = handle_request(req)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["family"], "greedy")
        self.assertEqual(res["selectedPattern"], "greedy_interval_selection")
        self.assertIsNotNone(res.get("greedy"))
        greedy_info = res["greedy"]
        self.assertTrue(greedy_info["hasGreedyChoice"])
        self.assertTrue(greedy_info["hasOptimalSubstructure"])
        self.assertIn("code", res)
        self.assertIn("invariant", res)
        self.assertIn("movement", res)


if __name__ == "__main__":
    unittest.main()
