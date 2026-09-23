"""
C++17 Code Generator for Heap / Priority Queue Domain (Phase 3G).

Generates production-grade C++17 implementations for:
1. heap_min_priority_queue
2. heap_max_priority_queue
3. heap_build
4. heap_top_k
5. heap_kth_element
6. heap_k_way_merge
7. heap_two_heaps
8. heap_dynamic_median
9. heap_scheduling
10. heap_greedy_selection
11. heap_lazy_deletion
"""

from typing import Dict, Any


def generate_heap_cpp(pattern: str, params: Dict[str, Any]) -> str:
    if pattern == "heap_min_priority_queue":
        return """#include <iostream>
#include <vector>
#include <queue>
#include <string>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    priority_queue<long long, vector<long long>, greater<long long>> pq;

    for (int i = 0; i < n; i++) {
        string op;
        cin >> op;
        if (op == "PUSH" || op == "push" || op == "insert") {
            long long val;
            cin >> val;
            pq.push(val);
        } else if (op == "POP" || op == "pop" || op == "extract") {
            if (!pq.empty()) {
                cout << pq.top() << "\\n";
                pq.pop();
            } else {
                cout << "EMPTY\\n";
            }
        } else if (op == "TOP" || op == "top" || op == "peek") {
            if (!pq.empty()) {
                cout << pq.top() << "\\n";
            } else {
                cout << "EMPTY\\n";
            }
        } else {
            try {
                long long val = stoll(op);
                pq.push(val);
            } catch (...) {}
        }
    }

    return 0;
}
"""

    if pattern == "heap_max_priority_queue":
        return """#include <iostream>
#include <vector>
#include <queue>
#include <string>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    priority_queue<long long> pq;

    for (int i = 0; i < n; i++) {
        string op;
        cin >> op;
        if (op == "PUSH" || op == "push" || op == "insert") {
            long long val;
            cin >> val;
            pq.push(val);
        } else if (op == "POP" || op == "pop" || op == "extract") {
            if (!pq.empty()) {
                cout << pq.top() << "\\n";
                pq.pop();
            } else {
                cout << "EMPTY\\n";
            }
        } else if (op == "TOP" || op == "top" || op == "peek") {
            if (!pq.empty()) {
                cout << pq.top() << "\\n";
            } else {
                cout << "EMPTY\\n";
            }
        } else {
            try {
                long long val = stoll(op);
                pq.push(val);
            } catch (...) {}
        }
    }

    return 0;
}
"""

    if pattern == "heap_build":
        return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    vector<long long> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    // Linear time O(N) bottom-up heap construction (default min-heap)
    make_heap(arr.begin(), arr.end(), greater<long long>());

    for (int i = 0; i < n; i++) {
        cout << arr[i] << (i == n - 1 ? "" : " ");
    }
    cout << "\\n";

    return 0;
}
"""

    if pattern == "heap_top_k":
        is_smallest = params.get("heap_k_direction") == "smallest" or params.get("heap_kind") == "max_heap"
        if is_smallest:
            return """#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, k;
    if (!(cin >> n >> k) || n <= 0 || k <= 0) return 0;

    // Retention Invariant: To find K smallest elements, maintain a MAX-HEAP of size K.
    // The max-heap root exposes the weakest element in O(1) for eviction.
    priority_queue<long long> max_heap;

    for (int i = 0; i < n; i++) {
        long long val;
        cin >> val;
        if ((int)max_heap.size() < k) {
            max_heap.push(val);
        } else if (val < max_heap.top()) {
            max_heap.pop();
            max_heap.push(val);
        }
    }

    vector<long long> result;
    while (!max_heap.empty()) {
        result.push_back(max_heap.top());
        max_heap.pop();
    }
    sort(result.begin(), result.end());

    for (size_t i = 0; i < result.size(); i++) {
        cout << result[i] << (i + 1 == result.size() ? "" : " ");
    }
    cout << "\\n";

    return 0;
}
"""
        return """#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, k;
    if (!(cin >> n >> k) || n <= 0 || k <= 0) return 0;

    // Retention Invariant: To find K largest elements, maintain a MIN-HEAP of size K.
    // The min-heap root exposes the weakest element in O(1) for eviction.
    priority_queue<long long, vector<long long>, greater<long long>> min_heap;

    for (int i = 0; i < n; i++) {
        long long val;
        cin >> val;
        if ((int)min_heap.size() < k) {
            min_heap.push(val);
        } else if (val > min_heap.top()) {
            min_heap.pop();
            min_heap.push(val);
        }
    }

    vector<long long> result;
    while (!min_heap.empty()) {
        result.push_back(min_heap.top());
        min_heap.pop();
    }
    sort(result.rbegin(), result.rend());

    for (size_t i = 0; i < result.size(); i++) {
        cout << result[i] << (i + 1 == result.size() ? "" : " ");
    }
    cout << "\\n";

    return 0;
}
"""

    if pattern == "heap_kth_element":
        is_smallest = params.get("heap_k_direction") == "smallest" or params.get("heap_kind") == "max_heap"
        if is_smallest:
            return """#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, k;
    if (!(cin >> n >> k) || n <= 0 || k <= 0) return 0;

    // To find K-th smallest: max-heap of size K. Root is the K-th smallest.
    priority_queue<long long> max_heap;

    for (int i = 0; i < n; i++) {
        long long val;
        cin >> val;
        if ((int)max_heap.size() < k) {
            max_heap.push(val);
        } else if (val < max_heap.top()) {
            max_heap.pop();
            max_heap.push(val);
        }
    }

    if (!max_heap.empty()) {
        cout << max_heap.top() << "\\n";
    }

    return 0;
}
"""
        return """#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, k;
    if (!(cin >> n >> k) || n <= 0 || k <= 0) return 0;

    // To find K-th largest: min-heap of size K. Root is the K-th largest.
    priority_queue<long long, vector<long long>, greater<long long>> min_heap;

    for (int i = 0; i < n; i++) {
        long long val;
        cin >> val;
        if ((int)min_heap.size() < k) {
            min_heap.push(val);
        } else if (val > min_heap.top()) {
            min_heap.pop();
            min_heap.push(val);
        }
    }

    if (!min_heap.empty()) {
        cout << min_heap.top() << "\\n";
    }

    return 0;
}
"""

    if pattern == "heap_k_way_merge":
        return """#include <iostream>
