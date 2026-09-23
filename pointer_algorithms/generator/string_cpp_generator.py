"""
CHUP Phase 3O — String Algorithms & Automata C++ Generator.

Generates complete, standalone, production-ready C++17 source code for the 10 Phase 3O patterns:
1. string_kmp_search
2. string_z_algorithm
3. string_rabin_karp
4. string_manacher
5. string_aho_corasick
6. string_suffix_array
7. string_suffix_automaton
8. string_lyndon_duval
9. string_subsequence_automaton
10. string_longest_common_substring_sam
"""

from typing import Dict, Any


def generate_string_cpp(pattern: str, params: Dict[str, Any]) -> str:
    """
    Generates standalone C++17 code for string and automata algorithms.
    """
    if pattern == "string_kmp_search":
        return r"""#include <iostream>
#include <vector>
#include <string>

using namespace std;

vector<int> compute_pi(const string& p) {
    int m = p.size();
    vector<int> pi(m, 0);
    for (int i = 1; i < m; ++i) {
        int j = pi[i - 1];
        while (j > 0 && p[i] != p[j]) j = pi[j - 1];
        if (p[i] == p[j]) j++;
        pi[i] = j;
    }
    return pi;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string text, pattern;
    if (!(cin >> text >> pattern)) return 0;

    int n = text.size(), m = pattern.size();
    if (m == 0 || n < m) return 0;

    vector<int> pi = compute_pi(pattern);
    vector<int> matches;

    int j = 0;
    for (int i = 0; i < n; ++i) {
        while (j > 0 && text[i] != pattern[j]) j = pi[j - 1];
        if (text[i] == pattern[j]) j++;
        if (j == m) {
            matches.push_back(i - m + 1);
            j = pi[j - 1];
        }
    }

    for (size_t i = 0; i < matches.size(); ++i) {
        cout << matches[i] << (i + 1 == matches.size() ? "" : " ");
    }
    cout << "\n";
    return 0;
}
"""

    if pattern == "string_z_algorithm":
        return r"""#include <iostream>
#include <vector>
#include <string>

using namespace std;

vector<int> compute_z(const string& s) {
    int n = s.size();
    vector<int> z(n, 0);
    z[0] = n;
    int l = 0, r = 0;
    for (int i = 1; i < n; ++i) {
        if (i <= r) z[i] = min(r - i + 1, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
        if (i + z[i] - 1 > r) {
            l = i;
            r = i + z[i] - 1;
        }
    }
    return z;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string s;
    if (!(cin >> s)) return 0;

    vector<int> z = compute_z(s);
    for (size_t i = 0; i < z.size(); ++i) {
        cout << z[i] << (i + 1 == z.size() ? "" : " ");
    }
    cout << "\n";
    return 0;
}
"""

    if pattern == "string_rabin_karp":
        return r"""#include <iostream>
#include <vector>
#include <string>

using namespace std;

typedef long long ll;

const ll MOD1 = 1000000007;
const ll MOD2 = 1000000009;
const ll BASE1 = 313;
const ll BASE2 = 317;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string text, pattern;
    if (!(cin >> text >> pattern)) return 0;

    int n = text.size(), m = pattern.size();
    if (m == 0 || n < m) return 0;

    vector<ll> p1(n + 1, 1), p2(n + 1, 1);
    vector<ll> h1(n + 1, 0), h2(n + 1, 0);

    for (int i = 0; i < n; ++i) {
        p1[i + 1] = (p1[i] * BASE1) % MOD1;
        p2[i + 1] = (p2[i] * BASE2) % MOD2;
        h1[i + 1] = (h1[i] * BASE1 + text[i]) % MOD1;
        h2[i + 1] = (h2[i] * BASE2 + text[i]) % MOD2;
    }

    ll pat_h1 = 0, pat_h2 = 0;
    for (char c : pattern) {
        pat_h1 = (pat_h1 * BASE1 + c) % MOD1;
        pat_h2 = (pat_h2 * BASE2 + c) % MOD2;
    }

    vector<int> matches;
    for (int i = 0; i <= n - m; ++i) {
        ll cur1 = (h1[i + m] - (h1[i] * p1[m]) % MOD1 + MOD1) % MOD1;
        ll cur2 = (h2[i + m] - (h2[i] * p2[m]) % MOD2 + MOD2) % MOD2;
        if (cur1 == pat_h1 && cur2 == pat_h2) {
            matches.push_back(i);
        }
    }

    for (size_t i = 0; i < matches.size(); ++i) {
        cout << matches[i] << (i + 1 == matches.size() ? "" : " ");
    }
    cout << "\n";
    return 0;
}
"""

    if pattern == "string_manacher":
        return r"""#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string s;
    if (!(cin >> s)) return 0;
    if (s.empty()) return 0;

    string t = "^";
    for (char c : s) {
        t += "#";
        t += c;
    }
    t += "#$";

    int m = t.size();
    vector<int> p(m, 0);
    int c = 0, r = 0;

    int max_len = 0;
    int center_index = 0;

    for (int i = 1; i < m - 1; ++i) {
        int i_mirror = 2 * c - i;
        if (r > i) {
            p[i] = min(r - i, p[i_mirror]);
        }
        while (t[i + 1 + p[i]] == t[i - 1 - p[i]]) {
            p[i]++;
        }
        if (i + p[i] > r) {
            c = i;
            r = i + p[i];
        }
        if (p[i] > max_len) {
            max_len = p[i];
            center_index = i;
        }
    }

    int start = (center_index - max_len) / 2;
    string lps = s.substr(start, max_len);

    cout << max_len << "\n";
    cout << lps << "\n";
    return 0;
}
"""

    if pattern == "string_aho_corasick":
        return r"""#include <iostream>
#include <vector>
#include <string>
#include <queue>
#include <map>

using namespace std;

struct Node {
    map<char, int> next;
    int link = 0;
    int dict_link = 0;
    vector<int> pattern_ids;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int k;
    if (!(cin >> k)) return 0;

    vector<string> patterns(k);
    vector<Node> trie(1);

    for (int i = 0; i < k; ++i) {
        cin >> patterns[i];
        int v = 0;
        for (char c : patterns[i]) {
            if (!trie[v].next.count(c)) {
                trie[v].next[c] = trie.size();
                trie.emplace_back();
            }
            v = trie[v].next[c];
        }
        trie[v].pattern_ids.push_back(i);
    }

    queue<int> q;
    for (auto& edge : trie[0].next) {
        q.push(edge.second);
    }

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        int p = trie[u].link;
        if (!trie[p].pattern_ids.empty()) {
            trie[u].dict_link = p;
        } else {
            trie[u].dict_link = trie[p].dict_link;
        }

        for (auto& edge : trie[u].next) {
            char c = edge.first;
            int v = edge.second;
            int f = trie[u].link;
            while (f > 0 && !trie[f].next.count(c)) {
                f = trie[f].link;
            }
            if (trie[f].next.count(c)) f = trie[f].next[c];
            trie[v].link = f;
            q.push(v);
        }
    }

    string text;
    cin >> text;

    vector<int> counts(k, 0);
    int curr = 0;

    for (char c : text) {
        while (curr > 0 && !trie[curr].next.count(c)) {
            curr = trie[curr].link;
        }
        if (trie[curr].next.count(c)) {
            curr = trie[curr].next[c];
        }

        int temp = curr;
        while (temp > 0) {
            for (int pid : trie[temp].pattern_ids) {
                counts[pid]++;
            }
            temp = trie[temp].dict_link;
        }
    }

    for (int i = 0; i < k; ++i) {
        cout << counts[i] << "\n";
    }
    return 0;
}
"""

    if pattern == "string_suffix_array":
        return r"""#include <iostream>
#include <vector>
#include <string>
#include <numeric>
#include <algorithm>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string s;
    if (!(cin >> s)) return 0;
    int n = s.size();

    vector<int> sa(n), rank(n);
    for (int i = 0; i < n; ++i) {
        sa[i] = i;
        rank[i] = s[i];
    }

    for (int k = 1; k < n; k <<= 1) {
        auto cmp = [&](int i, int j) {
            if (rank[i] != rank[j]) return rank[i] < rank[j];
            int ri = (i + k < n) ? rank[i + k] : -1;
            int rj = (j + k < n) ? rank[j + k] : -1;
            return ri < rj;
        };
        sort(sa.begin(), sa.end(), cmp);

        vector<int> temp(n, 0);
        for (int i = 1; i < n; ++i) {
            temp[i] = temp[i - 1] + (cmp(sa[i - 1], sa[i]) ? 1 : 0);
        }
        for (int i = 0; i < n; ++i) {
            rank[sa[i]] = temp[i];
        }
        if (temp[n - 1] == n - 1) break;
    }

    // Normalize initial rank for n == 1
    if (n == 1) {
        rank[0] = 0;
    }

    // Kasai LCP calculation
    vector<int> lcp(max(0, n - 1), 0);
    if (n > 1) {
        int h = 0;
        for (int i = 0; i < n; ++i) {
            int r = rank[i];
            if (r > 0 && r - 1 < (int)lcp.size()) {
                int j = sa[r - 1];
                while (i + h < n && j + h < n && s[i + h] == s[j + h]) h++;
                lcp[r - 1] = h;
                if (h > 0) h--;
            }
        }
    }

    for (int i = 0; i < n; ++i) {
        cout << sa[i] << (i + 1 == n ? "" : " ");
    }
    cout << "\n";

    for (size_t i = 0; i < lcp.size(); ++i) {
        cout << lcp[i] << (i + 1 == lcp.size() ? "" : " ");
    }
    cout << "\n";
    return 0;
}
"""

    if pattern == "string_suffix_automaton":
        return r"""#include <iostream>
#include <vector>
#include <string>
#include <map>

using namespace std;

typedef long long ll;

struct State {
    int len = 0;
    int link = -1;
    map<char, int> next;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string s;
    if (!(cin >> s)) return 0;

    int n = s.size();
    vector<State> st;
    st.emplace_back(); // root state 0
    int last = 0;

    for (char c : s) {
        int cur = st.size();
        st.emplace_back();
        st[cur].len = st[last].len + 1;

        int p = last;
        while (p != -1 && !st[p].next.count(c)) {
            st[p].next[c] = cur;
            p = st[p].link;
        }

        if (p == -1) {
            st[cur].link = 0;
        } else {
            int q = st[p].next[c];
            if (st[p].len + 1 == st[q].len) {
                st[cur].link = q;
            } else {
                int clone = st.size();
                st.push_back(st[q]);
                st[clone].len = st[p].len + 1;
                while (p != -1 && st[p].next[c] == q) {
                    st[p].next[c] = clone;
                    p = st[p].link;
                }
                st[q].link = st[cur].link = clone;
            }
        }
        last = cur;
    }

    // Direct mathematical invariant: distinct substrings = sum_{v != 0} (len[v] - len[link[v]])
    ll distinct_count = 0;
    for (size_t v = 1; v < st.size(); ++v) {
        distinct_count += (st[v].len - st[st[v].link].len);
    }

    cout << distinct_count << "\n";
    return 0;
}
"""

    if pattern == "string_lyndon_duval":
        return r"""#include <iostream>
#include <string>

using namespace std;

// Duval's algorithm to find lexicographically minimal cyclic shift in O(N) time and O(1) space
int minimal_rotation(string s) {
    int n = s.size();
    s += s;
    int i = 0, ans = 0;
    while (i < n) {
        ans = i;
        int j = i + 1, k = i;
        while (j < 2 * n && s[k] <= s[j]) {
            if (s[k] < s[j]) k = i;
            else k++;
            j++;
        }
        while (i <= k) i += j - k;
    }
    return ans;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string s;
    if (!(cin >> s)) return 0;

    int idx = minimal_rotation(s);
    int n = s.size();
    string res = s.substr(idx, n - idx) + s.substr(0, idx);
    cout << res << "\n";
    return 0;
}
"""

    if pattern == "string_subsequence_automaton":
        return r"""#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string s;
    if (!(cin >> s)) return 0;

    int q_count;
    if (!(cin >> q_count)) return 0;

    int n = s.size();
    // 26 lowercase alphabet transitions (dense representation)
    vector<vector<int>> next_pos(n + 1, vector<int>(26, -1));

    for (int i = n - 1; i >= 0; --i) {
        for (int c = 0; c < 26; ++c) {
            next_pos[i][c] = next_pos[i + 1][c];
        }
        next_pos[i][s[i] - 'a'] = i;
    }

    while (q_count--) {
        string q;
        cin >> q;
        int cur = 0;
        bool ok = true;
        for (char c : q) {
            int char_idx = c - 'a';
            if (char_idx < 0 || char_idx >= 26 || cur > n || next_pos[cur][char_idx] == -1) {
                ok = false;
                break;
            }
            cur = next_pos[cur][char_idx] + 1;
        }
        cout << (ok ? "YES" : "NO") << "\n";
    }
    return 0;
}
"""

    if pattern == "string_longest_common_substring_sam":
        return r"""#include <iostream>
#include <vector>
#include <string>
#include <map>

using namespace std;

struct State {
    int len = 0;
    int link = -1;
    map<char, int> next;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string s1, s2;
    if (!(cin >> s1 >> s2)) return 0;

    vector<State> st;
    st.emplace_back();
    int last = 0;

    for (char c : s1) {
        int cur = st.size();
        st.emplace_back();
        st[cur].len = st[last].len + 1;

        int p = last;
        while (p != -1 && !st[p].next.count(c)) {
            st[p].next[c] = cur;
            p = st[p].link;
        }

        if (p == -1) {
            st[cur].link = 0;
        } else {
            int q = st[p].next[c];
            if (st[p].len + 1 == st[q].len) {
                st[cur].link = q;
            } else {
                int clone = st.size();
                st.push_back(st[q]);
                st[clone].len = st[p].len + 1;
                while (p != -1 && st[p].next[c] == q) {
                    st[p].next[c] = clone;
                    p = st[p].link;
                }
                st[q].link = st[cur].link = clone;
            }
        }
        last = cur;
    }

    // Traverse s2 on SAM of s1
    int v = 0, l = 0;
    int best_len = 0, best_pos = 0;

    for (int i = 0; i < (int)s2.size(); ++i) {
        char c = s2[i];
        while (v != 0 && !st[v].next.count(c)) {
            v = st[v].link;
            l = st[v].len;
        }
        if (st[v].next.count(c)) {
            v = st[v].next[c];
            l++;
        }
        if (l > best_len) {
            best_len = l;
            best_pos = i;
        }
    }

    cout << best_len << "\n";
    if (best_len > 0) {
        cout << s2.substr(best_pos - best_len + 1, best_len) << "\n";
    } else {
        cout << "\n";
    }
    return 0;
}
"""

    return "// Unsupported string pattern\n"
