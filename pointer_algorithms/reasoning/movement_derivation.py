"""
Movement Derivation Engine for Pointer-Based Algorithms.

Formally derives pointer movements from:
- Objective function
- Monotonic relationships
- Mathematical elimination proofs
"""

from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class MovementDerivation:
    pattern: str
    objective_function: str
    decision_conditions: Dict[str, str]
    elimination_proof: str
    state_updates: Dict[str, str]

class MovementDerivationEngine:
    """Derives valid pointer movements from first principles and mathematical bounds."""

    @staticmethod
    def derive(pattern: str, params: Dict[str, Any]) -> MovementDerivation:
        if pattern == "pair_sum_sorted":
            target = params.get("target", "T")
            return MovementDerivation(
                pattern=pattern,
                objective_function=f"find pair (L, R) such that A[L] + A[R] == {target}",
                decision_conditions={
                    "A[L] + A[R] < target": "L++ (increment lower pointer)",
                    "A[L] + A[R] > target": "R-- (decrement upper pointer)",
                    "A[L] + A[R] == target": "Optimal match found"
                },
                elimination_proof=(
                    f"Assume A is sorted non-decreasingly.\n"
                    f"Case 1: A[L] + A[R] < {target}.\n"
                    f"For any k in [L, R - 1], A[k] <= A[R], which implies A[L] + A[k] <= A[L] + A[R] < {target}.\n"
                    f"Thus, index L cannot form a valid pair with ANY element in the current candidate set [L..R].\n"
                    f"Therefore, eliminating L by moving to L + 1 preserves all possible valid solutions.\n"
                    f"Case 2: A[L] + A[R] > {target}.\n"
                    f"For any k in [L + 1, R], A[k] >= A[L], which implies A[k] + A[R] >= A[L] + A[R] > {target}.\n"
                    f"Thus, index R cannot form a valid pair with any remaining candidate. R-- safely eliminates R."
                ),
                state_updates={
                    "L++": "Increases pair sum or keeps it equal; contracts lower bound",
                    "R--": "Decreases pair sum or keeps it equal; contracts upper bound"
                }
            )

        if pattern == "container_most_water":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maximize area(L, R) = min(h[L], h[R]) * (R - L)",
                decision_conditions={
                    "h[L] <= h[R]": "L++ (increment left pointer)",
                    "h[L] > h[R]": "R-- (decrement right pointer)"
                },
                elimination_proof=(
                    "Let area(L, R) = min(h[L], h[R]) * (R - L).\n"
                    "Assume without loss of generality that h[L] <= h[R].\n"
                    "Consider any inner position k where L < k < R.\n"
                    "The width between L and k is (k - L) < (R - L).\n"
                    "The height min(h[L], h[k]) is at most h[L].\n"
                    "Therefore, area(L, k) = min(h[L], h[k]) * (k - L) <= h[L] * (k - L) < h[L] * (R - L) = area(L, R).\n"
                    "This proves that NO pair (L, k) can possibly exceed the currently inspected area(L, R).\n"
                    "Hence, line L is exhausted and can be safely eliminated by advancing L to L + 1.\n"
                    "Symmetrically, if h[R] < h[L], line R cannot form a larger area with any k > L, so R--."
                ),
                state_updates={
                    "L++": "Discards left vertical boundary that strictly limits maximum potential area",
                    "R--": "Discards right vertical boundary that strictly limits maximum potential area"
                }
            )

        if pattern == "sliding_window_variable_max":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maximize window width (R - L + 1) subject to predicate is_valid(window)",
                decision_conditions={
                    "is_valid(window) == False": "remove(L); L++ (shrink window until validity restored)",
                    "is_valid(window) == True": "max_len = max(max_len, R - L + 1); add(R+1); R++ (expand window)"
                },
                elimination_proof=(
                    "Since the constraint violation is monotonic under addition of elements, "
                    "when window [L..R] is invalid, any window [L'..R] with L' < L is a superset and also invalid. "
                    "Thus, the minimal necessary left endpoint for a valid window ending at R must be at least L + 1. "
                    "Advancing L eliminates invalid prefix configurations without discarding any valid larger window."
                ),
                state_updates={
                    "add(R)": "Incorporates a[R] into state (frequency map, distinct count, etc.)",
                    "remove(L)": "Evicts a[L] from state, decrementing frequency/count, restoring validity",
                    "L++": "Contracts window from left",
                    "R++": "Expands window to the right"
                }
            )

        if pattern == "sliding_window_variable_min":
            target = params.get("target", "S")
            return MovementDerivation(
                pattern=pattern,
                objective_function=f"minimize window width (R - L + 1) subject to sum(window) >= {target}",
                decision_conditions={
                    f"sum >= {target}": "min_len = min(min_len, R - L + 1); sum -= a[L]; L++",
                    f"sum < {target}": "R++ (must expand to accumulate more sum)"
                },
                elimination_proof=(
                    f"Given all elements are non-negative, the window sum is non-decreasing with R and non-increasing with L.\n"
                    f"If window [L..R] has sum >= {target}, it is a candidate for minimal length. Any extension [L..R'] with R' > R "
                    f"has length (R' - L + 1) > (R - L + 1) and cannot be the minimal window starting at L. "
                    f"Therefore, L can be incremented to search for an even smaller valid window ending at R.\n"
                    f"Conversely, if sum < {target}, no subsegment [L'..R] with L' > L can have sum >= {target}, so R must expand."
                ),
                state_updates={
                    "sum += a[R]": "Monotonically increases cumulative window sum",
                    "sum -= a[L]": "Monotonically decreases cumulative window sum",
                    "L++": "Tests smaller window starting at next index",
                    "R++": "Accumulates additional sum to satisfy threshold"
                }
            )

        if pattern == "partition_dutch_flag":
            return MovementDerivation(
                pattern=pattern,
                objective_function="partition array into 3 contiguous regions (< pivot, == pivot, > pivot) in O(N) time and O(1) extra space",
                decision_conditions={
                    "a[mid] < pivot": "swap(a[low], a[mid]); low++; mid++",
                    "a[mid] == pivot": "mid++",
                    "a[mid] > pivot": "swap(a[mid], a[high]); high--"
                },
                elimination_proof=(
                    "The array is maintained with 4 regions:\n"
                    "1. [0..low-1]: all elements strictly less than pivot.\n"
                    "2. [low..mid-1]: all elements strictly equal to pivot.\n"
                    "3. [mid..high]: uninspected elements (the active search space).\n"
                    "4. [high+1..n-1]: all elements strictly greater than pivot.\n"
                    "When a[mid] < pivot: swapped with a[low] (which is guaranteed to be equal to pivot if low < mid), "
                    "so low and mid can both advance.\n"
                    "When a[mid] == pivot: already in region 1, so mid advances.\n"
                    "When a[mid] > pivot: swapped into region 4 at high; high decrements. mid is NOT advanced because the swapped-in "
                    "element from high has not yet been inspected.\n"
                    "In every step, high - mid + 1 decreases by at least 1, guaranteeing O(N) termination."
                ),
                state_updates={
                    "low++": "Expands region < pivot",
                    "mid++": "Expands region == pivot",
                    "high--": "Expands region > pivot"
                }
            )

        if pattern == "palindrome_verification":
            return MovementDerivation(
                pattern=pattern,
                objective_function="verify s[i] == s[n - 1 - i] for all alphanumeric characters",
                decision_conditions={
                    "!isalnum(s[lo])": "lo++ (skip non-alphanumeric character)",
                    "!isalnum(s[hi])": "hi-- (skip non-alphanumeric character)",
                    "tolower(s[lo]) == tolower(s[hi])": "lo++, hi-- (symmetric pair verified)",
                    "tolower(s[lo]) != tolower(s[hi])": "return false (symmetry violated)"
                },
                elimination_proof=(
                    "Palindrome symmetry requires that the i-th character matches the (n - 1 - i)-th character. "
                    "By verifying outermost alphanumeric characters first, any mismatch immediately disproves the property. "
                    "When a match is confirmed, both outermost positions are eliminated, shrinking the uninspected substring."
                ),
                state_updates={
                    "lo++": "Advances left boundary toward center",
                    "hi--": "Advances right boundary toward center"
                }
            )

        if pattern == "in_place_compaction":
            return MovementDerivation(
                pattern=pattern,
                objective_function="retain valid elements in-place while preserving relative order",
                decision_conditions={
                    "predicate(a[fast_read]) == True": "a[slow_write++] = a[fast_read]; fast_read++",
                    "predicate(a[fast_read]) == False": "fast_read++ (skip rejected element)"
                },
                elimination_proof=(
                    "Elements that fail the retention predicate cannot appear in the final compacted prefix. "
                    "Advancing fast_read without incrementing slow_write discards the invalid element in O(1) time "
                    "without shifting subsequent elements or allocating auxiliary storage."
                ),
                state_updates={
                    "slow_write++": "Expands compacted valid prefix",
                    "fast_read++": "Advances scanner to next candidate"
                }
            )

        if pattern == "merge_sorted_arrays":
            return MovementDerivation(
                pattern=pattern,
                objective_function="merge two sorted streams into non-decreasing output",
                decision_conditions={
                    "a[p1] <= b[p2]": "output.push(a[p1++])",
                    "a[p1] > b[p2]": "output.push(b[p2++])"
                },
                elimination_proof=(
                    "Because both input streams are sorted in non-decreasing order, min(a[p1], b[p2]) is guaranteed "
                    "to be less than or equal to all remaining unmerged elements in both arrays. "
                    "Emitting the minimum and advancing its pointer preserves the sorted invariant of the merged output."
                ),
                state_updates={
                    "p1++": "Consumes current smallest element from first array",
                    "p2++": "Consumes current smallest element from second array"
                }
            )

        if pattern == "partition_two_way":
            return MovementDerivation(
                pattern=pattern,
                objective_function="partition array into two contiguous regions in O(N) time and O(1) space",
                decision_conditions={
                    "is_region1(a[left])": "left++",
                    "is_region2(a[right])": "right--",
                    "else": "swap(a[left], a[right]); left++; right--"
                },
                elimination_proof=(
                    "If a[left] belongs to region 1, it is already correctly positioned. "
                    "If a[right] belongs to region 2, it is already correctly positioned. "
                    "If both are misplaced, swapping them places both in their correct regions simultaneously, "
                    "strictly shrinking the uninspected interval [left..right] by 2."
                ),
                state_updates={
                    "left++": "Expands region 1 from the left",
                    "right--": "Expands region 2 from the right"
                }
            )

        if pattern == "linked_middle_node":
            return MovementDerivation(
                pattern=pattern,
                objective_function="locate middle node of linked list in one pass with O(1) space",
                decision_conditions={
                    "fast != null && fast.next != null": "slow = slow.next; fast = fast.next.next",
                    "fast == null || fast.next == null": "return slow (middle reached)"
                },
                elimination_proof=(
                    "For every single step slow takes, fast takes two steps. "
                    "When fast reaches the end of a list of length L, slow has taken floor(L / 2) steps, "
                    "positioning slow directly at the middle node."
                ),
                state_updates={
                    "slow = slow.next": "Advances 1 node",
                    "fast = fast.next.next": "Advances 2 nodes"
                }
            )

        if pattern == "linked_cycle_start":
            return MovementDerivation(
                pattern=pattern,
                objective_function="locate cycle entrance node using Floyd's phase 2",
                decision_conditions={
                    "ptr1 != ptr2": "ptr1 = ptr1.next; ptr2 = ptr2.next",
                    "ptr1 == ptr2": "return ptr1 (cycle entry node found)"
                },
                elimination_proof=(
                    "Let distance from head to cycle entry be H, and cycle length be C. "
                    "The meeting node in phase 1 is at distance C - (H mod C) from the entry. "
                    "Resetting ptr1 to head and advancing both at speed 1 causes them to meet after exactly H steps at the cycle entrance."
                ),
                state_updates={
                    "ptr1 = ptr1.next": "Advances 1 node from head",
                    "ptr2 = ptr2.next": "Advances 1 node from meeting point"
                }
            )

        if pattern == "closest_pair_sum":
            target = params.get("target", "target")
            return MovementDerivation(
                pattern=pattern,
                objective_function=f"minimize |A[L] + A[R] - {target}|",
                decision_conditions={
                    "A[L] + A[R] < target": "L++ (increase sum toward target)",
                    "A[L] + A[R] > target": "R-- (decrease sum toward target)",
                    "A[L] + A[R] == target": "terminate (distance 0 is optimal)"
                },
                elimination_proof=(
                    f"If A[L] + A[R] < {target}: for any k < R, A[L] + A[k] <= A[L] + A[R] < {target}, "
                    f"so A[L] + A[k] is strictly farther from {target} than A[L] + A[R]. "
                    f"Index L is permanently exhausted and L++ safely eliminates L."
                ),
                state_updates={
                    "L++": "Contracts lower boundary, strictly increases lower candidate",
                    "R--": "Contracts upper boundary, strictly decreases upper candidate"
                }
            )

        if pattern in ("three_sum_converging", "four_sum_converging"):
            return MovementDerivation(
                pattern=pattern,
                objective_function="find all unique tuples summing to target without duplicates",
                decision_conditions={
                    "cur_sum < target": "L++",
                    "cur_sum > target": "R--",
                    "cur_sum == target": "record tuple; while (L < R && A[L] == A[L+1]) L++; while (L < R && A[R] == A[R-1]) R--; L++; R--;"
                },
                elimination_proof=(
                    "Sorting the array allows fixing outer indices and running converging two pointers. "
                    "Skipping duplicate elements in both outer loops and inner pointer updates guarantees "
                    "that each distinct value combination is emitted exactly once in O(N^(k-1)) time."
                ),
                state_updates={
                    "L++": "Eliminates smaller duplicate elements",
                    "R--": "Eliminates larger duplicate elements"
                }
            )

        if pattern == "trapping_rain_water":
            return MovementDerivation(
                pattern=pattern,
                objective_function="accumulate sum(max(0, min(left_max[i], right_max[i]) - height[i]))",
                decision_conditions={
                    "height[left] < height[right]": "process left column, update left_max, left++",
                    "height[left] >= height[right]": "process right column, update right_max, right--"
                },
                elimination_proof=(
                    "If height[left] < height[right], we know left_max is strictly less than or equal to height[right], "
                    "which means the water trapped at 'left' is strictly bounded by left_max regardless of future right bars. "
                    "Thus, left can be finalized and safely advanced via left++."
                ),
                state_updates={
                    "left++": "Advances left boundary, accumulates trapped water above left bar",
                    "right--": "Advances right boundary, accumulates trapped water above right bar"
                }
            )

        if pattern == "move_zeroes_ordered":
            return MovementDerivation(
                pattern=pattern,
                objective_function="shift zeroes to end in-place while preserving relative non-zero order",
                decision_conditions={
                    "A[fast] != 0": "A[slow++] = A[fast]; fast++",
                    "A[fast] == 0": "fast++ (skip zero without moving slow)"
                },
                elimination_proof=(
                    "The slow pointer points to the boundary of the compacted non-zero prefix. "
                    "The fast pointer scans every element. Writing only non-zero elements to slow preserves their relative order. "
                    "Trailing positions [slow..n-1] are zero-filled after the scan."
                ),
                state_updates={
                    "slow++": "Expands non-zero prefix",
                    "fast++": "Advances exploration scanner"
                }
            )

        if pattern == "chase_pointer_difference":
            diff = params.get("diff", "diff")
            return MovementDerivation(
                pattern=pattern,
                objective_function=f"find distinct pair (i, j) such that A[j] - A[i] == {diff}",
                decision_conditions={
                    "A[j] - A[i] < diff": "j++",
                    "A[j] - A[i] > diff": "i++",
                    "A[j] - A[i] == diff && i != j": "match found",
                    "i == j": "j++"
                },
                elimination_proof=(
                    f"Array is sorted. If A[j] - A[i] < {diff}: for any k <= i, A[j] - A[k] >= A[j] - A[i], but to increase the difference "
                    f"relative to i we must advance j. If A[j] - A[i] > {diff}, advancing i decreases the difference toward {diff}."
                ),
                state_updates={
                    "i++": "Decreases pair difference",
                    "j++": "Increases pair difference"
                }
            )

        if pattern == "count_pairs_less_than_k":
            k_val = params.get("k", "K")
            return MovementDerivation(
                pattern=pattern,
                objective_function=f"count pairs (i, j) with i < j such that A[i] + A[j] < {k_val}",
                decision_conditions={
                    "A[L] + A[R] < K": "count += (R - L); L++",
                    "A[L] + A[R] >= K": "R--"
                },
                elimination_proof=(
                    f"Because A is sorted non-decreasingly, if A[L] + A[R] < {k_val}, then for any m in [L + 1, R], "
                    f"A[L] + A[m] <= A[L] + A[R] < {k_val}. Thus all (R - L) elements paired with L are strictly valid. "
                    f"Adding (R - L) and advancing L to L + 1 completely counts all valid pairs with L and safely eliminates L."
                ),
                state_updates={
                    "L++": f"Adds (R - L) to total count; advances lower bound",
                    "R--": "Discards R as it cannot pair with any element >= L"
                }
            )

        if pattern == "count_subarrays_bounded":
            return MovementDerivation(
                pattern=pattern,
                objective_function="count contiguous subarrays satisfying running bounded constraint",
                decision_conditions={
                    "window valid": "count += (right - left + 1); right++",
                    "window invalid": "remove A[left++]; keep right fixed until valid"
                },
                elimination_proof=(
                    "For a fixed right endpoint, if A[left..right] satisfies the condition, all (right - left + 1) "
                    "contiguous subarrays ending at 'right' with starting points in [left..right] are valid by monotonicity. "
                    "Adding (right - left + 1) exhaustively counts all valid subarrays ending at right."
                ),
                state_updates={
                    "right++": "Expands window by incorporating next element",
                    "left++": "Shrinks window to restore validity"
                }
            )

        if pattern == "exact_count_derived":
            return MovementDerivation(
                pattern=pattern,
                objective_function="compute count where distinct elements == K",
                decision_conditions={
                    "derived": "count = atMost(K) - atMost(K - 1)"
                },
                elimination_proof=(
                    "An exact constraint is non-monotonic with respect to window shrinking, but atMost(K) is monotonic. "
                    "Decomposing exact(K) = atMost(K) - atMost(K - 1) evaluates two monotonic sliding windows in O(N) time."
                ),
                state_updates={
                    "atMost(k)": "Sliding window with frequency map"
                }
            )

        if pattern == "minimum_window_substring":
            return MovementDerivation(
                pattern=pattern,
                objective_function="minimize (right - left + 1) such that window contains all characters in target",
                decision_conditions={
                    "match_count < required": "incorporate S[right++]; update window frequency and match count",
                    "match_count == required": "record min length; remove S[left++]; if frequency falls below target, match_count--"
                },
                elimination_proof=(
                    "Advancing left while match_count == required finds the minimal valid window starting at left. "
                    "Once match_count drops below required, no smaller window starting at left can be valid, so right expands."
                ),
                state_updates={
                    "right++": "Expands covering span",
                    "left++": "Shrinks window seeking minimal length"
                }
            )

        # ── Monotonic Stack Movement / Pop-Push Derivations (Phase 3B) ──
        # Each derivation includes the elimination proof: why popping is permanently safe.

        if pattern in ("next_greater_element", "circular_next_greater"):
            suffix = " Array is traversed twice: i in [0, 2n), index = i % n." if pattern == "circular_next_greater" else ""
            return MovementDerivation(
                pattern=pattern,
                objective_function="for each index j, find the smallest i > j such that arr[i] > arr[j]." + suffix,
                decision_conditions={
                    "arr[i] > arr[stack.top()]": "pop stack.top() j; result[j] = arr[i]; repeat",
                    "arr[i] <= arr[stack.top()] or stack empty": "push i onto stack"
                },
                elimination_proof=(
                    "Dominance proof for pop (arr[i] > arr[j] where j = stack.top()):\n"
                    "1. j is on the stack because its next greater element has not yet been found.\n"
                    "2. i > j (we scan left to right), so i is to the right of j.\n"
                    "3. arr[i] > arr[j] satisfies the 'greater' relation.\n"
                    "4. For any future index k > i: k is even further right than i.\n"
                    "   Since i is already to j's right and satisfies the condition, i is the FIRST such index.\n"
                    "5. Therefore i definitively resolves j. j is permanently popped.\n"
                    "Push i: i now becomes a candidate seeking its own next greater element, "
                    "and arr[i] >= arr[previous_stack_top] (by the clearing loop), maintaining the decreasing invariant."
                ),
                state_updates={
                    "stack.pop()": "resolves next greater element for the popped index",
                    "result[j] = arr[i]": "records the first greater element to the right",
                    "stack.push(i)": "i becomes a new candidate; stack invariant restored"
                }
            )

        if pattern == "next_smaller_element":
            return MovementDerivation(
                pattern=pattern,
                objective_function="for each index j, find the smallest i > j such that arr[i] < arr[j].",
                decision_conditions={
                    "arr[i] < arr[stack.top()]": "pop stack.top() j; result[j] = arr[i]; repeat",
                    "arr[i] >= arr[stack.top()] or stack empty": "push i onto stack"
                },
                elimination_proof=(
                    "Dominance proof for pop (arr[i] < arr[j] where j = stack.top()):\n"
                    "1. j is on stack seeking its next smaller element.\n"
                    "2. i > j (left-to-right scan), so i is strictly to the right.\n"
                    "3. arr[i] < arr[j] satisfies 'smaller' relation.\n"
                    "4. Any future k > i would be further right; i is the FIRST satisfying index.\n"
                    "5. j is permanently resolved. Stack maintains non-decreasing order after push(i)."
                ),
                state_updates={
                    "stack.pop()": "resolves next smaller for the popped index",
                    "result[j] = arr[i]": "records the first smaller element to the right",
                    "stack.push(i)": "i added as a new candidate"
                }
            )

        if pattern == "previous_greater_element":
            return MovementDerivation(
                pattern=pattern,
                objective_function="for each index i, find the largest j < i such that arr[j] > arr[i].",
                decision_conditions={
                    "arr[stack.top()] <= arr[i]": "pop stack.top(); it cannot be the answer for i or any future right-neighbor",
                    "stack non-empty after pops": "result[i] = arr[stack.top()]",
                    "stack empty after pops": "result[i] = -1 (no previous greater)",
                },
                elimination_proof=(
                    "Dominance proof for pop (arr[stack.top()] <= arr[i]):\n"
                    "1. arr[stack.top()] <= arr[i]. For any index k > i to be processed later:\n"
                    "   arr[i] is between stack.top() and k. If arr[k] needs a previous greater element,\n"
                    "   arr[i] >= arr[stack.top()] means arr[i] dominates arr[stack.top()] from the left.\n"
                    "2. Therefore arr[stack.top()] can never be the nearest previous greater of any future k.\n"
                    "3. stack.top() is safely and permanently eliminated."
                ),
                state_updates={
                    "stack.pop()": "eliminates a dominated candidate",
                    "result[i] = arr[stack.top()]": "nearest previous greater found",
                    "stack.push(i)": "i added as a candidate for future indices"
                }
            )

        if pattern == "previous_smaller_element":
            return MovementDerivation(
                pattern=pattern,
                objective_function="for each index i, find the largest j < i such that arr[j] < arr[i].",
                decision_conditions={
                    "arr[stack.top()] >= arr[i]": "pop stack.top(); dominated by arr[i] for future queries",
                    "stack non-empty after pops": "result[i] = arr[stack.top()]",
                    "stack empty after pops": "result[i] = -1"
                },
                elimination_proof=(
                    "Dominance proof for pop (arr[stack.top()] >= arr[i]):\n"
                    "1. arr[i] <= arr[stack.top()]. For any future index k > i:\n"
                    "   if arr[k] > arr[i], then arr[k] > arr[stack.top()] as well (since arr[i] <= arr[stack.top()]).\n"
                    "   But arr[i] is closer to k than arr[stack.top()], so arr[i] would shadow arr[stack.top()].\n"
                    "2. Conversely if arr[k] <= arr[i] <= arr[stack.top()], neither is the previous smaller.\n"
                    "3. Therefore arr[stack.top()] can never be the nearest previous smaller for any future k."
                ),
                state_updates={
                    "stack.pop()": "dominated candidate eliminated",
                    "result[i] = arr[stack.top()]": "nearest previous smaller found",
                    "stack.push(i)": "i becomes a candidate for future elements"
                }
            )

        if pattern in ("nearest_greater_element", "nearest_smaller_element"):
            relation = "greater" if "greater" in pattern else "smaller"
            return MovementDerivation(
                pattern=pattern,
                objective_function=f"for each index i, find the nearest index j (either left or right) such that arr[j] {'>=' if relation == 'greater' else '<='} arr[i]. Return min(distance_left, distance_right).",
                decision_conditions={
                    "Pass 1 (right-to-left for previous)": f"pop when arr[stack.top()] {'<=' if relation == 'greater' else '>='} arr[i]",
                    "Pass 2 (left-to-right for next)": f"pop when arr[i] {'>=' if relation == 'greater' else '<='} arr[stack.top()]"
                },
                elimination_proof=(
                    f"Two independent elimination passes:\n"
                    f"Pass 1: eliminates candidates that cannot be the nearest previous {relation} for any future query.\n"
                    f"Pass 2: eliminates candidates that cannot be the nearest next {relation} for any past query.\n"
                    f"Each pass uses the same dominance argument as previous_{relation}_element and next_{relation}_element respectively."
                ),
                state_updates={
                    "left_dist[i]": "distance to nearest previous boundary (from pass 1)",
                    "right_dist[i]": "distance to nearest next boundary (from pass 2)",
                    "result[i]": "min(left_dist[i], right_dist[i])"
                }
            )

        if pattern == "stock_span":
            return MovementDerivation(
                pattern=pattern,
                objective_function="span[i] = number of consecutive days (including day i) for which price <= price[i].",
                decision_conditions={
                    "price[stack.top()] <= price[i]": "pop; that day's price is dominated by today's price",
                    "price[stack.top()] > price[i] or stack empty": "span[i] = i - stack.top() (or i+1 if empty). Push i."
                },
                elimination_proof=(
                    "Dominance proof for pop (price[stack.top()] <= price[i]):\n"
                    "1. Let j = stack.top(). price[j] <= price[i].\n"
                    "2. For any future day k > i: if price[k] > price[j], then also price[k] > price[i] (but irrelevant).\n"
                    "   More importantly: price[i] >= price[j], and i is between j and k.\n"
                    "   Therefore j can never be the nearest previous day with price > price[k] before encountering i.\n"
                    "3. j is permanently dominated for all future span queries. Safely popped."
                ),
                state_updates={
                    "stack.pop()": "eliminates dominated historical day",
                    "span[i] = i - stack.top()": "computes span as distance to previous greater-price day",
                    "stack.push(i)": "today added as future left boundary candidate"
                }
            )

        if pattern == "largest_rectangle_histogram":
            return MovementDerivation(
                pattern=pattern,
                objective_function="max area = max over all bars j of: height[j] * (right_boundary[j] - left_boundary[j] - 1).",
                decision_conditions={
                    "height[i] < height[stack.top()]": "pop j; compute area using i as right boundary; repeat",
                    "height[i] >= height[stack.top()] or stack empty": "push i"
                },
                elimination_proof=(
                    "Dominance proof for pop (height[i] < height[j] where j = stack.top()):\n"
                    "1. height[i] < height[j]. Bar i limits any rectangle extending through it to height < height[j].\n"
                    "2. The maximum rectangle with height = height[j] cannot extend past index i to the right.\n"
                    "   Its right boundary is definitively i.\n"
                    "3. Its left boundary: the new stack top after popping is the previous bar with height < height[j].\n"
                    "   Width = i - new_stack_top - 1.\n"
                    "4. No wider rectangle with height = height[j] is achievable (blocked on both sides by shorter bars).\n"
                    "5. j is permanently resolved. Area = height[j] * width. Flush remaining at i=n."
                ),
                state_updates={
                    "j = stack.pop()": "bar j's maximum rectangle computed",
                    "width = i - stack[-1] - 1": "width using previous stack element as left boundary",
                    "max_area = max(max_area, height[j] * width)": "global optimum updated",
                    "stack.push(i)": "bar i becomes new active left boundary candidate"
                }
            )

        if pattern in ("sum_subarray_minimums", "sum_subarray_maximums"):
            objective = "minimum" if pattern == "sum_subarray_minimums" else "maximum"
            compare_left = "<" if pattern == "sum_subarray_minimums" else ">"
            compare_right = "<=" if pattern == "sum_subarray_minimums" else ">="
            MOD = "10**9 + 7"
            return MovementDerivation(
                pattern=pattern,
                objective_function=f"sum of {objective}(arr[l..r]) for all 0 <= l <= r < n, modulo {MOD}.",
                decision_conditions={
                    f"Pass 1 (left[i]): pop while arr[stack.top()] {compare_left} arr[i]": f"strict comparison prevents double-counting when equal elements exist",
                    f"Pass 2 (right[i]): pop while arr[stack.top()] {compare_right} arr[i]": f"non-strict comparison on the other side"
                },
                elimination_proof=(
                    f"For each element arr[i]:\n"
                    f"  left[i] = i - (index of nearest element strictly {compare_left} arr[i] to the left, or -1)\n"
                    f"  right[i] = (index of nearest element {'<' if compare_right == '<=' else '>'} arr[i] to the right, or n) - i\n"
                    f"  contribution[i] = arr[i] * left[i] * right[i]\n"
                    f"Strictness convention: for duplicates arr[j] == arr[i], only one boundary is strict.\n"
                    f"This ensures each subarray is counted exactly once for its {objective}.\n"
                    f"Proof: arr[i] is the {objective} of exactly left[i]*right[i] subarrays by construction of boundaries."
                ),
                state_updates={
                    "left[i]": f"number of consecutive subarrays ending at i where arr[i] is {objective} (looking left)",
                    "right[i]": f"number of consecutive subarrays starting at i where arr[i] is {objective} (looking right)",
                    f"ans += arr[i] * left[i] * right[i]": f"arr[i]'s total contribution to the sum"
                }
            )

        # ── Monotonic Boundary / Binary Search Derivations (Phase 3C) ──

        if pattern == "binary_search_exact":
            return MovementDerivation(
                pattern=pattern,
                objective_function="Find index i such that arr[i] == target in a sorted array, or return -1 if absent.",
                decision_conditions={
                    "arr[mid] == target": "target matched exactly; return mid",
                    "arr[mid] < target": "target is strictly greater; eliminate [lo..mid], set lo = mid + 1",
                    "arr[mid] > target": "target is strictly smaller; eliminate [mid..hi], set hi = mid - 1"
                },
                elimination_proof=(
                    "Half-Elimination Proof (Exact Lookup):\n"
                    "1. Midpoint computation: mid = lo + (hi - lo) / 2. This is mathematically equivalent to (lo + hi) / 2 "
                    "   but provably avoids integer overflow when lo + hi exceeds the maximum representable integer.\n"
                    "2. Since arr is sorted, for any k <= mid, arr[k] <= arr[mid].\n"
                    "   If arr[mid] < target, then for all k <= mid: arr[k] <= arr[mid] < target.\n"
                    "   Hence, target cannot exist at any index in [lo..mid]. Setting lo = mid + 1 is safe.\n"
                    "3. Conversely, if arr[mid] > target, then for all k >= mid: arr[k] >= arr[mid] > target.\n"
                    "   Target cannot exist in [mid..hi]. Setting hi = mid - 1 is safe.\n"
                    "4. Termination: if lo > hi, every index has been eliminated with mathematical certainty. Output -1."
                ),
                state_updates={
                    "lo = mid + 1": "eliminates [lo..mid]; search moves right",
                    "hi = mid - 1": "eliminates [mid..hi]; search moves left"
                }
            )

        if pattern in ("lower_bound", "first_true", "successor"):
            rel_name = "arr[i] >= target" if pattern in ("lower_bound", "successor") else "P(i) == true"
            return MovementDerivation(
                pattern=pattern,
                objective_function=f"Find the minimal index i such that {rel_name}.",
                decision_conditions={
                    f"{rel_name} is true at mid": "mid is a valid candidate; first true must be <= mid; set hi = mid",
                    f"{rel_name} is false at mid": "mid and all earlier elements are false; first true must be > mid; set lo = mid + 1"
                },
                elimination_proof=(
                    f"Half-Elimination Proof (First True / Lower Bound):\n"
                    f"1. Monotonicity: P(i) satisfies false ... false true ... true.\n"
                    f"2. If P(mid) == true: mid is feasible. Any index k > mid cannot be the FIRST true "
                    f"   because mid is strictly smaller and already true. Thus (mid..hi] is eliminated, and hi = mid.\n"
                    f"3. If P(mid) == false: all k <= mid must also be false by monotonicity. "
                    f"   Thus [lo..mid] contains no satisfying index, and lo = mid + 1 safely eliminates this segment.\n"
                    f"4. Termination: lo == hi isolates the unique transition boundary in exactly ceil(log2(N)) iterations."
                ),
                state_updates={
                    "hi = mid": "discards right half (mid..hi]; candidate answer remains <= mid",
                    "lo = mid + 1": "discards left half [lo..mid]; candidate answer must be > mid"
                }
            )

        if pattern == "upper_bound":
            return MovementDerivation(
                pattern=pattern,
                objective_function="Find the minimal index i such that arr[i] > target in sorted array.",
                decision_conditions={
                    "arr[mid] > target": "mid is strictly greater; first index > target is <= mid; set hi = mid",
                    "arr[mid] <= target": "mid and all elements before it are <= target; set lo = mid + 1"
                },
                elimination_proof=(
                    "Half-Elimination Proof (Upper Bound):\n"
                    "1. Since arr is sorted, condition arr[i] > target is monotonic false -> true.\n"
                    "2. If arr[mid] > target: mid satisfies condition; the first such index is at or before mid. Set hi = mid.\n"
                    "3. If arr[mid] <= target: for all k <= mid, arr[k] <= arr[mid] <= target. None can exceed target. Set lo = mid + 1.\n"
                    "4. Termination: lo == hi identifies the first index strictly greater than target."
                ),
                state_updates={
                    "hi = mid": "narrows upper bound candidate window to [lo..mid]",
                    "lo = mid + 1": "discards [lo..mid] as <= target"
                }
            )

        if pattern in ("last_true", "predecessor", "first_false", "last_false"):
            cond_desc = "arr[mid] < target" if pattern == "predecessor" else "P(mid) == true"
            return MovementDerivation(
                pattern=pattern,
                objective_function=f"Find the maximal index i satisfying {cond_desc}.",
                decision_conditions={
                    f"{cond_desc} holds": "mid satisfies condition; record ans = mid, explore larger indices with lo = mid + 1",
                    f"{cond_desc} fails": "mid violates condition; by monotonicity all k >= mid violate; set hi = mid - 1"
                },
                elimination_proof=(
                    "Half-Elimination Proof (Last True / Predecessor):\n"
                    "1. Condition is monotonic true ... true false ... false.\n"
                    "2. When mid satisfies the condition: mid is feasible, but a larger index might also be feasible. "
                    "   We store ans = mid and advance lo = mid + 1 to explore the remaining right half.\n"
                    "3. When mid fails: no index k >= mid can satisfy the condition. Setting hi = mid - 1 eliminates [mid..hi].\n"
                    "4. Termination: when lo > hi, ans holds the maximum index that satisfied the condition, or -1."
                ),
                state_updates={
                    "ans = mid; lo = mid + 1": "records feasible candidate and tests larger candidates",
                    "hi = mid - 1": "eliminates infeasible suffix [mid..hi]"
                }
            )

        if pattern == "binary_search_answer_min":
            return MovementDerivation(
                pattern=pattern,
                objective_function="Minimize maximum answer value X such that feasibility(X) is true.",
                decision_conditions={
                    "feasible(mid) == true": "capacity/load mid is sufficient; minimal value is <= mid; set hi = mid",
                    "feasible(mid) == false": "capacity/load mid is insufficient; minimal value must be > mid; set lo = mid + 1"
                },
                elimination_proof=(
                    "Transformation & Monotonicity Proof (Answer Space Min):\n"
                    "1. Optimization problem: min X subject to task constraints.\n"
                    "2. Feasibility transformation: let P(X) = 'Can the goal be achieved with parameter <= X?'\n"
                    "3. Monotonicity: If X is feasible, any X' > X allows at least as much slack, hence P(X') is also true. "
                    "   P(X) is monotonic false -> true across [min_bound, max_bound].\n"
                    "4. Elimination: If P(mid) is true, hi = mid retains all potentially smaller feasible values while mid is safe. "
                    "   If P(mid) is false, all X <= mid are impossible; lo = mid + 1 permanently eliminates them.\n"
                    "5. Overflow safety: mid = lo + (hi - lo) / 2 using 64-bit integer arithmetic (long long)."
                ),
                state_updates={
                    "hi = mid": "retains feasible mid and explores smaller feasible answers",
                    "lo = mid + 1": "discards infeasible prefix [lo..mid]"
                }
            )

        if pattern == "binary_search_answer_max":
            return MovementDerivation(
                pattern=pattern,
                objective_function="Maximize minimum answer value D such that feasibility(D) is true.",
                decision_conditions={
                    "feasible(mid) == true": "distance/threshold mid is achievable; record ans = mid, test larger with lo = mid + 1",
                    "feasible(mid) == false": "distance/threshold mid is unachievable; set hi = mid - 1"
                },
                elimination_proof=(
                    "Transformation & Monotonicity Proof (Answer Space Max):\n"
                    "1. Optimization problem: max D subject to separation/threshold constraints.\n"
                    "2. Feasibility transformation: let P(D) = 'Can requirements be met with parameter >= D?'\n"
                    "3. Monotonicity: If D is achievable, any D' < D relaxes constraints, so P(D') is also true. "
                    "   P(D) is monotonic true -> false across [min_bound, max_bound].\n"
                    "4. Elimination: If P(mid) is true, ans = mid and lo = mid + 1 seeks larger valid thresholds. "
                    "   If P(mid) is false, no D >= mid can be valid; hi = mid - 1 permanently eliminates [mid..hi].\n"
                    "5. Termination: lo > hi terminates with ans holding the globally maximal achievable threshold."
                ),
                state_updates={
                    "ans = mid; lo = mid + 1": "records achievable threshold and searches right for larger values",
                    "hi = mid - 1": "discards unachievable suffix [mid..hi]"
                }
            )

        if pattern == "binary_search_value_domain":
            return MovementDerivation(
                pattern=pattern,
                objective_function="Find exact integer root or boundary x in [lo, hi] satisfying arithmetic condition f(x) <= target.",
                decision_conditions={
                    "f(mid) <= target": "mid is valid; record ans = mid, test larger with lo = mid + 1",
                    "f(mid) > target": "mid is too large; set hi = mid - 1"
                },
                elimination_proof=(
                    "Value Domain Elimination Proof:\n"
                    "1. Arithmetic function f(x) is monotonically increasing for non-negative integers x.\n"
                    "2. Compute mid = lo + (hi - lo) / 2 using 64-bit integers to prevent multiplication overflow (mid * mid).\n"
                    "3. If f(mid) <= target: mid is valid floor; ans = mid, lo = mid + 1 explores larger integers.\n"
                    "4. If f(mid) > target: all k >= mid have f(k) > target; hi = mid - 1 eliminates [mid..hi].\n"
                    "5. Output ans after convergence."
                ),
                state_updates={
                    "ans = mid; lo = mid + 1": "saves best valid floor and explores higher domain values",
                    "hi = mid - 1": "discards domain segment that exceeds target"
                }
            )

        # ── Trie Movement Derivations (Phase 3D) ──
        if pattern == "trie_insert":
            return MovementDerivation(
                pattern=pattern,
                objective_function="Insert word w into Trie, maintaining prefix sharing and dual counters.",
                decision_conditions={
                    "child[c] == nullptr": "create new TrieNode for character c",
                    "child[c] != nullptr": "reuse existing node sharing prefix"
                },
                elimination_proof=(
                    "Trie Insertion Transition Proof:\n"
                    "1. For each character c in w, increment curr->pass_count++.\n"
                    "2. Follow edge child[c] (allocating if null) to advance prefix from w[0..i-1] to w[0..i].\n"
                    "3. At word end, increment curr->word_count++.\n"
                    "4. Guarantees O(L) time where L is word length, independent of dictionary size."
                ),
                state_updates={
                    "curr->pass_count++": "tracks count of words traversing through this node",
                    "curr = curr->child[c]": "advances state along deterministic character edge",
                    "curr->word_count++": "marks word termination with multiplicity"
                }
            )

        if pattern in ("trie_exact_search", "trie_prefix_search"):
            is_prefix = (pattern == "trie_prefix_search")
            return MovementDerivation(
                pattern=pattern,
                objective_function="Traverse Trie along string characters to test existence.",
                decision_conditions={
                    "child[c] == nullptr": "path missing; query string does not exist in dictionary",
                    "child[c] != nullptr": "continue following character transition edge"
                },
                elimination_proof=(
                    "Deterministic Prefix Traversal Proof:\n"
                    "1. Because each edge labels a unique character, there is at most one path representing prefix P.\n"
                    "2. If at any character c, child[c] is null, no word in dictionary has P as prefix.\n"
                    f"3. At string end: {'return curr->pass_count > 0' if is_prefix else 'return curr->word_count > 0'}."
                ),
                state_updates={
                    "curr = curr->child[c]": "advances automaton state along matching edge"
                }
            )

        if pattern in ("trie_prefix_count", "trie_word_count"):
            is_word = (pattern == "trie_word_count")
            return MovementDerivation(
                pattern=pattern,
                objective_function=f"Count occurrences of {'word' if is_word else 'prefix'} in dictionary.",
                decision_conditions={
                    "child[c] == nullptr": "path missing; return 0",
                    "child[c] != nullptr": "traverse to child[c]"
                },
                elimination_proof=(
                    f"Multiplicity Query Proof:\n"
                    f"1. Dual counters explicitly maintain aggregate counts: pass_count for prefix, word_count for exact word.\n"
                    f"2. Follow edges to target node; return {'curr->word_count' if is_word else 'curr->pass_count'}."
                ),
                state_updates={
                    "curr = curr->child[c]": "transitions to child state"
                }
            )

        if pattern == "trie_deletion":
            return MovementDerivation(
                pattern=pattern,
                objective_function="Remove one instance of word from Trie and safely prune dead branches.",
                decision_conditions={
                    "word_count == 0": "word not in dictionary, abort without mutation",
                    "pass_count == 0": "safe to prune and deallocate child node"
                },
                elimination_proof=(
                    "Safe Deletion & Pruning Proof:\n"
                    "1. First verify word presence (word_count > 0).\n"
                    "2. Decrement pass_count on all nodes along word's path; decrement word_count at leaf.\n"
                    "3. Prune child pointer if and only if child->pass_count == 0.\n"
                    "4. Guarantees no other dictionary word's path is accidentally unlinked."
                ),
                state_updates={
                    "curr->pass_count--": "decrements active path count",
                    "curr->word_count--": "decrements instance multiplicity",
                    "delete child; child = nullptr": "safely reclaims unreferenced node"
                }
            )

        if pattern in ("trie_max_xor_pair", "trie_max_xor_query"):
            return MovementDerivation(
                pattern=pattern,
                objective_function="Find maximum bitwise XOR using 32-bit binary trie.",
                decision_conditions={
                    "child[1 - bit] != nullptr": "take opposite branch (secures 1 at current bit level)",
                    "child[1 - bit] == nullptr": "forced to take same bit branch (yields 0 at current bit level)"
                },
                elimination_proof=(
                    "Binary Trie Greedy Choice Proof:\n"
                    "1. Highest bit k contributes 2^k to the XOR sum.\n"
                    "2. sum_{j=0}^{k-1} 2^j = 2^k - 1 < 2^k.\n"
                    "3. Securing 1 at bit k strictly beats achieving 1 at all lower bits 0..k-1 combined.\n"
                    "4. Choosing child[1 - bit] when available is mathematically optimal and eliminates all other subtrees."
                ),
                state_updates={
                    "xor_val |= (1U << k); curr = curr->child[1 - bit]": "takes opposite branch and sets bit",
                    "curr = curr->child[bit]": "falls back to existing branch"
                }
            )

        if pattern in ("trie_lexicographic_sort", "trie_autocomplete"):
            return MovementDerivation(
                pattern=pattern,
                objective_function="Traverse Trie in lexicographical character order to collect words.",
                decision_conditions={
                    "child != nullptr": "recursively explore subtree in ascending character order",
                    "word_count > 0": "emit word with multiplicity"
                },
                elimination_proof=(
                    "Lexicographical In-Order Traversal Proof:\n"
                    "1. Child edges sorted by character (0..25 or map order) guarantee strictly lexicographical order.\n"
                    "2. In-order DFS visits prefixes before extensions and lower characters before higher characters.\n"
                    "3. Time complexity is O(total_characters), outperforming O(N * L * log N) comparison sort."
                ),
                state_updates={
                    "dfs(child, prefix + c)": "recurses in ascending character order"
                }
            )

        # ── Tree Movement Derivations (Phase 3E) ──
        if pattern == "tree_bst_search":
            return MovementDerivation(
                pattern=pattern,
                objective_function="Locate key k in BST via BST ordered-branch elimination.",
                decision_conditions={
                    "k < u->val": "descend left (u = u->left)",
                    "k > u->val": "descend right (u = u->right)",
                    "k == u->val": "target node found"
                },
                elimination_proof=(
                    "BST Ordered-Branch Elimination Proof:\n"
                    "1. BST invariant: for every node u, all keys in left subtree are < u->val, and all keys in right subtree are > u->val.\n"
                    "2. If k < u->val: by transitivity, for all y in right subtree, y > u->val > k. Hence, no node in right subtree can equal k.\n"
                    "3. Right subtree is safely eliminated; search space reduces strictly to left subtree.\n"
                    "4. Symmetrically, if k > u->val, left subtree is eliminated. Achieves O(H) complexity without candidate loss."
                ),
                state_updates={
                    "u = u->left": "eliminates entire right subtree",
                    "u = u->right": "eliminates entire left subtree"
                }
            )

        if pattern in ("tree_bst_insert", "tree_bst_delete", "tree_bst_min_max", "tree_bst_pred_succ"):
            return MovementDerivation(
                pattern=pattern,
                objective_function="Perform BST mutation or extreme search via BST ordered-branch elimination.",
                decision_conditions={
                    "key < u->val": "branch left",
                    "key > u->val": "branch right",
                    "key == u->val": "target site reached"
                },
                elimination_proof=(
                    "BST Ordered-Branch Elimination Mutation Proof:\n"
                    "1. Guided descent eliminates non-candidate branches at each step based on key ordering.\n"
                    "2. Insertion attaches new leaf preserving ancestor range constraints (low, high).\n"
                    "3. Deletion substitutes inorder successor when two children exist, preserving binary search invariant."
                ),
                state_updates={
                    "u = u->left / u->right": "advances down active branch",
                    "mutation": "updates pointer or replaces node value"
                }
            )

        if pattern == "tree_bst_validate":
            return MovementDerivation(
                pattern=pattern,
                objective_function="Verify all nodes satisfy BST ordered bounds (low, high).",
                decision_conditions={
                    "u->val <= low || u->val >= high": "BST invariant violated; return false",
                    "low < u->val < high": "node valid; recurse on left (low, u->val) and right (u->val, high)"
                },
                elimination_proof=(
                    "BST Validation Invariant Proof:\n"
                    "1. Local check (left < node < right) is insufficient because a right child's left descendant could be smaller than grandparent.\n"
                    "2. Passing inherited range (low, high) ensures every node satisfies transitive ancestor constraints.\n"
                    "3. If all subtrees satisfy bounded ranges, tree is globally a valid BST."
                ),
                state_updates={
                    "validate(u->left, low, u->val)": "restricts upper bound for left subtree",
                    "validate(u->right, u->val, high)": "restricts lower bound for right subtree"
                }
            )

        if pattern == "tree_lca_bst":
            return MovementDerivation(
                pattern=pattern,
                objective_function="Find LCA of p and q in BST via BST ordered-branch elimination.",
                decision_conditions={
                    "p->val < u->val && q->val < u->val": "descend left (u = u->left)",
                    "p->val > u->val && q->val > u->val": "descend right (u = u->right)",
                    "otherwise": "split point: u is LCA"
                },
                elimination_proof=(
                    "BST LCA Branch Elimination Proof:\n"
                    "1. If both p and q are strictly smaller than u->val, both reside in left subtree; u and right subtree cannot be LCA.\n"
                    "2. If both p and q are strictly larger than u->val, both reside in right subtree.\n"
                    "3. When p and q lie on opposite sides of u (or one equals u), u is the highest node separating them, hence the unique LCA."
                ),
                state_updates={
                    "u = u->left": "eliminates right branch and root u",
                    "u = u->right": "eliminates left branch and root u"
                }
            )

        if pattern == "tree_lca_binary_tree":
            return MovementDerivation(
                pattern=pattern,
                objective_function="Find LCA in general binary tree via recursive descendant discovery.",
                decision_conditions={
                    "u == nullptr || u == p || u == q": "return u",
                    "left != nullptr && right != nullptr": "u is LCA split point",
                    "left != nullptr": "return left",
                    "right != nullptr": "return right"
                },
                elimination_proof=(
                    "Binary Tree LCA Descendant Splitting Proof:\n"
                    "1. Postorder recursion bubbles up non-null pointer if p or q is contained in subtree.\n"
                    "2. When both left and right return non-null, p and q reside in disjoint subtrees of u, proving u is their LCA.\n"
                    "3. Runs in O(N) time visiting each node exactly once."
                ),
                state_updates={
                    "left = lca(u->left, p, q)": "searches left subtree",
                    "right = lca(u->right, p, q)": "searches right subtree"
                }
            )

        if pattern == "tree_lca_parent_array":
            return MovementDerivation(
                pattern=pattern,
                objective_function="Find LCA using parent pointers via depth-leveling and lockstep walk.",
                decision_conditions={
                    "depth[u] > depth[v]": "u = parent[u] (level depth)",
                    "depth[v] > depth[u]": "v = parent[v] (level depth)",
                    "depth[u] == depth[v] && u != v": "u = parent[u]; v = parent[v] (step together)",
                    "u == v": "LCA reached"
                },
                elimination_proof=(
                    "Parent Array LCA Leveling Proof:\n"
                    "1. LCA cannot reside at depth strictly greater than min(depth[u], depth[v]).\n"
                    "2. Lifting deeper node levels depth without bypassing LCA.\n"
                    "3. Once leveled, simultaneous single steps encounter the first common ancestor."
                ),
                state_updates={
                    "u = parent[u]": "walks toward root along unique ancestor path"
                }
            )

        if pattern == "tree_diameter":
            return MovementDerivation(
                pattern=pattern,
                objective_function="Compute tree diameter by tracking top two branch depths at each node.",
                decision_conditions={
                    "u == nullptr": "return 0",
                    "u != nullptr": "max_path_through_u = d1 + d2; update global_diameter = max(global_diameter, max_path_through_u)"
                },
                elimination_proof=(
                    "Tree Diameter Two-Branch Merge Proof:\n"
                    "1. Any simple path in a tree has a unique highest node (lowest common ancestor of the path endpoints).\n"
                    "2. For a fixed highest node u, the longest path passing through u is the sum of the two longest branches extending into its children.\n"
                    "3. Maximizing over all nodes u in postorder yields the exact diameter in O(N) time."
                ),
                state_updates={
                    "global_diameter = max(global_diameter, d1 + d2)": "tracks optimal diameter",
                    "return 1 + max(d1, d2)": "returns depth to parent"
                }
            )

        if pattern == "tree_dp_independent_set":
            return MovementDerivation(
                pattern=pattern,
                objective_function="Compute Maximum Weight Independent Set on tree via two-state DP.",
                decision_conditions={
                    "include u (dp1)": "dp1 = val[u] + sum_v dp0[v] (all children must be excluded)",
                    "exclude u (dp0)": "dp0 = sum_v max(dp0[v], dp1[v]) (each child can be independently included or excluded)"
                },
                elimination_proof=(
                    "Tree Independent Set Optimal Substructure Proof:\n"
                    "1. Since a tree has no cycles, subtrees of children v1, v2, ... are mutually independent.\n"
                    "2. If u is excluded, the choice to include or exclude child v1 has zero constraint on child v2.\n"
                    "3. Postorder evaluation computes optimal subproblem solutions without backtracking in O(N) time."
                ),
                state_updates={
                    "dp1[u] = val[u] + sum dp0[v]": "enforces independence constraint",
                    "dp0[u] = sum max(dp0[v], dp1[v])": "maximizes disjoint child choices"
                }
            )

        if pattern in ("tree_dfs_preorder", "tree_dfs_inorder", "tree_dfs_postorder", "tree_bfs_level_order",
                       "tree_depth_height", "tree_subtree_size", "tree_leaf_count", "tree_subtree_aggregation",
                       "tree_path_sum", "tree_dp_subtree_weight", "tree_dp_two_state"):
            return MovementDerivation(
                pattern=pattern,
                objective_function="Traverse or aggregate tree structure along hierarchical parent-child edges.",
                decision_conditions={
                    "u != nullptr": "process node and recurse/queue children",
                    "u == nullptr": "base case neutral value"
                },
                elimination_proof=(
                    "Tree Hierarchy Traversal & Parent Tracking Proof:\n"
                    "1. Undirected tree DFS with `if (v != p)` traverses all children without visited array overhead.\n"
                    "2. Acyclic property guarantees each undirected edge is crossed exactly once in each direction in O(N) time.\n"
                    "3. Subtree independence ensures bottom-up aggregations are exact and complete."
                ),
                state_updates={
                    "state(u) = combine(val[u], children_states)": "aggregates subtree value"
                }
            )

        # ── Phase 3F: Graph Pattern Movement Derivations ──

        if pattern == "graph_bfs_shortest_path":
            return MovementDerivation(
                pattern=pattern,
                objective_function="find minimum hop distance from source to all reachable vertices",
                decision_conditions={
                    "vertex v newly discovered": "set dist[v] = dist[u] + 1, enqueue v",
                    "vertex v already visited": "skip (dist[v] already finalized at earlier layer)"
                },
                elimination_proof=(
                    "BFS expands vertices in non-decreasing order of hop distance. "
                    "Once v is enqueued at distance d, any other path to v at distance d' >= d cannot improve it. "
                    "Proof: every path with k hops is explored before any path with k+1 hops."
                ),
                state_updates={
                    "dist[v] = dist[u] + 1": "records shortest hop distance",
                    "enqueue v": "schedules v for neighbor exploration at next layer"
                }
            )

        if pattern == "graph_dfs_traversal":
            return MovementDerivation(
                pattern=pattern,
                objective_function="visit all vertices reachable from source",
                decision_conditions={
                    "neighbor v is unvisited": "recurse into v (or push to stack)",
                    "neighbor v is visited": "skip (already fully explored)"
                },
                elimination_proof=(
                    "Each vertex is visited exactly once. visited[u] = True permanently eliminates u from future processing. "
                    "DFS explores each edge (u, v) at most twice (once forward in directed graph, twice in undirected). "
                    "Total: O(V + E)."
                ),
                state_updates={
                    "visited[u] = True": "marks u as permanently explored",
                    "recursion depth": "tracks DFS call stack depth"
                }
            )

        if pattern == "graph_dijkstra":
            return MovementDerivation(
                pattern=pattern,
                objective_function="minimize dist[v] = shortest path from source to v for all v",
                decision_conditions={
                    "dist[u] + w(u,v) < dist[v]": "relax: update dist[v] and push (dist[v], v) to priority queue",
                    "dist[u] + w(u,v) >= dist[v]": "no improvement, skip",
                    "u already settled": "skip stale PQ entry"
                },
                elimination_proof=(
                    "Greedy correctness: when u is extracted from PQ with distance d, dist[u] = d is final. "
                    "Proof by contradiction: if a shorter path to u existed, it would route through some unsettled vertex v' "
                    "with dist[v'] <= d. But v' was not yet extracted, so d is the minimum — contradiction. "
                    "Requires all edge weights w >= 0."
                ),
                state_updates={
                    "dist[v] = dist[u] + w": "relaxation step",
                    "settled.add(u)": "finalizes u's distance",
                    "PQ.push((dist[v], v))": "schedules v for future extraction"
                }
            )

        if pattern == "graph_bellman_ford":
            return MovementDerivation(
                pattern=pattern,
                objective_function="minimize dist[v] = shortest path from source to v (allows negative weights)",
                decision_conditions={
                    "dist[u] + w < dist[v]": "relax: dist[v] = dist[u] + w",
                    "V-th round relaxation succeeds": "negative cycle detected on reachable path"
                },
                elimination_proof=(
                    "After k rounds of edge relaxation, dist[v] <= length of shortest path from source to v using at most k edges. "
                    "A shortest path (in absence of negative cycles) uses at most V-1 edges. "
                    "After V-1 rounds, dist[v] is optimal. "
                    "If round V still relaxes, some cycle has negative total weight."
                ),
                state_updates={
                    "dist[v] = dist[u] + w": "edge relaxation",
                    "round counter": "increments from 1 to V-1 (and optionally V for cycle detection)"
                }
            )

        if pattern == "graph_floyd_warshall":
            return MovementDerivation(
                pattern=pattern,
                objective_function="minimize dist[i][j] = shortest path from i to j for all pairs",
                decision_conditions={
                    "dist[i][k] + dist[k][j] < dist[i][j]": "update dist[i][j] = dist[i][k] + dist[k][j]",
                    "no improvement via k": "skip"
                },
                elimination_proof=(
                    "Optimal substructure: shortest path from i to j using intermediate set {0..k} either "
                    "(1) does not use vertex k: dist[i][j] unchanged, or "
                    "(2) uses vertex k: dist[i][k] + dist[k][j]. "
                    "Taking the minimum yields the correct shortest path for the expanded intermediate set. "
                    "After k = V-1, all vertices have been considered as intermediates."
                ),
                state_updates={
                    "dist[i][j] = dist[i][k] + dist[k][j]": "via-k relaxation",
                    "k outer loop": "expands considered intermediate vertex set by one"
                }
            )

        if pattern == "graph_topological_sort":
            return MovementDerivation(
                pattern=pattern,
                objective_function="produce linear ordering of DAG vertices where each u precedes all its out-neighbors",
                decision_conditions={
                    "in_degree[v] == 0": "safe to output v (all predecessors already placed)",
                    "in_degree[v] > 0": "v has unresolved predecessors; skip until in_degree reduces to 0"
                },
                elimination_proof=(
                    "A vertex u is eliminated from waiting once all predecessors output. "
                    "When u is dequeued, its in_degree == 0, so it has no dependency ordering constraints remaining. "
                    "Removing u and decrementing neighbors' in-degrees may enqueue them. "
                    "A DAG always has at least one source (in_degree 0) at each step."
                ),
                state_updates={
                    "dequeue u": "places u in topological order",
                    "in_degree[v]--": "resolves one dependency for v",
                    "enqueue v if in_degree[v] == 0": "v is now a source vertex"
                }
            )

        if pattern == "graph_dag_dp":
            return MovementDerivation(
                pattern=pattern,
                objective_function="compute dp[v] = optimal path property from source to v in topological order",
                decision_conditions={
                    "dp[u] + w < dp[v] (or satisfies objective)": "update dp[v] via u",
                    "dp[u] not yet computed": "must process u before v (topological order ensures this)"
                },
                elimination_proof=(
                    "Processing vertices in topological order guarantees that when v is processed, "
                    "all predecessors of v have been finalized. "
                    "dp[v] = optimal combination over all predecessors u: f(dp[u], w(u,v)). "
                    "No future predecessor can update dp[v] since predecessors appear before v in topological order."
                ),
                state_updates={
                    "dp[v] = optimize(dp[v], dp[u] + w)": "relaxation/DP transition",
                    "topological processing order": "ensures predecessor finality"
                }
            )

        if pattern == "graph_connected_components":
            return MovementDerivation(
                pattern=pattern,
                objective_function="label each vertex with its connected component ID",
                decision_conditions={
                    "vertex v is unvisited": "start new BFS/DFS component from v; assign component_id",
                    "vertex v is visited": "already labeled; skip"
                },
                elimination_proof=(
                    "Each unvisited vertex v starts exactly one new component traversal. "
                    "BFS/DFS from v visits all vertices reachable from v and labels them with the same component_id. "
                    "After the traversal, no other traversal will visit those vertices (visited flag set)."
                ),
                state_updates={
                    "visited[v] = True": "permanently marks v as component-labeled",
                    "num_components++": "increments for each new unvisited source vertex"
                }
            )

        if pattern == "graph_cycle_detection_undirected":
            return MovementDerivation(
                pattern=pattern,
                objective_function="determine if undirected graph contains a cycle",
                decision_conditions={
                    "neighbor v is unvisited": "recurse with parent[v] = u",
                    "neighbor v is visited and v != parent[u]": "back-edge found → cycle exists",
                    "neighbor v == parent[u]": "bidirectional tree edge; skip"
                },
                elimination_proof=(
                    "In undirected DFS, a non-tree edge (u, v) where v is visited and v != parent[u] "
                    "is a back-edge that creates a cycle. "
                    "The only visited neighbor that is NOT a cycle indicator is the DFS parent "
                    "(it is the reverse of the current tree edge)."
                ),
                state_updates={
                    "visited[u] = True": "marks u as explored",
                    "parent[v] = u": "tracks DFS tree edge direction"
                }
            )

        if pattern == "graph_cycle_detection_directed":
            return MovementDerivation(
                pattern=pattern,
                objective_function="determine if directed graph contains a cycle",
                decision_conditions={
                    "color[v] == UNVISITED(0)": "recurse into v, set color[v] = VISITING",
                    "color[v] == VISITING(1)": "back-edge to ancestor → directed cycle found",
                    "color[v] == VISITED(2)": "fully processed; cross or forward edge; no cycle via this path"
                },
                elimination_proof=(
                    "VISITING state marks nodes in the current DFS recursive call stack. "
                    "An edge to a VISITING node creates a path that loops back to an ancestor — directed cycle. "
                    "VISITED nodes are not in the stack; reaching them is a forward or cross edge (no cycle implication)."
                ),
                state_updates={
                    "color[v] = VISITING(1)": "marks entry into v",
                    "color[v] = VISITED(2)": "marks full processing of v"
                }
            )

        if pattern == "graph_bipartite_coloring":
            return MovementDerivation(
                pattern=pattern,
                objective_function="determine if graph is 2-colorable (bipartite) and assign colors",
                decision_conditions={
                    "neighbor v uncolored": "assign color[v] = 1 - color[u]; enqueue v",
                    "neighbor v colored and color[v] == color[u]": "odd cycle detected → not bipartite",
                    "neighbor v colored and color[v] != color[u]": "consistent; no action needed"
                },
                elimination_proof=(
                    "2-coloring invariant: for each edge (u, v), color[u] != color[v]. "
                    "If this is violated (both endpoints same color), an odd cycle exists. "
                    "A graph is bipartite if and only if it contains no odd cycle (is 2-colorable)."
                ),
                state_updates={
                    "color[v] = 1 - color[u]": "assigns opposite color to neighbor",
                    "is_bipartite = False": "set on color conflict"
                }
            )

        if pattern == "graph_dsu":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain dynamic connectivity; answer union and find queries",
                decision_conditions={
                    "find(x) != find(y) in union(x,y)": "merge components: attach smaller-rank root under larger-rank root",
                    "find(x) == find(y) in union(x,y)": "x and y already in same component; no merge needed"
                },
                elimination_proof=(
                    "Path compression in find(): flattens the tree so future finds are near-O(1). "
                    "Union by rank: always attach shorter tree under taller tree, keeping height O(log V). "
                    "Together: amortized O(alpha(V)) per operation."
                ),
                state_updates={
                    "parent[root_x] = root_y": "merges two components",
                    "parent[x] = find(parent[x])": "path compression during find"
                }
            )

        if pattern == "graph_mst_kruskal":
            return MovementDerivation(
                pattern=pattern,
                objective_function="select minimum-weight edges forming a spanning tree",
                decision_conditions={
                    "find(u) != find(v) for edge (u,v,w)": "safe edge: add to MST; union(u, v)",
                    "find(u) == find(v) for edge (u,v,w)": "cycle would form; skip edge"
                },
                elimination_proof=(
                    "Cut Property: at the time edge (u, v, w) is considered, "
                    "it is the minimum-weight edge crossing the cut (component_of_u, rest). "
                    "Cycle Property: skipped edges would form cycles, violating spanning tree acyclicity. "
                    "Together: greedy edge selection produces the globally optimal MST."
                ),
                state_updates={
                    "MST.add(u, v, w)": "includes edge in spanning tree",
                    "union(u, v)": "merges u and v's components"
                }
            )

        if pattern == "graph_mst_prim":
            return MovementDerivation(
                pattern=pattern,
                objective_function="grow MST from a source by always adding the minimum crossing edge",
                decision_conditions={
                    "edge (u,v) has w < key[v] and v not in MST": "update key[v], parent[v] = u; push to PQ",
                    "v already in MST": "skip (already optimally connected)",
                    "stale PQ entry": "skip if key[v] was already improved by a lighter edge"
                },
                elimination_proof=(
                    "Cut Property: key[v] = minimum edge weight connecting v to the current MST component S. "
                    "Extracting min-key vertex adds the minimum crossing edge for cut (S, V\\S). "
                    "By Cut Property, this edge is in some MST. Inductively, the final set of V-1 added edges forms the MST."
                ),
                state_updates={
                    "key[v] = w": "records best known connection weight to MST",
                    "parent[v] = u": "records MST edge predecessor",
                    "inMST[u] = True": "finalizes u's MST membership"
                }
            )

        if pattern == "graph_scc_tarjan":
            return MovementDerivation(
                pattern=pattern,
                objective_function="partition directed graph vertices into maximal SCCs",
                decision_conditions={
                    "unvisited neighbor v": "recurse; after return, low[u] = min(low[u], low[v])",
                    "visited neighbor v on stack": "back-edge; low[u] = min(low[u], tin[v])",
                    "visited neighbor v not on stack": "cross/forward edge; ignore for low-link",
                    "low[u] == tin[u] after DFS": "u is SCC root; pop stack until u"
                },
                elimination_proof=(
                    "low[u] = minimum discovery time reachable from u's subtree via back-edges. "
                    "When low[u] == tin[u], no vertex in u's DFS subtree can reach an ancestor of u via back-edges. "
                    "Therefore u's stack segment forms a maximal SCC with mutual reachability."
                ),
                state_updates={
                    "tin[u] = low[u] = timer++": "records discovery time",
                    "stack.push(u)": "tracks active SCC candidates",
                    "low[u] = min(low[u], ...)": "propagates back-edge reachability"
                }
            )

        if pattern == "graph_bridges_articulation":
            return MovementDerivation(
                pattern=pattern,
                objective_function="find all bridges and articulation points using DFS low-link values",
                decision_conditions={
                    "low[v] > tin[u] after recursion into v": "edge (u,v) is a bridge",
                    "low[v] >= tin[u] and u is not root": "u is an articulation point",
                    "u is root with >= 2 DFS children": "u is an articulation point",
                    "back-edge to visited v != parent": "low[u] = min(low[u], tin[v])"
                },
                elimination_proof=(
                    "Bridge condition low[v] > tin[u]: v's subtree has no back-edge to u or its ancestors. "
                    "Removing edge (u,v) disconnects the graph. "
                    "AP condition low[v] >= tin[u] (non-root): v's subtree cannot bypass u to reach u's ancestors. "
                    "Removing u disconnects v's subtree from the rest."
                ),
                state_updates={
                    "low[u] = min(low[u], low[v])": "propagates subtree reachability",
                    "low[u] = min(low[u], tin[v])": "back-edge to ancestor v",
                    "tin[u] = timer++": "assigns discovery order"
                }
            )

        # ── Heap / Priority Queue Patterns (Phase 3G) ──

        if pattern == "heap_min_priority_queue":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain dynamic set with O(1) minimum access and O(log N) updates",
                decision_conditions={
                    "push(x)": "append at leaf index N; sift-up while A[i] < A[parent(i)]",
                    "pop()": "replace root with last leaf; pop back; sift-down with min(child_L, child_R)",
                    "peek()": "return root A[0] in O(1)"
                },
                elimination_proof=(
                    "Sift-up and sift-down maintain the partial ordering invariant A[parent(i)] <= A[i]. "
                    "Root is guaranteed to be the minimum. Non-minimal candidates are retained without total ordering overhead."
                ),
                state_updates={
                    "sift-up": "swaps element with parent until min-heap property holds in O(log N)",
                    "sift-down": "swaps element with smaller child until min-heap property holds in O(log N)"
                }
            )

        if pattern == "heap_max_priority_queue":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain dynamic set with O(1) maximum access and O(log N) updates",
                decision_conditions={
                    "push(x)": "append at leaf index N; sift-up while A[i] > A[parent(i)]",
                    "pop()": "replace root with last leaf; pop back; sift-down with max(child_L, child_R)",
                    "peek()": "return root A[0] in O(1)"
                },
                elimination_proof=(
                    "Sift-up and sift-down maintain max-heap invariant A[parent(i)] >= A[i]. "
                    "Root is guaranteed to be the maximum without inspecting children."
                ),
                state_updates={
                    "sift-up": "promotes larger elements toward root in O(log N)",
                    "sift-down": "demotes smaller elements toward leaves in O(log N)"
                }
            )

        if pattern == "heap_build":
            return MovementDerivation(
                pattern=pattern,
                objective_function="convert unordered array A[0..N-1] into a valid heap in linear O(N) time",
                decision_conditions={
                    "i >= floor(N/2)": "leaf nodes; trivially valid heaps of height 0",
                    "i < floor(N/2)": "apply sift-down(i) to merge valid subtrees left(i) and right(i)"
                },
                elimination_proof=(
                    "Bottom-up construction ensures that when sift-down is called on node i, both of its "
                    "child subtrees already satisfy the heap property. Sum of heights across all nodes is O(N)."
                ),
                state_updates={
                    "sift-down(i)": "restores heap property for subtree rooted at i in O(h_i) time"
                }
            )

        if pattern == "heap_top_k":
            return MovementDerivation(
                pattern=pattern,
                objective_function="select top-K extremal elements using bounded O(K) memory",
                decision_conditions={
                    "heap.size() < K": "push candidate unconditionally; size grows toward K",
                    "x > min_heap.top() (for K largest)": "pop weakest candidate min_heap.top(); push x in O(log K)",
                    "x <= min_heap.top() (for K largest)": "x cannot belong to top-K; eliminate x immediately in O(1)"
                },
                elimination_proof=(
                    "Retention Invariant: To keep K largest elements, the candidate set must evict the weakest "
                    "element in O(1). The weakest of the K largest is the minimum, so a MIN-HEAP of size K is used. "
                    "Any incoming element <= min_heap.top() is proven non-viable and safely eliminated."
                ),
                state_updates={
                    "pop_push(x)": "evicts weakest candidate, maintains size K invariant in O(log K)"
                }
            )

        if pattern == "heap_kth_element":
            return MovementDerivation(
                pattern=pattern,
                objective_function="identify the K-th extremal element in a stream or collection",
                decision_conditions={
                    "incoming candidate better than heap.top()": "pop root and push candidate in O(log K)",
                    "incoming candidate worse than or equal to heap.top()": "discard candidate immediately"
                },
                elimination_proof=(
                    "Bounded heap of size K stores the top-K elements. In a min-heap of the K largest elements, "
                    "the root is the minimum among the K largest, which is the exact K-th largest overall."
                ),
                state_updates={
                    "sift-down": "adjusts root position after displacement in O(log K)"
                }
            )

        if pattern == "heap_k_way_merge":
            return MovementDerivation(
                pattern=pattern,
                objective_function="merge K sorted streams into a single sorted stream in O(N log K) time",
                decision_conditions={
                    "heap has elements": "pop root (global min among stream frontiers), advance that stream",
                    "stream has more elements": "push next element (val, stream_id, idx+1) into min-heap in O(log K)",
                    "stream exhausted": "do not push; heap size decreases"
                },
                elimination_proof=(
                    "Since each input stream is pre-sorted, the global minimum of all remaining elements must be "
                    "among the current heads of the K streams. The min-heap dynamically maintains this K-candidate frontier."
                ),
                state_updates={
                    "heap.pop()": "emits globally minimum element",
                    "heap.push(next)": "maintains K-way priority frontier"
                }
            )

        if pattern == "heap_two_heaps":
            return MovementDerivation(
                pattern=pattern,
                objective_function="partition dynamic stream into balanced lower and upper halves",
                decision_conditions={
                    "x <= low.top()": "push x to max-heap low",
                    "x > low.top()": "push x to min-heap high",
                    "|low| > |high| + 1": "move low.top() to high (rebalance)",
                    "|high| > |low|": "move high.top() to low (rebalance)"
                },
                elimination_proof=(
                    "Two-heap invariant: all elements in low are <= all elements in high. "
                    "Size balance ensures low and high partition the stream into equal halves."
                ),
                state_updates={
                    "rebalance": "moves extremum across partition boundary to restore size balance"
                }
            )

        if pattern == "heap_dynamic_median":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain running median in O(1) query time and O(log N) insertion time",
                decision_conditions={
                    "N is odd": "median is low.top() in O(1)",
                    "N is even": "median is (low.top() + high.top()) / 2.0 in O(1)"
                },
                elimination_proof=(
                    "Partition invariant ensures low.top() is the maximum of the lower half and high.top() is "
                    "the minimum of the upper half. Thus the true median is directly observable from the two roots."
                ),
                state_updates={
                    "query": "O(1) root inspection",
                    "insert": "O(log N) push and potential rebalance"
                }
            )

        if pattern == "heap_scheduling":
            return MovementDerivation(
                pattern=pattern,
                objective_function="schedule overlapping intervals onto minimum number of resources",
                decision_conditions={
                    "start_time >= min_heap.top()": "earliest active resource has finished; pop and reuse resource",
                    "start_time < min_heap.top()": "all active resources occupied; allocate new resource",
                    "always": "push end_time into min-heap"
                },
                elimination_proof=(
                    "Greedy choice: by sorting intervals by start time and releasing the earliest-ending resource first, "
                    "we maximize resource reuse without backtracking."
                ),
                state_updates={
                    "heap.pop()": "frees reusable resource",
                    "heap.push(end_time)": "records new resource busy duration"
                }
            )

        if pattern == "heap_greedy_selection":
            return MovementDerivation(
                pattern=pattern,
                objective_function="repeatedly combine two smallest elements to minimize cumulative merge cost",
                decision_conditions={
                    "heap.size() >= 2": "extract two smallest a and b; cost += (a + b); push (a + b)",
                    "heap.size() == 1": "termination reached; return accumulated cost"
                },
                elimination_proof=(
                    "Huffman Greedy Choice Property: elements combined earlier appear at deeper tree levels and "
                    "are multiplied more times in the total cost sum. Pairing the two globally smallest elements minimizes the sum."
                ),
                state_updates={
                    "extract two & push sum": "reduces candidate count by 1 and updates cost in O(log N)"
                }
            )

        if pattern == "heap_lazy_deletion":
            return MovementDerivation(
                pattern=pattern,
                objective_function="support dynamic updates and deletions without O(N) heap search",
                decision_conditions={
                    "stale(heap.top())": "lazily pop and discard root until top is valid",
                    "valid(heap.top())": "access or pop active extremal element",
                    "update(x) / remove(x)": "record tombstone or decrement valid frequency in hash map"
                },
                elimination_proof=(
                    "By delaying removal of non-root elements until they float to the root, we avoid O(N) array search. "
                    "Amortized cost per operation remains O(log N)."
                ),
                state_updates={
                    "tracker[x]--": "marks element stale in O(1)",
                    "lazy pop": "cleans up invalid roots in O(log N)"
                }
            )

        # ── Disjoint Set Union (DSU) Movement Derivations (Phase 3H) ──

        if pattern == "dsu_basic":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain dynamic equivalence classes under union and find operations in nearly linear O(alpha(N)) amortized time",
                decision_conditions={
                    "find(x) != find(y)": "elements in different components; union merges them",
                    "find(x) == find(y)": "elements already in same component; union is redundant"
                },
                elimination_proof=(
                    "Two-pass path compression updates parent[curr] = root for all nodes along find path. "
                    "Union-by-size attaches smaller root under larger root. "
                    "Tarjan's theorem proves any sequence of M operations on N elements takes O(M * alpha(N)) time."
                ),
                state_updates={
                    "find(x)": "compresses traversed nodes directly to root",
                    "union(x, y)": "sets parent[smaller_root] = larger_root, adds size, decrements component count"
                }
            )

        if pattern == "dsu_component_metadata":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain aggregate metadata (sum, min, max, size) across dynamic components in O(alpha(N))",
                decision_conditions={
                    "rx != ry": "merge components and combine metadata: metadata[ry] = combine(metadata[ry], metadata[rx])",
                    "rx == ry": "redundant merge; metadata unchanged"
                },
                elimination_proof=(
                    "Because the metadata operation (sum, min, max) is associative, combining the roots' metadata "
                    "preserves the exact component aggregate without traversing constituent nodes."
                ),
                state_updates={
                    "combine(meta_y, meta_x)": "updates root aggregate in O(1)"
                }
            )

        if pattern == "dsu_dynamic_connectivity":
            return MovementDerivation(
                pattern=pattern,
                objective_function="process online edge additions and answer reachability queries in O(alpha(N))",
                decision_conditions={
                    "query(u, v)": "return find(u) == find(v)",
                    "add_edge(u, v)": "union(u, v)"
                },
                elimination_proof=(
                    "Equivalence relation is reflexive, symmetric, and transitive. "
                    "Transitive closure is maintained incrementally by tree mergers."
                ),
                state_updates={
                    "union": "merges components",
                    "find": "resolves canonical representative"
                }
            )

        if pattern == "dsu_weighted":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain relative potentials value[x] - value[y] = w in O(alpha(N))",
                decision_conditions={
                    "rx != ry": "attach rx to ry with pot[rx] = w - pot[x] + pot[y]",
                    "rx == ry && pot[x] - pot[y] == w": "consistent redundant constraint",
                    "rx == ry && pot[x] - pot[y] != w": "contradiction detected"
                },
                elimination_proof=(
                    "Let pot[u] = value[u] - value[parent[u]]. Path compression sums potentials along tree paths. "
                    "Attaching root rx under ry with pot[rx] = w - pot[x] + pot[y] satisfies (pot[x] + pot[rx]) - pot[y] = w."
                ),
                state_updates={
                    "find": "compresses path and accumulates potentials: pot[curr] += pot[prev_parent]",
                    "union": "sets pot[root_x] = w - pot[x] + pot[y]"
                }
            )

        if pattern == "dsu_potential_difference":
            return MovementDerivation(
                pattern=pattern,
                objective_function="query exact potential difference value[x] - value[y] if connected",
                decision_conditions={
                    "find(x) == find(y)": "return pot[x] - pot[y] in O(alpha(N))",
                    "find(x) != find(y)": "return indeterminate (disconnected components)"
                },
                elimination_proof=(
                    "When x and y share root r, pot[x] = value[x] - value[r] and pot[y] = value[y] - value[r]. "
                    "Subtracting yields value[x] - value[y] = pot[x] - pot[y]."
                ),
                state_updates={
                    "query": "returns pot[x] - pot[y]"
                }
            )

        if pattern == "dsu_parity":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain 2-coloring / bipartite relations (color[x] ^ color[y] = p) online in O(alpha(N))",
                decision_conditions={
                    "rx != ry": "attach rx to ry with parity[rx] = p ^ parity[x] ^ parity[y]",
                    "rx == ry && (parity[x] ^ parity[y]) == p": "consistent parity relation",
                    "rx == ry && (parity[x] ^ parity[y]) != p": "odd-cycle contradiction detected"
                },
                elimination_proof=(
                    "Parity is an element of GF(2). XOR addition is associative and self-inverse. "
                    "Attaching root rx to ry with parity[rx] = p ^ parity[x] ^ parity[y] ensures parity[x] ^ parity[y] = p relative to new common root."
                ),
                state_updates={
                    "find": "compresses path and XORs parity: parity[curr] ^= parity[prev_parent]",
                    "union": "sets parity[rx] = p ^ parity[x] ^ parity[y]"
                }
            )

        if pattern == "dsu_rollback":
            return MovementDerivation(
                pattern=pattern,
                objective_function="support union and exact snapshot rollback in O(log N) union and O(1) undo",
                decision_conditions={
                    "union(u, v)": "find roots without path compression; record previous state in history stack; attach smaller to larger",
                    "rollback()": "pop history stack; restore parent, size, component count, and metadata"
                },
                elimination_proof=(
                    "Without path compression, tree depth is strictly bounded by floor(log2(N)) by union-by-size/rank. "
                    "Each union mutates at most one parent pointer and one size field. "
                    "Recording these mutations in a LIFO stack allows exact restoration in O(1) per undo."
                ),
                state_updates={
                    "stack.push": "saves mutation snapshot",
                    "stack.pop": "reverts mutation in O(1)"
                }
            )

        if pattern == "dsu_offline_dynamic_connectivity":
            return MovementDerivation(
                pattern=pattern,
                objective_function="answer connectivity queries with arbitrary edge insertions and deletions offline in O(M log Q log N + Q log N)",
                decision_conditions={
                    "edge lifetime [t_start, t_end)": "insert edge into O(log Q) segment tree nodes covering interval",
                    "segment tree DFS visit node": "apply unions of all edges in node via Rollback DSU",
                    "segment tree leaf t": "answer query at time t",
                    "segment tree DFS exit node": "rollback all unions applied for this node"
                },
                elimination_proof=(
                    "Segment tree divides time into Q leaves of depth log Q. Each edge lifetime is decomposed into at most 2 log Q canonical intervals. "
                    "DFS visits tree in Euler tour order, matching the LIFO property of Rollback DSU."
                ),
                state_updates={
                    "enter_node": "applies batch of unions to rollback DSU",
                    "exit_node": "rolls back exact batch of unions in LIFO order"
                }
            )

        if pattern == "dsu_kruskal_support":
            return MovementDerivation(
                pattern=pattern,
                objective_function="identify minimum spanning tree edges in non-decreasing weight order avoiding cycles",
                decision_conditions={
                    "find(u) != find(v)": "edge crosses cut between disjoint components; include in MST and union(u, v)",
                    "find(u) == find(v)": "edge connects vertices in same component; forms a cycle; discard edge"
                },
                elimination_proof=(
                    "Cut Property: the lightest edge crossing any cut of a graph is guaranteed to belong to some MST. "
                    "DSU efficiently checks if an edge crosses a cut between existing connected components."
                ),
                state_updates={
                    "union(u, v)": "merges components",
                    "add_mst_edge": "records edge in MST result"
                }
            )

        if pattern == "dsu_constraint_consistency":
            return MovementDerivation(
                pattern=pattern,
                objective_function="verify whether incoming potential/parity constraints are satisfiable without contradiction",
                decision_conditions={
                    "find(x) != find(y)": "independent constraint; merge components and record relation",
                    "find(x) == find(y) && consistent": "redundant constraint; accept without change",
                    "find(x) == find(y) && inconsistent": "contradiction detected; return UNSATISFIABLE / false"
                },
                elimination_proof=(
                    "Equivalence paths inside the same tree uniquely fix the potential or parity between any two elements. "
                    "An incoming constraint between two already connected elements must match the existing derived relation; any discrepancy is a mathematical contradiction."
                ),
                state_updates={
                    "record_consistency": "verifies or flags contradiction in O(alpha(N))"
                }
            )

        # ── Phase 3I: Fenwick Tree Movement Derivations ──
        if pattern == "fenwick_point_update_prefix_query":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain dynamic prefix sums under point updates in O(log N) time",
                decision_conditions={
                    "point_update(i, delta)": "traverse tree[i] upward via i += lowbit(i)",
                    "prefix_query(x)": "accumulate tree[x] downward via x -= lowbit(x)",
                    "range_query(l, r)": "evaluate prefix_query(r) - prefix_query(l-1)"
                },
                elimination_proof=(
                    "Binary index decomposition divides [1, x] into at most floor(log2(x)) + 1 disjoint intervals whose right endpoints are indices visited by stripping lowbit. "
                    "Point update visits only indices whose intervals contain i."
                ),
                state_updates={
                    "i += lowbit(i)": "updates parent interval in Fenwick tree",
                    "x -= lowbit(x)": "removes lowbit interval, stepping to previous disjoint power-of-2 interval"
                }
            )

        if pattern == "fenwick_range_update_point_query":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain point values under range additions in O(log N) time",
                decision_conditions={
                    "range_update(l, r, delta)": "add(l, +delta) and add(r+1, -delta) on difference array BIT",
                    "point_query(x)": "prefix_query(x) on difference array BIT"
                },
                elimination_proof=(
                    "Difference array represents A[x] as sum_{j=1}^x D[j]. Range addition [l, r] affects only D[l] by +delta and D[r+1] by -delta, leaving all internal differences D[j] unchanged."
                ),
                state_updates={
                    "add(l, delta)": "adds delta to prefix for all x >= l",
                    "add(r+1, -delta)": "cancels delta from prefix for all x > r"
                }
            )

        if pattern == "fenwick_range_update_range_query":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain range sum queries under range additions in O(log N) time",
                decision_conditions={
                    "range_update(l, r, delta)": "update B1 at l (+delta) and r+1 (-delta); update B2 at l (+l*delta) and r+1 (-(r+1)*delta)",
                    "prefix_query(x)": "(x + 1) * query(B1, x) - query(B2, x)",
                    "range_query(l, r)": "prefix_query(r) - prefix_query(l-1)"
                },
                elimination_proof=(
                    "sum_{i=1}^x A[i] = (x + 1) * sum_{j=1}^x D[j] - sum_{j=1}^x (j * D[j]). Maintaining two Fenwick trees for D[j] and j*D[j] computes arbitrary range sum in O(log N)."
                ),
                state_updates={
                    "B1_update": "maintains coefficient of (x + 1)",
                    "B2_update": "maintains offset subtraction term"
                }
            )

        if pattern == "fenwick_frequency":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain dynamic element frequencies and cumulative frequency counts in O(log M)",
                decision_conditions={
                    "insert(val)": "add(val, +1)",
                    "remove(val)": "add(val, -1)",
                    "count_leq(val)": "prefix_query(val)"
                },
                elimination_proof=(
                    "Treats value universe as indexed array where each position tracks frequency. Lowbit traversal sums frequencies in canonical sub-ranges."
                ),
                state_updates={
                    "add(val, count)": "adjusts frequency of val and updates covering Fenwick intervals"
                }
            )

        if pattern == "fenwick_prefix_extremum":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain dynamic prefix minimum or maximum under monotonic updates in O(log N)",
                decision_conditions={
                    "update_min(i, val)": "val <= current_val required; tree[i] = min(tree[i], val); i += lowbit(i)",
                    "update_max(i, val)": "val >= current_val required; tree[i] = max(tree[i], val); i += lowbit(i)",
                    "prefix_extremum(x)": "accumulate downward via x -= lowbit(x)"
                },
                elimination_proof=(
                    "Under non-increasing (for min) or non-decreasing (for max) updates, sub-tree extrema can only be tightened and never retracted, preserving correctness of ancestor updates without full tree rebuild."
                ),
                state_updates={
                    "tighten_extremum": "replaces stored extremum with better value"
                }
            )

        if pattern == "fenwick_2d_point_update_range_query":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain 2D sub-rectangle sums under point updates in O(log N * log M) time",
                decision_conditions={
                    "update(r, c, delta)": "nested loops: r += lowbit(r) and c += lowbit(c)",
                    "prefix_query(r, c)": "accumulate tree[i][j] via i -= lowbit(i) and j -= lowbit(j)",
                    "subgrid_query(r1, c1, r2, c2)": "query(r2,c2) - query(r1-1,c2) - query(r2,c1-1) + query(r1-1,c1-1)"
                },
                elimination_proof=(
                    "2D lowbit decomposition partitions the rectangle [1, r] x [1, c] into products of canonical 1D intervals, covering the area without overlap."
                ),
                state_updates={
                    "2D_add": "updates 2D cells covering (r, c)"
                }
            )

        if pattern == "fenwick_kth_element":
            return MovementDerivation(
                pattern=pattern,
                objective_function="find smallest index x with prefix frequency >= k in O(log M) using binary lifting",
                decision_conditions={
                    "current_sum + tree[idx + step] < k": "idx += step; current_sum += tree[idx]",
                    "current_sum + tree[idx + step] >= k": "do not take step; step >>= 1"
                },
                elimination_proof=(
                    "When idx is a multiple of step, tree[idx + step] contains exactly the frequency sum in (idx, idx + step]. Comparing k with current_sum + tree[idx + step] decides whether the k-th element lies strictly to the right in O(1)."
                ),
                state_updates={
                    "idx += step": "advances base index by power-of-2 step",
                    "step >>= 1": "halves step size for binary refinement"
                }
            )

        if pattern == "fenwick_inversion_counting":
            return MovementDerivation(
                pattern=pattern,
                objective_function="count pairs (i, j) with i < j and A[i] > A[j] in O(N log M) time",
                decision_conditions={
                    "process(A[i]) right-to-left": "inversions += query(A[i] - 1); add(A[i], 1)",
                    "process(A[i]) left-to-right": "inversions += (i - query(A[i])); add(A[i], 1)"
                },
                elimination_proof=(
                    "Fenwick tree maintains the frequency of elements already visited. Querying strictly smaller elements in suffix yields exact number of inversions contributed by A[i]."
                ),
                state_updates={
                    "add_inversion": "accumulates inversion count",
                    "insert_element": "registers element in Fenwick frequency table"
                }
            )

        if pattern == "fenwick_multiset":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain ordered multiset operations (insert, erase, rank, select) in O(log M) time",
                decision_conditions={
                    "insert(x)": "add(x, +1)",
                    "erase(x)": "add(x, -1)",
                    "rank(x)": "query(x - 1) + 1",
                    "kth(k)": "binary lifting search"
                },
                elimination_proof=(
                    "Ordered statistics over discrete values are maintained by frequency Fenwick tree. Binary lifting provides O(log M) quantile search matching balanced BST performance with much smaller constants."
                ),
                state_updates={
                    "modify_frequency": "increments or decrements count of element x"
                }
            )

        if pattern == "fenwick_coordinate_compression":
            return MovementDerivation(
                pattern=pattern,
                objective_function="map sparse coordinates to compact range [1..M] preserving relative order in O(K log K)",
                decision_conditions={
                    "sort_and_unique": "sorted_unique = unique(sort(coords))",
                    "map_to_rank(x)": "lower_bound(sorted_unique.begin(), sorted_unique.end(), x) - sorted_unique.begin() + 1"
                },
                elimination_proof=(
                    "Strict monotonicity of sorting ensures x < y <=> rank(x) < rank(y). Binary search provides exact rank in O(log M)."
                ),
                state_updates={
                    "compress": "builds dense 1-based coordinate array of size M"
                }
            )

        # ── Segment Tree Patterns (Phase 3J) ──
        if pattern == "segment_tree_point_update_range_query":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain associative interval aggregates under dynamic point updates in O(log N)",
                decision_conditions={
                    "no_overlap (r < ql or l > qr)": "return identity element e",
                    "full_cover (ql <= l and r <= qr)": "return tree[u]",
                    "partial_overlap": "m = (l+r)//2; return merge(query(2u, l, m, ql, qr), query(2u+1, m+1, r, ql, qr))",
                    "leaf_update (l == r)": "tree[u] = val",
                    "internal_update": "update child containing idx, then tree[u] = merge(tree[2u], tree[2u+1])"
                },
                elimination_proof=(
                    "Interval tree decomposition guarantees at most 2 nodes visited per tree level, "
                    "bounding query and update traversals to O(log N) disjoint canonical intervals."
                ),
                state_updates={
                    "tree[u] = merge(tree[2u], tree[2u+1])": "pulls updated child aggregates into parent"
                }
            )

        if pattern == "segment_tree_range_add_range_query":
            return MovementDerivation(
                pattern=pattern,
                objective_function="apply range addition updates and answer range queries in O(log N) via lazy propagation",
                decision_conditions={
                    "full_cover (ql <= l and r <= qr)": "apply tag: tree[u] += delta * len, lazy[u] += delta; return",
                    "partial_overlap": "push(u): propagate lazy tag to children 2u and 2u+1; recurse left and right; pull(u)"
                },
                elimination_proof=(
                    "Lazy invariant ensures tree[u] always holds true aggregate for [l, r]; pushing before descending "
                    "guarantees children receive correct state before being accessed or queried."
                ),
                state_updates={
                    "lazy_push": "passes pending delta to 2u and 2u+1, resets lazy[u] = 0",
                    "pull": "tree[u] = tree[2u] + tree[2u+1]"
                }
            )

        if pattern == "segment_tree_range_assign_range_query":
            return MovementDerivation(
                pattern=pattern,
                objective_function="apply range assignment overwrites and answer range queries in O(log N)",
                decision_conditions={
                    "full_cover": "tree[u] = val * len; has_assign[u] = true, assign_val[u] = val; return",
                    "partial_overlap": "push(u): overwrite children's assign tags; recurse; pull(u)"
                },
                elimination_proof=(
                    "Range assignment replaces all previous additions and assignments on the covered interval; "
                    "lazy tag push ensures descendants inherit the most recent assignment."
                ),
                state_updates={
                    "lazy_push": "transfers assignment to children, resets has_assign[u] = false",
                    "pull": "tree[u] = tree[2u] + tree[2u+1]"
                }
            )

        if pattern == "segment_tree_combined_lazy_range_query":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain combined range assignments and additions with correct composition algebra in O(log N)",
                decision_conditions={
                    "new_assign": "overrides both assign_val and add_val: has_assign = true, assign_val = val, add_val = 0",
                    "new_add": "if has_assign: assign_val += delta; else: add_val += delta",
                    "partial_overlap": "push combined tag (has_assign, assign_val, add_val) to children; recurse; pull"
                },
                elimination_proof=(
                    "Composition algebra strictly preserves the mathematical execution order: any assignment clears prior "
                    "operations, and subsequent additions accumulate on top of the assigned value."
                ),
                state_updates={
                    "compose_and_push": "propagates composed tag to children, clears parent tags",
                    "pull": "tree[u] = merge(tree[2u], tree[2u+1])"
                }
            )

        if pattern == "segment_tree_metadata_aggregate":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain composite tuple (sum, min, max, count) simultaneously under point updates in O(log N)",
                decision_conditions={
                    "leaf_init": "sum = min = max = x, count = 1",
                    "merge_node": "sum = L.sum + R.sum; min = min(L.min, R.min); max = max(L.max, R.max); count = L.count + R.count"
                },
                elimination_proof=(
                    "All four metrics are independently associative and composable across sub-intervals, guaranteeing simultaneous correctness in O(log N)."
                ),
                state_updates={
                    "composite_pull": "reconstructs parent tuple from child tuples"
                }
            )

        if pattern == "segment_tree_max_subarray":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain maximum contiguous subarray sum (sum, pref, suff, ans) under point updates in O(log N)",
                decision_conditions={
                    "leaf_init": "sum = pref = suff = ans = A[i]",
                    "ordered_merge": "sum = L.sum + R.sum; pref = max(L.pref, L.sum + R.pref); suff = max(R.suff, R.sum + L.suff); ans = max({L.ans, R.ans, L.suff + R.pref})",
                    "query_merge": "combine disjoint canonical intervals strictly left-to-right using sentinel identity (empty = true)"
                },
                elimination_proof=(
                    "Any contiguous subarray either lies entirely in the left child, entirely in the right child, or straddles the boundary (L.suff + R.pref). "
                    "The merge exhaustively covers all possibilities in O(1)."
                ),
                state_updates={
                    "pull_max_sub": "updates parent max-subarray tuple from left and right children"
                }
            )

        if pattern == "segment_tree_frequency_order_statistic":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain dynamic frequency distribution and answer k-th element and rank queries in O(log M)",
                decision_conditions={
                    "k <= tree[2u].count": "k-th element is in left subtree [l, m]; recurse left",
                    "k > tree[2u].count": "k-th element is in right subtree [m+1, r]; k -= tree[2u].count; recurse right",
                    "l == r": "found exact value l"
                },
                elimination_proof=(
                    "Non-negative frequencies ensure tree[2u].count is monotonic, enabling single-pass O(log M) binary descent directly to the k-th element."
                ),
                state_updates={
                    "point_add": "increments or decrements leaf frequency and updates ancestor counts"
                }
            )

        if pattern == "segment_tree_interval_statistics":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maintain range extrema with exact multiplicity counts (min_val, min_count, max_val, max_count) in O(log N)",
                decision_conditions={
                    "L.min < R.min": "inherit L.min and L.min_count",
                    "R.min < L.min": "inherit R.min and R.min_count",
                    "L.min == R.min": "min_val = L.min, min_count = L.min_count + R.min_count",
                    "max_symmetric": "merge max_val and max_count symmetrically"
                },
                elimination_proof=(
                    "Conditional extrema merge preserves both global extrema and exact multiplicity without requiring full value frequency tables."
                ),
                state_updates={
                    "pull_stats": "reconstructs parent interval statistics from children"
                }
            )

        # ── Dynamic Programming Patterns (Phase 3K) ──
        if pattern == "dp_1d_linear":
            return MovementDerivation(
                pattern=pattern,
                objective_function="compute optimal prefix/sequence metric via 1D linear forward scan",
                decision_conditions={
                    "LIS transition": "dp[i] = 1 + max_{j < i, A[j] < A[i]} dp[j]",
                    "Kadane transition": "dp[i] = max(A[i], dp[i-1] + A[i])"
                },
                elimination_proof=(
                    "Prefix topological order guarantees all subproblems j < i are solved before i is evaluated, "
                    "exhaustively testing all legal predecessor extensions."
                ),
                state_updates={
                    "advance_index": "i += 1; dp[i] computed from dp[0..i-1]"
                }
            )

        if pattern == "dp_grid_2d":
            return MovementDerivation(
                pattern=pattern,
                objective_function="compute optimal path metric in 2D grid moving only right and down",
                decision_conditions={
                    "from_top": "dp[r-1][c] + grid[r][c]",
                    "from_left": "dp[r][c-1] + grid[r][c]",
                    "cell_choice": "dp[r][c] = min(from_top, from_left) or sum(from_top, from_left)"
                },
                elimination_proof=(
                    "Row-major iteration (r=0..R-1, c=0..C-1) satisfies DAG topological order since (r, c) only depends on (r-1, c) and (r, c-1)."
                ),
                state_updates={
                    "advance_cell": "c += 1 (or r += 1, c = 0); dp[r][c] finalized"
                }
            )

        if pattern == "dp_knapsack":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maximize value subject to weight constraint W",
                decision_conditions={
                    "exclude_item": "dp[i-1][w]",
                    "include_item (w >= weight[i])": "dp[i-1][w - weight[i]] + value[i]",
                    "0/1_choice": "dp[i][w] = max(exclude_item, include_item)",
                    "1D_reverse_sweep": "for w from W down to weight[i]: dp[w] = max(dp[w], dp[w - weight[i]] + value[i])"
                },
                elimination_proof=(
                    "Reverse weight iteration ensures each item is used at most once in 0/1 knapsack, "
                    "as dp[w - weight[i]] has not yet been updated for the current item i."
                ),
                state_updates={
                    "item_step": "i += 1; table row i computed from row i-1"
                }
            )

        if pattern == "dp_subsequence_string":
            return MovementDerivation(
                pattern=pattern,
                objective_function="compute optimal string alignment or subsequence score",
                decision_conditions={
                    "char_match (s1[i-1] == s2[j-1])": "dp[i-1][j-1] + 1 (or match cost)",
                    "char_mismatch": "max(dp[i-1][j], dp[i][j-1]) for LCS, or 1 + min(insert, delete, replace) for Edit Distance"
                },
                elimination_proof=(
                    "Evaluating in row-major order preserves prefix dependency DAG, exploring all alignment prefixes in O(|s1| * |s2|)."
                ),
                state_updates={
                    "advance_char": "j += 1 (or i += 1, j = 1); dp[i][j] finalized"
                }
            )

        if pattern == "dp_interval":
            return MovementDerivation(
                pattern=pattern,
                objective_function="find optimal cost of merging subsegments [i..j]",
                decision_conditions={
                    "split_choice": "for k from i to j-1: dp[i][k] + dp[k+1][j] + cost(i, k, j)",
                    "interval_opt": "dp[i][j] = min_{k} split_choice"
                },
                elimination_proof=(
                    "Iterating by increasing subsegment length (len = 2..N) ensures all strictly smaller sub-intervals [i..k] and [k+1..j] "
                    "are already solved before evaluating [i..j]."
                ),
                state_updates={
                    "advance_interval": "i += 1, j = i + len - 1; dp[i][j] finalized"
                }
            )

        if pattern == "dp_partition":
            return MovementDerivation(
                pattern=pattern,
                objective_function="partition array of length N into K contiguous segments with optimal metric",
                decision_conditions={
                    "prev_split": "for j from k-1 to i-1: max(dp[j][k-1], sum(j..i-1))",
                    "min_over_splits": "dp[i][k] = min_{j} prev_split"
                },
                elimination_proof=(
                    "Contiguous prefix partitioning guarantees subproblem optimality: optimal k-partition of prefix i depends on optimal (k-1)-partition of prefix j."
                ),
                state_updates={
                    "advance_partition": "k += 1, i += 1; dp[i][k] finalized"
                }
            )

        if pattern == "dp_state_machine":
            return MovementDerivation(
                pattern=pattern,
                objective_function="maximize profit over time subject to finite state machine transitions",
                decision_conditions={
                    "hold_state": "max(hold[i-1], rest[i-1] - price[i])",
                    "sold_state": "hold[i-1] + price[i]",
                    "rest_state": "max(rest[i-1], sold[i-1])"
                },
                elimination_proof=(
                    "FSM states capture all legal operational configurations, ensuring cooldown/fee rules are enforced without historical lookback."
                ),
                state_updates={
                    "day_step": "i += 1; states (hold, sold, rest) updated concurrently in O(1)"
                }
            )

        if pattern == "dp_bitmask":
            return MovementDerivation(
                pattern=pattern,
                objective_function="find optimal permutation or subset tour visiting all vertices",
                decision_conditions={
                    "transition_to_u": "min_{v in mask, v != u} (dp[mask ^ (1 << u)][v] + dist[v][u])",
                    "valid_mask": "mask & (1 << u) != 0"
                },
                elimination_proof=(
                    "Iterating masks numerically from 1 to 2^N - 1 guarantees that submask (mask ^ (1 << u)) is visited before mask."
                ),
                state_updates={
                    "mask_step": "mask += 1; dp[mask][u] computed for all u in mask"
                }
            )

        if pattern == "dp_tree":
            return MovementDerivation(
                pattern=pattern,
                objective_function="compute optimal tree metric via bottom-up post-order DFS",
                decision_conditions={
                    "child_aggregation": "aggregate dp[child][state] for all children of u",
                    "combine_states": "dp[u][state] = cost(u, state) + sum_{v in children} opt_child(v, state)"
                },
                elimination_proof=(
                    "Post-order traversal visits all subtree descendants before evaluating parent, ensuring complete subtree invariant."
                ),
                state_updates={
                    "dfs_pull": "subtree dp arrays merged into parent upon child return"
                }
            )

        if pattern == "dp_dag":
            return MovementDerivation(
                pattern=pattern,
                objective_function="compute longest or optimal path in Directed Acyclic Graph",
                decision_conditions={
                    "outgoing_edge": "dp[u] = max_{(u, v) in E} (dp[v] + weight(u, v))",
                    "sink_base": "if out_degree(u) == 0: dp[u] = 0"
                },
                elimination_proof=(
                    "Reverse topological sort guarantees all reachable vertices v from u are evaluated before u."
                ),
                state_updates={
                    "topo_step": "process next vertex in reverse topological order"
                }
            )

        if pattern == "dp_digit":
            return MovementDerivation(
                pattern=pattern,
                objective_function="count integers in [0..N] satisfying digit constraints",
                decision_conditions={
                    "digit_limit": "limit = tight ? digit[pos] : 9",
                    "recurse_digits": "sum_{d=0..limit} memo(pos+1, new_sum, tight && (d == limit), leading_zero && (d == 0))"
                },
                elimination_proof=(
                    "Digit position proceeds strictly from MSB to LSB; tight constraint relaxes as soon as a strictly smaller digit is chosen."
                ),
                state_updates={
                    "pos_step": "pos += 1; memo[pos][sum][tight][lz] cached"
                }
            )

        if pattern == "dp_optimization":
            return MovementDerivation(
                pattern=pattern,
                objective_function="accelerate DP transition argmin_k (dp[k] + cost(k, i)) from O(N) to O(1) amortized",
                decision_conditions={
                    "query_hull": "query optimal line/slope at x = i using binary search or deque pointer",
                    "insert_line": "maintain convexity by popping lines that are strictly dominated: intersect(L_new, L_back) <= intersect(L_back, L_second)"
                },
                elimination_proof=(
                    "Convexity / Monge property ensures candidate optimal split points are monotonically non-decreasing, allowing deque pruning."
                ),
                state_updates={
                    "hull_update": "prunes dominated lines; inserts new line in O(1) amortized"
                }
            )

        if pattern == "dp_solution_reconstruction":
            return MovementDerivation(
                pattern=pattern,
                objective_function="recover optimal sequence of decisions by backtracking from final state",
                decision_conditions={
                    "match_decision": "check which predecessor state p satisfies dp[cur] == dp[p] + cost(p, cur)",
                    "trace_step": "append decision to path; cur = p"
                },
                elimination_proof=(
                    "Following the decision chain that produced the optimum is guaranteed to produce an optimal path in O(length) time."
                ),
                state_updates={
                    "backtrack_step": "state = parent[state]; path.push_back(choice)"
                }
            )

        if pattern == "dp_space_optimization":
            return MovementDerivation(
                pattern=pattern,
                objective_function="minimize memory footprint by reusing state buffers across outer iterations",
                decision_conditions={
                    "reverse_iteration": "iterate inner loop in reverse (w = W..weight[i]) for 0/1 knapsack to preserve un-updated i-1 values",
                    "rolling_buffer": "swap cur and next row buffers: cur_row = 1 - cur_row"
                },
                elimination_proof=(
                    "States only depend on the immediately preceding row or higher capacities, so obsolete state rows can be overwritten safely."
                ),
                state_updates={
                    "buffer_swap": "dp_prev = dp_curr; dp_curr reset"
                }
            )

        # ── Greedy Algorithms (Phase 3L) ──
        if "interval_selection" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="maximize selected non-overlapping intervals",
                decision_conditions={
                    "start >= last_finish": "select interval and update last_finish = end",
                    "start < last_finish": "discard overlapping interval"
                },
                elimination_proof=(
                    "Intervals with earlier finish times leave maximum remaining room; overlapping intervals are safely discarded by exchange argument."
                ),
                state_updates={
                    "select": "last_finish = interval.end; count++",
                    "skip": "advance to next interval"
                }
            )

        if "interval_covering" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="minimize points to cover all intervals",
                decision_conditions={
                    "start > last_point": "place new point at interval.end",
                    "start <= last_point": "already covered by last_point"
                },
                elimination_proof=(
                    "Placing point at the rightmost endpoint of the first uncovered interval maximizes overlap with subsequent intervals."
                ),
                state_updates={
                    "place": "last_point = interval.end; points++",
                    "skip": "advance to next interval"
                }
            )

        if "fractional_knapsack" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="maximize total value within weight capacity W",
                decision_conditions={
                    "capacity >= weight": "take 100% of item",
                    "capacity < weight": "take fraction capacity / weight"
                },
                elimination_proof=(
                    "Taking highest value-density items first guarantees maximum average density across capacity W."
                ),
                state_updates={
                    "full_take": "val += v; cap -= w",
                    "fractional_take": "val += v * (cap/w); cap = 0"
                }
            )

        if "deadline_scheduling" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="minimize maximum lateness or weighted completion time",
                decision_conditions={
                    "EDD": "schedule in ascending deadline order",
                    "Smith": "schedule in descending w_i / p_i order"
                },
                elimination_proof=(
                    "Swapping any adjacent inversion does not increase maximum lateness (or strictly decreases weighted completion time)."
                ),
                state_updates={
                    "schedule": "time += p_i; lateness = max(lateness, time - d_i)"
                }
            )

        if "heap_assisted" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="minimize resource stops to reach destination",
                decision_conditions={
                    "fuel < 0": "extract maximum fuel from passed stations",
                    "fuel >= 0": "advance to next station"
                },
                elimination_proof=(
                    "Extracting the maximum available resource from past reachable stations maximizes the extension runway."
                ),
                state_updates={
                    "activate": "fuel += heap.pop(); stops++",
                    "pass": "heap.push(station_fuel)"
                }
            )

        if "huffman_merge" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="minimize weighted path length of merge tree",
                decision_conditions={
                    "merge": "extract two minimum elements from min-heap, combine and reinsert"
                },
                elimination_proof=(
                    "The two smallest elements must be siblings at maximum depth in an optimal tree; merging them preserves optimality by induction."
                ),
                state_updates={
                    "combine": "heap.push(heap.pop() + heap.pop()); cost += sum"
                }
            )

        if "sequence_local_choice" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="construct lexicographically minimal sequence under k deletions",
                decision_conditions={
                    "top > cur and k > 0": "pop stack, k--",
                    "otherwise": "push cur"
                },
                elimination_proof=(
                    "Higher place values dominate all lower place values; removing a larger predecessor digit strictly decreases the number."
                ),
                state_updates={
                    "pop": "stack.pop(); k--",
                    "push": "stack.push(cur)"
                }
            )

        if "reachability_partition" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="minimize jumps to reach destination",
                decision_conditions={
                    "i == jump_end": "jumps++; jump_end = max_reach",
                    "i < jump_end": "max_reach = max(max_reach, i + A[i])"
                },
                elimination_proof=(
                    "Greedy frontier max_reach stays ahead of any alternative jump sequence."
                ),
                state_updates={
                    "advance_frontier": "max_reach = max(max_reach, i + A[i])",
                    "jump": "jumps++; jump_end = max_reach"
                }
            )

        if "graph_mst" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="minimize total weight of spanning tree",
                decision_conditions={
                    "find(u) != find(v)": "include edge in MST; union(u, v)",
                    "find(u) == find(v)": "discard edge (cycle)"
                },
                elimination_proof=(
                    "Lightest edge crossing any cut is safe for MST (Cut Property); cycle-forming edges are redundant."
                ),
                state_updates={
                    "include": "dsu.union(u, v); mst_weight += w; edges++",
                    "discard": "skip edge"
                }
            )

        if "general_exchange" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="optimize global permutation objective via custom comparator",
                decision_conditions={
                    "comp(A, B)": "place A before B",
                    "!comp(A, B)": "place B before A"
                },
                elimination_proof=(
                    "Transitive comparator guarantees no adjacent swap can improve the global objective."
                ),
                state_updates={
                    "sort": "std::sort with comparator",
                    "scan": "accumulate optimal result"
                }
            )

        # ── Divide and Conquer & Backtracking (Phase 3M) ──
        if "merge_sort_inversions" in pattern or ("inversion" in pattern and "dc" in pattern):
            return MovementDerivation(
                pattern=pattern,
                objective_function="count inversions and reverse pairs via divide-and-conquer merge",
                decision_conditions={
                    "A[i] > A[j]": "inversions += (mid - i + 1); temp[k++] = A[j++]",
                    "A[i] <= A[j]": "temp[k++] = A[i++]"
                },
                elimination_proof=(
                    "Since left half A[l..m] is sorted, if A[i] > A[j], all subsequent elements in left half A[i..m] are strictly greater than A[j]."
                ),
                state_updates={
                    "merge": "copy merged elements back to A[l..r]",
                    "count": "accumulate cross-boundary inversions"
                }
            )

        if "quickselect" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="find k-th order statistic via 3-way partition without full sort",
                decision_conditions={
                    "k < lt": "recurse into [l..lt-1]",
                    "k in [lt..gt]": "return pivot A[k]",
                    "k > gt": "recurse into [gt+1..r]"
                },
                elimination_proof=(
                    "3-way partition places all elements equal to pivot in [lt..gt]; index k definitively selects which single partition to recurse into, safely eliminating the other two partitions."
                ),
                state_updates={
                    "partition": "3-way partition of A[l..r]",
                    "narrow": "update active search range [l..r]"
                }
            )

        if "closest_pair" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="find minimum Euclidean distance between any pair of 2D points",
                decision_conditions={
                    "dist(p_i, p_j) < delta": "delta = dist(p_i, p_j)",
                    "p_j.y - p_i.y >= delta": "break inner loop (at most 7 successors)"
                },
                elimination_proof=(
                    "Geometric packing in the 2*delta strip limits the number of points in any delta x delta box to at most 4; hence any point needs comparison with at most 7 successors in y-sorted order."
                ),
                state_updates={
                    "recurse": "delta = min(closest(left), closest(right))",
                    "strip_merge": "compare points within x_mid +- delta"
                }
            )

        if "tree_centroid" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="count or optimize paths in tree via centroid decomposition",
                decision_conditions={
                    "path through centroid": "combine paths from different subtrees",
                    "subtree component": "recurse into centroid-decomposed components"
                },
                elimination_proof=(
                    "Removing centroid C yields subtrees of size <= n/2; all paths either pass through C or lie entirely within one subtree component."
                ),
                state_updates={
                    "decompose": "mark centroid visited; build centroid tree",
                    "count": "aggregate path statistics through centroid"
                }
            )

        if "cdq" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="solve multi-dimensional offline queries via divide-and-conquer",
                decision_conditions={
                    "left_mod.dim2 <= right_query.dim2": "apply modification to Fenwick tree",
                    "otherwise": "query Fenwick tree for right query answer"
                },
                elimination_proof=(
                    "Primary dimension is separated by midpoint bisection (left < right); sorting both halves by secondary dimension allows two-pointer sweep with Fenwick tree."
                ),
                state_updates={
                    "left_to_right": "propagate left modifications to right queries",
                    "clear": "rollback Fenwick tree modifications"
                }
            )

        if "subsets_permutations" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="enumerate all valid combinatorial configurations",
                decision_conditions={
                    "i > start and A[i] == A[i-1]": "continue (skip duplicate branch)",
                    "otherwise": "path.push_back(A[i]); recurse; path.pop_back()"
                },
                elimination_proof=(
                    "Sorting elements ensures duplicate values are adjacent; skipping identical siblings when previous sibling was not chosen avoids duplicate combinatorial branches."
                ),
                state_updates={
                    "push": "path.push_back(A[i])",
                    "pop": "path.pop_back() (state restoration)"
                }
            )

        if "constraint_satisfaction" in pattern or "csp" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="find satisfying variable assignment subject to exact constraints",
                decision_conditions={
                    "bit & available_mask": "assign value, set bitmasks, recurse",
                    "no available value": "backtrack (domain wipeout)"
                },
                elimination_proof=(
                    "Bitwise constraint masks prune invalid choices in O(1) time without exploring dead-end subtrees."
                ),
                state_updates={
                    "assign": "cols |= bit; diag1 |= (bit << row); diag2 |= (bit >> row)",
                    "restore": "cols &= ~bit; diag1 &= ~(bit << row); diag2 &= ~(bit >> row)"
                }
            )

        if "branch_and_bound" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="find global optimal solution using admissible bounding function",
                decision_conditions={
                    "cost + bound >= best": "prune subtree",
                    "cost + bound < best": "branch to next decision"
                },
                elimination_proof=(
                    "Admissible lower bound guarantees that no completion of the current partial solution can beat best_cost."
                ),
                state_updates={
                    "branch": "cost += step_cost; recurse()",
                    "restore": "cost -= step_cost"
                }
            )

        if "state_space_search" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="search state space for target pattern or path",
                decision_conditions={
                    "valid_next_state and !visited": "mark visited, recurse, unmark",
                    "invalid or visited": "prune"
                },
                elimination_proof=(
                    "In-place visited marking prevents cyclic walks while exploring valid spatial or state extensions."
                ),
                state_updates={
                    "mark": "temp = board[r][c]; board[r][c] = '#'",
                    "unmark": "board[r][c] = temp (state restoration)"
                }
            )

        if "meet_in_the_middle" in pattern or "meet_in_middle" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="solve subset sum / combination for N <= 40 via bisection",
                decision_conditions={
                    "left_val + right_val == target": "optimal match found",
                    "search": "binary_search upper_bound in sorted left half"
                },
                elimination_proof=(
                    "Bisection of N elements into two sets of size N/2 reduces 2^N operations to 2 * 2^(N/2) + 2^(N/2) log(2^(N/2))."
                ),
                state_updates={
                    "generate_left": "left_sums.push_back(sum)",
                    "combine": "query sorted left_sums for each right_sum"
                }
            )

        # ── Phase 3N: Advanced Graph Movement Derivations ──
        if "01_bfs" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="find single-source shortest path on {0, 1}-weighted graph in O(V + E)",
                decision_conditions={
                    "edge_weight == 0": "push_front(v) (0-weight edge preserves current level d)",
                    "edge_weight == 1": "push_back(v) (1-weight edge advances to level d + 1)"
                },
                elimination_proof=(
                    "Monotonicity of distance levels: queue elements never differ in distance by more than 1. "
                    "Pushing 0-weight edges to the front ensures vertices are expanded in non-decreasing order of true distance, "
                    "avoiding Dijkstra log(V) heap overhead."
                ),
                state_updates={
                    "push_front": "dq.push_front(v); dist[v] = dist[u]",
                    "push_back": "dq.push_back(v); dist[v] = dist[u] + 1"
                }
            )

        if "spfa" in pattern or "negative_cycle" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="compute shortest paths or detect negative cycle with queue-based relaxation",
                decision_conditions={
                    "dist[v] > dist[u] + weight": "relax edge; if !in_queue[v]: push v, count[v]++",
                    "count[v] >= V": "negative cycle detected; terminate with cycle extraction"
                },
                elimination_proof=(
                    "Any simple shortest path in a graph with V vertices contains at most V - 1 edges. "
                    "By the Pigeonhole Principle, if any vertex is relaxed V times, a reachable negative cycle must exist."
                ),
                state_updates={
                    "relax": "dist[v] = dist[u] + w; parent[v] = u; in_queue[v] = true; q.push(v); count[v]++",
                    "pop": "in_queue[u] = false"
                }
            )

        if "eulerian" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="traverse every edge of the graph exactly once via Hierholzer trail stitching",
                decision_conditions={
                    "has_unused_edge(u)": "advance edge iterator; recurse/traverse edge (u, v)",
                    "no_unused_edge(u) (dead-end)": "push u to path trail; backtrack"
                },
                elimination_proof=(
                    "Because vertex degrees satisfy the Eulerian condition (all in-degree == out-degree or exactly 2 odd vertices), "
                    "any maximal trail from a vertex only terminates at a vertex when all incident edges are consumed, "
                    "allowing sub-circuits to be cleanly spliced."
                ),
                state_updates={
                    "traverse": "mark_edge_used(e); head[u]++",
                    "backtrack": "trail.push_back(u)"
                }
            )

        if "2sat" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="determine satisfiability of 2-CNF formula and find valid truth assignment",
                decision_conditions={
                    "comp[x] == comp[~x]": "formula unsatisfiable (x and ~x in same SCC)",
                    "comp[x] != comp[~x]": "assign val[x] = (comp[x] > comp[~x])"
                },
                elimination_proof=(
                    "If x and ~x belong to the same strongly connected component, x <=> ~x leads to a logical contradiction. "
                    "Otherwise, topological condensation ordering ensures that assigning truth to literals in reverse topological order "
                    "never propagates false -> true along implication edges."
                ),
                state_updates={
                    "implication_edge": "add_edge(~u, v); add_edge(~v, u)",
                    "assign": "val[x] = comp[x] > comp[~x]"
                }
            )

        if "block_cut" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="decompose graph into 2-vertex-connected components (blocks) and cut vertices",
                decision_conditions={
                    "low[v] >= tin[u]": "u is articulation point; pop edge stack to form block",
                    "tree_edge": "low[u] = min(low[u], low[v])",
                    "back_edge": "low[u] = min(low[u], tin[v])"
                },
                elimination_proof=(
                    "If low[v] >= tin[u], vertex v and its subtree have no back-edge to an ancestor of u, "
                    "meaning removal of u disconnects v from the rest of the graph, delineating a maximal biconnected component."
                ),
                state_updates={
                    "push_edge": "edge_stack.push_back({u, v})",
                    "pop_block": "extract edges until {u, v} into new block node"
                }
            )

        if "bridge_block" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="identify bridge edges and contract 2-edge-connected components",
                decision_conditions={
                    "low[v] > tin[u]": "edge (u, v) is a bridge",
                    "low[v] <= tin[u]": "edge (u, v) lies within a 2-edge-connected cycle"
                },
                elimination_proof=(
                    "If low[v] > tin[u], no vertex in v's DFS subtree has a back-edge to u or any ancestor of u. "
                    "Thus removal of edge (u, v) partitions the connected component."
                ),
                state_updates={
                    "mark_bridge": "is_bridge[edge_id] = true",
                    "contract": "2-edge-connected component flood-fill across non-bridge edges"
                }
            )

        if "bipartite_matching" in pattern or "kuhn" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="find maximum cardinality matching in bipartite graph via augmenting paths",
                decision_conditions={
                    "match[v] == -1": "augmenting path found; match[v] = u; return true",
                    "dfs(match[v])": "augmenting path extended through matched edge; match[v] = u; return true"
                },
                elimination_proof=(
                    "Berge's Lemma: A matching M is maximum if and only if there are no augmenting paths with respect to M. "
                    "Inverting matched and unmatched edges along an augmenting path strictly increases matching size by 1."
                ),
                state_updates={
                    "visit": "visited[v] = true",
                    "flip_match": "match[v] = u"
                }
            )

        if "max_flow" in pattern or "dinic" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="find maximum s-t flow in network via Dinic level graph blocking flows",
                decision_conditions={
                    "level[v] == level[u] + 1 and res_cap > 0": "push blocking flow along admissible edge",
                    "pushed == 0 or all arcs exhausted": "ptr[u]++ (current-arc pruning)"
                },
                elimination_proof=(
                    "In each phase, a maximal blocking flow is found in the layered DAG in O(V * E) time. "
                    "Each phase strictly increases the distance from source to sink in the residual network, "
                    "guaranteeing termination in at most V phases."
                ),
                state_updates={
                    "augment": "cap[u][v] -= pushed; cap[v][u] += pushed",
                    "advance_arc": "ptr[u]++"
                }
            )

        if "min_cut" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="find minimum capacity s-t cut partition separating source and sink",
                decision_conditions={
                    "cap[u][v] - flow[u][v] > 0": "v reachable from s in residual graph (v in S)",
                    "u in S and v in T": "cut edge across partition (S, T)"
                },
                elimination_proof=(
                    "Max-Flow Min-Cut Theorem: The value of maximum flow equals the capacity of the minimum cut. "
                    "Vertices reachable from s in the residual network form the source set S; saturated edges crossing to V \\ S "
                    "constitute the minimum cut."
                ),
                state_updates={
                    "residual_bfs": "visited[v] = true if residual capacity > 0",
                    "cut_classification": "in_cut_set[v] = visited[v]"
                }
            )

        if "mcmf" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="find minimum cost maximum flow on network with capacities and costs",
                decision_conditions={
                    "dist[v] > dist[u] + cost": "SPFA / Dijkstra relaxation along residual edge",
                    "sink reachable": "augment bottleneck capacity along shortest cost path"
                },
                elimination_proof=(
                    "Successive Shortest Path algorithm: Augmenting along the shortest path in the residual network maintains "
                    "the optimality condition (no negative cycles in the residual graph) while strictly increasing net flow toward maximum."
                ),
                state_updates={
                    "relax_cost": "dist[v] = dist[u] + cost[u][v]; parent_edge[v] = e",
                    "augment_flow": "cap[e] -= bot; cap[e ^ 1] += bot; total_flow += bot; total_cost += bot * cost[e]"
                }
            )

        # ── Phase 3O: String Algorithms & Automata ──
        if "string_kmp" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="find all exact occurrences of pattern P in text T in linear time",
                decision_conditions={
                    "T[i] == P[j]": "Advance both text and pattern pointers (i++, j++)",
                    "T[i] != P[j] and j > 0": "Retreat pattern pointer to pi[j-1] without rewinding text pointer i",
                    "T[i] != P[j] and j == 0": "Advance text pointer i++"
                },
                elimination_proof=(
                    "KMP Border Invariant: The proper prefix of length pi[j-1] is the longest prefix of P that is also a suffix "
                    "of T[i-j .. i-1]. Any longer prefix match is mathematically impossible by border maximality; "
                    "thus no potential occurrences are missed by shifting j to pi[j-1] without rewinding i."
                ),
                state_updates={
                    "match_step": "i++; j++; if j == M: report occurrence at i - M and set j = pi[j-1]",
                    "mismatch_step": "j = pi[j-1] if j > 0 else i++"
                }
            )

        if "string_z_algorithm" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="compute length of longest common prefix of S with every suffix S[i..]",
                decision_conditions={
                    "i > R": "Compare characters directly starting at index 0, initialize new Z-box [L, R]",
                    "i <= R and Z[i-L] < R - i + 1": "Set Z[i] = Z[i-L] without character comparisons (within Z-box)",
                    "i <= R and Z[i-L] >= R - i + 1": "Start comparison from R - i + 1, expand Z-box beyond R, update [L, R]"
                },
                elimination_proof=(
                    "Z-Box Invariant: For any i within [L, R], substring S[L .. R] matches prefix S[0 .. R-L]. "
                    "Therefore, the prefix of suffix S[i..] matches S[i-L .. R-L]. If Z[i-L] is strictly contained within the box, "
                    "Z[i] is identical by transitivity; comparisons are only performed when expanding strictly past R."
                ),
                state_updates={
                    "reuse_z": "Z[i] = min(R - i + 1, Z[i - L])",
                    "expand_box": "while S[Z[i]] == S[i + Z[i]]: Z[i]++; update L = i, R = i + Z[i] - 1"
                }
            )

        if "string_rabin_karp" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="locate pattern matches via rolling polynomial hash window in O(1) per shift",
                decision_conditions={
                    "H(window) == H(pattern)": "Hash equality: match confirmed under bounded collision probability (< 10^-14)",
                    "H(window) != H(pattern)": "Hash inequality: window definitely does not match pattern"
                },
                elimination_proof=(
                    "Polynomial Rolling Hash Invariant: Substring hash H(T[i..i+M-1]) can be computed in O(1) via "
                    "(pref[i+M] - pref[i] * base^M) mod P. By Schwarz-Zippel lemma and double independent prime moduli (10^9+7, 10^9+9), "
                    "collision probability across all N shifts is bounded below 10^-14."
                ),
                state_updates={
                    "shift_window": "H_new = ((H_old - T[i]*B^(M-1)) * B + T[i+M]) mod P",
                    "record_match": "report occurrence index i"
                }
            )

        if "string_manacher" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="find maximal palindromic radii centered at all indices in O(N) linear time",
                decision_conditions={
                    "i < R": "Initialize radius P[i] = min(R - i, P[2*C - i]) from symmetric mirror",
                    "i >= R": "Initialize radius P[i] = 0",
                    "boundary expansion": "Expand outward while S[i - P[i] - 1] == S[i + P[i] + 1]; if i + P[i] > R update C = i, R = i + P[i]"
                },
                elimination_proof=(
                    "Palindromic Symmetry Invariant: Within the active palindrome [C - P[C], C + P[C]], index i mirrors index i' = 2*C - i. "
                    "The substring centered at i is identical to that at i' up to boundary R. Comparisons only occur when expanding strictly "
                    "beyond R, guaranteeing each character is checked at most twice (O(N) total time)."
                ),
                state_updates={
                    "mirror_init": "P[i] = min(R - i, P[2 * C - i]) if i < R else 0",
                    "advance_boundary": "while matched: P[i]++; if i + P[i] > R: C = i, R = i + P[i]"
                }
            )

        if "string_aho_corasick" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="match entire dictionary of patterns simultaneously across streaming text",
                decision_conditions={
                    "goto(u, c) exists": "Traverse tree edge to child state u = goto(u, c)",
                    "goto(u, c) missing": "Follow suffix failure link u = fail[u] until valid transition or root",
                    "dict_link non-empty": "Report all patterns registered at u and its dictionary jump ancestors"
                },
                elimination_proof=(
                    "Aho-Corasick Automaton Invariant: Suffix failure link fail[u] points to the state representing the longest proper "
                    "suffix of string(u) that is a prefix in the trie. By following fail links on missing edges, no pattern matches "
                    "are missed, while text pointer i strictly advances without backtracking."
                ),
                state_updates={
                    "dfa_step": "curr = goto[curr][c]",
                    "collect_matches": "walk dict_link[curr] to accumulate pattern ids"
                }
            )

        if "string_suffix_array" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="construct sorted suffix permutation array and adjacent LCP array",
                decision_conditions={
                    "prefix doubling": "Sort suffixes by pairs (rank[i], rank[i + 2^k]) using radix/counting sort",
                    "kasai lcp": "Compare suffix S[i..] with predecessor S[sa[rank[i]-1]..] starting from h - 1"
                },
                elimination_proof=(
                    "Kasai Theorem Invariant: If LCP of suffix i is h, the LCP of suffix i+1 is at least h - 1. "
                    "Therefore h decreases by at most 1 per step, and can increase at most N times total, "
                    "proving the LCP construction completes in O(N) time after O(N log N) prefix doubling."
                ),
                state_updates={
                    "rank_update": "assign new discrete ranks based on sorted pair values",
                    "kasai_step": "h = max(0, h - 1); while S[i+h] == S[sa[rank[i]-1]+h]: h++; lcp[rank[i]-1] = h"
                }
            )

        if "string_suffix_automaton" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="construct minimal DFA recognizing all substrings of S in linear state space",
                decision_conditions={
                    "append character c": "Create new state cur with len[cur] = len[last] + 1",
                    "redirect suffix path": "Walk p = last along link[p], setting next[p][c] = cur while next[p][c] missing",
                    "continuous transition": "If len[q] == len[p] + 1, set link[cur] = q",
                    "split state": "If len[q] > len[p] + 1, clone q to clone_state, redirect transitions from p to clone, set links"
                },
                elimination_proof=(
                    "Right-Context Equivalence (Endpos) Theorem: Suffix automaton states correspond to equivalence classes "
                    "of substrings with identical endpos sets. State count is at most 2N - 1 and transitions at most 3N - 4. "
                    "Every substring corresponds to a unique path from root; distinct substring count equals sum(len[v] - len[link[v]])."
                ),
                state_updates={
                    "create_state": "cur = sz++; len[cur] = len[last] + 1",
                    "clone_state": "clone = sz++; len[clone] = len[p] + 1; next[clone] = next[q]; link[clone] = link[q]; link[q] = link[cur] = clone",
                    "update_last": "last = cur"
                }
            )

        if "string_lyndon_duval" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="factorize string into Lyndon words and identify minimal cyclic rotation",
                decision_conditions={
                    "S[j] == S[k]": "Periodic repetition in pre-Lyndon string: advance k++, j++",
                    "S[j] > S[k]": "Pre-Lyndon string strictly extends: reset k = i, advance j++",
                    "S[j] < S[k]": "End of Lyndon factor: output factors of length j - k, advance i += j - k, reset j = i + 1, k = i"
                },
                elimination_proof=(
                    "Duval Invariant: S[i .. j-1] is a pre-Lyndon word with period j - k. When S[j] < S[k], the pre-Lyndon property "
                    "breaks, and the prefix of length j - k is certified as a genuine Lyndon word. For doubled string S+S, "
                    "the first index i such that the factor length reaches N is guaranteed to be the lexicographically minimal rotation."
                ),
                state_updates={
                    "extend_periodic": "k++; j++",
                    "extend_simple": "k = i; j++",
                    "shift_factor": "i += j - k; j = i + 1; k = i"
                }
            )

        if "string_subsequence_automaton" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="verify subsequence queries in O(|Q|) query time without scanning text",
                decision_conditions={
                    "next_pos[curr][c] != -1": "Valid transition: jump to earliest occurrence curr = next_pos[curr][c] + 1",
                    "next_pos[curr][c] == -1": "Character c does not appear after curr: reject query as non-subsequence"
                },
                elimination_proof=(
                    "Greedy Subsequence Choice Theorem: Always choosing the earliest possible occurrence of character c in text "
                    "maximizes the remaining uninspected text suffix, strictly dominating any later choice of character c. "
                    "Therefore, next_pos table transitions preserve optimal subsequence matchability."
                ),
                state_updates={
                    "advance_pos": "curr = next_pos[curr][c] + 1",
                    "terminate_check": "if all characters of Q consumed, accept"
                }
            )

        if "string_longest_common_substring_sam" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="find longest common substring between two strings in linear time",
                decision_conditions={
                    "next[v][c] exists": "Extend current match: v = next[v][c], l++",
                    "next[v][c] missing and v != root": "Retreat along suffix link: v = link[v], l = len[v]",
                    "v == root": "Reset match length: l = 0"
                },
                elimination_proof=(
                    "SAM Traversal Invariant: The state v and length l maintain the longest suffix of S_2[0..i] that is a substring of S_1. "
                    "Following suffix links preserves the longest viable substring prefix upon mismatch. The maximum length l attained "
                    "across all steps is the global longest common substring."
                ),
                state_updates={
                    "extend_match": "v = next[v][c]; l++; update best_len = max(best_len, l)",
                    "retreat_link": "v = link[v]; l = len[v]"
                }
            )

        # ── Phase 3P: Number Theory & Combinatorics ──
        if "nt_extended_gcd" in pattern or "nt_diophantine" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="compute gcd(a, b) and Bezout coefficients x, y such that a*x + b*y = gcd(a, b)",
                decision_conditions={
                    "b == 0": "Base case reached: gcd = |a|, x = sgn(a), y = 0",
                    "b != 0": "Recursive Euclidean step: divide a by b, compute quotient q = a // b and remainder r = a % b"
                },
                elimination_proof=(
                    "Euclidean Division Invariant: Any common divisor of a and b also divides r = a - q*b. "
                    "The lattice of solutions a*x + b*y = c is non-empty iff gcd(a, b) divides c. "
                    "Bezout coefficients x, y are reconstructed without losing any lattice solutions."
                ),
                state_updates={
                    "recursive_step": "g = ext_gcd(b, a % b, x1, y1)",
                    "unwind_step": "x = y1; y = x1 - (a / b) * y1"
                }
            )

        if "nt_modular_inverse" in pattern or "nt_inv" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="find modular multiplicative inverse x such that a * x = 1 (mod m)",
                decision_conditions={
                    "m is certified prime": "Apply Fermat's Little Theorem: compute a^(m-2) mod m via binary exponentiation",
                    "m is general composite and gcd(a, m) == 1": "Apply Extended Euclidean Algorithm on a and m to find a*x + m*y = 1",
                    "gcd(a, m) != 1": "Fail closed: modular inverse does not exist because a and m share a common factor > 1"
                },
                elimination_proof=(
                    "Invertibility Theorem: In ring Z/mZ, an element a has a multiplicative inverse iff gcd(a, m) = 1. "
                    "When m is prime, all non-zero elements are coprime to m. For composite m, ExtGCD uniquely produces "
                    "the canonical inverse modulo m."
                ),
                state_updates={
                    "fermat_step": "inv = bin_exp(a, m - 2, m)",
                    "extgcd_step": "ext_gcd(a, m, x, y); inv = (x % m + m) % m"
                }
            )

        if "nt_chinese_remainder" in pattern or "nt_crt" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="solve simultaneous congruences x = r_i (mod m_i) for i = 0..K-1",
                decision_conditions={
                    "(r_i - x) % gcd(M, m_i) == 0": "Congruence is solvable; merge into accumulated solution",
                    "(r_i - x) % gcd(M, m_i) != 0": "Insolvability detected; fail closed with CRT_NO_SIMULTANEOUS_SOLUTION",
                    "new_lcm >= 2^127 - 1": "Fail closed with INTEGER_DOMAIN_EXCEEDED"
                },
                elimination_proof=(
                    "Chinese Remainder Theorem: Two congruences x = r1 (mod m1) and x = r2 (mod m2) have a simultaneous "
                    "solution iff r1 = r2 (mod gcd(m1, m2)). If solvable, the unique solution modulo lcm(m1, m2) "
                    "preserves all original constraints by induction."
                ),
                state_updates={
                    "merge_step": "t = (r_i - x) / g * inv(M/g, m_i/g) mod (m_i/g); x += M * t; M = lcm(M, m_i)"
                }
            )

        if "nt_linear_sieve" in pattern or "nt_prime_factorization" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="compute all primes and minimum prime factors (spf) up to N in strictly linear O(N) time",
                decision_conditions={
                    "spf[i] == 0": "Number i has no smaller factors; classify as prime, append to prime list, set spf[i] = i",
                    "p <= spf[i] and p * i <= N": "Mark composite spf[p * i] = p; advance to next prime",
                    "p > spf[i]": "Break inner loop: each composite is visited strictly by its smallest prime factor"
                },
                elimination_proof=(
                    "Euler Linear Sieve Uniqueness: Every composite number c can be uniquely written as c = p * i where p is the "
                    "smallest prime factor of c. The condition p <= spf[i] guarantees that p is indeed the smallest prime factor of p * i, "
                    "preventing any duplicate composite visits."
                ),
                state_updates={
                    "prime_discovery": "primes.push_back(i); spf[i] = i",
                    "composite_marking": "spf[p * i] = p"
                }
            )

        if "nt_euler_totient" in pattern or "nt_phi" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="compute Euler totient phi(N) counting integers 1 <= k <= N coprime to N",
                decision_conditions={
                    "d * d <= temp and temp % d == 0": "Found prime factor d; apply totient product term (d - 1) / d and divide out all d",
                    "temp > 1 at loop termination": "Remaining temp is prime; multiply by (temp - 1) / temp",
                    "linear sieve generation": "Use multiplicative property: phi(p*i) = phi(i)*(p-1) if p doesn't divide i else phi(i)*p"
                },
                elimination_proof=(
                    "Euler Product Formula: phi(N) = N * prod_{p | N} (1 - 1/p). By inclusion-exclusion, the proportion of "
                    "integers not divisible by any prime factor of N is exactly prod (1 - 1/p). Evaluating each distinct prime factor "
                    "once yields the exact totient count."
                ),
                state_updates={
                    "factor_removal": "ans -= ans / d; while (temp % d == 0) temp /= d",
                    "table_sieve": "phi[p * i] = (i % p == 0) ? phi[i] * p : phi[i] * (p - 1)"
                }
            )

        if "nt_mobius_inversion" in pattern or "nt_mobius_sieve" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="compute Mobius function mu(1..N) and reduce divisor-convolution sums",
                decision_conditions={
                    "i is prime": "Set mu[i] = -1",
                    "i % p == 0": "Prime p divides i, so p^2 divides p * i; set mu[p * i] = 0",
                    "i % p != 0": "Prime p does not divide i; square-free parity toggles, set mu[p * i] = -mu[i]"
                },
                elimination_proof=(
                    "Mobius Inversion Invariant: sum_{d | n} mu(d) = [n == 1]. Replacing the coprimality indicator [gcd(a, b) == 1] "
                    "with sum_{d | gcd(a, b)} mu(d) transforms quadratic double-summations into linear or sublinear harmonic block sweeps."
                ),
                state_updates={
                    "sieve_step": "mu[p * i] = (i % p == 0) ? 0 : -mu[i]",
                    "inversion_sum": "ans += mu[d] * (N / d) * (M / d)"
                }
            )

        if "nt_matrix_power" in pattern or "nt_linear_recurrence" in pattern or "nt_matrix_exponentiation" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="evaluate matrix power T^K mod M and solve linear recurrences in O(D^3 log K) time",
                decision_conditions={
                    "K & 1": "Multiply accumulated result matrix R by current base T: R = (R * T) mod M",
                    "always": "Square base transition matrix: T = (T * T) mod M; shift exponent K >>= 1",
                    "K == 0": "Terminate loop and return R (identity matrix if initial K was 0)"
                },
                elimination_proof=(
                    "Semigroup Exponentiation Invariant: Binary exponentiation relies on associativity of matrix multiplication. "
                    "The invariant R * T^K = T_initial^K_initial holds after every iteration. Logarithmic decomposition ensures "
                    "exact power calculation in floor(log2 K) + 1 steps."
                ),
                state_updates={
                    "accumulate": "R = mat_mul(R, T, M)",
                    "square_base": "T = mat_mul(T, T, M); K >>= 1"
                }
            )

        if "nt_combinatorics_factorials" in pattern or "nt_ncr_mod_p" in pattern or "nt_factorial_combinatorics" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="compute combinatorial combinations nCr mod p in O(1) query time using precomputed factorial tables",
                decision_conditions={
                    "r < 0 or r > n": "Combination is outside valid domain; short-circuit to 0",
                    "0 <= r <= n and n < p": "Evaluate formula: fact[n] * invFact[r] % p * invFact[n - r] % p",
                    "n >= p": "Invalid precondition: n! is 0 mod p, inverse does not exist; routes to Lucas theorem"
                },
                elimination_proof=(
                    "Factorial Inversion Invariant: For prime p and n < p, fact[n] has no factors of p and is invertible in F_p. "
                    "Backward telescoping invFact[i-1] = invFact[i] * i mod p correctly populates all inverse factorials from a single "
                    "modular inverse of fact[N]."
                ),
                state_updates={
                    "fact_precomp": "fact[i] = (fact[i-1] * i) % p",
                    "inv_fact_unwind": "invFact[i-1] = (invFact[i] * i) % p"
                }
            )

        if "nt_lucas_theorem" in pattern or "nt_lucas" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="compute nCr mod p for large n, r >= p with small prime p using Lucas base-p decomposition",
                decision_conditions={
                    "r_i > n_i": "Base-p digit combination binom(n_i, r_i) is 0; entire product becomes 0 mod p",
                    "r_i <= n_i": "Multiply accumulated answer by small combination binom(n_i, r_i) mod p",
                    "n == 0 and r == 0": "All base-p digits processed; return accumulated answer"
                },
                elimination_proof=(
                    "Lucas Congruence Theorem: (1 + X)^n = (1 + X)^{sum n_i p^i} = prod (1 + X^{p^i})^{n_i} = prod sum binom(n_i, r_i) X^{r_i p^i} (mod p). "
                    "Matching powers of X gives binom(n, r) = prod binom(n_i, r_i) (mod p). Large combinatorics reduces to independent "
                    "subproblems within the prime field F_p."
                ),
                state_updates={
                    "digit_extract": "n_i = n % p; r_i = r % p; n /= p; r /= p",
                    "accumulate": "ans = (ans * nCr_small(n_i, r_i, p)) % p"
                }
            )

        if "nt_miller_rabin" in pattern or "nt_primality_test" in pattern:
            return MovementDerivation(
                pattern=pattern,
                objective_function="certify primality of integer N < 2^64 deterministically using locked 7-witness basis",
                decision_conditions={
                    "x == 1 or x == N - 1": "Witness passes at initial power a^d mod N",
                    "x^2 == N - 1 in <= s-1 squarings": "Witness passes; non-trivial square root of 1 not encountered",
                    "never reaches N - 1": "Witness confirms N is composite via non-trivial square root of unity or Fermat failure"
                },
                elimination_proof=(
                    "Miller-Rabin Deterministic Primality: If N is prime, the only square roots of 1 in Z/N Z are 1 and -1. "
                    "By exhaustive mathematical verification, the 7-witness set {2, 325, 9375, 28178, 450775, 9780504, 1795265022} "
                    "has zero pseudoprimes for all unsigned 64-bit integers N < 2^64."
                ),
                state_updates={
                    "initial_power": "x = power_mod(a, d, N)",
                    "squaring_loop": "x = mul_mod(x, x, N)"
                }
            )

        # Default fallback
        return MovementDerivation(
            pattern=pattern,
            objective_function="satisfy problem constraints with linear pointer sweep",
            decision_conditions={"progress": "advance pointers toward termination"},
            elimination_proof="Search space monotonically shrinks with each pointer step.",
            state_updates={"step": "pointers adjust toward convergence"}
        )
