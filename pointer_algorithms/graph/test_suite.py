"""
Unit Test Suite for Graph Algorithmic Domain (Phase 3F).
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from pointer_algorithms.knowledge.taxonomy import (
    GraphKind, GraphWeightKind, GraphRepresentation as GraphRepr,
    AlgorithmFamily, PatternKind, GRAPH_PATTERNS, TAXONOMY_TREE
)
from pointer_algorithms.recognition.feature_extractor import FeatureExtractor
from pointer_algorithms.recognition.candidate_generator import CandidateGenerator
from pointer_algorithms.recognition.candidate_eliminator import CandidateEliminator
from pointer_algorithms.reasoning.reasoning_engine import (
    GraphStructuralReasoning, ShortestPathDecisionReasoning,
    CycleReasoning, BipartiteReasoning, TopologicalSortReasoning,
    DSUReasoning, MSTReasoning, SCCReasoning, BridgeArticulationReasoning
)
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine
from pointer_algorithms.failure_analysis.classifier import FailureClassifier, FailureCategory
from pointer_algorithms.bridge import handle_request, ALGORITHMIC_FAMILIES, POINTER_FAMILIES


class TestGraphDomain(unittest.TestCase):

    def test_taxonomy_registration(self):
        self.assertIn("graph", ALGORITHMIC_FAMILIES)
        self.assertIn("graph", POINTER_FAMILIES)
        self.assertEqual(AlgorithmFamily.GRAPH.value, "graph")
        self.assertEqual(len(GRAPH_PATTERNS), 16)
        self.assertIn("Graph", TAXONOMY_TREE.get("Pointer-Based Algorithms", {}))

    def test_feature_extractor_graph_dijkstra(self):
        f = FeatureExtractor.extract(
            "Given a directed weighted graph with non-negative edge weights. Find the shortest path from source 1."
        )
        self.assertTrue(f.is_graph_detected)
        self.assertTrue(f.graph_is_directed)
        self.assertTrue(f.graph_is_weighted)
        self.assertFalse(f.graph_has_negative_weights)
        self.assertEqual(f.graph_query_type, "shortest_path")
        self.assertEqual(f.graph_algorithm_family, "graph_dijkstra")

    def test_feature_extractor_negative_weights(self):
        f = FeatureExtractor.extract(
            "Find shortest path in directed graph with negative weights, but no negative cycles."
        )
        self.assertTrue(f.is_graph_detected)
        self.assertTrue(f.graph_has_negative_weights)
        self.assertFalse(f.graph_has_negative_cycles)
        self.assertEqual(f.graph_algorithm_family, "graph_bellman_ford")

    def test_feature_extractor_negative_cycles(self):
        f = FeatureExtractor.extract(
            "Graph has a negative cycle. Check if reachable negative-weight cycle exists."
        )
        self.assertTrue(f.is_graph_detected)
        self.assertTrue(f.graph_has_negative_weights)
        self.assertTrue(f.graph_has_negative_cycles)

    def test_feature_extractor_topological_sort(self):
        f = FeatureExtractor.extract(
            "Find topological order of dependencies in a directed acyclic graph (DAG)."
        )
        self.assertTrue(f.is_graph_detected)
        self.assertTrue(f.graph_is_directed)
        self.assertTrue(f.graph_is_dag)
        self.assertEqual(f.graph_query_type, "topological")
        self.assertEqual(f.graph_algorithm_family, "graph_topological_sort")

    def test_tree_vs_graph_discrimination(self):
        # Tree problem with tree-specific operations: must route to Tree, NOT Graph
        f_tree = FeatureExtractor.extract(
            "Given the root of a binary tree, find the lowest common ancestor (LCA) of nodes p and q."
        )
        self.assertFalse(f_tree.is_graph_detected)
        self.assertTrue(f_tree.tree_kind is not None)

        # Graph problem: must route to Graph
        f_graph = FeatureExtractor.extract(
            "Find the minimum spanning tree (MST) using Kruskal algorithm on undirected graph."
        )
        self.assertTrue(f_graph.is_graph_detected)
        self.assertEqual(f_graph.graph_algorithm_family, "graph_mst_kruskal")

    def test_candidate_elimination_dijkstra_on_negative_weights(self):
        f = FeatureExtractor.extract(
            "Find shortest path in graph with negative weight edges."
        )
        candidates = CandidateGenerator.generate_candidates(f)
        evals = CandidateEliminator.filter_and_rank(candidates, f)

        # Dijkstra must be rejected
        elim_pats = [e.candidate.pattern for e in evals["eliminated"]]
        self.assertIn("graph_dijkstra", elim_pats)

        dijkstra_eval = next(e for e in evals["eliminated"] if e.candidate.pattern == "graph_dijkstra")
        self.assertEqual(dijkstra_eval.rejection_code, "GRAPH_NEGATIVE_WEIGHTS_FOR_DIJKSTRA")

    def test_candidate_elimination_topological_on_cyclic(self):
        f = FeatureExtractor.extract(
            "Find topological order of a directed cyclic graph with cycle."
        )
        candidates = CandidateGenerator.generate_candidates(f)
        evals = CandidateEliminator.filter_and_rank(candidates, f)

        elim_codes = [e.rejection_code for e in evals["eliminated"]]
        self.assertIn("GRAPH_CYCLIC_FOR_TOPOLOGICAL_SORT", elim_codes)

    def test_candidate_elimination_floyd_warshall_complexity(self):
        f = FeatureExtractor.extract(
            "All-pairs shortest path with N = 100,000 vertices."
        )
        candidates = CandidateGenerator.generate_candidates(f)
        evals = CandidateEliminator.filter_and_rank(candidates, f)

        elim_codes = [e.rejection_code for e in evals["eliminated"]]
        self.assertIn("GRAPH_COMPLEXITY_EXCEEDED", elim_codes)

    def test_candidate_elimination_dijkstra_unweighted_suboptimal(self):
        f = FeatureExtractor.extract(
            "Find shortest path in unweighted graph from source to target."
        )
        candidates = CandidateGenerator.generate_candidates(f)
        evals = CandidateEliminator.filter_and_rank(candidates, f)

        # BFS should be accepted and top-ranked
        self.assertEqual(evals["selected"].candidate.pattern, "graph_bfs_shortest_path")

        # If Dijkstra is in accepted, it should be marked suboptimal
        dijkstra_accepted = [e for e in evals["accepted"] if e.candidate.pattern == "graph_dijkstra"]
        if dijkstra_accepted:
            self.assertTrue(dijkstra_accepted[0].is_suboptimal)

    def test_shortest_path_decision_reasoning(self):
        # Unweighted -> BFS
        dec_unweighted = ShortestPathDecisionReasoning.decide(
            is_weighted=False, has_negative_weights=False, has_negative_cycles=False, is_dag=None
        )
        self.assertEqual(dec_unweighted.selected_algorithm, "graph_bfs_shortest_path")

        # Non-negative weighted -> Dijkstra
        dec_non_neg = ShortestPathDecisionReasoning.decide(
            is_weighted=True, has_negative_weights=False, has_negative_cycles=False, is_dag=None
        )
        self.assertEqual(dec_non_neg.selected_algorithm, "graph_dijkstra")

        # Negative weights -> Bellman-Ford
        dec_neg = ShortestPathDecisionReasoning.decide(
            is_weighted=True, has_negative_weights=True, has_negative_cycles=False, is_dag=None
        )
        self.assertEqual(dec_neg.selected_algorithm, "graph_bellman_ford")

        # DAG -> DAG-DP
        dec_dag = ShortestPathDecisionReasoning.decide(
            is_weighted=True, has_negative_weights=False, has_negative_cycles=False, is_dag=True
        )
        self.assertEqual(dec_dag.selected_algorithm, "graph_dag_dp")

        # Small V all-pairs -> Floyd-Warshall
        dec_all_pairs = ShortestPathDecisionReasoning.decide(
            is_weighted=True, has_negative_weights=False, has_negative_cycles=False, is_dag=None,
            is_all_pairs=True, vertex_count=200
        )
        self.assertEqual(dec_all_pairs.selected_algorithm, "graph_floyd_warshall")

    def test_cycle_reasoning_undirected_vs_directed(self):
        undirected_proof = CycleReasoning.explain_undirected()
        self.assertEqual(undirected_proof.graph_type, "undirected")
        self.assertIn("parent", undirected_proof.state_definition)

        directed_proof = CycleReasoning.explain_directed()
        self.assertEqual(directed_proof.graph_type, "directed")
        self.assertIn("VISITING", directed_proof.state_definition)

    def test_bipartite_reasoning_impossibility(self):
        proof = BipartiteReasoning.explain()
        self.assertIn("odd-length cycle", proof.impossibility_condition)

    def test_topological_sort_reasoning(self):
        kahn = TopologicalSortReasoning.explain_kahn()
        self.assertIn("DAG", kahn.dag_theorem)
        self.assertIn("cycle", kahn.cycle_detection)

    def test_dsu_reasoning_complexity(self):
        dsu = DSUReasoning.explain()
        self.assertTrue("α(V)" in dsu.amortized_complexity or "alpha(V)" in dsu.amortized_complexity)

    def test_mst_reasoning_cut_and_cycle_properties(self):
        mst = MSTReasoning.explain()
        self.assertIn("Cut Property", mst.cut_property)
        self.assertIn("Cycle Property", mst.cycle_property)

    def test_scc_reasoning(self):
        scc = SCCReasoning.explain()
        self.assertIn("mutual reachability", scc.mutual_reachability.lower())
        self.assertIn("Condensation DAG", scc.condensation_dag)

    def test_bridge_articulation_reasoning(self):
        ba = BridgeArticulationReasoning.explain()
        self.assertIn("low[v] > tin[u]", ba.bridge_condition)
        self.assertIn("low[v] >= tin[u]", ba.articulation_condition)

    def test_all_16_graph_invariants(self):
        for pat in GRAPH_PATTERNS:
            inv = InvariantEngine.construct_invariant(pat, {})
            self.assertIsNotNone(inv.before_iteration)
            self.assertIsNotNone(inv.during_iteration)
            self.assertIsNotNone(inv.after_movement)
            self.assertIsNotNone(inv.at_termination)

    def test_all_16_graph_movements(self):
        for pat in GRAPH_PATTERNS:
            mov = MovementDerivationEngine.derive(pat, {})
            self.assertIsNotNone(mov.objective_function)
            self.assertGreaterEqual(len(mov.decision_conditions), 1)
            self.assertIsNotNone(mov.elimination_proof)

    def test_failure_classifier_graph_categories(self):
        # Negative weights on Dijkstra
        c1 = FailureClassifier.classify("GRAPH_NEGATIVE_WEIGHTS_FOR_DIJKSTRA", {})
        self.assertEqual(c1.category, FailureCategory.ALGORITHM_SELECTION_ERROR)

        # Topological sort on cyclic graph
        c2 = FailureClassifier.classify("GRAPH_CYCLIC_TOPO", {})
        self.assertEqual(c2.category, FailureCategory.CONSTRAINT_ANALYSIS_ERROR)

        # Floyd-Warshall complexity exceeded
        c3 = FailureClassifier.classify("FLOYD_COMPLEXITY_EXCEEDED", {})
        self.assertEqual(c3.category, FailureCategory.COMPLEXITY_ESTIMATION_ERROR)

    def test_bridge_graph_request(self):
        req = {
            "problemText": "Given an unweighted graph with V vertices and E edges. Find the shortest path from vertex 1 to vertex N."
        }
        resp = handle_request(req)
        self.assertEqual(resp["status"], "success")
        self.assertEqual(resp["family"], "graph")
        self.assertEqual(resp["selectedPattern"], "graph_bfs_shortest_path")
        self.assertIsNotNone(resp.get("graph"))
        self.assertIn("dist", resp["code"])


    def test_3F_H1_index_base_no_guessing(self):
        # Explicit 0-based
        f0 = FeatureExtractor.extract("Graph with vertices numbered 0 to n-1. Find shortest path.")
        self.assertEqual(f0.graph_index_base, 0)

        # Explicit 1-based
        f1 = FeatureExtractor.extract("Given a graph with vertices numbered 1 to n. Find shortest path.")
        self.assertEqual(f1.graph_index_base, 1)

        # Ambiguous / unspecified: must NOT infer or guess from vertex values
        f_ambig = FeatureExtractor.extract("Given an unweighted network. Find shortest path from vertex 2 to vertex 8.")
        self.assertIsNone(f_ambig.graph_index_base)

    def test_3F_H2_negative_cycle_semantics_cases_A_B_C(self):
        from pointer_algorithms.graph.verification.graph_oracles import oracle_negative_cycle_influence

        # Case A: Negative cycle exists, but unreachable from source (source=1)
        # Component 1: 1 -> 2 (weight 3), 2 -> 3 (weight 4) -> path to 3 is 7
        # Component 2: 4 -> 5 (-2), 5 -> 6 (-2), 6 -> 4 (-2) [neg cycle in {4,5,6}]
        edges_a = [(1, 2, 3), (2, 3, 4), (4, 5, -2), (5, 6, -2), (6, 4, -2)]
        res_a = oracle_negative_cycle_influence(6, edges_a, source=1, target=3)
        self.assertTrue(res_a.has_negative_cycle_in_graph)
        self.assertFalse(res_a.source_can_reach_negative_cycle)
        self.assertEqual(res_a.target_shortest_path_status, "WELL_DEFINED")
        self.assertEqual(res_a.target_distance, 7)

        # Case B: Negative cycle reachable from source (source=1), but cannot reach target (target=5)
        # 1 -> 2 (1), 2 -> 3 (-5), 3 -> 2 (-5) [neg cycle {2, 3}]
        # 1 -> 4 (2), 4 -> 5 (3) [independent branch to target 5; cycle cannot reach 4 or 5]
        edges_b = [(1, 2, 1), (2, 3, -5), (3, 2, -5), (1, 4, 2), (4, 5, 3)]
        res_b = oracle_negative_cycle_influence(5, edges_b, source=1, target=5)
        self.assertTrue(res_b.has_negative_cycle_in_graph)
        self.assertTrue(res_b.source_can_reach_negative_cycle)
        self.assertFalse(res_b.negative_cycle_can_reach_target)
        self.assertEqual(res_b.target_shortest_path_status, "WELL_DEFINED")
        self.assertEqual(res_b.target_distance, 5)

        # Case C: Negative cycle reachable from source AND can reach target (target=4)
        # 1 -> 2 (1), 2 -> 3 (-5), 3 -> 2 (-5), 3 -> 4 (2)
        edges_c = [(1, 2, 1), (2, 3, -5), (3, 2, -5), (3, 4, 2)]
        res_c = oracle_negative_cycle_influence(4, edges_c, source=1, target=4)
        self.assertTrue(res_c.has_negative_cycle_in_graph)
        self.assertTrue(res_c.source_can_reach_negative_cycle)
        self.assertTrue(res_c.negative_cycle_can_reach_target)
        self.assertEqual(res_c.target_shortest_path_status, "UNBOUNDED_BELOW")
        self.assertIn(4, res_c.unbounded_nodes)

    def test_3F_H3_floyd_warshall_budget_complexity(self):
        from pointer_algorithms.recognition.candidate_generator import AlgorithmCandidate

        cand = AlgorithmCandidate(pattern="graph_floyd_warshall", family="graph", confidence_prior=0.9, supporting_signals=[])

        # V = 400: estimated ops = 64,000,000 <= 1e8 budget -> accepted
        f400 = FeatureExtractor.extract("Floyd-Warshall all-pairs shortest path with V <= 400.")
        eval400 = CandidateEliminator.evaluate_candidate(cand, f400)
        self.assertTrue(eval400.accepted)

        # V = 600: estimated ops = 216,000,000 > 1e8 budget -> rejected
        f600 = FeatureExtractor.extract("Floyd-Warshall all-pairs shortest path with V <= 600.")
        eval600 = CandidateEliminator.evaluate_candidate(cand, f600)
        self.assertFalse(eval600.accepted)
        self.assertEqual(eval600.rejection_code, "GRAPH_COMPLEXITY_EXCEEDED")

        # Custom higher budget (e.g. 5.0 seconds time limit -> budget 5e8 ops): V = 600 accepted!
        f600_budget = FeatureExtractor.extract("Floyd-Warshall all-pairs shortest path with V <= 600. Time limit: 5.0 seconds.")
        eval600_budget = CandidateEliminator.evaluate_candidate(cand, f600_budget)
        self.assertTrue(eval600_budget.accepted)

    def test_3F_H6_mst_vs_spanning_forest(self):
        from pointer_algorithms.recognition.candidate_generator import AlgorithmCandidate

        cand = AlgorithmCandidate(pattern="graph_mst_kruskal", family="graph", confidence_prior=0.9, supporting_signals=[])

        # Disconnected graph asking for MST: rejected
        f_mst = FeatureExtractor.extract("Given a disconnected graph with multiple components. Find the minimum spanning tree.")
        eval_mst = CandidateEliminator.evaluate_candidate(cand, f_mst)
        self.assertFalse(eval_mst.accepted)
        self.assertEqual(eval_mst.rejection_code, "GRAPH_DISCONNECTED_MST")

        # Disconnected graph asking for Minimum Spanning Forest: accepted
        f_msf = FeatureExtractor.extract("Given a disconnected graph. Compute the minimum spanning forest cost.")
        eval_msf = CandidateEliminator.evaluate_candidate(cand, f_msf)
        self.assertTrue(eval_msf.accepted)


if __name__ == "__main__":
    unittest.main()

