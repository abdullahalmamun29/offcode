"""
CHUP Phase 3O — Semantic String Ontology & Provenance Model.

Defines orthogonal, primitive string-theoretic dimensions and derived structural properties
with complete mathematical provenance. Zero algorithm labels allowed in this ontology.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Set


# ── 1. Primitive Dimensions ──

class AlphabetDomain(str, Enum):
    BINARY = "BINARY"                                      # Sigma = {0, 1}, |Sigma| = 2
    LOWERCASE_LATIN = "LOWERCASE_LATIN"                    # Sigma = [a-z], |Sigma| = 26
    UPPERCASE_LATIN = "UPPERCASE_LATIN"                    # Sigma = [A-Z], |Sigma| = 26
    ALPHANUMERIC = "ALPHANUMERIC"                          # Sigma = [a-zA-Z0-9], |Sigma| = 62
    ASCII_STANDARD = "ASCII_STANDARD"                      # Standard 7-bit ASCII [0..127], |Sigma| = 128
    ASCII = "ASCII"                                        # 7-bit ASCII alias (|Sigma| = 128)
    BYTE_ALPHABET = "BYTE_ALPHABET"                        # Full 8-bit byte/octet [0..255], |Sigma| = 256
    GENERAL_INTEGER_ALPHABET = "GENERAL_INTEGER_ALPHABET"  # Arbitrary integer tokens sigma <= N


class SequenceMultiplicity(str, Enum):
    SINGLE_STRING = "SINGLE_STRING"            # S
    TEXT_AND_PATTERN = "TEXT_AND_PATTERN"      # T, P
    DICTIONARY_SET = "DICTIONARY_SET"          # {P_1, P_2, ..., P_k}
    PAIR_OF_STRINGS = "PAIR_OF_STRINGS"        # S_1, S_2


class StringSymmetry(str, Enum):
    PALINDROMIC = "PALINDROMIC"                # S = S^R
    PERIODIC = "PERIODIC"                      # S = P^k P'
    BORDERED = "BORDERED"                      # Non-empty proper prefix equals suffix
    NONE = "NONE"


class CorrectnessGuarantee(str, Enum):
    DETERMINISTIC_EXACT = "DETERMINISTIC_EXACT"                                    # Absolute mathematical correctness without error probability (e.g. KMP, Z-algorithm)
    PROBABILISTIC_COLLISION_BOUNDED = "PROBABILISTIC_COLLISION_BOUNDED"            # Las Vegas / fingerprinting with collision probability bounded by prime field (e.g. Rabin-Karp)
    MONTE_CARLO_BOUNDED_ERROR = "MONTE_CARLO_BOUNDED_ERROR"                        # Randomized decision with bounded error probability (e.g. polynomial identity testing)
    DETERMINISTIC = "DETERMINISTIC"                                                # Backward-compatibility alias
    PROBABILISTIC = "PROBABILISTIC"                                                # Backward-compatibility alias


class ComplexityContract(str, Enum):
    WORST_CASE = "WORST_CASE"                  # Guaranteed worst-case upper bound
    EXPECTED = "EXPECTED"                      # Expected runtime under randomized choice or hash distribution
    AMORTIZED = "AMORTIZED"                    # Amortized per-operation bound


class TransitionRepresentation(str, Enum):
    DENSE_TABLE = "DENSE_TABLE"                # Fast direct indexing (e.g. 26 array per state)
    SPARSE_ADJACENCY = "SPARSE_ADJACENCY"      # Space-efficient map or vector for large alphabets


# ── 2. String Semantic Objectives ──

class StringObjective(str, Enum):
    EXACT_SINGLE_PATTERN_MATCHING = "EXACT_SINGLE_PATTERN_MATCHING"      # Find occurrences of P in T
    EXACT_MULTI_PATTERN_MATCHING = "EXACT_MULTI_PATTERN_MATCHING"        # Find occurrences of {P_i} in T
    PREFIX_BORDER_ANALYSIS = "PREFIX_BORDER_ANALYSIS"                    # Longest proper prefix equal to suffix (pi-table)
    PREFIX_LCP_BOX_ANALYSIS = "PREFIX_LCP_BOX_ANALYSIS"                  # Longest common prefix with prefix (Z-box)
    MAXIMAL_PALINDROME_DETECTION = "MAXIMAL_PALINDROME_DETECTION"        # Longest / all palindromic substrings
    DISTINCT_SUBSTRING_ANALYSIS = "DISTINCT_SUBSTRING_ANALYSIS"          # Count or index distinct substrings
    LEXICOGRAPHICALLY_MINIMAL_ROTATION = "LEXICOGRAPHICALLY_MINIMAL_ROTATION" # Canonical minimal cyclic shift
    SUBSTRING_EQUALITY_LOOKUP = "SUBSTRING_EQUALITY_LOOKUP"              # O(1) equality of arbitrary substrings
    SUFFIX_SORTING_LCP = "SUFFIX_SORTING_LCP"                            # Lexicographical suffix order + LCP
    SUBSEQUENCE_AUTOMATON_QUERY = "SUBSEQUENCE_AUTOMATON_QUERY"          # Fast multi-query subsequence acceptance
    LONGEST_COMMON_SUBSTRING = "LONGEST_COMMON_SUBSTRING"                # Longest contiguous substring common to S_1, S_2
    NONE = "NONE"


# ── 3. Provenance Dataclass ──

class ProvenanceStatus(str, Enum):
    PROVEN = "PROVEN"
    UNPROVEN = "UNPROVEN"
    CONTRADICTED = "CONTRADICTED"


@dataclass
class DerivedFact:
    """
    Formal record tracking how a structural fact was deduced.
    """
    fact_id: str
    value: Any
    source_facts: List[str] = field(default_factory=list)
    derivation_rule: str = ""
    proof_obligations: List[str] = field(default_factory=list)
    status: ProvenanceStatus = ProvenanceStatus.PROVEN


# ── 4. Semantic String Model ──

@dataclass
class SemanticStringModel:
    """
    Complete semantic representation of a string problem.
    Contains primitive facts and derived structural properties with full provenance.
    Zero algorithm names allowed in this representation.
    """
    # Primitive facts
    alphabet_domain: AlphabetDomain = AlphabetDomain.LOWERCASE_LATIN
    sequence_multiplicity: SequenceMultiplicity = SequenceMultiplicity.SINGLE_STRING
    string_symmetry: StringSymmetry = StringSymmetry.NONE
    correctness_guarantee: CorrectnessGuarantee = CorrectnessGuarantee.DETERMINISTIC
    complexity_contract: ComplexityContract = ComplexityContract.WORST_CASE
    transition_representation: TransitionRepresentation = TransitionRepresentation.DENSE_TABLE

    # Atomic objective
    string_objective: StringObjective = StringObjective.NONE

    # Problem bounds
    text_len_bound: Optional[int] = None
    pattern_len_bound: Optional[int] = None
    alphabet_size: int = 26
    time_limit_ms: int = 1000

    # Derived properties & provenance
    derived_properties: Dict[str, Any] = field(default_factory=dict)
    provenance_records: List[DerivedFact] = field(default_factory=list)

    def add_derived_property(
        self,
        fact_id: str,
        value: Any,
        source_facts: List[str],
        rule: str,
        obligations: Optional[List[str]] = None
    ) -> None:
        self.derived_properties[fact_id] = value
        self.provenance_records.append(DerivedFact(
            fact_id=fact_id,
            value=value,
            source_facts=source_facts,
            derivation_rule=rule,
            proof_obligations=obligations or [],
            status=ProvenanceStatus.PROVEN
        ))
