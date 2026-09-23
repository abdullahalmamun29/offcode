"""
Phase 9 — stl_header_registry.py

Standard Library Symbol and Header Registry.
Used by MISSING_HEADER diagnosis to deterministically determine which
standard header is required by an unresolved standard symbol in the AST.
"""

from __future__ import annotations

from typing import Dict, Optional

# Mapping from qualified identifier to required standard C++ include header
STL_HEADER_REGISTRY: Dict[str, str] = {
    # <numeric>
    "std::accumulate": "<numeric>",
    "std::iota": "<numeric>",
    "std::partial_sum": "<numeric>",
    "std::adjacent_difference": "<numeric>",
    "std::inner_product": "<numeric>",
    "std::reduce": "<numeric>",
    "std::gcd": "<numeric>",
    "std::lcm": "<numeric>",
    "accumulate": "<numeric>",
    "iota": "<numeric>",

    # <algorithm>
    "std::max": "<algorithm>",
    "std::min": "<algorithm>",
    "std::sort": "<algorithm>",
    "std::stable_sort": "<algorithm>",
    "std::lower_bound": "<algorithm>",
    "std::upper_bound": "<algorithm>",
    "std::binary_search": "<algorithm>",
    "std::reverse": "<algorithm>",
    "std::fill": "<algorithm>",
    "std::max_element": "<algorithm>",
    "std::min_element": "<algorithm>",
    "std::unique": "<algorithm>",
    "std::clamp": "<algorithm>",
    "std::next_permutation": "<algorithm>",
    "std::prev_permutation": "<algorithm>",
    "max": "<algorithm>",
    "min": "<algorithm>",
    "sort": "<algorithm>",

    # <climits>
    "INT_MAX": "<climits>",
    "INT_MIN": "<climits>",
    "LLONG_MAX": "<climits>",
    "LLONG_MIN": "<climits>",

    # <cmath>
    "std::sqrt": "<cmath>",
    "std::abs": "<cmath>",
    "std::pow": "<cmath>",
    "std::ceil": "<cmath>",
    "std::floor": "<cmath>",
    "std::round": "<cmath>",
    "sqrt": "<cmath>",
    "pow": "<cmath>",

    # <queue>
    "std::priority_queue": "<queue>",
    "std::queue": "<queue>",
    "priority_queue": "<queue>",
    "queue": "<queue>",

    # <stack>
    "std::stack": "<stack>",
    "stack": "<stack>",

    # <vector>
    "std::vector": "<vector>",
    "vector": "<vector>",

    # <map>
    "std::map": "<map>",
    "map": "<map>",

    # <set>
    "std::set": "<set>",
    "std::multiset": "<set>",
    "set": "<set>",
    "multiset": "<set>",

    # <iostream>
    "std::cin": "<iostream>",
    "std::cout": "<iostream>",
    "std::cerr": "<iostream>",
    "cin": "<iostream>",
    "cout": "<iostream>",
}


def lookup_header_for_symbol(symbol: str) -> Optional[str]:
    """Look up required header for a symbol or standard identifier."""
    return STL_HEADER_REGISTRY.get(symbol)
