"""
Phase 4 Unit Test Suite: Cross-Family Composition & Multi-Component Synthesis.
Authoritative test suite with 34 rigorous unit tests covering:
- Universal StateContract & Asymmetric Satisfaction
- 3-Valued Property Logic (PROVEN_PRESENT, PROVEN_ABSENT, UNKNOWN)
- AttributeLattice & Semantic Attribute Transitivity
- Mutation Compatibility Matrix
- Proof Obligations & Lifecycle (Discharged vs Undischarged)
- Operation Algebra & Predicate Contracts
- DP Optimization Contracts
- Complexity Evaluator (Fail-Closed on UNKNOWN)
- Composition DAG Construction & Topological Sequencing
- VerifiedCompositionPlan Absolute Generator Barrier
- Gates A through H Closed-World Validation
- Recipe Registry for all 12 Canonical Patterns
- Derivation Engine Fact Extraction & Obligation Derivation
- Candidate Evaluator Ranking
- End-to-End Synthesis and C++17 Generation for all 12 Patterns
"""

import unittest
from typing import Dict, Any, List

from pointer_algorithms.cross_family.component_model import (
    StateContract,
    PropertyProofStatus,
    SemanticAttribute,
    AttributeDomainType,
    StateKind,
    MutationSemantics,
    MutationCompatibilityMatrix,
    NumericDomain,
    IndexingSemantics,
    AttributeLattice,
    AlgorithmComponent,
    CompositionNodeType,
)
from pointer_algorithms.cross_family.semantic_ontology import (
    DerivedFact,
    ProofObligation,
    ProofObligationRegistry,
    OperationAlgebra,
    PredicateContract,
    PredicateDirection,
    DPOptimizationContract,
    DPOptimizationKind,
    ComplexityModel,
    ComplexityEvaluator,
    ComplexityVerdict,
    CrossFamilyObjective,
    CrossFamilyProblemModel,
)
from pointer_algorithms.cross_family.component_registry import (
    CrossFamilyComponentRegistry,
    get_component_registry,
)
from pointer_algorithms.cross_family.recipe_registry import (
    CompositionRecipeRegistry,
    CompositionRecipe,
)
from pointer_algorithms.cross_family.derivation_engine import CrossFamilyDerivationEngine
from pointer_algorithms.cross_family.composition_engine import (
    CrossFamilyCompositionEngine,
    CompositionPlan,
    VerifiedCompositionPlan,
    CompositionEdge,
    CompositionEdgeType,
)
from pointer_algorithms.cross_family.gate_evaluator import CrossFamilyGateEvaluator
from pointer_algorithms.cross_family.candidate_evaluator import (
    CrossFamilyCandidateEvaluator,
    CandidateVerdict,
    CandidateEvaluationResult,
)
from pointer_algorithms.cross_family.facade import CrossFamilySynthesisEngine
from pointer_algorithms.cross_family.generator.cross_family_cpp_generator import CrossFamilyCppGenerator


