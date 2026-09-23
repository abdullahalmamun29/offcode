"""
CHUP Phase 4: Semantic Ontology, Proof Obligations & Complexity Model.

Core Principles:
1. Proof Graph: DerivedFact instances with explicit dependencies and proof_status.
2. ProofObligationRegistry: Declarative verification of mathematical requirements.
3. OperationAlgebra: Formal algebraic flags (associative, identity, commutative, invertible, idempotent).
4. PredicateContract & DPOptimizationContract: Rigorous contracts for bisection & DP acceleration.
5. Deterministic ComplexityEvaluator: Computes feasibility; UNKNOWN fails closed.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Set, Tuple
import math
from pointer_algorithms.cross_family.component_model import PropertyProofStatus, StateContract


# ── 1. Derived Facts & Proof Graph ──

@dataclass
class DerivedFact:
    """
    Node in the formal mathematical derivation and proof graph.
    """
    fact_id: str
    fact: str
    source: str
    derivation_rule: str
    dependencies: List[str] = field(default_factory=list)
    proof_status: PropertyProofStatus = PropertyProofStatus.PROVEN_PRESENT
    confidence: float = 1.0


# ── 2. Formal Proof Obligations ──

@dataclass
class ProofObligation:
    """
    Mathematical requirement that must be explicitly discharged before composition is admitted.
    """
    identifier: str
    required_facts: List[str]
    derivation_rules: List[str]
    verification_method: str
    failure_code: str


class ProofObligationRegistry:
    """
    Maintains registered mathematical proof obligations and verifies their discharge
    against established facts.
    """
    def __init__(self):
        self.obligations: Dict[str, ProofObligation] = {}
        self._register_default_obligations()

    def register(self, ob: ProofObligation) -> None:
        self.obligations[ob.identifier] = ob

    def get(self, identifier: str) -> Optional[ProofObligation]:
        return self.obligations.get(identifier)

    def is_discharged(self, identifier: str, established_facts: Set[str]) -> Tuple[bool, Optional[str]]:
        """
        Evaluates whether all required facts for an obligation are present in established_facts.
        Returns (is_satisfied, failure_code_if_not).
        """
        ob = self.get(identifier)
        if not ob:
            # Unknown obligation fails closed
            return False, "UNKNOWN_PROOF_OBLIGATION"
        for req in ob.required_facts:
            if req not in established_facts:
                return False, ob.failure_code
        return True, None

    def _register_default_obligations(self) -> None:
        self.register(ProofObligation(
            identifier="NON_NEGATIVE_WEIGHTS",
            required_facts=["FACT_EDGE_WEIGHTS_NON_NEGATIVE"],
            derivation_rules=["INSPECT_EDGE_WEIGHTS_BOUNDS"],
            verification_method="MINIMUM_WEIGHT_GEQ_ZERO",
            failure_code="NEGATIVE_EDGE_WEIGHTS_REJECT_GREEDY_HEAP"
        ))
        self.register(ProofObligation(
            identifier="NO_NEGATIVE_CYCLE",
            required_facts=["FACT_NO_NEGATIVE_CYCLE"],
            derivation_rules=["CYCLE_COST_ANALYSIS"],
            verification_method="BELLMAN_FORD_CHECK",
            failure_code="NEGATIVE_CYCLE_DETECTED"
        ))
        self.register(ProofObligation(
            identifier="ACYCLIC_STRUCTURE",
            required_facts=["FACT_TOPOLOGY_ACYCLIC"],
            derivation_rules=["DFS_CYCLE_DETECTION"],
            verification_method="TOPOLOGICAL_SORT_EXISTS",
            failure_code="REQUIRED_ACYCLICITY_VIOLATED"
        ))
        self.register(ProofObligation(
            identifier="CONNECTIVITY_ASSUMPTION",
            required_facts=["FACT_TOPOLOGY_CONNECTED"],
            derivation_rules=["COMPONENT_COUNT_IS_ONE"],
            verification_method="BFS_REACHES_ALL_VERTICES",
            failure_code="REQUIRED_CONNECTIVITY_VIOLATED"
        ))
        self.register(ProofObligation(
            identifier="MONOTONE_PREDICATE",
            required_facts=["FACT_PREDICATE_MONOTONIC"],
            derivation_rules=["PREDICATE_ORDER_PRESERVATION"],
            verification_method="DECISION_CUT_WITNESS",
            failure_code="PREDICATE_NOT_MONOTONIC"
        ))
        self.register(ProofObligation(
            identifier="CONVEX_TRANSITION",
            required_facts=["FACT_CONVEX_SLOPE_DOMINANCE"],
            derivation_rules=["SLOPE_MONOTONICITY_LEMMA"],
            verification_method="MONOTONIC_QUEUE_DOMINANCE",
            failure_code="NON_CONVEX_COST_REJECTS_MONOTONIC_QUEUE"
        ))
        self.register(ProofObligation(
            identifier="INVERTIBLE_OPERATION",
            required_facts=["FACT_OPERATION_INVERTIBLE"],
            derivation_rules=["ALGEBRAIC_GROUP_INVERSE"],
            verification_method="HAS_INVERSE_ELEMENT",
            failure_code="OPERATION_NOT_INVERTIBLE_REJECTS_PREFIX_DIFFERENCE"
        ))
        self.register(ProofObligation(
            identifier="ASSOCIATIVE_OPERATION",
            required_facts=["FACT_OPERATION_ASSOCIATIVE"],
            derivation_rules=["ALGEBRAIC_SEMIGROUP"],
            verification_method="ASSOCIATIVITY_PROVED",
            failure_code="OPERATION_NOT_ASSOCIATIVE"
        ))
        self.register(ProofObligation(
            identifier="GREEDY_CHOICE_PROPERTY",
            required_facts=["FACT_GREEDY_CHOICE_OPTIMAL"],
            derivation_rules=["EXCHANGE_ARGUMENT"],
            verification_method="MATROID_GREEDY_LEMMA",
            failure_code="GREEDY_CHOICE_NOT_OPTIMAL"
        ))
        self.register(ProofObligation(
            identifier="WEIGHT_COMPARABILITY",
            required_facts=["FACT_WEIGHTS_ARE_COMPARABLE"],
            derivation_rules=["TOTAL_ORDERING_ON_WEIGHTS"],
            verification_method="COMPARE_OPERATOR_EXISTS",
            failure_code="WEIGHTS_NOT_COMPARABLE"
        ))
        self.register(ProofObligation(
            identifier="FRACTIONAL_OBJECTIVE_FORM",
            required_facts=["FACT_FRACTIONAL_OBJECTIVE_RATIO"],
            derivation_rules=["FRACTIONAL_PROGRAMMING_REDUCTION"],
            verification_method="OBJECTIVE_IS_SUM_RATIO",
            failure_code="OBJECTIVE_NOT_FRACTIONAL_RATIO"
        ))
        self.register(ProofObligation(
            identifier="DENOMINATOR_POSITIVITY",
            required_facts=["FACT_DENOMINATOR_STRICTLY_POSITIVE"],
            derivation_rules=["INSPECT_DENOMINATOR_LOWER_BOUND"],
            verification_method="SUM_B_GREATER_THAN_ZERO",
            failure_code="DENOMINATOR_NOT_STRICTLY_POSITIVE"
        ))
        self.register(ProofObligation(
            identifier="PARAMETRIC_RATIO_TRANSFORMATION_VALID",
            required_facts=["FACT_PARAMETRIC_RATIO_TRANSFORMATION_PROVEN"],
            derivation_rules=["PARAMETRIC_BINARY_SEARCH_RATIO_REDUCTION"],
            verification_method="RATIO_INEQUALITY_EQUIVALENCE",
            failure_code="PARAMETRIC_RATIO_TRANSFORMATION_INVALID"
        ))
        self.register(ProofObligation(
            identifier="PARAMETRIC_TRANSFORMATION_VALID",
            required_facts=["FACT_PARAMETRIC_TRANSFORMATION_PROVEN"],
            derivation_rules=["PARAMETRIC_BINARY_SEARCH_RATIO_REDUCTION"],
            verification_method="ROOT_EQUIVALENCE_PROOF",
            failure_code="PARAMETRIC_TRANSFORMATION_INVALID"
        ))
        self.register(ProofObligation(
            identifier="NUMERICAL_PRECISION_BOUND",
            required_facts=["FACT_PRECISION_EPSILON_OR_ITERATIONS_BOUNDED"],
            derivation_rules=["BISECTION_CONVERGENCE_RATE"],
            verification_method="ITERATION_COUNT_LEQ_MAX",
            failure_code="NUMERICAL_PRECISION_UNBOUNDED"
        ))
        self.register(ProofObligation(
            identifier="SLIDING_WINDOW_MONOTONICITY",
            required_facts=["FACT_SLIDING_WINDOW_ORDERED"],
            derivation_rules=["DEQUE_MONOTONIC_VALUE_INVARIANT"],
            verification_method="MONOTONIC_DEQUE_INVARIANT",
            failure_code="SLIDING_WINDOW_ORDER_VIOLATED"
        ))
        self.register(ProofObligation(
            identifier="DOMINANCE_ORDER",
            required_facts=["FACT_DOMINANCE_ORDER_ESTABLISHED"],
            derivation_rules=["DOMINANCE_LEMMA"],
            verification_method="TRANSITIVITY_OF_COMPARISON",
            failure_code="DOMINANCE_ORDER_VIOLATED"
        ))
        self.register(ProofObligation(
            identifier="WINDOW_EXPIRATION",
            required_facts=["FACT_WINDOW_EXPIRATION_MONOTONIC"],
            derivation_rules=["MONOTONE_WINDOW_BOUNDS"],
            verification_method="INDEX_INTERVAL_MONOTONICITY",
            failure_code="WINDOW_EXPIRATION_VIOLATED"
        ))


# ── 3. Algebraic Operation Structure ──

@dataclass
class OperationAlgebra:
    """
    Formal algebraic structure for binary operations.
    """
    name: str
    associative: bool
    identity: bool
    commutative: bool
    invertible: bool
    idempotent: bool

    @classmethod
    def sum_group(cls) -> "OperationAlgebra":
        return cls(name="SUM", associative=True, identity=True, commutative=True, invertible=True, idempotent=False)

    @classmethod
    def min_semigroup(cls) -> "OperationAlgebra":
        return cls(name="MIN", associative=True, identity=False, commutative=True, invertible=False, idempotent=True)

    @classmethod
    def max_semigroup(cls) -> "OperationAlgebra":
        return cls(name="MAX", associative=True, identity=False, commutative=True, invertible=False, idempotent=True)

    @classmethod
    def gcd_monoid(cls) -> "OperationAlgebra":
        return cls(name="GCD", associative=True, identity=True, commutative=True, invertible=False, idempotent=True)

    @classmethod
    def xor_group(cls) -> "OperationAlgebra":
        return cls(name="XOR", associative=True, identity=True, commutative=True, invertible=True, idempotent=False)


# ── 4. Bisection Predicate Contract ──

class PredicateDirection(str, Enum):
    MONOTONE_INCREASING = "MONOTONE_INCREASING"  # False -> True (find first True)
    MONOTONE_DECREASING = "MONOTONE_DECREASING"  # True -> False (find last True)


@dataclass
class PredicateContract:
    """
    Formal contract for an answer-space decision predicate P(x).
    """
    domain: str                                 # e.g., "INTEGER_INTERVAL [1, 10^9]"
    direction: PredicateDirection
    witness_property: str                       # Property proved: e.g. "P(x) implies P(x+1)"
    is_monotonic_proven: bool = False
    proof_certificate: str = ""


# ── 5. DP Optimization Contract ──

class DPOptimizationKind(str, Enum):
    SLIDING_WINDOW_EXTREMA = "SLIDING_WINDOW_EXTREMA"    # Fixed window length, monotone deque
    MONOTONE_QUEUE = "MONOTONE_QUEUE"                    # 1D-1D DP with slope dominance
    CONVEX_HULL_TRICK = "CONVEX_HULL_TRICK"              # Linear functions envelope
    DIVIDE_AND_CONQUER = "DIVIDE_AND_CONQUER"            # Quadrangle inequality on 2D DP
    KNUTH_OPTIMIZATION = "KNUTH_OPTIMIZATION"            # Monotonic split points


@dataclass
class DPOptimizationContract:
    """
    Formal contract governing non-linear DP state transition accelerations.
    """
    kind: DPOptimizationKind
    recurrence_form: str
    transition_domain: str
    dominance_relation: str
    window_constraint: Optional[str] = None
    is_convex_or_monotone_proven: bool = False
    proof_certificate: str = ""


# ── 6. Deterministic Complexity Model & Evaluator ──

class ComplexityVerdict(str, Enum):
    PROVABLY_WITHIN = "PROVABLY_WITHIN"
    PROVABLY_EXCEEDS = "PROVABLY_EXCEEDS"
    UNKNOWN = "UNKNOWN"                          # Fails closed!


@dataclass
class ComplexityModel:
    asymptotic_expression: str                   # e.g. "O(N log N)", "O(V + E log V)", "O(N^2)"
    primary_variable: str = "N"
    variable_scale: int = 100000                 # Expected size of N
    secondary_scale: int = 200000                # Expected size of M/E/Q
    worst_case_constant: float = 2.0


class ComplexityEvaluator:
    """
    Evaluates algorithmic complexity bounds against problem resource limits.
    """
    MAX_OPS_PER_SECOND = 100_000_000             # 10^8 operations per second in standard CP

    @classmethod
    def evaluate(
        cls,
        time_complexity: str,
        n: int,
        m: int = 0,
        time_limit_sec: float = 1.0,
        memory_limit_mb: float = 256.0
    ) -> Tuple[ComplexityVerdict, float, str]:
        """
        Evaluates asymptotic expression with concrete bounds.
        UNKNOWN or ambiguous evaluations fail closed.
        """
        if n <= 0:
            return ComplexityVerdict.UNKNOWN, 0.0, "Input scale N is non-positive or unknown"

        expr = time_complexity.strip()
        ops = 0.0

        if expr in ("O(1)", "O(alpha(N))"):
            ops = 1.0
        elif expr in ("O(log N)", "O(log(N))"):
            ops = math.log2(max(2, n))
        elif expr in ("O(N)", "O(V + E)"):
            ops = float(n + m)
        elif expr in ("O(N log N)", "O(N log(N))", "O(E log V)"):
            ops = float(n if m == 0 else m) * math.log2(max(2, n))
        elif expr in ("O(N sqrt N)", "O(N sqrt(N))"):
            ops = float(n) * math.sqrt(n)
        elif expr in ("O(N^2)", "O(N*N)", "O(V^2)"):
            ops = float(n) * float(n)
        elif expr in ("O(N^3)", "O(V^3)"):
            ops = float(n) ** 3
        else:
            return ComplexityVerdict.UNKNOWN, 0.0, f"Unrecognized asymptotic expression: {time_complexity}"

        max_allowed = cls.MAX_OPS_PER_SECOND * time_limit_sec
        if ops <= max_allowed:
            return ComplexityVerdict.PROVABLY_WITHIN, ops, f"Estimated ops {ops:.1e} <= limit {max_allowed:.1e}"
        else:
            return ComplexityVerdict.PROVABLY_EXCEEDS, ops, f"Estimated ops {ops:.1e} > limit {max_allowed:.1e}"


# ── 7. Canonical Cross-Family Objectives ──

class CrossFamilyObjective(str, Enum):
    CF_KRUSKAL_MST = "CF_KRUSKAL_MST"                                                 # 1. Graph + DSU + Sorting
    CF_DIJKSTRA_SHORTEST_PATH = "CF_DIJKSTRA_SHORTEST_PATH"                           # 2. Graph + Heap Priority Queue
    CF_BOTTLENECK_PATH_BINARY_SEARCH = "CF_BOTTLENECK_PATH_BINARY_SEARCH"             # 3. Graph + Bisection + Reachability
    CF_GRAPH_SEGMENT_TREE_RELAXATION = "CF_GRAPH_SEGMENT_TREE_RELAXATION"             # 4. Graph + Segment Tree Auxiliary Nodes
    CF_TREE_SUBTREE_DP = "CF_TREE_SUBTREE_DP"                                         # 5. Tree + Subtree Recurrence DP
    CF_TREE_PATH_HLD_SEGMENT_TREE = "CF_TREE_PATH_HLD_SEGMENT_TREE"                   # 6. Tree + HLD + Range Provider
    CF_EVENT_SCHEDULING_GREEDY_HEAP = "CF_EVENT_SCHEDULING_GREEDY_HEAP"               # 7. Greedy Choice + Heap
    CF_INCREMENTAL_CONNECTIVITY_GREEDY_DSU = "CF_INCREMENTAL_CONNECTIVITY_GREEDY_DSU" # 8. Greedy Ordering + DSU
    CF_DP_RANGE_ACCELERATION_SEGMENT_TREE = "CF_DP_RANGE_ACCELERATION_SEGMENT_TREE"   # 9. DP + Range DS Acceleration
    CF_CONVEX_DP_MONOTONIC_QUEUE = "CF_CONVEX_DP_MONOTONIC_QUEUE"                     # 10. DP + Monotone Deque Optimization
    CF_BISECTION_GREEDY_FEASIBILITY = "CF_BISECTION_GREEDY_FEASIBILITY"               # 11. Bisection + Greedy Checker
    CF_FRACTIONAL_BISECTION_DP = "CF_FRACTIONAL_BISECTION_DP"                         # 12. Bisection + 0-1 DP Knapsack


# ── 8. Cross-Family Problem Model ──

@dataclass
class CrossFamilyProblemModel:
    """
    Rich structured problem representation for cross-family synthesis.
    """
    objective: Optional[CrossFamilyObjective] = None
    initial_states: List[StateContract] = field(default_factory=list)
    derived_facts: List[DerivedFact] = field(default_factory=list)
    predicate_contract: Optional[PredicateContract] = None
    dp_contract: Optional[DPOptimizationContract] = None
    operation_algebra: Optional[OperationAlgebra] = None
    time_limit_sec: float = 1.0
    memory_limit_mb: float = 256.0
    scale_n: int = 100000
    scale_m: int = 200000

    def add_fact(self, fact_id: str, fact_text: str, source: str, rule: str, deps: Optional[List[str]] = None):
        self.derived_facts.append(DerivedFact(
            fact_id=fact_id,
            fact=fact_text,
            source=source,
            derivation_rule=rule,
            dependencies=deps or [],
            proof_status=PropertyProofStatus.PROVEN_PRESENT
        ))

    def has_fact(self, fact_id: str) -> bool:
        return any(f.fact_id == fact_id and f.proof_status == PropertyProofStatus.PROVEN_PRESENT for f in self.derived_facts)

    def get_established_fact_ids(self) -> Set[str]:
        return {f.fact_id for f in self.derived_facts if f.proof_status == PropertyProofStatus.PROVEN_PRESENT}
