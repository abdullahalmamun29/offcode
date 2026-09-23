"""
CHUP Phase 4: Independent Verification Reference Oracles.

STRICT POLICY §31:
Oracles must NOT use the same algorithmic decomposition that the production
system is testing:
1. MST Kruskal production -> Prim algorithm or brute-force spanning tree oracle.
2. Dijkstra production -> Bellman-Ford / Floyd-Warshall oracle.
3. DP Acceleration production -> Direct O(N^2) quadratic DP oracle.
4. Convex DP Monotone Queue production -> Direct O(N * K) brute-force oracle.
5. Bisection production -> Linear search oracle.
6. Event scheduling -> Sweep-line maximum overlap point oracle.
"""

from typing import List, Tuple, Optional, Dict, Any
import math


class CrossFamilyOracles:

    @staticmethod
    def mst_prim(n: int, edges: List[Tuple[int, int, int]]) -> Tuple[bool, int]:
        """
        Prim's algorithm independent oracle for Minimum Spanning Forest/Tree.
        Edges: (u, v, w), 1-based vertices.
        """
        adj: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, n + 1)}
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        visited = set([1])
        total_weight = 0
        edge_count = 0

        while len(visited) < n:
            min_w = float('inf')
            best_u, best_v = -1, -1
            for u in visited:
                for v, w in adj[u]:
                    if v not in visited and w < min_w:
                        min_w = w
                        best_u, best_v = u, v
            if best_v == -1:
                # Disconnected graph -> spanning forest on component
                return False, total_weight
            visited.add(best_v)
            total_weight += min_w
            edge_count += 1

        return True, total_weight

    @staticmethod
    def dijkstra_bellman_ford(n: int, edges: List[Tuple[int, int, int]], src: int = 1) -> Tuple[bool, List[int]]:
        """
        Bellman-Ford independent oracle for single-source shortest path.
        Returns (has_no_negative_cycle, dist_array).
        """
        INF = 10**15
        dist = [INF] * (n + 1)
        dist[src] = 0

        for _ in range(n - 1):
            updated = False
            for u, v, w in edges:
                if dist[u] != INF and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True
            if not updated:
                break

        # Check for negative cycle
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                return False, dist  # Negative cycle detected

        return True, dist

    @staticmethod
    def dp_quadratic_lis(arr: List[int]) -> int:
        """
        Independent O(N^2) quadratic oracle for Longest Increasing Subsequence.
        """
        n = len(arr)
        if n == 0:
            return 0
        dp = [1] * n
        for i in range(n):
            for j in range(i):
                if arr[j] < arr[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)

    @staticmethod
    def dp_window_quadratic(arr: List[int], k: int) -> int:
        """
        Independent O(N * K) brute-force oracle for sliding-window DP:
        dp[i] = min_{j in [max(0, i-k), i-1]} (dp[j] + arr[i])
        """
        n = len(arr)
        if n == 0:
            return 0
        dp = [0] * n
        dp[0] = arr[0]
        for i in range(1, n):
            min_prev = float('inf')
            start_j = max(0, i - k)
            for j in range(start_j, i):
                min_prev = min(min_prev, dp[j])
            dp[i] = min_prev + arr[i]
        return dp[-1]

    @staticmethod
    def event_scheduling_sweep(intervals: List[Tuple[int, int]]) -> int:
        """
        Independent sweep-line point-overlap oracle for interval partitioning.
        """
        events = []
        for start, end in intervals:
            events.append((start, 1))   # Start of interval
            events.append((end, -1))    # End of interval
        events.sort(key=lambda x: (x[0], -x[1]))

        max_concurrent = 0
        current = 0
        for time, kind in events:
            current += kind
            max_concurrent = max(max_concurrent, current)
        return max_concurrent

    @staticmethod
    def bisection_linear_shipment(weights: List[int], k: int) -> int:
        """
        Independent linear-step oracle for package shipment capacity.
        """
        def check(c: int) -> bool:
            groups = 1
            cur = 0
            for w in weights:
                if w > c:
                    return False
                if cur + w > c:
                    groups += 1
                    cur = w
                else:
                    cur += w
            return groups <= k

        c = max(weights) if weights else 0
        while not check(c):
            c += 1
        return c

    @staticmethod
    def tree_path_query_brute(n: int, edges: List[Tuple[int, int]], values: List[int], u: int, v: int) -> int:
        """
        Independent DFS path sum oracle for tree path queries.
        """
        adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)

        path: List[int] = []
        def dfs(curr: int, target: int, parent: int) -> bool:
            path.append(curr)
            if curr == target:
                return True
            for nxt in adj[curr]:
                if nxt != parent:
                    if dfs(nxt, target, curr):
                        return True
            path.pop()
            return False

        dfs(u, v, 0)
        return sum(values[node - 1] for node in path)


def shrink_test_case(failing_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Automated input shrinking for failing randomized test cases.
    Attempts to halve the problem scale while preserving failure structure.
    """
    shrunk = dict(failing_input)
    if "arr" in shrunk and len(shrunk["arr"]) > 4:
        shrunk["arr"] = shrunk["arr"][: len(shrunk["arr"]) // 2]
    if "edges" in shrunk and len(shrunk["edges"]) > 4:
        shrunk["edges"] = shrunk["edges"][: len(shrunk["edges"]) // 2]
    return shrunk


def oracle_bottleneck_path(n: int, edges: List[Tuple[int, int, int]], src: int, dst: int) -> int:
    weights = sorted(set(w for _, _, w in edges))
    ans = -1
    for w in weights:
        adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
        for u, v, weight in edges:
            if weight >= w:
                adj[u].append(v)
                adj[v].append(u)
        q = [src]
        visited = {src}
        reached = False
        while q:
            curr = q.pop(0)
            if curr == dst:
                reached = True
                break
            for nxt in adj[curr]:
                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)
        if reached:
            ans = w
    return ans


def oracle_tree_subtree_dp(n: int, adj: Dict[int, List[int]], vals: Dict[int, int], root: int = 1) -> Tuple[Dict[int, int], Dict[int, int]]:
    sz: Dict[int, int] = {}
    sums: Dict[int, int] = {}
    def dfs(u: int, p: int) -> None:
        sz[u] = 1
        sums[u] = vals.get(u, 0)
        for v in adj.get(u, []):
            if v != p:
                dfs(v, u)
                sz[u] += sz[v]
                sums[u] += sums[v]
    dfs(root, 0)
    return sz, sums


oracle_kruskal_mst = CrossFamilyOracles.mst_prim

def oracle_dijkstra(n: int, adj: Dict[int, List[Tuple[int, int]]], src: int = 1) -> List[int]:
    edges = []
    for u in adj:
        for v, w in adj[u]:
            edges.append((u, v, w))
    _, dist = CrossFamilyOracles.dijkstra_bellman_ford(n, edges, src)
    return dist

def oracle_tree_path_hld(n: int, adj: Dict[int, List[int]], vals: Dict[int, int], queries: List[Tuple[int, int]]) -> List[int]:
    edge_list = []
    for u in adj:
        for v in adj[u]:
            edge_list.append((u, v))
    val_arr = [vals.get(i, 0) for i in range(1, n + 1)]
    return [CrossFamilyOracles.tree_path_query_brute(n, edge_list, val_arr, q[0], q[1]) for q in queries]

oracle_event_scheduling_heap = CrossFamilyOracles.event_scheduling_sweep
oracle_convex_dp_monotonic_queue = CrossFamilyOracles.dp_window_quadratic
oracle_bisection_greedy = CrossFamilyOracles.bisection_linear_shipment
