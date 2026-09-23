"""
Graph Blind Holdout Evaluation — Phase 3F (BH-01 through BH-12)

Unseen, realistic problem formulations with distinct vocabulary and phrasing:
  BH-01: Network transmission latency (Dijkstra)
  BH-02: Optical fiber wiring with minimum total cost (Prim MST)
  BH-03: Currency exchange arbitrage cycle (Bellman-Ford negative cycle)
  BH-04: Academic course prerequisite sequence (Topological sort)
  BH-05: Vulnerable internet backbone links (Bridges)
  BH-06: Social network friend clusters (Connected components)
  BH-07: Metro subway transit minimum stops (BFS shortest path)
  BH-08: Software project critical path duration (DAG DP)
  BH-09: Circuit loop detection in electrical network (Undirected cycle)
  BH-10: Tournament team partition without internal conflicts (Bipartite coloring)
  BH-11: Distributed server mutual communication clusters (Tarjan SCC)
  BH-12: Complete road network distance matrix (Floyd-Warshall)
"""

import sys
import os
import subprocess
import tempfile
from typing import Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from pointer_algorithms.bridge import handle_request


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


HOLDOUT_PROBLEMS = [
    {
        "id": "BH-01",
        "name": "Network Transmission Latency",
        "text": "A computer network is modeled as a directed graph where edge costs represent packet latency. All latencies are non-negative. Find the minimum latency to send a packet from server 1 to every other server.",
        "expected_pattern": "graph_dijkstra",
        "input": "4 4\n1 2 5\n1 3 10\n2 4 15\n3 4 5\n",
        "oracle_check": lambda out: out == "0 5 10 15"
    },
    {
        "id": "BH-02",
        "name": "Optical Fiber Wiring",
        "text": "Connect all data centers using optical fiber cables with minimum total cost using Prim's algorithm with priority queue.",
        "expected_pattern": "graph_mst_prim",
        "input": "4 5\n1 2 2\n2 3 3\n3 4 4\n1 4 8\n1 3 5\n",
        "oracle_check": lambda out: out == "9"
    },
    {
        "id": "BH-03",
        "name": "Currency Exchange Arbitrage",
        "text": "Detect if an arbitrage opportunity exists in a currency market with negative edge weights and negative weight cycle using Bellman-Ford.",
        "expected_pattern": "graph_bellman_ford",
        "input": "3 3\n1 2 -1\n2 3 -2\n3 1 -1\n",
        "oracle_check": lambda out: "NEGATIVE_CYCLE" in out
    },
    {
        "id": "BH-04",
        "name": "Academic Course Prerequisites",
        "text": "A university curriculum specifies prerequisite courses as directed edges. Find a valid course build sequence using topological sort.",
        "expected_pattern": "graph_topological_sort",
        "input": "4 3\n1 2\n2 3\n3 4\n",
        "oracle_check": lambda out: out == "1 2 3 4"
    },
    {
        "id": "BH-05",
        "name": "Vulnerable Backbone Links",
        "text": "Identify all critical communication bridges whose failure would disconnect the network using DFS low-link and tin values.",
        "expected_pattern": "graph_bridges_articulation",
        "input": "4 3\n1 2\n2 3\n3 4\n",
        "oracle_check": lambda out: "Bridges: 3" in out
    },
    {
        "id": "BH-06",
        "name": "Social Network Friend Clusters",
        "text": "Given a social network with undirected friendships, count the number of isolated friend circles and connected components.",
        "expected_pattern": "graph_connected_components",
        "input": "6 4\n1 2\n2 3\n4 5\n5 6\n",
        "oracle_check": lambda out: out == "2"
    },
    {
        "id": "BH-07",
        "name": "Metro Subway Transit",
        "text": "Find the minimum number of train stops needed to travel from subway station 1 to all other stations in an unweighted track network.",
        "expected_pattern": "graph_bfs_shortest_path",
        "input": "5 4\n1 2\n2 3\n3 4\n4 5\n",
        "oracle_check": lambda out: out == "0 1 2 3 4"
    },
    {
        "id": "BH-08",
        "name": "Project Critical Path",
        "text": "Compute the longest path duration of a software project represented as a DAG using DAG DP in topological order.",
        "expected_pattern": "graph_dag_dp",
        "input": "4 4\n1 2 10\n1 3 5\n2 4 10\n3 4 20\n",
        "oracle_check": lambda out: out == "25"
    },
    {
        "id": "BH-09",
        "name": "Circuit Loop Detection",
        "text": "Given an electrical circuit network of wires, detect if an undirected cycle exists using parent tracking DFS.",
        "expected_pattern": "graph_cycle_detection_undirected",
        "input": "4 4\n1 2\n2 3\n3 4\n4 1\n",
        "oracle_check": lambda out: out == "YES"
    },
    {
        "id": "BH-10",
        "name": "Tournament Team Partition",
        "text": "Divide tournament players into two opposing teams such that no two conflicting players are on the same team using bipartite 2-coloring.",
        "expected_pattern": "graph_bipartite_coloring",
        "input": "4 4\n1 2\n2 3\n3 4\n4 1\n",
        "oracle_check": lambda out: out == "YES"
    },
    {
        "id": "BH-11",
        "name": "Server Mutual Reachability",
        "text": "Group cluster servers into strongly connected components (SCC) where each server can communicate with every other server in its group using Tarjan algorithm.",
        "expected_pattern": "graph_scc_tarjan",
        "input": "4 4\n1 2\n2 3\n3 1\n3 4\n",
        "oracle_check": lambda out: out == "2"
    },
    {
        "id": "BH-12",
        "name": "All-City Transit Matrix",
        "text": "Compute the shortest travel distance between every pair of cities in a road network using Floyd-Warshall all-pairs algorithm with V = 3 vertices.",
        "expected_pattern": "graph_floyd_warshall",
        "input": "3 3\n1 2 2\n2 3 3\n1 3 10\n",
        "oracle_check": lambda out: "0 2 5" in out.splitlines()[0]
    },
]


