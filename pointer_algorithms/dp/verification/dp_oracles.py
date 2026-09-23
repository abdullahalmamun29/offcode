"""
Reference Oracles and Brute-Force Implementations for Dynamic Programming Domain (Phase 3K).

Provides clean, verifiable reference implementations for all 14 Dynamic Programming patterns:
1. Linear 1D DP (House Robber / Maximum Non-Adjacent Sum)
2. Prefix / Suffix DP (Two-Transaction Stock Trading)
3. 2D Grid DP (Minimum Cost Grid Path)
4. String Alignment DP (Longest Common Subsequence)
5. Interval DP (Minimum Cost Segment Merging)
6. 0/1 Knapsack DP (Bounded Capacity Subset Selection)
7. Unbounded Knapsack DP (Unlimited Capacity Optimization / Coin Change)
8. Tree DP (Maximum Weight Independent Set on Tree)
9. Bitmask DP (Traveling Salesperson Problem)
10. Digit DP (Constraint Digit Counting in Range [L, R])
11. State Machine DP (Stock Trading with Mandatory Cooldown)
12. DAG Longest Path DP (Topological Longest Path on DAG)
13. Divide and Conquer DP (Optimal K-Partitioning with Quadrangle Inequality)
14. Space Optimized DP (Rolling Vector In-Place Compression)

Includes matching brute-force reference oracles for differential testing.
"""

from typing import List, Tuple, Dict, Any, Optional
import math
import itertools
from functools import lru_cache


# ── 1. Linear 1D DP Oracle ──

def dp_1d_linear_oracle(nums: List[int]) -> int:
    """1D Linear DP: Maximum sum without picking adjacent elements."""
    n = len(nums)
    if n == 0:
        return 0
    if n == 1:
        return max(0, nums[0])
    dp = [0] * (n + 1)
    dp[1] = max(0, nums[0])
    for i in range(2, n + 1):
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i - 1])
    return dp[n]


def brute_force_1d_linear(nums: List[int]) -> int:
    """Brute-force verification by recursion."""
    def helper(idx: int) -> int:
        if idx >= len(nums):
            return 0
        pick = max(0, nums[idx]) + helper(idx + 2)
        skip = helper(idx + 1)
        return max(pick, skip)
    return helper(0)


# ── 2. Prefix / Suffix DP Oracle ──

def dp_prefix_suffix_oracle(prices: List[int]) -> int:
    """Prefix/Suffix DP: Maximum profit with at most 2 stock transactions."""
    n = len(prices)
    if n < 2:
        return 0
    pref = [0] * n
    min_val = prices[0]
    for i in range(1, n):
        pref[i] = max(pref[i - 1], prices[i] - min_val)
        min_val = min(min_val, prices[i])

    suff = [0] * n
    max_val = prices[n - 1]
    for i in range(n - 2, -1, -1):
        suff[i] = max(suff[i + 1], max_val - prices[i])
        max_val = max(max_val, prices[i])

    ans = pref[n - 1]
    for i in range(n - 1):
        ans = max(ans, pref[i] + suff[i + 1])
    return ans


def brute_force_prefix_suffix(prices: List[int]) -> int:
    """Brute force: try all possible split points between two transactions."""
    n = len(prices)
    if n < 2:
        return 0

    def single_trans(sub: List[int]) -> int:
        if len(sub) < 2:
            return 0
        min_p = sub[0]
        profit = 0
        for p in sub[1:]:
            profit = max(profit, p - min_p)
            min_p = min(min_p, p)
        return profit

    ans = single_trans(prices)
    for split in range(1, n):
        left = single_trans(prices[:split])
        right = single_trans(prices[split:])
        ans = max(ans, left + right)
    return ans


# ── 3. 2D Grid DP Oracle ──

def dp_2d_grid_oracle(grid: List[List[int]]) -> int:
    """2D Grid DP: Minimum cost path from (0,0) to (R-1, C-1)."""
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    dp = [[0] * C for _ in range(R)]
    dp[0][0] = grid[0][0]
    for c in range(1, C):
        dp[0][c] = dp[0][c - 1] + grid[0][c]
    for r in range(1, R):
        dp[r][0] = dp[r - 1][0] + grid[r][0]
    for r in range(1, R):
        for c in range(1, C):
            dp[r][c] = grid[r][c] + min(dp[r - 1][c], dp[r][c - 1])
    return dp[R - 1][C - 1]


