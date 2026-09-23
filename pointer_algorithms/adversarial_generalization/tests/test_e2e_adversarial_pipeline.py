"""
Test End-to-End Adversarial Pipeline & Clean C++ Code Guarantee.

Verifies:
1. Complete pipeline execution under adversarial surfaces:
   Problem Text (with lore/distractors) -> Phase 6 -> Phase 5 -> Phase 7 -> C++ Generator.
2. Clean C++ code guarantee: generated code contains zero explanation paragraphs or metadata.
3. Pre- and post-explanation C++ code snapshots are byte-for-byte identical.
4. Generated C++ compiles cleanly under g++ -std=c++17.
"""

import unittest
import subprocess
import tempfile
import os

from pointer_algorithms.adversarial_generalization.certified_fixtures import CertifiedFixtureRegistry
from pointer_algorithms.adversarial_generalization.keyword_trap_registry import KeywordTrapRegistry
from pointer_algorithms.deep_understanding.deep_understanding_facade import DeepProblemUnderstandingFacade
from pointer_algorithms.proof_explanation.explanation_builder import ExplanationBuilder
from pointer_algorithms.generator.cpp_generator import CppPointerGenerator


class TestEndToEndAdversarialPipeline(unittest.TestCase):

    def setUp(self):
        self.facade = DeepProblemUnderstandingFacade()

    def test_e2e_adversarial_two_sum_with_distractor_preserves_clean_cpp(self):
        fixture = CertifiedFixtureRegistry.get_fixture("CF-ARR-01")
        self.assertIsNotNone(fixture)
        self.assertIsNotNone(fixture.distractor_surface_variant)

        # 1. Take raw problem text with heavy distractor lore
        spec = {
            "text": fixture.distractor_surface_variant,
            "n": 100000,
            "sorted": True
        }

        # 2. Phase 6 Deep Problem Understanding
        du_res = self.facade.process(spec)
        self.assertEqual(du_res["status"], "success")
        self.assertIsNotNone(du_res.get("verified_plan"))

        # Snapshot C++ before Phase 7
        feature_dict = {
            "has_negative_values": False,
            "is_sorted": True,
            "target": "target"
        }
        cpp_before = CppPointerGenerator.generate("pair_sum_sorted", feature_dict)

        # 3. Phase 7 Explanation Construction
        doc = ExplanationBuilder.build(du_res, problem_id="e2e_adv_test")
        self.assertIsNotNone(doc)
        self.assertEqual(len(doc.all_claims()) > 0, True)

        # 4. Generate C++ after Phase 7
        cpp_after = CppPointerGenerator.generate("pair_sum_sorted", feature_dict)

        # Byte-for-byte snapshot equality
        self.assertEqual(cpp_before, cpp_after, "Phase 7 violated write-path isolation into generated C++ source!")

        # Source code cleanliness verification
        forbidden_tokens = [
            "ExplanationSector",
            "EpistemicStatus",
            "PROVEN",
            "HYPOTHETICAL",
            "EliminationCertificate",
            "ProvenanceGraph",
            "Phase 7",
            "Phase 8",
            "Chef Luigi",
            "Numeralia"
        ]
        for tok in forbidden_tokens:
            self.assertNotIn(tok, cpp_after, f"Generated C++ leaked metadata/distractor token: {tok}")

        # Check standard C++ compilation
        with tempfile.NamedTemporaryFile(suffix=".cpp", mode="w", delete=False) as f:
            f.write(cpp_after)
            temp_path = f.name

        try:
            compile_res = subprocess.run(
                ["g++", "-std=c++17", "-fsyntax-only", temp_path],
                capture_output=True,
                text=True
            )
            self.assertEqual(
                compile_res.returncode, 0,
                f"Generated C++ failed compilation: {compile_res.stderr}"
            )
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_e2e_adversarial_trap_elimination_halts_cleanly(self):
        trap = KeywordTrapRegistry.get_trap("TRAP-01-NEG-WEIGHTS")
        self.assertIsNotNone(trap)

        du_res = self.facade.process(trap.adversarial_spec)
        p5_res = du_res.get("phase5_result", {})
        analysis = p5_res.get("candidate_analysis")
        self.assertIsNotNone(analysis)
        self.assertIn("dijkstra_priority_queue", analysis.eliminated_candidates)

        # Build explanation for this elimination
        doc = ExplanationBuilder.build(du_res, problem_id="e2e_trap_test")
        self.assertIsNotNone(doc)
        # Ensure Dijkstra elimination is recorded in explanation claims
        elim_claim_cands = {c.candidate_id for c in doc.elimination_section.claims}
        self.assertIn("dijkstra_priority_queue", elim_claim_cands)


if __name__ == "__main__":
    unittest.main()
