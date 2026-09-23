# CHUP Phase 3H — Advanced DSU / Union-Find Domain Walkthrough

## 1. Executive Summary

Phase 3H integrates the **Advanced Disjoint Set Union / Union-Find (DSU)** domain into CHUP. Building upon the foundational DSU capability established in Phase 3F Graph, Phase 3H extends DSU into an advanced, reusable reasoning engine covering:
- Equivalence-class partitioning and incremental dynamic connectivity
- Component metadata aggregation
- Weighted relations and potential difference networks ($value[x] - value[parent[x]] = w$)
- Parity constraints and bipartite 2-coloring ($color[x] \oplus color[parent[x]] = p$)
- Backtracking/undo semantics via Rollback DSU ($O(\log N)$ by rank/size without path compression)
- Offline dynamic connectivity via segment-tree-over-time divide and conquer ($O(M \log Q \log N + Q \log N)$)
- Kruskal minimum spanning tree connectivity and cycle detection support
- System of difference constraints and contradiction detection
- Formal boundary classification rejecting arbitrary online deletions via `DSU_DELETION_UNSUPPORTED`

All verification suites achieved **100% pass rates** with **zero regressions** across all previously frozen domains (Two Pointers, Monotonic Stack, Binary Search, Trie, Tree, Graph, Heap, and the TypeScript master suite).

---

## 2. Core Architecture & Taxonomy

### 2.1 Taxonomy Definition (`pointer_algorithms/knowledge/taxonomy.py`)
- **`DSUKind`**:
  - `BASIC = "basic"`: Standard path compression + union by rank/size.
  - `WEIGHTED = "weighted"`: Relative potential tracking along tree paths.
  - `PARITY = "parity"`: Modular arithmetic / XOR parity tracking along tree paths.
  - `ROLLBACK = "rollback"`: History undo stack without path compression.
- **`DSUOperationKind`**:
  - `FIND = "find"`: Find representative with path compression or rank-only traversal.
  - `UNION = "union"`: Merge two equivalence classes.
  - `CONNECTED = "connected"`: Query if elements share a representative.
  - `COMPONENT_SIZE = "component_size"`: Query component cardinality.
  - `COMPONENT_METADATA = "component_metadata"`: Query component state summary.
  - `DIFF = "diff"`: Query potential difference $value[u] - value[v]$.
  - `CONSISTENCY_CHECK = "consistency_check"`: Check edge consistency with existing relations.
  - `SNAPSHOT = "snapshot"`: Record current operation count / state.
  - `ROLLBACK = "rollback"`: Revert mutations back to a previous snapshot.
- **`AlgorithmFamily.DSU = "dsu"`**
- **10 Pattern Kinds**:
  1. `dsu_basic`: Standard disjoint-set partition with path compression and union-by-rank.
  2. `dsu_component_metadata`: Incremental component state aggregation (sum, min, max, size).
  3. `dsu_dynamic_connectivity`: Incremental dynamic connectivity queries.
  4. `dsu_weighted`: Potential networks maintaining $value[x] - value[y] = w$.
  5. `dsu_potential_difference`: Direct relative difference queries between elements in the same component.
  6. `dsu_parity`: Parity / bipartite 2-coloring relations via XOR modular arithmetic.
  7. `dsu_rollback`: Undoable union operations tracking history without path compression.
  8. `dsu_offline_dynamic_connectivity`: Offline additions and deletions scheduled on a segment tree over time.
  9. `dsu_kruskal_support`: Incremental acyclic edge selection for Kruskal's algorithm.
  10. `dsu_constraint_consistency`: Validation of difference or parity constraints with contradiction detection.

---

## 3. Structural Reasoning & Formal Invariants

### 3.1 Structural Invariants & Conventions (`pointer_algorithms/reasoning/reasoning_engine.py`)
- **Equivalence Partition**:
  - Partitions universe $U = \{0, 1, \dots, N-1\}$ into disjoint subsets $S_1, \dots, S_k$ such that $\bigcup S_i = U$ and $S_i \cap S_j = \emptyset$.
  - Canonical representative invariant: $\forall x \in U, \text{find}(x) \in S(x)$, and $x \equiv y \iff \text{find}(x) = \text{find}(y)$.
- **Component Metadata Merge**:
  - Combines metadata on set union: $\text{meta}[\text{new\_root}] \leftarrow \text{combine}(\text{meta}[r_u], \text{meta}[r_v])$.
  - The requested component state must be maintainable correctly from stored metadata and available merge operations.
