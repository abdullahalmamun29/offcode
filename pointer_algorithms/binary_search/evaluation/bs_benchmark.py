"""
Binary Search Benchmark — Phase 3C (BS-01 through BS-40)

Benchmark structure:
  A. Basic Ordered Search        (BS-01..BS-08) — exact, bounds, occurrence, pred/succ
  B. Predicate & Boundary        (BS-09..BS-16) — first/last true/false, duplicates, extremes
  C. Binary Search on Answer     (BS-17..BS-24) — min capacity, max distance, allocations
  D. Compound Problems           (BS-25..BS-28) — BS + greedy, sorting, prefix sum
  E. Value Domain / Numerical    (BS-29..BS-32) — integer sqrt, overflow safety
  F. Anti-Patterns               (BS-33..BS-36) — unsorted, non-monotone, dynamic updates
  G. Adversarial / Reformulated  (BS-37..BS-40) — bananas, timestamps, all-equal, 2-element

All problems invoke the real pipeline entry point: handle_request({'problemText': ...}).
All generated C++ code is compiled with g++ -std=c++17 -O2, executed with test inputs,
and independently verified against brute-force oracles.
"""

import sys
import os
import subprocess
import tempfile
import random
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.binary_search.verification.bs_brute_force_oracles import (
    oracle_binary_search_exact,
    oracle_lower_bound,
    oracle_upper_bound,
    oracle_first_occurrence,
    oracle_last_occurrence,
    oracle_predecessor,
    oracle_successor,
    oracle_first_false,
    oracle_last_false,
    oracle_min_ship_capacity,
    oracle_max_min_distance,
    oracle_integer_sqrt,
)

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

def array_and_target_input(arr, target):
    return f"{len(arr)} {target}\n" + " ".join(map(str, arr)) + "\n"

def single_val_input(n):
    return f"{n}\n"

def parse_int_output(s):
    return int(s.strip())

PROBLEMS = []

def problem(pid, category, description, expected_pattern, test_type="solution"):
    def decorator(fn):
        PROBLEMS.append({
            "id": pid,
            "category": category,
            "description": description,
            "expected_pattern": expected_pattern,
            "test_type": test_type,
            "runner": fn,
        })
        return fn
    return decorator


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# A. Basic Ordered Search (BS-01 .. BS-08)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@problem("BS-01", "A.BasicOrdered", "Exact binary search lookup", "binary_search_exact")
def bs01():
    text = "Given a sorted array of integers, search for the target value x using exact binary search. Return its 0-based index or -1 if absent."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "binary_search_exact", f"Wrong pattern: {resp['selectedPattern']}"
    assert resp["family"] == "binary_search"
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target = 23
    expected = oracle_binary_search_exact(arr, target)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, target)))
    assert got == expected, f"BS-01 expected {expected}, got {got}"
    return True


@problem("BS-02", "A.BasicOrdered", "Lower bound lookup (first >= target)", "lower_bound")
def bs02():
    text = "Given a sorted array of numbers, find the lower bound of x: the smallest index such that arr[i] >= x."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "lower_bound", f"Wrong: {resp['selectedPattern']}"
    arr = [2, 4, 6, 8, 10, 12, 14]
    target = 7
    expected = oracle_lower_bound(arr, target)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, target)))
    assert got == expected, f"BS-02 expected {expected}, got {got}"
    return True


@problem("BS-03", "A.BasicOrdered", "Upper bound lookup (first > target)", "upper_bound")
def bs03():
    text = "In a sorted array, compute the upper bound of target: the first index where the element is strictly greater than target."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "upper_bound", f"Wrong: {resp['selectedPattern']}"
    arr = [2, 4, 6, 6, 6, 10, 12]
    target = 6
    expected = oracle_upper_bound(arr, target)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, target)))
    assert got == expected, f"BS-03 expected {expected}, got {got}"
    return True


@problem("BS-04", "A.BasicOrdered", "First occurrence in sorted array with duplicates", "first_true")
def bs04():
    text = "Given a sorted array containing duplicates, find the first occurrence of the target value. Return -1 if target is not found."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "first_true", f"Wrong: {resp['selectedPattern']}"
    arr = [1, 2, 2, 2, 3, 4, 5]
    target = 2
    expected = oracle_first_occurrence(arr, target)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, target)))
    assert got == expected, f"BS-04 expected {expected}, got {got}"
    return True


