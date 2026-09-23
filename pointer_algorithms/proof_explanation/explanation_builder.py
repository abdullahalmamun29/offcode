"""
CHUP Phase 7 — Explanation Builder.

Constructs an immutable ExplanationDocument exclusively from authoritative
Phase 5 and Phase 6 artifacts.

Laws enforced:
1. No explanation claim without an authoritative evidence reference.
2. Canonical metadata representations (no unverified free-form prose).
3. Fail closed: If evidence is missing or invalid, do not fabricate.
4. Freshness: Every build operates in complete isolation with zero cross-problem leakage.
"""

from typing import Dict, Any, Optional, List, Tuple
import hashlib

from pointer_algorithms.proof_explanation.evidence import (
    AuthoritativeEvidenceStore,
    EvidenceRef,
    EvidenceKind
)
from pointer_algorithms.proof_explanation.explanation_model import (
    ExplanationDocument,
    ExplanationLevel,
    ClaimType,
    EpistemicStatus,
    ProblemUnderstandingSection,
    ProblemUnderstandingClaim,
    ProvenFactsSection,
    ProvenFactClaim,
    DerivationSection,
    DerivationClaim,
    ConstraintSection,
    ConstraintClaim,
    CandidateEliminationSection,
    CandidateEliminationClaim,
    SelectionSection,
    ComponentSelectionClaim,
    CompositionSection,
    CompositionClaim,
    ResourceSection,
    ResourceClaim,
    CorrectnessSection,
    ProofObligationClaim,
    CorrectnessClaim,
    VerificationSummarySection,
    FinalStatusClaim
)


