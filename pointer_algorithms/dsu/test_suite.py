"""
Unit Test Suite for Advanced Disjoint Set Union (DSU) Algorithmic Knowledge Domain (Phase 3H).
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from pointer_algorithms.knowledge.taxonomy import (
    DSUKind, DSUOperationKind, AlgorithmFamily, PatternKind,
    DSU_PATTERNS, TAXONOMY_TREE
)
from pointer_algorithms.recognition.feature_extractor import FeatureExtractor
from pointer_algorithms.recognition.candidate_generator import CandidateGenerator
from pointer_algorithms.recognition.candidate_eliminator import CandidateEliminator
from pointer_algorithms.reasoning.reasoning_engine import DSUStructuralReasoning, DSUStructuralProof
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine
from pointer_algorithms.generator.dsu_cpp_generator import generate_dsu_cpp
from pointer_algorithms.failure_analysis.classifier import FailureClassifier, FailureCategory
from pointer_algorithms.bridge import handle_request, ALGORITHMIC_FAMILIES, POINTER_FAMILIES


class TestDSUDomain(unittest.TestCase):

    def test_taxonomy_registration(self):
        self.assertIn("dsu", ALGORITHMIC_FAMILIES)
        self.assertIn("dsu", POINTER_FAMILIES)
        self.assertEqual(AlgorithmFamily.DSU.value, "dsu")
        self.assertEqual(len(DSU_PATTERNS), 10)
        self.assertIn("Disjoint Set Union", TAXONOMY_TREE.get("Pointer-Based Algorithms", {}))

        # Verify DSUKind has exactly BASIC, WEIGHTED, PARITY, ROLLBACK
        self.assertEqual(set(DSUKind), {DSUKind.BASIC, DSUKind.WEIGHTED, DSUKind.PARITY, DSUKind.ROLLBACK})

        # Verify DSUOperationKind contains all core operations
        expected_ops = {
            DSUOperationKind.FIND, DSUOperationKind.UNION, DSUOperationKind.CONNECTED,
            DSUOperationKind.COMPONENT_SIZE, DSUOperationKind.COMPONENT_METADATA,
            DSUOperationKind.DIFF, DSUOperationKind.CONSISTENCY_CHECK,
            DSUOperationKind.SNAPSHOT, DSUOperationKind.ROLLBACK
        }
        self.assertEqual(set(DSUOperationKind), expected_ops)

    def test_structural_reasoning_basic_dsu(self):
        proof = DSUStructuralReasoning.explain("basic")
        self.assertIsInstance(proof, DSUStructuralProof)
        self.assertEqual(proof.dsu_kind, "basic")
        self.assertIn("alpha(n)", proof.representative_invariant.lower())
        self.assertIn("partition", proof.partition_of_universe.lower())

    def test_structural_reasoning_weighted_dsu(self):
        proof = DSUStructuralReasoning.explain("weighted")
        self.assertEqual(proof.dsu_kind, "weighted")
        self.assertIn("potential", proof.weighted_potential_derivation.lower())
        self.assertIn("w - px + py", proof.weighted_potential_derivation)

    def test_structural_reasoning_parity_dsu(self):
        proof = DSUStructuralReasoning.explain("parity")
        self.assertEqual(proof.dsu_kind, "parity")
        self.assertIn("xor", proof.parity_xor_derivation.lower())
        self.assertIn("contradiction", proof.parity_xor_derivation.lower())

    def test_structural_reasoning_rollback_dsu(self):
        proof = DSUStructuralReasoning.explain("rollback")
        self.assertEqual(proof.dsu_kind, "rollback")
        self.assertIn("path compression is strictly omitted", proof.rollback_restoration_invariant.lower())
        self.assertIn("o(log n)", proof.rollback_restoration_invariant.lower())

    def test_structural_reasoning_offline_dynamic_connectivity(self):
        proof = DSUStructuralReasoning.explain("rollback")
        self.assertIn("segment tree over time", proof.offline_dynamic_connectivity_complexity.lower())
        self.assertIn("log q", proof.offline_dynamic_connectivity_complexity.lower())

    def test_structural_limitations_and_elimination_reasons(self):
        proof = DSUStructuralReasoning.explain("basic")
        self.assertIn("arbitrary online edge deletion cannot be handled", proof.limitation_reasoning.lower())
        self.assertIn("DSU_DELETION_UNSUPPORTED", proof.limitation_reasoning)

    def test_invariant_engine_all_patterns(self):
        patterns = [
            "dsu_basic", "dsu_component_metadata", "dsu_dynamic_connectivity",
            "dsu_weighted", "dsu_potential_difference", "dsu_parity",
            "dsu_rollback", "dsu_offline_dynamic_connectivity",
            "dsu_kruskal_support", "dsu_constraint_consistency"
        ]
        for pat in patterns:
            inv = InvariantEngine.construct_invariant(pat, {"dsu_kind": "basic", "dsu_metadata_type": "size"})
            self.assertTrue(len(inv.before_iteration) > 0, f"Empty before_iteration for {pat}")
            self.assertTrue(len(inv.during_iteration) > 0, f"Empty during_iteration for {pat}")
            self.assertTrue(len(inv.after_movement) > 0, f"Empty after_movement for {pat}")
            self.assertTrue(len(inv.at_termination) > 0, f"Empty at_termination for {pat}")

    def test_movement_derivation_all_patterns(self):
        patterns = [
            "dsu_basic", "dsu_component_metadata", "dsu_dynamic_connectivity",
            "dsu_weighted", "dsu_potential_difference", "dsu_parity",
            "dsu_rollback", "dsu_offline_dynamic_connectivity",
            "dsu_kruskal_support", "dsu_constraint_consistency"
        ]
        for pat in patterns:
            mov = MovementDerivationEngine.derive(pat, {"dsu_kind": "basic", "dsu_metadata_type": "size"})
            self.assertTrue(len(mov.objective_function) > 0, f"Empty objective for {pat}")
            self.assertTrue(len(mov.decision_conditions) > 0, f"Empty decision conditions for {pat}")
            self.assertTrue(len(mov.elimination_proof) > 0, f"Empty elimination proof for {pat}")

    def test_cpp_code_generation_all_patterns(self):
        patterns = [
            "dsu_basic", "dsu_component_metadata", "dsu_dynamic_connectivity",
            "dsu_weighted", "dsu_potential_difference", "dsu_parity",
            "dsu_rollback", "dsu_offline_dynamic_connectivity",
            "dsu_kruskal_support", "dsu_constraint_consistency"
        ]
        for pat in patterns:
            code = generate_dsu_cpp(pat, {"dsu_kind": "basic", "dsu_metadata_type": "size"})
            self.assertTrue(len(code) > 200, f"Generated code too short for {pat}")
            self.assertIn("#include <vector>", code)
            self.assertIn("int main()", code)

    def test_candidate_elimination_arbitrary_deletion(self):
        feats = FeatureExtractor.extract("Arbitrary online edge deletion: delete edge between u and v dynamically.")
        self.assertTrue(feats.dsu_is_online_deletions)
        candidates = CandidateGenerator.generate_candidates(feats)
        evals = CandidateEliminator.filter_and_rank(candidates, feats)
        elim_codes = {e.candidate.pattern: e.rejection_code for e in evals["eliminated"]}
        self.assertIn("dsu_basic", elim_codes)
        self.assertEqual(elim_codes["dsu_basic"], "DSU_DELETION_UNSUPPORTED")

    def test_candidate_elimination_rollback_required(self):
        feats = FeatureExtractor.extract("Rollback and undo last merge with snapshot restoration.")
        self.assertTrue(feats.dsu_requires_rollback)
        candidates = CandidateGenerator.generate_candidates(feats)
        evals = CandidateEliminator.filter_and_rank(candidates, feats)
        elim_codes = {e.candidate.pattern: e.rejection_code for e in evals["eliminated"]}
        self.assertIn("dsu_basic", elim_codes)
        self.assertEqual(elim_codes["dsu_basic"], "DSU_ROLLBACK_REQUIRED")

    def test_candidate_elimination_weighted_mismatch(self):
        feats = FeatureExtractor.extract("Maintain relative potential difference value[x] - value[y] = w.")
        self.assertTrue(feats.dsu_has_weights)
        candidates = CandidateGenerator.generate_candidates(feats)
        evals = CandidateEliminator.filter_and_rank(candidates, feats)
        elim_codes = {e.candidate.pattern: e.rejection_code for e in evals["eliminated"]}
        self.assertIn("dsu_basic", elim_codes)
        self.assertEqual(elim_codes["dsu_basic"], "DSU_WEIGHT_MODEL_MISMATCH")

    def test_candidate_elimination_parity_mismatch(self):
        feats = FeatureExtractor.extract("Maintain parity constraints color[x] xor color[y] with dynamic 2-coloring.")
        self.assertTrue(feats.dsu_has_parity)
        candidates = CandidateGenerator.generate_candidates(feats)
        evals = CandidateEliminator.filter_and_rank(candidates, feats)
        elim_codes = {e.candidate.pattern: e.rejection_code for e in evals["eliminated"]}
        self.assertIn("dsu_basic", elim_codes)
        self.assertEqual(elim_codes["dsu_basic"], "DSU_PARITY_MODEL_MISMATCH")

    def test_candidate_elimination_offline_online_mismatch(self):
        feats = FeatureExtractor.extract("Offline dynamic connectivity with edge insertions and deletions where all queries known in advance.")
        self.assertTrue(feats.dsu_is_offline)
        candidates = CandidateGenerator.generate_candidates(feats)
        evals = CandidateEliminator.filter_and_rank(candidates, feats)
        elim_codes = {e.candidate.pattern: e.rejection_code for e in evals["eliminated"]}
        self.assertIn("dsu_basic", elim_codes)
        self.assertEqual(elim_codes["dsu_basic"], "DSU_ONLINE_OFFLINE_MISMATCH")

    def test_failure_classifier_categories(self):
        categories = [
            FailureCategory.DSU_UNKNOWN_STRUCTURAL_PATTERN,
            FailureCategory.DSU_DELETION_UNSUPPORTED,
            FailureCategory.DSU_ONLINE_OFFLINE_MISMATCH,
            FailureCategory.DSU_WEIGHT_MODEL_MISMATCH,
            FailureCategory.DSU_PARITY_MODEL_MISMATCH,
            FailureCategory.DSU_ROLLBACK_REQUIRED,
            FailureCategory.DSU_METADATA_MERGE_UNDEFINED,
            FailureCategory.DSU_CONTRADICTION_DETECTED,
            FailureCategory.DSU_COMPLEXITY_EXCEEDED,
            FailureCategory.DSU_PATH_COMPRESSION_ROLLBACK_CONFLICT,
            FailureCategory.DSU_POTENTIAL_ACCUMULATION_ERROR,
            FailureCategory.DSU_PARITY_XOR_ERROR,
            FailureCategory.DSU_IMPLEMENTATION_BUG,
            FailureCategory.DSU_OUTPUT_ERROR,
        ]
        for cat in categories:
            res = FailureClassifier.classify(cat.value, {})
            self.assertEqual(res.category, cat, f"Mismatch for {cat.value}")

    def test_bridge_request_and_dsu_metadata(self):
        resp = handle_request({"problemText": "Disjoint set union data structure supporting make_set, find, and union operations on elements."})
        self.assertEqual(resp.get("status"), "success")
        self.assertEqual(resp.get("family"), "dsu")
        self.assertEqual(resp.get("selectedPattern"), "dsu_basic")

        dsu_meta = resp.get("dsu")
        self.assertIsNotNone(dsu_meta)
        self.assertEqual(dsu_meta.get("kind"), "basic")
        self.assertEqual(dsu_meta.get("algorithmFamily"), "dsu_basic")

    def test_graph_kruskal_composition_with_dsu(self):
        # Verify Graph Kruskal specifies dsu_disjoint_sets capability in graph metadata
        resp = handle_request({"problemText": "Find minimum spanning tree (MST) using Kruskal algorithm on undirected graph."})
        self.assertEqual(resp.get("status"), "success")
        self.assertEqual(resp.get("family"), "graph")
        self.assertEqual(resp.get("selectedPattern"), "graph_mst_kruskal")

        graph_meta = resp.get("graph")
        self.assertIsNotNone(graph_meta)
        self.assertIn("dsu_disjoint_sets", graph_meta.get("composedCapabilities", []))


if __name__ == "__main__":
    unittest.main()
