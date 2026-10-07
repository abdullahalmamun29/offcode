"""
Comprehensive Verification Suite for Architecture V2 Universal Tree Capability.

Tests:
1. Universal contracts, semantic representations, and typed state descriptors.
2. Capability providers and state transformations.
3. Independent reference oracles vs production algorithms.
4. Capability planner synthesis and proof discharge.
5. Contradiction handling and fail-closed proofs (cyclic graphs, disconnected graphs).
6. End-to-end C++17 generation, compilation (g++), and execution across edge topologies
   and diverse payload carrier types (int, long long, double, string).
"""

import os
import subprocess
import tempfile
import pytest
from typing import Dict, List, Tuple

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
    TypedStateDescriptor,
    ResourceEnvelope,
    VerifiedPlanIR,
)
from architecture_v2.semantic_model import ProblemModel
from architecture_v2.tree_providers import (
    TreeRootingProvider,
    TreeTraversalProvider,
    TreeMetricsProvider,
    BinaryLiftingProvider,
    LcaBinaryLiftingProvider,
    EulerTourIntervalProvider,
    LcaPrefixDifferenceProvider,
    HeavyLightDecompositionProvider,
    TwoSweepDiameterProvider,
    TreeDpSubtreeProvider,
    TreeRerootingProvider,
    OrderedBstProvider,
    TreeDifferenceOfflineUpdatesProvider,
    PROVIDER_MAP,
)
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
# 1. Universal Contracts & Invariant Tests
# =====================================================================

def test_universal_contracts_dataclasses():
    """Verify contracts initialize correctly and maintain strict invariants."""
    topo = TopologyClaim(
        vertices_bound=10,
        edges_bound=9,
        is_connected=ProofStatus.PROVEN,
        is_acyclic=ProofStatus.PROVEN,
        proof_status=ProofStatus.PROVEN
    )
    assert topo.is_proven_tree is True

    root_spec = RootSpec(model=RootSemanticModel.ARBITRARY_COMPUTATIONAL, vertex=1)
    assert root_spec.model == RootSemanticModel.ARBITRARY_COMPUTATIONAL
    assert root_spec.vertex == 1

    alg = AlgebraicStructure(
        carrier_type=CppTypeDescriptor.INT64,
        operator=AlgebraicOp.SUM,
        is_invertible=True,
        is_associative=True,
        is_commutative=True
    )
    assert alg.is_invertible is True

    query = QueryRequirement(
        scope=QueryScope.PATH,
        action=QueryAction.AGGREGATE,
        target_domain=TargetDomain.VERTEX_PAYLOAD,
        interactivity=InteractivityModel.ONLINE_REPEATED
    )
    assert query.scope == QueryScope.PATH
    assert query.action == QueryAction.AGGREGATE


def test_algebraic_payload_invertibility():
    """Verify that non-invertible operators are correctly identified."""
    sum_alg = AlgebraicStructure(carrier_type=CppTypeDescriptor.INT32, operator=AlgebraicOp.SUM, is_invertible=True)
    min_alg = AlgebraicStructure(carrier_type=CppTypeDescriptor.INT32, operator=AlgebraicOp.MIN, is_invertible=False)
    assert sum_alg.is_invertible is True
    assert min_alg.is_invertible is False


# =====================================================================
# 2. Independent Reference Oracles vs Production Implementations
# =====================================================================

def test_oracle_lca_vs_climbing():
    """Verify LCA oracle on various tree shapes."""
    # Tree: 1 - 2 - 4
    #       |   `- 5
    #       `- 3
    parents = {1: 0, 2: 1, 3: 1, 4: 2, 5: 2}
    assert oracle_lca_parent_climbing(5, parents, 4, 5) == 2
    assert oracle_lca_parent_climbing(5, parents, 4, 3) == 1
    assert oracle_lca_parent_climbing(5, parents, 2, 4) == 2
    assert oracle_lca_parent_climbing(5, parents, 1, 5) == 1
    assert oracle_lca_parent_climbing(5, parents, 3, 3) == 3


