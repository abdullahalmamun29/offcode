"""
CHUP Phase 3O — String State Contracts & Semantic Substitutability.

Enforces formal state contracts for string and automata components.
Critical Invariant:
A specialized state may satisfy a generic state contract only when it is
semantically substitutable for that contract.
Structural resemblance, implementation similarity, or the fact that
an algorithm's internal representation happens to form a familiar
structure MUST NOT create an IS-A relationship.
When a specialized state can expose a generic representation, the
relationship MUST be represented as an explicit transformation / adapter node.
"""

from typing import Dict, Any, List, Optional
from pointer_algorithms.adv_graph.component_model import StateContract, CompositionNodeType


# ── String State Contracts ──

def make_border_array_state(length: int = 0) -> StateContract:
    return StateContract(
        name="BorderArrayState",
        attributes={"length": length},
        supertypes=[]
    )


def make_z_array_state(length: int = 0) -> StateContract:
    return StateContract(
        name="ZArrayState",
        attributes={"length": length},
        supertypes=[]
    )


def make_rolling_hash_state(probabilistic: bool = True) -> StateContract:
    return StateContract(
        name="RollingHashState",
        attributes={"probabilistic": probabilistic},
        supertypes=[]
    )


def make_palindromic_radii_state(length: int = 0) -> StateContract:
    return StateContract(
        name="PalindromicRadiiState",
        attributes={"length": length},
        supertypes=[]
    )


def make_trie_automaton_state(alphabet_size: int = 26) -> StateContract:
    return StateContract(
        name="TrieAutomatonState",
        attributes={"alphabet_size": alphabet_size},
        supertypes=[]
    )


def make_aho_corasick_state(alphabet_size: int = 26, has_failure_links: bool = True) -> StateContract:
    # Aho-Corasick is genuinely an augmented TrieAutomatonState (IS-A)
    return StateContract(
        name="AhoCorasickAutomatonState",
        attributes={"alphabet_size": alphabet_size, "has_failure_links": has_failure_links},
        supertypes=["TrieAutomatonState"]
    )


def make_suffix_array_state(length: int = 0, has_rank: bool = True) -> StateContract:
    return StateContract(
        name="SuffixArrayState",
        attributes={"length": length, "has_rank": has_rank},
        supertypes=[]
    )


def make_lcp_array_state(length: int = 0) -> StateContract:
    return StateContract(
        name="LCPArrayState",
        attributes={"length": length},
        supertypes=[]
    )


def make_suffix_automaton_state(alphabet_size: int = 26, transition_rep: str = "DENSE_TABLE") -> StateContract:
    # CRITICAL ARCHITECTURAL GUARDRAIL:
    # SuffixAutomatonState does NOT inherit DirectedAcyclicGraph directly!
    # Semantic substitutability rule: A SAM state contract requires SAM operations (link, len, clone).
    # Exposure as a generic DAG must go through SAMTransitionGraphAdapter.
    return StateContract(
        name="SuffixAutomatonState",
        attributes={"alphabet_size": alphabet_size, "transition_rep": transition_rep},
        supertypes=[]
    )


def make_sam_transition_dag_state(directed: bool = True, acyclic: bool = True) -> StateContract:
    # The explicit DAG projection created by SAMTransitionGraphAdapter
    return StateContract(
        name="SAMTransitionDAG",
        attributes={"directed": directed, "acyclic": acyclic},
        supertypes=["DirectedAcyclicGraph"]
    )


def make_lyndon_factorization_state(non_increasing: bool = True) -> StateContract:
    return StateContract(
        name="LyndonFactorizationState",
        attributes={"non_increasing": non_increasing},
        supertypes=[]
    )


def make_subsequence_automaton_state(alphabet_size: int = 26, representation: str = "DENSE_TABLE") -> StateContract:
    # Alphabet-agnostic: Supports DENSE_TABLE or SPARSE_ADJACENCY
    return StateContract(
        name="SubsequenceAutomatonState",
        attributes={"alphabet_size": alphabet_size, "representation": representation},
        supertypes=[]
    )
