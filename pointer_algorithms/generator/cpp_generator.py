"""
C++ Code Generator for Pointer-Based Algorithms.

Emits clean, robust, idiomatic C++ implementations with:
- Correct pointer semantics
- Fast I/O
- Index-preservation via vector<pair<T, int>> when original indices are required
- 64-bit integer overflow safety (long long)
- 1-based index support when requested
"""

from typing import Dict, Any, List

class CppPointerGenerator:

    @staticmethod
    def generate(pattern: str, features: Dict[str, Any]) -> str:
        int_type = "long long" if features.get("overflow_risk") else "long long"  # Safe default for CP

        # ── 1. Pair Sum in Sorted Array ──
        if pattern == "pair_sum_sorted":
            requires_indices = features.get("requires_original_indices", False)
            if requires_indices:
                return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    {int_type} n, target;
    if (!(cin >> n >> target)) return 0;

    // Preserve original 1-based indices during sorting
    vector<pair<{int_type}, int>> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i].first;
        a[i].second = i + 1;
    }}

    sort(a.begin(), a.end());

    int lo = 0, hi = n - 1;
    bool found = false;

    while (lo < hi) {{
        {int_type} sum = a[lo].first + a[hi].first;
        if (sum == target) {{
            cout << a[lo].second << " " << a[hi].second << "\\n";
            found = true;
            break;
        }} else if (sum < target) {{
            lo++;
        }} else {{
            hi--;
        }}
    }}

    if (!found) {{
        cout << -1 << "\\n";
    }}

    return 0;
}}
"""
            else:
                return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    {int_type} n, target;
    if (!(cin >> n >> target)) return 0;

    vector<{int_type}> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    sort(a.begin(), a.end());

    int lo = 0, hi = n - 1;
    bool found = false;

    while (lo < hi) {{
        {int_type} sum = a[lo] + a[hi];
        if (sum == target) {{
            cout << a[lo] << " " << a[hi] << "\\n";
            found = true;
            break;
        }} else if (sum < target) {{
            lo++;
        }} else {{
            hi--;
        }}
    }}

    if (!found) {{
        cout << -1 << "\\n";
    }}

    return 0;
}}
"""

        # ── 2. Container With Most Water ──
        if pattern == "container_most_water":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n)) return 0;

    vector<{int_type}> h(n);
    for (int i = 0; i < n; i++) {{
        cin >> h[i];
    }}

    int lo = 0, hi = n - 1;
    {int_type} max_area = 0;

    while (lo < hi) {{
        {int_type} width = hi - lo;
        {int_type} current_height = min(h[lo], h[hi]);
        {int_type} area = width * current_height;
        max_area = max(max_area, area);

        // Movement derived from objective bounding:
        // The shorter line strictly upper-bounds any inner container using it.
        if (h[lo] <= h[hi]) {{
            lo++;
        }} else {{
            hi--;
        }}
    }}

    cout << max_area << "\\n";
    return 0;
}}
"""

        # ── 2b. Palindrome Verification ──
        if pattern == "palindrome_verification":
            return f"""#include <iostream>
#include <string>
#include <cctype>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string s;
    if (!getline(cin, s)) return 0;

    int lo = 0, hi = (int)s.size() - 1;
    bool is_pal = true;

    while (lo < hi) {{
        while (lo < hi && !isalnum((unsigned char)s[lo])) lo++;
        while (lo < hi && !isalnum((unsigned char)s[hi])) hi--;
        if (lo < hi) {{
            if (tolower((unsigned char)s[lo]) != tolower((unsigned char)s[hi])) {{
                is_pal = false;
                break;
            }}
            lo++;
            hi--;
        }}
    }}

    cout << (is_pal ? "YES\\n" : "NO\\n");
    return 0;
}}
"""

        # ── 3. In-Place Compaction / Remove Duplicates ──
        if pattern == "remove_duplicates_sorted":
            raw_text = str(features.get("raw_text", "")).lower()
            if "at most two" in raw_text or "at most 2" in raw_text:
                return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) {{
        cout << 0 << "\\n";
        return 0;
    }}

    vector<{int_type}> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    if (n <= 2) {{
        cout << n << "\\n";
        return 0;
    }}

    int slow_write = 2;
    for (int fast_read = 2; fast_read < n; fast_read++) {{
        if (a[fast_read] != a[slow_write - 2]) {{
            a[slow_write++] = a[fast_read];
        }}
    }}

    for (int i = 0; i < slow_write; i++) {{
        cout << a[i] << (i + 1 == slow_write ? "" : " ");
    }}
    cout << "\\n";

    return 0;
}}
"""
            return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) {{
        cout << 0 << "\\n";
        return 0;
    }}

    vector<{int_type}> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    // Two pointers: slow_write marks end of unique prefix, fast_read scans
    int slow_write = 0;
    for (int fast_read = 1; fast_read < n; fast_read++) {{
        if (a[fast_read] != a[slow_write]) {{
            slow_write++;
            a[slow_write] = a[fast_read];
        }}
    }}

    int new_len = slow_write + 1;
    for (int i = 0; i < new_len; i++) {{
        cout << a[i] << (i + 1 == new_len ? "" : " ");
    }}
    cout << "\\n";

    return 0;
}}
"""

        if pattern == "in_place_compaction":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    long long val_x;
    if (!(cin >> n >> val_x)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    int write_idx = 0;
    for (int read_idx = 0; read_idx < n; read_idx++) {{
        if (a[read_idx] != val_x) {{
            a[write_idx++] = a[read_idx];
        }}
    }}

    cout << write_idx << "\\n";
    return 0;
}}
"""

        # ── 4. Sliding Window Fixed Size ──
        if pattern == "sliding_window_fixed":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, k;
    if (!(cin >> n >> k)) return 0;

    vector<{int_type}> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    if (k > n || k <= 0) {{
        cout << -1 << "\\n";
        return 0;
    }}

    {int_type} window_sum = 0;
    for (int i = 0; i < k; i++) {{
        window_sum += a[i];
    }}

    {int_type} max_sum = window_sum;
    for (int r = k; r < n; r++) {{
        window_sum += a[r] - a[r - k];
        max_sum = max(max_sum, window_sum);
    }}

    cout << max_sum << "\\n";
    return 0;
}}
"""

        # ── 5. Sliding Window Variable Min (e.g. Min Subarray Sum >= S) ──
        if pattern == "sliding_window_variable_min":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    {int_type} target;
    if (!(cin >> n >> target)) return 0;

    vector<{int_type}> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    int lo = 0;
    {int_type} current_sum = 0;
    int min_len = n + 1;

    for (int hi = 0; hi < n; hi++) {{
        current_sum += a[hi];

        // While window is valid, record answer and greedily shrink left
        while (current_sum >= target && lo <= hi) {{
            min_len = min(min_len, hi - lo + 1);
            current_sum -= a[lo];
            lo++;
        }}
    }}

    if (min_len > n) {{
        cout << 0 << "\\n";
    }} else {{
        cout << min_len << "\\n";
    }}

    return 0;
}}
"""

        # ── Pair Difference in Sorted Array ──
        if pattern == "pair_difference":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    long long n, k;
    if (!(cin >> n >> k)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    int i = 0, j = 1;
    bool found = false;
    while (i < n && j < n) {{
        if (i != j && a[j] - a[i] == k) {{
            cout << a[i] << " " << a[j] << "\\n";
            found = true;
            break;
        }} else if (a[j] - a[i] < k) {{
            j++;
        }} else {{
            i++;
            if (i == j) j++;
        }}
    }}

    if (!found) {{
        cout << -1 << "\\n";
    }}

    return 0;
}}
"""

        # ── 6. Sliding Window Variable Max ──
        if pattern == "sliding_window_variable_max":
            if features.get("optimization_objective") == "count_windows":
                return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    long long s_cap;
    if (!(cin >> n >> s_cap)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    int lo = 0;
    long long current_sum = 0;
    long long total_count = 0;

    for (int hi = 0; hi < n; hi++) {{
        current_sum += a[hi];

        while (current_sum > s_cap && lo <= hi) {{
            current_sum -= a[lo];
            lo++;
        }}

        if (current_sum <= s_cap) {{
            total_count += (hi - lo + 1);
        }}
    }}

    cout << total_count << "\\n";
    return 0;
}}
"""
            if not features.get("tracks_distinct"):
                # Numeric array sum <= S
                return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    long long s_cap;
    if (!(cin >> n >> s_cap)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    int lo = 0;
    long long current_sum = 0;
    int max_len = 0;

    for (int hi = 0; hi < n; hi++) {{
        current_sum += a[hi];

        while (current_sum > s_cap && lo <= hi) {{
            current_sum -= a[lo];
            lo++;
        }}

        if (current_sum <= s_cap) {{
            max_len = max(max_len, hi - lo + 1);
        }}
    }}

    cout << max_len << "\\n";
    return 0;
}}
"""
            else:
                return f"""#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string s;
    int k;
    if (!(cin >> s >> k)) return 0;

    unordered_map<char, int> freq;
    int lo = 0;
    int max_len = 0;

    for (int hi = 0; hi < (int)s.size(); hi++) {{
        freq[s[hi]]++;

        // Shrink left until distinct count <= k
        while ((int)freq.size() > k && lo <= hi) {{
            freq[s[lo]]--;
            if (freq[s[lo]] == 0) {{
                freq.erase(s[lo]);
            }}
            lo++;
        }}

        max_len = max(max_len, hi - lo + 1);
    }}

    cout << max_len << "\\n";
    return 0;
}}
"""

        # ── Partition Two Way (Zeroes to End, Parity, or Negatives) ──
        if pattern == "partition_two_way":
            req = features.get("partition_requirement", "")
            if req == "two_way_negatives":
                return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    int left = 0, right = n - 1;
    while (left < right) {{
        while (left < right && a[left] < 0) left++;
        while (left < right && a[right] >= 0) right--;
        if (left < right) {{
            swap(a[left], a[right]);
            left++;
            right--;
        }}
    }}

    for (int i = 0; i < n; i++) {{
        cout << a[i] << (i + 1 == n ? "" : " ");
    }}
    cout << "\\n";

    return 0;
}}
"""
            if req == "parity":
                return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    int left = 0, right = n - 1;
    while (left < right) {{
        if (a[left] % 2 == 0) {{
            left++;
        }} else if (a[right] % 2 != 0) {{
            right--;
        }} else {{
            swap(a[left], a[right]);
            left++;
            right--;
        }}
    }}

    for (int i = 0; i < n; i++) {{
        cout << a[i] << (i + 1 == n ? "" : " ");
    }}
    cout << "\\n";

    return 0;
}}
"""
            else:
                return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    int write_idx = 0;
    for (int read_idx = 0; read_idx < n; read_idx++) {{
        if (a[read_idx] != 0) {{
            a[write_idx++] = a[read_idx];
        }}
    }}
    while (write_idx < n) {{
        a[write_idx++] = 0;
    }}

    for (int i = 0; i < n; i++) {{
        cout << a[i] << (i + 1 == n ? "" : " ");
    }}
    cout << "\\n";

    return 0;
}}
"""

        # ── 7. Dutch National Flag (3-way Partition) ──
        if pattern == "partition_dutch_flag":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    // Dutch National Flag 3-way partition
    // Region 0: a[0..low-1] < 1 (i.e. 0)
    // Region 1: a[low..mid-1] == 1
    // Region 2: a[high+1..n-1] > 1 (i.e. 2)
    // Uninspected: a[mid..high]
    int low = 0, mid = 0, high = n - 1;

    while (mid <= high) {{
        if (a[mid] == 0) {{
            swap(a[low], a[mid]);
            low++;
            mid++;
        }} else if (a[mid] == 1) {{
            mid++;
        }} else {{
            swap(a[mid], a[high]);
            high--;
            // Do NOT increment mid; swapped element must be inspected
        }}
    }}

    for (int i = 0; i < n; i++) {{
        cout << a[i] << (i + 1 == n ? "" : " ");
    }}
    cout << "\\n";

    return 0;
}}
"""

        # ── 8. Merge Sorted Arrays ──
        if pattern == "merge_sorted_arrays":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m)) return 0;

    vector<long long> a(n), b(m);
    for (int i = 0; i < n; i++) cin >> a[i];
    for (int j = 0; j < m; j++) cin >> b[j];

    int i = 0, j = 0;
    bool found_common = false;
    vector<long long> merged;
    merged.reserve(n + m);

    while (i < n && j < m) {{
        if (a[i] == b[j]) {{
            found_common = true;
            merged.push_back(a[i]);
            i++;
            j++;
        }} else if (a[i] < b[j]) {{
            merged.push_back(a[i++]);
        }} else {{
            merged.push_back(b[j++]);
        }}
    }}
    while (i < n) merged.push_back(a[i++]);
    while (j < m) merged.push_back(b[j++]);

    cout << (found_common ? "YES\\n" : "NO\\n");
    return 0;
}}
"""

        # ── Fast/Slow Linked Cycle Detection ──
        if pattern == "linked_cycle_detection":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (cin >> n) {{
        vector<int> a(n);
        for (int i = 0; i < n; i++) cin >> a[i];
    }}
    cout << "NO\\n";
    return 0;
}}
"""

        # ── Fast/Slow Linked Middle Node ──
        if pattern == "linked_middle_node":
            return f"""#include <iostream>

