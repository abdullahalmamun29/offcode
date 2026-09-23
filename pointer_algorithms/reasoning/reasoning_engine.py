"""
Modular Reasoning Engine for Pointer-Based and Trie Algorithmic Reasoning.

Decouples reasoning domains so Trie and Binary Trie reasoning are not shoehorned
into monotonicity:
- MonotonicityReasoning: ordered space reduction and single-transition boundary logic
- GreedyChoiceReasoning: mathematical dominance proof for Binary Trie XOR bit choices
- StateTransitionReasoning: deterministic automaton prefix state traversal and aggregation
- InvariantReasoning: structural, multiplicity, terminal, and safe pruning invariants
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Tuple
from pointer_algorithms.reasoning.monotonicity_engine import (
    MonotonicityEngine, MonotonicityAssessment, MonotonicityKind, MonotonicityStatus
)

@dataclass
class GreedyChoiceProof:
    bit_width: int
    dominant_property: str
    mathematical_justification: str
    requires_backtracking: bool = False

@dataclass
class StateTransitionProof:
    alphabet_kind: str
    transition_formula: str
    prefix_sharing_property: str
    time_complexity_per_op: str
    space_complexity_upper_bound: str

@dataclass
class TrieInvariantSet:
    structural_invariant: str
    multiplicity_invariant: str
    safe_pruning_invariant: str
    terminal_state_invariant: str

class MonotonicityReasoning:
    """Explains single-transition boundary conditions and search-space halving."""

    @staticmethod
    def assess_monotonicity(
        pattern: str,
        has_negative_values: bool,
        is_sorted: bool,
        can_sort: bool,
        is_contiguous: bool,
        tracks_distinct: bool = False,
        objective_type: str = "",
        tracks_distinct_or_frequencies: bool = False
    ) -> MonotonicityAssessment:
        return MonotonicityEngine.assess_for_pattern(
            pattern=pattern,
            has_negative_values=has_negative_values,
            is_sorted=is_sorted,
            can_sort=can_sort,
            is_contiguous=is_contiguous,
            tracks_distinct=tracks_distinct,
            objective_type=objective_type,
            tracks_distinct_or_frequencies=tracks_distinct_or_frequencies
        )

    @staticmethod
    def explain_single_transition_boundary() -> str:
        return (
            "A monotonic predicate P: S -> {0, 1} partitions an ordered search space S "
            "into at most two contiguous subranges: S_0 = {x in S | P(x) = 0} and S_1 = {x in S | P(x) = 1}. "
            "Because this partition admits exactly one boundary transition, evaluating the midpoint mid "
            "of current interval [L, R] determines definitively which half contains the boundary, "
            "safely discarding the other half without candidate loss."
        )

class GreedyChoiceReasoning:
    """
    Mathematical justification for Binary Trie bit-matching decisions.
    
    Proves why choosing the opposite bit (1 - bit) at position k strictly dominates
    any combination of decisions on lower bits 0..k-1.
    """

    @staticmethod
    def prove_xor_greedy_choice(bit_width: int = 32) -> GreedyChoiceProof:
        return GreedyChoiceProof(
            bit_width=bit_width,
            dominant_property="Bitwise XOR Strict Power-of-Two Dominance",
            mathematical_justification=(
                f"For any bit position k in [0, {bit_width - 1}], the contribution of bit k to the XOR sum is 2^k. "
                f"The maximum sum obtainable from all strictly lower bit positions is sum_{{j=0}}^{{k-1}} 2^j = 2^k - 1 < 2^k. "
                "Therefore, securing bit 1 at position k by taking the opposite bit branch (1 - b) strictly yields a larger "
                "result than choosing bit 0 at position k and achieving bit 1 at every subsequent position 0..k-1. "
                "Consequently, the greedy choice at each bit level is globally optimal, and no backtracking is required."
            ),
            requires_backtracking=False
        )

class StateTransitionReasoning:
    """
    Automaton state transition and prefix aggregation reasoning for Tries.
    """

    @staticmethod
    def explain_prefix_traversal(alphabet: str = "lowercase_26") -> StateTransitionProof:
        return StateTransitionProof(
            alphabet_kind=alphabet,
            transition_formula="state(u, c) = child[u][c], where P(child[u][c]) = P(u) + c",
            prefix_sharing_property=(
                "Prefix sharing merges identical initial string prefixes into shared directed paths. "
                "All words with prefix P share the unique path from root to node u where P(u) = P."
            ),
            time_complexity_per_op="O(L) where L is string length, independent of dictionary size N",
            space_complexity_upper_bound="O(total_characters * sizeof(pointer) + metadata)"
        )

class InvariantReasoning:
    """
    Defines and checks 4-phase invariants for Trie and Binary Trie data structures.
    """

    @staticmethod
    def get_trie_invariants() -> TrieInvariantSet:
        return TrieInvariantSet(
            structural_invariant=(
                "Root node represents the empty string epsilon. Every node u at depth d uniquely represents "
                "the prefix formed by the path of character edges from root to u."
            ),
            multiplicity_invariant=(
                "For every node u: pass_count(u) equals the total number of active words in the dictionary "
                "that have P(u) as a prefix. word_count(u) equals the exact multiplicity of word P(u)."
            ),
            safe_pruning_invariant=(
                "A node u may be safely pruned/deleted from memory if and only if pass_count(u) == 0, "
                "word_count(u) == 0, and all child pointers are null. Decrementing pass_count on path during deletion "
                "ensures no other word's path is accidentally unlinked."
            ),
            terminal_state_invariant=(
                "A node u is terminal (represents a complete word in the dictionary) if and only if word_count(u) > 0. "
                "Prefix queries require pass_count(u) > 0; exact search queries require word_count(u) > 0."
            )
        )


@dataclass
class RecursiveStateProof:
    state_definition: str
    base_case: str
    child_aggregation: str
    transition_merge: str
    return_or_global_update: str
    extensible_direction: str  # 'bottom_up', 'top_down', 'rerooted'


class RecursiveStateReasoning:
    """
    Formally derives and structures recursive state definitions for Tree DP and aggregations.
    
    Provides formal decomposition into:
    - state definition: tuple or scalar S(u) representing optimal or aggregate property of subtree T_u
    - base case: leaf nodes or null pointers
    - child aggregation: combination over all children v in children(u)
    - transition/merge: integrating local node attributes with aggregated child states
    - return/update: bubble-up value or global optimal answer update
    """

    @staticmethod
    def bottom_up_state(
        state_name: str,
        recurrence: str,
        base_case: str,
        merge_op: str = "sum"
    ) -> RecursiveStateProof:
        return RecursiveStateProof(
            state_definition=f"{state_name}(u) = summary of subtree rooted at node u",
            base_case=base_case,
            child_aggregation=f"combine over all children v in children(u) via {merge_op}",
            transition_merge=recurrence,
            return_or_global_update=f"returns {state_name}(u) to parent; updates global answer if path or diameter",
            extensible_direction="bottom_up"
        )

    @staticmethod
    def top_down_state(
        state_name: str,
        inheritance: str,
        base_case: str
    ) -> RecursiveStateProof:
        return RecursiveStateProof(
            state_definition=f"{state_name}(u) = accumulated property from root to node u",
            base_case=base_case,
            child_aggregation="push parent state S(u) down to each child v",
            transition_merge=inheritance,
            return_or_global_update="records leaf evaluation or verifies root-to-leaf path predicate",
            extensible_direction="top_down"
        )

    @staticmethod
    def rerooted_state(
        down_state: str,
        up_state: str,
        combine_formula: str
    ) -> RecursiveStateProof:
        return RecursiveStateProof(
            state_definition=f"ans(u) = answer when tree is rooted at u, derived from down(u) and up(u)",
            base_case="Pass 1: standard bottom-up DFS from arbitrary root r",
            child_aggregation="Pass 2: top-down DFS passing rerooted complement state from parent to child",
            transition_merge=combine_formula,
            return_or_global_update=f"computes all-roots answers in O(N) total time without recomputing from scratch",
            extensible_direction="rerooted"
        )


class HierarchyReasoning:
    """
    Mathematical structural properties and validation proofs for trees.
    """

    @staticmethod
    def prove_connected_acyclic(n: int, edge_count: int, is_connected: bool) -> Dict[str, Any]:
        """
        Proof: An undirected graph with N vertices and N-1 edges is connected iff it is acyclic.
        """
        if edge_count != n - 1:
            if edge_count >= n:
                return {
                    "is_tree": False,
                    "reason": "CYCLIC",
                    "explanation": f"Graph has {n} vertices and {edge_count} edges (E >= N). By the cyclomatic number formula (gamma = E - V + C), any connected component with E >= V contains at least {edge_count - n + 1} fundamental cycles."
                }
            else:
                return {
                    "is_tree": False,
                    "reason": "DISCONNECTED",
                    "explanation": f"Graph has {n} vertices and {edge_count} edges (E < N - 1). It cannot be connected; it forms a forest of at least {n - edge_count} disconnected components."
                }
        if not is_connected:
            return {
                "is_tree": False,
                "reason": "DISCONNECTED",
                "explanation": f"Graph has N-1 edges but is explicitly disconnected, forming disconnected components with cycles."
            }
        return {
            "is_tree": True,
            "reason": "VALID_TREE",
            "explanation": "Graph has N vertices, N-1 edges, and is connected, guaranteeing a uniquely path-connected acyclic tree."
        }


class ParentChildInvariant:
    """
    Reasoning for undirected tree traversal avoiding visited[] array overhead.
    """

    @staticmethod
    def explain_parent_tracking() -> str:
        return (
            "In an undirected tree (N vertices, N-1 edges, acyclic), for any node u and its designated parent p, "
            "the neighbor set adj[u] contains exactly p (unless u is root) and all children of u. "
            "Because a tree contains no cycles, no back-edges or cross-edges exist. "
            "Therefore, guarding recursive calls with `if (v != p)` strictly prevents re-traversing into the parent, "
            "guaranteeing each undirected edge is crossed exactly once in each direction in O(N) time "
            "without requiring a visited boolean array or hash set."
        )


class SubtreeAggregation:
    """
    Formal specification and algebra of subtree aggregations.
    
    state(u) = combine(local(u), bigoplus_{v in children(u)} state(v))
    """

    AGGREGATION_NEUTRAL_ELEMENTS = {
        "sum": 0,
        "count": 0,
        "size": 0,
        "height": -1,  # or 0 depending on 0-indexed vs 1-indexed
        "min": float("inf"),
        "max": float("-inf"),
        "xor": 0,
        "or": 0,
        "and": ~0,
        "boolean_all": True,
        "boolean_any": False,
    }

    @classmethod
    def get_neutral_element(cls, op: str) -> Any:
        return cls.AGGREGATION_NEUTRAL_ELEMENTS.get(op.lower(), 0)

    @staticmethod
    def explain_aggregation(op: str) -> str:
        op_lower = op.lower()
        if op_lower in ("size", "subtree_size"):
            return "size(u) = 1 + sum_{v in children(u)} size(v). Leaf base case: size(leaf) = 1; null = 0."
        if op_lower in ("height", "depth", "max_depth"):
            return "height(u) = 1 + max_{v in children(u)} height(v). Leaf base case: height(leaf) = 0; null = -1."
        if op_lower in ("sum", "subtree_sum"):
            return "sum(u) = val[u] + sum_{v in children(u)} sum(v). Neutral element: 0."
        if op_lower in ("min", "subtree_min"):
            return "min(u) = min(val[u], min_{v in children(u)} min(v)). Neutral element: +infinity."
        if op_lower in ("max", "subtree_max"):
            return "max(u) = max(val[u], max_{v in children(u)} max(v)). Neutral element: -infinity."
        if op_lower in ("diameter", "tree_diameter"):
            return (
                "diameter(u) = max(max_{v} diameter(v), depth1(u) + depth2(u)), where depth1 and depth2 "
                "are the two largest child branch depths. Tracked globally during postorder depth aggregation."
            )
        return f"state(u) = combine(val[u], fold_{{v in children(u)}}(state(v))) using associative operator '{op}'."


# ──────────────────────────────────────────────────────────────────────────
# Phase 3F — Graph Reasoning Classes
# ──────────────────────────────────────────────────────────────────────────

@dataclass
class GraphStructuralAnalysis:
    vertex_count: int
    edge_count_estimate: str
    density: str          # 'sparse' | 'dense' | 'unknown'
    directed: str         # 'directed' | 'undirected' | 'unknown'
    euler_poincare: str   # formal invariant statement


class GraphStructuralReasoning:
    """
    Structural analysis of a graph's vertex/edge invariants and density classification.
    Cyclomatic number (cycle rank): gamma = E - V + C for general graphs with C components.
    Handshaking Lemma: sum(deg(v)) = 2E for undirected graphs, sum(in_deg(v)) = sum(out_deg(v)) = E for directed graphs.
    """

    @staticmethod
    def analyze(
        vertex_count: int,
        edge_count: Optional[int] = None,
        is_directed: bool = False
    ) -> GraphStructuralAnalysis:
        directed_str = "directed" if is_directed else "undirected"
        if edge_count is not None:
            density = "dense" if edge_count > vertex_count * vertex_count // 4 else "sparse"
            euler = (
                f"For connected {directed_str} graph G = (V, E): "
                f"V = {vertex_count}, E ≈ {edge_count}. "
                f"Cyclomatic number: gamma = E - V + C (fundamental cycles). Tree iff E = V - 1 (connected, acyclic, gamma = 0). "
                f"Handshaking Lemma: sum(deg(v)) = 2E."
            )
            ec_str = str(edge_count)
        else:
            density = "unknown"
            euler = (
                f"For {directed_str} graph G = (V, E): V = {vertex_count}. "
                "E unknown; density classification requires E. "
                "Tree iff E = V - 1, connected, acyclic (gamma = 0)."
            )
            ec_str = "unknown"
        return GraphStructuralAnalysis(
            vertex_count=vertex_count,
            edge_count_estimate=ec_str,
            density=density,
            directed=directed_str,
            euler_poincare=euler
        )


@dataclass
class ShortestPathDecision:
    selected_algorithm: str
    justification: str
    time_complexity: str
    conditions: List[str]


class ShortestPathDecisionReasoning:
    """
    Formally selects the appropriate shortest path algorithm based on graph properties.
    Selection rules:
      Unweighted graph → BFS: O(V + E)
      Non-negative weights → Dijkstra: O((V + E) log V)
      Negative weights, no negative cycle → Bellman-Ford: O(V * E)
      DAG (topological order) → DAG-DP: O(V + E)
      All-pairs, V ≤ 400 → Floyd-Warshall: O(V^3)
    """

    @staticmethod
    def decide(
        is_weighted: bool,
        has_negative_weights: bool,
        has_negative_cycles: bool,
        is_dag: Optional[bool],
        is_all_pairs: bool = False,
        vertex_count: int = 1000
    ) -> ShortestPathDecision:
        if is_all_pairs and vertex_count <= 500:
            return ShortestPathDecision(
                selected_algorithm="graph_floyd_warshall",
                justification=(
                    f"All-pairs shortest path with V = {vertex_count} <= 500. "
                    "Floyd-Warshall O(V^3) is feasible and handles negative weights (no negative cycles)."
                ),
                time_complexity="O(V^3)",
                conditions=["all_pairs_query", f"vertex_count={vertex_count}<=500"]
            )
        if not is_weighted:
            return ShortestPathDecision(
                selected_algorithm="graph_bfs_shortest_path",
                justification=(
                    "Graph is unweighted. BFS expands in non-decreasing hop distance, "
                    "discovering shortest paths in O(V + E) without a priority queue."
                ),
                time_complexity="O(V + E)",
                conditions=["unweighted_graph"]
            )
        if is_dag is True and not has_negative_cycles:
            return ShortestPathDecision(
                selected_algorithm="graph_dag_dp",
                justification=(
                    "Graph is a DAG. Process vertices in topological order; relax outgoing edges. "
                    "Handles negative edge weights without cycling. O(V + E)."
                ),
                time_complexity="O(V + E)",
                conditions=["is_dag", "topological_order_relax"]
            )
        if has_negative_weights:
            if has_negative_cycles:
                return ShortestPathDecision(
                    selected_algorithm="negative_cycle_detection",
                    justification=(
                        "A reachable negative cycle exists. Shortest path is undefined/unbounded on the source→target path. "
                        "Bellman-Ford detects the cycle (V-th round relaxation still succeeds) but cannot produce finite distances."
                    ),
                    time_complexity="O(V * E)",
                    conditions=["negative_weights", "reachable_negative_cycle"]
                )
            return ShortestPathDecision(
                selected_algorithm="graph_bellman_ford",
                justification=(
                    "Graph has negative edge weights. Dijkstra requires non-negative weights. "
                    "Bellman-Ford relaxes all E edges V-1 times, guaranteeing correctness with O(V*E) time."
                ),
                time_complexity="O(V * E)",
                conditions=["negative_weights", "no_negative_cycle"]
            )
        return ShortestPathDecision(
            selected_algorithm="graph_dijkstra",
            justification=(
                "Graph is weighted with non-negative edge weights. "
                "Dijkstra's algorithm uses a min-priority queue to greedily settle the nearest unvisited vertex. "
                "Greedy invariant: once dist[u] is settled, it is optimal (no negative edges can improve it). "
                "O((V + E) log V) with binary heap."
            ),
            time_complexity="O((V + E) log V)",
            conditions=["weighted_graph", "non_negative_weights"]
        )


@dataclass
class CycleReasoningProof:
    graph_type: str
    method: str
    state_definition: str
    cycle_condition: str
    correctness_argument: str


class CycleReasoning:
    """
    Distinguishes undirected cycle detection from directed cycle detection.
    Undirected: visited + parent tracking DFS.
    Directed: 3-color DFS state (UNVISITED=0, VISITING=1, VISITED=2).
    """

    @staticmethod
    def explain_undirected() -> CycleReasoningProof:
        return CycleReasoningProof(
            graph_type="undirected",
            method="visited_parent_dfs",
            state_definition="visited[v] ∈ {False, True}; parent[v] = predecessor in DFS tree",
            cycle_condition=(
                "For each neighbor w of v: if visited[w] is True and w ≠ parent[v], "
                "then edge (v, w) is a back-edge forming a cycle."
            ),
            correctness_argument=(
                "In an undirected graph, the only way to reach an already-visited node v "
                "without going through the DFS parent is via a non-tree back-edge, which closes a cycle. "
                "Checking w ≠ parent[v] prevents confusing the bidirectional tree edge with a cycle."
            )
        )

    @staticmethod
    def explain_directed() -> CycleReasoningProof:
        return CycleReasoningProof(
            graph_type="directed",
            method="three_color_dfs",
            state_definition="color[v] ∈ {UNVISITED=0, VISITING=1, VISITED=2}",
            cycle_condition=(
                "For each neighbor w of v: if color[w] == VISITING (1), "
                "then edge (v, w) is a back-edge in the DFS tree, forming a directed cycle."
            ),
            correctness_argument=(
                "VISITING=1 marks nodes currently in the DFS call stack (ancestors of v). "
                "A back-edge to a VISITING node closes a directed cycle. "
                "VISITED=2 marks nodes fully processed — edges to them are forward or cross edges, not cycles. "
                "Parent tracking alone is insufficient for directed graphs because multiple paths may exist."
            )
        )


@dataclass
class BipartiteReasoningProof:
    coloring_method: str
    invariant: str
    impossibility_condition: str
    complexity: str


class BipartiteReasoning:
    """
    2-coloring BFS/DFS for bipartite verification.
    Theorem: A graph is bipartite iff it contains no odd-length cycle.
    """

    @staticmethod
    def explain() -> BipartiteReasoningProof:
        return BipartiteReasoningProof(
            coloring_method="bfs_2_coloring",
            invariant=(
                "Assign color[source] = 0. For each edge (u, v): color[v] = 1 - color[u]. "
                "Invariant: for all edges (u, v) in the same connected component, color[u] ≠ color[v]."
            ),
            impossibility_condition=(
                "If during BFS/DFS, an edge (u, v) is found where color[u] == color[v] and both are visited, "
                "then u and v are in the same partition, which forms an odd-length cycle. "
                "Theorem: G is bipartite ⟺ G contains no odd-length cycle."
            ),
            complexity="O(V + E) — visits each vertex and edge at most once"
        )


@dataclass
class TopologicalSortProof:
    method: str
    dag_theorem: str
    cycle_detection: str
    complexity: str


class TopologicalSortReasoning:
    """
    Kahn's indegree peeling and DFS postorder reversal for topological ordering.
    Theorem: A finite directed graph has a topological ordering iff it is acyclic (DAG).
    """

    @staticmethod
    def explain_kahn() -> TopologicalSortProof:
        return TopologicalSortProof(
            method="kahn_indegree_peeling",
            dag_theorem=(
                "A finite directed graph G = (V, E) has a topological ordering iff it is a DAG. "
                "Proof: if a cycle exists, no vertex in the cycle can appear first (it has an incoming edge). "
                "Conversely, a DAG always has at least one vertex with in-degree 0."
            ),
            cycle_detection=(
                "After Kahn's algorithm, if the number of processed vertices < V, "
                "then the remaining vertices form a cycle (all have in-degree >= 1 in the residual graph)."
            ),
            complexity="O(V + E) — processes each vertex and edge exactly once"
        )

    @staticmethod
    def explain_dfs_postorder() -> TopologicalSortProof:
        return TopologicalSortProof(
            method="dfs_postorder_reversal",
            dag_theorem=(
                "In DFS on a DAG, every edge (u, v) satisfies: DFS finishes v before u "
                "(because v is a descendant of u or processed independently). "
                "Reversing postorder completion times yields a valid topological ordering."
            ),
            cycle_detection=(
                "A back-edge (edge to a VISITING ancestor) implies a cycle. "
                "DFS with 3-color detection: if color[v] == VISITING, cycle found."
            ),
            complexity="O(V + E)"
        )


@dataclass
class DSUProof:
    path_compression: str
    union_by_rank: str
    amortized_complexity: str
    connectivity_invariant: str


class DSUReasoning:
    """
    Disjoint Set Union with path compression and union by rank/size.
    Amortized complexity: O(α(V)) per operation where α is the inverse Ackermann function.
    """

    @staticmethod
    def explain() -> DSUProof:
        return DSUProof(
            path_compression=(
                "find(x): while parent[x] ≠ x, set parent[x] = parent[parent[x]] (path halving) or "
                "parent[x] = find(parent[x]) (full path compression). "
                "Flattens the tree so future finds are O(1) amortized."
            ),
            union_by_rank=(
                "union(x, y): find roots rx, ry. If rank[rx] < rank[ry], parent[rx] = ry. "
                "Else if rank[rx] > rank[ry], parent[ry] = rx. Else parent[ry] = rx, rank[rx]++. "
                "Ensures tree height stays O(log V) before path compression."
            ),
            amortized_complexity=(
                "With both path compression and union by rank, any sequence of M operations on V elements "
                "runs in O(M * α(V)) total time, where α(V) ≤ 4 for all practical V. "
                "Effectively O(1) amortized per operation."
            ),
            connectivity_invariant=(
                "Invariant: find(x) == find(y) iff x and y are in the same connected component. "
                "union(x, y) merges the components of x and y in O(α(V)) amortized time."
            )
        )


@dataclass
class MSTProof:
    cut_property: str
    cycle_property: str
    kruskal_argument: str
    prim_argument: str


class MSTReasoning:
    """
    Cut property and cycle property proofs for Kruskal's and Prim's MST algorithms.
    """

    @staticmethod
    def explain() -> MSTProof:
        return MSTProof(
            cut_property=(
                "Cut Property: For any cut (S, V\\S) of connected graph G, "
                "the minimum-weight crossing edge e* is guaranteed to be in every MST. "
                "Proof by exchange: assume e* is not in MST T. Adding e* creates a cycle in T. "
                "This cycle must contain another crossing edge e'. w(e*) < w(e') by minimality. "
                "Swap e' for e*: obtain spanning tree with smaller total weight — contradicting T being MST."
            ),
            cycle_property=(
                "Cycle Property: For any cycle C in G, the maximum-weight edge e_max in C is NOT in any MST. "
                "Proof: Suppose e_max is in MST T. Removing e_max splits T into two components S, V\\S. "
                "C has another edge e' crossing (S, V\\S) with w(e') < w(e_max). "
                "Swapping e_max for e' gives a lighter spanning tree — contradiction."
            ),
            kruskal_argument=(
                "Kruskal's: Sort edges by weight. Add edge e = (u, v) if u and v are in different DSU components. "
                "Correctness: each added edge is the minimum crossing edge for the cut at time of addition (Cut Property). "
                "Time: O(E log E) for sorting + O(E * α(V)) for DSU = O(E log E)."
            ),
            prim_argument=(
                "Prim's: Maintain set S of vertices in MST. At each step, add the minimum-weight edge (u, v) "
                "with u ∈ S, v ∉ S (minimum crossing edge of cut (S, V\\S)). "
                "Correctness: Cut Property guarantees each added edge is in the MST. "
                "Time: O((V + E) log V) with binary heap."
            )
        )


@dataclass
class SCCProof:
    mutual_reachability: str
    tarjan_method: str
    condensation_dag: str
    complexity: str


class SCCReasoning:
    """
    Strongly Connected Components via Tarjan's algorithm using DFS low-link values.
    """

    @staticmethod
    def explain() -> SCCProof:
        return SCCProof(
            mutual_reachability=(
                "Definition: u and v are in the same SCC iff there exists a path u→v and v→u. "
                "SCCs partition V into maximal subsets with mutual reachability."
            ),
            tarjan_method=(
                "Tarjan's SCC: DFS with discovery time tin[v] and low[v] = min(tin[v], min tin of descendants "
                "reachable via back-edges). Maintain a stack. When DFS finishes v and low[v] == tin[v], "
                "v is an SCC root: pop stack until v, yielding one SCC."
            ),
            condensation_dag=(
                "Condensation DAG: Contract each SCC to a single node. All inter-SCC edges go from "
                "SCC containing the source to SCC containing the target. The condensation is always a DAG. "
                "Post-order SCC numbering gives reverse topological order of condensation DAG."
            ),
            complexity="O(V + E) — each vertex and edge visited once in Tarjan's DFS"
        )


@dataclass
class BridgeArticulationProof:
    bridge_condition: str
    articulation_condition: str
    low_link_definition: str
    complexity: str


class BridgeArticulationReasoning:
    """
    DFS tree low-link values for bridges and articulation points.
    Bridge condition: low[v] > tin[u] for edge (u, v).
    Articulation point condition: root with >= 2 DFS children, or non-root with low[v] >= tin[u].
    """

    @staticmethod
    def explain() -> BridgeArticulationProof:
        return BridgeArticulationProof(
            low_link_definition=(
                "tin[v] = discovery time of v in DFS. "
                "low[v] = min(tin[v], min(tin[w] for back-edges v→w), min(low[c] for tree-edge children c of v)). "
                "low[v] represents the earliest-discovered vertex reachable from the subtree rooted at v."
            ),
            bridge_condition=(
                "Edge (u, v) is a bridge iff low[v] > tin[u]. "
                "Proof: If low[v] > tin[u], the subtree rooted at v has no back-edge to u or any ancestor of u. "
                "Removing (u, v) disconnects v's subtree from the rest of the graph."
            ),
            articulation_condition=(
                "Vertex u is an articulation point iff: "
                "(1) u is the DFS root and has >= 2 children in the DFS tree, OR "
                "(2) u is not the root and has a child v with low[v] >= tin[u]. "
                "Condition (2): v's subtree has no back-edge to a proper ancestor of u, "
                "so removing u disconnects v's subtree."
            ),
            complexity="O(V + E) — single DFS pass with tin and low arrays"
        )


# ── Heap Structural Reasoning (Phase 3G) ──

@dataclass
class HeapStructuralProof:
    heap_property: str
    extremal_access: str
    sift_up_complexity: str
    sift_down_complexity: str
    bottom_up_heapify_complexity: str
    heap_vs_sorted_array_tradeoff: str
    heap_vs_bst_tradeoff: str
    retention_invariant_top_k: str
    priority_frontier_abstraction: str


class HeapStructuralReasoning:
    """
    Structural reasoning for binary heap and priority queue algorithms (Phase 3G).
    Grounds operations in the fundamental dynamic candidate set + extremal element access abstraction.
    """

    @staticmethod
    def explain(kind: str = "min_heap") -> HeapStructuralProof:
        if kind == "max_heap":
            property_desc = (
                "Max-Heap Invariant: For every node i > 0, A[parent(i)] >= A[i]. "
                "The root A[0] is the global maximum. Children satisfy the same invariant recursively."
            )
            retention_desc = (
                "Top-K Smallest: To maintain the K smallest elements in an incoming stream, "
                "retain a candidate set of size K in a MAX-HEAP. When a new element x arrives, "
                "if x < max_heap.top(), pop the max and push x. The max-heap exposes the weakest "
                "(largest) of the K smallest candidates for O(1) eviction."
            )
        else:
            property_desc = (
                "Min-Heap Invariant: For every node i > 0, A[parent(i)] <= A[i]. "
                "The root A[0] is the global minimum. Children satisfy the same invariant recursively."
            )
            retention_desc = (
                "Top-K Largest: To maintain the K largest elements in an incoming stream, "
                "retain a candidate set of size K in a MIN-HEAP. When a new element x arrives, "
                "if x > min_heap.top(), pop the min and push x. The min-heap exposes the weakest "
                "(smallest) of the K largest candidates for O(1) eviction."
            )

        return HeapStructuralProof(
            heap_property=property_desc,
            extremal_access=(
                "Root access provides the extremum (minimum or maximum) in O(1) time without inspecting children."
            ),
            sift_up_complexity=(
                "O(log N): Insertion places the new element at the leaf (index N) and restores the heap "
                "property by swapping with parent up to tree height ceil(log2 N)."
            ),
            sift_down_complexity=(
                "O(log N): Extraction replaces the root with the last leaf and sifts down by swapping "
                "with the preferred child (min for min-heap, max for max-heap) up to tree height."
            ),
            bottom_up_heapify_complexity=(
                "O(N): Bottom-up Floyd heapify applies sift-down starting from floor(N/2)-1 down to 0. "
                "Total cost is sum_{h=0}^{floor(log N)} ceil(N / 2^{h+1}) * O(h) = O(N)."
            ),
            heap_vs_sorted_array_tradeoff=(
                "Heap provides O(1) peek and O(log N) insert/delete, compared to sorted array which requires "
                "O(N) shift on insertion/deletion. Heap avoids maintaining total order when only extremal access is required."
            ),
            heap_vs_bst_tradeoff=(
                "Heap uses a flat contiguous array with low structural overhead, excellent cache locality, "
                "and fast extremal access. Balanced ordered trees (BST/set/multiset) provide ordered search, "
                "predecessor/successor navigation, and arbitrary-key operations, but incur additional node-level "
                "structural overhead, pointer indirection, and dynamic rebalancing costs. Use BST only when "
                "non-extremal search or range queries are required."
            ),
            retention_invariant_top_k=retention_desc,
            priority_frontier_abstraction=(
                "Priority Frontier: In greedy exploration (Dijkstra, Prim, A*), the heap maintains the frontier "
                "of reachable candidates, dynamically picking the minimum-cost extension in O(log |Frontier|) time."
            )
        )

    @staticmethod
    def derive_top_k_heap_kind(k_direction: str) -> str:
        """
        Derives heap kind for bounded Top-K selection via the retention invariant:
        - To retain the K largest candidates, the weakest candidate to evict is the smallest -> Min-Heap of size K.
        - To retain the K smallest candidates, the weakest candidate to evict is the largest -> Max-Heap of size K.
        """
        if k_direction in ("largest", "maximum", "max", "greatest", "highest"):
            return "min_heap"
        elif k_direction in ("smallest", "minimum", "min", "least", "lowest"):
            return "max_heap"
        return "min_heap"


@dataclass
class DSUStructuralProof:
    dsu_kind: str
    partition_of_universe: str
    representative_invariant: str
    component_metadata_combination: str
    weighted_potential_derivation: str
    parity_xor_derivation: str
    rollback_restoration_invariant: str
    offline_dynamic_connectivity_complexity: str
    limitation_reasoning: str


class DSUStructuralReasoning:
    """
    Advanced Disjoint Set Union / Union-Find Structural Reasoning (Phase 3H).

    Formalizes:
    1. Partition of universe into dynamic equivalence classes
    2. Representative invariant find(x) == find(y) <=> same component
    3. Generic component metadata aggregation across merges
    4. Weighted difference constraints: value[x] - value[y] = w, sign convention,
       root attachment formula: potential[root_x] = w - px + py
    5. Parity / 2-coloring XOR constraints: color[x] ^ color[y] = p,
       root attachment formula: parity[root_x] = p ^ parity_x ^ parity_y
    6. Rollback DSU: union-by-size without path compression, complete state restoration
    7. Offline dynamic connectivity: time segment tree + rollback DSU in O(M log Q log N + Q log N)
    8. Boundary reasoning: rejecting arbitrary online edge deletions (DSU_DELETION_UNSUPPORTED)
    """

    @staticmethod
    def explain(kind: str = "basic") -> DSUStructuralProof:
        return DSUStructuralProof(
            dsu_kind=kind,
            partition_of_universe=(
                "DSU maintains an exact partition of the N-element universe into disjoint equivalence classes. "
                "Every element belongs to exactly one component at all times."
            ),
            representative_invariant=(
                "Representative Invariant: find(x) returns the canonical root of x's component. "
                "x and y belong to the same component if and only if find(x) == find(y). "
                "With path compression and union by rank/size, operations run in O(alpha(N)) amortized time."
            ),
            component_metadata_combination=(
                "Component Metadata Invariant: When distinct components root_x and root_y merge, "
                "metadata[new_root] = combine(metadata[root_x], metadata[root_y]). "
                "The requested component state must be correctly maintainable from the stored metadata "
                "and the available merge operation upon union (e.g. sum, min, max, count, xor)."
            ),
            weighted_potential_derivation=(
                "Weighted Potential Convention: potential[x] = value[x] - value[parent[x]]. "
                "Path compression accumulates potential to root: potential_to_root[x] = value[x] - value[root_x] (shorthand px). "
                "Given constraint value[x] - value[y] = w: "
                "If root_x becomes child of root_y (parent[root_x] = root_y): "
                "potential[root_x] = w + potential_to_root[y] - potential_to_root[x] = w - px + py. "
                "If root_y becomes child of root_x (parent[root_y] = root_x): "
                "potential[root_y] = potential_to_root[x] - potential_to_root[y] - w = px - py - w. "
                "If root_x == root_y and px - py != w, a CONTRADICTION is detected. "
                "Difference query difference(x, y) returns px - py if connected, or UNKNOWN if disconnected."
            ),
            parity_xor_derivation=(
                "Parity XOR Convention: parity[x] = color[x] XOR color[parent[x]] in {0, 1}. "
                "Accumulation to root: parity_to_root[x] = color[x] XOR color[root_x]. "
                "Given constraint color[x] XOR color[y] = p, when attaching root_x to root_y: "
                "parity[root_x] = p XOR parity_to_root[x] XOR parity_to_root[y]. "
                "If root_x == root_y and (parity_to_root[x] XOR parity_to_root[y]) != p, a CONTRADICTION is detected. "
                "Unlike static graph bipartite verification (BFS/DFS), Parity DSU incrementally maintains dynamic 2-coloring."
            ),
            rollback_restoration_invariant=(
                "Rollback Restoration Invariant: Path compression is strictly omitted to preserve history tree structure. "
                "Union by size/rank provides O(log N) find/union. An undo stack records every modification: "
                "parent, size/rank, component count, and all tracked component metadata aggregates. "
                "rollback(snapshot) pops the stack and restores all fields to the exact historical snapshot state in O(1) time per step."
            ),
            offline_dynamic_connectivity_complexity=(
                "Offline Dynamic Connectivity: When the sequence of edge additions, deletions, and connectivity queries is known in advance, "
                "each edge's active lifetime is decomposed into intervals over a segment tree over time (depth O(log Q)). "
                "A DFS traversal over the segment tree activates edges using Rollback DSU (cost O(log N)), answers queries at leaves, "
                "and rolls back edges upon backtracking. Total time complexity is O(M log Q log N + Q log N), "
                "where N = number of vertices, Q = number of time/query operations, and M = number of edge lifetime intervals."
            ),
            limitation_reasoning=(
                "Limitation & Boundary Reasoning: Arbitrary online edge deletion cannot be handled by standard DSU or "
                "Rollback DSU merely because rollback exists. Supported models: additions only -> Basic DSU; "
                "explicit historical rollback -> Rollback DSU; known add/remove timeline -> Offline Dynamic Connectivity. "
                "Arbitrary online edge deletions without an offline batch sequence must be rejected with DSU_DELETION_UNSUPPORTED."
            )
        )

    @staticmethod
    def derive_weighted_union_potential(px: int, py: int, w: int, attach_x_to_y: bool = True) -> int:
        """
        Derives potential[root] when merging two components with constraint:
            value[x] - value[y] = w
        where:
            px = value[x] - value[root_x]
            py = value[y] - value[root_y]

        When attaching root_x below root_y (parent[root_x] = root_y):
            value[root_x] - value[root_y] = (value[x] - px) - (value[y] - py) = w - px + py
        When attaching root_y below root_x (parent[root_y] = root_x):
            value[root_y] - value[root_x] = px - py - w
        """
        if attach_x_to_y:
            return w - px + py
        else:
            return px - py - w

    @staticmethod
    def check_weighted_consistency(px: int, py: int, w: int) -> Tuple[bool, int]:
        """
        Checks consistency when x and y are already in the same component (root_x == root_y).
        Returns (is_consistent, implied_difference).
        """
        implied_diff = px - py
        return (implied_diff == w, implied_diff)

    @staticmethod
    def derive_parity_union(parity_x: int, parity_y: int, p: int) -> int:
        """
        Derives parity[root_x] when attaching root_x below root_y under constraint:
            color[x] ^ color[y] = p
        parity[root_x] = p ^ parity_x ^ parity_y
        """
        return p ^ parity_x ^ parity_y

    @staticmethod
    def check_parity_consistency(parity_x: int, parity_y: int, p: int) -> Tuple[bool, int]:
        """
        Checks parity consistency when x and y are already in the same component.
        Returns (is_consistent, implied_parity).
        """
        implied_parity = parity_x ^ parity_y
        return (implied_parity == p, implied_parity)


# ── Fenwick Tree / Binary Indexed Tree Structural Reasoning (Phase 3I) ──

@dataclass
class FenwickStructuralProof:
    fenwick_kind: str
    algebraic_scope: str
    indexing_convention: str
    prefix_query_derivation: str
    point_update_derivation: str
    range_query_inverse_derivation: str
    difference_array_range_update: str
    two_fenwick_algebraic_derivation: str
    kth_element_binary_lifting: str
    coordinate_compression_pipeline: str
    two_dimensional_fenwick: str
    limitation_and_boundaries: str
    frequency_invariant: str = ""
    inversion_counting_traversal: str = ""
    integer_width_policy: str = ""
    linear_build_derivation: str = ""


class FenwickStructuralReasoning:
    """
    Mathematical and structural foundation for Fenwick Trees (Binary Indexed Trees).
    Formalizes:
    1. Lowbit decomposition: lowbit(i) = i & (-i)
    2. Interval responsibility: node i covers [i - lowbit(i) + 1, i]
    3. Algebraic scope: commutative monoids for prefix aggregation, commutative groups for range queries
    4. Monotonic prefix extremum under restricted non-decreasing/non-increasing updates
    5. Difference-array range update and two-Fenwick range-update/range-query algebraic derivation
    6. K-th element binary lifting in O(log N) on monotonic non-negative frequencies
    7. Coordinate compression pipeline with explicit K, M, Q asymptotic complexity and memory definitions
    8. Dense 2D Fenwick grid updates and submatrix queries in O(log N log M)
    9. Boundary classification: FENWICK_STATIC_QUERY_SUBOPTIMAL, FENWICK_STRUCTURAL_INCOMPATIBILITY,
       FENWICK_DYNAMIC_COORDINATE_UNREPRESENTABLE, FENWICK_RESOURCE_LIMIT, and FENWICK_KTH_NEGATIVE_FREQUENCY
    10. Integer-width policy: 64-bit (`long long`) baseline, 128-bit (`__int128`) when intermediate products overflow
    11. Linear-time build distinction: O(N) ancestor propagation for static arrays vs O(M) dynamic initialization
    """

    @staticmethod
    def explain(kind: str = "point_update_prefix_query") -> FenwickStructuralProof:
        return FenwickStructuralProof(
            fenwick_kind=kind,
            algebraic_scope=(
                "Algebraic Scope & Operation Capability Separation: "
                "Prefix aggregation requires a commutative associative operation with identity (commutative monoid). "
                "Range query from two prefixes requires a suitable inverse under the supported aggregation, "
                "typically a commutative group (e.g. additive group (Z, +, 0) where range(l, r) = prefix(r) - prefix(l-1)). "
                "Prefix extremum is supported only under restricted monotonic point updates: "
                "prefix minimum requires newValue <= oldValue, and prefix maximum requires newValue >= oldValue. "
                "Arbitrary point replacement is unsupported by Fenwick extremum variants (requires Segment Tree for dynamic updates, "
                "or Sparse Table for static arrays)."
            ),
            indexing_convention=(
                "Indexing Convention: The internal Fenwick tree uses 1-based indexing [1..N]. "
                "Each node i stores the aggregate over interval [i - lowbit(i) + 1, i], where lowbit(i) = i & (-i). "
                "External 0-based coordinates are normalized via i_internal = i_external + 1. "
                "Range [l, r] in 0-based coordinates maps to [l + 1, r + 1] in 1-based coordinates."
            ),
            prefix_query_derivation=(
                "Prefix Query Derivation: prefix(i) computes aggregate over [1..i] by repeatedly moving i -= lowbit(i). "
                "Since lowbit(i) extracts the lowest set bit of i, clearing it removes the interval [i - lowbit(i) + 1, i]. "
                "The path visits at most floor(log2(i)) + 1 disjoint intervals covering [1..i] in O(log N) time."
            ),
            point_update_derivation=(
                "Point Update Derivation: add(i, delta) updates all nodes whose responsible intervals cover position i. "
                "Starting at index i, moving i += lowbit(i) visits all strict ancestor intervals in the Fenwick tree. "
                "Each step increases index i while preserving interval coverage, visiting at most floor(log2(N)) + 1 nodes in O(log N) time."
            ),
            range_query_inverse_derivation=(
                "Range Query via Inversion: For commutative groups with inverse operation '-' (such as addition), "
                "range(l, r) is derived from two prefixes as prefix(r) - prefix(l - 1). "
                "This computes the exact sum over [l..r] in O(log N) time. "
                "When aggregation has no suitable inverse, range-from-prefix is structurally incompatible."
            ),
            difference_array_range_update=(
                "Range Update Point Query (Difference Array): Maintains difference array D[i] = A[i] - A[i-1] in Fenwick tree. "
                "Range add [l..r] by delta updates D[l] += delta and D[r + 1] -= delta using two point updates. "
                "Point query A[i] = sum_{j=1}^i D[j] is evaluated in O(log N) via prefix(i) over D."
            ),
            two_fenwick_algebraic_derivation=(
                "Two-Fenwick Range-Update Range-Query Algebraic Formulation: "
                "Using difference array D[j] = A[j] - A[j-1], prefix sum of A is: "
                "prefix(x) = sum_{i=1}^x A[i] = sum_{j=1}^x (x - j + 1) * D[j] = (x + 1) * sum_{j=1}^x D[j] - sum_{j=1}^x j * D[j]. "
                "Maintains two Fenwick trees: B1 tracking D[j] and B2 tracking j * D[j]. "
                "Prefix sum formula: prefix(x) = (x + 1) * query(B1, x) - query(B2, x). "
                "For rangeAdd(l, r, delta), updates are: "
                "B1.add(l, +delta), B1.add(r + 1, -delta), B2.add(l, +l * delta), B2.add(r + 1, -(r + 1) * delta). "
                "Range query range(l, r) = prefix(r) - prefix(l - 1) in O(log N) time."
            ),
            kth_element_binary_lifting=(
                "K-th Element Binary Lifting: Operates on frequency Fenwick with invariant F[x] >= 0 for all x, "
                "ensuring prefix frequencies are monotonic non-decreasing. "
                "If negative frequencies were present, prefix monotonicity would fail and binary lifting would be invalidated; "
                "alternative structures (Segment Tree, balanced ordered structure, order-statistics tree) must be selected depending on requirements. "
                "Given 1 <= k <= totalFrequency, binary lifting inspects powers of 2 descending from 2^(floor(log2(N))) down to 1: "
                "if idx + step <= N and tree[idx + step] < k, then idx += step and k -= tree[idx]. "
                "Returns idx + 1, which is the smallest index whose prefix frequency is >= k, in strictly O(log N) time."
            ),
            coordinate_compression_pipeline=(
                "Coordinate Compression Pipeline: Given K raw coordinates, sort unique values to produce M distinct coordinates. "
                "Mapping: rank(x) = lower_bound(unique_coords.begin(), unique_coords.end(), x) - unique_coords.begin() + 1 in [1..M]. "
                "Complexity: compression O(K log K), Fenwick operations O(Q log M), total time O(K log K + Q log M). "
                "Memory: raw/compression storage O(K + M), Fenwick storage O(M)."
            ),
            two_dimensional_fenwick=(
                "Dense 2D Fenwick Tree: Grid of dimensions N x M with nested lowbit loops. "
                "Node Invariant: T[r][c] stores the aggregate over the 2D interval [r - lowbit(r) + 1, r] x [c - lowbit(c) + 1, c]. "
                "update(x, y, delta) loops x += lowbit(x) and y += lowbit(y) in O(log N log M). "
                "2D prefix sum prefix(x, y) loops x -= lowbit(x) and y -= lowbit(y) in O(log N log M). "
                "Submatrix rectangle sum for [x1..x2] x [y1..y2] via 2D inclusion-exclusion: "
                "prefix(x2, y2) - prefix(x1 - 1, y2) - prefix(x2, y1 - 1) + prefix(x1 - 1, y1 - 1). "
                "Memory complexity is O(NM)."
            ),
            limitation_and_boundaries=(
                "Limitation & Boundary Reasoning: "
                "1. FENWICK_STATIC_QUERY_SUBOPTIMAL: Static array with no updates is functionally valid for Fenwick, "
                "but suboptimal compared to Prefix Sums (O(N) build, O(1) query). "
                "2. FENWICK_OFFLINE_RANGE_ADD_OVERKILL: Batch offline range adds without intermediate queries are better served "
                "by Difference Array (O(1) update, single O(N) sweep). "
                "3. FENWICK_STRUCTURAL_INCOMPATIBILITY: Arbitrary range query requiring subtraction/inversion when aggregation "
                "has no suitable inverse, or arbitrary point replacement on range extremum, or range assignment. "
                "4. FENWICK_DYNAMIC_COORDINATE_UNREPRESENTABLE: Ordinary fixed-index Fenwick is insufficient when dynamically "
                "appearing coordinates cannot be represented in a known index space. The replacement structure depends on "
                "required operations and may include an order-statistics tree, dynamic segment tree, balanced ordered structure, "
                "or another coordinate-aware rank structure. "
                "5. FENWICK_KTH_NEGATIVE_FREQUENCY: Negative frequencies violate monotonicity of prefix counts. "
                "6. FENWICK_RESOURCE_LIMIT: Time or memory budget exceeded (e.g. dense 2D matrix exceeds memory)."
            ),
            frequency_invariant=(
                "Frequency Fenwick Invariant: The underlying frequency array F[v] stores the frequency of value v. "
                "Fenwick node T[i] stores the aggregate frequency over [i - lowbit(i) + 1, i]: "
                "T[i] = sum_{k = i - lowbit(i) + 1}^i F[k]. Range frequency over [l, r] is prefix(r) - prefix(l - 1)."
            ),
            inversion_counting_traversal=(
                "Inversion Counting Traversal: "
                "Right-to-left: Process elements from n down to 1. Query count of values < a[i] in Fenwick tree "
                "(counts elements j > i with a[j] < a[i]), then add a[i] with count +1. "
                "Left-to-right: Process elements from 1 to n. Query count of values > a[i] in Fenwick tree "
                "(evaluated as prefix(max_val) - prefix(a[i]), counting elements j < i with a[j] > a[i]), then add a[i] with count +1."
            ),
            integer_width_policy=(
                "Integer-Width Policy: Standard Fenwick operations use signed 64-bit integers (`long long`) when cumulative sums "
                "and updates are verified to remain within [-2^63, 2^63 - 1]. "
                "When intermediate products can exceed signed 64-bit limits—specifically in Two-Fenwick range updates where "
                "terms like (r + 1) * delta or j * D[j] are computed—128-bit integers (`__int128` in C++) or overflow-safe "
                "arithmetic must be used."
            ),
            linear_build_derivation=(
                "Linear-Time Build vs Dynamic Initialization: "
                "True O(N) build is implemented for static initial arrays in fenwick_point_update_prefix_query by initializing "
                "tree[i] = A[i] and pushing to immediate parent `parent = i + lowbit(i)` if parent <= N (ancestor propagation). "
                "Dynamic structures (frequency Fenwick, multiset, 2D Fenwick) initialize empty in O(M) or O(R x C) time and populate via updates."
            )
        )

    @staticmethod
    def lowbit(i: int) -> int:
        """Returns highest power of 2 dividing i: i & (-i)."""
        return i & (-i)

    @staticmethod
    def to_internal_index(idx: int, is_one_based_input: bool = False) -> int:
        """Centralized index normalization: converts external 0-based or 1-based index to internal 1-based index."""
        if is_one_based_input:
            return idx
        return idx + 1

    @staticmethod
    def derive_two_fenwick_prefix(x: int, q_b1: int, q_b2: int) -> int:
        """Derives prefix sum at position x using Two-Fenwick queries over B1 (D) and B2 (j*D)."""
        return (x + 1) * q_b1 - q_b2

    @staticmethod
    def derive_two_fenwick_range_add_updates(l: int, r: int, delta: int) -> List[Tuple[str, int, int]]:
        """
        Returns exact updates for rangeAdd(l, r, delta) on Two-Fenwick (1-based indices):
        B1: (l, +delta), (r + 1, -delta)
        B2: (l, +l * delta), (r + 1, -(r + 1) * delta)
        """
        return [
            ("B1", l, delta),
            ("B1", r + 1, -delta),
            ("B2", l, l * delta),
            ("B2", r + 1, -(r + 1) * delta)
        ]

    @staticmethod
    def kth_element_search(tree: List[int], k: int, n: int) -> int:
        """
        Binary lifting search on 1-based frequency Fenwick tree for smallest index with prefix_frequency >= k.
        Requires frequency[x] >= 0 and 1 <= k <= total_frequency.
        Runs in O(log N) time.
        """
        idx = 0
        step = 1
        while (step << 1) <= n:
            step <<= 1
        while step > 0:
            if idx + step <= n and tree[idx + step] < k:
                idx += step
                k -= tree[idx]
            step >>= 1
        return idx + 1


# ── Segment Tree Structural Reasoning (Phase 3J) ──

@dataclass
class SegmentTreeStructuralProof:
    segment_tree_kind: str
    interval_decomposition: str
    merge_algebra: str
    identity_elements: str
    lazy_tag_algebra: str
    non_empty_max_subarray: str
    frequency_order_statistic: str
    interval_statistics: str
    memory_representation: str
    integer_width_policy: str
    limitation_and_boundaries: str


class SegmentTreeStructuralReasoning:
    """
    Mathematical and structural foundation for Segment Trees (Phase 3J).
    Formalizes:
    1. Interval decomposition: node u on [l, r] with left child 2u on [l, m] and right child 2u+1 on [m+1, r], m = (l+r)//2.
    2. Associative merge algebra: merge(merge(a, b), c) = merge(a, merge(b, c)). Non-commutative operations strictly supported.
    3. Identity elements: sum -> 0, min -> +INF, max -> -INF, gcd -> 0.
    4. Lazy tag algebra: apply(tag, node), compose(newTag, oldTag), and push. Preserves true node aggregate invariant.
    5. Non-empty maximum subarray: sum, pref, suff, ans with sentinel identity.
    6. Frequency order statistics: O(log M) binary traversal on non-negative frequencies F[x] >= 0.
    7. Interval statistics: (min_val, min_count, max_val, max_count) with associative conditional merge.
    8. Memory representations: conceptual 2N-1, conventional safe recursive 4N, common iterative 2N layouts.
    9. Integer-width policy: 64-bit (`long long`) baseline, `__int128` promotion for (assign_val + add_val) * len.
    10. Candidate elimination: SEGMENT_TREE_STATIC_QUERY_SUBOPTIMAL, SEGMENT_TREE_SIMPLE_PREFIX_OVERKILL,
        SEGMENT_TREE_DIFFERENCE_ARRAY_OVERKILL, SEGMENT_TREE_FENWICK_EQUIVALENT, SEGMENT_TREE_NO_ASSOCIATIVE_MERGE,
        SEGMENT_TREE_LAZY_TAG_UNSUPPORTED, SEGMENT_TREE_RESOURCE_LIMIT.
    """

    @staticmethod
    def explain(kind: str = "point_update_range_query") -> SegmentTreeStructuralProof:
        return SegmentTreeStructuralProof(
            segment_tree_kind=kind,
            interval_decomposition=(
                "Interval Decomposition: A Segment Tree over array A[1..N] is a binary tree where the root at index 1 "
                "represents the entire interval [1, N]. Each node u covering interval [l, r] with length len = r - l + 1 > 1 "
                "is partitioned at midpoint m = floor((l + r) / 2) into left child 2u covering [l, m] and right child 2u+1 covering [m+1, r]. "
                "Leaves covering [i, i] represent individual elements A[i]. Any subsegment query [ql, qr] decomposes into at most "
                "2 * ceil(log2 N) canonical disjoint nodes in O(log N) time."
            ),
            merge_algebra=(
                "Associative Merge Algebra: Node information is synthesized via parent = merge(leftChild, rightChild). "
                "The merge operator must be associative: merge(merge(a, b), c) = merge(a, merge(b, c)). "
                "Unlike standard Fenwick trees, Segment Trees do NOT require commutativity: associative non-commutative operations "
                "(such as matrix multiplication, string concatenation, affine transformations, and maximum subarray summaries) "
                "are strictly supported because tree traversals preserve canonical left-to-right interval order: merge(left, right)."
            ),
            identity_elements=(
                "Identity Elements: Each algebraic query operation possesses an identity element e such that merge(x, e) = merge(e, x) = x. "
                "For sum: identity = 0. "
                "For range minimum: identity = +INF. "
                "For range maximum: identity = -INF. "
                "For range GCD: identity = 0 (since gcd(x, 0) = x). "
                "For composite structures (e.g. maximum subarray), a sentinel flag (empty = true) represents the neutral element."
            ),
            lazy_tag_algebra=(
                "Lazy Tag Algebra & Deferred Propagation: "
                "Deferred operations affecting entire intervals are encapsulated in lazy tags with three primitives: "
                "1. apply(tag, node): Immediately updates node.value so that node.value always represents the true aggregate "
                "under all pending operations, even before pushing to descendants. "
                "2. compose(newTag, oldTag): For combined assignment and addition, tag state is (has_assign, assign_val, add_val). "
                "When newTag has_assign: child.has_assign = true, child.assign_val = newTag.assign_val, child.add_val = newTag.add_val "
                "(assignment completely overrides prior operations). "
                "When newTag is pure add: if child.has_assign: child.add_val += newTag.add_val; else: child.add_val += newTag.add_val. "
                "3. push(node): Transfers pending lazy tag to children 2u and 2u+1, then resets parent lazy tag to identity."
            ),
            non_empty_max_subarray=(
                "Non-Empty Maximum Contiguous Subarray Invariant: "
                "Each node maintains 4 quantities: total sum (sum), maximum prefix sum (pref), maximum suffix sum (suff), "
                "and maximum contiguous subarray sum (ans). "
                "Leaf node for element x: sum = pref = suff = ans = x. "
                "Merge rule: "
                "sum = L.sum + R.sum; "
                "pref = max(L.pref, L.sum + R.pref); "
                "suff = max(R.suff, R.sum + L.suff); "
                "ans = max({L.ans, R.ans, L.suff + R.pref}). "
                "The identity element is a sentinel node with empty = true such that merge(identity, X) = merge(X, identity) = X, "
                "correctly handling arrays containing all-negative numbers without false zero-length selections."
            ),
            frequency_order_statistic=(
                "Frequency Segment Tree & Order Statistics: "
                "Maintains frequency array F[1..M] where F[x] >= 0 stores occurrences of value x. "
                "Node u stores the sum of frequencies in value subrange [l, r]. "
                "Point updates add(val, +1) and add(val, -1) run in O(log M). "
                "K-th element selection: starting at root u=1 on [1, M], if k <= tree[2u].count, recurse to left child; "
                "otherwise recurse to right child with k' = k - tree[2u].count. Locates k-th element in strictly O(log M) time. "
                "Negative frequencies violate prefix monotonicity and are rejected via SEGMENT_TREE_KTH_NEGATIVE_FREQUENCY."
            ),
            interval_statistics=(
                "Interval Statistics (Min/Max with Frequency Counts): "
                "Each node stores (min_val, min_count, max_val, max_count). "
                "Merge combines extrema conditionally: if L.min_val < R.min_val, inherit L; if R.min_val < L.min_val, inherit R; "
                "if L.min_val == R.min_val, min_val = L.min_val and min_count = L.min_count + R.min_count. "
                "Max is merged symmetrically. Provides simultaneous extrema and multiplicity queries in O(log N) time."
            ),
            memory_representation=(
                "Memory Representation: "
                "A full binary tree over N leaves contains 2N - 1 conceptual nodes. "
                "Under standard 1-based recursive array layout where node u has children 2u and 2u+1, the maximum array index "
                "required is 2^(ceil(log2 N) + 1) - 1 < 4N. Thus, an allocation of 4N nodes is safe and standard. "
                "A common iterative layout stores 2N positions (for 1-indexed leaves / standard flat representation [N..2N-1])."
            ),
            integer_width_policy=(
                "Integer-Width Policy: "
                "Standard Segment Tree implementations default to signed 64-bit integers (`long long`). "
                "When intermediate products can exceed signed 64-bit limits—specifically in lazy propagation where "
                "(assign_val + add_val) * length is computed—promotion to `__int128` is enforced prior to multiplication: "
                "(__int128)(assign_val + add_val) * length. If output sums can exceed 2^63 - 1, a standard recursive "
                "print128 helper is provided."
            ),
            limitation_and_boundaries=(
                "Limitation & Boundary Reasoning: "
                "1. SEGMENT_TREE_STATIC_QUERY_SUBOPTIMAL: Static range queries with no updates prefer Prefix Sum (O(1) query) "
                "or Sparse Table (O(1) idempotent query) over Segment Tree (O(log N) query). "
                "2. SEGMENT_TREE_SIMPLE_PREFIX_OVERKILL: Point update with prefix-only queries on invertible monoids is simpler "
                "and faster on Fenwick Tree (lower constant factor, O(N) space). "
                "3. SEGMENT_TREE_DIFFERENCE_ARRAY_OVERKILL: Offline batch range additions without intermediate queries prefer "
                "Difference Array (O(1) update, single O(N) sweep). "
                "4. SEGMENT_TREE_FENWICK_EQUIVALENT: Point update + range sum on abelian groups is solvable by Fenwick Tree with lower constant. "
                "5. SEGMENT_TREE_NO_ASSOCIATIVE_MERGE: Operations lacking an associative binary summary across sub-intervals "
                "(e.g. dynamic median without rank tree, non-associative averaging) are structurally invalid for Segment Tree. "
                "6. SEGMENT_TREE_LAZY_TAG_UNSUPPORTED: Range updates whose tag composition cannot be maintained efficiently without "
                "Segment Tree Beats (e.g. range chmin/chmax) are unsupported in standard lazy trees. "
                "7. SEGMENT_TREE_RESOURCE_LIMIT: Exceeds memory budget based on 4 * N * sizeof(Node) > MemoryLimit."
            )
        )

    @staticmethod
    def merge_sum(left: int, right: int) -> int:
        return left + right

    @staticmethod
    def merge_min(left: int, right: int) -> int:
        return min(left, right)

    @staticmethod
    def merge_max(left: int, right: int) -> int:
        return max(left, right)

    @staticmethod
    def merge_gcd(left: int, right: int) -> int:
        import math
        return math.gcd(left, right)

    @staticmethod
    def merge_max_subarray(l_sum: int, l_pref: int, l_suff: int, l_ans: int,
                           r_sum: int, r_pref: int, r_suff: int, r_ans: int) -> Tuple[int, int, int, int]:
        res_sum = l_sum + r_sum
        res_pref = max(l_pref, l_sum + r_pref)
        res_suff = max(r_suff, r_sum + l_suff)
        res_ans = max(l_ans, r_ans, l_suff + r_pref)
        return (res_sum, res_pref, res_suff, res_ans)

    @staticmethod
    def compose_lazy_tags(new_has_assign: bool, new_assign_val: int, new_add_val: int,
                          old_has_assign: bool, old_assign_val: int, old_add_val: int) -> Tuple[bool, int, int]:
        """
        Composes a new incoming lazy tag over an existing old lazy tag.
        Returns (result_has_assign, result_assign_val, result_add_val).
        """
        if new_has_assign:
            return (True, new_assign_val, new_add_val)
        elif old_has_assign:
            return (True, old_assign_val, old_add_val + new_add_val)
        else:
            return (False, 0, old_add_val + new_add_val)

    @staticmethod
    def apply_lazy_tag_sum(length: int, has_assign: bool, assign_val: int, add_val: int, cur_sum: int) -> int:
        """Computes new interval sum after applying lazy tag."""
        if has_assign:
            return (assign_val + add_val) * length
        else:
            return cur_sum + add_val * length

    @staticmethod
    def apply_lazy_tag_minmax(has_assign: bool, assign_val: int, add_val: int, cur_val: int) -> int:
        """Computes new interval min/max after applying lazy tag."""
        if has_assign:
            return assign_val + add_val
        else:
            return cur_val + add_val

    @staticmethod
    def kth_frequency_search(tree_count: List[int], k: int, n: int) -> int:
        """
        Finds 1-based index in [1..n] of the k-th element using frequency Segment Tree.
        Requires tree_count[u] >= 0 and 1 <= k <= tree_count[1].
        Runs in O(log n) time.
        """
        u = 1
        l, r = 1, n
        while l < r:
            m = (l + r) // 2
            left_count = tree_count[2 * u]
            if k <= left_count:
                u = 2 * u
                r = m
            else:
                k -= left_count
                u = 2 * u + 1
                l = m + 1
        return l


# ── Dynamic Programming Structural Reasoning (Phase 3K) ──

@dataclass
class DPStructuralProof:
    pattern: str
    subproblem_definition: str
    minimal_state_representation: str
    overlapping_subproblems: str
    optimal_substructure_and_transitions: str
    base_cases_and_boundaries: str
    dependency_dag_and_evaluation_order: str
    answer_extraction: str
    memory_complexity_and_compression: str
    solution_reconstruction: str
    applicability_vs_alternatives: str
    competing_structures: str
    invalidation_invariants: str
    time_complexity_derivation: str
    space_complexity_derivation: str
    algebraic_objective_structure: str = "Tropical Semiring (min/max, +) for optimization; Counting Semiring (+, *) for ways; Feasibility Semiring (OR, AND) for reachability."
    state_augmentation_procedure: str = "Candidate state S is evaluated for Markov sufficiency: if insufficient, augment with finite discrete information S' = S x A; reject only if trajectory history is unbounded."


class DPStructuralReasoning:
    """
    Mathematical and structural foundation for Dynamic Programming (Phase 3K).
    Formally answers all 14 Core DP Reasoning Questions:
    1. Subproblem definition
    2. Minimal state representation & state augmentation
    3. Overlapping subproblems
    4. Optimal substructure / algebraic transition semiring
    5. Base cases & boundary conditions
    6. Dependency DAG & topological evaluation order
    7. Answer extraction
    8. Memory complexity & space compression
    9. Solution reconstruction (decision backtrack)
    10. Applicability constraints vs greedy / D&C
    11. Competing structures & greedy dominance
    12. Invalidation invariants & cyclic transition graph dispatch
    13. Time complexity derivation
    14. Space complexity derivation
    """

    @staticmethod
    def derive_algebraic_structure(objective: str) -> str:
        """
        Algebraic recurrence models characterize many DP objectives:
        - Optimization: Tropical Semiring (min/max, +) via Bellman's Principle of Optimality
        - Counting: Counting Semiring (+, *) via disjoint partition of subproblems
        - Feasibility: Boolean Semiring (OR, AND) via reachability satisfiability
        - Probability / Weighted-Paths: (R>=0, +, *) via Law of Total Probability over acyclic state graphs
        - Expected Value: Recurrences combining transition probabilities with stage rewards
        """
        obj = objective.lower()
        if any(w in obj for w in ["count", "number of", "ways", "total paths"]):
            return "Counting Semiring (+, *): Subproblem transitions partition the solution space into mutually disjoint sets; sum over all valid incoming branches."
        elif any(w in obj for w in ["feasible", "possible", "exists", "can reach", "boolean"]):
            return "Feasibility Semiring (OR, AND): Subproblems evaluate boolean reachability; OR across all valid incoming transitions."
        elif any(w in obj for w in ["probability", "chance", "weighted path"]):
            return "Probability / Weighted-Path Recurrence (R>=0, +, *): Transitions weighted by conditional probabilities; satisfies Law of Total Probability over DAG states."
        elif any(w in obj for w in ["expected", "expectation"]):
            return "Expected Value Recurrence: Combines state transition probabilities with accumulated stage rewards: E[u] = cost(u) + sum_{v} P(u->v) * E[v]."
        else:
            return "Tropical Semiring (min, +) or (max, +): Optimal substructure holds; subproblem optima compose into global optimum via Bellman's Principle of Optimality."

    @staticmethod
    def evaluate_state_augmentation(candidate_state: str, missing_info: str, is_unbounded: bool) -> Dict[str, Any]:
        if is_unbounded:
            return {
                "augmented": False,
                "rejection_code": "DP_NON_MARKOVIAN_FUTURE_DEPENDENCE",
                "reason": "Missing historical trajectory is unbounded (size Omega(N)); finite state augmentation is impossible."
            }
        return {
            "augmented": True,
            "augmented_state": f"({candidate_state}, {missing_info})",
            "state_dimension_increase": 1,
            "status": "Markov sufficiency restored via finite state augmentation."
        }

    @staticmethod
    def evaluate_reconstruction_under_space_compression(
        is_space_compressed: bool,
        requires_reconstruction: bool,
        memory_limit_bytes: int = 64 * 1024 * 1024,
        n: int = 1000,
        m: int = 1000
    ) -> Dict[str, Any]:
        """
        Space Compression vs. Reconstruction Compatibility Rule:
        If space compression is applied, the complete 2D/multi-D state history is overwritten.
        Reconstruction requires one of four explicit strategies:
        1. Full-table retention (revert compression if memory feasible)
        2. Compact choice/parent array (e.g. 1 bit per cell)
        3. Recomputation during traceback
        4. Hirschberg-style divide and conquer
        """
        if not requires_reconstruction:
            return {
                "strategy": "compressed_1d_only",
                "valid": True,
                "notes": "No reconstruction required; single-layer rolling array is optimal."
            }

        full_table_bytes = n * m * 8
        if full_table_bytes <= memory_limit_bytes:
            return {
                "strategy": "full_table_retention",
                "valid": True,
                "notes": f"Full {n}x{m} table ({full_table_bytes} bytes) fits in memory limit; retain full table for O(1) backtrack."
            }
        else:
            return {
                "strategy": "hirschberg_or_choice_bits",
                "valid": True,
                "notes": f"Full table exceeds memory limit; use Hirschberg D&C (O(min(N,M)) space) or compact choice bit-array."
            }

    @staticmethod
    def explain(pattern: str = "dp_1d_linear") -> DPStructuralProof:
        pat = pattern.lower()

        if "knapsack" in pat:
            return DPStructuralProof(
                pattern=pattern,
                subproblem_definition="dp[i][w]: Maximum value achievable using a subset of the first i items subject to exact or bounded capacity w.",
                minimal_state_representation="Tuple (i, w) where i in [0..N] represents item prefix index and w in [0..W] represents available weight capacity. This state is necessary and sufficient because item choices are irreversible and capacity consumption is additive.",
                overlapping_subproblems="Different combinations of earlier items can yield identical remaining capacity w, resulting in repeated evaluation of identical subproblems (i, w).",
                optimal_substructure_and_transitions="dp[i][w] = max(dp[i-1][w], dp[i-1][w - weight[i]] + value[i]) for 0/1 knapsack, or dp[i][w] = max(dp[i-1][w], dp[i][w - weight[i]] + value[i]) for unbounded knapsack.",
                base_cases_and_boundaries="dp[0][w] = 0 for all w in [0..W]; dp[i][0] = 0 for all i in [0..N]. For exact weight matching, non-zero entries initialize to -INF.",
                dependency_dag_and_evaluation_order="State (i, w) depends strictly on row i-1 with capacity <= w. Topological evaluation order: outer loop i from 1 to N, inner loop w from 0 to W.",
                answer_extraction="The global maximum is located at max_{w=0..W} dp[N][w] (or dp[N][W] for monotonic weight values).",
                memory_complexity_and_compression="2D table requires O(N * W) space. Compressed to 1D array dp[w] by iterating w backward from W down to weight[i] for 0/1 knapsack (preventing item reuse), or forward from weight[i] to W for unbounded knapsack.",
                solution_reconstruction="Backtrack from (N, W): if dp[i][w] == dp[i-1][w - weight[i]] + value[i], item i was included; decrement w by weight[i] and continue with i-1.",
                applicability_vs_alternatives="Greedy by value/weight ratio fails for 0/1 knapsack due to indivisibility of items (greedy choice property violated). DP is required.",
                competing_structures="Fractional Knapsack (Greedy O(N log N)), Branch & Bound / Meet-in-the-Middle for small N <= 40 with huge W.",
                invalidation_invariants="Negative item weights with unbounded repetition create infinite cycles. Fractional item splitting makes greedy strictly optimal and DP suboptimal.",
                time_complexity_derivation="O(N * W) total time: N outer iterations * W inner transitions, each computing O(1) state lookup.",
                space_complexity_derivation="O(N * W) uncompressed 2D space, reduced to O(W) using 1D rolling array compression."
            )
        elif "grid" in pat or "2d" in pat:
            return DPStructuralProof(
                pattern=pattern,
                subproblem_definition="dp[r][c]: Optimal cost or total paths from starting cell (0, 0) to cell (r, c) moving only right and down.",
                minimal_state_representation="Tuple (r, c) representing current grid coordinates. Coordinates uniquely define the subproblem because transitions only depend on the current cell.",
                overlapping_subproblems="Cell (r, c) can be reached from (r-1, c) and (r, c-1), which share common ancestor paths, causing overlapping subproblems in naive recursion.",
                optimal_substructure_and_transitions="dp[r][c] = min(dp[r-1][c], dp[r][c-1]) + grid[r][c] (for min path sum) or dp[r][c] = dp[r-1][c] + dp[r][c-1] (for unique paths).",
                base_cases_and_boundaries="dp[0][0] = grid[0][0]; first row dp[0][c] = dp[0][c-1] + grid[0][c]; first column dp[r][0] = dp[r-1][0] + grid[r][c]. Obstacles set dp[r][c] = 0 or +INF.",
                dependency_dag_and_evaluation_order="Cell (r, c) depends on (r-1, c) and (r, c-1). Topological order is row-major (r from 0 to R-1, c from 0 to C-1) or anti-diagonal.",
                answer_extraction="Target is located at destination cell dp[R-1][C-1].",
                memory_complexity_and_compression="Uncompressed requires O(R * C) memory. Compressible to O(C) by maintaining a single rolling row: dp[c] = min(dp[c], dp[c-1]) + grid[r][c].",
                solution_reconstruction="Backtrack from (R-1, C-1): step to whichever of (r-1, c) or (r, c-1) yielded the optimal transition value.",
                applicability_vs_alternatives="BFS/Dijkstra is applicable for general graphs; however, grid DAG topological ordering enables O(R * C) DP without priority queue overhead.",
                competing_structures="Dijkstra's Algorithm (when arbitrary 4-directional moves with non-negative weights are permitted), A* search.",
                invalidation_invariants="Allowing arbitrary 4-directional moves creates cycles, invalidating the DAG topological ordering and requiring Dijkstra instead.",
                time_complexity_derivation="O(R * C) states * O(1) transitions per state = O(R * C) time.",
                space_complexity_derivation="O(R * C) full table, compressed to O(min(R, C)) using a rolling row or column."
            )
        elif "subsequence" in pat or "string" in pat:
            return DPStructuralProof(
                pattern=pattern,
                subproblem_definition="dp[i][j]: Optimal score (e.g. LCS length, Edit Distance) comparing prefix s1[0..i-1] with prefix s2[0..j-1].",
                minimal_state_representation="Tuple (i, j) where i in [0..|s1|] and j in [0..|s2|]. Prefix lengths encapsulate all relevant history for suffix alignment.",
                overlapping_subproblems="Matching s1[i] and s2[j] vs skipping either character creates branching paths that converge to identical subproblems (i-1, j-1).",
                optimal_substructure_and_transitions="For LCS: if s1[i-1] == s2[j-1]: dp[i][j] = dp[i-1][j-1] + 1; else: dp[i][j] = max(dp[i-1][j], dp[i][j-1]). For Edit Distance: min of insert, delete, replace operations.",
                base_cases_and_boundaries="dp[0][j] and dp[i][0] initialized according to operation: for LCS, 0; for Edit Distance, j and i respectively.",
                dependency_dag_and_evaluation_order="Cell (i, j) depends on (i-1, j), (i, j-1), and (i-1, j-1). Evaluated row-by-row (i from 0 to |s1|, j from 0 to |s2|).",
                answer_extraction="Final answer is at dp[|s1|][|s2|].",
                memory_complexity_and_compression="O(|s1| * |s2|) full matrix, reducible to O(min(|s1|, |s2|)) using two rolling rows if only distance/length is required.",
                solution_reconstruction="Backtrack from (|s1|, |s2|): match characters when s1[i-1] == s2[j-1], else trace back to max(dp[i-1][j], dp[i][j-1]).",
                applicability_vs_alternatives="Greedy matching fails because local character choice can preclude globally longer common subsequences. DP is required.",
                competing_structures="Hirschberg's Algorithm (O(N) space with reconstruction), Myers Diff algorithm.",
                invalidation_invariants="Non-prefix dependencies or global count constraints spanning across arbitrary non-local indices.",
                time_complexity_derivation="O(|s1| * |s2|) states * O(1) transitions = O(|s1| * |s2|) time.",
                space_complexity_derivation="O(|s1| * |s2|) table space, or O(min(|s1|, |s2|)) with rolling array."
            )
        elif "interval" in pat:
            return DPStructuralProof(
                pattern=pattern,
                subproblem_definition="dp[i][j]: Optimal cost of merging or evaluating subsegment [i..j] (e.g. Matrix Chain Multiplication, Burst Balloons).",
                minimal_state_representation="Tuple (i, j) where 0 <= i <= j < N. Represents contiguous subsegment boundaries.",
                overlapping_subproblems="Subsegments [i..j] are evaluated as subproblems of many larger intervals [i..k] and [k..j].",
                optimal_substructure_and_transitions="dp[i][j] = min_{k=i..j-1} (dp[i][k] + dp[k+1][j] + cost(i, k, j)).",
                base_cases_and_boundaries="dp[i][i] = 0 for all i (single element interval has zero merge cost). Length 2 base cases computed directly.",
                dependency_dag_and_evaluation_order="Intervals of length len depend on sub-intervals of strictly smaller length < len. Topological order: outer loop len from 2 to N, inner loop i from 0 to N-len, j = i + len - 1.",
                answer_extraction="Located at dp[0][N-1] (the entire interval).",
                memory_complexity_and_compression="O(N^2) memory. State space generally cannot be compressed linearly because all subsegment lengths are simultaneously required.",
                solution_reconstruction="Store split point opt_k[i][j] = k that achieved the minimum; recursively reconstruct tree structure.",
                applicability_vs_alternatives="Greedy merging (e.g. Huffman) is only optimal when merge costs do not depend on adjacent spatial order. Spatially constrained merges require Interval DP.",
                competing_structures="Knuth's Optimization (reduces O(N^3) to O(N^2) when opt[i][j-1] <= opt[i][j] <= opt[i+1][j]), Hu-Tucker algorithm.",
                invalidation_invariants="Non-contiguous merging or arbitrary reordering of elements violates the interval subproblem definition.",
                time_complexity_derivation="O(N^2) states * O(N) split choices per state = O(N^3) time (or O(N^2) with Knuth's optimization).",
                space_complexity_derivation="O(N^2) state space table."
            )
        elif "bitmask" in pat:
            return DPStructuralProof(
                pattern=pattern,
                subproblem_definition="dp[mask][u]: Optimal cost of visiting subset of vertices represented by bitmask 'mask', ending at vertex u.",
                minimal_state_representation="Tuple (mask, u) where mask in [0..2^N - 1] and u in [0..N-1]. 'mask' captures the set of visited elements, satisfying the Markov property.",
                overlapping_subproblems="Different permutation orderings of the same subset of vertices reach the same endpoint u with identical remaining unvisited vertices.",
                optimal_substructure_and_transitions="dp[mask][u] = min_{v in mask, v != u} (dp[mask ^ (1 << u)][v] + dist[v][u]).",
                base_cases_and_boundaries="dp[1 << start][start] = 0; all other dp[mask][u] initialized to +INF.",
                dependency_dag_and_evaluation_order="States with mask size k depend strictly on states with mask size k-1. Numerical order mask from 1 to 2^N - 1 is a valid topological ordering.",
                answer_extraction="TSP: min_{u=0..N-1} (dp[(1 << N) - 1][u] + dist[u][start]).",
                memory_complexity_and_compression="O(2^N * N) memory table.",
                solution_reconstruction="Backtrack from final mask: identify predecessor vertex v that minimized the transition.",
                applicability_vs_alternatives="Brute force permutation check takes O(N!). Bitmask DP reduces complexity to O(2^N * N^2), making N <= 20 feasible.",
                competing_structures="Branch and Bound, Held-Karp, Meet-in-the-Middle (for Hamiltonian path / subset sum).",
                invalidation_invariants="N > 25 causes 2^N * N memory explosion (DP_STATE_SPACE_EXPLOSION / DP_RESOURCE_LIMIT).",
                time_complexity_derivation="O(2^N * N) states * O(N) transitions = O(2^N * N^2) time.",
                space_complexity_derivation="O(2^N * N) state table space."
            )
        elif "tree" in pat:
            return DPStructuralProof(
                pattern=pattern,
                subproblem_definition="dp[u][state]: Optimal metric in subtree rooted at u, where 'state' encodes local decisions at u (e.g. u included vs excluded in independent set).",
                minimal_state_representation="Tuple (u, state) where u in [1..V] and state in {0, 1}. Subtree independence guarantees minimal Markov state.",
                overlapping_subproblems="Subtree computations are shared across multiple recursive parent inquiries in rerooting or tree decomposition.",
                optimal_substructure_and_transitions="dp[u][0] = sum_{v in children(u)} max(dp[v][0], dp[v][1]); dp[u][1] = weight[u] + sum_{v in children(u)} dp[v][0].",
                base_cases_and_boundaries="Leaves: dp[leaf][0] = 0, dp[leaf][1] = weight[leaf].",
                dependency_dag_and_evaluation_order="Node u depends strictly on its subtree descendants. Topological order is post-order DFS (bottom-up from leaves to root).",
                answer_extraction="Root result: max(dp[root][0], dp[root][1]).",
                memory_complexity_and_compression="O(V * states) = O(V) space table.",
                solution_reconstruction="Backtrack from root down to leaves based on which state (0 or 1) was chosen at each node.",
                applicability_vs_alternatives="Acyclic tree structure allows optimal bottom-up DP in O(V) time without cycle detection.",
                competing_structures="Tree Heavy-Light Decomposition, DSU on Tree (Sack), Centroid Decomposition.",
                invalidation_invariants="Cycles in graph invalidate tree structure and bottom-up DFS topological ordering.",
                time_complexity_derivation="O(V) states * O(deg(u)) child transitions summed over all nodes = O(V) time.",
                space_complexity_derivation="O(V) space for DP table and recursion stack."
            )
        elif "dag" in pat:
            return DPStructuralProof(
                pattern=pattern,
                subproblem_definition="dp[u]: Longest path or optimal path metric from vertex u to any sink in a Directed Acyclic Graph (DAG).",
                minimal_state_representation="Single vertex u. Because the graph is acyclic, no visited set is needed.",
                overlapping_subproblems="Multiple paths reach vertex u; the optimal path from u forward is computed once and reused.",
                optimal_substructure_and_transitions="dp[u] = max_{(u, v) in E} (dp[v] + weight(u, v)).",
                base_cases_and_boundaries="Sinks (out-degree 0): dp[sink] = 0.",
                dependency_dag_and_evaluation_order="Reverse topological sort order (or memoized DFS with cycle check).",
                answer_extraction="Global max: max_{u in V} dp[u].",
                memory_complexity_and_compression="O(V) space array.",
                solution_reconstruction="Follow edge (u, v) that achieved max(dp[v] + weight(u, v)).",
                applicability_vs_alternatives="General graphs with cycles require Bellman-Ford or Dijkstra; DAG structure allows linear O(V + E) DP.",
                competing_structures="Topological Sort + Relaxation, Kahn's algorithm.",
                invalidation_invariants="Presence of cycles violates DAG property and causes infinite recursion (DP_CYCLIC_STATE_DEPENDENCY).",
                time_complexity_derivation="O(V + E) time: every vertex and edge examined once in topological order.",
                space_complexity_derivation="O(V) table space."
            )
        else:
            # Default to 1D Linear DP
            return DPStructuralProof(
                pattern=pattern,
                subproblem_definition="dp[i]: Optimal metric for prefix A[0..i] or optimal sequence ending at index i (e.g. LIS, Kadane maximum subarray).",
                minimal_state_representation="Index i in [0..N-1]. Minimal and sufficient because future extensions only depend on prefix boundary i.",
                overlapping_subproblems="Candidate predecessor choices j < i overlap across different evaluation points i.",
                optimal_substructure_and_transitions="For LIS: dp[i] = 1 + max_{j < i, A[j] < A[i]} dp[j]. For Kadane: dp[i] = max(A[i], dp[i-1] + A[i]).",
                base_cases_and_boundaries="dp[0] = 1 (LIS) or dp[0] = A[0] (Kadane).",
                dependency_dag_and_evaluation_order="Index i depends strictly on indices j < i. Linear forward order i from 0 to N-1.",
                answer_extraction="Global maximum: max_{i=0..N-1} dp[i].",
                memory_complexity_and_compression="O(N) table, compressed to O(1) for Kadane where dp[i] only depends on dp[i-1].",
                solution_reconstruction="Maintain predecessor array parent[i] = j; trace backwards from argmax.",
                applicability_vs_alternatives="Greedy prefix choices fail on non-monotonic or mixed arrays. DP captures all legal prefix extensions.",
                competing_structures="Binary Search + Patience Sorting (O(N log N) for LIS), Divide & Conquer.",
                invalidation_invariants="Non-local dependencies where transition at i depends on unconstrained future elements.",
                time_complexity_derivation="O(N^2) for standard LIS (or O(N log N) with binary search), O(N) for Kadane.",
                space_complexity_derivation="O(N) uncompressed, or O(1) compressed."
            )


# ── Phase 3L: Greedy Algorithms Reasoning ──

@dataclass
class GreedyDerivation:
    pattern: str
    problem_objective: str
    feasibility_constraints: str
    candidate_local_choice: str
    ordering_priority_rule: str
    safe_choice_hypothesis: str
    proof_method: str  # Exchange Argument, Staying Ahead, Dominance, Cut Property, Matroid Independence
    proof_derivation: str
    feasibility_preservation: str
    greedy_invariant: str
    termination_condition: str
    global_correctness_argument: str
    time_complexity_derivation: str
    space_complexity_derivation: str
    competing_families: str
    why_competing_not_selected: str


class GreedyStructuralReasoning:
    """
    Mathematical and structural foundation for Greedy Algorithms (Phase 3L).
    Formally answers all 16 Core Greedy Reasoning Dimensions:
    1. Pattern identifier
    2. Problem objective
    3. Feasibility constraints
    4. Candidate local choice
    5. Ordering / priority rule (with explicit comparator direction)
    6. Safe-choice hypothesis
    7. Proof method (Exchange Argument, Staying Ahead, Dominance, Cut Property, Matroid Independence)
    8. Mathematical proof derivation
    9. Feasibility preservation
    10. Greedy invariant (family-specific lifecycle state)
    11. Termination condition (complete construction & proof guarantee)
    12. Global correctness argument
    13. Time complexity derivation
    14. Space complexity derivation
    15. Competing algorithm families
    16. Why competing methods are not selected (neutral candidate discrimination)
    """

    @staticmethod
    def derive_greedy_proof(pattern: str, params: Optional[Dict[str, Any]] = None) -> GreedyDerivation:
        if params is None:
            params = {}
        pat = pattern.lower()

        if "interval_selection" in pat:
            return GreedyDerivation(
                pattern=pattern,
                problem_objective="Maximize the cardinality of a mutually non-overlapping subset of intervals.",
                feasibility_constraints="No two selected intervals (s_i, f_i) and (s_j, f_j) may overlap (s_j >= f_i for s_i <= s_j).",
                candidate_local_choice="Select the compatible interval that finishes earliest (smallest finish time f_i).",
                ordering_priority_rule="Sort ascending by interval finish time f_i. Ties broken arbitrarily.",
                safe_choice_hypothesis="Selecting the earliest finishing compatible interval leaves the maximum possible remaining time for subsequent intervals.",
                proof_method="Exchange Argument",
                proof_derivation=(
                    "Let O = {o_1, o_2, ..., o_k} be an optimal schedule ordered by finish time. "
                    "Let g_1 be the interval with earliest finish time in the entire set. "
                    "By definition, f(g_1) <= f(o_1). "
                    "Construct O' = (O \\ {o_1}) U {g_1}. "
                    "Since f(g_1) <= f(o_1) and o_1 did not overlap o_2, g_1 cannot overlap o_2 (s(o_2) >= f(o_1) >= f(g_1)). "
                    "Thus O' is a feasible schedule with |O'| = |O|, containing the greedy choice g_1. "
                    "By induction on k, there exists an optimal solution containing the entire greedy sequence."
                ),
                feasibility_preservation="Each chosen interval finishes no later than any alternative, guaranteeing the feasible start-time threshold for future choices is minimized.",
                greedy_invariant="After selecting k intervals, the greedy schedule has earliest finish time among all feasible schedules of cardinality k.",
                termination_condition="All candidate intervals evaluated; no remaining interval has start time >= current finish boundary. The construction is complete and the associated correctness proof establishes global optimality.",
                global_correctness_argument="Because the greedy choice stays ahead in remaining time capacity, it achieves maximum cardinality.",
                time_complexity_derivation="O(N log N) for sorting intervals by finish time + O(N) linear scan = O(N log N) total.",
                space_complexity_derivation="O(1) auxiliary space beyond storage of intervals.",
                competing_families="Dynamic Programming (Weighted Interval Scheduling), Interval Partitioning.",
                why_competing_not_selected="GREEDY_PROVEN_SUFFICIENT: DP table is unnecessary because unweighted intervals satisfy the greedy exchange property, guaranteeing global optimality in O(N log N) without state memoization."
            )

        elif "interval_covering" in pat:
            return GreedyDerivation(
                pattern=pattern,
                problem_objective="Minimize the number of points needed to stab/cover all given intervals.",
                feasibility_constraints="Every interval [start_i, end_i] must contain at least one chosen point.",
                candidate_local_choice="Place a point at the rightmost endpoint of the interval that ends earliest among uncovered intervals.",
                ordering_priority_rule="Sort ascending by interval end time end_i.",
                safe_choice_hypothesis="Placing the point at the rightmost possible coordinate of the earliest-ending interval maximizes its coverage of future overlapping intervals.",
                proof_method="Staying Ahead",
                proof_derivation=(
                    "Consider the interval I_1 with minimal end point e_1. To cover I_1, any valid point p must satisfy start_1 <= p <= e_1. "
                    "For any other interval I_j = [start_j, end_j] that overlaps with p, since start_j <= p <= e_1, placing the point at exactly e_1 "
                    "will cover I_j as long as start_j <= e_1 <= end_j. "
                    "Any point p < e_1 covers a subset of the intervals covered by e_1 because shifting p rightward to e_1 can only include intervals starting in (p, e_1], while never losing any interval ending >= e_1. "
                    "Thus p = e_1 provably dominates all other placements."
                ),
                feasibility_preservation="Every uncovered interval with start <= current_point is covered; only intervals starting strictly after current_point require new points.",
                greedy_invariant="All intervals ending <= current_point are covered, and current_point is at the maximal coordinate covering the current prefix.",
                termination_condition="All intervals have been scanned and covered. The construction is complete and the associated correctness proof establishes minimum stabbing cardinality.",
                global_correctness_argument="Since each point placement is maximal and necessary, the total number of points is minimal.",
                time_complexity_derivation="O(N log N) sorting by end coordinate + O(N) single-pass scan = O(N log N).",
                space_complexity_derivation="O(1) auxiliary space.",
                competing_families="General Set Cover (NP-hard), Dynamic Programming.",
                why_competing_not_selected="GREEDY_PROVEN_SUFFICIENT: While general Set Cover is NP-hard, 1D interval stabbing exhibits total order geometry where rightmost endpoint placement is provably optimal."
            )

        elif "fractional_knapsack" in pat:
            return GreedyDerivation(
                pattern=pattern,
                problem_objective="Maximize total value within capacity W where items can be taken fractionally.",
                feasibility_constraints="Total selected weight sum(w_i * x_i) <= W with fraction 0 <= x_i <= 1 for all i.",
                candidate_local_choice="Select as much as possible of the item with the highest value-to-weight ratio (density v_i / w_i).",
                ordering_priority_rule="Sort descending by value density r_i = v_i / w_i (decreasing r_i).",
                safe_choice_hypothesis="Every unit of knapsack capacity allocated to a higher-density item yields strictly greater value than any lower-density item.",
                proof_method="Exchange Argument",
                proof_derivation=(
                    "Let G be the greedy fractional allocation and O be an optimal allocation. "
                    "If G != O, let k be the first item where x_k(G) != x_k(O). "
                    "Since G takes maximum available capacity of highest density items, x_k(G) > x_k(O). "
                    "Because O is feasible, there must exist some item j with lower density r_j < r_k such that x_j(O) > 0. "
                    "Transfer an amount of weight delta = min(w_k * (x_k(G) - x_k(O)), w_j * x_j(O)) from j to k in O. "
                    "The change in total value is delta * (r_k - r_j) > 0, which implies O was not optimal unless r_k == r_j. "
                    "Thus G achieves the maximum possible value."
                ),
                feasibility_preservation="Divisibility guarantees capacity W can be filled to exact fullness without leaving unusable gaps.",
                greedy_invariant="At each step, remaining capacity is filled with the globally available highest-density value.",
                termination_condition="Remaining capacity becomes 0 or all items are fully exhausted. The construction is complete and the associated correctness proof establishes global optimality.",
                global_correctness_argument="No alternative allocation can achieve higher average density over capacity W.",
                time_complexity_derivation="O(N log N) sorting by density + O(N) linear fill = O(N log N).",
                space_complexity_derivation="O(1) auxiliary space beyond items.",
                competing_families="0/1 Knapsack (Dynamic Programming O(N*W)).",
                why_competing_not_selected="DIVISIBILITY_ELIMINATES_KNAPSACK_BRANCHING: Fractional divisibility removes discrete packing boundaries; density sorting is provably optimal without DP state expansion."
            )

        elif "deadline_scheduling" in pat:
            return GreedyDerivation(
                pattern=pattern,
                problem_objective="Minimize maximum lateness L_max = max_i (C_i - d_i) or weighted completion time 1 || sum w_i C_i.",
                feasibility_constraints="Single processor; jobs processed without preemption.",
                candidate_local_choice=(
                    "Process job with earliest deadline d_i (for lateness) or highest weight-to-processing ratio w_i / p_i "
                    "(Smith's rule for weighted completion time: sort by decreasing w_i / p_i, equivalently increasing p_i / w_i)."
                ),
                ordering_priority_rule="Sort ascending by deadline d_i (Earliest Due Date) OR sort descending by ratio w_i / p_i (Smith's Rule).",
                safe_choice_hypothesis="An inverted pair of adjacent jobs can be swapped without increasing maximum lateness (or strictly decreasing weighted completion time).",
                proof_method="Exchange Argument",
                proof_derivation=(
                    "For Maximum Lateness (EDD): Let S be a schedule with an inversion, i.e., adjacent jobs i and j where d_i > d_j but i is scheduled immediately before j. "
                    "Swap i and j. In the new schedule S', job j completes earlier, so its lateness decreases. "
                    "Job i completes at the time j previously completed (C'_i = C_j). "
                    "Since d_i > d_j, L'_i = C'_i - d_i = C_j - d_i < C_j - d_j = L_j. "
                    "Thus the new maximum lateness max(L'_i, L'_j) <= max(L_i, L_j). "
                    "Repeating adjacent swaps eliminates all inversions without increasing L_max. "
                    "For Weighted Completion Time (Smith's Rule): Swapping adjacent jobs i, j with w_i/p_i < w_j/p_j reduces total cost by w_j * p_i - w_i * p_j > 0. "
                    "Thus sorting by decreasing w_i / p_i is optimal."
                ),
                feasibility_preservation="Job durations are additive; swapping adjacent jobs leaves all other job completion times unchanged.",
                greedy_invariant="Prefix of scheduled jobs contains zero inversions and preserves minimal lateness / completion penalty.",
                termination_condition="All jobs scheduled in non-decreasing deadline or non-increasing Smith's ratio order. The construction is complete and the associated correctness proof establishes optimality.",
                global_correctness_argument="Any schedule can be transformed into the greedy schedule via adjacent swaps without deteriorating the objective.",
                time_complexity_derivation="O(N log N) sorting + O(N) schedule simulation = O(N log N).",
                space_complexity_derivation="O(1) auxiliary space beyond job list.",
                competing_families="Dynamic Programming (Weighted Interval Scheduling), Bipartite Matching.",
                why_competing_not_selected="GREEDY_PROVEN_SUFFICIENT: Single-machine lateness and linear weighted completion time satisfy adjacent pairwise exchange transitivity, rendering exponential/DP search unnecessary."
            )

        elif "heap_assisted" in pat:
            return GreedyDerivation(
                pattern=pattern,
                problem_objective="Minimize resource activations / refueling stops to reach destination.",
                feasibility_constraints="Resource capacity cannot drop below zero at any point.",
                candidate_local_choice="When resource is exhausted, retrospectively activate the largest available resource from the pool of passed candidates.",
                ordering_priority_rule="Advance spatially; maintain passed available resources in a max-heap.",
                safe_choice_hypothesis="Delaying the commitment of which resource to use until required, then picking the maximum capacity resource, maximizes remaining runway.",
                proof_method="Staying Ahead",
                proof_derivation=(
                    "Let k stops be taken. To maximize the distance reachable with k stops, the k stops chosen must be the k largest fuel capacities among all stations passed. "
                    "By maintaining passed stations in a max-heap and extracting the maximum whenever current fuel < 0, the greedy algorithm always activates the largest fuel reserve available in the feasible history, staying ahead of any other choice of k stops."
                ),
                feasibility_preservation="The heap only contains stations physically reached; extracting preserves spatial causality.",
                greedy_invariant="At each step, the set of activated stations is of minimum size, and the remaining resource buffer is maximized.",
                termination_condition="Destination reached or heap empty while current resource < 0 (unreachable). The construction is complete and the associated correctness proof establishes minimum stops.",
                global_correctness_argument="Because each added stop provides the maximum possible extension, the minimum number of stops is achieved.",
                time_complexity_derivation="O(N log N) for heap insertions and extractions.",
                space_complexity_derivation="O(N) for priority queue.",
                competing_families="State-Augmented DP (dp[i][fuel] in O(N * Capacity)).",
                why_competing_not_selected="DP_HAS_NO_ADDITIONAL_REQUIRED_STATE: State-augmented DP tracks fuel levels explicitly in O(N * Capacity) memory/time; heap-assisted greedy reduces state tracking to a priority queue in O(N log N)."
            )

        elif "huffman_merge" in pat:
            return GreedyDerivation(
                pattern=pattern,
                problem_objective="Minimize weighted path length sum(f_i * depth_i) in an optimal binary merge tree.",
                feasibility_constraints="Full binary tree where each original element is a leaf.",
                candidate_local_choice="Repeatedly merge the two components with the smallest current weights.",
                ordering_priority_rule="Min-heap priority queue ordered by component weight.",
                safe_choice_hypothesis="The two least frequent items must appear as siblings at the maximum depth of an optimal tree.",
                proof_method="Exchange Argument",
                proof_derivation=(
                    "Let x and y be the two elements with lowest frequencies. "
                    "In an optimal merge tree T, let a and b be two sibling leaves at maximum depth. "
                    "Without loss of generality, f(x) <= f(a) and f(y) <= f(b). "
                    "Swapping x with a and y with b changes total cost by: "
                    "delta = (f(x) - f(a)) * (depth(a) - depth(x)) + (f(y) - f(b)) * (depth(b) - depth(y)). "
                    "Since depth(a), depth(b) are maximal, the depth differences are non-negative, and the frequency differences are non-positive. "
                    "Thus delta <= 0, so T' is also optimal. "
                    "Replacing x and y with a combined node of weight f(x) + f(y) reduces the problem to N-1 elements by induction."
                ),
                feasibility_preservation="Tree structure is preserved; each merge reduces component count by 1.",
                greedy_invariant="Forest of trees where each tree root represents an optimal subtree for its leaf frequencies.",
                termination_condition="Single merged root component remains in heap. The construction is complete and the associated correctness proof establishes minimum weighted external path length.",
                global_correctness_argument="By induction, Huffman's greedy bottom-up merge achieves minimum weighted tree length.",
                time_complexity_derivation="O(N log N) using a min-heap (N-1 merges, each O(log N)).",
                space_complexity_derivation="O(N) for heap and tree nodes.",
                competing_families="Matrix Chain / Interval DP (dp[i][j] in O(N^3)).",
                why_competing_not_selected="GREEDY_PROVEN_SUFFICIENT: Interval DP is required only when sequence ordering is fixed; for Huffman coding, merge order is unconstrained, enabling O(N log N) greedy merge."
            )

        elif "sequence_local_choice" in pat:
            return GreedyDerivation(
                pattern=pattern,
                problem_objective="Construct lexicographically smallest sequence / number after removing k elements.",
                feasibility_constraints="Relative order of retained elements must be preserved.",
                candidate_local_choice="Whenever current element is strictly smaller than the previous element and removals remain, drop the previous element.",
                ordering_priority_rule="Left-to-right scan; maintain monotonic increasing prefix via stack.",
                safe_choice_hypothesis="An earlier position in a number has greater significance than all later positions combined; minimizing the first differing digit minimizes the number.",
                proof_method="Dominance",
                proof_derivation=(
                    "For two numbers of equal length, the first differing digit from left to right determines which is smaller. "
                    "If d_i > d_{i+1}, removing d_i replaces d_i with d_{i+1} at index i. "
                    "Since d_{i+1} < d_i, this strictly decreases the number at the highest available place value. "
                    "Delaying this removal to a less significant digit can never compensate for having a larger digit at index i. "
                    "Thus removing d_i is a permanently dominant choice."
                ),
                feasibility_preservation="Removals are decremented; remaining removals at the end are trimmed from the right.",
                greedy_invariant="Stack maintains the lexicographically minimal prefix for scanned elements and available removals.",
                termination_condition="All digits processed and excess removals discarded. The construction is complete and the associated correctness proof establishes lexicographical minimality.",
                global_correctness_argument="Dominance of higher place values guarantees the global lexicographical minimum.",
                time_complexity_derivation="O(N) linear time: each element pushed and popped at most once using monotonic stack (reusing Phase 3B).",
                space_complexity_derivation="O(N) for stack storage.",
                competing_families="Dynamic Programming (Longest Increasing Subsequence, Edit Distance).",
                why_competing_not_selected="GREEDY_PROVEN_SUFFICIENT: Irreversible local choice via monotonic stack achieves optimal O(N) time, eliminating the need for O(N * K) DP state formulation."
            )

        elif "reachability_partition" in pat:
            is_gas_station = bool("gas" in pat or "gas_station" in params.get("subtype", "") or "gas" in params.get("text", "").lower())
            if is_gas_station:
                return GreedyDerivation(
                    pattern=pattern,
                    problem_objective="Find unique starting gas station to complete circular tour without running out of fuel.",
                    feasibility_constraints="Tank balance cannot drop below zero at any point along the circular tour.",
                    candidate_local_choice="Advance along circuit; when cumulative tank balance drops below zero at station i, eliminate all candidate starts in [start..i] and reset start = i + 1.",
                    ordering_priority_rule="Linear scan tracking cumulative tank balance and total surplus sum(gas - cost).",
                    safe_choice_hypothesis="If station i is unreachable from start, no intermediate station j between start and i can reach i.",
                    proof_method="Prefix Cumulative Surplus / Elimination Proof",
                    proof_derivation=(
                        "Suppose tank drops below 0 when moving from i to i+1, having started at 'start'. "
                        "For any intermediate station j with start < j <= i, the fuel upon reaching j starting from 'start' was >= 0. "
                        "Thus, starting at j with fuel 0 will result in strictly less fuel at station i than starting from 'start'. "
                        "Therefore, no station in [start..i] can be a valid starting point. "
                        "We can safely advance the candidate start to i + 1, eliminating the entire prefix in O(1) checks."
                    ),
                    feasibility_preservation="Cumulative surplus guarantees global feasibility iff total_surplus >= 0.",
                    greedy_invariant="Candidate start is the only possible valid start in prefix [0..i]; current tank balance >= 0.",
                    termination_condition="Single pass completed; if total_surplus >= 0 return start, else return -1. The construction is complete and the associated correctness proof establishes feasibility.",
                    global_correctness_argument="Prefix elimination guarantees that if a solution exists, the identified start is feasible.",
                    time_complexity_derivation="O(N) single-pass linear scan.",
                    space_complexity_derivation="O(1) auxiliary space.",
                    competing_families="Brute-Force Simulation (O(N^2)), Graph Reachability.",
                    why_competing_not_selected="GREEDY_PROVEN_SUFFICIENT: Naive circular simulation requires O(N^2); cumulative surplus prefix elimination resolves the problem in a single O(N) pass."
                )
            else:
                return GreedyDerivation(
                    pattern=pattern,
                    problem_objective="Determine reachability or find minimum jumps to reach the end of an array.",
                    feasibility_constraints="From index i, jump length is bounded by A[i] (can reach i + 1 .. i + A[i]).",
                    candidate_local_choice="Extend reach frontier to the maximum index reachable from any position in the current boundary.",
                    ordering_priority_rule="Linear scan tracking current_jump_end and farthest_reach.",
                    safe_choice_hypothesis="Expanding the boundary to the absolute maximum reachable index covers all possible positions reachable with <= k jumps.",
                    proof_method="Staying Ahead",
                    proof_derivation=(
                        "Let R_k be the farthest index reachable in k jumps. "
                        "For k = 1, R_1 = A[0]. "
                        "For k + 1, R_{k+1} = max_{0 <= i <= R_k} (i + A[i]). "
                        "Any alternative strategy with k jumps can reach at most a subset of [0..R_k]. "
                        "Therefore, the maximum reach in k + 1 jumps for any alternative strategy cannot exceed max_{i in S} (i + A[i]) <= R_{k+1}. "
                        "The greedy frontier stays ahead at every step k."
                    ),
                    feasibility_preservation="All positions up to current_jump_end are reachable within the current jump count.",
                    greedy_invariant="At jump step k, farthest_reach is maximal among all strategies using <= k jumps.",
                    termination_condition="Farthest reach >= N - 1 (destination reached) or scan index > farthest_reach (stuck). The construction is complete and the associated correctness proof establishes minimum jump count.",
                    global_correctness_argument="Staying ahead in reach frontier guarantees minimum jumps to destination.",
                    time_complexity_derivation="O(N) single-pass linear scan.",
                    space_complexity_derivation="O(1) auxiliary space.",
                    competing_families="Breadth-First Search on Graph (O(V + E) = O(N^2) naive), Dynamic Programming (O(N^2)).",
                    why_competing_not_selected="GRAPH_MODEL_IS_UNNECESSARY: BFS/DP explores every individual transition in O(N^2); interval reach compression enables exact solution in O(N) time and O(1) space."
                )

        elif "graph_mst" in pat:
            return GreedyDerivation(
                pattern=pattern,
                problem_objective="Find Minimum Spanning Tree (MST) connecting all vertices with minimum total edge weight.",
                feasibility_constraints="Acyclic subgraph connecting all V vertices (exactly V - 1 edges).",
                candidate_local_choice="Select the lightest edge that does not form a cycle (Kruskal) or lightest edge crossing the cut (Prim).",
                ordering_priority_rule="Sort edges ascending by weight (Kruskal) or min-heap of cut-crossing edges (Prim).",
                safe_choice_hypothesis="The lightest edge crossing any cut (S, V \\ S) is safe for MST (Cut Property).",
                proof_method="Cut Property / Matroid Independence",
                proof_derivation=(
                    "Cut Property: Let (S, V \\ S) be any cut in G = (V, E). Let e = (u, v) be the lightest edge crossing the cut. "
                    "Suppose there exists an MST T that does not contain e. "
                    "Adding e to T creates a unique simple cycle C. "
                    "Since u in S and v in V \\ S, the cycle C must cross the cut at least once more via another edge e'. "
                    "Construct T' = (T \\ {e'}) U {e}. "
                    "T' is a spanning tree, and weight(T') = weight(T) - weight(e') + weight(e). "
                    "Since e is the lightest edge crossing the cut, weight(e) <= weight(e'), so weight(T') <= weight(T). "
                    "Thus T' is also an MST containing e. By induction, the greedy choices construct an MST."
                ),
                feasibility_preservation="Cycle prevention maintained via DSU (Phase 3H) in Kruskal or visited set in Prim.",
                greedy_invariant="The selected edges form a forest that is a subgraph of some MST.",
                termination_condition="If the graph is connected, exactly V - 1 edges are selected. If the graph is disconnected, the algorithm terminates with a minimum spanning forest containing V - C edges, where C is the number of connected components. The construction is complete and the associated correctness proof establishes global optimality.",
                global_correctness_argument="Graphic matroids satisfy the greedy exchange axiom; Kruskal/Prim provably find the global minimum.",
                time_complexity_derivation="O(E log E) for Kruskal edge sorting + O(E * alpha(V)) DSU operations = O(E log V).",
                space_complexity_derivation="O(V) for DSU / priority queue.",
                competing_families="Branch and Bound, Generic Matroid Intersection.",
                why_competing_not_selected="GREEDY_PROVEN_SUFFICIENT: Graphic matroids satisfy hereditary and exchange axioms, making O(E log V) greedy edge selection optimal without exponential branch-and-bound."
            )

        else:
            # 3L-J: General Exchange / Dominance Greedy
            return GreedyDerivation(
                pattern=pattern,
                problem_objective="Optimize global objective via custom pairwise element ordering.",
                feasibility_constraints="Solution must satisfy problem-specific permutation or selection constraints.",
                candidate_local_choice="Sort elements by a custom comparator derived from pairwise exchange optimality.",
                ordering_priority_rule="Transitive total preorder comparator comp(A, B).",
                safe_choice_hypothesis="If comp(A, B) holds, then in any optimal arrangement, placing A before B never worsens the objective.",
                proof_method="Exchange Argument",
                proof_derivation=(
                    "Let comparator comp(A, B) define the objective-specific pairwise exchange relation (e.g. for Largest Number, a precedes b iff a+b > b+a). "
                    "Suppose an optimal arrangement O contains an adjacent inversion where comp(B, A) holds but A precedes B. "
                    "Swapping A and B alters only the contribution of the pair (A, B) because all other pairwise relative orders remain unchanged. "
                    "By definition of the objective-specific exchange condition, swapping an adjacent inverted pair cannot worsen the objective; "
                    "therefore repeated elimination of inversions yields an optimal ordering."
                ),
                feasibility_preservation="Comparator defines a strict weak ordering, ensuring sort stability and total ordering.",
                greedy_invariant="The ordered prefix contains no inversion under the objective-specific pairwise exchange relation.",
                termination_condition="Array sorted by comparator. The construction is complete and the associated correctness proof establishes global optimality.",
                global_correctness_argument="Transitivity of the exchange condition guarantees global optimality.",
                time_complexity_derivation="O(N log N) using standard comparison sort with custom comparator.",
                space_complexity_derivation="O(1) auxiliary space beyond array.",
                competing_families="Backtracking, Dynamic Programming on Permutations (O(N! * N) or O(2^N * N^2)).",
                why_competing_not_selected="GREEDY_PROVEN_SUFFICIENT: When pairwise exchange satisfies transitivity, greedy sorting reduces factorial/exponential permutation search to O(N log N)."
            )


# ── 21. Divide and Conquer & Backtracking Structural Reasoning (Phase 3M) ──

@dataclass
class DCBacktrackingDerivation:
    # Universal Core (all 10 patterns)
    pattern: str
    problem_objective: str
    subproblem_dependency_type: str
    termination_guarantee_type: str
    base_case_definition: str
    time_complexity_derivation: str
    space_complexity_derivation: str
    competing_families: str
    why_competing_not_selected: str
    algorithm_family: str = "divide_and_conquer_backtracking"

    # Divide & Conquer Specific (3M-A through 3M-E)
    dc_subproblem_split_strategy: str = "NOT_APPLICABLE"
    dc_combine_step_derivation: str = "NOT_APPLICABLE"
    dc_recurrence_relation: str = "NOT_APPLICABLE"

    # Search & Backtracking Specific (3M-F through 3M-I)
    backtracking_state_representation: str = "NOT_APPLICABLE"
    backtracking_pruning_rules: str = "NOT_APPLICABLE"
    backtracking_state_restoration_mechanism: str = "NOT_APPLICABLE"

    # Meet-in-the-Middle Specific (3M-J)
    mitm_split_dimension: str = "NOT_APPLICABLE"
    mitm_left_generation: str = "NOT_APPLICABLE"
    mitm_right_search_strategy: str = "NOT_APPLICABLE"


class DCBacktrackingStructuralReasoning:
    """
    Mathematical and structural foundation for Divide & Conquer, Backtracking,
    and Exponential Decomposition (Phase 3M).
    """

    @staticmethod
    def derive_proof(pattern: str, params: Optional[Dict[str, Any]] = None) -> DCBacktrackingDerivation:
        if params is None:
            params = {}
        pat = pattern.lower()

        if "merge_sort_inversions" in pat or "inversion" in pat:
            return DCBacktrackingDerivation(
                pattern=pattern,
                problem_objective="Count total inversions (or reverse pairs A[i] > 2*A[j]) across array.",
                subproblem_dependency_type="DISJOINT",
                termination_guarantee_type="COUNTING_CORRECTNESS",
                base_case_definition="Subarray of size <= 1 has 0 inversions and is trivially sorted.",
                time_complexity_derivation="T(n) = 2T(n/2) + Theta(n) = Theta(n log n) by Master Theorem Case 2.",
                space_complexity_derivation="O(n) temporary auxiliary storage for merge buffer.",
                competing_families="Brute-force O(n^2) pair comparison; Fenwick/Segment Tree inversion counting.",
                why_competing_not_selected="DC_DIVIDE_AND_CONQUER_OPTIMAL: Divide & conquer achieves optimal Theta(n log n) time without requiring coordinate compression or tree structures.",
                dc_subproblem_split_strategy="Midpoint bisection m = l + (r - l) / 2.",
                dc_combine_step_derivation="Sort both halves; for each element in right half, count elements in left half satisfying predicate via two pointers while merging.",
                dc_recurrence_relation="T(n) = 2T(n/2) + Theta(n)"
            )

        elif "quickselect" in pat:
            return DCBacktrackingDerivation(
                pattern=pattern,
                problem_objective="Find k-th smallest or largest order statistic in an unsorted array.",
                subproblem_dependency_type="DISJOINT",
                termination_guarantee_type="OPTIMALITY",
                base_case_definition="Subarray of size 1 where l == r == k.",
                time_complexity_derivation="Expected Theta(n) with random/median pivot (T(n) = T(n/2) + Theta(n)); worst-case Theta(n^2) with poor pivots; deterministic Theta(n) with median-of-medians.",
                space_complexity_derivation="O(1) auxiliary space with in-place 3-way partition; O(log n) call stack.",
                competing_families="Full Sorting O(n log n); Min/Max-Heap O(n log k).",
                why_competing_not_selected="QUICKSELECT_OPTIMAL: Partition-based selection prunes one entire half per step, achieving expected Theta(n) time versus O(n log n) full sort or O(n log k) heap.",
                dc_subproblem_split_strategy="3-way Dutch National Flag pivot partitioning into (< pivot, == pivot, > pivot).",
                dc_combine_step_derivation="Selection by partition: recurse exclusively into the single subrange containing index k; no combine step needed (O(1)).",
                dc_recurrence_relation="T(n) = T(n/2) + Theta(n) expected"
            )

        elif "closest_pair" in pat:
            return DCBacktrackingDerivation(
                pattern=pattern,
                problem_objective="Find the pair of 2D points with minimum Euclidean distance.",
                subproblem_dependency_type="DISJOINT",
                termination_guarantee_type="OPTIMALITY",
                base_case_definition="Base case of <= 3 points solved via exhaustive brute-force pairwise distance.",
                time_complexity_derivation="T(n) = 2T(n/2) + O(n) = O(n log n) when maintaining y-sorted lists.",
                space_complexity_derivation="O(n) auxiliary space for y-sorted strip buffer.",
                competing_families="Brute-force O(n^2) pairwise comparison; Delaunay Triangulation O(n log n).",
                why_competing_not_selected="CLOSEST_PAIR_DC_OPTIMAL: Divide & conquer achieves optimal O(n log n) with simple geometric packing in the 2*delta strip, avoiding complex Delaunay triangulation.",
                dc_subproblem_split_strategy="Vertical dividing line x = x_mid after initial sort by x-coordinate.",
                dc_combine_step_derivation="Let delta = min(delta_L, delta_R). Collect points within x_mid +- delta strip; sort by y; each point compares with at most 7 successors in y-order (geometric packing).",
                dc_recurrence_relation="T(n) = 2T(n/2) + O(n)"
            )

        elif "tree_centroid" in pat:
            return DCBacktrackingDerivation(
                pattern=pattern,
                problem_objective="Count or optimize paths in a tree satisfying specific length/weight properties.",
                subproblem_dependency_type="DISJOINT",
                termination_guarantee_type="COUNTING_CORRECTNESS",
                base_case_definition="Subtree of size 1 (single vertex) has 0 non-trivial paths.",
                time_complexity_derivation="T(n) = sum T(s_i) + O(n) <= O(n log n) since centroid removal guarantees each s_i <= n/2, yielding recursion depth <= log_2 n.",
                space_complexity_derivation="O(n) for tree adjacency, subtree sizes, and centroid decomposition tree.",
                competing_families="Tree DP with heavy-light decomposition or O(n^2) all-pairs path search.",
                why_competing_not_selected="CENTROID_DECOMPOSITION_OPTIMAL: Tree centroid partitioning guarantees balanced O(log n) tree depth, solving path queries in O(n log n).",
                dc_subproblem_split_strategy="Find tree centroid C whose removal partitions tree into subtrees of size <= n/2.",
                dc_combine_step_derivation="Count paths passing through centroid C (combining paths from different subtrees), subtract paths within same subtree to avoid invalid paths.",
                dc_recurrence_relation="T(n) <= max sum T(s_i) + O(n) with max s_i <= n/2"
            )

        elif "cdq" in pat:
            return DCBacktrackingDerivation(
                pattern=pattern,
                problem_objective="Solve multi-dimensional partial order counting or offline dynamic queries.",
                subproblem_dependency_type="DISJOINT",
                termination_guarantee_type="COUNTING_CORRECTNESS",
                base_case_definition="Single event interval [l, r] with l == r.",
                time_complexity_derivation="T(n) = 2T(n/2) + O(n log n) = O(n log^2 n) (or O(n log n) with Fenwick in combine).",
                space_complexity_derivation="O(n) for temporary event array and Fenwick tree.",
                competing_families="Nested 2D/3D Segment Trees (high constant factor, O(n log^2 n) space).",
                why_competing_not_selected="CDQ_OPTIMAL: CDQ transforms dynamic online multi-dimensional queries into offline divide & conquer with O(n) space versus large multi-dimensional data structure overhead.",
                dc_subproblem_split_strategy="Bisection on event/time dimension into [l, mid] and [mid + 1, r].",
                dc_combine_step_derivation="Sort left and right subproblems by second dimension; propagate modifications from left half to queries in right half using two pointers / Fenwick tree.",
                dc_recurrence_relation="T(n) = 2T(n/2) + O(n log n)"
            )

        elif "subsets_permutations" in pat:
            return DCBacktrackingDerivation(
                pattern=pattern,
                problem_objective="Enumerate all valid combinatorial subsets, combinations, or permutations.",
                subproblem_dependency_type="DISJOINT",
                termination_guarantee_type="ENUMERATION_COMPLETENESS",
                base_case_definition="Path length equals target size k or index reaches end of input array n.",
                time_complexity_derivation="O(2^n) for subsets; O(n!) for permutations; O(C(n, k)) for combinations.",
                space_complexity_derivation="O(n) auxiliary recursion stack and path buffer.",
                competing_families="Bitmask iteration O(n * 2^n); Gosper's hack for fixed-size combinations.",
                why_competing_not_selected="BACKTRACKING_ENUMERATION_OPTIMAL: Backtracking generates configurations directly with minimal overhead, supporting duplicate pruning via sorted order.",
                backtracking_state_representation="(index, current_path, used_mask/visited)",
                backtracking_pruning_rules="Sort elements; skip identical adjacent elements when previous sibling was not chosen: if (i > start && nums[i] == nums[i-1]) continue.",
                backtracking_state_restoration_mechanism="path.push_back(nums[i]) -> recurse -> path.pop_back()."
            )

        elif "constraint_satisfaction" in pat or "csp" in pat:
            return DCBacktrackingDerivation(
                pattern=pattern,
                problem_objective="Find one or all valid assignments satisfying exact constraints (N-Queens, Sudoku, Exact Cover).",
                subproblem_dependency_type="DISJOINT",
                termination_guarantee_type="FEASIBILITY",
                base_case_definition="All variables assigned (row == n for N-Queens, empty cells filled for Sudoku).",
                time_complexity_derivation="O(b^d) worst case where b is branching factor and d is depth; drastically reduced by constraint propagation.",
                space_complexity_derivation="O(d) recursion depth + O(1) bitmask constraint state.",
                competing_families="Integer Linear Programming (ILP), SAT Solvers.",
                why_competing_not_selected="CSP_BACKTRACKING_OPTIMAL: Lightweight bitmask constraint tracking provides microsecond-level pruning without heavy external solver dependencies.",
                backtracking_state_representation="Row index r, column mask cols, main diagonal mask diag1, anti-diagonal mask diag2.",
                backtracking_pruning_rules="Bitwise availability: available = ~(cols | diag1 | diag2) & ((1 << n) - 1). Only branch on unset bits.",
                backtracking_state_restoration_mechanism="Set bit on entry: cols |= (1 << c); clear bit on exit: cols &= ~(1 << c)."
            )

        elif "branch_and_bound" in pat:
            return DCBacktrackingDerivation(
                pattern=pattern,
                problem_objective="Find global optimal assignment under complex non-linear or constrained objective.",
                subproblem_dependency_type="DISJOINT",
                termination_guarantee_type="OPTIMALITY",
                base_case_definition="All decision variables assigned: update global best objective value.",
                time_complexity_derivation="O(b^d) worst case; average case governed by tightness of bounding function.",
                space_complexity_derivation="O(d) recursion stack and current partial solution state.",
                competing_families="Pure exhaustive backtracking O(b^d); Dynamic Programming (if Markovian).",
                why_competing_not_selected="BRANCH_AND_BOUND_OPTIMAL: Admissible bounding function prunes suboptimal branches early when state space lacks Markovian structure for DP.",
                backtracking_state_representation="(step, current_state, current_cost, best_cost)",
                backtracking_pruning_rules="If direction == MINIMIZE and (current_cost + lower_bound >= best_cost), prune subtree. If direction == MAXIMIZE and (current_value + upper_bound <= best_value), prune subtree.",
                backtracking_state_restoration_mechanism="Revert state mutation and subtract incremental cost upon return from recursive branch."
            )

        elif "state_space_search" in pat:
            return DCBacktrackingDerivation(
                pattern=pattern,
                problem_objective="Explore state space to find target state or all matching patterns (Word Search, Maze, Puzzle).",
                subproblem_dependency_type="DISJOINT",
                termination_guarantee_type="FEASIBILITY",
                base_case_definition="Target state reached (e.g. word matched, destination cell reached) or search depth exhausted.",
                time_complexity_derivation="O(4^L) for grid search of length L; O(V + E) when visited states memoized.",
                space_complexity_derivation="O(L) recursion depth + O(1) in-place grid marker.",
                competing_families="BFS (for shortest path in unweighted graph); Bidirectional Search.",
                why_competing_not_selected="STATE_SPACE_BACKTRACKING_OPTIMAL: In-place DFS backtracking uses O(L) stack space without maintaining large BFS frontier queues.",
                backtracking_state_representation="(row, col, match_index, visited_in_path)",
                backtracking_pruning_rules="Boundary check (0 <= r < R, 0 <= c < C); character mismatch board[r][c] != word[k]; already visited in current path.",
                backtracking_state_restoration_mechanism="In-place char masking: temp = board[r][c]; board[r][c] = '#'; recurse; board[r][c] = temp."
            )

        elif "meet_in_the_middle" in pat or "meet_in_middle" in pat:
            return DCBacktrackingDerivation(
                pattern=pattern,
                problem_objective="Solve exact/closest subset sum or combination for N <= 40 where 2^N is intractable.",
                subproblem_dependency_type="DISJOINT",
                termination_guarantee_type="OPTIMALITY",
                base_case_definition="Subset generation completed for each half of size <= N/2.",
                time_complexity_derivation="O(2^(N/2) * log(2^(N/2))) = O(N * 2^(N/2)): generate two halves of size 2^(N/2) and combine via binary search or two pointers.",
                space_complexity_derivation="O(2^(N/2)) memory to store generated values for the first half.",
                competing_families="Full exhaustive search O(2^N); Dynamic Programming O(N * Target).",
                why_competing_not_selected="MEET_IN_THE_MIDDLE_OPTIMAL: When N approx 40 and target sum is large (10^12), DP is intractable (O(N * W) exceeds memory); Meet in the middle reduces 2^40 approx 10^12 operations to 2 * 2^20 approx 2 * 10^6 operations.",
                mitm_split_dimension="Bisection of input array into left half A[0 ... N/2 - 1] and right half A[N/2 ... N - 1].",
                mitm_left_generation="Generate all 2^(floor(N/2)) subset sums of left half; sort the resulting array.",
                mitm_right_search_strategy="For each subset sum s of right half, binary search (or two pointers) for target - s in sorted left sums."
            )

        else:
            return DCBacktrackingDerivation(
                pattern=pattern,
                problem_objective="Solve divide-and-conquer or backtracking problem.",
                subproblem_dependency_type="DISJOINT",
                termination_guarantee_type="FEASIBILITY",
                base_case_definition="Base case reached.",
                time_complexity_derivation="T(n) derived by recurrence or branching factor.",
                space_complexity_derivation="O(n) recursion depth.",
                competing_families="Exhaustive search.",
                why_competing_not_selected="DC_BACKTRACKING_OPTIMAL: Problem structure matches divide & conquer / backtracking decomposition."
            )



