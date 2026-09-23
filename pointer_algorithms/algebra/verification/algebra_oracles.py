"""
CHUP Phase 3Q — Independent Pure Python Reference Oracles for Algebra / Transforms.

Provides ground-truth implementations for differential stress testing and verification.
Zero shared implementation artifacts with derivation engines or C++ templates.
"""

import cmath
import math
from typing import List, Tuple, Optional


# ── 1. Fast Fourier Transform Oracle ──

def fft_oracle(a: List[int], b: List[int]) -> List[int]:
    """
    Polynomial convolution via naive polynomial product (exact oracle).
    """
    deg_a = len(a)
    deg_b = len(b)
    if deg_a == 0 or deg_b == 0:
        return []
    res = [0] * (deg_a + deg_b - 1)
    for i in range(deg_a):
        for j in range(deg_b):
            res[i + j] += a[i] * b[j]
    return res


# ── 2. Number Theoretic Transform Oracle ──

def ntt_oracle(a: List[int], b: List[int], mod: int = 998244353) -> List[int]:
    """
    Exact polynomial convolution modulo mod.
    """
    deg_a = len(a)
    deg_b = len(b)
    if deg_a == 0 or deg_b == 0:
        return []
    res = [0] * (deg_a + deg_b - 1)
    for i in range(deg_a):
        for j in range(deg_b):
            res[i + j] = (res[i + j] + a[i] * b[j]) % mod
    return res


# ── 3. Fast Walsh-Hadamard Transform Oracle (Strictly XOR) ──

def fwht_xor_oracle(a: List[int], b: List[int]) -> List[int]:
    """
    Exact bitwise XOR convolution: c[k] = sum_{i ^ j == k} a[i] * b[j].
    """
    n = max(len(a), len(b))
    # Pad to power of two
    m = 1
    while m < n:
        m <<= 1
    pad_a = a + [0] * (m - len(a))
    pad_b = b + [0] * (m - len(b))

    res = [0] * m
    for i in range(m):
        for j in range(m):
            k = i ^ j
            res[k] += pad_a[i] * pad_b[j]
    return res


# ── 4. Polynomial Inversion Oracle ──

def poly_inverse_oracle(a: List[int], n: int, mod: int = 998244353) -> List[int]:
    """
    Computes B(x) such that A(x) * B(x) == 1 (mod x^n) modulo prime mod.
    Precondition: a[0] != 0.
    """
    if not a or a[0] % mod == 0:
        raise ValueError("Constant term must be non-zero (unit)")

    b = [pow(a[0], mod - 2, mod)]
    deg = 1
    while deg < n:
        deg *= 2
        # B_new = B * (2 - A * B) mod x^deg
        cur_a = (a[:deg] + [0] * max(0, deg - len(a)))[:deg]
        # multiply cur_a * b
        ab = [0] * deg
        for i in range(len(b)):
            for j in range(min(len(cur_a), deg - i)):
                ab[i + j] = (ab[i + j] + b[i] * cur_a[j]) % mod

        two_minus_ab = [0] * deg
        two_minus_ab[0] = (2 - ab[0]) % mod
        for i in range(1, deg):
            two_minus_ab[i] = (-ab[i]) % mod

        b_new = [0] * deg
        for i in range(len(b)):
            for j in range(deg - i):
                b_new[i + j] = (b_new[i + j] + b[i] * two_minus_ab[j]) % mod
        b = b_new[:deg]

    return b[:n]


# ── 5. Real Gaussian Elimination Oracle ──

def gauss_real_oracle(
    a_mat: List[List[float]],
    b_vec: List[float],
    abs_tol: float = 1e-9
) -> Tuple[str, List[float], int, float]:
    """
    Solves A x = b over R using partial pivoting.
    Returns (status, solution, rank, det).
    """
    n = len(a_mat)
    m = len(a_mat[0]) if n > 0 else 0
    aug = [row[:] + [b_vec[i]] for i, row in enumerate(a_mat)]

    det = 1.0
    rank = 0
    row = 0
    for col in range(m):
        if row >= n:
            break
        # Partial pivoting: select max absolute element in column
        pivot_row = max(range(row, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot_row][col]) <= abs_tol:
            # Singular pivot in this column; det is 0
            det = 0.0
            continue

        if pivot_row != row:
            aug[row], aug[pivot_row] = aug[pivot_row], aug[row]
            det = -det

        det *= aug[row][col]
        pivot = aug[row][col]
        for c in range(col, m + 1):
            aug[row][c] /= pivot

        for r in range(n):
            if r != row and abs(aug[r][col]) > abs_tol:
                factor = aug[r][col]
                for c in range(col, m + 1):
                    aug[r][c] -= factor * aug[row][c]

        row += 1
        rank = row

    # Check consistency
    for r in range(rank, n):
        if abs(aug[r][m]) > abs_tol:
            return "INCONSISTENT", [], rank, det

    if rank < m:
        return "INFINITE_SOLUTIONS", [], rank, det

    sol = [aug[i][m] for i in range(m)]
    return "UNIQUE_SOLUTION", sol, rank, det