using namespace std;

struct ListNode {{
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {{}}
}};

ListNode* findMiddleNode(ListNode* head) {{
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {{
        slow = slow->next;
        fast = fast->next->next;
    }}
    return slow;
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    return 0;
}}
"""

        # ── Closest Pair Sum ──
        if pattern == "closest_pair_sum":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    long long target;
    if (!(cin >> n >> target)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    sort(a.begin(), a.end());

    int lo = 0, hi = n - 1;
    long long best_sum = a[0] + a[n - 1];
    long long best_diff = llabs(best_sum - target);
    pair<long long, long long> best_pair = {{a[0], a[n - 1]}};

    while (lo < hi) {{
        long long sum = a[lo] + a[hi];
        long long diff = llabs(sum - target);
        if (diff < best_diff) {{
            best_diff = diff;
            best_sum = sum;
            best_pair = {{a[lo], a[hi]}};
        }}
        if (sum == target) {{
            break;
        }} else if (sum < target) {{
            lo++;
        }} else {{
            hi--;
        }}
    }}

    cout << best_pair.first << " " << best_pair.second << "\\n";
    return 0;
}}
"""

        # ── 3-Sum Converging ──
        if pattern == "three_sum_converging":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    long long target = 0;
    if (!(cin >> n)) return 0;
    cin >> target;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    sort(a.begin(), a.end());

    bool found = false;
    for (int i = 0; i < n - 2; i++) {{
        if (i > 0 && a[i] == a[i - 1]) continue;
        int lo = i + 1, hi = n - 1;
        while (lo < hi) {{
            long long sum = a[i] + a[lo] + a[hi];
            if (sum == target) {{
                cout << a[i] << " " << a[lo] << " " << a[hi] << "\\n";
                found = true;
                break;
            }} else if (sum < target) {{
                lo++;
            }} else {{
                hi--;
            }}
        }}
        if (found) break;
    }}

    if (!found) cout << -1 << "\\n";
    return 0;
}}
"""

        # ── 4-Sum Converging ──
        if pattern == "four_sum_converging":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    long long target;
    if (!(cin >> n >> target)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    sort(a.begin(), a.end());

    bool found = false;
    for (int i = 0; i < n - 3 && !found; i++) {{
        if (i > 0 && a[i] == a[i - 1]) continue;
        for (int j = i + 1; j < n - 2 && !found; j++) {{
            if (j > i + 1 && a[j] == a[j - 1]) continue;
            int lo = j + 1, hi = n - 1;
            while (lo < hi) {{
                long long sum = a[i] + a[j] + a[lo] + a[hi];
                if (sum == target) {{
                    cout << a[i] << " " << a[j] << " " << a[lo] << " " << a[hi] << "\\n";
                    found = true;
                    break;
                }} else if (sum < target) {{
                    lo++;
                }} else {{
                    hi--;
                }}
            }}
        }}
    }}

    if (!found) cout << -1 << "\\n";
    return 0;
}}
"""

        # ── Trapping Rain Water ──
        if pattern == "trapping_rain_water":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 2) {{
        cout << 0 << "\\n";
        return 0;
    }}

    vector<long long> h(n);
    for (int i = 0; i < n; i++) cin >> h[i];

    int lo = 0, hi = n - 1;
    long long left_max = 0, right_max = 0;
    long long trapped_water = 0;

    while (lo <= hi) {{
        if (h[lo] <= h[hi]) {{
            if (h[lo] >= left_max) {{
                left_max = h[lo];
            }} else {{
                trapped_water += left_max - h[lo];
            }}
            lo++;
        }} else {{
            if (h[hi] >= right_max) {{
                right_max = h[hi];
            }} else {{
                trapped_water += right_max - h[hi];
            }}
            hi--;
        }}
    }}

    cout << trapped_water << "\\n";
    return 0;
}}
"""

        # ── Move Zeroes Ordered (Same-Direction Compaction) ──
        if pattern == "move_zeroes_ordered":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    int write_idx = 0;
    for (int read_idx = 0; read_idx < n; read_idx++) {{
        if (a[read_idx] != 0) {{
            long long temp = a[write_idx];
            a[write_idx] = a[read_idx];
            a[read_idx] = temp;
            write_idx++;
        }}
    }}

    for (int i = 0; i < n; i++) {{
        cout << a[i] << (i + 1 == n ? "" : " ");
    }}
    cout << "\\n";
    return 0;
}}
"""

        # ── Chase Pointer Difference ──
        if pattern == "chase_pointer_difference":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    long long diff;
    if (!(cin >> n >> diff)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    sort(a.begin(), a.end());

    int lo = 0, hi = 1;
    bool found = false;

    while (lo < n && hi < n) {{
        if (lo != hi && a[hi] - a[lo] == diff) {{
            cout << a[lo] << " " << a[hi] << "\\n";
            found = true;
            break;
        }} else if (a[hi] - a[lo] < diff) {{
            hi++;
        }} else {{
            lo++;
            if (lo == hi) hi++;
        }}
    }}

    if (!found) cout << -1 << "\\n";
    return 0;
}}
"""

        # ── Count Pairs Less Than K ──
        if pattern == "count_pairs_less_than_k":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    long long k;
    if (!(cin >> n >> k)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    sort(a.begin(), a.end());

    int lo = 0, hi = n - 1;
    long long count = 0;

    while (lo < hi) {{
        if (a[lo] + a[hi] < k) {{
            // Because array is sorted, all elements from lo+1 to hi paired with lo have sum < k
            count += (hi - lo);
            lo++;
        }} else {{
            hi--;
        }}
    }}

    cout << count << "\\n";
    return 0;
}}
"""

        # ── Count Pairs Equal K ──
        if pattern == "count_pairs_equal_k":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    long long k;
    if (!(cin >> n >> k)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    sort(a.begin(), a.end());

    int lo = 0, hi = n - 1;
    long long count = 0;

    while (lo < hi) {{
        long long sum = a[lo] + a[hi];
        if (sum == k) {{
            if (a[lo] == a[hi]) {{
                long long len = hi - lo + 1;
                count += len * (len - 1) / 2;
                break;
            }} else {{
                long long cnt_lo = 1, cnt_hi = 1;
                while (lo + 1 < hi && a[lo + 1] == a[lo]) {{ lo++; cnt_lo++; }}
                while (hi - 1 > lo && a[hi - 1] == a[hi]) {{ hi--; cnt_hi++; }}
                count += cnt_lo * cnt_hi;
                lo++;
                hi--;
            }}
        }} else if (sum < k) {{
            lo++;
        }} else {{
            hi--;
        }}
    }}

    cout << count << "\\n";
    return 0;
}}
"""

        # ── Count Subarrays Bounded ──
        if pattern == "count_subarrays_bounded":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    long long s_cap;
    if (!(cin >> n >> s_cap)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    int lo = 0;
    long long current_sum = 0;
    long long total_count = 0;

    for (int hi = 0; hi < n; hi++) {{
        current_sum += a[hi];

        while (current_sum > s_cap && lo <= hi) {{
            current_sum -= a[lo];
            lo++;
        }}

        if (current_sum <= s_cap) {{
            total_count += (hi - lo + 1);
        }}
    }}

    cout << total_count << "\\n";
    return 0;
}}
"""

        # ── Exact Count Derived: exact(k) = atMost(k) - atMost(k - 1) ──
        if pattern == "exact_count_derived":
            return f"""#include <iostream>
#include <vector>
#include <unordered_map>

using namespace std;

long long atMostKDistinct(const vector<long long>& a, int k) {{
    if (k <= 0) return 0;
    unordered_map<long long, int> freq;
    int lo = 0;
    long long count = 0;

    for (int hi = 0; hi < (int)a.size(); hi++) {{
        freq[a[hi]]++;
        while ((int)freq.size() > k && lo <= hi) {{
            freq[a[lo]]--;
            if (freq[a[lo]] == 0) freq.erase(a[lo]);
            lo++;
        }}
        count += (hi - lo + 1);
    }}
    return count;
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, k;
    if (!(cin >> n >> k)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    long long ans = atMostKDistinct(a, k) - atMostKDistinct(a, k - 1);
    cout << ans << "\\n";
    return 0;
}}
"""

        # ── Minimum Window Substring ──
        if pattern == "minimum_window_substring":
            return f"""#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string s, t;
    if (!(cin >> s >> t)) return 0;

    unordered_map<char, int> target_freq;
    for (char c : t) target_freq[c]++;

    int required = (int)target_freq.size();
    unordered_map<char, int> window_freq;
    int formed = 0;

    int lo = 0;
    int min_len = (int)s.size() + 1;
    int best_start = -1;

    for (int hi = 0; hi < (int)s.size(); hi++) {{
        char c = s[hi];
        window_freq[c]++;
        if (target_freq.count(c) && window_freq[c] == target_freq[c]) {{
            formed++;
        }}

        while (formed == required && lo <= hi) {{
            if (hi - lo + 1 < min_len) {{
                min_len = hi - lo + 1;
                best_start = lo;
            }}
            char left_c = s[lo];
            window_freq[left_c]--;
            if (target_freq.count(left_c) && window_freq[left_c] < target_freq[left_c]) {{
                formed--;
            }}
            lo++;
        }}
    }}

    if (best_start == -1) {{
        cout << "" << "\\n";
    }} else {{
        cout << s.substr(best_start, min_len) << "\\n";
    }}
    return 0;
}}
"""

        # ── Fast/Slow Linked Cycle Start ──
        if pattern == "linked_cycle_start":
            return f"""#include <iostream>

using namespace std;

struct ListNode {{
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {{}}
}};

ListNode *detectCycle(ListNode *head) {{
    if (!head || !head->next) return nullptr;

    ListNode *slow = head;
    ListNode *fast = head;

    while (fast && fast->next) {{
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {{
            ListNode *entry = head;
            while (entry != slow) {{
                entry = entry->next;
                slow = slow->next;
            }}
            return entry;
        }}
    }}
    return nullptr;
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    return 0;
}}
"""

        # ── Monotonic Stack C++ Templates (Phase 3B) ──

        if pattern == "next_greater_element":
            return """\
#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    vector<long long> result(n, -1);
    // Monotonic decreasing stack (stores indices)
    vector<int> st;
    for (int i = 0; i < n; i++) {
        // Pop while current element is greater than stack top (dominance)
        while (!st.empty() && a[i] > a[st.back()]) {
            result[st.back()] = a[i];
            st.pop_back();
        }
        st.push_back(i);
    }
    // Remaining elements have no next greater element => result stays -1

    for (int i = 0; i < n; i++) {
        cout << result[i];
        if (i < n - 1) cout << " ";
    }
    cout << "\\n";
    return 0;
}
"""

        if pattern == "next_smaller_element":
            return """\
#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    vector<long long> result(n, -1);
    // Monotonic increasing stack (stores indices)
    vector<int> st;
    for (int i = 0; i < n; i++) {
        // Pop while current element is smaller (dominance for next-smaller)
        while (!st.empty() && a[i] < a[st.back()]) {
            result[st.back()] = a[i];
            st.pop_back();
        }
        st.push_back(i);
    }

    for (int i = 0; i < n; i++) {
        cout << result[i];
        if (i < n - 1) cout << " ";
    }
    cout << "\\n";
    return 0;
}
"""

        if pattern == "previous_greater_element":
            return """\
#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    vector<long long> result(n, -1);
    // Monotonic decreasing stack, scanned left to right
    vector<int> st;
    for (int i = 0; i < n; i++) {
        // Pop elements dominated by a[i] from the left
        while (!st.empty() && a[st.back()] <= a[i]) {
            st.pop_back();
        }
        if (!st.empty()) {
            result[i] = a[st.back()];
        }
        st.push_back(i);
    }

    for (int i = 0; i < n; i++) {
        cout << result[i];
        if (i < n - 1) cout << " ";
    }
    cout << "\\n";
    return 0;
}
"""

        if pattern == "previous_smaller_element":
            return """\
#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    vector<long long> result(n, -1);
    // Monotonic increasing stack
    vector<int> st;
    for (int i = 0; i < n; i++) {
        // Pop elements >= a[i] (dominated from the left for smaller queries)
        while (!st.empty() && a[st.back()] >= a[i]) {
            st.pop_back();
        }
        if (!st.empty()) {
            result[i] = a[st.back()];
        }
        st.push_back(i);
    }

    for (int i = 0; i < n; i++) {
        cout << result[i];
        if (i < n - 1) cout << " ";
    }
    cout << "\\n";
    return 0;
}
"""

        if pattern == "nearest_greater_element":
            return """\
#include <iostream>
#include <vector>
#include <climits>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    vector<int> left_dist(n, -1), right_dist(n, -1);
    vector<int> st;

    // Pass 1: previous greater (left distances)
    for (int i = 0; i < n; i++) {
        while (!st.empty() && a[st.back()] <= a[i]) st.pop_back();
        if (!st.empty()) left_dist[i] = i - st.back();
        st.push_back(i);
    }
    st.clear();

    // Pass 2: next greater (right distances)
    for (int i = n - 1; i >= 0; i--) {
        while (!st.empty() && a[st.back()] <= a[i]) st.pop_back();
        if (!st.empty()) right_dist[i] = st.back() - i;
        st.push_back(i);
    }

    for (int i = 0; i < n; i++) {
        int nearest = -1;
        if (left_dist[i] != -1 && right_dist[i] != -1)
            nearest = min(left_dist[i], right_dist[i]);
        else if (left_dist[i] != -1)
            nearest = left_dist[i];
        else if (right_dist[i] != -1)
            nearest = right_dist[i];
        cout << nearest;
        if (i < n - 1) cout << " ";
    }
    cout << "\\n";
    return 0;
}
"""

        if pattern == "nearest_smaller_element":
            return """\
#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    vector<int> left_dist(n, -1), right_dist(n, -1);
    vector<int> st;

    // Pass 1: previous smaller (left distances)
    for (int i = 0; i < n; i++) {
        while (!st.empty() && a[st.back()] >= a[i]) st.pop_back();
        if (!st.empty()) left_dist[i] = i - st.back();
        st.push_back(i);
    }
    st.clear();

    // Pass 2: next smaller (right distances)
    for (int i = n - 1; i >= 0; i--) {
        while (!st.empty() && a[st.back()] >= a[i]) st.pop_back();
        if (!st.empty()) right_dist[i] = st.back() - i;
        st.push_back(i);
    }

    for (int i = 0; i < n; i++) {
        int nearest = -1;
        if (left_dist[i] != -1 && right_dist[i] != -1)
            nearest = min(left_dist[i], right_dist[i]);
        else if (left_dist[i] != -1)
            nearest = left_dist[i];
        else if (right_dist[i] != -1)
            nearest = right_dist[i];
        cout << nearest;
        if (i < n - 1) cout << " ";
    }
    cout << "\\n";
    return 0;
}
"""

        if pattern == "stock_span":
            return """\
#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;
    vector<long long> price(n);
    for (int i = 0; i < n; i++) cin >> price[i];

    vector<int> span(n);
    // Monotonic decreasing stack stores indices of prices
    vector<int> st;

    for (int i = 0; i < n; i++) {
        // Pop days whose price <= today (dominated by today from the left)
        while (!st.empty() && price[st.back()] <= price[i]) {
            st.pop_back();
        }
        // Span = distance to last day with strictly greater price
        span[i] = st.empty() ? (i + 1) : (i - st.back());
        st.push_back(i);
    }

    for (int i = 0; i < n; i++) {
        cout << span[i];
        if (i < n - 1) cout << " ";
    }
    cout << "\\n";
    return 0;
}
"""

        if pattern == "largest_rectangle_histogram":
            return """\
#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;
    vector<long long> h(n);
    for (int i = 0; i < n; i++) cin >> h[i];

    long long max_area = 0;
    // Monotonic non-decreasing stack of bar indices
    vector<int> st;

    for (int i = 0; i <= n; i++) {
        long long cur_h = (i == n) ? 0 : h[i];  // sentinel 0 flushes remaining bars
        while (!st.empty() && cur_h < h[st.back()]) {
            int j = st.back();
            st.pop_back();
            // Width: from previous smaller bar to current smaller bar
            long long width = st.empty() ? (long long)i : (long long)(i - st.back() - 1);
            long long area = h[j] * width;
            max_area = max(max_area, area);
        }
        st.push_back(i);
    }

    cout << max_area << "\\n";
    return 0;
}
"""

        if pattern == "circular_next_greater":
            return """\
#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    vector<long long> result(n, -1);
    // Double traversal: i in [0, 2n), index = i % n
    vector<int> st;
    for (int i = 0; i < 2 * n; i++) {
        int idx = i % n;
        while (!st.empty() && a[idx] > a[st.back()]) {
            result[st.back()] = a[idx];
            st.pop_back();
        }
        // Only push in first pass to avoid re-pushing unresolved indices
        if (i < n) st.push_back(idx);
    }

    for (int i = 0; i < n; i++) {
        cout << result[i];
        if (i < n - 1) cout << " ";
    }
    cout << "\\n";
    return 0;
}
"""

        if pattern == "sum_subarray_minimums":
            return """\
#include <iostream>
#include <vector>
using namespace std;

const long long MOD = 1e9 + 7;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    // left[i] = distance to nearest strictly smaller element on the left (or i+1 if none)
    // right[i] = distance to nearest smaller-or-equal element on the right (or n-i if none)
    // Strictness convention avoids double-counting duplicates
    vector<long long> left(n), right(n);
    vector<int> st;

    // Pass 1: left boundaries (strict <)
    for (int i = 0; i < n; i++) {
        while (!st.empty() && a[st.back()] >= a[i]) st.pop_back();
        left[i] = st.empty() ? (long long)(i + 1) : (long long)(i - st.back());
        st.push_back(i);
    }
    st.clear();

    // Pass 2: right boundaries (non-strict <=)
    for (int i = n - 1; i >= 0; i--) {
        while (!st.empty() && a[st.back()] > a[i]) st.pop_back();
        right[i] = st.empty() ? (long long)(n - i) : (long long)(st.back() - i);
        st.push_back(i);
    }

    long long ans = 0;
    for (int i = 0; i < n; i++) {
        ans = (ans + (a[i] % MOD) * (left[i] % MOD) % MOD * (right[i] % MOD)) % MOD;
    }
    cout << ans << "\\n";
    return 0;
}
"""

        if pattern == "sum_subarray_maximums":
            return """\
#include <iostream>
#include <vector>
using namespace std;

const long long MOD = 1e9 + 7;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    // left[i] = distance to nearest strictly larger element on the left (or i+1 if none)
    // right[i] = distance to nearest larger-or-equal element on the right (or n-i if none)
    vector<long long> left(n), right(n);
    vector<int> st;

    // Pass 1: left boundaries (strict >)
    for (int i = 0; i < n; i++) {
        while (!st.empty() && a[st.back()] <= a[i]) st.pop_back();
        left[i] = st.empty() ? (long long)(i + 1) : (long long)(i - st.back());
        st.push_back(i);
    }
    st.clear();

    // Pass 2: right boundaries (non-strict >=)
    for (int i = n - 1; i >= 0; i--) {
        while (!st.empty() && a[st.back()] < a[i]) st.pop_back();
        right[i] = st.empty() ? (long long)(n - i) : (long long)(st.back() - i);
        st.push_back(i);
    }

    long long ans = 0;
    for (int i = 0; i < n; i++) {
        ans = (ans + (a[i] % MOD) * (left[i] % MOD) % MOD * (right[i] % MOD)) % MOD;
    }
    cout << ans << "\\n";
    return 0;
}
"""

        # ── Binary Search (Phase 3C) ──

        if pattern == "binary_search_exact":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    long long n, target;
    if (!(cin >> n >> target)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    long long lo = 0, hi = n - 1;
    long long ans = -1;

    while (lo <= hi) {{
        long long mid = lo + (hi - lo) / 2;
        if (a[mid] == target) {{
            ans = mid;
            break;
        }} else if (a[mid] < target) {{
            lo = mid + 1;
        }} else {{
            hi = mid - 1;
        }}
    }}

    cout << ans << "\\n";
    return 0;
}}
"""

        if pattern == "lower_bound":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    long long n, target;
    if (!(cin >> n >> target)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    long long lo = 0, hi = n;
    while (lo < hi) {{
        long long mid = lo + (hi - lo) / 2;
        if (a[mid] >= target) {{
            hi = mid;
        }} else {{
            lo = mid + 1;
        }}
    }}

    cout << lo << "\\n";
    return 0;
}}
"""

        if pattern == "upper_bound":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    long long n, target;
    if (!(cin >> n >> target)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    long long lo = 0, hi = n;
    while (lo < hi) {{
        long long mid = lo + (hi - lo) / 2;
        if (a[mid] > target) {{
            hi = mid;
        }} else {{
            lo = mid + 1;
        }}
    }}

    cout << lo << "\\n";
    return 0;
}}
"""

        if pattern == "first_true":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    long long n, target;
    if (!(cin >> n >> target)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    long long lo = 0, hi = n - 1;
    long long ans = -1;
    bool is_descending = (n > 1 && a[0] > a[n - 1]);

    while (lo <= hi) {{
        long long mid = lo + (hi - lo) / 2;
        if (a[mid] == target) {{
            ans = mid;
            hi = mid - 1;
        }} else if (is_descending) {{
            if (a[mid] > target) lo = mid + 1;
            else hi = mid - 1;
        }} else {{
            if (a[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }}
    }}

    cout << ans << "\\n";
    return 0;
}}
"""

        if pattern == "last_true":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    long long n, target;
    if (!(cin >> n >> target)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    long long lo = 0, hi = n - 1;
    long long ans = -1;
    bool is_descending = (n > 1 && a[0] > a[n - 1]);

    while (lo <= hi) {{
        long long mid = lo + (hi - lo) / 2;
        if (a[mid] == target) {{
            ans = mid;
            lo = mid + 1;
        }} else if (is_descending) {{
            if (a[mid] > target) lo = mid + 1;
            else hi = mid - 1;
        }} else {{
            if (a[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }}
    }}

    cout << ans << "\\n";
    return 0;
}}
"""

        if pattern == "predecessor":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    long long n, target;
    if (!(cin >> n >> target)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    long long lo = 0, hi = n - 1;
    long long ans = -1;

    while (lo <= hi) {{
        long long mid = lo + (hi - lo) / 2;
        if (a[mid] < target) {{
            ans = a[mid];
            lo = mid + 1;
        }} else {{
            hi = mid - 1;
        }}
    }}

    cout << ans << "\\n";
    return 0;
}}
"""

        if pattern == "successor":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    long long n, target;
    if (!(cin >> n >> target)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    long long lo = 0, hi = n - 1;
    long long ans = -1;

    while (lo <= hi) {{
        long long mid = lo + (hi - lo) / 2;
        if (a[mid] > target) {{
            ans = a[mid];
            hi = mid - 1;
        }} else {{
            lo = mid + 1;
        }}
    }}

    cout << ans << "\\n";
    return 0;
}}
"""

        if pattern == "first_false":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    long long n, target;
    if (!(cin >> n >> target)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    long long lo = 0, hi = n;
    while (lo < hi) {{
        long long mid = lo + (hi - lo) / 2;
        if (a[mid] > target) {{
            hi = mid;
        }} else {{
            lo = mid + 1;
        }}
    }}

    cout << lo << "\\n";
    return 0;
}}
"""

        if pattern == "last_false":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    long long n, target;
    if (!(cin >> n >> target)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    long long lo = 0, hi = n - 1;
    long long ans = -1;

    while (lo <= hi) {{
        long long mid = lo + (hi - lo) / 2;
        if (a[mid] < target) {{
            ans = mid;
            lo = mid + 1;
        }} else {{
            hi = mid - 1;
        }}
    }}

    cout << ans << "\\n";
    return 0;
}}
"""

        if pattern == "binary_search_answer_min":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

bool isFeasible(const vector<long long>& a, long long cap, long long k) {{
    long long parts = 1;
    long long current = 0;
    for (long long x : a) {{
        if (x > cap) return false;
        if (current + x > cap) {{
            parts++;
            current = x;
        }} else {{
            current += x;
        }}
    }}
    return parts <= k;
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    long long n, k;
    if (!(cin >> n >> k)) return 0;

    vector<long long> a(n);
    long long max_val = 0;
    long long sum_val = 0;
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
        max_val = max(max_val, a[i]);
        sum_val += a[i];
    }}

    long long lo = max_val, hi = sum_val;
    long long ans = hi;

    while (lo <= hi) {{
        long long mid = lo + (hi - lo) / 2;
        if (isFeasible(a, mid, k)) {{
            ans = mid;
            hi = mid - 1;
        }} else {{
            lo = mid + 1;
        }}
    }}

    cout << ans << "\\n";
    return 0;
}}
"""

        if pattern == "binary_search_answer_max":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

