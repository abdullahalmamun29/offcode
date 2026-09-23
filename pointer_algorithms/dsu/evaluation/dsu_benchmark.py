"""
CHUP Phase 3H — Advanced Disjoint Set Union (DSU) Domain Benchmark.

Evaluates DSU recognition, structural reasoning, invariant verification,
code generation, and execution across 15 categories (3H-A through 3H-O, 60 problems):

3H-A: Basic Disjoint Set Union (D-01..D-04)
3H-B: Dynamic Incremental Connectivity (D-05..D-08)
3H-C: Component Metadata Tracking (Size, Sum, Min, Max) (D-09..D-12)
3H-D: Weighted / Potential DSU (Relative Differences) (D-13..D-16)
3H-E: Potential Difference Queries (D-17..D-20)
3H-F: Parity / Dynamic 2-Coloring (D-21..D-24)
3H-G: Dynamic Bipartiteness & Odd Cycle Detection (D-25..D-28)
3H-H: Rollback DSU & State Backtracking (D-29..D-32)
3H-I: Historical Snapshot & Reversion (D-33..D-36)
3H-J: Offline Dynamic Connectivity (Segment Tree over Time) (D-37..D-40)
3H-K: Kruskal MST Cycle Prevention Support (D-41..D-44)
3H-L: Constraint Consistency & Contradiction Detection (D-45..D-48)
3H-M: Component Aggregation Under Union (D-49..D-52)
3H-N: Offline vs Online Mismatch Elimination (D-53..D-55)
3H-O: Anti-Patterns & Elimination (D-56..D-60)
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
from pointer_algorithms.dsu.verification.dsu_oracles import (
    oracle_basic_dsu, oracle_component_metadata, oracle_dynamic_connectivity,
    oracle_weighted_dsu, oracle_potential_difference, oracle_parity_dsu,
    oracle_rollback_dsu, oracle_offline_dynamic_connectivity,
    oracle_kruskal_support, oracle_constraint_consistency
)

COMPILED_BINARIES: Dict[str, str] = {}


def compile_and_run_cpp(code: str, stdin_data: str, pattern: str = "", timeout: int = 10) -> str:
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
    # ── 3H-A: Basic Disjoint Set Union (D-01..D-04) ──
    {
        "id": "D-01",
        "category": "3H-A. Basic Disjoint Set Union",
        "text": "Disjoint set union data structure supporting make_set, find, and union operations on elements.",
        "expected_pattern": "dsu_basic",
        "input": "4 4\n1 1 2\n1 2 3\n2 1 3\n3 1 0\n",
        "oracle_fn": lambda: oracle_basic_dsu(4, [(1, 1, 2), (1, 2, 3), (2, 1, 3), (3, 1, 0)])
    },
    {
        "id": "D-02",
        "category": "3H-A. Basic Disjoint Set Union",
        "text": "Maintain equivalence classes with DSU union by size and path compression.",
        "expected_pattern": "dsu_basic",
        "input": "5 4\n1 1 2\n1 3 4\n2 1 4\n2 1 2\n",
        "oracle_fn": lambda: oracle_basic_dsu(5, [(1, 1, 2), (1, 3, 4), (2, 1, 4), (2, 1, 2)])
    },
    {
        "id": "D-03",
        "category": "3H-A. Basic Disjoint Set Union",
        "text": "Partition elements into disjoint subsets using DSU with union and find.",
        "expected_pattern": "dsu_basic",
        "input": "3 3\n1 1 2\n2 2 3\n3 1 0\n",
        "oracle_fn": lambda: oracle_basic_dsu(3, [(1, 1, 2), (2, 2, 3), (3, 1, 0)])
    },
    {
        "id": "D-04",
        "category": "3H-A. Basic Disjoint Set Union",
        "text": "Basic DSU operations with component size queries and set merging.",
        "expected_pattern": "dsu_basic",
        "input": "4 3\n1 1 4\n1 2 3\n3 4 0\n",
        "oracle_fn": lambda: oracle_basic_dsu(4, [(1, 1, 4), (1, 2, 3), (3, 4, 0)])
    },

    # ── 3H-B: Dynamic Incremental Connectivity (D-05..D-08) ──
    {
        "id": "D-05",
        "category": "3H-B. Dynamic Incremental Connectivity",
        "text": "Maintain incremental dynamic connectivity between elements as connection queries arrive online.",
        "expected_pattern": "dsu_dynamic_connectivity",
        "input": "4 4\n1 1 2\n1 3 4\n2 1 2\n2 1 4\n",
        "oracle_fn": lambda: oracle_dynamic_connectivity(4, [(1, 1, 2), (1, 3, 4), (2, 1, 2), (2, 1, 4)])
    },
    {
        "id": "D-06",
        "category": "3H-B. Dynamic Incremental Connectivity",
        "text": "Online dynamic connectivity queries: add connection between accounts and test if connected.",
        "expected_pattern": "dsu_dynamic_connectivity",
        "input": "5 4\n1 1 3\n1 3 5\n2 1 5\n2 2 4\n",
        "oracle_fn": lambda: oracle_dynamic_connectivity(5, [(1, 1, 3), (1, 3, 5), (2, 1, 5), (2, 2, 4)])
    },
    {
        "id": "D-07",
        "category": "3H-B. Dynamic Incremental Connectivity",
        "text": "Incremental connectivity stream with query connectivity and merge operations.",
        "expected_pattern": "dsu_dynamic_connectivity",
        "input": "3 3\n1 1 2\n2 1 2\n2 1 3\n",
        "oracle_fn": lambda: oracle_dynamic_connectivity(3, [(1, 1, 2), (2, 1, 2), (2, 1, 3)])
    },
    {
        "id": "D-08",
        "category": "3H-B. Dynamic Incremental Connectivity",
        "text": "Dynamic incremental connectivity to determine if pairs are in the same cluster.",
        "expected_pattern": "dsu_dynamic_connectivity",
        "input": "4 3\n1 2 4\n1 1 2\n2 1 4\n",
        "oracle_fn": lambda: oracle_dynamic_connectivity(4, [(1, 2, 4), (1, 1, 2), (2, 1, 4)])
    },

    # ── 3H-C: Component Metadata Tracking (D-09..D-12) ──
    {
        "id": "D-09",
        "category": "3H-C. Component Metadata Tracking",
        "text": "Maintain component metadata tracking component size, component sum, minimum and maximum values.",
        "expected_pattern": "dsu_component_metadata",
        "input": "4 3\n10 20 5 40\n1 1 2\n1 3 4\n2 1\n",
        "oracle_fn": lambda: oracle_component_metadata(4, [0, 10, 20, 5, 40], [(1, 1, 2), (1, 3, 4), (2, 1)])
    },
    {
        "id": "D-10",
        "category": "3H-C. Component Metadata Tracking",
        "text": "Disjoint set union tracking total sum and size of each component under set union.",
        "expected_pattern": "dsu_component_metadata",
        "input": "3 2\n100 200 50\n1 1 3\n2 3\n",
        "oracle_fn": lambda: oracle_component_metadata(3, [0, 100, 200, 50], [(1, 1, 3), (2, 3)])
    },
    {
        "id": "D-11",
        "category": "3H-C. Component Metadata Tracking",
        "text": "DSU component metadata aggregation for maximum component size and minimum value.",
        "expected_pattern": "dsu_component_metadata",
        "input": "5 3\n1 2 3 4 5\n1 1 2\n1 2 3\n2 1\n",
        "oracle_fn": lambda: oracle_component_metadata(5, [0, 1, 2, 3, 4, 5], [(1, 1, 2), (1, 2, 3), (2, 1)])
    },
    {
        "id": "D-12",
        "category": "3H-C. Component Metadata Tracking",
        "text": "Component metadata DSU maintaining running sum and extremum of merged components.",
        "expected_pattern": "dsu_component_metadata",
        "input": "4 3\n15 25 10 30\n1 2 4\n1 1 3\n2 2\n",
        "oracle_fn": lambda: oracle_component_metadata(4, [0, 15, 25, 10, 30], [(1, 2, 4), (1, 1, 3), (2, 2)])
    },

    # ── 3H-D: Weighted / Potential DSU (D-13..D-16) ──
    {
        "id": "D-13",
        "category": "3H-D. Weighted / Potential DSU",
        "text": "Weighted DSU maintaining relative potential difference constraints value[x] - value[y] = w.",
        "expected_pattern": "dsu_weighted",
        "input": "4 4\n1 1 2 5\n1 2 3 3\n2 1 3\n2 1 4\n",
        "oracle_fn": lambda: oracle_weighted_dsu(4, [(1, 1, 2, 5), (1, 2, 3, 3), (2, 1, 3), (2, 1, 4)])
    },
    {
        "id": "D-14",
        "category": "3H-D. Weighted / Potential DSU",
        "text": "Potential DSU with offset to root for relative weight differences between items.",
        "expected_pattern": "dsu_weighted",
        "input": "3 3\n1 1 2 10\n1 2 3 -4\n2 1 3\n",
        "oracle_fn": lambda: oracle_weighted_dsu(3, [(1, 1, 2, 10), (1, 2, 3, -4), (2, 1, 3)])
    },
    {
        "id": "D-15",
        "category": "3H-D. Weighted / Potential DSU",
        "text": "Weighted union-find maintaining potential difference equations and detecting inconsistencies.",
        "expected_pattern": "dsu_weighted",
        "input": "3 3\n1 1 2 7\n1 2 3 2\n1 1 3 8\n",
        "oracle_fn": lambda: oracle_weighted_dsu(3, [(1, 1, 2, 7), (1, 2, 3, 2), (1, 1, 3, 8)])
    },
    {
        "id": "D-16",
        "category": "3H-D. Weighted / Potential DSU",
        "text": "Maintain relative potentials with weighted DSU path compression and difference queries.",
        "expected_pattern": "dsu_weighted",
        "input": "4 3\n1 1 3 12\n1 2 4 4\n2 1 3\n",
        "oracle_fn": lambda: oracle_weighted_dsu(4, [(1, 1, 3, 12), (1, 2, 4, 4), (2, 1, 3)])
    },

    # ── 3H-E: Potential Difference Queries (D-17..D-20) ──
    {
        "id": "D-17",
        "category": "3H-E. Potential Difference Queries",
        "text": "Relative potential difference query value[x] - value[y] using weighted DSU.",
        "expected_pattern": "dsu_potential_difference",
        "input": "4 4\n1 1 2 8\n1 2 3 2\n2 1 3\n2 1 4\n",
        "oracle_fn": lambda: oracle_potential_difference(4, [(1, 1, 2, 8), (1, 2, 3, 2), (2, 1, 3), (2, 1, 4)])
    },
    {
        "id": "D-18",
        "category": "3H-E. Potential Difference Queries",
        "text": "Query potential difference between elements if in the same connected component else UNKNOWN.",
        "expected_pattern": "dsu_potential_difference",
        "input": "3 3\n1 1 2 15\n2 1 2\n2 2 3\n",
        "oracle_fn": lambda: oracle_potential_difference(3, [(1, 1, 2, 15), (2, 1, 2), (2, 2, 3)])
    },
    {
        "id": "D-19",
        "category": "3H-E. Potential Difference Queries",
        "text": "Evaluate difference query value[u] - value[v] under transitive potential relations.",
        "expected_pattern": "dsu_potential_difference",
        "input": "5 4\n1 1 2 6\n1 2 5 4\n2 1 5\n2 3 4\n",
        "oracle_fn": lambda: oracle_potential_difference(5, [(1, 1, 2, 6), (1, 2, 5, 4), (2, 1, 5), (2, 3, 4)])
    },
    {
        "id": "D-20",
        "category": "3H-E. Potential Difference Queries",
        "text": "Potential difference queries on weighted disjoint sets with path compression.",
        "expected_pattern": "dsu_potential_difference",
        "input": "4 3\n1 1 4 20\n1 4 2 5\n2 1 2\n",
        "oracle_fn": lambda: oracle_potential_difference(4, [(1, 1, 4, 20), (1, 4, 2, 5), (2, 1, 2)])
    },

    # ── 3H-F: Parity / Dynamic 2-Coloring (D-21..D-24) ──
    {
        "id": "D-21",
        "category": "3H-F. Parity / Dynamic 2-Coloring",
        "text": "Maintain parity constraints color[x] xor color[y] with dynamic 2-coloring DSU.",
        "expected_pattern": "dsu_parity",
        "input": "4 4\n1 1 2 1\n1 2 3 1\n2 1 3\n2 1 4\n",
        "oracle_fn": lambda: oracle_parity_dsu(4, [(1, 1, 2, 1), (1, 2, 3, 1), (2, 1, 3), (2, 1, 4)])
    },
    {
        "id": "D-22",
        "category": "3H-F. Parity / Dynamic 2-Coloring",
        "text": "Dynamic parity DSU tracking same or opposite color between elements.",
        "expected_pattern": "dsu_parity",
        "input": "3 3\n1 1 2 0\n2 1 2\n2 2 3\n",
        "oracle_fn": lambda: oracle_parity_dsu(3, [(1, 1, 2, 0), (2, 1, 2), (2, 2, 3)])
    },
    {
        "id": "D-23",
        "category": "3H-F. Parity / Dynamic 2-Coloring",
        "text": "Parity constraint tracking for friends or enemies using XOR parity DSU.",
        "expected_pattern": "dsu_parity",
        "input": "4 4\n1 1 2 1\n1 2 4 1\n2 1 4\n2 1 2\n",
        "oracle_fn": lambda: oracle_parity_dsu(4, [(1, 1, 2, 1), (1, 2, 4, 1), (2, 1, 4), (2, 1, 2)])
    },
    {
        "id": "D-24",
        "category": "3H-F. Parity / Dynamic 2-Coloring",
        "text": "Incremental two-coloring consistency with parity DSU path compression.",
        "expected_pattern": "dsu_parity",
        "input": "5 3\n1 1 3 1\n1 3 5 0\n2 1 5\n",
        "oracle_fn": lambda: oracle_parity_dsu(5, [(1, 1, 3, 1), (1, 3, 5, 0), (2, 1, 5)])
    },

    # ── 3H-G: Dynamic Bipartiteness & Odd Cycle Detection (D-25..D-28) ──
    {
        "id": "D-25",
        "category": "3H-G. Dynamic Bipartiteness & Odd Cycle Detection",
        "text": "Detect odd-cycle contradiction in dynamic bipartite coloring using parity DSU.",
        "expected_pattern": "dsu_parity",
        "input": "3 3\n1 1 2 1\n1 2 3 1\n1 3 1 1\n",
        "oracle_fn": lambda: oracle_parity_dsu(3, [(1, 1, 2, 1), (1, 2, 3, 1), (1, 3, 1, 1)])
    },
    {
        "id": "D-26",
        "category": "3H-G. Dynamic Bipartiteness & Odd Cycle Detection",
        "text": "Dynamic bipartite consistency check using parity relations.",
        "expected_pattern": "dsu_parity",
        "input": "4 3\n1 1 2 1\n1 3 4 1\n2 1 2\n",
        "oracle_fn": lambda: oracle_parity_dsu(4, [(1, 1, 2, 1), (1, 3, 4, 1), (2, 1, 2)])
    },
    {
        "id": "D-27",
        "category": "3H-G. Dynamic Bipartiteness & Odd Cycle Detection",
        "text": "Check if two elements must have opposite parity under dynamic 2-coloring.",
        "expected_pattern": "dsu_parity",
        "input": "3 2\n1 1 2 1\n2 1 2\n",
        "oracle_fn": lambda: oracle_parity_dsu(3, [(1, 1, 2, 1), (2, 1, 2)])
    },
    {
        "id": "D-28",
        "category": "3H-G. Dynamic Bipartiteness & Odd Cycle Detection",
        "text": "Bipartite consistency constraint checking with parity DSU.",
        "expected_pattern": "dsu_parity",
        "input": "4 3\n1 1 2 0\n1 2 3 1\n2 1 3\n",
        "oracle_fn": lambda: oracle_parity_dsu(4, [(1, 1, 2, 0), (1, 2, 3, 1), (2, 1, 3)])
    },

    # ── 3H-H: Rollback DSU & State Backtracking (D-29..D-32) ──
    {
        "id": "D-29",
        "category": "3H-H. Rollback DSU & State Backtracking",
        "text": "Rollback DSU with union-by-size and undo operation to revert previous merges.",
        "expected_pattern": "dsu_rollback",
        "input": "4 6\n1 1 2\n3\n1 2 3\n2 1 3\n4\n2 1 3\n",
        "oracle_fn": lambda: oracle_rollback_dsu(4, [(1, 1, 2), (3,), (1, 2, 3), (2, 1, 3), (4,), (2, 1, 3)])
    },
    {
        "id": "D-30",
        "category": "3H-H. Rollback DSU & State Backtracking",
        "text": "Undo the last union operation using rollback DSU history stack.",
        "expected_pattern": "dsu_rollback",
        "input": "3 5\n1 1 2\n3\n1 2 3\n4\n2 1 3\n",
        "oracle_fn": lambda: oracle_rollback_dsu(3, [(1, 1, 2), (3,), (1, 2, 3), (4,), (2, 1, 3)])
    },
    {
        "id": "D-31",
        "category": "3H-H. Rollback DSU & State Backtracking",
        "text": "Rollback DSU maintaining union-by-rank without path compression for backtracking.",
        "expected_pattern": "dsu_rollback",
        "input": "4 5\n3\n1 1 4\n2 1 4\n4\n2 1 4\n",
        "oracle_fn": lambda: oracle_rollback_dsu(4, [(3,), (1, 1, 4), (2, 1, 4), (4,), (2, 1, 4)])
    },
    {
        "id": "D-32",
        "category": "3H-H. Rollback DSU & State Backtracking",
        "text": "Revert to previous state with snapshot and rollback DSU operations.",
        "expected_pattern": "dsu_rollback",
        "input": "5 6\n1 1 2\n3\n1 3 4\n1 2 3\n4\n2 1 4\n",
        "oracle_fn": lambda: oracle_rollback_dsu(5, [(1, 1, 2), (3,), (1, 3, 4), (1, 2, 3), (4,), (2, 1, 4)])
    },

    # ── 3H-I: Historical Snapshot & Reversion (D-33..D-36) ──
    {
        "id": "D-33",
        "category": "3H-I. Historical Snapshot & Reversion",
        "text": "Historical snapshot and checkpoint rollback in DSU without path compression.",
        "expected_pattern": "dsu_rollback",
        "input": "4 5\n3\n1 2 3\n2 2 3\n4\n2 2 3\n",
        "oracle_fn": lambda: oracle_rollback_dsu(4, [(3,), (1, 2, 3), (2, 2, 3), (4,), (2, 2, 3)])
    },
    {
        "id": "D-34",
        "category": "3H-I. Historical Snapshot & Reversion",
        "text": "Revert to previous state with rollback snapshot checkpoint.",
        "expected_pattern": "dsu_rollback",
        "input": "3 4\n1 1 3\n3\n1 2 3\n4\n",
        "oracle_fn": lambda: oracle_rollback_dsu(3, [(1, 1, 3), (3,), (1, 2, 3), (4,)])
    },
    {
        "id": "D-35",
        "category": "3H-I. Historical Snapshot & Reversion",
        "text": "Undo union operations using rollback change history stack.",
        "expected_pattern": "dsu_rollback",
        "input": "4 4\n1 1 2\n2 1 2\n3\n4\n",
        "oracle_fn": lambda: oracle_rollback_dsu(4, [(1, 1, 2), (2, 1, 2), (3,), (4,)])
    },
    {
        "id": "D-36",
        "category": "3H-I. Historical Snapshot & Reversion",
        "text": "Checkpoint snapshot and rollback DSU without path compression.",
        "expected_pattern": "dsu_rollback",
        "input": "5 4\n3\n1 1 5\n4\n2 1 5\n",
        "oracle_fn": lambda: oracle_rollback_dsu(5, [(3,), (1, 1, 5), (4,), (2, 1, 5)])
    },

    # ── 3H-J: Offline Dynamic Connectivity (D-37..D-40) ──
    {
        "id": "D-37",
        "category": "3H-J. Offline Dynamic Connectivity",
        "text": "Offline dynamic connectivity using segment tree over time with rollback DSU.",
        "expected_pattern": "dsu_offline_dynamic_connectivity",
        "input": "4 5\n1 1 2\n3 1 2\n2 1 2\n3 1 2\n3 3 4\n",
        "oracle_fn": lambda: oracle_offline_dynamic_connectivity(4, [(1, 1, 2), (3, 1, 2), (2, 1, 2), (3, 1, 2), (3, 3, 4)])
    },
    {
        "id": "D-38",
        "category": "3H-J. Offline Dynamic Connectivity",
        "text": "Process edge additions, edge deletions, and connectivity queries using segment tree over time with all queries known in advance.",
        "expected_pattern": "dsu_offline_dynamic_connectivity",
        "input": "3 4\n1 1 2\n1 2 3\n3 1 3\n2 1 2\n",
        "oracle_fn": lambda: oracle_offline_dynamic_connectivity(3, [(1, 1, 2), (1, 2, 3), (3, 1, 3), (2, 1, 2)])
    },
    {
        "id": "D-39",
        "category": "3H-J. Offline Dynamic Connectivity",
        "text": "Offline dynamic connectivity with active time intervals for edges and connectivity queries.",
        "expected_pattern": "dsu_offline_dynamic_connectivity",
        "input": "4 4\n1 2 3\n3 2 3\n2 2 3\n3 2 3\n",
        "oracle_fn": lambda: oracle_offline_dynamic_connectivity(4, [(1, 2, 3), (3, 2, 3), (2, 2, 3), (3, 2, 3)])
    },
    {
        "id": "D-40",
        "category": "3H-J. Offline Dynamic Connectivity",
        "text": "Segment tree over time with rollback DSU for offline queries with additions and removals.",
        "expected_pattern": "dsu_offline_dynamic_connectivity",
        "input": "3 4\n1 1 3\n3 1 3\n2 1 3\n3 1 3\n",
        "oracle_fn": lambda: oracle_offline_dynamic_connectivity(3, [(1, 1, 3), (3, 1, 3), (2, 1, 3), (3, 1, 3)])
    },

    # ── 3H-K: Kruskal MST Cycle Prevention Support (D-41..D-44) ──
    {
        "id": "D-41",
        "category": "3H-K. Kruskal MST Cycle Prevention Support",
        "text": "DSU Kruskal support for cycle prevention by checking if edge endpoints are in the same disjoint set.",
        "expected_pattern": "dsu_kruskal_support",
        "input": "4 5\n1 2 1\n2 3 2\n3 4 3\n4 1 4\n1 3 5\n",
        "oracle_fn": lambda: str(oracle_kruskal_support(4, [(1, 2, 1), (2, 3, 2), (3, 4, 3), (4, 1, 4), (1, 3, 5)]))
    },
    {
        "id": "D-42",
        "category": "3H-K. Kruskal MST Cycle Prevention Support",
        "text": "Kruskal support DSU maintaining disjoint sets to avoid cycles while selecting minimum weight edges.",
        "expected_pattern": "dsu_kruskal_support",
        "input": "3 3\n1 2 10\n2 3 20\n1 3 30\n",
        "oracle_fn": lambda: str(oracle_kruskal_support(3, [(1, 2, 10), (2, 3, 20), (1, 3, 30)]))
    },
    {
        "id": "D-43",
        "category": "3H-K. Kruskal MST Cycle Prevention Support",
        "text": "DSU support in Kruskal algorithm to detect cycle when edge endpoints share the same root.",
        "expected_pattern": "dsu_kruskal_support",
        "input": "4 4\n1 2 5\n2 3 5\n3 4 5\n1 4 10\n",
        "oracle_fn": lambda: str(oracle_kruskal_support(4, [(1, 2, 5), (2, 3, 5), (3, 4, 5), (1, 4, 10)]))
    },
    {
        "id": "D-44",
        "category": "3H-K. Kruskal MST Cycle Prevention Support",
        "text": "Kruskal support with DSU disjoint set cycle check.",
        "expected_pattern": "dsu_kruskal_support",
        "input": "3 3\n1 2 2\n2 3 3\n1 3 4\n",
        "oracle_fn": lambda: str(oracle_kruskal_support(3, [(1, 2, 2), (2, 3, 3), (1, 3, 4)]))
    },

    # ── 3H-L: Constraint Consistency & Contradiction Detection (D-45..D-48) ──
    {
        "id": "D-45",
        "category": "3H-L. Constraint Consistency & Contradiction Detection",
        "text": "Check consistency and detect contradiction among difference constraints using DSU.",
        "expected_pattern": "dsu_constraint_consistency",
        "input": "3 3\n1 2 5\n2 3 3\n1 3 8\n",
        "oracle_fn": lambda: oracle_constraint_consistency(3, [(1, 2, 5), (2, 3, 3), (1, 3, 8)])
    },
    {
        "id": "D-46",
        "category": "3H-L. Constraint Consistency & Contradiction Detection",
        "text": "Detect contradictory difference constraints in system of equations with DSU.",
        "expected_pattern": "dsu_constraint_consistency",
        "input": "3 3\n1 2 5\n2 3 3\n1 3 9\n",
        "oracle_fn": lambda: oracle_constraint_consistency(3, [(1, 2, 5), (2, 3, 3), (1, 3, 9)])
    },
    {
        "id": "D-47",
        "category": "3H-L. Constraint Consistency & Contradiction Detection",
        "text": "Verify whether system of difference constraints is consistent or inconsistent.",
        "expected_pattern": "dsu_constraint_consistency",
        "input": "4 4\n1 2 10\n2 3 20\n3 4 30\n1 4 60\n",
        "oracle_fn": lambda: oracle_constraint_consistency(4, [(1, 2, 10), (2, 3, 20), (3, 4, 30), (1, 4, 60)])
    },
    {
        "id": "D-48",
        "category": "3H-L. Constraint Consistency & Contradiction Detection",
        "text": "Detect conflicting equations and verify consistency with potential DSU.",
        "expected_pattern": "dsu_constraint_consistency",
        "input": "4 4\n1 2 10\n2 3 20\n3 4 30\n1 4 50\n",
        "oracle_fn": lambda: oracle_constraint_consistency(4, [(1, 2, 10), (2, 3, 20), (3, 4, 30), (1, 4, 50)])
    },

    # ── 3H-M: Component Aggregation Under Union (D-49..D-52) ──
    {
        "id": "D-49",
        "category": "3H-M. Component Aggregation Under Union",
        "text": "DSU component metadata tracking component sum and minimum value across set mergers.",
        "expected_pattern": "dsu_component_metadata",
        "input": "3 2\n5 15 25\n1 1 2\n2 1\n",
        "oracle_fn": lambda: oracle_component_metadata(3, [0, 5, 15, 25], [(1, 1, 2), (2, 1)])
    },
    {
        "id": "D-50",
        "category": "3H-M. Component Aggregation Under Union",
        "text": "Maintain component maximum and total weight under set union using component metadata DSU.",
        "expected_pattern": "dsu_component_metadata",
        "input": "4 3\n10 50 30 20\n1 1 4\n1 2 3\n2 1\n",
        "oracle_fn": lambda: oracle_component_metadata(4, [0, 10, 50, 30, 20], [(1, 1, 4), (1, 2, 3), (2, 1)])
    },
    {
        "id": "D-51",
        "category": "3H-M. Component Aggregation Under Union",
        "text": "Query total sum of the component under set mergers.",
        "expected_pattern": "dsu_component_metadata",
        "input": "3 2\n7 8 9\n1 2 3\n2 3\n",
        "oracle_fn": lambda: oracle_component_metadata(3, [0, 7, 8, 9], [(1, 2, 3), (2, 3)])
    },
    {
        "id": "D-52",
        "category": "3H-M. Component Aggregation Under Union",
        "text": "Component metadata DSU tracking component size and maximum element.",
        "expected_pattern": "dsu_component_metadata",
        "input": "4 3\n2 4 6 8\n1 1 3\n1 2 4\n2 2\n",
        "oracle_fn": lambda: oracle_component_metadata(4, [0, 2, 4, 6, 8], [(1, 1, 3), (1, 2, 4), (2, 2)])
    },

    # ── 3H-N: Offline vs Online Mismatch Elimination (D-53..D-55) ──
    {
        "id": "D-53",
        "category": "3H-N. Offline vs Online Mismatch Elimination",
        "text": "Offline dynamic connectivity with edge insertions and deletions where all queries known in advance.",
        "expected_pattern": "dsu_offline_dynamic_connectivity",
        "anti_pattern_test": True,
        "rejected_pattern": "dsu_basic",
        "expected_rejection_code": "DSU_ONLINE_OFFLINE_MISMATCH"
    },
    {
        "id": "D-54",
        "category": "3H-N. Offline vs Online Mismatch Elimination",
        "text": "Segment tree over time for offline queries with edge deletions.",
        "expected_pattern": "dsu_offline_dynamic_connectivity",
        "anti_pattern_test": True,
        "rejected_pattern": "dsu_basic",
        "expected_rejection_code": "DSU_ONLINE_OFFLINE_MISMATCH"
    },
    {
        "id": "D-55",
        "category": "3H-N. Offline vs Online Mismatch Elimination",
        "text": "Offline dynamic connectivity with active time intervals for edges.",
        "expected_pattern": "dsu_offline_dynamic_connectivity",
        "anti_pattern_test": True,
        "rejected_pattern": "dsu_basic",
        "expected_rejection_code": "DSU_ONLINE_OFFLINE_MISMATCH"
    },

    # ── 3H-O: Anti-Patterns & Elimination (D-56..D-60) ──
    {
        "id": "D-56",
        "category": "3H-O. Anti-Patterns & Elimination",
        "text": "Arbitrary online edge deletion requested without offline knowledge: delete edge between u and v dynamically.",
        "expected_pattern": None,
        "anti_pattern_test": True,
        "rejected_pattern": "dsu_basic",
        "expected_rejection_code": "DSU_DELETION_UNSUPPORTED"
    },
    {
        "id": "D-57",
        "category": "3H-O. Anti-Patterns & Elimination",
        "text": "Online cut edge and disconnect edge operations arriving in real time.",
        "expected_pattern": None,
        "anti_pattern_test": True,
        "rejected_pattern": "dsu_dynamic_connectivity",
        "expected_rejection_code": "DSU_DELETION_UNSUPPORTED"
    },
    {
        "id": "D-58",
        "category": "3H-O. Anti-Patterns & Elimination",
        "text": "Rollback and revert to previous state required with snapshot restoration.",
        "expected_pattern": "dsu_rollback",
        "anti_pattern_test": True,
        "rejected_pattern": "dsu_basic",
        "expected_rejection_code": "DSU_ROLLBACK_REQUIRED"
    },
    {
        "id": "D-59",
        "category": "3H-O. Anti-Patterns & Elimination",
        "text": "Relative potential difference value[x] - value[y] = w constraints between elements.",
        "expected_pattern": "dsu_weighted",
        "anti_pattern_test": True,
        "rejected_pattern": "dsu_basic",
        "expected_rejection_code": "DSU_WEIGHT_MODEL_MISMATCH"
    },
    {
        "id": "D-60",
        "category": "3H-O. Anti-Patterns & Elimination",
        "text": "Dynamic parity constraints color[x] xor color[y] = p with two-coloring consistency.",
        "expected_pattern": "dsu_parity",
        "anti_pattern_test": True,
        "rejected_pattern": "dsu_basic",
        "expected_rejection_code": "DSU_PARITY_MODEL_MISMATCH"
    },
]


def run_benchmark():
    print("=" * 70)
    print("CHUP Phase 3H — Advanced DSU Domain Benchmark (D-01 through D-60)")
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
            actual_out = compile_and_run_cpp(code, stdin_data, actual_pat)

            # Oracle check
            oracle_fn = prob.get("oracle_fn")
            if oracle_fn:
                expected_out = oracle_fn()
                if isinstance(expected_out, list):
                    expected_str = "\n".join(expected_out).strip()
                else:
                    expected_str = str(expected_out).strip()

                if actual_out != expected_str:
                    print(f"  [FAIL] {pid} ({cat}): Output mismatch.\n    Expected: {expected_str}\n    Got: {actual_out}")
                    failed += 1
                    continue

            print(f"  [PASS] {pid} ({cat}): {actual_pat} verified against oracle (output: {actual_out[:40]})")
            passed += 1

        except Exception as e:
            print(f"  [FAIL] {pid} ({cat}): Exception occurred: {e}")
            failed += 1

    print("=" * 70)
    print(f"DSU Benchmark Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 70)
    return passed == total


if __name__ == "__main__":
    success = run_benchmark()
    sys.exit(0 if success else 1)
