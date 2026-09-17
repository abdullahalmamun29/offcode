try:
    from python_parser.vocabulary import CONTRASTIVE_MARKERS, SEQUENTIAL_MARKERS
except ImportError:
    from vocabulary import CONTRASTIVE_MARKERS, SEQUENTIAL_MARKERS

def analyze_compound(tokens, tags, intent_result):
    query = ' ' + ' '.join(tokens) + ' '
    
    if intent_result['intent'] == 'conceptual_question':
        return {
            'is_compound': False,
            'detected_actions': [],
            'sequencing_marker': None,
            'operation_negated': False
        }

    # Menu-driven queries and interactive selection queries are program composition mode, not unsupported compound sequences
    is_menu_candidate = not intent_result.get('forbid_menu', False) and (
        'menu' in tokens or 'menudriven' in tokens or
        any(m in query for m in [
            ' menu ', ' menu driven ', ' menu-driven ', ' with menu ', ' menu program ', ' menu for ',
            ' through a menu ', ' interactive ', ' choose between ', ' choose whether ',
            ' user should choose ', ' user can choose ', ' repeatedly select ',
            ' select which operation ', ' select the operation ', ' choose another operation ',
            ' every time i run ', ' choose push ', ' choose pop ', ' select the sorting ', ' select which algorithm ',
            ' user must choose ', ' user chooses ', ' chooses sorting ', ' choose the algorithm ', ' choose which algorithm ', ' choose an algorithm '
        ])
    )
    if is_menu_candidate:
        return {
            'is_compound': False,
            'detected_actions': list(set(a['action'] for a in tags['actions'])),
            'sequencing_marker': None,
            'operation_negated': False
        }
        
    has_contrastive = False
    for marker in CONTRASTIVE_MARKERS:
        if f' {marker} ' in query:
            has_contrastive = True
            break
            
    distinct_actions = set(a['action'] for a in tags['actions'])
    distinct_positions = set(p['position'] for p in tags['positions'])
    
    sequencing_marker = None
    for marker in SEQUENTIAL_MARKERS:
        if f' {marker} ' in query:
            sequencing_marker = marker
            break
            
    is_compound = False
    if len(distinct_actions) > 1:
        is_compound = True
    elif len(distinct_positions) > 1 and not has_contrastive:
        is_compound = True
    elif sequencing_marker:
        is_compound = True
        
    if has_contrastive and len(distinct_actions) <= 1:
        is_compound = False
        
    if ' and ' in query and len(distinct_actions) > 1 and not has_contrastive:
        is_compound = True
        sequencing_marker = 'and'
            
    return {
        'is_compound': is_compound,
        'detected_actions': list(distinct_actions),
        'sequencing_marker': sequencing_marker,
        'operation_negated': False 
    }
