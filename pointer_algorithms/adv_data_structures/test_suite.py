"""
CHUP Phase 3S — Unit Test Suite for Advanced Data Structures.

26 targeted unit tests covering all 10 canonical patterns, composable algebraic
properties, topological derived states, persistence trees, and Closed-World Validation
Gates (Gates A–I).
"""

import unittest
from pointer_algorithms.adv_data_structures.semantic_ontology import (
    SemanticAdvancedDataStructureModel,
    AdvancedDataStructureObjective,
    AlgebraicProperties,
    GraphTopologyState,
    PathValueDomain,
    PersistenceMode,
    StructureMutability,
    RangeOrderStatisticObjective,
    MoOrderingStrategy,
    CoordinateDomain,
    QueryMode,
    ProviderCapability,
)
from pointer_algorithms.adv_data_structures.ads_state_contracts import (
    make_sparse_table_state,
    make_tree_topology_state,
    make_binary_lifting_lca_state,
    make_heavy_light_decomposition_state,
    make_centroid_tree_state,
    make_persistent_segment_tree_state,
    make_dynamic_segment_tree_state,
    make_merge_sort_tree_state,
    make_sqrt_decomposition_state,
    make_mos_query_schedule_state,
    make_segment_tree_beats_state,
)
from pointer_algorithms.adv_data_structures.component_model import (
    AdvancedDataStructureComponentRegistry,
)
from pointer_algorithms.adv_data_structures.derivation_engine import (
    AdvancedDataStructureDerivationEngine,
)
from pointer_algorithms.adv_data_structures.derivation.candidate_evaluator import (
    CandidateVerdict,
)
from pointer_algorithms.adv_data_structures.verification.ads_oracles import (
    oracle_sparse_table,
    oracle_lca_binary_lifting,
    oracle_heavy_light_decomposition,
    oracle_centroid_decomposition,
    oracle_persistent_segment_tree,
    oracle_dynamic_segment_tree,
    oracle_merge_sort_tree,
    oracle_sqrt_decomposition,
    oracle_mos_algorithm,
    oracle_segment_tree_beats,
)


