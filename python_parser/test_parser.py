"""
Unit tests for CodeForge Python Parser.
Tests exact phrasing, synonyms, conservative parsing, fuzzy spelling,
unsupported operations, and compound query rejection.
"""

import pytest
from python_parser.parser import parse_problem

class TestCodeForgeParser:

    # 1. Normal and Synonymous Supported Cases
    def test_canonical_insert_end(self):
        query = "Insert a node at the end of a singly linked list."
        spec = parse_problem(query)
        assert spec["status"] == "success"
        assert spec["language"] == "cpp"
        assert spec["structure"] == "singly_linked_list"
        assert spec["operation"] == "insert_end"
        assert spec["confidence"] == 1.0
        assert spec["confidence_basis"] == "exact_rule_match"

    def test_synonym_tail(self):
        query = "Add a node to the tail of the linked list."
        spec = parse_problem(query)
        assert spec["status"] == "success"
        assert spec["structure"] == "singly_linked_list"
        assert spec["operation"] == "insert_end"
        assert spec["confidence_basis"] == "synonym_match"

    def test_synonym_append_with_structure(self):
        query = "Append a new node to the singly linked list."
        spec = parse_problem(query)
        assert spec["status"] == "success"
        assert spec["structure"] == "singly_linked_list"
        assert spec["operation"] == "insert_end"
        assert spec["confidence_basis"] == "synonym_match"

    def test_last_position_phrasing(self):
        query = "Insert a new element at the last position of a singly linked list."
        spec = parse_problem(query)
        assert spec["status"] == "success"
        assert spec["structure"] == "singly_linked_list"
        assert spec["operation"] == "insert_end"

    def test_create_and_insert_phrasing(self):
        query = "Create a singly linked list and insert a node at the end."
        spec = parse_problem(query)
        assert spec["status"] == "success"
        assert spec["structure"] == "singly_linked_list"
        assert spec["operation"] == "insert_end"

    # 2. Conservative Structure Requirement (Ambiguous when no structure specified)
    def test_conservative_append_without_structure(self):
        query = "Append a new node."
        spec = parse_problem(query)
        assert spec["status"] == "ambiguous"
        assert spec["error_code"] == "AMBIGUOUS_STRUCTURE"
        assert spec["structure"] is None

    def test_conservative_insert_end_without_structure(self):
        query = "Insert a node at the end."
        spec = parse_problem(query)
        assert spec["status"] == "ambiguous"
        assert spec["error_code"] == "AMBIGUOUS_STRUCTURE"

    # 3. Spelling Error Normalization (Fuzzy Matching)
    def test_spelling_correction_insert_tail(self):
        query = "insrt a node at the tail of a likned list"
        spec = parse_problem(query)
        assert spec["status"] == "success"
        assert spec["structure"] == "singly_linked_list"
        assert spec["operation"] == "insert_end"
        assert spec["confidence_basis"] == "fuzzy_match"

    def test_spelling_correction_apend(self):
        query = "apend a new node to the singly linked list"
        spec = parse_problem(query)
        assert spec["status"] == "success"
        assert spec["structure"] == "singly_linked_list"
        assert spec["operation"] == "insert_end"
        assert spec["confidence_basis"] == "fuzzy_match"

    def test_spelling_correction_beggining_unsupported(self):
        query = "insert a node at the beggining of a singly linked list"
        spec = parse_problem(query)
        assert spec["status"] == "unsupported"
        assert spec["structure"] == "singly_linked_list"
        assert spec["operation"] == "insert_beginning"
        assert spec["error_code"] == "UNSUPPORTED_OPERATION"
        assert spec["confidence_basis"] == "fuzzy_match"

    # 4. Unsupported Operations and Structures
    def test_unsupported_reverse_operation(self):
        query = "Reverse a linked list."
        spec = parse_problem(query)
        assert spec["status"] == "unsupported"
        assert spec["structure"] == "singly_linked_list"
        assert spec["operation"] == "reverse"
        assert spec["error_code"] == "UNSUPPORTED_OPERATION"

    def test_unsupported_delete_end(self):
        query = "Delete the last node of a singly linked list."
        spec = parse_problem(query)
        assert spec["status"] == "unsupported"
        assert spec["structure"] == "singly_linked_list"
        assert spec["operation"] == "delete_end"
        assert spec["error_code"] == "UNSUPPORTED_OPERATION"

    def test_unsupported_binary_tree_structure(self):
        query = "Implement a binary tree."
        spec = parse_problem(query)
        assert spec["status"] == "unsupported"
        assert spec["structure"] == "binary_tree"
        assert spec["error_code"] == "UNSUPPORTED_STRUCTURE"

    # 5. Compound Queries and False Positive Prevention
    def test_compound_reverse_and_insert_end(self):
        query = "Reverse a singly linked list and then insert a node at the end."
        spec = parse_problem(query)
        assert spec["status"] == "unsupported"
        assert spec["error_code"] == "UNSUPPORTED_COMPOUND_PROBLEM"

    def test_compound_delete_and_insert(self):
        query = "Delete the last node and insert a new node into the singly linked list."
        spec = parse_problem(query)
        assert spec["status"] == "unsupported"
        assert spec["error_code"] == "UNSUPPORTED_COMPOUND_PROBLEM"

    # 6. Unrelated / Ambiguous Inputs
    def test_unrelated_input(self):
        query = "How do I make chocolate cake?"
        spec = parse_problem(query)
        assert spec["status"] == "ambiguous"

    def test_empty_query(self):
        query = "   "
        spec = parse_problem(query)
        assert spec["status"] == "ambiguous"
        assert spec["error_code"] == "EMPTY_QUERY"
