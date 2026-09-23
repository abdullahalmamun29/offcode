"""
C++17 Code Generator for Segment Tree Domain (Phase 3J).

Generates production-grade C++17 implementations for:
1. segment_tree_point_update_range_query
2. segment_tree_range_add_range_query
3. segment_tree_range_assign_range_query
4. segment_tree_combined_lazy_range_query
5. segment_tree_metadata_aggregate
6. segment_tree_max_subarray
7. segment_tree_frequency_order_statistic
8. segment_tree_interval_statistics
"""

from typing import Dict, Any


def generate_segment_tree_cpp(pattern: str, params: Dict[str, Any]) -> str:
    # ── 1. Point Update Range Query (Tier A) ──
    if pattern == "segment_tree_point_update_range_query":
        op = params.get("segment_tree_query_op", "sum")
        if op == "min":
            identity = "LLONG_MAX"
            merge_expr = "min(left_val, right_val)"
            update_op = "val"
        elif op == "max":
            identity = "LLONG_MIN"
            merge_expr = "max(left_val, right_val)"
            update_op = "val"
        elif op == "gcd":
            identity = "0LL"
            merge_expr = "std::gcd(left_val, right_val)"
            update_op = "val"
        else:  # sum
            identity = "0LL"
            merge_expr = "left_val + right_val"
            update_op = "val"

        return f"""#include <iostream>
#include <vector>
#include <climits>
#include <numeric>
#include <algorithm>

using namespace std;

// Segment Tree for Point Updates and Range Queries
// 1-based indexing internally: root at 1 covering [1, n]
struct SegmentTree {{
    int n;
    vector<long long> tree;

    SegmentTree(int n) : n(n), tree(4 * n + 1, {identity}) {{}}

    SegmentTree(const vector<long long>& a) : n(a.size() - 1), tree(4 * (a.size() - 1) + 1, {identity}) {{
        build(1, 1, n, a);
    }}

    long long merge(long long left_val, long long right_val) const {{
        if (left_val == {identity}) return right_val;
        if (right_val == {identity}) return left_val;
        return {merge_expr};
    }}

    void build(int p, int l, int r, const vector<long long>& a) {{
        if (l == r) {{
            tree[p] = a[l];
            return;
        }}
        int mid = l + (r - l) / 2;
        build(2 * p, l, mid, a);
        build(2 * p + 1, mid + 1, r, a);
        tree[p] = merge(tree[2 * p], tree[2 * p + 1]);
    }}

    void update(int p, int l, int r, int idx, long long val) {{
        if (l == r) {{
            tree[p] = {update_op};
            return;
        }}
        int mid = l + (r - l) / 2;
        if (idx <= mid) {{
            update(2 * p, l, mid, idx, val);
        }} else {{
            update(2 * p + 1, mid + 1, r, idx, val);
        }}
        tree[p] = merge(tree[2 * p], tree[2 * p + 1]);
    }}

    long long query(int p, int l, int r, int ql, int qr) const {{
        if (ql <= l && r <= qr) {{
            return tree[p];
        }}
        int mid = l + (r - l) / 2;
        long long res = {identity};
        if (ql <= mid) {{
            res = merge(res, query(2 * p, l, mid, ql, qr));
        }}
        if (qr > mid) {{
            res = merge(res, query(2 * p + 1, mid + 1, r, ql, qr));
        }}
        return res;
    }}

    void point_update(int idx, long long val) {{
        update(1, 1, n, idx, val);
    }}

    long long range_query(int ql, int qr) const {{
        if (ql > qr) return {identity};
        return query(1, 1, n, ql, qr);
    }}
}};

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) {{
        cin >> a[i];
    }}

    SegmentTree st(a);

    while (q--) {{
        int type;
        cin >> type;
        if (type == 1) {{
            // Point update: set value at idx
            int idx;
            long long val;
            cin >> idx >> val;
            st.point_update(idx, val);
        }} else if (type == 2) {{
            // Range query: [ql, qr]
            int ql, qr;
            cin >> ql >> qr;
            cout << st.range_query(ql, qr) << "\\n";
        }}
    }}

    return 0;
}}
"""

    # ── 2. Range Add Range Query (Tier A) ──
    if pattern == "segment_tree_range_add_range_query":
        return """#include <iostream>
#include <vector>

using namespace std;

// Segment Tree with Lazy Propagation for Range Add and Range Sum Queries
// 1-based indexing internally: root at 1 covering [1, n]
struct LazySegmentTree {
    int n;
    vector<long long> tree;
    vector<long long> lazy;

    LazySegmentTree(int n) : n(n), tree(4 * n + 1, 0), lazy(4 * n + 1, 0) {}

    LazySegmentTree(const vector<long long>& a) : n(a.size() - 1), tree(4 * (a.size() - 1) + 1, 0), lazy(4 * (a.size() - 1) + 1, 0) {
        build(1, 1, n, a);
    }

    void build(int p, int l, int r, const vector<long long>& a) {
        if (l == r) {
            tree[p] = a[l];
            return;
        }
        int mid = l + (r - l) / 2;
        build(2 * p, l, mid, a);
        build(2 * p + 1, mid + 1, r, a);
        tree[p] = tree[2 * p] + tree[2 * p + 1];
    }

    void apply_add(int p, int l, int r, long long val) {
        tree[p] += (r - l + 1) * val;
        lazy[p] += val;
    }

    void push_down(int p, int l, int r) {
        if (lazy[p] != 0) {
            int mid = l + (r - l) / 2;
            apply_add(2 * p, l, mid, lazy[p]);
            apply_add(2 * p + 1, mid + 1, r, lazy[p]);
            lazy[p] = 0;
        }
    }

    void range_add(int p, int l, int r, int ql, int qr, long long val) {
        if (ql <= l && r <= qr) {
            apply_add(p, l, r, val);
            return;
        }
        push_down(p, l, r);
        int mid = l + (r - l) / 2;
        if (ql <= mid) {
            range_add(2 * p, l, mid, ql, qr, val);
        }
        if (qr > mid) {
            range_add(2 * p + 1, mid + 1, r, ql, qr, val);
        }
        tree[p] = tree[2 * p] + tree[2 * p + 1];
    }

    long long range_query(int p, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) {
            return tree[p];
        }
        push_down(p, l, r);
        int mid = l + (r - l) / 2;
        long long sum = 0;
        if (ql <= mid) {
            sum += range_query(2 * p, l, mid, ql, qr);
        }
        if (qr > mid) {
            sum += range_query(2 * p + 1, mid + 1, r, ql, qr);
        }
        return sum;
    }

    void update_range(int ql, int qr, long long val) {
        if (ql <= qr) range_add(1, 1, n, ql, qr, val);
    }

    long long query_range(int ql, int qr) {
        if (ql > qr) return 0;
        return range_query(1, 1, n, ql, qr);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    LazySegmentTree st(a);

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            // Range add: add val to [ql, qr]
            int ql, qr;
            long long val;
            cin >> ql >> qr >> val;
            st.update_range(ql, qr, val);
        } else if (type == 2) {
            // Range sum query: [ql, qr]
            int ql, qr;
            cin >> ql >> qr;
            cout << st.query_range(ql, qr) << "\\n";
        }
    }

    return 0;
}
"""

    # ── 3. Range Assign Range Query (Tier A) ──
    if pattern == "segment_tree_range_assign_range_query":
        return """#include <iostream>
#include <vector>

using namespace std;

// Segment Tree with Lazy Propagation for Range Assignment and Range Sum Queries
// 1-based indexing internally: root at 1 covering [1, n]
struct AssignSegmentTree {
    int n;
    vector<long long> tree;
    vector<long long> assign_val;
    vector<bool> has_assign;

    AssignSegmentTree(int n) : n(n), tree(4 * n + 1, 0), assign_val(4 * n + 1, 0), has_assign(4 * n + 1, false) {}

    AssignSegmentTree(const vector<long long>& a)
        : n(a.size() - 1), tree(4 * (a.size() - 1) + 1, 0), assign_val(4 * (a.size() - 1) + 1, 0), has_assign(4 * (a.size() - 1) + 1, false) {
        build(1, 1, n, a);
    }

    void build(int p, int l, int r, const vector<long long>& a) {
        if (l == r) {
            tree[p] = a[l];
            return;
        }
        int mid = l + (r - l) / 2;
        build(2 * p, l, mid, a);
        build(2 * p + 1, mid + 1, r, a);
        tree[p] = tree[2 * p] + tree[2 * p + 1];
    }

    void apply_assign(int p, int l, int r, long long val) {
        tree[p] = (r - l + 1) * val;
        assign_val[p] = val;
        has_assign[p] = true;
    }

    void push_down(int p, int l, int r) {
        if (has_assign[p]) {
            int mid = l + (r - l) / 2;
            apply_assign(2 * p, l, mid, assign_val[p]);
            apply_assign(2 * p + 1, mid + 1, r, assign_val[p]);
            has_assign[p] = false;
        }
    }

    void range_assign(int p, int l, int r, int ql, int qr, long long val) {
        if (ql <= l && r <= qr) {
            apply_assign(p, l, r, val);
            return;
        }
        push_down(p, l, r);
        int mid = l + (r - l) / 2;
        if (ql <= mid) {
            range_assign(2 * p, l, mid, ql, qr, val);
        }
        if (qr > mid) {
            range_assign(2 * p + 1, mid + 1, r, ql, qr, val);
        }
        tree[p] = tree[2 * p] + tree[2 * p + 1];
    }

    long long range_query(int p, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) {
            return tree[p];
        }
        push_down(p, l, r);
        int mid = l + (r - l) / 2;
        long long sum = 0;
        if (ql <= mid) {
            sum += range_query(2 * p, l, mid, ql, qr);
        }
        if (qr > mid) {
            sum += range_query(2 * p + 1, mid + 1, r, ql, qr);
        }
        return sum;
    }

    void update_range(int ql, int qr, long long val) {
        if (ql <= qr) range_assign(1, 1, n, ql, qr, val);
    }

    long long query_range(int ql, int qr) {
        if (ql > qr) return 0;
        return range_query(1, 1, n, ql, qr);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    AssignSegmentTree st(a);

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            // Range assign: set all elements in [ql, qr] to val
            int ql, qr;
            long long val;
            cin >> ql >> qr >> val;
            st.update_range(ql, qr, val);
        } else if (type == 2) {
            // Range sum query: [ql, qr]
            int ql, qr;
            cin >> ql >> qr;
            cout << st.query_range(ql, qr) << "\\n";
        }
    }

    return 0;
}
"""

    # ── 4. Combined Lazy Range Query (Tier A) ──
    if pattern == "segment_tree_combined_lazy_range_query":
        return """#include <iostream>
#include <vector>

using namespace std;

// Segment Tree with Combined Range Assignment and Range Addition
// Precedence invariant: Assignment resets addition; addition accumulates on current assignment
struct CombinedLazySegmentTree {
    struct Tag {
        bool has_assign;
        long long assign_val;
        long long add_val;

        Tag() : has_assign(false), assign_val(0), add_val(0) {}
    };

    int n;
    vector<long long> tree;
    vector<Tag> lazy;

    CombinedLazySegmentTree(int n) : n(n), tree(4 * n + 1, 0), lazy(4 * n + 1) {}

    CombinedLazySegmentTree(const vector<long long>& a)
        : n(a.size() - 1), tree(4 * (a.size() - 1) + 1, 0), lazy(4 * (a.size() - 1) + 1) {
        build(1, 1, n, a);
    }

    void build(int p, int l, int r, const vector<long long>& a) {
        if (l == r) {
            tree[p] = a[l];
            return;
        }
        int mid = l + (r - l) / 2;
        build(2 * p, l, mid, a);
        build(2 * p + 1, mid + 1, r, a);
        tree[p] = tree[2 * p] + tree[2 * p + 1];
    }

    void apply_tag(int p, int l, int r, const Tag& tag) {
        if (tag.has_assign) {
            tree[p] = (r - l + 1) * tag.assign_val;
            lazy[p].has_assign = true;
            lazy[p].assign_val = tag.assign_val;
            lazy[p].add_val = 0;
        }
        if (tag.add_val != 0) {
            tree[p] += (r - l + 1) * tag.add_val;
            if (lazy[p].has_assign) {
                lazy[p].assign_val += tag.add_val;
            } else {
                lazy[p].add_val += tag.add_val;
            }
        }
    }

    void push_down(int p, int l, int r) {
        if (lazy[p].has_assign || lazy[p].add_val != 0) {
            int mid = l + (r - l) / 2;
            apply_tag(2 * p, l, mid, lazy[p]);
            apply_tag(2 * p + 1, mid + 1, r, lazy[p]);
            lazy[p] = Tag();
        }
    }

    void range_assign(int p, int l, int r, int ql, int qr, long long val) {
        if (ql <= l && r <= qr) {
            Tag tag;
            tag.has_assign = true;
            tag.assign_val = val;
            apply_tag(p, l, r, tag);
            return;
        }
        push_down(p, l, r);
        int mid = l + (r - l) / 2;
        if (ql <= mid) range_assign(2 * p, l, mid, ql, qr, val);
        if (qr > mid) range_assign(2 * p + 1, mid + 1, r, ql, qr, val);
        tree[p] = tree[2 * p] + tree[2 * p + 1];
    }

    void range_add(int p, int l, int r, int ql, int qr, long long val) {
        if (ql <= l && r <= qr) {
            Tag tag;
            tag.add_val = val;
            apply_tag(p, l, r, tag);
            return;
        }
        push_down(p, l, r);
        int mid = l + (r - l) / 2;
        if (ql <= mid) range_add(2 * p, l, mid, ql, qr, val);
        if (qr > mid) range_add(2 * p + 1, mid + 1, r, ql, qr, val);
        tree[p] = tree[2 * p] + tree[2 * p + 1];
    }

    long long range_query(int p, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) {
            return tree[p];
        }
        push_down(p, l, r);
        int mid = l + (r - l) / 2;
        long long sum = 0;
        if (ql <= mid) sum += range_query(2 * p, l, mid, ql, qr);
        if (qr > mid) sum += range_query(2 * p + 1, mid + 1, r, ql, qr);
        return sum;
    }

    void assign_range(int ql, int qr, long long val) {
        if (ql <= qr) range_assign(1, 1, n, ql, qr, val);
    }

    void add_range(int ql, int qr, long long val) {
        if (ql <= qr) range_add(1, 1, n, ql, qr, val);
    }

    long long query_range(int ql, int qr) {
        if (ql > qr) return 0;
        return range_query(1, 1, n, ql, qr);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    CombinedLazySegmentTree st(a);

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            // Range add: [ql, qr] += val
            int ql, qr;
            long long val;
            cin >> ql >> qr >> val;
            st.add_range(ql, qr, val);
        } else if (type == 2) {
            // Range assign: [ql, qr] = val
            int ql, qr;
            long long val;
            cin >> ql >> qr >> val;
            st.assign_range(ql, qr, val);
        } else if (type == 3) {
            // Range sum query: [ql, qr]
            int ql, qr;
            cin >> ql >> qr;
            cout << st.query_range(ql, qr) << "\\n";
        }
    }

    return 0;
}
"""

    # ── 5. Metadata Aggregate (Tier A) ──
    if pattern == "segment_tree_metadata_aggregate":
        return """#include <iostream>
#include <vector>
#include <climits>
#include <algorithm>

using namespace std;

// Segment Tree for Simultaneous Multi-Attribute Metadata Aggregation
// Node stores: (sum, min_val, max_val, count)
struct MetadataNode {
    long long sum;
    long long min_val;
    long long max_val;
    long long count;

    MetadataNode() : sum(0), min_val(LLONG_MAX), max_val(LLONG_MIN), count(0) {}
    MetadataNode(long long val) : sum(val), min_val(val), max_val(val), count(1) {}
    MetadataNode(long long s, long long mn, long long mx, long long c)
        : sum(s), min_val(mn), max_val(mx), count(c) {}
};

MetadataNode merge_nodes(const MetadataNode& L, const MetadataNode& R) {
    if (L.count == 0) return R;
    if (R.count == 0) return L;
    return MetadataNode(
        L.sum + R.sum,
        min(L.min_val, R.min_val),
        max(L.max_val, R.max_val),
        L.count + R.count
    );
}

struct MetadataSegmentTree {
    int n;
    vector<MetadataNode> tree;

    MetadataSegmentTree(int n) : n(n), tree(4 * n + 1) {}

    MetadataSegmentTree(const vector<long long>& a) : n(a.size() - 1), tree(4 * (a.size() - 1) + 1) {
        build(1, 1, n, a);
    }

    void build(int p, int l, int r, const vector<long long>& a) {
        if (l == r) {
            tree[p] = MetadataNode(a[l]);
            return;
        }
        int mid = l + (r - l) / 2;
        build(2 * p, l, mid, a);
        build(2 * p + 1, mid + 1, r, a);
        tree[p] = merge_nodes(tree[2 * p], tree[2 * p + 1]);
    }

    void update(int p, int l, int r, int idx, long long val) {
        if (l == r) {
            tree[p] = MetadataNode(val);
            return;
        }
        int mid = l + (r - l) / 2;
        if (idx <= mid) update(2 * p, l, mid, idx, val);
        else update(2 * p + 1, mid + 1, r, idx, val);
        tree[p] = merge_nodes(tree[2 * p], tree[2 * p + 1]);
    }

    MetadataNode query(int p, int l, int r, int ql, int qr) const {
        if (ql <= l && r <= qr) {
            return tree[p];
        }
        int mid = l + (r - l) / 2;
        MetadataNode res;
        if (ql <= mid) res = merge_nodes(res, query(2 * p, l, mid, ql, qr));
        if (qr > mid) res = merge_nodes(res, query(2 * p + 1, mid + 1, r, ql, qr));
        return res;
    }

    void point_update(int idx, long long val) {
        update(1, 1, n, idx, val);
    }

    MetadataNode range_query(int ql, int qr) const {
        if (ql > qr) return MetadataNode();
        return query(1, 1, n, ql, qr);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    MetadataSegmentTree st(a);

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int idx;
            long long val;
            cin >> idx >> val;
            st.point_update(idx, val);
        } else if (type == 2) {
            int ql, qr;
            cin >> ql >> qr;
            MetadataNode res = st.range_query(ql, qr);
            cout << res.sum << " " << res.min_val << " " << res.max_val << " " << res.count << "\\n";
        }
    }

    return 0;
}
"""

    # ── 6. Maximum Subarray Sum (Tier B) ──
    if pattern == "segment_tree_max_subarray":
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Segment Tree for Maximum Contiguous Subarray Sum Queries (Non-empty contiguous subarray convention)
// Node maintains: (sum, pref, suff, ans, empty)
struct MaxSubarrayNode {
    long long sum;
    long long pref;
    long long suff;
    long long ans;
    bool empty;

