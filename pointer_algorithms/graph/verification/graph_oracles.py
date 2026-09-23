"""
Reference Graph Oracles for Phase 3F.

Pure Python reference implementations used as verification oracles:
- BFS shortest path
- DFS traversal
- Connected components
- Cycle detection (undirected & directed)
- Bipartite coloring (odd cycle check)
- Dijkstra shortest path
- Bellman-Ford shortest path & negative cycle detection
- Floyd-Warshall all-pairs shortest path
- Topological sort (Kahn / DFS)
- DAG DP (longest/shortest path)
- Disjoint Set Union (DSU)
- Kruskal & Prim MST
- Tarjan SCC
- Bridges & Articulation Points
"""

from collections import deque
import heapq
from typing import List, Tuple, Dict, Set, Optional, Any

INF = float("inf")


def oracle_bfs_shortest_path(n: int, edges: List[Tuple[int, int]], source: int = 1) -> List[int]:
    """Unweighted shortest path from source. Returns dist[1..n], -1 if unreachable."""
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    dist = [-1] * (n + 1)
    dist[source] = 0
    q = deque([source])

    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)

    return dist[1:]


def oracle_dfs_traversal(n: int, edges: List[Tuple[int, int]], source: int = 1) -> List[int]:
    """DFS preorder traversal order starting from source, then covering unvisited."""
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = [False] * (n + 1)
    order = []

    def dfs(u: int):
        visited[u] = True
        order.append(u)
        for v in sorted(adj[u]):
            if not visited[v]:
                dfs(v)

    if 1 <= source <= n:
        dfs(source)
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i)

    return order


def oracle_connected_components(n: int, edges: List[Tuple[int, int]]) -> int:
    """Returns the number of connected components in an undirected graph."""
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = [False] * (n + 1)
    count = 0

    for i in range(1, n + 1):
        if not visited[i]:
            count += 1
            q = deque([i])
            visited[i] = True
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        q.append(v)

    return count


def oracle_cycle_detection_undirected(n: int, edges: List[Tuple[int, int]]) -> bool:
    """Returns True if undirected graph contains any cycle, else False."""
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = [False] * (n + 1)

    def dfs(u: int, parent: int) -> bool:
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                if dfs(v, u):
                    return True
            elif v != parent:
                return True
        return False

    for i in range(1, n + 1):
        if not visited[i]:
            if dfs(i, 0):
                return True
    return False


def oracle_cycle_detection_directed(n: int, edges: List[Tuple[int, int]]) -> bool:
    """Returns True if directed graph contains any cycle using 3-color DFS."""
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)

    color = [0] * (n + 1)  # 0: UNVISITED, 1: VISITING, 2: VISITED

    def dfs(u: int) -> bool:
        color[u] = 1
        for v in adj[u]:
            if color[v] == 1:
                return True
            if color[v] == 0 and dfs(v):
                return True
        color[u] = 2
        return False

    for i in range(1, n + 1):
        if color[i] == 0:
            if dfs(i):
                return True
    return False


def oracle_bipartite_coloring(n: int, edges: List[Tuple[int, int]]) -> Tuple[bool, Optional[List[int]]]:
    """Returns (is_bipartite, colors) where colors is 0/1 array for nodes 1..n."""
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * (n + 1)

    for i in range(1, n + 1):
        if color[i] != -1:
            continue
        color[i] = 0
        q = deque([i])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False, None

    return True, color[1:]


