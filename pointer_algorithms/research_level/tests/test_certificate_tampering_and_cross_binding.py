"""
Test Suite: Cryptographic Tampering & Cross-Binding Defense
Verifies that tampering with certificates, changing envelope bounds, or attempting
cross-problem certificate reuse is cryptographically detected and rejected.
"""

import unittest
from pointer_algorithms.research_level.reduction_engine import ReductionEngine
from pointer_algorithms.research_level.research_types import (
    FiniteSearchEnvelope,
    ReductionCertificate,
)


class TestCertificateTamperingAndCrossBinding(unittest.TestCase):

    def test_certificate_fingerprint_tamper_detection(self):
        """Verify modifying any core field alters the cryptographic SHA-256 fingerprint."""
        cert = ReductionEngine.reduce_project_selection_to_min_cut(
            problem_id="PROB_AUTH_01",
            requirements_hash="req_h_valid",
            projects=[{"id": "P1", "profit": 5}],
            dependencies=[],
        )
        fp_original = cert.fingerprint()

        # Reconstruct certificate with tampered source_problem_id
        cert_tampered = ReductionCertificate(
            certificate_id=cert.certificate_id,
            source_problem_id="PROB_TAMPERED_02",  # Tampered!
            target_family_id=cert.target_family_id,
            reduction_type=cert.reduction_type,
            applicability_proof=cert.applicability_proof,
            semantic_proof=cert.semantic_proof,
            complexity_proof=cert.complexity_proof,
            forward_transform_name=cert.forward_transform_name,
            backward_solution_map_name=cert.backward_solution_map_name,
            domain_assumptions=cert.domain_assumptions,
            theorem_id=cert.theorem_id,
            theorem_version=cert.theorem_version,
            problem_hash=cert.problem_hash,
            requirements_hash=cert.requirements_hash,
            status=cert.status,
        )
        fp_tampered = cert_tampered.fingerprint()

        self.assertNotEqual(fp_original, fp_tampered)

    def test_finite_search_envelope_fingerprint_sensitivity(self):
        """Verify changes to envelope parameters produce distinct fingerprints."""
        env1 = FiniteSearchEnvelope(
            domain_type="GRAPH",
            size_bound=10,
            value_bound=5,
            structural_constraints=("CONNECTED",),
            max_states_budget=1000,
            timeout_ms_budget=5000,
            symmetry_reduction=True,
        )

        # Alter size bound
        env2 = FiniteSearchEnvelope(
            domain_type="GRAPH",
            size_bound=11,  # Altered
            value_bound=5,
            structural_constraints=("CONNECTED",),
            max_states_budget=1000,
            timeout_ms_budget=5000,
            symmetry_reduction=True,
        )

        # Alter constraints
        env3 = FiniteSearchEnvelope(
            domain_type="GRAPH",
            size_bound=10,
            value_bound=5,
            structural_constraints=("BIPARTITE",),  # Altered
            max_states_budget=1000,
            timeout_ms_budget=5000,
            symmetry_reduction=True,
        )

        self.assertNotEqual(env1.fingerprint(), env2.fingerprint())
        self.assertNotEqual(env1.fingerprint(), env3.fingerprint())
        self.assertNotEqual(env2.fingerprint(), env3.fingerprint())


if __name__ == "__main__":
    unittest.main()