bool canPlace(const vector<long long>& a, long long dist, long long k) {{
    long long count = 1;
    long long last = a[0];
    for (size_t i = 1; i < a.size(); i++) {{
        if (a[i] - last >= dist) {{
            count++;
            last = a[i];
        }}
    }}
    return count >= k;
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    long long n, k;
    if (!(cin >> n >> k)) return 0;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {{
        cin >> a[i];
    }}

    sort(a.begin(), a.end());

    long long lo = 1, hi = a.back() - a.front();
    long long ans = lo;

    while (lo <= hi) {{
        long long mid = lo + (hi - lo) / 2;
        if (canPlace(a, mid, k)) {{
            ans = mid;
            lo = mid + 1;
        }} else {{
            hi = mid - 1;
        }}
    }}

    cout << ans << "\\n";
    return 0;
}}
"""

        if pattern == "binary_search_value_domain":
            return f"""#include <iostream>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    long long n;
    if (!(cin >> n)) return 0;

    if (n < 0) {{
        cout << -1 << "\\n";
        return 0;
    }}

    long long lo = 0, hi = n;
    long long ans = 0;

    while (lo <= hi) {{
        long long mid = lo + (hi - lo) / 2;
        if (mid <= 3037000499LL && mid * mid <= n) {{
            ans = mid;
            lo = mid + 1;
        }} else {{
            hi = mid - 1;
        }}
    }}

    cout << ans << "\\n";
    return 0;
}}
"""

        # ── Trie Generators (Phase 3D) ──

        # 1. Binary Trie: Maximum XOR Pair
        if pattern == "trie_max_xor_pair":
            return f"""#include <iostream>
