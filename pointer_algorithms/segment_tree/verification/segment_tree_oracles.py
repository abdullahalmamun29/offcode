"""
Reference Oracles and Brute-Force Implementations for Segment Tree Domain (Phase 3J).

Provides clean, verifiable reference implementations for all 8 Segment Tree patterns:
1. SegmentTreeOracle (point update, range query for sum, min, max, gcd)
2. LazyRangeAddSegmentTreeOracle (range add, range sum query)
3. LazyRangeAssignSegmentTreeOracle (range assign, range sum query)
4. CombinedLazySegmentTreeOracle (range assign + range add, range sum query)
5. MetadataSegmentTreeOracle (point update, simultaneous sum, min, max, count)
6. MaxSubarraySegmentTreeOracle (point update, maximum non-empty contiguous subarray sum)
7. FrequencySegmentTreeOracle (point update frequency, k-th element tree walk)
8. IntervalStatisticsSegmentTreeOracle (point update, extrema with multiplicity)

Includes matching brute-force reference oracles for differential testing.
"""

from typing import List, Tuple, Optional, Dict, Any
import math


# ── 1. Point Update, Range Query Oracle ──

class SegmentTreeOracle:
    def __init__(self, n_or_array, op: str = "sum"):
        self.op = op
        if isinstance(n_or_array, int):
            self.n = n_or_array
            self.a = [0] * (self.n + 1)
        else:
            self.a = list(n_or_array)
            self.n = len(self.a) - 1

        self.tree = [self._identity()] * (4 * self.n + 1)
        if self.n > 0:
            self._build(1, 1, self.n)

    def _identity(self) -> int:
        if self.op == "min":
            return math.inf
        elif self.op == "max":
            return -math.inf
        elif self.op == "gcd":
            return 0
        return 0

    def _merge(self, a: int, b: int) -> int:
        if a == math.inf or a == -math.inf:
            return b
        if b == math.inf or b == -math.inf:
            return a
        if self.op == "min":
            return min(a, b)
        elif self.op == "max":
            return max(a, b)
        elif self.op == "gcd":
            return math.gcd(a, b)
        return a + b

    def _build(self, p: int, l: int, r: int) -> None:
        if l == r:
            self.tree[p] = self.a[l]
            return
        mid = (l + r) // 2
        self._build(2 * p, l, mid)
        self._build(2 * p + 1, mid + 1, r)
        self.tree[p] = self._merge(self.tree[2 * p], self.tree[2 * p + 1])

    def update(self, idx: int, val: int) -> None:
        self.a[idx] = val
        self._update(1, 1, self.n, idx, val)

    def _update(self, p: int, l: int, r: int, idx: int, val: int) -> None:
        if l == r:
            self.tree[p] = val
            return
        mid = (l + r) // 2
        if idx <= mid:
            self._update(2 * p, l, mid, idx, val)
        else:
            self._update(2 * p + 1, mid + 1, r, idx, val)
        self.tree[p] = self._merge(self.tree[2 * p], self.tree[2 * p + 1])

    def query(self, ql: int, qr: int) -> int:
        if ql > qr:
            return self._identity()
        return self._query(1, 1, self.n, ql, qr)

    def _query(self, p: int, l: int, r: int, ql: int, qr: int) -> int:
        if ql <= l and r <= qr:
            return self.tree[p]
        mid = (l + r) // 2
        res = self._identity()
        if ql <= mid:
            res = self._merge(res, self._query(2 * p, l, mid, ql, qr))
        if qr > mid:
            res = self._merge(res, self._query(2 * p + 1, mid + 1, r, ql, qr))
        return res


class BruteForcePointUpdateRangeQuery:
    def __init__(self, n_or_array, op: str = "sum"):
        self.op = op
        if isinstance(n_or_array, int):
            self.n = n_or_array
            self.a = [0] * (self.n + 1)
        else:
            self.a = list(n_or_array)
            self.n = len(self.a) - 1

    def update(self, idx: int, val: int) -> None:
        self.a[idx] = val

    def query(self, ql: int, qr: int) -> int:
        if ql > qr:
            return 0 if self.op != "min" and self.op != "max" else (math.inf if self.op == "min" else -math.inf)
        sub = self.a[ql:qr + 1]
        if self.op == "min":
            return min(sub)
        elif self.op == "max":
            return max(sub)
        elif self.op == "gcd":
            res = 0
            for x in sub:
                res = math.gcd(res, x)
            return res
        return sum(sub)


