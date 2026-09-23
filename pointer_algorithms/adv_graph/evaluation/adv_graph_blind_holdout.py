"""
CHUP Phase 3N — Advanced Graph Algorithms Blind Holdout Evaluation.

Evaluates 12 unseen, real-world domain problem formulations with rich contextual vocabulary
across the Advanced Graph domain:
1. AG-BH-01: Telecom Low-Latency Packet Routing (0-1 BFS)
2. AG-BH-02: Currency Arbitrage Loop Detector (SPFA Negative Cycle)
3. AG-BH-03: Snowplow Route Planning (Eulerian Trail)
4. AG-BH-04: Digital Circuit Fault Testing (2-SAT)
5. AG-BH-05: Critical Infrastructure Resilience Analysis (Block-Cut Tree)
6. AG-BH-06: Island Bridge Severance Vulnerability (Bridge-Block Tree)
7. AG-BH-07: Medical Residency Matching Program (Bipartite Matching)
8. AG-BH-08: Municipal Water Distribution Capacity (Dinic Max-Flow)
9. AG-BH-09: Power Grid Severance Min-Cut (Dinic Min-Cut)
10. AG-BH-10: Freight Logistics Optimal Routing (MCMF)
11. AG-BH-11: Robotic Grid Navigation with Turning Cost (0-1 BFS)
12. AG-BH-12: Forex Trading Negative Cycle Detection (SPFA)
"""

import sys
import os
import subprocess
import tempfile
import hashlib
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.adv_graph.verification.adv_graph_oracles import (
    adv_graph_01_bfs_oracle,
    adv_graph_spfa_negative_cycle_oracle,
    adv_graph_eulerian_path_oracle,
    adv_graph_2sat_oracle,
    adv_graph_block_cut_tree_oracle,
    adv_graph_bridge_block_tree_oracle,
    adv_graph_bipartite_matching_oracle,
    adv_graph_max_flow_oracle,
    adv_graph_min_cut_oracle,
    adv_graph_mcmf_oracle
)

COMPILED_BINARIES: Dict[str, str] = {}


def compile_and_run_cpp(code: str, stdin_data: str, timeout: int = 10) -> str:
    code_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()
    exe = COMPILED_BINARIES.get(code_hash)
    if not exe or not os.path.exists(exe):
        tmp_cpp = tempfile.NamedTemporaryFile(suffix=".cpp", delete=False)
        tmp_cpp.write(code.encode("utf-8"))
        tmp_cpp.close()
        exe = tmp_cpp.name[:-4]
        compile_res = subprocess.run(
            ["g++", "-std=c++17", "-O2", tmp_cpp.name, "-o", exe],
            capture_output=True, text=True
        )
        if compile_res.returncode != 0:
            return f"COMPILE_ERROR: {compile_res.stderr[:200]}"
        COMPILED_BINARIES[code_hash] = exe
    try:
        run_res = subprocess.run(
            [exe], input=stdin_data, capture_output=True, text=True, timeout=timeout
        )
        if run_res.returncode != 0:
            return f"RUNTIME_ERROR: {run_res.stderr[:200]}"
        return run_res.stdout.strip()
    except subprocess.TimeoutExpired:
        return "RUNTIME_ERROR: TimeoutExpired"


