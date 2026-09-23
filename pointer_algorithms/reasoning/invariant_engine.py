"""
Invariant Engine for Pointer-Based Algorithms.

Explicitly generates and verifies the 4 phases of invariant reasoning:
1. Before iteration: Base precondition and starting search space.
2. During iteration: Property preserved across steps.
3. After movement: Exact formal argument of what candidate states were eliminated.
4. At termination: Why termination guarantees completeness and correctness.
"""

from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class FormalInvariant:
    pattern: str
    before_iteration: str
    during_iteration: str
    after_movement: str
    at_termination: str

class InvariantEngine:
    """Provides mathematically sound invariant specifications for pointer algorithms."""

    @staticmethod
    def construct_invariant(pattern: str, params: Dict[str, Any]) -> FormalInvariant:
        if pattern == "pair_sum_sorted":
            target = params.get("target", "T")
            return FormalInvariant(
                pattern=pattern,
                before_iteration=f"Array A is sorted in non-decreasing order. Initial indices L = 0, R = n - 1 contain all valid candidate pairs.",
                during_iteration=f"If there exists a pair (i, j) such that A[i] + A[j] == {target}, it must satisfy L <= i < j <= R.",
                after_movement=(
                    f"If A[L] + A[R] < {target}: because A is sorted, for every k < R, A[L] + A[k] <= A[L] + A[R] < {target}. "
                    f"Therefore L cannot be part of any pair summing to {target}. L is eliminated via L++.\n"
                    f"If A[L] + A[R] > {target}: similarly for every k > L, A[k] + A[R] >= A[L] + A[R] > {target}, so R is eliminated via R--."
                ),
                at_termination=f"L >= R implies all (n * (n - 1)) / 2 pair possibilities have either been tested or eliminated by monotonicity."
            )

        if pattern == "container_most_water":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="L = 0, R = n - 1. Max width is captured. Current max area initialized to 0.",
                during_iteration="The global maximum water container is either the maximum recorded so far or formed by a pair in [L, R].",
                after_movement=(
                    "Area is min(h[L], h[R]) * (R - L). If h[L] <= h[R]: for every k in (L, R), min(h[L], h[k]) * (k - L) "
                    "<= h[L] * (k - L) < h[L] * (R - L). Therefore, no pair (L, k) can strictly exceed area(L, R). "
                    "L is safely eliminated via L++. Symmetrically, if h[R] < h[L], R is safely eliminated via R--."
                ),
                at_termination="L >= R leaves no positive width interval. All candidate line pairs were safely evaluated or eliminated."
            )

        if pattern == "remove_duplicates_sorted":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="slow_write = 0, fast_read = 1. The prefix A[0..slow_write] trivially contains 1 unique element.",
                during_iteration="A[0..slow_write] contains all unique elements seen in A[0..fast_read-1] in original relative order.",
                after_movement=(
                    "If A[fast_read] != A[slow_write], a new unique element is found: slow_write is advanced and written. "
                    "If A[fast_read] == A[slow_write], it is a redundant duplicate and fast_read advances past it without writing."
                ),
                at_termination="fast_read == n. Prefix A[0..slow_write] contains all unique elements in the array; new length is slow_write + 1."
            )

        if pattern == "sliding_window_variable_max":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="L = 0, R = 0. Window state initialized. max_length = 0.",
                during_iteration="Window A[L..R-1] satisfies the validity constraint.",
                after_movement=(
                    "Upon adding A[R], if the window violates constraint, L is advanced and state updated until validity is restored. "
                    "Because validity is monotonic under shrinking, no longer valid subsegments starting prior to current L can exist ending at R. "
                    "Record max_length = max(max_length, R - L + 1) and advance R."
                ),
                at_termination="R reaches n. Every maximal valid window ending at each position R has been considered."
            )

        if pattern == "sliding_window_variable_min":
            target = params.get("target", "S")
            return FormalInvariant(
                pattern=pattern,
                before_iteration=f"L = 0, R = 0. Window sum = 0. min_length = infinity.",
                during_iteration=f"Window state maintains exact sum of A[L..R-1].",
                after_movement=(
                    f"Expand R by adding A[R]. While sum >= {target}, window A[L..R] is valid. "
                    f"Update min_length = min(min_length, R - L + 1), then remove A[L] and L++. "
                    f"Since all elements are non-negative, shrinking L monotonically decreases window sum, testing minimal valid spans."
                ),
                at_termination=f"R reaches n and all possible minimal valid starting endpoints L are exhausted."
            )

        if pattern == "partition_dutch_flag":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="low = 0, mid = 0, high = n - 1. Uninspected segment is [mid..high].",
                during_iteration=(
                    "Region 0: A[0..low-1] < pivot\n"
                    "Region 1: A[low..mid-1] == pivot\n"
                    "Region 2: A[high+1..n-1] > pivot\n"
                    "Uninspected: A[mid..high]"
                ),
                after_movement=(
                    "If A[mid] < pivot: swap(A[low], A[mid]), low++, mid++.\n"
                    "If A[mid] == pivot: mid++.\n"
                    "If A[mid] > pivot: swap(A[mid], A[high]), high-- (mid is not advanced as swapped value is uninspected)."
                ),
                at_termination="mid > high: Uninspected region is empty. All elements partitioned into regions 0, 1, 2."
            )

        if pattern == "linked_cycle_detection":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="slow = head, fast = head. Both start at same initial node.",
                during_iteration="If cycle of length C exists, relative distance (index(fast) - index(slow)) mod C increases by 1 each step.",
                after_movement="slow moves 1 step; fast moves 2 steps. The relative gap decreases by 1 step mod C. If fast meets slow, cycle detected.",
                at_termination="fast == slow implies cycle found; fast reaches null implies linear acyclic list."
            )

        if pattern == "palindrome_verification":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="lo = 0, hi = s.length() - 1. Pointers span the entire input sequence.",
                during_iteration="The prefix s[0..lo-1] and suffix s[hi+1..n-1] are verified reverse matches of each other.",
                after_movement=(
                    "Non-alphanumeric characters are bypassed without comparison. "
                    "If tolower(s[lo]) == tolower(s[hi]), symmetric equivalence is confirmed; lo++, hi-- inward. "
                    "If characters differ, symmetry violation disproves palindrome property."
                ),
                at_termination="lo >= hi implies all corresponding symmetric character pairs have matched."
            )

        if pattern == "in_place_compaction":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="slow_write = 0, fast_read = 0. Processed valid prefix is initially empty.",
                during_iteration="Prefix A[0..slow_write-1] contains all retained elements satisfying retention criteria in relative order.",
                after_movement=(
                    "If element at fast_read satisfies retention predicate, it is written to slow_write and slow_write advances. "
                    "fast_read advances to evaluate the next element, discarding rejected elements without overwriting."
                ),
                at_termination="fast_read reaches n. Prefix A[0..slow_write-1] contains the complete compacted sequence of length slow_write."
            )

        if pattern == "merge_sorted_arrays":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="p1 = 0, p2 = 0. Both source sequences are sorted in non-decreasing order.",
                during_iteration="The merged output prefix contains the smallest (p1 + p2) elements from both sequences in sorted order.",
                after_movement=(
                    "Compare A[p1] and B[p2]. The smaller element is placed into the output sequence, and its pointer is advanced. "
                    "Monotonicity guarantees that no unvisited element in either sequence is smaller than the chosen element."
                ),
                at_termination="Both source sequences are exhausted; all elements are merged in non-decreasing order."
            )

        if pattern == "partition_two_way":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="left = 0, right = n - 1. Uninspected elements lie in [left..right].",
                during_iteration="A[0..left-1] contains elements belonging to region 1, and A[right+1..n-1] contains elements belonging to region 2.",
                after_movement=(
                    "If A[left] belongs in region 1, left advances. "
                    "If A[right] belongs in region 2, right decrements. "
                    "If both are misplaced, swap(A[left], A[right]), resolving both misplacements simultaneously."
                ),
                at_termination="left > right. The uninspected interval is empty; array is partitioned into two contiguous regions."
            )

        if pattern == "linked_middle_node":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="slow = head, fast = head. Both start at the head of the linked list.",
                during_iteration="slow has traversed k nodes while fast has traversed 2k nodes (distance ratio 1:2).",
                after_movement="slow moves 1 step; fast moves 2 steps. The 1:2 traversal invariant is preserved.",
                at_termination="fast reaches the end of the list (null or last node); slow points precisely to the middle node."
            )

        if pattern == "linked_cycle_start":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Phase 1 detected meeting node inside cycle. ptr1 = head, ptr2 = meeting_node.",
                during_iteration="Distance from head to cycle start equals distance from meeting node to cycle start modulo cycle length.",
                after_movement="Both ptr1 and ptr2 advance by 1 step simultaneously.",
                at_termination="ptr1 == ptr2. Meeting point is mathematically proven to be the exact cycle entry node."
            )

        if pattern == "closest_pair_sum":
            target = params.get("target", "target")
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Array is sorted. L = 0, R = n - 1. closest_diff initialized to infinity.",
                during_iteration="Best pair sum found so far in examined space is recorded.",
                after_movement=(
                    f"If cur_sum < {target}, any k < R satisfies A[L] + A[k] <= A[L] + A[R] < {target}, meaning no pair with L can be closer without exceeding target. L++.\n"
                    f"If cur_sum > {target}, symmetrically R--. If cur_sum == {target}, distance 0 is optimal; terminate."
                ),
                at_termination="L >= R guarantees all candidate pairs have been bounded and optimal proximity is found."
            )

        if pattern in ("three_sum_converging", "four_sum_converging"):
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Array is sorted. Outer loops iterate over first elements; inner search uses two pointers L and R.",
                during_iteration="For fixed outer elements, inner converging pointers search for target complement.",
                after_movement="Inner L and R skip identical adjacent duplicate values to avoid redundant combinations and infinite loops.",
                at_termination="All unique non-descending tuples summing to target are exhaustively enumerated without duplicate outputs."
            )

        if pattern == "trapping_rain_water":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="left = 0, right = n - 1. left_max = 0, right_max = 0. total_water = 0.",
                during_iteration="At each step, the bounded water at the limiting side is strictly determined by min(left_max, right_max).",
                after_movement=(
                    "If height[left] < height[right]: left_max bounds water trapping above left. "
                    "If height[left] >= left_max, update left_max; else add left_max - height[left] to water. left++.\n"
                    "Else height[right] <= height[left]: right_max bounds right. "
                    "If height[right] >= right_max, update right_max; else add right_max - height[right] to water. right--."
                ),
                at_termination="left == right. Water column above every index has been accumulated without overcounting."
            )

        if pattern == "move_zeroes_ordered":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="slow = 0, fast = 0. Output prefix is empty.",
                during_iteration="A[0..slow-1] contains all non-zero elements encountered so far in their original relative order.",
                after_movement="If A[fast] != 0, write to A[slow++] and fast++; else fast++ skips zero without moving slow.",
                at_termination="fast reaches n. Fill trailing positions A[slow..n-1] with zeros in O(n - slow) operations."
            )

        if pattern == "chase_pointer_difference":
            diff = params.get("diff", "diff")
            return FormalInvariant(
                pattern=pattern,
                before_iteration=f"Array is sorted. i = 0, j = 1. Target difference is {diff}.",
                during_iteration=f"Both pointers advance monotonically rightward; pair difference A[j] - A[i] is evaluated.",
                after_movement=(
                    f"If A[j] - A[i] < {diff}, j++ to increase the difference.\n"
                    f"If A[j] - A[i] > {diff}, i++ to decrease the difference.\n"
                    f"If i == j, j++ to ensure distinct indices."
                ),
                at_termination="j reaches n without match implies no distinct index pair has difference diff."
            )

        if pattern == "count_pairs_less_than_k":
            k_val = params.get("k", "K")
            return FormalInvariant(
                pattern=pattern,
                before_iteration=f"Array is sorted. L = 0, R = n - 1. Total count = 0.",
                during_iteration=f"Counts valid pairs in sorted array summing strictly less than {k_val}.",
                after_movement=(
                    f"If A[L] + A[R] < {k_val}: because A is sorted, for all m in [L + 1, R], A[L] + A[m] <= A[L] + A[R] < {k_val}. "
                    f"Thus, all (R - L) pairs (L, m) are valid. Add (R - L) to count and L++.\n"
                    f"If A[L] + A[R] >= {k_val}: R cannot pair with any element >= L, so R--."
                ),
                at_termination="L >= R: all valid pairs strictly less than K have been counted in O(N) steps."
            )

        if pattern == "count_pairs_equal_k":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Array is sorted. L = 0, R = n - 1. count = 0.",
                during_iteration="Evaluates pairs with sum == target, grouping duplicate blocks to avoid missing or overcounting pairs.",
                after_movement=(
                    "If A[L] + A[R] == target:\n"
                    "  If A[L] == A[R]: all k elements in [L..R] are equal; add k * (k - 1) / 2 and break.\n"
                    "  Else: count occurrences l_cnt of A[L] and r_cnt of A[R]; add l_cnt * r_cnt; L += l_cnt, R -= r_cnt."
                ),
                at_termination="L >= R guarantees every identical value combination is accounted for."
            )

        if pattern == "count_subarrays_bounded":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="left = 0, right = 0, count = 0. Product/sum accumulator initialized.",
                during_iteration="For each right endpoint, left is the minimal valid index such that A[left..right] is valid.",
                after_movement=(
                    "Expand by incorporating A[right]. While state violates bound, shrink via left++.\n"
                    "All (right - left + 1) contiguous subarrays ending at right are valid. Add (right - left + 1) to count."
                ),
                at_termination="right reaches n: every contiguous valid subarray ending at each index is uniquely counted."
            )

        if pattern == "exact_count_derived":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Decompose exact constraint into monotonic at-most queries: exact(K) = atMost(K) - atMost(K - 1).",
                during_iteration="Each atMost(K) query runs an O(N) sliding window with monotonic validity.",
                after_movement="Sliding window adds (right - left + 1) valid subarrays at each step.",
                at_termination="Difference between the two monotonic counters yields the exact frequency count."
            )

        if pattern == "minimum_window_substring":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="left = 0, right = 0. Target frequency table initialized. match_count = 0.",
                during_iteration="Window S[left..right] expands until all target characters are matched (match_count == required_unique).",
                after_movement=(
                    "While match_count == required_unique: record minimal window length; "
                    "remove S[left] from window frequency; if window frequency drops below target, decrement match_count; left++."
                ),
                at_termination="right reaches |S|: minimum covering substring is identified in O(|S| + |T|) time."
            )

        # ── Monotonic Stack Invariants (Phase 3B) ──

        if pattern in ("next_greater_element", "circular_next_greater"):
            circular_note = " For circular variant, the array is traversed twice (2n) with index % n." if pattern == "circular_next_greater" else ""
            return FormalInvariant(
                pattern=pattern,
                before_iteration=(
                    "Stack is empty. result[] initialized to -1 for all indices. "
                    "Stack stores indices whose next greater element has not yet been found. "
                    "Invariant: values at stack indices are monotonically non-increasing (bottom to top)." + circular_note
                ),
                during_iteration=(
                    "For each index i (scanning left to right): "
                    "while stack is non-empty and arr[i] > arr[stack.top()], "
                    "pop the top and mark its next greater element as arr[i]."
                ),
                after_movement=(
                    "For each popped index j: arr[i] > arr[j] is confirmed. "
                    "Since we scan left to right, i is the FIRST index to the right of j satisfying arr[i] > arr[j]. "
                    "Proof of finality: any later candidate k > i would arrive further right; "
                    "therefore i is definitively the first. result[j] = arr[i]. "
                    "After popping, push i; stack invariant is restored."
                ),
                at_termination=(
                    "All remaining stack indices have no element to their right that is strictly greater. "
                    "Their result[] entries remain -1 (no next greater element exists)."
                )
            )

        if pattern == "next_smaller_element":
            return FormalInvariant(
                pattern=pattern,
                before_iteration=(
                    "Stack is empty. result[] initialized to -1 for all indices. "
                    "Stack stores indices seeking their next smaller element. "
                    "Invariant: values at stack indices are monotonically non-decreasing (bottom to top)."
                ),
                during_iteration=(
                    "For each index i (left to right): "
                    "while stack is non-empty and arr[i] < arr[stack.top()], pop and resolve."
                ),
                after_movement=(
                    "For each popped index j: arr[i] < arr[j] is confirmed. "
                    "i is the FIRST index to the right satisfying arr[i] < arr[j]. "
                    "result[j] = arr[i]. Push i; stack invariant restored."
                ),
                at_termination=(
                    "Remaining stack indices have no element to their right that is strictly smaller. "
                    "result[] entries remain -1."
                )
            )

        if pattern == "previous_greater_element":
            return FormalInvariant(
                pattern=pattern,
                before_iteration=(
                    "Stack is empty. result[] initialized to -1. "
                    "Scanning right to left (or equivalently, maintaining a decreasing stack left to right). "
                    "Before processing index i, stack holds candidates for previous-greater queries from i onward."
                ),
                during_iteration=(
                    "For each index i (right to left): "
                    "while stack is non-empty and arr[stack.top()] <= arr[i], pop (it can never be the answer for i or any index to i's right that we haven't processed). "
                    "If stack is non-empty: result[i] = arr[stack.top()]. Push i."
                ),
                after_movement=(
                    "Popped elements are dominated by arr[i]: they can never be the first greater element "
                    "to the left for any index we have not yet processed (i is larger). "
                    "The stack top after popping is definitively the previous greater of i."
                ),
                at_termination=(
                    "All indices processed. Indices whose result[] is -1 have no greater element to their left."
                )
            )

        if pattern == "previous_smaller_element":
            return FormalInvariant(
                pattern=pattern,
                before_iteration=(
                    "Stack is empty. result[] initialized to -1. "
                    "Stack maintains monotonically non-decreasing values for previous-smaller queries."
                ),
                during_iteration=(
                    "For each index i (left to right): "
                    "while stack non-empty and arr[stack.top()] >= arr[i], pop. "
                    "If stack non-empty: result[i] = arr[stack.top()]. Push i."
                ),
                after_movement=(
                    "Popped elements >= arr[i] cannot be the first smaller element to i's left. "
                    "arr[i] dominates them for all future queries from the right. "
                    "Stack top after popping is definitively the previous smaller of i."
                ),
                at_termination=(
                    "result[i] == -1 means no element to i's left is strictly smaller."
                )
            )

        if pattern in ("nearest_greater_element", "nearest_smaller_element"):
            relation = "greater" if "greater" in pattern else "smaller"
            return FormalInvariant(
                pattern=pattern,
                before_iteration=(
                    f"Two-pass computation: pass 1 finds previous {relation} (right-to-left or left-to-right), "
                    f"pass 2 finds next {relation} (left-to-right). "
                    f"Each pass uses a separate monotonic stack with the appropriate order invariant."
                ),
                during_iteration=(
                    f"Pass 1: for each i, pop while stack.top() does not satisfy the '{relation}' relation to arr[i], push i. "
                    f"Pass 2: symmetric direction."
                ),
                after_movement=(
                    f"For each pop in pass 1: definitively resolves previous {relation} for the popped index. "
                    f"For each pop in pass 2: definitively resolves next {relation}. "
                    f"Both boundaries established independently and correctly."
                ),
                at_termination=(
                    f"Combined: nearest_{relation}[i] = min(distance_to_prev, distance_to_next) for each i. "
                    f"Unresolved entries remain -1 (no such neighbor exists)."
                )
            )

        if pattern == "stock_span":
            return FormalInvariant(
                pattern=pattern,
                before_iteration=(
                    "Stack stores (price_index) with monotonically decreasing prices bottom-to-top. "
                    "span[] array to be filled."
                ),
                during_iteration=(
                    "For each day i: while stack non-empty and price[stack.top()] <= price[i], pop. "
                    "span[i] = i - stack.top() if stack non-empty, else i + 1. Push i."
                ),
                after_movement=(
                    "Popped days have price <= price[i], so they are 'dominated' by today's price from the left. "
                    "They cannot contribute to the span of any future day as a left boundary. "
                    "The surviving stack top is the nearest previous day where price was strictly greater."
                ),
                at_termination=(
                    "All spans computed in O(n). Each index pushed and popped at most once."
                )
            )

        if pattern == "largest_rectangle_histogram":
            return FormalInvariant(
                pattern=pattern,
                before_iteration=(
                    "Stack is empty. max_area = 0. "
                    "Stack stores bar indices with monotonically non-decreasing heights (bottom-to-top). "
                    "These are bars whose maximum-area rectangle is still 'active' (right boundary not yet found)."
                ),
                during_iteration=(
                    "For each bar i: while stack non-empty and height[i] < height[stack.top()]: "
                    "pop j = stack.top(). Width = i - stack.top_after_pop - 1 (or i if stack empty). "
                    "Area = height[j] * width. Update max_area. "
                    "After loop: push i."
                ),
                after_movement=(
                    "For popped bar j: height[i] < height[j] is the first such element to j's right "
                    "(next smaller element). The new stack top after popping is the previous smaller element to j's left. "
                    "Width = right_boundary - left_boundary - 1. "
                    "This is the maximal width where height[j] can be maintained. "
                    "Area = height[j] * width. No wider rectangle with height[j] is achievable."
                ),
                at_termination=(
                    "After the main loop, flush remaining stack using virtual right boundary n. "
                    "For each remaining bar j: left_boundary = new_stack_top (or -1 if empty). "
                    "Width = n - left_boundary - 1. Area = height[j] * width."
                )
            )

        if pattern in ("sum_subarray_minimums", "sum_subarray_maximums"):
            objective = "minimum" if pattern == "sum_subarray_minimums" else "maximum"
            rel_left = "strictly smaller" if pattern == "sum_subarray_minimums" else "strictly larger"
            rel_right = "smaller or equal" if pattern == "sum_subarray_minimums" else "larger or equal"
            return FormalInvariant(
                pattern=pattern,
                before_iteration=(
                    f"Two monotonic stack passes over the array. "
                    f"left[i] = distance from i to the nearest previous element that is {rel_left} than arr[i] "
                    f"(or i+1 if no such element exists). "
                    f"right[i] = distance from i to the nearest next element that is {rel_right} than arr[i] "
                    f"(or n-i if no such element exists). "
                    f"Strictness convention: left uses strict comparison, right uses non-strict (or vice versa), "
                    f"to avoid double-counting duplicate values."
                ),
                during_iteration=(
                    f"Pass 1 (left boundaries): monotonic stack scanning left to right. "
                    f"Pass 2 (right boundaries): monotonic stack scanning right to left. "
                    f"For each pop: resolve the boundary for the popped element."
                ),
                after_movement=(
                    f"Element arr[i] is the {objective} of exactly left[i] * right[i] subarrays. "
                    f"Its total contribution = arr[i] * left[i] * right[i]. "
                    f"Proof: all subarrays [l..r] where l in (i - left[i], i] and r in [i, i + right[i]) "
                    f"have arr[i] as their {objective} by construction of boundaries."
                ),
                at_termination=(
                    f"Sum = sum(arr[i] * left[i] * right[i]) for all i, modulo 10^9+7. "
                    f"Each element's contribution is determined exactly once."
                )
            )

        # ── Binary Search Invariants (Phase 3C) ──

        if pattern == "binary_search_exact":
            return FormalInvariant(
                pattern=pattern,
                before_iteration=(
                    "lo = 0, hi = n - 1. Invariant: If target element x exists in the sorted array A, "
                    "then x in A[lo..hi]."
                ),
                during_iteration=(
                    "Midpoint mid = lo + (hi - lo) / 2 is computed (overflow-safe). "
                    "Comparison between A[mid] and target determines if match is found or which half is eliminated."
                ),
                after_movement=(
                    "If A[mid] == target: exact target found at index mid. "
                    "If A[mid] < target: array is sorted, so for all k <= mid, A[k] <= A[mid] < target; "
                    "updating lo = mid + 1 preserves x in A[lo..hi]. "
                    "If A[mid] > target: for all k >= mid, A[k] >= A[mid] > target; "
                    "updating hi = mid - 1 preserves x in A[lo..hi]."
                ),
                at_termination="lo > hi: search interval is empty, proving target does not exist in array A (returns -1)."
            )

        if pattern in ("lower_bound", "first_true", "successor"):
            rel_note = "A[i] >= target" if pattern in ("lower_bound", "successor") else "P(i) == true"
            return FormalInvariant(
                pattern=pattern,
                before_iteration=(
                    f"lo = 0, hi = n. Invariant: For all k < lo, {rel_note} is FALSE. "
                    f"The first index satisfying {rel_note} lies in [lo..hi]."
                ),
                during_iteration=(
                    f"mid = lo + (hi - lo) / 2 is tested against predicate {rel_note}."
                ),
                after_movement=(
                    f"If {rel_note} holds at mid: mid is a candidate, and by monotonicity no index after mid "
                    f"can be the FIRST true; updating hi = mid eliminates (mid..hi] and preserves the invariant. "
                    f"If {rel_note} is false at mid: by monotonicity all k <= mid are also false; "
                    f"updating lo = mid + 1 eliminates [lo..mid] and preserves the invariant."
                ),
                at_termination=(
                    f"lo == hi: active interval has converged to a single index. "
                    f"lo is definitively the smallest index where {rel_note} holds (or n if none exists)."
                )
            )

        if pattern == "upper_bound":
            return FormalInvariant(
                pattern=pattern,
                before_iteration=(
                    "lo = 0, hi = n. Invariant: For all k < lo, A[k] <= target. "
                    "The first index satisfying A[k] > target lies in [lo..hi]."
                ),
                during_iteration="mid = lo + (hi - lo) / 2. Condition A[mid] > target is evaluated.",
                after_movement=(
                    "If A[mid] > target: updating hi = mid preserves that the first element > target is at or before mid. "
                    "If A[mid] <= target: all k <= mid have A[k] <= target by sorting; updating lo = mid + 1 maintains invariant."
                ),
                at_termination="lo == hi: lo is the smallest index where A[lo] > target (or n if none exists)."
            )

        if pattern in ("last_true", "predecessor", "first_false", "last_false"):
            cond_note = "A[i] < target" if pattern == "predecessor" else "P(i) == true"
            return FormalInvariant(
                pattern=pattern,
                before_iteration=(
                    f"lo = 0, hi = n - 1, ans = -1. Invariant: For all k > hi that were eliminated, {cond_note} is false. "
                    f"ans stores the greatest index known to satisfy {cond_note}."
                ),
                during_iteration=f"mid = lo + (hi - lo) / 2 is tested against condition {cond_note}.",
                after_movement=(
                    f"If {cond_note} holds at mid: ans = mid, lo = mid + 1 explores larger indices while recording mid. "
                    f"If false at mid: all k >= mid are false; hi = mid - 1 eliminates [mid..hi]."
                ),
                at_termination="lo > hi: ans is definitively the largest index satisfying the condition, or -1 if none."
            )

        if pattern == "binary_search_answer_min":
            return FormalInvariant(
                pattern=pattern,
                before_iteration=(
                    "Search space [lo, hi] bounds all possible answer values. "
                    "Invariant: Feasibility predicate is monotone false -> true. "
                    "The minimum feasible value lies in [lo..hi]."
                ),
                during_iteration=(
                    "mid = lo + (hi - lo) / 2 is evaluated via feasibility predicate in O(N). "
                    "Overflow safe arithmetic prevents midpoint overflow."
                ),
                after_movement=(
                    "If feasible(mid) == true: capacity mid can satisfy constraints; by monotonicity, minimal capacity is <= mid; "
                    "hi = mid eliminates (mid..hi] while preserving the minimal valid answer. "
                    "If feasible(mid) == false: capacity mid is insufficient; by monotonicity, all c <= mid are insufficient; "
                    "lo = mid + 1 eliminates [lo..mid]."
                ),
                at_termination="lo == hi: lo is the unique minimum value satisfying feasibility. All values < lo are provably infeasible."
            )

        if pattern == "binary_search_answer_max":
            return FormalInvariant(
                pattern=pattern,
                before_iteration=(
                    "Search space [lo, hi] bounds all possible answer values, ans = lo. "
                    "Invariant: Feasibility predicate is monotone true -> false. "
                    "The maximum feasible threshold lies in [lo..hi]."
                ),
                during_iteration=(
                    "mid = lo + (hi - lo) / 2 is evaluated via feasibility check (e.g. greedy placement) in O(N)."
                ),
                after_movement=(
                    "If feasible(mid) == true: threshold mid is achievable; ans = mid, lo = mid + 1 searches for larger thresholds. "
                    "If feasible(mid) == false: threshold mid is impossible; by monotonicity, all d >= mid are impossible; hi = mid - 1."
                ),
                at_termination="lo > hi: ans is the maximum feasible value. All values > ans are provably impossible."
            )

        if pattern == "binary_search_value_domain":
            return FormalInvariant(
                pattern=pattern,
                before_iteration=(
                    "Search space [lo, hi] covers the discrete domain. "
                    "Invariant: Function f(x) is monotonic. The target discrete boundary lies in [lo..hi]."
                ),
                during_iteration="mid = lo + (hi - lo) / 2. 64-bit arithmetic prevents overflow when computing f(mid).",
                after_movement=(
                    "If f(mid) satisfies inequality: record ans = mid, update interval to search for larger boundary. "
                    "Otherwise, eliminate half-space that violates inequality."
                ),
                at_termination="lo > hi: ans is the exact discrete floor/boundary value satisfying the arithmetic constraint."
            )

        # ── Trie Invariants (Phase 3D) ──
        if pattern == "trie_insert":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Root node represents empty string epsilon. Pointer curr = root.",
                during_iteration="curr represents prefix w[0..i-1]. Increment curr->pass_count++.",
                after_movement="Allocate child node if null, advance curr = curr->child[c], extending prefix to w[0..i].",
                at_termination="At word end, curr->word_count++ confirms word presence in dictionary with exact multiplicity."
            )

        if pattern == "trie_exact_search":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="curr = root. Invariant: path represents prefix w[0..i-1].",
                during_iteration="If curr->child[c] == null, word cannot exist in dictionary; return false immediately.",
                after_movement="Advance curr = curr->child[c].",
                at_termination="At word end, return curr != null && curr->word_count > 0."
            )

        if pattern == "trie_prefix_search":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="curr = root. Target is prefix P.",
                during_iteration="If curr->child[c] == null, no word in dictionary has P as a prefix.",
                after_movement="Advance curr = curr->child[c].",
                at_termination="At end of prefix, return curr != null && curr->pass_count > 0."
            )

        if pattern == "trie_prefix_count":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="curr = root. Dual counter pass_count tracks number of descendant words.",
                during_iteration="Verify edge existence for character c in prefix.",
                after_movement="Advance curr = curr->child[c].",
                at_termination="At prefix end, return curr->pass_count."
            )

        if pattern == "trie_word_count":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="curr = root. Dual counter word_count tracks exact word multiplicity.",
                during_iteration="Follow exact character edges of word.",
                after_movement="Advance curr = curr->child[c].",
                at_termination="At word end, return curr->word_count."
            )

        if pattern == "trie_deletion":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Check word existence (word_count > 0). If absent, deletion is a safe no-op.",
                during_iteration="Traverse word path decrementing curr->pass_count-- on each ancestor node.",
                after_movement="At word end, decrement curr->word_count--. Recursively prune child pointer if child->pass_count == 0.",
                at_termination="Instance removed; safe pruning invariant guarantees no other word's path is disconnected."
            )

        if pattern == "trie_longest_prefix":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="curr = root. Common prefix string initialized to empty.",
                during_iteration="Check if curr has exactly 1 non-null child and curr->word_count == 0.",
                after_movement="Append character to prefix and advance curr to unique child.",
                at_termination="Branching or word termination stops traversal; returned prefix is maximal common prefix."
            )

        if pattern in ("trie_max_xor_pair", "trie_max_xor_query"):
            return FormalInvariant(
                pattern=pattern,
                before_iteration="32-bit unsigned binary trie. Bit k descends from 31 down to 0.",
                during_iteration="Target bit is opposite = 1 - current_bit. Power-of-two strict dominance: 2^k > sum_{j=0}^{k-1} 2^j.",
                after_movement="If curr->child[opposite] exists, take it and accumulate (1 << k); else take curr->child[current_bit].",
                at_termination="Greedy choice guarantees globally maximal bitwise XOR without backtracking."
            )

        if pattern == "trie_lexicographic_sort":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="All strings inserted into Trie. DFS traversal begins at root.",
                during_iteration="Child edges traversed in ascending character order (0..25 or std::map order).",
                after_movement="Whenever visiting node with word_count > 0, emit string word_count times.",
                at_termination="All words emitted in strictly lexicographical order in O(total_characters) time."
            )

        if pattern == "trie_autocomplete":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Locate prefix node in Trie. If prefix absent, return empty list.",
                during_iteration="DFS from prefix node in ascending character order collecting completions.",
                after_movement="Append valid words (word_count > 0) to suggestions until requested limit.",
                at_termination="Returns lexicographically sorted completions sharing the specified prefix."
            )

        # ── Tree Invariants (Phase 3E) ──
        if pattern == "tree_dfs_preorder":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Traversal starts at tree root; visited call-stack initialized.",
                during_iteration="Node u is processed strictly before any node in its child subtrees T_v.",
                after_movement="Recurse to each child in order, completely traversing left/earlier subtrees before right/later subtrees.",
                at_termination="Every node in the connected tree is visited exactly once; preorder list has length N."
            )

        if pattern == "tree_dfs_inorder":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Applies to binary tree structure with root node.",
                during_iteration="For each node u, left subtree T_{u.left} is fully processed before u, and u before right subtree T_{u.right}.",
                after_movement="In-order symmetric walk preserves subtree key projection.",
                at_termination="All nodes processed; for a valid BST, the resulting sequence is strictly monotonic non-decreasing."
            )

        if pattern == "tree_dfs_postorder":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Bottom-up evaluation begins at tree leaves.",
                during_iteration="Node u is evaluated only after all child subtrees T_v have been fully computed.",
                after_movement="Inductive hypothesis: child states S(v) are mathematically correct before parent transition combine(u, {S(v)}).",
                at_termination="Root state is computed last, completing global tree aggregation in O(N) time."
            )

        if pattern == "tree_bfs_level_order":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Queue Q initialized with {root}; depth d = 0.",
                during_iteration="Q contains all nodes at tree distance d from root. Pop each node u and push its children.",
                after_movement="FIFO order guarantees all depth d nodes are visited before any depth d+1 node.",
                at_termination="Q becomes empty; nodes are partitioned strictly by tree level/distance."
            )

        if pattern == "tree_depth_height":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Null node base case defined as height -1 (or 0); leaf height is 0 (or 1).",
                during_iteration="height(u) = 1 + max_{v in children(u)} height(v).",
                after_movement="Postorder return passes longest path length from u to any descendant leaf to u's parent.",
                at_termination="Returns root height in O(N) time; correctly captures tree depth."
            )

        if pattern == "tree_subtree_size":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Null node has size 0; single leaf has size 1.",
                during_iteration="size(u) = 1 + sum_{v in children(u)} size(v).",
                after_movement="Each child subtree size is computed disjointly and summed into parent.",
                at_termination="size(root) equals total number of vertices N in the tree."
            )

        if pattern == "tree_leaf_count":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Null node returns 0; node with no children returns 1.",
                during_iteration="Internal node u returns sum of leaf counts of all its child subtrees.",
                after_movement="Non-leaf nodes contribute 0 directly, aggregating leaf indicators from children.",
                at_termination="Returns total count of leaves in tree in O(N) time."
            )

        if pattern == "tree_subtree_aggregation":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Associative aggregation operator defined with identity element e.",
                during_iteration="state(u) = combine(val[u], fold_{v in children(u)}(state(v))).",
                after_movement="Child states aggregated without overlap because subtrees in a tree are vertex-disjoint.",
                at_termination="Returns complete tree aggregate in exactly O(N) time."
            )

        if pattern == "tree_path_sum":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Path accumulator initialized with 0 or root value.",
                during_iteration="At node u, check if leaf and accumulated sum satisfies target; else pass updated sum to children.",
                after_movement="Unique path property: there exists exactly one simple path from root to any node u.",
                at_termination="All root-to-leaf paths evaluated in O(N) time without path duplication."
            )

        if pattern == "tree_diameter":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Global max diameter D initialized to 0.",
                during_iteration="At node u, find top two child branch depths d1 >= d2. Longest path through u is d1 + d2 (or d1 + d2 + 2 edges).",
                after_movement="Update D = max(D, path_through_u); return 1 + d1 to parent.",
                at_termination="D records the maximum distance between any pair of vertices in the tree."
            )

        if pattern == "tree_bst_search":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Input satisfies BST ordering invariant: left subtree < u < right subtree.",
                during_iteration="Compare search target k with u->val.",
                after_movement=(
                    "BST ordered-branch elimination: if k < u->val, target cannot reside in right subtree, so descend left. "
                    "If k > u->val, target cannot reside in left subtree, so descend right. If k == u->val, target found."
                ),
                at_termination="Returns target node or null; achieves O(H) complexity without examining eliminated branches."
            )

        if pattern == "tree_bst_insert":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Tree satisfies BST ordering invariant.",
                during_iteration="Navigate tree via BST ordered-branch elimination to locate vacant leaf insertion site.",
                after_movement="New node attached at appropriate leaf; preserves ancestor ordering constraints (low < val < high).",
                at_termination="Returns tree root; structure remains a valid BST."
            )

        if pattern == "tree_bst_delete":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Target key k to delete from valid BST.",
                during_iteration="Locate target node u via BST ordered-branch elimination.",
                after_movement=(
                    "Three-case elimination: (1) leaf: safely delete; (2) 1 child: link parent directly to child; "
                    "(3) 2 children: swap value with inorder successor (smallest node in right subtree), then delete successor."
                ),
                at_termination="Key removed; BST ordering invariants strictly preserved in all subtrees."
            )

        if pattern == "tree_bst_min_max":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Tree satisfies BST ordering invariant.",
                during_iteration="For minimum: follow strictly left child pointers; for maximum: follow strictly right child pointers.",
                after_movement="By BST invariant, no element in any right subtree can be smaller than current node.",
                at_termination="Leftmost node is global minimum; rightmost node is global maximum."
            )

        if pattern == "tree_bst_pred_succ":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Target key k; candidate predecessor/successor initialized to null.",
                during_iteration="Descend tree via BST ordered-branch elimination.",
                after_movement="When branching right, record u as candidate predecessor; when branching left, record u as candidate successor.",
                at_termination="Returns closest key smaller/larger than k in O(H) time."
            )

        if pattern == "tree_bst_validate":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Valid key range for root is (-infinity, +infinity).",
                during_iteration="Verify that current node value satisfies low < u->val < high (subject to duplicate policy).",
                after_movement="Left child bounded by (low, u->val); right child bounded by (u->val, high).",
                at_termination="Tree is valid BST if and only if all nodes satisfy their ancestor-derived bounds."
            )

        if pattern == "tree_lca_binary_tree":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Query nodes p and q in binary tree.",
                during_iteration="At node u, if u == p or u == q, return u. Recursively search left and right subtrees.",
                after_movement="If both left and right return non-null, u is the lowest common ancestor; if one is non-null, propagate it up.",
                at_termination="Returns lowest node having both p and q in its subtree in O(N) time."
            )

        if pattern == "tree_lca_bst":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Query nodes p and q in valid BST.",
                during_iteration="Compare p->val and q->val with u->val.",
                after_movement=(
                    "BST ordered-branch elimination: if both p, q < u->val, LCA lies in left subtree. "
                    "If both p, q > u->val, LCA lies in right subtree. "
                    "If p and q split across u (or one equals u), u is definitively the lowest common ancestor."
                ),
                at_termination="Discovers LCA in O(H) time without inspecting any other branch."
            )

        if pattern == "tree_lca_parent_array":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Parent pointers available; node depths precomputed or measured.",
                during_iteration="Lift deeper node upward until depth(u) == depth(v).",
                after_movement="Step both nodes upward simultaneously: u = parent[u], v = parent[v] until u == v.",
                at_termination="Meeting point is the lowest common ancestor; takes O(H) time."
            )

        if pattern == "tree_dp_independent_set":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Bottom-up postorder Tree DP; state (dp0, dp1) for each node.",
                during_iteration="dp1[u] = val[u] + sum_v dp0[v] (including u requires excluding all children); dp0[u] = sum_v max(dp0[v], dp1[v]).",
                after_movement="Disjoint subtrees guarantee optimal substructure and zero cycle dependency.",
                at_termination="Global maximum independent set weight is max(dp0[root], dp1[root])."
            )

        if pattern == "tree_dp_subtree_weight":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Postorder Tree DP for maximum contiguous subtree weight.",
                during_iteration="dp[u] = val[u] + sum_{v in children(u)} max(0, dp[v]).",
                after_movement="Greedy pruning: child subtrees with negative net contribution are safely omitted.",
                at_termination="Returns maximum weight contiguous subtree in O(N) time."
            )

        if pattern == "tree_dp_two_state":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Two-state tuple (state0(u), state1(u)) defined on subtree T_u.",
                during_iteration="Combine child state tuples according to problem's transition constraints.",
                after_movement="Subtree independence ensures no cross-branch state interference.",
                at_termination="Root state tuple yields optimal tree solution in O(N) time."
            )

        # ── Phase 3F: Graph Pattern Invariants ──

        if pattern == "graph_bfs_shortest_path":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Queue Q = [source]. dist[source] = 0. dist[v] = INF for all other v. Invariant: all vertices at hop-distance d are fully processed before any vertex at hop-distance d+1.",
                during_iteration="For each vertex u dequeued at layer d: dist[u] == d and is final (no shorter path exists by BFS layering property). For each neighbor v: if dist[v] == INF, set dist[v] = d+1 and enqueue v.",
                after_movement="Once v is enqueued at layer d+1, dist[v] is finalized. No shorter path from source to v exists because all d-layer vertices were processed before d+1-layer vertices.",
                at_termination="Q is empty iff all reachable vertices have been settled. dist[v] = minimum hop distance from source to v, or INF if unreachable."
            )

        if pattern == "graph_dfs_traversal":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="visited[v] = False for all v. Stack or recursion starts at source.",
                during_iteration="visited[u] = True marks u as reached. For each unvisited neighbor v: recurse into v, maintaining DFS tree edges.",
                after_movement="Once visited[u] = True, u is finalized and will not be revisited.",
                at_termination="All vertices reachable from source have visited[v] = True. DFS completes in O(V + E)."
            )

        if pattern == "graph_connected_components":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="visited[v] = False for all v. component_id[v] = -1. num_components = 0.",
                during_iteration="For each unvisited vertex u: start BFS/DFS, label all reachable vertices with current component_id, increment num_components.",
                after_movement="Each BFS/DFS from an unvisited vertex discovers exactly one new connected component.",
                at_termination="visited[v] = True for all v. num_components = total number of connected components. component_id[v] identifies the component of v."
            )

        if pattern == "graph_cycle_detection_undirected":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="visited[v] = False for all v. parent[v] = -1 (unset).",
                during_iteration="visited[u] = True. For each neighbor v of u: if visited[v] and v != parent[u], a back-edge (u, v) is found, forming a cycle.",
                after_movement="If v is unvisited, DFS recurses with parent[v] = u. If v is visited and v != parent[u], cycle confirmed immediately.",
                at_termination="If DFS completes without back-edges: graph is acyclic. Else: cycle exists. O(V + E)."
            )

        if pattern == "graph_cycle_detection_directed":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="color[v] = UNVISITED(0) for all v.",
                during_iteration="color[u] = VISITING(1) when DFS enters u. For each neighbor v: if color[v] == VISITING(1), back-edge found, cycle detected. If color[v] == UNVISITED(0), recurse.",
                after_movement="color[u] = VISITED(2) when DFS fully processes u. Back-edges to VISITING nodes are the only cycle indicators.",
                at_termination="If no back-edge found: DAG. Else: directed cycle exists. O(V + E)."
            )

        if pattern == "graph_bipartite_coloring":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="color[v] = -1 (uncolored) for all v.",
                during_iteration="color[source] = 0. For each edge (u, v): if color[v] == -1, set color[v] = 1 - color[u] and enqueue. If color[v] == color[u]: odd cycle detected, not bipartite.",
                after_movement="Coloring invariant: for every edge (u, v), color[u] != color[v]. Violation implies odd cycle.",
                at_termination="If all components successfully 2-colored: bipartite. Else: non-bipartite (contains odd cycle). O(V + E)."
            )

        if pattern == "graph_dijkstra":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="dist[source] = 0. dist[v] = INF for all other v. Priority queue PQ = {(0, source)}. settled = {} (empty set).",
                during_iteration="Extract min (d, u) from PQ. If u already in settled: skip. Mark u as settled with dist[u] = d (finalized). For each neighbor v with edge weight w: if d + w < dist[v], update dist[v] = d + w and push (dist[v], v) to PQ.",
                after_movement="Greedy invariant: once u is settled, dist[u] is the globally optimal shortest path from source to u. Proof: all edges have w >= 0, so no future path can improve dist[u].",
                at_termination="PQ empty: all reachable vertices are settled with optimal distances. dist[v] = shortest path length, or INF if unreachable. O((V + E) log V)."
            )

        if pattern == "graph_bellman_ford":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="dist[source] = 0. dist[v] = INF for all other v.",
                during_iteration="Repeat V-1 times: for each edge (u, v, w): if dist[u] + w < dist[v], relax dist[v] = dist[u] + w.",
                after_movement="After k rounds, dist[v] gives the shortest path from source to v using at most k edges. After V-1 rounds, dist[v] is optimal for graphs without negative cycles.",
                at_termination="If the V-th round still produces relaxations: a reachable negative cycle exists (shortest path undefined). Else: dist[v] = optimal shortest path lengths. O(V * E)."
            )

        if pattern == "graph_floyd_warshall":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="dist[i][j] = w(i,j) if edge (i,j) exists, 0 if i==j, INF otherwise.",
                during_iteration="For each intermediate vertex k (0 to V-1): for all pairs (i, j): if dist[i][k] + dist[k][j] < dist[i][j], update dist[i][j] = dist[i][k] + dist[k][j].",
                after_movement="Invariant: after processing intermediate set {0..k}, dist[i][j] = length of shortest path from i to j using only vertices in {0..k} as intermediates.",
                at_termination="dist[i][j] = all-pairs shortest path lengths. Negative cycle check: dist[i][i] < 0 for some i indicates a negative cycle through i. O(V^3)."
            )

        if pattern == "graph_topological_sort":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="in_degree[v] = number of incoming edges for all v. Queue Q = all v with in_degree[v] == 0.",
                during_iteration="Dequeue u (in_degree[u] == 0, safe to place first). For each out-neighbor v: decrement in_degree[v]. If in_degree[v] == 0, enqueue v.",
                after_movement="Invariant: vertex u can only be enqueued after all its predecessors are processed. The topological order is the dequeue sequence.",
                at_termination="If processed vertices < V: remaining vertices form a cycle (all have in-degree >= 1). Else: topological order is valid. O(V + E)."
            )

        if pattern == "graph_dag_dp":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Process vertices in topological order. dp[source] = 0 (or base case). dp[v] = INF (uncomputed) for all others.",
                during_iteration="For vertex u in topological order: for each out-neighbor v with edge weight w: if dp[u] + w improves dp[v], update dp[v].",
                after_movement="Once u is processed in topological order, dp[u] is finalized (no predecessor can update it later — DAG property).",
                at_termination="dp[v] = optimal path cost from source to v (e.g. shortest, longest, count) using DAG structure. O(V + E)."
            )

        if pattern == "graph_dsu":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="parent[v] = v for all v. rank[v] = 0 for all v. Each vertex is its own component.",
                during_iteration="find(x): follow parent pointers to root, applying path compression. union(x, y): find roots rx, ry. If rx != ry, merge smaller rank tree under larger rank root.",
                after_movement="Invariant: find(x) == find(y) iff x and y are in the same connected component. After each union, exactly one fewer component exists.",
                at_termination="After processing all union operations: components are correctly identified. find(x) == find(y) for any query in O(alpha(V)) amortized time."
            )

        if pattern == "graph_mst_kruskal":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Sort all edges by weight ascending. DSU initialized with V singleton components. MST edge set T = {}.",
                during_iteration="For each edge (u, v, w) in sorted order: if find(u) != find(v), add edge to T and union(u, v).",
                after_movement="Cut Property invariant: each added edge is the minimum-weight edge crossing the cut (T-component, V\\T-component) at the time of addition. Cycle is impossible: edges are only added between different components.",
                at_termination="T contains exactly V-1 edges forming the MST (if graph is connected). Total weight is minimal by Cut Property. O(E log E)."
            )

        if pattern == "graph_mst_prim":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="key[source] = 0. key[v] = INF for all other v. inMST[v] = False. PQ = {(0, source)}.",
                during_iteration="Extract min (k, u). Mark inMST[u] = True. For each neighbor v not in MST with edge weight w: if w < key[v], update key[v] = w, parent[v] = u, push (w, v) to PQ.",
                after_movement="Cut Property: key[v] = minimum edge weight connecting v to the current MST component. Each extracted vertex joins MST via the minimum cut edge.",
                at_termination="inMST[v] = True for all v (connected graph). MST edges = parent[] array. Total weight = sum of key[v]. O((V + E) log V)."
            )

        if pattern == "graph_scc_tarjan":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="tin[v] = low[v] = -1 (unvisited). on_stack[v] = False. stack = []. timer = 0.",
                during_iteration="DFS visit u: tin[u] = low[u] = timer++. Push u on stack, on_stack[u] = True. For each neighbor v: if unvisited, recurse, then low[u] = min(low[u], low[v]). If visited and on_stack[v]: low[u] = min(low[u], tin[v]).",
                after_movement="Invariant: low[u] is the minimum discovery time reachable from u's subtree via back-edges. When low[u] == tin[u], u is the root of an SCC.",
                at_termination="When DFS finishes u and low[u] == tin[u]: pop stack until u, yielding one SCC. All SCCs are discovered in reverse topological order of condensation DAG. O(V + E)."
            )

        if pattern == "graph_bridges_articulation":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="tin[v] = low[v] = -1. visited[v] = False. timer = 0. Bridges = []. Articulation_points = {}.",
                during_iteration="DFS visit u with parent p: tin[u] = low[u] = timer++. children = 0. For each neighbor v: if unvisited, children++, recurse with parent=u, then low[u] = min(low[u], low[v]). Bridge check: low[v] > tin[u]. AP check: root with children >= 2, or low[v] >= tin[u]. If v is visited and v != p: low[u] = min(low[u], tin[v]).",
                after_movement="low[u] reflects earliest reachable discovery time via back-edges. Bridge condition low[v] > tin[u] means v's subtree has no back-edge to u's ancestors.",
                at_termination="Bridges: all edges (u, v) with low[v] > tin[u]. Articulation points: DFS root with >= 2 children, or non-root with low[v] >= tin[u] for some child v. O(V + E)."
            )

        # ── Heap / Priority Queue Patterns (Phase 3G) ──

        if pattern == "heap_min_priority_queue":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Empty min-heap initialized. Heap size = 0.",
                during_iteration="Min-heap invariant: for every node i > 0, A[parent(i)] <= A[i]. Root A[0] is the minimum element in the priority queue.",
                after_movement="Insert: append at leaf index N and sift-up in O(log N). Extract: swap root with leaf N-1, pop leaf, sift-down root in O(log N). Heap property restored.",
                at_termination="Elements extracted in non-decreasing order. Total complexity O(M log N) for M push/pop operations."
            )

        if pattern == "heap_max_priority_queue":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Empty max-heap initialized. Heap size = 0.",
                during_iteration="Max-heap invariant: for every node i > 0, A[parent(i)] >= A[i]. Root A[0] is the maximum element in the priority queue.",
                after_movement="Insert: append at leaf index N and sift-up in O(log N). Extract: swap root with leaf N-1, pop leaf, sift-down root in O(log N). Heap property restored.",
                at_termination="Elements extracted in non-increasing order. Total complexity O(M log N) for M push/pop operations."
            )

        if pattern == "heap_build":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Unordered array A[0..N-1] of N elements. Leaves from index floor(N/2) to N-1 trivially satisfy heap property.",
                during_iteration="For index i decreasing from floor(N/2)-1 down to 0: apply sift-down on subtree rooted at i.",
                after_movement="After sift-down at step i, subtree rooted at i satisfies the heap invariant, assuming subtrees rooted at left(i) and right(i) already do.",
                at_termination="Entire array A[0..N-1] satisfies the heap invariant. Total complexity sum_{h} (N / 2^{h+1}) * O(h) = O(N) linear time."
            )

        if pattern == "heap_top_k":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Capacity bounded to K. Retention Invariant: to maintain the K largest elements, initialize a MIN-HEAP of size K.",
                during_iteration="Heap stores the K best elements seen so far from stream A[0..i-1]. Root min_heap.top() is the weakest of these K candidates.",
                after_movement="When element x arrives: if heap.size() < K, push x. Else if x > min_heap.top(), pop the weakest element and push x in O(log K). Weaker candidates are permanently eliminated.",
                at_termination="Heap contains precisely the K largest elements of the entire sequence in O(N log K) time and O(K) space."
            )

        if pattern == "heap_kth_element":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Bounded heap of capacity K. Min-heap for K-th largest; Max-heap for K-th smallest.",
                during_iteration="Root of the bounded heap maintains the exact current K-th extremal element among all processed candidates.",
                after_movement="Incoming element x replaces the root if and only if x is strictly better than the current K-th candidate (sift-down in O(log K)).",
                at_termination="Root element is the true K-th extremal element of the complete input set. Time O(N log K), space O(K)."
            )

        if pattern == "heap_k_way_merge":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Min-heap initialized with the first element of each of the K sorted streams: tuple (value, stream_idx, elem_idx). Heap size <= K.",
                during_iteration="Root min_heap.top() is the globally smallest element among all current stream frontiers.",
                after_movement="Extract root (min element), emit to output, and push the next element from the same stream into the min-heap in O(log K). If that stream is exhausted, heap size decreases by 1.",
                at_termination="All N total elements across all K streams are emitted in non-decreasing sorted order. Time O(N log K), space O(K)."
            )

        if pattern == "heap_two_heaps":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Dual-heap structure: max-heap 'low' for lower half, min-heap 'high' for upper half. Both empty.",
                during_iteration="Partition invariant: for all x in low and y in high, x <= y. Size balance: 0 <= |low| - |high| <= 1.",
                after_movement="Insert element x: push to low if x <= low.top() else high. Rebalance: if |low| > |high| + 1, move low.top() to high; if |high| > |low|, move high.top() to low.",
                at_termination="Partition invariant and size balance guarantee quantile/median is accessible in O(1) from heap tops. Total time O(N log N)."
            )

        if pattern == "heap_dynamic_median":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Dual-heap initialized: max-heap 'low' and min-heap 'high'. Empty stream.",
                during_iteration="Median partition: low stores the smaller ceil(N/2) elements; high stores the larger floor(N/2) elements. low.top() <= high.top().",
                after_movement="Insert x, then balance so |low| == |high| or |low| == |high| + 1. Median: low.top() if N is odd, else (low.top() + high.top()) / 2.0.",
                at_termination="Dynamic median query answered in O(1) at any point in the stream with O(log N) insertion cost per element."
            )

        if pattern == "heap_scheduling":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Sort intervals by start time ascending. Min-heap stores end times of active intervals.",
                during_iteration="Min-heap root is the earliest end time among currently occupied resources/rooms.",
                after_movement="For interval [s, e]: if s >= min_heap.top(), resource is freed (pop). Push e into min-heap. Heap size represents concurrently active resources.",
                at_termination="Maximum heap size reached during simulation is the minimum number of resources/rooms required. Time O(N log N)."
            )

        if pattern == "heap_greedy_selection":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Min-heap populated with all initial weights/costs. Initial total cost = 0.",
                during_iteration="Root and second element are the two minimal weights in the current collection.",
                after_movement="Greedy Choice: extract two smallest elements a and b, accumulate (a + b) to total cost, and push (a + b) back into min-heap. Huffman prefix-code optimality.",
                at_termination="Heap reduced to single composite element. Accumulated cost is mathematically minimal. Time O(N log N)."
            )

        if pattern == "heap_lazy_deletion":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Priority queue stores candidate elements. Frequency map/tracker records valid vs canceled/stale elements.",
                during_iteration="Active extremal element is accessed by peeking the heap. If heap.top() is marked stale in tracker, lazily pop and discard it.",
                after_movement="Stale elements are only pruned when they reach the root. Fresh elements remain in valid partial heap order without O(N) search.",
                at_termination="All valid elements processed in priority order with O(log N) amortized cost per operation. No O(N) array scans."
            )

        # ── Disjoint Set Union (DSU) Invariants (Phase 3H) ──

        if pattern == "dsu_basic":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="N singleton disjoint sets {0}, {1}, ..., {N-1}. parent[i] = i, size[i] = 1, num_components = N. Path compression and union-by-size enabled.",
                during_iteration="Partition invariant: parent pointers form rooted trees representing equivalence classes. find(x) == find(y) iff x and y are in the same component.",
                after_movement="find(x) compresses paths by setting parent[v] = root for all nodes on search path, reducing tree height to O(1) amortized. union(x, y) attaches smaller component to larger component (union-by-size), preserving O(alpha(N)) complexity.",
                at_termination="All union/find queries answered in nearly linear O(Q * alpha(N)) time. Exactly num_components disjoint trees remain."
            )

        if pattern == "dsu_component_metadata":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Each singleton component i has metadata initialized (e.g. size=1, sum=val[i], min=val[i], max=val[i]). Root of each set stores valid component-wide aggregate.",
                during_iteration="Metadata invariant: for any root r, metadata[r] = combine(metadata[c]) over all elements c in the component of r. Non-root nodes' metadata may be stale.",
                after_movement="union(x, y): identify roots rx = find(x), ry = find(y). If rx != ry, attach smaller tree to larger tree (e.g. rx -> ry), update metadata[ry] = combine(metadata[ry], metadata[rx]), preserving metadata invariant at root ry.",
                at_termination="Component metadata queries at any element x answered in O(alpha(N)) by inspecting metadata[find(x)]."
            )

        if pattern == "dsu_dynamic_connectivity":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Graph vertices {0..N-1} initially disconnected. Incremental edge stream arrives online.",
                during_iteration="Connectedness invariant: find(u) == find(v) if and only if there exists an edge path between u and v among added edges.",
                after_movement="Adding edge (u, v): if find(u) == find(v), edge is redundant (cycle detected); else union(u, v) merges their components and decrements component count by 1.",
                at_termination="Answers all dynamic connectivity queries in O(alpha(N)) per query without full graph re-traversals."
            )

        if pattern == "dsu_weighted":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Parent pointers parent[i] = i, potential difference to parent potential[i] = 0. Invariant: potential[i] = value[i] - value[parent[i]].",
                during_iteration="Potential difference to root: along path i -> parent[i] -> ... -> root, cumulative sum of potentials equals value[i] - value[root].",
                after_movement="find(x) recursively compresses path and updates potential[x] += potential[prev_parent]. union(x, y, w) with constraint value[x] - value[y] = w attaches root_x to root_y with potential[root_x] = w - pot[x] + pot[y].",
                at_termination="All potential relations preserved consistently or reported inconsistent in O(alpha(N)) amortized time."
            )

        if pattern == "dsu_potential_difference":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Weighted DSU initialized. Relative potential differences are queryable between any two elements in the same component.",
                during_iteration="If find(x) == find(y), difference value[x] - value[y] = potential[x] - potential[y] is uniquely determined. If find(x) != find(y), difference is indeterminate.",
                after_movement="find(x) and find(y) compress paths and compute offsets from their respective roots. If connected, return pot[x] - pot[y]; else indicate disconnected.",
                at_termination="Exact difference queries answered in O(alpha(N)) amortized time."
            )

        if pattern == "dsu_parity":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="parent[i] = i, parity[i] = 0 (same color as parent). Represents dynamic 2-coloring / bipartite relations.",
                during_iteration="Parity invariant: parity[i] = color[i] ^ color[parent[i]]. Path compression updates parity[i] ^= parity[prev_parent], so parity[i] = color[i] ^ color[root].",
                after_movement="union(x, y, p) where color[x] ^ color[y] = p: if find(x) == find(y), verify if (parity[x] ^ parity[y]) == p; if mismatch, contradiction (odd cycle). If disconnected, attach root_x -> root_y with parity[root_x] = p ^ parity[x] ^ parity[y].",
                at_termination="Incremental 2-coloring and bipartiteness consistency verified online in O(alpha(N)) per constraint."
            )

        if pattern == "dsu_rollback":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Rollback DSU initialized with union-by-size/rank WITHOUT path compression. Change history stack records: (u, parent[u], v, size[v], num_components, metadata_delta).",
                during_iteration="Tree height bounded to O(log N) by union-by-size. Change stack captures exact historical mutations to enable LIFO restoration.",
                after_movement="union(u, v): push previous state of modified root to history stack before mutating. rollback(): pop change record and restore parent, size, component count, and metadata to previous snapshot in O(1).",
                at_termination="Allows arbitrary backtracking and snapshot rollback in O(K) where K is number of undone operations, preserving correctness across recursive branches."
            )

        if pattern == "dsu_offline_dynamic_connectivity":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Time interval segment tree built over queries [0..Q-1]. Each edge (u, v) active over time interval [t_start, t_end) is placed into O(log Q) segment tree nodes.",
                during_iteration="Segment tree DFS: when entering node, apply unions for all edges at this node via Rollback DSU. When at leaf t, answer connectivity query t in O(log N). When exiting, rollback all unions added at this node.",
                after_movement="Rollback DSU un-merges edges in reverse order of addition, perfectly preserving state without path compression conflicts.",
                at_termination="All Q online queries and edge lifetimes processed in O(M log Q log N + Q log N) time and O((N + M) log Q) space."
            )

        if pattern == "dsu_kruskal_support":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Sort all graph edges by weight ascending. Basic DSU initialized on V vertices. MST edge set initialized to empty.",
                during_iteration="Cut property: minimum weight edge connecting two disjoint components belongs to the MST. For each edge (u, v, w): test find(u) == find(v).",
                after_movement="If find(u) != find(v): edge does not form a cycle; add to MST and union(u, v). If find(u) == find(v): edge forms a cycle; discarded.",
                at_termination="Terminates when MST has V - 1 edges or all edges inspected. Yields Minimum Spanning Tree/Forest in O(E log E) time."
            )

        if pattern == "dsu_constraint_consistency":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Constraint verification engine with Weighted/Parity DSU. System state initialized to consistent.",
                during_iteration="For each incoming relation (x, y, val): check if x and y are already in the same equivalence component.",
                after_movement="If find(x) == find(y): verify if existing potential/parity relation matches val. If mismatch, report contradiction and flag inconsistency without corrupting state. If valid, redundant edge is safely ignored.",
                at_termination="Verifies satisfiability of system of difference / parity constraints in O(M * alpha(N)) time."
            )

        # ── Phase 3I: Fenwick Tree Invariants ──
        if pattern == "fenwick_point_update_prefix_query":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Array A[1..N] represented by Fenwick tree tree[1..N] initialized to 0 or via O(N) linear-time build. Invariant: tree[i] = sum(A[j]) for j in (i - lowbit(i), i].",
                during_iteration="Binary index decomposition: query(x) accumulates tree[x] and strips lowbit (x -= lowbit(x)), decomposing [1, x] into O(log x) canonical disjoint power-of-2 intervals. Update add(i, delta) adds delta to all tree[k] covering i by repeatedly adding lowbit (k += lowbit(k)).",
                after_movement="After query(x), exactly all elements A[1..x] have been summed with no duplicates and no omissions. After add(i, delta), every interval (k - lowbit(k), k] containing i is updated by delta.",
                at_termination="Range sum [l, r] is answered via query(r) - query(l-1) using commutative group inverse in O(log N) time and O(N) space."
            )

        if pattern == "fenwick_range_update_point_query":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Difference array D[1..N] where D[i] = A[i] - A[i-1] (with A[0] = 0). Fenwick tree maintains prefix sums of D such that A[i] = sum(D[1..i]).",
                during_iteration="Range addition [l, r] with +delta modifies only boundaries: D[l] += delta and D[r+1] -= delta. Point query at index x is equivalent to prefix sum query(x) on difference tree.",
                after_movement="Range add [l, r] executes two Fenwick updates: add(l, +delta) and add(r+1, -delta). For any index k in [l, r], prefix(k) increases by delta; for k > r, +delta and -delta cancel out completely.",
                at_termination="Point value query A[x] answered in O(log N) via query(x); range update [l, r] completed in O(log N) time with O(N) memory."
            )

        if pattern == "fenwick_range_update_range_query":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Two Fenwick trees B1 and B2 initialized over difference array D[i] = A[i] - A[i-1]. B1 stores D[i], B2 stores i * D[i]. Prefix sum formula: prefix(x) = (x + 1) * query(B1, x) - query(B2, x).",
                during_iteration="Double-difference invariant: algebraic expansion shows sum_{i=1}^x A[i] = sum_{j=1}^x (x - j + 1) * D[j] = (x + 1) * sum(D[j]) - sum(j * D[j]). Both B1 and B2 are maintained under range additions.",
                after_movement="Range add [l, r] with +delta applies updates: B1: add(l, +delta), add(r+1, -delta); B2: add(l, l * delta), add(r+1, -(r+1) * delta). Preserves exact double-difference algebraic invariant across all queries.",
                at_termination="Arbitrary range sum query [l, r] answered via prefix(r) - prefix(l-1) in O(log N) time and O(N) space."
            )

        if pattern == "fenwick_frequency":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Underlying frequency array F[1..M] where F[v] stores the frequency of value v. Fenwick tree tree[1..M] initialized to 0; each node tree[i] stores aggregate frequency over [i - lowbit(i) + 1, i]: tree[i] = sum(F[k]) for k = i - lowbit(i) + 1 .. i.",
                during_iteration="Point update add(val, +1) / add(val, -1) dynamically tracks occurrences. Prefix query query(val) computes cumulative frequency count of elements <= val: sum(F[1..val]).",
                after_movement="Frequency in range [low, high] computed via query(high) - query(low-1). Dynamic insertions and deletions update O(log M) Fenwick nodes.",
                at_termination="Answers dynamic frequency counting, cumulative distribution function queries, and rank queries in O(log M) time."
            )

        if pattern == "fenwick_prefix_extremum":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="tree[1..N] initialized with identity (infinity for min, -infinity for max). Point updates must satisfy monotonicity: non-increasing for min (newValue <= oldValue), non-decreasing for max (newValue >= oldValue); equality is valid.",
                during_iteration="Monotonic update invariant: update(i, val) only tightens the extremum (tree[i] = min/max(tree[i], val)). For all j covering i, tree[j] maintains exact prefix extremum over [j - lowbit(j) + 1, j].",
                after_movement="Prefix extremum query query(x) traverses downward (x -= lowbit(x)) combining disjoint intervals via associative commutative monoid extremum operator. Non-monotonic point replacements are rejected.",
                at_termination="Evaluates prefix minimum or maximum queries in O(log N) time under monotonic updates (equality valid)."
            )

        if pattern == "fenwick_2d_point_update_range_query":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="2D Fenwick grid tree[1..N][1..M] initialized to 0. Invariant: node tree[r][c] covers rectangle [r - lowbit(r) + 1, r] x [c - lowbit(c) + 1, c].",
                during_iteration="Nested binary index traversal: update(r, c, delta) traverses r += lowbit(r) and c += lowbit(c); 2D prefix query(r, c) accumulates tree[i][j] via i -= lowbit(i) and j -= lowbit(j).",
                after_movement="Sub-rectangle query [r1, c1] to [r2, c2] evaluated via 2D inclusion-exclusion principle: query(r2, c2) - query(r1-1, c2) - query(r2, c1-1) + query(r1-1, c1-1).",
                at_termination="Answers dynamic 2D sub-rectangle sum queries and point updates in O(log N * log M) time and O(N * M) space."
            )

        if pattern == "fenwick_kth_element":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Fenwick tree maintains non-negative frequency distribution (frequency[x] >= 0) with total count S = query(M). Target rank k satisfies 1 <= k <= S.",
                during_iteration="Binary lifting invariant: maintain accumulator idx = 0 and current_sum = 0. For step = 2^floor(log2(M)) down to 1: test if idx + step <= M and current_sum + tree[idx + step] < k. If true, advance idx += step and current_sum += tree[idx].",
                after_movement="At each power of 2, tree[idx + step] precisely stores the sum of frequencies in interval (idx, idx + step] because idx is a multiple of step. Sub-tree frequency is evaluated in O(1) without calling query().",
                at_termination="Termination yields smallest index x = idx + 1 such that prefix_frequency(x) >= k in single-pass O(log M) time, outperforming O(log^2 M) binary search."
            )

        if pattern == "fenwick_inversion_counting":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Array A[1..N] with elements normalized to range [1..M] (via coordinate compression if needed). Fenwick frequency tree initialized to 0. Inversion count = 0.",
                during_iteration="Sweep invariant: Processing right-to-left: for element A[i], query(A[i] - 1) counts processed elements j > i with A[j] < A[i], then add(A[i], 1). Processing left-to-right: for element A[i], query(M) - query(A[i]) counts processed elements j < i with A[j] > A[i], then add(A[i], 1).",
                after_movement="Add query result to total inversions, then insert A[i] into Fenwick tree via add(A[i], 1). Invariant maintained: Fenwick tree holds aggregate frequency of processed suffix/prefix.",
                at_termination="Computes total inversion count in O(N log M) time and O(M) space."
            )

        if pattern == "fenwick_multiset":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Fenwick tree representing dynamic multiset over bounded universe [1..M]. Total element count S = 0.",
                during_iteration="Multiset invariants: frequency count of each element >= 0. Operations supported: insert(x) -> add(x, +1), erase(x) -> add(x, -1) (requiring count(x) > 0), count(x) -> query(x) - query(x-1), rank(x) -> query(x-1) + 1, find_kth(k) -> binary lifting.",
                after_movement="Insertions and deletions update frequency in O(log M). Negative frequencies are prohibited to preserve binary lifting prefix monotonicity.",
                at_termination="Provides order-statistic multiset functionality (insert, erase, rank, select) in O(log M) time per operation."
            )

        if pattern == "fenwick_coordinate_compression":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Collection of raw coordinates X = {x_1, ..., x_K} from values and query endpoints over arbitrary comparable coordinates representable by the problem/input type.",
                during_iteration="Compression pipeline: extract unique coordinates, sort in ascending order, remove duplicates. Maps each raw coordinate x to its 1-based rank in [1..M] where M <= K.",
                after_movement="Mapping guarantee: for any x, y in X, x < y iff rank(x) < rank(y). Binary search (std::lower_bound) retrieves rank in O(log M) time. Dense Fenwick tree allocated of size M.",
                at_termination="Enables Fenwick Tree execution over sparse/unbounded integer universes in O(K log K + Q log M) time and O(M) Fenwick memory."
            )

        # ── Segment Tree Patterns (Phase 3J) ──
        if pattern == "segment_tree_point_update_range_query":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Array A[1..N] represented by Segment Tree tree[1..4N] initialized via O(N) build. Invariant: each node u covering [l, r] stores aggregate = merge(tree[2u], tree[2u+1]).",
                during_iteration="Point update at index i modifies leaf [i, i] and updates all ancestors along the O(log N) root-to-leaf path via parent = merge(left, right). Range query [ql, qr] decomposes into O(log N) canonical disjoint nodes.",
                after_movement="Node aggregates accurately reflect the updated leaf value; query returns exact associative merge of disjoint covering segments with zero omissions or double counts.",
                at_termination="Answers dynamic point updates and associative range queries (sum, min, max, gcd) in O(log N) time per operation and O(N) space."
            )

        if pattern == "segment_tree_range_add_range_query":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Tree initialized over A[1..N] with lazy add tags initialized to 0. Invariant: each node u stores true interval sum after applying pending lazy addition.",
                during_iteration="Range add [ql, qr] by delta visits O(log N) canonical nodes; if [l, r] is completely contained in [ql, qr], apply tag immediately (node.sum += delta * len, lazy += delta). On partial overlap, push lazy tag to children (lazy_push) before recursing, then pull (node.sum = left.sum + right.sum).",
                after_movement="Lazy push preserves exact node and child aggregates; pending additions are deferred until children are accessed.",
                at_termination="Answers arbitrary range additions and range sum/min/max queries in O(log N) time and O(N) space."
            )

        if pattern == "segment_tree_range_assign_range_query":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Tree initialized with lazy assignment tags (has_assign = false, assign_val = 0). Invariant: node.sum represents true aggregate under pending assignment.",
                during_iteration="Range assign [ql, qr] to val completely overwrites target intervals: on full cover, node.sum = val * len, has_assign = true, assign_val = val. On partial overlap, push assignment to children before recursing, then pull.",
                after_movement="Pushed assignment overrides any previous state on child nodes; stale tags are completely replaced.",
                at_termination="Answers dynamic range assignment overwrites and range queries in O(log N) time and O(N) space."
            )

        if pattern == "segment_tree_combined_lazy_range_query":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Tree initialized with combined lazy tags (has_assign = false, assign_val = 0, add_val = 0). Invariant: net element value in node interval is (assign_val + add_val) if has_assign else node.val + add_val.",
                during_iteration="Tag composition algebra: new assignment X overrides both previous assign and add (has_assign = true, assign_val = X, add_val = 0). New addition delta adds to add_val (or to assign_val if has_assign). On partial overlap, push combined tag to children before descending.",
                after_movement="Children receive accurately composed operations preserving mathematical execution order (assign followed by add).",
                at_termination="Arbitrary compositions of range assignments, additions, and range queries execute in O(log N) time and O(N) space."
            )

        if pattern == "segment_tree_metadata_aggregate":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Each node stores composite tuple (sum, min_val, max_val, count) over interval [l, r]. Invariant: composite metadata is maintained via simultaneous associative merge.",
                during_iteration="Updates and queries process all metadata simultaneously: sum = L.sum + R.sum, min_val = min(L.min, R.min), max_val = max(L.max, R.max), count = L.count + R.count.",
                after_movement="All four aggregate statistics remain consistent and mutually valid across all subsegments.",
                at_termination="Evaluates simultaneous dynamic interval statistics in O(log N) time per operation."
            )

        if pattern == "segment_tree_max_subarray":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Each node stores (sum, pref, suff, ans) for non-empty contiguous subarrays. Leaves covering [i, i] initialized to A[i].",
                during_iteration="Non-commutative merge rule: sum = L.sum + R.sum, pref = max(L.pref, L.sum + R.pref), suff = max(R.suff, R.sum + L.suff), ans = max({L.ans, R.ans, L.suff + R.pref}). Identity is sentinel with empty = true.",
                after_movement="Range query [ql, qr] combines canonical nodes in strict left-to-right order, correctly finding maximum contiguous subarray sum even when all elements are negative.",
                at_termination="Computes dynamic maximum contiguous subarray sum in O(log N) time under point updates."
            )

        if pattern == "segment_tree_frequency_order_statistic":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Frequency tree tree[1..4M] over value domain [1..M] initialized to 0 with non-negative frequency invariant F[x] >= 0. Total count = tree[1].",
                during_iteration="Binary tree descent for k-th element (1 <= k <= total): if k <= tree[2u].count, traverse left child; else k -= tree[2u].count and traverse right child. Updates insert (+1) or delete (-1) occurrences.",
                after_movement="Locates k-th smallest element or calculates rank in strictly O(log M) time without binary search overhead.",
                at_termination="Provides dynamic order statistics (k-th element, rank, count) in O(log M) time per operation."
            )

        if pattern == "segment_tree_interval_statistics":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Each node stores (min_val, min_count, max_val, max_count) over interval [l, r].",
                during_iteration="Merge combines extrema conditionally: if L.min_val < R.min_val, inherit L; if R.min_val < L.min_val, inherit R; if equal, sum multiplicities (min_count = L.min_count + R.min_count). Max is merged symmetrically.",
                after_movement="Preserves exact multiplicity counts for range extrema without full frequency array overhead.",
                at_termination="Answers dynamic range minimum/maximum with exact frequency counts in O(log N) time."
            )

        # ── Dynamic Programming Patterns (Phase 3K) ──
        if pattern == "dp_1d_linear":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="dp array of size N initialized with base cases: dp[0] holds optimal value for prefix of length 1.",
                during_iteration="Invariant: At index i, dp[i] contains the exact optimal metric for the subproblem ending at index i, derived via Bellman's principle of optimality over all valid predecessors j < i.",
                after_movement="Index advances to i + 1; all states <= i are permanently solved and never recomputed.",
                at_termination="Global optimum is the maximum/minimum over all dp[i] (or dp[N-1]) in O(N) or O(N^2) time."
            )

        if pattern == "dp_grid_2d":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="dp table of size R x C initialized; boundary row 0 and column 0 initialized from initial path constraints.",
                during_iteration="Invariant: At cell (r, c), dp[r][c] stores the exact optimal metric from (0, 0) to (r, c) moving only right and down, evaluated in row-major topological order.",
                after_movement="Row and column pointers advance; all cells in previous rows and preceding columns are solved.",
                at_termination="Destination cell dp[R-1][C-1] contains the exact optimal path value in O(R * C) time."
            )

        if pattern == "dp_knapsack":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="dp table of size (N+1) x (W+1) initialized to 0 (or -INF for exact capacity matching); dp[0][w] = 0.",
                during_iteration="Invariant: After processing item i, dp[i][w] contains the maximum value achievable using a subset of the first i items within weight budget w.",
                after_movement="Item index increments; space compression allows 1D array dp[w] updated in reverse weight order (W down to weight[i]) for 0/1 knapsack.",
                at_termination="dp[N][W] (or max over w) contains the maximum achievable value in O(N * W) time."
            )

        if pattern == "dp_subsequence_string":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="dp table of size (|s1|+1) x (|s2|+1) initialized; base cases dp[0][j] and dp[i][0] set.",
                during_iteration="Invariant: dp[i][j] contains the exact optimal alignment/subsequence score for prefixes s1[0..i-1] and s2[0..j-1].",
                after_movement="Pointers (i, j) advance; each state transitions strictly from solved subproblems (i-1, j), (i, j-1), or (i-1, j-1).",
                at_termination="dp[|s1|][|s2|] contains the exact global subsequence metric in O(|s1| * |s2|) time."
            )

        if pattern == "dp_interval":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="dp table of size N x N initialized; base cases of length 1 dp[i][i] set to 0.",
                during_iteration="Invariant: For current length len, dp[i][j] (where j = i + len - 1) stores the exact optimal cost of merging subsegment [i..j], computed over all split points k in [i..j-1].",
                after_movement="Length len increments; all subproblems of length < len are guaranteed solved and invariant.",
                at_termination="dp[0][N-1] contains the optimal merge cost for the entire interval in O(N^3) time (or O(N^2) with Knuth optimization)."
            )

        if pattern == "dp_partition":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="dp[i][k] initialized; dp[0][0] = 0, dp[0][k] = INF for k > 0.",
                during_iteration="Invariant: dp[i][k] contains the optimal partition metric dividing prefix A[0..i-1] into k contiguous subsegments.",
                after_movement="Prefix length i and partition count k advance; state transitions test all valid previous segment endpoints j < i.",
                at_termination="dp[N][K] contains the optimal partition metric in O(K * N^2) time."
            )

        if pattern == "dp_state_machine":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="State vectors for day 0 initialized: hold[0] = -price[0], sold[0] = 0, rest[0] = 0.",
                during_iteration="Invariant: On day i, each state machine node (e.g. hold, sold, rest) contains the maximum profit achievable terminating day i in that exact operational state.",
                after_movement="Day i increments; states transition according to the legal finite state automaton transition matrix.",
                at_termination="Maximum of final non-holding states represents optimal profit under all state constraints in O(N) time and O(1) space."
            )

        if pattern == "dp_bitmask":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="dp table of size 2^N x N initialized to INF; base case dp[1 << start][start] = 0.",
                during_iteration="Invariant: dp[mask][u] contains the optimal cost of visiting subset 'mask' of vertices ending at vertex u, evaluated in numerical mask order.",
                after_movement="Mask integer increments; every submask of 'mask' has strictly smaller integer value and is already fully solved.",
                at_termination="min_{u} (dp[(1 << N) - 1][u] + cost(u, start)) gives optimal TSP tour in O(2^N * N^2) time."
            )

        if pattern == "dp_tree":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Post-order traversal order established; leaves have base case values computed.",
                during_iteration="Invariant: At node u, dp[u][state] contains the exact optimal metric for the subtree rooted at u, synthesized from all children v of u.",
                after_movement="Bottom-up DFS completes for subtree u; parent can safely consume dp[u].",
                at_termination="max_{state} dp[root][state] contains the global tree metric in O(V) time."
            )

        if pattern == "dp_dag":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Topological order of vertices computed; sink vertices initialized to base values.",
                during_iteration="Invariant: At vertex u in reverse topological order, dp[u] stores the exact optimal path metric from u to any reachable sink.",
                after_movement="Vertex pointer moves to preceding vertex in topological order; all reachable descendants from u are already solved.",
                at_termination="Global extremum over all dp[u] represents the optimal path metric in O(V + E) time."
            )

        if pattern == "dp_digit":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Digits of bound N extracted; memoization table dp[pos][sum][tight][leading_zero] initialized to -1.",
                during_iteration="Invariant: dp(pos, sum, tight, leading_zero) returns the exact count of valid digit sequences for suffixes starting at position 'pos' subject to boundary constraints.",
                after_movement="Position index advances from most significant to least significant digit; tight flag relaxes once a strictly smaller digit is chosen.",
                at_termination="f(R) - f(L - 1) computes exact range query count in O(num_digits * state_space) time."
            )

        if pattern == "dp_optimization":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Optimization structure (e.g. Convex Hull deque, Monotonic Queue) initialized with base line/element.",
                during_iteration="Invariant: Optimal transition argmin_k (dp[k] + cost(k, i)) is maintained via monotonic frontier; suboptimal choices are pruned in O(1) amortized time.",
                after_movement="New line/state added to hull/queue maintaining convexity or monotonicity invariant.",
                at_termination="Reduces overall DP time from O(N^2) to O(N) or O(N log N)."
            )

        if pattern == "dp_solution_reconstruction":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Forward DP computes optimal values and records decision pointers choice[state] or parent[state].",
                during_iteration="Invariant: Backtracking from final state following choice[state] reconstructs the exact sequence of optimal decisions.",
                after_movement="State transitions backward along the optimal decision trajectory.",
                at_termination="Reconstructed path/sequence is verified optimal and returned in O(path_length) time."
            )

        if pattern == "dp_space_optimization":
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Full multi-dimensional table reduced to minimal dependency dimension (e.g. single 1D array or two rolling rows).",
                during_iteration="Invariant: Outer loop step preserves the exact values needed for the current step while overwriting obsolete historical rows.",
                after_movement="Iteration direction (e.g. backward for 0/1 knapsack) guarantees that un-updated values from step i-1 are not overwritten prematurely.",
                at_termination="Returns exact optimal result while reducing memory complexity from O(N * K) to O(K)."
            )

        # ── Greedy Algorithms (Phase 3L) ──
        if "interval_selection" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Intervals sorted in non-decreasing order of finish time f_i. Selected set S = empty, last_finish = -infinity, count = 0.",
                during_iteration="The selected subset S_k is mutually non-overlapping, has cardinality k, and leaves the earliest finish time among all feasible subsets of size k (staying-ahead invariant).",
                after_movement="If start_i >= last_finish: interval i is selected, last_finish = end_i, count++. If start_i < last_finish: interval i overlaps and is safely eliminated by exchange argument.",
                at_termination="All candidate intervals evaluated; the construction is complete and the associated correctness proof establishes global optimality (maximum cardinality non-overlapping subset)."
            )

        if "interval_covering" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Intervals sorted ascending by end coordinate end_i. Placed points P = empty, last_point = -infinity, points = 0.",
                during_iteration="All intervals ending <= last_point contain at least one point in P; last_point is the rightmost possible coordinate that covers the current prefix.",
                after_movement="If start_i > last_point: a new point is placed at end_i (covering interval i and all overlapping subsequent intervals), points++, last_point = end_i. Otherwise, interval i is already covered by last_point.",
                at_termination="Every interval contains at least one stabbing point; the construction is complete and the associated correctness proof establishes global optimality (minimum stabbing cardinality)."
            )

        if "fractional_knapsack" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Items sorted descending by value density r_i = v_i / w_i. Remaining capacity W' = W, total_val = 0.",
                during_iteration="Knapsack capacity W - W' is filled with items of highest available value density; any alternative packing using the same capacity achieves at most total_val.",
                after_movement="take = min(W', w_i); total_val += take * r_i; W' -= take; item i is fully or fractionally exhausted; remaining capacity decreases monotonically.",
                at_termination="Remaining capacity is 0 or all items are exhausted; the construction is complete and the associated correctness proof establishes global optimality."
            )

        if "deadline_scheduling" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Jobs sorted by Earliest Due Date (non-decreasing d_i) or Smith's Rule (non-increasing w_i / p_i, equivalently non-decreasing p_i / w_i). current_time = 0, penalty = 0.",
                during_iteration="Prefix of scheduled jobs contains zero inversions; any adjacent inversion would strictly increase or preserve the objective penalty.",
                after_movement="current_time += p_i; job i is scheduled in the earliest available completion slot; lateness / weighted completion time penalty updated.",
                at_termination="All jobs scheduled; the construction is complete and the associated correctness proof establishes global optimality."
            )

        if "heap_assisted" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Events/stations sorted spatially along the trajectory. Max-heap of available resource capacities initialized empty; current_resource = initial_amount.",
                during_iteration="Current location is reached using the minimum number of previously activated resources; remaining resource buffer is maximized at each step.",
                after_movement="While current_resource < distance_to_next: extract maximum available resource from heap, activations++, current_resource += extracted. If heap is empty: location is unreachable.",
                at_termination="Destination reached or unreachable; the construction is complete and the associated correctness proof establishes global optimality (or the required feasibility guarantee)."
            )

        if "huffman_merge" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Min-heap initialized with all symbol frequencies as singleton trees. total_merge_cost = 0.",
                during_iteration="Min-heap contains roots of an optimal prefix forest for the reduced ground set; two lowest-frequency roots are siblings at maximum tree depth.",
                after_movement="Extract two minimal roots x and y, merge into parent node with frequency x + y, total_merge_cost += x + y, reinsert parent into min-heap.",
                at_termination="Single merged root component remains; the construction is complete and the associated correctness proof establishes global optimality (minimum weighted external path length)."
            )

        if "sequence_local_choice" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Monotonic stack initialized empty. Remaining removal budget = k.",
                during_iteration="Stack contains the lexicographically smallest prefix for the processed sequence under the budget of removals consumed so far.",
                after_movement="While stack not empty, top > current_element, and k > 0: pop stack, k--. Push current_element. Higher place-value dominance preserves lexicographical minimality.",
                at_termination="All characters scanned; excess removals discarded; the construction is complete and the associated correctness proof establishes global optimality (lexicographical minimality)."
            )

        if "reachability_partition" in pattern:
            is_gas = (
                params.get("reachability_kind") == "gas_station"
                or "gas" in str(params.get("problem_text", "")).lower()
                or "gas" in str(params).lower()
            )
            if is_gas:
                return FormalInvariant(
                    pattern=pattern,
                    before_iteration="Candidate start index = 0, current_tank = 0, total_surplus = 0.",
                    during_iteration="Candidate start is the only possible valid start in prefix [0..i]; if current_tank < 0, no index in [start..i] can be a valid starting point, so start is reset to i + 1 with current_tank = 0.",
                    after_movement="total_surplus += gas[i] - cost[i]; current_tank += gas[i] - cost[i]. If current_tank < 0: start = i + 1, current_tank = 0.",
                    at_termination="Single pass completed; if total_surplus >= 0, candidate start is the unique valid starting index; otherwise no valid start exists. The construction is complete and the associated correctness proof establishes global optimality (or the required feasibility guarantee)."
                )
            return FormalInvariant(
                pattern=pattern,
                before_iteration="current_jump_end = 0, farthest_reach = 0, jumps = 0.",
                during_iteration="All indices in [0..current_jump_end] are reachable in <= jumps. farthest_reach is the maximum index reachable from any index in [0..current_jump_end] (staying-ahead invariant).",
                after_movement="farthest_reach = max(farthest_reach, i + A[i]). If i == current_jump_end: jumps++, current_jump_end = farthest_reach.",
                at_termination="farthest_reach >= n - 1 implies destination reached with minimum jumps; scan index > farthest_reach implies unreachable. The construction is complete and the associated correctness proof establishes global optimality (or the required feasibility guarantee)."
            )

        if "graph_mst" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Edges sorted in non-decreasing order of weight w_e. DSU initialized with V disjoint components. edges_count = 0, total_weight = 0.",
                during_iteration="The set of selected edges forms an acyclic forest that is a subgraph of some Minimum Spanning Tree (Cut Property / Safe Cut Theorem).",
                after_movement="For edge (u, v, w): if find(u) != find(v), union(u, v), edges_count++, total_weight += w; otherwise edge forms a fundamental cycle and is safely discarded.",
                at_termination="If the graph is connected, exactly V - 1 edges are selected. If the graph is disconnected, the algorithm terminates with a minimum spanning forest containing V - C edges, where C is the number of connected components. The construction is complete and the associated correctness proof establishes global optimality."
            )

        if "general_exchange" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Elements ordered according to custom pairwise comparator comp(A, B) satisfying strict weak ordering and transitivity.",
                during_iteration="The ordered prefix contains no inversion under the objective-specific pairwise exchange relation.",
                after_movement="Swapping an adjacent inverted pair cannot improve the objective; therefore repeated elimination of inversions yields an optimal ordering.",
                at_termination="All elements sorted and arranged; the construction is complete and the associated correctness proof establishes global optimality."
            )

        # ── Divide and Conquer & Backtracking (Phase 3M) ──
        if "merge_sort_inversions" in pattern or ("inversion" in pattern and "dc" in pattern):
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Array A[l..r] partitioned into disjoint halves A[l..m] and A[m+1..r].",
                during_iteration="Subproblems A[l..m] and A[m+1..r] sorted and their internal inversions counted; merge step maintains sorted output prefix.",
                after_movement="Comparing A[i] with A[j]: if A[i] > A[j] (or A[i] > 2*A[j]), all remaining elements in left half A[i..m] satisfy the predicate with A[j], contributing (m - i + 1) to inversion count.",
                at_termination="All disjoint subproblems and cross-boundary contributions aggregated; count is exact. The construction is complete and the associated correctness proof establishes counting correctness."
            )

        if "quickselect" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Subarray A[l..r] contains target index k in unsorted order.",
                during_iteration="Pivot p chosen; 3-way partition divides A[l..r] into (< p, == p, > p) with boundaries [l..lt-1], [lt..gt], [gt+1..r].",
                after_movement="If k in [lt..gt], pivot is the k-th element; if k < lt, discard [lt..r] and recurse into [l..lt-1]; if k > gt, discard [l..gt] and recurse into [gt+1..r].",
                at_termination="Order statistic partition selected; k-th element definitively identified. The construction is complete and the associated correctness proof establishes decision correctness."
            )

        if "closest_pair" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Points sorted by x-coordinate; vertical line x = x_mid bisects points into left and right halves of size <= ceil(n/2).",
                during_iteration="delta = min(delta_left, delta_right) is the minimum distance between points within either half.",
                after_movement="Collect points within x_mid +- delta strip; sort by y; for each point, check at most 7 successors in y-order (geometric packing). Update delta if smaller distance found.",
                at_termination="All subproblems evaluated and cross-boundary strip checked; global optimal value is certified. The construction is complete and the associated correctness proof establishes global optimality."
            )

        if "tree_centroid" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Centroid C of current tree component computed such that removing C leaves subtrees of size <= n/2.",
                during_iteration="Path counts/weights through centroid C aggregated across disjoint subtrees; paths within same subtree subtracted to avoid duplicates.",
                after_movement="Centroid C marked removed; divide-and-conquer recurses into each remaining subtree component with depth <= log_2 n.",
                at_termination="All disjoint subproblems and cross-boundary contributions aggregated; count is exact. The construction is complete and the associated correctness proof establishes counting correctness."
            )

        if "cdq" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Offline events/queries sorted by primary dimension (time/index) in interval [l..r].",
                during_iteration="Subproblems [l..mid] and [mid+1..r] recursively solved and sorted by second dimension; left modifications contribute to right queries.",
                after_movement="Two-pointer sweep over sorted halves propagates left modifications to right queries via Fenwick tree without cross-talk.",
                at_termination="All disjoint subproblems and cross-boundary contributions aggregated; count is exact. The construction is complete and the associated correctness proof establishes counting correctness."
            )

        if "subsets_permutations" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Current path/combination is empty; decision index at start; elements sorted for duplicate skipping.",
                during_iteration="Current path represents a valid prefix configuration; candidate element A[i] added if not duplicate (i == start or A[i] != A[i-1]).",
                after_movement="A[i] appended to path; recursive exploration completes all extensions; A[i] popped from path restoring exact state.",
                at_termination="All valid combinatorial branches explored; complete configuration set returned. The construction is complete and the associated correctness proof establishes enumeration completeness."
            )

        if "constraint_satisfaction" in pattern or "csp" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Constraint bitmasks (row, col, diagonals, box) initialized to all-available.",
                during_iteration="Current partial assignment satisfies all problem constraints; candidate assignments restricted to unconstrained domain values.",
                after_movement="Candidate value assigned; constraint bitmasks updated; recurse; on backtrack, assignment cleared and bitmasks restored via bitwise operations.",
                at_termination="Satisfying assignment found or complete tree searched; feasibility is certified. The construction is complete and the associated correctness proof establishes feasibility."
            )

        if "branch_and_bound" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="best_objective initialized to +-infinity; current_cost = 0; partial assignment empty.",
                during_iteration="Admissible bound h(state) computed; if current_cost + h(state) >= best_cost (for minimization), entire subtree pruned.",
                after_movement="Decision made; incremental cost added; recursive branch explored; on backtrack, decision reverted and cost subtracted.",
                at_termination="All subproblems evaluated / branch bounded; global optimal value is certified. The construction is complete and the associated correctness proof establishes global optimality."
            )

        if "state_space_search" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Starting state/cell identified; visited path tracker initialized; search depth = 0.",
                during_iteration="Current path in state graph is valid and acyclic; candidate transitions restricted to valid unvisited adjacent states.",
                after_movement="State marked visited in-place; transition explored; on backtrack, visited mark reverted to original state value.",
                at_termination="Satisfying assignment found or complete tree searched; feasibility is certified. The construction is complete and the associated correctness proof establishes feasibility."
            )

        if "meet_in_the_middle" in pattern or "meet_in_middle" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Input set of size N split into two halves of size floor(N/2) and ceil(N/2).",
                during_iteration="Left half generates all 2^(floor(N/2)) combinations into sorted array; right half generates combinations independently.",
                after_movement="For each right half combination, binary search or two pointers finds optimal matching left half element in O(log(2^(N/2))) = O(N) time.",
                at_termination="All subproblems evaluated / branch bounded; global optimal value is certified. The construction is complete and the associated correctness proof establishes global optimality."
            )

        # ── Phase 3N: Advanced Graph Invariants ──
        if "01_bfs" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Deque initialized with source vertex at distance 0. All other vertices at distance infinity.",
                during_iteration="Vertices in deque maintain distance property: all elements in deque have distance d or d + 1.",
                after_movement="Relaxation along edge (u, v, w): if w == 0, push_front(v) with dist[v] = dist[u]; if w == 1, push_back(v) with dist[v] = dist[u] + 1.",
                at_termination="All reachable vertices finalized in non-decreasing order of distance in O(V + E) time without priority queue overhead."
            )

        if "spfa" in pattern or "negative_cycle" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Distance vector dist[s] = 0, others infinity. In-queue tracker and relaxation counter count[v] = 0.",
                during_iteration="Queue contains vertices whose distance labels recently decreased. For each relaxation (u, v), dist[v] > dist[u] + w.",
                after_movement="dist[v] updated, count[v] incremented. If count[v] >= V, pigeonhole principle certifies presence of reachable negative cycle.",
                at_termination="Finite shortest paths computed or negative cycle traced back via parent pointers and certified."
            )

        if "eulerian" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Vertex degrees verified for Eulerian parity (undirected: 0 or 2 odd vertices; directed: in == out everywhere except start/end).",
                during_iteration="Hierholzer traversal follows unused edges, advancing edge iterators to ensure each edge is traversed at most once.",
                after_movement="Dead-end vertex popped from call/search stack and pushed onto trail vector; sub-circuits spliced at common vertices.",
                at_termination="Trail contains exactly E edges in valid traversal order with zero duplicate edge usage."
            )

        if "2sat" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="2-CNF clauses transformed into directed implication graph with 2N vertices (x and ~x).",
                during_iteration="Tarjan SCC condensation groups mutually reachable literals into equivalence classes with topological component IDs.",
                after_movement="For each variable x, verify comp[x] != comp[~x]. If equal, formula is certified unsatisfiable.",
                at_termination="If satisfiable, truth value assigned according to topological condensation order: val[x] = (comp[x] > comp[~x])."
            )

        if "block_cut" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="DFS entry time tin and low-link low initialized; edge stack tracks current biconnected component.",
                during_iteration="DFS traversal updates low[u] = min(tin[u], tin[v], low[children]). Articulation condition: low[v] >= tin[u].",
                after_movement="When low[v] >= tin[u], pop edge stack until (u, v) to form a new block node connected to articulation vertex u.",
                at_termination="Graph decomposed into bipartite Block-Cut Tree with alternating cut-vertices and 2-vertex-connected blocks."
            )

        if "bridge_block" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="DFS discovery and low-link numbers computed across undirected graph.",
                during_iteration="Bridge condition: low[v] > tin[u] strictly identifies cut-edges whose removal increases connected components.",
                after_movement="Bridges deleted/bypassed; remaining connected components contracted into 2-edge-connected macro-nodes.",
                at_termination="Condensation forest represents 2-edge-connected components with bridges forming tree edges."
            )

        if "bipartite_matching" in pattern or "kuhn" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Matching array match[v] = -1 for all vertices in right partition.",
                during_iteration="DFS searches for augmenting path alternating between unmatched and matched edges starting from unmatched left vertex.",
                after_movement="When augmenting path found, edges along path flipped, strictly increasing matching cardinality by 1 (Berge's Lemma).",
                at_termination="No augmenting paths remain; matching achieves maximum possible cardinality in O(V * E) time."
            )

        if "max_flow" in pattern or "dinic" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Residual network initialized with capacity cap[u][v] = c, cap[v][u] = 0. Flow F = 0.",
                during_iteration="BFS builds level graph level[v] = level[u] + 1 on residual edges with cap > 0. DFS pushes blocking flow with current-arc ptr[u].",
                after_movement="Residual capacities adjusted: cap[u][v] -= pushed, cap[v][u] += pushed. Level of sink strictly increases each phase.",
                at_termination="Sink unreachable in residual network. Max-flow min-cut theorem guarantees F is maximal."
            )

        if "min_cut" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Maximum flow established on network via Dinic algorithm, producing saturated residual graph.",
                during_iteration="BFS from source s in residual network identifies set S of all reachable vertices with residual capacity > 0.",
                after_movement="Cut partition defined as (S, T = V \\ S). Cut edges are (u, v) where u in S, v in T with cap[u][v] fully saturated.",
                at_termination="Total capacity of cut edges equals maximum flow value; minimum capacity s-t cut certified."
            )

        if "mcmf" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Residual network tracks both capacity and cost. Net cost = 0, total flow = 0.",
                during_iteration="Successive shortest path finds augmenting path with minimum unit cost in residual network using potentials/SPFA.",
                after_movement="Flow augmented along minimum-cost path by bottleneck capacity; residual capacities and reverse costs updated.",
                at_termination="Residual network contains no negative-cost cycles reachable from source; flow achieves maximum value at minimum cost."
            )

        # ── Phase 3O: String Algorithms & Automata ──
        if "string_kmp" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Pattern border array pi precomputed in O(M). Text pointer i = 0, pattern pointer j = 0.",
                during_iteration="T[i-j .. i-1] == P[0 .. j-1] maintains maximal matched pattern prefix.",
                after_movement="If T[i] == P[j], both pointers advance. On mismatch, j retreats to pi[j-1] without i rolling back.",
                at_termination="Text pointer i reaches N. All exact pattern match start indices recorded in deterministic O(N + M) time."
            )

        if "string_z_algorithm" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Z[0] = N, Z-box segment [L, R] initialized to [0, 0].",
                during_iteration="[L, R] represents the rightmost matching interval such that S[L .. R] == S[0 .. R-L].",
                after_movement="For i <= R, Z[i] initialized from mirror Z[i - L] clamped to R - i + 1; expanded beyond R if possible, updating [L, R].",
                at_termination="i reaches N. Array Z contains exact lengths of longest common prefix between S and every suffix S[i..]."
            )

        if "string_rabin_karp" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Prefix polynomial hashes precomputed under double prime moduli (10^9+7, 10^9+9). Target pattern hash computed.",
                during_iteration="Window hash H(T[i .. i+M-1]) evaluated in O(1) time via modular prefix subtraction and base powers.",
                after_movement="If rolling hash matches target pattern hash, candidate reported under bounded collision probability (< 10^-14).",
                at_termination="Sliding window completes in expected O(N + M) time with O(1) auxiliary memory."
            )

        if "string_manacher" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="String transformed with dummy delimiters (#) to unify even/odd palindromes. Center C = 0, boundary R = 0.",
                during_iteration="P[i] tracks maximal palindromic radius centered at index i; palindrome [C - P[C], C + P[C]] is rightmost.",
                after_movement="For i < R, P[i] initialized to min(R - i, P[2*C - i]); expanded character-by-character; C and R updated when i + P[i] > R.",
                at_termination="Linear sweep completes in O(N) time. Every maximal palindromic substring radius certified."
            )

        if "string_aho_corasick" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Trie built over dictionary set. Suffix failure links and dictionary jump links constructed via BFS level order.",
                during_iteration="Text characters feed into DFA state transitions delta(u, c), retreating along failure links on missing arcs.",
                after_movement="At each state, dictionary link chain traversed to report all pattern keywords ending at current text index.",
                at_termination="Entire text processed in O(|T| + matches) time without ever rescanning text characters."
            )

        if "string_suffix_array" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Suffixes partitioned by initial character. Prefix doubling step k initialized to 0.",
                during_iteration="Equivalence pairs (rank[i], rank[i + 2^k]) sorted via counting sort, doubling length of sorted prefix.",
                after_movement="New ranks assigned; terminate when all ranks distinct or 2^k >= N. Kasai algorithm computes adjacent LCP in O(N).",
                at_termination="Complete lexicographical permutation of suffixes and adjacent LCP array certified in O(N log N) time."
            )

        if "string_suffix_automaton" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="SAM initialized with root state (len=0, link=-1). Pointers to last added state maintained.",
                during_iteration="Online extension appends character c: state cur created; suffix path redirected; states cloned on non-continuous links.",
                after_movement="Number of distinct substrings evaluated via direct invariant sum(len[v] - len[link[v]]) over all non-root states.",
                at_termination="Minimal DFA recognizing all substrings of S constructed in O(N * |Sigma|) with state count <= 2N - 1."
            )

        if "string_lyndon_duval" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Pointers i = 0 (factor start), j = 1 (exploration), k = 0 (pre-Lyndon reference). String doubled for cyclic shift.",
                during_iteration="Substring S[i .. j-1] is pre-Lyndon with period j - k. Character S[j] compared against S[k].",
                after_movement="If S[j] == S[k], k++ and j++; if S[j] > S[k], k = i and j++; if S[j] < S[k], output Lyndon factors of length j - k and advance i.",
                at_termination="Duval's factorization identifies canonical lexicographically minimal cyclic rotation in O(N) time and O(1) space."
            )

        if "string_subsequence_automaton" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Next-occurrence transition table next_pos[i][c] precomputed from right to left in O(N * |Sigma|).",
                during_iteration="Query string Q consumed character-by-character; state transitions to next_pos[curr_pos][c].",
                after_movement="If next_pos is null/invalid, query rejected; else curr_pos advances to matching position.",
                at_termination="Subsequence acceptance decided in strictly O(|Q|) query time without scanning text."
            )

        if "string_longest_common_substring_sam" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Suffix automaton constructed on S_1. Current SAM state v = root, matched length l = 0.",
                during_iteration="Characters of S_2 stream through SAM: if transition exists, v = next(v, c) and l++; else follow suffix links.",
                after_movement="When link followed, l clamped to len[v]; track maximum match length achieved across all steps.",
                at_termination="Longest common contiguous substring between S_1 and S_2 identified in linear O(|S_1| * |Sigma| + |S_2|) time."
            )

        # ── Phase 3P: Number Theory & Combinatorics ──
        if "nt_extended_gcd" in pattern or "nt_diophantine" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Input coefficients a, b initialized. Base case: if b == 0, gcd = |a|, x = sgn(a), y = 0.",
                during_iteration="Euclidean division: a = q * b + r. Recursive call computes x1, y1 satisfying b * x1 + r * y1 = gcd(b, r).",
                after_movement="Unwind step updates Bezout coefficients: x = y1, y = x1 - q * y1, preserving invariant a*x + b*y = gcd(a, b).",
                at_termination="Termination when remainder r reaches 0. Returns certified gcd(a, b) and minimal particular solution x0, y0 in O(log(min(|a|, |b|)))."
            )

        if "nt_modular_inverse" in pattern or "nt_inv" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Modular element a and modulus m validated. Precondition: gcd(a, m) == 1 certified; if gcd != 1, inverse does not exist.",
                during_iteration="In prime field F_p: binary exponentiation evaluates a^(p-2) mod p. In ring Z/mZ: ExtGCD computes a*x + m*y = 1.",
                after_movement="Modular normalization ensures result lies in canonical representative range [0, m-1] via (x % m + m) % m.",
                at_termination="Certified inverse a^(-1) returned satisfying (a * a^(-1)) % m == 1 in O(log m) time with no precision loss."
            )

        if "nt_chinese_remainder" in pattern or "nt_crt" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="System congruences initialized: x = r_0 mod m_0. Global solution x = r_0, current modulus M = m_0.",
                during_iteration="For each subsequent congruence x = r_i mod m_i: solve M * t + m_i * u = (r_i - x). Solvability check: (r_i - x) % gcd(M, m_i) == 0.",
                after_movement="Update global solution x = (x + M * t) % lcm(M, m_i) and new modulus M = lcm(M, m_i) tracked in signed 128-bit capacity.",
                at_termination="All congruences simultaneously satisfied in range [0, M-1]; fails closed if insolvability detected or M >= 2^127 - 1."
            )

        if "nt_linear_sieve" in pattern or "nt_prime_factorization" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Arrays spf[1..N] initialized to 0; prime list empty. Iteration index i starts at 2.",
                during_iteration="If spf[i] == 0: i is prime, append i to prime list and set spf[i] = i.",
                after_movement="For each prime p <= spf[i] with p * i <= N: mark composite spf[p * i] = p. Strictly visited exactly once by its smallest prime factor.",
                at_termination="Euler sieve completes in strictly linear O(N) time with O(log K) factorizations per query up to N."
            )

        if "nt_euler_totient" in pattern or "nt_phi" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="For single-query: ans = N, temp = N, divisor d starts at 2. For range-query: phi[1..N] initialized via linear sieve.",
                during_iteration="For prime factor p dividing temp: multiply ans by (1 - 1/p) = (p - 1) / p; divide out all factors of p from temp.",
                after_movement="Multiplicative property phi(p * i) = phi(i) * (p - 1) if p doesn't divide i, else phi(i) * p maintained during sieve sweep.",
                at_termination="Single-instance totient computed in O(sqrt N); range table phi(1..N) generated in strictly linear O(N) time."
            )

        if "nt_mobius_inversion" in pattern or "nt_mobius_sieve" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Arrays mu[1..N] initialized: mu[1] = 1, primes recorded via linear sieve sweep.",
                during_iteration="For each composite p * i: if i % p == 0, then p^2 divides p * i, setting mu[p * i] = 0; else mu[p * i] = -mu[i].",
                after_movement="Divisor convolution f(n) = sum_{d | n} mu(d) * g(n/d) or coprime pair sum evaluated using square-free parity table.",
                at_termination="Möbius table mu(1..N) produced in linear O(N) time; divisor sum reduced from quadratic scan to linear or sublinear block scan."
            )

        if "nt_matrix_power" in pattern or "nt_linear_recurrence" in pattern or "nt_matrix_exponentiation" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Transition matrix T of dimension D x D constructed; result matrix R initialized to identity I_D; exponent K >= 0.",
                during_iteration="Binary exponentiation: while K > 0, if K & 1 then R = (R * T) mod M; then T = (T * T) mod M; K >>= 1.",
                after_movement="Associativity of matrix multiplication preserves invariant R * T^K == T_{init}^{K_{init}} (mod M) at every step.",
                at_termination="Linear recurrence state evaluated in strictly O(D^3 * log K) operations; identity matrix emitted for K == 0."
            )

        if "nt_combinatorics_factorials" in pattern or "nt_ncr_mod_p" in pattern or "nt_factorial_combinatorics" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Modulus p certified prime. Precondition: N < p. Arrays fact[0..N] and invFact[0..N] allocated.",
                during_iteration="Forward sweep computes fact[i] = (fact[i-1] * i) mod p. Fermat inverse computes invFact[N] = fact[N]^(p-2) mod p.",
                after_movement="Backward telescoping sweep: invFact[i-1] = (invFact[i] * i) mod p, achieving O(1) inverse factorials for all i < p.",
                at_termination="nCr mod p answered in O(1) time per query via fact[n] * invFact[r] * invFact[n-r] mod p, short-circuiting to 0 if r > n or r < 0."
            )

        if "nt_lucas_theorem" in pattern or "nt_lucas" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Modulus p certified prime. Precomputed small factorial tables up to p - 1 prepared in O(p) time.",
                during_iteration="While N > 0 or K > 0: extract base-p digits n_i = N % p, k_i = K % p; evaluate subproblem nCr_small(n_i, k_i) mod p; N /= p, K /= p.",
                after_movement="Congruence invariant binom(N, K) == prod binom(n_i, k_i) (mod p) maintained across base-p digit positions.",
                at_termination="If any k_i > n_i, overall combination congruent to 0 mod p; otherwise product of digit combinations returned in O(log_p N) time."
            )

        if "nt_miller_rabin" in pattern or "nt_primality_test" in pattern:
            return FormalInvariant(
                pattern=pattern,
                before_iteration="Candidate N parsed as unsigned 64-bit integer. Small primes (< 64) checked. Decompose N - 1 = 2^s * d with d odd.",
                during_iteration="For each witness a in locked 7-witness basis {2, 325, 9375, 28178, 450775, 9780504, 1795265022}: compute x = a^d mod N.",
                after_movement="If x == 1 or x == N - 1, witness passes. Otherwise square x up to s - 1 times: if x becomes N - 1, passes; if never N - 1, composite certified.",
                at_termination="All 7 deterministic witnesses pass without finding non-trivial square roots of 1 => N certified prime for all N < 2^64."
            )

        return FormalInvariant(
            pattern=pattern,
            before_iteration="Initial pointers positioned at valid collection boundaries.",
            during_iteration="Pointers maintain bounded valid search segment.",
            after_movement="Movement eliminates candidates proved non-optimal by invariant.",
            at_termination="Termination implies complete coverage of valid search space."
        )

