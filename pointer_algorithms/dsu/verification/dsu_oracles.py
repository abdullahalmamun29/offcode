"""
Python Reference Oracles for Disjoint Set Union (DSU) Domain (Phase 3H).

Independent reference implementations for all 10 DSU patterns.
Used for differential testing and oracle validation against generated C++17 implementations.
"""

from typing import List, Tuple, Dict, Any, Optional, Set
from collections import defaultdict, deque


def oracle_basic_dsu(n: int, operations: List[Tuple[int, int, int]]) -> List[str]:
    """
    Independent reference oracle for basic DSU.
    Operations:
    - (1, u, v): unite u and v
    - (2, u, v): query connected(u, v) -> "YES" or "NO"
    - (3, u, 0): query component_size(u) -> string integer
    Uses explicit set partition.
    """
    comp = {i: {i} for i in range(1, n + 1)}
    output: List[str] = []

    for op in operations:
        t = op[0]
        u = op[1]
        v = op[2] if len(op) > 2 else 0

        if t == 1:
            if u in comp and v in comp and comp[u] is not comp[v]:
                merged = comp[u] | comp[v]
                for node in merged:
                    comp[node] = merged
        elif t == 2:
            if u in comp and v in comp and comp[u] is comp[v]:
                output.append("YES")
            else:
                output.append("NO")
        elif t == 3:
            if u in comp:
                output.append(str(len(comp[u])))
            else:
                output.append("1")

    return output


def oracle_component_metadata(n: int, val: List[int], operations: List[Tuple[int, ...]]) -> List[str]:
    """
    Reference oracle for component metadata (size, sum, min, max).
    val is 1-indexed (val[1..n]).
    Operations:
    - (1, u, v): unite u and v
    - (2, u): query (size, sum, min, max) of component containing u
    """
    comp = {i: {i} for i in range(1, n + 1)}
    output: List[str] = []

    for op in operations:
        t = op[0]
        if t == 1:
            u, v = op[1], op[2]
            if comp[u] is not comp[v]:
                merged = comp[u] | comp[v]
                for node in merged:
                    comp[node] = merged
        elif t == 2:
            u = op[1]
            c = comp[u]
            sz = len(c)
            sm = sum(val[node] for node in c)
            mn = min(val[node] for node in c)
            mx = max(val[node] for node in c)
            output.append(f"{sz} {sm} {mn} {mx}")

    return output


def oracle_dynamic_connectivity(n: int, operations: List[Tuple[int, int, int]]) -> List[str]:
    """
    Reference oracle for incremental dynamic connectivity.
    Operations:
    - (1, u, v): add edge (unite u, v)
    - (2, u, v): query connected(u, v) -> "YES" or "NO"
    - (3, u, 0): query component_size(u) -> string integer
    """
    return oracle_basic_dsu(n, operations)


def oracle_weighted_dsu(n: int, operations: List[Tuple[int, ...]]) -> List[str]:
    """
    Reference oracle for Weighted / Potential DSU: value[x] - value[y] = w.
    Operations:
    - (1, u, v, w): assert value[u] - value[v] = w. If contradiction, output "CONTRADICTION".
    - (2, u, v): query value[u] - value[v]. If connected output difference, else "UNKNOWN".
    Uses reference BFS / path offset verification.
    """
    adj = defaultdict(list)  # u -> list of (v, weight) representing value[u] - value[v] = weight
    output: List[str] = []

    for op in operations:
        t = op[0]
        if t == 1:
            u, v, w = op[1], op[2], op[3]
            # Check reachability between u and v
            q = deque([(u, 0)])
            visited = {u: 0}
            connected = False
            while q:
                curr, pot = q.popleft()
                if curr == v:
                    connected = True
                    break
                for nxt, edge_w in adj[curr]:
                    if nxt not in visited:
                        visited[nxt] = pot + edge_w
                        q.append((nxt, pot + edge_w))

            if connected:
                # We know value[u] - value[curr] = visited[curr]
                # value[u] - value[v] is visited[v]
                existing_diff = visited[v]
                if existing_diff != w:
                    output.append("CONTRADICTION")
            else:
                # Add edge: value[u] - value[v] = w => u -> (v, w) and v -> (u, -w)
                adj[u].append((v, w))
                adj[v].append((u, -w))
        elif t == 2:
            u, v = op[1], op[2]
            q = deque([(u, 0)])
            visited = {u: 0}
            found = False
            while q:
                curr, pot = q.popleft()
                if curr == v:
                    output.append(str(pot))
                    found = True
                    break
                for nxt, edge_w in adj[curr]:
                    if nxt not in visited:
                        visited[nxt] = pot + edge_w
                        q.append((nxt, pot + edge_w))
            if not found:
                output.append("UNKNOWN")

    return output


def oracle_potential_difference(n: int, operations: List[Tuple[int, ...]]) -> List[str]:
    """
    Reference oracle for relative difference queries.
    Operations:
    - (1, u, v, w): assert value[u] - value[v] = w
    - (2, u, v): query value[u] - value[v] -> integer diff or "UNKNOWN"
    """
    return oracle_weighted_dsu(n, operations)


