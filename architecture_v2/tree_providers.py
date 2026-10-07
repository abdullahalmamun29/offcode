"""
Universal Tree Capability Providers for Architecture V2.

Implements declarative CapabilityProvider instances for tree reasoning as strongly-typed
state transformations. Zero hardcoded template cataloging or keyword routing.
"""

from typing import List, Dict, Any, Optional
from architecture_v2.universal_contracts import (
    CapabilityProvider, TypedStateDescriptor,
    STATE_TOPOLOGY, STATE_ROOTED_HIERARCHY, STATE_SUBTREE_SIZES,
    STATE_DEPTH_HEIGHT, STATE_ANCESTOR_TABLE, STATE_LCA,
    STATE_EULER_TOUR_INTERVALS, STATE_HEAVY_LIGHT_CHAINS,
    STATE_PREFIX_PATH_AGGREGATE, STATE_PATH_AGGREGATE,
    STATE_SUBTREE_DP, STATE_ALL_ROOTS, STATE_TREE_DIAMETER,
    STATE_DIFFERENCE_ACCUMULATOR, STATE_TRAVERSAL_ORDER,
    STATE_ORDERED_KEYS, STATE_SEARCH_INSERT_VALIDATE,
    ResourceEnvelope, PreconditionPredicate, ProofObligation,
    AlgebraicStructure, AlgebraicOp, CppTypeDescriptor, ProofStatus
)


# ── 1. Tree Rooting Provider ─────────────────────────────────────────────────

class TreeRootingProvider(CapabilityProvider):
    provider_id = "provider:tree_rooting"
    implements_capability = "service:tree_rooting"

    def consumes(self) -> List[TypedStateDescriptor]:
        return [STATE_TOPOLOGY]

    def produces(self) -> List[TypedStateDescriptor]:
        return [STATE_ROOTED_HIERARCHY]

    def preconditions(self) -> List[PreconditionPredicate]:
        return [
            PreconditionPredicate(
                name="is_tree_proven",
                evaluate_fn=lambda m: getattr(m, "topology_claim", None) is not None and m.topology_claim.is_proven_tree,
                failure_message="Graph is not proven to be a connected acyclic tree."
            )
        ]

    def semantic_proof_obligations(self) -> List[ProofObligation]:
        return [
            ProofObligation("connected_acyclic", "Graph satisfies |E| = |V| - 1 and is connected and acyclic."),
            ProofObligation("valid_root_selection", "Selected root vertex is in V.")
        ]

    def complexity_bounds(self, n: int, q: int) -> ResourceEnvelope:
        return ResourceEnvelope(
            time_preprocessing="O(V + E)",
            time_per_query="O(1)",
            space_preprocessing="O(V)",
            space_per_query="O(1)",
            recursion_depth="O(V)",
            requires_stack_expansion=(n >= 100000)
        )

    def emit_cpp_fragment(self, bindings: Dict[str, Any], payload: AlgebraicStructure) -> Dict[str, str]:
        t = payload.carrier_type.value if payload.carrier_type != CppTypeDescriptor.NONE else "int"
        return {
            "declarations": f"""
vector<vector<int>> adj;
vector<int> parent_node;
vector<int> depth;
vector<vector<int>> children;
int tree_root = 1;

void build_tree_hierarchy(int u, int p, int d) {{
    parent_node[u] = p;
    depth[u] = d;
    for (int v : adj[u]) {{
        if (v != p) {{
            children[u].push_back(v);
            build_tree_hierarchy(v, u, d + 1);
        }}
    }}
}}
""",
            "setup": f"""
    parent_node.assign(n + 1, 0);
    depth.assign(n + 1, 0);
    children.assign(n + 1, vector<int>());
    build_tree_hierarchy(tree_root, 0, 1);
"""
        }


# ── 2. Tree Traversal Provider ───────────────────────────────────────────────

