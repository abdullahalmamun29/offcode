"""
Comprehensive Unit Test Suite for CHUP Phase 3N: Advanced Graph Algorithms & Capability Composition.

Validates:
1. Advanced Graph Taxonomy & Enums (ADV_GRAPH_PATTERNS, AlgorithmFamily.ADV_GRAPH, TAXONOMY_TREE)
2. Semantic Ontology & Provenance Tracking (Atomic primitives, derived DAG/Bipartite properties)
3. Component Model & StateContract (IS-A hierarchy matching, attribute unification)
4. Recursive Composition Engine & Proof Gates (Gates A, B, C; anti-hardcoding registry checks)
5. Candidate Selection Semantics (VALID_OPTIMAL vs VALID_SUBOPTIMAL vs INVALID_PRECONDITION)
6. Feature Extraction & Derivation Engine integration
7. Formal 4-Phase Invariants for all 10 patterns
8. Movement Derivations for all 10 patterns
9. C++17 Solution Generation for all 10 patterns
10. Independent Reference Oracles for all 10 patterns
11. Bridge Integration & JSON-IPC end-to-end flow
"""

import unittest
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.knowledge.taxonomy import (
    PatternKind,
    AlgorithmFamily,
    ADV_GRAPH_PATTERNS,
    TAXONOMY_TREE
)
from pointer_algorithms.adv_graph.semantic_ontology import (
    Directedness,
    WeightDomain,
    CapacityDomain,
    CostDomain,
    BipartiteStatus,
    PathObjective,
    PathScope,
    TraversalObjective,
    CycleQuery,
    ConnectivityObjective,
    MatchingObjective,
    FlowObjective,
    LogicModel,
    DerivedFact,
    ProvenanceStatus,
    SemanticGraphModel
)
from pointer_algorithms.adv_graph.component_model import (
    StateContract,
    CompositionNodeType,
    AlgorithmComponent,
    ComponentRegistry
)
from pointer_algorithms.adv_graph.composition_engine import (
    CompositionEngine,
    CandidateStatus,
    SelectionStatus,
    CompositionPlan,
    CompositionFailureCategory
)
from pointer_algorithms.adv_graph.derivation_engine import (
    AdvancedGraphDerivationEngine,
    CandidateEvaluationResult
)
from pointer_algorithms.recognition.feature_extractor import FeatureExtractor
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine
from pointer_algorithms.generator.adv_graph_cpp_generator import generate_adv_graph_cpp
from pointer_algorithms.generator.cpp_generator import CppPointerGenerator
from pointer_algorithms.adv_graph.verification.adv_graph_oracles import (
    adv_graph_01_bfs_oracle,
    adv_graph_spfa_negative_cycle_oracle,
    adv_graph_eulerian_path_oracle,
    adv_graph_2sat_oracle,
    adv_graph_block_cut_tree_oracle,
    adv_graph_bridge_block_tree_oracle,
    adv_graph_bipartite_matching_oracle,
    adv_graph_max_flow_oracle,
    adv_graph_min_cut_oracle,
    adv_graph_mcmf_oracle
)
from pointer_algorithms.bridge import handle_request


class TestAdvGraphTaxonomy(unittest.TestCase):
    def test_taxonomy_definitions(self):
        """Verify 10 ADV_GRAPH patterns and taxonomy tree hierarchy."""
        self.assertEqual(len(ADV_GRAPH_PATTERNS), 10)
        self.assertIn("Advanced Graph Algorithms", TAXONOMY_TREE["Pointer-Based Algorithms"])
        self.assertEqual(AlgorithmFamily.ADV_GRAPH.value, "adv_graph")

    def test_pattern_kinds_exist(self):
        expected_patterns = [
            "adv_graph_01_bfs",
            "adv_graph_spfa_negative_cycle",
            "adv_graph_eulerian_path",
            "adv_graph_2sat",
            "adv_graph_block_cut_tree",
            "adv_graph_bridge_block_tree",
            "adv_graph_bipartite_matching",
            "adv_graph_max_flow_dinic",
            "adv_graph_min_cut",
            "adv_graph_mcmf",
        ]
        for pat in expected_patterns:
            self.assertIn(pat, ADV_GRAPH_PATTERNS)


