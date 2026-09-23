"""
Test Certified Paraphrase & Surface Invariance.

Verifies:
1. 100% semantic invariance across all certified surface variants.
2. Canonical mathematical models and symbolic budgets remain identical.
3. Verified plans are canonically equivalent.
"""

import unittest

from pointer_algorithms.adversarial_generalization.certified_fixtures import CertifiedFixtureRegistry
from pointer_algorithms.adversarial_generalization.adversarial_comparator import AdversarialComparator
from pointer_algorithms.deep_understanding.deep_understanding_facade import DeepProblemUnderstandingFacade


class TestCertifiedParaphraseInvariance(unittest.TestCase):

    def setUp(self):
        self.facade = DeepProblemUnderstandingFacade()

    def test_paraphrase_invariance_across_all_certified_fixtures(self):
        fixtures = CertifiedFixtureRegistry.get_all_fixtures()
        total_fixtures = len(fixtures)
        passed_fixtures = 0

        for f in fixtures:
            with self.subTest(fixture_id=f.fixture_id, domain=f.domain):
                res = AdversarialComparator.compare_invariance(f, self.facade)
                self.assertTrue(
                    res.all_variants_passed,
                    f"Fixture {f.fixture_id} failed invariance: {res.details}"
                )
                self.assertTrue(res.canonical_match, f"Canonical model mismatch for {f.fixture_id}")
                self.assertTrue(res.budget_match, f"Symbolic budget mismatch for {f.fixture_id}")
                self.assertTrue(res.plan_equivalent, f"Plan equivalence failure for {f.fixture_id}")
                passed_fixtures += 1

        self.assertEqual(passed_fixtures, total_fixtures, "All fixtures must pass 100% paraphrase invariance")

    def test_domain_specific_invariance_batteries(self):
        domains = ["array", "graph", "tree", "algebra", "numerical"]
        for d in domains:
            domain_fixtures = CertifiedFixtureRegistry.get_fixtures_by_domain(d)
            self.assertGreater(len(domain_fixtures), 0, f"Expected fixtures for domain: {d}")
            for f in domain_fixtures:
                with self.subTest(domain=d, fixture_id=f.fixture_id):
                    res = AdversarialComparator.compare_invariance(f, self.facade)
                    self.assertTrue(res.all_variants_passed)


if __name__ == "__main__":
    unittest.main()
