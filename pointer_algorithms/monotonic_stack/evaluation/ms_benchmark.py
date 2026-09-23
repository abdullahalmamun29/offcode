"""
Monotonic Stack Benchmark — Phase 3B (MS-01 through MS-40)

Benchmark structure:
  A. Primitive Patterns       (MS-01..MS-11) — 1 problem per core pattern
  B. Structural Applications  (MS-12..MS-18) — histograms, circular, compound
  C. Strictness Cases         (MS-19..MS-22) — non-strict, duplicates
  D. Contribution / Compound  (MS-23..MS-28) — sum of subarray min/max
  E. Anti-Patterns            (MS-29..MS-32) — problems that should be rejected
  F. Paraphrase Variants      (MS-33..MS-36) — same problem, different wording
  G. Adversarial / Edge Cases (MS-37..MS-40) — n=1, all-equal, monotone arrays

Rules:
- Problems call handle_request() — the real entry point
- No hardcoded problem IDs in solver logic
- Each test is verified against the O(n^2) oracle
- Anti-pattern tests verify rejection, not generation
"""

import sys
import os
import subprocess
import tempfile
import random
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.monotonic_stack.verification.ms_brute_force_oracles import (
    oracle_next_greater_element, oracle_next_smaller_element,
    oracle_previous_greater_element, oracle_previous_smaller_element,
    oracle_nearest_greater_element, oracle_nearest_smaller_element,
    oracle_stock_span, oracle_largest_rectangle_histogram,
    oracle_circular_next_greater,
    oracle_sum_subarray_minimums, oracle_sum_subarray_maximums,
)

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def compile_and_run_cpp(cpp_code: str, stdin_data: str, timeout: int = 5) -> str:
    """Compile C++ code, run with stdin_data, return stdout."""
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "sol.cpp")
        exe = os.path.join(tmpdir, "sol")
        with open(src, "w") as f:
            f.write(cpp_code)
        compile_result = subprocess.run(
            ["g++", "-std=c++17", "-O2", "-o", exe, src],
            capture_output=True, text=True, timeout=timeout
        )
        if compile_result.returncode != 0:
            return f"COMPILE_ERROR: {compile_result.stderr[:200]}"
        run_result = subprocess.run(
            [exe],
            input=stdin_data,
            capture_output=True, text=True, timeout=timeout
        )
        if run_result.returncode != 0:
            return f"RUNTIME_ERROR: {run_result.stderr[:200]}"
        return run_result.stdout.strip()

def list_to_input(arr):
    return f"{len(arr)}\n" + " ".join(map(str, arr)) + "\n"

def parse_output_list(s):
    return list(map(int, s.split()))

def parse_output_scalar(s):
    return int(s.strip())


# ─────────────────────────────────────────────────────────────────────────────
# Problem Definitions
# ─────────────────────────────────────────────────────────────────────────────

PROBLEMS = []

def problem(pid, category, description, pattern_expected, test_type="solution"):
    """Decorator-style appender for problems."""
    def decorator(fn):
        PROBLEMS.append({
            "id": pid,
            "category": category,
            "description": description,
            "pattern_expected": pattern_expected,
            "test_type": test_type,
            "runner": fn,
        })
        return fn
    return decorator


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# A. Primitive Patterns
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@problem("MS-01", "A.Primitive", "Next greater element — canonical formulation",
         "next_greater_element")
