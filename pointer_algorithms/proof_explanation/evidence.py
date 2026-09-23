"""
CHUP Phase 7 — Authoritative Evidence Model & Store.

Defines:
1. EvidenceKind: Authoritative categorization of proof evidence.
2. EvidenceRef: Immutable, deterministic reference to an authoritative artifact.
   Contains canonical metadata representation (not free-form generated prose).
3. AuthoritativeEvidenceStore: Immutable index over Phase 5 and Phase 6 artifacts.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional, Tuple, List, Set
import hashlib
import json


class EvidenceKind(Enum):
    OBSERVED_FACT = "OBSERVED_FACT"
    DERIVED_FACT = "DERIVED_FACT"
    PROVENANCE_NODE = "PROVENANCE_NODE"
    CONSTRAINT = "CONSTRAINT"
    ELIMINATION_CERTIFICATE = "ELIMINATION_CERTIFICATE"
    CAPABILITY_CONTRACT = "CAPABILITY_CONTRACT"
    RESOURCE_VERIFICATION = "RESOURCE_VERIFICATION"
    PROOF_OBLIGATION = "PROOF_OBLIGATION"
    VERIFIED_PLAN = "VERIFIED_PLAN"
    CONFLICT_CERTIFICATE = "CONFLICT_CERTIFICATE"
    AMBIGUITY_REPORT = "AMBIGUITY_REPORT"


@dataclass(frozen=True)
class EvidenceRef:
    """
    Immutable pointer to an authoritative evidence artifact.
    The summary field is strictly a canonical, deterministic metadata representation,
    never free-form generated prose.
    """
    evidence_id: str
    kind: EvidenceKind
    source_layer: str  # e.g., "PHASE_6_SEMANTICS", "PHASE_5_MULTI_CONSTRAINT"
    summary: str       # Canonical metadata representation, e.g. "Fact(NAME=TREE, tier=DERIVED_FACT)"
    fingerprint: Optional[str] = None  # SHA-256 seal or content digest

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "kind": self.kind.value,
            "source_layer": self.source_layer,
            "summary": self.summary,
            "fingerprint": self.fingerprint
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EvidenceRef":
        return cls(
            evidence_id=str(data["evidence_id"]),
            kind=EvidenceKind(data["kind"]),
            source_layer=str(data["source_layer"]),
            summary=str(data["summary"]),
            fingerprint=data.get("fingerprint")
        )


class AuthoritativeEvidenceStore:
    """
    Immutable index of authoritative evidence objects derived from
    Phase 5 and Phase 6 artifacts.
    """

    def __init__(self, evidence_map: Optional[Dict[str, EvidenceRef]] = None):
        self._store: Dict[str, EvidenceRef] = dict(evidence_map or {})

    def has_evidence(self, evidence_id: str) -> bool:
        return evidence_id in self._store

    def get_evidence(self, evidence_id: str) -> Optional[EvidenceRef]:
        return self._store.get(evidence_id)

    def all_evidence(self) -> Tuple[EvidenceRef, ...]:
        # Deterministic sorting by evidence_id
        return tuple(sorted(self._store.values(), key=lambda e: (e.kind.value, e.evidence_id)))

    def filter_by_kind(self, kind: EvidenceKind) -> Tuple[EvidenceRef, ...]:
        return tuple(sorted(
            (e for e in self._store.values() if e.kind == kind),
            key=lambda e: e.evidence_id
        ))

    @classmethod
    def from_artifacts(
        cls,
        phase6_facts: Optional[Any] = None,
        provenance_graph: Optional[Any] = None,
        complexity_envelope: Optional[Any] = None,
        conflict_certificate: Optional[Any] = None,
        ambiguity_report: Optional[Any] = None,
        phase5_result: Optional[Dict[str, Any]] = None,
        verified_plan: Optional[Any] = None
    ) -> "AuthoritativeEvidenceStore":
        """
        Builds the store by directly ingesting authoritative Phase 5 and Phase 6 artifacts.
        """
        store: Dict[str, EvidenceRef] = {}

        # 1. Phase 6 Facts
        if phase6_facts is not None:
            facts_iter = getattr(phase6_facts, "facts", phase6_facts)
            for fact in facts_iter:
                fid = getattr(fact, "fact_id", str(fact))
                fname = getattr(fact, "name", str(fact))
                ftier = getattr(fact, "tier", None)
                tier_str = ftier.value if hasattr(ftier, "value") else str(ftier)
                status = getattr(fact, "proof_status", None)
                status_str = status.value if hasattr(status, "value") else str(status)
                
                kind = EvidenceKind.DERIVED_FACT if tier_str == "DERIVED_FACT" else EvidenceKind.OBSERVED_FACT
                canonical_summary = f"Fact(name={fname}, tier={tier_str}, status={status_str})"
                store[fid] = EvidenceRef(
                    evidence_id=fid,
                    kind=kind,
                    source_layer="PHASE_6_SEMANTICS",
                    summary=canonical_summary,
                    fingerprint=hashlib.sha256(canonical_summary.encode("utf-8")).hexdigest()[:16]
                )

        # 2. Phase 6 Provenance Nodes
        if provenance_graph is not None:
            nodes = getattr(provenance_graph, "nodes", {})
            for pid, node in nodes.items():
                rule = getattr(node, "derivation_rule", "UNKNOWN_RULE")
                target = getattr(node, "target_fact_id", "")
                sources = ",".join(getattr(node, "source_fact_ids", ()))
                canonical_summary = f"ProvenanceNode(rule={rule}, target={target}, sources=[{sources}])"
                store[pid] = EvidenceRef(
                    evidence_id=pid,
                    kind=EvidenceKind.PROVENANCE_NODE,
                    source_layer="PHASE_6_SEMANTICS",
                    summary=canonical_summary,
                    fingerprint=hashlib.sha256(canonical_summary.encode("utf-8")).hexdigest()[:16]
                )

        # Determine run scope prefix for complete cross-run evidence isolation
        plan = verified_plan or (phase5_result.get("verified_plan") if phase5_result else None)
        if plan is not None:
            scope_prefix = getattr(plan, "plan_id", "plan")
        elif conflict_certificate is not None:
            scope_prefix = getattr(conflict_certificate, "conflict_id", getattr(conflict_certificate, "certificate_id", "conflict"))
        elif ambiguity_report is not None:
            scope_prefix = getattr(ambiguity_report, "report_id", "ambig")
        elif phase6_facts and hasattr(phase6_facts, "facts") and phase6_facts.facts:
            scope_prefix = next(iter(phase6_facts.facts)).fact_id
        else:
            scope_prefix = "run_default"

        # 3. Phase 6 Complexity Envelope
        if complexity_envelope is not None:
            env_id = f"{scope_prefix}_env_{getattr(complexity_envelope, 'time_limit_sec', 1.0)}_{getattr(complexity_envelope, 'memory_limit_mb', 256)}"
            n_bound = getattr(complexity_envelope, "n_bound", None)
            q_bound = getattr(complexity_envelope, "q_bound", None)
            canonical_summary = f"ComplexityEnvelope(N={n_bound}, Q={q_bound}, time={getattr(complexity_envelope, 'time_limit_sec', 1.0)}s, mem={getattr(complexity_envelope, 'memory_limit_mb', 256)}MB)"
            store[env_id] = EvidenceRef(
                evidence_id=env_id,
                kind=EvidenceKind.RESOURCE_VERIFICATION,
                source_layer="PHASE_6_SEMANTICS",
                summary=canonical_summary,
                fingerprint=hashlib.sha256(canonical_summary.encode("utf-8")).hexdigest()[:16]
            )

        # 4. Phase 6 Conflict Certificate
        if conflict_certificate is not None:
            competing = getattr(conflict_certificate, "competing_facts", ())
            c_type = getattr(conflict_certificate, "failure_code", getattr(conflict_certificate, "conflict_type", "UNSATISFIABLE_CONFLICT"))
            det_hash = hashlib.sha256(f"{c_type}_{','.join(competing)}".encode("utf-8")).hexdigest()[:8]
            cert_id = getattr(conflict_certificate, "conflict_id", getattr(conflict_certificate, "certificate_id", None)) or f"{scope_prefix}_conflict_{det_hash}"
            canonical_summary = f"ConflictingFactsCertificate(id={cert_id}, type={c_type}, facts=[{','.join(competing)}])"
            store[cert_id] = EvidenceRef(
                evidence_id=cert_id,
                kind=EvidenceKind.CONFLICT_CERTIFICATE,
                source_layer="PHASE_6_SEMANTICS",
                summary=canonical_summary,
                fingerprint=hashlib.sha256(canonical_summary.encode("utf-8")).hexdigest()[:16]
            )

        # 5. Phase 6 Ambiguity Report
        if ambiguity_report is not None:
            amb_facts = getattr(ambiguity_report, "ambiguous_fact_names", ())
            det_hash = hashlib.sha256(','.join(amb_facts).encode("utf-8")).hexdigest()[:8]
            amb_id = getattr(ambiguity_report, "report_id", None) or f"{scope_prefix}_ambig_{det_hash}"
            canonical_summary = f"AmbiguityReport(id={amb_id}, ambiguous_facts=[{','.join(amb_facts)}])"
            store[amb_id] = EvidenceRef(
                evidence_id=amb_id,
                kind=EvidenceKind.AMBIGUITY_REPORT,
                source_layer="PHASE_6_SEMANTICS",
                summary=canonical_summary,
                fingerprint=hashlib.sha256(canonical_summary.encode("utf-8")).hexdigest()[:16]
            )

        # 6. Phase 5 Candidate Analysis / Elimination Certificates
        if phase5_result is not None:
            cand_analysis = phase5_result.get("candidate_analysis")
            if cand_analysis is not None:
                eliminated = getattr(cand_analysis, "eliminated_candidates", {})
                elim_items = eliminated.values() if isinstance(eliminated, dict) else eliminated
                for elim in elim_items:
                    cand_id = getattr(elim, "candidate_id", "unknown_cand")
                    cert_id = f"{scope_prefix}_elim_{cand_id}"
                    reason = getattr(elim, "failure_code", getattr(elim, "rejection_reason", "REJECTED"))
                    viol = getattr(elim, "observed_constraint", getattr(elim, "violated_constraint", "none"))
                    canonical_summary = f"EliminationCertificate(candidate={cand_id}, reason={reason}, violated={viol})"
                    store[cert_id] = EvidenceRef(
                        evidence_id=cert_id,
                        kind=EvidenceKind.ELIMINATION_CERTIFICATE,
                        source_layer="PHASE_5_MULTI_CONSTRAINT",
                        summary=canonical_summary,
                        fingerprint=hashlib.sha256(canonical_summary.encode("utf-8")).hexdigest()[:16]
                    )

            # Phase 5 Conflict Certificate
            p5_conflict = phase5_result.get("conflict_certificate")
            if p5_conflict is not None:
                p5_cid = getattr(p5_conflict, "certificate_id", f"p5_conflict_{id(p5_conflict)}")
                canonical_summary = f"Phase5ConflictCertificate(id={p5_cid})"
                store[p5_cid] = EvidenceRef(
                    evidence_id=p5_cid,
                    kind=EvidenceKind.CONFLICT_CERTIFICATE,
                    source_layer="PHASE_5_MULTI_CONSTRAINT",
                    summary=canonical_summary,
                    fingerprint=hashlib.sha256(canonical_summary.encode("utf-8")).hexdigest()[:16]
                )

        # 7. Phase 5 Verified Plan
        plan = verified_plan or (phase5_result.get("verified_plan") if phase5_result else None)
        if plan is not None:
            plan_id = getattr(plan, "plan_id", f"plan_{id(plan)}")
            outcome = getattr(plan, "outcome_state", None)
            outcome_str = outcome.value if hasattr(outcome, "value") else str(outcome)
            comps = ",".join(getattr(plan, "selected_components", ()))
            seal = getattr(plan, "cryptographic_seal", None)
            canonical_summary = f"VerifiedMultiConstraintPlan(plan_id={plan_id}, outcome={outcome_str}, components=[{comps}])"
            store[plan_id] = EvidenceRef(
                evidence_id=plan_id,
                kind=EvidenceKind.VERIFIED_PLAN,
                source_layer="PHASE_5_MULTI_CONSTRAINT",
                summary=canonical_summary,
                fingerprint=seal
            )

            # Proof Obligations
            obligations = getattr(plan, "proof_obligations", ())
            for ob in obligations:
                ob_id = getattr(ob, "obligation_id", f"ob_{id(ob)}")
                desc = getattr(ob, "description", "")
                discharged = getattr(ob, "discharged", False)
                ob_eid = f"{scope_prefix}_ob_{ob_id}"
                canonical_summary = f"ProofObligation(plan={plan_id}, id={ob_id}, discharged={discharged}, desc={desc})"
                store[ob_eid] = EvidenceRef(
                    evidence_id=ob_eid,
                    kind=EvidenceKind.PROOF_OBLIGATION,
                    source_layer="PHASE_5_MULTI_CONSTRAINT",
                    summary=canonical_summary,
                    fingerprint=hashlib.sha256(canonical_summary.encode("utf-8")).hexdigest()[:16]
                )

            # Synthesized Pipeline Steps & Capability Contracts
            pipeline = getattr(plan, "synthesized_pipeline", ())
            for step in pipeline:
                step_idx = getattr(step, "step_index", 0)
                comp_id = getattr(step, "component_id", "unknown_comp")
                role = getattr(step, "role", "")
                step_eid = f"{plan_id}_step_{step_idx}_{comp_id}"
                canonical_summary = f"SynthesizedPipelineStep(plan={plan_id}, step={step_idx}, component={comp_id}, role={role})"
                store[step_eid] = EvidenceRef(
                    evidence_id=step_eid,
                    kind=EvidenceKind.CAPABILITY_CONTRACT,
                    source_layer="PHASE_5_MULTI_CONSTRAINT",
                    summary=canonical_summary,
                    fingerprint=hashlib.sha256(canonical_summary.encode("utf-8")).hexdigest()[:16]
                )

        return cls(store)
