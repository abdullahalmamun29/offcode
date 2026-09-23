"""
Declarative Algorithm Capability Registry for Architecture V2.

Algorithms advertise capabilities, preconditions, resource requirements,
and proof obligations rather than keyword recognition patterns.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from architecture_v2.semantic_model import (
    SelectionKind, RequiredOperation, RelationKind, OperatorKind,
    StructuralProperty
)


@dataclass
class AlgorithmCapability:
    """
    A declarative capability model for an algorithm or data structure.
    """
    name: str
    requires_selection: Optional[SelectionKind] = None
    requires_cardinality: Optional[int] = None
    requires_relations: List[RelationKind] = field(default_factory=list)
    requires_operators: List[OperatorKind] = field(default_factory=list)
    requires_operations: List[RequiredOperation] = field(default_factory=list)
    requires_properties: List[StructuralProperty] = field(default_factory=list)
    provides_operations: List[RequiredOperation] = field(default_factory=list)
    complexity_time: str = "O(N)"
    complexity_space: str = "O(N)"
    input_storage: str = "O(N)"
    auxiliary_space: str = "O(1)"
    output_contract: List[str] = field(default_factory=list)  # e.g., ["ORIGINAL_INDICES", "VALUES", "BOOLEAN"]
    proof_obligations: List[str] = field(default_factory=list)
    implementation_backend: str = ""
    is_composition: bool = False
    composed_of: List[str] = field(default_factory=list)


class CapabilityRegistry:
    """
    Maintains registered algorithm capabilities and supports requirement queries.
    """
    def __init__(self):
        self.capabilities: Dict[str, AlgorithmCapability] = {}
        self._register_default_capabilities()

    def register(self, cap: AlgorithmCapability) -> None:
        self.capabilities[cap.name] = cap

    def get(self, name: str) -> Optional[AlgorithmCapability]:
        return self.capabilities.get(name)

    def all(self) -> List[AlgorithmCapability]:
        return list(self.capabilities.values())

    def _register_default_capabilities(self) -> None:
        # 1. Two-Pointer Pair Sum
        self.register(AlgorithmCapability(
            name="two_pointer_pair_sum",
            requires_selection=SelectionKind.FIXED_CARDINALITY,
            requires_cardinality=2,
            requires_relations=[RelationKind.SUM],
            requires_operations=[RequiredOperation.PAIR_SUM_SEARCH],
            provides_operations=[RequiredOperation.PAIR_SUM_SEARCH, RequiredOperation.PAIR_SEARCH],
            complexity_time="O(N log N)",
            complexity_space="O(N)",
            output_contract=["ORIGINAL_INDICES", "VALUES", "BOOLEAN"],
            proof_obligations=[
                "selection_cardinality_is_2",
                "relation_is_sum",
                "sorting_permitted",
                "original_indices_preserved",
                "pointer_elimination_sound",
                "search_terminates"
            ],
            implementation_backend="cpp_generator:pair_sum_sorted"
        ))

        # 2. Hash Pair Sum (Unordered Set / Map Lookup)
        self.register(AlgorithmCapability(
            name="hash_pair_sum",
            requires_selection=SelectionKind.FIXED_CARDINALITY,
            requires_cardinality=2,
            requires_relations=[RelationKind.SUM],
            requires_operations=[RequiredOperation.PAIR_SUM_SEARCH],
            provides_operations=[RequiredOperation.PAIR_SUM_SEARCH, RequiredOperation.PAIR_SEARCH],
            complexity_time="O(N)",
            complexity_space="O(N)",
            output_contract=["ORIGINAL_INDICES", "VALUES", "BOOLEAN"],
            proof_obligations=[
                "selection_cardinality_is_2",
                "relation_is_sum",
                "complement_lookup_exact"
            ],
            implementation_backend="hash_map_pair_lookup"
        ))

        # 3. 0/1 Knapsack DP
        self.register(AlgorithmCapability(
            name="knapsack_01",
            requires_selection=SelectionKind.ARBITRARY_SUBSET,
            requires_relations=[RelationKind.SUM],
            requires_properties=[StructuralProperty.ARBITRARY_SUBSET, StructuralProperty.OPTIMAL_SUBSTRUCTURE],
            provides_operations=[RequiredOperation.SELECT, RequiredOperation.AGGREGATE],
            complexity_time="O(N * W)",
            complexity_space="O(W)",
            output_contract=["MAX_VALUE", "SUBSET"],
            proof_obligations=[
                "arbitrary_subset_selection",
                "bellman_optimality",
                "capacity_feasible"
            ],
            implementation_backend="cpp_generator:dp_knapsack"
        ))

        # 4. Subset Sum DP
        self.register(AlgorithmCapability(
            name="subset_sum_dp",
            requires_selection=SelectionKind.ARBITRARY_SUBSET,
            requires_relations=[RelationKind.SUM],
            requires_properties=[StructuralProperty.ARBITRARY_SUBSET],
            provides_operations=[RequiredOperation.SEARCH, RequiredOperation.SELECT],
            complexity_time="O(N * target)",
            complexity_space="O(target)",
            output_contract=["BOOLEAN", "SUBSET"],
            proof_obligations=[
                "arbitrary_subset_selection",
                "target_feasible"
            ],
            implementation_backend="cpp_generator:dp_knapsack"
        ))

        # 5. Ordered Multiset Predecessor
        self.register(AlgorithmCapability(
            name="ordered_multiset_predecessor",
            requires_properties=[StructuralProperty.DYNAMIC_STATE, StructuralProperty.ORDERED_STATE],
            requires_operations=[RequiredOperation.PREDECESSOR],
            provides_operations=[RequiredOperation.PREDECESSOR, RequiredOperation.DELETE, RequiredOperation.INSERT],
            complexity_time="O(log N)",
            complexity_space="O(N)",
            output_contract=["VALUES", "PREDECESSOR"],
            proof_obligations=[
                "ordered_comparator_valid",
                "dynamic_balanced_tree_invariants"
            ],
            implementation_backend="stl:multiset"
        ))

        # 6. Ordered Multiset Successor
        self.register(AlgorithmCapability(
            name="ordered_multiset_successor",
            requires_properties=[StructuralProperty.DYNAMIC_STATE, StructuralProperty.ORDERED_STATE],
            requires_operations=[RequiredOperation.SUCCESSOR],
            provides_operations=[RequiredOperation.SUCCESSOR, RequiredOperation.DELETE, RequiredOperation.INSERT],
            complexity_time="O(log N)",
            complexity_space="O(N)",
            output_contract=["VALUES", "SUCCESSOR"],
            proof_obligations=[
                "ordered_comparator_valid",
                "dynamic_balanced_tree_invariants"
            ],
            implementation_backend="stl:multiset"
        ))

        # 7. Binary Trie Max XOR
        self.register(AlgorithmCapability(
            name="trie_max_xor",
            requires_operators=[OperatorKind.XOR],
            requires_properties=[StructuralProperty.PAIRWISE_RELATION],
            requires_operations=[RequiredOperation.PAIR_SEARCH, RequiredOperation.MAXIMUM_QUERY],
            provides_operations=[RequiredOperation.PAIR_SEARCH, RequiredOperation.MAXIMUM_QUERY],
            complexity_time="O(N * 32)",
            complexity_space="O(N * 32)",
            output_contract=["MAX_VALUE", "PAIR_VALUES"],
            proof_obligations=[
                "bitwise_prefix_greedy_choice",
                "fixed_bitwidth_representation"
            ],
            implementation_backend="cpp_generator:trie_max_xor"
        ))

        # 8. Binary Search (Ordered Domain)
        self.register(AlgorithmCapability(
            name="binary_search",
            requires_properties=[StructuralProperty.ORDERED_STATE, StructuralProperty.MONOTONICITY],
            requires_operations=[RequiredOperation.SEARCH],
            provides_operations=[RequiredOperation.SEARCH, RequiredOperation.SELECT],
            complexity_time="O(log N)",
            complexity_space="O(1)",
            output_contract=["INDEX", "BOOLEAN", "VALUE"],
            proof_obligations=[
                "monotonic_predicate",
                "search_interval_contains_answer",
                "termination_without_infinite_loop"
            ],
            implementation_backend="cpp_generator:binary_search"
        ))

        # 9. DSU Connectivity
        self.register(AlgorithmCapability(
            name="dsu_connectivity",
            requires_properties=[StructuralProperty.CONNECTIVITY],
            requires_operations=[RequiredOperation.CONNECTIVITY],
            provides_operations=[RequiredOperation.CONNECTIVITY, RequiredOperation.MERGE],
            complexity_time="O(alpha(N))",
            complexity_space="O(N)",
            output_contract=["BOOLEAN", "COUNT"],
            proof_obligations=[
                "equivalence_relation_partition",
                "acyclic_component_merges"
            ],
            implementation_backend="cpp_generator:dsu_basic"
        ))

        # 10. Sliding Window Contiguous Aggregate
        self.register(AlgorithmCapability(
            name="sliding_window_contiguous",
            requires_selection=SelectionKind.CONTIGUOUS_SEGMENT,
            requires_properties=[StructuralProperty.CONTIGUOUS_SELECTION],
            requires_operations=[RequiredOperation.RANGE_AGGREGATE],
            provides_operations=[RequiredOperation.RANGE_AGGREGATE, RequiredOperation.AGGREGATE],
            complexity_time="O(N)",
            complexity_space="O(1)",
            output_contract=["VALUES", "MAX_VALUE", "MIN_VALUE"],
            proof_obligations=[
                "contiguous_range_preservation",
                "monotone_expansion_and_shrinking"
            ],
            implementation_backend="cpp_generator:sliding_window"
        ))

        # 11. Anchor Selection (Sub-capability for fixed-cardinality decomposition)
        self.register(AlgorithmCapability(
            name="anchor_selection",
            requires_selection=SelectionKind.FIXED_CARDINALITY,
            provides_operations=[RequiredOperation.SELECT],
            complexity_time="O(N)",
            complexity_space="O(1)",
            output_contract=["ORIGINAL_INDICES", "VALUES"],
            proof_obligations=[
                "anchor_excluded_from_residual_search",
                "original_indices_preserved"
            ]
        ))

        # 12. Greedy Capacity Pairing (At-most-2 grouping under additive capacity bound)
        self.register(AlgorithmCapability(
            name="greedy_capacity_pairing",
            requires_selection=SelectionKind.ALL_ELEMENTS,
            requires_relations=[RelationKind.LESS_EQUAL],
            requires_operations=[RequiredOperation.CAPACITY_PAIRING],
            requires_properties=[
                StructuralProperty.CAPACITY_CONSTRAINED_GROUPING,
                StructuralProperty.EXTREMAL_PAIRING,
                StructuralProperty.ORDERED_STATE,
                StructuralProperty.LOCAL_CHOICE
            ],
            provides_operations=[RequiredOperation.CAPACITY_PAIRING],
            complexity_time="O(N log N)",
            complexity_space="O(N)",
            output_contract=["COUNT", "VALUES"],
            proof_obligations=[
                "extremal_pairing_optimal",
                "sorting_permitted",
                "opposite_pointers_exhaust_search",
                "capacity_feasibility_checked",
                "all_items_covered"
            ],
            implementation_backend="cpp_generator:greedy_capacity_pairing"
        ))

        # 13. Greedy Two-Sequence Interval Matching
        self.register(AlgorithmCapability(
            name="greedy_two_sequence_interval_matching",
            requires_relations=[RelationKind.INTERVAL_TOLERANCE],
            requires_operations=[RequiredOperation.TWO_SEQUENCE_INTERVAL_MATCHING],
            requires_properties=[
                StructuralProperty.TWO_SEQUENCE_MATCHING,
                StructuralProperty.ONE_TO_ONE_MATCHING,
                StructuralProperty.MONOTONE_COMPATIBILITY,
                StructuralProperty.ORDERED_STATE,
                StructuralProperty.LOCAL_CHOICE,
                StructuralProperty.MAX_CARDINALITY_MATCHING
            ],
            provides_operations=[RequiredOperation.TWO_SEQUENCE_INTERVAL_MATCHING],
            complexity_time="O((N + M) log(N + M))",
            complexity_space="O(N + M)",
            output_contract=["COUNT"],
            proof_obligations=[
                "two_distinct_collections",
                "one_to_one_matching",
                "maximize_match_count",
                "sortable_numeric_domains",
                "interval_compatibility",
                "monotone_compatibility",
                "discard_too_small_is_safe",
                "discard_too_large_is_safe",
                "feasible_pair_match_is_safe",
                "both_pointers_monotonically_advance",
                "all_remaining_elements_eventually_processed"
            ],
            implementation_backend="cpp_generator:greedy_two_sequence_interval_matching"
        ))

        # 14. Sliding Window Exact Range Sum Count
        self.register(AlgorithmCapability(
            name="sliding_window_exact_range_sum_count",
            requires_selection=SelectionKind.CONTIGUOUS_SEGMENT,
            requires_relations=[RelationKind.EQUALITY],
            requires_operators=[OperatorKind.SUM],
            requires_properties=[
                StructuralProperty.CONTIGUOUS_SELECTION,
                StructuralProperty.MONOTONE_RANGE_SUM,
                StructuralProperty.ORDERED_STATE
            ],
            requires_operations=[
                RequiredOperation.RANGE_AGGREGATE,
                RequiredOperation.COUNT
            ],
            provides_operations=[
                RequiredOperation.RANGE_AGGREGATE,
                RequiredOperation.COUNT
            ],
            complexity_time="O(N)",
            complexity_space="O(N)",
            input_storage="O(N)",
            auxiliary_space="O(1)",
            output_contract=["COUNT"],
            proof_obligations=[
                "contiguous_range_selection",
                "strictly_positive_elements",
                "range_sum_equals_target",
                "monotone_right_expansion",
                "monotone_left_contraction",
                "no_solutions_skipped",
                "both_pointers_advance_monotonically",
                "count_all_valid_ranges"
            ],
            implementation_backend="cpp_generator:sliding_window_exact_sum_count"
        ))

        # 15. Sort and Maximum Bounded Diameter Subset
        self.register(AlgorithmCapability(
            name="sort_and_maximum_bounded_diameter_subset",
            requires_selection=SelectionKind.ARBITRARY_SUBSET,
            requires_relations=[RelationKind.PAIRWISE_ABSOLUTE_DIFFERENCE],
            requires_properties=[
                StructuralProperty.BOUNDED_DIAMETER,
                StructuralProperty.SORTED_CONTIGUOUS_OPTIMAL_BLOCK,
                StructuralProperty.MONOTONE_VALID_WINDOW,
                StructuralProperty.ORDERED_STATE,
                StructuralProperty.SINGLE_COLLECTION,
                StructuralProperty.SORTABLE
            ],
            requires_operations=[
                RequiredOperation.MAX_VALID_WINDOW
            ],
            provides_operations=[
                RequiredOperation.MAX_VALID_WINDOW,
                RequiredOperation.SELECT
            ],
            complexity_time="O(N log N)",
            complexity_space="O(N)",
            input_storage="O(N)",
            auxiliary_space="O(1)",
            output_contract=["MAX_CARDINALITY", "COUNT"],
            proof_obligations=[
                "bounded_diameter_holds",
                "optimal_subset_contiguous_in_sorted",
                "window_predicate_monotone",
                "maximize_cardinality_optimal",
                "sorting_permitted",
                "single_collection",
                "pointers_advance_monotonically"
            ],
            implementation_backend="cpp_generator:sort_and_maximum_bounded_diameter_subset"
        ))
