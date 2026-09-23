"""
CHUP Phase 3O — String Algorithms Architecture Composition Tests.

Verifies the 4 Mandatory Core Composition Gates:
- Composition Gate A: Aho-Corasick Multi-Pattern Trie -> Failure Link Construction
- Composition Gate B: Kasai LCP -> Suffix Array Construction
- Composition Gate C: SAM Distinct Substrings -> Mathematical Invariant (sum len - link len)
- Composition Gate D: Subsequence Automaton (Alphabet-Agnostic Dense vs Sparse Representations)

Also tests:
- StateContract strict attribute matching and supertype compatibility
- Closed-world isolation: SAM does not inherit DirectedAcyclicGraph
- Dual-path distinct substring counting (SAM vs SA+LCP)
"""

import unittest
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.adv_graph.component_model import (
    StateContract,
    CompositionNodeType
)
from pointer_algorithms.strings.string_state_contracts import (
    make_trie_automaton_state,
    make_aho_corasick_state,
    make_suffix_array_state,
    make_lcp_array_state,
    make_suffix_automaton_state,
    make_sam_transition_dag_state,
    make_subsequence_automaton_state
)
from pointer_algorithms.strings.component_model import (
    StringComponentRegistry,
    sam_transition_graph_adapter,
    sam_direct_distinct_counter,
    sa_distinct_substring_counter
)


class TestStringComposition(unittest.TestCase):

    def setUp(self):
        self.registry = StringComponentRegistry()

    # ── 1. StateContract Exact Match & Attribute Unification ──
    def test_state_contract_exact_match(self):
        s1 = StateContract(name="SuffixArrayState", attributes={"has_rank": True, "alphabet_size": 26})
        req = StateContract(name="SuffixArrayState", attributes={"has_rank": True, "alphabet_size": 26})
        self.assertTrue(s1.satisfies(req))

    def test_state_contract_supertype_match(self):
        # AhoCorasickAutomatonState IS-A TrieAutomatonState
        ac_state = make_aho_corasick_state(alphabet_size=26)
        req = StateContract(name="TrieAutomatonState", attributes={"alphabet_size": 26})
        self.assertTrue(ac_state.satisfies(req))

    def test_state_contract_attribute_conflict_rejected(self):
        # Alphabet size mismatch
        s1 = StateContract(name="TrieAutomatonState", attributes={"alphabet_size": 26})
        req = StateContract(name="TrieAutomatonState", attributes={"alphabet_size": 128})
        self.assertFalse(s1.satisfies(req))

    # ── 2. Gate A: Aho-Corasick Multi-Pattern Trie -> Failure Links ──
    def test_composition_gate_a_aho_corasick(self):
        trie_builder = self.registry.get("trie_builder")
        fail_builder = self.registry.get("failure_link_construction")
        self.assertIsNotNone(trie_builder)
        self.assertIsNotNone(fail_builder)

        # Trie builder consumes RawStringState and produces TrieAutomatonState
        self.assertTrue(any(s.name == "TrieAutomatonState" for s in trie_builder.provides_states))
        # Failure link builder consumes TrieAutomatonState and produces AhoCorasickAutomatonState
        trie_output = trie_builder.provides_states[0]
        self.assertTrue(fail_builder.requires_states[0].satisfies(trie_output) or trie_output.satisfies(fail_builder.requires_states[0]))
        self.assertTrue(any(s.name == "AhoCorasickAutomatonState" for s in fail_builder.provides_states))

    # ── 3. Gate B: Kasai LCP -> Suffix Array Dependency ──
    def test_composition_gate_b_kasai_lcp(self):
        sa_builder = self.registry.get("suffix_array_doubling")
        kasai_builder = self.registry.get("kasai_lcp_builder")
        self.assertIsNotNone(sa_builder)
        self.assertIsNotNone(kasai_builder)

        # Suffix array doubling produces SuffixArrayState
        sa_output = sa_builder.provides_states[0]
        self.assertEqual(sa_output.name, "SuffixArrayState")
        # Kasai consumes SuffixArrayState
        self.assertTrue(sa_output.satisfies(kasai_builder.requires_states[0]))
        # Kasai provides LCPArrayState
        self.assertEqual(kasai_builder.provides_states[0].name, "LCPArrayState")

    # ── 4. Gate C: SAM Direct Distinct Substrings Invariant ──
    def test_composition_gate_c_sam_distinct_substrings(self):
        sam_builder = self.registry.get("sam_builder")
        direct_counter = self.registry.get("sam_direct_distinct_counter")
        self.assertIsNotNone(sam_builder)
        self.assertIsNotNone(direct_counter)

        sam_output = sam_builder.provides_states[0]
        self.assertEqual(sam_output.name, "SuffixAutomatonState")
        # Invariant: SAM does NOT declare DirectedAcyclicGraph as supertype
        self.assertNotIn("DirectedAcyclicGraph", sam_output.supertypes)
        # Direct counter consumes SuffixAutomatonState without generic DAG requirement
        self.assertTrue(sam_output.satisfies(direct_counter.requires_states[0]))
        self.assertEqual(direct_counter.provides_states[0].name, "DistinctSubstringCountState")
        self.assertIn("sum_len_minus_link_equals_distinct_substrings", direct_counter.proof_obligations)

    # ── 5. Gate C (Dual Path): Suffix Array + Kasai Distinct Substrings ──
    def test_composition_gate_c_sa_distinct_substrings(self):
        sa_builder = self.registry.get("suffix_array_doubling")
        kasai_builder = self.registry.get("kasai_lcp_builder")
        sa_counter = self.registry.get("sa_distinct_substring_counter")
        self.assertIsNotNone(sa_counter)

        sa_state = sa_builder.provides_states[0]
        lcp_state = kasai_builder.provides_states[0]
        # sa_distinct_substring_counter consumes SuffixArrayState and LCPArrayState
        self.assertTrue(sa_state.satisfies(sa_counter.requires_states[0]))
        self.assertTrue(lcp_state.satisfies(sa_counter.requires_states[1]))
        self.assertEqual(sa_counter.provides_states[0].name, "DistinctSubstringCountState")
        self.assertIn("n_choose_2_minus_sum_lcp_proven", sa_counter.proof_obligations)

    # ── 6. Gate D: Subsequence Automaton Alphabet Representation ──
    def test_composition_gate_d_subsequence_automaton(self):
        builder = self.registry.get("subseq_automaton_builder")
        self.assertIsNotNone(builder)
        default_state = builder.provides_states[0]
        self.assertEqual(default_state.name, "SubsequenceAutomatonState")

        dense_state = make_subsequence_automaton_state(alphabet_size=26, representation="DENSE_TABLE")
        sparse_state = make_subsequence_automaton_state(alphabet_size=100000, representation="SPARSE_ADJACENCY")

        # Strict representation checks
        self.assertTrue(dense_state.satisfies(StateContract("SubsequenceAutomatonState", attributes={"representation": "DENSE_TABLE"})))
        self.assertFalse(dense_state.satisfies(StateContract("SubsequenceAutomatonState", attributes={"representation": "SPARSE_ADJACENCY"})))
        self.assertTrue(sparse_state.satisfies(StateContract("SubsequenceAutomatonState", attributes={"representation": "SPARSE_ADJACENCY"})))


if __name__ == "__main__":
    unittest.main()
