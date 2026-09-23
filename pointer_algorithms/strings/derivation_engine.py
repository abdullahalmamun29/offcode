"""
CHUP Phase 3O — String Semantic Derivation & Candidate Evaluation Engine.

Translates problem statements into SemanticStringModel with mathematical provenance,
evaluates competing candidates while preserving VALID_OPTIMAL vs VALID_SUBOPTIMAL distinction,
and synthesizes composition execution plans.
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set, Tuple

from pointer_algorithms.strings.semantic_ontology import (
    AlphabetDomain, SequenceMultiplicity, StringSymmetry, CorrectnessGuarantee,
    ComplexityContract, TransitionRepresentation, StringObjective,
    DerivedFact, ProvenanceStatus, SemanticStringModel
)
from pointer_algorithms.adv_graph.composition_engine import (
    CandidateStatus, SelectionStatus, CompositionPlan, CompositionFailureCategory
)
from pointer_algorithms.strings.component_model import (
    StringComponentRegistry, AlgorithmComponent
)


@dataclass
class StringCandidateEvaluation:
    pattern: str
    component_name: str
    status: CandidateStatus
    selection: SelectionStatus
    rejection_code: Optional[str] = None
    evidence: str = ""
    complexity: str = ""
    justification: str = ""


class StringDerivationEngine:
    """
    Parses natural language into a SemanticStringModel, deduces derived properties,
    evaluates competing string candidates, and synthesizes dependency plans.
    """

    def __init__(self, registry: Optional[StringComponentRegistry] = None):
        self.registry = registry or StringComponentRegistry()

    def extract_semantic_model(self, text: str) -> SemanticStringModel:
        lower = text.lower()
        model = SemanticStringModel()

        # ── 1. Alphabet Domain ──
        if re.search(r'binary\s+string|alphabet\s*=\s*\{0,\s*1\}|only\s+0\s+and\s+1|bits?\s+sequence', lower):
            model.alphabet_domain = AlphabetDomain.BINARY
            model.alphabet_size = 2
        elif re.search(r'uppercase|\[A-Z\]', text):
            model.alphabet_domain = AlphabetDomain.UPPERCASE_LATIN
            model.alphabet_size = 26
        elif re.search(r'alphanumeric|letters\s+and\s+digits', lower):
            model.alphabet_domain = AlphabetDomain.ALPHANUMERIC
            model.alphabet_size = 62
        elif re.search(r'bytes?|octets?|extended\s+ascii|raw\s+bytes?', lower):
            model.alphabet_domain = AlphabetDomain.BYTE_ALPHABET
            model.alphabet_size = 256
        elif re.search(r'ascii|arbitrary\s+characters|full\s+character\s+set', lower):
            model.alphabet_domain = AlphabetDomain.ASCII_STANDARD
            model.alphabet_size = 128
        elif re.search(r'integer\s+alphabet|numeric\s+tokens|array\s+of\s+integers\s+as\s+characters', lower):
            model.alphabet_domain = AlphabetDomain.GENERAL_INTEGER_ALPHABET
            model.transition_representation = TransitionRepresentation.SPARSE_ADJACENCY
        else:
            model.alphabet_domain = AlphabetDomain.LOWERCASE_LATIN
            model.alphabet_size = 26

        # ── 2. Sequence Multiplicity ──
        if re.search(r'dictionary|set\s+of\s+keywords|multiple\s+patterns?|list\s+of\s+words?|collection\s+of\s+strings?', lower):
            model.sequence_multiplicity = SequenceMultiplicity.DICTIONARY_SET
        elif re.search(r'two\s+strings?|pair\s+of\s+strings?|common\s+to\s+both\s+strings?', lower):
            model.sequence_multiplicity = SequenceMultiplicity.PAIR_OF_STRINGS
        elif re.search(r'pattern\s+p\s+in\s+text\s+t|find\s+pattern|search\s+for\s+needle|occurrences?\s+of\s+pattern', lower):
            model.sequence_multiplicity = SequenceMultiplicity.TEXT_AND_PATTERN
        else:
            model.sequence_multiplicity = SequenceMultiplicity.SINGLE_STRING

        # ── 3. Structural Symmetries & Provenance ──
        if re.search(r'palindrome|palindromic|reads\s+the\s+same\s+backwards', lower):
            model.string_symmetry = StringSymmetry.PALINDROMIC
            model.add_derived_property(
                "is_palindromic", True, ["text:palindrome_evidence"],
                "palindromic_symmetry_derivation",
                ["S[i] == S[n-1-i] for all 0 <= i < n"]
            )

        if re.search(r'period(?:ic)?|repeating\s+pattern|formed\s+by\s+repeating|k\s+times\s+repetition', lower):
            model.string_symmetry = StringSymmetry.PERIODIC
            model.add_derived_property(
                "is_periodic", True, ["text:periodicity_evidence"],
                "periodicity_border_derivation",
                ["n % (n - pi[n-1]) == 0", "pi[n-1] > 0"]
            )

        if re.search(r'border|prefix\s+that\s+is\s+also\s+(?:a\s+)?suffix|longest\s+proper\s+prefix', lower):
            model.string_symmetry = StringSymmetry.BORDERED
            model.add_derived_property(
                "has_border", True, ["text:border_evidence"],
                "prefix_suffix_border_derivation",
                ["pi[n-1] > 0"]
            )

        # ── 4. Atomic String Objectives ──
        if re.search(r'longest\s+common\s+(?:contiguous\s+)?substring|common\s+(?:contiguous\s+)?substring|lcs\s+substring', lower):
            model.string_objective = StringObjective.LONGEST_COMMON_SUBSTRING
        elif re.search(r'minimal\s+(?:string\s+)?rotation|lexicographically\s+(?:smallest|minimal)\s+(?:cyclic\s+)?(?:shift|rotation)|canonical\s+shift|booth|duval|lyndon|cyclic\s+shift', lower):
            model.string_objective = StringObjective.LEXICOGRAPHICALLY_MINIMAL_ROTATION
        elif re.search(r'(?:count|number\s+of|total)?\s*(?:distinct|unique|different)\s+substrings?', lower):
            model.string_objective = StringObjective.DISTINCT_SUBSTRING_ANALYSIS
        elif re.search(r'aho[- ]corasick|multi[- ]pattern\s+search|dictionary\s+matching|find\s+all\s+words\s+from\s+dictionary', lower):
            model.string_objective = StringObjective.EXACT_MULTI_PATTERN_MATCHING
            model.sequence_multiplicity = SequenceMultiplicity.DICTIONARY_SET
        elif re.search(r'subsequence\s+automaton|next[- ]occurrence\s+automaton|subsequence\s+queries|queries\s+asking\s+if\s+.*is\s+a\s+subsequence|fast\s+subsequence\s+testing|next\s+array', lower):
            model.string_objective = StringObjective.SUBSEQUENCE_AUTOMATON_QUERY
        elif re.search(r'manacher|longest\s+palindromic\s+substring|count\s+palindromic\s+substrings?|maximal\s+palindrome', lower):
            model.string_objective = StringObjective.MAXIMAL_PALINDROME_DETECTION
        elif re.search(r'suffix\s+array|suffix\s+sorting|kasai|lcp\s+array|lexicographical\s+order\s+of\s+all\s+suffixes', lower):
            model.string_objective = StringObjective.SUFFIX_SORTING_LCP
        elif re.search(r'z[- ]algorithm|z[- ]function|z[- ]array|z[- ]box|z\s+values?|longest\s+common\s+prefix\s+of\s+s\s+and\s+suffix', lower):
            model.string_objective = StringObjective.PREFIX_LCP_BOX_ANALYSIS
        elif re.search(r'rolling\s+hash|rabin[- ]karp|polynomial\s+hash|hash[- ]based\s+search', lower):
            model.string_objective = StringObjective.EXACT_SINGLE_PATTERN_MATCHING
            model.correctness_guarantee = CorrectnessGuarantee.PROBABILISTIC_COLLISION_BOUNDED
            model.complexity_contract = ComplexityContract.EXPECTED
        elif re.search(r'kmp|knuth[- ]morris[- ]pratt|failure\s+function|pi[- ]table|border\s+array|find\s+(?:all\s+)?occurrences?\s+of\s+pattern', lower):
            model.string_objective = StringObjective.EXACT_SINGLE_PATTERN_MATCHING
        elif re.search(r'pattern\s+matching|find\s+all\s+indices|exact\s+matching', lower):
            model.string_objective = StringObjective.EXACT_SINGLE_PATTERN_MATCHING

        return model

    def evaluate_candidates(self, model: SemanticStringModel) -> Tuple[List[StringCandidateEvaluation], Optional[str]]:
        evaluations: List[StringCandidateEvaluation] = []
        selected_pattern: Optional[str] = None

        obj = model.string_objective

        # ── EXACT_SINGLE_PATTERN_MATCHING ──
        # Candidate status is evaluated strictly relative to the requirement contract
        # (e.g. deterministic worst-case vs probabilistic/expected goals).
        if obj == StringObjective.EXACT_SINGLE_PATTERN_MATCHING:
            if model.correctness_guarantee in (CorrectnessGuarantee.PROBABILISTIC, CorrectnessGuarantee.PROBABILISTIC_COLLISION_BOUNDED):
                evaluations.append(StringCandidateEvaluation(
                    pattern="string_rabin_karp",
                    component_name="rolling_hash_builder",
                    status=CandidateStatus.VALID_OPTIMAL,
                    selection=SelectionStatus.SELECTED,
                    complexity="Expected O(N + M)",
                    justification="Rabin-Karp is VALID_OPTIMAL under requirement allowing probabilistic hashing with expected O(N + M) runtime."
                ))
                evaluations.append(StringCandidateEvaluation(
                    pattern="string_kmp_search",
                    component_name="kmp_matcher",
                    status=CandidateStatus.VALID_SUBOPTIMAL,
                    selection=SelectionStatus.NOT_SELECTED,
                    rejection_code="SUBOPTIMAL_FOR_HASH_FINGERPRINTING",
                    complexity="O(N + M) worst-case",
                    evidence="Deterministic KMP border traversal is valid, but evaluated as VALID_SUBOPTIMAL when hash-based fingerprinting is the primary requirement."
                ))
                selected_pattern = "string_rabin_karp"
            else:
                evaluations.append(StringCandidateEvaluation(
                    pattern="string_kmp_search",
                    component_name="kmp_matcher",
                    status=CandidateStatus.VALID_OPTIMAL,
                    selection=SelectionStatus.SELECTED,
                    complexity="O(N + M) worst-case",
                    justification="KMP border array is VALID_OPTIMAL under requirement demanding deterministic O(N + M) worst-case exact matching."
                ))
                evaluations.append(StringCandidateEvaluation(
                    pattern="string_rabin_karp",
                    component_name="rolling_hash_builder",
                    status=CandidateStatus.VALID_SUBOPTIMAL,
                    selection=SelectionStatus.NOT_SELECTED,
                    rejection_code="PROBABILISTIC_COLLISION_MODEL",
                    complexity="Expected O(N + M)",
                    evidence="Rabin-Karp is valid but evaluated as VALID_SUBOPTIMAL under strict deterministic worst-case requirement due to collision risk."
                ))
                evaluations.append(StringCandidateEvaluation(
                    pattern="string_z_algorithm",
                    component_name="z_algorithm_builder",
                    status=CandidateStatus.VALID_SUBOPTIMAL,
                    selection=SelectionStatus.NOT_SELECTED,
                    rejection_code="CONCATENATION_OVERHEAD",
                    complexity="O(N + M)",
                    evidence="Z-algorithm on P + # + T requires string concatenation and additional space; KMP matches streaming text in O(M) space."
                ))
                selected_pattern = "string_kmp_search"

        # ── PREFIX_LCP_BOX_ANALYSIS ──
        elif obj == StringObjective.PREFIX_LCP_BOX_ANALYSIS:
            evaluations.append(StringCandidateEvaluation(
                pattern="string_z_algorithm",
                component_name="z_algorithm_builder",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(N + M)",
                justification="Z-algorithm directly computes LCP of each suffix with entire string in linear time."
            ))
            selected_pattern = "string_z_algorithm"

        # ── MAXIMAL_PALINDROME_DETECTION ──
        elif obj == StringObjective.MAXIMAL_PALINDROME_DETECTION:
            evaluations.append(StringCandidateEvaluation(
                pattern="string_manacher",
                component_name="manacher_engine",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(N)",
                justification="Manacher's algorithm finds maximal palindromic radii around dummy separators in O(N) linear time."
            ))
            selected_pattern = "string_manacher"

        # ── EXACT_MULTI_PATTERN_MATCHING ──
        elif obj == StringObjective.EXACT_MULTI_PATTERN_MATCHING:
            evaluations.append(StringCandidateEvaluation(
                pattern="string_aho_corasick",
                component_name="aho_corasick_builder",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(sum(|P_i|) * |Sigma| + |T| + matches)",
                justification="Aho-Corasick automaton matches entire dictionary simultaneously via suffix failure links."
            ))
            selected_pattern = "string_aho_corasick"

        # ── SUFFIX_SORTING_LCP ──
        elif obj == StringObjective.SUFFIX_SORTING_LCP:
            evaluations.append(StringCandidateEvaluation(
                pattern="string_suffix_array",
                component_name="suffix_array_doubling",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(N log N) or O(N log^2 N) sorting + O(N) Kasai LCP",
                justification="Suffix array prefix doubling with Kasai LCP computes lexicographical suffix order and LCP array."
            ))
            selected_pattern = "string_suffix_array"

        # ── DISTINCT_SUBSTRING_ANALYSIS ──
        elif obj == StringObjective.DISTINCT_SUBSTRING_ANALYSIS:
            evaluations.append(StringCandidateEvaluation(
                pattern="string_suffix_automaton",
                component_name="sam_builder",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(N) with map transitions or O(N * |Sigma|) dense",
                justification="Suffix Automaton computes distinct substring count in linear time via sum(len[v] - len[link[v]])."
            ))
            evaluations.append(StringCandidateEvaluation(
                pattern="string_suffix_array",
                component_name="suffix_array_doubling",
                status=CandidateStatus.VALID_SUBOPTIMAL,
                selection=SelectionStatus.NOT_SELECTED,
                rejection_code="LOGARITHMIC_SORTING_OVERHEAD",
                complexity="O(N log N) + O(N)",
                evidence="Suffix array distinct substring counting via N*(N+1)/2 - sum(LCP) incurs sorting overhead compared to linear SAM."
            ))
            selected_pattern = "string_suffix_automaton"

        # ── LEXICOGRAPHICALLY_MINIMAL_ROTATION ──
        elif obj == StringObjective.LEXICOGRAPHICALLY_MINIMAL_ROTATION:
            evaluations.append(StringCandidateEvaluation(
                pattern="string_lyndon_duval",
                component_name="duval_factorizer",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(N) time, O(1) space",
                justification="Duval's algorithm finds lexicographically minimal cyclic shift in strictly linear time and constant auxiliary memory."
            ))
            selected_pattern = "string_lyndon_duval"

        # ── SUBSEQUENCE_AUTOMATON_QUERY ──
        elif obj == StringObjective.SUBSEQUENCE_AUTOMATON_QUERY:
            evaluations.append(StringCandidateEvaluation(
                pattern="string_subsequence_automaton",
                component_name="subseq_automaton_builder",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(N * |Sigma|) build, O(|Q|) query",
                justification="Alphabet-aware next-occurrence transition table tests multiple subsequence queries in optimal O(|Q|) time."
            ))
            selected_pattern = "string_subsequence_automaton"

        # ── LONGEST_COMMON_SUBSTRING ──
        elif obj == StringObjective.LONGEST_COMMON_SUBSTRING:
            evaluations.append(StringCandidateEvaluation(
                pattern="string_longest_common_substring_sam",
                component_name="sam_lcs_matcher",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(|S_1| * |Sigma| + |S_2|)",
                justification="Traversing S_2 along the Suffix Automaton of S_1 computes the longest common substring in linear time."
            ))
            selected_pattern = "string_longest_common_substring_sam"

        return evaluations, selected_pattern
