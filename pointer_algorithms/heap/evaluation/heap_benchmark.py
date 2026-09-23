"""
CHUP Phase 3G — Heap / Priority Queue Domain Benchmark.

Evaluates Heap recognition, invariant verification, code generation,
and execution across 14 categories (3G-A through 3G-N, 56 problems):

3G-A: Min-Priority Queue (H-01..H-04)
3G-B: Max-Priority Queue (H-05..H-08)
3G-C: Bottom-Up Heap Construction (H-09..H-12)
3G-D: Top-K Largest Elements (H-13..H-16)
3G-E: Top-K Smallest Elements (H-17..H-20)
3G-F: K-th Extremal Element (H-21..H-24)
3G-G: K-Way Stream Merge (H-25..H-28)
3G-H: Two-Heaps Partitioning (H-29..H-32)
3G-I: Dynamic Median of Data Stream (H-33..H-36)
3G-J: Task & Resource Scheduling (H-37..H-40)
3G-K: Greedy Extremal Selection (H-41..H-44)
3G-L: Lazy Deletion & Tombstones (H-45..H-48)
3G-M: Bounded Stream Memory (H-49..H-52)
3G-N: Anti-Patterns & Elimination (H-53..H-56)
"""

import sys
import os
import subprocess
import tempfile
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request
from pointer_algorithms.recognition.feature_extractor import FeatureExtractor
from pointer_algorithms.recognition.candidate_generator import CandidateGenerator
from pointer_algorithms.recognition.candidate_eliminator import CandidateEliminator

COMPILED_BINARIES: Dict[str, str] = {}


import hashlib

def compile_and_run_cpp(code: str, stdin_data: str, pattern: str = "", timeout: int = 10) -> str:
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


