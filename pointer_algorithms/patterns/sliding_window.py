"""
Sliding Window Patterns with Strong Formal Abstraction:
- Window State
- State Update on R (add)
- Validity Predicate
- State Update on L (remove)
- Monotonic Property
- Objective Update

Subtypes:
1. Fixed-size window (size K, e.g. maximum sum)
2. Variable-size window (longest valid segment, e.g. <= K distinct values)
3. Variable-size window (shortest valid segment, e.g. sum >= S)
"""

from typing import Dict, Any, List, Optional
from collections import defaultdict
from dataclasses import dataclass, field
from pointer_algorithms.patterns.base import BasePointerPattern
from pointer_algorithms.knowledge.pointer_roles import PointerRole, RoleType
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine, FormalInvariant
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine, MovementDerivation

@dataclass
class WindowState:
    current_sum: int = 0
    frequencies: Dict[Any, int] = field(default_factory=lambda: defaultdict(int))
    distinct_count: int = 0

    def add_element(self, val: Any) -> None:
        if isinstance(val, (int, float)):
            self.current_sum += val
        if self.frequencies[val] == 0:
            self.distinct_count += 1
        self.frequencies[val] += 1

    def remove_element(self, val: Any) -> None:
        if isinstance(val, (int, float)):
            self.current_sum -= val
        self.frequencies[val] -= 1
        if self.frequencies[val] == 0:
            self.distinct_count -= 1
            del self.frequencies[val]


class SlidingWindowFixedPattern(BasePointerPattern):
    @property
    def pattern_name(self) -> str:
        return "sliding_window_fixed"

    @property
    def family_name(self) -> str:
        return "sliding_window"

    def get_pointer_roles(self) -> List[PointerRole]:
        return [
            PointerRole(
                role=RoleType.WINDOW_START,
                name="L",
                initial_position="0",
                direction="increment",
                represents="Left boundary of fixed window [L..L+K-1]",
                invariants_maintained="Tracks position being evicted when window slides"
            ),
            PointerRole(
                role=RoleType.WINDOW_END,
                name="R",
                initial_position="K - 1",
                direction="increment",
                represents="Right boundary of fixed window",
                invariants_maintained="Distance R - L + 1 == K at each evaluation"
            )
        ]

    def get_invariant(self, params: Dict[str, Any]) -> FormalInvariant:
        k = params.get("k", "K")
        return FormalInvariant(
            pattern=self.pattern_name,
            before_iteration=f"First window of size {k} is accumulated into window_sum.",
            during_iteration=f"Window contains exactly {k} consecutive elements; max_sum stores optimum.",
            after_movement="window_sum += a[R] - a[R - k]; advances both boundaries by 1 in O(1) time.",
            at_termination="All contiguous windows of length K evaluated."
        )

    def derive_movement(self, params: Dict[str, Any]) -> MovementDerivation:
        return MovementDerivationEngine.derive(self.pattern_name, params)

    def simulate_step_by_step(self, arr: List[int], params: Dict[str, Any]) -> Dict[str, Any]:
        k = params.get("k", 1)
        n = len(arr)
        if k > n or k <= 0:
            return {"max_sum": -1, "steps": []}

        state = WindowState()
        for i in range(k):
            state.add_element(arr[i])

        max_sum = state.current_sum
        steps = [{"step": 0, "window": arr[:k], "window_sum": state.current_sum, "max_sum": max_sum}]

        for r in range(k, n):
            evicted = arr[r - k]
            added = arr[r]
            state.remove_element(evicted)
            state.add_element(added)
            if state.current_sum > max_sum:
                max_sum = state.current_sum
            steps.append({
                "step": r - k + 1,
                "evicted": evicted,
                "added": added,
                "window_sum": state.current_sum,
                "max_sum": max_sum
            })

        return {"max_sum": max_sum, "steps": steps}


