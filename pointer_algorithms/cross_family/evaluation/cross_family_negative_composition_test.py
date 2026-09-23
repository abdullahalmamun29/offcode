"""
CHUP Phase 4: Negative Component Composition Tests (6 Fail-Closed Scenarios).

Verifies fail-closed behavior on invalid composition preconditions:
1. Gate A: Tree Topology Violation -> REQUIRED_ACYCLICITY_VIOLATED
2. Gate B: Negative Edge Weight on Greedy Heap -> NEGATIVE_EDGE_WEIGHTS_REJECT_GREEDY_HEAP
3. Gate C: Predicate Non-Monotonic in Bisection -> PREDICATE_NOT_MONOTONIC
4. Gate D: Non-Convex Cost in Monotonic Deque -> NON_CONVEX_COST_REJECTS_MONOTONIC_QUEUE
5. Gate F: Non-Invertible Operation on Prefix Difference -> OPERATION_NOT_INVERTIBLE_REJECTS_PREFIX_DIFFERENCE
6. Gate G: State Space Resource Budget Exceeded -> STATE_SPACE_EXCEEDS_RESOURCE_BOUNDS
"""

import unittest
from pointer_algorithms.cross_family.facade import CrossFamilySynthesisEngine
from pointer_algorithms.cross_family.candidate_evaluator import CandidateVerdict


class TestCrossFamilyNegativeComposition(unittest.TestCase):
    def setUp(self):
        self.engine = CrossFamilySynthesisEngine()

    def test_neg_01_gate_a_tree_topology_violation(self):
        """1. Gate A: Tree Subtree DP on Cyclic Graph -> REQUIRED_ACYCLICITY_VIOLATED"""
        spec = {
            "objective": "CF_TREE_SUBTREE_DP",
            "is_cyclic": True,
            "topology": "CYCLIC"
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "REQUIRED_ACYCLICITY_VIOLATED")
        self.assertIsNone(res["verified_plan"])
        self.assertIsNone(res["code"])
        self.assertEqual(res["eval_result"].verdict, CandidateVerdict.INVALID_PRECONDITION)

    def test_neg_02_gate_b_negative_weight_violation(self):
        """2. Gate B: Dijkstra Greedy Frontier on Negative Edges -> NEGATIVE_EDGE_WEIGHTS_REJECT_GREEDY_HEAP"""
        spec = {
            "objective": "CF_DIJKSTRA_SHORTEST_PATH",
            "has_negative_weights": True
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "NEGATIVE_EDGE_WEIGHTS_REJECT_GREEDY_HEAP")
        self.assertIsNone(res["verified_plan"])
        self.assertIsNone(res["code"])
        self.assertEqual(res["eval_result"].verdict, CandidateVerdict.INVALID_PRECONDITION)

    def test_neg_03_gate_c_non_monotonic_predicate(self):
        """3. Gate C: Answer Bisection on Oscillating Predicate -> PREDICATE_NOT_MONOTONIC"""
        spec = {
            "objective": "CF_BISECTION_GREEDY_FEASIBILITY",
            "predicate_monotonic": False
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "PREDICATE_NOT_MONOTONIC")
        self.assertIsNone(res["verified_plan"])
        self.assertIsNone(res["code"])
        self.assertEqual(res["eval_result"].verdict, CandidateVerdict.INVALID_PRECONDITION)

    def test_neg_04_gate_d_non_convex_dp_cost(self):
        """4. Gate D: Monotone Queue DP on Non-Convex Transition -> NON_CONVEX_COST_REJECTS_MONOTONIC_QUEUE"""
        spec = {
            "objective": "CF_CONVEX_DP_MONOTONIC_QUEUE",
            "dp_convex": False
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "NON_CONVEX_COST_REJECTS_MONOTONIC_QUEUE")
        self.assertIsNone(res["verified_plan"])
        self.assertIsNone(res["code"])
        self.assertEqual(res["eval_result"].verdict, CandidateVerdict.INVALID_PRECONDITION)

    def test_neg_05_gate_f_non_invertible_operation(self):
        """5. Gate F: Prefix Difference Range Acceleration on Non-Invertible Operation -> OPERATION_NOT_INVERTIBLE_REJECTS_PREFIX_DIFFERENCE"""
        # Testing Gate F with a direct plan having INVERTIBLE_OPERATION obligation and MIN algebra
        from pointer_algorithms.cross_family.component_model import AlgorithmComponent
        from pointer_algorithms.cross_family.composition_engine import CompositionPlan
        from pointer_algorithms.cross_family.semantic_ontology import CrossFamilyProblemModel, OperationAlgebra
        from pointer_algorithms.cross_family.gate_evaluator import CrossFamilyGateEvaluator

        model = CrossFamilyProblemModel()
        model.scale_n = 1000
        model.operation_algebra = OperationAlgebra.min_semigroup()

        comp = AlgorithmComponent(
            name="prefix_diff",
            category="algebra",
            proof_obligations=["INVERTIBLE_OPERATION"]
        )
        plan = CompositionPlan(
            objective=None,
            recipe_name="prefix_diff_min",
            target_state_name="RangeAggregatedSequence",
            components=[comp]
        )
        passed, code, msg = CrossFamilyGateEvaluator.evaluate(model, plan)
        self.assertFalse(passed)
        self.assertEqual(code, "OPERATION_NOT_INVERTIBLE_REJECTS_PREFIX_DIFFERENCE")

    def test_neg_06_gate_g_resource_budget_exceeded(self):
        """6. Gate G: Complexity Exceeds Time Limit -> STATE_SPACE_EXCEEDS_RESOURCE_BOUNDS"""
        from pointer_algorithms.cross_family.component_model import AlgorithmComponent
        from pointer_algorithms.cross_family.composition_engine import CompositionPlan
        from pointer_algorithms.cross_family.semantic_ontology import CrossFamilyProblemModel
        from pointer_algorithms.cross_family.gate_evaluator import CrossFamilyGateEvaluator

        model = CrossFamilyProblemModel()
        model.scale_n = 500000
        model.time_limit_sec = 0.5  # 500,000^2 = 2.5 * 10^11 operations, far exceeds 0.5s limit

        comp = AlgorithmComponent(
            name="quadratic_all_pairs",
            category="graph",
            complexity_time="O(N^2)"
        )
        plan = CompositionPlan(
            objective=None,
            recipe_name="all_pairs",
            target_state_name="DistMatrix",
            components=[comp]
        )
        passed, code, msg = CrossFamilyGateEvaluator.evaluate(model, plan)
        self.assertFalse(passed)
        self.assertEqual(code, "STATE_SPACE_EXCEEDS_RESOURCE_BOUNDS")


if __name__ == "__main__":
    unittest.main()