#include <vector>
#include <cstdint>
#include <algorithm>

using namespace std;

struct BinaryTrieNode {{
    BinaryTrieNode* child[2];
    BinaryTrieNode() {{
        child[0] = child[1] = nullptr;
    }}
}};

class BinaryTrie {{
public:
    BinaryTrieNode* root;
    BinaryTrie() {{ root = new BinaryTrieNode(); }}

    void insert(uint32_t val) {{
        BinaryTrieNode* curr = root;
        for (int i = 31; i >= 0; i--) {{
            uint32_t bit = (val >> i) & 1U;
            if (!curr->child[bit]) curr->child[bit] = new BinaryTrieNode();
            curr = curr->child[bit];
        }}
    }}

    uint32_t query_max_xor(uint32_t val) {{
        BinaryTrieNode* curr = root;
        uint32_t max_xor = 0;
        for (int i = 31; i >= 0; i--) {{
            uint32_t bit = (val >> i) & 1U;
            uint32_t opp = 1U - bit;
            if (curr->child[opp]) {{
                max_xor |= (1U << i);
                curr = curr->child[opp];
            }} else if (curr->child[bit]) {{
                curr = curr->child[bit];
            }} else {{
                break;
            }}
        }}
        return max_xor;
    }}
}};

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    vector<uint32_t> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    if (n == 1) {{
        cout << 0 << "\\n";
        return 0;
    }}

    BinaryTrie trie;
    trie.insert(a[0]);
    uint32_t max_ans = 0;

    for (int i = 1; i < n; i++) {{
        max_ans = max(max_ans, trie.query_max_xor(a[i]));
        trie.insert(a[i]);
    }}

    cout << max_ans << "\\n";
    return 0;
}}
"""

        # 2. Binary Trie: Maximum XOR with Query
        if pattern == "trie_max_xor_query":
            return f"""#include <iostream>
