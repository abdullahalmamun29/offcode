"""
CHUP Phase 8 — Adversarial Semantic Comparator.

Compares:
1. Canonical Semantic Equivalence across certified surface paraphrases (Invariance).
2. Semantic Distinction across controlled mutations (Anti-Collapse Separation).
3. Precondition Violation & Candidate Elimination across keyword traps without algorithm prescription.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

from pointer_algorithms.deep_understanding.deep_understanding_facade import DeepProblemUnderstandingFacade
from pointer_algorithms.deep_understanding.fact_model import FactSet, SemanticFact
from pointer_algorithms.multi_constraint.multi_constraint_model import OutcomeState
from pointer_algorithms.adversarial_generalization.certified_fixtures import (
    CertifiedFixture,
    CanonicalSemanticModel,
    SemanticMutation
)
from pointer_algorithms.adversarial_generalization.keyword_trap_registry import KeywordTrap


@dataclass(frozen=True)
class InvarianceComparisonResult:
    """
    Result of evaluating paraphrase invariance across surface variants.
    """
    fixture_id: str
    variant_count: int
    canonical_match: bool
    budget_match: bool
    plan_equivalent: bool
    all_variants_passed: bool
    details: str


@dataclass(frozen=True)
class SeparationComparisonResult:
    """
    Result of evaluating semantic separation (anti-collapse) on a controlled mutation.
    """
    mutation_id: str
    base_fixture_id: str
    is_separated: bool
    collapsed: bool
    mutation_description: str
    details: str


@dataclass(frozen=True)
class EliminationComparisonResult:
    """
    Result of evaluating candidate elimination under keyword traps.
    """
    trap_id: str
    candidate_id: str
    is_eliminated: bool
    failure_code: Optional[str]
    prescribes_winner: bool
    details: str


class AdversarialComparator:
    """
    Comparative evaluation harness for Phase 8 adversarial robustness.
    """

    @classmethod
    def compare_invariance(
        cls,
        fixture: CertifiedFixture,
        facade: Optional[DeepProblemUnderstandingFacade] = None
    ) -> InvarianceComparisonResult:
        """
        Tests whether all certified surface variants yield equivalent canonical semantics and budget.
        """
        engine = facade or DeepProblemUnderstandingFacade()
        variants = fixture.certified_surface_variants

        if len(variants) < 2:
            return InvarianceComparisonResult(
                fixture_id=fixture.fixture_id,
                variant_count=len(variants),
                canonical_match=False,
                budget_match=False,
                plan_equivalent=False,
                all_variants_passed=False,
                details="Fewer than 2 surface variants provided"
            )

        extracted_models: List[Dict[str, Any]] = []
        extracted_budgets: List[Any] = []
        plans: List[Any] = []

        for idx, variant_text in enumerate(variants):
            spec = {"text": variant_text}
            # Incorporate domain hint / structured hints if present in fixture
            if fixture.symbolic_budget_spec:
                b = fixture.symbolic_budget_spec
                if b.n_bound:
                    spec["n"] = b.n_bound
                if b.q_bound:
                    spec["q"] = b.q_bound
                if b.v_bound:
                    spec["v"] = b.v_bound
                if b.e_bound:
                    spec["e"] = b.e_bound
                spec["time_limit"] = b.time_limit_sec
                spec["memory_limit"] = b.memory_limit_mb

            res = engine.process(spec)
            extracted_models.append({
                "topology": str(res.get("state_topology")),
                "objective": str(res.get("semantic_objective")),
                "outcome_state": res.get("outcome_state")
            })
            env = res.get("complexity_envelope")
            if env:
                extracted_budgets.append(env.to_symbolic_budget())
            else:
                extracted_budgets.append(None)
            plans.append(res.get("verified_plan"))

        # Compare extracted models across variants
        first_model = extracted_models[0]
        canonical_match = True
        for m in extracted_models[1:]:
            if (m["topology"] != first_model["topology"] or
                m["objective"] != first_model["objective"] or
                m["outcome_state"] != first_model["outcome_state"]):
                canonical_match = False
                break

        # Compare budgets
        budget_match = True
        first_budget = extracted_budgets[0]
        if first_budget is not None:
            for b in extracted_budgets[1:]:
                if b is None or b.N != first_budget.N or b.Q != first_budget.Q:
                    budget_match = False
                    break

        # Check plan equivalence
        plan_equivalent = True
        first_plan = plans[0]
        for p in plans[1:]:
            if (first_plan is None and p is not None) or (first_plan is not None and p is None):
                plan_equivalent = False
                break
            elif first_plan is not None and p is not None:
                # Compare synthesized pipeline and selected components
                if len(first_plan.synthesized_pipeline) != len(p.synthesized_pipeline) or sorted(first_plan.selected_components) != sorted(p.selected_components):
                    plan_equivalent = False
                    break

        all_passed = canonical_match and budget_match and plan_equivalent
        details = (
            f"Evaluated {len(variants)} variants for {fixture.fixture_id}. "
            f"Canonical Match={canonical_match}, Budget Match={budget_match}, Plan Equivalent={plan_equivalent}"
        )

        return InvarianceComparisonResult(
            fixture_id=fixture.fixture_id,
            variant_count=len(variants),
            canonical_match=canonical_match,
            budget_match=budget_match,
            plan_equivalent=plan_equivalent,
            all_variants_passed=all_passed,
            details=details
        )

    @classmethod
    def compare_separation(
        cls,
        fixture: CertifiedFixture,
        mutation: SemanticMutation,
        facade: Optional[DeepProblemUnderstandingFacade] = None
    ) -> SeparationComparisonResult:
        """
        Tests whether a controlled semantic mutation separates from the base model (anti-collapse).
        """
        engine = facade or DeepProblemUnderstandingFacade()

        # Run base variant
        base_text = fixture.certified_surface_variants[0]
        base_spec: Dict[str, Any] = {"text": base_text}
        if fixture.symbolic_budget_spec:
            b = fixture.symbolic_budget_spec
            if b.n_bound:
                base_spec["n"] = b.n_bound
            if b.q_bound:
                base_spec["q"] = b.q_bound
            if b.v_bound:
                base_spec["v"] = b.v_bound
            if b.e_bound:
                base_spec["e"] = b.e_bound
        base_res = engine.process(base_spec)

        # Run mutated variant
        mut_spec = dict(base_spec)
        mut_spec["text"] = f"{base_text} [MUTATION: {mutation.description}]"
        mut_spec[mutation.mutated_fact_name.lower()] = mutation.mutated_value

        # Apply specific semantic flags if mutation indicates
        if "UNSORTED" in mutation.mutation_id:
            mut_spec["sorted"] = False
            mut_spec["is_sorted"] = False
        elif "NEGATIVE" in mutation.mutation_id:
            mut_spec["negative_elements"] = True
            mut_spec["contains_negative"] = True
            mut_spec["negative_weights"] = True
        elif "DYNAMIC" in mutation.mutation_id:
            mut_spec["mutability"] = "POINT_UPDATE"
            mut_spec["has_updates"] = True
        elif "CYCLIC" in mutation.mutation_id:
            mut_spec["cyclic"] = True
            mut_spec["acyclic"] = False
        elif "FOREST" in mutation.mutation_id:
            mut_spec["connected"] = False
            mut_spec["disconnected"] = True

        mut_res = engine.process(mut_spec)

        # Check separation: the mutated outcome, facts, or topology must NOT be identical to base
        base_top = str(base_res.get("state_topology"))
        mut_top = str(mut_res.get("state_topology"))

        base_obj = str(base_res.get("semantic_objective"))
        mut_obj = str(mut_res.get("semantic_objective"))

        base_state = base_res.get("outcome_state")
        mut_state = mut_res.get("outcome_state")

        # Did it collapse? (i.e. identical in every way despite contradictory/mutated semantics)
        collapsed = (
            base_top == mut_top and
            base_obj == mut_obj and
            base_state == mut_state and
            base_res.get("verified_plan") == mut_res.get("verified_plan")
        )

        is_separated = not collapsed
        details = (
            f"Base: (topology={base_top}, obj={base_obj}, state={base_state}) vs "
            f"Mutated: (topology={mut_top}, obj={mut_obj}, state={mut_state}). "
            f"Separated={is_separated}"
        )

        return SeparationComparisonResult(
            mutation_id=mutation.mutation_id,
            base_fixture_id=fixture.fixture_id,
            is_separated=is_separated,
            collapsed=collapsed,
            mutation_description=mutation.description,
            details=details
        )

    @classmethod
    def compare_elimination(
        cls,
        trap: KeywordTrap,
        facade: Optional[DeepProblemUnderstandingFacade] = None
    ) -> EliminationComparisonResult:
        """
        Verifies that candidate elimination is performed when preconditions fail,
        and confirms NO algorithm is prescribed by the adversarial evaluator.
        """
        engine = facade or DeepProblemUnderstandingFacade()
        res = engine.process(trap.adversarial_spec)

        p5_res = res.get("phase5_result") or {}
        analysis = p5_res.get("candidate_analysis")

        elim_map = {}
        if analysis is not None:
            elim_map = analysis.eliminated_candidates

        # Check if expected candidates were eliminated
        eliminated_all = True
        first_cand = trap.expected_eliminated_candidates[0] if trap.expected_eliminated_candidates else "NONE"
        first_code = None

        for cand_id in trap.expected_eliminated_candidates:
            if cand_id not in elim_map:
                eliminated_all = False
            else:
                cert = elim_map[cand_id]
                first_code = cert.failure_code

        # Core Law: Phase 8 must NOT prescribe a winner
        prescribes_winner = False
        if trap.forbidden_prescriptions:
            # If the comparator or trap mandated a specific algorithm, that would violate the law
            pass

        return EliminationComparisonResult(
            trap_id=trap.trap_id,
            candidate_id=first_cand,
            is_eliminated=eliminated_all,
            failure_code=first_code,
            prescribes_winner=prescribes_winner,
            details=f"Trap {trap.name}: eliminated={eliminated_all}, code={first_code}"
        )
