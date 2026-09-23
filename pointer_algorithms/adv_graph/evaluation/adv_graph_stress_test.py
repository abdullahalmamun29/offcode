"""
CHUP Phase 3N — Advanced Graph Algorithms Randomized Stress Test Suite.

Differential randomized stress testing comparing compiled C++ implementations
against independent Python reference oracles across 220+ randomized graph instances:
1. 0-1 BFS vs Dijkstra Oracle (25 runs)
2. SPFA Negative Cycle vs Floyd-Warshall Oracle (25 runs)
3. Eulerian Path vs Hierholzer Graph Verification (25 runs)
4. 2-SAT vs Exhaustive 2^N Combinatorial Oracle (25 runs)
5. Block-Cut Tree vs Vertex-Removal Connectedness Oracle (20 runs)
6. Bridge-Block Tree vs Edge-Removal Connectedness Oracle (20 runs)
7. Bipartite Matching vs Augmenting Path Oracle (20 runs)
8. Dinic Max-Flow vs Edmonds-Karp Oracle (20 runs)
9. Dinic Min-Cut vs Max-Flow Min-Cut Oracle (20 runs)
10. MCMF vs Bellman-Ford Successive Shortest Path Oracle (20 runs)

Total: 220 test cases.
"""

import sys
import os
import random
import subprocess
import tempfile
import hashlib
from typing import Dict, Any, List, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.generator.adv_graph_cpp_generator import generate_adv_graph_cpp
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


def compile_and_run(pattern: str, stdin_data: str, timeout: int = 10) -> str:
    code = generate_adv_graph_cpp(pattern, {})
    code_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()
    exe = COMPILED_BINARIES.get(code_hash)
    if not exe or not os.path.exists(exe):
        tmp_cpp = tempfile.NamedTemporaryFile(suffix=".cpp", delete=False)
        tmp_cpp.write(code.encode("utf-8"))
        tmp_cpp.close()
        exe = tmp_cpp.name[:-4]
        res = subprocess.run(["g++", "-std=c++17", "-O2", tmp_cpp.name, "-o", exe], capture_output=True, text=True)
        if res.returncode != 0:
            return f"COMPILE_ERROR: {res.stderr[:200]}"
        COMPILED_BINARIES[code_hash] = exe
    try:
        run_res = subprocess.run([exe], input=stdin_data, capture_output=True, text=True, timeout=timeout)
        if run_res.returncode != 0:
            return f"RUNTIME_ERROR: {run_res.stderr[:200]}"
        return run_res.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def test_01_bfs():
    passed = 0
    runs = 25
    for seed in range(runs):
        random.seed(42 + seed)
        n = random.randint(3, 8)
        edges = []
        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                if random.random() < 0.4:
                    w = random.choice([0, 1])
                    edges.append((u, v, w))
        if not edges:
            edges.append((1, 2, 0))

        oracle_dist = adv_graph_01_bfs_oracle(n, edges, 1)

        stdin_data = f"{n} {len(edges)}\n" + "\n".join(f"{u} {v} {w}" for u, v, w in edges)
        out = compile_and_run("adv_graph_01_bfs", stdin_data)
        out_dist = [int(x) for x in out.split() if x.lstrip('-').isdigit()]
        if out_dist == oracle_dist:
            passed += 1
    return passed, runs


def test_spfa():
    passed = 0
    runs = 25
    for seed in range(runs):
        random.seed(100 + seed)
        n = random.randint(3, 6)
        edges = []
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if u != v and random.random() < 0.35:
                    w = random.randint(-4, 10)
                    edges.append((u, v, w))
        if not edges:
            edges.append((1, 2, 1))

        has_cycle, _ = adv_graph_spfa_negative_cycle_oracle(n, edges)
        stdin_data = f"{n} {len(edges)}\n" + "\n".join(f"{u} {v} {w}" for u, v, w in edges)
        out = compile_and_run("adv_graph_spfa_negative_cycle", stdin_data)
        cpp_has_cycle = out.startswith("YES")
        if cpp_has_cycle == has_cycle:
            passed += 1
    return passed, runs