    MaxSubarrayNode() : sum(0), pref(0), suff(0), ans(0), empty(true) {}
    MaxSubarrayNode(long long val) : sum(val), pref(val), suff(val), ans(val), empty(false) {}
};

MaxSubarrayNode merge_nodes(const MaxSubarrayNode& L, const MaxSubarrayNode& R) {
    if (L.empty) return R;
    if (R.empty) return L;
    MaxSubarrayNode res;
    res.empty = false;
    res.sum = L.sum + R.sum;
    res.pref = max(L.pref, L.sum + R.pref);
    res.suff = max(R.suff, R.sum + L.suff);
    res.ans = max({L.ans, R.ans, L.suff + R.pref});
    return res;
}

struct MaxSubarraySegmentTree {
    int n;
    vector<MaxSubarrayNode> tree;

    MaxSubarraySegmentTree(int n) : n(n), tree(4 * n + 1) {}

    MaxSubarraySegmentTree(const vector<long long>& a) : n(a.size() - 1), tree(4 * (a.size() - 1) + 1) {
        build(1, 1, n, a);
    }

    void build(int p, int l, int r, const vector<long long>& a) {
        if (l == r) {
            tree[p] = MaxSubarrayNode(a[l]);
            return;
        }
        int mid = l + (r - l) / 2;
        build(2 * p, l, mid, a);
        build(2 * p + 1, mid + 1, r, a);
        tree[p] = merge_nodes(tree[2 * p], tree[2 * p + 1]);
    }