BENCHMARK_PROBLEMS = [
    # ── 3G-A: Min-Priority Queue (H-01..H-04) ──
    {
        "id": "H-01",
        "category": "3G-A. Min-Priority Queue",
        "text": "Given a sequence of operations on a min-priority queue, execute push, pop, and top operations.",
        "expected_pattern": "heap_min_priority_queue",
        "input": "5\nPUSH 10\nPUSH 5\nPUSH 20\nPOP\nTOP\n",
        "oracle_check": lambda out: out.split() == ["5", "10"]
    },
    {
        "id": "H-02",
        "category": "3G-A. Min-Priority Queue",
        "text": "Maintain a min-heap structure. Insert elements and repeatedly extract minimum.",
        "expected_pattern": "heap_min_priority_queue",
        "input": "4\ninsert 42\ninsert 7\nextract\nextract\n",
        "oracle_check": lambda out: out.split() == ["7", "42"]
    },
    {
        "id": "H-03",
        "category": "3G-A. Min-Priority Queue",
        "text": "Process priority queue min-heap queries with negative and positive values.",
        "expected_pattern": "heap_min_priority_queue",
        "input": "4\nPUSH -5\nPUSH -10\nPOP\nPOP\n",
        "oracle_check": lambda out: out.split() == ["-10", "-5"]
    },
    {
        "id": "H-04",
        "category": "3G-A. Min-Priority Queue",
        "text": "Check minimum element in a dynamic min-heap without removing it using peek operation.",
        "expected_pattern": "heap_min_priority_queue",
        "input": "3\nPUSH 15\nPUSH 3\nTOP\n",
        "oracle_check": lambda out: out.strip() == "3"
    },

    # ── 3G-B: Max-Priority Queue (H-05..H-08) ──
    {
        "id": "H-05",
        "category": "3G-B. Max-Priority Queue",
        "text": "Execute push, pop, and top operations on a max-priority queue (maximum heap).",
        "expected_pattern": "heap_max_priority_queue",
        "input": "5\nPUSH 10\nPUSH 5\nPUSH 20\nPOP\nTOP\n",
        "oracle_check": lambda out: out.split() == ["20", "10"]
    },
    {
        "id": "H-06",
        "category": "3G-B. Max-Priority Queue",
        "text": "Maintain a max-heap priority queue. Extract maximum elements in descending order.",
        "expected_pattern": "heap_max_priority_queue",
        "input": "4\ninsert 8\ninsert 99\nextract\nextract\n",
        "oracle_check": lambda out: out.split() == ["99", "8"]
    },
    {
        "id": "H-07",
        "category": "3G-B. Max-Priority Queue",
        "text": "Max-priority queue handling negative values where maximum is closest to zero.",
        "expected_pattern": "heap_max_priority_queue",
        "input": "4\nPUSH -20\nPUSH -5\nPOP\nPOP\n",
        "oracle_check": lambda out: out.split() == ["-5", "-20"]
    },
    {
        "id": "H-08",
        "category": "3G-B. Max-Priority Queue",
        "text": "Peek maximum value from max-heap without extracting.",
        "expected_pattern": "heap_max_priority_queue",
        "input": "3\nPUSH 50\nPUSH 100\nTOP\n",
        "oracle_check": lambda out: out.strip() == "100"
    },

    # ── 3G-C: Bottom-Up Heap Construction (H-09..H-12) ──
    {
        "id": "H-09",
        "category": "3G-C. Bottom-Up Heap Construction",
        "text": "Convert an arbitrary array into a valid binary heap using linear time bottom-up heapify.",
        "expected_pattern": "heap_build",
        "input": "5\n9 4 7 1 3\n",
        "oracle_check": lambda out: int(out.split()[0]) == 1  # Root must be minimum
    },
    {
        "id": "H-10",
        "category": "3G-C. Bottom-Up Heap Construction",
        "text": "Perform Floyd heapify on an array to build a min-heap in O(N) linear time.",
        "expected_pattern": "heap_build",
        "input": "6\n12 11 13 5 6 7\n",
        "oracle_check": lambda out: int(out.split()[0]) == 5
    },
    {
        "id": "H-11",
        "category": "3G-C. Bottom-Up Heap Construction",
        "text": "Build heap from an already sorted array in linear time.",
        "expected_pattern": "heap_build",
        "input": "4\n1 2 3 4\n",
        "oracle_check": lambda out: int(out.split()[0]) == 1
    },
    {
        "id": "H-12",
        "category": "3G-C. Bottom-Up Heap Construction",
        "text": "Bottom-up heapify on array with duplicates.",
        "expected_pattern": "heap_build",
        "input": "5\n5 2 5 2 5\n",
        "oracle_check": lambda out: int(out.split()[0]) == 2
    },

    # ── 3G-D: Top-K Largest Elements (H-13..H-16) ──
    {
        "id": "H-13",
        "category": "3G-D. Top-K Largest Elements",
        "text": "Find the top K largest elements in an unsorted stream using a bounded min-heap.",
        "expected_pattern": "heap_top_k",
        "input": "6 3\n3 2 1 5 6 4\n",
        "oracle_check": lambda out: out.split() == ["6", "5", "4"]
    },
    {
        "id": "H-14",
        "category": "3G-D. Top-K Largest Elements",
        "text": "Extract top K largest numbers from an integer array of size N.",
        "expected_pattern": "heap_top_k",
        "input": "5 2\n10 50 20 40 30\n",
        "oracle_check": lambda out: out.split() == ["50", "40"]
    },
    {
        "id": "H-15",
        "category": "3G-D. Top-K Largest Elements",
        "text": "Top-K largest elements when K equals 1.",
        "expected_pattern": "heap_top_k",
        "input": "4 1\n7 2 9 4\n",
        "oracle_check": lambda out: out.strip() == "9"
    },
    {
        "id": "H-16",
        "category": "3G-D. Top-K Largest Elements",
        "text": "Top K largest elements with duplicate values in stream.",
        "expected_pattern": "heap_top_k",
        "input": "5 3\n5 5 5 5 5\n",
        "oracle_check": lambda out: out.split() == ["5", "5", "5"]
    },

    # ── 3G-E: Top-K Smallest Elements (H-17..H-20) ──
    {
        "id": "H-17",
        "category": "3G-E. Top-K Smallest Elements",
        "text": "Find the K smallest elements in an incoming stream using bounded retention.",
        "expected_pattern": "heap_top_k",
        "input": "6 3\n7 10 4 3 20 15\n",
        "oracle_check": lambda out: set(out.split()) == {"3", "4", "7"}
    },
    {
        "id": "H-18",
        "category": "3G-E. Top-K Smallest Elements",
        "text": "Compute top K smallest integers from collection using max-heap of size K.",
        "expected_pattern": "heap_top_k",
        "input": "5 2\n8 2 5 1 9\n",
        "oracle_check": lambda out: set(out.split()) == {"1", "2"}
    },
    {
        "id": "H-19",
        "category": "3G-E. Top-K Smallest Elements",
        "text": "Find top K smallest elements with negative integers.",
        "expected_pattern": "heap_top_k",
        "input": "5 2\n0 -5 10 -20 3\n",
        "oracle_check": lambda out: set(out.split()) == {"-20", "-5"}
    },
    {
        "id": "H-20",
        "category": "3G-E. Top-K Smallest Elements",
        "text": "Top K smallest values when K equals array length N.",
        "expected_pattern": "heap_top_k",
        "input": "3 3\n3 1 2\n",
        "oracle_check": lambda out: set(out.split()) == {"1", "2", "3"}
    },

    # ── 3G-F: K-th Extremal Element (H-21..H-24) ──
    {
        "id": "H-21",
        "category": "3G-F. K-th Extremal Element",
        "text": "Find the K-th largest element in an array using min-heap of size K.",
        "expected_pattern": "heap_kth_element",
        "input": "6 2\n3 2 1 5 6 4\n",
        "oracle_check": lambda out: out.strip() == "5"
    },
    {
        "id": "H-22",
        "category": "3G-F. K-th Extremal Element",
        "text": "Determine the 4-th largest element in an unsorted stream of numbers.",
        "expected_pattern": "heap_kth_element",
        "input": "9 4\n3 2 3 1 2 4 5 5 6\n",
        "oracle_check": lambda out: out.strip() == "4"
    },
    {
        "id": "H-23",
        "category": "3G-F. K-th Extremal Element",
        "text": "Find the 1st largest element in sequence (maximum).",
        "expected_pattern": "heap_kth_element",
        "input": "4 1\n10 80 30 90\n",
        "oracle_check": lambda out: out.strip() == "90"
    },
    {
        "id": "H-24",
        "category": "3G-F. K-th Extremal Element",
        "text": "Find K-th largest element with all duplicate elements.",
        "expected_pattern": "heap_kth_element",
        "input": "4 2\n7 7 7 7\n",
        "oracle_check": lambda out: out.strip() == "7"
    },

    # ── 3G-G: K-Way Stream Merge (H-25..H-28) ──
    {
        "id": "H-25",
        "category": "3G-G. K-Way Stream Merge",
        "text": "Merge K sorted arrays into one sorted sequence using a min-heap priority frontier.",
        "expected_pattern": "heap_k_way_merge",
        "input": "3\n3 1 4 7\n3 2 5 8\n3 3 6 9\n",
        "oracle_check": lambda out: out.split() == ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    },
    {
        "id": "H-26",
        "category": "3G-G. K-Way Stream Merge",
        "text": "K-way merge with sorted lists of different lengths.",
        "expected_pattern": "heap_k_way_merge",
        "input": "3\n2 1 10\n4 2 3 7 8\n1 5\n",
        "oracle_check": lambda out: out.split() == ["1", "2", "3", "5", "7", "8", "10"]
    },
    {
        "id": "H-27",
        "category": "3G-G. K-Way Stream Merge",
        "text": "Merge K sorted streams containing empty stream.",
        "expected_pattern": "heap_k_way_merge",
        "input": "2\n2 1 3\n2 2 4\n",
        "oracle_check": lambda out: out.split() == ["1", "2", "3", "4"]
    },
    {
        "id": "H-28",
        "category": "3G-G. K-Way Stream Merge",
        "text": "Merge K sorted sequences with duplicate values across lists.",
        "expected_pattern": "heap_k_way_merge",
        "input": "2\n2 2 2\n2 2 2\n",
        "oracle_check": lambda out: out.split() == ["2", "2", "2", "2"]
    },

    # ── 3G-H: Two-Heaps Partitioning (H-29..H-32) ──
    {
        "id": "H-29",
        "category": "3G-H. Two-Heaps Partitioning",
        "text": "Partition incoming numbers into two halves using two heaps to balance stream dynamically.",
        "expected_pattern": "heap_two_heaps",
        "input": "4\n5\n15\n1\n3\n",
        "oracle_check": lambda out: len(out.split()) == 4
    },
    {
        "id": "H-30",
        "category": "3G-H. Two-Heaps Partitioning",
        "text": "Two heaps maintaining lower and upper quantile balance across dynamic insertions.",
        "expected_pattern": "heap_two_heaps",
        "input": "3\n10\n20\n30\n",
        "oracle_check": lambda out: out.split()[-1] == "20"
    },
    {
        "id": "H-31",
        "category": "3G-H. Two-Heaps Partitioning",
        "text": "Dual heaps balance with descending arrival order.",
        "expected_pattern": "heap_two_heaps",
        "input": "3\n30\n20\n10\n",
        "oracle_check": lambda out: out.split()[-1] == "20"
    },
    {
        "id": "H-32",
        "category": "3G-H. Two-Heaps Partitioning",
        "text": "Two heaps partition invariant test with identical numbers.",
        "expected_pattern": "heap_two_heaps",
        "input": "4\n5\n5\n5\n5\n",
        "oracle_check": lambda out: out.split()[-1] == "5"
    },

    # ── 3G-I: Dynamic Median of Data Stream (H-33..H-36) ──
    {
        "id": "H-33",
        "category": "3G-I. Dynamic Median",
        "text": "Find median from data stream as new numbers arrive continuously.",
        "expected_pattern": "heap_dynamic_median",
        "input": "3\n1\n2\n3\n",
        "oracle_check": lambda out: out.split() == ["1", "1.5", "2"]
    },
    {
        "id": "H-34",
        "category": "3G-I. Dynamic Median",
        "text": "Maintain running median of an online stream of numbers.",
        "expected_pattern": "heap_dynamic_median",
        "input": "4\n5\n15\n1\n3\n",
        "oracle_check": lambda out: out.split() == ["5", "10", "5", "4"]
    },
    {
        "id": "H-35",
        "category": "3G-I. Dynamic Median",
        "text": "Dynamic median with negative integers in stream.",
        "expected_pattern": "heap_dynamic_median",
        "input": "3\n-1\n-2\n-3\n",
        "oracle_check": lambda out: out.split() == ["-1", "-1.5", "-2"]
    },
    {
        "id": "H-36",
        "category": "3G-I. Dynamic Median",
        "text": "Continuous median calculation for alternating values.",
        "expected_pattern": "heap_dynamic_median",
        "input": "4\n10\n1\n10\n1\n",
        "oracle_check": lambda out: out.split() == ["10", "5.5", "10", "5.5"]
    },

    # ── 3G-J: Task & Resource Scheduling (H-37..H-40) ──
    {
        "id": "H-37",
        "category": "3G-J. Task Scheduling",
        "text": "Compute minimum number of meeting rooms required for scheduled conference intervals.",
        "expected_pattern": "heap_scheduling",
        "input": "3\n0 30\n5 10\n15 20\n",
        "oracle_check": lambda out: out.strip() == "2"
    },
    {
        "id": "H-38",
        "category": "3G-J. Task Scheduling",
        "text": "Schedule tasks with start and end times to find minimum concurrent servers required.",
        "expected_pattern": "heap_scheduling",
        "input": "3\n7 10\n2 4\n1 5\n",
        "oracle_check": lambda out: out.strip() == "2"
    },
    {
        "id": "H-39",
        "category": "3G-J. Task Scheduling",
        "text": "Interval scheduling with all intervals overlapping simultaneously.",
        "expected_pattern": "heap_scheduling",
        "input": "3\n1 10\n2 9\n3 8\n",
        "oracle_check": lambda out: out.strip() == "3"
    },
    {
        "id": "H-40",
        "category": "3G-J. Task Scheduling",
        "text": "Meeting rooms with back-to-back non-overlapping meetings.",
        "expected_pattern": "heap_scheduling",
        "input": "3\n1 5\n5 10\n10 15\n",
        "oracle_check": lambda out: out.strip() == "1"
    },

    # ── 3G-K: Greedy Extremal Selection (H-41..H-44) ──
    {
        "id": "H-41",
        "category": "3G-K. Greedy Extremal Selection",
        "text": "Connect ropes with minimum cost by repeatedly combining two smallest ropes.",
        "expected_pattern": "heap_greedy_selection",
        "input": "4\n4 3 2 6\n",
        "oracle_check": lambda out: out.strip() == "29"
    },
    {
        "id": "H-42",
        "category": "3G-K. Greedy Extremal Selection",
        "text": "Minimum cost to connect sticks using greedy selection with a min-heap.",
        "expected_pattern": "heap_greedy_selection",
        "input": "3\n1 8 3\n",
        "oracle_check": lambda out: out.strip() == "16"
    },
    {
        "id": "H-43",
        "category": "3G-K. Greedy Extremal Selection",
        "text": "Huffman greedy choice combination of single pair.",
        "expected_pattern": "heap_greedy_selection",
        "input": "2\n5 10\n",
        "oracle_check": lambda out: out.strip() == "15"
    },
    {
        "id": "H-44",
        "category": "3G-K. Greedy Extremal Selection",
        "text": "Greedy merge cost with equal stick lengths.",
        "expected_pattern": "heap_greedy_selection",
        "input": "4\n2 2 2 2\n",
        "oracle_check": lambda out: out.strip() == "16"
    },

    # ── 3G-L: Lazy Deletion & Tombstones (H-45..H-48) ──
    {
        "id": "H-45",
        "category": "3G-L. Lazy Deletion",
        "text": "Support dynamic deletion in priority queue using lazy deletion with tombstone frequencies.",
        "expected_pattern": "heap_lazy_deletion",
        "input": "5\nINSERT 10\nINSERT 20\nDELETE 20\nGET_MAX\nEXTRACT_MAX\n",
        "oracle_check": lambda out: out.split() == ["10", "10"]
    },
    {
        "id": "H-46",
        "category": "3G-L. Lazy Deletion",
        "text": "Priority queue with lazy deletion where max element is repeatedly deleted and updated.",
        "expected_pattern": "heap_lazy_deletion",
        "input": "5\nINSERT 50\nINSERT 30\nDELETE 50\nINSERT 40\nGET_MAX\n",
        "oracle_check": lambda out: out.strip() == "40"
    },
    {
        "id": "H-47",
        "category": "3G-L. Lazy Deletion",
        "text": "Lazy deletion of non-top elements that subsequently surface to the root.",
        "expected_pattern": "heap_lazy_deletion",
        "input": "6\nINSERT 10\nINSERT 20\nINSERT 30\nDELETE 20\nEXTRACT_MAX\nGET_MAX\n",
        "oracle_check": lambda out: out.split() == ["30", "10"]
    },
    {
        "id": "H-48",
        "category": "3G-L. Lazy Deletion",
        "text": "Lazy deletion emptying the entire priority queue.",
        "expected_pattern": "heap_lazy_deletion",
        "input": "4\nINSERT 5\nDELETE 5\nGET_MAX\nEXTRACT_MAX\n",
        "oracle_check": lambda out: out.split() == ["EMPTY", "EMPTY"]
    },

    # ── 3G-M: Bounded Stream Memory (H-49..H-52) ──
    {
        "id": "H-49",
        "category": "3G-M. Bounded Stream Memory",
        "text": "Process a stream of elements to maintain top K largest in O(K) space.",
        "expected_pattern": "heap_top_k",
        "input": "8 3\n1 10 2 9 3 8 4 7\n",
        "oracle_check": lambda out: out.split() == ["10", "9", "8"]
    },
    {
        "id": "H-50",
        "category": "3G-M. Bounded Stream Memory",
        "text": "Find K-th largest in high throughput stream.",
        "expected_pattern": "heap_kth_element",
        "input": "7 3\n10 20 30 40 50 60 70\n",
        "oracle_check": lambda out: out.strip() == "50"
    },
    {
        "id": "H-51",
        "category": "3G-M. Bounded Stream Memory",
        "text": "Continuous stream median computation with 5 values.",
        "expected_pattern": "heap_dynamic_median",
        "input": "5\n100\n200\n50\n25\n300\n",
        "oracle_check": lambda out: out.split()[-1] == "100"
    },
    {
        "id": "H-52",
        "category": "3G-M. Bounded Stream Memory",
        "text": "Merge 4 sorted streams in bounded frontier memory.",
        "expected_pattern": "heap_k_way_merge",
        "input": "4\n1 1\n1 2\n1 3\n1 4\n",
        "oracle_check": lambda out: out.split() == ["1", "2", "3", "4"]
    },

    # ── 3G-N: Anti-Patterns & Elimination (H-53..H-56) ──
    {
        "id": "H-53",
        "category": "3G-N. Anti-Patterns",
        "text": "Maintain collection supporting arbitrary element deletion and search for arbitrary key X by value.",
        "expected_elimination": "HEAP_ARBITRARY_DELETE_MISMATCH",
        "target_candidate": "heap_min_priority_queue"
    },
    {
        "id": "H-54",
        "category": "3G-N. Anti-Patterns",
        "text": "Sort the entire array offline in full lexicographical order.",
        "expected_elimination": "HEAP_UNNECESSARY_SORTING",
        "target_candidate": "heap_min_priority_queue"
    },
    {
        "id": "H-55",
        "category": "3G-N. Anti-Patterns",
        "text": "Maintain top K largest elements using a max-heap of size K.",
        "expected_elimination": "HEAP_WRONG_EXTREMUM",
        "target_candidate": "heap_top_k"
    },
    {
        "id": "H-56",
        "category": "3G-N. Anti-Patterns",
        "text": "Given a static array, find K-th element offline with K=10. Full sorting is unnecessary.",
        "expected_elimination": "HEAP_UNNECESSARY_SORTING",
        "target_candidate": "sorting"
    },
]


