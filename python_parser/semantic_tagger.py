try:
    from python_parser.vocabulary import STRUCTURE_ALIASES, ACTION_ALIASES, POSITION_ALIASES, CONTRASTIVE_MARKERS
except ImportError:
    from vocabulary import STRUCTURE_ALIASES, ACTION_ALIASES, POSITION_ALIASES, CONTRASTIVE_MARKERS

def extract_semantics(tokens):
    query = ' ' + ' '.join(tokens) + ' '
    
    tags = {
        'structure': None,
        'actions': [],
        'positions': [],
        'target_value': None,
        'target_index': None
    }
    
    # Extract structure
    all_struct_aliases = []
    for struct_id, aliases in STRUCTURE_ALIASES.items():
        for alias in aliases:
            all_struct_aliases.append((alias, struct_id))
            
    all_struct_aliases.sort(key=lambda x: len(x[0]), reverse=True)
    
    for alias, struct_id in all_struct_aliases:
        if f' {alias} ' in query:
            tags['structure'] = struct_id
            query = query.replace(f' {alias} ', ' ') # consume
            break
            
    # Extract index/value
    for i, token in enumerate(tokens):
        if token.isdigit():
            # context to check if index or value
            prev = tokens[i-1] if i > 0 else ""
            if prev in ['index', 'position']:
                tags['target_index'] = int(token)
            else:
                tags['target_value'] = int(token)
                
    # Extract actions and positions
    # Need to match longest aliases first so "push_back" matches before "push"
    all_action_aliases = []
    for action_alias, (canonical_action, default_position) in ACTION_ALIASES.items():
        all_action_aliases.append((action_alias, canonical_action, default_position))
    all_action_aliases.sort(key=lambda x: len(x[0]), reverse=True)
    
    for action_alias, canonical_action, default_position in all_action_aliases:
        if f' {action_alias} ' in query:
            tags['actions'].append({
                'action': canonical_action,
                'default_position': default_position,
                'alias': action_alias
            })
            query = query.replace(f' {action_alias} ', ' ')
            query = query.replace(f' {action_alias.replace("_", " ")} ', ' ') # consume action so it doesn't double count
            
    all_pos_aliases = []
    for pos_id, aliases in POSITION_ALIASES.items():
        for alias in aliases:
            all_pos_aliases.append((alias, pos_id))
    all_pos_aliases.sort(key=lambda x: len(x[0]), reverse=True)
    
    for alias, pos_id in all_pos_aliases:
        if f' {alias} ' in query:
            tags['positions'].append({
                'position': pos_id,
                'alias': alias
            })
            query = query.replace(f' {alias} ', ' ') # consume position
                
    return tags