def oracle_dijkstra(n: int, edges: List[Tuple[int, int, int]], source: int = 1) -> List[int]:
    """Single-source shortest path for non-negative weights. Returns dist[1..n], -1 if INF."""
    adj: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, n + 1)}
    for u, v, w in edges:
        adj[u].append((v, w))

    dist = [INF] * (n + 1)
    dist[source] = 0
    pq = [(0, source)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    return [int(d) if d != INF else -1 for d in dist[1:]]


def oracle_bellman_ford(n: int, edges: List[Tuple[int, int, int]], source: int = 1) -> Tuple[bool, List[int]]:
    """Bellman-Ford. Returns (has_negative_cycle, dist[1..n]). dist is -1 for unreachable."""
    dist = [INF] * (n + 1)
    dist[source] = 0

    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break

from dataclasses import dataclass

@dataclass
class NegativeCycleInfluence:
    has_negative_cycle_in_graph: bool
    source_can_reach_negative_cycle: bool
    negative_cycle_can_reach_target: bool
    target_shortest_path_status: str  # 'WELL_DEFINED', 'UNBOUNDED_BELOW', 'UNREACHABLE'
    target_distance: Optional[int]
    unbounded_nodes: List[int]
    distances: List[Any]  # int, -1 for unreachable, '-INF' for unbounded below


def oracle_negative_cycle_influence(n: int, edges: List[Tuple[int, int, int]], source: int = 1, target: Optional[int] = None) -> NegativeCycleInfluence:
    """
    Evaluates shortest path reachability and negative cycle influence under exact graph semantics:
    1. Distinguishes whether a negative cycle exists anywhere in the graph.
    2. Distinguishes whether a negative cycle is reachable from the source.
    3. Distinguishes whether a negative cycle can forward-reach the target.
    A negative cycle makes a target's distance unbounded below (-INF) iff source -> cycle AND cycle -> target.
    """
    # Check if a negative cycle exists anywhere in the graph (using a virtual super-source connected to all nodes with 0 weight)
    virtual_dist = [0] * (n + 1)
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if virtual_dist[u] + w < virtual_dist[v]:
                virtual_dist[v] = virtual_dist[u] + w
                changed = True
        if not changed:
            break
    has_neg_cycle_anywhere = False
    for u, v, w in edges:
        if virtual_dist[u] + w < virtual_dist[v]:
            has_neg_cycle_anywhere = True
            break

    # Now run Bellman-Ford from the actual source
    dist = [INF] * (n + 1)
    dist[source] = 0

    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break

    # Find all vertices relaxed on round V (directly in or reached by a negative cycle reachable from source)
    cycle_seeds = set()
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            cycle_seeds.add(v)

    source_can_reach_cycle = len(cycle_seeds) > 0

    # Propagate negative-cycle reachability forward along all edges
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v, w in edges:
        adj[u].append(v)

    unbounded = set(cycle_seeds)
    q = deque(cycle_seeds)
    while q:
        curr = q.popleft()
        for nxt in adj[curr]:
            if nxt not in unbounded:
                unbounded.add(nxt)
                q.append(nxt)

    # Build final distance vector
    result_dist = []
    for i in range(1, n + 1):
        if i in unbounded:
            result_dist.append("-INF")
        elif dist[i] == INF:
            result_dist.append(-1)
        else:
            result_dist.append(int(dist[i]))

    target_status = "WELL_DEFINED"
    target_dist = None
    neg_cycle_reaches_target = False

    if target is not None and 1 <= target <= n:
        if target in unbounded:
            target_status = "UNBOUNDED_BELOW"
            neg_cycle_reaches_target = True
        elif dist[target] == INF:
            target_status = "UNREACHABLE"
            target_dist = -1
        else:
            target_status = "WELL_DEFINED"
            target_dist = int(dist[target])

    return NegativeCycleInfluence(
        has_negative_cycle_in_graph=has_neg_cycle_anywhere,
        source_can_reach_negative_cycle=source_can_reach_cycle,
        negative_cycle_can_reach_target=neg_cycle_reaches_target,
        target_shortest_path_status=target_status,
        target_distance=target_dist,
        unbounded_nodes=sorted(list(unbounded)),
        distances=result_dist
    )


def oracle_bellman_ford(n: int, edges: List[Tuple[int, int, int]], source: int = 1) -> Tuple[bool, List[int]]:
    """Bellman-Ford. Returns (has_negative_cycle_reachable_from_source, dist[1..n]). dist is -1 for unreachable."""
    analysis = oracle_negative_cycle_influence(n, edges, source=source)
    # For backwards compatibility with standard tests
    res_dist = []
    for d in analysis.distances:
        if d == "-INF":
            res_dist.append(-1)
        else:
            res_dist.append(d)
    return analysis.source_can_reach_negative_cycle, res_dist


def oracle_floyd_warshall(n: int, edges: List[Tuple[int, int, int]]) -> List[List[int]]:
    """All-pairs shortest path matrix. -1 for unreachable."""
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)

    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if dist[i][k] != INF and dist[k][j] != INF:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    result = []
    for i in range(1, n + 1):
        row = [int(dist[i][j]) if dist[i][j] != INF else -1 for j in range(1, n + 1)]
        result.append(row)
    return result


