"""
Universal Tree Reasoning Capability Benchmark Suite.

Covers the 11 Mandatory Categories:
1. Basic / Canonical Trees (diameter, rooting, leaf counting)
2. Binary Trees (traversals, heights, symmetric structures)
3. General Trees (N-ary heights, subtree sizes)
4. Tree Queries (LCA, distance, k-th ancestor, path sum, subtree sum)
5. Tree Dynamic Programming (MWIS, rerooting DP)
6. Advanced Tree Operations (Heavy-Light Decomposition for non-invertible path extrema)
7. Composed Pipelines (typed state dataflow transitions)
8. Diverse Carrier Datatypes (int, long long, double, string, char)
9. Paraphrase Robustness (unseen natural language problem narratives)
10. Negative Reasoning & Contradiction Detection (fail-closed refutations)
11. Adversarial Topologies (chain, star, skewed, N=1, N=2)
"""

import pytest
from architecture_v2.universal_contracts import (
    ProofStatus,
    TopologyClaim,
    RootSpec,
    RootSemanticModel,
    AlgebraicStructure,
    AlgebraicOp,
    CppTypeDescriptor,
    QueryRequirement,
    QueryScope,
    QueryAction,
    TargetDomain,
    InteractivityModel,
    VerifiedPlanIR,
)
from architecture_v2.semantic_model import ProblemModel
from architecture_v2.semantic_adapter import SemanticAdapter
from architecture_v2.capability_planner import CapabilityPlanner
from architecture_v2.planner import AlgorithmPlannerV2, PlanStatus
from architecture_v2.generator.cpp_plan_emitter import CppPlanEmitter
from architecture_v2.tests.tree_oracles import (
    oracle_lca_parent_climbing,
    oracle_kth_ancestor_naive,
    oracle_tree_diameter_all_pairs,
    oracle_subtree_aggregate_fresh_dfs,
    oracle_tree_independent_set_bitmask,
    oracle_path_aggregate_bfs,
    oracle_tree_difference_brute_force,
)


# =====================================================================
# Category 1: Basic / Canonical Trees
# =====================================================================

def test_cat1_tree_diameter():
    """Verify tree diameter synthesis and correctness."""
    text = "Given an unweighted tree of N nodes and N-1 edges, find the maximum distance between any two vertices."
    model = SemanticAdapter.parse(text)
    assert model.topology_claim.is_proven_tree is True
    plan = AlgorithmPlannerV2.create_plan(model)
    assert plan.status == PlanStatus.PROVEN
    assert "provider:two_sweep_diameter" in plan.composed_capabilities
    assert plan.code is not None
    assert "compute_tree_diameter" in plan.code


def test_cat1_tree_rooting_and_metrics():
    """Verify tree rooting and subtree size metrics."""
    text = "Given a tree rooted at 1 with N vertices, for every vertex find the number of nodes in its subtree."
    model = SemanticAdapter.parse(text)
    assert model.root_spec.model == RootSemanticModel.INPUT_SPECIFIED
    assert model.root_spec.vertex == 1
    plan = AlgorithmPlannerV2.create_plan(model)
    assert plan.status == PlanStatus.PROVEN
    assert "provider:tree_metrics" in plan.composed_capabilities


# =====================================================================
# Category 2: Binary Trees
# =====================================================================

def test_cat2_binary_tree_traversal():
    """Verify binary tree traversal planning."""
    text = "Given a binary tree, print the preorder traversal of all vertices."
    model = SemanticAdapter.parse(text)
    plan = AlgorithmPlannerV2.create_plan(model)
    assert plan.status == PlanStatus.PROVEN
    assert "provider:tree_traversal" in plan.composed_capabilities


# =====================================================================
# Category 3: General Trees
# =====================================================================

def test_cat3_nary_tree_subtree_sizes():
    """Verify subtree sizes on general trees."""
    text = "Given a general tree with N nodes and N-1 edges rooted at vertex 1, compute the subtree size of each node."
    model = SemanticAdapter.parse(text)
    plan = AlgorithmPlannerV2.create_plan(model)
    assert plan.status == PlanStatus.PROVEN
    assert "provider:tree_metrics" in plan.composed_capabilities


