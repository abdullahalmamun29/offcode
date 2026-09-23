"""
Same-Direction (Fast/Slow, Read/Write, Compaction) Pointers Pattern.

Includes:
- Remove duplicates from sorted array
- In-place compaction / Move zeroes
- Two-pointer merge
"""

from typing import Dict, Any, List
from pointer_algorithms.patterns.base import BasePointerPattern
from pointer_algorithms.knowledge.pointer_roles import PointerRole, RoleType
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine, FormalInvariant
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine, MovementDerivation

class SameDirectionCompactionPattern(BasePointerPattern):
    @property
    def pattern_name(self) -> str:
        return "remove_duplicates_sorted"

    @property
    def family_name(self) -> str:
        return "two_pointers_same_direction"

    def get_pointer_roles(self) -> List[PointerRole]:
        return [
            PointerRole(
                role=RoleType.SLOW_WRITE,
                name="slow_write",
                initial_position="0",
                direction="conditional",
                represents="Tail index of compacted unique prefix",
                invariants_maintained="Prefix [0..slow_write] contains only unique elements in original relative order"
            ),
            PointerRole(
                role=RoleType.FAST_READ,
                name="fast_read",
                initial_position="1",
                direction="increment",
                represents="Head pointer scanning uncompressed input array",
                invariants_maintained="Examines each input element exactly once"
            )
        ]

    def get_invariant(self, params: Dict[str, Any]) -> FormalInvariant:
        return InvariantEngine.construct_invariant("remove_duplicates_sorted", params)

    def derive_movement(self, params: Dict[str, Any]) -> MovementDerivation:
        return MovementDerivationEngine.derive("remove_duplicates_sorted", params)

    def simulate_step_by_step(self, arr: List[int], params: Dict[str, Any]) -> Dict[str, Any]:
        if not arr:
            return {"new_length": 0, "compacted_array": [], "steps": []}

        mut_arr = list(arr)
        slow_write = 0
        steps = []

        for fast_read in range(1, len(mut_arr)):
            step_info = {
                "fast_read": fast_read,
                "slow_write": slow_write,
                "val_fast": mut_arr[fast_read],
                "val_slow": mut_arr[slow_write]
            }
            if mut_arr[fast_read] != mut_arr[slow_write]:
                slow_write += 1
                mut_arr[slow_write] = mut_arr[fast_read]
                step_info["action"] = "WRITE_AND_ADVANCE"
                step_info["reason"] = "Distinct value found. Advance slow_write and commit value."
            else:
                step_info["action"] = "SKIP_DUPLICATE"
                step_info["reason"] = "Duplicate value. Advance fast_read without overwriting."
            steps.append(step_info)

        return {
            "new_length": slow_write + 1,
            "compacted_array": mut_arr[:slow_write + 1],
            "steps": steps
        }