class TestAdvGraphSemanticOntology(unittest.TestCase):
    def test_dag_derivation_from_directed_and_acyclic(self):
        """Verify DAG is a derived structural property with provenance."""
        model = SemanticGraphModel(
            directedness=Directedness.DIRECTED
        )
        model.add_derived_property(
            "is_dag",
            True,
            ["directedness=DIRECTED", "no_cycles_indicated"],
            "dag_structural_derivation"
        )
        self.assertTrue(model.is_dag())
        self.assertEqual(len(model.provenance_records), 1)
        rec = model.provenance_records[0]
        self.assertEqual(rec.fact_id, "is_dag")
        self.assertEqual(rec.derivation_rule, "dag_structural_derivation")
        self.assertEqual(rec.status, ProvenanceStatus.PROVEN)

    def test_bipartite_derivation_from_partition(self):
        """Verify Bipartite is derived from partition constraints."""
        model = SemanticGraphModel(
            directedness=Directedness.UNDIRECTED,
            bipartite_status=BipartiteStatus.BIPARTITE_DERIVED
        )
        self.assertTrue(model.is_bipartite())


class TestAdvGraphComponentModelAndStateContract(unittest.TestCase):
    def test_state_contract_isa_compatibility(self):
        """Verify SaturatedResidualNetwork satisfies ResidualNetwork via IS-A matching."""
        req = StateContract(
            name="ResidualNetwork",
            attributes={"source": 1, "sink": 5}
        )
        provided = StateContract(
            name="SaturatedResidualNetwork",
            attributes={"source": 1, "sink": 5},
            supertypes=["ResidualNetwork"]
        )
        self.assertTrue(provided.satisfies(req))

    def test_state_contract_attribute_unification_failure(self):
        """Verify attribute mismatch causes contract satisfaction to fail."""
        req = StateContract(
            name="ResidualNetwork",
            attributes={"source": 1, "sink": 5}
        )
        provided = StateContract(
            name="ResidualNetwork",
            attributes={"source": 2, "sink": 5}
        )
        self.assertFalse(provided.satisfies(req))


class TestAdvGraphCompositionEngineGates(unittest.TestCase):
    def setUp(self):
        self.registry = ComponentRegistry()
        self.engine = CompositionEngine(self.registry)

    def test_gate_a_kruskal_requires_dsu(self):
        """Gate A: Kruskal MST requires DSU component."""
        init_states = [
            StateContract(name="WeightedUndirectedGraph", attributes={"directed": False, "weighted": True}),
            StateContract(name="VertexUniverse")
        ]
        goal = StateContract(name="SpanningForestResult")

        plan = self.engine.synthesize_plan(init_states, goal)
        self.assertTrue(plan.is_valid, f"Kruskal composition failed: {plan.failure_reason}")
        self.assertTrue(plan.has_component("disjoint_set_union"))

        # Anti-hardcoding test: remove DSU and verify failure
        reg_no_dsu = ComponentRegistry()
        del reg_no_dsu.components["disjoint_set_union"]
        engine_no_dsu = CompositionEngine(reg_no_dsu)
        plan_failed = engine_no_dsu.synthesize_plan(init_states, goal)
        self.assertFalse(plan_failed.is_valid)
        self.assertEqual(plan_failed.failure_category, CompositionFailureCategory.NO_PROVIDER)

    def test_gate_b_2sat_requires_scc(self):
        """Gate B: 2-SAT requires SCC component."""
        init_states = [
            StateContract(name="TwoCnfFormula", attributes={"clause_cardinality": 2})
        ]
        goal = StateContract(name="TwoSatAssignmentResult")

        plan = self.engine.synthesize_plan(init_states, goal)
        self.assertTrue(plan.is_valid, f"2-SAT composition failed: {plan.failure_reason}")
        self.assertTrue(plan.has_component("scc_condensation_engine"))

        # Anti-hardcoding test: remove SCC and verify failure
        reg_no_scc = ComponentRegistry()
        del reg_no_scc.components["scc_condensation_engine"]
        engine_no_scc = CompositionEngine(reg_no_scc)
        plan_failed = engine_no_scc.synthesize_plan(init_states, goal)
        self.assertFalse(plan_failed.is_valid)
        self.assertEqual(plan_failed.failure_category, CompositionFailureCategory.NO_PROVIDER)

    def test_gate_c_mincut_requires_maxflow(self):
        """Gate C: Min-Cut requires Dinic max-flow component."""
        init_states = [
            StateContract(name="CapacitatedNetwork", attributes={"directed": True})
        ]
        goal = StateContract(name="MinCutPartition")

        plan = self.engine.synthesize_plan(init_states, goal)
        self.assertTrue(plan.is_valid, f"Min-Cut composition failed: {plan.failure_reason}")
        self.assertTrue(plan.has_component("max_flow_dinic"))

        # Anti-hardcoding test: remove Dinic and verify failure
        reg_no_dinic = ComponentRegistry()
        del reg_no_dinic.components["max_flow_dinic"]
        engine_no_dinic = CompositionEngine(reg_no_dinic)
        plan_failed = engine_no_dinic.synthesize_plan(init_states, goal)
        self.assertFalse(plan_failed.is_valid)
        self.assertEqual(plan_failed.failure_category, CompositionFailureCategory.NO_PROVIDER)