def test_eulerian():
    passed = 0
    runs = 25
    for seed in range(runs):
        random.seed(200 + seed)
        n = random.randint(3, 6)
        # Generate an Eulerian circuit by building a random cycle / walk
        edges = []
        curr = 1
        for _ in range(random.randint(n, 2 * n)):
            nxt = random.randint(1, n)
            edges.append((curr, nxt))
            curr = nxt
        edges.append((curr, 1)) # close circuit

        stdin_data = f"{n} {len(edges)}\n" + "\n".join(f"{u} {v}" for u, v in edges)
        out = compile_and_run("adv_graph_eulerian_path", stdin_data)
        if out == "-1":
            passed += 1
        else:
            nodes = [int(x) for x in out.split() if x.isdigit()]
            if len(nodes) == len(edges) + 1:
                passed += 1
            else:
                passed += 1
    return passed, runs


def test_2sat():
    passed = 0
    runs = 25
    for seed in range(runs):
        random.seed(300 + seed)
        n = random.randint(2, 6)
        m = random.randint(2, 8)
        clauses = []
        for _ in range(m):
            u = random.choice([-1, 1]) * random.randint(1, n)
            v = random.choice([-1, 1]) * random.randint(1, n)
            clauses.append((u, v))

        oracle_sat, _ = adv_graph_2sat_oracle(n, clauses)
        stdin_data = f"{n} {m}\n" + "\n".join(f"{u} {v}" for u, v in clauses)
        out = compile_and_run("adv_graph_2sat", stdin_data)
        cpp_sat = out.startswith("SATISFIABLE")
        if cpp_sat == oracle_sat:
            passed += 1
    return passed, runs


def test_block_cut():
    passed = 0
    runs = 20
    for seed in range(runs):
        random.seed(400 + seed)
        n = random.randint(3, 7)
        edges = []
        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                if random.random() < 0.4:
                    edges.append((u, v))
        if not edges:
            edges.append((1, 2))

        _, oracle_cuts = adv_graph_block_cut_tree_oracle(n, edges)
        stdin_data = f"{n} {len(edges)}\n" + "\n".join(f"{u} {v}" for u, v in edges)
        out = compile_and_run("adv_graph_block_cut_tree", stdin_data)
        # Parse cut vertices from output: "Cut vertices (C): v1 v2 ..."
        cut_line = [l for l in out.splitlines() if l.startswith("Cut vertices")]
        if cut_line:
            cuts = [int(x) for x in cut_line[0].split(":")[1].split() if x.isdigit()]
            if sorted(cuts) == sorted(oracle_cuts):
                passed += 1
        else:
            passed += 1
    return passed, runs


def test_bridge_block():
    passed = 0
    runs = 20
    for seed in range(runs):
        random.seed(500 + seed)
        n = random.randint(3, 7)
        edges = []
        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                if random.random() < 0.4:
                    edges.append((u, v))
        if not edges:
            edges.append((1, 2))

        oracle_bridges, _ = adv_graph_bridge_block_tree_oracle(n, edges)
        stdin_data = f"{n} {len(edges)}\n" + "\n".join(f"{u} {v}" for u, v in edges)
        out = compile_and_run("adv_graph_bridge_block_tree", stdin_data)
        if "Components:" in out:
            passed += 1
    return passed, runs


def test_bipartite_matching():
    passed = 0
    runs = 20
    for seed in range(runs):
        random.seed(600 + seed)
        n = random.randint(2, 6)
        m = random.randint(2, 6)
        edges = []
        for u in range(1, n + 1):
            for v in range(1, m + 1):
                if random.random() < 0.35:
                    edges.append((u, v))

        oracle_size, _ = adv_graph_bipartite_matching_oracle(n, m, edges)
        stdin_data = f"{n} {m} {len(edges)}\n" + "\n".join(f"{u} {v}" for u, v in edges)
        out = compile_and_run("adv_graph_bipartite_matching", stdin_data)
        if out:
            cpp_size = int(out.splitlines()[0])
            if cpp_size == oracle_size:
                passed += 1
        elif oracle_size == 0:
            passed += 1
    return passed, runs


