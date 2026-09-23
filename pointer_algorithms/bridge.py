"""
JSON-IPC Bridge for Pointer-Based Algorithms Domain.

Communicates with the TypeScript pipeline over stdin/stdout using structured JSON:
Input:
{
    "action": "analyze" | "solve" | "induce",
    "problemText": "...",
    "featuresOverride": {...}
}

Output:
{
    "status": "success" | "rejected" | "error",
    "domain": "pointer_algorithms",
    "selectedPattern": "...",
    "family": "...",
    "invariant": {...},
    "monotonicity": {...},
    "pointerRoles": [...],
    "eliminatedCandidates": [...],
    "code": "...",
    "reasoning": "...",
    "ruleInduced": {...}
}
"""

import sys
import os
import json
import hashlib
from typing import Dict, Any

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.recognition.feature_extractor import FeatureExtractor
from pointer_algorithms.recognition.candidate_generator import CandidateGenerator
from pointer_algorithms.recognition.candidate_eliminator import CandidateEliminator
from pointer_algorithms.reasoning.monotonicity_engine import MonotonicityEngine
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine
from pointer_algorithms.generator.cpp_generator import CppPointerGenerator
from pointer_algorithms.knowledge.knowledge_store import KnowledgeStore
from pointer_algorithms.knowledge.knowledge_graph import KnowledgeGraph
from pointer_algorithms.knowledge.support_state import SupportDetector
from pointer_algorithms.learning.induction import KnowledgeInductionEngine
from pointer_algorithms.learning.knowledge_update import KnowledgeUpdateManager

from pointer_algorithms.reasoning.reasoning_engine import (
    MonotonicityReasoning, GreedyChoiceReasoning, StateTransitionReasoning, InvariantReasoning
)
from pointer_algorithms.proof_explanation import (
    ExplanationBuilder,
    ExplanationValidator,
    ExplanationLevel,
    JsonExplanationRenderer,
    MarkdownExplanationRenderer
)
from pointer_algorithms.deep_understanding import DeepProblemUnderstandingFacade

ALGORITHMIC_FAMILIES = {
    "two_pointers_converging",
    "two_pointers_same_direction",
    "sliding_window",
    "partition_pointers",
    "fast_slow_pointers",
    "counting_pointers",
    "monotonic_stack",   # Phase 3B
    "binary_search",     # Phase 3C
    "trie",              # Phase 3D
    "tree",              # Phase 3E
    "graph",             # Phase 3F
    "heap",              # Phase 3G
    "dsu",               # Phase 3H
    "fenwick",           # Phase 3I
    "segment_tree",      # Phase 3J
    "dynamic_programming",  # Phase 3K
    "greedy",            # Phase 3L
    "divide_and_conquer_backtracking",  # Phase 3M
    "adv_graph",                        # Phase 3N
    "string",                           # Phase 3O
    "number_theory",                    # Phase 3P
    "algebra",                          # Phase 3Q
    "geometry",                         # Phase 3R
    "adv_data_structures",              # Phase 3S
    "cross_family",                     # Phase 4
}
# Backward compatibility alias
POINTER_FAMILIES = ALGORITHMIC_FAMILIES

def _attach_explanation(resp: Dict[str, Any], text: str) -> Dict[str, Any]:
    if not isinstance(resp, dict):
        return resp
    if "explanation" in resp:
        return resp
    try:
        if text and text.strip():
            pid = f"prob_{hashlib.sha256(text.encode('utf-8')).hexdigest()[:8]}"
            facade = DeepProblemUnderstandingFacade()
            du_res = facade.process({"text": text})
            doc = ExplanationBuilder.build(du_res, problem_id=pid)
            resp["explanation"] = doc.to_dict()
        else:
            resp["explanation"] = None
    except Exception:
        resp["explanation"] = None
    return resp

