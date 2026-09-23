"""
CHUP Phase 4: Closed-World Validation Gates (A through H).

Authoritative 8-Gate Taxonomy:
- Gate A: Topology / Structural Invariants (Acyclicity, Connectivity, Directedness, Rootedness)
- Gate B: Structural Validity & Cardinality Bounds (N >= 1, M >= M_min for connected, endpoint bounds)
- Gate C: Weight & Algebraic Validity (Component-specific weights: Dijkstra non-negative, Kruskal arbitrary comparable; negative cycles; invertibility/associativity)
- Gate D: Predicate & Optimization Monotonicity (Bisection decision cut monotonicity)
- Gate E: DP Optimization Validity (Sliding window order, recurrence convexity & slope dominance)
- Gate F: Mutation & Storage Compatibility (MutationSemantics vs StorageSemantics compatibility matrix, state contracts)
- Gate G: Resource Feasibility (Time & memory limits, state space bounds)
- Gate H: Provider & Dependency Resolution (Provider existence, dependency cycle detection)
"""

from typing import Tuple, Optional, Dict, Any
from pointer_algorithms.cross_family.semantic_ontology import (
    CrossFamilyProblemModel,
    CrossFamilyObjective,
    ComplexityEvaluator,
    ComplexityVerdict,
)
from pointer_algorithms.cross_family.component_model import MutationCompatibilityMatrix
from pointer_algorithms.cross_family.composition_engine import CompositionPlan


