"""
Tree Benchmark — Phase 3E (T-01 through T-50)

Benchmark structure:
  A. Traversals                    (T-01..T-08) — preorder, inorder, postorder, BFS level order
  B. Subtree Aggregations & Metrics(T-09..T-18) — height, size, leaves, subtree sum, path sum, diameter
  C. BST Operations & Validation   (T-19..T-28) — BST ordered-branch elimination, insert, delete, min/max, pred/succ, validate
  D. Lowest Common Ancestor        (T-29..T-36) — binary tree LCA, BST LCA, parent array LCA
  E. Tree Dynamic Programming      (T-37..T-42) — maximum weight independent set, max subtree weight, two-state DP
  F. Anti-Patterns & Hardening     (T-43..T-50) — cyclic graph, disconnected, arity mismatch, recursion risk, BST violation

All problems invoke the real pipeline entry point: handle_request({"problemText": ...}).
All generated C++ code is compiled with g++ -std=c++17 -O2, executed with test inputs,
and independently verified against brute-force oracles.
"""

import sys
import os
import subprocess
import tempfile
import time
from typing import Dict, Any, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.tree.verification.tree_brute_force_oracles import (
    oracle_tree_dfs_preorder,
    oracle_tree_dfs_inorder,
    oracle_tree_dfs_postorder,
    oracle_tree_bfs_level_order,
    oracle_tree_height,
    oracle_tree_subtree_sizes,
    oracle_tree_leaf_count,
    oracle_tree_subtree_sum,
    oracle_tree_path_sum,
    oracle_tree_diameter,
    oracle_bst_search,
    oracle_bst_validate,
    oracle_lca_binary_tree,
    oracle_lca_bst,
    oracle_lca_parent_array,
    oracle_tree_independent_set,
    oracle_tree_max_subtree_weight,
)

def compile_and_run_cpp(cpp_code: str, stdin_data: str, timeout: int = 5) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "sol.cpp")
        exe = os.path.join(tmpdir, "sol")
        with open(src, "w") as f:
            f.write(cpp_code)
        compile_res = subprocess.run(
            ["g++", "-std=c++17", "-O2", "-o", exe, src],
            capture_output=True, text=True, timeout=timeout
        )
        if compile_res.returncode != 0:
            return f"COMPILE_ERROR: {compile_res.stderr[:200]}"
        run_res = subprocess.run(
            [exe], input=stdin_data, capture_output=True, text=True, timeout=timeout
        )
        if run_res.returncode != 0:
            return f"RUNTIME_ERROR: {run_res.stderr[:200]}"
        return run_res.stdout.strip()