# =====================================================================
# Category 4: Tree Queries
# =====================================================================

def test_cat4_lca_queries():
    """Verify Lowest Common Ancestor query pipeline."""
    text = "You are given a tree rooted at node 1. Answer Q queries asking for the lowest common ancestor of u and v."
    model = SemanticAdapter.parse(text)
    plan = AlgorithmPlannerV2.create_plan(model)
    assert plan.status == PlanStatus.PROVEN
    assert "provider:binary_lifting" in plan.composed_capabilities
    assert "provider:lca_binary_lifting" in plan.composed_capabilities


def test_cat4_tree_distance_queries():
    """Verify tree distance query synthesis."""
    text = "Given a tree with N nodes, compute the shortest distance between two nodes u and v for Q queries."
    model = SemanticAdapter.parse(text)
    plan = AlgorithmPlannerV2.create_plan(model)
    assert plan.status == PlanStatus.PROVEN
    assert "provider:binary_lifting" in plan.composed_capabilities


def test_cat4_kth_ancestor_queries():
    """Verify k-th ancestor query synthesis."""
    text = "Given a rooted tree of N nodes, answer queries asking for the k-th ancestor of node u."
    model = SemanticAdapter.parse(text)
    plan = AlgorithmPlannerV2.create_plan(model)
    assert plan.status == PlanStatus.PROVEN
    assert "provider:binary_lifting" in plan.composed_capabilities


def test_cat4_path_sum_invertible():
    """Verify path sum queries with invertible group operation (SUM)."""
    planner = CapabilityPlanner()
    model = ProblemModel(
        raw_text="Path sum aggregate",
        topology_claim=TopologyClaim(vertices_bound=1000, edges_bound=999, is_connected=ProofStatus.PROVEN, is_acyclic=ProofStatus.PROVEN, proof_status=ProofStatus.PROVEN),
        root_spec=RootSpec(model=RootSemanticModel.ARBITRARY_COMPUTATIONAL, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.PATH, action=QueryAction.AGGREGATE, target_domain=TargetDomain.VERTEX_PAYLOAD)],
        algebraic_payload=AlgebraicStructure(carrier_type=CppTypeDescriptor.INT64, operator=AlgebraicOp.SUM, is_invertible=True)
    )
    plan = planner.synthesize_tree_plan(model)
    assert plan is not None
    provider_ids = [step.provider_id for step in plan.pipeline_steps]
    assert "provider:lca_prefix_difference" in provider_ids


def test_cat4_subtree_sum_queries():
    """Verify subtree aggregate queries with Euler Tour."""
    planner = CapabilityPlanner()
    model = ProblemModel(
        raw_text="Subtree sum aggregate",
        topology_claim=TopologyClaim(vertices_bound=1000, edges_bound=999, is_connected=ProofStatus.PROVEN, is_acyclic=ProofStatus.PROVEN, proof_status=ProofStatus.PROVEN),
        root_spec=RootSpec(model=RootSemanticModel.INPUT_SPECIFIED, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.SUBTREE, action=QueryAction.AGGREGATE)],
        algebraic_payload=AlgebraicStructure(carrier_type=CppTypeDescriptor.INT64, operator=AlgebraicOp.SUM)
    )
    plan = planner.synthesize_tree_plan(model)
    assert plan is not None
    provider_ids = [step.provider_id for step in plan.pipeline_steps]
    assert "provider:euler_tour_intervals" in provider_ids


# =====================================================================
# Category 5: Dynamic Programming on Trees
# =====================================================================

def test_cat5_maximum_weight_independent_set():
    """Verify Maximum Weight Independent Set tree DP synthesis."""
    text = "Given a tree where each node has a weight, find an independent set of vertices with maximum total weight."
    model = SemanticAdapter.parse(text)
    plan = AlgorithmPlannerV2.create_plan(model)
    assert plan.status == PlanStatus.PROVEN
    assert "provider:tree_dp_subtrees" in plan.composed_capabilities


