"""
Monotonic Stack Brute-Force Oracles (Phase 3B).

Each oracle implements the naive O(n^2) algorithm for a monotonic stack pattern.
Used to verify the correctness of O(n) stack-based solutions.
"""

from typing import List

MOD = 10**9 + 7


def oracle_next_greater_element(arr):
    n = len(arr)
    result = [-1] * n
    for i in range(n):
        for j in range(i + 1, n):
            if arr[j] > arr[i]:
                result[i] = arr[j]
                break
    return result


def oracle_next_smaller_element(arr):
    n = len(arr)
    result = [-1] * n
    for i in range(n):
        for j in range(i + 1, n):
            if arr[j] < arr[i]:
                result[i] = arr[j]
                break
    return result


def oracle_previous_greater_element(arr):
    n = len(arr)
    result = [-1] * n
    for i in range(n):
        for j in range(i - 1, -1, -1):
            if arr[j] > arr[i]:
                result[i] = arr[j]
                break
    return result


def oracle_previous_smaller_element(arr):
    n = len(arr)
    result = [-1] * n
    for i in range(n):
        for j in range(i - 1, -1, -1):
            if arr[j] < arr[i]:
                result[i] = arr[j]
                break
    return result


def oracle_nearest_greater_element(arr):
    n = len(arr)
    result = [-1] * n
    for i in range(n):
        best = None
        for j in range(i - 1, -1, -1):
            if arr[j] > arr[i]:
                best = i - j if best is None else min(best, i - j)
                break
        for j in range(i + 1, n):
            if arr[j] > arr[i]:
                d = j - i
                best = d if best is None else min(best, d)
                break
        result[i] = best if best is not None else -1
    return result


def oracle_nearest_smaller_element(arr):
    n = len(arr)
    result = [-1] * n
    for i in range(n):
        best = None
        for j in range(i - 1, -1, -1):
            if arr[j] < arr[i]:
                best = i - j if best is None else min(best, i - j)
                break
        for j in range(i + 1, n):
            if arr[j] < arr[i]:
                d = j - i
                best = d if best is None else min(best, d)
                break
        result[i] = best if best is not None else -1
    return result


def oracle_stock_span(prices):
    n = len(prices)
    span = [0] * n
    for i in range(n):
        count = 1
        j = i - 1
        while j >= 0 and prices[j] <= prices[i]:
            count += 1
            j -= 1
        span[i] = count
    return span


def oracle_largest_rectangle_histogram(heights):
    n = len(heights)
    max_area = 0
    for i in range(n):
        min_h = heights[i]
        for j in range(i, n):
            min_h = min(min_h, heights[j])
            area = min_h * (j - i + 1)
            max_area = max(max_area, area)
    return max_area


def oracle_circular_next_greater(arr):
    n = len(arr)
    result = [-1] * n
    for i in range(n):
        for offset in range(1, n):
            j = (i + offset) % n
            if arr[j] > arr[i]:
                result[i] = arr[j]
                break
    return result


def oracle_sum_subarray_minimums(arr):
    n = len(arr)
    total = 0
    for l in range(n):
        cur_min = arr[l]
        for r in range(l, n):
            cur_min = min(cur_min, arr[r])
            total = (total + cur_min) % MOD
    return total


def oracle_sum_subarray_maximums(arr):
    n = len(arr)
    total = 0
    for l in range(n):
        cur_max = arr[l]
        for r in range(l, n):
            cur_max = max(cur_max, arr[r])
            total = (total + cur_max) % MOD
    return total


ORACLE_DISPATCH = {
    "next_greater_element": oracle_next_greater_element,
    "next_smaller_element": oracle_next_smaller_element,
    "previous_greater_element": oracle_previous_greater_element,
    "previous_smaller_element": oracle_previous_smaller_element,
    "nearest_greater_element": oracle_nearest_greater_element,
    "nearest_smaller_element": oracle_nearest_smaller_element,
    "stock_span": oracle_stock_span,
    "largest_rectangle_histogram": oracle_largest_rectangle_histogram,
    "circular_next_greater": oracle_circular_next_greater,
    "sum_subarray_minimums": oracle_sum_subarray_minimums,
    "sum_subarray_maximums": oracle_sum_subarray_maximums,
}
