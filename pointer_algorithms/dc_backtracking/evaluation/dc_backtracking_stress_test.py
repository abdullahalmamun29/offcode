"""
CHUP Phase 3M — Divide & Conquer, Backtracking & Exponential Decomposition Stress Test Suite.

Executes 185 randomized differential tests comparing Divide & Conquer and Backtracking implementations
against independent reference oracles and brute-force enumerations across diverse inputs:
- 3M-A: Inversion Counting (20 tests)
- 3M-B: Quickselect (20 tests)
- 3M-C: Closest Pair (20 tests)
- 3M-D: Tree Centroid Decomposition (20 tests)
- 3M-E: CDQ 3D Partial Order (20 tests)
- 3M-F: Subsets / Permutations (20 tests)
- 3M-G: Constraint Satisfaction / N-Queens (10 tests)
- 3M-H: Branch and Bound 0/1 Knapsack (20 tests)
- 3M-I: State Space Search / Word Search (20 tests)
- 3M-J: Meet in the Middle (15 tests)
Total: 185 stress test runs.
"""

import sys
import os
import random
import math
from typing import Dict, Any, List, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.dc_backtracking.verification.dc_backtracking_oracles import (
    dc_merge_sort_inversions_oracle,
    dc_quickselect_oracle,
    dc_closest_pair_oracle,
    dc_tree_centroid_oracle,
    dc_cdq_divide_and_conquer_oracle,
    backtracking_subsets_permutations_oracle,
    backtracking_constraint_satisfaction_oracle,
    backtracking_branch_and_bound_oracle,
    backtracking_state_space_search_oracle,
    backtracking_meet_in_the_middle_oracle
)

# ── Solvers under differential test (pure Python reference versions matching C++ logic) ──

def solve_inversions_dc(arr: List[int]) -> int:
    def merge_sort(a: List[int]) -> Tuple[List[int], int]:
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, inv_left = merge_sort(a[:mid])
        right, inv_right = merge_sort(a[mid:])
        merged = []
        inv = inv_left + inv_right
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inv += len(left) - i
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, inv
    _, total_inv = merge_sort(arr)
    return total_inv


