"""
CHUP Phase 5 — Closed-World Candidate Elimination Engine.

Evaluates candidate profiles against active multi-dimensional constraints.
Emits structured, immutable EliminationCertificates with formal failure codes,
witnesses, and asymptotic arguments. Never conflates candidate elimination
with axiomatic contradiction.
"""

from typing import Dict, Any, List, Optional, Set, FrozenSet
from dataclasses import dataclass, field
from pointer_algorithms.multi_constraint.constraint_lattice import (
    TemporalMode,
    MutabilityCapability,
    MutabilitySet,
    CoordinateScale,
    MultiConstraintVector,
)
from pointer_algorithms.multi_constraint.aggregate_ontology import (
    QuerySpec,
    QueryTarget,
    AggregateSpec,
)
from pointer_algorithms.multi_constraint.candidate_profile import CandidateProfile
from pointer_algorithms.multi_constraint.resource_evaluator import (
    ResourceEvaluator,
    SymbolicBudget,
)


@dataclass(frozen=True)
class EliminationCertificate:
    """
    Immutable, machine-verifiable record of an algorithmic candidate elimination.
    """
    candidate_id: str
    constraint_id: str
    failure_code: str
    expected_capability: str
    observed_constraint: str
    witness: str
    asymptotic_argument: str
    severity: str = "HARD_PRECONDITION_VIOLATION"


@dataclass(frozen=True)
class CandidateAnalysis:
    """
    Complete analysis of candidate survival, elimination certificates, and
    uncovered constraint gaps.
    """
    surviving_candidates: List[CandidateProfile]
    eliminated_candidates: Dict[str, EliminationCertificate]
    uncovered_constraints: List[str]
    ambiguous_constraints: List[str] = field(default_factory=list)

    @property
    def has_single_survivor(self) -> bool:
        return len(self.surviving_candidates) == 1 and not self.uncovered_constraints

    @property
    def is_composition_required(self) -> bool:
        return (len(self.surviving_candidates) == 0 and not self.is_empty_universe) or len(self.uncovered_constraints) > 0

    @property
    def is_empty_universe(self) -> bool:
        return len(self.surviving_candidates) == 0 and len(self.eliminated_candidates) == 0


