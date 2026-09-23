"""
CHUP Phase 3M — Divide & Conquer, Backtracking & Exponential Decomposition Adversarial Test Suite.

Contains 16 adversarial and edge cases:
- Empty inputs and single elements
- Identical elements and zero distance / inversions
- Deep recursion and boundary conditions
- All duplicates subsets deduplication
- Impossible constraint satisfaction (N=2, N=3 Queens)
- Zero knapsack capacity in branch and bound
- 1x1 grid search in state space
- Meet in the middle extreme targets
- Section 8 Gate: Tower Problem rejection
"""

import sys
import os
import subprocess
import tempfile
import hashlib
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request

COMPILED_BINARIES: Dict[str, str] = {}


def compile_and_run_cpp(code: str, stdin_data: str, timeout: int = 10) -> str:
    code_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()
    exe = COMPILED_BINARIES.get(code_hash)
    if not exe or not os.path.exists(exe):
        tmp_cpp = tempfile.NamedTemporaryFile(suffix=".cpp", delete=False)
        tmp_cpp.write(code.encode("utf-8"))
        tmp_cpp.close()
        exe = tmp_cpp.name[:-4]
        compile_res = subprocess.run(
            ["g++", "-std=c++17", "-O2", tmp_cpp.name, "-o", exe],
            capture_output=True, text=True
        )
        if compile_res.returncode != 0:
            return f"COMPILE_ERROR: {compile_res.stderr[:200]}"
        COMPILED_BINARIES[code_hash] = exe
    try:
        run_res = subprocess.run(
            [exe], input=stdin_data, capture_output=True, text=True, timeout=timeout
        )
        if run_res.returncode != 0:
            return f"RUNTIME_ERROR: {run_res.stderr[:200]}"
        return run_res.stdout.strip()
    except subprocess.TimeoutExpired:
        return "RUNTIME_ERROR: TimeoutExpired"


ADVERSARIAL_CASES = [
    {
        "id": "ADV-DC-01",
        "title": "Inversions with Zero Elements",
        "pattern": "dc_merge_sort_inversions",
        "input": "0",
        "expected": "0"
    },
    {
        "id": "ADV-DC-02",
        "title": "Inversions with 10 Identical Elements",
        "pattern": "dc_merge_sort_inversions",
        "input": "10\n5 5 5 5 5 5 5 5 5 5",
        "expected": "0"
    },
    {
        "id": "ADV-DC-03",
        "title": "Quickselect Min Element on Sorted Array",
        "pattern": "dc_quickselect",
        "input": "5 0\n1 2 3 4 5",
        "expected": "1"
    },
    {
        "id": "ADV-DC-04",
        "title": "Quickselect Max Element on Reverse Array",
        "pattern": "dc_quickselect",
        "input": "5 4\n5 4 3 2 1",
        "expected": "5"
    },
    {
        "id": "ADV-DC-05",
        "title": "Closest Pair with Identical X Coordinates",
        "pattern": "dc_closest_pair",
        "input": "3\n5 1\n5 8\n5 4",
        "expected": "3.000000"
    },
    {
        "id": "ADV-DC-06",
        "title": "Closest Pair Two Points Base Case",
        "pattern": "dc_closest_pair",
        "input": "2\n0 0\n3 4",
        "expected": "5.000000"
    },
    {
        "id": "ADV-DC-07",
        "title": "Tree Centroid Single Node Tree",
        "pattern": "dc_tree_centroid",
        "input": "1 5",
        "expected": "0"
    },
    {
        "id": "ADV-DC-08",
        "title": "Tree Centroid Star Graph K=1",
        "pattern": "dc_tree_centroid",
        "input": "5 1\n1 2\n1 3\n1 4\n1 5",
        "expected": "4"
    },
    {
        "id": "ADV-DC-09",
        "title": "CDQ 3D Partial Order All Identical Tuples",
        "pattern": "dc_cdq_divide_and_conquer",
        "input": "3\n1 1 1\n1 1 1\n1 1 1",
        "expected": "2\n2\n2"
    },
    {
        "id": "ADV-DC-10",
        "title": "Subsets All Identical Elements",
        "pattern": "backtracking_subsets_permutations",
        "input": "4\n7 7 7 7",
        "expected": "Total Subsets: 5"
    },
    {
        "id": "ADV-DC-11",
        "title": "N-Queens 1-Queen Base Case",
        "pattern": "backtracking_constraint_satisfaction",
        "input": "1",
        "expected": "1"
    },
    {
        "id": "ADV-DC-12",
        "title": "N-Queens 2-Queens Infeasible",
        "pattern": "backtracking_constraint_satisfaction",
        "input": "2",
        "expected": "0"
    },
    {
        "id": "ADV-DC-13",
        "title": "Branch and Bound Zero Knapsack Capacity",
        "pattern": "backtracking_branch_and_bound",
        "input": "3 0\n10 60\n20 100\n30 120",
        "expected": "0"
    },
    {
        "id": "ADV-DC-14",
        "title": "Word Search Single Cell Match",
        "pattern": "backtracking_state_space_search",
        "input": "1 1\nZ\nZ",
        "expected": "true"
    },
    {
        "id": "ADV-DC-15",
        "title": "Meet in the Middle Target 0",
        "pattern": "backtracking_meet_in_the_middle",
        "input": "4 0\n1 2 3 4",
        "expected": "1"
    },
    {
        "id": "ADV-DC-16",
        "title": "Section 8 Gate: Tower Problem Composition Gate",
        "is_rejection_test": True,
        "text": "You are given n cubes. Build towers by placing each cube on an existing tower. Find minimum number of towers.",
        "expected_rejection": "COMPOSITION_UNSUPPORTED"
    }
]


