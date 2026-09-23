"""
Fast/Slow Pointers on Linked Structures (Cycle Detection & Middle Node).
"""

from typing import Dict, Any, List, Optional
from pointer_algorithms.patterns.base import BasePointerPattern
from pointer_algorithms.knowledge.pointer_roles import PointerRole, RoleType
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine, FormalInvariant
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine, MovementDerivation

class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next

class FastSlowCyclePattern(BasePointerPattern):
    @property
    def pattern_name(self) -> str:
        return "linked_cycle_detection"

    @property
    def family_name(self) -> str:
        return "fast_slow_pointers"

    def get_pointer_roles(self) -> List[PointerRole]:
        return [
            PointerRole(
                role=RoleType.TORTOISE,
                name="slow",
                initial_position="head",
                direction="step_1",
                represents="Slow pointer advancing 1 node per iteration",
                invariants_maintained="At iteration t, slow is at node (t)"
            ),
            PointerRole(
                role=RoleType.HARE,
                name="fast",
                initial_position="head",
                direction="step_2",
                represents="Fast pointer advancing 2 nodes per iteration",
                invariants_maintained="At iteration t, fast is at node (2t)"
            )
        ]

    def get_invariant(self, params: Dict[str, Any]) -> FormalInvariant:
        return InvariantEngine.construct_invariant("linked_cycle_detection", params)

    def derive_movement(self, params: Dict[str, Any]) -> MovementDerivation:
        return MovementDerivationEngine.derive("linked_cycle_detection", params)

    def simulate_step_by_step(self, head: Optional[ListNode], params: Dict[str, Any]) -> Dict[str, Any]:
        if not head or not head.next:
            return {"has_cycle": False, "steps": []}

        slow = head
        fast = head
        steps = []
        step_idx = 0

        while fast and fast.next:
            step_idx += 1
            slow = slow.next
            fast = fast.next.next

            steps.append({
                "step": step_idx,
                "slow_val": slow.val if slow else None,
                "fast_val": fast.val if fast else None,
                "collision": slow is fast
            })

            if slow is fast:
                return {"has_cycle": True, "steps": steps, "collision_step": step_idx}

        return {"has_cycle": False, "steps": steps}
