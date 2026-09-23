"""
CHUP Phase 5 — Aggregate Ontology & Decomposed Query Semantics.

Captures precise operation semantics (algebraic structure, identity,
idempotence, invertibility, lazy tag distribution, order statistics)
rather than relying on a coarse ASSOCIATIVE flag alone. Decomposes queries
into target, aggregate, output, and dependency facets.
"""

from enum import Enum, auto
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass(frozen=True)
class AggregateSpec:
    """
    Formal algebraic and operational specification of an aggregate operation.
    """
    operation_name: str                  # "SUM", "MIN", "MAX", "GCD", "XOR", "COUNT", "DISTINCT", "KTH", "MAX_SUBARRAY"
    identity_element: Any                # 0 for SUM/XOR, +inf for MIN, -inf for MAX, 0 for GCD
    is_associative: bool                 # (a * b) * c == a * (b * c)
    is_commutative: bool                 # a * b == b * a
    is_idempotent: bool                  # a * a == a (enables O(1) Sparse Table overlapping queries)
    is_invertible: bool                  # exists inverse a^-1 (enables O(log N) prefix difference in BIT)
    supports_merge: bool                 # disjoint range summaries can be merged in O(1)
    supports_lazy_update: bool           # tag composition distributes over aggregate
    supports_order_statistics: bool      # elements can be ranked or retrieved by quantile/k-th index
    inverse_operation: Optional[str] = None
    description: str = ""

    @classmethod
    def sum_group(cls) -> "AggregateSpec":
        return cls(
            operation_name="SUM",
            identity_element=0,
            is_associative=True,
            is_commutative=True,
            is_idempotent=False,
            is_invertible=True,
            supports_merge=True,
            supports_lazy_update=True,
            supports_order_statistics=False,
            inverse_operation="SUBTRACTION",
            description="Addition abelian group with subtraction inverse"
        )

    @classmethod
    def min_semigroup(cls) -> "AggregateSpec":
        return cls(
            operation_name="MIN",
            identity_element=float("inf"),
            is_associative=True,
            is_commutative=True,
            is_idempotent=True,
            is_invertible=False,
            supports_merge=True,
            supports_lazy_update=True,
            supports_order_statistics=False,
            description="Minimum semilattice with idempotent meet"
        )

    @classmethod
    def max_semigroup(cls) -> "AggregateSpec":
        return cls(
            operation_name="MAX",
            identity_element=float("-inf"),
            is_associative=True,
            is_commutative=True,
            is_idempotent=True,
            is_invertible=False,
            supports_merge=True,
            supports_lazy_update=True,
            supports_order_statistics=False,
            description="Maximum semilattice with idempotent join"
        )

    @classmethod
    def gcd_monoid(cls) -> "AggregateSpec":
        return cls(
            operation_name="GCD",
            identity_element=0,
            is_associative=True,
            is_commutative=True,
            is_idempotent=True,
            is_invertible=False,
            supports_merge=True,
            supports_lazy_update=False,
            supports_order_statistics=False,
            description="Greatest Common Divisor monoid"
        )

    @classmethod
    def xor_group(cls) -> "AggregateSpec":
        return cls(
            operation_name="XOR",
            identity_element=0,
            is_associative=True,
            is_commutative=True,
            is_idempotent=False,
            is_invertible=True,
            supports_merge=True,
            supports_lazy_update=True,
            supports_order_statistics=False,
            inverse_operation="XOR",
            description="Bitwise XOR group with self-inverse"
        )

    @classmethod
    def kth_order_statistic(cls) -> "AggregateSpec":
        return cls(
            operation_name="KTH",
            identity_element=None,
            is_associative=False,
            is_commutative=False,
            is_idempotent=False,
            is_invertible=False,
            supports_merge=True,
            supports_lazy_update=False,
            supports_order_statistics=True,
            description="K-th order statistic selection query"
        )

    @classmethod
    def max_subarray_monoid(cls) -> "AggregateSpec":
        return cls(
            operation_name="MAX_SUBARRAY",
            identity_element=None,
            is_associative=True,
            is_commutative=False,
            is_idempotent=False,
            is_invertible=False,
            supports_merge=True,
            supports_lazy_update=True,
            supports_order_statistics=False,
            description="Maximum contiguous subarray sum with prefix/suffix/total metadata merge"
        )

    @classmethod
    def distinct_count(cls) -> "AggregateSpec":
        return cls(
            operation_name="DISTINCT",
            identity_element=0,
            is_associative=True,
            is_commutative=True,
            is_idempotent=True,
            is_invertible=False,
            supports_merge=False,   # Disjoint distinct counts cannot be merged in O(1) without bitsets/sets
            supports_lazy_update=False,
            supports_order_statistics=False,
            description="Distinct element counting over interval"
        )


class QueryTarget(Enum):
    POINT = "POINT"
    LINEAR_RANGE = "LINEAR_RANGE"
    TREE_PATH = "TREE_PATH"
    TREE_SUBTREE = "TREE_SUBTREE"
    ALL_PAIRS = "ALL_PAIRS"


class QueryOutput(Enum):
    SCALAR_VALUE = "SCALAR_VALUE"
    FREQUENCY_COUNT = "FREQUENCY_COUNT"
    EXISTENCE_BOOLEAN = "EXISTENCE_BOOLEAN"
    PATH_SEQUENCE = "PATH_SEQUENCE"
    VERSION_SNAPSHOT = "VERSION_SNAPSHOT"


class QueryDependency(Enum):
    INDEPENDENT = "INDEPENDENT"
    PREFIX_DEPENDENT = "PREFIX_DEPENDENT"
    STATE_DEPENDENT = "STATE_DEPENDENT"


@dataclass(frozen=True)
class QuerySpec:
    """
    Decomposed query specification.
    """
    target: QueryTarget = QueryTarget.LINEAR_RANGE
    aggregate: AggregateSpec = field(default_factory=AggregateSpec.sum_group)
    output: QueryOutput = QueryOutput.SCALAR_VALUE
    dependency: QueryDependency = QueryDependency.INDEPENDENT
    requires_historical_versions: bool = False
    requires_order_statistics: bool = False

    def is_tree_path(self) -> bool:
        return self.target == QueryTarget.TREE_PATH

    def is_tree_subtree(self) -> bool:
        return self.target == QueryTarget.TREE_SUBTREE

    def is_range_query(self) -> bool:
        return self.target in (QueryTarget.LINEAR_RANGE, QueryTarget.TREE_PATH, QueryTarget.TREE_SUBTREE)
