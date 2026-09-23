# CHUP Phase 3G — Heap / Priority Queue Domain Walkthrough

## 1. Executive Summary

Phase 3G integrates the **Heap / Priority Queue** algorithmic domain into CHUP. The domain is built upon rigorous structural proofs, bounded retention invariants, asymptotic trade-off reasoning, candidate elimination against competitors (total sorting, BST/balanced search trees, quickselect, FIFO queues, LIFO stacks), clean C++17 code generation, and capability composition (`heap_priority_frontier` consumed by Graph Dijkstra and Prim).

All verification suites achieved **100% pass rates** with **zero regressions** across previously frozen domains (Two Pointers, Monotonic Stack, Binary Search, Trie, Tree, Graph, and the TypeScript master suite).

---

## 2. Core Architecture & Taxonomy

### 2.1 Taxonomy Definition (`pointer_algorithms/knowledge/taxonomy.py`)
- **`HeapKind`**:
  - `MIN_HEAP = "min_heap"`
  - `MAX_HEAP = "max_heap"`
  *(Strictly no double-ended priority structure enum; dynamic median and interval tracking use dual paired heaps).*
- **`HeapOperationKind`**:
  - `PEEK = "peek"`
  - `INSERT = "insert"`
  - `EXTRACT = "extract"`
  - `UPDATE = "update"`
  - `REMOVE = "remove"`
  - `BUILD = "build"`
  - `MERGE = "merge"`
- **`AlgorithmFamily.HEAP = "heap"`**
- **11 Pattern Kinds**:
  1. `heap_min_priority_queue`: Dynamic minimum element extraction and insertion.
  2. `heap_max_priority_queue`: Dynamic maximum element extraction and insertion.
  3. `heap_build`: Floyd's linear-time $O(N)$ bottom-up heap construction.
  4. `heap_top_k`: Bounded capacity-$K$ retention of extremal elements from a stream or collection.
  5. `heap_kth_element`: $K$-th extremal order statistic via size-$K$ heap.
  6. `heap_k_way_merge`: Multiway sorted sequence merge tracking $K$ heads.
  7. `heap_two_heaps`: Complementary balanced partition (max-heap for lower half, min-heap for upper half).
  8. `heap_dynamic_median`: Continuous running median maintenance on streaming data.
  9. `heap_scheduling`: Earliest available resource / interval event processing.
  10. `heap_greedy_selection`: Huffman / rope-splicing repeated smallest pair combination.
  11. `heap_lazy_deletion`: Amortized element removal using auxiliary tombstone frequency map.

---

## 3. Structural Reasoning & Formal Invariants

### 3.1 Structural Proofs (`pointer_algorithms/reasoning/reasoning_engine.py`)
- **Complete Binary Tree in Contiguous Array**:
  $$\text{parent}(i) = \left\lfloor \frac{i-1}{2} \right\rfloor, \quad \text{left}(i) = 2i + 1, \quad \text{right}(i) = 2i + 2$$
- **Asymptotic Complexity**:
  - Root Extremal Access: $O(1)$
  - Sift-Up / Sift-Down: $O(\log N)$
  - Floyd's Bottom-Up Construction:
    $$\sum_{h=0}^{\lfloor\log_2 N\rfloor} \frac{N}{2^{h+1}} O(h) = O(N)$$
- **Bounded Top-K Retention Invariant**:
  - **Top-$K$ Largest**: Maintain a **Min-Heap** of size $K$. The root holds the current $K$-th largest element (the weakest among the top $K$). Any incoming element $x > \text{root}$ evicts the root via `pop()` and inserts $x$.
  - **Top-$K$ Smallest**: Maintain a **Max-Heap** of size $K$. The root holds the current $K$-th smallest element (the weakest among the bottom $K$). Any incoming element $x < \text{root}$ evicts the root via `pop()` and inserts $x$.
- **Array Heap vs. Balanced BST**:
  - Array heap: flat contiguous storage, low structural overhead, excellent cache locality, fast extremal access.
  - BST/Set: ordered search, predecessor/successor navigation, and arbitrary-key operations, but incurs additional node-level structural overhead, pointer indirection, and dynamic rebalancing costs. Heap preferred when arbitrary search/predecessor is not required.