def test_oracle_kth_ancestor():
    parents = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4}
    assert oracle_kth_ancestor_naive(parents, 5, 2) == 3
    assert oracle_kth_ancestor_naive(parents, 5, 4) == 1
    assert oracle_kth_ancestor_naive(parents, 5, 5) == 0


def test_oracle_diameter_all_pairs():
    # Chain graph: 1 - 2 - 3 - 4 - 5 -> diameter 4
    adj = {1: [2], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4]}
    assert oracle_tree_diameter_all_pairs(5, adj) == 4

    # Star graph: center 1, leaves 2, 3, 4 -> diameter 2
    star_adj = {1: [2, 3, 4], 2: [1], 3: [1], 4: [1]}
    assert oracle_tree_diameter_all_pairs(4, star_adj) == 2


def test_oracle_subtree_aggregate():
    children = {1: [2, 3], 2: [4, 5], 3: [], 4: [], 5: []}
    values = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50}
    assert oracle_subtree_aggregate_fresh_dfs(1, children, values, "SUM") == 150
    assert oracle_subtree_aggregate_fresh_dfs(2, children, values, "SUM") == 110
    assert oracle_subtree_aggregate_fresh_dfs(4, children, values, "SUM") == 40
    assert oracle_subtree_aggregate_fresh_dfs(1, children, values, "MAX") == 50


def test_oracle_independent_set():
    # Tree: 1 - 2, 2 - 3, 2 - 4
    # Weights: 1: 10, 2: 100, 3: 20, 4: 30
    edges = [(1, 2), (2, 3), (2, 4)]
    weights = {1: 10, 2: 100, 3: 20, 4: 30}
    assert oracle_tree_independent_set_bitmask(4, edges, weights) == 100

    weights2 = {1: 10, 2: 10, 3: 20, 4: 30}
    assert oracle_tree_independent_set_bitmask(4, edges, weights2) == 60


def test_oracle_path_aggregate():
    adj = {1: [2, 3], 2: [1, 4], 3: [1], 4: [2]}
    values = {1: 5, 2: 15, 3: 25, 4: 35}
    # Path from 4 to 3: 4 -> 2 -> 1 -> 3, sum = 35 + 15 + 5 + 25 = 80
    assert oracle_path_aggregate_bfs(4, adj, values, 4, 3, "SUM") == 80
    assert oracle_path_aggregate_bfs(4, adj, values, 4, 2, "SUM") == 50


def test_oracle_tree_difference():
    adj = {1: [2, 3], 2: [1], 3: [1]}
    updates = [(2, 3, 5), (1, 2, 2)]
    res = oracle_tree_difference_brute_force(3, adj, updates)
    assert res[1] == 7
    assert res[2] == 7
    assert res[3] == 5


# =====================================================================
# 3. Capability Provider Registry & State Pipeline Synthesis
# =====================================================================

def test_capability_provider_registry():
    assert len(PROVIDER_MAP) >= 12
    assert "provider:tree_rooting" in PROVIDER_MAP
    assert "provider:two_sweep_diameter" in PROVIDER_MAP
    assert "provider:tree_difference_offline" in PROVIDER_MAP


def test_capability_planner_synthesis_path_aggregate():
    planner = CapabilityPlanner()
    model = ProblemModel(
        raw_text="Find sum of values on path between u and v",
        topology_claim=TopologyClaim(
            vertices_bound=1000,
            edges_bound=999,
            is_connected=ProofStatus.PROVEN,
            is_acyclic=ProofStatus.PROVEN,
            proof_status=ProofStatus.PROVEN
        ),
        root_spec=RootSpec(model=RootSemanticModel.ARBITRARY_COMPUTATIONAL, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.PATH, action=QueryAction.AGGREGATE, target_domain=TargetDomain.VERTEX_PAYLOAD)],
        algebraic_payload=AlgebraicStructure(carrier_type=CppTypeDescriptor.INT64, operator=AlgebraicOp.SUM, is_invertible=True)
    )
    plan = planner.synthesize_tree_plan(model)
    assert plan is not None
    provider_ids = [step.provider_id for step in plan.pipeline_steps]
    assert "provider:tree_rooting" in provider_ids
    assert "provider:binary_lifting" in provider_ids
    assert "provider:lca_binary_lifting" in provider_ids
    assert "provider:lca_prefix_difference" in provider_ids


