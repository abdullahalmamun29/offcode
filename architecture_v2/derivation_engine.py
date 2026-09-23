"""
Generic Derivation Engine with Dependency Tracking for Architecture V2.

Transforms established facts into new semantic facts using generic derivation rules.
Records provenance, dependencies, and rules for complete auditability.
"""

from typing import List, Dict, Any, Optional, Callable
from architecture_v2.semantic_model import (
    ProblemModel, Fact, FactStatus,
    SelectionKind, ObjectiveKind,
    RelationKind, OperatorKind,
    ConstraintDomain,
    RequiredOperation, StructuralProperty
)


class DerivationRule:
    """
    A generic derivation rule.
    Declarative: specifies name, required dependencies, and derivation logic.
    """
    def __init__(
        self,
        name: str,
        description: str,
        dependencies: List[str],
        apply_fn: Callable[[ProblemModel], Optional[Fact]]
    ):
        self.name = name
        self.description = description
        self.dependencies = dependencies
        self.apply_fn = apply_fn

    def execute(self, model: ProblemModel) -> Optional[Fact]:
        # Verify all dependencies exist and are active (KNOWN or INFERRED)
        # and not UNKNOWN, AMBIGUOUS, or CONTRADICTED.
        for dep in self.dependencies:
            if not model.has_fact(dep):
                return None
            fact = model.get_fact(dep)
            if fact is None:
                return None
            if fact.status in (FactStatus.UNKNOWN, FactStatus.AMBIGUOUS, FactStatus.CONTRADICTED):
                return None
            if fact.value in (SelectionKind.UNKNOWN, ObjectiveKind.UNKNOWN, None):
                return None
        return self.apply_fn(model)


