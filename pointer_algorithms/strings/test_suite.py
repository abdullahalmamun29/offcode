"""
Comprehensive Unit Test Suite for CHUP Phase 3O: String Algorithms & Automata.

Validates:
1. Semantic ontology & orthogonal primitive representation
2. Derived facts & provenance records (PROVEN status, rule tracking)
3. StateContract strict semantic substitutability (positive match, supertype match, attribute conflict rejection)
4. Suffix Automaton State Contract isolation (SAM does NOT inherit DirectedAcyclicGraph)
5. Suffix Automaton Transition Graph Adapter (mediates DirectedAcyclicGraph projection)
6. Closed-world Gate A: Aho-Corasick requires TrieAutomatonState & FailureLinkConstruction
7. Closed-world Gate B: Kasai LCP requires valid SuffixArrayState
8. Closed-world Gate C: SAM distinct-substring counting uses direct math invariant via DistinctSubstringCountingCapability
9. Closed-world Gate D: Subsequence Automaton alphabet representation (dense vs sparse)
10. Candidate status preservation: Rabin-Karp is VALID_SUBOPTIMAL (probabilistic) vs KMP VALID_OPTIMAL (deterministic)
11. Candidate status preservation: Z-algorithm is VALID_SUBOPTIMAL for single pattern search
12. Duval Lyndon factorization & minimal rotation derivation
13. 4-phase formal invariants for all 10 string patterns in InvariantEngine
14. Formal movement derivations and elimination proofs in MovementDerivationEngine
15-24. C++ generator dispatch and code generation for all 10 string patterns
25. Bridge integration with handle_request() for string problems
26. String candidate eliminator overrides generic fallbacks
"""

