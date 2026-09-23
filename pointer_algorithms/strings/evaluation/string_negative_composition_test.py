"""
CHUP Phase 3O — String Negative Composition Tests (Anti-Hardcoding & Leakage Gates).

Validates:
1. Anti-hardcoding Invariant Gate A: Removal of Trie builder breaks Aho-Corasick pipeline.
2. Anti-hardcoding Invariant Gate B: Removal of Suffix Array builder breaks Kasai LCP pipeline.
3. SAM State Leakage Invariant: SAM state directly cannot satisfy a generic DAG requirement without adapter.
4. Anti-hardcoding Invariant Gate C: Removal of SAM builder prevents SAM distinct substring counting.
5. Representation Conflict Gate D: Dense-only automaton state cannot satisfy sparse contract requirement.
6. Unsatisfiable Goal Rejection: Completely unsupported state requirements fail closed.
"""

import unittest
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.adv_graph.component_model import StateContract
from pointer_algorithms.strings.string_state_contracts import (
    make_suffix_automaton_state,
    make_subsequence_automaton_state
)
from pointer_algorithms.strings.component_model import (
    StringComponentRegistry,
    sam_transition_graph_adapter
)


class TestStringNegativeComposition(unittest.TestCase):

    def setUp(self):
        self.registry = StringComponentRegistry()

    def test_01_negative_gate_a_missing_trie(self):
        """Removing trie_builder means failure_link_construction cannot find provider for TrieAutomatonState."""
        self.registry.remove("trie_builder")
        ac_builder = self.registry.get("failure_link_construction")
        self.assertIsNotNone(ac_builder)
        req_state = ac_builder.requires_states[0]

        # No remaining base component produces TrieAutomatonState from RawStringState
        providers = [c for c in self.registry.all_components() if c.name != "failure_link_construction" and any(s.satisfies(req_state) for s in c.provides_states)]
        self.assertEqual(len(providers), 0)

    def test_02_negative_gate_b_missing_suffix_array(self):
        """Removing suffix_array_doubling means kasai_lcp_builder has no provider for SuffixArrayState."""
        self.registry.remove("suffix_array_doubling")
        kasai = self.registry.get("kasai_lcp_builder")
        self.assertIsNotNone(kasai)
        req_state = kasai.requires_states[0]

        providers = [c for c in self.registry.all_components() if any(s.satisfies(req_state) for s in c.provides_states)]
        self.assertEqual(len(providers), 0)

    def test_03_negative_gate_c_sam_dag_leakage(self):
        """SAM state must NOT satisfy DirectedAcyclicGraph without adapter mediation."""
        sam_state = make_suffix_automaton_state()
        dag_req = StateContract("DirectedAcyclicGraph")
        self.assertFalse(sam_state.satisfies(dag_req), "SAM must NOT directly satisfy DirectedAcyclicGraph!")

        # Only after adapter transformation can it satisfy DAG requirement
        adapter = sam_transition_graph_adapter()
        projected = adapter.provides_states[0]
        self.assertTrue(projected.satisfies(dag_req), "Projected SAM transition DAG must satisfy DirectedAcyclicGraph!")

    def test_04_negative_gate_c_missing_sam_builder(self):
        """Removing sam_builder means sam_direct_distinct_counter has no provider for SuffixAutomatonState."""
        self.registry.remove("sam_builder")
        counter = self.registry.get("sam_direct_distinct_counter")
        self.assertIsNotNone(counter)
        req_state = counter.requires_states[0]

        providers = [c for c in self.registry.all_components() if any(s.satisfies(req_state) for s in c.provides_states)]
        self.assertEqual(len(providers), 0)

    def test_05_negative_gate_d_representation_conflict(self):
        """A dense table representation cannot satisfy a sparse adjacency requirement."""
        dense_state = make_subsequence_automaton_state(alphabet_size=26, representation="DENSE_TABLE")
        sparse_req = StateContract("SubsequenceAutomatonState", attributes={"representation": "SPARSE_ADJACENCY"})
        self.assertFalse(dense_state.satisfies(sparse_req))

    def test_06_negative_unsatisfiable_goal_rejection(self):
        """Unsupported state contract goals have zero providers in the registry."""
        impossible_goal = StateContract("GeneralizedCompressedSuffixTreeState")
        providers = [c for c in self.registry.all_components() if any(s.satisfies(impossible_goal) for s in c.provides_states)]
        self.assertEqual(len(providers), 0)


if __name__ == "__main__":
    unittest.main()
