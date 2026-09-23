"""
C++17 Code Generator for Graph Domain (Phase 3F).

Generates production-grade C++17 implementations for:
1. graph_bfs_shortest_path
2. graph_dfs_traversal
3. graph_connected_components
4. graph_cycle_detection_undirected
5. graph_cycle_detection_directed
6. graph_bipartite_coloring
7. graph_dijkstra
8. graph_bellman_ford
9. graph_floyd_warshall
10. graph_topological_sort
11. graph_dag_dp
12. graph_dsu
13. graph_mst_kruskal
14. graph_mst_prim
15. graph_scc_tarjan
16. graph_bridges_articulation
"""

from typing import Dict, Any


def generate_graph_cpp(pattern: str, params: Dict[str, Any]) -> str:
    target = params.get("target", "target")

    if pattern == "graph_bfs_shortest_path":
        return """#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        if (cin >> u >> v) {
            adj[u].push_back(v);
            adj[v].push_back(u);
        }
    }

    int source = 1;
    vector<int> dist(n + 1, -1);
    queue<int> q;

    dist[source] = 0;
    q.push(source);

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }

    for (int i = 1; i <= n; i++) {
        cout << dist[i] << (i == n ? "" : " ");
    }
    cout << "\\n";

    return 0;
}
"""

    if pattern == "graph_dfs_traversal":
        return """#include <iostream>
#include <vector>

using namespace std;

void dfs(int u, const vector<vector<int>>& adj, vector<bool>& visited, vector<int>& order) {
    visited[u] = true;
    order.push_back(u);
    for (int v : adj[u]) {
        if (!visited[v]) {
            dfs(v, adj, visited, order);
        }
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        if (cin >> u >> v) {
            adj[u].push_back(v);
            adj[v].push_back(u);
        }
    }

    vector<bool> visited(n + 1, false);
    vector<int> order;

    for (int i = 1; i <= n; i++) {
        if (!visited[i]) {
            dfs(i, adj, visited, order);
        }
    }

    for (size_t i = 0; i < order.size(); i++) {
        cout << order[i] << (i + 1 == order.size() ? "" : " ");
    }
    cout << "\\n";

    return 0;
}
"""

    if pattern == "graph_connected_components":
        return """#include <iostream>
#include <vector>

using namespace std;

void dfsComponent(int u, int comp_id, const vector<vector<int>>& adj, vector<int>& comp) {
    comp[u] = comp_id;
    for (int v : adj[u]) {
        if (comp[v] == 0) {
            dfsComponent(v, comp_id, adj, comp);
        }
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        if (cin >> u >> v) {
            adj[u].push_back(v);
            adj[v].push_back(u);
        }
    }

    vector<int> comp(n + 1, 0);
    int num_components = 0;

    for (int i = 1; i <= n; i++) {
        if (comp[i] == 0) {
            num_components++;
            dfsComponent(i, num_components, adj, comp);
        }
    }

    cout << num_components << "\\n";

    return 0;
}
"""

    if pattern == "graph_cycle_detection_undirected":
        return """#include <iostream>
#include <vector>

using namespace std;

bool dfsCycle(int u, int p, const vector<vector<int>>& adj, vector<bool>& visited) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) {
            if (dfsCycle(v, u, adj, visited)) return true;
        } else if (v != p) {
            return true; // Back-edge found
        }
    }
    return false;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        if (cin >> u >> v) {
            adj[u].push_back(v);
            adj[v].push_back(u);
        }
    }

    vector<bool> visited(n + 1, false);
    bool has_cycle = false;

    for (int i = 1; i <= n; i++) {
        if (!visited[i]) {
            if (dfsCycle(i, 0, adj, visited)) {
                has_cycle = true;
                break;
            }
        }
    }

    cout << (has_cycle ? "YES" : "NO") << "\\n";

    return 0;
}
"""

    if pattern == "graph_cycle_detection_directed":
        return """#include <iostream>
#include <vector>

using namespace std;

// 0: UNVISITED, 1: VISITING (in call stack), 2: VISITED (done)
bool dfsDirectedCycle(int u, const vector<vector<int>>& adj, vector<int>& color) {
    color[u] = 1;
    for (int v : adj[u]) {
        if (color[v] == 1) {
            return true; // Back-edge to node currently in recursion stack
        }
        if (color[v] == 0 && dfsDirectedCycle(v, adj, color)) {
            return true;
        }
    }
    color[u] = 2;
    return false;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        if (cin >> u >> v) {
            adj[u].push_back(v);
        }
    }

    vector<int> color(n + 1, 0);
    bool has_cycle = false;

    for (int i = 1; i <= n; i++) {
        if (color[i] == 0) {
            if (dfsDirectedCycle(i, adj, color)) {
                has_cycle = true;
                break;
            }
        }
    }

    cout << (has_cycle ? "YES" : "NO") << "\\n";

    return 0;
}
"""

    if pattern == "graph_bipartite_coloring":
        return """#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        if (cin >> u >> v) {
            adj[u].push_back(v);
            adj[v].push_back(u);
        }
    }

    vector<int> color(n + 1, -1);
    bool is_bipartite = true;

    for (int start = 1; start <= n; start++) {
        if (color[start] != -1) continue;

        color[start] = 0;
        queue<int> q;
        q.push(start);

        while (!q.empty()) {
            int u = q.front();
            q.pop();

            for (int v : adj[u]) {
                if (color[v] == -1) {
                    color[v] = 1 - color[u];
                    q.push(v);
                } else if (color[v] == color[u]) {
                    is_bipartite = false;
                    break;
                }
            }
            if (!is_bipartite) break;
        }
        if (!is_bipartite) break;
    }

    cout << (is_bipartite ? "YES" : "NO") << "\\n";

    return 0;
}
"""

    if pattern == "graph_dijkstra":
        return """#include <iostream>
#include <vector>
#include <queue>

using namespace std;

const long long INF = 1e18;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<vector<pair<int, long long>>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        if (cin >> u >> v >> w) {
            adj[u].push_back({v, w});
        }
    }

    int source = 1;
    vector<long long> dist(n + 1, INF);
    // Min-heap: {distance, vertex}
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;

    dist[source] = 0;
    pq.push({0, source});

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();

        if (d > dist[u]) continue; // Stale entry

        for (auto& edge : adj[u]) {
            int v = edge.first;
            long long w = edge.second;
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }

    for (int i = 1; i <= n; i++) {
        if (dist[i] == INF) cout << -1;
        else cout << dist[i];
        cout << (i == n ? "" : " ");
    }
    cout << "\\n";

    return 0;
}
"""

    if pattern == "graph_bellman_ford":
        return """#include <iostream>
#include <vector>
#include <queue>

using namespace std;

const long long INF = 1e18;

struct Edge {
    int u, v;
    long long w;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<Edge> edges(m);
    for (int i = 0; i < m; i++) {
        cin >> edges[i].u >> edges[i].v >> edges[i].w;
    }

    int source = 1;
    vector<long long> dist(n + 1, INF);
    dist[source] = 0;

    // V - 1 rounds of relaxation
    for (int round = 1; round <= n - 1; round++) {
        bool changed = false;
        for (const auto& e : edges) {
            if (dist[e.u] < INF && dist[e.u] + e.w < dist[e.v]) {
                dist[e.v] = dist[e.u] + e.w;
                changed = true;
            }
        }
        if (!changed) break;
    }

    // Identify vertices directly relaxed by negative cycles reachable from source
    vector<bool> in_neg_cycle(n + 1, false);
    bool has_reachable_neg_cycle = false;
    for (const auto& e : edges) {
        if (dist[e.u] < INF && dist[e.u] + e.w < dist[e.v]) {
            dist[e.v] = -INF;
            in_neg_cycle[e.v] = true;
            has_reachable_neg_cycle = true;
        }
    }

    // Propagate negative-cycle influence forward to all reachable targets
    if (has_reachable_neg_cycle) {
        vector<vector<int>> adj(n + 1);
        for (const auto& e : edges) {
            adj[e.u].push_back(e.v);
        }
        queue<int> q;
        for (int i = 1; i <= n; i++) {
            if (in_neg_cycle[i]) q.push(i);
        }
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (int v : adj[u]) {
                if (!in_neg_cycle[v]) {
                    in_neg_cycle[v] = true;
                    dist[v] = -INF;
                    q.push(v);
                }
            }
        }

        cout << "NEGATIVE_CYCLE\\n";
        return 0;
    }

    for (int i = 1; i <= n; i++) {
        if (in_neg_cycle[i]) cout << "-INF";
        else if (dist[i] == INF) cout << -1;
        else cout << dist[i];
        cout << (i == n ? "" : " ");
    }
    cout << "\\n";

    return 0;
}
"""

    if pattern == "graph_floyd_warshall":
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const long long INF = 1e18;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<vector<long long>> dist(n + 1, vector<long long>(n + 1, INF));
    for (int i = 1; i <= n; i++) {
        dist[i][i] = 0;
    }

    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        if (cin >> u >> v >> w) {
            dist[u][v] = min(dist[u][v], w);
        }
    }

    // Floyd-Warshall intermediate vertex relaxation
    for (int k = 1; k <= n; k++) {
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                if (dist[i][k] < INF && dist[k][j] < INF) {
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
                }
            }
        }
    }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            if (dist[i][j] == INF) cout << -1;
            else cout << dist[i][j];
            cout << (j == n ? "" : " ");
        }
        cout << "\\n";
    }

    return 0;
}
"""

    if pattern == "graph_topological_sort":
        return """#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<vector<int>> adj(n + 1);
    vector<int> in_degree(n + 1, 0);

    for (int i = 0; i < m; i++) {
        int u, v;
        if (cin >> u >> v) {
            adj[u].push_back(v);
            in_degree[v]++;
        }
    }

    queue<int> q;
    for (int i = 1; i <= n; i++) {
        if (in_degree[i] == 0) {
            q.push(i);
        }
    }

    vector<int> topo_order;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        topo_order.push_back(u);

        for (int v : adj[u]) {
            if (--in_degree[v] == 0) {
                q.push(v);
            }
        }
    }

    if ((int)topo_order.size() < n) {
        cout << "CYCLE_DETECTED\\n";
    } else {
        for (size_t i = 0; i < topo_order.size(); i++) {
            cout << topo_order[i] << (i + 1 == topo_order.size() ? "" : " ");
        }
        cout << "\\n";
    }

    return 0;
}
"""

    if pattern == "graph_dag_dp":
        return """#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

