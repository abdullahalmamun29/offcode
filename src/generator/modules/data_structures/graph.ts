import { CodeFragment } from '../../codeComposer';

const STRUCT = ``;

export const graph: Record<string, () => CodeFragment> = {
  'create_adjacency_list': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Adds an edge.
void addEdge(std::vector<std::vector<int>>& adj, int u, int v) {
    adj[u].push_back(v);
    adj[v].push_back(u);
}`],
    mainCode: `int vertices, edges, u, v;
    std::cin >> vertices >> edges;
    std::vector<std::vector<int>> adj(vertices);
    for (int i = 0; i < edges; ++i) {
        std::cin >> u >> v;
        addEdge(adj, u, v);
    }`
  }),
  'bfs': () => ({
    includes: ['iostream', 'vector', 'queue'],
    structs: [STRUCT],
    functions: [
`// BFS traversal.
void bfs(const std::vector<std::vector<int>>& adj, int start) {
    std::vector<bool> visited(adj.size(), false);
    std::queue<int> q;
    visited[start] = true;
    q.push(start);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        std::cout << u << " ";
        for (int v : adj[u]) {
            if (!visited[v]) {
                visited[v] = true;
                q.push(v);
            }
        }
    }
    std::cout << "\\n";
}`],
    mainCode: `int vertices = 5;
    std::vector<std::vector<int>> adj(vertices); // assume populated
    bfs(adj, 0);`
  }),
  'dfs': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// DFS traversal helper.
void dfsUtil(const std::vector<std::vector<int>>& adj, int u, std::vector<bool>& visited) {
    visited[u] = true;
    std::cout << u << " ";
    for (int v : adj[u]) {
        if (!visited[v]) dfsUtil(adj, v, visited);
    }
}
// Starts DFS.
void dfs(const std::vector<std::vector<int>>& adj, int start) {
    std::vector<bool> visited(adj.size(), false);
    dfsUtil(adj, start, visited);
    std::cout << "\\n";
}`],
    mainCode: `int vertices = 5;
    std::vector<std::vector<int>> adj(vertices); // assume populated
    dfs(adj, 0);`
  }),
  'display': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Displays adjacency list.
void display(const std::vector<std::vector<int>>& adj) {
    for (size_t i = 0; i < adj.size(); ++i) {
        std::cout << i << ": ";
        for (int v : adj[i]) std::cout << v << " ";
        std::cout << "\\n";
    }
}`],
    mainCode: `int vertices = 5;
    std::vector<std::vector<int>> adj(vertices); // assume populated
    display(adj);`
  })
};