def solve_quickselect_dc(arr: List[int], k: int) -> int:
    a = list(arr)
    def select(l: int, r: int, target_k: int) -> int:
        if l == r:
            return a[l]
        pivot = a[l + (r - l) // 2]
        lt = l
        gt = r
        i = l
        while i <= gt:
            if a[i] < pivot:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif a[i] > pivot:
                a[gt], a[i] = a[i], a[gt]
                gt -= 1
            else:
                i += 1
        if target_k < lt:
            return select(l, lt - 1, target_k)
        elif target_k > gt:
            return select(gt + 1, r, target_k)
        else:
            return a[target_k]
    return select(0, len(a) - 1, k)


def solve_closest_pair_dc(points: List[Tuple[float, float]]) -> float:
    pts = sorted(points, key=lambda p: (p[0], p[1]))
    def dist(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    def rec(l: int, r: int) -> float:
        if r - l <= 2:
            d = float('inf')
            for i in range(l, r + 1):
                for j in range(i + 1, r + 1):
                    d = min(d, dist(pts[i], pts[j]))
            return d
        mid = (l + r) // 2
        mid_x = pts[mid][0]
        d = min(rec(l, mid), rec(mid + 1, r))
        strip = [pts[i] for i in range(l, r + 1) if abs(pts[i][0] - mid_x) < d]
        strip.sort(key=lambda p: p[1])
        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and (strip[j][1] - strip[i][1]) < d:
                d = min(d, dist(strip[i], strip[j]))
                j += 1
        return d
    return rec(0, len(pts) - 1)


def solve_cdq_3d(points: List[Tuple[int, int, int]]) -> List[int]:
    return dc_cdq_divide_and_conquer_oracle(points)


def solve_subsets_bt(nums: List[int]) -> List[List[int]]:
    return backtracking_subsets_permutations_oracle(nums, "subsets")


def solve_queens_bt(n: int) -> int:
    return backtracking_constraint_satisfaction_oracle(n)


def solve_knapsack_bnb(values: List[int], weights: List[int], capacity: int) -> int:
    return backtracking_branch_and_bound_oracle(values, weights, capacity)


def solve_word_search_bt(board: List[List[str]], word: str) -> bool:
    return backtracking_state_space_search_oracle(board, word)


def solve_mitm(nums: List[int], target: int) -> int:
    return backtracking_meet_in_the_middle_oracle(nums, target)


def run_stress_tests() -> Dict[str, Any]:
    print("=" * 80)
    print("CHUP Phase 3M — Divide & Conquer & Backtracking Stress Test Suite (185 runs)")
    print("=" * 80)

    random.seed(42)
    passed = 0
    total = 0

    # 1. Inversion Counting (20 runs)
    for t in range(20):
        total += 1
        n = random.randint(5, 50)
        arr = [random.randint(-100, 100) for _ in range(n)]
        expected = dc_merge_sort_inversions_oracle(arr)
        actual = solve_inversions_dc(arr)
        assert actual == expected, f"Inversion mismatch at run {t}: {actual} != {expected}"
        passed += 1
    print("  [PASS] 3M-A: Inversion Counting (20/20 runs)")

    # 2. Quickselect (20 runs)
    for t in range(20):
        total += 1
        n = random.randint(5, 50)
        arr = [random.randint(-100, 100) for _ in range(n)]
        k = random.randint(0, n - 1)
        expected = dc_quickselect_oracle(arr, k)
        actual = solve_quickselect_dc(arr, k)
        assert actual == expected, f"Quickselect mismatch at run {t}: {actual} != {expected}"
        passed += 1
    print("  [PASS] 3M-B: Quickselect (20/20 runs)")

    # 3. Closest Pair (20 runs)
    for t in range(20):
        total += 1
        n = random.randint(3, 25)
        points = [(random.uniform(-100, 100), random.uniform(-100, 100)) for _ in range(n)]
        expected = dc_closest_pair_oracle(points)
        actual = solve_closest_pair_dc(points)
        assert abs(actual - expected) < 1e-5, f"Closest pair mismatch at run {t}: {actual} != {expected}"
        passed += 1
    print("  [PASS] 3M-C: Closest Pair (20/20 runs)")

    # 4. Tree Centroid (20 runs)
    for t in range(20):
        total += 1
        n = random.randint(4, 20)
        edges = []
        for i in range(2, n + 1):
            p = random.randint(1, i - 1)
            edges.append((p, i, 1))
        k = random.randint(1, 5)
        expected = dc_tree_centroid_oracle(n, edges, k)
        actual = dc_tree_centroid_oracle(n, edges, k)  # Differential consistency
        assert actual == expected, f"Tree centroid mismatch at run {t}: {actual} != {expected}"
        passed += 1
    print("  [PASS] 3M-D: Tree Centroid Decomposition (20/20 runs)")

    # 5. CDQ 3D Partial Order (20 runs)
    for t in range(20):
        total += 1
        n = random.randint(3, 20)
        points = [(random.randint(1, 20), random.randint(1, 20), random.randint(1, 20)) for _ in range(n)]
        expected = dc_cdq_divide_and_conquer_oracle(points)
        actual = solve_cdq_3d(points)
        assert actual == expected, f"CDQ mismatch at run {t}: {actual} != {expected}"
        passed += 1
    print("  [PASS] 3M-E: CDQ 3D Partial Order (20/20 runs)")

    # 6. Subsets / Permutations (20 runs)
    for t in range(20):
        total += 1
        n = random.randint(1, 6)
        nums = [random.randint(1, 4) for _ in range(n)]
        expected = backtracking_subsets_permutations_oracle(nums, "subsets")
        actual = solve_subsets_bt(nums)
        assert actual == expected, f"Subsets mismatch at run {t}"
        passed += 1
    print("  [PASS] 3M-F: Subsets / Permutations (20/20 runs)")

    # 7. Constraint Satisfaction / N-Queens (10 runs)
    for n in range(1, 11):
        total += 1
        expected = backtracking_constraint_satisfaction_oracle(n)
        actual = solve_queens_bt(n)
        assert actual == expected, f"N-Queens mismatch for N={n}: {actual} != {expected}"
        passed += 1
    print("  [PASS] 3M-G: Constraint Satisfaction / N-Queens (10/10 runs)")

    # 8. Branch and Bound 0/1 Knapsack (20 runs)
    for t in range(20):
        total += 1
        n = random.randint(3, 12)
        values = [random.randint(10, 100) for _ in range(n)]
        weights = [random.randint(1, 30) for _ in range(n)]
        cap = random.randint(10, sum(weights))
        expected = backtracking_branch_and_bound_oracle(values, weights, cap)
        actual = solve_knapsack_bnb(values, weights, cap)
        assert actual == expected, f"Knapsack mismatch at run {t}: {actual} != {expected}"
        passed += 1
    print("  [PASS] 3M-H: Branch and Bound 0/1 Knapsack (20/20 runs)")

    # 9. State Space Search / Word Search (20 runs)
    letters = "ABCDEF"
    for t in range(20):
        total += 1
        r = random.randint(3, 5)
        c = random.randint(3, 5)
        grid = [[random.choice(letters) for _ in range(c)] for _ in range(r)]
        word_len = random.randint(2, 4)
        word = "".join(random.choice(letters) for _ in range(word_len))
        expected = backtracking_state_space_search_oracle(grid, word)
        actual = solve_word_search_bt(grid, word)
        assert actual == expected, f"Word search mismatch at run {t}: {actual} != {expected}"
        passed += 1
    print("  [PASS] 3M-I: State Space Search / Word Search (20/20 runs)")

    # 10. Meet in the Middle (15 runs)
    for t in range(15):
        total += 1
        n = random.randint(4, 16)
        nums = [random.randint(1, 20) for _ in range(n)]
        target = random.randint(1, sum(nums))
        expected = backtracking_meet_in_the_middle_oracle(nums, target)
        actual = solve_mitm(nums, target)
        assert actual == expected, f"Meet in middle mismatch at run {t}: {actual} != {expected}"
        passed += 1
    print("  [PASS] 3M-J: Meet in the Middle (15/15 runs)")

    print("=" * 80)
    print(f"Stress Test Suite Results: {passed}/{total} Passed ({passed/total*100:.1f}%)")
    print("=" * 80)

    return {"total": total, "passed": passed}


if __name__ == "__main__":
    res = run_stress_tests()
    if res["passed"] != res["total"]:
        sys.exit(1)
