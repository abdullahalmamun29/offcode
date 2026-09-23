"""
Independent Reference Python Mathematical Oracles for Phase 3P Number Theory.

All implementations are independently derived directly from pure mathematical definitions
without sharing generator code.
"""

from typing import Tuple, List, Optional
import math


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Computes (g, x, y) such that a*x + b*y = g = gcd(a, b) with g >= 0.
    """
    if b == 0:
        if a >= 0:
            return (a, 1, 0)
        else:
            return (-a, -1, 0)
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)


def solve_diophantine(a: int, b: int, c: int) -> Optional[Tuple[int, int, int, int, int]]:
    """
    Solves a*x + b*y = c. Returns (x0, y0, step_x, step_y, g) or None if unsolvable.
    General solution: x = x0 + step_x * t, y = y0 + step_y * t.
    """
    if a == 0 and b == 0:
        if c == 0:
            return (0, 0, 0, 0, 0)
        return None
    g, x, y = extended_gcd(a, b)
    if c % g != 0:
        return None
    factor = c // g
    x0 = x * factor
    y0 = y * factor
    step_x = b // g
    step_y = -(a // g)
    return (x0, y0, step_x, step_y, g)


def modular_inverse(a: int, m: int) -> Optional[int]:
    """
    Computes a^(-1) mod m where m > 1. Returns None if gcd(a, m) != 1.
    """
    if m <= 1:
        return None
    a = (a % m + m) % m
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return (x % m + m) % m


def chinese_remainder_pair(r1: int, m1: int, r2: int, m2: int) -> Optional[Tuple[int, int]]:
    """
    Merges x = r1 mod m1 and x = r2 mod m2 for general (possibly non-coprime) moduli.
    Returns (merged_residue, merged_modulus) or None if unsolvable.
    """
    g, p, _ = extended_gcd(m1, m2)
    diff = r2 - r1
    if diff % g != 0:
        return None
    step = m2 // g
    k = ((diff // g) % step * (p % step)) % step
    k = (k + step) % step
    merged_m = (m1 // g) * m2
    merged_r = (r1 + m1 * k) % merged_m
    return (merged_r, merged_m)


def chinese_remainder(congruences: List[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    """
    Solves x = r_i mod m_i for a list of (r_i, m_i).
    """
    if not congruences:
        return (0, 1)
    cur_r, cur_m = congruences[0]
    cur_r = (cur_r % cur_m + cur_m) % cur_m
    for r, m in congruences[1:]:
        r = (r % m + m) % m
        res = chinese_remainder_pair(cur_r, cur_m, r, m)
        if res is None:
            return None
        cur_r, cur_m = res
    return (cur_r, cur_m)


def linear_sieve(n: int) -> Tuple[List[int], List[int]]:
    """
    Euler's linear sieve up to N.
    Returns (primes, spf) where spf[x] is minimum prime factor of x.
    """
    spf = [0] * (n + 1)
    primes = []
    for i in range(2, n + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
        for p in primes:
            if p > spf[i] or i * p > n:
                break
            spf[i * p] = p
    return (primes, spf)


def euler_totient_single(n: int) -> int:
    """
    Computes phi(N) via O(sqrt(N)) trial factorization.
    """
    if n <= 0:
        return 0
    ans = n
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            while temp % d == 0:
                temp //= d
            ans -= ans // d
        d += 1
    if temp > 1:
        ans -= ans // temp
    return ans


def euler_totient_range(n: int) -> List[int]:
    """
    Computes phi(1..N) table via linear sieve in strictly O(N) time.
    """
    phi = [0] * (n + 1)
    phi[1] = 1
    spf = [0] * (n + 1)
    primes = []
    for i in range(2, n + 1):
        if spf[i] == 0:
            spf[i] = i
            phi[i] = i - 1
            primes.append(i)
        for p in primes:
            if p > spf[i] or i * p > n:
                break
            spf[i * p] = p
            if i % p == 0:
                phi[i * p] = phi[i] * p
            else:
                phi[i * p] = phi[i] * (p - 1)
    return phi


def mobius_range(n: int) -> List[int]:
    """
    Computes mu(1..N) table via linear sieve in strictly O(N) time.
    """
    mu = [0] * (n + 1)
    mu[1] = 1
    spf = [0] * (n + 1)
    primes = []
    for i in range(2, n + 1):
        if spf[i] == 0:
            spf[i] = i
            mu[i] = -1
            primes.append(i)
        for p in primes:
            if p > spf[i] or i * p > n:
                break
            spf[i * p] = p
            if i % p == 0:
                mu[i * p] = 0
            else:
                mu[i * p] = -mu[i]
    return mu


def coprime_pairs_grid(n: int, m: int) -> int:
    """
    Counts pairs (i, j) with 1 <= i <= n, 1 <= j <= m such that gcd(i, j) == 1.
    Uses sum_{d=1}^{min(n, m)} mu(d) * floor(n/d) * floor(m/d).
    """
    lim = min(n, m)
    mu = mobius_range(lim)
    total = 0
    for d in range(1, lim + 1):
        if mu[d] != 0:
            total += mu[d] * (n // d) * (m // d)
    return total


def matrix_multiply(A: List[List[int]], B: List[List[int]], mod: int) -> List[List[int]]:
    d = len(A)
    C = [[0] * d for _ in range(d)]
    for i in range(d):
        for k in range(d):
            if A[i][k] == 0:
                continue
            for j in range(d):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C


def matrix_power(A: List[List[int]], k: int, mod: int) -> List[List[int]]:
    d = len(A)
    res = [[1 if i == j else 0 for j in range(d)] for i in range(d)]
    base = [row[:] for row in A]
    while k > 0:
        if k & 1:
            res = matrix_multiply(res, base, mod)
        base = matrix_multiply(base, base, mod)
        k >>= 1
    return res


def combinations_mod_p(n: int, k: int, p: int) -> int:
    """
    Computes nCr mod p for prime p with 0 <= k <= n < p.
    """
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    num = 1
    den = 1
    for i in range(1, k + 1):
        num = (num * (n - i + 1)) % p
        den = (den * i) % p
    inv_den = modular_inverse(den, p)
    return (num * inv_den) % p


def lucas_theorem(n: int, k: int, p: int) -> int:
    """
    Computes nCr mod p for arbitrary n, k >= 0 and prime p.
    """
    if k < 0 or k > n:
        return 0
    ans = 1
    while n > 0 or k > 0:
        ni = n % p
        ki = k % p
        if ki > ni:
            return 0
        ans = (ans * combinations_mod_p(ni, ki, p)) % p
        n //= p
        k //= p
    return ans


def power_mod(base: int, exp: int, mod: int) -> int:
    res = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            res = (res * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return res


def miller_rabin_deterministic(n: int) -> bool:
    """
    Deterministic Miller-Rabin primality test for all n < 2^64.
    Uses exact 7-witness basis: [2, 325, 9375, 28178, 450775, 9780504, 1795265022].
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    witnesses = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
    for a in witnesses:
        if a % n == 0:
            continue
        x = power_mod(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composite = True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                composite = False
                break
        if composite:
            return False
    return True