class SlidingWindowVariableMaxPattern(BasePointerPattern):
    """Longest valid contiguous segment (e.g. at most K distinct elements, or sum <= S on positives)."""

    @property
    def pattern_name(self) -> str:
        return "sliding_window_variable_max"

    @property
    def family_name(self) -> str:
        return "sliding_window"

    def get_pointer_roles(self) -> List[PointerRole]:
        return [
            PointerRole(
                role=RoleType.WINDOW_START,
                name="L",
                initial_position="0",
                direction="increment",
                represents="Left boundary shrinking window to restore validity",
                invariants_maintained="Advances until validity predicate is satisfied"
            ),
            PointerRole(
                role=RoleType.WINDOW_END,
                name="R",
                initial_position="0",
                direction="increment",
                represents="Right boundary expanding search space",
                invariants_maintained="Considers every element as potential right endpoint"
            )
        ]

    def get_invariant(self, params: Dict[str, Any]) -> FormalInvariant:
        return InvariantEngine.construct_invariant("sliding_window_variable_max", params)

    def derive_movement(self, params: Dict[str, Any]) -> MovementDerivation:
        return MovementDerivationEngine.derive("sliding_window_variable_max", params)

    def simulate_step_by_step(self, arr: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        k_distinct = params.get("k_distinct", None)
        max_sum_cap = params.get("max_sum_cap", None)
        n = len(arr)

        state = WindowState()
        L = 0
        max_len = 0
        best_window = (0, 0)
        steps = []

        def is_valid() -> bool:
            if k_distinct is not None and state.distinct_count > k_distinct:
                return False
            if max_sum_cap is not None and state.current_sum > max_sum_cap:
                return False
            return True

        for R in range(n):
            state.add_element(arr[R])

            while not is_valid() and L <= R:
                state.remove_element(arr[L])
                L += 1

            current_len = R - L + 1
            if current_len > max_len:
                max_len = current_len
                best_window = (L, R)

            steps.append({
                "R": R, "L": L, "window_len": current_len,
                "distinct_count": state.distinct_count,
                "current_sum": state.current_sum,
                "max_len": max_len
            })

        return {
            "max_len": max_len,
            "best_window": best_window,
            "steps": steps
        }


class SlidingWindowVariableMinPattern(BasePointerPattern):
    """Shortest valid contiguous segment (e.g. min length subarray with sum >= S on non-negatives)."""

    @property
    def pattern_name(self) -> str:
        return "sliding_window_variable_min"

    @property
    def family_name(self) -> str:
        return "sliding_window"

    def get_pointer_roles(self) -> List[PointerRole]:
        return [
            PointerRole(
                role=RoleType.WINDOW_START,
                name="L",
                initial_position="0",
                direction="increment",
                represents="Left boundary probing minimal length while valid",
                invariants_maintained="Evicts elements while maintaining validity"
            ),
            PointerRole(
                role=RoleType.WINDOW_END,
                name="R",
                initial_position="0",
                direction="increment",
                represents="Right boundary expanding to accumulate requirement",
                invariants_maintained="Advances when window sum is below threshold"
            )
        ]

    def get_invariant(self, params: Dict[str, Any]) -> FormalInvariant:
        return InvariantEngine.construct_invariant("sliding_window_variable_min", params)

    def derive_movement(self, params: Dict[str, Any]) -> MovementDerivation:
        return MovementDerivationEngine.derive("sliding_window_variable_min", params)

    def simulate_step_by_step(self, arr: List[int], params: Dict[str, Any]) -> Dict[str, Any]:
        target = params.get("target", 0)
        n = len(arr)
        state = WindowState()
        L = 0
        min_len = float('inf')
        best_window = None
        steps = []

        for R in range(n):
            state.add_element(arr[R])

            while state.current_sum >= target and L <= R:
                cur_len = R - L + 1
                if cur_len < min_len:
                    min_len = cur_len
                    best_window = (L, R)

                steps.append({
                    "R": R, "L": L, "cur_len": cur_len,
                    "window_sum": state.current_sum, "target": target,
                    "action": "RECORD_AND_SHRINK"
                })
                state.remove_element(arr[L])
                L += 1

        res_len = min_len if min_len != float('inf') else 0
        return {
            "min_len": res_len,
            "best_window": best_window,
            "steps": steps
        }
