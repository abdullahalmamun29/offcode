"""
Independent Reference Oracles for Phase 3M — Divide & Conquer, Backtracking, and Exponential Decomposition.

Implements mathematically independent reference solvers (brute-force enumeration,
exact dynamic programming, or BFS all-pairs path search) for all 10 Phase 3M patterns.
"""

from typing import List, Tuple, Dict, Any, Optional
import itertools
import math
from collections import deque

def dc_merge_sort_inversions_oracle(arr: List[int], predicate_multiplier: int = 1) -> int:
    """
    Brute-force O(N^2) oracle for inversion / reverse pair counting.
    Counts pairs (i, j) such that i < j and arr[i] > predicate_multiplier * arr[j].
    """
    n = len(arr)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > predicate_multiplier * arr[j]:
                count += 1
    return count


def dc_quickselect_oracle(arr: List[int], k: int) -> int:
    """
    Independent oracle for k-th order statistic via total sorting.
    k is 0-based.
    """
    if not arr:
        return 0
    k = max(0, min(len(arr) - 1, k))
    return sorted(arr)[k]


def dc_closest_pair_oracle(pts: List[Tuple[float, float]]) -> float:
    """
    Brute-force O(N^2) oracle for minimum Euclidean distance between 2D points.
    """
    n = len(pts)
    if n < 2:
        return 0.0
    min_dist_sq = float('inf')
    for i in range(n):
        x1, y1 = pts[i]
        for j in range(i + 1, n):
            x2, y2 = pts[j]
            d_sq = (x1 - x2) ** 2 + (y1 - y2) ** 2
            if d_sq < min_dist_sq:
                min_dist_sq = d_sq
    return math.sqrt(min_dist_sq)


def dc_tree_centroid_oracle(n: int, edges: List[Tuple[int, int, int]], k_target: int) -> int:
    """
    All-pairs tree path search via BFS/DFS from each node.
    edges: list of (u, v, weight).
    Counts pairs (u, v) with u < v such that dist(u, v) <= k_target.
    """
    if n <= 1:
        return 0
    adj: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, n + 1)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    count = 0
    for start in range(1, n + 1):
        # BFS from start
        visited = {start}
        q = deque([(start, 0)])
        while q:
            u, d = q.popleft()
            if u > start and d <= k_target:
                count += 1
            for v, w in adj[u]:
                if v not in visited:
                    visited.add(v)
                    q.append((v, d + w))
    return count


def dc_cdq_divide_and_conquer_oracle(elements: List[Tuple[int, int, int]]) -> List[int]:
    """
    Brute-force O(N^2) oracle for 3D partial order counting:
    For each element i, count j != i such that a_j <= a_i and b_j <= b_i and c_j <= c_i.
    """
    n = len(elements)
    ans = [0] * n
    for i in range(n):
        a_i, b_i, c_i = elements[i]
        for j in range(n):
            if i != j:
                a_j, b_j, c_j = elements[j]
                if a_j <= a_i and b_j <= b_i and c_j <= c_i:
                    ans[i] += 1
    return ans


def backtracking_subsets_permutations_oracle(nums: List[int], mode: str = "subsets") -> List[List[int]]:
    """
    Independent combinatorial generation using itertools with duplicate deduplication.
    """
    if mode == "subsets":
        results = set()
        sorted_nums = sorted(nums)
        for r in range(len(sorted_nums) + 1):
            for comb in itertools.combinations(sorted_nums, r):
                results.add(comb)
        return [list(x) for x in sorted(results)]
    else:
        results = set()
        sorted_nums = sorted(nums)
        for perm in itertools.permutations(sorted_nums):
            results.add(perm)
        return [list(x) for x in sorted(results)]


def backtracking_constraint_satisfaction_oracle(n: int) -> int:
    """
    N-Queens solution count via brute-force permutation test.
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    solutions = 0
    for perm in itertools.permutations(range(n)):
        # Check diagonal collisions
        diag1 = set()
        diag2 = set()
        valid = True
        for row, col in enumerate(perm):
            if (row - col) in diag1 or (row + col) in diag2:
                valid = False
                break
            diag1.add(row - col)
            diag2.add(row + col)
        if valid:
            solutions += 1
    return solutions


def backtracking_branch_and_bound_oracle(values: List[int], weights: List[int], capacity: int) -> int:
    """
    Exact 0/1 knapsack dynamic programming table oracle.
    """
    n = len(values)
    if n == 0 or capacity <= 0:
        return 0
    dp = [0] * (capacity + 1)
    for i in range(n):
        v, w = values[i], weights[i]
        for cap in range(capacity, w - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - w] + v)
    return dp[capacity]


def backtracking_state_space_search_oracle(board: List[str], word: str) -> bool:
    """
    Independent 2D grid word search oracle.
    """
    if not board or not word:
        return False
    R, C = len(board), len(board[0])
    L = len(word)

    def dfs(r: int, c: int, idx: int, visited: set) -> bool:
        if idx == L:
            return True
        if r < 0 or r >= R or c < 0 or c >= C or (r, c) in visited or board[r][c] != word[idx]:
            return False
        visited.add((r, c))
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if dfs(r + dr, c + dc, idx + 1, visited):
                return True
        visited.remove((r, c))
        return False

    for r in range(R):
        for c in range(C):
            if board[r][c] == word[0]:
                if dfs(r, c, 0, set()):
                    return True
    return False


def backtracking_meet_in_the_middle_oracle(nums: List[int], target: int) -> int:
    """
    Brute-force subset sum count oracle: counts all subsets whose sum equals target.
    """
    count = 0
    n = len(nums)
    for r in range(n + 1):
        for comb in itertools.combinations(nums, r):
            if sum(comb) == target:
                count += 1
    return count
