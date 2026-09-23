"""
Test Relevance Discrimination & Distractor Resilience.

Verifies:
1. Extraneous narrative lore produces zero spurious constraints.
2. Authoritative problem parameters are strictly extracted and preserved.
3. Distractor audit flags any leakage or parameter omission.
"""

import unittest

from pointer_algorithms.adversarial_generalization.certified_fixtures import CertifiedFixtureRegistry
from pointer_algorithms.adversarial_generalization.relevance_discriminator import RelevanceDiscriminator
from pointer_algorithms.deep_understanding.deep_understanding_facade import DeepProblemUnderstandingFacade


class TestRelevanceDiscrimination(unittest.TestCase):

    def setUp(self):
        self.facade = DeepProblemUnderstandingFacade()

    def test_distractor_resilience_on_two_sum_lore(self):
        fixture = CertifiedFixtureRegistry.get_fixture("CF-ARR-01")
        self.assertIsNotNone(fixture)
        self.assertIsNotNone(fixture.distractor_spec)
        self.assertIsNotNone(fixture.distractor_surface_variant)

        res = self.facade.process({
            "text": fixture.distractor_surface_variant,
            "n": 100000
        })

        facts = res["phase6_facts"]
        audit_res = RelevanceDiscriminator.audit(
            fixture.distractor_surface_variant,
            fixture.distractor_spec,
            facts
        )

        self.assertTrue(audit_res.is_resilient, f"Distractor audit failed: {audit_res.diagnostics}")
        self.assertEqual(len(audit_res.leaked_lore), 0, f"Leaked lore: {audit_res.leaked_lore}")
        self.assertGreater(len(audit_res.quarantined_lore), 0)
        self.assertGreater(len(audit_res.preserved_parameters), 0)

    def test_distractor_resilience_on_prefix_sum_weather_lore(self):
        fixture = CertifiedFixtureRegistry.get_fixture("CF-ARR-02")
        self.assertIsNotNone(fixture)
        self.assertIsNotNone(fixture.distractor_spec)
        self.assertIsNotNone(fixture.distractor_surface_variant)

        res = self.facade.process({
            "text": fixture.distractor_surface_variant,
            "n": 200000,
            "q": 200000
        })

        facts = res["phase6_facts"]
        audit_res = RelevanceDiscriminator.audit(
            fixture.distractor_surface_variant,
            fixture.distractor_spec,
            facts
        )

        self.assertTrue(audit_res.is_resilient, f"Distractor audit failed: {audit_res.diagnostics}")
        self.assertEqual(len(audit_res.leaked_lore), 0)
        self.assertEqual(len(audit_res.missing_parameters), 0)


if __name__ == "__main__":
    unittest.main()
