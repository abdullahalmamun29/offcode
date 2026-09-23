"""
Binary Search Blind Holdout — Phase 3C (BH-01 through BH-10)

10 problems NOT referenced during development, testing genuine generalization
over novel phrasings, unseen domains, and feasibility formulations.
"""

import sys
import os
import random
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.binary_search.evaluation.bs_benchmark import (
    compile_and_run_cpp, array_and_target_input, single_val_input, parse_int_output
)
from pointer_algorithms.binary_search.verification.bs_brute_force_oracles import (
    oracle_binary_search_exact,
    oracle_lower_bound,
    oracle_upper_bound,
    oracle_predecessor,
    oracle_successor,
    oracle_min_ship_capacity,
    oracle_max_min_distance,
    oracle_integer_sqrt,
)

HOLDOUT = []

def holdout(pid, desc):
    def decorator(fn):
        HOLDOUT.append({"id": pid, "description": desc, "runner": fn})
        return fn
    return decorator


@holdout("BH-01", "Warehouse barcode catalog: exact binary search in ascending serials")
def bh01():
    text = (
        "In an automated warehouse, item barcodes are cataloged in an array in ascending order. "
        "Search for the target barcode x using exact binary search. Output its index or -1 if not cataloged."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "binary_search_exact"
    catalog = [101, 204, 309, 412, 515, 620, 735]
    target = 412
    expected = oracle_binary_search_exact(catalog, target)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(catalog, target)))
    assert got == expected, f"BH-01 expected {expected}, got {got}"
    return True


@holdout("BH-02", "Elevator weight batches: minimum capacity to lift in K trips")
def bh02():
    text = (
        "Construction materials with given weights must be lifted to a high floor. "
        "Find the minimum elevator capacity to transport all materials in at most K trips."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "binary_search_answer_min"
    weights = [4, 8, 15, 16, 23, 42]
    trips = 3
    expected = oracle_min_ship_capacity(weights, trips)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(weights, trips)))
    assert got == expected, f"BH-02 expected {expected}, got {got}"
    return True


@holdout("BH-03", "Solar tracking posts: maximize minimum distance along highway")
def bh03():
    text = (
        "Solar monitoring posts are positioned at various milestones along a road. "
        "Activate K posts such that the minimum distance between any two active posts is maximized."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "binary_search_answer_max"
    milestones = [5, 12, 18, 29, 35, 41]
    k = 3
    expected = oracle_max_min_distance(milestones, k)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(milestones, k)))
    assert got == expected, f"BH-03 expected {expected}, got {got}"
    return True


@holdout("BH-04", "Network packet latency: lower bound threshold query")
def bh04():
    text = (
        "Packet round-trip latencies are stored in a sorted array. "
        "Compute the lower bound of latency target T: the first position where the latency is at least T."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "lower_bound"
    latencies = [12, 18, 25, 31, 45, 60]
    t = 28
    expected = oracle_lower_bound(latencies, t)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(latencies, t)))
    assert got == expected, f"BH-04 expected {expected}, got {got}"
    return True


@holdout("BH-05", "Sensor temperature limit: upper bound strictly greater query")
def bh05():
    text = (
        "Recorded sensor temperatures are sorted in non-decreasing order. "
        "Find the upper bound of safe temperature T: the first index where the temperature is strictly greater than T."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "upper_bound"
    temps = [20, 22, 24, 24, 24, 30, 35]
    limit = 24
    expected = oracle_upper_bound(temps, limit)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(temps, limit)))
    assert got == expected, f"BH-05 expected {expected}, got {got}"
    return True


@holdout("BH-06", "Factory order delivery: minimum speed in D days")
def bh06():
    text = (
        "A factory manufactures orders of varied sizes. "
        "Find the minimum speed of processing to deliver all orders within D days."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "binary_search_answer_min"
    orders = [10, 20, 15, 25, 30]
    days = 4
    expected = oracle_min_ship_capacity(orders, days)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(orders, days)))
    assert got == expected, f"BH-06 expected {expected}, got {got}"
    return True


@holdout("BH-07", "Satellite orbit altitude: predecessor strictly below target")
def bh07():
    text = (
        "Satellite altitudes are listed in ascending order. "
        "Find the predecessor altitude for a target ceiling x: the highest listed altitude strictly less than x."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "predecessor"
    altitudes = [350, 420, 500, 580, 650]
    ceiling = 520
    expected = oracle_predecessor(altitudes, ceiling)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(altitudes, ceiling)))
    assert got == expected, f"BH-07 expected {expected}, got {got}"
    return True


@holdout("BH-08", "Integer square root calculation on arbitrary integer")
def bh08():
    text = (
        "Given a non-negative integer n, compute the integer square root of n using binary search."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "binary_search_value_domain"
    n = 150
    expected = oracle_integer_sqrt(n)
    got = parse_int_output(compile_and_run_cpp(resp["code"], single_val_input(n)))
    assert got == expected, f"BH-08 expected {expected}, got {got}"
    return True


@holdout("BH-09", "Radio frequency band: successor strictly above target")
def bh09():
    text = (
        "Licensed frequencies are ordered in a sorted list. "
        "Find the successor frequency for frequency f: the lowest available frequency strictly greater than f."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "success"
    assert resp["selectedPattern"] == "successor"
    freqs = [88, 92, 98, 104, 108]
    f = 95
    expected = oracle_successor(freqs, f)
    got = parse_int_output(compile_and_run_cpp(resp["code"], array_and_target_input(freqs, f)))
    assert got == expected, f"BH-09 expected {expected}, got {got}"
    return True


@holdout("BH-10", "Anti-pattern: unsorted stream search rejected")
def bh10():
    text = (
        "Given an unsorted array of numbers, search for the target value using binary search without sorting."
    )
    resp = handle_request({"problemText": text})
    assert resp["status"] == "rejected", f"Expected rejection, got {resp['status']}"
    return True


def run_holdout(verbose=True):
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
            res = runner()
            elapsed = time.time() - start
            if res:
                passed += 1
                if verbose:
                    print(f"  ✓ {pid} {desc[:60]} ({elapsed:.2f}s)")
        except Exception as e:
            elapsed = time.time() - start
            failed += 1
            err = str(e)[:200]
            errors.append((pid, desc, err))
            if verbose:
                print(f"  ✗ {pid} {desc[:60]} — {err} ({elapsed:.2f}s)")

    total_elapsed = time.time() - start_total
    total = passed + failed
    print()
    print("=" * 70)
    print(f"  Binary Search Blind Holdout: {passed}/{total} passed ({100*passed//total if total else 0}%)")
    print(f"  Total time: {total_elapsed:.2f}s")
    print("=" * 70)

    if errors:
        print("\n  FAILURES:")
        for pid, desc, err in errors:
            print(f"    [{pid}] {desc[:50]}: {err}")

    return passed, failed, errors

if __name__ == "__main__":
    print("CHUP Phase 3C — Binary Search Blind Holdout")
    print("=" * 70)
    run_holdout()
