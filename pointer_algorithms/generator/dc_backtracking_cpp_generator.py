"""
C++ Code Generator for Divide & Conquer, Backtracking, and Exponential Decomposition (Phase 3M).

Emits clean, robust, modern C++17 implementations for:
1. dc_merge_sort_inversions (Merge Sort & Cross-Boundary Inversion Counting)
2. dc_quickselect (Linear-time Selection by 3-Way Partition)
3. dc_closest_pair (Geometric Divide & Conquer with 2-Delta Strip Packing)
4. dc_tree_centroid (Centroid Decomposition on Trees)
5. dc_cdq_divide_and_conquer (CDQ Offline Multi-Dimensional Divide & Conquer)
6. backtracking_subsets_permutations (Combinatorial Backtracking with Duplicate Pruning)
7. backtracking_constraint_satisfaction (N-Queens with Bitmask Constraint Propagation)
8. backtracking_branch_and_bound (Branch & Bound with Admissible Bound Pruning)
9. backtracking_state_space_search (Grid State-Space Search with In-Place Restoration)
10. backtracking_meet_in_the_middle (Meet-in-the-Middle Bisection for N <= 40)
"""

from typing import Dict, Any

def generate_dc_backtracking_cpp(pattern: str, features: Dict[str, Any]) -> str:
    pat = pattern.lower()

    # ── 1. Merge Sort Inversion Counting (3M-A) ──
    if "merge_sort_inversions" in pat or ("inversion" in pat and "dc" in pat):
        return """#include <iostream>
#include <vector>

using namespace std;

// 3M-A: Divide & Conquer — Merge Sort Inversion Counting
// Invariant: Subarrays A[l..mid] and A[mid+1..r] are recursively sorted and their
// internal inversions counted. Two-pointer merge counts cross-boundary pairs in O(N).
long long merge_and_count(vector<long long>& arr, vector<long long>& temp, int left, int mid, int right) {
    int i = left;
    int j = mid + 1;
    int k = left;
    long long inv_count = 0;

    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) {
            temp[k++] = arr[i++];
        } else {
            // arr[i] > arr[j] implies all elements in arr[i..mid] are > arr[j]
            temp[k++] = arr[j++];
            inv_count += (mid - i + 1);
        }
    }

    while (i <= mid) temp[k++] = arr[i++];
    while (j <= right) temp[k++] = arr[j++];

    for (i = left; i <= right; i++) arr[i] = temp[i];
    return inv_count;
}

long long merge_sort(vector<long long>& arr, vector<long long>& temp, int left, int right) {
    long long inv_count = 0;
    if (left < right) {
        int mid = left + (right - left) / 2;
        inv_count += merge_sort(arr, temp, left, mid);
        inv_count += merge_sort(arr, temp, mid + 1, right);
        inv_count += merge_and_count(arr, temp, left, mid, right);
    }
    return inv_count;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<long long> arr(n);
    for (int i = 0; i < n; i++) cin >> arr[i];

    vector<long long> temp(n);
    long long total_inversions = merge_sort(arr, temp, 0, n - 1);
    cout << total_inversions << "\\n";

    return 0;
}
"""

    # ── 2. Quickselect by 3-Way Partition (3M-B) ──
    elif "quickselect" in pat:
        return """#include <iostream>
#include <vector>
#include <algorithm>
#include <random>

using namespace std;

// 3M-B: Quickselect — Selection by 3-Way Partition
// Invariant: 3-way Dutch National Flag partitioning splits array into (< p, == p, > p).
// Recurses strictly into the single range containing target k, expected O(N) time.
pair<int, int> partition3(vector<long long>& arr, int l, int r, long long pivot) {
    int lt = l;
    int i = l;
    int gt = r;
    while (i <= gt) {
        if (arr[i] < pivot) {
            swap(arr[lt++], arr[i++]);
        } else if (arr[i] > pivot) {
            swap(arr[i], arr[gt--]);
        } else {
            i++;
        }
    }
    return {lt, gt};
}

long long quickselect(vector<long long>& arr, int l, int r, int k, mt19937& rng) {
    if (l == r) return arr[l];

    uniform_int_distribution<int> dist(l, r);
    int p_idx = dist(rng);
    long long pivot = arr[p_idx];

    auto [lt, gt] = partition3(arr, l, r, pivot);

    if (k < lt) {
        return quickselect(arr, l, lt - 1, k, rng);
    } else if (k > gt) {
        return quickselect(arr, gt + 1, r, k, rng);
    } else {
        return arr[k];
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, k;
    if (!(cin >> n >> k) || n <= 0) return 0;

    vector<long long> arr(n);
    for (int i = 0; i < n; i++) cin >> arr[i];

    // 0-based k-th smallest index
    k = max(0, min(n - 1, k));

    mt19937 rng(1337);
    long long ans = quickselect(arr, 0, n - 1, k, rng);
    cout << ans << "\\n";

    return 0;
}
"""

    # ── 3. Closest Pair of Points in 2D (3M-C) ──
    elif "closest_pair" in pat:
        return """#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <iomanip>

using namespace std;

// 3M-C: Closest Pair of 2D Points — Geometric Divide & Conquer
// Invariant: Minimum distance delta = min(delta_L, delta_R).
// Cross-boundary strip of width 2*delta requires at most 7-8 successor comparisons in y-sorted order.
struct Point {
    long long x, y;
};

long long dist_sq(const Point& p1, const Point& p2) {
    long long dx = p1.x - p2.x;
    long long dy = p1.y - p2.y;
    return dx * dx + dy * dy;
}

long long closest_pair_rec(vector<Point>& pts_x, vector<Point>& pts_y, int l, int r) {
    if (r - l <= 3) {
        long long min_d = 4e18;
        for (int i = l; i <= r; i++) {
            for (int j = i + 1; j <= r; j++) {
                min_d = min(min_d, dist_sq(pts_x[i], pts_x[j]));
            }
        }
        sort(pts_x.begin() + l, pts_x.begin() + r + 1, [](const Point& a, const Point& b) {
            return a.y < b.y;
        });
        return min_d;
    }

    int mid = l + (r - l) / 2;
    long long mid_x = pts_x[mid].x;

    long long d_left = closest_pair_rec(pts_x, pts_y, l, mid);
    long long d_right = closest_pair_rec(pts_x, pts_y, mid + 1, r);
    long long d = min(d_left, d_right);

    // Merge y-sorted halves
    vector<Point> merged(r - l + 1);
    merge(pts_x.begin() + l, pts_x.begin() + mid + 1,
          pts_x.begin() + mid + 1, pts_x.begin() + r + 1,
          merged.begin(), [](const Point& a, const Point& b) {
              return a.y < b.y;
          });
    copy(merged.begin(), merged.end(), pts_x.begin() + l);

    // Filter strip
    vector<Point> strip;
    for (int i = l; i <= r; i++) {
        long long dx = pts_x[i].x - mid_x;
        if (dx * dx < d) {
            strip.push_back(pts_x[i]);
        }
    }

    // Check at most 7 successors per point in y-order
    for (size_t i = 0; i < strip.size(); i++) {
        for (size_t j = i + 1; j < strip.size() && (strip[j].y - strip[i].y) * (strip[j].y - strip[i].y) < d; j++) {
            d = min(d, dist_sq(strip[i], strip[j]));
        }
    }

    return d;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n < 2) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<Point> pts(n);
    for (int i = 0; i < n; i++) cin >> pts[i].x >> pts[i].y;

    sort(pts.begin(), pts.end(), [](const Point& a, const Point& b) {
        if (a.x != b.x) return a.x < b.x;
        return a.y < b.y;
    });

    vector<Point> pts_y = pts;
    long long min_dist_sq = closest_pair_rec(pts, pts_y, 0, n - 1);
    cout << fixed << setprecision(6) << sqrt((double)min_dist_sq) << "\\n";

    return 0;
}
"""

    # ── 4. Centroid Decomposition (3M-D) ──
    elif "tree_centroid" in pat:
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// 3M-D: Tree Centroid Decomposition
// Invariant: Tree centroid C partitions tree into subtrees of size <= N/2.
// Recursion depth is bounded by log2(N); all paths are classified by which centroid they cross.
struct Edge {
    int to;
    long long weight;
};