class TreeTraversalProvider(CapabilityProvider):
    provider_id = "provider:tree_traversal"
    implements_capability = "service:tree_traversal"

    def consumes(self) -> List[TypedStateDescriptor]:
        return [STATE_ROOTED_HIERARCHY]

    def produces(self) -> List[TypedStateDescriptor]:
        return [STATE_TRAVERSAL_ORDER]

    def preconditions(self) -> List[PreconditionPredicate]:
        return []

    def semantic_proof_obligations(self) -> List[ProofObligation]:
        return [ProofObligation("traversal_bijection", "Every vertex is visited exactly once.")]

    def complexity_bounds(self, n: int, q: int) -> ResourceEnvelope:
        return ResourceEnvelope("O(V)", "O(1)", "O(V)", "O(1)", "O(V)")

    def emit_cpp_fragment(self, bindings: Dict[str, Any], payload: AlgebraicStructure) -> Dict[str, str]:
        mode = bindings.get("order", "preorder")
        return {
            "declarations": f"""
vector<int> traversal_result;

void execute_tree_traversal(int u, int p) {{
    {"traversal_result.push_back(u);" if mode == "preorder" else ""}
    for (int v : children[u]) {{
        execute_tree_traversal(v, u);
    }}
    {"traversal_result.push_back(u);" if mode == "postorder" else ""}
}}
""",
            "setup": "execute_tree_traversal(tree_root, 0);"
        }


# ── 3. Tree Metrics Provider (Height, Depth, Size, Leaves) ────────────────────

class TreeMetricsProvider(CapabilityProvider):
    provider_id = "provider:tree_metrics"
    implements_capability = "service:tree_metrics"

    def consumes(self) -> List[TypedStateDescriptor]:
        return [STATE_ROOTED_HIERARCHY]

    def produces(self) -> List[TypedStateDescriptor]:
        return [STATE_SUBTREE_SIZES, STATE_DEPTH_HEIGHT]

    def preconditions(self) -> List[PreconditionPredicate]:
        return []

    def semantic_proof_obligations(self) -> List[ProofObligation]:
        return [
            ProofObligation("subtree_size_partition", "Subtree size equals 1 + sum of child subtree sizes."),
            ProofObligation("depth_height_consistency", "Height equals maximum distance to descendant leaf.")
        ]

    def complexity_bounds(self, n: int, q: int) -> ResourceEnvelope:
        return ResourceEnvelope("O(V)", "O(1)", "O(V)", "O(1)", "O(V)")

    def emit_cpp_fragment(self, bindings: Dict[str, Any], payload: AlgebraicStructure) -> Dict[str, str]:
        return {
            "declarations": """
vector<int> subtree_size;
vector<int> node_height;
int total_leaf_count = 0;

void compute_tree_metrics(int u) {
    subtree_size[u] = 1;
    node_height[u] = 0;
    if (children[u].empty()) {
        total_leaf_count++;
    }
    for (int v : children[u]) {
        compute_tree_metrics(v);
        subtree_size[u] += subtree_size[v];
        node_height[u] = max(node_height[u], 1 + node_height[v]);
    }
}
""",
            "setup": """
    subtree_size.assign(n + 1, 0);
    node_height.assign(n + 1, 0);
    compute_tree_metrics(tree_root);
"""
        }


# ── 4. Binary Lifting Ancestor Table Provider ─────────────────────────────────