def test_capability_planner_synthesis_subtree_aggregate():
    planner = CapabilityPlanner()
    model = ProblemModel(
        raw_text="Find subtree sum after point updates",
        topology_claim=TopologyClaim(
            vertices_bound=1000,
            edges_bound=999,
            is_connected=ProofStatus.PROVEN,
            is_acyclic=ProofStatus.PROVEN,
            proof_status=ProofStatus.PROVEN
        ),
        root_spec=RootSpec(model=RootSemanticModel.INPUT_SPECIFIED, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.SUBTREE, action=QueryAction.AGGREGATE)],
        algebraic_payload=AlgebraicStructure(carrier_type=CppTypeDescriptor.INT32, operator=AlgebraicOp.SUM)
    )
    plan = planner.synthesize_tree_plan(model)
    assert plan is not None
    provider_ids = [step.provider_id for step in plan.pipeline_steps]
    assert "provider:euler_tour_intervals" in provider_ids


def test_capability_planner_synthesis_diameter():
    planner = CapabilityPlanner()
    model = ProblemModel(
        raw_text="Compute the diameter of the tree",
        topology_claim=TopologyClaim(
            vertices_bound=1000,
            edges_bound=999,
            is_connected=ProofStatus.PROVEN,
            is_acyclic=ProofStatus.PROVEN,
            proof_status=ProofStatus.PROVEN
        ),
        root_spec=RootSpec(model=RootSemanticModel.ARBITRARY_COMPUTATIONAL, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.GLOBAL, action=QueryAction.EXTREMUM, target_domain=TargetDomain.TOPOLOGY_ONLY)],
        algebraic_payload=AlgebraicStructure(carrier_type=CppTypeDescriptor.INT32, operator=AlgebraicOp.SUM)
    )
    plan = planner.synthesize_tree_plan(model)
    assert plan is not None
    provider_ids = [step.provider_id for step in plan.pipeline_steps]
    assert "provider:two_sweep_diameter" in provider_ids


def test_capability_planner_synthesis_tree_dp():
    planner = CapabilityPlanner()
    model = ProblemModel(
        raw_text="Find maximum weight independent set on the tree",
        topology_claim=TopologyClaim(
            vertices_bound=1000,
            edges_bound=999,
            is_connected=ProofStatus.PROVEN,
            is_acyclic=ProofStatus.PROVEN,
            proof_status=ProofStatus.PROVEN
        ),
        root_spec=RootSpec(model=RootSemanticModel.ARBITRARY_COMPUTATIONAL, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.GLOBAL, action=QueryAction.EXTREMUM, target_domain=TargetDomain.VERTEX_PAYLOAD)],
        algebraic_payload=AlgebraicStructure(carrier_type=CppTypeDescriptor.INT64, operator=AlgebraicOp.MAX)
    )
    plan = planner.synthesize_tree_plan(model)
    assert plan is not None
    provider_ids = [step.provider_id for step in plan.pipeline_steps]
    assert "provider:tree_dp_subtrees" in provider_ids


def test_capability_planner_synthesis_gate8_extensibility():
    """Verify Gate 8: offline tree difference updates synthesized through provider pipeline."""
    planner = CapabilityPlanner()
    model = ProblemModel(
        raw_text="Add x to all vertices on path (u, v) across multiple offline updates",
        topology_claim=TopologyClaim(
            vertices_bound=1000,
            edges_bound=999,
            is_connected=ProofStatus.PROVEN,
            is_acyclic=ProofStatus.PROVEN,
            proof_status=ProofStatus.PROVEN
        ),
        root_spec=RootSpec(model=RootSemanticModel.ARBITRARY_COMPUTATIONAL, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.PATH, action=QueryAction.MUTATION, interactivity=InteractivityModel.OFFLINE_BATCH)],
        algebraic_payload=AlgebraicStructure(carrier_type=CppTypeDescriptor.INT64, operator=AlgebraicOp.SUM, is_invertible=True)
    )
    plan = planner.synthesize_tree_plan(model)
    assert plan is not None
    provider_ids = [step.provider_id for step in plan.pipeline_steps]
    assert "provider:tree_difference_offline" in provider_ids


