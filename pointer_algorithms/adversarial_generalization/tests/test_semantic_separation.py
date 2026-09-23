"""
Test Semantic Separation & Anti-Collapse (Negative Controls).

Verifies:
1. Semantically distinct inputs do NOT collapse into the same mathematical model.
2. 100% of controlled semantic mutations produce distinguishable models or failure states.
"""

import unittest

from pointer_algorithms.adversarial_generalization.certified_fixtures import CertifiedFixtureRegistry
from pointer_algorithms.adversarial_generalization.adversarial_comparator import AdversarialComparator
from pointer_algorithms.deep_understanding.deep_understanding_facade import DeepProblemUnderstandingFacade


class TestSemanticSeparation(unittest.TestCase):

    def setUp(self):
        self.facade = DeepProblemUnderstandingFacade()

    def test_all_controlled_semantic_mutations_are_separated(self):
        fixtures = CertifiedFixtureRegistry.get_all_fixtures()
        total_mutations = 0
        separated_mutations = 0

        for f in fixtures:
            for mutation in f.controlled_semantic_mutations:
                total_mutations += 1
                with self.subTest(fixture_id=f.fixture_id, mutation_id=mutation.mutation_id):
                    res = AdversarialComparator.compare_separation(f, mutation, self.facade)
                    self.assertTrue(
                        res.is_separated,
                        f"Mutation {mutation.mutation_id} collapsed into base model: {res.details}"
                    )
                    self.assertFalse(res.collapsed, f"Semantic collapse detected for {mutation.mutation_id}")
                    separated_mutations += 1

        self.assertGreaterEqual(total_mutations, 6, "Expected at least 6 controlled mutations across fixtures")
        self.assertEqual(separated_mutations, total_mutations, "100% of mutations must separate cleanly")

    def test_specific_critical_separations(self):
        # 1. Sorted vs Unsorted Array
        f_arr = CertifiedFixtureRegistry.get_fixture("CF-ARR-01")
        mut_unsorted = next(m for m in f_arr.controlled_semantic_mutations if "UNSORTED" in m.mutation_id)
        res_unsorted = AdversarialComparator.compare_separation(f_arr, mut_unsorted, self.facade)
        self.assertTrue(res_unsorted.is_separated)

        # 2. Non-negative vs Negative Edge Weights
        f_grp = CertifiedFixtureRegistry.get_fixture("CF-GRP-01")
        mut_neg = next(m for m in f_grp.controlled_semantic_mutations if "NEGATIVE" in m.mutation_id)
        res_neg = AdversarialComparator.compare_separation(f_grp, mut_neg, self.facade)
        self.assertTrue(res_neg.is_separated)

        # 3. Static Array vs Dynamic Point Updates
        f_pre = CertifiedFixtureRegistry.get_fixture("CF-ARR-02")
        mut_dyn = next(m for m in f_pre.controlled_semantic_mutations if "DYNAMIC" in m.mutation_id)
        res_dyn = AdversarialComparator.compare_separation(f_pre, mut_dyn, self.facade)
        self.assertTrue(res_dyn.is_separated)


if __name__ == "__main__":
    unittest.main()