def oracle_parity_dsu(n: int, operations: List[Tuple[int, ...]]) -> List[str]:
    """
    Reference oracle for dynamic 2-coloring / parity DSU: color[u] ^ color[v] = p.
    p = 0 -> same color; p = 1 -> different color.
    Operations:
    - (1, u, v, p): assert relation. If contradiction, output "CONTRADICTION".
    - (2, u, v): query relationship -> "SAME", "DIFFERENT", or "UNKNOWN".
    """
    adj = defaultdict(list)  # u -> list of (v, p)
    output: List[str] = []

    for op in operations:
        t = op[0]
        if t == 1:
            u, v, p = op[1], op[2], op[3]
            # Check existing color relation
            q = deque([(u, 0)])
            visited = {u: 0}
            connected = False
            while q:
                curr, col = q.popleft()
                if curr == v:
                    connected = True
                    break
                for nxt, edge_p in adj[curr]:
                    if nxt not in visited:
                        visited[nxt] = col ^ edge_p
                        q.append((nxt, col ^ edge_p))

            if connected:
                existing_p = visited[v]
                if existing_p != p:
                    output.append("CONTRADICTION")
            else:
                adj[u].append((v, p))
                adj[v].append((u, p))
        elif t == 2:
            u, v = op[1], op[2]
            q = deque([(u, 0)])
            visited = {u: 0}
            found = False
            while q:
                curr, col = q.popleft()
                if curr == v:
                    output.append("SAME" if col == 0 else "DIFFERENT")
                    found = True
                    break
                for nxt, edge_p in adj[curr]:
                    if nxt not in visited:
                        visited[nxt] = col ^ edge_p
                        q.append((nxt, col ^ edge_p))
            if not found:
                output.append("UNKNOWN")

    return output


def oracle_rollback_dsu(n: int, operations: List[Tuple[int, ...]]) -> List[str]:
    """
    Reference oracle for Rollback DSU.
    Operations:
    - (1, u, v): unite u and v
    - (2, u, v): query connected(u, v) -> "YES" or "NO"
    - (3,): create snapshot
    - (4,): rollback to last snapshot
    """
    state_stack = []
    # State is represented as an adjacency map or disjoint set partition
    current_sets = {i: {i} for i in range(1, n + 1)}
    output: List[str] = []

    for op in operations:
        t = op[0]
        if t == 1:
            u, v = op[1], op[2]
            if current_sets[u] is not current_sets[v]:
                merged = current_sets[u] | current_sets[v]
                for node in merged:
                    current_sets[node] = merged
        elif t == 2:
            u, v = op[1], op[2]
            output.append("YES" if current_sets[u] is current_sets[v] else "NO")
        elif t == 3:
            # Snapshot: make a deep copy of current partition
            # Represent sets as frozensets
            unique_sets = set(frozenset(s) for s in current_sets.values())
            state_stack.append(unique_sets)
        elif t == 4:
            # Rollback to last snapshot
            if state_stack:
                restored = state_stack.pop()
                current_sets = {}
                for s in restored:
                    mutable_s = set(s)
                    for node in mutable_s:
                        current_sets[node] = mutable_s

    return output


def oracle_offline_dynamic_connectivity(n: int, queries: List[Tuple[int, int, int]]) -> List[str]:
    """
    Reference oracle for offline dynamic connectivity.
    queries: list of (type, u, v) where:
    - type 1: add edge (u, v)
    - type 2: remove edge (u, v)
    - type 3: query connected(u, v) -> "YES" or "NO"
    Simulates exact active graph at each query step via BFS.
    """
    adj = defaultdict(set)
    output: List[str] = []

    for q in queries:
        t, u, v = q[0], q[1], q[2]
        if t == 1:
            adj[u].add(v)
            adj[v].add(u)
        elif t == 2:
            adj[u].discard(v)
            adj[v].discard(u)
        elif t == 3:
            # BFS reachability
            queue = deque([u])
            visited = {u}
            found = False
            while queue:
                curr = queue.popleft()
                if curr == v:
                    found = True
                    break
                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            output.append("YES" if found else "NO")

    return output


def oracle_kruskal_support(n: int, edges: List[Tuple[int, int, int]]) -> int:
    """
    Reference oracle for Kruskal MST support.
    edges: list of (u, v, weight).
    Returns total MST weight.
    """
    sorted_edges = sorted(edges, key=lambda e: e[2])
    parent = list(range(n + 1))

    def find(x):
        while x != parent[x]:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def unite(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        parent[rx] = ry
        return True

    total_weight = 0
    edges_count = 0
    for u, v, w in sorted_edges:
        if unite(u, v):
            total_weight += w
            edges_count += 1
            if edges_count == n - 1:
                break

    return total_weight


def oracle_constraint_consistency(n: int, constraints: List[Tuple[int, int, int]]) -> str:
    """
    Reference oracle for system of difference constraints value[u] - value[v] = diff.
    Returns "CONSISTENT" or "INCONSISTENT".
    """
    adj = defaultdict(list)
    for u, v, diff in constraints:
        # Check if u and v are connected
        q = deque([(u, 0)])
        visited = {u: 0}
        connected = False
        while q:
            curr, pot = q.popleft()
            if curr == v:
                connected = True
                break
            for nxt, edge_w in adj[curr]:
                if nxt not in visited:
                    visited[nxt] = pot + edge_w
                    q.append((nxt, pot + edge_w))

        if connected:
            if visited[v] != diff:
                return "INCONSISTENT"
        else:
            adj[u].append((v, diff))
            adj[v].append((u, -diff))

    return "CONSISTENT"
