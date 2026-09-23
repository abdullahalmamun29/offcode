"""
C++17 Code Generator for Dynamic Programming Domain (Phase 3K).

Generates production-grade C++17 implementations for:
1. dp_1d_linear (Linear 1D DP)
2. dp_prefix_suffix (Prefix/Suffix Accumulation DP)
3. dp_2d_grid (Grid Path DP)
4. dp_string_alignment (String Alignment / LCS / Edit Distance DP)
5. dp_interval (Interval / Range DP)
6. dp_knapsack_01 (0/1 Knapsack)
7. dp_knapsack_unbounded (Unbounded Knapsack / Coin Change)
8. dp_tree (Tree DP / Subtree Aggregation)
9. dp_bitmask (Bitmask DP / Subset States)
10. dp_digit (Digit DP / Counting with Constraints)
11. dp_state_machine (State Machine / Multi-State DP)
12. dp_dag_longest_path (Topological / DAG DP)
13. dp_divide_and_conquer (Divide and Conquer Optimization DP)
14. dp_space_optimization (Rolling Buffer / In-Place Compressed DP)
"""

from typing import Dict, Any


def generate_dp_cpp(pattern: str, params: Dict[str, Any]) -> str:
    # ── 1. Linear 1D DP ──
    if pattern == "dp_1d_linear":
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// 1D Linear Dynamic Programming
// State: dp[i] = optimal solution considering prefix of size i
// Transition: dp[i] = max(dp[i-1], dp[i-2] + a[i]) (e.g. House Robber)
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    if (n == 1) {
        cout << max(0LL, a[0]) << "\\n";
        return 0;
    }

    vector<long long> dp(n + 1, 0);
    dp[1] = max(0LL, a[0]);
    for (int i = 2; i <= n; i++) {
        dp[i] = max(dp[i - 1], dp[i - 2] + a[i - 1]);
    }

    cout << dp[n] << "\\n";
    return 0;
}
"""

    # ── 2. Prefix / Suffix DP ──
    elif pattern in ("dp_prefix_suffix", "dp_partition"):
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Prefix / Suffix Dynamic Programming
// State: pref[i] = optimal metric on prefix a[0..i], suff[i] = optimal metric on suffix a[i..n-1]
// Split: combine at partition point k to maximize pref[k] + suff[k+1]
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n < 2) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    vector<long long> pref(n, 0);
    long long min_val = a[0];
    for (int i = 1; i < n; i++) {
        pref[i] = max(pref[i - 1], a[i] - min_val);
        min_val = min(min_val, a[i]);
    }

    vector<long long> suff(n, 0);
    long long max_val = a[n - 1];
    for (int i = n - 2; i >= 0; i--) {
        suff[i] = max(suff[i + 1], max_val - a[i]);
        max_val = max(max_val, a[i]);
    }

    long long ans = pref[n - 1];
    for (int i = 0; i < n - 1; i++) {
        ans = max(ans, pref[i] + suff[i + 1]);
    }

    cout << ans << "\\n";
    return 0;
}
"""

    # ── 3. 2D Grid DP ──
    elif pattern in ("dp_2d_grid", "dp_grid_2d"):
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// 2D Grid Dynamic Programming
// State: dp[r][c] = minimum cost path from (0, 0) to (r, c)
// Transition: dp[r][c] = grid[r][c] + min(dp[r-1][c], dp[r][c-1])
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int R, C;
    if (!(cin >> R >> C) || R <= 0 || C <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<vector<long long>> grid(R, vector<long long>(C));
    for (int r = 0; r < R; r++) {
        for (int c = 0; c < C; c++) {
            cin >> grid[r][c];
        }
    }

    vector<vector<long long>> dp(R, vector<long long>(C, 0));
    dp[0][0] = grid[0][0];

    for (int c = 1; c < C; c++) {
        dp[0][c] = dp[0][c - 1] + grid[0][c];
    }
    for (int r = 1; r < R; r++) {
        dp[r][0] = dp[r - 1][0] + grid[r][0];
    }

    for (int r = 1; r < R; r++) {
        for (int c = 1; c < C; c++) {
            dp[r][c] = grid[r][c] + min(dp[r - 1][c], dp[r][c - 1]);
        }
    }

    cout << dp[R - 1][C - 1] << "\\n";
    return 0;
}
"""

    # ── 4. String Alignment / LCS DP ──
    elif pattern in ("dp_string_alignment", "dp_subsequence_string"):
        return """#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

