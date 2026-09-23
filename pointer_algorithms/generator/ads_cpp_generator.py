"""
CHUP Phase 3S — Standalone C++17 Code Generator for Advanced Data Structures.

Generates production-grade, highly optimized, standalone C++17 code for all 10 canonical patterns:
1. ads_sparse_table (Static RMQ with O(1) overlapping query)
2. ads_lca_binary_lifting (Binary Lifting jump table)
3. ads_heavy_light_decomposition (Heavy-Light chain decomposition)
4. ads_centroid_decomposition (Balanced centroid tree decomposition)
5. ads_persistent_segment_tree (Path-copying persistent segment tree)
6. ads_dynamic_segment_tree (Pointer-index lazy node allocation over large domains)
7. ads_merge_sort_tree (Sorted vector segment tree for range rank)
8. ads_sqrt_decomposition (Block partitioning with lazy tags)
9. ads_mos_algorithm (Offline query scheduler with snake block ordering)
10. ads_segment_tree_beats (Range chmin + current max hierarchy)
"""

from typing import Dict, Any, Optional


def generate_ads_cpp(pattern: str, params: Optional[Dict[str, Any]] = None) -> str:
    p = params or {}

    if pattern == "ads_sparse_table":
        return generate_sparse_table_cpp(p)
    elif pattern == "ads_lca_binary_lifting":
        return generate_lca_binary_lifting_cpp(p)
    elif pattern == "ads_heavy_light_decomposition":
        return generate_heavy_light_decomposition_cpp(p)
    elif pattern == "ads_centroid_decomposition":
        return generate_centroid_decomposition_cpp(p)
    elif pattern == "ads_persistent_segment_tree":
        return generate_persistent_segment_tree_cpp(p)
    elif pattern == "ads_dynamic_segment_tree":
        return generate_dynamic_segment_tree_cpp(p)
    elif pattern == "ads_merge_sort_tree":
        return generate_merge_sort_tree_cpp(p)
    elif pattern == "ads_sqrt_decomposition":
        return generate_sqrt_decomposition_cpp(p)
    elif pattern == "ads_mos_algorithm":
        return generate_mos_algorithm_cpp(p)
    elif pattern == "ads_segment_tree_beats":
        return generate_segment_tree_beats_cpp(p)
    else:
        return f"// Unsupported advanced data structure pattern: {pattern}\n"


def generate_sparse_table_cpp(p: Dict[str, Any]) -> str:
    return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

template <typename T>
class SparseTable {
private:
    int n;
    int k_max;
    vector<int> log_table;
    vector<vector<T>> st;

public:
    SparseTable(const vector<T>& arr) {
        n = arr.size();
        log_table.assign(n + 1, 0);
        for (int i = 2; i <= n; ++i) {
            log_table[i] = log_table[i / 2] + 1;
        }
        k_max = log_table[n] + 1;
        st.assign(k_max, vector<T>(n));

        for (int i = 0; i < n; ++i) {
            st[0][i] = arr[i];
        }

        for (int k = 1; k < k_max; ++k) {
            int half = 1 << (k - 1);
            for (int i = 0; i + (1 << k) <= n; ++i) {
                st[k][i] = min(st[k - 1][i], st[k - 1][i + half]);
            }
        }
    }

    T query(int l, int r) const {
        int length = r - l + 1;
        int k = log_table[length];
        return min(st[k][l], st[k][r - (1 << k) + 1]);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q)) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    SparseTable<long long> st(a);
    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << st.query(l, r) << "\\n";
    }
    return 0;
}
"""


def generate_lca_binary_lifting_cpp(p: Dict[str, Any]) -> str:
    return """#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

class BinaryLiftingLCA {
private:
    int n;
    int max_log;
    vector<vector<int>> adj;
    vector<int> depth;
    vector<vector<int>> up;

    void dfs(int u, int p, int d) {
        up[0][u] = p;
        depth[u] = d;
        for (int v : adj[u]) {
            if (v != p) {
                dfs(v, u, d + 1);
            }
        }
    }

public:
    BinaryLiftingLCA(int n_nodes, int root = 0) : n(n_nodes) {
        max_log = max(1, (int)ceil(log2(n + 1)) + 1);
        adj.assign(n, vector<int>());
        depth.assign(n, 0);
        up.assign(max_log, vector<int>(n, root));
    }

