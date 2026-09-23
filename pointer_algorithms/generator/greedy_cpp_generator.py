"""
C++ Code Generator for Greedy Algorithms (Phase 3L).

Emits clean, robust, modern C++17 implementations for:
1. greedy_interval_selection (Activity Selection / Max Non-overlapping Intervals)
2. greedy_interval_covering (Interval Stabbing / Min Points / Arrows)
3. greedy_fractional_knapsack (Divisible Resource Allocation by Value Density)
4. greedy_deadline_scheduling (Minimize Max Lateness via EDD / Smith's Rule)
5. greedy_heap_assisted (Min Refueling Stops / Event Horizon Priority Queue)
6. greedy_huffman_merge (Optimal Merge Pattern / Huffman Coding)
7. greedy_sequence_local_choice (Remove K Digits / Monotonic Stack Greedy)
8. greedy_reachability_partition (Jump Game Reachability / Minimum Jumps)
9. greedy_graph_mst (Kruskal's MST via DSU with Cut Property)
10. greedy_general_exchange (Custom Comparator / Pairwise Exchange Sort)
"""

from typing import Dict, Any

def generate_greedy_cpp(pattern: str, features: Dict[str, Any]) -> str:
    pat = pattern.lower()

    # ── 1. Interval Selection / Activity Scheduling (3L-A) ──
    if "interval_selection" in pat:
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Greedy Interval Selection / Activity Scheduling
// Invariant: Selecting the compatible interval that finishes earliest
// leaves the maximum remaining capacity for subsequent choices.
struct Interval {
    long long start, finish;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<Interval> intervals(n);
    for (int i = 0; i < n; i++) {
        cin >> intervals[i].start >> intervals[i].finish;
    }

    // Sort ascending by finish time
    sort(intervals.begin(), intervals.end(), [](const Interval& a, const Interval& b) {
        if (a.finish != b.finish) return a.finish < b.finish;
        return a.start < b.start;
    });

    int count = 0;
    long long last_finish = -2e18; // -infinity

    for (const auto& iv : intervals) {
        if (iv.start >= last_finish) {
            count++;
            last_finish = iv.finish;
        }
    }

    cout << count << "\\n";
    return 0;
}
"""

    # ── 2. Interval Covering / Minimum Point Selection (3L-B) ──
    elif "interval_covering" in pat:
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Greedy Interval Covering / Stabbing
// Invariant: Placing a point at the rightmost endpoint of the first uncovered interval
// maximizes its overlap with all subsequent intervals.
struct Interval {
    long long start, end;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<Interval> intervals(n);
    for (int i = 0; i < n; i++) {
        cin >> intervals[i].start >> intervals[i].end;
    }

    // Sort ascending by end point
    sort(intervals.begin(), intervals.end(), [](const Interval& a, const Interval& b) {
        if (a.end != b.end) return a.end < b.end;
        return a.start < b.start;
    });

    int points = 0;
    long long last_point = -2e18; // -infinity

    for (const auto& iv : intervals) {
        if (iv.start > last_point) {
            points++;
            last_point = iv.end;
        }
    }

    cout << points << "\\n";
    return 0;
}
"""

    # ── 3. Fractional Knapsack / Divisible Resource Allocation (3L-C) ──
    elif "fractional_knapsack" in pat:
        return """#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>

using namespace std;

// Greedy Fractional Knapsack
// Invariant: Taking the highest value-to-weight density items first
// guarantees maximum total value across capacity W.
struct Item {
    double value, weight;
    double density() const { return value / weight; }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    double W;
    if (!(cin >> n >> W) || n <= 0 || W <= 0) {
        cout << fixed << setprecision(2) << 0.0 << "\\n";
        return 0;
    }

    vector<Item> items(n);
    for (int i = 0; i < n; i++) {
        cin >> items[i].value >> items[i].weight;
    }

    // Sort descending by value density
    sort(items.begin(), items.end(), [](const Item& a, const Item& b) {
        return a.density() > b.density();
    });

    double total_value = 0.0;
    double rem_capacity = W;

    for (const auto& item : items) {
        if (rem_capacity <= 0) break;
        if (item.weight <= rem_capacity) {
            total_value += item.value;
            rem_capacity -= item.weight;
        } else {
            total_value += item.value * (rem_capacity / item.weight);
            rem_capacity = 0;
            break;
        }
    }

    cout << fixed << setprecision(2) << total_value << "\\n";
    return 0;
}
"""

    # ── 4. Deadline / Scheduling Greedy (3L-D) ──
    elif "deadline_scheduling" in pat:
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Greedy Deadline Scheduling: Minimize Maximum Lateness (Earliest Due Date)
// Invariant: An inverted pair of adjacent jobs (d_i > d_j) can be swapped
// without increasing the maximum lateness of the schedule.
struct Job {
    long long duration, deadline;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<Job> jobs(n);
    for (int i = 0; i < n; i++) {
        cin >> jobs[i].duration >> jobs[i].deadline;
    }

