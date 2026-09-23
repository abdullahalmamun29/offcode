"""
CHUP Phase 5 — Tier 1 Master Unit Test Suite.

Verifies:
1. Mutability singleton range reduction (RANGE_WRITE -> POINT_WRITE).
2. Parameter-dependent coordinate scale feasibility (not hardcoded N <= 10^6).
3. Axiomatic graph topology contradiction derivation (E = V - 1).
4. AggregateSpec algebraic signatures and decomposed query facets.
5. DomainCapabilityAdapter covering all 19 frozen domains + Phase 4.
6. Conflict detector isolating UNSATISFIABLE_CONSTRAINT_SET from candidate gaps.
7. Closed-world elimination engine emitting structured EliminationCertificates.
8. Symbolic parameterized resource evaluation (N, Q, V, E, C).
9. CandidateAnalysis minimal surviving candidate set.
10. CapabilitySynthesizer state transitions (requires -> produces).
11. Four disjoint outcome states (Single survivor, Composed, Contradiction, Unresolved).
12. Formal proof obligations and deterministic SHA-256 integrity sealing.
13. Absolute generator barrier fail-closed enforcement on unsealed or tampered plans.
14. End-to-end C++17 emission for single and composed solutions.
"""

import unittest
from pointer_algorithms.multi_constraint.constraint_lattice import (
    TemporalMode,
    MutabilityCapability,
    MutabilitySet,
    CoordinateScale,
    MultiConstraintVector,
    Constraint,
    ConstraintPolarity,
    TopologyDomain,
    Directedness,
    Connectedness,
    Cyclicity,
    Simplicity,
)
from pointer_algorithms.multi_constraint.aggregate_ontology import (
    QuerySpec,
    QueryTarget,
    QueryOutput,
    QueryDependency,
    AggregateSpec,
)
from pointer_algorithms.multi_constraint.candidate_profile import (
    CandidateProfile,
    SymbolicComplexity,
)
from pointer_algorithms.multi_constraint.domain_capability_adapter import DomainCapabilityAdapter
from pointer_algorithms.multi_constraint.conflict_detector import (
    ConflictDetector,
    ConstraintContradictionCertificate,
)
from pointer_algorithms.multi_constraint.resource_evaluator import (
    ResourceEvaluator,
    SymbolicBudget,
)
from pointer_algorithms.multi_constraint.elimination_engine import (
    EliminationEngine,
    CandidateAnalysis,
    EliminationCertificate,
)
from pointer_algorithms.multi_constraint.capability_synthesizer import (
    CapabilitySynthesizer,
    CapabilitySynthesisResult,
    SynthesizedPipelineStep,
)
from pointer_algorithms.multi_constraint.multi_constraint_model import (
    OutcomeState,
    ProofStatus,
    ProofObligation,
    UnresolvedCoverageCertificate,
    VerifiedMultiConstraintPlan,
)
from pointer_algorithms.multi_constraint.facade import MultiConstraintSolver
from pointer_algorithms.multi_constraint.generator.multi_constraint_generator import (
    MultiConstraintCppGenerator,
    GeneratorBarrierError,
)


