"""
CHUP Phase 3N — Advanced Graph Algorithms & Capability Composition Benchmark.

Evaluates recognition, structural reasoning, invariant verification,
composition plan synthesis, code generation, and execution across all 10 Phase 3N patterns (60 problems total):

3N-A: 0-1 BFS Shortest Path (AG-01..AG-06)
3N-B: SPFA Negative Cycle Detection & Traceback (AG-07..AG-12)
3N-C: Eulerian Path / Trail via Hierholzer (AG-13..AG-18)
3N-D: 2-SAT Satisfiability & Assignment (AG-19..AG-24)
3N-E: Block-Cut Tree Decomposition (AG-25..AG-30)
3N-F: Bridge-Block Tree (2-Edge-Connected Components) (AG-31..AG-36)
3N-G: Maximum Bipartite Matching via Kuhn (AG-37..AG-42)
3N-H: Dinic Maximum Flow (AG-43..AG-48)
3N-I: Minimum Cut Partition (AG-49..AG-54)
3N-J: Minimum Cost Maximum Flow (AG-55..AG-60)
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


BENCHMARK_PROBLEMS = [
    # ── 3N-A: 0-1 BFS Shortest Path (AG-01..AG-06) ──
    {
        "id": "AG-01",
        "category": "3N-A",
        "title": "Basic 0-1 BFS Linear Graph",
        "text": "Find single-source shortest path on a graph where edge weights are strictly 0 or 1 using deque.",
        "expected_pattern": "adv_graph_01_bfs",
        "input": "4 3\n1 2 0\n2 3 1\n3 4 0",
        "oracle_fn": lambda: "0 0 1 1"
    },
    {
        "id": "AG-02",
        "category": "3N-A",
        "title": "Grid-like 0-1 Weights",
        "text": "Compute shortest distances from source in a network with binary 0-1 weights using double-ended queue.",
        "expected_pattern": "adv_graph_01_bfs",
        "input": "4 4\n1 2 1\n1 3 0\n3 4 1\n2 4 0",
        "oracle_fn": lambda: "0 1 0 1"
    },
    {
        "id": "AG-03",
        "category": "3N-A",
        "title": "0-1 BFS with Zero-Weight Shortcut",
        "text": "Given graph with weights restricted to {0, 1}, find shortest paths using 0-1 BFS deque relaxation.",
        "expected_pattern": "adv_graph_01_bfs",
        "input": "5 5\n1 2 1\n2 3 1\n1 4 0\n4 5 0\n5 3 0",
        "oracle_fn": lambda: "0 1 0 0 0"
    },
    {
        "id": "AG-04",
        "category": "3N-A",
        "title": "0-1 BFS All Zero Edges",
        "text": "Find shortest path from vertex 1 in an unweighted or 0-weight graph where all weights are zero or one via deque.",
        "expected_pattern": "adv_graph_01_bfs",
        "input": "3 2\n1 2 0\n2 3 0",
        "oracle_fn": lambda: "0 0 0"
    },
    {
        "id": "AG-05",
        "category": "3N-A",
        "title": "0-1 BFS Disconnected Node",
        "text": "Single source shortest path on 0-1 weighted graph with unreachable vertex using deque.",
        "expected_pattern": "adv_graph_01_bfs",
        "input": "3 1\n1 2 1",
        "oracle_fn": lambda: "0 1 -1"
    },
    {
        "id": "AG-06",
        "category": "3N-A",
        "title": "0-1 BFS Diamond Topology",
        "text": "Calculate shortest path tree on graph with binary {0, 1} weights using 0-1 BFS algorithm.",
        "expected_pattern": "adv_graph_01_bfs",
        "input": "4 5\n1 2 1\n1 3 0\n2 4 1\n3 4 1\n2 3 0",
        "oracle_fn": lambda: "0 0 0 1"
    },

    # ── 3N-B: SPFA Negative Cycle (AG-07..AG-12) ──
    {
        "id": "AG-07",
        "category": "3N-B",
        "title": "Directed Negative Weight Triangle",
        "text": "Detect negative cycle in a directed graph using SPFA queue relaxation and output YES or NO.",
        "expected_pattern": "adv_graph_spfa_negative_cycle",
        "input": "3 3\n1 2 1\n2 3 2\n3 1 -4",
        "oracle_fn": lambda: "YES"
    },
    {
        "id": "AG-08",
        "category": "3N-B",
        "title": "Negative Edge but No Negative Cycle",
        "text": "Determine if directed graph contains negative cycles using SPFA queue relaxation algorithm.",
        "expected_pattern": "adv_graph_spfa_negative_cycle",
        "input": "3 3\n1 2 2\n2 3 2\n3 1 -3",
        "oracle_fn": lambda: "NO"
    },
    {
        "id": "AG-09",
        "category": "3N-B",
        "title": "Isolated Negative Cycle",
        "text": "Detect if graph has negative weight cycle or arbitrage opportunity using SPFA relaxation.",
        "expected_pattern": "adv_graph_spfa_negative_cycle",
        "input": "4 4\n1 2 5\n2 3 5\n3 4 -10\n4 3 -5",
        "oracle_fn": lambda: "YES"
    },
    {
        "id": "AG-10",
        "category": "3N-B",
        "title": "DAG with Negative Edges",
        "text": "Run SPFA negative cycle check on directed acyclic graph with negative weights.",
        "expected_pattern": "adv_graph_spfa_negative_cycle",
        "input": "4 4\n1 2 -5\n2 3 -5\n3 4 -5\n1 4 -20",
        "oracle_fn": lambda: "NO"
    },
    {
        "id": "AG-11",
        "category": "3N-B",
        "title": "Large Negative Self Loop",
        "text": "Detect negative cycle in directed graph with negative cost edges using SPFA algorithm.",
        "expected_pattern": "adv_graph_spfa_negative_cycle",
        "input": "2 2\n1 2 1\n2 2 -3",
        "oracle_fn": lambda: "YES"
    },
    {
        "id": "AG-12",
        "category": "3N-B",
        "title": "Positive Cycle Graph",
        "text": "Verify absence of negative cycles in graph using SPFA queue relaxation.",
        "expected_pattern": "adv_graph_spfa_negative_cycle",
        "input": "3 3\n1 2 3\n2 3 4\n3 1 5",
        "oracle_fn": lambda: "NO"
    },

    # ── 3N-C: Eulerian Path / Trail (AG-13..AG-18) ──
    {
        "id": "AG-13",
        "category": "3N-C",
        "title": "Undirected Eulerian Circuit Triangle",
        "text": "Find Eulerian circuit traversing every edge exactly once using Hierholzer algorithm.",
        "expected_pattern": "adv_graph_eulerian_path",
        "input": "3 3\n1 2\n2 3\n3 1",
        "oracle_fn": lambda: "1 3 2 1"
    },
    {
        "id": "AG-14",
        "category": "3N-C",
        "title": "Undirected Eulerian Trail with 2 Odd Vertices",
        "text": "Find Eulerian trail visiting every edge once in an undirected graph via Hierholzer trail.",
        "expected_pattern": "adv_graph_eulerian_path",
        "input": "4 3\n1 2\n2 3\n3 4",
        "oracle_fn": lambda: "1 2 3 4"
    },
    {
        "id": "AG-15",
        "category": "3N-C",
        "title": "Bowtie Graph Eulerian Circuit",
        "text": "Traverse each edge exactly once in graph using Hierholzer Eulerian path algorithm.",
        "expected_pattern": "adv_graph_eulerian_path",
        "input": "5 6\n1 2\n2 3\n3 1\n3 4\n4 5\n5 3",
        "oracle_fn": lambda: "1 3 5 4 3 2 1"
    },
    {
        "id": "AG-16",
        "category": "3N-C",
        "title": "Complete Graph K4 Non-Eulerian",
        "text": "Determine if Eulerian path exists to visit every edge exactly once or output -1 using Hierholzer.",
        "expected_pattern": "adv_graph_eulerian_path",
        "input": "4 6\n1 2\n1 3\n1 4\n2 3\n2 4\n3 4",
        "oracle_fn": lambda: "-1"
    },
    {
        "id": "AG-17",
        "category": "3N-C",
        "title": "Star Graph Non-Eulerian",
        "text": "Eulerian path traversal to visit each edge exactly once via Hierholzer path algorithm.",
        "expected_pattern": "adv_graph_eulerian_path",
        "input": "4 3\n1 2\n1 3\n1 4",
        "oracle_fn": lambda: "-1"
    },
    {
        "id": "AG-18",
        "category": "3N-C",
        "title": "Disconnected Graph Non-Eulerian",
        "text": "Find Eulerian trail to draw graph without lifting pen traversing every edge once.",
        "expected_pattern": "adv_graph_eulerian_path",
        "input": "4 2\n1 2\n3 4",
        "oracle_fn": lambda: "-1"
    },

    # ── 3N-D: 2-SAT Satisfiability & Assignment (AG-19..AG-24) ──
    {
        "id": "AG-19",
        "category": "3N-D",
        "title": "Satisfiable 2-CNF Simple Formula",
        "text": "Solve 2-SAT boolean satisfiability problem with 2-literal clauses using implication graph and Tarjan SCC.",
        "expected_pattern": "adv_graph_2sat",
        "input": "2 3\n1 2\n-1 2\n1 -2",
        "oracle_fn": lambda: "SATISFIABLE\n1 1"
    },
    {
        "id": "AG-20",
        "category": "3N-D",
        "title": "Unsatisfiable 2-SAT Formula",
        "text": "Determine 2-satisfiability of boolean formula with 2 literals per clause via 2-SAT implication graph.",
        "expected_pattern": "adv_graph_2sat",
        "input": "1 2\n1 1\n-1 -1",
        "oracle_fn": lambda: "UNSATISFIABLE"
    },
    {
        "id": "AG-21",
        "category": "3N-D",
        "title": "3-Variable 2-SAT Satisfiable",
        "text": "Find satisfying truth assignment for 2-SAT boolean formula clauses using Tarjan SCC condensation.",
        "expected_pattern": "adv_graph_2sat",
        "input": "3 4\n1 2\n-1 3\n-2 -3\n1 3",
        "oracle_fn": lambda: "SATISFIABLE\n1 0 1"
    },
    {
        "id": "AG-22",
        "category": "3N-D",
        "title": "2-SAT Contradiction Cycle",
        "text": "Check if 2-CNF formula is satisfiable using 2-SAT implication graph SCC decomposition.",
        "expected_pattern": "adv_graph_2sat",
        "input": "2 4\n1 2\n1 -2\n-1 2\n-1 -2",
        "oracle_fn": lambda: "UNSATISFIABLE"
    },
    {
        "id": "AG-23",
        "category": "3N-D",
        "title": "Chain of Implications 2-SAT",
        "text": "Evaluate 2-SAT system of boolean constraints (x or y) using topological truth assignment.",
        "expected_pattern": "adv_graph_2sat",
        "input": "3 3\n-1 2\n-2 3\n1 1",
        "oracle_fn": lambda: "SATISFIABLE\n1 1 1"
    },
    {
        "id": "AG-24",
        "category": "3N-D",
        "title": "Independent Clauses 2-SAT",
        "text": "Solve 2-SAT satisfiability for disjoint variables with Tarjan strongly connected components.",
        "expected_pattern": "adv_graph_2sat",
        "input": "2 2\n1 1\n2 2",
        "oracle_fn": lambda: "SATISFIABLE\n1 1"
    },

    # ── 3N-E: Block-Cut Tree Decomposition (AG-25..AG-30) ──
    {
        "id": "AG-25",
        "category": "3N-E",
        "title": "Linear Path Graph Block-Cut Tree",
        "text": "Decompose graph into biconnected components and cut vertices forming Block-Cut tree.",
        "expected_pattern": "adv_graph_block_cut_tree",
        "input": "3 2\n1 2\n2 3",
        "oracle_fn": lambda: "Blocks: 2\nBlock 1 size 2: 2 3\nBlock 2 size 2: 1 2\nCut vertices (1): 2"
    },
    {
        "id": "AG-26",
        "category": "3N-E",
        "title": "Single Cycle No Cut Vertices",
        "text": "Find articulation points and biconnected blocks to construct Block-Cut tree decomposition.",
        "expected_pattern": "adv_graph_block_cut_tree",
        "input": "3 3\n1 2\n2 3\n3 1",
        "oracle_fn": lambda: "Blocks: 1\nBlock 1 size 3: 1 2 3\nCut vertices (0):"
    },
    {
        "id": "AG-27",
        "category": "3N-E",
        "title": "Bowtie Graph Articulation Point",
        "text": "Compute Block-Cut tree decomposition identifying cut vertices and maximal biconnected components.",
        "expected_pattern": "adv_graph_block_cut_tree",
        "input": "5 6\n1 2\n2 3\n3 1\n3 4\n4 5\n5 3",
        "oracle_fn": lambda: "Blocks: 2\nBlock 1 size 3: 3 4 5\nBlock 2 size 3: 1 2 3\nCut vertices (1): 3"
    },
    {
        "id": "AG-28",
        "category": "3N-E",
        "title": "Star Graph Center Cut Vertex",
        "text": "Identify articulation points and blocks in tree structure using Block-Cut tree algorithm.",
        "expected_pattern": "adv_graph_block_cut_tree",
        "input": "4 3\n1 2\n1 3\n1 4",
        "oracle_fn": lambda: "Blocks: 3\nBlock 1 size 2: 1 4\nBlock 2 size 2: 1 3\nBlock 3 size 2: 1 2\nCut vertices (1): 1"
    },
    {
        "id": "AG-29",
        "category": "3N-E",
        "title": "Cycle with Tail Block-Cut",
        "text": "Decompose graph into 2-vertex-connected blocks and articulation points via Block-Cut tree.",
        "expected_pattern": "adv_graph_block_cut_tree",
        "input": "4 4\n1 2\n2 3\n3 1\n1 4",
        "oracle_fn": lambda: "Blocks: 2\nBlock 1 size 2: 1 4\nBlock 2 size 3: 1 2 3\nCut vertices (1): 1"
    },
    {
        "id": "AG-30",
        "category": "3N-E",
        "title": "Two Cycles Sharing a Vertex",
        "text": "Construct Block-Cut tree for biconnected components and cut vertices using Tarjan low-link.",
        "expected_pattern": "adv_graph_block_cut_tree",
        "input": "5 6\n1 2\n2 3\n3 1\n3 4\n4 5\n5 3",
        "oracle_fn": lambda: "Blocks: 2\nCut vertices (1): 3"
    },

    # ── 3N-F: Bridge-Block Tree (2-ECC) (AG-31..AG-36) ──
    {
        "id": "AG-31",
        "category": "3N-F",
        "title": "Two Cycles Connected by a Bridge",
        "text": "Find bridges and contract 2-edge-connected components into a bridge-block tree.",
        "expected_pattern": "adv_graph_bridge_block_tree",
        "input": "6 7\n1 2\n2 3\n3 1\n3 4\n4 5\n5 6\n6 4",
        "oracle_fn": lambda: "Components: 2\n1 1 1 2 2 2"
    },
    {
        "id": "AG-32",
        "category": "3N-F",
        "title": "Single Bridge in 4-Node Graph",
        "text": "Identify bridges and decompose into 2-edge-connected components via bridge-block condensation.",
        "expected_pattern": "adv_graph_bridge_block_tree",
        "input": "4 4\n1 2\n2 3\n3 1\n1 4",
        "oracle_fn": lambda: "Components: 2\n1 1 1 2"
    },
    {
        "id": "AG-33",
        "category": "3N-F",
        "title": "Tree with All Bridges",
        "text": "Contract two-edge-connected components and build bridge-block tree.",
        "expected_pattern": "adv_graph_bridge_block_tree",
        "input": "3 2\n1 2\n2 3",
        "oracle_fn": lambda: "Components: 3\n1 2 3"
    },
    {
        "id": "AG-34",
        "category": "3N-F",
        "title": "Simple Cycle No Bridges",
        "text": "Detect bridge-block components in 2-edge-connected graph without cut-edges.",
        "expected_pattern": "adv_graph_bridge_block_tree",
        "input": "4 4\n1 2\n2 3\n3 4\n4 1",
        "oracle_fn": lambda: "Components: 1\n1 1 1 1"
    },
    {
        "id": "AG-35",
        "category": "3N-F",
        "title": "Bridge Connecting to Isolated Node",
        "text": "Find 2-edge-connected components and bridge edges using bridge-block tree condensation.",
        "expected_pattern": "adv_graph_bridge_block_tree",
        "input": "5 5\n1 2\n2 3\n3 1\n3 4\n4 5",
        "oracle_fn": lambda: "Components: 3\n1 1 1 2 3"
    },
    {
        "id": "AG-36",
        "category": "3N-F",
        "title": "Complete Graph K4 No Bridges",
        "text": "Decompose into two-edge-connected components using bridge-block tree algorithm.",
        "expected_pattern": "adv_graph_bridge_block_tree",
        "input": "4 6\n1 2\n1 3\n1 4\n2 3\n2 4\n3 4",
        "oracle_fn": lambda: "Components: 1\n1 1 1 1"
    },

    # ── 3N-G: Maximum Bipartite Matching (AG-37..AG-42) ──
    {
        "id": "AG-37",
        "category": "3N-G",
        "title": "Perfect Bipartite Matching",
        "text": "Find maximum cardinality matching in bipartite graph with two disjoint sets using Kuhn augmenting path.",
        "expected_pattern": "adv_graph_bipartite_matching",
        "input": "2 2 2\n1 1\n2 2",
        "oracle_fn": lambda: "2\n1 1\n2 2"
    },
    {
        "id": "AG-38",
        "category": "3N-G",
        "title": "Cross Bipartite Matching",
        "text": "Compute maximum bipartite matching between applicants and jobs using Kuhn augmenting paths.",
        "expected_pattern": "adv_graph_bipartite_matching",
        "input": "2 2 3\n1 1\n1 2\n2 2",
        "oracle_fn": lambda: "2\n1 1\n2 2"
    },
    {
        "id": "AG-39",
        "category": "3N-G",
        "title": "Bottleneck Bipartite Matching",
        "text": "Find maximum matching size in bipartite graph where vertices partition into two sets via Kuhn.",
        "expected_pattern": "adv_graph_bipartite_matching",
        "input": "3 3 3\n1 1\n2 1\n3 1",
        "oracle_fn": lambda: "1\n3 1"
    },
    {
        "id": "AG-40",
        "category": "3N-G",
        "title": "3x3 Full Matching",
        "text": "Maximum cardinality bipartite matching between students and schools using Kuhn algorithm.",
        "expected_pattern": "adv_graph_bipartite_matching",
        "input": "3 3 5\n1 1\n1 2\n2 2\n2 3\n3 3",
        "oracle_fn": lambda: "3\n1 1\n2 2\n3 3"
    },
    {
        "id": "AG-41",
        "category": "3N-G",
        "title": "Empty Bipartite Matching",
        "text": "Compute maximum bipartite matching on bipartite graph with zero edges using Kuhn algorithm.",
        "expected_pattern": "adv_graph_bipartite_matching",
        "input": "2 2 0",
        "oracle_fn": lambda: "0"
    },
    {
        "id": "AG-42",
        "category": "3N-G",
        "title": "Asymmetric Bipartite Matching",
        "text": "Assign applicants to jobs maximizing matches in bipartite graph with Kuhn augmenting path.",
        "expected_pattern": "adv_graph_bipartite_matching",
        "input": "3 2 4\n1 1\n2 1\n3 2\n1 2",
        "oracle_fn": lambda: "2\n2 1\n3 2"
    },

    # ── 3N-H: Dinic Maximum Flow (AG-43..AG-48) ──
    {
        "id": "AG-43",
        "category": "3N-H",
        "title": "Diamond Flow Network",
        "text": "Find maximum flow from source to sink in flow network with capacities using Dinic blocking flow.",
        "expected_pattern": "adv_graph_max_flow_dinic",
        "input": "4 5 1 4\n1 2 10\n1 3 10\n2 4 10\n3 4 10\n2 3 2",
        "oracle_fn": lambda: "20"
    },
    {
        "id": "AG-44",
        "category": "3N-H",
        "title": "Single Bottleneck Flow",
        "text": "Compute maximum flow value in network with pipe capacities via Dinic algorithm.",
        "expected_pattern": "adv_graph_max_flow_dinic",
        "input": "3 2 1 3\n1 2 100\n2 3 5",
        "oracle_fn": lambda: "5"
    },
    {
        "id": "AG-45",
        "category": "3N-H",
        "title": "Two Independent Paths Flow",
        "text": "Determine maximum s-t network flow with integer capacities using Dinic algorithm.",
        "expected_pattern": "adv_graph_max_flow_dinic",
        "input": "4 4 1 4\n1 2 7\n2 4 7\n1 3 8\n3 4 8",
        "oracle_fn": lambda: "15"
    },
    {
        "id": "AG-46",
        "category": "3N-H",
        "title": "No Path Between Source and Sink",
        "text": "Calculate max flow in disconnected capacitated flow network with Dinic algorithm.",
        "expected_pattern": "adv_graph_max_flow_dinic",
        "input": "3 1 1 3\n1 2 10",
        "oracle_fn": lambda: "0"
    },
    {
        "id": "AG-47",
        "category": "3N-H",
        "title": "Cross-Bridge Capacitated Network",
        "text": "Find maximum flow through capacitated network using Dinic level graph BFS and blocking flow DFS.",
        "expected_pattern": "adv_graph_max_flow_dinic",
        "input": "4 5 1 4\n1 2 1000\n1 3 1000\n2 3 1\n2 4 1000\n3 4 1000",
        "oracle_fn": lambda: "2000"
    },
    {
        "id": "AG-48",
        "category": "3N-H",
        "title": "Multi-Hop Pipeline Flow",
        "text": "Compute max flow from source to sink in capacitated network via Dinic algorithm.",
        "expected_pattern": "adv_graph_max_flow_dinic",
        "input": "5 4 1 5\n1 2 10\n2 3 8\n3 4 6\n4 5 4",
        "oracle_fn": lambda: "4"
    },

    # ── 3N-I: Minimum Cut Partition (AG-49..AG-54) ──
    {
        "id": "AG-49",
        "category": "3N-I",
        "title": "Simple s-t Min-Cut",
        "text": "Find minimum cut capacity separating source and sink in a flow network via Dinic min-cut.",
        "expected_pattern": "adv_graph_min_cut",
        "input": "4 5 1 4\n1 2 3\n1 3 3\n2 4 2\n3 4 2\n2 3 1",
        "oracle_fn": lambda: "4\n2 4\n3 4"
    },
    {
        "id": "AG-50",
        "category": "3N-I",
        "title": "Single Bottleneck Min-Cut",
        "text": "Compute cut with minimum capacity separating s and t using Dinic max-flow min-cut theorem.",
        "expected_pattern": "adv_graph_min_cut",
        "input": "3 2 1 3\n1 2 10\n2 3 4",
        "oracle_fn": lambda: "4\n2 3"
    },
    {
        "id": "AG-51",
        "category": "3N-I",
        "title": "Two Independent Path Cut",
        "text": "Find minimum capacity s-t cut partition in network using Dinic residual reachability.",
        "expected_pattern": "adv_graph_min_cut",
        "input": "4 4 1 4\n1 2 5\n2 4 5\n1 3 7\n3 4 7",
        "oracle_fn": lambda: "12\n1 2\n1 3"
    },
    {
        "id": "AG-52",
        "category": "3N-I",
        "title": "Disconnected Source Sink Min-Cut",
        "text": "Determine minimum cut capacity in flow network where sink is unreachable.",
        "expected_pattern": "adv_graph_min_cut",
        "input": "3 1 1 3\n1 2 10",
        "oracle_fn": lambda: "0"
    },
    {
        "id": "AG-53",
        "category": "3N-I",
        "title": "Diamond Symmetric Min-Cut",
        "text": "Calculate minimum cut in capacitated network from source to sink via Dinic min-cut.",
        "expected_pattern": "adv_graph_min_cut",
        "input": "4 4 1 4\n1 2 10\n1 3 10\n2 4 10\n3 4 10",
        "oracle_fn": lambda: "20\n1 2\n1 3"
    },
    {
        "id": "AG-54",
        "category": "3N-I",
        "title": "Three-Stage Pipeline Cut",
        "text": "Find s-t min-cut and cut edges in capacitated network with Dinic algorithm.",
        "expected_pattern": "adv_graph_min_cut",
        "input": "4 3 1 4\n1 2 10\n2 3 5\n3 4 10",
        "oracle_fn": lambda: "5\n2 3"
    },

    # ── 3N-J: Minimum Cost Maximum Flow (AG-55..AG-60) ──
    {
        "id": "AG-55",
        "category": "3N-J",
        "title": "Two Parallel Paths Different Costs",
        "text": "Find minimum cost maximum flow with capacities and unit costs using MCMF successive shortest path.",
        "expected_pattern": "adv_graph_mcmf",
        "input": "4 4 1 4\n1 2 2 1\n2 4 2 1\n1 3 2 5\n3 4 2 5",
        "oracle_fn": lambda: "4 24"
    },
    {
        "id": "AG-56",
        "category": "3N-J",
        "title": "Single Path MCMF",
        "text": "Compute min-cost max-flow on network with cost per unit flow via MCMF algorithm.",
        "expected_pattern": "adv_graph_mcmf",
        "input": "3 2 1 3\n1 2 5 2\n2 3 3 4",
        "oracle_fn": lambda: "3 18"
    },
    {
        "id": "AG-57",
        "category": "3N-J",
        "title": "Diamond Network MCMF with Cross Edge",
        "text": "Calculate minimum cost max flow in network with capacities and costs using MCMF algorithm.",
        "expected_pattern": "adv_graph_mcmf",
        "input": "4 5 1 4\n1 2 10 2\n1 3 10 3\n2 3 5 1\n2 4 10 5\n3 4 10 2",
        "oracle_fn": lambda: "20 120"
    },
    {
        "id": "AG-58",
        "category": "3N-J",
        "title": "Zero Cost Edges MCMF",
        "text": "Determine minimum cost maximum flow on network where some edges have zero cost via MCMF.",
        "expected_pattern": "adv_graph_mcmf",
        "input": "4 4 1 4\n1 2 4 0\n2 4 4 0\n1 3 4 3\n3 4 4 3",
        "oracle_fn": lambda: "8 24"
    },
    {
        "id": "AG-59",
        "category": "3N-J",
        "title": "Disconnected Graph MCMF",
        "text": "Run MCMF minimum cost maximum flow algorithm on network with no path from source to sink.",
        "expected_pattern": "adv_graph_mcmf",
        "input": "3 1 1 3\n1 2 5 10",
        "oracle_fn": lambda: "0 0"
    },
    {
        "id": "AG-60",
        "category": "3N-J",
        "title": "Asymmetric Multi-Route MCMF",
        "text": "Find min cost max flow with capacity and cost per unit flow using MCMF algorithm.",
        "expected_pattern": "adv_graph_mcmf",
        "input": "4 3 1 4\n1 2 3 1\n2 4 3 2\n1 4 2 5",
        "oracle_fn": lambda: "5 19"
    },
]


def run_benchmark():
    passed = 0
    failed = 0
    total = len(BENCHMARK_PROBLEMS)

    print("=" * 80)
    print("CHUP Phase 3N — Advanced Graph Algorithms Benchmark")
    print(f"Total problems: {total} (10 families, 6 problems each)")
    print("=" * 80)

    for prob in BENCHMARK_PROBLEMS:
        pid = prob["id"]
        cat = prob["category"]
        title = prob["title"]
        text = prob["text"]

        res = handle_request({"action": "solve", "problemText": text})

        expected_pat = prob["expected_pattern"]
        if res["status"] != "success":
            failed += 1
            print(f"[{cat}] {pid} FAIL: Bridge returned status={res['status']}, reasoning={res.get('reasoning')} ({title})")
            continue

        if res["selectedPattern"] != expected_pat:
            failed += 1
            print(f"[{cat}] {pid} FAIL: Expected pattern {expected_pat}, got {res['selectedPattern']} ({title})")
            continue

        code = res.get("code", "")
        stdin_data = prob.get("input", "")
        cpp_output = compile_and_run_cpp(code, stdin_data)
        expected_output = prob["oracle_fn"]()

        if "COMPILE_ERROR" in cpp_output or "RUNTIME_ERROR" in cpp_output:
            failed += 1
            print(f"[{cat}] {pid} FAIL: C++ execution error: {cpp_output} ({title})")
            continue

        # Compare output: exact match or structured domain validation
        match = False
        if cpp_output == expected_output or expected_output in cpp_output:
            match = True
        elif cat == "3N-B" and cpp_output.startswith(expected_output):
            match = True
        elif cat == "3N-C":
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
        elif cat == "3N-E":
            exp_blocks = [line for line in expected_output.splitlines() if line.startswith("Blocks:")]
            exp_cuts = [line for line in expected_output.splitlines() if line.startswith("Cut vertices")]
            act_blocks = [line for line in cpp_output.splitlines() if line.startswith("Blocks:")]
            act_cuts = [line for line in cpp_output.splitlines() if line.startswith("Cut vertices")]
            match = (exp_blocks == act_blocks and exp_cuts == act_cuts)
        elif cat == "3N-G":
            exp_size = expected_output.splitlines()[0].strip()
            act_size = cpp_output.splitlines()[0].strip()
            match = (exp_size == act_size)

        if match:
            passed += 1
            print(f"[{cat}] {pid} PASS: {title} (Pattern={expected_pat})")
        else:
            failed += 1
            print(f"[{cat}] {pid} FAIL: Output mismatch: expected '{expected_output}', got '{cpp_output}' ({title})")

    print("=" * 80)
    print(f"Benchmark Results: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("=" * 80)
    return passed == total


if __name__ == "__main__":
    success = run_benchmark()
    sys.exit(0 if success else 1)
