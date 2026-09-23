"""
CHUP Phase 5 — Multi-Constraint Conflict Detection Evaluation Suite (Tier 2).

Verifies axiomatic contradiction detection across 10 distinct mathematical impossibility
scenarios, ensuring UNSATISFIABLE_CONSTRAINT_SET and structured ConstraintContradictionCertificates.
"""

import unittest
from pointer_algorithms.multi_constraint.facade import MultiConstraintSolver
from pointer_algorithms.multi_constraint.multi_constraint_model import OutcomeState


class TestMultiConstraintConflict(unittest.TestCase):
    """Tier 2 evaluation: verifies axiomatic contradiction detection."""

    def setUp(self):
        self.solver = MultiConstraintSolver()

    def test_conflict_01_tree_with_cycle(self):
        """Tree topology asserted together with cyclic graph yields ACYCLIC_AND_CYCLIC_CONTRADICTION."""
        spec = {
            "topology": {
                "directed": False,
                "connected": True,
                "acyclic": False,  # Contradicts tree requirement of acyclicity
                "simple": True,
                "v": 10,
                "e": 9
            }
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        cert = res["conflict_certificate"]
        self.assertIsNotNone(cert)
        self.assertEqual(cert.failure_code, "ACYCLIC_AND_CYCLIC_CONTRADICTION")
        self.assertTrue(any("Acyclic" in c for c in cert.incompatible_constraints))

    def test_conflict_02_tree_edge_count_violation(self):
        """Tree topology with E >= V yields TREE_EDGE_COUNT_CONTRADICTION."""
        spec = {
            "topology": "UNDIRECTED_TREE",
            "v": 10,
            "e": 10  # Tree on 10 vertices must have exactly 9 edges
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        cert = res["conflict_certificate"]
        self.assertIsNotNone(cert)
        self.assertEqual(cert.failure_code, "TREE_EDGE_COUNT_CONTRADICTION")
        self.assertIn("10", cert.formal_proof)

    def test_conflict_03_tree_disconnected(self):
        """Tree topology declared disconnected yields TREE_CONNECTEDNESS_CONTRADICTION."""
        spec = {
            "topology": {
                "directed": False,
                "connected": False,  # Trees must be connected
                "acyclic": True,
                "simple": True,
                "v": 5,
                "e": 4
            }
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        cert = res["conflict_certificate"]
        self.assertIsNotNone(cert)
        self.assertEqual(cert.failure_code, "TREE_CONNECTEDNESS_CONTRADICTION")

    def test_conflict_04_negative_cycle_shortest_path(self):
        """Shortest path query on graph with proven negative cycle yields NEGATIVE_CYCLE_SHORTEST_PATH_CONTRADICTION."""
        spec = {
            "query_target": "SINGLE_SOURCE_SHORTEST_PATH",
            "shortest_path_query": True,
            "proven_negative_cycle": True
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        cert = res["conflict_certificate"]
        self.assertIsNotNone(cert)
        self.assertEqual(cert.failure_code, "NEGATIVE_CYCLE_SHORTEST_PATH_CONTRADICTION")
        self.assertIn("-inf", cert.formal_proof)

    def test_conflict_05_online_stream_with_offline_only(self):
        """Online stream requiring full offline query sorting yields ONLINE_STREAM_WITH_OFFLINE_REQUIREMENT."""
        spec = {
            "temporal": "ONLINE",
            "require_offline_sorting": True
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        cert = res["conflict_certificate"]
        self.assertIsNotNone(cert)
        self.assertEqual(cert.failure_code, "ONLINE_STREAM_WITH_OFFLINE_REQUIREMENT")

    def test_conflict_06_cell_probe_lower_bound(self):
        """Dynamic RMQ with O(1) query AND O(1) update violates cell-probe lower bound."""
        spec = {
            "cell_probe_lower_bound_trigger": True
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        cert = res["conflict_certificate"]
        self.assertIsNotNone(cert)
        self.assertEqual(cert.failure_code, "CELL_PROBE_LOWER_BOUND_VIOLATION")
        self.assertIn("cell-probe", cert.formal_proof.lower())

    def test_conflict_07_read_only_with_structural_mutation(self):
        """Array declared read-only with structural mutation yields MUTABILITY_LEVEL_CONTRADICTION."""
        spec = {
            "mutability": "STATIC",
            "require_structural_insert": True
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        cert = res["conflict_certificate"]
        self.assertIsNotNone(cert)
        self.assertEqual(cert.failure_code, "MUTABILITY_LEVEL_CONTRADICTION")

    def test_conflict_08_monotone_predicate_contradiction(self):
        """Predicate declared monotone and non-monotone simultaneously yields PREDICATE_MONOTONICITY_CONTRADICTION."""
        spec = {
            "predicate_monotonic": True,
            "non_monotone_predicate": True
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        cert = res["conflict_certificate"]
        self.assertIsNotNone(cert)
        self.assertEqual(cert.failure_code, "PREDICATE_MONOTONICITY_CONTRADICTION")

    def test_conflict_09_dag_with_directed_cycle(self):
        """DAG declared with directed cycle yields ACYCLIC_AND_CYCLIC_CONTRADICTION."""
        spec = {
            "topology": {
                "directed": True,
                "connected": True,
                "acyclic": False,  # Cycle in DAG
                "simple": True,
                "is_dag": True
            }
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        cert = res["conflict_certificate"]
        self.assertIsNotNone(cert)
        self.assertEqual(cert.failure_code, "ACYCLIC_AND_CYCLIC_CONTRADICTION")

    def test_conflict_10_contradiction_certificate_integrity(self):
        """All contradiction certificates possess non-empty axioms, proofs, and failure codes."""
        spec = {
            "topology": "UNDIRECTED_TREE",
            "v": 20,
            "e": 25
        }
        res = self.solver.solve(spec)
        cert = res["conflict_certificate"]
        self.assertTrue(len(cert.failure_code) > 0)
        self.assertTrue(len(cert.incompatible_constraints) >= 2)
        self.assertTrue(len(cert.minimal_unsat_core) >= 2)
        self.assertTrue(len(cert.formal_proof) > 10)
        self.assertTrue(len(cert.rejection_witness) > 0)


if __name__ == "__main__":
    unittest.main()