    void update(int p, int l, int r, int idx, long long val) {
        if (l == r) {
            tree[p] = MaxSubarrayNode(val);
            return;
        }
        int mid = l + (r - l) / 2;
        if (idx <= mid) update(2 * p, l, mid, idx, val);
        else update(2 * p + 1, mid + 1, r, idx, val);
        tree[p] = merge_nodes(tree[2 * p], tree[2 * p + 1]);
    }

    MaxSubarrayNode query(int p, int l, int r, int ql, int qr) const {
        if (ql <= l && r <= qr) {
            return tree[p];
        }
        int mid = l + (r - l) / 2;
        MaxSubarrayNode res;
        if (ql <= mid) res = merge_nodes(res, query(2 * p, l, mid, ql, qr));
        if (qr > mid) res = merge_nodes(res, query(2 * p + 1, mid + 1, r, ql, qr));
        return res;
    }

    void point_update(int idx, long long val) {
        update(1, 1, n, idx, val);
    }

    long long query_max_subarray(int ql, int qr) const {
        if (ql > qr) return 0;
        return query(1, 1, n, ql, qr).ans;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    MaxSubarraySegmentTree st(a);

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int idx;
            long long val;
            cin >> idx >> val;
            st.point_update(idx, val);
        } else if (type == 2) {
            int ql, qr;
            cin >> ql >> qr;
            cout << st.query_max_subarray(ql, qr) << "\\n";
        }
    }

    return 0;
}
"""

    # ── 7. Frequency Order Statistic (Tier B) ──
    if pattern == "segment_tree_frequency_order_statistic":
        return """#include <iostream>
