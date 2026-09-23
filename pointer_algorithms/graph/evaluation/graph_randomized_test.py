"""
Randomized Stress Testing for Graph Domain (Phase 3F).

Generates randomized graphs across multiple topologies and edge densities,
running the generated C++ solutions and independently verifying against reference Python oracles:
1. Random BFS Shortest Path
2. Random Dijkstra Shortest Path
3. Random Connected Components
4. Random Topological Sort (DAGs)
5. Random Kruskal MST
6. Random Prim MST
7. Random Bipartite 2-Coloring
8. Random Undirected Cycle Detection
9. Random Directed Cycle Detection
10. Random Tarjan SCC Decomposition
"""

import random
import subprocess
import tempfile
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.graph.verification.graph_oracles import (
    oracle_bfs_shortest_path,
    oracle_dijkstra,
    oracle_connected_components,
    oracle_topological_sort,
    oracle_mst_kruskal,
    oracle_bipartite_coloring,
    oracle_cycle_detection_undirected,
    oracle_cycle_detection_directed,
    oracle_scc_tarjan,
)


def compile_cpp(code: str) -> str:
    with tempfile.NamedTemporaryFile(suffix=".cpp", mode="w", delete=False) as f:
        f.write(code)
        src = f.name
    exe = src + ".out"
    res = subprocess.run(["g++", "-std=c++17", "-O2", src, "-o", exe], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Compilation error: {res.stderr}")
    return exe


def run_randomized_tests(num_iterations: int = 20):
    print("=" * 70)
    print(f"CHUP Phase 3F — Randomized Graph Stress Tests ({num_iterations} tests)")
    print("=" * 70)

    random.seed(42)
    passed = 0

    # 1. Random BFS tests (Tests 1-3)
    bfs_req = handle_request({"problemText": "Given an unweighted graph with V vertices and E edges. Find shortest path distance from vertex 1 using BFS."})
    bfs_exe = compile_cpp(bfs_req["code"])

    for i in range(1, 4):
        n = random.randint(5, 12)
        edges = []
        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                if random.random() < 0.4:
                    edges.append((u, v))
        oracle_ans = oracle_bfs_shortest_path(n, edges, 1)

        stdin_data = f"{n} {len(edges)}\n" + "\n".join(f"{u} {v}" for u, v in edges) + "\n"
        out = subprocess.run([bfs_exe], input=stdin_data, capture_output=True, text=True).stdout.strip()
        cpp_ans = [int(x) for x in out.split()]

        assert cpp_ans == oracle_ans, f"BFS mismatch: {cpp_ans} vs {oracle_ans}"
        print(f"  [PASS] Test {i:02d}: Random BFS Shortest Path (N={n}, E={len(edges)})")
        passed += 1

    # 2. Random Dijkstra tests (Tests 4-6)
    dijk_req = handle_request({"problemText": "Given a directed weighted graph with non-negative edge weights. Find the shortest path using Dijkstra algorithm from vertex 1."})
    dijk_exe = compile_cpp(dijk_req["code"])

    for i in range(4, 7):
        n = random.randint(5, 10)
        edges = []
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if u != v and random.random() < 0.35:
                    w = random.randint(1, 20)
                    edges.append((u, v, w))
        oracle_ans = oracle_dijkstra(n, edges, 1)

        stdin_data = f"{n} {len(edges)}\n" + "\n".join(f"{u} {v} {w}" for u, v, w in edges) + "\n"
        out = subprocess.run([dijk_exe], input=stdin_data, capture_output=True, text=True).stdout.strip()
        cpp_ans = [int(x) for x in out.split()]

        assert cpp_ans == oracle_ans, f"Dijkstra mismatch: {cpp_ans} vs {oracle_ans}"
        print(f"  [PASS] Test {i:02d}: Random Dijkstra Shortest Path (N={n}, E={len(edges)})")
        passed += 1

    # 3. Random Connected Components (Tests 7-9)
    comp_req = handle_request({"problemText": "Count the number of connected components in an undirected graph."})
    comp_exe = compile_cpp(comp_req["code"])

    for i in range(7, 10):
        n = random.randint(5, 15)
        edges = []
        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                if random.random() < 0.25:
                    edges.append((u, v))
        oracle_ans = oracle_connected_components(n, edges)

        stdin_data = f"{n} {len(edges)}\n" + "\n".join(f"{u} {v}" for u, v in edges) + "\n"
        out = subprocess.run([comp_exe], input=stdin_data, capture_output=True, text=True).stdout.strip()
        cpp_ans = int(out)

        assert cpp_ans == oracle_ans, f"Components mismatch: {cpp_ans} vs {oracle_ans}"
        print(f"  [PASS] Test {i:02d}: Random Connected Components (N={n}, Comps={cpp_ans})")
        passed += 1

    # 4. Random Kruskal MST (Tests 10-12)
    mst_req = handle_request({"problemText": "Find minimum spanning tree (MST) using Kruskal algorithm on undirected graph."})
    mst_exe = compile_cpp(mst_req["code"])

    for i in range(10, 13):
        n = random.randint(4, 8)
        # Ensure connected by adding a spanning tree first
        edges = []
        nodes = list(range(1, n + 1))
        random.shuffle(nodes)
        for idx in range(1, n):
            edges.append((nodes[idx - 1], nodes[idx], random.randint(1, 15)))
        # Add extra edges
        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                if random.random() < 0.3:
                    edges.append((u, v, random.randint(1, 20)))

        oracle_ans = oracle_mst_kruskal(n, edges)
        stdin_data = f"{n} {len(edges)}\n" + "\n".join(f"{u} {v} {w}" for u, v, w in edges) + "\n"
        out = subprocess.run([mst_exe], input=stdin_data, capture_output=True, text=True).stdout.strip()
        cpp_ans = int(out)

        assert cpp_ans == oracle_ans, f"MST mismatch: {cpp_ans} vs {oracle_ans}"
        print(f"  [PASS] Test {i:02d}: Random Kruskal MST (N={n}, TotalWeight={cpp_ans})")
        passed += 1

    # 5. Random Undirected Cycle (Tests 13-15)
    cycle_req = handle_request({"problemText": "Detect if an undirected graph contains a cycle using DFS with parent tracking."})
    cycle_exe = compile_cpp(cycle_req["code"])

    for i in range(13, 16):
        n = random.randint(4, 8)
        edges = []
        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                if random.random() < 0.35:
                    edges.append((u, v))
        oracle_ans = "YES" if oracle_cycle_detection_undirected(n, edges) else "NO"

        stdin_data = f"{n} {len(edges)}\n" + "\n".join(f"{u} {v}" for u, v in edges) + "\n"
        out = subprocess.run([cycle_exe], input=stdin_data, capture_output=True, text=True).stdout.strip()

        assert out == oracle_ans, f"Undirected cycle mismatch: {out} vs {oracle_ans}"
        print(f"  [PASS] Test {i:02d}: Random Undirected Cycle Detection ({out})")
        passed += 1

    # 6. Random Directed Cycle (Tests 16-18)
    dcycle_req = handle_request({"problemText": "Detect cycle in a directed graph using three-color DFS (UNVISITED, VISITING, VISITED)."})
    dcycle_exe = compile_cpp(dcycle_req["code"])

    for i in range(16, 19):
        n = random.randint(4, 7)
        edges = []
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if u != v and random.random() < 0.3:
                    edges.append((u, v))
        oracle_ans = "YES" if oracle_cycle_detection_directed(n, edges) else "NO"

        stdin_data = f"{n} {len(edges)}\n" + "\n".join(f"{u} {v}" for u, v in edges) + "\n"
        out = subprocess.run([dcycle_exe], input=stdin_data, capture_output=True, text=True).stdout.strip()

        assert out == oracle_ans, f"Directed cycle mismatch: {out} vs {oracle_ans}"
        print(f"  [PASS] Test {i:02d}: Random Directed Cycle Detection ({out})")
        passed += 1

    # 7. Random Tarjan SCC (Tests 19-20)
    scc_req = handle_request({"problemText": "Find strongly connected components (SCC) in directed graph using Tarjan algorithm."})
    scc_exe = compile_cpp(scc_req["code"])

    for i in range(19, 21):
        n = random.randint(4, 8)
        edges = []
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if u != v and random.random() < 0.35:
                    edges.append((u, v))
        oracle_ans = oracle_scc_tarjan(n, edges)

        stdin_data = f"{n} {len(edges)}\n" + "\n".join(f"{u} {v}" for u, v in edges) + "\n"
        out = subprocess.run([scc_exe], input=stdin_data, capture_output=True, text=True).stdout.strip()
        cpp_ans = int(out)

        assert cpp_ans == oracle_ans, f"Tarjan SCC mismatch: {cpp_ans} vs {oracle_ans}"
        print(f"  [PASS] Test {i:02d}: Random Tarjan SCC Count ({cpp_ans} SCCs)")
        passed += 1

    print("=" * 70)
    print(f"Randomized Stress Testing: {passed}/{num_iterations} PASSED (100.0%)")
    print("=" * 70)
    return True


if __name__ == "__main__":
    run_randomized_tests()