def brute_force_2d_grid(grid: List[List[int]]) -> int:
    """Brute force DFS for grid paths."""
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])

    def dfs(r: int, c: int) -> int:
        if r == R - 1 and c == C - 1:
            return grid[r][c]
        res = math.inf
        if r + 1 < R:
            res = min(res, grid[r][c] + dfs(r + 1, c))
        if c + 1 < C:
            res = min(res, grid[r][c] + dfs(r, c + 1))
        return int(res)

    return dfs(0, 0)


# ── 4. String Alignment / LCS DP Oracle ──

def dp_string_alignment_oracle(s1: str, s2: str) -> int:
    """LCS DP."""
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m]


def brute_force_string_alignment(s1: str, s2: str) -> int:
    """Brute force recursive LCS."""
    @lru_cache(maxsize=None)
    def lcs(i: int, j: int) -> int:
        if i == len(s1) or j == len(s2):
            return 0
        if s1[i] == s2[j]:
            return 1 + lcs(i + 1, j + 1)
        return max(lcs(i + 1, j), lcs(i, j + 1))
    return lcs(0, 0)


# ── 5. Interval DP Oracle ──

def dp_interval_oracle(nums: List[int]) -> int:
    """Interval DP: Minimum cost to merge array elements into one segment."""
    n = len(nums)
    if n <= 1:
        return 0
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + nums[i]

    def range_sum(l: int, r: int) -> int:
        return pref[r + 1] - pref[l]

    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost = range_sum(i, j)
            dp[i][j] = min(dp[i][k] + dp[k + 1][j] + cost for k in range(i, j))
    return dp[0][n - 1]


def brute_force_interval(nums: List[int]) -> int:
    """Brute force recursive interval evaluation."""
    n = len(nums)
    if n <= 1:
        return 0

    @lru_cache(maxsize=None)
    def solve(i: int, j: int) -> int:
        if i == j:
            return 0
        cost = sum(nums[i:j + 1])
        return min(solve(i, k) + solve(k + 1, j) + cost for k in range(i, j))

    return solve(0, n - 1)


# ── 6. 0/1 Knapsack Oracle ──

def dp_knapsack_01_oracle(weights: List[int], values: List[int], W: int) -> int:
    """0/1 Knapsack DP."""
    n = len(weights)
    dp = [0] * (W + 1)
    for i in range(n):
        w_i, v_i = weights[i], values[i]
        for w in range(W, w_i - 1, -1):
            dp[w] = max(dp[w], dp[w - w_i] + v_i)
    return dp[W]


def brute_force_knapsack_01(weights: List[int], values: List[int], W: int) -> int:
    """Brute force 0/1 knapsack by testing all subsets."""
    n = len(weights)
    max_val = 0
    for mask in range(1 << n):
        total_w = sum(weights[i] for i in range(n) if (mask & (1 << i)))
        if total_w <= W:
            total_v = sum(values[i] for i in range(n) if (mask & (1 << i)))
            max_val = max(max_val, total_v)
    return max_val


# ── 7. Unbounded Knapsack Oracle ──

def dp_knapsack_unbounded_oracle(weights: List[int], values: List[int], W: int) -> int:
    """Unbounded Knapsack DP."""
    dp = [0] * (W + 1)
    for w_i, v_i in zip(weights, values):
        for w in range(w_i, W + 1):
            dp[w] = max(dp[w], dp[w - w_i] + v_i)
    return dp[W]


def brute_force_knapsack_unbounded(weights: List[int], values: List[int], W: int) -> int:
    """Brute force recursive unbounded knapsack."""
    @lru_cache(maxsize=None)
    def solve(rem: int) -> int:
        best = 0
        for w, v in zip(weights, values):
            if rem >= w:
                best = max(best, v + solve(rem - w))
        return best
    return solve(W)


# ── 8. Tree DP Oracle ──

