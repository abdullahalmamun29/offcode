"""
Monotonic Stack Blind Holdout — Phase 3B (BH-01 through BH-10)

10 problems NOT referenced during development. Each is independently verified
against the O(n^2) oracle. These test genuine generalization.

All problems use distinct phrasing not seen in ms_benchmark.py.
"""

import sys
import os
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.monotonic_stack.evaluation.ms_benchmark import (
    compile_and_run_cpp, list_to_input, parse_output_list, parse_output_scalar
)
from pointer_algorithms.monotonic_stack.verification.ms_brute_force_oracles import (
    oracle_next_greater_element, oracle_next_smaller_element,
    oracle_previous_greater_element, oracle_previous_smaller_element,
    oracle_stock_span, oracle_largest_rectangle_histogram,
    oracle_circular_next_greater,
    oracle_sum_subarray_minimums, oracle_sum_subarray_maximums,
)

def rng_arr(n, lo, hi, seed):
    r = random.Random(seed)
    return [r.randint(lo, hi) for _ in range(n)]

HOLDOUT = []

def holdout(pid, desc):
    def decorator(fn):
        HOLDOUT.append({"id": pid, "description": desc, "runner": fn})
        return fn
    return decorator


@holdout("BH-01",
    "Temperature forecast: find earliest future day warmer than current (novel phrasing)")
