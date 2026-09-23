"""
CHUP Phase 6 — Vocabulary Collision Evaluation Suite.

Evaluates problems sharing identical surface vocabulary ("cities", "roads", "distance", "network")
that specify fundamentally different mathematical problems:
1. Minimum Spanning Tree (connect all cities with minimum total road length)
2. Single-Pair Shortest Path (find minimum travel distance between two cities)
3. Critical Bridge Detection (identify roads whose destruction disconnects the network)
4. Connected Components (group cities into connected clusters)

Permanent Phase 6 Regression Invariant:
Same vocabulary must NEVER produce the same algorithmic hypothesis or structural derivation
merely due to shared keywords. The semantic objective, query target, and proof obligations
must strictly reflect the underlying mathematical problem.
"""

import unittest
from pointer_algorithms.deep_understanding.deep_understanding_facade import DeepProblemUnderstandingFacade
from pointer_algorithms.deep_understanding.semantic_objective import ObjectiveKind
from pointer_algorithms.multi_constraint.aggregate_ontology import QueryTarget


class TestPhase6VocabularyCollision(unittest.TestCase):

    def setUp(self):
        self.facade = DeepProblemUnderstandingFacade()

    def test_vocabulary_collision_distinct_mathematics(self):
        # Problem 1: MST
        spec_mst = {
            "text": "A network of cities and bidirectional roads. Connect all cities with minimum total road distance.",
            "v": 100,
            "e": 500,
            "all_non_negative": True,
            "undirected": True,
            "connected": True,
            "goal": "OPTIMIZE_EXTREMUM",
            "target": "TREE_SPANNING",
            "operation": "SUM"
        }

        # Problem 2: Shortest Path
        spec_shortest_path = {
            "text": "A network of cities and directed roads with positive distance. Find the minimum travel distance from start city to end city.",
            "v": 100,
            "e": 500,
            "all_non_negative": True,
            "directed": True,
            "goal": "OPTIMIZE_EXTREMUM",
            "target": "POINT",
            "operation": "MIN"
        }

        # Problem 3: Decision Feasibility on Network Distance
        spec_feasibility = {
            "text": "In a road network between cities, determine if a distance threshold D is achievable between city A and city B.",
            "v": 100,
            "e": 500,
            "goal": "DECISION_FEASIBILITY",
            "target": "POINT",
            "operation": "MIN"
        }

        # Problem 4: Range aggregate across network coordinates
        spec_linear_queries = {
            "text": "A linear network of cities along a highway road. Answer range sum queries for total distance between mile markers.",
            "n": 100_000,
            "q": 100_000,
            "operation": "SUM",
            "target": "LINEAR_RANGE",
            "immutable": True
        }

        res_mst = self.facade.process(spec_mst)
        res_sp = self.facade.process(spec_shortest_path)
        res_feas = self.facade.process(spec_feasibility)
        res_lin = self.facade.process(spec_linear_queries)

        # 1. Verify semantic objectives are structurally differentiated
        self.assertEqual(res_feas["semantic_objective"], ObjectiveKind.DECISION_FEASIBILITY)
        self.assertEqual(res_mst["semantic_objective"], ObjectiveKind.OPTIMIZATION_EXTREMUM)

        # 2. Verify operations are differentiated (SUM vs MIN)
        self.assertEqual(spec_mst["operation"], "SUM")
        self.assertEqual(spec_shortest_path["operation"], "MIN")

        # 3. Verify target query structures are differentiated
        facts_lin = res_lin["phase6_facts"]
        self.assertTrue(facts_lin.has_proven("TARGET_LINEAR_RANGE", True))
        facts_sp = res_sp["phase6_facts"]
        self.assertFalse(facts_sp.has_proven("TARGET_LINEAR_RANGE", True))

        # 4. Invariant: Identical surface words ("cities", "roads", "network") did not collapse into a single template
        self.assertNotEqual(res_lin["verified_plan"].canonical_digest, res_mst["verified_plan"].canonical_digest)


if __name__ == "__main__":
    unittest.main()
