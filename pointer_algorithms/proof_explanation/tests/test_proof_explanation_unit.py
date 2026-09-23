"""
Unit tests for CHUP Phase 7 — Proof / Explanation Engine Core.
"""

import unittest
import json
from pointer_algorithms.proof_explanation import (
    EvidenceKind,
    EvidenceRef,
    AuthoritativeEvidenceStore,
    ClaimType,
    ExplanationLevel,
    EpistemicStatus,
    ProblemUnderstandingClaim,
    ProvenFactClaim,
    DerivationClaim,
    ConstraintClaim,
    CandidateEliminationClaim,
    ComponentSelectionClaim,
    CompositionClaim,
    ResourceClaim,
    ProofObligationClaim,
    FinalStatusClaim,
    ProblemUnderstandingSection,
    ProvenFactsSection,
    DerivationSection,
    ConstraintSection,
    CandidateEliminationSection,
    SelectionSection,
    CompositionSection,
    ResourceSection,
    CorrectnessSection,
    VerificationSummarySection,
    ExplanationDocument,
    ExplanationValidator,
    JsonExplanationRenderer,
    MarkdownExplanationRenderer,
    TextExplanationRenderer,
    ProofTraceNavigator
)


class TestProofExplanationUnit(unittest.TestCase):

    def setUp(self):
        self.eref1 = EvidenceRef(
            evidence_id="fact_1",
            kind=EvidenceKind.OBSERVED_FACT,
            source_layer="PHASE_6_SEMANTICS",
            summary="Fact(name=IS_TREE, tier=OBSERVED_FACT, status=PROVEN)",
            fingerprint="hash123"
        )
        self.eref2 = EvidenceRef(
            evidence_id="prov_1",
            kind=EvidenceKind.PROVENANCE_NODE,
            source_layer="PHASE_6_SEMANTICS",
            summary="ProvenanceNode(rule=RULE_FULL_CAYLEY_TREE, target=fact_tree, sources=[fact_1])",
            fingerprint="hash456"
        )
        self.store = AuthoritativeEvidenceStore({
            "fact_1": self.eref1,
            "prov_1": self.eref2
        })

    def test_01_evidence_ref_immutability(self):
        """EvidenceRef must be an immutable frozen dataclass."""
        with self.assertRaises((AttributeError, TypeError)):
            self.eref1.summary = "mutated summary"  # type: ignore

    def test_02_evidence_store_lookup(self):
        """AuthoritativeEvidenceStore lookup and filtering."""
        self.assertTrue(self.store.has_evidence("fact_1"))
        self.assertFalse(self.store.has_evidence("fact_unknown"))
        self.assertEqual(self.store.get_evidence("fact_1"), self.eref1)

        facts = self.store.filter_by_kind(EvidenceKind.OBSERVED_FACT)
        self.assertEqual(len(facts), 1)
        self.assertEqual(facts[0].evidence_id, "fact_1")

    def test_03_claim_serialization_and_roundtrip(self):
        """ExplanationDocument serialization to dict and reconstruction from dict."""
        claim1 = ProblemUnderstandingClaim(
            claim_id="und_v",
            claim_type=ClaimType.PROBLEM_UNDERSTANDING,
            text="Vertex count is 5000",
            evidence_refs=(self.eref1,),
            source_layer="PHASE_6_SEMANTICS",
            epistemic_status=EpistemicStatus.PROVEN,
            dimension="STRUCTURE",
            key="VERTEX_COUNT",
            canonical_value="5000"
        )
        claim2 = ProvenFactClaim(
            claim_id="pf_tree",
            claim_type=ClaimType.PROVEN_FACT,
            text="Tree topology proven",
            evidence_refs=(self.eref1,),
            source_layer="PHASE_6_SEMANTICS",
            epistemic_status=EpistemicStatus.PROVEN,
            fact_name="TREE",
            tier="DERIVED_FACT",
            witness="Cayley theorem discharged"
        )
        doc = ExplanationDocument(
            schema_version="1.0.0",
            problem_id="prob_test_1",
            outcome_state="SATISFIABLE_SINGLE_CANDIDATE",
            level=ExplanationLevel.DETAILED,
            understanding_section=ProblemUnderstandingSection(claims=(claim1,)),
            proven_facts_section=ProvenFactsSection(claims=(claim2,))
        )

        doc_dict = doc.to_dict()
        doc_reconstructed = ExplanationDocument.from_dict(doc_dict)

        self.assertEqual(doc.schema_version, doc_reconstructed.schema_version)
        self.assertEqual(doc.problem_id, doc_reconstructed.problem_id)
        self.assertEqual(doc.outcome_state, doc_reconstructed.outcome_state)
        self.assertEqual(len(doc.all_claims()), len(doc_reconstructed.all_claims()))
        self.assertEqual(doc.understanding_section.claims[0].key, "VERTEX_COUNT")
        self.assertEqual(doc.proven_facts_section.claims[0].fact_name, "TREE")

    def test_04_level_filtering(self):
        """filter_level returns concise view without altering underlying document."""
        claim1 = ProblemUnderstandingClaim(
            claim_id="und_v",
            claim_type=ClaimType.PROBLEM_UNDERSTANDING,
            text="Vertex count 5000",
            evidence_refs=(self.eref1,),
            source_layer="PHASE_6_SEMANTICS",
            epistemic_status=EpistemicStatus.PROVEN,
            dimension="STRUCTURE",
            key="VERTEX_COUNT",
            canonical_value="5000"
        )
        claim2 = DerivationClaim(
            claim_id="der_1",
            claim_type=ClaimType.DERIVATION,
            text="Derived TREE",
            evidence_refs=(self.eref2,),
            source_layer="PHASE_6_SEMANTICS",
            epistemic_status=EpistemicStatus.PROVEN,
            derived_fact="TREE",
            rule_name="FULL_CAYLEY_TREE",
            source_fact_ids=("fact_1",),
            witness="Discharged"
        )
        doc = ExplanationDocument(
            schema_version="1.0.0",
            problem_id="prob_test_1",
            outcome_state="SATISFIABLE_SINGLE_CANDIDATE",
            level=ExplanationLevel.DETAILED,
            understanding_section=ProblemUnderstandingSection(claims=(claim1,)),
            derivation_section=DerivationSection(claims=(claim2,))
        )

        concise_doc = doc.filter_level(ExplanationLevel.CONCISE)
        self.assertEqual(concise_doc.level, ExplanationLevel.CONCISE)
        self.assertEqual(len(concise_doc.derivation_section.claims), 0)
        self.assertEqual(len(concise_doc.understanding_section.claims), 1)

    def test_05_validator_passes_valid_document(self):
        """Validator returns True when all claims have store-backed evidence."""
        claim1 = ProblemUnderstandingClaim(
            claim_id="und_v",
            claim_type=ClaimType.PROBLEM_UNDERSTANDING,
            text="Vertex count is 5000",
            evidence_refs=(self.eref1,),
            source_layer="PHASE_6_SEMANTICS",
            epistemic_status=EpistemicStatus.PROVEN,
            dimension="STRUCTURE",
            key="VERTEX_COUNT",
            canonical_value="5000"
        )
        doc = ExplanationDocument(
            schema_version="1.0.0",
            problem_id="prob_test_1",
            outcome_state="SATISFIABLE_SINGLE_CANDIDATE",
            level=ExplanationLevel.DETAILED,
            understanding_section=ProblemUnderstandingSection(claims=(claim1,))
        )

        res = ExplanationValidator.validate(doc, self.store)
        self.assertTrue(res.valid)
        self.assertEqual(len(res.errors), 0)

    def test_06_validator_rejects_missing_evidence(self):
        """Validator fails closed when claim has empty evidence."""
        claim_bad = ProblemUnderstandingClaim(
            claim_id="und_unbacked",
            claim_type=ClaimType.PROBLEM_UNDERSTANDING,
            text="Unbacked claim",
            evidence_refs=(),
            source_layer="PHASE_6_SEMANTICS",
            epistemic_status=EpistemicStatus.PROVEN,
            dimension="STRUCTURE",
            key="VERTEX_COUNT",
            canonical_value="5000"
        )
        doc = ExplanationDocument(
            schema_version="1.0.0",
            problem_id="prob_test_1",
            outcome_state="SATISFIABLE_SINGLE_CANDIDATE",
            level=ExplanationLevel.DETAILED,
            understanding_section=ProblemUnderstandingSection(claims=(claim_bad,))
        )

        res = ExplanationValidator.validate(doc, self.store)
        self.assertFalse(res.valid)
        self.assertTrue(any("NO evidence references" in e for e in res.errors))

    def test_07_validator_rejects_unknown_evidence_id(self):
        """Validator fails closed when claim references unknown evidence ID."""
        fake_eref = EvidenceRef(
            evidence_id="fake_ghost_id",
            kind=EvidenceKind.OBSERVED_FACT,
            source_layer="PHASE_6_SEMANTICS",
            summary="Fact(fake)"
        )
        claim_bad = ProblemUnderstandingClaim(
            claim_id="und_fake",
            claim_type=ClaimType.PROBLEM_UNDERSTANDING,
            text="Fake claim",
            evidence_refs=(fake_eref,),
            source_layer="PHASE_6_SEMANTICS",
            epistemic_status=EpistemicStatus.PROVEN,
            dimension="STRUCTURE",
            key="VERTEX_COUNT",
            canonical_value="5000"
        )
        doc = ExplanationDocument(
            schema_version="1.0.0",
            problem_id="prob_test_1",
            outcome_state="SATISFIABLE_SINGLE_CANDIDATE",
            level=ExplanationLevel.DETAILED,
            understanding_section=ProblemUnderstandingSection(claims=(claim_bad,))
        )

        res = ExplanationValidator.validate(doc, self.store)
        self.assertFalse(res.valid)
        self.assertTrue(any("references unknown evidence ID" in e for e in res.errors))

    def test_08_validator_rejects_epistemic_violation(self):
        """Validator detects when hypothetical/unresolved fact is claimed as PROVEN."""
        hypo_eref = EvidenceRef(
            evidence_id="hypo_fact",
            kind=EvidenceKind.DERIVED_FACT,
            source_layer="PHASE_6_SEMANTICS",
            summary="Fact(name=DIJKSTRA_COMPATIBLE, tier=DERIVED_FACT, status=HYPOTHETICAL)"
        )
        store_with_hypo = AuthoritativeEvidenceStore({
            "hypo_fact": hypo_eref
        })
        claim_violating = ProvenFactClaim(
            claim_id="pf_viol",
            claim_type=ClaimType.PROVEN_FACT,
            text="Dijkstra is proven",
            evidence_refs=(hypo_eref,),
            source_layer="PHASE_6_SEMANTICS",
            epistemic_status=EpistemicStatus.PROVEN,  # Epistemic violation!
            fact_name="DIJKSTRA_COMPATIBLE",
            tier="DERIVED_FACT",
            witness="Hypothesis only"
        )
        doc = ExplanationDocument(
            schema_version="1.0.0",
            problem_id="prob_test_1",
            outcome_state="SATISFIABLE_SINGLE_CANDIDATE",
            level=ExplanationLevel.DETAILED,
            proven_facts_section=ProvenFactsSection(claims=(claim_violating,))
        )

        res = ExplanationValidator.validate(doc, store_with_hypo)
        self.assertFalse(res.valid)
        self.assertTrue(any("Epistemic violation" in e for e in res.errors))

    def test_09_validator_rejects_subjective_language(self):
        """Validator detects forbidden subjective rankings (e.g. 'best algorithm')."""
        claim_subjective = ProblemUnderstandingClaim(
            claim_id="und_subj",
            claim_type=ClaimType.PROBLEM_UNDERSTANDING,
            text="We selected this because it is the best algorithm for the problem",
            evidence_refs=(self.eref1,),
            source_layer="PHASE_6_SEMANTICS",
            epistemic_status=EpistemicStatus.PROVEN,
            dimension="STRUCTURE",
            key="ALGO",
            canonical_value="best"
        )
        doc = ExplanationDocument(
            schema_version="1.0.0",
            problem_id="prob_test_1",
            outcome_state="SATISFIABLE_SINGLE_CANDIDATE",
            level=ExplanationLevel.DETAILED,
            understanding_section=ProblemUnderstandingSection(claims=(claim_subjective,))
        )

        res = ExplanationValidator.validate(doc, self.store)
        self.assertFalse(res.valid)
        self.assertTrue(any("forbidden subjective phrasing" in e for e in res.errors))

    def test_10_renderers(self):
        """Renderers produce expected non-empty output."""
        claim1 = ProblemUnderstandingClaim(
            claim_id="und_v",
            claim_type=ClaimType.PROBLEM_UNDERSTANDING,
            text="Vertex count is 5000",
            evidence_refs=(self.eref1,),
            source_layer="PHASE_6_SEMANTICS",
            epistemic_status=EpistemicStatus.PROVEN,
            dimension="STRUCTURE",
            key="VERTEX_COUNT",
            canonical_value="5000"
        )
        doc = ExplanationDocument(
            schema_version="1.0.0",
            problem_id="prob_test_1",
            outcome_state="SATISFIABLE_SINGLE_CANDIDATE",
            level=ExplanationLevel.DETAILED,
            understanding_section=ProblemUnderstandingSection(claims=(claim1,))
        )

        # JSON renderer
        j_str = JsonExplanationRenderer.to_json(doc)
        parsed = json.loads(j_str)
        self.assertEqual(parsed["problem_id"], "prob_test_1")

        # Markdown renderer
        md_str = MarkdownExplanationRenderer.render(doc)
        self.assertIn("# CHUP Proof & Verification Explanation", md_str)
        self.assertIn("VERTEX_COUNT", md_str)

        # Text renderer
        txt_str = TextExplanationRenderer.render(doc)
        self.assertIn("CHUP PROOF & EXPLANATION", txt_str)
        self.assertIn("VERTEX_COUNT", txt_str)


if __name__ == "__main__":
    unittest.main()