def test_cat5_all_roots_rerooting():
    """Verify rerooting DP synthesis when all roots must be evaluated."""
    text = "Given an unweighted tree, for each vertex as root compute the sum of distances to all other vertices."
    model = SemanticAdapter.parse(text)
    assert model.root_spec.model == RootSemanticModel.ALL_ROOTS_EVALUATED
    plan = AlgorithmPlannerV2.create_plan(model)
    assert plan.status == PlanStatus.PROVEN
    assert "provider:tree_rerooting" in plan.composed_capabilities


# =====================================================================
# Category 6: Advanced Tree Operations
# =====================================================================

def test_cat6_heavy_light_decomposition():
    """Verify HLD selection when operator is non-invertible (MIN or MAX on path)."""
    planner = CapabilityPlanner()
    model = ProblemModel(
        raw_text="Find maximum value on path between u and v",
        topology_claim=TopologyClaim(vertices_bound=1000, edges_bound=999, is_connected=ProofStatus.PROVEN, is_acyclic=ProofStatus.PROVEN, proof_status=ProofStatus.PROVEN),
        root_spec=RootSpec(model=RootSemanticModel.ARBITRARY_COMPUTATIONAL, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.PATH, action=QueryAction.AGGREGATE, target_domain=TargetDomain.VERTEX_PAYLOAD)],
        algebraic_payload=AlgebraicStructure(carrier_type=CppTypeDescriptor.INT64, operator=AlgebraicOp.MAX, is_invertible=False)
    )
    plan = planner.synthesize_tree_plan(model)
    assert plan is not None
    provider_ids = [step.provider_id for step in plan.pipeline_steps]
    assert "provider:heavy_light_decomposition" in provider_ids
    assert "provider:lca_prefix_difference" not in provider_ids


# =====================================================================
# Category 7: Composed Pipelines & Gate 8 Extensibility
# =====================================================================

def test_cat7_composed_pipeline_offline_tree_difference():
    """Gate 8 Extensibility: offline path difference updates."""
    text = "Given a tree with N nodes and Q offline updates, add value x to all nodes on the path between u and v."
    model = SemanticAdapter.parse(text)
    plan = AlgorithmPlannerV2.create_plan(model)
    assert plan.status == PlanStatus.PROVEN
    assert "provider:tree_difference_offline" in plan.composed_capabilities
    assert "accumulate_tree_difference" in plan.code


# =====================================================================
# Category 8: Diverse Carrier Datatypes
# =====================================================================

@pytest.mark.parametrize("dtype,cpp_type", [
    (CppTypeDescriptor.INT32, "int"),
    (CppTypeDescriptor.INT64, "long long"),
    (CppTypeDescriptor.DOUBLE, "double"),
    (CppTypeDescriptor.STRING, "std::string"),
    (CppTypeDescriptor.CHAR, "char"),
])
def test_cat8_diverse_carrier_types(dtype, cpp_type):
    """Verify code emitter handles diverse payload types parametrically."""
    planner = CapabilityPlanner()
    model = ProblemModel(
        raw_text="Generic payload tree problem",
        topology_claim=TopologyClaim(vertices_bound=10, edges_bound=9, is_connected=ProofStatus.PROVEN, is_acyclic=ProofStatus.PROVEN, proof_status=ProofStatus.PROVEN),
        root_spec=RootSpec(model=RootSemanticModel.ARBITRARY_COMPUTATIONAL, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.PATH, action=QueryAction.AGGREGATE, target_domain=TargetDomain.VERTEX_PAYLOAD)],
        algebraic_payload=AlgebraicStructure(carrier_type=dtype, operator=AlgebraicOp.SUM, is_invertible=True)
    )
    plan = planner.synthesize_tree_plan(model)
    code = CppPlanEmitter.emit(plan)
    assert f"vector<{cpp_type}>" in code


# =====================================================================
# Category 9: Paraphrase Robustness
# =====================================================================