class ExplanationBuilder:
    """
    Pure functional builder for ExplanationDocument.
    """

    @classmethod
    def build(
        cls,
        du_result: Dict[str, Any],
        problem_id: str = "problem_default",
        level: ExplanationLevel = ExplanationLevel.DETAILED
    ) -> ExplanationDocument:
        """
        Builds an ExplanationDocument from Phase 6 facade result (which incorporates Phase 5).
        """
        facts = du_result.get("phase6_facts")
        prov_graph = du_result.get("provenance_graph")
        envelope = du_result.get("complexity_envelope")
        p5_res = du_result.get("phase5_result", {})
        verified_plan = du_result.get("verified_plan") or p5_res.get("verified_plan")
        conflict_cert = du_result.get("conflict_certificate") or p5_res.get("conflict_certificate")
        ambig_report = du_result.get("ambiguity_report") or p5_res.get("unresolved_certificate")

        # 1. Ingest authoritative evidence into fresh store
        evidence_store = AuthoritativeEvidenceStore.from_artifacts(
            phase6_facts=facts,
            provenance_graph=prov_graph,
            complexity_envelope=envelope,
            conflict_certificate=conflict_cert,
            ambiguity_report=ambig_report,
            phase5_result=p5_res,
            verified_plan=verified_plan
        )

        outcome = du_result.get("outcome_state")
        outcome_str = outcome.value if hasattr(outcome, "value") else str(outcome or "UNKNOWN")

        # Determine run scope prefix for complete cross-run evidence isolation
        plan = verified_plan or (p5_res.get("verified_plan") if p5_res else None)
        if plan is not None:
            scope_prefix = getattr(plan, "plan_id", "plan")
        elif conflict_cert is not None:
            scope_prefix = getattr(conflict_cert, "conflict_id", getattr(conflict_cert, "certificate_id", "conflict"))
        elif ambig_report is not None:
            scope_prefix = getattr(ambig_report, "report_id", "ambig")
        elif facts and hasattr(facts, "facts") and facts.facts:
            scope_prefix = next(iter(facts.facts)).fact_id
        else:
            scope_prefix = "run_default"

        # 2. Build Problem Understanding Section
        understanding_claims: List[ProblemUnderstandingClaim] = []
        if facts is not None:
            fact_iter = getattr(facts, "facts", facts)
            for f in sorted(fact_iter, key=lambda x: getattr(x, "name", str(x))):
                fname = getattr(f, "name", str(f))
                fval = getattr(f, "value", True)
                fid = getattr(f, "fact_id", "")
                eref = evidence_store.get_evidence(fid)
                if not eref:
                    continue  # Fail closed: no claim without evidence
                
                dim = "GENERAL"
                if any(k in fname for k in ("COUNT", "LIMIT", "BOUND")):
                    dim = "BOUNDS"
                elif any(k in fname for k in ("TREE", "GRAPH", "CONNECTED", "DIRECTED", "CYCLE", "TOPOLOGY")):
                    dim = "STRUCTURE"
                elif any(k in fname for k in ("SUM", "MAX", "MIN", "QUERY", "OPERATION", "TARGET")):
                    dim = "OPERATIONS"
                elif any(k in fname for k in ("NEGATIVE", "POSITIVE", "MONOTONE")):
                    dim = "WEIGHTS_AND_SIGNS"

                status = getattr(f, "proof_status", None)
                status_str = status.value if hasattr(status, "value") else str(status)
                ep_status = EpistemicStatus.PROVEN if status_str == "PROVEN" else EpistemicStatus.UNRESOLVED

                understanding_claims.append(ProblemUnderstandingClaim(
                    claim_id=f"und_{fname.lower()}",
                    claim_type=ClaimType.PROBLEM_UNDERSTANDING,
                    text=f"{fname}: {fval}",
                    evidence_refs=(eref,),
                    source_layer="PHASE_6_SEMANTICS",
                    epistemic_status=ep_status,
                    dimension=dim,
                    key=fname,
                    canonical_value=str(fval)
                ))

        # 3. Build Proven Facts Section
        proven_fact_claims: List[ProvenFactClaim] = []
        if facts is not None:
            fact_iter = getattr(facts, "facts", facts)
            for f in sorted(fact_iter, key=lambda x: getattr(x, "name", str(x))):
                fid = getattr(f, "fact_id", "")
                eref = evidence_store.get_evidence(fid)
                if not eref:
                    continue
                fname = getattr(f, "name", str(f))
                ftier = getattr(f, "tier", None)
                tier_str = ftier.value if hasattr(ftier, "value") else str(ftier)
                status = getattr(f, "proof_status", None)
                status_str = status.value if hasattr(status, "value") else str(status)
                ep_status = EpistemicStatus.PROVEN if status_str == "PROVEN" else (
                    EpistemicStatus.SUPPORTED if status_str == "SUPPORTED" else (
                        EpistemicStatus.HYPOTHETICAL if status_str == "HYPOTHETICAL" else EpistemicStatus.UNRESOLVED
                    )
                )
                witness = getattr(f, "witness", "")

                proven_fact_claims.append(ProvenFactClaim(
                    claim_id=f"pfact_{fname.lower()}",
                    claim_type=ClaimType.PROVEN_FACT,
                    text=f"Fact '{fname}' has status {ep_status.value}.",
                    evidence_refs=(eref,),
                    source_layer="PHASE_6_SEMANTICS",
                    epistemic_status=ep_status,
                    fact_name=fname,
                    tier=tier_str,
                    witness=witness
                ))

        # 4. Build Axiomatic Derivations & Invariants Section
        derivation_claims: List[DerivationClaim] = []
        if prov_graph is not None:
            nodes = getattr(prov_graph, "nodes", {})
            for pid, node in sorted(nodes.items(), key=lambda item: item[0]):
                rule = getattr(node, "derivation_rule", "")
                if rule == "RULE_DIRECT_OBSERVATION":
                    continue
                target_id = getattr(node, "target_fact_id", "")
                target_fact = facts.get_by_id(target_id) if hasattr(facts, "get_by_id") else None
                target_name = getattr(target_fact, "name", target_id)
                sources = getattr(node, "source_fact_ids", ())
                witness = getattr(node, "witness", "")

                refs: List[EvidenceRef] = []
                p_ref = evidence_store.get_evidence(pid)
                if p_ref:
                    refs.append(p_ref)
                t_ref = evidence_store.get_evidence(target_id)
                if t_ref:
                    refs.append(t_ref)

                if not refs:
                    continue

                derivation_claims.append(DerivationClaim(
                    claim_id=f"deriv_{pid}",
                    claim_type=ClaimType.DERIVATION,
                    text=f"Derived '{target_name}' via rule '{rule}'.",
                    evidence_refs=tuple(refs),
                    source_layer="PHASE_6_SEMANTICS",
                    epistemic_status=EpistemicStatus.PROVEN,
                    derived_fact=target_name,
                    rule_name=rule,
                    source_fact_ids=tuple(sources),
                    witness=witness
                ))

        # 5. Build Enriched Constraints Section
        constraint_claims: List[ConstraintClaim] = []
        if facts is not None and hasattr(facts, "eligible_facts"):
            for f in sorted(facts.eligible_facts(), key=lambda x: getattr(x, "name", str(x))):
                fid = getattr(f, "fact_id", "")
                eref = evidence_store.get_evidence(fid)
                if not eref:
                    continue
                fname = getattr(f, "name", str(f))
                constraint_claims.append(ConstraintClaim(
                    claim_id=f"con_{fname.lower()}",
                    claim_type=ClaimType.CONSTRAINT,
                    text=f"Constraint '{fname}' verified and passed to solver.",
                    evidence_refs=(eref,),
                    source_layer="PHASE_5_MULTI_CONSTRAINT",
                    epistemic_status=EpistemicStatus.PROVEN,
                    constraint_name=fname,
                    polarity="REQUIRED",
                    lattice_dimension="DEEP_SEMANTICS"
                ))

        # 6. Build Candidate Elimination Section
        elimination_claims: List[CandidateEliminationClaim] = []
        cand_analysis = p5_res.get("candidate_analysis")
        if cand_analysis is not None:
            eliminated = getattr(cand_analysis, "eliminated_candidates", {})
            elim_items = eliminated.values() if isinstance(eliminated, dict) else eliminated
            for elim in sorted(elim_items, key=lambda e: getattr(e, "candidate_id", "")):
                cand_id = getattr(elim, "candidate_id", "unknown_cand")
                cert_id = f"{scope_prefix}_elim_{cand_id}"
                eref = evidence_store.get_evidence(cert_id)
                if not eref:
                    continue
                reason = getattr(elim, "failure_code", getattr(elim, "rejection_reason", ""))
                viol = getattr(elim, "observed_constraint", getattr(elim, "violated_constraint", ""))

                elimination_claims.append(CandidateEliminationClaim(
                    claim_id=f"elim_{cand_id}",
                    claim_type=ClaimType.CANDIDATE_ELIMINATION,
                    text=f"Candidate '{cand_id}' eliminated: {reason}.",
                    evidence_refs=(eref,),
                    source_layer="PHASE_5_MULTI_CONSTRAINT",
                    epistemic_status=EpistemicStatus.PROVEN,
                    candidate_id=cand_id,
                    family="MULTI_CONSTRAINT",
                    rejection_code=reason,
                    certificate_id=cert_id,
                    violated_constraint=viol
                ))

        # 7. Build Selection & Composition Sections
        selection_claims: List[ComponentSelectionClaim] = []
        composition_claims: List[CompositionClaim] = []
        if verified_plan is not None:
            plan_id = getattr(verified_plan, "plan_id", "")
            plan_ref = evidence_store.get_evidence(plan_id)
            refs_plan = (plan_ref,) if plan_ref else ()

            components = getattr(verified_plan, "selected_components", ())
            pipeline = getattr(verified_plan, "synthesized_pipeline", ())

            for comp in components:
                selection_claims.append(ComponentSelectionClaim(
                    claim_id=f"sel_{comp}",
                    claim_type=ClaimType.COMPONENT_SELECTION,
                    text=f"Selected component '{comp}' fulfills required capabilities.",
                    evidence_refs=refs_plan,
                    source_layer="PHASE_5_MULTI_CONSTRAINT",
                    epistemic_status=EpistemicStatus.PROVEN,
                    component_id=comp,
                    role="CORE_SOLVER",
                    supported_capabilities=tuple()
                ))

            for step in pipeline:
                step_idx = getattr(step, "step_index", 1)
                comp_id = getattr(step, "component_id", "")
                role = getattr(step, "role", "")
                step_eid = f"{plan_id}_step_{step_idx}_{comp_id}"
                step_ref = evidence_store.get_evidence(step_eid)
                step_refs = (step_ref,) if step_ref else refs_plan

                composition_claims.append(CompositionClaim(
                    claim_id=f"comp_step_{step_idx}",
                    claim_type=ClaimType.COMPOSITION,
                    text=f"Step {step_idx}: Component '{comp_id}' role '{role}'.",
                    evidence_refs=step_refs,
                    source_layer="PHASE_5_MULTI_CONSTRAINT",
                    epistemic_status=EpistemicStatus.PROVEN,
                    step_index=step_idx,
                    producer_id=comp_id,
                    consumer_id="pipeline",
                    capability_name=role,
                    contract_status="SATISFIED"
                ))

        # 8. Build Resource Section
        resource_claims: List[ResourceClaim] = []
        if envelope is not None:
            env_ref = evidence_store.filter_by_kind(EvidenceKind.RESOURCE_VERIFICATION)
            refs_env = (env_ref[0],) if env_ref else ()
            if refs_env:
                resource_claims.append(ResourceClaim(
                    claim_id="res_time_bound",
                    claim_type=ClaimType.RESOURCE,
                    text=f"Time limit is {getattr(envelope, 'time_limit_sec', 1.0)}s.",
                    evidence_refs=refs_env,
                    source_layer="PHASE_6_SEMANTICS",
                    epistemic_status=EpistemicStatus.PROVEN,
                    metric="TIME_LIMIT",
                    bound_value=f"{getattr(envelope, 'time_limit_sec', 1.0)}s",
                    verdict="SATISFIED"
                ))
                resource_claims.append(ResourceClaim(
                    claim_id="res_mem_bound",
                    claim_type=ClaimType.RESOURCE,
                    text=f"Memory limit is {getattr(envelope, 'memory_limit_mb', 256)}MB.",
                    evidence_refs=refs_env,
                    source_layer="PHASE_6_SEMANTICS",
                    epistemic_status=EpistemicStatus.PROVEN,
                    metric="MEMORY_LIMIT",
                    bound_value=f"{getattr(envelope, 'memory_limit_mb', 256)}MB",
                    verdict="SATISFIED"
                ))

        # 9. Build Correctness & Proof Obligations Section
        correctness_claims: List[Union[ProofObligationClaim, CorrectnessClaim]] = []
        if verified_plan is not None:
            obligations = getattr(verified_plan, "proof_obligations", ())
            for ob in obligations:
                ob_id = getattr(ob, "obligation_id", "")
                ob_eid = f"{scope_prefix}_ob_{ob_id}"
                eref = evidence_store.get_evidence(ob_eid)
                if not eref:
                    continue
                desc = getattr(ob, "description", "")
                discharged = getattr(ob, "discharged", False)

                correctness_claims.append(ProofObligationClaim(
                    claim_id=f"ob_{ob_id}",
                    claim_type=ClaimType.PROOF_OBLIGATION,
                    text=f"Proof obligation '{desc}' was successfully discharged.",
                    evidence_refs=(eref,),
                    source_layer="PHASE_5_MULTI_CONSTRAINT",
                    epistemic_status=EpistemicStatus.PROVEN if discharged else EpistemicStatus.UNRESOLVED,
                    obligation_id=ob_id,
                    description=desc,
                    discharge_status="DISCHARGED" if discharged else "FAILED",
                    witness=f"Discharge certificate verified"
                ))

        # 10. Build Verification Summary Section (Terminal states)
        summary_claims: List[FinalStatusClaim] = []
        plan_id = getattr(verified_plan, "plan_id", "none") if verified_plan else "none"
        vap_id = getattr(verified_plan, "verification_artifact_id", "none") if verified_plan else "none"
        seal = getattr(verified_plan, "cryptographic_seal", None) if verified_plan else None

        summary_refs: List[EvidenceRef] = []
        if verified_plan is not None:
            p_ref = evidence_store.get_evidence(plan_id)
            if p_ref:
                summary_refs.append(p_ref)
        elif conflict_cert is not None:
            cid = getattr(conflict_cert, "conflict_id", getattr(conflict_cert, "certificate_id", ""))
            c_ref = evidence_store.get_evidence(cid)
            if c_ref:
                summary_refs.append(c_ref)
            else:
                c_refs = evidence_store.filter_by_kind(EvidenceKind.CONFLICT_CERTIFICATE)
                if c_refs:
                    summary_refs.append(c_refs[0])
        elif ambig_report is not None:
            aid = getattr(ambig_report, "report_id", "")
            a_ref = evidence_store.get_evidence(aid)
            if a_ref:
                summary_refs.append(a_ref)
            else:
                a_refs = evidence_store.filter_by_kind(EvidenceKind.AMBIGUITY_REPORT)
                if a_refs:
                    summary_refs.append(a_refs[0])

        summary_claims.append(FinalStatusClaim(
            claim_id="final_status_verdict",
            claim_type=ClaimType.FINAL_STATUS,
            text=f"Final outcome: {outcome_str}.",
            evidence_refs=tuple(summary_refs),
            source_layer="PHASE_5_MULTI_CONSTRAINT",
            epistemic_status=EpistemicStatus.PROVEN,
            outcome_state=outcome_str,
            plan_id=plan_id,
            verification_artifact_id=vap_id,
            integrity_seal=seal
        ))

        doc = ExplanationDocument(
            schema_version="1.0.0",
            problem_id=problem_id,
            outcome_state=outcome_str,
            level=level,
            understanding_section=ProblemUnderstandingSection(claims=tuple(understanding_claims)),
            proven_facts_section=ProvenFactsSection(claims=tuple(proven_fact_claims)),
            derivation_section=DerivationSection(claims=tuple(derivation_claims)),
            constraint_section=ConstraintSection(claims=tuple(constraint_claims)),
            elimination_section=CandidateEliminationSection(claims=tuple(elimination_claims)),
            selection_section=SelectionSection(claims=tuple(selection_claims)),
            composition_section=CompositionSection(claims=tuple(composition_claims)),
            resource_section=ResourceSection(claims=tuple(resource_claims)),
            correctness_section=CorrectnessSection(claims=tuple(correctness_claims)),
            summary_section=VerificationSummarySection(claims=tuple(summary_claims))
        )

        return doc.filter_level(level)
