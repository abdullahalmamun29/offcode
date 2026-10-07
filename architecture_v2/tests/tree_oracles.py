"""
Independent Reference Oracles for Tree Capability Verification.

CRITICAL INVARIANT:
These oracles are mathematically and algorithmically independent from production capabilities.
They use naive mathematical specifications (parent-walking, all-pairs BFS, exponential subset
enumeration, uncached fresh traversals) rather than binary lifting, Euler tours, HLD, or tree DP.
"""

from typing import List, Dict, Any, Optional, Tuple, Set
from collections import deque


def oracle_lca_parent_climbing(n: int, parent: Dict[int, int], u: int, v: int) -> int:
    """
    Computes LCA in O(N) time with strictly O(1) auxiliary space:
    1. Computes depth(u) and depth(v) by climbing to root.
    2. Lifts the deeper vertex until depths match.
    3. Walks u and v up in lockstep until they coincide.
    Zero visited bitsets, zero precomputation, zero binary lifting tables.
    """
    # 1. Compute depth(u)
    depth_u = 0
    curr = u
    while curr in parent and parent[curr] != 0 and parent[curr] != curr:
        depth_u += 1
        curr = parent[curr]

    # 2. Compute depth(v)
    depth_v = 0
    curr = v
    while curr in parent and parent[curr] != 0 and parent[curr] != curr:
        depth_v += 1
        curr = parent[curr]

    # 3. Equalize depths
    curr_u, curr_v = u, v
    while depth_u > depth_v:
        curr_u = parent.get(curr_u, 0)
        depth_u -= 1
    while depth_v > depth_u:
        curr_v = parent.get(curr_v, 0)
        depth_v -= 1

    # 4. Lockstep upward traversal
    while curr_u != curr_v:
        curr_u = parent.get(curr_u, 0)
        curr_v = parent.get(curr_v, 0)
        if curr_u == 0 or curr_v == 0:
            break

    return curr_u


def oracle_kth_ancestor_naive(parent: Dict[int, int], u: int, k: int) -> int:
    """
    O(k) naive parent stepping.
    """
    curr = u
    for _ in range(k):
        if curr not in parent or parent[curr] == 0:
            return 0
        curr = parent[curr]
    return curr


def oracle_tree_diameter_all_pairs(n: int, adj: Dict[int, List[int]]) -> int:
    """
    Computes diameter by running BFS from every single vertex u in V.
    O(V * (V + E)) naive metric scan.
    Completely independent from two-sweep BFS and tree DP.
    """
    max_dist = 0
    for start in range(1, n + 1):
        dist = {i: -1 for i in range(1, n + 1)}
        dist[start] = 0
        q = deque([start])
        while q:
            u = q.popleft()
            max_dist = max(max_dist, dist[u])
            for v in adj.get(u, []):
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    q.append(v)
    return max_dist


def oracle_subtree_aggregate_fresh_dfs(
    root: int,
    children: Dict[int, List[int]],
    values: Dict[int, Any],
    op: str = "SUM"
) -> Any:
    """
    Computes subtree aggregate by running a fresh, isolated recursive DFS
    traversing only the descendants of root from scratch.
    Zero interval flattening, zero Fenwick/Segment Tree, zero memoization.
    """
    acc = values.get(root, 0)
    for c in children.get(root, []):
        child_val = oracle_subtree_aggregate_fresh_dfs(c, children, values, op)
        if op == "SUM":
            acc += child_val
        elif op == "XOR":
            acc ^= child_val
        elif op == "MIN":
            acc = min(acc, child_val)
        elif op == "MAX":
            acc = max(acc, child_val)
    return acc


def oracle_tree_independent_set_bitmask(
    n: int,
    edges: List[Tuple[int, int]],
    weights: Dict[int, int]
) -> int:
    """
    Solves Maximum Weight Independent Set via brute-force exponential subset enumeration.
    Valid for small n (n <= 16).
    Checks all 2^N subsets against adjacency, finding maximum weight sum.
    100% independent from Tree DP.
    """
    edge_set = set()
    for u, v in edges:
        edge_set.add((min(u, v), max(u, v)))

    best_weight = 0
    for mask in range(1 << n):
        # Check if mask is an independent set
        is_independent = True
        chosen = [i + 1 for i in range(n) if (mask >> i) & 1]
        for i in range(len(chosen)):
            for j in range(i + 1, len(chosen)):
                u, v = chosen[i], chosen[j]
                if (min(u, v), max(u, v)) in edge_set:
                    is_independent = False
                    break
            if not is_independent:
                break

        if is_independent:
            cur_weight = sum(weights.get(v, 0) for v in chosen)
            best_weight = max(best_weight, cur_weight)

    return best_weight


def oracle_path_aggregate_bfs(
    n: int,
    adj: Dict[int, List[int]],
    values: Dict[int, Any],
    start: int,
    target: int,
    op: str = "SUM"
) -> Any:
    """
    Runs single-source BFS from start to target, reconstructs simple path,
    and directly aggregates node values.
    Zero LCA, zero prefix arrays, zero HLD.
    """
    parent = {start: None}
    q = deque([start])
    while q:
        u = q.popleft()
        if u == target:
            break
        for v in adj.get(u, []):
            if v not in parent:
                parent[v] = u
                q.append(v)

    # Reconstruct path
    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = parent.get(curr)
    path.reverse()

    if not path or path[0] != start:
        return 0

    acc = values.get(path[0], 0)
    for node in path[1:]:
        val = values.get(node, 0)
        if op == "SUM":
            acc += val
        elif op == "XOR":
            acc ^= val
        elif op == "MIN":
            acc = min(acc, val)
        elif op == "MAX":
            acc = max(acc, val)
    return acc


def oracle_tree_difference_brute_force(
    n: int,
    adj: Dict[int, List[int]],
    updates: List[Tuple[int, int, int]]
) -> Dict[int, int]:
    """
    Naive baseline for Gate 8 extensibility:
    For each path update (u, v, x), finds the simple path via BFS and
    directly increments each node's value.
    """
    vals = {i: 0 for i in range(1, n + 1)}
    for u, v, x in updates:
        # BFS path find
        parent = {u: None}
        q = deque([u])
        while q:
            curr = q.popleft()
            if curr == v:
                break
            for nxt in adj.get(curr, []):
                if nxt not in parent:
                    parent[nxt] = curr
                    q.append(nxt)

        curr = v
        while curr is not None:
            vals[curr] += x
            curr = parent.get(curr)

    return vals