    void add_edge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    void build(int root = 0) {
        dfs(root, root, 0);
        for (int k = 1; k < max_log; ++k) {
            for (int u = 0; u < n; ++u) {
                up[k][u] = up[k - 1][up[k - 1][u]];
            }
        }
    }

    int get_lca(int u, int v) const {
        if (depth[u] < depth[v]) swap(u, v);
        int diff = depth[u] - depth[v];
        for (int k = 0; k < max_log; ++k) {
            if ((diff >> k) & 1) {
                u = up[k][u];
            }
        }
        if (u == v) return u;

        for (int k = max_log - 1; k >= 0; --k) {
            if (up[k][u] != up[k][v]) {
                u = up[k][u];
                v = up[k][v];
            }
        }
        return up[0][u];
    }

    int get_distance(int u, int v) const {
        int l = get_lca(u, v);
        return depth[u] + depth[v] - 2 * depth[l];
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q)) return 0;
    BinaryLiftingLCA lca(n);
    for (int i = 0; i < n - 1; ++i) {
        int u, v;
        cin >> u >> v;
        lca.add_edge(u, v);
    }
    lca.build(0);

    while (q--) {
        int u, v;
        cin >> u >> v;
        cout << lca.get_lca(u, v) << "\\n";
    }
    return 0;
}
"""


def generate_heavy_light_decomposition_cpp(p: Dict[str, Any]) -> str:
    is_edge = p.get("is_edge_values", False)
    edge_flag = "true" if is_edge else "false"

    return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

class HeavyLightDecomposition {{
private:
    int n;
    bool is_edge_values;
    vector<vector<int>> adj;
    vector<int> parent, depth, heavy, head, pos;
    vector<long long> tree;
    int cur_pos;

    void dfs_sz(int u, int p, int d) {{
        parent[u] = p;
        depth[u] = d;
        int sz = 1;
        int max_c_sz = 0;
        heavy[u] = -1;
        for (int v : adj[u]) {{
            if (v != p) {{
                dfs_sz(v, u, d + 1);
                sz += 1;
                if (sz > max_c_sz) {{
                    max_c_sz = sz;
                    heavy[u] = v;
                }}
            }}
        }}
    }}

    void dfs_hld(int u, int h) {{
        head[u] = h;
        pos[u] = cur_pos++;
        if (heavy[u] != -1) {{
            dfs_hld(heavy[u], h);
        }}
        for (int v : adj[u]) {{
            if (v != parent[u] && v != heavy[u]) {{
                dfs_hld(v, v);
            }}
        }}
    }}

    void update_st(int node, int l, int r, int idx, long long val) {{
        if (l == r) {{
            tree[node] = val;
            return;
        }}
        int mid = l + (r - l) / 2;
        if (idx <= mid) update_st(2 * node, l, mid, idx, val);
        else update_st(2 * node + 1, mid + 1, r, idx, val);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }}

    long long query_st(int node, int l, int r, int ql, int qr) {{
        if (ql > r || qr < l || ql > qr) return 0;
        if (ql <= l && r <= qr) return tree[node];
        int mid = l + (r - l) / 2;
        return query_st(2 * node, l, mid, ql, qr) + query_st(2 * node + 1, mid + 1, r, ql, qr);
    }}

public:
    HeavyLightDecomposition(int n_nodes, bool edge_mode = {edge_flag}) : n(n_nodes), is_edge_values(edge_mode) {{
        adj.assign(n, vector<int>());
        parent.assign(n, 0);
        depth.assign(n, 0);
        heavy.assign(n, -1);
        head.assign(n, 0);
        pos.assign(n, 0);
        tree.assign(4 * n + 1, 0);
        cur_pos = 0;
    }}

    void add_edge(int u, int v) {{
        adj[u].push_back(v);
        adj[v].push_back(u);
    }}

    void build(int root = 0) {{
        cur_pos = 0;
        dfs_sz(root, root, 0);
        dfs_hld(root, root);
    }}

    void set_node_value(int u, long long val) {{
        update_st(1, 0, n - 1, pos[u], val);
    }}

    long long query_path(int u, int v) {{
        long long res = 0;
        while (head[u] != head[v]) {{
            if (depth[head[u]] > depth[head[v]]) swap(u, v);
            res += query_st(1, 0, n - 1, pos[head[v]], pos[v]);
            v = parent[head[v]];
        }}
        if (depth[u] > depth[v]) swap(u, v);
        if (is_edge_values) {{
            if (depth[u] < depth[v]) {{
                res += query_st(1, 0, n - 1, pos[u] + 1, pos[v]);
            }}
        }} else {{
            res += query_st(1, 0, n - 1, pos[u], pos[v]);
        }}
        return res;
    }}
}};

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q)) return 0;
    HeavyLightDecomposition hld(n);
    for (int i = 0; i < n - 1; ++i) {{
        int u, v;
        cin >> u >> v;
        hld.add_edge(u, v);
    }}
    hld.build(0);

    for (int i = 0; i < n; ++i) {{
        long long val;
        cin >> val;
        hld.set_node_value(i, val);
    }}

    while (q--) {{
        int type, u, v;
        cin >> type >> u >> v;
        if (type == 1) {{
            hld.set_node_value(u, v);
        }} else {{
            cout << hld.query_path(u, v) << "\\n";
        }}
    }}
    return 0;
}}
"""


