"""
CHUP Phase 3S — Positive Component Composition Tests (8 Scenarios).

Verifies multi-component algorithmic pipelines and state contract transitions across
advanced data structures without monolithic shortcuts.
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


class TestADSComposition(unittest.TestCase):
    def setUp(self):
        self.engine = AdvancedDataStructureDerivationEngine()

    def test_comp_01_hld_segment_tree_path_query(self):
        """Pipeline 1: Tree -> HLD -> SegmentTreeState -> PathQuery"""
        spec = {
            "objective": "HEAVY_LIGHT_DECOMPOSITION",
            "topology_state": "VALID_TREE",
            "path_value_domain": "VERTEX_VALUES",
            "has_range_provider": True
        }
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["optimal_candidate"], "heavy_light_decomposition")

        edges = [(0, 1), (1, 2), (2, 3), (0, 4)]
        vals = [5, 10, 15, 20, 25]
        queries = [("query", 3, 4), ("update", 2, 50), ("query", 3, 4)]
        ans = oracle_heavy_light_decomposition(5, edges, vals, queries, is_edge_values=False)
        self.assertEqual(ans, [75, 110])

    def test_comp_02_lca_binary_lifting_distance(self):
        """Pipeline 2: Tree -> BinaryLiftingLCAState -> DistanceQuery"""
        spec = {
            "objective": "LCA_BINARY_LIFTING",
            "topology_state": "VALID_TREE"
        }
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["optimal_candidate"], "binary_lifting_lca")

        edges = [(0, 1), (0, 2), (1, 3), (2, 4)]
        ans = oracle_lca_binary_lifting(5, edges, [(3, 4), (1, 3)])
        self.assertEqual(ans, [0, 1])

    def test_comp_03_persistent_version_tree_branching(self):
        """Pipeline 3: Array -> Rooted Version Tree -> PersistentSegmentTreeState -> HistoricalQuery"""
        spec = {
            "objective": "PERSISTENT_SEGMENT_TREE",
            "persistence_mode": "FULLY_PERSISTENT"
        }
        res = self.engine.process(spec, context={"query_version": 2, "num_versions": 4})
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["optimal_candidate"], "persistent_segment_tree")

        initial = [10, 20, 30]
        # v1 branches from v0 at index 1 -> [10, 100, 30]
        # v2 branches from v0 at index 0 -> [50, 20, 30]
        # v3 branches from v1 at index 2 -> [10, 100, 90]
        updates = [(0, 1, 100), (0, 0, 50), (1, 2, 90)]
        queries = [(0, 0, 2), (1, 0, 2), (2, 0, 2), (3, 0, 2)]
        ans = oracle_persistent_segment_tree(initial, updates, queries)
        self.assertEqual(ans, [60, 140, 100, 200])

    def test_comp_04_dynamic_sparse_coordinate_domain(self):
        """Pipeline 4: CoordinateDomain([1, 10^18]) -> DynamicSegmentTreeState -> SparsePointUpdate -> Query"""
        spec = {
            "objective": "DYNAMIC_SEGMENT_TREE",
            "coordinate_domain": {"lower": 1, "upper": 10**18}
        }
        res = self.engine.process(spec, context={"allocated_nodes": 50, "max_capacity": 10**5})
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["optimal_candidate"], "dynamic_sparse_segment_tree")

        updates = [(10**12, 100), (10**15, 200)]
        queries = [(1, 10**13), (10**13 + 1, 10**16), (1, 10**18)]
        ans = oracle_dynamic_segment_tree(1, 10**18, updates, queries)
        self.assertEqual(ans, [100, 200, 300])

    def test_comp_05_centroid_decomposition_ancestor_distance(self):
        """Pipeline 5: Tree -> CentroidTreeState -> AncestorDistanceTable -> PathMetric"""
        spec = {
            "objective": "CENTROID_DECOMPOSITION",
            "topology_state": "VALID_TREE"
        }
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["optimal_candidate"], "centroid_tree_builder")

        edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
        c_parent, c_depth, dist_table = oracle_centroid_decomposition(5, edges)
        self.assertIn(1, dist_table[4]) # 1 is root centroid
        self.assertEqual(dist_table[4][1], 2) # dist from 4 to 1 is 2

    def test_comp_06_mos_offline_query_schedule_reversible(self):
        """Pipeline 6: Array -> OfflineQuerySet -> MoQueryScheduleState -> ReversibleTransition -> BatchResult"""
        spec = {
            "objective": "MOS_ALGORITHM",
            "query_mode": "OFFLINE",
            "mo_ordering_strategy": "STANDARD_BLOCK_SNAKE",
            "transition_cost": {"is_reversible": True}
        }
        res = self.engine.process(spec)
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["optimal_candidate"], "mos_algorithm_offline")

        arr = [1, 2, 1, 3, 2, 4, 1]
        queries = [(0, 2), (1, 4), (0, 6)]
        ans = oracle_mos_algorithm(arr, queries, "STANDARD_BLOCK_SNAKE")
        self.assertEqual(ans, [2, 3, 4])

    def test_comp_07_segment_tree_beats_chmin_current_max(self):
        """Pipeline 7: Array -> SegmentTreeBeatsState -> RangeChmin -> CurrentMaxHierarchy -> Query"""
        spec = {
            "objective": "SEGMENT_TREE_BEATS",
            "supported_ops": ["RANGE_CHMIN", "RANGE_SUM_QUERY", "RANGE_MAX_QUERY"]
        }
        res = self.engine.process(spec, context={"max1": 10, "max2": 5, "has_second_max": True})
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["optimal_candidate"], "segment_tree_beats_chmin")

        arr = [10, 10, 8, 4]
        ops = [("query_sum", 0, 3, None), ("chmin", 0, 2, 9), ("query_sum", 0, 3, None)]
        ans = oracle_segment_tree_beats(arr, ops)
        self.assertEqual(ans, [32, 30])

    def test_comp_08_merge_sort_tree_order_statistic(self):
        """Pipeline 8: Array -> MergeSortTreeState -> RangeCountLeq"""
        spec = {
            "objective": "MERGE_SORT_TREE",
            "is_static": True,
            "order_statistic_objective": "COUNT_LEQ"
        }
        res = self.engine.process(spec, context={"has_updates": False})
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["optimal_candidate"], "merge_sort_tree")

        arr = [3, 8, 2, 9, 1, 5]
        ans = oracle_merge_sort_tree(arr, [(0, 5, 4), (1, 4, 8)])
        self.assertEqual(ans, [3, 3])


if __name__ == "__main__":
    unittest.main()
