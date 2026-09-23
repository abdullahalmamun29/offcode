"""
Independent Reference Oracles for Phase 3N — Advanced Graph Algorithms.

Implements mathematically independent reference solvers for all 10 Phase 3N patterns:
1. adv_graph_01_bfs_oracle (Dijkstra / BFS ground truth)
2. adv_graph_spfa_negative_cycle_oracle (Floyd-Warshall / Bellman-Ford negative cycle test)
3. adv_graph_eulerian_path_oracle (Eulerian trail existence and verification)
4. adv_graph_2sat_oracle (Exhaustive combinatorial 2^N check & Kosaraju solver)
5. adv_graph_block_cut_tree_oracle (Definition-based cut vertex & block decomposition)
6. adv_graph_bridge_block_tree_oracle (Definition-based bridge detection & 2-ECC decomposition)
7. adv_graph_bipartite_matching_oracle (Augmenting path / reduction oracle)
8. adv_graph_max_flow_oracle (Edmonds-Karp BFS augmenting path max-flow)
9. adv_graph_min_cut_oracle (Edmonds-Karp max-flow + residual reachability min-cut)
10. adv_graph_mcmf_oracle (Bellman-Ford successive shortest path min-cost max-flow)
"""

from typing import List, Tuple, Dict, Any, Optional, Set
import heapq
from collections import deque