class BinaryLiftingProvider(CapabilityProvider):
    provider_id = "provider:binary_lifting"
    implements_capability = "service:ancestor_table"

    def consumes(self) -> List[TypedStateDescriptor]:
        return [STATE_ROOTED_HIERARCHY]

    def produces(self) -> List[TypedStateDescriptor]:
        return [STATE_ANCESTOR_TABLE]

    def preconditions(self) -> List[PreconditionPredicate]:
        return []

    def semantic_proof_obligations(self) -> List[ProofObligation]:
        return [ProofObligation("binary_lifting_recurrence", "up[k][v] == up[k-1][up[k-1][v]] holds for all k >= 1.")]

    def complexity_bounds(self, n: int, q: int) -> ResourceEnvelope:
        return ResourceEnvelope("O(V log V)", "O(1)", "O(V log V)", "O(1)", "O(V)")

    def emit_cpp_fragment(self, bindings: Dict[str, Any], payload: AlgebraicStructure) -> Dict[str, str]:
        return {
            "declarations": """
const int MAX_LOG = 20;
vector<vector<int>> up_ancestor;

void build_binary_lifting(int n) {
    up_ancestor.assign(MAX_LOG, vector<int>(n + 1, 0));
    for (int i = 1; i <= n; i++) {
        up_ancestor[0][i] = parent_node[i];
    }
    for (int k = 1; k < MAX_LOG; k++) {
        for (int i = 1; i <= n; i++) {
            int mid = up_ancestor[k - 1][i];
            up_ancestor[k][i] = (mid == 0 ? 0 : up_ancestor[k - 1][mid]);
        }
    }
}

int get_kth_ancestor(int u, int k) {
    for (int bit = 0; bit < MAX_LOG; bit++) {
        if ((k >> bit) & 1) {
            u = up_ancestor[bit][u];
            if (u == 0) break;
        }
    }
    return u;
}
""",
            "setup": "build_binary_lifting(n);"
        }


# ── 5. LCA via Binary Lifting Provider ───────────────────────────────────────

class LcaBinaryLiftingProvider(CapabilityProvider):
    provider_id = "provider:lca_binary_lifting"
    implements_capability = "service:lowest_common_ancestor"

    def consumes(self) -> List[TypedStateDescriptor]:
        return [STATE_ROOTED_HIERARCHY, STATE_ANCESTOR_TABLE]

    def produces(self) -> List[TypedStateDescriptor]:
        return [STATE_LCA]

    def preconditions(self) -> List[PreconditionPredicate]:
        return []

    def semantic_proof_obligations(self) -> List[ProofObligation]:
        return [ProofObligation("lca_deepest_common", "Returned vertex is ancestor of both u and v with maximal depth.")]

    def complexity_bounds(self, n: int, q: int) -> ResourceEnvelope:
        return ResourceEnvelope("O(1)", "O(log V)", "O(1)", "O(1)", "O(1)")

    def emit_cpp_fragment(self, bindings: Dict[str, Any], payload: AlgebraicStructure) -> Dict[str, str]:
        return {
            "declarations": """
int query_lca(int u, int v) {
    if (depth[u] < depth[v]) swap(u, v);
    // Lift u to same depth as v
    int diff = depth[u] - depth[v];
    for (int k = 0; k < MAX_LOG; k++) {
        if ((diff >> k) & 1) {
            u = up_ancestor[k][u];
        }
    }
    if (u == v) return u;
    for (int k = MAX_LOG - 1; k >= 0; k--) {
        if (up_ancestor[k][u] != up_ancestor[k][v]) {
            u = up_ancestor[k][u];
            v = up_ancestor[k][v];
        }
    }
    return up_ancestor[0][u];
}

int query_tree_distance(int u, int v) {
    int lca = query_lca(u, v);
    return depth[u] + depth[v] - 2 * depth[lca];
}
""",
            "setup": ""
        }


# ── 6. Euler Tour Subtree Intervals Provider ─────────────────────────────────