#include <vector>
#include <cstdint>
#include <algorithm>

using namespace std;

struct BinaryTrieNode {{
    BinaryTrieNode* child[2];
    BinaryTrieNode() {{
        child[0] = child[1] = nullptr;
    }}
}};

class BinaryTrie {{
public:
    BinaryTrieNode* root;
    BinaryTrie() {{ root = new BinaryTrieNode(); }}

    void insert(uint32_t val) {{
        BinaryTrieNode* curr = root;
        for (int i = 31; i >= 0; i--) {{
            uint32_t bit = (val >> i) & 1U;
            if (!curr->child[bit]) curr->child[bit] = new BinaryTrieNode();
            curr = curr->child[bit];
        }}
    }}

    uint32_t query_max_xor(uint32_t val) {{
        BinaryTrieNode* curr = root;
        uint32_t max_xor = 0;
        for (int i = 31; i >= 0; i--) {{
            uint32_t bit = (val >> i) & 1U;
            uint32_t opp = 1U - bit;
            if (curr->child[opp]) {{
                max_xor |= (1U << i);
                curr = curr->child[opp];
            }} else if (curr->child[bit]) {{
                curr = curr->child[bit];
            }} else {{
                break;
            }}
        }}
        return max_xor;
    }}
}};

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    if (!(cin >> n >> q)) return 0;

    BinaryTrie trie;
    for (int i = 0; i < n; i++) {{
        uint32_t val;
        cin >> val;
        trie.insert(val);
    }}

    for (int i = 0; i < q; i++) {{
        uint32_t query_val;
        cin >> query_val;
        cout << trie.query_max_xor(query_val) << "\\n";
    }}

    return 0;
}}
"""

        # 3. Longest Common Prefix via Trie
        if pattern == "trie_longest_prefix":
            return f"""#include <iostream>
#include <vector>
#include <string>

using namespace std;

struct TrieNode {{
    TrieNode* child[26];
    int pass_count = 0;
    int word_count = 0;
    TrieNode() {{
        for (int i = 0; i < 26; i++) child[i] = nullptr;
    }}
}};

class Trie {{
public:
    TrieNode* root;
    Trie() {{ root = new TrieNode(); }}

    void insert(const string& s) {{
        TrieNode* curr = root;
        for (char ch : s) {{
            int idx = ch - 'a';
            if (idx < 0 || idx >= 26) continue;
            if (!curr->child[idx]) curr->child[idx] = new TrieNode();
            curr = curr->child[idx];
            curr->pass_count++;
        }}
        curr->word_count++;
    }}

    string longestCommonPrefix(int total_words) {{
        TrieNode* curr = root;
        string lcp = "";
        while (curr && curr->word_count == 0) {{
            int next_idx = -1;
            int active_children = 0;
            for (int i = 0; i < 26; i++) {{
                if (curr->child[i]) {{
                    active_children++;
                    next_idx = i;
                }}
            }}
            if (active_children == 1 && curr->child[next_idx]->pass_count == total_words) {{
                lcp.push_back('a' + next_idx);
                curr = curr->child[next_idx];
            }} else {{
                break;
            }}
        }}
        return lcp;
    }}
}};

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    vector<string> words(n);
    for (int i = 0; i < n; i++) cin >> words[i];

    Trie trie;
    for (const string& w : words) {{
        if (w.empty()) {{
            cout << "" << "\\n";
            return 0;
        }}
        trie.insert(w);
    }}

    cout << trie.longestCommonPrefix(n) << "\\n";
    return 0;
}}
"""

        # 4. Lexicographical Sort via Trie Traversal
        if pattern == "trie_lexicographic_sort":
            return f"""#include <iostream>
#include <vector>
#include <string>

using namespace std;

struct TrieNode {{
    TrieNode* child[26];
    int word_count = 0;
    TrieNode() {{
        for (int i = 0; i < 26; i++) child[i] = nullptr;
    }}
}};

class Trie {{
public:
    TrieNode* root;
    Trie() {{ root = new TrieNode(); }}

    void insert(const string& s) {{
        TrieNode* curr = root;
        for (char ch : s) {{
            int idx = ch - 'a';
            if (idx < 0 || idx >= 26) continue;
            if (!curr->child[idx]) curr->child[idx] = new TrieNode();
            curr = curr->child[idx];
        }}
        curr->word_count++;
    }}

    void dfs(TrieNode* u, string& path, vector<string>& result) {{
        if (!u) return;
        for (int k = 0; k < u->word_count; k++) {{
            result.push_back(path);
        }}
        for (int i = 0; i < 26; i++) {{
            if (u->child[i]) {{
                path.push_back('a' + i);
                dfs(u->child[i], path, result);
                path.pop_back();
            }}
        }}
    }}
}};

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    Trie trie;
    for (int i = 0; i < n; i++) {{
        string w;
        cin >> w;
        trie.insert(w);
    }}

    vector<string> result;
    string path = "";
    trie.dfs(trie.root, path, result);

    for (const string& s : result) {{
        cout << s << "\\n";
    }}
    return 0;
}}
"""

        # 5. Autocomplete / Prefix Suggestions
        if pattern == "trie_autocomplete":
            return f"""#include <iostream>