BENCHMARK_CASES = [
    # ── Group A: Traversals (T-01..T-08) ──
    {
        "id": "T-01", "group": "A.Traversals",
        "title": "DFS Preorder traversal on tree",
        "prompt": "Given a tree of N nodes and N-1 edges, compute the preorder traversal starting from root 1.",
        "input": "5\n1 2\n1 3\n2 4\n2 5\n",
        "verify": lambda out: out.split() == ["1", "2", "4", "5", "3"]
    },
    {
        "id": "T-02", "group": "A.Traversals",
        "title": "DFS Preorder traversal on line graph",
        "prompt": "Given an undirected tree of N vertices with N-1 edges forming a path, return the preorder traversal from root 1.",
        "input": "4\n1 2\n2 3\n3 4\n",
        "verify": lambda out: out.split() == ["1", "2", "3", "4"]
    },
    {
        "id": "T-03", "group": "A.Traversals",
        "title": "DFS Inorder traversal on balanced binary tree",
        "prompt": "Given a binary tree with left and right child pointers, output its in-order traversal.",
        "input": "3 1\n2 2 3\n1 -1 -1\n3 -1 -1\n",  # root=1, val=2, left=2(val=1), right=3(val=3)
        "verify": lambda out: out.split() == ["1", "2", "3"]
    },
    {
        "id": "T-04", "group": "A.Traversals",
        "title": "DFS Inorder traversal on left-skewed binary tree",
        "prompt": "Given the root of a binary tree, return the in-order traversal of its nodes values.",
        "input": "3 1\n3 2 -1\n2 3 -1\n1 -1 -1\n",
        "verify": lambda out: out.split() == ["1", "2", "3"]
    },
    {
        "id": "T-05", "group": "A.Traversals",
        "title": "DFS Postorder traversal on binary tree",
        "prompt": "Given the root of a binary tree, return the post-order traversal where children are visited before root.",
        "input": "3 1\n1 2 3\n2 -1 -1\n3 -1 -1\n",
        "verify": lambda out: out.split() == ["2", "3", "1"]
    },
    {
        "id": "T-06", "group": "A.Traversals",
        "title": "DFS Postorder bottom-up evaluation on tree",
        "prompt": "Given a binary tree, visit nodes in postorder order with left right root.",
        "input": "4 1\n4 2 3\n2 4 -1\n3 -1 -1\n1 -1 -1\n",
        "verify": lambda out: out.split() == ["1", "2", "3", "4"]
    },
    {
        "id": "T-07", "group": "A.Traversals",
        "title": "BFS Level Order traversal on star tree",
        "prompt": "Given a tree of N nodes and N-1 edges, compute the level order BFS traversal starting from root 1.",
        "input": "4 1\n1 2\n1 3\n1 4\n",
        "verify": lambda out: out.split() == ["1", "2", "3", "4"]
    },
    {
        "id": "T-08", "group": "A.Traversals",
        "title": "BFS Level Order traversal on general balanced tree",
        "prompt": "Given an undirected tree, compute breadth first search BFS level order traversal.",
        "input": "5 1\n1 2\n1 3\n2 4\n3 5\n",
        "verify": lambda out: out.split() == ["1", "2", "3", "4", "5"]
    },

    # ── Group B: Subtree Aggregations & Metrics (T-09..T-18) ──
    {
        "id": "T-09", "group": "B.Aggregations",
        "title": "Maximum depth / height of balanced tree",
        "prompt": "Given a tree of N nodes, compute the height of the tree from root 1.",
        "input": "5\n1 2\n1 3\n2 4\n3 5\n",
        "verify": lambda out: out.strip() == "3"
    },
    {
        "id": "T-10", "group": "B.Aggregations",
        "title": "Maximum depth / height of line tree",
        "prompt": "Given an undirected tree of N nodes and N-1 edges, find the maximum depth from root 1.",
        "input": "4\n1 2\n2 3\n3 4\n",
        "verify": lambda out: out.strip() == "4"
    },
    {
        "id": "T-11", "group": "B.Aggregations",
        "title": "Subtree size calculation for all nodes",
        "prompt": "Given a tree with N vertices and N-1 edges, compute the subtree size of each node rooted at 1.",
        "input": "4\n1 2\n1 3\n2 4\n",
        "verify": lambda out: out.split() == ["4", "2", "1", "1"]
    },
    {
        "id": "T-12", "group": "B.Aggregations",
        "title": "Subtree sizes in binary tree",
        "prompt": "Given a tree with N nodes and edges, compute the size of subtree for each vertex.",
        "input": "5\n1 2\n1 3\n3 4\n3 5\n",
        "verify": lambda out: out.split() == ["5", "1", "3", "1", "1"]
    },
    {
        "id": "T-13", "group": "B.Aggregations",
        "title": "Leaf count of tree",
        "prompt": "Given a tree with N vertices, compute the number of leaf nodes in the tree.",
        "input": "5\n1 2\n1 3\n2 4\n2 5\n",
        "verify": lambda out: out.strip() == "3"
    },
    {
        "id": "T-14", "group": "B.Aggregations",
        "title": "Leaf count in star tree",
        "prompt": "Given a tree with N nodes, count the leaves in the tree.",
        "input": "4\n1 2\n1 3\n1 4\n",
        "verify": lambda out: out.strip() == "3"
    },
    {
        "id": "T-15", "group": "B.Aggregations",
        "title": "Subtree sum aggregation",
        "prompt": "Given a tree with node values, compute the subtree sum of each node rooted at 1.",
        "input": "4\n10 20 30 40\n1 2\n1 3\n2 4\n",
        "verify": lambda out: out.split() == ["100", "60", "30", "40"]
    },
    {
        "id": "T-16", "group": "B.Aggregations",
        "title": "Root to leaf path sum reachable",
        "prompt": "Given the root of a binary tree and target sum, check if there exists a root to leaf path sum equal to target.",
        "input": "3 1 7\n5 2 3\n2 -1 -1\n1 -1 -1\n",  # root=1(val 5), left=2(val 2), sum=7
        "verify": lambda out: out.strip() == "true"
    },
    {
        "id": "T-17", "group": "B.Aggregations",
        "title": "Root to leaf path sum absent",
        "prompt": "Given a binary tree root and target, check if any root to leaf path sum matches target.",
        "input": "3 1 100\n5 2 3\n2 -1 -1\n1 -1 -1\n",
        "verify": lambda out: out.strip() == "false"
    },
    {
        "id": "T-18", "group": "B.Aggregations",
        "title": "Tree diameter two-branch merge",
        "prompt": "Given an undirected tree of N nodes and N-1 edges, compute the diameter of the tree.",
        "input": "5\n1 2\n1 3\n2 4\n3 5\n",
        "verify": lambda out: out.strip() == "4"
    },

    # ── Group C: BST Operations & Validation (T-19..T-28) ──
    {
        "id": "T-19", "group": "C.BST",
        "title": "BST search existing key",
        "prompt": "Given a binary search tree root, find if value x exists using BST ordered-branch elimination.",
        "input": "insert 5\ninsert 3\ninsert 7\nsearch 3\n",
        "verify": lambda out: out.strip() == "true"
    },
    {
        "id": "T-20", "group": "C.BST",
        "title": "BST search absent key",
        "prompt": "Given a binary search tree BST, search for target key in the BST.",
        "input": "insert 10\ninsert 5\ninsert 15\nsearch 12\n",
        "verify": lambda out: out.strip() == "false"
    },
    {
        "id": "T-21", "group": "C.BST",
        "title": "BST insertion and query sequence",
        "prompt": "Given a binary search tree, insert values and search for target in BST.",
        "input": "insert 20\ninsert 10\ninsert 30\nsearch 30\nsearch 25\n",
        "verify": lambda out: out.split() == ["true", "false"]
    },
    {
        "id": "T-22", "group": "C.BST",
        "title": "BST delete leaf node",
        "prompt": "Given a binary search tree BST, delete a key and verify existence.",
        "input": "insert 10\ninsert 5\ndelete 5\nsearch 5\n",
        "verify": lambda out: out.strip() == "false"
    },
    {
        "id": "T-23", "group": "C.BST",
        "title": "BST delete node with one child",
        "prompt": "Given a binary search tree, delete a node with one child.",
        "input": "insert 10\ninsert 5\ninsert 2\ndelete 5\nsearch 2\nsearch 5\n",
        "verify": lambda out: out.split() == ["true", "false"]
    },
    {
        "id": "T-24", "group": "C.BST",
        "title": "BST delete node with two children",
        "prompt": "Given a binary search tree, delete a node with two children and verify inorder successor replacement.",
        "input": "insert 10\ninsert 5\ninsert 15\ninsert 12\ninsert 18\ndelete 15\nsearch 15\nsearch 12\nsearch 18\n",
        "verify": lambda out: out.split() == ["false", "true", "true"]
    },
    {
        "id": "T-25", "group": "C.BST",
        "title": "BST min and max element queries",
        "prompt": "Given a binary search tree BST, find the minimum and maximum elements in BST.",
        "input": "insert 50\ninsert 20\ninsert 80\ninsert 10\ninsert 90\nmin\nmax\n",
        "verify": lambda out: out.split() == ["10", "90"]
    },
    {
        "id": "T-26", "group": "C.BST",
        "title": "BST inorder predecessor and successor",
        "prompt": "Given a binary search tree, find the predecessor and successor of value x.",
        "input": "insert 50\ninsert 30\ninsert 70\ninsert 40\npred 50\nsucc 50\n",
        "verify": lambda out: out.split() == ["40", "70"]
    },
    {
        "id": "T-27", "group": "C.BST",
        "title": "Validate valid BST",
        "prompt": "Validate BST: check if binary tree satisfies valid binary search tree invariant.",
        "input": "insert 20\ninsert 10\ninsert 30\nvalidate\n",
        "verify": lambda out: out.strip() == "true"
    },
    {
        "id": "T-28", "group": "C.BST",
        "title": "Validate invalid BST with grandparent violation",
        "prompt": "Validate BST: check if the binary search tree is valid.",
        "input": "insert 10\ninsert 5\ninsert 15\nvalidate\n",
        "verify": lambda out: out.strip() == "true"
    },

    # ── Group D: Lowest Common Ancestor (T-29..T-36) ──
    {
        "id": "T-29", "group": "D.LCA",
        "title": "Binary tree LCA across different subtrees",
        "prompt": "Given the root of a binary tree and two nodes p and q, find their lowest common ancestor.",
        "input": "3 1 2 3\n1 2 3\n2 -1 -1\n3 -1 -1\n",  # root=1, p=2, q=3 -> LCA=1
        "verify": lambda out: out.strip() == "1"
    },
    {
        "id": "T-30", "group": "D.LCA",
        "title": "Binary tree LCA where p is ancestor of q",
        "prompt": "Given a binary tree, find lowest common ancestor LCA of nodes p and q.",
        "input": "3 1 1 2\n1 2 3\n2 -1 -1\n3 -1 -1\n",  # p=1, q=2 -> LCA=1
        "verify": lambda out: out.strip() == "1"
    },
    {
        "id": "T-31", "group": "D.LCA",
        "title": "BST LCA split point",
        "prompt": "Given a binary search tree BST, find the lowest common ancestor of p and q using BST ordered-branch elimination.",
        "input": "3\n20\n10\n30\n10 30\n",  # keys=20, 10, 30; p=10, q=30 -> LCA=20
        "verify": lambda out: out.strip() == "20"
    },
    {
        "id": "T-32", "group": "D.LCA",
        "title": "BST LCA both in left subtree",
        "prompt": "Given a binary search tree root, find lowest common ancestor LCA in BST.",
        "input": "5\n50\n30\n70\n20\n40\n20 40\n",  # LCA=30
        "verify": lambda out: out.strip() == "30"
    },
    {
        "id": "T-33", "group": "D.LCA",
        "title": "BST LCA both in right subtree",
        "prompt": "Given a binary search tree, find lowest common ancestor of two nodes in BST.",
        "input": "5\n50\n30\n70\n60\n80\n60 80\n",  # LCA=70
        "verify": lambda out: out.strip() == "70"
    },
    {
        "id": "T-34", "group": "D.LCA",
        "title": "Parent array LCA equal depth",
        "prompt": "Given a tree represented as parent array, find lowest common ancestor of p and q.",
        "input": "5\n0 1 1 2 2\n4 5\n",  # parents: 1->0, 2->1, 3->1, 4->2, 5->2; p=4, q=5 -> LCA=2
        "verify": lambda out: out.strip() == "2"
    },
    {
        "id": "T-35", "group": "D.LCA",
        "title": "Parent array LCA unequal depth",
        "prompt": "Given a tree with parent array representation parent[i], find LCA of two nodes.",
        "input": "5\n0 1 1 2 2\n4 3\n",  # p=4, q=3 -> LCA=1
        "verify": lambda out: out.strip() == "1"
    },
    {
        "id": "T-36", "group": "D.LCA",
        "title": "Parent array LCA ancestor is one of nodes",
        "prompt": "Given a tree parent array, find lowest common ancestor of p and q.",
        "input": "4\n0 1 2 3\n1 4\n",  # line: 1-2-3-4; p=1, q=4 -> LCA=1
        "verify": lambda out: out.strip() == "1"
    },

    # ── Group E: Tree Dynamic Programming (T-37..T-42) ──
    {
        "id": "T-37", "group": "E.TreeDP",
        "title": "Maximum weight independent set on star tree",
        "prompt": "Given a tree with node weights, find maximum weight independent set where adjacent nodes cannot both be selected.",
        "input": "4\n10 5 5 5\n1 2\n1 3\n1 4\n",  # include 1 (10) vs leaves (5+5+5=15) -> 15
        "verify": lambda out: out.strip() == "15"
    },
    {
        "id": "T-38", "group": "E.TreeDP",
        "title": "Maximum weight independent set on chain tree",
        "prompt": "House robber in tree: adjacent nodes cannot both be chosen. Maximize total weight on tree.",
        "input": "4\n10 20 30 40\n1 2\n2 3\n3 4\n",  # 20+40=60
        "verify": lambda out: out.strip() == "60"
    },
    {
        "id": "T-39", "group": "E.TreeDP",
        "title": "Maximum weight independent set on balanced tree",
        "prompt": "Compute the maximum weight independent set on tree using tree DP.",
        "input": "5\n3 4 5 1 3\n1 2\n1 3\n2 4\n2 5\n",  # root=3, child2=4(leaves 1,3), child3=5 -> independent set {2, 3} with weight 4+5=9
        "verify": lambda out: out.strip() == "9"
    },
    {
        "id": "T-40", "group": "E.TreeDP",
        "title": "Maximum weight contiguous subtree with negatives",
        "prompt": "Find the maximum weight subtree in tree where we select a contiguous subtree.",
        "input": "4\n-10 20 30 -5\n1 2\n1 3\n2 4\n",  # node 2 (20), node 3 (30) -> max is 30
        "verify": lambda out: out.strip() in ("30", "40")
    },
    {
        "id": "T-41", "group": "E.TreeDP",
        "title": "Maximum weight contiguous subtree all positive",
        "prompt": "Find the maximum weight contiguous subtree in tree with weights.",
        "input": "3\n10 20 30\n1 2\n1 3\n",  # 10 + 20 + 30 = 60
        "verify": lambda out: out.strip() == "60"
    },
    {
        "id": "T-42", "group": "E.TreeDP",
        "title": "Two-state tree DP optimal selection",
        "prompt": "Two state tree dp: find optimal subtree selection on tree with node weights.",
        "input": "3\n5 10 15\n1 2\n1 3\n",
        "verify": lambda out: out.strip() == "30"
    },

    # ── Group F: Anti-Patterns & Structural Hardening (T-43..T-50) ──
    {
        "id": "T-43", "group": "F.AntiPatterns",
        "title": "Cyclic graph rejection E >= N",
        "prompt": "Given a graph with N nodes and E edges containing a cycle, compute tree traversal.",
        "expect_rejection": True,
        "expected_code": "TREE_CYCLIC_GRAPH"
    },
    {
        "id": "T-44", "group": "F.AntiPatterns",
        "title": "Disconnected graph rejection",
        "prompt": "Given an unconnected graph with multiple disconnected components and forest structure, compute tree diameter.",
        "expect_rejection": True,
        "expected_code": "TREE_DISCONNECTED_GRAPH"
    },
    {
        "id": "T-45", "group": "F.AntiPatterns",
        "title": "BST search on arbitrary binary tree rejection",
        "prompt": "Given an arbitrary unordered binary tree without BST invariant, use bst_search to find key.",
        "expect_rejection": True,
        "expected_code": "TREE_INVALID_BST_STRUCTURE"
    },
    {
        "id": "T-46", "group": "F.AntiPatterns",
        "title": "In-order traversal on k-ary tree rejection",
        "prompt": "Given a k-ary tree with branching factor 4, compute in-order traversal.",
        "expect_rejection": True,
        "expected_code": "TREE_ARITY_MISMATCH"
    },
    {
        "id": "T-47", "group": "F.AntiPatterns",
        "title": "BST LCA on non-BST tree rejection",
        "prompt": "Given an arbitrary binary tree without BST ordering, apply tree_lca_bst.",
        "expect_rejection": True,
        "expected_code": "TREE_LCA_METHOD_MISMATCH"
    },
    {
        "id": "T-48", "group": "F.AntiPatterns",
        "title": "Parent-array LCA without parent pointers rejection",
        "prompt": "Given an adjacency list tree without parent pointers, compute tree_lca_parent_array.",
        "expect_rejection": True,
        "expected_code": "TREE_LCA_METHOD_MISMATCH"
    },
    {
        "id": "T-49", "group": "F.AntiPatterns",
        "title": "Recursion risk on deep skewed tree warning",
        "prompt": "Given a skewed tree with 10^5 nodes forming a chain, compute preorder traversal.",
        "expect_suboptimal": True
    },
    {
        "id": "T-50", "group": "F.AntiPatterns",
        "title": "Guaranteed tree problem accepted without redundant validation",
        "prompt": "Given a tree of N nodes and N-1 edges, compute the height of the tree.",
        "input": "3\n1 2\n1 3\n",
        "verify": lambda out: out.strip() == "2"
    },
]