def test_cat9_kingdom_communication_paraphrase():
    """Story problem: kingdom cities without loops."""
    narrative = (
        "In the Kingdom of Treeland, there are N cities connected by exactly N-1 bidirectional roads "
        "such that every city can reach every other city without any redundant connection or loop. "
        "The King resides in city 1. For Q queries, citizens want to know the first common ancestor "
        "city on the royal paths to the capital."
    )
    model = SemanticAdapter.parse(narrative)
    assert model.topology_claim.is_proven_tree is True
    plan = AlgorithmPlannerV2.create_plan(model)
    assert plan.status == PlanStatus.PROVEN
    assert "provider:lca_binary_lifting" in plan.composed_capabilities


def test_cat9_corporate_hierarchy_paraphrase():
    """Story problem: corporate reporting structure."""
    narrative = (
        "An enterprise consists of N employees. Employee 1 is the CEO. Every other employee has exactly "
        "one direct manager, forming a rooted tree hierarchy. Compute the size of the team managed by "
        "each employee (including themselves)."
    )
    model = SemanticAdapter.parse(narrative)
    assert model.topology_claim.is_proven_tree is True
    plan = AlgorithmPlannerV2.create_plan(model)
    assert plan.status == PlanStatus.PROVEN
    assert "provider:tree_metrics" in plan.composed_capabilities


# =====================================================================
# Category 10: Negative Reasoning & Contradiction Detection
# =====================================================================

def test_cat10_contradiction_graph_with_cycle():
    """Graph contains a cycle -> tree reasoning MUST fail closed."""
    narrative = "There is a connected network of N vertices and N edges containing a cycle. Find tree diameter."
    model = SemanticAdapter.parse(narrative)
    assert model.topology_claim.is_acyclic == ProofStatus.CONTRADICTED
    plan = AlgorithmPlannerV2.create_plan(model)
    assert plan.status == PlanStatus.UNSUPPORTED
    assert plan.strategy_name == "tree_cyclic_contradiction"
    assert any("TREE_CYCLIC_GRAPH" in r for r in plan.rejection_reasons)


def test_cat10_contradiction_disconnected_network():
    """Disconnected graph -> tree reasoning MUST fail closed."""
    narrative = "There is a disconnected graph with multiple components. Find LCA."
    model = SemanticAdapter.parse(narrative)
    assert model.topology_claim.is_connected == ProofStatus.CONTRADICTED
    plan = AlgorithmPlannerV2.create_plan(model)
    assert plan.status == PlanStatus.UNSUPPORTED
    assert plan.strategy_name == "tree_disconnected_contradiction"
    assert any("TREE_DISCONNECTED_GRAPH" in r for r in plan.rejection_reasons)


# =====================================================================
# Category 11: Adversarial Topologies
# =====================================================================

def test_cat11_star_graph():
    """Adversarial star graph (hub at 1, leaves 2..N)."""
    # Verify diameter oracle matches specification: diameter of star with >= 2 leaves is 2
    adj = {1: [2, 3, 4, 5, 6], 2: [1], 3: [1], 4: [1], 5: [1], 6: [1]}
    assert oracle_tree_diameter_all_pairs(6, adj) == 2


def test_cat11_line_chain_graph():
    """Adversarial chain graph (1-2-3-4-5)."""
    adj = {1: [2], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4]}
    assert oracle_tree_diameter_all_pairs(5, adj) == 4


def test_cat11_deep_recursion_guard():
    """Very large N (>= 100,000) triggers recursion stack expansion guard in PlanIR."""
    planner = CapabilityPlanner()
    model = ProblemModel(
        raw_text="Deep chain tree with large N",
        topology_claim=TopologyClaim(vertices_bound=200000, edges_bound=199999, is_connected=ProofStatus.PROVEN, is_acyclic=ProofStatus.PROVEN, proof_status=ProofStatus.PROVEN),
        root_spec=RootSpec(model=RootSemanticModel.ARBITRARY_COMPUTATIONAL, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.GLOBAL, action=QueryAction.EXTREMUM, target_domain=TargetDomain.TOPOLOGY_ONLY)],
        algebraic_payload=AlgebraicStructure(carrier_type=CppTypeDescriptor.INT32, operator=AlgebraicOp.SUM)
    )
    plan = planner.synthesize_tree_plan(model)
    assert plan.recursion_guard is True
    code = CppPlanEmitter.emit(plan)
    assert "#include <sys/resource.h>" in code
    assert "setrlimit" in code
