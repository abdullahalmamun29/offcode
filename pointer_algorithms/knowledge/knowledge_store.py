"""
Knowledge Store for Pointer-Based Algorithms.

Stores both foundational domain rules and induced abstractions.
Confidence levels: CANDIDATE -> VALIDATED -> REPEATEDLY_VALIDATED.
"""

from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import json

class ConfidenceLevel(str, Enum):
    CANDIDATE = "candidate"
    VALIDATED = "validated"
    REPEATEDLY_VALIDATED = "repeatedly_validated"

@dataclass
class AlgorithmicRule:
    rule_id: str
    domain: str
    pattern: str
    preconditions: List[str]
    state_variables: List[str]
    pointer_roles: List[Dict[str, Any]]
    invariant: Dict[str, str]  # before, during, after, termination
    monotonic_relation: str
    movement_rule: Dict[str, str]
    elimination_proof: str
    complexity: Dict[str, str]  # time, space, preprocessing
    failure_conditions: List[str]
    supporting_examples: List[str] = field(default_factory=list)
    counterexamples: List[str] = field(default_factory=list)
    confidence_level: ConfidenceLevel = ConfidenceLevel.CANDIDATE
    validation_count: int = 1

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['confidence_level'] = self.confidence_level.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AlgorithmicRule":
        data_copy = dict(data)
        if isinstance(data_copy.get('confidence_level'), str):
            data_copy['confidence_level'] = ConfidenceLevel(data_copy['confidence_level'])
        return cls(**data_copy)


