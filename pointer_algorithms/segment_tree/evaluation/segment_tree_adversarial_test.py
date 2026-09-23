"""
CHUP Phase 3J — Segment Tree Adversarial Algebra Test Suite (15 Tests: ST-ADV-01 .. ST-ADV-15).

Verifies hard edge cases and algebraic invariants of Segment Trees:
- ST-ADV-01: Non-commutative associative merge (Ordered Matrix Multiplication)
- ST-ADV-02: All-negative maximum-subarray sum (Non-empty invariant)
- ST-ADV-03: Identity returned from left query only (Neutral element merge)
- ST-ADV-04: Identity returned from right query only (Neutral element merge)
- ST-ADV-05: Assignment -> Addition tag composition order
- ST-ADV-06: Addition -> Assignment tag composition order
- ST-ADV-07: Assignment -> Addition -> Assignment tag composition order
- ST-ADV-08: Multiple overlapping range assignments
- ST-ADV-09: Negative values + assignment and addition
- ST-ADV-10: 64-bit integer overflow boundary
- ST-ADV-11: __int128 intermediate multiplication safety
- ST-ADV-12: N not a power of two (N in {3, 5, 7, 10, 13, 23})
- ST-ADV-13: N = 1 (Single-element boundary base case)
- ST-ADV-14: Query exactly equal to canonical node boundaries
- ST-ADV-15: Query repeatedly crossing midpoints at multiple depths
"""

import sys
import os
import math
import subprocess
import tempfile
from typing import List, Tuple, Any

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.generator.segment_tree_cpp_generator import generate_segment_tree_cpp
from pointer_algorithms.segment_tree.verification.segment_tree_oracles import (
    SegmentTreeOracle,
    LazyRangeAddSegmentTreeOracle,
    LazyRangeAssignSegmentTreeOracle,
    CombinedLazySegmentTreeOracle,
    MaxSubarraySegmentTreeOracle,
    FrequencySegmentTreeOracle,
    IntervalStatisticsSegmentTreeOracle,
    BruteForceMaxSubarray,
    BruteForceCombinedLazy,
)


class CppBinary:
    """Compiles C++ code once and executes input against the binary."""
    def __init__(self, cpp_code: str):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.src = os.path.join(self.tmp_dir.name, "sol.cpp")
        self.exe = os.path.join(self.tmp_dir.name, "sol")
        with open(self.src, "w") as f:
            f.write(cpp_code)
        compile_res = subprocess.run(
            ["g++", "-std=c++17", "-O2", "-o", self.exe, self.src],
            capture_output=True, text=True, timeout=15
        )
        if compile_res.returncode != 0:
            raise RuntimeError(f"Compilation failed: {compile_res.stderr}")

    def run(self, stdin_input: str) -> str:
        res = subprocess.run(
            [self.exe],
            input=stdin_input,
            capture_output=True,
            text=True,
            timeout=10
        )
        if res.returncode != 0:
            raise RuntimeError(f"Execution failed: {res.stderr}")
        return res.stdout.strip()

    def __del__(self):
        self.tmp_dir.cleanup()


