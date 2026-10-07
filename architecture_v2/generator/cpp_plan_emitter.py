"""
Universal C++17 Plan Emitter for Architecture V2.

CRITICAL INVARIANT:
Consumes ONLY a typed VerifiedPlanIR. Contains ZERO branches inspecting natural language,
problem text, or high-level problem classifications.
Emits clean, compiling ISO C++17 from bound capability providers and dataflow ports.
"""

from typing import Dict, Any, List
from architecture_v2.universal_contracts import (
    VerifiedPlanIR, InputRepresentationKind, CppTypeDescriptor,
    AlgebraicStructure, AlgebraicOp
)
from architecture_v2.tree_providers import PROVIDER_MAP


class CppPlanEmitter:
    """
    Translates VerifiedPlanIR into clean, compiling C++17 source code.
    """

    @classmethod
    def emit(cls, plan_ir: VerifiedPlanIR) -> str:
        headers = [
            "#include <iostream>",
            "#include <vector>",
            "#include <algorithm>",
            "#include <queue>",
            "#include <string>",
            "#include <cmath>"
        ]
        if plan_ir.recursion_guard:
            headers.append("#include <sys/resource.h>")

        headers_block = "\n".join(headers)

        declarations: List[str] = []
        setup_calls: List[str] = []

        # 1. Collect declarations and setup from bound pipeline steps
        for step in plan_ir.pipeline_steps:
            provider = PROVIDER_MAP.get(step.provider_id)
            if provider:
                fragment = provider.emit_cpp_fragment(step.parameters, plan_ir.payload_spec)
                if fragment.get("declarations"):
                    declarations.append(fragment["declarations"].strip())
                if fragment.get("setup"):
                    setup_calls.append(fragment["setup"].strip())

        declarations_block = "\n\n".join(declarations)
        setup_block = "\n    ".join(setup_calls)

        # 2. Render input reading block based on InputRepresentationKind
        carrier = plan_ir.payload_spec.carrier_type.value if plan_ir.payload_spec.carrier_type != CppTypeDescriptor.NONE else "long long"

        if plan_ir.input_representation == InputRepresentationKind.PARENT_ARRAY:
            read_input_block = f"""
    int n;
    if (!(cin >> n) || n <= 0) return 0;
    adj.assign(n + 1, vector<int>());
    for (int i = 2; i <= n; i++) {{
        int p;
        cin >> p;
        adj[p].push_back(i);
        adj[i].push_back(p);
    }}
"""
        elif plan_ir.input_representation == InputRepresentationKind.ADJACENCY_LIST:
            read_input_block = f"""
    int n;
    if (!(cin >> n) || n <= 0) return 0;
    adj.assign(n + 1, vector<int>());
    for (int u = 1; u <= n; u++) {{
        int degree;
        cin >> degree;
        for (int j = 0; j < degree; j++) {{
            int v;
            cin >> v;
            adj[u].push_back(v);
        }}
    }}
"""
        else:
            # Default: standard edge list
            read_input_block = f"""
    int n;
    if (!(cin >> n) || n <= 0) return 0;
    adj.assign(n + 1, vector<int>());
    for (int i = 0; i < n - 1; i++) {{
        int u, v;
        if (cin >> u >> v) {{
            adj[u].push_back(v);
            adj[v].push_back(u);
        }}
    }}
"""

        if plan_ir.has_vertex_weights:
            uses_mis = any(s.provider_id == "provider:tree_dp_subtrees" for s in plan_ir.pipeline_steps)
            uses_prefix = any(s.provider_id == "provider:lca_prefix_difference" for s in plan_ir.pipeline_steps)
            if uses_mis:
                read_input_block += f"""
    vertex_weight.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) {{
        cin >> vertex_weight[i];
    }}
"""
            elif uses_prefix:
                read_input_block += f"""
    node_val.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) {{
        cin >> node_val[i];
    }}
"""

        # 3. Render Query Handling Block
        query_blocks = []
        for qh in plan_ir.query_handlers:
            if qh.emit_action == "lca_queries":
                query_blocks.append("""
    int q;
    if (cin >> q) {
        while (q--) {
            int u, v;
            cin >> u >> v;
            cout << query_lca(u, v) << "\\n";
        }
    }
""")
            elif qh.emit_action == "path_aggregate_queries":
                query_blocks.append("""
    int q;
    if (cin >> q) {
        while (q--) {
            int u, v;
            cin >> u >> v;
            cout << query_path_aggregate(u, v) << "\\n";
        }
    }
""")
            elif qh.emit_action == "subtree_aggregate_queries":
                query_blocks.append("""
    SubtreeFenwick fenwick(n);
    int q;
    if (cin >> q) {
        while (q--) {
            int u;
            cin >> u;
            cout << fenwick.query_range(tin[u], tout[u]) << "\\n";
        }
    }
""")
            elif qh.emit_action == "distance_queries":
                query_blocks.append("""
    int q;
    if (cin >> q) {
        while (q--) {
            int u, v;
            cin >> u >> v;
            cout << query_tree_distance(u, v) << "\\n";
        }
    }
""")
            elif qh.emit_action == "kth_ancestor_queries":
                query_blocks.append("""
    int q;
    if (cin >> q) {
        while (q--) {
            int u, k;
            cin >> u >> k;
            cout << get_kth_ancestor(u, k) << "\\n";
        }
    }
""")
            elif qh.emit_action == "diameter_output":
                query_blocks.append("""
    cout << compute_tree_diameter(n) << "\\n";
""")
            elif qh.emit_action == "subtree_size_output":
                query_blocks.append("""
    for (int i = 1; i <= n; i++) {
        cout << subtree_size[i] << (i == n ? "" : " ");
    }
    cout << "\\n";
""")
            elif qh.emit_action == "traversal_output":
                query_blocks.append("""
    for (int i = 0; i < (int)traversal_result.size(); i++) {
        cout << traversal_result[i] << (i + 1 == (int)traversal_result.size() ? "" : " ");
    }
    cout << "\\n";
""")
            elif qh.emit_action == "tree_difference_batch":
                query_blocks.append(f"""
    int q;
    if (cin >> q) {{
        while (q--) {{
            int u, v;
            {carrier} x;
            cin >> u >> v >> x;
            apply_path_difference_update(u, v, x);
        }}
    }}
    accumulate_tree_difference(tree_root);
    for (int i = 1; i <= n; i++) {{
        cout << final_values[i] << (i == n ? "" : " ");
    }}
    cout << "\\n";
""")
            elif qh.emit_action == "tree_dp_mis_output":
                query_blocks.append("""
    cout << max(dp_mis[tree_root][0], dp_mis[tree_root][1]) << "\\n";
""")
            elif qh.emit_action == "all_roots_output":
                query_blocks.append("""
    for (int i = 1; i <= n; i++) {
        cout << reroot_ans[i] << (i == n ? "" : " ");
    }
    cout << "\\n";
""")

        query_loop_block = "\n".join(query_blocks)

        recursion_setup = ""
        if plan_ir.recursion_guard:
            recursion_setup = """
    // Stack expansion for deep recursion (N >= 10^5)
    struct rlimit rlim;
    if (getrlimit(RLIMIT_STACK, &rlim) == 0) {
        rlim.rlim_cur = 256 * 1024 * 1024;
        setrlimit(RLIMIT_STACK, &rlim);
    }
"""

        cpp_code = f"""{headers_block}

using namespace std;

{declarations_block}

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
{recursion_setup}
{read_input_block}
    {setup_block}
{query_loop_block}
    return 0;
}}
"""
        return cpp_code