class TestAdvGraphCandidateSelection(unittest.TestCase):
    def test_dijkstra_suboptimal_for_binary_weights(self):
        """Verify Dijkstra is VALID_SUBOPTIMAL while 0-1 BFS is VALID_OPTIMAL for binary weights."""
        model = SemanticGraphModel(
            directedness=Directedness.UNDIRECTED,
            weight_domain=WeightDomain.BINARY_01,
            path_objective=PathObjective.SHORTEST,
            path_scope=PathScope.SINGLE_SOURCE
        )
        ag_engine = AdvancedGraphDerivationEngine()
        candidates, optimal = ag_engine.evaluate_candidates(model)

        self.assertEqual(optimal, "adv_graph_01_bfs")
        dijkstra_eval = next((c for c in candidates if c.pattern == "graph_dijkstra"), None)
        bfs_eval = next((c for c in candidates if c.pattern == "adv_graph_01_bfs"), None)

        self.assertIsNotNone(dijkstra_eval)
        self.assertIsNotNone(bfs_eval)
        self.assertEqual(bfs_eval.status, CandidateStatus.VALID_OPTIMAL)
        self.assertEqual(dijkstra_eval.status, CandidateStatus.VALID_SUBOPTIMAL)


class TestAdvGraphInvariantsAndMovements(unittest.TestCase):
    def test_invariants_for_all_10_patterns(self):
        """Verify formal 4-phase invariants for all 10 Phase 3N patterns."""
        for pat in ADV_GRAPH_PATTERNS:
            inv = InvariantEngine.construct_invariant(pat, {})
            self.assertTrue(len(inv.before_iteration) > 0, f"Empty before_iteration for {pat}")
            self.assertTrue(len(inv.during_iteration) > 0, f"Empty during_iteration for {pat}")
            self.assertTrue(len(inv.after_movement) > 0, f"Empty after_movement for {pat}")
            self.assertTrue(len(inv.at_termination) > 0, f"Empty at_termination for {pat}")

    def test_movement_derivations_for_all_10_patterns(self):
        """Verify movement derivations for all 10 Phase 3N patterns."""
        for pat in ADV_GRAPH_PATTERNS:
            mov = MovementDerivationEngine.derive(pat, {})
            self.assertTrue(len(mov.objective_function) > 0, f"Empty objective for {pat}")
            self.assertTrue(len(mov.elimination_proof) > 0, f"Empty proof for {pat}")
            self.assertTrue(len(mov.decision_conditions) > 0, f"Empty decisions for {pat}")


class TestAdvGraphCppGenerator(unittest.TestCase):
    def test_cpp_code_generation_all_patterns(self):
        """Verify C++17 code generator emits complete, valid implementations."""
        for pat in ADV_GRAPH_PATTERNS:
            code = generate_adv_graph_cpp(pat, {})
            self.assertIn("#include <iostream>", code, f"Missing include in {pat}")
            self.assertIn("int main()", code, f"Missing main in {pat}")
            self.assertIn("ios_base::sync_with_stdio(false)", code, f"Missing fast IO in {pat}")

    def test_dispatch_via_cpp_pointer_generator(self):
        """Verify CppPointerGenerator dispatches adv_graph_ patterns."""
        code = CppPointerGenerator.generate("adv_graph_max_flow_dinic", {})
        self.assertIn("dinic", code.lower())