#include <vector>

using namespace std;

// Frequency Segment Tree for Order Statistics (k-th Smallest Element Search)
// Covers value domain [1, max_val]; node stores frequency sum in subtree
// Invariant: Non-negative frequencies ensure monotonic subtree counts for binary descent
struct FrequencySegmentTree {
    int max_val;
    vector<long long> tree;

    FrequencySegmentTree(int max_val) : max_val(max_val), tree(4 * max_val + 1, 0) {}

    void add(int p, int l, int r, int val, long long count) {
        tree[p] += count;
        if (l == r) return;
        int mid = l + (r - l) / 2;
        if (val <= mid) add(2 * p, l, mid, val, count);
        else add(2 * p + 1, mid + 1, r, val, count);
    }

    // Binary descent / tree walk to find k-th smallest element (1-based k)
    int find_kth(int p, int l, int r, long long k) const {
        if (l == r) return l;
        int mid = l + (r - l) / 2;
        if (tree[2 * p] >= k) {
            return find_kth(2 * p, l, mid, k);
        } else {
            return find_kth(2 * p + 1, mid + 1, r, k - tree[2 * p]);
        }
    }

    void insert_value(int val, long long count = 1) {
        if (val >= 1 && val <= max_val) {
            add(1, 1, max_val, val, count);
        }
    }

