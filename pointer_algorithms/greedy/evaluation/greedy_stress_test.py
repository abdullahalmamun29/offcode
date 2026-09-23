"""
CHUP Phase 3L — Greedy Algorithms Stress Test Suite.
Executes 150+ randomized differential tests comparing Greedy implementations
against independent reference oracles and brute-force enumerations across diverse inputs.
"""

import sys
import os
import random
import itertools
import heapq
from typing import Dict, Any, List, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.greedy.verification.greedy_oracles import (
    greedy_interval_selection_oracle,
    greedy_interval_covering_oracle,
    greedy_fractional_knapsack_oracle,
    greedy_deadline_scheduling_oracle,
    greedy_heap_assisted_oracle,
    greedy_huffman_merge_oracle,
    greedy_sequence_local_choice_oracle,
    greedy_reachability_partition_oracle,
    greedy_graph_mst_oracle,
    greedy_general_exchange_oracle
)

# ── Greedy Solvers under differential test ──

def solve_interval_selection_greedy(intervals: List[Tuple[int, int]]) -> int:
    if not intervals:
        return 0
    # Earliest finish time
    sorted_iv = sorted(intervals, key=lambda x: (x[1], x[0]))
    count = 1
    last_end = sorted_iv[0][1]
    for s, e in sorted_iv[1:]:
        if s >= last_end:
            count += 1
            last_end = e
    return count

def solve_interval_covering_greedy(intervals: List[Tuple[int, int]]) -> int:
    if not intervals:
        return 0
    # Sort by end point
    sorted_iv = sorted(intervals, key=lambda x: (x[1], x[0]))
    points = 1
    last_point = sorted_iv[0][1]
    for s, e in sorted_iv[1:]:
        if s > last_point:
            points += 1
            last_point = e
    return points

def solve_fractional_knapsack_greedy(items: List[Tuple[float, float]], capacity: float) -> float:
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

def solve_deadline_scheduling_greedy(jobs: List[Tuple[int, int]]) -> int:
    if not jobs:
        return 0
    # Earliest Due Date (EDD)
    sorted_jobs = sorted(jobs, key=lambda x: (x[1], x[0]))
    cur_time = 0
    max_late = 0
    for dur, dead in sorted_jobs:
        cur_time += dur
        max_late = max(max_late, max(0, cur_time - dead))
    return max_late

def solve_heap_assisted_greedy(target: int, start_fuel: int, stations: List[Tuple[int, int]]) -> int:
    sorted_st = sorted(stations, key=lambda x: x[0])
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

def solve_huffman_merge_greedy(frequencies: List[int]) -> int:
    if len(frequencies) <= 1:
        return 0
    h = list(frequencies)
    heapq.heapify(h)
    total_cost = 0
    while len(h) > 1:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        c = a + b
        total_cost += c
        heapq.heappush(h, c)
    return total_cost

def solve_sequence_local_choice_greedy(num: str, k: int) -> str:
    n = len(num)
    if k >= n:
        return "0"
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

def solve_reachability_partition_greedy(arr: List[int]) -> int:
    n = len(arr)
    if n <= 1:
        return 0
    jumps = 0
    cur_end = 0
    farthest = 0
    for i in range(n - 1):
        farthest = max(farthest, i + arr[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
            if cur_end >= n - 1:
                break
    return jumps

def solve_graph_mst_kruskal(n: int, edges: List[Tuple[int, int, int]]) -> int:
    parent = list(range(n + 1))
    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])
        return parent[i]
    def union(i, j):
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj
            return True
        return False

    sorted_edges = sorted(edges, key=lambda x: x[2])
    mst_weight = 0
    edge_count = 0
    for u, v, w in sorted_edges:
        if union(u, v):
            mst_weight += w
            edge_count += 1
            if edge_count == n - 1:
                break
    return mst_weight if edge_count == n - 1 or n <= 1 else 0

def solve_general_exchange_greedy(nums: List[str]) -> str:
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


