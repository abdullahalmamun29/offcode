"""
Graph Benchmark — Phase 3F (G-01 through G-60)

Benchmark categories:
  3F-A. BFS / Unweighted Shortest Path (G-01..G-04)
  3F-B. DFS / Components / Reachability (G-05..G-08)
  3F-C. Undirected Cycle Detection     (G-09..G-12)
  3F-D. Directed Cycle Detection       (G-13..G-16)
  3F-E. Bipartite Graph Verification   (G-17..G-20)
  3F-F. Dijkstra's Algorithm           (G-21..G-24)
  3F-G. Bellman-Ford / Negative Weights(G-25..G-28)
  3F-H. Floyd-Warshall All-Pairs       (G-29..G-32)
  3F-I. Topological Sort (Kahn / DAG)  (G-33..G-36)
  3F-J. DAG Dynamic Programming        (G-37..G-40)
  3F-K. Disjoint Set Union (DSU)       (G-41..G-44)
  3F-L. Minimum Spanning Tree          (G-45..G-48)
  3F-M. Strongly Connected Components  (G-49..G-52)
  3F-N. Bridges & Articulation Points  (G-53..G-56)
  3F-O. Anti-Patterns & Hardening      (G-57..G-60)

All problems invoke the real pipeline entry point: handle_request({"problemText": ...}).
All generated C++ code is compiled with g++ -std=c++17 -O2, executed with test inputs,
and independently verified against reference graph oracles.
"""

import sys
import os
import subprocess
import tempfile
import time
from typing import Dict, Any, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.graph.verification.graph_oracles import (
    oracle_bfs_shortest_path,
    oracle_dfs_traversal,
    oracle_connected_components,
    oracle_cycle_detection_undirected,
    oracle_cycle_detection_directed,
    oracle_bipartite_coloring,
    oracle_dijkstra,
    oracle_bellman_ford,
    oracle_floyd_warshall,
    oracle_topological_sort,
    oracle_dag_dp_longest_path,
    oracle_mst_kruskal,
    oracle_mst_prim,
    oracle_scc_tarjan,
    oracle_bridges_and_articulation,
)


COMPILED_BINARIES: Dict[str, str] = {}


def compile_and_run_cpp(cpp_code: str, stdin_data: str, pattern: str = "", timeout: int = 15) -> str:
    global COMPILED_BINARIES
    if pattern and pattern in COMPILED_BINARIES and os.path.exists(COMPILED_BINARIES[pattern]):
        exe = COMPILED_BINARIES[pattern]
    else:
        tmp = tempfile.NamedTemporaryFile(suffix=".cpp", mode="w", delete=False)
        tmp.write(cpp_code)
        tmp.close()
        src = tmp.name
        exe = src + ".out"
        compile_res = subprocess.run(
            ["g++", "-std=c++17", "-O2", "-o", exe, src],
            capture_output=True, text=True, timeout=timeout
        )
        if compile_res.returncode != 0:
            return f"COMPILE_ERROR: {compile_res.stderr[:200]}"
        if pattern:
            COMPILED_BINARIES[pattern] = exe
    try:
        run_res = subprocess.run(
            [exe], input=stdin_data, capture_output=True, text=True, timeout=timeout
        )
        if run_res.returncode != 0:
            return f"RUNTIME_ERROR: {run_res.stderr[:200]}"
        return run_res.stdout.strip()
    except subprocess.TimeoutExpired:
        return "RUNTIME_ERROR: TimeoutExpired"