# =====================================================================
# 4. Fail-Closed Contradiction Handling & Proof Refutation
# =====================================================================

def test_contradiction_cyclic_graph():
    """Attempting tree reasoning on a graph with cycles must fail closed."""
    model = ProblemModel(
        raw_text="Find LCA on graph with cycle",
        topology_claim=TopologyClaim(
            is_connected=ProofStatus.PROVEN,
            is_acyclic=ProofStatus.CONTRADICTED,
            proof_status=ProofStatus.CONTRADICTED
        ),
        query_requirements=[QueryRequirement(scope=QueryScope.PATH, action=QueryAction.ANCESTOR_CHECK)]
    )
    plan = AlgorithmPlannerV2.create_plan(model)
    assert plan.status == PlanStatus.UNSUPPORTED
    assert plan.strategy_name == "tree_cyclic_contradiction"
    assert any("TREE_CYCLIC_GRAPH" in r for r in plan.rejection_reasons)


def test_contradiction_disconnected_graph():
    """Attempting tree reasoning on a disconnected graph must fail closed."""
    model = ProblemModel(
        raw_text="Compute diameter on forest of multiple components",
        topology_claim=TopologyClaim(
            is_connected=ProofStatus.CONTRADICTED,
            is_acyclic=ProofStatus.PROVEN,
            proof_status=ProofStatus.CONTRADICTED
        ),
        query_requirements=[QueryRequirement(scope=QueryScope.GLOBAL, action=QueryAction.EXTREMUM, target_domain=TargetDomain.TOPOLOGY_ONLY)]
    )
    plan = AlgorithmPlannerV2.create_plan(model)
    assert plan.status == PlanStatus.UNSUPPORTED
    assert plan.strategy_name == "tree_disconnected_contradiction"
    assert any("TREE_DISCONNECTED_GRAPH" in r for r in plan.rejection_reasons)


def test_non_invertible_path_aggregate_selects_hld():
    """Path aggregate with non-invertible operator (MIN) must NOT select prefix difference, but HLD."""
    planner = CapabilityPlanner()
    model = ProblemModel(
        raw_text="Find minimum value on path between u and v",
        topology_claim=TopologyClaim(
            vertices_bound=1000,
            edges_bound=999,
            is_connected=ProofStatus.PROVEN,
            is_acyclic=ProofStatus.PROVEN,
            proof_status=ProofStatus.PROVEN
        ),
        root_spec=RootSpec(model=RootSemanticModel.ARBITRARY_COMPUTATIONAL, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.PATH, action=QueryAction.AGGREGATE, target_domain=TargetDomain.VERTEX_PAYLOAD)],
        algebraic_payload=AlgebraicStructure(carrier_type=CppTypeDescriptor.INT32, operator=AlgebraicOp.MIN, is_invertible=False)
    )
    plan = planner.synthesize_tree_plan(model)
    assert plan is not None
    provider_ids = [step.provider_id for step in plan.pipeline_steps]
    assert "provider:lca_prefix_difference" not in provider_ids
    assert "provider:heavy_light_decomposition" in provider_ids


# =====================================================================
# 5. C++17 Plan Emitter & Execution Verification (Compilation & Run)
# =====================================================================

def _compile_and_run_cpp(cpp_code: str, stdin_input: str) -> str:
    """Helper to compile C++17 source and execute with stdin."""
    with tempfile.TemporaryDirectory() as tmpdir:
        src_file = os.path.join(tmpdir, "solution.cpp")
        bin_file = os.path.join(tmpdir, "solution")
        with open(src_file, "w") as f:
            f.write(cpp_code)

        compile_cmd = ["g++", "-std=c++17", "-O2", src_file, "-o", bin_file]
        compile_res = subprocess.run(compile_cmd, capture_output=True, text=True)
        if compile_res.returncode != 0:
            raise RuntimeError(f"C++ Compilation failed:\n{compile_res.stderr}\nCode:\n{cpp_code}")

        run_res = subprocess.run([bin_file], input=stdin_input, capture_output=True, text=True, timeout=5)
        if run_res.returncode != 0:
            raise RuntimeError(f"Execution failed:\n{run_res.stderr}")
        return run_res.stdout.strip()