const long long INF = 1e18;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<vector<pair<int, long long>>> adj(n + 1);
    vector<int> in_degree(n + 1, 0);

    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        if (cin >> u >> v >> w) {
            adj[u].push_back({v, w});
            in_degree[v]++;
        }
    }

    queue<int> q;
    for (int i = 1; i <= n; i++) {
        if (in_degree[i] == 0) {
            q.push(i);
        }
    }

    vector<int> topo;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        topo.push_back(u);
        for (auto& edge : adj[u]) {
            if (--in_degree[edge.first] == 0) {
                q.push(edge.first);
            }
        }
    }

    // Longest path in DAG (or shortest path)
    int source = 1;
    vector<long long> dp(n + 1, -INF);
    dp[source] = 0;

    for (int u : topo) {
        if (dp[u] == -INF) continue;
        for (auto& edge : adj[u]) {
            int v = edge.first;
            long long w = edge.second;
            dp[v] = max(dp[v], dp[u] + w);
        }
    }

    long long max_path = 0;
    for (int i = 1; i <= n; i++) {
        max_path = max(max_path, dp[i]);
    }
    cout << max_path << "\\n";

    return 0;
}
"""

    if pattern == "graph_dsu":
        return """#include <iostream>
#include <vector>
#include <numeric>

using namespace std;

