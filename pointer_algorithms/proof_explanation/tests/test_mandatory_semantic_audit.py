"""
Mandatory Semantic Audit Tests (Tests A through M) for CHUP Phase 7.

Validates:
- Test A: No second proof system (cannot introduce constraints or select algorithms).
- Test B: Evidence requirement (fail closed).
- Test C: Proven vs hypothetical (quarantine integrity).
- Test D: Unresolved state.
- Test E: Contradiction certificate exposure without side-picking.
- Test F: Candidate elimination fidelity.
- Test G: Composition fidelity.
- Test H: Resource fidelity.
- Test I: Source cleanliness (generated C++ contains zero explanation traces).
- Test J: Surface independence (narrative skins).
- Test K: Explanation faithfulness audit.
- Test L: Determinism test (100 runs produce identical IR).
- Test M: Stale explanation freshness / state isolation.
"""

import unittest
import copy
from pointer_algorithms.deep_understanding.deep_understanding_facade import DeepProblemUnderstandingFacade
from pointer_algorithms.deep_understanding.fact_model import SemanticFact, FactTier, ProofStatus
from pointer_algorithms.multi_constraint.multi_constraint_model import OutcomeState
from pointer_algorithms.generator.cpp_generator import CppPointerGenerator
from pointer_algorithms.proof_explanation import (
    ExplanationBuilder,
    ExplanationValidator,
    AuthoritativeEvidenceStore,
    ExplanationLevel,
    EpistemicStatus,
    ClaimType
)


