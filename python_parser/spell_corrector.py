import difflib
try:
    from python_parser.vocabulary import STRUCTURE_ALIASES, ACTION_ALIASES, POSITION_ALIASES, NUMERICAL_METHOD_ALIASES, SORTING_ALIASES, SEARCHING_ALIASES, GRAPH_ALGORITHM_ALIASES
except ImportError:
    from vocabulary import STRUCTURE_ALIASES, ACTION_ALIASES, POSITION_ALIASES, NUMERICAL_METHOD_ALIASES, SORTING_ALIASES, SEARCHING_ALIASES, GRAPH_ALGORITHM_ALIASES

DOMAIN_VOCABULARY = set()
for aliases in STRUCTURE_ALIASES.values():
    for alias in aliases:
        DOMAIN_VOCABULARY.update(alias.split())
for alias in ACTION_ALIASES.keys():
    DOMAIN_VOCABULARY.update(alias.split())
for aliases in POSITION_ALIASES.values():
    for alias in aliases:
        DOMAIN_VOCABULARY.update(alias.split())
for aliases in NUMERICAL_METHOD_ALIASES.values():
    for alias in aliases:
        DOMAIN_VOCABULARY.update(alias.split())
for aliases in SORTING_ALIASES.values():
    for alias in aliases:
        DOMAIN_VOCABULARY.update(alias.split())
for aliases in SEARCHING_ALIASES.values():
    for alias in aliases:
        DOMAIN_VOCABULARY.update(alias.split())
for aliases in GRAPH_ALGORITHM_ALIASES.values():
    for alias in aliases:
        DOMAIN_VOCABULARY.update(alias.split())
DOMAIN_VOCABULARY.update([
    'list', 'last', 'structure', 'insert', 'end', 'beginning', 'element', 'node', 'value', 'item', 'data',
    'interaction', 'interactive', 'interface', 'user', 'choice', 'selection', 'select', 'program',
    'code', 'function', 'class', 'method', 'variable', 'variables', 'input', 'output', 'runtime'
])

def correct_tokens_with_context(tokens):
    corrected_tokens = []
    was_corrected = False
    
    for i, token in enumerate(tokens):
        if token in DOMAIN_VOCABULARY or token.isdigit():
            corrected_tokens.append(token)
            continue
            
        if len(token) <= 3 and token not in ['lst', 'sll', 'dll', 'cll', 'bt', 'bst', 'bfs', 'dfs']:
            corrected_tokens.append(token)
            continue
            
        context = []
        if i > 0: context.append(tokens[i-1])
        if i < len(tokens) - 1: context.append(tokens[i+1])
        
        if token == 'lst' and 'linked' in context:
            corrected_tokens.append('list')
            was_corrected = True
            continue
        elif token == 'insrt':
            corrected_tokens.append('insert')
            was_corrected = True
            continue
        elif token == 'likned':
            corrected_tokens.append('linked')
            was_corrected = True
            continue
            
        matches = difflib.get_close_matches(token, DOMAIN_VOCABULARY, n=5, cutoff=0.85)
        if matches:
            best_match = matches[0]
            
            corrected_tokens.append(best_match)
            if best_match != token:
                was_corrected = True
        else:
            corrected_tokens.append(token)
            
    return corrected_tokens, was_corrected