# ── 2. Range Add Range Query Oracle ──

class LazyRangeAddSegmentTreeOracle:
    def __init__(self, n_or_array):
        if isinstance(n_or_array, int):
            self.n = n_or_array
            self.a = [0] * (self.n + 1)
        else:
            self.a = list(n_or_array)
            self.n = len(self.a) - 1

        self.tree = [0] * (4 * self.n + 1)
        self.lazy = [0] * (4 * self.n + 1)
        if self.n > 0:
            self._build(1, 1, self.n)

    def _build(self, p: int, l: int, r: int) -> None:
        if l == r:
            self.tree[p] = self.a[l]
            return
        mid = (l + r) // 2
        self._build(2 * p, l, mid)
        self._build(2 * p + 1, mid + 1, r)
        self.tree[p] = self.tree[2 * p] + self.tree[2 * p + 1]

    def _apply_add(self, p: int, l: int, r: int, val: int) -> None:
        self.tree[p] += (r - l + 1) * val
        self.lazy[p] += val

    def _push_down(self, p: int, l: int, r: int) -> None:
        if self.lazy[p] != 0:
            mid = (l + r) // 2
            self._apply_add(2 * p, l, mid, self.lazy[p])
            self._apply_add(2 * p + 1, mid + 1, r, self.lazy[p])
            self.lazy[p] = 0

    def range_add(self, ql: int, qr: int, val: int) -> None:
        if ql <= qr:
            self._range_add(1, 1, self.n, ql, qr, val)

    def _range_add(self, p: int, l: int, r: int, ql: int, qr: int, val: int) -> None:
        if ql <= l and r <= qr:
            self._apply_add(p, l, r, val)
            return
        self._push_down(p, l, r)
        mid = (l + r) // 2
        if ql <= mid:
            self._range_add(2 * p, l, mid, ql, qr, val)
        if qr > mid:
            self._range_add(2 * p + 1, mid + 1, r, ql, qr, val)
        self.tree[p] = self.tree[2 * p] + self.tree[2 * p + 1]

    def range_query(self, ql: int, qr: int) -> int:
        if ql > qr:
            return 0
        return self._range_query(1, 1, self.n, ql, qr)

    def _range_query(self, p: int, l: int, r: int, ql: int, qr: int) -> int:
        if ql <= l and r <= qr:
            return self.tree[p]
        self._push_down(p, l, r)
        mid = (l + r) // 2
        s = 0
        if ql <= mid:
            s += self._range_query(2 * p, l, mid, ql, qr)
        if qr > mid:
            s += self._range_query(2 * p + 1, mid + 1, r, ql, qr)
        return s


class BruteForceRangeAdd:
    def __init__(self, n_or_array):
        if isinstance(n_or_array, int):
            self.n = n_or_array
            self.a = [0] * (self.n + 1)
        else:
            self.a = list(n_or_array)
            self.n = len(self.a) - 1

    def range_add(self, ql: int, qr: int, val: int) -> None:
        for i in range(ql, qr + 1):
            self.a[i] += val

    def range_query(self, ql: int, qr: int) -> int:
        if ql > qr:
            return 0
        return sum(self.a[ql:qr + 1])


# ── 3. Range Assign Range Query Oracle ──

