"""
CHUP Phase 3J — Segment Tree Domain Benchmark.

Evaluates Segment Tree recognition, structural reasoning, invariant verification,
code generation, and execution across 15 categories (3J-A through 3J-O, 60 problems):

3J-A: Point Update & Range Sum Query (ST-01..ST-04)
3J-B: Point Update & Range Extremum (Min / Max) Query (ST-05..ST-08)
3J-C: Point Update & Range GCD Query (ST-09..ST-12)
3J-D: Range Add & Range Sum Query (Lazy Propagation) (ST-13..ST-16)
3J-E: Range Assignment & Range Sum Query (ST-17..ST-20)
3J-F: Combined Range Assignment & Range Addition (Lazy Composition) (ST-21..ST-24)
3J-G: Simultaneous Multi-Attribute Metadata Aggregation (Sum, Min, Max, Count) (ST-25..ST-28)
3J-H: Maximum Contiguous Subarray Sum Query (ST-29..ST-32)
3J-I: Frequency Segment Tree & K-th Smallest Element Search (ST-33..ST-36)
3J-J: Interval Statistics (Extrema with Multiplicity / Frequency) (ST-37..ST-40)
3J-K: Linear-Time O(N) Tree Construction & Batch Initialization (ST-41..ST-44)
3J-L: Boundary Handling & Canonical Interval Decomposition (ST-45..ST-48)
3J-M: Non-Commutative Associative Merge Verification (ST-49..ST-52)
3J-N: 64-bit Integer Overflow & Width Safety Policy (ST-53..ST-56)
3J-O: Anti-Pattern Elimination & Structural Incompatibility (ST-57..ST-60)
"""