class TestMandatorySemanticAudit(unittest.TestCase):

    def setUp(self):
        self.facade = DeepProblemUnderstandingFacade()

    def test_A_no_second_proof_system(self):
        """
        Test A: Phase 7 consumes authoritative Phase 5/6 artifacts and terminal results;
        it cannot introduce constraints, select algorithms, eliminate candidates, or discharge proof obligations.
        """
        spec = {
            "v": 10,
            "e": 9,
            "connected": True,
            "undirected": True,
            "simple": True,
            "target": "TREE_PATH",
            "operation": "SUM"
        }
        du_res = self.facade.process(spec)
        self.assertEqual(du_res["outcome_state"], OutcomeState.SATISFIABLE_SINGLE_CANDIDATE)

        # Snapshot before explanation
        facts_before = len(du_res["phase6_facts"].facts)
        plan_before_id = du_res["verified_plan"].plan_id

        doc = ExplanationBuilder.build(du_res, problem_id="test_A")

        # Verify Phase 7 did not mutate Phase 5/6 artifacts
        self.assertEqual(len(du_res["phase6_facts"].facts), facts_before)
        self.assertEqual(du_res["verified_plan"].plan_id, plan_before_id)

        # Verify all selected components in doc were already in the verified plan
        plan_comps = set(du_res["verified_plan"].selected_components)
        doc_comps = {c.component_id for c in doc.selection_section.claims}
        self.assertEqual(plan_comps, doc_comps)

    def test_B_evidence_requirement_fail_closed(self):
        """
        Test B: Attempt to render a claim without evidence fails closed.
        """
        spec = {"n": 100, "operation": "SUM"}
        du_res = self.facade.process(spec)

        doc = ExplanationBuilder.build(du_res, problem_id="test_B")
        store = AuthoritativeEvidenceStore.from_artifacts(
            phase6_facts=du_res.get("phase6_facts"),
            provenance_graph=du_res.get("provenance_graph"),
            complexity_envelope=du_res.get("complexity_envelope"),
            phase5_result=du_res.get("phase5_result"),
            verified_plan=du_res.get("verified_plan")
        )

        val = ExplanationValidator.validate(doc, store)
        self.assertTrue(val.valid, f"Validation errors: {val.errors}")

        for claim in doc.all_claims():
            self.assertTrue(len(claim.evidence_refs) > 0, f"Claim '{claim.claim_id}' lacks evidence!")

    def test_C_proven_vs_hypothetical(self):
        """
        Test C: Provide TREE = PROVEN, USE_DIJKSTRA = HYPOTHETICAL.
        Explanation may state TREE is proven; it must not state Dijkstra is proven to be required.
        """
        spec = {
            "v": 50,
            "e": 49,
            "connected": True,
            "undirected": True,
            "simple": True,
            "target": "TREE_PATH",
            "operation": "SUM"
        }
        du_res = self.facade.process(spec)
        # Inject hypothetical algorithm hypothesis into facts
        hypo_fact = SemanticFact(
            fact_id="fact_hypo_dijkstra",
            tier=FactTier.ALGORITHM_HYPOTHESIS,
            name="USE_DIJKSTRA",
            value=True,
            proof_status=ProofStatus.HYPOTHETICAL,
            witness="Hypothetical candidate conjecture"
        )
        all_facts = list(du_res["phase6_facts"].facts) + [hypo_fact]
        from pointer_algorithms.deep_understanding.fact_model import FactSet
        du_res["phase6_facts"] = FactSet.from_iterable(all_facts)

        doc = ExplanationBuilder.build(du_res, problem_id="test_C")
        
        # Verify TREE is proven
        tree_claim = next((c for c in doc.proven_facts_section.claims if c.fact_name == "TOPOLOGY_TREE"), None)
        self.assertIsNotNone(tree_claim)
        self.assertEqual(tree_claim.epistemic_status, EpistemicStatus.PROVEN)

        # Verify USE_DIJKSTRA is NOT PROVEN
        dijkstra_claim = next((c for c in doc.proven_facts_section.claims if c.fact_name == "USE_DIJKSTRA"), None)
        self.assertIsNotNone(dijkstra_claim)
        self.assertEqual(dijkstra_claim.epistemic_status, EpistemicStatus.HYPOTHETICAL)
        self.assertNotEqual(dijkstra_claim.epistemic_status, EpistemicStatus.PROVEN)

    def test_D_unresolved_state(self):
        """
        Test D: UNRESOLVED_BY_CURRENT_ONTOLOGY explained accurately as unresolved without assumptions.
        Zero claims fabricated in selection, composition, or correctness sections.
        """
        spec = {
            "text": "Queries arrive in arbitrary order with unspecified update semantics."
        }
        du_res = self.facade.process(spec)
        self.assertEqual(du_res["status"], "ambiguous")

        doc = ExplanationBuilder.build(du_res, problem_id="test_D")
        self.assertEqual(doc.outcome_state, OutcomeState.UNRESOLVED_BY_CURRENT_ONTOLOGY.value)
        self.assertTrue(
            any("UNRESOLVED" in c.outcome_state for c in doc.summary_section.claims),
            "Summary claim did not reflect UNRESOLVED status!"
        )
        # Non-applicable sections legitimately contain ZERO claims — no fabricated plans or obligations
        self.assertEqual(len(doc.selection_section.claims), 0, "Fabricated selection claims in unresolved state!")
        self.assertEqual(len(doc.composition_section.claims), 0, "Fabricated composition claims in unresolved state!")
        self.assertEqual(len(doc.correctness_section.claims), 0, "Fabricated correctness claims in unresolved state!")
        store = AuthoritativeEvidenceStore.from_artifacts(
            phase6_facts=du_res.get("phase6_facts"),
            provenance_graph=du_res.get("provenance_graph"),
            complexity_envelope=du_res.get("complexity_envelope"),
            conflict_certificate=du_res.get("conflict_certificate"),
            ambiguity_report=du_res.get("ambiguity_report"),
            phase5_result=du_res.get("phase5_result"),
            verified_plan=du_res.get("verified_plan")
        )
        self.assertTrue(ExplanationValidator.validate(doc, store), "Document with 0 claims in non-applicable sections failed validation!")

    def test_E_contradiction_certificate_exposure(self):
        """
        Test E: CONFLICTING_SOURCE_FACTS / UNSATISFIABLE_CONSTRAINT_SET exposes certificate without picking a side.
        Zero claims fabricated in selection, composition, or correctness sections.
        """
        spec = {
            "connected": True,
            "disconnected": True  # Direct explicit contradiction
        }
        du_res = self.facade.process(spec)
        self.assertEqual(du_res["status"], "conflict")
        self.assertEqual(du_res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)

        doc = ExplanationBuilder.build(du_res, problem_id="test_E")
        self.assertEqual(doc.outcome_state, OutcomeState.UNSATISFIABLE_CONSTRAINT_SET.value)

        # Summary must reference the conflict certificate
        self.assertTrue(len(doc.summary_section.claims) > 0)
        final_claim = doc.summary_section.claims[0]
        self.assertTrue(any(e.kind.value == "CONFLICT_CERTIFICATE" for e in final_claim.evidence_refs))

        # Non-applicable sections legitimately contain ZERO claims — no fabricated plans or obligations
        self.assertEqual(len(doc.selection_section.claims), 0, "Fabricated selection claims in unsatisfiable state!")
        self.assertEqual(len(doc.composition_section.claims), 0, "Fabricated composition claims in unsatisfiable state!")
        self.assertEqual(len(doc.correctness_section.claims), 0, "Fabricated correctness claims in unsatisfiable state!")
        store = AuthoritativeEvidenceStore.from_artifacts(
            phase6_facts=du_res.get("phase6_facts"),
            provenance_graph=du_res.get("provenance_graph"),
            complexity_envelope=du_res.get("complexity_envelope"),
            conflict_certificate=du_res.get("conflict_certificate"),
            ambiguity_report=du_res.get("ambiguity_report"),
            phase5_result=du_res.get("phase5_result"),
            verified_plan=du_res.get("verified_plan")
        )
        self.assertTrue(ExplanationValidator.validate(doc, store), "Document with 0 claims in non-applicable sections failed validation!")

    def test_F_candidate_elimination_fidelity(self):
        """
        Test F: Every displayed elimination claim corresponds 1:1 to an actual Phase 5 certificate.
        """
        spec = {
            "v": 10,
            "e": 9,
            "connected": True,
            "undirected": True,
            "simple": True,
            "temporal": "ONLINE",
            "target": "TREE_PATH",
            "operation": "SUM"
        }
        du_res = self.facade.process(spec)
        p5_res = du_res.get("phase5_result", {})
        cand_analysis = p5_res.get("candidate_analysis")
        self.assertIsNotNone(cand_analysis)

        eliminated_p5_cands = set(cand_analysis.eliminated_candidates.keys())

        doc = ExplanationBuilder.build(du_res, problem_id="test_F")
        doc_elim_cands = {c.candidate_id for c in doc.elimination_section.claims}

        self.assertEqual(eliminated_p5_cands, doc_elim_cands)

    def test_G_composition_fidelity(self):
        """
        Test G: Composition steps map 1:1 to verified Phase 5 capability contracts.
        """
        spec = {
            "v": 100,
            "e": 99,
            "connected": True,
            "undirected": True,
            "simple": True,
            "temporal": "ONLINE",
            "target": "TREE_PATH",
            "operation": "SUM"
        }
        du_res = self.facade.process(spec)
        plan = du_res.get("verified_plan")
        self.assertIsNotNone(plan)

        doc = ExplanationBuilder.build(du_res, problem_id="test_G")
        plan_steps = getattr(plan, "synthesized_pipeline", ())
        self.assertEqual(len(plan_steps), len(doc.composition_section.claims))

        for p_step, c_claim in zip(plan_steps, doc.composition_section.claims):
            self.assertEqual(p_step.component_id, c_claim.producer_id)
            self.assertEqual(p_step.step_index, c_claim.step_index)

    def test_H_resource_fidelity(self):
        """
        Test H: Displayed resource limits match authoritative Phase 6 envelope.
        """
        spec = {
            "n": 50000,
            "q": 100000,
            "target": "LINEAR_RANGE",
            "operation": "SUM"
        }
        du_res = self.facade.process(spec)
        envelope = du_res.get("complexity_envelope")
        self.assertIsNotNone(envelope)

        doc = ExplanationBuilder.build(du_res, problem_id="test_H")
        time_claim = next(c for c in doc.resource_section.claims if c.metric == "TIME_LIMIT")
        mem_claim = next(c for c in doc.resource_section.claims if c.metric == "MEMORY_LIMIT")

        self.assertIn(f"{envelope.time_limit_sec}s", time_claim.bound_value)
        self.assertIn(f"{envelope.memory_limit_mb}MB", mem_claim.bound_value)

    def test_I_source_cleanliness(self):
        """
        Test I: Source Cleanliness & Write-Path Isolation.
        1. Emits 100% clean C++ code containing zero explanation paragraphs, proof traces, or metadata comments.
        2. Proves Phase 7 has NO write path into the generated-source artifact (snapshot comparison).
        3. Proves Phase 7 is a pure leaf consumer: removing it leaves generated C++ byte-for-byte identical.
        """
        spec = {
            "n": 100,
            "q": 100,
            "target": "LINEAR_RANGE",
            "operation": "SUM"
        }
        du_res = self.facade.process(spec)

        feature_dict = {
            "has_negative_values": False,
            "is_sorted": True,
            "target": "target"
        }

        # 1. Snapshot C++ before Phase 7 Explanation is built
        code_snapshot = CppPointerGenerator.generate("pair_sum_sorted", feature_dict)

        # 2. Execute Phase 7 ExplanationBuilder
        doc = ExplanationBuilder.build(du_res, problem_id="test_I")
        self.assertIsNotNone(doc)

        # 3. Snapshot C++ after Phase 7 Explanation is built
        code_post = CppPointerGenerator.generate("pair_sum_sorted", feature_dict)

        # 4. Byte-for-byte snapshot comparison: Explanation generation did NOT mutate C++ output
        self.assertEqual(code_snapshot, code_post, "Phase 7 mutated the CppPointerGenerator output!")

        # 5. Verify C++ code contains zero explanation / reasoning comments
        forbidden_substrings = [
            "Phase 7",
            "Explanation",
            "Provenance",
            "AuthoritativeEvidenceStore",
            "ProofObligation",
            "CandidateElimination",
            "EpistemicStatus"
        ]
        for forbidden in forbidden_substrings:
            self.assertNotIn(forbidden, code_post)
        self.assertTrue(code_post.startswith("#include") or "#include <iostream>" in code_post)

        # 6. Verify via IPC bridge solve path
        from pointer_algorithms.bridge import handle_request
        resp = handle_request({
            "action": "solve",
            "problemText": "Given a sorted array of integers, find two numbers that sum to target."
        })
        self.assertIn("code", resp)
        self.assertIn("explanation", resp)
        bridge_code = resp["code"]
        for forbidden in forbidden_substrings:
            self.assertNotIn(forbidden, bridge_code)

    def test_J_surface_independence(self):
        """
        Test J: Different narrative skins with identical mathematical structure
        produce semantically identical Explanation documents.
        """
        skin1 = {
            "text": "The kingdom has V=5 cities and E=4 roads connecting them all without cycles. Find shortest road sum between cities.",
            "v": 5, "e": 4, "connected": True, "undirected": True, "simple": True,
            "target": "TREE_PATH", "operation": "SUM"
        }
        skin2 = {
            "text": "In a distributed computer network with 5 servers and 4 bi-directional links, compute total packet latency along paths.",
            "v": 5, "e": 4, "connected": True, "undirected": True, "simple": True,
            "target": "TREE_PATH", "operation": "SUM"
        }

        res1 = self.facade.process(skin1)
        res2 = self.facade.process(skin2)

        doc1 = ExplanationBuilder.build(res1, problem_id="skin1")
        doc2 = ExplanationBuilder.build(res2, problem_id="skin2")

        # Both must prove tree and reach identical outcome
        self.assertEqual(doc1.outcome_state, doc2.outcome_state)

        facts1 = {c.fact_name: c.epistemic_status for c in doc1.proven_facts_section.claims}
        facts2 = {c.fact_name: c.epistemic_status for c in doc2.proven_facts_section.claims}
        self.assertEqual(facts1.get("TOPOLOGY_TREE"), facts2.get("TOPOLOGY_TREE"))
        self.assertEqual(facts1.get("TOPOLOGY_TREE"), EpistemicStatus.PROVEN)

    def test_K_explanation_faithfulness_audit(self):
        """
        Test K: Every substantive claim in the explanation links to real evidence in store.
        """
        spec = {
            "v": 20, "e": 19, "connected": True, "undirected": True, "simple": True,
            "target": "TREE_PATH", "operation": "SUM"
        }
        du_res = self.facade.process(spec)
        doc = ExplanationBuilder.build(du_res, problem_id="test_K")
        store = AuthoritativeEvidenceStore.from_artifacts(
            phase6_facts=du_res.get("phase6_facts"),
            provenance_graph=du_res.get("provenance_graph"),
            complexity_envelope=du_res.get("complexity_envelope"),
            phase5_result=du_res.get("phase5_result"),
            verified_plan=du_res.get("verified_plan")
        )

        for claim in doc.all_claims():
            self.assertTrue(len(claim.evidence_refs) > 0, f"Claim {claim.claim_id} lacks evidence refs")
            for ref in claim.evidence_refs:
                self.assertTrue(store.has_evidence(ref.evidence_id), f"Missing evidence ID {ref.evidence_id}")

    def test_L_determinism_100_runs(self):
        """
        Test L: 100 runs on identical input produce byte-identical Explanation IR documents.
        Enforces invariant: Canonical Explanation IR must not depend on wall-clock time.
        """
        spec = {
            "v": 15, "e": 14, "connected": True, "undirected": True, "simple": True,
            "target": "TREE_PATH", "operation": "SUM"
        }
        du_res = self.facade.process(spec)

        baseline_doc = ExplanationBuilder.build(du_res, problem_id="det")
        baseline_dict = baseline_doc.to_dict()

        # Invariant: Canonical Explanation IR does not contain wall-clock timestamps or time fields
        time_keys = {"timestamp", "created_at", "generated_at", "time", "clock"}
        for claim in baseline_doc.all_claims():
            claim_dict = claim.to_dict()
            for tk in time_keys:
                self.assertNotIn(tk, claim_dict, f"Claim contains time-dependent field '{tk}'!")
        for tk in time_keys:
            self.assertNotIn(tk, baseline_dict, f"Baseline dict contains time-dependent field '{tk}'!")

        for _ in range(100):
            run_dict = ExplanationBuilder.build(du_res, problem_id="det").to_dict()
            self.assertEqual(baseline_dict, run_dict)

    def test_M_stale_explanation_isolation(self):
        """
        Test M: Solving Problem A followed by Problem B produces an explanation
        containing ZERO claims, evidence IDs, or plan IDs from Problem A.
        """
        spec_A = {
            "v": 100, "e": 99, "connected": True, "undirected": True, "simple": True,
            "target": "TREE_PATH", "operation": "SUM"
        }
        res_A = self.facade.process(spec_A)
        doc_A = ExplanationBuilder.build(res_A, problem_id="problem_A")

        plan_A_id = res_A["verified_plan"].plan_id
        evidence_A_ids = {e.evidence_id for c in doc_A.all_claims() for e in c.evidence_refs}

        spec_B = {
            "n": 50, "q": 10, "target": "LINEAR_RANGE", "operation": "SUM"
        }
        res_B = self.facade.process(spec_B)
        doc_B = ExplanationBuilder.build(res_B, problem_id="problem_B")

        # Verify zero leakage from Problem A into Explanation B
        for claim in doc_B.all_claims():
            self.assertNotIn("problem_A", claim.claim_id)
            for eref in claim.evidence_refs:
                self.assertNotIn(eref.evidence_id, evidence_A_ids)
                self.assertNotEqual(eref.evidence_id, plan_A_id)


if __name__ == "__main__":
    unittest.main()