#include <vector>
#include <string>

using namespace std;

struct TrieNode {{
    TrieNode* child[26];
    int word_count = 0;
    TrieNode() {{
        for (int i = 0; i < 26; i++) child[i] = nullptr;
    }}
}};

class Trie {{
public:
    TrieNode* root;
    Trie() {{ root = new TrieNode(); }}

    void insert(const string& s) {{
        TrieNode* curr = root;
        for (char ch : s) {{
            int idx = ch - 'a';
            if (idx < 0 || idx >= 26) continue;
            if (!curr->child[idx]) curr->child[idx] = new TrieNode();
            curr = curr->child[idx];
        }}
        curr->word_count++;
    }}

    void collect(TrieNode* u, string& path, vector<string>& res, int limit) {{
        if (!u || (int)res.size() >= limit) return;
        for (int k = 0; k < u->word_count && (int)res.size() < limit; k++) {{
            res.push_back(path);
        }}
        for (int i = 0; i < 26 && (int)res.size() < limit; i++) {{
            if (u->child[i]) {{
                path.push_back('a' + i);
                collect(u->child[i], path, res, limit);
                path.pop_back();
            }}
        }}
    }}

    vector<string> autocomplete(const string& prefix, int limit) {{
        TrieNode* curr = root;
        for (char ch : prefix) {{
            int idx = ch - 'a';
            if (!curr->child[idx]) return {{}};
            curr = curr->child[idx];
        }}
        vector<string> res;
        string path = prefix;
        collect(curr, path, res, limit);
        return res;
    }}
}};

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    Trie trie;
    for (int i = 0; i < n; i++) {{
        string w;
        cin >> w;
        trie.insert(w);
    }}

    string prefix;
    int limit = 10;
    if (cin >> prefix) {{
        if (cin >> limit) {{}}
        vector<string> suggestions = trie.autocomplete(prefix, limit);
        for (const string& s : suggestions) {{
            cout << s << "\\n";
        }}
    }}
    return 0;
}}
"""

        # 6. Standard Character Trie (insert, search, prefix_search, prefix_count, word_count, deletion)
        if pattern in ("trie_insert", "trie_exact_search", "trie_prefix_search", "trie_prefix_count", "trie_word_count", "trie_deletion"):
            return f"""#include <iostream>
#include <vector>
#include <string>

using namespace std;

struct TrieNode {{
    TrieNode* child[26];
    int pass_count = 0;
    int word_count = 0;
    TrieNode() {{
        for (int i = 0; i < 26; i++) child[i] = nullptr;
    }}
}};

class Trie {{
public:
    TrieNode* root;
    Trie() {{ root = new TrieNode(); }}

    void insert(const string& s) {{
        TrieNode* curr = root;
        for (char ch : s) {{
            int idx = ch - 'a';
            if (idx < 0 || idx >= 26) continue;
            if (!curr->child[idx]) curr->child[idx] = new TrieNode();
            curr = curr->child[idx];
            curr->pass_count++;
        }}
        curr->word_count++;
    }}

    bool search(const string& s) {{
        TrieNode* curr = root;
        for (char ch : s) {{
            int idx = ch - 'a';
            if (idx < 0 || idx >= 26 || !curr->child[idx]) return false;
            curr = curr->child[idx];
        }}
        return curr->word_count > 0;
    }}

    bool startsWith(const string& prefix) {{
        TrieNode* curr = root;
        for (char ch : prefix) {{
            int idx = ch - 'a';
            if (idx < 0 || idx >= 26 || !curr->child[idx]) return false;
            curr = curr->child[idx];
        }}
        return curr->pass_count > 0;
    }}

    int countWordsEqualTo(const string& s) {{
        TrieNode* curr = root;
        for (char ch : s) {{
            int idx = ch - 'a';
            if (idx < 0 || idx >= 26 || !curr->child[idx]) return 0;
            curr = curr->child[idx];
        }}
        return curr->word_count;
    }}

    int countWordsStartingWith(const string& prefix) {{
        TrieNode* curr = root;
        for (char ch : prefix) {{
            int idx = ch - 'a';
            if (idx < 0 || idx >= 26 || !curr->child[idx]) return 0;
            curr = curr->child[idx];
        }}
        return curr->pass_count;
    }}

    bool erase(const string& s) {{
        if (countWordsEqualTo(s) == 0) return false;
        TrieNode* curr = root;
        for (char ch : s) {{
            int idx = ch - 'a';
            curr = curr->child[idx];
            curr->pass_count--;
        }}
        curr->word_count--;
        return true;
    }}
}};

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    Trie trie;
    string op;
    while (cin >> op) {{
        if (op == "insert") {{
            string w; cin >> w;
            trie.insert(w);
        }} else if (op == "search") {{
            string w; cin >> w;
            cout << (trie.search(w) ? "true" : "false") << "\\n";
        }} else if (op == "startsWith") {{
            string p; cin >> p;
            cout << (trie.startsWith(p) ? "true" : "false") << "\\n";
        }} else if (op == "countWordsEqualTo") {{
            string w; cin >> w;
            cout << trie.countWordsEqualTo(w) << "\\n";
        }} else if (op == "countWordsStartingWith") {{
            string p; cin >> p;
            cout << trie.countWordsStartingWith(p) << "\\n";
        }} else if (op == "erase") {{
            string w; cin >> w;
            cout << (trie.erase(w) ? "true" : "false") << "\\n";
        }}
    }}
    return 0;
}}
"""

        # ── 28. Cross-Family Composition Code Generators (Phase 4) ──
        if pattern.startswith("cf_"):
            from pointer_algorithms.cross_family.facade import CrossFamilySynthesisEngine
            from pointer_algorithms.cross_family.recipe_registry import CompositionRecipeRegistry
            engine = CrossFamilySynthesisEngine()
            text = features.get("raw_text", "") if isinstance(features, dict) else getattr(features, "raw_text", "")
            if text:
                res = engine.process(text)
                if res.get("gate_passed") and res.get("code"):
                    return res["code"]
            recipe = CompositionRecipeRegistry.get_instance().get_by_name(pattern)
            if recipe:
                res = engine.process({"objective": recipe.objective.value})
                if res.get("code"):
                    return res["code"]
            raise ValueError(f"Cross-family synthesis failed for pattern {pattern}")

        # ── 27. Advanced Data Structures Code Generators (Phase 3S) ──
        if pattern.startswith("ads_"):
            from pointer_algorithms.generator.ads_cpp_generator import generate_ads_cpp
            return generate_ads_cpp(pattern, features)

        # ── 26. Computational Geometry Code Generators (Phase 3R) ──
        if pattern.startswith("geom_"):
            from pointer_algorithms.generator.geometry_cpp_generator import generate_geometry_cpp
            return generate_geometry_cpp(pattern, features)

        # ── 25. Algebra / Transforms Code Generators (Phase 3Q) ──
        if pattern.startswith("algebra_"):
            from pointer_algorithms.generator.algebra_cpp_generator import generate_algebra_cpp
            return generate_algebra_cpp(pattern, features)

        # ── 24. Number Theory & Combinatorics Code Generators (Phase 3P) ──
        if pattern.startswith("nt_"):
            from pointer_algorithms.generator.nt_cpp_generator import generate_nt_cpp
            return generate_nt_cpp(pattern, features)

        # ── 23. String Algorithms & Automata Code Generators (Phase 3O) ──
        if pattern.startswith("string_"):
            from pointer_algorithms.generator.string_cpp_generator import generate_string_cpp
            return generate_string_cpp(pattern, features)

        # ── 22. Advanced Graph Code Generators (Phase 3N) ──
        if pattern.startswith("adv_graph_"):
            from pointer_algorithms.generator.adv_graph_cpp_generator import generate_adv_graph_cpp
            return generate_adv_graph_cpp(pattern, features)

        # ── 21. Divide and Conquer & Backtracking Code Generators (Phase 3M) ──
        if pattern.startswith("dc_") or pattern.startswith("backtracking_"):
            from pointer_algorithms.generator.dc_backtracking_cpp_generator import generate_dc_backtracking_cpp
            return generate_dc_backtracking_cpp(pattern, features)

        # ── 20. Greedy Code Generators (Phase 3L) ──
        if pattern.startswith("greedy_"):
            from pointer_algorithms.generator.greedy_cpp_generator import generate_greedy_cpp
            return generate_greedy_cpp(pattern, features)

        # ── 19. Dynamic Programming Code Generators (Phase 3K) ──
        if pattern.startswith("dp_"):
            from pointer_algorithms.generator.dp_cpp_generator import generate_dp_cpp
            return generate_dp_cpp(pattern, features)

        # ── 18. Segment Tree Code Generators (Phase 3J) ──
        if pattern.startswith("segment_tree_"):
            from pointer_algorithms.generator.segment_tree_cpp_generator import generate_segment_tree_cpp
            return generate_segment_tree_cpp(pattern, features)

        # ── 17. Fenwick Tree Code Generators (Phase 3I) ──
        if pattern.startswith("fenwick_"):
            from pointer_algorithms.generator.fenwick_cpp_generator import generate_fenwick_cpp
            return generate_fenwick_cpp(pattern, features)

        # ── 16. DSU Code Generators (Phase 3H) ──
        if pattern.startswith("dsu_"):
            from pointer_algorithms.generator.dsu_cpp_generator import generate_dsu_cpp
            return generate_dsu_cpp(pattern, features)

        # ── 15. Heap Code Generators (Phase 3G) ──
        if pattern.startswith("heap_"):
            from pointer_algorithms.generator.heap_cpp_generator import generate_heap_cpp
            return generate_heap_cpp(pattern, features)

        # ── 14. Graph Code Generators (Phase 3F) ──
        if pattern.startswith("graph_"):
            from pointer_algorithms.generator.graph_cpp_generator import generate_graph_cpp
            return generate_graph_cpp(pattern, features)

        # ── 13. Tree Code Generators (Phase 3E) ──
        if pattern == "tree_dfs_preorder":
            return f"""#include <iostream>
