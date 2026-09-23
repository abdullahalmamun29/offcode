"""
CHUP Recognition Architecture V2 Package.

Semantic Problem Understanding → Structural Reasoning → Candidate Selection → Composable Algorithm Planning.
"""

from architecture_v2.semantic_model import (
    Evidence, EvidenceStatus,
    Fact, FactStatus,
    Hypothesis, HypothesisStatus,
    SelectionKind, SelectionModel,
    ObjectiveKind, ObjectiveModel,
    ConstraintModel,
    RequiredOperation,
    RelationKind, OperatorKind, RelationModel,
    StructuralProperty,
    StateModel,
    ProblemStructureGraph,
    ProblemModel
)

__all__ = [
    "Evidence", "EvidenceStatus",
    "Fact", "FactStatus",
    "Hypothesis", "HypothesisStatus",
    "SelectionKind", "SelectionModel",
    "ObjectiveKind", "ObjectiveModel",
    "ConstraintModel",
    "RequiredOperation",
    "RelationKind", "OperatorKind", "RelationModel",
    "StructuralProperty",
    "StateModel",
    "ProblemStructureGraph",
    "ProblemModel"
]
