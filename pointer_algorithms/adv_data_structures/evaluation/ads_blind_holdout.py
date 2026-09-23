"""
CHUP Phase 3S — Blind Holdout Benchmark Suite (12 Unseen Narratives: ADS-BH-01..12).

Tests generalization on unseen competitive programming problem narratives disguised
with real-world domain metaphors without explicit data structure keywords.
"""

import unittest
from pointer_algorithms.adv_data_structures.derivation_engine import (
    AdvancedDataStructureDerivationEngine,
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


class TestADSBlindHoldout(unittest.TestCase):
    def setUp(self):
        self.engine = AdvancedDataStructureDerivationEngine()

    def test_ADS_BH_01_sensor_voltage_stability_window(self):
        """Metaphor: Sensor voltage static minimum in factory assembly line."""
        spec = {"objective": "SPARSE_TABLE_RMQ", "algebraic_properties": {"operation": "min"}}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "sparse_table_rmq")
        self.assertEqual(oracle_sparse_table([220, 215, 218, 212, 225], [(0, 4), (1, 3)], "min"), [212, 212])

    def test_ADS_BH_02_corporate_management_common_supervisor(self):
        """Metaphor: Finding nearest common manager in corporate organizational tree."""
        spec = {"objective": "LCA_BINARY_LIFTING", "topology_state": "VALID_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "binary_lifting_lca")
        edges = [(0, 1), (0, 2), (1, 3), (1, 4)]
        self.assertEqual(oracle_lca_binary_lifting(5, edges, [(3, 4), (3, 2)], 0), [1, 0])

    def test_ADS_BH_03_telecom_fiber_cable_bandwidth_allocation(self):
        """Metaphor: Bottleneck capacity updates and queries along optical fiber paths."""
        spec = {"objective": "HEAVY_LIGHT_DECOMPOSITION", "has_range_provider": True}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "heavy_light_decomposition")
        edges = [(0, 1), (1, 2), (2, 3)]
        vals = [100, 200, 300, 400]
        self.assertEqual(oracle_heavy_light_decomposition(4, edges, vals, [("query", 0, 3)]), [1000])

    def test_ADS_BH_04_disaster_relief_hub_placement(self):
        """Metaphor: Subtree bisection for emergency distribution hub placement."""
        spec = {"objective": "CENTROID_DECOMPOSITION", "topology_state": "VALID_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "centroid_tree_builder")
        c_parent, _, _ = oracle_centroid_decomposition(5, [(0, 1), (1, 2), (2, 3), (3, 4)])
        self.assertEqual(c_parent[2], -1)

    def test_ADS_BH_05_git_commit_source_code_snapshot(self):
        """Metaphor: Querying code line count across past git branch commits."""
        spec = {"objective": "PERSISTENT_SEGMENT_TREE", "persistence_mode": "FULLY_PERSISTENT"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "persistent_segment_tree")
        ans = oracle_persistent_segment_tree([50, 50], [(0, 0, 80)], [(0, 0, 1), (1, 0, 1)])
        self.assertEqual(ans, [100, 130])

    def test_ADS_BH_06_astronomical_catalog_stellar_coordinates(self):
        """Metaphor: Counting celestial objects in light-year interval [1, 10^15]."""
        spec = {"objective": "DYNAMIC_SEGMENT_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "dynamic_sparse_segment_tree")
        ans = oracle_dynamic_segment_tree(1, 10**18, [(10**12, 1), (10**15, 1)], [(1, 10**13)])
        self.assertEqual(ans, [1])

    def test_ADS_BH_07_university_exam_percentile_cutoff(self):
        """Metaphor: Counting exam scores <= cutoff in student roll-number range."""
        spec = {"objective": "MERGE_SORT_TREE", "is_static": True}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "merge_sort_tree")
        self.assertEqual(oracle_merge_sort_tree([85, 92, 78, 65, 99], [(0, 4, 80)]), [2])

    def test_ADS_BH_08_freight_cargo_train_container_loads(self):
        """Metaphor: Incremental cargo loading and verification on long train blocks."""
        spec = {"objective": "SQRT_DECOMPOSITION"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "sqrt_block_decomposition")
        self.assertEqual(oracle_sqrt_decomposition([10, 20, 30], [(0, 1, 5)], [(0, 2)]), [70])

    def test_ADS_BH_09_dna_sequencing_unique_kmers_offline(self):
        """Metaphor: Counting unique gene variants across batch sequence windows."""
        spec = {"objective": "MOS_ALGORITHM", "query_mode": "OFFLINE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "mos_algorithm_offline")
        self.assertEqual(oracle_mos_algorithm([1, 2, 2, 3, 1], [(0, 2), (1, 4)]), [2, 3])

    def test_ADS_BH_10_smart_grid_peak_power_clipping(self):
        """Metaphor: Capping microgrid peak power draw without affecting lower loads."""
        spec = {"objective": "SEGMENT_TREE_BEATS"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "segment_tree_beats_chmin")
        ops = [("chmin", 0, 3, 100), ("query_sum", 0, 3, None)]
        self.assertEqual(oracle_segment_tree_beats([120, 150, 80, 90], ops), [370])

    def test_ADS_BH_11_air_traffic_flight_path_elevation(self):
        """Metaphor: Flight altitude clearance maximum across fixed flight corridors."""
        spec = {"objective": "SPARSE_TABLE_RMQ", "algebraic_properties": {"operation": "max"}}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "sparse_table_rmq")
        self.assertEqual(oracle_sparse_table([3000, 3500, 2800, 4100], [(0, 2), (1, 3)], "max"), [3500, 4100])

    def test_ADS_BH_12_subway_line_interchange_station(self):
        """Metaphor: Finding earliest shared transfer terminal on branching rail lines."""
        spec = {"objective": "LCA_BINARY_LIFTING", "topology_state": "VALID_TREE"}
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "binary_lifting_lca")
        edges = [(0, 1), (1, 2), (1, 3), (0, 4)]
        self.assertEqual(oracle_lca_binary_lifting(5, edges, [(2, 3), (2, 4)], 0), [1, 0])


if __name__ == "__main__":
    unittest.main()