- **Potential Difference Convention & Root-Orientation**:
  - Tree convention: $potential[x] = value[x] - value[parent[x]]$.
  - Path compression accumulates potential to root:
    $$potential\_to\_root[x] = value[x] - value[root_x] \quad (\text{shorthand } px)$$
  - Difference query: $(value[u] - value[root]) - (value[v] - value[root]) = value[u] - value[v] = px - py$.
  - **Union update under constraint** $value[u] - value[v] = w$:
    - **If $root_u$ becomes child of $root_v$ ($parent[root_u] = root_v$):**
      $$weight[root_u] = w + potential\_to\_root[v] - potential\_to\_root[u] = w - px + py$$
    - **If $root_v$ becomes child of $root_u$ ($parent[root_v] = root_u$):**
      $$weight[root_v] = potential\_to\_root[u] - potential\_to\_root[v] - w = px - py - w$$
  - Contradiction detected if $root_u = root_v$ and $px - py \neq w$.
- **Parity / Bipartite Convention**:
  - Parity convention: $parity[x] = color[x] \oplus color[parent[x]]$.
  - Relative color to root: $color[x] \oplus color[root] = \bigoplus_{e \in x \rightsquigarrow root} parity[e]$.
  - Union update when joining $u$ and $v$ with relation $color[u] \oplus color[v] = p$ (attaching $root_u$ under $root_v$):
    $$parity[root_u] = p \oplus parity\_to\_root[u] \oplus parity\_to\_root[v]$$
  - Contradiction occurs if $root_u = root_v$ and $(parity\_to\_root[u] \oplus parity\_to\_root[v]) \neq p$.
- **Rollback Invariant**:
  - Strict preservation of tree invertibility: mutations are logged to a history stack `RollbackOp{u, v, rank_inc}`.
  - **No path compression allowed**: Path compression mutates parent pointers along query paths unpredictably, violating $O(1)$ rollback per edge.
  - Complexity: Union and find take $O(\log N)$ worst-case using union-by-rank / size; rollback of $K$ operations takes $O(K)$.
- **Offline Dynamic Connectivity Complexity**:
  - Decomposes edge active lifespans into intervals over a segment tree over time (depth $O(\log Q)$).
  - Traversal via DFS pushes active edges into Rollback DSU ($O(\log N)$), answers queries at leaf nodes, and rolls back mutations on backtrack.
  - **Total time complexity**:
    $$O(M \log Q \log N + Q \log N)$$
    where:
    - $N$ = number of vertices
    - $Q$ = number of time/query operations
    - $M$ = number of edge lifetime intervals (not necessarily identical to input edge count)
- **Arbitrary Online Deletions Limitation**:
  - Arbitrary online edge deletion cannot be supported in polylogarithmic time by standard DSU or Rollback DSU.
  - Rollback DSU only supports LIFO un-merging of historical mutations, not arbitrary edge deletions.
  - Such requests must be rejected via `DSU_DELETION_UNSUPPORTED`.

---

## 4. Candidate Elimination Rules (`candidate_eliminator.py`)

1. `DSU_DELETION_UNSUPPORTED`:
   Arbitrary online edge deletion cannot be handled by standard DSU or Rollback DSU merely because rollback exists.
   Supported models:
   - additions only $\implies$ Basic DSU
   - explicit historical rollback $\implies$ Rollback DSU
   - known add/remove timeline $\implies$ Offline Dynamic Connectivity
2. `DSU_ONLINE_OFFLINE_MISMATCH`: Offline dynamic connectivity proposed for online stream without pre-known query timestamps.
3. `DSU_WEIGHT_MODEL_MISMATCH`: Weighted DSU applied to problems without additive potential constraints.
4. `DSU_PARITY_MODEL_MISMATCH`: Parity DSU applied to non-parity / non-bipartite 2-coloring relations.
5. `DSU_ROLLBACK_REQUIRED`: Standard DSU with path compression proposed when history undo/rollback is required.
6. `DSU_METADATA_MERGE_UNDEFINED`:
   The requested component state cannot be maintained correctly from the stored metadata and the available merge operation.
7. `DSU_CONTRADICTION_DETECTED`: Inconsistent constraints added to an unresolvable equivalence state.
8. `DSU_COMPLEXITY_EXCEEDED`: DSU operations exceed the allowed time budget.

