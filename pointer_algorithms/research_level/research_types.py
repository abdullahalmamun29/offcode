"""
Phase 10 — research_types.py

Structured proof objects, certificates, and the 5-state epistemic model
for research-level algorithmic reasoning. All types are deeply frozen.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional, Sequence, Tuple


# ---------------------------------------------------------------------------
# 5-State Epistemic Model
# ---------------------------------------------------------------------------

class EpistemicStatus(str, Enum):
    """
    Discrete 5-State Epistemic Model:
    PROVEN: Analytically discharged proof / mechanically verified theorem.
    REFUTED: Concrete counterexample witness proven.
    SUPPORTED: Exhaustive search complete within declared FiniteSearchEnvelope.
    HYPOTHETICAL: Initial conjecture formulated.
    UNRESOLVED: Incomplete evidence, oracle inconsistency, or unverified gate.
    """
    PROVEN = "PROVEN"
    REFUTED = "REFUTED"
    SUPPORTED = "SUPPORTED"
    HYPOTHETICAL = "HYPOTHETICAL"
    UNRESOLVED = "UNRESOLVED"


# ---------------------------------------------------------------------------
# Reduction Types & Enumerations
# ---------------------------------------------------------------------------

class ReductionType(str, Enum):
    PROJECT_SELECTION_TO_MIN_CUT = "PROJECT_SELECTION_TO_MIN_CUT"
    BIPARTITE_MATCHING_TO_VERTEX_COVER = "BIPARTITE_MATCHING_TO_VERTEX_COVER"
    VERTEX_COVER_TO_INDEPENDENT_SET = "VERTEX_COVER_TO_INDEPENDENT_SET"
    DIFFERENCE_CONSTRAINTS_TO_SHORTEST_PATH = "DIFFERENCE_CONSTRAINTS_TO_SHORTEST_PATH"
    PLANAR_DUAL_ROUTING = "PLANAR_DUAL_ROUTING"
    COMPLEMENT_INCLUSION_EXCLUSION = "COMPLEMENT_INCLUSION_EXCLUSION"
    COMPOSED_REDUCTION = "COMPOSED_REDUCTION"
    HARDNESS_REDUCTION_REVERSE = "HARDNESS_REDUCTION_REVERSE"


class HypothesisSchema(str, Enum):
    GREEDY_BY_KEY = "GREEDY_BY_KEY"
    MONOTONICITY = "MONOTONICITY"
    EXCHANGE_ARGUMENT = "EXCHANGE_ARGUMENT"
    STATE_DIMENSION_REMOVAL = "STATE_DIMENSION_REMOVAL"
    LOCAL_OPTIMALITY = "LOCAL_OPTIMALITY"
    PARITY_STRUCTURE = "PARITY_STRUCTURE"
    POTENTIAL_DECREASE = "POTENTIAL_DECREASE"


class InvariantClass(str, Enum):
    LINEAR_COMBINATION = "LINEAR_COMBINATION"
    MODULAR_CONSERVATION = "MODULAR_CONSERVATION"
    PARITY_INVARIANT = "PARITY_INVARIANT"
    BOUNDED_POTENTIAL = "BOUNDED_POTENTIAL"
    XOR_SUM_GRUNDY = "XOR_SUM_GRUNDY"


# ---------------------------------------------------------------------------
# Structured Proof Objects (Replacing Free-Form Prose)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PredicateEvidence:
    """Instance-level predicate evidence for reduction applicability."""
    predicate_name: str
    satisfied: bool
    witness_data: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ApplicabilityProof:
    """Proof that instance satisfies all preconditions for a reduction."""
    predicates: Tuple[PredicateEvidence, ...]
    discharged: bool

    def validate(self) -> bool:
        return self.discharged and all(p.satisfied for p in self.predicates)


@dataclass(frozen=True)
class ProofObligationItem:
    """Discrete mathematical obligation ensuring semantic preservation."""
    obligation_id: str
    property_name: str
    discharged: bool
    evidence_details: str = ""


@dataclass(frozen=True)
class SemanticPreservationProof:
    """Proof that objective value and solution feasibility are preserved."""
    obligations: Tuple[ProofObligationItem, ...]
    discharged: bool

    def validate(self) -> bool:
        return self.discharged and all(o.discharged for o in self.obligations)


@dataclass(frozen=True)
class ComplexityBound:
    asymptotic_formula: str
    parameter_dependencies: Tuple[str, ...]
    is_polynomial: bool
    budget_satisfied: bool


@dataclass(frozen=True)
class ComplexityProof:
    """Guarantees forward, solver, and backward complexity satisfy budget."""
    forward_bound: ComplexityBound
    solver_bound: ComplexityBound
    backward_bound: ComplexityBound
    total_bound: ComplexityBound
    discharged: bool

    def validate(self) -> bool:
        return (
            self.discharged
            and self.forward_bound.budget_satisfied
            and self.solver_bound.budget_satisfied
            and self.backward_bound.budget_satisfied
            and self.total_bound.budget_satisfied
        )


# ---------------------------------------------------------------------------
# Pillar I: Certified Reduction Certificate
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ReductionCertificate:
    """
    Immutable certificate recording a formally proven problem reduction P <=_m Q.
    Authority is derived strictly from structured proof objects.
    """
    certificate_id: str
    source_problem_id: str
    target_family_id: str
    reduction_type: ReductionType

    applicability_proof: ApplicabilityProof
    semantic_proof: SemanticPreservationProof
    complexity_proof: ComplexityProof

    forward_transform_name: str
    backward_solution_map_name: str
    domain_assumptions: Tuple[str, ...]
    theorem_id: str
    theorem_version: str
    problem_hash: str
    requirements_hash: str
    status: EpistemicStatus

    def is_valid(self) -> bool:
        return (
            self.status == EpistemicStatus.PROVEN
            and self.applicability_proof.validate()
            and self.semantic_proof.validate()
            and self.complexity_proof.validate()
        )

    def fingerprint(self) -> str:
        data = {
            "certificate_id": self.certificate_id,
            "source_problem_id": self.source_problem_id,
            "target_family_id": self.target_family_id,
            "reduction_type": self.reduction_type.value,
            "problem_hash": self.problem_hash,
            "requirements_hash": self.requirements_hash,
            "theorem_id": self.theorem_id,
            "status": self.status.value,
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


# ---------------------------------------------------------------------------
# Pillar II: Finite Search Envelope & Refutation Certificates
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FiniteSearchEnvelope:
    """Exact specification of the bounded finite state space explored."""
    domain_type: str                         # "ARRAY", "GRAPH", "TREE", "GRID", "PARTITION"
    size_bound: int                          # Maximum N explored
    value_bound: int                         # Values bounded in [-V, V]
    structural_constraints: Tuple[str, ...]  # ("CONNECTED", "SIMPLE", etc.)
    max_states_budget: int                   # Bound on evaluated instances
    timeout_ms_budget: int                   # Execution time budget in ms
    symmetry_reduction: bool = True

    def fingerprint(self) -> str:
        data = {
            "domain_type": self.domain_type,
            "size_bound": self.size_bound,
            "value_bound": self.value_bound,
            "constraints": list(self.structural_constraints),
            "max_states": self.max_states_budget,
            "symmetry": self.symmetry_reduction,
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


@dataclass(frozen=True)
class RefutationCertificate:
    """
    Emitted when an algorithmic hypothesis is definitively falsified by a concrete witness.
    Law 2: A single machine-verifiable counterexample is sufficient for definitive rejection.
    """
    certificate_id: str
    hypothesis_id: str
    schema: HypothesisSchema
    counterexample_witness: Mapping[str, Any]
    hypothesis_output: str
    oracle_output: str
    envelope_fingerprint: str
    status: EpistemicStatus = EpistemicStatus.REFUTED


@dataclass(frozen=True)
class CorroborationCertificate:
    """
    Emitted when exhaustive search across FiniteSearchEnvelope finds zero counterexamples.
    Law 3: Finite exhaustive testing corroborates strictly within envelope (SUPPORTED).
    Law 4: Cannot be converted into PROVEN.
    """
    certificate_id: str
    hypothesis_id: str
    schema: HypothesisSchema
    envelope_fingerprint: str
    states_evaluated: int
    exhaustive_within_envelope: bool
    status: EpistemicStatus = EpistemicStatus.SUPPORTED


# ---------------------------------------------------------------------------
# Pillar III: Invariant & Monovariant Certificates
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class InvariantCertificate:
    """
    Certified discrete invariant or well-founded potential function.
    """
    certificate_id: str
    invariant_class: InvariantClass
    expression_representation: str
    codomain: str                        # "NATURAL_NUMBERS", "INTEGERS_MOD_K", "NIM_VALUES"
    well_founded_proven: bool
    strict_decrease_proven: bool
    modular_conservation_proven: bool
    termination_bound_steps: Optional[int]
    status: EpistemicStatus = EpistemicStatus.PROVEN

    def is_valid(self) -> bool:
        if self.invariant_class == InvariantClass.BOUNDED_POTENTIAL:
            return self.well_founded_proven and self.strict_decrease_proven
        if self.invariant_class == InvariantClass.MODULAR_CONSERVATION:
            return self.modular_conservation_proven
        if self.invariant_class == InvariantClass.XOR_SUM_GRUNDY:
            return self.well_founded_proven
        return True


# ---------------------------------------------------------------------------
# Pillar IV: Hardness & Parameter Feasibility Certificates
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class HardnessCertificate:
    """
    Certified hardness reduction H <=_p P from a known NP-hard core.
    Law 6: NP-hardness requires certified reverse polynomial reduction.
    """
    certificate_id: str
    user_problem_id: str
    known_hard_core_id: str               # "3SAT", "VERTEX_COVER", "TSP", "SUBSET_SUM"
    reduction_proof: ReductionCertificate
    is_np_hard: bool
    status: EpistemicStatus = EpistemicStatus.PROVEN


@dataclass(frozen=True)
class ResourceFeasibilityCertificate:
    """
    Certifies whether an algorithm is within computational budget.
    Law 7: Budget exceeded is NOT problem unsatisfiability.
    """
    certificate_id: str
    algorithm_name: str
    parameter_name: str
    parameter_value: int
    complexity_formula: str
    estimated_operations: int
    max_operations_budget: int
    is_feasible: bool
    status_label: str  # "FEASIBLE" or "PARAMETER_EXCEEDS_CERTIFIED_FEASIBILITY"