class TestAdvancedDataStructures(unittest.TestCase):
    def setUp(self):
        self.engine = AdvancedDataStructureDerivationEngine()
        self.registry = AdvancedDataStructureComponentRegistry()

    # ── 1. Oracle Tests (Tests 1–10) ──

    def test_01_oracle_sparse_table(self):
        arr = [4, 2, 7, 1, 9, 3, 6]
        queries = [(0, 3), (2, 5), (0, 6)]
        res = oracle_sparse_table(arr, queries, "min")
        self.assertEqual(res, [1, 1, 1])

    def test_02_oracle_lca_binary_lifting(self):
        # Tree: 0-1, 0-2, 1-3, 1-4, 2-5
        edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]
        queries = [(3, 4), (3, 5), (1, 3), (0, 5)]
        res = oracle_lca_binary_lifting(6, edges, queries, root=0)
        self.assertEqual(res, [1, 0, 1, 0])

    def test_03_oracle_heavy_light_decomposition(self):
        edges = [(0, 1), (1, 2), (0, 3)]
        vals = [10, 20, 30, 40]
        queries = [("query", 2, 3), ("update", 1, 25), ("query", 2, 3)]
        res = oracle_heavy_light_decomposition(4, edges, vals, queries, is_edge_values=False)
        self.assertEqual(res, [100, 105])

    def test_04_oracle_centroid_decomposition(self):
        # Line graph 0-1-2-3-4; centroid of 0..4 is 2
        edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
        c_parent, c_depth, dist_table = oracle_centroid_decomposition(5, edges)
        # Root centroid should be 2
        self.assertEqual(c_parent[2], -1)
        self.assertEqual(dist_table[0][2], 2)
        self.assertEqual(dist_table[4][2], 2)

    def test_05_oracle_persistent_segment_tree(self):
        initial = [1, 2, 3, 4]
        updates = [(0, 1, 10), (1, 3, 20)] # v1: [1, 10, 3, 4], v2: [1, 10, 3, 20]
        queries = [(0, 0, 3), (1, 0, 3), (2, 0, 3)]
        res = oracle_persistent_segment_tree(initial, updates, queries)
        self.assertEqual(res, [10, 18, 34])

    def test_06_oracle_dynamic_segment_tree(self):
        updates = [(5, 10), (1000000000, 20), (500000, 30)]
        queries = [(1, 10), (1, 1000000000), (6, 999999)]
        res = oracle_dynamic_segment_tree(1, 10**18, updates, queries)
        self.assertEqual(res, [10, 60, 30])

    def test_07_oracle_merge_sort_tree(self):
        arr = [5, 1, 9, 3, 7, 2, 8]
        queries = [(0, 6, 5), (1, 4, 6), (0, 2, 0)]
        res = oracle_merge_sort_tree(arr, queries)
        self.assertEqual(res, [4, 2, 0])

    def test_08_oracle_sqrt_decomposition(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        updates = [(0, 4, 10)] # adds 10 to [0..4]
        queries = [(0, 8), (0, 4), (5, 8)]
        res = oracle_sqrt_decomposition(arr, updates, queries)
        self.assertEqual(res, [95, 65, 30])

    def test_09_oracle_mos_algorithm(self):
        arr = [1, 1, 2, 1, 3, 4, 5, 2, 3]
        queries = [(0, 3), (2, 6), (0, 8)]
        res = oracle_mos_algorithm(arr, queries, "STANDARD_BLOCK_SNAKE")
        # [1, 1, 2, 1] -> distinct 2 (1, 2)
        # [2, 1, 3, 4, 5] -> distinct 5
        # [1..3] -> distinct 5
        self.assertEqual(res, [2, 5, 5])

    def test_10_oracle_segment_tree_beats(self):
        arr = [5, 5, 10, 10, 3]
        ops = [
            ("query_sum", 0, 4, None),   # sum = 33
            ("chmin", 0, 3, 7),          # arr becomes [5, 5, 7, 7, 3]
            ("query_sum", 0, 4, None),   # sum = 27
            ("query_max", 0, 4, None),   # max = 7
        ]
        res = oracle_segment_tree_beats(arr, ops)
        self.assertEqual(res, [33, 27, 7])

    # ── 2. Algebraic Properties & Sparse Table Tests (Tests 11–13) ──

    def test_11_composable_algebraic_properties(self):
        p_min = AlgebraicProperties.min_operation()
        self.assertTrue(p_min.associative)
        self.assertTrue(p_min.idempotent)
        self.assertFalse(p_min.invertible)
        self.assertTrue(p_min.has_identity)

        p_sum = AlgebraicProperties.sum_operation()
        self.assertTrue(p_sum.associative)
        self.assertFalse(p_sum.idempotent)
        self.assertTrue(p_sum.invertible)

    def test_12_sparse_table_derivation_optimal(self):
        spec = {
            "objective": "SPARSE_TABLE_RMQ",
            "algebraic_properties": {"operation": "min"}
        }
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["optimal_candidate"], "sparse_table_rmq")

    def test_13_gate_c_sparse_table_non_idempotent_rejection(self):
        spec = {
            "objective": "SPARSE_TABLE_RMQ",
            "algebraic_properties": {"operation": "sum"}
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "NON_IDEMPOTENT_OPERATION_REJECTS_O1_SPARSE_TABLE")

    # ── 3. Tree Topology & Gate A Tests (Tests 14–16) ──

    def test_14_gate_a_topology_empty(self):
        spec = {
            "objective": "LCA_BINARY_LIFTING",
            "topology_state": "EMPTY",
            "vertex_count": 0
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "TOPOLOGY_EMPTY")

    def test_15_gate_a_topology_cyclic(self):
        spec = {
            "objective": "LCA_BINARY_LIFTING",
            "topology_state": "CYCLIC"
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "TOPOLOGY_CYCLIC")

    def test_16_gate_a_topology_disconnected(self):
        spec = {
            "objective": "HEAVY_LIGHT_DECOMPOSITION",
            "topology_state": "DISCONNECTED"
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "TOPOLOGY_DISCONNECTED")

    # ── 4. HLD Path Domains & Gate H Tests (Tests 17–18) ──

    def test_17_hld_edge_vs_vertex_semantics(self):
        spec_v = {"objective": "HEAVY_LIGHT_DECOMPOSITION", "path_value_domain": "VERTEX_VALUES"}
        model_v = self.engine.extractor.extract(spec_v)
        self.assertEqual(model_v.path_value_domain, PathValueDomain.VERTEX_VALUES)

        spec_e = {"objective": "HEAVY_LIGHT_DECOMPOSITION", "path_value_domain": "EDGE_VALUES"}
        model_e = self.engine.extractor.extract(spec_e)
        self.assertEqual(model_e.path_value_domain, PathValueDomain.EDGE_VALUES)

    def test_18_gate_h_hld_missing_range_provider(self):
        spec = {
            "objective": "HEAVY_LIGHT_DECOMPOSITION",
            "has_range_provider": False
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "NO_RANGE_STRUCTURE_PROVIDER")

    # ── 5. Mo's Algorithm & Gates B, G Tests (Tests 19–20) ──

    def test_19_gate_b_mos_algorithm_online_rejection(self):
        spec = {
            "objective": "MOS_ALGORITHM",
            "query_mode": "ONLINE"
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "ALGORITHM_REQUIRES_OFFLINE_QUERIES")

    def test_20_gate_g_mos_irreversible_transitions(self):
        spec = {
            "objective": "MOS_ALGORITHM",
            "query_mode": "OFFLINE",
            "transition_cost": {"is_reversible": False}
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "IRREVERSIBLE_INTERVAL_TRANSITION")

    # ── 6. Persistent SegTree & Gate E Tests (Tests 21–22) ──

    def test_21_persistence_rooted_tree_state(self):
        state = make_persistent_segment_tree_state(size=10, persistence_mode=PersistenceMode.FULLY_PERSISTENT, num_versions=5)
        self.assertTrue(state.attributes["is_rooted_tree"])
        self.assertEqual(state.attributes["persistence_mode"], PersistenceMode.FULLY_PERSISTENT)

    def test_22_gate_e_persistent_version_out_of_bounds(self):
        spec = {"objective": "PERSISTENT_SEGMENT_TREE"}
        res = self.engine.process(spec, context={"query_version": 5, "num_versions": 3})
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "VERSION_ROOT_OUT_OF_BOUNDS")

    # ── 7. Dynamic SegTree & Gate F Tests (Tests 23–24) ──

    def test_23_dynamic_coordinate_domain_overflow_safe_midpoint(self):
        cd = CoordinateDomain(lower=1, upper=10**18)
        self.assertEqual(cd.midpoint(1, 10**18), 5 * 10**17)
        self.assertEqual(cd.midpoint(10**18 - 10, 10**18), 10**18 - 5)

    def test_24_gate_f_dynamic_segtree_node_limit_exceeded(self):
        spec = {"objective": "DYNAMIC_SEGMENT_TREE"}
        res = self.engine.process(spec, context={"allocated_nodes": 1000005, "max_capacity": 1000000})
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "NODE_ALLOCATION_LIMIT_EXCEEDED")

    # ── 8. Merge Sort Tree & Gate D Tests (Test 25) ──

    def test_25_gate_d_merge_sort_tree_static_immutability(self):
        spec = {
            "objective": "MERGE_SORT_TREE",
            "is_static": False
        }
        res = self.engine.process(spec, context={"has_updates": True})
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "MUTATION_NOT_SUPPORTED_ON_STATIC_STRUCTURE")

    # ── 9. Segment Tree Beats & Gate I Tests (Test 26) ──

    def test_26_gate_i_beats_second_max_tag_violation(self):
        spec = {"objective": "SEGMENT_TREE_BEATS"}
        # Violation: max2 >= max1 with has_second_max = True
        res = self.engine.process(spec, context={"max1": 5, "max2": 5, "has_second_max": True})
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "SEGMENT_BEATS_TAG_VIOLATION")


if __name__ == "__main__":
    unittest.main()