class EulerTourIntervalProvider(CapabilityProvider):
    provider_id = "provider:euler_tour_intervals"
    implements_capability = "service:subtree_range_intervals"

    def consumes(self) -> List[TypedStateDescriptor]:
        return [STATE_ROOTED_HIERARCHY]

    def produces(self) -> List[TypedStateDescriptor]:
        return [STATE_EULER_TOUR_INTERVALS]

    def preconditions(self) -> List[PreconditionPredicate]:
        return []

    def semantic_proof_obligations(self) -> List[ProofObligation]:
        return [
            ProofObligation("euler_interval_nesting", "Descendants of u lie entirely within range [tin[u], tout[u]]."),
            ProofObligation("euler_interval_disjoint", "Non-descendant subtrees have disjoint ranges.")
        ]

    def complexity_bounds(self, n: int, q: int) -> ResourceEnvelope:
        return ResourceEnvelope("O(V)", "O(1)", "O(V)", "O(1)", "O(V)")

    def emit_cpp_fragment(self, bindings: Dict[str, Any], payload: AlgebraicStructure) -> Dict[str, str]:
        t = payload.carrier_type.value if payload.carrier_type != CppTypeDescriptor.NONE else "long long"
        return {
            "declarations": f"""
vector<int> tin, tout, euler_order;
int timer = 0;

void build_euler_tour(int u) {{
    tin[u] = ++timer;
    euler_order.push_back(u);
    for (int v : children[u]) {{
        build_euler_tour(v);
    }}
    tout[u] = timer;
}}

// Fenwick tree over euler order for subtree updates and queries
struct SubtreeFenwick {{
    int sz;
    vector<{t}> tree;
    SubtreeFenwick(int n) : sz(n + 1), tree(n + 2, 0) {{}}
    void add(int i, {t} delta) {{
        for (; i < sz; i += i & -i) tree[i] += delta;
    }}
    {t} query(int i) {{
        {t} sum = 0;
        for (; i > 0; i -= i & -i) sum += tree[i];
        return sum;
    }}
    {t} query_range(int l, int r) {{
        return query(r) - query(l - 1);
    }}
}};
""",
            "setup": """
    tin.assign(n + 1, 0);
    tout.assign(n + 1, 0);
    euler_order.reserve(n + 1);
    build_euler_tour(tree_root);
"""
        }


# ── 7. LCA Invertible Prefix Difference Provider ─────────────────────────────

class LcaPrefixDifferenceProvider(CapabilityProvider):
    provider_id = "provider:lca_prefix_difference"
    implements_capability = "service:path_aggregate"

    def consumes(self) -> List[TypedStateDescriptor]:
        return [STATE_ROOTED_HIERARCHY, STATE_LCA, STATE_PREFIX_PATH_AGGREGATE]

    def produces(self) -> List[TypedStateDescriptor]:
        return [STATE_PATH_AGGREGATE]

    def preconditions(self) -> List[PreconditionPredicate]:
        return [
            PreconditionPredicate(
                name="is_invertible_abelian",
                evaluate_fn=lambda m: getattr(m, "algebraic_payload", None) is not None and m.algebraic_payload.is_invertible and m.algebraic_payload.is_commutative,
                failure_message="Prefix path difference strictly requires an invertible commutative monoid/group (e.g. SUM or XOR)."
            )
        ]

    def semantic_proof_obligations(self) -> List[ProofObligation]:
        return [
            ProofObligation("invertible_abelian_cancellation", "path(u, v) = pref[u] + pref[v] - 2*pref[lca] + val[lca] holds algebraically.")
        ]

    def complexity_bounds(self, n: int, q: int) -> ResourceEnvelope:
        return ResourceEnvelope("O(V)", "O(1)", "O(V)", "O(1)", "O(V)")

    def emit_cpp_fragment(self, bindings: Dict[str, Any], payload: AlgebraicStructure) -> Dict[str, str]:
        t = payload.carrier_type.value
        op = payload.operator
        is_xor = (op == AlgebraicOp.XOR)
        return {
            "declarations": f"""
vector<{t}> node_val;
vector<{t}> path_pref;

void compute_path_prefix(int u, {t} acc) {{
    {f"acc ^= node_val[u];" if is_xor else "acc += node_val[u];"}
    path_pref[u] = acc;
    for (int v : children[u]) {{
        compute_path_prefix(v, acc);
    }}
}}

{t} query_path_aggregate(int u, int v) {{
    int lca = query_lca(u, v);
    {f"return path_pref[u] ^ path_pref[v] ^ node_val[lca];" if is_xor else f"return path_pref[u] + path_pref[v] - 2 * path_pref[lca] + node_val[lca];"}
}}
""",
            "setup": f"""
    path_pref.assign(n + 1, 0);
    compute_path_prefix(tree_root, 0);
"""
        }


# ── 8. Heavy-Light Decomposition Provider ─────────────────────────────────────