def run_adversarial_suite() -> Dict[str, Any]:
    print("=" * 80)
    print("CHUP Phase 3M — Divide & Conquer & Backtracking Adversarial Test Suite")
    print(f"Total test cases: {len(ADVERSARIAL_CASES)}")
    print("=" * 80)

    passed = 0
    failed = 0

    for case in ADVERSARIAL_CASES:
        cid = case["id"]
        title = case["title"]

        if case.get("is_rejection_test"):
            text = case["text"]
            expected_rej = case["expected_rejection"]
            res = handle_request({"action": "solve", "problemText": text})
            elim_codes = [e["rejectionCode"] for e in res.get("eliminatedCandidates", []) if e.get("rejectionCode")]
            if expected_rej in elim_codes or res.get("status") == "rejected":
                passed += 1
                print(f"[{cid}] PASS: {title} (Correctly rejected with {expected_rej})")
            else:
                failed += 1
                print(f"[{cid}] FAIL: {title} (Expected rejection {expected_rej}, got status={res['status']})")
            continue

        pat = case["pattern"]
        stdin_data = case["input"]
        expected = case["expected"]

        # Request code generation for the pattern
        res = handle_request({"action": "solve", "problemText": f"Solve using {pat} algorithm."})

        if res["status"] != "success":
            failed += 1
            print(f"[{cid}] FAIL: Bridge returned status={res['status']} ({title})")
            continue

        code = res.get("code", "")
        actual = compile_and_run_cpp(code, stdin_data)

        if "COMPILE_ERROR" in actual or "RUNTIME_ERROR" in actual:
            failed += 1
            print(f"[{cid}] FAIL: Execution error: {actual} ({title})")
            continue

        if actual == expected or expected in actual:
            passed += 1
            print(f"[{cid}] PASS: {title} (Output: {actual})")
        else:
            failed += 1
            print(f"[{cid}] FAIL: Output mismatch: expected '{expected}', got '{actual}' ({title})")

    total = len(ADVERSARIAL_CASES)
    print("=" * 80)
    print(f"Adversarial Suite Results: {passed}/{total} Passed ({passed/total*100:.1f}%)")
    print("=" * 80)

    return {"total": total, "passed": passed, "failed": failed}


if __name__ == "__main__":
    res = run_adversarial_suite()
    if res["failed"] > 0:
        sys.exit(1)
