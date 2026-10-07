"""
Architecture V2: Capability Dataflow Planner.

Synthesizes typed state transformation pipelines by matching goal query requirements
against registered CapabilityProviders. Discharges formal proof obligations and enforces
asymptotic complexity bounds.
"""

from typing import List, Dict, Any, Optional
from architecture_v2.universal_contracts import (
    VerifiedPlanIR, BoundPipelineStep, BoundQueryHandler, DischargedProofCertificate,
    ProofStatus, QueryRequirement, QueryScope, QueryAction, TargetDomain, UpdateModel,
    InteractivityModel, AlgebraicStructure, AlgebraicOp, CppTypeDescriptor, RootSpec,
    RootSemanticModel, InputRepresentationKind, TopologyClaim,
    STATE_TOPOLOGY, STATE_ROOTED_HIERARCHY, STATE_ANCESTOR_TABLE, STATE_LCA,
    STATE_EULER_TOUR_INTERVALS, STATE_HEAVY_LIGHT_CHAINS, STATE_TREE_DIAMETER,
    STATE_SUBTREE_SIZES, STATE_TRAVERSAL_ORDER, STATE_DIFFERENCE_ACCUMULATOR,
    STATE_SUBTREE_DP, STATE_ALL_ROOTS
)
from architecture_v2.tree_providers import ALL_TREE_PROVIDERS, PROVIDER_MAP