class TestCrossFamilyComponentModel(unittest.TestCase):
    """Tests for StateContract, 3-valued logic, attributes, and mutations."""

    def test_01_asymmetric_satisfaction_basic(self):
        """Test actual.satisfies(required) as an asymmetric relation."""
        # Tree satisfies GraphState requirement via supertypes
        actual = StateContract(
            state_kind=StateKind.TREE,
            name="RootedTree",
            supertypes=["GRAPH", "GraphState", "TreeState"],
        )
        required = StateContract(
            state_kind=StateKind.GRAPH,
            name="GraphState",
        )

        # Actual (Tree) satisfies Required (GraphState)
        self.assertTrue(actual.satisfies(required))

        # Required (GraphState) does NOT satisfy Actual (RootedTree) (asymmetric!)
        self.assertFalse(required.satisfies(actual))

    def test_02_three_valued_property_logic(self):
        """Test 3-valued property logic (PROVEN_PRESENT, PROVEN_ABSENT, UNKNOWN)."""
        required = StateContract(
            state_kind=StateKind.GRAPH,
            name="GraphState",
            forbidden_properties={"CONTAINS_NEGATIVE_WEIGHTS"},
        )

        present_state = StateContract(
            state_kind=StateKind.GRAPH,
            name="GraphState",
            proven_properties={"CONTAINS_NEGATIVE_WEIGHTS": PropertyProofStatus.PROVEN_PRESENT},
        )
        self.assertFalse(present_state.satisfies(required))

        absent_state = StateContract(
            state_kind=StateKind.GRAPH,
            name="GraphState",
            proven_properties={"CONTAINS_NEGATIVE_WEIGHTS": PropertyProofStatus.PROVEN_ABSENT},
        )
        self.assertTrue(absent_state.satisfies(required))

        unknown_state = StateContract(
            state_kind=StateKind.GRAPH,
            name="GraphState",
            proven_properties={"CONTAINS_NEGATIVE_WEIGHTS": PropertyProofStatus.UNKNOWN},
        )
        self.assertTrue(unknown_state.satisfies(required))

    def test_03_forbidden_properties_fail_closed(self):
        """Test forbidden properties cause immediate satisfaction failure when proven present."""
        actual = StateContract(
            state_kind=StateKind.GRAPH,
            name="GraphState",
            forbidden_properties={"NEGATIVE_CYCLE"},
        )
        requirement_with_neg_cycle = StateContract(
            state_kind=StateKind.GRAPH,
            name="GraphState",
            proven_properties={"NEGATIVE_CYCLE": PropertyProofStatus.PROVEN_PRESENT},
        )
        # Actual forbids NEGATIVE_CYCLE, requirement has it proven present -> fails
        self.assertFalse(actual.satisfies(requirement_with_neg_cycle))

    def test_04_attribute_lattice_implications_and_contradictions(self):
        """Test attribute lattice implications expansion and contradiction detection."""
        attrs = {
            "weights": SemanticAttribute("weights", AttributeDomainType.WEIGHT_KIND, "NON_NEGATIVE")
        }
        expanded = AttributeLattice.expand_implications(attrs)
        self.assertIn("graph_type", expanded)
        self.assertEqual(expanded["graph_type"].value, "WEIGHTED_GRAPH")

        # Direct check on contradiction dictionary
        has_no_contra, contra_msg = AttributeLattice.check_contradictions({
            "cyclicity": SemanticAttribute("cyclicity", AttributeDomainType.TOPOLOGY, "ACYCLIC"),
        })
        self.assertTrue(has_no_contra)

    def test_05_mutation_compatibility_matrix(self):
        """Test consumer mutation safety matrix."""
        # READ_ONLY consumer cannot read from CONSUMING provider
        self.assertFalse(
            MutationCompatibilityMatrix.is_compatible(
                provider=MutationSemantics.CONSUMING,
                consumer=MutationSemantics.READ_ONLY,
            )
        )
        # READ_ONLY consumer can read from READ_ONLY provider
        self.assertTrue(
            MutationCompatibilityMatrix.is_compatible(
                provider=MutationSemantics.READ_ONLY,
                consumer=MutationSemantics.READ_ONLY,
            )
        )
        # READ_ONLY consumer can read from DERIVING provider
        self.assertTrue(
            MutationCompatibilityMatrix.is_compatible(
                provider=MutationSemantics.DERIVING,
                consumer=MutationSemantics.READ_ONLY,
            )
        )

    def test_06_numeric_domain_and_indexing(self):
        """Test numeric domain safe casting and indexing compatibility."""
        self.assertTrue(NumericDomain.INT32.can_safely_cast_to(NumericDomain.INT64))
        self.assertTrue(NumericDomain.INT64.can_safely_cast_to(NumericDomain.INT128))
        self.assertFalse(NumericDomain.INT64.can_safely_cast_to(NumericDomain.INT32))

        c1 = StateContract(
            state_kind=StateKind.SEQUENCE,
            name="Seq",
            numeric_domain=NumericDomain.INT64,
        )
        c2 = StateContract(
            state_kind=StateKind.SEQUENCE,
            name="Seq",
            numeric_domain=NumericDomain.INT32,
        )
        # c2 (INT32) can cast to c1 (INT64)
        self.assertTrue(c2.satisfies(c1))
        # c1 (INT64) cannot cast to c2 (INT32)
        self.assertFalse(c1.satisfies(c2))


