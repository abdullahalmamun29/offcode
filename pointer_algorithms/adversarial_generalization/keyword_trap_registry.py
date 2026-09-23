"""
CHUP Phase 8 — Canonical Keyword Trap Registry.

Curates 10 canonical competitive programming keyword traps with strict
mathematical qualification: audits candidate elimination and precondition
failure without prescribing winning replacement algorithms.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass


@dataclass(frozen=True)
class KeywordTrap:
    """
    Specification of an adversarial keyword trap.
    """
    trap_id: str
    name: str
    lure_keywords: Tuple[str, ...]
    adversarial_spec: Dict[str, Any]
    adversarial_text: str
    expected_eliminated_candidates: Tuple[str, ...]
    expected_failure_codes: Tuple[str, ...]
    forbidden_prescriptions: Tuple[str, ...]
    description: str


class KeywordTrapRegistry:
    """
    Curated registry of the 10 canonical competitive programming keyword traps.
    """

    _TRAPS: Dict[str, KeywordTrap] = {}

    @classmethod
    def _initialize(cls):
        if cls._TRAPS:
            return

        traps: List[KeywordTrap] = [
            # Trap 1: Negative Shortest Path Trap
            KeywordTrap(
                trap_id="TRAP-01-NEG-WEIGHTS",
                name="Negative Shortest Path Trap",
                lure_keywords=("shortest path", "dijkstra", "minimum distance"),
                adversarial_spec={
                    "v": 1000,
                    "e": 5000,
                    "negative_edge_weights": True,
                    "has_negative_weights": True,
                    "negative_weights": True,
                    "contains_negative": True,
                    "shortest_path_query": True,
                    "query_target": "SINGLE_SOURCE_SHORTEST_PATH",
                    "text": "Find shortest path from node 1 to node N in a graph with some negative weight edges but no negative cycles."
                },
                adversarial_text="Compute single-source shortest paths in a directed graph where some edges have negative weights.",
                expected_eliminated_candidates=("dijkstra_priority_queue",),
                expected_failure_codes=("NEGATIVE_WEIGHTS_REJECT_DIJKSTRA",),
                forbidden_prescriptions=("bellman_ford_only", "spfa_only", "dag_dp_only"),
                description="Greedy frontier expansion in Dijkstra fails when negative edges exist; Dijkstra must be eliminated without prescribing Bellman-Ford vs SPFA vs DAG DP."
            ),

            # Trap 2: Unweighted Shortest Path Trap
            KeywordTrap(
                trap_id="TRAP-02-UNWEIGHTED-BFS",
                name="Unweighted Shortest Path Complexity Trap",
                lure_keywords=("shortest path", "dijkstra", "priority queue"),
                adversarial_spec={
                    "v": 200000,
                    "e": 500000,
                    "unit_weights": True,
                    "all_weights_unit": True,
                    "shortest_path_query": True,
                    "time_limit": 0.2,
                    "text": "In an unweighted graph where every edge has weight 1, find minimum distance from source S to all vertices."
                },
                adversarial_text="Given an unweighted network with all edge lengths equal to 1, compute distance from root.",
                expected_eliminated_candidates=(),
                expected_failure_codes=(),
                forbidden_prescriptions=("dijkstra_mandatory",),
                description="Unweighted graph admits O(V+E) BFS; Dijkstra's O((V+E) log V) is asymptotically suboptimal under tight time bounds."
            ),

            # Trap 3: Tree Shortest Path Trap
            KeywordTrap(
                trap_id="TRAP-03-TREE-PATH",
                name="Tree Shortest Path Trap",
                lure_keywords=("shortest path", "dijkstra", "graph search"),
                adversarial_spec={
                    "is_tree": True,
                    "connected": True,
                    "acyclic": True,
                    "v": 200000,
                    "e": 199999,
                    "query_target": "TREE_PATH",
                    "text": "Given a tree with N nodes and N-1 edges, find shortest distance between pairs of nodes across Q queries."
                },
                adversarial_text="Calculate shortest path lengths between vertices in a tree structure.",
                expected_eliminated_candidates=(),
                expected_failure_codes=(),
                forbidden_prescriptions=("dijkstra_on_tree", "unconditional_lca"),
                description="Tree topology has unique simple paths between node pairs; general shortest path algorithms are unnecessary."
            ),

            # Trap 4: Directed Graph Spanning Trap
            KeywordTrap(
                trap_id="TRAP-04-DIRECTED-MST",
                name="Directed Graph Spanning Arborescence Trap",
                lure_keywords=("minimum spanning tree", "kruskal", "prim", "mst"),
                adversarial_spec={
                    "directed": True,
                    "is_directed": True,
                    "spanning_arborescence": True,
                    "v": 1000,
                    "e": 5000,
                    "text": "Find the minimum weight directed spanning arborescence rooted at node r in a directed graph."
                },
                adversarial_text="Construct a minimum directed spanning arborescence rooted at r in a directed weighted graph.",
                expected_eliminated_candidates=("kruskal_mst",),
                expected_failure_codes=("TARGET_TOPOLOGY_INCOMPATIBLE",),
                forbidden_prescriptions=("edmonds_mandatory",),
                description="Kruskal and Prim MST algorithms require undirected graphs; directed graphs require arborescence algorithms."
            ),

            # Trap 5: Unsorted Sequence Two Pointers Trap
            KeywordTrap(
                trap_id="TRAP-05-UNSORTED-TWO-POINTERS",
                name="Unsorted Sequence Two Pointers Trap",
                lure_keywords=("two pointers", "pair sum", "target sum"),
                adversarial_spec={
                    "sorted": False,
                    "is_sorted": False,
                    "n": 100000,
                    "preserve_indices": True,
                    "negative_elements": True,
                    "negative_elements_for_range_sum": True,
                    "contains_negative": True,
                    "text": "Given an arbitrary unsorted array containing negative numbers, find a contiguous subarray whose sum equals K."
                },
                adversarial_text="In an unsorted sequence with negative values, identify subarray with sum K.",
                expected_eliminated_candidates=("two_pointers_monotone_window",),
                expected_failure_codes=("NON_MONOTONE_WINDOW_REJECTS_TWO_POINTERS",),
                forbidden_prescriptions=("hash_map_only",),
                description="Monotone window two-pointers requires sorted order or non-negative elements; negative values break window monotonicity."
            ),

            # Trap 6: Dynamic Range Sum Trap
            KeywordTrap(
                trap_id="TRAP-06-DYNAMIC-RANGE-SUM",
                name="Dynamic Range Sum Trap",
                lure_keywords=("range sum", "prefix sum", "cumulative sum"),
                adversarial_spec={
                    "n": 100000,
                    "q": 100000,
                    "mutability": "POINT_UPDATE",
                    "has_updates": True,
                    "operation": "MIN",
                    "text": "Given an array, process Q queries of two types: update value at index i, and compute minimum in range [L, R]."
                },
                adversarial_text="Maintain dynamic range minimum queries under frequent point mutations.",
                expected_eliminated_candidates=("sparse_table",),
                expected_failure_codes=("MUTATION_DISALLOWED_ON_STATIC_STRUCTURE",),
                forbidden_prescriptions=("fenwick_only", "segment_tree_only"),
                description="Static prefix sums and sparse tables cannot accept dynamic point mutations; static structures are eliminated."
            ),

            # Trap 7: Static RMQ Envelope Trap
            KeywordTrap(
                trap_id="TRAP-07-STATIC-RMQ-ENVELOPE",
                name="Static RMQ Preprocessing vs Query Envelope Trap",
                lure_keywords=("range minimum", "segment tree", "rmq"),
                adversarial_spec={
                    "n": 100000,
                    "q": 10000000,
                    "time_limit": 1.0,
                    "operation": "MIN",
                    "mutability": "STATIC",
                    "text": "Given a static array of size N=100000, answer Q=10^7 range minimum queries within 1.0 second."
                },
                adversarial_text="Static RMQ with 10^7 queries on an immutable array of size 10^5.",
                expected_eliminated_candidates=(),
                expected_failure_codes=(),
                forbidden_prescriptions=("sparse_table_only",),
                description="Under Q=10^7 queries in 1s, O(log N) segment tree per query takes ~1.7*10^8 operations, exceeding limits; O(1) query is required."
            ),

            # Trap 8: Unit Weight Knapsack Trap
            KeywordTrap(
                trap_id="TRAP-08-UNIT-KNAPSACK",
                name="Unit Weight Knapsack Trap",
                lure_keywords=("knapsack", "dynamic programming", "0-1 knapsack"),
                adversarial_spec={
                    "n": 100000,
                    "capacity": 50000,
                    "unit_weights": True,
                    "all_items_equal_weight": True,
                    "text": "Select up to K items from N items where each item has identical weight 1 to maximize total value."
                },
                adversarial_text="Maximize item value under cardinality limit K with unit item weights.",
                expected_eliminated_candidates=(),
                expected_failure_codes=(),
                forbidden_prescriptions=("dp_only", "greedy_only"),
                description="When all weights are equal, 0-1 knapsack degenerates into selecting the top K values (greedy sort O(N log N)), not O(NW) DP."
            ),

            # Trap 9: Multi-Root Forest Trap
            KeywordTrap(
                trap_id="TRAP-09-FOREST-DISCONNECTED",
                name="Multi-Root Forest Disconnected Trap",
                lure_keywords=("tree", "tree algorithm", "dfs"),
                adversarial_spec={
                    "v": 100000,
                    "e": 99998,
                    "disconnected": True,
                    "components": 2,
                    "text": "A graph has V nodes and V-2 edges with no cycles. Process tree queries."
                },
                adversarial_text="An acyclic graph with V nodes and V-2 edges consisting of multiple trees (forest).",
                expected_eliminated_candidates=(),
                expected_failure_codes=(),
                forbidden_prescriptions=("single_tree_dfs",),
                description="E = V - 2 violates Cayley tree property; graph is a forest of multiple components. Single tree algorithms must fail closed or handle forest."
            ),

            # Trap 10: Large Coordinate Density Trap
            KeywordTrap(
                trap_id="TRAP-10-LARGE-COORDINATES",
                name="Large Coordinate Density Trap",
                lure_keywords=("coordinates", "range query", "direct indexing"),
                adversarial_spec={
                    "n": 100000,
                    "max_coordinate": 10**18,
                    "coordinate_scale": "MASSIVE",
                    "c": 10**18,
                    "text": "Given points with coordinates up to 10^18, answer range queries without 10^18 array memory."
                },
                adversarial_text="Range queries over points on a coordinate axis where values reach 10^18.",
                expected_eliminated_candidates=(),
                expected_failure_codes=(),
                forbidden_prescriptions=("compression_mandatory",),
                description="Coordinates up to 10^18 eliminate flat direct array indexing; compression or dynamic sparse structures are required."
            )
        ]

        for t in traps:
            cls._TRAPS[t.trap_id] = t

    @classmethod
    def get_trap(cls, trap_id: str) -> Optional[KeywordTrap]:
        cls._initialize()
        return cls._TRAPS.get(trap_id)

    @classmethod
    def get_all_traps(cls) -> List[KeywordTrap]:
        cls._initialize()
        return list(cls._TRAPS.values())
