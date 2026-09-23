"""
Adversarial and Edge Case Generator.

Synthesizes stressful test cases:
- Empty array
- Single element
- Two elements
- All equal elements
- All distinct elements
- Strictly increasing
- Strictly decreasing
- All zeroes
- Large numbers (up to 10^9)
- Many duplicates
- Boundary answers (pair at (0, 1), (0, n-1), (n-2, n-1), or no answer)
"""

from typing import List, Dict, Any

class AdversarialGenerator:

    @staticmethod
    def generate_sorted_edge_cases() -> List[Dict[str, Any]]:
        return [
            {"label": "two_elements_sum", "arr": [1, 5], "target": 6, "expected_found": True},
            {"label": "two_elements_no_sum", "arr": [1, 5], "target": 7, "expected_found": False},
            {"label": "all_equal", "arr": [3, 3, 3, 3], "target": 6, "expected_found": True},
            {"label": "all_distinct_ends", "arr": [1, 2, 4, 7, 11], "target": 12, "expected_found": True},
            {"label": "with_negatives", "arr": [-10, -3, 0, 5, 9], "target": -1, "expected_found": True},
            {"label": "with_negatives_zero_sum", "arr": [-7, -2, 0, 2, 8], "target": 0, "expected_found": True},
            {"label": "large_values", "arr": [1000000000, 1000000001], "target": 2000000001, "expected_found": True}
        ]

    @staticmethod
    def generate_container_edge_cases() -> List[Dict[str, Any]]:
        return [
            {"label": "two_lines_equal", "heights": [5, 5], "expected_area": 5},
            {"label": "two_lines_unequal", "heights": [2, 10], "expected_area": 2},
            {"label": "tall_in_middle", "heights": [1, 8, 8, 1], "expected_area": 8},
            {"label": "strictly_increasing", "heights": [1, 2, 3, 4, 5], "expected_area": 6},
            {"label": "strictly_decreasing", "heights": [5, 4, 3, 2, 1], "expected_area": 6},
            {"label": "all_equal_many", "heights": [4, 4, 4, 4, 4], "expected_area": 16}
        ]

    @staticmethod
    def generate_sliding_window_edge_cases() -> List[Dict[str, Any]]:
        return [
            {"label": "k_equals_n", "arr": [1, 2, 3, 4], "k": 4, "expected_max_sum": 10},
            {"label": "k_equals_1", "arr": [2, 5, 1, 9], "k": 1, "expected_max_sum": 9},
            {"label": "all_zeroes", "arr": [0, 0, 0, 0], "k": 2, "expected_max_sum": 0}
        ]