- **Capability Composition**:
  - Dijkstra and Prim algorithms declare `"composedCapabilities": ["heap_priority_frontier"]`, consuming heap semantics cleanly through modular contracts without architectural coupling.

---

## 4. Invariant Engine & Movement Derivations

### 4.1 4-Phase Invariants (`pointer_algorithms/invariants/invariant_engine.py`)
Each pattern defines explicit:
- `before_iteration`: Heap invariants established prior to the main loop.
- `during_iteration`: Structural heap ordering maintained at loop boundaries.
- `after_movement`: Local sift or eviction operations restoring the heap property.
- `at_termination`: Final state guaranteeing correct extremal or bounded subset output.

### 4.2 Candidate Elimination Rules (`pointer_algorithms/recognition/candidate_eliminator.py`)
- `HEAP_WRONG_EXTREMUM`: Heap direction (min vs max) inverts the required invariant.
- `HEAP_CAPACITY_MISMATCH`: The heap exceeds the allowed retention capacity or fails to enforce the required bounded-state invariant (`heap_size <= K`, `heap_size == min(N, K)`).
- `HEAP_UNNECESSARY_SORTING`: Candidate attempts full $O(N \log N)$ sorting when only $O(N \log K)$ or $O(N)$ partial selection is required.
- `HEAP_ARBITRARY_DELETE_MISMATCH`: Candidate requires $O(\log N)$ arbitrary key search/deletion without a tombstone mechanism.
- `HEAP_UPDATE_SEMANTICS_MISMATCH`: Dynamic key decrease/increase required without handle mapping.
- `HEAP_COMPLEXITY_EXCEEDED`: Heap operations exceed available time budget.

---

## 5. C++17 Code Generator (`generator/heap_cpp_generator.py`)

Emits clean, idiomatic C++17 implementations:
- Standard container: `std::priority_queue<T, std::vector<T>, std::greater<T>>` for min-heaps, default `std::priority_queue<T>` for max-heaps.
- Bottom-up heap construction: `std::make_heap` with in-place vector rearrangement.
- Multi-way merge: `std::priority_queue` over tuples `(value, array_index, element_index)`.
- Dynamic median: Balanced pair of `priority_queue<long long>` (lower max-heap) and `priority_queue<long long, vector<long long>, greater<long long>>` (upper min-heap).
- Lazy deletion: Priority queue paired with `std::unordered_map<long long, int> tombstone_counts`.

---

## 6. Verification Results

| Suite | Category / Scope | Test Count | Result | Pass Rate |
| :--- | :--- | :--- | :--- | :--- |
| **Unit Tests** | `pointer_algorithms/heap/test_suite.py` | 19 | Passed | **100.0%** |
| **Randomized Stress** | `heap_randomized_test.py` (11 patterns x 15 tests, seeds 1..100) | 165 | Passed | **100.0%** |
| **Main Benchmark** | `heap_benchmark.py` (Categories 3G-A through 3G-N) | 56 | Passed | **100.0%** |
| **Blind Holdout** | `heap_blind_holdout.py` (Unseen real-world problems BH-01..BH-12) | 12 | Passed | **100.0%** |
| **'No Heap' Holdout** | `heap_no_heap_holdout.py` (Discrimination battery NH-01..NH-10) | 10 | Passed | **100.0%** |

### Multi-Domain Regression Results (Zero Regressions)

| Domain / Suite | Scope | Result | Pass Rate |
| :--- | :--- | :--- | :--- |
| **Main Pointer Tests** | `pointer_algorithms/test_suite.py` | 13/13 | **100.0%** |
| **Monotonic Stack (3B)** | `pointer_algorithms/monotonic_stack/evaluation/ms_benchmark.py` | 40/40 | **100.0%** |
| **Binary Search (3C)** | `pointer_algorithms/binary_search/evaluation/bs_benchmark.py` | 40/40 | **100.0%** |
| **Trie (3D)** | `pointer_algorithms/trie/evaluation/tr_benchmark.py` | 40/40 | **100.0%** |
| **Tree (3E)** | `pointer_algorithms/tree/evaluation/tree_benchmark.py` | 50/50 | **100.0%** |
| **Graph (3F)** | `pointer_algorithms/graph/evaluation/graph_benchmark.py` | 60/60 | **100.0%** |
| **TypeScript Master** | `npm test` | 275/275 | **100.0%** |
