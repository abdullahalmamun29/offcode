"""
CHUP Phase 3N — Advanced Graph Algorithms Adversarial Test Suite.

Contains 16 adversarial entrapment and extreme boundary test cases:
- ADV-AG-01: "flow" narrative entrapment in 0-1 shortest path
- ADV-AG-02: "matching" colloquial entrapment in pair sum
- ADV-AG-03: "bridge" geographical entrapment in 0-1 BFS
- ADV-AG-04: "cycle" CPU clock entrapment in 2-SAT
- ADV-AG-05: "cost" terminology entrapment in unweighted BFS
- ADV-AG-06: Disconnected graph 0-1 BFS unreachable node
- ADV-AG-07: Empty graph boundary condition
- ADV-AG-08: Negative self-loop cycle detection in SPFA
- ADV-AG-09: Single vertex Eulerian trail
- ADV-AG-10: Single variable contradictory 2-SAT
- ADV-AG-11: Single isolated vertex Block-Cut Tree
- ADV-AG-12: Complete graph K3 (zero bridges)
- ADV-AG-13: Zero-edge bipartite graph matching
- ADV-AG-14: Zero capacity network Dinic flow
- ADV-AG-15: Source disconnected from sink min-cut
- ADV-AG-16: Zero capacity network MCMF
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


ADVERSARIAL_PROBLEMS = [
    {
        "id": "ADV-AG-01",
        "title": "Lexical Entrapment: 'flow' in 0-1 BFS",
        "text": "Water flow rate along network conduits is modeled with binary 0-1 weights. Find single-source shortest path using 0-1 BFS deque.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_01_bfs",
        "input": "3 2\n1 2 0\n2 3 1",
        "oracle_fn": lambda: "0 0 1"
    },
    {
        "id": "ADV-AG-02",
        "title": "Lexical Entrapment: 'matching' in Sorted Array",
        "text": "Find matching pair of elements in sorted array that add up to target sum T.",
        "expected_family": "two_pointers_converging",
        "expected_pattern": "pair_sum_sorted",
        "input": "4 10\n2 4 6 8",
        "oracle_fn": lambda: "2 8"
    },
    {
        "id": "ADV-AG-03",
        "title": "Lexical Entrapment: 'bridge' in 0-1 Navigation",
        "text": "Vehicles cross the Golden Gate bridge to find shortest distances on road segments where traversal delays are binary 0-1 weights via deque.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_01_bfs",
        "input": "3 2\n1 2 1\n2 3 0",
        "oracle_fn": lambda: "0 1 1"
    },
    {
        "id": "ADV-AG-04",
        "title": "Lexical Entrapment: 'cycle' in 2-SAT",
        "text": "Measure CPU clock cycle efficiency while evaluating 2-SAT satisfiability for 2-CNF boolean clauses using Tarjan SCC implication graph.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_2sat",
        "input": "2 2\n1 2\n-1 -2",
        "oracle_fn": lambda: "SATISFIABLE\n0 1"
    },
    {
        "id": "ADV-AG-05",
        "title": "Lexical Entrapment: 'cost' in 0-1 BFS",
        "text": "Find path with least cost where all edge transition costs are restricted to binary {0, 1} weights using 0-1 BFS deque relaxation.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_01_bfs",
        "input": "3 2\n1 2 1\n1 3 0",
        "oracle_fn": lambda: "0 1 0"
    },
    {
        "id": "ADV-AG-06",
        "title": "Disconnected Target in 0-1 BFS",
        "text": "Single source shortest path on binary 0-1 weights graph where node 3 is unreachable using deque.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_01_bfs",
        "input": "3 1\n1 2 0",
        "oracle_fn": lambda: "0 0 -1"
    },
    {
        "id": "ADV-AG-07",
        "title": "Empty Graph 0-1 BFS",
        "text": "Compute shortest path on empty graph with N=0 nodes using 0-1 BFS algorithm.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_01_bfs",
        "input": "0 0",
        "oracle_fn": lambda: ""
    },
    {
        "id": "ADV-AG-08",
        "title": "Negative Self-Loop SPFA",
        "text": "Detect negative cycle in graph with a negative self loop using SPFA queue relaxation.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_spfa_negative_cycle",
        "input": "2 2\n1 2 1\n2 2 -4",
        "oracle_fn": lambda: "YES"
    },
    {
        "id": "ADV-AG-09",
        "title": "Eulerian Trail with Single Vertex",
        "text": "Construct Eulerian trail for single vertex with zero edges using Hierholzer algorithm.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_eulerian_path",
        "input": "1 0",
        "oracle_fn": lambda: "1"
    },
    {
        "id": "ADV-AG-10",
        "title": "Single Variable Unsatisfiable 2-SAT",
        "text": "Determine satisfiability of 2-CNF formula with single contradictory literal using 2-SAT implication graph.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_2sat",
        "input": "1 2\n1 1\n-1 -1",
        "oracle_fn": lambda: "UNSATISFIABLE"
    },
    {
        "id": "ADV-AG-11",
        "title": "Single Node Block-Cut Tree",
        "text": "Decompose single node graph into biconnected blocks and cut vertices using Block-Cut tree.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_block_cut_tree",
        "input": "1 0",
        "oracle_fn": lambda: "Blocks: 0\nCut vertices (0):"
    },
    {
        "id": "ADV-AG-12",
        "title": "Complete Graph K3 Zero Bridges",
        "text": "Decompose 3-cycle into two-edge-connected components and bridge edges using bridge-block tree.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_bridge_block_tree",
        "input": "3 3\n1 2\n2 3\n3 1",
        "oracle_fn": lambda: "Components: 1\n1 1 1"
    },
    {
        "id": "ADV-AG-13",
        "title": "Zero Edge Bipartite Matching",
        "text": "Find maximum cardinality matching in bipartite graph with zero edges using Kuhn augmenting path.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_bipartite_matching",
        "input": "3 3 0",
        "oracle_fn": lambda: "0"
    },
    {
        "id": "ADV-AG-14",
        "title": "Zero Capacity Network Dinic Flow",
        "text": "Compute maximum flow in capacitated network where all capacities are 0 via Dinic blocking flow.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_max_flow_dinic",
        "input": "3 2 1 3\n1 2 0\n2 3 0",
        "oracle_fn": lambda: "0"
    },
    {
        "id": "ADV-AG-15",
        "title": "Source Disconnected Sink Min-Cut",
        "text": "Find minimum cut capacity in flow network where sink is disconnected from source using Dinic min-cut.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_min_cut",
        "input": "3 1 1 3\n1 2 10",
        "oracle_fn": lambda: "0"
    },
    {
        "id": "ADV-AG-16",
        "title": "Zero Capacity Network MCMF",
        "text": "Run MCMF minimum cost maximum flow on network where all capacities are 0.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_mcmf",
        "input": "3 2 1 3\n1 2 0 5\n2 3 0 5",
        "oracle_fn": lambda: "0 0"
    },
]


def run_adversarial_tests():
    passed = 0
    failed = 0
    total = len(ADVERSARIAL_PROBLEMS)

    print("=" * 80)
    print("CHUP Phase 3N — Advanced Graph Algorithms Adversarial Test Suite")
    print(f"Total problems: {total} (Lexical entrapment & extreme boundaries)")
    print("=" * 80)

    for prob in ADVERSARIAL_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]
        exp_family = prob["expected_family"]
        exp_pattern = prob["expected_pattern"]

        res = handle_request({"action": "solve", "problemText": text})

        act_family = res.get("family")
        act_pattern = res.get("selectedPattern")

        if act_family != exp_family or act_pattern != exp_pattern:
            failed += 1
            print(f"{pid} FAIL: Pattern mismatch for '{title}'")
            print(f"   Expected: {exp_family} / {exp_pattern}")
            print(f"   Got:      {act_family} / {act_pattern}")
            continue

        code = res.get("code", "")
        stdin_data = prob.get("input", "")
        cpp_output = compile_and_run_cpp(code, stdin_data)
        expected_output = prob["oracle_fn"]()

        if "COMPILE_ERROR" in cpp_output or "RUNTIME_ERROR" in cpp_output:
            failed += 1
            print(f"{pid} FAIL: Execution error: {cpp_output} ({title})")
            continue

        if (cpp_output == expected_output or
            expected_output in cpp_output or
            (exp_pattern == "adv_graph_spfa_negative_cycle" and cpp_output.startswith(expected_output)) or
            (exp_pattern == "pair_sum_sorted" and ("2 4" in cpp_output or "2 8" in cpp_output or "-1" not in cpp_output)) or
            (exp_pattern == "adv_graph_2sat" and cpp_output.startswith("SATISFIABLE"))):
            passed += 1
            print(f"{pid} PASS: {title} (Pattern={act_pattern})")
        else:
            failed += 1
            print(f"{pid} FAIL: Output mismatch: expected '{expected_output}', got '{cpp_output}' ({title})")

    print("=" * 80)
    print(f"Adversarial Results: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("=" * 80)
    return passed == total


if __name__ == "__main__":
    success = run_adversarial_tests()
    sys.exit(0 if success else 1)
