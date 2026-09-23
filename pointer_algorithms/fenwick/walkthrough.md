# CHUP Phase 3I — Fenwick Tree (Binary Indexed Tree) Verification & Walkthrough Report

## 1. Executive Summary

Phase 3I establishes **Fenwick Tree (Binary Indexed Tree / BIT)** as a first-class, general algorithmic family within the CHUP system. Rather than treating Fenwick Trees as a single memorized snippet, CHUP implements deep structural and algebraic reasoning across 10 pattern variants organized into Tier A (Core Variants), Tier B (Applications), and Tier C (Transformations), rigorous candidate elimination rules, C++17 generators with bounded integer width policies and 1-based internal indexing, and comprehensive reference oracles.

### Verification Battery Results

| Test Battery | Target Domain | Tests | Passed | Success Rate |
| :--- | :--- | :---: | :---: | :---: |
| **Fenwick Main Benchmark** (`fenwick_benchmark.py`) | 3I (Tiers A, B, C) | 60 | 60 | **100.0%** |
| **Fenwick Blind Holdout** (`fenwick_blind_holdout.py`) | 3I (FH-01..FH-12) | 12 | 12 | **100.0%** |
| **Fenwick 'No Fenwick' Holdout** (`fenwick_no_fenwick_holdout.py`) | 3I Discrimination | 12 | 12 | **100.0%** |
| **Fenwick Randomized Differential** (`fenwick_randomized_test.py`) | 3I Differential Stress | 165 | 165 | **100.0%** (4,125 ops) |
| **Fenwick Unit Tests** (`test_suite.py`) | 3I Unit Logic | 14 | 14 | **100.0%** |
| **DSU Main Benchmark** (`dsu_benchmark.py`) | 3H Regression | 60 | 60 | **100.0%** |
| **DSU Blind Holdout** (`dsu_blind_holdout.py`) | 3H Regression | 12 | 12 | **100.0%** |
| **DSU Discrimination Holdout** (`dsu_no_dsu_holdout.py`) | 3H Regression | 12 | 12 | **100.0%** |
| **DSU Randomized Differential** (`dsu_randomized_test.py`) | 3H Regression | 165 | 165 | **100.0%** (3,650 ops) |
| **Heap Main Benchmark** (`heap_benchmark.py`) | 3G Regression | 56 | 56 | **100.0%** |
| **Graph Main Benchmark** (`graph_benchmark.py`) | 3F Regression | 60 | 60 | **100.0%** |
| **All Domain Unit Tests** (`-p "test_suite.py"`) | 3A–3I Regressions | 112 | 112 | **100.0%** |
| **TypeScript Master Test Suite** (`npm test`) | Full System | 275 | 275 | **100.0%** |

---

## 2. Mathematical & Algebraic Foundations

### 2.1 Lowbit & Interval Decomposition
A Fenwick tree stores partial aggregates of an underlying 1-based array $A[1 \dots N]$ in a tree array $T[1 \dots N]$.
- **Lowbit Extraction**:
  $$\text{lowbit}(i) = i \ \& \ (-i)$$
- **Interval Coverage**: Node $i$ covers the contiguous half-open interval:
  $$[i - \text{lowbit}(i) + 1, \, i]$$
- **Index Traversal**:
  - Point Add / Update: $i \leftarrow i + \text{lowbit}(i)$ (traversing ancestors)
  - Prefix Query: $i \leftarrow i - \text{lowbit}(i)$ (accumulating disjoint interval blocks)

### 2.2 Algebraic Scope Separation
CHUP strictly distinguishes between algebraic structures rather than assuming universal invertibility:
1. **Prefix Aggregation**: Requires a **commutative monoid** $(S, \oplus, e)$ where $\oplus$ is associative and commutative with identity $e$. Non-commutative operations cannot be queried via standard Fenwick interval decomposition because node intervals are accumulated in bit-order.
2. **Range Query from Two Prefixes**: Requires an appropriate **commutative group** $(S, \oplus, \ominus, e)$ where an inverse operation $\ominus$ exists such that:
   $$\sum_{i=l}^r A[i] = \text{prefix}(r) \ominus \text{prefix}(l - 1)$$
3. **Prefix Extremum**: Supported under monotonic updates where equality is valid:
   - Prefix minimum:
     $$\text{newValue} \le \text{oldValue}$$
   - Prefix maximum:
     $$\text{newValue} \ge \text{oldValue}$$
   - Arbitrary point replacement is **unsupported** by Fenwick extremum variants and eliminated via `FENWICK_STRUCTURAL_INCOMPATIBILITY` in favor of Segment Trees.

### 2.3 Two-Fenwick Range Add & Range Query Derivation
To support dynamic range additions and dynamic range sum queries in $O(\log N)$ time:
- Let difference array $D[i] = A[i] - A[i-1]$ with $A[0] = 0$.
- The prefix sum is:
  $$\text{prefix}(x) = \sum_{i=1}^x A[i] = \sum_{i=1}^x \sum_{j=1}^i D[j] = \sum_{j=1}^x (x - j + 1) D[j] = (x + 1) \sum_{j=1}^x D[j] - \sum_{j=1}^x j \cdot D[j]$$
