"""
CHUP Phase 3N — Advanced Graph Algorithms Discrimination Holdout Evaluation.

Tests discrimination between Advanced Graph patterns (Phase 3N) and competing alternative families:
- 0-1 BFS vs Classical Dijkstra (binary weights vs general real weights)
- SPFA Negative Cycle vs Positive Shortest Path
- Eulerian Trail (Hierholzer) vs Hamiltonian Path (NP-Hard Backtracking)
- 2-SAT (linear SCC) vs 3-SAT (NP-Complete Exponential Backtracking)
- Bipartite Matching vs Classical DSU Partition
- Dinic Max Flow vs Greedy Flow Approximation
- Dinic Min Cut vs Graph Connectivity
- MCMF vs Unweighted Shortest Path
"""

import sys
import os
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request

DISCRIMINATION_PROBLEMS = [
    {
        "id": "AGD-01",
        "title": "General Non-Negative Weights Shortest Path (Compete with Graph Dijkstra)",
        "text": "Find shortest path from source vertex to all other vertices in non-negative weighted graph using Dijkstra priority queue.",
        "expected_family": "graph",
        "expected_pattern": "graph_dijkstra"
    },
    {
        "id": "AGD-02",
        "title": "Strictly 0-1 Binary Weights (Must Select 0-1 BFS over Dijkstra)",
        "text": "Compute single-source shortest path on a graph where edge weights are strictly 0 or 1 using 0-1 BFS deque relaxation.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_01_bfs"
    },
    {
        "id": "AGD-03",
        "title": "Negative Cycles Arbitrage (Select SPFA over Dijkstra)",
        "text": "Detect if directed graph contains negative cycles or negative cost loops using SPFA queue relaxation.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_spfa_negative_cycle"
    },
    {
        "id": "AGD-04",
        "title": "Traverse Every Edge Exactly Once (Eulerian Trail)",
        "text": "Traverse each edge of the graph exactly once via Hierholzer Eulerian trail algorithm.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_eulerian_path"
    },
    {
        "id": "AGD-05",
        "title": "Hamiltonian Path All Vertices (Compete with Exponential Bitmask DP)",
        "text": "Find Hamiltonian path visiting every vertex exactly once in arbitrary graph using state space search backtracking.",
        "expected_family": "dynamic_programming",
        "expected_pattern": "dp_bitmask"
    },
    {
        "id": "AGD-06",
        "title": "2-CNF Clauses Satisfiability (2-SAT)",
        "text": "Determine satisfiability of boolean formula with 2 literals per clause using 2-SAT implication graph and Tarjan SCC.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_2sat"
    },
    {
        "id": "AGD-07",
        "title": "3-CNF Formula Satisfiability (Compete with Constraint Satisfaction)",
        "text": "Find satisfying variable assignment for 3-SAT boolean constraint satisfaction problem using backtracking search.",
        "expected_family": "divide_and_conquer_backtracking",
        "expected_pattern": "backtracking_constraint_satisfaction"
    },
    {
        "id": "AGD-08",
        "title": "Dynamic Disjoint Sets Connectivity (Compete with DSU)",
        "text": "Maintain connected components under incremental edge additions and check connectivity using disjoint set union DSU.",
        "expected_family": "graph",
        "expected_pattern": "graph_dsu"
    },
    {
        "id": "AGD-09",
        "title": "Bipartite Maximum Matching (Select Kuhn Matching)",
        "text": "Find maximum cardinality matching between applicants and jobs in bipartite graph using Kuhn augmenting path algorithm.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_bipartite_matching"
    },
    {
        "id": "AGD-10",
        "title": "Capacitated Maximum Flow (Dinic)",
        "text": "Find maximum flow from source to sink in flow network with capacities using Dinic blocking flow algorithm.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_max_flow_dinic"
    },
    {
        "id": "AGD-11",
        "title": "Minimum Cut Partition (Dinic Min-Cut)",
        "text": "Find minimum capacity s-t cut separating source and sink in a flow network via Dinic min-cut reachability.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_min_cut"
    },
    {
        "id": "AGD-12",
        "title": "Minimum Cost Maximum Flow (MCMF)",
        "text": "Find minimum cost maximum flow with capacities and unit costs using MCMF successive shortest path.",
        "expected_family": "adv_graph",
        "expected_pattern": "adv_graph_mcmf"
    }
]


def run_discrimination_holdout():
    passed = 0
    failed = 0
    total = len(DISCRIMINATION_PROBLEMS)

    print("=" * 80)
    print("CHUP Phase 3N — Advanced Graph Discrimination Holdout Evaluation")
    print(f"Total problems: {total} (Competitor & boundary discrimination)")
    print("=" * 80)

    for prob in DISCRIMINATION_PROBLEMS:
        pid = prob["id"]
        title = prob["title"]
        text = prob["text"]
        exp_family = prob["expected_family"]
        exp_pattern = prob["expected_pattern"]

        res = handle_request({"action": "solve", "problemText": text})

        act_family = res.get("family")
        act_pattern = res.get("selectedPattern")

        if act_family == exp_family and act_pattern == exp_pattern:
            passed += 1
            print(f"{pid} PASS: {title} -> {act_family} / {act_pattern}")
        else:
            failed += 1
            print(f"{pid} FAIL: {title}")
            print(f"   Expected: {exp_family} / {exp_pattern}")
            print(f"   Got:      {act_family} / {act_pattern}")

    print("=" * 80)
    print(f"Discrimination Holdout Results: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("=" * 80)
    return passed == total


if __name__ == "__main__":
    success = run_discrimination_holdout()
    sys.exit(0 if success else 1)
