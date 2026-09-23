"""
CHUP Historical Milestone Regression Registry.

Aggregates and verifies all 19 historical algorithmic test suites from Phase 3A through Phase 3S:
1. Phase 3A: Two Pointers (13 tests) - pointer_algorithms/test_suite.py
2. Phase 3B: Binary Search (9 tests) - pointer_algorithms/binary_search/test_suite.py
3. Phase 3C: Monotonic Stack (8 tests) - pointer_algorithms/monotonic_stack/test_suite.py
4. Phase 3D: Trie (10 tests) - pointer_algorithms/trie/test_suite.py
5. Phase 3E: Tree (13 tests) - pointer_algorithms/tree/test_suite.py
6. Phase 3F: Graph (26 tests) - pointer_algorithms/graph/test_suite.py
7. Phase 3G: Heap (19 tests) - pointer_algorithms/heap/test_suite.py
8. Phase 3H: DSU (18 tests) - pointer_algorithms/dsu/test_suite.py
9. Phase 3I: Fenwick (14 tests) - pointer_algorithms/fenwick/test_suite.py
10. Phase 3J: Segment Tree (22 tests) - pointer_algorithms/segment_tree/test_suite.py
11. Phase 3K: DP (23 tests) - pointer_algorithms/dp/test_suite.py
12. Phase 3L: Greedy (22 tests) - pointer_algorithms/greedy/test_suite.py
13. Phase 3M: D&C / Backtracking (29 tests) - pointer_algorithms/dc_backtracking/test_suite.py
14. Phase 3N: Advanced Graph (26 tests) - pointer_algorithms/adv_graph/test_suite.py
15. Phase 3O: String Algorithms (26 tests) - pointer_algorithms/strings/test_suite.py
16. Phase 3P: Number Theory (26 tests) - pointer_algorithms/number_theory/test_suite.py
17. Phase 3Q: Algebra / Transforms (26 tests) - pointer_algorithms/algebra/test_suite.py
18. Phase 3R: Computational Geometry (26 tests) - pointer_algorithms/geometry/test_suite.py
19. Phase 3S: Advanced Data Structures (26 tests) - pointer_algorithms/adv_data_structures/test_suite.py

Total: 382 tests.
"""

import sys
import os
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

HISTORICAL_SUITES = [
    ("Phase 3A: Two Pointers", "pointer_algorithms.test_suite"),
    ("Phase 3B: Binary Search", "pointer_algorithms.binary_search.test_suite"),
    ("Phase 3C: Monotonic Stack", "pointer_algorithms.monotonic_stack.test_suite"),
    ("Phase 3D: Trie", "pointer_algorithms.trie.test_suite"),
    ("Phase 3E: Tree", "pointer_algorithms.tree.test_suite"),
    ("Phase 3F: Graph", "pointer_algorithms.graph.test_suite"),
    ("Phase 3G: Heap", "pointer_algorithms.heap.test_suite"),
    ("Phase 3H: DSU", "pointer_algorithms.dsu.test_suite"),
    ("Phase 3I: Fenwick", "pointer_algorithms.fenwick.test_suite"),
    ("Phase 3J: Segment Tree", "pointer_algorithms.segment_tree.test_suite"),
    ("Phase 3K: Dynamic Programming", "pointer_algorithms.dp.test_suite"),
    ("Phase 3L: Greedy", "pointer_algorithms.greedy.test_suite"),
    ("Phase 3M: D&C / Backtracking", "pointer_algorithms.dc_backtracking.test_suite"),
    ("Phase 3N: Advanced Graph", "pointer_algorithms.adv_graph.test_suite"),
    ("Phase 3O: String Algorithms", "pointer_algorithms.strings.test_suite"),
    ("Phase 3P: Number Theory", "pointer_algorithms.number_theory.test_suite"),
    ("Phase 3Q: Algebra / Transforms", "pointer_algorithms.algebra.test_suite"),
    ("Phase 3R: Computational Geometry", "pointer_algorithms.geometry.test_suite"),
    ("Phase 3S: Advanced Data Structures", "pointer_algorithms.adv_data_structures.test_suite"),
    ("Phase 4: Cross-Family Composition", "pointer_algorithms.cross_family.test_suite"),
]


def load_historical_suite() -> unittest.TestSuite:
    loader = unittest.defaultTestLoader
    master_suite = unittest.TestSuite()
    for name, module_name in HISTORICAL_SUITES:
        suite = loader.loadTestsFromName(module_name)
        master_suite.addTests(suite)
    return master_suite


def run_historical_regressions() -> bool:
    suite = load_historical_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print(f"\nHistorical Milestone Regressions Result: {result.testsRun} run, {len(result.failures)} failures, {len(result.errors)} errors")
    return result.wasSuccessful() and result.testsRun == 416


if __name__ == "__main__":
    success = run_historical_regressions()
    sys.exit(0 if success else 1)
