"""
CHUP Phase 3S — Discrimination Holdout Suite (12 Cross-Family Discrimination Tests: ADS-D-01..12).

Verifies that the system discriminates fine-grained algorithmic boundaries, selecting
the mathematically and asymptotically optimal component over plausible alternatives:
- Sparse Table over Segment Tree for static RMQ (O(1) query)
- Prefix Sum over Sparse Table for invertible associative sum (O(N) vs O(N log N) space)
- HLD over repeated DFS for multi-query tree path updates
- Mo's Algorithm over naive sliding windows for arbitrary offline intervals
- Segment Tree Beats over ordinary Lazy Segment Tree for range chmin
- Persistent Segment Tree over array copies for versioned queries
"""

import unittest
from pointer_algorithms.adv_data_structures.derivation_engine import (
    AdvancedDataStructureDerivationEngine,
)
from pointer_algorithms.adv_data_structures.derivation.candidate_evaluator import (
    CandidateVerdict,
)


class TestADSDiscriminationHoldout(unittest.TestCase):
    def setUp(self):
        self.engine = AdvancedDataStructureDerivationEngine()

    def test_ADS_D_01_static_rmq_prefers_sparse_table_over_segtree(self):
        """Static array with idempotent min favors Sparse Table O(1) query over SegTree O(log N)."""
        spec = {
            "objective": "SPARSE_TABLE_RMQ",
            "is_static": True,
            "algebraic_properties": {"operation": "min"}
        }
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "sparse_table_rmq")

    def test_ADS_D_02_invertible_sum_rejects_sparse_table(self):
        """Static sum is invertible but not idempotent; rejects O(1) Sparse Table."""
        spec = {
            "objective": "SPARSE_TABLE_RMQ",
            "algebraic_properties": {"operation": "sum"}
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "NON_IDEMPOTENT_OPERATION_REJECTS_O1_SPARSE_TABLE")

    def test_ADS_D_03_tree_path_updates_selects_hld(self):
        """Heavy-Light Decomposition selected for multiple dynamic path queries on trees."""
        spec = {
            "objective": "HEAVY_LIGHT_DECOMPOSITION",
            "topology_state": "VALID_TREE",
            "has_range_provider": True
        }
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "heavy_light_decomposition")

    def test_ADS_D_04_offline_batch_distinct_selects_mos(self):
        """Offline query batches favor Mo's algorithm with O((N+Q)sqrt(N)) over repeated set scans."""
        spec = {
            "objective": "MOS_ALGORITHM",
            "query_mode": "OFFLINE",
            "transition_cost": {"is_reversible": True}
        }
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "mos_algorithm_offline")

    def test_ADS_D_05_range_chmin_selects_beats_over_standard_lazy(self):
        """Range chmin requires tag break conditions (max1, max2); selects Segment Tree Beats."""
        spec = {
            "objective": "SEGMENT_TREE_BEATS",
            "supported_ops": ["RANGE_CHMIN", "RANGE_SUM_QUERY", "RANGE_MAX_QUERY"]
        }
        res = self.engine.process(spec, context={"max1": 10, "max2": 5, "has_second_max": True})
        self.assertEqual(res["optimal_candidate"], "segment_tree_beats_chmin")

    def test_ADS_D_06_versioned_history_selects_persistent_tree(self):
        """Historical version queries select Persistent Segment Tree over repeated array snapshots."""
        spec = {
            "objective": "PERSISTENT_SEGMENT_TREE",
            "persistence_mode": "PARTIALLY_PERSISTENT"
        }
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "persistent_segment_tree")

    def test_ADS_D_07_extreme_coordinate_range_selects_dynamic_tree(self):
        """Coordinates up to 10^18 select Dynamic Segment Tree with lazy pointer allocation."""
        spec = {
            "objective": "DYNAMIC_SEGMENT_TREE",
            "coordinate_domain": {"lower": 1, "upper": 10**18}
        }
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "dynamic_sparse_segment_tree")

    def test_ADS_D_08_static_rank_selects_merge_sort_tree(self):
        """Static range count <= X selects Merge Sort Tree over dynamic structures."""
        spec = {
            "objective": "MERGE_SORT_TREE",
            "is_static": True
        }
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "merge_sort_tree")

    def test_ADS_D_09_suboptimal_sqrt_decomp_candidate(self):
        """Sqrt block decomposition recognized as valid suboptimal candidate for range queries."""
        spec = {
            "objective": "SPARSE_TABLE_RMQ",
            "algebraic_properties": {"operation": "min"}
        }
        res = self.engine.process(spec)
        evals = {r.component_name: r.verdict for r in res["evaluation_results"]}
        self.assertEqual(evals.get("sparse_table_rmq"), CandidateVerdict.VALID_OPTIMAL)
        self.assertEqual(evals.get("sqrt_block_decomposition"), CandidateVerdict.VALID_SUBOPTIMAL)

    def test_ADS_D_10_centroid_selected_for_balanced_tree_divide_and_conquer(self):
        """Tree-wide path distance inquiries select Centroid Decomposition."""
        spec = {
            "objective": "CENTROID_DECOMPOSITION",
            "topology_state": "VALID_TREE"
        }
        res = self.engine.process(spec)
        self.assertEqual(res["optimal_candidate"], "centroid_tree_builder")

    def test_ADS_D_11_lca_binary_lifting_vs_hld_tradeoff(self):
        """LCA Binary Lifting recognized as valid suboptimal alternative for pure path queries."""
        spec = {
            "objective": "HEAVY_LIGHT_DECOMPOSITION",
            "has_range_provider": True
        }
        res = self.engine.process(spec)
        evals = {r.component_name: r.verdict for r in res["evaluation_results"]}
        self.assertEqual(evals.get("heavy_light_decomposition"), CandidateVerdict.VALID_OPTIMAL)
        self.assertEqual(evals.get("binary_lifting_lca"), CandidateVerdict.VALID_SUBOPTIMAL)

    def test_ADS_D_12_irreversible_transitions_rejects_mos(self):
        """Non-reversible interval updates reject Mo's algorithm regardless of offline queries."""
        spec = {
            "objective": "MOS_ALGORITHM",
            "query_mode": "OFFLINE",
            "transition_cost": {"is_reversible": False}
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "IRREVERSIBLE_INTERVAL_TRANSITION")


if __name__ == "__main__":
    unittest.main()
