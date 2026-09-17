try:
    from python_parser.vocabulary import (
        QUESTION_INDICATORS, GLOBAL_NEGATION_PATTERNS, MENU_PROHIBITION_PATTERNS,
        OPERATION_EXCLUSION_PATTERNS, NUMERICAL_DOMAIN_KEYWORDS,
        SORTING_ALIASES, SEARCHING_ALIASES, GRAPH_ALGORITHM_ALIASES
    )
except ImportError:
    from vocabulary import (
        QUESTION_INDICATORS, GLOBAL_NEGATION_PATTERNS, MENU_PROHIBITION_PATTERNS,
        OPERATION_EXCLUSION_PATTERNS, NUMERICAL_DOMAIN_KEYWORDS,
        SORTING_ALIASES, SEARCHING_ALIASES, GRAPH_ALGORITHM_ALIASES
    )

def classify_intent(tokens, raw_query):
    query = ' ' + ' '.join(tokens) + ' '
    query = query.replace(" binary search tree ", " bst ")
    raw_query_clean = ' ' + raw_query.lower() + ' '
    
    intent = "code_generation"
    for qi in QUESTION_INDICATORS:
        if f' {qi} ' in raw_query_clean or f' {qi} ' in query:
            intent = "conceptual_question"
            break
            
    import re

    forbid_menu = False
    for mp in MENU_PROHIBITION_PATTERNS:
        if mp in raw_query_clean:
            forbid_menu = True
            raw_query_clean = raw_query_clean.replace(mp, ' ')

    for oe in OPERATION_EXCLUSION_PATTERNS:
        if oe in raw_query_clean:
            raw_query_clean = raw_query_clean.replace(oe, ' ')

    # Strip clauses that specifically exclude operations, e.g. "Do not implement insert-before, delete-before..."
    raw_query_clean = re.sub(r'\b(?:do not|dont|don\'t)\s+(?:implement|include|add|use)\s+(?:any\s+)?(?:other|insert|delete|search|reverse|before|after|at)[^.\n]*', ' ', raw_query_clean)

    # Check if raw_query was ONLY a menu prohibition (e.g. "Do not create a menu.")
    words_remaining = [w for w in raw_query_clean.strip().split() if w not in ['.', ',', '!', '?', ';', 'a', 'the', '-']]
    if not words_remaining and forbid_menu:
        # Just saying "Do not create a menu." without any task
        return {
            "intent": "ambiguous",
            "is_negated": False,
            "forbid_menu": True,
            "is_contradiction": False
        }

    # Contradiction checks
    raw_lower_orig = raw_query.lower()
    has_menu_keyword = any(m in raw_lower_orig for m in [
        'menu driven', 'menu-driven', 'with menu', 'menu program', 'menu for',
        'menu based', 'a menu where', 'make a menu', 'create a menu', 'through a menu', 'a menu with'
    ])
    
    is_contradiction = False
    if has_menu_keyword and forbid_menu:
        is_contradiction = True
    elif 'runtime' in raw_lower_orig and ('do not ask the user for input' in raw_lower_orig or 'no user input' in raw_lower_orig):
        is_contradiction = True
    elif 'dynamic memory' in raw_lower_orig and ('do not allocate memory' in raw_lower_orig or 'no dynamic memory' in raw_lower_orig):
        is_contradiction = True
    elif 'use recursion' in raw_lower_orig and ('do not use recursion' in raw_lower_orig or 'without recursion' in raw_lower_orig):
        is_contradiction = True
    elif ('classes' in raw_lower_orig or 'c++ classes' in raw_lower_orig) and ('in c' in raw_lower_orig or 'program in c' in raw_lower_orig):
        is_contradiction = True
    elif 'menu' in raw_lower_orig and ('no user interaction' in raw_lower_orig or 'without user interaction' in raw_lower_orig or 'with no user interaction' in raw_lower_orig):
        is_contradiction = True

    if is_contradiction:
        return {
            "intent": "ambiguous",
            "is_negated": False,
            "forbid_menu": forbid_menu,
            "is_contradiction": True
        }

    is_negated = False
    for neg in GLOBAL_NEGATION_PATTERNS:
        if f' {neg} ' in raw_query_clean:
            is_negated = True
            break
            
    return {
        "intent": intent,
        "is_negated": is_negated,
        "forbid_menu": forbid_menu,
        "is_contradiction": False
    }

def classify_domain(tokens):
    query = ' ' + ' '.join(tokens) + ' '
    query = query.replace(" binary search tree ", " bst ")
    
    # Check numerical
    for kw in NUMERICAL_DOMAIN_KEYWORDS:
        if f' {kw} ' in query:
            return "numerical"
            
    # Check algorithm
    if any(k in query for k in [' sorting ', ' sort ']):
        return "algorithm"
    for aliases in SORTING_ALIASES.values():
        for alias in aliases:
            if f' {alias} ' in query:
                return "algorithm"
    for aliases in SEARCHING_ALIASES.values():
        for alias in aliases:
            if f' {alias} ' in query:
                return "algorithm"
    for aliases in GRAPH_ALGORITHM_ALIASES.values():
        for alias in aliases:
            if f' {alias} ' in query:
                return "algorithm"
                
    return "data_structure"