def bh01():
    # Phrasing: 'first future day' + 'warmer' → NGE
    text = (
        "You are given a temperature forecast for the next N days. "
        "For each day, output the temperature on the first future day that is warmer "
        "than the current day's temperature. If no such day exists, output -1."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "next_greater_element", f"Wrong: {resp['selectedPattern']}"
    arr = [30, 25, 27, 35, 28, 33]
    expected = oracle_next_greater_element(arr)
    got = parse_output_list(compile_and_run_cpp(resp["generatedCode"], list_to_input(arr)))
    assert got == expected, f"BH-01: expected {expected}, got {got}"
    return True


@holdout("BH-02",
    "Building skyline: for each building, find the taller building immediately to its left")
def bh02():
    text = (
        "Given an array of building heights, for each building find the height of "
        "the nearest taller building to its left. Output -1 if no taller building exists on the left."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "previous_greater_element", f"Wrong: {resp['selectedPattern']}"
    arr = [3, 5, 2, 6, 4]
    expected = oracle_previous_greater_element(arr)
    got = parse_output_list(compile_and_run_cpp(resp["generatedCode"], list_to_input(arr)))
    assert got == expected, f"BH-02: expected {expected}, got {got}"
    return True


@holdout("BH-03",
    "Water trap depths: for each trench, find first shallower trench to the right")
def bh03():
    text = (
        "You have trenches of various depths. For each trench, find the first trench "
        "to the right that is shallower (has a smaller depth value). Output -1 if none exists."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "next_smaller_element", f"Wrong: {resp['selectedPattern']}"
    arr = [4, 8, 3, 7, 2]
    expected = oracle_next_smaller_element(arr)
    got = parse_output_list(compile_and_run_cpp(resp["generatedCode"], list_to_input(arr)))
    assert got == expected, f"BH-03: expected {expected}, got {got}"
    return True


@holdout("BH-04",
    "River levels: previous lower water level to the left")
def bh04():
    text = (
        "Given river water levels recorded daily, for each day find the most recent "
        "previous day when the water level was strictly lower. Output -1 if no such day exists."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "previous_smaller_element", f"Wrong: {resp['selectedPattern']}"
    arr = [5, 3, 7, 4, 8]
    expected = oracle_previous_smaller_element(arr)
    got = parse_output_list(compile_and_run_cpp(resp["generatedCode"], list_to_input(arr)))
    assert got == expected, f"BH-04: expected {expected}, got {got}"
    return True


@holdout("BH-05",
    "Market streak: consecutive days stock did not exceed today's price (stock span paraphrase)")
def bh05():
    text = (
        "In a stock market, the 'streak' of a given day is the number of consecutive "
        "recent days (ending at and including today) for which the closing price "
        "was not higher than today's closing price. Compute the streak for each day."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "stock_span", f"Wrong: {resp['selectedPattern']}"
    arr = [60, 70, 60, 80, 90, 50, 85]
    expected = oracle_stock_span(arr)
    got = parse_output_list(compile_and_run_cpp(resp["generatedCode"], list_to_input(arr)))
    assert got == expected, f"BH-05: expected {expected}, got {got}"
    return True


@holdout("BH-06",
    "Fence sections: largest rectangular fence section from varying plank heights")
def bh06():
    text = (
        "You have a fence made of N planks in a row, each with a given height. "
        "All planks have width 1. Find the maximum area of a rectangular section "
        "you can cut out of the fence (the section must be contiguous and bounded above by the plank heights)."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "largest_rectangle_histogram", f"Wrong: {resp['selectedPattern']}"
    arr = [3, 6, 5, 4, 4, 1, 2]
    expected = oracle_largest_rectangle_histogram(arr)
    got = parse_output_scalar(compile_and_run_cpp(resp["generatedCode"], list_to_input(arr)))
    assert got == expected, f"BH-06: expected {expected}, got {got}"
    return True


@holdout("BH-07",
    "Circular temperature ring: next warmer in circular arrangement")
def bh07():
    text = (
        "Cities are arranged in a circle. For each city, find the temperature of "
        "the first city you reach (going clockwise) that has a higher temperature. "
        "Output -1 if no such city exists."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "circular_next_greater", f"Wrong: {resp['selectedPattern']}"
    arr = [5, 3, 4, 6, 2]
    expected = oracle_circular_next_greater(arr)
    got = parse_output_list(compile_and_run_cpp(resp["generatedCode"], list_to_input(arr)))
    assert got == expected, f"BH-07: expected {expected}, got {got}"
    return True


@holdout("BH-08",
    "Cost accounting: sum of minimums of all expense subarrays")
def bh08():
    text = (
        "A company tracks daily expenses in an array. For every contiguous period of days, "
        "record the minimum daily expense during that period. "
        "Return the total across all periods, modulo 10^9+7."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "sum_subarray_minimums", f"Wrong: {resp['selectedPattern']}"
    arr = rng_arr(n=9, lo=1, hi=20, seed=808)
    expected = oracle_sum_subarray_minimums(arr)
    got = parse_output_scalar(compile_and_run_cpp(resp["generatedCode"], list_to_input(arr)))
    assert got == expected, f"BH-08: expected {expected}, got {got}"
    return True


@holdout("BH-09",
    "Peak revenues: sum of peak revenues over all contiguous periods")
def bh09():
    text = (
        "Given an array of daily revenues, for every contiguous range of days, "
        "determine the maximum daily revenue in that range. "
        "Return the sum of all such maximum values modulo 10^9+7."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success", f"Expected success: {resp['status']}"
    assert resp["selectedPattern"] == "sum_subarray_maximums", f"Wrong: {resp['selectedPattern']}"
    arr = rng_arr(n=9, lo=1, hi=25, seed=909)
    expected = oracle_sum_subarray_maximums(arr)
    got = parse_output_scalar(compile_and_run_cpp(resp["generatedCode"], list_to_input(arr)))
    assert got == expected, f"BH-09: expected {expected}, got {got}"
    return True


@holdout("BH-10",
    "Anti-pattern: point update + next-greater query — should reject")
def bh10():
    text = (
        "Given an array, support two operations in any order: "
        "(1) set arr[pos] = val (update), and "
        "(2) query for the next greater element starting from index i. "
        "There are up to Q operations."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "rejected", f"Expected rejection (dynamic updates), got {resp['status']}"
    return True


def run_holdout(verbose=True):
    import time
    passed = 0
    failed = 0
    errors = []
    start_total = time.time()

    for p in HOLDOUT:
        pid = p["id"]
        desc = p["description"]
        runner = p["runner"]
        start = time.time()
        try:
            result = runner()
            elapsed = time.time() - start
            if result:
                passed += 1
                if verbose:
                    print(f"  ✓ {pid} {desc[:65]} ({elapsed:.2f}s)")
        except Exception as e:
            elapsed = time.time() - start
            failed += 1
            err = str(e)[:200]
            errors.append((pid, desc, err))
            if verbose:
                print(f"  ✗ {pid} {desc[:65]} — {err} ({elapsed:.2f}s)")

    total_elapsed = time.time() - start_total
    total = passed + failed
    print()
    print("=" * 70)
    print(f"  Blind Holdout Results: {passed}/{total} passed ({100*passed//total if total else 0}%)")
    print(f"  Total time: {total_elapsed:.2f}s")
    print("=" * 70)
    if errors:
        print("\n  FAILURES:")
        for pid, desc, err in errors:
            print(f"    [{pid}] {desc[:50]}: {err}")
    return passed, failed, errors


if __name__ == "__main__":
    print("CHUP Phase 3B — Monotonic Stack Blind Holdout")
    print("=" * 70)
    run_holdout()
