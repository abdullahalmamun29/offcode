"""
CHUP Phase 3O — String Component Model & Transformation Registry.

Defines declarative AlgorithmComponents and Transformation Adapters for the String domain.
Enforces:
1. Explicit StateContract input/output typing and attribute unification.
2. Distinction between algorithmic components and mathematical reductions/adapters.
3. Decoupled capabilities enabling multiple interchangeable providers.
4. Clean closed-world isolation testing for Gates A, B, C, D.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from pointer_algorithms.adv_graph.component_model import (
    CompositionNodeType, StateContract
)
from pointer_algorithms.strings.string_state_contracts import (
    make_border_array_state,
    make_z_array_state,
    make_rolling_hash_state,
    make_palindromic_radii_state,
    make_trie_automaton_state,
    make_aho_corasick_state,
    make_suffix_array_state,
    make_lcp_array_state,
    make_suffix_automaton_state,
    make_sam_transition_dag_state,
    make_lyndon_factorization_state,
    make_subsequence_automaton_state
)


@dataclass
class AlgorithmComponent:
    """
    Declarative capability model for an algorithm, primitive data structure, or transformation.
    """
    name: str
    node_type: CompositionNodeType = CompositionNodeType.COMPONENT
    category: str = "string"
    requires_states: List[StateContract] = field(default_factory=list)
    provides_states: List[StateContract] = field(default_factory=list)
    requires_capabilities: List[str] = field(default_factory=list)
    provided_capabilities: List[str] = field(default_factory=list)
    preconditions: List[str] = field(default_factory=list)
    proof_obligations: List[str] = field(default_factory=list)
    time_complexity: str = ""
    space_complexity: str = ""
    description: str = ""
    implementation_backend: str = ""

    # Compatibility aliases
    @property
    def consumes_state(self) -> List[StateContract]:
        return self.requires_states

    @property
    def produces_state(self) -> List[StateContract]:
        return self.provides_states

    @property
    def required_operations(self) -> List[str]:
        return self.requires_capabilities

    @property
    def complexity_time(self) -> str:
        return self.time_complexity

    @property
    def complexity_space(self) -> str:
        return self.space_complexity


class StringComponentRegistry:
    """
    Central registry for Phase 3O string algorithmic components and transformation adapters.
    """
    def __init__(self):
        self._components: Dict[str, AlgorithmComponent] = {}
        self._register_default_components()

    def register(self, component: AlgorithmComponent) -> None:
        self._components[component.name] = component

    def get(self, name: str) -> Optional[AlgorithmComponent]:
        return self._components.get(name)

    def remove(self, name: str) -> Optional[AlgorithmComponent]:
        return self._components.pop(name, None)

    def all_components(self) -> List[AlgorithmComponent]:
        return list(self._components.values())

    def _register_default_components(self) -> None:
        # ── 1. Border Array Builder (Failure Function pi) ──
        self.register(AlgorithmComponent(
            name="border_array_builder",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[StateContract("RawStringState")],
            provides_states=[make_border_array_state()],
            requires_capabilities=[],
            provided_capabilities=["BORDER_ARRAY_CONSTRUCTION", "PERIODICITY_ANALYSIS"],
            preconditions=["pattern_length_ge_1"],
            proof_obligations=["prefix_border_maximality_proven"],
            time_complexity="O(M)",
            space_complexity="O(M)",
            description="Computes KMP pi-table (longest proper prefix that is also suffix) in linear time."
        ))

        # ── 2. KMP Matcher (Deterministic Exact Matching) ──
        self.register(AlgorithmComponent(
            name="kmp_matcher",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[make_border_array_state(), StateContract("RawStringState")],
            provides_states=[StateContract("MatchOccurrencesState")],
            requires_capabilities=["BORDER_ARRAY_CONSTRUCTION"],
            provided_capabilities=["EXACT_SINGLE_PATTERN_MATCHING"],
            preconditions=["border_array_computed"],
            proof_obligations=["deterministic_no_false_negatives", "linear_time_amortized_bound"],
            time_complexity="O(N + M)",
            space_complexity="O(M)",
            description="Knuth-Morris-Pratt deterministic exact pattern matching via border transitions."
        ))

        # ── 3. Z-Algorithm Builder (Z-Box LCP) ──
        self.register(AlgorithmComponent(
            name="z_algorithm_builder",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[StateContract("RawStringState")],
            provides_states=[make_z_array_state()],
            requires_capabilities=[],
            provided_capabilities=["PREFIX_LCP_BOX_ANALYSIS", "EXACT_SINGLE_PATTERN_MATCHING"],
            preconditions=["concatenated_pattern_text_valid"],
            proof_obligations=["z_box_boundary_correctness_proven"],
            time_complexity="O(N + M)",
            space_complexity="O(N + M)",
            description="Linear-time Z-algorithm computing LCP of each suffix with entire string."
        ))

        # ── 4. Rolling Hash Builder (Rabin-Karp) ──
        self.register(AlgorithmComponent(
            name="rolling_hash_builder",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[StateContract("RawStringState")],
            provides_states=[make_rolling_hash_state(probabilistic=True)],
            requires_capabilities=[],
            provided_capabilities=["SUBSTRING_EQUALITY_LOOKUP", "EXACT_SINGLE_PATTERN_MATCHING"],
            preconditions=["prime_moduli_distinct_from_base"],
            proof_obligations=["collision_probability_bounded_below_1e_14"],
            time_complexity="Expected O(N + M)",
            space_complexity="O(1) auxiliary",
            description="Polynomial rolling hash engine using double large prime moduli (1e9+7, 1e9+9)."
        ))

        # ── 5. Manacher Engine (Palindromic Radii) ──
        self.register(AlgorithmComponent(
            name="manacher_engine",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[StateContract("RawStringState")],
            provides_states=[make_palindromic_radii_state()],
            requires_capabilities=[],
            provided_capabilities=["MAXIMAL_PALINDROME_DETECTION"],
            preconditions=["delimiter_symbol_not_in_alphabet"],
            proof_obligations=["palindromic_symmetry_reflection_proven"],
            time_complexity="O(N)",
            space_complexity="O(N)",
            description="Linear-time Manacher algorithm computing maximal palindromic radii around dummy separators."
        ))

        # ── 6. Trie Builder ──
        self.register(AlgorithmComponent(
            name="trie_builder",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[StateContract("DictionarySetState")],
            provides_states=[make_trie_automaton_state()],
            requires_capabilities=[],
            provided_capabilities=["PREFIX_TREE_INDEXING"],
            preconditions=["dictionary_non_empty"],
            proof_obligations=["prefix_sharing_uniqueness_proven"],
            time_complexity="DENSE_TABLE: O(sum(|P_i|) * |Sigma|) | SPARSE_ADJACENCY: O(sum(|P_i|) log |Sigma|)",
            space_complexity="DENSE_TABLE: O(sum(|P_i|) * |Sigma|) | SPARSE_ADJACENCY: O(sum(|P_i|))",
            description="Constructs a multi-string prefix tree (trie) over an alphabet with representation-dependent complexity."
        ))

        # ── 7. Failure Link Construction (Backend for Aho-Corasick) ──
        self.register(AlgorithmComponent(
            name="failure_link_construction",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[make_trie_automaton_state()],
            provides_states=[make_aho_corasick_state()],
            requires_capabilities=["PREFIX_TREE_INDEXING"],
            provided_capabilities=["FAILURE_LINK_CONSTRUCTION", "EXACT_MULTI_PATTERN_MATCHING"],
            preconditions=["trie_root_valid"],
            proof_obligations=["longest_proper_suffix_matching_proven"],
            time_complexity="DENSE_TABLE: O(sum(|P_i|) * |Sigma|) | SPARSE_ADJACENCY: O(sum(|P_i|) log |Sigma|)",
            space_complexity="DENSE_TABLE: O(sum(|P_i|) * |Sigma|) | SPARSE_ADJACENCY: O(sum(|P_i|))",
            description="Constructs Aho-Corasick suffix failure links and dictionary jump links."
        ))

        # ── 8. Suffix Array Prefix Doubling ──
        self.register(AlgorithmComponent(
            name="suffix_array_doubling",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[StateContract("RawStringState")],
            provides_states=[make_suffix_array_state(has_rank=True)],
            requires_capabilities=[],
            provided_capabilities=["SUFFIX_SORTING"],
            preconditions=["sentinel_character_minimal"],
            proof_obligations=["suffix_permutation_strictly_monotonic"],
            time_complexity="O(N log N) or O(N log^2 N)",
            space_complexity="O(N)",
            description="Constructs the sorted suffix permutation array via logarithmic prefix doubling."
        ))

        # ── 9. Kasai LCP Builder ──
        self.register(AlgorithmComponent(
            name="kasai_lcp_builder",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[make_suffix_array_state(has_rank=True), StateContract("RawStringState")],
            provides_states=[make_lcp_array_state()],
            requires_capabilities=["SUFFIX_SORTING"],
            provided_capabilities=["LCP_DERIVATION"],
            preconditions=["suffix_array_and_rank_valid"],
            proof_obligations=["kasai_monotonic_decrement_invariant_proven"],
            time_complexity="O(N)",
            space_complexity="O(N)",
            description="Computes the Longest Common Prefix (LCP) array in linear time using Kasai's theorem."
        ))

        # ── 10. Suffix Automaton Builder (SAM) ──
        self.register(AlgorithmComponent(
            name="sam_builder",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[StateContract("RawStringState")],
            provides_states=[make_suffix_automaton_state()],
            requires_capabilities=[],
            provided_capabilities=["MINIMAL_SUBSTRING_DFA_INDEXING", "DISTINCT_SUBSTRING_ANALYSIS"],
            preconditions=["online_character_stream_valid"],
            proof_obligations=["minimal_dfa_equivalence_proven", "linear_state_bound_le_2N"],
            time_complexity="DENSE_TABLE: O(N * |Sigma|) | SPARSE_ADJACENCY: O(N log |Sigma|) or O(N)",
            space_complexity="DENSE_TABLE: O(N * |Sigma|) | SPARSE_ADJACENCY: O(N)",
            description="Online construction of the minimal deterministic automaton recognizing all substrings with representation-dependent bounds."
        ))

        # ── 11. SAM Transition Graph Adapter (Transformation) ──
        # CRITICAL ARCHITECTURAL ADAPTER: Exposes SAM transition structure as a generic DAG!
        self.register(AlgorithmComponent(
            name="sam_transition_graph_adapter",
            node_type=CompositionNodeType.TRANSFORMATION,
            requires_states=[make_suffix_automaton_state()],
            provides_states=[make_sam_transition_dag_state(directed=True, acyclic=True)],
            requires_capabilities=["MINIMAL_SUBSTRING_DFA_INDEXING"],
            provided_capabilities=["SAM_DAG_PROJECTION"],
            preconditions=["sam_states_acyclic_under_length_order"],
            proof_obligations=["topological_precedence_preserved"],
            time_complexity="O(|V| + |E|)",
            space_complexity="O(|V| + |E|)",
            description="Explicit mathematical adapter projecting a Suffix Automaton transition structure into a generic DirectedAcyclicGraph."
        ))

        # ── 12. SAM Direct Distinct Substring Invariant (Mathematical Transformation) ──
        self.register(AlgorithmComponent(
            name="sam_direct_distinct_counter",
            node_type=CompositionNodeType.TRANSFORMATION,
            requires_states=[make_suffix_automaton_state()],
            provides_states=[StateContract("DistinctSubstringCountState")],
            requires_capabilities=["MINIMAL_SUBSTRING_DFA_INDEXING"],
            provided_capabilities=["DISTINCT_SUBSTRING_ANALYSIS"],
            preconditions=["sam_built_successfully"],
            proof_obligations=["sum_len_minus_link_equals_distinct_substrings"],
            time_complexity="O(|V|)",
            space_complexity="O(1)",
            description="Directly computes distinct substring count via sum(len[v] - len[link[v]]) invariant without DAG path counting."
        ))

        # ── 13. Suffix Array + LCP Distinct Substring Reducer (Transformation) ──
        self.register(AlgorithmComponent(
            name="sa_distinct_substring_counter",
            node_type=CompositionNodeType.TRANSFORMATION,
            requires_states=[make_suffix_array_state(), make_lcp_array_state()],
            provides_states=[StateContract("DistinctSubstringCountState")],
            requires_capabilities=["SUFFIX_SORTING", "LCP_DERIVATION"],
            provided_capabilities=["DISTINCT_SUBSTRING_ANALYSIS"],
            preconditions=["sa_and_lcp_lengths_equal"],
            proof_obligations=["n_choose_2_minus_sum_lcp_proven"],
            time_complexity="O(N)",
            space_complexity="O(1)",
            description="Computes distinct substrings via N*(N+1)/2 - sum(LCP) algebraic reduction."
        ))

        # ── 14. Duval's Lyndon Factorizer ──
        self.register(AlgorithmComponent(
            name="duval_factorizer",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[StateContract("RawStringState")],
            provides_states=[make_lyndon_factorization_state(non_increasing=True)],
            requires_capabilities=[],
            provided_capabilities=["LEXICOGRAPHICALLY_MINIMAL_ROTATION", "LYNDON_FACTORIZATION"],
            preconditions=["string_finite_length"],
            proof_obligations=["lyndon_duval_three_pointer_invariant_proven"],
            time_complexity="O(N)",
            space_complexity="O(1)",
            description="Duval's linear-time constant-space algorithm for Lyndon factorization and minimal string rotation."
        ))

        # ── 15. Subsequence Automaton Builder ──
        self.register(AlgorithmComponent(
            name="subseq_automaton_builder",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[StateContract("RawStringState")],
            provides_states=[make_subsequence_automaton_state()],
            requires_capabilities=[],
            provided_capabilities=["SUBSEQUENCE_AUTOMATON_QUERY"],
            preconditions=["alphabet_size_known"],
            proof_obligations=["next_occurrence_correctness_proven"],
            time_complexity="DENSE_TABLE: O(N * |Sigma| + Q * M) | SPARSE_ADJACENCY: O(N + Q * M log |Sigma|)",
            space_complexity="DENSE_TABLE: O(N * |Sigma|) | SPARSE_ADJACENCY: O(N)",
            description="Alphabet-agnostic next-occurrence table for O(|Q|) fast subsequence acceptance queries."
        ))

        # ── 16. SAM Longest Common Substring (Online Matcher) ──
        self.register(AlgorithmComponent(
            name="sam_lcs_matcher",
            node_type=CompositionNodeType.COMPONENT,
            requires_states=[make_suffix_automaton_state(), StateContract("RawStringState")],
            provides_states=[StateContract("LongestCommonSubstringState")],
            requires_capabilities=["MINIMAL_SUBSTRING_DFA_INDEXING"],
            provided_capabilities=["LONGEST_COMMON_SUBSTRING"],
            preconditions=["first_string_sam_valid"],
            proof_obligations=["sam_longest_common_substring_traversal_proven"],
            time_complexity="DENSE_TABLE: O(|S_1| * |Sigma| + |S_2|) | SPARSE_ADJACENCY: O((|S_1| + |S_2|) log |Sigma|)",
            space_complexity="DENSE_TABLE: O(|S_1| * |Sigma|) | SPARSE_ADJACENCY: O(|S_1|)",
            description="Traverses SAM of S_1 with characters of S_2 to find LCS in linear time with backend-dependent complexity."
        ))


def sam_transition_graph_adapter() -> AlgorithmComponent:
    return StringComponentRegistry().get("sam_transition_graph_adapter")


def sam_direct_distinct_counter() -> AlgorithmComponent:
    return StringComponentRegistry().get("sam_direct_distinct_counter")


def sa_distinct_substring_counter() -> AlgorithmComponent:
    return StringComponentRegistry().get("sa_distinct_substring_counter")

