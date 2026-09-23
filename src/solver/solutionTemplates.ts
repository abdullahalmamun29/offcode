/**
 * CHUP V2 — Parameterized C++ Solution Templates.
 *
 * Each template takes problem-specific parameters and produces a CodeFragment
 * (reusing v1's interface from codeComposer.ts) that assembles into complete,
 * compilable C++17 code.
 *
 * Templates cover the 9 supported algorithmic patterns in the DSA knowledge base.
 */

import { CodeFragment } from '../generator/codeComposer';

// ═══════════════════════════════════════════════════════════════════════════════
// Template Parameter Types
// ═══════════════════════════════════════════════════════════════════════════════

export interface TemplateParams {
  /** Use 'long long' when overflow risk detected */
  intType: 'int' | 'long long';
  hasQueries?: boolean;
  operationSubtype?: 'range_sum' | 'target_sum' | 'pair_sum_positions' | 'container_most_water' | 'variable_min' | string;
  hasInitialSort?: boolean;
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template Registry
// ═══════════════════════════════════════════════════════════════════════════════

export type TemplateId =
  | 'frequencyCount'
  | 'prefixSum'
  | 'twoPointers'
  | 'slidingWindow'
  | 'binarySearch'
  | 'sortGreedy'
  | 'bfs'
  | 'dfs'
  | 'dp1d'
  | 'arithmeticGap'
  | 'lis'
  | 'monotonicStack'
  | 'trie'
  | 'lruCache'
  | 'lfuCache'
  | 'treeDp';

const TEMPLATE_BUILDERS: Record<TemplateId, (params: TemplateParams) => CodeFragment> = {
  frequencyCount: buildFrequencyCount,
  prefixSum: buildPrefixSum,
  twoPointers: buildTwoPointers,
  slidingWindow: buildSlidingWindow,
  binarySearch: buildBinarySearch,
  sortGreedy: buildSortGreedy,
  bfs: buildBfs,
  dfs: buildDfs,
  dp1d: buildDp1d,
  arithmeticGap: buildArithmeticGap,
  lis: buildLis,
  monotonicStack: buildMonotonicStack,
  trie: buildTrie,
  lruCache: buildLruCache,
  lfuCache: buildLfuCache,
  treeDp: buildTreeDp
};

/**
 * Build a solution from a template ID and parameters.
 * Returns null if the template ID is not found.
 */
export function buildFromTemplate(templateId: string, params: TemplateParams): CodeFragment | null {
  const builder = TEMPLATE_BUILDERS[templateId as TemplateId];
  if (!builder) return null;
  return builder(params);
}

/** Get all available template IDs. */
export function getAvailableTemplates(): TemplateId[] {
  return Object.keys(TEMPLATE_BUILDERS) as TemplateId[];
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template 1: Frequency Counting / Hash Map
// ═══════════════════════════════════════════════════════════════════════════════

function buildFrequencyCount(params: TemplateParams): CodeFragment {
  const T = params.intType;
  return {
    includes: ['<iostream>', '<unordered_map>', '<vector>'],
    functions: [],
    mainCode: `    ${T} n;
    cin >> n;
    vector<${T}> a(n);
    for (${T} i = 0; i < n; i++) {
        cin >> a[i];
    }

    unordered_map<${T}, ${T}> freq;
    for (${T} i = 0; i < n; i++) {
        freq[a[i]]++;
    }

    // Example: find the most frequent element
    ${T} maxFreq = 0, result = 0;
    for (auto& [val, cnt] : freq) {
        if (cnt > maxFreq) {
            maxFreq = cnt;
            result = val;
        }
    }
    cout << result << endl;`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template 2: Prefix Sum
// ═══════════════════════════════════════════════════════════════════════════════

function buildPrefixSum(params: TemplateParams): CodeFragment {
  const T = params.intType;

  // Variant A: Range Sum Queries (Q queries with l and r positions)
  if (params.operationSubtype === 'range_sum' || params.hasQueries) {
    const includes = ['<iostream>', '<vector>'];
    if (params.hasInitialSort) {
      includes.push('<algorithm>');
    }
    return {
      includes,
      functions: [],
      mainCode: `    ${T} n, q;
    if (!(cin >> n >> q)) return 0;
    vector<${T}> a(n);
    for (${T} i = 0; i < n; i++) {
        cin >> a[i];
    }
    ${params.hasInitialSort ? `sort(a.begin(), a.end());\n    ` : ''}vector<${T}> pref(n + 1, 0);
    for (${T} i = 0; i < n; i++) {
        pref[i + 1] = pref[i] + a[i];
    }

    while (q--) {
        ${T} l, r;
        cin >> l >> r;
        // 1-indexed range query [l, r]
        cout << pref[r] - pref[l - 1] << "\\n";
    }`
    };
  }

  // Variant B: Target sum subarray (e.g. subarray sum = k)
  return {
    includes: ['<iostream>', '<vector>', '<unordered_map>'],
    functions: [],
    mainCode: `    ${T} n, k;
    cin >> n >> k;
    vector<${T}> a(n);
    for (${T} i = 0; i < n; i++) {
        cin >> a[i];
    }

    // Prefix sum + hash map: find longest subarray with sum = k
    unordered_map<${T}, ${T}> firstOccurrence;
    firstOccurrence[0] = -1;  // empty prefix has sum 0

    ${T} prefixSum = 0;
    ${T} maxLen = 0;

    for (${T} i = 0; i < n; i++) {
        prefixSum += a[i];

        ${T} target = prefixSum - k;
        if (firstOccurrence.count(target)) {
            ${T} len = i - firstOccurrence[target];
            if (len > maxLen) maxLen = len;
        }

        if (!firstOccurrence.count(prefixSum)) {
            firstOccurrence[prefixSum] = i;
        }
    }

    cout << maxLen << endl;`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template 3: Two Pointers
// ═══════════════════════════════════════════════════════════════════════════════

function buildTwoPointers(params: TemplateParams): CodeFragment {
  const T = params.intType;

  if (params.operationSubtype === 'pair_sum_positions') {
    return {
      includes: ['<iostream>', '<vector>', '<algorithm>'],
      functions: [],
      mainCode: `    ${T} n, target;
    if (!(cin >> n >> target)) return 0;
    vector<pair<${T}, int>> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i].first;
        a[i].second = i + 1;
    }

    sort(a.begin(), a.end());

    int lo = 0, hi = n - 1;
    bool found = false;

    while (lo < hi) {
        ${T} sum = a[lo].first + a[hi].first;
        if (sum == target) {
            cout << a[lo].second << " " << a[hi].second << endl;
            found = true;
            break;
        } else if (sum < target) {
            lo++;
        } else {
            hi--;
        }
    }

    if (!found) {
        cout << -1 << endl;
    }`
    };
  }

  if (params.operationSubtype === 'container_most_water') {
    return {
      includes: ['<iostream>', '<vector>', '<algorithm>'],
      functions: [],
      mainCode: `    int n;
    if (!(cin >> n)) return 0;
    vector<${T}> h(n);
    for (int i = 0; i < n; i++) {
        cin >> h[i];
    }

    int lo = 0, hi = n - 1;
    ${T} maxArea = 0;

    while (lo < hi) {
        ${T} width = hi - lo;
        ${T} currentH = min(h[lo], h[hi]);
        ${T} area = width * currentH;
        maxArea = max(maxArea, area);

        if (h[lo] <= h[hi]) {
            lo++;
        } else {
            hi--;
        }
    }

    cout << maxArea << endl;`
    };
  }

  return {
    includes: ['<iostream>', '<vector>', '<algorithm>'],
    functions: [],
    mainCode: `    ${T} n, target;
    cin >> n >> target;
    vector<${T}> a(n);
    for (${T} i = 0; i < n; i++) {
        cin >> a[i];
    }

    sort(a.begin(), a.end());

    // Two pointers: find pair with given sum
    ${T} lo = 0, hi = n - 1;
    bool found = false;

    while (lo < hi) {
        ${T} sum = a[lo] + a[hi];
        if (sum == target) {
            cout << a[lo] << " " << a[hi] << endl;
            found = true;
            break;
        } else if (sum < target) {
            lo++;
        } else {
            hi--;
        }
    }

    if (!found) {
        cout << -1 << endl;
    }`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template 4: Sliding Window
// ═══════════════════════════════════════════════════════════════════════════════

function buildSlidingWindow(params: TemplateParams): CodeFragment {
  const T = params.intType;

  if (params.operationSubtype === 'variable_min') {
    return {
      includes: ['<iostream>', '<vector>', '<algorithm>'],
      functions: [],
      mainCode: `    int n;
    ${T} target;
    if (!(cin >> n >> target)) return 0;
    vector<${T}> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    int lo = 0;
    ${T} currentSum = 0;
    int minLen = n + 1;

    for (int hi = 0; hi < n; hi++) {
        currentSum += a[hi];
        while (currentSum >= target && lo <= hi) {
            minLen = min(minLen, hi - lo + 1);
            currentSum -= a[lo];
            lo++;
        }
    }

    cout << (minLen > n ? 0 : minLen) << endl;`
    };
  }

  return {
    includes: ['<iostream>', '<vector>', '<algorithm>'],
    functions: [],
    mainCode: `    ${T} n, k;
    cin >> n >> k;
    vector<${T}> a(n);
    for (${T} i = 0; i < n; i++) {
        cin >> a[i];
    }

    // Sliding window: maximum sum subarray of size k
    if (k > n) {
        cout << -1 << endl;
        return 0;
    }

    ${T} windowSum = 0;
    for (${T} i = 0; i < k; i++) {
        windowSum += a[i];
    }

    ${T} maxSum = windowSum;

    for (${T} i = k; i < n; i++) {
        windowSum += a[i] - a[i - k];
        maxSum = max(maxSum, windowSum);
    }

    cout << maxSum << endl;`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template 5: Binary Search
// ═══════════════════════════════════════════════════════════════════════════════

function buildBinarySearch(params: TemplateParams): CodeFragment {
  const T = params.intType;
  return {
    includes: ['<iostream>', '<vector>', '<algorithm>'],
    functions: [
      `// Binary search: find first occurrence of target in sorted array
${T} lowerBound(vector<${T}>& a, ${T} target) {
    ${T} lo = 0, hi = (${T})a.size() - 1, result = -1;
    while (lo <= hi) {
        ${T} mid = lo + (hi - lo) / 2;
        if (a[mid] == target) {
            result = mid;
            hi = mid - 1;
        } else if (a[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return result;
}`
    ],
    mainCode: `    ${T} n, target;
    cin >> n >> target;
    vector<${T}> a(n);
    for (${T} i = 0; i < n; i++) {
        cin >> a[i];
    }

    sort(a.begin(), a.end());

    ${T} idx = lowerBound(a, target);
    if (idx != -1) {
        cout << idx << endl;
    } else {
        cout << -1 << endl;
    }`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template 6: Sorting + Greedy
// ═══════════════════════════════════════════════════════════════════════════════

function buildSortGreedy(params: TemplateParams): CodeFragment {
  const T = params.intType;
  return {
    includes: ['<iostream>', '<vector>', '<algorithm>'],
    functions: [],
    mainCode: `    ${T} n;
    cin >> n;
    vector<pair<${T}, ${T}>> intervals(n);
    for (${T} i = 0; i < n; i++) {
        cin >> intervals[i].first >> intervals[i].second;
    }

    // Sort by end time (greedy: activity selection)
    sort(intervals.begin(), intervals.end(),
         [](const pair<${T},${T}>& a, const pair<${T},${T}>& b) {
             return a.second < b.second;
         });

    ${T} count = 1;
    ${T} lastEnd = intervals[0].second;

    for (${T} i = 1; i < n; i++) {
        if (intervals[i].first >= lastEnd) {
            count++;
            lastEnd = intervals[i].second;
        }
    }

    cout << count << endl;`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template 7: BFS
// ═══════════════════════════════════════════════════════════════════════════════

function buildBfs(params: TemplateParams): CodeFragment {
  const T = params.intType;
  return {
    includes: ['<iostream>', '<vector>', '<queue>'],
    functions: [],
    mainCode: `    ${T} n, m;
    cin >> n >> m;
    vector<vector<${T}>> adj(n + 1);
    for (${T} i = 0; i < m; i++) {
        ${T} u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);  // undirected
    }

    ${T} src, dest;
    cin >> src >> dest;

    // BFS: shortest path in unweighted graph
    vector<${T}> dist(n + 1, -1);
    queue<${T}> q;
    dist[src] = 0;
    q.push(src);

    while (!q.empty()) {
        ${T} u = q.front();
        q.pop();
        for (${T} v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }

    cout << dist[dest] << endl;`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template 8: DFS
// ═══════════════════════════════════════════════════════════════════════════════

function buildDfs(params: TemplateParams): CodeFragment {
  const T = params.intType;
  return {
    includes: ['<iostream>', '<vector>'],
    functions: [
      `// DFS to mark all nodes in a connected component
void dfs(${T} u, vector<vector<${T}>>& adj, vector<bool>& visited) {
    visited[u] = true;
    for (${T} v : adj[u]) {
        if (!visited[v]) {
            dfs(v, adj, visited);
        }
    }
}`
    ],
    mainCode: `    ${T} n, m;
    cin >> n >> m;
    vector<vector<${T}>> adj(n + 1);
    for (${T} i = 0; i < m; i++) {
        ${T} u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);  // undirected
    }

    // Count connected components
    vector<bool> visited(n + 1, false);
    ${T} components = 0;

    for (${T} i = 1; i <= n; i++) {
        if (!visited[i]) {
            dfs(i, adj, visited);
            components++;
        }
    }

    cout << components << endl;`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template 9: Simple 1D DP (Kadane's Algorithm variant)
// ═══════════════════════════════════════════════════════════════════════════════

function buildDp1d(params: TemplateParams): CodeFragment {
  const T = params.intType;
  return {
    includes: ['<iostream>', '<vector>', '<algorithm>', '<climits>'],
    functions: [],
    mainCode: `    ${T} n;
    cin >> n;
    vector<${T}> a(n);
    for (${T} i = 0; i < n; i++) {
        cin >> a[i];
    }

    // Kadane's algorithm: maximum subarray sum
    ${T} maxEndingHere = a[0];
    ${T} maxSoFar = a[0];

    for (${T} i = 1; i < n; i++) {
        maxEndingHere = max(a[i], maxEndingHere + a[i]);
        maxSoFar = max(maxSoFar, maxEndingHere);
    }

    cout << maxSoFar << endl;`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template 10: Arithmetic Gap
// ═══════════════════════════════════════════════════════════════════════════════

function buildArithmeticGap(params: TemplateParams): CodeFragment {
  return {
    includes: ['<iostream>', '<vector>'],
    functions: [],
    mainCode: `    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    long long n;
    if (!(cin >> n)) return 0;
    long long expected = n * (n + 1) / 2;
    long long actual = 0;
    for (long long i = 0; i < n - 1; i++) {
        long long x; cin >> x; actual += x;
    }
    cout << (expected - actual) << "\\n";`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template 11: Longest Increasing Subsequence
// ═══════════════════════════════════════════════════════════════════════════════

function buildLis(params: TemplateParams): CodeFragment {
  return {
    includes: ['<iostream>', '<vector>', '<algorithm>'],
    functions: [],
    mainCode: `    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    long long n;
    if (!(cin >> n)) return 0;
    vector<long long> a(n);
    for (long long i = 0; i < n; i++) cin >> a[i];
    // O(N log N) patience sort
    vector<long long> dp;
    for (long long i = 0; i < n; i++) {
        auto it = lower_bound(dp.begin(), dp.end(), a[i]);
        if (it == dp.end()) dp.push_back(a[i]);
        else *it = a[i];
    }
    cout << dp.size() << "\\n";`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template 12: Monotonic Stack (Dominance Elimination)
// ═══════════════════════════════════════════════════════════════════════════════

function buildMonotonicStack(params: TemplateParams): CodeFragment {
  const T = params.intType;

  if (params.operationSubtype === 'histogram') {
    return {
      includes: ['<iostream>', '<vector>', '<stack>', '<algorithm>'],
      functions: [],
      mainCode: `    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    vector<${T}> h(n);
    for (int i = 0; i < n; i++) cin >> h[i];
    stack<int> st;
    long long maxArea = 0;
    for (int i = 0; i <= n; i++) {
        long long curH = (i == n ? 0 : h[i]);
        while (!st.empty() && (i == n || h[st.top()] >= curH)) {
            long long height = h[st.top()];
            st.pop();
            long long width = st.empty() ? i : (i - st.top() - 1);
            maxArea = max(maxArea, height * width);
        }
        st.push(i);
    }
    cout << maxArea << "\\n";`
    };
  }

  if (params.operationSubtype === 'next_greater') {
    return {
      includes: ['<iostream>', '<vector>', '<stack>'],
      functions: [],
      mainCode: `    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    vector<${T}> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    stack<${T}> st;
    vector<${T}> ans(n, -1);
    for (int i = n - 1; i >= 0; i--) {
        while (!st.empty() && st.top() <= a[i]) st.pop();
        ans[i] = st.empty() ? -1 : st.top();
        st.push(a[i]);
    }
    for (int i = 0; i < n; i++) {
        cout << ans[i] << (i + 1 == n ? "" : " ");
    }
    cout << "\\n";`
    };
  }
  if (params.operationSubtype === 'daily_temperatures') {
    return {
      includes: ['<iostream>', '<vector>', '<stack>'],
      functions: [],
      mainCode: `    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    vector<${T}> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    stack<int> st;
    vector<int> ans(n, 0);
    for (int i = 0; i < n; i++) {
        while (!st.empty() && a[i] > a[st.top()]) {
            int prev = st.top();
            st.pop();
            ans[prev] = i - prev;
        }
        st.push(i);
    }
    for (int i = 0; i < n; i++) {
        cout << ans[i] << (i + 1 == n ? "" : " ");
    }
    cout << "\\n";`
    };
  }

  if (params.operationSubtype === 'stock_span') {
    return {
      includes: ['<iostream>', '<vector>', '<stack>'],
      functions: [],
      mainCode: `    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    vector<${T}> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    stack<int> st;
    vector<int> ans(n, 1);
    for (int i = 0; i < n; i++) {
        while (!st.empty() && a[st.top()] <= a[i]) st.pop();
        ans[i] = st.empty() ? (i + 1) : (i - st.top());
        st.push(i);
    }
    for (int i = 0; i < n; i++) {
        cout << ans[i] << (i + 1 == n ? "" : " ");
    }
    cout << "\\n";`
    };
  }

  // Default: Nearest Smaller to Left (CSES 1645 style)
  return {
    includes: ['<iostream>', '<vector>', '<stack>'],
    functions: [],
    mainCode: `    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    vector<${T}> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    stack<int> st;
    vector<int> ans(n, 0);
    for (int i = 0; i < n; i++) {
        while (!st.empty() && a[st.top()] >= a[i]) st.pop();
        ans[i] = st.empty() ? 0 : st.top() + 1;
        st.push(i);
    }
    for (int i = 0; i < n; i++) {
        cout << ans[i] << (i + 1 == n ? "" : " ");
    }
    cout << "\\n";`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template 13: Trie / Prefix Tree
// ═══════════════════════════════════════════════════════════════════════════════

function buildTrie(params: TemplateParams): CodeFragment {
  const TRIE_CLASS = `struct TrieNode {
    int next[26];
    int countPrefix = 0;
    bool isWord = false;
    TrieNode() {
        fill(begin(next), end(next), -1);
    }
};

class Trie {
public:
    vector<TrieNode> tree;
    Trie() {
        tree.emplace_back();
    }
    void insert(const string& s) {
        int u = 0;
        tree[u].countPrefix++;
        for (char c : s) {
            int idx = c - 'a';
            if (tree[u].next[idx] == -1) {
                tree[u].next[idx] = (int)tree.size();
                tree.emplace_back();
            }
            u = tree[u].next[idx];
            tree[u].countPrefix++;
        }
        tree[u].isWord = true;
    }
    bool search(const string& s) const {
        int u = 0;
        for (char c : s) {
            int idx = c - 'a';
            if (tree[u].next[idx] == -1) return false;
            u = tree[u].next[idx];
        }
        return tree[u].isWord;
    }
    bool startsWith(const string& prefix) const {
        int u = 0;
        for (char c : prefix) {
            int idx = c - 'a';
            if (tree[u].next[idx] == -1) return false;
            u = tree[u].next[idx];
        }
        return true;
    }
    int countPrefix(const string& prefix) const {
        int u = 0;
        for (char c : prefix) {
            int idx = c - 'a';
            if (tree[u].next[idx] == -1) return 0;
            u = tree[u].next[idx];
        }
        return tree[u].countPrefix;
    }
};`;

  return {
    includes: ['<iostream>', '<vector>', '<string>', '<algorithm>'],
    functions: [TRIE_CLASS],
    mainCode: `    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n, q;
    if (!(cin >> n >> q)) return 0;
    Trie trie;
    for (int i = 0; i < n; i++) {
        string w;
        cin >> w;
        trie.insert(w);
    }
    while (q--) {
        int type;
        string s;
        cin >> type >> s;
        if (type == 1) {
            cout << (trie.search(s) ? "YES" : "NO") << "\\n";
        } else if (type == 2) {
            cout << (trie.startsWith(s) ? "YES" : "NO") << "\\n";
        } else {
            cout << trie.countPrefix(s) << "\\n";
        }
    }`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template 14: LRU Cache
// ═══════════════════════════════════════════════════════════════════════════════

function buildLruCache(params: TemplateParams): CodeFragment {
  const LRU_CLASS = `class LRUCache {
    int capacity;
    list<pair<int, int>> items; // {key, value}, front = MRU, back = LRU
    unordered_map<int, list<pair<int, int>>::iterator> lookup;
public:
    LRUCache(int cap) : capacity(cap) {}

    int get(int key) {
        auto it = lookup.find(key);
        if (it == lookup.end()) return -1;
        items.splice(items.begin(), items, it->second);
        return it->second->second;
    }

    void put(int key, int value) {
        auto it = lookup.find(key);
        if (it != lookup.end()) {
            it->second->second = value;
            items.splice(items.begin(), items, it->second);
            return;
        }
        if ((int)items.size() == capacity) {
            int lruKey = items.back().first;
            lookup.erase(lruKey);
            items.pop_back();
        }
        items.emplace_front(key, value);
        lookup[key] = items.begin();
    }
};`;

  return {
    includes: ['<iostream>', '<list>', '<unordered_map>', '<string>', '<utility>'],
    functions: [LRU_CLASS],
    mainCode: `    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int capacity, q;
    if (!(cin >> capacity >> q)) return 0;
    LRUCache cache(capacity);
    while (q--) {
        string op;
        cin >> op;
        if (op == "get") {
            int key;
            cin >> key;
            cout << cache.get(key) << "\\n";
        } else if (op == "put") {
            int key, val;
            cin >> key >> val;
            cache.put(key, val);
        }
    }`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template 15: LFU Cache
// ═══════════════════════════════════════════════════════════════════════════════

function buildLfuCache(params: TemplateParams): CodeFragment {
  const LFU_CLASS = `class LFUCache {
    int capacity;
    int minFreq;
    unordered_map<int, pair<int, int>> keyTable; // key -> {value, freq}
    unordered_map<int, list<int>::iterator> keyIter; // key -> iterator in freqLists[freq]
    unordered_map<int, list<int>> freqLists; // freq -> list of keys (front = MRU, back = LRU)

    void updateFreq(int key) {
        int freq = keyTable[key].second;
        freqLists[freq].erase(keyIter[key]);
        if (freqLists[freq].empty()) {
            freqLists.erase(freq);
            if (minFreq == freq) minFreq++;
        }
        int newFreq = freq + 1;
        keyTable[key].second = newFreq;
        freqLists[newFreq].push_front(key);
        keyIter[key] = freqLists[newFreq].begin();
    }

public:
    LFUCache(int cap) : capacity(cap), minFreq(0) {}

    int get(int key) {
        if (capacity == 0) return -1;
        auto it = keyTable.find(key);
        if (it == keyTable.end()) return -1;
        updateFreq(key);
        return it->second.first;
    }

    void put(int key, int value) {
        if (capacity == 0) return;
        auto it = keyTable.find(key);
        if (it != keyTable.end()) {
            it->second.first = value;
            updateFreq(key);
            return;
        }
        if ((int)keyTable.size() == capacity) {
            int evictKey = freqLists[minFreq].back();
            freqLists[minFreq].pop_back();
            if (freqLists[minFreq].empty()) {
                freqLists.erase(minFreq);
            }
            keyTable.erase(evictKey);
            keyIter.erase(evictKey);
        }
        minFreq = 1;
        keyTable[key] = {value, 1};
        freqLists[1].push_front(key);
        keyIter[key] = freqLists[1].begin();
    }
};`;

  return {
    includes: ['<iostream>', '<list>', '<unordered_map>', '<string>', '<utility>'],
    functions: [LFU_CLASS],
    mainCode: `    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int capacity, q;
    if (!(cin >> capacity >> q)) return 0;
    LFUCache cache(capacity);
    while (q--) {
        string op;
        cin >> op;
        if (op == "get") {
            int key;
            cin >> key;
            cout << cache.get(key) << "\\n";
        } else if (op == "put") {
            int key, val;
            cin >> key >> val;
            cache.put(key, val);
        }
    }`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// Template 16: Tree Dynamic Programming
// ═══════════════════════════════════════════════════════════════════════════════

function buildTreeDp(params: TemplateParams): CodeFragment {
  const TREE_DP_FN = `int dfsDiameter(int u, int p, const vector<vector<int>>& adj, int& maxDiameter) {
    int max1 = 0, max2 = 0;
    for (int v : adj[u]) {
        if (v == p) continue;
        int d = dfsDiameter(v, u, adj, maxDiameter) + 1;
        if (d > max1) {
            max2 = max1;
            max1 = d;
        } else if (d > max2) {
            max2 = d;
        }
    }
    maxDiameter = max(maxDiameter, max1 + max2);
    return max1;
}`;

  return {
    includes: ['<iostream>', '<vector>', '<algorithm>'],
    functions: [TREE_DP_FN],
    mainCode: `    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    if (n <= 1) {
        cout << 0 << "\\n";
        return 0;
    }
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    int maxDiameter = 0;
    dfsDiameter(1, 0, adj, maxDiameter);
    cout << maxDiameter << "\\n";`
  };
}