def run_greedy_stress_tests() -> Dict[str, Any]:
    random.seed(42)
    total_tests = 0
    passed_tests = 0
    failures = []

    print(f"\n========================================================")
    print(f"  CHUP Phase 3L — Greedy Algorithms Stress Test Suite")
    print(f"  Target: 150+ Randomized Differential Runs")
    print(f"========================================================\n")

    # 1. 3L-A Interval Selection Differential Tests (20 runs)
    print("  [Suite 1/10] 3L-A Interval Selection Stress (20 runs)...")
    for i in range(20):
        total_tests += 1
        n = random.randint(1, 12)
        intervals = []
        for _ in range(n):
            s = random.randint(0, 20)
            e = s + random.randint(1, 10)
            intervals.append((s, e))
        greedy_res = solve_interval_selection_greedy(intervals)
        oracle_res = greedy_interval_selection_oracle(intervals)
        if greedy_res == oracle_res:
            passed_tests += 1
        else:
            failures.append((f"Interval Selection Run {i}", f"Greedy={greedy_res} != Oracle={oracle_res} on {intervals}"))

    # 2. 3L-B Interval Covering Differential Tests (20 runs)
    print("  [Suite 2/10] 3L-B Interval Covering Stress (20 runs)...")
    for i in range(20):
        total_tests += 1
        n = random.randint(1, 15)
        intervals = []
        for _ in range(n):
            s = random.randint(0, 25)
            e = s + random.randint(1, 12)
            intervals.append((s, e))
        greedy_res = solve_interval_covering_greedy(intervals)
        oracle_res = greedy_interval_covering_oracle(intervals)
        if greedy_res == oracle_res:
            passed_tests += 1
        else:
            failures.append((f"Interval Covering Run {i}", f"Greedy={greedy_res} != Oracle={oracle_res} on {intervals}"))

    # 3. 3L-C Fractional Knapsack Differential Tests (20 runs)
    print("  [Suite 3/10] 3L-C Fractional Knapsack Stress (20 runs)...")
    for i in range(20):
        total_tests += 1
        n = random.randint(1, 10)
        cap = random.randint(10, 100)
        items = []
        for _ in range(n):
            val = random.randint(5, 100)
            wt = random.randint(1, 40)
            items.append((float(val), float(wt)))
        greedy_res = solve_fractional_knapsack_greedy(items, cap)
        oracle_res = greedy_fractional_knapsack_oracle(items, cap)
        if abs(greedy_res - oracle_res) < 1e-2:
            passed_tests += 1
        else:
            failures.append((f"Fractional Knapsack Run {i}", f"Greedy={greedy_res} != Oracle={oracle_res} on {items}, cap={cap}"))

    # 4. 3L-D Deadline Scheduling EDD Differential Tests (20 runs)
    print("  [Suite 4/10] 3L-D Deadline Scheduling EDD Stress (20 runs)...")
    for i in range(20):
        total_tests += 1
        n = random.randint(1, 8)
        jobs = []
        for _ in range(n):
            dur = random.randint(1, 10)
            dead = random.randint(1, 25)
            jobs.append((dur, dead))
        greedy_res = solve_deadline_scheduling_greedy(jobs)
        oracle_res = greedy_deadline_scheduling_oracle(jobs)
        if greedy_res == oracle_res:
            passed_tests += 1
        else:
            failures.append((f"Deadline Scheduling Run {i}", f"Greedy={greedy_res} != Oracle={oracle_res} on {jobs}"))

    # 5. 3L-E Heap-Assisted Refueling Differential Tests (15 runs)
    print("  [Suite 5/10] 3L-E Heap-Assisted Refueling Stress (15 runs)...")
    for i in range(15):
        total_tests += 1
        target = random.randint(30, 100)
        start_fuel = random.randint(5, 30)
        m = random.randint(1, 6)
        stations = []
        pos = 0
        for _ in range(m):
            pos += random.randint(5, 20)
            if pos < target:
                fuel = random.randint(5, 30)
                stations.append((pos, fuel))
        greedy_res = solve_heap_assisted_greedy(target, start_fuel, stations)
        oracle_res = greedy_heap_assisted_oracle(target, start_fuel, stations)
        if greedy_res == oracle_res:
            passed_tests += 1
        else:
            failures.append((f"Heap Refueling Run {i}", f"Greedy={greedy_res} != Oracle={oracle_res} on target={target}, fuel={start_fuel}, st={stations}"))

    # 6. 3L-F Huffman Optimal Merge Differential Tests (20 runs)
    print("  [Suite 6/10] 3L-F Huffman Optimal Merge Stress (20 runs)...")
    for i in range(20):
        total_tests += 1
        n = random.randint(1, 10)
        freqs = [random.randint(1, 50) for _ in range(n)]
        greedy_res = solve_huffman_merge_greedy(freqs)
        oracle_res = greedy_huffman_merge_oracle(freqs)
        if greedy_res == oracle_res:
            passed_tests += 1
        else:
            failures.append((f"Huffman Merge Run {i}", f"Greedy={greedy_res} != Oracle={oracle_res} on {freqs}"))

    # 7. 3L-G Sequence Local Choice (Remove K Digits) Differential Tests (20 runs)
    print("  [Suite 7/10] 3L-G Sequence Local Choice Stress (20 runs)...")
    for i in range(20):
        total_tests += 1
        n = random.randint(1, 10)
        num = "".join(str(random.randint(0, 9)) for _ in range(n))
        # ensure first digit is non-zero
        num = str(random.randint(1, 9)) + num[1:]
        k = random.randint(0, n)
        greedy_res = solve_sequence_local_choice_greedy(num, k)
        oracle_res = greedy_sequence_local_choice_oracle(num, k)
        if greedy_res == oracle_res:
            passed_tests += 1
        else:
            failures.append((f"Sequence Local Choice Run {i}", f"Greedy={greedy_res} != Oracle={oracle_res} on num={num}, k={k}"))

    # 8. 3L-H Reachability Frontier (Jump Game) Differential Tests (20 runs)
    print("  [Suite 8/10] 3L-H Reachability Frontier Stress (20 runs)...")
    for i in range(20):
        total_tests += 1
        n = random.randint(1, 12)
        # Ensure reachability: each arr[j] >= 1
        arr = [random.randint(1, 4) for _ in range(n)]
        greedy_res = solve_reachability_partition_greedy(arr)
        oracle_res = greedy_reachability_partition_oracle(arr)
        if greedy_res == oracle_res:
            passed_tests += 1
        else:
            failures.append((f"Reachability Frontier Run {i}", f"Greedy={greedy_res} != Oracle={oracle_res} on {arr}"))

    # 9. 3L-I Graph MST Kruskal vs Prim Differential Tests (15 runs)
    print("  [Suite 9/10] 3L-I Graph MST Kruskal vs Prim Stress (15 runs)...")
    for i in range(15):
        total_tests += 1
        n = random.randint(2, 6)
        # Generate connected random graph
        edges = []
        for v in range(2, n + 1):
            u = random.randint(1, v - 1)
            w = random.randint(1, 20)
            edges.append((u, v, w))
        # Add a few random extra edges
        extra = random.randint(0, 4)
        for _ in range(extra):
            u = random.randint(1, n)
            v = random.randint(1, n)
            if u != v:
                w = random.randint(1, 20)
                edges.append((u, v, w))
        greedy_res = solve_graph_mst_kruskal(n, edges)
        oracle_res = greedy_graph_mst_oracle(n, edges)
        if greedy_res == oracle_res:
            passed_tests += 1
        else:
            failures.append((f"Graph MST Run {i}", f"Kruskal={greedy_res} != Prim={oracle_res} on n={n}, edges={edges}"))

    # 10. 3L-J General Exchange Comparator Differential Tests (15 runs)
    print("  [Suite 10/10] 3L-J General Exchange Comparator Stress (15 runs)...")
    for i in range(15):
        total_tests += 1
        n = random.randint(1, 7)
        nums = [str(random.randint(0, 99)) for _ in range(n)]
        greedy_res = solve_general_exchange_greedy(nums)
        oracle_res = greedy_general_exchange_oracle(nums)
        if greedy_res == oracle_res:
            passed_tests += 1
        else:
            failures.append((f"General Exchange Run {i}", f"Greedy={greedy_res} != Oracle={oracle_res} on {nums}"))

    summary = {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failures": failures
    }

    print("\n--------------------------------------------------------")
    print(f"  Stress Test Results: {passed_tests}/{total_tests} passed ({passed_tests/total_tests*100:.1f}%)")
    print("--------------------------------------------------------\n")

    return summary


if __name__ == "__main__":
    summary = run_greedy_stress_tests()
    if summary["failures"]:
        sys.exit(1)