def run_blind_holdouts():
    print("=" * 70)
    print("CHUP Phase 3F — Graph Blind Holdout Evaluation (BH-01..BH-12)")
    print("=" * 70)

    passed = 0
    total = len(HOLDOUT_PROBLEMS)

    for prob in HOLDOUT_PROBLEMS:
        pid = prob["id"]
        pname = prob["name"]
        text = prob["text"]
        expected_pat = prob["expected_pattern"]

        try:
            resp = handle_request({"problemText": text})
            actual_pat = resp.get("selectedPattern")
            code = resp.get("code") or resp.get("generatedCode")

            if actual_pat != expected_pat:
                print(f"  [FAIL] {pid} ({pname}): Expected {expected_pat}, got {actual_pat}")
                continue

            if not code:
                print(f"  [FAIL] {pid} ({pname}): No C++ code generated")
                continue

            output = compile_and_run_cpp(code, prob["input"], pattern=actual_pat)
            if output.startswith("COMPILE_ERROR") or output.startswith("RUNTIME_ERROR"):
                print(f"  [FAIL] {pid} ({pname}): Error: {output[:120]}")
                continue

            check_fn = prob.get("oracle_check")
            if check_fn and not check_fn(output):
                print(f"  [FAIL] {pid} ({pname}): Oracle check failed (got '{output}')")
                continue

            print(f"  [PASS] {pid} ({pname}): {actual_pat} verified (output: {output.strip()[:30]})")
            passed += 1

        except Exception as ex:
            print(f"  [ERROR] {pid} ({pname}): Exception: {ex}")

    print("=" * 70)
    pct = (passed / total) * 100
    print(f"Blind Holdout Score: {passed}/{total} ({pct:.1f}%)")
    print("=" * 70)
    return passed == total


if __name__ == "__main__":
    success = run_blind_holdouts()
    sys.exit(0 if success else 1)
