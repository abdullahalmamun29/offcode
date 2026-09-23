"""
CHUP Phase 6 — Provenance & Auditability Evaluation Suite.

Verifies:
1. 100% of facts eligible to modify Phase 5 carry a valid ProvenanceNode.
2. Every ProvenanceNode has ProofStatus.PROVEN.
3. Every ProvenanceNode records an authoritative derivation rule and concrete witness.
4. Ancestry traces back to initial observations are verified cycle-free.
5. Markdown audit trails format complete provenance histories.
"""

import unittest
from pointer_algorithms.deep_understanding.deep_understanding_facade import DeepProblemUnderstandingFacade
from pointer_algorithms.deep_understanding.fact_model import ProofStatus


class TestPhase6Provenance(unittest.TestCase):

    def setUp(self):
        self.facade = DeepProblemUnderstandingFacade()

    def test_01_provenance_coverage_and_trace_verification(self):
        spec = {
            "text": "A tree with n=100 vertices and e=99 edges that is connected, undirected, and simple. Answer range sum queries.",
            "n": 100,
            "q": 50,
            "vertex_count": 100,
            "edge_count": 99,
            "connected": True,
            "undirected": True,
            "simple": True,
            "operation": "SUM",
            "target": "LINEAR_RANGE"
        }
        res = self.facade.process(spec)
        self.assertEqual(res["status"], "success")

        facts = res["phase6_facts"]
        graph = res["provenance_graph"]

        eligible_facts = facts.eligible_facts()
        self.assertGreater(len(eligible_facts), 0, "Must have eligible facts modifying Phase 5.")

        for fact in eligible_facts:
            # 1. Provenance link must exist
            self.assertIsNotNone(fact.provenance_id, f"Fact {fact.name} missing provenance_id.")
            node = graph.get_node(fact.provenance_id)
            self.assertIsNotNone(node, f"Node {fact.provenance_id} not registered in ProvenanceGraph.")

            # 2. Must be PROVEN
            self.assertEqual(node.proof_status, ProofStatus.PROVEN)

            # 3. Non-empty rule and witness
            self.assertTrue(bool(node.derivation_rule))
            self.assertTrue(bool(node.witness))

            # 4. Verified cycle-free trace
            self.assertTrue(graph.verify_trace(fact.fact_id), f"Trace verification failed for fact {fact.name}")

    def test_02_derived_fact_audit_trail_generation(self):
        spec = {
            "text": "Connected simple undirected graph with V=10 and E=9.",
            "vertex_count": 10,
            "edge_count": 9,
            "connected": True,
            "undirected": True,
            "simple": True
        }
        res = self.facade.process(spec)
        facts = res["phase6_facts"]
        graph = res["provenance_graph"]

        tree_fact = facts.get("TOPOLOGY_TREE")
        self.assertIsNotNone(tree_fact)
        trail = graph.format_audit_trail(tree_fact.fact_id)

        self.assertIn("Provenance Audit Trail for Fact", trail)
        self.assertIn("RULE_TREE_EQUIVALENCE_E_EQ_V_MINUS_ONE", trail)
        self.assertIn("Cayley's Tree Characterization Theorem", trail)


if __name__ == "__main__":
    unittest.main()
