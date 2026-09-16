"""
Deterministic Natural Language Problem Parser for CodeForge.
Extracts structured ProblemSpec JSON without using generative AI.
"""

import sys
import os
import json
from typing import Dict, Any, List, Optional, Tuple

# Ensure repository root is in sys.path for robust execution from any working directory
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

try:
    from python_parser.normalizer import normalize_text, tokenize
    from python_parser.spell_corrector import correct_tokens
except ImportError:
    from normalizer import normalize_text, tokenize
    from spell_corrector import correct_tokens

# Supported configurations in Prototype V0
SUPPORTED_STRUCTURE = "singly_linked_list"
SUPPORTED_OPERATION = "insert_end"
SUPPORTED_LANGUAGE = "cpp"

# Structure definitions
STRUCTURE_PATTERNS = {
    "singly_linked_list": [
        ["singly", "linked", "list"],
        ["linked", "list"],
    ],
    "doubly_linked_list": [
        ["doubly", "linked", "list"],
    ],
    "binary_tree": [
        ["binary", "tree"],
        ["tree"],
    ],
    "stack": [
        ["stack"],
    ],
    "queue": [
        ["queue"],
    ],
    "graph": [
        ["graph"],
    ]
}

def detect_structure(tokens: List[str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Detects the target data structure from tokens.
    Returns: (structure_key, match_type)
    """
    text_joined = " " + " ".join(tokens) + " "

    # Check doubly linked list first (more specific than linked list)
    if " doubly linked list " in text_joined or " doubly linked " in text_joined:
        return "doubly_linked_list", "exact"

    # Check singly linked list
    if " singly linked list " in text_joined or " singly linked " in text_joined:
        return "singly_linked_list", "exact"

    # Check general linked list (defaults to singly linked list in this domain)
    if " linked list " in text_joined:
        return "singly_linked_list", "synonym"

    # Check other structures
    if " binary tree " in text_joined:
        return "binary_tree", "exact"
    if " tree " in text_joined:
        return "binary_tree", "synonym"
    if " stack " in text_joined:
        return "stack", "exact"
    if " queue " in text_joined:
        return "queue", "exact"
    if " graph " in text_joined:
        return "graph", "exact"

    return None, None

def detect_candidate_operations(tokens: List[str]) -> List[Tuple[str, str]]:
    """
    Scans tokens to find all candidate operations present in the query.
    Returns a list of (operation_name, match_type).
    """
    text_joined = " " + " ".join(tokens) + " "
    operations = []

    # 1. Reverse
    if " reverse " in text_joined or " invert " in text_joined:
        operations.append(("reverse", "exact" if "reverse" in text_joined else "synonym"))

    # 2. Delete / Remove / Pop
    has_delete = any(f" {v} " in text_joined for v in ["delete", "remove", "pop"])
    if has_delete:
        if any(f" {pos} " in text_joined for pos in ["end", "tail", "last", "back"]):
            operations.append(("delete_end", "exact" if "delete" in text_joined else "synonym"))
        elif any(f" {pos} " in text_joined for pos in ["beginning", "head", "front", "first"]):
            operations.append(("delete_beginning", "exact" if "delete" in text_joined else "synonym"))
        else:
            operations.append(("delete", "exact" if "delete" in text_joined else "synonym"))

    # 3. Insert / Add / Append / Push / Attach
    # End positions
    has_end_pos = (
        any(f" {pos} " in text_joined for pos in ["end", "tail", "last", "back"]) or
        "last position" in text_joined
    )
    # Beginning positions
    has_beg_pos = any(f" {pos} " in text_joined for pos in ["beginning", "head", "front", "start", "first"])

    has_insert_verb = any(f" {v} " in text_joined for v in ["insert", "add", "push", "attach", "put"])
    has_append_verb = " append " in text_joined
    has_prepend_verb = " prepend " in text_joined

    if has_prepend_verb or (has_insert_verb and has_beg_pos):
        match_type = "exact" if "insert" in text_joined and "beginning" in text_joined else "synonym"
        operations.append(("insert_beginning", match_type))

    if has_append_verb:
        # Append inherently means insert at end
        operations.append(("insert_end", "synonym"))
    elif has_insert_verb and has_end_pos:
        match_type = "exact" if ("insert" in text_joined and "end" in text_joined) else "synonym"
        operations.append(("insert_end", match_type))

    # 4. Search / Find
    if any(f" {v} " in text_joined for v in ["search", "find"]):
        operations.append(("search", "exact"))

    return operations

def detect_compound_intent(raw_query: str, tokens: List[str], candidate_ops: List[Tuple[str, str]]) -> bool:
    """
    Detects if the query contains compound operations or explicit sequencing.
    e.g. 'Reverse a singly linked list and then insert a node at the end.'
         'Delete the last node and insert a new node.'
    """
    raw_lower = raw_query.lower()

    # Explicit sequential connectors
    sequential_markers = ["and then", "and also", "then insert", "then add", "then delete", "then reverse", "after that", "followed by"]
    for marker in sequential_markers:
        if marker in raw_lower:
            return True

    # If there are multiple distinct operation types detected
    unique_ops = set(op for op, _ in candidate_ops)
    if len(unique_ops) > 1:
        return True

    return False

def parse_problem(query: str) -> Dict[str, Any]:
    """
    Parses a natural-language programming problem into a structured ProblemSpec.
    """
    if not query or not query.strip():
        return {
            "status": "ambiguous",
            "language": SUPPORTED_LANGUAGE,
            "domain": "data_structure",
            "structure": None,
            "operation": None,
            "confidence": 0.0,
            "confidence_basis": "ambiguous",
            "error_code": "EMPTY_QUERY",
            "message": "Empty query received. Please provide a problem statement.",
            "raw_query": query,
            "normalized_query": ""
        }

    raw_query = query.strip()
    norm_text = normalize_text(raw_query)
    raw_tokens = tokenize(norm_text)

    # Spell correction
    tokens, was_corrected = correct_tokens(raw_tokens)
    normalized_query = " ".join(tokens)

    # Candidate operations
    candidate_ops = detect_candidate_operations(tokens)

    # Check for compound operations first (refuse rather than guess!)
    if detect_compound_intent(raw_query, tokens, candidate_ops):
        return {
            "status": "unsupported",
            "language": SUPPORTED_LANGUAGE,
            "domain": "data_structure",
            "structure": None,
            "operation": None,
            "confidence": 0.0,
            "confidence_basis": "unsupported",
            "error_code": "UNSUPPORTED_COMPOUND_PROBLEM",
            "message": "CodeForge detected multiple operations in a single query. Compound operations are not supported in Prototype V0.",
            "raw_query": raw_query,
            "normalized_query": normalized_query
        }

    # Detect Data Structure (CONSERVATIVE: requires explicit structure)
    structure, struct_match_type = detect_structure(tokens)

    if not structure:
        # Check if they asked an operation without specifying structure
        op_name = candidate_ops[0][0] if candidate_ops else None
        return {
            "status": "ambiguous",
            "language": SUPPORTED_LANGUAGE,
            "domain": "data_structure",
            "structure": None,
            "operation": op_name,
            "confidence": 0.0,
            "confidence_basis": "ambiguous",
            "error_code": "AMBIGUOUS_STRUCTURE",
            "message": "No explicit data structure was specified (e.g. 'singly linked list'). CodeForge requires an explicit target data structure.",
            "raw_query": raw_query,
            "normalized_query": normalized_query
        }

    # If structure is detected but not supported in Prototype V0
    if structure != SUPPORTED_STRUCTURE:
        op_name = candidate_ops[0][0] if candidate_ops else None
        return {
            "status": "unsupported",
            "language": SUPPORTED_LANGUAGE,
            "domain": "data_structure",
            "structure": structure,
            "operation": op_name,
            "confidence": 0.0,
            "confidence_basis": "unsupported",
            "error_code": "UNSUPPORTED_STRUCTURE",
            "message": f"Data structure '{structure}' was identified, but CodeForge Prototype V0 currently only supports 'singly_linked_list'.",
            "raw_query": raw_query,
            "normalized_query": normalized_query
        }

    # Structure is singly_linked_list. Now evaluate operation.
    if not candidate_ops:
        return {
            "status": "ambiguous",
            "language": SUPPORTED_LANGUAGE,
            "domain": "data_structure",
            "structure": structure,
            "operation": None,
            "confidence": 0.0,
            "confidence_basis": "ambiguous",
            "error_code": "UNKNOWN_OPERATION",
            "message": f"Target data structure is '{structure}', but no supported operation (such as 'insert at end') was recognized.",
            "raw_query": raw_query,
            "normalized_query": normalized_query
        }

    operation, op_match_type = candidate_ops[0]

    # Determine matching confidence basis
    if was_corrected:
        confidence_basis = "fuzzy_match"
        confidence = 0.9
    elif struct_match_type == "exact" and op_match_type == "exact":
        confidence_basis = "exact_rule_match"
        confidence = 1.0
    else:
        confidence_basis = "synonym_match"
        confidence = 1.0

    # Check if operation is supported
    if operation != SUPPORTED_OPERATION:
        return {
            "status": "unsupported",
            "language": SUPPORTED_LANGUAGE,
            "domain": "data_structure",
            "structure": structure,
            "operation": operation,
            "confidence": 0.0,
            "confidence_basis": confidence_basis,
            "error_code": "UNSUPPORTED_OPERATION",
            "message": f"Operation '{operation}' was identified for '{structure}', but CodeForge Prototype V0 currently only has a verified solution for 'insert_end'.",
            "raw_query": raw_query,
            "normalized_query": normalized_query
        }

    return {
        "status": "success",
        "language": SUPPORTED_LANGUAGE,
        "domain": "data_structure",
        "structure": structure,
        "operation": operation,
        "confidence": confidence,
        "confidence_basis": confidence_basis,
        "error_code": None,
        "message": f"Successfully identified {structure} with {operation} operation.",
        "raw_query": raw_query,
        "normalized_query": normalized_query
    }

def main():
    """
    CLI interface supporting either command line argument or stdin JSON streaming.
    """
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        result = parse_problem(query)
        print(json.dumps(result, indent=2))
        return

    # Check if input is piped through stdin
    if not sys.stdin.isatty():
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                # Could be JSON { "query": "..." } or raw string
                payload = json.loads(line)
                query = payload.get("query", "")
            except json.JSONDecodeError:
                query = line
            result = parse_problem(query)
            print(json.dumps(result))
            sys.stdout.flush()
    else:
        # Interactive test mode
        print("CodeForge Python Parser (Prototype V0). Type a query or Ctrl+C to exit:")
        while True:
            try:
                query = input("> ")
                result = parse_problem(query)
                print(json.dumps(result, indent=2))
            except (EOFError, KeyboardInterrupt):
                break

if __name__ == "__main__":
    main()