@problem("BS-05", "A.BasicOrdered", "Last occurrence in sorted array with duplicates", "last_true")
def bs05():
    text = "Given a sorted array containing duplicates, find the last occurrence of the target value. Return -1 if not found."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "last_true", f"Wrong: {resp['selectedPattern']}"
    arr = [1, 2, 2, 2, 2, 3, 4]
    target = 2
    expected = oracle_last_occurrence(arr, target)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, target)))
    assert got == expected, f"BS-05 expected {expected}, got {got}"
    return True


@problem("BS-06", "A.BasicOrdered", "Predecessor in sorted array (largest < target)", "predecessor")
def bs06():
    text = "Find the predecessor of x in a sorted array: the largest element that is strictly less than x. Output -1 if no such element exists."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "predecessor", f"Wrong: {resp['selectedPattern']}"
    arr = [3, 7, 12, 18, 25]
    target = 15
    expected = oracle_predecessor(arr, target)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, target)))
    assert got == expected, f"BS-06 expected {expected}, got {got}"
    return True


@problem("BS-07", "A.BasicOrdered", "Successor in sorted array (smallest > target)", "successor")
def bs07():
    text = "Find the successor of x in a sorted array: the smallest element that is strictly greater than x. Output -1 if no such element exists."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "successor", f"Wrong: {resp['selectedPattern']}"
    arr = [3, 7, 12, 18, 25]
    target = 12
    expected = oracle_successor(arr, target)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, target)))
    assert got == expected, f"BS-07 expected {expected}, got {got}"
    return True


@problem("BS-08", "A.BasicOrdered", "Boundary existence check: target absent", "binary_search_exact")
def bs08():
    text = "Given a sorted array, search for the target value using exact binary search. Output -1 when the element is not present."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "binary_search_exact"
    arr = [10, 20, 30, 40, 50]
    target = 35
    expected = oracle_binary_search_exact(arr, target)
    assert expected == -1
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, target)))
    assert got == -1, f"BS-08 expected -1, got {got}"
    return True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# B. Predicate & Boundary Reasoning (BS-09 .. BS-16)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@problem("BS-09", "B.PredicateBoundary", "First true on monotonic boolean predicate", "first_true")
def bs09():
    text = "Given a sorted array where a boolean predicate transitions from false to true, find the first index where the predicate is true."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "first_true"
    arr = [0, 0, 0, 1, 1, 1]
    expected = 3
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, 1)))
    assert got == expected, f"BS-09 expected {expected}, got {got}"
    return True


@problem("BS-10", "B.PredicateBoundary", "Last true on monotonic boolean predicate", "last_true")
def bs10():
    text = "Given a sorted array where a condition holds for a prefix, find the last index where the condition is true."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "last_true"
    arr = [1, 1, 1, 1, 0, 0]
    expected = 3
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, 1)))
    assert got == expected, f"BS-10 expected {expected}, got {got}"
    return True


@problem("BS-11", "B.PredicateBoundary", "First false on monotonic predicate", "first_false")
def bs11():
    text = "In an ordered collection, identify the first false transition point where the elements stop satisfying the threshold."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "first_false"
    arr = [1, 2, 3, 4, 8, 9]
    target = 4
    expected = oracle_first_false(arr, target)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, target)))
    assert got == expected, f"BS-11 expected {expected}, got {got}"
    return True


@problem("BS-12", "B.PredicateBoundary", "Last false on monotonic predicate", "last_false")
def bs12():
    text = "In a sorted sequence, find the last false position before the values reach the required threshold."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "last_false"
    arr = [1, 2, 3, 5, 8, 10]
    target = 5
    expected = oracle_last_false(arr, target)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, target)))
    assert got == expected, f"BS-12 expected {expected}, got {got}"
    return True


@problem("BS-13", "B.PredicateBoundary", "Duplicate-heavy array lower bound", "lower_bound")
def bs13():
    text = "Given a sorted array of numbers with many duplicate elements, compute the lower bound of x."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    arr = [5, 5, 5, 5, 5, 5, 5]
    target = 5
    expected = oracle_lower_bound(arr, target)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, target)))
    assert got == expected, f"BS-13 expected {expected}, got {got}"
    return True