struct DSU {
    vector<int> parent, rank;
    int components;

    DSU(int n) : parent(n + 1), rank(n + 1, 0), components(n) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]); // Path compression
        }
        return parent[x];
    }

    bool unite(int x, int y) {
        int rx = find(x);
        int ry = find(y);
        if (rx == ry) return false;

        // Union by rank
        if (rank[rx] < rank[ry]) swap(rx, ry);
        parent[ry] = rx;
        if (rank[rx] == rank[ry]) rank[rx]++;
        components--;
        return true;
    }

    bool connected(int x, int y) {
        return find(x) == find(y);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    DSU dsu(n);
    while (q--) {
        int type, u, v;
        cin >> type >> u >> v;
        if (type == 1) {
            dsu.unite(u, v);
        } else {
            cout << (dsu.connected(u, v) ? "YES" : "NO") << "\\n";
        }
    }

    return 0;
}
"""

    if pattern == "graph_mst_kruskal":
        return """#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>

using namespace std;

struct Edge {
    int u, v;
    long long w;
    bool operator<(const Edge& other) const {
        return w < other.w;
    }
};

struct DSU {
    vector<int> parent, rank;
    int components;

    DSU(int n) : parent(n + 1), rank(n + 1, 0), components(n) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }

    bool unite(int x, int y) {
        int rx = find(x), ry = find(y);
        if (rx == ry) return false;
        if (rank[rx] < rank[ry]) swap(rx, ry);
        parent[ry] = rx;
        if (rank[rx] == rank[ry]) rank[rx]++;
        components--;
        return true;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<Edge> edges(m);
    for (int i = 0; i < m; i++) {
        cin >> edges[i].u >> edges[i].v >> edges[i].w;
    }

    sort(edges.begin(), edges.end());

    DSU dsu(n);
    long long total_weight = 0;
    int edges_used = 0;

    for (const auto& e : edges) {
        if (dsu.unite(e.u, e.v)) {
            total_weight += e.w;
            edges_used++;
            if (edges_used == n - 1) break;
        }
    }

    if (edges_used == n - 1 || n == 1) {
        cout << total_weight << "\\n";
    } else {
        cout << -1 << "\\n"; // Disconnected graph, no MST exists
    }

    return 0;
}
"""

    if pattern == "graph_mst_prim":
        return """#include <iostream>
