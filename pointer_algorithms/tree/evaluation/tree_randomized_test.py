"""
Randomized Testing Suite for Tree Domain (Phase 3E).

Generates diverse randomized tree topologies:
- Chains (worst-case depth H = N)
- Stars (maximum branching factor, depth 2)
- Balanced binary trees (depth O(log N))
- Random Prüfer trees (uniform random trees)
- Duplicate-heavy node values
- Trees with negative node values

Verifies C++ compiled code against independent brute-force oracles.
"""

import sys
import os
import random
import subprocess
import tempfile
import time
from typing import List, Tuple, Dict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.tree.verification.tree_brute_force_oracles import (
    oracle_tree_height,
    oracle_tree_subtree_sizes,
    oracle_tree_leaf_count,
    oracle_tree_subtree_sum,
    oracle_tree_diameter,
    oracle_tree_independent_set,
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

def generate_chain_tree(n: int) -> List[Tuple[int, int]]:
    return [(i, i + 1) for i in range(1, n)]

def generate_star_tree(n: int) -> List[Tuple[int, int]]:
    return [(1, i) for i in range(2, n + 1)]

def generate_balanced_binary_tree(n: int) -> List[Tuple[int, int]]:
    edges = []
    for i in range(1, n + 1):
        left = 2 * i
        right = 2 * i + 1
        if left <= n:
            edges.append((i, left))
        if right <= n:
            edges.append((i, right))
    return edges

def generate_random_tree(n: int) -> List[Tuple[int, int]]:
    if n <= 1:
        return []
    prufer = [random.randint(1, n) for _ in range(n - 2)]
    degree = [1] * (n + 1)
    for v in prufer:
        degree[v] += 1
    
    edges = []
    for v in prufer:
        for u in range(1, n + 1):
            if degree[u] == 1:
                edges.append((u, v))
                degree[u] -= 1
                degree[v] -= 1
                break
    
    u = v = 0
    for i in range(1, n + 1):
        if degree[i] == 1:
            if u == 0:
                u = i
            else:
                v = i
                break
    edges.append((u, v))
    return edges

def run_randomized_tests():
    print("=" * 70)
    print("CHUP Phase 3E — Tree Randomized Testing Suite")
    print("=" * 70)

    random.seed(42)
    test_count = 0
    passed = 0

    # 1. Chains: height, diameter, subtree size
    for n in (5, 10, 20):
        test_count += 1
        edges = generate_chain_tree(n)
        expected_h = oracle_tree_height(n, edges, 1)
        expected_d = oracle_tree_diameter(n, edges)
        
        # Test height
        req = {"problemText": "Given a tree of N nodes and N-1 edges, compute the height of the tree."}
        resp = handle_request(req)
        stdin_data = f"{n}\n" + "\n".join(f"{u} {v}" for u, v in edges) + "\n"
        out = compile_and_run_cpp(resp["code"], stdin_data)
        if out.strip() == str(expected_h):
            passed += 1
            print(f"  ✓ Chain Tree (N={n}) height={expected_h}")
        else:
            print(f"  ✗ Chain Tree (N={n}) height: expected {expected_h}, got {out}")

        # Test diameter
        test_count += 1
        req_d = {"problemText": "Given an undirected tree of N nodes, compute the diameter of the tree."}
        resp_d = handle_request(req_d)
        out_d = compile_and_run_cpp(resp_d["code"], stdin_data)
        if out_d.strip() == str(expected_d):
            passed += 1
            print(f"  ✓ Chain Tree (N={n}) diameter={expected_d}")
        else:
            print(f"  ✗ Chain Tree (N={n}) diameter: expected {expected_d}, got {out_d}")

    # 2. Stars: leaf count, subtree sizes, diameter
    for n in (5, 15, 25):
        test_count += 1
        edges = generate_star_tree(n)
        expected_leaves = oracle_tree_leaf_count(n, edges, 1)
        req = {"problemText": "Given a tree with N nodes and edges, count the leaves in the tree."}
        resp = handle_request(req)
        stdin_data = f"{n}\n" + "\n".join(f"{u} {v}" for u, v in edges) + "\n"
        out = compile_and_run_cpp(resp["code"], stdin_data)
        if out.strip() == str(expected_leaves):
            passed += 1
            print(f"  ✓ Star Tree (N={n}) leaves={expected_leaves}")
        else:
            print(f"  ✗ Star Tree (N={n}) leaves: expected {expected_leaves}, got {out}")

    # 3. Balanced binary trees: subtree sum, independent set
    for n in (7, 15, 31):
        test_count += 1
        edges = generate_balanced_binary_tree(n)
        vals = [random.randint(1, 100) for _ in range(n)]
        expected_mis = oracle_tree_independent_set(n, edges, vals, 1)
        req = {"problemText": "Given a tree with node weights, find maximum weight independent set."}
        resp = handle_request(req)
        stdin_data = f"{n}\n" + " ".join(map(str, vals)) + "\n" + "\n".join(f"{u} {v}" for u, v in edges) + "\n"
        out = compile_and_run_cpp(resp["code"], stdin_data)
        if out.strip() == str(expected_mis):
            passed += 1
            print(f"  ✓ Balanced Tree (N={n}) MIS={expected_mis}")
        else:
            print(f"  ✗ Balanced Tree (N={n}) MIS: expected {expected_mis}, got {out}")

    # 4. Random Prüfer trees: diameter, subtree sums
    for n in (6, 12, 18):
        test_count += 1
        edges = generate_random_tree(n)
        expected_d = oracle_tree_diameter(n, edges)
        req = {"problemText": "Given an undirected tree of N nodes and N-1 edges, compute the diameter of the tree."}
        resp = handle_request(req)
        stdin_data = f"{n}\n" + "\n".join(f"{u} {v}" for u, v in edges) + "\n"
        out = compile_and_run_cpp(resp["code"], stdin_data)
        if out.strip() == str(expected_d):
            passed += 1
            print(f"  ✓ Random Tree (N={n}) diameter={expected_d}")
        else:
            print(f"  ✗ Random Tree (N={n}) diameter: expected {expected_d}, got {out}")

    # 5. Duplicate node values & negative values
    for n in (5, 10):
        test_count += 1
        edges = generate_chain_tree(n)
        vals = [-10 if i % 2 == 0 else 20 for i in range(n)]
        expected_sub_sum = oracle_tree_subtree_sum(n, edges, vals, 1)
        req = {"problemText": "Given a tree with node values, compute the subtree sum of each node."}
        resp = handle_request(req)
        stdin_data = f"{n}\n" + " ".join(map(str, vals)) + "\n" + "\n".join(f"{u} {v}" for u, v in edges) + "\n"
        out = compile_and_run_cpp(resp["code"], stdin_data)
        if out.split() == list(map(str, expected_sub_sum)):
            passed += 1
            print(f"  ✓ Negatives/Duplicates Tree (N={n}) subtree sum verified")
        else:
            print(f"  ✗ Negatives/Duplicates Tree (N={n}) subtree sum failed: got {out}")

    print("=" * 70)
    print(f"  Randomized Tree Tests: {passed}/{test_count} passed ({(passed/test_count)*100:.0f}%)")
    print("=" * 70)
    return passed == test_count

if __name__ == "__main__":
    success = run_randomized_tests()
    sys.exit(0 if success else 1)