def generate_centroid_decomposition_cpp(p: Dict[str, Any]) -> str:
    return """#include <iostream>
#include <vector>
#include <map>

using namespace std;

class CentroidDecomposition {
private:
    int n;
    vector<vector<int>> adj;
    vector<bool> removed;
    vector<int> sz;
    vector<int> c_parent;
    vector<int> c_depth;
    vector<map<int, int>> dist_to_centroid;

    int get_sizes(int u, int p) {
        sz[u] = 1;
        for (int v : adj[u]) {
            if (v != p && !removed[v]) {
                sz[u] += get_sizes(v, u);
            }
        }
        return sz[u];
    }

    int get_centroid(int u, int p, int total) {
        for (int v : adj[u]) {
            if (v != p && !removed[v] && sz[v] > total / 2) {
                return get_centroid(v, u, total);
            }
        }
        return u;
    }

    void record_distances(int u, int p, int d, int centroid) {
        dist_to_centroid[u][centroid] = d;
        for (int v : adj[u]) {
            if (v != p && !removed[v]) {
                record_distances(v, u, d + 1, centroid);
            }
        }
    }

    int decompose(int u, int p, int depth) {
        int total = get_sizes(u, -1);
        int c = get_centroid(u, -1, total);
        removed[c] = true;
        c_parent[c] = p;
        c_depth[c] = depth;

        record_distances(c, -1, 0, c);

        for (int v : adj[c]) {
            if (!removed[v]) {
                decompose(v, c, depth + 1);
            }
        }
        return c;
    }

public:
    CentroidDecomposition(int n_nodes) : n(n_nodes) {
        adj.assign(n, vector<int>());
        removed.assign(n, false);
        sz.assign(n, 0);
        c_parent.assign(n, -1);
        c_depth.assign(n, 0);
        dist_to_centroid.assign(n, map<int, int>());
    }

    void add_edge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    int build() {
        return decompose(0, -1, 0);
    }

    int get_distance_to_ancestor(int u, int c) const {
        auto it = dist_to_centroid[u].find(c);
        if (it != dist_to_centroid[u].end()) return it->second;
        return -1;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n)) return 0;
    CentroidDecomposition cd(n);
    for (int i = 0; i < n - 1; ++i) {
        int u, v;
        cin >> u >> v;
        cd.add_edge(u, v);
    }
    cd.build();
    cout << "Centroid tree built successfully.\\n";
    return 0;
}
"""