    void remove_value(int val, long long count = 1) {
        if (val >= 1 && val <= max_val) {
            add(1, 1, max_val, val, -count);
        }
    }

    int query_kth(long long k) const {
        if (k < 1 || k > tree[1]) return -1;
        return find_kth(1, 1, max_val, k);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int max_val, q;
    if (!(cin >> max_val >> q) || max_val <= 0) return 0;

    FrequencySegmentTree st(max_val);

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            // Insert element
            int val;
            cin >> val;
            st.insert_value(val);
        } else if (type == 2) {
            // Delete element
            int val;
            cin >> val;
            st.remove_value(val);
        } else if (type == 3) {
            // Query k-th smallest
            long long k;
            cin >> k;
            cout << st.query_kth(k) << "\\n";
        }
    }

    return 0;
}
"""

    # ── 8. Interval Statistics (Tier B) ──
    if pattern == "segment_tree_interval_statistics":
        return """#include <iostream>
#include <vector>
#include <climits>
#include <algorithm>

using namespace std;

// Segment Tree for Range Extrema with Multiplicity (Min and Max with Frequency)
struct ExtremaNode {
    long long min_val;
    int min_count;
    long long max_val;
    int max_count;

    ExtremaNode() : min_val(LLONG_MAX), min_count(0), max_val(LLONG_MIN), max_count(0) {}
    ExtremaNode(long long val) : min_val(val), min_count(1), max_val(val), max_count(1) {}
    ExtremaNode(long long mn, int mnc, long long mx, int mxc)
        : min_val(mn), min_count(mnc), max_val(mx), max_count(mxc) {}
};

