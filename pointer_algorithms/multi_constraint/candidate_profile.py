"""
CHUP Phase 5 — Unified Candidate Profile & Capability Contract.

Encodes the capability footprint, requirements, produced states, and
symbolic asymptotic bounds of all algorithmic candidate components.
"""

from typing import Dict, Any, List, Optional, FrozenSet, Callable
from dataclasses import dataclass, field
from pointer_algorithms.multi_constraint.constraint_lattice import (
    TemporalMode,
    MutabilityCapability,
    MutabilitySet,
)
from pointer_algorithms.multi_constraint.aggregate_ontology import (
    QueryTarget,
    AggregateSpec,
)


@dataclass(frozen=True)
class SymbolicComplexity:
    """
    Symbolic resource complexity model.
    """
    time_op_formula: str         # e.g. "log(N)", "1", "sqrt(N)"
    total_time_formula: str      # e.g. "Q * log(N)", "(N + Q) * sqrt(N)"
    space_bytes_formula: str     # e.g. "4 * N", "4 * N * log(N)"
    space_complexity_class: str  # "O(1)", "O(N)", "O(N log N)", "O(N sqrt N)", "O(N^2)"

    # Function pointers for numeric evaluation given concrete bounds (N, Q, V, E, C)
    estimate_ops: Callable[[int, int, int, int, int], int] = field(default=lambda n, q, v, e, c: 0)
    estimate_bytes: Callable[[int, int, int, int, int], int] = field(default=lambda n, q, v, e, c: 0)


@dataclass(frozen=True)
class CandidateProfile:
    """
    Unified candidate component capability profile.
    Contains explicit requires and produces contracts for capability-DAG synthesis.
    """
    candidate_id: str
    family: str
    display_name: str
    supported_temporals: FrozenSet[TemporalMode]
    supported_mutability: MutabilitySet
    supported_query_targets: FrozenSet[QueryTarget]
    supported_aggregate_names: FrozenSet[str]    # e.g. {"SUM", "MIN", "MAX", ...} or {"*"}
    requires_idempotence: bool = False
    requires_invertibility: bool = False
    requires_order_statistics: bool = False
    requires_capabilities: FrozenSet[str] = field(default_factory=frozenset)
    produces_capabilities: FrozenSet[str] = field(default_factory=frozenset)
    preconditions: FrozenSet[str] = field(default_factory=frozenset)
    forbidden_properties: FrozenSet[str] = field(default_factory=frozenset)
    complexity: SymbolicComplexity = field(
        default_factory=lambda: SymbolicComplexity("1", "Q", "N", "O(N)")
    )
    description: str = ""

    def supports_temporal(self, mode: TemporalMode) -> bool:
        if mode == TemporalMode.ANY or TemporalMode.ANY in self.supported_temporals:
            return True
        return mode in self.supported_temporals

    def supports_mutability(self, required: MutabilityCapability) -> bool:
        return self.supported_mutability.satisfies(required)

    def supports_target(self, target: QueryTarget) -> bool:
        return target in self.supported_query_targets

    def supports_aggregate(self, agg: AggregateSpec) -> bool:
        if "*" in self.supported_aggregate_names:
            pass
        elif agg.operation_name not in self.supported_aggregate_names:
            return False

        if self.requires_idempotence and not agg.is_idempotent:
            return False
        if self.requires_invertibility and not agg.is_invertible:
            return False
        if self.requires_order_statistics and not agg.supports_order_statistics:
            return False
        return True
