"""
Phase 3N: Negative Composition Tests.

Verifies fail-closed behavior when composition prerequisites,
weight domains, topologies, or structural properties are violated.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from pointer_algorithms.adv_graph.semantic_ontology import (
    Directedness, WeightDomain, CapacityDomain, CostDomain, BipartiteStatus,
    SemanticGraphModel, DerivedFact
)
from pointer_algorithms.adv_graph.component_model import (
    StateContract, AlgorithmComponent, ComponentRegistry
)
from pointer_algorithms.adv_graph.composition_engine import (
    CompositionEngine, CompositionPlan, CompositionFailureCategory
)


class TestAdvGraphNegativeComposition(unittest.TestCase):

    def setUp(self):
        self.registry = ComponentRegistry()
        self.engine = CompositionEngine(self.registry)

    def test_negative_2sat_without_implication_structure(self):
        """
        If input is not a 2-CNF formula (e.g. general 3-CNF or unrestricted Boolean formula),
        two_cnf_to_implication_graph MUST NOT match.
        """
        init_states = [
            StateContract(name="ThreeCnfFormula", attributes={"clause_cardinality": 3})
        ]
        goal = StateContract(name="TwoSatAssignmentResult")

        plan = self.engine.synthesize_plan(init_states, goal)
        self.assertFalse(plan.is_valid)
        self.assertEqual(plan.failure_category, CompositionFailureCategory.NO_PROVIDER)

    def test_negative_min_cut_without_capacitated_network(self):
        """
        Min-Cut requires CapacitatedNetwork (directed=True).
        If input is an uncapacitated graph, composition must fail closed.
        """
        init_states = [
            StateContract(name="UnweightedUndirectedGraph", attributes={"directed": False})
        ]
        goal = StateContract(name="MinCutPartition")

        plan = self.engine.synthesize_plan(init_states, goal)
        self.assertFalse(plan.is_valid)
        self.assertEqual(plan.failure_category, CompositionFailureCategory.NO_PROVIDER)

    def test_negative_01_bfs_with_general_weights(self):
        """
        0-1 BFS requires Binary01Graph (weights_binary=True).
        General weighted graph must be rejected by deque_01_relaxation.
        """
        init_states = [
            StateContract(name="GeneralWeightedGraph", attributes={"weights_binary": False})
        ]
        goal = StateContract(name="MonotoneDistanceVector")

        plan = self.engine.synthesize_plan(init_states, goal)
        self.assertFalse(plan.is_valid)
        self.assertEqual(plan.failure_category, CompositionFailureCategory.NO_PROVIDER)

    def test_negative_kruskal_on_directed_graph(self):
        """
        Kruskal requires WeightedUndirectedGraph (directed=False).
        Directed graph must be rejected for standard MST.
        """
        init_states = [
            StateContract(name="WeightedDirectedGraph", attributes={"directed": True, "weighted": True}),
            StateContract(name="VertexUniverse")
        ]
        goal = StateContract(name="SpanningForestResult")

        plan = self.engine.synthesize_plan(init_states, goal)
        self.assertFalse(plan.is_valid)
        self.assertEqual(plan.failure_category, CompositionFailureCategory.NO_PROVIDER)

    def test_negative_eulerian_trail_with_degree_parity_violation(self):
        """
        Eulerian trail requires degree_parity_valid=True.
        Odd-degree mismatch violates prerequisites.
        """
        init_states = [
            StateContract(name="EulerianGraph", attributes={"degree_parity_valid": False, "connected": True})
        ]
        goal = StateContract(name="EulerianTrail")

        plan = self.engine.synthesize_plan(init_states, goal)
        self.assertFalse(plan.is_valid)
        self.assertEqual(plan.failure_category, CompositionFailureCategory.NO_PROVIDER)

    def test_negative_bipartite_matching_on_odd_cycle_graph(self):
        """
        Bipartite matching requires bipartite=True.
        Non-bipartite graph with odd cycle must be rejected.
        """
        init_states = [
            StateContract(name="GeneralGraphWithOddCycles", attributes={"bipartite": False})
        ]
        goal = StateContract(name="MaximumMatchingAssignment")

        plan = self.engine.synthesize_plan(init_states, goal)
        self.assertFalse(plan.is_valid)
        self.assertEqual(plan.failure_category, CompositionFailureCategory.NO_PROVIDER)


if __name__ == "__main__":
    unittest.main()
