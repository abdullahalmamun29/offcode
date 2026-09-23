"""
C++17 Code Generator for Fenwick Tree / Binary Indexed Tree (BIT) Domain (Phase 3I).

Generates production-grade C++17 implementations for:
1. fenwick_point_update_prefix_query
2. fenwick_range_update_point_query
3. fenwick_range_update_range_query
4. fenwick_frequency
5. fenwick_prefix_extremum
6. fenwick_2d_point_update_range_query
7. fenwick_kth_element
8. fenwick_inversion_counting
9. fenwick_multiset
10. fenwick_coordinate_compression
"""

from typing import Dict, Any


def generate_fenwick_cpp(pattern: str, params: Dict[str, Any]) -> str:
    if pattern == "fenwick_point_update_prefix_query":
        return """#include <iostream>
#include <vector>

using namespace std;

// Fenwick Tree (Binary Indexed Tree) for Point Updates and Prefix/Range Queries
// 1-based indexing internally: interval (i - lowbit(i), i]
struct FenwickTree {
    int n;
    vector<long long> tree;

    FenwickTree(int n) : n(n), tree(n + 1, 0) {}

    // Linear-time O(N) build from 1-based initial array
    FenwickTree(const vector<long long>& a) : n(a.size() - 1), tree(a.size(), 0) {
        for (int i = 1; i <= n; i++) {
            tree[i] += a[i];
            int parent = i + (i & -i);
            if (parent <= n) {
                tree[parent] += tree[i];
            }
        }
    }

    void add(int i, long long delta) {
        for (; i <= n; i += i & -i) {
            tree[i] += delta;
        }
    }

    long long query(int i) const {
        long long sum = 0;
        for (; i > 0; i -= i & -i) {
            sum += tree[i];
        }
        return sum;
    }

    long long range_query(int l, int r) const {
        if (l > r) return 0;
        return query(r) - query(l - 1);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    vector<long long> a(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    FenwickTree ft(a);

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            // Point update: add delta to position idx
            int idx;
            long long delta;
            cin >> idx >> delta;
            ft.add(idx, delta);
        } else if (type == 2) {
            // Range sum query: sum in [l, r]
            int l, r;
            cin >> l >> r;
            cout << ft.range_query(l, r) << "\\n";
        }
    }

    return 0;
}
"""

    if pattern == "fenwick_range_update_point_query":
        return """#include <iostream>
#include <vector>

using namespace std;

// Range Update, Point Query via Difference Array Fenwick Tree
// Maintains D[i] = A[i] - A[i-1]. Point value A[x] = prefix sum of D up to x.
struct RangeUpdatePointQueryBIT {
    int n;
    vector<long long> tree;

    RangeUpdatePointQueryBIT(int n) : n(n), tree(n + 1, 0) {}

    void add(int i, long long delta) {
        for (; i <= n; i += i & -i) {
            tree[i] += delta;
        }
    }

    // Range addition [l, r] with +delta
    void range_add(int l, int r, long long delta) {
        if (l > r) return;
        add(l, delta);
        add(r + 1, -delta);
    }

    // Point query at index i: sum of differences D[1..i]
    long long point_query(int i) const {
        long long val = 0;
        for (; i > 0; i -= i & -i) {
            val += tree[i];
        }
        return val;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    RangeUpdatePointQueryBIT bit(n);

    // Initial values loaded as point differences
    long long prev = 0;
    for (int i = 1; i <= n; i++) {
        long long cur;
        cin >> cur;
        bit.add(i, cur - prev);
        prev = cur;
    }

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            // Range addition [l, r] += delta
            int l, r;
            long long delta;
            cin >> l >> r >> delta;
            bit.range_add(l, r, delta);
        } else if (type == 2) {
            // Point query at index idx
            int idx;
            cin >> idx;
            cout << bit.point_query(idx) << "\\n";
        }
    }

    return 0;
}
"""

    if pattern == "fenwick_range_update_range_query":
        return """#include <iostream>
#include <vector>

using namespace std;

// Two-Fenwick Formulation for Range Updates and Range Queries
// B1 maintains D[j], B2 maintains j * D[j]
// Prefix sum: prefix(x) = (x + 1) * sum(B1, x) - sum(B2, x)
struct RangeUpdateRangeQueryBIT {
    int n;
    vector<long long> b1, b2;

    RangeUpdateRangeQueryBIT(int n) : n(n), b1(n + 1, 0), b2(n + 1, 0) {}

    void add_internal(vector<long long>& t, int i, long long delta) {
        for (; i <= n; i += i & -i) {
            t[i] += delta;
        }
    }

    long long query_internal(const vector<long long>& t, int i) const {
        long long s = 0;
        for (; i > 0; i -= i & -i) {
            s += t[i];
        }
        return s;
    }

    // Range addition [l, r] with +delta
    void range_add(int l, int r, long long delta) {
        if (l > r) return;
        add_internal(b1, l, delta);
        add_internal(b1, r + 1, -delta);
        add_internal(b2, l, delta * l);
        add_internal(b2, r + 1, -delta * (r + 1));
    }

    // Prefix sum sum_{i=1}^x A[i]
    long long prefix_query(int x) const {
        if (x <= 0) return 0;
        return 1LL * (x + 1) * query_internal(b1, x) - query_internal(b2, x);
    }

    // Arbitrary range sum [l, r]
    long long range_query(int l, int r) const {
        if (l > r) return 0;
        return prefix_query(r) - prefix_query(l - 1);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    RangeUpdateRangeQueryBIT rurq(n);

    for (int i = 1; i <= n; i++) {
        long long val;
        cin >> val;
        rurq.range_add(i, i, val);
    }

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            // Range update [l, r] += delta
            int l, r;
            long long delta;
            cin >> l >> r >> delta;
            rurq.range_add(l, r, delta);
        } else if (type == 2) {
            // Range sum query [l, r]
            int l, r;
            cin >> l >> r;
            cout << rurq.range_query(l, r) << "\\n";
        }
    }

    return 0;
}
"""

    if pattern == "fenwick_frequency":
        return """#include <iostream>
#include <vector>

using namespace std;

// Frequency Fenwick Tree over bounded domain [1..M]
// Tracks element counts, cumulative frequencies, and range counts
struct FrequencyBIT {
    int max_val;
    vector<int> tree;

    FrequencyBIT(int max_val) : max_val(max_val), tree(max_val + 1, 0) {}

    void insert(int val, int count = 1) {
        if (val < 1 || val > max_val) return;
        for (; val <= max_val; val += val & -val) {
            tree[val] += count;
        }
    }

    void remove(int val, int count = 1) {
        insert(val, -count);
    }

    // Number of elements with value <= val
    int count_leq(int val) const {
        if (val > max_val) val = max_val;
        int count = 0;
        for (; val > 0; val -= val & -val) {
            count += tree[val];
        }
        return count;
    }

    // Number of elements in range [low, high]
    int count_range(int low, int high) const {
        if (low > high) return 0;
        return count_leq(high) - count_leq(low - 1);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int m, q;
    if (!(cin >> m >> q) || m <= 0) return 0;

    FrequencyBIT freq(m);

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            // Insert value
            int val;
            cin >> val;
            freq.insert(val, 1);
        } else if (type == 2) {
            // Remove value
            int val;
            cin >> val;
            freq.remove(val, 1);
        } else if (type == 3) {
            // Count in range [l, r]
            int l, r;
            cin >> l >> r;
            cout << freq.count_range(l, r) << "\\n";
        }
    }

    return 0;
}
"""

    if pattern == "fenwick_prefix_extremum":
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Fenwick Prefix Extremum under Monotonic Updates
// Min Fenwick: point updates may only decrease values (new_val <= old_val)
// Max Fenwick: point updates may only increase values (new_val >= old_val)
struct PrefixExtremumBIT {
    int n;
    bool is_min_mode;
    vector<long long> tree;
    const long long INF = 2e18;

