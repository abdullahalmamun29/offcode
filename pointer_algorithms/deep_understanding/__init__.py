"""
CHUP Phase 6 — Deep Problem Understanding Package.
"""

from pointer_algorithms.deep_understanding.fact_model import (
    FactTier,
    ProofStatus,
    AmbiguityStatus,
    SemanticFact,
    FactSet
)
from pointer_algorithms.deep_understanding.provenance import (
    ProvenanceNode,
    ProvenanceGraph
)
from pointer_algorithms.deep_understanding.rule_registry import (
    DerivationRule,
    DerivationRuleRegistry
)
from pointer_algorithms.deep_understanding.contradiction_engine import (
    SourceFactContradictionEngine,
    ConflictingFactsCertificate,
    AmbiguityReport
)
from pointer_algorithms.deep_understanding.invariant_prover import InvariantProver
from pointer_algorithms.deep_understanding.implicit_constraints import ImplicitConstraintInferrer
from pointer_algorithms.deep_understanding.hidden_invariants import HiddenInvariantEngine
from pointer_algorithms.deep_understanding.operation_semantics import OperationSemanticsEngine
from pointer_algorithms.deep_understanding.state_dependency import (
    StateDependencyEngine,
    StateTopologyKind
)
from pointer_algorithms.deep_understanding.semantic_objective import (
    SemanticObjectiveEngine,
    ObjectiveKind,
    ArithmeticRequirement
)
from pointer_algorithms.deep_understanding.complexity_requirements import (
    ComplexityRequirementEngine,
    ComplexityRequirementEnvelope,
    MachineModel,
    ComplexityBoundKind
)
from pointer_algorithms.deep_understanding.deep_understanding_facade import DeepProblemUnderstandingFacade