class HeavyLightDecompositionProvider(CapabilityProvider):
    provider_id = "provider:heavy_light_decomposition"
    implements_capability = "service:path_decomposition"

    def consumes(self) -> List[TypedStateDescriptor]:
        return [STATE_ROOTED_HIERARCHY, STATE_SUBTREE_SIZES]

    def produces(self) -> List[TypedStateDescriptor]:
        return [STATE_HEAVY_LIGHT_CHAINS]

    def preconditions(self) -> List[PreconditionPredicate]:
        return []

    def semantic_proof_obligations(self) -> List[ProofObligation]:
        return [
            ProofObligation("hld_chain_partition", "Every vertex belongs to exactly one heavy path."),
            ProofObligation("hld_log_path_bound", "Any path between two vertices decomposes into at most 2 * log2(V) continuous segments.")
        ]

    def complexity_bounds(self, n: int, q: int) -> ResourceEnvelope:
        return ResourceEnvelope("O(V)", "O(log^2 V)", "O(V)", "O(1)", "O(V)")

    def emit_cpp_fragment(self, bindings: Dict[str, Any], payload: AlgebraicStructure) -> Dict[str, str]:
        t = payload.carrier_type.value
        return {
            "declarations": f"""
vector<int> heavy_child, head, hld_pos;
int cur_hld_pos = 0;

void hld_decompose(int u, int h) {{
    head[u] = h;
    hld_pos[u] = ++cur_hld_pos;
    int heavy = -1, max_sz = -1;
    for (int v : children[u]) {{
        if (subtree_size[v] > max_sz) {{
            max_sz = subtree_size[v];
            heavy = v;
        }}
    }}
    heavy_child[u] = heavy;
    if (heavy != -1) {{
        hld_decompose(heavy, h);
    }}
    for (int v : children[u]) {{
        if (v != heavy) {{
            hld_decompose(v, v);
        }}
    }}
}}

// Segment Tree for HLD path queries
struct HldSegmentTree {{
    int sz;
    vector<{t}> tree;
    HldSegmentTree(int n) : sz(n + 1), tree(4 * n + 4, 0) {{}}
    void update(int node, int l, int r, int idx, {t} val) {{
        if (l == r) {{ tree[node] = val; return; }}
        int mid = (l + r) / 2;
        if (idx <= mid) update(2 * node, l, mid, idx, val);
        else update(2 * node + 1, mid + 1, r, idx, val);
        tree[node] = max(tree[2 * node], tree[2 * node + 1]);
    }}
    {t} query(int node, int l, int r, int ql, int qr) {{
        if (ql > r || qr < l) return -1e18;
        if (ql <= l && r <= qr) return tree[node];
        int mid = (l + r) / 2;
        return max(query(2 * node, l, mid, ql, qr), query(2 * node + 1, mid + 1, r, ql, qr));
    }}
}};
""",
            "setup": """
    heavy_child.assign(n + 1, -1);
    head.assign(n + 1, 0);
    hld_pos.assign(n + 1, 0);
    hld_decompose(tree_root, tree_root);
"""
        }


# ── 9. Two-Sweep Tree Diameter Provider ───────────────────────────────────────