    // Sort ascending by deadline (EDD rule)
    sort(jobs.begin(), jobs.end(), [](const Job& a, const Job& b) {
        if (a.deadline != b.deadline) return a.deadline < b.deadline;
        return a.duration < b.duration;
    });

    long long current_time = 0;
    long long max_lateness = 0;

    for (const auto& j : jobs) {
        current_time += j.duration;
        long long lateness = max(0LL, current_time - j.deadline);
        max_lateness = max(max_lateness, lateness);
    }

    cout << max_lateness << "\\n";
    return 0;
}
"""

    # ── 5. Heap-Assisted Greedy (3L-E) ──
    elif "heap_assisted" in pat:
        return """#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

// Heap-Assisted Greedy: Minimum Refueling Stops
// Invariant: When current fuel is insufficient to reach the next position,
// retrospectively activating the maximum fuel station from the passed pool
// maximizes the forward reach.
struct Station {
    long long pos, fuel;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    long long target, start_fuel;
    int n;
    if (!(cin >> target >> start_fuel >> n)) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<Station> stations(n);
    for (int i = 0; i < n; i++) {
        cin >> stations[i].pos >> stations[i].fuel;
    }

    sort(stations.begin(), stations.end(), [](const Station& a, const Station& b) {
        return a.pos < b.pos;
    });

    priority_queue<long long> max_heap;
    long long cur_fuel = start_fuel;
    int stops = 0;
    int idx = 0;

    while (cur_fuel < target) {
        while (idx < n && stations[idx].pos <= cur_fuel) {
            max_heap.push(stations[idx].fuel);
            idx++;
        }
        if (max_heap.empty()) {
            cout << -1 << "\\n";
            return 0;
        }
        cur_fuel += max_heap.top();
        max_heap.pop();
        stops++;
    }

    cout << stops << "\\n";
    return 0;
}
"""

    # ── 6. Huffman / Optimal Merge Pattern (3L-F) ──
    elif "huffman_merge" in pat:
        return """#include <iostream>
#include <vector>
#include <queue>

using namespace std;

// Greedy Huffman / Optimal Merge Pattern
// Invariant: The two components with lowest weights must be merged first
// and appear as siblings at maximum depth in the optimal tree.
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 1) {
        cout << 0 << "\\n";
        return 0;
    }

    priority_queue<long long, vector<long long>, greater<long long>> min_heap;
    for (int i = 0; i < n; i++) {
        long long f;
        cin >> f;
        min_heap.push(f);
    }

    long long total_cost = 0;
    while (min_heap.size() > 1) {
        long long a = min_heap.top(); min_heap.pop();
        long long b = min_heap.top(); min_heap.pop();
        long long merged = a + b;
        total_cost += merged;
        min_heap.push(merged);
    }

    cout << total_cost << "\\n";
    return 0;
}
"""

    # ── 7. Sequence / String Local-Choice Greedy (3L-G) ──
    elif "sequence_local_choice" in pat:
        return """#include <iostream>
#include <string>
#include <vector>

using namespace std;