class KnowledgeStore:
    """In-memory and persistent knowledge store for algorithmic rules."""

    def __init__(self):
        self.rules: Dict[str, AlgorithmicRule] = {}
        self._load_foundational_rules()

    def _load_foundational_rules(self):
        # 1. Converging Pair Sum
        self.add_rule(AlgorithmicRule(
            rule_id="converging_pair_sum_sorted",
            domain="pointer_algorithms",
            pattern="pair_sum_sorted",
            preconditions=["sorted_order", "search_space_monotonicity"],
            state_variables=["L", "R", "current_sum", "target"],
            pointer_roles=[
                {"name": "L", "role": "left_bound", "direction": "increment", "represents": "Smallest candidate value"},
                {"name": "R", "role": "right_bound", "direction": "decrement", "represents": "Largest candidate value"}
            ],
            invariant={
                "before": "Array is sorted. Search space is pairs (i, j) with 0 <= i < j < n.",
                "during": "Optimal or matching pair (if it exists) lies in the index range [L, R].",
                "after": "If A[L] + A[R] < target, for any k <= R, A[L] + A[k] <= A[L] + A[R] < target, so L cannot pair with any remaining candidate. Incrementing L safely eliminates all pairs (L, k). Conversely for R--.",
                "termination": "L >= R means all potential pairs have been evaluated or safely pruned."
            },
            monotonic_relation="value_order_monotonicity: a[i] <= a[j] for i < j implies a[i] + a[k] <= a[j] + a[k].",
            movement_rule={
                "sum < target": "L++",
                "sum > target": "R--",
                "sum == target": "match found; record or advance"
            },
            elimination_proof="Because array is non-decreasing, for any k < R, A[L] + A[k] <= A[L] + A[R] < target. Therefore no pair starting with L can equal or exceed target with remaining elements. L is safely eliminated.",
            complexity={"time": "O(N)", "space": "O(1)", "preprocessing": "O(N log N) if sorting required"},
            failure_conditions=["UNSORTED_WITHOUT_SORTING_ALLOWED", "INDEX_PRESERVATION_LOST"],
            supporting_examples=["two_sum_sorted", "pair_with_given_sum"],
            confidence_level=ConfidenceLevel.REPEATEDLY_VALIDATED,
            validation_count=10
        ))

        # 2. Container With Most Water
        self.add_rule(AlgorithmicRule(
            rule_id="converging_container_most_water",
            domain="pointer_algorithms",
            pattern="container_most_water",
            preconditions=["contiguous_bounds", "objective_monotonicity"],
            state_variables=["L", "R", "h_L", "h_R", "max_area"],
            pointer_roles=[
                {"name": "L", "role": "left_bound", "direction": "increment", "represents": "Left boundary line"},
                {"name": "R", "role": "right_bound", "direction": "decrement", "represents": "Right boundary line"}
            ],
            invariant={
                "before": "L=0, R=n-1 captures maximum possible width.",
                "during": "The global maximum area is either in the evaluated area history or formed by boundaries in [L, R].",
                "after": "Area is min(h[L], h[R]) * (R - L). If h[L] <= h[R], for any k < R, min(h[L], h[k]) * (k - L) <= h[L] * (k - L) < h[L] * (R - L). Hence L cannot form a larger area with any inner line k. Eliminating L is strictly safe.",
                "termination": "L >= R leaves no positive width container."
            },
            monotonic_relation="objective_monotonicity: width strictly decreases with movement; the shorter vertical bar upper-bounds all inner pairs using it.",
            movement_rule={
                "h[L] <= h[R]": "L++",
                "h[L] > h[R]": "R--"
            },
            elimination_proof="Assume h[L] <= h[R]. For any k < R, width (k - L) < (R - L) and height min(h[L], h[k]) <= h[L]. Thus area(L, k) <= h[L] * (k - L) < h[L] * (R - L) = area(L, R). L cannot beat current area.",
            complexity={"time": "O(N)", "space": "O(1)", "preprocessing": "None"},
            failure_conditions=["NON_POSITIVE_WIDTH", "NON_MONOTONIC_OBJECTIVE"],
            supporting_examples=["container_with_most_water"],
            confidence_level=ConfidenceLevel.REPEATEDLY_VALIDATED,
            validation_count=8
        ))

        # 3. In-Place Compaction / Deduplication
        self.add_rule(AlgorithmicRule(
            rule_id="same_direction_compaction",
            domain="pointer_algorithms",
            pattern="remove_duplicates_sorted",
            preconditions=["sorted_order_or_filtering", "in_place_modification_allowed"],
            state_variables=["slow_write", "fast_read"],
            pointer_roles=[
                {"name": "slow_write", "role": "slow_write", "direction": "increment", "represents": "Boundary of valid compacted prefix"},
                {"name": "fast_read", "role": "fast_read", "direction": "increment", "represents": "Scanner inspecting each input element"}
            ],
            invariant={
                "before": "slow_write=0, fast_read=1. Prefix [0..slow_write] is deduplicated and valid.",
                "during": "Prefix [0..slow_write] contains all unique elements discovered so far in their original relative order.",
                "after": "When fast_read finds a distinct value, incrementing slow_write and assigning preserves unique prefix.",
                "termination": "fast_read reaches n, prefix [0..slow_write] contains the exact filtered sequence."
            },
            monotonic_relation="pointer_elimination_monotonicity: fast_read advances monotonically through the array, skipping redundant duplicates.",
            movement_rule={
                "a[fast_read] != a[slow_write]": "slow_write++; a[slow_write] = a[fast_read]; fast_read++",
                "a[fast_read] == a[slow_write]": "fast_read++"
            },
            elimination_proof="Duplicate elements are redundant according to the uniqueness predicate and safely bypassed by fast_read.",
            complexity={"time": "O(N)", "space": "O(1)", "preprocessing": "None"},
            failure_conditions=["OUT_OF_PLACE_MUTATION_FORBIDDEN"],
            supporting_examples=["remove_duplicates_from_sorted_array", "move_zeroes"],
            confidence_level=ConfidenceLevel.REPEATEDLY_VALIDATED,
            validation_count=8
        ))

        # 4. Variable Sliding Window (Longest Valid / At Most K Distinct)
        self.add_rule(AlgorithmicRule(
            rule_id="sliding_window_variable_max",
            domain="pointer_algorithms",
            pattern="sliding_window_variable_max",
            preconditions=["contiguous_subarray", "window_validity_monotonicity"],
            state_variables=["L", "R", "window_state", "max_len"],
            pointer_roles=[
                {"name": "L", "role": "window_start", "direction": "increment", "represents": "Left bound of current window"},
                {"name": "R", "role": "window_end", "direction": "increment", "represents": "Right bound of current window"}
            ],
            invariant={
                "before": "L=0, R=0, window is empty or single element.",
                "during": "After shrinking L to restore validity, window [L..R] satisfies the validity predicate.",
                "after": "Expanding R adds a[R] to window state. If invalid, incrementing L monotonically restores validity because removing elements monotonically relaxes the constraint (e.g. distinct count non-increasing).",
                "termination": "R reaches n, maximum valid window length observed is optimal."
            },
            monotonic_relation="window_validity_monotonicity: shrinking L monotonically decreases violation count or distinct element count, ensuring validity is predictably recoverable.",
            movement_rule={
                "add(R)": "update state",
                "while not valid": "remove(L); L++",
                "when valid": "max_len = max(max_len, R - L + 1); R++"
            },
            elimination_proof="For any fixed R, shrinking L is minimal necessary step; any subsegment starting prior to L when invalid is also invalid.",
            complexity={"time": "O(N)", "space": "O(K) auxiliary state", "preprocessing": "None"},
            failure_conditions=["WINDOW_NOT_MONOTONIC"],
            supporting_examples=["longest_substring_k_distinct", "longest_subarray_sum_at_most_s"],
            confidence_level=ConfidenceLevel.REPEATEDLY_VALIDATED,
            validation_count=8
        ))

        # 5. Variable Sliding Window (Shortest Valid / Sum >= S)
        self.add_rule(AlgorithmicRule(
            rule_id="sliding_window_variable_min",
            domain="pointer_algorithms",
            pattern="sliding_window_variable_min",
            preconditions=["contiguous_subarray", "window_validity_monotonicity", "non_negative_incremental"],
            state_variables=["L", "R", "current_sum", "min_len", "target"],
            pointer_roles=[
                {"name": "L", "role": "window_start", "direction": "increment", "represents": "Left bound of valid window"},
                {"name": "R", "role": "window_end", "direction": "increment", "represents": "Right bound of expanding window"}
            ],
            invariant={
                "before": "L=0, R=0, sum=0, min_len=infinity.",
                "during": "Whenever sum >= target, window [L..R] is valid; updating min_len and shrinking L checks if smaller window is also valid.",
                "after": "Because all elements >= 0, sum monotonically increases with R and monotonically decreases with L.",
                "termination": "R reaches n and all valid minimal left endpoints explored."
            },
            monotonic_relation="value_order_monotonicity & window_validity_monotonicity: non-negative array entries guarantee prefix sums of window are non-decreasing.",
            movement_rule={
                "add(R)": "sum += a[R]",
                "while sum >= target": "min_len = min(min_len, R - L + 1); sum -= a[L]; L++",
                "after while": "R++"
            },
            elimination_proof="Since elements are non-negative, if [L..R] has sum >= target, checking if [L+1..R] is also >= target explores strictly smaller candidates. If sum < target, any subsegment of [L..R] ending at R also has sum < target, so R must expand.",
            complexity={"time": "O(N)", "space": "O(1)", "preprocessing": "None"},
            failure_conditions=["WINDOW_NOT_MONOTONIC", "NEGATIVE_VALUES_PRESENT"],
            supporting_examples=["min_size_subarray_sum"],
            confidence_level=ConfidenceLevel.REPEATEDLY_VALIDATED,
            validation_count=8
        ))

        # 6. Partition Pointers (Dutch National Flag 3-Way)
        self.add_rule(AlgorithmicRule(
            rule_id="partition_dutch_national_flag",
            domain="pointer_algorithms",
            pattern="partition_dutch_flag",
            preconditions=["in_place_modification_allowed", "three_way_predicate"],
            state_variables=["low", "mid", "high"],
            pointer_roles=[
                {"name": "low", "role": "low_boundary", "direction": "increment", "represents": "Boundary for elements < pivot (region 0)"},
                {"name": "mid", "role": "mid_scanner", "direction": "increment", "represents": "Scanner for elements == pivot (region 1)"},
                {"name": "high", "role": "high_boundary", "direction": "decrement", "represents": "Boundary for elements > pivot (region 2)"}
            ],
            invariant={
                "before": "low=0, mid=0, high=n-1. All regions uninspected.",
                "during": "Regions: a[0..low-1] < pivot, a[low..mid-1] == pivot, a[mid..high] uninspected, a[high+1..n-1] > pivot.",
                "after": "Swapping a[mid] into respective boundary and adjusting pointer preserves 4-region partition invariant.",
                "termination": "mid > high means uninspected region is empty; entire array partitioned."
            },
            monotonic_relation="pointer_elimination_monotonicity: uninspected window [mid..high] shrinks at every step.",
            movement_rule={
                "a[mid] == 0": "swap(a[low], a[mid]); low++; mid++",
                "a[mid] == 1": "mid++",
                "a[mid] == 2": "swap(a[mid], a[high]); high--"
            },
            elimination_proof="Every element swapped into [0..low-1] is known to be 0; elements in [low..mid-1] are known to be 1; elements in [high+1..n-1] are known to be 2. The uninspected segment strictly decreases.",
            complexity={"time": "O(N)", "space": "O(1)", "preprocessing": "None"},
            failure_conditions=["NON_PARTITIONABLE_KEYS"],
            supporting_examples=["sort_colors_012", "dutch_national_flag"],
            confidence_level=ConfidenceLevel.REPEATEDLY_VALIDATED,
            validation_count=8
        ))

        # 7. Fast/Slow Pointers on Linked Structures (Floyd's Cycle)
        self.add_rule(AlgorithmicRule(
            rule_id="fast_slow_cycle_detection",
            domain="pointer_algorithms",
            pattern="linked_cycle_detection",
            preconditions=["linked_structure_or_functional_graph", "relative_speed_progression"],
            state_variables=["slow", "fast"],
            pointer_roles=[
                {"name": "slow", "role": "tortoise", "direction": "step_1", "represents": "Pointer moving 1 step per iteration"},
                {"name": "hare", "role": "hare", "direction": "step_2", "represents": "Pointer moving 2 steps per iteration"}
            ],
            invariant={
                "before": "slow = head, fast = head.",
                "during": "If a cycle of length C exists, the distance between fast and slow modulo C decreases by 1 on every step.",
                "after": "Relative speed = 2 - 1 = 1 node per iteration, guaranteeing convergence within at most C steps inside cycle.",
                "termination": "fast reaches null (no cycle) OR fast == slow (cycle detected)."
            },
            monotonic_relation="relative_speed_progression: distance between pointers modulo cycle length strictly decreases.",
            movement_rule={
                "step": "slow = slow->next; fast = fast->next->next",
                "collision": "if slow == fast return true",
                "end": "if fast == null || fast->next == null return false"
            },
            elimination_proof="In a finite cycle of length C, relative distance d decreases by (2 - 1) = 1 each step. Since 1 and C are coprime (distance reduces mod C), fast must meet slow without hopping over.",
            complexity={"time": "O(N)", "space": "O(1)", "preprocessing": "None"},
            failure_conditions=["ARBITRARY_GRAPH_NOT_FUNCTIONAL"],
            supporting_examples=["linked_list_cycle", "find_duplicate_number_floyd"],
            confidence_level=ConfidenceLevel.REPEATEDLY_VALIDATED,
            validation_count=8
        ))

    def add_rule(self, rule: AlgorithmicRule) -> None:
        self.rules[rule.rule_id] = rule

    def get_rule(self, rule_id: str) -> Optional[AlgorithmicRule]:
        return self.rules.get(rule_id)

    def find_rules_by_pattern(self, pattern: str) -> List[AlgorithmicRule]:
        return [r for r in self.rules.values() if r.pattern == pattern]

    def all_rules(self) -> List[AlgorithmicRule]:
        return list(self.rules.values())