class DerivationEngine:
    """
    Executes derivation rules in topological/iterative passes until fixed point.
    """
    def __init__(self):
        self.rules: List[DerivationRule] = []
        self._register_default_rules()

    def register_rule(self, rule: DerivationRule) -> None:
        self.rules.append(rule)

    def _register_default_rules(self) -> None:
        # ── Rule 1: Contiguous Selection ──
        def derive_contiguous(m: ProblemModel) -> Optional[Fact]:
            sel = m.get_fact("selection.kind")
            if sel and sel.value == SelectionKind.CONTIGUOUS_SEGMENT:
                m.structural_properties.add(StructuralProperty.CONTIGUOUS_SELECTION)
                return Fact(
                    name="structural.contiguous_selection",
                    value=True,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="ContiguousSelectionRule",
                    dependencies=["selection.kind"],
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="ContiguousSelectionRule",
            description="Derives CONTIGUOUS_SELECTION from selection.kind = CONTIGUOUS_SEGMENT",
            dependencies=["selection.kind"],
            apply_fn=derive_contiguous
        ))

        # ── Rule 2: Arbitrary Subset ──
        def derive_arbitrary_subset(m: ProblemModel) -> Optional[Fact]:
            sel = m.get_fact("selection.kind")
            if sel and sel.value == SelectionKind.ARBITRARY_SUBSET:
                m.structural_properties.add(StructuralProperty.ARBITRARY_SUBSET)
                return Fact(
                    name="structural.arbitrary_subset",
                    value=True,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="ArbitrarySubsetRule",
                    dependencies=["selection.kind"],
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="ArbitrarySubsetRule",
            description="Derives ARBITRARY_SUBSET from selection.kind = ARBITRARY_SUBSET",
            dependencies=["selection.kind"],
            apply_fn=derive_arbitrary_subset
        ))

        # ── Rule 3: All Elements ──
        def derive_all_elements(m: ProblemModel) -> Optional[Fact]:
            sel = m.get_fact("selection.kind")
            if sel and sel.value == SelectionKind.ALL_ELEMENTS:
                m.structural_properties.add(StructuralProperty.ALL_ELEMENTS_REQUIRED)
                return Fact(
                    name="structural.all_elements_required",
                    value=True,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="AllElementsRule",
                    dependencies=["selection.kind"],
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="AllElementsRule",
            description="Derives ALL_ELEMENTS_REQUIRED from selection.kind = ALL_ELEMENTS",
            dependencies=["selection.kind"],
            apply_fn=derive_all_elements
        ))

        # ── Rule 4: Delete Action ──
        def derive_delete(m: ProblemModel) -> Optional[Fact]:
            has_del = m.has_fact("action.delete") or m.has_fact("operation.delete")
            if has_del:
                m.operations.add(RequiredOperation.DELETE)
                m.structural_properties.add(StructuralProperty.DYNAMIC_STATE)
                dep = "action.delete" if m.has_fact("action.delete") else "operation.delete"
                return Fact(
                    name="operation.delete",
                    value=RequiredOperation.DELETE,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="DeleteActionRule",
                    dependencies=[dep],
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="DeleteActionRule",
            description="Derives DELETE operation and DYNAMIC_STATE from action.delete",
            dependencies=[],
            apply_fn=derive_delete
        ))

        # ── Rule 5: Insert Action ──
        def derive_insert(m: ProblemModel) -> Optional[Fact]:
            has_ins = m.has_fact("action.insert") or m.has_fact("operation.insert")
            if has_ins:
                m.operations.add(RequiredOperation.INSERT)
                m.structural_properties.add(StructuralProperty.DYNAMIC_STATE)
                dep = "action.insert" if m.has_fact("action.insert") else "operation.insert"
                return Fact(
                    name="operation.insert",
                    value=RequiredOperation.INSERT,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="InsertActionRule",
                    dependencies=[dep],
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="InsertActionRule",
            description="Derives INSERT operation and DYNAMIC_STATE from action.insert",
            dependencies=[],
            apply_fn=derive_insert
        ))

        # ── Rule 6: Repeated Queries ──
        def derive_query(m: ProblemModel) -> Optional[Fact]:
            if m.has_fact("query.repeated"):
                m.operations.add(RequiredOperation.QUERY)
                return Fact(
                    name="operation.query",
                    value=RequiredOperation.QUERY,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="RepeatedQueriesRule",
                    dependencies=["query.repeated"],
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="RepeatedQueriesRule",
            description="Derives QUERY operation from query.repeated",
            dependencies=["query.repeated"],
            apply_fn=derive_query
        ))

        # ── Rule A: Fixed Cardinality Pair Sum ──
        def derive_pair_sum(m: ProblemModel) -> Optional[Fact]:
            sel_fact = m.get_fact("selection.cardinality")
            rel_fact = m.get_fact("relation.kind")
            rel_domain_ok = any((r.kind == RelationKind.SUM or r.operator == OperatorKind.SUM) and r.domain == ConstraintDomain.PROBLEM_DATA for r in m.relations) if m.relations else True
            if (sel_fact and sel_fact.value == 2) and (rel_fact and rel_fact.value == RelationKind.SUM) and rel_domain_ok:
                m.operations.add(RequiredOperation.PAIR_SUM_SEARCH)
                m.operations.add(RequiredOperation.PAIR_SEARCH)
                m.structural_properties.add(StructuralProperty.FIXED_CARDINALITY)
                m.structural_properties.add(StructuralProperty.PAIRWISE_RELATION)
                return Fact(
                    name="operation.pair_sum_search",
                    value=RequiredOperation.PAIR_SUM_SEARCH,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="FixedCardinalityPairSum",
                    dependencies=["selection.cardinality", "relation.kind"],
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="FixedCardinalityPairSum",
            description="Derives PAIR_SUM_SEARCH from fixed_cardinality=2 and relation=SUM",
            dependencies=["selection.cardinality", "relation.kind"],
            apply_fn=derive_pair_sum
        ))

        # ── Rule A2: Fixed Cardinality Additive Target (Generic k >= 2) ──
        def derive_additive_target(m: ProblemModel) -> Optional[Fact]:
            sel_fact = m.get_fact("selection.cardinality")
            rel_fact = m.get_fact("relation.kind")
            rel_domain_ok = any((r.kind == RelationKind.SUM or r.operator == OperatorKind.SUM) and r.domain == ConstraintDomain.PROBLEM_DATA for r in m.relations) if m.relations else True
            if (sel_fact and isinstance(sel_fact.value, int) and sel_fact.value >= 2) and (rel_fact and rel_fact.value == RelationKind.SUM) and rel_domain_ok:
                m.operations.add(RequiredOperation.ADDITIVE_TARGET_SEARCH)
                m.structural_properties.add(StructuralProperty.FIXED_CARDINALITY)
                if sel_fact.value > 2:
                    m.structural_properties.add(StructuralProperty.DECOMPOSABLE_ADDITIVE_SEARCH)
                return Fact(
                    name="operation.additive_target_search",
                    value=RequiredOperation.ADDITIVE_TARGET_SEARCH,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="FixedCardinalityAdditiveTarget",
                    dependencies=["selection.cardinality", "relation.kind"],
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="FixedCardinalityAdditiveTarget",
            description="Derives ADDITIVE_TARGET_SEARCH from fixed_cardinality >= 2 and relation=SUM",
            dependencies=["selection.cardinality", "relation.kind"],
            apply_fn=derive_additive_target
        ))

        # ── Rule A3: Distinct Selection Requirement ──
        def derive_distinct_selection(m: ProblemModel) -> Optional[Fact]:
            dist_fact = m.get_fact("selection.distinct_positions")
            if dist_fact and dist_fact.value is True:
                m.structural_properties.add(StructuralProperty.PAIRWISE_DISTINCT_SELECTION)
                return Fact(
                    name="structural.pairwise_distinct_selection",
                    value=True,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="DistinctSelectionRule",
                    dependencies=["selection.distinct_positions"],
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="DistinctSelectionRule",
            description="Derives PAIRWISE_DISTINCT_SELECTION from selection.distinct_positions = True",
            dependencies=["selection.distinct_positions"],
            apply_fn=derive_distinct_selection
        ))

        # ── Rule B: Max Valid Value Under Upper Bound → Dynamic Predecessor vs Static Bounded Selection ──
        def derive_predecessor(m: ProblemModel) -> Optional[Fact]:
            obj_fact = m.get_fact("objective.kind")
            rel_fact = m.get_fact("relation.kind")
            if (obj_fact and obj_fact.value == ObjectiveKind.MAXIMIZE) and \
               (rel_fact and rel_fact.value == RelationKind.LESS_EQUAL):
                is_dynamic = (
                    m.has_fact("collection.dynamic") or
                    m.has_fact("action.delete") or
                    m.has_fact("action.insert") or
                    m.has_fact("operation.delete") or
                    m.has_fact("operation.insert") or
                    m.has_fact("query.repeated") or
                    m.has_fact("stream.sequential") or
                    m.has_fact("processing.sequential") or
                    RequiredOperation.DELETE in m.operations or
                    RequiredOperation.INSERT in m.operations or
                    RequiredOperation.QUERY in m.operations or
                    StructuralProperty.DYNAMIC_STATE in m.structural_properties
                )
                m.operations.add(RequiredOperation.PREDECESSOR)
                if is_dynamic:
                    m.structural_properties.add(StructuralProperty.PREDECESSOR_QUERY)
                    deps = ["objective.kind", "relation.kind"]
                    for d in ["collection.dynamic", "action.delete", "action.insert", "query.repeated", "stream.sequential"]:
                        if m.has_fact(d):
                            deps.append(d)
                    return Fact(
                        name="operation.predecessor",
                        value=RequiredOperation.PREDECESSOR,
                        status=FactStatus.INFERRED,
                        source="derivation",
                        derivation_rule="MaxValidValueUnderUpperBound",
                        dependencies=deps,
                        confidence=1.0
                    )
                else:
                    m.operations.add(RequiredOperation.STATIC_BOUNDED_SELECTION)
                    m.structural_properties.add(StructuralProperty.STATIC_BOUNDED_SELECTION)
                    return Fact(
                        name="operation.static_bounded_selection",
                        value=RequiredOperation.STATIC_BOUNDED_SELECTION,
                        status=FactStatus.INFERRED,
                        source="derivation",
                        derivation_rule="MaxValidValueUnderUpperBound",
                        dependencies=["objective.kind", "relation.kind"],
                        confidence=1.0
                    )
            return None

        self.register_rule(DerivationRule(
            name="MaxValidValueUnderUpperBound",
            description="Derives PREDECESSOR (dynamic) or STATIC_BOUNDED_SELECTION (static) from maximize objective and value <= bound relation",
            dependencies=["objective.kind", "relation.kind"],
            apply_fn=derive_predecessor
        ))

        # ── Rule C: Min Valid Value Above Lower Bound → Dynamic Successor vs Static Bounded Selection ──
        def derive_successor(m: ProblemModel) -> Optional[Fact]:
            obj_fact = m.get_fact("objective.kind")
            rel_fact = m.get_fact("relation.kind")
            if (obj_fact and obj_fact.value == ObjectiveKind.MINIMIZE) and \
               (rel_fact and rel_fact.value == RelationKind.GREATER_EQUAL):
                is_dynamic = (
                    m.has_fact("collection.dynamic") or
                    m.has_fact("action.delete") or
                    m.has_fact("action.insert") or
                    m.has_fact("operation.delete") or
                    m.has_fact("operation.insert") or
                    m.has_fact("query.repeated") or
                    m.has_fact("stream.sequential") or
                    m.has_fact("processing.sequential") or
                    RequiredOperation.DELETE in m.operations or
                    RequiredOperation.INSERT in m.operations or
                    RequiredOperation.QUERY in m.operations or
                    StructuralProperty.DYNAMIC_STATE in m.structural_properties
                )
                m.operations.add(RequiredOperation.SUCCESSOR)
                if is_dynamic:
                    m.structural_properties.add(StructuralProperty.SUCCESSOR_QUERY)
                    deps = ["objective.kind", "relation.kind"]
                    for d in ["collection.dynamic", "action.delete", "action.insert", "query.repeated", "stream.sequential"]:
                        if m.has_fact(d):
                            deps.append(d)
                    return Fact(
                        name="operation.successor",
                        value=RequiredOperation.SUCCESSOR,
                        status=FactStatus.INFERRED,
                        source="derivation",
                        derivation_rule="MinValidValueAboveLowerBound",
                        dependencies=deps,
                        confidence=1.0
                    )
                else:
                    m.operations.add(RequiredOperation.STATIC_BOUNDED_SELECTION)
                    m.structural_properties.add(StructuralProperty.STATIC_BOUNDED_SELECTION)
                    return Fact(
                        name="operation.static_bounded_selection",
                        value=RequiredOperation.STATIC_BOUNDED_SELECTION,
                        status=FactStatus.INFERRED,
                        source="derivation",
                        derivation_rule="MinValidValueAboveLowerBound",
                        dependencies=["objective.kind", "relation.kind"],
                        confidence=1.0
                    )
            return None

        self.register_rule(DerivationRule(
            name="MinValidValueAboveLowerBound",
            description="Derives SUCCESSOR (dynamic) or STATIC_BOUNDED_SELECTION (static) from minimize objective and value >= bound relation",
            dependencies=["objective.kind", "relation.kind"],
            apply_fn=derive_successor
        ))

        # ── Rule D: Dynamic Collection Maintenance ──
        def derive_dynamic_state(m: ProblemModel) -> Optional[Fact]:
            has_insert = RequiredOperation.INSERT in m.operations or m.has_fact("action.insert") or m.has_fact("operation.insert")
            has_delete = RequiredOperation.DELETE in m.operations or m.has_fact("action.delete") or m.has_fact("operation.delete")
            has_dynamic = m.has_fact("collection.dynamic") or m.has_fact("stream.sequential") or m.has_fact("processing.sequential")
            if has_insert or has_delete or has_dynamic:
                m.structural_properties.add(StructuralProperty.DYNAMIC_STATE)
                deps = [d for d in ["collection.dynamic", "action.insert", "action.delete", "operation.insert", "operation.delete", "stream.sequential", "processing.sequential"] if m.has_fact(d)]
                return Fact(
                    name="structural.dynamic_state",
                    value=True,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="DynamicCollectionMaintenance",
                    dependencies=deps,
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="DynamicCollectionMaintenance",
            description="Derives DYNAMIC_STATE when collection requires dynamic insertions/deletions or sequential processing",
            dependencies=[],
            apply_fn=derive_dynamic_state
        ))

        # ── Rule E: Ordered Search Requirement ──
        def derive_ordered_search(m: ProblemModel) -> Optional[Fact]:
            has_pred = RequiredOperation.PREDECESSOR in m.operations or m.has_fact("operation.predecessor")
            has_succ = RequiredOperation.SUCCESSOR in m.operations or m.has_fact("operation.successor")
            has_static_bounded = (
                RequiredOperation.STATIC_BOUNDED_SELECTION in m.operations or
                m.has_fact("operation.static_bounded_selection")
            )
            if has_pred or has_succ or has_static_bounded:
                m.structural_properties.add(StructuralProperty.ORDERED_STATE)
                deps = [d for d in ["operation.predecessor", "operation.successor", "operation.static_bounded_selection"] if m.has_fact(d)]
                return Fact(
                    name="structural.ordered_search_required",
                    value=True,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="OrderedSearchRequirement",
                    dependencies=deps,
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="OrderedSearchRequirement",
            description="Derives ORDERED_STATE requirement when predecessor/successor or static bounded queries exist",
            dependencies=[],
            apply_fn=derive_ordered_search
        ))

        # ── Rule F: Divide & Conquer Potential ──
        def derive_dc_potential(m: ProblemModel) -> Optional[Fact]:
            indep = m.get_fact("subproblem.independence")
            recurs = m.get_fact("structure.recursive_decomposition")
            if indep and indep.value and recurs and recurs.value:
                m.structural_properties.add(StructuralProperty.INDEPENDENT_SUBPROBLEMS)
                m.structural_properties.add(StructuralProperty.RECURSIVE_DECOMPOSITION)
                return Fact(
                    name="structural.dc_potential",
                    value=True,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="DivideAndConquerPotential",
                    dependencies=["subproblem.independence", "structure.recursive_decomposition"],
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="DivideAndConquerPotential",
            description="Derives D&C potential from independent subproblems and recursive decomposition",
            dependencies=["subproblem.independence", "structure.recursive_decomposition"],
            apply_fn=derive_dc_potential
        ))

        # ── Rule G: Backtracking Potential ──
        def derive_backtracking_potential(m: ProblemModel) -> Optional[Fact]:
            rev = m.get_fact("state.reversibility")
            branch = m.get_fact("structure.branching")
            if rev and rev.value and branch and branch.value:
                m.structural_properties.add(StructuralProperty.REVERSIBLE_DECISIONS)
                m.structural_properties.add(StructuralProperty.BRANCHING)
                return Fact(
                    name="structural.backtracking_potential",
                    value=True,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="BacktrackingPotential",
                    dependencies=["state.reversibility", "structure.branching"],
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="BacktrackingPotential",
            description="Derives Backtracking potential from reversible decisions and branching",
            dependencies=["state.reversibility", "structure.branching"],
            apply_fn=derive_backtracking_potential
        ))

        # ── Rule H: DP Potential ──
        def derive_dp_potential(m: ProblemModel) -> Optional[Fact]:
            overlap = m.get_fact("subproblem.overlapping")
            opt_sub = m.get_fact("structure.optimal_substructure")
            if (overlap and overlap.value) and (opt_sub and opt_sub.value):
                m.structural_properties.add(StructuralProperty.OVERLAPPING_SUBPROBLEMS)
                m.structural_properties.add(StructuralProperty.OPTIMAL_SUBSTRUCTURE)
                return Fact(
                    name="structural.dp_potential",
                    value=True,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="DynamicProgrammingPotential",
                    dependencies=["subproblem.overlapping", "structure.optimal_substructure"],
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="DynamicProgrammingPotential",
            description="Derives DP potential from overlapping subproblems and optimal substructure",
            dependencies=["subproblem.overlapping", "structure.optimal_substructure"],
            apply_fn=derive_dp_potential
        ))

        # ── Rule I: Capacity-Constrained Pairing Greedy ──
        def derive_capacity_pairing_greedy(m: ProblemModel) -> Optional[Fact]:
            obj_fact = m.get_fact("objective.kind")
            sel_fact = m.get_fact("selection.kind")
            group_card_fact = m.get_fact("group.max_cardinality")
            is_less_equal = any(r.kind == RelationKind.LESS_EQUAL and r.domain == ConstraintDomain.PROBLEM_DATA for r in m.relations) or (m.has_fact("relation.kind") and m.get_fact("relation.kind").value == RelationKind.LESS_EQUAL)
            is_sum_op = (
                any((r.operator == OperatorKind.SUM or r.kind == RelationKind.SUM) and r.domain == ConstraintDomain.PROBLEM_DATA for r in m.relations) or
                (m.has_fact("operator.kind") and m.get_fact("operator.kind").value == OperatorKind.SUM) or
                (m.has_fact("relation.kind") and m.get_fact("relation.kind").value == RelationKind.SUM)
            )
            has_capacity = m.has_fact("constraint.group_capacity") or m.has_fact("group.capacity_constrained") or m.constraints.group_capacity is not None

            # Preconditions:
            # 1. Objective is MINIMIZE (specifically partitions/groups)
            # 2. Maximum group cardinality is 2
            # 3. Additive feasibility relation: sum(weights) <= capacity
            # 4. All elements must be assigned (selection.kind == ALL_ELEMENTS)
            is_min_groups = (
                obj_fact and obj_fact.value == ObjectiveKind.MINIMIZE and
                (m.objective.target_property in ("groups", "partitions", "general") or m.has_fact("objective.target_property"))
            )
            is_cardinality_2 = (
                (group_card_fact and group_card_fact.value == 2) or
                m.constraints.max_group_cardinality == 2
            )
            is_additive_capacity = is_less_equal and (is_sum_op or has_capacity)
            is_all_elements = (
                (sel_fact and sel_fact.value == SelectionKind.ALL_ELEMENTS) or
                m.selection.kind == SelectionKind.ALL_ELEMENTS or
                StructuralProperty.ALL_ELEMENTS_REQUIRED in m.structural_properties
            )

            if is_min_groups and is_cardinality_2 and is_additive_capacity and is_all_elements:
                m.operations.add(RequiredOperation.CAPACITY_PAIRING)
                m.structural_properties.add(StructuralProperty.CAPACITY_CONSTRAINED_GROUPING)
                m.structural_properties.add(StructuralProperty.EXTREMAL_PAIRING)
                m.structural_properties.add(StructuralProperty.ORDERED_STATE)
                m.structural_properties.add(StructuralProperty.LOCAL_CHOICE)
                m.structural_properties.add(StructuralProperty.GLOBAL_OPTIMUM)

                deps = ["objective.kind", "selection.kind"]
                for d in ["group.max_cardinality", "relation.kind", "operator.kind", "constraint.group_capacity"]:
                    if m.has_fact(d):
                        deps.append(d)

                return Fact(
                    name="operation.capacity_pairing",
                    value=RequiredOperation.CAPACITY_PAIRING,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="CapacityPairingGreedyRule",
                    dependencies=deps,
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="CapacityPairingGreedyRule",
            description="Derives CAPACITY_PAIRING, CAPACITY_CONSTRAINED_GROUPING, and EXTREMAL_PAIRING from MINIMIZE groups, group_cardinality<=2, additive capacity bound, and ALL_ELEMENTS",
            dependencies=["objective.kind", "selection.kind"],
            apply_fn=derive_capacity_pairing_greedy
        ))

        # ── Rule J: Two-Sequence Monotonic Matching Greedy ──
        def derive_two_sequence_monotonic_matching(m: ProblemModel) -> Optional[Fact]:
            has_two_colls = (
                m.has_fact("collection.two_distinct_collections") or
                len(m.collections) >= 2 or
                StructuralProperty.TWO_SEQUENCE_MATCHING in m.structural_properties
            )
            has_1to1 = (
                m.has_fact("matching.one_to_one") or
                StructuralProperty.ONE_TO_ONE_MATCHING in m.structural_properties
            )
            has_interval_tol = (
                any(r.kind == RelationKind.INTERVAL_TOLERANCE for r in m.relations) or
                m.has_fact("relation.interval_tolerance") or
                StructuralProperty.MONOTONE_COMPATIBILITY in m.structural_properties
            )
            obj_fact = m.get_fact("objective.kind")
            is_max_matches = (
                obj_fact and obj_fact.value == ObjectiveKind.MAXIMIZE and
                (
                    m.objective.target_property in ("matches", "assignments", "elements", "general") or
                    m.has_fact("objective.maximize_matches") or
                    StructuralProperty.MAX_CARDINALITY_MATCHING in m.structural_properties
                )
            )

            if has_two_colls and has_1to1 and has_interval_tol and is_max_matches:
                m.operations.add(RequiredOperation.TWO_SEQUENCE_INTERVAL_MATCHING)
                m.structural_properties.add(StructuralProperty.TWO_SEQUENCE_MATCHING)
                m.structural_properties.add(StructuralProperty.ONE_TO_ONE_MATCHING)
                m.structural_properties.add(StructuralProperty.MONOTONE_COMPATIBILITY)
                m.structural_properties.add(StructuralProperty.ORDERED_STATE)
                m.structural_properties.add(StructuralProperty.LOCAL_CHOICE)
                m.structural_properties.add(StructuralProperty.MAX_CARDINALITY_MATCHING)

                deps = []
                for d in ["collection.two_distinct_collections", "matching.one_to_one", "relation.interval_tolerance", "objective.kind"]:
                    if m.has_fact(d):
                        deps.append(d)

                return Fact(
                    name="operation.two_sequence_interval_matching",
                    value=RequiredOperation.TWO_SEQUENCE_INTERVAL_MATCHING,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="TwoSequenceMonotonicMatchingGreedyRule",
                    dependencies=deps,
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="TwoSequenceMonotonicMatchingGreedyRule",
            description="Derives TWO_SEQUENCE_INTERVAL_MATCHING, TWO_SEQUENCE_MATCHING, ONE_TO_ONE_MATCHING, MONOTONE_COMPATIBILITY, ORDERED_STATE, LOCAL_CHOICE, and MAX_CARDINALITY_MATCHING from two distinct collections, 1-to-1 matching, interval tolerance relation, and MAXIMIZE matches objective",
            dependencies=["collection.two_distinct_collections", "matching.one_to_one", "relation.interval_tolerance", "objective.kind"],
            apply_fn=derive_two_sequence_monotonic_matching
        ))

        # ── Rule K: Monotone Range Sum Derivation Rule ──
        def derive_monotone_range_sum(m: ProblemModel) -> Optional[Fact]:
            sel = m.get_fact("selection.kind")
            is_contiguous = (
                (sel and sel.value == SelectionKind.CONTIGUOUS_SEGMENT) or
                m.selection.kind == SelectionKind.CONTIGUOUS_SEGMENT or
                StructuralProperty.CONTIGUOUS_SELECTION in m.structural_properties
            )
            is_sum_op = (
                any((r.operator == OperatorKind.SUM or r.kind == RelationKind.SUM) and r.domain == ConstraintDomain.PROBLEM_DATA for r in m.relations) or
                (m.has_fact("operator.kind") and m.get_fact("operator.kind").value == OperatorKind.SUM) or
                (m.has_fact("relation.kind") and m.get_fact("relation.kind").value == RelationKind.SUM)
            )
            is_equality_or_bound = (
                any(r.kind in (RelationKind.EQUALITY, RelationKind.LESS_EQUAL, RelationKind.SUM) and r.domain == ConstraintDomain.PROBLEM_DATA for r in m.relations) or
                (m.has_fact("relation.kind") and m.get_fact("relation.kind").value in (RelationKind.EQUALITY, RelationKind.LESS_EQUAL, RelationKind.SUM))
            )
            is_strictly_positive = (
                m.constraints.strictly_positive or
                (m.has_fact("domain.strictly_positive") and m.get_fact("domain.strictly_positive").value is True) or
                (m.has_fact("domain.value_positivity") and m.get_fact("domain.value_positivity").value == "POSITIVE")
            )

            # Mathematical Preconditions:
            # 1. Contiguous segment selection
            # 2. Additive aggregation (SUM)
            # 3. Target constraint (equality or bound)
            # 4. Strictly positive values (a_i > 0)
            #
            # Mathematical Proof:
            # For all i, a[i] > 0.
            # For fixed L, S(L, R + 1) = S(L, R) + a[R + 1] > S(L, R) (strictly increasing as R advances).
            # For fixed R, S(L + 1, R) = S(L, R) - a[L] < S(L, R) (strictly decreasing as L advances).
            # Therefore:
            # - If sum < target: R must advance (extending window is necessary to increase sum).
            # - If sum > target: L must advance (shrinking window is necessary to decrease sum).
            # - If sum == target: for the current R, exactly one valid L exists.
            # The search space is strictly monotone; no valid range can be skipped.
            if is_contiguous and is_sum_op and is_equality_or_bound and is_strictly_positive:
                m.structural_properties.add(StructuralProperty.MONOTONE_RANGE_SUM)
                m.structural_properties.add(StructuralProperty.MONOTONICITY)
                m.structural_properties.add(StructuralProperty.CONTIGUOUS_SELECTION)
                m.structural_properties.add(StructuralProperty.ORDERED_STATE)
                m.operations.add(RequiredOperation.RANGE_AGGREGATE)

                deps = ["selection.kind", "domain.strictly_positive"]
                for d in ["relation.kind", "operator.kind", "domain.value_positivity"]:
                    if m.has_fact(d):
                        deps.append(d)

                return Fact(
                    name="structural.monotone_range_sum",
                    value=True,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="MonotoneRangeSumDerivationRule",
                    dependencies=deps,
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="MonotoneRangeSumDerivationRule",
            description="Derives MONOTONE_RANGE_SUM, MONOTONICITY, and RANGE_AGGREGATE from CONTIGUOUS_SEGMENT selection, SUM operator, and strictly positive elements (a_i > 0)",
            dependencies=["selection.kind", "domain.strictly_positive"],
            apply_fn=derive_monotone_range_sum
        ))

        # ── Rule: Count Objective ──
        def derive_count_objective(m: ProblemModel) -> Optional[Fact]:
            obj = m.get_fact("objective.kind")
            if (obj and obj.value == ObjectiveKind.COUNT) or m.objective.kind == ObjectiveKind.COUNT:
                m.operations.add(RequiredOperation.COUNT)
                return Fact(
                    name="operation.count",
                    value=True,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="CountObjectiveRule",
                    dependencies=["objective.kind"] if obj else [],
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="CountObjectiveRule",
            description="Derives RequiredOperation.COUNT from objective.kind = COUNT",
            dependencies=["objective.kind"],
            apply_fn=derive_count_objective
        ))

        # ── Rule L: Pairwise Difference to Bounded Diameter Rule ──
        def derive_bounded_diameter(m: ProblemModel) -> Optional[Fact]:
            has_pairwise_diff = (
                any(r.kind == RelationKind.PAIRWISE_ABSOLUTE_DIFFERENCE and r.domain == ConstraintDomain.PROBLEM_DATA for r in m.relations) or
                m.has_fact("relation.pairwise_absolute_difference") or
                (m.has_fact("relation.kind") and m.get_fact("relation.kind").value == RelationKind.PAIRWISE_ABSOLUTE_DIFFERENCE)
            )
            # Mathematical Proof:
            # Let S be a subset of elements.
            # Condition 1: For all x, y in S, |x - y| <= k.
            # Condition 2: max(S) - min(S) <= k.
            # Proof:
            # (1 => 2): Since max(S) in S and min(S) in S, setting x = max(S), y = min(S) gives |max(S) - min(S)| = max(S) - min(S) <= k.
            # (2 => 1): For any x, y in S, min(S) <= x <= max(S) and min(S) <= y <= max(S).
            # Thus |x - y| <= max(S) - min(S) <= k.
            # Therefore, pairwise absolute difference is logically and mathematically equivalent to bounded diameter.
            if has_pairwise_diff:
                m.structural_properties.add(StructuralProperty.BOUNDED_DIAMETER)
                m.structural_properties.add(StructuralProperty.PAIRWISE_RELATION)
                deps = [d for d in ["relation.pairwise_absolute_difference", "relation.kind"] if m.has_fact(d)]
                return Fact(
                    name="structural.bounded_diameter",
                    value=True,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="PairwiseDifferenceToBoundedDiameterRule",
                    dependencies=deps,
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="PairwiseDifferenceToBoundedDiameterRule",
            description="Derives BOUNDED_DIAMETER and PAIRWISE_RELATION from PAIRWISE_ABSOLUTE_DIFFERENCE relation (max(S) - min(S) <= k <=> forall x, y in S: |x - y| <= k)",
            dependencies=[],
            apply_fn=derive_bounded_diameter
        ))

        # ── Rule M: Sorted Contiguous Optimal Block Rule ──
        def derive_sorted_contiguous_optimal_block(m: ProblemModel) -> Optional[Fact]:
            is_arbitrary_subset = (
                StructuralProperty.ARBITRARY_SUBSET in m.structural_properties or
                m.selection.kind == SelectionKind.ARBITRARY_SUBSET or
                (m.has_fact("selection.kind") and m.get_fact("selection.kind").value == SelectionKind.ARBITRARY_SUBSET)
            )
            is_bounded_diameter = (
                StructuralProperty.BOUNDED_DIAMETER in m.structural_properties or
                m.has_fact("structural.bounded_diameter")
            )
            is_max_cardinality = (
                m.objective.kind == ObjectiveKind.MAXIMIZE_CARDINALITY or
                (m.has_fact("objective.kind") and m.get_fact("objective.kind").value == ObjectiveKind.MAXIMIZE_CARDINALITY)
            )
            is_single_collection = (
                StructuralProperty.SINGLE_COLLECTION in m.structural_properties or
                m.has_fact("collection.single_collection") or
                len(m.collections) <= 1
            )
            is_sortable = (
                StructuralProperty.SORTABLE in m.structural_properties or
                m.has_fact("collection.sortable") or
                m.has_fact("domain.orderable")
            )

            # Strict Dependency & Invariant:
            # Must explicitly require ARBITRARY_SUBSET + BOUNDED_DIAMETER + MAXIMIZE_CARDINALITY + SINGLE_COLLECTION + SORTABLE.
            # Do NOT use ObjectiveKind.MAXIMIZE as fallback.
            #
            # Mathematical Proof:
            # Let sorted array be A[1..n] with A[1] <= A[2] <= ... <= A[n].
            # Suppose S* is an optimal subset maximizing |S*| subject to diam(S*) <= k.
            # Let i = min_{x in S*} idx(x) and j = max_{x in S*} idx(x).
            # Feasibility: A[j] - A[i] <= k.
            # For any intermediate index m in [i, j], A[i] <= A[m] <= A[j] by sorted monotonicity.
            # Thus A[m] - A[i] <= A[j] - A[i] <= k and A[j] - A[m] <= A[j] - A[i] <= k.
            # Therefore the contiguous block B = A[i..j] is feasible: diam(B) = A[j] - A[i] <= k.
            # Since S* is a subset of B, |B| >= |S*|.
            # Since S* is optimal maximizing cardinality, |S*| >= |B|, which implies |B| = |S*|.
            # Hence, there exists an optimal subset that forms a contiguous block in the sorted sequence.
            if is_arbitrary_subset and is_bounded_diameter and is_max_cardinality and is_single_collection and is_sortable:
                m.structural_properties.add(StructuralProperty.SORTED_CONTIGUOUS_OPTIMAL_BLOCK)
                m.structural_properties.add(StructuralProperty.ORDERED_STATE)
                deps = ["selection.kind", "objective.kind"]
                for d in ["structural.bounded_diameter", "collection.single_collection", "collection.sortable"]:
                    if m.has_fact(d):
                        deps.append(d)
                return Fact(
                    name="structural.sorted_contiguous_optimal_block",
                    value=True,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="SortedContiguousOptimalBlockRule",
                    dependencies=deps,
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="SortedContiguousOptimalBlockRule",
            description="Derives SORTED_CONTIGUOUS_OPTIMAL_BLOCK and ORDERED_STATE from ARBITRARY_SUBSET + BOUNDED_DIAMETER + MAXIMIZE_CARDINALITY + SINGLE_COLLECTION + SORTABLE",
            dependencies=["selection.kind", "objective.kind"],
            apply_fn=derive_sorted_contiguous_optimal_block
        ))

        # ── Rule N: Monotone Valid Window Rule ──
        def derive_monotone_valid_window(m: ProblemModel) -> Optional[Fact]:
            has_sorted_block = (
                StructuralProperty.SORTED_CONTIGUOUS_OPTIMAL_BLOCK in m.structural_properties or
                m.has_fact("structural.sorted_contiguous_optimal_block")
            )
            has_bounded_diameter = (
                StructuralProperty.BOUNDED_DIAMETER in m.structural_properties or
                m.has_fact("structural.bounded_diameter")
            )
            is_ordered = (
                StructuralProperty.ORDERED_STATE in m.structural_properties or
                StructuralProperty.SORTABLE in m.structural_properties or
                m.has_fact("collection.sortable")
            )
            pairwise_diff_rel = next(
                (r for r in m.relations if r.kind == RelationKind.PAIRWISE_ABSOLUTE_DIFFERENCE and r.domain == ConstraintDomain.PROBLEM_DATA),
                None
            )
            has_diff_rel = pairwise_diff_rel is not None or m.has_fact("relation.pairwise_absolute_difference")

            # Mathematical Derivation Chain:
            # 1. Premise: Sorted contiguous optimal block (SORTED_CONTIGUOUS_OPTIMAL_BLOCK)
            #    guarantees that an optimal subset S* corresponds to a contiguous index window [L, R]
            #    in the sorted sequence A[1..n] where A[1] <= A[2] <= ... <= A[n].
            # 2. Reduction: In any sorted contiguous slice A[L..R], the minimum element is A[L]
            #    and the maximum element is A[R].
            #    Therefore, the diameter constraint max(S) - min(S) <= k reduces exactly to the
            #    linear window predicate:
            #        P(L, R) <=> A[R] - A[L] <= k
            # 3. Directional Monotonicity:
            #    - Right expansion: Since A is sorted non-decreasingly, A[R+1] >= A[R].
            #      Thus (A[R+1] - A[L]) >= (A[R] - A[L]). The difference is monotonically non-decreasing in R.
            #    - Left contraction: Similarly, A[L+1] >= A[L], so (A[R] - A[L+1]) <= (A[R] - A[L]).
            #      The difference is monotonically non-increasing in L.
            # 4. Soundness of Two-Pointer Sliding Window:
            #    For each right boundary R, the feasible left boundaries form a contiguous range [L*(R), R]
            #    where L*(R) = min { L <= R : A[R] - A[L] <= k }.
            #    Because A[R+1] >= A[R], we have L*(R+1) >= L*(R).
            #    Therefore, the left pointer L never retreats; both pointers advance monotonically.
            if has_sorted_block and has_bounded_diameter and is_ordered and has_diff_rel:
                m.structural_properties.add(StructuralProperty.MONOTONE_VALID_WINDOW)
                m.structural_properties.add(StructuralProperty.MONOTONICITY)
                m.operations.add(RequiredOperation.MAX_VALID_WINDOW)

                # Record the derived window predicate explicitly into the model facts
                tol_val = m.get_fact("relation.pairwise_absolute_difference").value if m.has_fact("relation.pairwise_absolute_difference") else (pairwise_diff_rel.tolerance if pairwise_diff_rel else "k")
                m.add_fact(Fact(
                    name="window.predicate",
                    value=f"A[R] - A[L] <= {tol_val}",
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="MonotoneValidWindowRule",
                    dependencies=["structural.sorted_contiguous_optimal_block", "structural.bounded_diameter"],
                    confidence=1.0
                ))
                m.add_fact(Fact(
                    name="window.left_monotonicity",
                    value="NON_INCREASING_IN_L",
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="MonotoneValidWindowRule",
                    dependencies=["structural.sorted_contiguous_optimal_block"],
                    confidence=1.0
                ))
                m.add_fact(Fact(
                    name="window.right_monotonicity",
                    value="NON_DECREASING_IN_R",
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="MonotoneValidWindowRule",
                    dependencies=["structural.sorted_contiguous_optimal_block"],
                    confidence=1.0
                ))

                deps = ["structural.sorted_contiguous_optimal_block"]
                if m.has_fact("structural.bounded_diameter"):
                    deps.append("structural.bounded_diameter")
                if m.has_fact("relation.pairwise_absolute_difference"):
                    deps.append("relation.pairwise_absolute_difference")

                return Fact(
                    name="structural.monotone_valid_window",
                    value=True,
                    status=FactStatus.INFERRED,
                    source="derivation",
                    derivation_rule="MonotoneValidWindowRule",
                    dependencies=deps,
                    confidence=1.0
                )
            return None

        self.register_rule(DerivationRule(
            name="MonotoneValidWindowRule",
            description="Derives MONOTONE_VALID_WINDOW, MONOTONICITY, window.predicate (A[R] - A[L] <= k), and directional monotonicity from SORTED_CONTIGUOUS_OPTIMAL_BLOCK and BOUNDED_DIAMETER",
            dependencies=["structural.sorted_contiguous_optimal_block"],
            apply_fn=derive_monotone_valid_window
        ))

    def run(self, model: ProblemModel, max_iterations: int = 10) -> ProblemModel:
        """
        Runs derivation rules iteratively until no new facts are produced.
        """
        for _ in range(max_iterations):
            new_facts = 0
            for rule in self.rules:
                fact = rule.execute(model)
                if fact and not model.has_fact(fact.name):
                    model.add_fact(fact)
                    new_facts += 1
            if new_facts == 0:
                break
        return model