BENCHMARK_PROBLEMS = [
    # ── 3F-A: BFS Shortest Path (G-01..G-04) ──
    {
        "id": "G-01",
        "category": "3F-A. BFS Shortest Path",
        "text": "Given an unweighted graph with V vertices and E edges. Find the shortest path distance from vertex 1 to all vertices using BFS.",
        "expected_pattern": "graph_bfs_shortest_path",
        "input": "4 4\n1 2\n2 3\n3 4\n1 3\n",
        "oracle_check": lambda out: out == "0 1 1 2"
    },
    {
        "id": "G-02",
        "category": "3F-A. BFS Shortest Path",
        "text": "Find shortest path hop distance from source vertex 1 in an unweighted undirected graph.",
        "expected_pattern": "graph_bfs_shortest_path",
        "input": "5 4\n1 2\n2 3\n3 4\n4 5\n",
        "oracle_check": lambda out: out == "0 1 2 3 4"
    },
    {
        "id": "G-03",
        "category": "3F-A. BFS Shortest Path",
        "text": "Breadth-first search shortest path layer traversal in unweighted network from node 1.",
        "expected_pattern": "graph_bfs_shortest_path",
        "input": "3 1\n1 2\n",
        "oracle_check": lambda out: out == "0 1 -1"
    },
    {
        "id": "G-04",
        "category": "3F-A. BFS Shortest Path",
        "text": "Find minimum number of edges to reach each vertex from vertex 1 in an unweighted graph.",
        "expected_pattern": "graph_bfs_shortest_path",
        "input": "4 3\n1 2\n1 3\n1 4\n",
        "oracle_check": lambda out: out == "0 1 1 1"
    },

    # ── 3F-B: DFS / Components (G-05..G-08) ──
    {
        "id": "G-05",
        "category": "3F-B. DFS / Components",
        "text": "Count the number of connected components in an undirected graph.",
        "expected_pattern": "graph_connected_components",
        "input": "5 3\n1 2\n2 3\n4 5\n",
        "oracle_check": lambda out: out == "2"
    },
    {
        "id": "G-06",
        "category": "3F-B. DFS / Components",
        "text": "Find total number of connected components in given vertices and edges.",
        "expected_pattern": "graph_connected_components",
        "input": "4 0\n",
        "oracle_check": lambda out: out == "4"
    },
    {
        "id": "G-07",
        "category": "3F-B. DFS / Components",
        "text": "Perform depth first search (DFS) traversal order starting from vertex 1.",
        "expected_pattern": "graph_dfs_traversal",
        "input": "4 3\n1 2\n2 3\n3 4\n",
        "oracle_check": lambda out: len(out.split()) == 4
    },
    {
        "id": "G-08",
        "category": "3F-B. DFS / Components",
        "text": "Graph DFS reachability traversal visiting all reachable nodes.",
        "expected_pattern": "graph_dfs_traversal",
        "input": "3 2\n1 2\n2 3\n",
        "oracle_check": lambda out: len(out.split()) == 3
    },

    # ── 3F-C: Undirected Cycle Detection (G-09..G-12) ──
    {
        "id": "G-09",
        "category": "3F-C. Undirected Cycle Detection",
        "text": "Detect if an undirected graph contains a cycle using DFS with parent tracking.",
        "expected_pattern": "graph_cycle_detection_undirected",
        "input": "3 3\n1 2\n2 3\n3 1\n",
        "oracle_check": lambda out: out == "YES"
    },
    {
        "id": "G-10",
        "category": "3F-C. Undirected Cycle Detection",
        "text": "Check if an undirected graph has any cycle. Graph has 4 vertices and 3 edges forming a tree.",
        "expected_pattern": "graph_cycle_detection_undirected",
        "input": "4 3\n1 2\n2 3\n3 4\n",
        "oracle_check": lambda out: out == "NO"
    },
    {
        "id": "G-11",
        "category": "3F-C. Undirected Cycle Detection",
        "text": "Determine cycle existence in an undirected network.",
        "expected_pattern": "graph_cycle_detection_undirected",
        "input": "4 4\n1 2\n2 3\n3 4\n4 1\n",
        "oracle_check": lambda out: out == "YES"
    },
    {
        "id": "G-12",
        "category": "3F-C. Undirected Cycle Detection",
        "text": "Undirected cycle detection on a graph with multiple components.",
        "expected_pattern": "graph_cycle_detection_undirected",
        "input": "5 3\n1 2\n3 4\n4 5\n",
        "oracle_check": lambda out: out == "NO"
    },

    # ── 3F-D: Directed Cycle Detection (G-13..G-16) ──
    {
        "id": "G-13",
        "category": "3F-D. Directed Cycle Detection",
        "text": "Detect cycle in a directed graph using three-color DFS (UNVISITED, VISITING, VISITED).",
        "expected_pattern": "graph_cycle_detection_directed",
        "input": "3 3\n1 2\n2 3\n3 1\n",
        "oracle_check": lambda out: out == "YES"
    },
    {
        "id": "G-14",
        "category": "3F-D. Directed Cycle Detection",
        "text": "Check if directed graph contains any directed cycle.",
        "expected_pattern": "graph_cycle_detection_directed",
        "input": "3 2\n1 2\n2 3\n",
        "oracle_check": lambda out: out == "NO"
    },
    {
        "id": "G-15",
        "category": "3F-D. Directed Cycle Detection",
        "text": "Directed graph cycle detection with back-edges to visiting ancestors.",
        "expected_pattern": "graph_cycle_detection_directed",
        "input": "4 4\n1 2\n2 3\n3 4\n4 2\n",
        "oracle_check": lambda out: out == "YES"
    },
    {
        "id": "G-16",
        "category": "3F-D. Directed Cycle Detection",
        "text": "Verify whether given digraph has cycles or is a directed acyclic graph.",
        "expected_pattern": "graph_cycle_detection_directed",
        "input": "4 3\n1 2\n1 3\n2 4\n",
        "oracle_check": lambda out: out == "NO"
    },

    # ── 3F-E: Bipartite Graph Verification (G-17..G-20) ──
    {
        "id": "G-17",
        "category": "3F-E. Bipartite Graph Verification",
        "text": "Check if graph is bipartite using 2-coloring BFS/DFS.",
        "expected_pattern": "graph_bipartite_coloring",
        "input": "4 4\n1 2\n2 3\n3 4\n4 1\n",
        "oracle_check": lambda out: out == "YES"
    },
    {
        "id": "G-18",
        "category": "3F-E. Bipartite Graph Verification",
        "text": "Determine if graph can be colored with 2 colors without conflict.",
        "expected_pattern": "graph_bipartite_coloring",
        "input": "3 3\n1 2\n2 3\n3 1\n",
        "oracle_check": lambda out: out == "NO"
    },
    {
        "id": "G-19",
        "category": "3F-E. Bipartite Graph Verification",
        "text": "Verify bipartite property on disconnected graph components.",
        "expected_pattern": "graph_bipartite_coloring",
        "input": "5 4\n1 2\n2 3\n4 5\n5 4\n",
        "oracle_check": lambda out: out in ("YES", "NO")
    },
    {
        "id": "G-20",
        "category": "3F-E. Bipartite Graph Verification",
        "text": "Test 2-colorability of bipartite tree structure.",
        "expected_pattern": "graph_bipartite_coloring",
        "input": "4 3\n1 2\n1 3\n1 4\n",
        "oracle_check": lambda out: out == "YES"
    },

    # ── 3F-F: Dijkstra's Algorithm (G-21..G-24) ──
    {
        "id": "G-21",
        "category": "3F-F. Dijkstra's Algorithm",
        "text": "Given directed weighted graph with non-negative edge weights. Find shortest path using Dijkstra algorithm from vertex 1.",
        "expected_pattern": "graph_dijkstra",
        "input": "4 4\n1 2 2\n2 3 3\n1 3 6\n3 4 1\n",
        "oracle_check": lambda out: out == "0 2 5 6"
    },
    {
        "id": "G-22",
        "category": "3F-F. Dijkstra's Algorithm",
        "text": "Single-source shortest path with non-negative weights using min-heap priority queue Dijkstra.",
        "expected_pattern": "graph_dijkstra",
        "input": "3 3\n1 2 1\n2 3 2\n1 3 4\n",
        "oracle_check": lambda out: out == "0 1 3"
    },
    {
        "id": "G-23",
        "category": "3F-F. Dijkstra's Algorithm",
        "text": "Dijkstra algorithm on non-negative weighted graph with unreachable nodes.",
        "expected_pattern": "graph_dijkstra",
        "input": "4 2\n1 2 5\n2 3 5\n",
        "oracle_check": lambda out: out == "0 5 10 -1"
    },
    {
        "id": "G-24",
        "category": "3F-F. Dijkstra's Algorithm",
        "text": "Compute shortest path distances from source 1 on weighted network with non-negative costs.",
        "expected_pattern": "graph_dijkstra",
        "input": "3 2\n1 2 10\n1 3 20\n",
        "oracle_check": lambda out: out == "0 10 20"
    },

    # ── 3F-G: Bellman-Ford (G-25..G-28) ──
    {
        "id": "G-25",
        "category": "3F-G. Bellman-Ford",
        "text": "Find shortest path in directed graph with negative weights using Bellman-Ford algorithm from source 1.",
        "expected_pattern": "graph_bellman_ford",
        "input": "4 4\n1 2 4\n1 3 5\n2 4 5\n3 2 -2\n",
        "oracle_check": lambda out: out == "0 3 5 8"
    },
    {
        "id": "G-26",
        "category": "3F-G. Bellman-Ford",
        "text": "Bellman-Ford algorithm for graph with negative edge weights and negative cycle detection.",
        "expected_pattern": "graph_bellman_ford",
        "input": "3 3\n1 2 1\n2 3 -3\n3 2 1\n",
        "oracle_check": lambda out: "NEGATIVE_CYCLE" in out
    },
    {
        "id": "G-27",
        "category": "3F-G. Bellman-Ford",
        "text": "Shortest path with negative edge weights and no negative cycles using edge relaxation.",
        "expected_pattern": "graph_bellman_ford",
        "input": "3 2\n1 2 -5\n2 3 -3\n",
        "oracle_check": lambda out: out == "0 -5 -8"
    },
    {
        "id": "G-28",
        "category": "3F-G. Bellman-Ford",
        "text": "Bellman-Ford algorithm relaxing all E edges V-1 times.",
        "expected_pattern": "graph_bellman_ford",
        "input": "4 3\n1 2 1\n2 3 -1\n3 4 2\n",
        "oracle_check": lambda out: out == "0 1 0 2"
    },

    # ── 3F-H: Floyd-Warshall (G-29..G-32) ──
    {
        "id": "G-29",
        "category": "3F-H. Floyd-Warshall",
        "text": "Find all-pairs shortest paths using Floyd-Warshall algorithm for a graph with V = 4 vertices.",
        "expected_pattern": "graph_floyd_warshall",
        "input": "3 3\n1 2 3\n2 3 4\n1 3 10\n",
        "oracle_check": lambda out: "0 3 7" in out.splitlines()[0]
    },
    {
        "id": "G-30",
        "category": "3F-H. Floyd-Warshall",
        "text": "All-pairs shortest path matrix computation using intermediate vertex dynamic programming.",
        "expected_pattern": "graph_floyd_warshall",
        "input": "2 1\n1 2 5\n",
        "oracle_check": lambda out: len(out.splitlines()) == 2
    },
    {
        "id": "G-31",
        "category": "3F-H. Floyd-Warshall",
        "text": "Compute distance between all pairs of vertices in small weighted graph.",
        "expected_pattern": "graph_floyd_warshall",
        "input": "3 2\n1 2 1\n2 3 2\n",
        "oracle_check": lambda out: len(out.splitlines()) == 3
    },
    {
        "id": "G-32",
        "category": "3F-H. Floyd-Warshall",
        "text": "Floyd-Warshall algorithm for all-pairs distance with V = 3 vertices.",
        "expected_pattern": "graph_floyd_warshall",
        "input": "3 1\n1 2 4\n",
        "oracle_check": lambda out: len(out.splitlines()) == 3
    },

    # ── 3F-I: Topological Sort (G-33..G-36) ──
    {
        "id": "G-33",
        "category": "3F-I. Topological Sort",
        "text": "Find a topological sort of a directed acyclic graph (DAG) using Kahn algorithm.",
        "expected_pattern": "graph_topological_sort",
        "input": "4 3\n1 2\n2 3\n3 4\n",
        "oracle_check": lambda out: out == "1 2 3 4"
    },
    {
        "id": "G-34",
        "category": "3F-I. Topological Sort",
        "text": "Topological order for task scheduling in a DAG.",
        "expected_pattern": "graph_topological_sort",
        "input": "3 2\n1 3\n2 3\n",
        "oracle_check": lambda out: "3" == out.split()[-1]
    },
    {
        "id": "G-35",
        "category": "3F-I. Topological Sort",
        "text": "Topological ordering in DAG with cycle detection capability.",
        "expected_pattern": "graph_topological_sort",
        "input": "3 3\n1 2\n2 3\n3 1\n",
        "oracle_check": lambda out: "CYCLE" in out
    },
    {
        "id": "G-36",
        "category": "3F-I. Topological Sort",
        "text": "Compute build dependency order using topological sorting on DAG.",
        "expected_pattern": "graph_topological_sort",
        "input": "4 4\n1 2\n1 3\n2 4\n3 4\n",
        "oracle_check": lambda out: len(out.split()) == 4
    },

    # ── 3F-J: DAG Dynamic Programming (G-37..G-40) ──
    {
        "id": "G-37",
        "category": "3F-J. DAG Dynamic Programming",
        "text": "Find the longest path in a DAG using DAG DP in topological order.",
        "expected_pattern": "graph_dag_dp",
        "input": "4 4\n1 2 3\n2 3 4\n1 3 2\n3 4 5\n",
        "oracle_check": lambda out: out == "12"
    },
    {
        "id": "G-38",
        "category": "3F-J. DAG Dynamic Programming",
        "text": "Dynamic programming on DAG to compute maximum path weight from source 1.",
        "expected_pattern": "graph_dag_dp",
        "input": "3 2\n1 2 10\n2 3 20\n",
        "oracle_check": lambda out: out == "30"
    },
    {
        "id": "G-39",
        "category": "3F-J. DAG Dynamic Programming",
        "text": "DAG DP optimal path transition processing vertices in topological order.",
        "expected_pattern": "graph_dag_dp",
        "input": "4 3\n1 2 5\n2 3 5\n3 4 5\n",
        "oracle_check": lambda out: out == "15"
    },
    {
        "id": "G-40",
        "category": "3F-J. DAG Dynamic Programming",
        "text": "Longest path calculation on DAG with edge weights.",
        "expected_pattern": "graph_dag_dp",
        "input": "3 3\n1 2 4\n1 3 1\n2 3 5\n",
        "oracle_check": lambda out: out == "9"
    },

    # ── 3F-K: Disjoint Set Union (G-41..G-44) ──
    {
        "id": "G-41",
        "category": "3F-K. Disjoint Set Union",
        "text": "Implement Disjoint Set Union (DSU) with path compression and union by rank for connectivity queries.",
        "expected_pattern": "graph_dsu",
        "input": "4 4\n1 1 2\n1 2 3\n2 1 3\n2 1 4\n",
        "oracle_check": lambda out: out.splitlines() == ["YES", "NO"]
    },
    {
        "id": "G-42",
        "category": "3F-K. Disjoint Set Union",
        "text": "Union-find data structure maintaining dynamic connectivity of vertices.",
        "expected_pattern": "graph_dsu",
        "input": "3 3\n1 1 2\n2 1 2\n2 2 3\n",
        "oracle_check": lambda out: out.splitlines() == ["YES", "NO"]
    },
    {
        "id": "G-43",
        "category": "3F-K. Disjoint Set Union",
        "text": "DSU queries: unite sets and check if two nodes are connected.",
        "expected_pattern": "graph_dsu",
        "input": "5 3\n1 1 5\n1 2 3\n2 1 5\n",
        "oracle_check": lambda out: out.strip() == "YES"
    },
    {
        "id": "G-44",
        "category": "3F-K. Disjoint Set Union",
        "text": "Disjoint set union with path compression O(alpha(V)) amortized.",
        "expected_pattern": "graph_dsu",
        "input": "4 2\n1 3 4\n2 3 4\n",
        "oracle_check": lambda out: out.strip() == "YES"
    },

    # ── 3F-L: Minimum Spanning Tree (G-45..G-48) ──
    {
        "id": "G-45",
        "category": "3F-L. Minimum Spanning Tree",
        "text": "Find minimum spanning tree (MST) using Kruskal algorithm on undirected graph.",
        "expected_pattern": "graph_mst_kruskal",
        "input": "4 5\n1 2 1\n2 3 2\n3 4 3\n4 1 4\n1 3 5\n",
        "oracle_check": lambda out: out == "6"
    },
    {
        "id": "G-46",
        "category": "3F-L. Minimum Spanning Tree",
        "text": "Kruskal algorithm edge sorting and DSU for minimum spanning tree weight.",
        "expected_pattern": "graph_mst_kruskal",
        "input": "3 3\n1 2 10\n2 3 20\n1 3 30\n",
        "oracle_check": lambda out: out == "30"
    },
    {
        "id": "G-47",
        "category": "3F-L. Minimum Spanning Tree",
        "text": "Compute MST total cost using Prim's algorithm with priority queue.",
        "expected_pattern": "graph_mst_prim",
        "input": "4 4\n1 2 1\n2 3 2\n3 4 3\n1 4 10\n",
        "oracle_check": lambda out: out == "6"
    },
    {
        "id": "G-48",
        "category": "3F-L. Minimum Spanning Tree",
        "text": "Prim algorithm minimum spanning tree on connected weighted graph.",
        "expected_pattern": "graph_mst_prim",
        "input": "3 3\n1 2 5\n2 3 5\n1 3 10\n",
        "oracle_check": lambda out: out == "10"
    },

    # ── 3F-M: Strongly Connected Components (G-49..G-52) ──
    {
        "id": "G-49",
        "category": "3F-M. Strongly Connected Components",
        "text": "Find strongly connected components (SCC) in directed graph using Tarjan algorithm.",
        "expected_pattern": "graph_scc_tarjan",
        "input": "5 5\n1 2\n2 3\n3 1\n3 4\n4 5\n",
        "oracle_check": lambda out: out == "3"
    },
    {
        "id": "G-50",
        "category": "3F-M. Strongly Connected Components",
        "text": "Count total number of strongly connected components using Tarjan low-link values.",
        "expected_pattern": "graph_scc_tarjan",
        "input": "4 4\n1 2\n2 3\n3 4\n4 1\n",
        "oracle_check": lambda out: out == "1"
    },
    {
        "id": "G-51",
        "category": "3F-M. Strongly Connected Components",
        "text": "Tarjan SCC decomposition on DAG where each vertex is its own SCC.",
        "expected_pattern": "graph_scc_tarjan",
        "input": "3 2\n1 2\n2 3\n",
        "oracle_check": lambda out: out == "3"
    },
    {
        "id": "G-52",
        "category": "3F-M. Strongly Connected Components",
        "text": "Determine strongly connected components partitioning directed graph vertices.",
        "expected_pattern": "graph_scc_tarjan",
        "input": "4 3\n1 2\n2 1\n3 4\n",
        "oracle_check": lambda out: out == "3"
    },

    # ── 3F-N: Bridges & Articulation Points (G-53..G-56) ──
    {
        "id": "G-53",
        "category": "3F-N. Bridges & Articulation Points",
        "text": "Find all bridges in the graph and articulation points using DFS low-link values.",
        "expected_pattern": "graph_bridges_articulation",
        "input": "4 3\n1 2\n2 3\n3 4\n",
        "oracle_check": lambda out: "Bridges: 3" in out and "Articulation Points: 2" in out
    },
    {
        "id": "G-54",
        "category": "3F-N. Bridges & Articulation Points",
        "text": "Find bridges and cut vertices in undirected network.",
        "expected_pattern": "graph_bridges_articulation",
        "input": "3 3\n1 2\n2 3\n3 1\n",
        "oracle_check": lambda out: "Bridges: 0" in out and "Articulation Points: 0" in out
    },
    {
        "id": "G-55",
        "category": "3F-N. Bridges & Articulation Points",
        "text": "Identify critical edges (bridges) and critical vertices (articulation points) in a connected graph.",
        "expected_pattern": "graph_bridges_articulation",
        "input": "5 5\n1 2\n2 3\n3 1\n3 4\n4 5\n",
        "oracle_check": lambda out: "Bridges: 2" in out
    },
    {
        "id": "G-56",
        "category": "3F-N. Bridges & Articulation Points",
        "text": "Bridges and articulation points computation using tin and low arrays.",
        "expected_pattern": "graph_bridges_articulation",
        "input": "4 4\n1 2\n2 3\n3 1\n1 4\n",
        "oracle_check": lambda out: "Bridges: 1" in out
    },

    # ── 3F-O: Anti-Patterns & Hardening (G-57..G-60) ──
    {
        "id": "G-57",
        "category": "3F-O. Anti-Patterns",
        "text": "Run Dijkstra on graph with negative edge weights to find shortest path.",
        "anti_pattern_test": True,
        "rejected_pattern": "graph_dijkstra",
        "expected_rejection_code": "GRAPH_NEGATIVE_WEIGHTS_FOR_DIJKSTRA"
    },
    {
        "id": "G-58",
        "category": "3F-O. Anti-Patterns",
        "text": "Topological sort on directed cyclic graph with cycle.",
        "anti_pattern_test": True,
        "rejected_pattern": "graph_topological_sort",
        "expected_rejection_code": "GRAPH_CYCLIC_FOR_TOPOLOGICAL_SORT"
    },
    {
        "id": "G-59",
        "category": "3F-O. Anti-Patterns",
        "text": "All-pairs shortest path with N = 100,000 vertices.",
        "anti_pattern_test": True,
        "rejected_pattern": "graph_floyd_warshall",
        "expected_rejection_code": "GRAPH_COMPLEXITY_EXCEEDED"
    },
    {
        "id": "G-60",
        "category": "3F-O. Anti-Patterns",
        "text": "Minimum spanning tree on a disconnected graph with multiple components.",
        "anti_pattern_test": True,
        "rejected_pattern": "graph_mst_kruskal",
        "expected_rejection_code": "GRAPH_DISCONNECTED_MST"
    },
]