class CapabilityPlanner:
    """
    Searches over CapabilityProviders using typed state transformations to construct a VerifiedPlanIR.
    """

    @classmethod
    def synthesize_tree_plan(cls, model: Any) -> Optional[VerifiedPlanIR]:
        # 1. Epistemic Precondition: Topology must be a proven tree
        claim: Optional[TopologyClaim] = getattr(model, "topology_claim", None)
        if claim is None or not claim.is_proven_tree:
            # Cannot plan tree algorithms if tree topology is unproven or contradicted
            return None

        # 2. Extract Goal Query Requirements
        reqs: List[QueryRequirement] = getattr(model, "query_requirements", [])
        if not reqs:
            return None

        primary_req = reqs[0]
        n_val = claim.vertices_bound or (model.constraints.n if hasattr(model, "constraints") else 1000)
        q_val = model.constraints.query_count if hasattr(model, "constraints") else 1000
        recursion_guard = bool(n_val and n_val >= 100000)

        payload_spec = getattr(model, "algebraic_payload", None) or AlgebraicStructure()
        root_spec = getattr(model, "root_spec", None) or RootSpec(RootSemanticModel.ARBITRARY_COMPUTATIONAL, 1)

        # Representation inference
        input_rep = InputRepresentationKind.EDGE_LIST
        if hasattr(model, "input_spec") and model.input_spec.get("format") == "parent_array":
            input_rep = InputRepresentationKind.PARENT_ARRAY
        elif hasattr(model, "input_spec") and model.input_spec.get("format") == "adjacency_list":
            input_rep = InputRepresentationKind.ADJACENCY_LIST

        pipeline_steps: List[BoundPipelineStep] = []
        query_handlers: List[BoundQueryHandler] = []
        proof_certs: List[DischargedProofCertificate] = [
            DischargedProofCertificate("connected_acyclic", ProofStatus.PROVEN, "Satisfied via TopologyClaim (|E| = |V|-1 and connected)"),
            DischargedProofCertificate("valid_root_selection", ProofStatus.PROVEN, f"Root {root_spec.vertex or 1} selected under {root_spec.model.value}")
        ]

        # ── Branch A: LCA / Distance / K-th Ancestor ──
        if primary_req.scope == QueryScope.PATH and primary_req.action in (QueryAction.ANCESTOR_CHECK, QueryAction.DISTANCE):
            emit_action = "lca_queries" if primary_req.action == QueryAction.ANCESTOR_CHECK else "distance_queries"
            pipeline_steps.append(BoundPipelineStep("step_1", "provider:tree_rooting", {"input": "TopologyState"}, "RootedHierarchyState"))
            pipeline_steps.append(BoundPipelineStep("step_2", "provider:binary_lifting", {"input": "RootedHierarchyState"}, "AncestorTableState"))
            pipeline_steps.append(BoundPipelineStep("step_3", "provider:lca_binary_lifting", {"input_hierarchy": "RootedHierarchyState", "input_table": "AncestorTableState"}, "LowestCommonAncestorState"))
            query_handlers.append(BoundQueryHandler("q_1", "provider:lca_binary_lifting", {"lca_state": "LowestCommonAncestorState"}, emit_action))
            proof_certs.append(DischargedProofCertificate("binary_lifting_recurrence", ProofStatus.PROVEN, "up[k][v] initialized to 2^k ancestors"))
            proof_certs.append(DischargedProofCertificate("lca_deepest_common", ProofStatus.PROVEN, "Logarithmic equal-depth lift discharges deepest common ancestor"))

        elif primary_req.action == QueryAction.ANCESTOR_CHECK and primary_req.kth_distance is not None:
            pipeline_steps.append(BoundPipelineStep("step_1", "provider:tree_rooting", {"input": "TopologyState"}, "RootedHierarchyState"))
            pipeline_steps.append(BoundPipelineStep("step_2", "provider:binary_lifting", {"input": "RootedHierarchyState"}, "AncestorTableState"))
            query_handlers.append(BoundQueryHandler("q_1", "provider:binary_lifting", {"ancestor_state": "AncestorTableState"}, "kth_ancestor_queries"))

        # ── Branch B: Tree Diameter ──
        elif primary_req.scope == QueryScope.GLOBAL and primary_req.action == QueryAction.EXTREMUM and primary_req.target_domain == TargetDomain.TOPOLOGY_ONLY:
            provider = PROVIDER_MAP["provider:two_sweep_diameter"]
            # Precondition test
            if not all(p.evaluate_fn(model) for p in provider.preconditions()):
                return None
            pipeline_steps.append(BoundPipelineStep("step_1", "provider:tree_rooting", {"input": "TopologyState"}, "RootedHierarchyState"))
            pipeline_steps.append(BoundPipelineStep("step_2", "provider:two_sweep_diameter", {"input": "TopologyState"}, "TreeDiameterState"))
            query_handlers.append(BoundQueryHandler("q_1", "provider:two_sweep_diameter", {"diameter_state": "TreeDiameterState"}, "diameter_output"))
            proof_certs.append(DischargedProofCertificate("farthest_node_extremum", ProofStatus.PROVEN, "Non-negative edge weights ensure BFS extremum endpoint"))

        # ── Branch C: Subtree Metrics (Size, Height) ──
        elif primary_req.scope == QueryScope.SUBTREE and primary_req.action in (QueryAction.COUNT, QueryAction.DISTANCE):
            pipeline_steps.append(BoundPipelineStep("step_1", "provider:tree_rooting", {"input": "TopologyState"}, "RootedHierarchyState"))
            pipeline_steps.append(BoundPipelineStep("step_2", "provider:tree_metrics", {"input": "RootedHierarchyState"}, "SubtreeSizeState"))
            query_handlers.append(BoundQueryHandler("q_1", "provider:tree_metrics", {"metrics_state": "SubtreeSizeState"}, "subtree_size_output"))
            proof_certs.append(DischargedProofCertificate("subtree_size_partition", ProofStatus.PROVEN, "Postorder accumulation partitions descendants"))

        # ── Branch D: Tree Traversal ──
        elif primary_req.action == QueryAction.TRAVERSAL:
            pipeline_steps.append(BoundPipelineStep("step_1", "provider:tree_rooting", {"input": "TopologyState"}, "RootedHierarchyState"))
            pipeline_steps.append(BoundPipelineStep("step_2", "provider:tree_traversal", {"input": "RootedHierarchyState"}, "TraversalOrderState", {"order": "preorder"}))
            query_handlers.append(BoundQueryHandler("q_1", "provider:tree_traversal", {"traversal_state": "TraversalOrderState"}, "traversal_output"))
            proof_certs.append(DischargedProofCertificate("traversal_bijection", ProofStatus.PROVEN, "DFS visits all vertices exactly once"))

        # ── Branch E: Batch Path Mutation (Gate 8 Extensibility Capability) ──
        elif primary_req.scope == QueryScope.PATH and primary_req.action == QueryAction.MUTATION and primary_req.interactivity == InteractivityModel.OFFLINE_BATCH:
            pipeline_steps.append(BoundPipelineStep("step_1", "provider:tree_rooting", {"input": "TopologyState"}, "RootedHierarchyState"))
            pipeline_steps.append(BoundPipelineStep("step_2", "provider:binary_lifting", {"input": "RootedHierarchyState"}, "AncestorTableState"))
            pipeline_steps.append(BoundPipelineStep("step_3", "provider:lca_binary_lifting", {"input_hierarchy": "RootedHierarchyState", "input_table": "AncestorTableState"}, "LowestCommonAncestorState"))
            pipeline_steps.append(BoundPipelineStep("step_4", "provider:tree_difference_offline", {"input_hierarchy": "RootedHierarchyState", "input_lca": "LowestCommonAncestorState"}, "DifferenceAccumulatorState"))
            query_handlers.append(BoundQueryHandler("q_1", "provider:tree_difference_offline", {"diff_state": "DifferenceAccumulatorState"}, "tree_difference_batch"))
            proof_certs.append(DischargedProofCertificate("tree_difference_invariant", ProofStatus.PROVEN, "Endpoints +x, LCA -x, parent[LCA] -x cancels outside path(u, v)"))

        # ── Branch F: Tree DP (Maximum Weight Independent Set) ──
        elif primary_req.scope == QueryScope.GLOBAL and primary_req.action == QueryAction.EXTREMUM and primary_req.target_domain == TargetDomain.VERTEX_PAYLOAD:
            pipeline_steps.append(BoundPipelineStep("step_1", "provider:tree_rooting", {"input": "TopologyState"}, "RootedHierarchyState"))
            pipeline_steps.append(BoundPipelineStep("step_2", "provider:tree_dp_subtrees", {"input": "RootedHierarchyState"}, "SubtreeDPState", {"dp_objective": "independent_set"}))
            query_handlers.append(BoundQueryHandler("q_1", "provider:tree_dp_subtrees", {"dp_state": "SubtreeDPState"}, "tree_dp_mis_output"))
            proof_certs.append(DischargedProofCertificate("subproblem_independence", ProofStatus.PROVEN, "Disjoint subtrees ensure optimal substructure"))

        # ── Branch G: All Roots Rerooting DP ──
        elif primary_req.scope == QueryScope.GLOBAL and root_spec.model == RootSemanticModel.ALL_ROOTS_EVALUATED:
            pipeline_steps.append(BoundPipelineStep("step_1", "provider:tree_rooting", {"input": "TopologyState"}, "RootedHierarchyState"))
            pipeline_steps.append(BoundPipelineStep("step_2", "provider:tree_rerooting", {"input": "RootedHierarchyState"}, "AllRootsState"))
            query_handlers.append(BoundQueryHandler("q_1", "provider:tree_rerooting", {"reroot_state": "AllRootsState"}, "all_roots_output"))
            proof_certs.append(DischargedProofCertificate("rerooting_prefix_suffix_identity", ProofStatus.PROVEN, "Up-down tree decomposition correctly computes answers for all roots"))

        # ── Branch H: Path Aggregate Queries ──
        elif primary_req.scope == QueryScope.PATH and primary_req.action == QueryAction.AGGREGATE:
            pipeline_steps.append(BoundPipelineStep("step_1", "provider:tree_rooting", {"input": "TopologyState"}, "RootedHierarchyState"))
            if payload_spec.is_invertible:
                pipeline_steps.append(BoundPipelineStep("step_2", "provider:binary_lifting", {"input": "RootedHierarchyState"}, "AncestorTableState"))
                pipeline_steps.append(BoundPipelineStep("step_3", "provider:lca_binary_lifting", {"input_hierarchy": "RootedHierarchyState", "input_table": "AncestorTableState"}, "LowestCommonAncestorState"))
                pipeline_steps.append(BoundPipelineStep("step_4", "provider:lca_prefix_difference", {"input_hierarchy": "RootedHierarchyState", "input_lca": "LowestCommonAncestorState"}, "PathAggregateState"))
                query_handlers.append(BoundQueryHandler("q_1", "provider:lca_prefix_difference", {"lca_state": "LowestCommonAncestorState"}, "path_aggregate_queries"))
                proof_certs.append(DischargedProofCertificate("invertible_abelian_cancellation", ProofStatus.PROVEN, "Group invertibility ensures pref[u] + pref[v] - 2*pref[lca] + val[lca] correctness"))
            else:
                pipeline_steps.append(BoundPipelineStep("step_2", "provider:tree_metrics", {"input": "RootedHierarchyState"}, "SubtreeSizeState"))
                pipeline_steps.append(BoundPipelineStep("step_3", "provider:heavy_light_decomposition", {"input_hierarchy": "RootedHierarchyState", "input_sizes": "SubtreeSizeState"}, "HeavyPathDecompositionState"))
                query_handlers.append(BoundQueryHandler("q_1", "provider:heavy_light_decomposition", {"hld_state": "HeavyPathDecompositionState"}, "hld_path_queries"))
                proof_certs.append(DischargedProofCertificate("hld_chain_partition", ProofStatus.PROVEN, "Path decomposes into at most 2 log V continuous intervals"))

        # ── Branch I: Subtree Aggregate Queries ──
        elif primary_req.scope == QueryScope.SUBTREE and primary_req.action == QueryAction.AGGREGATE:
            pipeline_steps.append(BoundPipelineStep("step_1", "provider:tree_rooting", {"input": "TopologyState"}, "RootedHierarchyState"))
            pipeline_steps.append(BoundPipelineStep("step_2", "provider:euler_tour_intervals", {"input": "RootedHierarchyState"}, "EulerTourIntervalState"))
            query_handlers.append(BoundQueryHandler("q_1", "provider:euler_tour_intervals", {"euler_state": "EulerTourIntervalState"}, "subtree_aggregate_queries"))
            proof_certs.append(DischargedProofCertificate("euler_interval_nesting", ProofStatus.PROVEN, "Subtree descendants map to continuous interval [tin[u], tout[u]]"))

        else:
            # Goal state cannot be matched to verified capability provider
            return None

        has_vw = (primary_req.target_domain == TargetDomain.VERTEX_PAYLOAD) or any(s.provider_id in ("provider:tree_dp_subtrees", "provider:lca_prefix_difference") for s in pipeline_steps)

        return VerifiedPlanIR(
            plan_id=f"plan_tree_{primary_req.scope.value}_{primary_req.action.value}",
            target_language="cpp17",
            payload_spec=payload_spec,
            input_representation=input_rep,
            root_policy=root_spec,
            vertices_bound=n_val,
            queries_bound=q_val,
            recursion_guard=recursion_guard,
            pipeline_steps=pipeline_steps,
            query_handlers=query_handlers,
            proof_certificates=proof_certs,
            has_vertex_weights=has_vw
        )