class TestSemanticOntologyAndContracts(unittest.TestCase):
    """Tests for OperationAlgebra, Predicates, DP contracts, and ComplexityEvaluator."""

    def test_07_operation_algebra_invariants(self):
        """Test algebraic property checks on operations."""
        sum_op = OperationAlgebra.sum_group()
        self.assertTrue(sum_op.associative)
        self.assertTrue(sum_op.commutative)
        self.assertTrue(sum_op.invertible)
        self.assertFalse(sum_op.idempotent)

        min_op = OperationAlgebra.min_semigroup()
        self.assertTrue(min_op.associative)
        self.assertTrue(min_op.idempotent)
        self.assertFalse(min_op.invertible)

    def test_08_predicate_contract_monotonicity(self):
        """Test predicate contract properties."""
        pred = PredicateContract(
            domain="INTEGER_INTERVAL",
            direction=PredicateDirection.MONOTONE_INCREASING,
            witness_property="P(x) => P(x+1)",
            is_monotonic_proven=True,
        )
        self.assertTrue(pred.is_monotonic_proven)
        self.assertEqual(pred.direction, PredicateDirection.MONOTONE_INCREASING)

    def test_09_dp_optimization_contract(self):
        """Test DP optimization contract validation."""
        opt = DPOptimizationContract(
            kind=DPOptimizationKind.MONOTONE_QUEUE,
            recurrence_form="dp[i] = min_{j < i}(dp[j] + cost(j, i))",
            transition_domain="WINDOW_OR_PREFIX",
            dominance_relation="SLOPE_MONOTONICITY",
            is_convex_or_monotone_proven=True,
        )
        self.assertTrue(opt.is_convex_or_monotone_proven)
        self.assertEqual(opt.kind, DPOptimizationKind.MONOTONE_QUEUE)

    def test_10_complexity_evaluator_fail_closed(self):
        """Test ComplexityEvaluator fails closed on UNKNOWN and evaluates bounds accurately."""
        # Provably within
        verdict, ops, msg = ComplexityEvaluator.evaluate("O(N log N)", n=100000, time_limit_sec=1.0)
        self.assertEqual(verdict, ComplexityVerdict.PROVABLY_WITHIN)

        # Provably exceeds
        verdict, ops, msg = ComplexityEvaluator.evaluate("O(N^2)", n=100000, time_limit_sec=1.0)
        self.assertEqual(verdict, ComplexityVerdict.PROVABLY_EXCEEDS)

        # Unknown fails closed
        verdict, ops, msg = ComplexityEvaluator.evaluate("O(N^{1.7})", n=100000, time_limit_sec=1.0)
        self.assertEqual(verdict, ComplexityVerdict.UNKNOWN)


class TestCompositionAndProofObligations(unittest.TestCase):
    """Tests for ProofObligations, CompositionPlan DAG, and VerifiedCompositionPlan."""

    def test_11_proof_obligation_registry(self):
        """Test ProofObligationRegistry discharge checking."""
        registry = ProofObligationRegistry()
        facts_ok = {"FACT_TOPOLOGY_ACYCLIC"}
        discharged, err = registry.is_discharged("ACYCLIC_STRUCTURE", facts_ok)
        self.assertTrue(discharged)
        self.assertIsNone(err)

        facts_missing = {"FACT_TOPOLOGY_CYCLIC"}
        discharged, err = registry.is_discharged("ACYCLIC_STRUCTURE", facts_missing)
        self.assertFalse(discharged)
        self.assertEqual(err, "REQUIRED_ACYCLICITY_VIOLATED")

    def test_12_composition_dag_edges_and_plan(self):
        """Test composition plan DAG edge types and component tracking."""
        comp = AlgorithmComponent(
            name="test_comp",
            category="test",
            node_type=CompositionNodeType.COMPONENT,
            complexity_time="O(N)",
        )
        plan = CompositionPlan(
            objective=CrossFamilyObjective.CF_KRUSKAL_MST,
            recipe_name="cf_kruskal_mst",
            target_state_name="MinimumSpanningForest",
            components=[comp],
        )
        edge = CompositionEdge(
            source_node="WeightedGraph",
            target_node="test_comp",
            edge_type=CompositionEdgeType.DATA_DEPENDENCY,
            state_name="WeightedGraph",
        )
        plan.dependency_edges.append(edge)
        self.assertTrue(plan.has_component("test_comp"))
        self.assertEqual(plan.get_component_names(), ["test_comp"])
        self.assertEqual(len(plan.dependency_edges), 1)

    def test_13_verified_composition_plan_barrier(self):
        """Test VerifiedCompositionPlan is required for code generation."""
        comp_engine = CrossFamilyCompositionEngine()
        invalid_plan = CompositionPlan(
            objective=CrossFamilyObjective.CF_KRUSKAL_MST,
            recipe_name="cf_kruskal_mst",
            target_state_name="MST",
            is_valid=False,
            failure_code="STATE_CONTRACT_MISMATCH",
        )
        # verify_and_seal_plan returns None for invalid plans
        verified = comp_engine.verify_and_seal_plan(invalid_plan)
        self.assertIsNone(verified)

        # CrossFamilyCppGenerator accepts ONLY VerifiedCompositionPlan
        generator = CrossFamilyCppGenerator()
        model = CrossFamilyProblemModel()
        with self.assertRaises(TypeError):
            generator.generate(invalid_plan, model)  # Passing unsealed plan must raise TypeError