class LazyRangeAssignSegmentTreeOracle:
    def __init__(self, n_or_array):
        if isinstance(n_or_array, int):
            self.n = n_or_array
            self.a = [0] * (self.n + 1)
        else:
            self.a = list(n_or_array)
            self.n = len(self.a) - 1

        self.tree = [0] * (4 * self.n + 1)
        self.assign_val = [0] * (4 * self.n + 1)
        self.has_assign = [False] * (4 * self.n + 1)
        if self.n > 0:
            self._build(1, 1, self.n)

    def _build(self, p: int, l: int, r: int) -> None:
        if l == r:
            self.tree[p] = self.a[l]
            return
        mid = (l + r) // 2
        self._build(2 * p, l, mid)
        self._build(2 * p + 1, mid + 1, r)
        self.tree[p] = self.tree[2 * p] + self.tree[2 * p + 1]

    def _apply_assign(self, p: int, l: int, r: int, val: int) -> None:
        self.tree[p] = (r - l + 1) * val
        self.assign_val[p] = val
        self.has_assign[p] = True

    def _push_down(self, p: int, l: int, r: int) -> None:
        if self.has_assign[p]:
            mid = (l + r) // 2
            self._apply_assign(2 * p, l, mid, self.assign_val[p])
            self._apply_assign(2 * p + 1, mid + 1, r, self.assign_val[p])
            self.has_assign[p] = False

    def range_assign(self, ql: int, qr: int, val: int) -> None:
        if ql <= qr:
            self._range_assign(1, 1, self.n, ql, qr, val)

    def _range_assign(self, p: int, l: int, r: int, ql: int, qr: int, val: int) -> None:
        if ql <= l and r <= qr:
            self._apply_assign(p, l, r, val)
            return
        self._push_down(p, l, r)
        mid = (l + r) // 2
        if ql <= mid:
            self._range_assign(2 * p, l, mid, ql, qr, val)
        if qr > mid:
            self._range_assign(2 * p + 1, mid + 1, r, ql, qr, val)
        self.tree[p] = self.tree[2 * p] + self.tree[2 * p + 1]

    def range_query(self, ql: int, qr: int) -> int:
        if ql > qr:
            return 0
        return self._range_query(1, 1, self.n, ql, qr)

    def _range_query(self, p: int, l: int, r: int, ql: int, qr: int) -> int:
        if ql <= l and r <= qr:
            return self.tree[p]
        self._push_down(p, l, r)
        mid = (l + r) // 2
        s = 0
        if ql <= mid:
            s += self._range_query(2 * p, l, mid, ql, qr)
        if qr > mid:
            s += self._range_query(2 * p + 1, mid + 1, r, ql, qr)
        return s


class BruteForceRangeAssign:
    def __init__(self, n_or_array):
        if isinstance(n_or_array, int):
            self.n = n_or_array
            self.a = [0] * (self.n + 1)
        else:
            self.a = list(n_or_array)
            self.n = len(self.a) - 1

    def range_assign(self, ql: int, qr: int, val: int) -> None:
        for i in range(ql, qr + 1):
            self.a[i] = val

    def range_query(self, ql: int, qr: int) -> int:
        if ql > qr:
            return 0
        return sum(self.a[ql:qr + 1])


# ── 4. Combined Lazy Range Query Oracle ──

