"""
CHUP Phase 6 — Semantic Objective & Arithmetic Domain Engine.

Models WHAT the problem asks for, completely decoupled from algorithmic selection.

Authoritative Invariant:
ObjectiveKind describes the semantic goal, NOT the solution technique:
- OPTIMIZATION_EXTREMUM describes min/max goal, NEVER prescribing Greedy or DP.
- CARDINALITY_COUNTING describes counting goal, NEVER prescribing DP or Combinatorics.
- DECISION_FEASIBILITY describes boolean goal, NEVER prescribing Bisection or 2-SAT.
- EXISTENTIAL_WITNESS describes construction goal, NEVER prescribing Backtracking.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Tuple
import uuid
from pointer_algorithms.deep_understanding.fact_model import (
    SemanticFact,
    FactSet,
    FactTier,
    ProofStatus,
    AmbiguityStatus
)
from pointer_algorithms.deep_understanding.provenance import (
    ProvenanceNode,
    ProvenanceGraph
)
from pointer_algorithms.multi_constraint.aggregate_ontology import (
    QuerySpec,
    QueryTarget,
    QueryOutput,
    QueryDependency,
    AggregateSpec
)


class ObjectiveKind(Enum):
    OPTIMIZATION_EXTREMUM = "OPTIMIZATION_EXTREMUM"
    EXISTENTIAL_WITNESS = "EXISTENTIAL_WITNESS"
    CARDINALITY_COUNTING = "CARDINALITY_COUNTING"
    DECISION_FEASIBILITY = "DECISION_FEASIBILITY"
    DYNAMIC_QUERY_AGGREGATE = "DYNAMIC_QUERY_AGGREGATE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class ArithmeticRequirement:
    """
    Precision and overflow guard requirements.
    """
    requires_64bit: bool = False
    modulo: Optional[int] = None
    floating_tolerance: Optional[float] = None


class SemanticObjectiveEngine:
    """
    Maps problem targets to formal semantic objectives and arithmetic requirements.
    """

    @classmethod
    def deduce_objective(
        cls,
        facts: FactSet,
        aggregate_spec: Optional[AggregateSpec] = None
    ) -> Tuple[ObjectiveKind, QuerySpec, ArithmeticRequirement]:
        """
        Deduces semantic objective and builds an authoritative QuerySpec for Phase 5.
        """
        # 1. Determine ObjectiveKind
        if facts.has_proven("GOAL_COUNT_WAYS", True):
            obj_kind = ObjectiveKind.CARDINALITY_COUNTING
            output_type = QueryOutput.FREQUENCY_COUNT
        elif facts.has_proven("GOAL_DECISION_FEASIBILITY", True):
            obj_kind = ObjectiveKind.DECISION_FEASIBILITY
            output_type = QueryOutput.EXISTENCE_BOOLEAN
        elif facts.has_proven("GOAL_FIND_ANY_WITNESS", True):
            obj_kind = ObjectiveKind.EXISTENTIAL_WITNESS
            output_type = QueryOutput.PATH_SEQUENCE
        elif facts.has_proven("GOAL_DYNAMIC_QUERIES", True):
            obj_kind = ObjectiveKind.DYNAMIC_QUERY_AGGREGATE
            output_type = QueryOutput.SCALAR_VALUE
        elif facts.has_proven("GOAL_OPTIMIZE_EXTREMUM", True):
            obj_kind = ObjectiveKind.OPTIMIZATION_EXTREMUM
            output_type = QueryOutput.SCALAR_VALUE
        else:
            obj_kind = ObjectiveKind.UNKNOWN
            output_type = QueryOutput.SCALAR_VALUE

        # 2. Determine QueryTarget
        target = QueryTarget.POINT
        if facts.has_proven("TARGET_LINEAR_RANGE", True):
            target = QueryTarget.LINEAR_RANGE
        elif facts.has_proven("TARGET_TREE_PATH", True):
            target = QueryTarget.TREE_PATH
        elif facts.has_proven("TARGET_TREE_SUBTREE", True):
            target = QueryTarget.TREE_SUBTREE
        elif facts.has_proven("TARGET_ALL_PAIRS", True):
            target = QueryTarget.ALL_PAIRS

        # 3. Arithmetic Requirements
        req_64bit = facts.has_proven("POTENTIAL_INTEGER_OVERFLOW", True)
        modulo_val = None
        mod_fact = facts.get("ARITHMETIC_MODULO")
        if mod_fact and isinstance(mod_fact.value, int):
            modulo_val = mod_fact.value
        elif facts.has_proven("MODULO_1E9_7", True):
            modulo_val = 1_000_000_007
        elif facts.has_proven("MODULO_998244353", True):
            modulo_val = 998_244_353

        arith = ArithmeticRequirement(
            requires_64bit=req_64bit,
            modulo=modulo_val,
            floating_tolerance=1e-6 if facts.has_proven("FLOATING_POINT_ANSWER", True) else None
        )

        query_spec = QuerySpec(
            target=target,
            aggregate=aggregate_spec,
            output=output_type,
            dependency=QueryDependency.INDEPENDENT
        )

        return obj_kind, query_spec, arith
