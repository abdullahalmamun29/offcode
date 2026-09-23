"""
Tree Blind Holdout Suite — Phase 3E (BH-01 through BH-12)

Evaluates domain reasoning on disguised, domain-transferred problem statements
that omit explicit textbook terminology ("tree", "bst", "traversal", "dfs", "bfs").

Problems:
- BH-01: Corporate hierarchy compensation sum (Subtree sum)
- BH-02: Organization line of command report (Preorder traversal)
- BH-03: Dependency deallocation teardown order (Postorder traversal)
- BH-04: Network broadcast hop levels (BFS level order)
- BH-05: Critical network backbone span (Tree diameter)
- BH-06: Non-conflicting departmental grant allocation (Independent set)
- BH-07: Version control branch fork divergence (LCA parent array)
- BH-08: Tax bracket bracket lookup (BST search via ordered-branch elimination)
- BH-09: Financial audit boundary hierarchy check (BST validate)
- BH-10: Redundant pipeline cycle check (Cycle rejection)
- BH-11: Substation islanding forest check (Disconnected rejection)
- BH-12: Signal transmission path power check (Path sum)
"""

import sys
import os
import subprocess
import tempfile
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from pointer_algorithms.bridge import handle_request

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

BLIND_HOLDOUT_CASES = [
    {
        "id": "BH-01",
        "title": "Corporate hierarchy compensation sum",
        "prompt": "An organization has N employees structured hierarchically where employee 1 is CEO. Given each employee salary and supervisor connections without cycles, compute the total subtree sum of compensation under each manager.",
        "input": "4\n10 20 30 40\n1 2\n1 3\n2 4\n",
        "verify": lambda out: out.split() == ["100", "60", "30", "40"]
    },
    {
        "id": "BH-02",
        "title": "Organization line of command report",
        "prompt": "A military brigade is structured hierarchically. Starting from commanding general root 1, emit every personnel node visiting superiors before their respective child subtrees in preorder sequence.",
        "input": "4\n1 2\n1 3\n2 4\n",
        "verify": lambda out: out.split() == ["1", "2", "4", "3"]
    },
    {
        "id": "BH-03",
        "title": "Dependency deallocation teardown order",
        "prompt": "Software objects are allocated in a binary tree hierarchy. Clean up resources in safe teardown order: child subtrees must be deallocated completely before parent root.",
        "input": "3 1\n1 2 3\n2 -1 -1\n3 -1 -1\n",
        "verify": lambda out: out.split() == ["2", "3", "1"]
    },
    {
        "id": "BH-04",
        "title": "Network broadcast hop levels",
        "prompt": "A sensor broadcast network propagates signals outwards from root gateway 1. Group sensor nodes level by level using breadth first search BFS level order.",
        "input": "4 1\n1 2\n1 3\n1 4\n",
        "verify": lambda out: out.split() == ["1", "2", "3", "4"]
    },
    {
        "id": "BH-05",
        "title": "Critical network backbone span",
        "prompt": "A fiber optic tree connects N communications stations without loops. Find the longest path between any two nodes in the tree.",
        "input": "5\n1 2\n1 3\n2 4\n3 5\n",
        "verify": lambda out: out.strip() == "4"
    },
    {
        "id": "BH-06",
        "title": "Non-conflicting departmental grant allocation",
        "prompt": "A university tree has funding requests at each department node. Because adjacent nodes conflict, adjacent nodes cannot both be selected. Maximize total funding using independent set.",
        "input": "4\n10 5 5 5\n1 2\n1 3\n1 4\n",
        "verify": lambda out: out.strip() == "15"
    },
    {
        "id": "BH-07",
        "title": "Version control branch fork divergence",
        "prompt": "A version control graph stores commit revisions with parent array representation parent[i]. Given commits p and q, locate their lowest common ancestor commit.",
        "input": "5\n0 1 1 2 2\n4 5\n",
        "verify": lambda out: out.strip() == "2"
    },
    {
        "id": "BH-08",
        "title": "Tax bracket classification search",
        "prompt": "A financial database stores indexed tax thresholds in a binary search tree BST. Search for target threshold value using BST ordered-branch elimination.",
        "input": "insert 50\ninsert 25\ninsert 75\nsearch 25\nsearch 60\n",
        "verify": lambda out: out.split() == ["true", "false"]
    },
    {
        "id": "BH-09",
        "title": "Financial audit boundary hierarchy check",
        "prompt": "Validate BST: verify whether accounting tree nodes strictly observe valid binary search tree bounded intervals.",
        "input": "insert 100\ninsert 50\ninsert 150\nvalidate\n",
        "verify": lambda out: out.strip() == "true"
    },
    {
        "id": "BH-10",
        "title": "Redundant pipeline cycle check",
        "prompt": "Water pipeline network has N junctions with redundant loop connection where E >= N, creating a cycle. Compute tree traversal.",
        "expect_rejection": True,
        "expected_code": "TREE_CYCLIC_GRAPH"
    },
    {
        "id": "BH-11",
        "title": "Substation islanding forest check",
        "prompt": "Power grid network was split into disconnected components forming an isolated forest where E < N - 1. Compute tree diameter.",
        "expect_rejection": True,
        "expected_code": "TREE_DISCONNECTED_GRAPH"
    },
    {
        "id": "BH-12",
        "title": "Signal transmission path power check",
        "prompt": "An optical relay network has binary node splits. Determine if there is a root to leaf path sum equal to target power budget.",
        "input": "3 1 15\n10 2 3\n5 -1 -1\n2 -1 -1\n",
        "verify": lambda out: out.strip() == "true"
    },
]