def oracle_topological_sort(n: int, edges: List[Tuple[int, int]]) -> Optional[List[int]]:
    """Kahn's topological sort. Returns ordering or None if cycle."""
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    in_deg = [0] * (n + 1)
    for u, v in edges:
        adj[u].append(v)
        in_deg[v] += 1

    q = deque([i for i in range(1, n + 1) if in_deg[i] == 0])
    order = []

    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            in_deg[v] -= 1
            if in_deg[v] == 0:
                q.append(v)

    return order if len(order) == n else None


def oracle_dag_dp_longest_path(n: int, edges: List[Tuple[int, int, int]], source: int = 1) -> int:
    """Longest path in a DAG from source. Returns max weight."""
    topo = oracle_topological_sort(n, [(u, v) for u, v, _ in edges])
    if topo is None:
        raise ValueError("Graph is not a DAG")

    adj: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, n + 1)}
    for u, v, w in edges:
        adj[u].append((v, w))

    dp = [-INF] * (n + 1)
    dp[source] = 0

    for u in topo:
        if dp[u] == -INF:
            continue
        for v, w in adj[u]:
            dp[v] = max(dp[v], dp[u] + w)

    valid_vals = [int(val) for val in dp[1:] if val != -INF]
    return max(valid_vals) if valid_vals else 0


class OracleDSU:
    def __init__(self, n: int):
        self.parent = list(range(n + 1))
        self.rank = [0] * (n + 1)
        self.components = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def unite(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


def oracle_mst_kruskal(n: int, edges: List[Tuple[int, int, int]]) -> int:
    """Kruskal's MST total weight. Returns -1 if disconnected."""
    sorted_edges = sorted(edges, key=lambda e: e[2])
    dsu = OracleDSU(n)
    total_w = 0
    edges_used = 0

    for u, v, w in sorted_edges:
        if dsu.unite(u, v):
            total_w += w
            edges_used += 1
            if edges_used == n - 1:
                break

    if edges_used == n - 1 or n == 1:
        return total_w
    return -1


def oracle_mst_prim(n: int, edges: List[Tuple[int, int, int]]) -> int:
    """Prim's MST total weight. Returns -1 if disconnected."""
    adj: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, n + 1)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    in_mst = [False] * (n + 1)
    pq = [(0, 1)]  # (weight, vertex)
    total_w = 0
    count = 0

    while pq:
        w, u = heapq.heappop(pq)
        if in_mst[u]:
            continue
        in_mst[u] = True
        total_w += w
        count += 1

        for v, weight in adj[u]:
            if not in_mst[v]:
                heapq.heappush(pq, (weight, v))

    return total_w if count == n else -1


def oracle_scc_tarjan(n: int, edges: List[Tuple[int, int]]) -> int:
    """Returns the number of strongly connected components using Tarjan's algorithm."""
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)

    tin = [0] * (n + 1)
    low = [0] * (n + 1)
    on_stack = [False] * (n + 1)
    st: List[int] = []
    timer = [0]
    scc_count = [0]

    def dfs(u: int):
        timer[0] += 1
        tin[u] = low[u] = timer[0]
        st.append(u)
        on_stack[u] = True

        for v in adj[u]:
            if tin[v] == 0:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif on_stack[v]:
                low[u] = min(low[u], tin[v])

        if low[u] == tin[u]:
            scc_count[0] += 1
            while True:
                v = st.pop()
                on_stack[v] = False
                if u == v:
                    break

    for i in range(1, n + 1):
        if tin[i] == 0:
            dfs(i)

    return scc_count[0]


def oracle_bridges_and_articulation(n: int, edges: List[Tuple[int, int]]) -> Tuple[List[Tuple[int, int]], Set[int]]:
    """Returns (bridges, articulation_points) using DFS low-link."""
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    tin = [0] * (n + 1)
    low = [0] * (n + 1)
    timer = [0]
    bridges = []
    ap: Set[int] = set()

    def dfs(u: int, p: int):
        timer[0] += 1
        tin[u] = low[u] = timer[0]
        children = 0

        for v in adj[u]:
            if v == p:
                continue
            if tin[v] != 0:
                low[u] = min(low[u], tin[v])
            else:
                children += 1
                dfs(v, u)
                low[u] = min(low[u], low[v])

                if low[v] > tin[u]:
                    bridges.append((min(u, v), max(u, v)))
                if p != 0 and low[v] >= tin[u]:
                    ap.add(u)

        if p == 0 and children >= 2:
            ap.add(u)

    for i in range(1, n + 1):
        if tin[i] == 0:
            dfs(i, 0)

    return sorted(bridges), ap