// String Alignment / Longest Common Subsequence DP
// State: dp[i][j] = LCS length of s1[0..i-1] and s2[0..j-1]
// Transition: dp[i][j] = (s1[i-1] == s2[j-1]) ? 1 + dp[i-1][j-1] : max(dp[i-1][j], dp[i][j-1])
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string s1, s2;
    if (!(cin >> s1 >> s2)) {
        cout << 0 << "\\n";
        return 0;
    }

    int n = s1.size();
    int m = s2.size();

    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (s1[i - 1] == s2[j - 1]) {
                dp[i][j] = 1 + dp[i - 1][j - 1];
            } else {
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    cout << dp[n][m] << "\\n";
    return 0;
}
"""

    # ── 5. Interval DP ──
    elif pattern == "dp_interval":
        return """#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

// Interval / Range Dynamic Programming
// State: dp[i][j] = optimal cost to merge/process segment a[i..j]
// Transition: dp[i][j] = min_{k} (dp[i][k] + dp[k+1][j] + cost(i, j))
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<long long> a(n);
    vector<long long> pref(n + 1, 0);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
        pref[i + 1] = pref[i] + a[i];
    }

    auto range_sum = [&](int l, int r) -> long long {
        return pref[r + 1] - pref[l];
    };

    vector<vector<long long>> dp(n, vector<long long>(n, 0));

    for (int len = 2; len <= n; len++) {
        for (int i = 0; i + len - 1 < n; i++) {
            int j = i + len - 1;
            dp[i][j] = LLONG_MAX;
            long long cost = range_sum(i, j);
            for (int k = i; k < j; k++) {
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + cost);
            }
        }
    }

    cout << dp[0][n - 1] << "\\n";
    return 0;
}
"""

    # ── 6. Knapsack (0/1 or Unbounded) ──
    elif pattern in ("dp_knapsack_01", "dp_knapsack", "dp_knapsack_unbounded"):
        if pattern == "dp_knapsack_unbounded" or params.get("dp_is_unbounded"):
            return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Unbounded Knapsack / Complete Knapsack Dynamic Programming
// State: dp[w] = max value achievable with capacity w using unlimited items
// Transition: dp[w] = max(dp[w], dp[w - weight[i]] + value[i]), forward loop
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    long long W;
    if (!(cin >> n >> W) || n <= 0 || W <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<long long> weights(n);
    vector<long long> values(n);
    for (int i = 0; i < n; i++) {
        cin >> weights[i] >> values[i];
    }

    vector<long long> dp(W + 1, 0);

    for (int i = 0; i < n; i++) {
        for (long long w = weights[i]; w <= W; w++) {
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }

    cout << dp[W] << "\\n";
    return 0;
}
"""
        else:
            return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// 0/1 Knapsack Dynamic Programming