# ── 6. Modular Gaussian Elimination Oracle ──

def gauss_modular_oracle(
    a_mat: List[List[int]],
    b_vec: List[int],
    mod: int = 998244353
) -> Tuple[str, List[int], int, int]:
    """
    Solves A x = b mod prime mod.
    Returns (status, solution, rank, det).
    """
    n = len(a_mat)
    m = len(a_mat[0]) if n > 0 else 0
    aug = [[val % mod for val in row] + [b_vec[i] % mod] for i, row in enumerate(a_mat)]

    det = 1
    rank = 0
    row = 0
    for col in range(m):
        if row >= n:
            break
        pivot_row = -1
        for r in range(row, n):
            if aug[r][col] % mod != 0:
                pivot_row = r
                break
        if pivot_row == -1:
            det = 0
            continue

        if pivot_row != row:
            aug[row], aug[pivot_row] = aug[pivot_row], aug[row]
            det = (mod - det) % mod

        det = (det * aug[row][col]) % mod
        inv_pivot = pow(aug[row][col], mod - 2, mod)
        for c in range(col, m + 1):
            aug[row][c] = (aug[row][c] * inv_pivot) % mod

        for r in range(n):
            if r != row and aug[r][col] % mod != 0:
                factor = aug[r][col]
                for c in range(col, m + 1):
                    aug[r][c] = (aug[r][c] - factor * aug[row][c]) % mod

        row += 1
        rank = row

    for r in range(rank, n):
        if aug[r][m] % mod != 0:
            return "INCONSISTENT", [], rank, det

    if rank < m:
        return "INFINITE_SOLUTIONS", [], rank, det

    sol = [aug[i][m] % mod for i in range(m)]
    return "UNIQUE_SOLUTION", sol, rank, det


# ── 7. Bitset Gaussian Elimination Oracle (F_2) ──

def gauss_xor_oracle(
    a_mat: List[List[int]],
    b_vec: List[int]
) -> Tuple[str, List[int], int]:
    """
    Solves A x = b over F_2.
    Returns (status, solution, rank).
    """
    n = len(a_mat)
    m = len(a_mat[0]) if n > 0 else 0
    aug = [[val & 1 for val in row] + [b_vec[i] & 1] for i, row in enumerate(a_mat)]

    rank = 0
    row = 0
    for col in range(m):
        if row >= n:
            break
        pivot_row = -1
        for r in range(row, n):
            if aug[r][col] == 1:
                pivot_row = r
                break
        if pivot_row == -1:
            continue

        if pivot_row != row:
            aug[row], aug[pivot_row] = aug[pivot_row], aug[row]

        for r in range(n):
            if r != row and aug[r][col] == 1:
                for c in range(col, m + 1):
                    aug[r][c] ^= aug[row][c]

        row += 1
        rank = row

    for r in range(rank, n):
        if aug[r][m] == 1:
            return "INCONSISTENT", [], rank

    if rank < m:
        return "INFINITE_SOLUTIONS", [], rank

    sol = [aug[i][m] for i in range(m)]
    return "UNIQUE_SOLUTION", sol, rank


# ── 8. XOR Linear Basis Oracle ──

def linear_basis_xor_oracle(vectors: List[int], bit_width: int = 64) -> Tuple[List[int], int]:
    """
    Online echelonized basis in F_2^B.
    Returns (basis_array, max_xor_sum).
    """
    basis = [0] * bit_width
    for v in vectors:
        val = v
        for b in range(bit_width - 1, -1, -1):
            if (val >> b) & 1:
                if basis[b] == 0:
                    basis[b] = val
                    break
                val ^= basis[b]

    # Max XOR sum
    max_xor = 0
    for b in range(bit_width - 1, -1, -1):
        if (max_xor ^ basis[b]) > max_xor:
            max_xor ^= basis[b]

    return basis, max_xor


