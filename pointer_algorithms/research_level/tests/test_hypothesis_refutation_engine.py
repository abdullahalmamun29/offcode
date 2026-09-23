"""
Test Suite: Pillar II — Inductive Hypothesis Refutation Engine
Verifies Law 2 (counterexample => REFUTED), Law 3 (exhaustion => SUPPORTED),
Law 4 (no search-to-proof laundering), and Phase 9 oracle integrity inheritance.
"""

import unittest
from pointer_algorithms.self_diagnosis.oracle_integrity import OracleExecutionEvidence
from pointer_algorithms.self_diagnosis.diagnostic_types import OracleStatus
from pointer_algorithms.research_level.hypothesis_refutation import InductiveRefutationEngine
from pointer_algorithms.research_level.research_types import (
    EpistemicStatus,
    FiniteSearchEnvelope,
    HypothesisSchema,
)


class TestHypothesisRefutationEngine(unittest.TestCase):

    def _healthy_oracle_evidence(self):
        return [
            OracleExecutionEvidence(
                exit_code=0,
                stdout="OK\n",
                stderr="",
                crashed=False,
                wall_time_ms=5.0,
            ),
            OracleExecutionEvidence(
                exit_code=0,
                stdout="OK\n",
                stderr="",
                crashed=False,
                wall_time_ms=6.0,
            ),
        ]

    def test_greedy_coin_change_refutation_on_non_canonical_coins(self):
        """
        Verify falsification of GREEDY_BY_KEY hypothesis on coin system {1, 3, 4}.
        Witness target 6: greedy gives 4 + 1 + 1 (3 coins), oracle gives 3 + 3 (2 coins).
        """
        envelope = FiniteSearchEnvelope(
            domain_type="INTEGER_TARGET",
            size_bound=20,
            value_bound=20,
            structural_constraints=("POSITIVE_INTEGERS",),
            max_states_budget=100,
            timeout_ms_budget=1000,
            symmetry_reduction=True,
        )

        def generator(env: FiniteSearchEnvelope):
            for target in range(1, env.size_bound + 1):
                yield target

        def greedy_solver(target: int) -> int:
            coins = [4, 3, 1]
            count = 0
            curr = target
            for c in coins:
                count += curr // c
                curr %= c
            return count

        def oracle_solver(target: int) -> int:
            # Optimal DP for {1, 3, 4}
            coins = [1, 3, 4]
            dp = [0] + [float("inf")] * target
            for i in range(1, target + 1):
                for c in coins:
                    if i >= c:
                        dp[i] = min(dp[i], dp[i - c] + 1)
            return dp[target]

        ref_cert, corrob_cert, status, reason = InductiveRefutationEngine.evaluate_hypothesis(
            hypothesis_id="HYP_GREEDY_COIN_CHANGE",
            schema=HypothesisSchema.GREEDY_BY_KEY,
            envelope=envelope,
            instance_generator=generator,
            hypothesis_solver=greedy_solver,
            reference_oracle=oracle_solver,
            oracle_runs=self._healthy_oracle_evidence(),
            metamorphic_check_passed=True,
            secondary_oracle_agreement=True,
        )

        self.assertEqual(status, EpistemicStatus.REFUTED)
        self.assertIsNotNone(ref_cert)
        self.assertIsNone(corrob_cert)
        self.assertEqual(ref_cert.counterexample_witness["instance"], "6")
        self.assertEqual(ref_cert.hypothesis_output, "3")
        self.assertEqual(ref_cert.oracle_output, "2")
        self.assertIn("falsified", reason)

    def test_interval_scheduling_corroboration_within_envelope(self):
        """
        Verify exhaustive envelope search corroborates earliest-finish-time interval scheduling.
        Law 3 & Law 4: Corroboration emits SUPPORTED, NEVER PROVEN.
        """
        envelope = FiniteSearchEnvelope(
            domain_type="INTERVAL_LIST",
            size_bound=5,
            value_bound=10,
            structural_constraints=("VALID_INTERVALS",),
            max_states_budget=200,
            timeout_ms_budget=2000,
            symmetry_reduction=True,
        )

        sample_instances = [
            [(1, 3), (2, 5), (3, 9)],
            [(1, 2), (2, 3), (3, 4)],
            [(1, 10), (2, 3), (4, 5)],
            [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)],
        ]

        def generator(env: FiniteSearchEnvelope):
            for inst in sample_instances:
                yield inst

        def greedy_eft(intervals):
            # Sort by finish time
            sorted_intervals = sorted(intervals, key=lambda x: x[1])
            count = 0
            last_finish = -1
            for start, finish in sorted_intervals:
                if start >= last_finish:
                    count += 1
                    last_finish = finish
            return count

        def brute_force_oracle(intervals):
            # Compute max independent set of intervals
            n = len(intervals)
            best = 0
            for mask in range(1 << min(n, 12)):
                subset = [intervals[i] for i in range(min(n, 12)) if (mask & (1 << i))]
                # check compatible
                sorted_sub = sorted(subset, key=lambda x: x[0])
                compatible = True
                for i in range(len(sorted_sub) - 1):
                    if sorted_sub[i][1] > sorted_sub[i + 1][0]:
                        compatible = False
                        break
                if compatible:
                    best = max(best, len(subset))
            return best

        ref_cert, corrob_cert, status, reason = InductiveRefutationEngine.evaluate_hypothesis(
            hypothesis_id="HYP_INTERVAL_SCHEDULING_EFT",
            schema=HypothesisSchema.GREEDY_BY_KEY,
            envelope=envelope,
            instance_generator=generator,
            hypothesis_solver=greedy_eft,
            reference_oracle=brute_force_oracle,
            oracle_runs=self._healthy_oracle_evidence(),
            metamorphic_check_passed=True,
            secondary_oracle_agreement=True,
        )

        self.assertIsNone(ref_cert)
        self.assertIsNotNone(corrob_cert)
        self.assertEqual(status, EpistemicStatus.SUPPORTED)
        self.assertNotEqual(status, EpistemicStatus.PROVEN)  # Law 4
        self.assertTrue(corrob_cert.exhaustive_within_envelope)
        self.assertEqual(corrob_cert.states_evaluated, len(sample_instances))

    def test_oracle_defect_halts_as_unresolved(self):
        """
        Verify Phase 9 inheritance: defective reference oracle prevents refutation or corroboration.
        Fails closed to UNRESOLVED (anti-guessing / anti-hallucination).
        """
        bad_oracle_evidence = [
            OracleExecutionEvidence(
                exit_code=1,
                stdout="",
                stderr="Segmentation fault",
                crashed=True,
                exception_name="SIGSEGV",
                wall_time_ms=10.0,
            )
        ]

        envelope = FiniteSearchEnvelope(
            domain_type="INTEGER_TARGET",
            size_bound=10,
            value_bound=10,
            structural_constraints=(),
            max_states_budget=10,
            timeout_ms_budget=1000,
        )

        ref_cert, corrob_cert, status, reason = InductiveRefutationEngine.evaluate_hypothesis(
            hypothesis_id="HYP_ANY",
            schema=HypothesisSchema.LOCAL_OPTIMALITY,
            envelope=envelope,
            instance_generator=lambda env: iter([1, 2, 3]),
            hypothesis_solver=lambda x: x,
            reference_oracle=lambda x: x,
            oracle_runs=bad_oracle_evidence,
        )

        self.assertIsNone(ref_cert)
        self.assertIsNone(corrob_cert)
        self.assertEqual(status, EpistemicStatus.UNRESOLVED)
        self.assertIn("Oracle integrity check failed", reason)

    def test_hypothesis_solver_crash_yields_refutation(self):
        """
        Verify that an unhandled crash inside the hypothesis solver is treated as a definitive counterexample witness.
        """
        envelope = FiniteSearchEnvelope(
            domain_type="INTEGER",
            size_bound=5,
            value_bound=5,
            structural_constraints=(),
            max_states_budget=10,
            timeout_ms_budget=1000,
        )

        def crashing_solver(x: int) -> int:
            if x == 3:
                raise ZeroDivisionError("Division by zero in candidate solver")
            return x

        ref_cert, corrob_cert, status, reason = InductiveRefutationEngine.evaluate_hypothesis(
            hypothesis_id="HYP_CRASHING",
            schema=HypothesisSchema.LOCAL_OPTIMALITY,
            envelope=envelope,
            instance_generator=lambda env: iter([1, 2, 3, 4]),
            hypothesis_solver=crashing_solver,
            reference_oracle=lambda x: x,
            oracle_runs=self._healthy_oracle_evidence(),
            metamorphic_check_passed=True,
            secondary_oracle_agreement=True,
        )

        self.assertEqual(status, EpistemicStatus.REFUTED)
        self.assertIsNotNone(ref_cert)
        self.assertIn("CRASH", ref_cert.hypothesis_output)
        self.assertEqual(ref_cert.counterexample_witness["instance"], "3")


if __name__ == "__main__":
    unittest.main()