    PrefixExtremumBIT(int n, bool is_min = true) : n(n), is_min_mode(is_min) {
        tree.assign(n + 1, is_min_mode ? INF : -INF);
    }

    // Monotonic update: only tightens extremum
    void update(int i, long long val) {
        for (; i <= n; i += i & -i) {
            if (is_min_mode) {
                tree[i] = min(tree[i], val);
            } else {
                tree[i] = max(tree[i], val);
            }
        }
    }

    long long query_prefix(int i) const {
        long long res = is_min_mode ? INF : -INF;
        for (; i > 0; i -= i & -i) {
            if (is_min_mode) {
                res = min(res, tree[i]);
            } else {
                res = max(res, tree[i]);
            }
        }
        return res;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q) || n <= 0) return 0;

    PrefixExtremumBIT bit(n, true); // default prefix min

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int idx;
            long long val;
            cin >> idx >> val;
            bit.update(idx, val);
        } else if (type == 2) {
            int idx;
            cin >> idx;
            cout << bit.query_prefix(idx) << "\\n";
        }
    }

    return 0;
}
"""

    if pattern == "fenwick_2d_point_update_range_query":
        return """#include <iostream>
#include <vector>

using namespace std;

// 2D Fenwick Tree for Grid Sub-rectangle Sums
// Complexity: O(log N * log M) per update and query
struct Fenwick2D {
    int n, m;
    vector<vector<long long>> tree;

    Fenwick2D(int n, int m) : n(n), m(m), tree(n + 1, vector<long long>(m + 1, 0)) {}

