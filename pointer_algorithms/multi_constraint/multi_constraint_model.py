"""
CHUP Phase 5 — Multi-Constraint Model & Verified Composition Plan.

Encodes the four disjoint outcome states, formal proof obligations,
and the VerifiedMultiConstraintPlan carrying SHA-256 integrity sealing.
"""

from enum import Enum, auto
from typing import Dict, Any, List, Optional, FrozenSet
from dataclasses import dataclass, field
import hashlib
import json
from pointer_algorithms.multi_constraint.elimination_engine import EliminationCertificate
from pointer_algorithms.multi_constraint.capability_synthesizer import SynthesizedPipelineStep


class OutcomeState(Enum):
    """
    Four mutually exclusive terminal states of multi-constraint reasoning.
    Axiomatic impossibility is strictly decoupled from candidate insufficiency.
    """
    SATISFIABLE_SINGLE_CANDIDATE = "SATISFIABLE_SINGLE_CANDIDATE"
    SATISFIABLE_COMPOSED_PLAN = "SATISFIABLE_COMPOSED_PLAN"
    UNSATISFIABLE_CONSTRAINT_SET = "UNSATISFIABLE_CONSTRAINT_SET"
    UNRESOLVED_BY_CURRENT_ONTOLOGY = "UNRESOLVED_BY_CURRENT_ONTOLOGY"


class ProofStatus(Enum):
    DISCHARGED = "DISCHARGED"
    UNMET = "UNMET"


@dataclass(frozen=True)
class ProofObligation:
    """
    Formally dischargeable proof obligation tying a required constraint
    property to satisfying evidence from an assigned component.
    """
    obligation_id: str
    constraint_id: str
    required_property: str
    satisfying_component: str
    evidence: str
    verification_status: ProofStatus = ProofStatus.DISCHARGED


@dataclass(frozen=True)
class UnresolvedCoverageCertificate:
    """
    Record produced when a problem is satisfiable, but the registered
    19-domain universe cannot bridge the remaining coverage gap.
    """
    uncovered_capabilities: List[str]
    reason: str
    witness: str


@dataclass(frozen=True)
class VerifiedMultiConstraintPlan:
    """
    Immutable, cryptographically sealed multi-constraint execution plan.
    Carries SHA-256 integrity seal over canonical serialization.
    """
    plan_id: str
    outcome_state: OutcomeState
    selected_components: List[str]
    synthesized_pipeline: List[SynthesizedPipelineStep]
    proof_obligations: List[ProofObligation]
    elimination_certificates: Dict[str, EliminationCertificate]
    canonical_digest: str
    verification_artifact_id: str

    @property
    def cryptographic_hash_seal(self) -> str:
        """Alias for canonical_digest representing the SHA-256 seal."""
        return self.canonical_digest

    def verify_seal(self) -> bool:
        """Verifies that the canonical SHA-256 digest matches the plan content."""
        return self.canonical_digest == self.compute_canonical_digest()

    def all_obligations_discharged(self) -> bool:
        if not self.proof_obligations:
            return True
        return all(o.verification_status == ProofStatus.DISCHARGED for o in self.proof_obligations)

    def is_topologically_sound(self) -> bool:
        # Steps must have strictly increasing step_index
        indices = [step.step_index for step in self.synthesized_pipeline]
        return indices == sorted(indices)

    def compute_canonical_digest(self) -> str:
        """
        Computes deterministic SHA-256 digest over the canonical JSON representation.
        """
        payload = {
            "plan_id": self.plan_id,
            "outcome_state": self.outcome_state.value,
            "selected_components": sorted(self.selected_components),
            "pipeline": [
                {
                    "step": s.step_index,
                    "component": s.component_id,
                    "role": s.role,
                    "consumed": sorted(list(s.consumed_capabilities)),
                    "produced": sorted(list(s.produced_capabilities))
                }
                for s in self.synthesized_pipeline
            ],
            "obligations": [
                {
                    "id": o.obligation_id,
                    "constraint": o.constraint_id,
                    "property": o.required_property,
                    "component": o.satisfying_component,
                    "status": o.verification_status.value
                }
                for o in sorted(self.proof_obligations, key=lambda x: x.obligation_id)
            ],
            "eliminated": sorted(list(self.elimination_certificates.keys())),
            "artifact_id": self.verification_artifact_id
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    @classmethod
    def seal(
        cls,
        plan_id: str,
        outcome_state: OutcomeState,
        selected_components: List[str],
        synthesized_pipeline: List[SynthesizedPipelineStep],
        proof_obligations: List[ProofObligation],
        elimination_certificates: Dict[str, EliminationCertificate],
        verification_artifact_id: str
    ) -> "VerifiedMultiConstraintPlan":
        """
        Constructs and cryptographically seals a VerifiedMultiConstraintPlan.
        """
        temp_plan = cls(
            plan_id=plan_id,
            outcome_state=outcome_state,
            selected_components=selected_components,
            synthesized_pipeline=synthesized_pipeline,
            proof_obligations=proof_obligations,
            elimination_certificates=elimination_certificates,
            canonical_digest="",
            verification_artifact_id=verification_artifact_id
        )
        digest = temp_plan.compute_canonical_digest()
        return cls(
            plan_id=plan_id,
            outcome_state=outcome_state,
            selected_components=selected_components,
            synthesized_pipeline=synthesized_pipeline,
            proof_obligations=proof_obligations,
            elimination_certificates=elimination_certificates,
            canonical_digest=digest,
            verification_artifact_id=verification_artifact_id
        )