def run_blind_holdouts():
    print("=" * 70)
    print("CHUP Phase 3E — Tree Blind Holdout Evaluation (BH-01..BH-12)")
    print("=" * 70)

    passed = 0
    failed = 0
    start_time = time.time()

    for tc in BLIND_HOLDOUT_CASES:
        t0 = time.time()
        tc_id = tc["id"]
        title = tc["title"]
        prompt = tc["prompt"]

        req = {"problemText": prompt}
        resp = handle_request(req)

        if tc.get("expect_rejection"):
            expected_code = tc["expected_code"]
            eliminated = resp.get("eliminatedCandidates", [])
            elim_codes = [e["rejectionCode"] for e in eliminated if e.get("rejectionCode")]
            status = resp.get("status")
            if status == "rejected" or expected_code in elim_codes:
                dt = time.time() - t0
                print(f"  ✓ {tc_id} {title} (rejected: {expected_code}) ({dt:.2f}s)")
                passed += 1
            else:
                dt = time.time() - t0
                print(f"  ✗ {tc_id} {title} (expected rejection {expected_code}) ({dt:.2f}s)")
                failed += 1
            continue

        if resp.get("status") != "success":
            dt = time.time() - t0
            print(f"  ✗ {tc_id} {title} (Rejected: {resp.get('reasoning')}) ({dt:.2f}s)")
            failed += 1
            continue

        cpp_code = resp.get("code", "")
        stdin_data = tc["input"]
        out = compile_and_run_cpp(cpp_code, stdin_data)
        if "COMPILE_ERROR" in out or "RUNTIME_ERROR" in out:
            dt = time.time() - t0
            print(f"  ✗ {tc_id} {title} ({out[:100]}) ({dt:.2f}s)")
            failed += 1
            continue

        verify_fn = tc["verify"]
        if verify_fn(out):
            dt = time.time() - t0
            print(f"  ✓ {tc_id} {title} ({dt:.2f}s)")
            passed += 1
        else:
            dt = time.time() - t0
            print(f"  ✗ {tc_id} {title} (Verification failed. Output: '{out}') ({dt:.2f}s)")
            failed += 1

    total_time = time.time() - start_time
    total = len(BLIND_HOLDOUT_CASES)
    pct = (passed / total) * 100
    print("=" * 70)
    print(f"  Tree Blind Holdout Results: {passed}/{total} passed ({pct:.0f}%)")
    print(f"  Total time: {total_time:.2f}s")
    print("=" * 70)
    return passed == total

if __name__ == "__main__":
    success = run_blind_holdouts()
    sys.exit(0 if success else 1)