def run_benchmark():
    print("=" * 70)
    print("CHUP Phase 3G — Heap / Priority Queue Domain Benchmark (H-01 through H-56)")
    print("=" * 70)

    passed = 0
    total = len(BENCHMARK_PROBLEMS)

    for p in BENCHMARK_PROBLEMS:
        pid = p["id"]
        cat = p["category"]

        if "expected_elimination" in p:
            # Anti-pattern rejection test
            feat = FeatureExtractor.extract(p["text"])
            from pointer_algorithms.recognition.candidate_generator import AlgorithmCandidate
            cand = AlgorithmCandidate(
                pattern=p["target_candidate"],
                family="heap" if "heap" in p["target_candidate"] else "sorting",
                confidence_prior=0.9,
                supporting_signals=["max_heap"] if pid == "H-55" else []
            )
            eval_res = CandidateEliminator.evaluate_candidate(cand, feat)
            if not eval_res.accepted and eval_res.rejection_code == p["expected_elimination"]:
                print(f"  [PASS] {pid} ({cat}): Correctly eliminated {p['target_candidate']} with {p['expected_elimination']}")
                passed += 1
            else:
                print(f"  [FAIL] {pid} ({cat}): Expected rejection {p['expected_elimination']}, got accepted={eval_res.accepted}, code={eval_res.rejection_code}")
            continue

        resp = handle_request({"problemText": p["text"]})
        if resp.get("status") != "success":
            print(f"  [FAIL] {pid} ({cat}): Request status {resp.get('status')}, reason: {resp.get('reasoning')}")
            continue

        actual_pattern = resp.get("selectedPattern")
        if actual_pattern != p["expected_pattern"]:
            print(f"  [FAIL] {pid} ({cat}): Expected {p['expected_pattern']}, got {actual_pattern}")
            continue

        cpp_code = resp.get("code", "")
        out = compile_and_run_cpp(cpp_code, p["input"], pattern=actual_pattern)

        if out.startswith("COMPILE_ERROR") or out.startswith("RUNTIME_ERROR"):
            print(f"  [FAIL] {pid} ({cat}): Execution error: {out[:120]}")
            continue

        if p["oracle_check"](out):
            print(f"  [PASS] {pid} ({cat}): {actual_pattern} verified against oracle (output: {out[:40].strip()})")
            passed += 1
        else:
            print(f"  [FAIL] {pid} ({cat}): Output '{out[:40].strip()}' failed oracle check")

    print("=" * 70)
    score_pct = (passed / total) * 100
    print(f"Heap Benchmark Score: {passed}/{total} ({score_pct:.1f}%)")
    print("=" * 70)
    return passed == total


if __name__ == "__main__":
    success = run_benchmark()
    sys.exit(0 if success else 1)
