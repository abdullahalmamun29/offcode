"""
CHUP Phase 3I — Fenwick Tree / Binary Indexed Tree (BIT) Domain Benchmark.

Evaluates Fenwick Tree recognition, structural reasoning, invariant verification,
code generation, and execution across 15 categories (3I-A through 3I-O, 60 problems):

3I-A: Point Update & Prefix/Range Query (F-01..F-04)
3I-B: Range Update & Point Query (F-05..F-08)
3I-C: Range Update & Range Query (Two-Fenwick) (F-09..F-12)
3I-D: Dynamic Frequency Counting & CDF (F-13..F-16)
3I-E: Monotonic Prefix Minimum / Maximum (F-17..F-20)
3I-F: 2D Fenwick Grid & Rectangle Sums (F-21..F-24)
3I-G: K-th Element via Binary Lifting (F-25..F-28)
3I-H: Inversion Counting & Inversion Index (F-29..F-32)
3I-I: Dynamic Multiset Operations (F-33..F-36)
3I-J: Coordinate Compression & Sparse Indexing (F-37..F-40)
3I-K: Linear-Time O(N) Build & Batch Init (F-41..F-44)
3I-L: Boundary Handling & 0/1-Based Invariant Conversion (F-45..F-48)
3I-M: Invertible Group vs Monoid Monotonic Distinction (F-49..F-52)
3I-N: 2D Subgrid Inclusion-Exclusion (F-53..F-56)
3I-O: Competing Patterns & Anti-Pattern Elimination (F-57..F-60)
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
from pointer_algorithms.fenwick.verification.fenwick_oracles import (
    FenwickTreeOracle, RangeUpdatePointQueryBITOracle, RangeUpdateRangeQueryBITOracle,
    FrequencyBITOracle, PrefixExtremumBITOracle, Fenwick2DOracle,
    KthElementBITOracle, FenwickInversionOracle, FenwickMultisetOracle,
    CoordinateCompressorOracle
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

def run_oracle_point_update_prefix(n: int, a: List[int], queries: List[Tuple[int, ...]]) -> str:
    ft = FenwickTreeOracle(a)
    out = []
    for q in queries:
        if q[0] == 1:
            ft.add(q[1], q[2])
        elif q[0] == 2:
            out.append(str(ft.query(q[1])))
    return "\n".join(out)


def run_oracle_point_update_range(n: int, a: List[int], queries: List[Tuple[int, ...]]) -> str:
    ft = FenwickTreeOracle(a)
    out = []
    for q in queries:
        if q[0] == 1:
            ft.add(q[1], q[2])
        elif q[0] == 2:
            out.append(str(ft.range_query(q[1], q[2])))
    return "\n".join(out)


def run_oracle_range_update_point(n: int, a: List[int], queries: List[Tuple[int, ...]]) -> str:
    bit = RangeUpdatePointQueryBITOracle(n)
    prev = 0
    for i in range(1, n + 1):
        cur = a[i]
        bit._add(i, cur - prev)
        prev = cur
    out = []
    for q in queries:
        if q[0] == 1:
            bit.range_add(q[1], q[2], q[3])
        elif q[0] == 2:
            out.append(str(bit.point_query(q[1])))
    return "\n".join(out)


def run_oracle_range_update_range(n: int, a: List[int], queries: List[Tuple[int, ...]]) -> str:
    bit = RangeUpdateRangeQueryBITOracle(n)
    for i in range(1, n + 1):
        bit.range_add(i, i, a[i])
    out = []
    for q in queries:
        if q[0] == 1:
            bit.range_add(q[1], q[2], q[3])
        elif q[0] == 2:
            out.append(str(bit.range_query(q[1], q[2])))
    return "\n".join(out)


def run_oracle_frequency(m: int, queries: List[Tuple[int, ...]]) -> str:
    freq = FrequencyBITOracle(m)
    out = []
    for q in queries:
        if q[0] == 1:
            freq.insert(q[1], 1)
        elif q[0] == 2:
            freq.remove(q[1], 1)
        elif q[0] == 3:
            out.append(str(freq.count_range(q[1], q[2])))
    return "\n".join(out)


def run_oracle_prefix_extremum(n: int, is_min: bool, queries: List[Tuple[int, ...]]) -> str:
    bit = PrefixExtremumBITOracle(n, is_min)
    out = []
    for q in queries:
        if q[0] == 1:
            bit.update(q[1], q[2])
        elif q[0] == 2:
            out.append(str(bit.query_prefix(q[1])))
    return "\n".join(out)


def run_oracle_2d(n: int, m: int, queries: List[Tuple[int, ...]]) -> str:
    bit2d = Fenwick2DOracle(n, m)
    out = []
    for q in queries:
        if q[0] == 1:
            bit2d.add(q[1], q[2], q[3])
        elif q[0] == 2:
            out.append(str(bit2d.range_query(q[1], q[2], q[3], q[4])))
    return "\n".join(out)


def run_oracle_kth(m: int, queries: List[Tuple[int, ...]]) -> str:
    bit = KthElementBITOracle(m)
    out = []
    for q in queries:
        if q[0] == 1:
            bit.add(q[1], 1)
        elif q[0] == 2:
            bit.add(q[1], -1)
        elif q[0] == 3:
            out.append(str(bit.find_kth(q[1])))
    return "\n".join(out)


def run_oracle_multiset(m: int, queries: List[Tuple[int, ...]]) -> str:
    ms = FenwickMultisetOracle(m)
    out = []
    for q in queries:
        if q[0] == 1:
            ms.insert(q[1])
        elif q[0] == 2:
            ms.erase(q[1])
        elif q[0] == 3:
            out.append(str(ms.count(q[1])))
        elif q[0] == 4:
            out.append(str(ms.rank(q[1])))
        elif q[0] == 5:
            out.append(str(ms.select(q[1])))
    return "\n".join(out)


def run_oracle_coord_compression(queries: List[Tuple[int, ...]]) -> str:
    raw_coords = []
    for q in queries:
        if q[0] == 1:
            raw_coords.append(q[1])
        elif q[0] == 2:
            raw_coords.append(q[1])
            raw_coords.append(q[2])
    unique_sorted = sorted(set(raw_coords))
    rank_map = {x: i + 1 for i, x in enumerate(unique_sorted)}
    m = len(unique_sorted)
    ft = FenwickTreeOracle(m)
    out = []
    for q in queries:
        if q[0] == 1:
            r = rank_map[q[1]]
            ft.add(r, q[2])
        elif q[0] == 2:
            rl = rank_map[q[1]]
            rr = rank_map[q[2]]
            out.append(str(ft.range_query(rl, rr)))
    return "\n".join(out)


# ── 60 Benchmark Problems ──

BENCHMARK_PROBLEMS = [
    # ── 3I-A: Point Update & Prefix/Range Query (F-01..F-04) ──
    {
        "id": "F-01",
        "category": "3I-A. Point Update & Prefix/Range Query",
        "text": "Maintain an array subject to dynamic point update (add val to element at index) and range sum queries.",
        "expected_pattern": "fenwick_point_update_prefix_query",
        "input": "5 4\n1 2 3 4 5\n2 1 5\n1 3 10\n2 1 5\n2 2 4\n",
        "oracle_fn": lambda: run_oracle_point_update_range(5, [0, 1, 2, 3, 4, 5], [(2, 1, 5), (1, 3, 10), (2, 1, 5), (2, 2, 4)])
    },
    {
        "id": "F-02",
        "category": "3I-A. Point Update & Prefix/Range Query",
        "text": "Process a stream of point updates modifying individual elements and prefix query sum from 1 to i.",
        "expected_pattern": "fenwick_point_update_prefix_query",
        "input": "4 3\n0 0 0 0\n1 2 5\n1 4 3\n2 1 4\n",
        "oracle_fn": lambda: run_oracle_point_update_range(4, [0, 0, 0, 0, 0], [(1, 2, 5), (1, 4, 3), (2, 1, 4)])
    },
    {
        "id": "F-03",
        "category": "3I-A. Point Update & Prefix/Range Query",
        "text": "Binary indexed tree point increment and range sum evaluation over dynamic array.",
        "expected_pattern": "fenwick_point_update_prefix_query",
        "input": "6 3\n10 20 30 40 50 60\n2 2 5\n1 1 5\n2 1 3\n",
        "oracle_fn": lambda: run_oracle_point_update_range(6, [0, 10, 20, 30, 40, 50, 60], [(2, 2, 5), (1, 1, 5), (2, 1, 3)])
    },
    {
        "id": "F-04",
        "category": "3I-A. Point Update & Prefix/Range Query",
        "text": "Maintain cumulative prefix sums subject to single position increment and range sum queries.",
        "expected_pattern": "fenwick_point_update_prefix_query",
        "input": "5 3\n1 1 1 1 1\n1 3 4\n2 1 3\n2 3 5\n",
        "oracle_fn": lambda: run_oracle_point_update_range(5, [0, 1, 1, 1, 1, 1], [(1, 3, 4), (2, 1, 3), (2, 3, 5)])
    },

    # ── 3I-B: Range Update & Point Query (F-05..F-08) ──
    {
        "id": "F-05",
        "category": "3I-B. Range Update & Point Query",
        "text": "Maintain array with range update (add delta to range [l, r]) and point query value at index.",
        "expected_pattern": "fenwick_range_update_point_query",
        "input": "5 4\n10 20 30 40 50\n1 2 4 5\n2 3\n2 1\n2 5\n",
        "oracle_fn": lambda: run_oracle_range_update_point(5, [0, 10, 20, 30, 40, 50], [(1, 2, 4, 5), (2, 3), (2, 1), (2, 5)])
    },
    {
        "id": "F-06",
        "category": "3I-B. Range Update & Point Query",
        "text": "Apply range addition updates across intervals and answer single element point query.",
        "expected_pattern": "fenwick_range_update_point_query",
        "input": "4 3\n0 0 0 0\n1 1 3 10\n1 2 4 5\n2 2\n",
        "oracle_fn": lambda: run_oracle_range_update_point(4, [0, 0, 0, 0, 0], [(1, 1, 3, 10), (1, 2, 4, 5), (2, 2)])
    },
    {
        "id": "F-07",
        "category": "3I-B. Range Update & Point Query",
        "text": "Difference array Fenwick tree for interval additions and point value queries.",
        "expected_pattern": "fenwick_range_update_point_query",
        "input": "6 3\n5 5 5 5 5 5\n1 3 5 2\n2 4\n2 6\n",
        "oracle_fn": lambda: run_oracle_range_update_point(6, [0, 5, 5, 5, 5, 5, 5], [(1, 3, 5, 2), (2, 4), (2, 6)])
    },
    {
        "id": "F-08",
        "category": "3I-B. Range Update & Point Query",
        "text": "Support range increment on intervals and query element at position.",
        "expected_pattern": "fenwick_range_update_point_query",
        "input": "5 4\n1 2 3 4 5\n1 1 5 1\n2 1\n2 3\n2 5\n",
        "oracle_fn": lambda: run_oracle_range_update_point(5, [0, 1, 2, 3, 4, 5], [(1, 1, 5, 1), (2, 1), (2, 3), (2, 5)])
    },

    # ── 3I-C: Range Update & Range Query (Two-Fenwick) (F-09..F-12) ──
    {
        "id": "F-09",
        "category": "3I-C. Range Update & Range Query",
        "text": "Maintain an array supporting range update and range sum queries simultaneously.",
        "expected_pattern": "fenwick_range_update_range_query",
        "input": "5 4\n1 2 3 4 5\n2 1 5\n1 2 4 2\n2 1 5\n2 2 4\n",
        "oracle_fn": lambda: run_oracle_range_update_range(5, [0, 1, 2, 3, 4, 5], [(2, 1, 5), (1, 2, 4, 2), (2, 1, 5), (2, 2, 4)])
    },
    {
        "id": "F-10",
        "category": "3I-C. Range Update & Range Query",
        "text": "Two-Fenwick tree formulation for interval addition and range sum evaluation.",
        "expected_pattern": "fenwick_range_update_range_query",
        "input": "4 3\n0 0 0 0\n1 1 3 5\n1 2 4 10\n2 1 4\n",
        "oracle_fn": lambda: run_oracle_range_update_range(4, [0, 0, 0, 0, 0], [(1, 1, 3, 5), (1, 2, 4, 10), (2, 1, 4)])
    },
    {
        "id": "F-11",
        "category": "3I-C. Range Update & Range Query",
        "text": "Add delta to range [l, r] and compute range sum of elements in interval.",
        "expected_pattern": "fenwick_range_update_range_query",
        "input": "6 3\n10 10 10 10 10 10\n1 3 6 5\n2 1 6\n2 4 5\n",
        "oracle_fn": lambda: run_oracle_range_update_range(6, [0, 10, 10, 10, 10, 10, 10], [(1, 3, 6, 5), (2, 1, 6), (2, 4, 5)])
    },
    {
        "id": "F-12",
        "category": "3I-C. Range Update & Range Query",
        "text": "Range update and range query with double difference array maintaining prefix sums.",
        "expected_pattern": "fenwick_range_update_range_query",
        "input": "5 3\n2 4 6 8 10\n1 1 2 3\n2 1 3\n2 2 5\n",
        "oracle_fn": lambda: run_oracle_range_update_range(5, [0, 2, 4, 6, 8, 10], [(1, 1, 2, 3), (2, 1, 3), (2, 2, 5)])
    },

    # ── 3I-D: Dynamic Frequency Counting & CDF (F-13..F-16) ──
    {
        "id": "F-13",
        "category": "3I-D. Dynamic Frequency Counting",
        "text": "Frequency Fenwick table tracking dynamic occurrences of numbers and cumulative counts.",
        "expected_pattern": "fenwick_frequency",
        "input": "10 4\n1 3\n1 5\n1 3\n3 2 4\n",
        "oracle_fn": lambda: run_oracle_frequency(10, [(1, 3), (1, 5), (1, 3), (3, 2, 4)])
    },
    {
        "id": "F-14",
        "category": "3I-D. Dynamic Frequency Counting",
        "text": "Dynamic frequency table: insert value, remove value, and count elements in range [low, high].",
        "expected_pattern": "fenwick_frequency",
        "input": "20 5\n1 5\n1 10\n1 15\n2 10\n3 1 15\n",
        "oracle_fn": lambda: run_oracle_frequency(20, [(1, 5), (1, 10), (1, 15), (2, 10), (3, 1, 15)])
    },
    {
        "id": "F-15",
        "category": "3I-D. Dynamic Frequency Counting",
        "text": "Maintain count of elements <= x and rank of element in dynamic numerical stream.",
        "expected_pattern": "fenwick_frequency",
        "input": "15 4\n1 2\n1 4\n1 6\n3 1 5\n",
        "oracle_fn": lambda: run_oracle_frequency(15, [(1, 2), (1, 4), (1, 6), (3, 1, 5)])
    },
    {
        "id": "F-16",
        "category": "3I-D. Dynamic Frequency Counting",
        "text": "Cumulative frequency count of elements with dynamic insertions and frequency queries.",
        "expected_pattern": "fenwick_frequency",
        "input": "10 4\n1 1\n1 1\n1 2\n3 1 2\n",
        "oracle_fn": lambda: run_oracle_frequency(10, [(1, 1), (1, 1), (1, 2), (3, 1, 2)])
    },

    # ── 3I-E: Monotonic Prefix Minimum / Maximum (F-17..F-20) ──
    {
        "id": "F-17",
        "category": "3I-E. Monotonic Prefix Extremum",
        "text": "Maintain prefix minimum under non-increasing point updates (new val <= old val).",
        "expected_pattern": "fenwick_prefix_extremum",
        "input": "5 4\n1 3 10\n1 1 20\n2 3\n2 5\n",
        "oracle_fn": lambda: run_oracle_prefix_extremum(5, True, [(1, 3, 10), (1, 1, 20), (2, 3), (2, 5)])
    },
    {
        "id": "F-18",
        "category": "3I-E. Monotonic Prefix Extremum",
        "text": "Fenwick prefix min with monotonic updates where point update only decreases value.",
        "expected_pattern": "fenwick_prefix_extremum",
        "input": "6 4\n1 2 15\n1 4 8\n2 3\n2 5\n",
        "oracle_fn": lambda: run_oracle_prefix_extremum(6, True, [(1, 2, 15), (1, 4, 8), (2, 3), (2, 5)])
    },
    {
        "id": "F-19",
        "category": "3I-E. Monotonic Prefix Extremum",
        "text": "Prefix maximum under non-decreasing monotonic updates on array.",
        "expected_pattern": "fenwick_prefix_extremum",
        "input": "4 4\n1 2 5\n1 4 20\n2 3\n2 4\n",
        "oracle_fn": lambda: run_oracle_prefix_extremum(4, True, [(1, 2, 5), (1, 4, 20), (2, 3), (2, 4)])
    },
    {
        "id": "F-20",
        "category": "3I-E. Monotonic Prefix Extremum",
        "text": "Dynamic prefix minimum query under monotonically decreasing values.",
        "expected_pattern": "fenwick_prefix_extremum",
        "input": "5 3\n1 5 100\n1 2 50\n2 4\n",
        "oracle_fn": lambda: run_oracle_prefix_extremum(5, True, [(1, 5, 100), (1, 2, 50), (2, 4)])
    },

    # ── 3I-F: 2D Fenwick Grid & Rectangle Sums (F-21..F-24) ──
    {
        "id": "F-21",
        "category": "3I-F. 2D Fenwick Grid",
        "text": "2D Fenwick tree for matrix point update and 2D submatrix rectangle sum queries.",
        "expected_pattern": "fenwick_2d_point_update_range_query",
        "input": "4 4 4\n1 2 2 5\n1 3 3 10\n2 1 1 3 3\n2 2 2 4 4\n",
        "oracle_fn": lambda: run_oracle_2d(4, 4, [(1, 2, 2, 5), (1, 3, 3, 10), (2, 1, 1, 3, 3), (2, 2, 2, 4, 4)])
    },
    {
        "id": "F-22",
        "category": "3I-F. 2D Fenwick Grid",
        "text": "Matrix grid point update and submatrix sum query using 2D binary indexed tree.",
        "expected_pattern": "fenwick_2d_point_update_range_query",
        "input": "5 5 3\n1 1 1 3\n1 4 4 7\n2 1 1 5 5\n",
        "oracle_fn": lambda: run_oracle_2d(5, 5, [(1, 1, 1, 3), (1, 4, 4, 7), (2, 1, 1, 5, 5)])
    },
    {
        "id": "F-23",
        "category": "3I-F. 2D Fenwick Grid",
        "text": "Dynamic 2D range sum and cell update on 2D grid via inclusion-exclusion.",
        "expected_pattern": "fenwick_2d_point_update_range_query",
        "input": "3 3 4\n1 1 2 4\n1 2 1 6\n2 1 1 2 2\n2 2 2 3 3\n",
        "oracle_fn": lambda: run_oracle_2d(3, 3, [(1, 1, 2, 4), (1, 2, 1, 6), (2, 1, 1, 2, 2), (2, 2, 2, 3, 3)])
    },
    {
        "id": "F-24",
        "category": "3I-F. 2D Fenwick Grid",
        "text": "2D BIT for rectangle sum queries and cell additions on 2D coordinate grid.",
        "expected_pattern": "fenwick_2d_point_update_range_query",
        "input": "4 3 3\n1 2 2 8\n1 4 1 2\n2 2 1 4 3\n",
        "oracle_fn": lambda: run_oracle_2d(4, 3, [(1, 2, 2, 8), (1, 4, 1, 2), (2, 2, 1, 4, 3)])
    },

    # ── 3I-G: K-th Element via Binary Lifting (F-25..F-28) ──
    {
        "id": "F-25",
        "category": "3I-G. K-th Element via Binary Lifting",
        "text": "Find k-th smallest element dynamically using binary lifting on Fenwick tree frequencies.",
        "expected_pattern": "fenwick_kth_element",
        "input": "10 5\n1 3\n1 5\n1 1\n3 2\n3 3\n",
        "oracle_fn": lambda: run_oracle_kth(10, [(1, 3), (1, 5), (1, 1), (3, 2), (3, 3)])
    },
    {
        "id": "F-26",
        "category": "3I-G. K-th Element via Binary Lifting",
        "text": "Maintain elements and answer k-th element quantile query in single pass O(log M).",
        "expected_pattern": "fenwick_kth_element",
        "input": "16 5\n1 4\n1 8\n1 12\n3 1\n3 2\n",
        "oracle_fn": lambda: run_oracle_kth(16, [(1, 4), (1, 8), (1, 12), (3, 1), (3, 2)])
    },
    {
        "id": "F-27",
        "category": "3I-G. K-th Element via Binary Lifting",
        "text": "Find k-th order statistic with element insertions and removals via Fenwick binary lifting.",
        "expected_pattern": "fenwick_kth_element",
        "input": "8 5\n1 2\n1 6\n1 4\n2 2\n3 2\n",
        "oracle_fn": lambda: run_oracle_kth(8, [(1, 2), (1, 6), (1, 4), (2, 2), (3, 2)])
    },
    {
        "id": "F-28",
        "category": "3I-G. K-th Element via Binary Lifting",
        "text": "Binary lifting on BIT frequency array to locate k-th smallest active element.",
        "expected_pattern": "fenwick_kth_element",
        "input": "12 4\n1 7\n1 3\n1 10\n3 2\n",
        "oracle_fn": lambda: run_oracle_kth(12, [(1, 7), (1, 3), (1, 10), (3, 2)])
    },

    # ── 3I-H: Inversion Counting & Inversion Index (F-29..F-32) ──
    {
        "id": "F-29",
        "category": "3I-H. Inversion Counting",
        "text": "Count inversions: number of pairs (i, j) with i < j and a[i] > a[j] using Fenwick tree.",
        "expected_pattern": "fenwick_inversion_counting",
        "input": "5\n2 4 1 3 5\n",
        "oracle_fn": lambda: str(FenwickInversionOracle.count_inversions([2, 4, 1, 3, 5]))
    },
    {
        "id": "F-30",
        "category": "3I-H. Inversion Counting",
        "text": "Compute total number of inversions in array using BIT with coordinate compression.",
        "expected_pattern": "fenwick_inversion_counting",
        "input": "6\n6 5 4 3 2 1\n",
        "oracle_fn": lambda: str(FenwickInversionOracle.count_inversions([6, 5, 4, 3, 2, 1]))
    },
    {
        "id": "F-31",
        "category": "3I-H. Inversion Counting",
        "text": "Inversion count for already sorted array of integers.",
        "expected_pattern": "fenwick_inversion_counting",
        "input": "5\n1 2 3 4 5\n",
        "oracle_fn": lambda: str(FenwickInversionOracle.count_inversions([1, 2, 3, 4, 5]))
    },
    {
        "id": "F-32",
        "category": "3I-H. Inversion Counting",
        "text": "Count elements greater than a[i] to the left for all elements in array.",
        "expected_pattern": "fenwick_inversion_counting",
        "input": "4\n8 4 2 1\n",
        "oracle_fn": lambda: str(FenwickInversionOracle.count_inversions([8, 4, 2, 1]))
    },

    # ── 3I-I: Dynamic Multiset Operations (F-33..F-36) ──
    {
        "id": "F-33",
        "category": "3I-I. Dynamic Multiset",
        "text": "Dynamic multiset with insert, delete, rank, and k-th smallest element query.",
        "expected_pattern": "fenwick_multiset",
        "input": "10 6\n1 5\n1 2\n1 8\n4 5\n5 2\n3 5\n",
        "oracle_fn": lambda: run_oracle_multiset(10, [(1, 5), (1, 2), (1, 8), (4, 5), (5, 2), (3, 5)])
    },
    {
        "id": "F-34",
        "category": "3I-I. Dynamic Multiset",
        "text": "Order-statistic multiset supporting rank of element and k-th selection via Fenwick tree.",
        "expected_pattern": "fenwick_multiset",
        "input": "15 5\n1 10\n1 10\n1 3\n3 10\n4 10\n",
        "oracle_fn": lambda: run_oracle_multiset(15, [(1, 10), (1, 10), (1, 3), (3, 10), (4, 10)])
    },
    {
        "id": "F-35",
        "category": "3I-I. Dynamic Multiset",
        "text": "Multiset with k-th element retrieval, element counting, and element deletion.",
        "expected_pattern": "fenwick_multiset",
        "input": "20 5\n1 7\n1 14\n2 7\n3 7\n5 1\n",
        "oracle_fn": lambda: run_oracle_multiset(20, [(1, 7), (1, 14), (2, 7), (3, 7), (5, 1)])
    },
    {
        "id": "F-36",
        "category": "3I-I. Dynamic Multiset",
        "text": "Dynamic collection maintaining multiplicity, 1-based rank, and quantile select.",
        "expected_pattern": "fenwick_multiset",
        "input": "12 4\n1 4\n1 9\n4 9\n5 1\n",
        "oracle_fn": lambda: run_oracle_multiset(12, [(1, 4), (1, 9), (4, 9), (5, 1)])
    },

    # ── 3I-J: Coordinate Compression & Sparse Indexing (F-37..F-40) ──
    {
        "id": "F-37",
        "category": "3I-J. Coordinate Compression",
        "text": "Fenwick tree with coordinate compression for coordinates up to 10^9 and point add.",
        "expected_pattern": "fenwick_coordinate_compression",
        "input": "4\n1 1000000000 5\n1 500000000 10\n2 1 1000000000\n2 600000000 1000000000\n",
        "oracle_fn": lambda: run_oracle_coord_compression([(1, 1000000000, 5), (1, 500000000, 10), (2, 1, 1000000000), (2, 600000000, 1000000000)])
    },
    {
        "id": "F-38",
        "category": "3I-J. Coordinate Compression",
        "text": "Sparse coordinates up to 10^9 mapped via rank compression for range sum queries.",
        "expected_pattern": "fenwick_coordinate_compression",
        "input": "3\n1 999999999 15\n1 123456789 25\n2 100000000 1000000000\n",
        "oracle_fn": lambda: run_oracle_coord_compression([(1, 999999999, 15), (1, 123456789, 25), (2, 100000000, 1000000000)])
    },
    {
        "id": "F-39",
        "category": "3I-J. Coordinate Compression",
        "text": "Compress coordinates for dynamic range queries over unbounded integer keys.",
        "expected_pattern": "fenwick_coordinate_compression",
        "input": "4\n1 50 1\n1 200 2\n1 1000 3\n2 1 500\n",
        "oracle_fn": lambda: run_oracle_coord_compression([(1, 50, 1), (1, 200, 2), (1, 1000, 3), (2, 1, 500)])
    },
    {
        "id": "F-40",
        "category": "3I-J. Coordinate Compression",
        "text": "Relative ranking of values via coordinate compression for Fenwick tree range aggregation.",
        "expected_pattern": "fenwick_coordinate_compression",
        "input": "3\n1 1000000 4\n1 2000000 6\n2 1 3000000\n",
        "oracle_fn": lambda: run_oracle_coord_compression([(1, 1000000, 4), (1, 2000000, 6), (2, 1, 3000000)])
    },

    # ── 3I-K: Linear-Time O(N) Build & Batch Init (F-41..F-44) ──
    {
        "id": "F-41",
        "category": "3I-K. Linear-Time Build",
        "text": "Initialize Fenwick tree in linear O(N) time from given array and process point updates.",
        "expected_pattern": "fenwick_point_update_prefix_query",
        "input": "5 2\n5 4 3 2 1\n2 1 5\n1 2 10\n",
        "oracle_fn": lambda: run_oracle_point_update_range(5, [0, 5, 4, 3, 2, 1], [(2, 1, 5), (1, 2, 10)])
    },
    {
        "id": "F-42",
        "category": "3I-K. Linear-Time Build",
        "text": "Construct binary indexed tree in O(N) and answer range sum queries.",
        "expected_pattern": "fenwick_point_update_prefix_query",
        "input": "4 1\n10 20 30 40\n2 2 4\n",
        "oracle_fn": lambda: run_oracle_point_update_range(4, [0, 10, 20, 30, 40], [(2, 2, 4)])
    },
    {
        "id": "F-43",
        "category": "3I-K. Linear-Time Build",
        "text": "Batch initialize Fenwick array and evaluate point update and prefix sums.",
        "expected_pattern": "fenwick_point_update_prefix_query",
        "input": "6 2\n1 1 1 1 1 1\n1 6 5\n2 1 6\n",
        "oracle_fn": lambda: run_oracle_point_update_range(6, [0, 1, 1, 1, 1, 1, 1], [(1, 6, 5), (2, 1, 6)])
    },
    {
        "id": "F-44",
        "category": "3I-K. Linear-Time Build",
        "text": "Linear build of Fenwick tree with point update at index and range sum in interval.",
        "expected_pattern": "fenwick_point_update_prefix_query",
        "input": "3 1\n7 8 9\n2 1 3\n",
        "oracle_fn": lambda: run_oracle_point_update_range(3, [0, 7, 8, 9], [(2, 1, 3)])
    },

    # ── 3I-L: Boundary Handling & Index Conversion (F-45..F-48) ──
    {
        "id": "F-45",
        "category": "3I-L. Boundary Handling",
        "text": "Fenwick range sum query at single element boundary [x, x] with point updates.",
        "expected_pattern": "fenwick_point_update_prefix_query",
        "input": "5 2\n1 2 3 4 5\n2 3 3\n1 3 10\n",
        "oracle_fn": lambda: run_oracle_point_update_range(5, [0, 1, 2, 3, 4, 5], [(2, 3, 3), (1, 3, 10)])
    },
    {
        "id": "F-46",
        "category": "3I-L. Boundary Handling",
        "text": "Point increment at boundary index 1 and query range sum [1, 1].",
        "expected_pattern": "fenwick_point_update_prefix_query",
        "input": "4 2\n1 1 1 1\n1 1 10\n2 1 1\n",
        "oracle_fn": lambda: run_oracle_point_update_range(4, [0, 1, 1, 1, 1], [(1, 1, 10), (2, 1, 1)])
    },
    {
        "id": "F-47",
        "category": "3I-L. Boundary Handling",
        "text": "Point update at maximum boundary index N and evaluate range sum [N, N].",
        "expected_pattern": "fenwick_point_update_prefix_query",
        "input": "5 2\n0 0 0 0 0\n1 5 100\n2 5 5\n",
        "oracle_fn": lambda: run_oracle_point_update_range(5, [0, 0, 0, 0, 0, 0], [(1, 5, 100), (2, 5, 5)])
    },
    {
        "id": "F-48",
        "category": "3I-L. Boundary Handling",
        "text": "Difference array Fenwick range update covering full range [1, N] and point query.",
        "expected_pattern": "fenwick_range_update_point_query",
        "input": "4 2\n2 2 2 2\n1 1 4 5\n2 3\n",
        "oracle_fn": lambda: run_oracle_range_update_point(4, [0, 2, 2, 2, 2], [(1, 1, 4, 5), (2, 3)])
    },

    # ── 3I-M: Invertible Group vs Monoid Monotonic Distinction (F-49..F-52) ──
    {
        "id": "F-49",
        "category": "3I-M. Invertible vs Monoid Monotonic",
        "text": "Prefix minimum query with point update decreasing value monotonically.",
        "expected_pattern": "fenwick_prefix_extremum",
        "input": "5 3\n1 2 8\n1 4 3\n2 5\n",
        "oracle_fn": lambda: run_oracle_prefix_extremum(5, True, [(1, 2, 8), (1, 4, 3), (2, 5)])
    },
    {
        "id": "F-50",
        "category": "3I-M. Invertible vs Monoid Monotonic",
        "text": "Prefix maximum query with non-decreasing monotonic point modifications.",
        "expected_pattern": "fenwick_prefix_extremum",
        "input": "5 3\n1 1 10\n1 3 50\n2 4\n",
        "oracle_fn": lambda: run_oracle_prefix_extremum(5, True, [(1, 1, 10), (1, 3, 50), (2, 4)])
    },
    {
        "id": "F-51",
        "category": "3I-M. Invertible vs Monoid Monotonic",
        "text": "Additive group invertible range sum queries with dynamic point updates.",
        "expected_pattern": "fenwick_point_update_prefix_query",
        "input": "4 2\n10 20 30 40\n1 2 -5\n2 1 3\n",
        "oracle_fn": lambda: run_oracle_point_update_range(4, [0, 10, 20, 30, 40], [(1, 2, -5), (2, 1, 3)])
    },
    {
        "id": "F-52",
        "category": "3I-M. Invertible vs Monoid Monotonic",
        "text": "Point addition with negative delta on group sum Fenwick tree and range query.",
        "expected_pattern": "fenwick_point_update_prefix_query",
        "input": "5 2\n1 2 3 4 5\n1 4 -10\n2 3 5\n",
        "oracle_fn": lambda: run_oracle_point_update_range(5, [0, 1, 2, 3, 4, 5], [(1, 4, -10), (2, 3, 5)])
    },

    # ── 3I-N: 2D Subgrid Inclusion-Exclusion (F-53..F-56) ──
    {
        "id": "F-53",
        "category": "3I-N. 2D Subgrid Inclusion-Exclusion",
        "text": "2D matrix point update and rectangular subgrid sum via 2D BIT inclusion-exclusion.",
        "expected_pattern": "fenwick_2d_point_update_range_query",
        "input": "3 3 3\n1 1 1 5\n1 3 3 10\n2 1 1 3 3\n",
        "oracle_fn": lambda: run_oracle_2d(3, 3, [(1, 1, 1, 5), (1, 3, 3, 10), (2, 1, 1, 3, 3)])
    },
    {
        "id": "F-54",
        "category": "3I-N. 2D Subgrid Inclusion-Exclusion",
        "text": "Submatrix sum on 2D grid with dynamic cell increment operations.",
        "expected_pattern": "fenwick_2d_point_update_range_query",
        "input": "4 4 3\n1 2 3 15\n1 3 2 25\n2 2 2 3 3\n",
        "oracle_fn": lambda: run_oracle_2d(4, 4, [(1, 2, 3, 15), (1, 3, 2, 25), (2, 2, 2, 3, 3)])
    },
    {
        "id": "F-55",
        "category": "3I-N. 2D Subgrid Inclusion-Exclusion",
        "text": "Evaluate submatrix queries using 2D binary indexed tree with point updates.",
        "expected_pattern": "fenwick_2d_point_update_range_query",
        "input": "5 4 3\n1 5 4 100\n1 1 1 50\n2 1 1 5 4\n",
        "oracle_fn": lambda: run_oracle_2d(5, 4, [(1, 5, 4, 100), (1, 1, 1, 50), (2, 1, 1, 5, 4)])
    },
    {
        "id": "F-56",
        "category": "3I-N. 2D Subgrid Inclusion-Exclusion",
        "text": "2D rectangle sum on grid subject to cell point modifications.",
        "expected_pattern": "fenwick_2d_point_update_range_query",
        "input": "3 4 3\n1 2 2 4\n1 2 3 6\n2 2 2 2 3\n",
        "oracle_fn": lambda: run_oracle_2d(3, 4, [(1, 2, 2, 4), (1, 2, 3, 6), (2, 2, 2, 2, 3)])
    },

    # ── 3I-O: Competing Patterns & Anti-Pattern Elimination (F-57..F-60) ──
    {
        "id": "F-57",
        "category": "3I-O. Anti-Patterns & Elimination",
        "text": "Static array with no updates: compute static range sum queries repeatedly on immutable sequence.",
        "anti_pattern_test": True,
        "rejected_pattern": "fenwick_point_update_prefix_query",
        "expected_rejection_code": "FENWICK_STATIC_QUERY_SUBOPTIMAL"
    },
    {
        "id": "F-58",
        "category": "3I-O. Anti-Patterns & Elimination",
        "text": "Batch range adds offline where all queries are only after all updates finish.",
        "anti_pattern_test": True,
        "rejected_pattern": "fenwick_point_update_prefix_query",
        "expected_rejection_code": "FENWICK_OFFLINE_RANGE_ADD_OVERKILL"
    },
    {
        "id": "F-59",
        "category": "3I-O. Anti-Patterns & Elimination",
        "text": "Arbitrary range query requiring subtraction and inversion for non-invertible range gcd without inverse.",
        "anti_pattern_test": True,
        "rejected_pattern": "fenwick_point_update_prefix_query",
        "expected_rejection_code": "FENWICK_STRUCTURAL_INCOMPATIBILITY"
    },
    {
        "id": "F-60",
        "category": "3I-O. Anti-Patterns & Elimination",
        "text": "Allow negative counts for k-th element search with negative frequency updates.",
        "anti_pattern_test": True,
        "rejected_pattern": "fenwick_kth_element",
        "expected_rejection_code": "FENWICK_KTH_NEGATIVE_FREQUENCY"
    }
]


def run_benchmark() -> bool:
    print("=" * 70)
    print("CHUP Phase 3I — Fenwick Tree Benchmark Suite (F-01 through F-60)")
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
    print(f"Fenwick Benchmark Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 70)
    return passed == total


if __name__ == "__main__":
    success = run_benchmark()
    sys.exit(0 if success else 1)