class EliminationEngine:
    """
    Closed-world candidate elimination engine.
    """

    @classmethod
    def evaluate(
        cls,
        vector: MultiConstraintVector,
        query: QuerySpec,
        budget: SymbolicBudget,
        candidates: Dict[str, CandidateProfile]
    ) -> CandidateAnalysis:
        survivors: List[CandidateProfile] = []
        eliminated: Dict[str, EliminationCertificate] = []
        elim_map: Dict[str, EliminationCertificate] = {}

        for cid, cand in candidates.items():
            cert = cls._test_candidate(cand, vector, query, budget)
            if cert is None:
                survivors.append(cand)
            else:
                elim_map[cid] = cert

        # Analyze uncovered constraints if any survivors exist
        uncovered: List[str] = []
        if query.is_tree_path():
            # If survivors only support linear arrays, tree path is uncovered as a standalone candidate
            if survivors and all(QueryTarget.TREE_PATH not in c.supported_query_targets for c in survivors):
                uncovered.append("TREE_PATH_QUERY_UNCOVERED")

        if vector.coordinate_scale == CoordinateScale.MASSIVE:
            if survivors and all("DYNAMIC_COORDINATE_INDEXING" not in c.produces_capabilities for c in survivors):
                uncovered.append("MASSIVE_COORDINATE_SPACE_UNCOVERED")

        return CandidateAnalysis(
            surviving_candidates=survivors,
            eliminated_candidates=elim_map,
            uncovered_constraints=uncovered
        )

    @classmethod
    def verify_and_eliminate(
        cls,
        cand: CandidateProfile,
        vector: MultiConstraintVector,
        query: QuerySpec,
        budget: SymbolicBudget
    ) -> Optional[EliminationCertificate]:
        """Tests a single candidate against vector, query, and budget, returning an EliminationCertificate if rejected."""
        return cls._test_candidate(cand, vector, query, budget)

    @classmethod
    def test_candidate(
        cls,
        cand: CandidateProfile,
        vector: MultiConstraintVector,
        query: QuerySpec,
        budget: SymbolicBudget
    ) -> Optional[EliminationCertificate]:
        return cls._test_candidate(cand, vector, query, budget)

    @classmethod
    def _test_candidate(
        cls,
        cand: CandidateProfile,
        vector: MultiConstraintVector,
        query: QuerySpec,
        budget: SymbolicBudget
    ) -> Optional[EliminationCertificate]:
        # 1. Temporal Compatibility
        if vector.temporal != TemporalMode.ANY:
            if not cand.supports_temporal(vector.temporal):
                return EliminationCertificate(
                    candidate_id=cand.candidate_id,
                    constraint_id="TEMPORAL_MODE",
                    failure_code="OFFLINE_MODE_REQUIRED_REJECTS_ONLINE_MOS" if cand.candidate_id == "mos_algorithm_scheduler" else "TEMPORAL_MODE_INCOMPATIBLE",
                    expected_capability=f"Candidate requires temporal modes: {[m.value for m in cand.supported_temporals]}",
                    observed_constraint=f"Problem specifies temporal mode: {vector.temporal.value}",
                    witness=f"Query stream is {vector.temporal.value}",
                    asymptotic_argument="Offline query reordering/sorting cannot be performed on online interactive query streams",
                    severity="TEMPORAL_INCOMPATIBILITY"
                )

        # 2. Domain Preconditions & Forbidden Properties (High Priority Specific Rejections)
        if cand.candidate_id == "dijkstra_priority_queue":
            if vector.has_constraint("NEGATIVE_EDGE_WEIGHTS"):
                return EliminationCertificate(
                    candidate_id=cand.candidate_id,
                    constraint_id="EDGE_WEIGHTS",
                    failure_code="NEGATIVE_WEIGHTS_REJECT_DIJKSTRA",
                    expected_capability="Non-negative edge weights (w >= 0)",
                    observed_constraint="Graph possesses negative edge weights",
                    witness="Negative edge weights present",
                    asymptotic_argument="Greedy frontier expansion in Dijkstra fails when negative edges allow later paths to be strictly shorter than settled distances",
                    severity="HARD_PRECONDITION_VIOLATION"
                )

        if cand.candidate_id == "two_pointers_monotone_window":
            if vector.has_constraint("NEGATIVE_ELEMENTS_FOR_RANGE_SUM"):
                return EliminationCertificate(
                    candidate_id=cand.candidate_id,
                    constraint_id="MONOTONE_WINDOW",
                    failure_code="NON_MONOTONE_WINDOW_REJECTS_TWO_POINTERS",
                    expected_capability="Monotonically non-decreasing prefix sums (all elements >= 0)",
                    observed_constraint="Negative elements allow window sum to decrease when expanding",
                    witness="Negative elements present in sequence",
                    asymptotic_argument="Two Pointers sliding window requires that expanding the right pointer monotonically increases window sum; negative elements break two-pointer contract",
                    severity="HARD_PRECONDITION_VIOLATION"
                )

        if cand.candidate_id == "binary_search_bisection":
            if vector.has_constraint("NON_MONOTONE_PREDICATE"):
                return EliminationCertificate(
                    candidate_id=cand.candidate_id,
                    constraint_id="PREDICATE_MONOTONICITY",
                    failure_code="NON_MONOTONE_PREDICATE_REJECTS_BISECTION",
                    expected_capability="Monotone boolean decision cut P(x)",
                    observed_constraint="Decision predicate oscillates non-monotonically",
                    witness="Decision predicate is not monotone",
                    asymptotic_argument="Binary search bisection requires predicate order-preservation; non-monotone predicates cannot eliminate half the search interval",
                    severity="HARD_PRECONDITION_VIOLATION"
                )

        if cand.candidate_id == "monotonic_deque_sliding_window":
            if vector.has_constraint("NON_CONVEX_TRANSITION"):
                return EliminationCertificate(
                    candidate_id=cand.candidate_id,
                    constraint_id="COST_CONVEXITY",
                    failure_code="NON_CONVEX_COST_REJECTS_MONOTONIC_DEQUE",
                    expected_capability="Cost function satisfies slope dominance / convexity",
                    observed_constraint="Transition cost violates quadrangle inequality / convexity",
                    witness="Non-convex transition cost",
                    asymptotic_argument="Monotonic deque candidate dominance requires that suboptimal elements can never become optimal later; non-convex costs violate dominance",
                    severity="HARD_PRECONDITION_VIOLATION"
                )

        if cand.candidate_id == "dynamic_segment_tree":
            if vector.has_constraint("DYNAMIC_POINTERS_FORBIDDEN"):
                return EliminationCertificate(
                    candidate_id=cand.candidate_id,
                    constraint_id="DYNAMIC_POINTERS",
                    failure_code="DYNAMIC_POINTER_ALLOCATION_FORBIDDEN",
                    expected_capability="Flat array memory layout without pointer chasing",
                    observed_constraint="Dynamic pointer allocation forbidden",
                    witness="Dynamic pointer allocation disallowed",
                    asymptotic_argument="Dynamic segment tree requires pointer-based node allocation; prohibited by constraint",
                    severity="HARD_PRECONDITION_VIOLATION"
                )

        # 3. Mutability Compatibility
        for cap in (MutabilityCapability.POINT_WRITE, MutabilityCapability.RANGE_WRITE, MutabilityCapability.STRUCTURAL_INSERT, MutabilityCapability.STRUCTURAL_DELETE):
            if vector.mutability.satisfies(cap):
                if not cand.supports_mutability(cap):
                    return EliminationCertificate(
                        candidate_id=cand.candidate_id,
                        constraint_id="MUTABILITY_CAPABILITY",
                        failure_code="MUTATION_DISALLOWED_ON_STATIC_STRUCTURE",
                        expected_capability=f"Candidate mutabilities: {[m.value for m in cand.supported_mutability.capabilities]}",
                        observed_constraint=f"Problem mandates mutation capability: {cap.value}",
                        witness=f"Active mutation capability required: {cap.value}",
                        asymptotic_argument=f"Static/immutable data structure {cand.display_name} cannot support dynamic {cap.value} updates",
                        severity="HARD_PRECONDITION_VIOLATION"
                    )

        # 4. Algebraic Specific Requirements (Idempotence & Invertibility before generic aggregate)
        if cand.requires_idempotence and not query.aggregate.is_idempotent:
            return EliminationCertificate(
                candidate_id=cand.candidate_id,
                constraint_id="ALGEBRAIC_IDEMPOTENCE",
                failure_code="NON_IDEMPOTENT_OPERATION_REJECTS_SPARSE_TABLE",
                expected_capability="Requires idempotent semilattice operation (x * x == x)",
                observed_constraint=f"Operation {query.aggregate.operation_name} is non-idempotent",
                witness=f"Operation: {query.aggregate.operation_name}",
                asymptotic_argument="Sparse Table achieves O(1) query complexity via overlapping power-of-two intervals; non-idempotent operations double-count overlapping elements",
                severity="HARD_PRECONDITION_VIOLATION"
            )

        if cand.requires_invertibility and not query.aggregate.is_invertible:
            return EliminationCertificate(
                candidate_id=cand.candidate_id,
                constraint_id="ALGEBRAIC_INVERTIBILITY",
                failure_code="NON_INVERTIBLE_OPERATION_REJECTS_FENWICK",
                expected_capability="Requires invertible abelian group with subtraction/inverse",
                observed_constraint=f"Operation {query.aggregate.operation_name} lacks inverse",
                witness=f"Operation: {query.aggregate.operation_name}",
                asymptotic_argument="Standard Fenwick tree computes range query [L, R] as prefix(R) - prefix(L-1); non-invertible operations cannot extract subsegments by difference",
                severity="HARD_PRECONDITION_VIOLATION"
            )

        if cand.requires_order_statistics and not query.aggregate.supports_order_statistics:
            if query.aggregate.operation_name not in cand.supported_aggregate_names and "*" not in cand.supported_aggregate_names:
                return EliminationCertificate(
                    candidate_id=cand.candidate_id,
                    constraint_id="ORDER_STATISTICS",
                    failure_code="OPERATION_NOT_ORDER_STATISTIC",
                    expected_capability="Requires order statistic or rank queries",
                    observed_constraint=f"Operation is {query.aggregate.operation_name}",
                    witness=f"Operation: {query.aggregate.operation_name}",
                    asymptotic_argument=f"{cand.display_name} is designed for order statistics / rank queries; incompatible with {query.aggregate.operation_name}",
                    severity="HARD_PRECONDITION_VIOLATION"
                )

        if not cand.supports_aggregate(query.aggregate):
            return EliminationCertificate(
                candidate_id=cand.candidate_id,
                constraint_id="OPERATION_AGGREGATE",
                failure_code="UNSUPPORTED_AGGREGATE_OPERATION",
                expected_capability=f"Candidate supports operations: {list(cand.supported_aggregate_names)}",
                observed_constraint=f"Query specifies operation {query.aggregate.operation_name}",
                witness=f"Operation: {query.aggregate.operation_name}",
                asymptotic_argument=f"{cand.display_name} cannot compute {query.aggregate.operation_name} aggregate",
                severity="HARD_PRECONDITION_VIOLATION"
            )

        # 5. Query Target Compatibility
        if query.target not in cand.supported_query_targets:
            return EliminationCertificate(
                candidate_id=cand.candidate_id,
                constraint_id="QUERY_TARGET",
                failure_code="TARGET_TOPOLOGY_INCOMPATIBLE",
                expected_capability=f"Candidate targets: {[t.value for t in cand.supported_query_targets]}",
                observed_constraint=f"Query target is {query.target.value}",
                witness=f"{cand.display_name} does not support {query.target.value} query target",
                asymptotic_argument=f"Topology/target mismatch: candidate cannot evaluate {query.target.value} queries directly",
                severity="HARD_PRECONDITION_VIOLATION"
            )

        # 6. Range Aggregation Capability Check
        # Structural decomposers (like HLD) cannot answer range aggregations without an attached provider
        if query.is_range_query() and "RANGE_AGGREGATION" not in cand.produces_capabilities:
            return EliminationCertificate(
                candidate_id=cand.candidate_id,
                constraint_id="QUERY_CAPABILITY",
                failure_code="CANNOT_PROVIDE_RANGE_AGGREGATE",
                expected_capability="Produces RANGE_AGGREGATION",
                observed_constraint="Query requires range aggregation answers",
                witness=f"Candidate {cand.candidate_id} is a structural decomposer, not a range query answerer",
                asymptotic_argument="Path decomposition alone cannot compute aggregate values without an attached range query provider",
                severity="HARD_PRECONDITION_VIOLATION"
            )

        # 6. Massive Coordinates Direct Indexing Check
        if vector.coordinate_scale == CoordinateScale.MASSIVE:
            if "MASSIVE_COORDINATES" not in cand.requires_capabilities and "DYNAMIC_COORDINATE_INDEXING" not in cand.produces_capabilities and cand.candidate_id != "coordinate_compressor":
                return EliminationCertificate(
                    candidate_id=cand.candidate_id,
                    constraint_id="COORDINATE_SCALE",
                    failure_code="MASSIVE_COORDINATES_REJECT_FLAT_ARRAY",
                    expected_capability="Compact index space (1..N)",
                    observed_constraint="Coordinate domain up to 10^18",
                    witness="Coordinate values up to 10^18",
                    asymptotic_argument="Flat array-indexed structures cannot allocate 10^18 indices directly; requires dynamic node allocation or coordinate compression",
                    severity="HARD_PRECONDITION_VIOLATION"
                )

        # 7. Resource Feasibility (Symbolic Budget)
        res = ResourceEvaluator.evaluate(cand, budget)
        if not res.is_feasible:
            return EliminationCertificate(
                candidate_id=cand.candidate_id,
                constraint_id="RESOURCE_BOUND",
                failure_code=res.failure_code or "RESOURCE_BUDGET_EXCEEDED",
                expected_capability="Operations and space within budget limits",
                observed_constraint=f"Estimated ops={res.estimated_ops}, bytes={res.estimated_bytes}",
                witness=res.failure_argument,
                asymptotic_argument=res.failure_argument,
                severity="RESOURCE_BUDGET_EXCEEDED"
            )

        return None
