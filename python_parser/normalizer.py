import re
try:
    from python_parser.vocabulary import CONTRACTIONS, FILLER_WORDS
except ImportError:
    from vocabulary import CONTRACTIONS, FILLER_WORDS

def normalize(query: str):
    query = query.lower()
    
    # Expand contractions
    for contraction, expansion in CONTRACTIONS.items():
        query = re.sub(r'\b' + re.escape(contraction) + r'\b', expansion, query)
    
    # Handle specific replacements
    query = query.replace('::', ' ')
    query = query.replace('@', ' at ')
    query = query.replace('(', ' ')
    query = query.replace(')', ' ')
    
    # Handle snake_case: produce both (e.g. push_back -> push_back push back)
    # Actually, to make it simple, we can just keep _ and let vocabulary check handle it,
    # but the prompt asks to produce both. Let's just add the spaces version.
    words = query.split()
    new_words = []
    for w in words:
        if '_' in w:
            new_words.append(w)
            new_words.extend(w.split('_'))
        else:
            new_words.append(w)
    query = ' '.join(new_words)
    
    # Strip other punctuation except alphanumeric and underscores
    query = re.sub(r'[^a-z0-9_ ]+', ' ', query)
    
    original_tokens = query.split()
    
    # Strip filler words
    normalized_tokens = [t for t in original_tokens if t not in FILLER_WORDS]
    
    normalized = ' '.join(normalized_tokens)
    return normalized, original_tokens, normalized_tokens