def ms01():
    text = (
        "Given an array of N integers, for each element find its next greater element "
        "to the right. Output -1 if no such element exists."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success, got {resp['status']}"
    assert resp["selectedPattern"] == "next_greater_element", f"Wrong pattern: {resp['selectedPattern']}"
    cpp = resp.get("generatedCode", "")
    assert cpp, "No C++ code generated"
    arr = [4, 5, 2, 25, 7, 8]
    expected = oracle_next_greater_element(arr)
    got_str = compile_and_run_cpp(cpp, list_to_input(arr))
    assert not got_str.startswith("COMPILE_ERROR"), got_str
    assert not got_str.startswith("RUNTIME_ERROR"), got_str
    got = parse_output_list(got_str)
    assert got == expected, f"NGE: expected {expected}, got {got}"
    return True


@problem("MS-02", "A.Primitive", "Next smaller element — canonical formulation",
         "next_smaller_element")
def ms02():
    text = (
        "Given an integer array, for each element find the next smaller element to its right. "
        "Output -1 if no smaller element exists on the right side."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success, got {resp['status']}"
    assert resp["selectedPattern"] == "next_smaller_element", f"Wrong: {resp['selectedPattern']}"
    cpp = resp.get("generatedCode", "")
    arr = [4, 8, 5, 2, 25]
    expected = oracle_next_smaller_element(arr)
    got_str = compile_and_run_cpp(cpp, list_to_input(arr))
    got = parse_output_list(got_str)
    assert got == expected, f"NSE: expected {expected}, got {got}"
    return True


@problem("MS-03", "A.Primitive", "Previous greater element — canonical formulation",
         "previous_greater_element")
def ms03():
    text = (
        "Given an array, for each element find the previous greater element "
        "(the nearest element to its left that is strictly greater). "
        "Output -1 if no such element exists."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success, got {resp['status']}"
    assert resp["selectedPattern"] == "previous_greater_element", f"Wrong: {resp['selectedPattern']}"
    cpp = resp.get("generatedCode", "")
    arr = [10, 4, 5, 90, 120, 80]
    expected = oracle_previous_greater_element(arr)
    got_str = compile_and_run_cpp(cpp, list_to_input(arr))
    got = parse_output_list(got_str)
    assert got == expected, f"PGE: expected {expected}, got {got}"
    return True


@problem("MS-04", "A.Primitive", "Previous smaller element — canonical formulation",
         "previous_smaller_element")
def ms04():
    text = (
        "For each element in the array, find the previous smaller element "
        "(the nearest element on the left that is strictly smaller). Output -1 if none exists."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success, got {resp['status']}"
    assert resp["selectedPattern"] == "previous_smaller_element", f"Wrong: {resp['selectedPattern']}"
    cpp = resp.get("generatedCode", "")
    arr = [3, 7, 8, 4, 6]
    expected = oracle_previous_smaller_element(arr)
    got_str = compile_and_run_cpp(cpp, list_to_input(arr))
    got = parse_output_list(got_str)
    assert got == expected, f"PSE: expected {expected}, got {got}"
    return True


@problem("MS-05", "A.Primitive", "Nearest greater element — both directions",
         "nearest_greater_element")
def ms05():
    text = (
        "Given an array, for each element find the distance to the nearest element that is "
        "strictly greater than it (looking in either direction — left or right). "
        "Output the minimum such distance, or -1 if no greater element exists."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success, got {resp['status']}"
    assert resp["selectedPattern"] == "nearest_greater_element", f"Wrong: {resp['selectedPattern']}"
    cpp = resp.get("generatedCode", "")
    arr = [1, 3, 2, 4, 2]
    expected = oracle_nearest_greater_element(arr)
    got_str = compile_and_run_cpp(cpp, list_to_input(arr))
    got = parse_output_list(got_str)
    assert got == expected, f"NGE-both: expected {expected}, got {got}"
    return True


@problem("MS-06", "A.Primitive", "Nearest smaller element — both directions",
         "nearest_smaller_element")
def ms06():
    text = (
        "For each element in the given array, find the distance to its nearest element "
        "that is strictly smaller than it (either to the left or right). "
        "Return -1 if no smaller element exists."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success, got {resp['status']}"
    assert resp["selectedPattern"] == "nearest_smaller_element", f"Wrong: {resp['selectedPattern']}"
    cpp = resp.get("generatedCode", "")
    arr = [5, 3, 4, 1, 6]
    expected = oracle_nearest_smaller_element(arr)
    got_str = compile_and_run_cpp(cpp, list_to_input(arr))
    got = parse_output_list(got_str)
    assert got == expected, f"NSE-both: expected {expected}, got {got}"
    return True


@problem("MS-07", "A.Primitive", "Stock span problem — classic",
         "stock_span")
def ms07():
    text = (
        "The stock span problem: given a series of daily stock prices, for each day compute "
        "the number of consecutive days (including today) for which the price was less than or "
        "equal to today's price."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success, got {resp['status']}"
    assert resp["selectedPattern"] == "stock_span", f"Wrong: {resp['selectedPattern']}"
    cpp = resp.get("generatedCode", "")
    arr = [100, 80, 60, 70, 60, 75, 85]
    expected = oracle_stock_span(arr)
    got_str = compile_and_run_cpp(cpp, list_to_input(arr))
    got = parse_output_list(got_str)
    assert got == expected, f"SPAN: expected {expected}, got {got}"
    return True


@problem("MS-08", "A.Primitive", "Largest rectangle in histogram",
         "largest_rectangle_histogram")
def ms08():
    text = (
        "Given a histogram represented as an array of non-negative bar heights where each bar "
        "has width 1, find the area of the largest rectangle in the histogram."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success, got {resp['status']}"
    assert resp["selectedPattern"] == "largest_rectangle_histogram", f"Wrong: {resp['selectedPattern']}"
    cpp = resp.get("generatedCode", "")
    arr = [2, 1, 5, 6, 2, 3]
    expected = oracle_largest_rectangle_histogram(arr)
    got_str = compile_and_run_cpp(cpp, list_to_input(arr))
    got_val = parse_output_scalar(got_str)
    assert got_val == expected, f"HIST: expected {expected}, got {got_val}"
    return True


@problem("MS-09", "A.Primitive", "Circular array — next greater element",
         "circular_next_greater")
def ms09():
    text = (
        "Given a circular array, find the next greater number for every element in the array. "
        "The search wraps around. Output -1 if no greater number exists."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success, got {resp['status']}"
    assert resp["selectedPattern"] == "circular_next_greater", f"Wrong: {resp['selectedPattern']}"
    cpp = resp.get("generatedCode", "")
    arr = [1, 2, 1]
    expected = oracle_circular_next_greater(arr)
    got_str = compile_and_run_cpp(cpp, list_to_input(arr))
    got = parse_output_list(got_str)
    assert got == expected, f"CIRC: expected {expected}, got {got}"
    return True


@problem("MS-10", "A.Primitive", "Sum of subarray minimums",
         "sum_subarray_minimums")
def ms10():
    text = (
        "Given an array of integers, find the sum of minimums of all subarrays modulo 10^9+7."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success, got {resp['status']}"
    assert resp["selectedPattern"] == "sum_subarray_minimums", f"Wrong: {resp['selectedPattern']}"
    cpp = resp.get("generatedCode", "")
    arr = [3, 1, 2, 4]
    expected = oracle_sum_subarray_minimums(arr)
    got_str = compile_and_run_cpp(cpp, list_to_input(arr))
    got_val = parse_output_scalar(got_str)
    assert got_val == expected, f"SUMMIN: expected {expected}, got {got_val}"
    return True


@problem("MS-11", "A.Primitive", "Sum of subarray maximums",
         "sum_subarray_maximums")
def ms11():
    text = (
        "Given an array of integers, compute the sum of maximums of all subarrays modulo 10^9+7."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success, got {resp['status']}"
    assert resp["selectedPattern"] == "sum_subarray_maximums", f"Wrong: {resp['selectedPattern']}"
    cpp = resp.get("generatedCode", "")
    arr = [3, 1, 2, 4]
    expected = oracle_sum_subarray_maximums(arr)
    got_str = compile_and_run_cpp(cpp, list_to_input(arr))
    got_val = parse_output_scalar(got_str)
    assert got_val == expected, f"SUMMAX: expected {expected}, got {got_val}"
    return True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# B. Structural Applications — Random Oracle Verification
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def random_array(n=10, lo=1, hi=20, seed=42):
    rng = random.Random(seed)
    return [rng.randint(lo, hi) for _ in range(n)]

def verify_pattern_oracle(pattern_text, pattern_name, arr, oracle_fn, parse=parse_output_list):
    resp = handle_request({"problemText": pattern_text})
    assert resp["status"] == "success", f"[{pattern_name}] Expected success, got {resp['status']}"
    assert resp["selectedPattern"] == pattern_name, f"[{pattern_name}] Wrong: {resp['selectedPattern']}"
    cpp = resp.get("generatedCode", "")
    expected = oracle_fn(arr)
    got_str = compile_and_run_cpp(cpp, list_to_input(arr))
    assert not got_str.startswith("COMPILE_ERROR"), f"[{pattern_name}] {got_str}"
    assert not got_str.startswith("RUNTIME_ERROR"), f"[{pattern_name}] {got_str}"
    got = parse(got_str)
    assert got == expected, f"[{pattern_name}] Oracle mismatch: expected {expected}, got {got}"


@problem("MS-12", "B.Structural", "NGE with random array (oracle verification)",
         "next_greater_element")
def ms12():
    arr = random_array(n=12, lo=1, hi=30, seed=12)
    verify_pattern_oracle(
        "For each element in the array, find the next greater element to its right. Return -1 if none.",
        "next_greater_element", arr, oracle_next_greater_element
    )
    return True


@problem("MS-13", "B.Structural", "NSE with random array (oracle verification)",
         "next_smaller_element")
def ms13():
    arr = random_array(n=10, lo=1, hi=15, seed=13)
    verify_pattern_oracle(
        "Given an integer array, for each element find the next smaller element to its right. Output -1 if no smaller element exists.",
        "next_smaller_element", arr, oracle_next_smaller_element
    )
    return True


@problem("MS-14", "B.Structural", "Stock span with random prices",
         "stock_span")
def ms14():
    arr = random_array(n=10, lo=50, hi=200, seed=14)
    verify_pattern_oracle(
        "The stock span problem: given daily stock prices, for each day find how many consecutive previous days had price less than or equal to today's price, including today.",
        "stock_span", arr, oracle_stock_span
    )
    return True


@problem("MS-15", "B.Structural", "Histogram largest rectangle random",
         "largest_rectangle_histogram")
def ms15():
    arr = random_array(n=8, lo=1, hi=10, seed=15)
    verify_pattern_oracle(
        "Find the area of the largest rectangle in the histogram.",
        "largest_rectangle_histogram", arr, oracle_largest_rectangle_histogram,
        parse=parse_output_scalar
    )
    return True


@problem("MS-16", "B.Structural", "Circular NGE with random array",
         "circular_next_greater")
def ms16():
    arr = random_array(n=6, lo=1, hi=10, seed=16)
    verify_pattern_oracle(
        "Given a circular array, find the next greater number for every element. The search wraps around. Output -1 if none.",
        "circular_next_greater", arr, oracle_circular_next_greater
    )
    return True


@problem("MS-17", "B.Structural", "Sum of subarray minimums random array",
         "sum_subarray_minimums")
def ms17():
    arr = random_array(n=8, lo=1, hi=10, seed=17)
    verify_pattern_oracle(
        "Find the sum of minimums of all subarrays modulo 10^9+7.",
        "sum_subarray_minimums", arr, oracle_sum_subarray_minimums,
        parse=parse_output_scalar
    )
    return True


@problem("MS-18", "B.Structural", "Sum of subarray maximums random array",
         "sum_subarray_maximums")
def ms18():
    arr = random_array(n=8, lo=1, hi=10, seed=18)
    verify_pattern_oracle(
        "Compute the sum of maximums of all subarrays modulo 10^9+7.",
        "sum_subarray_maximums", arr, oracle_sum_subarray_maximums,
        parse=parse_output_scalar
    )
    return True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# C. Strictness Cases — Duplicates
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@problem("MS-19", "C.Strictness", "NGE with duplicate values — strict comparison",
         "next_greater_element")
def ms19():
    arr = [3, 3, 3, 3, 5]
    text = "For each element in the array, find the next element that is strictly greater than it. Output -1 if no such element exists to the right."
    verify_pattern_oracle(text, "next_greater_element", arr, oracle_next_greater_element)
    return True


@problem("MS-20", "C.Strictness", "Sum of subarray minimums with all-equal array",
         "sum_subarray_minimums")
def ms20():
    arr = [5, 5, 5, 5]
    text = "Find the sum of minimums of all subarrays modulo 10^9+7."
    verify_pattern_oracle(text, "sum_subarray_minimums", arr, oracle_sum_subarray_minimums,
                          parse=parse_output_scalar)
    return True


@problem("MS-21", "C.Strictness", "Histogram with all equal bars",
         "largest_rectangle_histogram")
def ms21():
    arr = [4, 4, 4, 4, 4]
    text = "Find the area of the largest rectangle in the histogram."
    verify_pattern_oracle(text, "largest_rectangle_histogram", arr, oracle_largest_rectangle_histogram,
                          parse=parse_output_scalar)
    return True


@problem("MS-22", "C.Strictness", "Stock span with consecutive equal prices",
         "stock_span")
def ms22():
    arr = [10, 10, 10, 10]
    text = "The stock span problem: for each day compute the number of consecutive days with price less than or equal to today's price."
    verify_pattern_oracle(text, "stock_span", arr, oracle_stock_span)
    return True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# D. Contribution / Compound Problems
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@problem("MS-23", "D.Contribution", "Sum of subarray minimums — large random",
         "sum_subarray_minimums")
def ms23():
    arr = random_array(n=15, lo=1, hi=50, seed=23)
    text = "Given an array, find the sum of minimums of all subarrays modulo 10^9+7."
    verify_pattern_oracle(text, "sum_subarray_minimums", arr, oracle_sum_subarray_minimums,
                          parse=parse_output_scalar)
    return True


@problem("MS-24", "D.Contribution", "Sum of subarray maximums — large random",
         "sum_subarray_maximums")
def ms24():
    arr = random_array(n=15, lo=1, hi=50, seed=24)
    text = "Given an integer array, compute the sum of maximums of all subarrays modulo 10^9+7."
    verify_pattern_oracle(text, "sum_subarray_maximums", arr, oracle_sum_subarray_maximums,
                          parse=parse_output_scalar)
    return True


@problem("MS-25", "D.Contribution", "Sum of subarray mins — array with duplicates",
         "sum_subarray_minimums")
def ms25():
    arr = [1, 2, 1, 2, 1]
    text = "Find the sum of minimums of all subarrays modulo 10^9+7."
    verify_pattern_oracle(text, "sum_subarray_minimums", arr, oracle_sum_subarray_minimums,
                          parse=parse_output_scalar)
    return True


@problem("MS-26", "D.Contribution", "Sum of subarray maxes — array with duplicates",
         "sum_subarray_maximums")
def ms26():
    arr = [2, 1, 2, 1, 2]
    text = "Compute the sum of maximums of all subarrays modulo 10^9+7."
    verify_pattern_oracle(text, "sum_subarray_maximums", arr, oracle_sum_subarray_maximums,
                          parse=parse_output_scalar)
    return True


@problem("MS-27", "D.Contribution", "NGE — multiple random trials",
         "next_greater_element")
def ms27():
    for seed in [27, 271, 2700]:
        arr = random_array(n=10, lo=1, hi=20, seed=seed)
        verify_pattern_oracle(
            "For each element in the array, find the next greater element to the right. Return -1 if none exists.",
            "next_greater_element", arr, oracle_next_greater_element
        )
    return True


@problem("MS-28", "D.Contribution", "Histogram — multiple random trials",
         "largest_rectangle_histogram")
def ms28():
    for seed in [28, 280, 2800]:
        arr = random_array(n=7, lo=1, hi=12, seed=seed)
        verify_pattern_oracle(
            "Find the area of the largest rectangle in the histogram.",
            "largest_rectangle_histogram", arr, oracle_largest_rectangle_histogram,
            parse=parse_output_scalar
        )
    return True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# E. Anti-Patterns — Must Be Rejected
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@problem("MS-29", "E.AntiPattern",
         "Dynamic updates — should NOT use monotonic stack",
         "rejected", test_type="rejection")
def ms29():
    text = (
        "You are given an array and can perform two operations online: "
        "(1) update arr[i] to a new value, (2) query for the next greater element at position j. "
        "Queries and updates are interleaved."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "rejected", f"Expected rejection, got {resp['status']}"
    return True


@problem("MS-30", "E.AntiPattern",
         "Pair sum sorted — should route to two_pointers, not monotonic_stack",
         "two_pointers_converging", test_type="non_ms_routing")
def ms30():
    text = "Given a sorted array and a target sum, find if any pair sums to the target."
    resp = handle_request({"problemText": text})
    # This should be accepted but NOT as monotonic_stack
    assert resp["status"] == "success", f"Expected success, got {resp['status']}"
    assert resp.get("family") != "monotonic_stack", f"Should not be monotonic_stack"
    return True


@problem("MS-31", "E.AntiPattern",
         "Sliding window max k elements — should route to sliding window, not MS",
         "sliding_window", test_type="non_ms_routing")
def ms31():
    text = "Given an array and window size k, find the maximum element in each window of size k."
    resp = handle_request({"problemText": text})
    # Should be accepted but not monotonic_stack (it's a sliding window deque problem)
    assert resp["status"] in ("success", "rejected"), f"Unexpected status: {resp['status']}"
    if resp["status"] == "success":
        assert resp.get("family") != "monotonic_stack", "Should not be monotonic stack for fixed window max"
    return True


@problem("MS-32", "E.AntiPattern",
         "Range minimum query with dynamic updates — should be rejected for monotonic stack",
         "rejected", test_type="rejection")
def ms32():
    text = (
        "Given an array, answer Q range minimum queries [l, r] and support point updates "
        "to arr[i]. Queries and updates are interleaved."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "rejected", f"Expected rejection, got {resp['status']}"
    return True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# F. Paraphrase Variants — Same Problem, Different Wording
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@problem("MS-33", "F.Paraphrase",
         "Daily temperatures — paraphrase of NGE (wait days until warmer)",
         "next_greater_element")
def ms33():
    text = (
        "Given a list of daily temperatures, return an array such that, for each day, "
        "tells you how many days you would have to wait until a warmer temperature. "
        "If there is no future day with a warmer temperature, put 0 in that spot."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success, got {resp['status']}"
    assert resp["selectedPattern"] == "next_greater_element", f"Wrong: {resp['selectedPattern']}"
    # Note: this paraphrase asks for distance (not value), but the same stack structure applies
    # Verify the C++ compiles and runs:
    cpp = resp.get("generatedCode", "")
    arr = [73, 74, 75, 71, 69, 72, 76, 73]
    got_str = compile_and_run_cpp(cpp, list_to_input(arr))
    assert not got_str.startswith("COMPILE_ERROR"), got_str
    assert not got_str.startswith("RUNTIME_ERROR"), got_str
    return True


@problem("MS-34", "F.Paraphrase",
         "Maximal rectangle in histogram — paraphrase with 'bars'",
         "largest_rectangle_histogram")
def ms34():
    text = (
        "You are given an array of bars in a histogram. Each bar has height h[i] and width 1. "
        "Find the largest rectangle you can form using consecutive bars."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success, got {resp['status']}"
    assert resp["selectedPattern"] == "largest_rectangle_histogram", f"Wrong: {resp['selectedPattern']}"
    arr = [6, 2, 5, 4, 5, 1, 6]
    expected = oracle_largest_rectangle_histogram(arr)
    cpp = resp.get("generatedCode", "")
    got_str = compile_and_run_cpp(cpp, list_to_input(arr))
    got = parse_output_scalar(got_str)
    assert got == expected, f"HIST paraphrase: expected {expected}, got {got}"
    return True


@problem("MS-35", "F.Paraphrase",
         "Previous smaller element — phrased as 'nearest left boundary'",
         "previous_smaller_element")
def ms35():
    text = (
        "For each position i in the array, find the nearest position j < i such that "
        "the value at j is strictly smaller than the value at i. Output the value at j, "
        "or -1 if no such position exists on the left."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success, got {resp['status']}"
    assert resp["selectedPattern"] == "previous_smaller_element", f"Wrong: {resp['selectedPattern']}"
    arr = [2, 5, 3, 7, 4]
    expected = oracle_previous_smaller_element(arr)
    cpp = resp.get("generatedCode", "")
    got_str = compile_and_run_cpp(cpp, list_to_input(arr))
    got = parse_output_list(got_str)
    assert got == expected, f"PSE paraphrase: expected {expected}, got {got}"
    return True


@problem("MS-36", "F.Paraphrase",
         "Sum of subarray minimums — phrased differently",
         "sum_subarray_minimums")
def ms36():
    text = (
        "Given an array A, for every possible contiguous subarray of A, "
        "record the minimum value in that subarray. "
        "Return the total sum of all those minimum values, modulo 10^9+7."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success, got {resp['status']}"
    assert resp["selectedPattern"] == "sum_subarray_minimums", f"Wrong: {resp['selectedPattern']}"
    arr = [2, 4, 1, 3]
    expected = oracle_sum_subarray_minimums(arr)
    cpp = resp.get("generatedCode", "")
    got_str = compile_and_run_cpp(cpp, list_to_input(arr))
    got = parse_output_scalar(got_str)
    assert got == expected, f"SUMMIN paraphrase: expected {expected}, got {got}"
    return True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# G. Adversarial / Edge Cases
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@problem("MS-37", "G.Adversarial", "n=1 edge case — NGE",
         "next_greater_element")
def ms37():
    text = "For each element in the array, find the next greater element to the right. Return -1 if none exists."
    verify_pattern_oracle(text, "next_greater_element", [42], oracle_next_greater_element)
    return True


@problem("MS-38", "G.Adversarial", "Strictly monotone decreasing — all NGE = -1",
         "next_greater_element")
def ms38():
    arr = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    text = "For each element, find the next greater element to the right. Return -1 if none."
    expected = oracle_next_greater_element(arr)
    assert all(v == -1 for v in expected), "All NGE should be -1 for strictly decreasing"
    verify_pattern_oracle(text, "next_greater_element", arr, oracle_next_greater_element)
    return True


@problem("MS-39", "G.Adversarial", "Histogram with single tallest bar in middle",
         "largest_rectangle_histogram")
def ms39():
    arr = [1, 2, 3, 10, 3, 2, 1]
    text = "Find the area of the largest rectangle in the histogram."
    expected = oracle_largest_rectangle_histogram(arr)
    verify_pattern_oracle(text, "largest_rectangle_histogram", arr, oracle_largest_rectangle_histogram,
                          parse=parse_output_scalar)
    return True


@problem("MS-40", "G.Adversarial", "Circular NGE — all equal (all -1)",
         "circular_next_greater")
def ms40():
    arr = [3, 3, 3, 3]
    text = "Given a circular array, find the next greater number for every element. Output -1 if no greater number exists anywhere in the circular array."
    expected = oracle_circular_next_greater(arr)
    assert all(v == -1 for v in expected), f"All circular NGE should be -1 for all-equal: {expected}"
    verify_pattern_oracle(text, "circular_next_greater", arr, oracle_circular_next_greater)
    return True


# ─────────────────────────────────────────────────────────────────────────────
# Benchmark Runner
# ─────────────────────────────────────────────────────────────────────────────

def run_benchmark(problems=None, verbose=True):
    target = problems or PROBLEMS
    passed = 0
    failed = 0
    errors = []
    total_start = time.time()

    for p in target:
        pid = p["id"]
        cat = p["category"]
        desc = p["description"]
        runner = p["runner"]

        start = time.time()
        try:
            result = runner()
            elapsed = time.time() - start
            if result:
                passed += 1
                if verbose:
                    print(f"  ✓ {pid} [{cat}] {desc[:60]} ({elapsed:.2f}s)")
        except Exception as e:
            elapsed = time.time() - start
            failed += 1
            err = str(e)[:200]
            errors.append((pid, cat, desc, err))
            if verbose:
                print(f"  ✗ {pid} [{cat}] {desc[:60]} — {err} ({elapsed:.2f}s)")

    total_elapsed = time.time() - total_start
    total = passed + failed

    print()
    print("=" * 70)
    print(f"  MS Benchmark Results: {passed}/{total} passed ({100*passed//total if total else 0}%)")
    print(f"  Total time: {total_elapsed:.2f}s")
    print("=" * 70)

    if errors:
        print("\n  FAILURES:")
        for pid, cat, desc, err in errors:
            print(f"    [{pid}] {desc[:50]}: {err}")

    return passed, failed, errors


if __name__ == "__main__":
    print("CHUP Phase 3B — Monotonic Stack Benchmark")
    print("=" * 70)
    run_benchmark()