#include <vector>
#include <queue>
#include <tuple>

using namespace std;

using StreamElement = tuple<long long, int, int>;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int k;
    if (!(cin >> k) || k <= 0) return 0;

    vector<vector<long long>> streams(k);
    for (int i = 0; i < k; i++) {
        int sz;
        if (cin >> sz && sz > 0) {
            streams[i].resize(sz);
            for (int j = 0; j < sz; j++) {
                cin >> streams[i][j];
            }
        }
    }

    priority_queue<StreamElement, vector<StreamElement>, greater<StreamElement>> pq;

    for (int i = 0; i < k; i++) {
        if (!streams[i].empty()) {
            pq.push(make_tuple(streams[i][0], i, 0));
        }
    }

    bool first = true;
    while (!pq.empty()) {
        auto [val, stream_idx, elem_idx] = pq.top();
        pq.pop();

        if (!first) cout << " ";
        cout << val;
        first = false;

        if (elem_idx + 1 < (int)streams[stream_idx].size()) {
            pq.push(make_tuple(streams[stream_idx][elem_idx + 1], stream_idx, elem_idx + 1));
        }
    }
    cout << "\\n";

    return 0;
}
"""

    if pattern == "heap_two_heaps":
        return """#include <iostream>
#include <vector>
#include <queue>
#include <string>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    priority_queue<long long> low;
    priority_queue<long long, vector<long long>, greater<long long>> high;

    for (int i = 0; i < n; i++) {
        long long val;
        cin >> val;

        if (low.empty() || val <= low.top()) {
            low.push(val);
        } else {
            high.push(val);
        }

        if (low.size() > high.size() + 1) {
            high.push(low.top());
            low.pop();
        } else if (high.size() > low.size()) {
            low.push(high.top());
            high.pop();
        }

        if (low.size() > high.size()) {
            cout << low.top() << "\\n";
        } else {
            double med = (low.top() + high.top()) / 2.0;
            if (med == (long long)med) {
                cout << (long long)med << "\\n";
            } else {
                cout << med << "\\n";
            }
        }
    }

    return 0;
}
"""

    if pattern == "heap_dynamic_median":
        return """#include <iostream>