# ── 9. Berlekamp-Massey & Linear Recurrence Oracle ──

def berlekamp_massey_oracle(s: List[int], mod: int = 998244353) -> List[int]:
    """
    Finds the shortest linear recurrence polynomial C(x) generating sequence s mod prime mod.
    C(x) = 1 - c_1 x - c_2 x^2 ...
    Returns coefficients [c_1, c_2, ..., c_L] such that s_k = sum_{i=1}^L c_i * s_{k-i}.
    """
    n = len(s)
    b = [1]
    c = [1]
    l = 0
    m = 1
    b_val = 1

    for i in range(n):
        # Discrepancy d = sum_{j=0}^L c_j * s_{i-j}
        d = 0
        for j in range(len(c)):
            d = (d + c[j] * s[i - j]) % mod

        if d == 0:
            m += 1
        else:
            t = c[:]
            factor = (d * pow(b_val, mod - 2, mod)) % mod
            # c = c - factor * x^m * b
            needed_len = max(len(c), len(b) + m)
            c.extend([0] * (needed_len - len(c)))
            for j in range(len(b)):
                c[j + m] = (c[j + m] - factor * b[j]) % mod

            if 2 * l <= i:
                l = i + 1 - l
                b = t
                b_val = d
                m = 1
            else:
                m += 1

    # Convert C(x) = 1 - c_1 x - ... into recurrence coefficients [c_1, ..., c_L]
    rec = [(-c[i]) % mod for i in range(1, len(c))]
    return rec


def linear_recurrence_eval_oracle(s: List[int], n: int, mod: int = 998244353) -> int:
    """
    Evaluates the N-th term s_N of sequence s generated by its minimal recurrence.
    """
    if n < len(s):
        return s[n] % mod
    rec = berlekamp_massey_oracle(s, mod)
    k = len(rec)
    if k == 0:
        return 0

    # Polynomial modulus multiplication: compute x^N mod P(x) where P(x) = x^k - sum c_i x^{k-i}
    # Using binary exponentiation of polynomial x
    def poly_mul(p1: List[int], p2: List[int]) -> List[int]:
        res = [0] * (len(p1) + len(p2) - 1)
        for i in range(len(p1)):
            for j in range(len(p2)):
                res[i + j] = (res[i + j] + p1[i] * p2[j]) % mod
        # Reduce mod P(x)
        for i in range(len(res) - 1, k - 1, -1):
            if res[i] != 0:
                factor = res[i]
                for j in range(1, k + 1):
                    res[i - j] = (res[i - j] + factor * rec[j - 1]) % mod
                res[i] = 0
        return res[:k]

    poly = [0] * k
    poly[0] = 1  # 1
    base = [0] * k
    if k > 1:
        base[1] = 1  # x
    else:
        base[0] = rec[0] if k == 1 else 0

    exp = n
    while exp > 0:
        if exp & 1:
            poly = poly_mul(poly, base)
        base = poly_mul(base, base)
        exp >>= 1

    ans = 0
    for i in range(min(k, len(s))):
        ans = (ans + poly[i] * s[i]) % mod
    return ans


# ── 10. Lagrange Interpolation Oracle ──

def lagrange_eval_oracle(
    x_pts: List[int],
    y_pts: List[int],
    x_query: int,
    mod: int = 998244353
) -> int:
    """
    Evaluates degree-d polynomial at x_query from d+1 distinct points modulo prime mod.
    P(x) = sum_i y_i * prod_{j != i} (x - x_j) / (x_i - x_j).
    """
    k = len(x_pts)
    for i in range(k):
        if (x_query - x_pts[i]) % mod == 0:
            return y_pts[i] % mod

    ans = 0
    for i in range(k):
        num = 1
        den = 1
        for j in range(k):
            if i != j:
                num = (num * (x_query - x_pts[j])) % mod
                den = (den * (x_pts[i] - x_pts[j])) % mod
        term = (y_pts[i] * num) % mod
        term = (term * pow(den, mod - 2, mod)) % mod
        ans = (ans + term) % mod
    return ans
