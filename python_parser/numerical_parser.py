try:
    from python_parser.vocabulary import NUMERICAL_METHOD_ALIASES, NUMERICAL_CATEGORIES
except ImportError:
    from vocabulary import NUMERICAL_METHOD_ALIASES, NUMERICAL_CATEGORIES

def parse_numerical(corrected_tokens, raw_query, normalized_query, was_corrected):
    raw_lower = raw_query.lower()
    clean_lower = ' '.join(raw_lower.replace('-', ' ').split())
    forbid_menu = any(p in clean_lower for p in ['do not create a menu', 'no menu', 'without menu', 'without a menu', 'non menu']) or 'no-menu' in raw_lower or 'non-menu' in raw_lower
    is_menu = ('menu' in clean_lower or 'menudriven' in clean_lower or 'choose between' in clean_lower) and not forbid_menu

    if is_menu:
        found_methods = []
        for m, aliases in NUMERICAL_METHOD_ALIASES.items():
            for alias in aliases:
                idx = clean_lower.find(alias)
                if idx != -1:
                    found_methods.append((idx, m))
                    break
        found_methods.sort(key=lambda x: x[0])
        deduped = []
        for _, m in found_methods:
            if m not in deduped:
                deduped.append(m)

        return {
            "status": "success",
            "language": "cpp",
            "domain": "numerical",
            "intent": "code_generation",
            "structure": None,
            "operation": "menu",
            "operation_action": "menu",
            "operation_position": None,
            "operation_negated": False,
            "target_value": None,
            "target_index": None,
            "is_compound": False,
            "detected_actions": [],
            "sequencing_marker": None,
            "numerical_method": "menu",
            "numerical_category": "root_finding",
            "confidence": 1.0,
            "confidence_basis": "exact_rule_match",
            "error_code": None,
            "message": "Menu-driven numerical method program identified",
            "raw_query": raw_query,
            "normalized_query": normalized_query,
            "generation_mode": "menu",
            "menu_operations": deduped if deduped else ['bisection', 'false_position', 'newton_raphson', 'secant']
        }

    query = ' ' + ' '.join(corrected_tokens) + ' '
    
    method = None
    category = None
    
    for m, aliases in NUMERICAL_METHOD_ALIASES.items():
        for alias in sorted(aliases, key=len, reverse=True):
            if f' {alias} ' in query:
                method = m
                break
        if method:
            break
            
    if method:
        for cat, methods in NUMERICAL_CATEGORIES.items():
            if method in methods:
                category = cat
                break
                
    return {
        "status": "success" if method else "ambiguous",
        "language": "cpp",
        "domain": "numerical",
        "intent": "code_generation",
        "structure": None,
        "operation": method,
        "operation_action": None,
        "operation_position": None,
        "operation_negated": False,
        "target_value": None,
        "target_index": None,
        "is_compound": False,
        "detected_actions": [],
        "sequencing_marker": None,
        "numerical_method": method,
        "numerical_category": category,
        "confidence": 1.0 if method else 0.0,
        "confidence_basis": "fuzzy_match" if was_corrected else "exact_rule_match",
        "error_code": None if method else "AMBIGUOUS_OPERATION",
        "message": "Numerical method identified successfully" if method else "Unknown numerical method",
        "raw_query": raw_query,
        "normalized_query": normalized_query
    }
