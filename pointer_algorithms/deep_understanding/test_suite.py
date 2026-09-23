"""
CHUP Phase 6 — Deep Problem Understanding Unit Test Suite.

Comprehensive unit verification covering:
1. Fact Model & Epistemic Contracts (FactTier, ProofStatus, AmbiguityStatus)
2. Immutable Provenance Tracking & DAG Cycle Detection
3. Derivation Rule Contracts & Invariant Provers
4. Source Fact Contradiction Detection & Ambiguity Isolation
5. Implicit Constraint Axiomatic Deduction (Tree, DAG, Coordinate Scale)
6. Operation Semantics & Algebraic Decoupling
7. State Dependency Structural Modeling
8. Semantic Objectives & Arithmetic Requirements
9. Complexity Envelopes & Machine Model Estimation
10. Master Facade Integration with Phase 5 MultiConstraintSolver
"""

import unittest
from pointer_algorithms.deep_understanding.fact_model import (
    FactTier,
    ProofStatus,
    AmbiguityStatus,
    SemanticFact,
    FactSet
)
from pointer_algorithms.deep_understanding.provenance import (
    ProvenanceNode,
    ProvenanceGraph
)
from pointer_algorithms.deep_understanding.rule_registry import (
    DerivationRuleRegistry,
    DerivationRule
)
from pointer_algorithms.deep_understanding.contradiction_engine import (
    SourceFactContradictionEngine,
    ConflictingFactsCertificate,
    AmbiguityReport
)
from pointer_algorithms.deep_understanding.invariant_prover import InvariantProver
from pointer_algorithms.deep_understanding.implicit_constraints import ImplicitConstraintInferrer
from pointer_algorithms.deep_understanding.hidden_invariants import HiddenInvariantEngine
from pointer_algorithms.deep_understanding.operation_semantics import OperationSemanticsEngine
from pointer_algorithms.deep_understanding.state_dependency import (
    StateDependencyEngine,
    StateTopologyKind
)
from pointer_algorithms.deep_understanding.semantic_objective import (
    SemanticObjectiveEngine,
    ObjectiveKind
)
from pointer_algorithms.deep_understanding.complexity_requirements import (
    ComplexityRequirementEngine,
    ComplexityRequirementEnvelope,
    MachineModel
)
from pointer_algorithms.deep_understanding.deep_understanding_facade import DeepProblemUnderstandingFacade
from pointer_algorithms.multi_constraint.multi_constraint_model import OutcomeState
from pointer_algorithms.multi_constraint.constraint_lattice import Cyclicity, Directedness


