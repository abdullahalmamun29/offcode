"""
Independent Brute-Force Oracles for Binary Search Domain (Phase 3C).

These functions serve as ground truth for all benchmark and property verification.
None of these functions use binary search; they use explicit linear scans and
exhaustive testing over the domain.
"""

from typing import List, Optional

def oracle_binary_search_exact(arr: List[int], target: int) -> int:
    """Linear search for exact target match."""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

def oracle_lower_bound(arr: List[int], target: int) -> int:
    """Smallest index i such that arr[i] >= target, or len(arr) if none."""
    for i, val in enumerate(arr):
        if val >= target:
            return i
    return len(arr)

def oracle_upper_bound(arr: List[int], target: int) -> int:
    """Smallest index i such that arr[i] > target, or len(arr) if none."""
    for i, val in enumerate(arr):
        if val > target:
            return i
    return len(arr)

def oracle_first_occurrence(arr: List[int], target: int) -> int:
    """First index where arr[i] == target, or -1 if absent."""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

def oracle_last_occurrence(arr: List[int], target: int) -> int:
    """Last index where arr[i] == target, or -1 if absent."""
    ans = -1
    for i, val in enumerate(arr):
        if val == target:
            ans = i
    return ans

def oracle_predecessor(arr: List[int], target: int) -> int:
    """Largest element strictly less than target in sorted arr, or -1."""
    ans = -1
    for val in arr:
        if val < target:
            ans = val
    return ans

def oracle_successor(arr: List[int], target: int) -> int:
    """Smallest element strictly greater than target in sorted arr, or -1."""
    for val in arr:
        if val > target:
            return val
    return -1

def oracle_first_false(arr: List[int], target: int) -> int:
    """First index where condition <= target fails (i.e. first > target), or len(arr)."""
    for i, val in enumerate(arr):
        if val > target:
            return i
    return len(arr)

def oracle_last_false(arr: List[int], target: int) -> int:
    """Last index where condition >= target fails (i.e. last < target), or -1."""
    ans = -1
    for i, val in enumerate(arr):
        if val < target:
            ans = i
    return ans

def oracle_min_ship_capacity(weights: List[int], days: int) -> int:
    """Exhaustive linear search for minimal capacity to ship within days."""
    if not weights:
        return 0
    lo = max(weights)
    hi = sum(weights)
    for cap in range(lo, hi + 1):
        parts = 1
        current = 0
        for w in weights:
            if current + w > cap:
                parts += 1
                current = w
            else:
                current += w
        if parts <= days:
            return cap
    return hi

def oracle_max_min_distance(stalls: List[int], cows: int) -> int:
    """Exhaustive linear search for maximal separation distance."""
    sorted_stalls = sorted(stalls)
    if len(sorted_stalls) < cows or cows < 2:
        return 0
    max_d = sorted_stalls[-1] - sorted_stalls[0]
    best = 1
    for d in range(1, max_d + 1):
        count = 1
        last = sorted_stalls[0]
        for pos in sorted_stalls[1:]:
            if pos - last >= d:
                count += 1
                last = pos
        if count >= cows:
            best = d
    return best

def oracle_integer_sqrt(n: int) -> int:
    """Exhaustive linear scan for floor(sqrt(n))."""
    if n < 0:
        return -1
    x = 0
    while (x + 1) * (x + 1) <= n:
        x += 1
    return x
