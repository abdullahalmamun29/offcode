"""
Test Evaluator Order Independence & State Isolation.

Verifies:
1. Evaluating Fixture A followed by Fixture B produces identical evaluation results
   to evaluating Fixture B followed by Fixture A (A -> B == B -> A).
2. Evaluator and comparator harnesses maintain zero cross-evaluation state leakage.
"""

import unittest

from pointer_algorithms.adversarial_generalization.certified_fixtures import CertifiedFixtureRegistry
from pointer_algorithms.adversarial_generalization.adversarial_comparator import AdversarialComparator
from pointer_algorithms.deep_understanding.deep_understanding_facade import DeepProblemUnderstandingFacade


class TestEvaluatorOrderIndependence(unittest.TestCase):

    def setUp(self):
        self.facade = DeepProblemUnderstandingFacade()

    def test_pairwise_order_independence(self):
        f1 = CertifiedFixtureRegistry.get_fixture("CF-ARR-01")
        f2 = CertifiedFixtureRegistry.get_fixture("CF-GRP-01")
        self.assertIsNotNone(f1)
        self.assertIsNotNone(f2)

        # Execution Order 1: f1 then f2
        res1_order1 = AdversarialComparator.compare_invariance(f1, self.facade)
        res2_order1 = AdversarialComparator.compare_invariance(f2, self.facade)

        # Execution Order 2: f2 then f1 (using a new facade instance or same facade)
        facade_order2 = DeepProblemUnderstandingFacade()
        res2_order2 = AdversarialComparator.compare_invariance(f2, facade_order2)
        res1_order2 = AdversarialComparator.compare_invariance(f1, facade_order2)

        # Verify exact equality of evaluation outcomes
        self.assertEqual(res1_order1.canonical_match, res1_order2.canonical_match)
        self.assertEqual(res1_order1.budget_match, res1_order2.budget_match)
        self.assertEqual(res1_order1.plan_equivalent, res1_order2.plan_equivalent)
        self.assertEqual(res1_order1.all_variants_passed, res1_order2.all_variants_passed)

        self.assertEqual(res2_order1.canonical_match, res2_order2.canonical_match)
        self.assertEqual(res2_order1.budget_match, res2_order2.budget_match)
        self.assertEqual(res2_order1.plan_equivalent, res2_order2.plan_equivalent)
        self.assertEqual(res2_order1.all_variants_passed, res2_order2.all_variants_passed)

    def test_repeated_evaluation_determinism(self):
        fixture = CertifiedFixtureRegistry.get_fixture("CF-TRE-01")
        self.assertIsNotNone(fixture)

        results = []
        for _ in range(5):
            res = AdversarialComparator.compare_invariance(fixture, self.facade)
            results.append(res)

        first = results[0]
        for idx, r in enumerate(results[1:], start=2):
            self.assertEqual(first.canonical_match, r.canonical_match, f"Run {idx} differed in canonical_match")
            self.assertEqual(first.budget_match, r.budget_match, f"Run {idx} differed in budget_match")
            self.assertEqual(first.plan_equivalent, r.plan_equivalent, f"Run {idx} differed in plan_equivalent")


if __name__ == "__main__":
    unittest.main()