int n;
long long k_target;
vector<vector<Edge>> adj;
vector<int> sz;
vector<bool> visited;
long long total_paths = 0;

int get_sizes(int u, int p) {
    sz[u] = 1;
    for (const auto& e : adj[u]) {
        if (e.to != p && !visited[e.to]) {
            sz[u] += get_sizes(e.to, u);
        }
    }
    return sz[u];
}

int find_centroid(int u, int p, int total) {
    for (const auto& e : adj[u]) {
        if (e.to != p && !visited[e.to] && sz[e.to] > total / 2) {
            return find_centroid(e.to, u, total);
        }
    }
    return u;
}

void get_dists(int u, int p, long long d, vector<long long>& dists) {
    dists.push_back(d);
    for (const auto& e : adj[u]) {
        if (e.to != p && !visited[e.to]) {
            get_dists(e.to, u, d + e.weight, dists);
        }
    }
}

long long count_pairs(vector<long long>& dists, long long target) {
    sort(dists.begin(), dists.end());
    long long count = 0;
    int l = 0, r = (int)dists.size() - 1;
    while (l < r) {
        if (dists[l] + dists[r] <= target) {
            count += (r - l);
            l++;
        } else {
            r--;
        }
    }
    return count;
}

void decompose(int u) {
    int total = get_sizes(u, 0);
    int c = find_centroid(u, 0, total);
    visited[c] = true;

    vector<long long> all_dists = {0};
    for (const auto& e : adj[c]) {
        if (!visited[e.to]) {
            vector<long long> sub_dists;
            get_dists(e.to, c, e.weight, sub_dists);
            total_paths -= count_pairs(sub_dists, k_target);
            all_dists.insert(all_dists.end(), sub_dists.begin(), sub_dists.end());
        }
    }
    total_paths += count_pairs(all_dists, k_target);

    for (const auto& e : adj[c]) {
        if (!visited[e.to]) {
            decompose(e.to);
        }
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    if (!(cin >> n >> k_target) || n <= 0) return 0;

    adj.assign(n + 1, {});
    sz.assign(n + 1, 0);
    visited.assign(n + 1, false);

    for (int i = 0; i < n - 1; i++) {
        int u, v;
        long long w = 1;
        cin >> u >> v;
        // if weighted, read w
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }

    decompose(1);
    cout << total_paths << "\\n";

    return 0;
}
"""

    # ── 5. CDQ Offline Divide & Conquer (3M-E) ──
    elif "cdq" in pat:
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// 3M-E: CDQ Divide & Conquer for 3D Partial Order
// Invariant: Subproblems [l..mid] and [mid+1..r] are recursively solved and sorted by dimension 2.
// Two-pointer sweep applies left modifications to Fenwick tree and answers right queries.
struct Element {
    int a, b, c;
    int id;
    int cnt;
    int ans;
};

struct Fenwick {
    int n;
    vector<int> tree;
    Fenwick(int n) : n(n), tree(n + 1, 0) {}
    void add(int i, int delta) {
        for (; i <= n; i += i & -i) tree[i] += delta;
    }
    int query(int i) {
        int sum = 0;
        for (; i > 0; i -= i & -i) sum += tree[i];
        return sum;
    }
};

void cdq_solve(vector<Element>& elems, int l, int r, Fenwick& bit) {
    if (l >= r) return;
    int mid = l + (r - l) / 2;

    cdq_solve(elems, l, mid, bit);
    cdq_solve(elems, mid + 1, r, bit);

    // Sort halves by second dimension b
    sort(elems.begin() + l, elems.begin() + mid + 1, [](const Element& x, const Element& y) {
        if (x.b != y.b) return x.b < y.b;
        return x.c < y.c;
    });
    sort(elems.begin() + mid + 1, elems.begin() + r + 1, [](const Element& x, const Element& y) {
        if (x.b != y.b) return x.b < y.b;
        return x.c < y.c;
    });

    int i = l;
    for (int j = mid + 1; j <= r; j++) {
        while (i <= mid && elems[i].b <= elems[j].b) {
            bit.add(elems[i].c, elems[i].cnt);
            i++;
        }
        elems[j].ans += bit.query(elems[j].c);
    }

    // Rollback Fenwick modifications
    for (int k = l; k < i; k++) {
        bit.add(elems[k].c, -elems[k].cnt);
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, max_c = 100000;
    if (!(cin >> n) || n <= 0) return 0;

    vector<Element> raw_elems(n);
    for (int i = 0; i < n; i++) {
        cin >> raw_elems[i].a >> raw_elems[i].b >> raw_elems[i].c;
        raw_elems[i].id = i;
        raw_elems[i].cnt = 1;
        raw_elems[i].ans = 0;
        max_c = max(max_c, raw_elems[i].c);
    }

    // Sort by primary dimension a, then b, then c
    sort(raw_elems.begin(), raw_elems.end(), [](const Element& x, const Element& y) {
        if (x.a != y.a) return x.a < y.a;
        if (x.b != y.b) return x.b < y.b;
        return x.c < y.c;
    });

    // Compact identical elements
    vector<Element> elems;
    vector<int> raw_to_unique(n);
    for (int i = 0; i < n; i++) {
        if (!elems.empty() && elems.back().a == raw_elems[i].a && elems.back().b == raw_elems[i].b && elems.back().c == raw_elems[i].c) {
            elems.back().cnt++;
            raw_to_unique[i] = (int)elems.size() - 1;
        } else {
            elems.push_back(raw_elems[i]);
            elems.back().cnt = 1;
            raw_to_unique[i] = (int)elems.size() - 1;
        }
    }

    Fenwick bit(max_c + 5);
    cdq_solve(elems, 0, (int)elems.size() - 1, bit);

    for (auto& e : elems) {
        e.ans += (e.cnt - 1);
    }

    // Output answers in original order
    vector<int> res(n);
    for (int i = 0; i < n; i++) {
        res[raw_elems[i].id] = elems[raw_to_unique[i]].ans;
    }
    for (int i = 0; i < n; i++) cout << res[i] << "\\n";

    return 0;
}
"""

    # ── 6. Combinatorial Backtracking (Subsets & Permutations) (3M-F) ──
    elif "subsets_permutations" in pat:
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// 3M-F: Combinatorial Backtracking with Duplicate Pruning
// Invariant: Sorting adjacent duplicates guarantees identical siblings are skipped
// when the preceding sibling was not selected.
void generate_subsets(int start, const vector<int>& nums, vector<int>& path, vector<vector<int>>& result) {
    result.push_back(path);

    for (int i = start; i < (int)nums.size(); i++) {
        // Skip duplicates at same recursion level
        if (i > start && nums[i] == nums[i - 1]) continue;

        path.push_back(nums[i]);
        generate_subsets(i + 1, nums, path, result);
        path.pop_back(); // State restoration
    }
}

void generate_permutations(const vector<int>& nums, vector<bool>& visited, vector<int>& path, vector<vector<int>>& result) {
    if (path.size() == nums.size()) {
        result.push_back(path);
        return;
    }

    for (int i = 0; i < (int)nums.size(); i++) {
        if (visited[i]) continue;
        // Duplicate pruning: only use duplicate element if predecessor was used
        if (i > 0 && nums[i] == nums[i - 1] && !visited[i - 1]) continue;

        visited[i] = true;
        path.push_back(nums[i]);
        generate_permutations(nums, visited, path, result);
        path.pop_back(); // State restoration
        visited[i] = false;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];

    sort(nums.begin(), nums.end());

    vector<vector<int>> subsets;
    vector<int> path;
    generate_subsets(0, nums, path, subsets);

    cout << "Total Subsets: " << subsets.size() << "\\n";
    for (const auto& s : subsets) {
        cout << "[";
        for (size_t i = 0; i < s.size(); i++) {
            cout << s[i] << (i + 1 < s.size() ? ", " : "");
        }
        cout << "]\\n";
    }

    return 0;
}
"""

    # ── 7. Constraint Satisfaction (N-Queens with Bitmasks) (3M-G) ──
    elif "constraint_satisfaction" in pat or "csp" in pat:
        return """#include <iostream>
#include <vector>

using namespace std;

// 3M-G: Constraint Satisfaction — N-Queens with Bitmask Propagation
// Invariant: Bitmasks cols, diag1, diag2 maintain availability of unoccupied lanes.
// Available positions computed in O(1) via bitwise AND with domain mask.
int n;
int solutions_count = 0;

void solve_nqueens(int row, int cols, int diag1, int diag2, int mask) {
    if (row == n) {
        solutions_count++;
        return;
    }

    // Available positions in current row
    int available = mask & ~(cols | diag1 | diag2);

    while (available) {
        int p = available & -available; // Extract lowest set bit
        available -= p;

        solve_nqueens(
            row + 1,
            cols | p,
            (diag1 | p) << 1,
            (diag2 | p) >> 1,
            mask
        );
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    if (!(cin >> n) || n <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    int mask = (1 << n) - 1;
    solve_nqueens(0, 0, 0, 0, mask);

    cout << solutions_count << "\\n";
    return 0;
}
"""

    # ── 8. Branch & Bound (3M-H) ──
    elif "branch_and_bound" in pat:
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// 3M-H: Branch & Bound — 0/1 Knapsack with Fractional Relaxation Bounding
// Invariant: Fractional knapsack relaxation provides an admissible upper bound on the
// maximum achievable value in the current subtree; prune if bound <= best_value.
struct Item {
    long long value, weight;
    double density() const { return (double)value / weight; }
};

int n;
long long capacity;
vector<Item> items;
long long max_value = 0;

double bound(int idx, long long cur_weight, long long cur_value) {
    if (cur_weight >= capacity) return 0;
    double b = (double)cur_value;
    long long rem_w = capacity - cur_weight;

    for (int i = idx; i < n; i++) {
        if (items[i].weight <= rem_w) {
            rem_w -= items[i].weight;
            b += items[i].value;
        } else {
            b += (double)items[i].value * ((double)rem_w / items[i].weight);
            break;
        }
    }
    return b;
}

void branch_and_bound(int idx, long long cur_weight, long long cur_value) {
    if (cur_weight <= capacity && cur_value > max_value) {
        max_value = cur_value;
    }

    if (idx == n || cur_weight >= capacity) return;

    // Prune subtree if optimistic bound cannot exceed currently recorded best
    if (bound(idx, cur_weight, cur_value) <= (double)max_value) return;

    // Branch 1: Include item idx (if feasible)
    if (cur_weight + items[idx].weight <= capacity) {
        branch_and_bound(idx + 1, cur_weight + items[idx].weight, cur_value + items[idx].value);
    }

    // Branch 2: Exclude item idx
    branch_and_bound(idx + 1, cur_weight, cur_value);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    if (!(cin >> n >> capacity) || n <= 0 || capacity <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    items.resize(n);
    for (int i = 0; i < n; i++) cin >> items[i].weight >> items[i].value;

    // Sort descending by value density
    sort(items.begin(), items.end(), [](const Item& a, const Item& b) {
        return a.density() > b.density();
    });

    branch_and_bound(0, 0, 0);
    cout << max_value << "\\n";

    return 0;
}
"""

    # ── 9. State-Space Search (Word Search in 2D Grid) (3M-I) ──
    elif "state_space_search" in pat:
        return """#include <iostream>
#include <vector>
#include <string>

using namespace std;

// 3M-I: State-Space Search — 2D Grid Word Search with In-Place Restoration
// Invariant: In-place marking board[r][c] = '#' prevents revisiting cells in the current path.
// Exact character restoration upon return ensures full state integrity.
int R, C;
vector<string> board;
string word;

const int dr[] = {-1, 1, 0, 0};
const int dc[] = {0, 0, -1, 1};

bool dfs_search(int r, int c, int idx) {
    if (idx == (int)word.size()) return true;
    if (r < 0 || r >= R || c < 0 || c >= C || board[r][c] != word[idx]) return false;

    char temp = board[r][c];
    board[r][c] = '#'; // In-place visited mark

    for (int d = 0; d < 4; d++) {
        if (dfs_search(r + dr[d], c + dc[d], idx + 1)) {
            board[r][c] = temp; // Restore before returning true
            return true;
        }
    }

    board[r][c] = temp; // State restoration
    return false;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    if (!(cin >> R >> C) || R <= 0 || C <= 0) {
        cout << "false\\n";
        return 0;
    }

    board.assign(R, string(C, ' '));
    for (int i = 0; i < R; i++) {
        for (int j = 0; j < C; j++) {
            cin >> board[i][j];
        }
    }
    cin >> word;

    bool found = false;
    for (int i = 0; i < R && !found; i++) {
        for (int j = 0; j < C && !found; j++) {
            if (board[i][j] == word[0] && dfs_search(i, j, 0)) {
                found = true;
            }
        }
    }

    cout << (found ? "true" : "false") << "\\n";
    return 0;
}
"""

    # ── 10. Meet in the Middle (3M-J) ──
    elif "meet_in_the_middle" in pat or "meet_in_middle" in pat:
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// 3M-J: Meet in the Middle — Bisection for N <= 40
// Invariant: Bisection of N into halves of size N/2 generates two sets of size 2^(N/2).
// Sorting left half enables O(N) binary search per right half sum, achieving O(N * 2^(N/2)).
void generate_sums(int idx, int end, const vector<long long>& nums, long long current, vector<long long>& sums) {
    if (idx == end) {
        sums.push_back(current);
        return;
    }
    // Exclude nums[idx]
    generate_sums(idx + 1, end, nums, current, sums);
    // Include nums[idx]
    generate_sums(idx + 1, end, nums, current + nums[idx], sums);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    long long target;
    if (!(cin >> n >> target) || n <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<long long> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];

    int mid = n / 2;
    vector<long long> left_sums, right_sums;

    generate_sums(0, mid, nums, 0, left_sums);
    generate_sums(mid, n, nums, 0, right_sums);

    sort(left_sums.begin(), left_sums.end());

    long long count_exact = 0;
    for (long long s : right_sums) {
        long long need = target - s;
        auto range = equal_range(left_sums.begin(), left_sums.end(), need);
        count_exact += distance(range.first, range.second);
    }

    cout << count_exact << "\\n";
    return 0;
}
"""

    # Fallback
    return """#include <iostream>
using namespace std;
int main() { return 0; }
"""
