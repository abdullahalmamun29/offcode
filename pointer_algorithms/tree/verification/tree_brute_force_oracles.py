"""
Independent Brute-Force Oracles for Tree Domain (Phase 3E).

These functions serve as ground truth for all Tree benchmark, randomized tests,
and property verifications. None of these functions use the pipeline; they use naive,
independent Python algorithms and exhaustive checks.
"""

from collections import deque
from typing import List, Dict, Tuple, Optional, Any

def oracle_tree_dfs_preorder(n: int, edges: List[Tuple[int, int]], root: int = 1) -> List[int]:
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    order = []
    def dfs(u: int, p: int):
        order.append(u)
        for v in sorted(adj[u]):
            if v != p:
                dfs(v, u)
    dfs(root, 0)
    return order

def oracle_tree_dfs_inorder(nodes: Dict[int, Tuple[int, int, int]], root: int) -> List[int]:
    order = []
    def dfs(u: int):
        if u == -1:
            return
        val, left, right = nodes[u]
        dfs(left)
        order.append(val)
        dfs(right)
    dfs(root)
    return order

def oracle_tree_dfs_postorder(nodes: Dict[int, Tuple[int, int, int]], root: int) -> List[int]:
    order = []
    def dfs(u: int):
        if u == -1:
            return
        val, left, right = nodes[u]
        dfs(left)
        dfs(right)
        order.append(val)
    dfs(root)
    return order

def oracle_tree_bfs_level_order(n: int, edges: List[Tuple[int, int]], root: int = 1) -> List[int]:
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    order = []
    vis = set([root])
    q = deque([root])
    while q:
        u = q.popleft()
        order.append(u)
        for v in sorted(adj[u]):
            if v not in vis:
                vis.add(v)
                q.append(v)
    return order

def oracle_tree_height(n: int, edges: List[Tuple[int, int]], root: int = 1) -> int:
    if n <= 0:
        return 0
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    def dfs(u: int, p: int) -> int:
        h = 0
        for v in adj[u]:
            if v != p:
                h = max(h, dfs(v, u))
        return 1 + h
    return dfs(root, 0)

def oracle_tree_subtree_sizes(n: int, edges: List[Tuple[int, int]], root: int = 1) -> List[int]:
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    sz = [0] * (n + 1)
    def dfs(u: int, p: int) -> int:
        s = 1
        for v in adj[u]:
            if v != p:
                s += dfs(v, u)
        sz[u] = s
        return s
    dfs(root, 0)
    return sz[1:]

def oracle_tree_leaf_count(n: int, edges: List[Tuple[int, int]], root: int = 1) -> int:
    if n <= 0:
        return 0
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    def dfs(u: int, p: int) -> int:
        children = [v for v in adj[u] if v != p]
        if not children:
            return 1
        return sum(dfs(v, u) for v in children)
    return dfs(root, 0)

def oracle_tree_subtree_sum(n: int, edges: List[Tuple[int, int]], values: List[int], root: int = 1) -> List[int]:
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    ans = [0] * (n + 1)
    def dfs(u: int, p: int) -> int:
        total = values[u - 1]
        for v in adj[u]:
            if v != p:
                total += dfs(v, u)
        ans[u] = total
        return total
    dfs(root, 0)
    return ans[1:]

def oracle_tree_path_sum(nodes: Dict[int, Tuple[int, int, int]], root: int, target: int) -> bool:
    def dfs(u: int, rem: int) -> bool:
        if u == -1:
            return False
        val, left, right = nodes[u]
        rem -= val
        if left == -1 and right == -1:
            return rem == 0
        return dfs(left, rem) or dfs(right, rem)
    return dfs(root, target)

def oracle_tree_diameter(n: int, edges: List[Tuple[int, int]]) -> int:
    if n <= 1:
        return 0
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    # 2-BFS method for diameter
    def bfs_farthest(start: int) -> Tuple[int, int]:
        dist = {i: -1 for i in range(1, n + 1)}
        dist[start] = 0
        q = deque([start])
        farthest_node = start
        while q:
            u = q.popleft()
            if dist[u] > dist[farthest_node]:
                farthest_node = u
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    q.append(v)
        return farthest_node, dist[farthest_node]
    
    u, _ = bfs_farthest(1)
    _, d = bfs_farthest(u)
    return d

def oracle_bst_search(keys: List[int], target: int) -> bool:
    return target in set(keys)

def oracle_bst_validate(nodes: Dict[int, Tuple[int, int, int]], root: int) -> bool:
    inorder = oracle_tree_dfs_inorder(nodes, root)
    for i in range(len(inorder) - 1):
        if inorder[i] >= inorder[i + 1]:
            return False
    return True

def oracle_lca_binary_tree(nodes: Dict[int, Tuple[int, int, int]], root: int, p: int, q: int) -> int:
    def dfs(u: int) -> Optional[int]:
        if u == -1 or u == p or u == q:
            return u
        val, left, right = nodes[u]
        l = dfs(left)
        r = dfs(right)
        if l != -1 and r != -1:
            return u
        return l if l != -1 else r
    res = dfs(root)
    return res if res is not None else -1

def oracle_lca_bst(keys: List[int], p: int, q: int) -> int:
    class BSTNode:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None
    
    root = None
    for k in keys:
        if root is None:
            root = BSTNode(k)
        else:
            curr = root
            while True:
                if k < curr.val:
                    if curr.left is None:
                        curr.left = BSTNode(k)
                        break
                    curr = curr.left
                elif k > curr.val:
                    if curr.right is None:
                        curr.right = BSTNode(k)
                        break
                    curr = curr.right
                else:
                    break
    
    curr = root
    while curr:
        if p < curr.val and q < curr.val:
            curr = curr.left
        elif p > curr.val and q > curr.val:
            curr = curr.right
        else:
            return curr.val
    return -1

def oracle_lca_parent_array(parents: List[int], p: int, q: int) -> int:
    # 1-indexed parents
    ancestors_p = set()
    curr = p
    while curr != 0 and curr < len(parents):
        ancestors_p.add(curr)
        curr = parents[curr]
    curr = q
    while curr != 0 and curr < len(parents):
        if curr in ancestors_p:
            return curr
        curr = parents[curr]
    return 0

def oracle_tree_independent_set(n: int, edges: List[Tuple[int, int]], values: List[int], root: int = 1) -> int:
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    def dfs(u: int, p: int) -> Tuple[int, int]:
        include = values[u - 1]
        exclude = 0
        for v in adj[u]:
            if v != p:
                inc_v, exc_v = dfs(v, u)
                include += exc_v
                exclude += max(inc_v, exc_v)
        return include, exclude
    
    inc, exc = dfs(root, 0)
    return max(inc, exc)

def oracle_tree_max_subtree_weight(n: int, edges: List[Tuple[int, int]], values: List[int], root: int = 1) -> int:
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    max_ans = [values[root - 1]]
    def dfs(u: int, p: int) -> int:
        s = values[u - 1]
        for v in adj[u]:
            if v != p:
                child_w = dfs(v, u)
                if child_w > 0:
                    s += child_w
        max_ans[0] = max(max_ans[0], s)
        return s
    
    dfs(root, 0)
    return max_ans[0]
