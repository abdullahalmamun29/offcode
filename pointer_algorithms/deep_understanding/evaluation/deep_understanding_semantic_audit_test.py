"""
CHUP Phase 6 — Semantic Audit & Malicious Inference Test Battery.

Addresses the 5 critical semantic contract audits:
1. Dijkstra Compatibility vs Selection:
   - Non-negative weights prove DIJKSTRA_COMPATIBLE (compatibility only).
   - USE_DIJKSTRA is strictly ALGORITHM_HYPOTHESIS, quarantined, and never enters Phase 5.
2. Cayley Tree Exact Precondition Discharge:
   - (E = V-1, connected, undirected, simple) -> Tree PROVEN.
   - (E = V-1, disconnected) -> NOT proven Tree.
   - (connected, acyclic, undirected, simple) -> Tree PROVEN.
   - (directed, E = V-1) -> NOT Tree.
   - (multigraph / self-loops) -> NOT Tree.
3. Complexity Envelope Purity:
   - Envelope contains bounds, ops, bytes, and asymptotic requirements.
   - Envelope NEVER contains algorithm selections, candidate eliminations, or template prescriptions.
4. Maliciously Plausible Inference Rejection:
   - "Queries arrive quickly." -> does NOT prove ONLINE_REQUIRED or POINT_UPDATE.
   - "The graph represents roads." -> does NOT prove UNDIRECTED.
   - "N is very large." -> does NOT prove O(N log N) REQUIRED.
   - "We need the shortest route." -> does NOT prove DIJKSTRA.
   - "Coordinates are up to 10^18." -> does NOT prove COORDINATE_COMPRESSION_REQUIRED.
"""

import unittest
from pointer_algorithms.deep_understanding.fact_model import (
    SemanticFact,
    FactSet,
    FactTier,
    ProofStatus,
    AmbiguityStatus
)
from pointer_algorithms.deep_understanding.rule_registry import DerivationRuleRegistry
from pointer_algorithms.deep_understanding.deep_understanding_facade import DeepProblemUnderstandingFacade
from pointer_algorithms.deep_understanding.state_dependency import StateDependencyEngine, StateTopologyKind
from pointer_algorithms.deep_understanding.complexity_requirements import ComplexityRequirementEngine
from pointer_algorithms.multi_constraint.constraint_lattice import TemporalMode, CoordinateScale