BLIND_HOLDOUT_PROBLEMS = [
    {
        "id": "AG-BH-01",
        "title": "Telecom Low-Latency Packet Routing",
        "text": "Data packets travel across optical fibers and local switches where latency is either 0ms (same rack) or 1ms (cross-datacenter). Find single-source shortest path using 0-1 BFS deque relaxation.",
        "expected_pattern": "adv_graph_01_bfs",
        "input": "4 4\n1 2 0\n2 3 1\n3 4 0\n1 4 1",
        "oracle_fn": lambda: "0 0 1 1"
    },
    {
        "id": "AG-BH-02",
        "title": "Currency Arbitrage Loop Detector",
        "text": "A foreign exchange market displays conversion multipliers transformed into negative log rates. Detect if a negative weight cycle or arbitrage opportunity exists using SPFA queue relaxation.",
        "expected_pattern": "adv_graph_spfa_negative_cycle",
        "input": "3 3\n1 2 1\n2 3 1\n3 1 -3",
        "oracle_fn": lambda: "YES"
    },
    {
        "id": "AG-BH-03",
        "title": "Snowplow Route Planning",
        "text": "A municipal maintenance truck must traverse each street segment in a neighborhood exactly once. Construct the traversal route using Hierholzer Eulerian trail algorithm.",
        "expected_pattern": "adv_graph_eulerian_path",
        "input": "4 4\n1 2\n2 3\n3 4\n4 1",
        "oracle_fn": lambda: "1 4 3 2 1"
    },
    {
        "id": "AG-BH-04",
        "title": "Digital Circuit Fault Testing",
        "text": "A microchip verification module tests pairs of logic gates under 2-literal boolean clause constraints. Solve the 2-SAT satisfiability problem using implication graph and Tarjan SCC condensation.",
        "expected_pattern": "adv_graph_2sat",
        "input": "2 3\n1 2\n-1 2\n1 -2",
        "oracle_fn": lambda: "SATISFIABLE\n1 1"
    },
    {
        "id": "AG-BH-05",
        "title": "Critical Infrastructure Resilience Analysis",
        "text": "Analyze national transportation network to find single-point-of-failure articulation points and decompose into 2-vertex-connected components using Block-Cut tree decomposition.",
        "expected_pattern": "adv_graph_block_cut_tree",
        "input": "4 3\n1 2\n2 3\n3 4",
        "oracle_fn": lambda: "Blocks: 3\nBlock 1 size 2: 3 4\nBlock 2 size 2: 2 3\nBlock 3 size 2: 1 2\nCut vertices (2): 2 3"
    },
    {
        "id": "AG-BH-06",
        "title": "Island Bridge Severance Vulnerability",
        "text": "Identify critical bridge connections between archipelago islands and contract 2-edge-connected components into a bridge-block condensation tree.",
        "expected_pattern": "adv_graph_bridge_block_tree",
        "input": "5 5\n1 2\n2 3\n3 1\n3 4\n4 5",
        "oracle_fn": lambda: "Components: 3\n1 1 1 2 3"
    },
    {
        "id": "AG-BH-07",
        "title": "Medical Residency Matching Program",
        "text": "Match graduating medical residents to hospital programs partitioned into two disjoint sets, maximizing total assignments via Kuhn bipartite matching augmenting path algorithm.",
        "expected_pattern": "adv_graph_bipartite_matching",
        "input": "3 3 4\n1 1\n2 1\n2 2\n3 3",
        "oracle_fn": lambda: "3\n1 1\n2 2\n3 3"
    },
    {
        "id": "AG-BH-08",
        "title": "Municipal Water Distribution Capacity",
        "text": "Calculate maximum volumetric water flow from main reservoir source to city terminal sink through pipe network with capacities using Dinic blocking flow algorithm.",
        "expected_pattern": "adv_graph_max_flow_dinic",
        "input": "4 5 1 4\n1 2 20\n1 3 10\n2 3 5\n2 4 15\n3 4 20",
        "oracle_fn": lambda: "30"
    },
    {
        "id": "AG-BH-09",
        "title": "Power Grid Severance Min-Cut",
        "text": "Identify the minimum capacity s-t cut partition separating electrical generation substation from high-demand industrial sector via Dinic min-cut algorithm.",
        "expected_pattern": "adv_graph_min_cut",
        "input": "4 4 1 4\n1 2 10\n1 3 15\n2 4 10\n3 4 15",
        "oracle_fn": lambda: "25\n1 2\n1 3"
    },
    {
        "id": "AG-BH-10",
        "title": "Freight Logistics Optimal Routing",
        "text": "Transport container shipping units from origin harbor to destination terminal minimizing total monetary transit expense given container capacities and unit costs using MCMF.",
        "expected_pattern": "adv_graph_mcmf",
        "input": "4 4 1 4\n1 2 10 3\n2 4 10 2\n1 3 10 1\n3 4 10 6",
        "oracle_fn": lambda: "20 120"
    },
    {
        "id": "AG-BH-11",
        "title": "Robotic Grid Navigation with Turning Cost",
        "text": "Autonomous warehouse rover moves on a grid where continuing straight has 0 weight cost and making a 90-degree turn has 1 weight cost. Compute shortest path via 0-1 BFS deque.",
        "expected_pattern": "adv_graph_01_bfs",
        "input": "3 2\n1 2 0\n2 3 1",
        "oracle_fn": lambda: "0 0 1"
    },
    {
        "id": "AG-BH-12",
        "title": "Forex Trading Negative Cycle Detection",
        "text": "An automated foreign exchange arbitrage scanner monitors currency pairs. Determine if directed graph has a negative cycle using SPFA queue relaxation.",
        "expected_pattern": "adv_graph_spfa_negative_cycle",
        "input": "3 3\n1 2 4\n2 3 4\n3 1 -10",
        "oracle_fn": lambda: "YES"
    },
]