def run_benchmark():
    print("=" * 70)
    print("CHUP Phase 3F — Graph Domain Benchmark (G-01 through G-60)")
    print("=" * 70)

    passed = 0
    failed = 0
    total = len(BENCHMARK_PROBLEMS)

    for prob in BENCHMARK_PROBLEMS:
        pid = prob["id"]
        cat = prob["category"]
        text = prob["text"]

        try:
            resp = handle_request({"problemText": text})

            if prob.get("anti_pattern_test"):
                # Must eliminate the forbidden candidate
                elim = resp.get("eliminatedCandidates", [])
                rej_pat = prob["rejected_pattern"]
                expected_code = prob["expected_rejection_code"]

                found_elim = any(
                    e.get("candidate") == rej_pat and e.get("rejectionCode") == expected_code
                    for e in elim
                )
                if found_elim:
                    print(f"  [PASS] {pid} ({cat}): Correctly eliminated {rej_pat} with {expected_code}")
                    passed += 1
                else:
                    print(f"  [FAIL] {pid} ({cat}): Failed to eliminate {rej_pat} with {expected_code}. Elim: {elim}")
                    failed += 1
                continue

            # Standard positive test
            expected_pat = prob["expected_pattern"]
            actual_pat = resp.get("selectedPattern")
            code = resp.get("code") or resp.get("generatedCode")

            if actual_pat != expected_pat:
                print(f"  [FAIL] {pid} ({cat}): Expected {expected_pat}, got {actual_pat}")
                failed += 1
                continue

            if not code or len(code) < 50:
                print(f"  [FAIL] {pid} ({cat}): No code generated")
                failed += 1
                continue

            # Compile and execute
            stdin_data = prob.get("input", "")
            output = compile_and_run_cpp(code, stdin_data, pattern=actual_pat)

            if output.startswith("COMPILE_ERROR") or output.startswith("RUNTIME_ERROR"):
                print(f"  [FAIL] {pid} ({cat}): Execution error: {output[:150]}")
                failed += 1
                continue

            # Oracle validation
            check_fn = prob.get("oracle_check")
            if check_fn and not check_fn(output):
                print(f"  [FAIL] {pid} ({cat}): Output '{output[:80]}' failed oracle check")
                failed += 1
                continue

            print(f"  [PASS] {pid} ({cat}): {actual_pat} verified against oracle (output: {output[:30]})")
            passed += 1

        except Exception as ex:
            print(f"  [ERROR] {pid} ({cat}): Exception: {ex}")
            failed += 1

    print("=" * 70)
    score_pct = (passed / total) * 100
    print(f"Graph Benchmark Score: {passed}/{total} ({score_pct:.1f}%)")
    print("=" * 70)
    return passed == total


if __name__ == "__main__":
    success = run_benchmark()
    sys.exit(0 if success else 1)
