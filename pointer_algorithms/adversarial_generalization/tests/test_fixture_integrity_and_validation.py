"""
Test Fixture Cryptographic Integrity & Structural Validation.

Verifies:
1. Every certified benchmark fixture passes SHA-256 fingerprint verification.
2. Any tampered fixture is detected and rejected.
3. Structural validator enforces all schema constraints.
"""

import unittest
from dataclasses import replace

from pointer_algorithms.adversarial_generalization.certified_fixtures import (
    CertifiedFixtureRegistry,
    FixtureValidator,
    CertifiedFixture,
    CanonicalSemanticModel,
    CanonicalFact,
    _create_signed_fixture
)


class TestFixtureIntegrityAndValidation(unittest.TestCase):

    def test_all_fixtures_pass_cryptographic_fingerprint_verification(self):
        fixtures = CertifiedFixtureRegistry.get_all_fixtures()
        self.assertGreaterEqual(len(fixtures), 8, "Expected at least 8 certified fixtures in registry")

        for f in fixtures:
            with self.subTest(fixture_id=f.fixture_id):
                is_valid = FixtureValidator.validate_integrity(f)
                self.assertTrue(is_valid, f"Fixture {f.fixture_id} failed SHA-256 integrity fingerprint check")
                self.assertTrue(len(f.integrity_fingerprint) == 64, "Fingerprint must be 64-char hex string")

    def test_all_fixtures_pass_structural_validation(self):
        fixtures = CertifiedFixtureRegistry.get_all_fixtures()
        for f in fixtures:
            with self.subTest(fixture_id=f.fixture_id):
                errors = FixtureValidator.validate_structure(f)
                self.assertEqual(len(errors), 0, f"Fixture {f.fixture_id} had structural errors: {errors}")

    def test_tampered_fixture_fails_integrity_verification(self):
        fixture = CertifiedFixtureRegistry.get_fixture("CF-ARR-01")
        self.assertIsNotNone(fixture)

        # Tamper with surface variants
        tampered_variants = list(fixture.certified_surface_variants)
        tampered_variants[0] = "Tampered text without valid semantics"

        tampered_fixture = replace(fixture, certified_surface_variants=tuple(tampered_variants))
        self.assertFalse(
            FixtureValidator.validate_integrity(tampered_fixture),
            "Tampered fixture must fail SHA-256 integrity verification"
        )

        errors = FixtureValidator.validate_structure(tampered_fixture)
        self.assertIn("Cryptographic integrity fingerprint mismatch", errors)

    def test_structural_validation_catches_invalid_domains_and_empty_variants(self):
        fixture = CertifiedFixtureRegistry.get_fixture("CF-ARR-01")
        self.assertIsNotNone(fixture)

        # Invalid domain
        invalid_domain_fixture = replace(fixture, domain="quantum_computing")
        errors = FixtureValidator.validate_structure(invalid_domain_fixture)
        self.assertTrue(any("Invalid domain" in e for e in errors))

        # Single surface variant (minimum 2 required)
        single_variant_fixture = replace(fixture, certified_surface_variants=(fixture.certified_surface_variants[0],))
        errors = FixtureValidator.validate_structure(single_variant_fixture)
        self.assertTrue(any("at least 2 certified surface variants" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
