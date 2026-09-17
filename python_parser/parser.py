try:
    from python_parser.normalizer import normalize
    from python_parser.spell_corrector import correct_tokens_with_context
    from python_parser.intent_classifier import classify_intent, classify_domain
    from python_parser.semantic_tagger import extract_semantics
    from python_parser.compound_analyzer import analyze_compound
    from python_parser.numerical_parser import parse_numerical
    from python_parser.vocabulary import SORTING_ALIASES, SEARCHING_ALIASES, GRAPH_ALGORITHM_ALIASES, MENU_OPERATION_KEYWORDS
except ImportError:
    from normalizer import normalize
    from spell_corrector import correct_tokens_with_context
    from intent_classifier import classify_intent, classify_domain
    from semantic_tagger import extract_semantics
    from compound_analyzer import analyze_compound
    from numerical_parser import parse_numerical
    from vocabulary import SORTING_ALIASES, SEARCHING_ALIASES, GRAPH_ALGORITHM_ALIASES, MENU_OPERATION_KEYWORDS

# Supported structures and operations for V1
SUPPORTED = {
    'singly_linked_list': ['insert_end']
}

def assemble_problem_spec(tags, compound, intent_result, domain, raw_query, normalized, was_corrected):
    status = "ambiguous"
    error_code = None
    message = ""
    operation = None
    operation_action = None
    operation_position = None
    
    # Base spec
    spec = {
        "status": status,
        "language": "cpp",
        "domain": domain,
        "intent": intent_result['intent'],
        "structure": tags['structure'],
        "operation": None,
        "operation_action": None,
        "operation_position": None,
        "operation_negated": compound['operation_negated'],
        "target_value": tags['target_value'],
        "target_index": tags['target_index'],
        "is_compound": compound['is_compound'],
        "detected_actions": compound['detected_actions'],
        "sequencing_marker": compound['sequencing_marker'],
        "numerical_method": None,
        "numerical_category": None,
        "confidence": 1.0,
        "confidence_basis": "fuzzy_match" if was_corrected else "exact_rule_match",
        "error_code": None,
        "message": "",
        "raw_query": raw_query,
        "normalized_query": normalized
    }

    if intent_result.get('is_contradiction', False):
        spec['status'] = "ambiguous"
        spec['error_code'] = "CONTRADICTION_DETECTED"
        spec['message'] = "Contradictory requirements detected in prompt."
        return spec

    if intent_result['is_negated']:
        spec['status'] = "negated"
        spec['error_code'] = "NEGATED_INSTRUCTION_REFUSAL"
        spec['message'] = "CodeForge detected a prohibitive instruction. Code generation was halted."
        return spec
        
    if intent_result['intent'] == 'conceptual_question':
        spec['status'] = "question"
        spec['error_code'] = "CONCEPTUAL_QUESTION_DETECTED"
        spec['message'] = "Conceptual question, not a programming task"
        return spec

    if compound['is_compound']:
        spec['status'] = "unsupported"
        spec['error_code'] = "UNSUPPORTED_COMPOUND_PROBLEM"
        spec['message'] = "Compound problems are not supported."
        return spec

    if domain == 'algorithm':
        query = ' '.join(normalized.split())
        for algo, aliases in {**SORTING_ALIASES, **SEARCHING_ALIASES, **GRAPH_ALGORITHM_ALIASES}.items():
            for alias in aliases:
                if alias in query:
                    spec['operation'] = algo
                    spec['status'] = "success"
                    spec['message'] = "Algorithm detected."
                    spec['structure'] = None
                    return spec

    # Menu-driven program detection
    clean_lower = ' '.join(raw_query.lower().split())
    raw_lower = clean_lower
    forbid_menu = intent_result.get('forbid_menu', False)
    has_menu_keyword = any(m in raw_lower or m in normalized for m in [
        'menu driven', 'menu-driven', 'with menu', 'menu program', 'menu for',
        'menu based', 'a menu where', 'make a menu', 'create a menu', 'through a menu',
        'a menu with', 'a menu to', 'put these', 'choose between', 'choose whether',
        'user should choose', 'user can choose', 'repeatedly select', 'select which operation',
        'select the operation', 'choose another operation', 'interactive',
        'every time i run', 'choose push', 'choose pop', 'select the sorting', 'select which algorithm',
        'user must choose', 'user chooses', 'chooses sorting', 'choose the algorithm', 'choose which algorithm', 'choose an algorithm'
    ]) or ('menu' in raw_lower and not forbid_menu)
    is_menu = has_menu_keyword and not forbid_menu
    if is_menu:
        if not tags['structure']:
            raw_lower_check = raw_query.lower()
            if ('node' in raw_lower_check or 'nodes' in raw_lower_check) and ('after' in raw_lower_check or 'first node' in raw_lower_check):
                tags['structure'] = 'singly_linked_list'
                spec['structure'] = 'singly_linked_list'
            elif 'push' in raw_lower_check or 'pop' in raw_lower_check or 'stack' in raw_lower_check:
                tags['structure'] = 'stack'
                spec['structure'] = 'stack'
            elif 'sort' in raw_lower_check or 'sorting' in raw_lower_check:
                spec['domain'] = 'algorithm'
                spec['operation'] = 'menu'
                spec['generation_mode'] = 'menu'
                spec['status'] = 'success'
                spec['message'] = 'Sorting algorithm menu detected.'
                return spec
            else:
                tags['structure'] = 'singly_linked_list'
                spec['structure'] = 'singly_linked_list'

    if is_menu and tags['structure']:
        import re
        excluded_ops = set()
        exclusion_matches = re.finditer(r'\b(?:do not|dont|don\'t)\s+(?:implement|include|add|use)\s+([^.]+)', raw_lower)
        for m in exclusion_matches:
            clause = m.group(1)
            for op_id, patterns in MENU_OPERATION_KEYWORDS:
                for pat in patterns:
                    if pat in clause:
                        excluded_ops.add(op_id)

        found_ops = []
        for op_id, patterns in MENU_OPERATION_KEYWORDS:
            if op_id in excluded_ops:
                continue
            earliest_pos = -1
            for pat in patterns:
                if pat in ('creating', 'creation'):
                    if re.search(r'\b' + pat + r'\s+(?:(?:a|an|the)\s+)?(?:menu|program)\b', raw_lower):
                        continue
                idx = raw_lower.find(pat)
                if idx != -1:
                    is_in_exclusion = False
                    for em in re.finditer(r'\b(?:do not|dont|don\'t)\s+(?:implement|include|add|use)\s+([^.]+)', raw_lower):
                        if em.start() <= idx <= em.end():
                            is_in_exclusion = True
                            break
                    if not is_in_exclusion and (earliest_pos == -1 or idx < earliest_pos):
                        earliest_pos = idx
            if earliest_pos != -1:
                found_ops.append((earliest_pos, op_id))
        
        found_ops.sort(key=lambda x: x[0])
        deduped_ops = []
        for _, op_id in found_ops:
            if op_id not in deduped_ops and op_id not in excluded_ops:
                deduped_ops.append(op_id)

        spec['operation'] = 'menu'
        spec['operation_action'] = 'menu'
        spec['status'] = 'success'
        spec['generation_mode'] = 'menu'
        spec['menu_operations'] = deduped_ops if deduped_ops else None
        spec['message'] = (
            f"Menu-driven program detected for {tags['structure']} with {len(deduped_ops)} specific operations."
            if deduped_ops else f"Canonical menu-driven program detected for {tags['structure']}."
        )
        return spec

    if tags['structure'] == 'polynomial':
        spec['operation'] = 'add'
        spec['operation_action'] = 'add'
        spec['status'] = 'success'
        spec['message'] = 'Polynomial operation identified.'
        return spec
                    
    # Determine operation
    if tags['actions']:
        primary_action = tags['actions'][0]
        operation_action = primary_action['action']
        
        # Position logic
        if tags['positions']:
            # For simplicity, pick the first
            operation_position = tags['positions'][0]['position']
        elif tags['target_index'] is not None:
            operation_position = 'index'
        else:
            operation_position = primary_action['default_position']
            
        spec['operation_action'] = operation_action
        spec['operation_position'] = operation_position
        
        if operation_action == 'insert':
            if operation_position == 'head': operation = 'insert_beginning'
            elif operation_position == 'tail': operation = 'insert_end'
            elif operation_position == 'index': operation = 'insert_position'
            else: operation = 'insert'
        elif operation_action == 'delete':
            if operation_position == 'head': operation = 'delete_beginning'
            elif operation_position == 'tail': operation = 'delete_end'
            elif operation_position == 'index': operation = 'delete_position'
            else: operation = 'delete'
        else:
            operation = operation_action
            
        spec['operation'] = operation
        
    # Check structure
    if not tags['structure']:
        spec['status'] = "ambiguous"
        spec['error_code'] = "AMBIGUOUS_STRUCTURE"
        spec['message'] = "No valid data structure identified."
        return spec

    # Is the structure supported?
    if tags['structure'] not in SUPPORTED:
        spec['status'] = "unsupported"
        spec['error_code'] = "UNSUPPORTED_STRUCTURE"
        spec['message'] = f"Data structure '{tags['structure']}' is currently not supported."
        return spec
        
    # Is the operation provided?
    if not spec['operation']:
        spec['status'] = "ambiguous"
        spec['error_code'] = "AMBIGUOUS_OPERATION"
        spec['message'] = "No valid operation identified."
        return spec

    # Is the operation supported on the structure?
    if spec['operation'] not in SUPPORTED[tags['structure']]:
        spec['status'] = "unsupported"
        spec['error_code'] = "UNSUPPORTED_OPERATION"
        spec['message'] = f"Operation '{spec['operation']}' on '{tags['structure']}' is not supported."
        return spec

    spec['status'] = "success"
    spec['message'] = "Valid structure and operation identified."
    return spec

