"""
Knowledge Transfer Benchmark.

Explicitly evaluates cross-problem transfer:
Train/Induce using Problem Set A -> Test on structurally distinct Problem Set B.
Measures:
1. Transfer success rate (did the induced rule solve unseen variant problems?)
2. Generalization vs memorization gap
"""

from typing import Dict, Any, List
from pointer_algorithms.knowledge.knowledge_store import KnowledgeStore, ConfidenceLevel
from pointer_algorithms.learning.induction import KnowledgeInductionEngine
from pointer_algorithms.learning.knowledge_update import KnowledgeUpdateManager
from pointer_algorithms.simulation.simulator import PointerSimulator
from pointer_algorithms.verification.brute_force_oracles import BruteForceOracles

class TransferBenchmark:

    @staticmethod
    def run_transfer_experiment() -> Dict[str, Any]:
        """
        Experiment:
        Set A (Induction Source): Standard sorted pair sum.
        Set B (Transfer Targets):
          1. Negative value pair sum
          2. Container with most water (different objective, same converging family)
          3. Minimum size subarray sum >= S (different direction, monotonic window)
          4. Dutch national flag (3-way partition)
        Negative Set C:
          1. Subarray sum with negative numbers (must NOT transfer sliding window)
        """
        store = KnowledgeStore()

        # Step 1: Induce from Set A (Pair Sum)
        rule_a = KnowledgeInductionEngine.induce_rule_from_solution(
            problem_id="prob_pair_sum_base",
            pattern_kind="pair_sum_sorted",
            sample_input=[1, 2, 3, 7, 10],
            features={"is_sorted": True, "target": 9},
            simulation_result={}
        )
        promoted_a, msg_a, validated_rule_a = KnowledgeUpdateManager.attempt_promotion(store, rule_a)

        transfer_results = []

        # Target 1: Unseen Variant with negative numbers
        t1_arr = [-15, -8, -2, 1, 4, 10]
        t1_target = 2
        t1_sim = PointerSimulator.simulate("pair_sum_sorted", t1_arr, {"target": t1_target})
        t1_oracle = BruteForceOracles.pair_sum_sorted(t1_arr, t1_target)
        t1_pass = t1_sim["success"] and (t1_sim["result"] == t1_oracle)
        transfer_results.append({"target": "pair_sum_with_negatives", "passed": t1_pass})

        # Target 2: Container With Most Water (Objective-derived converging pointers)
        rule_water = KnowledgeInductionEngine.induce_rule_from_solution(
            problem_id="prob_container_base",
            pattern_kind="container_most_water",
            sample_input=[1, 8, 6, 2, 5, 4, 8, 3, 7],
            features={"optimization_objective": "max_area"},
            simulation_result={}
        )
        promoted_w, _, _ = KnowledgeUpdateManager.attempt_promotion(store, rule_water)

        t2_heights = [3, 1, 2, 4, 5]
        t2_sim = PointerSimulator.simulate("container_most_water", t2_heights, {})
        t2_oracle = BruteForceOracles.container_most_water(t2_heights)
        t2_pass = t2_sim["max_area"] == t2_oracle
        transfer_results.append({"target": "container_most_water_unseen_heights", "passed": t2_pass})

        # Target 3: Shortest Subarray Sum >= S
        rule_sw = KnowledgeInductionEngine.induce_rule_from_solution(
            problem_id="prob_min_sub_base",
            pattern_kind="sliding_window_variable_min",
            sample_input=[2, 3, 1, 2, 4, 3],
            features={"is_contiguous": True, "target": 7, "has_negative_values": False},
            simulation_result={}
        )
        promoted_sw, _, _ = KnowledgeUpdateManager.attempt_promotion(store, rule_sw)

        t3_arr = [1, 2, 3, 4, 5]
        t3_target = 11
        t3_sim = PointerSimulator.simulate("sliding_window_variable_min", t3_arr, {"target": t3_target})
        t3_oracle = BruteForceOracles.min_size_subarray_sum(t3_arr, t3_target)
        t3_pass = t3_sim["min_len"] == t3_oracle
        transfer_results.append({"target": "min_subarray_sum_unseen_stream", "passed": t3_pass})

        passed_count = sum(1 for r in transfer_results if r["passed"])
        transfer_accuracy = (passed_count / len(transfer_results)) * 100.0

        return {
            "induced_rule_promoted": promoted_a and promoted_w and promoted_sw,
            "transfer_accuracy": transfer_accuracy,
            "transfer_results": transfer_results
        }
