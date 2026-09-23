"""
Monotonicity Engine for Pointer-Based Algorithms.

Explicitly models and verifies the required monotonicity type:
- VALUE_ORDER_MONOTONICITY: a[i] <= a[j] for i < j allows bounding pair relations.
- WINDOW_VALIDITY_MONOTONICITY: expanding R monotonically changes state in one direction,
  shrinking L monotonically reverses it (e.g., distinct count, positive sum).
- OBJECTIVE_MONOTONICITY: bounding objective values by geometric or arithmetic limits (e.g., Container With Most Water).
- SEARCH_SPACE_MONOTONICITY: boundary movement strictly contracts candidate solution space without losing optimum.
- POINTER_ELIMINATION_MONOTONICITY: scanner advances forward strictly skipping redundant candidates.
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

class MonotonicityKind(str, Enum):
    VALUE_ORDER_MONOTONICITY = "value_order_monotonicity"
    WINDOW_VALIDITY_MONOTONICITY = "window_validity_monotonicity"
    OBJECTIVE_MONOTONICITY = "objective_monotonicity"
    SEARCH_SPACE_MONOTONICITY = "search_space_monotonicity"
    POINTER_ELIMINATION_MONOTONICITY = "pointer_elimination_monotonicity"
    # Phase 3B: stack elements maintain a monotonic invariant enabling permanent candidate elimination
    STACK_ELIMINATION_MONOTONICITY = "stack_elimination_monotonicity"
    # Phase 3C: monotone predicates and feasibility transitions enabling interval halving
    PREDICATE_MONOTONICITY = "predicate_monotonicity"
    FEASIBILITY_MONOTONICITY = "feasibility_monotonicity"

class MonotonicityStatus(str, Enum):
    MONOTONICITY_REQUIRED = "monotonicity_required"
    MONOTONICITY_CONFIRMED = "monotonicity_confirmed"
    MONOTONICITY_BROKEN = "monotonicity_broken"

@dataclass
class MonotonicityAssessment:
    kind: MonotonicityKind
    status: MonotonicityStatus
    property_description: str
    justification: str
    is_valid_for_movement: bool
    broken_reason: Optional[str] = None

class MonotonicityEngine:
    """Evaluates whether the structural conditions of a problem provide the needed monotonicity."""

    @staticmethod
    def assess_for_pattern(
        pattern: str,
        has_negative_values: bool,
        is_sorted: bool,
        can_sort: bool,
        is_contiguous: bool,
        tracks_distinct: bool = False,
        objective_type: str = "",
        tracks_distinct_or_frequencies: bool = False
    ) -> MonotonicityAssessment:
        distinct_flag = tracks_distinct or tracks_distinct_or_frequencies
        """
        Determines what property must be monotonic for THIS movement to be valid
        and whether that property is confirmed or broken.
        """

        # 1. Converging Pair / Multi-element Sum & Difference
        if pattern in ("pair_sum_sorted", "closest_pair_sum", "three_sum_converging", "four_sum_converging", "pair_difference", "chase_pointer_difference"):
            kind = MonotonicityKind.VALUE_ORDER_MONOTONICITY
            if is_sorted or can_sort:
                return MonotonicityAssessment(
                    kind=kind,
                    status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                    property_description="Sorted element sequence guarantees multi-element sum/diff changes monotonically with pointer index moves.",
                    justification="Non-decreasing order ensures sum monotonic bounds regardless of signs (positive or negative).",
                    is_valid_for_movement=True
                )
            else:
                return MonotonicityAssessment(
                    kind=kind,
                    status=MonotonicityStatus.MONOTONICITY_BROKEN,
                    property_description="Value order monotonicity requires sorted elements.",
                    justification="Array is unsorted and sorting is forbidden or would destroy required semantic positions.",
                    is_valid_for_movement=False,
                    broken_reason="UNSORTED_WITHOUT_SORTING_PERMITTED"
                )

        # 2. Container With Most Water & Trapping Rain Water
        if pattern == "container_most_water":
            kind = MonotonicityKind.OBJECTIVE_MONOTONICITY
            return MonotonicityAssessment(
                kind=kind,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description="Area is bounded by min(h[L], h[R]) * (R - L). Width strictly decreases.",
                justification="Because min(h[L], h[k]) <= h[L] for any k < R, no pair (L, k) can beat the current area when h[L] <= h[R].",
                is_valid_for_movement=True
            )

        if pattern == "trapping_rain_water":
            kind = MonotonicityKind.OBJECTIVE_MONOTONICITY
            return MonotonicityAssessment(
                kind=kind,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description="Water trapped at boundary is strictly determined by min(left_max, right_max).",
                justification="When left_max < right_max, water at L is bounded purely by left_max regardless of internal heights, enabling safe inward movement of L.",
                is_valid_for_movement=True
            )

        # 3. Counting with Pointers on Sorted Arrays
        if pattern in ("count_pairs_less_than_k", "count_pairs_equal_k"):
            kind = MonotonicityKind.VALUE_ORDER_MONOTONICITY
            if is_sorted or can_sort:
                return MonotonicityAssessment(
                    kind=kind,
                    status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                    property_description="Sorted order guarantees that if a[L] + a[R] < K, then all pairs (L, k) for k in L+1..R also satisfy the condition.",
                    justification="Monotonic increase allows batched counting of R - L elements in O(1) step followed by L++ elimination.",
                    is_valid_for_movement=True
                )
            else:
                return MonotonicityAssessment(
                    kind=kind,
                    status=MonotonicityStatus.MONOTONICITY_BROKEN,
                    property_description="Batched pair counting requires value order monotonicity on sorted elements.",
                    justification="Unsorted array prevents inferring relation for intermediate elements.",
                    is_valid_for_movement=False,
                    broken_reason="UNSORTED_WITHOUT_SORTING_PERMITTED"
                )

        # 4. Counting Subarrays Bounded & Exact Count Derived
        if pattern in ("count_subarrays_bounded", "exact_count_derived"):
            kind = MonotonicityKind.WINDOW_VALIDITY_MONOTONICITY
            if has_negative_values and not distinct_flag:
                return MonotonicityAssessment(
                    kind=kind,
                    status=MonotonicityStatus.MONOTONICITY_BROKEN,
                    property_description="Window validity monotonicity requires non-negative elements or frequency metrics.",
                    justification="Negative elements break prefix sum monotonicity, invalidating single-pass sliding window counting.",
                    is_valid_for_movement=False,
                    broken_reason="WINDOW_NOT_MONOTONIC_NEGATIVE_SUM"
                )
            return MonotonicityAssessment(
                kind=kind,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description="Window validity is monotonic; for valid window [L..R], R - L + 1 contiguous subarrays end at R.",
                justification="For exact count K, monotonic decomposition into atMost(K) - atMost(K-1) preserves window monotonicity on both sub-queries.",
                is_valid_for_movement=True
            )

        # 5. Sliding Window - Sum Based
        if pattern in ("sliding_window_variable_min", "sliding_window_variable_max") and not distinct_flag:
            kind = MonotonicityKind.WINDOW_VALIDITY_MONOTONICITY
            if has_negative_values:
                # With negative numbers, adding an element can DECREASE sum, removing can INCREASE sum!
                return MonotonicityAssessment(
                    kind=kind,
                    status=MonotonicityStatus.MONOTONICITY_BROKEN,
                    property_description="Window sum monotonicity requires non-negative increments.",
                    justification="Arbitrary negative and positive numbers allow window sum to fluctuate non-monotonically, invalidating greedy shrinking.",
                    is_valid_for_movement=False,
                    broken_reason="WINDOW_NOT_MONOTONIC_NEGATIVE_SUM"
                )
            else:
                return MonotonicityAssessment(
                    kind=kind,
                    status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                    property_description="Non-negative elements ensure window sum is non-decreasing with R and non-increasing with L.",
                    justification="Sum increases monotonically upon R expansion, and decreases monotonically upon L contraction.",
                    is_valid_for_movement=True
                )

        # 6. Sliding Window - Frequency / Distinct Count / Substring
        if distinct_flag or pattern in ("sliding_window_fixed", "minimum_window_substring"):
            kind = MonotonicityKind.WINDOW_VALIDITY_MONOTONICITY
            return MonotonicityAssessment(
                kind=kind,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description="Frequency and coverage constraints are monotonic with window boundary shifts.",
                justification="Expanding R can only satisfy or maintain character constraints; shrinking L eventually tightens the window to minimal valid span.",
                is_valid_for_movement=True
            )

        # 7. Same-Direction Compaction / Deduplication / In-Place Reordering
        if pattern in ("remove_duplicates_sorted", "in_place_compaction", "move_zeroes_ordered"):
            kind = MonotonicityKind.POINTER_ELIMINATION_MONOTONICITY
            return MonotonicityAssessment(
                kind=kind,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description="Fast/read pointer advances strictly forward through the sequence.",
                justification="Elements that fail predicate or match duplicate state are safely skipped without revisitation.",
                is_valid_for_movement=True
            )

        # 8. Partition Pointers (Dutch National Flag)
        if pattern in ("partition_dutch_flag", "partition_two_way"):
            kind = MonotonicityKind.SEARCH_SPACE_MONOTONICITY
            return MonotonicityAssessment(
                kind=kind,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description="Uninspected window [mid..high] strictly contracts.",
                justification="Every step places an element into one of the invariant regions, shrinking uninspected domain by 1.",
                is_valid_for_movement=True
            )

        # 9. Palindrome Verification
        if pattern == "palindrome_verification":
            kind = MonotonicityKind.SEARCH_SPACE_MONOTONICITY
            return MonotonicityAssessment(
                kind=kind,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description="Symmetric outer positions converge monotonically inward.",
                justification="Comparing symmetric endpoints contracts uninspected substring while preserving palindrome property.",
                is_valid_for_movement=True
            )

        # 10. Merge Sorted Arrays
        if pattern == "merge_sorted_arrays":
            kind = MonotonicityKind.POINTER_ELIMINATION_MONOTONICITY
            return MonotonicityAssessment(
                kind=kind,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description="Read pointers advance monotonically through sorted streams.",
                justification="Because both input sequences are sorted, advancing the smaller element produces non-decreasing merged order.",
                is_valid_for_movement=True
            )

        # 11. Fast / Slow Linked Structures
        if pattern in ("linked_cycle_detection", "linked_cycle_start", "linked_middle_node"):
            kind = MonotonicityKind.POINTER_ELIMINATION_MONOTONICITY
            return MonotonicityAssessment(
                kind=kind,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description="Relative pointer offset advances strictly monotonically.",
                justification="Fast pointer advances 2 steps while slow advances 1 step, establishing a 2:1 distance invariant.",
                is_valid_for_movement=True
            )

        # ── 12. Monotonic Stack Patterns (Phase 3B) ──
        # All stack patterns rely on STACK_ELIMINATION_MONOTONICITY:
        # values along the stack maintain a monotonic order, and any element
        # that violates this order permanently dominates (and resolves) the top.

        MS_DIRECTIONAL = {
            "next_greater_element", "next_smaller_element",
            "previous_greater_element", "previous_smaller_element",
            "nearest_greater_element", "nearest_smaller_element",
            "circular_next_greater"
        }

        if pattern in MS_DIRECTIONAL:
            relation = "greater" if "greater" in pattern else "smaller"
            direction = "right" if "next" in pattern else ("left" if "previous" in pattern else "both")
            stack_order = "decreasing" if relation == "greater" else "increasing"
            return MonotonicityAssessment(
                kind=MonotonicityKind.STACK_ELIMINATION_MONOTONICITY,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description=(
                    f"Stack maintains monotonically {stack_order} values. "
                    f"Scanning {direction}, each element that violates the {stack_order} order "
                    f"is dominated by the current element and permanently resolved."
                ),
                justification=(
                    f"Invariant: elements on the stack are waiting for their {direction} {relation} neighbor. "
                    f"When arr[i] {'>' if relation == 'greater' else '<'} arr[stack.top()], "
                    f"arr[i] is definitively the first {relation} element for stack.top(), "
                    f"which can never be superseded by any future candidate."
                ),
                is_valid_for_movement=True
            )

        if pattern == "stock_span":
            return MonotonicityAssessment(
                kind=MonotonicityKind.STACK_ELIMINATION_MONOTONICITY,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description=(
                    "Stack maintains monotonically decreasing prices (left-to-right). "
                    "Span = current_index - index_of_last_greater_element."
                ),
                justification=(
                    "When price[i] >= price[stack.top()], stack.top() can never be the previous greater "
                    "element for any future index, since price[i] dominates it from the left."
                ),
                is_valid_for_movement=True
            )

        if pattern == "largest_rectangle_histogram":
            return MonotonicityAssessment(
                kind=MonotonicityKind.STACK_ELIMINATION_MONOTONICITY,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description=(
                    "Stack maintains monotonically non-decreasing bar heights. "
                    "When a shorter bar is encountered, taller stack bars are permanently bounded on the right."
                ),
                justification=(
                    "When height[i] < height[stack.top()]: stack.top() is the tallest remaining "
                    "left-extending bar, and i is its rightmost extent. Width = i - previous_stack_top - 1. "
                    "No future bar can extend this rectangle further right since it would be blocked by the current short bar."
                ),
                is_valid_for_movement=True
            )

        if pattern in ("sum_subarray_minimums", "sum_subarray_maximums"):
            relation = "smaller" if pattern == "sum_subarray_minimums" else "larger"
            objective = "minimum" if pattern == "sum_subarray_minimums" else "maximum"
            return MonotonicityAssessment(
                kind=MonotonicityKind.STACK_ELIMINATION_MONOTONICITY,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description=(
                    f"Stack maintains monotonically {'increasing' if relation == 'smaller' else 'decreasing'} values. "
                    f"For each element, two monotonic stack passes determine the left and right boundaries "
                    f"of subarrays where it is the {objective}."
                ),
                justification=(
                    f"Element arr[i] is the {objective} of all subarrays [l..r] where l is in "
                    f"(left_boundary[i], i] and r is in [i, right_boundary[i]). "
                    f"These boundaries are determined in O(n) by two monotonic stack scans. "
                    f"Strictness convention prevents double-counting of equal elements."
                ),
                is_valid_for_movement=True
            )

        # ── Binary Search Monotonicity (Phase 3C) ──

        if pattern in ("binary_search_exact", "lower_bound", "upper_bound", "predecessor", "successor"):
            return MonotonicityAssessment(
                kind=MonotonicityKind.VALUE_ORDER_MONOTONICITY,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description="Sorted array order guarantees monotonic predicate evaluation across indices.",
                justification=(
                    "For a sorted array A: i <= j implies A[i] <= A[j]. "
                    "For any target x, the predicate P(i) : A[i] >= x (or > x) is monotonically non-decreasing (false -> true). "
                    "Therefore, if P(mid) is true, no earlier index can be the first true, and all later indices are also true, "
                    "enabling exact half-space elimination in O(log N) steps."
                ),
                is_valid_for_movement=True
            )

        if pattern in ("first_true", "last_true", "first_false", "last_false"):
            return MonotonicityAssessment(
                kind=MonotonicityKind.PREDICATE_MONOTONICITY,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description="Boolean decision predicate P(i) exhibits a single monotonic transition boundary.",
                justification=(
                    "The domain partitions into two contiguous intervals: {x : P(x) = false} and {x : P(x) = true}. "
                    "Evaluating P(mid) definitively rules out one contiguous half-interval, preserving the invariant that "
                    "the transition boundary lies within the updated active interval [lo, hi]."
                ),
                is_valid_for_movement=True
            )

        if pattern == "binary_search_answer_min":
            return MonotonicityAssessment(
                kind=MonotonicityKind.FEASIBILITY_MONOTONICITY,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description="Feasibility predicate P(c) is monotonic false -> true with respect to capacity/load.",
                justification=(
                    "If a candidate capacity or speed c is sufficient to fulfill the task requirements under constraints, "
                    "any larger capacity c' > c is also sufficient (greater capacity strictly increases operational slack). "
                    "Consequently, P(c) transitions monotonically from false (infeasible) to true (feasible). "
                    "The global minimum feasible answer is precisely the first true value in the answer space."
                ),
                is_valid_for_movement=True
            )

        if pattern == "binary_search_answer_max":
            return MonotonicityAssessment(
                kind=MonotonicityKind.FEASIBILITY_MONOTONICITY,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description="Feasibility predicate P(d) is monotonic true -> false with respect to distance/threshold.",
                justification=(
                    "If a minimum distance or allocation d is achievable, any smaller threshold d' < d is also achievable "
                    "(a smaller distance threshold relaxes placement constraints). "
                    "Consequently, P(d) transitions monotonically from true (feasible) to false (infeasible). "
                    "The global maximum feasible answer is precisely the last true value in the answer space."
                ),
                is_valid_for_movement=True
            )

        if pattern == "binary_search_value_domain":
            return MonotonicityAssessment(
                kind=MonotonicityKind.SEARCH_SPACE_MONOTONICITY,
                status=MonotonicityStatus.MONOTONICITY_CONFIRMED,
                property_description="Monotonic arithmetic function over discrete integer domain.",
                justification=(
                    "Arithmetic function f(x) (e.g. x*x) is strictly increasing for non-negative integers x. "
                    "The condition f(x) <= n transitions from true to false at floor(sqrt(n)). "
                    "Interval bisection locates the exact discrete boundary in O(log(upper_bound)) steps."
                ),
                is_valid_for_movement=True
            )

        # Default fallback
        return MonotonicityAssessment(
            kind=MonotonicityKind.SEARCH_SPACE_MONOTONICITY,
            status=MonotonicityStatus.MONOTONICITY_REQUIRED,
            property_description="General search space reduction.",
            justification="Requires verification of boundary elimination rule.",
            is_valid_for_movement=True
        )

