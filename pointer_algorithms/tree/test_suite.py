"""
Unit Test Suite for Tree Algorithmic Knowledge Domain (Phase 3E).
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from pointer_algorithms.knowledge.taxonomy import (
    TreeKind, TreeRepresentation, TreeTraversalOrder, PatternKind, TREE_PATTERNS
)
from pointer_algorithms.recognition.feature_extractor import FeatureExtractor
from pointer_algorithms.recognition.candidate_generator import CandidateGenerator
from pointer_algorithms.recognition.candidate_eliminator import CandidateEliminator
from pointer_algorithms.reasoning.reasoning_engine import (
    RecursiveStateReasoning, HierarchyReasoning, ParentChildInvariant, SubtreeAggregation
)
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine
from pointer_algorithms.failure_analysis.classifier import FailureClassifier, FailureCategory
from pointer_algorithms.bridge import handle_request, ALGORITHMIC_FAMILIES, POINTER_FAMILIES

class TestTreeDomain(unittest.TestCase):

    def test_taxonomy_registration(self):
        self.assertIn("tree", ALGORITHMIC_FAMILIES)
        self.assertIn("tree", POINTER_FAMILIES)
        self.assertGreaterEqual(len(TREE_PATTERNS), 20)

    def test_feature_extractor_tree_properties(self):
        f = FeatureExtractor.extract("Given a binary search tree root, find if key 42 exists.")
        self.assertTrue(f.is_bst)
        self.assertFalse(f.is_validating_bst)
        self.assertEqual(f.tree_kind, TreeKind.BST)
        self.assertEqual(f.tree_representation, TreeRepresentation.BINARY_POINTERS)

    def test_feature_extractor_bst_validation(self):
        f = FeatureExtractor.extract("Validate BST: check if the binary search tree is valid.")
        self.assertTrue(f.is_validating_bst)
        self.assertTrue(f.is_bst)

    def test_hierarchy_reasoning_acyclic_proof(self):
        # N=5, E=4, connected -> Tree
        proof = HierarchyReasoning.prove_connected_acyclic(5, 4, True)
        self.assertTrue(proof["is_tree"])
        self.assertEqual(proof["reason"], "VALID_TREE")

        # N=5, E=5 -> Cyclic
        proof_cycle = HierarchyReasoning.prove_connected_acyclic(5, 5, True)
        self.assertFalse(proof_cycle["is_tree"])
        self.assertEqual(proof_cycle["reason"], "CYCLIC")

        # N=5, E=3 -> Disconnected
        proof_disc = HierarchyReasoning.prove_connected_acyclic(5, 3, False)
        self.assertFalse(proof_disc["is_tree"])
        self.assertEqual(proof_disc["reason"], "DISCONNECTED")

    def test_parent_child_invariant(self):
        expl = ParentChildInvariant.explain_parent_tracking()
        self.assertIn("v != p", expl)
        self.assertIn("visited", expl)

    def test_recursive_state_reasoning(self):
        dp = RecursiveStateReasoning.bottom_up_state("size", "1 + sum", "null = 0")
        self.assertEqual(dp.extensible_direction, "bottom_up")
        reroot = RecursiveStateReasoning.rerooted_state("down", "up", "combine")
        self.assertEqual(reroot.extensible_direction, "rerooted")

    def test_candidate_generator_bst_search(self):
        f = FeatureExtractor.extract("Given a binary search tree, search for value x.")
        cands = CandidateGenerator.generate_candidates(f)
        pat_names = [c.pattern for c in cands]
        self.assertIn(PatternKind.TREE_BST_SEARCH.value, pat_names)

    def test_candidate_generator_lca_distinction(self):
        f_bst = FeatureExtractor.extract("Given a binary search tree, find LCA of p and q.")
        cands_bst = CandidateGenerator.generate_candidates(f_bst)
        pat_names_bst = [c.pattern for c in cands_bst]
        self.assertIn(PatternKind.TREE_LCA_BST.value, pat_names_bst)

        f_bt = FeatureExtractor.extract("Given a binary tree, find lowest common ancestor of p and q.")
        cands_bt = CandidateGenerator.generate_candidates(f_bt)
        pat_names_bt = [c.pattern for c in cands_bt]
        self.assertIn(PatternKind.TREE_LCA_BINARY_TREE.value, pat_names_bt)

    def test_candidate_eliminator_cycle_rejection(self):
        f = FeatureExtractor.extract("Graph has redundant connection forming a cycle, compute tree traversal.")
        cands = CandidateGenerator.generate_candidates(f)
        res = CandidateEliminator.filter_and_rank(cands, f)
        self.assertFalse(any(e.accepted for e in res["eliminated"] if e.candidate.family == "tree"))
        elim_codes = [e.rejection_code for e in res["eliminated"]]
        self.assertIn("TREE_CYCLIC_GRAPH", elim_codes)

    def test_candidate_eliminator_bst_violation(self):
        f = FeatureExtractor.extract("Given an unordered binary tree without BST invariant, use bst_search.")
        cands = CandidateGenerator.generate_candidates(f)
        res = CandidateEliminator.filter_and_rank(cands, f)
        elim_codes = [e.rejection_code for e in res["eliminated"]]
        self.assertIn("TREE_INVALID_BST_STRUCTURE", elim_codes)

    def test_movement_derivation_bst_ordered_branch_elimination(self):
        mov = MovementDerivationEngine.derive("tree_bst_search", {})
        self.assertIn("BST ordered-branch elimination", mov.objective_function)
        self.assertIn("BST Ordered-Branch Elimination Proof", mov.elimination_proof)

    def test_failure_classifier_tree_categories(self):
        cls1 = FailureClassifier.classify("TREE_CYCLIC_GRAPH", {})
        self.assertEqual(cls1.category, FailureCategory.TREE_CYCLIC_GRAPH)
        cls2 = FailureClassifier.classify("RECURSION_LIMIT_EXCEEDED", {})
        self.assertEqual(cls2.category, FailureCategory.TREE_RECURSION_LIMIT_EXCEEDED)

    def test_bridge_handshake_tree_payload(self):
        resp = handle_request({"problemText": "Given a binary search tree root, find if value x exists."})
        self.assertEqual(resp["status"], "success")
        self.assertEqual(resp["family"], "tree")
        self.assertIsNotNone(resp.get("tree"))
        self.assertEqual(resp["tree"]["kind"], "bst")

if __name__ == "__main__":
    unittest.main()