@problem("BS-14", "B.PredicateBoundary", "Target smaller than all elements", "lower_bound")
def bs14():
    text = "Find the lower bound of target in a sorted array where target is smaller than every element."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    arr = [10, 20, 30, 40]
    target = 5
    expected = oracle_lower_bound(arr, target)
    assert expected == 0
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, target)))
    assert got == 0, f"BS-14 expected 0, got {got}"
    return True


@problem("BS-15", "B.PredicateBoundary", "Target larger than all elements", "lower_bound")
def bs15():
    text = "Find the lower bound of target in a sorted array where target is strictly larger than every element in the array."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    arr = [10, 20, 30, 40]
    target = 50
    expected = oracle_lower_bound(arr, target)
    assert expected == len(arr)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, target)))
    assert got == len(arr), f"BS-15 expected {len(arr)}, got {got}"
    return True


@problem("BS-16", "B.PredicateBoundary", "Single-element array exact search", "binary_search_exact")
def bs16():
    text = "Given a sorted array of 1 element, search for the target value x using exact binary search."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    arr = [42]
    # found
    got1 = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, 42)))
    assert got1 == 0, f"BS-16 found expected 0, got {got1}"
    # absent
    got2 = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, 99)))
    assert got2 == -1, f"BS-16 absent expected -1, got {got2}"
    return True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# C. Binary Search on Answer (BS-17 .. BS-24)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@problem("BS-17", "C.AnswerSpace", "Ship capacity within D days", "binary_search_answer_min")
def bs17():
    text = "Given weights of packages, find the minimum ship capacity to deliver all packages within D days."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "binary_search_answer_min"
    weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    days = 5
    expected = oracle_min_ship_capacity(weights, days)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(weights, days)))
    assert got == expected, f"BS-17 expected {expected}, got {got}"
    return True


@problem("BS-18", "C.AnswerSpace", "Minimum speed to finish in time", "binary_search_answer_min")
def bs18():
    text = "A worker has tasks with given workloads. Find the minimum speed (work capacity per period) to complete all tasks in at most K periods."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "binary_search_answer_min"
    tasks = [3, 6, 7, 11]
    k = 8
    expected = oracle_min_ship_capacity(tasks, k)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(tasks, k)))
    assert got == expected, f"BS-18 expected {expected}, got {got}"
    return True


@problem("BS-19", "C.AnswerSpace", "Painter partition: minimum maximum load", "binary_search_answer_min")
def bs19():
    text = "In painter's partition, allocate contiguous boards to K painters to minimize the maximum load assigned to any painter."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "binary_search_answer_min"
    boards = [10, 20, 30, 40]
    k = 2
    expected = oracle_min_ship_capacity(boards, k)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(boards, k)))
    assert got == expected, f"BS-19 expected {expected}, got {got}"
    return True


@problem("BS-20", "C.AnswerSpace", "Split array largest sum into K subarrays", "binary_search_answer_min")
def bs20():
    text = "Split array largest sum: partition an array into K contiguous subarrays such that the smallest maximum sum of any subarray is achieved."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "binary_search_answer_min"
    arr = [7, 2, 5, 10, 8]
    k = 2
    expected = oracle_min_ship_capacity(arr, k)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, k)))
    assert got == expected, f"BS-20 expected {expected}, got {got}"
    return True


@problem("BS-21", "C.AnswerSpace", "Aggressive cows: maximize minimum distance", "binary_search_answer_max")
def bs21():
    text = "Given stalls positions, place C cows such that the minimum distance between any two cows is maximized. Solve aggressive cows."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "binary_search_answer_max"
    stalls = [1, 2, 8, 4, 9]
    cows = 3
    expected = oracle_max_min_distance(stalls, cows)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(stalls, cows)))
    assert got == expected, f"BS-21 expected {expected}, got {got}"
    return True


@problem("BS-22", "C.AnswerSpace", "Maximum feasible threshold", "binary_search_answer_max")
def bs22():
    text = "Given coordinate positions of markers along a track, select K markers to achieve the maximum possible minimum distance between consecutive chosen markers."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "binary_search_answer_max"
    markers = [0, 3, 4, 7, 10, 9]
    k = 3
    expected = oracle_max_min_distance(markers, k)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(markers, k)))
    assert got == expected, f"BS-22 expected {expected}, got {got}"
    return True


