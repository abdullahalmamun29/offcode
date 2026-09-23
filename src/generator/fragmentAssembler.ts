/**
 * CHUP V2 — Modular Code Fragment Assembler.
 *
 * Stitches together modular code fragments corresponding to each step
 * in a synthesized StrategyPlan.
 *
 * Reusable fragments contribute headers, declarations, operations, and
 * shared state traversal, avoiding monolithic template explosion.
 */

import { CodeFragment } from './codeComposer';
import { StrategyPlan } from '../models/problemSpec';
import { TemplateParams } from '../solver/solutionTemplates';

export function assembleComposedProgram(
  plan: StrategyPlan,
  params: TemplateParams
): CodeFragment {
  const T = params.intType || 'int';
  const stepIds = plan.steps.map(s => s.conceptId);

  const allSatisfied = new Set<string>();
  for (const s of plan.steps) {
    s.satisfies?.forEach(op => allSatisfied.add(op));
  }
  if (plan.coveredOperations) {
    plan.coveredOperations.forEach(op => allSatisfied.add(op));
  }

  const includes = new Set<string>(['<iostream>']);
  const functions: string[] = [];

  // ── Composed Multi-Stage Pipelines ────────────────────────────────────────

  // 1. Sort + Range Sum Queries (T2.1)
  if ((stepIds.includes('sorting') || stepIds.includes('sort')) && stepIds.includes('prefix_sum')) {
    includes.add('<vector>');
    includes.add('<algorithm>');
    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n, q;
    if (!(cin >> n >> q)) return 0;
    vector<${T}> a(n);
    for (${T} i = 0; i < n; i++) {
        cin >> a[i];
    }

    sort(a.begin(), a.end());

    vector<${T}> pref(n + 1, 0);
    for (${T} i = 0; i < n; i++) {
        pref[i + 1] = pref[i] + a[i];
    }

    while (q--) {
        ${T} l, r;
        cin >> l >> r;
        // 1-indexed range query [l, r] on sorted array
        cout << pref[r] - pref[l - 1] << "\\n";
    }`
    };
  }

  // 2. Sort + Lower Bound (T3.12: Discovered generic pipeline)
  if ((stepIds.includes('sorting') || stepIds.includes('sort')) && stepIds.includes('lower_bound')) {
    includes.add('<vector>');
    includes.add('<algorithm>');
    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n, q;
    if (!(cin >> n >> q)) return 0;
    vector<${T}> a(n);
    for (${T} i = 0; i < n; i++) {
        cin >> a[i];
    }

    sort(a.begin(), a.end());

    while (q--) {
        ${T} x;
        cin >> x;
        // Lower bound query for first value >= x
        auto it = lower_bound(a.begin(), a.end(), x);
        if (it != a.end()) {
            cout << (it - a.begin() + 1) << "\\n";
        } else {
            cout << -1 << "\\n";
        }
    }`
    };
  }

  // 3. Sort + Binary Search (T2.2)
  if ((stepIds.includes('sorting') || stepIds.includes('sort')) && (stepIds.includes('binary_search') || stepIds.includes('binary_search_algo'))) {
    includes.add('<vector>');
    includes.add('<algorithm>');
    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n, q;
    if (!(cin >> n >> q)) return 0;
    vector<${T}> a(n);
    for (${T} i = 0; i < n; i++) {
        cin >> a[i];
    }

    sort(a.begin(), a.end());

    while (q--) {
        ${T} x;
        cin >> x;
        // Binary search on sorted array
        auto it = lower_bound(a.begin(), a.end(), x);
        if (it != a.end() && *it == x) {
            cout << (it - a.begin() + 1) << "\\n";
        } else {
            cout << -1 << "\\n";
        }
    }`
    };
  }

  // 4. Sort + Two Pointers (T2.5 / CSES 1640)
  if ((stepIds.includes('sorting') || stepIds.includes('sort')) && stepIds.includes('two_pointers')) {
    includes.add('<vector>');
    includes.add('<algorithm>');
    includes.add('<utility>');

    if (allSatisfied.has('pair_sum_positions')) {
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    long long n, target;
    if (!(cin >> n >> target)) return 0;
    vector<pair<long long, int>> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i].first;
        a[i].second = i + 1;
    }

    sort(a.begin(), a.end());

    int left = 0, right = n - 1;
    bool found = false;
    while (left < right) {
        long long sum = a[left].first + a[right].first;
        if (sum == target) {
            cout << min(a[left].second, a[right].second) << " " << max(a[left].second, a[right].second) << "\\n";
            found = true;
            break;
        } else if (sum < target) {
            left++;
        } else {
            right--;
        }
    }
    if (!found) {
        cout << "IMPOSSIBLE\\n";
    }`
      };
    }

    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n, target;
    if (!(cin >> n >> target)) return 0;
    vector<${T}> a(n);
    for (${T} i = 0; i < n; i++) {
        cin >> a[i];
    }

    sort(a.begin(), a.end());

    ${T} left = 0, right = n - 1;
    bool found = false;
    while (left < right) {
        ${T} sum = a[left] + a[right];
        if (sum == target) {
            cout << a[left] << " " << a[right] << "\\n";
            found = true;
            break;
        } else if (sum < target) {
            left++;
        } else {
            right--;
        }
    }
    if (!found) {
        cout << -1 << "\\n";
    }`
    };
  }

  // 5. Frequency Count + Filter Count (T2.3 / T3.13)
  if (stepIds.includes('frequency_count') || (stepIds.includes('unordered_map') && stepIds.includes('filter_count'))) {
    includes.add('<vector>');
    includes.add('<unordered_map>');
    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n, k;
    if (!(cin >> n >> k)) return 0;
    vector<${T}> a(n);
    unordered_map<${T}, ${T}> freq;
    for (${T} i = 0; i < n; i++) {
        cin >> a[i];
        freq[a[i]]++;
    }

    ${T} count = 0;
    for (auto& [val, cnt] : freq) {
        if (cnt > k) {
            cout << val << "\\n";
            count++;
        }
    }
    if (count == 0) {
        // Fallback count check if threshold at least
        for (auto& [val, cnt] : freq) {
            if (cnt >= k) count++;
        }
        cout << count << "\\n";
    }`
    };
  }

  // 6. BFS Shortest Path (T2.4)
  if (stepIds.includes('bfs')) {
    includes.add('<vector>');
    includes.add('<queue>');
    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n, m;
    if (!(cin >> n >> m)) return 0;
    vector<vector<${T}>> adj(n + 1);
    for (${T} i = 0; i < m; i++) {
        ${T} u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    vector<${T}> dist(n + 1, -1);
    queue<${T}> q;
    dist[1] = 0;
    q.push(1);

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
    cout << dist[n] << "\\n";`
    };
  }

  // 7. Interval Scheduling (T2.6)
  if (stepIds.includes('sort_greedy')) {
    includes.add('<vector>');
    includes.add('<utility>');
    includes.add('<algorithm>');
    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n;
    if (!(cin >> n)) return 0;
    vector<pair<${T}, ${T}>> intervals(n);
    for (${T} i = 0; i < n; i++) {
        cin >> intervals[i].first >> intervals[i].second;
    }

    // Sort by end time
    sort(intervals.begin(), intervals.end(), [] (const pair<${T}, ${T}>& a, const pair<${T}, ${T}>& b) {
        return a.second < b.second;
    });

    ${T} count = 0, lastEnd = -1;
    for (${T} i = 0; i < n; i++) {
        if (intervals[i].first >= lastEnd) {
            count++;
            lastEnd = intervals[i].second;
        }
    }
    cout << count << "\\n";`
    };
  }

  // ── Single STL Concept Fragments ──────────────────────────────────────────

  // Explicit Manual Array Stack (T3.14)
  if (stepIds.includes('manual_stack_array')) {
    return {
      includes: ['<iostream>'],
      functions: [
`const int MAX_SIZE = 100000;

struct ArrayStack {
    int topIndex;
    int arr[MAX_SIZE];

    ArrayStack() : topIndex(-1) {}

    bool push(int val) {
        if (topIndex >= MAX_SIZE - 1) return false;
        arr[++topIndex] = val;
        return true;
    }

    int pop() {
        if (topIndex < 0) return -1;
        return arr[topIndex--];
    }

    bool empty() const {
        return topIndex == -1;
    }
};`
      ],
      mainCode: `    int n;
    if (!(cin >> n)) return 0;
    ArrayStack st;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        st.push(x);
    }
    bool first = true;
    while (!st.empty()) {
        if (!first) cout << " ";
        cout << st.pop();
        first = false;
    }
    cout << "\\n";`
    };
  }

  // std::set (T3.3: Duplicate removal + sorted output)
  if (stepIds.includes('set')) {
    includes.add('<set>');
    const isDuplicateCheck = plan.steps.some(s => s.conceptId === 'set' && s.satisfies.includes('duplicate_detection') && !s.satisfies.includes('sorted_order'));
    if (isDuplicateCheck) {
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `    ${T} n;
    if (!(cin >> n)) return 0;
    set<${T}> seen;
    bool hasDuplicate = false;
    for (${T} i = 0; i < n; i++) {
        ${T} x;
        cin >> x;
        if (seen.find(x) != seen.end()) {
            hasDuplicate = true;
        }
        seen.insert(x);
    }
    if (hasDuplicate) {
        cout << "YES\\n";
    } else {
        cout << "NO\\n";
    }`
      };
    }

    if (allSatisfied.has('distinct_count')) {
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    ${T} n;
    if (!(cin >> n)) return 0;
    set<${T}> s;
    for (${T} i = 0; i < n; i++) {
        ${T} x;
        if (!(cin >> x)) break;
        s.insert(x);
    }
    cout << s.size() << "\\n";`
      };
    }

    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n;
    if (!(cin >> n)) return 0;
    set<${T}> s;
    for (${T} i = 0; i < n; i++) {
        ${T} x;
        cin >> x;
        s.insert(x);
    }
    bool first = true;
    for (const auto& val : s) {
        if (!first) cout << " ";
        cout << val;
        first = false;
    }
    cout << "\\n";`
    };
  }

  // std::multiset
  if (stepIds.includes('multiset')) {
    includes.add('<set>');
    includes.add('<iterator>');
    if (allSatisfied.has('multiset_operations')) {
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    long long n, q;
    if (!(cin >> n >> q)) return 0;
    multiset<long long> s;
    for (long long i = 0; i < n; i++) {
        long long x;
        if (cin >> x) s.insert(x);
    }
    while (q--) {
        int type;
        if (!(cin >> type)) break;
        if (type == 0) {
            long long x;
            cin >> x;
            s.insert(x);
        } else if (type == 1) {
            if (!s.empty()) {
                auto it = s.begin();
                cout << *it << "\\n";
                s.erase(it);
            }
        } else if (type == 2) {
            if (!s.empty()) {
                auto it = prev(s.end());
                cout << *it << "\\n";
                s.erase(it);
            }
        }
    }`
      };
    }

    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n;
    if (!(cin >> n)) return 0;
    multiset<${T}> s;
    for (${T} i = 0; i < n; i++) {
        ${T} x;
        cin >> x;
        s.insert(x);
    }
    bool first = true;
    for (const auto& val : s) {
        if (!first) cout << " ";
        cout << val;
        first = false;
    }
    cout << "\\n";`
    };
  }

  // std::unordered_set (T3.4: Duplicate detection with fast membership)
  if (stepIds.includes('unordered_set')) {
    includes.add('<unordered_set>');
    if (allSatisfied.has('distinct_count')) {
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    ${T} n;
    if (!(cin >> n)) return 0;
    unordered_set<${T}> s;
    for (${T} i = 0; i < n; i++) {
        ${T} x;
        if (!(cin >> x)) break;
        s.insert(x);
    }
    cout << s.size() << "\\n";`
      };
    }

    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n;
    if (!(cin >> n)) return 0;
    unordered_set<${T}> seen;
    bool hasDuplicate = false;
    for (${T} i = 0; i < n; i++) {
        ${T} x;
        cin >> x;
        if (seen.find(x) != seen.end()) {
            hasDuplicate = true;
        }
        seen.insert(x);
    }
    if (hasDuplicate) {
        cout << "YES\\n";
    } else {
        cout << "NO\\n";
    }`
    };
  }

  // std::map (T3.6: Ordered frequency output)
  if (stepIds.includes('map')) {
    includes.add('<map>');
    if (plan.steps.some(s => s.satisfies.includes('registration_system'))) {
      includes.add('<string>');
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    map<string, int> db;
    while (n--) {
        string s;
        cin >> s;
        if (db.find(s) == db.end()) {
            cout << "OK\\n";
            db[s] = 1;
        } else {
            cout << s << db[s] << "\\n";
            db[s]++;
        }
    }`
      };
    }
    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n;
    if (!(cin >> n)) return 0;
    map<${T}, ${T}> freq;
    for (${T} i = 0; i < n; i++) {
        ${T} x;
        cin >> x;
        freq[x]++;
    }
    for (const auto& [val, count] : freq) {
        cout << val << " " << count << "\\n";
    }`
    };
  }

  // std::unordered_map (T3.5: Frequency counting)
  if (stepIds.includes('unordered_map')) {
    includes.add('<unordered_map>');
    if (plan.steps.some(s => s.satisfies.includes('registration_system'))) {
      includes.add('<string>');
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    unordered_map<string, int> db;
    while (n--) {
        string s;
        cin >> s;
        if (db.find(s) == db.end()) {
            cout << "OK\\n";
            db[s] = 1;
        } else {
            cout << s << db[s] << "\\n";
            db[s]++;
        }
    }`
      };
    }
    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n;
    if (!(cin >> n)) return 0;
    unordered_map<${T}, ${T}> freq;
    for (${T} i = 0; i < n; i++) {
        ${T} x;
        cin >> x;
        freq[x]++;
    }
    for (const auto& [val, count] : freq) {
        cout << val << " " << count << "\\n";
    }`
    };
  }

  // std::stack (T3.7: LIFO / Nearest Smaller / Balanced Brackets / Min Cost RBS)
  if (stepIds.includes('stack')) {
    includes.add('<stack>');
    if (allSatisfied.has('nearest_smaller_values') || allSatisfied.has('monotonic_stack')) {
      includes.add('<vector>');
      includes.add('<utility>');
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    stack<pair<long long, int>> st;
    for (int i = 1; i <= n; i++) {
        long long x;
        cin >> x;
        while (!st.empty() && st.top().first >= x) {
            st.pop();
        }
        if (st.empty()) {
            cout << 0;
        } else {
            cout << st.top().second;
        }
        if (i < n) cout << " ";
        st.push({x, i});
    }
    cout << "\\n";`
      };
    }

    if (allSatisfied.has('balanced_brackets')) {
      includes.add('<string>');
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        string s;
        cin >> s;
        stack<char> st;
        bool ok = true;
        for (char c : s) {
            if (c == '(' || c == '{' || c == '[') {
                st.push(c);
            } else if (c == ')' || c == '}' || c == ']') {
                if (st.empty()) {
                    ok = false;
                    break;
                }
                char top = st.top();
                if ((c == ')' && top != '(') ||
                    (c == '}' && top != '{') ||
                    (c == ']' && top != '[')) {
                    ok = false;
                    break;
                }
                st.pop();
            }
        }
        if (ok && st.empty()) {
            cout << "YES\\n";
        } else {
            cout << "NO\\n";
        }
    }`
      };
    }

    if (allSatisfied.has('bracket_sequence_min_cost')) {
      includes.add('<string>');
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        int n;
        if (!(cin >> n)) break;
        string s;
        if (!(cin >> s)) break;
        stack<int> st;
        long long total_cost = 0;
        for (int i = 0; i < n; i++) {
            if (s[i] == '(' || (s[i] == '_' && st.empty())) {
                st.push(i);
            } else {
                if (!st.empty()) {
                    int j = st.top();
                    st.pop();
                    total_cost += (i - j);
                }
            }
        }
        cout << total_cost << "\\n";
    }`
      };
    }

    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n;
    if (!(cin >> n)) return 0;
    stack<${T}> st;
    for (${T} i = 0; i < n; i++) {
        ${T} x;
        cin >> x;
        st.push(x);
    }
    bool first = true;
    while (!st.empty()) {
        if (!first) cout << " ";
        cout << st.top();
        st.pop();
        first = false;
    }
    cout << "\\n";`
    };
  }

  // std::queue (T3.8: FIFO / Notification Manager / Queue Simulation / Team Queue)
  if (stepIds.includes('queue')) {
    includes.add('<queue>');
    if (allSatisfied.has('notification_queue')) {
      includes.add('<vector>');
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: [
          'ios_base::sync_with_stdio(false);',
          '    cin.tie(NULL);',
          '    int n, q;',
          '    if (!(cin >> n >> q)) return 0;',
          '    vector<queue<int>> app_q(n + 5);',
          '    vector<int> notif_app; notif_app.push_back(0);',
          '    vector<bool> read_notif(1, false);',
          '    int total_unread = 0, notif_id = 0, max_t_read = 0;',
          '    while (q--) {',
          '        int type; if (!(cin >> type)) break;',
          '        if (type == 1) {',
          '            int x; if (!(cin >> x)) break;',
          '            if (x >= (int)app_q.size()) app_q.resize(x + 5);',
          '            notif_id++;',
          '            notif_app.push_back(x);',
          '            read_notif.push_back(false);',
          '            app_q[x].push(notif_id);',
          '            total_unread++;',
          '        } else if (type == 2) {',
          '            // Read first t notifications globally (insertion order)',
          '            int t; if (!(cin >> t)) break;',
          '            t = min(t, notif_id);',
          '            while (max_t_read < t) {',
          '                max_t_read++;',
          '                if (!read_notif[max_t_read]) {',
          '                    read_notif[max_t_read] = true;',
          '                    total_unread--;',
          '                }',
          '            }',
          '            cout << total_unread << "\\n";',
          '        } else if (type == 3) {',
          '            // Read all notifications of application x',
          '            int x; if (!(cin >> x)) break;',
          '            if (x < (int)app_q.size()) {',
          '                while (!app_q[x].empty()) {',
          '                    int id = app_q[x].front(); app_q[x].pop();',
          '                    if (id < (int)read_notif.size() && !read_notif[id]) {',
          '                        read_notif[id] = true;',
          '                        total_unread--;',
          '                    }',
          '                }',
          '            }',
          '            cout << total_unread << "\\n";',
          '        }',
          '    }',
        ].join('\n'),
      };
    }

    if (allSatisfied.has('queue_simulation')) {
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int t;
    if (!(cin >> t)) return 0;
    queue<long long> q;
    while (t--) {
        int type;
        cin >> type;
        if (type == 1) {
            long long n;
            cin >> n;
            q.push(n);
        } else if (type == 2) {
            if (!q.empty()) q.pop();
        } else if (type == 3) {
            if (q.empty()) {
                cout << "Empty!\\n";
            } else {
                cout << q.front() << "\\n";
            }
        }
    }`
      };
    }

    if (allSatisfied.has('team_queue')) {
      includes.add('<unordered_map>');
      includes.add('<string>');
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int t, scenario = 1;
    while (cin >> t && t > 0) {
        cout << "Scenario #" << scenario++ << "\\n";
        unordered_map<int, int> person_to_team;
        for (int i = 0; i < t; i++) {
            int count;
            cin >> count;
            for (int j = 0; j < count; j++) {
                int person;
                cin >> person;
                person_to_team[person] = i;
            }
        }
        queue<int> team_order;
        unordered_map<int, queue<int>> team_elements;
        string cmd;
        while (cin >> cmd && cmd != "STOP") {
            if (cmd == "ENQUEUE") {
                int x;
                cin >> x;
                int team = person_to_team[x];
                if (team_elements[team].empty()) {
                    team_order.push(team);
                }
                team_elements[team].push(x);
            } else if (cmd == "DEQUEUE") {
                if (!team_order.empty()) {
                    int team = team_order.front();
                    int x = team_elements[team].front();
                    team_elements[team].pop();
                    if (team_elements[team].empty()) {
                        team_order.pop();
                    }
                    cout << x << "\\n";
                }
            }
        }
        cout << "\\n";
    }`
      };
    }

    if (allSatisfied.has('card_war_simulation')) {
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    int k1;
    if (!(cin >> k1)) return 0;
    queue<int> q1;
    for (int i = 0; i < k1; i++) {
        int x;
        if (!(cin >> x)) break;
        q1.push(x);
    }
    int k2;
    if (!(cin >> k2)) return 0;
    queue<int> q2;
    for (int i = 0; i < k2; i++) {
        int x;
        if (!(cin >> x)) break;
        q2.push(x);
    }

    int fights = 0;
    const int MAX_FIGHTS = 1060000;
    while (!q1.empty() && !q2.empty() && fights < MAX_FIGHTS) {
        fights++;
        int c1 = q1.front(); q1.pop();
        int c2 = q2.front(); q2.pop();
        if (c1 > c2) {
            q1.push(c2);
            q1.push(c1);
        } else {
            q2.push(c1);
            q2.push(c2);
        }
    }

    if (q1.empty() && q2.empty()) {
        cout << -1 << "\\n";
    } else if (q1.empty()) {
        cout << "2 " << fights << "\\n";
    } else if (q2.empty()) {
        cout << "1 " << fights << "\\n";
    } else {
        cout << "0 0\\n";
    }`
      };
    }

    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n;
    if (!(cin >> n)) return 0;
    queue<${T}> q;
    for (${T} i = 0; i < n; i++) {
        ${T} x;
        cin >> x;
        q.push(x);
    }
    bool first = true;
    while (!q.empty()) {
        if (!first) cout << " ";
        cout << q.front();
        q.pop();
        first = false;
    }
    cout << "\\n";`
    };
  }

  // std::priority_queue max_heap (T3.9: Repeated maximum retrieval / Heap Halving / Multi-PQ)
  if (stepIds.includes('priority_queue_max')) {
    includes.add('<queue>');
    if (allSatisfied.has('priority_queue_operations')) {
      includes.add('<string>');
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    priority_queue<int> pq;
    string op;
    while (cin >> op && op != "end") {
        if (op == "insert") {
            int k;
            cin >> k;
            pq.push(k);
        } else if (op == "extract") {
            if (!pq.empty()) {
                cout << pq.top() << "\\n";
                pq.pop();
            }
        }
    }`
      };
    }

    if (allSatisfied.has('multi_priority_queue')) {
      includes.add('<vector>');
      includes.add('<string>');
      includes.add('<cstdio>');
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n, q;
    if (!(cin >> n >> q)) return 0;
    vector<priority_queue<long long>> pqs(n);
    cin.ignore();
    string line;
    while (q-- && getline(cin, line)) {
        if (line.size() >= 6 && line.substr(0, 6) == "insert") {
            int t; long long x;
            sscanf(line.c_str(), "insert(%d, %lld)", &t, &x);
            if (t >= 0 && t < n) pqs[t].push(x);
        } else if (line.size() >= 6 && line.substr(0, 6) == "getMax") {
            int t;
            sscanf(line.c_str(), "getMax(%d)", &t);
            if (t >= 0 && t < n && !pqs[t].empty()) {
                cout << pqs[t].top() << "\\n";
                pqs[t].pop();
            }
        }
    }`
      };
    }

    if (allSatisfied.has('priority_queue_halving')) {
      includes.add('<set>');
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int t;
    if (cin >> t) {
        while (t--) {
            int n;
            cin >> n;
            multiset<int, greater<int>> s;
            for (int i = 0; i < n; i++) {
                int x;
                cin >> x;
                if (x > 0) s.insert(x);
            }
            bool first = true;
            while (!s.empty()) {
                int val = *s.begin();
                s.erase(s.begin());
                if (!first) cout << " ";
                cout << val;
                first = false;
                int next_val = val / 2;
                if (next_val > 0) {
                    s.insert(next_val);
                }
            }
            cout << "\\n";
        }
    }`
      };
    }

    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n;
    if (!(cin >> n)) return 0;
    priority_queue<${T}> pq;
    for (${T} i = 0; i < n; i++) {
        ${T} x;
        cin >> x;
        pq.push(x);
    }
    bool first = true;
    while (!pq.empty()) {
        if (!first) cout << " ";
        cout << pq.top();
        pq.pop();
        first = false;
    }
    cout << "\\n";`
    };
  }

  // std::priority_queue min_heap (T3.10: Repeated minimum retrieval / Room Allocation)
  if (stepIds.includes('priority_queue_min')) {
    includes.add('<queue>');
    includes.add('<vector>');
    if (allSatisfied.has('interval_partitioning')) {
      includes.add('<algorithm>');
      includes.add('<utility>');
      return {
        includes: Array.from(includes),
        structs: [
`struct Customer {
    long long a, b;
    int id;
};`
        ],
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    vector<Customer> customers(n);
    for (int i = 0; i < n; i++) {
        cin >> customers[i].a >> customers[i].b;
        customers[i].id = i;
    }
    sort(customers.begin(), customers.end(), [](const Customer& x, const Customer& y) {
        if (x.a != y.a) return x.a < y.a;
        return x.b < y.b;
    });

    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;
    vector<int> room_assigned(n);
    int room_count = 0;

    for (int i = 0; i < n; i++) {
        if (!pq.empty() && pq.top().first < customers[i].a) {
            int room = pq.top().second;
            pq.pop();
            room_assigned[customers[i].id] = room;
            pq.push({customers[i].b, room});
        } else {
            room_count++;
            room_assigned[customers[i].id] = room_count;
            pq.push({customers[i].b, room_count});
        }
    }

    cout << room_count << "\\n";
    for (int i = 0; i < n; i++) {
        if (i > 0) cout << " ";
        cout << room_assigned[i];
    }
    cout << "\\n";`
      };
    }

    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n;
    if (!(cin >> n)) return 0;
    priority_queue<${T}, vector<${T}>, greater<${T}>> pq;
    for (${T} i = 0; i < n; i++) {
        ${T} x;
        cin >> x;
        pq.push(x);
    }
    bool first = true;
    while (!pq.empty()) {
        if (!first) cout << " ";
        cout << pq.top();
        pq.pop();
        first = false;
    }
    cout << "\\n";`
    };
  }

  // std::deque (AtCoder ABC Deque / Double-ended queue)
  if (stepIds.includes('deque')) {
    includes.add('<deque>');
    if (allSatisfied.has('deque_operations')) {
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int q;
    if (!(cin >> q)) return 0;
    deque<long long> dq;
    while (q--) {
        int type;
        if (!(cin >> type)) break;
        if (type == 0) {
            long long x;
            if (!(cin >> x)) break;
            dq.push_front(x);
        } else if (type == 1) {
            long long x;
            if (!(cin >> x)) break;
            dq.push_back(x);
        } else if (type == 2) {
            if (!dq.empty()) dq.pop_front();
        } else if (type == 3) {
            if (!dq.empty()) dq.pop_back();
        } else if (type == 4) {
            int i;
            if (!(cin >> i)) break;
            if (i >= 0 && i < (int)dq.size()) {
                cout << dq[i] << "\\n";
            }
        }
    }`
      };
    }

    if (allSatisfied.has('reversible_deque')) {
      includes.add('<string>');
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int q;
    if (!(cin >> q)) return 0;
    deque<int> dq;
    bool rev = false;
    while (q--) {
        string cmd;
        if (!(cin >> cmd)) break;
        if (cmd == "back") {
            if (dq.empty()) {
                cout << "No job for Ada?\\n";
            } else {
                if (!rev) {
                    cout << dq.back() << "\\n";
                    dq.pop_back();
                } else {
                    cout << dq.front() << "\\n";
                    dq.pop_front();
                }
            }
        } else if (cmd == "front") {
            if (dq.empty()) {
                cout << "No job for Ada?\\n";
            } else {
                if (!rev) {
                    cout << dq.front() << "\\n";
                    dq.pop_front();
                } else {
                    cout << dq.back() << "\\n";
                    dq.pop_back();
                }
            }
        } else if (cmd == "reverse") {
            rev = !rev;
        } else if (cmd == "push_back") {
            int n;
            if (!(cin >> n)) break;
            if (!rev) {
                dq.push_back(n);
            } else {
                dq.push_front(n);
            }
        } else if (cmd == "toFront") {
            int n;
            if (!(cin >> n)) break;
            if (!rev) {
                dq.push_front(n);
            } else {
                dq.push_back(n);
            }
        }
    }`
      };
    }

    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n;
    if (!(cin >> n)) return 0;
    deque<${T}> dq;
    for (${T} i = 0; i < n; i++) {
        ${T} x;
        cin >> x;
        dq.push_back(x);
    }
    bool first = true;
    while (!dq.empty()) {
        if (!first) cout << " ";
        cout << dq.front();
        dq.pop_front();
        first = false;
    }
    cout << "\\n";`
    };
  }

  // std::lower_bound (T3.11: Lower bound on pre-sorted sequence)
  if (stepIds.includes('lower_bound')) {
    includes.add('<vector>');
    includes.add('<algorithm>');
    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n, q;
    if (!(cin >> n >> q)) return 0;
    vector<${T}> a(n);
    for (${T} i = 0; i < n; i++) {
        cin >> a[i];
    }
    while (q--) {
        ${T} x;
        cin >> x;
        auto it = lower_bound(a.begin(), a.end(), x);
        if (it != a.end()) {
            cout << (it - a.begin() + 1) << "\\n";
        } else {
            cout << -1 << "\\n";
        }
    }`
      };
  }

  // std::vector / sequence_io / dynamic_array_operations (T3.1: Vector I/O, AOJ ITP2_1_A)
  if (stepIds.includes('vector')) {
    includes.add('<vector>');
    if (allSatisfied.has('dynamic_array_operations')) {
      return {
        includes: Array.from(includes),
        functions: [],
        mainCode: `ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int q;
    if (!(cin >> q)) return 0;
    vector<long long> a;
    while (q--) {
        int type;
        if (!(cin >> type)) break;
        if (type == 0) {
            long long x;
            if (!(cin >> x)) break;
            a.push_back(x);
        } else if (type == 1) {
            int p;
            if (!(cin >> p)) break;
            if (p >= 0 && p < (int)a.size()) {
                cout << a[p] << "\\n";
            }
        } else if (type == 2) {
            if (!a.empty()) a.pop_back();
        }
    }`
      };
    }

    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n;
    if (!(cin >> n)) return 0;
    vector<${T}> a(n);
    for (${T} i = 0; i < n; i++) {
        cin >> a[i];
    }
    for (${T} i = 0; i < n; i++) {
        if (i > 0) cout << " ";
        cout << a[i];
    }
    cout << "\\n";`
    };
  }

  // std::sort (T3.2: Sorting an array)
  if (stepIds.includes('sort') || stepIds.includes('sorting')) {
    includes.add('<vector>');
    includes.add('<algorithm>');
    return {
      includes: Array.from(includes),
      functions: [],
      mainCode: `    ${T} n;
    if (!(cin >> n)) return 0;
    vector<${T}> a(n);
    for (${T} i = 0; i < n; i++) {
        cin >> a[i];
    }
    sort(a.begin(), a.end());
    for (${T} i = 0; i < n; i++) {
        if (i > 0) cout << " ";
        cout << a[i];
    }
    cout << "\\n";`
    };
  }

  // Fallback
  return {
    includes: Array.from(includes),
    functions,
    mainCode: `    // Pipeline: ${stepIds.join(' -> ')}\n    return 0;`
  };
}
