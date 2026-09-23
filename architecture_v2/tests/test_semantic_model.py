"""
Unit tests for architecture_v2.semantic_model.
"""

import unittest
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

class TestSemanticModel(unittest.TestCase):

    def test_evidence_provenance(self):
        ev = Evidence(
            fact="two distinct elements",
            source="Find two distinct elements whose sum equals target.",
            confidence=0.99,
            status=EvidenceStatus.EXPLICIT
        )
        self.assertEqual(ev.fact, "two distinct elements")
        self.assertEqual(ev.status, EvidenceStatus.EXPLICIT)
        self.assertNotIn("algorithm", repr(ev))

    def test_fact_dependencies(self):
        f1 = Fact(name="selection.cardinality", value=2, status=FactStatus.KNOWN, source="text")
        f2 = Fact(name="relation.kind", value=RelationKind.SUM, status=FactStatus.KNOWN, source="text")
        f3 = Fact(
            name="required_operation",
            value=RequiredOperation.PAIR_SUM_SEARCH,
            status=FactStatus.INFERRED,
            source="derivation",
            derivation_rule="FixedCardinalityPairSum",
            dependencies=["selection.cardinality", "relation.kind"]
        )
        self.assertEqual(f3.dependencies, ["selection.cardinality", "relation.kind"])
        self.assertEqual(f3.status, FactStatus.INFERRED)

    def test_selection_model(self):
        s1 = SelectionModel(kind=SelectionKind.FIXED_CARDINALITY, cardinality=2)
        s2 = SelectionModel(kind=SelectionKind.CONTIGUOUS_SEGMENT)
        s3 = SelectionModel(kind=SelectionKind.ARBITRARY_SUBSET)
        self.assertEqual(s1.cardinality, 2)
        self.assertEqual(s2.kind, SelectionKind.CONTIGUOUS_SEGMENT)
        self.assertEqual(s3.kind, SelectionKind.ARBITRARY_SUBSET)

    def test_problem_model_graph_and_facts(self):
        pm = ProblemModel(raw_text="Find two elements with sum equal to target")
        pm.selection = SelectionModel(SelectionKind.FIXED_CARDINALITY, 2)
        pm.objective = ObjectiveModel(ObjectiveKind.FIND_ANY)
        pm.constraints.target_value = 100
        pm.constraints.memory_limit_mb = 256

        f1 = Fact("selection.cardinality", 2, FactStatus.KNOWN, "text")
        pm.add_fact(f1)
        self.assertTrue(pm.has_fact("selection.cardinality"))
        self.assertEqual(pm.get_fact("selection.cardinality").value, 2)

        deps = pm.graph.get_dependencies("selection.cardinality")
        self.assertEqual(deps, [])

    def test_structural_properties_and_state_model(self):
        sm = StateModel(
            state_variables={"i": "int", "j": "int"},
            transitions=["lo++", "hi--"],
            state_reversibility=True
        )
        self.assertTrue(sm.state_reversibility)
        self.assertIn("i", sm.state_variables)

if __name__ == "__main__":
    unittest.main()
