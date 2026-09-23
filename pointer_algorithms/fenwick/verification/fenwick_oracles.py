"""
Reference Oracles and Brute-Force Implementations for Fenwick Tree Domain (Phase 3I).

Provides clean, verifiable reference implementations for all 10 Fenwick patterns:
1. FenwickTreeOracle (point update, prefix & range query)
2. RangeUpdatePointQueryBITOracle (difference array BIT)
3. RangeUpdateRangeQueryBITOracle (two-Fenwick double difference)
4. FrequencyBITOracle (frequency tracking & cumulative counts)
5. PrefixExtremumBITOracle (prefix min / prefix max under monotonic updates)
6. Fenwick2DOracle (2D grid BIT with inclusion-exclusion range queries)
7. KthElementBITOracle (binary lifting on Fenwick frequencies)
8. FenwickInversionOracle (inversion counting with coordinate compression)
9. FenwickMultisetOracle (order-statistic multiset)
10. CoordinateCompressionBITOracle (sparse value normalization)

Includes matching brute-force reference oracles for differential testing.
"""

from typing import List, Tuple, Optional, Dict
import bisect
import math


# ── 1. Point Update, Prefix & Range Query Oracle ──

class FenwickTreeOracle:
    def __init__(self, n_or_array):
        if isinstance(n_or_array, int):
            self.n = n_or_array
            self.tree = [0] * (self.n + 1)
        else:
            # 1-based array initial build
            a = list(n_or_array)
            self.n = len(a) - 1
            self.tree = [0] * (self.n + 1)
            for i in range(1, self.n + 1):
                self.tree[i] += a[i]
                parent = i + (i & -i)
                if parent <= self.n:
                    self.tree[parent] += self.tree[i]

    def add(self, i: int, delta: int) -> None:
        if i <= 0:
            raise ValueError(f"Fenwick indexing must be 1-based, got {i}")
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def query(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s

    def range_query(self, l: int, r: int) -> int:
        if l > r:
            return 0
        return self.query(r) - self.query(l - 1)


class BruteForceArray:
    def __init__(self, n_or_array):
        if isinstance(n_or_array, int):
            self.n = n_or_array
            self.a = [0] * (self.n + 1)
        else:
            self.a = list(n_or_array)
            self.n = len(self.a) - 1

    def add(self, i: int, delta: int) -> None:
        self.a[i] += delta

    def query(self, i: int) -> int:
        return sum(self.a[1:i+1])

    def range_query(self, l: int, r: int) -> int:
        if l > r:
            return 0
        return sum(self.a[l:r+1])


# ── 2. Range Update, Point Query Oracle ──

class RangeUpdatePointQueryBITOracle:
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)

    def _add(self, i: int, delta: int) -> None:
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def range_add(self, l: int, r: int, delta: int) -> None:
        if l > r:
            return
        self._add(l, delta)
        self._add(r + 1, -delta)

    def point_query(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s


class BruteForceRangeAddPointQuery:
    def __init__(self, n: int):
        self.n = n
        self.a = [0] * (n + 1)

    def range_add(self, l: int, r: int, delta: int) -> None:
        for i in range(max(1, l), min(self.n, r) + 1):
            self.a[i] += delta

    def point_query(self, i: int) -> int:
        return self.a[i]


# ── 3. Range Update, Range Query Oracle (Two Fenwicks) ──

class RangeUpdateRangeQueryBITOracle:
    def __init__(self, n: int):
        self.n = n
        self.b1 = [0] * (n + 1)
        self.b2 = [0] * (n + 1)

    def _add(self, tree: List[int], i: int, delta: int) -> None:
        while i <= self.n:
            tree[i] += delta
            i += i & -i

    def _query(self, tree: List[int], i: int) -> int:
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    def range_add(self, l: int, r: int, delta: int) -> None:
        if l > r:
            return
        self._add(self.b1, l, delta)
        self._add(self.b1, r + 1, -delta)
        self._add(self.b2, l, delta * l)
        self._add(self.b2, r + 1, -delta * (r + 1))

    def prefix_query(self, x: int) -> int:
        if x <= 0:
            return 0
        return (x + 1) * self._query(self.b1, x) - self._query(self.b2, x)

    def range_query(self, l: int, r: int) -> int:
        if l > r:
            return 0
        return self.prefix_query(r) - self.prefix_query(l - 1)


class BruteForceRangeAddRangeQuery:
    def __init__(self, n: int):
        self.n = n
        self.a = [0] * (n + 1)

    def range_add(self, l: int, r: int, delta: int) -> None:
        for i in range(max(1, l), min(self.n, r) + 1):
            self.a[i] += delta

    def prefix_query(self, x: int) -> int:
        return sum(self.a[1:x+1])

    def range_query(self, l: int, r: int) -> int:
        if l > r:
            return 0
        return sum(self.a[l:r+1])


# ── 4. Frequency BIT Oracle ──

class FrequencyBITOracle:
    def __init__(self, max_val: int):
        self.max_val = max_val
        self.tree = [0] * (max_val + 1)

    def insert(self, val: int, count: int = 1) -> None:
        if val < 1 or val > self.max_val:
            return
        while val <= self.max_val:
            self.tree[val] += count
            val += val & -val

    def remove(self, val: int, count: int = 1) -> None:
        self.insert(val, -count)

    def count_leq(self, val: int) -> int:
        if val > self.max_val:
            val = self.max_val
        s = 0
        while val > 0:
            s += self.tree[val]
            val -= val & -val
        return s

    def count_range(self, low: int, high: int) -> int:
        if low > high:
            return 0
        return self.count_leq(high) - self.count_leq(low - 1)


class BruteForceFrequency:
    def __init__(self, max_val: int):
        self.max_val = max_val
        self.counts = [0] * (max_val + 1)

    def insert(self, val: int, count: int = 1) -> None:
        if 1 <= val <= self.max_val:
            self.counts[val] += count

    def remove(self, val: int, count: int = 1) -> None:
        if 1 <= val <= self.max_val:
            self.counts[val] -= count

    def count_leq(self, val: int) -> int:
        val = min(val, self.max_val)
        return sum(self.counts[1:val+1])

    def count_range(self, low: int, high: int) -> int:
        if low > high:
            return 0
        return sum(self.counts[max(1, low):min(self.max_val, high)+1])


# ── 5. Prefix Extremum Oracle (Monotonic updates) ──

class PrefixExtremumBITOracle:
    def __init__(self, n: int, is_min: bool = True):
        self.n = n
        self.is_min = is_min
        self.inf = float('inf') if is_min else float('-inf')
        self.tree = [self.inf] * (n + 1)

    def update(self, i: int, val: int) -> None:
        while i <= self.n:
            if self.is_min:
                self.tree[i] = min(self.tree[i], val)
            else:
                self.tree[i] = max(self.tree[i], val)
            i += i & -i

    def query_prefix(self, i: int) -> int:
        res = self.inf
        while i > 0:
            if self.is_min:
                res = min(res, self.tree[i])
            else:
                res = max(res, self.tree[i])
            i -= i & -i
        return res


class BruteForcePrefixExtremum:
    def __init__(self, n: int, is_min: bool = True):
        self.n = n
        self.is_min = is_min
        self.inf = float('inf') if is_min else float('-inf')
        self.a = [self.inf] * (n + 1)

    def update(self, i: int, val: int) -> None:
        if self.is_min:
            self.a[i] = min(self.a[i], val)
        else:
            self.a[i] = max(self.a[i], val)

    def query_prefix(self, i: int) -> int:
        res = self.inf
        for idx in range(1, i + 1):
            if self.is_min:
                res = min(res, self.a[idx])
            else:
                res = max(res, self.a[idx])
        return res


# ── 6. 2D Fenwick Grid Oracle ──

class Fenwick2DOracle:
    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.tree = [[0] * (m + 1) for _ in range(n + 1)]

    def add(self, r: int, c: int, delta: int) -> None:
        i = r
        while i <= self.n:
            j = c
            while j <= self.m:
                self.tree[i][j] += delta
                j += j & -j
            i += i & -i

    def query(self, r: int, c: int) -> int:
        if r <= 0 or c <= 0:
            return 0
        s = 0
        i = min(r, self.n)
        while i > 0:
            j = min(c, self.m)
            while j > 0:
                s += self.tree[i][j]
                j -= j & -j
            i -= i & -i
        return s

    def range_query(self, r1: int, c1: int, r2: int, c2: int) -> int:
        if r1 > r2 or c1 > c2:
            return 0
        return (
            self.query(r2, c2)
            - self.query(r1 - 1, c2)
            - self.query(r2, c1 - 1)
            + self.query(r1 - 1, c1 - 1)
        )


class BruteForce2DGrid:
    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.grid = [[0] * (m + 1) for _ in range(n + 1)]

    def add(self, r: int, c: int, delta: int) -> None:
        self.grid[r][c] += delta

    def query(self, r: int, c: int) -> int:
        s = 0
        for i in range(1, min(r, self.n) + 1):
            for j in range(1, min(c, self.m) + 1):
                s += self.grid[i][j]
        return s

    def range_query(self, r1: int, c1: int, r2: int, c2: int) -> int:
        s = 0
        for i in range(r1, r2 + 1):
            for j in range(c1, c2 + 1):
                s += self.grid[i][j]
        return s


# ── 7. K-th Element via Binary Lifting Oracle ──

class KthElementBITOracle:
    def __init__(self, max_val: int):
        self.max_val = max_val
        self.tree = [0] * (max_val + 1)

    def add(self, val: int, delta: int) -> None:
        while val <= self.max_val:
            self.tree[val] += delta
            val += val & -val

    def find_kth(self, k: int) -> int:
        idx = 0
        current_sum = 0
        max_step = 1
        while (max_step << 1) <= self.max_val:
            max_step <<= 1

        step = max_step
        while step > 0:
            if idx + step <= self.max_val and current_sum + self.tree[idx + step] < k:
                idx += step
                current_sum += self.tree[idx]
            step >>= 1
        return idx + 1


class BruteForceKthElement:
    def __init__(self, max_val: int):
        self.max_val = max_val
        self.counts = [0] * (max_val + 1)

    def add(self, val: int, delta: int) -> None:
        self.counts[val] += delta

    def find_kth(self, k: int) -> int:
        running = 0
        for i in range(1, self.max_val + 1):
            running += self.counts[i]
            if running >= k:
                return i
        return self.max_val + 1


# ── 8. Inversion Counting Oracle ──

class FenwickInversionOracle:
    @staticmethod
    def count_inversions(arr: List[int]) -> int:
        if not arr:
            return 0
        # Coordinate compression
        unique_sorted = sorted(set(arr))
        rank_map = {val: i + 1 for i, val in enumerate(unique_sorted)}
        m = len(unique_sorted)

        ft = FenwickTreeOracle(m)
        inv_count = 0
        # Sweep right-to-left: count elements strictly smaller than arr[i] seen so far
        for val in reversed(arr):
            rank = rank_map[val]
            inv_count += ft.query(rank - 1)
            ft.add(rank, 1)
        return inv_count


class BruteForceInversions:
    @staticmethod
    def count_inversions(arr: List[int]) -> int:
        count = 0
        n = len(arr)
        for i in range(n):
            for j in range(i + 1, n):
                if arr[i] > arr[j]:
                    count += 1
        return count


# ── 9. Order-Statistic Multiset Oracle ──

class FenwickMultisetOracle:
    def __init__(self, max_val: int):
        self.max_val = max_val
        self.tree = [0] * (max_val + 1)
        self.total_size = 0

    def insert(self, x: int, cnt: int = 1) -> None:
        if x < 1 or x > self.max_val:
            return
        self.total_size += cnt
        i = x
        while i <= self.max_val:
            self.tree[i] += cnt
            i += i & -i

    def erase(self, x: int, cnt: int = 1) -> bool:
        if x < 1 or x > self.max_val:
            return False
        if self.count(x) < cnt:
            return False
        self.total_size -= cnt
        i = x
        while i <= self.max_val:
            self.tree[i] -= cnt
            i += i & -i
        return True

    def query(self, x: int) -> int:
        if x > self.max_val:
            x = self.max_val
        s = 0
        while x > 0:
            s += self.tree[x]
            x -= x & -x
        return s

    def count(self, x: int) -> int:
        if x < 1 or x > self.max_val:
            return 0
        return self.query(x) - self.query(x - 1)

    def rank(self, x: int) -> int:
        # 1-based rank: number of elements strictly smaller + 1
        if x <= 1:
            return 1
        return self.query(x - 1) + 1

    def select(self, k: int) -> int:
        if k < 1 or k > self.total_size:
            return -1
        idx = 0
        current_sum = 0
        max_step = 1
        while (max_step << 1) <= self.max_val:
            max_step <<= 1

        step = max_step
        while step > 0:
            if idx + step <= self.max_val and current_sum + self.tree[idx + step] < k:
                idx += step
                current_sum += self.tree[idx]
            step >>= 1
        return idx + 1

    def size(self) -> int:
        return self.total_size


class BruteForceMultiset:
    def __init__(self, max_val: int):
        self.max_val = max_val
        self.elements: List[int] = []

    def insert(self, x: int, cnt: int = 1) -> None:
        for _ in range(cnt):
            self.elements.append(x)
        self.elements.sort()

    def erase(self, x: int, cnt: int = 1) -> bool:
        if self.elements.count(x) < cnt:
            return False
        for _ in range(cnt):
            self.elements.remove(x)
        return True

    def count(self, x: int) -> int:
        return self.elements.count(x)

    def rank(self, x: int) -> int:
        return sum(1 for e in self.elements if e < x) + 1

    def select(self, k: int) -> int:
        if 1 <= k <= len(self.elements):
            return self.elements[k - 1]
        return -1

    def size(self) -> int:
        return len(self.elements)


# ── 10. Coordinate Compression Oracle ──

class CoordinateCompressorOracle:
    def __init__(self):
        self.raw_coords: List[int] = []
        self.unique_sorted: List[int] = []

    def add(self, x: int) -> None:
        self.raw_coords.append(x)

    def build(self) -> None:
        self.unique_sorted = sorted(set(self.raw_coords))

    def get_rank(self, x: int) -> int:
        return bisect.bisect_left(self.unique_sorted, x) + 1

    def get_val(self, rank: int) -> int:
        return self.unique_sorted[rank - 1]

    def size(self) -> int:
        return len(self.unique_sorted)
