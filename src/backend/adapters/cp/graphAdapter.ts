/**
 * CHUP / Offcode — Graph Algorithm Adapter (Phase 5)
 *
 * Adapts existing verified graph solvers and templates for graph capabilities:
 * - single_source_shortest_path (Dijkstra, BFS shortest path)
 * - graph_traversal (BFS, DFS)
 * - topological_sort (Kahn, DFS postorder)
 * - minimum_spanning_tree (Kruskal with DSU, Prim with Priority Queue)
 * - connected_components (BFS, DSU)
 *
 * Invariants:
 * - Operates strictly on structured plan and composition steps.
 * - Reuses existing verified graph algorithmic infrastructure.
 */

import { CapabilityPlan, CompositionStep } from '../../../models/capabilityModel';
import { BackendExecutionResult } from '../../../models/backendModel';
import { generateCpp } from '../../../generator/cppGenerator';
import { StructuredProblem } from '../../../models/problemSpec';

export class GraphAlgorithmAdapter {
  public execute(
    plan: CapabilityPlan,
    step: CompositionStep,
    problem?: StructuredProblem
  ): BackendExecutionResult {
    const algoId = step.algorithmId;
    let code = '';

    if (algoId === 'dijkstra') {
      code = `#include <iostream>
#include <vector>
#include <queue>

using namespace std;

const long long INF = 1e18;

// Solves Single Source Shortest Path using Dijkstra's Algorithm with Min-Heap
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<vector<pair<int, long long>>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        if (cin >> u >> v >> w) {
            adj[u].push_back({v, w});
        }
    }

    int source = 1;
    vector<long long> dist(n + 1, INF);
    // Min-heap: {distance, vertex}
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;

    dist[source] = 0;
    pq.push({0, source});

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();

        if (d > dist[u]) continue; // Stale entry

        for (auto& edge : adj[u]) {
            int v = edge.first;
            long long weight = edge.second;

            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.push({dist[v], v});
            }
        }
    }

    for (int i = 1; i <= n; i++) {
        if (dist[i] == INF) cout << -1 << (i == n ? "" : " ");
        else cout << dist[i] << (i == n ? "" : " ");
    }
    cout << "\\n";

    return 0;
}
`;
    } else if (algoId === 'kahn_algorithm' || step.capabilityId === 'topological_sort') {
      code = `#include <iostream>
#include <vector>
#include <queue>

using namespace std;

// Topological Sort of Directed Acyclic Graph using Kahn's Algorithm
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<vector<int>> adj(n + 1);
    vector<int> in_degree(n + 1, 0);

    for (int i = 0; i < m; i++) {
        int u, v;
        if (cin >> u >> v) {
            adj[u].push_back(v);
            in_degree[v]++;
        }
    }

    queue<int> q;
    for (int i = 1; i <= n; i++) {
        if (in_degree[i] == 0) q.push(i);
    }

    vector<int> topo_order;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        topo_order.push_back(u);

        for (int v : adj[u]) {
            if (--in_degree[v] == 0) {
                q.push(v);
            }
        }
    }

    if (topo_order.size() != (size_t)n) {
        cout << "Cycle detected: Graph is not a DAG\\n";
        return 0;
    }

    for (size_t i = 0; i < topo_order.size(); i++) {
        cout << topo_order[i] << (i + 1 == topo_order.size() ? "" : " ");
    }
    cout << "\\n";

    return 0;
}
`;
    } else if (algoId === 'kruskal' || step.capabilityId === 'minimum_spanning_tree') {
      code = `#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>

using namespace std;

struct Edge {
    int u, v;
    long long weight;
    bool operator<(const Edge& other) const {
        return weight < other.weight;
    }
};

struct DSU {
    vector<int> parent, rank;
    DSU(int n) : parent(n + 1), rank(n + 1, 0) {
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent[i]);
    }
    bool unite(int i, int j) {
        int root_i = find(i);
        int root_j = find(j);
        if (root_i != root_j) {
            if (rank[root_i] < rank[root_j]) swap(root_i, root_j);
            parent[root_j] = root_i;
            if (rank[root_i] == rank[root_j]) rank[root_i]++;
            return true;
        }
        return false;
    }
};

// Minimum Spanning Tree using Kruskal's Algorithm with DSU
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<Edge> edges(m);
    for (int i = 0; i < m; i++) {
        cin >> edges[i].u >> edges[i].v >> edges[i].weight;
    }

    sort(edges.begin(), edges.end());

    DSU dsu(n);
    long long mst_weight = 0;
    int edges_count = 0;

    for (const auto& edge : edges) {
        if (dsu.unite(edge.u, edge.v)) {
            mst_weight += edge.weight;
            edges_count++;
            if (edges_count == n - 1) break;
        }
    }

    cout << mst_weight << "\\n";
    return 0;
}
`;
    } else if (step.capabilityId === 'connected_components') {
      code = `#include <iostream>
#include <vector>
#include <queue>

using namespace std;

// Connected Components in Undirected Graph using BFS
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    if (!(cin >> n >> m) || n <= 0) return 0;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        if (cin >> u >> v) {
            adj[u].push_back(v);
            adj[v].push_back(u);
        }
    }

    vector<bool> visited(n + 1, false);
    int components = 0;

    for (int i = 1; i <= n; i++) {
        if (!visited[i]) {
            components++;
            queue<int> q;
            q.push(i);
            visited[i] = true;
            while (!q.empty()) {
                int u = q.front();
                q.pop();
                for (int v : adj[u]) {
                    if (!visited[v]) {
                        visited[v] = true;
                        q.push(v);
                    }
                }
            }
        }
    }

    cout << components << "\\n";
    return 0;
}
`;
    } else {
      // General BFS/DFS from graph fragments
      code = generateCpp({
        code: 'SUCCESS',
        moduleId: 'graph.bfs.cpp',
        moduleName: 'Graph Traversal',
        message: 'Resolved graph traversal',
        spec: { domain: 'data_structure', structure: { type: 'graph' }, operation: { combined: 'bfs' } }
      } as any);
    }

    return {
      status: 'SUCCESS',
      backendId: 'cp_algorithm_backend',
      capabilityId: step.capabilityId,
      algorithmId: algoId,
      implementationMechanism: step.implementationMechanism,
      generatedCode: code,
      diagnostics: [`Emitted graph solution for ${step.capabilityId} using algorithm ${algoId}`],
      metadata: {
        componentsUsed: step.requiredComponents,
        mechanism: step.implementationMechanism
      }
    };
  }
}

export const GRAPH_ADAPTER = new GraphAlgorithmAdapter();
