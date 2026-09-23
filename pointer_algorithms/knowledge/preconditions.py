"""
Explicit Preconditions for Pointer-Based Algorithms.

A candidate strategy is rejected if its required structural properties do not hold.
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class PreconditionType(str, Enum):
    SORTED_ORDER = "sorted_order"
    SORTING_PERMISSIBLE = "sorting_permissible"
    MONOTONIC_SEARCH_SPACE = "monotonic_search_space"
    CONTIGUOUS_SUBARRAY = "contiguous_subarray"
    NON_NEGATIVE_INCREMENTAL = "non_negative_incremental"
    INCREMENTAL_WINDOW_VALIDITY = "incremental_window_validity"
    IN_PLACE_MODIFICATION_ALLOWED = "in_place_modification_allowed"
    RELATIVE_SPEED_PROGRESSION = "relative_speed_progression"
    INDEX_PRESERVATION_NOT_REQUIRED_OR_TRACKABLE = "index_preservation_not_required_or_trackable"

@dataclass
class PreconditionRule:
    rule_type: PreconditionType
    description: str
    failure_message: str
    rejection_code: str
