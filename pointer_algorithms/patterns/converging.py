"""
Converging (Opposite Direction) Pointers Pattern.

Includes:
- Pair sum in sorted array (with value or index output)
- Container with most water (area maximization)
- Palindrome verification
"""

from typing import Dict, Any, List, Optional
from pointer_algorithms.patterns.base import BasePointerPattern
from pointer_algorithms.knowledge.pointer_roles import PointerRole, RoleType
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine, FormalInvariant
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine, MovementDerivation

class ConvergingPairSumPattern(BasePointerPattern):
    @property
    def pattern_name(self) -> str:
        return "pair_sum_sorted"

    @property
    def family_name(self) -> str:
        return "two_pointers_converging"

    def get_pointer_roles(self) -> List[PointerRole]:
        return [
            PointerRole(
                role=RoleType.LEFT_BOUND,
                name="L",
                initial_position="0",
                direction="increment",
                represents="Lower boundary pointing to candidate smaller element",
                invariants_maintained="All elements prior to L cannot pair with any remaining candidate"
            ),
            PointerRole(
                role=RoleType.RIGHT_BOUND,
                name="R",
                initial_position="n - 1",
                direction="decrement",
                represents="Upper boundary pointing to candidate larger element",
                invariants_maintained="All elements after R cannot pair with any remaining candidate"
            )
        ]

    def get_invariant(self, params: Dict[str, Any]) -> FormalInvariant:
        return InvariantEngine.construct_invariant("pair_sum_sorted", params)

    def derive_movement(self, params: Dict[str, Any]) -> MovementDerivation:
        return MovementDerivationEngine.derive("pair_sum_sorted", params)

    def simulate_step_by_step(self, arr: List[int], params: Dict[str, Any]) -> Dict[str, Any]:
        target = params.get("target", 0)
        n = len(arr)
        L = 0
        R = n - 1
        steps = []
        found_pair = None

        while L < R:
            s = arr[L] + arr[R]
            step_info = {
                "L": L, "R": R, "val_L": arr[L], "val_R": arr[R],
                "current_sum": s, "target": target
            }
            if s == target:
                found_pair = (L, R)
                step_info["action"] = "FOUND_PAIR"
                steps.append(step_info)
                break
            elif s < target:
                step_info["action"] = "L_INCREMENT"
                step_info["reason"] = f"sum {s} < {target}; because array is sorted, any pair (L, k) with k < {R} has sum <= {s} < {target}. L is eliminated."
                steps.append(step_info)
                L += 1
            else:
                step_info["action"] = "R_DECREMENT"
                step_info["reason"] = f"sum {s} > {target}; because array is sorted, any pair (k, R) with k > {L} has sum >= {s} > {target}. R is eliminated."
                steps.append(step_info)
                R -= 1

        return {
            "success": found_pair is not None,
            "result": found_pair,
            "steps": steps,
            "termination_reason": "MATCH_FOUND" if found_pair else "SEARCH_SPACE_EXHAUSTED"
        }


class ContainerMostWaterPattern(BasePointerPattern):
    @property
    def pattern_name(self) -> str:
        return "container_most_water"

    @property
    def family_name(self) -> str:
        return "two_pointers_converging"

    def get_pointer_roles(self) -> List[PointerRole]:
        return [
            PointerRole(
                role=RoleType.LEFT_BOUND,
                name="L",
                initial_position="0",
                direction="increment",
                represents="Left boundary wall of container",
                invariants_maintained="Maximum area involving lines < L has already been captured"
            ),
            PointerRole(
                role=RoleType.RIGHT_BOUND,
                name="R",
                initial_position="n - 1",
                direction="decrement",
                represents="Right boundary wall of container",
                invariants_maintained="Maximum area involving lines > R has already been captured"
            )
        ]

    def get_invariant(self, params: Dict[str, Any]) -> FormalInvariant:
        return InvariantEngine.construct_invariant("container_most_water", params)

    def derive_movement(self, params: Dict[str, Any]) -> MovementDerivation:
        return MovementDerivationEngine.derive("container_most_water", params)

    def simulate_step_by_step(self, heights: List[int], params: Dict[str, Any]) -> Dict[str, Any]:
        n = len(heights)
        L = 0
        R = n - 1
        max_area = 0
        best_pair = (0, 0)
        steps = []

        while L < R:
            w = R - L
            h = min(heights[L], heights[R])
            area = w * h
            if area > max_area:
                max_area = area
                best_pair = (L, R)

            step_info = {
                "L": L, "R": R, "h_L": heights[L], "h_R": heights[R],
                "width": w, "area": area, "max_area_so_far": max_area
            }

            if heights[L] <= heights[R]:
                step_info["action"] = "L_INCREMENT"
                step_info["reason"] = f"h[L]={heights[L]} <= h[R]={heights[R]}. Any inner line k < {R} yields min(h[L], h[k])*(k-L) <= h[L]*(k-L) < {area}. L cannot beat {area}."
                steps.append(step_info)
                L += 1
            else:
                step_info["action"] = "R_DECREMENT"
                step_info["reason"] = f"h[R]={heights[R]} < h[L]={heights[L]}. Any inner line k > {L} yields min(h[k], h[R])*(R-k) <= h[R]*(R-k) < {area}. R cannot beat {area}."
                steps.append(step_info)
                R -= 1

        return {
            "success": True,
            "max_area": max_area,
            "best_pair": best_pair,
            "steps": steps,
            "termination_reason": "ALL_INTERVALS_EVALUATED"
        }
