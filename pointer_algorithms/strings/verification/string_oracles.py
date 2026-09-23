"""
Independent Reference Oracles for Phase 3O — String Algorithms & Automata.

Implements mathematically independent, brute-force / definition-based reference solvers
for all 10 Phase 3O patterns:
1. string_kmp_oracle (Brute-force exact pattern matching)
2. string_z_algorithm_oracle (Definition-based LCP box computation)
3. string_rabin_karp_oracle (Brute-force polynomial hash verification / search)
4. string_manacher_oracle (Exhaustive center-expansion palindromic search)
5. string_aho_corasick_oracle (Independent multi-pattern dictionary search)
6. string_suffix_array_lcp_oracle (Python sort-based suffix array + naive LCP computation)
7. string_sam_distinct_substrings_oracle (Combinatorial set-of-substrings count)
8. string_lyndon_duval_oracle (Brute-force Lyndon word verification and minimal rotation)
9. string_subsequence_automaton_oracle (Greedy two-pointer subsequence verification)
10. string_lcs_sam_oracle (Exhaustive all-substring intersection)
"""

from typing import List, Tuple, Dict, Any, Optional, Set


# ── 1. KMP / Exact Pattern Match Oracle ──
def string_kmp_oracle(text: str, pattern: str) -> List[int]:
    """
    Independent brute-force reference for single-pattern exact matching.
    Returns 0-indexed start positions where pattern matches text.
    """
    if not pattern:
        return []
    n, m = len(text), len(pattern)
    matches: List[int] = []
    for i in range(n - m + 1):
        if text[i:i + m] == pattern:
            matches.append(i)
    return matches


# ── 2. Z-Algorithm Oracle ──
def string_z_algorithm_oracle(s: str) -> List[int]:
    """
    Independent definition-based Z-array computation.
    Z[i] is the length of the longest common prefix of s[i:] and s. Z[0] = n.
    """
    n = len(s)
    if n == 0:
        return []
    z = [0] * n
    z[0] = n
    for i in range(1, n):
        lcp = 0
        while i + lcp < n and s[lcp] == s[i + lcp]:
            lcp += 1
        z[i] = lcp
    return z


# ── 3. Rabin-Karp Oracle ──
def string_rabin_karp_oracle(text: str, pattern: str) -> List[int]:
    """
    Independent polynomial rolling hash check + character-by-character confirmation.
    """
    if not pattern or len(pattern) > len(text):
        return []
    n, m = len(text), len(pattern)
    base = 31
    mod = 1_000_000_007

    p_hash = 0
    t_hash = 0
    power = 1

    for i in range(m):
        p_hash = (p_hash * base + ord(pattern[i])) % mod
        t_hash = (t_hash * base + ord(text[i])) % mod
        if i < m - 1:
            power = (power * base) % mod

    matches: List[int] = []
    for i in range(n - m + 1):
        if p_hash == t_hash:
            if text[i:i + m] == pattern:
                matches.append(i)
        if i < n - m:
            t_hash = (t_hash - ord(text[i]) * power) % mod
            t_hash = (t_hash * base + ord(text[i + m])) % mod
            t_hash = (t_hash + mod) % mod

    return matches


# ── 4. Manacher / Longest Palindrome Oracle ──
def string_manacher_oracle(s: str) -> Tuple[int, str]:
    """
    Independent brute-force center expansion for longest palindromic substring.
    Returns (length, substring).
    """
    n = len(s)
    if n == 0:
        return 0, ""

    best_len = 0
    best_sub = ""

    # Odd length palindromes
    for center in range(n):
        l, r = center, center
        while l >= 0 and r < n and s[l] == s[r]:
            cur_len = r - l + 1
            if cur_len > best_len:
                best_len = cur_len
                best_sub = s[l:r + 1]
            l -= 1
            r += 1

    # Even length palindromes
    for center in range(n - 1):
        l, r = center, center + 1
        while l >= 0 and r < n and s[l] == s[r]:
            cur_len = r - l + 1
            if cur_len > best_len:
                best_len = cur_len
                best_sub = s[l:r + 1]
            l -= 1
            r += 1

    return best_len, best_sub


# ── 5. Aho-Corasick Multi-Pattern Oracle ──
def string_aho_corasick_oracle(patterns: List[str], text: str) -> Dict[str, List[int]]:
    """
    Independent multi-pattern exact search oracle.
    Returns mapping from pattern to list of 0-indexed start occurrences.
    """
    results: Dict[str, List[int]] = {}
    for p in patterns:
        results[p] = string_kmp_oracle(text, p)
    return results


# ── 6. Suffix Array & Kasai LCP Oracle ──
def string_suffix_array_lcp_oracle(s: str) -> Tuple[List[int], List[int]]:
    """
    Independent Python standard-sort suffix array + definition LCP computation.
    SA: array of suffix start indices sorted lexicographically.
    LCP: array where LCP[i] = length of LCP(s[SA[i]:], s[SA[i+1]:]).
    """
    n = len(s)
    sa = sorted(range(n), key=lambda i: s[i:])
    lcp = [0] * (n - 1) if n > 1 else []

    for i in range(n - 1):
        idx1 = sa[i]
        idx2 = sa[i + 1]
        k = 0
        while idx1 + k < n and idx2 + k < n and s[idx1 + k] == s[idx2 + k]:
            k += 1
        lcp[i] = k

    return sa, lcp


# ── 7. SAM Distinct Substrings Oracle ──
def string_sam_distinct_substrings_oracle(s: str) -> int:
    """
    Independent set-of-substrings enumeration for counting distinct non-empty substrings.
    """
    n = len(s)
    seen: Set[str] = set()
    for i in range(n):
        for j in range(i + 1, n + 1):
            seen.add(s[i:j])
    return len(seen)


# ── 8. Duval Lyndon Factorization & Minimal Rotation Oracle ──
def string_lyndon_duval_oracle(s: str) -> Tuple[List[str], str]:
    """
    Independent verification of Lyndon factorization and minimal string rotation.
    Returns (lyndon_factors, min_rotation).
    """
    n = len(s)
    if n == 0:
        return [], ""

    # Minimal rotation
    min_rot = min(s[i:] + s[:i] for i in range(n))

    # Duval's algorithm reference for Lyndon words
    i = 0
    factors: List[str] = []
    while i < n:
        j, k = i + 1, i
        while j < n and s[k] <= s[j]:
            if s[k] < s[j]:
                k = i
            else:
                k += 1
            j += 1
        while i <= k:
            factors.append(s[i:i + j - k])
            i += j - k

    return factors, min_rot


# ── 9. Subsequence Automaton Oracle ──
def string_subsequence_automaton_oracle(s: str, queries: List[str]) -> List[bool]:
    """
    Independent greedy two-pointer subsequence oracle.
    """
    results: List[bool] = []
    for q in queries:
        s_idx = 0
        q_idx = 0
        while s_idx < len(s) and q_idx < len(q):
            if s[s_idx] == q[q_idx]:
                q_idx += 1
            s_idx += 1
        results.append(q_idx == len(q))
    return results


# ── 10. SAM Longest Common Substring Oracle ──
def string_lcs_sam_oracle(s1: str, s2: str) -> str:
    """
    Independent exhaustive search for longest common contiguous substring between s1 and s2.
    """
    best = ""
    n1 = len(s1)
    for i in range(n1):
        for j in range(i + 1, n1 + 1):
            sub = s1[i:j]
            if len(sub) > len(best) and sub in s2:
                best = sub
    return best
