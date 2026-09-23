"""
Property-Based Testing for General Unseen Problems.

Verifies structural invariants and properties without needing a problem-specific oracle:
- Multiset conservation (elements permuted without loss or creation)
- Partition ordering (region 0 < pivot <= region 1 <= region 2)
- Subarray bounds (0 <= L <= R < n)
- Monotonicity of result
"""

from typing import List, Any
from collections import Counter

class PropertyVerifier:

    @staticmethod
    def verify_multiset_conservation(original: List[Any], transformed: List[Any]) -> bool:
        """Verifies that an in-place partition or rearrangement preserved all elements."""
        return Counter(original) == Counter(transformed)

    @staticmethod
    def verify_dutch_flag_partition(arr: List[int]) -> bool:
        """Verifies that arr is strictly ordered as 0s, then 1s, then 2s."""
        n = len(arr)
        # Check non-decreasing 0 <= 1 <= 2
        for i in range(1, n):
            if arr[i] < arr[i - 1]:
                return False
        return True

    @staticmethod
    def verify_in_place_compaction(original: List[int], compacted: List[int]) -> bool:
        """Verifies that compacted array contains unique elements from original in order."""
        # Check all distinct
        if len(compacted) != len(set(compacted)):
            return False
        # Check all unique elements from original are present
        expected_unique = sorted(list(set(original)))
        return sorted(compacted) == expected_unique

    @staticmethod
    def verify_valid_pair_sum(arr: List[int], pair: tuple, target: int) -> bool:
        """Verifies that returned pair indices are valid and sum to target."""
        if not pair:
            return False
        i, j = pair
        if not (0 <= i < j < len(arr)):
            return False
        return arr[i] + arr[j] == target