class CombinedLazySegmentTreeOracle:
    class Tag:
        def __init__(self, has_assign: bool = False, assign_val: int = 0, add_val: int = 0):
            self.has_assign = has_assign
            self.assign_val = assign_val
            self.add_val = add_val

    def __init__(self, n_or_array):
        if isinstance(n_or_array, int):
            self.n = n_or_array
            self.a = [0] * (self.n + 1)
        else:
            self.a = list(n_or_array)
            self.n = len(self.a) - 1

        self.tree = [0] * (4 * self.n + 1)
        self.lazy = [self.Tag() for _ in range(4 * self.n + 1)]
        if self.n > 0:
            self._build(1, 1, self.n)

    def _build(self, p: int, l: int, r: int) -> None:
        if l == r:
            self.tree[p] = self.a[l]
            return
        mid = (l + r) // 2
        self._build(2 * p, l, mid)
        self._build(2 * p + 1, mid + 1, r)
        self.tree[p] = self.tree[2 * p] + self.tree[2 * p + 1]

    def _apply_tag(self, p: int, l: int, r: int, tag: Tag) -> None:
        if tag.has_assign:
            self.tree[p] = (r - l + 1) * tag.assign_val
            self.lazy[p].has_assign = True
            self.lazy[p].assign_val = tag.assign_val
            self.lazy[p].add_val = 0
        if tag.add_val != 0:
            self.tree[p] += (r - l + 1) * tag.add_val
            if self.lazy[p].has_assign:
                self.lazy[p].assign_val += tag.add_val
            else:
                self.lazy[p].add_val += tag.add_val

    def _push_down(self, p: int, l: int, r: int) -> None:
        if self.lazy[p].has_assign or self.lazy[p].add_val != 0:
            mid = (l + r) // 2
            self._apply_tag(2 * p, l, mid, self.lazy[p])
            self._apply_tag(2 * p + 1, mid + 1, r, self.lazy[p])
            self.lazy[p] = self.Tag()

    def range_assign(self, ql: int, qr: int, val: int) -> None:
        if ql <= qr:
            self._range_assign(1, 1, self.n, ql, qr, val)

    def _range_assign(self, p: int, l: int, r: int, ql: int, qr: int, val: int) -> None:
        if ql <= l and r <= qr:
            self._apply_tag(p, l, r, self.Tag(has_assign=True, assign_val=val, add_val=0))
            return
        self._push_down(p, l, r)
        mid = (l + r) // 2
        if ql <= mid:
            self._range_assign(2 * p, l, mid, ql, qr, val)
        if qr > mid:
            self._range_assign(2 * p + 1, mid + 1, r, ql, qr, val)
        self.tree[p] = self.tree[2 * p] + self.tree[2 * p + 1]

    def range_add(self, ql: int, qr: int, val: int) -> None:
        if ql <= qr:
            self._range_add(1, 1, self.n, ql, qr, val)

    def _range_add(self, p: int, l: int, r: int, ql: int, qr: int, val: int) -> None:
        if ql <= l and r <= qr:
            self._apply_tag(p, l, r, self.Tag(has_assign=False, assign_val=0, add_val=val))
            return
        self._push_down(p, l, r)
        mid = (l + r) // 2
        if ql <= mid:
            self._range_add(2 * p, l, mid, ql, qr, val)
        if qr > mid:
            self._range_add(2 * p + 1, mid + 1, r, ql, qr, val)
        self.tree[p] = self.tree[2 * p] + self.tree[2 * p + 1]

    def range_query(self, ql: int, qr: int) -> int:
        if ql > qr:
            return 0
        return self._range_query(1, 1, self.n, ql, qr)

    def _range_query(self, p: int, l: int, r: int, ql: int, qr: int) -> int:
        if ql <= l and r <= qr:
            return self.tree[p]
        self._push_down(p, l, r)
        mid = (l + r) // 2
        s = 0
        if ql <= mid:
            s += self._range_query(2 * p, l, mid, ql, qr)
        if qr > mid:
            s += self._range_query(2 * p + 1, mid + 1, r, ql, qr)
        return s


class BruteForceCombinedLazy:
    def __init__(self, n_or_array):
        if isinstance(n_or_array, int):
            self.n = n_or_array
            self.a = [0] * (self.n + 1)
        else:
            self.a = list(n_or_array)
            self.n = len(self.a) - 1

    def range_assign(self, ql: int, qr: int, val: int) -> None:
        for i in range(ql, qr + 1):
            self.a[i] = val

    def range_add(self, ql: int, qr: int, val: int) -> None:
        for i in range(ql, qr + 1):
            self.a[i] += val

    def range_query(self, ql: int, qr: int) -> int:
        if ql > qr:
            return 0
        return sum(self.a[ql:qr + 1])


# ── 5. Metadata Aggregate Oracle ──

