"""
Domain-specific spell corrector for CodeForge.
Uses deterministic fuzzy matching (RapidFuzz / Levenshtein) over a controlled
dictionary of computer science and data structure vocabulary.
"""

from typing import List, Tuple, Set, Optional

try:
    from rapidfuzz.distance import DamerauLevenshtein
    HAS_RAPIDFUZZ = True
except ImportError:
    HAS_RAPIDFUZZ = False

# Controlled dictionary of supported and recognizable domain keywords
DOMAIN_VOCABULARY = {
    # Data Structures
    "singly", "doubly", "linked", "list", "node", "tree", "binary",
    "stack", "queue", "graph", "array", "heap",

    # Operations / Verbs
    "insert", "add", "append", "push", "prepend", "attach", "create",
    "delete", "remove", "pop", "reverse", "invert", "search", "find",
    "traverse", "display", "print",

    # Modifiers / Positions
    "end", "tail", "last", "back", "beginning", "head", "front",
    "start", "first", "middle", "position", "element", "item",

    # Common Conjunctions / Prepositions / Connectors (pass-through)
    "a", "an", "the", "of", "to", "in", "at", "new", "data", "value",
    "and", "then", "after", "also", "with", "for", "cpp", "c"
}

def _damerau_levenshtein_distance(s1: str, s2: str) -> int:
    """Fallback pure-Python Damerau-Levenshtein distance (handles transpositions)."""
    d = {}
    len1, len2 = len(s1), len(s2)
    for i in range(-1, len1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, len2 + 1):
        d[(-1, j)] = j + 1

    for i in range(len1):
        for j in range(len2):
            cost = 0 if s1[i] == s2[j] else 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,        # deletion
                d[(i, j - 1)] + 1,        # insertion
                d[(i - 1, j - 1)] + cost  # substitution
            )
            if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + cost) # transposition

    return d[(len1 - 1, len2 - 1)]

def get_distance(s1: str, s2: str) -> int:
    """Calculates Damerau-Levenshtein distance using rapidfuzz or fallback."""
    if HAS_RAPIDFUZZ:
        return DamerauLevenshtein.distance(s1, s2)
    return _damerau_levenshtein_distance(s1, s2)

def correct_word(word: str) -> Tuple[str, bool]:
    """
    Corrects a single word if close to any word in DOMAIN_VOCABULARY.
    Returns: (corrected_word, was_corrected)
    """
    if not word or word in DOMAIN_VOCABULARY:
        return word, False

    # Numbers or pure punctuation pass through
    if word.isdigit():
        return word, False

    word_len = len(word)
    if word_len <= 3:
        max_dist = 1
    elif word_len <= 5:
        max_dist = 1
    else:
        max_dist = 2

    best_match: Optional[str] = None
    min_dist = max_dist + 1

    for candidate in DOMAIN_VOCABULARY:
        # Optimization: length difference filter
        if abs(len(candidate) - word_len) > max_dist:
            continue

        # Prevent false positives on tiny words
        if word_len <= 3 and len(candidate) <= 3:
            if word[0] != candidate[0]:
                continue

        dist = get_distance(word, candidate)
        if dist < min_dist:
            min_dist = dist
            best_match = candidate

    if best_match and min_dist <= max_dist:
        return best_match, True

    return word, False

def correct_tokens(tokens: List[str]) -> Tuple[List[str], bool]:
    """
    Applies spell correction over a list of tokens.
    Returns: (corrected_tokens, any_corrected)
    """
    corrected = []
    any_corrected = False
    for token in tokens:
        word, was_corr = correct_word(token)
        corrected.append(word)
        if was_corr:
            any_corrected = True
    return corrected, any_corrected