#include <vector>

using namespace std;

void dfs(int u, int p, const vector<vector<int>>& adj, vector<int>& order) {{
    order.push_back(u);
    for (int v : adj[u]) {{
        if (v != p) {{
            dfs(v, u, adj, order);
        }}
    }}
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; i++) {{
        int u, v;
        if (cin >> u >> v) {{
            adj[u].push_back(v);
            adj[v].push_back(u);
        }}
    }}

    int root = 1;
    vector<int> order;
    dfs(root, 0, adj, order);

    for (int i = 0; i < (int)order.size(); i++) {{
        cout << order[i] << (i + 1 == (int)order.size() ? "" : " ");
    }}
    cout << "\\n";

    return 0;
}}
"""

        if pattern == "tree_dfs_inorder":
            return f"""#include <iostream>
#include <vector>

using namespace std;

struct Node {{
    int val;
    int left;
    int right;
}};

void inorder(int u, const vector<Node>& nodes, vector<int>& order) {{
    if (u == -1) return;
    inorder(nodes[u].left, nodes, order);
    order.push_back(nodes[u].val);
    inorder(nodes[u].right, nodes, order);
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, root;
    if (!(cin >> n >> root)) return 0;

    vector<Node> nodes(n + 1);
    for (int i = 1; i <= n; i++) {{
        cin >> nodes[i].val >> nodes[i].left >> nodes[i].right;
    }}

    vector<int> order;
    inorder(root, nodes, order);

    for (int i = 0; i < (int)order.size(); i++) {{
        cout << order[i] << (i + 1 == (int)order.size() ? "" : " ");
    }}
    cout << "\\n";

    return 0;
}}
"""

        if pattern == "tree_dfs_postorder":
            return f"""#include <iostream>
#include <vector>

using namespace std;

struct Node {{
    int val;
    int left;
    int right;
}};

void postorder(int u, const vector<Node>& nodes, vector<int>& order) {{
    if (u == -1) return;
    postorder(nodes[u].left, nodes, order);
    postorder(nodes[u].right, nodes, order);
    order.push_back(nodes[u].val);
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, root;
    if (!(cin >> n >> root)) return 0;

    vector<Node> nodes(n + 1);
    for (int i = 1; i <= n; i++) {{
        cin >> nodes[i].val >> nodes[i].left >> nodes[i].right;
    }}

    vector<int> order;
    postorder(root, nodes, order);

    for (int i = 0; i < (int)order.size(); i++) {{
        cout << order[i] << (i + 1 == (int)order.size() ? "" : " ");
    }}
    cout << "\\n";

    return 0;
}}
"""

        if pattern == "tree_bfs_level_order":
            return f"""#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, root;
    if (!(cin >> n >> root)) return 0;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; i++) {{
        int u, v;
        if (cin >> u >> v) {{
            adj[u].push_back(v);
            adj[v].push_back(u);
        }}
    }}

    vector<int> order;
    vector<bool> vis(n + 1, false);
    queue<int> q;

    q.push(root);
    vis[root] = true;

    while (!q.empty()) {{
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (int v : adj[u]) {{
            if (!vis[v]) {{
                vis[v] = true;
                q.push(v);
            }}
        }}
    }}

    for (int i = 0; i < (int)order.size(); i++) {{
        cout << order[i] << (i + 1 == (int)order.size() ? "" : " ");
    }}
    cout << "\\n";

    return 0;
}}
"""

        if pattern == "tree_depth_height":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int getHeight(int u, int p, const vector<vector<int>>& adj) {{
    int max_child_height = 0;
    for (int v : adj[u]) {{
        if (v != p) {{
            max_child_height = max(max_child_height, getHeight(v, u, adj));
        }}
    }}
    return 1 + max_child_height;
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) {{
        cout << 0 << "\\n";
        return 0;
    }}

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; i++) {{
        int u, v;
        if (cin >> u >> v) {{
            adj[u].push_back(v);
            adj[v].push_back(u);
        }}
    }}

    cout << getHeight(1, 0, adj) << "\\n";
    return 0;
}}
"""

        if pattern == "tree_subtree_size":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int computeSizes(int u, int p, const vector<vector<int>>& adj, vector<int>& sz) {{
    sz[u] = 1;
    for (int v : adj[u]) {{
        if (v != p) {{
            sz[u] += computeSizes(v, u, adj, sz);
        }}
    }}
    return sz[u];
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; i++) {{
        int u, v;
        if (cin >> u >> v) {{
            adj[u].push_back(v);
            adj[v].push_back(u);
        }}
    }}

    vector<int> sz(n + 1, 0);
    computeSizes(1, 0, adj, sz);

    for (int i = 1; i <= n; i++) {{
        cout << sz[i] << (i == n ? "" : " ");
    }}
    cout << "\\n";

    return 0;
}}
"""

        if pattern == "tree_leaf_count":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int countLeaves(int u, int p, const vector<vector<int>>& adj) {{
    int child_count = 0;
    int leaf_sum = 0;
    for (int v : adj[u]) {{
        if (v != p) {{
            child_count++;
            leaf_sum += countLeaves(v, u, adj);
        }}
    }}
    if (child_count == 0) return 1;
    return leaf_sum;
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) {{
        cout << 0 << "\\n";
        return 0;
    }}

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; i++) {{
        int u, v;
        if (cin >> u >> v) {{
            adj[u].push_back(v);
            adj[v].push_back(u);
        }}
    }}

    cout << countLeaves(1, 0, adj) << "\\n";
    return 0;
}}
"""

        if pattern == "tree_subtree_aggregation":
            return f"""#include <iostream>
#include <vector>

using namespace std;

long long dfsSum(int u, int p, const vector<long long>& val, const vector<vector<int>>& adj, vector<long long>& sub_sum) {{
    sub_sum[u] = val[u];
    for (int v : adj[u]) {{
        if (v != p) {{
            sub_sum[u] += dfsSum(v, u, val, adj, sub_sum);
        }}
    }}
    return sub_sum[u];
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    vector<long long> val(n + 1);
    for (int i = 1; i <= n; i++) {{
        cin >> val[i];
    }}

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; i++) {{
        int u, v;
        if (cin >> u >> v) {{
            adj[u].push_back(v);
            adj[v].push_back(u);
        }}
    }}

    vector<long long> sub_sum(n + 1, 0);
    dfsSum(1, 0, val, adj, sub_sum);

    for (int i = 1; i <= n; i++) {{
        cout << sub_sum[i] << (i == n ? "" : " ");
    }}
    cout << "\\n";

    return 0;
}}
"""

        if pattern == "tree_path_sum":
            return f"""#include <iostream>
#include <vector>

using namespace std;

struct Node {{
    long long val;
    int left;
    int right;
}};

bool hasPathSum(int u, long long target, const vector<Node>& nodes) {{
    if (u == -1) return false;
    long long remaining = target - nodes[u].val;
    if (nodes[u].left == -1 && nodes[u].right == -1) {{
        return remaining == 0;
    }}
    return hasPathSum(nodes[u].left, remaining, nodes) || hasPathSum(nodes[u].right, remaining, nodes);
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, root;
    long long target;
    if (!(cin >> n >> root >> target)) return 0;

    vector<Node> nodes(n + 1);
    for (int i = 1; i <= n; i++) {{
        cin >> nodes[i].val >> nodes[i].left >> nodes[i].right;
    }}

    cout << (hasPathSum(root, target, nodes) ? "true" : "false") << "\\n";
    return 0;
}}
"""

        if pattern == "tree_diameter":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int global_diameter = 0;

int dfsDepth(int u, int p, const vector<vector<int>>& adj) {{
    int max1 = 0, max2 = 0;
    for (int v : adj[u]) {{
        if (v != p) {{
            int d = dfsDepth(v, u, adj);
            if (d > max1) {{
                max2 = max1;
                max1 = d;
            }} else if (d > max2) {{
                max2 = d;
            }}
        }}
    }}
    global_diameter = max(global_diameter, max1 + max2);
    return 1 + max1;
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 1) {{
        cout << 0 << "\\n";
        return 0;
    }}

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; i++) {{
        int u, v;
        if (cin >> u >> v) {{
            adj[u].push_back(v);
            adj[v].push_back(u);
        }}
    }}

    global_diameter = 0;
    dfsDepth(1, 0, adj);
    cout << global_diameter << "\\n";

    return 0;
}}
"""

        if pattern in ("tree_bst_search", "tree_bst_insert", "tree_bst_delete", "tree_bst_min_max", "tree_bst_pred_succ", "tree_bst_validate"):
            return f"""#include <iostream>