def dp_tree_oracle(n: int, edges: List[Tuple[int, int]], values: List[int]) -> int:
    """Tree DP: Maximum Weight Independent Set."""
    if n <= 0:
        return 0
    adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    dp = {i: [0, 0] for i in range(1, n + 1)}

    def dfs(u: int, p: int) -> None:
        dp[u][0] = 0
        dp[u][1] = values[u - 1]
        for v in adj[u]:
            if v == p:
                continue
            dfs(v, u)
            dp[u][0] += max(dp[v][0], dp[v][1])
            dp[u][1] += dp[v][0]

    dfs(1, 0)
    return max(dp[1][0], dp[1][1])


def brute_force_tree(n: int, edges: List[Tuple[int, int]], values: List[int]) -> int:
    """Brute force independent set over all 2^n subsets."""
    edge_set = set()
    for u, v in edges:
        edge_set.add((min(u, v), max(u, v)))

    best = 0
    for mask in range(1 << n):
        chosen = [i + 1 for i in range(n) if (mask & (1 << i))]
        valid = True
        for i in range(len(chosen)):
            for j in range(i + 1, len(chosen)):
                u, v = min(chosen[i], chosen[j]), max(chosen[i], chosen[j])
                if (u, v) in edge_set:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            val = sum(values[i - 1] for i in chosen)
            best = max(best, val)
    return best


# ── 9. Bitmask DP Oracle ──

def dp_bitmask_oracle(n: int, dist: List[List[int]]) -> int:
    """TSP / Bitmask DP."""
    if n <= 1:
        return 0
    total = 1 << n
    dp = [[math.inf] * n for _ in range(total)]
    dp[1][0] = 0

    for mask in range(1, total):
        for u in range(n):
            if not (mask & (1 << u)) or dp[mask][u] == math.inf:
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                next_mask = mask | (1 << v)
                dp[next_mask][v] = min(dp[next_mask][v], dp[mask][u] + dist[u][v])

    ans = math.inf
    for u in range(n):
        if dp[total - 1][u] != math.inf:
            ans = min(ans, dp[total - 1][u] + dist[u][0])
    return int(ans) if ans != math.inf else -1


def brute_force_bitmask(n: int, dist: List[List[int]]) -> int:
    """Brute force TSP checking all (n-1)! permutations."""
    if n <= 1:
        return 0
    cities = list(range(1, n))
    best = math.inf
    for p in itertools.permutations(cities):
        cost = dist[0][p[0]]
        for i in range(len(p) - 1):
            cost += dist[p[i]][p[i + 1]]
        cost += dist[p[-1]][0]
        best = min(best, cost)
    return int(best)


# ── 10. Digit DP Oracle ──

def dp_digit_oracle(low: int, high: int) -> int:
    """Digit DP: count positive numbers with at least one non-zero digit sum."""
    def count_up_to(n: int) -> int:
        if n <= 0:
            return 0
        s = str(n)
        memo: Dict[Tuple[int, int, bool, bool], int] = {}

        def solve(idx: int, digit_sum: int, tight: bool, started: bool) -> int:
            if idx == len(s):
                return 1 if (started and digit_sum > 0) else 0
            key = (idx, digit_sum, tight, started)
            if key in memo:
                return memo[key]
            ans = 0
            limit = int(s[idx]) if tight else 9
            for d in range(limit + 1):
                ans += solve(
                    idx + 1,
                    digit_sum + d,
                    tight and (d == limit),
                    started or (d > 0)
                )
            memo[key] = ans
            return ans

        return solve(0, 0, True, False)

    return count_up_to(high) - count_up_to(low - 1)


def brute_force_digit(low: int, high: int) -> int:
    """Brute force: iterate directly over range [low, high]."""
    count = 0
    for x in range(max(1, low), high + 1):
        if sum(int(d) for d in str(x)) > 0:
            count += 1
    return count


# ── 11. State Machine DP Oracle ──

def dp_state_machine_oracle(prices: List[int]) -> int:
    """State Machine DP: stock trading with 1-day cooldown."""
    n = len(prices)
    if n <= 1:
        return 0
    s0, s1, s2 = 0, -prices[0], 0
    for i in range(1, n):
        prev_s0, prev_s1, prev_s2 = s0, s1, s2
        s0 = max(prev_s0, prev_s2)
        s1 = max(prev_s1, prev_s0 - prices[i])
        s2 = prev_s1 + prices[i]
    return max(s0, s2)