// Greedy Sequence Local-Choice: Remove K Digits (Reusing Monotonic Stack 3B)
// Invariant: Dropping a digit when it is strictly greater than its successor
// minimizes the most significant decimal place, dominating all later removals.
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string num;
    int k;
    if (!(cin >> num >> k)) {
        cout << "0\\n";
        return 0;
    }

    string stack = "";
    for (char digit : num) {
        while (!stack.empty() && stack.back() > digit && k > 0) {
            stack.pop_back();
            k--;
        }
        stack.push_back(digit);
    }

    // If removals remain, trim from the right
    while (k > 0 && !stack.empty()) {
        stack.pop_back();
        k--;
    }

    // Strip leading zeroes
    int start = 0;
    while (start < (int)stack.size() && stack[start] == '0') {
        start++;
    }

    string result = stack.substr(start);
    if (result.empty()) result = "0";

    cout << result << "\\n";
    return 0;
}
"""

    # ── 8. Reachability / Coverage / Partition Greedy (3L-H) ──
    elif "reachability_partition" in pat:
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Greedy Reachability / Partition: Minimum Jumps (Jump Game II)
// Invariant: The greedy frontier (max_reach) stays ahead of any alternative
// jump sequence of the same length.
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 1) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    int jumps = 0;
    int current_jump_end = 0;
    int farthest_reach = 0;

    for (int i = 0; i < n - 1; i++) {
        farthest_reach = max(farthest_reach, i + a[i]);
        if (i == current_jump_end) {
            jumps++;
            current_jump_end = farthest_reach;
            if (current_jump_end >= n - 1) break;
        }
    }

    cout << jumps << "\\n";
    return 0;
}
"""

    # ── 9. Graph-Greedy Integration: Kruskal's MST (3L-I) ──
    elif "graph_mst" in pat:
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Graph-Greedy Integration: Kruskal's Minimum Spanning Tree
// Reuses Disjoint Set Union (Phase 3H) with path compression and rank.
// Invariant: The lightest edge crossing any cut is safe for MST (Cut Property).
struct Edge {
    int u, v;
    long long weight;
};

struct DSU {
    vector<int> parent, rank;
    DSU(int n) : parent(n + 1), rank(n + 1, 0) {
        for (int i = 0; i <= n; i++) parent[i] = i;
    }
    int find(int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent[i]);
    }
    bool unite(int i, int j) {
        int root_i = find(i), root_j = find(j);
        if (root_i == root_j) return false;
        if (rank[root_i] < rank[root_j]) swap(root_i, root_j);
        parent[root_j] = root_i;
        if (rank[root_i] == rank[root_j]) rank[root_i]++;
        return true;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 1) {
        cout << 0 << "\\n";
        return 0;
    }

    vector<Edge> edges(m);
    for (int i = 0; i < m; i++) {
        cin >> edges[i].u >> edges[i].v >> edges[i].weight;
    }

    // Sort edges ascending by weight
    sort(edges.begin(), edges.end(), [](const Edge& a, const Edge& b) {
        return a.weight < b.weight;
    });

    DSU dsu(n);
    long long mst_weight = 0;
    int edges_count = 0;

    for (const auto& e : edges) {
        if (dsu.unite(e.u, e.v)) {
            mst_weight += e.weight;
            edges_count++;
            if (edges_count == n - 1) break;
        }
    }

    cout << mst_weight << "\\n";
    return 0;
}
"""

    # ── 10. General Exchange / Dominance Greedy (3L-J) ──
    else:
        return """#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

// General Exchange / Dominance Greedy: Largest Number Composition
// Invariant: For any two elements A and B, if A + B > B + A, then placing A
// before B is strictly optimal under pairwise exchange.
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) {
        cout << "\\n";
        return 0;
    }

    vector<string> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }

    // Sort with custom pairwise exchange comparator
    sort(nums.begin(), nums.end(), [](const string& a, const string& b) {
        return a + b > b + a;
    });

    if (nums[0] == "0") {
        cout << "0\\n";
        return 0;
    }

    string result = "";
    for (const auto& s : nums) {
        result += s;
    }

    cout << result << "\\n";
    return 0;
}
"""