ExtremaNode merge_extrema(const ExtremaNode& L, const ExtremaNode& R) {
    if (L.min_count == 0) return R;
    if (R.min_count == 0) return L;

    long long res_min;
    int res_min_cnt;
    if (L.min_val < R.min_val) {
        res_min = L.min_val;
        res_min_cnt = L.min_count;
    } else if (L.min_val > R.min_val) {
        res_min = R.min_val;
        res_min_cnt = R.min_count;
    } else {
        res_min = L.min_val;
        res_min_cnt = L.min_count + R.min_count;
    }

    long long res_max;
    int res_max_cnt;
    if (L.max_val > R.max_val) {
        res_max = L.max_val;
        res_max_cnt = L.max_count;
    } else if (L.max_val < R.max_val) {
        res_max = R.max_val;
        res_max_cnt = R.max_count;
    } else {
        res_max = L.max_val;
        res_max_cnt = L.max_count + R.max_count;
    }

    return ExtremaNode(res_min, res_min_cnt, res_max, res_max_cnt);
}

struct IntervalStatisticsSegmentTree {
    int n;
    vector<ExtremaNode> tree;

    IntervalStatisticsSegmentTree(int n) : n(n), tree(4 * n + 1) {}

    IntervalStatisticsSegmentTree(const vector<long long>& a) : n(a.size() - 1), tree(4 * (a.size() - 1) + 1) {
        build(1, 1, n, a);
    }