def brute_force_state_machine(prices: List[int]) -> int:
    """Brute force recursive stock trading with cooldown."""
    n = len(prices)

    @lru_cache(maxsize=None)
    def trade(i: int, state: int) -> int:
        # state: 0 = unheld, 1 = held, 2 = cooldown
        if i >= n:
            return 0
        if state == 0:
            buy = -prices[i] + trade(i + 1, 1)
            rest = trade(i + 1, 0)
            return max(buy, rest)
        elif state == 1:
            sell = prices[i] + trade(i + 1, 2)
            hold = trade(i + 1, 1)
            return max(sell, hold)
        else: # cooldown
            return trade(i + 1, 0)

    return trade(0, 0)


# ── 12. DAG Longest Path Oracle ──

def dp_dag_longest_path_oracle(n: int, edges: List[Tuple[int, int, int]]) -> int:
    """Topological DP: longest path in a directed acyclic graph."""
    adj: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, n + 1)}
    in_deg = {i: 0 for i in range(1, n + 1)}
    for u, v, w in edges:
        adj[u].append((v, w))
        in_deg[v] += 1

    queue = [u for u in range(1, n + 1) if in_deg[u] == 0]
    dp = {i: 0 for i in range(1, n + 1)}
    max_path = 0

    while queue:
        u = queue.pop(0)
        for v, w in adj[u]:
            dp[v] = max(dp[v], dp[u] + w)
            max_path = max(max_path, dp[v])
            in_deg[v] -= 1
            if in_deg[v] == 0:
                queue.append(v)
    return max_path


def brute_force_dag_longest_path(n: int, edges: List[Tuple[int, int, int]]) -> int:
    """Brute force DFS on DAG."""
    adj: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, n + 1)}
    for u, v, w in edges:
        adj[u].append((v, w))

    def dfs(u: int) -> int:
        best = 0
        for v, w in adj[u]:
            best = max(best, w + dfs(v))
        return best

    return max((dfs(u) for u in range(1, n + 1)), default=0)


# ── 13. Divide and Conquer DP Oracle ──

def dp_divide_and_conquer_oracle(n: int, K: int, cost_fn) -> int:
    """D&C DP optimization: partitioning prefix into K segments."""
    dp_prev = [cost_fn(0, i) for i in range(n)]

    for k in range(2, K + 1):
        dp_curr = [math.inf] * n

        def compute(l: int, r: int, opt_l: int, opt_r: int) -> None:
            if l > r:
                return
            mid = (l + r) // 2
            best_opt = -1
            for opt in range(opt_l, min(mid, opt_r + 1)):
                val = dp_prev[opt] + cost_fn(opt + 1, mid)
                if val < dp_curr[mid]:
                    dp_curr[mid] = val
                    best_opt = opt
            if best_opt != -1:
                compute(l, mid - 1, opt_l, best_opt)
                compute(mid + 1, r, best_opt, opt_r)
            else:
                compute(l, mid - 1, opt_l, opt_r)
                compute(mid + 1, r, opt_l, opt_r)

        compute(k - 1, n - 1, k - 2, n - 1)
        dp_prev = dp_curr

    return int(dp_prev[n - 1])


def brute_force_divide_and_conquer(n: int, K: int, cost_fn) -> int:
    """Standard O(K * N^2) DP oracle."""
    dp = [[math.inf] * n for _ in range(K + 1)]
    for i in range(n):
        dp[1][i] = cost_fn(0, i)

    for k in range(2, K + 1):
        for i in range(k - 1, n):
            for j in range(k - 2, i):
                dp[k][i] = min(dp[k][i], dp[k - 1][j] + cost_fn(j + 1, i))

    return int(dp[K][n - 1])


# ── 14. Space Optimized DP Oracle ──

def dp_space_optimized_oracle(weights: List[int], values: List[int], W: int) -> int:
    """1D rolling array space optimized DP."""
    dp = [0] * (W + 1)
    for w_i, v_i in zip(weights, values):
        for w in range(W, w_i - 1, -1):
            dp[w] = max(dp[w], dp[w - w_i] + v_i)
    return dp[W]
