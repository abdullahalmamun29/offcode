"""
Phase 3N: Architecture Composition Tests.

Verifies the 3 Mandatory Core Composition Gates:
- Composition Gate A: Kruskal <-> DSU
- Composition Gate B: 2-SAT <-> SCC
- Composition Gate C: Min-Cut <-> Max-Flow

Also tests:
- StateContract attribute unification & supertype compatibility
- Rejection when dependencies are removed from registry (Anti-Hardcoding Invariant)
- Machine-readable composition plan & dependency DAG verification
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from pointer_algorithms.adv_graph.semantic_ontology import (
    DerivedFact, ProvenanceStatus
)
from pointer_algorithms.adv_graph.component_model import (
    StateContract, AlgorithmComponent, CompositionNodeType, ComponentRegistry
)
from pointer_algorithms.adv_graph.composition_engine import (
    CompositionEngine, CompositionPlan, CompositionFailureCategory, CandidateStatus
)


class TestAdvGraphComposition(unittest.TestCase):

    def setUp(self):
        self.registry = ComponentRegistry()
        self.engine = CompositionEngine(self.registry)

    # ── 1. StateContract Unification Tests ──

    def test_state_contract_exact_match(self):
        s1 = StateContract(name="ResidualNetwork", attributes={"source": 1, "sink": 5})
        req = StateContract(name="ResidualNetwork", attributes={"source": 1, "sink": 5})
        self.assertTrue(s1.satisfies(req))

    def test_state_contract_supertype_match(self):
        # SaturatedResidualNetwork IS-A ResidualNetwork
        s1 = StateContract(
            name="SaturatedResidualNetwork",
            attributes={"source": 1, "sink": 5},
            supertypes=["ResidualNetwork"]
        )
        req = StateContract(name="ResidualNetwork", attributes={"source": 1, "sink": 5})
        self.assertTrue(s1.satisfies(req))

    def test_state_contract_attribute_conflict_rejected(self):
        # Mismatch on source vertex: 1 vs 2
        s1 = StateContract(name="ResidualNetwork", attributes={"source": 1, "sink": 5})
        req = StateContract(name="ResidualNetwork", attributes={"source": 2, "sink": 5})
        self.assertFalse(s1.satisfies(req))

    def test_state_contract_missing_attribute_rejected(self):
        # State missing required attribute 'sink'
        s1 = StateContract(name="ResidualNetwork", attributes={"source": 1})
        req = StateContract(name="ResidualNetwork", attributes={"source": 1, "sink": 5})
        self.assertFalse(s1.satisfies(req))

    # ── 2. Composition Gate A: Kruskal <-> DSU ──

    def test_composition_gate_a_kruskal_dsu(self):
        """
        Kruskal must be synthesized generically from:
        WeightedUndirectedGraph + VertexUniverse
        -> graph_edge_sorting (Transformation)
        -> disjoint_set_union (Component)
        -> cycle_free_edge_selection (Transformation)
        -> SpanningForestResult
        """
        init_states = [
            StateContract(name="WeightedUndirectedGraph", attributes={"directed": False, "weighted": True}),
            StateContract(name="VertexUniverse")
        ]
        goal = StateContract(name="SpanningForestResult")

        plan = self.engine.synthesize_plan(init_states, goal)
        self.assertTrue(plan.is_valid, f"Kruskal composition failed: {plan.failure_reason}")
        self.assertTrue(plan.has_component("disjoint_set_union"))
        self.assertTrue(plan.has_component("graph_edge_sorting"))
        self.assertTrue(plan.has_component("cycle_free_edge_selection"))

        # Check topological order: sorting and dsu must precede selection
        order = plan.execution_order
        self.assertIn("graph_edge_sorting", order)
        self.assertIn("disjoint_set_union", order)
        self.assertIn("cycle_free_edge_selection", order)
        self.assertLess(order.index("graph_edge_sorting"), order.index("cycle_free_edge_selection"))
        self.assertLess(order.index("disjoint_set_union"), order.index("cycle_free_edge_selection"))

    def test_composition_gate_a_anti_hardcoding_dsu_removal(self):
        """
        ARCHITECTURAL LEAKAGE TEST:
        If DSU is removed from registry, Kruskal composition MUST FAIL with NO_PROVIDER.
        """
        reg_no_dsu = ComponentRegistry()
        del reg_no_dsu.components["disjoint_set_union"]
        engine_no_dsu = CompositionEngine(reg_no_dsu)

        init_states = [
            StateContract(name="WeightedUndirectedGraph", attributes={"directed": False, "weighted": True}),
            StateContract(name="VertexUniverse")
        ]
        goal = StateContract(name="SpanningForestResult")

        plan = engine_no_dsu.synthesize_plan(init_states, goal)
        self.assertFalse(plan.is_valid)
        self.assertEqual(plan.failure_category, CompositionFailureCategory.NO_PROVIDER)

    # ── 3. Composition Gate B: 2-SAT <-> SCC ──

    def test_composition_gate_b_2sat_scc(self):
        """
        2-SAT must be synthesized from:
        TwoCnfFormula
        -> two_cnf_to_implication_graph (Transformation)
        -> scc_condensation_engine (Component)
        -> scc_to_twosat_assignment (Transformation)
        -> TwoSatAssignmentResult
        """
        init_states = [
            StateContract(name="TwoCnfFormula", attributes={"clause_cardinality": 2})
        ]
        goal = StateContract(name="TwoSatAssignmentResult")

        plan = self.engine.synthesize_plan(init_states, goal)
        self.assertTrue(plan.is_valid, f"2-SAT composition failed: {plan.failure_reason}")
        self.assertTrue(plan.has_component("two_cnf_to_implication_graph"))
        self.assertTrue(plan.has_component("scc_condensation_engine"))
        self.assertTrue(plan.has_component("scc_to_twosat_assignment"))

        # Verify topological execution order
        order = plan.execution_order
        self.assertLess(order.index("two_cnf_to_implication_graph"), order.index("scc_condensation_engine"))
        self.assertLess(order.index("scc_condensation_engine"), order.index("scc_to_twosat_assignment"))

    def test_composition_gate_b_anti_hardcoding_scc_removal(self):
        """
        ARCHITECTURAL LEAKAGE TEST:
        If SCC engine is removed from registry, 2-SAT composition MUST FAIL with NO_PROVIDER.
        """
        reg_no_scc = ComponentRegistry()
        del reg_no_scc.components["scc_condensation_engine"]
        engine_no_scc = CompositionEngine(reg_no_scc)

        init_states = [
            StateContract(name="TwoCnfFormula", attributes={"clause_cardinality": 2})
        ]
        goal = StateContract(name="TwoSatAssignmentResult")

        plan = engine_no_scc.synthesize_plan(init_states, goal)
        self.assertFalse(plan.is_valid)
        self.assertEqual(plan.failure_category, CompositionFailureCategory.NO_PROVIDER)

    # ── 4. Composition Gate C: Min-Cut <-> Max-Flow ──

    def test_composition_gate_c_min_cut_max_flow(self):
        """
        Min-Cut must be synthesized from:
        CapacitatedNetwork
        -> max_flow_dinic (Component)
        -> saturated_residual_to_min_cut (Transformation)
        -> MinCutPartition
        """
        init_states = [
            StateContract(name="CapacitatedNetwork", attributes={"directed": True})
        ]
        goal = StateContract(name="MinCutPartition")

        plan = self.engine.synthesize_plan(init_states, goal)
        self.assertTrue(plan.is_valid, f"Min-Cut composition failed: {plan.failure_reason}")
        self.assertTrue(plan.has_component("max_flow_dinic"))
        self.assertTrue(plan.has_component("saturated_residual_to_min_cut"))

        # Max flow must precede residual reachability
        order = plan.execution_order
        self.assertLess(order.index("max_flow_dinic"), order.index("saturated_residual_to_min_cut"))

    def test_composition_gate_c_anti_hardcoding_flow_removal(self):
        """
        ARCHITECTURAL LEAKAGE TEST:
        If Max-Flow is removed from registry, Min-Cut composition MUST FAIL with NO_PROVIDER.
        """
        reg_no_flow = ComponentRegistry()
        del reg_no_flow.components["max_flow_dinic"]
        engine_no_flow = CompositionEngine(reg_no_flow)

        init_states = [
            StateContract(name="CapacitatedNetwork", attributes={"directed": True})
        ]
        goal = StateContract(name="MinCutPartition")

        plan = engine_no_flow.synthesize_plan(init_states, goal)
        self.assertFalse(plan.is_valid)
        self.assertEqual(plan.failure_category, CompositionFailureCategory.NO_PROVIDER)

    # ── 5. Machine-Readable Dependency DAG Verification ──

    def test_composition_plan_dag_structure(self):
        init_states = [
            StateContract(name="TwoCnfFormula", attributes={"clause_cardinality": 2})
        ]
        goal = StateContract(name="TwoSatAssignmentResult")

        plan = self.engine.synthesize_plan(init_states, goal)
        self.assertTrue(plan.is_valid)
        self.assertGreater(len(plan.dependency_edges), 0)
        self.assertIn("scc_condensation_engine::condensation_dag_acyclicity", plan.proof_obligations)
        self.assertIn("two_cnf_to_implication_graph::implication_logic_equivalence", plan.proof_obligations)

        explanation = plan.explain_chain()
        self.assertIn("Goal State: TwoSatAssignmentResult", explanation)
        self.assertIn("scc_condensation_engine", explanation)


if __name__ == "__main__":
    unittest.main()