- Maintain two Fenwick trees:
  - $B_1$ maintains $D[j]$
  - $B_2$ maintains $j \cdot D[j]$
- Updates for range addition $[l, r]$ by $\Delta$:
  - $B_1$: add $\Delta$ at $l$, add $-\Delta$ at $r + 1$
  - $B_2$: add $l \cdot \Delta$ at $l$, add $-(r + 1) \cdot \Delta$ at $r + 1$
- Query: $\text{prefix}(x) = (x + 1) \cdot B_1.\text{query}(x) - B_2.\text{query}(x)$.

### 2.4 Binary Lifting for K-th Element
When values or elements are non-negative frequencies, the prefix sums $\text{prefix}(i)$ are monotonically non-decreasing.
- The $K$-th element search finds the smallest index $idx$ such that $\text{prefix}(idx) \ge K$.
- Utilizing the binary representation of the tree size, binary lifting inspects powers of 2 ($2^{\lfloor \log_2 N \rfloor}, \dots, 2^0$):
  ```cpp
  int idx = 0;
  for (int step = 1 << __lg(N); step > 0; step >>= 1) {
      if (idx + step <= N && tree[idx + step] < k) {
          idx += step;
          k -= tree[idx];
      }
  }
  return idx + 1;
  ```
- **Time Complexity**: $O(\log N)$ in a single pass without binary search overhead ($O(\log^2 N)$).
- **Non-negative Requirement**: If frequency values can become negative, the Fenwick K-th binary-lifting invariant is invalid because prefix sums lose monotonicity. Possible alternatives depend on the specific problem requirements (e.g., Segment Tree, balanced ordered structure, order-statistics tree, or another structure supporting dynamic rank operations with negative counts). CHUP eliminates this candidate via `FENWICK_KTH_NEGATIVE_FREQUENCY`.

---

## 3. Pattern Taxonomy & Structural Invariants

The 10 patterns are organized into the three architectural tiers defined in the implementation plan:

### Tier A — Core Fenwick Variants
1. **`fenwick_point_update_prefix_query`**:
   - *Description*: 1D Point add, Prefix / Range sum.
   - *Structural Invariant*: Node $T[i]$ stores $\sum_{k = i - \text{lowbit}(i) + 1}^i A[k]$. Add propagates to ancestors $i \leftarrow i + \text{lowbit}(i)$; query accumulates disjoint blocks $i \leftarrow i - \text{lowbit}(i)$.
2. **`fenwick_range_update_point_query`**:
   - *Description*: 1D Difference range add, Point value query.
   - *Structural Invariant*: Maintains difference array $D[i] = A[i] - A[i-1]$ in Fenwick tree. Range add $[l, r]$ by $\Delta$ modifies $D[l] \mathrel{+}= \Delta$ and $D[r+1] \mathrel{-}= \Delta$. Point value $A[x]$ equals prefix sum $\sum_{k=1}^x D[k]$.
3. **`fenwick_range_update_range_query`**:
   - *Description*: Two-Fenwick algebraic range add, Range sum query.
   - *Structural Invariant*: Tree $B_1$ maintains $D[j]$; Tree $B_2$ maintains $j \cdot D[j]$. Prefix sum $\text{prefix}(x) = (x + 1) \sum B_1 - \sum B_2$.
4. **`fenwick_frequency`**:
   - *Description*: Dynamic frequency table and cumulative counting.
   - *Structural Invariant*: The underlying frequency array $F[v]$ stores the frequency of value $v$. Fenwick node $T[i]$ stores the aggregate frequency over $[i - \text{lowbit}(i) + 1, i]$. Query $\text{prefix}(v)$ computes cumulative frequency of elements $\le v$.
5. **`fenwick_prefix_extremum`**:
   - *Description*: Monotonic prefix min / max under non-increasing (min: $\text{newValue} \le \text{oldValue}$) or non-decreasing (max: $\text{newValue} \ge \text{oldValue}$) point updates.
   - *Structural Invariant*: Node $T[i] = \text{opt}_{k \in [i - \text{lowbit}(i) + 1, i]} A[k]$. Updates are monotonic ($\text{newValue} \le \text{oldValue}$ for min, $\text{newValue} \ge \text{oldValue}$ for max, equality is valid); arbitrary replacement is unsupported.
6. **`fenwick_2d_point_update_range_query`**:
   - *Description*: 2D Grid submatrix point add, Rectangle sum query.
   - *Structural Invariant*: Node $T[r][c]$ represents the aggregate over:
     $$[r - \text{lowbit}(r) + 1, \, r] \times [c - \text{lowbit}(c) + 1, \, c]$$
     Rectangle query is derived via 2D inclusion-exclusion over prefix queries:
     $$P(r_2, c_2) - P(r_1 - 1, c_2) - P(r_2, c_1 - 1) + P(r_1 - 1, c_1 - 1)$$