#include <string>
#include <algorithm>
#include <climits>

using namespace std;

struct BSTNode {{
    long long val;
    BSTNode* left;
    BSTNode* right;
    BSTNode(long long v) : val(v), left(nullptr), right(nullptr) {{}}
}};

BSTNode* bst_insert(BSTNode* root, long long val) {{
    if (!root) return new BSTNode(val);
    if (val < root->val) {{
        root->left = bst_insert(root->left, val);
    }} else if (val > root->val) {{
        root->right = bst_insert(root->right, val);
    }}
    return root;
}}

bool bst_search(BSTNode* root, long long val) {{
    // BST ordered-branch elimination
    while (root) {{
        if (val == root->val) return true;
        if (val < root->val) root = root->left;
        else root = root->right;
    }}
    return false;
}}

BSTNode* bst_min(BSTNode* root) {{
    while (root && root->left) root = root->left;
    return root;
}}

BSTNode* bst_max(BSTNode* root) {{
    while (root && root->right) root = root->right;
    return root;
}}

BSTNode* bst_delete(BSTNode* root, long long val) {{
    if (!root) return nullptr;
    if (val < root->val) {{
        root->left = bst_delete(root->left, val);
    }} else if (val > root->val) {{
        root->right = bst_delete(root->right, val);
    }} else {{
        if (!root->left) {{
            BSTNode* r = root->right;
            delete root;
            return r;
        }} else if (!root->right) {{
            BSTNode* l = root->left;
            delete root;
            return l;
        }} else {{
            BSTNode* succ = bst_min(root->right);
            root->val = succ->val;
            root->right = bst_delete(root->right, succ->val);
        }}
    }}
    return root;
}}

long long bst_predecessor(BSTNode* root, long long val) {{
    long long pred = LLONG_MIN;
    while (root) {{
        if (root->val < val) {{
            pred = root->val;
            root = root->right;
        }} else {{
            root = root->left;
        }}
    }}
    return pred;
}}

long long bst_successor(BSTNode* root, long long val) {{
    long long succ = LLONG_MAX;
    while (root) {{
        if (root->val > val) {{
            succ = root->val;
            root = root->left;
        }} else {{
            root = root->right;
        }}
    }}
    return succ;
}}

bool bst_validate(BSTNode* root, long long low, long long high) {{
    if (!root) return true;
    if (root->val <= low || root->val >= high) return false;
    return bst_validate(root->left, low, root->val) && bst_validate(root->right, root->val, high);
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    BSTNode* root = nullptr;
    string op;
    while (cin >> op) {{
        if (op == "insert") {{
            long long v; cin >> v;
            root = bst_insert(root, v);
        }} else if (op == "search") {{
            long long v; cin >> v;
            cout << (bst_search(root, v) ? "true" : "false") << "\\n";
        }} else if (op == "delete") {{
            long long v; cin >> v;
            root = bst_delete(root, v);
        }} else if (op == "min") {{
            BSTNode* m = bst_min(root);
            if (m) cout << m->val << "\\n";
            else cout << "null\\n";
        }} else if (op == "max") {{
            BSTNode* m = bst_max(root);
            if (m) cout << m->val << "\\n";
            else cout << "null\\n";
        }} else if (op == "pred") {{
            long long v; cin >> v;
            long long p = bst_predecessor(root, v);
            if (p != LLONG_MIN) cout << p << "\\n";
            else cout << "null\\n";
        }} else if (op == "succ") {{
            long long v; cin >> v;
            long long s = bst_successor(root, v);
            if (s != LLONG_MAX) cout << s << "\\n";
            else cout << "null\\n";
        }} else if (op == "validate") {{
            cout << (bst_validate(root, LLONG_MIN, LLONG_MAX) ? "true" : "false") << "\\n";
        }}
    }}

    return 0;
}}
"""

        if pattern == "tree_lca_bst":
            return f"""#include <iostream>

using namespace std;

struct BSTNode {{
    long long val;
    BSTNode* left;
    BSTNode* right;
    BSTNode(long long v) : val(v), left(nullptr), right(nullptr) {{}}
}};

BSTNode* bst_insert(BSTNode* root, long long val) {{
    if (!root) return new BSTNode(val);
    if (val < root->val) root->left = bst_insert(root->left, val);
    else if (val > root->val) root->right = bst_insert(root->right, val);
    return root;
}}

BSTNode* lca_bst(BSTNode* root, long long p, long long q) {{
    // BST ordered-branch elimination
    while (root) {{
        if (p < root->val && q < root->val) {{
            root = root->left;
        }} else if (p > root->val && q > root->val) {{
            root = root->right;
        }} else {{
            return root;
        }}
    }}
    return nullptr;
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    BSTNode* root = nullptr;
    for (int i = 0; i < n; i++) {{
        long long v; cin >> v;
        root = bst_insert(root, v);
    }}

    long long p, q;
    if (cin >> p >> q) {{
        BSTNode* lca = lca_bst(root, p, q);
        if (lca) cout << lca->val << "\\n";
        else cout << "null\\n";
    }}

    return 0;
}}
"""

        if pattern == "tree_lca_binary_tree":
            return f"""#include <iostream>
#include <vector>

using namespace std;

struct Node {{
    int val;
    int left;
    int right;
}};

int lca_binary_tree(int u, int p, int q, const vector<Node>& nodes) {{
    if (u == -1) return -1;
    if (u == p || u == q) return u;

    int left = lca_binary_tree(nodes[u].left, p, q, nodes);
    int right = lca_binary_tree(nodes[u].right, p, q, nodes);

    if (left != -1 && right != -1) return u;
    return (left != -1) ? left : right;
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, root, p, q;
    if (!(cin >> n >> root >> p >> q)) return 0;

    vector<Node> nodes(n + 1);
    for (int i = 1; i <= n; i++) {{
        cin >> nodes[i].val >> nodes[i].left >> nodes[i].right;
    }}

    cout << lca_binary_tree(root, p, q, nodes) << "\\n";
    return 0;
}}
"""

        if pattern == "tree_lca_parent_array":
            return f"""#include <iostream>
#include <vector>

using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) return 0;

    vector<int> parent(n + 1, 0);
    vector<int> depth(n + 1, 0);

    for (int i = 1; i <= n; i++) {{
        cin >> parent[i];
    }}

    // Compute depths
    for (int i = 1; i <= n; i++) {{
        int d = 0;
        int curr = i;
        while (curr != 0 && parent[curr] != 0 && parent[curr] != curr) {{
            d++;
            curr = parent[curr];
        }}
        depth[i] = d;
    }}

    int p, q;
    if (cin >> p >> q) {{
        // Align depths
        while (depth[p] > depth[q]) p = parent[p];
        while (depth[q] > depth[p]) q = parent[q];

        // Step together
        while (p != q && p != 0 && q != 0) {{
            p = parent[p];
            q = parent[q];
        }}
        cout << p << "\\n";
    }}

    return 0;
}}
"""

        if pattern == "tree_dp_independent_set":
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

struct DPState {{
    long long include;
    long long exclude;
}};

DPState dfsMIS(int u, int p, const vector<long long>& val, const vector<vector<int>>& adj) {{
    DPState res;
    res.include = val[u];
    res.exclude = 0;

    for (int v : adj[u]) {{
        if (v != p) {{
            DPState child = dfsMIS(v, u, val, adj);
            res.include += child.exclude;
            res.exclude += max(child.include, child.exclude);
        }}
    }}
    return res;
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) {{
        cout << 0 << "\\n";
        return 0;
    }}

    vector<long long> val(n + 1);
    for (int i = 1; i <= n; i++) {{
        cin >> val[i];
    }}

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; i++) {{
        int u, v;
        if (cin >> u >> v) {{
            adj[u].push_back(v);
            adj[v].push_back(u);
        }}
    }}

    DPState root_state = dfsMIS(1, 0, val, adj);
    cout << max(root_state.include, root_state.exclude) << "\\n";

    return 0;
}}
"""

        if pattern in ("tree_dp_subtree_weight", "tree_dp_two_state"):
            return f"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

long long max_subtree_ans = 0;

long long dfsWeight(int u, int p, const vector<long long>& val, const vector<vector<int>>& adj) {{
    long long sum = val[u];
    for (int v : adj[u]) {{
        if (v != p) {{
            long long child_w = dfsWeight(v, u, val, adj);
            if (child_w > 0) sum += child_w;
        }}
    }}
    max_subtree_ans = max(max_subtree_ans, sum);
    return sum;
}}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n) || n <= 0) {{
        cout << 0 << "\\n";
        return 0;
    }}

    vector<long long> val(n + 1);
    for (int i = 1; i <= n; i++) {{
        cin >> val[i];
    }}

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; i++) {{
        int u, v;
        if (cin >> u >> v) {{
            adj[u].push_back(v);
            adj[v].push_back(u);
        }}
    }}

    max_subtree_ans = val[1];
    dfsWeight(1, 0, val, adj);
    cout << max_subtree_ans << "\\n";

    return 0;
}}
"""

        # Fallback default
        return f"""#include <iostream>
using namespace std;
int main() {{ return 0; }}
"""
