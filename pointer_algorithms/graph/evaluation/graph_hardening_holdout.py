"""
Graph Hardening Blind Holdout Evaluation — Phase 3F-H8 (HH-01 through HH-12)

Strictly evaluates semantic recognition on disguised real-world problems.
The problem metadata and prompts DO NOT mention algorithm names (no Dijkstra,
BFS, Prim, Kruskal, Bellman-Ford, Tarjan, etc.).

Categories:
  HH-01: Infrastructure Network Reliability (Bridges)
  HH-02: Emergency Resource Movement (BFS shortest path)
  HH-03: Manufacturing Assembly Precedence (Topological sort)
  HH-04: Wireless Frequency Allocation (Bipartite 2-coloring)
  HH-05: Power Grid Infrastructure Wiring (Kruskal MST)
  HH-06: Software Build Critical Path (DAG DP)
  HH-07: International Currency Devaluation Loop (Bellman-Ford negative cycle)
  HH-08: Database Server Replication Latency (Dijkstra)
  HH-09: Telecommunication Island Count (Connected components)
  HH-10: Multi-Threaded Deadlock Detection (Directed cycle)
  HH-11: Distributed Consensus Server Enclaves (Tarjan SCC)
  HH-12: Campus Logistics Pairwise Transit (Floyd-Warshall)
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


HARDENING_PROBLEMS = [
    {
        "id": "HH-01",
        "name": "Infrastructure Network Reliability",
        "text": "In a nationwide optical telecommunication network, identify all critical backbone connections whose severance would partition the network into disconnected segments.",
        "expected_pattern": "graph_bridges_articulation",
        "input": "4 3\n1 2\n2 3\n3 4\n",
        "oracle_check": lambda out: "Bridges: 3" in out
    },
    {
        "id": "HH-02",
        "name": "Emergency Resource Movement",
        "text": "Medical supplies must be transported across an unweighted route network from central depot 1 to all regional hubs. Calculate the fewest route transfers required to reach each hub.",
        "expected_pattern": "graph_bfs_shortest_path",
        "input": "4 3\n1 2\n2 3\n3 4\n",
        "oracle_check": lambda out: out == "0 1 2 3"
    },
    {
        "id": "HH-03",
        "name": "Manufacturing Assembly Precedence",
        "text": "A manufacturing plant must execute factory assembly steps such that each prerequisite step completes before dependent steps begin. Output a valid global step execution order.",
        "expected_pattern": "graph_topological_sort",
        "input": "3 2\n1 2\n2 3\n",
        "oracle_check": lambda out: out == "1 2 3"
    },
    {
        "id": "HH-04",
        "name": "Wireless Frequency Allocation",
        "text": "Two radio broadcast frequencies are available. Determine if antennas can be assigned to the two frequencies such that no two adjacent interfering antennas share the same frequency.",
        "expected_pattern": "graph_bipartite_coloring",
        "input": "4 4\n1 2\n2 3\n3 4\n4 1\n",
        "oracle_check": lambda out: out == "YES"
    },
    {
        "id": "HH-05",
        "name": "Power Grid Infrastructure Wiring",
        "text": "Electrical cables must link all electrical substations together so that electricity can flow between any two substations, while minimizing total trenching expenditure.",
        "expected_pattern": "graph_mst_kruskal",
        "input": "4 5\n1 2 1\n2 3 2\n3 4 3\n1 4 10\n2 4 5\n",
        "oracle_check": lambda out: out == "6"
    },
    {
        "id": "HH-06",
        "name": "Software Build Critical Path",
        "text": "A software project consists of tasks with dependencies forming an acyclic task network with duration costs. Compute the longest completion time path of the project.",
        "expected_pattern": "graph_dag_dp",
        "input": "4 4\n1 2 4\n1 3 2\n2 4 5\n3 4 8\n",
        "oracle_check": lambda out: out == "10"
    },
    {
        "id": "HH-07",
        "name": "International Currency Devaluation Loop",
        "text": "A foreign currency trading desk monitors exchange conversion ratios with negative transaction fees. Detect whether a negative cycle exists allowing infinite value accumulation.",
        "expected_pattern": "graph_bellman_ford",
        "input": "3 3\n1 2 -2\n2 3 -3\n3 1 -1\n",
        "oracle_check": lambda out: "NEGATIVE_CYCLE" in out
    },
    {
        "id": "HH-08",
        "name": "Database Server Replication Latency",
        "text": "A cloud distributed database sends updates from master server 1 across directed network connections with non-negative millisecond transmission latency. Determine minimum delay to all servers.",
        "expected_pattern": "graph_dijkstra",
        "input": "4 4\n1 2 2\n1 3 5\n2 4 4\n3 4 1\n",
        "oracle_check": lambda out: out == "0 2 5 6"
    },
    {
        "id": "HH-09",
        "name": "Telecommunication Island Count",
        "text": "After a natural storm, certain inter-city phone lines remain operational while others failed. Count the number of isolated regional communication groups that remain.",
        "expected_pattern": "graph_connected_components",
        "input": "5 2\n1 2\n3 4\n",
        "oracle_check": lambda out: out == "3"
    },
    {
        "id": "HH-10",
        "name": "Multi-Threaded Deadlock Detection",
        "text": "In an operating system process scheduler, directed edges represent processes waiting on locks held by other processes. Determine whether a circular dependency deadlock exists.",
        "expected_pattern": "graph_cycle_detection_directed",
        "input": "3 3\n1 2\n2 3\n3 1\n",
        "oracle_check": lambda out: out == "YES"
    },
    {
        "id": "HH-11",
        "name": "Distributed Consensus Server Enclaves",
        "text": "In a distributed consensus protocol, identify isolated groups of servers where every server within the group has mutual reachability to exchange quorum messages with all other group members.",
        "expected_pattern": "graph_scc_tarjan",
        "input": "4 4\n1 2\n2 3\n3 1\n3 4\n",
        "oracle_check": lambda out: out == "2"
    },
    {
        "id": "HH-12",
        "name": "Campus Logistics Pairwise Transit",
        "text": "Given a logistics campus with a small number of buildings, calculate the complete pairwise travel distance matrix between every pair of buildings.",
        "expected_pattern": "graph_floyd_warshall",
        "input": "3 3\n1 2 2\n2 3 3\n1 3 6\n",
        "oracle_check": lambda out: out == "0 2 5\n-1 0 3\n-1 -1 0"
    },
]


def run_hardening_holdout():
    print("=" * 70)
    print("CHUP Phase 3F — Graph Hardening Blind Holdout Evaluation (HH-01..HH-12)")
    print("=" * 70)

    passed = 0
    failed = 0

    for prob in HARDENING_PROBLEMS:
        pid = prob["id"]
        name = prob["name"]
        text = prob["text"]
        expected_pat = prob["expected_pattern"]
        stdin_data = prob["input"]
        oracle_check = prob["oracle_check"]

        resp = handle_request({"problemText": text})
        selected_pat = resp.get("selectedPattern")

        if selected_pat != expected_pat:
            print(f"  [FAIL] {pid} ({name}): Expected {expected_pat}, got {selected_pat}")
            failed += 1
            continue

        cpp_code = resp.get("code")
        if not cpp_code:
            print(f"  [FAIL] {pid} ({name}): No C++ code generated")
            failed += 1
            continue

        out = compile_and_run_cpp(cpp_code, stdin_data, pattern=selected_pat)
        if "COMPILE_ERROR" in out or "RUNTIME_ERROR" in out:
            print(f"  [FAIL] {pid} ({name}): Execution error: {out}")
            failed += 1
            continue

        if oracle_check(out):
            print(f"  [PASS] {pid} ({name}): {selected_pat} verified (output: {out})")
            passed += 1
        else:
            print(f"  [FAIL] {pid} ({name}): Oracle verification failed (output: '{out}')")
            failed += 1

    print("=" * 70)
    score = (passed / len(HARDENING_PROBLEMS)) * 100
    print(f"Hardening Holdout Score: {passed}/{len(HARDENING_PROBLEMS)} ({score:.1f}%)")
    print("=" * 70)
    return passed, len(HARDENING_PROBLEMS)


if __name__ == "__main__":
    passed, total = run_hardening_holdout()
    sys.exit(0 if passed == total else 1)
