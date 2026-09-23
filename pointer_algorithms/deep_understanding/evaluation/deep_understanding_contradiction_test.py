"""
CHUP Phase 6 — Contradiction & Ambiguity Evaluation Suite.

Evaluates:
1. Source Fact Contradiction Detection:
   - Directed vs Undirected
   - Online Stream vs Offline Reordering
   - Immutable array vs Dynamic Point Updates
   - Tree topology with E != V - 1
   - Acyclic DAG with confirmed directed cycle
   - Non-negative elements with confirmed negative elements
2. Ambiguity Handling:
   - Underspecified or multi-interpretation statements emit AmbiguityReport
   - Ambiguous facts never enter the Phase 5 constraint vector

Fail-Closed Invariant:
Every contradictory input MUST immediately halt the pipeline with
outcome_state == UNSATISFIABLE_CONSTRAINT_SET, failure_code == CONFLICTING_SOURCE_FACTS,
and verified_plan == None.
"""

import unittest
from pointer_algorithms.deep_understanding.deep_understanding_facade import DeepProblemUnderstandingFacade
from pointer_algorithms.deep_understanding.fact_model import (
    SemanticFact,
    FactSet,
    FactTier,
    ProofStatus,
    AmbiguityStatus
)
from pointer_algorithms.deep_understanding.contradiction_engine import SourceFactContradictionEngine
from pointer_algorithms.multi_constraint.multi_constraint_model import OutcomeState


class TestPhase6ContradictionAndAmbiguity(unittest.TestCase):

    def setUp(self):
        self.facade = DeepProblemUnderstandingFacade()

    def test_01_directed_vs_undirected_halts(self):
        spec = {
            "text": "A network that is directed and undirected.",
            "directed": True,
            "undirected": True
        }
        res = self.facade.process(spec)
        self.assertEqual(res["status"], "conflict")
        self.assertEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        self.assertIsNone(res["verified_plan"])
        self.assertEqual(res["conflict_certificate"].failure_code, "CONFLICTING_SOURCE_FACTS")

    def test_02_online_stream_vs_offline_reordering_halts(self):
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "REQUIRES_ONLINE_INTERACTIVE", True, ProofStatus.PROVEN),
            SemanticFact("f2", FactTier.OBSERVED_FACT, "OFFLINE_QUERY_REORDERING_REQUIRED", True, ProofStatus.PROVEN)
        ])
        cert, ambig = SourceFactContradictionEngine.analyze(facts)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.conflict_id, "CONFLICT_TEMPORAL_MODE")

    def test_03_immutable_vs_dynamic_updates_halts(self):
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "IMMUTABLE_ARRAY", True, ProofStatus.PROVEN),
            SemanticFact("f2", FactTier.OBSERVED_FACT, "REQUIRES_DYNAMIC_POINT_UPDATE", True, ProofStatus.PROVEN)
        ])
        cert, ambig = SourceFactContradictionEngine.analyze(facts)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.conflict_id, "CONFLICT_MUTABILITY")

    def test_04_tree_cardinality_mismatch_halts(self):
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "CLAIMED_TREE", True, ProofStatus.PROVEN),
            SemanticFact("f2", FactTier.OBSERVED_FACT, "VERTEX_COUNT", 10, ProofStatus.PROVEN),
            SemanticFact("f3", FactTier.OBSERVED_FACT, "EDGE_COUNT", 12, ProofStatus.PROVEN)
        ])
        cert, ambig = SourceFactContradictionEngine.analyze(facts)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.conflict_id, "CONFLICT_TREE_CARDINALITY")

    def test_05_acyclic_dag_with_directed_cycle_halts(self):
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "REQUIRES_ACYCLIC_DAG", True, ProofStatus.PROVEN),
            SemanticFact("f2", FactTier.OBSERVED_FACT, "HAS_DIRECTED_CYCLE", True, ProofStatus.PROVEN)
        ])
        cert, ambig = SourceFactContradictionEngine.analyze(facts)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.conflict_id, "CONFLICT_CYCLICITY")

    def test_06_non_negative_vs_negative_elements_halts(self):
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "ALL_ELEMENTS_NON_NEGATIVE", True, ProofStatus.PROVEN),
            SemanticFact("f2", FactTier.OBSERVED_FACT, "CONTAINS_NEGATIVE_ELEMENTS", True, ProofStatus.PROVEN)
        ])
        cert, ambig = SourceFactContradictionEngine.analyze(facts)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.conflict_id, "CONFLICT_VALUE_SIGNS")

    def test_07_ambiguous_statement_does_not_mutate_phase5(self):
        """Ambiguous statement without clear temporal mode leaves outcome unresolved without false plan."""
        spec = {
            "text": "Answer range queries in arbitrary order.",
            "n": 100,
            "q": 100
        }
        res = self.facade.process(spec)
        self.assertEqual(res["status"], "ambiguous")
        self.assertEqual(res["outcome_state"], OutcomeState.UNRESOLVED_BY_CURRENT_ONTOLOGY)
        self.assertIsNone(res["verified_plan"])


if __name__ == "__main__":
    unittest.main()