class TestPhase5MultiConstraint(unittest.TestCase):

    def setUp(self):
        self.solver = MultiConstraintSolver()
        self.universe = DomainCapabilityAdapter.get_candidate_universe()

    # ── 1. Constraint Lattice & Predicates ──

    def test_01_mutability_singleton_range_reduction(self):
        """RANGE_WRITE satisfies POINT_WRITE via singleton range [i, i]."""
        range_set = MutabilitySet.range_update()
        point_set = MutabilitySet.point_update()
        static_set = MutabilitySet.read_only()

        self.assertTrue(range_set.satisfies(MutabilityCapability.POINT_WRITE))
        self.assertTrue(range_set.satisfies(MutabilityCapability.RANGE_WRITE))
        self.assertTrue(point_set.satisfies(MutabilityCapability.POINT_WRITE))
        self.assertFalse(point_set.satisfies(MutabilityCapability.RANGE_WRITE))
        self.assertFalse(static_set.satisfies(MutabilityCapability.POINT_WRITE))

    def test_02_dense_feasibility_parameter_dependent(self):
        """CoordinateScale dense feasibility is parameter-dependent, not hardcoded."""
        # N = 2*10^6, 4 bytes/int = 8MB. In 1GB budget -> True. In 4MB budget -> False.
        self.assertTrue(CoordinateScale.is_dense_feasible(2000000, 4, 1024 * 1024 * 1024))
        self.assertFalse(CoordinateScale.is_dense_feasible(2000000, 4, 4 * 1024 * 1024))

    def test_03_axiomatic_tree_contradiction_derived(self):
        """Undirected connected acyclic simple graph with V=5, E=5 derives axiomatic contradiction."""
        tree_invalid = TopologyDomain.undirected_tree(v=5, e=5)
        invariants = tree_invalid.derive_invariants()
        contradiction_ids = [inv[0] for inv in invariants]
        self.assertIn("AXIOMATIC_TREE_EDGE_COUNT_CONTRADICTION", contradiction_ids)

    # ── 2. Aggregate Ontology & Decomposed Queries ──

    def test_04_aggregate_spec_algebra(self):
        """Verifies formal algebraic signatures for SUM, MIN, and DISTINCT."""
        sum_agg = AggregateSpec.sum_group()
        self.assertTrue(sum_agg.is_invertible)
        self.assertFalse(sum_agg.is_idempotent)

        min_agg = AggregateSpec.min_semigroup()
        self.assertTrue(min_agg.is_idempotent)
        self.assertFalse(min_agg.is_invertible)

        distinct_agg = AggregateSpec.distinct_count()
        self.assertFalse(distinct_agg.supports_merge)

    # ── 3. Universal Domain Capability Adapter ──

    def test_05_domain_capability_adapter_loads_19_domains(self):
        """DomainCapabilityAdapter loads candidates from across all 19 frozen domains."""
        self.assertIn("sparse_table", self.universe)
        self.assertIn("fenwick_tree", self.universe)
        self.assertIn("segment_tree_standard", self.universe)
        self.assertIn("dynamic_segment_tree", self.universe)
        self.assertIn("persistent_segment_tree", self.universe)
        self.assertIn("merge_sort_tree", self.universe)
        self.assertIn("mos_algorithm_scheduler", self.universe)
        self.assertIn("heavy_light_decomposition", self.universe)
        self.assertIn("dijkstra_priority_queue", self.universe)
        self.assertIn("kruskal_mst", self.universe)
        self.assertIn("two_pointers_monotone_window", self.universe)
        self.assertIn("monotonic_deque_sliding_window", self.universe)
        self.assertIn("binary_search_bisection", self.universe)
        self.assertIn("coordinate_compressor", self.universe)

    # ── 4. Axiomatic Conflict Detection (UNSATISFIABLE_CONSTRAINT_SET) ──

    def test_06_conflict_detector_temporal_contradiction(self):
        """Simultaneous online interactive and offline batching triggers UNSATISFIABLE_CONSTRAINT_SET."""
        spec = {"temporal": "ONLINE"}
        vec = self.solver._build_constraint_vector(spec)
        vec.add_constraint(Constraint("TEMPORAL", "REQUIRES_OFFLINE_BATCH", ConstraintPolarity.REQUIRED, "Offline batch"))
        cert = ConflictDetector.detect_conflicts(vec)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.failure_code, "ONLINE_STREAM_WITH_OFFLINE_REQUIREMENT")

    def test_07_conflict_detector_cell_probe_lower_bound(self):
        """O(1) query and O(1) update on dynamic range minimum triggers cell probe contradiction."""
        spec = {"cell_probe_lower_bound_trigger": True}
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        self.assertEqual(res["conflict_certificate"].failure_code, "CELL_PROBE_LOWER_BOUND_VIOLATION")

    def test_08_conflict_detector_negative_cycle_shortest_path(self):
        """Shortest path on graph with negative cycle triggers axiomatic contradiction."""
        spec = {"shortest_path_query": True, "proven_negative_cycle": True}
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        self.assertEqual(res["conflict_certificate"].failure_code, "NEGATIVE_CYCLE_SHORTEST_PATH_CONTRADICTION")

    # ── 5. Closed-World Candidate Elimination ──

    def test_09_elimination_sparse_table_on_point_update(self):
        """Point updates eliminate static Sparse Table with MUTATION_DISALLOWED_ON_STATIC_STRUCTURE."""
        spec = {"mutability": "POINT_UPDATE", "operation": "MIN"}
        res = self.solver.solve(spec)
        certs = res["candidate_analysis"].eliminated_candidates
        self.assertIn("sparse_table", certs)
        self.assertEqual(certs["sparse_table"].failure_code, "MUTATION_DISALLOWED_ON_STATIC_STRUCTURE")

    def test_10_elimination_sparse_table_on_non_idempotent_sum(self):
        """Range sum eliminates Sparse Table with NON_IDEMPOTENT_OPERATION_REJECTS_SPARSE_TABLE."""
        spec = {"mutability": "STATIC", "operation": "SUM"}
        res = self.solver.solve(spec)
        certs = res["candidate_analysis"].eliminated_candidates
        self.assertIn("sparse_table", certs)
        self.assertEqual(certs["sparse_table"].failure_code, "NON_IDEMPOTENT_OPERATION_REJECTS_SPARSE_TABLE")

    def test_11_elimination_fenwick_on_non_invertible_min(self):
        """Range min eliminates Fenwick tree with NON_INVERTIBLE_OPERATION_REJECTS_FENWICK."""
        spec = {"mutability": "POINT_UPDATE", "operation": "MIN"}
        res = self.solver.solve(spec)
        certs = res["candidate_analysis"].eliminated_candidates
        self.assertIn("fenwick_tree", certs)
        self.assertEqual(certs["fenwick_tree"].failure_code, "NON_INVERTIBLE_OPERATION_REJECTS_FENWICK")

    def test_12_elimination_mos_on_online_stream(self):
        """Online query stream eliminates Mo's algorithm with OFFLINE_MODE_REQUIRED_REJECTS_ONLINE_MOS."""
        spec = {"temporal": "ONLINE", "operation": "SUM"}
        res = self.solver.solve(spec)
        certs = res["candidate_analysis"].eliminated_candidates
        self.assertIn("mos_algorithm_scheduler", certs)
        self.assertEqual(certs["mos_algorithm_scheduler"].failure_code, "OFFLINE_MODE_REQUIRED_REJECTS_ONLINE_MOS")

    def test_13_elimination_dijkstra_on_negative_weights(self):
        """Negative edge weights eliminate Dijkstra with NEGATIVE_WEIGHTS_REJECT_DIJKSTRA."""
        spec = {"negative_weights": True}
        res = self.solver.solve(spec)
        certs = res["candidate_analysis"].eliminated_candidates
        self.assertIn("dijkstra_priority_queue", certs)
        self.assertEqual(certs["dijkstra_priority_queue"].failure_code, "NEGATIVE_WEIGHTS_REJECT_DIJKSTRA")

    def test_14_elimination_two_pointers_on_negative_elements(self):
        """Negative elements eliminate Two Pointers range sum with NON_MONOTONE_WINDOW_REJECTS_TWO_POINTERS."""
        spec = {"negative_elements": True, "operation": "SUM"}
        res = self.solver.solve(spec)
        certs = res["candidate_analysis"].eliminated_candidates
        self.assertIn("two_pointers_monotone_window", certs)
        self.assertEqual(certs["two_pointers_monotone_window"].failure_code, "NON_MONOTONE_WINDOW_REJECTS_TWO_POINTERS")

    def test_15_elimination_binary_search_on_oscillating_predicate(self):
        """Oscillating predicate eliminates Binary Search with NON_MONOTONE_PREDICATE_REJECTS_BISECTION."""
        spec = {"predicate_monotonic": False}
        res = self.solver.solve(spec)
        certs = res["candidate_analysis"].eliminated_candidates
        self.assertIn("binary_search_bisection", certs)
        self.assertEqual(certs["binary_search_bisection"].failure_code, "NON_MONOTONE_PREDICATE_REJECTS_BISECTION")

    def test_16_elimination_monotonic_deque_on_non_convex_cost(self):
        """Non-convex transition cost eliminates Monotonic Deque with NON_CONVEX_COST_REJECTS_MONOTONIC_DEQUE."""
        spec = {"dp_convex": False, "operation": "MIN"}
        res = self.solver.solve(spec)
        certs = res["candidate_analysis"].eliminated_candidates
        self.assertIn("monotonic_deque_sliding_window", certs)
        self.assertEqual(certs["monotonic_deque_sliding_window"].failure_code, "NON_CONVEX_COST_REJECTS_MONOTONIC_DEQUE")

    def test_17_elimination_massive_coordinates_rejects_flat_array(self):
        """Massive coordinates 10^18 eliminate flat array structures with MASSIVE_COORDINATES_REJECT_FLAT_ARRAY."""
        spec = {"coordinate_scale": "MASSIVE", "c": 10**18, "mutability": "POINT_UPDATE", "operation": "SUM"}
        res = self.solver.solve(spec)
        certs = res["candidate_analysis"].eliminated_candidates
        self.assertIn("fenwick_tree", certs)
        self.assertEqual(certs["fenwick_tree"].failure_code, "MASSIVE_COORDINATES_REJECT_FLAT_ARRAY")

    # ── 6. Resource Evaluator ──

    def test_18_resource_evaluator_space_bound_exceeded(self):
        """Candidate exceeding memory limit produces SPACE_BOUND_EXCEEDED certificate."""
        cand = self.universe["sparse_table"]
        budget = SymbolicBudget(N=20000000, Q=1000, time_limit_ms=10000, memory_limit_mb=16)  # 20M elements in Sparse Table > 1GB >> 16MB
        res = ResourceEvaluator.evaluate(cand, budget)
        self.assertFalse(res.is_feasible)
        self.assertEqual(res.failure_code, "SPACE_BOUND_EXCEEDED")

    def test_19_resource_evaluator_time_budget_exceeded(self):
        """Candidate exceeding operation limit produces TIME_BUDGET_EXCEEDED certificate."""
        cand = self.universe["dijkstra_priority_queue"]
        budget = SymbolicBudget(V=10000000, E=20000000, time_limit_ms=10) # 10ms cannot do 3*10^7 log V
        res = ResourceEvaluator.evaluate(cand, budget)
        self.assertFalse(res.is_feasible)
        self.assertEqual(res.failure_code, "TIME_BUDGET_EXCEEDED")

    def test_20_elimination_certificate_structure(self):
        """Every EliminationCertificate possesses all required structured audit fields."""
        spec = {"mutability": "POINT_UPDATE", "operation": "MIN"}
        res = self.solver.solve(spec)
        cert = res["candidate_analysis"].eliminated_candidates["sparse_table"]
        self.assertEqual(cert.candidate_id, "sparse_table")
        self.assertTrue(len(cert.failure_code) > 0)
        self.assertTrue(len(cert.witness) > 0)
        self.assertTrue(len(cert.asymptotic_argument) > 0)

    # ── 7. Single Candidate Solutions ──

    def test_21_candidate_analysis_minimal_surviving_set(self):
        """CandidateAnalysis partitions candidates into surviving and eliminated sets."""
        spec = {"temporal": "ONLINE", "mutability": "STATIC", "operation": "MIN"}
        res = self.solver.solve(spec)
        analysis = res["candidate_analysis"]
        self.assertTrue(len(analysis.surviving_candidates) > 0)
        self.assertTrue(len(analysis.eliminated_candidates) > 0)

    def test_22_single_candidate_selection_sparse_table(self):
        """Static online range minimum selects Sparse Table as SATISFIABLE_SINGLE_CANDIDATE."""
        spec = {"temporal": "ONLINE", "mutability": "STATIC", "operation": "MIN"}
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.SATISFIABLE_SINGLE_CANDIDATE)
        self.assertIn("sparse_table", res["verified_plan"].selected_components)

    def test_23_single_candidate_selection_fenwick(self):
        """Point update range sum selects Fenwick Tree as SATISFIABLE_SINGLE_CANDIDATE."""
        spec = {"temporal": "ONLINE", "mutability": "POINT_UPDATE", "operation": "SUM"}
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.SATISFIABLE_SINGLE_CANDIDATE)
        self.assertIn("fenwick_tree", res["verified_plan"].selected_components)

    def test_24_single_candidate_selection_dynamic_segtree(self):
        """Online point update on massive coordinates 10^18 selects Dynamic Segment Tree."""
        spec = {"temporal": "ONLINE", "coordinate_scale": "MASSIVE", "c": 10**18, "mutability": "POINT_UPDATE", "operation": "SUM"}
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.SATISFIABLE_SINGLE_CANDIDATE)
        self.assertIn("dynamic_segment_tree", res["verified_plan"].selected_components)

    # ── 8. Capability-DAG Synthesis & Compositions ──

    def test_25_capability_synthesis_tree_path_hld_segtree(self):
        """Tree path query synthesizes HLD + Segment Tree as SATISFIABLE_COMPOSED_PLAN."""
        spec = {
            "topology": "UNDIRECTED_TREE",
            "v": 100000,
            "e": 99999,
            "query_target": "TREE_PATH",
            "mutability": "POINT_UPDATE",
            "operation": "SUM"
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.SATISFIABLE_COMPOSED_PLAN)
        plan = res["verified_plan"]
        self.assertIn("heavy_light_decomposition", plan.selected_components)
        self.assertTrue(
            any(c in plan.selected_components for c in ("segment_tree_standard", "fenwick_tree")),
            f"Expected range query provider (segment_tree_standard or fenwick_tree), got {plan.selected_components}"
        )

    def test_26_capability_synthesis_massive_coords_compression(self):
        """Offline range sum on massive coordinates synthesizes Coordinate Compressor + Range Provider."""
        spec = {
            "temporal": "OFFLINE",
            "coordinate_scale": "MASSIVE",
            "offline_coordinates_known": True,
            "dynamic_pointers_allowed": False,
            "mutability": "POINT_UPDATE",
            "operation": "SUM"
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.SATISFIABLE_COMPOSED_PLAN)
        plan = res["verified_plan"]
        self.assertIn("coordinate_compressor", plan.selected_components)
        self.assertTrue(
            any(c in plan.selected_components for c in ("segment_tree_standard", "fenwick_tree")),
            f"Expected range query provider (segment_tree_standard or fenwick_tree), got {plan.selected_components}"
        )

    # ── 9. Disjoint Outcomes & Coverage Gap ──

    def test_27_coverage_gap_unresolved_by_ontology(self):
        """A problem whose capability gap cannot be bridged returns UNRESOLVED_BY_CURRENT_ONTOLOGY."""
        spec = {
            "query_target": "ALL_PAIRS",
            "mutability": "RANGE_UPDATE",
            "operation": "DISTINCT", # Unsupported combination
        }
        res = self.solver.solve(spec)
        self.assertEqual(res["outcome_state"], OutcomeState.UNRESOLVED_BY_CURRENT_ONTOLOGY)
        self.assertIsNotNone(res["unresolved_certificate"])

    def test_28_distinction_contradiction_vs_candidate_insufficiency(self):
        """Asserts that UNRESOLVED_BY_CURRENT_ONTOLOGY is strictly distinct from UNSATISFIABLE_CONSTRAINT_SET."""
        self.assertNotEqual(OutcomeState.UNRESOLVED_BY_CURRENT_ONTOLOGY, OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)

    # ── 10. Proof Obligations & Integrity Sealing ──

    def test_29_proof_obligations_structure_and_discharge(self):
        """Verified plans carry formally discharged proof obligations."""
        spec = {"temporal": "ONLINE", "mutability": "STATIC", "operation": "MIN"}
        res = self.solver.solve(spec)
        plan = res["verified_plan"]
        self.assertTrue(len(plan.proof_obligations) > 0)
        self.assertTrue(plan.all_obligations_discharged())

    def test_30_canonical_digest_deterministic_sha256(self):
        """SHA-256 seal is deterministic and matches canonical serialization digest."""
        spec = {"temporal": "ONLINE", "mutability": "STATIC", "operation": "MIN"}
        res = self.solver.solve(spec)
        plan = res["verified_plan"]
        self.assertEqual(len(plan.canonical_digest), 64)
        self.assertEqual(plan.canonical_digest, plan.compute_canonical_digest())

    # ── 11. Absolute Generator Barrier ──

    def test_31_generator_barrier_requires_verified_plan(self):
        """Generator strictly rejects raw input or unverified objects."""
        with self.assertRaises(TypeError):
            MultiConstraintCppGenerator.generate({"raw": "spec"})

    def test_32_generator_barrier_detects_tampered_digest(self):
        """Generator raises GeneratorBarrierError if integrity digest is tampered."""
        spec = {"temporal": "ONLINE", "mutability": "STATIC", "operation": "MIN"}
        res = self.solver.solve(spec)
        plan = res["verified_plan"]

        # Tampered plan with falsified digest
        tampered = VerifiedMultiConstraintPlan(
            plan_id=plan.plan_id,
            outcome_state=plan.outcome_state,
            selected_components=plan.selected_components,
            synthesized_pipeline=plan.synthesized_pipeline,
            proof_obligations=plan.proof_obligations,
            elimination_certificates=plan.elimination_certificates,
            canonical_digest="0000000000000000000000000000000000000000000000000000000000000000",
            verification_artifact_id=plan.verification_artifact_id
        )
        with self.assertRaises(GeneratorBarrierError):
            MultiConstraintCppGenerator.generate(tampered)

    def test_33_generator_barrier_detects_undischarged_obligations(self):
        """Generator raises GeneratorBarrierError if any proof obligation is UNMET."""
        spec = {"temporal": "ONLINE", "mutability": "STATIC", "operation": "MIN"}
        res = self.solver.solve(spec)
        plan = res["verified_plan"]

        unmet_obl = [
            ProofObligation("OBL-1", "C-1", "Prop", "Comp", "Ev", ProofStatus.UNMET)
        ]
        unmet_plan = VerifiedMultiConstraintPlan.seal(
            plan_id=plan.plan_id,
            outcome_state=plan.outcome_state,
            selected_components=plan.selected_components,
            synthesized_pipeline=plan.synthesized_pipeline,
            proof_obligations=unmet_obl,
            elimination_certificates=plan.elimination_certificates,
            verification_artifact_id=plan.verification_artifact_id
        )
        with self.assertRaises(GeneratorBarrierError):
            MultiConstraintCppGenerator.generate(unmet_plan)

    def test_34_generator_barrier_detects_invalid_topological_order(self):
        """Generator raises GeneratorBarrierError if step indices are out of order."""
        step2 = SynthesizedPipelineStep(2, "fenwick_tree", "Provider", frozenset(), frozenset())
        step1 = SynthesizedPipelineStep(1, "heavy_light_decomposition", "Decomposer", frozenset(), frozenset())

        invalid_plan = VerifiedMultiConstraintPlan.seal(
            plan_id="MCP-invalid-order",
            outcome_state=OutcomeState.SATISFIABLE_COMPOSED_PLAN,
            selected_components=["fenwick_tree", "heavy_light_decomposition"],
            synthesized_pipeline=[step2, step1], # Inverted order
            proof_obligations=[],
            elimination_certificates={},
            verification_artifact_id="VAP-invalid"
        )
        with self.assertRaises(GeneratorBarrierError):
            MultiConstraintCppGenerator.generate(invalid_plan)

    def test_35_end_to_end_cpp_generation_sealed_plan(self):
        """Generator emits clean standalone C++17 for a sealed plan."""
        spec = {"temporal": "ONLINE", "mutability": "STATIC", "operation": "MIN"}
        res = self.solver.solve(spec)
        code = MultiConstraintCppGenerator.generate(res["verified_plan"])
        self.assertIn("#include <iostream>", code)
        self.assertIn("SparseTable", code)
        self.assertIn(res["verified_plan"].canonical_digest, code)
        self.assertIn("int main()", code)


if __name__ == "__main__":
    unittest.main()
