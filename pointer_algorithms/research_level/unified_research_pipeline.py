"""
Phase 10 — unified_research_pipeline.py

Pillar V: Unified Research-Level Cognitive Pipeline Orchestrator.
Coordinates:
1. Problem Reduction (Pillar I)
2. Hypothesis Refutation (Pillar II)
3. Invariant Synthesis (Pillar III)
4. Parameterized Hardness Boundary (Pillar IV)
5. Proof Obligation Gate -> Phase 5 Planning
6. Complete End-to-End Cryptographic Provenance Chain
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence, Tuple

from .hardness_boundary import HardnessBoundaryEngine
from .hypothesis_refutation import InductiveRefutationEngine
from .invariant_synthesizer import InvariantSynthesizer
from .proof_obligation_gate import ProofObligationGate, ResearchCandidateArtifact
from .reduction_engine import ReductionEngine
from .research_types import (
    EpistemicStatus,
    HardnessCertificate,
    InvariantCertificate,
    ReductionCertificate,
    RefutationCertificate,
    ResourceFeasibilityCertificate,
)


@dataclass(frozen=True)
class ResearchProvenanceChain:
    """Complete cryptographic audit trail for Phase 10 research reasoning."""
    problem_hash: str
    requirements_hash: str
    reduction_certificate_hash: str
    hypothesis_refutation_hash: str
    invariant_certificate_hash: str
    hardness_certificate_hash: str
    master_provenance_digest: str


@dataclass(frozen=True)
class ResearchPipelineResult:
    problem_id: str
    admitted_to_planning: bool
    status: EpistemicStatus
    reduction_cert: Optional[ReductionCertificate] = None
    refutation_cert: Optional[RefutationCertificate] = None
    invariant_cert: Optional[InvariantCertificate] = None
    hardness_cert: Optional[HardnessCertificate] = None
    feasibility_cert: Optional[ResourceFeasibilityCertificate] = None
    provenance_chain: Optional[ResearchProvenanceChain] = None
    reason: str = ""


class UnifiedResearchPipeline:
    """
    Unified Orchestrator for Phase 10 Research-Level Reasoning.
    """

    @classmethod
    def execute(
        cls,
        *,
        problem_id: str,
        requirements_text: str,
        reduction_cert: Optional[ReductionCertificate] = None,
        refutation_cert: Optional[RefutationCertificate] = None,
        invariant_cert: Optional[InvariantCertificate] = None,
        hardness_cert: Optional[HardnessCertificate] = None,
        feasibility_cert: Optional[ResourceFeasibilityCertificate] = None,
    ) -> ResearchPipelineResult:
        prob_hash = hashlib.sha256(problem_id.encode()).hexdigest()
        req_hash = hashlib.sha256(requirements_text.encode()).hexdigest()

        red_hash = reduction_cert.fingerprint() if reduction_cert else ""
        hyp_hash = refutation_cert.certificate_id if refutation_cert else ""
        inv_hash = invariant_cert.certificate_id if invariant_cert else ""
        hard_hash = hardness_cert.certificate_id if hardness_cert else ""

        chain_data = {
            "problem_hash": prob_hash,
            "requirements_hash": req_hash,
            "red_hash": red_hash,
            "hyp_hash": hyp_hash,
            "inv_hash": inv_hash,
            "hard_hash": hard_hash,
        }
        master_digest = hashlib.sha256(json.dumps(chain_data, sort_keys=True).encode()).hexdigest()
        prov_chain = ResearchProvenanceChain(
            problem_hash=prob_hash,
            requirements_hash=req_hash,
            reduction_certificate_hash=red_hash,
            hypothesis_refutation_hash=hyp_hash,
            invariant_certificate_hash=inv_hash,
            hardness_certificate_hash=hard_hash,
            master_provenance_digest=master_digest,
        )

        # 1. If refutation certificate exists, fail closed (Law 2)
        if refutation_cert is not None:
            return ResearchPipelineResult(
                problem_id=problem_id,
                admitted_to_planning=False,
                status=EpistemicStatus.REFUTED,
                refutation_cert=refutation_cert,
                provenance_chain=prov_chain,
                reason="Hypothesis definitively refuted by counterexample witness.",
            )

        # 2. If parameter exceeds certified feasibility, fail closed (Law 7)
        if feasibility_cert is not None and not feasibility_cert.is_feasible:
            return ResearchPipelineResult(
                problem_id=problem_id,
                admitted_to_planning=False,
                status=EpistemicStatus.UNRESOLVED,
                feasibility_cert=feasibility_cert,
                provenance_chain=prov_chain,
                reason=f"Resource envelope exceeded: {feasibility_cert.status_label}.",
            )

        # 3. If reduction certificate is provided, evaluate via Proof Obligation Gate
        if reduction_cert is not None:
            ok, gate_msg, artifact = ProofObligationGate.evaluate_reduction_candidate(reduction_cert)
            if not ok:
                return ResearchPipelineResult(
                    problem_id=problem_id,
                    admitted_to_planning=False,
                    status=EpistemicStatus.UNRESOLVED,
                    reduction_cert=reduction_cert,
                    provenance_chain=prov_chain,
                    reason=gate_msg or "Failed Proof Obligation Gate",
                )

            return ResearchPipelineResult(
                problem_id=problem_id,
                admitted_to_planning=True,
                status=EpistemicStatus.PROVEN,
                reduction_cert=reduction_cert,
                provenance_chain=prov_chain,
                reason="Reduction candidate verified across Gates A-C and admitted to Phase 5 planning.",
            )

        # 4. If invariant certificate is provided and verified
        if invariant_cert is not None and invariant_cert.is_valid():
            return ResearchPipelineResult(
                problem_id=problem_id,
                admitted_to_planning=True,
                status=EpistemicStatus.PROVEN,
                invariant_cert=invariant_cert,
                provenance_chain=prov_chain,
                reason="Discrete invariant verified and admitted to Phase 5 planning.",
            )

        # Default fallback: Unresolved evidence fails closed (Law 10)
        return ResearchPipelineResult(
            problem_id=problem_id,
            admitted_to_planning=False,
            status=EpistemicStatus.UNRESOLVED,
            provenance_chain=prov_chain,
            reason="Unresolved research evidence; fails closed with zero code generation.",
        )
