"""
CHUP Phase 7 — Explanation IR Model.

Defines an immutable, typed Explanation Intermediate Representation (IR):
- Strongly-typed claim payloads (discriminated union over ClaimType)
- Epistemic statuses (PROVEN, SUPPORTED, HYPOTHETICAL, UNRESOLVED)
- Multi-level explanation filtering (CONCISE, DETAILED, AUDIT_PROOF_TRACE)
- Safe serializable audit structure for Level 3
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional, Tuple, List, Union
from pointer_algorithms.proof_explanation.evidence import EvidenceRef, EvidenceKind


class ClaimType(Enum):
    PROBLEM_UNDERSTANDING = "PROBLEM_UNDERSTANDING"
    PROVEN_FACT = "PROVEN_FACT"
    DERIVATION = "DERIVATION"
    CONSTRAINT = "CONSTRAINT"
    CANDIDATE_ELIMINATION = "CANDIDATE_ELIMINATION"
    COMPONENT_SELECTION = "COMPONENT_SELECTION"
    COMPOSITION = "COMPOSITION"
    RESOURCE = "RESOURCE"
    PROOF_OBLIGATION = "PROOF_OBLIGATION"
    CORRECTNESS = "CORRECTNESS"
    FINAL_STATUS = "FINAL_STATUS"


class ExplanationLevel(Enum):
    CONCISE = "CONCISE"                      # Level 1
    DETAILED = "DETAILED"                    # Level 2
    AUDIT_PROOF_TRACE = "AUDIT_PROOF_TRACE"  # Level 3


class EpistemicStatus(Enum):
    PROVEN = "PROVEN"
    SUPPORTED = "SUPPORTED"
    HYPOTHETICAL = "HYPOTHETICAL"
    UNRESOLVED = "UNRESOLVED"


# ---------------------------------------------------------------------------
# Typed Claim Payloads
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ExplanationClaimBase:
    """Base class for all typed explanation claims."""
    claim_id: str
    claim_type: ClaimType
    text: str
    evidence_refs: Tuple[EvidenceRef, ...]
    source_layer: str
    epistemic_status: EpistemicStatus

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "claim_type": self.claim_type.value,
            "text": self.text,
            "evidence_refs": [e.to_dict() for e in self.evidence_refs],
            "source_layer": self.source_layer,
            "epistemic_status": self.epistemic_status.value
        }


@dataclass(frozen=True)
class ProblemUnderstandingClaim(ExplanationClaimBase):
    dimension: str = ""       # e.g. "STRUCTURE", "OPERATIONS", "BOUNDS", "QUERIES"
    key: str = ""             # e.g. "VERTEX_COUNT", "TOPOLOGY"
    canonical_value: str = "" # e.g. "5000", "TREE"

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "dimension": self.dimension,
            "key": self.key,
            "canonical_value": self.canonical_value
        })
        return d


@dataclass(frozen=True)
class ProvenFactClaim(ExplanationClaimBase):
    fact_name: str = ""
    tier: str = ""
    witness: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "fact_name": self.fact_name,
            "tier": self.tier,
            "witness": self.witness
        })
        return d


@dataclass(frozen=True)
class DerivationClaim(ExplanationClaimBase):
    derived_fact: str = ""
    rule_name: str = ""
    source_fact_ids: Tuple[str, ...] = ()
    witness: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "derived_fact": self.derived_fact,
            "rule_name": self.rule_name,
            "source_fact_ids": list(self.source_fact_ids),
            "witness": self.witness
        })
        return d


@dataclass(frozen=True)
class ConstraintClaim(ExplanationClaimBase):
    constraint_name: str = ""
    polarity: str = ""
    lattice_dimension: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "constraint_name": self.constraint_name,
            "polarity": self.polarity,
            "lattice_dimension": self.lattice_dimension
        })
        return d


@dataclass(frozen=True)
class CandidateEliminationClaim(ExplanationClaimBase):
    candidate_id: str = ""
    family: str = ""
    rejection_code: str = ""
    certificate_id: str = ""
    violated_constraint: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "candidate_id": self.candidate_id,
            "family": self.family,
            "rejection_code": self.rejection_code,
            "certificate_id": self.certificate_id,
            "violated_constraint": self.violated_constraint
        })
        return d


@dataclass(frozen=True)
class ComponentSelectionClaim(ExplanationClaimBase):
    component_id: str = ""
    role: str = ""
    supported_capabilities: Tuple[str, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "component_id": self.component_id,
            "role": self.role,
            "supported_capabilities": list(self.supported_capabilities)
        })
        return d


@dataclass(frozen=True)
class CompositionClaim(ExplanationClaimBase):
    step_index: int = 1
    producer_id: str = ""
    consumer_id: str = ""
    capability_name: str = ""
    contract_status: str = "SATISFIED"

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "step_index": self.step_index,
            "producer_id": self.producer_id,
            "consumer_id": self.consumer_id,
            "capability_name": self.capability_name,
            "contract_status": self.contract_status
        })
        return d


@dataclass(frozen=True)
class ResourceClaim(ExplanationClaimBase):
    metric: str = ""       # e.g., "TIME_COMPLEXITY", "SPACE_COMPLEXITY", "OPERATION_BUDGET"
    bound_value: str = ""  # e.g., "O(V log V)", "256 MB"
    verdict: str = "SATISFIED"

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "metric": self.metric,
            "bound_value": self.bound_value,
            "verdict": self.verdict
        })
        return d


@dataclass(frozen=True)
class ProofObligationClaim(ExplanationClaimBase):
    obligation_id: str = ""
    description: str = ""
    discharge_status: str = "DISCHARGED"
    witness: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "obligation_id": self.obligation_id,
            "description": self.description,
            "discharge_status": self.discharge_status,
            "witness": self.witness
        })
        return d


@dataclass(frozen=True)
class CorrectnessClaim(ExplanationClaimBase):
    invariant_name: str = ""
    argument: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "invariant_name": self.invariant_name,
            "argument": self.argument
        })
        return d


@dataclass(frozen=True)
class FinalStatusClaim(ExplanationClaimBase):
    outcome_state: str = ""
    plan_id: str = ""
    verification_artifact_id: str = ""
    integrity_seal: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "outcome_state": self.outcome_state,
            "plan_id": self.plan_id,
            "verification_artifact_id": self.verification_artifact_id,
            "integrity_seal": self.integrity_seal
        })
        return d


# Union of all typed claims
ExplanationClaim = Union[
    ProblemUnderstandingClaim,
    ProvenFactClaim,
    DerivationClaim,
    ConstraintClaim,
    CandidateEliminationClaim,
    ComponentSelectionClaim,
    CompositionClaim,
    ResourceClaim,
    ProofObligationClaim,
    CorrectnessClaim,
    FinalStatusClaim
]


# ---------------------------------------------------------------------------
# Section Models
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ProblemUnderstandingSection:
    title: str = "Problem Understanding"
    claims: Tuple[ProblemUnderstandingClaim, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        return {"title": self.title, "claims": [c.to_dict() for c in self.claims]}


@dataclass(frozen=True)
class ProvenFactsSection:
    title: str = "Proven Mathematical Facts"
    claims: Tuple[ProvenFactClaim, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        return {"title": self.title, "claims": [c.to_dict() for c in self.claims]}


@dataclass(frozen=True)
class DerivationSection:
    title: str = "Axiomatic Derivations & Invariants"
    claims: Tuple[DerivationClaim, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        return {"title": self.title, "claims": [c.to_dict() for c in self.claims]}


@dataclass(frozen=True)
class ConstraintSection:
    title: str = "Enriched Constraints"
    claims: Tuple[ConstraintClaim, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        return {"title": self.title, "claims": [c.to_dict() for c in self.claims]}


@dataclass(frozen=True)
class CandidateEliminationSection:
    title: str = "Candidate Elimination Analysis"
    claims: Tuple[CandidateEliminationClaim, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        return {"title": self.title, "claims": [c.to_dict() for c in self.claims]}


@dataclass(frozen=True)
class SelectionSection:
    title: str = "Selected Algorithm Components"
    claims: Tuple[ComponentSelectionClaim, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        return {"title": self.title, "claims": [c.to_dict() for c in self.claims]}


@dataclass(frozen=True)
class CompositionSection:
    title: str = "Composition & Capability Contracts"
    claims: Tuple[CompositionClaim, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        return {"title": self.title, "claims": [c.to_dict() for c in self.claims]}


@dataclass(frozen=True)
class ResourceSection:
    title: str = "Resource & Complexity Verification"
    claims: Tuple[ResourceClaim, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        return {"title": self.title, "claims": [c.to_dict() for c in self.claims]}


@dataclass(frozen=True)
class CorrectnessSection:
    title: str = "Correctness & Proof Obligations"
    claims: Tuple[Union[ProofObligationClaim, CorrectnessClaim], ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        return {"title": self.title, "claims": [c.to_dict() for c in self.claims]}


@dataclass(frozen=True)
class VerificationSummarySection:
    title: str = "Verification Summary"
    claims: Tuple[FinalStatusClaim, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        return {"title": self.title, "claims": [c.to_dict() for c in self.claims]}


# ---------------------------------------------------------------------------
# Root Document
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ExplanationDocument:
    """
    Root immutable Explanation Intermediate Representation (IR).
    Contains strictly evidence-backed claims and sections.
    """
    schema_version: str = "1.0.0"
    problem_id: str = "problem_default"
    outcome_state: str = "UNKNOWN"
    level: ExplanationLevel = ExplanationLevel.DETAILED

    understanding_section: ProblemUnderstandingSection = field(default_factory=ProblemUnderstandingSection)
    proven_facts_section: ProvenFactsSection = field(default_factory=ProvenFactsSection)
    derivation_section: DerivationSection = field(default_factory=DerivationSection)
    constraint_section: ConstraintSection = field(default_factory=ConstraintSection)
    elimination_section: CandidateEliminationSection = field(default_factory=CandidateEliminationSection)
    selection_section: SelectionSection = field(default_factory=SelectionSection)
    composition_section: CompositionSection = field(default_factory=CompositionSection)
    resource_section: ResourceSection = field(default_factory=ResourceSection)
    correctness_section: CorrectnessSection = field(default_factory=CorrectnessSection)
    summary_section: VerificationSummarySection = field(default_factory=VerificationSummarySection)

    def all_claims(self) -> Tuple[ExplanationClaim, ...]:
        claims: List[ExplanationClaim] = []
        claims.extend(self.understanding_section.claims)
        claims.extend(self.proven_facts_section.claims)
        claims.extend(self.derivation_section.claims)
        claims.extend(self.constraint_section.claims)
        claims.extend(self.elimination_section.claims)
        claims.extend(self.selection_section.claims)
        claims.extend(self.composition_section.claims)
        claims.extend(self.resource_section.claims)
        claims.extend(self.correctness_section.claims)
        claims.extend(self.summary_section.claims)
        return tuple(claims)

    def filter_level(self, target_level: ExplanationLevel) -> "ExplanationDocument":
        """Returns a new ExplanationDocument adapted for the target level."""
        if target_level == ExplanationLevel.CONCISE:
            # Concise: High-level overview (Understanding summary, key facts, summary)
            return ExplanationDocument(
                schema_version=self.schema_version,
                problem_id=self.problem_id,
                outcome_state=self.outcome_state,
                level=ExplanationLevel.CONCISE,
                understanding_section=self.understanding_section,
                proven_facts_section=ProvenFactsSection(
                    claims=tuple(c for c in self.proven_facts_section.claims if c.epistemic_status == EpistemicStatus.PROVEN)[:4]
                ),
                derivation_section=DerivationSection(claims=()),
                constraint_section=ConstraintSection(claims=()),
                elimination_section=CandidateEliminationSection(claims=()),
                selection_section=self.selection_section,
                composition_section=CompositionSection(claims=()),
                resource_section=ResourceSection(
                    claims=tuple(c for c in self.resource_section.claims if c.metric in ("TIME_COMPLEXITY", "SPACE_COMPLEXITY"))
                ),
                correctness_section=CorrectnessSection(claims=()),
                summary_section=self.summary_section
            )
        elif target_level == ExplanationLevel.DETAILED:
            return self
        else:
            # Level 3: Full audit trace
            return ExplanationDocument(
                schema_version=self.schema_version,
                problem_id=self.problem_id,
                outcome_state=self.outcome_state,
                level=ExplanationLevel.AUDIT_PROOF_TRACE,
                understanding_section=self.understanding_section,
                proven_facts_section=self.proven_facts_section,
                derivation_section=self.derivation_section,
                constraint_section=self.constraint_section,
                elimination_section=self.elimination_section,
                selection_section=self.selection_section,
                composition_section=self.composition_section,
                resource_section=self.resource_section,
                correctness_section=self.correctness_section,
                summary_section=self.summary_section
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "problem_id": self.problem_id,
            "outcome_state": self.outcome_state,
            "level": self.level.value,
            "understanding_section": self.understanding_section.to_dict(),
            "proven_facts_section": self.proven_facts_section.to_dict(),
            "derivation_section": self.derivation_section.to_dict(),
            "constraint_section": self.constraint_section.to_dict(),
            "elimination_section": self.elimination_section.to_dict(),
            "selection_section": self.selection_section.to_dict(),
            "composition_section": self.composition_section.to_dict(),
            "resource_section": self.resource_section.to_dict(),
            "correctness_section": self.correctness_section.to_dict(),
            "summary_section": self.summary_section.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExplanationDocument":
        def parse_evidence_refs(raw_refs: List[Dict[str, Any]]) -> Tuple[EvidenceRef, ...]:
            return tuple(EvidenceRef.from_dict(r) for r in raw_refs)

        # Helper to reconstruct claims
        def parse_claim(c_data: Dict[str, Any]) -> ExplanationClaim:
            ctype = ClaimType(c_data["claim_type"])
            refs = parse_evidence_refs(c_data.get("evidence_refs", []))
            base_args = {
                "claim_id": str(c_data["claim_id"]),
                "claim_type": ctype,
                "text": str(c_data["text"]),
                "evidence_refs": refs,
                "source_layer": str(c_data["source_layer"]),
                "epistemic_status": EpistemicStatus(c_data["epistemic_status"])
            }
            if ctype == ClaimType.PROBLEM_UNDERSTANDING:
                return ProblemUnderstandingClaim(
                    **base_args,
                    dimension=c_data.get("dimension", ""),
                    key=c_data.get("key", ""),
                    canonical_value=c_data.get("canonical_value", "")
                )
            elif ctype == ClaimType.PROVEN_FACT:
                return ProvenFactClaim(
                    **base_args,
                    fact_name=c_data.get("fact_name", ""),
                    tier=c_data.get("tier", ""),
                    witness=c_data.get("witness", "")
                )
            elif ctype == ClaimType.DERIVATION:
                return DerivationClaim(
                    **base_args,
                    derived_fact=c_data.get("derived_fact", ""),
                    rule_name=c_data.get("rule_name", ""),
                    source_fact_ids=tuple(c_data.get("source_fact_ids", ())),
                    witness=c_data.get("witness", "")
                )
            elif ctype == ClaimType.CONSTRAINT:
                return ConstraintClaim(
                    **base_args,
                    constraint_name=c_data.get("constraint_name", ""),
                    polarity=c_data.get("polarity", ""),
                    lattice_dimension=c_data.get("lattice_dimension", "")
                )
            elif ctype == ClaimType.CANDIDATE_ELIMINATION:
                return CandidateEliminationClaim(
                    **base_args,
                    candidate_id=c_data.get("candidate_id", ""),
                    family=c_data.get("family", ""),
                    rejection_code=c_data.get("rejection_code", ""),
                    certificate_id=c_data.get("certificate_id", ""),
                    violated_constraint=c_data.get("violated_constraint", "")
                )
            elif ctype == ClaimType.COMPONENT_SELECTION:
                return ComponentSelectionClaim(
                    **base_args,
                    component_id=c_data.get("component_id", ""),
                    role=c_data.get("role", ""),
                    supported_capabilities=tuple(c_data.get("supported_capabilities", ()))
                )
            elif ctype == ClaimType.COMPOSITION:
                return CompositionClaim(
                    **base_args,
                    step_index=c_data.get("step_index", 1),
                    producer_id=c_data.get("producer_id", ""),
                    consumer_id=c_data.get("consumer_id", ""),
                    capability_name=c_data.get("capability_name", ""),
                    contract_status=c_data.get("contract_status", "SATISFIED")
                )
            elif ctype == ClaimType.RESOURCE:
                return ResourceClaim(
                    **base_args,
                    metric=c_data.get("metric", ""),
                    bound_value=c_data.get("bound_value", ""),
                    verdict=c_data.get("verdict", "SATISFIED")
                )
            elif ctype == ClaimType.PROOF_OBLIGATION:
                return ProofObligationClaim(
                    **base_args,
                    obligation_id=c_data.get("obligation_id", ""),
                    description=c_data.get("description", ""),
                    discharge_status=c_data.get("discharge_status", "DISCHARGED"),
                    witness=c_data.get("witness", "")
                )
            elif ctype == ClaimType.CORRECTNESS:
                return CorrectnessClaim(
                    **base_args,
                    invariant_name=c_data.get("invariant_name", ""),
                    argument=c_data.get("argument", "")
                )
            elif ctype == ClaimType.FINAL_STATUS:
                return FinalStatusClaim(
                    **base_args,
                    outcome_state=c_data.get("outcome_state", ""),
                    plan_id=c_data.get("plan_id", ""),
                    verification_artifact_id=c_data.get("verification_artifact_id", ""),
                    integrity_seal=c_data.get("integrity_seal")
                )
            else:
                return ExplanationClaimBase(**base_args)

        sec_und = ProblemUnderstandingSection(
            title=data.get("understanding_section", {}).get("title", "Problem Understanding"),
            claims=tuple(parse_claim(c) for c in data.get("understanding_section", {}).get("claims", []))
        )
        sec_pf = ProvenFactsSection(
            title=data.get("proven_facts_section", {}).get("title", "Proven Mathematical Facts"),
            claims=tuple(parse_claim(c) for c in data.get("proven_facts_section", {}).get("claims", []))
        )
        sec_der = DerivationSection(
            title=data.get("derivation_section", {}).get("title", "Axiomatic Derivations & Invariants"),
            claims=tuple(parse_claim(c) for c in data.get("derivation_section", {}).get("claims", []))
        )
        sec_con = ConstraintSection(
            title=data.get("constraint_section", {}).get("title", "Enriched Constraints"),
            claims=tuple(parse_claim(c) for c in data.get("constraint_section", {}).get("claims", []))
        )
        sec_elim = CandidateEliminationSection(
            title=data.get("elimination_section", {}).get("title", "Candidate Elimination Analysis"),
            claims=tuple(parse_claim(c) for c in data.get("elimination_section", {}).get("claims", []))
        )
        sec_sel = SelectionSection(
            title=data.get("selection_section", {}).get("title", "Selected Algorithm Components"),
            claims=tuple(parse_claim(c) for c in data.get("selection_section", {}).get("claims", []))
        )
        sec_comp = CompositionSection(
            title=data.get("composition_section", {}).get("title", "Composition & Capability Contracts"),
            claims=tuple(parse_claim(c) for c in data.get("composition_section", {}).get("claims", []))
        )
        sec_res = ResourceSection(
            title=data.get("resource_section", {}).get("title", "Resource & Complexity Verification"),
            claims=tuple(parse_claim(c) for c in data.get("resource_section", {}).get("claims", []))
        )
        sec_corr = CorrectnessSection(
            title=data.get("correctness_section", {}).get("title", "Correctness & Proof Obligations"),
            claims=tuple(parse_claim(c) for c in data.get("correctness_section", {}).get("claims", []))
        )
        sec_sum = VerificationSummarySection(
            title=data.get("summary_section", {}).get("title", "Verification Summary"),
            claims=tuple(parse_claim(c) for c in data.get("summary_section", {}).get("claims", []))
        )

        return cls(
            schema_version=data.get("schema_version", "1.0.0"),
            problem_id=data.get("problem_id", "problem_default"),
            outcome_state=data.get("outcome_state", "UNKNOWN"),
            level=ExplanationLevel(data.get("level", "DETAILED")),
            understanding_section=sec_und,
            proven_facts_section=sec_pf,
            derivation_section=sec_der,
            constraint_section=sec_con,
            elimination_section=sec_elim,
            selection_section=sec_sel,
            composition_section=sec_comp,
            resource_section=sec_res,
            correctness_section=sec_corr,
            summary_section=sec_sum
        )