class MetadataSegmentTreeOracle:
    def __init__(self, n_or_array):
        if isinstance(n_or_array, int):
            self.n = n_or_array
            self.a = [0] * (self.n + 1)
        else:
            self.a = list(n_or_array)
            self.n = len(self.a) - 1

        self.tree_sum = [0] * (4 * self.n + 1)
        self.tree_min = [math.inf] * (4 * self.n + 1)
        self.tree_max = [-math.inf] * (4 * self.n + 1)
        self.tree_cnt = [0] * (4 * self.n + 1)
        if self.n > 0:
            self._build(1, 1, self.n)

    def _build(self, p: int, l: int, r: int) -> None:
        if l == r:
            self.tree_sum[p] = self.a[l]
            self.tree_min[p] = self.a[l]
            self.tree_max[p] = self.a[l]
            self.tree_cnt[p] = 1
            return
        mid = (l + r) // 2
        self._build(2 * p, l, mid)
        self._build(2 * p + 1, mid + 1, r)
        self._pull(p)

    def _pull(self, p: int) -> None:
        lp, rp = 2 * p, 2 * p + 1
        self.tree_sum[p] = self.tree_sum[lp] + self.tree_sum[rp]
        self.tree_min[p] = min(self.tree_min[lp], self.tree_min[rp])
        self.tree_max[p] = max(self.tree_max[lp], self.tree_max[rp])
        self.tree_cnt[p] = self.tree_cnt[lp] + self.tree_cnt[rp]

    def update(self, idx: int, val: int) -> None:
        self.a[idx] = val
        self._update(1, 1, self.n, idx, val)

    def _update(self, p: int, l: int, r: int, idx: int, val: int) -> None:
        if l == r:
            self.tree_sum[p] = val
            self.tree_min[p] = val
            self.tree_max[p] = val
            self.tree_cnt[p] = 1
            return
        mid = (l + r) // 2
        if idx <= mid:
            self._update(2 * p, l, mid, idx, val)
        else:
            self._update(2 * p + 1, mid + 1, r, idx, val)
        self._pull(p)

    def query(self, ql: int, qr: int) -> Tuple[int, int, int, int]:
        if ql > qr:
            return (0, math.inf, -math.inf, 0)
        return self._query(1, 1, self.n, ql, qr)

    def _query(self, p: int, l: int, r: int, ql: int, qr: int) -> Tuple[int, int, int, int]:
        if ql <= l and r <= qr:
            return (self.tree_sum[p], self.tree_min[p], self.tree_max[p], self.tree_cnt[p])
        mid = (l + r) // 2
        s, mn, mx, cnt = 0, math.inf, -math.inf, 0
        if ql <= mid:
            ls, lmn, lmx, lcnt = self._query(2 * p, l, mid, ql, qr)
            s += ls
            mn = min(mn, lmn)
            mx = max(mx, lmx)
            cnt += lcnt
        if qr > mid:
            rs, rmn, rmx, rcnt = self._query(2 * p + 1, mid + 1, r, ql, qr)
            s += rs
            mn = min(mn, rmn)
            mx = max(mx, rmx)
            cnt += rcnt
        return (s, mn, mx, cnt)


class BruteForceMetadata:
    def __init__(self, n_or_array):
        if isinstance(n_or_array, int):
            self.n = n_or_array
            self.a = [0] * (self.n + 1)
        else:
            self.a = list(n_or_array)
            self.n = len(self.a) - 1

    def update(self, idx: int, val: int) -> None:
        self.a[idx] = val

    def query(self, ql: int, qr: int) -> Tuple[int, int, int, int]:
        if ql > qr:
            return (0, math.inf, -math.inf, 0)
        sub = self.a[ql:qr + 1]
        return (sum(sub), min(sub), max(sub), len(sub))


# ── 6. Maximum Subarray Sum Oracle ──