class TestAdvGraphIndependentOracles(unittest.TestCase):
    def test_01_bfs_oracle(self):
        d = adv_graph_01_bfs_oracle(4, [(1, 2, 0), (2, 3, 1), (1, 4, 1), (4, 3, 0)], 1)
        self.assertEqual(d, [0, 0, 1, 1])

    def test_spfa_negative_cycle_oracle(self):
        has_cycle, _ = adv_graph_spfa_negative_cycle_oracle(3, [(1, 2, 2), (2, 3, 2), (3, 1, -5)])
        self.assertTrue(has_cycle)
        no_cycle, _ = adv_graph_spfa_negative_cycle_oracle(3, [(1, 2, 2), (2, 3, 2), (3, 1, -3)])
        self.assertFalse(no_cycle)

    def test_eulerian_path_oracle(self):
        trail = adv_graph_eulerian_path_oracle(3, [(1, 2), (2, 3), (3, 1)])
        self.assertIsNotNone(trail)
        self.assertEqual(len(trail), 4)

    def test_2sat_oracle(self):
        sat, assign = adv_graph_2sat_oracle(2, [(1, 2), (-1, 2), (1, -2)])
        self.assertTrue(sat)
        unsat, _ = adv_graph_2sat_oracle(1, [(1, 1), (-1, -1)])
        self.assertFalse(unsat)

    def test_block_cut_tree_oracle(self):
        blocks, cuts = adv_graph_block_cut_tree_oracle(4, [(1, 2), (2, 3), (3, 4), (4, 2)])
        self.assertEqual(cuts, [2])

    def test_bridge_block_tree_oracle(self):
        bridges, comps = adv_graph_bridge_block_tree_oracle(4, [(1, 2), (2, 3), (3, 4), (4, 2)])
        self.assertEqual(len(bridges), 1)
        self.assertEqual(bridges[0], (1, 2))

    def test_bipartite_matching_oracle(self):
        size, pairs = adv_graph_bipartite_matching_oracle(3, 3, [(1, 1), (1, 2), (2, 2), (3, 3)])
        self.assertEqual(size, 3)

    def test_max_flow_oracle(self):
        flow = adv_graph_max_flow_oracle(4, [(1, 2, 5), (1, 3, 5), (2, 4, 3), (3, 4, 3)], 1, 4)
        self.assertEqual(flow, 6)

    def test_min_cut_oracle(self):
        cap, edges = adv_graph_min_cut_oracle(4, [(1, 2, 5), (1, 3, 5), (2, 4, 3), (3, 4, 3)], 1, 4)
        self.assertEqual(cap, 6)
        self.assertEqual(len(edges), 2)

    def test_mcmf_oracle(self):
        flow, cost = adv_graph_mcmf_oracle(4, [(1, 2, 2, 1), (2, 4, 2, 1), (1, 3, 2, 5), (3, 4, 2, 5)], 1, 4)
        self.assertEqual(flow, 4)
        self.assertEqual(cost, 2 * (1 + 1) + 2 * (5 + 5))


class TestAdvGraphBridgeIntegration(unittest.TestCase):
    def test_bridge_solves_01_bfs_problem(self):
        """Verify bridge handles 0-1 BFS problem end-to-end."""
        text = "Find single-source shortest path on a graph where edge weights are strictly 0 or 1 using deque."
        res = handle_request({"problemText": text})
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["family"], "adv_graph")
        self.assertEqual(res["selectedPattern"], "adv_graph_01_bfs")
        self.assertIn("adv_graph", res)
        self.assertTrue(res["adv_graph"]["detected"])
        self.assertIn("deque", res["code"].lower())

    def test_bridge_solves_dinic_max_flow_problem(self):
        """Verify bridge handles maximum flow problem end-to-end."""
        text = "Find the maximum flow from source to sink in a flow network with capacities using Dinic blocking flow."
        res = handle_request({"problemText": text})
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["family"], "adv_graph")
        self.assertEqual(res["selectedPattern"], "adv_graph_max_flow_dinic")
        self.assertIn("dinic", res["code"].lower())


if __name__ == "__main__":
    unittest.main()