class TestPhase6DeepProblemUnderstanding(unittest.TestCase):

    def setUp(self):
        self.facade = DeepProblemUnderstandingFacade()

    # ── 1. Fact Model & Epistemic Contracts ──────────────────────────────────────

    def test_01_fact_eligibility_invariant(self):
        """Only PROVEN facts of eligible tiers can modify Phase 5."""
        proven_obs = SemanticFact("f1", FactTier.OBSERVED_FACT, "V_COUNT", 10, ProofStatus.PROVEN)
        self.assertTrue(proven_obs.is_eligible_for_phase5())

        proven_derived = SemanticFact("f2", FactTier.DERIVED_FACT, "TOPOLOGY_TREE", "TREE", ProofStatus.PROVEN)
        self.assertTrue(proven_derived.is_eligible_for_phase5())

        hypothetical = SemanticFact("f3", FactTier.DERIVED_FACT, "TREE", True, ProofStatus.HYPOTHETICAL)
        self.assertFalse(hypothetical.is_eligible_for_phase5())

        # ALGORITHM_HYPOTHESIS is quarantined even if claimed PROVEN
        algo_hypo = SemanticFact("f4", FactTier.ALGORITHM_HYPOTHESIS, "USE_DIJKSTRA", True, ProofStatus.PROVEN)
        self.assertFalse(algo_hypo.is_eligible_for_phase5())

    def test_02_ambiguous_fact_ineligibility(self):
        """Ambiguous facts are strictly ineligible for Phase 5."""
        ambig_fact = SemanticFact(
            "f5", FactTier.OBSERVED_FACT, "QUERY_ORDER", "ARBITRARY",
            ProofStatus.PROVEN, ambiguity=AmbiguityStatus.AMBIGUOUS
        )
        self.assertFalse(ambig_fact.is_eligible_for_phase5())

    # ── 2. Provenance Graph & Traceability ───────────────────────────────────────

    def test_03_provenance_graph_trace_and_ancestry(self):
        """Provenance graph tracks ancestors and verifies unbroken PROVEN chain."""
        graph = ProvenanceGraph()
        n1 = ProvenanceNode("p1", "f_obs", (), "RULE_DIRECT_OBSERVATION", ProofStatus.PROVEN, "Direct input")
        n2 = ProvenanceNode("p2", "f_der", ("f_obs",), "RULE_DERIVATION", ProofStatus.PROVEN, "Derived from obs")
        graph.add_node(n1)
        graph.add_node(n2)

        ancestors = graph.get_ancestors("f_der")
        self.assertEqual(len(ancestors), 2)
        self.assertTrue(graph.verify_trace("f_der"))

    def test_04_provenance_cycle_detection(self):
        """Circular reasoning in provenance throws an immediate validation error."""
        graph = ProvenanceGraph()
        n1 = ProvenanceNode("p1", "f1", ("f2",), "RULE_A", ProofStatus.PROVEN, "f1 from f2")
        n2 = ProvenanceNode("p2", "f2", ("f1",), "RULE_B", ProofStatus.PROVEN, "f2 from f1")
        graph.add_node(n1)
        graph.add_node(n2)

        with self.assertRaises(ValueError):
            graph.get_ancestors("f1")

    # ── 3. Contradiction Engine ──────────────────────────────────────────────────

    def test_05_contradiction_directed_vs_undirected(self):
        """Simultaneous directed and undirected assertions halt with CONFLICTING_SOURCE_FACTS."""
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "IS_DIRECTED", True, ProofStatus.PROVEN),
            SemanticFact("f2", FactTier.OBSERVED_FACT, "IS_UNDIRECTED", True, ProofStatus.PROVEN)
        ])
        cert, ambig = SourceFactContradictionEngine.analyze(facts)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.failure_code, "CONFLICTING_SOURCE_FACTS")
        self.assertIn("IS_DIRECTED", cert.competing_facts)

    def test_06_contradiction_tree_cardinality(self):
        """Claimed tree with E != V - 1 triggers cardinality conflict."""
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "CLAIMED_TREE", True, ProofStatus.PROVEN),
            SemanticFact("f2", FactTier.OBSERVED_FACT, "VERTEX_COUNT", 5, ProofStatus.PROVEN),
            SemanticFact("f3", FactTier.OBSERVED_FACT, "EDGE_COUNT", 6, ProofStatus.PROVEN)
        ])
        cert, _ = SourceFactContradictionEngine.analyze(facts)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.conflict_id, "CONFLICT_TREE_CARDINALITY")

    def test_07_ambiguity_report_isolation(self):
        """Ambiguous statements emit an AmbiguityReport without triggering contradiction."""
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "ORDER", "ANY", ProofStatus.PROVEN, AmbiguityStatus.AMBIGUOUS)
        ])
        cert, ambig = SourceFactContradictionEngine.analyze(facts)
        self.assertIsNone(cert)
        self.assertIsNotNone(ambig)
        self.assertIn("ORDER", ambig.ambiguous_fact_names)

    # ── 4. Invariant Prover & Derivation Rules ───────────────────────────────────

    def test_08_tree_equivalence_deduction(self):
        """Tree topology is deduced only when E = V - 1, connected, undirected, and simple."""
        graph = ProvenanceGraph()
        inferrer = ImplicitConstraintInferrer()

        # Incomplete facts: E = V - 1 alone
        incomplete_facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "VERTEX_COUNT", 5, ProofStatus.PROVEN),
            SemanticFact("f2", FactTier.OBSERVED_FACT, "EDGE_COUNT", 4, ProofStatus.PROVEN)
        ])
        res = inferrer.infer_constraints(incomplete_facts, graph)
        self.assertFalse(any(f.name == "TOPOLOGY_TREE" for f in res))

        # Complete facts: E = V - 1 conjoined with Connected, Undirected, Simple
        complete_facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "VERTEX_COUNT", 5, ProofStatus.PROVEN),
            SemanticFact("f2", FactTier.OBSERVED_FACT, "EDGE_COUNT", 4, ProofStatus.PROVEN),
            SemanticFact("f3", FactTier.OBSERVED_FACT, "IS_CONNECTED", True, ProofStatus.PROVEN),
            SemanticFact("f4", FactTier.OBSERVED_FACT, "IS_UNDIRECTED", True, ProofStatus.PROVEN),
            SemanticFact("f5", FactTier.OBSERVED_FACT, "IS_SIMPLE", True, ProofStatus.PROVEN)
        ])
        res = inferrer.infer_constraints(complete_facts, graph)
        tree_fact = next((f for f in res if f.name == "TOPOLOGY_TREE"), None)
        self.assertIsNotNone(tree_fact)
        self.assertEqual(tree_fact.value, "TREE")
        self.assertTrue(tree_fact.is_eligible_for_phase5())

    def test_09_predicate_monotonicity_prover(self):
        """Predicate monotonicity discharges proof obligation and produces bisection support."""
        graph = ProvenanceGraph()
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "PREDICATE_MONOTONE", True, ProofStatus.PROVEN)
        ])
        res = InvariantProver.prove_predicate_monotonicity(facts, graph)
        self.assertIsNotNone(res)
        self.assertEqual(res.name, "ANSWER_BISECTION_SUPPORTED")
        self.assertEqual(res.proof_status, ProofStatus.PROVEN)

    def test_10_sliding_window_prover_requires_non_negative(self):
        """Sliding window monotonicity requires both right expansion monotonicity and non-negative values."""
        graph = ProvenanceGraph()
        # Missing non-negative elements
        facts_no_nonneg = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "WINDOW_VALIDITY_MONOTONE_IN_RIGHT_EXPANSION", True, ProofStatus.PROVEN)
        ])
        res1 = InvariantProver.prove_sliding_window_monotonicity(facts_no_nonneg, graph)
        self.assertIsNone(res1)

        # Both present
        facts_complete = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "WINDOW_VALIDITY_MONOTONE_IN_RIGHT_EXPANSION", True, ProofStatus.PROVEN),
            SemanticFact("f2", FactTier.OBSERVED_FACT, "ELEMENTS_NON_NEGATIVE", True, ProofStatus.PROVEN)
        ])
        res2 = InvariantProver.prove_sliding_window_monotonicity(facts_complete, graph)
        self.assertIsNotNone(res2)
        self.assertEqual(res2.name, "SLIDING_WINDOW_TWO_POINTER_SUPPORTED")

    # ── 5. Operation Semantics & State Topology ──────────────────────────────────

    def test_11_algebraic_semantics_sum_and_min(self):
        """SUM possesses invertibility for prefix derivability; MIN possesses idempotence for overlapping intervals."""
        graph = ProvenanceGraph()
        facts = FactSet.from_iterable([])

        sum_facts, sum_agg = OperationSemanticsEngine.deduce_algebraic_capabilities("SUM", facts, graph)
        self.assertTrue(sum_agg.is_invertible)
        self.assertTrue(any(f.name == "RANGE_DERIVABLE_FROM_PREFIXES" for f in sum_facts))

        min_facts, min_agg = OperationSemanticsEngine.deduce_algebraic_capabilities("MIN", facts, graph)
        self.assertTrue(min_agg.is_idempotent)
        self.assertFalse(min_agg.is_invertible)
        self.assertTrue(any(f.name == "OVERLAPPING_INTERVAL_QUERY_SUPPORTED" for f in min_facts))

    def test_12_state_topology_structural_description(self):
        """State topology reflects structural properties, not algorithm prescriptions."""
        graph = ProvenanceGraph()
        facts_dag = FactSet.from_iterable([
            SemanticFact("f1", FactTier.DERIVED_FACT, "STATE_TOPOLOGY_DAG", "DAG", ProofStatus.PROVEN)
        ])
        topo_kind, topo_domain = StateDependencyEngine.deduce_topology(facts_dag, graph)
        self.assertEqual(topo_kind, StateTopologyKind.DAG)
        self.assertEqual(topo_domain.cyclicity, Cyclicity.ACYCLIC)
        self.assertEqual(topo_domain.directedness, Directedness.DIRECTED)

    # ── 6. Semantic Objective & Complexity Envelopes ─────────────────────────────

    def test_13_semantic_objective_and_overflow_guard(self):
        """Detects optimization extremum and flags 64-bit integer overflow requirement."""
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "GOAL_OPTIMIZE_EXTREMUM", True, ProofStatus.PROVEN),
            SemanticFact("f2", FactTier.OBSERVED_FACT, "TARGET_LINEAR_RANGE", True, ProofStatus.PROVEN),
            SemanticFact("f3", FactTier.OBSERVED_FACT, "POTENTIAL_INTEGER_OVERFLOW", True, ProofStatus.PROVEN)
        ])
        obj_kind, query_spec, arith = SemanticObjectiveEngine.deduce_objective(facts)
        self.assertEqual(obj_kind, ObjectiveKind.OPTIMIZATION_EXTREMUM)
        self.assertTrue(arith.requires_64bit)

    def test_14_complexity_envelope_derivation(self):
        """Derives upper asymptotic envelope and operations ceiling without evaluating candidates."""
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "N_COUNT", 200_000, ProofStatus.PROVEN),
            SemanticFact("f2", FactTier.OBSERVED_FACT, "Q_COUNT", 200_000, ProofStatus.PROVEN),
            SemanticFact("f3", FactTier.OBSERVED_FACT, "TIME_LIMIT_SEC", 2.0, ProofStatus.PROVEN)
        ])
        envelope = ComplexityRequirementEngine.derive_envelope(facts)
        self.assertEqual(envelope.target_asymptotic_class, "O((N+Q) log N)")
        self.assertGreater(envelope.max_estimated_operations, 1e8)

        # Translates into Phase 5 SymbolicBudget
        budget = envelope.to_symbolic_budget()
        self.assertEqual(budget.N, 200_000)
        self.assertEqual(budget.Q, 200_000)

    # ── 7. End-to-End Facade Integration ─────────────────────────────────────────

    def test_15_facade_end_to_end_satisfiable_plan(self):
        """End-to-end processing of valid problem yields a verified multi-constraint plan from Phase 5."""
        spec = {
            "text": "Given an array of n integers and q range sum queries.",
            "n": 100_000,
            "q": 100_000,
            "operation": "SUM",
            "target": "LINEAR_RANGE",
            "immutable": True
        }
        res = self.facade.process(spec)
        self.assertEqual(res["status"], "success")
        self.assertIn(res["outcome_state"], (OutcomeState.SATISFIABLE_SINGLE_CANDIDATE, OutcomeState.SATISFIABLE_COMPOSED_PLAN))
        self.assertIsNotNone(res["verified_plan"])

    def test_16_facade_conflicting_facts_halts_with_certificate(self):
        """Conflicting source facts immediately halt the pipeline with ConflictingFactsCertificate."""
        spec = {
            "text": "The graph is both directed and undirected.",
            "directed": True,
            "undirected": True
        }
        res = self.facade.process(spec)
        self.assertEqual(res["status"], "conflict")
        self.assertEqual(res["outcome_state"], OutcomeState.UNSATISFIABLE_CONSTRAINT_SET)
        self.assertIsNotNone(res["conflict_certificate"])
        self.assertEqual(res["conflict_certificate"].failure_code, "CONFLICTING_SOURCE_FACTS")


    def test_17_immutability_of_facts_and_provenance(self):
        """SemanticFact and ProvenanceNode are frozen; mutation raises FrozenInstanceError."""
        fact = SemanticFact("f1", FactTier.OBSERVED_FACT, "V", 10, ProofStatus.PROVEN)
        with self.assertRaises(Exception):
            fact.value = 20  # type: ignore

        node = ProvenanceNode("p1", "f1", (), "RULE", ProofStatus.PROVEN, "witness")
        with self.assertRaises(Exception):
            node.witness = "tampered"  # type: ignore

    def test_18_dag_from_monotonic_coordinates(self):
        """Monotonic coordinate progression formally deduces DAG state topology."""
        graph = ProvenanceGraph()
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "TRANSITIONS_NON_DECREASING_COORDINATES", True, ProofStatus.PROVEN)
        ])
        inferrer = ImplicitConstraintInferrer()
        derived = inferrer.infer_constraints(facts, graph)
        dag_fact = next((f for f in derived if f.name == "STATE_TOPOLOGY_DAG"), None)
        self.assertIsNotNone(dag_fact)
        self.assertEqual(dag_fact.value, "DAG")

    def test_19_bipartite_from_absence_of_odd_cycles(self):
        """Absence of odd cycles formally deduces BIPARTITE graph topology."""
        graph = ProvenanceGraph()
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "NO_ODD_CYCLES", True, ProofStatus.PROVEN)
        ])
        inferrer = ImplicitConstraintInferrer()
        derived = inferrer.infer_constraints(facts, graph)
        bip_fact = next((f for f in derived if f.name == "GRAPH_BIPARTITE"), None)
        self.assertIsNotNone(bip_fact)
        self.assertEqual(bip_fact.value, "BIPARTITE")

    def test_20_massive_coordinates_dense_incompatibility(self):
        """Massive coordinates (>10^9) with coordinate indexing deduces DENSE_INDEX_SPACE_UNAVAILABLE."""
        graph = ProvenanceGraph()
        facts = FactSet.from_iterable([
            SemanticFact("f1", FactTier.OBSERVED_FACT, "COORDINATES_EXCEED_DENSE_MEMORY_BOUND", True, ProofStatus.PROVEN),
            SemanticFact("f2", FactTier.OBSERVED_FACT, "COORDINATE_QUERY_OR_INDEX_REQUIRED", True, ProofStatus.PROVEN)
        ])
        inferrer = ImplicitConstraintInferrer()
        derived = inferrer.infer_constraints(facts, graph)
        dense_unavail = next((f for f in derived if f.name == "DENSE_INDEX_SPACE_UNAVAILABLE"), None)
        self.assertIsNotNone(dense_unavail)
        self.assertTrue(dense_unavail.value)

    def test_21_provenance_audit_trail_formatting(self):
        """Provenance graph formats valid human-readable Markdown audit trails."""
        graph = ProvenanceGraph()
        n1 = ProvenanceNode("p1", "f_obs", (), "RULE_DIRECT_OBSERVATION", ProofStatus.PROVEN, "Direct input text")
        n2 = ProvenanceNode("p2", "f_der", ("f_obs",), "RULE_DERIVATION", ProofStatus.PROVEN, "Derived consequence")
        graph.add_node(n1)
        graph.add_node(n2)

        trail = graph.format_audit_trail("f_der")
        self.assertIn("Provenance Audit Trail for Fact: f_der", trail)
        self.assertIn("RULE_DERIVATION", trail)
        self.assertIn("Direct input text", trail)

    def test_22_fact_set_filtering_and_queries(self):
        """FactSet handles querying, eligible fact filtering, and value checks."""
        f1 = SemanticFact("f1", FactTier.OBSERVED_FACT, "A", 10, ProofStatus.PROVEN)
        f2 = SemanticFact("f2", FactTier.ALGORITHM_HYPOTHESIS, "B", 20, ProofStatus.PROVEN)
        fset = FactSet.from_iterable([f1, f2])

        self.assertTrue(fset.has_proven("A", 10))
        self.assertFalse(fset.has_proven("A", 99))
        self.assertEqual(len(fset.eligible_facts()), 1)
        self.assertEqual(fset.eligible_facts()[0].name, "A")


if __name__ == "__main__":
    unittest.main()