class MaxSubarraySegmentTreeOracle:
    class Node:
        def __init__(self, s: int = 0, pref: int = 0, suff: int = 0, ans: int = 0, empty: bool = True):
            self.s = s
            self.pref = pref
            self.suff = suff
            self.ans = ans
            self.empty = empty

    def __init__(self, n_or_array):
        if isinstance(n_or_array, int):
            self.n = n_or_array
            self.a = [0] * (self.n + 1)
        else:
            self.a = list(n_or_array)
            self.n = len(self.a) - 1

        self.tree = [self.Node() for _ in range(4 * self.n + 1)]
        if self.n > 0:
            self._build(1, 1, self.n)

    def _merge(self, L: Node, R: Node) -> Node:
        if L.empty:
            return R
        if R.empty:
            return L
        res = self.Node()
        res.empty = False
        res.s = L.s + R.s
        res.pref = max(L.pref, L.s + R.pref)
        res.suff = max(R.suff, R.s + L.suff)
        res.ans = max(L.ans, R.ans, L.suff + R.pref)
        return res

    def _build(self, p: int, l: int, r: int) -> None:
        if l == r:
            v = self.a[l]
            self.tree[p] = self.Node(s=v, pref=v, suff=v, ans=v, empty=False)
            return
        mid = (l + r) // 2
        self._build(2 * p, l, mid)
        self._build(2 * p + 1, mid + 1, r)
        self.tree[p] = self._merge(self.tree[2 * p], self.tree[2 * p + 1])

    def update(self, idx: int, val: int) -> None:
        self.a[idx] = val
        self._update(1, 1, self.n, idx, val)

    def _update(self, p: int, l: int, r: int, idx: int, val: int) -> None:
        if l == r:
            self.tree[p] = self.Node(s=val, pref=val, suff=val, ans=val, empty=False)
            return
        mid = (l + r) // 2
        if idx <= mid:
            self._update(2 * p, l, mid, idx, val)
        else:
            self._update(2 * p + 1, mid + 1, r, idx, val)
        self.tree[p] = self._merge(self.tree[2 * p], self.tree[2 * p + 1])

    def query(self, ql: int, qr: int) -> int:
        if ql > qr:
            return 0
        return self._query(1, 1, self.n, ql, qr).ans

    def _query(self, p: int, l: int, r: int, ql: int, qr: int) -> Node:
        if ql <= l and r <= qr:
            return self.tree[p]
        mid = (l + r) // 2
        res = self.Node()
        if ql <= mid:
            res = self._merge(res, self._query(2 * p, l, mid, ql, qr))
        if qr > mid:
            res = self._merge(res, self._query(2 * p + 1, mid + 1, r, ql, qr))
        return res


class BruteForceMaxSubarray:
    def __init__(self, n_or_array):
        if isinstance(n_or_array, int):
            self.n = n_or_array
            self.a = [0] * (self.n + 1)
        else:
            self.a = list(n_or_array)
            self.n = len(self.a) - 1

    def update(self, idx: int, val: int) -> None:
        self.a[idx] = val

    def query(self, ql: int, qr: int) -> int:
        if ql > qr:
            return 0
        best = -math.inf
        # Non-empty contiguous subarray
        for i in range(ql, qr + 1):
            cur = 0
            for j in range(i, qr + 1):
                cur += self.a[j]
                if cur > best:
                    best = cur
        return best


# ── 7. Frequency Order Statistic Oracle ──

class FrequencySegmentTreeOracle:
    def __init__(self, max_val: int):
        self.max_val = max_val
        self.tree = [0] * (4 * max_val + 1)

    def add(self, val: int, count: int) -> None:
        self._add(1, 1, self.max_val, val, count)

    def _add(self, p: int, l: int, r: int, val: int, count: int) -> None:
        self.tree[p] += count
        if l == r:
            return
        mid = (l + r) // 2
        if val <= mid:
            self._add(2 * p, l, mid, val, count)
        else:
            self._add(2 * p + 1, mid + 1, r, val, count)

    def query_kth(self, k: int) -> int:
        if k < 1 or k > self.tree[1]:
            return -1
        return self._find_kth(1, 1, self.max_val, k)

    def _find_kth(self, p: int, l: int, r: int, k: int) -> int:
        if l == r:
            return l
        mid = (l + r) // 2
        if self.tree[2 * p] >= k:
            return self._find_kth(2 * p, l, mid, k)
        else:
            return self._find_kth(2 * p + 1, mid + 1, r, k - self.tree[2 * p])


class BruteForceFrequencyKth:
    def __init__(self, max_val: int):
        self.max_val = max_val
        self.freq = [0] * (max_val + 1)

    def add(self, val: int, count: int) -> None:
        self.freq[val] += count

    def query_kth(self, k: int) -> int:
        cum = 0
        for v in range(1, self.max_val + 1):
            cum += self.freq[v]
            if cum >= k:
                return v
        return -1