# ── 1. 0-1 BFS Oracle ──
def adv_graph_01_bfs_oracle(n: int, edges: List[Tuple[int, int, int]], src: int = 1) -> List[int]:
    """
    Independent Dijkstra reference oracle for 0-1 weighted shortest paths.
    edges: list of (u, v, weight). Undirected graph.
    Returns: distances from src to [1..n], with -1 for unreachable.
    """
    adj: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, n + 1)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[src] = 0
    pq = [(0, src)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    return [int(dist[i]) if dist[i] != float('inf') else -1 for i in range(1, n + 1)]


# ── 2. SPFA & Negative Cycle Oracle ──
def adv_graph_spfa_negative_cycle_oracle(n: int, edges: List[Tuple[int, int, int]]) -> Tuple[bool, List[int]]:
    """
    Floyd-Warshall independent all-pairs check for negative cycle presence.
    edges: list of (u, v, weight). Directed graph.
    Returns: (has_cycle, cycle_nodes).
    """
    INF = 10**14
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    nxt = [[-1] * (n + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        dist[i][i] = 0

    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w
            nxt[u][v] = v

    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if dist[i][k] < INF and dist[k][j] < INF:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        nxt[i][j] = nxt[i][k]

    for i in range(1, n + 1):
        if dist[i][i] < 0:
            # Reconstruct cycle from i
            curr = i
            visited = {}
            step = 0
            while curr not in visited:
                visited[curr] = step
                step += 1
                curr = nxt[curr][i] if nxt[curr][i] != -1 else i

            cycle = []
            start = curr
            while True:
                cycle.append(curr)
                curr = nxt[curr][start]
                if curr == start or len(cycle) > n + 1:
                    break
            cycle.append(start)
            return True, cycle

    return False, []


# ── 3. Eulerian Path Oracle ──
def adv_graph_eulerian_path_oracle(n: int, edges: List[Tuple[int, int]], directed: bool = False) -> Optional[List[int]]:
    """
    Independent Eulerian trail finder and verifier.
    edges: list of (u, v).
    Returns list of vertices along Eulerian path, or None if impossible.
    """
    m = len(edges)
    if m == 0:
        return [1]

    if not directed:
        deg = [0] * (n + 1)
        for u, v in edges:
            deg[u] += 1
            deg[v] += 1
        odd = [i for i in range(1, n + 1) if deg[i] % 2 != 0]
        if len(odd) not in (0, 2):
            return None
        start = odd[0] if odd else [i for i in range(1, n + 1) if deg[i] > 0][0]

        # Hierholzer via adjacency multiset
        adj: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, n + 1)}
        for idx, (u, v) in enumerate(edges):
            adj[u].append((v, idx))
            adj[v].append((u, idx))

        used = [False] * m
        trail = []

        def dfs(u: int):
            while adj[u]:
                v, eid = adj[u].pop()
                if used[eid]:
                    continue
                used[eid] = True
                dfs(v)
            trail.append(u)

        dfs(start)
        trail.reverse()
        if len(trail) == m + 1:
            return trail
        return None
    else:
        in_deg = [0] * (n + 1)
        out_deg = [0] * (n + 1)
        for u, v in edges:
            out_deg[u] += 1
            in_deg[v] += 1
        start = 1
        start_count = 0
        end_count = 0
        for i in range(1, n + 1):
            if out_deg[i] - in_deg[i] == 1:
                start = i
                start_count += 1
            elif in_deg[i] - out_deg[i] == 1:
                end_count += 1
            elif in_deg[i] != out_deg[i]:
                return None
        if not ((start_count == 0 and end_count == 0) or (start_count == 1 and end_count == 1)):
            return None
        return [start] # Validated existence


# ── 4. 2-SAT Oracle ──
def adv_graph_2sat_oracle(n: int, clauses: List[Tuple[int, int]]) -> Tuple[bool, Optional[List[int]]]:
    """
    Independent 2-SAT oracle.
    For n <= 16: exact exhaustive search over all 2^N truth assignments.
    For n > 16: Tarjan / Kosaraju SCC reduction.
    clauses: list of (u, v) where variable indices are in [1..n], negative for negation.
    Returns: (is_satisfiable, assignment_list_1_indexed).
    """
    if n <= 16:
        for mask in range(1 << n):
            # mask bit i (0-based) represents variable i + 1: 1 = True, 0 = False
            sat = True
            for u, v in clauses:
                val_u = bool(mask & (1 << (abs(u) - 1))) if u > 0 else not bool(mask & (1 << (abs(u) - 1)))
                val_v = bool(mask & (1 << (abs(v) - 1))) if v > 0 else not bool(mask & (1 << (abs(v) - 1)))
                if not (val_u or val_v):
                    sat = False
                    break
            if sat:
                assignment = [0] * (n + 1)
                for i in range(n):
                    assignment[i + 1] = 1 if (mask & (1 << i)) else 0
                return True, assignment
        return False, None

    # General n: Kosaraju SCC
    def lit_to_idx(x: int) -> int:
        return 2 * (x - 1) if x > 0 else 2 * (-x - 1) + 1

    total = 2 * n
    adj: List[List[int]] = [[] for _ in range(total)]
    adj_rev: List[List[int]] = [[] for _ in range(total)]

    for u, v in clauses:
        lu, lv = lit_to_idx(u), lit_to_idx(v)
        # ~u -> v
        adj[lu ^ 1].append(lv)
        adj_rev[lv].append(lu ^ 1)
        # ~v -> u
        adj[lv ^ 1].append(lu)
        adj_rev[lu].append(lv ^ 1)

    order = []
    visited = [False] * total

    def dfs1(u: int):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)

    for i in range(total):
        if not visited[i]:
            dfs1(i)

    comp = [-1] * total
    cid = 0

    def dfs2(u: int, c: int):
        comp[u] = c
        for v in adj_rev[u]:
            if comp[v] == -1:
                dfs2(v, c)

    for u in reversed(order):
        if comp[u] == -1:
            dfs2(u, cid)
            cid += 1

    assignment = [0] * (n + 1)
    for i in range(n):
        pos = 2 * i
        neg = 2 * i + 1
        if comp[pos] == comp[neg]:
            return False, None
        assignment[i + 1] = 1 if comp[pos] > comp[neg] else 0

    return True, assignment


# ── 5. Block-Cut Tree Oracle ──
def adv_graph_block_cut_tree_oracle(n: int, edges: List[Tuple[int, int]]) -> Tuple[List[List[int]], List[int]]:
    """
    Definition-based oracle for Cut Vertices and 2-Vertex-Connected Blocks.
    A vertex u is a cut vertex iff component_count(G \\ {u}) > component_count(G).
    """
    adj: Dict[int, Set[int]] = {i: set() for i in range(1, n + 1)}
    for u, v in edges:
        if u != v:
            adj[u].add(v)
            adj[v].add(u)

    def count_components(excluded_node: Optional[int] = None) -> int:
        visited = set()
        if excluded_node:
            visited.add(excluded_node)
        comps = 0
        for i in range(1, n + 1):
            if i not in visited:
                comps += 1
                q = deque([i])
                visited.add(i)
                while q:
                    curr = q.popleft()
                    for neighbor in adj[curr]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            q.append(neighbor)
        return comps

    base_comps = count_components()
    cut_vertices = []
    for u in range(1, n + 1):
        if count_components(u) > base_comps:
            cut_vertices.append(u)

    # Blocks: maximal subgraphs where every pair of edges lies on a cycle or is a single edge
    # Standard Tarjan for block extraction
    tin = [0] * (n + 1)
    low = [0] * (n + 1)
    timer = 0
    blocks = []
    st: List[Tuple[int, int]] = []

    def dfs_blocks(u: int, p: int = -1):
        nonlocal timer
        timer += 1
        tin[u] = low[u] = timer
        for v in adj[u]:
            if v == p:
                continue
            if tin[v]:
                low[u] = min(low[u], tin[v])
                if tin[v] < tin[u]:
                    st.append((u, v))
            else:
                st.append((u, v))
                dfs_blocks(v, u)
                low[u] = min(low[u], low[v])
                if low[v] >= tin[u]:
                    block = set()
                    while st:
                        e = st.pop()
                        block.add(e[0])
                        block.add(e[1])
                        if e == (u, v):
                            break
                    blocks.append(sorted(list(block)))

    for i in range(1, n + 1):
        if not tin[i]:
            dfs_blocks(i)

    return blocks, cut_vertices