def generate_persistent_segment_tree_cpp(p: Dict[str, Any]) -> str:
    return """#include <iostream>
#include <vector>

using namespace std;

class PersistentSegmentTree {
public:
    struct Node {
        long long sum;
        int left, right;
        Node(long long s = 0, int l = 0, int r = 0) : sum(s), left(l), right(r) {}
    };

private:
    int n;
    vector<Node> tree;
    vector<int> roots;

    int build(int l, int r, const vector<long long>& a) {
        int node = tree.size();
        tree.emplace_back();
        if (l == r) {
            tree[node].sum = a[l];
            return node;
        }
        int mid = l + (r - l) / 2;
        tree[node].left = build(l, mid, a);
        tree[node].right = build(mid + 1, r, a);
        tree[node].sum = tree[tree[node].left].sum + tree[tree[node].right].sum;
        return node;
    }

    int update(int prev_node, int l, int r, int idx, long long val) {
        int node = tree.size();
        tree.push_back(tree[prev_node]);
        if (l == r) {
            tree[node].sum = val;
            return node;
        }
        int mid = l + (r - l) / 2;
        if (idx <= mid) {
            tree[node].left = update(tree[prev_node].left, l, mid, idx, val);
        } else {
            tree[node].right = update(tree[prev_node].right, mid + 1, r, idx, val);
        }
        tree[node].sum = tree[tree[node].left].sum + tree[tree[node].right].sum;
        return node;
    }

    long long query(int node, int l, int r, int ql, int qr) const {
        if (node == 0 || ql > r || qr < l || ql > qr) return 0;
        if (ql <= l && r <= qr) return tree[node].sum;
        int mid = l + (r - l) / 2;
        return query(tree[node].left, l, mid, ql, qr) + query(tree[node].right, mid + 1, r, ql, qr);
    }

public:
    PersistentSegmentTree(const vector<long long>& a) {
        n = a.size();
        tree.emplace_back(); // 0 is dummy null node
        roots.push_back(build(0, n - 1, a));
    }

    int update_version(int parent_version, int idx, long long val) {
        int new_root = update(roots[parent_version], 0, n - 1, idx, val);
        roots.push_back(new_root);
        return roots.size() - 1;
    }

    long long query_version(int version, int l, int r) const {
        return query(roots[version], 0, n - 1, l, r);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q)) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    PersistentSegmentTree pst(a);
    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int ver, idx;
            long long val;
            cin >> ver >> idx >> val;
            pst.update_version(ver, idx, val);
        } else {
            int ver, l, r;
            cin >> ver >> l >> r;
            cout << pst.query_version(ver, l, r) << "\\n";
        }
    }
    return 0;
}
"""


def generate_dynamic_segment_tree_cpp(p: Dict[str, Any]) -> str:
    return """#include <iostream>
#include <vector>

using namespace std;

class DynamicSegmentTree {
public:
    struct Node {
        long long sum;
        int left, right;
        Node() : sum(0), left(0), right(0) {}
    };

private:
    long long lower_bound;
    long long upper_bound;
    vector<Node> pool;
    int root;

    int allocate_node() {
        pool.emplace_back();
        return pool.size() - 1;
    }

    void update(int& node, long long l, long long r, long long idx, long long val) {
        if (!node) node = allocate_node();
        pool[node].sum += val;
        if (l == r) return;
        long long mid = l + (r - l) / 2;
        if (idx <= mid) {
            int left_child = pool[node].left;
            update(left_child, l, mid, idx, val);
            pool[node].left = left_child;
        } else {
            int right_child = pool[node].right;
            update(right_child, mid + 1, r, idx, val);
            pool[node].right = right_child;
        }
    }

    long long query(int node, long long l, long long r, long long ql, long long qr) const {
        if (!node || ql > r || qr < l || ql > qr) return 0;
        if (ql <= l && r <= qr) return pool[node].sum;
        long long mid = l + (r - l) / 2;
        return query(pool[node].left, l, mid, ql, qr) + query(pool[node].right, mid + 1, r, ql, qr);
    }

public:
    DynamicSegmentTree(long long low = 1, long long high = 1e18) : lower_bound(low), upper_bound(high) {
        pool.emplace_back(); // index 0 is null
        root = allocate_node();
    }

    void update(long long idx, long long val) {
        update(root, lower_bound, upper_bound, idx, val);
    }

    long long query(long long l, long long r) const {
        return query(root, lower_bound, upper_bound, l, r);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    DynamicSegmentTree dst(1, 1000000000LL);
    int q;
    if (!(cin >> q)) return 0;
    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            long long idx, val;
            cin >> idx >> val;
            dst.update(idx, val);
        } else {
            long long l, r;
            cin >> l >> r;
            cout << dst.query(l, r) << "\\n";
        }
    }
    return 0;
}
"""


def generate_merge_sort_tree_cpp(p: Dict[str, Any]) -> str:
    return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

class MergeSortTree {
private:
    int n;
    vector<vector<int>> tree;

    void build(int node, int l, int r, const vector<int>& a) {
        if (l == r) {
            tree[node] = {a[l]};
            return;
        }
        int mid = l + (r - l) / 2;
        build(2 * node, l, mid, a);
        build(2 * node + 1, mid + 1, r, a);
        tree[node].resize(tree[2 * node].size() + tree[2 * node + 1].size());
        merge(tree[2 * node].begin(), tree[2 * node].end(),
              tree[2 * node + 1].begin(), tree[2 * node + 1].end(),
              tree[node].begin());
    }

