"""
CodeForge Stress Test Suite (40-50 Realistic, Colloquial, and Edge-Case Prompts).
Evaluates parser robustness, identifies edge cases, and generates a structured failure dataset.
"""

import os
import sys
import json
from dataclasses import dataclass
from typing import Optional, Dict, Any, List

# Ensure repository root is in sys.path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from python_parser.parser import parse_problem

@dataclass
class TestCase:
    id: int
    prompt: str
    expected_status: str  # "success", "unsupported", "ambiguous"
    expected_structure: Optional[str]
    expected_operation: Optional[str]
    expected_error_code: Optional[str]
    intent_category: str
    notes: str

TEST_CASES: List[TestCase] = [
    # Category 1: Natural variations of Singly Linked List + Insert at End
    TestCase(1, "add node at tail in singly linked list", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "Colloquial 'at tail in'"),
    TestCase(2, "put 50 at the end of linked list", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "Value '50' with 'put at end'"),
    TestCase(3, "append node to linked list", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "'append node to linked list'"),
    TestCase(4, "append a node to a singly linked list", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "Canonical append phrasing"),
    TestCase(5, "insert new element after the last node in singly linked list", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "'after the last node' phrasing"),
    TestCase(6, "add one more node to the tail of linked list", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "'one more node to the tail'"),
    TestCase(7, "insrt node at the end of likned list", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "Double typo: 'insrt' and 'likned'"),
    TestCase(8, "singly linked list insert at the end", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "Inverted word order"),
    TestCase(9, "push_back in singly linked list", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "C++ STL style 'push_back'"),
    TestCase(10, "attach an integer at the end of the singly linked list", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "'attach an integer at the end'"),
    TestCase(11, "i want to append a value to the tail of my linked list", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "Conversational filler words"),
    TestCase(12, "insert into the back of a linked list", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "'into the back of'"),
    TestCase(13, "pls insrt 10 @ end of likned lst asap!!!", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "Slang, punctuation, and multi-typos"),
    TestCase(14, "yo bro add a node to the tail of this singly linked list", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "Heavy colloquial slang"),
    TestCase(15, "INSERT A NODE AT THE END OF A SINGLY LINKED LIST!!!!", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "All caps + exclamation marks"),

    # Category 2: Conservative Rejections (Missing structure or ambiguous target)
    TestCase(16, "create a node and attach it at last", "ambiguous", None, None, "AMBIGUOUS_STRUCTURE", "Conservative Rejections", "Missing explicit data structure"),
    TestCase(17, "add one more node to the tail", "ambiguous", None, None, "AMBIGUOUS_STRUCTURE", "Conservative Rejections", "Has 'tail' and 'node' but no linked list specified"),
    TestCase(18, "add node to list", "ambiguous", None, None, "AMBIGUOUS_STRUCTURE", "Conservative Rejections", "'list' alone is ambiguous (linked list, array, python list)"),
    TestCase(19, "append 42", "ambiguous", None, None, "AMBIGUOUS_STRUCTURE", "Conservative Rejections", "No structure specified"),
    TestCase(20, "insert at end", "ambiguous", None, None, "AMBIGUOUS_STRUCTURE", "Conservative Rejections", "No structure specified"),
    TestCase(21, "push to tail", "ambiguous", None, None, "AMBIGUOUS_STRUCTURE", "Conservative Rejections", "No structure specified"),
    TestCase(22, "insert a new element after the last node", "ambiguous", None, None, "AMBIGUOUS_STRUCTURE", "Conservative Rejections", "'last node' without explicitly naming list"),

    # Category 3: Unsupported Operations on Linked List
    TestCase(23, "reverse the linked list", "unsupported", "singly_linked_list", "reverse", "UNSUPPORTED_OPERATION", "Unsupported Operations", "Valid reverse operation, no generator"),
    TestCase(24, "remove last node from linked list", "unsupported", "singly_linked_list", "delete_end", "UNSUPPORTED_OPERATION", "Unsupported Operations", "Delete from end"),
    TestCase(25, "delete head from singly linked list", "unsupported", "singly_linked_list", "delete_beginning", "UNSUPPORTED_OPERATION", "Unsupported Operations", "Delete from beginning"),
    TestCase(26, "find value 10 in singly linked list", "unsupported", "singly_linked_list", "search", "UNSUPPORTED_OPERATION", "Unsupported Operations", "Search in linked list"),
    TestCase(27, "insert at index 3 in singly linked list", "unsupported", "singly_linked_list", None, "UNSUPPORTED_OPERATION", "Unsupported Operations", "Arbitrary index insertion"),
    TestCase(28, "traverse and print all elements of singly linked list", "unsupported", "singly_linked_list", None, "UNSUPPORTED_OPERATION", "Unsupported Operations", "Traversal / display only"),

    # Category 4: Unsupported Data Structures
    TestCase(29, "make a doubly linked list", "unsupported", "doubly_linked_list", None, "UNSUPPORTED_STRUCTURE", "Unsupported Structures", "Doubly linked list structure"),
    TestCase(30, "insert into a binary search tree", "unsupported", "binary_tree", None, "UNSUPPORTED_STRUCTURE", "Unsupported Structures", "Binary tree structure"),
    TestCase(31, "push element to stack", "unsupported", "stack", None, "UNSUPPORTED_STRUCTURE", "Unsupported Structures", "Stack structure"),
    TestCase(32, "enqueue item in queue", "unsupported", "queue", None, "UNSUPPORTED_STRUCTURE", "Unsupported Structures", "Queue structure"),
    TestCase(33, "graph traversal using bfs", "unsupported", "graph", None, "UNSUPPORTED_STRUCTURE", "Unsupported Structures", "Graph structure"),

    # Category 5: Compound / Multi-Step Operations
    TestCase(34, "insert at beginning and then at end of singly linked list", "unsupported", None, None, "UNSUPPORTED_COMPOUND_PROBLEM", "Compound Operations", "Explicit sequencing 'and then'"),
    TestCase(35, "insert at beginning and then at end", "unsupported", None, None, "UNSUPPORTED_COMPOUND_PROBLEM", "Compound Operations", "Compound without structure"),
    TestCase(36, "delete the last node and insert a new node into singly linked list", "unsupported", None, None, "UNSUPPORTED_COMPOUND_PROBLEM", "Compound Operations", "Delete + insert"),
    TestCase(37, "create a linked list, insert 5 nodes at the end, and then reverse it", "unsupported", None, None, "UNSUPPORTED_COMPOUND_PROBLEM", "Compound Operations", "Multi-operation with reverse"),
    TestCase(38, "find 10 in singly linked list and delete it", "unsupported", None, None, "UNSUPPORTED_COMPOUND_PROBLEM", "Compound Operations", "Find + delete compound"),
    TestCase(39, "reverse singly linked list after inserting a node at tail", "unsupported", None, None, "UNSUPPORTED_COMPOUND_PROBLEM", "Compound Operations", "'after inserting' sequencing"),

    # Category 6: Negations, Conceptual Questions & Adversarial Phrasings
    TestCase(40, "insert a node at the beginning not at the end of singly linked list", "unsupported", "singly_linked_list", "insert_beginning", "UNSUPPORTED_OPERATION", "Adversarial / Negation", "Negation 'not at the end' - should pick beginning or refuse"),
    TestCase(41, "do not insert at the end of the linked list", "ambiguous", None, None, None, "Adversarial / Negation", "Negation: should not execute insert_end!"),
    TestCase(42, "whats the difference between insert at tail and insert at head in a linked list", "ambiguous", None, None, None, "Conceptual / Non-code", "Conceptual question, not a programming task"),
    TestCase(43, "how do i make a pizza with cheese", "ambiguous", None, None, None, "Completely Unrelated", "Nonsense / unrelated query"),
    TestCase(44, "fastest way to append to linked list in c++", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "Inquiry about append implementation"),
    TestCase(45, "singly_linked_list::insert_tail()", "success", "singly_linked_list", "insert_end", None, "Code-like Syntax", "C++ scope syntax"),
    TestCase(46, "add 99 to the back of the linked list", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "'add 99 to the back'"),
    TestCase(47, "attach node to end", "ambiguous", None, None, "AMBIGUOUS_STRUCTURE", "Conservative Rejections", "Missing structure"),
    TestCase(48, "append element to tail of singly linked list", "success", "singly_linked_list", "insert_end", None, "Supported Phrasings", "'append element to tail'")
]