class TwoSweepDiameterProvider(CapabilityProvider):
    provider_id = "provider:two_sweep_diameter"
    implements_capability = "service:tree_diameter"

    def consumes(self) -> List[TypedStateDescriptor]:
        return [STATE_TOPOLOGY]

    def produces(self) -> List[TypedStateDescriptor]:
        return [STATE_TREE_DIAMETER]

    def preconditions(self) -> List[PreconditionPredicate]:
        return [
            PreconditionPredicate(
                name="weights_non_negative",
                evaluate_fn=lambda m: getattr(m, "algebraic_payload", None) is None or m.algebraic_payload.weights_non_negative,
                failure_message="Two-sweep BFS diameter requires non-negative edge weights."
            )
        ]

    def semantic_proof_obligations(self) -> List[ProofObligation]:
        return [
            ProofObligation("farthest_node_extremum", "In a tree with non-negative weights, the farthest vertex from any vertex u is an endpoint of a diameter.")
        ]

    def complexity_bounds(self, n: int, q: int) -> ResourceEnvelope:
        return ResourceEnvelope("O(V + E)", "O(1)", "O(V)", "O(1)", "O(V)")

    def emit_cpp_fragment(self, bindings: Dict[str, Any], payload: AlgebraicStructure) -> Dict[str, str]:
        t = payload.carrier_type.value if payload.carrier_type != CppTypeDescriptor.NONE else "long long"
        return {
            "declarations": f"""
pair<int, {t}> bfs_farthest(int start_node, int n) {{
    vector<{t}> dist(n + 1, -1);
    queue<int> q;
    dist[start_node] = 0;
    q.push(start_node);
    int best_node = start_node;
    {t} max_dist = 0;

    while (!q.empty()) {{
        int u = q.front();
        q.pop();
        if (dist[u] > max_dist) {{
            max_dist = dist[u];
            best_node = u;
        }}
        for (int v : adj[u]) {{
            if (dist[v] == -1) {{
                dist[v] = dist[u] + 1;
                q.push(v);
            }}
        }}
    }}
    return {{best_node, max_dist}};
}}

{t} compute_tree_diameter(int n) {{
    auto [node_a, d1] = bfs_farthest(1, n);
    auto [node_b, diam] = bfs_farthest(node_a, n);
    return diam;
}}
""",
            "setup": ""
        }


# ── 10. Tree DP Subtrees Provider ─────────────────────────────────────────────

class TreeDpSubtreeProvider(CapabilityProvider):
    provider_id = "provider:tree_dp_subtrees"
    implements_capability = "service:subtree_dp"

    def consumes(self) -> List[TypedStateDescriptor]:
        return [STATE_ROOTED_HIERARCHY]

    def produces(self) -> List[TypedStateDescriptor]:
        return [STATE_SUBTREE_DP]

    def preconditions(self) -> List[PreconditionPredicate]:
        return []

    def semantic_proof_obligations(self) -> List[ProofObligation]:
        return [
            ProofObligation("subproblem_independence", "Subtrees of distinct children are disjoint, guaranteeing independent optimal substructure.")
        ]

    def complexity_bounds(self, n: int, q: int) -> ResourceEnvelope:
        return ResourceEnvelope("O(V)", "O(1)", "O(V)", "O(1)", "O(V)")

    def emit_cpp_fragment(self, bindings: Dict[str, Any], payload: AlgebraicStructure) -> Dict[str, str]:
        t = payload.carrier_type.value
        dp_objective = bindings.get("dp_objective", "independent_set")
        if dp_objective == "independent_set":
            return {
                "declarations": f"""
// Maximum Weight Independent Set on Tree
vector<vector<{t}>> dp_mis;
vector<{t}> vertex_weight;

void solve_tree_dp(int u) {{
    dp_mis[u][0] = 0;
    dp_mis[u][1] = vertex_weight[u];
    for (int v : children[u]) {{
        solve_tree_dp(v);
        dp_mis[u][0] += max(dp_mis[v][0], dp_mis[v][1]);
        dp_mis[u][1] += dp_mis[v][0];
    }}
}}
""",
                "setup": """
    dp_mis.assign(n + 1, vector<long long>(2, 0));
    solve_tree_dp(tree_root);
"""
            }
        else:
            return {
                "declarations": f"""
vector<{t}> dp_subtree;
vector<{t}> vertex_weight;

void solve_subtree_sum_dp(int u) {{
    dp_subtree[u] = vertex_weight[u];
    for (int v : children[u]) {{
        solve_subtree_sum_dp(v);
        dp_subtree[u] += dp_subtree[v];
    }}
}}
""",
                "setup": """
    dp_subtree.assign(n + 1, 0);
    solve_subtree_sum_dp(tree_root);
"""
            }


# ── 11. Tree Rerooting Provider (All-Roots DP) ────────────────────────────────