    int query(int node, int l, int r, int ql, int qr, int x) const {
        if (ql > r || qr < l || ql > qr) return 0;
        if (ql <= l && r <= qr) {
            return upper_bound(tree[node].begin(), tree[node].end(), x) - tree[node].begin();
        }
        int mid = l + (r - l) / 2;
        return query(2 * node, l, mid, ql, qr, x) + query(2 * node + 1, mid + 1, r, ql, qr, x);
    }

public:
    MergeSortTree(const vector<int>& a) {
        n = a.size();
        tree.assign(4 * n + 1, vector<int>());
        build(1, 0, n - 1, a);
    }

    int count_leq(int l, int r, int x) const {
        return query(1, 0, n - 1, l, r, x);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q)) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    MergeSortTree mst(a);
    while (q--) {
        int l, r, x;
        cin >> l >> r >> x;
        cout << mst.count_leq(l, r, x) << "\\n";
    }
    return 0;
}
"""


def generate_sqrt_decomposition_cpp(p: Dict[str, Any]) -> str:
    return """#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

class SqrtDecomposition {
private:
    int n, block_size, num_blocks;
    vector<long long> a;
    vector<long long> block_sum;
    vector<long long> block_lazy;

public:
    SqrtDecomposition(const vector<long long>& arr) {
        n = arr.size();
        block_size = max(1, (int)sqrt(n));
        num_blocks = (n + block_size - 1) / block_size;
        a = arr;
        block_sum.assign(num_blocks, 0);
        block_lazy.assign(num_blocks, 0);

        for (int i = 0; i < n; ++i) {
            block_sum[i / block_size] += a[i];
        }
    }

    void range_add(int l, int r, long long val) {
        int bl = l / block_size;
        int br = r / block_size;

        if (bl == br) {
            for (int i = l; i <= r; ++i) {
                a[i] += val;
                block_sum[bl] += val;
            }
        } else {
            for (int i = l; i < (bl + 1) * block_size; ++i) {
                a[i] += val;
                block_sum[bl] += val;
            }
            for (int b = bl + 1; b < br; ++b) {
                block_lazy[b] += val;
            }
            for (int i = br * block_size; i <= r; ++i) {
                a[i] += val;
                block_sum[br] += val;
            }
        }
    }

    long long range_sum(int l, int r) {
        int bl = l / block_size;
        int br = r / block_size;
        long long res = 0;

        if (bl == br) {
            for (int i = l; i <= r; ++i) {
                res += a[i] + block_lazy[bl];
            }
        } else {
            for (int i = l; i < (bl + 1) * block_size; ++i) {
                res += a[i] + block_lazy[bl];
            }
            for (int b = bl + 1; b < br; ++b) {
                res += block_sum[b] + block_lazy[b] * block_size;
            }
            for (int i = br * block_size; i <= r; ++i) {
                res += a[i] + block_lazy[br];
            }
        }
        return res;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q)) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    SqrtDecomposition sd(a);
    while (q--) {
        int type, l, r;
        cin >> type >> l >> r;
        if (type == 1) {
            long long val;
            cin >> val;
            sd.range_add(l, r, val);
        } else {
            cout << sd.range_sum(l, r) << "\\n";
        }
    }
    return 0;
}
"""


def generate_mos_algorithm_cpp(p: Dict[str, Any]) -> str:
    return """#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

using namespace std;

struct Query {
    int l, r, id;
};

int block_size;