import unittest
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.knowledge.taxonomy import (
    PatternKind,
    STRING_PATTERNS
)
from pointer_algorithms.strings.semantic_ontology import (
    AlphabetDomain,
    SequenceMultiplicity,
    StringSymmetry,
    CorrectnessGuarantee,
    ComplexityContract,
    TransitionRepresentation,
    StringObjective,
    DerivedFact,
    ProvenanceStatus,
    SemanticStringModel
)
from pointer_algorithms.adv_graph.component_model import (
    StateContract,
    CompositionNodeType
)
from pointer_algorithms.strings.component_model import (
    AlgorithmComponent,
    StringComponentRegistry,
    sam_transition_graph_adapter,
    sam_direct_distinct_counter,
    sa_distinct_substring_counter
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
from pointer_algorithms.strings.derivation_engine import (
    StringDerivationEngine,
    CandidateStatus,
    SelectionStatus,
    StringCandidateEvaluation
)
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine
from pointer_algorithms.generator.cpp_generator import CppPointerGenerator
from pointer_algorithms.recognition.candidate_generator import AlgorithmCandidate
from pointer_algorithms.recognition.candidate_eliminator import CandidateEliminator
from pointer_algorithms.recognition.feature_extractor import ProblemFeatures, FeatureExtractor
from pointer_algorithms.bridge import handle_request


class TestPhase3OStringAlgorithms(unittest.TestCase):

    def test_01_ontology_primitive_orthogonality(self):
        """Test that all ontology dimensions are orthogonal, disjoint, and non-overlapping."""
        self.assertEqual(AlphabetDomain.LOWERCASE_LATIN.value, "LOWERCASE_LATIN")
        self.assertEqual(AlphabetDomain.ASCII_STANDARD.value, "ASCII_STANDARD")
        self.assertEqual(AlphabetDomain.ASCII.value, "ASCII")
        self.assertEqual(AlphabetDomain.BYTE_ALPHABET.value, "BYTE_ALPHABET")
        self.assertEqual(SequenceMultiplicity.SINGLE_STRING.value, "SINGLE_STRING")
        self.assertEqual(SequenceMultiplicity.DICTIONARY_SET.value, "DICTIONARY_SET")
        self.assertEqual(StringSymmetry.PALINDROMIC.value, "PALINDROMIC")
        self.assertEqual(CorrectnessGuarantee.DETERMINISTIC_EXACT.value, "DETERMINISTIC_EXACT")
        self.assertEqual(CorrectnessGuarantee.PROBABILISTIC_COLLISION_BOUNDED.value, "PROBABILISTIC_COLLISION_BOUNDED")
        self.assertEqual(CorrectnessGuarantee.MONTE_CARLO_BOUNDED_ERROR.value, "MONTE_CARLO_BOUNDED_ERROR")
        self.assertEqual(CorrectnessGuarantee.DETERMINISTIC.value, "DETERMINISTIC")
        self.assertEqual(CorrectnessGuarantee.PROBABILISTIC.value, "PROBABILISTIC")
        self.assertEqual(ComplexityContract.WORST_CASE.value, "WORST_CASE")
        self.assertEqual(ComplexityContract.EXPECTED.value, "EXPECTED")
        self.assertEqual(TransitionRepresentation.DENSE_TABLE.value, "DENSE_TABLE")
        self.assertEqual(TransitionRepresentation.SPARSE_ADJACENCY.value, "SPARSE_ADJACENCY")
        self.assertEqual(StringObjective.EXACT_SINGLE_PATTERN_MATCHING.value, "EXACT_SINGLE_PATTERN_MATCHING")
        self.assertEqual(StringObjective.DISTINCT_SUBSTRING_ANALYSIS.value, "DISTINCT_SUBSTRING_ANALYSIS")

    def test_02_derived_facts_and_provenance(self):
        """Test provenance tracking and derivation rule logging."""
        model = SemanticStringModel()
        model.add_derived_property(
            fact_id="DETERMINISTIC_STREAMING_COMPATIBLE",
            value=True,
            source_facts=["BORDER_ARRAY_AVAILABLE", "WORST_CASE_TIME_BOUNDED"],
            rule="KMP_STREAMING_DETERMINISM",
            obligations=["amortized_linear_time_proven"]
        )
        self.assertIn("DETERMINISTIC_STREAMING_COMPATIBLE", model.derived_properties)
        self.assertTrue(model.derived_properties["DETERMINISTIC_STREAMING_COMPATIBLE"])
        self.assertEqual(len(model.provenance_records), 1)
        record = model.provenance_records[0]
        self.assertEqual(record.status, ProvenanceStatus.PROVEN)
        self.assertEqual(record.derivation_rule, "KMP_STREAMING_DETERMINISM")
        self.assertEqual(record.proof_obligations, ["amortized_linear_time_proven"])

    def test_03_state_contract_strict_substitutability(self):
        """Test StateContract strict attribute matching and supertype satisfaction."""
        state = make_aho_corasick_state(alphabet_size=26)
        # Exact name match
        self.assertTrue(state.satisfies(StateContract("AhoCorasickAutomatonState")))
        # Supertype match (AhoCorasickAutomatonState IS-A TrieAutomatonState)
        self.assertTrue(state.satisfies(StateContract("TrieAutomatonState")))
        # Attribute matching
        self.assertTrue(state.satisfies(StateContract("TrieAutomatonState", attributes={"alphabet_size": 26})))
        # Attribute mismatch rejection
        self.assertFalse(state.satisfies(StateContract("TrieAutomatonState", attributes={"alphabet_size": 128})))
        # Unrelated type rejection
        self.assertFalse(state.satisfies(StateContract("SuffixArrayState")))

    def test_04_suffix_automaton_state_contract_isolation(self):
        """Test SAM is isolated and does NOT inherit DirectedAcyclicGraph."""
        sam_state = make_suffix_automaton_state(alphabet_size=26)
        self.assertEqual(sam_state.name, "SuffixAutomatonState")
        # Critical architectural invariant: SAM must NOT declare DirectedAcyclicGraph as supertype
        self.assertNotIn("DirectedAcyclicGraph", sam_state.supertypes)
        self.assertFalse(sam_state.satisfies(StateContract("DirectedAcyclicGraph")))

    def test_05_sam_transition_graph_adapter_projection(self):
        """Test SAMTransitionGraphAdapter projects SAM into a DAG state."""
        adapter = sam_transition_graph_adapter()
        self.assertEqual(adapter.node_type, CompositionNodeType.TRANSFORMATION)
        self.assertEqual(adapter.requires_states[0].name, "SuffixAutomatonState")
        self.assertEqual(adapter.provides_states[0].name, "SAMTransitionDAG")
        # Projected state satisfies DirectedAcyclicGraph
        projected = make_sam_transition_dag_state()
        self.assertTrue(projected.satisfies(StateContract("DirectedAcyclicGraph")))
        self.assertIn("DirectedAcyclicGraph", projected.supertypes)

    def test_06_gate_a_aho_corasick_requirements(self):
        """Test Closed-World Gate A: Aho-Corasick requires TrieAutomatonState and FailureLinkConstruction."""
        registry = StringComponentRegistry()
        ac_builder = registry.get("failure_link_construction")
        self.assertIsNotNone(ac_builder)
        req_state_names = [s.name for s in ac_builder.requires_states]
        self.assertIn("TrieAutomatonState", req_state_names)
        self.assertIn("PREFIX_TREE_INDEXING", ac_builder.requires_capabilities)
        self.assertIn("FAILURE_LINK_CONSTRUCTION", ac_builder.provided_capabilities)

    def test_07_gate_b_kasai_lcp_requires_suffix_array(self):
        """Test Closed-World Gate B: Kasai LCP requires valid SuffixArrayState."""
        registry = StringComponentRegistry()
        kasai = registry.get("kasai_lcp_builder")
        self.assertIsNotNone(kasai)
        req_state_names = [s.name for s in kasai.requires_states]
        self.assertIn("SuffixArrayState", req_state_names)
        self.assertIn("LCPArrayState", [s.name for s in kasai.provides_states])

    def test_08_gate_c_sam_distinct_substrings_direct_math(self):
        """Test Closed-World Gate C: SAM distinct-substring counting uses math invariant directly."""
        direct_counter = sam_direct_distinct_counter()
        self.assertEqual(direct_counter.node_type, CompositionNodeType.TRANSFORMATION)
        self.assertIn("DISTINCT_SUBSTRING_ANALYSIS", direct_counter.provided_capabilities)
        self.assertIn("sum_len_minus_link_equals_distinct_substrings", direct_counter.proof_obligations)
        # Does NOT require generic DAG path counter
        self.assertEqual(direct_counter.requires_states[0].name, "SuffixAutomatonState")
        self.assertNotIn("DirectedAcyclicGraph", [s.name for s in direct_counter.requires_states])

    def test_09_gate_d_subsequence_automaton_representations(self):
        """Test Closed-World Gate D: Subsequence Automaton alphabet representation support."""
        dense_state = make_subsequence_automaton_state(alphabet_size=26, representation="DENSE_TABLE")
        self.assertEqual(dense_state.attributes["representation"], "DENSE_TABLE")
        sparse_state = make_subsequence_automaton_state(alphabet_size=100000, representation="SPARSE_ADJACENCY")
        self.assertEqual(sparse_state.attributes["representation"], "SPARSE_ADJACENCY")
        self.assertTrue(dense_state.satisfies(StateContract("SubsequenceAutomatonState", attributes={"representation": "DENSE_TABLE"})))
        self.assertFalse(dense_state.satisfies(StateContract("SubsequenceAutomatonState", attributes={"representation": "SPARSE_ADJACENCY"})))

    def test_10_candidate_status_preservation_kmp_vs_rabin_karp(self):
        """Test deterministic KMP is VALID_OPTIMAL while probabilistic Rabin-Karp is preserved as VALID_SUBOPTIMAL."""
        engine = StringDerivationEngine()
        model = engine.extract_semantic_model("Find occurrences of pattern P in text T exactly.")
        cands, selected = engine.evaluate_candidates(model)
        self.assertEqual(selected, PatternKind.STRING_KMP_SEARCH.value)

        cand_map = {c.pattern: c for c in cands}
        self.assertIn(PatternKind.STRING_KMP_SEARCH.value, cand_map)
        self.assertEqual(cand_map[PatternKind.STRING_KMP_SEARCH.value].status, CandidateStatus.VALID_OPTIMAL)
        self.assertEqual(cand_map[PatternKind.STRING_KMP_SEARCH.value].selection, SelectionStatus.SELECTED)

        self.assertIn(PatternKind.STRING_RABIN_KARP.value, cand_map)
        self.assertEqual(cand_map[PatternKind.STRING_RABIN_KARP.value].status, CandidateStatus.VALID_SUBOPTIMAL)
        self.assertEqual(cand_map[PatternKind.STRING_RABIN_KARP.value].selection, SelectionStatus.NOT_SELECTED)

    def test_11_candidate_status_preservation_z_algorithm(self):
        """Test Z-algorithm is preserved as VALID_SUBOPTIMAL for single pattern search."""
        engine = StringDerivationEngine()
        model = engine.extract_semantic_model("Find occurrences of pattern P in text T.")
        cands, _ = engine.evaluate_candidates(model)
        cand_map = {c.pattern: c for c in cands}
        self.assertIn(PatternKind.STRING_Z_ALGORITHM.value, cand_map)
        self.assertEqual(cand_map[PatternKind.STRING_Z_ALGORITHM.value].status, CandidateStatus.VALID_SUBOPTIMAL)

    def test_12_duval_lyndon_factorization_derivation(self):
        """Test Duval Lyndon factorizer selection for minimal rotation and Lyndon factorization."""
        engine = StringDerivationEngine()
        model = engine.extract_semantic_model("Find the lexicographically minimal rotation of string S via Lyndon factorization.")
        cands, selected = engine.evaluate_candidates(model)
        self.assertEqual(selected, PatternKind.STRING_LYNDON_DUVAL.value)
        cand_map = {c.pattern: c for c in cands}
        self.assertEqual(cand_map[PatternKind.STRING_LYNDON_DUVAL.value].status, CandidateStatus.VALID_OPTIMAL)

    def test_13_invariant_engine_all_10_string_patterns(self):
        """Test formal 4-phase invariants for all 10 string patterns in InvariantEngine."""
        for pat in STRING_PATTERNS:
            inv = InvariantEngine.construct_invariant(pat, {})
            self.assertEqual(inv.pattern, pat)
            self.assertTrue(len(inv.before_iteration) > 0, f"Missing before_iteration for {pat}")
            self.assertTrue(len(inv.during_iteration) > 0, f"Missing during_iteration for {pat}")
            self.assertTrue(len(inv.after_movement) > 0, f"Missing after_movement for {pat}")
            self.assertTrue(len(inv.at_termination) > 0, f"Missing at_termination for {pat}")

    def test_14_movement_derivation_all_10_string_patterns(self):
        """Test formal movement derivations and elimination proofs for all 10 string patterns."""
        for pat in STRING_PATTERNS:
            m = MovementDerivationEngine.derive(pat, {})
            self.assertEqual(m.pattern, pat)
            self.assertTrue(len(m.objective_function) > 0, f"Missing objective for {pat}")
            self.assertTrue(len(m.decision_conditions) > 0, f"Missing decision conditions for {pat}")
            self.assertTrue(len(m.elimination_proof) > 0, f"Missing elimination proof for {pat}")
            self.assertTrue(len(m.state_updates) > 0, f"Missing state updates for {pat}")

    def test_15_cpp_generator_kmp(self):
        """Test C++ code generator for KMP search."""
        code = CppPointerGenerator.generate(PatternKind.STRING_KMP_SEARCH.value, {})
        self.assertIn("vector<int> compute_pi(const string& p)", code)
        self.assertIn("matches.push_back(i - m + 1);", code)

    def test_16_cpp_generator_z_algorithm(self):
        """Test C++ code generator for Z-algorithm."""
        code = CppPointerGenerator.generate(PatternKind.STRING_Z_ALGORITHM.value, {})
        self.assertIn("vector<int> compute_z(const string& s)", code)
        self.assertIn("z[0] = n;", code)

    def test_17_cpp_generator_rabin_karp(self):
        """Test C++ code generator for Rabin-Karp."""
        code = CppPointerGenerator.generate(PatternKind.STRING_RABIN_KARP.value, {})
        self.assertIn("MOD1", code)
        self.assertIn("BASE1", code)
        self.assertIn("vector<ll> h1", code)

    def test_18_cpp_generator_manacher(self):
        """Test C++ code generator for Manacher."""
        code = CppPointerGenerator.generate(PatternKind.STRING_MANACHER.value, {})
        self.assertIn('t += "#"', code)
        self.assertIn("int i_mirror = 2 * c - i;", code)
        self.assertIn("max_len", code)

    def test_19_cpp_generator_aho_corasick(self):
        """Test C++ code generator for Aho-Corasick."""
        code = CppPointerGenerator.generate(PatternKind.STRING_AHO_CORASICK.value, {})
        self.assertIn("struct Node", code)
        self.assertIn("dict_link", code)
        self.assertIn("trie[v].pattern_ids", code)

    def test_20_cpp_generator_suffix_array(self):
        """Test C++ code generator for Suffix Array and Kasai LCP."""
        code = CppPointerGenerator.generate(PatternKind.STRING_SUFFIX_ARRAY.value, {})
        self.assertIn("vector<int> sa(n), rank(n);", code)
        self.assertIn("Kasai LCP calculation", code)
        self.assertIn("lcp[r - 1] = h;", code)

    def test_21_cpp_generator_suffix_automaton(self):
        """Test C++ code generator for Suffix Automaton."""
        code = CppPointerGenerator.generate(PatternKind.STRING_SUFFIX_AUTOMATON.value, {})
        self.assertIn("struct State", code)
        self.assertIn("st[cur].link", code)
        self.assertIn("distinct_count", code)

    def test_22_cpp_generator_lyndon_duval(self):
        """Test C++ code generator for Duval Lyndon factorization."""
        code = CppPointerGenerator.generate(PatternKind.STRING_LYNDON_DUVAL.value, {})
        self.assertIn("minimal_rotation", code)
        self.assertIn("s[k] <= s[j]", code)

    def test_23_cpp_generator_subsequence_automaton(self):
        """Test C++ code generator for Subsequence Automaton."""
        code = CppPointerGenerator.generate(PatternKind.STRING_SUBSEQUENCE_AUTOMATON.value, {})
        self.assertIn("next_pos", code)
        self.assertIn("next_pos[cur][char_idx]", code)

    def test_24_cpp_generator_sam_lcs(self):
        """Test C++ code generator for SAM Longest Common Substring."""
        code = CppPointerGenerator.generate(PatternKind.STRING_LONGEST_COMMON_SUBSTRING_SAM.value, {})
        self.assertIn("st[v].link", code)
        self.assertIn("s2.substr", code)

    def test_25_bridge_end_to_end_string_request(self):
        """Test bridge.handle_request end-to-end integration for string algorithms."""
        req = {
            "problemText": "Find all occurrences of pattern in text using Knuth-Morris-Pratt prefix function pi table."
        }
        resp = handle_request(req)
        self.assertEqual(resp.get("status"), "success")
        self.assertEqual(resp.get("family"), "string")
        self.assertEqual(resp.get("selectedPattern"), PatternKind.STRING_KMP_SEARCH.value)
        self.assertIn("string", resp)
        self.assertTrue(resp["string"]["detected"])
        self.assertTrue(len(resp.get("code", "")) > 50)

    def test_26_candidate_eliminator_generic_fallback_override(self):
        """Test that CandidateEliminator eliminates generic fallbacks when string algorithm is detected."""
        cand = AlgorithmCandidate(
            pattern="graph_shortest_path_or_scc",
            family="graph",
            confidence_prior=0.5,
            supporting_signals=["graph_test"]
        )
        features = FeatureExtractor.extract("Find pattern occurrences in text")
        features.is_string_algorithm_detected = True
        features.string_algorithm_family = "string_kmp_search"

        eval_res = CandidateEliminator.evaluate_candidate(cand, features)
        self.assertFalse(eval_res.accepted)
        self.assertEqual(eval_res.rejection_code, "STRING_SPECIFIC_ALGORITHM_RESOLVED")
        self.assertEqual(eval_res.recommended_alternative, "string_kmp_search")


if __name__ == "__main__":
    unittest.main()