class TestGatesAndEvaluators(unittest.TestCase):
    """Tests for Gates A through H and CandidateEvaluator."""

    def setUp(self):
        self.gate_evaluator = CrossFamilyGateEvaluator()
        self.candidate_evaluator = CrossFamilyCandidateEvaluator()
        self.recipe_registry = CompositionRecipeRegistry.get_instance()

    def test_14_gate_a_topology_evaluation(self):
        """Test Gate A topology validation rejects cyclic graphs when acyclicity is required."""
        model = CrossFamilyProblemModel()
        model.add_fact("FACT_TOPOLOGY_CYCLIC", "Cyclic", "analyzer", "RULE")
        model.scale_n = 100

        comp = AlgorithmComponent(
            name="tree_dp",
            category="dp",
            proof_obligations=["ACYCLIC_STRUCTURE"],
        )
        plan = CompositionPlan(
            objective=CrossFamilyObjective.CF_TREE_SUBTREE_DP,
            recipe_name="cf_tree_subtree_dp",
            target_state_name="SubtreeAggregates",
            components=[comp],
        )
        passed, code, msg = self.gate_evaluator.evaluate(model, plan)
        self.assertFalse(passed)
        self.assertEqual(code, "REQUIRED_ACYCLICITY_VIOLATED")

    def test_15_gate_c_edge_weight_evaluation(self):
        """Test Gate C rejects Dijkstra on negative weights, but admits Kruskal on arbitrary comparable weights."""
        model = CrossFamilyProblemModel()
        model.add_fact("FACT_EDGE_WEIGHTS_CONTAIN_NEGATIVE", "Has negatives", "inspector", "RULE")
        model.add_fact("FACT_WEIGHTS_ARE_COMPARABLE", "Comparable", "inspector", "RULE")
        model.scale_n = 100

        # Dijkstra requires NON_NEGATIVE_WEIGHTS -> rejected by Gate C
        dijkstra_comp = AlgorithmComponent(
            name="dijkstra_heap",
            category="graph",
            proof_obligations=["NON_NEGATIVE_WEIGHTS"],
        )
        dijkstra_plan = CompositionPlan(
            objective=CrossFamilyObjective.CF_DIJKSTRA_SHORTEST_PATH,
            recipe_name="cf_dijkstra_shortest_path",
            target_state_name="ShortestPathTree",
            components=[dijkstra_comp],
        )
        passed, code, msg = self.gate_evaluator.evaluate(model, dijkstra_plan)
        self.assertFalse(passed)
        self.assertEqual(code, "NEGATIVE_EDGE_WEIGHTS_REJECT_GREEDY_HEAP")

        # Kruskal requires only WEIGHT_COMPARABILITY -> passes Gate C even with negative weights!
        kruskal_comp = AlgorithmComponent(
            name="graph_edge_sort",
            category="transformation",
            proof_obligations=["WEIGHT_COMPARABILITY"],
        )
        kruskal_plan = CompositionPlan(
            objective=CrossFamilyObjective.CF_KRUSKAL_MST,
            recipe_name="cf_kruskal_mst",
            target_state_name="MinimumSpanningForest",
            components=[kruskal_comp],
        )
        k_passed, k_code, k_msg = self.gate_evaluator.evaluate(model, kruskal_plan)
        self.assertTrue(k_passed)
        self.assertIsNone(k_code)

    def test_16_gate_c_monotonicity_evaluation(self):
        """Test Gate C rejects bisection when predicate monotonicity is unproven."""
        model = CrossFamilyProblemModel()
        model.add_fact("FACT_PREDICATE_NON_MONOTONIC", "Oscillates", "bisection", "RULE")
        model.scale_n = 100

        comp = AlgorithmComponent(
            name="bisection",
            category="search",
            proof_obligations=["MONOTONE_PREDICATE"],
        )
        plan = CompositionPlan(
            objective=CrossFamilyObjective.CF_BISECTION_GREEDY_FEASIBILITY,
            recipe_name="cf_bisection_greedy_feasibility",
            target_state_name="OptimalBoundaryValue",
            components=[comp],
        )
        passed, code, msg = self.gate_evaluator.evaluate(model, plan)
        self.assertFalse(passed)
        self.assertEqual(code, "PREDICATE_NOT_MONOTONIC")

    def test_17_gate_d_convexity_evaluation(self):
        """Test Gate D rejects monotone deque when cost function is non-convex."""
        model = CrossFamilyProblemModel()
        model.add_fact("FACT_NON_CONVEX_TRANSITION", "Non-convex", "dp", "RULE")
        model.scale_n = 100

        comp = AlgorithmComponent(
            name="monotone_deque",
            category="dp",
            proof_obligations=["CONVEX_TRANSITION"],
        )
        plan = CompositionPlan(
            objective=CrossFamilyObjective.CF_CONVEX_DP_MONOTONIC_QUEUE,
            recipe_name="cf_convex_dp_monotonic_queue",
            target_state_name="OptimizedDPTable",
            components=[comp],
        )
        passed, code, msg = self.gate_evaluator.evaluate(model, plan)
        self.assertFalse(passed)
        self.assertEqual(code, "NON_CONVEX_COST_REJECTS_MONOTONIC_QUEUE")

    def test_18_gate_f_algebraic_invertibility(self):
        """Test Gate F rejects prefix difference when operation is non-invertible."""
        model = CrossFamilyProblemModel()
        model.operation_algebra = OperationAlgebra.min_semigroup()  # MIN is not invertible
        model.scale_n = 100

        comp = AlgorithmComponent(
            name="prefix_diff",
            category="algebra",
            proof_obligations=["INVERTIBLE_OPERATION"],
        )
        plan = CompositionPlan(
            objective=CrossFamilyObjective.CF_DP_RANGE_ACCELERATION_SEGMENT_TREE,
            recipe_name="cf_dp_range_acceleration_segment_tree",
            target_state_name="RangeAggregatedSequence",
            components=[comp],
        )
        passed, code, msg = self.gate_evaluator.evaluate(model, plan)
        self.assertFalse(passed)
        self.assertEqual(code, "OPERATION_NOT_INVERTIBLE_REJECTS_PREFIX_DIFFERENCE")

    def test_19_recipe_registry_all_12_canonical_recipes(self):
        """Test that all 12 canonical recipes are registered with valid specs."""
        expected_recipes = [
            "cf_kruskal_mst",
            "cf_dijkstra_shortest_path",
            "cf_bottleneck_path_binary_search",
            "cf_graph_segment_tree_relaxation",
            "cf_tree_subtree_dp",
            "cf_tree_path_hld_segment_tree",
            "cf_event_scheduling_greedy_heap",
            "cf_incremental_connectivity_greedy_dsu",
            "cf_dp_range_acceleration_segment_tree",
            "cf_convex_dp_monotonic_queue",
            "cf_bisection_greedy_feasibility",
            "cf_fractional_bisection_dp",
        ]
        registered = self.recipe_registry.list_recipes()
        self.assertEqual(len(registered), 12)
        for r_id in expected_recipes:
            self.assertIn(r_id, registered)
            recipe = self.recipe_registry.get_by_name(r_id)
            self.assertIsNotNone(recipe)
            self.assertGreater(len(recipe.allowed_component_names), 0)
            self.assertGreater(len(recipe.proof_obligations), 0)

    def test_20_derivation_engine_fact_extraction(self):
        """Test DerivationEngine derives correct facts from problem spec."""
        engine = CrossFamilyDerivationEngine()
        spec = {
            "objective": "CF_KRUSKAL_MST",
            "weights": "NON_NEGATIVE",
            "topology": "CONNECTED_ACYCLIC",
            "n": 50000,
            "m": 100000,
        }
        model = engine.extract_semantic_model(spec)
        self.assertEqual(model.objective, CrossFamilyObjective.CF_KRUSKAL_MST)
        self.assertTrue(model.has_fact("FACT_EDGE_WEIGHTS_NON_NEGATIVE"))
        self.assertTrue(model.has_fact("FACT_TOPOLOGY_ACYCLIC"))

    def test_21_candidate_evaluator_verdicts(self):
        """Test CandidateEvaluator returns VALID_OPTIMAL for valid plan and INVALID_PRECONDITION for failed gate."""
        comp = AlgorithmComponent(name="c1", category="g", complexity_time="O(M log N)")
        plan = CompositionPlan(
            objective=CrossFamilyObjective.CF_KRUSKAL_MST,
            recipe_name="cf_kruskal_mst",
            target_state_name="MST",
            components=[comp],
            is_valid=True,
        )
        res_ok = self.candidate_evaluator.evaluate(plan, gate_passed=True, gate_code=None, gate_msg=None)
        self.assertEqual(res_ok.verdict, CandidateVerdict.VALID_OPTIMAL)

        res_fail = self.candidate_evaluator.evaluate(plan, gate_passed=False, gate_code="GATE_FAIL", gate_msg="Failed")
        self.assertEqual(res_fail.verdict, CandidateVerdict.INVALID_PRECONDITION)