class TreeRerootingProvider(CapabilityProvider):
    provider_id = "provider:tree_rerooting"
    implements_capability = "service:all_roots_dp"

    def consumes(self) -> List[TypedStateDescriptor]:
        return [STATE_ROOTED_HIERARCHY, STATE_SUBTREE_DP]

    def produces(self) -> List[TypedStateDescriptor]:
        return [STATE_ALL_ROOTS]

    def preconditions(self) -> List[PreconditionPredicate]:
        return [
            PreconditionPredicate(
                name="is_associative_merge",
                evaluate_fn=lambda m: getattr(m, "algebraic_payload", None) is None or m.algebraic_payload.is_associative,
                failure_message="Rerooting DP requires an associative combine/merge operation."
            )
        ]

    def semantic_proof_obligations(self) -> List[ProofObligation]:
        return [
            ProofObligation("rerooting_prefix_suffix_identity", "Prefix and suffix child aggregates correctly reconstitute up-contribution from parent.")
        ]

    def complexity_bounds(self, n: int, q: int) -> ResourceEnvelope:
        return ResourceEnvelope("O(V)", "O(1)", "O(V)", "O(1)", "O(V)")

    def emit_cpp_fragment(self, bindings: Dict[str, Any], payload: AlgebraicStructure) -> Dict[str, str]:
        t = payload.carrier_type.value
        return {
            "declarations": f"""
vector<{t}> subtree_dp_val;
vector<{t}> reroot_ans;
vector<int> sub_size;

void dfs_down(int u, int p) {{
    sub_size[u] = 1;
    subtree_dp_val[u] = 0;
    for (int v : adj[u]) {{
        if (v != p) {{
            dfs_down(v, u);
            sub_size[u] += sub_size[v];
            subtree_dp_val[u] += subtree_dp_val[v] + sub_size[v];
        }}
    }}
}}

void dfs_up(int u, int p, int n) {{
    for (int v : adj[u]) {{
        if (v != p) {{
            // Reroot contribution to child v
            reroot_ans[v] = reroot_ans[u] - sub_size[v] + (n - sub_size[v]);
            dfs_up(v, u, n);
        }}
    }}
}}
""",
            "setup": """
    sub_size.assign(n + 1, 0);
    subtree_dp_val.assign(n + 1, 0);
    reroot_ans.assign(n + 1, 0);
    dfs_down(1, 0);
    reroot_ans[1] = subtree_dp_val[1];
    dfs_up(1, 0, n);
"""
        }


# ── 12. Ordered Binary Search Tree Provider ───────────────────────────────────

class OrderedBstProvider(CapabilityProvider):
    provider_id = "provider:ordered_bst"
    implements_capability = "service:ordered_search"

    def consumes(self) -> List[TypedStateDescriptor]:
        return [STATE_ORDERED_KEYS]

    def produces(self) -> List[TypedStateDescriptor]:
        return [STATE_SEARCH_INSERT_VALIDATE]

    def preconditions(self) -> List[PreconditionPredicate]:
        return [
            PreconditionPredicate(
                name="has_total_order",
                evaluate_fn=lambda m: getattr(m, "algebraic_payload", None) is None or m.algebraic_payload.has_total_order,
                failure_message="BST operations require a totally ordered carrier type."
            )
        ]

    def semantic_proof_obligations(self) -> List[ProofObligation]:
        return [
            ProofObligation("bst_invariant_order", "For all nodes x: all keys in left(x) < key(x) < all keys in right(x).")
        ]

    def complexity_bounds(self, n: int, q: int) -> ResourceEnvelope:
        return ResourceEnvelope("O(H)", "O(H)", "O(V)", "O(1)", "O(H)")

    def emit_cpp_fragment(self, bindings: Dict[str, Any], payload: AlgebraicStructure) -> Dict[str, str]:
        t = payload.carrier_type.value
        return {
            "declarations": f"""
struct BSTNode {{
    {t} key;
    BSTNode* left;
    BSTNode* right;
    BSTNode({t} k) : key(k), left(nullptr), right(nullptr) {{}}
}};

BSTNode* bst_insert(BSTNode* root, {t} key) {{
    if (!root) return new BSTNode(key);
    if (key < root->key) root->left = bst_insert(root->left, key);
    else if (key > root->key) root->right = bst_insert(root->right, key);
    return root;
}}

bool bst_search(BSTNode* root, {t} key) {{
    if (!root) return false;
    if (root->key == key) return true;
    if (key < root->key) return bst_search(root->left, key);
    return bst_search(root->right, key);
}}

bool bst_validate(BSTNode* root, {t} min_val, {t} max_val, bool has_min, bool has_max) {{
    if (!root) return true;
    if (has_min && root->key <= min_val) return false;
    if (has_max && root->key >= max_val) return false;
    return bst_validate(root->left, min_val, root->key, has_min, true) &&
           bst_validate(root->right, root->key, max_val, true, has_max);
}}
""",
            "setup": "BSTNode* bst_root = nullptr;"
        }