@problem("BS-23", "C.AnswerSpace", "Minimum capacity with randomized weights", "binary_search_answer_min")
def bs23():
    text = "Compute the minimum capacity required to ship items within D days across multiple random trials."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    rng = random.Random(23)
    weights = [rng.randint(1, 30) for _ in range(12)]
    days = 4
    expected = oracle_min_ship_capacity(weights, days)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(weights, days)))
    assert got == expected, f"BS-23 expected {expected}, got {got}"
    return True


@problem("BS-24", "C.AnswerSpace", "Maximum distance with randomized coordinates", "binary_search_answer_max")
def bs24():
    text = "Place cows in stalls to maximize the minimum distance between any pair of cows."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    rng = random.Random(24)
    stalls = sorted([rng.randint(1, 100) for _ in range(10)])
    cows = 4
    expected = oracle_max_min_distance(stalls, cows)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(stalls, cows)))
    assert got == expected, f"BS-24 expected {expected}, got {got}"
    return True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# D. Compound Problems (BS-25 .. BS-28)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@problem("BS-25", "D.Compound", "Binary Search + Greedy check", "binary_search_answer_min")
def bs25():
    text = "Given an array of job workloads, greedily test feasibility to find the minimum capacity to finish all jobs within K days."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "binary_search_answer_min"
    jobs = [12, 34, 67, 90]
    k = 2
    expected = oracle_min_ship_capacity(jobs, k)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(jobs, k)))
    assert got == expected, f"BS-25 expected {expected}, got {got}"
    return True


@problem("BS-26", "D.Compound", "Binary Search + Sorting unsorted input", "binary_search_answer_max")
def bs26():
    text = "Given unsorted stall coordinates, sort first and then binary search the answer to place K cows such that the minimum distance is maximized."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "binary_search_answer_max"
    stalls = [10, 2, 5, 3, 9]
    k = 3
    expected = oracle_max_min_distance(stalls, k)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(stalls, k)))
    assert got == expected, f"BS-26 expected {expected}, got {got}"
    return True


@problem("BS-27", "D.Compound", "Binary Search + Prefix sum / Contiguous segments", "binary_search_answer_min")
def bs27():
    text = "Using prefix sum or greedy partition, find the minimum possible maximum load allocated across K workers."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "binary_search_answer_min"
    loads = [1, 4, 4]
    k = 3
    expected = oracle_min_ship_capacity(loads, k)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(loads, k)))
    assert got == expected, f"BS-27 expected {expected}, got {got}"
    return True


@problem("BS-28", "D.Compound", "Binary Search + Range boundary", "lower_bound")
def bs28():
    text = "Find the lower bound index in a sorted array to evaluate range queries."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    arr = [5, 10, 15, 20, 25]
    target = 18
    expected = oracle_lower_bound(arr, target)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, target)))
    assert got == expected, f"BS-28 expected {expected}, got {got}"
    return True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# E. Value Domain / Numerical Cases (BS-29 .. BS-32)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@problem("BS-29", "E.ValueDomain", "Integer square root of positive N", "binary_search_value_domain")
def bs29():
    text = "Given an integer n, find its integer square root (the largest integer x such that x*x <= n) using binary search."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "binary_search_value_domain"
    n = 26
    expected = oracle_integer_sqrt(n)
    got = parse_int_output(compile_and_run_cpp(resp["code"], single_val_input(n)))
    assert got == expected, f"BS-29 expected {expected}, got {got}"
    return True


@problem("BS-30", "E.ValueDomain", "Integer square root of 0 (edge case)", "binary_search_value_domain")
def bs30():
    text = "Find the integer square root of 0 using binary search over the integer domain."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    got = parse_int_output(compile_and_run_cpp(resp["code"], single_val_input(0)))
    assert got == 0, f"BS-30 expected 0, got {got}"
    return True


@problem("BS-31", "E.ValueDomain", "Integer square root with large number (overflow safe)", "binary_search_value_domain")
def bs31():
    text = "Find the integer square root of a large integer n where x*x might exceed 32-bit limits."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    n = 1000000000000  # 10^12 -> sqrt is 10^6
    expected = 1000000
    got = parse_int_output(compile_and_run_cpp(resp["code"], single_val_input(n)))
    assert got == expected, f"BS-31 expected {expected}, got {got}"
    return True


@problem("BS-32", "E.ValueDomain", "Integer square root perfect square", "binary_search_value_domain")
def bs32():
    text = "Compute square root of an integer: find integer x such that x*x is exactly equal or floor."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    n = 81
    got = parse_int_output(compile_and_run_cpp(resp["code"], single_val_input(n)))
    assert got == 9, f"BS-32 expected 9, got {got}"
    return True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# F. Anti-Patterns (Strict Rejections) (BS-33 .. BS-36)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@problem("BS-33", "F.AntiPattern", "Unsorted array without sorting — should reject",
         "rejected", test_type="rejection")