---

## 5. C++17 Code Generator (`generator/dsu_cpp_generator.py`)

Emits clean, idiomatic C++17 implementations:
- **`BasicDSU`**: Vector parent and rank, path compression `find(x)`, union by rank, `connected(u, v)`.
- **`MetadataDSU`**: Vector parent, size, and custom metadata (`min`, `max`, `sum`) merged on union.
- **`PotentialDSU`**: Vector parent and `weight` offset; path compression updating offsets recursively:
  ```cpp
  int find(int i) {
      if (parent[i] == i) return i;
      int root = find(parent[i]);
      weight[i] += weight[parent[i]];
      return parent[i] = root;
  }
  ```
- **`ParityDSU`**: Vector parent and `parity` (0 or 1); path compression updating parity via XOR.
- **`RollbackDSU`**: Vector parent and rank; history stack recording `RollbackOp{u, v, rank_inc}` without path compression.
- **`OfflineDynamicConnectivity`**: Segment tree over time $[0, Q-1]$ storing edge intervals, solved with `RollbackDSU` and DFS traversal.

---

## 6. Multi-Layer Verification Results

Verification of Phase 3H relies on a defense-in-depth approach combining curated problem benchmarks, blind real-world holdout evaluation, non-DSU discrimination testing, and extensive randomized oracle validation.

### 6.1 DSU Domain Suites

| Suite | Scope / Description | Tests / Ops | Result | Pass Rate |
| :--- | :--- | :--- | :--- | :--- |
| **Unit Tests** | `pointer_algorithms/dsu/test_suite.py` | 18 tests | Passed | **100.0%** |
| **Main Benchmark** | `dsu_benchmark.py` (Categories 3H-A to 3H-O, D-01..D-60) | 60 problems | Passed | **100.0%** |
| **Blind Holdout** | `dsu_blind_holdout.py` (Unseen real-world problems DH-01..DH-12) | 12 problems | Passed | **100.0%** |
| **"No DSU" Discrimination** | `dsu_no_dsu_holdout.py` (Non-DSU discrimination ND-01..ND-12) | 12 problems | Passed | **100.0%** |
| **Randomized Oracle Validation** | `dsu_randomized_test.py` (10 patterns $\times$ 15-20 seeds) | 165 runs / 3,650 ops | Passed | **100.0%** |

*(Note: The randomized suite validates generated C++ against independent Python reference oracles across pseudo-random operational streams, providing strong empirical evidence rather than formal mathematical proof).*

### 6.2 Multi-Domain Regression Results (Zero Regressions)

| Domain | Benchmark Suite | Unit Test Suite | Pass Rate |
| :--- | :--- | :--- | :--- |
| **Pointer Basics (3A)** | `pointer_algorithms/test_suite.py` | 13 / 13 tests | **100.0%** |
| **Monotonic Stack (3B)** | `ms_benchmark.py` (40 / 40) | `monotonic_stack/test_suite.py` (8 / 8) | **100.0%** |
| **Binary Search (3C)** | `bs_benchmark.py` (40 / 40) | `binary_search/test_suite.py` (9 / 9) | **100.0%** |
| **Trie (3D)** | `tr_benchmark.py` (40 / 40) | `trie/test_suite.py` (10 / 10) | **100.0%** |
| **Tree (3E)** | `tree_benchmark.py` (50 / 50) | `tree/test_suite.py` (13 / 13) | **100.0%** |
| **Graph (3F)** | `graph_benchmark.py` (60 / 60) | `graph/test_suite.py` (26 / 26) | **100.0%** |
| **Heap (3G)** | `heap_benchmark.py` (56 / 56) | `heap/test_suite.py` (19 / 19) | **100.0%** |
| **Advanced DSU (3H)** | `dsu_benchmark.py` (60 / 60) | `dsu/test_suite.py` (18 / 18) | **100.0%** |
| **TypeScript Master Suite** | `npm test` | 275 / 275 tests | **100.0%** |

---

## 7. Milestone Domain Status

```text
Phase 3F Graph       COMPLETE / HARDENED / FROZEN
Phase 3G Heap        COMPLETE / CORRECTED / FROZEN
Phase 3H DSU         COMPLETE / VERIFIED / FROZEN
Next Milestone       Phase 3I Fenwick Tree (Binary Indexed Tree)
```