bool mo_cmp(const Query& a, const Query& b) {
    int b1 = a.l / block_size;
    int b2 = b.l / block_size;
    if (b1 != b2) return b1 < b2;
    return (b1 % 2 == 0) ? (a.r < b.r) : (a.r > b.r);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q)) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    block_size = max(1, (int)sqrt(n));
    vector<Query> queries(q);
    for (int i = 0; i < q; ++i) {
        cin >> queries[i].l >> queries[i].r;
        queries[i].id = i;
    }

    sort(queries.begin(), queries.end(), mo_cmp);

    vector<int> freq(1000005, 0);
    int distinct_count = 0;

    auto add = [&](int x) {
        if (++freq[x] == 1) distinct_count++;
    };

    auto remove = [&](int x) {
        if (--freq[x] == 0) distinct_count--;
    };

    int cur_l = 0, cur_r = -1;
    vector<int> ans(q);

    for (const auto& qry : queries) {
        while (cur_l > qry.l) add(a[--cur_l]);
        while (cur_r < qry.r) add(a[++cur_r]);
        while (cur_l < qry.l) remove(a[cur_l++]);
        while (cur_r > qry.r) remove(a[cur_r--]);
        ans[qry.id] = distinct_count;
    }

    for (int i = 0; i < q; ++i) {
        cout << ans[i] << "\\n";
    }
    return 0;
}
"""


def generate_segment_tree_beats_cpp(p: Dict[str, Any]) -> str:
    return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const long long INF = 2e18;

class SegmentTreeBeats {
private:
    struct Node {
        long long sum;
        long long max1, max2;
        int cnt_max;
    };

    int n;
    vector<Node> tree;

    void pushup(int node) {
        int l = 2 * node, r = 2 * node + 1;
        tree[node].sum = tree[l].sum + tree[r].sum;

        if (tree[l].max1 == tree[r].max1) {
            tree[node].max1 = tree[l].max1;
            tree[node].cnt_max = tree[l].cnt_max + tree[r].cnt_max;
            tree[node].max2 = max(tree[l].max2, tree[r].max2);
        } else if (tree[l].max1 > tree[r].max1) {
            tree[node].max1 = tree[l].max1;
            tree[node].cnt_max = tree[l].cnt_max;
            tree[node].max2 = max(tree[l].max2, tree[r].max1);
        } else {
            tree[node].max1 = tree[r].max1;
            tree[node].cnt_max = tree[r].cnt_max;
            tree[node].max2 = max(tree[l].max1, tree[r].max2);
        }
    }

    void apply_chmin(int node, long long v) {
        if (v >= tree[node].max1) return;
        tree[node].sum -= (tree[node].max1 - v) * tree[node].cnt_max;
        tree[node].max1 = v;
    }

    void pushdown(int node) {
        int l = 2 * node, r = 2 * node + 1;
        if (tree[l].max1 > tree[node].max1) apply_chmin(l, tree[node].max1);
        if (tree[r].max1 > tree[node].max1) apply_chmin(r, tree[node].max1);
    }

    void build(int node, int l, int r, const vector<long long>& a) {
        if (l == r) {
            tree[node].sum = a[l];
            tree[node].max1 = a[l];
            tree[node].max2 = -INF;
            tree[node].cnt_max = 1;
            return;
        }
        int mid = l + (r - l) / 2;
        build(2 * node, l, mid, a);
        build(2 * node + 1, mid + 1, r, a);
        pushup(node);
    }

    void update_chmin(int node, int l, int r, int ql, int qr, long long v) {
        if (ql > r || qr < l || v >= tree[node].max1) return;
        if (ql <= l && r <= qr && v > tree[node].max2) {
            apply_chmin(node, v);
            return;
        }
        pushdown(node);
        int mid = l + (r - l) / 2;
        update_chmin(2 * node, l, mid, ql, qr, v);
        update_chmin(2 * node + 1, mid + 1, r, ql, qr, v);
        pushup(node);
    }

    long long query_sum(int node, int l, int r, int ql, int qr) {
        if (ql > r || qr < l) return 0;
        if (ql <= l && r <= qr) return tree[node].sum;
        pushdown(node);
        int mid = l + (r - l) / 2;
        return query_sum(2 * node, l, mid, ql, qr) + query_sum(2 * node + 1, mid + 1, r, ql, qr);
    }

    long long query_max(int node, int l, int r, int ql, int qr) {
        if (ql > r || qr < l) return -INF;
        if (ql <= l && r <= qr) return tree[node].max1;
        pushdown(node);
        int mid = l + (r - l) / 2;
        return max(query_max(2 * node, l, mid, ql, qr), query_max(2 * node + 1, mid + 1, r, ql, qr));
    }

public:
    SegmentTreeBeats(const vector<long long>& a) {
        n = a.size();
        tree.assign(4 * n + 1, Node());
        build(1, 0, n - 1, a);
    }

    void chmin(int l, int r, long long v) {
        update_chmin(1, 0, n - 1, l, r, v);
    }

    long long get_sum(int l, int r) {
        return query_sum(1, 0, n - 1, l, r);
    }

    long long get_max(int l, int r) {
        return query_max(1, 0, n - 1, l, r);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q)) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    SegmentTreeBeats stb(a);
    while (q--) {
        int type, l, r;
        cin >> type >> l >> r;
        if (type == 1) {
            long long v;
            cin >> v;
            stb.chmin(l, r, v);
        } else if (type == 2) {
            cout << stb.get_sum(l, r) << "\\n";
        } else {
            cout << stb.get_max(l, r) << "\\n";
        }
    }
    return 0;
}
"""
