"""
C++17 Code Generator for Disjoint Set Union (DSU) Domain (Phase 3H).

Generates production-grade C++17 implementations for:
1. dsu_basic
2. dsu_component_metadata
3. dsu_dynamic_connectivity
4. dsu_weighted
5. dsu_potential_difference
6. dsu_parity
7. dsu_rollback
8. dsu_offline_dynamic_connectivity
9. dsu_kruskal_support
10. dsu_constraint_consistency
"""

from typing import Dict, Any


def generate_dsu_cpp(pattern: str, params: Dict[str, Any]) -> str:
    if pattern == "dsu_basic":
        return """#include <iostream>
#include <vector>
#include <numeric>

using namespace std;

struct BasicDSU {
    vector<int> parent;
    vector<int> sz;
    int num_components;

    BasicDSU(int n) : parent(n + 1), sz(n + 1, 1), num_components(n) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]); // Two-pass path compression
        }
        return parent[x];
    }

    bool unite(int x, int y) {
        int rx = find(x);
        int ry = find(y);
        if (rx == ry) return false;
        // Union by size
        if (sz[rx] < sz[ry]) swap(rx, ry);
        parent[ry] = rx;
        sz[rx] += sz[ry];
        num_components--;
        return true;
    }

    bool connected(int x, int y) {
        return find(x) == find(y);
    }

    int component_size(int x) {
        return sz[find(x)];
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    BasicDSU dsu(n);
    while (q--) {
        int type, u, v;
        cin >> type >> u >> v;
        if (type == 1) {
            dsu.unite(u, v);
        } else if (type == 2) {
            cout << (dsu.connected(u, v) ? "YES" : "NO") << "\\n";
        } else if (type == 3) {
            cout << dsu.component_size(u) << "\\n";
        }
    }
    return 0;
}
"""

    if pattern == "dsu_component_metadata":
        return """#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>

using namespace std;

struct MetadataDSU {
    vector<int> parent;
    vector<int> sz;
    vector<long long> sum;
    vector<long long> mn;
    vector<long long> mx;
    int num_components;

    MetadataDSU(int n, const vector<long long>& val) 
        : parent(n + 1), sz(n + 1, 1), sum(n + 1), mn(n + 1), mx(n + 1), num_components(n) {
        iota(parent.begin(), parent.end(), 0);
        for (int i = 1; i <= n; i++) {
            sum[i] = val[i];
            mn[i] = val[i];
            mx[i] = val[i];
        }
    }

    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    bool unite(int x, int y) {
        int rx = find(x);
        int ry = find(y);
        if (rx == ry) return false;
        if (sz[rx] < sz[ry]) swap(rx, ry);
        parent[ry] = rx;
        sz[rx] += sz[ry];
        sum[rx] += sum[ry];
        mn[rx] = min(mn[rx], mn[ry]);
        mx[rx] = max(mx[rx], mx[ry]);
        num_components--;
        return true;
    }

    long long get_sum(int x) { return sum[find(x)]; }
    long long get_min(int x) { return mn[find(x)]; }
    long long get_max(int x) { return mx[find(x)]; }
    int get_size(int x) { return sz[find(x)]; }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    vector<long long> val(n + 1);
    for (int i = 1; i <= n; i++) cin >> val[i];

    MetadataDSU dsu(n, val);
    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int u, v;
            cin >> u >> v;
            dsu.unite(u, v);
        } else if (type == 2) {
            int u;
            cin >> u;
            cout << dsu.get_size(u) << " " << dsu.get_sum(u) << " " << dsu.get_min(u) << " " << dsu.get_max(u) << "\\n";
        }
    }
    return 0;
}
"""

    if pattern == "dsu_dynamic_connectivity":
        return """#include <iostream>
#include <vector>
#include <numeric>

using namespace std;

struct DynamicConnectivityDSU {
    vector<int> parent;
    vector<int> sz;
    int components;

    DynamicConnectivityDSU(int n) : parent(n + 1), sz(n + 1, 1), components(n) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    bool unite(int x, int y) {
        int rx = find(x), ry = find(y);
        if (rx == ry) return false;
        if (sz[rx] < sz[ry]) swap(rx, ry);
        parent[ry] = rx;
        sz[rx] += sz[ry];
        components--;
        return true;
    }

    bool connected(int x, int y) {
        return find(x) == find(y);
    }

    int component_size(int x) {
        return sz[find(x)];
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    DynamicConnectivityDSU dsu(n);
    while (q--) {
        int type, u, v;
        cin >> type >> u >> v;
        if (type == 1) {
            dsu.unite(u, v);
        } else if (type == 2) {
            cout << (dsu.connected(u, v) ? "YES" : "NO") << "\\n";
        } else if (type == 3) {
            cout << dsu.component_size(u) << "\\n";
        }
    }
    return 0;
}
"""

    if pattern == "dsu_weighted":
        return """#include <iostream>
#include <vector>
#include <numeric>

using namespace std;

// Weighted / Potential DSU: maintains value[x] - value[parent[x]] = potential[x]
struct PotentialDSU {
    vector<int> parent;
    vector<long long> potential;
    int components;

    PotentialDSU(int n) : parent(n + 1), potential(n + 1, 0), components(n) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        if (parent[x] != x) {
            int p = parent[x];
            parent[x] = find(p);
            potential[x] += potential[p];
        }
        return parent[x];
    }

    // Constraint: value[x] - value[y] = w
    bool unite(int x, int y, long long w) {
        int rx = find(x);
        int ry = find(y);
        if (rx == ry) {
            return (potential[x] - potential[y]) == w;
        }
        parent[rx] = ry;
        potential[rx] = w - potential[x] + potential[y];
        components--;
        return true;
    }

    bool same_component(int x, int y) {
        return find(x) == find(y);
    }

    long long diff(int x, int y) {
        find(x);
        find(y);
        return potential[x] - potential[y];
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    PotentialDSU dsu(n);
    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int u, v;
            long long w;
            cin >> u >> v >> w;
            bool ok = dsu.unite(u, v, w);
            if (!ok) {
                cout << "CONTRADICTION\\n";
            }
        } else if (type == 2) {
            int u, v;
            cin >> u >> v;
            if (dsu.same_component(u, v)) {
                cout << dsu.diff(u, v) << "\\n";
            } else {
                cout << "UNKNOWN\\n";
            }
        }
    }
    return 0;
}
"""

    if pattern == "dsu_potential_difference":
        return """#include <iostream>
#include <vector>
#include <numeric>

using namespace std;

// Relative Potential Difference Queries
struct PotentialDifferenceDSU {
    vector<int> parent;
    vector<long long> potential;

    PotentialDifferenceDSU(int n) : parent(n + 1), potential(n + 1, 0) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        if (parent[x] != x) {
            int p = parent[x];
            parent[x] = find(p);
            potential[x] += potential[p];
        }
        return parent[x];
    }

    bool unite(int x, int y, long long diff_xy) {
        int rx = find(x);
        int ry = find(y);
        if (rx == ry) {
            return (potential[x] - potential[y]) == diff_xy;
        }
        parent[rx] = ry;
        potential[rx] = diff_xy - potential[x] + potential[y];
        return true;
    }

    bool query_diff(int x, int y, long long& result) {
        if (find(x) != find(y)) return false;
        result = potential[x] - potential[y];
        return true;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    PotentialDifferenceDSU dsu(n);
    while (q--) {
        int type, u, v;
        cin >> type >> u >> v;
        if (type == 1) {
            long long w;
            cin >> w;
            dsu.unite(u, v, w);
        } else {
            long long res;
            if (dsu.query_diff(u, v, res)) {
                cout << res << "\\n";
            } else {
                cout << "UNKNOWN\\n";
            }
        }
    }
    return 0;
}
"""

    if pattern == "dsu_parity":
        return """#include <iostream>
#include <vector>
#include <numeric>

using namespace std;

// Dynamic Parity / 2-Coloring DSU: color[x] ^ color[parent[x]] = parity[x]
struct ParityDSU {
    vector<int> parent;
    vector<int> parity;
    bool has_odd_cycle;

    ParityDSU(int n) : parent(n + 1), parity(n + 1, 0), has_odd_cycle(false) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        if (parent[x] != x) {
            int p = parent[x];
            parent[x] = find(p);
            parity[x] ^= parity[p];
        }
        return parent[x];
    }

    // Constraint: color[x] ^ color[y] = p (0 for same color, 1 for opposite color)
    bool unite(int x, int y, int p) {
        int rx = find(x);
        int ry = find(y);
        if (rx == ry) {
            if ((parity[x] ^ parity[y]) != p) {
                has_odd_cycle = true;
                return false;
            }
            return true;
        }
        parent[rx] = ry;
        parity[rx] = p ^ parity[x] ^ parity[y];
        return true;
    }

    bool is_same_color(int x, int y) {
        return (find(x) == find(y)) && (parity[x] == parity[y]);
    }

    bool is_opposite_color(int x, int y) {
        return (find(x) == find(y)) && (parity[x] != parity[y]);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    ParityDSU dsu(n);
    while (q--) {
        int type, u, v, p;
        cin >> type >> u >> v;
        if (type == 1) {
            cin >> p;
            bool ok = dsu.unite(u, v, p);
            if (!ok) cout << "CONTRADICTION\\n";
        } else {
            if (dsu.find(u) != dsu.find(v)) {
                cout << "UNKNOWN\\n";
            } else if (dsu.parity[u] == dsu.parity[v]) {
                cout << "SAME\\n";
            } else {
                cout << "DIFFERENT\\n";
            }
        }
    }
    return 0;
}
"""

    if pattern == "dsu_rollback":
        return """#include <iostream>
#include <vector>
#include <numeric>

using namespace std;

// Rollback DSU: supports union-by-size and exact snapshot restoration
struct RollbackDSU {
    vector<int> parent;
    vector<int> sz;
    int components;

    struct Change {
        int u;       // root attached
        int prev_p;  // previous parent of u
        int v;       // root whose size was incremented
        int prev_sz; // previous size of v
        bool merged;
    };
    vector<Change> history;

    RollbackDSU(int n) : parent(n + 1), sz(n + 1, 1), components(n) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) const {
        while (x != parent[x]) {
            x = parent[x]; // NO path compression
        }
        return x;
    }

    bool unite(int x, int y) {
        int rx = find(x);
        int ry = find(y);
        if (rx == ry) {
            history.push_back({-1, -1, -1, -1, false});
            return false;
        }
        if (sz[rx] < sz[ry]) swap(rx, ry);
        history.push_back({ry, parent[ry], rx, sz[rx], true});
        parent[ry] = rx;
        sz[rx] += sz[ry];
        components--;
        return true;
    }

    int checkpoint() const {
        return history.size();
    }

    void rollback(int snapshot) {
        while ((int)history.size() > snapshot) {
            Change c = history.back();
            history.pop_back();
            if (c.merged) {
                parent[c.u] = c.prev_p;
                sz[c.v] = c.prev_sz;
                components++;
            }
        }
    }

    bool connected(int x, int y) const {
        return find(x) == find(y);
    }

    int component_size(int x) const {
        return sz[find(x)];
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    RollbackDSU dsu(n);
    vector<int> checkpoints;

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) { // unite
            int u, v;
            cin >> u >> v;
            dsu.unite(u, v);
        } else if (type == 2) { // connected
            int u, v;
            cin >> u >> v;
            cout << (dsu.connected(u, v) ? "YES" : "NO") << "\\n";
        } else if (type == 3) { // snapshot
            checkpoints.push_back(dsu.checkpoint());
        } else if (type == 4) { // rollback to last snapshot
            if (!checkpoints.empty()) {
                dsu.rollback(checkpoints.back());
                checkpoints.pop_back();
            }
        }
    }
    return 0;
}
"""

    if pattern == "dsu_offline_dynamic_connectivity":
        return """#include <iostream>
#include <vector>
#include <numeric>
#include <map>
#include <algorithm>

using namespace std;

struct RollbackDSU {
    vector<int> parent;
    vector<int> sz;
    int components;

    struct Change {
        int u, prev_p, v, prev_sz;
        bool merged;
    };
    vector<Change> history;

    RollbackDSU(int n) : parent(n + 1), sz(n + 1, 1), components(n) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) const {
        while (x != parent[x]) x = parent[x];
        return x;
    }

    bool unite(int x, int y) {
        int rx = find(x), ry = find(y);
        if (rx == ry) {
            history.push_back({-1, -1, -1, -1, false});
            return false;
        }
        if (sz[rx] < sz[ry]) swap(rx, ry);
        history.push_back({ry, parent[ry], rx, sz[rx], true});
        parent[ry] = rx;
        sz[rx] += sz[ry];
        components--;
        return true;
    }

    int checkpoint() const { return history.size(); }

    void rollback(int snapshot) {
        while ((int)history.size() > snapshot) {
            Change c = history.back();
            history.pop_back();
            if (c.merged) {
                parent[c.u] = c.prev_p;
                sz[c.v] = c.prev_sz;
                components++;
            }
        }
    }

    bool connected(int x, int y) const {
        return find(x) == find(y);
    }
};

struct Edge {
    int u, v;
};

struct Query {
    int type; // 1: add, 2: delete, 3: query connected
    int u, v;
};

// Segment tree over time [0..Q-1]
struct SegTreeOffline {
    int q_count;
    vector<vector<Edge>> tree;

    SegTreeOffline(int q) : q_count(q), tree(4 * max(1, q) + 1) {}

    void add_edge(int node, int l, int r, int ql, int qr, const Edge& e) {
        if (ql > r || qr < l) return;
        if (ql <= l && r <= qr) {
            tree[node].push_back(e);
            return;
        }
        int mid = l + (r - l) / 2;
        add_edge(2 * node, l, mid, ql, qr, e);
        add_edge(2 * node + 1, mid + 1, r, ql, qr, e);
    }

    void dfs(int node, int l, int r, RollbackDSU& dsu, const vector<Query>& queries, vector<string>& answers) {
        int snap = dsu.checkpoint();
        for (const auto& e : tree[node]) {
            dsu.unite(e.u, e.v);
        }

        if (l == r) {
            if (l < (int)queries.size() && queries[l].type == 3) {
                answers[l] = dsu.connected(queries[l].u, queries[l].v) ? "YES" : "NO";
            }
        } else {
            int mid = l + (r - l) / 2;
            dfs(2 * node, l, mid, dsu, queries, answers);
            dfs(2 * node + 1, mid + 1, r, dsu, queries, answers);
        }

        dsu.rollback(snap);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    vector<Query> queries(q);
    map<pair<int, int>, int> active_edges;
    vector<pair<Edge, pair<int, int>>> edge_lifetimes;

    for (int t = 0; t < q; t++) {
        cin >> queries[t].type >> queries[t].u >> queries[t].v;
        int u = queries[t].u;
        int v = queries[t].v;
        if (u > v) swap(u, v);

        if (queries[t].type == 1) { // add edge
            active_edges[{u, v}] = t;
        } else if (queries[t].type == 2) { // remove edge
            auto it = active_edges.find({u, v});
            if (it != active_edges.end()) {
                edge_lifetimes.push_back({{u, v}, {it->second, t - 1}});
                active_edges.erase(it);
            }
        }
    }

    // Remaining active edges live until end of query timeline (q - 1)
    for (const auto& pair : active_edges) {
        edge_lifetimes.push_back({{pair.first.first, pair.first.second}, {pair.second, q - 1}});
    }

    SegTreeOffline seg(q);
    for (const auto& el : edge_lifetimes) {
        if (el.second.first <= el.second.second) {
            seg.add_edge(1, 0, q - 1, el.second.first, el.second.second, el.first);
        }
    }

    RollbackDSU dsu(n);
    vector<string> answers(q, "");
    seg.dfs(1, 0, q - 1, dsu, queries, answers);

    for (int t = 0; t < q; t++) {
        if (queries[t].type == 3) {
            cout << answers[t] << "\\n";
        }
    }

    return 0;
}
"""

    if pattern == "dsu_kruskal_support":
        return """#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>

using namespace std;

struct Edge {
    int u, v;
    long long weight;
    bool operator<(const Edge& other) const {
        return weight < other.weight;
    }
};

struct KruskalDSU {
    vector<int> parent, sz;
    int components;

    KruskalDSU(int n) : parent(n + 1), sz(n + 1, 1), components(n) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }

    bool unite(int x, int y) {
        int rx = find(x), ry = find(y);
        if (rx == ry) return false;
        if (sz[rx] < sz[ry]) swap(rx, ry);
        parent[ry] = rx;
        sz[rx] += sz[ry];
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
        cin >> edges[i].u >> edges[i].v >> edges[i].weight;
    }

    sort(edges.begin(), edges.end());

    KruskalDSU dsu(n);
    long long total_weight = 0;
    int edges_used = 0;

    for (const auto& e : edges) {
        if (dsu.unite(e.u, e.v)) {
            total_weight += e.weight;
            edges_used++;
            if (edges_used == n - 1) break;
        }
    }

    cout << total_weight << "\\n";
    return 0;
}
"""

    if pattern == "dsu_constraint_consistency":
        return """#include <iostream>
#include <vector>
#include <numeric>

using namespace std;

// Constraint Consistency Solver using Potential DSU
struct ConstraintConsistencyDSU {
    vector<int> parent;
    vector<long long> potential;
    bool consistent;

    ConstraintConsistencyDSU(int n) : parent(n + 1), potential(n + 1, 0), consistent(true) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        if (parent[x] != x) {
            int p = parent[x];
            parent[x] = find(p);
            potential[x] += potential[p];
        }
        return parent[x];
    }

    // Adds constraint: value[x] - value[y] = diff
    bool add_constraint(int x, int y, long long diff) {
        int rx = find(x);
        int ry = find(y);
        if (rx == ry) {
            if ((potential[x] - potential[y]) != diff) {
                consistent = false;
                return false;
            }
            return true;
        }
        parent[rx] = ry;
        potential[rx] = diff - potential[x] + potential[y];
        return true;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    ConstraintConsistencyDSU dsu(n);
    for (int i = 0; i < m; i++) {
        int u, v;
        long long diff;
        cin >> u >> v >> diff;
        dsu.add_constraint(u, v, diff);
    }

    if (dsu.consistent) {
        cout << "CONSISTENT\\n";
    } else {
        cout << "INCONSISTENT\\n";
    }

    return 0;
}
"""

    return """#include <iostream>
using namespace std;
int main() { return 0; }
"""
