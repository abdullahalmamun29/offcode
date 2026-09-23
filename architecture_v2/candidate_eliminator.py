"""
Generic Hard Candidate Elimination for Architecture V2.

Evaluates candidates against the canonical ProblemModel using hard constraints:
1. Selection & Cardinality compatibility
2. Operation coverage
3. Resource / Complexity feasibility
4. Output compatibility
5. Structural compatibility
6. Proof obligation feasibility

STRICT INVARIANT:
Candidate prior or confidence NEVER overrides a hard contradiction.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Set
from architecture_v2.semantic_model import (
    ProblemModel, SelectionKind, RequiredOperation, RelationKind,
    OperatorKind, StructuralProperty, ObjectiveKind
)
from architecture_v2.capability_registry import AlgorithmCapability, CapabilityRegistry


class CandidateStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    UNPROVEN = "UNPROVEN"
    UNSUPPORTED = "UNSUPPORTED"


@dataclass
class CandidateDecision:
    candidate_name: str
    status: CandidateStatus
    reasons: List[str] = field(default_factory=list)
    satisfied_requirements: List[str] = field(default_factory=list)
    missing_requirements: List[str] = field(default_factory=list)
    violated_constraints: List[str] = field(default_factory=list)
    proof_status: Dict[str, str] = field(default_factory=dict)
    backend: str = ""

    def __repr__(self) -> str:
        return f"CandidateDecision({self.candidate_name}: {self.status.value}, reasons={self.reasons})"


class CandidateEliminatorV2:
    """
    Evaluates candidate algorithm capabilities against a canonical ProblemModel.
    """

    @classmethod
    def evaluate(cls, capability: AlgorithmCapability, model: ProblemModel) -> CandidateDecision:
        reasons: List[str] = []
        satisfied: List[str] = []
        missing: List[str] = []
        violated: List[str] = []
        proofs: Dict[str, str] = {}

        # ── 1. Selection Model & Cardinality Check ──
        if capability.requires_selection is not None:
            if model.selection.kind != SelectionKind.UNKNOWN and model.selection.kind != capability.requires_selection:
                reasons.append("SELECTION_MODEL_MISMATCH")
                violated.append(f"Problem requires {model.selection.kind.value} but candidate requires {capability.requires_selection.value}")
                if model.selection.kind == SelectionKind.FIXED_CARDINALITY and capability.requires_selection == SelectionKind.ARBITRARY_SUBSET:
                    reasons.append("CARDINALITY_MISMATCH")
                    violated.append(f"Problem requires fixed cardinality {model.selection.cardinality} but candidate assumes arbitrary cardinality")
            else:
                satisfied.append("selection_model_compatible")

        if capability.requires_cardinality is not None:
            if model.selection.cardinality is not None and model.selection.cardinality != capability.requires_cardinality:
                reasons.append("CARDINALITY_MISMATCH")
                violated.append(f"Problem requires cardinality {model.selection.cardinality} but candidate requires {capability.requires_cardinality}")
            elif model.selection.cardinality == capability.requires_cardinality:
                satisfied.append(f"cardinality_{capability.requires_cardinality}_satisfied")

        # ── 2. Relation Compatibility Check ──
        for req_rel in capability.requires_relations:
            if any(r.kind == req_rel for r in model.relations):
                satisfied.append(f"relation_{req_rel.value}_satisfied")
            else:
                missing.append(f"relation_{req_rel.value}")
                reasons.append("RELATION_MISMATCH")

        for req_op in capability.requires_operators:
            if any(r.operator == req_op for r in model.relations):
                satisfied.append(f"operator_{req_op.value}_satisfied")
            else:
                missing.append(f"operator_{req_op.value}")
                reasons.append("OPERATOR_MISMATCH")

        # ── 3. Operation Coverage Check ──
        for req_operation in capability.requires_operations:
            if req_operation in model.operations:
                satisfied.append(f"operation_{req_operation.value}_present")
            else:
                missing.append(f"operation_{req_operation.value}")

        # ── 4. Structural Property Check ──
        for req_prop in capability.requires_properties:
            if req_prop in model.structural_properties:
                satisfied.append(f"property_{req_prop.value}_present")
            else:
                # If required property is not yet established
                missing.append(f"property_{req_prop.value}")
                reasons.append(f"MISSING_STRUCTURAL_PROPERTY_{req_prop.value}")

        # ── 5. Output Compatibility Check ──
        if model.output_spec.get("type") == "ORIGINAL_INDICES":
            if "ORIGINAL_INDICES" not in capability.output_contract:
                reasons.append("OUTPUT_MISMATCH")
                violated.append("Problem requires original indices but candidate output contract cannot preserve original indices")
            else:
                satisfied.append("output_original_indices_supported")

        if model.output_spec.get("type") == "COUNT" or model.objective.kind == ObjectiveKind.COUNT:
            if capability.output_contract and "COUNT" not in capability.output_contract:
                reasons.append("OUTPUT_MISMATCH")
                violated.append(f"Problem requires COUNT output but candidate output contract {capability.output_contract} does not produce COUNT")
            else:
                satisfied.append("output_count_supported")

        if model.output_spec.get("type") == "MAX_CARDINALITY" or model.objective.kind == ObjectiveKind.MAXIMIZE_CARDINALITY:
            if capability.output_contract and not any(k in capability.output_contract for k in ("MAX_CARDINALITY", "COUNT")):
                reasons.append("OUTPUT_MISMATCH")
                violated.append(f"Problem requires MAX_CARDINALITY output but candidate output contract {capability.output_contract} does not produce it")
            else:
                satisfied.append("output_max_cardinality_supported")

        if model.output_spec.get("type") == "BOOLEAN" or model.objective.kind == ObjectiveKind.DECIDE:
            if capability.output_contract and "BOOLEAN" not in capability.output_contract:
                reasons.append("OUTPUT_MISMATCH")
                violated.append(f"Problem requires BOOLEAN decision output but candidate output contract {capability.output_contract} does not produce BOOLEAN")
            else:
                satisfied.append("output_boolean_supported")

        # ── 6. Resource / Complexity Feasibility Check ──
        if "W" in capability.complexity_space or "target" in capability.complexity_space:
            target_val = model.constraints.target_value
            if target_val is not None:
                # If target is huge, e.g. 10^9, DP requiring O(W) or O(target) space is impossible
                estimated_bytes = target_val * 4  # 4 bytes per integer
                estimated_mb = estimated_bytes / (1024 * 1024)
                if model.constraints.is_memory_exceeded(estimated_mb):
                    reasons.append("MEMORY_INFEASIBLE")
                    violated.append(f"State space O({target_val}) requires ~{estimated_mb:.1f} MB, exceeding {model.constraints.memory_limit_mb} MB limit")

        if "N^2" in capability.complexity_time:
            n_val = model.constraints.n
            if n_val is not None:
                ops = n_val * n_val
                max_ops = 10**8 * (model.constraints.time_limit_ms / 1000.0)
                if ops > max_ops:
                    reasons.append("TIME_INFEASIBLE")
                    violated.append(f"Time complexity O(N^2) requires {ops} operations, exceeding {max_ops:.0f} operation limit for {model.constraints.time_limit_ms}ms")

        # ── 7. Proof Obligations ──
        for obl in capability.proof_obligations:
            if obl == "selection_cardinality_is_2":
                proofs[obl] = "PROVEN" if (model.selection.cardinality == 2) else "UNPROVEN"
            elif obl == "relation_is_sum":
                proofs[obl] = "PROVEN" if any(r.kind == RelationKind.SUM for r in model.relations) else "UNPROVEN"
            elif obl == "residual_target_correctness":
                proofs[obl] = "PROVEN" if any(r.kind == RelationKind.SUM for r in model.relations) else "UNPROVEN"
            elif obl == "sorting_permitted":
                if model.selection.kind == SelectionKind.CONTIGUOUS_SEGMENT:
                    proofs[obl] = "UNPROVEN"
                else:
                    proofs[obl] = "PROVEN"
            elif obl == "original_indices_preserved":
                proofs[obl] = "PROVEN" if ("ORIGINAL_INDICES" in capability.output_contract) else "UNPROVEN"
            elif obl == "anchor_index_preserved":
                proofs[obl] = "PROVEN" if ("ORIGINAL_INDICES" in capability.output_contract) else "UNPROVEN"
            elif obl == "residual_indices_preserved":
                proofs[obl] = "PROVEN" if ("ORIGINAL_INDICES" in capability.output_contract) else "UNPROVEN"
            elif obl == "anchor_excluded_from_residual_search":
                proofs[obl] = "PROVEN" if (model.selection.distinct_positions or StructuralProperty.PAIRWISE_DISTINCT_SELECTION in model.structural_properties) else "UNPROVEN"
            elif obl == "residual_pair_indices_distinct":
                proofs[obl] = "PROVEN" if (model.selection.distinct_positions or StructuralProperty.PAIRWISE_DISTINCT_SELECTION in model.structural_properties) else "UNPROVEN"
            elif obl == "pairwise_indices_distinct":
                proofs[obl] = "PROVEN" if (model.selection.distinct_positions or StructuralProperty.PAIRWISE_DISTINCT_SELECTION in model.structural_properties) else "UNPROVEN"
            elif obl == "complexity_feasibility":
                proofs[obl] = "PROVEN" if ("TIME_INFEASIBLE" not in reasons and "MEMORY_INFEASIBLE" not in reasons) else "UNPROVEN"
            elif obl == "pointer_elimination_sound":
                proofs[obl] = "PROVEN" if any(r.kind == RelationKind.SUM for r in model.relations) else "UNPROVEN"
            elif obl == "search_terminates":
                proofs[obl] = "PROVEN"
            elif obl == "complement_lookup_exact":
                proofs[obl] = "PROVEN" if any(r.kind == RelationKind.SUM for r in model.relations) else "UNPROVEN"
            elif obl == "arbitrary_subset_selection":
                proofs[obl] = "PROVEN" if (model.selection.kind == SelectionKind.ARBITRARY_SUBSET) else "UNPROVEN"
            elif obl == "bellman_optimality":
                proofs[obl] = "PROVEN" if (StructuralProperty.OPTIMAL_SUBSTRUCTURE in model.structural_properties) else "UNPROVEN"
            elif obl in ("capacity_feasible", "target_feasible"):
                target_val = model.constraints.target_value
                if target_val is not None:
                    est_mb = (target_val * 4) / (1024 * 1024)
                    proofs[obl] = "PROVEN" if not model.constraints.is_memory_exceeded(est_mb) else "UNPROVEN"
                else:
                    proofs[obl] = "UNPROVEN"
            elif obl == "ordered_comparator_valid":
                proofs[obl] = "PROVEN" if (StructuralProperty.ORDERED_STATE in model.structural_properties) else "UNPROVEN"
            elif obl == "dynamic_balanced_tree_invariants":
                is_dyn_ord = (
                    StructuralProperty.DYNAMIC_STATE in model.structural_properties and
                    StructuralProperty.ORDERED_STATE in model.structural_properties
                )
                proofs[obl] = "PROVEN" if is_dyn_ord else "UNPROVEN"
            elif obl == "bitwise_prefix_greedy_choice":
                proofs[obl] = "PROVEN" if any(r.operator == OperatorKind.XOR for r in model.relations) else "UNPROVEN"
            elif obl == "fixed_bitwidth_representation":
                proofs[obl] = "PROVEN" if any(r.operator == OperatorKind.XOR for r in model.relations) else "UNPROVEN"
            elif obl == "monotonic_predicate":
                proofs[obl] = "PROVEN" if (StructuralProperty.MONOTONICITY in model.structural_properties) else "UNPROVEN"
            elif obl == "search_interval_contains_answer":
                proofs[obl] = "PROVEN" if (StructuralProperty.ORDERED_STATE in model.structural_properties) else "UNPROVEN"
            elif obl == "termination_without_infinite_loop":
                proofs[obl] = "PROVEN"
            elif obl == "equivalence_relation_partition":
                proofs[obl] = "PROVEN" if (StructuralProperty.CONNECTIVITY in model.structural_properties) else "UNPROVEN"
            elif obl == "acyclic_component_merges":
                proofs[obl] = "PROVEN" if (StructuralProperty.CONNECTIVITY in model.structural_properties) else "UNPROVEN"
            elif obl == "contiguous_range_preservation":
                proofs[obl] = "PROVEN" if (model.selection.kind == SelectionKind.CONTIGUOUS_SEGMENT) else "UNPROVEN"
            elif obl == "monotone_expansion_and_shrinking":
                proofs[obl] = "PROVEN" if (StructuralProperty.CONTIGUOUS_SELECTION in model.structural_properties) else "UNPROVEN"
            elif obl == "extremal_pairing_optimal":
                proofs[obl] = "PROVEN" if (StructuralProperty.EXTREMAL_PAIRING in model.structural_properties) else "UNPROVEN"
            elif obl == "opposite_pointers_exhaust_search":
                proofs[obl] = "PROVEN" if (StructuralProperty.ORDERED_STATE in model.structural_properties) else "UNPROVEN"
            elif obl == "capacity_feasibility_checked":
                proofs[obl] = "PROVEN" if any(r.kind == RelationKind.LESS_EQUAL for r in model.relations) else "UNPROVEN"
            elif obl == "all_items_covered":
                proofs[obl] = "PROVEN" if (model.selection.kind == SelectionKind.ALL_ELEMENTS or StructuralProperty.ALL_ELEMENTS_REQUIRED in model.structural_properties) else "UNPROVEN"
            elif obl == "two_distinct_collections":
                proofs[obl] = "PROVEN" if (
                    StructuralProperty.TWO_SEQUENCE_MATCHING in model.structural_properties or
                    model.has_fact("collection.two_distinct_collections") or
                    len(model.collections) >= 2
                ) else "UNPROVEN"
            elif obl == "one_to_one_matching":
                proofs[obl] = "PROVEN" if (
                    StructuralProperty.ONE_TO_ONE_MATCHING in model.structural_properties or
                    model.has_fact("matching.one_to_one")
                ) else "UNPROVEN"
            elif obl == "maximize_match_count":
                proofs[obl] = "PROVEN" if (
                    StructuralProperty.MAX_CARDINALITY_MATCHING in model.structural_properties or
                    model.has_fact("objective.maximize_matches") or
                    (model.objective.kind == ObjectiveKind.MAXIMIZE and model.objective.target_property in ("matches", "general"))
                ) else "UNPROVEN"
            elif obl == "sortable_numeric_domains":
                proofs[obl] = "PROVEN" if (
                    StructuralProperty.ORDERED_STATE in model.structural_properties
                ) else "UNPROVEN"
            elif obl == "interval_compatibility":
                proofs[obl] = "PROVEN" if any(r.kind == RelationKind.INTERVAL_TOLERANCE for r in model.relations) else "UNPROVEN"
            elif obl == "monotone_compatibility":
                proofs[obl] = "PROVEN" if (
                    StructuralProperty.MONOTONE_COMPATIBILITY in model.structural_properties
                ) else "UNPROVEN"
            elif obl == "discard_too_small_is_safe":
                proofs[obl] = "PROVEN" if (
                    StructuralProperty.ORDERED_STATE in model.structural_properties and
                    StructuralProperty.MONOTONE_COMPATIBILITY in model.structural_properties
                ) else "UNPROVEN"
            elif obl == "discard_too_large_is_safe":
                proofs[obl] = "PROVEN" if (
                    StructuralProperty.ORDERED_STATE in model.structural_properties and
                    StructuralProperty.MONOTONE_COMPATIBILITY in model.structural_properties
                ) else "UNPROVEN"
            elif obl == "feasible_pair_match_is_safe":
                proofs[obl] = "PROVEN" if (
                    StructuralProperty.LOCAL_CHOICE in model.structural_properties and
                    StructuralProperty.MONOTONE_COMPATIBILITY in model.structural_properties
                ) else "UNPROVEN"
            elif obl == "both_pointers_monotonically_advance":
                proofs[obl] = "PROVEN" if (
                    StructuralProperty.ORDERED_STATE in model.structural_properties
                ) else "UNPROVEN"
            elif obl == "all_remaining_elements_eventually_processed":
                proofs[obl] = "PROVEN"
            elif obl == "contiguous_range_selection":
                proofs[obl] = "PROVEN" if (
                    model.selection.kind == SelectionKind.CONTIGUOUS_SEGMENT or
                    StructuralProperty.CONTIGUOUS_SELECTION in model.structural_properties
                ) else "UNPROVEN"
            elif obl == "strictly_positive_elements":
                proofs[obl] = "PROVEN" if (
                    model.constraints.strictly_positive is True or
                    (model.has_fact("domain.strictly_positive") and model.get_fact("domain.strictly_positive").value is True) or
                    (model.has_fact("domain.value_positivity") and model.get_fact("domain.value_positivity").value == "POSITIVE")
                ) else "UNPROVEN"
            elif obl == "range_sum_equals_target":
                proofs[obl] = "PROVEN" if (
                    any(r.kind in (RelationKind.EQUALITY, RelationKind.SUM) for r in model.relations) and
                    (any(r.operator == OperatorKind.SUM for r in model.relations) or model.has_fact("operator.kind"))
                ) else "UNPROVEN"
            elif obl in ("monotone_right_expansion", "monotone_left_contraction", "no_solutions_skipped"):
                proofs[obl] = "PROVEN" if (
                    StructuralProperty.MONOTONE_RANGE_SUM in model.structural_properties
                ) else "UNPROVEN"
            elif obl == "both_pointers_advance_monotonically":
                proofs[obl] = "PROVEN" if (
                    StructuralProperty.ORDERED_STATE in model.structural_properties
                ) else "UNPROVEN"
            elif obl == "count_all_valid_ranges":
                proofs[obl] = "PROVEN" if (
                    model.objective.kind == ObjectiveKind.COUNT or
                    model.has_fact("objective.kind") and model.get_fact("objective.kind").value == ObjectiveKind.COUNT
                ) else "UNPROVEN"
            elif obl == "bounded_diameter_holds":
                proofs[obl] = "PROVEN" if (
                    StructuralProperty.BOUNDED_DIAMETER in model.structural_properties or
                    model.has_fact("structural.bounded_diameter")
                ) else "UNPROVEN"
            elif obl == "optimal_subset_contiguous_in_sorted":
                proofs[obl] = "PROVEN" if (
                    StructuralProperty.SORTED_CONTIGUOUS_OPTIMAL_BLOCK in model.structural_properties or
                    model.has_fact("structural.sorted_contiguous_optimal_block")
                ) else "UNPROVEN"
            elif obl == "window_predicate_monotone":
                proofs[obl] = "PROVEN" if (
                    StructuralProperty.MONOTONE_VALID_WINDOW in model.structural_properties or
                    model.has_fact("structural.monotone_valid_window")
                ) else "UNPROVEN"
            elif obl == "maximize_cardinality_optimal":
                proofs[obl] = "PROVEN" if (
                    model.objective.kind == ObjectiveKind.MAXIMIZE_CARDINALITY or
                    (model.has_fact("objective.kind") and model.get_fact("objective.kind").value == ObjectiveKind.MAXIMIZE_CARDINALITY)
                ) else "UNPROVEN"
            elif obl == "single_collection":
                proofs[obl] = "PROVEN" if (
                    StructuralProperty.SINGLE_COLLECTION in model.structural_properties or
                    model.has_fact("collection.single_collection") or
                    len(model.collections) <= 1
                ) else "UNPROVEN"
            elif obl == "pointers_advance_monotonically":
                proofs[obl] = "PROVEN" if (
                    (StructuralProperty.ORDERED_STATE in model.structural_properties or StructuralProperty.SORTABLE in model.structural_properties) and
                    (StructuralProperty.MONOTONE_VALID_WINDOW in model.structural_properties or model.has_fact("structural.monotone_valid_window"))
                ) else "UNPROVEN"
            else:
                proofs[obl] = "UNPROVEN"

        # Final decision status
        if reasons:
            status = CandidateStatus.REJECTED
        elif any(v == "UNPROVEN" for v in proofs.values()):
            status = CandidateStatus.UNPROVEN
        else:
            status = CandidateStatus.ACCEPTED

        return CandidateDecision(
            candidate_name=capability.name,
            status=status,
            reasons=reasons,
            satisfied_requirements=satisfied,
            missing_requirements=missing,
            violated_constraints=violated,
            proof_status=proofs,
            backend=capability.implementation_backend
        )

    @classmethod
    def filter_candidates(cls, registry: CapabilityRegistry, model: ProblemModel) -> List[CandidateDecision]:
        decisions: List[CandidateDecision] = []
        for cap in registry.all():
            decision = cls.evaluate(cap, model)
            decisions.append(decision)
        return decisions
