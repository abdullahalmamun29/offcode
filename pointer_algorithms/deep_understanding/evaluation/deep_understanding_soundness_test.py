"""
CHUP Phase 6 — Soundness & Non-Inference Evaluation Suite.

Verifies the mathematical soundness guarantees of Phase 6:
1. Large coordinates alone do NOT imply coordinate compression or dynamic segment tree.
2. Negative weights alone do NOT cause false global UNSAT.
3. E = V - 1 alone does NOT imply TREE topology.
4. Directed graph with E = V - 1 is NOT contradictory.
5. Offline-compatible is NOT equivalent to offline-required.
6. Pairwise mutual exclusion alone does NOT imply bipartite matching.
"""

import unittest
from pointer_algorithms.deep_understanding.fact_model import (
    FactTier,
    ProofStatus,
    AmbiguityStatus,
    SemanticFact,
    FactSet
)
from pointer_algorithms.deep_understanding.provenance import ProvenanceGraph
from pointer_algorithms.deep_understanding.implicit_constraints import ImplicitConstraintInferrer
from pointer_algorithms.deep_understanding.contradiction_engine import SourceFactContradictionEngine
from pointer_algorithms.deep_understanding.deep_understanding_facade import DeepProblemUnderstandingFacade
from pointer_algorithms.multi_constraint.multi_constraint_model import OutcomeState


class TestPhase6Soundness(unittest.TestCase):

    def setUp(self):
        self.facade = DeepProblemUnderstandingFacade()

    def test_01_large_coordinate_alone_does_not_imply_compression(self):
        """Large coordinates alone (e.g. N=2, x=[1e18, 1e18+1]) without coordinate indexing do NOT mandate compression."""
        graph = ProvenanceGraph()
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "COORDINATES_EXCEED_DENSE_MEMORY_BOUND", True, ProofStatus.PROVEN),
            SemanticFact("f2", FactTier.OBSERVED_FACT, "N_COUNT", 2, ProofStatus.PROVEN)
            # Notice: COORDINATE_QUERY_OR_INDEX_REQUIRED is ABSENT
        ])
        inferrer = ImplicitConstraintInferrer()
        derived = inferrer.infer_constraints(facts, graph)
        self.assertFalse(any(f.name == "DENSE_INDEX_SPACE_UNAVAILABLE" for f in derived))

    def test_02_negative_weight_does_not_cause_false_unsat(self):
        """Negative edge weights alone must NOT trigger false global UNSAT if no negative cycles exist."""
        spec = {
            "text": "Weighted graph with negative weights without negative cycles.",
            "contains_negative": True,
            "operation": "SUM",
            "v": 100,
            "e": 200
        }
        res = self.facade.process(spec)
        self.assertNotEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)

    def test_03_e_equals_v_minus_one_alone_does_not_imply_tree(self):
        """Merely having E = V - 1 without connectedness, undirectedness, or simplicity does NOT infer TREE."""
        graph = ProvenanceGraph()
        inferrer = ImplicitConstraintInferrer()

        facts_incomplete = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "VERTEX_COUNT", 10, ProofStatus.PROVEN),
            SemanticFact("f2", FactTier.OBSERVED_FACT, "EDGE_COUNT", 9, ProofStatus.PROVEN)
            # Missing IS_CONNECTED, IS_UNDIRECTED, IS_SIMPLE
        ])
        derived = inferrer.infer_constraints(facts_incomplete, graph)
        self.assertFalse(any(f.name == "TOPOLOGY_TREE" for f in derived))

    def test_04_directed_graph_with_e_equals_v_minus_one_not_contradictory(self):
        """A directed graph with E = V - 1 (e.g. arborescence or DAG) is NOT contradictory."""
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "IS_DIRECTED", True, ProofStatus.PROVEN),
            SemanticFact("f2", FactTier.OBSERVED_FACT, "VERTEX_COUNT", 10, ProofStatus.PROVEN),
            SemanticFact("f3", FactTier.OBSERVED_FACT, "EDGE_COUNT", 9, ProofStatus.PROVEN)
        ])
        cert, _ = SourceFactContradictionEngine.analyze(facts)
        self.assertIsNone(cert, "Directed graph with E = V - 1 must not trigger contradiction.")

    def test_05_offline_compatible_not_equivalent_to_offline_required(self):
        """Queries that can be answered in arbitrary order do not strictly mandate offline batch sorting."""
        spec = {
            "text": "Find prefix sum for q independent queries.",
            "n": 100_000,
            "q": 100_000,
            "operation": "SUM",
            "target": "LINEAR_RANGE"
        }
        res = self.facade.process(spec)
        self.assertEqual(res["status"], "success")
        self.assertIn(res["outcome_state"], (OutcomeState.SATISFIABLE_SINGLE_CANDIDATE, OutcomeState.SATISFIABLE_COMPOSED_PLAN))

    def test_06_mutual_exclusion_alone_does_not_imply_bipartite(self):
        """Pairwise mutual exclusion alone does not imply bipartite graph unless 2-colorable."""
        graph = ProvenanceGraph()
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "MUTUAL_EXCLUSION_CONSTRAINTS_PRESENT", True, ProofStatus.PROVEN)
        ])
        inferrer = ImplicitConstraintInferrer()
        derived = inferrer.infer_constraints(facts, graph)
        self.assertFalse(any(f.name == "GRAPH_BIPARTITE" for f in derived))


if __name__ == "__main__":
    unittest.main()