// State: dp[w] = max value achievable with capacity w
// Transition: dp[w] = max(dp[w], dp[w - weight[i]] + value[i]), reverse loop for 0/1
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    long long W;
    if (!(cin >> n >> W) || n <= 0 || W <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<long long> weights(n);
    vector<long long> values(n);
    for (int i = 0; i < n; i++) {
        cin >> weights[i] >> values[i];
    }

    vector<long long> dp(W + 1, 0);

    for (int i = 0; i < n; i++) {
        for (long long w = W; w >= weights[i]; w--) {
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }

    cout << dp[W] << "\\n";
    return 0;
}
"""

    # ── 8. Tree DP ──
    elif pattern == "dp_tree":
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Tree Dynamic Programming (Maximum Weight Independent Set)
// State: dp[u][0] = max weight in subtree u when u is NOT chosen
//        dp[u][1] = max weight in subtree u when u IS chosen
// Transition: dp[u][0] = sum_{v in children} max(dp[v][0], dp[v][1])
//             dp[u][1] = weight[u] + sum_{v in children} dp[v][0]
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<long long> val(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> val[i];
    }

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    vector<vector<long long>> dp(n + 1, vector<long long>(2, 0));

    auto dfs = [&](auto& self, int u, int p) -> void {
        dp[u][0] = 0;
        dp[u][1] = val[u];
        for (int v : adj[u]) {
            if (v == p) continue;
            self(self, v, u);
            dp[u][0] += max(dp[v][0], dp[v][1]);
            dp[u][1] += dp[v][0];
        }
    };

    dfs(dfs, 1, 0);

    cout << max(dp[1][0], dp[1][1]) << "\\n";
    return 0;
}
"""

    # ── 9. Bitmask DP ──
    elif pattern == "dp_bitmask":
        return """#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

// Bitmask Dynamic Programming (Traveling Salesperson / Assignment)
// State: dp[mask][u] = min cost to visit subset 'mask' ending at vertex 'u'
// Transition: dp[mask | (1 << v)][v] = min(dp[mask | (1 << v)][v], dp[mask][u] + dist[u][v])
const long long INF = 1e18;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<vector<long long>> dist(n, vector<long long>(n));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> dist[i][j];
        }
    }

    int total_masks = 1 << n;
    vector<vector<long long>> dp(total_masks, vector<long long>(n, INF));
    dp[1][0] = 0; // start at node 0

    for (int mask = 1; mask < total_masks; mask++) {
        for (int u = 0; u < n; u++) {
            if (!(mask & (1 << u)) || dp[mask][u] == INF) continue;
            for (int v = 0; v < n; v++) {
                if (mask & (1 << v)) continue;
                int next_mask = mask | (1 << v);
                dp[next_mask][v] = min(dp[next_mask][v], dp[mask][u] + dist[u][v]);
            }
        }
    }

    long long ans = INF;
    for (int u = 0; u < n; u++) {
        if (dp[total_masks - 1][u] != INF) {
            ans = min(ans, dp[total_masks - 1][u] + dist[u][0]);
        }
    }

    cout << (ans == INF ? -1 : ans) << "\\n";
    return 0;
}
"""

    # ── 10. Digit DP ──
    elif pattern == "dp_digit":
        return """#include <iostream>
#include <string>
#include <vector>
#include <cstring>

using namespace std;

// Digit Dynamic Programming
// State: memo[idx][sum][tight][started] = count of valid suffixes
long long memo[20][200][2][2];
string S;

long long solve_digit(int idx, int sum, bool tight, bool started) {
    if (idx == (int)S.size()) {
        return (started && sum > 0) ? 1 : 0;
    }
    if (memo[idx][sum][tight][started] != -1) {
        return memo[idx][sum][tight][started];
    }

    long long ans = 0;
    int limit = tight ? (S[idx] - '0') : 9;

    for (int d = 0; d <= limit; d++) {
        bool next_tight = tight && (d == limit);
        bool next_started = started || (d > 0);
        int next_sum = sum + d;
        ans += solve_digit(idx + 1, next_sum, next_tight, next_started);
    }

    return memo[idx][sum][tight][started] = ans;
}

long long count_valid(long long n) {
    if (n <= 0) return 0;
    S = to_string(n);
    memset(memo, -1, sizeof(memo));
    return solve_digit(0, 0, true, false);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    long long L, R;
    if (!(cin >> L >> R)) return 0;

    cout << count_valid(R) - count_valid(L - 1) << "\\n";
    return 0;
}
"""

    # ── 11. State Machine DP ──
    elif pattern == "dp_state_machine":
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// State Machine Dynamic Programming (Stock Trading with Cooldown)
// States:
//   s0[i]: Rest state (no stock held, ready to buy)
//   s1[i]: Hold state (stock held, ready to sell)
//   s2[i]: Cooldown state (just sold, cannot buy today)
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 1) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<long long> prices(n);
    for (int i = 0; i < n; i++) {
        cin >> prices[i];
    }

    long long s0 = 0;
    long long s1 = -prices[0];
    long long s2 = 0;

    for (int i = 1; i < n; i++) {
        long long prev_s0 = s0;
        long long prev_s1 = s1;
        long long prev_s2 = s2;

        s0 = max(prev_s0, prev_s2);
        s1 = max(prev_s1, prev_s0 - prices[i]);
        s2 = prev_s1 + prices[i];
    }

    cout << max(s0, s2) << "\\n";
    return 0;
}
"""

    # ── 12. DAG Longest Path DP ──
    elif pattern in ("dp_dag_longest_path", "dp_dag"):
        return """#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