def parse_problem(query: str):
    normalized, original_tokens, normalized_tokens = normalize(query)
    corrected_tokens, was_corrected = correct_tokens_with_context(normalized_tokens)
    intent_result = classify_intent(corrected_tokens, query)
    domain = classify_domain(corrected_tokens)
    
    if intent_result.get('is_contradiction', False):
        return {
            "status": "ambiguous",
            "language": "cpp",
            "domain": domain,
            "intent": "ambiguous",
            "confidence": 0.95,
            "confidence_basis": "exact_rule_match",
            "error_code": "CONTRADICTION_DETECTED",
            "message": "Contradictory requirements detected in prompt.",
            "raw_query": query,
            "normalized_query": normalized
        }
        
    if domain == 'numerical':
        return parse_numerical(corrected_tokens, query, normalized, was_corrected)
        
    tags = extract_semantics(corrected_tokens)
    compound = analyze_compound(corrected_tokens, tags, intent_result)
    
    return assemble_problem_spec(tags, compound, intent_result, domain, query, normalized, was_corrected)


if __name__ == '__main__':
    import sys
    import json

    try:
        raw_input = sys.stdin.read().strip()
        if not raw_input:
            result = {
                "status": "ambiguous",
                "language": "cpp",
                "domain": "data_structure",
                "intent": "ambiguous",
                "confidence": 0,
                "confidence_basis": "ambiguous",
                "error_code": "EMPTY_INPUT",
                "message": "No input received.",
                "raw_query": "",
                "normalized_query": ""
            }
        else:
            try:
                data = json.loads(raw_input)
                query = data.get("query", "")
            except json.JSONDecodeError:
                query = raw_input

            if not query.strip():
                result = {
                    "status": "ambiguous",
                    "language": "cpp",
                    "domain": "data_structure",
                    "intent": "ambiguous",
                    "confidence": 0,
                    "confidence_basis": "ambiguous",
                    "error_code": "EMPTY_QUERY",
                    "message": "Empty query string.",
                    "raw_query": "",
                    "normalized_query": ""
                }
            else:
                result = parse_problem(query)

        print(json.dumps(result))
    except Exception as e:
        error_result = {
            "status": "ambiguous",
            "language": "cpp",
            "domain": "data_structure",
            "intent": "ambiguous",
            "confidence": 0,
            "confidence_basis": "ambiguous",
            "error_code": "INTERNAL_ERROR",
            "message": f"Parser error: {str(e)}",
            "raw_query": "",
            "normalized_query": ""
        }
        print(json.dumps(error_result))