### Tier B — Applications
7. **`fenwick_kth_element`**:
   - *Description*: $K$-th order statistic via single-pass binary lifting in $O(\log M)$.
   - *Structural Invariant*: Frequencies are non-negative, ensuring monotonic prefix sums. Powers of 2 step through tree nodes to locate the smallest index with cumulative frequency $\ge K$.
8. **`fenwick_inversion_counting`**:
   - *Description*: Inversion counting and permutation disorder via coordinate-compressed frequency Fenwick.
   - *Structural Invariant*:
     - Right-to-left traversal: query count of values $< a[i]$, counting elements $a[j] < a[i]$ for $j > i$.
     - Left-to-right traversal: query count of values $> a[i]$, counting earlier elements greater than $a[i]$.
9. **`fenwick_multiset`**:
   - *Description*: Dynamic multiset supporting insert, delete, count, rank, and $K$-th selection.
   - *Structural Invariant*: Non-negative multiplicity array; rank computed via prefix sum $\text{prefix}(v)$, $K$-th element retrieved via binary lifting.

### Tier C — Transformations
10. **`fenwick_coordinate_compression`**:
    - *Description*: Coordinate compression pipeline over large or sparse coordinate spaces.
    - *Structural Invariant*: Sort and unique pipeline maps arbitrary comparable coordinates representable by the problem/input type ($\text{sort} \to \text{unique} \to \text{map to ranks } [1, M]$ where $M \le N$), enabling compact Fenwick tree allocation.

---

## 4. Candidate Elimination & Anti-Pattern Detection

Section 17 candidate elimination rules prevent misrouting and distinguish structural incompatibility from asymptotic preference:

1. `FENWICK_STATIC_QUERY_SUBOPTIMAL`:
   - *Classification*: Asymptotic preference, not correctness failure.
   - *Rule*: Static array range sum queries without updates are structurally valid on Fenwick trees, but static prefix sums are preferred because prefix sums achieve $O(1)$ query time versus Fenwick's $O(\log N)$.
2. `FENWICK_OFFLINE_RANGE_ADD_OVERKILL`:
   - *Classification*: Asymptotic preference, not correctness failure.
   - *Rule*: Batch range additions where queries only occur after all updates are complete are preferred on static difference arrays ($O(N)$ total reconstruction) rather than dynamic Fenwick range trees ($O(Q \log N)$).
3. `FENWICK_STRUCTURAL_INCOMPATIBILITY`:
   - *Classification*: Structural correctness failure.
   - *Rule*: Arbitrary range queries requiring inversion when no suitable inverse exists (e.g. dynamic range GCD), interval assignment/overwrite operations, or dynamic range minimum with arbitrary point replacements cannot be represented by Fenwick trees and are eliminated in favor of Segment Trees.
4. `FENWICK_DYNAMIC_COORDINATE_UNREPRESENTABLE`:
   - *Classification*: Structural correctness failure.
   - *Rule*: Ordinary fixed-index Fenwick is insufficient when dynamically appearing coordinates cannot be represented in a known index space. The replacement structure depends on required operations and may include an order-statistics tree, dynamic segment tree, balanced ordered structure, or another coordinate-aware rank structure.
5. `FENWICK_KTH_NEGATIVE_FREQUENCY`:
   - *Classification*: Invariant violation.
   - *Rule*: $K$-th element search where frequency updates can become negative invalidates the monotonic prefix sum invariant required for binary lifting. Eliminated in favor of structures supporting general dynamic rank operations under negative weights (e.g., Segment Tree or balanced ordered structure).
6. `FENWICK_RESOURCE_LIMIT`:
   - *Classification*: Resource constraint.
   - *Rule*: 2D Fenwick trees whose grid dimensions exceed memory budgets ($R \times C \times 8 > 64\text{MB}$) are eliminated.

---

## 5. C++17 Generator Verification

All generated C++17 implementations adhere to:
- **1-based Internal Indexing**: Clean `lowbit(i) = i & (-i)` loops. Zero-indexed user inputs are normalized at I/O boundaries.
- **Integer-Width Policy**: `long long` is used where the mathematical result is guaranteed to fit within signed 64-bit bounds. Intermediate products such as $(r + 1) \cdot \Delta$ or $j \cdot D[j]$ must also be checked against problem constraints; where constraints permit intermediate values beyond 64-bit, `__int128` must be used for products/accumulators.
- **Fast I/O**: `std::ios_base::sync_with_stdio(false); std::cin.tie(NULL);` included in every template.
- **Construction Complexity**:
  - Linear-Time $O(N)$ Build: Implemented in `fenwick_point_update_prefix_query` where initial array values propagate directly to `parent = i + lowbit(i)` in $O(N)$ time without $O(N \log N)$ repeated `add` calls.
  - Dynamic Initialization: Frequency, multiset, and 2D variants initialize empty structures in $O(M)$ or $O(R \times C)$ and apply dynamic updates.