    void add(int r, int c, long long delta) {
        for (int i = r; i <= n; i += i & -i) {
            for (int j = c; j <= m; j += j & -j) {
                tree[i][j] += delta;
            }
        }
    }

    // Prefix sum over rectangle [1, 1] to [r, c]
    long long query(int r, int c) const {
        if (r <= 0 || c <= 0) return 0;
        long long sum = 0;
        for (int i = min(r, n); i > 0; i -= i & -i) {
            for (int j = min(c, m); j > 0; j -= j & -j) {
                sum += tree[i][j];
            }
        }
        return sum;
    }

    // Sub-rectangle sum [r1, c1] to [r2, c2] via 2D inclusion-exclusion
    long long range_query(int r1, int c1, int r2, int c2) const {
        if (r1 > r2 || c1 > c2) return 0;
        return query(r2, c2) - query(r1 - 1, c2) - query(r2, c1 - 1) + query(r1 - 1, c1 - 1);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m, q;
    if (!(cin >> n >> m >> q) || n <= 0 || m <= 0) return 0;

    Fenwick2D ft2d(n, m);

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            // Point update: add delta at (r, c)
            int r, c;
            long long delta;
            cin >> r >> c >> delta;
            ft2d.add(r, c, delta);
        } else if (type == 2) {
            // Subgrid query [r1, c1] to [r2, c2]
            int r1, c1, r2, c2;
            cin >> r1 >> c1 >> r2 >> c2;
            cout << ft2d.range_query(r1, c1, r2, c2) << "\\n";
        }
    }

    return 0;
}
"""

    if pattern == "fenwick_kth_element":
        return """#include <iostream>
#include <vector>

using namespace std;

// K-th Element via Binary Lifting on Fenwick Tree
// Precondition: frequency[x] >= 0, 1 <= k <= total_frequency
// Single-pass O(log M) without O(log^2 M) binary search
struct KthElementBIT {
    int max_val;
    vector<long long> tree;

    KthElementBIT(int max_val) : max_val(max_val), tree(max_val + 1, 0) {}

    void add(int val, long long delta) {
        for (; val <= max_val; val += val & -val) {
            tree[val] += delta;
        }
    }

    long long query(int val) const {
        long long s = 0;
        for (; val > 0; val -= val & -val) {
            s += tree[val];
        }
        return s;
    }