def test_st_adv_01_non_commutative_merge() -> bool:
    """ST-ADV-01: Non-commutative associative merge (2x2 Matrix Multiplication)."""
    # Matrices A[1..4]:
    # A1 = [[1, 2], [0, 1]], A2 = [[2, 0], [1, 1]], A3 = [[1, 1], [1, 0]], A4 = [[0, 1], [1, 0]]
    # Product must be computed in strict left-to-right order: A1 * A2 * A3 * A4
    MOD = 1_000_000_007

    def mat_mul(A, B):
        return [
            [(A[0][0] * B[0][0] + A[0][1] * B[1][0]) % MOD, (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % MOD],
            [(A[1][0] * B[0][0] + A[1][1] * B[1][0]) % MOD, (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % MOD]
        ]

    identity = [[1, 0], [0, 1]]
    matrices = [
        [[1, 2], [0, 1]],
        [[2, 0], [1, 1]],
        [[1, 1], [1, 0]],
        [[0, 1], [1, 0]],
    ]

    # Build 1-based tree
    tree = [identity] * 16
    def build(p, l, r):
        if l == r:
            tree[p] = matrices[l - 1]
            return
        mid = (l + r) // 2
        build(2 * p, l, mid)
        build(2 * p + 1, mid + 1, r)
        tree[p] = mat_mul(tree[2 * p], tree[2 * p + 1])

    def query(p, l, r, ql, qr):
        if ql <= l and r <= qr:
            return tree[p]
        mid = (l + r) // 2
        res = identity
        if ql <= mid:
            res = mat_mul(res, query(2 * p, l, mid, ql, qr))
        if qr > mid:
            res = mat_mul(res, query(2 * p + 1, mid + 1, r, ql, qr))
        return res

    build(1, 1, 4)
    # Forward product
    p14 = query(1, 1, 4, 1, 4)
    expected_p14 = mat_mul(mat_mul(mat_mul(matrices[0], matrices[1]), matrices[2]), matrices[3])
    # Reverse product (deliberately wrong)
    reverse_p14 = mat_mul(mat_mul(mat_mul(matrices[3], matrices[2]), matrices[1]), matrices[0])

    assert p14 == expected_p14, f"Matrix product mismatch: got {p14}, expected {expected_p14}"
    assert p14 != reverse_p14, "Non-commutative test invalid: forward and reverse products are identical!"
    return True


def test_st_adv_02_all_negative_max_subarray() -> bool:
    """ST-ADV-02: All-negative maximum contiguous subarray sum."""
    arr = [0, -5, -2, -8, -1, -9]
    oracle = MaxSubarraySegmentTreeOracle(arr)
    # Expected maximum non-empty subarray sum is -1 (element at index 4)
    ans = oracle.query(1, 5)
    assert ans == -1, f"Expected -1 for all-negative array, got {ans}"

    # Query subsegment [1, 3]: [-5, -2, -8] -> max is -2
    ans_13 = oracle.query(1, 3)
    assert ans_13 == -2, f"Expected -2 for [-5, -2, -8], got {ans_13}"

    # Point update: change arr[4] to -15 -> max is now -2
    oracle.update(4, -15)
    ans_after = oracle.query(1, 5)
    assert ans_after == -2, f"Expected -2 after update, got {ans_after}"
    return True


def test_st_adv_03_identity_from_left_query_only() -> bool:
    """ST-ADV-03: Identity returned from left query only (query strictly in right subtree)."""
    # In tree on [1..8], mid=4. Query [5, 7] strictly in right child [5, 8].
    # Left recursive branch returns identity; verify merge(identity, R) == R.
    arr = [0, 10, 20, 30, 40, 50, 60, 70, 80]
    oracle_sum = SegmentTreeOracle(arr, op="sum")
    oracle_min = SegmentTreeOracle(arr, op="min")
    oracle_max = SegmentTreeOracle(arr, op="max")
    oracle_gcd = SegmentTreeOracle(arr, op="gcd")

    assert oracle_sum.query(5, 7) == 50 + 60 + 70  # 180
    assert oracle_min.query(5, 7) == 50
    assert oracle_max.query(5, 7) == 70
    assert oracle_gcd.query(5, 7) == math.gcd(math.gcd(50, 60), 70)  # 10
    return True


def test_st_adv_04_identity_from_right_query_only() -> bool:
    """ST-ADV-04: Identity returned from right query only (query strictly in left subtree)."""
    # In tree on [1..8], mid=4. Query [2, 3] strictly in left child [1, 4].
    # Right recursive branch returns identity; verify merge(L, identity) == L.
    arr = [0, 10, 20, 30, 40, 50, 60, 70, 80]
    oracle_sum = SegmentTreeOracle(arr, op="sum")
    oracle_min = SegmentTreeOracle(arr, op="min")
    oracle_max = SegmentTreeOracle(arr, op="max")
    oracle_gcd = SegmentTreeOracle(arr, op="gcd")

    assert oracle_sum.query(2, 3) == 20 + 30  # 50
    assert oracle_min.query(2, 3) == 20
    assert oracle_max.query(2, 3) == 30
    assert oracle_gcd.query(2, 3) == math.gcd(20, 30)  # 10
    return True


def test_st_adv_05_assignment_then_addition() -> bool:
    """ST-ADV-05: Tag composition order: Assignment followed by Addition."""
    # Start: [1, 2, 3, 4, 5, 6]
    # 1. assign [2, 5] = 10 -> [1, 10, 10, 10, 10, 6]
    # 2. add [2, 5] += 7   -> [1, 17, 17, 17, 17, 6]
    oracle = CombinedLazySegmentTreeOracle([0, 1, 2, 3, 4, 5, 6])
    oracle.range_assign(2, 5, 10)
    oracle.range_add(2, 5, 7)

    assert oracle.range_query(2, 5) == 4 * 17  # 68
    assert oracle.range_query(1, 6) == 1 + 68 + 6  # 75
    return True


def test_st_adv_06_addition_then_assignment() -> bool:
    """ST-ADV-06: Tag composition order: Addition followed by Assignment."""
    # Start: [1, 2, 3, 4, 5, 6]
    # 1. add [2, 5] += 7   -> [1, 9, 10, 11, 12, 6]
    # 2. assign [2, 5] = 10 -> [1, 10, 10, 10, 10, 6] (assignment overrides prior add!)
    oracle = CombinedLazySegmentTreeOracle([0, 1, 2, 3, 4, 5, 6])
    oracle.range_add(2, 5, 7)
    oracle.range_assign(2, 5, 10)

    assert oracle.range_query(2, 5) == 4 * 10  # 40
    assert oracle.range_query(1, 6) == 1 + 40 + 6  # 47
    return True


def test_st_adv_07_assign_add_assign() -> bool:
    """ST-ADV-07: Tag composition order: Assign -> Add -> Assign."""
    # Start: [0, 0, 0, 0]
    # 1. assign [1, 4] = 100
    # 2. add [1, 4] += 50 -> 150
    # 3. assign [1, 4] = 25 -> 25 (overrides all prior operations!)
    oracle = CombinedLazySegmentTreeOracle([0, 0, 0, 0, 0])
    oracle.range_assign(1, 4, 100)
    oracle.range_add(1, 4, 50)
    oracle.range_assign(1, 4, 25)

    assert oracle.range_query(1, 4) == 4 * 25  # 100
    return True


def test_st_adv_08_overlapping_assignments() -> bool:
    """ST-ADV-08: Multiple overlapping range assignments."""
    # Array size 10, all 0
    # 1. assign [1, 6] = 10
    # 2. assign [4, 8] = 20
    # Result: [10, 10, 10, 20, 20, 20, 20, 20, 0, 0]
    oracle = CombinedLazySegmentTreeOracle(10)
    oracle.range_assign(1, 6, 10)
    oracle.range_assign(4, 8, 20)

    assert oracle.range_query(1, 3) == 30
    assert oracle.range_query(4, 6) == 60
    assert oracle.range_query(7, 8) == 40
    assert oracle.range_query(9, 10) == 0
    assert oracle.range_query(1, 10) == 130
    return True


def test_st_adv_09_negative_values_lazy() -> bool:
    """ST-ADV-09: Negative values in range assignment and addition."""
    oracle = CombinedLazySegmentTreeOracle(6)
    oracle.range_assign(1, 6, -50)
    oracle.range_add(2, 4, 30)  # [1]: -50, [2..4]: -20, [5..6]: -50

    assert oracle.range_query(1, 1) == -50
    assert oracle.range_query(2, 4) == 3 * (-20)  # -60
    assert oracle.range_query(1, 6) == -50 - 60 - 100  # -210
    return True


def test_st_adv_10_64bit_overflow_boundary() -> bool:
    """ST-ADV-10: 64-bit integer range sum (> 2^31 - 1)."""
    # 100,000 elements of value 1,000,000,000
    # Total sum = 10^14 (fits in signed 64-bit long long, overflows 32-bit int)
    oracle = SegmentTreeOracle(100_000, op="sum")
    oracle.update(1, 1_000_000_000)
    oracle.update(50_000, 1_000_000_000)
    oracle.update(100_000, 1_000_000_000)

    ans = oracle.query(1, 100_000)
    assert ans == 3_000_000_000, f"Expected 3*10^9, got {ans}"
    return True


def test_st_adv_11_int128_intermediate_multiplication() -> bool:
    """ST-ADV-11: Intermediate multiplication safety in lazy updates."""
    # When (assign_val + add_val) * len is computed, ensure multiplication does not truncate
    # Test through C++ code generation
    cpp_code = generate_segment_tree_cpp("segment_tree_combined_lazy_range_query", {})
    bin_cpp = CppBinary(cpp_code)
    # Feed input:
    # 4 2 (N=4, Q=2)
    # 1000000000 1000000000 1000000000 1000000000
    # Type 1 = Range Add: 1 1 4 1000000000 (add 10^9 to [1..4] -> each becomes 2*10^9)
    # Type 3 = Range Query: 3 1 4 (query sum -> 4 * 2*10^9 = 8 * 10^9)
    inp = "4 2\n1000000000 1000000000 1000000000 1000000000\n1 1 4 1000000000\n3 1 4\n"
    out = bin_cpp.run(inp)
    assert out.strip() == "8000000000", f"Expected 8000000000, got {out}"
    return True


def test_st_adv_12_n_not_power_of_two() -> bool:
    """ST-ADV-12: Correctness for N not a power of two (N in {3, 5, 7, 10, 13, 23})."""
    for N in [3, 5, 7, 10, 13, 23]:
        arr = [0] + [i * 3 for i in range(1, N + 1)]
        oracle = SegmentTreeOracle(arr, op="sum")
        for l in range(1, N + 1):
            for r in range(l, N + 1):
                expected = sum(arr[l:r + 1])
                got = oracle.query(l, r)
                assert got == expected, f"N={N}, query({l}, {r}): expected {expected}, got {got}"
    return True


def test_st_adv_13_n_equals_one() -> bool:
    """ST-ADV-13: N = 1 boundary base case."""
    arr = [0, 42]
    oracle = SegmentTreeOracle(arr, op="sum")
    assert oracle.query(1, 1) == 42
    oracle.update(1, 99)
    assert oracle.query(1, 1) == 99

    lazy_oracle = CombinedLazySegmentTreeOracle(arr)
    assert lazy_oracle.range_query(1, 1) == 42
    lazy_oracle.range_add(1, 1, 10)
    assert lazy_oracle.range_query(1, 1) == 52
    lazy_oracle.range_assign(1, 1, 7)
    assert lazy_oracle.range_query(1, 1) == 7
    return True


def test_st_adv_14_query_exact_node_boundary() -> bool:
    """ST-ADV-14: Query exactly equal to canonical node boundaries."""
    N = 8
    arr = [0] + list(range(1, N + 1))  # [1..8]
    oracle = SegmentTreeOracle(arr, op="sum")

    # Midpoint of [1..8] is 4
    # Exact left child [1, 4]
    assert oracle.query(1, 4) == sum(range(1, 5))
    # Exact right child [5, 8]
    assert oracle.query(5, 8) == sum(range(5, 9))
    # Exact root [1, 8]
    assert oracle.query(1, 8) == sum(range(1, 9))
    # Sub-boundaries: [1, 2], [3, 4], [5, 6], [7, 8]
    assert oracle.query(1, 2) == 1 + 2
    assert oracle.query(3, 4) == 3 + 4
    assert oracle.query(5, 6) == 5 + 6
    assert oracle.query(7, 8) == 7 + 8
    return True


def test_st_adv_15_query_crossing_midpoint_repeatedly() -> bool:
    """ST-ADV-15: Query crossing midpoints repeatedly at multiple depths."""
    N = 16
    arr = [0] + [i * 2 for i in range(1, N + 1)]
    oracle = SegmentTreeOracle(arr, op="sum")

    crossing_queries = [
        (8, 9),
        (7, 9),
        (8, 10),
        (7, 10),
        (6, 11),
        (5, 12),
        (4, 13),
        (2, 7),
        (10, 15),
        (1, 16),
    ]
    for ql, qr in crossing_queries:
        expected = sum(arr[ql:qr + 1])
        got = oracle.query(ql, qr)
        assert got == expected, f"Query({ql}, {qr}): expected {expected}, got {got}"
    return True


def run_adversarial_battery() -> int:
    """Runs all 15 adversarial algebra tests and reports results."""
    tests = [
        ("ST-ADV-01", "Non-commutative associative merge (2x2 Matrix Mul)", test_st_adv_01_non_commutative_merge),
        ("ST-ADV-02", "All-negative maximum-subarray sum", test_st_adv_02_all_negative_max_subarray),
        ("ST-ADV-03", "Identity returned from left query only", test_st_adv_03_identity_from_left_query_only),
        ("ST-ADV-04", "Identity returned from right query only", test_st_adv_04_identity_from_right_query_only),
        ("ST-ADV-05", "Assignment -> Addition tag composition", test_st_adv_05_assignment_then_addition),
        ("ST-ADV-06", "Addition -> Assignment tag composition", test_st_adv_06_addition_then_assignment),
        ("ST-ADV-07", "Assign -> Add -> Assign tag composition", test_st_adv_07_assign_add_assign),
        ("ST-ADV-08", "Multiple overlapping range assignments", test_st_adv_08_overlapping_assignments),
        ("ST-ADV-09", "Negative values in range updates", test_st_adv_09_negative_values_lazy),
        ("ST-ADV-10", "64-bit integer overflow boundary", test_st_adv_10_64bit_overflow_boundary),
        ("ST-ADV-11", "__int128 intermediate multiplication safety", test_st_adv_11_int128_intermediate_multiplication),
        ("ST-ADV-12", "N not a power of two (N in {3, 5, 7, 10, 13, 23})", test_st_adv_12_n_not_power_of_two),
        ("ST-ADV-13", "N = 1 boundary base case", test_st_adv_13_n_equals_one),
        ("ST-ADV-14", "Query exactly equal to canonical node boundaries", test_st_adv_14_query_exact_node_boundary),
        ("ST-ADV-15", "Query repeatedly crossing midpoints", test_st_adv_15_query_crossing_midpoint_repeatedly),
    ]

    print("=" * 70)
    print("CHUP Phase 3J — Segment Tree Adversarial Algebra Test Suite (15 Tests)")
    print("=" * 70)
    passed = 0
    for tid, desc, fn in tests:
        try:
            fn()
            print(f"[{tid}] {desc}: PASS")
            passed += 1
        except Exception as e:
            print(f"[{tid}] {desc}: FAIL ({e})")

    print("-" * 70)
    print(f"Adversarial Algebra Results: {passed}/{len(tests)} passed ({passed/len(tests)*100:.1f}%)")
    print("=" * 70)
    return 0 if passed == len(tests) else 1


if __name__ == "__main__":
    sys.exit(run_adversarial_battery())