class CrossFamilyGateEvaluator:
    """
    Evaluates closed-world validation gates A through H against a candidate plan
    and problem model.
    """

    @classmethod
    def evaluate(
        cls,
        model: CrossFamilyProblemModel,
        plan: CompositionPlan,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        ctx = context or {}

        # ── Gate A: Topology / Structural Invariants ──
        # Evaluated context-sensitively: only fails if a component requires ACYCLIC or CONNECTED
        requires_acyclic = any("ACYCLIC_STRUCTURE" in c.proof_obligations for c in plan.components)
        if requires_acyclic and model.has_fact("FACT_TOPOLOGY_CYCLIC"):
            return False, "REQUIRED_ACYCLICITY_VIOLATED", "Component requires acyclic topology, but graph is proven cyclic."

        requires_connected = any("CONNECTIVITY_ASSUMPTION" in c.proof_obligations for c in plan.components)
        if requires_connected and model.has_fact("FACT_TOPOLOGY_DISCONNECTED"):
            return False, "REQUIRED_CONNECTIVITY_VIOLATED", "Component requires connected topology, but graph has multiple components."

        # ── Gate B: Structural Validity & Cardinality Bounds ──
        if model.scale_n <= 0:
            return False, "TOPOLOGY_EMPTY", "Vertex set has size zero or non-positive cardinality."

        if requires_connected and model.scale_m < model.scale_n - 1:
            return False, "REQUIRED_CONNECTIVITY_VIOLATED", f"Edge count M={model.scale_m} is insufficient to form connected topology on N={model.scale_n} (requires M >= N-1)."

        if ctx.get("invalid_endpoint", False):
            return False, "VERTEX_INDEX_OUT_OF_BOUNDS", "Edge endpoint index is outside valid range [0, N-1]."

        # ── Gate C: Weight & Algebraic Validity ──
        # Component-specific: Only algorithms requiring non-negative weights (e.g. Dijkstra) reject negative weights
        requires_non_negative = any("NON_NEGATIVE_WEIGHTS" in c.proof_obligations for c in plan.components)
        if requires_non_negative and model.has_fact("FACT_EDGE_WEIGHTS_CONTAIN_NEGATIVE"):
            return False, "NEGATIVE_EDGE_WEIGHTS_REJECT_GREEDY_HEAP", "Greedy frontier expansion requires all w >= 0; negative edge weight detected."

        if model.has_fact("FACT_NEGATIVE_CYCLE_DETECTED"):
            return False, "NEGATIVE_CYCLE_DETECTED", "Graph contains reachable negative weight cycle."

        requires_invertible = any("INVERTIBLE_OPERATION" in c.proof_obligations for c in plan.components)
        if requires_invertible:
            if model.operation_algebra and not model.operation_algebra.invertible:
                return False, "OPERATION_NOT_INVERTIBLE_REJECTS_PREFIX_DIFFERENCE", f"Prefix difference range query requires invertible group operation; {model.operation_algebra.name} lacks inverse."

        requires_associative = any("ASSOCIATIVE_OPERATION" in c.proof_obligations for c in plan.components)
        if requires_associative:
            if model.operation_algebra and not model.operation_algebra.associative:
                return False, "OPERATION_NOT_ASSOCIATIVE", f"Range aggregation requires associative operation; {model.operation_algebra.name} is not associative."

        # ── Gate D: Predicate & Optimization Monotonicity ──
        requires_monotone = any("MONOTONE_PREDICATE" in c.proof_obligations for c in plan.components)
        if requires_monotone:
            if model.has_fact("FACT_PREDICATE_NON_MONOTONIC") or (model.predicate_contract and not model.predicate_contract.is_monotonic_proven):
                return False, "PREDICATE_NOT_MONOTONIC", "Bisection requires monotone decision predicate P(x); predicate oscillates or monotonicity unproven."

        # ── Gate E: DP Optimization Validity ──
        requires_convex = (
            plan.recipe_name == "cf_convex_dp_monotonic_queue"
            or any("CONVEX_TRANSITION" in c.proof_obligations or "DOMINANCE_ORDER" in c.proof_obligations for c in plan.components)
        )
        if requires_convex:
            if model.has_fact("FACT_NON_CONVEX_TRANSITION") or (model.dp_contract and not model.dp_contract.is_convex_or_monotone_proven):
                return False, "NON_CONVEX_COST_REJECTS_MONOTONIC_QUEUE", "Monotonic deque optimization requires convex cost / slope dominance; convexity condition unproven."

        requires_sliding_window = any("SLIDING_WINDOW_MONOTONICITY" in c.proof_obligations for c in plan.components)
        if requires_sliding_window:
            if not model.has_fact("FACT_SLIDING_WINDOW_ORDERED"):
                return False, "SLIDING_WINDOW_ORDER_VIOLATED", "Sliding window monotonic deque invariant is violated."

        requires_dominance = any("DOMINANCE_ORDER" in c.proof_obligations for c in plan.components)
        if requires_dominance:
            if not model.has_fact("FACT_DOMINANCE_ORDER_ESTABLISHED"):
                return False, "DOMINANCE_ORDER_VIOLATED", "Candidate dominance ordering is violated: suboptimal element may become optimal later."

        requires_expiration = any("WINDOW_EXPIRATION" in c.proof_obligations for c in plan.components)
        if requires_expiration:
            if not model.has_fact("FACT_WINDOW_EXPIRATION_MONOTONIC"):
                return False, "WINDOW_EXPIRATION_VIOLATED", "Window expiration is not monotone."

        # ── Gate F: Mutation & Storage Compatibility ──
        if not plan.is_valid and plan.failure_code in ("STATE_CONTRACT_MISMATCH", "ATTRIBUTE_UNIFICATION_FAILED"):
            return False, plan.failure_code, plan.failure_reason

        for comp in plan.components:
            for req in comp.consumes_state:
                for s in plan.initial_states:
                    if s.satisfies(req):
                        if not MutationCompatibilityMatrix.is_compatible(
                            provider=s.mutation_semantics,
                            consumer=comp.mutation_semantics,
                            provider_storage=s.storage_semantics
                        ):
                            return False, "MUTATION_STORAGE_INCOMPATIBLE", f"Component {comp.name} mutation {comp.mutation_semantics.value} incompatible with storage {s.storage_semantics.value}."

        # ── Gate G: Resource Feasibility ──
        for comp in plan.components:
            verdict, ops, msg = ComplexityEvaluator.evaluate(
                comp.complexity_time,
                n=model.scale_n,
                m=model.scale_m,
                time_limit_sec=model.time_limit_sec,
                memory_limit_mb=model.memory_limit_mb
            )
            if verdict == ComplexityVerdict.PROVABLY_EXCEEDS:
                return False, "STATE_SPACE_EXCEEDS_RESOURCE_BOUNDS", f"Component {comp.name} worst-case operations exceed time limit: {msg}"
            if verdict == ComplexityVerdict.UNKNOWN and ctx.get("strict_complexity", False):
                return False, "STATE_SPACE_EXCEEDS_RESOURCE_BOUNDS", f"Component {comp.name} complexity is unknown: {msg}"

        # ── Gate H: Provider Availability & Dependency Resolution ──
        if not plan.is_valid and plan.failure_code == "NO_PROVIDER_FOR_REQUIRED_STATE":
            return False, "NO_PROVIDER_FOR_REQUIRED_STATE", plan.failure_reason

        if not plan.is_valid and plan.failure_code == "DEPENDENCY_CYCLE":
            return False, "DEPENDENCY_CYCLE", plan.failure_reason

        if not plan.is_valid and plan.failure_code:
            return False, plan.failure_code, plan.failure_reason

        return True, None, None