    void build(int p, int l, int r, const vector<long long>& a) {
        if (l == r) {
            tree[p] = ExtremaNode(a[l]);
            return;
        }
        int mid = l + (r - l) / 2;
        build(2 * p, l, mid, a);
        build(2 * p + 1, mid + 1, r, a);
        tree[p] = merge_extrema(tree[2 * p], tree[2 * p + 1]);
    }

    void update(int p, int l, int r, int idx, long long val) {
        if (l == r) {
            tree[p] = ExtremaNode(val);
            return;
        }
        int mid = l + (r - l) / 2;
        if (idx <= mid) update(2 * p, l, mid, idx, val);
        else update(2 * p + 1, mid + 1, r, idx, val);
        tree[p] = merge_extrema(tree[2 * p], tree[2 * p + 1]);
    }

    ExtremaNode query(int p, int l, int r, int ql, int qr) const {
        if (ql <= l && r <= qr) {
            return tree[p];
        }
        int mid = l + (r - l) / 2;
        ExtremaNode res;
        if (ql <= mid) res = merge_extrema(res, query(2 * p, l, mid, ql, qr));
        if (qr > mid) res = merge_extrema(res, query(2 * p + 1, mid + 1, r, ql, qr));
        return res;
    }

    void point_update(int idx, long long val) {
        update(1, 1, n, idx, val);
    }

    ExtremaNode range_query(int ql, int qr) const {
        if (ql > qr) return ExtremaNode();
        return query(1, 1, n, ql, qr);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    IntervalStatisticsSegmentTree st(a);

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int idx;
            long long val;
            cin >> idx >> val;
            st.point_update(idx, val);
        } else if (type == 2) {
            int ql, qr;
            cin >> ql >> qr;
            ExtremaNode res = st.range_query(ql, qr);
            cout << res.min_val << " " << res.min_count << " " << res.max_val << " " << res.max_count << "\\n";
        }
    }

    return 0;
}
"""

    return "// Unsupported Segment Tree pattern: " + pattern