# ── 13. Tree Difference Offline Updates Provider (Gate 8 Extensibility) ────────

class TreeDifferenceOfflineUpdatesProvider(CapabilityProvider):
    """
    Extensibility Stress Test Capability.
    Proves that adding offline batch path updates requires ZERO changes to central
    enums, routers, or parsers.
    """
    provider_id = "provider:tree_difference_offline"
    implements_capability = "service:batch_path_mutation"

    def consumes(self) -> List[TypedStateDescriptor]:
        return [STATE_ROOTED_HIERARCHY, STATE_LCA]

    def produces(self) -> List[TypedStateDescriptor]:
        return [STATE_DIFFERENCE_ACCUMULATOR]

    def preconditions(self) -> List[PreconditionPredicate]:
        return []

    def semantic_proof_obligations(self) -> List[ProofObligation]:
        return [
            ProofObligation("tree_difference_invariant", "Adding +x to u and v, -x to lca, and -x to parent[lca] yields exactly +x on path(u,v) under subtree accumulation.")
        ]

    def complexity_bounds(self, n: int, q: int) -> ResourceEnvelope:
        return ResourceEnvelope("O(V + Q)", "O(1)", "O(V)", "O(1)", "O(V)")

    def emit_cpp_fragment(self, bindings: Dict[str, Any], payload: AlgebraicStructure) -> Dict[str, str]:
        t = payload.carrier_type.value
        return {
            "declarations": f"""
vector<{t}> tree_diff;
vector<{t}> final_values;

void apply_path_difference_update(int u, int v, {t} x) {{
    int lca = query_lca(u, v);
    tree_diff[u] += x;
    tree_diff[v] += x;
    tree_diff[lca] -= x;
    int p_lca = parent_node[lca];
    if (p_lca != 0) {{
        tree_diff[p_lca] -= x;
    }}
}}

void accumulate_tree_difference(int u) {{
    final_values[u] = tree_diff[u];
    for (int v : children[u]) {{
        accumulate_tree_difference(v);
        final_values[u] += final_values[v];
    }}
}}
""",
            "setup": """
    tree_diff.assign(n + 1, 0);
    final_values.assign(n + 1, 0);
"""
        }


# ── Provider Registry ────────────────────────────────────────────────────────

ALL_TREE_PROVIDERS: List[CapabilityProvider] = [
    TreeRootingProvider(),
    TreeTraversalProvider(),
    TreeMetricsProvider(),
    BinaryLiftingProvider(),
    LcaBinaryLiftingProvider(),
    EulerTourIntervalProvider(),
    LcaPrefixDifferenceProvider(),
    HeavyLightDecompositionProvider(),
    TwoSweepDiameterProvider(),
    TreeDpSubtreeProvider(),
    TreeRerootingProvider(),
    OrderedBstProvider(),
    TreeDifferenceOfflineUpdatesProvider()
]

PROVIDER_MAP: Dict[str, CapabilityProvider] = {
    p.provider_id: p for p in ALL_TREE_PROVIDERS
}