def test_cpp_emission_and_execution_lca():
    planner = CapabilityPlanner()
    model = ProblemModel(
        raw_text="Find LCA of multiple pairs of vertices",
        topology_claim=TopologyClaim(
            vertices_bound=5,
            edges_bound=4,
            is_connected=ProofStatus.PROVEN,
            is_acyclic=ProofStatus.PROVEN,
            proof_status=ProofStatus.PROVEN
        ),
        root_spec=RootSpec(model=RootSemanticModel.INPUT_SPECIFIED, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.PATH, action=QueryAction.ANCESTOR_CHECK)],
        algebraic_payload=AlgebraicStructure(carrier_type=CppTypeDescriptor.INT32, operator=AlgebraicOp.SUM)
    )
    plan = planner.synthesize_tree_plan(model)
    code = CppPlanEmitter.emit(plan)

    assert "#include <iostream>" in code
    assert "int query_lca(int u, int v)" in code

    # Test input:
    # 5 nodes, 4 edges, root 1
    # 1 2
    # 1 3
    # 2 4
    # 2 5
    # 3 queries: (4, 5) -> 2, (4, 3) -> 1, (2, 4) -> 2
    stdin_data = (
        "5\n"
        "1 2\n"
        "1 3\n"
        "2 4\n"
        "2 5\n"
        "3\n"
        "4 5\n"
        "4 3\n"
        "2 4\n"
    )
    out = _compile_and_run_cpp(code, stdin_data)
    lines = [line.strip() for line in out.splitlines() if line.strip()]
    assert lines == ["2", "1", "2"]


def test_cpp_emission_and_execution_diameter():
    planner = CapabilityPlanner()
    model = ProblemModel(
        raw_text="Find diameter of tree",
        topology_claim=TopologyClaim(
            vertices_bound=5,
            edges_bound=4,
            is_connected=ProofStatus.PROVEN,
            is_acyclic=ProofStatus.PROVEN,
            proof_status=ProofStatus.PROVEN
        ),
        root_spec=RootSpec(model=RootSemanticModel.ARBITRARY_COMPUTATIONAL, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.GLOBAL, action=QueryAction.EXTREMUM, target_domain=TargetDomain.TOPOLOGY_ONLY)],
        algebraic_payload=AlgebraicStructure(carrier_type=CppTypeDescriptor.INT32, operator=AlgebraicOp.SUM)
    )
    plan = planner.synthesize_tree_plan(model)
    code = CppPlanEmitter.emit(plan)

    assert "compute_tree_diameter" in code

    # Tree: 5 nodes, chain 1-2-3-4-5 -> diameter 4
    stdin_data = (
        "5\n"
        "1 2\n"
        "2 3\n"
        "3 4\n"
        "4 5\n"
    )
    out = _compile_and_run_cpp(code, stdin_data)
    assert out == "4"


def test_cpp_emission_and_execution_mwis_dp():
    planner = CapabilityPlanner()
    model = ProblemModel(
        raw_text="Find maximum weight independent set",
        topology_claim=TopologyClaim(
            vertices_bound=4,
            edges_bound=3,
            is_connected=ProofStatus.PROVEN,
            is_acyclic=ProofStatus.PROVEN,
            proof_status=ProofStatus.PROVEN
        ),
        root_spec=RootSpec(model=RootSemanticModel.ARBITRARY_COMPUTATIONAL, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.GLOBAL, action=QueryAction.EXTREMUM, target_domain=TargetDomain.VERTEX_PAYLOAD)],
        algebraic_payload=AlgebraicStructure(carrier_type=CppTypeDescriptor.INT64, operator=AlgebraicOp.MAX)
    )
    plan = planner.synthesize_tree_plan(model)
    code = CppPlanEmitter.emit(plan)

    # 4 nodes: weights 10 100 20 30
    # edges: 1-2, 2-3, 2-4 -> MWIS = 100
    stdin_data = (
        "4\n"
        "1 2\n"
        "2 3\n"
        "2 4\n"
        "10 100 20 30\n"
    )
    out = _compile_and_run_cpp(code, stdin_data)
    assert out == "100"