    // Binary lifting to find smallest index with prefix_frequency >= k
    int find_kth(long long k) const {
        int idx = 0;
        long long current_sum = 0;
        int max_step = 1;
        while ((max_step << 1) <= max_val) {
            max_step <<= 1;
        }

        for (int step = max_step; step > 0; step >>= 1) {
            if (idx + step <= max_val && current_sum + tree[idx + step] < k) {
                idx += step;
                current_sum += tree[idx];
            }
        }
        return idx + 1;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int m, q;
    if (!(cin >> m >> q) || m <= 0) return 0;

    KthElementBIT bit(m);

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            // Insert element
            int val;
            cin >> val;
            bit.add(val, 1);
        } else if (type == 2) {
            // Erase element
            int val;
            cin >> val;
            bit.add(val, -1);
        } else if (type == 3) {
            // Query k-th smallest element
            long long k;
            cin >> k;
            cout << bit.find_kth(k) << "\\n";
        }
    }

    return 0;
}
"""

    if pattern == "fenwick_inversion_counting":
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Inversion Counting via Fenwick Tree + Coordinate Compression
// Complexity: O(N log N) time, O(N) space
struct FenwickInversion {
    int n;
    vector<int> tree;

    FenwickInversion(int n) : n(n), tree(n + 1, 0) {}

    void add(int i, int delta) {
        for (; i <= n; i += i & -i) {
            tree[i] += delta;
        }
    }

    int query(int i) const {
        int s = 0;
        for (; i > 0; i -= i & -i) {
            s += tree[i];
        }
        return s;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<long long> a(n);
    vector<long long> coords(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
        coords[i] = a[i];
    }

    // Coordinate compression
    sort(coords.begin(), coords.end());
    coords.erase(unique(coords.begin(), coords.end()), coords.end());
    int m = coords.size();

    FenwickInversion ft(m);
    long long total_inversions = 0;

    // Iterate right-to-left: count elements strictly smaller than a[i] seen so far
    for (int i = n - 1; i >= 0; i--) {
        int rank = lower_bound(coords.begin(), coords.end(), a[i]) - coords.begin() + 1;
        total_inversions += ft.query(rank - 1);
        ft.add(rank, 1);
    }

    cout << total_inversions << "\\n";

    return 0;
}
"""

    if pattern == "fenwick_multiset":
        return """#include <iostream>
#include <vector>

using namespace std;

// Order-Statistic Multiset via Fenwick Tree
// Supported operations in O(log M):
// - insert(x)
// - erase(x)
// - count(x)
// - rank(x): 1-based rank of element x
// - select(k): k-th smallest element via binary lifting
struct FenwickMultiset {
    int max_val;
    vector<int> tree;
    int total_size;

    FenwickMultiset(int max_val) : max_val(max_val), tree(max_val + 1, 0), total_size(0) {}

    void insert(int x, int cnt = 1) {
        if (x < 1 || x > max_val) return;
        total_size += cnt;
        for (; x <= max_val; x += x & -x) {
            tree[x] += cnt;
        }
    }

    bool erase(int x, int cnt = 1) {
        if (x < 1 || x > max_val) return false;
        if (count(x) < cnt) return false;
        total_size -= cnt;
        for (; x <= max_val; x += x & -x) {
            tree[x] -= cnt;
        }
        return true;
    }

    int count(int x) const {
        if (x < 1 || x > max_val) return 0;
        return query(x) - query(x - 1);
    }

    int query(int x) const {
        if (x > max_val) x = max_val;
        int s = 0;
        for (; x > 0; x -= x & -x) {
            s += tree[x];
        }
        return s;
    }

    // 1-based rank: number of elements strictly smaller than x + 1
    int rank(int x) const {
        if (x <= 1) return 1;
        return query(x - 1) + 1;
    }

    // Find k-th element (1 <= k <= total_size) via binary lifting
    int select(int k) const {
        if (k < 1 || k > total_size) return -1;
        int idx = 0;
        int current_sum = 0;
        int max_step = 1;
        while ((max_step << 1) <= max_val) max_step <<= 1;

        for (int step = max_step; step > 0; step >>= 1) {
            if (idx + step <= max_val && current_sum + tree[idx + step] < k) {
                idx += step;
                current_sum += tree[idx];
            }
        }
        return idx + 1;
    }

    int size() const {
        return total_size;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int m, q;
    if (!(cin >> m >> q) || m <= 0) return 0;

    FenwickMultiset ms(m);

    while (q--) {
        int type, x;
        cin >> type >> x;
        if (type == 1) {
            ms.insert(x);
        } else if (type == 2) {
            ms.erase(x);
        } else if (type == 3) {
            cout << ms.count(x) << "\\n";
        } else if (type == 4) {
            cout << ms.rank(x) << "\\n";
        } else if (type == 5) {
            cout << ms.select(x) << "\\n";
        }
    }

    return 0;
}
"""

    if pattern == "fenwick_coordinate_compression":
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Coordinate Compression Engine for Fenwick Tree
// Maps arbitrary sparse integer universe to compact range [1..M]
// Complexity: O(K log K + Q log M) time, O(M) Fenwick memory
struct CoordinateCompressor {
    vector<long long> coords;

    void add(long long x) {
        coords.push_back(x);
    }

    void build() {
        sort(coords.begin(), coords.end());
        coords.erase(unique(coords.begin(), coords.end()), coords.end());
    }

    int get_rank(long long x) const {
        return lower_bound(coords.begin(), coords.end(), x) - coords.begin() + 1;
    }

    long long get_val(int rank) const {
        return coords[rank - 1];
    }

    int size() const {
        return coords.size();
    }
};

struct CompressedBIT {
    int m;
    vector<long long> tree;

    CompressedBIT(int m) : m(m), tree(m + 1, 0) {}

    void add(int i, long long delta) {
        for (; i <= m; i += i & -i) {
            tree[i] += delta;
        }
    }

    long long query(int i) const {
        long long s = 0;
        for (; i > 0; i -= i & -i) {
            s += tree[i];
        }
        return s;
    }

    long long range_query(int l, int r) const {
        if (l > r) return 0;
        return query(r) - query(l - 1);
    }
};

struct Query {
    int type;
    long long l, r, val;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int q;
    if (!(cin >> q) || q <= 0) return 0;

    CoordinateCompressor comp;
    vector<Query> queries(q);

    for (int i = 0; i < q; i++) {
        cin >> queries[i].type;
        if (queries[i].type == 1) {
            // Point add (pos, val)
            cin >> queries[i].l >> queries[i].val;
            comp.add(queries[i].l);
        } else if (queries[i].type == 2) {
            // Range sum [l, r]
            cin >> queries[i].l >> queries[i].r;
            comp.add(queries[i].l);
            comp.add(queries[i].r);
        }
    }

    comp.build();
    CompressedBIT bit(comp.size());

    for (const auto& qry : queries) {
        if (qry.type == 1) {
            int rank = comp.get_rank(qry.l);
            bit.add(rank, qry.val);
        } else if (qry.type == 2) {
            int r_l = comp.get_rank(qry.l);
            int r_r = comp.get_rank(qry.r);
            cout << bit.range_query(r_l, r_r) << "\\n";
        }
    }

    return 0;
}
"""

    return """#include <iostream>
using namespace std;
int main() { return 0; }
"""
