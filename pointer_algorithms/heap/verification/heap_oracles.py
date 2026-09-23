"""
Python Reference Oracles for Heap / Priority Queue Domain (Phase 3G).

Independent reference implementations for all 11 heap patterns.
Used for differential testing against generated C++17 implementations.
"""

import heapq
from typing import List, Tuple, Any, Optional, Union


def oracle_min_priority_queue(operations: List[Union[Tuple[str, int], str]]) -> List[str]:
    """
    Simulates a min-priority queue.
    Operations can be:
    - ("PUSH", val) or "PUSH val"
    - "POP" / "pop" -> extracts min
    - "TOP" / "top" -> peeks min
    """
    heap: List[int] = []
    output: List[str] = []

    for op in operations:
        if isinstance(op, tuple):
            cmd, val = op[0].upper(), op[1]
        else:
            parts = op.strip().split()
            cmd = parts[0].upper()
            val = int(parts[1]) if len(parts) > 1 else 0

        if cmd in ("PUSH", "INSERT"):
            heapq.heappush(heap, val)
        elif cmd in ("POP", "EXTRACT"):
            if heap:
                output.append(str(heapq.heappop(heap)))
            else:
                output.append("EMPTY")
        elif cmd in ("TOP", "PEEK"):
            if heap:
                output.append(str(heap[0]))
            else:
                output.append("EMPTY")

    return output


def oracle_max_priority_queue(operations: List[Union[Tuple[str, int], str]]) -> List[str]:
    """
    Simulates a max-priority queue using negated keys.
    """
    heap: List[int] = []
    output: List[str] = []

    for op in operations:
        if isinstance(op, tuple):
            cmd, val = op[0].upper(), op[1]
        else:
            parts = op.strip().split()
            cmd = parts[0].upper()
            val = int(parts[1]) if len(parts) > 1 else 0

        if cmd in ("PUSH", "INSERT"):
            heapq.heappush(heap, -val)
        elif cmd in ("POP", "EXTRACT"):
            if heap:
                output.append(str(-heapq.heappop(heap)))
            else:
                output.append("EMPTY")
        elif cmd in ("TOP", "PEEK"):
            if heap:
                output.append(str(-heap[0]))
            else:
                output.append("EMPTY")

    return output


def oracle_heap_build(arr: List[int], kind: str = "min") -> List[int]:
    """
    Converts array into a heap in O(N) time.
    Returns the array representation of the heap.
    """
    res = list(arr)
    if kind == "min":
        heapq.heapify(res)
    else:
        # Max-heap: in Python heapq is min-heap, but std::make_heap in C++ produces a valid max-heap
        # or min-heap depending on comparator. We verify the heap property:
        heapq._heapify_max(res)
    return res


def oracle_top_k(arr: List[int], k: int, direction: str = "largest") -> List[int]:
    """
    Retention Invariant:
    - Top-K largest: maintain min-heap of size K.
    - Top-K smallest: maintain max-heap of size K.
    Returns the top-K elements sorted descending (for largest) or ascending (for smallest).
    """
    if not arr or k <= 0:
        return []
    k = min(k, len(arr))

    if direction in ("largest", "max"):
        min_heap: List[int] = []
        for x in arr:
            if len(min_heap) < k:
                heapq.heappush(min_heap, x)
            elif x > min_heap[0]:
                heapq.heapreplace(min_heap, x)
        return sorted(min_heap, reverse=True)
    else:
        max_heap: List[int] = []
        for x in arr:
            if len(max_heap) < k:
                heapq.heappush(max_heap, -x)
            elif -x > max_heap[0]:
                heapq.heapreplace(max_heap, -x)
        return sorted([-x for x in max_heap])


def oracle_kth_element(arr: List[int], k: int, direction: str = "largest") -> int:
    """
    Finds the K-th largest or K-th smallest element.
    """
    top_k = oracle_top_k(arr, k, direction)
    return top_k[-1] if top_k else 0