class TestPhase6SemanticAuditAndMaliciousInference(unittest.TestCase):
    def setUp(self):
        self.facade = DeepProblemUnderstandingFacade()
        self.registry = DerivationRuleRegistry()

    # =========================================================================
    # Audit 1: Dijkstra Compatibility vs Selection
    # =========================================================================

    def test_dijkstra_compatibility_vs_selection(self):
        """Non-negative weights prove compatibility, NOT necessity or algorithm selection."""
        spec = {
            "text": "Weighted graph with all non-negative edge costs between vertices.",
            "v": 500,
            "e": 2000,
            "all_non_negative": True,
            "target": "POINT",
            "operation": "MIN"
        }
        res = self.facade.process(spec)
        facts = res["phase6_facts"]

        # 1. Non-negative weights are proven
        self.assertTrue(facts.has_proven("ALL_EDGE_WEIGHTS_NON_NEGATIVE", True))
        self.assertTrue(facts.has_proven("NON_NEGATIVE_EDGE_WEIGHTS", True))

        # 2. Dijkstra compatibility is proven
        self.assertTrue(facts.has_proven("DIJKSTRA_COMPATIBLE", True))

        # 3. USE_DIJKSTRA is NOT a proven fact
        self.assertFalse(facts.has_proven("USE_DIJKSTRA", True))

        # 4. Any algorithm hypothesis remains quarantined and outside Phase 5
        eligible_names = {f.name for f in facts.eligible_facts()}
        self.assertNotIn("USE_DIJKSTRA", eligible_names)
        for f in facts.eligible_facts():
            self.assertNotEqual(f.tier, FactTier.ALGORITHM_HYPOTHESIS)

    # =========================================================================
    # Audit 2: Cayley Rule Exact Precondition Discharge
    # =========================================================================

    def test_cayley_connected_undirected_simple_is_tree(self):
        """E = V - 1, connected, undirected, simple -> Tree PROVEN."""
        spec = {
            "text": "A connected, undirected, simple network with V=100 vertices and E=99 edges.",
            "v": 100,
            "e": 99,
            "connected": True,
            "undirected": True,
            "simple": True
        }
        res = self.facade.process(spec)
        facts = res["phase6_facts"]
        self.assertTrue(facts.has_proven("TOPOLOGY_TREE", "TREE"))
        self.assertEqual(res["state_topology"], StateTopologyKind.TREE)

    def test_cayley_disconnected_is_not_tree(self):
        """E = V - 1 on a disconnected graph must NOT be proven Tree."""
        spec = {
            "text": "A disconnected network with V=10 vertices and E=9 edges (two separate components).",
            "v": 10,
            "e": 9,
            "disconnected": True,
            "undirected": True,
            "simple": True
        }
        res = self.facade.process(spec)
        facts = res["phase6_facts"]
        self.assertFalse(facts.has_proven("TOPOLOGY_TREE", "TREE"))
        self.assertNotEqual(res["state_topology"], StateTopologyKind.TREE)

    def test_tree_connected_acyclic(self):
        """Connected + acyclic + undirected + simple -> Tree PROVEN without explicit edge count."""
        spec = {
            "text": "An acyclic connected undirected simple graph.",
            "connected": True,
            "acyclic": True,
            "undirected": True,
            "simple": True
        }
        res = self.facade.process(spec)
        facts = res["phase6_facts"]
        self.assertTrue(facts.has_proven("TOPOLOGY_TREE", "TREE"))
        self.assertEqual(res["state_topology"], StateTopologyKind.TREE)

    def test_directed_with_e_eq_v_minus_one_not_tree(self):
        """Directed graph with E = V - 1 is NOT an undirected Tree."""
        spec = {
            "text": "A directed graph with V=50 and E=49.",
            "v": 50,
            "e": 49,
            "directed": True,
            "connected": True,
            "simple": True
        }
        res = self.facade.process(spec)
        facts = res["phase6_facts"]
        self.assertFalse(facts.has_proven("TOPOLOGY_TREE", "TREE"))
        self.assertNotEqual(res["state_topology"], StateTopologyKind.TREE)

    def test_multigraph_with_e_eq_v_minus_one_not_tree(self):
        """Multigraph with E = V - 1 is NOT a simple tree."""
        spec = {
            "text": "A multigraph with parallel edges having V=10 and E=9.",
            "v": 10,
            "e": 9,
            "multigraph": True,
            "connected": True,
            "undirected": True
        }
        res = self.facade.process(spec)
        facts = res["phase6_facts"]
        self.assertFalse(facts.has_proven("TOPOLOGY_TREE", "TREE"))
        self.assertNotEqual(res["state_topology"], StateTopologyKind.TREE)

    # =========================================================================
    # Audit 3: Complexity Envelope Purity
    # =========================================================================

    def test_complexity_envelope_contains_requirements_not_algorithms(self):
        """The complexity envelope crossing into Phase 5 contains requirements, not algorithm selections."""
        spec = {
            "text": "Answer range queries on an array.",
            "n": 200_000,
            "q": 200_000,
            "operation": "SUM",
            "target": "LINEAR_RANGE"
        }
        res = self.facade.process(spec)
        envelope = res["complexity_envelope"]

        # Requirements present
        self.assertEqual(envelope.target_asymptotic_class, "O((N+Q) log N)")
        self.assertEqual(envelope.numeric_bounds["n"], 200_000)
        self.assertEqual(envelope.numeric_bounds["q"], 200_000)
        self.assertGreater(envelope.max_estimated_operations, 0)
        self.assertGreater(envelope.max_estimated_bytes, 0)

        # No algorithm names in the envelope
        envelope_dict_repr = str(envelope.__dict__)
        forbidden_algo_names = ["fenwick", "segment_tree", "sparse_table", "dijkstra", "kruskal", "mo_algorithm"]
        for algo in forbidden_algo_names:
            self.assertNotIn(algo, envelope_dict_repr.lower())

    # =========================================================================
    # Audit 5: Maliciously Plausible Inference Rejection Suite
    # =========================================================================

    def test_malicious_queries_arrive_quickly_rejects_online_and_point_update(self):
        """'Queries arrive quickly.' must NOT prove ONLINE_REQUIRED or POINT_UPDATE."""
        spec = {
            "text": "Queries arrive quickly in this problem. Calculate the sum of elements.",
            "n": 100_000,
            "q": 100_000,
            "operation": "SUM",
            "target": "LINEAR_RANGE"
        }
        res = self.facade.process(spec)
        facts = res["phase6_facts"]

        # Must not prove online stream
        self.assertFalse(facts.has_proven("ONLINE_QUERY_STREAM", True))
        self.assertFalse(facts.has_proven("REQUIRES_ONLINE_INTERACTIVE", True))

        # Must not prove point update
        self.assertFalse(facts.has_proven("REQUIRES_DYNAMIC_POINT_UPDATE", True))

        # Solver still succeeds by selecting static range query candidate
        self.assertIsNotNone(res["verified_plan"])

    def test_malicious_roads_rejects_undirected(self):
        """'The graph represents roads.' must NOT prove UNDIRECTED."""
        spec = {
            "text": "The graph represents roads between locations in a city. Find paths.",
            "v": 500,
            "e": 1000
        }
        res = self.facade.process(spec)
        facts = res["phase6_facts"]

        # Must not prove undirected (roads can be one-way / directed)
        self.assertFalse(facts.has_proven("IS_UNDIRECTED", True))
        self.assertFalse(facts.has_proven("IS_DIRECTED", True))

    def test_malicious_n_is_very_large_rejects_asymptotic_requirement(self):
        """'N is very large.' without numeric bound must NOT prove O(N log N) REQUIRED."""
        spec = {
            "text": "N is very large in this data problem. Process all elements.",
            "operation": "SUM"
        }
        res = self.facade.process(spec)
        envelope = res["complexity_envelope"]

        # Without numeric bound, target asymptotic class must be UNSPECIFIED
        self.assertEqual(envelope.target_asymptotic_class, "UNSPECIFIED")

    def test_malicious_shortest_route_rejects_dijkstra_selection(self):
        """'We need the shortest route.' must NOT prove DIJKSTRA."""
        spec = {
            "text": "We need the shortest route between junction A and junction B.",
            "v": 100,
            "e": 500,
            "operation": "MIN",
            "target": "POINT"
        }
        res = self.facade.process(spec)
        facts = res["phase6_facts"]

        # Must NOT prove DIJKSTRA
        self.assertFalse(facts.has_proven("USE_DIJKSTRA", True))
        self.assertFalse(facts.has_proven("DIJKSTRA_REQUIRED", True))
        eligible_names = {f.name for f in facts.eligible_facts()}
        self.assertNotIn("USE_DIJKSTRA", eligible_names)

    def test_malicious_massive_coordinates_without_indexing_rejects_compression(self):
        """'Coordinates are up to 10^18.' without coordinate queries must NOT prove compression required."""
        spec = {
            "text": "Coordinates are up to 10^18 in a 2D plane. Compute the Euclidean distance between two points.",
            "n": 2,
            "max_coordinate": 10**18
        }
        res = self.facade.process(spec)
        facts = res["phase6_facts"]

        # Large coordinate is observed
        self.assertTrue(facts.has_proven("COORDINATES_EXCEED_DENSE_MEMORY_BOUND", True))

        # But coordinate indexing is NOT required (only two points evaluated mathematically)
        self.assertFalse(facts.has_proven("COORDINATE_QUERY_OR_INDEX_REQUIRED", True))
        self.assertFalse(facts.has_proven("DENSE_INDEX_SPACE_UNAVAILABLE", True))


if __name__ == "__main__":
    unittest.main()
