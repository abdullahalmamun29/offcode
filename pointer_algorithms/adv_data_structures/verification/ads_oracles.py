"""
CHUP Phase 3S — Reference Python Oracles for Advanced Data Structures.

Independent golden Python reference implementations and algorithmic oracles for all 10
canonical patterns:
1. Sparse Table RMQ
2. LCA Binary Lifting
3. Heavy-Light Decomposition
4. Centroid Decomposition
5. Persistent Segment Tree
6. Dynamic Sparse Segment Tree
7. Merge Sort Tree
8. Sqrt Decomposition
9. Mo's Algorithm Offline Scheduler
10. Segment Tree Beats (Chmin)
"""

import math
import bisect
from typing import List, Tuple, Dict, Any, Optional, Set


# ── 1. Sparse Table RMQ Oracle (3S-A) ──

def oracle_sparse_table(
    arr: List[int],
    queries: List[Tuple[int, int]],
    op: str = "min"
) -> List[int]:
    """Reference oracle for static range queries on idempotent/associative arrays."""
    n = len(arr)
    if n == 0:
        return []

    log_table = [0] * (n + 1)
    for i in range(2, n + 1):
        log_table[i] = log_table[i // 2] + 1

    k_max = log_table[n] + 1
    st = [[0] * n for _ in range(k_max)]

    for i in range(n):
        st[0][i] = arr[i]

    def combine(a: int, b: int) -> int:
        if op == "min":
            return min(a, b)
        elif op == "max":
            return max(a, b)
        elif op == "gcd":
            return math.gcd(a, b)
        elif op == "and":
            return a & b
        elif op == "or":
            return a | b
        return min(a, b)

    for k in range(1, k_max):
        half = 1 << (k - 1)
        for i in range(n - (1 << k) + 1):
            st[k][i] = combine(st[k - 1][i], st[k - 1][i + half])

    results = []
    for l, r in queries:
        length = r - l + 1
        k = log_table[length]
        ans = combine(st[k][l], st[k][r - (1 << k) + 1])
        results.append(ans)
    return results


# ── 2. LCA Binary Lifting Oracle (3S-B) ──

def oracle_lca_binary_lifting(
    n: int,
    edges: List[Tuple[int, int]],
    queries: List[Tuple[int, int]],
    root: int = 0
) -> List[int]:
    """Reference oracle for Lowest Common Ancestor via binary lifting."""
    if n == 0:
        return []

    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    max_log = max(1, math.ceil(math.log2(n + 1)) + 1)
    up = [[root] * n for _ in range(max_log)]
    depth = [0] * n
    visited = [False] * n

    # BFS/DFS for depth and up[0]
    stack = [(root, root, 0)]
    visited[root] = True
    while stack:
        u, p, d = stack.pop()
        up[0][u] = p
        depth[u] = d
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                stack.append((v, u, d + 1))

    for k in range(1, max_log):
        for u in range(n):
            up[k][u] = up[k - 1][up[k - 1][u]]

    def get_lca(u: int, v: int) -> int:
        if depth[u] < depth[v]:
            u, v = v, u
        # Lift u to same depth as v
        diff = depth[u] - depth[v]
        for k in range(max_log):
            if (diff >> k) & 1:
                u = up[k][u]
        if u == v:
            return u
        # Lift both simultaneously
        for k in range(max_log - 1, -1, -1):
            if up[k][u] != up[k][v]:
                u = up[k][u]
                v = up[k][v]
        return up[0][u]

    return [get_lca(u, v) for u, v in queries]


# ── 3. Heavy-Light Decomposition Oracle (3S-C) ──

def oracle_heavy_light_decomposition(
    n: int,
    edges: List[Tuple[int, int]],
    values: List[int],
    queries: List[Tuple[str, int, int]], # ("query", u, v) or ("update", u, val)
    is_edge_values: bool = False,
    root: int = 0
) -> List[int]:
    """Reference oracle for tree path queries via HLD with linear range segment tree."""
    if n == 0:
        return []

    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    parent = [root] * n
    depth = [0] * n
    heavy = [-1] * n
    sz = [0] * n

    # DFS 1: Subtree sizes, depths, parents, heavy edges
    def dfs_sz(u: int, p: int, d: int):
        parent[u] = p
        depth[u] = d
        sz[u] = 1
        max_c_size = 0
        for v in adj[u]:
            if v != p:
                dfs_sz(v, u, d + 1)
                sz[u] += sz[v]
                if sz[v] > max_c_size:
                    max_c_size = sz[v]
                    heavy[u] = v

    dfs_sz(root, root, 0)

    # DFS 2: Chain heads and positions
    head = [root] * n
    pos = [0] * n
    cur_pos = 0

    def dfs_hld(u: int, h: int):
        nonlocal cur_pos
        head[u] = h
        pos[u] = cur_pos
        cur_pos += 1
        if heavy[u] != -1:
            dfs_hld(heavy[u], h)
        for v in adj[u]:
            if v != parent[u] and v != heavy[u]:
                dfs_hld(v, v)

    dfs_hld(root, root)

    # Base Segment Tree
    tree_vals = [0] * (4 * n + 1)

    def update_st(node: int, l: int, r: int, idx: int, val: int):
        if l == r:
            tree_vals[node] = val
            return
        mid = (l + r) // 2
        if idx <= mid:
            update_st(2 * node, l, mid, idx, val)
        else:
            update_st(2 * node + 1, mid + 1, r, idx, val)
        tree_vals[node] = tree_vals[2 * node] + tree_vals[2 * node + 1]

    def query_st(node: int, l: int, r: int, ql: int, qr: int) -> int:
        if ql > r or qr < l or ql > qr:
            return 0
        if ql <= l and r <= qr:
            return tree_vals[node]
        mid = (l + r) // 2
        return query_st(2 * node, l, mid, ql, qr) + query_st(2 * node + 1, mid + 1, r, ql, qr)

    for i in range(n):
        if not is_edge_values:
            update_st(1, 0, n - 1, pos[i], values[i])

    def query_path(u: int, v: int) -> int:
        res = 0
        while head[u] != head[v]:
            if depth[head[u]] > depth[head[v]]:
                u, v = v, u
            res += query_st(1, 0, n - 1, pos[head[v]], pos[v])
            v = parent[head[v]]
        if depth[u] > depth[v]:
            u, v = v, u
        if is_edge_values:
            if depth[u] < depth[v]:
                res += query_st(1, 0, n - 1, pos[u] + 1, pos[v])
        else:
            res += query_st(1, 0, n - 1, pos[u], pos[v])
        return res

    results = []
    for q in queries:
        if q[0] == "query":
            results.append(query_path(q[1], q[2]))
        elif q[0] == "update":
            u, val = q[1], q[2]
            update_st(1, 0, n - 1, pos[u], val)
    return results


# ── 4. Centroid Decomposition Oracle (3S-D) ──

def oracle_centroid_decomposition(
    n: int,
    edges: List[Tuple[int, int]]
) -> Tuple[List[int], List[int], Dict[int, Dict[int, int]]]:
    """
    Reference oracle for centroid tree decomposition.
    Returns (centroid_parent, centroid_depth, ancestor_distances).
    """
    if n == 0:
        return [], [], {}

    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    removed = [False] * n
    sz = [0] * n
    c_parent = [-1] * n
    c_depth = [0] * n
    dist_table: Dict[int, Dict[int, int]] = {i: {} for i in range(n)}

    def get_sizes(u: int, p: int) -> int:
        sz[u] = 1
        for v in adj[u]:
            if v != p and not removed[v]:
                sz[u] += get_sizes(v, u)
        return sz[u]

    def get_centroid(u: int, p: int, total: int) -> int:
        for v in adj[u]:
            if v != p and not removed[v] and sz[v] > total // 2:
                return get_centroid(v, u, total)
        return u

    def record_distances(u: int, p: int, d: int, centroid: int):
        dist_table[u][centroid] = d
        for v in adj[u]:
            if v != p and not removed[v]:
                record_distances(v, u, d + 1, centroid)

    def decompose(u: int, p: int, depth: int) -> int:
        total = get_sizes(u, -1)
        c = get_centroid(u, -1, total)
        removed[c] = True
        c_parent[c] = p
        c_depth[c] = depth

        record_distances(c, -1, 0, c)

        for v in adj[c]:
            if not removed[v]:
                decompose(v, c, depth + 1)
        return c

    root_c = decompose(0, -1, 0)
    return c_parent, c_depth, dist_table


# ── 5. Persistent Segment Tree Oracle (3S-E) ──

def oracle_persistent_segment_tree(
    initial_arr: List[int],
    updates: List[Tuple[int, int, int]],     # (parent_version, idx, val) -> spawns new version
    queries: List[Tuple[int, int, int]]      # (version, l, r)
) -> List[int]:
    """Reference oracle for path-copying persistent segment tree."""
    # Simple array-version tracking for golden truth
    versions = [list(initial_arr)]
    for p_ver, idx, val in updates:
        new_v = list(versions[p_ver])
        new_v[idx] = val
        versions.append(new_v)

    results = []
    for ver, l, r in queries:
        results.append(sum(versions[ver][l:r + 1]))
    return results


# ── 6. Dynamic Sparse Segment Tree Oracle (3S-F) ──

def oracle_dynamic_segment_tree(
    domain_lower: int,
    domain_upper: int,
    updates: List[Tuple[int, int]],         # (point, val)
    queries: List[Tuple[int, int]]          # (l, r)
) -> List[int]:
    """Reference oracle for dynamic sparse segment tree over large coordinate intervals."""
    # Map-based sparse truth for large domains
    data: Dict[int, int] = {}
    results = []

    for pt, val in updates:
        data[pt] = data.get(pt, 0) + val

    for ql, qr in queries:
        s = sum(v for pt, v in data.items() if ql <= pt <= qr)
        results.append(s)
    return results


# ── 7. Merge Sort Tree Oracle (3S-G) ──

def oracle_merge_sort_tree(
    arr: List[int],
    queries: List[Tuple[int, int, int]]     # (l, r, X) -> count <= X
) -> List[int]:
    """Reference oracle for Merge Sort Tree counting elements in [l, r] <= X."""
    results = []
    for l, r, x in queries:
        cnt = sum(1 for v in arr[l:r + 1] if v <= x)
        results.append(cnt)
    return results


# ── 8. Sqrt Decomposition Oracle (3S-H) ──

def oracle_sqrt_decomposition(
    arr: List[int],
    updates: List[Tuple[int, int, int]],    # (l, r, add_val)
    queries: List[Tuple[int, int]]         # (l, r) -> sum
) -> List[int]:
    """Reference oracle for sqrt block decomposition with range adds and sum queries."""
    data = list(arr)
    results = []
    for l, r, val in updates:
        for i in range(l, r + 1):
            data[i] += val

    for l, r in queries:
        results.append(sum(data[l:r + 1]))
    return results


# ── 9. Mo's Algorithm Oracle (3S-I) ──

def oracle_mos_algorithm(
    arr: List[int],
    queries: List[Tuple[int, int]],
    strategy: str = "STANDARD_BLOCK_SNAKE"
) -> List[int]:
    """
    Reference oracle for Mo's offline range query algorithm.
    Counts number of distinct elements in each range [L, R].
    """
    n = len(arr)
    q = len(queries)
    if n == 0 or q == 0:
        return []

    block_size = max(1, int(math.isqrt(n)))

    # Decorate queries with original index
    indexed_queries = [(queries[i][0], queries[i][1], i) for i in range(q)]

    if strategy == "STANDARD_BLOCK_SNAKE":
        indexed_queries.sort(key=lambda item: (
            item[0] // block_size,
            item[1] if (item[0] // block_size) % 2 == 0 else -item[1]
        ))
    else:
        indexed_queries.sort(key=lambda item: (item[0] // block_size, item[1]))

    freq: Dict[int, int] = {}
    distinct_count = 0

    def add(x: int):
        nonlocal distinct_count
        c = freq.get(x, 0)
        if c == 0:
            distinct_count += 1
        freq[x] = c + 1

    def remove(x: int):
        nonlocal distinct_count
        c = freq.get(x, 0)
        if c == 1:
            distinct_count -= 1
        freq[x] = c - 1

    cur_l = 0
    cur_r = -1
    ans = [0] * q

    for l, r, q_idx in indexed_queries:
        while cur_l > l:
            cur_l -= 1
            add(arr[cur_l])
        while cur_r < r:
            cur_r += 1
            add(arr[cur_r])
        while cur_l < l:
            remove(arr[cur_l])
            cur_l += 1
        while cur_r > r:
            remove(arr[cur_r])
            cur_r -= 1
        ans[q_idx] = distinct_count

    return ans


# ── 10. Segment Tree Beats Oracle (3S-J) ──

def oracle_segment_tree_beats(
    arr: List[int],
    operations: List[Tuple[str, int, int, Optional[int]]]
) -> List[int]:
    """
    Reference oracle for Segment Tree Beats (Range Chmin, Range Sum, Range Max).
    operations: list of ("chmin", l, r, v), ("query_sum", l, r, None), ("query_max", l, r, None).
    """
    data = list(arr)
    results = []

    for op, l, r, v in operations:
        if op == "chmin" and v is not None:
            for i in range(l, r + 1):
                if data[i] > v:
                    data[i] = v
        elif op == "query_sum":
            results.append(sum(data[l:r + 1]))
        elif op == "query_max":
            results.append(max(data[l:r + 1]))

    return results
