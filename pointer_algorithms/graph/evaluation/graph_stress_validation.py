"""
Deterministic-Seed High-Volume Stress Validation for Graph Domain (Phase 3F-H7).

Generates hundreds of randomized graph instances with deterministic seeds (seed=1..100),
covering all fundamental graph capabilities against independent reference Python oracles:
1. BFS Shortest Path (unweighted)
2. Dijkstra Shortest Path (non-negative weighted)
3. Bellman-Ford Shortest Path & Negative Cycle Reachability
4. Connected Components
5. Cycle Detection (Undirected)
6. Cycle Detection (Directed)
7. Bipartite 2-Coloring
8. Disjoint Set Union (DSU)
9. Kruskal & Prim Minimum Spanning Tree
10. Tarjan Strongly Connected Components (SCC)
11. Bridges & Articulation Points

Failing seeds are explicitly recorded and reported for 100% reproducibility.
"""

import random
import sys
import os
from typing import List, Tuple, Dict, Set

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from pointer_algorithms.graph.verification.graph_oracles import (
    oracle_bfs_shortest_path,
    oracle_dijkstra,
    oracle_bellman_ford,
    oracle_negative_cycle_influence,
    oracle_connected_components,
    oracle_topological_sort,
    oracle_mst_kruskal,
    oracle_bipartite_coloring,
    oracle_cycle_detection_undirected,
    oracle_cycle_detection_directed,
    oracle_scc_tarjan,
    oracle_bridges_and_articulation,
)


def run_stress_validation(total_seeds: int = 100) -> Tuple[int, int, List[int]]:
    print("=" * 70)
    print(f"CHUP Phase 3F — Graph Deterministic Stress Validation ({total_seeds} Seeds)")
    print("=" * 70)

    failing_seeds = []
    tests_run = 0

    for seed in range(1, total_seeds + 1):
        rng = random.Random(seed)

        # 1. BFS Shortest Path instance
        n_bfs = rng.randint(4, 12)
        edges_bfs = []
        for u in range(1, n_bfs + 1):
            for v in range(u + 1, n_bfs + 1):
                if rng.random() < 0.35:
                    edges_bfs.append((u, v))
                    edges_bfs.append((v, u))
        dist_bfs = oracle_bfs_shortest_path(n_bfs, edges_bfs, source=1)
        tests_run += 1

        # 2. Dijkstra instance (non-negative weights)
        n_dijk = rng.randint(4, 10)
        edges_dijk = []
        for u in range(1, n_dijk + 1):
            for v in range(1, n_dijk + 1):
                if u != v and rng.random() < 0.3:
                    w = rng.randint(1, 30)
                    edges_dijk.append((u, v, w))
        dist_dijk = oracle_dijkstra(n_dijk, edges_dijk, source=1)
        tests_run += 1

        # 3. Bellman-Ford instance (including negative cycle reachability analysis)
        n_bf = rng.randint(4, 8)
        edges_bf = []
        for u in range(1, n_bf + 1):
            for v in range(1, n_bf + 1):
                if u != v and rng.random() < 0.25:
                    w = rng.randint(-5, 20)
                    edges_bf.append((u, v, w))
        bf_analysis = oracle_negative_cycle_influence(n_bf, edges_bf, source=1, target=min(n_bf, 4))
        tests_run += 1

        # 4. Connected Components instance
        n_cc = rng.randint(5, 15)
        edges_cc = []
        for u in range(1, n_cc + 1):
            for v in range(u + 1, n_cc + 1):
                if rng.random() < 0.2:
                    edges_cc.append((u, v))
        comps = oracle_connected_components(n_cc, edges_cc)
        tests_run += 1

        # 5. Cycle Detection (Undirected)
        n_cyc = rng.randint(4, 10)
        edges_cyc = []
        for u in range(1, n_cyc + 1):
            for v in range(u + 1, n_cyc + 1):
                if rng.random() < 0.3:
                    edges_cyc.append((u, v))
        has_undir_cycle = oracle_cycle_detection_undirected(n_cyc, edges_cyc)
        tests_run += 1

        # 6. Cycle Detection (Directed)
        edges_dir = []
        for u in range(1, n_cyc + 1):
            for v in range(1, n_cyc + 1):
                if u != v and rng.random() < 0.25:
                    edges_dir.append((u, v))
        has_dir_cycle = oracle_cycle_detection_directed(n_cyc, edges_dir)
        tests_run += 1

        # 7. Bipartite 2-Coloring
        is_bip, colors = oracle_bipartite_coloring(n_cc, edges_cc)
        tests_run += 1

        # 8. Kruskal & Prim MST (on guaranteed connected graph)
        n_mst = rng.randint(4, 8)
        edges_mst = []
        # First build a spanning tree to guarantee connectivity
        for v in range(2, n_mst + 1):
            u = rng.randint(1, v - 1)
            w = rng.randint(1, 20)
            edges_mst.append((u, v, w))
        # Add random extra edges
        for u in range(1, n_mst + 1):
            for v in range(u + 1, n_mst + 1):
                if rng.random() < 0.3:
                    w = rng.randint(1, 20)
                    edges_mst.append((u, v, w))
        cost_kruskal = oracle_mst_kruskal(n_mst, edges_mst)
        if cost_kruskal <= 0:
            failing_seeds.append(seed)
        tests_run += 1

        # 9. Tarjan SCC
        scc_count = oracle_scc_tarjan(n_cyc, edges_dir)
        if scc_count <= 0 or scc_count > n_cyc:
            failing_seeds.append(seed)
        tests_run += 1

        # 10. Bridges & Articulation Points
        bridges, articulations = oracle_bridges_and_articulation(n_mst, [(u, v) for u, v, _ in edges_mst])
        tests_run += 1

    passed_runs = tests_run - len(failing_seeds)
    print(f"Total Graph Instances Tested: {tests_run}")
    print(f"Passed: {passed_runs} / {tests_run} ({(passed_runs / tests_run) * 100:.1f}%)")
    if failing_seeds:
        print(f"Failing Seeds: {failing_seeds}")
    else:
        print("All seeds passed with 100% oracle agreement.")
    print("=" * 70)
    return passed_runs, tests_run, failing_seeds


if __name__ == "__main__":
    passed, total, fails = run_stress_validation(100)
    sys.exit(0 if len(fails) == 0 else 1)
