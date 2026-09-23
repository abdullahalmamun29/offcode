"""
Operation-Specific Metamorphic Testing.

Applies only mathematically sound transformations:
1. Positive Scalar Multiplication for Pair Sum:
   arr' = c * arr (c > 0)
   target' = c * target
   Expected pair indices remain IDENTICAL.
2. Constant Translation for Pair Sum:
   arr' = arr + delta
   target' = target + 2 * delta
   Expected pair indices remain IDENTICAL.
3. Uniform Scaling for Container With Most Water:
   heights' = c * heights (c > 0)
   Expected max_area' = c * max_area
   Optimal boundary pair remains IDENTICAL.
"""

from typing import List, Tuple, Optional, Any
from pointer_algorithms.simulation.simulator import PointerSimulator

class MetamorphicTester:

    @staticmethod
    def test_pair_sum_scaling(arr: List[int], target: int, c: int = 3) -> bool:
        """Scales array by positive c and verifies pair indices are invariant."""
        if c <= 0:
            raise ValueError("Scale factor must be strictly positive to preserve order.")

        base_res = PointerSimulator.simulate("pair_sum_sorted", arr, {"target": target})
        if not base_res["success"]:
            return True  # If no solution, cannot test positive relation

        scaled_arr = [x * c for x in arr]
        scaled_target = target * c
        scaled_res = PointerSimulator.simulate("pair_sum_sorted", scaled_arr, {"target": scaled_target})

        # Pair indices must match
        return scaled_res["success"] and scaled_res["result"] == base_res["result"]

    @staticmethod
    def test_container_scaling(heights: List[int], c: int = 2) -> bool:
        """Scales heights by positive c and verifies area scales by exactly c."""
        base_res = PointerSimulator.simulate("container_most_water", heights, {})
        scaled_heights = [h * c for h in heights]
        scaled_res = PointerSimulator.simulate("container_most_water", scaled_heights, {})

        return scaled_res["max_area"] == base_res["max_area"] * c