def oracle_k_way_merge(streams: List[List[int]]) -> List[int]:
    """
    Merges K sorted streams using a min-heap on the K-way frontier.
    """
    heap: List[Tuple[int, int, int]] = []
    for stream_idx, stream in enumerate(streams):
        if stream:
            heapq.heappush(heap, (stream[0], stream_idx, 0))

    result: List[int] = []
    while heap:
        val, stream_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        if elem_idx + 1 < len(streams[stream_idx]):
            heapq.heappush(heap, (streams[stream_idx][elem_idx + 1], stream_idx, elem_idx + 1))

    return result


def oracle_two_heaps(elements: List[int]) -> List[float]:
    """
    Maintains dual heaps (max-heap low, min-heap high) and records median at each step.
    """
    low: List[int] = []   # max-heap via negative numbers
    high: List[int] = []  # min-heap
    medians: List[float] = []

    for x in elements:
        if not low or x <= -low[0]:
            heapq.heappush(low, -x)
        else:
            heapq.heappush(high, x)

        # Balance sizes: 0 <= |low| - |high| <= 1
        if len(low) > len(high) + 1:
            heapq.heappush(high, -heapq.heappop(low))
        elif len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))

        if len(low) > len(high):
            medians.append(float(-low[0]))
        else:
            medians.append((-low[0] + high[0]) / 2.0)

    return medians


def oracle_dynamic_median(elements: List[int]) -> List[Union[int, float]]:
    """
    Dynamic median: returns integer if whole, float otherwise.
    """
    raw_meds = oracle_two_heaps(elements)
    res: List[Union[int, float]] = []
    for m in raw_meds:
        if m == int(m):
            res.append(int(m))
        else:
            res.append(round(m, 1))
    return res


def oracle_scheduling(intervals: List[Tuple[int, int]]) -> int:
    """
    Meeting rooms: computes minimum number of conference rooms required.
    """
    if not intervals:
        return 0
    sorted_ivs = sorted(intervals, key=lambda x: (x[0], x[1]))
    rooms_heap: List[int] = []  # stores end times

    max_rooms = 0
    for start, end in sorted_ivs:
        while rooms_heap and rooms_heap[0] <= start:
            heapq.heappop(rooms_heap)
        heapq.heappush(rooms_heap, end)
        max_rooms = max(max_rooms, len(rooms_heap))

    return max_rooms


def oracle_greedy_selection(weights: List[int]) -> int:
    """
    Connect ropes / Huffman combination: repeatedly merges two smallest elements.
    """
    if not weights or len(weights) <= 1:
        return 0
    heap = list(weights)
    heapq.heapify(heap)

    total_cost = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        merged = a + b
        total_cost += merged
        heapq.heappush(heap, merged)

    return total_cost


def oracle_lazy_deletion(operations: List[Tuple[str, Optional[int]]]) -> List[str]:
    """
    Priority queue with lazy deletion tracking via frequency count.
    Operations:
    - ("INSERT", x)
    - ("DELETE", x)
    - ("GET_MAX", None)
    - ("EXTRACT_MAX", None)
    """
    heap: List[int] = []  # max-heap via negative
    counts: dict[int, int] = {}
    output: List[str] = []

    for op, val in operations:
        cmd = op.upper()
        if cmd in ("INSERT", "PUSH") and val is not None:
            heapq.heappush(heap, -val)
            counts[val] = counts.get(val, 0) + 1
        elif cmd in ("DELETE", "REMOVE") and val is not None:
            if counts.get(val, 0) > 0:
                counts[val] -= 1
        elif cmd in ("GET_MAX", "TOP"):
            while heap and counts.get(-heap[0], 0) == 0:
                heapq.heappop(heap)
            if heap:
                output.append(str(-heap[0]))
            else:
                output.append("EMPTY")
        elif cmd in ("EXTRACT_MAX", "POP"):
            while heap and counts.get(-heap[0], 0) == 0:
                heapq.heappop(heap)
            if heap:
                mx = -heapq.heappop(heap)
                counts[mx] -= 1
                output.append(str(mx))
            else:
                output.append("EMPTY")

    return output
