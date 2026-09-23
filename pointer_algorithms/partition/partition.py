"""
Partition Pointers (Dutch National Flag & Two-Way Partition).
"""

from typing import Dict, Any, List
from pointer_algorithms.patterns.base import BasePointerPattern
from pointer_algorithms.knowledge.pointer_roles import PointerRole, RoleType
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine, FormalInvariant
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine, MovementDerivation

class DutchNationalFlagPattern(BasePointerPattern):
    @property
    def pattern_name(self) -> str:
        return "partition_dutch_flag"

    @property
    def family_name(self) -> str:
        return "partition_pointers"

    def get_pointer_roles(self) -> List[PointerRole]:
        return [
            PointerRole(
                role=RoleType.LOW_BOUNDARY,
                name="low",
                initial_position="0",
                direction="increment",
                represents="Upper exclusive bound of region 0 (elements < pivot)",
                invariants_maintained="A[0..low-1] contains only elements < pivot"
            ),
            PointerRole(
                role=RoleType.MID_SCANNER,
                name="mid",
                initial_position="0",
                direction="increment",
                represents="Current inspection pointer and upper bound of region 1",
                invariants_maintained="A[low..mid-1] contains only elements == pivot"
            ),
            PointerRole(
                role=RoleType.HIGH_BOUNDARY,
                name="high",
                initial_position="n - 1",
                direction="decrement",
                represents="Lower exclusive bound of region 2 (elements > pivot)",
                invariants_maintained="A[high+1..n-1] contains only elements > pivot"
            )
        ]

    def get_invariant(self, params: Dict[str, Any]) -> FormalInvariant:
        return InvariantEngine.construct_invariant("partition_dutch_flag", params)

    def derive_movement(self, params: Dict[str, Any]) -> MovementDerivation:
        return MovementDerivationEngine.derive("partition_dutch_flag", params)

    def simulate_step_by_step(self, arr: List[int], params: Dict[str, Any]) -> Dict[str, Any]:
        mut_arr = list(arr)
        n = len(mut_arr)
        low = 0
        mid = 0
        high = n - 1
        steps = []

        while mid <= high:
            val = mut_arr[mid]
            step_info = {"low": low, "mid": mid, "high": high, "val": val}
            if val == 0:
                mut_arr[low], mut_arr[mid] = mut_arr[mid], mut_arr[low]
                step_info["action"] = "SWAP_LOW_MID"
                step_info["reason"] = "Element 0 belongs in region 0. Swap to low; increment low and mid."
                low += 1
                mid += 1
            elif val == 1:
                step_info["action"] = "ADVANCE_MID"
                step_info["reason"] = "Element 1 belongs in region 1. mid advances without swap."
                mid += 1
            else: # val == 2
                mut_arr[mid], mut_arr[high] = mut_arr[high], mut_arr[mid]
                step_info["action"] = "SWAP_MID_HIGH"
                step_info["reason"] = "Element 2 belongs in region 2. Swap to high; decrement high. Do NOT advance mid (swapped value uninspected)."
                high -= 1
            steps.append(step_info)

        return {
            "partitioned_array": mut_arr,
            "steps": steps,
            "termination_reason": "UNINSPECTED_REGION_EXHAUSTED"
        }
