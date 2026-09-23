"""
Pointer Roles representation.

Explicit, semantic roles for pointers across all pattern families.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional

class RoleType(str, Enum):
    # Converging
    LEFT_BOUND = "left_bound"
    RIGHT_BOUND = "right_bound"

    # Same Direction
    SLOW_WRITE = "slow_write"
    FAST_READ = "fast_read"
    PREV_POINTER = "prev_pointer"
    CURR_POINTER = "curr_pointer"
    MERGE_PTR_A = "merge_ptr_a"
    MERGE_PTR_B = "merge_ptr_b"

    # Sliding Window
    WINDOW_START = "window_start"
    WINDOW_END = "window_end"

    # Partition
    LOW_BOUNDARY = "low_boundary"
    MID_SCANNER = "mid_scanner"
    HIGH_BOUNDARY = "high_boundary"

    # Linked structures
    TORTOISE = "tortoise"
    HARE = "hare"

@dataclass
class PointerRole:
    role: RoleType
    name: str
    initial_position: str
    direction: str  # 'increment', 'decrement', 'conditional', 'step_2'
    represents: str
    invariants_maintained: str
