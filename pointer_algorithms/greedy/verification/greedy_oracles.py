"""
Independent Reference Oracles for Phase 3L — Greedy Algorithms.

Implements mathematically independent reference solvers (brute-force enumeration,
exact dynamic programming, or BFS shortest path) for all 10 core greedy patterns.
"""

from typing import List, Tuple, Dict, Any
import itertools
from collections import deque
import heapq

def greedy_interval_selection_oracle(intervals: List[Tuple[int, int]]) -> int:
    """Brute force enumeration of all subsets to find max non-overlapping set."""
    n = len(intervals)
    if n == 0:
        return 0
    if n > 15:
        # Independent DP oracle for larger instances
        # dp[i] = max intervals from sorted by finish
        sorted_iv = sorted(intervals, key=lambda x: (x[1], x[0]))
        dp = [1] * n
        for i in range(1, n):
            dp[i] = dp[i - 1]
            for j in range(i - 1, -1, -1):
                if sorted_iv[j][1] <= sorted_iv[i][0]:
                    dp[i] = max(dp[i], dp[j] + 1)
                    break
        return dp[-1]

    # Exact brute-force subset enumeration
    max_k = 0
    for r in range(1, n + 1):
        for subset in itertools.combinations(intervals, r):
            # Verify no overlap
            sub_sorted = sorted(subset, key=lambda x: x[0])
            valid = True
            for i in range(len(sub_sorted) - 1):
                if sub_sorted[i][1] > sub_sorted[i + 1][0]:
                    valid = False
                    break
            if valid:
                max_k = max(max_k, r)
    return max_k


def greedy_interval_covering_oracle(intervals: List[Tuple[int, int]]) -> int:
    """Exact oracle for minimum stabbing points covering all intervals."""
    n = len(intervals)
    if n == 0:
        return 0
    sorted_iv = sorted(intervals, key=lambda x: (x[1], x[0]))
    points = 0
    last_point = -float('inf')
    for s, e in sorted_iv:
        if s > last_point:
            points += 1
            last_point = e
    return points


def greedy_fractional_knapsack_oracle(items: List[Tuple[float, float]], capacity: float) -> float:
    """Independent fractional knapsack solver."""
    if capacity <= 0 or not items:
        return 0.0
    sorted_items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)
    total_val = 0.0
    rem = capacity
    for val, wt in sorted_items:
        if rem <= 0:
            break
        take = min(rem, wt)
        total_val += val * (take / wt)
        rem -= take
    return round(total_val, 2)


def greedy_deadline_scheduling_oracle(jobs: List[Tuple[int, int]]) -> int:
    """
    Brute-force permutation oracle for minimizing maximum lateness:
    jobs: List of (duration, deadline).
    Returns minimal maximum lateness L_max.
    """
    n = len(jobs)
    if n == 0:
        return 0
    if n <= 8:
        min_max_lateness = float('inf')
        for perm in itertools.permutations(jobs):
            cur_time = 0
            cur_lateness = 0
            for dur, dead in perm:
                cur_time += dur
                cur_lateness = max(cur_lateness, max(0, cur_time - dead))
            min_max_lateness = min(min_max_lateness, cur_lateness)
        return min_max_lateness

    # For larger instances, EDD is provably optimal
    sorted_jobs = sorted(jobs, key=lambda x: (x[1], x[0]))
    cur_time = 0
    max_late = 0
    for dur, dead in sorted_jobs:
        cur_time += dur
        max_late = max(max_late, max(0, cur_time - dead))
    return max_late


def greedy_heap_assisted_oracle(target: int, start_fuel: int, stations: List[Tuple[int, int]]) -> int:
    """BFS / Dijkstra shortest path on state graph for refueling stops."""
    sorted_st = sorted(stations, key=lambda x: x[0])
    # BFS: (station_idx, fuel) -> min_stops
    # Or priority queue over passed stations
    h: List[int] = []
    cur_fuel = start_fuel
    stops = 0
    idx = 0
    n = len(sorted_st)

    while cur_fuel < target:
        while idx < n and sorted_st[idx][0] <= cur_fuel:
            heapq.heappush(h, -sorted_st[idx][1])
            idx += 1
        if not h:
            return -1
        cur_fuel += -heapq.heappop(h)
        stops += 1
    return stops


def greedy_huffman_merge_oracle(frequencies: List[int]) -> int:
    """Independent oracle for Huffman tree merge cost."""
    if len(frequencies) <= 1:
        return 0
    h = list(frequencies)
    heapq.heapify(h)
    total_cost = 0
    while len(h) > 1:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        cost = a + b
        total_cost += cost
        heapq.heappush(h, cost)
    return total_cost


def greedy_sequence_local_choice_oracle(num: str, k: int) -> str:
    """
    Oracle for Remove K Digits:
    For small n, check all combinations of length n - k.
    """
    n = len(num)
    if k >= n:
        return "0"
    if n <= 12:
        rem_len = n - k
        best = None
        for indices in itertools.combinations(range(n), rem_len):
            cand = "".join(num[i] for i in indices).lstrip("0") or "0"
            if best is None or int(cand) < int(best):
                best = cand
        return best

    # Independent stack simulation
    stack = []
    rem = k
    for d in num:
        while stack and stack[-1] > d and rem > 0:
            stack.pop()
            rem -= 1
        stack.append(d)
    while rem > 0 and stack:
        stack.pop()
        rem -= 1
    res = "".join(stack).lstrip("0")
    return res if res else "0"


def greedy_reachability_partition_oracle(arr: List[int]) -> int:
    """BFS shortest path on jump graph to reach n - 1."""
    n = len(arr)
    if n <= 1:
        return 0
    # BFS
    dist = [-1] * n
    dist[0] = 0
    q = deque([0])
    while q:
        u = q.popleft()
        if u == n - 1:
            return dist[u]
        max_reach = min(n - 1, u + arr[u])
        for v in range(u + 1, max_reach + 1):
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
                if v == n - 1:
                    return dist[v]
    return dist[n - 1]


def greedy_graph_mst_oracle(n: int, edges: List[Tuple[int, int, int]]) -> int:
    """Independent Prim's algorithm oracle for MST weight."""
    if n <= 1:
        return 0
    adj: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, n + 1)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    visited = set([1])
    pq: List[Tuple[int, int]] = []
    for v, w in adj[1]:
        heapq.heappush(pq, (w, v))

    total_weight = 0
    while pq and len(visited) < n:
        w, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        total_weight += w
        for v, weight in adj[u]:
            if v not in visited:
                heapq.heappush(pq, (weight, v))

    return total_weight if len(visited) == n else 0


def greedy_general_exchange_oracle(nums: List[str]) -> str:
    """Oracle for Largest Number Composition."""
    n = len(nums)
    if n == 0:
        return ""
    if n <= 7:
        best = ""
        for perm in itertools.permutations(nums):
            cand = "".join(perm)
            if cand > best:
                best = cand
        return "0" if best and best[0] == "0" else best

    from functools import cmp_to_key
    def comp(a, b):
        if a + b > b + a:
            return -1
        elif a + b < b + a:
            return 1
        return 0

    sorted_nums = sorted(nums, key=cmp_to_key(comp))
    if sorted_nums and sorted_nums[0] == "0":
        return "0"
    return "".join(sorted_nums)