def run_blind_holdout():
    passed = 0
    failed = 0
    total = len(BLIND_HOLDOUT_PROBLEMS)

    print("=" * 80)
    print("CHUP Phase 3N — Advanced Graph Algorithms Blind Holdout Evaluation")
    print(f"Total problems: {total} (Real-world domain formulations)")
    print("=" * 80)

    for prob in BLIND_HOLDOUT_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]

        res = handle_request({"action": "solve", "problemText": text})

        expected_pat = prob["expected_pattern"]
        if res["status"] != "success":
            failed += 1
            print(f"{pid} FAIL: Bridge returned status={res['status']} ({title})")
            continue

        if res["selectedPattern"] != expected_pat:
            failed += 1
            print(f"{pid} FAIL: Expected {expected_pat}, got {res['selectedPattern']} ({title})")
            continue

        code = res.get("code", "")
        stdin_data = prob.get("input", "")
        cpp_output = compile_and_run_cpp(code, stdin_data)
        expected_output = prob["oracle_fn"]()

        if "COMPILE_ERROR" in cpp_output or "RUNTIME_ERROR" in cpp_output:
            failed += 1
            print(f"{pid} FAIL: Execution error: {cpp_output} ({title})")
            continue

        # Compare output: exact match or structured domain validation
        match = False
        if cpp_output == expected_output or expected_output in cpp_output:
            match = True
        elif expected_pat == "adv_graph_spfa_negative_cycle" and cpp_output.startswith(expected_output):
            match = True
        elif expected_pat == "adv_graph_eulerian_path":
            if expected_output == "-1":
                match = (cpp_output.strip() == "-1")
            else:
                nodes = [int(x) for x in cpp_output.split() if x.lstrip('-').isdigit()]
                lines = stdin_data.strip().splitlines()
                n, m = map(int, lines[0].split()[:2])
                if len(nodes) == m + 1:
                    edges_input = []
                    for line in lines[1:m+1]:
                        u, v = map(int, line.split()[:2])
                        edges_input.append((min(u, v), max(u, v)))
                    edges_traversed = [(min(nodes[i], nodes[i+1]), max(nodes[i], nodes[i+1])) for i in range(len(nodes)-1)]
                    match = (sorted(edges_input) == sorted(edges_traversed))
        elif expected_pat == "adv_graph_block_cut_tree":
            exp_blocks = [line for line in expected_output.splitlines() if line.startswith("Blocks:")]
            exp_cuts = [line for line in expected_output.splitlines() if line.startswith("Cut vertices")]
            act_blocks = [line for line in cpp_output.splitlines() if line.startswith("Blocks:")]
            act_cuts = [line for line in cpp_output.splitlines() if line.startswith("Cut vertices")]
            match = (exp_blocks == act_blocks and exp_cuts == act_cuts)
        elif expected_pat == "adv_graph_bipartite_matching":
            exp_size = expected_output.splitlines()[0].strip()
            act_size = cpp_output.splitlines()[0].strip()
            match = (exp_size == act_size)

        if match:
            passed += 1
            print(f"{pid} PASS: {title} (Pattern={expected_pat})")
        else:
            failed += 1
            print(f"{pid} FAIL: Output mismatch: expected '{expected_output}', got '{cpp_output}' ({title})")

    print("=" * 80)
    print(f"Blind Holdout Results: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("=" * 80)
    return passed == total


if __name__ == "__main__":
    success = run_blind_holdout()
    sys.exit(0 if success else 1)