def run_stress_test():
    total = len(TEST_CASES)
    passed_count = 0
    failures = []

    print(f"Running CodeForge Stress Test ({total} Prompts)...\n")

    for tc in TEST_CASES:
        actual = parse_problem(tc.prompt)

        # Check conditions
        status_match = (actual.get("status") == tc.expected_status)
        struct_match = True
        if tc.expected_structure is not None:
            struct_match = (actual.get("structure") == tc.expected_structure)
        op_match = True
        if tc.expected_operation is not None:
            op_match = (actual.get("operation") == tc.expected_operation)
        err_match = True
        if tc.expected_error_code is not None:
            err_match = (actual.get("error_code") == tc.expected_error_code)

        is_success = status_match and struct_match and op_match and err_match

        if is_success:
            passed_count += 1
            print(f"  [{tc.id:02d}] PASS: \"{tc.prompt}\" -> {actual.get('status')} ({actual.get('structure')}, {actual.get('operation')})")
        else:
            print(f"  [{tc.id:02d}] FAIL: \"{tc.prompt}\"")
            print(f"        Expected: status={tc.expected_status}, struct={tc.expected_structure}, op={tc.expected_operation}, err={tc.expected_error_code}")
            print(f"        Actual  : status={actual.get('status')}, struct={actual.get('structure')}, op={actual.get('operation')}, err={actual.get('error_code')}")
            print(f"        Basis   : {actual.get('confidence_basis')}, Message: {actual.get('message')}")

            # Diagnosis of why it failed
            reasons = []
            if not status_match:
                reasons.append(f"Status mismatch: expected '{tc.expected_status}', got '{actual.get('status')}'")
            if not struct_match:
                reasons.append(f"Structure mismatch: expected '{tc.expected_structure}', got '{actual.get('structure')}'")
            if not op_match:
                reasons.append(f"Operation mismatch: expected '{tc.expected_operation}', got '{actual.get('operation')}'")
            if not err_match:
                reasons.append(f"Error code mismatch: expected '{tc.expected_error_code}', got '{actual.get('error_code')}'")

            failures.append({
                "id": tc.id,
                "input": tc.prompt,
                "category": tc.intent_category,
                "expected": {
                    "status": tc.expected_status,
                    "structure": tc.expected_structure,
                    "operation": tc.expected_operation,
                    "error_code": tc.expected_error_code
                },
                "actual": {
                    "status": actual.get("status"),
                    "structure": actual.get("structure"),
                    "operation": actual.get("operation"),
                    "error_code": actual.get("error_code")
                },
                "parser_decision": {
                    "confidence_basis": actual.get("confidence_basis"),
                    "normalized_query": actual.get("normalized_query"),
                    "message": actual.get("message")
                },
                "why_it_failed": "; ".join(reasons)
            })

    print(f"\n=================================================")
    print(f"Stress Test Summary: {passed_count}/{total} passed ({(passed_count/total)*100:.1f}%)")
    print(f"Total Discrepancies/Failures: {len(failures)}")
    print(f"=================================================\n")

    # Save failure dataset to JSON for analysis
    output_path = os.path.join(REPO_ROOT, "dist_test", "stress_test_failures.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(failures, f, indent=2)

    return failures

if __name__ == "__main__":
    run_stress_test()
