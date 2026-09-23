"""
Step-by-Step Simulation and Tracing Engine.

Executes pointer algorithms in-memory, asserting invariant validity at every step.
"""

from typing import Dict, Any, List
from pointer_algorithms.patterns.converging import ConvergingPairSumPattern, ContainerMostWaterPattern
from pointer_algorithms.patterns.same_direction import SameDirectionCompactionPattern
from pointer_algorithms.patterns.sliding_window import (
    SlidingWindowFixedPattern,
    SlidingWindowVariableMaxPattern,
    SlidingWindowVariableMinPattern
)
from pointer_algorithms.partition.partition import DutchNationalFlagPattern
from pointer_algorithms.fast_slow.fast_slow import FastSlowCyclePattern

class PointerSimulator:
    """Executes trace simulation for any recognized pattern."""

    PATTERNS = {
        "pair_sum_sorted": ConvergingPairSumPattern(),
        "container_most_water": ContainerMostWaterPattern(),
        "remove_duplicates_sorted": SameDirectionCompactionPattern(),
        "sliding_window_fixed": SlidingWindowFixedPattern(),
        "sliding_window_variable_max": SlidingWindowVariableMaxPattern(),
        "sliding_window_variable_min": SlidingWindowVariableMinPattern(),
        "partition_dutch_flag": DutchNationalFlagPattern(),
        "linked_cycle_detection": FastSlowCyclePattern()
    }

    @classmethod
    def simulate(cls, pattern: str, data: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        pat_impl = cls.PATTERNS.get(pattern)
        if not pat_impl:
            raise ValueError(f"Unknown pattern for simulation: {pattern}")
        return pat_impl.simulate_step_by_step(data, params)