#include <vector>
#include <queue>
#include <iomanip>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    priority_queue<long long> low;
    priority_queue<long long, vector<long long>, greater<long long>> high;

    for (int i = 0; i < n; i++) {
        long long val;
        cin >> val;

        if (low.empty() || val <= low.top()) {
            low.push(val);
        } else {
            high.push(val);
        }

        if (low.size() > high.size() + 1) {
            high.push(low.top());
            low.pop();
        } else if (high.size() > low.size()) {
            low.push(high.top());
            high.pop();
        }

        if (low.size() > high.size()) {
            cout << low.top() << "\\n";
        } else {
            double med = (low.top() + high.top()) / 2.0;
            if (med == (long long)med) {
                cout << (long long)med << "\\n";
            } else {
                cout << fixed << setprecision(1) << med << "\\n";
            }
        }
    }

    return 0;
}
"""

    if pattern == "heap_scheduling":
        return """#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

struct Interval {
    int start, end;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    vector<Interval> intervals(n);
    for (int i = 0; i < n; i++) {
        cin >> intervals[i].start >> intervals[i].end;
    }

    sort(intervals.begin(), intervals.end(), [](const Interval& a, const Interval& b) {
        if (a.start != b.start) return a.start < b.start;
        return a.end < b.end;
    });

    priority_queue<int, vector<int>, greater<int>> pq;

    int max_rooms = 0;
    for (const auto& iv : intervals) {
        while (!pq.empty() && pq.top() <= iv.start) {
            pq.pop();
        }
        pq.push(iv.end);
        max_rooms = max(max_rooms, (int)pq.size());
    }

    cout << max_rooms << "\\n";

    return 0;
}
"""

    if pattern == "heap_greedy_selection":
        return """#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    priority_queue<long long, vector<long long>, greater<long long>> pq;

    for (int i = 0; i < n; i++) {
        long long val;
        cin >> val;
        pq.push(val);
    }

    long long total_cost = 0;
    while (pq.size() > 1) {
        long long a = pq.top(); pq.pop();
        long long b = pq.top(); pq.pop();
        long long merged = a + b;
        total_cost += merged;
        pq.push(merged);
    }

    cout << total_cost << "\\n";

    return 0;
}
"""

    if pattern == "heap_lazy_deletion":
        return """#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <string>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int q;
    if (!(cin >> q) || q <= 0) return 0;

    priority_queue<long long> pq;
    unordered_map<long long, int> valid_counts;

    for (int i = 0; i < q; i++) {
        string op;
        cin >> op;
        if (op == "INSERT" || op == "insert" || op == "PUSH" || op == "push") {
            long long val;
            cin >> val;
            pq.push(val);
            valid_counts[val]++;
        } else if (op == "DELETE" || op == "delete" || op == "REMOVE" || op == "remove") {
            long long val;
            cin >> val;
            if (valid_counts[val] > 0) {
                valid_counts[val]--;
            }
        } else if (op == "GET_MAX" || op == "get_max" || op == "TOP" || op == "top") {
            while (!pq.empty() && valid_counts[pq.top()] == 0) {
                pq.pop();
            }
            if (!pq.empty()) {
                cout << pq.top() << "\\n";
            } else {
                cout << "EMPTY\\n";
            }
        } else if (op == "EXTRACT_MAX" || op == "extract_max" || op == "POP" || op == "pop") {
            while (!pq.empty() && valid_counts[pq.top()] == 0) {
                pq.pop();
            }
            if (!pq.empty()) {
                long long mx = pq.top();
                pq.pop();
                valid_counts[mx]--;
                cout << mx << "\\n";
            } else {
                cout << "EMPTY\\n";
            }
        }
    }

    return 0;
}
"""

    return f"""#include <iostream>
#include <queue>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    priority_queue<long long> pq;
    return 0;
}}
"""
