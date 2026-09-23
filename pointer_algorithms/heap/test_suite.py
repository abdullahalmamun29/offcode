"""
Unit Test Suite for Heap / Priority Queue Algorithmic Knowledge Domain (Phase 3G).
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from pointer_algorithms.knowledge.taxonomy import (
    HeapKind, HeapOperationKind, AlgorithmFamily, PatternKind,
    HEAP_PATTERNS, TAXONOMY_TREE
)
from pointer_algorithms.recognition.feature_extractor import FeatureExtractor
from pointer_algorithms.recognition.candidate_generator import CandidateGenerator
from pointer_algorithms.recognition.candidate_eliminator import CandidateEliminator
from pointer_algorithms.reasoning.reasoning_engine import HeapStructuralReasoning
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine
from pointer_algorithms.generator.heap_cpp_generator import generate_heap_cpp
from pointer_algorithms.failure_analysis.classifier import FailureClassifier, FailureCategory
from pointer_algorithms.bridge import handle_request, ALGORITHMIC_FAMILIES, POINTER_FAMILIES


class TestHeapDomain(unittest.TestCase):

    def test_taxonomy_registration(self):
        self.assertIn("heap", ALGORITHMIC_FAMILIES)
        self.assertIn("heap", POINTER_FAMILIES)
        self.assertEqual(AlgorithmFamily.HEAP.value, "heap")
        self.assertEqual(len(HEAP_PATTERNS), 11)
        self.assertIn("Heap", TAXONOMY_TREE.get("Pointer-Based Algorithms", {}))
        
        # Verify HeapKind has ONLY MIN_HEAP and MAX_HEAP (no double-ended)
        self.assertEqual(set(HeapKind), {HeapKind.MIN_HEAP, HeapKind.MAX_HEAP})

    def test_heap_structural_reasoning_retention_invariant(self):
        # Top-K largest MUST derive min_heap
        kind_largest = HeapStructuralReasoning.derive_top_k_heap_kind("largest")
        self.assertEqual(kind_largest, "min_heap")

        # Top-K smallest MUST derive max_heap
        kind_smallest = HeapStructuralReasoning.derive_top_k_heap_kind("smallest")
        self.assertEqual(kind_smallest, "max_heap")

        # Explanation check
        proof_min = HeapStructuralReasoning.explain("min_heap")
        self.assertIn("Top-K Largest", proof_min.retention_invariant_top_k)
        self.assertIn("weakest", proof_min.retention_invariant_top_k)

        proof_max = HeapStructuralReasoning.explain("max_heap")
        self.assertIn("Top-K Smallest", proof_max.retention_invariant_top_k)
        self.assertIn("weakest", proof_max.retention_invariant_top_k)

    def test_heap_structural_proof_optimality(self):
        proof = HeapStructuralReasoning.explain("min_heap")
        self.assertIn("O(log N)", proof.sift_up_complexity)
        self.assertIn("O(log N)", proof.sift_down_complexity)
        self.assertIn("O(N)", proof.bottom_up_heapify_complexity)
        self.assertIn("O(1)", proof.extremal_access)
        self.assertIn("flat contiguous array", proof.heap_vs_bst_tradeoff)

    def test_feature_extractor_top_k(self):
        f = FeatureExtractor.extract(
            "Find the top 10 largest elements from a stream of numbers."
        )
        self.assertTrue(f.is_heap_detected)
        self.assertEqual(f.heap_kind, HeapKind.MIN_HEAP)
        self.assertEqual(f.heap_k_direction, "largest")
        self.assertEqual(f.heap_k_value, 10)
        self.assertTrue(f.heap_is_streaming)
        self.assertEqual(f.heap_algorithm_family, "heap_top_k")

    def test_feature_extractor_k_way_merge(self):
        f = FeatureExtractor.extract(
            "Merge K sorted lists into a single sorted list."
        )
        self.assertTrue(f.is_heap_detected)
        self.assertTrue(f.heap_is_k_way_merge)
        self.assertEqual(f.heap_algorithm_family, "heap_k_way_merge")

    def test_feature_extractor_dynamic_median(self):
        f = FeatureExtractor.extract(
            "Continuously find running dynamic median from a data stream."
        )
        self.assertTrue(f.is_heap_detected)
        self.assertTrue(f.heap_is_dynamic_median)
        self.assertEqual(f.heap_algorithm_family, "heap_dynamic_median")

    def test_feature_extractor_scheduling(self):
        f = FeatureExtractor.extract(
            "Given meeting intervals with start and end times, determine minimum conference rooms required."
        )
        self.assertTrue(f.is_heap_detected)
        self.assertTrue(f.heap_is_scheduling)
        self.assertEqual(f.heap_algorithm_family, "heap_scheduling")

    def test_feature_extractor_lazy_deletion(self):
        f = FeatureExtractor.extract(
            "Design a priority queue supporting lazy deletion with tombstone frequencies."
        )
        self.assertTrue(f.is_heap_detected)
        self.assertTrue(f.heap_is_lazy_deletion)
        self.assertEqual(f.heap_algorithm_family, "heap_lazy_deletion")

    def test_candidate_generator_heap(self):
        f = FeatureExtractor.extract("Find top k largest elements from stream.")
        cands = CandidateGenerator.generate_candidates(f)
        pats = [c.pattern for c in cands]
        self.assertIn(PatternKind.HEAP_TOP_K.value, pats)

    def test_candidate_elimination_wrong_extremum(self):
        # A min query attempted with max-heap
        f = FeatureExtractor.extract("Extract minimum elements repeatedly.")
        f.heap_kind = HeapKind.MIN_HEAP
        cands = CandidateGenerator.generate_candidates(f)
        evals = CandidateEliminator.filter_and_rank(cands, f)
        for elim in evals["eliminated"]:
            if elim.candidate.pattern == "heap_max_priority_queue":
                self.assertEqual(elim.rejection_code, "HEAP_WRONG_EXTREMUM")

    def test_candidate_elimination_arbitrary_delete(self):
        f = FeatureExtractor.extract("Find order with arbitrary key deletion by value without tombstones.")
        f.heap_requires_arbitrary_delete = True
        cands = CandidateGenerator.generate_candidates(f)
        evals = CandidateEliminator.filter_and_rank(cands, f)
        for elim in evals["eliminated"]:
            if elim.candidate.pattern in ("heap_min_priority_queue", "heap_max_priority_queue"):
                self.assertEqual(elim.rejection_code, "HEAP_ARBITRARY_DELETE_MISMATCH")

    def test_candidate_elimination_unnecessary_sorting(self):
        f = FeatureExtractor.extract("Return all elements in complete sorted order from static array.")
        f.heap_requires_full_sort = True
        cands = CandidateGenerator.generate_candidates(f)
        evals = CandidateEliminator.filter_and_rank(cands, f)
        for elim in evals["eliminated"]:
            if elim.candidate.pattern in ("heap_top_k", "heap_min_priority_queue"):
                self.assertEqual(elim.rejection_code, "HEAP_UNNECESSARY_SORTING")

    def test_candidate_elimination_complexity_exceeded(self):
        f = FeatureExtractor.extract("Find k-th element in static array of size 10^7 with k=10^6.")
        f.heap_is_offline_kth = True
        cands = CandidateGenerator.generate_candidates(f)
        evals = CandidateEliminator.filter_and_rank(cands, f)
        for elim in evals["eliminated"]:
            if elim.candidate.pattern == "heap_kth_element":
                self.assertEqual(elim.rejection_code, "HEAP_COMPLEXITY_EXCEEDED")

    def test_invariants_and_movement_derivation(self):
        # 4-phase invariant test
        inv = InvariantEngine.construct_invariant("heap_top_k", {})
        self.assertIn("min_heap", inv.during_iteration)
        self.assertIn("K largest", inv.at_termination)

        # Movement derivation test
        m = MovementDerivationEngine.derive("heap_top_k", {})
        self.assertIn("weakest", m.elimination_proof)

        m_med = MovementDerivationEngine.derive("heap_dynamic_median", {})
        self.assertIn("median", m_med.objective_function)

    def test_cpp_code_generation(self):
        for pat in HEAP_PATTERNS:
            code = generate_heap_cpp(pat, {})
            self.assertIn("#include <iostream>", code)
            self.assertTrue("priority_queue" in code or "make_heap" in code)
            self.assertIn("int main()", code)

    def test_failure_classifier(self):
        res = FailureClassifier.classify("HEAP_WRONG_EXTREMUM", {})
        self.assertEqual(res.category, FailureCategory.HEAP_WRONG_EXTREMUM)

    def test_bridge_json_ipc(self):
        req = {
            "action": "classify_and_solve",
            "problemText": "Find top 5 largest elements from an input stream."
        }
        resp = handle_request(req)
        self.assertEqual(resp["family"], "heap")
        self.assertEqual(resp["selectedPattern"], "heap_top_k")
        self.assertIn("code", resp)
        self.assertIn("priority_queue", resp["code"])
        self.assertIn("heap", resp)
        self.assertEqual(resp["heap"]["kind"], "min_heap")

    def test_capability_composition_dijkstra_prim(self):
        # Dijkstra request should compose heap priority frontier capability
        req_dijkstra = {
            "action": "classify_and_solve",
            "problemText": "Find shortest path from source in a weighted directed graph with positive weights."
        }
        resp_dijkstra = handle_request(req_dijkstra)
        self.assertEqual(resp_dijkstra["family"], "graph")
        self.assertEqual(resp_dijkstra["selectedPattern"], "graph_dijkstra")
        self.assertIn("composedCapabilities", resp_dijkstra["graph"])
        self.assertIn("heap_priority_frontier", resp_dijkstra["graph"]["composedCapabilities"])

        # Prim request should compose heap priority frontier capability
        req_prim = {
            "action": "classify_and_solve",
            "problemText": "Compute minimum spanning tree MST using Prim's algorithm on an undirected graph."
        }
        resp_prim = handle_request(req_prim)
        self.assertEqual(resp_prim["family"], "graph")
        self.assertEqual(resp_prim["selectedPattern"], "graph_mst_prim")
        self.assertIn("composedCapabilities", resp_prim["graph"])
        self.assertIn("heap_priority_frontier", resp_prim["graph"]["composedCapabilities"])

    def test_top_k_capacity_invariants(self):
        """
        Verify bounded retention capacity invariants (heap_size <= K, heap_size == min(N, K)):
        Tests for N < K, N == K, N > K, and K == 1.
        """
        from pointer_algorithms.heap.verification.heap_oracles import oracle_top_k

        # 1. N < K (arr size 3, K = 5) -> heap size == 3 <= 5
        arr_small = [10, 5, 20]
        res_small = oracle_top_k(arr_small, k=5, direction="largest")
        self.assertEqual(len(res_small), 3)
        self.assertEqual(res_small, [20, 10, 5])

        # 2. N == K (arr size 4, K = 4) -> heap size == 4 <= 4
        arr_eq = [1, 2, 3, 4]
        res_eq = oracle_top_k(arr_eq, k=4, direction="largest")
        self.assertEqual(len(res_eq), 4)
        self.assertEqual(res_eq, [4, 3, 2, 1])

        # 3. N > K (arr size 7, K = 3) -> heap size <= 3 throughout, exactly 3 at termination
        arr_large = [7, 2, 9, 4, 1, 8, 3]
        res_large = oracle_top_k(arr_large, k=3, direction="largest")
        self.assertEqual(len(res_large), 3)
        self.assertEqual(res_large, [9, 8, 7])

        # 4. K == 1 (arr size 5, K = 1) -> heap size == 1
        arr_k1 = [15, 3, 42, 8, 23]
        res_k1 = oracle_top_k(arr_k1, k=1, direction="largest")
        self.assertEqual(len(res_k1), 1)
        self.assertEqual(res_k1, [42])

        # Smallest direction K == 1
        res_k1_min = oracle_top_k(arr_k1, k=1, direction="smallest")
        self.assertEqual(len(res_k1_min), 1)
        self.assertEqual(res_k1_min, [3])

        # Verify failure classifier for capacity mismatch
        fc = FailureClassifier.classify("HEAP_CAPACITY_MISMATCH", {})
        self.assertEqual(fc.category, FailureCategory.HEAP_CAPACITY_MISMATCH)
        self.assertIn("exceeds the allowed retention capacity", fc.description)


if __name__ == "__main__":
    unittest.main()