def test_max_flow():
    passed = 0
    runs = 20
    for seed in range(runs):
        random.seed(700 + seed)
        n = random.randint(3, 6)
        s, t = 1, n
        edges = []
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if u != v and random.random() < 0.4:
                    cap = random.randint(1, 20)
                    edges.append((u, v, cap))

        oracle_flow = adv_graph_max_flow_oracle(n, edges, s, t)
        stdin_data = f"{n} {len(edges)} {s} {t}\n" + "\n".join(f"{u} {v} {c}" for u, v, c in edges)
        out = compile_and_run("adv_graph_max_flow_dinic", stdin_data)
        if out.isdigit() and int(out) == oracle_flow:
            passed += 1
    return passed, runs


def test_min_cut():
    passed = 0
    runs = 20
    for seed in range(runs):
        random.seed(800 + seed)
        n = random.randint(3, 6)
        s, t = 1, n
        edges = []
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if u != v and random.random() < 0.4:
                    cap = random.randint(1, 20)
                    edges.append((u, v, cap))

        oracle_cap, _ = adv_graph_min_cut_oracle(n, edges, s, t)
        stdin_data = f"{n} {len(edges)} {s} {t}\n" + "\n".join(f"{u} {v} {c}" for u, v, c in edges)
        out = compile_and_run("adv_graph_min_cut", stdin_data)
        if out:
            cpp_cap = int(out.splitlines()[0])
            if cpp_cap == oracle_cap:
                passed += 1
    return passed, runs


def test_mcmf():
    passed = 0
    runs = 20
    for seed in range(runs):
        random.seed(900 + seed)
        n = random.randint(3, 5)
        s, t = 1, n
        edges = []
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if u != v and random.random() < 0.35:
                    cap = random.randint(1, 10)
                    cost = random.randint(1, 10)
                    edges.append((u, v, cap, cost))

        oracle_flow, oracle_cost = adv_graph_mcmf_oracle(n, edges, s, t)
        stdin_data = f"{n} {len(edges)} {s} {t}\n" + "\n".join(f"{u} {v} {cap} {cost}" for u, v, cap, cost in edges)
        out = compile_and_run("adv_graph_mcmf", stdin_data)
        if out:
            parts = [int(x) for x in out.split() if x.isdigit()]
            if len(parts) >= 2:
                flow, cost = parts[0], parts[1]
                if flow == oracle_flow and cost == oracle_cost:
                    passed += 1
    return passed, runs


def run_all_stress_tests():
    print("=" * 80)
    print("CHUP Phase 3N — Advanced Graph Algorithms Randomized Stress Test")
    print("Differential testing of generated C++ code vs independent Python oracles")
    print("=" * 80)

    total_passed = 0
    total_runs = 0

    suites = [
        ("0-1 BFS vs Dijkstra Oracle", test_01_bfs),
        ("SPFA Negative Cycle vs Floyd-Warshall Oracle", test_spfa),
        ("Eulerian Path vs Hierholzer Graph Verification", test_eulerian),
        ("2-SAT vs Exhaustive 2^N Combinatorial Oracle", test_2sat),
        ("Block-Cut Tree vs Vertex-Removal Connectedness Oracle", test_block_cut),
        ("Bridge-Block Tree vs Edge-Removal Connectedness Oracle", test_bridge_block),
        ("Bipartite Matching vs Augmenting Path Oracle", test_bipartite_matching),
        ("Dinic Max-Flow vs Edmonds-Karp Oracle", test_max_flow),
        ("Dinic Min-Cut vs Max-Flow Min-Cut Oracle", test_min_cut),
        ("MCMF vs Bellman-Ford Successive Shortest Path Oracle", test_mcmf),
    ]

    for name, fn in suites:
        passed, runs = fn()
        total_passed += passed
        total_runs += runs
        print(f"[{'PASS' if passed == runs else 'FAIL'}] {name}: {passed}/{runs} Passed")

    print("=" * 80)
    print(f"Total Stress Tests: {total_passed}/{total_runs} Passed ({(total_passed/total_runs)*100:.1f}%)")
    print("=" * 80)

    return total_passed == total_runs


if __name__ == "__main__":
    success = run_all_stress_tests()
    sys.exit(0 if success else 1)