def bs33():
    text = "Given an unsorted array of numbers, search for target using binary search without sorting the array."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "rejected", f"Expected rejection, got {resp['status']}"
    return True


@problem("BS-34", "F.AntiPattern", "Non-monotone predicate (oscillating) — should reject",
         "rejected", test_type="rejection")
def bs34():
    text = "Given an array where the test predicate alternates between true and false arbitrarily, find an element satisfying the non-monotonic predicate."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "rejected", f"Expected rejection, got {resp['status']}"
    return True


@problem("BS-35", "F.AntiPattern", "Dynamic point updates with queries — should reject static BS",
         "rejected", test_type="rejection")
def bs35():
    text = "Given a sequence, support interleaved online point updates to elements and repeated binary search queries."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "rejected", f"Expected rejection, got {resp['status']}"
    return True


@problem("BS-36", "F.AntiPattern", "Non-monotone feasibility in answer space — should reject",
         "rejected", test_type="rejection")
def bs36():
    text = "Find minimum capacity where feasibility is non-monotonic and oscillates true then false then true."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "rejected", f"Expected rejection, got {resp['status']}"
    return True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# G. Adversarial / Reformulated Problems (BS-37 .. BS-40)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@problem("BS-37", "G.Adversarial", "Koko eating bananas paraphrase", "binary_search_answer_min")
def bs37():
    text = "Piles of bananas are given. A monkey wants to find the minimum eating speed to finish all banana piles within H hours. Koko eating bananas."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "binary_search_answer_min"
    piles = [3, 6, 7, 11]
    h = 8
    expected = oracle_min_ship_capacity(piles, h)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(piles, h)))
    assert got == expected, f"BS-37 expected {expected}, got {got}"
    return True


@problem("BS-38", "G.Adversarial", "Timestamp threshold search (lower bound paraphrase)", "lower_bound")
def bs38():
    text = "Telemetry timestamps are recorded in ascending order. Find the first index where the recorded timestamp is greater than or equal to the query timestamp."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "lower_bound"
    timestamps = [100, 200, 300, 400, 500]
    t = 250
    expected = oracle_lower_bound(timestamps, t)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(timestamps, t)))
    assert got == expected, f"BS-38 expected {expected}, got {got}"
    return True


@problem("BS-39", "G.Adversarial", "All-equal array binary search", "binary_search_exact")
def bs39():
    text = "Given a sorted array where every single element is identical, search for target using exact binary search."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    arr = [7, 7, 7, 7, 7]
    got1 = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, 7)))
    assert got1 in (0, 1, 2, 3, 4), f"BS-39 expected valid index, got {got1}"
    got2 = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, 8)))
    assert got2 == -1, f"BS-39 expected -1, got {got2}"
    return True


@problem("BS-40", "G.Adversarial", "Two-element array boundary search", "lower_bound")
def bs40():
    text = "Given a sorted array of exactly two elements, compute the lower bound of target."
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    arr = [10, 20]
    assert parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, 5))) == 0
    assert parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, 15))) == 1
    assert parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(arr, 25))) == 2
    return True


# ─────────────────────────────────────────────────────────────────────────────
# Runner
# ─────────────────────────────────────────────────────────────────────────────

def run_benchmark(verbose=True):
    passed = 0
    failed = 0
    errors = []
    total_start = time.time()

    for p in PROBLEMS:
        pid = p["id"]
        cat = p["category"]
        desc = p["description"]
        runner = p["runner"]

        start = time.time()
        try:
            res = runner()
            elapsed = time.time() - start
            if res:
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
    print(f"  Binary Search Benchmark Results: {passed}/{total} passed ({100*passed//total if total else 0}%)")
    print(f"  Total time: {total_elapsed:.2f}s")
    print("=" * 70)

    if errors:
        print("\n  FAILURES:")
        for pid, cat, desc, err in errors:
            print(f"    [{pid}] {desc[:50]}: {err}")

    return passed, failed, errors

if __name__ == "__main__":
    print("CHUP Phase 3C — Binary Search Benchmark")
    print("=" * 70)
    run_benchmark()