#include <vector>
#include <queue>

using namespace std;

const long long INF = 1e18;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<vector<pair<int, long long>>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        if (cin >> u >> v >> w) {
            adj[u].push_back({v, w});
            adj[v].push_back({u, w});
        }
    }

    vector<bool> in_mst(n + 1, false);
    vector<long long> key(n + 1, INF);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;

    int start = 1;
    key[start] = 0;
    pq.push({0, start});

    long long total_weight = 0;
    int nodes_in_mst = 0;

    while (!pq.empty()) {
        auto [w, u] = pq.top();
        pq.pop();

        if (in_mst[u]) continue;
        in_mst[u] = true;
        total_weight += w;
        nodes_in_mst++;

        for (auto& edge : adj[u]) {
            int v = edge.first;
            long long weight = edge.second;
            if (!in_mst[v] && weight < key[v]) {
                key[v] = weight;
                pq.push({key[v], v});
            }
        }
    }

    if (nodes_in_mst == n) {
        cout << total_weight << "\\n";
    } else {
        cout << -1 << "\\n"; // Disconnected
    }

    return 0;
}
"""

    if pattern == "graph_scc_tarjan":
        return """#include <iostream>
#include <vector>
#include <stack>
#include <algorithm>

using namespace std;

int timer_idx = 0;
int scc_count = 0;

void tarjanDFS(int u, const vector<vector<int>>& adj, vector<int>& tin, vector<int>& low,
               stack<int>& st, vector<bool>& on_stack, vector<int>& scc_id) {
    tin[u] = low[u] = ++timer_idx;
    st.push(u);
    on_stack[u] = true;

    for (int v : adj[u]) {
        if (tin[v] == 0) {
            tarjanDFS(v, adj, tin, low, st, on_stack, scc_id);
            low[u] = min(low[u], low[v]);
        } else if (on_stack[v]) {
            low[u] = min(low[u], tin[v]);
        }
    }

    // Root of SCC found
    if (low[u] == tin[u]) {
        scc_count++;
        while (true) {
            int v = st.top();
            st.pop();
            on_stack[v] = false;
            scc_id[v] = scc_count;
            if (u == v) break;
        }
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        if (cin >> u >> v) {
            adj[u].push_back(v);
        }
    }

    vector<int> tin(n + 1, 0), low(n + 1, 0), scc_id(n + 1, 0);
    vector<bool> on_stack(n + 1, false);
    stack<int> st;

    for (int i = 1; i <= n; i++) {
        if (tin[i] == 0) {
            tarjanDFS(i, adj, tin, low, st, on_stack, scc_id);
        }
    }

    cout << scc_count << "\\n";

    return 0;
}
"""

    if pattern == "graph_bridges_articulation":
        return """#include <iostream>
#include <vector>
#include <algorithm>
#include <set>

using namespace std;

int timer_idx = 0;

void dfsBridgeAP(int u, int p, const vector<vector<int>>& adj,
                 vector<int>& tin, vector<int>& low,
                 vector<pair<int, int>>& bridges, set<int>& articulation_points) {
    tin[u] = low[u] = ++timer_idx;
    int children = 0;

    for (int v : adj[u]) {
        if (v == p) continue;
        if (tin[v] != 0) {
            low[u] = min(low[u], tin[v]); // Back-edge
        } else {
            children++;
            dfsBridgeAP(v, u, adj, tin, low, bridges, articulation_points);
            low[u] = min(low[u], low[v]);

            // Bridge condition: low[v] > tin[u]
            if (low[v] > tin[u]) {
                bridges.push_back({min(u, v), max(u, v)});
            }

            // Articulation point condition (non-root): low[v] >= tin[u]
            if (p != 0 && low[v] >= tin[u]) {
                articulation_points.insert(u);
            }
        }
    }

    // Root articulation point condition: >= 2 children in DFS tree
    if (p == 0 && children >= 2) {
        articulation_points.insert(u);
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        if (cin >> u >> v) {
            adj[u].push_back(v);
            adj[v].push_back(u);
        }
    }

    vector<int> tin(n + 1, 0), low(n + 1, 0);
    vector<pair<int, int>> bridges;
    set<int> articulation_points;

    for (int i = 1; i <= n; i++) {
        if (tin[i] == 0) {
            dfsBridgeAP(i, 0, adj, tin, low, bridges, articulation_points);
        }
    }

    cout << "Bridges: " << bridges.size() << "\\n";
    cout << "Articulation Points: " << articulation_points.size() << "\\n";

    return 0;
}
"""

    return f"""#include <iostream>
using namespace std;
int main() {{ return 0; }}
"""
