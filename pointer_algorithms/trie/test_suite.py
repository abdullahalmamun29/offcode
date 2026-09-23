"""
Unit Test Suite for Trie Algorithmic Domain (Phase 3D).
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.recognition.feature_extractor import FeatureExtractor
from pointer_algorithms.recognition.candidate_generator import CandidateGenerator
from pointer_algorithms.recognition.candidate_eliminator import CandidateEliminator
from pointer_algorithms.knowledge.taxonomy import TrieKind, TrieAlphabetKind, TrieStorageKind
from pointer_algorithms.reasoning.reasoning_engine import (
    MonotonicityReasoning, GreedyChoiceReasoning, StateTransitionReasoning, InvariantReasoning
)
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine
from pointer_algorithms.generator.cpp_generator import CppPointerGenerator
from pointer_algorithms.failure_analysis.classifier import FailureClassifier, FailureCategory

class TestTrieDomain(unittest.TestCase):

    def test_01_feature_extraction_character_trie(self):
        prob = "Implement a trie with insert, search, and startsWith methods."
        features = FeatureExtractor.extract(prob)
        self.assertEqual(features.trie_kind, TrieKind.CHARACTER_TRIE)
        self.assertEqual(features.prefix_query_type, "exact_search")
        self.assertEqual(features.trie_alphabet, TrieAlphabetKind.LOWERCASE_26)
        self.assertEqual(features.trie_storage, TrieStorageKind.FIXED_ARRAY)
        self.assertTrue(features.has_prefix_sharing_advantage)

    def test_02_feature_extraction_binary_trie(self):
        prob = "Find maximum bitwise XOR of two numbers in an array using a binary trie."
        features = FeatureExtractor.extract(prob)
        self.assertEqual(features.trie_kind, TrieKind.BINARY_TRIE)
        self.assertEqual(features.prefix_query_type, "max_xor_pair")
        self.assertEqual(features.trie_alphabet, TrieAlphabetKind.BINARY_2)
        self.assertEqual(features.trie_storage, TrieStorageKind.FIXED_ARRAY)

    def test_03_candidate_generation_and_ranking(self):
        prob = "Given a dictionary of words, sort all words in lexicographical order."
        features = FeatureExtractor.extract(prob)
        candidates = CandidateGenerator.generate_candidates(features)
        self.assertTrue(any(c.family == "trie" for c in candidates))
        
        ranked = CandidateEliminator.filter_and_rank(candidates, features)
        self.assertIsNotNone(ranked["selected"])
        self.assertEqual(ranked["selected"].candidate.family, "trie")

    def test_04_suboptimal_candidate_handling(self):
        # A naive linear scan candidate must be marked is_suboptimal=True, NOT accepted=False
        prob = "Find target in sorted array using binary search."
        features = FeatureExtractor.extract(prob)
        candidates = CandidateGenerator.generate_candidates(features)
        evals = [CandidateEliminator.evaluate_candidate(c, features) for c in candidates]
        
        naive_evals = [e for e in evals if e.candidate.pattern == "linear_scan_lookup"]
        self.assertTrue(len(naive_evals) > 0)
        self.assertTrue(naive_evals[0].accepted)
        self.assertTrue(naive_evals[0].is_suboptimal)

    def test_05_greedy_choice_proof(self):
        proof = GreedyChoiceReasoning.prove_xor_greedy_choice(32)
        self.assertEqual(proof.bit_width, 32)
        self.assertFalse(proof.requires_backtracking)
        self.assertIn("2^k - 1 < 2^k", proof.mathematical_justification)

    def test_06_state_transition_and_invariants(self):
        trans = StateTransitionReasoning.explain_prefix_traversal("lowercase_26")
        self.assertIn("O(L)", trans.time_complexity_per_op)
        
        invs = InvariantReasoning.get_trie_invariants()
        self.assertIn("pass_count", invs.multiplicity_invariant)
        self.assertIn("word_count", invs.terminal_state_invariant)
        self.assertIn("safe", invs.safe_pruning_invariant.lower())

    def test_07_formal_invariants_generation(self):
        inv = InvariantEngine.construct_invariant("trie_deletion", {})
        self.assertIn("pass_count", inv.during_iteration)
        self.assertIn("pruning", inv.at_termination)

    def test_08_movement_derivation(self):
        mov = MovementDerivationEngine.derive("trie_max_xor_pair", {})
        self.assertIn("1 - bit", mov.elimination_proof)

    def test_09_failure_classifier_trie_categories(self):
        res = FailureClassifier.classify("DUAL_COUNTER_MISMATCH", {})
        self.assertEqual(res.category, FailureCategory.TR_DUAL_COUNTER_CORRUPTION)

        res2 = FailureClassifier.classify("XOR_BRANCH_ERROR", {})
        self.assertEqual(res2.category, FailureCategory.TR_GREEDY_XOR_WRONG_BRANCH)

    def test_10_bridge_ipc_response(self):
        prob = "Implement a trie supporting insert and startsWith."
        resp = handle_request({"problemText": prob})
        self.assertEqual(resp["status"], "success")
        self.assertEqual(resp["family"], "trie")
        self.assertIsNotNone(resp.get("trie"))
        self.assertIsNotNone(resp.get("code"))


if __name__ == "__main__":
    unittest.main()