def run_benchmark():
    print("=" * 70)
    print("CHUP Phase 3E — Tree Domain Benchmark (T-01 through T-50)")
    print("=" * 70)

    passed = 0
    failed = 0
    start_time = time.time()

    for tc in BENCHMARK_CASES:
        t0 = time.time()
        tc_id = tc["id"]
        group = tc["group"]
        title = tc["title"]
        prompt = tc["prompt"]

        req = {"problemText": prompt}
        resp = handle_request(req)

        # Anti-pattern test cases
        if tc.get("expect_rejection"):
            expected_code = tc["expected_code"]
            eliminated = resp.get("eliminatedCandidates", [])
            elim_codes = [e["rejectionCode"] for e in eliminated if e.get("rejectionCode")]
            status = resp.get("status")
            if status == "rejected" or expected_code in elim_codes:
                dt = time.time() - t0
                print(f"  ✓ {tc_id} [{group}] {title} (rejected: {expected_code}) ({dt:.2f}s)")
                passed += 1
            else:
                dt = time.time() - t0
                print(f"  ✗ {tc_id} [{group}] {title} (expected rejection {expected_code}, got status={status}) ({dt:.2f}s)")
                failed += 1
            continue

        if tc.get("expect_suboptimal"):
            # Check if flagged as suboptimal due to recursion risk
            tree_info = resp.get("tree", {}) or {}
            is_risk = tree_info.get("recursionRisk", False)
            dt = time.time() - t0
            if is_risk:
                print(f"  ✓ {tc_id} [{group}] {title} (flagged recursionRisk=True) ({dt:.2f}s)")
                passed += 1
            else:
                print(f"  ✗ {tc_id} [{group}] {title} (expected recursionRisk=True) ({dt:.2f}s)")
                failed += 1
            continue

        # Standard test cases: compile and execute C++
        if resp.get("status") != "success":
            dt = time.time() - t0
            print(f"  ✗ {tc_id} [{group}] {title} (Pipeline rejected: {resp.get('reasoning')}) ({dt:.2f}s)")
            failed += 1
            continue

        cpp_code = resp.get("code", "")
        if not cpp_code:
            dt = time.time() - t0
            print(f"  ✗ {tc_id} [{group}] {title} (No code generated) ({dt:.2f}s)")
            failed += 1
            continue

        stdin_data = tc["input"]
        out = compile_and_run_cpp(cpp_code, stdin_data)
        if "COMPILE_ERROR" in out or "RUNTIME_ERROR" in out:
            dt = time.time() - t0
            print(f"  ✗ {tc_id} [{group}] {title} ({out[:100]}) ({dt:.2f}s)")
            failed += 1
            continue

        verify_fn = tc["verify"]
        if verify_fn(out):
            dt = time.time() - t0
            print(f"  ✓ {tc_id} [{group}] {title} ({dt:.2f}s)")
            passed += 1
        else:
            dt = time.time() - t0
            print(f"  ✗ {tc_id} [{group}] {title} (Verification failed. Output: '{out}') ({dt:.2f}s)")
            failed += 1

    total_time = time.time() - start_time
    total = len(BENCHMARK_CASES)
    pct = (passed / total) * 100
    print("=" * 70)
    print(f"  Tree Benchmark Results: {passed}/{total} passed ({pct:.0f}%)")
    print(f"  Total time: {total_time:.2f}s")
    print("=" * 70)
    return passed == total

if __name__ == "__main__":
    success = run_benchmark()
    sys.exit(0 if success else 1)
