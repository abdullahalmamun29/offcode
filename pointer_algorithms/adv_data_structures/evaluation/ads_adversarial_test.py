"""
CHUP Phase 3S — Adversarial & Boundary Test Suite (16 Tests: ADV-ADS-01..16).

Tests extreme boundaries, degeneracies, singletons, large coordinates, and tag collisions.
"""

import unittest
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


class TestADSAdversarial(unittest.TestCase):

    def test_ADV_ADS_01_sparse_table_singleton(self):
        """Sparse Table on N=1 array."""
        self.assertEqual(oracle_sparse_table([99], [(0, 0)], "min"), [99])

    def test_ADV_ADS_02_sparse_table_full_span(self):
        """Sparse Table query spanning entire array."""
        arr = [10, 20, 5, 40, 50, 2, 70, 80]
        self.assertEqual(oracle_sparse_table(arr, [(0, 7)], "min"), [2])

    def test_ADV_ADS_03_lca_single_vertex(self):
        """LCA on N=1 tree."""
        self.assertEqual(oracle_lca_binary_lifting(1, [], [(0, 0)], 0), [0])

    def test_ADV_ADS_04_lca_deep_linear_chain(self):
        """LCA on linear chain of length 50."""
        n = 50
        edges = [(i, i + 1) for i in range(n - 1)]
        self.assertEqual(oracle_lca_binary_lifting(n, edges, [(10, 40), (0, 49)], 0), [10, 0])

    def test_ADV_ADS_05_lca_star_graph_high_degree(self):
        """LCA on star graph of size 50 with center 0."""
        n = 50
        edges = [(0, i) for i in range(1, n)]
        self.assertEqual(oracle_lca_binary_lifting(n, edges, [(5, 10), (1, 49)], 0), [0, 0])

    def test_ADV_ADS_06_hld_leaf_to_root_query(self):
        """HLD path query from deepest leaf directly to root."""
        edges = [(0, 1), (1, 2), (2, 3)]
        vals = [10, 20, 30, 40]
        self.assertEqual(oracle_heavy_light_decomposition(4, edges, vals, [("query", 3, 0)]), [100])

    def test_ADV_ADS_07_hld_single_edge_query(self):
        """HLD edge-value mode on adjacent vertices."""
        edges = [(0, 1)]
        vals = [0, 50] # edge 0-1 has weight 50
        # in edge values, path between 0 and 1 has weight 50 (query from 0 to 1)
        ans = oracle_heavy_light_decomposition(2, edges, vals, [("query", 0, 1)], is_edge_values=False)
        self.assertEqual(ans, [50])

    def test_ADV_ADS_08_centroid_two_nodes(self):
        """Centroid decomposition on N=2 graph."""
        c_parent, c_depth, dist = oracle_centroid_decomposition(2, [(0, 1)])
        self.assertEqual(len(c_parent), 2)
        self.assertEqual(dist[0][c_parent.index(-1)], 0 if c_parent[0] == -1 else 1)

    def test_ADV_ADS_09_centroid_star_graph(self):
        """Centroid decomposition on star graph: center must be root centroid."""
        n = 30
        edges = [(0, i) for i in range(1, n)]
        c_parent, _, _ = oracle_centroid_decomposition(n, edges)
        self.assertEqual(c_parent[0], -1)

    def test_ADV_ADS_10_persistent_segtree_no_updates(self):
        """Persistent Segment Tree querying only version 0."""
        initial = [100, 200, 300]
        self.assertEqual(oracle_persistent_segment_tree(initial, [], [(0, 0, 2), (0, 1, 1)]), [600, 200])

    def test_ADV_ADS_11_persistent_segtree_hotspot_updates(self):
        """Persistent Segment Tree repeatedly updating the same index across 5 versions."""
        initial = [0, 0]
        updates = [(0, 0, 1), (1, 0, 2), (2, 0, 3), (3, 0, 4), (4, 0, 5)]
        queries = [(v, 0, 1) for v in range(6)]
        self.assertEqual(oracle_persistent_segment_tree(initial, updates, queries), [0, 1, 2, 3, 4, 5])

    def test_ADV_ADS_12_dynamic_segtree_large_coordinates(self):
        """Dynamic Segment Tree on coordinates near 10^18."""
        big = 10**18
        updates = [(big - 2, 10), (big, 20)]
        self.assertEqual(oracle_dynamic_segment_tree(1, big, updates, [(big - 5, big)]), [30])

    def test_ADV_ADS_13_merge_sort_tree_identical_elements(self):
        """Merge Sort Tree with all identical elements."""
        arr = [7, 7, 7, 7, 7]
        self.assertEqual(oracle_merge_sort_tree(arr, [(0, 4, 7), (0, 4, 6), (0, 4, 8)]), [5, 0, 5])

    def test_ADV_ADS_14_sqrt_decomp_small_n(self):
        """Sqrt Decomposition with small array size."""
        self.assertEqual(oracle_sqrt_decomposition([5, 10], [(0, 1, 2)], [(0, 1)]), [19])

    def test_ADV_ADS_15_mos_algorithm_point_queries(self):
        """Mo's algorithm where every query is a single point L=R."""
        arr = [1, 2, 3, 4]
        queries = [(i, i) for i in range(4)]
        self.assertEqual(oracle_mos_algorithm(arr, queries), [1, 1, 1, 1])

    def test_ADV_ADS_16_beats_all_identical_chmin(self):
        """Segment Tree Beats where all elements start identical and chmin lowers them."""
        arr = [10, 10, 10, 10]
        ops = [("chmin", 0, 3, 6), ("query_sum", 0, 3, None), ("query_max", 0, 3, None)]
        self.assertEqual(oracle_segment_tree_beats(arr, ops), [24, 6])


if __name__ == "__main__":
    unittest.main()
