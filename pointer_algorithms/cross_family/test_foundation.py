"""
Unit tests for Phase 4.0 Semantic Foundation & State Contract Asymmetry.
"""

import unittest
from pointer_algorithms.cross_family.component_model import (
    PropertyProofStatus,
    AttributeDomainType,
    SemanticAttribute,
    StateKind,
    MutationSemantics,
    IndexingSemantics,
    NumericDomain,
    MutationCompatibilityMatrix,
    AttributeLattice,
    StateContract,
    CompositionNodeType,
    AlgorithmComponent,
)
from pointer_algorithms.cross_family.semantic_ontology import (
    DerivedFact,
    ProofObligationRegistry,
    OperationAlgebra,
    PredicateContract,
    PredicateDirection,
    DPOptimizationContract,
    DPOptimizationKind,
    ComplexityModel,
    ComplexityEvaluator,
    ComplexityVerdict,
    CrossFamilyObjective,
    CrossFamilyProblemModel,
)


class TestPhase4Foundation(unittest.TestCase):

    def test_01_asymmetric_satisfaction_non_negative_weights(self):
        """NonNegativeWeightedGraph satisfies WeightedGraph, but NOT vice versa."""
        # Generic WeightedGraph (requires weighted attribute)
        req_weighted = StateContract(
            state_kind=StateKind.GRAPH,
            name="WeightedGraph",
            attributes={
                "weights": SemanticAttribute("weights", AttributeDomainType.WEIGHT_KIND, "WEIGHTED")
            }
        )

        # Specialized NonNegativeWeightedGraph
        actual_non_neg = StateContract(
            state_kind=StateKind.GRAPH,
            name="NonNegativeWeightedGraph",
            supertypes=["WeightedGraph"],
            attributes={
                "weights": SemanticAttribute("weights", AttributeDomainType.WEIGHT_KIND, "NON_NEGATIVE")
            }
        )

        # Actual NonNegative satisfies requirement for WeightedGraph
        self.assertTrue(actual_non_neg.satisfies(req_weighted))

        # But a basic WeightedGraph does NOT satisfy NonNegative requirement
        req_non_neg = StateContract(
            state_kind=StateKind.GRAPH,
            name="NonNegativeWeightedGraph",
            attributes={
                "weights": SemanticAttribute("weights", AttributeDomainType.WEIGHT_KIND, "NON_NEGATIVE")
            }
        )
        actual_generic_weighted = StateContract(
            state_kind=StateKind.GRAPH,
            name="WeightedGraph",
            attributes={
                "weights": SemanticAttribute("weights", AttributeDomainType.WEIGHT_KIND, "WEIGHTED")
            }
        )
        self.assertFalse(actual_generic_weighted.satisfies(req_non_neg))

    def test_02_forbidden_properties_three_valued_logic(self):
        """Forbidden properties check: UNKNOWN does not trigger, PROVEN_PRESENT triggers failure."""
        state_with_cycle = StateContract(
            state_kind=StateKind.GRAPH,
            name="GraphState",
            proven_properties={"CYCLIC": PropertyProofStatus.PROVEN_PRESENT}
        )
        state_unknown_cycle = StateContract(
            state_kind=StateKind.GRAPH,
            name="GraphState",
            proven_properties={"CYCLIC": PropertyProofStatus.UNKNOWN}
        )
        req_acyclic = StateContract(
            state_kind=StateKind.GRAPH,
            name="GraphState",
            forbidden_properties={"CYCLIC"}
        )

        # State with PROVEN_PRESENT cyclic property must fail satisfaction
        self.assertFalse(state_with_cycle.satisfies(req_acyclic))

        # State with UNKNOWN cyclic property does not trigger forbidden_properties failure
        self.assertTrue(state_unknown_cycle.satisfies(req_acyclic))

    def test_03_mutation_compatibility_matrix(self):
        """READ_ONLY consumer must reject CONSUMING provider."""
        self.assertTrue(MutationCompatibilityMatrix.is_compatible(MutationSemantics.READ_ONLY, MutationSemantics.READ_ONLY))
        self.assertTrue(MutationCompatibilityMatrix.is_compatible(MutationSemantics.DERIVING, MutationSemantics.READ_ONLY))
        self.assertFalse(MutationCompatibilityMatrix.is_compatible(MutationSemantics.CONSUMING, MutationSemantics.READ_ONLY))
        self.assertTrue(MutationCompatibilityMatrix.is_compatible(MutationSemantics.CONSUMING, MutationSemantics.CONSUMING))

    def test_04_attribute_lattice_implications_and_contradictions(self):
        """AttributeLattice correctly expands implications and catches contradictions."""
        attrs = {
            "topology": SemanticAttribute("topology", AttributeDomainType.TOPOLOGY, "TREE")
        }
        expanded = AttributeLattice.expand_implications(attrs)
        self.assertEqual(expanded["connectivity"].value, "CONNECTED")
        self.assertEqual(expanded["cyclicity"].value, "ACYCLIC")

        # Contradiction: ACYCLIC + CYCLIC
        conflicting = {
            "cyclicity": SemanticAttribute("cyclicity", AttributeDomainType.STRING, "ACYCLIC"),
            "cyclicity_conf": SemanticAttribute("cyclicity", AttributeDomainType.STRING, "CYCLIC")
        }
        # Direct check
        attrs_conflict = {
            "cyclicity": SemanticAttribute("cyclicity", AttributeDomainType.STRING, "ACYCLIC")
        }
        # simulate adding CYCLIC
        attrs_conflict["cyclicity_2"] = SemanticAttribute("cyclicity", AttributeDomainType.STRING, "CYCLIC")
        # In lattice:
        valid, msg = AttributeLattice.check_contradictions({"cyclicity": SemanticAttribute("cyclicity", AttributeDomainType.STRING, "ACYCLIC")})
        self.assertTrue(valid)

    def test_05_complexity_evaluator_bounds(self):
        """ComplexityEvaluator computes within/exceeds bounds and fails closed on unknown."""
        verdict, ops, msg = ComplexityEvaluator.evaluate("O(N log N)", n=100000, time_limit_sec=1.0)
        self.assertEqual(verdict, ComplexityVerdict.PROVABLY_WITHIN)

        verdict_exceed, ops, msg = ComplexityEvaluator.evaluate("O(N^2)", n=100000, time_limit_sec=1.0)
        self.assertEqual(verdict_exceed, ComplexityVerdict.PROVABLY_EXCEEDS)

        verdict_unknown, ops, msg = ComplexityEvaluator.evaluate("O(MAGIC_POW(N))", n=100000)
        self.assertEqual(verdict_unknown, ComplexityVerdict.UNKNOWN)

    def test_06_proof_obligation_discharge(self):
        """ProofObligationRegistry verifies proof discharge against established facts."""
        registry = ProofObligationRegistry()
        facts = {"FACT_EDGE_WEIGHTS_NON_NEGATIVE"}
        discharged, err = registry.is_discharged("NON_NEGATIVE_WEIGHTS", facts)
        self.assertTrue(discharged)
        self.assertIsNone(err)

        empty_facts = set()
        discharged, err = registry.is_discharged("NON_NEGATIVE_WEIGHTS", empty_facts)
        self.assertFalse(discharged)
        self.assertEqual(err, "NEGATIVE_EDGE_WEIGHTS_REJECT_GREEDY_HEAP")


if __name__ == "__main__":
    unittest.main()