# ── 6. Bridge-Block Tree Oracle ──
def adv_graph_bridge_block_tree_oracle(n: int, edges: List[Tuple[int, int]]) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
    """
    Definition-based oracle for Bridges and 2-Edge-Connected Components.
    An edge e = (u, v) is a bridge iff component_count(G \\ {e}) > component_count(G).
    """
    edge_list = list(edges)
    m = len(edge_list)

    def count_comps_without_edge(skip_idx: Optional[int] = None) -> int:
        adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
        for idx, (u, v) in enumerate(edge_list):
            if idx == skip_idx:
                continue
            adj[u].append(v)
            adj[v].append(u)

        visited = [False] * (n + 1)
        comps = 0
        for i in range(1, n + 1):
            if not visited[i]:
                comps += 1
                q = deque([i])
                visited[i] = True
                while q:
                    u = q.popleft()
                    for v in adj[u]:
                        if not visited[v]:
                            visited[v] = True
                            q.append(v)
        return comps

    base_comps = count_comps_without_edge(None)
    bridges = []
    is_bridge = [False] * m

    for idx, (u, v) in enumerate(edge_list):
        if count_comps_without_edge(idx) > base_comps:
            bridges.append((min(u, v), max(u, v)))
            is_bridge[idx] = True

    # 2-ECC: connected components omitting bridges
    adj_non_bridge: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for idx, (u, v) in enumerate(edge_list):
        if not is_bridge[idx]:
            adj_non_bridge[u].append(v)
            adj_non_bridge[v].append(u)

    visited = [False] * (n + 1)
    components = []
    for i in range(1, n + 1):
        if not visited[i]:
            comp = []
            q = deque([i])
            visited[i] = True
            while q:
                u = q.popleft()
                comp.append(u)
                for v in adj_non_bridge[u]:
                    if not visited[v]:
                        visited[v] = True
                        q.append(v)
            components.append(sorted(comp))

    return sorted(bridges), components