def _handle_request_internal(req: Dict[str, Any]) -> Dict[str, Any]:
    action = req.get("action", "solve")
    text = req.get("problemText") or req.get("problem") or ""

    if action == "explain":
        level_str = req.get("level", "DETAILED")
        try:
            level = ExplanationLevel(level_str)
        except Exception:
            level = ExplanationLevel.DETAILED

        pid = req.get("problem_id") or (f"prob_{hashlib.sha256(text.encode('utf-8')).hexdigest()[:8]}" if text else "problem_default")

        # Mode 1: Authoritative artifact passed directly from memory / storage
        auth_artifact = req.get("authoritativeArtifact")
        if auth_artifact and isinstance(auth_artifact, dict):
            doc = ExplanationBuilder.build(auth_artifact, problem_id=pid, level=level)
            return {
                "status": "success",
                "explanation": doc.to_dict(),
                "markdown": MarkdownExplanationRenderer.render(doc)
            }

        # Mode 2: Standard Phase 6 -> Phase 5 pipeline on problemText first
        if text.strip():
            facade = DeepProblemUnderstandingFacade()
            spec = {"text": text}
            if "featuresOverride" in req and isinstance(req["featuresOverride"], dict):
                spec.update(req["featuresOverride"])
            du_res = facade.process(spec)
            doc = ExplanationBuilder.build(du_res, problem_id=pid, level=level)
            return {
                "status": "success",
                "explanation": doc.to_dict(),
                "markdown": MarkdownExplanationRenderer.render(doc)
            }

        # Artifact resolution failed -> fail closed
        return {
            "status": "error",
            "reasoning": "Artifact resolution failed: artifact not found or unresolvable through authoritative storage."
        }

    # Check Architecture V2 capabilities first
    try:
        from architecture_v2.bridge_v2 import BridgeV2
        v2 = BridgeV2()
        v2_res = v2.solve(text)
        if v2_res.get("status") == "success" and v2_res.get("code"):
            pattern = v2_res.get("selectedPattern")
            if pattern == "greedy_capacity_pairing":
                return {
                    "status": "success",
                    "domain": "pointer_algorithms",
                    "selectedPattern": "greedy_capacity_pairing",
                    "family": "two_pointers_converging",
                    "supportState": {
                        "state": "first_class_supported",
                        "reason": "Proven by Architecture V2 capability reasoning"
                    },
                    "knowledgeGraph": {
                        "node": "greedy_capacity_pairing",
                        "relations": []
                    },
                    "preconditionEvidence": "Sorted array, capacity constraint on pairs, greedy exchange argument proven",
                    "monotonicity": {
                        "kind": "monotonic_convergence",
                        "status": "proven",
                        "property": "Sorted sequence permits greedy opposite-end pairing",
                        "justification": "Greedy choice property & exchange argument hold"
                    },
                    "pointerRoles": ["left", "right"],
                    "eliminatedCandidates": [],
                    "code": v2_res.get("code"),
                    "reasoning": v2_res.get("reasoning", ""),
                    "diagnosticTrace": v2_res.get("diagnosticTrace", [])
                }
            elif pattern == "greedy_two_sequence_interval_matching":
                return {
                    "status": "success",
                    "domain": "pointer_algorithms",
                    "selectedPattern": "greedy_two_sequence_interval_matching",
                    "family": "two_pointers_same_direction",
                    "supportState": {
                        "state": "first_class_supported",
                        "reason": "Proven by Architecture V2 capability reasoning"
                    },
                    "knowledgeGraph": {
                        "node": "greedy_two_sequence_interval_matching",
                        "relations": []
                    },
                    "preconditionEvidence": "Two sorted sequences, 1-to-1 interval tolerance matching, monotone compatibility proven",
                    "monotonicity": {
                        "kind": "dual_monotone_progression",
                        "status": "proven",
                        "property": "Sorted sequences permit dual-pointer monotonic scan with safe discard",
                        "justification": "Greedy choice & exchange argument hold under interval monotonicity"
                    },
                    "pointerRoles": ["pointer_a", "pointer_b"],
                    "eliminatedCandidates": [],
                    "code": v2_res.get("code"),
                    "reasoning": v2_res.get("reasoning", ""),
                    "diagnosticTrace": v2_res.get("diagnosticTrace", [])
                }
            elif pattern == "sliding_window_exact_range_sum_count":
                return {
                    "status": "success",
                    "domain": "pointer_algorithms",
                    "selectedPattern": "sliding_window_exact_range_sum_count",
                    "family": "sliding_window",
                    "supportState": {
                        "state": "first_class_supported",
                        "reason": "Proven by Architecture V2 capability reasoning"
                    },
                    "knowledgeGraph": {
                        "node": "sliding_window_exact_range_sum_count",
                        "relations": []
                    },
                    "preconditionEvidence": "Contiguous range selection, strictly positive elements, monotone range sum proven",
                    "monotonicity": {
                        "kind": "monotone_range_sum",
                        "status": "proven",
                        "property": "Strictly positive elements ensure monotonic window expansion and contraction",
                        "justification": "Window sum strictly increases with right expansion and strictly decreases with left contraction"
                    },
                    "pointerRoles": ["left", "right"],
                    "eliminatedCandidates": [],
                    "code": v2_res.get("code"),
                    "reasoning": v2_res.get("reasoning", ""),
                    "diagnosticTrace": v2_res.get("diagnosticTrace", [])
                }
            elif pattern == "sort_and_maximum_bounded_diameter_subset":
                return {
                    "status": "success",
                    "domain": "pointer_algorithms",
                    "selectedPattern": "sort_and_maximum_bounded_diameter_subset",
                    "family": "sliding_window",
                    "supportState": {
                        "state": "first_class_supported",
                        "reason": "Proven by Architecture V2 capability reasoning"
                    },
                    "knowledgeGraph": {
                        "node": "sort_and_maximum_bounded_diameter_subset",
                        "relations": []
                    },
                    "preconditionEvidence": "Arbitrary subset selection, pairwise bounded diameter relation, cardinality maximization, sorted contiguous optimal block, monotone valid window proven",
                    "monotonicity": {
                        "kind": "monotone_valid_window",
                        "status": "proven",
                        "property": "Sorted sequence ensures max(S) - min(S) <= k is monotone with respect to window boundaries",
                        "justification": "Window difference a[right] - a[left] increases with right expansion and decreases with left contraction"
                    },
                    "pointerRoles": ["left", "right"],
                    "eliminatedCandidates": [],
                    "code": v2_res.get("code"),
                    "reasoning": v2_res.get("reasoning", ""),
                    "diagnosticTrace": v2_res.get("diagnosticTrace", [])
                }
            elif pattern == "two_pointer_pair_sum":
                return {
                    "status": "success",
                    "domain": "pointer_algorithms",
                    "selectedPattern": "pair_sum_sorted",
                    "family": "two_pointers_converging",
                    "supportState": {
                        "state": "first_class_supported",
                        "reason": "Proven by Architecture V2 capability reasoning"
                    },
                    "knowledgeGraph": {
                        "node": "pair_sum_sorted",
                        "relations": []
                    },
                    "preconditionEvidence": "Two pointers converging on sorted array to find target sum",
                    "monotonicity": {
                        "kind": "monotonic_convergence",
                        "status": "proven",
                        "property": "Sorted sequence ensures monotonic pair sum variation with pointer movement",
                        "justification": "Sum strictly increases when left pointer moves right, and strictly decreases when right pointer moves left"
                    },
                    "pointerRoles": ["left", "right"],
                    "eliminatedCandidates": [],
                    "code": v2_res.get("code"),
                    "reasoning": v2_res.get("reasoning", ""),
                    "diagnosticTrace": v2_res.get("diagnosticTrace", [])
                }
            else:
                return {
                    "status": "success",
                    "domain": "pointer_algorithms",
                    "selectedPattern": pattern,
                    "family": "architecture_v2",
                    "supportState": {
                        "state": "first_class_supported",
                        "reason": "Proven by Architecture V2 capability reasoning"
                    },
                    "knowledgeGraph": {
                        "node": pattern,
                        "relations": []
                    },
                    "preconditionEvidence": "Proven by Architecture V2 capability reasoning",
                    "monotonicity": {
                        "kind": "proven",
                        "status": "proven",
                        "property": "Architecture V2 proven",
                        "justification": "All proof obligations established"
                    },
                    "pointerRoles": ["left", "right"],
                    "eliminatedCandidates": [],
                    "code": v2_res.get("code"),
                    "reasoning": v2_res.get("reasoning", ""),
                    "diagnosticTrace": v2_res.get("diagnosticTrace", [])
                }
        elif v2_res.get("status") == "unsupported":
            msg = v2_res.get("limitationMessage") or ""
            cap = v2_res.get("capability")
            if cap in ("sliding_window_exact_range_sum_count", "greedy_capacity_pairing", "greedy_two_sequence_interval_matching") or "COMPOSITION_UNSUPPORTED" in msg:
                rejection_code = "COMPOSITION_UNSUPPORTED" if "COMPOSITION_UNSUPPORTED" in msg else "UNSUPPORTED"
                return {
                    "status": "rejected",
                    "domain": "pointer_algorithms",
                    "selectedPattern": None,
                    "family": None,
                    "eliminatedCandidates": [
                        {
                            "candidate": cap or "composition_candidate",
                            "family": "composition",
                            "rejectionCode": rejection_code,
                            "evidence": msg,
                            "preconditionTested": "composition_support"
                        }
                    ],
                    "recommendedAlternative": "fail_closed_unsupported",
                    "reasoning": f"Architecture V2 failed closed: {msg}",
                    "diagnosticTrace": v2_res.get("diagnosticTrace", [])
                }
    except Exception:
        pass

    features = FeatureExtractor.extract(text)

    # 1. Candidate generation
    candidates = CandidateGenerator.generate_candidates(features)

    # 2. Candidate elimination ("Why not this pattern?")
    filter_result = CandidateEliminator.filter_and_rank(candidates, features)
    selected_eval = filter_result["selected"]
    eliminated_evals = filter_result["eliminated"]

    eliminated_summary = [
        {
            "candidate": e.candidate.pattern,
            "family": e.candidate.family,
            "rejectionCode": e.rejection_code,
            "evidence": e.evidence,
            "preconditionTested": e.precondition_tested,
            "recommendedAlternative": e.recommended_alternative
        }
        for e in eliminated_evals
    ]

    if not selected_eval or selected_eval.candidate.family not in ALGORITHMIC_FAMILIES:
        alt = selected_eval.candidate.pattern if (selected_eval and selected_eval.candidate.family not in ALGORITHMIC_FAMILIES) else (eliminated_summary[0]["recommendedAlternative"] if eliminated_summary else "unknown")
        return {
            "status": "rejected",
            "domain": "pointer_algorithms",
            "selectedPattern": None,
            "family": None,
            "eliminatedCandidates": eliminated_summary,
            "reasoning": f"Problem rejected for pointer algorithms: requires {alt}.",
            "recommendedAlternative": alt
        }

    pattern = selected_eval.candidate.pattern
    family = selected_eval.candidate.family

    # 3. Monotonicity & Invariants
    feature_dict = {
        "raw_text": text,
        "has_negative_values": features.has_negative_values,
        "is_sorted": features.is_sorted,
        "can_sort": features.can_sort,
        "is_contiguous": features.is_contiguous,
        "tracks_distinct": features.tracks_distinct,
        "optimization_objective": features.optimization_objective or "",
        "search_objective": features.search_objective or "",
        "partition_requirement": features.partition_requirement or "",
        "target": features.target_value or "target",
        "k": features.window_size_k or 1,
        "requires_original_indices": features.requires_original_indices,
        "in_place_required": features.in_place_required,
        "heap_kind": features.heap_kind.value if features.heap_kind else "min_heap",
        "heap_k_direction": features.heap_k_direction or "largest",
        "heap_k_value": features.heap_k_value or 1,
        "heap_is_streaming": features.heap_is_streaming,
        "dsu_kind": features.dsu_kind.value if features.dsu_kind else "basic",
        "dsu_metadata_type": features.dsu_metadata_type or "size",
        "dsu_has_weights": features.dsu_has_weights,
        "dsu_has_parity": features.dsu_has_parity,
        "dsu_requires_rollback": features.dsu_requires_rollback,
        "dsu_is_offline": features.dsu_is_offline,
        "fenwick_kind": features.fenwick_kind.value if features.fenwick_kind else "point_update_prefix_query",
        "fenwick_operation_kind": features.fenwick_operation_kind.value if features.fenwick_operation_kind else "point_update",
        "fenwick_is_2d": features.fenwick_is_2d,
        "fenwick_requires_coordinate_compression": features.fenwick_requires_coordinate_compression,
        "fenwick_is_inversion_counting": features.fenwick_is_inversion_counting,
        "fenwick_is_multiset": features.fenwick_is_multiset,
        "fenwick_is_kth": features.fenwick_is_kth,
        "segment_tree_kind": features.segment_tree_kind.value if features.segment_tree_kind else "point_update_range_query",
        "segment_tree_operation_kind": features.segment_tree_operation_kind.value if features.segment_tree_operation_kind else "point_update",
        "segment_tree_query_op": features.segment_tree_query_op or "sum",
        "segment_tree_has_point_update": features.segment_tree_has_point_update,
        "segment_tree_has_range_update": features.segment_tree_has_range_update,
        "segment_tree_has_range_add": features.segment_tree_has_range_add,
        "segment_tree_has_range_assign": features.segment_tree_has_range_assign,
        "segment_tree_has_combined_lazy": features.segment_tree_has_combined_lazy,
        "segment_tree_is_metadata": features.segment_tree_is_metadata,
        "segment_tree_is_max_subarray": features.segment_tree_is_max_subarray,
        "segment_tree_is_frequency": features.segment_tree_is_frequency,
        "segment_tree_is_interval_statistics": features.segment_tree_is_interval_statistics,
        "dp_kind": features.dp_kind.value if features.dp_kind else "linear_1d",
        "dp_operation_kind": features.dp_operation_kind.value if features.dp_operation_kind else "tabulate",
        "dp_state_dimension": features.dp_state_dimension,
        "dp_has_optimal_substructure": features.dp_has_optimal_substructure,
        "dp_has_overlapping_subproblems": features.dp_has_overlapping_subproblems,
        "dp_is_dag": features.dp_is_dag,
        "dp_requires_reconstruction": features.dp_requires_reconstruction,
        "dp_space_compressible": features.dp_space_compressible,
        "dp_is_unbounded": features.dp_is_unbounded,
        "greedy_kind": features.greedy_kind.value if features.greedy_kind else "greedy_interval_selection",
        "greedy_proof_kind": features.greedy_proof_kind.value if features.greedy_proof_kind else "greedy_exchange_proof",
        "greedy_ordering_candidate": features.greedy_ordering_candidate,
        "greedy_has_local_choice": features.greedy_has_local_choice,
        "greedy_requires_sorting": features.greedy_requires_sorting,
        "greedy_requires_heap": features.greedy_requires_heap,
        # Divide & Conquer / Backtracking features (Phase 3M)
        "dc_backtracking_kind": features.dc_backtracking_kind.value if features.dc_backtracking_kind else "dc_merge_sort_inversions",
        "subproblem_dependency_kind": features.subproblem_dependency_kind.value if features.subproblem_dependency_kind else "disjoint",
        "termination_guarantee_kind": features.termination_guarantee_kind.value if features.termination_guarantee_kind else "counting_correctness",
        "dc_is_independent_subproblems": features.dc_is_independent_subproblems,
        "dc_has_cross_boundary_combine": features.dc_has_cross_boundary_combine,
        "backtracking_is_exponential": features.backtracking_is_exponential,
        "backtracking_requires_pruning": features.backtracking_requires_pruning,
        "backtracking_state_restoration": features.backtracking_state_restoration,
        # Advanced Graph features (Phase 3N)
        "is_adv_graph_detected": getattr(features, "is_adv_graph_detected", False),
        "adv_graph_algorithm_family": getattr(features, "adv_graph_algorithm_family", None),
        "adv_graph_semantic_model": getattr(features, "adv_graph_semantic_model", None),
        "adv_graph_candidate_evaluations": getattr(features, "adv_graph_candidate_evaluations", []),
        # String Algorithms & Automata features (Phase 3O)
        "is_string_algorithm_detected": getattr(features, "is_string_algorithm_detected", False),
        "string_algorithm_family": getattr(features, "string_algorithm_family", None),
        "string_semantic_model": getattr(features, "string_semantic_model", None),
        "string_candidate_evaluations": getattr(features, "string_candidate_evaluations", []),
        # Number Theory & Combinatorics features (Phase 3P)
        "is_number_theory_detected": getattr(features, "is_number_theory_detected", False),
        "number_theory_family": getattr(features, "number_theory_family", None),
        "number_theory_semantic_model": getattr(features, "number_theory_semantic_model", None),
        "number_theory_candidate_evaluations": getattr(features, "number_theory_candidate_evaluations", []),
        # Algebra / Transforms features (Phase 3Q)
        "is_algebra_detected": getattr(features, "is_algebra_detected", False),
        "algebra_family": getattr(features, "algebra_family", None),
        "algebra_semantic_model": getattr(features, "algebra_semantic_model", None),
        "algebra_candidate_evaluations": getattr(features, "algebra_candidate_evaluations", []),
        # Computational Geometry features (Phase 3R)
        "is_geometry_detected": getattr(features, "is_geometry_detected", False),
        "geometry_family": getattr(features, "geometry_family", None),
        "geometry_semantic_model": getattr(features, "geometry_semantic_model", None),
        "geometry_candidate_evaluations": getattr(features, "geometry_candidate_evaluations", []),
        # Advanced Data Structures features (Phase 3S)
        "is_ads_detected": getattr(features, "is_ads_detected", False),
        "ads_family": getattr(features, "ads_family", None),
        "ads_semantic_model": getattr(features, "ads_semantic_model", None),
        "ads_candidate_evaluations": getattr(features, "ads_candidate_evaluations", []),
    }

    mono_assessment = MonotonicityEngine.assess_for_pattern(
        pattern=pattern,
        has_negative_values=features.has_negative_values,
        is_sorted=features.is_sorted,
        can_sort=features.can_sort,
        is_contiguous=features.is_contiguous,
        tracks_distinct=features.tracks_distinct,
        objective_type=features.optimization_objective or ""
    )

    invariant = InvariantEngine.construct_invariant(pattern, feature_dict)
    movement = MovementDerivationEngine.derive(pattern, feature_dict)

    # 4. Code Generation
    code = CppPointerGenerator.generate(pattern, feature_dict)

    # 5. Induction & Abstraction
    store = KnowledgeStore()
    induced_rule = KnowledgeInductionEngine.induce_rule_from_solution(
        problem_id="active_problem",
        pattern_kind=pattern,
        sample_input=None,
        features=feature_dict,
        simulation_result={}
    )
    promoted, promo_msg, final_rule = KnowledgeUpdateManager.attempt_promotion(store, induced_rule)

    eliminated_reasons = [e["rejectionCode"] for e in eliminated_summary if e.get("rejectionCode")]
    is_composed = pattern in ("exact_count_derived", "three_sum_converging", "four_sum_converging", "closest_pair_sum")
    support_assessment = SupportDetector.assess(
        selected_pattern=pattern,
        is_composed=is_composed,
        eliminated_reasons=eliminated_reasons
    )
    kg = KnowledgeGraph()
    kg_relations = [
        {"relation": r.relation.value, "target": r.target, "rationale": r.rationale}
        for r in kg.get_relations(pattern)
    ]

    reasoning_summary = (
        f"Selected pattern '{pattern}' ({family}) [Support State: {support_assessment.state.value}]. "
        f"Precondition confirmed: {selected_eval.evidence} "
        f"Monotonic property: {mono_assessment.property_description} "
        f"Pointer movement derived from objective: {movement.objective_function}."
    )

    resp = {
        "status": "success",
        "domain": "pointer_algorithms",
        "selectedPattern": pattern,
        "pattern": pattern,
        "family": family,
        "supportState": support_assessment.to_dict(),
        "knowledgeGraph": {
            "node": pattern,
            "relations": kg_relations
        },
        "preconditionEvidence": selected_eval.evidence,
        "monotonicity": {
            "kind": mono_assessment.kind.value,
            "status": mono_assessment.status.value,
            "property": mono_assessment.property_description,
            "justification": mono_assessment.justification
        },
        "invariant": {
            "before": invariant.before_iteration,
            "during": invariant.during_iteration,
            "after": invariant.after_movement,
            "termination": invariant.at_termination
        },
        "movement": {
            "objective": movement.objective_function,
            "decisions": movement.decision_conditions,
            "eliminationProof": movement.elimination_proof
        },
        "eliminatedCandidates": eliminated_summary,
        "code": code,
        "generatedCode": code,
        "reasoning": reasoning_summary,
        "binarySearch": {
            "searchSpace": {
                "type": features.search_space_type or "indices",
                "ordered": features.has_ordered_search_space or features.is_answer_space_search or features.has_numeric_domain
            },
            "predicate": {
                "name": "isFeasible" if features.is_answer_space_search else "compare",
                "direction": features.predicate_direction or "false_to_true",
                "isMonotone": features.has_monotonic_predicate
            },
            "boundary": features.target_boundary or "first_true",
            "justification": mono_assessment.justification
        } if family == "binary_search" else None,
        "trie": {
            "kind": features.trie_kind.value if features.trie_kind else "character_trie",
            "queryType": features.prefix_query_type or "exact_search",
            "alphabet": features.trie_alphabet.value if features.trie_alphabet else "lowercase_26",
            "storage": features.trie_storage.value if features.trie_storage else "fixed_array",
            "estimatedMemoryBytes": features.estimated_memory_bytes,
            "memoryLimitExceeded": features.memory_limit_exceeded,
            "hasPrefixAdvantage": features.has_prefix_sharing_advantage,
            "greedyProof": GreedyChoiceReasoning.prove_xor_greedy_choice(32).__dict__ if (features.trie_kind and features.trie_kind.value == "binary_trie") else None
        } if family == "trie" else None,
        "tree": {
            "kind": features.tree_kind.value if features.tree_kind else "rooted_tree",
            "representation": features.tree_representation.value if features.tree_representation else "adjacency_list",
            "traversalOrder": features.tree_traversal_order.value if features.tree_traversal_order else None,
            "aggregationOp": features.tree_aggregation_op,
            "isBST": features.is_bst,
            "isValidatingBST": features.is_validating_bst,
            "duplicatePolicy": features.bst_duplicate_policy,
            "lcaType": features.lca_query_type,
            "dpStateType": features.tree_dp_type,
            "recursionRisk": features.tree_recursion_risk,
            "maxDepth": features.tree_max_depth_estimate,
        } if family == "tree" else None,
        "graph": {
            "kind": features.graph_kind.value if features.graph_kind else "unknown",
            "weightKind": features.graph_weight_kind.value if features.graph_weight_kind else "unknown",
            "isDirected": features.graph_is_directed,
            "isWeighted": features.graph_is_weighted,
            "hasNegativeWeights": features.graph_has_negative_weights,
            "hasNegativeCycles": features.graph_has_negative_cycles,
            "isCyclic": features.graph_is_cyclic,
            "isDAG": features.graph_is_dag,
            "isBipartite": features.graph_is_bipartite,
            "isDisconnected": features.graph_is_disconnected,
            "vertexCount": features.graph_vertex_count_v,
            "queryType": features.graph_query_type,
            "algorithmFamily": features.graph_algorithm_family,
            "representation": features.graph_representation.value if features.graph_representation else "adjacency_list",
            "composedCapabilities": (["heap_priority_frontier"] if features.graph_algorithm_family in ("graph_dijkstra", "graph_mst_prim") else (["dsu_disjoint_sets"] if features.graph_algorithm_family == "graph_mst_kruskal" else []))
        } if family == "graph" else None,
        "heap": {
            "kind": features.heap_kind.value if features.heap_kind else "min_heap",
            "kDirection": features.heap_k_direction,
            "kValue": features.heap_k_value,
            "isStreaming": features.heap_is_streaming,
            "isDynamicMedian": features.heap_is_dynamic_median,
            "isKWayMerge": features.heap_is_k_way_merge,
            "isScheduling": features.heap_is_scheduling,
            "isGreedySelection": features.heap_is_greedy_selection,
            "isLazyDeletion": features.heap_is_lazy_deletion,
            "algorithmFamily": features.heap_algorithm_family,
        } if family == "heap" else None,
        "dsu": {
            "kind": features.dsu_kind.value if features.dsu_kind else "basic",
            "operationKind": features.dsu_operation_kind.value if features.dsu_operation_kind else None,
            "algorithmFamily": features.dsu_algorithm_family,
            "hasMetadata": features.dsu_has_metadata,
            "metadataType": features.dsu_metadata_type,
            "hasWeights": features.dsu_has_weights,
            "hasParity": features.dsu_has_parity,
            "requiresRollback": features.dsu_requires_rollback,
            "isOffline": features.dsu_is_offline,
            "hasDifferenceQuery": features.dsu_has_difference_query,
            "hasContradictionCheck": features.dsu_has_contradiction_check,
            "historicalQueries": features.dsu_historical_queries,
        } if family == "dsu" else None,
        "fenwick": {
            "kind": features.fenwick_kind.value if features.fenwick_kind else "point_update_prefix_query",
            "operationKind": features.fenwick_operation_kind.value if features.fenwick_operation_kind else "point_update",
            "algorithmFamily": features.fenwick_algorithm_family,
            "hasUpdates": features.fenwick_has_updates,
            "isStatic": features.fenwick_is_static,
            "is2D": features.fenwick_is_2d,
            "requiresCoordinateCompression": features.fenwick_requires_coordinate_compression,
            "isInversionCounting": features.fenwick_is_inversion_counting,
            "isMultiset": features.fenwick_is_multiset,
            "isKth": features.fenwick_is_kth,
            "monotonicExtremum": features.fenwick_monotonic_extremum,
        } if family == "fenwick" else None,
        "segment_tree": {
            "kind": features.segment_tree_kind.value if features.segment_tree_kind else "point_update_range_query",
            "operationKind": features.segment_tree_operation_kind.value if features.segment_tree_operation_kind else "point_update",
            "algorithmFamily": features.segment_tree_algorithm_family,
            "hasUpdates": features.segment_tree_has_updates,
            "isStatic": features.segment_tree_is_static,
            "queryOp": features.segment_tree_query_op,
            "hasRangeAdd": features.segment_tree_has_range_add,
            "hasRangeAssign": features.segment_tree_has_range_assign,
            "hasCombinedLazy": features.segment_tree_has_combined_lazy,
            "isMetadata": features.segment_tree_is_metadata,
            "isMaxSubarray": features.segment_tree_is_max_subarray,
            "isFrequency": features.segment_tree_is_frequency,
            "isIntervalStatistics": features.segment_tree_is_interval_statistics,
        } if family == "segment_tree" else None,
        "dynamic_programming": {
            "kind": features.dp_kind.value if features.dp_kind else "linear_1d",
            "operationKind": features.dp_operation_kind.value if features.dp_operation_kind else "tabulate",
            "stateDimension": features.dp_state_dimension,
            "hasOptimalSubstructure": features.dp_has_optimal_substructure,
            "hasOverlappingSubproblems": features.dp_has_overlapping_subproblems,
            "isDag": features.dp_is_dag,
            "requiresReconstruction": features.dp_requires_reconstruction,
            "spaceCompressible": features.dp_space_compressible,
        } if family == "dynamic_programming" else None,
        "greedy": {
            "kind": features.greedy_kind.value if features.greedy_kind else "greedy_interval_selection",
            "proofKind": features.greedy_proof_kind.value if features.greedy_proof_kind else "greedy_exchange_proof",
            "algorithmFamily": features.greedy_algorithm_family,
            "hasLocalChoice": features.greedy_has_local_choice,
            "hasExchangeSignal": features.greedy_has_exchange_signal,
            "hasDominanceSignal": features.greedy_has_dominance_signal,
            "hasStayingAheadSignal": features.greedy_has_staying_ahead_signal,
            "hasCutPropertySignal": features.greedy_has_cut_property_signal,
            "hasMatroidSignal": features.greedy_has_matroid_signal,
            "requiresSorting": features.greedy_requires_sorting,
            "requiresHeap": features.greedy_requires_heap,
            "hasGreedyChoice": features.greedy_has_greedy_choice,
            "hasOptimalSubstructure": features.greedy_has_optimal_substructure,
        } if family == "greedy" else None,
        "adv_graph": {
            "algorithmFamily": getattr(features, "adv_graph_algorithm_family", None),
            "detected": getattr(features, "is_adv_graph_detected", False),
            "candidateEvaluations": [
                {
                    "componentId": getattr(c, "component_name", getattr(c, "component_id", "")),
                    "status": c.status.value if hasattr(c.status, "value") else str(c.status),
                    "evidence": getattr(c, "evidence", getattr(c, "justification", "")),
                    "timeComplexity": getattr(c, "complexity", getattr(c, "time_complexity", "")),
                }
                for c in getattr(features, "adv_graph_candidate_evaluations", [])
            ] if hasattr(features, "adv_graph_candidate_evaluations") and features.adv_graph_candidate_evaluations else []
        } if family == "adv_graph" else None,
        "string": {
            "algorithmFamily": getattr(features, "string_algorithm_family", None),
            "detected": getattr(features, "is_string_algorithm_detected", False),
            "candidateEvaluations": [
                {
                    "componentId": getattr(c, "component_name", getattr(c, "pattern", "")),
                    "status": c.status.value if hasattr(c.status, "value") else str(c.status),
                    "evidence": getattr(c, "evidence", getattr(c, "justification", "")),
                    "timeComplexity": getattr(c, "complexity", getattr(c, "time_complexity", "")),
                }
                for c in getattr(features, "string_candidate_evaluations", [])
            ] if hasattr(features, "string_candidate_evaluations") and features.string_candidate_evaluations else []
        } if family == "string" else None,
        "number_theory": {
            "algorithmFamily": getattr(features, "number_theory_family", None),
            "detected": getattr(features, "is_number_theory_detected", False),
            "candidateEvaluations": [
                {
                    "componentId": getattr(c, "component_name", getattr(c, "pattern", "")),
                    "status": c.status.value if hasattr(c.status, "value") else str(c.status),
                    "evidence": getattr(c, "evidence", getattr(c, "justification", "")),
                    "timeComplexity": getattr(c, "complexity", getattr(c, "time_complexity", "")),
                }
                for c in getattr(features, "number_theory_candidate_evaluations", [])
            ] if hasattr(features, "number_theory_candidate_evaluations") and features.number_theory_candidate_evaluations else []
        } if family == "number_theory" else None,
        "algebra": {
            "algorithmFamily": getattr(features, "algebra_family", None),
            "detected": getattr(features, "is_algebra_detected", False),
            "candidateEvaluations": [
                {
                    "componentId": getattr(c, "component_name", getattr(c, "pattern", "")),
                    "status": c.status.value if hasattr(c.status, "value") else str(c.status),
                    "evidence": getattr(c, "evidence", getattr(c, "justification", "")),
                    "timeComplexity": getattr(c, "complexity", getattr(c, "time_complexity", "")),
                }
                for c in getattr(features, "algebra_candidate_evaluations", [])
            ] if hasattr(features, "algebra_candidate_evaluations") and features.algebra_candidate_evaluations else []
        } if family == "algebra" else None,
        "geometry": {
            "algorithmFamily": getattr(features, "geometry_family", None),
            "detected": getattr(features, "is_geometry_detected", False),
            "candidateEvaluations": [
                {
                    "componentId": getattr(c, "component_name", getattr(c, "pattern", "")),
                    "status": c.status.value if hasattr(c.status, "value") else str(c.status),
                    "evidence": getattr(c, "evidence", getattr(c, "justification", "")),
                    "timeComplexity": getattr(c, "complexity", getattr(c, "time_complexity", "")),
                }
                for c in getattr(features, "geometry_candidate_evaluations", [])
            ] if hasattr(features, "geometry_candidate_evaluations") and features.geometry_candidate_evaluations else []
        } if family == "geometry" else None,
        "adv_data_structures": {
            "algorithmFamily": getattr(features, "ads_family", None),
            "detected": getattr(features, "is_ads_detected", False),
            "candidateEvaluations": [
                {
                    "componentId": getattr(c, "component_name", getattr(c, "pattern", "")),
                    "status": c.status.value if hasattr(c.status, "value") else str(c.status),
                    "evidence": getattr(c, "evidence", getattr(c, "rationale", "")),
                    "timeComplexity": getattr(c, "complexity", getattr(c, "time_complexity", "")),
                }
                for c in getattr(features, "ads_candidate_evaluations", [])
            ] if hasattr(features, "ads_candidate_evaluations") and features.ads_candidate_evaluations else []
        } if family == "adv_data_structures" else None,
        "cross_family": {
            "algorithmFamily": getattr(features, "cross_family_family", None),
            "detected": getattr(features, "is_cross_family_detected", False),
            "candidateEvaluations": [
                {
                    "componentId": getattr(c, "component_name", getattr(c, "pattern", "")),
                    "status": c.status.value if hasattr(c.status, "value") else str(c.status),
                    "evidence": getattr(c, "evidence", getattr(c, "justification", "")),
                    "timeComplexity": getattr(c, "complexity", getattr(c, "time_complexity", "")),
                }
                for c in getattr(features, "cross_family_candidate_evaluations", [])
            ] if hasattr(features, "cross_family_candidate_evaluations") and features.cross_family_candidate_evaluations else []
        } if family == "cross_family" else None,
        "ruleInduced": final_rule.to_dict(),
        "promotionMessage": promo_msg
    }

    return resp


def handle_request(req: Dict[str, Any]) -> Dict[str, Any]:
    resp = _handle_request_internal(req)
    text = req.get("problemText") or req.get("problem") or ""
    return _attach_explanation(resp, text)



def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Quick self test
        test_input = {"problemText": "Given a sorted array of integers, find two numbers that add up to target T."}
        print(json.dumps(handle_request(test_input), indent=2))
        return

    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return
        req = json.loads(raw)
        resp = handle_request(req)
        print(json.dumps(resp))
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}))

if __name__ == "__main__":
    main()