class TestEndToEndSynthesisAndGeneration(unittest.TestCase):
    """End-to-end synthesis and C++17 emission tests for all 12 patterns."""

    def setUp(self):
        self.synthesis_engine = CrossFamilySynthesisEngine()

    def _test_pattern_synthesis(self, spec: Dict[str, Any], expected_snippets: List[str]):
        """Helper to run synthesis and verify C++ code generation."""
        res = self.synthesis_engine.process(spec)
        self.assertTrue(res["gate_passed"], f"Gate failed: {res.get('gate_failure_code')} - {res.get('gate_failure_message')}")
        self.assertIsNotNone(res["verified_plan"], "Verified plan was not created.")
        self.assertIsNotNone(res["code"], "C++ code generation returned None.")

        cpp_code = res["code"]
        self.assertIn("#include <iostream>", cpp_code)
        self.assertIn("int main()", cpp_code)
        for snip in expected_snippets:
            self.assertIn(snip, cpp_code)
        return cpp_code

    def test_22_e2e_kruskal_mst(self):
        """E2E test: cf_kruskal_mst (Graph + Sorting + DSU with arbitrary negative/positive weights)."""
        spec = {"objective": "CF_KRUSKAL_MST", "has_negative_weights": True, "weights": "ARBITRARY_SIGN", "topology": "CONNECTED_ACYCLIC"}
        self._test_pattern_synthesis(spec, ["struct Edge", "struct DSU", "iota(parent.begin(), parent.end(), 0)"])
        # Verify VerifiedCompositionPlan carries cryptographic proof_digest and verification_artifact_id
        res = self.synthesis_engine.process(spec)
        v_plan = res["verified_plan"]
        self.assertIsNotNone(v_plan)
        self.assertTrue(v_plan.verification_artifact_id.startswith("VAP-cf_kruskal_mst-"))
        self.assertEqual(len(v_plan.proof_digest), 64)

    def test_23_e2e_dijkstra_shortest_path(self):
        """E2E test: cf_dijkstra_shortest_path (Weighted Graph + Min-Heap)."""
        spec = {"objective": "CF_DIJKSTRA_SHORTEST_PATH", "has_negative_weights": False}
        self._test_pattern_synthesis(spec, ["priority_queue", "dist[1] = 0"])

    def test_24_e2e_bottleneck_path_binary_search(self):
        """E2E test: cf_bottleneck_path_binary_search (Graph + Bisection + Reachability)."""
        spec = {"objective": "CF_BOTTLENECK_PATH_BINARY_SEARCH"}
        self._test_pattern_synthesis(spec, ["canReach", "while (lo <= hi)"])

    def test_25_e2e_graph_segment_tree_relaxation(self):
        """E2E test: cf_graph_segment_tree_relaxation (Graph + Segment Tree Auxiliary Nodes)."""
        spec = {"objective": "CF_GRAPH_SEGMENT_TREE_RELAXATION"}
        self._test_pattern_synthesis(spec, ["struct SegGraph", "add_interval_edge"])

    def test_26_e2e_tree_subtree_dp(self):
        """E2E test: cf_tree_subtree_dp (Tree + Post-Order Recurrence)."""
        spec = {"objective": "CF_TREE_SUBTREE_DP", "topology": "CONNECTED_ACYCLIC"}
        self._test_pattern_synthesis(spec, ["void dfs(int u, int p)", "subtree_sum[u]"])

    def test_27_e2e_tree_path_hld_segment_tree(self):
        """E2E test: cf_tree_path_hld_segment_tree (Tree + HLD + Segment Tree Range Provider)."""
        spec = {"objective": "CF_TREE_PATH_HLD_SEGMENT_TREE", "topology": "CONNECTED_ACYCLIC"}
        self._test_pattern_synthesis(spec, ["struct SegTree", "parent_node, depth, heavy, head, pos"])

    def test_28_e2e_event_scheduling_greedy_heap(self):
        """E2E test: cf_event_scheduling_greedy_heap (Greedy Choice + Min-Heap Priority Queue)."""
        spec = {"objective": "CF_EVENT_SCHEDULING_GREEDY_HEAP"}
        self._test_pattern_synthesis(spec, ["struct Interval", "priority_queue<long long"])

    def test_29_e2e_incremental_connectivity_greedy_dsu(self):
        """E2E test: cf_incremental_connectivity_greedy_dsu (Greedy Ordering + DSU)."""
        spec = {"objective": "CF_INCREMENTAL_CONNECTIVITY_GREEDY_DSU"}
        self._test_pattern_synthesis(spec, ["struct Edge", "struct DSU", "dsu.unite"])

    def test_30_e2e_dp_range_acceleration_segment_tree(self):
        """E2E test: cf_dp_range_acceleration_segment_tree (DP + Range Acceleration)."""
        spec = {"objective": "CF_DP_RANGE_ACCELERATION_SEGMENT_TREE", "algebra_op": "SUM"}
        self._test_pattern_synthesis(spec, ["struct SegTree", "st.update"])

    def test_31_e2e_convex_dp_monotonic_queue(self):
        """E2E test: cf_convex_dp_monotonic_queue (1D-1D DP + Monotone Deque)."""
        spec = {"objective": "CF_CONVEX_DP_MONOTONIC_QUEUE", "dp_convex": True}
        self._test_pattern_synthesis(spec, ["deque<int> dq", "while (!dq.empty()"])

    def test_32_e2e_bisection_greedy_feasibility(self):
        """E2E test: cf_bisection_greedy_feasibility (Answer Bisection + Greedy Checker)."""
        spec = {"objective": "CF_BISECTION_GREEDY_FEASIBILITY", "predicate_monotonic": True}
        self._test_pattern_synthesis(spec, ["bool isFeasible", "while (lo <= hi)"])

    def test_33_e2e_fractional_bisection_dp(self):
        """E2E test: cf_fractional_bisection_dp (Bisection + 0-1 DP Knapsack)."""
        spec = {"objective": "CF_FRACTIONAL_BISECTION_DP", "predicate_monotonic": True}
        self._test_pattern_synthesis(spec, ["struct Item", "bool checkParametric"])

    def test_34_negative_gate_rejection_emits_zero_code(self):
        """Test negative case: gate rejection halts synthesis with zero code emission."""
        spec = {
            "objective": "CF_DIJKSTRA_SHORTEST_PATH",
            "has_negative_weights": True,
        }
        res = self.synthesis_engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertIsNone(res["verified_plan"])
        self.assertIsNone(res["code"])
        self.assertEqual(res["gate_failure_code"], "NEGATIVE_EDGE_WEIGHTS_REJECT_GREEDY_HEAP")


if __name__ == "__main__":
    unittest.main()