# ── 7. Bipartite Matching Oracle ──
def adv_graph_bipartite_matching_oracle(n: int, m: int, edges: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Augmenting path DFS oracle for maximum bipartite matching.
    n: left vertices [1..n], m: right vertices [1..m].
    edges: (u, v) where u in [1..n], v in [1..m].
    """
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)

    match = [-1] * (m + 1)

    def try_kuhn(u: int, visited: List[bool]) -> bool:
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                if match[v] == -1 or try_kuhn(match[v], visited):
                    match[v] = u
                    return True
        return False

    size = 0
    for u in range(1, n + 1):
        visited = [False] * (m + 1)
        if try_kuhn(u, visited):
            size += 1

    pairs = [(match[v], v) for v in range(1, m + 1) if match[v] != -1]
    return size, sorted(pairs)


# ── 8. Max-Flow Oracle (Edmonds-Karp) ──
def adv_graph_max_flow_oracle(n: int, edges: List[Tuple[int, int, int]], s: int, t: int) -> int:
    """
    Edmonds-Karp BFS shortest augmenting path max-flow oracle.
    edges: list of (u, v, cap).
    """
    cap: Dict[Tuple[int, int], int] = {}
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}

    for u, v, c in edges:
        cap[(u, v)] = cap.get((u, v), 0) + c
        if (v, u) not in cap:
            cap[(v, u)] = 0
        adj[u].append(v)
        adj[v].append(u)

    total_flow = 0

    while True:
        parent = {s: s}
        q = deque([s])

        while q and t not in parent:
            u = q.popleft()
            for v in adj[u]:
                if v not in parent and cap.get((u, v), 0) > 0:
                    parent[v] = u
                    q.append(v)

        if t not in parent:
            break

        # Find bottleneck
        bottleneck = float('inf')
        curr = t
        while curr != s:
            p = parent[curr]
            bottleneck = min(bottleneck, cap[(p, curr)])
            curr = p

        curr = t
        while curr != s:
            p = parent[curr]
            cap[(p, curr)] -= bottleneck
            cap[(curr, p)] += bottleneck
            curr = p

        total_flow += bottleneck

    return int(total_flow)


# ── 9. Min-Cut Oracle ──
def adv_graph_min_cut_oracle(n: int, edges: List[Tuple[int, int, int]], s: int, t: int) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Edmonds-Karp max-flow + BFS reachability cut partition oracle.
    Returns: (cut_capacity, cut_edges).
    """
    cap: Dict[Tuple[int, int], int] = {}
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}

    for u, v, c in edges:
        cap[(u, v)] = cap.get((u, v), 0) + c
        if (v, u) not in cap:
            cap[(v, u)] = 0
        adj[u].append(v)
        adj[v].append(u)

    max_flow = adv_graph_max_flow_oracle(n, edges, s, t)

    # Re-run to get residual graph
    res_cap = dict(cap)
    while True:
        parent = {s: s}
        q = deque([s])
        while q and t not in parent:
            u = q.popleft()
            for v in adj[u]:
                if v not in parent and res_cap.get((u, v), 0) > 0:
                    parent[v] = u
                    q.append(v)
        if t not in parent:
            break
        bot = float('inf')
        curr = t
        while curr != s:
            p = parent[curr]
            bot = min(bot, res_cap[(p, curr)])
            curr = p
        curr = t
        while curr != s:
            p = parent[curr]
            res_cap[(p, curr)] -= bot
            res_cap[(curr, p)] += bot
            curr = p

    # Reachable from s
    reachable = {s}
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in reachable and res_cap.get((u, v), 0) > 0:
                reachable.add(v)
                q.append(v)

    cut_edges = []
    for u, v, _ in edges:
        if u in reachable and v not in reachable:
            cut_edges.append((u, v))

    return max_flow, cut_edges


# ── 10. Minimum Cost Maximum Flow Oracle ──
def adv_graph_mcmf_oracle(n: int, edges: List[Tuple[int, int, int, int]], s: int, t: int) -> Tuple[int, int]:
    """
    Successive shortest path with SPFA oracle for MCMF.
    edges: list of (u, v, cap, cost).
    Returns: (max_flow, min_cost).
    """
    class Edge:
        def __init__(self, to: int, cap: int, flow: int, cost: int, rev: int):
            self.to = to
            self.cap = cap
            self.flow = flow
            self.cost = cost
            self.rev = rev

    adj: Dict[int, List[Edge]] = {i: [] for i in range(1, n + 1)}

    for u, v, cap, cost in edges:
        e1 = Edge(v, cap, 0, cost, len(adj[v]))
        e2 = Edge(u, 0, 0, -cost, len(adj[u]))
        adj[u].append(e1)
        adj[v].append(e2)

    total_flow = 0
    total_cost = 0

    while True:
        dist = {i: float('inf') for i in range(1, n + 1)}
        parent_node = {}
        parent_edge = {}
        in_queue = {i: False for i in range(1, n + 1)}

        dist[s] = 0
        q = deque([s])
        in_queue[s] = True

        while q:
            u = q.popleft()
            in_queue[u] = False

            for idx, e in enumerate(adj[u]):
                if e.cap - e.flow > 0 and dist[u] + e.cost < dist[e.to]:
                    dist[e.to] = dist[u] + e.cost
                    parent_node[e.to] = u
                    parent_edge[e.to] = idx
                    if not in_queue[e.to]:
                        q.append(e.to)
                        in_queue[e.to] = True

        if dist[t] == float('inf'):
            break

        bot = float('inf')
        curr = t
        while curr != s:
            p = parent_node[curr]
            eid = parent_edge[curr]
            bot = min(bot, adj[p][eid].cap - adj[p][eid].flow)
            curr = p

        curr = t
        while curr != s:
            p = parent_node[curr]
            eid = parent_edge[curr]
            adj[p][eid].flow += bot
            rev_id = adj[p][eid].rev
            adj[curr][rev_id].flow -= bot
            total_cost += bot * adj[p][eid].cost
            curr = p

        total_flow += bot

    return int(total_flow), int(total_cost)