# ── 8. Interval Statistics Oracle ──

class IntervalStatisticsSegmentTreeOracle:
    class Node:
        def __init__(self, mn: int = math.inf, mnc: int = 0, mx: int = -math.inf, mxc: int = 0):
            self.mn = mn
            self.mnc = mnc
            self.mx = mx
            self.mxc = mxc

    def __init__(self, n_or_array):
        if isinstance(n_or_array, int):
            self.n = n_or_array
            self.a = [0] * (self.n + 1)
        else:
            self.a = list(n_or_array)
            self.n = len(self.a) - 1

        self.tree = [self.Node() for _ in range(4 * self.n + 1)]
        if self.n > 0:
            self._build(1, 1, self.n)

    def _merge(self, L: Node, R: Node) -> Node:
        if L.mnc == 0:
            return R
        if R.mnc == 0:
            return L

        if L.mn < R.mn:
            res_mn, res_mnc = L.mn, L.mnc
        elif L.mn > R.mn:
            res_mn, res_mnc = R.mn, R.mnc
        else:
            res_mn, res_mnc = L.mn, L.mnc + R.mnc

        if L.mx > R.mx:
            res_mx, res_mxc = L.mx, L.mxc
        elif L.mx < R.mx:
            res_mx, res_mxc = R.mx, R.mxc
        else:
            res_mx, res_mxc = L.mx, L.mxc + R.mxc

        return self.Node(mn=res_mn, mnc=res_mnc, mx=res_mx, mxc=res_mxc)

    def _build(self, p: int, l: int, r: int) -> None:
        if l == r:
            v = self.a[l]
            self.tree[p] = self.Node(mn=v, mnc=1, mx=v, mxc=1)
            return
        mid = (l + r) // 2
        self._build(2 * p, l, mid)
        self._build(2 * p + 1, mid + 1, r)
        self.tree[p] = self._merge(self.tree[2 * p], self.tree[2 * p + 1])

    def update(self, idx: int, val: int) -> None:
        self.a[idx] = val
        self._update(1, 1, self.n, idx, val)

    def _update(self, p: int, l: int, r: int, idx: int, val: int) -> None:
        if l == r:
            self.tree[p] = self.Node(mn=val, mnc=1, mx=val, mxc=1)
            return
        mid = (l + r) // 2
        if idx <= mid:
            self._update(2 * p, l, mid, idx, val)
        else:
            self._update(2 * p + 1, mid + 1, r, idx, val)
        self.tree[p] = self._merge(self.tree[2 * p], self.tree[2 * p + 1])

    def query(self, ql: int, qr: int) -> Tuple[int, int, int, int]:
        if ql > qr:
            return (math.inf, 0, -math.inf, 0)
        node = self._query(1, 1, self.n, ql, qr)
        return (node.mn, node.mnc, node.mx, node.mxc)

    def _query(self, p: int, l: int, r: int, ql: int, qr: int) -> Node:
        if ql <= l and r <= qr:
            return self.tree[p]
        mid = (l + r) // 2
        res = self.Node()
        if ql <= mid:
            res = self._merge(res, self._query(2 * p, l, mid, ql, qr))
        if qr > mid:
            res = self._merge(res, self._query(2 * p + 1, mid + 1, r, ql, qr))
        return res


class BruteForceIntervalStatistics:
    def __init__(self, n_or_array):
        if isinstance(n_or_array, int):
            self.n = n_or_array
            self.a = [0] * (self.n + 1)
        else:
            self.a = list(n_or_array)
            self.n = len(self.a) - 1

    def update(self, idx: int, val: int) -> None:
        self.a[idx] = val

    def query(self, ql: int, qr: int) -> Tuple[int, int, int, int]:
        if ql > qr:
            return (math.inf, 0, -math.inf, 0)
        sub = self.a[ql:qr + 1]
        mn = min(sub)
        mx = max(sub)
        mnc = sub.count(mn)
        mxc = sub.count(mx)
        return (mn, mnc, mx, mxc)