import sys
import os
import subprocess
import tempfile
import hashlib
from typing import Dict, Any, List, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.segment_tree.verification.segment_tree_oracles import (
    SegmentTreeOracle, LazyRangeAddSegmentTreeOracle, LazyRangeAssignSegmentTreeOracle,
    CombinedLazySegmentTreeOracle, MetadataSegmentTreeOracle, MaxSubarraySegmentTreeOracle,
    FrequencySegmentTreeOracle, IntervalStatisticsSegmentTreeOracle
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


# ── Oracle Runner Helpers ──

def run_oracle_point_update_range_sum(n: int, a: List[int], queries: List[Tuple[int, ...]]) -> str:
    st = SegmentTreeOracle(a, op="sum")
    out = []
    for q in queries:
        if q[0] == 1:
            st.update(q[1], q[2])
        elif q[0] == 2:
            out.append(str(st.query(q[1], q[2])))
    return "\n".join(out)


def run_oracle_point_update_range_min(n: int, a: List[int], queries: List[Tuple[int, ...]]) -> str:
    st = SegmentTreeOracle(a, op="min")
    out = []
    for q in queries:
        if q[0] == 1:
            st.update(q[1], q[2])
        elif q[0] == 2:
            out.append(str(st.query(q[1], q[2])))
    return "\n".join(out)


def run_oracle_point_update_range_max(n: int, a: List[int], queries: List[Tuple[int, ...]]) -> str:
    st = SegmentTreeOracle(a, op="max")
    out = []
    for q in queries:
        if q[0] == 1:
            st.update(q[1], q[2])
        elif q[0] == 2:
            out.append(str(st.query(q[1], q[2])))
    return "\n".join(out)


def run_oracle_point_update_range_gcd(n: int, a: List[int], queries: List[Tuple[int, ...]]) -> str:
    st = SegmentTreeOracle(a, op="gcd")
    out = []
    for q in queries:
        if q[0] == 1:
            st.update(q[1], q[2])
        elif q[0] == 2:
            out.append(str(st.query(q[1], q[2])))
    return "\n".join(out)


def run_oracle_range_add_sum(n: int, a: List[int], queries: List[Tuple[int, ...]]) -> str:
    st = LazyRangeAddSegmentTreeOracle(a)
    out = []
    for q in queries:
        if q[0] == 1:
            st.range_add(q[1], q[2], q[3])
        elif q[0] == 2:
            out.append(str(st.range_query(q[1], q[2])))
    return "\n".join(out)


def run_oracle_range_assign_sum(n: int, a: List[int], queries: List[Tuple[int, ...]]) -> str:
    st = LazyRangeAssignSegmentTreeOracle(a)
    out = []
    for q in queries:
        if q[0] == 1:
            st.range_assign(q[1], q[2], q[3])
        elif q[0] == 2:
            out.append(str(st.range_query(q[1], q[2])))
    return "\n".join(out)


def run_oracle_combined_lazy(n: int, a: List[int], queries: List[Tuple[int, ...]]) -> str:
    st = CombinedLazySegmentTreeOracle(a)
    out = []
    for q in queries:
        if q[0] == 1:
            st.range_add(q[1], q[2], q[3])
        elif q[0] == 2:
            st.range_assign(q[1], q[2], q[3])
        elif q[0] == 3:
            out.append(str(st.range_query(q[1], q[2])))
    return "\n".join(out)


def run_oracle_metadata(n: int, a: List[int], queries: List[Tuple[int, ...]]) -> str:
    st = MetadataSegmentTreeOracle(a)
    out = []
    for q in queries:
        if q[0] == 1:
            st.update(q[1], q[2])
        elif q[0] == 2:
            s, mn, mx, c = st.query(q[1], q[2])
            out.append(f"{s} {mn} {mx} {c}")
    return "\n".join(out)


def run_oracle_max_subarray(n: int, a: List[int], queries: List[Tuple[int, ...]]) -> str:
    st = MaxSubarraySegmentTreeOracle(a)
    out = []
    for q in queries:
        if q[0] == 1:
            st.update(q[1], q[2])
        elif q[0] == 2:
            out.append(str(st.query(q[1], q[2])))
    return "\n".join(out)


def run_oracle_frequency_kth(max_val: int, queries: List[Tuple[int, ...]]) -> str:
    st = FrequencySegmentTreeOracle(max_val)
    out = []
    for q in queries:
        if q[0] == 1:
            st.add(q[1], 1)
        elif q[0] == 2:
            st.add(q[1], -1)
        elif q[0] == 3:
            out.append(str(st.query_kth(q[1])))
    return "\n".join(out)


def run_oracle_interval_statistics(n: int, a: List[int], queries: List[Tuple[int, ...]]) -> str:
    st = IntervalStatisticsSegmentTreeOracle(a)
    out = []
    for q in queries:
        if q[0] == 1:
            st.update(q[1], q[2])
        elif q[0] == 2:
            mn, mnc, mx, mxc = st.query(q[1], q[2])
            out.append(f"{mn} {mnc} {mx} {mxc}")
    return "\n".join(out)


# ── Benchmark Problem Definitions ──

BENCHMARK_PROBLEMS: List[Dict[str, Any]] = [
    # ── 3J-A: Point Update & Range Sum Query (ST-01..ST-04) ──
    {
        "id": "ST-01",
        "category": "3J-A",
        "text": "Segment tree for dynamic point updates and range sum queries on array of length N.",
        "pattern": "segment_tree_point_update_range_query",
        "input": "5 4\n1 2 3 4 5\n2 1 5\n1 3 10\n2 1 5\n2 2 4",
        "runner": lambda: run_oracle_point_update_range_sum(5, [0, 1, 2, 3, 4, 5], [(2, 1, 5), (1, 3, 10), (2, 1, 5), (2, 2, 4)])
    },
    {
        "id": "ST-02",
        "category": "3J-A",
        "text": "Maintain array with point modification at index and range sum queries using segment tree.",
        "pattern": "segment_tree_point_update_range_query",
        "input": "6 3\n10 20 30 40 50 60\n2 2 5\n1 4 100\n2 3 6",
        "runner": lambda: run_oracle_point_update_range_sum(6, [0, 10, 20, 30, 40, 50, 60], [(2, 2, 5), (1, 4, 100), (2, 3, 6)])
    },
    {
        "id": "ST-03",
        "category": "3J-A",
        "text": "Segment tree point update and range query with sum aggregation over dynamic sequence.",
        "pattern": "segment_tree_point_update_range_query",
        "input": "4 4\n5 5 5 5\n2 1 4\n1 1 2\n1 4 8\n2 1 4",
        "runner": lambda: run_oracle_point_update_range_sum(4, [0, 5, 5, 5, 5], [(2, 1, 4), (1, 1, 2), (1, 4, 8), (2, 1, 4)])
    },
    {
        "id": "ST-04",
        "category": "3J-A",
        "text": "Point update and range sum queries using segment tree on large array.",
        "pattern": "segment_tree_point_update_range_query",
        "input": "5 3\n0 0 0 0 0\n1 3 7\n1 5 12\n2 1 5",
        "runner": lambda: run_oracle_point_update_range_sum(5, [0, 0, 0, 0, 0, 0], [(1, 3, 7), (1, 5, 12), (2, 1, 5)])
    },

    # ── 3J-B: Point Update & Range Extremum (Min / Max) Query (ST-05..ST-08) ──
    {
        "id": "ST-05",
        "category": "3J-B",
        "text": "Segment tree for range minimum query with point updates on array.",
        "pattern": "segment_tree_point_update_range_query",
        "op": "min",
        "input": "6 4\n5 2 8 1 9 3\n2 1 6\n1 4 10\n2 1 6\n2 3 5",
        "runner": lambda: run_oracle_point_update_range_min(6, [0, 5, 2, 8, 1, 9, 3], [(2, 1, 6), (1, 4, 10), (2, 1, 6), (2, 3, 5)])
    },
    {
        "id": "ST-06",
        "category": "3J-B",
        "text": "Range minimum queries and point updates using segment tree.",
        "pattern": "segment_tree_point_update_range_query",
        "op": "min",
        "input": "5 3\n7 4 9 2 6\n2 2 4\n1 4 15\n2 2 4",
        "runner": lambda: run_oracle_point_update_range_min(5, [0, 7, 4, 9, 2, 6], [(2, 2, 4), (1, 4, 15), (2, 2, 4)])
    },
    {
        "id": "ST-07",
        "category": "3J-B",
        "text": "Segment tree for range maximum queries with point modifications.",
        "pattern": "segment_tree_point_update_range_query",
        "op": "max",
        "input": "5 4\n1 8 3 7 2\n2 1 5\n1 3 15\n2 1 5\n2 4 5",
        "runner": lambda: run_oracle_point_update_range_max(5, [0, 1, 8, 3, 7, 2], [(2, 1, 5), (1, 3, 15), (2, 1, 5), (2, 4, 5)])
    },
    {
        "id": "ST-08",
        "category": "3J-B",
        "text": "Range maximum query and point update on sequence using segment tree.",
        "pattern": "segment_tree_point_update_range_query",
        "op": "max",
        "input": "4 3\n10 5 20 15\n2 1 3\n1 2 25\n2 1 3",
        "runner": lambda: run_oracle_point_update_range_max(4, [0, 10, 5, 20, 15], [(2, 1, 3), (1, 2, 25), (2, 1, 3)])
    },

    # ── 3J-C: Point Update & Range GCD Query (ST-09..ST-12) ──
    {
        "id": "ST-09",
        "category": "3J-C",
        "text": "Segment tree for greatest common divisor in range with point updates.",
        "pattern": "segment_tree_point_update_range_query",
        "op": "gcd",
        "input": "5 4\n12 18 24 36 60\n2 1 5\n1 3 30\n2 1 5\n2 2 4",
        "runner": lambda: run_oracle_point_update_range_gcd(5, [0, 12, 18, 24, 36, 60], [(2, 1, 5), (1, 3, 30), (2, 1, 5), (2, 2, 4)])
    },
    {
        "id": "ST-10",
        "category": "3J-C",
        "text": "Range gcd queries with point updates using segment tree.",
        "pattern": "segment_tree_point_update_range_query",
        "op": "gcd",
        "input": "4 3\n8 16 32 64\n2 1 4\n1 2 12\n2 1 4",
        "runner": lambda: run_oracle_point_update_range_gcd(4, [0, 8, 16, 32, 64], [(2, 1, 4), (1, 2, 12), (2, 1, 4)])
    },
    {
        "id": "ST-11",
        "category": "3J-C",
        "text": "Dynamic point modifications with range gcd queries on segment tree.",
        "pattern": "segment_tree_point_update_range_query",
        "op": "gcd",
        "input": "5 3\n7 14 21 28 35\n2 1 5\n1 1 10\n2 1 5",
        "runner": lambda: run_oracle_point_update_range_gcd(5, [0, 7, 14, 21, 28, 35], [(2, 1, 5), (1, 1, 10), (2, 1, 5)])
    },
    {
        "id": "ST-12",
        "category": "3J-C",
        "text": "Segment tree point update and range gcd query.",
        "pattern": "segment_tree_point_update_range_query",
        "op": "gcd",
        "input": "6 3\n15 25 35 45 55 65\n2 2 5\n1 4 20\n2 2 5",
        "runner": lambda: run_oracle_point_update_range_gcd(6, [0, 15, 25, 35, 45, 55, 65], [(2, 2, 5), (1, 4, 20), (2, 2, 5)])
    },

    # ── 3J-D: Range Add & Range Sum Query (Lazy Propagation) (ST-13..ST-16) ──
    {
        "id": "ST-13",
        "category": "3J-D",
        "text": "Segment tree with lazy propagation for range addition and range sum queries.",
        "pattern": "segment_tree_range_add_range_query",
        "input": "5 4\n1 2 3 4 5\n2 1 5\n1 2 4 10\n2 1 5\n2 2 4",
        "runner": lambda: run_oracle_range_add_sum(5, [0, 1, 2, 3, 4, 5], [(2, 1, 5), (1, 2, 4, 10), (2, 1, 5), (2, 2, 4)])
    },
    {
        "id": "ST-14",
        "category": "3J-D",
        "text": "Range add delta to all elements in range and query range sum using lazy segment tree.",
        "pattern": "segment_tree_range_add_range_query",
        "input": "6 4\n0 0 0 0 0 0\n1 1 3 5\n1 4 6 10\n2 1 6\n2 3 4",
        "runner": lambda: run_oracle_range_add_sum(6, [0, 0, 0, 0, 0, 0, 0], [(1, 1, 3, 5), (1, 4, 6, 10), (2, 1, 6), (2, 3, 4)])
    },
    {
        "id": "ST-15",
        "category": "3J-D",
        "text": "Increment range and query interval sum with lazy propagation segment tree.",
        "pattern": "segment_tree_range_add_range_query",
        "input": "4 4\n10 10 10 10\n2 1 4\n1 2 3 5\n2 1 4\n2 2 3",
        "runner": lambda: run_oracle_range_add_sum(4, [0, 10, 10, 10, 10], [(2, 1, 4), (1, 2, 3, 5), (2, 1, 4), (2, 2, 3)])
    },
    {
        "id": "ST-16",
        "category": "3J-D",
        "text": "Segment tree range addition and range sum queries.",
        "pattern": "segment_tree_range_add_range_query",
        "input": "5 3\n1 1 1 1 1\n1 1 5 2\n1 2 4 3\n2 1 5",
        "runner": lambda: run_oracle_range_add_sum(5, [0, 1, 1, 1, 1, 1], [(1, 1, 5, 2), (1, 2, 4, 3), (2, 1, 5)])
    },

    # ── 3J-E: Range Assignment & Range Sum Query (ST-17..ST-20) ──
    {
        "id": "ST-17",
        "category": "3J-E",
        "text": "Segment tree with lazy propagation for range assignment and range sum queries.",
        "pattern": "segment_tree_range_assign_range_query",
        "input": "5 4\n1 2 3 4 5\n2 1 5\n1 2 4 7\n2 1 5\n2 2 4",
        "runner": lambda: run_oracle_range_assign_sum(5, [0, 1, 2, 3, 4, 5], [(2, 1, 5), (1, 2, 4, 7), (2, 1, 5), (2, 2, 4)])
    },
    {
        "id": "ST-18",
        "category": "3J-E",
        "text": "Set all elements in range to constant value and query range sum using segment tree.",
        "pattern": "segment_tree_range_assign_range_query",
        "input": "6 4\n10 20 30 40 50 60\n1 1 3 5\n2 1 6\n1 3 5 0\n2 1 6",
        "runner": lambda: run_oracle_range_assign_sum(6, [0, 10, 20, 30, 40, 50, 60], [(1, 1, 3, 5), (2, 1, 6), (1, 3, 5, 0), (2, 1, 6)])
    },
    {
        "id": "ST-19",
        "category": "3J-E",
        "text": "Overwrite interval values and answer range queries with lazy segment tree.",
        "pattern": "segment_tree_range_assign_range_query",
        "input": "4 4\n2 2 2 2\n2 1 4\n1 2 3 10\n2 1 4\n2 2 3",
        "runner": lambda: run_oracle_range_assign_sum(4, [0, 2, 2, 2, 2], [(2, 1, 4), (1, 2, 3, 10), (2, 1, 4), (2, 2, 3)])
    },
    {
        "id": "ST-20",
        "category": "3J-E",
        "text": "Segment tree range assignment and range sum query.",
        "pattern": "segment_tree_range_assign_range_query",
        "input": "5 3\n5 5 5 5 5\n1 1 5 1\n1 2 4 3\n2 1 5",
        "runner": lambda: run_oracle_range_assign_sum(5, [0, 5, 5, 5, 5, 5], [(1, 1, 5, 1), (1, 2, 4, 3), (2, 1, 5)])
    },

    # ── 3J-F: Combined Range Assignment & Range Addition (ST-21..ST-24) ──
    {
        "id": "ST-21",
        "category": "3J-F",
        "text": "Segment tree supporting both range assignment and range add with range queries.",
        "pattern": "segment_tree_combined_lazy_range_query",
        "input": "5 4\n1 2 3 4 5\n1 1 5 2\n3 1 5\n2 2 4 10\n3 1 5",
        "runner": lambda: run_oracle_combined_lazy(5, [0, 1, 2, 3, 4, 5], [(1, 1, 5, 2), (3, 1, 5), (2, 2, 4, 10), (3, 1, 5)])
    },
    {
        "id": "ST-22",
        "category": "3J-F",
        "text": "Combined lazy segment tree with range add and range assign operations.",
        "pattern": "segment_tree_combined_lazy_range_query",
        "input": "6 5\n0 0 0 0 0 0\n2 1 6 5\n1 2 4 3\n3 1 6\n2 3 5 2\n3 1 6",
        "runner": lambda: run_oracle_combined_lazy(6, [0, 0, 0, 0, 0, 0, 0], [(2, 1, 6, 5), (1, 2, 4, 3), (3, 1, 6), (2, 3, 5, 2), (3, 1, 6)])
    },
    {
        "id": "ST-23",
        "category": "3J-F",
        "text": "Segment tree with combined lazy tags for interval assignment and addition.",
        "pattern": "segment_tree_combined_lazy_range_query",
        "input": "4 4\n10 10 10 10\n1 1 4 5\n2 2 3 0\n3 1 4\n3 2 3",
        "runner": lambda: run_oracle_combined_lazy(4, [0, 10, 10, 10, 10], [(1, 1, 4, 5), (2, 2, 3, 0), (3, 1, 4), (3, 2, 3)])
    },
    {
        "id": "ST-24",
        "category": "3J-F",
        "text": "Both range assignment and range add queries using combined lazy segment tree.",
        "pattern": "segment_tree_combined_lazy_range_query",
        "input": "5 4\n1 1 1 1 1\n2 1 5 10\n1 3 5 5\n3 1 5\n3 1 2",
        "runner": lambda: run_oracle_combined_lazy(5, [0, 1, 1, 1, 1, 1], [(2, 1, 5, 10), (1, 3, 5, 5), (3, 1, 5), (3, 1, 2)])
    },

    # ── 3J-G: Simultaneous Multi-Attribute Metadata Aggregation (ST-25..ST-28) ──
    {
        "id": "ST-25",
        "category": "3J-G",
        "text": "Segment tree with composite node metadata: sum, min, and max simultaneously with point updates.",
        "pattern": "segment_tree_metadata_aggregate",
        "input": "5 4\n3 1 4 1 5\n2 1 5\n1 2 10\n2 1 5\n2 3 5",
        "runner": lambda: run_oracle_metadata(5, [0, 3, 1, 4, 1, 5], [(2, 1, 5), (1, 2, 10), (2, 1, 5), (2, 3, 5)])
    },
    {
        "id": "ST-26",
        "category": "3J-G",
        "text": "Simultaneous aggregate statistics sum, min, max, count with point updates using segment tree.",
        "pattern": "segment_tree_metadata_aggregate",
        "input": "6 3\n5 8 2 1 9 4\n2 2 5\n1 4 12\n2 2 5",
        "runner": lambda: run_oracle_metadata(6, [0, 5, 8, 2, 1, 9, 4], [(2, 2, 5), (1, 4, 12), (2, 2, 5)])
    },
    {
        "id": "ST-27",
        "category": "3J-G",
        "text": "Segment tree composite node metadata for multi-attribute queries.",
        "pattern": "segment_tree_metadata_aggregate",
        "input": "4 3\n10 20 30 40\n2 1 4\n1 3 5\n2 1 4",
        "runner": lambda: run_oracle_metadata(4, [0, 10, 20, 30, 40], [(2, 1, 4), (1, 3, 5), (2, 1, 4)])
    },
    {
        "id": "ST-28",
        "category": "3J-G",
        "text": "Composite node metadata segment tree for sum min max count.",
        "pattern": "segment_tree_metadata_aggregate",
        "input": "5 3\n1 2 3 4 5\n1 1 10\n2 1 5\n2 2 4",
        "runner": lambda: run_oracle_metadata(5, [0, 1, 2, 3, 4, 5], [(1, 1, 10), (2, 1, 5), (2, 2, 4)])
    },

    # ── 3J-H: Maximum Contiguous Subarray Sum Query (ST-29..ST-32) ──
    {
        "id": "ST-29",
        "category": "3J-H",
        "text": "Segment tree for maximum contiguous subarray sum queries with point updates.",
        "pattern": "segment_tree_max_subarray",
        "input": "5 4\n1 -2 3 4 -1\n2 1 5\n1 2 5\n2 1 5\n2 4 5",
        "runner": lambda: run_oracle_max_subarray(5, [0, 1, -2, 3, 4, -1], [(2, 1, 5), (1, 2, 5), (2, 1, 5), (2, 4, 5)])
    },
    {
        "id": "ST-30",
        "category": "3J-H",
        "text": "Maximum subarray sum with point updates on dynamic sequence using segment tree.",
        "pattern": "segment_tree_max_subarray",
        "input": "6 4\n-3 4 -1 2 -5 3\n2 1 6\n1 5 10\n2 1 6\n2 1 3",
        "runner": lambda: run_oracle_max_subarray(6, [0, -3, 4, -1, 2, -5, 3], [(2, 1, 6), (1, 5, 10), (2, 1, 6), (2, 1, 3)])
    },
    {
        "id": "ST-31",
        "category": "3J-H",
        "text": "Max contiguous subarray sum queries with point modifications via segment tree.",
        "pattern": "segment_tree_max_subarray",
        "input": "4 3\n-5 -2 -8 -1\n2 1 4\n1 3 10\n2 1 4",
        "runner": lambda: run_oracle_max_subarray(4, [0, -5, -2, -8, -1], [(2, 1, 4), (1, 3, 10), (2, 1, 4)])
    },
    {
        "id": "ST-32",
        "category": "3J-H",
        "text": "Segment tree maximum subarray sum query.",
        "pattern": "segment_tree_max_subarray",
        "input": "5 3\n2 -1 2 3 -9\n2 1 4\n1 5 20\n2 1 5",
        "runner": lambda: run_oracle_max_subarray(5, [0, 2, -1, 2, 3, -9], [(2, 1, 4), (1, 5, 20), (2, 1, 5)])
    },

    # ── 3J-I: Frequency Segment Tree & K-th Smallest Element Search (ST-33..ST-36) ──
    {
        "id": "ST-33",
        "category": "3J-I",
        "text": "Frequency segment tree for order statistic and k-th smallest element search.",
        "pattern": "segment_tree_frequency_order_statistic",
        "input": "10 5\n1 5\n1 3\n1 7\n3 2\n3 1",
        "runner": lambda: run_oracle_frequency_kth(10, [(1, 5), (1, 3), (1, 7), (3, 2), (3, 1)])
    },
    {
        "id": "ST-34",
        "category": "3J-I",
        "text": "K-th element in frequency segment tree with arbitrary decrements and insertions.",
        "pattern": "segment_tree_frequency_order_statistic",
        "input": "20 6\n1 10\n1 5\n1 15\n3 2\n2 5\n3 2",
        "runner": lambda: run_oracle_frequency_kth(20, [(1, 10), (1, 5), (1, 15), (3, 2), (2, 5), (3, 2)])
    },
    {
        "id": "ST-35",
        "category": "3J-I",
        "text": "Dynamic order statistic search on frequency segment tree.",
        "pattern": "segment_tree_frequency_order_statistic",
        "input": "10 4\n1 2\n1 2\n1 4\n3 2",
        "runner": lambda: run_oracle_frequency_kth(10, [(1, 2), (1, 2), (1, 4), (3, 2)])
    },
    {
        "id": "ST-36",
        "category": "3J-I",
        "text": "Frequency segment tree order statistics with updates.",
        "pattern": "segment_tree_frequency_order_statistic",
        "input": "8 4\n1 1\n1 8\n1 4\n3 3",
        "runner": lambda: run_oracle_frequency_kth(8, [(1, 1), (1, 8), (1, 4), (3, 3)])
    },

    # ── 3J-J: Interval Statistics (Extrema with Multiplicity) (ST-37..ST-40) ──
    {
        "id": "ST-37",
        "category": "3J-J",
        "text": "Segment tree for interval statistics: min and max with multiplicity and point updates.",
        "pattern": "segment_tree_interval_statistics",
        "input": "5 4\n3 1 4 1 5\n2 1 5\n1 3 1\n2 1 5\n2 3 5",
        "runner": lambda: run_oracle_interval_statistics(5, [0, 3, 1, 4, 1, 5], [(2, 1, 5), (1, 3, 1), (2, 1, 5), (2, 3, 5)])
    },
    {
        "id": "ST-38",
        "category": "3J-J",
        "text": "Range extrema frequency: min and max with multiplicity using segment tree.",
        "pattern": "segment_tree_interval_statistics",
        "input": "6 3\n2 5 2 7 7 2\n2 1 6\n1 4 2\n2 1 6",
        "runner": lambda: run_oracle_interval_statistics(6, [0, 2, 5, 2, 7, 7, 2], [(2, 1, 6), (1, 4, 2), (2, 1, 6)])
    },
    {
        "id": "ST-39",
        "category": "3J-J",
        "text": "Frequency of minimum and maximum in range with point updates via segment tree.",
        "pattern": "segment_tree_interval_statistics",
        "input": "4 3\n5 5 5 5\n2 1 4\n1 2 1\n2 1 4",
        "runner": lambda: run_oracle_interval_statistics(4, [0, 5, 5, 5, 5], [(2, 1, 4), (1, 2, 1), (2, 1, 4)])
    },
    {
        "id": "ST-40",
        "category": "3J-J",
        "text": "Segment tree interval statistics with frequency of extrema.",
        "pattern": "segment_tree_interval_statistics",
        "input": "5 3\n1 2 3 2 1\n2 1 5\n1 3 1\n2 1 5",
        "runner": lambda: run_oracle_interval_statistics(5, [0, 1, 2, 3, 2, 1], [(2, 1, 5), (1, 3, 1), (2, 1, 5)])
    },

    # ── 3J-K: Linear-Time O(N) Tree Construction & Batch Initialization (ST-41..ST-44) ──
    {
        "id": "ST-41",
        "category": "3J-K",
        "text": "Segment tree linear build from initial array and range sum queries.",
        "pattern": "segment_tree_point_update_range_query",
        "input": "5 3\n10 20 30 40 50\n2 1 5\n2 2 4\n2 3 3",
        "runner": lambda: run_oracle_point_update_range_sum(5, [0, 10, 20, 30, 40, 50], [(2, 1, 5), (2, 2, 4), (2, 3, 3)])
    },
    {
        "id": "ST-42",
        "category": "3J-K",
        "text": "Build segment tree from sequence and perform range sum queries.",
        "pattern": "segment_tree_point_update_range_query",
        "input": "4 3\n1 1 1 1\n2 1 4\n1 2 5\n2 1 4",
        "runner": lambda: run_oracle_point_update_range_sum(4, [0, 1, 1, 1, 1], [(2, 1, 4), (1, 2, 5), (2, 1, 4)])
    },
    {
        "id": "ST-43",
        "category": "3J-K",
        "text": "Batch initialization of segment tree with range minimum queries.",
        "pattern": "segment_tree_point_update_range_query",
        "op": "min",
        "input": "5 3\n9 8 7 6 5\n2 1 5\n2 1 3\n2 3 5",
        "runner": lambda: run_oracle_point_update_range_min(5, [0, 9, 8, 7, 6, 5], [(2, 1, 5), (2, 1, 3), (2, 3, 5)])
    },
    {
        "id": "ST-44",
        "category": "3J-K",
        "text": "Initial array construction of segment tree with range maximum queries.",
        "pattern": "segment_tree_point_update_range_query",
        "op": "max",
        "input": "5 3\n3 1 4 1 5\n2 1 5\n1 4 9\n2 1 5",
        "runner": lambda: run_oracle_point_update_range_max(5, [0, 3, 1, 4, 1, 5], [(2, 1, 5), (1, 4, 9), (2, 1, 5)])
    },

    # ── 3J-L: Boundary Handling & Canonical Interval Decomposition (ST-45..ST-48) ──
    {
        "id": "ST-45",
        "category": "3J-L",
        "text": "Single element interval query and boundary point updates on segment tree.",
        "pattern": "segment_tree_point_update_range_query",
        "input": "5 4\n10 20 30 40 50\n2 1 1\n2 5 5\n1 5 100\n2 5 5",
        "runner": lambda: run_oracle_point_update_range_sum(5, [0, 10, 20, 30, 40, 50], [(2, 1, 1), (2, 5, 5), (1, 5, 100), (2, 5, 5)])
    },
    {
        "id": "ST-46",
        "category": "3J-L",
        "text": "Boundary queries at array edges using segment tree.",
        "pattern": "segment_tree_point_update_range_query",
        "input": "4 4\n5 6 7 8\n2 1 4\n1 1 10\n1 4 20\n2 1 4",
        "runner": lambda: run_oracle_point_update_range_sum(4, [0, 5, 6, 7, 8], [(2, 1, 4), (1, 1, 10), (1, 4, 20), (2, 1, 4)])
    },
    {
        "id": "ST-47",
        "category": "3J-L",
        "text": "Canonical interval decomposition verification on segment tree range query.",
        "pattern": "segment_tree_point_update_range_query",
        "input": "6 3\n1 2 3 4 5 6\n2 2 5\n2 3 4\n2 1 6",
        "runner": lambda: run_oracle_point_update_range_sum(6, [0, 1, 2, 3, 4, 5, 6], [(2, 2, 5), (2, 3, 4), (2, 1, 6)])
    },
    {
        "id": "ST-48",
        "category": "3J-L",
        "text": "Full array range query and edge point update with segment tree.",
        "pattern": "segment_tree_point_update_range_query",
        "input": "5 3\n2 4 6 8 10\n2 1 5\n1 3 0\n2 1 5",
        "runner": lambda: run_oracle_point_update_range_sum(5, [0, 2, 4, 6, 8, 10], [(2, 1, 5), (1, 3, 0), (2, 1, 5)])
    },

    # ── 3J-M: Non-Commutative Associative Merge Verification (ST-49..ST-52) ──
    {
        "id": "ST-49",
        "category": "3J-M",
        "text": "Segment tree maximum contiguous subarray sum with negative values.",
        "pattern": "segment_tree_max_subarray",
        "input": "5 3\n-2 -3 4 -1 -2\n2 1 5\n1 1 5\n2 1 5",
        "runner": lambda: run_oracle_max_subarray(5, [0, -2, -3, 4, -1, -2], [(2, 1, 5), (1, 1, 5), (2, 1, 5)])
    },
    {
        "id": "ST-50",
        "category": "3J-M",
        "text": "Maximum subarray sum queries on array with all negative numbers using segment tree.",
        "pattern": "segment_tree_max_subarray",
        "input": "4 3\n-10 -20 -30 -40\n2 1 4\n1 2 -5\n2 1 4",
        "runner": lambda: run_oracle_max_subarray(4, [0, -10, -20, -30, -40], [(2, 1, 4), (1, 2, -5), (2, 1, 4)])
    },
    {
        "id": "ST-51",
        "category": "3J-M",
        "text": "Associative non-commutative maximum contiguous subarray segment tree.",
        "pattern": "segment_tree_max_subarray",
        "input": "5 3\n1 2 -5 4 5\n2 1 5\n1 3 0\n2 1 5",
        "runner": lambda: run_oracle_max_subarray(5, [0, 1, 2, -5, 4, 5], [(2, 1, 5), (1, 3, 0), (2, 1, 5)])
    },
    {
        "id": "ST-52",
        "category": "3J-M",
        "text": "Max subarray sum queries on sequence with point updates.",
        "pattern": "segment_tree_max_subarray",
        "input": "6 3\n3 -2 5 -1 4 -6\n2 1 6\n1 2 10\n2 1 6",
        "runner": lambda: run_oracle_max_subarray(6, [0, 3, -2, 5, -1, 4, -6], [(2, 1, 6), (1, 2, 10), (2, 1, 6)])
    },

    # ── 3J-N: 64-bit Integer Overflow & Width Safety Policy (ST-53..ST-56) ──
    {
        "id": "ST-53",
        "category": "3J-N",
        "text": "Segment tree range sum queries with large 64-bit values and point updates.",
        "pattern": "segment_tree_point_update_range_query",
        "input": "4 3\n1000000000 1000000000 1000000000 1000000000\n2 1 4\n1 2 2000000000\n2 1 4",
        "runner": lambda: run_oracle_point_update_range_sum(4, [0, 1000000000, 1000000000, 1000000000, 1000000000], [(2, 1, 4), (1, 2, 2000000000), (2, 1, 4)])
    },
    {
        "id": "ST-54",
        "category": "3J-N",
        "text": "Lazy range add with large numbers avoiding 32-bit overflow using segment tree.",
        "pattern": "segment_tree_range_add_range_query",
        "input": "4 3\n1000000000 1000000000 1000000000 1000000000\n1 1 4 1000000000\n2 1 4\n2 2 3",
        "runner": lambda: run_oracle_range_add_sum(4, [0, 1000000000, 1000000000, 1000000000, 1000000000], [(1, 1, 4, 1000000000), (2, 1, 4), (2, 2, 3)])
    },
    {
        "id": "ST-55",
        "category": "3J-N",
        "text": "Segment tree range assignment with large values and 64-bit sum queries.",
        "pattern": "segment_tree_range_assign_range_query",
        "input": "5 3\n0 0 0 0 0\n1 1 5 1000000000\n2 1 5\n2 1 3",
        "runner": lambda: run_oracle_range_assign_sum(5, [0, 0, 0, 0, 0, 0], [(1, 1, 5, 1000000000), (2, 1, 5), (2, 1, 3)])
    },
    {
        "id": "ST-56",
        "category": "3J-N",
        "text": "Combined lazy segment tree with large 64-bit additions and assignments.",
        "pattern": "segment_tree_combined_lazy_range_query",
        "input": "4 4\n0 0 0 0\n2 1 4 1000000000\n1 1 4 500000000\n3 1 4\n3 1 2",
        "runner": lambda: run_oracle_combined_lazy(4, [0, 0, 0, 0, 0], [(2, 1, 4, 1000000000), (1, 1, 4, 500000000), (3, 1, 4), (3, 1, 2)])
    },

    # ── 3J-O: Anti-Pattern Elimination & Structural Incompatibility (ST-57..ST-60) ──
    {
        "id": "ST-57",
        "category": "3J-O",
        "text": "Static array with no updates: range minimum queries on fixed array.",
        "expected_rejection": "SEGMENT_TREE_STATIC_QUERY_SUBOPTIMAL",
    },
    {
        "id": "ST-58",
        "category": "3J-O",
        "text": "Point updates at index with prefix sum only queries on array.",
        "expected_rejection": "SEGMENT_TREE_SIMPLE_PREFIX_OVERKILL",
    },
    {
        "id": "ST-59",
        "category": "3J-O",
        "text": "Batch range adds where queries are only at the end with final reconstruction.",
        "expected_rejection": "SEGMENT_TREE_DIFFERENCE_ARRAY_OVERKILL",
    },
    {
        "id": "ST-60",
        "category": "3J-O",
        "text": "Dynamic median without rank tree requires non-associative interval query.",
        "expected_rejection": "SEGMENT_TREE_NO_ASSOCIATIVE_MERGE",
    },
]


def run_benchmark() -> Dict[str, Any]:
    print("=" * 70)
    print("CHUP Phase 3J — Segment Tree Benchmark (60 Problems)")
    print("=" * 70)

    total = len(BENCHMARK_PROBLEMS)
    passed = 0
    results = []

    for prob in BENCHMARK_PROBLEMS:
        pid = prob["id"]
        cat = prob["category"]
        text = prob["text"]

        res = handle_request({"problemText": text})

        if "expected_rejection" in prob:
            # Anti-pattern test
            exp_rej = prob["expected_rejection"]
            elim = res.get("eliminatedCandidates", [])
            has_rej = any(e.get("rejectionCode") == exp_rej for e in elim)
            if has_rej:
                passed += 1
                print(f"[{pid}] {cat}: PASS (Rejected with {exp_rej})")
                results.append((pid, cat, True, f"Rejected with {exp_rej}"))
            else:
                print(f"[{pid}] {cat}: FAIL (Expected rejection {exp_rej}, got {elim})")
                results.append((pid, cat, False, f"Expected {exp_rej}"))
            continue

        # Standard pattern test
        exp_pat = prob["pattern"]
        sel_pat = res.get("selectedPattern")

        if sel_pat != exp_pat:
            print(f"[{pid}] {cat}: FAIL (Pattern mismatch: expected {exp_pat}, got {sel_pat})")
            results.append((pid, cat, False, f"Pattern mismatch: {sel_pat}"))
            continue

        code = res.get("code", "")
        if not code or "COMPILE_ERROR" in code:
            print(f"[{pid}] {cat}: FAIL (No code generated)")
            results.append((pid, cat, False, "No code generated"))
            continue

        stdin_data = prob["input"]
        actual_out = compile_and_run_cpp(code, stdin_data, pattern=exp_pat)
        expected_out = prob["runner"]()

        if actual_out == expected_out:
            passed += 1
            print(f"[{pid}] {cat}: PASS")
            results.append((pid, cat, True, "Match"))
        else:
            print(f"[{pid}] {cat}: FAIL (Execution mismatch)")
            print(f"  Expected:\n{expected_out[:100]}")
            print(f"  Actual:\n{actual_out[:100]}")
            results.append((pid, cat, False, "Output mismatch"))

    rate = (passed / total) * 100
    print("-" * 70)
    print(f"Benchmark Results: {passed}/{total} passed ({rate:.1f}%)")
    print("-" * 70)

    return {
        "total": total,
        "passed": passed,
        "rate": rate,
        "results": results
    }


if __name__ == "__main__":
    res = run_benchmark()
    if res["passed"] < res["total"]:
        sys.exit(1)
