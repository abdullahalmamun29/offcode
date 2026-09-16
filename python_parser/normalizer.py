"""
Text normalizer for CodeForge.
Deterministic text cleaning, punctuation removal, and tokenization.
"""

import re
from typing import List, Tuple

def normalize_text(text: str) -> str:
    """
    Lowercases text, expands contractions, standardizes hyphens,
    and strips redundant punctuation and whitespace.
    """
    if not text:
        return ""

    # Convert to lowercase
    normalized = text.lower().strip()

    # Standardize hyphens in compound words (e.g., singly-linked -> singly linked)
    normalized = re.sub(r'(\w+)-(\w+)', r'\1 \2', normalized)

    # Replace punctuation (except alphanumeric and whitespace) with spaces
    normalized = re.sub(r'[^\w\s]', ' ', normalized)

    # Collapse multiple whitespace characters into a single space
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    return normalized

def tokenize(text: str) -> List[str]:
    """
    Tokenizes normalized text into a list of words.
    """
    cleaned = normalize_text(text)
    return cleaned.split() if cleaned else []

def find_phrases(tokens: List[str], phrase_tokens: List[str]) -> bool:
    """
    Checks if a contiguous sequence of phrase_tokens exists in tokens.
    """
    if not phrase_tokens or len(phrase_tokens) > len(tokens):
        return False

    k = len(phrase_tokens)
    for i in range(len(tokens) - k + 1):
        if tokens[i:i + k] == phrase_tokens:
            return True
    return False