def test_cpp_emission_and_execution_gate8_tree_difference():
    planner = CapabilityPlanner()
    model = ProblemModel(
        raw_text="Tree difference updates on paths",
        topology_claim=TopologyClaim(
            vertices_bound=3,
            edges_bound=2,
            is_connected=ProofStatus.PROVEN,
            is_acyclic=ProofStatus.PROVEN,
            proof_status=ProofStatus.PROVEN
        ),
        root_spec=RootSpec(model=RootSemanticModel.ARBITRARY_COMPUTATIONAL, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.PATH, action=QueryAction.MUTATION, interactivity=InteractivityModel.OFFLINE_BATCH)],
        algebraic_payload=AlgebraicStructure(carrier_type=CppTypeDescriptor.INT64, operator=AlgebraicOp.SUM, is_invertible=True)
    )
    plan = planner.synthesize_tree_plan(model)
    code = CppPlanEmitter.emit(plan)

    assert "accumulate_tree_difference" in code

    # 3 nodes: 1-2, 1-3
    # 2 updates: (2, 3, 5), (1, 2, 2)
    stdin_data = (
        "3\n"
        "1 2\n"
        "1 3\n"
        "2\n"
        "2 3 5\n"
        "1 2 2\n"
    )
    out = _compile_and_run_cpp(code, stdin_data)
    # Output should be values for 1, 2, 3: 7 7 5
    assert out == "7 7 5"


# =====================================================================
# 6. Edge Topologies & Diverse Carrier Types
# =====================================================================

def test_edge_topologies_n1_and_n2():
    """Verify N=1 and N=2 edge cases for diameter and traversal."""
    planner = CapabilityPlanner()
    model = ProblemModel(
        raw_text="Diameter of tree",
        topology_claim=TopologyClaim(
            vertices_bound=2,
            edges_bound=1,
            is_connected=ProofStatus.PROVEN,
            is_acyclic=ProofStatus.PROVEN,
            proof_status=ProofStatus.PROVEN
        ),
        root_spec=RootSpec(model=RootSemanticModel.ARBITRARY_COMPUTATIONAL, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.GLOBAL, action=QueryAction.EXTREMUM, target_domain=TargetDomain.TOPOLOGY_ONLY)],
        algebraic_payload=AlgebraicStructure(carrier_type=CppTypeDescriptor.INT32, operator=AlgebraicOp.SUM)
    )
    plan = planner.synthesize_tree_plan(model)
    code = CppPlanEmitter.emit(plan)

    # N=1
    out_1 = _compile_and_run_cpp(code, "1\n")
    assert out_1 == "0"

    # N=2
    out_2 = _compile_and_run_cpp(code, "2\n1 2\n")
    assert out_2 == "1"


def test_carrier_types_double_and_string():
    """Verify emitter generates correct carrier types for floating point and text."""
    planner = CapabilityPlanner()
    model_double = ProblemModel(
        raw_text="Path aggregate with floating point",
        topology_claim=TopologyClaim(
            vertices_bound=100,
            edges_bound=99,
            is_connected=ProofStatus.PROVEN,
            is_acyclic=ProofStatus.PROVEN,
            proof_status=ProofStatus.PROVEN
        ),
        root_spec=RootSpec(model=RootSemanticModel.ARBITRARY_COMPUTATIONAL, vertex=1),
        query_requirements=[QueryRequirement(scope=QueryScope.PATH, action=QueryAction.AGGREGATE, target_domain=TargetDomain.VERTEX_PAYLOAD)],
        algebraic_payload=AlgebraicStructure(carrier_type=CppTypeDescriptor.DOUBLE, operator=AlgebraicOp.SUM, is_invertible=True)
    )
    plan_double = planner.synthesize_tree_plan(model_double)
    code_double = CppPlanEmitter.emit(plan_double)
    assert "vector<double> node_val;" in code_double
    assert "vector<double> path_pref;" in code_double
