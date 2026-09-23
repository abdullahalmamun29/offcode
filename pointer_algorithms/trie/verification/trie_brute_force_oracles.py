"""
Independent Brute-Force Oracles for Trie Domain (Phase 3D).

These functions serve as ground truth for all Trie benchmark and property verification.
None of these functions use a Trie; they use naive linear scans, direct string checks,
and exhaustive combinatorial loops.
"""

from typing import List, Optional

def oracle_trie_search(words: List[str], target: str) -> bool:
    """Linear search for exact word existence."""
    return target in words

def oracle_trie_starts_with(words: List[str], prefix: str) -> bool:
    """Linear search for any word having the given prefix."""
    for w in words:
        if w.startswith(prefix):
            return True
    return False

def oracle_count_words_equal_to(words: List[str], target: str) -> int:
    """Exact count of occurrences of target in words list."""
    count = 0
    for w in words:
        if w == target:
            count += 1
    return count

def oracle_count_words_starting_with(words: List[str], prefix: str) -> int:
    """Count how many words start with the given prefix."""
    count = 0
    for w in words:
        if w.startswith(prefix):
            count += 1
    return count

def oracle_trie_deletion(words: List[str], to_delete: str) -> List[str]:
    """Simulates deletion of one instance of to_delete from words list."""
    copy = list(words)
    if to_delete in copy:
        copy.remove(to_delete)
    return copy

def oracle_longest_common_prefix(words: List[str]) -> str:
    """Finds longest common prefix across all words using naive pairwise inspection."""
    if not words:
        return ""
    prefix = words[0]
    for w in words[1:]:
        while not w.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix

def oracle_max_xor_pair(nums: List[int]) -> int:
    """Brute force O(N^2) pairwise XOR scan for maximum XOR value."""
    if len(nums) < 2:
        return 0
    max_xor = 0
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            val = nums[i] ^ nums[j]
            if val > max_xor:
                max_xor = val
    return max_xor

def oracle_max_xor_query(nums: List[int], query: int) -> int:
    """Brute force O(N) scan for maximum XOR with a query number."""
    if not nums:
        return 0
    max_xor = 0
    for x in nums:
        val = x ^ query
        if val > max_xor:
            max_xor = val
    return max_xor

def oracle_lexicographic_sort(words: List[str]) -> List[str]:
    """Returns words in standard lexicographical order."""
    return sorted(words)

def oracle_autocomplete(words: List[str], prefix: str, limit: int = 10) -> List[str]:
    """Returns up to limit words starting with prefix, in lexicographical order."""
    matching = [w for w in words if w.startswith(prefix)]
    matching.sort()
    return matching[:limit]