// Topological / DAG Dynamic Programming
// State: dp[u] = length of longest path ending at node u
// Transition: processed in topological order: dp[v] = max(dp[v], dp[u] + weight(u, v))
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<vector<pair<int, long long>>> adj(n + 1);
    vector<int> in_degree(n + 1, 0);

    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        adj[u].push_back({v, w});
        in_degree[v]++;
    }

    queue<int> q;
    for (int i = 1; i <= n; i++) {
        if (in_degree[i] == 0) {
            q.push(i);
        }
    }

    vector<long long> dp(n + 1, 0);
    long long max_path = 0;

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        for (auto& edge : adj[u]) {
            int v = edge.first;
            long long w = edge.second;
            dp[v] = max(dp[v], dp[u] + w);
            max_path = max(max_path, dp[v]);
            if (--in_degree[v] == 0) {
                q.push(v);
            }
        }
    }

    cout << max_path << "\\n";
    return 0;
}
"""

    # ── 13. Divide and Conquer Optimization DP ──
    elif pattern in ("dp_divide_and_conquer", "dp_optimization"):
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Divide and Conquer DP Optimization
// State: dp[k][i] = optimal partitioning of prefix a[0..i-1] into k segments
// Condition: opt(k, i) <= opt(k, i + 1) due to quadrangle inequality
const long long INF = 1e18;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, K;
    if (!(cin >> n >> K) || n <= 0 || K <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    auto cost = [&](int l, int r) -> long long {
        // Sample monotonic cost function: (r - l + 1) * max(a[l..r]) or squared sum
        long long s = 0;
        for (int i = l; i <= r; i++) s += a[i];
        return s * (r - l + 1);
    };

    vector<long long> dp_prev(n + 1, INF);
    vector<long long> dp_curr(n + 1, INF);
    dp_prev[0] = 0;

    auto compute = [&](auto& self, int l, int r, int opt_l, int opt_r) -> void {
        if (l > r) return;
        int mid = l + (r - l) / 2;
        int best_opt = -1;
        dp_curr[mid] = INF;

        for (int k = opt_l; k <= min(mid - 1, opt_r); k++) {
            if (dp_prev[k] == INF) continue;
            long long val = dp_prev[k] + cost(k, mid - 1);
            if (val < dp_curr[mid]) {
                dp_curr[mid] = val;
                best_opt = k;
            }
        }

        self(self, l, mid - 1, opt_l, best_opt != -1 ? best_opt : opt_r);
        self(self, mid + 1, r, best_opt != -1 ? best_opt : opt_l, opt_r);
    };

    for (int k = 1; k <= K; k++) {
        compute(compute, 1, n, 0, n - 1);
        dp_prev = dp_curr;
        fill(dp_curr.begin(), dp_curr.end(), INF);
    }

    cout << dp_prev[n] << "\\n";
    return 0;
}
"""

    # ── 14. Space Optimized DP ──
    elif pattern == "dp_space_optimization":
        return """#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>

using namespace std;

// Space-Optimized Dynamic Programming (Rolling Vector / In-Place Compression)
// State: dp[w] compressed from dp[i][w] since each state depends only on previous row
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    long long W;
    if (!(cin >> n >> W) || n <= 0 || W <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<long long> weights(n);
    vector<long long> values(n);
    for (int i = 0; i < n; i++) {
        cin >> weights[i] >> values[i];
    }

    // Space reduced from O(N * W) to O(W)
    vector<long long> dp(W + 1, 0);

    for (int i = 0; i < n; i++) {
        for (long long w = W; w >= weights[i]; w--) {
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }

    cout << dp[W] << "\\n";
    return 0;
}
"""

    # ── 15. Solution Reconstruction DP ──
    elif pattern in ("dp_solution_reconstruction", "dp_reconstruction"):
        return """#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

// DP Solution Reconstruction (Longest Common Subsequence / Path Recovery)
// State: dp[i][j] = length of LCS
// Reconstruction: backtrack using parent decisions
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string s1, s2;
    if (!(cin >> s1 >> s2)) {
        cout << "\\n";
        return 0;
    }

    int n = s1.size(), m = s2.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (s1[i - 1] == s2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    // Reconstruction phase: backtrack from (n, m)
    string lcs = "";
    int i = n, j = m;
    while (i > 0 && j > 0) {
        if (s1[i - 1] == s2[j - 1]) {
            lcs.push_back(s1[i - 1]);
            i--; j--;
        } else if (dp[i - 1][j] >= dp[i][j - 1]) {
            i--;
        } else {
            j--;
        }
    }
    reverse(lcs.begin(), lcs.end());
    cout << lcs << "\\n";
    return 0;
}
"""

    # Fallback default
    return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cout << 0 << "\\n";
    return 0;
}
"""
