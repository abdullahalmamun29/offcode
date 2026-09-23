"""
Brute-Force / Reference Oracles for Benchmark Problem Verification.

Provides indisputable ground truth for small input instances (N <= 100).
"""

from typing import List, Tuple, Optional, Any
from collections import Counter

class BruteForceOracles:

    @staticmethod
    def pair_sum_sorted(arr: List[int], target: int) -> Optional[Tuple[int, int]]:
        """O(N^2) exhaustive pair sum search."""
        n = len(arr)
        for i in range(n):
            for j in range(i + 1, n):
                if arr[i] + arr[j] == target:
                    return (i, j)
        return None

    @staticmethod
    def container_most_water(heights: List[int]) -> int:
        """O(N^2) exhaustive area calculation."""
        n = len(heights)
        max_area = 0
        for i in range(n):
            for j in range(i + 1, n):
                area = min(heights[i], heights[j]) * (j - i)
                if area > max_area:
                    max_area = area
        return max_area

    @staticmethod
    def remove_duplicates(arr: List[int]) -> List[int]:
        """Reference deduplication preserving order."""
        seen = set()
        res = []
        for x in arr:
            if x not in seen:
                seen.add(x)
                res.append(x)
        return res

    @staticmethod
    def sliding_window_fixed_max(arr: List[int], k: int) -> int:
        """O(N * K) brute force fixed window max sum."""
        n = len(arr)
        if k > n or k <= 0:
            return -1
        max_s = float('-inf')
        for i in range(n - k + 1):
            s = sum(arr[i:i + k])
            if s > max_s:
                max_s = s
        return max_s

    @staticmethod
    def min_size_subarray_sum(arr: List[int], target: int) -> int:
        """O(N^2) brute force minimum length subarray with sum >= target."""
        n = len(arr)
        min_l = float('inf')
        for i in range(n):
            s = 0
            for j in range(i, n):
                s += arr[j]
                if s >= target:
                    min_l = min(min_l, j - i + 1)
                    break
        return min_l if min_l != float('inf') else 0

    @staticmethod
    def longest_substring_k_distinct(s: str, k: int) -> int:
        """O(N^2) brute force longest substring with at most k distinct."""
        n = len(s)
        max_l = 0
        for i in range(n):
            seen = set()
            for j in range(i, n):
                seen.add(s[j])
                if len(seen) <= k:
                    max_l = max(max_l, j - i + 1)
                else:
                    break
        return max_l

    @staticmethod
    def dutch_national_flag(arr: List[int]) -> List[int]:
        """Reference sort for 0, 1, 2."""
        return sorted(arr)
